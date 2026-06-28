# OpenBook: Interactive Online Textbooks - Server
# Copyright 2026 Sebastian Wolf, Daniel Sachada
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from types import SimpleNamespace
from unittest.mock import patch
from uuid import uuid4

from asgiref.sync import async_to_sync
from django.test import SimpleTestCase

from openbook.ai.consumers.chat import ChatConsumer
from openbook.ai.messages.chat import LearningPageCompleted
from openbook.ai.messages.chat import LearningPageOpened
from openbook.ai.messages.chat import LearningQuizResult
from openbook.ai.messages.chat import QuizStart
from openbook.assistant.services.quiz_generation import GeneratedQuiz
from openbook.assistant.services.quiz_generation import GeneratedQuizOption
from openbook.assistant.services.quiz_generation import GeneratedQuizQuestion


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
