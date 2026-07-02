# OpenBook: Interactive Online Textbooks - Server
# Copyright 2026 Sebastian Wolf, Daniel Sachadä
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

import tempfile
from io import StringIO

from django.core.management import call_command
from django.test import TestCase
from django.test import override_settings

from openbook.assistant.models.document import AssistantDocument
from openbook.assistant.models.document import AssistantDocumentChunk
from openbook.assistant.services.textbook_sync import TextbookDocumentSyncService
from openbook.auth.middleware.current_user import reset_current_user
from openbook.content.models.course import Course
from openbook.content.models.course_material import CourseMaterial
from openbook.content.models.library_group import LibraryGroup
from openbook.content.models.textbook import Textbook
from openbook.content.models.textbook_page import TextbookPage


class TextbookDocumentSyncService_Tests(TestCase):
    """Tests for the TextbookDocumentSyncService."""

    def setUp(self):
        reset_current_user()
        self.media_dir = tempfile.TemporaryDirectory()
        self.settings_override = override_settings(
            MEDIA_ROOT=self.media_dir.name,
            MISTRAL_API_KEY="",
        )
        self.settings_override.enable()
        self.addCleanup(self.settings_override.disable)
        self.addCleanup(self.media_dir.cleanup)

        self.library_group = LibraryGroup.objects.create(name="Library", slug="library")
        self.course = Course.objects.create(
            name="Course",
            slug="course",
            group=self.library_group,
        )
        self.textbook = Textbook.objects.create(
            name="Textbook",
            slug="textbook",
            group=self.library_group,
        )
        CourseMaterial.objects.create(
            course=self.course,
            textbook=self.textbook,
            position=1,
        )
        self.page = TextbookPage.objects.create(
            textbook=self.textbook,
            name="Page",
            position=1,
            content={
                "type": "source",
                "format": "MD",
                "source": "Initial content",
            },
        )

    def test_sync_creates_downloadable_document(self):
        """Sync should create a generated file for the current textbook."""
        document = TextbookDocumentSyncService().sync_textbook_for_course(
            textbook=self.textbook,
            course=self.course,
        )

        self.assertEqual(document.course, self.course)
        self.assertEqual(document.textbook, self.textbook)
        self.assertEqual(document.title, "Textbook")
        self.assertTrue(document.file_data)
        self.assertEqual(document.index_status, AssistantDocument.IndexStatusChoices.FAILED)
        self.assertIn("MISTRAL_API_KEY", document.index_error)

        document.file_data.open("rb")
        try:
            content = document.file_data.read().decode("utf-8")
        finally:
            document.file_data.close()

        self.assertIn("# Textbook", content)
        self.assertIn("## Page", content)
        self.assertIn("Initial content", content)

    def test_sync_ignores_textbook_description(self):
        """Sync should use page content, not textbook description, as RAG source."""
        self.textbook.description = "Description should not be indexed."
        self.textbook.save(update_fields=["description"])

        document = TextbookDocumentSyncService().sync_textbook_for_course(
            textbook=self.textbook,
            course=self.course,
        )

        document.file_data.open("rb")
        try:
            content = document.file_data.read().decode("utf-8")
        finally:
            document.file_data.close()

        self.assertIn("Initial content", content)
        self.assertNotIn("Description should not be indexed.", content)

    def test_sync_skips_textbook_without_page_content(self):
        """Sync should not create RAG documents from metadata-only textbooks."""
        self.textbook.description = "Only metadata"
        self.textbook.save(update_fields=["description"])
        self.page.content = {}
        self.page.save(update_fields=["content"])

        document = TextbookDocumentSyncService().sync_textbook_for_course(
            textbook=self.textbook,
            course=self.course,
        )

        self.assertIsNone(document)
        self.assertFalse(
            AssistantDocument.objects.filter(
                course=self.course,
                textbook=self.textbook,
            ).exists()
        )

    def test_sync_deletes_existing_document_without_page_content(self):
        """Sync should remove stale documents when pages no longer have content."""
        sync_service = TextbookDocumentSyncService()
        document = sync_service.sync_textbook_for_course(
            textbook=self.textbook,
            course=self.course,
        )
        self.assertIsNotNone(document)

        self.page.content = {}
        self.page.save(update_fields=["content"])

        document = sync_service.sync_textbook_for_course(
            textbook=self.textbook,
            course=self.course,
        )

        self.assertIsNone(document)
        self.assertFalse(
            AssistantDocument.objects.filter(
                course=self.course,
                textbook=self.textbook,
            ).exists()
        )

    def test_resync_replaces_file_and_old_chunks(self):
        """Resync should drop stale chunks and write the latest page content."""
        sync_service = TextbookDocumentSyncService()
        document = sync_service.sync_textbook_for_course(
            textbook=self.textbook,
            course=self.course,
        )
        AssistantDocumentChunk.objects.create(
            parent=document,
            position=0,
            content="stale content",
            embedding=b"stale",
        )

        self.page.content = {
            "type": "source",
            "format": "MD",
            "source": "Updated content",
        }
        self.page.save(update_fields=["content"])

        document = sync_service.sync_textbook_for_course(
            textbook=self.textbook,
            course=self.course,
        )

        self.assertEqual(document.chunks.count(), 0)

        document.file_data.open("rb")
        try:
            content = document.file_data.read().decode("utf-8")
        finally:
            document.file_data.close()

        self.assertIn("Updated content", content)
        self.assertNotIn("Initial content", content)

    def test_sync_command_rebuilds_document_from_pages(self):
        """Management command should rebuild generated documents from page content."""
        self.textbook.description = "Description should not survive command resync."
        self.textbook.save(update_fields=["description"])
        self.page.content = {
            "type": "source",
            "format": "MD",
            "source": "Command page content",
        }
        self.page.save(update_fields=["content"])

        output = StringIO()

        call_command(
            "sync_textbook_documents",
            course=str(self.course.id),
            stdout=output,
        )

        document = AssistantDocument.objects.get(
            course=self.course,
            textbook=self.textbook,
        )
        document.file_data.open("rb")
        try:
            content = document.file_data.read().decode("utf-8")
        finally:
            document.file_data.close()

        self.assertIn("Textbook documents rebuilt: 1", output.getvalue())
        self.assertIn("Command page content", content)
        self.assertNotIn("Description should not survive command resync.", content)
