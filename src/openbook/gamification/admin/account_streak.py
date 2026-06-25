# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
# Ledejna Salihi (@LedejnaSalihi)
# Lars Zieger (@lzieger03)

from openbook.admin import CustomModelAdmin

from ..models.account_streak import AccountStreak


class AccountStreakAdmin(CustomModelAdmin):
    model           = AccountStreak
    list_display    = ["account", "current_streak", "longest_streak", "last_active_date", "streak_freezes", "updated_at"]
    list_filter     = ["last_active_date", "updated_at"]
    search_fields   = ["account__username", "account__email"]
    readonly_fields = ["created_at", "updated_at"]
