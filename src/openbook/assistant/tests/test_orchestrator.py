# OpenBook: Interactive Online Textbooks - Server
# Copyright 2026 Sebastian Wolf, Daniel Sachada
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from unittest.mock import Mock

from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied
from django.test import TestCase

from openbook.assistant.services.orchestrator import AssistantOrchestrator
from openbook.auth.middleware.current_user import reset_current_user
from openbook.auth.models.user import User
from openbook.content.models.course import Course
from openbook.content.models.library_group import LibraryGroup


class AssistantOrchestrator_Tests(TestCase):
    """Tests for the AssistantOrchestrator service."""

    def setUp(self):
        reset_current_user()
        self.owner = User.objects.create_user(
            username="teacher",
            email="teacher@example.com",
            password="password",
        )
        self.student = User.objects.create_user(
            username="student",
            email="student@example.com",
            password="password",
        )
        self.library_group = LibraryGroup.objects.create(name="Library", slug="library")
        self.course = Course.objects.create(
            name="Course",
            slug="course",
            group=self.library_group,
            owner=self.owner,
        )
        self.llm_client = Mock()
        self.llm_client.perform_rag_query.return_value = "answer"
        self.orchestrator = AssistantOrchestrator(llm_client=self.llm_client)

    def test_answer_global_query(self):
        """Global chat should not require a course permission check."""
        answer = self.orchestrator.answer("Question?", user=self.student)

        self.assertEqual(answer, "answer")
        self.llm_client.perform_rag_query.assert_called_once_with(
            "Question?",
            course=None,
        )

    def test_answer_global_query_denied_for_anonymous_user(self):
        """Global chat should require authentication."""
        with self.assertRaises(PermissionDenied):
            self.orchestrator.answer("Question?", user=AnonymousUser())

    def test_answer_course_query(self):
        """Course chat should pass the course into RAG."""
        answer = self.orchestrator.answer(
            "Question?",
            user=self.owner,
            course=self.course,
        )

        self.assertEqual(answer, "answer")
        self.llm_client.perform_rag_query.assert_called_once_with(
            "Question?",
            course=self.course,
        )

    def test_answer_course_query_denied(self):
        """Course chat should require course view permission."""
        with self.assertRaises(PermissionDenied):
            self.orchestrator.answer(
                "Question?",
                user=self.student,
                course=self.course,
            )
