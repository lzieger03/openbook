# OpenBook: Interactive Online Textbooks - Server
# © 2026 Sebastian Wolf, Daniel Sachadä
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.conf import settings


class LLM_Client:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(LLM_Client, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "initialized"):
            api_key = settings.MISTRAL_API_KEY

            if not api_key:
                raise ValueError("MISTRAL_API_KEY is not set in settings")

            self.client = self._create_client(api_key)
            self.model = "mistral-small-latest"
            self.embedding_model = "mistral-embed"
            self.initialized = True

    def _create_client(self, api_key: str):
        try:
            from mistralai.client import Mistral
        except ImportError:
            try:
                from mistralai import Mistral
            except ImportError as error:
                raise RuntimeError("mistralai is required to use the assistant LLM client.") from error

        return Mistral(api_key=api_key)

    def get_user_message(self, message: str) -> str:
        """Collected User-Prompt

        Args:
            message (str): Prompt von User

        Returns:
            str: Ausgabe von Mistral basierend auf User-Prompt
        """
        response = self.client.chat.complete(
            model=self.model,
            messages=[{"role": "user", "content": message}],
        )
        return response.choices[0].message.content

    def get_embedding(self, text: str) -> list[float]:
        """Retrieve Embedding aus Vector-DB

        Args:
            text (str): Input-Text, für den das Embedding abgerufen werden soll.

        Returns:
            list[float]: Das abgerufene Embedding
        """
        response = self.client.embeddings.create(model=self.embedding_model, inputs=[text])
        return response.data[0].embedding

    def load_data(self, file_path: str, course=None) -> None:
        """Delegiert das Laden der RAG-Daten an den RagClient."""
        self._get_rag_client().load_data(file_path, course=course)

    def perform_rag_query(self, query: str, course=None, learning_context: str = "") -> str:
        """Delegiert die RAG-Abfrage an den RagClient."""
        return self._get_rag_client().perform_rag_query(
            query,
            course=course,
            learning_context=learning_context,
        )

    def _get_rag_client(self):
        """Create the RAG client lazily to avoid circular service initialization."""
        if not hasattr(self, "rag_client"):
            from .rag_client import RagClient

            self.rag_client = RagClient(assistant=self)

        return self.rag_client
