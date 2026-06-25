# OpenBook: Interactive Online Textbooks
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from __future__ import annotations

# =============================================================================
# FÜR DAS FRONTEND-TEAM:
# =============================================================================
# Diese Datei definiert das vollständige WebSocket-Protokoll zwischen
# Frontend (Svelte) und KI-Backend.
#
# VERBINDUNG AUFBAUEN:
#   const socket = new WebSocket("ws://localhost:8000/ws/ai/chat")
#
# WICHTIG - AUTHENTIFIZIERUNG:
#   Der WebSocket erfordert einen eingeloggten User (Session-Cookie).
#   Die Verbindung muss aus dem Browser hergestellt werden NACHDEM der
#   User sich eingeloggt hat. Ohne Login wird die Verbindung abgelehnt.
#
# NACHRICHTEN SCHICKEN (Frontend → Backend):
#
#   1. Chat-Nachricht senden:
#      socket.send(JSON.stringify({
#        action: "chat_input",
#        payload: { format: "markdown", content: "Deine Frage hier" }
#      }))
#
#   2. Chatverlauf abrufen:
#      socket.send(JSON.stringify({ action: "get_chat_history", payload: null }))
#
#   3. Verbindung testen:
#      socket.send(JSON.stringify({ action: "ping", payload: null }))
#
# NACHRICHTEN EMPFANGEN (Backend → Frontend):
#
#   socket.onmessage = (event) => {
#     const msg = JSON.parse(event.data)
#
#     if (msg.action === "chat_message") {
#       // msg.payload.sender    → "user" | "assistant"
#       // msg.payload.content   → Text (Markdown)
#       // msg.payload.finished  → false = noch am Streamen, true = fertig
#       // msg.payload.id        → gleiche ID bei allen Streaming-Chunks einer Antwort
#       // msg.payload.datetime  → ISO-Timestamp
#       // msg.payload.type      → "normal" | "status" | "thought" | "action" | "system"
#       // msg.payload.severity  → "info" | "warning" | "error" | "critical"
#       // msg.payload.format    → "markdown" | "json" | "image"
#     }
#
#     if (msg.action === "chat_history") {
#       // msg.payload.messages  → Array von chat_message Payloads (s.o.)
#     }
#
#     if (msg.action === "pong") { /* Verbindung OK */ }
#   }
#
# STREAMING:
#   Der Server schickt die KI-Antwort Token für Token als "chat_message".
#   Solange finished === false kommen weitere Chunks mit derselben id.
#   Wenn finished === true ist die Antwort vollständig.
#   → Im Frontend: Chunks mit gleicher id zusammensetzen und anzeigen.
# =============================================================================

from chanx.messages.base import BaseMessage
from datetime            import datetime
from pydantic            import BaseModel, Field
from typing              import Literal
from uuid                import UUID, uuid4

ChatMessageSender = Literal["user", "assistant"]
"""Who sent the message, the user or the AI assistant"""

ChatMessageType = Literal["normal", "status", "thought", "action", "system"]
"""
How to interpret and handle a chat message. The user can only send normal messages.
The other values are reserved for the AI assistant.

- ``normal``:  Regular chat message
- ``status``:  Temporary status message, e.g. "Thinking"
- ``thought``: Temporary chain of thought message
- ``action``:  A UI action triggered by the assistant
- ``system``:  An information, warning or error message
"""

ChatMessageSeverity = Literal["info", "warning", "error", "critical"]
"""Severity of system messages"""

ChatMessageFormat = Literal["markdown", "json", "image"]
"""Format of the message content. Binary content is always Base64 encoded."""

class GuardRailCheckResult(BaseModel):
    """
    Guard rails check incoming chat messages for disallowed or dangerous content.
    This type defines the data structure for the check results.
    """
    findings:    Literal["none", "offensive_language", "dangerous_content", "others"]
    explanation: str

class ChatInputPayload(BaseModel):
    """
    Payload for incoming user chat messages.
    """
    format:  ChatMessageFormat
    content: str

class ChatMessagePayload(BaseModel):
    """
    Payload for a single chat message.
    """
    id:         str = Field(default_factory = lambda: str(uuid4()))
    datetime:   datetime
    sender:     ChatMessageSender
    type:       ChatMessageType
    severity:   ChatMessageSeverity
    guardRails: GuardRailCheckResult
    format:     ChatMessageFormat
    content:    str
    finished:   bool

class ChatHistoryPayload(BaseModel):
    """
    Payload containing the full chat history of one session. ``session_id`` is the
    session the messages belong to (null when starting a fresh, unsaved chat).
    """
    messages:   list[ChatMessagePayload]
    session_id: str | None = None

class OpenChatSessionPayload(BaseModel):
    """
    Payload to open a saved chat session (or start a new one when ``session_id`` is null).
    """
    session_id: UUID | None = None

