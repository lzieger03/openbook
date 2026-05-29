# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>

from django.db import IntegrityError
from django.test import RequestFactory
from django.test import TestCase

from openbook.auth.models.user import User
from openbook.auth.middleware.current_user import reset_current_user
from openbook.content.models.course import Course
from openbook.content.models.library_group import LibraryGroup

from ..models import CourseProgress
from ..viewsets.course_progress import CourseProgressViewSet


class CourseProgress_Tests(TestCase):
    """Tests for the course progress model."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="course-user",
            email="course-user@test.com",
            password="password",
        )
        reset_current_user()
        self.group = LibraryGroup.objects.create(name="Main Library", slug="main-library")
        self.course = Course.objects.create(group=self.group, name="Course 1", slug="course-1", position=1)

    def test_course_progress_defaults(self):
        """New course progress rows start at zero points, level 1 and zero progress."""
        progress = CourseProgress.objects.create(account=self.user, course=self.course)

        self.assertEqual(progress.course_points, 0)
        self.assertEqual(progress.course_level, 1)
        self.assertEqual(progress.course_progress, 0)

    def test_course_progress_is_unique_per_account_and_course(self):
        """An account can only have one progress row per course."""
        CourseProgress.objects.create(account=self.user, course=self.course)

        with self.assertRaises(IntegrityError):
            CourseProgress.objects.create(account=self.user, course=self.course)


class CourseProgress_ViewSet_Tests(TestCase):
    """Tests for the course progress REST endpoint."""

    def setUp(self):
        self.factory = RequestFactory()
        reset_current_user()

        self.user = User.objects.create_user("course-view-user", password="password", email="course-view@test.com")
        self.other_user = User.objects.create_user("other-view-user", password="password", email="other-view@test.com")
        self.staff = User.objects.create_user(
            "course-view-staff",
            password="password",
            email="course-view-staff@test.com",
            is_staff=True,
            is_superuser=True,
        )

        self.group = LibraryGroup.objects.create(name="Main Library", slug="main-library")
        self.course1 = Course.objects.create(group=self.group, name="Course 1", slug="course-1", position=1)
        self.course2 = Course.objects.create(group=self.group, name="Course 2", slug="course-2", position=2)

        self.progress1 = CourseProgress.objects.create(
            account=self.user,
            course=self.course1,
            course_points=35,
            course_level=2,
            course_progress=35,
        )
        self.progress2 = CourseProgress.objects.create(
            account=self.user,
            course=self.course2,
            course_points=80,
            course_level=4,
            course_progress=80,
        )
        CourseProgress.objects.create(
            account=self.other_user,
            course=self.course1,
            course_points=10,
            course_level=1,
            course_progress=10,
        )

    def test_non_staff_only_sees_own_course_progress(self):
        """Non-staff users only see their own course progress rows."""
        request = self.factory.get("/api/gamification/course_progress/")
        request.user = self.user

        viewset = CourseProgressViewSet()
        viewset.request = request
        queryset = viewset.get_queryset()

        self.assertEqual(queryset.count(), 2)

    def test_staff_can_see_other_users_course_progress(self):
        """Staff users can inspect another user's course progress rows."""
        request = self.factory.get("/api/gamification/course_progress/", {"account": self.other_user.username})
        request.user = self.staff

        viewset = CourseProgressViewSet()
        viewset.request = request
        queryset = viewset.get_queryset()

        self.assertEqual(queryset.count(), 3)
        self.assertEqual(queryset.filter(account=self.other_user).count(), 1)