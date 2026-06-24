# OpenBook: Interactive Online Textbooks - Server
# © 2026 Sebastian Wolf, Daniel Sachadä
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from django.core.files import File
from django.db import DatabaseError
from django.db import transaction
from sqlite_vec import serialize_float32

from openbook.assistant.models import AssistantDocument
from openbook.assistant.models import AssistantDocumentChunk
from openbook.assistant.services.prompt_builder import PromptBuilder
from openbook.assistant.services.vector_index import DOCUMENTS_TABLE
from openbook.assistant.services.vector_index import delete_document_vectors
from openbook.assistant.services.vector_index import get_vector_connection

if TYPE_CHECKING:
    from openbook.content.models import Course

    from .llm_client import LLM_Client


@dataclass(frozen=True)
class RagSource:
    """Describe one document chunk used as RAG context."""

    chunk_id: str
    document_id: str
    document_title: str
    position: int


@dataclass(frozen=True)
class RagQueryResult:
    """Bundle an assistant answer with the RAG sources used to produce it."""

    answer: str
    sources: tuple[RagSource, ...]


@dataclass(frozen=True)
class RagContext:
    """Document context retrieved from the assistant vector index."""

    context: str
    sources: tuple[RagSource, ...]


class RagClient:
    def __init__(
        self,
        assistant: "LLM_Client",
        prompt_builder: PromptBuilder | None = None,
    ):
        self.assistant = assistant
        self.prompt_builder = prompt_builder or PromptBuilder()
        self.text_data = None

    def load_data(
        self,
        file_path: str | Path,
        course: "Course | None" = None,
    ) -> AssistantDocument:
        """Create an assistant document from a local file and index it."""
        path = Path(file_path)
        document = AssistantDocument.objects.create(title=path.stem, course=course)

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

        try:
            if not document.file_data:
                raise RuntimeError("Assistant document has no uploaded file.")

            document.mark_indexing(embedding_model=self.assistant.embedding_model)
            document.save(
                update_fields=[
                    "index_status",
                    "index_error",
                    "embedding_model",
                    "chunk_count",
                    "modified_at",
                ]
            )
            self.clear_document_index(document, using=database_alias)

            document.file_data.open("rb")
            try:
                content = document.file_data.read().decode("utf-8", errors="replace")
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

            with transaction.atomic(using=database_alias):
                for indexed_chunk in indexed_chunks:
                    document_chunk = AssistantDocumentChunk.objects.using(database_alias).create(
                        parent=document,
                        position=indexed_chunk["position"],
                        content=indexed_chunk["content"],
                        embedding=indexed_chunk["embedding"],
                    )
                    self._insert_vector_index(document_chunk, using=database_alias)

                document.mark_indexed(chunk_count=len(indexed_chunks))
                document.save(
                    update_fields=[
                        "index_status",
                        "index_error",
                        "chunk_count",
                        "indexed_at",
                        "modified_at",
                    ]
                )

            self.text_data = content
        except Exception as error:
            document.mark_index_failed(error)
            document.save(
                update_fields=[
                    "index_status",
                    "index_error",
                    "chunk_count",
                    "indexed_at",
                    "modified_at",
                ]
            )
            raise

    def perform_rag_query(
        self,
        query: str,
        course: "Course | None" = None,
        learning_context: str = "",
    ) -> str:
        """Run a RAG query and return only the generated answer text."""
        return self.perform_rag_query_with_sources(
            query=query,
            course=course,
            learning_context=learning_context,
        ).answer

    def perform_rag_query_with_sources(
        self,
        query: str,
        course: "Course | None" = None,
        learning_context: str = "",
    ) -> RagQueryResult:
        """Run a RAG query and return the generated answer with used sources."""
        rag_context = self.retrieve_document_context(
            query=query,
            course=course,
            limit=3,
        )

        if not rag_context.context:
            return self._perform_unindexed_query(
                query,
                course=course,
                learning_context=learning_context,
            )

        prompt = self.prompt_builder.build_course_question_prompt(
            query=query,
            document_context=rag_context.context,
            learning_context=learning_context,
        )
        answer = self.assistant.get_user_message(prompt)
        return RagQueryResult(answer=answer, sources=rag_context.sources)

    def retrieve_document_context(
        self,
        query: str,
        course: "Course | None" = None,
        limit: int = 3,
    ) -> RagContext:
        """Retrieve matching document chunks without calling the chat model."""
        try:
            context_limit = int(limit)
        except (TypeError, ValueError) as error:
            raise ValueError("RAG context limit must be an integer.") from error

        if context_limit < 1:
            raise ValueError("RAG context limit must be at least 1.")

        connection = get_vector_connection()
        if connection is None:
            return RagContext(context="", sources=())

        chunk_queryset = AssistantDocumentChunk.objects.filter(
            parent__index_status=AssistantDocument.IndexStatusChoices.INDEXED,
        ).select_related("parent")
        indexed_chunk_count = chunk_queryset.count()

        if course is None:
            chunk_queryset = chunk_queryset.filter(parent__course__isnull=True)
        else:
            chunk_queryset = chunk_queryset.filter(parent__course=course)

        if not chunk_queryset.exists():
            return RagContext(context="", sources=())

        query_embedding = self.assistant.get_embedding(query)
        search_limit = self._vector_search_limit(
            indexed_chunk_count=indexed_chunk_count,
            context_limit=context_limit,
        )

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    f"""
                    SELECT
                        chunk_id,
                        distance
                    FROM {DOCUMENTS_TABLE}
                    WHERE embedding MATCH %s
                    ORDER BY distance
                    LIMIT {search_limit}
                    """,
                    [serialize_float32(query_embedding)],
                )
                rows = cursor.fetchall()
        except DatabaseError:
            return RagContext(context="", sources=())

        chunk_ids = [row[0] for row in rows]
        chunks_by_id = {
            str(chunk.id): chunk
            for chunk in chunk_queryset.filter(id__in=chunk_ids)
        }
        top_chunks = [
            chunks_by_id[chunk_id]
            for chunk_id in chunk_ids
            if chunk_id in chunks_by_id
        ][:context_limit]
        top_contexts = [chunk.content for chunk in top_chunks]

        if not top_contexts:
            return RagContext(context="", sources=())

        return RagContext(
            context="\n\n".join(top_contexts),
            sources=tuple(
                RagSource(
                    chunk_id=str(chunk.id),
                    document_id=str(chunk.parent_id),
                    document_title=chunk.parent.title,
                    position=chunk.position,
                )
                for chunk in top_chunks
            ),
        )

    def _perform_unindexed_query(
        self,
        query: str,
        course: "Course | None" = None,
        learning_context: str = "",
    ) -> RagQueryResult:
        """Answer without document context when no current chunks are available."""
        prompt_parts = ["Du bist ein hilfreicher Assistent."]

        if course is not None:
            prompt_parts.append(f"Der Nutzer arbeitet im Kurs \"{course.name}\".")

        if learning_context:
            prompt_parts.append("Beruecksichtige diesen Lernstand des Nutzers:")
            prompt_parts.append(learning_context)

        prompt_parts.append(f"Frage: {query}")
        prompt = "\n\n".join(prompt_parts).strip()

        return RagQueryResult(
            answer=self.assistant.get_user_message(prompt),
            sources=(),
        )

    def _vector_search_limit(self, indexed_chunk_count: int, context_limit: int) -> int:
        """Return enough vector candidates to filter the course scope afterwards."""
        return max(context_limit, indexed_chunk_count)

    def clear_document_index(
        self,
        document: AssistantDocument,
        using: str = "default",
    ) -> None:
        """Remove all persisted chunks and vector rows for one document."""
        with transaction.atomic(using=using):
            document.chunks.all().delete()
            delete_document_vectors(document.id, using=using)

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
                    course_id,
                    document_id,
                    chunk_id,
                    position
                )
                VALUES (%s, %s, %s, %s, %s)
                """,
                [
                    bytes(chunk.embedding),
                    str(chunk.parent.course_id or ""),
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
