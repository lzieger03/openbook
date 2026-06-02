/*
 * OpenBook: Interactive Online Textbooks - Server
 * © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 */

import backend from "../backend.js";
import type {
    AccountProgressMe,
    CurrentUser,
    PaginatedCurrentUserList,
    StreakState,
} from "../api-client/models/index.js";
import type {
    CourseProgress,
    SkillProgress,
} from "../api-client/models/index.js";

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

type CurrentUserResponse = PaginatedCurrentUserList | CurrentUser;

type SkillProgressRecord = SkillProgress & {skill: string | ExpandedSkill};

type CourseProgressRecord = CourseProgress & {course: string | ExpandedCourse};

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
    if ("results" in response && Array.isArray(response.results)) {
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
        fullName: user.fullName ?? user.username,
        avatarUrl: user.picture ?? null,
        isAuthenticated: Boolean(user.isAuthenticated),
    };
}

function mapStats(progress: AccountProgressMe | null, streak: StreakState | null): DashboardStats | null {
    if (!progress && !streak) {
        return null;
    }

    return {
        points: toNumber(progress?.pointTotal ?? 0),
        level: toNumber(progress?.level ?? 1, 1),
        currentStreak: toNumber(streak?.currentStreak ?? 0),
        longestStreak: toNumber(streak?.longestStreak ?? 0),
        streakFreezes: toNumber(streak?.streakFreezes ?? 0),
        lastActiveDate: streak?.lastActiveDate ?? null,
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
            level: toNumber(record.courseLevel ?? 1, 1),
            points: toNumber(record.coursePoints ?? 0),
            progress: clampPercent(toNumber(record.courseProgress ?? 0)),
        };
    });
}

async function loadCurrentUser(): Promise<DashboardUser | null> {
    const response = await backend.auth.currentUser.authCurrentUser();
    const user = extractCurrentUser(response as CurrentUserResponse);
    return mapUser(user);
}

async function loadAccountProgress(): Promise<AccountProgressMe> {
    return backend.gamification.accountProgress.gamificationAccountProgressMe();
}

async function loadStreakState(): Promise<StreakState | null> {
    const response = await backend.gamification.streak.gamificationStreakRetrieve();
    return response.length > 0 ? response[0] : null;
}

async function loadSkillProgress(): Promise<DashboardSkill[]> {
    const response = await backend.gamification.skillProgress.gamificationSkillProgressList({
        expand: "skill",
        pageSize: 50,
        sort: "skill__name",
    });

    const records = Array.isArray(response.results)
        ? (response.results as SkillProgressRecord[])
        : [];

    return mapSkillProgress(records);
}

async function loadCourseProgress(): Promise<DashboardCourse[]> {
    const response = await backend.gamification.courseProgress.gamificationCourseProgressList({
        expand: "course",
        pageSize: 50,
        sort: "course__name",
    });

    const records = Array.isArray(response.results)
        ? (response.results as CourseProgressRecord[])
        : [];

    return mapCourseProgress(records);
}

export async function loadGamificationDashboardData(): Promise<DashboardPayload> {
    const [user, accountProgress, streak, skills, courses] = await Promise.all([
        loadCurrentUser(),
        loadAccountProgress(),
        loadStreakState(),
        loadSkillProgress(),
        loadCourseProgress(),
    ]);

    return {
        user,
        stats: mapStats(accountProgress, streak),
        skills,
        courses,
    };
}
