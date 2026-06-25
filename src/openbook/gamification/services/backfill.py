# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
# Ledejna Salihi (@LedejnaSalihi)
# Lars Zieger (@lzieger03)

from django.contrib.auth import get_user_model
from django.db          import transaction

from ..constants                import StreakEventType
from ..models.account_activity_day import AccountActivityDay
from ..models.account_streak    import AccountStreak
from ..models.reward_event_log  import RewardEventLog
from .streak                    import _advance_streak, get_streak_state

User = get_user_model()


@transaction.atomic
def backfill_account_streak(account_id) -> dict:
    """
    Recompute the streak for a single account by replaying its point-earning reward
    events in chronological order through the same streak rules used at runtime
    (including the 24h break rule). Streak bookkeeping events are skipped.

    Idempotent: the streak and per-day rows are reset first, so re-running yields
    the same result.
    """
    AccountActivityDay.objects.filter(account_id=account_id).delete()
    AccountStreak.objects.update_or_create(
        account_id = account_id,
        defaults   = {
            "current_streak":   0,
            "longest_streak":   0,
            "last_active_at":   None,
            "last_active_date": None,
        },
    )

    events = (
        RewardEventLog.objects
        .filter(account_id=account_id)
        .exclude(event_type__in=StreakEventType.values)
        .order_by("created_at")
        .only("created_at")
    )

    for event in events:
        _advance_streak(account_id, event.created_at, log_events=False)

    return get_streak_state(account_id)


def backfill_all_streaks():
    """
    Ensure every existing user has a recomputed AccountStreak row. Returns a list
    of (username, state) tuples.
    """
    results = []

    for user in User.objects.all().order_by("username"):
        state = backfill_account_streak(user.id)
        results.append((user.get_username(), state))

    return results
