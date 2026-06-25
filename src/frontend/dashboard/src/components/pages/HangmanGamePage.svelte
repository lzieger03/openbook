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
Hangman built from the course's real content: the secret words are subject terms
extracted from the textbook pages. Guess letters via the on-screen keyboard or your
physical keyboard before the figure is complete.
-->
<script lang="ts">
    import {onMount} from "svelte";
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

    const courseTitle = $derived(
        state.courses.find((course) => course.id === params?.id)?.name ?? "Course",
    );

    const ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("");
    const MAX_WRONG = 6;

    let words = $state<string[]>([]);
    let loading = $state(true);
    let word = $state(""); // uppercase secret word
    let guessed = $state<string[]>([]);
    let wrong = $state(0);

    const lettersInWord = $derived(new Set(word.split("").filter((c) => /[A-ZÄÖÜ]/.test(c))));
    const solved = $derived(
        word.length > 0 && [...lettersInWord].every((letter) => guessed.includes(letter)),
    );
    const lost = $derived(wrong >= MAX_WRONG);
    const over = $derived(solved || lost);

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
        let terms: string[] = [];
        try {
            terms = courseId ? await loadCourseTerms(courseId) : [];
        } catch {
            terms = [];
        }

        // Good hangman words: letters (and spaces), 3–18 chars. Fall back to a small
        // neutral set when the course has nothing suitable.
        words = terms
            .map((term) => term.toUpperCase())
            .filter((term) => /^[A-ZÄÖÜ ]{3,18}$/.test(term));

        if (words.length === 0) {
            words = ["VARIABLE", "FUNCTION", "DATABASE", "ELEMENT", "BROWSER", "NETWORK"];
        }

        loading = false;
        newWord();
    }

    function newWord(): void {
        const pick = words[Math.floor(Math.random() * words.length)] ?? "";
        word = pick;
        guessed = [];
        wrong = 0;
    }

    function guess(letter: string): void {
        if (over || guessed.includes(letter)) {
            return;
        }
        guessed = [...guessed, letter];
        if (!word.includes(letter)) {
            wrong += 1;
        }
    }

    function reveal(char: string): string {
        if (char === " ") return " ";
        if (!/[A-ZÄÖÜ]/.test(char)) return char; // punctuation/numbers shown as-is
        return guessed.includes(char) || lost ? char : "_";
    }

    function onKey(event: KeyboardEvent): void {
        const key = event.key.toUpperCase();
        if (key.length === 1 && /[A-ZÄÖÜ]/.test(key)) {
            guess(key);
        } else if (event.key === "Enter" && over) {
            newWord();
        }
    }
</script>

