# OpenBook: Interactive Online Textbooks - Server
# Copyright 2026 Sebastian Wolf, Daniel Sachada
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from unittest.mock import Mock
from unittest.mock import patch

from django.test import TestCase

from openbook.assistant.services.rag_client import RagClient


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
