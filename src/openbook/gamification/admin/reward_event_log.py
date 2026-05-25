# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>

from openbook.admin import CustomModelAdmin

from ..models.reward_event_log import RewardEventLog


class RewardEventLogAdmin(CustomModelAdmin):
    model          = RewardEventLog
    list_display    = ["account", "reward", "event_type", "points_delta", "created_at"]
    list_filter     = ["event_type", "created_at"]
    search_fields   = ["account__username", "account__email", "reward__reward_type", "event_type"]
    readonly_fields = ["created_at"]
