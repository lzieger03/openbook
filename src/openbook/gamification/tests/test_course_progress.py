# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>

from django.db import IntegrityError
from django.test import TestCase

from openbook.auth.models.user import User
from openbook.auth.middleware.current_user import reset_current_user
from openbook.content.models.course import Course
from openbook.content.models.library_group import LibraryGroup

from ..models import CourseProgress


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
        self.course = Course.objects.create(group=self.group, name="Course 1", slug="course-1")

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