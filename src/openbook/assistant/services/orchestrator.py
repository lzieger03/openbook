# OpenBook: Interactive Online Textbooks - Server
# Copyright 2026 Sebastian Wolf, Daniel Sachada
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from __future__ import annotations

from uuid import UUID

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from openbook.content.models import Course
from openbook.content.models import TextbookPage
from openbook.learning.models import LearningState
from openbook.learning.models import QuizResult

from .learning_context import LearningContextService
from .llm_client import LLM_Client


class AssistantOrchestrator:
    """Coordinate course-aware assistant chat requests."""

    def __init__(
        self,
        llm_client: LLM_Client | None = None,
        learning_context_service: LearningContextService | None = None,
    ):
        self.llm_client = llm_client or LLM_Client()
        self.learning_context_service = learning_context_service or LearningContextService()

    def answer(
        self,
        query: str,
        user: AbstractUser | AnonymousUser | None = None,
        course: Course | UUID | str | None = None,
    ) -> str:
        """Generate an assistant answer for a global or course-scoped query."""
        course_obj = self._resolve_course(course)
        self._check_chat_permission(user=user, course=course_obj)

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
    ) -> QuizResult:
        """Store the user's latest quiz result for a course page."""
        course_obj = self._resolve_required_course(course)
        page_obj = self._resolve_page(page)
        self._check_chat_permission(user=user, course=course_obj)
        return self.learning_context_service.record_quiz_result(
            user=user,
            course=course_obj,
            page=page_obj,
            score=score,
            attempts=attempts,
        )

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
