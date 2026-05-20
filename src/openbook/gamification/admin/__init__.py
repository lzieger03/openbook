# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>

from .account_points import AccountPointsAdmin
from .reward import RewardAdmin
from .reward_event import RewardEventAdmin
from .skill import SkillAdmin

from .. import models
from openbook.admin import admin_site

admin_site.register(models.AccountPoints, AccountPointsAdmin)
admin_site.register(models.Reward,        RewardAdmin)
admin_site.register(models.RewardEvent,   RewardEventAdmin)
admin_site.register(models.Skill,         SkillAdmin)
