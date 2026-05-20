# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>

from openbook.admin import CustomModelAdmin

from ..models.reward import Reward


class RewardAdmin(CustomModelAdmin):
    model        = Reward
    list_display  = ["reward_type", "value"]
    list_filter   = ["reward_type"]
    search_fields = ["reward_type", "description"]
    list_editable = ["value"]
    ordering = ["reward_type", "-value"]
