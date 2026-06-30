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
AI-generated, AI-graded course exam. The assistant backend produces a mix of open
free-text and multiple-choice questions over the course chat WebSocket channel. The
learner answers them in a single form; on submission the backend grades free text via
the LLM and multiple choice by comparison, then awards points and skills like a quiz.
-->
<script lang="ts">
    import {onDestroy, onMount} from "svelte";
    import {push} from "svelte-spa-router";

    import {fetchMaterials} from "../../api/content.js";
    import {fetchExamAttempts, deleteExamAttempt} from "../../api/exams.js";
    import type {ExamAttemptDto} from "../../api/exams.js";
    import {dashboardStore} from "../../stores/dashboard.store.js";
    import type {DashboardState} from "../../stores/dashboard.store.js";
    import {clearPageContext, setCourseContext} from "../../stores/page-context.store.js";
    import type {PageContext} from "../../stores/page-context.store.js";
    import {createExamStore} from "../../stores/exam.store.js";
    import type {ExamAnswer, ExamState} from "../../stores/exam.store.js";

    let {params}: {params?: {id?: string}} = $props();

    interface TextbookChoice {
        id: string;
        name: string;
        skills: {id: string; name: string}[];
    }

    let state = $state<DashboardState>({
        isLoading: true,
        errorMessage: "",
        user: null,
        stats: null,
        skills: [],
        courses: [],
    });

    const exam = createExamStore(() => params?.id, {
        onResultRecorded: () => {
            // Points/skills were awarded server-side; refresh the dashboard totals and
            // the exam history (a new/updated attempt was just saved).
            dashboardStore.refresh();
            void loadAttempts();
        },
    });
    let examState = $state<ExamState>({
        connection: "disconnected",
        isLoading: false,
        isGrading: false,
        errorMessage: "",
        questions: [],
        contextSource: null,
        sources: [],
        textbookId: null,
        pageId: null,
        result: null,
    });

    // Give the global Quick Chat the current-page context (an exam in this course).
    let contextToken: PageContext | null = null;
    $effect(() => {
        contextToken = setCourseContext("taking an exam", state.courses.find((course) => course.id === params?.id));
    });
    onDestroy(() => clearPageContext(contextToken));

    const letters = ["A", "B", "C", "D", "E", "F"];

    // Learner answers keyed by question id: free text, or the picked option index.
    let textAnswers = $state<Record<string, string>>({});
    let choiceAnswers = $state<Record<string, number>>({});

    // Textbook selection step shown before an exam is generated.
    let textbooks = $state<TextbookChoice[]>([]);
    let textbooksLoading = $state(true);
    let textbooksError = $state("");
    let selectedTextbookId = $state<string | null>(null);

    // Saved exam history (review / repeat / delete).
    let attempts = $state<ExamAttemptDto[]>([]);
    let deletingAttemptId = $state<string | null>(null);

    onMount(() => {
        const unsubscribeDashboard = dashboardStore.subscribe((value) => {
            state = value;
        });

        if (state.courses.length === 0) {
            dashboardStore.refresh();
        }

        const unsubscribeExam = exam.subscribe((value) => {
            examState = value;
        });

        void loadTextbooks();
        void loadAttempts();

        return () => {
            unsubscribeDashboard();
            unsubscribeExam();
            void exam.disconnect();
        };
    });

    const courseTitle = $derived(
        state.courses.find((course) => course.id === params?.id)?.name ?? "Course",
    );
    const selecting = $derived(selectedTextbookId === null);
    const selectedTextbookName = $derived(
        textbooks.find((book) => book.id === selectedTextbookId)?.name ?? "",
    );
    const questions = $derived(examState.questions);
    const result = $derived(examState.result);
    const isBusy = $derived(
        examState.isLoading
            || examState.connection === "connecting"
            || examState.connection === "wait_before_retry",
    );

    // Every question must be answered before the exam can be submitted.
    const answeredCount = $derived(
        questions.filter((question) =>
            question.kind === "multiple_choice"
                ? choiceAnswers[question.id] !== undefined
                : (textAnswers[question.id] ?? "").trim().length > 0,
        ).length,
    );
    const allAnswered = $derived(questions.length > 0 && answeredCount === questions.length);

    const scorePercent = $derived(
        result ? Math.round((result.max_points ? result.total_points / result.max_points : 0) * 100) : 0,
    );

    function resetAnswers(): void {
        textAnswers = {};
        choiceAnswers = {};
    }

    async function loadTextbooks(): Promise<void> {
        const courseId = params?.id;
        if (!courseId) {
            textbooksLoading = false;
            textbooksError = "No course selected.";
            return;
        }

        textbooksLoading = true;
        textbooksError = "";

        try {
            const materials = await fetchMaterials(courseId);
            const choices: TextbookChoice[] = [];

            for (const material of materials) {
                if (material.textbook && typeof material.textbook === "object") {
                    choices.push({
                        id: material.textbook.id,
                        name: material.textbook.name,
                        skills: (material.textbook.skills ?? []).map((skill) => ({id: skill.id, name: skill.name})),
                    });
                }
            }

            textbooks = choices;
        } catch (error) {
            textbooksError = error instanceof Error ? error.message : String(error);
        } finally {
            textbooksLoading = false;
        }
    }

    async function chooseTextbook(textbookId: string): Promise<void> {
        selectedTextbookId = textbookId;
        await loadExam();
    }

    function backToSelection(): void {
        resetAnswers();
        selectedTextbookId = null;
    }

    async function loadExam(): Promise<void> {
        if (!selectedTextbookId) {
            return;
        }
        resetAnswers();
        await exam.requestExam(6, selectedTextbookId);
    }

    function submit(): void {
        if (!allAnswered || examState.isGrading) {
            return;
        }

        const answers: ExamAnswer[] = questions.map((question) =>
            question.kind === "multiple_choice"
                ? {question_id: question.id, selected_index: choiceAnswers[question.id] ?? null}
                : {question_id: question.id, text: textAnswers[question.id] ?? ""},
        );

        void exam.submitExam(answers);
    }

    function retake(): void {
        resetAnswers();
        void loadExam();
    }

    // ── Exam history ───────────────────────────────────────────────────────────
    async function loadAttempts(): Promise<void> {
        const courseId = params?.id;
        if (!courseId) {
            return;
        }
        try {
            attempts = await fetchExamAttempts(courseId);
        } catch {
            // History is non-critical; leave whatever we had.
        }
    }

    /** Mark that we're now in a taking/result view (leave the textbook selection). */
    function enterFromHistory(attempt: ExamAttemptDto): void {
        resetAnswers();
        // Use the saved exam's textbook so "New exam" regenerates on the right one;
        // fall back to a sentinel so the selection screen is left either way.
        selectedTextbookId = attempt.textbook ?? "history";
    }

    /** Re-take a saved exam with the same questions. */
    function repeatAttempt(attempt: ExamAttemptDto): void {
        enterFromHistory(attempt);
        void exam.resumeExam(attempt.id);
    }

    /** Review a saved exam's last graded result without re-taking it. */
    function reviewAttempt(attempt: ExamAttemptDto): void {
        if (!attempt.result) {
            return;
        }
        enterFromHistory(attempt);
        exam.showResult(attempt.result);
    }

    async function onDeleteAttempt(attempt: ExamAttemptDto): Promise<void> {
        if (!confirm(`Delete the exam “${attempt.title}”? This cannot be undone.`)) {
            return;
        }
        deletingAttemptId = attempt.id;
        try {
            await deleteExamAttempt(attempt.id);
            attempts = attempts.filter((item) => item.id !== attempt.id);
        } catch (error) {
            textbooksError = error instanceof Error ? error.message : String(error);
        } finally {
            deletingAttemptId = null;
        }
    }

    function attemptScore(attempt: ExamAttemptDto): number {
        return attempt.max_points > 0 ? Math.round((attempt.total_points / attempt.max_points) * 100) : 0;
    }

    function formatDate(iso: string): string {
        const date = new Date(iso);
        return Number.isFinite(date.getTime()) ? date.toLocaleDateString() : "";
    }
