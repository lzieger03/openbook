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
 * Shared Markdown renderer for user-facing text (chat replies, etc.).
 *
 * `html: false` so raw HTML in the source is escaped, not executed — safe to inject
 * the result with `{@html}` even for assistant- or user-provided content.
 */

import MarkdownIt from "markdown-it";

const renderer = new MarkdownIt({
    breaks: true,
    html: false,
    linkify: true,
    typographer: true,
});

/** Render Markdown source to safe HTML. */
export function renderMarkdown(source: string): string {
    return renderer.render(source ?? "");
}
