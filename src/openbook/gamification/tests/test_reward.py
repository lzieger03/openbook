# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>

from django.test      import TestCase

from openbook.test    import ModelViewSetTestMixin
from ..models         import Reward

class Reward_ViewSet_Tests(ModelViewSetTestMixin, TestCase):
    """Test the RewardViewSet REST API."""

    base_name     = "reward"
    model         = Reward
    search_string = "question"
    search_count  = 1
    sort_field    = "value"

    operations = {
        "create":         {"supported": False},
        "update":         {"supported": False},
        "partial_update": {"supported": False},
        "destroy":        {"supported": False},
    }

    def setUp(self):
        super().setUp()

        self.reward_quiz = Reward.objects.create(
            reward_type = "quiz_complete",
            value       = 50,
            description = "Quiz completed",
        )

        Reward.objects.create(
            reward_type = "question_correct",
            value       = 10,
            description = "Question answered correctly",
        )

        Reward.objects.create(
            reward_type = "first_login",
            value       = 5,
            description = "First login reward",
        )

    def pk_found(self):
        return self.reward_quiz.id
