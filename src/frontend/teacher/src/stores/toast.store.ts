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
 * Lightweight, app-wide toast notifications for transient feedback ("Saved", "Deleted",
 * errors). Replaces persistent inline alerts so messages don't linger on screen.
 */

import {writable} from "svelte/store";

export type ToastKind = "success" | "error" | "info";

export interface Toast {
    id: number;
    kind: ToastKind;
    message: string;
}

const {subscribe, update} = writable<Toast[]>([]);

let nextId = 1;

function dismiss(id: number): void {
    update((list) => list.filter((toast) => toast.id !== id));
}

/** Show a toast; it auto-dismisses after a few seconds (errors linger a little longer). */
function show(message: string, kind: ToastKind = "info"): void {
    const id = nextId++;
    update((list) => [...list, {id, kind, message}]);
    const ttl = kind === "error" ? 6000 : 3000;
    setTimeout(() => dismiss(id), ttl);
}

export const toasts = {
    subscribe,
    show,
    success: (message: string) => show(message, "success"),
    error: (message: string) => show(message, "error"),
    info: (message: string) => show(message, "info"),
    dismiss,
};
