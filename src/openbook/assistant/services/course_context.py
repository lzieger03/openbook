# OpenBook: Interactive Online Textbooks - Server
# Copyright 2026 Sebastian Wolf, Daniel Sachada
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from __future__ import annotations

from typing import Any
from uuid import UUID

from openbook.content.models import Course
from openbook.content.models import CourseMaterial
from openbook.content.models import Textbook
from openbook.content.models import TextbookPage


class CourseContentContextService:
    """Build prompt-ready context from course and textbook content."""

    CONTEXT_LIMIT = 12000

    def resolve_course_material(
        self,
        course: Course,
        textbook: Textbook | UUID | str | None,
    ) -> CourseMaterial | None:
        """Return the course material for a chosen textbook, or None for whole-course work."""
        if textbook is None:
            return None

        textbook_id = textbook.pk if isinstance(textbook, Textbook) else textbook
        material = (
            CourseMaterial.objects
            .select_related("textbook")
            .filter(course=course, textbook_id=textbook_id)
            .first()
        )

        if material is None:
            raise ValueError("The selected textbook is not part of this course.")

        return material

    def anchor_page_for_material(self, material: CourseMaterial | None) -> TextbookPage | None:
        """Return the first reading-order page of a material."""
        if material is None or not material.textbook_id:
            return None

        pages = self.pages_for_material(material)
        return pages[0] if pages else None

    def build_course_context(
        self,
        course: Course,
        material: CourseMaterial | None = None,
    ) -> str:
        """
        Build fallback context from course metadata, skills and authored content.

        When ``material`` is given, only that textbook's content is included so generated
        activities stay focused on the textbook the learner selected.
        """
        parts = [f"Kurs: {course.name}"]

        if course.description.strip():
            parts.append(f"Kursbeschreibung:\n{course.description.strip()}")

        skills = list(course.skills.order_by("name"))
        if skills:
            parts.append(
                "Kompetenzen:\n"
                + "\n".join(
                    self._format_skill(skill)
                    for skill in skills
                )
            )

        if material is not None:
            materials = [material] if material.textbook_id else []
        else:
            materials = (
                course.materials.select_related("textbook")
                .prefetch_related("page_ranges")
                .order_by("position")
            )

        for course_material in materials:
            if not course_material.textbook_id:
                continue

            parts.append(f"Material: {course_material.textbook.name}")

            for page in self.pages_for_material(course_material):
                page_text = self.extract_page_text(page)
                if page_text:
                    parts.append(f"Seite: {page.name}\n{page_text}")

        return self.truncate_context("\n\n".join(parts))

    def build_textbook_pages_context(self, material: CourseMaterial) -> str:
        """Build exam context from only the selected textbook's pages."""
        parts = [f"Lehrbuch: {material.textbook.name}"]

        for page in self.pages_for_material(material):
            page_text = self.extract_page_text(page)
            if page_text:
                parts.append(f"Seite: {page.name}\n{page_text}")

        return self.truncate_context("\n\n".join(parts))

    def pages_for_material(self, material: CourseMaterial) -> list[TextbookPage]:
        """Return pages selected by a course material, in reading order."""
        pages = list(
            TextbookPage.objects.filter(textbook=material.textbook)
            .order_by("parent_id", "position", "name")
        )
        ordered_pages = self.reading_order(pages)
        page_ranges = list(
            material.page_ranges.select_related("start_page", "end_page")
            .order_by("position", "id")
        )

        if not page_ranges:
            return ordered_pages

        index_by_id = {page.id: index for index, page in enumerate(ordered_pages)}
        selected_pages = []
        seen_page_ids = set()

        for page_range in page_ranges:
            start_index = index_by_id.get(page_range.start_page_id)
            end_index = index_by_id.get(page_range.end_page_id)

            if start_index is None or end_index is None:
                continue

            first_index = min(start_index, end_index)
            last_index = max(start_index, end_index)

            for page in ordered_pages[first_index:last_index + 1]:
                if page.id not in seen_page_ids:
                    selected_pages.append(page)
                    seen_page_ids.add(page.id)

        return selected_pages

    def reading_order(self, pages: list[TextbookPage]) -> list[TextbookPage]:
        """Flatten a textbook page tree roots-first in sibling position order."""
        by_parent_id = {}

        for page in pages:
            by_parent_id.setdefault(page.parent_id, []).append(page)

        for siblings in by_parent_id.values():
            siblings.sort(key=lambda page: (page.position, page.name))

        ordered = []

        def visit(parent_id):
            for page in by_parent_id.get(parent_id, []):
                ordered.append(page)
                visit(page.id)

        visit(None)

        if len(ordered) < len(pages):
            seen_page_ids = {page.id for page in ordered}
            ordered.extend(page for page in pages if page.id not in seen_page_ids)

        return ordered

    def extract_page_text(self, page: TextbookPage) -> str:
        """Extract prompt-readable text from a textbook page."""
        parts = []

        if page.description.strip():
            parts.append(page.description.strip())

        content_text = self.extract_content_text(page.content)
        if content_text:
            parts.append(content_text)

        return "\n".join(parts).strip()

    def extract_content_text(self, value: Any) -> str:
        """Extract text from the authored page content JSON tree."""
        if isinstance(value, str):
            return value.strip()

        if isinstance(value, list):
            return "\n".join(
                text
                for item in value
                if (text := self.extract_content_text(item))
            )

        if isinstance(value, dict):
            source = value.get("source")
            if isinstance(source, str):
                return source.strip()

            preferred_keys = ("text", "content", "children", "items", "value")
            preferred_text = [
                self.extract_content_text(value[key])
                for key in preferred_keys
                if key in value
            ]
            if preferred_text:
                return "\n".join(text for text in preferred_text if text)

            return "\n".join(
                text
                for item in value.values()
                if (text := self.extract_content_text(item))
            )

        return ""

    def truncate_context(self, context: str) -> str:
        """Limit fallback context size before sending it to the LLM."""
        if len(context) <= self.CONTEXT_LIMIT:
            return context

        return context[: self.CONTEXT_LIMIT].rsplit("\n", 1)[0].strip()

    def _format_skill(self, skill: Any) -> str:
        """Return one skill line for the fallback course context."""
        description = getattr(skill, "description", "")
        if isinstance(description, str) and description.strip():
            return f"- {skill.name}: {description.strip()}"
        return f"- {skill.name}"
