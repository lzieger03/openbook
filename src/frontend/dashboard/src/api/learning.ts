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
 * Learning-state tracking: report when a learner opens or finishes a page and when
 * they complete a course. The course-completion endpoint also awards gamification
 * points server-side. The current user is taken from the session.
 */

import {apiGet, apiSend} from "./client.js";

export interface LearningStateDto {
    id: string;
    course: string;
    last_page: string | null;
    // Ids of the pages the learner has marked as completed.
    completed_pages: string[];
    is_completed: boolean;
}

interface Paginated<T> {
    results: T[];
}

/** The learner's state for one course, or null if they have none yet. */
export async function fetchLearningState(courseId: string): Promise<LearningStateDto | null> {
    const data = await apiGet<LearningStateDto[] | Paginated<LearningStateDto>>(
        "/api/learning/states/",
        {course: courseId},
    );
    const list = Array.isArray(data) ? data : data.results;
    return list[0] ?? null;
}

/** Record that the learner opened a page (updates their last position). Best-effort. */
export function recordPageOpened(courseId: string, pageId: string): Promise<LearningStateDto> {
    return apiSend<LearningStateDto>("POST", "/api/learning/states/record-page-opened/", {
        course: courseId,
        page: pageId,
    });
}

/** Mark a page as completed; returns the updated state (with completed_pages). */
export function markPageCompleted(courseId: string, pageId: string): Promise<LearningStateDto> {
    return apiSend<LearningStateDto>("POST", "/api/learning/states/mark-page-completed/", {
        course: courseId,
        page: pageId,
    });
}

/** Mark the whole course completed; awards course points server-side (first time only). */
export function completeCourse(courseId: string): Promise<LearningStateDto> {
    return apiSend<LearningStateDto>("POST", "/api/learning/states/complete-course/", {
        course: courseId,
    });
}
