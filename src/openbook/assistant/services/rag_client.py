# OpenBook: Interactive Online Textbooks - Server
# © 2026 Sebastian Wolf, Daniel Sachadä
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from pathlib import Path
from typing import TYPE_CHECKING

from django.core.files import File
from sqlite_vec import serialize_float32

from openbook.assistant.models import AssistantDocument
from openbook.assistant.models import AssistantDocumentChunk
from openbook.assistant.services.vector_index import DOCUMENTS_TABLE
from openbook.assistant.services.vector_index import delete_document_vectors
from openbook.assistant.services.vector_index import get_vector_connection

from .llm_client import SNOW_FILE_PATH

if TYPE_CHECKING:
    from .llm_client import LLM_Client


class RagClient:
    def __init__(self, assistant: "LLM_Client"):
        self.assistant = assistant
        self.text_data = None

    def load_data(self, file_path: str | Path = SNOW_FILE_PATH) -> AssistantDocument:
        """Create an assistant document from a local file and index it."""
        path = Path(file_path)
        document = AssistantDocument.objects.create(title=path.stem)

        try:
            with path.open("rb") as file:
                document.file_data.save(path.name, File(file), save=True)

            self.index_document(document)
            return document
        except Exception:
            if document.file_data:
                document.file_data.delete(save=False)
            document.delete()
            raise

    def index_document(self, document: AssistantDocument) -> None:
        """Read an uploaded assistant document and rebuild its retrieval index."""
        database_alias = document._state.db or "default"
        get_vector_connection(database_alias)

        document.file_data.open("rb")
        try:
            content = document.file_data.read().decode("utf-8")
        finally:
            document.file_data.close()

        chunks = self._chunk_text(content)
        indexed_chunks = []

        for position, chunk in enumerate(chunks):
            indexed_chunks.append(
                {
                    "position": position,
                    "content": chunk,
                    "embedding": serialize_float32(self.assistant.get_embedding(chunk)),
                }
            )

        document.chunks.all().delete()
        delete_document_vectors(document.id, using=database_alias)

        for indexed_chunk in indexed_chunks:
            document_chunk = AssistantDocumentChunk.objects.using(database_alias).create(
                parent=document,
                position=indexed_chunk["position"],
                content=indexed_chunk["content"],
                embedding=indexed_chunk["embedding"],
            )
            self._insert_vector_index(document_chunk, using=database_alias)

        self.text_data = content

    def perform_rag_query(self, query: str) -> str:
        """Run a RAG query through sqlite-vec on Django's database connection."""
        connection = get_vector_connection()
        if connection is None:
            raise RuntimeError("RAG vector search currently requires Django's SQLite backend.")

        if not AssistantDocumentChunk.objects.exists():
            self.load_data()

        query_embedding = self.assistant.get_embedding(query)

        with connection.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT
                    chunk_id,
                    distance
                FROM {DOCUMENTS_TABLE}
                WHERE embedding MATCH %s
                ORDER BY distance
                LIMIT 3
                """,
                [serialize_float32(query_embedding)],
            )
            rows = cursor.fetchall()

        chunk_ids = [row[0] for row in rows]
        chunks_by_id = {
            str(chunk.id): chunk
            for chunk in AssistantDocumentChunk.objects.filter(id__in=chunk_ids)
        }
        top_contexts = [
            chunks_by_id[chunk_id].content
            for chunk_id in chunk_ids
            if chunk_id in chunks_by_id
        ]
        context = "\n\n".join(top_contexts)

        prompt = f"""
            Du bist ein hilfreicher Assistent.
            Beantworte die folgende Frage basierend auf diesem Kontext:
            \n\n{context}\n\nFrage: {query}
        """.strip()
        return self.assistant.get_user_message(prompt)

    def _insert_vector_index(
        self,
        chunk: AssistantDocumentChunk,
        using: str = "default",
    ) -> None:
        """Insert one Django chunk into the sqlite-vec search index."""
        connection = get_vector_connection(using)
        if connection is None:
            return

        with connection.cursor() as cursor:
            cursor.execute(
                f"""
                INSERT INTO {DOCUMENTS_TABLE} (
                    embedding,
                    document_id,
                    chunk_id,
                    position
                )
                VALUES (%s, %s, %s, %s)
                """,
                [
                    bytes(chunk.embedding),
                    str(chunk.parent_id),
                    str(chunk.id),
                    chunk.position,
                ],
            )

    def _chunk_text(
        self,
        text: str,
        chunk_size: int = 1000,
        overlap: int = 200,
    ) -> list[str]:
        """Split text into overlapping chunks."""
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunks.append(text[start:end])
            start += chunk_size - overlap
        return chunks
