# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
# Ledejna Salihi (@LedejnaSalihi)
# Lars Zieger (@lzieger03)

from django.contrib.auth import get_user_model
from django.test         import TestCase

from ..models import AccountProgress, LevelThreshold, Reward, RewardEventLog

User = get_user_model()


class LevelThreshold_Tests(TestCase):
    """Tests for level computation from the LevelThreshold table."""

    def test_level_for_points_defaults_to_one(self):
        """Without any matching threshold the level is the starting level 1."""
        self.assertEqual(LevelThreshold.level_for_points(0), 1)
        self.assertEqual(LevelThreshold.level_for_points(9999), 1)

    def test_level_for_points_picks_highest_reached(self):
        """level_for_points returns the highest level whose required points are reached."""
        LevelThreshold.objects.create(level=2, min_points=100)
        LevelThreshold.objects.create(level=3, min_points=250)

        self.assertEqual(LevelThreshold.level_for_points(50), 1)
        self.assertEqual(LevelThreshold.level_for_points(100), 2)
        self.assertEqual(LevelThreshold.level_for_points(249), 2)
        self.assertEqual(LevelThreshold.level_for_points(250), 3)
        self.assertEqual(LevelThreshold.level_for_points(1000), 3)

    def test_reward_event_raises_level(self):
        """Earning enough points through reward events bumps the account level."""
        LevelThreshold.objects.create(level=2, min_points=100)

        user = User.objects.create_user(
            username = "level-user",
            email    = "level-user@test.com",
            password = "password",
        )

        self.assertEqual(AccountProgress.objects.get(account=user).level, 1)

        reward = Reward.objects.create(reward_type="quiz_complete", value=120)

        RewardEventLog.objects.create(
            account      = user,
            reward       = reward,
            event_type   = "quiz_complete",
            points_delta = 120,
            context      = {},
        )

        progress = AccountProgress.objects.get(account=user)
        self.assertEqual(progress.point_total, 120)
        self.assertEqual(progress.level, 2)
