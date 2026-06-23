# OpenBook: Interactive Online Textbooks - Server
# Copyright 2026 Sebastian Wolf, Daniel Sachada
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.test import SimpleTestCase

from openbook.assistant.services.prompt_builder import PromptBuilder


class PromptBuilder_Tests(SimpleTestCase):
    """Tests for assistant prompt construction."""

    def test_build_course_question_prompt_includes_contexts(self):
        """Course question prompts should include question, documents, and learning context."""
        prompt = PromptBuilder().build_course_question_prompt(
            query="Was ist HTML?",
            document_context="HTML ist eine Auszeichnungssprache.",
            learning_context="Zuletzt gelesene Seite: Grundlagen.",
        )

        self.assertIn("Was ist HTML?", prompt)
        self.assertIn("HTML ist eine Auszeichnungssprache.", prompt)
        self.assertIn("Zuletzt gelesene Seite: Grundlagen.", prompt)

    def test_build_quiz_generation_prompt_requests_json(self):
        """Quiz prompts should ask the model for structured JSON."""
        prompt = PromptBuilder().build_quiz_generation_prompt(
            document_context="HTML Grundlagen",
            course_context="Kurs: Web Basics",
            question_count=3,
        )

        self.assertIn("Erzeuge exakt 3 Multiple-Choice-Fragen", prompt)
        self.assertIn("HTML Grundlagen", prompt)
        self.assertIn("Kurs: Web Basics", prompt)
        self.assertIn("prompt", prompt)
        self.assertIn("options", prompt)
        self.assertIn("valide", prompt)
        self.assertIn("JSON", prompt)
