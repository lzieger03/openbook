# OpenBook: Interactive Online Textbooks
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from __future__ import annotations

from django.db                          import transaction
from django.db.models                   import Max
from django_filters.filterset           import FilterSet
from drf_spectacular.utils              import extend_schema
from rest_framework                     import status
from rest_framework.decorators          import action
from rest_framework.response            import Response
from rest_framework.viewsets            import ModelViewSet

from openbook.assistant.services.textbook_sync import (
    TextbookDocumentSyncService,
)
from openbook.auth.filters.mixins.audit import CreatedModifiedByFilterMixin
from openbook.auth.serializers.user     import UserField
from openbook.drf.flex_serializers      import FlexFieldsModelSerializer
from openbook.drf.viewsets              import AllowAnonymousListRetrieveViewSetMixin
from openbook.drf.viewsets              import ModelViewSetMixin
from openbook.drf.viewsets              import with_flex_fields_parameters
from ..models.course_material           import CourseMaterial


class CourseMaterialSerializer(FlexFieldsModelSerializer):
    created_by  = UserField(read_only=True)
    modified_by = UserField(read_only=True)

    class Meta:
        model = CourseMaterial

        fields = [
            "id",
            "course", "textbook",
            "position",
            "page_ranges",
            "created_by", "created_at", "modified_by", "modified_at",
        ]

        read_only_fields = [
            "id",
            "page_ranges",
            "created_at", "modified_at",
        ]

        expandable_fields = {
            "course":      "openbook.content.viewsets.course.CourseSerializer",
            "textbook":    "openbook.content.viewsets.textbook.TextbookSerializer",
            "page_ranges": ("openbook.content.viewsets.course_material_page_range.CourseMaterialPageRangeSerializer", {"many": True}),
            "created_by":  "openbook.auth.viewsets.user.UserSerializer",
            "modified_by": "openbook.auth.viewsets.user.UserSerializer",
        }


class CourseMaterialFilter(CreatedModifiedByFilterMixin, FilterSet):
    class Meta:
        model  = CourseMaterial
        fields = {
            "course":   ["exact"],
            "textbook": ["exact"],
            "position": ["exact", "lte", "gte"],
            **CreatedModifiedByFilterMixin.Meta.fields,
        }


@extend_schema(
    extensions={
        "x-app-name":   "Content",
        "x-model-name": "Course Materials",
    }
)
@with_flex_fields_parameters()
class CourseMaterialViewSet(AllowAnonymousListRetrieveViewSetMixin, ModelViewSetMixin, ModelViewSet):
    __doc__ = "Course Materials"

    queryset         = CourseMaterial.objects.all()
    filterset_class  = CourseMaterialFilter
    serializer_class = CourseMaterialSerializer
    ordering         = ["course", "position"]
    search_fields    = ["course__name", "textbook__name"]

    def perform_create(self, serializer) -> None:
        """Sync a textbook document when it is attached to a course."""
        material = serializer.save()
        TextbookDocumentSyncService().sync_textbook_for_course(
            textbook=material.textbook,
            course=material.course,
        )

    def perform_update(self, serializer) -> None:
        """Keep derived documents aligned when material ownership changes."""
        previous_course = serializer.instance.course
        previous_textbook = serializer.instance.textbook
        material = serializer.save()

        sync_service = TextbookDocumentSyncService()
        if (
            previous_course.id != material.course_id
            or previous_textbook.id != material.textbook_id
        ):
            sync_service.delete_course_textbook_document(
                textbook=previous_textbook,
                course=previous_course,
            )
            sync_service.sync_textbook_for_course(
                textbook=material.textbook,
                course=material.course,
            )

    def perform_destroy(self, instance) -> None:
        """Delete the derived document when a textbook leaves a course."""
        course = instance.course
        textbook = instance.textbook
        instance.delete()
        TextbookDocumentSyncService().delete_course_textbook_document(
            textbook=textbook,
            course=course,
        )

    @extend_schema(
        request={
            "application/json": {
                "type": "object",
                "properties": {"direction": {"type": "string", "enum": ["up", "down"]}},
                "required": ["direction"],
            }
        },
        responses=CourseMaterialSerializer,
    )
    @action(detail=True, methods=["post"])
    def move(self, request, *args, **kwargs):
        """
        Swap this material with its neighbour in the syllabus.

        Reordering by directly swapping the two ``position`` values would violate the
        unique ``(course, position)`` constraint, so the swap is performed atomically
        by first parking this material on a temporary free position.
        """
        direction = (request.data or {}).get("direction")

        if direction not in ("up", "down"):
            return Response(
                {"direction": ["Must be either 'up' or 'down'."]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        material = self.get_object()

        with transaction.atomic():
            siblings = CourseMaterial.objects.select_for_update().filter(course_id=material.course_id)

            if direction == "up":
                neighbour = siblings.filter(position__lt=material.position).order_by("-position").first()
            else:
                neighbour = siblings.filter(position__gt=material.position).order_by("position").first()

            if neighbour is not None:
                material_position  = material.position
                neighbour_position = neighbour.position

                # Park this material on a temporary, unused position so neither UPDATE
                # collides with the unique (course, position) constraint mid-swap.
                temp_position = siblings.aggregate(max_position=Max("position"))["max_position"] + 1
                material.position = temp_position
                material.save(update_fields=["position"])

                neighbour.position = material_position
                neighbour.save(update_fields=["position"])

                material.position = neighbour_position
                material.save(update_fields=["position"])

        serializer = self.get_serializer(material)
        return Response(serializer.data)
