# OpenBook: Interactive Online Textbooks - Server
# Copyright 2026 Sebastian Wolf, Daniel Sachada
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from __future__ import annotations

import logging

from typing import Any
from uuid import UUID

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from openbook.content.models import Course
from openbook.content.models import CourseMaterial
from openbook.content.models import Textbook
from openbook.content.models import TextbookPage
from openbook.learning.models import LearningState
from openbook.learning.models import QuizResult

from .learning_context import LearningContextService
from .llm_client import LLM_Client
from .prompt_builder import PromptBuilder
from .quiz_generation import GeneratedQuiz
from .quiz_generation import QuizResponseParser

logger = logging.getLogger(__name__)


class AssistantOrchestrator:
    """Coordinate course-aware assistant chat requests."""

    COURSE_CONTEXT_LIMIT = 12000

    def __init__(
        self,
        llm_client: LLM_Client | None = None,
        learning_context_service: LearningContextService | None = None,
        prompt_builder: PromptBuilder | None = None,
        quiz_response_parser: QuizResponseParser | None = None,
    ):
        self.llm_client = llm_client or LLM_Client()
        self.learning_context_service = learning_context_service or LearningContextService()
        self.prompt_builder = prompt_builder or PromptBuilder()
        self.quiz_response_parser = quiz_response_parser or QuizResponseParser()

    def answer(
        self,
        query: str,
        user: AbstractUser | AnonymousUser | None = None,
        course: Course | UUID | str | None = None,
    ) -> str:
        """Generate an assistant answer for a global or course-scoped query."""
        course_obj = self._resolve_course(course)
        self._check_chat_permission(user=user, course=course_obj)

        # Asking a question in a course chat earns a small (daily-capped) reward.
        if course_obj is not None:
            self._award_chat_question_reward(user=user, course=course_obj)

        learning_context = ""
        if course_obj is not None:
            learning_context = self.learning_context_service.get_prompt_context(
                user=user,
                course=course_obj,
            )

        try:
            return self.llm_client.perform_rag_query(
                query,
                course=course_obj,
                learning_context=learning_context,
            )
        except RuntimeError as error:
            if str(error) in {
                "No global assistant documents have been indexed yet.",
                "No assistant documents have been indexed for this course yet.",
            }:
                return self.llm_client.get_user_message(query)

            raise

    def record_page_opened(
        self,
        user: AbstractUser | AnonymousUser | None,
        course: Course | UUID | str,
        page: TextbookPage | UUID | str,
    ) -> LearningState:
        """Store that a user opened a course page."""
        course_obj = self._resolve_required_course(course)
        page_obj = self._resolve_page(page)
        self._check_chat_permission(user=user, course=course_obj)
        return self.learning_context_service.record_page_opened(
            user=user,
            course=course_obj,
            page=page_obj,
        )

    def mark_page_completed(
        self,
        user: AbstractUser | AnonymousUser | None,
        course: Course | UUID | str,
        page: TextbookPage | UUID | str,
    ) -> LearningState:
        """Store that a user completed a course page."""
        course_obj = self._resolve_required_course(course)
        page_obj = self._resolve_page(page)
        self._check_chat_permission(user=user, course=course_obj)
        return self.learning_context_service.mark_page_completed(
            user=user,
            course=course_obj,
            page=page_obj,
        )

    def record_quiz_result(
        self,
        user: AbstractUser | AnonymousUser | None,
        course: Course | UUID | str,
        page: TextbookPage | UUID | str,
        score: float,
        attempts: int | None = None,
    ) -> dict[str, Any]:
        """
        Store the user's latest quiz result for a course page and award points.

        Returns a summary of what was granted (``points_awarded`` and the names of the
        ``skills_advanced``) so the caller can show immediate feedback to the learner.
        """
        course_obj = self._resolve_required_course(course)
        page_obj = self._resolve_page(page)
        self._check_chat_permission(user=user, course=course_obj)
        quiz_result = self.learning_context_service.record_quiz_result(
            user=user,
            course=course_obj,
            page=page_obj,
            score=score,
            attempts=attempts,
        )

        # Reward correct answers: course points (and the page's skills) scale with the
        # score, and only an improvement over the best previous score is paid out.
        reward = self._award_quiz_rewards(
            user=user,
            course=course_obj,
            page=page_obj,
            score=score,
        )

        return {
            "quiz_result":     quiz_result,
            "points_awarded":  reward.get("points_awarded", 0),
            "skills_advanced": reward.get("skills_advanced", []),
        }

    def generate_quiz(
        self,
        user: AbstractUser | AnonymousUser | None,
        course: Course | UUID | str,
        question_count: int = 5,
        textbook: Textbook | UUID | str | None = None,
    ) -> GeneratedQuiz:
        """
        Generate a course quiz from RAG documents or course content fallback.

        When ``textbook`` is given, the quiz is narrowed to that textbook (the learner
        picked it) and the result is anchored to the textbook's first page so points
        and skills can be awarded for it.
        """
        course_obj = self._resolve_required_course(course)
        self._check_chat_permission(user=user, course=course_obj)

        material = self._resolve_course_material(course=course_obj, textbook=textbook)

        question_count = max(1, min(int(question_count), 10))
        learning_context = self.learning_context_service.get_prompt_context(
            user=user,
            course=course_obj,
        )
        rag_context = self.llm_client.retrieve_rag_context(
            query=self._build_quiz_query(
                course=course_obj,
                question_count=question_count,
                material=material,
            ),
            course=course_obj,
            limit=5,
        )

        course_context = ""
        context_source = "rag_documents"

        if not rag_context.context:
            context_source = "course_context"
            course_context = self._build_course_context(course_obj, material=material)

        prompt = self.prompt_builder.build_quiz_generation_prompt(
            document_context=rag_context.context,
            course_context=course_context,
            learning_context=learning_context,
            question_count=question_count,
        )
        response = self.llm_client.get_user_message(prompt)

        anchor_page = self._anchor_page_for_material(material)

        return GeneratedQuiz(
            questions=self.quiz_response_parser.parse(str(response or "")),
            context_source=context_source,
            sources=rag_context.sources,
            textbook_id=str(material.textbook_id) if material else None,
            page_id=str(anchor_page.id) if anchor_page else None,
        )

    def _resolve_course_material(
        self,
        course: Course,
        textbook: Textbook | UUID | str | None,
    ) -> CourseMaterial | None:
        """Return the course material for a chosen textbook, or None for whole-course quizzes."""
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

    def _anchor_page_for_material(self, material: CourseMaterial | None) -> TextbookPage | None:
        """Return the first reading-order page of a material to anchor the quiz result to."""
        if material is None or not material.textbook_id:
            return None

        pages = self._pages_for_material(material)
        return pages[0] if pages else None

    def _award_chat_question_reward(
        self,
        user: AbstractUser | AnonymousUser | None,
        course: Course,
    ) -> None:
        """Grant the (daily-capped) chat reward for asking a course question."""
        if user is None or not getattr(user, "is_authenticated", False):
            return

        # Keep gamification a soft dependency: never let a reward error break chat.
        try:
            from openbook.gamification.services import award_chat_question_reward
        except ImportError:
            return

        try:
            award_chat_question_reward(account_id=user.pk, course_id=course.pk)
        except Exception:
            pass

    def _award_quiz_rewards(
        self,
        user: AbstractUser | AnonymousUser | None,
        course: Course,
        page: TextbookPage,
        score: float,
    ) -> dict[str, Any]:
        """
        Grant course points and skill progress for a quiz attempt on a page.

        Returns ``{"points_awarded": int, "skills_advanced": [skill names]}``; an empty
        award when the learner is anonymous or nothing new could be earned.
        """
        empty: dict[str, Any] = {"points_awarded": 0, "skills_advanced": []}

        if user is None or not getattr(user, "is_authenticated", False):
            return empty

        try:
            from openbook.gamification.models import Skill
            from openbook.gamification.services import award_quiz_rewards
        except ImportError:
            return empty

        # The quiz covers a whole textbook, so advance every skill that any page of that
        # textbook trains (deduplicated). A textbook-less page falls back to its own skills.
        skills = list(
            Skill.objects
            .filter(textbook_pages__textbook_id=page.textbook_id)
            .distinct()
        )
        skill_ids   = [skill.pk for skill in skills]
        skill_names = {str(skill.pk): skill.name for skill in skills}

        try:
            result = award_quiz_rewards(
                account_id = user.pk,
                course_id  = course.pk,
                page_id    = page.pk,
                score      = score,
                skill_ids  = skill_ids,
            )
        except Exception:
            # Never let a reward failure break recording the quiz result, but make the
            # failure visible in the logs instead of swallowing it silently.
            logger.exception(
                "Failed to award quiz rewards for account=%s course=%s page=%s",
                user.pk, course.pk, page.pk,
            )
            return empty

        advanced = result.get("skills_advanced", []) or []
        return {
            "points_awarded":  result.get("points_awarded", 0),
            "skills_advanced": [skill_names.get(str(skill_id), str(skill_id)) for skill_id in advanced],
        }

    def _resolve_course(self, course: Course | UUID | str | None) -> Course | None:
        """Return a Course instance for supported course identifiers."""
        if course is None or isinstance(course, Course):
            return course

        return get_object_or_404(Course, pk=course)

    def _resolve_required_course(self, course: Course | UUID | str) -> Course:
        """Return a Course instance for learning-state mutations."""
        course_obj = self._resolve_course(course)
        if course_obj is None:
            raise ValueError("Course is required.")
        return course_obj

    def _resolve_page(self, page: TextbookPage | UUID | str) -> TextbookPage:
        """Return a TextbookPage instance for supported page identifiers."""
        if isinstance(page, TextbookPage):
            return page

        return get_object_or_404(TextbookPage, pk=page)

    def _check_chat_permission(
        self,
        user: AbstractUser | AnonymousUser | None,
        course: Course | None,
    ) -> None:
        """Require authentication and course view permission for course chat."""
        if user is None or not user.is_authenticated:
            raise PermissionDenied("You are not allowed to use the assistant.")

        if course is None:
            return

        if not user.has_perm("openbook_content.view_course", course):
            raise PermissionDenied("You are not allowed to use the assistant for this course.")

    def _build_quiz_query(
        self,
        course: Course,
        question_count: int,
        material: CourseMaterial | None = None,
    ) -> str:
        """Build the retrieval query used to find relevant quiz source documents."""
        if material is not None and material.textbook_id:
            return (
                f"Erzeuge {question_count} Multiple-Choice-Quizfragen zum Lehrbuch "
                f'"{material.textbook.name}" aus dem Kurs "{course.name}".'
            )

        return (
            f"Erzeuge {question_count} Multiple-Choice-Quizfragen fuer den Kurs "
            f'"{course.name}".'
        )

    def _build_course_context(self, course: Course, material: CourseMaterial | None = None) -> str:
        """
        Build fallback context from course metadata, skills and authored content.

        When ``material`` is given, only that textbook's content is included so the quiz
        stays focused on the textbook the learner selected.
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

        for material in materials:
            if not material.textbook_id:
                continue

            parts.append(f"Material: {material.textbook.name}")

            for page in self._pages_for_material(material):
                page_text = self._extract_page_text(page)
                if page_text:
                    parts.append(f"Seite: {page.name}\n{page_text}")

        return self._truncate_context("\n\n".join(parts))

    def _format_skill(self, skill: Any) -> str:
        """Return one skill line for the fallback course context."""
        description = getattr(skill, "description", "")
        if isinstance(description, str) and description.strip():
            return f"- {skill.name}: {description.strip()}"
        return f"- {skill.name}"

    def _pages_for_material(self, material: CourseMaterial) -> list[TextbookPage]:
        """Return pages selected by a course material, in reading order."""
        pages = list(
            TextbookPage.objects.filter(textbook=material.textbook)
            .order_by("parent_id", "position", "name")
        )
        ordered_pages = self._reading_order(pages)
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

    def _reading_order(self, pages: list[TextbookPage]) -> list[TextbookPage]:
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

    def _extract_page_text(self, page: TextbookPage) -> str:
        """Extract prompt-readable text from a textbook page."""
        parts = []

        if page.description.strip():
            parts.append(page.description.strip())

        content_text = self._extract_content_text(page.content)
        if content_text:
            parts.append(content_text)

        return "\n".join(parts).strip()

    def _extract_content_text(self, value: Any) -> str:
        """Extract text from the authored page content JSON tree."""
        if isinstance(value, str):
            return value.strip()

        if isinstance(value, list):
            return "\n".join(
                text
                for item in value
                if (text := self._extract_content_text(item))
            )

        if isinstance(value, dict):
            source = value.get("source")
            if isinstance(source, str):
                return source.strip()

            preferred_keys = ("text", "content", "children", "items", "value")
            preferred_text = [
                self._extract_content_text(value[key])
                for key in preferred_keys
                if key in value
            ]
            if preferred_text:
                return "\n".join(text for text in preferred_text if text)

            return "\n".join(
                text
                for item in value.values()
                if (text := self._extract_content_text(item))
            )

        return ""

    def _truncate_context(self, context: str) -> str:
        """Limit fallback context size before sending it to the LLM."""
        if len(context) <= self.COURSE_CONTEXT_LIMIT:
            return context

        return context[: self.COURSE_CONTEXT_LIMIT].rsplit("\n", 1)[0].strip()