class ChatSessionPayload(BaseModel):
    """
    Summary of one saved chat session, shown in the chat sidebar.
    """
    id:         str
    title:      str
    updated_at: datetime

class ChatSessionListPayload(BaseModel):
    """
    Payload listing the learner's saved chat sessions for the current course.
    """
    sessions: list[ChatSessionPayload]

class RenameChatSessionPayload(BaseModel):
    """Payload to rename a saved chat session."""
    session_id: UUID
    title:      str

class DeleteChatSessionPayload(BaseModel):
    """Payload to delete a saved chat session."""
    session_id: UUID

class LearningPagePayload(BaseModel):
    """
    Payload for page-related learning progress events.
    """
    page_id: UUID

class LearningQuizResultPayload(BaseModel):
    """
    Payload for storing a quiz result in the learning model.
    """
    page_id:  UUID
    score:    float
    attempts: int | None = None

class LearningEventStatusPayload(BaseModel):
    """
    Payload acknowledging a learning progress event.

    For a ``learning_quiz_result`` event, ``points_awarded`` and ``skills_advanced``
    report what the learner just earned so the UI can show immediate feedback.
    """
    event:           str
    success:         bool
    message:         str = ""
    points_awarded:  int = 0
    skills_advanced: list[str] = Field(default_factory=list)

class QuizStartPayload(BaseModel):
    """
    Payload for requesting a generated quiz for the current course channel.

    ``textbook_id`` optionally narrows the quiz to a single textbook of the course so
    the learner can choose which textbook to be quizzed on. When omitted, the quiz is
    generated from the whole course as before.
    """
    question_count: int = Field(default=5, ge=1, le=10)
    textbook_id:    UUID | None = None

class QuizAnswerOptionPayload(BaseModel):
    """
    A selectable answer option in a generated quiz question.
    """
    text:    str
    correct: bool

class QuizQuestionPayload(BaseModel):
    """
    One generated multiple-choice quiz question.
    """
    id:      str = Field(default_factory=lambda: str(uuid4()))
    prompt:  str
    options: list[QuizAnswerOptionPayload]

class QuizSourcePayload(BaseModel):
    """
    Source metadata for a RAG chunk used to generate a quiz.
    """
    chunk_id:       str
    document_id:    str
    document_title: str
    position:       int

class QuizGeneratedPayload(BaseModel):
    """
    Generated quiz questions for the current course.

    ``textbook_id`` echoes the textbook the quiz was scoped to (if any). ``page_id`` is
    the textbook page the result should be anchored to: the client sends it back in a
    ``learning_quiz_result`` message so the score can be stored and points awarded.
    """
    course_id:      UUID
    context_source: Literal["rag_documents", "course_context"]
    questions:      list[QuizQuestionPayload]
    sources:        list[QuizSourcePayload] = Field(default_factory=list)
    textbook_id:    UUID | None = None
    page_id:        UUID | None = None

class ExamStartPayload(BaseModel):
    """
    Payload for requesting a generated exam for the current course channel.

    ``textbook_id`` optionally narrows the exam to a single textbook of the course,
    mirroring the quiz flow. When omitted, the exam covers the whole course.
    """
    question_count: int = Field(default=5, ge=1, le=10)
    textbook_id:    UUID | None = None

class ExamQuestionPayload(BaseModel):
    """
    One generated exam question, as sent to the client. The correct answers and
    model answers are intentionally omitted so the exam cannot be solved from the
    payload; grading happens server-side on submission.
    """
    id:         str
    kind:       Literal["free_text", "multiple_choice"]
    prompt:     str
    max_points: int
    # Only populated for multiple-choice questions (option texts, no correct flags).
    options:    list[str] = Field(default_factory=list)

class ExamGeneratedPayload(BaseModel):
    """
    Generated exam questions for the current course.

    ``page_id`` is the textbook page the result is anchored to; the client echoes it
    back in ``exam_submit`` so the score can be stored and points awarded.
    """
    course_id:      UUID
    context_source: Literal["rag_documents", "course_context"]
    questions:      list[ExamQuestionPayload]
    sources:        list[QuizSourcePayload] = Field(default_factory=list)
    textbook_id:    UUID | None = None
    page_id:        UUID | None = None

class ExamAnswerPayload(BaseModel):
    """One submitted answer: free text, or the picked option index for multiple choice."""
    question_id:    str
    text:           str = ""
    selected_index: int | None = None

class ExamSubmitPayload(BaseModel):
    """Payload submitting a learner's exam answers for grading."""
    answers: list[ExamAnswerPayload] = Field(default_factory=list)

class ExamResumePayload(BaseModel):
    """Payload to replay a previously saved exam (same questions)."""
    exam_id: UUID

