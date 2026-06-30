import uuid

from django.contrib.auth    import get_user_model
from django.test            import TestCase
from django.urls            import reverse
from rest_framework.test    import APIClient

from openbook.content.models              import Course, CourseMaterial, LibraryGroup, Textbook, TextbookPage
from openbook.learning.models.quiz_result import QuizResult

User = get_user_model()


def _u():
    return uuid.uuid4().hex[:8]


def _make_user(suffix, *, superuser=False):
    username = f"qr-{suffix}-{_u()}"
    return User.objects.create_user(
        username     = username,
        email        = f"{username}@test.com",
        password     = "password",
        is_superuser = superuser,
        is_staff     = superuser,
    )


def _make_page():
    uid      = _u()
    group    = LibraryGroup.objects.create(name=f"QRG-{uid}", slug=f"qrg-{uid}")
    tuid     = _u()
    textbook = Textbook.objects.create(name=f"QRTB-{tuid}", slug=f"qrtb-{tuid}", group=group)
    puid     = _u()
    return TextbookPage.objects.create(name=f"QRP-{puid}", textbook=textbook, position=0)


def _make_course_with_page():
    uid      = _u()
    group    = LibraryGroup.objects.create(name=f"QRCG-{uid}", slug=f"qrcg-{uid}")
    course   = Course.objects.create(name=f"QRC-{uid}", slug=f"qrc-{uid}", group=group)
    textbook = Textbook.objects.create(name=f"QRTBC-{uid}", slug=f"qrtbc-{uid}", group=group)
    CourseMaterial.objects.create(course=course, textbook=textbook, position=0)
    page = TextbookPage.objects.create(name=f"QRCP-{uid}", textbook=textbook, position=0)
    return course, textbook, page


LIST_URL   = reverse("quiz-result-list")
DETAIL_URL = lambda pk: reverse("quiz-result-detail", args=[pk])
ACTIVITY_URL = reverse("quiz-result-record-activity")


class QuizResult_List_Tests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user1  = _make_user("u1")
        self.user2  = _make_user("u2")
        self.page   = _make_page()

        QuizResult.objects.create(user=self.user1, page=self.page, score=0.8)
        QuizResult.objects.create(user=self.user2, page=self.page, score=0.5)

    def test_unauthenticated_returns_403(self):
        response = self.client.get(LIST_URL)
        self.assertEqual(response.status_code, 403)

    def test_user_sees_only_own_results(self):
        self.client.force_authenticate(self.user1)
        response = self.client.get(LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)

    def test_filter_by_page(self):
        page2 = _make_page()
        QuizResult.objects.create(user=self.user1, page=page2, score=1.0)

        self.client.force_authenticate(self.user1)
        response = self.client.get(LIST_URL, {"page": str(self.page.pk)})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)

    def test_filter_by_activity_type(self):
        course, _textbook, _page = _make_course_with_page()
        QuizResult.objects.create(
            user=self.user1,
            course=course,
            activity_type=QuizResult.ActivityTypeChoices.HANGMAN,
            score=1.0,
        )

        self.client.force_authenticate(self.user1)
        response = self.client.get(
            LIST_URL,
            {"activity_type": QuizResult.ActivityTypeChoices.HANGMAN},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)


class QuizResult_Create_Tests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user   = _make_user("c", superuser=True)
        self.page   = _make_page()

    def test_create_sets_user_from_request(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(
            LIST_URL,
            {"page": str(self.page.pk), "score": 0.9},
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        result = QuizResult.objects.get(pk=response.data["id"])
        self.assertEqual(result.user, self.user)
        self.assertEqual(result.activity_type, QuizResult.ActivityTypeChoices.QUIZ)

    def test_duplicate_page_returns_400(self):
        QuizResult.objects.create(user=self.user, page=self.page, score=0.5)
        self.client.force_authenticate(self.user)
        response = self.client.post(
            LIST_URL,
            {"page": str(self.page.pk), "score": 0.8},
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_record_activity_upserts_game_result(self):
        course, _textbook, _page = _make_course_with_page()
        self.client.force_authenticate(self.user)

        first_response = self.client.post(
            ACTIVITY_URL,
            {
                "course": str(course.pk),
                "activity_type": QuizResult.ActivityTypeChoices.HANGMAN,
                "score": 0.5,
                "metadata": {"wrong_guesses": 3},
            },
            format="json",
        )
        second_response = self.client.post(
            ACTIVITY_URL,
            {
                "course": str(course.pk),
                "activity_type": QuizResult.ActivityTypeChoices.HANGMAN,
                "score": 1.0,
                "metadata": {"wrong_guesses": 0},
            },
            format="json",
        )

        self.assertEqual(first_response.status_code, 200)
        self.assertEqual(second_response.status_code, 200)
        self.assertEqual(first_response.data["id"], second_response.data["id"])

        result = QuizResult.objects.get(pk=second_response.data["id"])
        self.assertEqual(result.score, 1.0)
        self.assertEqual(result.attempts, 2)
        self.assertEqual(result.metadata["wrong_guesses"], 0)


class QuizResult_Update_Tests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user   = _make_user("upd", superuser=True)
        self.page   = _make_page()
        self.result = QuizResult.objects.create(user=self.user, page=self.page, score=0.5)

    def test_update_score_and_attempts(self):
        self.client.force_authenticate(self.user)
        response = self.client.patch(
            DETAIL_URL(self.result.pk),
            {"score": 1.0, "attempts": 2},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.result.refresh_from_db()
        self.assertEqual(self.result.score, 1.0)
        self.assertEqual(self.result.attempts, 2)

    def test_other_user_cannot_update(self):
        other = _make_user("oth")
        self.client.force_authenticate(other)
        response = self.client.patch(
            DETAIL_URL(self.result.pk),
            {"score": 0.0},
            format="json",
        )
        self.assertEqual(response.status_code, 404)
