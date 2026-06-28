# OpenBook: Interactive Online Textbooks - Server
# Copyright 2026 Sebastian Wolf, Daniel Sachada
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from __future__ import annotations

import logging
from typing import Any
from uuid import UUID

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AnonymousUser

from openbook.content.models import Course
from openbook.content.models import Textbook
from openbook.learning.services import LearningActivityService

from .course_context import CourseContentContextService
from .exam_generation import _clamp_points
from .exam_generation import ExamGenerationParser
from .exam_generation import ExamGradingParser
from .exam_generation import GeneratedExam
from .exam_generation import GeneratedExamQuestion
from .exam_generation import GradedExam
from .exam_generation import GradedExamQuestion
from .llm_client import LLM_Client
from .prompt_builder import PromptBuilder
from .request_context import AssistantRequestContextService

logger = logging.getLogger(__name__)


class ExamService:
    """Generate and grade course exams."""

    def __init__(
        self,
        llm_client: LLM_Client | None = None,
        learning_activity_service: LearningActivityService | None = None,
        course_context_service: CourseContentContextService | None = None,
        request_context_service: AssistantRequestContextService | None = None,
        prompt_builder: PromptBuilder | None = None,
        generation_parser: ExamGenerationParser | None = None,
        grading_parser: ExamGradingParser | None = None,
    ):
        self.llm_client = llm_client or LLM_Client()
        self.learning_activity_service = learning_activity_service or LearningActivityService()
        self.course_context_service = course_context_service or CourseContentContextService()
        self.request_context_service = request_context_service or AssistantRequestContextService()
        self.prompt_builder = prompt_builder or PromptBuilder()
        self.generation_parser = generation_parser or ExamGenerationParser()
        self.grading_parser = grading_parser or ExamGradingParser()

    def generate_exam(
        self,
        user: AbstractUser | AnonymousUser | None,
        course: Course,
        question_count: int = 5,
        textbook: Textbook | UUID | str | None = None,
    ) -> GeneratedExam:
        """
        Generate a mixed free-text + multiple-choice exam from selected textbook pages.
        """
        material = self.course_context_service.resolve_course_material(
            course=course,
            textbook=textbook,
        )
        if material is None or not material.textbook_id:
            raise ValueError("An exam requires a textbook to be selected.")

        question_count = max(1, min(int(question_count), 10))
        textbook_context = self.course_context_service.build_textbook_pages_context(material)
        if not textbook_context.strip():
            raise ValueError("The selected textbook has no page content to build an exam from.")

        prompt = self.prompt_builder.build_exam_generation_prompt(
            document_context="",
            course_context=textbook_context,
            learning_context="",
            question_count=question_count,
        )
        response = self.llm_client.get_user_message(prompt)
        anchor_page = self.course_context_service.anchor_page_for_material(material)

        return GeneratedExam(
            questions=self.generation_parser.parse(str(response or "")),
            context_source="course_context",
            sources=(),
            textbook_id=str(material.textbook_id),
            page_id=str(anchor_page.id) if anchor_page else None,
        )

    def grade_exam(
        self,
        user: AbstractUser | AnonymousUser | None,
        course: Course,
        exam: GeneratedExam,
        answers: list[dict],
    ) -> dict[str, Any]:
        """Grade a submitted exam and award learning rewards."""
        answer_by_id = {str(answer.get("question_id")): answer for answer in answers}
        graded_by_id: dict[str, GradedExamQuestion] = {}
        free_text_items: list[dict] = []
        free_text_answers: dict[str, str] = {}

        for question in exam.questions:
            answer = answer_by_id.get(question.id, {})

            if question.kind == "multiple_choice":
                graded_by_id[question.id] = self._grade_choice_question(question, answer)
            else:
                student_answer = str(answer.get("text") or "").strip()
                free_text_answers[question.id] = student_answer
                free_text_items.append(
                    {
                        "question_id": question.id,
                        "prompt": question.prompt,
                        "expected": question.expected,
                        "max_points": question.max_points,
                        "answer": student_answer,
                    }
                )

        verdicts = self._grade_free_text(free_text_items)
        for question in exam.questions:
            if question.kind != "multiple_choice":
                graded_by_id[question.id] = self._grade_free_text_question(
                    question,
                    student_answer=free_text_answers.get(question.id, ""),
                    verdict=verdicts.get(question.id, {}),
                )

        results = tuple(graded_by_id[question.id] for question in exam.questions)
        total_points = sum(result.awarded_points for result in results)
        max_points = sum(result.max_points for result in results)
        score = (total_points / max_points) if max_points else 0.0

        graded_exam = GradedExam(
            results=results,
            total_points=total_points,
            max_points=max_points,
            score=score,
        )

        reward: dict[str, Any] = {"points_awarded": 0, "skills_advanced": []}
        if exam.page_id:
            reward = self.learning_activity_service.record_exam_result(
                user=user,
                course=course,
                page=self.request_context_service.resolve_page(exam.page_id),
                score=score,
            )

        return {
            "graded_exam": graded_exam,
            "points_awarded": reward.get("points_awarded", 0),
            "skills_advanced": reward.get("skills_advanced", []),
        }

    def _grade_choice_question(
        self,
        question: GeneratedExamQuestion,
        answer: dict,
    ) -> GradedExamQuestion:
        """Grade one multiple-choice question by comparing the picked option."""
        selected_index = answer.get("selected_index")
        correct_index = next(
            (index for index, option in enumerate(question.options) if option.correct),
            None,
        )
        is_correct = (
            isinstance(selected_index, int)
            and 0 <= selected_index < len(question.options)
            and question.options[selected_index].correct
        )
        your_answer = (
            question.options[selected_index].text
            if isinstance(selected_index, int) and 0 <= selected_index < len(question.options)
            else ""
        )
        correct_answer = (
            question.options[correct_index].text if correct_index is not None else ""
        )

        return GradedExamQuestion(
            question_id=question.id,
            kind="multiple_choice",
            prompt=question.prompt,
            your_answer=your_answer,
            awarded_points=question.max_points if is_correct else 0,
            max_points=question.max_points,
            feedback="Richtig." if is_correct else f"Richtige Antwort: {correct_answer}",
            correct=is_correct,
            correct_answer=correct_answer,
        )

    def _grade_free_text_question(
        self,
        question: GeneratedExamQuestion,
        student_answer: str,
        verdict: dict,
    ) -> GradedExamQuestion:
        """Turn the LLM verdict for one free-text question into a graded result."""
        awarded = _clamp_points(verdict.get("awarded_points", 0), question.max_points)
        feedback = verdict.get("feedback") or ""
        if not student_answer:
            awarded = 0
            feedback = feedback or "Keine Antwort abgegeben."

        return GradedExamQuestion(
            question_id=question.id,
            kind="free_text",
            prompt=question.prompt,
            your_answer=student_answer,
            awarded_points=awarded,
            max_points=question.max_points,
            feedback=feedback,
            correct=None,
            correct_answer=question.expected,
        )

    def _grade_free_text(self, items: list[dict]) -> dict[str, dict]:
        """Ask the LLM to grade all free-text answers; tolerate grading failures."""
        if not items:
            return {}

        try:
            prompt = self.prompt_builder.build_exam_grading_prompt(items)
            response = self.llm_client.get_user_message(prompt)
            return self.grading_parser.parse(str(response or ""))
        except Exception:
            logger.exception("Failed to grade free-text exam answers")
            return {}
