# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>

from django.conf import settings
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from openbook.core.models.mixins.uuid import UUIDMixin


class CourseProgress(UUIDMixin):
    """
    Store the current point total, level and progress for a user inside a course.
    """

    account = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        verbose_name=_("Account"),
        on_delete=models.CASCADE,
        related_name="course_progresses",
    )

    course = models.ForeignKey(
        to="openbook_content.Course",
        verbose_name=_("Course"),
        on_delete=models.CASCADE,
        related_name="course_progresses",
    )

    course_points = models.IntegerField(
        verbose_name=_("Course Points"),
        default=0,
    )

    course_level = models.PositiveIntegerField(
        verbose_name=_("Course Level"),
        default=1,
    )

    course_progress = models.DecimalField(
        verbose_name=_("Course Progress"),
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )

    class Meta:
        db_table = "openbook_gamification_course_progress"
        verbose_name = _("Course Progress")
        verbose_name_plural = _("Course Progresses")
        ordering = ["account", "course"]
        constraints = [
            models.UniqueConstraint(
                fields=["account", "course"],
                name="unique_course_progress_per_account_and_course",
            ),
        ]

    def __str__(self):
        return f"{self.account} - {self.course} (level {self.course_level}, {self.course_points} pts, {self.course_progress}%)"