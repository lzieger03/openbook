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

import {writable} from "svelte/store";
import {
    loadGamificationDashboardData,
    type DashboardCourse,
    type DashboardPayload,
    type DashboardSkill,
    type DashboardStats,
    type DashboardUser,
} from "../data/gamification-dashboard.js";

type GamificationDashboardState = {
    isLoading: boolean;
    errorMessage: string;
    user: DashboardUser | null;
    stats: DashboardStats | null;
    skills: DashboardSkill[];
    courses: DashboardCourse[];
};

const initialState: GamificationDashboardState = {
    isLoading: true,
    errorMessage: "",
    user: null,
    stats: null,
    skills: [],
    courses: [],
};

const dashboardState = writable<GamificationDashboardState>(initialState);

function setLoadingState(): void {
    dashboardState.update((state) => ({
        ...state,
        isLoading: true,
        errorMessage: "",
    }));
}

function setErrorState(errorMessage: string): void {
    dashboardState.update((state) => ({
        ...state,
        isLoading: false,
        errorMessage,
    }));
}

function applyPayload(payload: DashboardPayload): void {
    dashboardState.set({
        isLoading: false,
        errorMessage: "",
        user: payload.user,
        stats: payload.stats,
        skills: payload.skills,
        courses: payload.courses,
    });
}

function toErrorMessage(error: unknown): string {
    if (error instanceof Error) {
        return error.message;
    }

    return String(error);
}

async function refresh(): Promise<void> {
    setLoadingState();

    try {
        const payload = await loadGamificationDashboardData();
        applyPayload(payload);
    } catch (error) {
        setErrorState(toErrorMessage(error));
    }
}

export const gamificationDashboardStore = {
    subscribe: dashboardState.subscribe,
    refresh,
};

export type {GamificationDashboardState};
