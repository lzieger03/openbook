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
 * Derive learning material for the mini-games from a course's *actual* page content
 * (the text teachers authored), not from metadata like skills or page titles.
 *
 * - `loadCourseTerms`     → concise subject terms (headings, bold/emphasis, code,
 *                           short list items) used by Memory and Hangman.
 * - `loadCourseFlashcards`→ heading → section pairs used by Flashcards.
 */

import {loadCourseContent} from "./course-content.js";

const STOP_TERMS = new Set(
    [
        "back",
        "card",
        "click",
        "content",
        "course",
        "download",
        "explanation",
        "home",
        "lesson",
        "next",
        "overview",
        "page",
        "previous",
        "read more",
        "section",
        "term",
        "weiter",
        "zurück",
    ].map((term) => term.toLowerCase()),
);

/** Strip tags + decode the few entities our Markdown renderer emits, collapse spaces. */
function stripHtml(value: string): string {
    return (value ?? "")
        .replace(/<[^>]+>/g, " ")
        .replace(/&amp;/g, "&")
        .replace(/&lt;/g, "<")
        .replace(/&gt;/g, ">")
        .replace(/&quot;/g, '"')
        .replace(/&#39;/g, "'")
        .replace(/&nbsp;/g, " ")
        .replace(/\s+/g, " ")
        .trim();
}

function normalizeTerm(value: string): string {
    return stripHtml(value)
        .replace(/^[\s\-*•·:;,.!?()[\]{}]+/g, "")
        .replace(/[\s\-*•·:;,.!?()[\]{}]+$/g, "")
        .replace(/\s+/g, " ")
        .trim();
}

function isUsefulTerm(value: string, options: {fromList?: boolean} = {}): boolean {
    const term = normalizeTerm(value);
    const lower = term.toLowerCase();
    const words = term.split(/\s+/).filter(Boolean);
    const letters = term.match(/[A-Za-zÄÖÜäöüß]/g)?.length ?? 0;
    const visible = term.replace(/\s/g, "").length;

    if (term.length < 2 || term.length > 36) return false;
    if (STOP_TERMS.has(lower)) return false;
    if (!/[A-Za-zÄÖÜäöüß]/.test(term)) return false;
    if (/https?:|www\.|@/.test(lower)) return false;
    if (/^\d/.test(term)) return false;
    if (visible > 0 && letters / visible < 0.45) return false;
    if (words.length > 4) return false;
    if (options.fromList && (words.length > 3 || /[.!?;:]/.test(term))) return false;
    if (/[.!?]/.test(term) && words.length > 2) return false;

    return true;
}

function isUsefulFlashcard(front: string, back: string): boolean {
    const cleanFront = normalizeTerm(front);
    const cleanBack = stripHtml(back);

    if (!isUsefulTerm(cleanFront)) return false;
    if (cleanBack.length < 24) return false;
    if (cleanBack.toLowerCase() === cleanFront.toLowerCase()) return false;

    return true;
}

/** Concept-like terms from a page's rendered HTML. */
export function extractTerms(html: string): string[] {
    const out: string[] = [];
    const tagRe = /<(h[1-6]|strong|b|em|i|code|li)\b[^>]*>([\s\S]*?)<\/\1>/gi;
    let match: RegExpExecArray | null;
    while ((match = tagRe.exec(html)) !== null) {
        const tag = (match[1] ?? "").toLowerCase();
        const text = normalizeTerm(match[2] ?? "");
        if (isUsefulTerm(text, {fromList: tag === "li"})) {
            out.push(text);
        }
    }
    return out;
}

export interface Flashcard {
    front: string;
    back: string;
}

/**
 * Split a page into heading → section flashcards. Pages without headings become a
 * single card (page title → full text).
 */
export function extractFlashcards(html: string, fallbackTitle: string): Flashcard[] {
    const cards: Flashcard[] = [];
    const headingRe = /<(h[1-6])\b[^>]*>([\s\S]*?)<\/\1>/gi;
    const matches = [...html.matchAll(headingRe)];

    if (matches.length === 0) {
        const text = stripHtml(html);
        const front = normalizeTerm(fallbackTitle) || "Card";
        if (isUsefulFlashcard(front, text)) {
            cards.push({front: front.slice(0, 80), back: text.slice(0, 600)});
        }
        return cards;
    }

    for (let i = 0; i < matches.length; i++) {
        const current = matches[i]!;
        const front = normalizeTerm(current[2] ?? "");
        const start = (current.index ?? 0) + current[0].length;
        const end = i + 1 < matches.length ? (matches[i + 1]!.index ?? html.length) : html.length;
        const back = stripHtml(html.slice(start, end));
        if (isUsefulFlashcard(front, back)) {
            cards.push({front: front.slice(0, 80), back: back.slice(0, 600)});
        }
    }
    return cards;
}

/** Deduplicated, concise subject terms across all pages of a course. */
export async function loadCourseTerms(courseId: string): Promise<string[]> {
    const materials = await loadCourseContent(courseId);

    const seen = new Set<string>();
    const terms: string[] = [];
    for (const material of materials) {
        for (const page of material.pages) {
            for (const raw of extractTerms(page.html)) {
                const term = normalizeTerm(raw);
                const key = term.toLowerCase();
                if (isUsefulTerm(term) && term.length <= 28 && !seen.has(key)) {
                    seen.add(key);
                    terms.push(term);
                }
            }
        }
    }
    return terms;
}

/** Heading → section flashcards across all pages of a course (deduplicated by front). */
export async function loadCourseFlashcards(courseId: string): Promise<Flashcard[]> {
    const materials = await loadCourseContent(courseId);

    const seen = new Set<string>();
    const cards: Flashcard[] = [];
    for (const material of materials) {
        for (const page of material.pages) {
            for (const card of extractFlashcards(page.html, page.title)) {
                const key = card.front.toLowerCase();
                if (!seen.has(key)) {
                    seen.add(key);
                    cards.push(card);
                }
            }
        }
    }
    return cards;
}
