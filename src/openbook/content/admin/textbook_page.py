# OpenBook: Interactive Online Textbooks
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from __future__ import annotations

from django.utils.translation          import gettext_lazy as _

from openbook.admin                    import CustomModelAdmin
from openbook.admin                    import ImportExportModelResource
from openbook.assistant.services.textbook_sync import (
    TextbookDocumentSyncService,
)
from openbook.auth.admin.mixins.audit  import created_modified_by_fields
from openbook.auth.admin.mixins.audit  import created_modified_by_fieldset
from openbook.auth.admin.mixins.audit  import created_modified_by_filter
from openbook.auth.admin.mixins.audit  import created_modified_by_related
from ..models.textbook_page            import TextbookPage


class TextbookPageResource(ImportExportModelResource):
    class Meta:
        model  = TextbookPage
        fields = [
            "id", "delete",
            "name", "description", "text_format",
            "textbook", "parent", "position",
        ]


class TextbookPageAdmin(CustomModelAdmin):
    model               = TextbookPage
    resource_classes    = [TextbookPageResource]
    list_display        = ["name", "textbook", "parent", "position", *created_modified_by_fields]
    list_display_links  = ["name"]
    list_filter         = ["textbook", "parent", *created_modified_by_filter]
    list_select_related = ["textbook", "parent", *created_modified_by_related]
    search_fields       = ["name", "textbook__name", "parent__name"]
    ordering            = ["textbook_id", "parent_id", "position", "name"]
    readonly_fields     = ["content", *created_modified_by_fields]
    filter_horizontal   = ["skills"]

    fieldsets = [
        (None, {
            "fields": ["name", "textbook", ("parent", "position")],
        }),
        (_("Description"), {
            "classes": ["tab"],
            "fields": ["description", "text_format"],
        }),
        (_("Skills"), {
            "classes": ["tab"],
            "fields": ["skills"],
        }),
        (_("Content"), {
            "classes": ["tab"],
            "fields": ["content"],
        }),
        created_modified_by_fieldset,
    ]

    add_fieldsets = [
        (None, {
            "fields": ["name", "textbook", ("parent", "position")],
        }),
        (_("Description"), {
            "classes": ["tab"],
            "fields": ["description", "text_format"],
        }),
        (_("Skills"), {
            "classes": ["tab"],
            "fields": ["skills"],
        }),
    ]

    def save_model(self, request, obj, form, change) -> None:
        """Sync derived assistant documents after a textbook page changes."""
        previous_textbook = None

        if change and obj.pk:
            previous_textbook = TextbookPage.objects.get(pk=obj.pk).textbook

        super().save_model(request, obj, form, change)
        sync_service = TextbookDocumentSyncService()

        if previous_textbook and previous_textbook.id != obj.textbook_id:
            sync_service.sync_textbook(previous_textbook)

        sync_service.sync_textbook(obj.textbook)

    def delete_model(self, request, obj) -> None:
        """Sync derived assistant documents after a textbook page is deleted."""
        textbook = obj.textbook
        super().delete_model(request, obj)
        TextbookDocumentSyncService().sync_textbook(textbook)
