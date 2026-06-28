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
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from openbook.content.models import Course
from openbook.content.models import CourseMaterial
from openbook.content.models import Textbook
from openbook.content.models import TextbookPage
from openbook.learning.models import LearningState
from openbook.learning.models import QuizResult

from .exam_generation import _clamp_points
from .exam_generation import ExamGenerationParser
from .exam_generation import ExamGradingParser
from .exam_generation import GeneratedExam
from .exam_generation import GeneratedExamQuestion
from .exam_generation import GradedExam
from .exam_generation import GradedExamQuestion
from .learning_context import LearningContextService
from .llm_client import LLM_Client
from .prompt_builder import PromptBuilder
from .quiz_generation import GeneratedQuiz
from .quiz_generation import QuizResponseParser

logger = logging.getLogger(__name__)


class AssistantOrchestrator:
    """Coordinate course-aware assistant chat requests."""

    COURSE_CONTEXT_LIMIT = 12000

    def __init__(
        self,
        llm_client: LLM_Client | None = None,
        learning_context_service: LearningContextService | None = None,
        prompt_builder: PromptBuilder | None = None,
        quiz_response_parser: QuizResponseParser | None = None,
        exam_generation_parser: ExamGenerationParser | None = None,
        exam_grading_parser: ExamGradingParser | None = None,
    ):
        self.llm_client = llm_client or LLM_Client()
        self.learning_context_service = learning_context_service or LearningContextService()
        self.prompt_builder = prompt_builder or PromptBuilder()
        self.quiz_response_parser = quiz_response_parser or QuizResponseParser()
        self.exam_generation_parser = exam_generation_parser or ExamGenerationParser()
        self.exam_grading_parser = exam_grading_parser or ExamGradingParser()

    def answer(
        self,
        query: str,
        user: AbstractUser | AnonymousUser | None = None,
        course: Course | UUID | str | None = None,
        context: str = "",
    ) -> str:
        """Generate an assistant answer for a global or course-scoped query.

        ``context`` is optional free-text describing what the user is currently looking
        at (e.g. the textbook page they are reading); it is added to the prompt so the
        Quick Chat can answer about the current page.
        """
        course_obj = self._resolve_course(course)
        self._check_chat_permission(user=user, course=course_obj)

        # Asking a question in a course chat earns a small (daily-capped) reward.
        if course_obj is not None:
            self._award_chat_question_reward(user=user, course=course_obj)

        context_block = self._page_context_block(context)

        if course_obj is None:
            return self.llm_client.get_user_message(f"{context_block}{query}")

        learning_context = self.learning_context_service.get_prompt_context(
            user=user,
            course=course_obj,
        )
        # The page context belongs in the generation context, not the retrieval query,
        # so RAG still retrieves on the user's actual question.
        if context_block:
            learning_context = f"{learning_context}\n\n{context_block}".strip()

        try:
            return self.llm_client.perform_rag_query(
                query,
                course=course_obj,
                learning_context=learning_context,
            )
        except RuntimeError as error:
            if str(error) in {
                "No global assistant documents have been indexed yet.",
                "No assistant documents have been indexed for this course yet.",
            }:
                return self.llm_client.get_user_message(f"{context_block}{query}")

            raise

    @staticmethod
    def _page_context_block(context: str) -> str:
        """Wrap the current-page context for inclusion in a prompt (capped in size)."""
        context = (context or "").strip()
        if not context:
            return ""

        # Cap so a very long page cannot blow up the prompt / token budget.
        max_length = 6000
        if len(context) > max_length:
            context = context[:max_length].rstrip() + "…"

        return (
            "The learner is currently looking at the following in the OpenBook app. "
            "Use it as context for their question when it is relevant:\n"
            f'"""\n{context}\n"""\n\n'
        )

    def record_page_opened(
        self,
        user: AbstractUser | AnonymousUser | None,
        course: Course | UUID | str,
        page: TextbookPage | UUID | str,
    ) -> LearningState:
        """Store that a user opened a course page."""
        course_obj = self._resolve_required_course(course)
        page_obj = self._resolve_page(page)
        self._check_chat_permission(user=user, course=course_obj)
        return self.learning_context_service.record_page_opened(
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
        course_obj = self._resolve_required_course(course)
        page_obj = self._resolve_page(page)
        self._check_chat_permission(user=user, course=course_obj)
        return self.learning_context_service.mark_page_completed(
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
        """
        Store the user's latest quiz result for a course page and award points.

        Returns a summary of what was granted (``points_awarded`` and the names of the
        ``skills_advanced``) so the caller can show immediate feedback to the learner.
        """
        course_obj = self._resolve_required_course(course)
        page_obj = self._resolve_page(page)
        self._check_chat_permission(user=user, course=course_obj)
        quiz_result = self.learning_context_service.record_quiz_result(
            user=user,
            course=course_obj,
            page=page_obj,
            score=score,
            attempts=attempts,
        )

        # Reward correct answers: course points (and the page's skills) scale with the
        # score, and only an improvement over the best previous score is paid out.
        reward = self._award_quiz_rewards(
            user=user,
            course=course_obj,
            page=page_obj,
            score=score,
        )

        return {
            "quiz_result":     quiz_result,
            "points_awarded":  reward.get("points_awarded", 0),
            "skills_advanced": reward.get("skills_advanced", []),
        }

    def generate_quiz(
        self,
        user: AbstractUser | AnonymousUser | None,
        course: Course | UUID | str,
        question_count: int = 5,
        textbook: Textbook | UUID | str | None = None,
    ) -> GeneratedQuiz:
        """
        Generate a course quiz from RAG documents or course content fallback.

        When ``textbook`` is given, the quiz is narrowed to that textbook (the learner
        picked it) and the result is anchored to the textbook's first page so points
        and skills can be awarded for it.
        """
        course_obj = self._resolve_required_course(course)
        self._check_chat_permission(user=user, course=course_obj)

        material = self._resolve_course_material(course=course_obj, textbook=textbook)

        question_count = max(1, min(int(question_count), 10))
        learning_context = self.learning_context_service.get_prompt_context(
            user=user,
            course=course_obj,
        )
        rag_context = self.llm_client.retrieve_rag_context(
            query=self._build_quiz_query(
                course=course_obj,
                question_count=question_count,
                material=material,
            ),
            course=course_obj,
            limit=5,
        )

        course_context = ""
        context_source = "rag_documents"

        if not rag_context.context:
            context_source = "course_context"
            course_context = self._build_course_context(course_obj, material=material)

        prompt = self.prompt_builder.build_quiz_generation_prompt(
            document_context=rag_context.context,
            course_context=course_context,
            learning_context=learning_context,
            question_count=question_count,
        )
        response = self.llm_client.get_user_message(prompt)

        anchor_page = self._anchor_page_for_material(material)

        return GeneratedQuiz(
            questions=self.quiz_response_parser.parse(str(response or "")),
            context_source=context_source,
            sources=rag_context.sources,
            textbook_id=str(material.textbook_id) if material else None,
            page_id=str(anchor_page.id) if anchor_page else None,
        )

    def generate_exam(
        self,
        user: AbstractUser | AnonymousUser | None,
        course: Course | UUID | str,
        question_count: int = 5,
        textbook: Textbook | UUID | str | None = None,
    ) -> GeneratedExam:
        """
        Generate a mixed free-text + multiple-choice exam **strictly** from the pages of
        the selected textbook.

        Unlike the quiz, the exam deliberately does not use course-wide RAG documents or
        other course content: it is built only from the authored text of the chosen
        textbook's pages, so the exam can never test anything outside that textbook. A
        textbook is therefore required, and the result is anchored to its first page so
        points and skills can be awarded.
        """
        course_obj = self._resolve_required_course(course)
        self._check_chat_permission(user=user, course=course_obj)

        material = self._resolve_course_material(course=course_obj, textbook=textbook)
        if material is None or not material.textbook_id:
            raise ValueError("An exam requires a textbook to be selected.")

        question_count = max(1, min(int(question_count), 10))

        # Context is exclusively the selected textbook's page content – nothing else.
        textbook_context = self._build_textbook_pages_context(material)
        if not textbook_context.strip():
            raise ValueError("The selected textbook has no page content to build an exam from.")

        prompt = self.prompt_builder.build_exam_generation_prompt(
            document_context="",
            course_context=textbook_context,
            learning_context="",
            question_count=question_count,
        )
        response = self.llm_client.get_user_message(prompt)

        anchor_page = self._anchor_page_for_material(material)

        return GeneratedExam(
            questions=self.exam_generation_parser.parse(str(response or "")),
            context_source="course_context",
            sources=(),
            textbook_id=str(material.textbook_id),
            page_id=str(anchor_page.id) if anchor_page else None,
        )

    def grade_exam(
        self,
        user: AbstractUser | AnonymousUser | None,
        course: Course | UUID | str,
        exam: GeneratedExam,
        answers: list[dict],
    ) -> dict[str, Any]:
        """
        Grade a submitted exam: multiple-choice locally, free text via the LLM.

        Awards course points and skill progress through the dedicated exam reward path
        (anchored to the textbook's first page), so the points show up in the course
        progress, the overall total and the course skills. Returns the graded exam
        together with the ``points_awarded`` and ``skills_advanced`` granted.
        """
        course_obj = self._resolve_required_course(course)
        self._check_chat_permission(user=user, course=course_obj)

        answer_by_id = {str(answer.get("question_id")): answer for answer in answers}

        # Grade the multiple-choice questions immediately; collect free text for the LLM.
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
                free_text_items.append({
                    "question_id": question.id,
                    "prompt": question.prompt,
                    "expected": question.expected,
                    "max_points": question.max_points,
                    "answer": student_answer,
                })

        verdicts = self._grade_free_text(free_text_items)
        for question in exam.questions:
            if question.kind != "multiple_choice":
                graded_by_id[question.id] = self._grade_free_text_question(
                    question,
                    student_answer=free_text_answers.get(question.id, ""),
                    verdict=verdicts.get(question.id, {}),
                )

        # Keep the graded questions in the exam's original order.
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

        # Award course points and skill progress via the dedicated exam reward path so
        # the points land in the course progress, the overall total and the skills.
        reward: dict[str, Any] = {"points_awarded": 0, "skills_advanced": []}
        if exam.page_id:
            reward = self._award_exam_rewards(
                user=user,
                course=course_obj,
                page=self._resolve_page(exam.page_id),
                score=score,
            )

        return {
            "graded_exam":     graded_exam,
            "points_awarded":  reward.get("points_awarded", 0),
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
            return self.exam_grading_parser.parse(str(response or ""))
        except Exception:
            # Grading is best-effort: if the LLM/parser fails, award zero with a notice
            # rather than failing the whole submission.
            logger.exception("Failed to grade free-text exam answers")
            return {}

    def _resolve_course_material(
        self,
        course: Course,
        textbook: Textbook | UUID | str | None,
    ) -> CourseMaterial | None:
        """Return the course material for a chosen textbook, or None for whole-course quizzes."""
        if textbook is None:
            return None

        textbook_id = textbook.pk if isinstance(textbook, Textbook) else textbook
        material = (
            CourseMaterial.objects
            .select_related("textbook")
            .filter(course=course, textbook_id=textbook_id)
            .first()
        )

        if material is None:
            raise ValueError("The selected textbook is not part of this course.")

        return material

    def _anchor_page_for_material(self, material: CourseMaterial | None) -> TextbookPage | None:
        """Return the first reading-order page of a material to anchor the quiz result to."""
        if material is None or not material.textbook_id:
            return None

        pages = self._pages_for_material(material)
        return pages[0] if pages else None

    def _award_chat_question_reward(
        self,
        user: AbstractUser | AnonymousUser | None,
        course: Course,
    ) -> None:
        """Grant the (daily-capped) chat reward for asking a course question."""
        if user is None or not getattr(user, "is_authenticated", False):
            return

        # Keep gamification a soft dependency: never let a reward error break chat.
        try:
            from openbook.gamification.services import award_chat_question_reward
        except ImportError:
            return

        try:
            award_chat_question_reward(account_id=user.pk, course_id=course.pk)
        except Exception:
            pass

    def _award_quiz_rewards(
        self,
        user: AbstractUser | AnonymousUser | None,
        course: Course,
        page: TextbookPage,
        score: float,
    ) -> dict[str, Any]:
        """
        Grant course points and skill progress for a quiz attempt on a page.

        Returns ``{"points_awarded": int, "skills_advanced": [skill names]}``; an empty
        award when the learner is anonymous or nothing new could be earned.
        """
        empty: dict[str, Any] = {"points_awarded": 0, "skills_advanced": []}

        if user is None or not getattr(user, "is_authenticated", False):
            return empty

        try:
            from openbook.gamification.models import Skill
            from openbook.gamification.services import award_quiz_rewards
        except ImportError:
            return empty

        # The quiz covers a whole textbook, so advance every skill that any page of that
        # textbook trains (deduplicated). A textbook-less page falls back to its own skills.
        skills = list(
            Skill.objects
            .filter(textbook_pages__textbook_id=page.textbook_id)
            .distinct()
        )
        skill_ids   = [skill.pk for skill in skills]
        skill_names = {str(skill.pk): skill.name for skill in skills}

        try:
            result = award_quiz_rewards(
                account_id = user.pk,
                course_id  = course.pk,
                page_id    = page.pk,
                score      = score,
                skill_ids  = skill_ids,
            )
        except Exception:
            # Never let a reward failure break recording the quiz result, but make the
            # failure visible in the logs instead of swallowing it silently.
            logger.exception(
                "Failed to award quiz rewards for account=%s course=%s page=%s",
                user.pk, course.pk, page.pk,
            )
            return empty

        advanced = result.get("skills_advanced", []) or []
        return {
            "points_awarded":  result.get("points_awarded", 0),
            "skills_advanced": [skill_names.get(str(skill_id), str(skill_id)) for skill_id in advanced],
        }

    def _award_exam_rewards(
        self,
        user: AbstractUser | AnonymousUser | None,
        course: Course,
        page: TextbookPage,
        score: float,
    ) -> dict[str, Any]:
        """
        Grant course points and skill progress for an exam attempt on a textbook.

        Mirrors :meth:`_award_quiz_rewards` but feeds the dedicated exam reward path, so
        exam points add to the course progress, the overall account total and the course
        skills independently of any quiz points. Returns ``{"points_awarded": int,
        "skills_advanced": [skill names]}`` (empty for anonymous users / nothing new).
        """
        empty: dict[str, Any] = {"points_awarded": 0, "skills_advanced": []}

        if user is None or not getattr(user, "is_authenticated", False):
            return empty

        try:
            from openbook.gamification.models import Skill
            from openbook.gamification.services import award_exam_rewards
        except ImportError:
            return empty

        # The exam covers the whole textbook, so advance every skill any of its pages
        # trains (deduplicated).
        skills = list(
            Skill.objects
            .filter(textbook_pages__textbook_id=page.textbook_id)
            .distinct()
        )
        skill_ids   = [skill.pk for skill in skills]
        skill_names = {str(skill.pk): skill.name for skill in skills}

        try:
            result = award_exam_rewards(
                account_id = user.pk,
                course_id  = course.pk,
                page_id    = page.pk,
                score      = score,
                skill_ids  = skill_ids,
            )
        except Exception:
            logger.exception(
                "Failed to award exam rewards for account=%s course=%s page=%s",
                user.pk, course.pk, page.pk,
            )
            return empty

        advanced = result.get("skills_advanced", []) or []
        return {
            "points_awarded":  result.get("points_awarded", 0),
            "skills_advanced": [skill_names.get(str(skill_id), str(skill_id)) for skill_id in advanced],
        }

    def _resolve_course(self, course: Course | UUID | str | None) -> Course | None:
        """Return a Course instance for supported course identifiers."""
        if course is None or isinstance(course, Course):
            return course

        return get_object_or_404(Course, pk=course)

    def _resolve_required_course(self, course: Course | UUID | str) -> Course:
        """Return a Course instance for learning-state mutations."""
        course_obj = self._resolve_course(course)
        if course_obj is None:
            raise ValueError("Course is required.")
        return course_obj

    def _resolve_page(self, page: TextbookPage | UUID | str) -> TextbookPage:
        """Return a TextbookPage instance for supported page identifiers."""
        if isinstance(page, TextbookPage):
            return page

        return get_object_or_404(TextbookPage, pk=page)

    def _check_chat_permission(
        self,
        user: AbstractUser | AnonymousUser | None,
        course: Course | None,
    ) -> None:
        """Require authentication and course view permission for course chat."""
        if user is None or not user.is_authenticated:
            raise PermissionDenied("You are not allowed to use the assistant.")

        if course is None:
            return

        if not user.has_perm("openbook_content.view_course", course):
            raise PermissionDenied("You are not allowed to use the assistant for this course.")

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

    def _build_course_context(self, course: Course, material: CourseMaterial | None = None) -> str:
        """
        Build fallback context from course metadata, skills and authored content.

        When ``material`` is given, only that textbook's content is included so the quiz
        stays focused on the textbook the learner selected.
        """
        parts = [f"Kurs: {course.name}"]

        if course.description.strip():
            parts.append(f"Kursbeschreibung:\n{course.description.strip()}")

        skills = list(course.skills.order_by("name"))
        if skills:
            parts.append(
                "Kompetenzen:\n"
                + "\n".join(
                    self._format_skill(skill)
                    for skill in skills
                )
            )

        if material is not None:
            materials = [material] if material.textbook_id else []
        else:
            materials = (
                course.materials.select_related("textbook")
                .prefetch_related("page_ranges")
                .order_by("position")
            )

        for material in materials:
            if not material.textbook_id:
                continue

            parts.append(f"Material: {material.textbook.name}")

            for page in self._pages_for_material(material):
                page_text = self._extract_page_text(page)
                if page_text:
                    parts.append(f"Seite: {page.name}\n{page_text}")

        return self._truncate_context("\n\n".join(parts))

    def _build_textbook_pages_context(self, material: CourseMaterial) -> str:
        """
        Build exam context from only the selected textbook's pages.

        Includes the textbook name and the authored text of each selected page – and
        nothing else (no course description, no other materials, no skills), so the exam
        is based purely on the content of the clicked textbook's pages.
        """
        parts = [f"Lehrbuch: {material.textbook.name}"]

        for page in self._pages_for_material(material):
            page_text = self._extract_page_text(page)
            if page_text:
                parts.append(f"Seite: {page.name}\n{page_text}")

        return self._truncate_context("\n\n".join(parts))

    def _format_skill(self, skill: Any) -> str:
        """Return one skill line for the fallback course context."""
        description = getattr(skill, "description", "")
        if isinstance(description, str) and description.strip():
            return f"- {skill.name}: {description.strip()}"
        return f"- {skill.name}"

    def _pages_for_material(self, material: CourseMaterial) -> list[TextbookPage]:
        """Return pages selected by a course material, in reading order."""
        pages = list(
            TextbookPage.objects.filter(textbook=material.textbook)
            .order_by("parent_id", "position", "name")
        )
        ordered_pages = self._reading_order(pages)
        page_ranges = list(
            material.page_ranges.select_related("start_page", "end_page")
            .order_by("position", "id")
        )

        if not page_ranges:
            return ordered_pages

        index_by_id = {page.id: index for index, page in enumerate(ordered_pages)}
        selected_pages = []
        seen_page_ids = set()

        for page_range in page_ranges:
            start_index = index_by_id.get(page_range.start_page_id)
            end_index = index_by_id.get(page_range.end_page_id)

            if start_index is None or end_index is None:
                continue

            first_index = min(start_index, end_index)
            last_index = max(start_index, end_index)

            for page in ordered_pages[first_index:last_index + 1]:
                if page.id not in seen_page_ids:
                    selected_pages.append(page)
                    seen_page_ids.add(page.id)

        return selected_pages

    def _reading_order(self, pages: list[TextbookPage]) -> list[TextbookPage]:
        """Flatten a textbook page tree roots-first in sibling position order."""
        by_parent_id = {}

        for page in pages:
            by_parent_id.setdefault(page.parent_id, []).append(page)

        for siblings in by_parent_id.values():
            siblings.sort(key=lambda page: (page.position, page.name))

        ordered = []

        def visit(parent_id):
            for page in by_parent_id.get(parent_id, []):
                ordered.append(page)
                visit(page.id)

        visit(None)

        if len(ordered) < len(pages):
            seen_page_ids = {page.id for page in ordered}
            ordered.extend(page for page in pages if page.id not in seen_page_ids)

        return ordered

    def _extract_page_text(self, page: TextbookPage) -> str:
        """Extract prompt-readable text from a textbook page."""
        parts = []

        if page.description.strip():
            parts.append(page.description.strip())

        content_text = self._extract_content_text(page.content)
        if content_text:
            parts.append(content_text)

        return "\n".join(parts).strip()

    def _extract_content_text(self, value: Any) -> str:
        """Extract text from the authored page content JSON tree."""
        if isinstance(value, str):
            return value.strip()

        if isinstance(value, list):
            return "\n".join(
                text
                for item in value
                if (text := self._extract_content_text(item))
            )

        if isinstance(value, dict):
            source = value.get("source")
            if isinstance(source, str):
                return source.strip()

            preferred_keys = ("text", "content", "children", "items", "value")
            preferred_text = [
                self._extract_content_text(value[key])
                for key in preferred_keys
                if key in value
            ]
            if preferred_text:
                return "\n".join(text for text in preferred_text if text)

            return "\n".join(
                text
                for item in value.values()
                if (text := self._extract_content_text(item))
            )

        return ""

    def _truncate_context(self, context: str) -> str:
        """Limit fallback context size before sending it to the LLM."""
        if len(context) <= self.COURSE_CONTEXT_LIMIT:
            return context

        return context[: self.COURSE_CONTEXT_LIMIT].rsplit("\n", 1)[0].strip()
