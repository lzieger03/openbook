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
 * Exam history: the learner's saved AI exams (created server-side via the exam
 * WebSocket). Used to list, review and delete past exams from the exam page.
 */

import {apiGet, apiSend} from "./client.js";
import type {ExamResult} from "../stores/exam.store.js";

export interface ExamAttemptDto {
    id: string;
    course: string | null;
    textbook: string | null;
    title: string;
    result: ExamResult | null;
    total_points: number;
    max_points: number;
    score: number;
    created_at: string;
    updated_at: string;
}

interface Paginated<T> {
    results: T[];
}

/** The learner's saved exams for a course, newest first. */
export async function fetchExamAttempts(courseId: string): Promise<ExamAttemptDto[]> {
    const data = await apiGet<ExamAttemptDto[] | Paginated<ExamAttemptDto>>(
        "/api/assistant/exam_attempts/",
        {course: courseId, _sort: "-updated_at", _page_size: "100"},
    );
    return Array.isArray(data) ? data : data.results;
}

/** Permanently delete a saved exam from the history. */
export async function deleteExamAttempt(id: string): Promise<void> {
    await apiSend<void>("DELETE", `/api/assistant/exam_attempts/${encodeURIComponent(id)}/`);
}
