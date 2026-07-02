from __future__ import annotations

from django.conf import settings
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.db   import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from openbook.core.models.mixins.uuid import UUIDMixin


class QuizResult(UUIDMixin):
    """Stores the latest scored learning activity for a user."""

    class ActivityTypeChoices(models.TextChoices):
        QUIZ       = "quiz", _("Quiz")
        EXAM       = "exam", _("Exam")
        HANGMAN    = "hangman", _("Hangman")
        MEMORY     = "memory", _("Memory")
        FLASHCARDS = "flashcards", _("Flashcards")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("User"),
        on_delete=models.CASCADE,
        related_name="quiz_results",
    )

    course = models.ForeignKey(
        "openbook_content.Course",
        verbose_name=_("Course"),
        on_delete=models.CASCADE,
        related_name="quiz_results",
        null=True,
        blank=True,
    )

    textbook = models.ForeignKey(
        "openbook_content.Textbook",
        verbose_name=_("Textbook"),
        on_delete=models.SET_NULL,
        related_name="quiz_results",
        null=True,
        blank=True,
    )

    page = models.ForeignKey(
        "openbook_content.TextbookPage",
        verbose_name=_("Page"),
        on_delete=models.SET_NULL,
        related_name="quiz_results",
        null=True,
        blank=True,
    )

    activity_type = models.CharField(
        verbose_name=_("Activity Type"),
        max_length=32,
        choices=ActivityTypeChoices.choices,
        default=ActivityTypeChoices.QUIZ,
        db_index=True,
    )

    score = models.FloatField(
        verbose_name=_("Score"),
        help_text=_("Normalized score between 0.0 and 1.0."),
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(1.0),
        ],
    )

    attempts = models.PositiveIntegerField(
        verbose_name=_("Attempts"),
        default=1,
    )

    metadata = models.JSONField(
        verbose_name=_("Metadata"),
        blank=True,
        default=dict,
    )

    answered_at = models.DateTimeField(
        verbose_name=_("Answered At"),
        auto_now=True,
    )

    class Meta:
        verbose_name        = _("Quiz Result")
        verbose_name_plural = _("Quiz Results")
        ordering            = ["-answered_at"]
        indexes             = [
            models.Index(
                fields=["user", "course", "activity_type"],
                name="obl_qr_user_course_act_idx",
            ),
            models.Index(
                fields=["user", "page", "activity_type"],
                name="obl_qr_user_page_act_idx",
            ),
        ]
        constraints         = [
            models.UniqueConstraint(
                fields=["user", "page", "activity_type"],
                condition=Q(page__isnull=False),
                name="openbook_learning_unique_user_page_activity",
            ),
        ]

    def __str__(self):
        target = self.page or self.textbook or self.course or _("Learning activity")
        return _("{user} {activity} on {target}: {score}").format(
            user=self.user,
            activity=self.get_activity_type_display(),
            target=target,
            score=self.score,
        )
