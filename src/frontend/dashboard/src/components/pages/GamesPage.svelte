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
Games hub for a course: a chooser shown when the learner opens "Games". Each game
is a card; Memory is playable today, more can be added here later.
-->
<script lang="ts">
    import {onMount} from "svelte";
    import {push} from "svelte-spa-router";
    import {dashboardStore} from "../../stores/dashboard.store.js";
    import type {DashboardState} from "../../stores/dashboard.store.js";

    let {params}: {params?: {id?: string}} = $props();

    let state = $state<DashboardState>({
        isLoading: true,
        errorMessage: "",
        user: null,
        stats: null,
        skills: [],
        courses: [],
    });

    onMount(() => {
        const unsubscribe = dashboardStore.subscribe((value) => (state = value));
        if (state.courses.length === 0) {
            dashboardStore.refresh();
        }
        return unsubscribe;
    });

    const courseTitle = $derived(
        state.courses.find((course) => course.id === params?.id)?.name ?? "Course",
    );
    const courseId = $derived(params?.id ?? "");

    interface Game {
        icon: string;
        name: string;
        description: string;
        to?: string;
    }

    const games = $derived<Game[]>([
        {
            icon: "🃏",
            name: "Memory",
            description: "Match pairs of terms from your course.",
            to: `/games/${courseId}/memory`,
        },
        {
            icon: "🔤",
            name: "Flashcards",
            description: "Flip through your course's key concepts.",
            to: `/games/${courseId}/flashcards`,
        },
        {
            icon: "🪢",
            name: "Hangman",
            description: "Guess subject terms letter by letter.",
            to: `/games/${courseId}/hangman`,
        },
    ]);
</script>

<div class="games-screen">
    <header class="games-head">
        <button type="button" class="back" onclick={() => push(`/chat/${courseId}`)}>← Back to chat</button>
        <h1 class="title">Games</h1>
        <p class="subtitle">{courseTitle}</p>
    </header>

    <p class="lead">Choose a game to play.</p>

    <div class="game-grid">
        {#each games as game (game.name)}
            <button
                type="button"
                class="game-card"
                disabled={!game.to}
                onclick={() => game.to && push(game.to)}
            >
                <span class="game-icon" aria-hidden="true">{game.icon}</span>
                <span class="game-name">
                    {game.name}
                    {#if !game.to}<span class="soon">soon</span>{/if}
                </span>
                <span class="game-desc">{game.description}</span>
            </button>
        {/each}
    </div>
</div>

<style>
    .games-screen {
        flex: 1;
        min-height: 0;
        overflow-y: auto;
        width: 90%;
        max-width: 56rem;
        margin: 0 auto;
        padding: 1.5rem 0 2.5rem;
        display: flex;
        flex-direction: column;
        gap: 1.25rem;
    }

    .games-head {
        text-align: center;
        position: relative;
    }

    .back {
        position: absolute;
        left: 0;
        top: 0.25rem;
        background: none;
        border: none;
        cursor: pointer;
        font-weight: 600;
        color: var(--color-primary);
    }

    .back:focus-visible {
        outline: 2px solid var(--color-primary);
        outline-offset: 2px;
    }

    .title {
        font-size: clamp(1.8rem, 4vw, 2.6rem);
        font-weight: 800;
        color: var(--color-base-content);
        text-shadow: 0 0 22px color-mix(in oklab, var(--color-primary) 35%, transparent);
    }

    .subtitle {
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: var(--color-primary);
    }

    .lead {
        text-align: center;
        color: color-mix(in oklab, var(--color-base-content) 70%, transparent);
    }

    .game-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(13rem, 1fr));
        grid-auto-rows: 1fr;
        gap: 1.1rem;
    }

    .game-card {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        gap: 0.5rem;
        height: 100%;
        padding: 1.25rem;
        border-radius: 1rem;
        cursor: pointer;
        text-align: left;
        color: var(--color-base-content);
        background: color-mix(in oklab, var(--color-base-100) 82%, transparent);
        border: 1px solid color-mix(in oklab, var(--color-base-content) 12%, transparent);
        transition: transform 0.12s ease, border-color 0.2s ease, box-shadow 0.2s ease, background 0.2s ease;
        box-shadow: 0 4px 14px color-mix(in oklab, var(--color-base-content) 10%, transparent);
    }

    .game-card:not(:disabled):hover {
        transform: translateY(-3px);
        background: color-mix(in oklab, var(--color-primary) 8%, transparent);
        border-color: color-mix(in oklab, var(--color-primary) 55%, transparent);
        box-shadow: 0 10px 24px color-mix(in oklab, var(--color-primary) 22%, transparent);
    }

    .game-card:focus-visible {
        outline: 3px solid var(--color-primary);
        outline-offset: 3px;
    }

    .game-card:disabled {
        cursor: not-allowed;
        opacity: 0.55;
    }

    .game-icon {
        display: grid;
        place-items: center;
        width: 2.8rem;
        height: 2.8rem;
        border-radius: 0.8rem;
        font-size: 1.5rem;
        background: color-mix(in oklab, var(--color-primary) 16%, transparent);
        border: 1px solid color-mix(in oklab, var(--color-primary) 28%, transparent);
    }

    .game-name {
        display: flex;
        align-items: center;
        gap: 0.4rem;
        font-size: 1.1rem;
        font-weight: 700;
    }

    .soon {
        font-size: 0.6rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        padding: 0.05rem 0.4rem;
        border-radius: 999px;
        color: var(--color-warning);
        background: color-mix(in oklab, var(--color-warning) 16%, transparent);
    }

    .game-desc {
        font-size: 0.85rem;
        color: color-mix(in oklab, var(--color-base-content) 65%, transparent);
    }
</style>
