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
    quizId: string | null;
    textbookId: string | null;
    pageId: string | null;
}

export interface QuizSubmittedAnswer {
    question_id: string;
    selected_index: number | null;
}

export interface QuizQuestionResult {
    question_id: string;
    selected_index: number | null;
    correct_index: number;
    correct: boolean;
    correct_answer: string;
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
        quiz_id: string;
        answers: QuizSubmittedAnswer[];
        attempts: number | null;
    };
}

interface QuizGenerated {
    action: "quiz_generated";
    payload: {
        quiz_id: string;
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
        score?: number | null;
        correct_count?: number | null;
        question_count?: number | null;
        quiz_results?: QuizQuestionResult[];
    };
}

/** What the learner earned from a submitted quiz, passed to {@link QuizStoreOptions.onResultRecorded}. */
export interface QuizRewardSummary {
    pointsAwarded: number;
    skillsAdvanced: string[];
    score: number;
    correctCount: number;
    questionCount: number;
    results: QuizQuestionResult[];
}

type SentMessages = QuizStart | LearningQuizResult;

type ReceivedMessages = QuizGenerated | LearningEventStatus;

type CourseIdSource = string | (() => string | undefined);

/** Options for {@link createQuizStore}. */
export interface QuizStoreOptions {
    /**
     * Called once the backend has graded a submitted quiz and awarded points/skills.
     */
    onResultRecorded?: (reward: QuizRewardSummary) => void;
}

export interface QuizStore {
    subscribe: (run: (value: QuizState) => void) => () => void;
    connect: () => Promise<void>;
    disconnect: () => Promise<void>;
    requestQuiz: (questionCount?: number, textbookId?: string) => Promise<void>;
    submitResult: (answers: QuizSubmittedAnswer[], attempts?: number) => Promise<void>;
}

function initialState(): QuizState {
    return {
        connection: "disconnected",
        isLoading: false,
        errorMessage: "",
        questions: [],
        contextSource: null,
        sources: [],
        quizId: null,
        textbookId: null,
        pageId: null,
    };
}

export function createQuizStore(courseId: CourseIdSource, options: QuizStoreOptions = {}): QuizStore {
    const {subscribe, update} = writable<QuizState>(initialState());

    let socket: WebSocketClient<SentMessages, ReceivedMessages> | undefined;
    let currentQuizId: string | null = null;

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
                currentQuizId = message.payload.quiz_id;
                update((state) => ({
                    ...state,
                    isLoading: false,
                    errorMessage: "",
                    questions: message.payload.questions,
                    contextSource: message.payload.context_source,
                    sources: message.payload.sources,
                    quizId: message.payload.quiz_id,
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
                        options.onResultRecorded?.({
                            pointsAwarded: message.payload.points_awarded ?? 0,
                            skillsAdvanced: message.payload.skills_advanced ?? [],
                            score: message.payload.score ?? 0,
                            correctCount: message.payload.correct_count ?? 0,
                            questionCount: message.payload.question_count ?? 0,
                            results: message.payload.quiz_results ?? [],
                        });
                    } else {
                        console.error("[quiz] Grading quiz failed:", detail);
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
        currentQuizId = null;
        update((state) => ({
            ...state,
            isLoading: true,
            errorMessage: "",
            questions: [],
            contextSource: null,
            sources: [],
            quizId: null,
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

    async function submitResult(answers: QuizSubmittedAnswer[], attempts?: number): Promise<void> {
        if (!currentQuizId) {
            console.warn("[quiz] Result not submitted: this quiz has no server id.");
            return;
        }

        try {
            await connect();
            await socket?.send({
                action: "learning_quiz_result",
                payload: {
                    quiz_id: currentQuizId,
                    answers,
                    attempts: attempts ?? null,
                },
            });
        } catch (error) {
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
