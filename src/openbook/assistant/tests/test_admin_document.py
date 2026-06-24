# OpenBook: Interactive Online Textbooks - Server
# Copyright 2026 Sebastian Wolf, Daniel Sachada
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from types import SimpleNamespace
from unittest.mock import Mock
from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import RequestFactory
from django.test import TestCase
from django.test import override_settings

from openbook.admin import admin_site
from openbook.assistant.admin.document import AssistantDocumentAdmin
from openbook.assistant.models.document import AssistantDocument
from openbook.auth.middleware.current_user import reset_current_user


class AssistantDocumentAdmin_Tests(TestCase):
    """Tests for assistant document admin behavior."""

    def setUp(self):
        reset_current_user()
        self.admin = AssistantDocumentAdmin(AssistantDocument, admin_site)
        self.request = RequestFactory().post("/admin/")

    @override_settings(MISTRAL_API_KEY="test-key")
    def test_save_model_indexes_changed_file_upload(self):
        """Changed file uploads should rebuild the assistant index."""
        document = AssistantDocument(
            title="Guide",
            file_data=SimpleUploadedFile("guide.txt", b"Hello"),
        )
        form = SimpleNamespace(changed_data=["file_data"])
        rag_client = Mock()
        llm_client = Mock()
        llm_client._get_rag_client.return_value = rag_client

        with patch(
            "openbook.assistant.services.llm_client.LLM_Client",
            return_value=llm_client,
        ), patch.object(self.admin, "message_user"):
            self.admin.save_model(self.request, document, form, change=False)

        rag_client.index_document.assert_called_once_with(document)

    @override_settings(MISTRAL_API_KEY="")
    def test_save_model_skips_indexing_without_api_key(self):
        """Missing Mistral configuration should not block saving uploads."""
        document = AssistantDocument(
            title="Guide",
            file_data=SimpleUploadedFile("guide.txt", b"Hello"),
        )
        form = SimpleNamespace(changed_data=["file_data"])

        with patch(
            "openbook.assistant.services.llm_client.LLM_Client",
        ) as llm_client, patch.object(self.admin, "message_user") as message_user:
            self.admin.save_model(self.request, document, form, change=False)

        llm_client.assert_not_called()
        message_user.assert_called_once()
