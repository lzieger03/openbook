# OpenBook: Interactive Online Textbooks - Server
# Copyright 2026 Sebastian Wolf, Daniel Sachada
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from __future__ import annotations

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AnonymousUser

from openbook.content.models import Course
from openbook.learning.services import LearningActivityService
from openbook.learning.services import LearningContextService

from .llm_client import LLM_Client


class AssistantChatService:
    """Answer global and course-scoped assistant chat requests."""

    def __init__(
        self,
        llm_client: LLM_Client | None = None,
        learning_context_service: LearningContextService | None = None,
        learning_activity_service: LearningActivityService | None = None,
    ):
        self.llm_client = llm_client or LLM_Client()
        self.learning_context_service = learning_context_service or LearningContextService()
        self.learning_activity_service = learning_activity_service or LearningActivityService(
            context_service=self.learning_context_service,
        )

    def answer(
        self,
        query: str,
        user: AbstractUser | AnonymousUser | None,
        course: Course | None = None,
    ) -> str:
        """Generate an assistant answer for a global or course-scoped query."""
        if course is None:
            return self.llm_client.get_user_message(query)

        self.learning_activity_service.record_chat_question(user=user, course=course)
        learning_context = self.learning_context_service.get_prompt_context(
            user=user,
            course=course,
        )

        try:
            return self.llm_client.perform_rag_query(
                query,
                course=course,
                learning_context=learning_context,
            )
        except RuntimeError as error:
            if str(error) in {
                "No global assistant documents have been indexed yet.",
                "No assistant documents have been indexed for this course yet.",
            }:
                return self.llm_client.get_user_message(query)

            raise
