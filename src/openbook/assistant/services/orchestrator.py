# OpenBook: Interactive Online Textbooks - Server
# Copyright 2026 Sebastian Wolf, Daniel Sachada
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from __future__ import annotations

from typing import Any
from uuid import UUID

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AnonymousUser

from openbook.content.models import Course
from openbook.content.models import Textbook
from openbook.content.models import TextbookPage
from openbook.learning.models import LearningState
from openbook.learning.services import LearningActivityService
from openbook.learning.services import LearningContextService

from .chat import AssistantChatService
from .course_context import CourseContentContextService
from .exam_generation import ExamGenerationParser
from .exam_generation import ExamGradingParser
from .exam_generation import GeneratedExam
from .exam_service import ExamService
from .llm_client import LLM_Client
from .prompt_builder import PromptBuilder
from .quiz_generation import GeneratedQuiz
from .quiz_generation import QuizResponseParser
from .quiz_service import QuizService
from .request_context import AssistantRequestContextService


class AssistantOrchestrator:
    """Route assistant requests to focused services."""

    def __init__(
        self,
        llm_client: LLM_Client | None = None,
        learning_context_service: LearningContextService | None = None,
        learning_activity_service: LearningActivityService | None = None,
        request_context_service: AssistantRequestContextService | None = None,
        course_context_service: CourseContentContextService | None = None,
        chat_service: AssistantChatService | None = None,
        quiz_service: QuizService | None = None,
        exam_service: ExamService | None = None,
        prompt_builder: PromptBuilder | None = None,
        quiz_response_parser: QuizResponseParser | None = None,
        exam_generation_parser: ExamGenerationParser | None = None,
        exam_grading_parser: ExamGradingParser | None = None,
    ):
        self.llm_client = llm_client or LLM_Client()
        self.learning_context_service = learning_context_service or LearningContextService()
        self.learning_activity_service = learning_activity_service or LearningActivityService(
            context_service=self.learning_context_service,
        )
        self.request_context_service = request_context_service or AssistantRequestContextService()
        self.course_context_service = course_context_service or CourseContentContextService()
        self.prompt_builder = prompt_builder or PromptBuilder()
        self.quiz_response_parser = quiz_response_parser or QuizResponseParser()
        self.exam_generation_parser = exam_generation_parser or ExamGenerationParser()
        self.exam_grading_parser = exam_grading_parser or ExamGradingParser()
        self.chat_service = chat_service or AssistantChatService(
            llm_client=self.llm_client,
            learning_context_service=self.learning_context_service,
            learning_activity_service=self.learning_activity_service,
        )
        self.quiz_service = quiz_service or QuizService(
            llm_client=self.llm_client,
            learning_context_service=self.learning_context_service,
            learning_activity_service=self.learning_activity_service,
            course_context_service=self.course_context_service,
            request_context_service=self.request_context_service,
            prompt_builder=self.prompt_builder,
            response_parser=self.quiz_response_parser,
        )
        self.exam_service = exam_service or ExamService(
            llm_client=self.llm_client,
            learning_activity_service=self.learning_activity_service,
            course_context_service=self.course_context_service,
            request_context_service=self.request_context_service,
            prompt_builder=self.prompt_builder,
            generation_parser=self.exam_generation_parser,
            grading_parser=self.exam_grading_parser,
        )

    def answer(
        self,
        query: str,
        user: AbstractUser | AnonymousUser | None = None,
        course: Course | UUID | str | None = None,
    ) -> str:
        """Generate an assistant answer for a global or course-scoped query."""
        course_obj = self.request_context_service.resolve_course(course)
        self.request_context_service.check_chat_permission(user=user, course=course_obj)
        return self.chat_service.answer(
            query=query,
            user=user,
            course=course_obj,
        )

    def record_page_opened(
        self,
        user: AbstractUser | AnonymousUser | None,
        course: Course | UUID | str,
        page: TextbookPage | UUID | str,
    ) -> LearningState:
        """Store that a user opened a course page."""
        course_obj = self.request_context_service.resolve_required_course(course)
        page_obj = self.request_context_service.resolve_page(page)
        self.request_context_service.check_chat_permission(user=user, course=course_obj)
        return self.learning_activity_service.record_page_opened(
            user=user,
            course=course_obj,
            page=page_obj,
        )

    def mark_page_completed(
        self,
        user: AbstractUser | AnonymousUser | None,
        course: Course | UUID | str,
        page: TextbookPage | UUID | str,
    ) -> LearningState:
        """Store that a user completed a course page."""
        course_obj = self.request_context_service.resolve_required_course(course)
        page_obj = self.request_context_service.resolve_page(page)
        self.request_context_service.check_chat_permission(user=user, course=course_obj)
        return self.learning_activity_service.mark_page_completed(
            user=user,
            course=course_obj,
            page=page_obj,
        )

    def record_quiz_result(
        self,
        user: AbstractUser | AnonymousUser | None,
        course: Course | UUID | str,
        page: TextbookPage | UUID | str,
        score: float,
        attempts: int | None = None,
    ) -> dict[str, Any]:
        """Store the user's latest quiz result for a course page and award points."""
        course_obj = self.request_context_service.resolve_required_course(course)
        page_obj = self.request_context_service.resolve_page(page)
        self.request_context_service.check_chat_permission(user=user, course=course_obj)
        return self.learning_activity_service.record_quiz_result(
            user=user,
            course=course_obj,
            page=page_obj,
            score=score,
            attempts=attempts,
        )

    def generate_quiz(
        self,
        user: AbstractUser | AnonymousUser | None,
        course: Course | UUID | str,
        question_count: int = 5,
        textbook: Textbook | UUID | str | None = None,
    ) -> GeneratedQuiz:
        """Generate a course quiz."""
        course_obj = self.request_context_service.resolve_required_course(course)
        self.request_context_service.check_chat_permission(user=user, course=course_obj)
        return self.quiz_service.generate_quiz(
            user=user,
            course=course_obj,
            question_count=question_count,
            textbook=textbook,
        )

    def grade_quiz(
        self,
        user: AbstractUser | AnonymousUser | None,
        course: Course | UUID | str,
        quiz: GeneratedQuiz,
        answers: list[dict],
        attempts: int | None = None,
    ) -> dict[str, Any]:
        """Grade a submitted quiz and award rewards."""
        course_obj = self.request_context_service.resolve_required_course(course)
        self.request_context_service.check_chat_permission(user=user, course=course_obj)
        return self.quiz_service.grade_quiz(
            user=user,
            course=course_obj,
            quiz=quiz,
            answers=answers,
            attempts=attempts,
        )

    def generate_exam(
        self,
        user: AbstractUser | AnonymousUser | None,
        course: Course | UUID | str,
        question_count: int = 5,
        textbook: Textbook | UUID | str | None = None,
    ) -> GeneratedExam:
        """Generate a course exam."""
        course_obj = self.request_context_service.resolve_required_course(course)
        self.request_context_service.check_chat_permission(user=user, course=course_obj)
        return self.exam_service.generate_exam(
            user=user,
            course=course_obj,
            question_count=question_count,
            textbook=textbook,
        )

    def grade_exam(
        self,
        user: AbstractUser | AnonymousUser | None,
        course: Course | UUID | str,
        exam: GeneratedExam,
        answers: list[dict],
    ) -> dict[str, Any]:
        """Grade a submitted exam and award rewards."""
        course_obj = self.request_context_service.resolve_required_course(course)
        self.request_context_service.check_chat_permission(user=user, course=course_obj)
        return self.exam_service.grade_exam(
            user=user,
            course=course_obj,
            exam=exam,
            answers=answers,
        )
