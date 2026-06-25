# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from __future__ import annotations

from django.conf              import settings
from django.db                import models
from django.utils.translation import gettext_lazy as _

from openbook.core.models.mixins.uuid import UUIDMixin


class ExamAttempt(UUIDMixin):
    """
    A saved AI exam a learner generated and graded, scoped to a course. Keeps the full
    generated exam (questions incl. the server-side answers, in ``exam``) so it can be
    replayed, plus the latest grading ``result`` for review. Powers the exam history.
    """

    user = models.ForeignKey(
        to           = settings.AUTH_USER_MODEL,
        verbose_name = _("User"),
        on_delete    = models.CASCADE,
        related_name = "exam_attempts",
    )

    course = models.ForeignKey(
        to           = "openbook_content.Course",
        verbose_name = _("Course"),
        on_delete    = models.CASCADE,
        related_name = "exam_attempts",
        null         = True,
        blank        = True,
    )

    textbook = models.ForeignKey(
        to           = "openbook_content.Textbook",
        verbose_name = _("Textbook"),
        on_delete    = models.SET_NULL,
        related_name = "exam_attempts",
        null         = True,
        blank        = True,
    )

    title = models.CharField(
        verbose_name = _("Title"),
        max_length   = 160,
        blank        = True,
        default      = "Exam",
    )

    # Full generated exam (with server-side answers) so it can be replayed. Never sent
    # to the client verbatim — the API exposes a stripped question list instead.
    exam = models.JSONField(
        verbose_name = _("Exam"),
        default      = dict,
    )

    # Latest grading result shown when reviewing (questions, feedback, points, score).
    result = models.JSONField(
        verbose_name = _("Result"),
        blank        = True,
        null         = True,
    )

    total_points = models.IntegerField(verbose_name=_("Total Points"), default=0)
    max_points   = models.IntegerField(verbose_name=_("Max Points"),   default=0)
    score        = models.FloatField(verbose_name=_("Score"),          default=0.0)

    created_at = models.DateTimeField(verbose_name=_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("Updated At"), auto_now=True, db_index=True)

    class Meta:
        db_table            = "openbook_assistant_exam_attempt"
        verbose_name        = _("Exam Attempt")
        verbose_name_plural = _("Exam Attempts")
        ordering            = ["-updated_at"]
        indexes = [
            models.Index(fields=["user", "course", "-updated_at"]),
        ]

    def __str__(self):
        return f"{self.title} ({self.score:.0f}%)"
