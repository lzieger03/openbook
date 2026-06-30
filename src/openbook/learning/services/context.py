# OpenBook: Interactive Online Textbooks - Server
# Copyright 2026 Sebastian Wolf, Daniel Sachadä
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db.models import Q

from openbook.content.models import Course
from openbook.content.models import Textbook
from openbook.content.models import TextbookPage
from openbook.learning.models import LearningState
from openbook.learning.models import QuizResult


@dataclass(frozen=True)
class LearningPageSummary:
    """Summarize one textbook page for assistant context."""

    id: str
    name: str


@dataclass(frozen=True)
class LearningQuizSummary:
    """Summarize one quiz result for assistant context."""

    activity_type: str
    label: str
    page: LearningPageSummary | None
    score: float
    attempts: int


@dataclass(frozen=True)
class LearningGamificationSummary:
    """Summarize gamification values as part of learning context."""

    course_points: int | None = None
    course_level: int | None = None
    course_progress: Decimal | None = None


@dataclass(frozen=True)
class LearningContext:
    """Bundle learning progress data consumed by the assistant orchestrator."""

    last_page: LearningPageSummary | None
    completed_pages: tuple[LearningPageSummary, ...]
    quiz_results: tuple[LearningQuizSummary, ...]
    gamification: LearningGamificationSummary | None

    def as_prompt_context(self) -> str:
        """Render a compact German context block for the LLM prompt."""
        parts = []

        if self.last_page:
            parts.append(f"Zuletzt gelesene Seite: {self.last_page.name}.")

        if self.completed_pages:
            completed_names = ", ".join(page.name for page in self.completed_pages[:8])
            parts.append(f"Abgeschlossene Seiten: {completed_names}.")

        if self.quiz_results:
            weak_results = [
                result
                for result in self.quiz_results
                if result.score < 0.5
            ]
            if weak_results:
                weak_labels = ", ".join(result.label for result in weak_results[:5])
                parts.append(f"Schwache Übungsbereiche: {weak_labels}.")

        if self.gamification:
            gamification_parts = []
            if self.gamification.course_level is not None:
                gamification_parts.append(f"Kurslevel {self.gamification.course_level}")
            if self.gamification.course_points is not None:
                gamification_parts.append(f"{self.gamification.course_points} Kurspunkte")
            if self.gamification.course_progress is not None:
                gamification_parts.append(
                    f"{self.gamification.course_progress}% Kursfortschritt"
                )
            if gamification_parts:
                parts.append("Gamification: " + ", ".join(gamification_parts) + ".")

        return "\n".join(parts)


