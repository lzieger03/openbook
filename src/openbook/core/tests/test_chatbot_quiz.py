# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from io                     import StringIO
from unittest.mock          import patch

from django.core.management import call_command
from django.test            import TestCase

from openbook.quiz.quiz_logic import QuizQuestion

class ChatbotQuiz_Command_Tests(TestCase):
    """Tests for the chatbot_quiz management command."""

    @patch("builtins.input", side_effect=["Q"])
    def test_quit_immediately(self, mock_input):
        """Command should exit immediately when user enters Q."""
        out = StringIO()
        call_command("chatbot_quiz", stdout=out)
        output = out.getvalue()
        self.assertIn("Willkommen", output)
        self.assertIn("Danke fürs Spielen", output)

    @patch("builtins.input", side_effect=["A", "N"])
    @patch("openbook.quiz.quiz_logic.QuizManager.get_random_question")
    def test_correct_answer_then_quit(self, mock_choice, mock_input):
        """Command should report correct answer, then exit when user enters N."""
        # Mock choice to return a predictable QuizQuestion
        mock_choice.return_value = QuizQuestion(
            question_text="Is 1+1=2?",
            choice_a="Yes",
            choice_b="No",
            choice_c="Maybe",
            choice_d="I don't know",
            correct_choice="A"
        )
        out = StringIO()
        call_command("chatbot_quiz", stdout=out)
        output = out.getvalue()
        self.assertIn("Is 1+1=2?", output)
        self.assertIn("Richtig! Richtig!", output)
        self.assertIn("Danke fürs Spielen", output)

    @patch("builtins.input", side_effect=["B", "N"])
    @patch("openbook.quiz.quiz_logic.QuizManager.get_random_question")
    def test_incorrect_answer_then_quit(self, mock_choice, mock_input):
        """Command should report incorrect answer and print correct option, then exit when user enters N."""
        mock_choice.return_value = QuizQuestion(
            question_text="Is 1+1=2?",
            choice_a="Yes",
            choice_b="No",
            choice_c="Maybe",
            choice_d="I don't know",
            correct_choice="A"
        )
        out = StringIO()
        call_command("chatbot_quiz", stdout=out)
        output = out.getvalue()
        self.assertIn("Is 1+1=2?", output)
        self.assertIn("Falsch! Die richtige Antwort war [A] Yes", output)
        self.assertIn("Danke fürs Spielen", output)
