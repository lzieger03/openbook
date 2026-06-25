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
Gamification dashboard for the current user.
-->
<script lang="ts">
    import {onMount} from "svelte";
    import {push} from "svelte-spa-router";
    import {gamificationDashboardStore} from "../../../stores/gamification-dashboard.store.js";

    type RadarAxis = {
        x: number;
        y: number;
        label: string;
        anchor: "start" | "middle" | "end";
    };

    type RadarConfig = {
        rings: string[];
        axes: Array<{x: number; y: number}>;
        labels: RadarAxis[];
        polygon: string;
    };

    const dashboardStore = gamificationDashboardStore;
    const tabOptions = ["Current", "Path", "Repeat"] as const;
    const numberFormatter = new Intl.NumberFormat(undefined, {maximumFractionDigits: 0});

    onMount(() => {
        dashboardStore.refresh();
    });

    const dashboardState = $derived(() => $dashboardStore);

    const displayHandle = $derived(() => {
        const username = dashboardState.user?.username;
        return username ? `@${username}` : "@user";
    });

    const displayName = $derived(() => {
        return dashboardState.user?.fullName || "Learner";
    });

    const pointsMax = $derived(() => {
        const points = dashboardState.stats?.points ?? 0;
        if (points <= 1000) {
            return 1000;
        }

        return Math.ceil(points / 1000) * 1000;
    });

    const isEmptyState = $derived(() => {
        return !dashboardState.isLoading
            && !dashboardState.errorMessage
            && dashboardState.skills.length === 0
            && dashboardState.courses.length === 0;
    });

    const radar = $derived(() => buildRadarConfig(dashboardState.skills.map((skill) => ({
        label: skill.name,
        value: skill.progress,
    }))));

    function formatNumber(value: number): string {
        return numberFormatter.format(value);
    }

    function courseInitials(name: string): string {
        return name
            .split(" ")
            .filter(Boolean)
            .slice(0, 2)
            .map((part) => part[0]?.toUpperCase() ?? "")
            .join("");
    }

    function formatDate(value: Date | null): string {
        if (!value) {
            return "--";
        }

        return new Intl.DateTimeFormat(undefined, {month: "short", day: "2-digit"}).format(value);
    }

    function goToProfile(): void {
        push("/profile");
    }

    function openCourse(courseId: string): void {
        push(`/courses/${courseId}`);
    }

    function buildRadarConfig(data: Array<{label: string; value: number}>): RadarConfig {
        const labels = data.length > 0
            ? data.slice(0, 5)
            : [
                {label: "HTML", value: 0},
                {label: "CSS", value: 0},
                {label: "JS", value: 0},
                {label: "UX", value: 0},
                {label: "DB", value: 0},
            ];

        const size = 200;
        const center = size / 2;
        const radius = 70;
        const axisCount = labels.length;

        const axisPoints = labels.map((_, index) => {
            const angle = (Math.PI * 2 * index) / axisCount - Math.PI / 2;
            return {
                x: center + Math.cos(angle) * radius,
                y: center + Math.sin(angle) * radius,
            };
        });

        const rings = [0.2, 0.4, 0.6, 0.8, 1].map((step) => {
            return buildPolygon(labels.map((item) => item.value * step), axisCount, radius, center);
        });

        const polygon = buildPolygon(labels.map((item) => item.value), axisCount, radius, center);

        const axisLabels = labels.map((item, index) => {
            const angle = (Math.PI * 2 * index) / axisCount - Math.PI / 2;
            const x = center + Math.cos(angle) * (radius + 18);
            const y = center + Math.sin(angle) * (radius + 18);
            const anchor: RadarAxis["anchor"] = Math.abs(Math.cos(angle)) < 0.2
                ? "middle"
                : Math.cos(angle) > 0
                    ? "start"
                    : "end";

            return {
                x,
                y,
                label: item.label,
                anchor,
            };
        });

        return {
            rings,
            axes: axisPoints,
            labels: axisLabels,
            polygon,
        };
    }

    function buildPolygon(values: number[], axisCount: number, radius: number, center: number): string {
        return values
            .slice(0, axisCount)
            .map((value, index) => {
                const normalized = Math.min(100, Math.max(0, value)) / 100;
                const angle = (Math.PI * 2 * index) / axisCount - Math.PI / 2;
                const x = center + Math.cos(angle) * radius * normalized;
                const y = center + Math.sin(angle) * radius * normalized;
                return `${x.toFixed(2)},${y.toFixed(2)}`;
            })
            .join(" ");
    }
