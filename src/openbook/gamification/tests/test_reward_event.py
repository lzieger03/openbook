# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>

from django.test               import TestCase
from django.urls               import reverse

from openbook.auth.models.user import User
from openbook.auth.utils       import permission_for_perm_string
from openbook.test             import ModelViewSetTestMixin
from ..models                  import AccountPoints
from ..models                  import Reward
from ..models                  import RewardEvent

class RewardEvent_ViewSet_Tests(ModelViewSetTestMixin, TestCase):
    """Test the RewardEventViewSet REST API including trigger action."""

    base_name         = "reward_event"
    model             = RewardEvent
    search_string     = "quiz_complete"
    search_count      = 1
    sort_field        = "points_delta"
    expandable_fields = ["reward", "account"]

    operations = {
        "list": {
            "username": "admin",
            "password": "password",
        },
        "retrieve": {
            "username": "admin",
            "password": "password",
        },
        "create":         {"supported": False},
        "update":         {"supported": False},
        "partial_update": {"supported": False},
        "destroy":        {"supported": False},
    }

    def setUp(self):
        super().setUp()

        self.user1 = User.objects.create_user("user1", password="password", email="user1@test.com")
        self.user2 = User.objects.create_user("user2", password="password", email="user2@test.com")
        self.admin = User.objects.create_user(
            "admin",
            password     = "password",
            email        = "admin@test.com",
            is_staff     = True,
            is_superuser = True,
        )

        self.reward_quiz = Reward.objects.create(
            reward_type = "quiz_complete",
            value       = 50,
            description = "Quiz completed",
        )

        self.reward_question = Reward.objects.create(
            reward_type = "question_correct",
            value       = 10,
            description = "Question answered correctly",
        )

        self.event_user1 = RewardEvent.objects.create(
            account      = self.user1,
            reward       = self.reward_quiz,
            event_type   = "quiz_complete",
            points_delta = 50,
            context      = {"quiz_id": "quiz-1"},
        )

        self.event_user2 = RewardEvent.objects.create(
            account      = self.user2,
            reward       = self.reward_question,
            event_type   = "question_correct",
            points_delta = 10,
            context      = {"question_id": "q-1"},
        )

    def pk_found(self):
        return self.event_user1.id

    def test_trigger_creates_reward_event_and_updates_points(self):
        """Trigger endpoint creates a RewardEvent and increments AccountPoints."""
        self.login("user1", "password")

        old_points = AccountPoints.objects.get(account=self.user1).point_total

        response = self.client.post(
            reverse("reward_event-trigger"),
            {
                "reward": str(self.reward_question.id),
                "context": {"question_id": "q-2"},
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["reward_event"]["event_type"], "question_correct")
        self.assertEqual(response.data["reward_event"]["points_delta"], 10)
        self.assertEqual(response.data["point_total"], old_points + 10)

    def test_trigger_uses_explicit_event_type(self):
        """Trigger endpoint uses provided event_type when explicitly set."""
        self.login("user1", "password")

        response = self.client.post(
            reverse("reward_event-trigger"),
            {
                "reward": str(self.reward_question.id),
                "event_type": "bonus_event",
                "context": {"reason": "manual bonus"},
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["reward_event"]["event_type"], "bonus_event")

    def test_trigger_requires_authentication(self):
        """Trigger endpoint rejects unauthenticated requests."""
        self.logout()

        response = self.client.post(
            reverse("reward_event-trigger"),
            {"reward": str(self.reward_question.id)},
            format="json",
        )

        self.assertIn(response.status_code, [401, 403])

    def test_non_staff_cannot_trigger_for_other_account(self):
        """Non-staff users cannot trigger rewards for another account."""
        self.login("user1", "password")

        response = self.client.post(
            reverse("reward_event-trigger"),
            {
                "account": self.user2.username,
                "reward": str(self.reward_question.id),
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("account", response.data)

    def test_staff_can_trigger_for_other_account(self):
        """Staff users can trigger rewards for another account."""
        self.login("admin", "password")

        old_points = AccountPoints.objects.get(account=self.user2).point_total

        response = self.client.post(
            reverse("reward_event-trigger"),
            {
                "account": self.user2.username,
                "reward": str(self.reward_question.id),
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)

        new_points = AccountPoints.objects.get(account=self.user2).point_total
        self.assertEqual(new_points, old_points + 10)

    def test_non_staff_list_only_contains_own_events(self):
        """Non-staff users can only list their own reward events."""
        self.user1.user_permissions.add(permission_for_perm_string("openbook_gamification.view_rewardevent"))
        self.login("user1", "password")

        response = self.client.get(reverse("reward_event-list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["account"], "user1")
