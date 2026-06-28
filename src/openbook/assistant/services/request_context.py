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


class AssistantRequestContextService:
    """Resolve request identifiers and enforce assistant access rules."""

    def resolve_course(self, course: Course | UUID | str | None) -> Course | None:
        """Return a Course instance for supported course identifiers."""
        if course is None or isinstance(course, Course):
            return course

        return get_object_or_404(Course, pk=course)

    def resolve_required_course(self, course: Course | UUID | str) -> Course:
        """Return a Course instance when a course-scoped action requires one."""
        course_obj = self.resolve_course(course)
        if course_obj is None:
            raise ValueError("Course is required.")
        return course_obj

    def resolve_page(self, page: TextbookPage | UUID | str) -> TextbookPage:
        """Return a TextbookPage instance for supported page identifiers."""
        if isinstance(page, TextbookPage):
            return page

        return get_object_or_404(TextbookPage, pk=page)

    def check_chat_permission(
        self,
        user: AbstractUser | AnonymousUser | None,
        course: Course | None,
    ) -> None:
        """Require authentication and course view permission for assistant use."""
        if user is None or not user.is_authenticated:
            raise PermissionDenied("You are not allowed to use the assistant.")

        if course is None:
            return

        if not user.has_perm("openbook_content.view_course", course):
            raise PermissionDenied("You are not allowed to use the assistant for this course.")
