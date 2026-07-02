# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
# Ledejna Salihi (@LedejnaSalihi)
# Lars Zieger (@lzieger03)

from openbook.admin import CustomModelAdmin

from ..models.level_threshold import LevelThreshold


class LevelThresholdAdmin(CustomModelAdmin):
    model         = LevelThreshold
    list_display  = ["level", "min_points"]
    list_filter   = ["level"]
    ordering      = ["min_points", "level"]
