# OpenBook: Interactive Online Textbooks - Server
# Copyright 2026 Sebastian Wolf, Daniel Sachada
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from unittest.mock import Mock
from unittest.mock import ANY
from unittest.mock import MagicMock
from unittest.mock import patch

from django.test import TestCase

from openbook.assistant.models.document import AssistantDocument
from openbook.assistant.models.document import AssistantDocumentChunk
from openbook.assistant.services.rag_client import RagClient
from openbook.auth.middleware.current_user import reset_current_user
from openbook.content.models.course import Course
from openbook.content.models.library_group import LibraryGroup


class RagClient_Tests(TestCase):
    """Tests for the RAG client."""

    def test_perform_rag_query_requires_indexed_documents(self):
        """Queries should not implicitly import demo data."""
        rag_client = RagClient(assistant=Mock())

        with patch(
            "openbook.assistant.services.rag_client.get_vector_connection",
            return_value=Mock(),
        ), patch.object(rag_client, "load_data") as load_data:
            with self.assertRaises(RuntimeError):
                rag_client.perform_rag_query("What is this?")

        load_data.assert_not_called()

    def test_perform_rag_query_filters_by_course(self):
        """Queries should restrict vector search to the requested course."""
        reset_current_user()
        library_group = LibraryGroup.objects.create(name="Library", slug="library")
        course = Course.objects.create(
            name="Course",
            slug="course",
            group=library_group,
        )
        document = AssistantDocument.objects.create(
            course=course,
            title="Guide",
            index_status=AssistantDocument.IndexStatusChoices.INDEXED,
        )
        chunk = AssistantDocumentChunk.objects.create(
            parent=document,
            position=0,
            content="Course context",
            embedding=b"embedding",
        )
        assistant = Mock()
        assistant.get_embedding.return_value = [0.0] * 1024
        assistant.get_user_message.return_value = "answer"
        rag_client = RagClient(assistant=assistant)
        connection = MagicMock()
        cursor = connection.cursor.return_value.__enter__.return_value
        cursor.fetchall.return_value = [(str(chunk.id), 0.1)]

        with patch(
            "openbook.assistant.services.rag_client.get_vector_connection",
            return_value=connection,
        ):
            answer = rag_client.perform_rag_query("Question?", course=course)

        self.assertEqual(answer, "answer")
        cursor.execute.assert_called_once_with(ANY, [ANY, str(course.id)])
        assistant.get_user_message.assert_called_once()
        self.assertIn(
            "Course context",
            assistant.get_user_message.call_args.args[0],
        )
