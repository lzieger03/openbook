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
"My Learning" panel: course progress groups plus a list of skill rows. Only the
"Current" tab is wired in v1; "Path" and "Repeat" are inert placeholders.

Note: the backend exposes no skill -> course relation on these endpoints, so
skills are shown as a flat list rather than nested under their course.
-->
<script lang="ts">
    import ProgressBar from "../basic/ProgressBar.svelte";
    import LearningRow from "../basic/LearningRow.svelte";
    import SegmentedTabs from "../basic/SegmentedTabs.svelte";
    import type {DashboardCourse, DashboardSkill} from "../../data/dashboard.js";

    let {courses, skills}: {courses: DashboardCourse[]; skills: DashboardSkill[]} = $props();

    const tabs = ["Current", "Path", "Repeat"] as const;
    const disabledTabs = ["Path", "Repeat"] as const;

    const isEmpty = $derived(courses.length === 0 && skills.length === 0);
</script>

<section class="card panel">
    <header class="panel-head">
        <h2 class="panel-title">My Learning</h2>
        <SegmentedTabs tabs={tabs} active="Current" disabledTabs={disabledTabs} />
    </header>

    <div class="panel-body">
        {#if isEmpty}
            <p class="empty">No learning progress yet. Start a course to see it here.</p>
        {:else}
            {#each courses as course (course.id)}
                <div class="course-group">
                    <div class="course-head">
                        <span class="course-name">{course.name}</span>
                        <span class="course-bar">
                            <ProgressBar value={course.progress} label={`${course.name} progress`} />
                        </span>
                        <span class="course-percent">{Math.round(course.progress)}%</span>
                    </div>
                </div>
            {/each}

            {#if skills.length > 0}
                <ul class="skill-list">
                    {#each skills as skill (skill.id)}
                        <li>
                            <LearningRow label={skill.name} iconPath={skill.iconPath} />
                        </li>
                    {/each}
                </ul>
            {/if}
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

    /* Scroll area: keeps the card a fixed size regardless of how many items. */
    .panel-body {
        flex: 1;
        min-height: 0;
        overflow-y: auto;
        padding-right: 0.5rem;
    }

    .panel-body::-webkit-scrollbar {
        width: 0.5rem;
    }

    .panel-body::-webkit-scrollbar-thumb {
        border-radius: 999px;
        background: color-mix(in oklab, var(--color-base-content) 20%, transparent);
    }

    .course-group {
        margin: 1.25rem 0;
    }

    /* Fixed name + percent columns => the 1fr bar column is identical on every row. */
    .course-head {
        display: grid;
        grid-template-columns: 15rem 1fr 3.5rem;
        align-items: center;
        gap: 1rem;
    }

    .course-name {
        font-size: 1.8rem;
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

    .skill-list {
        list-style: none;
        margin: 0;
        padding: 0;
    }

    .empty {
        color: color-mix(in oklab, var(--color-base-content) 60%, transparent);
        padding: 1.5rem 0;
    }
</style>
