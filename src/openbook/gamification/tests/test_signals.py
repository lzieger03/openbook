# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>

from django.contrib.auth import get_user_model
from django.test         import TestCase

from ..models            import AccountProgress
from ..models            import Reward
from ..models            import RewardEventLog

User = get_user_model()

class Gamification_Signal_Tests(TestCase):
    """Tests for gamification signal handlers."""

    def test_account_points_created_for_new_user(self):
        """A new user automatically gets an AccountProgress row with 0 points."""
        user = User.objects.create_user(
            username = "signal-user-1",
            email    = "signal-user-1@test.com",
            password = "password",
        )

        self.assertTrue(AccountProgress.objects.filter(account=user).exists())
        self.assertEqual(AccountProgress.objects.get(account=user).point_total, 0)

    def test_reward_event_updates_point_total(self):
        """Creating a RewardEventLog entry increments the current account point total."""
        user = User.objects.create_user(
            username = "signal-user-2",
            email    = "signal-user-2@test.com",
            password = "password",
        )

        reward = Reward.objects.create(
            reward_type = "question_correct",
            value       = 10,
        )

        RewardEventLog.objects.create(
            account      = user,
            reward       = reward,
            event_type   = "question_correct",
            points_delta = 10,
            context      = {"question_id": "q-1"},
        )

        account_points = AccountProgress.objects.get(account=user)
        self.assertEqual(account_points.point_total, 10)

    def test_reward_event_recreates_missing_account_points(self):
        """If AccountProgress was deleted, RewardEventLog creation recreates it and applies delta."""
        user = User.objects.create_user(
            username = "signal-user-3",
            email    = "signal-user-3@test.com",
            password = "password",
        )

        reward = Reward.objects.create(
            reward_type = "quiz_complete",
            value       = 50,
        )

        AccountProgress.objects.filter(account=user).delete()
        self.assertFalse(AccountProgress.objects.filter(account=user).exists())

        RewardEventLog.objects.create(
            account      = user,
            reward       = reward,
            event_type   = "quiz_complete",
            points_delta = 50,
            context      = {"quiz_id": "quiz-1"},
        )

        account_points = AccountProgress.objects.get(account=user)
        self.assertEqual(account_points.point_total, 50)
