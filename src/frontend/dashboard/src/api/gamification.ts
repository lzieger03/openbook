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
 * Raw API data transfer objects (snake_case, as returned by the backend) and
 * the gamification/current-user endpoint calls used by the dashboard.
 */

import {apiGet} from "./client.js";

export interface AccountProgressDto {
    point_total: number;
    level: number;
    current_level_min_points?: number;
    next_level_min_points?: number | null;
}

export interface StreakDto {
    current_streak: number;
    longest_streak: number;
    streak_freezes: number;
    last_active_date: string | null;
}

export interface SkillDto {
    id: string;
    name: string;
    description?: string;
    icon_path?: string;
}

export interface SkillProgressDto {
    id: string;
    account: string;
    skill: string | SkillDto;
    level?: number;
    // DecimalField: serialized as a string such as "66.00".
    progress?: number | string;
}

export interface CourseDto {
    id: string;
    name: string;
    slug?: string;
    // Skills this course teaches; only present when expanded via `course.skills`.
    skills?: SkillDto[];
}

export interface CourseProgressDto {
    id: string;
    account: string;
    course: string | CourseDto;
    course_points?: number;
    course_level?: number;
    // DecimalField: serialized as a string such as "15.00".
    course_progress?: number | string;
}

export interface LeaderboardEntryDto {
    rank: number;
    username: string;
    full_name: string;
    level: number;
    point_total: number;
    is_current_user: boolean;
}

export interface CurrentUserDto {
    username: string;
    full_name: string | null;
    first_name?: string;
    last_name?: string;
    description?: string;
    email?: string;
    picture?: string | null;
    is_authenticated: boolean;
}

interface Paginated<T> {
    results: T[];
}

/** Return the array of items from either a paginated or a plain-list response. */
function toList<T>(data: T[] | Paginated<T>): T[] {
    return Array.isArray(data) ? data : data.results;
}

export function fetchAccountProgress(): Promise<AccountProgressDto> {
    return apiGet<AccountProgressDto>("/api/gamification/account_progress/me/");
}

export async function fetchStreak(): Promise<StreakDto | null> {
    // The streak endpoint returns a single object, but stay tolerant of a list.
    const data = await apiGet<StreakDto | StreakDto[] | Paginated<StreakDto>>("/api/gamification/streak/");

    if (Array.isArray(data)) {
        return data[0] ?? null;
    }

    if ("results" in data) {
        return data.results[0] ?? null;
    }

    return data;
}

export async function fetchSkillProgress(username?: string | null): Promise<SkillProgressDto[]> {
    const query: Record<string, string> = {_expand: "skill", _page_size: "100", _sort: "skill__name"};

    // Scope to the current user so staff accounts do not see everyone's progress.
    if (username) {
        query.account = username;
    }

    const data = await apiGet<SkillProgressDto[] | Paginated<SkillProgressDto>>(
        "/api/gamification/skill_progress/",
        query,
    );
    return toList(data);
}

export async function fetchCourseProgress(username?: string | null): Promise<CourseProgressDto[]> {
    const query: Record<string, string> = {
        // Expand the course; its `skills` (the earnable skills derived from the course's
        // pages) are a read-only field included automatically with the expanded course.
        _expand: "course",
        _page_size: "100",
        _sort: "course__name",
    };

    // Scope to the current user so staff accounts do not see everyone's progress.
    if (username) {
        query.account = username;
    }

    const data = await apiGet<CourseProgressDto[] | Paginated<CourseProgressDto>>(
        "/api/gamification/course_progress/",
        query,
    );
    return toList(data);
}

export async function fetchLeaderboard(): Promise<LeaderboardEntryDto[]> {
    const data = await apiGet<LeaderboardEntryDto[] | Paginated<LeaderboardEntryDto>>(
        "/api/gamification/account_progress/leaderboard/",
    );
    return toList(data);
}

export async function fetchCurrentUser(): Promise<CurrentUserDto | null> {
    // The endpoint may return a paginated list, a plain array, or a single object.
    const data = await apiGet<CurrentUserDto | CurrentUserDto[] | Paginated<CurrentUserDto>>(
        "/api/auth/current_user/",
    );

    if (Array.isArray(data)) {
        return data[0] ?? null;
    }

    if ("results" in data) {
        return data.results[0] ?? null;
    }

    return data;
}
