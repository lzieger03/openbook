/*
 * OpenBook: Interactive Online Textbooks - Server
 * (c) 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 */

/**
 * Course quiz state backed by the existing course chat WebSocket channel.
 */

import {writable} from "svelte/store";

import {ws} from "../api/client.js";
import type {WebSocketClient, WSConnectionStatus} from "../api/websocket.js";

export type QuizContextSource = "rag_documents" | "course_context";

export interface QuizOption {
    text: string;
    correct: boolean;
}

export interface QuizQuestion {
    id: string;
    prompt: string;
    options: QuizOption[];
}

export interface QuizSource {
    chunk_id: string;
    document_id: string;
    document_title: string;
    position: number;
}

export interface QuizState {
    connection: WSConnectionStatus;
    isLoading: boolean;
    errorMessage: string;
    questions: QuizQuestion[];
    contextSource: QuizContextSource | null;
    sources: QuizSource[];
}

interface QuizStart {
    action: "quiz_start";
    payload: {
        question_count: number;
    };
}

interface QuizGenerated {
    action: "quiz_generated";
    payload: {
        course_id: string;
        context_source: QuizContextSource;
        questions: QuizQuestion[];
        sources: QuizSource[];
    };
}

interface LearningEventStatus {
    action: "learning_event_status";
    payload: {
        event: string;
        success: boolean;
        message: string;
    };
}

type SentMessages = QuizStart;

type ReceivedMessages = QuizGenerated | LearningEventStatus;

type CourseIdSource = string | (() => string | undefined);

export interface QuizStore {
    subscribe: (run: (value: QuizState) => void) => () => void;
    connect: () => Promise<void>;
    disconnect: () => Promise<void>;
    requestQuiz: (questionCount?: number) => Promise<void>;
}

function initialState(): QuizState {
    return {
        connection: "disconnected",
        isLoading: false,
        errorMessage: "",
        questions: [],
        contextSource: null,
        sources: [],
    };
}

export function createQuizStore(courseId: CourseIdSource): QuizStore {
    const {subscribe, update} = writable<QuizState>(initialState());

    let socket: WebSocketClient<SentMessages, ReceivedMessages> | undefined;

    function resolveCourseId(): string {
        const resolvedCourseId = typeof courseId === "function" ? courseId() : courseId;
        if (!resolvedCourseId) {
            throw new Error("Course id is required for quiz generation.");
        }
        return resolvedCourseId;
    }

    async function connect(): Promise<void> {
        if (!socket) {
            const resolvedCourseId = resolveCourseId();
            socket = await ws<SentMessages, ReceivedMessages>(
                `/ai/courses/${encodeURIComponent(resolvedCourseId)}/chat`,
            );

            socket.setConnectionStatusListener((status) => {
                update((state) => ({
                    ...state,
                    connection: status,
                    errorMessage: status === "connected" ? "" : state.errorMessage,
                }));
            });

            socket.setErrorHandler((error) => {
                const message = error instanceof Error ? error.message : "WebSocket error.";
                update((state) => ({...state, errorMessage: message, isLoading: false}));
            });

            socket.setMessageHandler("quiz_generated", (message: QuizGenerated) => {
                update((state) => ({
                    ...state,
                    isLoading: false,
                    errorMessage: "",
                    questions: message.payload.questions,
                    contextSource: message.payload.context_source,
                    sources: message.payload.sources,
                }));
            });

            socket.setMessageHandler("learning_event_status", (message: LearningEventStatus) => {
                if (message.payload.event !== "quiz_start") {
                    return;
                }

                update((state) => ({
                    ...state,
                    isLoading: false,
                    errorMessage: message.payload.success ? "" : message.payload.message,
                }));
            });
        }

        await socket.connect();
    }

    async function disconnect(): Promise<void> {
        await socket?.disconnect();
    }

    async function requestQuiz(questionCount = 5): Promise<void> {
        update((state) => ({
            ...state,
            isLoading: true,
            errorMessage: "",
            questions: [],
            contextSource: null,
            sources: [],
        }));

        try {
            if (!socket) {
                await connect();
            }

            await socket?.send({
                action: "quiz_start",
                payload: {question_count: questionCount},
            });
        } catch (error) {
            const message = error instanceof Error ? error.message : String(error);
            update((state) => ({...state, isLoading: false, errorMessage: message}));
        }
    }

    return {
        subscribe,
        connect,
        disconnect,
        requestQuiz,
    };
}
