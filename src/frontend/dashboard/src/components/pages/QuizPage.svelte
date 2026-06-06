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
Quiz page (prototype). A Kahoot-style multiple-choice quiz for a course.
Selecting an answer reveals the result and auto-advances to the next question.

Note: no quiz backend exists yet, so the questions are placeholder sample data.
TODO: load questions from the quiz API once it exists and report the result.
-->
<script lang="ts">
    import {onDestroy, onMount} from "svelte";
    import {push} from "svelte-spa-router";
    import {dashboardStore} from "../../stores/dashboard.store.js";
    import type {DashboardState} from "../../stores/dashboard.store.js";

    interface Option {
        text: string;
        correct: boolean;
    }

    interface Question {
        prompt: string;
        options: Option[];
    }

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
        const unsubscribe = dashboardStore.subscribe((value) => {
            state = value;
        });

        if (state.courses.length === 0) {
            dashboardStore.refresh();
        }

        return unsubscribe;
    });

    const courseTitle = $derived(
        state.courses.find((course) => course.id === params?.id)?.name ?? "HTML, beginners",
    );

    // Placeholder sample quiz until a quiz backend exists.
    const questions: Question[] = [
        {
            prompt: "How do you start a HTML file?",
            options: [
                {text: "<html>", correct: true},
                {text: "<htm>", correct: false},
                {text: "<hml>", correct: false},
                {text: "<hm>", correct: false},
            ],
        },
        {
            prompt: "Which tag holds the page title?",
            options: [
                {text: "<title>", correct: true},
                {text: "<head>", correct: false},
                {text: "<h1>", correct: false},
                {text: "<meta>", correct: false},
            ],
        },
        {
            prompt: "Which tag creates a hyperlink?",
            options: [
                {text: "<a>", correct: true},
                {text: "<link>", correct: false},
                {text: "<href>", correct: false},
                {text: "<nav>", correct: false},
            ],
        },
        {
            prompt: "Which tag inserts an image?",
            options: [
                {text: "<img>", correct: true},
                {text: "<image>", correct: false},
                {text: "<src>", correct: false},
                {text: "<pic>", correct: false},
            ],
        },
        {
            prompt: "Which tag defines a list item?",
            options: [
                {text: "<li>", correct: true},
                {text: "<ul>", correct: false},
                {text: "<ol>", correct: false},
                {text: "<item>", correct: false},
            ],
        },
    ];

    const letters = ["A", "B", "C", "D"];

    let index = $state(0);
    let selected = $state<number | null>(null);
    let score = $state(0);
    let finished = $state(false);
    let timer: ReturnType<typeof setTimeout> | null = null;

    const current = $derived(questions[index]);
    const answered = $derived(selected !== null);
    const progressPct = $derived(((index + (selected !== null ? 1 : 0)) / questions.length) * 100);

    function advance(): void {
        timer = null;
        if (index === questions.length - 1) {
            finished = true;
        } else {
            index += 1;
            selected = null;
        }
    }

    function choose(optionIndex: number): void {
        if (selected !== null) {
            return;
        }

        selected = optionIndex;
        if (current.options[optionIndex].correct) {
            score += 1;
        }

        // Reveal the result briefly, then move on automatically.
        timer = setTimeout(advance, 950);
    }

    function restart(): void {
        index = 0;
        selected = null;
        score = 0;
        finished = false;
    }

    onDestroy(() => {
        if (timer) {
            clearTimeout(timer);
        }
    });
</script>

