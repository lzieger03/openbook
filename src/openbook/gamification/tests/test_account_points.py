# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>

from django.test              import TestCase
from django.urls              import reverse

from openbook.auth.utils      import permission_for_perm_string
from openbook.test            import ModelViewSetTestMixin
from openbook.auth.models.user import User
from ..models                 import AccountPoints

class AccountPoints_ViewSet_Tests(ModelViewSetTestMixin, TestCase):
    """Test the AccountPointsViewSet REST API."""

    base_name         = "account_points"
    model             = AccountPoints
    search_string     = "user2"
    search_count      = 1
    sort_field        = "point_total"
    expandable_fields = ["account"]

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
            password    = "password",
            email       = "admin@test.com",
            is_staff    = True,
            is_superuser= True,
        )

        self.ap_user1 = AccountPoints.objects.get(account=self.user1)
        self.ap_user2 = AccountPoints.objects.get(account=self.user2)
        self.ap_admin = AccountPoints.objects.get(account=self.admin)

        self.ap_user1.point_total = 30
        self.ap_user2.point_total = 10
        self.ap_admin.point_total = 99

        self.ap_user1.save()
        self.ap_user2.save()
        self.ap_admin.save()

    def pk_found(self):
        return self.ap_user1.id

    def test_me_returns_current_users_total(self):
        """The /me endpoint returns the currently authenticated user's point total."""
        self.login("user1", "password")

        response = self.client.get(reverse("account_points-me"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["point_total"], 30)

    def test_me_recreates_missing_account_points(self):
        """The /me endpoint recreates missing AccountPoints rows with 0 points."""
        self.login("user1", "password")
        AccountPoints.objects.filter(account=self.user1).delete()

        response = self.client.get(reverse("account_points-me"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["point_total"], 0)
        self.assertTrue(AccountPoints.objects.filter(account=self.user1).exists())

    def test_non_staff_list_only_contains_own_points(self):
        """Non-staff users can only list their own AccountPoints row."""
        self.user1.user_permissions.add(permission_for_perm_string("openbook_gamification.view_accountpoints"))
        self.login("user1", "password")

        response = self.client.get(reverse("account_points-list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["account"], "user1")

    def test_non_staff_cannot_retrieve_other_account_points(self):
        """Non-staff users cannot retrieve another user's AccountPoints row."""
        self.user1.user_permissions.add(permission_for_perm_string("openbook_gamification.view_accountpoints"))
        self.login("user1", "password")

        response = self.client.get(reverse("account_points-detail", args=[str(self.ap_user2.id)]))

        self.assertEqual(response.status_code, 404)
