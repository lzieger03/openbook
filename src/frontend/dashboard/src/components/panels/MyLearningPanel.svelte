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
"My Learning" panel: each course is a clickable card showing its progress and
the skills it teaches (as read-only tags). Clicking a course opens its AI tutor
page. "Current" and "Next Steps" are wired off real data; "Repeat" is still a
placeholder.

The "Next Steps" tab is a "what next?" guide rather than another list: it
synthesises courses, skills and stats into a short, prioritised set of
recommended next steps (finish a course, level up a skill, reach the next level,
keep the streak).
-->
<script lang="ts">
    import ProgressBar from "../basic/ProgressBar.svelte";
    import SegmentedTabs from "../basic/SegmentedTabs.svelte";
    import type {DashboardCourse, DashboardSkill, DashboardStats} from "../../data/dashboard.js";

    let {
        courses,
        skills,
        stats,
        onCourseOpen,
    }: {
        courses: DashboardCourse[];
        skills: DashboardSkill[];
        stats: DashboardStats | null;
        onCourseOpen?: (course: DashboardCourse) => void;
    } = $props();

    const tabs = ["Current", "Next Steps", "Repeat"] as const;
    let activeTab = $state<string>("Current");

    const isEmpty = $derived(courses.length === 0);

    // Show only a few skill tags per course and collapse the rest into a "+N" badge so
    // courses that train many skills don't blow up the card.
    const maxVisibleSkills = 3;

    // A single recommended next step on the "Path" tab. `progress` adds a bar;
    // `course` makes the card clickable (opens that course's tutor page).
    interface Recommendation {
        icon: string;
        title: string;
        detail: string;
        progress?: number;
        course?: DashboardCourse;
    }

    /** Pick the most "finish-able" item: the one with the highest progress below 100. */
    function closestToDone<T extends {progress: number}>(items: T[]): T | undefined {
        return items
            .filter((item) => item.progress > 0 && item.progress < 100)
            .sort((a, b) => b.progress - a.progress)[0];
    }

    // The "Path" guide: a short, prioritised list of next steps synthesised from
    // the loaded data. Only steps that actually apply to this user are shown.
    const recommendations = $derived.by<Recommendation[]>(() => {
        const list: Recommendation[] = [];

        // 1. Finish a course that is already underway, otherwise start a new one.
        const courseInProgress = closestToDone(courses);
        const notStarted = courses.find((course) => course.progress === 0);
        if (courseInProgress) {
            list.push({
                icon: "▶️",
                title: "Finish a course",
                detail: `${courseInProgress.name} — ${Math.round(courseInProgress.progress)}% done, almost there!`,
                course: courseInProgress,
            });
        } else if (notStarted) {
            list.push({
                icon: "▶️",
                title: "Start a new course",
                detail: `Begin ${notStarted.name} and make your first progress.`,
                course: notStarted,
            });
        }

        // 2. Level up the skill closest to its next level.
        const skillToLevel = closestToDone(skills);
        if (skillToLevel) {
            list.push({
                icon: "⬆️",
                title: "Level up a skill",
                detail: `${skillToLevel.name} to Level ${skillToLevel.level + 1} — ${100 - Math.round(skillToLevel.progress)}% to go.`,
            });
        }

        // 3. Reach the next account level (or celebrate the top level).
        if (stats) {
            if (stats.nextLevelPoints === null) {
                list.push({
                    icon: "🏅",
                    title: "Top level reached",
                    detail: `You're at Level ${stats.level} — the highest there is. 🎉`,
                });
            } else {
                const remaining = Math.max(0, stats.nextLevelPoints - stats.points);
                list.push({
                    icon: "⭐",
                    title: "Reach the next level",
                    detail: `${remaining} points to Level ${stats.level + 1}.`,
                    progress: stats.levelProgress,
                });
            }
        }

        // 4. Keep (or start) the daily streak.
        if (stats) {
            if (stats.currentStreak > 0) {
                list.push({
                    icon: "🔥",
                    title: "Keep your streak",
                    detail: `${stats.currentStreak}-day streak — study today to reach ${stats.currentStreak + 1}.`,
                });
            } else {
                list.push({
                    icon: "🔥",
                    title: "Start a streak",
                    detail: "Study today to begin a new daily streak.",
                });
            }
        }

        return list;
    });

    // Mock data for the not-yet-built Repeat tab (shown blurred behind a "Coming soon" notice).
    const repeatItems = [
        {title: "HTML structure", due: "Due today"},
        {title: "CSS selectors", due: "Due in 2 days"},
        {title: "JS functions", due: "New"},
    ];
