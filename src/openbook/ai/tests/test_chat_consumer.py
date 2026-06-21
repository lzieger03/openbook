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


class ChatConsumerLearningEvent_Tests(SimpleTestCase):
    """Tests for learning progress WebSocket events."""

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
        page_id = uuid4()
        consumer = self._consumer(course_id=course_id)

        with patch("openbook.ai.consumers.chat.AssistantOrchestrator") as orchestrator:
            response = async_to_sync(consumer.handle_learning_quiz_result)(
                LearningQuizResult(
                    payload={
                        "page_id": page_id,
                        "score": 0.8,
                        "attempts": 2,
                    },
                ),
            )

        self.assertTrue(response.payload.success)
        orchestrator.return_value.record_quiz_result.assert_called_once_with(
            user=consumer.scope["user"],
            course=course_id,
            page=page_id,
            score=0.8,
            attempts=2,
        )

    def test_learning_events_require_course_route(self):
        """Learning events should fail on the global chat route."""
        consumer = self._consumer()

        response = async_to_sync(consumer.handle_learning_page_opened)(
            LearningPageOpened(payload={"page_id": uuid4()}),
        )

        self.assertFalse(response.payload.success)
        self.assertIn("course-scoped", response.payload.message)
