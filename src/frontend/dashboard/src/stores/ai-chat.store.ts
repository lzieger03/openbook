/*
 * OpenBook: Interactive Online Textbooks - Server
 * © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 */

/**
 * AI chat store backed by the WebSocket API.
 *
 * IMPORTANT: the message typings below must match the Python side. There is no
 * tool yet to generate them from the server's AsyncAPI spec, so when the Python
 * messages change (action / payload / field names), mirror them here by hand.
 * See README-websocket-api.md.
 */

import {writable} from "svelte/store";
import {ws} from "../api/client.js";
import type {WebSocketClient, WSConnectionStatus} from "../api/websocket.js";

// ── Message contract (mirrored from src/openbook/ai/messages/chat.py) ─────────

export type ChatMessageSender = "user" | "assistant";

export type ChatMessageType = "normal" | "status" | "thought" | "action" | "system";

export type ChatMessageSeverity = "info" | "warning" | "error" | "critical";

export type ChatMessageFormat = "markdown" | "json" | "image";

export interface GuardRailCheckResult {
    findings: "none" | "offensive_language" | "dangerous_content" | "others";
    explanation: string;
}

export interface ChatInputPayload {
    format: ChatMessageFormat;
    content: string;
}

export interface ChatMessagePayload {
    id: string;
    datetime: string;
    sender: ChatMessageSender;
    type: ChatMessageType;
    severity: ChatMessageSeverity;
    guardRails: GuardRailCheckResult;
    format: ChatMessageFormat;
    content: string;
    finished: boolean;
}

export interface ChatHistoryPayload {
    messages: ChatMessagePayload[];
}

export interface ChatInput {
    action: "chat_input";
    payload: ChatInputPayload;
}

export interface ChatMessage {
    action: "chat_message";
    payload: ChatMessagePayload;
}

export interface GetChatHistory {
    action: "get_chat_history";
    payload: null;
}

export interface ChatHistory {
    action: "chat_history";
    payload: ChatHistoryPayload;
}

export interface LearningPagePayload {
    page_id: string;
}

export interface LearningQuizResultPayload {
    page_id: string;
    score: number;
    attempts?: number | null;
}

export interface LearningEventStatusPayload {
    event: string;
    success: boolean;
    message: string;
}

export interface LearningPageOpened {
    action: "learning_page_opened";
    payload: LearningPagePayload;
}

export interface LearningPageCompleted {
    action: "learning_page_completed";
    payload: LearningPagePayload;
}

export interface LearningQuizResult {
    action: "learning_quiz_result";
    payload: LearningQuizResultPayload;
}

export interface LearningEventStatus {
    action: "learning_event_status";
    payload: LearningEventStatusPayload;
}

/** Messages the client sends to the server. */
export type SentMessages =
    | GetChatHistory
    | ChatInput
    | LearningPageOpened
    | LearningPageCompleted
    | LearningQuizResult;

/** Messages the server sends to the client. */
export type ReceivedMessages = ChatHistory | ChatMessage | LearningEventStatus;

// ── Store ─────────────────────────────────────────────────────────────────────

export interface AiChatState {
    connection: WSConnectionStatus;
    errorMessage: string;
    messages: ChatMessagePayload[];
}

export interface AiChatStore {
    subscribe: (run: (value: AiChatState) => void) => () => void;
    connect: () => Promise<void>;
    disconnect: () => Promise<void>;
    retry: () => Promise<void>;
    getChatHistory: () => Promise<void>;
    sendChatInput: (format: ChatMessageFormat, content: string) => Promise<void>;
    recordPageOpened: (pageId: string) => Promise<void>;
    markPageCompleted: (pageId: string) => Promise<void>;
    recordQuizResult: (pageId: string, score: number, attempts?: number) => Promise<void>;
}

type CourseIdSource = string | (() => string | undefined);

/**
 * Create an independent AI chat store. Each UI surface (full page, widget) gets
 * its own instance; connect() on mount, disconnect() on unmount.
 */
export function createAiChatStore(courseId?: CourseIdSource): AiChatStore {
    const {subscribe, update} = writable<AiChatState>({
        connection: "disconnected",
        errorMessage: "",
        messages: [],
    });

    let socket: WebSocketClient<SentMessages, ReceivedMessages> | undefined;

    async function getChatHistory(): Promise<void> {
        await socket?.send({action: "get_chat_history", payload: null});
    }

    async function connect(): Promise<void> {
        if (!socket) {
            const resolvedCourseId = typeof courseId === "function" ? courseId() : courseId;
            const channel = resolvedCourseId
                ? `/ai/courses/${encodeURIComponent(resolvedCourseId)}/chat`
                : "/ai/chat";
            socket = await ws<SentMessages, ReceivedMessages>(channel);

            socket.setConnectionStatusListener((status) => {
                update((state) => ({
                    ...state,
                    connection: status,
                    errorMessage: status === "connected" ? "" : state.errorMessage,
                }));
                if (status === "connected") {
                    void getChatHistory();
                }
            });

            socket.setErrorHandler((error) => {
                const message = error instanceof Error ? error.message : "WebSocket error.";
                update((state) => ({...state, errorMessage: message}));
            });

            socket.setMessageHandler("chat_history", (message: ChatHistory) => {
                update((state) => ({...state, messages: message.payload.messages}));
            });

            // Streaming message: replace by id if it exists, otherwise append.
            socket.setMessageHandler("chat_message", (message: ChatMessage) => {
                update((state) => {
                    const index = state.messages.findIndex((m) => m.id === message.payload.id);
                    const messages =
                        index === -1
                            ? [...state.messages, message.payload]
                            : state.messages.map((m, i) => (i === index ? message.payload : m));
                    return {...state, messages};
                });
            });

            socket.setMessageHandler("learning_event_status", (message: LearningEventStatus) => {
                update((state) => ({
                    ...state,
                    errorMessage: message.payload.success ? state.errorMessage : message.payload.message,
                }));
            });
        }

        await socket.connect();
    }

    async function disconnect(): Promise<void> {
        await socket?.disconnect();
    }

    /** Clear the error and try connecting again (resets the unstable-retry guard). */
    async function retry(): Promise<void> {
        update((state) => ({...state, errorMessage: ""}));
        if (socket) {
            await socket.retry();
        } else {
            await connect();
        }
    }

    /** Send a user chat message. The server echoes it back, so we do not add it locally. */
    async function sendChatInput(format: ChatMessageFormat, content: string): Promise<void> {
        await socket?.send({action: "chat_input", payload: {format, content}});
    }

    async function recordPageOpened(pageId: string): Promise<void> {
        await socket?.send({action: "learning_page_opened", payload: {page_id: pageId}});
    }

    async function markPageCompleted(pageId: string): Promise<void> {
        await socket?.send({action: "learning_page_completed", payload: {page_id: pageId}});
    }

    async function recordQuizResult(
        pageId: string,
        score: number,
        attempts?: number,
    ): Promise<void> {
        await socket?.send({
            action: "learning_quiz_result",
            payload: {page_id: pageId, score, attempts: attempts ?? null},
        });
    }

    return {
        subscribe,
        connect,
        disconnect,
        retry,
        getChatHistory,
        sendChatInput,
        recordPageOpened,
        markPageCompleted,
        recordQuizResult,
    };
}
