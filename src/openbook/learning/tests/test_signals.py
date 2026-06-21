from django.contrib.auth import get_user_model
from django.test         import TestCase

from openbook.content.models             import Course, CourseMaterial, LibraryGroup, Textbook, TextbookPage
from openbook.gamification.models        import AccountActivityDay, Reward, RewardEventLog
from openbook.learning.models.state      import LearningState

User = get_user_model()


def _make_user(username):
    return User.objects.create_user(
        username = username,
        email    = f"{username}@test.com",
        password = "password",
    )


def _make_course_with_pages(page_count=2):
    """Return (course, [pages]) with a textbook linked via CourseMaterial."""
    group    = LibraryGroup.objects.create(name="Test Group")
    textbook = Textbook.objects.create(name="Test Textbook", group=group)
    course   = Course.objects.create(name="Test Course", group=group)
    CourseMaterial.objects.create(course=course, textbook=textbook, position=1)
    pages = [
        TextbookPage.objects.create(name=f"Page {i}", textbook=textbook, position=i)
        for i in range(page_count)
    ]
    return course, pages


class LearningSignal_ContentViewed_Tests(TestCase):

    def test_saving_learning_state_records_streak_activity(self):
        """Saving a LearningState should create an AccountActivityDay entry."""
        user   = _make_user("streak-user-1")
        course, _ = _make_course_with_pages()

        LearningState.objects.create(user=user, course=course)

        self.assertTrue(AccountActivityDay.objects.filter(account=user).exists())

    def test_multiple_saves_same_day_count_as_one_activity(self):
        """Multiple saves on the same day must not create duplicate ActivityDay rows."""
        user   = _make_user("streak-user-2")
        course, pages = _make_course_with_pages()

        state = LearningState.objects.create(user=user, course=course)
        state.last_page = pages[0]
        state.save()

        self.assertEqual(AccountActivityDay.objects.filter(account=user).count(), 1)


class LearningSignal_CourseCompletion_Tests(TestCase):

    def setUp(self):
        self.reward = Reward.objects.create(
            reward_type = "COURSE_COMPLETION",
            value       = 200,
        )

    def test_completing_all_pages_awards_points(self):
        """Adding all course pages to completed_pages must create a RewardEventLog."""
        user   = _make_user("complete-user-1")
        course, pages = _make_course_with_pages(page_count=2)
        state  = LearningState.objects.create(user=user, course=course)

        state.completed_pages.add(*pages)

        log = RewardEventLog.objects.filter(account=user, event_type="COURSE_COMPLETION")
        self.assertEqual(log.count(), 1)
        self.assertEqual(log.first().points_delta, 200)

    def test_partial_completion_does_not_award_points(self):
        """Adding only some pages must not trigger the COURSE_COMPLETION reward."""
        user   = _make_user("complete-user-2")
        course, pages = _make_course_with_pages(page_count=2)
        state  = LearningState.objects.create(user=user, course=course)

        state.completed_pages.add(pages[0])

        self.assertFalse(
            RewardEventLog.objects.filter(account=user, event_type="COURSE_COMPLETION").exists()
        )

    def test_completion_not_awarded_twice(self):
        """Completing the course a second time must not create a second reward entry."""
        user   = _make_user("complete-user-3")
        course, pages = _make_course_with_pages(page_count=2)
        state  = LearningState.objects.create(user=user, course=course)

        state.completed_pages.add(*pages)
        state.completed_pages.remove(pages[0])
        state.completed_pages.add(pages[0])

        self.assertEqual(
            RewardEventLog.objects.filter(account=user, event_type="COURSE_COMPLETION").count(),
            1,
        )

    def test_completion_without_reward_defined_does_not_crash(self):
        """If no COURSE_COMPLETION reward exists the signal must not raise."""
        self.reward.delete()

        user   = _make_user("complete-user-4")
        course, pages = _make_course_with_pages(page_count=1)
        state  = LearningState.objects.create(user=user, course=course)

        # Should complete without exception
        state.completed_pages.add(*pages)

        self.assertFalse(
            RewardEventLog.objects.filter(account=user, event_type="COURSE_COMPLETION").exists()
        )
