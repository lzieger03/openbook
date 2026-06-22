# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>

from django.apps              import AppConfig
from django.utils.translation import gettext_lazy as _


class GamificationApp(AppConfig):
    name         = "openbook.gamification"
    label        = "openbook_gamification"
    verbose_name = _("Gamification")

    def ready(self):
        """
        Load gamification signal handlers.
        """
        from . import signals  # noqa: F401
