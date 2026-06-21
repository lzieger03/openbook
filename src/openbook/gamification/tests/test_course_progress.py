# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>

from decimal import Decimal

from django.db import IntegrityError
from django.test import RequestFactory
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate

from openbook.auth.models.user import User
from openbook.auth.middleware.current_user import reset_current_user
from openbook.content.models.course import Course
from openbook.content.models.library_group import LibraryGroup

from ..constants import CourseEventType
from ..models import AccountProgress, CourseProgress, LevelThreshold, RewardEventLog
from ..services.course import award_course_points
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


class AwardCoursePoints_Tests(TestCase):
    """Tests for the award_course_points service."""

    def setUp(self):
        reset_current_user()

        self.user = User.objects.create_user(
            username="award-user",
            email="award-user@test.com",
            password="password",
        )
        reset_current_user()

        self.group = LibraryGroup.objects.create(name="Main Library", slug="main-library")
        self.course = Course.objects.create(group=self.group, name="Course 1", slug="course-1")

        # Same thresholds the dummy-data command seeds: level 1 at 0, level 2 at 100.
        for level, min_points in [(1, 0), (2, 100), (3, 300)]:
            LevelThreshold.objects.create(level=level, min_points=min_points)

    def test_awarding_points_creates_and_increments_course_progress(self):
        """The first award creates the row; further awards accumulate points."""
        state = award_course_points(self.user.id, self.course.id, 40)

        self.assertEqual(state["course_points"], 40)
        self.assertEqual(state["course_level"], 1)

        state = award_course_points(self.user.id, self.course.id, 30)
        self.assertEqual(state["course_points"], 70)

        progress = CourseProgress.objects.get(account=self.user, course=self.course)
        self.assertEqual(progress.course_points, 70)

    def test_course_level_and_progress_bar_advance_with_points(self):
        """Course level follows the thresholds and the bar tracks progress to the next level."""
        # 50 points: still level 1, halfway to the 100-point level-2 threshold.
        award_course_points(self.user.id, self.course.id, 50)
        progress = CourseProgress.objects.get(account=self.user, course=self.course)
        self.assertEqual(progress.course_level, 1)
        self.assertEqual(progress.course_progress, Decimal("50.00"))

        # 100 points total: reaches level 2, bar resets towards the 300-point level 3.
        award_course_points(self.user.id, self.course.id, 50)
        progress.refresh_from_db()
        self.assertEqual(progress.course_level, 2)
        self.assertEqual(progress.course_progress, Decimal("0.00"))

    def test_course_points_raise_global_account_progress_and_level(self):
        """Points earned in a course also move the overall point total and level."""
        award_course_points(self.user.id, self.course.id, 120)

        account_progress = AccountProgress.objects.get(account=self.user)
        self.assertEqual(account_progress.point_total, 120)
        self.assertEqual(account_progress.level, 2)

    def test_award_logs_a_reward_event(self):
        """Each award writes a reward event carrying the course context."""
        award_course_points(self.user.id, self.course.id, 25)

        event = RewardEventLog.objects.get(
            account=self.user,
            event_type=CourseEventType.COURSE_POINTS_AWARDED,
        )
        self.assertEqual(event.points_delta, 25)
        self.assertEqual(event.context["course_id"], str(self.course.id))

    def test_course_points_never_drop_below_zero(self):
        """A correcting negative award cannot push the course point total negative."""
        award_course_points(self.user.id, self.course.id, 30)
        state = award_course_points(self.user.id, self.course.id, -100)

        self.assertEqual(state["course_points"], 0)

    def test_zero_points_are_rejected(self):
        """Awarding zero points is a programming error and raises."""
        with self.assertRaises(ValueError):
            award_course_points(self.user.id, self.course.id, 0)


class AwardCoursePoints_Endpoint_Tests(TestCase):
    """Tests for the course_progress 'award' REST action."""

    def setUp(self):
        reset_current_user()

        self.factory = APIRequestFactory()
        self.user = User.objects.create_user("award-ep-user", password="password", email="award-ep@test.com")
        self.staff = User.objects.create_user(
            "award-ep-staff", password="password", email="award-ep-staff@test.com",
            is_staff=True, is_superuser=True,
        )
        reset_current_user()

        self.group = LibraryGroup.objects.create(name="Main Library", slug="main-library")
        self.course = Course.objects.create(group=self.group, name="Course 1", slug="course-1")

        for level, min_points in [(1, 0), (2, 100)]:
            LevelThreshold.objects.create(level=level, min_points=min_points)

        self.view = CourseProgressViewSet.as_view({"post": "award"})

    def _award(self, user, data):
        request = self.factory.post("/api/gamification/course_progress/award/", data, format="json")
        force_authenticate(request, user=user)
        return self.view(request)

    def test_award_endpoint_updates_course_and_global_progress(self):
        """Posting to /award/ advances both the course bar and the global point total."""
        response = self._award(self.user, {"course": str(self.course.id), "points": 60})

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["course_points"], 60)
        self.assertEqual(response.data["point_total"], 60)

        progress = CourseProgress.objects.get(account=self.user, course=self.course)
        self.assertEqual(progress.course_points, 60)

    def test_non_staff_cannot_award_to_other_account(self):
        """A non-staff user may not award course points to someone else."""
        response = self._award(self.user, {
            "account": self.staff.username,
            "course": str(self.course.id),
            "points": 10,
        })

        self.assertEqual(response.status_code, 400)
        self.assertFalse(CourseProgress.objects.filter(account=self.staff).exists())

    def test_zero_points_are_rejected_by_endpoint(self):
        """Awarding zero points returns a validation error."""
        response = self._award(self.user, {"course": str(self.course.id), "points": 0})

        self.assertEqual(response.status_code, 400)


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
        self.course1 = Course.objects.create(group=self.group, name="Course 1", slug="course-1")
        self.course2 = Course.objects.create(group=self.group, name="Course 2", slug="course-2")

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
