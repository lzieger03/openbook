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
A small memory matching game (under "Games" in the course chat sidebar). The deck
is built from the course's own content — its skills, textbook names and page titles —
so learners match terms from their course. Falls back to neutral symbols when a
course has no content yet. Frontend-only.
-->
<script lang="ts">
    import {onMount, onDestroy} from "svelte";
    import {push} from "svelte-spa-router";
    import {dashboardStore} from "../../stores/dashboard.store.js";
    import type {DashboardState} from "../../stores/dashboard.store.js";
    import {loadCourseTerms} from "../../data/course-terms.js";

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
        void loadDeck();
        return () => {
            unsubscribe();
            clearTimers();
        };
    });

    const course = $derived(state.courses.find((c) => c.id === params?.id) ?? null);
    const courseTitle = $derived(course?.name ?? "Course");

    // ── Deck source (course terms) ────────────────────────────────────────────
    const SYMBOLS = ["🧠", "📚", "✏️", "💡", "🔬", "🧮", "🌍", "⚛️", "🧪", "📐", "🔤", "🧬"];

    let pool = $state<string[]>([]);
    let loading = $state(true);

    /** Build the term pool from the course's real page content. */
    async function loadDeck(): Promise<void> {
        const courseId = params?.id;
        loading = true;

        try {
            pool = courseId ? await loadCourseTerms(courseId) : [];
        } catch {
            // Non-critical: fall back to neutral symbols below.
            pool = [];
        }

        loading = false;
        startGame();
    }

    // Use course terms when there are enough; otherwise neutral symbols.
    const usingCourseTerms = $derived(pool.length >= 3);
    const deckSource = $derived(usingCourseTerms ? pool : SYMBOLS);
    const maxPairs = $derived(deckSource.length);

    const LEVELS = [
        {label: "Easy", pairs: 6},
        {label: "Medium", pairs: 8},
        {label: "Hard", pairs: 12},
    ] as const;

    // Only offer levels the deck can fill; if even "Easy" is too big, offer "All".
    const levels = $derived.by(() => {
        const feasible = LEVELS.filter((level) => level.pairs <= maxPairs);
        return feasible.length > 0 ? feasible : [{label: "All", pairs: maxPairs}];
    });

    // ── Game state ───────────────────────────────────────────────────────────
    interface Card {
        id: number;
        symbol: string;
        flipped: boolean;
        matched: boolean;
    }

    let pairs = $state(6);
    let cards = $state<Card[]>([]);
    let flipped = $state<number[]>([]);
    let moves = $state(0);
    let matches = $state(0);
    let locked = $state(false);
    let started = $state(false);
    let seconds = $state(0);
    let flipBackTimer: ReturnType<typeof setTimeout> | null = null;
    let tickTimer: ReturnType<typeof setInterval> | null = null;

    const won = $derived(cards.length > 0 && matches === pairs);

    function clearTimers(): void {
        if (flipBackTimer) {
            clearTimeout(flipBackTimer);
            flipBackTimer = null;
        }
        if (tickTimer) {
            clearInterval(tickTimer);
            tickTimer = null;
        }
    }

    function shuffle<T>(items: T[]): T[] {
        const copy = [...items];
        for (let i = copy.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [copy[i]!, copy[j]!] = [copy[j]!, copy[i]!];
        }
        return copy;
    }

    function startGame(): void {
        clearTimers();
        // Clamp the requested difficulty to what the deck can fill.
        const wanted = Math.min(pairs, maxPairs);
        pairs = wanted >= 2 ? wanted : maxPairs;

        const chosen = shuffle(deckSource).slice(0, pairs);
        const deck = shuffle([...chosen, ...chosen]);
        cards = deck.map((symbol, index) => ({id: index, symbol, flipped: false, matched: false}));
        flipped = [];
        moves = 0;
        matches = 0;
        locked = false;
        started = false;
        seconds = 0;
    }

    function setLevel(value: number): void {
        pairs = Math.min(value, maxPairs);
        startGame();
    }

    function startTimer(): void {
        if (tickTimer) {
            return;
        }
        started = true;
        tickTimer = setInterval(() => (seconds += 1), 1000);
    }

    function flip(index: number): void {
        const card = cards[index];
        if (loading || locked || won || !card || card.flipped || card.matched) {
            return;
        }

        startTimer();
        cards[index] = {...card, flipped: true};
        flipped = [...flipped, index];

        if (flipped.length < 2) {
            return;
        }

        moves += 1;
        const [a, b] = flipped;
        const first = cards[a!]!;
        const second = cards[b!]!;

        if (first.symbol === second.symbol) {
            cards[a!] = {...first, matched: true};
            cards[b!] = {...second, matched: true};
            matches += 1;
            flipped = [];
            if (matches === pairs) {
                clearTimers();
            }
        } else {
            locked = true;
            flipBackTimer = setTimeout(() => {
                cards[a!] = {...cards[a!]!, flipped: false};
                cards[b!] = {...cards[b!]!, flipped: false};
                flipped = [];
                locked = false;
                flipBackTimer = null;
            }, 850);
        }
    }

    function formatTime(total: number): string {
        const m = Math.floor(total / 60);
        const s = total % 60;
        return `${m}:${s.toString().padStart(2, "0")}`;
    }

    onDestroy(clearTimers);
