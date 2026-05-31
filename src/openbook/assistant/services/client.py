from django.conf import settings
from mistralai.client import Mistral
from dotenv import load_dotenv
import requests
import os

load_dotenv()


class MistralClient:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(MistralClient, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # api_key = getattr(settings, "MISTRAL_API_KEY", None)

        if not hasattr(self, "initialized"):
            api_key = os.environ["MISTRAL_API_KEY"]

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