class ExamQuestionResultPayload(BaseModel):
    """The grading outcome for a single exam question, shown to the learner."""
    question_id:    str
    kind:           Literal["free_text", "multiple_choice"]
    prompt:         str
    your_answer:    str
    awarded_points: int
    max_points:     int
    feedback:       str
    correct:        bool | None = None
    correct_answer: str = ""

class ExamGradedPayload(BaseModel):
    """
    The full grading outcome of an exam attempt, including the points and skills the
    learner earned (reported like a quiz result so the UI can show immediate feedback).
    """
    score:           float
    total_points:    int
    max_points:      int
    results:         list[ExamQuestionResultPayload]
    overall_feedback: str = ""
    points_awarded:  int = 0
    skills_advanced: list[str] = Field(default_factory=list)

class ChatInput(BaseMessage):
    """
    Chat input sent by the user to the assistant.
    """
    action:  Literal["chat_input"] = "chat_input"
    payload: ChatInputPayload

class ChatMessage(BaseMessage):
    """
    A single chat message within a larger chat conversation. This is the data that
    the server uses internally to drive the AI chat functionality and persist the
    chat history.
    """
    action:  Literal["chat_message"] = "chat_message"
    payload: ChatMessagePayload

class GetChatHistory(BaseMessage):
    """
    Message sent by the client to retrieve the full chat history from the server.
    """
    action:  Literal["get_chat_history"] = "get_chat_history"
    payload: None = None

class ChatHistory(BaseMessage):
    """
    Full chat history.
    """
    action:  Literal["chat_history"] = "chat_history"
    payload: ChatHistoryPayload

class ListChatSessions(BaseMessage):
    """
    Message sent by the client to list its saved chat sessions for the current course.
    """
    action:  Literal["list_chat_sessions"] = "list_chat_sessions"
    payload: None = None

class OpenChatSession(BaseMessage):
    """
    Message sent by the client to open a saved chat session (or start a new one).
    """
    action:  Literal["open_chat_session"] = "open_chat_session"
    payload: OpenChatSessionPayload

class ChatSessionList(BaseMessage):
    """
    The learner's saved chat sessions for the current course.
    """
    action:  Literal["chat_session_list"] = "chat_session_list"
    payload: ChatSessionListPayload

class RenameChatSession(BaseMessage):
    """Message sent by the client to rename a saved chat session."""
    action:  Literal["rename_chat_session"] = "rename_chat_session"
    payload: RenameChatSessionPayload

class DeleteChatSession(BaseMessage):
    """Message sent by the client to delete a saved chat session."""
    action:  Literal["delete_chat_session"] = "delete_chat_session"
    payload: DeleteChatSessionPayload

class LearningPageOpened(BaseMessage):
    """
    Message sent by the client when the current course page was opened.
    """
    action:  Literal["learning_page_opened"] = "learning_page_opened"
    payload: LearningPagePayload

class LearningPageCompleted(BaseMessage):
    """
    Message sent by the client when the current course page was completed.
    """
    action:  Literal["learning_page_completed"] = "learning_page_completed"
    payload: LearningPagePayload

class LearningQuizResult(BaseMessage):
    """
    Message sent by the client when a course quiz result should be stored.
    """
    action:  Literal["learning_quiz_result"] = "learning_quiz_result"
    payload: LearningQuizResultPayload

class LearningEventStatus(BaseMessage):
    """
    Acknowledgement for a learning progress event.
    """
    action:  Literal["learning_event_status"] = "learning_event_status"
    payload: LearningEventStatusPayload

class QuizStart(BaseMessage):
    """
    Message sent by the client to generate a course quiz.
    """
    action:  Literal["quiz_start"] = "quiz_start"
    payload: QuizStartPayload

class QuizGenerated(BaseMessage):
    """
    Message sent by the server after generating a course quiz.
    """
    action:  Literal["quiz_generated"] = "quiz_generated"
    payload: QuizGeneratedPayload

class ExamStart(BaseMessage):
    """
    Message sent by the client to generate a course exam.
    """
    action:  Literal["exam_start"] = "exam_start"
    payload: ExamStartPayload

class ExamGenerated(BaseMessage):
    """
    Message sent by the server after generating a course exam.
    """
    action:  Literal["exam_generated"] = "exam_generated"
    payload: ExamGeneratedPayload

class ExamSubmit(BaseMessage):
    """
    Message sent by the client to submit exam answers for AI grading.
    """
    action:  Literal["exam_submit"] = "exam_submit"
    payload: ExamSubmitPayload

class ExamResume(BaseMessage):
    """
    Message sent by the client to replay a saved exam (same questions, fresh attempt).
    """
    action:  Literal["exam_resume"] = "exam_resume"
    payload: ExamResumePayload

class ExamGraded(BaseMessage):
    """
    Message sent by the server with the graded exam result.
    """
    action:  Literal["exam_graded"] = "exam_graded"
    payload: ExamGradedPayload
