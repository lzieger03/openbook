# OpenBook: Interactive Online Textbooks - Server
# Copyright 2026 Sebastian Wolf, Daniel Sachada
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.core.exceptions import ValidationError
from django.test import TestCase

from openbook.auth.middleware.current_user import reset_current_user
from openbook.auth.models.user import User
from openbook.content.models.course import Course
from openbook.content.models.course_material import CourseMaterial
from openbook.content.models.library_group import LibraryGroup
from openbook.content.models.textbook import Textbook
from openbook.content.models.textbook_page import TextbookPage
from openbook.gamification.models.course_progress import CourseProgress
from openbook.learning.models.quiz_result import QuizResult
from openbook.learning.models.state import LearningState
from openbook.learning.services import LearningContextService


class LearningContextService_Tests(TestCase):
    """Tests for the LearningContextService."""

    def setUp(self):
        reset_current_user()
        self.user = User.objects.create_user(
            username="student",
            email="student@example.com",
            password="password",
        )
        self.library_group = LibraryGroup.objects.create(name="Library", slug="library")
        self.course = Course.objects.create(
            name="Course",
            slug="course",
            group=self.library_group,
        )
        self.textbook = Textbook.objects.create(
            name="Textbook",
            slug="textbook",
            group=self.library_group,
        )
        CourseMaterial.objects.create(
            course=self.course,
            textbook=self.textbook,
            position=0,
        )
        self.last_page = TextbookPage.objects.create(
            textbook=self.textbook,
            name="Basics",
            position=0,
        )
        self.completed_page = TextbookPage.objects.create(
            textbook=self.textbook,
            name="Setup",
            position=1,
        )
        self.service = LearningContextService()

    def test_get_prompt_context(self):
        """Learning context should include learning, quiz, and gamification data."""
        learning_state = LearningState.objects.create(
            user=self.user,
            course=self.course,
            last_page=self.last_page,
        )
        learning_state.completed_pages.add(self.completed_page)
        QuizResult.objects.create(
            user=self.user,
            page=self.last_page,
            score=0.4,
            attempts=2,
        )
        CourseProgress.objects.create(
            account=self.user,
            course=self.course,
            course_points=120,
            course_level=3,
            course_progress=25,
        )

        context = self.service.get_prompt_context(
            user=self.user,
            course=self.course,
        )

        self.assertIn("Zuletzt gelesene Seite: Basics.", context)
        self.assertIn("Abgeschlossene Seiten: Setup.", context)
        self.assertIn("Schwache Quizbereiche: Basics.", context)
        self.assertIn("Kurslevel 3", context)

    def test_record_page_opened_creates_learning_state(self):
        """Opening a page should create or update the user's learning state."""
        learning_state = self.service.record_page_opened(
            user=self.user,
            course=self.course,
            page=self.last_page,
        )

        self.assertEqual(learning_state.last_page, self.last_page)
        self.assertEqual(learning_state.user, self.user)
        self.assertEqual(learning_state.course, self.course)

    def test_mark_page_completed_creates_learning_state(self):
        """Completing a page should add it to the user's completed pages."""
        learning_state = self.service.mark_page_completed(
            user=self.user,
            course=self.course,
            page=self.completed_page,
        )

        self.assertIn(self.completed_page, learning_state.completed_pages.all())

    def test_record_quiz_result_creates_and_updates_result(self):
        """Quiz results should be stored once per user and page."""
        quiz_result = self.service.record_quiz_result(
            user=self.user,
            course=self.course,
            page=self.last_page,
            score=0.8,
        )

        updated_quiz_result = self.service.record_quiz_result(
            user=self.user,
            course=self.course,
            page=self.last_page,
            score=0.4,
        )

        self.assertEqual(updated_quiz_result.id, quiz_result.id)
        self.assertEqual(updated_quiz_result.score, 0.4)
        self.assertEqual(updated_quiz_result.attempts, 2)

    def test_record_page_opened_rejects_page_outside_course(self):
        """Learning updates should reject pages outside the course material."""
        outside_textbook = Textbook.objects.create(
            name="Outside Textbook",
            slug="outside-textbook",
            group=self.library_group,
        )
        outside_page = TextbookPage.objects.create(
            textbook=outside_textbook,
            name="Outside",
            position=0,
        )

        with self.assertRaises(ValidationError):
            self.service.record_page_opened(
                user=self.user,
                course=self.course,
                page=outside_page,
            )

    def test_record_quiz_result_rejects_invalid_score(self):
        """Quiz results should only accept normalized scores."""
        with self.assertRaises(ValidationError):
            self.service.record_quiz_result(
                user=self.user,
                course=self.course,
                page=self.last_page,
                score=1.5,
            )
