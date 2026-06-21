# OpenBook: Interactive Online Textbooks - Server
# Copyright 2026 Sebastian Wolf, Daniel Sachada
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from __future__ import annotations


class PromptBuilder:
    """Build LLM prompts for assistant workflows."""

    def build_course_question_prompt(
        self,
        query: str,
        document_context: str,
        learning_context: str = "",
    ) -> str:
        """Build a prompt for answering a course or global assistant question."""
        prompt_parts = [
            "Du bist ein hilfreicher Assistent.",
            "Beantworte die folgende Frage basierend auf dem Dokumentkontext.",
        ]

        if learning_context:
            prompt_parts.append(
                "Beruecksichtige zusaetzlich diesen Lernstand des Nutzers:"
            )
            prompt_parts.append(learning_context)

        prompt_parts.append(f"Dokumentkontext:\n{document_context}")
        prompt_parts.append(f"Frage: {query}")
        return "\n\n".join(prompt_parts).strip()

    def build_quiz_generation_prompt(
        self,
        document_context: str,
        learning_context: str = "",
        question_count: int = 5,
    ) -> str:
        """Build a prompt for future structured quiz generation."""
        prompt_parts = [
            "Du bist ein Quizgenerator fuer einen OpenBook-Kurs.",
            f"Erzeuge {question_count} Multiple-Choice-Fragen aus dem Dokumentkontext.",
            "Gib ausschliesslich valides JSON zurueck.",
            (
                "Schema: {\"questions\":[{\"question\":\"...\","
                "\"answers\":[{\"text\":\"...\",\"correct\":true}]}]}"
            ),
        ]

        if learning_context:
            prompt_parts.append(
                "Beruecksichtige zusaetzlich diesen Lernstand des Nutzers:"
            )
            prompt_parts.append(learning_context)

        prompt_parts.append(f"Dokumentkontext:\n{document_context}")
        return "\n\n".join(prompt_parts).strip()
