# OpenBook: Interactive Online Textbooks - Server
# Copyright 2026 Sebastian Wolf, Daniel Sachada
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from __future__ import annotations

from uuid import UUID

from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from openbook.content.models import Course

from .llm_client import LLM_Client


class AssistantOrchestrator:
    """Coordinate course-aware assistant chat requests."""

    def __init__(self, llm_client: LLM_Client | None = None):
        self.llm_client = llm_client or LLM_Client()

    def answer(
        self,
        query: str,
        user: AbstractUser | AnonymousUser | None = None,
        course: Course | UUID | str | None = None,
    ) -> str:
        """Generate an assistant answer for a global or course-scoped query."""
        course_obj = self._resolve_course(course)
        self._check_chat_permission(user=user, course=course_obj)

        return self.llm_client.perform_rag_query(query, course=course_obj)

    def _resolve_course(self, course: Course | UUID | str | None) -> Course | None:
        """Return a Course instance for supported course identifiers."""
        if course is None or isinstance(course, Course):
            return course

        return get_object_or_404(Course, pk=course)

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
