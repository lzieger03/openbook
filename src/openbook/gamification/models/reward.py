# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
# Ledejna Salihi (@LedejnaSalihi)
# Lars Zieger (@lzieger03)

from django.db                import models
from django.utils.translation import gettext_lazy as _

from openbook.core.models.mixins.uuid import UUIDMixin


class Reward(UUIDMixin):
    """
    Define a reward that can be granted through the gamification system.
    """

    reward_type = models.CharField(
        verbose_name = _("Reward Type"),
        max_length   = 64,
        db_column    = "type",
        db_index     = True,
    )

    value = models.IntegerField(
        verbose_name = _("Value"),
    )

    description = models.TextField(
        verbose_name = _("Description"),
        blank        = True,
        default      = "",
    )

    class Meta:
        verbose_name        = _("Reward")
        verbose_name_plural = _("Rewards")
        ordering            = ["reward_type", "value"]

    def __str__(self):
        return f"{self.reward_type} ({self.value})"
