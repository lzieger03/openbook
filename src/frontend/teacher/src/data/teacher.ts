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
 * View models for the teacher area plus the mapping from raw API DTOs. This is
 * the single place that translates backend data into the shape the UI consumes.
 */

import {fetchCourses, fetchCurrentUser} from "../api/courses.js";
import type {CourseDto, CurrentUserDto} from "../api/courses.js";
import {fetchEnrolledStudents} from "../api/enrollment.js";
import type {RoleAssignmentDto, UserDto} from "../api/enrollment.js";
import {fetchMaterials, fetchPageRanges} from "../api/content.js";
import type {CourseMaterialDto, PageRangeDto, TextbookDto, TextbookPageDto} from "../api/content.js";

export interface TeacherUser {
    username: string;
    fullName: string;
    avatarUrl: string | null;
    isAuthenticated: boolean;
}

export interface TeacherCourse {
    id: string;
    name: string;
    description: string;
    group: string;
    materialCount: number;
    isTemplate: boolean;
}

export interface EnrolledStudent {
    assignmentId: string;
    username: string;
    fullName: string;
    avatarUrl: string | null;
}

export interface CourseMaterialView {
    id: string;
    position: number;
    textbookId: string;
    textbookName: string;
    pageRangeCount: number;
}

export interface PageRangeView {
    id: string;
    position: number;
    startPageName: string;
    endPageName: string;
}

export function mapUser(user: CurrentUserDto | null): TeacherUser | null {
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

function mapCourse(course: CourseDto): TeacherCourse {
    return {
        id: course.id,
        name: course.name,
        description: course.description ?? "",
        group: course.group,
        materialCount: course.materials?.length ?? 0,
        isTemplate: Boolean(course.is_template),
    };
}

/** A user reference is either an expanded object or a bare username string. */
function userFullName(user: string | UserDto): {username: string; fullName: string; avatarUrl: string | null} {
    if (typeof user === "string") {
        return {username: user, fullName: user, avatarUrl: null};
    }

    return {
        username: user.username,
        fullName: user.full_name || user.username,
        avatarUrl: user.picture ?? null,
    };
}

function mapStudent(assignment: RoleAssignmentDto): EnrolledStudent {
    const {username, fullName, avatarUrl} = userFullName(assignment.user);
    return {assignmentId: assignment.id, username, fullName, avatarUrl};
}

function textbookName(textbook: string | TextbookDto): {id: string; name: string} {
    if (typeof textbook === "string") {
        return {id: textbook, name: textbook};
    }

    return {id: textbook.id, name: textbook.name};
}

function mapMaterial(material: CourseMaterialDto): CourseMaterialView {
    const {id, name} = textbookName(material.textbook);
    return {
        id: material.id,
        position: material.position,
        textbookId: id,
        textbookName: name,
        pageRangeCount: material.page_ranges?.length ?? 0,
    };
}

function pageName(page: string | TextbookPageDto): string {
    return typeof page === "string" ? page : page.name;
}

function mapPageRange(range: PageRangeDto): PageRangeView {
    return {
        id: range.id,
        position: range.position,
        startPageName: pageName(range.start_page),
        endPageName: pageName(range.end_page),
    };
}

/** Resolve the signed-in teacher. */
export async function loadCurrentUser(): Promise<TeacherUser | null> {
    return mapUser(await fetchCurrentUser());
}

/** Load the courses owned by the given teacher as view models. */
export async function loadCourses(username: string | null): Promise<TeacherCourse[]> {
    const courses = await fetchCourses(username);
    return courses.map(mapCourse);
}

export async function loadStudents(courseId: string): Promise<EnrolledStudent[]> {
    const assignments = await fetchEnrolledStudents(courseId);
    return assignments.map(mapStudent);
}

export async function loadMaterials(courseId: string): Promise<CourseMaterialView[]> {
    const materials = await fetchMaterials(courseId);
    return materials.map(mapMaterial).sort((a, b) => a.position - b.position);
}

export async function loadPageRanges(materialId: string): Promise<PageRangeView[]> {
    const ranges = await fetchPageRanges(materialId);
    return ranges.map(mapPageRange).sort((a, b) => a.position - b.position);
}
