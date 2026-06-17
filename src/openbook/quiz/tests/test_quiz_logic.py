# OpenBook: Interactive Online Textbooks - Server
# © 2026 Sebastian Wolf, Daniel Sachadä
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

import os

from django.conf import settings
from django.test import TestCase

from openbook.quiz.quiz_logic import QuizManager, QuizQuestion


class QuizLogic_Tests(TestCase):
    """Tests for the pure Python quiz logic classes."""

    def test_quiz_question_creation(self):
        """QuizQuestion should be created with correct attributes."""
        q = QuizQuestion(
            question_text="Test?",
            choice_a="A",
            choice_b="B",
            choice_c="C",
            choice_d="D",
            correct_choice="C"
        )
        self.assertEqual(q.question_text, "Test?")
        self.assertEqual(q.get_choice_text("C"), "C")
        self.assertTrue(q.check_answer("C"))
        self.assertFalse(q.check_answer("A"))

    def test_quiz_manager_load(self):
        """QuizManager should successfully load questions from JSON."""
        json_path = os.path.join(settings.BASE_DIR, "openbook", "quiz", "data", "questions.json")
        manager = QuizManager(json_path)
        self.assertGreater(len(manager.questions), 0)

        q = manager.get_random_question()
        self.assertIsNotNone(q)
        self.assertIsNotNone(q.question_text)
