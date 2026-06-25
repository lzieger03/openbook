# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
# Ledejna Salihi (@LedejnaSalihi)
# Lars Zieger (@lzieger03)

"""
Award points to a learner inside a single course.

Earning course points does two things at once:

1. It updates the learner's per-course progress (``CourseProgress``): the point
   total grows, the course level is recomputed from the shared ``LevelThreshold``
   table and the course progress bar (0–100 %) advances towards the next level.

2. It feeds the same point delta into the global gamification system by writing a
   ``RewardEventLog`` entry. The existing reward-event signal then adds the points
   to the account's overall total, recomputes the global level and advances the
   daily streak. This is how points earned in a course also move the overall level
   and point system.
"""

from django.db          import transaction

from ..constants                import CourseEventType
from ..models.course_progress   import CourseProgress
from ..models.level_threshold   import LevelThreshold
from ..models.reward_event_log  import RewardEventLog


def get_course_progress_state(account_id, course_id) -> dict:
    """
    Return the current per-course progress for an account. Courses the account has
    not earned any points in yet are reported as a fresh, zeroed progress.
    """
    progress = CourseProgress.objects.filter(account_id=account_id, course_id=course_id).first()

    if progress is None:
        return {
            "course_points":   0,
            "course_level":    1,
            "course_progress": 0,
        }

    return {
        "course_points":   progress.course_points,
        "course_level":    progress.course_level,
        "course_progress": progress.course_progress,
    }


@transaction.atomic
def award_course_points(account_id, course_id, points, *, reward=None, event_type=None, context=None) -> dict:
    """
    Award ``points`` to ``account_id`` inside ``course_id``.

    Updates the per-course progress (points, level and the progress bar) and logs a
    reward event so the same points also raise the account's overall level and point
    total. Returns the updated per-course progress state.

    ``points`` must be a non-zero integer. Negative values are allowed so points can
    be corrected, but the course point total never drops below zero.
    """
    points = int(points)

    if points == 0:
        raise ValueError("Cannot award zero course points.")

    event_type = event_type or CourseEventType.COURSE_POINTS_AWARDED

    # Make sure a progress row exists, then apply the delta atomically. select_for_update
    # keeps concurrent awards for the same account/course from clobbering each other.
    progress, _ = CourseProgress.objects.get_or_create(account_id=account_id, course_id=course_id)
    progress = CourseProgress.objects.select_for_update().get(pk=progress.pk)

    new_points = max(0, progress.course_points + points)

    progress.course_points   = new_points
    progress.course_level    = LevelThreshold.level_for_points(new_points)
    progress.course_progress = LevelThreshold.progress_to_next_level(new_points)
    progress.save(update_fields=["course_points", "course_level", "course_progress"])

    # Feed the same delta into the global system. The reward-event signal adds the
    # points to AccountProgress, recomputes the overall level and advances the streak.
    event_context = dict(context or {})
    event_context.setdefault("course_id", str(course_id))
    event_context["course_points"]   = new_points
    event_context["course_level"]    = progress.course_level
    event_context["course_progress"] = str(progress.course_progress)

    RewardEventLog.objects.create(
        account_id   = account_id,
        reward       = reward,
        event_type   = event_type,
        points_delta = points,
        context      = event_context,
    )

    return get_course_progress_state(account_id, course_id)
