# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>

from openbook.admin import CustomModelAdmin

from ..models.account_points import AccountPoints


class AccountPointsAdmin(CustomModelAdmin):
    model          = AccountPoints
    list_display    = ["account", "point_total", "updated_at"]
    list_filter     = ["updated_at"]
    search_fields   = ["account__username", "account__email"]
    readonly_fields = ["updated_at"]
