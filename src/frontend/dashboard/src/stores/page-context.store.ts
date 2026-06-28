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

/** Set the current page context (replaces any previous one). */
export function setPageContext(context: PageContext | null): void {
    pageContext.set(context);
}

/** Clear the current page context (call on page unmount). */
export function clearPageContext(): void {
    pageContext.set(null);
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
