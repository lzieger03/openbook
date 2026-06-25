# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>

"""
Turn learning activities into gamification points.

This is the bridge between the learning/assistant side (a learner answers a quiz or
asks a question in the course chat) and the gamification point system. It decides how
many points an activity is worth and then feeds them through the existing services so
every point lands in all the right places at once:

* ``award_course_points`` raises the per-course progress (course points, course level
  and the course progress bar) and logs a reward event, which in turn raises the
  account's overall point total ("Gesamtpunkte"), the global level and the streak.
* ``award_skill_progress`` raises the matching skill(s) on the learner's dashboard.

Two activities are rewarded:

Quiz answers
    Points are proportional to the quiz score (share of correct answers). To prevent
    farming by re-taking a quiz, only an *improvement* over the best score ever
    rewarded for that page is paid out. The same improvement also advances the skills
    that the page trains (``TextbookPage.skills``) – so an HTML quiz only grows the
    HTML skill.

Chat questions
    Asking a question in a course chat grants a small flat reward, capped to a number
    of rewarded questions per day and course so it cannot be farmed by spamming.
"""

from __future__ import annotations

from datetime import UTC

from django.db        import transaction
from django.db.models import Sum
from django.utils     import timezone

from ..constants                import BERLIN_TZ, CourseEventType
from ..models.reward_event_log  import RewardEventLog
from .course                    import award_course_points, get_course_progress_state
from .skill                     import award_skill_progress

# --- Tunable reward configuration -------------------------------------------------

# Maximum course points a single page quiz can be worth (at a perfect score). The
# actual award scales with the score, e.g. an 80 % score is worth 80 % of this.
QUIZ_MAX_COURSE_POINTS = 50

# Percentage points of skill progress granted per earned course quiz point. With 0.5,
# a 40-point quiz improvement advances each trained skill by 20 % (= one fifth level).
QUIZ_SKILL_PROGRESS_PER_POINT = 0.5

# Maximum course points a single textbook exam can be worth (at a perfect score). Exams
# are worth more than a quiz because they cover the whole textbook and are AI-graded.
EXAM_MAX_COURSE_POINTS = 100

# Percentage points of skill progress granted per earned course exam point.
EXAM_SKILL_PROGRESS_PER_POINT = 0.5

# Course points granted for asking one question in the course chat.
CHAT_QUESTION_POINTS = 5

# Maximum number of chat questions that are rewarded per day and course. Further
# questions on the same day still work, they just stop earning points.
CHAT_QUESTION_DAILY_LIMIT = 10


def _quiz_points_already_awarded(account_id, page_id) -> int:
    """
    Return the course points already paid out for this account's quiz on ``page_id``.

    Because quiz awards are always positive (only improvements are paid), this sum
    equals ``round(best_score_so_far * QUIZ_MAX_COURSE_POINTS)`` and therefore acts as
    the high-water mark used to reward only further improvement.
    """
    total = (
        RewardEventLog.objects
        .filter(
            account_id            = account_id,
            event_type            = CourseEventType.QUIZ_POINTS_AWARDED,
            context__page_id      = str(page_id),
        )
        .aggregate(total=Sum("points_delta"))
        .get("total")
    )
    return total or 0


@transaction.atomic
def award_quiz_rewards(account_id, course_id, page_id, score, skill_ids=None) -> dict:
    """
    Reward a quiz attempt on a course page.

    ``score`` is the normalized share of correct answers (0.0–1.0). Points are
    proportional to the score, and only the improvement over the best previously
    rewarded score for this page is granted. The same improvement is also added as
    skill progress to every skill in ``skill_ids`` (typically the page's skills).

    Returns a summary describing what was awarded.
    """
    score = max(0.0, min(float(score), 1.0))
    skill_ids = list(skill_ids or [])

    target_points = round(score * QUIZ_MAX_COURSE_POINTS)
    already        = _quiz_points_already_awarded(account_id, page_id)
    delta          = target_points - already

    if delta <= 0:
        # No improvement over the best score so far – nothing new to reward.
        return {
            "points_awarded":  0,
            "skills_advanced": [],
            "course_progress": get_course_progress_state(account_id, course_id),
        }

    award_course_points(
        account_id,
        course_id,
        delta,
        event_type = CourseEventType.QUIZ_POINTS_AWARDED,
        context    = {
            "page_id": str(page_id),
            "score":   score,
            "source":  "quiz",
        },
    )

    skill_amount     = delta * QUIZ_SKILL_PROGRESS_PER_POINT
    skills_advanced  = []

    if skill_amount > 0:
        for skill_id in skill_ids:
            award_skill_progress(account_id, skill_id, skill_amount)
            skills_advanced.append(str(skill_id))

    return {
        "points_awarded":  delta,
        "skills_advanced": skills_advanced,
        "course_progress": get_course_progress_state(account_id, course_id),
    }


