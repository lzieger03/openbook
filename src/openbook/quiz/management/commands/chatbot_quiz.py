# OpenBook: Interactive Online Textbooks - Server
# © 2026 Sebastian Wolf, Daniel Sachadä
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

import os

from django.conf                 import settings
from django.core.management.base import BaseCommand

from openbook.quiz.quiz_logic    import QuizManager


class Command(BaseCommand):
    help = "Runs an interactive terminal-based quiz chatbot using random questions from a JSON file."

    def handle(self, *args, **options):
        # Locate the questions.json file using settings.BASE_DIR
        json_path = os.path.join(settings.BASE_DIR, "openbook", "quiz", "data", "questions.json")

        try:
            manager = QuizManager(json_path)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error initializing QuizManager: {e}"))
            return

        if not manager.questions:
            self.stdout.write(self.style.WARNING("No questions found in questions.json."))
            return

        self.stdout.write(self.style.SUCCESS("=== Willkommen beim OpenBook Quiz ChatBot! ==="))
        self.stdout.write("Beantworte die Fragen oder gib 'Q' ein, um das Quiz zu beenden.\n")

        while True:
            q = manager.get_random_question()
            if not q:
                break

            self.stdout.write(self.style.WARNING(f"\nFrage: {q.question_text}"))
            self.stdout.write(f"[A] {q.choice_a}")
            self.stdout.write(f"[B] {q.choice_b}")
            self.stdout.write(f"[C] {q.choice_c}")
            self.stdout.write(f"[D] {q.choice_d}")

            user_input = ""
            while user_input not in ["A", "B", "C", "D", "Q"]:
                try:
                    user_input = input("\nDeine Antwort (A/B/C/D) oder Q zum Beenden: ").strip().upper()
                except (KeyboardInterrupt, EOFError):
                    user_input = "Q"
                    break

            if user_input == "Q":
                self.stdout.write(self.style.SUCCESS("\nDanke fürs Spielen! Auf Wiedersehen!\n"))
                break

            if q.check_answer(user_input):
                self.stdout.write(self.style.SUCCESS("Richtig! Richtig! 🥳\n"))
            else:
                correct_text = q.get_choice_text(q.correct_choice)
                self.stdout.write(self.style.ERROR(f"Falsch! Die richtige Antwort war [{q.correct_choice}] {correct_text}. 😢\n"))

            # Ask if the user wants to play again
            try:
                again = input("Nächste Frage? (J/N): ").strip().upper()
            except (KeyboardInterrupt, EOFError):
                again = "N"

            if again not in ["J", "JA", "Y", "YES"]:
                self.stdout.write(self.style.SUCCESS("\nDanke fürs Spielen! Auf Wiedersehen!\n"))
                break