</script>

<div class="exam">
    <header class="exam-top">
        <button type="button" class="content-btn" onclick={() => window.history.back()}>Back</button>
        {#if !selecting && !result && questions.length > 0 && !isBusy}
            <div class="progress-track" aria-hidden="true">
                <div class="progress-fill" style="width: {(answeredCount / questions.length) * 100}%"></div>
            </div>
            <span class="progress-count">{answeredCount}/{questions.length}</span>
        {/if}
    </header>

    {#if selecting}
        <section class="stage select-stage">
            <h1 class="course">{courseTitle}</h1>
            <p class="select-hint">Choose a textbook to be examined on. The exam is generated and graded by AI.</p>

            {#if textbooksLoading}
                <div class="status-card"><span class="loader" aria-hidden="true"></span><p>Loading textbooks...</p></div>
            {:else if textbooksError}
                <div class="status-card error-card" role="alert">
                    <p>{textbooksError}</p>
                    <button type="button" class="btn btn-primary" onclick={() => loadTextbooks()}>Retry</button>
                </div>
            {:else if textbooks.length === 0}
                <div class="status-card"><p>This course has no textbooks to be examined on yet.</p></div>
            {:else}
                <div class="textbook-list">
                    {#each textbooks as book (book.id)}
                        <button type="button" class="textbook-card" onclick={() => chooseTextbook(book.id)}>
                            <span class="textbook-icon" aria-hidden="true">🎓</span>
                            <span class="textbook-name">{book.name}</span>
                            {#if book.skills.length > 0}
                                <span class="textbook-skills">
                                    {#each book.skills as skill (skill.id)}
                                        <span class="textbook-skill">{skill.name}</span>
                                    {/each}
                                </span>
                            {:else}
                                <span class="textbook-skills empty">No skills yet</span>
                            {/if}
                        </button>
                    {/each}
                </div>
            {/if}

            {#if attempts.length > 0}
                <section class="history" aria-labelledby="exam-history-title">
                    <h2 id="exam-history-title" class="history-title">Your exams</h2>
                    <ul class="history-list">
                        {#each attempts as attempt (attempt.id)}
                            <li class="history-item">
                                <span class="hi-score" class:graded={attempt.result}>
                                    {attempt.result ? `${attemptScore(attempt)}%` : "—"}
                                </span>
                                <span class="hi-main">
                                    <span class="hi-title">{attempt.title}</span>
                                    <span class="hi-meta">{formatDate(attempt.updated_at)}</span>
                                </span>
                                <span class="hi-actions">
                                    {#if attempt.result}
                                        <button type="button" class="btn btn-xs btn-ghost" onclick={() => reviewAttempt(attempt)}>Review</button>
                                    {/if}
                                    <button type="button" class="btn btn-xs btn-primary" onclick={() => repeatAttempt(attempt)}>Repeat</button>
                                    <button
                                        type="button"
                                        class="btn btn-xs btn-ghost text-error"
                                        disabled={deletingAttemptId === attempt.id}
                                        aria-label={`Delete exam ${attempt.title}`}
                                        onclick={() => onDeleteAttempt(attempt)}
                                    >
                                        {#if deletingAttemptId === attempt.id}<span class="loading loading-spinner loading-xs"></span>{:else}✕{/if}
                                    </button>
                                </span>
                            </li>
                        {/each}
                    </ul>
                </section>
            {/if}
        </section>
    {:else if isBusy}
        <section class="stage status-stage" aria-live="polite">
            <h1 class="course">{courseTitle}</h1>
            <div class="status-card"><span class="loader" aria-hidden="true"></span><p>Generating exam...</p></div>
        </section>
    {:else if examState.errorMessage && !result}
        <section class="stage status-stage">
            <h1 class="course">{courseTitle}</h1>
            <div class="status-card error-card" role="alert">
                <p>{examState.errorMessage}</p>
                <button type="button" class="btn btn-primary" onclick={() => loadExam()}>Retry</button>
            </div>
        </section>
    {:else if result}
        <section class="stage result-stage">
            <h1 class="course">{courseTitle}</h1>
            {#if selectedTextbookName}<span class="progress-pill">{selectedTextbookName}</span>{/if}

            <div class="score-ring">
                <span class="score-pct">{scorePercent}%</span>
                <span class="score-pts">{result.total_points}/{result.max_points} pts</span>
            </div>

            {#if result.points_awarded > 0}
                <div class="reward" role="status">
                    <span class="reward-points">+{result.points_awarded} points</span>
                    {#if result.skills_advanced.length > 0}
                        <span class="reward-skills">
                            Skill progress:
                            {#each result.skills_advanced as skill (skill)}<span class="reward-skill">{skill}</span>{/each}
                        </span>
                    {/if}
                </div>
            {:else}
                <p class="reward-none">No new points — beat your previous best score to earn more.</p>
            {/if}

            <div class="feedback-list">
                {#each result.results as item, index (item.question_id)}
                    <article class="feedback-card" class:correct={item.correct === true} class:wrong={item.correct === false}>
                        <header class="feedback-head">
                            <span class="feedback-q">Q{index + 1}</span>
                            <span class="feedback-points">{item.awarded_points}/{item.max_points} pts</span>
                        </header>
                        <p class="feedback-prompt">{item.prompt}</p>
                        <p class="feedback-answer"><strong>Your answer:</strong> {item.your_answer || "—"}</p>
                        {#if item.correct_answer}
                            <p class="feedback-expected"><strong>Expected:</strong> {item.correct_answer}</p>
                        {/if}
                        {#if item.feedback}
                            <p class="feedback-text">{item.feedback}</p>
                        {/if}
                    </article>
                {/each}
            </div>

            <div class="result-actions">
                <button type="button" class="btn btn-primary" onclick={retake}>New exam</button>
                <button type="button" class="btn btn-outline" onclick={backToSelection}>Change textbook</button>
                <button type="button" class="btn btn-ghost" onclick={() => push("/")}>Back to Dashboard</button>
            </div>
        </section>
    {:else if questions.length > 0}
        <section class="stage exam-stage">
            <h1 class="course">{courseTitle}</h1>
            {#if selectedTextbookName}<span class="progress-pill">{selectedTextbookName}</span>{/if}

            <div class="question-list">
                {#each questions as question, index (question.id)}
                    <article class="question-card">
                        <header class="question-head">
                            <span class="question-num">Q{index + 1}</span>
                            <span class="question-kind">{question.kind === "multiple_choice" ? "Multiple choice" : "Free text"}</span>
                            <span class="question-points">{question.max_points} pts</span>
                        </header>
                        <p class="question-prompt">{question.prompt}</p>

                        {#if question.kind === "multiple_choice"}
                            <div class="options">
                                {#each question.options as option, optionIndex (option)}
                                    <label class="option" class:selected={choiceAnswers[question.id] === optionIndex}>
                                        <input
                                            type="radio"
                                            name={`q-${question.id}`}
                                            value={optionIndex}
                                            checked={choiceAnswers[question.id] === optionIndex}
                                            onchange={() => (choiceAnswers = {...choiceAnswers, [question.id]: optionIndex})}
                                        />
                                        <span class="option-letter">{letters[optionIndex]}</span>
                                        <span class="option-text">{option}</span>
                                    </label>
                                {/each}
                            </div>
                        {:else}
                            <textarea
                                class="free-text"
                                rows="4"
                                placeholder="Type your answer..."
                                value={textAnswers[question.id] ?? ""}
                                oninput={(event) =>
                                    (textAnswers = {...textAnswers, [question.id]: event.currentTarget.value})}
                            ></textarea>
                        {/if}
                    </article>
                {/each}
            </div>

            <div class="submit-bar">
                {#if examState.errorMessage}<p class="error">{examState.errorMessage}</p>{/if}
                <button
                    type="button"
                    class="btn btn-primary btn-lg"
                    onclick={submit}
                    disabled={!allAnswered || examState.isGrading}
                >
                    {#if examState.isGrading}<span class="loading loading-spinner loading-sm"></span> Grading...{:else}Submit for AI grading{/if}
                </button>
                {#if !allAnswered}<p class="submit-hint">Answer all {questions.length} questions to submit ({answeredCount}/{questions.length}).</p>{/if}
            </div>
        </section>
    {:else}
        <section class="stage status-stage">
            <h1 class="course">{courseTitle}</h1>
            <div class="status-card">
                <p>No exam questions were generated.</p>
                <button type="button" class="btn btn-primary" onclick={() => loadExam()}>Generate exam</button>
            </div>
        </section>
    {/if}
</div>

<style>
    .exam {
        flex: 1;
        min-height: 0;
        display: flex;
        flex-direction: column;
        width: 100%;
        background:
            radial-gradient(120% 70% at 50% 0%, color-mix(in oklab, var(--color-primary) 8%, transparent), transparent 55%),
            var(--color-base-200);
    }

    .exam-top {
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

    .progress-count {
        flex: 0 0 auto;
        font-size: 0.8rem;
        font-weight: 700;
        color: color-mix(in oklab, var(--color-base-content) 65%, transparent);
    }

    /* The stage scrolls so long exams and result lists stay reachable. */
    .stage {
        flex: 1;
        min-height: 0;
        overflow-y: auto;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 1.25rem;
        width: 90%;
        max-width: 56rem;
        margin: 0 auto;
        padding: 1rem 0 3rem;
    }

    .select-stage,
    .exam-stage,
    .result-stage {
        justify-content: flex-start;
        padding-top: 1.5rem;
    }

    .status-stage {
        justify-content: center;
        max-width: 34rem;
    }

    .course {
        font-size: clamp(1.3rem, 2.4vw, 1.9rem);
        font-weight: 700;
        text-align: center;
        color: var(--color-base-content);
        text-shadow: 0 0 20px color-mix(in oklab, var(--color-primary) 40%, transparent);
    }

    .select-hint {
        font-size: 1.05rem;
        font-weight: 600;
        text-align: center;
        color: color-mix(in oklab, var(--color-base-content) 80%, transparent);
        margin: 0;
    }

    .textbook-list {
        width: 100%;
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(15rem, 1fr));
        grid-auto-rows: 1fr;
        gap: 1.1rem;
        margin-top: 0.5rem;
    }

    .textbook-card {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        gap: 0.85rem;
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

    .textbook-card:hover {
        transform: translateY(-3px);
        background: color-mix(in oklab, var(--color-primary) 8%, transparent);
        border-color: color-mix(in oklab, var(--color-primary) 55%, transparent);
        box-shadow: 0 10px 24px color-mix(in oklab, var(--color-primary) 22%, transparent);
    }

    .textbook-icon {
        flex: 0 0 auto;
        display: grid;
        place-items: center;
        width: 2.6rem;
        height: 2.6rem;
        border-radius: 0.8rem;
        font-size: 1.4rem;
        background: color-mix(in oklab, var(--color-primary) 16%, transparent);
        border: 1px solid color-mix(in oklab, var(--color-primary) 28%, transparent);
    }

    .textbook-name {
        font-size: 1.1rem;
        font-weight: 700;
        line-height: 1.3;
        overflow-wrap: anywhere;
    }

    .textbook-skills {
        margin-top: auto;
        display: flex;
        flex-wrap: wrap;
        gap: 0.35rem;
    }

    .textbook-skills.empty {
        font-size: 0.72rem;
        color: color-mix(in oklab, var(--color-base-content) 45%, transparent);
    }

    .textbook-skill {
        font-size: 0.72rem;
        font-weight: 600;
        padding: 0.12rem 0.6rem;
        border-radius: 999px;
        color: var(--color-primary);
        background: color-mix(in oklab, var(--color-primary) 14%, transparent);
        border: 1px solid color-mix(in oklab, var(--color-primary) 30%, transparent);
    }

    .status-card {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 1rem;
        width: 100%;
        padding: 2rem;
        border-radius: 0.75rem;
        text-align: center;
        color: var(--color-base-content);
        background: color-mix(in oklab, var(--color-base-100) 82%, transparent);
        border: 1px solid color-mix(in oklab, var(--color-primary) 24%, transparent);
    }

    .error-card {
        border-color: color-mix(in oklab, var(--color-error) 45%, transparent);
    }

    .loader {
        width: 2.25rem;
        height: 2.25rem;
        border-radius: 999px;
        border: 0.25rem solid color-mix(in oklab, var(--color-primary) 25%, transparent);
        border-top-color: var(--color-primary);
        animation: spin 0.8s linear infinite;
    }

    .progress-pill {
        padding: 0.3rem 1rem;
        border-radius: 999px;
        font-weight: 700;
        color: var(--color-primary);
        background: color-mix(in oklab, var(--color-primary) 16%, transparent);
        border: 1px solid color-mix(in oklab, var(--color-primary) 35%, transparent);
    }

    /* Question list (taking the exam) */
    .question-list {
        width: 100%;
        display: flex;
        flex-direction: column;
        gap: 1.25rem;
    }

    .question-card {
        width: 100%;
        padding: 1.5rem;
        border-radius: 1rem;
        background: color-mix(in oklab, var(--color-base-100) 85%, transparent);
        border: 1px solid color-mix(in oklab, var(--color-base-content) 12%, transparent);
        box-shadow: 0 4px 14px color-mix(in oklab, var(--color-base-content) 8%, transparent);
    }

    .question-head {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 0.6rem;
    }

    .question-num {
        font-weight: 800;
        color: var(--color-primary);
    }

    .question-kind {
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        padding: 0.1rem 0.55rem;
        border-radius: 999px;
        color: color-mix(in oklab, var(--color-base-content) 70%, transparent);
        background: color-mix(in oklab, var(--color-base-content) 8%, transparent);
    }

    .question-points {
        margin-left: auto;
        font-size: 0.8rem;
        font-weight: 700;
        color: color-mix(in oklab, var(--color-base-content) 60%, transparent);
    }

    .question-prompt {
        font-size: 1.15rem;
        font-weight: 600;
        line-height: 1.5;
        color: var(--color-base-content);
        margin-bottom: 1rem;
    }

    .options {
        display: flex;
        flex-direction: column;
        gap: 0.6rem;
    }

    .option {
        display: flex;
        align-items: center;
        gap: 0.85rem;
        padding: 0.85rem 1rem;
        border-radius: 0.75rem;
        cursor: pointer;
        border: 1px solid color-mix(in oklab, var(--color-base-content) 14%, transparent);
        background: color-mix(in oklab, var(--color-base-100) 60%, transparent);
        transition: border-color 0.15s ease, background 0.15s ease;
    }

    .option:hover {
        border-color: color-mix(in oklab, var(--color-primary) 45%, transparent);
    }

    .option.selected {
        border-color: var(--color-primary);
        background: color-mix(in oklab, var(--color-primary) 12%, transparent);
    }

    .option input {
        accent-color: var(--color-primary);
    }

    .option-letter {
        display: grid;
        place-items: center;
        width: 1.8rem;
        height: 1.8rem;
        flex: 0 0 auto;
        border-radius: 0.5rem;
        font-weight: 700;
        color: var(--color-primary);
        background: color-mix(in oklab, var(--color-primary) 14%, transparent);
    }

    .option-text {
        flex: 1 1 auto;
        line-height: 1.4;
    }

    .free-text {
        width: 100%;
        padding: 0.85rem 1rem;
        border-radius: 0.75rem;
        border: 1px solid color-mix(in oklab, var(--color-base-content) 18%, transparent);
        background: var(--color-base-100);
        color: var(--color-base-content);
        font: inherit;
        line-height: 1.5;
        resize: vertical;
    }

    .free-text:focus {
        outline: 2px solid var(--color-primary);
        outline-offset: 1px;
    }

    .submit-bar {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.5rem;
        width: 100%;
        margin-top: 0.5rem;
    }

    .submit-hint {
        font-size: 0.85rem;
        color: color-mix(in oklab, var(--color-base-content) 60%, transparent);
    }

    /* Result screen */
    .score-ring {
        display: grid;
        place-items: center;
        gap: 0.1rem;
        width: 9.5rem;
        height: 9.5rem;
        border-radius: 999px;
        color: var(--color-base-content);
        background: color-mix(in oklab, var(--color-primary) 14%, transparent);
        border: 4px solid color-mix(in oklab, var(--color-primary) 55%, transparent);
        box-shadow: 0 0 28px color-mix(in oklab, var(--color-primary) 35%, transparent);
    }

    .score-pct {
        font-size: 2.2rem;
        font-weight: 800;
    }

    .score-pts {
        font-size: 0.85rem;
        font-weight: 600;
        color: color-mix(in oklab, var(--color-base-content) 65%, transparent);
    }

    .reward {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.5rem;
    }

    .reward-points {
        font-size: 1.3rem;
        font-weight: 800;
        padding: 0.25rem 1rem;
        border-radius: 999px;
        color: var(--color-primary-content);
        background: var(--color-primary);
        box-shadow: 0 0 16px color-mix(in oklab, var(--color-primary) 50%, transparent);
    }

    .reward-skills {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        justify-content: center;
        gap: 0.4rem;
        font-size: 0.9rem;
        color: color-mix(in oklab, var(--color-base-content) 70%, transparent);
    }

    .reward-skill {
        font-size: 0.8rem;
        font-weight: 600;
        padding: 0.1rem 0.6rem;
        border-radius: 999px;
        color: var(--color-primary);
        background: color-mix(in oklab, var(--color-primary) 14%, transparent);
        border: 1px solid color-mix(in oklab, var(--color-primary) 30%, transparent);
    }

    .reward-none {
        font-size: 0.9rem;
        color: color-mix(in oklab, var(--color-base-content) 60%, transparent);
    }

    .feedback-list {
        width: 100%;
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }

    .feedback-card {
        width: 100%;
        padding: 1.25rem;
        border-radius: 1rem;
        background: color-mix(in oklab, var(--color-base-100) 85%, transparent);
        border: 1px solid color-mix(in oklab, var(--color-base-content) 12%, transparent);
        border-left: 4px solid color-mix(in oklab, var(--color-base-content) 25%, transparent);
    }

    .feedback-card.correct {
        border-left-color: var(--color-success);
    }

    .feedback-card.wrong {
        border-left-color: var(--color-error);
    }

    .feedback-head {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 0.4rem;
    }

    .feedback-q {
        font-weight: 800;
        color: var(--color-primary);
    }

    .feedback-points {
        font-size: 0.85rem;
        font-weight: 700;
        color: color-mix(in oklab, var(--color-base-content) 65%, transparent);
    }

    .feedback-prompt {
        font-weight: 600;
        line-height: 1.5;
        margin-bottom: 0.5rem;
    }

    .feedback-answer,
    .feedback-expected {
        font-size: 0.9rem;
        line-height: 1.5;
        color: color-mix(in oklab, var(--color-base-content) 80%, transparent);
        margin-bottom: 0.25rem;
    }

    .feedback-text {
        margin-top: 0.5rem;
        font-size: 0.9rem;
        line-height: 1.55;
        padding: 0.5rem 0.85rem;
        border-radius: 0.6rem;
        background: color-mix(in oklab, var(--color-primary) 8%, transparent);
        color: var(--color-base-content);
    }

    .result-actions {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 1rem;
        margin-top: 0.5rem;
    }

    .error {
        color: var(--color-error, crimson);
        font-size: 0.9rem;
    }

    @keyframes spin {
        to {
            transform: rotate(360deg);
        }
    }

    /* --- Exam history --------------------------------------------------------- */
    .history {
        width: 100%;
        margin-top: 1rem;
        display: flex;
        flex-direction: column;
        gap: 0.6rem;
    }

    .history-title {
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: color-mix(in oklab, var(--color-base-content) 55%, transparent);
    }

    .history-list {
        list-style: none;
        margin: 0;
        padding: 0;
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }

    .history-item {
        display: flex;
        align-items: center;
        gap: 0.85rem;
        padding: 0.6rem 0.85rem;
        border-radius: 0.75rem;
        background: color-mix(in oklab, var(--color-base-100) 82%, transparent);
        border: 1px solid color-mix(in oklab, var(--color-base-content) 12%, transparent);
    }

    .hi-score {
        flex: 0 0 auto;
        display: grid;
        place-items: center;
        min-width: 2.8rem;
        height: 2.8rem;
        padding: 0 0.4rem;
        border-radius: 0.6rem;
        font-weight: 800;
        font-size: 0.85rem;
        color: color-mix(in oklab, var(--color-base-content) 55%, transparent);
        background: color-mix(in oklab, var(--color-base-content) 8%, transparent);
    }

    .hi-score.graded {
        color: var(--color-primary);
        background: color-mix(in oklab, var(--color-primary) 14%, transparent);
        border: 1px solid color-mix(in oklab, var(--color-primary) 30%, transparent);
    }

    .hi-main {
        flex: 1 1 auto;
        min-width: 0;
        display: flex;
        flex-direction: column;
        gap: 0.1rem;
    }

    .hi-title {
        font-weight: 700;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        color: var(--color-base-content);
    }

    .hi-meta {
        font-size: 0.75rem;
        color: color-mix(in oklab, var(--color-base-content) 55%, transparent);
    }

    .hi-actions {
        flex: 0 0 auto;
        display: flex;
        align-items: center;
        gap: 0.25rem;
    }

    @media (max-width: 34rem) {
        .history-item {
            flex-wrap: wrap;
        }
        .hi-actions {
            width: 100%;
            justify-content: flex-end;
        }
    }
</style>
