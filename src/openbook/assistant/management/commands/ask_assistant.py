# OpenBook: Interactive Online Textbooks - Server
# © 2026 Sebastian Wolf, Daniel Sachadä
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# src/openbook/assistant/management/commands/ask_assistant.py
from django.core.management.base import BaseCommand
from openbook.assistant.services.llm_client import LLM_Client, SNOW_FILE_PATH


class Command(BaseCommand):
    help = "Ermöglicht die LOKALE Interaktion mit Assistent"

    def handle(self, *args, **options):
        llm_client = LLM_Client()
        file_path = input(
            f"Gib den Pfad zur Textdatei ein (Enter für '{SNOW_FILE_PATH}'): "
        ).strip()
        if not file_path:
            file_path = SNOW_FILE_PATH

        try:
            llm_client.load_data(file_path)

            while True:
                query = input("\nDeine Frage: ").strip()
                answer = llm_client.perform_rag_query(query)
                self.stdout.write(self.style.SUCCESS(f"Antwort:\n{answer}"))

        except KeyboardInterrupt:
            self.stdout.write("\nAbbruch durch Benutzer.")
        except Exception as e:
            self.stderr.write(f"Fehler beim Laden der Datei: {e}")


# poetry run python src/manage.py ask_assistant
