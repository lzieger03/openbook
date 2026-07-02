# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
# Ledejna Salihi (@LedejnaSalihi)
# Lars Zieger (@lzieger03)

from datetime           import date, datetime

from django.test        import TestCase
from django.urls        import reverse
from rest_framework.test import APIClient

from openbook.auth.models.user import User
from ..constants               import BERLIN_TZ, LearningActivityType, StreakEventType
from ..models                  import AccountActivityDay, AccountStreak, RewardEventLog
from ..services.streak         import get_streak_state, record_learning_activity


def at(year, month, day, hour=12):
    """Build a timezone-aware datetime in Europe/Berlin."""
    return datetime(year, month, day, hour, 0, tzinfo=BERLIN_TZ)


class Streak_Service_Tests(TestCase):
    """Tests for the streak service rules."""

    def setUp(self):
        self.user = User.objects.create_user("streakuser", password="password", email="streak@test.com")

    def test_first_activity_starts_streak(self):
        """The first learning activity starts the streak at 1 and logs STREAK_STARTED."""
        state = record_learning_activity(
            self.user.id, LearningActivityType.QUIZ_COMPLETED, occurred_at=at(2026, 1, 1),
        )

        self.assertEqual(state["current_streak"], 1)
        self.assertEqual(state["longest_streak"], 1)
        self.assertEqual(state["last_active_date"], date(2026, 1, 1))
        self.assertTrue(
            RewardEventLog.objects.filter(
                account=self.user, event_type=StreakEventType.STREAK_STARTED,
            ).exists()
        )

    def test_same_day_does_not_increment(self):
        """A second activity on the same day bumps the counter but not the streak."""
        record_learning_activity(self.user.id, LearningActivityType.CHAT_MESSAGE_SENT, occurred_at=at(2026, 1, 1, 9))
        state = record_learning_activity(self.user.id, LearningActivityType.QUIZ_ANSWERED, occurred_at=at(2026, 1, 1, 18))

        self.assertEqual(state["current_streak"], 1)
        self.assertEqual(AccountActivityDay.objects.filter(account=self.user).count(), 1)
        self.assertEqual(AccountActivityDay.objects.get(account=self.user).activity_count, 2)
        self.assertTrue(
            RewardEventLog.objects.filter(
                account=self.user, event_type=StreakEventType.STREAK_ALREADY_COUNTED_TODAY,
            ).exists()
        )

    def test_next_day_increments_streak(self):
        """An activity on the following calendar day increments the streak."""
        record_learning_activity(self.user.id, LearningActivityType.QUIZ_COMPLETED, occurred_at=at(2026, 1, 1))
        state = record_learning_activity(self.user.id, LearningActivityType.QUIZ_COMPLETED, occurred_at=at(2026, 1, 2))

        self.assertEqual(state["current_streak"], 2)
        self.assertEqual(state["longest_streak"], 2)
        self.assertTrue(
            RewardEventLog.objects.filter(
                account=self.user, event_type=StreakEventType.STREAK_INCREMENTED,
            ).exists()
        )

    def test_missed_day_resets_streak(self):
        """Skipping one or more days resets the current streak to 1."""
        record_learning_activity(self.user.id, LearningActivityType.QUIZ_COMPLETED, occurred_at=at(2026, 1, 1))
        record_learning_activity(self.user.id, LearningActivityType.QUIZ_COMPLETED, occurred_at=at(2026, 1, 2))
        state = record_learning_activity(self.user.id, LearningActivityType.QUIZ_COMPLETED, occurred_at=at(2026, 1, 4))

        self.assertEqual(state["current_streak"], 1)
        self.assertEqual(state["longest_streak"], 2)
        self.assertTrue(
            RewardEventLog.objects.filter(
                account=self.user, event_type=StreakEventType.STREAK_RESET,
            ).exists()
        )

    def test_longest_streak_is_preserved_after_reset(self):
        """The longest streak keeps the record even after the current streak resets."""
        for day in (1, 2, 3):
            record_learning_activity(self.user.id, LearningActivityType.QUIZ_COMPLETED, occurred_at=at(2026, 1, day))

        record_learning_activity(self.user.id, LearningActivityType.QUIZ_COMPLETED, occurred_at=at(2026, 1, 6))

        state = get_streak_state(self.user.id)
        self.assertEqual(state["current_streak"], 1)
        self.assertEqual(state["longest_streak"], 3)

    def test_learning_activity_recorded_event_written(self):
        """Every recorded activity writes a LEARNING_ACTIVITY_RECORDED event."""
        record_learning_activity(self.user.id, LearningActivityType.GAME_PLAYED, occurred_at=at(2026, 1, 1))

        self.assertEqual(
            RewardEventLog.objects.filter(
                account=self.user, event_type=StreakEventType.LEARNING_ACTIVITY_RECORDED,
            ).count(),
            1,
        )

    def test_invalid_activity_type_rejected(self):
        """A non-learning activity type (e.g. login) is rejected."""
        with self.assertRaises(ValueError):
            record_learning_activity(self.user.id, "LOGIN", occurred_at=at(2026, 1, 1))

    def test_duplicate_calls_do_not_create_duplicate_day_rows(self):
        """Duplicate calls for the same day create exactly one activity-day row."""
        timestamp = at(2026, 1, 1, 10)
        record_learning_activity(self.user.id, LearningActivityType.QUIZ_COMPLETED, occurred_at=timestamp)
        record_learning_activity(self.user.id, LearningActivityType.QUIZ_COMPLETED, occurred_at=timestamp)

        self.assertEqual(AccountActivityDay.objects.filter(account=self.user).count(), 1)
        self.assertEqual(AccountStreak.objects.get(account=self.user).current_streak, 1)

    def test_gap_over_24h_breaks_streak(self):
        """More than 24h between activities breaks the streak even on the next day."""
        record_learning_activity(self.user.id, LearningActivityType.QUIZ_COMPLETED, occurred_at=at(2026, 1, 1, 12))
        state = record_learning_activity(self.user.id, LearningActivityType.QUIZ_COMPLETED, occurred_at=at(2026, 1, 2, 13))

        self.assertEqual(state["current_streak"], 1)
        self.assertTrue(
            RewardEventLog.objects.filter(
                account=self.user, event_type=StreakEventType.STREAK_RESET,
            ).exists()
        )

    def test_gap_within_24h_next_day_increments(self):
        """An activity on the next day within 24h increments the streak."""
        record_learning_activity(self.user.id, LearningActivityType.QUIZ_COMPLETED, occurred_at=at(2026, 1, 1, 20))
        state = record_learning_activity(self.user.id, LearningActivityType.QUIZ_COMPLETED, occurred_at=at(2026, 1, 2, 19))

        self.assertEqual(state["current_streak"], 2)


