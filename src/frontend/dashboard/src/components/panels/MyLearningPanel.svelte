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
    let activeTab = $state<string>("Current");

    const isEmpty = $derived(courses.length === 0);

    // Mock data for the not-yet-built tabs (shown blurred behind a "Coming soon" notice).
    const pathSteps = [
        {step: 1, title: "Foundations", status: "Completed"},
        {step: 2, title: "Core concepts", status: "In progress"},
        {step: 3, title: "Hands-on practice", status: "Locked"},
        {step: 4, title: "Mastery project", status: "Locked"},
    ];
    const repeatItems = [
        {title: "HTML structure", due: "Due today"},
        {title: "CSS selectors", due: "Due in 2 days"},
        {title: "JS functions", due: "New"},
    ];

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
        <SegmentedTabs tabs={tabs} active={activeTab} onSelect={(tab) => (activeTab = tab)} />
    </header>

    <div class="panel-body">
        {#if activeTab === "Current"}
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
        {:else}
            <!-- Frontend-only: mock content for the unfinished tabs, blurred behind a notice. -->
            <div class="locked">
                <div class="locked-content" aria-hidden="true">
                    {#if activeTab === "Path"}
                        {#each pathSteps as item (item.step)}
                            <div class="path-step">
                                <span class="step-num">{item.step}</span>
                                <span class="step-title">{item.title}</span>
                                <span class="step-status">{item.status}</span>
                            </div>
                        {/each}
                    {:else}
                        {#each repeatItems as item (item.title)}
                            <div class="repeat-item">
                                <span class="repeat-title">{item.title}</span>
                                <span class="repeat-due">{item.due}</span>
                            </div>
                        {/each}
                    {/if}
                </div>
                <div class="locked-overlay" role="status">
                    <span class="overlay-badge">🚧 Coming soon</span>
                    <span class="overlay-note">{activeTab} mode is in the works.</span>
                </div>
            </div>
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
        /* Firefox: keep the track transparent so the bar only shows on hover. */
        scrollbar-width: thin;
        scrollbar-color: transparent transparent;
    }

    .panel-body:hover {
        scrollbar-color: color-mix(in oklab, var(--color-base-content) 20%, transparent) transparent;
    }

    .panel-body::-webkit-scrollbar {
        width: 0.5rem;
    }

    .panel-body::-webkit-scrollbar-thumb {
        border-radius: 999px;
        background: transparent;
    }

    .panel-body:hover::-webkit-scrollbar-thumb {
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

    /* Mock content for Path/Repeat, blurred behind a "Coming soon" overlay. */
    .locked {
        position: relative;
        flex: 1;
        min-height: 0;
    }

    .locked-content {
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
        filter: blur(5px);
        opacity: 0.5;
        pointer-events: none;
        user-select: none;
    }

    .locked-overlay {
        position: absolute;
        inset: 0;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        text-align: center;
    }

    .overlay-badge {
        padding: 0.4rem 1rem;
        border-radius: 999px;
        font-weight: 700;
        letter-spacing: 0.04em;
        color: var(--color-warning);
        background: color-mix(in oklab, var(--color-warning) 16%, transparent);
        border: 1px solid color-mix(in oklab, var(--color-warning) 40%, transparent);
    }

    .overlay-note {
        font-size: 0.85rem;
        color: color-mix(in oklab, var(--color-base-content) 70%, transparent);
    }

    .path-step,
    .repeat-item {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 0.9rem 1.1rem;
        border-radius: 1rem;
        background: color-mix(in oklab, var(--color-base-200) 50%, transparent);
        border: 1px solid color-mix(in oklab, var(--color-base-content) 8%, transparent);
    }

    .repeat-item {
        justify-content: space-between;
    }

    .step-num {
        display: grid;
        place-items: center;
        width: 2rem;
        height: 2rem;
        flex: 0 0 auto;
        border-radius: 999px;
        font-weight: 700;
        color: var(--color-primary-content);
        background: var(--color-primary);
    }

    .step-title,
    .repeat-title {
        flex: 1 1 auto;
        font-weight: 600;
        color: var(--color-base-content);
    }

    .step-status {
        font-size: 0.8rem;
        color: color-mix(in oklab, var(--color-base-content) 65%, transparent);
    }

    .repeat-due {
        flex: 0 0 auto;
        font-size: 0.8rem;
        padding: 0.15rem 0.6rem;
        border-radius: 999px;
        color: var(--color-primary);
        background: color-mix(in oklab, var(--color-primary) 14%, transparent);
    }
</style>
