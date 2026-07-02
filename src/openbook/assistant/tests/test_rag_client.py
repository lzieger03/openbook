# OpenBook: Interactive Online Textbooks - Server
# Copyright 2026 Sebastian Wolf, Daniel Sachadä
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from unittest.mock import Mock
from unittest.mock import ANY
from unittest.mock import MagicMock
from unittest.mock import patch

from django.db import DatabaseError
from django.test import TestCase

from openbook.assistant.models.document import AssistantDocument
from openbook.assistant.models.document import AssistantDocumentChunk
from openbook.assistant.services.rag_client import RagClient
from openbook.auth.middleware.current_user import reset_current_user
from openbook.content.models.course import Course
from openbook.content.models.library_group import LibraryGroup


class RagClient_Tests(TestCase):
    """Tests for the RAG client."""

    def test_perform_rag_query_falls_back_without_global_documents(self):
        """Queries without indexed global documents should use the plain LLM fallback."""
        assistant = Mock()
        assistant.get_user_message.return_value = "fallback answer"
        rag_client = RagClient(assistant=assistant)

        with patch(
            "openbook.assistant.services.rag_client.get_vector_connection",
            return_value=Mock(),
        ), patch.object(rag_client, "load_data") as load_data:
            answer = rag_client.perform_rag_query("What is this?")

        self.assertEqual(answer, "fallback answer")
        load_data.assert_not_called()
        assistant.get_embedding.assert_not_called()
        assistant.get_user_message.assert_called_once()
        self.assertIn("What is this?", assistant.get_user_message.call_args.args[0])
        self.assertNotIn("indexiert", assistant.get_user_message.call_args.args[0])

    def test_perform_rag_query_falls_back_without_course_documents(self):
        """Course queries without indexed documents should use the plain LLM fallback."""
        reset_current_user()
        library_group = LibraryGroup.objects.create(name="Library", slug="library")
        course = Course.objects.create(
            name="Course",
            slug="course",
            group=library_group,
        )
        assistant = Mock()
        assistant.get_user_message.return_value = "fallback answer"
        rag_client = RagClient(assistant=assistant)

        with patch(
            "openbook.assistant.services.rag_client.get_vector_connection",
            return_value=Mock(),
        ):
            answer = rag_client.perform_rag_query("Question?", course=course)

        self.assertEqual(answer, "fallback answer")
        assistant.get_embedding.assert_not_called()
        assistant.get_user_message.assert_called_once()
        prompt = assistant.get_user_message.call_args.args[0]
        self.assertIn("Question?", prompt)
        self.assertIn("Course", prompt)
        self.assertNotIn("indexiert", prompt)

    def test_perform_rag_query_filters_by_course(self):
        """Queries should restrict returned chunks to the requested course."""
        reset_current_user()
        library_group = LibraryGroup.objects.create(name="Library", slug="library")
        course = Course.objects.create(
            name="Course",
            slug="course",
            group=library_group,
        )
        other_course = Course.objects.create(
            name="Other Course",
            slug="other-course",
            group=library_group,
        )
        document = AssistantDocument.objects.create(
            course=course,
            title="Guide",
            index_status=AssistantDocument.IndexStatusChoices.INDEXED,
        )
        other_document = AssistantDocument.objects.create(
            course=other_course,
            title="Other Guide",
            index_status=AssistantDocument.IndexStatusChoices.INDEXED,
        )
        chunk = AssistantDocumentChunk.objects.create(
            parent=document,
            position=0,
            content="Course context",
            embedding=b"embedding",
        )
        other_chunk = AssistantDocumentChunk.objects.create(
            parent=other_document,
            position=0,
            content="Other course context",
            embedding=b"embedding",
        )
        assistant = Mock()
        assistant.get_embedding.return_value = [0.0] * 1024
        assistant.get_user_message.return_value = "answer"
        rag_client = RagClient(assistant=assistant)
        connection = MagicMock()
        cursor = connection.cursor.return_value.__enter__.return_value
        cursor.fetchall.return_value = [
            (str(other_chunk.id), 0.1),
            (str(chunk.id), 0.2),
        ]

        with patch(
            "openbook.assistant.services.rag_client.get_vector_connection",
            return_value=connection,
        ):
            answer = rag_client.perform_rag_query(
                "Question?",
                course=course,
                learning_context="Lernstand: letzte Seite Grundlagen.",
            )

        self.assertEqual(answer, "answer")
        cursor.execute.assert_called_once_with(ANY, [ANY])
        self.assertNotIn("course_id", cursor.execute.call_args.args[0])
        assistant.get_user_message.assert_called_once()
        self.assertIn(
            "Course context",
            assistant.get_user_message.call_args.args[0],
        )
        self.assertNotIn(
            "Other course context",
            assistant.get_user_message.call_args.args[0],
        )
        self.assertIn(
            "Lernstand: letzte Seite Grundlagen.",
            assistant.get_user_message.call_args.args[0],
        )

    def test_perform_rag_query_falls_back_when_vector_query_fails(self):
        """Course chat should still answer when sqlite-vec retrieval fails."""
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
        AssistantDocumentChunk.objects.create(
            parent=document,
            position=0,
            content="Course context",
            embedding=b"embedding",
        )
        assistant = Mock()
        assistant.get_embedding.return_value = [0.0] * 1024
        assistant.get_user_message.return_value = "fallback answer"
        rag_client = RagClient(assistant=assistant)
        connection = MagicMock()
        cursor = connection.cursor.return_value.__enter__.return_value
        cursor.execute.side_effect = DatabaseError(
            "An illegal WHERE constraint was provided on a vec0 auxiliary column "
            "in a KNN query."
        )

        with patch(
            "openbook.assistant.services.rag_client.get_vector_connection",
            return_value=connection,
        ):
            answer = rag_client.perform_rag_query("Question?", course=course)

        self.assertEqual(answer, "fallback answer")
        assistant.get_embedding.assert_called_once_with("Question?")
        assistant.get_user_message.assert_called_once()
        prompt = assistant.get_user_message.call_args.args[0]
        self.assertIn("Question?", prompt)
        self.assertIn("Course", prompt)
        self.assertNotIn("illegal WHERE constraint", prompt)

    def test_perform_rag_query_with_sources_returns_used_chunks(self):
        """Queries should expose the chunks used as optional source metadata."""
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
            position=4,
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
            result = rag_client.perform_rag_query_with_sources(
                "Question?",
                course=course,
            )

        self.assertEqual(result.answer, "answer")
        self.assertEqual(len(result.sources), 1)
        self.assertEqual(result.sources[0].chunk_id, str(chunk.id))
        self.assertEqual(result.sources[0].document_id, str(document.id))
        self.assertEqual(result.sources[0].document_title, "Guide")
        self.assertEqual(result.sources[0].position, 4)
