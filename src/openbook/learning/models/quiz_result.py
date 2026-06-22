from __future__ import annotations

from django.conf import settings
from django.db   import models
from django.utils.translation import gettext_lazy as _

from openbook.core.models.mixins.uuid import UUIDMixin


class QuizResult(UUIDMixin):
    """Stores the latest quiz attempt for a user on a specific page."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("User"),
        on_delete=models.CASCADE,
        related_name="quiz_results",
    )

    page = models.ForeignKey(
        "openbook_content.TextbookPage",
        verbose_name=_("Page"),
        on_delete=models.CASCADE,
        related_name="quiz_results",
    )

    score = models.FloatField(
        verbose_name=_("Score"),
        help_text=_("Normalized score between 0.0 and 1.0."),
    )

    attempts = models.PositiveIntegerField(
        verbose_name=_("Attempts"),
        default=1,
    )

    answered_at = models.DateTimeField(
        verbose_name=_("Answered At"),
        auto_now=True,
    )

    class Meta:
        verbose_name        = _("Quiz Result")
        verbose_name_plural = _("Quiz Results")
        ordering            = ["-answered_at"]
        constraints         = [
            models.UniqueConstraint(
                fields=["user", "page"],
                name="openbook_learning_unique_user_page_quiz",
            )
        ]

    def __str__(self):
        return _("{user} on {page}: {score}").format(
            user=self.user,
            page=self.page,
            score=self.score,
        )