class LearningContextService:
    """Load learning progress for assistant prompts through one internal interface."""

    def get_context(self, user: AbstractUser, course: Course) -> LearningContext:
        """Return learning and gamification context for one user in one course."""
        learning_state = (
            LearningState.objects.filter(user=user, course=course)
            .select_related("last_page")
            .prefetch_related("completed_pages")
            .first()
        )

        quiz_results = (
            QuizResult.objects.filter(user=user)
            .filter(
                Q(course=course)
                | Q(page__textbook__used_in_courses__course=course)
            )
            .select_related("course", "textbook", "page")
            .order_by("-answered_at")
            .distinct()[:8]
        )

        return LearningContext(
            last_page=self._page_summary(learning_state.last_page)
            if learning_state and learning_state.last_page
            else None,
            completed_pages=tuple(
                self._page_summary(page)
                for page in learning_state.completed_pages.all()
            )
            if learning_state
            else (),
            quiz_results=tuple(
                LearningQuizSummary(
                    activity_type=result.activity_type,
                    label=self._activity_label(result),
                    page=self._page_summary(result.page),
                    score=result.score,
                    attempts=result.attempts,
                )
                for result in quiz_results
            ),
            gamification=self._get_gamification(user=user, course=course),
        )

    def get_prompt_context(self, user: AbstractUser, course: Course) -> str:
        """Return a prompt-ready learning context string."""
        return self.get_context(user=user, course=course).as_prompt_context()

    def record_page_opened(
        self,
        user: AbstractUser,
        course: Course,
        page: TextbookPage,
    ) -> LearningState:
        """Store the last opened page for a user in a course."""
        self._validate_page_in_course(page=page, course=course)
        learning_state = self._get_or_create_learning_state(user=user, course=course)
        learning_state.last_page = page
        learning_state.save(update_fields=["last_page", "last_accessed"])
        return learning_state

    def mark_page_completed(
        self,
        user: AbstractUser,
        course: Course,
        page: TextbookPage,
    ) -> LearningState:
        """Add a completed page to the user's learning state."""
        self._validate_page_in_course(page=page, course=course)
        learning_state = self._get_or_create_learning_state(user=user, course=course)
        learning_state.completed_pages.add(page)
        learning_state.save(update_fields=["last_accessed"])
        return learning_state

    def record_quiz_result(
        self,
        user: AbstractUser,
        course: Course,
        page: TextbookPage,
        score: float,
        attempts: int | None = None,
        metadata: dict | None = None,
    ) -> QuizResult:
        """Create or update the quiz result for a user on a course page."""
        return self.record_activity_result(
            user=user,
            course=course,
            activity_type=QuizResult.ActivityTypeChoices.QUIZ,
            page=page,
            score=score,
            attempts=attempts,
            metadata=metadata,
        )

    def record_exam_result(
        self,
        user: AbstractUser,
        course: Course,
        page: TextbookPage,
        score: float,
        attempts: int | None = None,
        metadata: dict | None = None,
    ) -> QuizResult:
        """Create or update the exam result for a user on a course page."""
        return self.record_activity_result(
            user=user,
            course=course,
            activity_type=QuizResult.ActivityTypeChoices.EXAM,
            page=page,
            score=score,
            attempts=attempts,
            metadata=metadata,
        )

    def record_activity_result(
        self,
        user: AbstractUser,
        course: Course,
        activity_type: str,
        score: float,
        page: TextbookPage | None = None,
        textbook: Textbook | None = None,
        attempts: int | None = None,
        metadata: dict | None = None,
    ) -> QuizResult:
        """Create or update the latest scored learning activity for a user."""
        self._validate_activity_type(activity_type=activity_type)
        self._validate_score(score=score)

        if page is not None:
            self._validate_page_in_course(page=page, course=course)
            textbook = page.textbook
            quiz_result, created = QuizResult.objects.get_or_create(
                user=user,
                page=page,
                activity_type=activity_type,
                defaults={
                    "course": course,
                    "textbook": textbook,
                    "score": score,
                    "attempts": attempts or 1,
                    "metadata": metadata or {},
                },
            )
        else:
            if textbook is not None:
                self._validate_textbook_in_course(textbook=textbook, course=course)
            quiz_result = (
                QuizResult.objects.filter(
                    user=user,
                    course=course,
                    page__isnull=True,
                    activity_type=activity_type,
                )
                .order_by("-answered_at")
                .first()
            )
            created = quiz_result is None
            if created:
                quiz_result = QuizResult.objects.create(
                    user=user,
                    course=course,
                    textbook=textbook,
                    page=None,
                    activity_type=activity_type,
                    score=score,
                    attempts=attempts or 1,
                    metadata=metadata or {},
                )

        if created:
            return quiz_result

        quiz_result.course = course
        quiz_result.textbook = textbook
        quiz_result.score = score
        quiz_result.attempts = attempts if attempts is not None else quiz_result.attempts + 1
        update_fields = ["course", "textbook", "score", "attempts", "answered_at"]

        if metadata is not None:
            quiz_result.metadata = metadata
            update_fields.append("metadata")

        quiz_result.save(update_fields=update_fields)
        return quiz_result

    def _page_summary(self, page: TextbookPage | None) -> LearningPageSummary | None:
        """Return the compact representation used in prompt context."""
        if page is None:
            return None

        return LearningPageSummary(
            id=str(page.id),
            name=page.name,
        )

    def _activity_label(self, result: QuizResult) -> str:
        """Return a compact label for prompt context."""
        if result.page_id and result.page:
            return result.page.name
        if result.textbook_id and result.textbook:
            return f"{result.get_activity_type_display()} ({result.textbook.name})"
        return str(result.get_activity_type_display())

    def _get_gamification(
        self,
        user: AbstractUser,
        course: Course,
    ) -> LearningGamificationSummary | None:
        """Read gamification through the learning context boundary."""
        try:
            from openbook.gamification.models import CourseProgress
        except ImportError:
            return None

        course_progress = CourseProgress.objects.filter(
            account=user,
            course=course,
        ).first()
        if not course_progress:
            return None

        return LearningGamificationSummary(
            course_points=course_progress.course_points,
            course_level=course_progress.course_level,
            course_progress=course_progress.course_progress,
        )

    def _get_or_create_learning_state(
        self,
        user: AbstractUser,
        course: Course,
    ) -> LearningState:
        """Return the user's learning state, creating it when needed."""
        learning_state, _ = LearningState.objects.get_or_create(
            user=user,
            course=course,
        )
        return learning_state

    def _validate_page_in_course(self, page: TextbookPage, course: Course) -> None:
        """Require the page's textbook to be part of the course material."""
        if page.textbook.used_in_courses.filter(course=course).exists():
            return

        raise ValidationError(
            "The page does not belong to the given course.",
            code="page_not_in_course",
        )

    def _validate_textbook_in_course(self, textbook: Textbook, course: Course) -> None:
        """Require the textbook to be part of the course material."""
        if textbook.used_in_courses.filter(course=course).exists():
            return

        raise ValidationError(
            "The textbook does not belong to the given course.",
            code="textbook_not_in_course",
        )

    def _validate_score(self, score: float) -> None:
        """Require normalized learning activity scores."""
        if 0.0 <= score <= 1.0:
            return

        raise ValidationError(
            "Activity score must be between 0.0 and 1.0.",
            code="invalid_activity_score",
        )

    def _validate_activity_type(self, activity_type: str) -> None:
        """Require a supported learning activity type."""
        if activity_type in QuizResult.ActivityTypeChoices.values:
            return

        raise ValidationError(
            "Unknown learning activity type.",
            code="invalid_activity_type",
        )
