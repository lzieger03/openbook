<!--
OpenBook: Interactive Online Textbooks - Server
© 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>

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
    import OverviewPanel from "../panels/OverviewPanel.svelte";
    import StudentsPanel from "../panels/StudentsPanel.svelte";
    import ContentPanel from "../panels/ContentPanel.svelte";

    let {params}: {params?: {id?: string}} = $props();

    const courseId = $derived(params?.id ?? "");

    type Tab = "overview" | "students" | "content";
    let tab = $state<Tab>("overview");

    let course = $state<CourseDto | null>(null);
    let isLoading = $state(true);
    let errorMessage = $state("");

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

    // Reload whenever the route's course id changes.
    $effect(() => {
        void courseId;
        load();
    });
</script>

<div class="page">
    <nav class="crumbs">
        <button type="button" class="btn btn-ghost btn-sm" onclick={() => push("/")}>&larr; My Courses</button>
    </nav>

    {#if isLoading}
        <div class="status" role="status" aria-live="polite">
            <span class="loading loading-spinner loading-lg"></span>
        </div>
    {:else if errorMessage}
        <div class="status" role="alert">
            <p class="error">{errorMessage}</p>
            <button type="button" class="btn btn-sm" onclick={load}>Retry</button>
        </div>
    {:else if course}
        <header class="top">
            <h1 class="title">{course.name}</h1>
        </header>

        <div role="tablist" class="tabs tabs-bordered">
            <button role="tab" class="tab" class:tab-active={tab === "overview"} onclick={() => (tab = "overview")}>
                Overview
            </button>
            <button role="tab" class="tab" class:tab-active={tab === "students"} onclick={() => (tab = "students")}>
                Students
            </button>
            <button role="tab" class="tab" class:tab-active={tab === "content"} onclick={() => (tab = "content")}>
                Content
            </button>
        </div>

        <section class="panel-area">
            {#if tab === "overview"}
                <OverviewPanel {course} onSaved={load} />
            {:else if tab === "students"}
                <StudentsPanel {courseId} />
            {:else}
                <ContentPanel {courseId} />
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

    .title {
        font-size: clamp(1.4rem, 3vw, 2rem);
        font-weight: 800;
    }

    .panel-area {
        margin-top: 0.5rem;
    }

    .status {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 1rem;
        padding: 4rem 0;
        color: color-mix(in oklab, var(--color-base-content) 70%, transparent);
    }

    .error {
        color: var(--color-error);
        font-weight: 600;
        text-align: center;
    }
</style>
