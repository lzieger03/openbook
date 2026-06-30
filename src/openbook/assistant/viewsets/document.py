# OpenBook: Interactive Online Textbooks - Server
# Copyright 2026 Sebastian Wolf, Daniel Sachadä
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from __future__ import annotations

from pathlib import Path

from django.conf import settings
from django.http import FileResponse
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_filters.filterset import FilterSet
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.viewsets import ModelViewSet

from openbook.auth.filters.mixins.audit import CreatedModifiedByFilterMixin
from openbook.auth.serializers.user import UserField
from openbook.assistant.services.textbook_sync import (
    TextbookDocumentSyncService,
)
from openbook.drf.flex_serializers import FlexFieldsModelSerializer
from openbook.drf.viewsets import ModelViewSetMixin
from openbook.drf.viewsets import with_flex_fields_parameters

from ..models.document import AssistantDocument


class AssistantDocumentSerializer(FlexFieldsModelSerializer):
    """Serializer for course-scoped assistant documents."""

    created_by = UserField(read_only=True)
    modified_by = UserField(read_only=True)
    download_url = serializers.SerializerMethodField()

    class Meta:
        model = AssistantDocument

        fields = [
            "id",
            "course",
            "textbook",
            "title",
            "file_data",
            "file_name",
            "file_size",
            "mime_type",
            "download_url",
            "index_status",
            "index_error",
            "indexed_at",
            "embedding_model",
            "chunk_count",
            "created_by",
            "created_at",
            "modified_by",
            "modified_at",
        ]

        read_only_fields = [
            "id",
            "file_name",
            "file_size",
            "mime_type",
            "download_url",
            "index_status",
            "index_error",
            "indexed_at",
            "embedding_model",
            "chunk_count",
            "created_at",
            "modified_at",
        ]

        expandable_fields = {
            "course": "openbook.content.viewsets.course.CourseSerializer",
            "textbook": "openbook.content.viewsets.textbook.TextbookSerializer",
            "created_by": "openbook.auth.viewsets.user.UserSerializer",
            "modified_by": "openbook.auth.viewsets.user.UserSerializer",
        }

    def validate(self, attrs):
        """Require an uploaded file when creating assistant documents."""
        attrs = super().validate(attrs)

        if self.instance is None and not attrs.get("file_data"):
            raise serializers.ValidationError({
                "file_data": _("An assistant document upload is required."),
            })

        return attrs

    def get_download_url(self, obj: AssistantDocument) -> str:
        """Return the authenticated download URL for this document."""
        if not obj.file_data:
            return ""

        path = reverse("assistant-document-download", args=[obj.pk])
        request = self.context.get("request")

        if request is None:
            return path

        return request.build_absolute_uri(path)


class AssistantDocumentFilter(CreatedModifiedByFilterMixin, FilterSet):
    class Meta:
        model = AssistantDocument
        fields = {
            "course": ["exact", "isnull"],
            "textbook": ["exact", "isnull"],
            "title": ["exact"],
            "file_name": ["exact"],
            "mime_type": ["exact"],
            "index_status": ["exact"],
            **CreatedModifiedByFilterMixin.Meta.fields,
        }


@extend_schema(
    extensions={
        "x-app-name": "Assistant",
        "x-model-name": "Assistant Documents",
    }
)
@with_flex_fields_parameters()
class AssistantDocumentViewSet(ModelViewSetMixin, ModelViewSet):
    """Assistant documents available to the current user."""

    queryset = AssistantDocument.objects.all()
    serializer_class = AssistantDocumentSerializer
    filterset_class = AssistantDocumentFilter
    ordering = ["course", "title", "file_name"]
    search_fields = ["title", "file_name", "course__name", "textbook__name"]

    @extend_schema(responses=OpenApiTypes.BINARY)
    @action(detail=True, methods=["get"])
    def download(self, request, *args, **kwargs):
        """Download the current file backing an assistant document."""
        document = self.get_object()

        if not document.file_data:
            raise NotFound(_("This document has no downloadable file."))

        filename = Path(document.file_name or document.file_data.name).name
        document.file_data.open("rb")
        return FileResponse(
            document.file_data,
            as_attachment=True,
            filename=filename,
        )

    def perform_create(self, serializer) -> None:
        """Save the upload and start synchronous indexing when configured."""
        document = serializer.save()
        self._index_document_if_possible(document)

    def perform_update(self, serializer) -> None:
        """Reindex when file data or course assignment changes."""
        should_reindex = {"file_data", "course"}.intersection(serializer.validated_data)
        document = serializer.save()

        if should_reindex:
            self._index_document_if_possible(document)

    def _index_document_if_possible(self, document: AssistantDocument) -> None:
        """Index document contents or store a configuration error."""
        if not document.file_data:
            TextbookDocumentSyncService().clear_document_index(document)
            document.index_status = AssistantDocument.IndexStatusChoices.PENDING
            document.index_error = ""
            document.chunk_count = 0
            document.indexed_at = None
            document.save(
                update_fields=[
                    "index_status",
                    "index_error",
                    "chunk_count",
                    "indexed_at",
                    "modified_at",
                ]
            )
            return

        if not getattr(settings, "MISTRAL_API_KEY", ""):
            TextbookDocumentSyncService().clear_document_index(document)
            document.mark_index_failed("MISTRAL_API_KEY is not set.")
            document.save(
                update_fields=[
                    "index_status",
                    "index_error",
                    "chunk_count",
                    "indexed_at",
                    "modified_at",
                ]
            )
            return

        from openbook.assistant.services.llm_client import LLM_Client

        try:
            LLM_Client()._get_rag_client().index_document(document)
        except Exception as error:
            TextbookDocumentSyncService().clear_document_index(document)
            document.mark_index_failed(error)
            document.save(
                update_fields=[
                    "index_status",
                    "index_error",
                    "chunk_count",
                    "indexed_at",
                    "modified_at",
                ]
            )
