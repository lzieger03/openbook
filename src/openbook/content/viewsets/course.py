# OpenBook: Interactive Online Textbooks
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from __future__ import annotations

from pathlib import Path

from django.db                              import transaction
from django.db.models                       import Max
from django.shortcuts                       import get_object_or_404
from django.utils.text                      import slugify
from django_filters.filterset               import FilterSet
from drf_spectacular.utils                  import extend_schema
from rest_framework                         import serializers
from rest_framework                         import status
from rest_framework.decorators              import action
from rest_framework.exceptions              import PermissionDenied
from rest_framework.response                import Response
from rest_framework.viewsets                import ModelViewSet

from openbook.assistant.services.textbook_sync import (
    TextbookDocumentSyncService,
)
from ..services.chapter_extraction import ChapterExtractionError
from ..services.chapter_extraction import extract_chapters
from ..services.chapter_extraction import extract_pdf_chapters
from openbook.drf.flex_serializers          import FlexFieldsModelSerializer
from openbook.drf.viewsets                  import AllowAnonymousListRetrieveViewSetMixin
from openbook.drf.viewsets                  import ModelViewSetMixin
from openbook.drf.viewsets                  import with_flex_fields_parameters
from openbook.auth.filters.mixins.audit     import CreatedModifiedByFilterMixin
from openbook.auth.filters.mixins.scope     import ScopedRolesFilterMixin
from openbook.auth.serializers.mixins.scope import ScopedRolesSerializerMixin
from openbook.auth.serializers.user         import UserField
from ..models.course                        import Course
from ..models.course_material               import CourseMaterial
from ..models.textbook                      import Textbook
from ..models.textbook_page                 import TextbookPage


class CourseTextbookUploadSerializer(serializers.Serializer):
    """Validate a teacher upload that should become course material."""

    SUPPORTED_EXTENSIONS = {".md", ".markdown", ".html", ".htm", ".txt", ".pdf"}

    file = serializers.FileField()
    name = serializers.CharField(required=False, allow_blank=True, max_length=255)
    slug = serializers.CharField(required=False, allow_blank=True, max_length=255)
    description = serializers.CharField(required=False, allow_blank=True)

    def validate_file(self, file):
        """Allow only source formats the textbook editor can represent."""
        extension = Path(file.name).suffix.lower()

        if extension not in self.SUPPORTED_EXTENSIONS:
            raise serializers.ValidationError(
                "Supported formats are .md, .markdown, .html, .htm, .txt and .pdf."
            )

        return file


class CourseSerializer(ScopedRolesSerializerMixin, FlexFieldsModelSerializer):
    created_by  = UserField(read_only=True)
    modified_by = UserField(read_only=True)

    # Skills a learner can earn in this course: the union of the skills trained by the
    # pages of every textbook in the course. Derived (read-only) from the page-level
    # assignment so the dashboard shows exactly what quizzes here can award.
    skills      = serializers.SerializerMethodField()

    def get_skills(self, obj):
        from openbook.gamification.models import Skill
        from openbook.gamification.viewsets.skill import SkillSerializer

        earnable = (
            Skill.objects
            .filter(textbook_pages__textbook__used_in_courses__course=obj)
            .distinct()
            .order_by("name")
        )
        return SkillSerializer(earnable, many=True, context=self.context).data

    class Meta:
        model = Course

        fields = [
            "id", "slug",
            "name", "description", "text_format",
            "group", "is_template",
            "materials", "skills",
            *ScopedRolesSerializerMixin.Meta.fields,
            "created_by", "created_at", "modified_by", "modified_at",
        ]

        read_only_fields = [
            "id",
            "materials", "skills",
            *ScopedRolesSerializerMixin.Meta.read_only_fields,
            "created_at", "modified_at",
        ]

        expandable_fields = {
            **ScopedRolesSerializerMixin.Meta.expandable_fields,
            "group":       "openbook.content.viewsets.library_group.LibraryGroupSerializer",
            "materials":   ("openbook.content.viewsets.course_material.CourseMaterialSerializer", {"many": True}),
            "created_by":  "openbook.auth.viewsets.user.UserSerializer",
            "modified_by": "openbook.auth.viewsets.user.UserSerializer",
        }

class CourseFilter(CreatedModifiedByFilterMixin, ScopedRolesFilterMixin, FilterSet):
    class Meta:
        model  = Course
        fields = {
            "slug":        ["exact"],
            "name":        ["exact"],
            "group":       ["exact"],
            "is_template": ["exact"],
            **ScopedRolesFilterMixin.Meta.fields,
            **CreatedModifiedByFilterMixin.Meta.fields,
        }

