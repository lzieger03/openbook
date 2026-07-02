# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
# Ledejna Salihi (@LedejnaSalihi)
# Lars Zieger (@lzieger03)

from openbook.admin import CustomModelAdmin

from ..models.account_activity_day import AccountActivityDay


class AccountActivityDayAdmin(CustomModelAdmin):
    model           = AccountActivityDay
    list_display    = ["account", "activity_date", "activity_count", "first_activity_at", "last_activity_at"]
    list_filter     = ["activity_date"]
    search_fields   = ["account__username", "account__email"]
    readonly_fields = ["created_at", "updated_at"]
