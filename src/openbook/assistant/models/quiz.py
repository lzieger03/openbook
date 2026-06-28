# OpenBook: Interactive Online Textbooks - Server
# Copyright 2026 Sebastian Wolf, Daniel Sachada
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from __future__ import annotations

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from openbook.core.models.mixins.uuid import UUIDMixin


class QuizAttempt(UUIDMixin):
    """
    A generated AI quiz scoped to a learner and course.

    The full quiz JSON keeps the correct answers server-side so the client can submit
    selected options and the backend can calculate the score before awarding points.
    """

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        verbose_name=_("User"),
        on_delete=models.CASCADE,
        related_name="quiz_attempts",
    )

    course = models.ForeignKey(
        to="openbook_content.Course",
        verbose_name=_("Course"),
        on_delete=models.CASCADE,
        related_name="quiz_attempts",
        null=True,
        blank=True,
    )

    textbook = models.ForeignKey(
        to="openbook_content.Textbook",
        verbose_name=_("Textbook"),
        on_delete=models.SET_NULL,
        related_name="quiz_attempts",
        null=True,
        blank=True,
    )

    page = models.ForeignKey(
        to="openbook_content.TextbookPage",
        verbose_name=_("Anchor Page"),
        on_delete=models.SET_NULL,
        related_name="quiz_attempts",
        null=True,
        blank=True,
    )

    quiz = models.JSONField(
        verbose_name=_("Quiz"),
        default=dict,
    )

    result = models.JSONField(
        verbose_name=_("Result"),
        blank=True,
        null=True,
    )

    correct_count = models.IntegerField(verbose_name=_("Correct Answers"), default=0)
    question_count = models.IntegerField(verbose_name=_("Question Count"), default=0)
    score = models.FloatField(verbose_name=_("Score"), default=0.0)

    created_at = models.DateTimeField(verbose_name=_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("Updated At"), auto_now=True, db_index=True)

    class Meta:
        db_table = "openbook_assistant_quiz_attempt"
        verbose_name = _("Quiz Attempt")
        verbose_name_plural = _("Quiz Attempts")
        ordering = ["-updated_at"]
        indexes = [
            models.Index(
                fields=["user", "course", "-updated_at"],
                name="openbook_as_user_id_60c823_idx",
            ),
        ]

    def __str__(self):
        return f"Quiz ({self.score:.0%})"
