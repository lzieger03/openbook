# OpenBook: Interactive Online Textbooks
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from __future__ import annotations

import asyncio

from chanx.channels.websocket import AsyncJsonWebsocketConsumer
from chanx.core.decorators    import channel, ws_handler
from chanx.messages.incoming  import PingMessage
from chanx.messages.outgoing  import PongMessage
from datetime                 import datetime, UTC
from uuid                     import uuid4

from ..messages.chat          import (
    ChatHistory,
    ChatHistoryPayload,
    ChatInput,
    ChatMessage,
    ChatMessagePayload,
    GetChatHistory,
)

# =============================================================================
# FÜR DAS KI-TEAM:
# =============================================================================
# Diese Datei ist euer Einstiegspunkt. Hier passiert die gesamte
# WebSocket-Kommunikation zwischen Frontend und KI-Backend.
#
# WEBSOCKET-ENDPUNKT:
#   ws://localhost:8000/ws/ai/chat
#
# WAS IHR ANPASSEN MÜSST:
#   1. handle_chat_input() — ersetzt den Fake-LLM-Block (Zeile ~90) durch
#      einen echten Mistral-API-Call. Der API-Key steht in settings.py
#      unter MISTRAL_API_KEY. Streamt die Tokens direkt durch, das Protokoll
#      bleibt identisch.
#
#      WICHTIG - ASYNC: Dieser Consumer ist vollständig async. Euer LLM_Client
#      ist synchron. Ihr habt zwei Optionen:
#        a) Sync-Aufruf wrappen:
#           from asgiref.sync import sync_to_async
#           response = await sync_to_async(llm.get_user_message)(message)
#        b) Euren LLM_Client mit async/await umschreiben (empfohlen für Streaming)
#
#      WICHTIG - STREAMING: Der Consumer schickt die Antwort Token für Token.
#      Euer LLM-Aufruf muss also ebenfalls Token für Token liefern (stream=True
#      bei Mistral), nicht die komplette Antwort auf einmal.
#
#   2. __init__() — ersetzt self.chat_history (In-Memory-Liste) durch
#      Datenbankzugriff, damit der Verlauf über Sessions hinweg erhalten bleibt.
#
#   3. handle_chat_input() Zeile ~80 — guardRails ist immer "none". Hier
#      könnte eine echte Inhaltsprüfung rein, bevor die Nachricht ans LLM geht.
#
# NEUEN CONSUMER (z.B. Quiz) ANLEGEN:
#   1. Neue Datei consumers/quiz.py nach dem gleichen Muster erstellen
#   2. Import + Route in asgi.py eintragen (dort steht ein Kommentar wo genau)
#   3. Nachrichtentypen in messages/ definieren (siehe messages/chat.py als Vorlage)
#
# DAS NACHRICHTENPROTOKOLL (was Frontend schickt/empfängt) steht in:
#   openbook/ai/messages/chat.py
# =============================================================================

@channel(
    name        = "chat",
    description = "Chat with AI Assistant",
    tags        = ["ai", "chat"],
)
class ChatConsumer(AsyncJsonWebsocketConsumer):
    """
    Websocket consumer for chatting with the AI assistant.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize object with a simply in-memory chat history. Note: In future
        versions this should be replaced with a persisted chat memory.
        """
        super().__init__(*args, **kwargs)
        self.chat_history: list[ChatMessagePayload] = []

    @ws_handler(
        summary     = "Handle Ping Requests",
        description = "Simple ping-pong for connectivity testing",
    )
    async def handle_ping(self, message: PingMessage) -> PongMessage:
        return PongMessage()

    @ws_handler(
        summary     = "Get Chat History",
        description = "Retrieve the full chat history from the server",
    )
    async def handle_get_chat_history(self, message: GetChatHistory) -> ChatHistory:
        """
        Return the whole chat history to the client.
        """
        return ChatHistory(payload=ChatHistoryPayload(messages=self.chat_history))

    @ws_handler(
        summary     = "Handle Chat Input",
        description = "Send a new chat message from the user to the assistant",
    )
    async def handle_chat_input(self, message: ChatInput) -> ChatMessage:
        """
        Handle incoming chat message sent by the user.
        """
        # Log user message in the chat history and send it back to the client,
        # so that the client knows the full message details and that it was received.
        user_message = ChatMessage(
            payload = ChatMessagePayload(
                datetime   = datetime.now(UTC),
                sender     = "user",
                type       = "normal",
                severity   = "info",
                guardRails = {"findings": "none", "explanation": ""},
                format     = message.payload.format,
                content    = message.payload.content,
                finished   = True,
            ),
        )

        self.chat_history.append(user_message.payload)
        await self.send_message(user_message)

        # Fake streaming LLM response
        response_string  = f"Fake response: {message.payload.content}"
        response_tokens  = response_string.split(" ")
        response_partial = ""
        response_id      = str(uuid4())

        for response_token in response_tokens:
            if not response_partial:
                response_partial = response_token
            else:
                response_partial += f" {response_token}"

            response_message = ChatMessage(
                payload = ChatMessagePayload(
                    id         = response_id,
                    datetime   = datetime.now(UTC),
                    sender     = "assistant",
                    type       = "normal",
                    severity   = "info",
                    guardRails = {"findings": "none", "explanation": ""},
                    format     = "markdown",
                    content    = response_partial,
                    finished   = False,
                ),
            )

            await self.send_message(response_message)
            await asyncio.sleep(0.25)

        # Send final response and log it to the chat history
        response_message = ChatMessage(
            payload = ChatMessagePayload(
                id         = response_id,
                datetime   = datetime.now(UTC),
                sender     = "assistant",
                type       = "normal",
                severity   = "info",
                guardRails = {"findings": "none", "explanation": ""},
                format     = "markdown",
                content    = response_string,
                finished   = True,
            ),
        )

        self.chat_history.append(response_message.payload)
        return response_message

