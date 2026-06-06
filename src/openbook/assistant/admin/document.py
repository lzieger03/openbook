# OpenBook: Interactive Online Textbooks - Server
# © 2026 Sebastian Wolf, Daniel Sachadä
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.conf import settings
from django.contrib import messages
from django.contrib.admin import RelatedOnlyFieldListFilter
from django.utils.translation import gettext_lazy as _
from unfold.admin import TabularInline

from openbook.admin import CustomModelAdmin
from openbook.admin import ImportExportModelResource
from openbook.auth.admin.mixins.audit import created_modified_by_fields
from openbook.auth.admin.mixins.audit import created_modified_by_fieldset
from openbook.auth.admin.mixins.audit import created_modified_by_filter
from openbook.auth.admin.mixins.audit import created_modified_by_related

from ..models.document import AssistantDocument
from ..models.document import AssistantDocumentChunk


class _AssistantDocumentChunkInline(TabularInline):
    model = AssistantDocumentChunk
    extra = 0
    show_change_link = True
    tab = True
    fields = ["position", "content"]
    readonly_fields = ["position", "content"]
    ordering = ["position"]


class AssistantDocumentResource(ImportExportModelResource):
    class Meta:
        model = AssistantDocument
        fields = [
            "id",
            "delete",
            "title",
            "file_data",
            "file_name",
            "file_size",
            "mime_type",
        ]


class AssistantDocumentChunkResource(ImportExportModelResource):
    class Meta:
        model = AssistantDocumentChunk
        fields = [
            "id",
            "delete",
            "parent",
            "position",
            "content",
        ]


class AssistantDocumentAdmin(CustomModelAdmin):
    model = AssistantDocument
    resource_classes = [AssistantDocumentResource]
    list_display = [
        "title",
        "file_name",
        "file_size",
        "mime_type",
        *created_modified_by_fields,
    ]
    list_display_links = ["title", "file_name"]
    list_filter = ["mime_type", *created_modified_by_filter]
    list_select_related = [*created_modified_by_related]
    search_fields = ["title", "file_name"]
    ordering = ["title", "file_name"]
    readonly_fields = [
        "file_name",
        "file_size",
        "mime_type",
        *created_modified_by_fields,
    ]
    inlines = [_AssistantDocumentChunkInline]

    fieldsets = [
        (None, {
            "fields": ["title", "file_data"],
        }),
        (_("File Metadata"), {
            "classes": ["tab"],
            "fields": ["file_name", "file_size", "mime_type"],
        }),
        created_modified_by_fieldset,
    ]

    add_fieldsets = [
        (None, {
            "fields": ["title", "file_data"],
        }),
    ]

    def save_model(self, request, obj, form, change) -> None:
        """Save uploaded documents and rebuild their assistant index."""
        super().save_model(request, obj, form, change)

        if "file_data" not in form.changed_data:
            return

        if not obj.file_data:
            obj.chunks.all().delete()
            return

        if not getattr(settings, "MISTRAL_API_KEY", ""):
            self.message_user(
                request,
                _(
                    "Document saved, but indexing was skipped because "
                    "MISTRAL_API_KEY is not set."
                ),
                level=messages.WARNING,
            )
            return

        from openbook.assistant.services.llm_client import LLM_Client

        try:
            LLM_Client()._get_rag_client().index_document(obj)
        except Exception as error:
            self.message_user(
                request,
                _("Document saved, but indexing failed: %(error)s") % {"error": error},
                level=messages.ERROR,
            )
            return

        self.message_user(
            request,
            _("Document indexed for assistant retrieval."),
            level=messages.SUCCESS,
        )


class AssistantDocumentChunkAdmin(CustomModelAdmin):
    model = AssistantDocumentChunk
    resource_classes = [AssistantDocumentChunkResource]
    list_display = ["parent", "position", *created_modified_by_fields]
    list_display_links = ["parent", "position"]
    list_filter = [("parent", RelatedOnlyFieldListFilter), *created_modified_by_filter]
    list_select_related = ["parent", *created_modified_by_related]
    search_fields = ["parent__title", "parent__file_name", "content"]
    ordering = ["parent", "position"]
    readonly_fields = ["embedding", *created_modified_by_fields]

    fieldsets = [
        (None, {
            "fields": ["parent", "position", "content"],
        }),
        (_("Embedding"), {
            "classes": ["tab"],
            "fields": ["embedding"],
        }),
        created_modified_by_fieldset,
    ]

    add_fieldsets = [
        (None, {
            "fields": ["parent", "position", "content", "embedding"],
        }),
    ]
