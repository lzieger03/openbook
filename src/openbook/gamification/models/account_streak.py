# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
# Ledejna Salihi (@LedejnaSalihi)
# Lars Zieger (@lzieger03)

from django.conf                import settings
from django.db                  import models
from django.utils.translation   import gettext_lazy as _

from openbook.core.models.mixins.uuid import UUIDMixin


class AccountStreak(UUIDMixin):
    """
    Daily learning streak for a user account. Tracks the current consecutive-day
    streak, the all-time record and the last day a learning activity was counted.
    """

    account = models.OneToOneField(
        to           = settings.AUTH_USER_MODEL,
        verbose_name = _("Account"),
        on_delete    = models.CASCADE,
        related_name = "account_streak",
    )

    current_streak = models.PositiveIntegerField(
        verbose_name = _("Current Streak"),
        default      = 0,
    )

    longest_streak = models.PositiveIntegerField(
        verbose_name = _("Longest Streak"),
        default      = 0,
    )

    last_active_date = models.DateField(
        verbose_name = _("Last Active Date"),
        null         = True,
        blank        = True,
    )

    last_active_at = models.DateTimeField(
        verbose_name = _("Last Active At"),
        null         = True,
        blank        = True,
    )

    streak_freezes = models.PositiveIntegerField(
        verbose_name = _("Streak Freezes"),
        default      = 0,
    )

    created_at = models.DateTimeField(
        verbose_name = _("Created At"),
        auto_now_add = True,
    )

    updated_at = models.DateTimeField(
        verbose_name = _("Updated At"),
        auto_now     = True,
        db_index     = True,
    )

    class Meta:
        db_table            = "openbook_gamification_account_streak"
        verbose_name        = _("Account Streak")
        verbose_name_plural = _("Account Streaks")
        ordering            = ["account"]

    def __str__(self):
        return f"{self.account} (streak {self.current_streak}, best {self.longest_streak})"
