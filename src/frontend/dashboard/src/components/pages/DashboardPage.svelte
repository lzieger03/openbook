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
Gamification dashboard page: loads progress data and renders the three panels
with loading / error / content states.
-->
<script lang="ts">
    import {onMount} from "svelte";
    import {push} from "svelte-spa-router";
    import {dashboardStore} from "../../stores/dashboard.store.js";
    import type {DashboardState} from "../../stores/dashboard.store.js";
    import MyLearningPanel from "../panels/MyLearningPanel.svelte";
    import StatsPanel from "../panels/StatsPanel.svelte";
    import LeaderboardPanel from "../panels/LeaderboardPanel.svelte";
    import SkillMatrixPanel from "../panels/SkillMatrixPanel.svelte";

    let state = $state<DashboardState>({
        isLoading: true,
        errorMessage: "",
        user: null,
        stats: null,
        skills: [],
        courses: [],
        leaderboard: [],
    });

    onMount(() => {
        const unsubscribe = dashboardStore.subscribe((value) => {
            state = value;
        });

        dashboardStore.refresh();

        return unsubscribe;
    });

    const handle = $derived(state.user?.username ? `@${state.user.username}` : "@user");
</script>

<div class="dashboard">
    <header class="top">
        <h1 class="title">{handle} Dashboard</h1>
    </header>

    {#if state.isLoading}
        <div class="status-box" role="status" aria-live="polite">
            <span class="loading loading-spinner loading-lg"></span>
            <p>Loading your dashboard…</p>
        </div>
    {:else if state.errorMessage}
        <div class="status-box" role="alert">
            <p class="error">{state.errorMessage}</p>
            <button type="button" class="btn btn-primary btn-sm" onclick={() => dashboardStore.refresh()}>
                Retry
            </button>
        </div>
    {:else}
        <div class="grid">
            <div class="grid-main">
                <MyLearningPanel
                    courses={state.courses}
                    skills={state.skills}
                    stats={state.stats}
                    onCourseOpen={(course) => push(`/chat/${course.id}`)}
                />
            </div>
            <div class="grid-side">
                <StatsPanel user={state.user} stats={state.stats} onProfile={() => push("/profile")} />
                <LeaderboardPanel entries={state.leaderboard} />
                <SkillMatrixPanel skills={state.skills} />
            </div>
        </div>
    {/if}
</div>

<style>
    /* Fill ~90% of the viewport with little margin around the edges. */
    .dashboard {
        flex: 1;
        min-height: 0;
        overflow-y: auto;
        display: flex;
        flex-direction: column;
        gap: 1.25rem;
        width: 90%;
        max-width: 110rem;
        margin: 0 auto;
        padding: 1.25rem 0 0.5rem;
    }

    .top {
        flex: 0 0 auto;
        text-align: center;
    }

    .title {
        font-size: clamp(1.6rem, 3.5vw, 2.6rem);
        font-weight: 800;
        letter-spacing: 0.04em;
        color: var(--color-base-content);
        text-shadow: 0 0 24px color-mix(in oklab, var(--color-primary) 45%, transparent);
    }

    /* Stretch so both columns share the available height. */
    .grid {
        flex: 1;
        min-height: 0;
        display: grid;
        grid-template-columns: 2fr 1fr;
        gap: 1.25rem;
        align-items: stretch;
    }

    .grid-main {
        display: flex;
        min-height: 0;
    }

    /* The side column scrolls as one unit; its panels keep their natural height
       (no per-panel scroll) so My Stats, Leaderboard and Skills move together. */
    .grid-side {
        display: flex;
        flex-direction: column;
        gap: 1.25rem;
        min-height: 0;
        overflow-y: auto;
        padding-right: 0.5rem;
        /* Firefox: keep the track transparent so the bar only shows on hover. */
        scrollbar-width: thin;
        scrollbar-color: transparent transparent;
    }

    .grid-side:hover {
        scrollbar-color: color-mix(in oklab, var(--color-base-content) 20%, transparent) transparent;
    }

    .grid-side > :global(.card) {
        flex: 0 0 auto;
    }

    .grid-side::-webkit-scrollbar {
        width: 0.5rem;
    }

    .grid-side::-webkit-scrollbar-thumb {
        border-radius: 999px;
        background: transparent;
    }

    .grid-side:hover::-webkit-scrollbar-thumb {
        background: color-mix(in oklab, var(--color-base-content) 20%, transparent);
    }

    .status-box {
        flex: 1;
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

    @media (max-width: 60rem) {
        .grid {
            grid-template-columns: 1fr;
        }
    }
</style>
