# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>

from openbook.admin import CustomModelAdmin

from ..models.skill import Skill


class SkillAdmin(CustomModelAdmin):
    model        = Skill
    list_display  = ["account", "name", "level", "progress"]
    list_filter   = ["level"]
    search_fields = ["account__username", "account__email", "name"]
