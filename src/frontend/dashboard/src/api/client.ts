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
