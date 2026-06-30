# OpenBook: Interactive Online Textbooks - Server
# Copyright 2026 Sebastian Wolf, Daniel Sachadä
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
from openbook.assistant.services.quiz_generation import GeneratedQuiz
from openbook.assistant.services.quiz_generation import GeneratedQuizOption
from openbook.assistant.services.quiz_generation import GeneratedQuizQuestion
from openbook.assistant.services.rag_client import RagContext
from openbook.assistant.services.rag_client import RagSource
from openbook.auth.middleware.current_user import reset_current_user
from openbook.auth.models.user import User
from openbook.content.models.course import Course
from openbook.content.models.course_material import CourseMaterial
from openbook.content.models.library_group import LibraryGroup
from openbook.content.models.textbook import Textbook
from openbook.content.models.textbook_page import TextbookPage


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
        self.page = TextbookPage.objects.create(
            textbook=self.textbook,
            name="Page",
            position=0,
        )
        self.llm_client = Mock()
        self.llm_client.perform_rag_query.return_value = "answer"
        self.learning_context_service = Mock()
        self.learning_context_service.get_prompt_context.return_value = "learning context"
        self.orchestrator = AssistantOrchestrator(
            llm_client=self.llm_client,
            learning_context_service=self.learning_context_service,
        )

    def _quiz_response(self):
        """Return a minimal valid generated quiz response."""
        return """
        {
            "questions": [
                {
                    "prompt": "What is HTML?",
                    "options": [
                        {"text": "Markup language", "correct": true},
                        {"text": "Database", "correct": false},
                        {"text": "Server", "correct": false},
                        {"text": "Image format", "correct": false}
                    ]
                }
            ]
        }
        """

    def test_answer_global_query(self):
        """Global chat should use the LLM directly without RAG."""
        self.llm_client.get_user_message.return_value = "direct answer"

        answer = self.orchestrator.answer("Question?", user=self.student)

        self.assertEqual(answer, "direct answer")
        self.llm_client.get_user_message.assert_called_once_with("Question?")
        self.llm_client.perform_rag_query.assert_not_called()
        self.learning_context_service.get_prompt_context.assert_not_called()

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
            learning_context="learning context",
        )
        self.learning_context_service.get_prompt_context.assert_called_once_with(
            user=self.owner,
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

    def test_answer_course_query_uses_rag_client_fallback(self):
        """Course chat fallback should stay inside the RAG client service."""
        self.llm_client.perform_rag_query.return_value = "direct course answer"

        answer = self.orchestrator.answer(
            "Question?",
            user=self.owner,
            course=self.course,
        )

        self.assertEqual(answer, "direct course answer")
        self.llm_client.perform_rag_query.assert_called_once_with(
            "Question?",
            course=self.course,
            learning_context="learning context",
        )
        self.llm_client.get_user_message.assert_not_called()

    def test_record_page_opened(self):
        """Page-open events should be delegated to the learning context service."""
        self.learning_context_service.record_page_opened.return_value = "learning state"

        learning_state = self.orchestrator.record_page_opened(
            user=self.owner,
            course=self.course,
            page=self.page,
        )

        self.assertEqual(learning_state, "learning state")
        self.learning_context_service.record_page_opened.assert_called_once_with(
            user=self.owner,
            course=self.course,
            page=self.page,
        )

    def test_mark_page_completed(self):
        """Page-completion events should be delegated to the learning context service."""
        self.learning_context_service.mark_page_completed.return_value = "learning state"

        learning_state = self.orchestrator.mark_page_completed(
            user=self.owner,
            course=self.course,
            page=self.page,
        )

        self.assertEqual(learning_state, "learning state")
        self.learning_context_service.mark_page_completed.assert_called_once_with(
            user=self.owner,
            course=self.course,
            page=self.page,
        )

    def test_record_quiz_result(self):
        """Quiz-result events should be delegated and return the awarded points."""
        self.learning_context_service.record_quiz_result.return_value = "quiz result"

        result = self.orchestrator.record_quiz_result(
            user=self.owner,
            course=self.course,
            page=self.page,
            score=0.75,
            attempts=3,
        )

        self.assertEqual(result["quiz_result"], "quiz result")
        self.assertIn("points_awarded", result)
        self.assertIn("skills_advanced", result)
        self.learning_context_service.record_quiz_result.assert_called_once_with(
            user=self.owner,
            course=self.course,
            page=self.page,
            score=0.75,
            attempts=3,
        )

    def test_grade_quiz_calculates_score_before_recording_result(self):
        """Submitted quiz answers should be graded server-side before learning is updated."""
        self.learning_context_service.record_quiz_result.return_value = "quiz result"
        quiz = GeneratedQuiz(
            context_source="course_context",
            page_id=str(self.page.id),
            questions=(
                GeneratedQuizQuestion(
                    id="question-1",
                    prompt="What is HTML?",
                    options=(
                        GeneratedQuizOption(text="Markup language", correct=True),
                        GeneratedQuizOption(text="Database", correct=False),
                        GeneratedQuizOption(text="Server", correct=False),
                        GeneratedQuizOption(text="Image format", correct=False),
                    ),
                ),
                GeneratedQuizQuestion(
                    id="question-2",
                    prompt="What is CSS?",
                    options=(
                        GeneratedQuizOption(text="Markup language", correct=False),
                        GeneratedQuizOption(text="Stylesheet language", correct=True),
                        GeneratedQuizOption(text="Server", correct=False),
                        GeneratedQuizOption(text="Image format", correct=False),
                    ),
                ),
            ),
        )

        result = self.orchestrator.grade_quiz(
            user=self.owner,
            course=self.course,
            quiz=quiz,
            answers=[
                {"question_id": "question-1", "selected_index": 0},
                {"question_id": "question-2", "selected_index": 0},
            ],
            attempts=1,
        )

        self.assertEqual(result["graded_quiz"].correct_count, 1)
        self.assertEqual(result["graded_quiz"].question_count, 2)
        self.assertEqual(result["graded_quiz"].score, 0.5)
        self.learning_context_service.record_quiz_result.assert_called_once_with(
            user=self.owner,
            course=self.course,
            page=self.page,
            score=0.5,
            attempts=1,
        )

    def test_generate_quiz_uses_rag_documents_first(self):
        """Quiz generation should prefer indexed assistant document context."""
        source = RagSource(
            chunk_id="chunk-1",
            document_id="document-1",
            document_title="Guide",
            position=0,
        )
        self.llm_client.retrieve_rag_context.return_value = RagContext(
            context="Indexed HTML context",
            sources=(source,),
        )
        self.llm_client.get_user_message.return_value = self._quiz_response()

        quiz = self.orchestrator.generate_quiz(
            user=self.owner,
            course=self.course,
            question_count=1,
        )

        self.assertEqual(quiz.context_source, "rag_documents")
        self.assertEqual(quiz.sources, (source,))
        self.assertEqual(len(quiz.questions), 1)
        self.llm_client.retrieve_rag_context.assert_called_once()
        prompt = self.llm_client.get_user_message.call_args.args[0]
        self.assertIn("Indexed HTML context", prompt)
        self.assertNotIn("Kurskontext:", prompt)

    def test_generate_quiz_falls_back_to_course_context(self):
        """Quiz generation should use course content when no RAG documents exist."""
        self.page.content = {
            "type": "source",
            "format": "MD",
            "source": "# HTML Basics\nHTML structures web pages.",
        }
        self.page.save(update_fields=["content"])
        self.llm_client.retrieve_rag_context.return_value = RagContext(
            context="",
            sources=(),
        )
        self.llm_client.get_user_message.return_value = self._quiz_response()

        quiz = self.orchestrator.generate_quiz(
            user=self.owner,
            course=self.course,
            question_count=1,
        )

        self.assertEqual(quiz.context_source, "course_context")
        self.assertEqual(len(quiz.questions), 1)
        prompt = self.llm_client.get_user_message.call_args.args[0]
        self.assertIn("Kurskontext:", prompt)
        self.assertIn("Course", prompt)
        self.assertIn("HTML structures web pages.", prompt)

    def test_generate_quiz_scoped_to_textbook_anchors_page(self):
        """A textbook-scoped quiz reports the textbook and a page to anchor the result to."""
        self.page.content = {
            "type": "source",
            "format": "MD",
            "source": "# HTML Basics\nHTML structures web pages.",
        }
        self.page.save(update_fields=["content"])
        self.llm_client.retrieve_rag_context.return_value = RagContext(context="", sources=())
        self.llm_client.get_user_message.return_value = self._quiz_response()

        quiz = self.orchestrator.generate_quiz(
            user=self.owner,
            course=self.course,
            question_count=1,
            textbook=self.textbook,
        )

        self.assertEqual(quiz.textbook_id, str(self.textbook.id))
        self.assertEqual(quiz.page_id, str(self.page.id))

    def test_generate_quiz_rejects_textbook_not_in_course(self):
        """Choosing a textbook that is not part of the course is rejected."""
        other_textbook = Textbook.objects.create(
            name="Other",
            slug="other",
            group=self.library_group,
        )

        with self.assertRaises(ValueError):
            self.orchestrator.generate_quiz(
                user=self.owner,
                course=self.course,
                question_count=1,
                textbook=other_textbook,
            )

    def test_record_page_opened_denied(self):
        """Learning-state writes should require course access."""
        with self.assertRaises(PermissionDenied):
            self.orchestrator.record_page_opened(
                user=self.student,
                course=self.course,
                page=self.page,
            )
