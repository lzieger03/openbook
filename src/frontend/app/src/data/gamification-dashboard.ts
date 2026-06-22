/*
 * OpenBook: Interactive Online Textbooks - Server
 * © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 */

export type DashboardUser = {
    username: string;
    fullName: string;
    avatarUrl: string | null;
    isAuthenticated: boolean;
};

export type DashboardStats = {
    points: number;
    level: number;
    currentStreak: number;
    longestStreak: number;
    streakFreezes: number;
    lastActiveDate: Date | null;
};

export type DashboardSkill = {
    id: string;
    name: string;
    description: string;
    iconPath: string;
    level: number;
    progress: number;
};

export type DashboardCourse = {
    id: string;
    name: string;
    level: number;
    points: number;
    progress: number;
};

export type DashboardPayload = {
    user: DashboardUser | null;
    stats: DashboardStats | null;
    skills: DashboardSkill[];
    courses: DashboardCourse[];
};

type AccountProgressMe = {
    point_total: number;
    level: number;
    current_level_min_points?: number;
    next_level_min_points?: number | null;
};

type StreakState = {
    current_streak: number;
    longest_streak: number;
    streak_freezes: number;
    last_active_date: string | null;
};

type CurrentUser = {
    username: string;
    full_name?: string | null;
    picture?: string | null;
    is_authenticated?: boolean;
};

type ExpandedSkill = {
    id: string;
    name: string;
    description?: string;
    icon_path?: string;
};

type ExpandedCourse = {
    id: string;
    name: string;
    slug?: string;
};

type PaginatedResponse<T> = {
    results: T[];
};

type CurrentUserResponse = PaginatedResponse<CurrentUser> | CurrentUser[] | CurrentUser;

type SkillProgressRecord = {
    id: string;
    skill: string | ExpandedSkill;
    level?: number;
    progress?: number | string;
};

type CourseProgressRecord = {
    id: string;
    course: string | ExpandedCourse;
    course_points?: number;
    course_level?: number;
    course_progress?: number | string;
};

let baseUrlPromise: Promise<string> | null = null;

function isLoopbackHost(hostname: string): boolean {
    return hostname === "localhost" || hostname === "127.0.0.1" || hostname === "::1";
}

function normalizeBaseUrl(value: string): string {
    let configuredUrl = new URL(value || window.location.origin, window.location.origin);
    const currentUrl = new URL(window.location.origin);

    if (
        isLoopbackHost(configuredUrl.hostname)
        && isLoopbackHost(currentUrl.hostname)
        && configuredUrl.protocol === currentUrl.protocol
        && configuredUrl.port === currentUrl.port
    ) {
        configuredUrl = currentUrl;
    }

    let url = configuredUrl.toString();

    while (url.endsWith("/")) {
        url = url.slice(0, url.length - 1);
    }

    return url;
}

async function resolveBaseUrl(): Promise<string> {
    const response = await fetch("server.url");

    if (!response.ok) {
        throw new Error(`Could not load backend URL (HTTP ${response.status}).`);
    }

    return normalizeBaseUrl((await response.text()).trim());
}

function getBaseUrl(): Promise<string> {
    if (!baseUrlPromise) {
        baseUrlPromise = resolveBaseUrl();
    }

    return baseUrlPromise;
}

