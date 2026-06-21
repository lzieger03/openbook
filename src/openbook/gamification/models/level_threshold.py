# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>

from decimal                  import Decimal

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

    @classmethod
    def progress_to_next_level(cls, points):
        """
        Return the progress (0–100) from the current level's threshold towards the
        next one. Resets to 0 on each level-up and is full (100) once the highest
        configured level has been reached. This is the value rendered as a progress
        bar both for an account and for a single course.
        """
        level = cls.level_for_points(points)

        current_threshold = (
            cls.objects
            .filter(level__lte=level)
            .order_by("-level")
            .first()
        )
        next_threshold = (
            cls.objects
            .filter(level__gt=level)
            .order_by("level")
            .first()
        )

        # No higher level defined (max level reached) => the bar is full.
        if next_threshold is None:
            return Decimal("100.00")

        current_min = current_threshold.min_points if current_threshold else 0
        span        = next_threshold.min_points - current_min

        if span <= 0:
            return Decimal("0.00")

        percent = (Decimal(points - current_min) / Decimal(span)) * 100
        percent = max(Decimal(0), min(Decimal(100), percent))

        return percent.quantize(Decimal("0.01"))
