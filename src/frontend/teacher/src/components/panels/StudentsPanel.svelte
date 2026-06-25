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
Students tab: list the students enrolled in a course and enrol new ones via a
user search. Enrolling creates a student-role assignment in the course scope;
unenrolling deletes it.
-->
<script lang="ts">
    import {loadStudents} from "../../data/teacher.js";
    import type {EnrolledStudent} from "../../data/teacher.js";
    import {enrollStudent, searchUsers, unenrollStudent} from "../../api/enrollment.js";
    import type {UserDto} from "../../api/enrollment.js";

    let {courseId}: {courseId: string} = $props();

    let students = $state<EnrolledStudent[]>([]);
    let isLoading = $state(true);
    let error = $state("");

    // Enrolment search state.
    let term = $state("");
    let results = $state<UserDto[]>([]);
    let searching = $state(false);
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
        searching = true;
        try {
            results = await searchUsers(term);
        } catch (e) {
            error = e instanceof Error ? e.message : String(e);
        } finally {
            searching = false;
        }
    }

    async function enroll(username: string): Promise<void> {
        busyUser = username;
        error = "";
        try {
            await enrollStudent(courseId, username);
            await load();
        } catch (e) {
            error = e instanceof Error ? e.message : String(e);
        } finally {
            busyUser = null;
        }
    }

    async function unenroll(student: EnrolledStudent): Promise<void> {
        busyUser = student.username;
        error = "";
        try {
            await unenrollStudent(student.assignmentId);
            await load();
        } catch (e) {
            error = e instanceof Error ? e.message : String(e);
        } finally {
            busyUser = null;
        }
    }
</script>

<div class="grid">
    <!-- Enrolled students -->
    <div class="card bg-base-100 shadow-sm">
        <div class="card-body">
            <h2 class="card-title">Enrolled students</h2>

            {#if error}
                <div class="alert alert-error"><span>{error}</span></div>
            {/if}

            {#if isLoading}
                <span class="loading loading-spinner"></span>
            {:else if students.length === 0}
                <p class="muted">No students enrolled yet.</p>
            {:else}
                <table class="table table-sm">
                    <thead>
                        <tr><th>Name</th><th>Username</th><th></th></tr>
                    </thead>
                    <tbody>
                        {#each students as student (student.assignmentId)}
                            <tr>
                                <td>{student.fullName}</td>
                                <td class="muted">@{student.username}</td>
                                <td class="text-right">
                                    <button
                                        type="button"
                                        class="btn btn-xs btn-ghost text-error"
                                        disabled={busyUser === student.username}
                                        onclick={() => unenroll(student)}
                                    >
                                        Remove
                                    </button>
                                </td>
                            </tr>
                        {/each}
                    </tbody>
                </table>
            {/if}
        </div>
    </div>

    <!-- Enrol a student -->
    <div class="card bg-base-100 shadow-sm">
        <div class="card-body">
            <h2 class="card-title">Enrol a student</h2>

            <div class="search-row">
                <input
                    class="input input-bordered w-full"
                    type="text"
                    placeholder="Search by name or username"
                    bind:value={term}
                    onkeydown={(e) => e.key === "Enter" && runSearch()}
                />
                <button type="button" class="btn btn-primary" onclick={runSearch} disabled={searching}>
                    {#if searching}<span class="loading loading-spinner loading-sm"></span>{/if}
                    Search
                </button>
            </div>

            {#if results.length > 0}
                <ul class="result-list">
                    {#each results as user (user.username)}
                        <li>
                            <span>
                                <strong>{user.full_name || user.username}</strong>
                                <span class="muted">@{user.username}</span>
                            </span>
                            {#if enrolledUsernames.has(user.username)}
                                <span class="badge badge-ghost">Enrolled</span>
                            {:else}
                                <button
                                    type="button"
                                    class="btn btn-xs btn-primary"
                                    disabled={busyUser === user.username}
                                    onclick={() => enroll(user.username)}
                                >
                                    Enrol
                                </button>
                            {/if}
                        </li>
                    {/each}
                </ul>
            {/if}
        </div>
    </div>
</div>

<style>
    .grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
    }

    .search-row {
        display: flex;
        gap: 0.5rem;
    }

    .result-list {
        list-style: none;
        margin: 0.75rem 0 0;
        padding: 0;
        display: flex;
        flex-direction: column;
        gap: 0.4rem;
    }

    .result-list li {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 0.5rem;
        padding: 0.4rem 0.6rem;
        border-radius: 0.5rem;
        background: color-mix(in oklab, var(--color-base-200) 60%, transparent);
    }

    .muted {
        color: color-mix(in oklab, var(--color-base-content) 60%, transparent);
        font-size: 0.85rem;
    }

    @media (max-width: 55rem) {
        .grid {
            grid-template-columns: 1fr;
        }
    }
</style>
