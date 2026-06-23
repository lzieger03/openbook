# OpenBook: Interactive Online Textbooks - Server
# Copyright 2026 Sebastian Wolf, Daniel Sachada
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.test import SimpleTestCase

from openbook.assistant.services.quiz_generation import QuizResponseParser


class QuizResponseParser_Tests(SimpleTestCase):
    """Tests for generated quiz response parsing."""

    def test_parse_valid_quiz_json(self):
        """Valid quiz JSON should be converted into structured questions."""
        questions = QuizResponseParser().parse(
            """
            {
                "questions": [
                    {
                        "prompt": "What is HTML?",
                        "options": [
                            {"text": "Markup language", "correct": true},
                            {"text": "Database", "correct": false},
                            {"text": "Server", "correct": false},
                            {"text": "Image format", "correct": false}
                        ]
                    }
                ]
            }
            """
        )

        self.assertEqual(len(questions), 1)
        self.assertEqual(questions[0].prompt, "What is HTML?")
        self.assertTrue(questions[0].options[0].correct)

    def test_parse_rejects_questions_without_single_correct_answer(self):
        """Each generated question must have exactly one correct answer."""
        with self.assertRaisesMessage(ValueError, "exactly one correct"):
            QuizResponseParser().parse(
                """
                {
                    "questions": [
                        {
                            "prompt": "What is HTML?",
                            "options": [
                                {"text": "A", "correct": true},
                                {"text": "B", "correct": true},
                                {"text": "C", "correct": false},
                                {"text": "D", "correct": false}
                            ]
                        }
                    ]
                }
                """
            )
