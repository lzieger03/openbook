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
"My Learning" panel: each course is a clickable card showing its progress and
the skills it teaches (as read-only tags). Clicking a course opens its AI tutor
page. Only the "Current" tab is wired; "Path"/"Repeat" are placeholders.

Note: the backend has no course -> skill relation yet, so the skill tags are
placeholders derived from the available skill names until that data exists.
-->
<script lang="ts">
    import ProgressBar from "../basic/ProgressBar.svelte";
    import SegmentedTabs from "../basic/SegmentedTabs.svelte";
    import type {DashboardCourse, DashboardSkill} from "../../data/dashboard.js";

    let {
        courses,
        skills,
        onCourseOpen,
    }: {
        courses: DashboardCourse[];
        skills: DashboardSkill[];
        onCourseOpen?: (course: DashboardCourse) => void;
    } = $props();

    const tabs = ["Current", "Path", "Repeat"] as const;
    const disabledTabs = ["Path", "Repeat"] as const;

    const isEmpty = $derived(courses.length === 0);

    // Placeholder tag pool: real skills if known, otherwise a generic sample.
    const fallbackPool = ["Grundlagen", "HTML", "CSS", "JavaScript", "SQL", "Datenmodellierung"];
    const tagPool = $derived(skills.length > 0 ? skills.map((skill) => skill.name) : fallbackPool);

    // Deterministic placeholder tags per course (rotates through the pool).
    function courseTags(index: number): string[] {
        const pool = tagPool;
        if (pool.length === 0) {
            return [];
        }

        const count = Math.min(3, pool.length);
        return Array.from({length: count}, (_, offset) => pool[(index + offset) % pool.length]);
    }
</script>

<section class="card panel">
    <header class="panel-head">
        <h2 class="panel-title">My Learning</h2>
        <SegmentedTabs tabs={tabs} active="Current" disabledTabs={disabledTabs} />
    </header>

    <div class="panel-body">
        {#if isEmpty}
            <p class="empty">No courses in progress yet. Enrol in a course to see it here.</p>
        {:else}
            {#each courses as course, index (course.id)}
                <button type="button" class="course-card" onclick={() => onCourseOpen?.(course)}>
                    <div class="course-head">
                        <span class="course-name">{course.name}</span>
                        <span class="course-bar">
                            <ProgressBar value={course.progress} label={`${course.name} progress`} />
                        </span>
                        <span class="course-percent">{Math.round(course.progress)}%</span>
                        <span class="course-go" aria-hidden="true">›</span>
                    </div>

                    <div class="course-tags">
                        {#each courseTags(index) as tag (tag)}
                            <span class="tag">{tag}</span>
                        {/each}
                    </div>
                </button>
            {/each}
        {/if}
    </div>
</section>

<style>
    /* Fill the grid cell at a fixed height; the body scrolls instead of growing. */
    .panel {
        flex: 1;
        min-height: 0;
        display: flex;
        flex-direction: column;
        background: var(--color-base-100);
        border-radius: 1.25rem;
        padding: 1.75rem;
        box-shadow: 0 0 24px color-mix(in oklab, var(--color-primary) 10%, transparent);
    }

    .panel-head {
        flex: 0 0 auto;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
        padding-bottom: 1rem;
        margin-bottom: 0.5rem;
        border-bottom: 1px solid color-mix(in oklab, var(--color-base-content) 8%, transparent);
    }

    .panel-title {
        font-size: 1.5rem;
        font-weight: 700;
        letter-spacing: 0.02em;
        color: var(--color-base-content);
    }

    /* Scroll area: keeps the card a fixed size regardless of how many courses. */
    .panel-body {
        flex: 1;
        min-height: 0;
        overflow-y: auto;
        padding-right: 0.5rem;
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
    }

    .panel-body::-webkit-scrollbar {
        width: 0.5rem;
    }

    .panel-body::-webkit-scrollbar-thumb {
        border-radius: 999px;
        background: color-mix(in oklab, var(--color-base-content) 20%, transparent);
    }

    /* A whole course is one clickable card. */
    .course-card {
        display: block;
        width: 100%;
        text-align: left;
        cursor: pointer;
        background: color-mix(in oklab, var(--color-base-200) 50%, transparent);
        border: 1px solid color-mix(in oklab, var(--color-base-content) 8%, transparent);
        border-radius: 1rem;
        padding: 1rem 1.25rem;
        transition: border-color 0.2s ease, background 0.2s ease;
    }

    .course-card:hover {
        background: color-mix(in oklab, var(--color-primary) 12%, transparent);
        border-color: color-mix(in oklab, var(--color-primary) 45%, transparent);
    }

    .course-card:focus-visible {
        outline: 2px solid var(--color-primary);
        outline-offset: 2px;
    }

    /* Fixed name + percent columns => the 1fr bar column is identical on every row. */
    .course-head {
        display: grid;
        grid-template-columns: 14rem 1fr 3.5rem auto;
        align-items: center;
        gap: 1rem;
    }

    .course-name {
        font-size: 1.6rem;
        font-weight: 700;
        color: var(--color-base-content);
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .course-bar {
        min-width: 0;
    }

    .course-percent {
        font-weight: 700;
        text-align: right;
        color: var(--color-base-content);
    }

    .course-go {
        display: grid;
        place-items: center;
        width: 2rem;
        height: 2rem;
        border-radius: 999px;
        font-size: 1.2rem;
        line-height: 1;
        color: var(--color-primary-content);
        background: var(--color-primary);
        box-shadow: 0 0 12px color-mix(in oklab, var(--color-primary) 45%, transparent);
    }

    .course-tags {
        display: flex;
        flex-wrap: wrap;
        gap: 0.4rem;
        margin-top: 0.75rem;
    }

    .tag {
        font-size: 0.75rem;
        padding: 0.15rem 0.6rem;
        border-radius: 999px;
        color: color-mix(in oklab, var(--color-base-content) 75%, transparent);
        background: color-mix(in oklab, var(--color-base-content) 10%, transparent);
        border: 1px solid color-mix(in oklab, var(--color-base-content) 12%, transparent);
    }

    .empty {
        color: color-mix(in oklab, var(--color-base-content) 60%, transparent);
        padding: 1.5rem 0;
    }
</style>
