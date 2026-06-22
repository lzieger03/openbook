# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>

from datetime           import timedelta

from django.db          import transaction
from django.db.models   import F
from django.utils       import timezone

from ..constants                    import BERLIN_TZ, LearningActivityType, StreakEventType
from ..models.account_activity_day  import AccountActivityDay
from ..models.account_streak        import AccountStreak
from ..models.reward_event_log      import RewardEventLog

# A streak is broken when more than this much time passes between the previous
# and the current activity.
STREAK_BREAK_GAP = timedelta(hours=24)


def _normalize(occurred_at):
    """Return a timezone-aware datetime, defaulting to now."""
    if occurred_at is None:
        return timezone.now()
    if timezone.is_naive(occurred_at):
        return timezone.make_aware(occurred_at, timezone.get_current_timezone())
    return occurred_at


def _log_event(account_id, event_type, context=None):
    """
    Append an entry to the reward event log. Streak events carry no reward and a
    zero point delta, so they do not affect the account's point total.
    """
    # Avoid creating repeated daily 'already counted' streak events. They are
    # noisy in the audit log and carry no points, so only record one per
    # account/date when activity_date is provided in the context.
    if event_type == StreakEventType.STREAK_ALREADY_COUNTED_TODAY:
        activity_date = None
        if context:
            activity_date = context.get("activity_date")

        if activity_date:
            exists = RewardEventLog.objects.filter(
                account_id=account_id,
                event_type=event_type,
                context__activity_date=activity_date,
            ).exists()
        else:
            exists = RewardEventLog.objects.filter(
                account_id=account_id,
                event_type=event_type,
            ).exists()

        if exists:
            return

    RewardEventLog.objects.create(
        account_id   = account_id,
        reward       = None,
        event_type   = event_type,
        points_delta = 0,
        context      = context or {},
    )


def get_streak_state(account_id) -> dict:
    """
    Return the current streak state for an account. Accounts without any recorded
    activity yet are reported with a zeroed, never-active streak.
    """
    streak = AccountStreak.objects.filter(account_id=account_id).first()

    if streak is None:
        return {
            "current_streak":   0,
            "longest_streak":   0,
            "last_active_date": None,
            "streak_freezes":   0,
        }

    return {
        "current_streak":   streak.current_streak,
        "longest_streak":   streak.longest_streak,
        "last_active_date": streak.last_active_date,
        "streak_freezes":   streak.streak_freezes,
    }


def _advance_streak(account_id, occurred_at, *, log_events=True) -> dict:
    """
    Record one activity for the given moment and advance the streak.

    Rules:
    - First ever activity starts the streak at 1.
    - More than 24h since the previous activity breaks and restarts the streak.
    - Another activity on the same calendar day (Europe/Berlin) does not advance.
    - Otherwise the streak increments by one.

    The per-day row keeps the operation idempotent for repeated same-day activity.
    Must be called inside a transaction.
    """
    local_date = occurred_at.astimezone(BERLIN_TZ).date()

    activity_day, day_created = AccountActivityDay.objects.get_or_create(
        account_id    = account_id,
        activity_date = local_date,
        defaults      = {
            "activity_count":    1,
            "first_activity_at": occurred_at,
            "last_activity_at":  occurred_at,
        },
    )

    if not day_created:
        AccountActivityDay.objects.filter(pk=activity_day.pk).update(
            activity_count   = F("activity_count") + 1,
            last_activity_at = occurred_at,
        )

    streak, _ = AccountStreak.objects.select_for_update().get_or_create(account_id=account_id)
    previous_at = streak.last_active_at

    event_type = None

    if previous_at is None:
        streak.current_streak = 1
        event_type = StreakEventType.STREAK_STARTED
    elif occurred_at < previous_at:
        # Backdated activity: never move the streak backwards.
        event_type = None
    elif occurred_at - previous_at > STREAK_BREAK_GAP:
        streak.current_streak = 1
        event_type = StreakEventType.STREAK_RESET
    elif local_date == streak.last_active_date:
        event_type = StreakEventType.STREAK_ALREADY_COUNTED_TODAY
    else:
        streak.current_streak += 1
        event_type = StreakEventType.STREAK_INCREMENTED

    if previous_at is None or occurred_at > previous_at:
        streak.last_active_at   = occurred_at
        streak.last_active_date = local_date

    if streak.current_streak > streak.longest_streak:
        streak.longest_streak = streak.current_streak

    streak.save()

    if log_events and event_type is not None:
        _log_event(account_id, event_type, {
            "current_streak": streak.current_streak,
            "longest_streak": streak.longest_streak,
            "activity_date":  local_date.isoformat(),
        })

    return get_streak_state(account_id)


@transaction.atomic
def record_learning_activity(account_id, activity_type, occurred_at=None, metadata=None) -> dict:
    """
    Record an explicit learning activity and advance the daily streak. Runs in one
    transaction; the per-day unique constraint keeps duplicate/concurrent calls for
    the same day idempotent.
    """
    if activity_type not in LearningActivityType.values:
        raise ValueError(f"Invalid learning activity type: {activity_type!r}")

    occurred_at = _normalize(occurred_at)
    local_date  = occurred_at.astimezone(BERLIN_TZ).date()

    context = dict(metadata or {})
    context["activity_type"] = activity_type
    context["activity_date"] = local_date.isoformat()

    _log_event(account_id, StreakEventType.LEARNING_ACTIVITY_RECORDED, context)

    return _advance_streak(account_id, occurred_at, log_events=True)


@transaction.atomic
def update_streak_for_points(account_id, occurred_at=None) -> dict:
    """
    Recompute the streak because the account just earned points. Used by the reward
    event signal so any point-earning event keeps the streak up to date.
    """
    return _advance_streak(account_id, _normalize(occurred_at), log_events=True)
