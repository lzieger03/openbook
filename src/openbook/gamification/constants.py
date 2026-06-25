# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>

from zoneinfo                  import ZoneInfo

from django.db                  import models
from django.utils.translation   import gettext_lazy as _

# Timezone used to derive the calendar day a learning activity belongs to.
BERLIN_TZ = ZoneInfo("Europe/Berlin")


class LearningActivityType(models.TextChoices):
    """
    Activity types that count as a real learning activity and may advance the
    daily streak. A plain login is intentionally not part of this list.
    """
    CHAT_MESSAGE_SENT = "CHAT_MESSAGE_SENT", _("Chat Message Sent")
    QUIZ_ANSWERED     = "QUIZ_ANSWERED",     _("Quiz Answered")
    QUIZ_COMPLETED    = "QUIZ_COMPLETED",    _("Quiz Completed")
    CONTENT_VIEWED    = "CONTENT_VIEWED",    _("Content Viewed")
    MODULE_COMPLETED  = "MODULE_COMPLETED",  _("Module Completed")
    GAME_PLAYED       = "GAME_PLAYED",       _("Game Played")


class CourseEventType(models.TextChoices):
    """
    Event types written to the reward event log when a learner earns points inside
    a course. These carry a non-zero point delta so the global account progress and
    streak are updated alongside the per-course progress.
    """
    COURSE_POINTS_AWARDED = "COURSE_POINTS_AWARDED", _("Course Points Awarded")
    QUIZ_POINTS_AWARDED   = "QUIZ_POINTS_AWARDED",   _("Quiz Points Awarded")
    EXAM_POINTS_AWARDED   = "EXAM_POINTS_AWARDED",   _("Exam Points Awarded")
    CHAT_POINTS_AWARDED   = "CHAT_POINTS_AWARDED",   _("Chat Points Awarded")


class StreakEventType(models.TextChoices):
    """
    Event types written to the reward event log when a learning activity is
    recorded and the streak state changes.
    """
    STREAK_STARTED               = "STREAK_STARTED",               _("Streak Started")
    STREAK_INCREMENTED           = "STREAK_INCREMENTED",           _("Streak Incremented")
    STREAK_RESET                 = "STREAK_RESET",                 _("Streak Reset")
    STREAK_ALREADY_COUNTED_TODAY = "STREAK_ALREADY_COUNTED_TODAY", _("Streak Already Counted Today")
    LEARNING_ACTIVITY_RECORDED   = "LEARNING_ACTIVITY_RECORDED",   _("Learning Activity Recorded")
