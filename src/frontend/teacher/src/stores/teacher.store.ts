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
 * Shared teacher state: the signed-in user and their courses. The store loads
 * data through the data layer and exposes loading / error / content state plus
 * course create / update / delete actions through a single subscribable value.
 */

import {writable} from "svelte/store";
import {loadCourses, loadCurrentUser} from "../data/teacher.js";
import type {TeacherCourse, TeacherUser} from "../data/teacher.js";
import {createCourse, deleteCourse, updateCourse} from "../api/courses.js";
import type {CourseWriteFields} from "../api/courses.js";

export interface TeacherState {
    isLoading: boolean;
    errorMessage: string;
    user: TeacherUser | null;
    courses: TeacherCourse[];
}

const initialState: TeacherState = {
    isLoading: true,
    errorMessage: "",
    user: null,
    courses: [],
};

const state = writable<TeacherState>(initialState);

function toMessage(error: unknown): string {
    return error instanceof Error ? error.message : String(error);
}

let currentUsername: string | null = null;

/** Reload the teacher and their courses, toggling loading and error state. */
async function refresh(): Promise<void> {
    state.update((current) => ({...current, isLoading: true, errorMessage: ""}));

    try {
        const user = await loadCurrentUser();
        currentUsername = user?.username ?? null;
        const courses = await loadCourses(currentUsername);
        state.set({isLoading: false, errorMessage: "", user, courses});
    } catch (error) {
        state.update((current) => ({...current, isLoading: false, errorMessage: toMessage(error)}));
    }
}

async function create(fields: CourseWriteFields): Promise<void> {
    await createCourse(fields);
    await refresh();
}

async function update(id: string, fields: Partial<CourseWriteFields>): Promise<void> {
    await updateCourse(id, fields);
    await refresh();
}

async function remove(id: string): Promise<void> {
    await deleteCourse(id);
    await refresh();
}

export const teacherStore = {
    subscribe: state.subscribe,
    refresh,
    create,
    update,
    remove,
};
