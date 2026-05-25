# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>

from .account_activity_day import AccountActivityDayAdmin
from .account_progress import AccountProgressAdmin
from .account_streak import AccountStreakAdmin
from .level_threshold import LevelThresholdAdmin
from .reward import RewardAdmin
from .reward_event_log import RewardEventLogAdmin
from .skill import SkillAdmin

from .. import models
from openbook.admin import admin_site

admin_site.register(models.AccountActivityDay, AccountActivityDayAdmin)
admin_site.register(models.AccountProgress, AccountProgressAdmin)
admin_site.register(models.AccountStreak,   AccountStreakAdmin)
admin_site.register(models.LevelThreshold, LevelThresholdAdmin)
admin_site.register(models.Reward,         RewardAdmin)
admin_site.register(models.RewardEventLog,  RewardEventLogAdmin)
admin_site.register(models.Skill,          SkillAdmin)
