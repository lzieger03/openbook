# OpenBook: Interactive Online Textbooks - Server
# Copyright 2026 Sebastian Wolf, Daniel Sachadä
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from datetime import UTC
from datetime import datetime
from types import SimpleNamespace
from unittest.mock import patch
from uuid import uuid4

from asgiref.sync import async_to_sync
from django.test import SimpleTestCase
from django.test import TestCase

from openbook.ai.consumers.chat import ChatConsumer
from openbook.ai.messages.chat import ChatMessagePayload
from openbook.ai.messages.chat import LearningPageCompleted
from openbook.ai.messages.chat import LearningPageOpened
from openbook.ai.messages.chat import LearningQuizResult
from openbook.ai.messages.chat import QuizStart
from openbook.assistant.models import ChatMessage
from openbook.assistant.models import ChatSession
from openbook.assistant.models import ExamAttempt
from openbook.assistant.services.quiz_generation import GeneratedQuiz
from openbook.assistant.services.quiz_generation import GeneratedQuizOption
from openbook.assistant.services.quiz_generation import GeneratedQuizQuestion
from openbook.auth.models.user import User
from openbook.content.models.course import Course
from openbook.content.models.library_group import LibraryGroup
from openbook.content.models.textbook import Textbook
from openbook.content.models.textbook_page import TextbookPage


class ChatConsumerLearningEvent_Tests(SimpleTestCase):
    """Tests for learning progress WebSocket events."""

    def test_consumer_does_not_camelize_messages(self):
        """
        Outgoing fields must stay snake_case. The frontend reads snake_case keys (e.g.
        ``page_id``, ``points_awarded``); chanx's camelCase conversion would rename them
        and silently break quiz anchoring and point awarding.
        """
        self.assertFalse(ChatConsumer().should_camelize)

    def _consumer(self, course_id=None) -> ChatConsumer:
        """Return a ChatConsumer with a minimal test scope."""
        consumer = ChatConsumer()
        kwargs = {}
        if course_id is not None:
            kwargs["course_id"] = course_id

        consumer.scope = {
            "url_route": {"kwargs": kwargs},
            "user": SimpleNamespace(is_authenticated=True),
        }
        return consumer

    def test_handle_learning_page_opened(self):
        """Page-opened events should be delegated to the orchestrator."""
        course_id = uuid4()
        page_id = uuid4()
        consumer = self._consumer(course_id=course_id)

        with patch("openbook.ai.consumers.chat.AssistantOrchestrator") as orchestrator:
            response = async_to_sync(consumer.handle_learning_page_opened)(
                LearningPageOpened(payload={"page_id": page_id}),
            )

        self.assertTrue(response.payload.success)
        orchestrator.return_value.record_page_opened.assert_called_once_with(
            user=consumer.scope["user"],
            course=course_id,
            page=page_id,
        )

    def test_handle_learning_page_completed(self):
        """Page-completed events should be delegated to the orchestrator."""
        course_id = uuid4()
        page_id = uuid4()
        consumer = self._consumer(course_id=course_id)

        with patch("openbook.ai.consumers.chat.AssistantOrchestrator") as orchestrator:
            response = async_to_sync(consumer.handle_learning_page_completed)(
                LearningPageCompleted(payload={"page_id": page_id}),
            )

        self.assertTrue(response.payload.success)
        orchestrator.return_value.mark_page_completed.assert_called_once_with(
            user=consumer.scope["user"],
            course=course_id,
            page=page_id,
        )

    def test_handle_learning_quiz_result(self):
        """Quiz-result events should be delegated to the orchestrator."""
        course_id = uuid4()
        quiz_id = uuid4()
        consumer = self._consumer(course_id=course_id)
        graded_quiz = SimpleNamespace(
            score=0.5,
            correct_count=1,
            question_count=2,
            results=(
                SimpleNamespace(
                    question_id="q1",
                    selected_index=0,
                    correct_index=0,
                    correct=True,
                    correct_answer="Markup language",
                ),
            ),
        )

        with patch.object(consumer, "_record_quiz_result") as record_quiz_result:
            record_quiz_result.return_value = {
                "graded_quiz": graded_quiz,
                "points_awarded": 40,
                "skills_advanced": ["HTML", "CSS"],
            }
            response = async_to_sync(consumer.handle_learning_quiz_result)(
                LearningQuizResult(
                    payload={
                        "quiz_id": quiz_id,
                        "answers": [
                            {
                                "question_id": "q1",
                                "selected_index": 0,
                            },
                        ],
                        "attempts": 2,
                    },
                ),
            )

        self.assertTrue(response.payload.success)
        self.assertEqual(response.payload.points_awarded, 40)
        self.assertEqual(response.payload.skills_advanced, ["HTML", "CSS"])
        self.assertEqual(response.payload.score, 0.5)
        self.assertEqual(response.payload.correct_count, 1)
        self.assertEqual(response.payload.question_count, 2)
        self.assertTrue(response.payload.quiz_results[0].correct)
        record_quiz_result.assert_called_once()
        self.assertEqual(
            record_quiz_result.call_args.kwargs["quiz_id"],
            quiz_id,
        )

    def test_learning_events_require_course_route(self):
        """Learning events should fail on the global chat route."""
        consumer = self._consumer()

        response = async_to_sync(consumer.handle_learning_page_opened)(
            LearningPageOpened(payload={"page_id": uuid4()}),
        )

        self.assertFalse(response.payload.success)
        self.assertIn("course-scoped", response.payload.message)

    def test_handle_quiz_start(self):
        """Quiz-start events should be delegated to the orchestrator."""
        course_id = uuid4()
        consumer = self._consumer(course_id=course_id)
        generated_quiz = GeneratedQuiz(
            context_source="course_context",
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
            ),
        )
        quiz_attempt = SimpleNamespace(id=uuid4())

        with patch.object(consumer, "_generate_quiz") as generate_quiz:
            generate_quiz.return_value = (quiz_attempt, generated_quiz)
            response = async_to_sync(consumer.handle_quiz_start)(
                QuizStart(payload={"question_count": 1}),
            )

        generate_quiz.assert_called_once_with(question_count=1, textbook_id=None)
        self.assertEqual(response.payload.quiz_id, quiz_attempt.id)
        self.assertEqual(response.payload.context_source, "course_context")
        self.assertEqual(response.payload.questions[0].id, "question-1")
        self.assertEqual(response.payload.questions[0].prompt, "What is HTML?")
        self.assertFalse(hasattr(response.payload.questions[0].options[0], "correct"))

    def test_quiz_start_requires_course_route(self):
        """Quiz generation should fail on the global chat route."""
        consumer = self._consumer()

        response = async_to_sync(consumer.handle_quiz_start)(
            QuizStart(payload={"question_count": 1}),
        )

        self.assertFalse(response.payload.success)
        self.assertEqual(response.payload.event, "quiz_start")
        self.assertIn("course-scoped", response.payload.message)


