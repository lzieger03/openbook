# OpenBook: Interactive Online Textbooks
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from __future__ import annotations

from django_filters.filterset           import FilterSet
from drf_spectacular.utils              import extend_schema
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
from ..models.textbook_page             import TextbookPage


class TextbookPageSerializer(FlexFieldsModelSerializer):
    created_by  = UserField(read_only=True)
    modified_by = UserField(read_only=True)

    class Meta:
        model = TextbookPage

        fields = [
            "id",
            "textbook", "parent", "children",
            "position",
            "name", "description", "text_format",
            "content",
            "created_by", "created_at", "modified_by", "modified_at",
        ]

        read_only_fields = [
            "id",
            "children",
            "created_at", "modified_at",
        ]

        expandable_fields = {
            "textbook":    "openbook.content.viewsets.textbook.TextbookSerializer",
            "parent":      "openbook.content.viewsets.textbook_page.TextbookPageSerializer",
            "children":    ("openbook.content.viewsets.textbook_page.TextbookPageSerializer", {"many": True}),
            "created_by":  "openbook.auth.viewsets.user.UserSerializer",
            "modified_by": "openbook.auth.viewsets.user.UserSerializer",
        }


class TextbookPageFilter(CreatedModifiedByFilterMixin, FilterSet):
    class Meta:
        model  = TextbookPage
        fields = {
            "textbook": ["exact"],
            "parent":   ["exact"],
            "position": ["exact", "lte", "gte"],
            "name":     ["exact"],
            **CreatedModifiedByFilterMixin.Meta.fields,
        }


@extend_schema(
    extensions={
        "x-app-name":   "Content",
        "x-model-name": "Textbook Pages",
    }
)
@with_flex_fields_parameters()
class TextbookPageViewSet(AllowAnonymousListRetrieveViewSetMixin, ModelViewSetMixin, ModelViewSet):
    __doc__ = "Textbook Pages"

    queryset         = TextbookPage.objects.all()
    filterset_class  = TextbookPageFilter
    serializer_class = TextbookPageSerializer
    ordering         = ["textbook", "parent", "position", "name"]
    search_fields    = ["name", "description"]

    def perform_create(self, serializer) -> None:
        """Sync derived assistant documents after a page is created."""
        page = serializer.save()
        TextbookDocumentSyncService().sync_textbook(page.textbook)

    def perform_update(self, serializer) -> None:
        """Sync derived assistant documents after page content or order changes."""
        previous_textbook = serializer.instance.textbook
        page = serializer.save()
        sync_service = TextbookDocumentSyncService()

        if previous_textbook.id != page.textbook_id:
            sync_service.sync_textbook(previous_textbook)

        sync_service.sync_textbook(page.textbook)

    def perform_destroy(self, instance) -> None:
        """Sync derived assistant documents after a page is deleted."""
        textbook = instance.textbook
        instance.delete()
        TextbookDocumentSyncService().sync_textbook(textbook)
