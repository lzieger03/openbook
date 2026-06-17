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


def rebuild_documents_vector_table(apps, schema_editor) -> None:
    """Rebuild the sqlite-vec index table with Django model identifiers."""
    if schema_editor.connection.vendor != "sqlite":
        return

    sqlite_connection = schema_editor.connection.connection
    sqlite_connection.enable_load_extension(True)
    try:
        sqlite_vec.load(sqlite_connection)
    finally:
        sqlite_connection.enable_load_extension(False)

    with schema_editor.connection.cursor() as cursor:
        cursor.execute(f"DROP TABLE IF EXISTS {DOCUMENTS_TABLE}")
        cursor.execute(
            f"""
            CREATE VIRTUAL TABLE {DOCUMENTS_TABLE} USING vec0(
                embedding float[1024],
                +document_id TEXT,
                +chunk_id TEXT,
                +position INTEGER
            )
            """
        )


def restore_legacy_documents_vector_table(apps, schema_editor) -> None:
    """Restore the sqlite-vec index schema created by migration 0001."""
    if schema_editor.connection.vendor != "sqlite":
        return

    sqlite_connection = schema_editor.connection.connection
    sqlite_connection.enable_load_extension(True)
    try:
        sqlite_vec.load(sqlite_connection)
    finally:
        sqlite_connection.enable_load_extension(False)

    with schema_editor.connection.cursor() as cursor:
        cursor.execute(f"DROP TABLE IF EXISTS {DOCUMENTS_TABLE}")
        cursor.execute(
            f"""
            CREATE VIRTUAL TABLE {DOCUMENTS_TABLE} USING vec0(
                embedding float[1024],
                +chunk_id INTEGER,
                +content TEXT
            )
            """
        )


class Migration(migrations.Migration):
    dependencies = [
        ("openbook_assistant", "0002_initial"),
    ]

    operations = [
        migrations.RunPython(
            rebuild_documents_vector_table,
            reverse_code=restore_legacy_documents_vector_table,
        ),
    ]
