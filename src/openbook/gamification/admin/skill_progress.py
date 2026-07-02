# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
# Ledejna Salihi (@LedejnaSalihi)
# Lars Zieger (@lzieger03)

from openbook.admin import CustomModelAdmin

from ..models.skill_progress import SkillProgress


class SkillProgressAdmin(CustomModelAdmin):
    model = SkillProgress
    list_display = ["account", "skill", "level", "progress"]
    list_filter = ["level"]
    ordering = ["account", "skill"]
    search_fields = ["account__username", "account__email", "skill__name"]
