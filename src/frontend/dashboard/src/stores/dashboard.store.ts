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
 * Shared dashboard state. The store fetches data via the data layer and exposes
 * loading / error / content state to the UI through a single subscribable value.
 */

import {writable} from "svelte/store";
import {loadDashboardData} from "../data/dashboard.js";
import type {
    DashboardCourse,
    DashboardLeaderboardEntry,
    DashboardSkill,
    DashboardStats,
    DashboardUser,
} from "../data/dashboard.js";

export interface DashboardState {
    isLoading: boolean;
    errorMessage: string;
    user: DashboardUser | null;
    stats: DashboardStats | null;
    skills: DashboardSkill[];
    courses: DashboardCourse[];
    leaderboard: DashboardLeaderboardEntry[];
}

const initialState: DashboardState = {
    isLoading: true,
    errorMessage: "",
    user: null,
    stats: null,
    skills: [],
    courses: [],
    leaderboard: [],
};

const state = writable<DashboardState>(initialState);

function toMessage(error: unknown): string {
    return error instanceof Error ? error.message : String(error);
}

/** Reload all dashboard data, toggling loading and error state accordingly. */
async function refresh(): Promise<void> {
    state.update((current) => ({...current, isLoading: true, errorMessage: ""}));

    try {
        const data = await loadDashboardData();
        state.set({isLoading: false, errorMessage: "", ...data});
    } catch (error) {
        state.update((current) => ({...current, isLoading: false, errorMessage: toMessage(error)}));
    }
}

export const dashboardStore = {
    subscribe: state.subscribe,
    refresh,
};
