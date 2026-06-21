from django.contrib.auth import get_user_model
from django.test         import TestCase

from openbook.content.models             import Course, CourseMaterial, LibraryGroup, Textbook, TextbookPage
from openbook.gamification.models        import AccountActivityDay
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
