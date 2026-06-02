# src/openbook/assistant/management/commands/ask_assistant.py
import sys
from django.core.management.base import BaseCommand
from openbook.assistant.services.client import AssistantClient, SNOW_FILE_PATH


class Command(BaseCommand):
    help = "Ermöglicht die LOKALE Interaktion mit Assistent"

    def handle(self, *args, **options):
        client = AssistantClient()
        file_path = input(
            f"Gib den Pfad zur Textdatei ein (Enter für '{SNOW_FILE_PATH}'): "
        ).strip()
        if not file_path:
            file_path = SNOW_FILE_PATH

        try:
            client.load_data(file_path)
            query = input("\nDeine Frage: ").strip()
            answer = client.perform_rag_query(query)
            self.stdout.write(self.style.SUCCESS(f"Antwort:\n{answer}"))
        except KeyboardInterrupt:
            self.stdout.write("\nAbbruch durch Benutzer.")
        except Exception as e:
            self.stderr.write(f"Fehler beim Laden der Datei: {e}")


# poetry run python src/manage.py ask_assistant
