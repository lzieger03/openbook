# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>

from django.db import models
from django.utils.translation import gettext_lazy as _

from openbook.core.models.mixins.uuid import UUIDMixin


class Skill(UUIDMixin):
    """
    Global skill catalog entry.
    """

    name = models.CharField(
        verbose_name=_("Name"),
        max_length=255,
    )

    description = models.TextField(
        verbose_name=_("Description"),
        blank=True,
        default="",
    )

    icon_path = models.CharField(
        verbose_name=_("Icon Path"),
        max_length=255,
        blank=True,
        default="",
    )

    class Meta:
        verbose_name = _("Skill")
        verbose_name_plural = _("Skills")
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(fields=["name"], name="unique_skill_name"),
        ]

    def __str__(self):
        return self.name
