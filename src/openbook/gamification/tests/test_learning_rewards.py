# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>

from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from openbook.auth.models.user import User
from openbook.auth.middleware.current_user import reset_current_user
from openbook.content.models.course import Course
from openbook.content.models.library_group import LibraryGroup

from ..constants import CourseEventType
from ..models import AccountProgress, CourseProgress, LevelThreshold, RewardEventLog, Skill, SkillProgress
from ..services.learning_rewards import (
    CHAT_QUESTION_DAILY_LIMIT,
    CHAT_QUESTION_POINTS,
    QUIZ_MAX_COURSE_POINTS,
    QUIZ_SKILL_PROGRESS_PER_POINT,
    award_chat_question_reward,
    award_quiz_rewards,
)


class AwardQuizRewards_Tests(TestCase):
    """Tests for rewarding quiz attempts."""

    def setUp(self):
        reset_current_user()
        self.user = User.objects.create_user(
            username="quiz-user", email="quiz-user@test.com", password="password",
        )
        reset_current_user()

        self.group = LibraryGroup.objects.create(name="Lib", slug="lib")
        self.course = Course.objects.create(group=self.group, name="Course", slug="course")
        self.skill = Skill.objects.create(name="HTML")
        self.other_skill = Skill.objects.create(name="CSS")

        for level, min_points in [(1, 0), (2, 100), (3, 300)]:
            LevelThreshold.objects.create(level=level, min_points=min_points)

        # A fake page id is enough: the service only stores it as context.
        self.page_id = "11111111-1111-1111-1111-111111111111"

    def test_quiz_points_scale_with_score(self):
        """An 80% score is worth 80% of the maximum quiz points."""
        state = award_quiz_rewards(
            self.user.id, self.course.id, self.page_id, score=0.8, skill_ids=[self.skill.id],
        )

        expected = round(0.8 * QUIZ_MAX_COURSE_POINTS)
        self.assertEqual(state["points_awarded"], expected)
        self.assertEqual(state["course_progress"]["course_points"], expected)

    def test_quiz_points_flow_into_global_account_total(self):
        """Quiz points raise the overall account point total via the reward event."""
        award_quiz_rewards(self.user.id, self.course.id, self.page_id, score=1.0)

        account = AccountProgress.objects.get(account=self.user)
        self.assertEqual(account.point_total, QUIZ_MAX_COURSE_POINTS)

    def test_only_improvement_over_best_score_is_rewarded(self):
        """Re-taking a quiz only pays out the improvement over the best score."""
        first = award_quiz_rewards(self.user.id, self.course.id, self.page_id, score=0.6)
        self.assertEqual(first["points_awarded"], round(0.6 * QUIZ_MAX_COURSE_POINTS))

        # A better score pays only the difference.
        second = award_quiz_rewards(self.user.id, self.course.id, self.page_id, score=0.9)
        self.assertEqual(
            second["points_awarded"],
            round(0.9 * QUIZ_MAX_COURSE_POINTS) - round(0.6 * QUIZ_MAX_COURSE_POINTS),
        )

        progress = CourseProgress.objects.get(account=self.user, course=self.course)
        self.assertEqual(progress.course_points, round(0.9 * QUIZ_MAX_COURSE_POINTS))

    def test_worse_or_equal_retake_awards_nothing(self):
        """A repeated attempt that does not beat the best score earns no points."""
        award_quiz_rewards(self.user.id, self.course.id, self.page_id, score=0.9)
        state = award_quiz_rewards(self.user.id, self.course.id, self.page_id, score=0.5)

        self.assertEqual(state["points_awarded"], 0)
        self.assertEqual(
            CourseProgress.objects.get(account=self.user, course=self.course).course_points,
            round(0.9 * QUIZ_MAX_COURSE_POINTS),
        )

    def test_quiz_advances_only_the_pages_skills(self):
        """Only the skills passed in (the page's skills) gain progress."""
        award_quiz_rewards(
            self.user.id, self.course.id, self.page_id, score=1.0, skill_ids=[self.skill.id],
        )

        advanced = SkillProgress.objects.get(account=self.user, skill=self.skill)
        expected = QUIZ_MAX_COURSE_POINTS * QUIZ_SKILL_PROGRESS_PER_POINT
        self.assertEqual(float(advanced.progress), expected)

        # The unrelated skill must stay untouched.
        self.assertFalse(
            SkillProgress.objects.filter(account=self.user, skill=self.other_skill).exists()
        )

    def test_zero_score_awards_nothing(self):
        """A score of zero (all wrong) earns no points and creates no events."""
        state = award_quiz_rewards(self.user.id, self.course.id, self.page_id, score=0.0)

        self.assertEqual(state["points_awarded"], 0)
        self.assertFalse(
            RewardEventLog.objects.filter(
                account=self.user, event_type=CourseEventType.QUIZ_POINTS_AWARDED,
            ).exists()
        )


class AwardChatQuestionReward_Tests(TestCase):
    """Tests for rewarding chat questions."""

    def setUp(self):
        reset_current_user()
        self.user = User.objects.create_user(
            username="chat-user", email="chat-user@test.com", password="password",
        )
        reset_current_user()

        self.group = LibraryGroup.objects.create(name="Lib", slug="lib")
        self.course = Course.objects.create(group=self.group, name="Course", slug="course")

        for level, min_points in [(1, 0), (2, 100)]:
            LevelThreshold.objects.create(level=level, min_points=min_points)

    def test_chat_question_awards_points(self):
        """Asking a question grants the flat chat reward."""
        state = award_chat_question_reward(self.user.id, self.course.id)

        self.assertEqual(state["points_awarded"], CHAT_QUESTION_POINTS)
        self.assertEqual(
            CourseProgress.objects.get(account=self.user, course=self.course).course_points,
            CHAT_QUESTION_POINTS,
        )

    def test_chat_reward_is_capped_per_day(self):
        """Once the daily limit is hit, further questions earn nothing."""
        for _ in range(CHAT_QUESTION_DAILY_LIMIT):
            award_chat_question_reward(self.user.id, self.course.id)

        state = award_chat_question_reward(self.user.id, self.course.id)
        self.assertEqual(state["points_awarded"], 0)

        progress = CourseProgress.objects.get(account=self.user, course=self.course)
        self.assertEqual(progress.course_points, CHAT_QUESTION_DAILY_LIMIT * CHAT_QUESTION_POINTS)

    def test_yesterdays_questions_do_not_count_against_today(self):
        """The daily cap only looks at the current day."""
        # Simulate a full day of rewards in the past.
        for _ in range(CHAT_QUESTION_DAILY_LIMIT):
            award_chat_question_reward(self.user.id, self.course.id)

        yesterday = timezone.now() - timedelta(days=1)
        RewardEventLog.objects.filter(
            account=self.user, event_type=CourseEventType.CHAT_POINTS_AWARDED,
        ).update(created_at=yesterday)

        state = award_chat_question_reward(self.user.id, self.course.id)
        self.assertEqual(state["points_awarded"], CHAT_QUESTION_POINTS)
