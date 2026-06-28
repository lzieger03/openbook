# OpenBook: Interactive Online Textbooks - Server
# Copyright 2026 Sebastian Wolf, Daniel Sachada
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from __future__ import annotations

from typing import Any

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AnonymousUser

from openbook.content.models import Course
from openbook.content.models import TextbookPage
from openbook.learning.models import LearningState

from .context import LearningContextService
from .rewards import LearningRewardService


class LearningActivityService:
    """Handle learning events and their gamification side effects."""

    def __init__(
        self,
        context_service: LearningContextService | None = None,
        reward_service: LearningRewardService | None = None,
    ):
        self.context_service = context_service or LearningContextService()
        self.reward_service = reward_service or LearningRewardService()

    def record_chat_question(
        self,
        user: AbstractUser | AnonymousUser | None,
        course: Course,
    ) -> dict[str, Any]:
        """Record that a learner asked a course chat question."""
        return self.reward_service.award_chat_question_reward(user=user, course=course)

    def record_page_opened(
        self,
        user: AbstractUser,
        course: Course,
        page: TextbookPage,
    ) -> LearningState:
        """Store that a learner opened a course page."""
        return self.context_service.record_page_opened(
            user=user,
            course=course,
            page=page,
        )

    def mark_page_completed(
        self,
        user: AbstractUser,
        course: Course,
        page: TextbookPage,
    ) -> LearningState:
        """Store that a learner completed a course page."""
        return self.context_service.mark_page_completed(
            user=user,
            course=course,
            page=page,
        )

    def record_quiz_result(
        self,
        user: AbstractUser | AnonymousUser | None,
        course: Course,
        page: TextbookPage,
        score: float,
        attempts: int | None = None,
    ) -> dict[str, Any]:
        """Store a quiz result and return the awarded points and skills."""
        quiz_result = self.context_service.record_quiz_result(
            user=user,
            course=course,
            page=page,
            score=score,
            attempts=attempts,
        )
        reward = self.reward_service.award_quiz_rewards(
            user=user,
            course=course,
            page=page,
            score=score,
        )

        return {
            "quiz_result": quiz_result,
            "points_awarded": reward.get("points_awarded", 0),
            "skills_advanced": reward.get("skills_advanced", []),
        }

    def record_exam_result(
        self,
        user: AbstractUser | AnonymousUser | None,
        course: Course,
        page: TextbookPage,
        score: float,
    ) -> dict[str, Any]:
        """Record an exam score and return the awarded points and skills."""
        return self.reward_service.award_exam_rewards(
            user=user,
            course=course,
            page=page,
            score=score,
        )