async function apiGet<T>(path: string, query: Record<string, string> = {}): Promise<T> {
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

function hasResults<T>(value: unknown): value is PaginatedResponse<T> {
    const result = value as {results?: unknown};

    return typeof value === "object"
        && value !== null
        && "results" in value
        && Array.isArray(result.results);
}

function toList<T>(value: T[] | PaginatedResponse<T>): T[] {
    return Array.isArray(value) ? value : value.results;
}

function toNumber(value: unknown, fallback = 0): number {
    const numeric = typeof value === "number" ? value : Number(value);
    return Number.isFinite(numeric) ? numeric : fallback;
}

function clampPercent(value: number): number {
    if (!Number.isFinite(value)) {
        return 0;
    }

    return Math.min(100, Math.max(0, value));
}

function toDate(value: string | null | undefined): Date | null {
    if (!value) {
        return null;
    }

    const date = new Date(value);
    return Number.isNaN(date.getTime()) ? null : date;
}

function normalizeSkill(skill: string | ExpandedSkill): ExpandedSkill {
    if (typeof skill === "string") {
        return {
            id: skill,
            name: skill,
            description: "",
            icon_path: "",
        };
    }

    return {
        id: skill.id,
        name: skill.name,
        description: skill.description ?? "",
        icon_path: skill.icon_path ?? "",
    };
}

function normalizeCourse(course: string | ExpandedCourse): ExpandedCourse {
    if (typeof course === "string") {
        return {
            id: course,
            name: course,
            slug: "",
        };
    }

    return {
        id: course.id,
        name: course.name,
        slug: course.slug ?? "",
    };
}

function extractCurrentUser(response: CurrentUserResponse): CurrentUser | null {
    if (Array.isArray(response)) {
        return response[0] ?? null;
    }

    if (hasResults(response)) {
        return response.results[0] ?? null;
    }

    if ("username" in response) {
        return response;
    }

    return null;
}

function mapUser(user: CurrentUser | null): DashboardUser | null {
    if (!user) {
        return null;
    }

    return {
        username: user.username,
        fullName: user.full_name ?? user.username,
        avatarUrl: user.picture ?? null,
        isAuthenticated: Boolean(user.is_authenticated),
    };
}

function mapStats(progress: AccountProgressMe | null, streak: StreakState | null): DashboardStats | null {
    if (!progress && !streak) {
        return null;
    }

    return {
        points: toNumber(progress?.point_total ?? 0),
        level: toNumber(progress?.level ?? 1, 1),
        currentStreak: toNumber(streak?.current_streak ?? 0),
        longestStreak: toNumber(streak?.longest_streak ?? 0),
        streakFreezes: toNumber(streak?.streak_freezes ?? 0),
        lastActiveDate: toDate(streak?.last_active_date),
    };
}

function mapSkillProgress(records: SkillProgressRecord[]): DashboardSkill[] {
    return records.map((record) => {
        const skill = normalizeSkill(record.skill);
        return {
            id: record.id,
            name: skill.name,
            description: skill.description ?? "",
            iconPath: skill.icon_path ?? "",
            level: toNumber(record.level ?? 1, 1),
            progress: clampPercent(toNumber(record.progress ?? 0)),
        };
    });
}

function mapCourseProgress(records: CourseProgressRecord[]): DashboardCourse[] {
    return records.map((record) => {
        const course = normalizeCourse(record.course);
        return {
            id: record.id,
            name: course.name,
            level: toNumber(record.course_level ?? 1, 1),
            points: toNumber(record.course_points ?? 0),
            progress: clampPercent(toNumber(record.course_progress ?? 0)),
        };
    });
}

async function loadCurrentUser(): Promise<DashboardUser | null> {
    const response = await apiGet<CurrentUserResponse>("/api/auth/current_user/");
    const user = extractCurrentUser(response);
    return mapUser(user);
}

async function loadAccountProgress(): Promise<AccountProgressMe> {
    return apiGet<AccountProgressMe>("/api/gamification/account_progress/me/");
}

async function loadStreakState(): Promise<StreakState | null> {
    const response = await apiGet<StreakState | StreakState[] | PaginatedResponse<StreakState>>("/api/gamification/streak/");

    if (Array.isArray(response)) {
        return response[0] ?? null;
    }

    if (hasResults(response)) {
        return response.results[0] ?? null;
    }

    return response;
}

async function loadSkillProgress(username?: string | null): Promise<DashboardSkill[]> {
    const query: Record<string, string> = {
        _expand: "skill",
        _page_size: "50",
        _sort: "skill__name",
    };

    if (username) {
        query.account = username;
    }

    const response = await apiGet<SkillProgressRecord[] | PaginatedResponse<SkillProgressRecord>>(
        "/api/gamification/skill_progress/",
        query,
    );
    const records = toList(response);

    return mapSkillProgress(records);
}

async function loadCourseProgress(username?: string | null): Promise<DashboardCourse[]> {
    const query: Record<string, string> = {
        _expand: "course",
        _page_size: "50",
        _sort: "course__name",
    };

    if (username) {
        query.account = username;
    }

    const response = await apiGet<CourseProgressRecord[] | PaginatedResponse<CourseProgressRecord>>(
        "/api/gamification/course_progress/",
        query,
    );
    const records = toList(response);

    return mapCourseProgress(records);
}

export async function loadGamificationDashboardData(): Promise<DashboardPayload> {
    const user = await loadCurrentUser();
    const [accountProgress, streak, skills, courses] = await Promise.all([
        loadAccountProgress(),
        loadStreakState(),
        loadSkillProgress(user?.username),
        loadCourseProgress(user?.username),
    ]);

    return {
        user,
        stats: mapStats(accountProgress, streak),
        skills,
        courses,
    };
}
