# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
# Ledejna Salihi (@LedejnaSalihi)
# Lars Zieger (@lzieger03)

from django.db import IntegrityError
from django.test import RequestFactory
from django.test import TestCase

from openbook.auth.models.user import User
from openbook.auth.middleware.current_user import reset_current_user

from ..models import Skill
from ..models import SkillProgress
from ..viewsets.skill_progress import SkillProgressViewSet


class SkillProgress_Model_Tests(TestCase):
    """Tests for the SkillProgress model."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="skill-user",
            email="skill-user@test.com",
            password="password",
        )
        reset_current_user()
        self.skill = Skill.objects.create(name="Python")

    def test_skill_progress_defaults(self):
        """New skill progress rows start at level 1 and progress 0."""
        progress = SkillProgress.objects.create(account=self.user, skill=self.skill)

        self.assertEqual(progress.level, 1)
        self.assertEqual(progress.progress, 0)

    def test_skill_progress_is_unique_per_account_and_skill(self):
        """An account can only have one progress row per skill."""
        SkillProgress.objects.create(account=self.user, skill=self.skill)

        with self.assertRaises(IntegrityError):
            SkillProgress.objects.create(account=self.user, skill=self.skill)


class SkillProgress_ViewSet_Tests(TestCase):
    """Tests for the skill progress REST endpoint."""

    def setUp(self):
        self.factory = RequestFactory()
        reset_current_user()

        self.user = User.objects.create_user("skill-view-user", password="password", email="skill-view@test.com")
        self.other_user = User.objects.create_user("skill-other-user", password="password", email="skill-other@test.com")
        self.staff = User.objects.create_user(
            "skill-view-staff",
            password="password",
            email="skill-view-staff@test.com",
            is_staff=True,
            is_superuser=True,
        )

        self.skill_python = Skill.objects.create(name="Python")
        self.skill_design = Skill.objects.create(name="Design")

        SkillProgress.objects.create(account=self.user, skill=self.skill_python, level=2, progress=45)
        SkillProgress.objects.create(account=self.user, skill=self.skill_design, level=1, progress=15)
        SkillProgress.objects.create(account=self.other_user, skill=self.skill_python, level=3, progress=70)

    def test_non_staff_only_sees_own_skill_progress(self):
        """Non-staff users only see their own skill progress rows."""
        request = self.factory.get("/api/gamification/skill_progress/")
        request.user = self.user

        viewset = SkillProgressViewSet()
        viewset.request = request
        queryset = viewset.get_queryset()

        self.assertEqual(queryset.count(), 2)
        self.assertEqual(queryset.filter(account=self.other_user).count(), 0)

    def test_staff_can_see_all_skill_progress(self):
        """Staff users can inspect all skill progress rows."""
        request = self.factory.get("/api/gamification/skill_progress/")
        request.user = self.staff

        viewset = SkillProgressViewSet()
        viewset.request = request
        queryset = viewset.get_queryset()

        self.assertEqual(queryset.count(), 3)
