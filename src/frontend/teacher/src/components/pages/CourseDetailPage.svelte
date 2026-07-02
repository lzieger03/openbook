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
Course management page. Loads a single course and exposes three tabs:
Overview (edit details), Students (enrol/unenrol) and Content (materials and
page ranges). The active course id comes from the route parameter.
-->
<script lang="ts">
    import {push} from "svelte-spa-router";
    import {fetchCourse} from "../../api/courses.js";
    import type {CourseDto} from "../../api/courses.js";
    import {fetchMaterials} from "../../api/content.js";
    import {loadStudents} from "../../data/teacher.js";
    import OverviewPanel from "../panels/OverviewPanel.svelte";
    import StudentsPanel from "../panels/StudentsPanel.svelte";
    import ContentPanel from "../panels/ContentPanel.svelte";

    let {params}: {params?: {id?: string}} = $props();

    const courseId = $derived(params?.id ?? "");

    // Content is the most-used tab, so it opens first; settings live last.
    type Tab = "content" | "students" | "settings";
    let tab = $state<Tab>("content");

    let course = $state<CourseDto | null>(null);
    let isLoading = $state(true);
    let errorMessage = $state("");

    // At-a-glance counts shown in the summary header and tab badges.
    let textbookCount = $state(0);
    let studentCount = $state(0);
    const skillCount = $derived(course?.skills?.length ?? 0);

    async function load(): Promise<void> {
        if (!courseId) {
            return;
        }

        isLoading = true;
        errorMessage = "";

        try {
            course = await fetchCourse(courseId);
        } catch (error) {
            errorMessage = error instanceof Error ? error.message : String(error);
        } finally {
            isLoading = false;
        }
    }

    /** Refresh the summary counts (called on load and after content/student changes). */
    async function loadStats(): Promise<void> {
        if (!courseId) {
            return;
        }
        try {
            const [materials, students] = await Promise.all([
                fetchMaterials(courseId),
                loadStudents(courseId),
            ]);
            textbookCount = materials.length;
            studentCount = students.length;
        } catch {
            // Counts are non-critical; leave whatever we had.
        }
    }

    // Reload whenever the route's course id changes.
    $effect(() => {
        void courseId;
        load();
        void loadStats();
    });
</script>

<div class="page">
    <nav class="crumbs">
        <button type="button" class="btn btn-ghost btn-sm" onclick={() => push("/")}>&larr; My Courses</button>
    </nav>

    {#if isLoading}
        <div class="status-box" role="status" aria-live="polite">
            <span class="loading loading-spinner loading-lg"></span>
        </div>
    {:else if errorMessage}
        <div class="status-box" role="alert">
            <p class="error">{errorMessage}</p>
            <button type="button" class="btn btn-sm" onclick={load}>Retry</button>
        </div>
    {:else if course}
        <header class="top">
            <h1 class="title">{course.name}</h1>
            {#if course.is_template}<span class="template-badge">Template</span>{/if}
        </header>

        <div class="summary">
            <span class="summary-stat"><strong>{textbookCount}</strong> Textbooks</span>
            <span class="summary-sep" aria-hidden="true">·</span>
            <span class="summary-stat"><strong>{studentCount}</strong> Students</span>
            <span class="summary-sep" aria-hidden="true">·</span>
            <span class="summary-stat"><strong>{skillCount}</strong> Skills</span>
        </div>

        <div role="tablist" class="tabs tabs-bordered">
            <button role="tab" class="tab" class:tab-active={tab === "content"} onclick={() => (tab = "content")}>
                Content {#if textbookCount > 0}<span class="tab-badge">{textbookCount}</span>{/if}
            </button>
            <button role="tab" class="tab" class:tab-active={tab === "students"} onclick={() => (tab = "students")}>
                Students {#if studentCount > 0}<span class="tab-badge">{studentCount}</span>{/if}
            </button>
            <button role="tab" class="tab" class:tab-active={tab === "settings"} onclick={() => (tab = "settings")}>
                Settings
            </button>
        </div>

        <section class="panel-area">
            {#if tab === "content"}
                <ContentPanel {courseId} courseGroupId={course.group} onChanged={loadStats} />
            {:else if tab === "students"}
                <StudentsPanel {courseId} onChanged={loadStats} />
            {:else}
                <OverviewPanel {course} onSaved={() => { load(); loadStats(); }} />
            {/if}
        </section>
    {/if}
</div>

<style>
    .page {
        width: 90%;
        max-width: 70rem;
        margin: 0 auto;
        padding: 1.25rem 0 2rem;
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }

    .crumbs {
        display: flex;
    }

    .top {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }

    .title {
        font-size: clamp(1.4rem, 3vw, 2rem);
        font-weight: 800;
    }

    .template-badge {
        font-size: 0.65rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        padding: 0.15rem 0.55rem;
        border-radius: 999px;
        color: var(--color-warning);
        background: color-mix(in oklab, var(--color-warning) 16%, transparent);
    }

    /* At-a-glance summary under the title. */
    .summary {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        font-size: 0.9rem;
        color: color-mix(in oklab, var(--color-base-content) 70%, transparent);
        margin-top: -0.25rem;
    }

    .summary-stat strong {
        color: var(--color-base-content);
        font-weight: 800;
    }

    .summary-sep {
        color: color-mix(in oklab, var(--color-base-content) 35%, transparent);
    }

    /* Count badge inside a tab label. */
    .tab-badge {
        margin-left: 0.4rem;
        font-size: 0.7rem;
        font-weight: 700;
        padding: 0.05rem 0.45rem;
        border-radius: 999px;
        color: var(--color-primary);
        background: color-mix(in oklab, var(--color-primary) 16%, transparent);
    }

    .panel-area {
        margin-top: 0.5rem;
    }

    .status-box {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 1rem;
        padding: 4rem 1rem;
        text-align: center;
        color: color-mix(in oklab, var(--color-base-content) 70%, transparent);
    }

    .error {
        color: var(--color-error);
        font-weight: 600;
        text-align: center;
    }
</style>
