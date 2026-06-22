# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>

from django.contrib.auth                   import get_user_model
from django.test                           import TestCase

from openbook.auth.middleware.current_user import reset_current_user
from openbook.auth.models.role             import Role
from openbook.auth.models.role_assignment  import RoleAssignment
from openbook.content.models.course        import Course
from openbook.content.models.library_group import LibraryGroup

from ..models            import AccountProgress
from ..models            import CourseProgress
from ..models            import Reward
from ..models            import RewardEventLog

User = get_user_model()

class Gamification_Signal_Tests(TestCase):
    """Tests for gamification signal handlers."""

    def test_account_points_created_for_new_user(self):
        """A new user automatically gets an AccountProgress row with 0 points."""
        user = User.objects.create_user(
            username = "signal-user-1",
            email    = "signal-user-1@test.com",
            password = "password",
        )

        self.assertTrue(AccountProgress.objects.filter(account=user).exists())
        self.assertEqual(AccountProgress.objects.get(account=user).point_total, 0)

    def test_reward_event_updates_point_total(self):
        """Creating a RewardEventLog entry increments the current account point total."""
        user = User.objects.create_user(
            username = "signal-user-2",
            email    = "signal-user-2@test.com",
            password = "password",
        )

        reward = Reward.objects.create(
            reward_type = "question_correct",
            value       = 10,
        )

        RewardEventLog.objects.create(
            account      = user,
            reward       = reward,
            event_type   = "question_correct",
            points_delta = 10,
            context      = {"question_id": "q-1"},
        )

        account_points = AccountProgress.objects.get(account=user)
        self.assertEqual(account_points.point_total, 10)

    def test_reward_event_recreates_missing_account_points(self):
        """If AccountProgress was deleted, RewardEventLog creation recreates it and applies delta."""
        user = User.objects.create_user(
            username = "signal-user-3",
            email    = "signal-user-3@test.com",
            password = "password",
        )

        reward = Reward.objects.create(
            reward_type = "quiz_complete",
            value       = 50,
        )

        AccountProgress.objects.filter(account=user).delete()
        self.assertFalse(AccountProgress.objects.filter(account=user).exists())

        RewardEventLog.objects.create(
            account      = user,
            reward       = reward,
            event_type   = "quiz_complete",
            points_delta = 50,
            context      = {"quiz_id": "quiz-1"},
        )

        account_points = AccountProgress.objects.get(account=user)
        self.assertEqual(account_points.point_total, 50)


class Gamification_Enrollment_Signal_Tests(TestCase):
    """Tests for the CourseProgress signals tied to course enrollment."""

    def setUp(self):
        super().setUp()
        reset_current_user()

        self.user          = User.objects.create_user(
            username = "enroll-user",
            email    = "enroll-user@test.com",
            password = "password",
        )
        self.library_group = LibraryGroup.objects.create(name="Test", slug="test")
        self.course        = Course.objects.create(name="Test Course", slug="test-course", group=self.library_group)

        self.role_student  = Role.from_obj(self.course, name="Student", slug="student", priority=0)
        self.role_teacher  = Role.from_obj(self.course, name="Teacher", slug="teacher", priority=2)
        self.role_student.save()
        self.role_teacher.save()

    def _enroll(self, role):
        assignment = RoleAssignment.from_obj(self.course, role=role, user=self.user)
        assignment.save()
        return assignment

    def test_enrolling_student_creates_course_progress(self):
        """Enrolling a user as a student creates a zeroed CourseProgress row."""
        self._enroll(self.role_student)

        progress = CourseProgress.objects.get(account=self.user, course=self.course)
        self.assertEqual(progress.course_points, 0)
        self.assertEqual(progress.course_level, 1)

    def test_enrolling_non_student_role_does_not_create_progress(self):
        """A teacher assignment must not create a learner CourseProgress row."""
        self._enroll(self.role_teacher)

        self.assertFalse(CourseProgress.objects.filter(account=self.user, course=self.course).exists())

    def test_enrolling_twice_is_idempotent(self):
        """Re-saving a student assignment must not raise or duplicate progress rows."""
        assignment = self._enroll(self.role_student)
        assignment.save()

        self.assertEqual(
            CourseProgress.objects.filter(account=self.user, course=self.course).count(),
            1,
        )

    def test_unenrolling_removes_empty_progress(self):
        """Withdrawing a student who earned no points removes the placeholder row."""
        assignment = self._enroll(self.role_student)
        assignment.delete()

        self.assertFalse(CourseProgress.objects.filter(account=self.user, course=self.course).exists())

    def test_unenrolling_keeps_progress_with_points(self):
        """Withdrawing a student who earned points keeps their progress and history."""
        assignment = self._enroll(self.role_student)

        progress = CourseProgress.objects.get(account=self.user, course=self.course)
        progress.course_points = 25
        progress.save(update_fields=["course_points"])

        assignment.delete()

        self.assertTrue(CourseProgress.objects.filter(account=self.user, course=self.course).exists())