</script>

<!-- Shared inner markup for a recommendation, rendered inside either a button or a div. -->
{#snippet recInner(rec: Recommendation)}
    <span class="rec-icon" aria-hidden="true">{rec.icon}</span>
    <span class="rec-body">
        <span class="rec-title">{rec.title}</span>
        <span class="rec-detail">{rec.detail}</span>
        {#if rec.progress !== undefined}
            <span class="rec-bar">
                <ProgressBar value={rec.progress} label={rec.title} />
            </span>
        {/if}
    </span>
    {#if rec.course}
        <span class="rec-go" aria-hidden="true">›</span>
    {/if}
{/snippet}

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
                {#each courses as course (course.id)}
                    <button type="button" class="course-card" onclick={() => onCourseOpen?.(course)}>
                        <div class="course-head">
                            <span class="course-title">
                                <span class="course-name">{course.name}</span>
                                <span class="course-level">Level {course.level}</span>
                            </span>
                            <span class="course-bar">
                                <ProgressBar value={course.progress} label={`${course.name} progress`} />
                            </span>
                            <span class="course-percent">{Math.round(course.progress)}%</span>
                            <span class="course-go" aria-hidden="true">›</span>
                        </div>

                        {#if course.skills.length > 0}
                            <div class="course-tags">
                                {#each course.skills.slice(0, maxVisibleSkills) as skill (skill.id)}
                                    <span class="tag">{skill.name}</span>
                                {/each}
                                {#if course.skills.length > maxVisibleSkills}
                                    <span
                                        class="tag tag-more"
                                        title={course.skills
                                            .slice(maxVisibleSkills)
                                            .map((skill) => skill.name)
                                            .join(", ")}
                                    >
                                        +{course.skills.length - maxVisibleSkills}
                                    </span>
                                {/if}
                            </div>
                        {/if}
                    </button>
                {/each}
            {/if}
        {:else if activeTab === "Next Steps"}
            {#if recommendations.length === 0}
                <p class="empty">No next steps yet. Enrol in a course to start your learning path.</p>
            {:else}
                {#each recommendations as rec (rec.title)}
                    {#if rec.course}
                        <button
                            type="button"
                            class="rec-card clickable"
                            onclick={() => onCourseOpen?.(rec.course!)}
                        >
                            {@render recInner(rec)}
                        </button>
                    {:else}
                        <div class="rec-card">
                            {@render recInner(rec)}
                        </div>
                    {/if}
                {/each}
            {/if}
        {:else}
            <!-- Frontend-only: mock content for the Repeat tab, blurred behind a notice. -->
            <div class="locked">
                <div class="locked-content" aria-hidden="true">
                    {#each repeatItems as item (item.title)}
                        <div class="repeat-item">
                            <span class="repeat-title">{item.title}</span>
                            <span class="repeat-due">{item.due}</span>
                        </div>
                    {/each}
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
        grid-template-columns: minmax(0, 14rem) 1fr 3.5rem auto;
        align-items: center;
        gap: 1rem;
    }

    /* Name stacked over its level badge, sharing the first (14rem) grid column. */
    .course-title {
        display: flex;
        flex-direction: column;
        gap: 0.2rem;
        min-width: 0;
    }

    .course-name {
        font-size: 1.6rem;
        font-weight: 700;
        color: var(--color-base-content);
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .course-level {
        align-self: flex-start;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.02em;
        padding: 0.1rem 0.55rem;
        border-radius: 999px;
        color: var(--color-primary);
        background: color-mix(in oklab, var(--color-primary) 14%, transparent);
        border: 1px solid color-mix(in oklab, var(--color-primary) 30%, transparent);
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

    /* Collapsed-overflow badge ("+N"); hint at the hidden skills via its tooltip. */
    .tag-more {
        cursor: default;
        font-weight: 700;
        color: var(--color-primary);
        background: color-mix(in oklab, var(--color-primary) 14%, transparent);
        border-color: color-mix(in oklab, var(--color-primary) 30%, transparent);
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

    /* A recommendation card may render as a <button> (clickable course) or a <div>;
       reset the button chrome so both look identical. */
    .rec-card {
        display: flex;
        align-items: center;
        gap: 1rem;
        width: 100%;
        text-align: left;
        font: inherit;
        padding: 0.9rem 1.1rem;
        border-radius: 1rem;
        background: color-mix(in oklab, var(--color-base-200) 50%, transparent);
        border: 1px solid color-mix(in oklab, var(--color-base-content) 8%, transparent);
    }

    .rec-card.clickable {
        cursor: pointer;
        transition: border-color 0.2s ease, background 0.2s ease;
    }

    .rec-card.clickable:hover {
        background: color-mix(in oklab, var(--color-primary) 12%, transparent);
        border-color: color-mix(in oklab, var(--color-primary) 45%, transparent);
    }

    .rec-card.clickable:focus-visible {
        outline: 2px solid var(--color-primary);
        outline-offset: 2px;
    }

    .rec-icon {
        flex: 0 0 auto;
        display: grid;
        place-items: center;
        width: 2.5rem;
        height: 2.5rem;
        border-radius: 999px;
        font-size: 1.2rem;
        background: color-mix(in oklab, var(--color-primary) 14%, transparent);
    }

    /* Title, detail and optional progress bar stacked, taking the row's free space. */
    .rec-body {
        flex: 1 1 auto;
        min-width: 0;
        display: flex;
        flex-direction: column;
        gap: 0.25rem;
    }

    .rec-title {
        font-weight: 700;
        color: var(--color-base-content);
    }

    .rec-detail {
        font-size: 0.85rem;
        color: color-mix(in oklab, var(--color-base-content) 70%, transparent);
    }

    .rec-bar {
        margin-top: 0.35rem;
    }

    .rec-go {
        flex: 0 0 auto;
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

    .repeat-item {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
        padding: 0.9rem 1.1rem;
        border-radius: 1rem;
        background: color-mix(in oklab, var(--color-base-200) 50%, transparent);
        border: 1px solid color-mix(in oklab, var(--color-base-content) 8%, transparent);
    }

    .repeat-title {
        flex: 1 1 auto;
        font-weight: 600;
        color: var(--color-base-content);
    }

    .repeat-due {
        flex: 0 0 auto;
        font-size: 0.8rem;
        padding: 0.15rem 0.6rem;
        border-radius: 999px;
        color: var(--color-primary);
        background: color-mix(in oklab, var(--color-primary) 14%, transparent);
    }

    /* On narrow screens the progress bar drops onto its own full-width line below the
       course name so nothing is squeezed or clipped. */
    @media (max-width: 38rem) {
        .panel {
            padding: 1.1rem;
            border-radius: 1rem;
        }

        .panel-head {
            flex-wrap: wrap;
        }

        .course-head {
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            gap: 0.4rem 0.75rem;
        }

        .course-title {
            flex: 1 1 auto;
            min-width: 0;
        }

        .course-name {
            font-size: 1.2rem;
        }

        .course-percent {
            order: 2;
        }

        .course-go {
            order: 3;
        }

        .course-bar {
            order: 4;
            flex: 1 1 100%;
        }
    }
</style>
