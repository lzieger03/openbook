<!--
OpenBook: Interactive Online Textbooks - Server
© 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
Ledejna Salihi (@LedejnaSalihi)
Lars Zieger (@lzieger03)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.
-->

<!--
@component
Students tab: enrol students via an inline user search and manage the enrolled list.
Enrolling creates a "student" role assignment in the course scope; unenrolling deletes
it. `onChanged` lets the parent refresh its student count.
-->
<script lang="ts">
    import {loadStudents} from "../../data/teacher.js";
    import type {EnrolledStudent} from "../../data/teacher.js";
    import {enrollStudent, searchUsers, unenrollStudent} from "../../api/enrollment.js";
    import type {UserDto} from "../../api/enrollment.js";
    import {toasts} from "../../stores/toast.store.js";

    let {courseId, onChanged}: {courseId: string; onChanged?: () => void} = $props();

    let students = $state<EnrolledStudent[]>([]);
    let isLoading = $state(true);
    let error = $state("");

    // Enrolment search state.
    let term = $state("");
    let results = $state<UserDto[]>([]);
    let searching = $state(false);
    let searched = $state(false);
    let busyUser = $state<string | null>(null);

    async function load(): Promise<void> {
        isLoading = true;
        error = "";
        try {
            students = await loadStudents(courseId);
        } catch (e) {
            error = e instanceof Error ? e.message : String(e);
        } finally {
            isLoading = false;
        }
    }

    $effect(() => {
        void courseId;
        load();
    });

    const enrolledUsernames = $derived(new Set(students.map((s) => s.username)));

    async function runSearch(): Promise<void> {
        if (!term.trim()) {
            return;
        }
        searching = true;
        error = "";
        try {
            results = await searchUsers(term);
            searched = true;
        } catch (e) {
            error = e instanceof Error ? e.message : String(e);
        } finally {
            searching = false;
        }
    }

    async function enroll(user: UserDto): Promise<void> {
        busyUser = user.username;
        try {
            await enrollStudent(courseId, user.username);
            await load();
            onChanged?.();
            toasts.success(`Enrolled ${user.full_name || user.username}.`);
        } catch (e) {
            toasts.error(e instanceof Error ? e.message : String(e));
        } finally {
            busyUser = null;
        }
    }

    async function unenroll(student: EnrolledStudent): Promise<void> {
        if (!confirm(`Remove ${student.fullName} from this course?`)) {
            return;
        }
        busyUser = student.username;
        try {
            await unenrollStudent(student.assignmentId);
            await load();
            onChanged?.();
            toasts.success(`Removed ${student.fullName}.`);
        } catch (e) {
            toasts.error(e instanceof Error ? e.message : String(e));
        } finally {
            busyUser = null;
        }
    }

    function initials(name: string): string {
        return name.trim().charAt(0).toUpperCase() || "?";
    }
</script>

<div class="card bg-base-100 shadow-sm">
    <div class="card-body">
        <!-- Enrol: inline search with results dropdown -->
        <h2 class="card-title">Enrol a student</h2>
        <div class="search-row">
            <input
                class="input input-bordered w-full"
                type="search"
                placeholder="Search by name or username…"
                bind:value={term}
                onkeydown={(e) => e.key === "Enter" && runSearch()}
            />
            <button type="button" class="btn btn-primary" onclick={runSearch} disabled={searching || !term.trim()}>
                {#if searching}<span class="loading loading-spinner loading-sm"></span>{/if}
                Search
            </button>
        </div>

        {#if error}
            <div class="alert alert-error mt-2"><span>{error}</span></div>
        {/if}

        {#if results.length > 0}
            <ul class="result-list">
                {#each results as user (user.username)}
                    <li>
                        <span class="ident">
                            <span class="avatar-dot" aria-hidden="true">{initials(user.full_name || user.username)}</span>
                            <span class="ident-text">
                                <strong>{user.full_name || user.username}</strong>
                                <span class="muted">@{user.username}</span>
                            </span>
                        </span>
                        {#if enrolledUsernames.has(user.username)}
                            <span class="badge badge-ghost">Enrolled</span>
                        {:else}
                            <button
                                type="button"
                                class="btn btn-xs btn-primary"
                                disabled={busyUser === user.username}
                                onclick={() => enroll(user)}
                            >
                                {#if busyUser === user.username}<span class="loading loading-spinner loading-xs"></span>{/if}
                                + Enrol
                            </button>
                        {/if}
                    </li>
                {/each}
            </ul>
        {:else if searched && !searching}
            <p class="muted mt-2">No users match “{term}”.</p>
        {/if}

        <div class="divider"></div>

        <!-- Enrolled list -->
        <div class="list-head">
            <h2 class="card-title">Enrolled students</h2>
            <span class="count-pill">{students.length}</span>
        </div>

        {#if isLoading}
            <span class="loading loading-spinner"></span>
        {:else if students.length === 0}
            <p class="muted">No students enrolled yet — search above to add some.</p>
        {:else}
            <ul class="student-list">
                {#each students as student (student.assignmentId)}
                    <li class="student-row">
                        <span class="ident">
                            <span class="avatar-dot" aria-hidden="true">
                                {#if student.avatarUrl}<img src={student.avatarUrl} alt="" />{:else}{initials(student.fullName)}{/if}
                            </span>
                            <span class="ident-text">
                                <strong>{student.fullName}</strong>
                                <span class="muted">@{student.username}</span>
                            </span>
                        </span>
                        <button
                            type="button"
                            class="btn btn-xs btn-ghost text-error"
                            disabled={busyUser === student.username}
                            onclick={() => unenroll(student)}
                        >
                            {#if busyUser === student.username}<span class="loading loading-spinner loading-xs"></span>{/if}
                            Remove
                        </button>
                    </li>
                {/each}
            </ul>
        {/if}
    </div>
</div>

<style>
    .search-row {
        display: flex;
        gap: 0.5rem;
    }

    .list-head {
        display: flex;
        align-items: center;
        gap: 0.6rem;
    }

    .count-pill {
        font-size: 0.8rem;
        font-weight: 700;
        padding: 0.05rem 0.55rem;
        border-radius: 999px;
        color: var(--color-primary);
        background: color-mix(in oklab, var(--color-primary) 14%, transparent);
    }

    .result-list,
    .student-list {
        list-style: none;
        margin: 0.5rem 0 0;
        padding: 0;
        display: flex;
        flex-direction: column;
        gap: 0.35rem;
    }

    .result-list li,
    .student-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 0.5rem;
        padding: 0.5rem 0.7rem;
        border-radius: 0.6rem;
        background: color-mix(in oklab, var(--color-base-200) 55%, transparent);
        border: 1px solid color-mix(in oklab, var(--color-base-content) 8%, transparent);
    }

    .ident {
        display: flex;
        align-items: center;
        gap: 0.65rem;
        min-width: 0;
    }

    .avatar-dot {
        flex: 0 0 auto;
        display: grid;
        place-items: center;
        width: 2rem;
        height: 2rem;
        border-radius: 999px;
        overflow: hidden;
        font-weight: 700;
        color: var(--color-primary-content);
        background: color-mix(in oklab, var(--color-primary) 70%, transparent);
    }

    .avatar-dot img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    .ident-text {
        display: flex;
        flex-direction: column;
        min-width: 0;
        line-height: 1.25;
    }

    .ident-text .muted {
        font-size: 0.8rem;
    }

    .muted {
        color: color-mix(in oklab, var(--color-base-content) 60%, transparent);
    }
</style>
