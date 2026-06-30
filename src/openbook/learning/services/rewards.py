# OpenBook: Interactive Online Textbooks - Server
# Copyright 2026 Sebastian Wolf, Daniel Sachadä
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from __future__ import annotations

import logging
from typing import Any

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AnonymousUser

from openbook.content.models import Course
from openbook.content.models import TextbookPage

logger = logging.getLogger(__name__)


class LearningRewardService:
    """Coordinate learning-triggered gamification rewards."""

    def award_chat_question_reward(
        self,
        user: AbstractUser | AnonymousUser | None,
        course: Course,
    ) -> dict[str, Any]:
        """Grant the daily-capped chat reward for asking a course question."""
        empty: dict[str, Any] = {"points_awarded": 0}

        if user is None or not getattr(user, "is_authenticated", False):
            return empty

        try:
            from openbook.gamification.services import award_chat_question_reward
        except ImportError:
            return empty

        try:
            return award_chat_question_reward(account_id=user.pk, course_id=course.pk)
        except Exception:
            logger.exception(
                "Failed to award chat reward for account=%s course=%s",
                user.pk,
                course.pk,
            )
            return empty

    def award_quiz_rewards(
        self,
        user: AbstractUser | AnonymousUser | None,
        course: Course,
        page: TextbookPage,
        score: float,
    ) -> dict[str, Any]:
        """Grant course points and skill progress for a quiz attempt on a page."""
        return self._award_scored_rewards(
            user=user,
            course=course,
            page=page,
            score=score,
            reward_function_name="award_quiz_rewards",
        )

    def award_exam_rewards(
        self,
        user: AbstractUser | AnonymousUser | None,
        course: Course,
        page: TextbookPage,
        score: float,
    ) -> dict[str, Any]:
        """Grant course points and skill progress for an exam attempt on a textbook."""
        return self._award_scored_rewards(
            user=user,
            course=course,
            page=page,
            score=score,
            reward_function_name="award_exam_rewards",
        )

    def _award_scored_rewards(
        self,
        user: AbstractUser | AnonymousUser | None,
        course: Course,
        page: TextbookPage,
        score: float,
        reward_function_name: str,
    ) -> dict[str, Any]:
        """Grant rewards whose value is derived from a normalized score."""
        empty: dict[str, Any] = {"points_awarded": 0, "skills_advanced": []}

        if user is None or not getattr(user, "is_authenticated", False):
            return empty

        try:
            from openbook.gamification.models import Skill
            from openbook.gamification import services as gamification_services
        except ImportError:
            return empty

        reward_function = getattr(gamification_services, reward_function_name)
        skills = list(
            Skill.objects
            .filter(textbook_pages__textbook_id=page.textbook_id)
            .distinct()
        )
        skill_ids = [skill.pk for skill in skills]
        skill_names = {str(skill.pk): skill.name for skill in skills}

        try:
            result = reward_function(
                account_id=user.pk,
                course_id=course.pk,
                page_id=page.pk,
                score=score,
                skill_ids=skill_ids,
            )
        except Exception:
            logger.exception(
                "Failed to award %s for account=%s course=%s page=%s",
                reward_function_name,
                user.pk,
                course.pk,
                page.pk,
            )
            return empty

        advanced = result.get("skills_advanced", []) or []
        return {
            "points_awarded": result.get("points_awarded", 0),
            "skills_advanced": [
                skill_names.get(str(skill_id), str(skill_id))
                for skill_id in advanced
            ],
        }
