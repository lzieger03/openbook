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
"Your Stats" panel: avatar, username, level/points progress and four stat tiles
(current streak, longest streak, total points, level).
-->
<script lang="ts">
    import ProgressBar from "../basic/ProgressBar.svelte";
    import StatTile from "../basic/StatTile.svelte";
    import type {DashboardStats, DashboardUser} from "../../data/dashboard.js";

    let {
        user,
        stats,
        onProfile,
    }: {
        user: DashboardUser | null;
        stats: DashboardStats | null;
        onProfile?: () => void;
    } = $props();

    const numberFormat = new Intl.NumberFormat();

    const username = $derived(user?.username ?? "user");
    const points = $derived(stats?.points ?? 0);
    const level = $derived(stats?.level ?? 1);

    // No explicit "points needed for next level" is exposed; show progress toward
    // the next 1000-point milestone as a reasonable visual approximation.
    const pointsMax = $derived(points <= 0 ? 1000 : Math.ceil((points + 1) / 1000) * 1000);
    const levelProgress = $derived((points / pointsMax) * 100);

    function format(value: number): string {
        return numberFormat.format(value);
    }
</script>

<section class="card panel">
    <header class="panel-head">
        <h2 class="panel-title">Your Stats</h2>
        <button type="button" class="btn btn-outline btn-sm" onclick={() => onProfile?.()}>Go to Profile</button>
    </header>

    <div class="identity">
        <span class="avatar-mark" aria-hidden="true">
            {#if user?.avatarUrl}
                <img src={user.avatarUrl} alt="" />
            {/if}
        </span>
        <div class="identity-text">
            <span class="username">{username}</span>
            <div class="level-row">
                <span class="level-label">Level {level}</span>
                <div class="level-bar">
                    <ProgressBar value={levelProgress} label={`Level ${level} progress`} />
                </div>
                <span class="level-points">{format(points)}</span>
            </div>
        </div>
    </div>

    <div class="stat-grid">
        <StatTile icon="🔥" value={format(stats?.currentStreak ?? 0)} label="Current streak" />
        <StatTile icon="🏆" value={format(stats?.longestStreak ?? 0)} label="Longest streak" />
        <StatTile icon="🎯" value={format(points)} label="Total points" />
        <StatTile icon="🏅" value={format(level)} label="Level" />
    </div>
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

    .identity {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }

    .avatar-mark {
        width: 3.5rem;
        height: 3.5rem;
        flex: 0 0 auto;
        border-radius: 999px;
        overflow: hidden;
        background: color-mix(in oklab, var(--color-base-content) 18%, transparent);
        box-shadow: 0 0 16px color-mix(in oklab, var(--color-primary) 35%, transparent);
    }

    .avatar-mark img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    .identity-text {
        flex: 1 1 auto;
        min-width: 0;
    }

    .username {
        display: block;
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--color-base-content);
    }

    .level-row {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        margin-top: 0.35rem;
    }

    .level-label {
        font-size: 0.8rem;
        white-space: nowrap;
        color: color-mix(in oklab, var(--color-base-content) 70%, transparent);
    }

    .level-bar {
        flex: 1 1 auto;
    }

    .level-points {
        font-weight: 700;
        color: var(--color-base-content);
    }

    .stat-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 0.75rem;
    }
</style>
