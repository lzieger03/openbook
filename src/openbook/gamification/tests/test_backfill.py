# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>

from datetime           import date, datetime

from django.test        import TestCase

from openbook.auth.models.user import User
from ..constants               import BERLIN_TZ, StreakEventType
from ..models                  import AccountActivityDay, AccountStreak, RewardEventLog
from ..services.backfill       import backfill_account_streak, backfill_all_streaks


def make_log(user, year, month, day, event_type="level_completed"):
    """Create a reward event log entry on a specific Europe/Berlin day."""
    entry = RewardEventLog.objects.create(
        account=user, reward=None, event_type=event_type, points_delta=0, context={},
    )
    # created_at uses auto_now_add, so override it explicitly afterwards.
    RewardEventLog.objects.filter(pk=entry.pk).update(
        created_at=datetime(year, month, day, 12, 0, tzinfo=BERLIN_TZ),
    )


class Backfill_Tests(TestCase):
    """Tests for recomputing streaks from reward_event_log history."""

    def setUp(self):
        self.user = User.objects.create_user("bfuser", password="password", email="bf@test.com")

    def test_consecutive_days_build_streak(self):
        """Consecutive activity days yield a matching current and longest streak."""
        for day in (1, 2, 3):
            make_log(self.user, 2026, 3, day)

        state = backfill_account_streak(self.user.id)

        self.assertEqual(state["current_streak"], 3)
        self.assertEqual(state["longest_streak"], 3)
        self.assertEqual(state["last_active_date"], date(2026, 3, 3))
        self.assertEqual(AccountActivityDay.objects.filter(account=self.user).count(), 3)

    def test_gap_keeps_longest_but_resets_current(self):
        """A gap before the latest day resets current streak but preserves the record."""
        for day in (1, 2, 3):
            make_log(self.user, 2026, 3, day)
        make_log(self.user, 2026, 3, 6)

        state = backfill_account_streak(self.user.id)

        self.assertEqual(state["current_streak"], 1)
        self.assertEqual(state["longest_streak"], 3)
        self.assertEqual(state["last_active_date"], date(2026, 3, 6))

    def test_streak_bookkeeping_events_are_ignored(self):
        """STREAK_* events are not counted as activity days during backfill."""
        make_log(self.user, 2026, 3, 1)
        make_log(self.user, 2026, 3, 2, event_type=StreakEventType.STREAK_STARTED)

        state = backfill_account_streak(self.user.id)

        self.assertEqual(state["current_streak"], 1)
        self.assertEqual(AccountActivityDay.objects.filter(account=self.user).count(), 1)

    def test_backfill_is_idempotent(self):
        """Running the backfill twice produces the same state and no duplicate days."""
        for day in (1, 2):
            make_log(self.user, 2026, 3, day)

        backfill_account_streak(self.user.id)
        state = backfill_account_streak(self.user.id)

        self.assertEqual(state["current_streak"], 2)
        self.assertEqual(state["longest_streak"], 2)
        self.assertEqual(AccountActivityDay.objects.filter(account=self.user).count(), 2)
        self.assertEqual(AccountStreak.objects.filter(account=self.user).count(), 1)

    def test_backfill_all_creates_row_for_user_without_activity(self):
        """Users without any logged activity still receive a zeroed streak row."""
        other = User.objects.create_user("noactivity", password="password", email="no@test.com")

        backfill_all_streaks()

        streak = AccountStreak.objects.get(account=other)
        self.assertEqual(streak.current_streak, 0)
        self.assertEqual(streak.longest_streak, 0)
        self.assertIsNone(streak.last_active_date)
