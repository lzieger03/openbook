import uuid

from django.contrib.auth    import get_user_model
from django.test            import TestCase
from django.urls            import reverse
from rest_framework.test    import APIClient

from openbook.content.models        import Course, CourseMaterial, LibraryGroup, Textbook, TextbookPage
from openbook.learning.models.state import LearningState

User = get_user_model()


def _u():
    return uuid.uuid4().hex[:8]


def _make_user(suffix, *, superuser=False):
    username = f"ls-{suffix}-{_u()}"
    return User.objects.create_user(
        username     = username,
        email        = f"{username}@test.com",
        password     = "password",
        is_superuser = superuser,
        is_staff     = superuser,
    )


def _make_course():
    uid   = _u()
    group = LibraryGroup.objects.create(name=f"LG-{uid}", slug=f"lg-{uid}")
    cuid  = _u()
    return Course.objects.create(name=f"Course-{cuid}", slug=f"course-{cuid}", group=group)


def _make_page():
    uid      = _u()
    group    = LibraryGroup.objects.create(name=f"PG-{uid}", slug=f"pg-{uid}")
    tuid     = _u()
    textbook = Textbook.objects.create(name=f"TB-{tuid}", slug=f"tb-{tuid}", group=group)
    puid     = _u()
    return TextbookPage.objects.create(name=f"Page-{puid}", textbook=textbook, position=0)


def _make_course_with_page():
    uid      = _u()
    group    = LibraryGroup.objects.create(name=f"LSPG-{uid}", slug=f"lspg-{uid}")
    course   = Course.objects.create(name=f"LSCourse-{uid}", slug=f"lscourse-{uid}", group=group)
    textbook = Textbook.objects.create(name=f"LSTB-{uid}", slug=f"lstb-{uid}", group=group)
    CourseMaterial.objects.create(course=course, textbook=textbook, position=0)
    page = TextbookPage.objects.create(name=f"LSPage-{uid}", textbook=textbook, position=0)
    return course, page


LIST_URL   = reverse("learning-state-list")
DETAIL_URL = lambda pk: reverse("learning-state-detail", args=[pk])
RECORD_OPENED_URL = reverse("learning-state-record-page-opened")
MARK_COMPLETED_URL = reverse("learning-state-mark-page-completed")


class LearningState_List_Tests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user1  = _make_user("u1")
        self.user2  = _make_user("u2")
        self.course = _make_course()

        LearningState.objects.create(user=self.user1, course=self.course)
        LearningState.objects.create(user=self.user2, course=self.course)

    def test_unauthenticated_returns_403(self):
        response = self.client.get(LIST_URL)
        self.assertEqual(response.status_code, 403)

    def test_user_sees_only_own_states(self):
        self.client.force_authenticate(self.user1)
        response = self.client.get(LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)

    def test_filter_by_course(self):
        course2 = _make_course()
        LearningState.objects.create(user=self.user1, course=course2)

        self.client.force_authenticate(self.user1)
        response = self.client.get(LIST_URL, {"course": str(self.course.pk)})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)


class LearningState_Create_Tests(TestCase):

    def setUp(self):
        self.client = APIClient()
        # Superuser to bypass object-permission check in ModelViewSetMixin.create()
        self.user   = _make_user("c", superuser=True)
        self.course = _make_course()

    def test_create_sets_user_from_request(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(LIST_URL, {"course": str(self.course.pk)}, format="json")
        self.assertEqual(response.status_code, 201)
        state = LearningState.objects.get(pk=response.data["id"])
        self.assertEqual(state.user, self.user)

    def test_duplicate_course_returns_400(self):
        LearningState.objects.create(user=self.user, course=self.course)
        self.client.force_authenticate(self.user)
        response = self.client.post(LIST_URL, {"course": str(self.course.pk)}, format="json")
        self.assertEqual(response.status_code, 400)


class LearningState_Update_Tests(TestCase):

    def setUp(self):
        self.client = APIClient()
        # Superuser to bypass object-permission check in ModelViewSetMixin.create()
        self.user   = _make_user("upd", superuser=True)
        self.course = _make_course()
        self.state  = LearningState.objects.create(user=self.user, course=self.course)

    def test_set_last_page(self):
        page = _make_page()
        self.client.force_authenticate(self.user)
        response = self.client.patch(
            DETAIL_URL(self.state.pk),
            {"last_page": str(page.pk)},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.state.refresh_from_db()
        self.assertEqual(self.state.last_page, page)

    def test_add_completed_page(self):
        page = _make_page()
        self.client.force_authenticate(self.user)
        response = self.client.patch(
            DETAIL_URL(self.state.pk),
            {"completed_pages": [str(page.pk)]},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(page, self.state.completed_pages.all())

    def test_other_user_cannot_update(self):
        other = _make_user("oth")
        page  = _make_page()
        self.client.force_authenticate(other)
        response = self.client.patch(
            DETAIL_URL(self.state.pk),
            {"last_page": str(page.pk)},
            format="json",
        )
        self.assertEqual(response.status_code, 404)


class LearningState_Action_Tests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user   = _make_user("act", superuser=True)
        self.course, self.page = _make_course_with_page()

    def test_record_page_opened_uses_service_validation(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(
            RECORD_OPENED_URL,
            {"course": str(self.course.pk), "page": str(self.page.pk)},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        state = LearningState.objects.get(user=self.user, course=self.course)
        self.assertEqual(state.last_page, self.page)

    def test_mark_page_completed_uses_service_validation(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(
            MARK_COMPLETED_URL,
            {"course": str(self.course.pk), "page": str(self.page.pk)},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        state = LearningState.objects.get(user=self.user, course=self.course)
        self.assertIn(self.page, state.completed_pages.all())

    def test_record_page_opened_rejects_page_outside_course(self):
        outside_page = _make_page()
        self.client.force_authenticate(self.user)
        response = self.client.post(
            RECORD_OPENED_URL,
            {"course": str(self.course.pk), "page": str(outside_page.pk)},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
