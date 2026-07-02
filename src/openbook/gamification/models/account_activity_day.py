# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
# Ledejna Salihi (@LedejnaSalihi)
# Lars Zieger (@lzieger03)

from django.conf                import settings
from django.db                  import models
from django.utils.translation   import gettext_lazy as _

from openbook.core.models.mixins.uuid import UUIDMixin


class AccountActivityDay(UUIDMixin):
    """
    Aggregated learning activity for a single calendar day (Europe/Berlin) per
    account. The unique constraint on (account, activity_date) guarantees exactly
    one row per account and day, which makes streak counting idempotent.
    """

    account = models.ForeignKey(
        to           = settings.AUTH_USER_MODEL,
        verbose_name = _("Account"),
        on_delete    = models.CASCADE,
        related_name = "activity_days",
    )

    activity_date = models.DateField(
        verbose_name = _("Activity Date"),
        db_index     = True,
    )

    activity_count = models.PositiveIntegerField(
        verbose_name = _("Activity Count"),
        default      = 1,
    )

    first_activity_at = models.DateTimeField(
        verbose_name = _("First Activity At"),
    )

    last_activity_at = models.DateTimeField(
        verbose_name = _("Last Activity At"),
    )

    created_at = models.DateTimeField(
        verbose_name = _("Created At"),
        auto_now_add = True,
    )

    updated_at = models.DateTimeField(
        verbose_name = _("Updated At"),
        auto_now     = True,
    )

    class Meta:
        db_table            = "openbook_gamification_account_activity_day"
        verbose_name        = _("Account Activity Day")
        verbose_name_plural = _("Account Activity Days")
        ordering            = ["-activity_date"]
        constraints = [
            models.UniqueConstraint(
                fields = ["account", "activity_date"],
                name   = "unique_account_activity_day",
            ),
        ]

    def __str__(self):
        return f"{self.account} {self.activity_date} ({self.activity_count}x)"
