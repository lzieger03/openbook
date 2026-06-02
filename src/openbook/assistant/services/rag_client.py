# OpenBook: Interactive Online Textbooks - Server
# © 2026 Sebastian Wolf, Daniel Sachadä
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.conf import settings

try:  # Drop-In replacement für SQLite 3 aufgrund von MacOS Problemen mit Loadable Extensions
    import sqlean as sqlite3
except ImportError:
    import sqlite3
import sqlite_vec
from sqlite_vec import serialize_float32
from .client import AssistantClient, SNOW_FILE_PATH

DB_PATH = settings.BASE_DIR / "db.sqlite3"


class RagClient:
    def __init__(self):
        self.assistant = AssistantClient()
        self.text_data = None

        # Setup SQLite connection
        self.db = sqlite3.connect(str(DB_PATH), check_same_thread=False)
        try:
            self.db.enable_load_extension(True)
            sqlite_vec.load(self.db)
            self.db.enable_load_extension(False)
            self.db.execute("""
                CREATE VIRTUAL TABLE IF NOT EXISTS documents USING vec0(
                    embedding float[1024],
                    +chunk_id INTEGER,
                    +content TEXT
                )
            """)
            self.db.commit()
        except AttributeError:
            print(
                "Warning: sqlite3 does not support enable_load_extension. SQLite Vec cannot be loaded.",
                flush=True,
            )
        except sqlite3.OperationalError as e:
            print(f"Failed to create virtual table: {e}", flush=True)

    def load_data(self, file_path: str = SNOW_FILE_PATH):
        """Lädt Datei in SQLite-Datenbank als Vektoren."""
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Check if already loaded
        count_res = self.db.execute("SELECT count(*) FROM documents").fetchone()
        if count_res and count_res[0] > 0:
            if file_path:
                print(
                    "Datei bereits in Datenbank.",
                    flush=True,
                )
                self.db.execute("DELETE FROM documents")
                print("Datenbank geleert. Neue Datei wird geladen...", flush=True)
                print(self.db.execute("SELECT count(*) FROM documents").fetchone())
            else:
                self.text_data = content
                return

        # Vektorisieren und in SQLite einfügen
        chunks = self._chunk_text(content)
        for i, chunk in enumerate(chunks):
            embedding = self.assistant.get_embedding(chunk)
            self.db.execute(
                "INSERT INTO documents (embedding, chunk_id, content) VALUES (?, ?, ?)",
                (serialize_float32(embedding), i, chunk),
            )
        self.db.commit()
        self.text_data = content

    def perform_rag_query(self, query: str):
        """Führe eine RAG-Abfrage mittels Embeddings in SQLite durch."""
        if not self.text_data:
            self.load_data()

        query_embedding = self.assistant.get_embedding(query)

        rows = self.db.execute(
            """
            SELECT
                chunk_id,
                content,
                distance
            FROM documents
            WHERE embedding MATCH ?
            ORDER BY distance
            LIMIT 3
            """,
            [serialize_float32(query_embedding)],
        ).fetchall()

        top_contexts = [row[1] for row in rows]
        context = "\n\n".join(top_contexts)

        prompt = f"""
            Du bist ein hilfreicher Assistent.
            Beantworte die folgende Frage basierend auf diesem Kontext:
            \n\n{context}\n\nFrage: {query}
        """.strip()
        return self.assistant.get_user_message(prompt)

    def _chunk_text(
        self, text: str, chunk_size: int = 1000, overlap: int = 200
    ) -> list[str]:
        """Chunks text in multiple Größen von max. 1000"""
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunks.append(text[start:end])
            start += chunk_size - overlap
        return chunks
