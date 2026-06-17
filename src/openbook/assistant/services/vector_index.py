# OpenBook: Interactive Online Textbooks - Server
# © 2026 Sebastian Wolf, Daniel Sachadä
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.db import connections
import sqlite_vec

DOCUMENTS_TABLE = "openbook_assistant_documents"

_sqlite_vec_connections = {}


def get_vector_connection(using: str = "default"):
    """Load sqlite-vec on the active Django database connection."""
    connection = connections[using]
    connection.ensure_connection()

    if connection.vendor != "sqlite":
        return None

    sqlite_connection = connection.connection
    if _sqlite_vec_connections.get(using) is sqlite_connection:
        return connection

    sqlite_connection.enable_load_extension(True)
    try:
        sqlite_vec.load(sqlite_connection)
    finally:
        sqlite_connection.enable_load_extension(False)

    _sqlite_vec_connections[using] = sqlite_connection
    return connection


def delete_document_vectors(document_id, using: str = "default") -> None:
    """Delete vector rows for one assistant document."""
    connection = get_vector_connection(using)
    if connection is None:
        return

    with connection.cursor() as cursor:
        cursor.execute(
            f"DELETE FROM {DOCUMENTS_TABLE} WHERE document_id = %s",
            [str(document_id)],
        )


def delete_course_vectors(course_id, using: str = "default") -> None:
    """Delete vector rows for one course."""
    connection = get_vector_connection(using)
    if connection is None:
        return

    with connection.cursor() as cursor:
        cursor.execute(
            f"DELETE FROM {DOCUMENTS_TABLE} WHERE course_id = %s",
            [str(course_id)],
        )


def delete_chunk_vector(chunk_id, using: str = "default") -> None:
    """Delete the vector row for one assistant document chunk."""
    connection = get_vector_connection(using)
    if connection is None:
        return

    with connection.cursor() as cursor:
        cursor.execute(
            f"DELETE FROM {DOCUMENTS_TABLE} WHERE chunk_id = %s",
            [str(chunk_id)],
        )
