# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
# Ledejna Salihi (@LedejnaSalihi)
# Lars Zieger (@lzieger03)

from decimal import Decimal

from django.test import TestCase

from openbook.auth.models.user import User
from openbook.auth.middleware.current_user import reset_current_user

from ..models import Skill, SkillProgress
from ..services.skill import award_skill_progress, get_skill_progress_state


class AwardSkillProgress_Tests(TestCase):
    """Tests for the award_skill_progress service."""

    def setUp(self):
        reset_current_user()

        self.user = User.objects.create_user(
            username="skill-user",
            email="skill-user@test.com",
            password="password",
        )
        reset_current_user()

        self.skill = Skill.objects.create(name="HTML")

    def test_awarding_creates_and_increments_skill_progress(self):
        """The first award creates the row; further awards accumulate progress."""
        state = award_skill_progress(self.user.id, self.skill.id, 30)
        self.assertEqual(state["skill_level"], 1)
        self.assertEqual(state["skill_progress"], Decimal("30"))

        state = award_skill_progress(self.user.id, self.skill.id, 25)
        self.assertEqual(state["skill_level"], 1)
        self.assertEqual(state["skill_progress"], Decimal("55"))

        self.assertEqual(SkillProgress.objects.filter(account=self.user, skill=self.skill).count(), 1)

    def test_reaching_100_percent_levels_up_and_carries_over(self):
        """Filling past 100 % raises the level and carries the overflow."""
        award_skill_progress(self.user.id, self.skill.id, 80)
        state = award_skill_progress(self.user.id, self.skill.id, 30)

        self.assertEqual(state["skill_level"], 2)
        self.assertEqual(state["skill_progress"], Decimal("10"))

    def test_large_award_can_grant_several_levels(self):
        """A single big award levels up multiple times with the remainder kept."""
        state = award_skill_progress(self.user.id, self.skill.id, 250)

        self.assertEqual(state["skill_level"], 3)
        self.assertEqual(state["skill_progress"], Decimal("50"))

    def test_non_positive_amount_is_rejected(self):
        """Awarding zero or negative progress raises a ValueError."""
        with self.assertRaises(ValueError):
            award_skill_progress(self.user.id, self.skill.id, 0)

        with self.assertRaises(ValueError):
            award_skill_progress(self.user.id, self.skill.id, -10)

    def test_state_for_untrained_skill_is_zeroed(self):
        """A skill the account never trained reports level 1 at 0 %."""
        state = get_skill_progress_state(self.user.id, self.skill.id)

        self.assertEqual(state["skill_level"], 1)
        self.assertEqual(state["skill_progress"], Decimal("0"))
