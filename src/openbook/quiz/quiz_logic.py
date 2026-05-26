# OpenBook: Interactive Online Textbooks - Server
# © 2026 Sebastian Wolf
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

import json
import os
import random


class QuizQuestion:
    """
    A simple Python class representing a single quiz question,
    used to load questions from a JSON database.
    """

    def __init__(
        self, question_text, choice_a, choice_b, choice_c, choice_d, correct_choice
    ):
        self.question_text = question_text
        self.choice_a = choice_a
        self.choice_b = choice_b
        self.choice_c = choice_c
        self.choice_d = choice_d
        self.correct_choice = correct_choice.upper()

    def get_choice_text(self, choice_letter):
        """Returns the text for the given choice letter (A, B, C, D)."""
        letter = choice_letter.upper()
        if letter == "A":
            return self.choice_a
        elif letter == "B":
            return self.choice_b
        elif letter == "C":
            return self.choice_c
        elif letter == "D":
            return self.choice_d
        return ""

    def check_answer(self, user_answer):
        """Checks if the user's answer (A, B, C, D) is correct."""
        return user_answer.upper() == self.correct_choice


class QuizManager:
    """
    Manages loading and choosing questions from a JSON file.
    """

    def __init__(self, json_path):
        self.json_path = json_path
        self.questions = []
        self.load_questions()

    def load_questions(self):
        """Loads questions from the JSON file."""
        if not os.path.exists(self.json_path):
            raise FileNotFoundError(
                f"Questions JSON file not found at: {self.json_path}"
            )

        with open(self.json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.questions = [
            QuizQuestion(
                question_text=q["question_text"],
                choice_a=q["choice_a"],
                choice_b=q["choice_b"],
                choice_c=q["choice_c"],
                choice_d=q["choice_d"],
                correct_choice=q["correct_choice"],
            )
            for q in data
        ]

    def get_random_question(self):
        """Returns a random QuizQuestion or None if no questions are loaded."""
        if not self.questions:
            return None
        return random.choice(self.questions)
