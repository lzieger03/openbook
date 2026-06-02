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

    {#if isEmpty}
        <p class="empty">No learning progress yet. Start a course to see it here.</p>
    {:else}
        {#each courses as course (course.id)}
            <div class="course-group">
                <div class="course-head">
                    <span class="course-name">{course.name}</span>
                    <span class="course-percent">{Math.round(course.progress)}%</span>
                </div>
                <ProgressBar value={course.progress} label={`${course.name} progress`} />
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
</section>

<style>
    .panel {
        background: var(--color-base-100);
        border-radius: 1rem;
        padding: 1.5rem;
        box-shadow: 0 0 24px color-mix(in oklab, var(--color-primary) 10%, transparent);
    }

    .panel-head {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
        margin-bottom: 1.25rem;
    }

    .panel-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: var(--color-base-content);
    }

    .course-group {
        margin-bottom: 1.25rem;
    }

    .course-head {
        display: flex;
        align-items: baseline;
        justify-content: space-between;
        margin-bottom: 0.4rem;
    }

    .course-name {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--color-base-content);
    }

    .course-percent {
        font-weight: 700;
        color: var(--color-primary);
    }

    .skill-list {
        list-style: none;
        margin: 0;
        padding: 0;
        border-top: 1px solid color-mix(in oklab, var(--color-base-content) 10%, transparent);
        padding-top: 0.5rem;
    }

    .empty {
        color: color-mix(in oklab, var(--color-base-content) 60%, transparent);
        padding: 1.5rem 0;
    }
</style>
