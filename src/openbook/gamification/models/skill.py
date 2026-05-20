# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>

from django.conf                import settings
from django.core.validators     import MaxValueValidator
from django.core.validators     import MinValueValidator
from django.db                  import models
from django.utils.translation   import gettext_lazy as _

from openbook.core.models.mixins.uuid import UUIDMixin


class Skill(UUIDMixin):
    """
    Track a named skill and the user's progress in it.
    """

    account = models.ForeignKey(
        to           = settings.AUTH_USER_MODEL,
        verbose_name = _("Account"),
        on_delete    = models.CASCADE,
        related_name = "skills",
    )

    name = models.CharField(
        verbose_name = _("Name"),
        max_length   = 255,
    )

    level = models.PositiveIntegerField(
        verbose_name = _("Level"),
        default      = 0,
    )

    progress = models.DecimalField(
        verbose_name   = _("Progress"),
        max_digits     = 5,
        decimal_places = 2,
        default        = 0,
        validators     = [MinValueValidator(0), MaxValueValidator(100)],
    )

    class Meta:
        verbose_name        = _("Skill")
        verbose_name_plural = _("Skills")
        ordering            = ["account", "name"]
        constraints         = [
            models.UniqueConstraint(fields=["account", "name"], name="unique_skill_per_account"),
        ]

    def __str__(self):
        return f"{self.account} - {self.name}"
