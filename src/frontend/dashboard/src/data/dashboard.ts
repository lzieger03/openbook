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
 * View models for the dashboard plus mapping from the raw API DTOs. This is the
 * single place that translates backend data into the shape the UI consumes.
 */

import {
    fetchAccountProgress,
    fetchCourseProgress,
    fetchCurrentUser,
    fetchLeaderboard,
    fetchSkillProgress,
    fetchStreak,
} from "../api/gamification.js";
import type {
    AccountProgressDto,
    CourseDto,
    CourseProgressDto,
    CurrentUserDto,
    LeaderboardEntryDto,
    SkillDto,
    SkillProgressDto,
    StreakDto,
} from "../api/gamification.js";

export interface DashboardUser {
    username: string;
    fullName: string;
    avatarUrl: string | null;
    isAuthenticated: boolean;
}

export interface DashboardStats {
    points: number;
    level: number;
    // Progress (0–100) towards the next level; resets to 0 on each level-up.
    levelProgress: number;
    // Points required to reach the next level (null at the maximum level).
    nextLevelPoints: number | null;
    currentStreak: number;
    longestStreak: number;
    streakFreezes: number;
    lastActiveDate: Date | null;
}

export interface DashboardSkill {
    id: string;
    name: string;
    iconPath: string;
    level: number;
    progress: number;
}

export interface DashboardCourseSkill {
    id: string;
    name: string;
}

export interface DashboardCourse {
    id: string;
    name: string;
    level: number;
    points: number;
    progress: number;
    skills: DashboardCourseSkill[];
}

export interface DashboardLeaderboardEntry {
    rank: number;
    username: string;
    fullName: string;
    level: number;
    points: number;
    isCurrentUser: boolean;
}

export interface DashboardData {
    user: DashboardUser | null;
    stats: DashboardStats | null;
    skills: DashboardSkill[];
    courses: DashboardCourse[];
    leaderboard: DashboardLeaderboardEntry[];
}

function toNumber(value: number | string | undefined | null, fallback = 0): number {
    // DRF DecimalFields (e.g. progress) arrive as strings like "15.00", so parse them.
    const numeric = typeof value === "number" ? value : Number(value);
    return Number.isFinite(numeric) ? numeric : fallback;
}

function clampPercent(value: number): number {
    return Math.min(100, Math.max(0, value));
}

function mapUser(user: CurrentUserDto | null): DashboardUser | null {
    if (!user) {
        return null;
    }

    return {
        username: user.username,
        fullName: user.full_name || user.username,
        avatarUrl: user.picture ?? null,
        isAuthenticated: Boolean(user.is_authenticated),
    };
}

/** Progress (0–100) from the current level's threshold towards the next one. */
function levelProgress(points: number, progress: AccountProgressDto | null): number {
    const currentMin = toNumber(progress?.current_level_min_points);
    const nextMin = progress?.next_level_min_points;

    // No higher level defined (max level reached) => bar full.
    if (nextMin === null || nextMin === undefined) {
        return 100;
    }

    const span = nextMin - currentMin;
    return span > 0 ? clampPercent(((points - currentMin) / span) * 100) : 0;
}

function mapStats(progress: AccountProgressDto | null, streak: StreakDto | null): DashboardStats | null {
    if (!progress && !streak) {
        return null;
    }

    const points = toNumber(progress?.point_total);

    return {
        points,
        level: toNumber(progress?.level, 1),
        levelProgress: levelProgress(points, progress),
        nextLevelPoints: progress?.next_level_min_points ?? null,
        currentStreak: toNumber(streak?.current_streak),
        longestStreak: toNumber(streak?.longest_streak),
        streakFreezes: toNumber(streak?.streak_freezes),
        lastActiveDate: streak?.last_active_date ? new Date(streak.last_active_date) : null,
    };
}

function skillName(skill: string | SkillDto): {name: string; iconPath: string} {
    if (typeof skill === "string") {
        return {name: skill, iconPath: ""};
    }

    return {name: skill.name, iconPath: skill.icon_path ?? ""};
}

function mapSkills(records: SkillProgressDto[]): DashboardSkill[] {
    return records.map((record) => {
        const {name, iconPath} = skillName(record.skill);
        return {
            id: record.id,
            name,
            iconPath,
            level: toNumber(record.level, 1),
            progress: clampPercent(toNumber(record.progress)),
        };
    });
}

function courseName(course: string | CourseDto): string {
    return typeof course === "string" ? course : course.name;
}

/** Course-scoped routes (chat, quiz, content) key off the real course id, so map it
 *  from the expanded course rather than the progress record's own id. */
function courseId(course: string | CourseDto): string {
    return typeof course === "string" ? course : course.id;
}

/** The skills a course teaches, available only when the course was expanded. */
function courseSkills(course: string | CourseDto): DashboardCourseSkill[] {
    if (typeof course === "string" || !course.skills) {
        return [];
    }

    return course.skills.map((skill) => ({id: skill.id, name: skill.name}));
}

function mapCourses(records: CourseProgressDto[]): DashboardCourse[] {
    return records.map((record) => ({
        id: courseId(record.course),
        name: courseName(record.course),
        level: toNumber(record.course_level, 1),
        points: toNumber(record.course_points),
        progress: clampPercent(toNumber(record.course_progress)),
        skills: courseSkills(record.course),
    }));
}

function mapLeaderboard(records: LeaderboardEntryDto[]): DashboardLeaderboardEntry[] {
    return records.map((record) => ({
        rank: toNumber(record.rank, 1),
        username: record.username,
        fullName: record.full_name || record.username,
        level: toNumber(record.level, 1),
        points: toNumber(record.point_total),
        isCurrentUser: Boolean(record.is_current_user),
    }));
}

/** Load and map every piece of data the dashboard needs. */
export async function loadDashboardData(): Promise<DashboardData> {
    // Resolve the current user first so skill/course progress can be scoped to them.
    const user = await fetchCurrentUser();
    const username = user?.username ?? null;

    const [progress, streak, skills, courses, leaderboard] = await Promise.all([
        fetchAccountProgress(),
        fetchStreak(),
        fetchSkillProgress(username),
        fetchCourseProgress(username),
        fetchLeaderboard(),
    ]);

    // Defence in depth: even if the server returns other accounts' rows (e.g. for
    // staff users), only keep records that belong to the current user.
    const ownSkills = username ? skills.filter((record) => record.account === username) : skills;
    const ownCourses = username ? courses.filter((record) => record.account === username) : courses;

    return {
        user: mapUser(user),
        stats: mapStats(progress, streak),
        skills: mapSkills(ownSkills),
        courses: mapCourses(ownCourses),
        leaderboard: mapLeaderboard(leaderboard),
    };
}
