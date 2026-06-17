# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>

from django.db                import models
from django.utils.translation import gettext_lazy as _

from openbook.core.models.mixins.uuid import UUIDMixin


class LevelThreshold(UUIDMixin):
    """
    Define how many points are required to reach a given level. The level of an
    account is the highest level whose required point total has been reached.
    """

    level = models.PositiveIntegerField(
        verbose_name = _("Level"),
        unique       = True,
    )

    min_points = models.IntegerField(
        verbose_name = _("Required Points"),
        db_index     = True,
    )

    class Meta:
        verbose_name        = _("Level Threshold")
        verbose_name_plural = _("Level Thresholds")
        ordering            = ["min_points", "level"]

    def __str__(self):
        return f"Level {self.level} (≥ {self.min_points} pts)"

    @classmethod
    def level_for_points(cls, points):
        """
        Return the level that corresponds to the given point total. Falls back to
        level 1 (the starting level) when no threshold has been reached.
        """
        threshold = (
            cls.objects
            .filter(min_points__lte=points)
            .order_by("-min_points", "-level")
            .first()
        )

        return threshold.level if threshold else 1
