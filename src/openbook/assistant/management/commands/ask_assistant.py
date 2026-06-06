# OpenBook: Interactive Online Textbooks - Server
# Copyright 2026 Sebastian Wolf, Daniel Sachada
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.core.management.base import BaseCommand

from openbook.assistant.models import AssistantDocument
from openbook.assistant.models import AssistantDocumentChunk
from openbook.assistant.services.llm_client import LLM_Client


class Command(BaseCommand):
    help = "Lokaler Assistenten-Chat mit bereits indexierten Admin-Uploads."

    def handle(self, *args, **options):
        document_count = AssistantDocument.objects.count()
        chunk_count = AssistantDocumentChunk.objects.count()

        if chunk_count == 0:
            self.stderr.write(
                "Keine indexierten Assistant-Dokumente gefunden. "
                "Bitte zuerst eine Textdatei im Django Admin hochladen."
            )
            return

        self.stdout.write(
            f"Nutze {chunk_count} indexierte Chunks aus {document_count} Dokument(en)."
        )

        try:
            llm_client = LLM_Client()

            while True:
                query = input("\nDeine Frage: ").strip()
                if not query:
                    continue

                answer = llm_client.perform_rag_query(query)
                self.stdout.write(self.style.SUCCESS(f"Antwort:\n{answer}"))

        except KeyboardInterrupt:
            self.stdout.write("\nAbbruch durch Benutzer.")
        except Exception as error:
            self.stderr.write(f"Assistenten-Abfrage fehlgeschlagen: {error}")


# poetry run python src/manage.py ask_assistant
