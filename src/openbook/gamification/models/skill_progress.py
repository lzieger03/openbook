# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>

from django.conf import settings
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from openbook.core.models.mixins.uuid import UUIDMixin


class SkillProgress(UUIDMixin):
    """
    Store the current progress and level of an account for one global skill.
    """

    skill = models.ForeignKey(
        to="openbook_gamification.Skill",
        verbose_name=_("Skill"),
        on_delete=models.CASCADE,
        related_name="skill_progresses",
    )

    account = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        verbose_name=_("Account"),
        on_delete=models.CASCADE,
        related_name="skill_progresses",
    )

    level = models.PositiveIntegerField(
        verbose_name=_("Level"),
        default=1,
    )

    progress = models.DecimalField(
        verbose_name=_("Progress"),
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )

    class Meta:
        db_table = "openbook_gamification_skill_progress"
        verbose_name = _("Skill Progress")
        verbose_name_plural = _("Skill Progresses")
        ordering = ["account", "skill"]
        constraints = [
            models.UniqueConstraint(
                fields=["account", "skill"],
                name="unique_skill_progress_per_account_and_skill",
            ),
        ]

    def __str__(self):
        return f"{self.account} - {self.skill} (level {self.level}, {self.progress}%)"
