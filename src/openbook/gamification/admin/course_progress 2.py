# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>

from openbook.admin import CustomModelAdmin

from ..models.course_progress import CourseProgress


class CourseProgressAdmin(CustomModelAdmin):
    model = CourseProgress
    list_display = ["account", "course", "course_points", "course_level", "course_progress"]
    list_filter = ["course_level"]
    search_fields = ["account__username", "account__email", "course__name"]