</script>

<section class="dashboard-shell">
    <div class="dashboard-gridlines" aria-hidden="true"></div>

    <div class="dashboard-content">
        <header class="dashboard-hero">
            <div>
                <p class="hero-kicker">User Dashboard</p>
                <h1 class="hero-title">{displayHandle} Dashboard</h1>
                <p class="hero-subtitle">Adaptive gamification metrics for your learning journey.</p>
            </div>
            <div class="hero-tabs">
                {#each tabOptions as tab}
                    <button class="btn btn-sm btn-ghost" type="button">{tab}</button>
                {/each}
            </div>
        </header>

        {#if dashboardState.isLoading}
            <div class="dashboard-loading">
                <div class="loading-panel skeleton"></div>
                <div class="loading-panel skeleton"></div>
            </div>
        {:else if dashboardState.errorMessage}
            <div class="alert alert-error">
                <span>{dashboardState.errorMessage}</span>
                <button class="btn btn-sm" type="button" onclick={() => dashboardStore.refresh()}>
                    Retry
                </button>
            </div>
        {:else if isEmptyState}
            <div class="alert alert-info">
                <span>No gamification progress available yet.</span>
                <button class="btn btn-sm" type="button" onclick={() => dashboardStore.refresh()}>
                    Refresh
                </button>
            </div>
        {:else}
            <div class="dashboard-grid">
                <section class="dashboard-panel panel-learning">
                    <div class="panel-head">
                        <h2>My Learning</h2>
                        <div class="panel-meta">
                            <span>Current</span>
                            <span>Path</span>
                            <span>Repeat</span>
                        </div>
                    </div>

                    {#if dashboardState.courses.length === 0}
                        <p class="panel-empty">No course progress found.</p>
                    {:else}
                        <div class="learning-list">
                            {#each dashboardState.courses as course (course.id)}
                                <article class="learning-item">
                                    <div class="learning-icon">
                                        <span>{courseInitials(course.name)}</span>
                                    </div>
                                    <div class="learning-details">
                                        <div class="learning-title">
                                            <strong>{course.name}</strong>
                                            <span>Level {course.level}</span>
                                        </div>
                                        <progress
                                            class="progress progress-primary"
                                            value={course.progress}
                                            max="100"
                                        ></progress>
                                    </div>
                                    <button
                                        class="btn btn-circle btn-ghost"
                                        type="button"
                                        aria-label={`Open ${course.name}`}
                                        onclick={() => openCourse(course.id)}
                                    >
                                        <span aria-hidden="true">&rarr;</span>
                                    </button>
                                </article>
                            {/each}
                        </div>
                    {/if}
                </section>

                <section class="dashboard-side">
                    <div class="dashboard-panel panel-stats">
                        <div class="panel-head">
                            <h2>Your Stats</h2>
                            <button class="btn btn-xs btn-outline" type="button" onclick={goToProfile}>
                                Go to Profile
                            </button>
                        </div>

                        <div class="stats-user">
                            <div class="avatar">
                                {#if dashboardState.user?.avatarUrl}
                                    <img src={dashboardState.user.avatarUrl} alt="" />
                                {:else}
                                    <div class="avatar-fallback">{displayHandle.slice(1, 3)}</div>
                                {/if}
                            </div>
                            <div>
                                <div class="stats-name">{displayName}</div>
                                <div class="stats-level">Level {dashboardState.stats?.level ?? 1}</div>
                            </div>
                        </div>

                        <div class="stats-progress">
                            <div class="stats-progress-row">
                                <span>Points</span>
                                <span>{formatNumber(dashboardState.stats?.points ?? 0)}</span>
                            </div>
                            <progress
                                class="progress progress-accent"
                                value={dashboardState.stats?.points ?? 0}
                                max={pointsMax}
                            ></progress>
                        </div>

                        <div class="stats-grid">
                            <div class="stat-pill">
                                <span class="stat-label">Streak</span>
                                <span class="stat-value">{dashboardState.stats?.currentStreak ?? 0}</span>
                            </div>
                            <div class="stat-pill">
                                <span class="stat-label">Best</span>
                                <span class="stat-value">{dashboardState.stats?.longestStreak ?? 0}</span>
                            </div>
                            <div class="stat-pill">
                                <span class="stat-label">Freezes</span>
                                <span class="stat-value">{dashboardState.stats?.streakFreezes ?? 0}</span>
                            </div>
                            <div class="stat-pill">
                                <span class="stat-label">Active</span>
                                <span class="stat-value">{formatDate(dashboardState.stats?.lastActiveDate ?? null)}</span>
                            </div>
                        </div>
                    </div>

                    <div class="dashboard-panel panel-matrix">
                        <div class="panel-head">
                            <h2>Skill Matrix</h2>
                        </div>

                        <div class="matrix-wrapper">
                            <svg class="radar-chart" viewBox="0 0 200 200" role="img" aria-label="Skill matrix">
                                {#each radar.rings as ring}
                                    <polygon class="radar-grid" points={ring}></polygon>
                                {/each}

                                {#each radar.axes as axis}
                                    <line
                                        class="radar-axis"
                                        x1="100"
                                        y1="100"
                                        x2={axis.x}
                                        y2={axis.y}
                                    ></line>
                                {/each}

                                <polygon class="radar-area" points={radar.polygon}></polygon>

                                {#each radar.labels as label}
                                    <text
                                        class="radar-label"
                                        x={label.x}
                                        y={label.y}
                                        text-anchor={label.anchor}
                                    >
                                        {label.label}
                                    </text>
                                {/each}
                            </svg>
                        </div>
                    </div>
                </section>
            </div>
        {/if}
    </div>
</section>

<style>
    .dashboard-shell {
        position: relative;
        flex: 1;
        padding: 2rem 1.5rem 3rem;
        background: var(--color-base-100);
        overflow: hidden;
    }

    .dashboard-gridlines {
        position: absolute;
        inset: 0;
        background:
            radial-gradient(circle at top, color-mix(in oklab, var(--color-primary) 14%, transparent), transparent 65%),
            radial-gradient(circle at 15% 35%, color-mix(in oklab, var(--color-secondary) 18%, transparent), transparent 60%),
            linear-gradient(135deg,
                color-mix(in oklab, var(--color-base-200) 70%, transparent),
                color-mix(in oklab, var(--color-base-100) 80%, transparent)
            ),
            repeating-linear-gradient(0deg,
                color-mix(in oklab, var(--color-base-content) 6%, transparent),
                color-mix(in oklab, var(--color-base-content) 6%, transparent) 1px,
                transparent 1px,
                transparent 38px
            ),
            repeating-linear-gradient(90deg,
                color-mix(in oklab, var(--color-base-content) 6%, transparent),
                color-mix(in oklab, var(--color-base-content) 6%, transparent) 1px,
                transparent 1px,
                transparent 38px
            );
        opacity: 0.8;
        pointer-events: none;
    }

    .dashboard-content {
        position: relative;
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
        max-width: 1200px;
        margin: 0 auto;
    }

    .dashboard-hero {
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        align-items: flex-end;
        gap: 1rem;
    }

    .hero-kicker {
        text-transform: uppercase;
        letter-spacing: 0.3em;
        font-size: 0.7rem;
        color: color-mix(in oklab, var(--color-base-content) 60%, transparent);
        margin-bottom: 0.5rem;
    }

    .hero-title {
        font-size: clamp(1.8rem, 2.6vw, 2.6rem);
        font-weight: 700;
        letter-spacing: 0.06em;
    }

    .hero-subtitle {
        color: color-mix(in oklab, var(--color-base-content) 70%, transparent);
        max-width: 28rem;
    }

    .hero-tabs {
        display: flex;
        gap: 0.5rem;
    }

    .dashboard-loading {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
        gap: 1.5rem;
    }

    .loading-panel {
        height: 320px;
        border-radius: 1rem;
    }

    .dashboard-grid {
        display: grid;
        grid-template-columns: minmax(0, 2fr) minmax(0, 1fr);
        gap: 1.5rem;
    }

    .dashboard-panel {
        background: color-mix(in oklab, var(--color-base-200) 90%, transparent);
        border-radius: 1rem;
        padding: 1.5rem;
        box-shadow: 0 24px 60px -50px color-mix(in oklab, var(--color-base-content) 80%, transparent);
        border: 1px solid color-mix(in oklab, var(--color-base-content) 10%, transparent);
        backdrop-filter: blur(10px);
    }

    .panel-head {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }

    .panel-head h2 {
        font-size: 1.1rem;
        text-transform: uppercase;
        letter-spacing: 0.2em;
    }

    .panel-meta {
        display: flex;
        gap: 1rem;
        font-size: 0.75rem;
        text-transform: uppercase;
        color: color-mix(in oklab, var(--color-base-content) 60%, transparent);
    }

    .panel-empty {
        padding: 2rem 0;
        text-align: center;
        color: color-mix(in oklab, var(--color-base-content) 60%, transparent);
    }

    .learning-list {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }

    .learning-item {
        display: grid;
        grid-template-columns: auto 1fr auto;
        gap: 1rem;
        align-items: center;
        padding: 0.75rem 0.75rem;
        border-radius: 0.75rem;
        background: color-mix(in oklab, var(--color-base-100) 70%, transparent);
    }

    .learning-icon {
        width: 2.5rem;
        height: 2.5rem;
        border-radius: 999px;
        display: grid;
        place-items: center;
        font-weight: 700;
        color: var(--color-base-100);
        background: linear-gradient(135deg,
            color-mix(in oklab, var(--color-primary) 80%, transparent),
            color-mix(in oklab, var(--color-secondary) 70%, transparent)
        );
    }

    .learning-details {
        display: flex;
        flex-direction: column;
        gap: 0.35rem;
    }

    .learning-title {
        display: flex;
        justify-content: space-between;
        font-size: 0.95rem;
    }

    .dashboard-side {
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
    }

    .stats-user {
        display: flex;
        gap: 1rem;
        align-items: center;
    }

    .avatar {
        width: 3rem;
        height: 3rem;
        border-radius: 999px;
        overflow: hidden;
        background: color-mix(in oklab, var(--color-base-200) 70%, transparent);
        display: grid;
        place-items: center;
    }

    .avatar img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    .avatar-fallback {
        text-transform: uppercase;
        letter-spacing: 0.2em;
        font-size: 0.75rem;
    }

    .stats-name {
        font-weight: 600;
    }

    .stats-level {
        font-size: 0.8rem;
        color: color-mix(in oklab, var(--color-base-content) 60%, transparent);
    }

    .stats-progress {
        margin-top: 1.25rem;
    }

    .stats-progress-row {
        display: flex;
        justify-content: space-between;
        font-size: 0.8rem;
        margin-bottom: 0.35rem;
    }

    .stats-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 0.75rem;
        margin-top: 1.25rem;
    }

    .stat-pill {
        display: flex;
        flex-direction: column;
        gap: 0.35rem;
        padding: 0.75rem;
        border-radius: 0.75rem;
        background: color-mix(in oklab, var(--color-base-100) 70%, transparent);
    }

    .stat-label {
        font-size: 0.65rem;
        text-transform: uppercase;
        letter-spacing: 0.2em;
        color: color-mix(in oklab, var(--color-base-content) 60%, transparent);
    }

    .stat-value {
        font-size: 1.05rem;
        font-weight: 600;
    }

    .matrix-wrapper {
        display: grid;
        place-items: center;
    }

    .radar-chart {
        width: 100%;
        max-width: 260px;
        height: auto;
    }

    .radar-grid {
        fill: none;
        stroke: color-mix(in oklab, var(--color-base-content) 12%, transparent);
        stroke-width: 1;
    }

    .radar-axis {
        stroke: color-mix(in oklab, var(--color-base-content) 18%, transparent);
        stroke-width: 1;
    }

    .radar-area {
        fill: color-mix(in oklab, var(--color-primary) 45%, transparent);
        stroke: var(--color-primary);
        stroke-width: 1.5;
    }

    .radar-label {
        font-size: 0.5rem;
        text-transform: uppercase;
        fill: color-mix(in oklab, var(--color-base-content) 70%, transparent);
        letter-spacing: 0.12em;
    }

    @media (max-width: 960px) {
        .dashboard-grid {
            grid-template-columns: 1fr;
        }
    }

    @media (max-width: 640px) {
        .dashboard-shell {
            padding: 1.5rem 1rem 2rem;
        }

        .panel-meta {
            display: none;
        }

        .learning-title {
            flex-direction: column;
            align-items: flex-start;
            gap: 0.25rem;
        }
    }
</style>
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
Gamification dashboard with learning progress, stats, and skill matrix.
-->
<script lang="ts">
    import {onMount} from "svelte";
    import {push} from "svelte-spa-router";
    import {
        gamificationDashboardStore,
        type GamificationDashboardState,
    } from "../../../stores/gamification-dashboard.store.js";
    import type {DashboardCourse, DashboardSkill} from "../../../data/gamification-dashboard.js";

    type SkillMatrix = {
        labels: string[];
        values: number[];
    };

    const radarCenter = 100;
    const radarRadius = 70;
    const radarLabelRadius = 92;

    const store = gamificationDashboardStore;

    let activeTab = $state("Current");

    onMount(() => {
        store.refresh();
    });

    const dashboardState = $derived($store as GamificationDashboardState);

    const displayHandle = $derived(() => {
        const username = dashboardState.user?.username ?? "user";
        return `@${username}`;
    });

    const overallProgress = $derived(() => {
        if (dashboardState.courses.length === 0) {
            return 0;
        }

        const total = dashboardState.courses.reduce((sum, course) => sum + course.progress, 0);
        return Math.round(total / dashboardState.courses.length);
    });

    const displayedCourses = $derived(() => dashboardState.courses.slice(0, 6));

    const displayedSkills = $derived(() => dashboardState.skills.slice(0, 6));

    const skillMatrix = $derived(() => buildSkillMatrix(displayedSkills));

    const isEmpty = $derived(() => dashboardState.courses.length === 0 && dashboardState.skills.length === 0);

    function formatNumber(value: number): string {
        return new Intl.NumberFormat().format(value);
    }

    function formatDate(value: Date | null): string {
        if (!value) {
            return "-";
        }

        return value.toLocaleDateString();
    }

    function courseInitials(name: string): string {
        const parts = name.split(" ").filter(Boolean);
        const initials = parts.slice(0, 2).map((part) => part[0].toUpperCase());
        return initials.join("") || "--";
    }

    function buildSkillMatrix(skills: DashboardSkill[]): SkillMatrix | null {
        if (skills.length < 3) {
            return null;
        }

        const sorted = [...skills].sort((a, b) => b.progress - a.progress).slice(0, 5);
        return {
            labels: sorted.map((skill) => skill.name),
            values: sorted.map((skill) => skill.progress),
        };
    }

    function radarPoints(values: number[]): string {
        const count = values.length;
        return values
            .map((value, index) => {
                const angle = (Math.PI * 2 * index) / count - Math.PI / 2;
                const radius = (value / 100) * radarRadius;
                const x = radarCenter + Math.cos(angle) * radius;
                const y = radarCenter + Math.sin(angle) * radius;
                return `${x.toFixed(2)},${y.toFixed(2)}`;
            })
            .join(" ");
    }

    function radarRingPoints(count: number, ring: number): string {
        const radius = (radarRadius / 5) * ring;
        return Array.from({length: count}).map((_, index) => {
            const angle = (Math.PI * 2 * index) / count - Math.PI / 2;
            const x = radarCenter + Math.cos(angle) * radius;
            const y = radarCenter + Math.sin(angle) * radius;
            return `${x.toFixed(2)},${y.toFixed(2)}`;
        }).join(" ");
    }

    function radarAxis(count: number, index: number): {x: number; y: number} {
        const angle = (Math.PI * 2 * index) / count - Math.PI / 2;
        return {
            x: radarCenter + Math.cos(angle) * radarRadius,
            y: radarCenter + Math.sin(angle) * radarRadius,
        };
    }

    function radarLabel(count: number, index: number): {x: number; y: number} {
        const angle = (Math.PI * 2 * index) / count - Math.PI / 2;
        return {
            x: radarCenter + Math.cos(angle) * radarLabelRadius,
            y: radarCenter + Math.sin(angle) * radarLabelRadius,
        };
    }

    function goToProfile(): void {
        push("/profile");
    }

    function openCourse(course: DashboardCourse): void {
        push(`/courses/${course.id}`);
    }

    function setTab(tab: string): void {
        activeTab = tab;
    }
</script>

<section class="dashboard-shell">
    <div class="dashboard-glow" aria-hidden="true"></div>
    <div class="dashboard-grid" aria-hidden="true"></div>

    <div class="dashboard-content">
        <div class="dashboard-header">
            <div>
                <p class="dashboard-kicker">Welcome back</p>
                <h1 class="dashboard-title">{displayHandle} Dashboard</h1>
            </div>
            <div class="dashboard-actions">
                <button class="btn btn-outline btn-sm" type="button" onclick={() => store.refresh()}>
                    Refresh
                </button>
                <button class="btn btn-primary btn-sm" type="button" onclick={goToProfile}>
                    Go to Profile
                </button>
            </div>
        </div>

        <div class="dashboard-tabs">
            {#each ["Current", "Path", "Repeat"] as tab}
                <button
                    class={`btn btn-xs ${activeTab === tab ? "btn-primary" : "btn-ghost"}`}
                    type="button"
                    onclick={() => setTab(tab)}
                >
                    {tab}
                </button>
            {/each}
        </div>

        {#if dashboardState.isLoading}
            <div class="dashboard-state card bg-base-200">
                <div class="card-body">
                    <p>Loading your gamification dashboard...</p>
                </div>
            </div>
        {:else if dashboardState.errorMessage}
            <div class="dashboard-state card bg-base-200">
                <div class="card-body">
                    <p class="text-error">{dashboardState.errorMessage}</p>
                </div>
            </div>
        {:else if isEmpty}
            <div class="dashboard-state card bg-base-200">
                <div class="card-body">
                    <p>No learning progress available yet. Start a course to see your dashboard fill up.</p>
                </div>
            </div>
        {:else}
            <div class="dashboard-layout">
                <div class="dashboard-main">
                    <article class="card bg-base-200 shadow-xl">
                        <div class="card-body">
                            <div class="learning-header">
                                <h2 class="card-title text-xl">My Learning</h2>
                                <div class="learning-progress">
                                    <span>Overall</span>
                                    <progress class="progress progress-primary" value={overallProgress} max="100"></progress>
                                    <span>{overallProgress}%</span>
                                </div>
                            </div>

                            <div class="learning-list">
                                {#each displayedCourses as course (course.id)}
                                    <button class="learning-item" type="button" onclick={() => openCourse(course)}>
                                        <div class="learning-icon">
                                            <span>{courseInitials(course.name)}</span>
                                        </div>
                                        <div class="learning-info">
                                            <h3>{course.name}</h3>
                                            <p>Level {course.level} | {formatNumber(course.points)} points</p>
                                            <progress class="progress progress-accent" value={course.progress} max="100"></progress>
                                        </div>
                                        <div class="learning-meta">
                                            <span>{course.progress}%</span>
                                        </div>
                                    </button>
                                {/each}
                            </div>
                        </div>
                    </article>
                </div>

                <div class="dashboard-side">
                    <article class="card bg-base-200 shadow-xl">
                        <div class="card-body">
                            <div class="stats-header">
                                <div>
                                    <h2 class="card-title text-xl">Your Stats</h2>
                                    <p class="text-sm opacity-75">{dashboardState.user?.fullName ?? displayHandle}</p>
                                </div>
                                <div class="stats-avatar"></div>
                            </div>
                            <div class="stats-level">
                                <div>
                                    <p class="text-xs uppercase opacity-60">Level</p>
                                    <h3>{dashboardState.stats?.level ?? 1}</h3>
                                </div>
                                <div>
                                    <p class="text-xs uppercase opacity-60">Points</p>
                                    <h3>{formatNumber(dashboardState.stats?.points ?? 0)}</h3>
                                </div>
                            </div>
                            <div class="stats-grid">
                                <div class="stat-item">
                                    <p class="stat-label">Current streak</p>
                                    <p class="stat-value">{dashboardState.stats?.currentStreak ?? 0}</p>
                                </div>
                                <div class="stat-item">
                                    <p class="stat-label">Longest streak</p>
                                    <p class="stat-value">{dashboardState.stats?.longestStreak ?? 0}</p>
                                </div>
                                <div class="stat-item">
                                    <p class="stat-label">Streak freezes</p>
                                    <p class="stat-value">{dashboardState.stats?.streakFreezes ?? 0}</p>
                                </div>
                                <div class="stat-item">
                                    <p class="stat-label">Last active</p>
                                    <p class="stat-value">{formatDate(dashboardState.stats?.lastActiveDate ?? null)}</p>
                                </div>
                            </div>
                        </div>
                    </article>

                    <article class="card bg-base-200 shadow-xl">
                        <div class="card-body">
                            <div class="flex items-center justify-between">
                                <h2 class="card-title text-xl">Skill Matrix</h2>
                                <span class="badge badge-outline">Top skills</span>
                            </div>

                            {#if skillMatrix}
                                <div class="skill-matrix">
                                    <svg viewBox="0 0 200 200" role="img" aria-label="Skill matrix">
                                        {#each [1, 2, 3, 4, 5] as ring}
                                            <polygon points={radarRingPoints(skillMatrix.labels.length, ring)} class="radar-grid"></polygon>
                                        {/each}

                                        {#each skillMatrix.labels as label, index}
                                            {@const axis = radarAxis(skillMatrix.labels.length, index)}
                                            <line x1={radarCenter} y1={radarCenter} x2={axis.x} y2={axis.y} class="radar-axis"></line>
                                        {/each}

                                        <polygon points={radarPoints(skillMatrix.values)} class="radar-area"></polygon>

                                        {#each skillMatrix.labels as label, index}
                                            {@const pos = radarLabel(skillMatrix.labels.length, index)}
                                            <text x={pos.x} y={pos.y} class="radar-label">{label}</text>
                                        {/each}
                                    </svg>
                                </div>
                            {:else}
                                <p class="text-sm opacity-70">Add at least three skills to unlock the matrix.</p>
                            {/if}
                        </div>
                    </article>
                </div>
            </div>
        {/if}
    </div>
</section>

<style>
    @import url("https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;700&family=Space+Mono:wght@400;700&display=swap");

    .dashboard-shell {
        position: relative;
        flex: 1;
        padding: 2.5rem 1.5rem 3rem;
        background: radial-gradient(circle at top,
            color-mix(in oklab, var(--color-base-200) 75%, transparent),
            color-mix(in oklab, var(--color-base-100) 85%, transparent)
        );
        overflow: hidden;
        font-family: "Rajdhani", "normaltext";
    }

    .dashboard-glow {
        position: absolute;
        inset: 0;
        background: radial-gradient(circle at 20% 20%,
            color-mix(in oklab, var(--color-primary) 35%, transparent),
            transparent 55%
        );
        opacity: 0.4;
        pointer-events: none;
    }

    .dashboard-grid {
        position: absolute;
        inset: 0;
        background-image:
            linear-gradient(0deg, color-mix(in oklab, var(--color-base-content) 8%, transparent) 1px, transparent 1px),
            linear-gradient(90deg, color-mix(in oklab, var(--color-base-content) 8%, transparent) 1px, transparent 1px);
        background-size: 48px 48px;
        opacity: 0.25;
        pointer-events: none;
    }

    .dashboard-content {
        position: relative;
        z-index: 1;
        max-width: 1200px;
        margin: 0 auto;
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
    }

    .dashboard-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 1rem;
    }

    .dashboard-kicker {
        text-transform: uppercase;
        letter-spacing: 0.2em;
        font-size: 0.7rem;
        opacity: 0.7;
    }

    .dashboard-title {
        font-family: "Space Mono", "normaltext";
        font-size: clamp(1.8rem, 3vw, 2.6rem);
        margin: 0.25rem 0 0;
    }

    .dashboard-actions {
        display: flex;
        gap: 0.75rem;
        align-items: center;
    }

    .dashboard-tabs {
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
    }

    .dashboard-state {
        max-width: 520px;
    }

    .dashboard-layout {
        display: grid;
        grid-template-columns: minmax(0, 2fr) minmax(0, 1fr);
        gap: 1.5rem;
    }

    .dashboard-main {
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
    }

    .dashboard-side {
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
    }

    .learning-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 1rem;
    }

    .learning-progress {
        display: grid;
        grid-template-columns: auto minmax(120px, 1fr) auto;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.9rem;
    }

    .learning-list {
        margin-top: 1rem;
        display: grid;
        gap: 0.75rem;
    }

    .learning-item {
        display: grid;
        grid-template-columns: auto 1fr auto;
        gap: 1rem;
        padding: 0.75rem;
        border-radius: 1rem;
        background: color-mix(in oklab, var(--color-base-100) 75%, transparent);
        border: 1px solid color-mix(in oklab, var(--color-base-content) 10%, transparent);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        text-align: left;
    }

    .learning-item:hover,
    .learning-item:focus-visible {
        transform: translateY(-2px);
        box-shadow: 0 12px 30px color-mix(in oklab, var(--color-base-content) 20%, transparent);
        outline: none;
    }

    .learning-icon {
        width: 44px;
        height: 44px;
        border-radius: 14px;
        display: grid;
        place-items: center;
        font-weight: 700;
        background: color-mix(in oklab, var(--color-primary) 30%, transparent);
        color: var(--color-primary-content);
    }

    .learning-info h3 {
        margin: 0;
        font-size: 1rem;
    }

    .learning-info p {
        margin: 0.15rem 0 0.5rem;
        font-size: 0.85rem;
        opacity: 0.7;
    }

    .learning-meta {
        display: flex;
        align-items: center;
        font-size: 0.9rem;
    }

    .stats-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
    }

    .stats-avatar {
        width: 48px;
        height: 48px;
        border-radius: 16px;
        background: color-mix(in oklab, var(--color-secondary) 35%, transparent);
        border: 1px solid color-mix(in oklab, var(--color-base-content) 12%, transparent);
    }

    .stats-level {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 1rem;
        margin-top: 1rem;
    }

    .stats-level h3 {
        margin: 0;
        font-size: 1.6rem;
        font-family: "Space Mono", "normaltext";
    }

    .stats-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 0.75rem;
        margin-top: 1.5rem;
    }

    .stat-item {
        padding: 0.75rem;
        border-radius: 0.75rem;
        background: color-mix(in oklab, var(--color-base-100) 70%, transparent);
        border: 1px solid color-mix(in oklab, var(--color-base-content) 10%, transparent);
    }

    .stat-label {
        margin: 0;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        opacity: 0.6;
    }

    .stat-value {
        margin: 0.35rem 0 0;
        font-family: "Space Mono", "normaltext";
        font-size: 1.1rem;
    }

    .skill-matrix {
        margin-top: 1rem;
        display: flex;
        justify-content: center;
    }

    .radar-grid {
        fill: none;
        stroke: color-mix(in oklab, var(--color-base-content) 25%, transparent);
        stroke-width: 1;
    }

    .radar-axis {
        stroke: color-mix(in oklab, var(--color-base-content) 25%, transparent);
        stroke-width: 1;
    }

    .radar-area {
        fill: color-mix(in oklab, var(--color-primary) 45%, transparent);
        stroke: var(--color-primary);
        stroke-width: 2;
    }

    .radar-label {
        fill: color-mix(in oklab, var(--color-base-content) 75%, transparent);
        font-size: 0.65rem;
        text-anchor: middle;
        dominant-baseline: middle;
    }

    @media (max-width: 960px) {
        .dashboard-layout {
            grid-template-columns: 1fr;
        }
    }

    @media (max-width: 640px) {
        .learning-item {
            grid-template-columns: 1fr;
        }

        .learning-meta {
            justify-content: flex-end;
        }
    }
</style>