class ChatConsumerPersistenceScope_Tests(TestCase):
    """Tests for course scoping of persisted assistant state."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="student",
            email="student@example.com",
            password="password",
        )
        self.library_group = LibraryGroup.objects.create(name="Library", slug="library")
        self.course = Course.objects.create(
            name="Course A",
            slug="course-a",
            group=self.library_group,
            owner=self.user,
        )
        self.other_course = Course.objects.create(
            name="Course B",
            slug="course-b",
            group=self.library_group,
            owner=self.user,
        )

    def _consumer(self, course: Course) -> ChatConsumer:
        """Return a consumer scoped to the given course."""
        consumer = ChatConsumer()
        consumer.scope = {
            "url_route": {"kwargs": {"course_id": course.id}},
            "user": self.user,
        }
        return consumer

    def _message_payload(self, sender: str, content: str) -> ChatMessagePayload:
        """Return a minimal persisted chat payload."""
        return ChatMessagePayload(
            datetime=datetime.now(UTC),
            sender=sender,
            type="normal",
            severity="info",
            guardRails={"findings": "none", "explanation": ""},
            format="markdown",
            content=content,
            finished=True,
        )

    def test_load_active_history_ignores_session_from_another_course(self):
        """A stale session id from another course must not leak chat history."""
        other_session = ChatSession.objects.create(
            user=self.user,
            course=self.other_course,
            title="Other course",
        )
        ChatMessage.objects.create(
            session=other_session,
            sender="assistant",
            content="Hidden message",
        )
        consumer = self._consumer(self.course)
        consumer.session_id = str(other_session.id)

        session_id, messages = consumer._load_active_history()

        self.assertIsNone(session_id)
        self.assertEqual(messages, [])

    def test_rename_session_does_not_touch_another_course(self):
        """Course-scoped rename messages must not rename another course's chat."""
        other_session = ChatSession.objects.create(
            user=self.user,
            course=self.other_course,
            title="Original",
        )
        consumer = self._consumer(self.course)

        consumer._rename_session(other_session.id, "Renamed")

        other_session.refresh_from_db()
        self.assertEqual(other_session.title, "Original")

    def test_delete_session_does_not_remove_another_course(self):
        """Course-scoped delete messages must not delete another course's chat."""
        other_session = ChatSession.objects.create(
            user=self.user,
            course=self.other_course,
            title="Original",
        )
        consumer = self._consumer(self.course)

        deleted_active = consumer._delete_session(other_session.id)

        self.assertFalse(deleted_active)
        self.assertTrue(ChatSession.objects.filter(pk=other_session.id).exists())

    def test_persist_turn_creates_current_course_session_for_stale_session_id(self):
        """A stale session id must not append messages to a different course."""
        other_session = ChatSession.objects.create(
            user=self.user,
            course=self.other_course,
            title="Other course",
        )
        consumer = self._consumer(self.course)
        consumer.session_id = str(other_session.id)

        session_id, created_new = consumer._persist_turn(
            self._message_payload("user", "Question"),
            self._message_payload("assistant", "Answer"),
            "Question",
        )

        self.assertTrue(created_new)
        self.assertNotEqual(session_id, str(other_session.id))
        self.assertEqual(ChatSession.objects.get(pk=session_id).course, self.course)
        self.assertEqual(other_session.messages.count(), 0)

    def test_load_saved_exam_requires_current_course(self):
        """A saved exam from another course must not be resumed in this course."""
        textbook = Textbook.objects.create(
            name="Textbook",
            slug="textbook",
            group=self.library_group,
        )
        page = TextbookPage.objects.create(textbook=textbook, name="Page", position=0)
        attempt = ExamAttempt.objects.create(
            user=self.user,
            course=self.other_course,
            textbook=textbook,
            exam={
                "context_source": "course_context",
                "textbook_id": str(textbook.id),
                "page_id": str(page.id),
                "questions": [],
            },
        )
        consumer = self._consumer(self.course)

        self.assertIsNone(consumer._load_saved_exam(str(attempt.id)))