def _exam_points_already_awarded(account_id, page_id) -> int:
    """
    Return the course points already paid out for this account's exam on ``page_id``.

    Like the quiz high-water mark, but tracked separately under the exam event type so
    exam points are awarded independently of quiz points for the same page.
    """
    total = (
        RewardEventLog.objects
        .filter(
            account_id       = account_id,
            event_type       = CourseEventType.EXAM_POINTS_AWARDED,
            context__page_id = str(page_id),
        )
        .aggregate(total=Sum("points_delta"))
        .get("total")
    )
    return total or 0


@transaction.atomic
def award_exam_rewards(account_id, course_id, page_id, score, skill_ids=None) -> dict:
    """
    Reward an exam attempt on a course textbook (anchored to its first page).

    Works like :func:`award_quiz_rewards` but with its own, higher point ceiling and a
    separate high-water mark, so exam points add to the course progress, the overall
    account total and the course skills on top of any quiz points already earned. Only
    the improvement over the best previously rewarded exam score for this page is paid.
    """
    score = max(0.0, min(float(score), 1.0))
    skill_ids = list(skill_ids or [])

    target_points = round(score * EXAM_MAX_COURSE_POINTS)
    already        = _exam_points_already_awarded(account_id, page_id)
    delta          = target_points - already

    if delta <= 0:
        return {
            "points_awarded":  0,
            "skills_advanced": [],
            "course_progress": get_course_progress_state(account_id, course_id),
        }

    award_course_points(
        account_id,
        course_id,
        delta,
        event_type = CourseEventType.EXAM_POINTS_AWARDED,
        context    = {
            "page_id": str(page_id),
            "score":   score,
            "source":  "exam",
        },
    )

    skill_amount    = delta * EXAM_SKILL_PROGRESS_PER_POINT
    skills_advanced = []

    if skill_amount > 0:
        for skill_id in skill_ids:
            award_skill_progress(account_id, skill_id, skill_amount)
            skills_advanced.append(str(skill_id))

    return {
        "points_awarded":  delta,
        "skills_advanced": skills_advanced,
        "course_progress": get_course_progress_state(account_id, course_id),
    }


def _chat_questions_rewarded_today(account_id, course_id) -> int:
    """Return how many chat questions were already rewarded today (Europe/Berlin)."""
    local_now   = timezone.now().astimezone(BERLIN_TZ)
    start_local = local_now.replace(hour=0, minute=0, second=0, microsecond=0)
    start_utc   = start_local.astimezone(UTC)

    return RewardEventLog.objects.filter(
        account_id          = account_id,
        event_type          = CourseEventType.CHAT_POINTS_AWARDED,
        context__course_id  = str(course_id),
        created_at__gte     = start_utc,
    ).count()


@transaction.atomic
def award_chat_question_reward(account_id, course_id) -> dict:
    """
    Reward asking one question in a course chat.

    Grants a small flat number of course points, but stops once the daily per-course
    limit of rewarded questions is reached, so the reward cannot be farmed by spamming
    messages. Returns a summary describing what was awarded.
    """
    if _chat_questions_rewarded_today(account_id, course_id) >= CHAT_QUESTION_DAILY_LIMIT:
        return {
            "points_awarded":  0,
            "daily_limit":     CHAT_QUESTION_DAILY_LIMIT,
            "course_progress": get_course_progress_state(account_id, course_id),
        }

    award_course_points(
        account_id,
        course_id,
        CHAT_QUESTION_POINTS,
        event_type = CourseEventType.CHAT_POINTS_AWARDED,
        context    = {
            "course_id": str(course_id),
            "source":    "chat_question",
        },
    )

    return {
        "points_awarded":  CHAT_QUESTION_POINTS,
        "daily_limit":     CHAT_QUESTION_DAILY_LIMIT,
        "course_progress": get_course_progress_state(account_id, course_id),
    }
