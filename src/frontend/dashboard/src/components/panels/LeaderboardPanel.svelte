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
"Leaderboard" panel: the global top-ranked learners by points. The top three
ranks get a medal, everyone else their rank number, and the current user's row
is highlighted.
-->
<script lang="ts">
    import type {DashboardLeaderboardEntry} from "../../data/dashboard.js";

    let {entries}: {entries: DashboardLeaderboardEntry[]} = $props();

    const numberFormat = new Intl.NumberFormat();
    const medals: Record<number, string> = {1: "🥇", 2: "🥈", 3: "🥉"};

    const isEmpty = $derived(entries.length === 0);

    function format(value: number): string {
        return numberFormat.format(value);
    }
</script>

<section class="card panel">
    <h2 class="panel-title">Leaderboard</h2>

    <div class="panel-body">
        {#if isEmpty}
            <p class="empty">No ranking yet. Earn points in your courses to climb the leaderboard.</p>
        {:else}
            {#each entries as entry (entry.username)}
                <div class="row" class:me={entry.isCurrentUser}>
                    <span class="rank" class:medal={entry.rank <= 3}>
                        {medals[entry.rank] ?? entry.rank}
                    </span>
                    <span class="name">
                        {entry.fullName}{#if entry.isCurrentUser}<span class="you">you</span>{/if}
                    </span>
                    <span class="level">Lv {entry.level}</span>
                    <span class="points">{format(entry.points)}</span>
                </div>
            {/each}
        {/if}
    </div>
</section>

<style>
    .panel {
        background: var(--color-base-100);
        border-radius: 1rem;
        padding: 1.5rem;
        box-shadow: 0 0 24px color-mix(in oklab, var(--color-primary) 10%, transparent);
    }

    .panel-title {
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 1rem;
        color: var(--color-base-content);
    }

    .panel-body {
        display: flex;
        flex-direction: column;
        gap: 0.4rem;
    }

    .row {
        display: grid;
        grid-template-columns: 2rem 1fr auto auto;
        align-items: center;
        gap: 0.75rem;
        padding: 0.55rem 0.75rem;
        border-radius: 0.75rem;
        border: 1px solid transparent;
    }

    /* Highlight the current user's row, mirroring the screenshot. */
    .row.me {
        background: color-mix(in oklab, var(--color-primary) 16%, transparent);
        border-color: color-mix(in oklab, var(--color-primary) 45%, transparent);
    }

    .rank {
        font-size: 0.95rem;
        font-weight: 700;
        text-align: center;
        color: color-mix(in oklab, var(--color-base-content) 65%, transparent);
    }

    .rank.medal {
        font-size: 1.2rem;
    }

    .name {
        font-weight: 600;
        color: var(--color-base-content);
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .you {
        margin-left: 0.35rem;
        font-size: 0.8rem;
        font-weight: 600;
        color: var(--color-primary);
    }

    .level {
        font-size: 0.75rem;
        white-space: nowrap;
        color: color-mix(in oklab, var(--color-base-content) 60%, transparent);
    }

    .points {
        font-weight: 700;
        text-align: right;
        color: var(--color-primary);
    }

    .empty {
        color: color-mix(in oklab, var(--color-base-content) 60%, transparent);
        padding: 1rem 0;
    }
</style>
