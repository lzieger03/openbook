from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class AiApp(AppConfig):
    name = 'openbook.ai'
    label = 'openbook_ai'
    verbose_name = _("AI")