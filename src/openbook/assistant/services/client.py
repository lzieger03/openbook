# OpenBook: Interactive Online Textbooks - Server
# © 2026 Sebastian Wolf, Daniel Sachadä
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.conf import settings
from mistralai.client import Mistral
import requests


class MistralClient:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(MistralClient, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "initialized"):
            api_key = settings.MISTRAL_API_KEY

            if not api_key:
                raise ValueError("MISTRAL_API_KEY is not set in settings")

            self.client = Mistral(api_key=api_key)
            self.model = "mistral-small-latest"
            self.text_data = None

            self.initialized = True

    def chat_complete(self, message: str) -> str:
        response = self.client.chat.complete(
            model=self.model,
            messages=[{"role": "user", "content": message}],
        )
        return response

    def _load_data(self):
        """Downloads the data and sets up the initial index"""
        response = requests.get(
            "https://raw.githubusercontent.com/run-llama/llama_index/main/docs/docs/examples/data/paul_graham/paul_graham_essay.txt"
        )
        self.text_data = response.text
        # TODO: Add logic to chunk text, create embeddings, and add to self.index

    def perform_rag_query(self, query: str):
        """Example method to be called from other files"""
        if not self.text_data:
            raise ValueError("Data not loaded yet.")
        # TODO: Implement embedding the query, searching the FAISS index, and calling Mistral
        return f"Results for: {query}"


mistral_client = MistralClient()
