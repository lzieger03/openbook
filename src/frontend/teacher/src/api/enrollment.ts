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
 * Student enrolment for a course. Enrolment is modelled as a role assignment in
 * the course scope: every course gets a scoped "student" role on demand, and
 * enrolling/unenrolling creates or deletes a RoleAssignment for that role.
 */

import {apiGet, apiSend} from "./client.js";

/** Fully-qualified model string used as the role/assignment scope for a course. */
export const COURSE_SCOPE_TYPE = "openbook_content.course";

/** Slug of the per-course role that marks a user as an enrolled student. */
export const STUDENT_ROLE_SLUG = "student";

export interface UserDto {
    username: string;
    full_name: string | null;
    first_name: string;
    last_name: string;
    picture?: string | null;
}

export interface RoleDto {
    id: string;
    slug: string;
    name: string;
    scope_uuid: string;
}

export interface RoleAssignmentDto {
    id: string;
    scope_uuid: string;
    role: string | RoleDto;
    user: string | UserDto;
    is_active: boolean;
    created_at: string;
}

interface Paginated<T> {
    results: T[];
}

function toList<T>(data: T[] | Paginated<T>): T[] {
    return Array.isArray(data) ? data : data.results;
}

/** Search active users by username / name so a teacher can pick who to enrol. */
export async function searchUsers(term: string): Promise<UserDto[]> {
    const query: Record<string, string> = {_page_size: "25", _sort: "username"};

    if (term.trim()) {
        query._search = term.trim();
    }

    const data = await apiGet<UserDto[] | Paginated<UserDto>>("/api/auth/users/", query);
    return toList(data);
}

/** Fetch the scoped student role for a course, or null when it does not exist yet. */
async function findStudentRole(courseId: string): Promise<RoleDto | null> {
    const data = await apiGet<RoleDto[] | Paginated<RoleDto>>("/api/auth/roles/", {
        scope_type: COURSE_SCOPE_TYPE,
        scope_uuid: courseId,
        slug: STUDENT_ROLE_SLUG,
    });
    return toList(data)[0] ?? null;
}

/**
 * Return the course's student role, creating it on first use. The role carries no
 * extra permissions; it simply records that a user is enrolled in the course.
 */
async function ensureStudentRole(courseId: string): Promise<RoleDto> {
    const existing = await findStudentRole(courseId);

    if (existing) {
        return existing;
    }

    return apiSend<RoleDto>("POST", "/api/auth/roles/", {
        scope_type: COURSE_SCOPE_TYPE,
        scope_uuid: courseId,
        slug: STUDENT_ROLE_SLUG,
        name: "Student",
        description: "Enrolled student of this course.",
        text_format: "MD",
        priority: 10,
        is_active: true,
        permissions: [],
    });
}

/** List the students enrolled in a course (active student-role assignments). */
export async function fetchEnrolledStudents(courseId: string): Promise<RoleAssignmentDto[]> {
    const data = await apiGet<RoleAssignmentDto[] | Paginated<RoleAssignmentDto>>(
        "/api/auth/role_assignments/",
        {
            scope_type: COURSE_SCOPE_TYPE,
            scope_uuid: courseId,
            role: STUDENT_ROLE_SLUG,
            _expand: "user",
            _page_size: "200",
        },
    );
    return toList(data);
}

/** Enrol a user into a course as a student. Returns the created assignment. */
export async function enrollStudent(courseId: string, username: string): Promise<RoleAssignmentDto> {
    const role = await ensureStudentRole(courseId);

    return apiSend<RoleAssignmentDto>("POST", "/api/auth/role_assignments/", {
        scope_type: COURSE_SCOPE_TYPE,
        scope_uuid: courseId,
        role: role.slug,
        user: username,
        assignment_method: "manual",
        is_active: true,
    });
}

/** Remove an enrolment by its role-assignment id. */
export async function unenrollStudent(assignmentId: string): Promise<void> {
    await apiSend<void>("DELETE", `/api/auth/role_assignments/${encodeURIComponent(assignmentId)}/`);
}
