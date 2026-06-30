# OpenBook: Interactive Online Textbooks - Server
# Copyright 2026 Sebastian Wolf, Daniel Sachadä
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from unittest.mock import Mock

from django.test import SimpleTestCase

from openbook.assistant.services.llm_client import LLM_Client


class LLMClient_Tests(SimpleTestCase):
    """Tests for assistant LLM delegation behavior."""

    def _client_without_api_initialization(self) -> LLM_Client:
        client = object.__new__(LLM_Client)
        client.rag_client = Mock()
        return client

    def test_load_data_delegates_to_rag_client(self):
        """File loading should be delegated to the RAG client."""
        client = self._client_without_api_initialization()
        course = Mock()

        client.load_data("data.txt", course=course)

        client.rag_client.load_data.assert_called_once_with("data.txt", course=course)

    def test_perform_rag_query_delegates_to_rag_client(self):
        """RAG queries should be delegated to the RAG client."""
        client = self._client_without_api_initialization()
        client.rag_client.perform_rag_query.return_value = "rag answer"
        course = Mock()

        answer = client.perform_rag_query(
            "Was soll ich als naechstes lernen?",
            course=course,
            learning_context="Fortschritt: 30%",
        )

        self.assertEqual(answer, "rag answer")
        client.rag_client.perform_rag_query.assert_called_once_with(
            "Was soll ich als naechstes lernen?",
            course=course,
            learning_context="Fortschritt: 30%",
        )

    def test_retrieve_rag_context_delegates_to_rag_client(self):
        """RAG context retrieval should be delegated to the RAG client."""
        client = self._client_without_api_initialization()
        client.rag_client.retrieve_document_context.return_value = ["context"]
        course = Mock()

        context = client.retrieve_rag_context("Frage?", course=course, limit=5)

        self.assertEqual(context, ["context"])
        client.rag_client.retrieve_document_context.assert_called_once_with(
            query="Frage?",
            course=course,
            limit=5,
        )

    def test_perform_rag_query_reraises_other_rag_errors(self):
        """Unexpected RAG errors should not be hidden by the LLM client."""
        client = self._client_without_api_initialization()
        client.rag_client.perform_rag_query.side_effect = RuntimeError("Vector DB failed.")

        with self.assertRaisesMessage(RuntimeError, "Vector DB failed."):
            client.perform_rag_query("Frage?")
