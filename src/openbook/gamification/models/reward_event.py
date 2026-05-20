# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>

from django.conf                import settings
from django.db                  import models
from django.utils.translation   import gettext_lazy as _

from openbook.core.models.mixins.uuid import UUIDMixin

from .reward import Reward


class RewardEvent(UUIDMixin):
    """
    Store reward-related account events.
    """

    account = models.ForeignKey(
        to           = settings.AUTH_USER_MODEL,
        verbose_name = _("Account"),
        on_delete    = models.CASCADE,
        related_name = "reward_events",
    )

    reward = models.ForeignKey(
        to           = Reward,
        verbose_name = _("Reward"),
        on_delete    = models.CASCADE,
        related_name = "events",
    )

    event_type = models.CharField(
        verbose_name = _("Event Type"),
        max_length   = 64,
        db_index     = True,
    )

    points_delta = models.IntegerField(
        verbose_name = _("Points Delta"),
    )

    created_at = models.DateTimeField(
        verbose_name = _("Created At"),
        auto_now_add = True,
        db_index     = True,
    )

    context = models.JSONField(
        verbose_name = _("Context"),
        db_column    = "context_json",
        blank        = True,
        default      = dict,
    )

    class Meta:
        verbose_name        = _("Reward Event")
        verbose_name_plural = _("Reward Events")
        ordering            = ["-created_at"]

    def __str__(self):
        return f"{self.account} {self.event_type} {self.points_delta:+d}"
