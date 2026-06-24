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
    // Textbook the current quiz is scoped to and the page its result anchors to.
    textbookId: string | null;
    pageId: string | null;
}

interface QuizStart {
    action: "quiz_start";
    payload: {
        question_count: number;
        textbook_id?: string;
    };
}

interface LearningQuizResult {
    action: "learning_quiz_result";
    payload: {
        page_id: string;
        score: number;
        attempts: number | null;
    };
}

interface QuizGenerated {
    action: "quiz_generated";
    payload: {
        course_id: string;
        context_source: QuizContextSource;
        questions: QuizQuestion[];
        sources: QuizSource[];
        textbook_id: string | null;
        page_id: string | null;
    };
}

interface LearningEventStatus {
    action: "learning_event_status";
    payload: {
        event: string;
        success: boolean;
        message: string;
        points_awarded?: number;
        skills_advanced?: string[];
    };
}

/** What the learner earned from a submitted quiz, passed to {@link QuizStoreOptions.onResultRecorded}. */
export interface QuizRewardSummary {
    pointsAwarded: number;
    skillsAdvanced: string[];
}

type SentMessages = QuizStart | LearningQuizResult;

type ReceivedMessages = QuizGenerated | LearningEventStatus;

type CourseIdSource = string | (() => string | undefined);

/** Options for {@link createQuizStore}. */
export interface QuizStoreOptions {
    /**
     * Called once the backend has acknowledged a submitted quiz result (points and
     * skill progress have been awarded). Receives what the learner earned so the UI can
     * show it; the dashboard also uses this to refresh so the new totals show up.
     */
    onResultRecorded?: (reward: QuizRewardSummary) => void;
}

export interface QuizStore {
    subscribe: (run: (value: QuizState) => void) => () => void;
    connect: () => Promise<void>;
    disconnect: () => Promise<void>;
    requestQuiz: (questionCount?: number, textbookId?: string) => Promise<void>;
    submitResult: (score: number, attempts?: number) => Promise<void>;
}

function initialState(): QuizState {
    return {
        connection: "disconnected",
        isLoading: false,
        errorMessage: "",
        questions: [],
        contextSource: null,
        sources: [],
        textbookId: null,
        pageId: null,
    };
}

export function createQuizStore(courseId: CourseIdSource, options: QuizStoreOptions = {}): QuizStore {
    const {subscribe, update} = writable<QuizState>(initialState());

    let socket: WebSocketClient<SentMessages, ReceivedMessages> | undefined;
    // Anchor page for the active quiz, used when submitting the result.
    let currentPageId: string | null = null;

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
                currentPageId = message.payload.page_id;
                update((state) => ({
                    ...state,
                    isLoading: false,
                    errorMessage: "",
                    questions: message.payload.questions,
                    contextSource: message.payload.context_source,
                    sources: message.payload.sources,
                    textbookId: message.payload.textbook_id,
                    pageId: message.payload.page_id,
                }));
            });

            socket.setMessageHandler("learning_event_status", (message: LearningEventStatus) => {
                const {event, success, message: detail} = message.payload;

                if (event === "quiz_start") {
                    update((state) => ({
                        ...state,
                        isLoading: false,
                        errorMessage: success ? "" : detail,
                    }));
                    return;
                }

                if (event === "learning_quiz_result") {
                    if (success) {
                        // Points and skill progress were awarded server-side; hand the
                        // earned amounts to the UI and let the dashboard refresh.
                        options.onResultRecorded?.({
                            pointsAwarded: message.payload.points_awarded ?? 0,
                            skillsAdvanced: message.payload.skills_advanced ?? [],
                        });
                    } else {
                        console.error("[quiz] Awarding quiz points failed:", detail);
                    }
                }
            });
        }

        await socket.connect();
    }

    async function disconnect(): Promise<void> {
        await socket?.disconnect();
    }

    async function requestQuiz(questionCount = 5, textbookId?: string): Promise<void> {
        currentPageId = null;
        update((state) => ({
            ...state,
            isLoading: true,
            errorMessage: "",
            questions: [],
            contextSource: null,
            sources: [],
            textbookId: textbookId ?? null,
            pageId: null,
        }));

        try {
            if (!socket) {
                await connect();
            }

            await socket?.send({
                action: "quiz_start",
                payload: {
                    question_count: questionCount,
                    ...(textbookId ? {textbook_id: textbookId} : {}),
                },
            });
        } catch (error) {
            const message = error instanceof Error ? error.message : String(error);
            update((state) => ({...state, isLoading: false, errorMessage: message}));
        }
    }

    /**
     * Submit the finished quiz score so the backend stores it and awards points. The
     * score is normalized to 0–1. Does nothing if the quiz has no anchor page.
     */
    async function submitResult(score: number, attempts?: number): Promise<void> {
        if (!currentPageId) {
            // No anchor page means the quiz wasn't tied to a textbook page, so the
            // backend has nothing to attach the score (and points) to.
            console.warn("[quiz] Result not submitted: this quiz has no anchor page.");
            return;
        }

        const normalized = Math.max(0, Math.min(1, score));

        try {
            // The socket may have gone idle while the learner worked through the quiz.
            // Re-establish it first (a no-op when already connected) so the result is
            // actually delivered instead of being queued on a dead socket and lost.
            await connect();
            await socket?.send({
                action: "learning_quiz_result",
                payload: {
                    page_id: currentPageId,
                    score: normalized,
                    attempts: attempts ?? null,
                },
            });
        } catch (error) {
            // Awarding points is best-effort; never break the quiz UI over it.
            console.error("[quiz] Failed to submit quiz result:", error);
        }
    }

    return {
        subscribe,
        connect,
        disconnect,
        requestQuiz,
        submitResult,
    };
}
