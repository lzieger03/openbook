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
 * Centralized theme handling. Defaults to the system colour scheme, lets a
 * stored choice override it, and exposes a store + toggle for the UI. The theme
 * is applied via `data-theme` on the root element.
 */

import {get, writable} from "svelte/store";

const STORAGE_KEY = "openbook-dashboard-theme";
const DARK_QUERY = "(prefers-color-scheme: dark)";

export type Theme = "light" | "dark";

function systemTheme(): Theme {
    return window.matchMedia(DARK_QUERY).matches ? "dark" : "light";
}

function storedTheme(): Theme | null {
    const value = localStorage.getItem(STORAGE_KEY);
    return value === "light" || value === "dark" ? value : null;
}

function applyTheme(value: Theme): void {
    document.documentElement.setAttribute("data-theme", value);
}

/** The active theme. Components subscribe to this to reflect the current choice. */
export const theme = writable<Theme>(storedTheme() ?? systemTheme());

/** Persist and apply a theme choice. */
export function setTheme(value: Theme): void {
    localStorage.setItem(STORAGE_KEY, value);
    applyTheme(value);
    theme.set(value);
}

/** Switch between light and dark. */
export function toggleTheme(): void {
    setTheme(get(theme) === "dark" ? "light" : "dark");
}

/** Apply the initial theme and keep following the system when no choice is stored. */
export function initTheme(): void {
    applyTheme(get(theme));

    window.matchMedia(DARK_QUERY).addEventListener("change", (event) => {
        if (!storedTheme()) {
            const next: Theme = event.matches ? "dark" : "light";
            applyTheme(next);
            theme.set(next);
        }
    });
}
