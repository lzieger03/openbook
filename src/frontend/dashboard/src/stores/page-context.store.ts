/*
 * OpenBook: Interactive Online Textbooks - Server
 * © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
 * Ledejna Salihi (@LedejnaSalihi)
 * Lars Zieger (@lzieger03)
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 */

/**
 * Tracks what the user is currently looking at, so the global Quick Chat can pass it
 * to the assistant as context. Pages set it on mount / when the visible content
 * changes and clear it on destroy.
 */

import {writable} from "svelte/store";

export interface PageContext {
    /** Short human-readable description, e.g. `Reading "HTML Basics" in "Web Dev"`. */
    label: string;
    /** Optional longer text (e.g. the page content) the assistant can reason about. */
    details?: string;
}

export const pageContext = writable<PageContext | null>(null);

/** Set the current page context (replaces any previous one). Returns the set object
 *  so callers can pass it back to {@link clearPageContext} as a guard token. */
export function setPageContext(context: PageContext): PageContext {
    pageContext.set(context);
    return context;
}

/**
 * Clear the current page context. With a `token`, only clears when it is still the
 * active context — this avoids a page's onDestroy clobbering the context the next
 * page already set (the mount/destroy order across routes is not guaranteed).
 */
export function clearPageContext(token?: PageContext | null): void {
    if (token === undefined) {
        pageContext.set(null);
        return;
    }
    pageContext.update((current) => (current === token ? null : current));
}

/** A course as seen by the dashboard (subset of DashboardCourse), used for context. */
export interface CourseContextInput {
    name: string;
    level?: number;
    progress?: number;
    skills?: {name: string}[];
}

/**
 * Build + set a course-scoped page context for a given activity (e.g. "taking an
 * exam"). Gives the assistant the course it is about plus a short summary, so the
 * Quick Chat is course-aware everywhere inside a course. Returns the token.
 */
export function setCourseContext(activity: string, course: CourseContextInput | undefined): PageContext {
    const name = course?.name ?? "the current course";
    const details: string[] = [];

    if (course) {
        const summary = [`Course: "${course.name}"`];
        if (course.level !== undefined) {
            summary.push(`learner level ${course.level}`);
        }
        if (course.progress !== undefined) {
            summary.push(`${Math.round(course.progress)}% complete`);
        }
        details.push(summary.join(", ") + ".");
        if (course.skills?.length) {
            details.push(`Skills taught in this course: ${course.skills.map((skill) => skill.name).join(", ")}.`);
        }
    }

    return setPageContext({
        label: `The learner is currently ${activity} in the course "${name}".`,
        details: details.join(" ") || undefined,
    });
}

/** Flatten a PageContext into the single string the chat sends to the backend. */
export function formatPageContext(context: PageContext | null): string {
    if (!context) {
        return "";
    }
    const parts = [context.label.trim()];
    if (context.details?.trim()) {
        parts.push(context.details.trim());
    }
    return parts.filter(Boolean).join("\n\n");
}
