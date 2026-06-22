# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>

from django.conf                import settings
from django.db                  import models
from django.utils.translation   import gettext_lazy as _

from openbook.core.models.mixins.uuid import UUIDMixin


class AccountProgress(UUIDMixin):
    """
    Store the current point total and level for a user account.
    """

    account = models.OneToOneField(
        to           = settings.AUTH_USER_MODEL,
        verbose_name = _("Account"),
        on_delete    = models.CASCADE,
        related_name = "account_progress",
    )

    point_total = models.IntegerField(
        verbose_name = _("Point Total"),
        default      = 0,
    )

    level = models.PositiveIntegerField(
        verbose_name = _("Level"),
        default      = 1,
    )

    updated_at = models.DateTimeField(
        verbose_name = _("Updated At"),
        auto_now     = True,
        db_index     = True,
    )

    class Meta:
        verbose_name        = _("Account Progress")
        verbose_name_plural = _("Account Progress")
        ordering            = ["account"]

    def __str__(self):
        return f"{self.account} (Level {self.level}, {self.point_total} pts)"
