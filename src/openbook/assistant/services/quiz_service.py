# OpenBook: Interactive Online Textbooks - Server
# Copyright 2026 Sebastian Wolf, Daniel Sachada
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from __future__ import annotations

from uuid import UUID

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AnonymousUser

from openbook.content.models import Course
from openbook.content.models import CourseMaterial
from openbook.content.models import Textbook
from openbook.learning.services import LearningActivityService
from openbook.learning.services import LearningContextService

from .course_context import CourseContentContextService
from .llm_client import LLM_Client
from .prompt_builder import PromptBuilder
from .quiz_generation import GeneratedQuiz
from .quiz_generation import GeneratedQuizQuestion
from .quiz_generation import GradedQuiz
from .quiz_generation import GradedQuizQuestion
from .quiz_generation import QuizResponseParser
from .request_context import AssistantRequestContextService


class QuizService:
    """Generate course quizzes from RAG or authored course content."""

    def __init__(
        self,
        llm_client: LLM_Client | None = None,
        learning_context_service: LearningContextService | None = None,
        learning_activity_service: LearningActivityService | None = None,
        course_context_service: CourseContentContextService | None = None,
        request_context_service: AssistantRequestContextService | None = None,
        prompt_builder: PromptBuilder | None = None,
        response_parser: QuizResponseParser | None = None,
    ):
        self.llm_client = llm_client or LLM_Client()
        self.learning_context_service = learning_context_service or LearningContextService()
        self.learning_activity_service = learning_activity_service or LearningActivityService(
            context_service=self.learning_context_service,
        )
        self.course_context_service = course_context_service or CourseContentContextService()
        self.request_context_service = request_context_service or AssistantRequestContextService()
        self.prompt_builder = prompt_builder or PromptBuilder()
        self.response_parser = response_parser or QuizResponseParser()

    def generate_quiz(
        self,
        user: AbstractUser | AnonymousUser | None,
        course: Course,
        question_count: int = 5,
        textbook: Textbook | UUID | str | None = None,
    ) -> GeneratedQuiz:
        """
        Generate a course quiz from RAG documents or course content fallback.

        When ``textbook`` is given, the quiz is narrowed to that textbook and the result
        is anchored to the textbook's first page so points and skills can be awarded.
        """
        material = self.course_context_service.resolve_course_material(
            course=course,
            textbook=textbook,
        )
        question_count = max(1, min(int(question_count), 10))
        learning_context = self.learning_context_service.get_prompt_context(
            user=user,
            course=course,
        )
        rag_context = self.llm_client.retrieve_rag_context(
            query=self._build_quiz_query(
                course=course,
                question_count=question_count,
                material=material,
            ),
            course=course,
            limit=5,
        )

        course_context = ""
        context_source = "rag_documents"

        if not rag_context.context:
            context_source = "course_context"
            course_context = self.course_context_service.build_course_context(
                course,
                material=material,
            )

        prompt = self.prompt_builder.build_quiz_generation_prompt(
            document_context=rag_context.context,
            course_context=course_context,
            learning_context=learning_context,
            question_count=question_count,
        )
        response = self.llm_client.get_user_message(prompt)
        anchor_page = self.course_context_service.anchor_page_for_material(material)

        return GeneratedQuiz(
            questions=self.response_parser.parse(str(response or "")),
            context_source=context_source,
            sources=rag_context.sources,
            textbook_id=str(material.textbook_id) if material else None,
            page_id=str(anchor_page.id) if anchor_page else None,
        )

    def grade_quiz(
        self,
        user: AbstractUser | AnonymousUser | None,
        course: Course,
        quiz: GeneratedQuiz,
        answers: list[dict],
        attempts: int | None = None,
    ) -> dict:
        """Grade submitted quiz answers and record the learning result."""
        answer_by_id = {str(answer.get("question_id")): answer for answer in answers}
        results = tuple(
            self._grade_question(
                question=question,
                answer=answer_by_id.get(question.id, {}),
            )
            for question in quiz.questions
        )
        correct_count = sum(1 for result in results if result.correct)
        question_count = len(results)
        score = (correct_count / question_count) if question_count else 0.0
        graded_quiz = GradedQuiz(
            results=results,
            correct_count=correct_count,
            question_count=question_count,
            score=score,
        )

        reward = {"quiz_result": None, "points_awarded": 0, "skills_advanced": []}
        if quiz.page_id:
            reward = self.learning_activity_service.record_quiz_result(
                user=user,
                course=course,
                page=self.request_context_service.resolve_page(quiz.page_id),
                score=score,
                attempts=attempts,
            )

        return {
            "graded_quiz": graded_quiz,
            "quiz_result": reward.get("quiz_result"),
            "points_awarded": reward.get("points_awarded", 0),
            "skills_advanced": reward.get("skills_advanced", []),
        }

    def _build_quiz_query(
        self,
        course: Course,
        question_count: int,
        material: CourseMaterial | None = None,
    ) -> str:
        """Build the retrieval query used to find relevant quiz source documents."""
        if material is not None and material.textbook_id:
            return (
                f"Erzeuge {question_count} Multiple-Choice-Quizfragen zum Lehrbuch "
                f'"{material.textbook.name}" aus dem Kurs "{course.name}".'
            )

        return (
            f"Erzeuge {question_count} Multiple-Choice-Quizfragen fuer den Kurs "
            f'"{course.name}".'
        )

    def _grade_question(
        self,
        question: GeneratedQuizQuestion,
        answer: dict,
    ) -> GradedQuizQuestion:
        """Grade one multiple-choice quiz question."""
        selected_index = answer.get("selected_index")
        correct_index = next(
            index
            for index, option in enumerate(question.options)
            if option.correct
        )
        is_correct = (
            isinstance(selected_index, int)
            and 0 <= selected_index < len(question.options)
            and question.options[selected_index].correct
        )
        return GradedQuizQuestion(
            question_id=question.id,
            prompt=question.prompt,
            selected_index=selected_index
            if isinstance(selected_index, int)
            else None,
            correct_index=correct_index,
            correct=is_correct,
            correct_answer=question.options[correct_index].text,
        )
