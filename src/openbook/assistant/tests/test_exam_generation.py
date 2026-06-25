# OpenBook: Interactive Online Textbooks - Server
# Copyright 2026 Sebastian Wolf, Daniel Sachada
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.test import SimpleTestCase

from openbook.assistant.services.exam_generation import (
    ExamGenerationParser,
    ExamGradingParser,
)


class ExamGenerationParser_Tests(SimpleTestCase):
    """Tests for parsing the AI-generated exam JSON."""

    def test_parses_mixed_questions(self):
        """A mix of free-text and multiple-choice questions is parsed and validated."""
        questions = ExamGenerationParser().parse(
            """
            ```json
            {
                "questions": [
                    {"kind": "free_text", "prompt": "Explain normalization.",
                     "max_points": 15, "expected": "Reduce redundancy ..."},
                    {"kind": "multiple_choice", "prompt": "What is a primary key?",
                     "max_points": 10, "options": [
                        {"text": "A unique row identifier", "correct": true},
                        {"text": "A foreign table", "correct": false},
                        {"text": "An index type", "correct": false},
                        {"text": "A constraint name", "correct": false}
                     ]}
                ]
            }
            ```
            """
        )

        self.assertEqual(len(questions), 2)

        free_text = questions[0]
        self.assertEqual(free_text.kind, "free_text")
        self.assertEqual(free_text.max_points, 15)
        self.assertTrue(free_text.expected)
        self.assertTrue(free_text.id)

        choice = questions[1]
        self.assertEqual(choice.kind, "multiple_choice")
        self.assertEqual(len(choice.options), 4)
        self.assertEqual(sum(1 for option in choice.options if option.correct), 1)

    def test_rejects_choice_without_single_correct_option(self):
        """A multiple-choice question needs exactly one correct option."""
        with self.assertRaises(ValueError):
            ExamGenerationParser().parse(
                """
                {"questions": [
                    {"kind": "multiple_choice", "prompt": "Pick one",
                     "options": [
                        {"text": "a", "correct": true},
                        {"text": "b", "correct": true}
                     ]}
                ]}
                """
            )

    def test_unknown_kind_falls_back_to_free_text(self):
        """A question without a recognized kind is treated as gradable free text."""
        questions = ExamGenerationParser().parse(
            '{"questions": [{"prompt": "Describe ACID.", "expected": "Atomicity ..."}]}'
        )
        self.assertEqual(questions[0].kind, "free_text")
        self.assertEqual(questions[0].max_points, 10)  # default points applied


class ExamGradingParser_Tests(SimpleTestCase):
    """Tests for parsing the AI grading verdict for free-text answers."""

    def test_parses_results_by_question_id(self):
        """The grading verdict is keyed by question id with points and feedback."""
        graded = ExamGradingParser().parse(
            """
            {"results": [
                {"question_id": "q1", "awarded_points": 12, "feedback": "Good, but ..."},
                {"question_id": "q2", "awarded_points": 0, "feedback": "Off topic."}
            ]}
            """
        )

        self.assertEqual(graded["q1"]["awarded_points"], 12)
        self.assertEqual(graded["q1"]["feedback"], "Good, but ...")
        self.assertEqual(graded["q2"]["awarded_points"], 0)

    def test_rejects_response_without_results_list(self):
        """A grading response must contain a results list."""
        with self.assertRaises(ValueError):
            ExamGradingParser().parse('{"foo": "bar"}')
