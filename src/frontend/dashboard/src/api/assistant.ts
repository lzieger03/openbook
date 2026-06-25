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
 * AI assistant (chat) integration.
 *
 * The backend / webhook does not exist yet. To activate the chat once it does:
 *   1. set ASSISTANT_ENABLED = true;
 *   2. point ASSISTANT_ENDPOINT at the real REST endpoint or webhook URL;
 *   3. if the response field name differs, add it in `extractReply` below.
 * Everything else (composer, message list, history, CSRF, errors) is already wired.
 */

import {apiSend} from "./client.js";

// ── Backend integration point ────────────────────────────────────────────────
/** Flip to true when the assistant backend is reachable. */
export const ASSISTANT_ENABLED = false;
/** REST endpoint or webhook the chat posts to (adjust to the real contract). */
const ASSISTANT_ENDPOINT = "/api/assistant/chat/";
// ─────────────────────────────────────────────────────────────────────────────

export interface ChatMessage {
    role: "user" | "assistant";
    content: string;
}

interface ChatRequest {
    message: string;
    context?: string;
    history: ChatMessage[];
}

interface ChatResponse {
    // Accept several common field names so matching the backend is a one-liner.
    reply?: string;
    answer?: string;
    message?: string;
    content?: string;
}

function extractReply(data: ChatResponse): string {
    return (data.reply ?? data.answer ?? data.message ?? data.content ?? "").trim();
}

/**
 * Send a message to the assistant and return its reply text. `context` can carry
 * grounding info (e.g. the course name); `history` is the prior conversation.
 */
export async function sendChatMessage(
    message: string,
    context?: string,
    history: ChatMessage[] = [],
): Promise<string> {
    const payload: ChatRequest = {message, context, history};
    const data = await apiSend<ChatResponse>("POST", ASSISTANT_ENDPOINT, payload);
    return extractReply(data) || "(no response)";
}
