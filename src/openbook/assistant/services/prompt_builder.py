# OpenBook: Interactive Online Textbooks - Server
# Copyright 2026 Sebastian Wolf, Daniel Sachada
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from __future__ import annotations

import json


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

    def build_exam_generation_prompt(
        self,
        document_context: str = "",
        course_context: str = "",
        learning_context: str = "",
        question_count: int = 5,
    ) -> str:
        """Build a prompt for a mixed free-text + multiple-choice exam."""
        prompt_parts = [
            "Du bist ein Pruefungsgenerator fuer einen OpenBook-Kurs.",
            f"Erzeuge exakt {question_count} Pruefungsfragen.",
            "Mische offene Freitextfragen (kind=\"free_text\") und "
            "Multiple-Choice-Fragen (kind=\"multiple_choice\").",
            "Strebe etwa die Haelfte Freitext und die Haelfte Multiple-Choice an.",
            "Stelle die Fragen AUSSCHLIESSLICH zum bereitgestellten Kurskontext "
            "(dem Inhalt der Lehrbuchseiten).",
            "Verwende keinerlei Wissen ausserhalb dieses Kontexts und erfinde keine "
            "Inhalte. Jede Frage und jede Loesung muss sich allein aus dem Kontext "
            "beantworten lassen.",
            "Jede Frage braucht ein Feld max_points (ganze Zahl zwischen 5 und 20).",
            "Freitextfragen brauchen ein Feld expected mit einer kurzen Musterloesung.",
            "Multiple-Choice-Fragen brauchen vier options; genau eine mit correct=true.",
            "Gib ausschliesslich valides JSON ohne Markdown-Codeblock zurueck.",
            (
                "Schema: {\"questions\":["
                "{\"kind\":\"free_text\",\"prompt\":\"...\",\"max_points\":10,"
                "\"expected\":\"...\"},"
                "{\"kind\":\"multiple_choice\",\"prompt\":\"...\",\"max_points\":10,"
                "\"options\":[{\"text\":\"...\",\"correct\":true},"
                "{\"text\":\"...\",\"correct\":false},"
                "{\"text\":\"...\",\"correct\":false},"
                "{\"text\":\"...\",\"correct\":false}]}"
                "]}"
            ),
        ]

        if learning_context:
            prompt_parts.append("Beruecksichtige zusaetzlich diesen Lernstand des Nutzers:")
            prompt_parts.append(learning_context)

        if document_context:
            prompt_parts.append(f"Dokumentkontext:\n{document_context}")

        if course_context:
            prompt_parts.append(f"Kurskontext:\n{course_context}")

        return "\n\n".join(prompt_parts).strip()

    def build_exam_grading_prompt(self, items: list[dict]) -> str:
        """
        Build a prompt to grade free-text exam answers.

        ``items`` is a list of ``{"id", "prompt", "expected", "max_points", "answer"}``
        dicts. The LLM returns, for each question, an ``awarded_points`` value (0..max)
        and a short ``feedback`` string explaining the grade.
        """
        prompt_parts = [
            "Du bist ein fairer Pruefer und bewertest Freitextantworten eines Lernenden.",
            "Vergib fuer jede Frage Punkte zwischen 0 und dem jeweiligen max_points-Wert.",
            "Orientiere dich an der Musterloesung (expected), erlaube aber sinngemaesse "
            "und gleichwertige Formulierungen.",
            "Schreibe ein kurzes, konstruktives Feedback (1-2 Saetze) auf Deutsch.",
            "Gib ausschliesslich valides JSON ohne Markdown-Codeblock zurueck.",
            (
                "Schema: {\"results\":[{\"question_id\":\"...\","
                "\"awarded_points\":0,\"feedback\":\"...\"}]}"
            ),
            "Zu bewertende Antworten:",
            json.dumps(items, ensure_ascii=False),
        ]

        return "\n\n".join(prompt_parts).strip()
