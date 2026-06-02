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
Root of the gamification dashboard microfrontend. Orchestrates data loading and
renders the loading / error / content states across the three panels.
-->
<script lang="ts">
    import {onMount} from "svelte";
    import {dashboardStore} from "../stores/dashboard.store.js";
    import type {DashboardState} from "../stores/dashboard.store.js";
    import DashboardHeader from "./app-frame/DashboardHeader.svelte";
    import MyLearningPanel from "./panels/MyLearningPanel.svelte";
    import StatsPanel from "./panels/StatsPanel.svelte";
    import SkillMatrixPanel from "./panels/SkillMatrixPanel.svelte";

    // Mirror the store into local reactive state via an explicit subscription.
    let state = $state<DashboardState>({
        isLoading: true,
        errorMessage: "",
        user: null,
        stats: null,
        skills: [],
        courses: [],
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

<DashboardHeader user={state.user} />

<div class="dashboard">
    <header class="top">
        <h1 class="title">{handle} Dashboard</h1>
    </header>

    {#if state.isLoading}
        <div class="status" role="status" aria-live="polite">
            <span class="loading loading-spinner loading-lg"></span>
            <p>Loading your dashboard…</p>
        </div>
    {:else if state.errorMessage}
        <div class="status" role="alert">
            <p class="error">{state.errorMessage}</p>
            <button type="button" class="btn btn-primary btn-sm" onclick={() => dashboardStore.refresh()}>
                Retry
            </button>
        </div>
    {:else}
        <div class="grid">
            <div class="grid-main">
                <MyLearningPanel courses={state.courses} skills={state.skills} />
            </div>
            <div class="grid-side">
                <StatsPanel user={state.user} stats={state.stats} />
                <SkillMatrixPanel skills={state.skills} />
            </div>
        </div>
    {/if}

    <footer class="bottom">
        <span>Copyright 2026 | OpenBook</span>
    </footer>
</div>

<style>
    /* Fill ~90% of the viewport with little margin around the edges. */
    .dashboard {
        flex: 1;
        min-height: 0;
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

    .grid-side {
        display: flex;
        flex-direction: column;
        gap: 1.25rem;
        min-height: 0;
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

    .bottom {
        margin-top: auto;
        text-align: center;
        font-size: 0.75rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: color-mix(in oklab, var(--color-base-content) 60%, transparent);
    }

    @media (max-width: 60rem) {
        .grid {
            grid-template-columns: 1fr;
        }
    }
</style>