<div class="hm-screen">
    <header class="head">
        <button type="button" class="back" onclick={() => push(`/games/${params?.id ?? ""}`)}>← Back to games</button>
        <h1 class="title">Hangman</h1>
        <p class="subtitle">{courseTitle}</p>
    </header>

    {#if loading}
        <div class="center"><span class="loading loading-spinner loading-lg"></span></div>
    {:else}
        <div class="stage">
            <!-- Gallows + figure; parts appear with each wrong guess. -->
            <svg class="gallows" viewBox="0 0 120 140" aria-hidden="true">
                <line x1="10" y1="135" x2="80" y2="135" />
                <line x1="30" y1="135" x2="30" y2="10" />
                <line x1="30" y1="10" x2="85" y2="10" />
                <line x1="85" y1="10" x2="85" y2="25" />
                {#if wrong > 0}<circle class="part" cx="85" cy="35" r="10" />{/if}
                {#if wrong > 1}<line class="part" x1="85" y1="45" x2="85" y2="80" />{/if}
                {#if wrong > 2}<line class="part" x1="85" y1="55" x2="70" y2="68" />{/if}
                {#if wrong > 3}<line class="part" x1="85" y1="55" x2="100" y2="68" />{/if}
                {#if wrong > 4}<line class="part" x1="85" y1="80" x2="72" y2="100" />{/if}
                {#if wrong > 5}<line class="part" x1="85" y1="80" x2="98" y2="100" />{/if}
            </svg>

            <div class="info">
                <p class="lives">Wrong: {wrong} / {MAX_WRONG}</p>
                <div class="word" aria-label="Secret word">
                    {#each word.split("") as char, i (i)}
                        <span class="slot" class:space={char === " "} class:filled={reveal(char) !== "_"}>
                            {reveal(char)}
                        </span>
                    {/each}
                </div>

                {#if over}
                    <div class="result" role="status">
                        {#if solved}
                            <p class="win">🎉 Correct!</p>
                        {:else}
                            <p class="lose">💀 The word was <strong>{word}</strong></p>
                        {/if}
                        <button type="button" class="btn btn-primary btn-sm" onclick={newWord}>Next word</button>
                    </div>
                {/if}
            </div>
        </div>

        <div class="keyboard" role="group" aria-label="Letters">
            {#each ALPHABET as letter (letter)}
                {@const used = guessed.includes(letter)}
                <button
                    type="button"
                    class="key"
                    class:hit={used && word.includes(letter)}
                    class:miss={used && !word.includes(letter)}
                    disabled={used || over}
                    onclick={() => guess(letter)}
                >
                    {letter}
                </button>
            {/each}
        </div>
    {/if}
</div>

<style>
    .hm-screen {
        flex: 1;
        min-height: 0;
        overflow-y: auto;
        width: 90%;
        max-width: 44rem;
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

    .stage {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        justify-content: center;
        gap: 1.5rem;
    }

    .gallows {
        width: 9rem;
        height: 10.5rem;
        flex: 0 0 auto;
    }

    .gallows line,
    .gallows circle {
        stroke: var(--color-base-content);
        stroke-width: 3;
        stroke-linecap: round;
        fill: none;
    }

    .gallows .part {
        stroke: var(--color-error);
    }

    .info {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.85rem;
        min-width: 0;
    }

    .lives {
        font-size: 0.85rem;
        font-weight: 600;
        color: color-mix(in oklab, var(--color-base-content) 65%, transparent);
    }

    .word {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 0.4rem;
    }

    .slot {
        display: grid;
        place-items: center;
        min-width: 1.4rem;
        font-size: 1.6rem;
        font-weight: 800;
        border-bottom: 3px solid color-mix(in oklab, var(--color-base-content) 35%, transparent);
        color: var(--color-base-content);
    }

    .slot.space {
        border-bottom: none;
        min-width: 0.8rem;
    }

    .slot.filled {
        border-bottom-color: var(--color-primary);
    }

    .result {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.5rem;
    }

    .win {
        font-weight: 800;
        color: var(--color-success);
    }

    .lose {
        font-weight: 600;
        color: color-mix(in oklab, var(--color-base-content) 80%, transparent);
    }

    .keyboard {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(2.1rem, 1fr));
        gap: 0.4rem;
        max-width: 30rem;
        margin: 0 auto;
        width: 100%;
    }

    .key {
        aspect-ratio: 1 / 1;
        border-radius: 0.5rem;
        border: 1px solid color-mix(in oklab, var(--color-base-content) 18%, transparent);
        background: color-mix(in oklab, var(--color-base-100) 80%, transparent);
        color: var(--color-base-content);
        font-weight: 700;
        cursor: pointer;
        transition: background 0.12s ease, transform 0.08s ease;
    }

    .key:not(:disabled):hover {
        background: color-mix(in oklab, var(--color-primary) 16%, transparent);
        border-color: color-mix(in oklab, var(--color-primary) 45%, transparent);
    }

    .key:disabled {
        cursor: default;
    }

    .key.hit {
        background: color-mix(in oklab, var(--color-success) 22%, transparent);
        border-color: color-mix(in oklab, var(--color-success) 45%, transparent);
        color: var(--color-base-content);
    }

    .key.miss {
        background: color-mix(in oklab, var(--color-error) 18%, transparent);
        border-color: color-mix(in oklab, var(--color-error) 40%, transparent);
        opacity: 0.7;
    }
</style>