@extend_schema(
    extensions={
        "x-app-name":   "Courses",
        "x-model-name": "Courses",
    }
)
@with_flex_fields_parameters()
class CourseViewSet(AllowAnonymousListRetrieveViewSetMixin, ModelViewSetMixin, ModelViewSet):
    __doc__ = "Courses"

    queryset         = Course.objects.all()
    filterset_class  = CourseFilter
    serializer_class = CourseSerializer
    ordering         = ["group", "name"]
    search_fields    = ["slug", "name", "description"]

    @extend_schema(
        request=CourseTextbookUploadSerializer,
        responses={
            status.HTTP_201_CREATED: {
                "type": "object",
                "properties": {
                    "textbook": {"type": "string", "format": "uuid"},
                    "material": {"type": "string", "format": "uuid"},
                    "document": {"type": "string", "format": "uuid"},
                    "index_status": {"type": "string"},
                    "pages_created": {"type": "integer"},
                    "chapters": {"type": "array", "items": {"type": "string"}},
                },
            },
        },
    )
    @action(detail=True, methods=["post"], url_path="upload_textbook")
    def upload_textbook(self, request, *args, **kwargs):
        """Create course material from an uploaded source file and sync it to RAG."""
        course = get_object_or_404(Course, pk=kwargs["pk"])

        if not request.user.has_perm("openbook_content.change_course", course):
            raise PermissionDenied("You are not allowed to upload content for this course.")

        serializer = CourseTextbookUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uploaded_file = serializer.validated_data["file"]
        filename = Path(uploaded_file.name)
        name = serializer.validated_data.get("name", "").strip() or filename.stem
        raw_bytes = uploaded_file.read()

        # Split the uploaded script into chapters so each one becomes its own page.
        # A document without recognizable headings yields a single chapter, so the
        # whole file still ends up as one readable page.
        if filename.suffix.lower() == ".pdf":
            # PDF text is extracted and kept as Markdown (line breaks are preserved
            # by the renderer); chapters come from the PDF outline or detected headings.
            text_format = Textbook.TextFormatChoices.MARKDOWN
            try:
                chapters = extract_pdf_chapters(raw_bytes)
            except ChapterExtractionError as error:
                raise serializers.ValidationError({"file": str(error)})
        else:
            text_format = self._format_from_filename(filename.name)
            source = raw_bytes.decode("utf-8", errors="replace")
            if not source.strip():
                raise serializers.ValidationError({
                    "file": "Uploaded file must contain text content.",
                })
            chapters = extract_chapters(source, text_format)

        if not chapters:
            raise serializers.ValidationError({
                "file": "Uploaded file did not produce textbook page content.",
            })

        with transaction.atomic():
            textbook = Textbook.objects.create(
                group=course.group,
                name=name,
                slug=serializer.validated_data.get("slug", "").strip()
                or slugify(name)
                or "textbook",
                description=serializer.validated_data.get("description", "").strip(),
                text_format=text_format,
            )
            material = CourseMaterial.objects.create(
                course=course,
                textbook=textbook,
                position=self._next_material_position(course),
            )
            for position, chapter in enumerate(chapters, start=1):
                # A single untitled chapter inherits the textbook name; otherwise fall
                # back to a numbered title when the extractor found no heading text.
                page_name = chapter.title or (
                    name if len(chapters) == 1 else f"Chapter {position}"
                )
                TextbookPage.objects.create(
                    textbook=textbook,
                    position=position,
                    name=page_name[:255],
                    text_format=text_format,
                    content={
                        "type": "source",
                        "format": text_format,
                        "source": chapter.source,
                        "filename": filename.name,
                    },
                )

        document = TextbookDocumentSyncService().sync_textbook_for_course(
            textbook=textbook,
            course=course,
        )
        if document is None:
            raise serializers.ValidationError({
                "file": "Uploaded file did not produce textbook page content.",
            })

        return Response(
            {
                "textbook": str(textbook.id),
                "material": str(material.id),
                "document": str(document.id),
                "index_status": document.index_status,
                "pages_created": len(chapters),
                "chapters": [
                    chapter.title or f"Chapter {position}"
                    for position, chapter in enumerate(chapters, start=1)
                ],
            },
            status=status.HTTP_201_CREATED,
        )

    def _format_from_filename(self, filename: str) -> str:
        """Infer the OpenBook source format from a filename."""
        lower_filename = filename.lower()

        if lower_filename.endswith((".html", ".htm")):
            return Textbook.TextFormatChoices.HTML

        if lower_filename.endswith(".txt"):
            return Textbook.TextFormatChoices.PLAIN_TEXT

        return Textbook.TextFormatChoices.MARKDOWN

    def _next_material_position(self, course: Course) -> int:
        """Return the next free material position for a course."""
        max_position = CourseMaterial.objects.filter(course=course).aggregate(
            max_position=Max("position")
        )["max_position"]
        return (max_position or 0) + 1
