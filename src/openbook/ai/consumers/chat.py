# OpenBook: Interactive Online Textbooks
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from __future__ import annotations

import logging

from asgiref.sync             import sync_to_async
from chanx.channels.websocket import AsyncJsonWebsocketConsumer
from chanx.core.decorators    import channel, ws_handler
from chanx.messages.incoming  import PingMessage
from chanx.messages.outgoing  import PongMessage
from datetime                 import datetime, UTC
from uuid                     import UUID, uuid4

from openbook.assistant.services.orchestrator import AssistantOrchestrator

from ..messages.chat          import (
    ChatHistory,
    ChatHistoryPayload,
    ChatInput,
    ChatMessage,
    ChatMessagePayload,
    ChatSessionList,
    ChatSessionListPayload,
    ChatSessionPayload,
    DeleteChatSession,
    ExamAnswerPayload,
    ExamGenerated,
    ExamGeneratedPayload,
    ExamGraded,
    ExamGradedPayload,
    ExamQuestionPayload,
    ExamQuestionResultPayload,
    ExamResume,
    ExamStart,
    ExamSubmit,
    GetChatHistory,
    LearningEventStatus,
    LearningEventStatusPayload,
    LearningPageCompleted,
    LearningPageOpened,
    LearningQuizResult,
    ListChatSessions,
    OpenChatSession,
    RenameChatSession,
    QuizAnswerOptionPayload,
    QuizGenerated,
    QuizGeneratedPayload,
    QuizQuestionPayload,
    QuizSourcePayload,
    QuizStart,
)

# DB models for persisted chat history (aliased so they don't clash with the
# WebSocket ``ChatMessage`` *message* class above).
from openbook.assistant.models import ChatMessage as ChatMessageModel
from openbook.assistant.models import ChatSession as ChatSessionModel
from openbook.assistant.models import ExamAttempt as ExamAttemptModel
from openbook.assistant.models import QuizAttempt as QuizAttemptModel
from openbook.assistant.services.exam_generation import deserialize_generated_exam
from openbook.assistant.services.exam_generation import serialize_generated_exam
from openbook.assistant.services.quiz_generation import deserialize_generated_quiz
from openbook.assistant.services.quiz_generation import serialize_generated_quiz

