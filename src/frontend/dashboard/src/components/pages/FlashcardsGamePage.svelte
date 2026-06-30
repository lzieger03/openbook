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
Flashcards built from the course's real content: each card is a section of a textbook
page — the heading on the front, the section text on the back. Flip to check yourself,
navigate with the controls (or arrow keys / space).
-->
<script lang="ts">
    import {onDestroy, onMount} from "svelte";
    import {push} from "svelte-spa-router";
    import {dashboardStore} from "../../stores/dashboard.store.js";
    import type {DashboardState} from "../../stores/dashboard.store.js";
    import {loadCourseFlashcards} from "../../data/course-terms.js";
    import type {Flashcard} from "../../data/course-terms.js";
    import {clearPageContext, setCourseContext} from "../../stores/page-context.store.js";
    import type {PageContext} from "../../stores/page-context.store.js";

    let {params}: {params?: {id?: string}} = $props();

    let state = $state<DashboardState>({
        isLoading: true,
        errorMessage: "",
        user: null,
        stats: null,
        skills: [],
        courses: [],
    });

    let cards = $state<Flashcard[]>([]);
    let loading = $state(true);
    let index = $state(0);
    let flippedCard = $state(false);

    const courseTitle = $derived(
        state.courses.find((course) => course.id === params?.id)?.name ?? "Course",
    );
    const current = $derived(cards[index] ?? null);

    // Give the global Quick Chat the current-page context (flashcards in this course).
    let contextToken: PageContext | null = null;
    $effect(() => {
        contextToken = setCourseContext("reviewing flashcards", state.courses.find((course) => course.id === params?.id));
    });
    onDestroy(() => clearPageContext(contextToken));

    onMount(() => {
        const unsubscribe = dashboardStore.subscribe((value) => (state = value));
        if (state.courses.length === 0) {
            dashboardStore.refresh();
        }
        void load();
        window.addEventListener("keydown", onKey);
        return () => {
            unsubscribe();
            window.removeEventListener("keydown", onKey);
        };
    });

    async function load(): Promise<void> {
        const courseId = params?.id;
        loading = true;
        try {
            cards = courseId ? await loadCourseFlashcards(courseId) : [];
        } catch {
            cards = [];
        }
        index = 0;
        flippedCard = false;
        loading = false;
    }

    function next(): void {
        if (index < cards.length - 1) {
            index += 1;
            flippedCard = false;
        }
    }

    function prev(): void {
        if (index > 0) {
            index -= 1;
            flippedCard = false;
        }
    }

    function flip(): void {
        flippedCard = !flippedCard;
    }

    function shuffle(): void {
        for (let i = cards.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [cards[i]!, cards[j]!] = [cards[j]!, cards[i]!];
        }
        cards = [...cards];
        index = 0;
        flippedCard = false;
    }

    function onKey(event: KeyboardEvent): void {
        if (event.key === "ArrowRight") next();
        else if (event.key === "ArrowLeft") prev();
        else if (event.key === " ") {
            event.preventDefault();
            flip();
        }
    }
</script>

<div class="cards-screen">
    <header class="head">
        <button type="button" class="back" onclick={() => push(`/games/${params?.id ?? ""}`)}>← Back to games</button>
        <h1 class="title">Flashcards</h1>
        <p class="subtitle">{courseTitle}</p>
    </header>

    {#if loading}
        <div class="center"><span class="loading loading-spinner loading-lg"></span></div>
    {:else if cards.length === 0}
        <div class="empty">
            <p class="empty-title">No flashcards yet</p>
            <p class="muted">This course has no readable content to turn into flashcards.</p>
        </div>
    {:else}
        <p class="counter">Card {index + 1} of {cards.length}</p>

        <button type="button" class="flashcard" class:flipped={flippedCard} onclick={flip} aria-label="Flip card">
            <span class="fc-inner">
                <span class="fc-face fc-front">
                    <span class="fc-tag">Term</span>
                    <span class="fc-text">{current?.front}</span>
                    <span class="fc-hint">Click to flip</span>
                </span>
                <span class="fc-face fc-back">
                    <span class="fc-tag">Explanation</span>
                    <span class="fc-text small">{current?.back}</span>
                </span>
            </span>
        </button>

        <div class="controls">
            <button type="button" class="btn btn-ghost" onclick={prev} disabled={index === 0}>← Prev</button>
            <button type="button" class="btn btn-sm btn-ghost" onclick={shuffle}>↺ Shuffle</button>
            <button type="button" class="btn btn-ghost" onclick={next} disabled={index === cards.length - 1}>Next →</button>
        </div>
    {/if}
</div>

<style>
    .cards-screen {
        flex: 1;
        min-height: 0;
        overflow-y: auto;
        width: 90%;
        max-width: 48rem;
        margin: 0 auto;
        padding: 1.5rem 0 2.5rem;
        display: flex;
        flex-direction: column;
        gap: 1.25rem;
    }

    .head {
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

    .center {
        display: flex;
        justify-content: center;
        padding: 3rem 0;
    }

    .empty {
        text-align: center;
        padding: 2.5rem 1rem;
        border: 1px dashed color-mix(in oklab, var(--color-base-content) 18%, transparent);
        border-radius: 0.75rem;
    }

    .empty-title {
        font-weight: 700;
        margin-bottom: 0.25rem;
    }

    .muted {
        color: color-mix(in oklab, var(--color-base-content) 60%, transparent);
        font-size: 0.9rem;
    }

    .counter {
        text-align: center;
        font-size: 0.85rem;
        color: color-mix(in oklab, var(--color-base-content) 60%, transparent);
    }

    .flashcard {
        width: 100%;
        min-height: 16rem;
        border: none;
        background: none;
        padding: 0;
        cursor: pointer;
        perspective: 1200px;
    }

    .flashcard:focus-visible {
        outline: 2px solid var(--color-primary);
        outline-offset: 3px;
        border-radius: 1rem;
    }

    .fc-inner {
        position: relative;
        display: block;
        width: 100%;
        min-height: 16rem;
        transform-style: preserve-3d;
        transition: transform 0.45s ease;
    }

    .flashcard.flipped .fc-inner {
        transform: rotateY(180deg);
    }

    .fc-face {
        position: absolute;
        inset: 0;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 0.75rem;
        padding: 1.5rem;
        border-radius: 1rem;
        backface-visibility: hidden;
        text-align: center;
    }

    .fc-front {
        background: color-mix(in oklab, var(--color-primary) 12%, var(--color-base-100));
        border: 1px solid color-mix(in oklab, var(--color-primary) 30%, transparent);
    }

    .fc-back {
        transform: rotateY(180deg);
        background: var(--color-base-100);
        border: 1px solid color-mix(in oklab, var(--color-base-content) 15%, transparent);
        overflow-y: auto;
    }

    .fc-tag {
        font-size: 0.65rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 700;
        color: var(--color-primary);
    }

    .fc-text {
        font-size: clamp(1.3rem, 4vw, 1.9rem);
        font-weight: 800;
        color: var(--color-base-content);
        overflow-wrap: anywhere;
    }

    .fc-text.small {
        font-size: clamp(0.95rem, 2.4vw, 1.15rem);
        font-weight: 500;
        line-height: 1.5;
    }

    .fc-hint {
        font-size: 0.75rem;
        color: color-mix(in oklab, var(--color-base-content) 50%, transparent);
    }

    .controls {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.75rem;
    }
</style>
