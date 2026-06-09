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
 * Minimal typed fetch client for the OpenBook REST API. The backend base URL is
 * read once from the static `server.url` file (same convention as the main app).
 * Only GET requests are used, so no CSRF token is needed; the session cookie is
 * sent automatically for same-origin requests.
 */

let baseUrlPromise: Promise<string> | null = null;

async function resolveBaseUrl(): Promise<string> {
    const response = await fetch("server.url");

    if (!response.ok) {
        throw new Error(`Could not load backend URL (HTTP ${response.status}).`);
    }

    let url = (await response.text()).trim();

    while (url.endsWith("/")) {
        url = url.slice(0, url.length - 1);
    }

    return url;
}

function getBaseUrl(): Promise<string> {
    if (!baseUrlPromise) {
        baseUrlPromise = resolveBaseUrl();
    }

    return baseUrlPromise;
}

/** Perform a typed GET request against the API and return the parsed JSON body. */
export async function apiGet<T>(path: string, query: Record<string, string> = {}): Promise<T> {
    const base = await getBaseUrl();
    const url = new URL(`${base}${path}`);

    for (const [key, value] of Object.entries(query)) {
        url.searchParams.set(key, value);
    }

    const response = await fetch(url.toString(), {
        credentials: "include",
        headers: {Accept: "application/json"},
    });

    if (response.status === 401 || response.status === 403) {
        throw new Error("You are not signed in. Please log in to view your dashboard.");
    }

    if (!response.ok) {
        throw new Error(`Request to ${path} failed (HTTP ${response.status}).`);
    }

    return (await response.json()) as T;
}

/** Read a cookie value by name (used for the CSRF token on write requests). */
function readCookie(name: string): string {
    const match = document.cookie.match(new RegExp(`(?:^|; )${name}=([^;]*)`));
    const value = match?.[1];
    return value ? decodeURIComponent(value) : "";
}

/** Best-effort extraction of a human-readable message from an API error body. */
function extractError(data: unknown): string {
    if (typeof data === "string") {
        return data;
    }

    if (data && typeof data === "object") {
        const record = data as Record<string, unknown>;

        if (typeof record.detail === "string") {
            return record.detail;
        }

        // allauth wraps errors as {errors: [{message}]}.
        if (Array.isArray(record.errors)) {
            const messages = record.errors
                .map((entry) => (entry && typeof entry === "object" ? String((entry as Record<string, unknown>).message ?? "") : ""))
                .filter(Boolean);
            if (messages.length > 0) {
                return messages.join(" ");
            }
        }

        // DRF field errors: {field: ["msg", ...]}.
        const fieldMessages = Object.values(record)
            .flatMap((value) => (Array.isArray(value) ? value : [value]))
            .filter((value): value is string => typeof value === "string");
        if (fieldMessages.length > 0) {
            return fieldMessages.join(" ");
        }
    }

    return "";
}

type WriteMethod = "POST" | "PUT" | "PATCH" | "DELETE";

/**
 * Perform a typed write request. JSON bodies are serialized automatically; pass a
 * `FormData` body with `{formData: true}` for multipart uploads. The CSRF token is
 * read from the cookie and the session cookie is sent for authentication.
 */
export async function apiSend<T>(
    method: WriteMethod,
    path: string,
    body?: unknown,
    options: {formData?: boolean} = {},
): Promise<T> {
    const base = await getBaseUrl();

    const headers: Record<string, string> = {
        Accept: "application/json",
        "X-CSRFToken": readCookie("csrftoken"),
    };

    let payload: BodyInit | undefined;

    if (options.formData && body instanceof FormData) {
        payload = body; // The browser sets the multipart Content-Type with boundary.
    } else if (body !== undefined) {
        headers["Content-Type"] = "application/json";
        payload = JSON.stringify(body);
    }

    const response = await fetch(`${base}${path}`, {
        method,
        credentials: "include",
        headers,
        body: payload,
    });

    if (!response.ok) {
        const data = await response.json().catch(() => null);
        throw new Error(extractError(data) || `Request to ${path} failed (HTTP ${response.status}).`);
    }

    if (response.status === 204) {
        return undefined as T;
    }

    return (await response.json().catch(() => undefined)) as T;
}
