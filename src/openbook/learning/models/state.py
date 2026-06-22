from __future__ import annotations

from django.conf import settings
from django.db   import models
from django.utils.translation import gettext_lazy as _

from openbook.core.models.mixins.uuid import UUIDMixin


class LearningState(UUIDMixin):
    """Tracks a user's current position and progress in a course."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("User"),
        on_delete=models.CASCADE,
        related_name="learning_states",
    )

    course = models.ForeignKey(
        "openbook_content.Course",
        verbose_name=_("Course"),
        on_delete=models.CASCADE,
        related_name="learning_states",
    )

    last_page = models.ForeignKey(
        "openbook_content.TextbookPage",
        verbose_name=_("Last Page"),
        on_delete=models.SET_NULL,
        related_name="learning_states",
        null=True,
        blank=True,
    )

    completed_pages = models.ManyToManyField(
        "openbook_content.TextbookPage",
        verbose_name=_("Completed Pages"),
        related_name="completed_in_states",
        blank=True,
    )

    last_accessed = models.DateTimeField(
        verbose_name=_("Last Accessed"),
        auto_now=True,
    )

    class Meta:
        verbose_name        = _("Learning State")
        verbose_name_plural = _("Learning States")
        ordering            = ["-last_accessed"]
        constraints         = [
            models.UniqueConstraint(
                fields=["user", "course"],
                name="openbook_learning_unique_user_course_state",
            )
        ]
