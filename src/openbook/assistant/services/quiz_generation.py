# OpenBook: Interactive Online Textbooks - Server
# Copyright 2026 Sebastian Wolf, Daniel Sachadä
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
import json
import re
from typing import Literal
from uuid import uuid4

from openbook.assistant.services.rag_client import RagSource


QuizContextSource = Literal["rag_documents", "course_context"]


@dataclass(frozen=True)
class GeneratedQuizOption:
    """One selectable answer in a generated quiz question."""

    text: str
    correct: bool


@dataclass(frozen=True)
class GeneratedQuizQuestion:
    """One generated multiple-choice quiz question."""

    prompt: str
    options: tuple[GeneratedQuizOption, ...]
    id: str = field(default_factory=lambda: str(uuid4()))


@dataclass(frozen=True)
class GeneratedQuiz:
    """Structured quiz generated from RAG documents or course context."""

    questions: tuple[GeneratedQuizQuestion, ...]
    context_source: QuizContextSource
    sources: tuple[RagSource, ...] = ()
    # Optional textbook the quiz was scoped to and the page the result anchors to.
    textbook_id: str | None = None
    page_id: str | None = None


@dataclass(frozen=True)
class GradedQuizQuestion:
    """The grading outcome for one generated quiz question."""

    question_id: str
    prompt: str
    selected_index: int | None
    correct_index: int
    correct: bool
    correct_answer: str


@dataclass(frozen=True)
class GradedQuiz:
    """The full grading outcome of a generated quiz attempt."""

    results: tuple[GradedQuizQuestion, ...]
    correct_count: int
    question_count: int
    score: float


class QuizResponseParser:
    """Parse and validate the JSON shape returned by the LLM quiz prompt."""

    def parse(self, response: str) -> tuple[GeneratedQuizQuestion, ...]:
        """Return normalized quiz questions from a raw LLM response."""
        payload = self._load_json(response)
        raw_questions = payload.get("questions")

        if not isinstance(raw_questions, list) or not raw_questions:
            raise ValueError("The quiz response did not contain any questions.")

        questions = tuple(
            self._parse_question(raw_question)
            for raw_question in raw_questions
        )
        return questions

    def _load_json(self, response: str) -> dict:
        """Load a JSON object, tolerating Markdown code fences around it."""
        cleaned = response.strip()
        fence_match = re.search(r"```(?:json)?\s*(\{.*\})\s*```", cleaned, re.DOTALL)
        if fence_match:
            cleaned = fence_match.group(1)

        try:
            payload = json.loads(cleaned)
        except json.JSONDecodeError as error:
            raise ValueError("The quiz response was not valid JSON.") from error

        if not isinstance(payload, dict):
            raise ValueError("The quiz response must be a JSON object.")
        return payload

    def _parse_question(self, raw_question: object) -> GeneratedQuizQuestion:
        """Parse and validate one question object."""
        if not isinstance(raw_question, dict):
            raise ValueError("Every quiz question must be a JSON object.")

        prompt = self._read_string(raw_question, "prompt", fallback_key="question")
        raw_options = raw_question.get("options", raw_question.get("answers"))

        if not isinstance(raw_options, list) or len(raw_options) != 4:
            raise ValueError("Every quiz question must contain exactly four answers.")

        options = tuple(self._parse_option(raw_option) for raw_option in raw_options)
        correct_count = sum(1 for option in options if option.correct)

        if correct_count != 1:
            raise ValueError("Every quiz question must contain exactly one correct answer.")

        return GeneratedQuizQuestion(prompt=prompt, options=options)

    def _parse_option(self, raw_option: object) -> GeneratedQuizOption:
        """Parse and validate one answer option object."""
        if not isinstance(raw_option, dict):
            raise ValueError("Every quiz answer must be a JSON object.")

        text = self._read_string(raw_option, "text")
        correct = raw_option.get("correct")

        if not isinstance(correct, bool):
            raise ValueError("Every quiz answer must define a boolean correct flag.")

        return GeneratedQuizOption(text=text, correct=correct)

    def _read_string(
        self,
        data: dict,
        key: str,
        fallback_key: str | None = None,
    ) -> str:
        """Read a required non-empty string field."""
        value = data.get(key)
        if value is None and fallback_key is not None:
            value = data.get(fallback_key)

        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"The quiz response field {key} must be a non-empty string.")

        return value.strip()


def serialize_generated_quiz(quiz: GeneratedQuiz) -> dict:
    """Serialize a generated quiz including server-side correct answers."""
    return {
        "context_source": quiz.context_source,
        "textbook_id": quiz.textbook_id,
        "page_id": quiz.page_id,
        "questions": [
            {
                "id": question.id,
                "prompt": question.prompt,
                "options": [
                    {
                        "text": option.text,
                        "correct": option.correct,
                    }
                    for option in question.options
                ],
            }
            for question in quiz.questions
        ],
    }


def deserialize_generated_quiz(data: dict) -> GeneratedQuiz:
    """Reconstruct a generated quiz from :func:`serialize_generated_quiz`."""
    questions = tuple(
        GeneratedQuizQuestion(
            id=str(raw.get("id") or uuid4()),
            prompt=raw.get("prompt", "") or "",
            options=tuple(
                GeneratedQuizOption(
                    text=option.get("text", "") or "",
                    correct=bool(option.get("correct")),
                )
                for option in raw.get("options", [])
            ),
        )
        for raw in data.get("questions", [])
    )

    context_source = (
        "rag_documents"
        if data.get("context_source") == "rag_documents"
        else "course_context"
    )
    return GeneratedQuiz(
        questions=questions,
        context_source=context_source,
        textbook_id=data.get("textbook_id"),
        page_id=data.get("page_id"),
    )