<div class="quiz">
    <header class="quiz-top">
        <button type="button" class="content-btn" onclick={() => push(`/content/${params?.id ?? ""}`)}>
            ← Content
        </button>
        {#if !finished}
            <div class="progress-track" aria-hidden="true">
                <div class="progress-fill" style="width: {progressPct}%"></div>
            </div>
        {/if}
    </header>

    {#if finished}
        <section class="stage result">
            <h1 class="course">{courseTitle}</h1>
            <div class="score-ring">{score}/{questions.length}</div>
            <p class="result-text">
                {score === questions.length ? "Perfect! 🎉" : "Nice work — keep practising!"}
            </p>
            <div class="result-actions">
                <button type="button" class="btn btn-primary" onclick={restart}>Try again</button>
                <button type="button" class="btn btn-ghost" onclick={() => push("/")}>Back to Dashboard</button>
            </div>
        </section>
    {:else}
        <section class="stage">
            <h1 class="course">{courseTitle}</h1>
            <span class="progress-pill">Question {index + 1} / {questions.length}</span>
            <h2 class="prompt">{current.prompt}</h2>

            <div class="answers">
                {#each current.options as option, optionIndex (option.text)}
                    <button
                        type="button"
                        class="answer c{optionIndex}"
                        class:correct={answered && option.correct}
                        class:wrong={answered && optionIndex === selected && !option.correct}
                        class:dim={answered && !option.correct && optionIndex !== selected}
                        disabled={answered}
                        onclick={() => choose(optionIndex)}
                    >
                        <span class="letter">{letters[optionIndex]}</span>
                        <span class="text">{option.text}</span>
                    </button>
                {/each}
            </div>
        </section>
    {/if}
</div>

<style>
    .quiz {
        flex: 1;
        min-height: 0;
        display: flex;
        flex-direction: column;
        width: 100%;
        background:
            radial-gradient(120% 70% at 50% 0%, color-mix(in oklab, var(--color-primary) 8%, transparent), transparent 55%),
            var(--color-base-200);
    }

    .quiz-top {
        flex: 0 0 auto;
        display: flex;
        align-items: center;
        gap: 1.5rem;
        padding: 1.25rem 1.5rem;
    }

    .content-btn {
        flex: 0 0 auto;
        padding: 0.5rem 1.25rem;
        border-radius: 0.75rem;
        font-weight: 600;
        color: color-mix(in oklab, var(--color-base-content) 80%, transparent);
        background: color-mix(in oklab, var(--color-base-100) 70%, transparent);
        border: 1px solid color-mix(in oklab, var(--color-base-content) 14%, transparent);
        cursor: pointer;
    }

    .content-btn:hover {
        border-color: color-mix(in oklab, var(--color-primary) 45%, transparent);
    }

    .progress-track {
        flex: 1 1 auto;
        height: 0.5rem;
        border-radius: 999px;
        overflow: hidden;
        background: color-mix(in oklab, var(--color-base-content) 12%, transparent);
    }

    .progress-fill {
        height: 100%;
        border-radius: 999px;
        background: linear-gradient(90deg, var(--color-primary), var(--color-success));
        transition: width 0.3s ease;
    }

    .stage {
        flex: 1;
        min-height: 0;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 1.25rem;
        width: 90%;
        max-width: 64rem;
        margin: 0 auto;
        padding: 1rem 0 2.5rem;
    }

    .course {
        font-size: clamp(1.3rem, 2.4vw, 1.9rem);
        font-weight: 700;
        text-align: center;
        color: var(--color-base-content);
        text-shadow: 0 0 20px color-mix(in oklab, var(--color-primary) 40%, transparent);
    }

    .progress-pill {
        padding: 0.3rem 1rem;
        border-radius: 999px;
        font-weight: 700;
        color: var(--color-primary);
        background: color-mix(in oklab, var(--color-primary) 16%, transparent);
        border: 1px solid color-mix(in oklab, var(--color-primary) 35%, transparent);
    }

    .prompt {
        font-size: clamp(1.7rem, 3.6vw, 2.8rem);
        font-weight: 800;
        text-align: center;
        color: var(--color-base-content);
        text-shadow: 0 0 22px color-mix(in oklab, var(--color-primary) 35%, transparent);
        margin: 0.5rem 0 1rem;
    }

    .answers {
        width: 100%;
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1.1rem;
    }

    /* Answer colours map to DaisyUI semantic tokens (no hardcoded hex). */
    .answer {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 1.4rem 1.5rem;
        border-radius: 1rem;
        border: none;
        font-family: ui-monospace, "SF Mono", Menlo, monospace;
        font-size: 1.2rem;
        font-weight: 700;
        cursor: pointer;
        transition: transform 0.12s ease, opacity 0.2s ease, box-shadow 0.2s ease;
        box-shadow: 0 6px 18px color-mix(in oklab, var(--color-base-content) 14%, transparent);
    }

    .answer:hover:not(:disabled) {
        transform: translateY(-3px);
    }

    .answer:focus-visible {
        outline: 3px solid var(--color-base-content);
        outline-offset: 3px;
    }

    .letter {
        display: grid;
        place-items: center;
        width: 2.1rem;
        height: 2.1rem;
        flex: 0 0 auto;
        border-radius: 0.6rem;
        font-family: inherit;
        background: color-mix(in oklab, currentColor 18%, transparent);
    }

    .text {
        flex: 1 1 auto;
        text-align: center;
    }

    .answer.c0 {
        background: var(--color-error);
        color: var(--color-error-content);
    }

    .answer.c1 {
        background: var(--color-info);
        color: var(--color-info-content);
    }

    .answer.c2 {
        background: var(--color-warning);
        color: var(--color-warning-content);
    }

    .answer.c3 {
        background: var(--color-success);
        color: var(--color-success-content);
    }

    .answer.dim {
        opacity: 0.35;
    }

    .answer.correct {
        outline: 4px solid var(--color-base-content);
        outline-offset: 3px;
        transform: translateY(-3px);
    }

    .answer.wrong {
        opacity: 0.65;
        text-decoration: line-through;
    }

    .result {
        justify-content: center;
    }

    .score-ring {
        display: grid;
        place-items: center;
        width: 9rem;
        height: 9rem;
        border-radius: 999px;
        font-size: 2rem;
        font-weight: 800;
        color: var(--color-base-content);
        background: color-mix(in oklab, var(--color-primary) 14%, transparent);
        border: 4px solid color-mix(in oklab, var(--color-primary) 55%, transparent);
        box-shadow: 0 0 28px color-mix(in oklab, var(--color-primary) 35%, transparent);
    }

    .result-text {
        font-size: 1.2rem;
        font-weight: 600;
        color: color-mix(in oklab, var(--color-base-content) 80%, transparent);
    }

    .result-actions {
        display: flex;
        gap: 1rem;
    }

    @media (max-width: 40rem) {
        .answers {
            grid-template-columns: 1fr;
        }
    }
</style>
