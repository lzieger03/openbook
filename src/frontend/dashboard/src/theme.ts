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
 * Centralized theme handling. Defaults to the system colour scheme and lets a
 * stored choice override it. Applied before render to avoid a flash.
 */

const STORAGE_KEY = "openbook-dashboard-theme";
const DARK_QUERY = "(prefers-color-scheme: dark)";

type Theme = "light" | "dark";

function systemTheme(): Theme {
    return window.matchMedia(DARK_QUERY).matches ? "dark" : "light";
}

function storedTheme(): Theme | null {
    const value = localStorage.getItem(STORAGE_KEY);
    return value === "light" || value === "dark" ? value : null;
}

function applyTheme(theme: Theme): void {
    document.documentElement.setAttribute("data-theme", theme);
}

/** Apply the initial theme and keep following the system when no choice is stored. */
export function initTheme(): void {
    applyTheme(storedTheme() ?? systemTheme());

    window.matchMedia(DARK_QUERY).addEventListener("change", (event) => {
        if (!storedTheme()) {
            applyTheme(event.matches ? "dark" : "light");
        }
    });
}
