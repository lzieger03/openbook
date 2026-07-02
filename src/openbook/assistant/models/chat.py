# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
# Ledejna Salihi (@LedejnaSalihi)
# Lars Zieger (@lzieger03)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from __future__ import annotations

from django.conf              import settings
from django.db                import models
from django.utils.translation import gettext_lazy as _

from openbook.core.models.mixins.uuid import UUIDMixin


class ChatSession(UUIDMixin):
    """
    A single saved conversation between one learner and the AI assistant, scoped to a
    course. A learner can have several sessions per course; each carries a short title
    (derived from the first message) and is shown in the chat sidebar.
    """

    user = models.ForeignKey(
        to           = settings.AUTH_USER_MODEL,
        verbose_name = _("User"),
        on_delete    = models.CASCADE,
        related_name = "chat_sessions",
    )

    course = models.ForeignKey(
        to           = "openbook_content.Course",
        verbose_name = _("Course"),
        on_delete    = models.CASCADE,
        related_name = "chat_sessions",
        null         = True,
        blank        = True,
    )

    title = models.CharField(
        verbose_name = _("Title"),
        max_length   = 120,
        blank        = True,
        default      = "",
    )

    created_at = models.DateTimeField(
        verbose_name = _("Created At"),
        auto_now_add = True,
    )

    updated_at = models.DateTimeField(
        verbose_name = _("Updated At"),
        auto_now     = True,
        db_index     = True,
    )

    class Meta:
        db_table            = "openbook_assistant_chat_session"
        verbose_name        = _("Chat Session")
        verbose_name_plural = _("Chat Sessions")
        ordering            = ["-updated_at"]
        indexes = [
            models.Index(fields=["user", "course", "-updated_at"]),
        ]

    def __str__(self):
        return self.title or f"Chat {self.pk}"


class ChatMessage(UUIDMixin):
    """
    One message inside a :class:`ChatSession`. Mirrors the fields of the WebSocket
    ``ChatMessagePayload`` so the stored history can be replayed to the client verbatim.
    """

    session = models.ForeignKey(
        to           = ChatSession,
        verbose_name = _("Session"),
        on_delete    = models.CASCADE,
        related_name = "messages",
    )

    sender = models.CharField(
        verbose_name = _("Sender"),
        max_length   = 16,
    )

    type = models.CharField(
        verbose_name = _("Type"),
        max_length   = 16,
        default      = "normal",
    )

    severity = models.CharField(
        verbose_name = _("Severity"),
        max_length   = 16,
        default      = "info",
    )

    format = models.CharField(
        verbose_name = _("Format"),
        max_length   = 16,
        default      = "markdown",
    )

    content = models.TextField(
        verbose_name = _("Content"),
        blank        = True,
        default      = "",
    )

    guard_rails = models.JSONField(
        verbose_name = _("Guard Rails"),
        blank        = True,
        default      = dict,
    )

    finished = models.BooleanField(
        verbose_name = _("Finished"),
        default      = True,
    )

    created_at = models.DateTimeField(
        verbose_name = _("Created At"),
        auto_now_add = True,
        db_index     = True,
    )

    class Meta:
        db_table            = "openbook_assistant_chat_message"
        verbose_name        = _("Chat Message")
        verbose_name_plural = _("Chat Messages")
        ordering            = ["created_at"]

    def __str__(self):
        return f"{self.sender}: {self.content[:40]}"
