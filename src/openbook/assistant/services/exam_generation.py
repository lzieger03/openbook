# OpenBook: Interactive Online Textbooks - Server
# Copyright 2026 Sebastian Wolf, Daniel Sachadä
# Ledejna Salihi (@LedejnaSalihi)
# Lars Zieger (@lzieger03)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

"""
Data structures and parsers for AI-generated and AI-graded course exams.

An exam mixes open free-text questions (graded by the LLM against a model answer)
and multiple-choice questions (graded by comparing the picked option). The model
answers and the ``correct`` flags are kept server-side and never sent to the client,
so the exam cannot be trivially solved by inspecting the payload.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
import re
from typing import Literal
from uuid import uuid4

from openbook.assistant.services.rag_client import RagSource


ExamContextSource = Literal["rag_documents", "course_context"]
ExamQuestionKind = Literal["free_text", "multiple_choice"]

# Points a single question is worth when the LLM does not specify a value.
DEFAULT_QUESTION_POINTS = 10
MAX_QUESTION_POINTS = 100


@dataclass(frozen=True)
class GeneratedExamOption:
    """One selectable answer of a multiple-choice exam question."""

    text: str
    correct: bool


@dataclass(frozen=True)
class GeneratedExamQuestion:
    """One generated exam question (free text or multiple choice)."""

    id: str
    kind: ExamQuestionKind
    prompt: str
    max_points: int
    # Free-text only: the model answer / rubric the LLM grades against (server-side).
    expected: str = ""
    # Multiple-choice only: the selectable options (with the correct flag, server-side).
    options: tuple[GeneratedExamOption, ...] = ()


@dataclass(frozen=True)
class GeneratedExam:
    """A structured exam generated from RAG documents or course context."""

    questions: tuple[GeneratedExamQuestion, ...]
    context_source: ExamContextSource
    sources: tuple[RagSource, ...] = ()
    # Optional textbook the exam was scoped to and the page the result anchors to.
    textbook_id: str | None = None
    page_id: str | None = None


@dataclass(frozen=True)
class GradedExamQuestion:
    """The grading outcome for a single exam question."""

    question_id: str
    kind: ExamQuestionKind
    prompt: str
    your_answer: str
    awarded_points: int
    max_points: int
    feedback: str
    # True/False for multiple choice; None for free text.
    correct: bool | None = None
    # The expected / correct answer, shown to the learner after grading.
    correct_answer: str = ""


@dataclass(frozen=True)
class GradedExam:
    """The full grading outcome of an exam attempt."""

    results: tuple[GradedExamQuestion, ...]
    total_points: int
    max_points: int
    score: float
    overall_feedback: str = ""


def _load_json_object(response: str) -> dict:
    """Load a JSON object, tolerating Markdown code fences around it."""
    cleaned = (response or "").strip()
    fence_match = re.search(r"```(?:json)?\s*(\{.*\})\s*```", cleaned, re.DOTALL)
    if fence_match:
        cleaned = fence_match.group(1)

    try:
        payload = json.loads(cleaned)
    except json.JSONDecodeError as error:
        raise ValueError("The exam response was not valid JSON.") from error

    if not isinstance(payload, dict):
        raise ValueError("The exam response must be a JSON object.")
    return payload


def _read_string(data: dict, key: str, *fallback_keys: str, required: bool = True) -> str:
    """Read a string field, optionally falling back to alternative keys."""
    value = data.get(key)
    for fallback in fallback_keys:
        if value is None:
            value = data.get(fallback)

    if not isinstance(value, str) or not value.strip():
        if required:
            raise ValueError(f"The exam response field {key} must be a non-empty string.")
        return ""

    return value.strip()


def _clamp_points(value: object, maximum: int) -> int:
    """Coerce a value into an integer point amount within ``0..maximum``."""
    try:
        points = int(value)
    except (TypeError, ValueError):
        points = 0
    return max(0, min(points, maximum))


class ExamGenerationParser:
    """Parse and validate the JSON shape returned by the exam generation prompt."""

    def parse(self, response: str) -> tuple[GeneratedExamQuestion, ...]:
        """Return normalized exam questions from a raw LLM response."""
        payload = _load_json_object(response)
        raw_questions = payload.get("questions")

        if not isinstance(raw_questions, list) or not raw_questions:
            raise ValueError("The exam response did not contain any questions.")

        return tuple(self._parse_question(raw) for raw in raw_questions)

    def _parse_question(self, raw: object) -> GeneratedExamQuestion:
        if not isinstance(raw, dict):
            raise ValueError("Every exam question must be a JSON object.")

        kind = raw.get("kind") or raw.get("type")
        prompt = _read_string(raw, "prompt", "question")
        max_points = _clamp_points(
            raw.get("max_points", DEFAULT_QUESTION_POINTS),
            MAX_QUESTION_POINTS,
        ) or DEFAULT_QUESTION_POINTS
        question_id = str(raw.get("id") or uuid4())

        if kind == "multiple_choice":
            options = self._parse_options(raw)
            return GeneratedExamQuestion(
                id=question_id,
                kind="multiple_choice",
                prompt=prompt,
                max_points=max_points,
                options=options,
            )

        # Anything that is not an explicit multiple-choice question is treated as free
        # text, so a slightly malformed "kind" still yields a usable, gradable question.
        expected = _read_string(raw, "expected", "answer", "model_answer", required=False)
        return GeneratedExamQuestion(
            id=question_id,
            kind="free_text",
            prompt=prompt,
            max_points=max_points,
            expected=expected,
        )

    def _parse_options(self, raw: dict) -> tuple[GeneratedExamOption, ...]:
        raw_options = raw.get("options", raw.get("answers"))
        if not isinstance(raw_options, list) or len(raw_options) < 2:
            raise ValueError("A multiple-choice question needs at least two options.")

        options = tuple(self._parse_option(option) for option in raw_options)
        if sum(1 for option in options if option.correct) != 1:
            raise ValueError("A multiple-choice question must have exactly one correct option.")

        return options

    def _parse_option(self, raw: object) -> GeneratedExamOption:
        if not isinstance(raw, dict):
            raise ValueError("Every multiple-choice option must be a JSON object.")

        text = _read_string(raw, "text")
        correct = raw.get("correct")
        if not isinstance(correct, bool):
            raise ValueError("Every multiple-choice option needs a boolean correct flag.")

        return GeneratedExamOption(text=text, correct=correct)


class ExamGradingParser:
    """Parse the JSON grading verdict the LLM returns for free-text answers."""

    def parse(self, response: str) -> dict[str, dict]:
        """Return a mapping of question id -> {awarded_points, feedback}."""
        payload = _load_json_object(response)
        raw_results = payload.get("results")

        if not isinstance(raw_results, list):
            raise ValueError("The grading response must contain a results list.")

        graded: dict[str, dict] = {}
        for raw in raw_results:
            if not isinstance(raw, dict):
                continue
            question_id = raw.get("question_id") or raw.get("id")
            if not question_id:
                continue
            graded[str(question_id)] = {
                "awarded_points": raw.get("awarded_points", raw.get("points", 0)),
                "feedback": _read_string(raw, "feedback", required=False),
            }

        return graded


# --- Persistence helpers (for saving/replaying exams) -----------------------------

def serialize_generated_exam(exam: GeneratedExam) -> dict:
    """Serialize a generated exam (incl. server-side answers) to a JSON-safe dict."""
    return {
        "context_source": exam.context_source,
        "textbook_id": exam.textbook_id,
        "page_id": exam.page_id,
        "questions": [
            {
                "id": question.id,
                "kind": question.kind,
                "prompt": question.prompt,
                "max_points": question.max_points,
                "expected": question.expected,
                "options": [
                    {"text": option.text, "correct": option.correct}
                    for option in question.options
                ],
            }
            for question in exam.questions
        ],
    }


def deserialize_generated_exam(data: dict) -> GeneratedExam:
    """Reconstruct a :class:`GeneratedExam` from :func:`serialize_generated_exam`."""
    questions = tuple(
        GeneratedExamQuestion(
            id=str(raw.get("id") or uuid4()),
            kind="multiple_choice" if raw.get("kind") == "multiple_choice" else "free_text",
            prompt=raw.get("prompt", ""),
            max_points=int(raw.get("max_points", 0) or 0),
            expected=raw.get("expected", "") or "",
            options=tuple(
                GeneratedExamOption(text=option.get("text", ""), correct=bool(option.get("correct")))
                for option in raw.get("options", [])
            ),
        )
        for raw in data.get("questions", [])
    )

    context_source = "rag_documents" if data.get("context_source") == "rag_documents" else "course_context"
    return GeneratedExam(
        questions=questions,
        context_source=context_source,
        textbook_id=data.get("textbook_id"),
        page_id=data.get("page_id"),
    )
