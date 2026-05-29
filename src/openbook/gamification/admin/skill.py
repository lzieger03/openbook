# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>

from openbook.admin import CustomModelAdmin

from ..models.skill import Skill


class SkillAdmin(CustomModelAdmin):
    model = Skill
    list_display = ["name", "description", "icon_path"]
    ordering = ["name"]
    search_fields = ["name", "description", "icon_path"]
