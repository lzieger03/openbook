# OpenBook: Interactive Online Textbooks - Server
# Copyright 2026 Sebastian Wolf, Daniel Sachadä
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from __future__ import annotations

import json

from django.conf import settings
from django.core.files.base import ContentFile
from django.db import transaction
from django.utils.text import slugify

from openbook.assistant.models import AssistantDocument
from openbook.assistant.services.vector_index import delete_document_vectors
from openbook.content.models import Course
from openbook.content.models import Textbook
from openbook.content.models import TextbookPage


class TextbookDocumentSyncService:
    """Synchronize textbook content into downloadable and indexed documents."""

    def sync_textbook(self, textbook: Textbook) -> list[AssistantDocument]:
        """Rebuild course-scoped assistant documents for every course using a textbook."""
        courses = Course.objects.filter(materials__textbook=textbook).distinct()
        documents = []

        for course in courses:
            document = self.sync_textbook_for_course(textbook=textbook, course=course)
            if document is not None:
                documents.append(document)

        return documents

    def sync_textbook_for_course(
        self,
        textbook: Textbook,
        course: Course,
    ) -> AssistantDocument | None:
        """Rebuild one course-scoped assistant document for a textbook."""
        content = self.render_textbook(textbook)

        if not content.strip():
            self.delete_course_textbook_document(textbook=textbook, course=course)
            return None

        document, _created = AssistantDocument.objects.get_or_create(
            course=course,
            textbook=textbook,
            defaults={"title": textbook.name},
        )
        document.title = textbook.name
        document.course = course
        document.textbook = textbook
        document.save(update_fields=["title", "course", "textbook", "modified_at"])

        self._write_document_file(document=document, textbook=textbook, content=content)
        self._rebuild_index(document)
        return document

    def delete_course_textbook_document(
        self,
        textbook: Textbook,
        course: Course,
    ) -> None:
        """Delete the derived assistant document when a textbook leaves a course."""
        AssistantDocument.objects.filter(course=course, textbook=textbook).delete()

    def render_textbook(self, textbook: Textbook) -> str:
        """Render the current textbook pages as a stable Markdown export."""
        parts = [f"# {textbook.name}".strip()]

        for page in self._reading_order(textbook):
            page_source = self._extract_page_source(page)
            if page_source:
                parts.append(f"## {page.name}\n\n{page_source}".strip())

        if len(parts) == 1:
            return ""

        return "\n\n".join(parts).strip() + "\n"

    def clear_document_index(self, document: AssistantDocument) -> None:
        """Remove all chunks and vector rows for a document."""
        database_alias = document._state.db or "default"

        with transaction.atomic(using=database_alias):
            document.chunks.all().delete()
            delete_document_vectors(document.id, using=database_alias)

    def _write_document_file(
        self,
        document: AssistantDocument,
        textbook: Textbook,
        content: str,
    ) -> None:
        """Persist the generated textbook export as the document file."""
        if document.file_data:
            document.file_data.delete(save=False)

        filename = f"{slugify(textbook.slug or textbook.name) or textbook.id}.md"
        document.file_data.save(
            filename,
            ContentFile(content.encode("utf-8")),
            save=True,
        )

    def _rebuild_index(self, document: AssistantDocument) -> None:
        """Rebuild RAG chunks for the generated document when Mistral is configured."""
        self.clear_document_index(document)
        document.chunk_count = 0

        if not getattr(settings, "MISTRAL_API_KEY", ""):
            document.mark_index_failed("MISTRAL_API_KEY is not set.")
            document.save(
                update_fields=[
                    "index_status",
                    "index_error",
                    "chunk_count",
                    "indexed_at",
                    "modified_at",
                ]
            )
            return

        try:
            from openbook.assistant.services.llm_client import LLM_Client

            LLM_Client()._get_rag_client().index_document(document)
        except Exception as error:
            self.clear_document_index(document)
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

    def _reading_order(self, textbook: Textbook) -> list[TextbookPage]:
        """Flatten a textbook page tree roots-first in sibling position order."""
        pages = list(
            TextbookPage.objects.filter(textbook=textbook)
            .order_by("parent_id", "position", "name")
        )
        by_parent_id: dict[str | None, list[TextbookPage]] = {}

        for page in pages:
            parent_id = str(page.parent_id) if page.parent_id else None
            by_parent_id.setdefault(parent_id, []).append(page)

        for siblings in by_parent_id.values():
            siblings.sort(key=lambda page: (page.position, page.name))

        ordered: list[TextbookPage] = []

        def visit(parent_id: str | None) -> None:
            for page in by_parent_id.get(parent_id, []):
                ordered.append(page)
                visit(str(page.id))

        visit(None)

        if len(ordered) < len(pages):
            seen_page_ids = {page.id for page in ordered}
            ordered.extend(page for page in pages if page.id not in seen_page_ids)

        return ordered

    def _extract_page_source(self, page: TextbookPage) -> str:
        """Extract the current prompt/download source from a textbook page."""
        content = page.content

        if isinstance(content, dict):
            source = content.get("source")
            if isinstance(source, str):
                return source.strip()

        if isinstance(content, str):
            return content.strip()

        if content:
            return json.dumps(content, ensure_ascii=False, indent=2)

        return ""
