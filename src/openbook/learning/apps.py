from django.apps              import AppConfig
from django.utils.translation import gettext_lazy as _

class LearningApp(AppConfig):
    name         = "openbook.learning"
    label        = "openbook_learning"
    verbose_name = _("Learning State")

    def ready(self):
        from . import signals  # noqa: F401
