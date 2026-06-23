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
        document_context: str = "",
        course_context: str = "",
        learning_context: str = "",
        question_count: int = 5,
    ) -> str:
        """Build a prompt for structured course quiz generation."""
        prompt_parts = [
            "Du bist ein Quizgenerator fuer einen OpenBook-Kurs.",
            f"Erzeuge exakt {question_count} Multiple-Choice-Fragen.",
            "Nutze vorrangig den Dokumentkontext.",
            "Wenn kein Dokumentkontext vorhanden ist, nutze den Kurskontext.",
            "Jede Frage muss vier Antwortoptionen haben.",
            "Genau eine Antwortoption pro Frage muss correct=true haben.",
            "Gib ausschliesslich valides JSON ohne Markdown-Codeblock zurueck.",
            (
                "Schema: {\"questions\":[{\"prompt\":\"...\","
                "\"options\":[{\"text\":\"...\",\"correct\":true},"
                "{\"text\":\"...\",\"correct\":false},"
                "{\"text\":\"...\",\"correct\":false},"
                "{\"text\":\"...\",\"correct\":false}]}]}"
            ),
        ]

        if learning_context:
            prompt_parts.append(
                "Beruecksichtige zusaetzlich diesen Lernstand des Nutzers:"
            )
            prompt_parts.append(learning_context)

        if document_context:
            prompt_parts.append(f"Dokumentkontext:\n{document_context}")

        if course_context:
            prompt_parts.append(f"Kurskontext:\n{course_context}")

        return "\n\n".join(prompt_parts).strip()