</script>

<div class="game-screen">
    <header class="game-head">
        <button type="button" class="back" onclick={() => push(`/games/${params?.id ?? ""}`)}>← Back to games</button>
        <h1 class="title">Memory</h1>
        <p class="subtitle">{courseTitle}</p>
    </header>

    {#if loading}
        <div class="center"><span class="loading loading-spinner loading-lg"></span></div>
    {:else}
        <div class="toolbar">
            <div class="levels" role="group" aria-label="Difficulty">
                {#each levels as level (level.pairs)}
                    <button
                        type="button"
                        class="level"
                        class:active={pairs === level.pairs}
                        onclick={() => setLevel(level.pairs)}
                    >
                        {level.label}
                    </button>
                {/each}
            </div>

            <div class="stats">
                <span class="stat"><span class="stat-label">Moves</span> {moves}</span>
                <span class="stat"><span class="stat-label">Pairs</span> {matches}/{pairs}</span>
                <span class="stat"><span class="stat-label">Time</span> {formatTime(seconds)}</span>
            </div>

            <button type="button" class="btn btn-sm btn-ghost restart" onclick={startGame}>↺ Restart</button>
        </div>

        {#if !usingCourseTerms}
            <p class="hint">No course content to play with yet — using neutral symbols.</p>
        {/if}

        <div class="board" class:hard={pairs >= 12} aria-label="Memory board">
            {#each cards as card, index (card.id)}
                <button
                    type="button"
                    class="card"
                    class:flipped={card.flipped || card.matched}
                    class:matched={card.matched}
                    disabled={locked || card.matched}
                    aria-label={card.flipped || card.matched ? card.symbol : "Hidden card"}
                    onclick={() => flip(index)}
                >
                    <span class="card-inner">
                        <span class="card-face card-front" aria-hidden="true">?</span>
                        <span class="card-face card-back" class:text={card.symbol.length > 2} aria-hidden="true">
                            {card.symbol}
                        </span>
                    </span>
                </button>
            {/each}
        </div>
    {/if}

    {#if won}
        <div class="win" role="status">
            <p class="win-title">🎉 Solved!</p>
            <p class="win-detail">{moves} moves · {formatTime(seconds)}</p>
            <div class="win-actions">
                <button type="button" class="btn btn-primary" onclick={startGame}>Play again</button>
                <button type="button" class="btn btn-ghost" onclick={() => push(`/games/${params?.id ?? ""}`)}>Back to games</button>
            </div>
        </div>
    {/if}
</div>

<style>
    .game-screen {
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

    .game-head {
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

    .hint {
        text-align: center;
        font-size: 0.85rem;
        color: color-mix(in oklab, var(--color-base-content) 60%, transparent);
        margin-top: -0.5rem;
    }

    .toolbar {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        justify-content: space-between;
        gap: 0.75rem 1rem;
    }

    .levels {
        display: inline-flex;
        border-radius: 999px;
        padding: 0.2rem;
        background: color-mix(in oklab, var(--color-base-content) 8%, transparent);
        border: 1px solid color-mix(in oklab, var(--color-base-content) 12%, transparent);
    }

    .level {
        border: none;
        background: none;
        cursor: pointer;
        padding: 0.35rem 0.9rem;
        border-radius: 999px;
        font-size: 0.85rem;
        font-weight: 600;
        color: color-mix(in oklab, var(--color-base-content) 70%, transparent);
    }

    .level.active {
        background: var(--color-primary);
        color: var(--color-primary-content);
    }

    .stats {
        display: flex;
        gap: 1rem;
        font-weight: 700;
        color: var(--color-base-content);
    }

    .stat-label {
        font-size: 0.65rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: color-mix(in oklab, var(--color-base-content) 55%, transparent);
        margin-right: 0.2rem;
    }

    .board {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 0.7rem;
    }

    @media (min-width: 32rem) {
        .board {
            grid-template-columns: repeat(4, 1fr);
        }
        .board.hard {
            grid-template-columns: repeat(6, 1fr);
        }
    }

    .card {
        aspect-ratio: 1 / 1;
        border: none;
        background: none;
        padding: 0;
        cursor: pointer;
        perspective: 600px;
    }

    .card:disabled {
        cursor: default;
    }

    .card:focus-visible {
        outline: 2px solid var(--color-primary);
        outline-offset: 2px;
        border-radius: 0.8rem;
    }

    .card-inner {
        position: relative;
        display: block;
        width: 100%;
        height: 100%;
        transform-style: preserve-3d;
        transition: transform 0.35s ease;
    }

    .card.flipped .card-inner {
        transform: rotateY(180deg);
    }

    .card-face {
        position: absolute;
        inset: 0;
        display: grid;
        place-items: center;
        border-radius: 0.8rem;
        backface-visibility: hidden;
        font-size: clamp(1.4rem, 6vw, 2.2rem);
        user-select: none;
    }

    .card-front {
        color: color-mix(in oklab, var(--color-primary) 70%, var(--color-base-content));
        background: color-mix(in oklab, var(--color-primary) 16%, var(--color-base-100));
        border: 1px solid color-mix(in oklab, var(--color-primary) 30%, transparent);
        font-weight: 800;
    }

    .card:not(:disabled):hover .card-front {
        background: color-mix(in oklab, var(--color-primary) 26%, var(--color-base-100));
    }

    .card-back {
        transform: rotateY(180deg);
        background: var(--color-base-100);
        border: 1px solid color-mix(in oklab, var(--color-base-content) 15%, transparent);
    }

    /* Text terms (course content) need smaller, wrapping type instead of big emoji. */
    .card-back.text {
        font-size: clamp(0.7rem, 2.4vw, 0.95rem);
        font-weight: 700;
        line-height: 1.2;
        text-align: center;
        padding: 0.35rem;
        overflow-wrap: anywhere;
        color: var(--color-base-content);
    }

    .card.matched .card-back {
        background: color-mix(in oklab, var(--color-success) 18%, var(--color-base-100));
        border-color: color-mix(in oklab, var(--color-success) 45%, transparent);
        box-shadow: 0 0 14px color-mix(in oklab, var(--color-success) 30%, transparent);
    }

    .win {
        text-align: center;
        padding: 1.5rem;
        border-radius: 1rem;
        background: color-mix(in oklab, var(--color-primary) 10%, var(--color-base-100));
        border: 1px solid color-mix(in oklab, var(--color-primary) 30%, transparent);
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.5rem;
    }

    .win-title {
        font-size: 1.5rem;
        font-weight: 800;
        color: var(--color-base-content);
    }

    .win-detail {
        color: color-mix(in oklab, var(--color-base-content) 70%, transparent);
    }

    .win-actions {
        display: flex;
        gap: 0.75rem;
        margin-top: 0.5rem;
    }
</style>
