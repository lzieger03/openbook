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
 * Course CRUD plus the current-user and library-group lookups the teacher area
 * needs. Courses are scoped to the signed-in teacher via the `created_by` filter.
 */

import {apiGet, apiSend} from "./client.js";

/** Long-text format flag shared by name/description models (Markdown by default). */
export type TextFormat = "TEXT" | "HTML" | "MD";

export interface CourseDto {
    id: string;
    slug: string;
    name: string;
    description: string;
    text_format: TextFormat;
    group: string;
    is_template: boolean;
    materials: string[];
    owner: string | null;
    created_by: string | null;
    created_at: string;
    modified_at: string;
}

export interface LibraryGroupDto {
    id: string;
    name: string;
    slug: string;
    description?: string;
    parent?: string | null;
}

export interface CurrentUserDto {
    username: string;
    full_name: string | null;
    picture?: string | null;
    is_authenticated: boolean;
}

export interface CourseWriteFields {
    slug?: string;
    name: string;
    description: string;
    group: string;
    text_format?: TextFormat;
    is_template?: boolean;
}

export interface LibraryGroupWriteFields {
    slug?: string;
    name: string;
    description: string;
    parent?: string | null;
    text_format?: TextFormat;
}

/** Derive a URL-safe slug from a course name (the backend requires a slug). */
export function slugify(value: string): string {
    const slug = value
        .toLowerCase()
        .normalize("NFKD")
        .replace(/[̀-ͯ]/g, "")
        .replace(/[^a-z0-9]+/g, "-")
        .replace(/^-+|-+$/g, "");

    return slug || "course";
}

interface Paginated<T> {
    results: T[];
}

/** Return the array of items from either a paginated or a plain-list response. */
function toList<T>(data: T[] | Paginated<T>): T[] {
    return Array.isArray(data) ? data : data.results;
}

export async function fetchCurrentUser(): Promise<CurrentUserDto | null> {
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

/** List the courses owned/created by the given teacher (all courses if no user). */
export async function fetchCourses(username?: string | null): Promise<CourseDto[]> {
    const query: Record<string, string> = {_page_size: "200", _sort: "name"};

    if (username) {
        query.created_by = username;
    }

    const data = await apiGet<CourseDto[] | Paginated<CourseDto>>("/api/content/courses/", query);
    return toList(data);
}

export async function fetchCourse(id: string): Promise<CourseDto> {
    return apiGet<CourseDto>(`/api/content/courses/${encodeURIComponent(id)}/`);
}

export async function createCourse(fields: CourseWriteFields): Promise<CourseDto> {
    const slug = fields.slug?.trim() || slugify(fields.name);
    const {slug: _slug, ...payloadFields} = fields;

    return apiSend<CourseDto>("POST", "/api/content/courses/", {
        text_format: "MD",
        is_template: false,
        public_permissions: [],
        ...payloadFields,
        slug,
    });
}

export async function updateCourse(id: string, fields: Partial<CourseWriteFields>): Promise<CourseDto> {
    return apiSend<CourseDto>("PATCH", `/api/content/courses/${encodeURIComponent(id)}/`, fields);
}

export async function deleteCourse(id: string): Promise<void> {
    await apiSend<void>("DELETE", `/api/content/courses/${encodeURIComponent(id)}/`);
}

/** Library groups a course can be filed under (required for creation). */
export async function fetchLibraryGroups(): Promise<LibraryGroupDto[]> {
    const data = await apiGet<LibraryGroupDto[] | Paginated<LibraryGroupDto>>(
        "/api/content/library_groups/",
        {_page_size: "200", _sort: "name"},
    );
    return toList(data);
}

export async function createLibraryGroup(fields: LibraryGroupWriteFields): Promise<LibraryGroupDto> {
    const slug = fields.slug?.trim() || slugify(fields.name);
    const {slug: _slug, ...payloadFields} = fields;

    return apiSend<LibraryGroupDto>("POST", "/api/content/library_groups/", {
        text_format: "MD",
        parent: null,
        public_permissions: [],
        ...payloadFields,
        slug,
    });
}