class Streak_Signal_Tests(TestCase):
    """Tests that earning points advances the streak via the reward event signal."""

    def setUp(self):
        self.user = User.objects.create_user("pointsuser", password="password", email="points@test.com")

    def test_point_earning_event_advances_streak(self):
        """Creating a point-earning reward event advances the streak."""
        RewardEventLog.objects.create(
            account=self.user, reward=None, event_type="quiz_answer_correct", points_delta=10, context={},
        )

        streak = AccountStreak.objects.get(account=self.user)
        self.assertEqual(streak.current_streak, 1)
        self.assertEqual(streak.longest_streak, 1)

    def test_zero_delta_event_does_not_advance_streak(self):
        """An event without points does not advance the streak."""
        RewardEventLog.objects.create(
            account=self.user, reward=None, event_type="info_only", points_delta=0, context={},
        )

        streak = AccountStreak.objects.filter(account=self.user).first()
        self.assertTrue(streak is None or streak.current_streak == 0)


class Streak_API_Tests(TestCase):
    """Tests for the streak / activity REST endpoints."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user("apiuser", password="password", email="api@test.com")

    def test_record_activity_endpoint_starts_streak(self):
        """POST /api/gamification/activity records an activity and returns the streak state."""
        self.client.force_authenticate(self.user)

        response = self.client.post(
            reverse("activity-list"),
            {"activity_type": "QUIZ_COMPLETED"},
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["current_streak"], 1)
        self.assertEqual(response.data["longest_streak"], 1)

    def test_streak_endpoint_returns_state(self):
        """GET /api/gamification/streak returns the current streak state."""
        self.client.force_authenticate(self.user)

        response = self.client.get(reverse("streak-list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["current_streak"], 0)
        self.assertEqual(response.data["longest_streak"], 0)

    def test_invalid_activity_type_returns_400(self):
        """A login (non-learning) activity type is rejected by the endpoint."""
        self.client.force_authenticate(self.user)

        response = self.client.post(
            reverse("activity-list"),
            {"activity_type": "LOGIN"},
            format="json",
        )

        self.assertEqual(response.status_code, 400)

    def test_endpoints_require_authentication(self):
        """Unauthenticated requests are rejected."""
        response = self.client.get(reverse("streak-list"))
        self.assertIn(response.status_code, [401, 403])