logger = logging.getLogger(__name__)

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

    # The frontend speaks snake_case (matching the Pydantic payload field names), so
    # disable chanx's automatic camelCase conversion. With it on, multi-word outgoing
    # fields like ``page_id`` were sent as ``pageId`` and silently missed by the
    # frontend — which left quizzes without an anchor page and thus never awarded any
    # points or skills. Single-word chat fields hid the bug.
    camelize = False

    def __init__(self, *args, **kwargs):
        """Track which saved chat session this connection is currently writing to."""
        super().__init__(*args, **kwargs)
        # The active ChatSession id; None means "a fresh chat not yet saved".
        self.session_id: str | None = None
        # The exam most recently generated on this connection, kept so the answers can
        # be graded server-side without ever sending the correct answers to the client.
        self._active_exam = None
        # The saved ExamAttempt this exam belongs to (set when resuming a saved exam, or
        # after the first grade persists a freshly generated one). Drives create-vs-update.
        self._active_exam_id: str | None = None

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
        Return the active session's history. With no active session yet, fall back to
        the learner's most recent session for this course (so a returning user keeps
        their last conversation) or an empty history.
        """
        session_id, messages = await sync_to_async(self._load_active_history)()
        self.session_id = session_id
        return ChatHistory(payload=ChatHistoryPayload(messages=messages, session_id=session_id))

    @ws_handler(
        summary     = "List Chat Sessions",
        description = "List the learner's saved chat sessions for this course",
    )
    async def handle_list_chat_sessions(self, message: ListChatSessions) -> ChatSessionList:
        """Return the learner's saved sessions (newest first) for the sidebar."""
        sessions = await sync_to_async(self._session_summaries)()
        return ChatSessionList(payload=ChatSessionListPayload(sessions=sessions))

    @ws_handler(
        summary     = "Open Chat Session",
        description = "Open a saved chat session, or start a new (unsaved) one",
    )
    async def handle_open_chat_session(self, message: OpenChatSession) -> ChatHistory:
        """
        Switch the active session. A null ``session_id`` starts a fresh chat that is
        only persisted once the learner sends the first message.
        """
        requested = message.payload.session_id
        session_id, messages = await sync_to_async(self._open_session)(requested)
        self.session_id = session_id
        return ChatHistory(payload=ChatHistoryPayload(messages=messages, session_id=session_id))

    @ws_handler(
        summary     = "Rename Chat Session",
        description = "Rename one of the learner's saved chat sessions",
    )
    async def handle_rename_chat_session(self, message: RenameChatSession) -> ChatSessionList:
        """Rename a session (if owned) and return the refreshed session list."""
        await sync_to_async(self._rename_session)(
            message.payload.session_id, message.payload.title,
        )
        sessions = await sync_to_async(self._session_summaries)()
        return ChatSessionList(payload=ChatSessionListPayload(sessions=sessions))

    @ws_handler(
        summary     = "Delete Chat Session",
        description = "Delete one of the learner's saved chat sessions",
    )
    async def handle_delete_chat_session(self, message: DeleteChatSession) -> ChatSessionList:
        """
        Delete a session (if owned). If it was the active one, clear the conversation
        first, then return the refreshed session list.
        """
        deleted_active = await sync_to_async(self._delete_session)(message.payload.session_id)

        if deleted_active:
            self.session_id = None
            await self.send_message(
                ChatHistory(payload=ChatHistoryPayload(messages=[], session_id=None)),
            )

        sessions = await sync_to_async(self._session_summaries)()
        return ChatSessionList(payload=ChatSessionListPayload(sessions=sessions))

    @ws_handler(
        summary     = "Handle Chat Input",
        description = "Send a new chat message from the user to the assistant",
    )
    async def handle_chat_input(self, message: ChatInput) -> ChatMessage:
        """
        Handle an incoming user message: echo it, answer it, and persist both turns to
        the active session (creating one on the first message of a fresh chat).
        """
        # Echo the user message so the client sees it was received.
        user_payload = ChatMessagePayload(
            datetime   = datetime.now(UTC),
            sender     = "user",
            type       = "normal",
            severity   = "info",
            guardRails = {"findings": "none", "explanation": ""},
            format     = message.payload.format,
            content    = message.payload.content,
            finished   = True,
        )
        await self.send_message(ChatMessage(payload=user_payload))

        try:
            response_string = await sync_to_async(self._answer_chat_query)(
                message.payload.content,
                message.payload.page_context,
            )
            response_type     = "normal"
            response_severity = "info"
        except Exception as error:
            response_string = f"Die Assistenten-Abfrage ist fehlgeschlagen: {error}"
            response_type     = "system"
            response_severity = "error"

        assistant_payload = ChatMessagePayload(
            id         = str(uuid4()),
            datetime   = datetime.now(UTC),
            sender     = "assistant",
            type       = response_type,
            severity   = response_severity,
            guardRails = {"findings": "none", "explanation": ""},
            format     = "markdown",
            content    = response_string,
            finished   = True,
        )

        # Persist both turns. Creating a new session here means the sidebar needs a
        # refresh, so push the updated session list to the client.
        session_id, created_new = await sync_to_async(self._persist_turn)(
            user_payload, assistant_payload, message.payload.content,
        )
        self.session_id = session_id

        if created_new:
            sessions = await sync_to_async(self._session_summaries)()
            await self.send_message(ChatSessionList(payload=ChatSessionListPayload(sessions=sessions)))

        return ChatMessage(payload=assistant_payload)

    # ------------------------------------------------------------------ helpers

    def _course_id(self):
        """Course id from the course-scoped route, or None on the global chat route."""
        return self.scope.get("url_route", {}).get("kwargs", {}).get("course_id")

    @staticmethod
    def _make_title(content: str) -> str:
        """Build a short sidebar title from the first user message."""
        first_line = (content or "").strip().splitlines()[0] if content.strip() else ""
        title = first_line[:60].strip()
        return title or "Neuer Chat"

    @staticmethod
    def _payloads_for(session: ChatSessionModel) -> list[ChatMessagePayload]:
        """Replay a session's stored messages as WebSocket payloads."""
        return [
            ChatMessagePayload(
                id         = str(row.id),
                datetime   = row.created_at,
                sender     = row.sender,
                type       = row.type,
                severity   = row.severity,
                guardRails = row.guard_rails or {"findings": "none", "explanation": ""},
                format     = row.format,
                content    = row.content,
                finished   = row.finished,
            )
            for row in session.messages.all()
        ]

    def _session_summaries(self) -> list[ChatSessionPayload]:
        """Saved sessions of the current user+course, newest first."""
        user = self.scope.get("user")
        if user is None or not getattr(user, "is_authenticated", False):
            return []

        sessions = ChatSessionModel.objects.filter(user=user, course_id=self._course_id())
        return [
            ChatSessionPayload(id=str(s.id), title=s.title or "Neuer Chat", updated_at=s.updated_at)
            for s in sessions
        ]

    def _load_active_history(self):
        """(session_id, messages) for the active session, else the latest, else empty."""
        if self.session_id:
            session = ChatSessionModel.objects.filter(pk=self.session_id).first()
            if session is not None:
                return str(session.id), self._payloads_for(session)

        user = self.scope.get("user")
        if user is None or not getattr(user, "is_authenticated", False):
            return None, []

        latest = (
            ChatSessionModel.objects
            .filter(user=user, course_id=self._course_id())
            .first()
        )
        if latest is None:
            return None, []

        return str(latest.id), self._payloads_for(latest)

    def _open_session(self, session_id):
        """Validate ownership and return (session_id, messages); None starts a fresh chat."""
        if session_id is None:
            return None, []

        user = self.scope.get("user")
        session = ChatSessionModel.objects.filter(
            pk=session_id, user=user, course_id=self._course_id(),
        ).first()

        if session is None:
            # Unknown / not owned -> behave like a fresh chat instead of leaking state.
            return None, []

        return str(session.id), self._payloads_for(session)

    def _rename_session(self, session_id, title) -> None:
        """Set a new title on an owned session (trimmed, capped to the model length)."""
        user = self.scope.get("user")
        clean = (title or "").strip()[:120] or "Neuer Chat"
        ChatSessionModel.objects.filter(pk=session_id, user=user).update(title=clean)

    def _delete_session(self, session_id) -> bool:
        """Delete an owned session. Returns whether it was the active session."""
        user = self.scope.get("user")
        was_active = str(session_id) == str(self.session_id)
        ChatSessionModel.objects.filter(pk=session_id, user=user).delete()
        return was_active

    def _persist_turn(self, user_payload, assistant_payload, source_text):
        """Persist a user+assistant turn; create the session on the first message."""
        user = self.scope.get("user")
        if user is None or not getattr(user, "is_authenticated", False):
            return None, False  # Anonymous chats are not saved.

        created_new = False
        session = None

        if self.session_id:
            session = ChatSessionModel.objects.filter(
                pk=self.session_id, user=user,
            ).first()

        if session is None:
            session = ChatSessionModel.objects.create(
                user=user,
                course_id=self._course_id(),
                title=self._make_title(source_text),
            )
            created_new = True

        for payload, sender in ((user_payload, "user"), (assistant_payload, "assistant")):
            ChatMessageModel.objects.create(
                session    = session,
                sender     = sender,
                type       = payload.type,
                severity   = payload.severity,
                format     = payload.format,
                content    = payload.content,
                guard_rails= payload.guardRails.model_dump() if hasattr(payload.guardRails, "model_dump") else dict(payload.guardRails),
                finished   = payload.finished,
            )

        session.save(update_fields=["updated_at"])  # bump ordering
        return str(session.id), created_new

    @ws_handler(
        summary     = "Handle Page Opened",
        description = "Store the last opened page in the learning model",
    )
    async def handle_learning_page_opened(
        self,
        message: LearningPageOpened,
    ) -> LearningEventStatus:
        """
        Store that the current user opened a course page.
        """
        return await self._run_learning_event(
            event="learning_page_opened",
            callback=lambda: self._record_page_opened(message.payload.page_id),
        )

    @ws_handler(
        summary     = "Handle Page Completed",
        description = "Store a completed page in the learning model",
    )
    async def handle_learning_page_completed(
        self,
        message: LearningPageCompleted,
    ) -> LearningEventStatus:
        """
        Store that the current user completed a course page.
        """
        return await self._run_learning_event(
            event="learning_page_completed",
            callback=lambda: self._mark_page_completed(message.payload.page_id),
        )

    @ws_handler(
        summary     = "Handle Quiz Result",
        description = "Store a quiz result in the learning model",
    )
    async def handle_learning_quiz_result(
        self,
        message: LearningQuizResult,
    ) -> LearningEventStatus:
        """
        Store the current user's quiz result for a course page and acknowledge the
        points and skills the learner just earned.
        """
        try:
            reward = await sync_to_async(self._record_quiz_result)(
                quiz_id=message.payload.quiz_id,
                answers=message.payload.answers,
                attempts=message.payload.attempts,
            )
            graded_quiz = reward.get("graded_quiz")
            return LearningEventStatus(
                payload=LearningEventStatusPayload(
                    event="learning_quiz_result",
                    success=True,
                    points_awarded=reward.get("points_awarded", 0),
                    skills_advanced=reward.get("skills_advanced", []),
                    score=graded_quiz.score if graded_quiz else None,
                    correct_count=graded_quiz.correct_count if graded_quiz else None,
                    question_count=graded_quiz.question_count if graded_quiz else None,
                    quiz_results=[
                        {
                            "question_id": result.question_id,
                            "selected_index": result.selected_index,
                            "correct_index": result.correct_index,
                            "correct": result.correct,
                            "correct_answer": result.correct_answer,
                        }
                        for result in graded_quiz.results
                    ] if graded_quiz else [],
                ),
            )
        except Exception as error:
            return LearningEventStatus(
                payload=LearningEventStatusPayload(
                    event="learning_quiz_result",
                    success=False,
                    message=str(error),
                ),
            )

    @ws_handler(
        summary     = "Generate Quiz",
        description = "Generate a course quiz from RAG documents or course content",
    )
    async def handle_quiz_start(
        self,
        message: QuizStart,
    ) -> QuizGenerated | LearningEventStatus:
        """
        Generate quiz questions for the current course.
        """
        try:
            quiz_attempt, quiz = await sync_to_async(self._generate_quiz)(
                question_count=message.payload.question_count,
                textbook_id=message.payload.textbook_id,
            )
            return QuizGenerated(
                payload=QuizGeneratedPayload(
                    quiz_id=quiz_attempt.id,
                    course_id=self._get_required_course_id(),
                    context_source=quiz.context_source,
                    textbook_id=quiz.textbook_id,
                    page_id=quiz.page_id,
                    questions=[
                        QuizQuestionPayload(
                            id=question.id,
                            prompt=question.prompt,
                            options=[
                                QuizAnswerOptionPayload(
                                    text=option.text,
                                )
                                for option in question.options
                            ],
                        )
                        for question in quiz.questions
                    ],
                    sources=[
                        QuizSourcePayload(
                            chunk_id=source.chunk_id,
                            document_id=source.document_id,
                            document_title=source.document_title,
                            position=source.position,
                        )
                        for source in quiz.sources
                    ],
                ),
            )
        except Exception as error:
            return LearningEventStatus(
                payload=LearningEventStatusPayload(
                    event="quiz_start",
                    success=False,
                    message=str(error),
                ),
            )

    @ws_handler(
        summary     = "Generate Exam",
        description = "Generate a mixed free-text + multiple-choice course exam",
    )
    async def handle_exam_start(
        self,
        message: ExamStart,
    ) -> ExamGenerated | LearningEventStatus:
        """
        Generate exam questions for the current course and remember them on the
        connection so the submitted answers can be graded against them.
        """
        try:
            exam = await sync_to_async(self._generate_exam)(
                question_count=message.payload.question_count,
                textbook_id=message.payload.textbook_id,
            )
            self._active_exam = exam
            self._active_exam_id = None  # a fresh exam, not yet saved
            return self._exam_generated_message(exam)
        except Exception as error:
            return LearningEventStatus(
                payload=LearningEventStatusPayload(
                    event="exam_start",
                    success=False,
                    message=str(error),
                ),
            )

    @ws_handler(
        summary     = "Resume Exam",
        description = "Replay a previously saved exam with the same questions",
    )
    async def handle_exam_resume(
        self,
        message: ExamResume,
    ) -> ExamGenerated | LearningEventStatus:
        """Load a saved exam into this connection so it can be taken again."""
        exam = await sync_to_async(self._load_saved_exam)(str(message.payload.exam_id))
        if exam is None:
            return LearningEventStatus(
                payload=LearningEventStatusPayload(
                    event="exam_resume",
                    success=False,
                    message="Exam not found.",
                ),
            )

        self._active_exam = exam
        self._active_exam_id = str(message.payload.exam_id)
        return self._exam_generated_message(exam)

    def _exam_generated_message(self, exam) -> ExamGenerated:
        """Build the client-facing ``exam_generated`` message (no server-side answers)."""
        return ExamGenerated(
            payload=ExamGeneratedPayload(
                course_id=self._get_required_course_id(),
                context_source=exam.context_source,
                textbook_id=exam.textbook_id,
                page_id=exam.page_id,
                questions=[
                    ExamQuestionPayload(
                        id=question.id,
                        kind=question.kind,
                        prompt=question.prompt,
                        max_points=question.max_points,
                        options=[option.text for option in question.options],
                    )
                    for question in exam.questions
                ],
                sources=[
                    QuizSourcePayload(
                        chunk_id=source.chunk_id,
                        document_id=source.document_id,
                        document_title=source.document_title,
                        position=source.position,
                    )
                    for source in getattr(exam, "sources", ())
                ],
            ),
        )

    @ws_handler(
        summary     = "Grade Exam",
        description = "Grade submitted exam answers and award points/skills",
    )
    async def handle_exam_submit(
        self,
        message: ExamSubmit,
    ) -> ExamGraded | LearningEventStatus:
        """Grade the answers for the connection's active exam and award rewards."""
        if self._active_exam is None:
            return LearningEventStatus(
                payload=LearningEventStatusPayload(
                    event="exam_submit",
                    success=False,
                    message="No active exam to grade. Generate an exam first.",
                ),
            )

        try:
            graded = await sync_to_async(self._grade_exam)(message.payload.answers)
            exam_result = graded["graded_exam"]
            return ExamGraded(
                payload=ExamGradedPayload(
                    score=exam_result.score,
                    total_points=exam_result.total_points,
                    max_points=exam_result.max_points,
                    overall_feedback=exam_result.overall_feedback,
                    points_awarded=graded.get("points_awarded", 0),
                    skills_advanced=graded.get("skills_advanced", []),
                    results=[
                        ExamQuestionResultPayload(
                            question_id=result.question_id,
                            kind=result.kind,
                            prompt=result.prompt,
                            your_answer=result.your_answer,
                            awarded_points=result.awarded_points,
                            max_points=result.max_points,
                            feedback=result.feedback,
                            correct=result.correct,
                            correct_answer=result.correct_answer,
                        )
                        for result in exam_result.results
                    ],
                ),
            )
        except Exception as error:
            return LearningEventStatus(
                payload=LearningEventStatusPayload(
                    event="exam_submit",
                    success=False,
                    message=str(error),
                ),
            )

    async def _run_learning_event(self, event: str, callback) -> LearningEventStatus:
        """Run a blocking learning event and convert the result into an acknowledgement."""
        try:
            await sync_to_async(callback)()
            return LearningEventStatus(
                payload=LearningEventStatusPayload(event=event, success=True),
            )
        except Exception as error:
            return LearningEventStatus(
                payload=LearningEventStatusPayload(
                    event=event,
                    success=False,
                    message=str(error),
                ),
            )

    def _answer_chat_query(self, query: str, page_context: str = "") -> str:
        """Run the blocking assistant stack outside the async event loop."""
        course_id = self.scope.get("url_route", {}).get("kwargs", {}).get("course_id")
        user = self.scope.get("user")
        answer = AssistantOrchestrator().answer(
            query=query,
            user=user,
            course=course_id,
            context=page_context,
        )
        return str(answer or "")

    def _generate_quiz(self, question_count: int, textbook_id=None):
        """Run the blocking quiz generation stack outside the async event loop."""
        course_id = self._get_required_course_id()
        user = self.scope.get("user")
        quiz = AssistantOrchestrator().generate_quiz(
            user=self.scope.get("user"),
            course=course_id,
            question_count=question_count,
            textbook=textbook_id,
        )
        quiz_attempt = QuizAttemptModel.objects.create(
            user=user,
            course_id=course_id,
            textbook_id=quiz.textbook_id or None,
            page_id=quiz.page_id or None,
            quiz=serialize_generated_quiz(quiz),
            question_count=len(quiz.questions),
        )
        return quiz_attempt, quiz

    def _generate_exam(self, question_count: int, textbook_id=None):
        """Run the blocking exam generation stack outside the async event loop."""
        course_id = self._get_required_course_id()
        return AssistantOrchestrator().generate_exam(
            user=self.scope.get("user"),
            course=course_id,
            question_count=question_count,
            textbook=textbook_id,
        )

    def _grade_exam(self, answers) -> dict:
        """Grade the active exam against the submitted answers, award rewards, and save it."""
        course_id = self._get_required_course_id()
        graded = AssistantOrchestrator().grade_exam(
            user=self.scope.get("user"),
            course=course_id,
            exam=self._active_exam,
            answers=[answer.model_dump() for answer in answers],
        )
        try:
            self._persist_exam(graded.get("graded_exam"))
        except Exception:
            logger.exception("Failed to save exam attempt")
        return graded

    def _exam_title(self, exam) -> str:
        """A readable title for a saved exam (the textbook's name, else 'Exam')."""
        if getattr(exam, "textbook_id", None):
            from openbook.content.models import Textbook
            textbook = Textbook.objects.filter(pk=exam.textbook_id).first()
            if textbook:
                return textbook.name
        return "Exam"

    def _persist_exam(self, graded_exam) -> None:
        """Create or update the saved ExamAttempt for the current (graded) exam."""
        user = self.scope.get("user")
        if user is None or not getattr(user, "is_authenticated", False) or self._active_exam is None or graded_exam is None:
            return

        result = {
            "score":            graded_exam.score,
            "total_points":     graded_exam.total_points,
            "max_points":       graded_exam.max_points,
            "overall_feedback": graded_exam.overall_feedback,
            "results": [
                {
                    "question_id":    item.question_id,
                    "kind":           item.kind,
                    "prompt":         item.prompt,
                    "your_answer":    item.your_answer,
                    "awarded_points": item.awarded_points,
                    "max_points":     item.max_points,
                    "feedback":       item.feedback,
                    "correct":        item.correct,
                    "correct_answer": item.correct_answer,
                }
                for item in graded_exam.results
            ],
        }

        attempt = None
        if self._active_exam_id:
            attempt = ExamAttemptModel.objects.filter(pk=self._active_exam_id, user=user).first()

        if attempt is None:
            attempt = ExamAttemptModel(
                user=user,
                course_id=self._get_required_course_id(),
                textbook_id=getattr(self._active_exam, "textbook_id", None) or None,
                title=self._exam_title(self._active_exam),
                exam=serialize_generated_exam(self._active_exam),
            )

        attempt.result       = result
        attempt.total_points = graded_exam.total_points
        attempt.max_points   = graded_exam.max_points
        attempt.score        = graded_exam.score
        attempt.save()
        self._active_exam_id = str(attempt.id)

    def _load_saved_exam(self, exam_id: str):
        """Reconstruct a saved exam (with answers) for the current user, or None."""
        attempt = ExamAttemptModel.objects.filter(pk=exam_id, user=self.scope.get("user")).first()
        if attempt is None or not attempt.exam:
            return None
        return deserialize_generated_exam(attempt.exam)

    def _record_page_opened(self, page_id: UUID) -> None:
        """Store that the current user opened a course page."""
        course_id = self._get_required_course_id()
        AssistantOrchestrator().record_page_opened(
            user=self.scope.get("user"),
            course=course_id,
            page=page_id,
        )

    def _mark_page_completed(self, page_id: UUID) -> None:
        """Store that the current user completed a course page."""
        course_id = self._get_required_course_id()
        AssistantOrchestrator().mark_page_completed(
            user=self.scope.get("user"),
            course=course_id,
            page=page_id,
        )

    def _record_quiz_result(
        self,
        quiz_id: UUID,
        answers,
        attempts: int | None,
    ) -> dict:
        """Store the current user's quiz result and return the awarded points/skills."""
        course_id = self._get_required_course_id()
        attempt = QuizAttemptModel.objects.filter(
            pk=quiz_id,
            user=self.scope.get("user"),
            course_id=course_id,
        ).first()
        if attempt is None:
            raise ValueError("Quiz not found.")

        quiz = deserialize_generated_quiz(attempt.quiz)
        graded = AssistantOrchestrator().grade_quiz(
            user=self.scope.get("user"),
            course=course_id,
            quiz=quiz,
            answers=[answer.model_dump() for answer in answers],
            attempts=attempts,
        )
        graded_quiz = graded.get("graded_quiz")
        if graded_quiz:
            attempt.result = {
                "score": graded_quiz.score,
                "correct_count": graded_quiz.correct_count,
                "question_count": graded_quiz.question_count,
                "results": [
                    {
                        "question_id": result.question_id,
                        "selected_index": result.selected_index,
                        "correct_index": result.correct_index,
                        "correct": result.correct,
                        "correct_answer": result.correct_answer,
                    }
                    for result in graded_quiz.results
                ],
            }
            attempt.correct_count = graded_quiz.correct_count
            attempt.question_count = graded_quiz.question_count
            attempt.score = graded_quiz.score
            attempt.save(
                update_fields=[
                    "result",
                    "correct_count",
                    "question_count",
                    "score",
                    "updated_at",
                ]
            )
        return graded

    def _get_required_course_id(self):
        """Return the course id from the course-scoped WebSocket route."""
        course_id = self.scope.get("url_route", {}).get("kwargs", {}).get("course_id")
        if course_id is None:
            raise ValueError("Learning events require a course-scoped chat WebSocket.")
        return course_id
