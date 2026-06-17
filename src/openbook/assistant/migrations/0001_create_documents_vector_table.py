# OpenBook: Interactive Online Textbooks - Server
# © 2026 Sebastian Wolf, Daniel Sachadä
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.db import migrations
import sqlite_vec

DOCUMENTS_TABLE = "openbook_assistant_documents"


def create_documents_vector_table(apps, schema_editor) -> None:
    """Create the sqlite-vec virtual table used by the assistant."""
    if schema_editor.connection.vendor != "sqlite":
        return

    sqlite_connection = schema_editor.connection.connection
    sqlite_connection.enable_load_extension(True)
    try:
        sqlite_vec.load(sqlite_connection)
    finally:
        sqlite_connection.enable_load_extension(False)

    with schema_editor.connection.cursor() as cursor:
        cursor.execute(
            f"""
            CREATE VIRTUAL TABLE IF NOT EXISTS {DOCUMENTS_TABLE} USING vec0(
                embedding float[1024],
                +chunk_id INTEGER,
                +content TEXT
            )
            """
        )


def drop_documents_vector_table(apps, schema_editor) -> None:
    """Drop the sqlite-vec virtual table used by the assistant."""
    if schema_editor.connection.vendor != "sqlite":
        return

    with schema_editor.connection.cursor() as cursor:
        cursor.execute(f"DROP TABLE IF EXISTS {DOCUMENTS_TABLE}")


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.RunPython(
            create_documents_vector_table,
            reverse_code=drop_documents_vector_table,
        ),
    ]
