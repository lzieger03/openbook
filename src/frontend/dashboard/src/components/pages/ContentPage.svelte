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
Wiki-style course content page: a table of contents on the left and a readable
article on the right.

Note: the demo courses have no authored content yet (description is empty,
text_format = Markdown), so the sections below are sample placeholders. TODO:
load and render the real course material (Markdown) from the content API.
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
        const unsubscribe = dashboardStore.subscribe((value) => {
            state = value;
        });

        if (state.courses.length === 0) {
            dashboardStore.refresh();
        }

        return unsubscribe;
    });

    const courseTitle = $derived(
        state.courses.find((course) => course.id === params?.id)?.name ?? "Course",
    );

    const sections = [
        {id: "overview", title: "Overview"},
        {id: "getting-started", title: "Getting started"},
        {id: "key-concepts", title: "Key concepts"},
        {id: "example", title: "Example"},
        {id: "summary", title: "Summary"},
    ];

    function scrollTo(id: string): void {
        document.getElementById(id)?.scrollIntoView({behavior: "smooth", block: "start"});
    }
</script>

<div class="content-screen">
    <aside class="toc">
        <button type="button" class="back" onclick={() => push(`/chat/${params?.id ?? ""}`)}>← Back to chat</button>

        <p class="toc-label">On this page</p>
        <nav class="toc-nav" aria-label="Table of contents">
            {#each sections as section (section.id)}
                <button type="button" class="toc-link" onclick={() => scrollTo(section.id)}>
                    {section.title}
                </button>
            {/each}
        </nav>
    </aside>

    <main class="article">
        <header class="article-head">
            <p class="eyebrow">Course content</p>
            <h1 class="article-title">{courseTitle}</h1>
            <p class="placeholder-note">📝 Sample content — the authored course material will appear here.</p>
        </header>

        <section id="overview" class="block">
            <h2>Overview</h2>
            <p>
                Welcome to <strong>{courseTitle}</strong>. This page collects the course material in a
                readable, wiki-style format so you can browse concepts, examples and summaries at your own pace.
            </p>
        </section>

        <section id="getting-started" class="block">
            <h2>Getting started</h2>
            <p>Work through the sections in order. Each concept builds on the previous one.</p>
            <div class="callout">
                💡 Tip: open the AI tutor (the chat icon) any time you want a concept explained differently.
            </div>
        </section>

        <section id="key-concepts" class="block">
            <h2>Key concepts</h2>
            <ul>
                <li>The fundamentals and core vocabulary of {courseTitle}.</li>
                <li>How the pieces fit together in practice.</li>
                <li>Common mistakes and how to avoid them.</li>
            </ul>
        </section>

        <section id="example" class="block">
            <h2>Example</h2>
            <p>A minimal example you can adapt:</p>
            <pre class="code"><code>&lt;!DOCTYPE html&gt;
&lt;html&gt;
  &lt;head&gt;&lt;title&gt;{courseTitle}&lt;/title&gt;&lt;/head&gt;
  &lt;body&gt;Hello, learner!&lt;/body&gt;
&lt;/html&gt;</code></pre>
        </section>

        <section id="summary" class="block">
            <h2>Summary</h2>
            <p>
                You now have a map of {courseTitle}. Test yourself with the quiz, or ask the tutor to go deeper
                on any section.
            </p>
            <div class="actions">
                <button type="button" class="btn btn-primary" onclick={() => push(`/quiz/${params?.id ?? ""}`)}>
                    Take the quiz
                </button>
                <button type="button" class="btn btn-ghost" onclick={() => push(`/chat/${params?.id ?? ""}`)}>
                    Ask the tutor
                </button>
            </div>
        </section>
    </main>
</div>

<style>
    .content-screen {
        flex: 1;
        min-height: 0;
        display: grid;
        grid-template-columns: 15rem minmax(0, 1fr);
        width: 100%;
    }

    .toc {
        display: flex;
        flex-direction: column;
        gap: 1rem;
        padding: 1.5rem 1rem;
        border-right: 1px solid color-mix(in oklab, var(--color-base-content) 10%, transparent);
        background: color-mix(in oklab, var(--color-base-100) 60%, transparent);
    }

    .back {
        align-self: flex-start;
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

    .toc-label {
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: color-mix(in oklab, var(--color-base-content) 55%, transparent);
    }

    .toc-nav {
        display: flex;
        flex-direction: column;
        gap: 0.15rem;
    }

    .toc-link {
        text-align: left;
        padding: 0.4rem 0.6rem;
        border-radius: 0.5rem;
        border: none;
        background: transparent;
        color: color-mix(in oklab, var(--color-base-content) 75%, transparent);
        cursor: pointer;
    }

    .toc-link:hover {
        background: color-mix(in oklab, var(--color-primary) 14%, transparent);
        color: var(--color-base-content);
    }

    .article {
        min-height: 0;
        overflow-y: auto;
        padding: 2.5rem 0;
    }

    /* Content text spans ~90% of the content view. */
    .article > * {
        width: 90%;
        margin-left: auto;
        margin-right: auto;
    }

    .article-head {
        margin-bottom: 2rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid color-mix(in oklab, var(--color-base-content) 12%, transparent);
    }

    .eyebrow {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: var(--color-primary);
    }

    .article-title {
        font-size: clamp(2rem, 4vw, 2.8rem);
        font-weight: 800;
        color: var(--color-base-content);
        text-shadow: 0 0 22px color-mix(in oklab, var(--color-primary) 30%, transparent);
    }

    .placeholder-note {
        margin-top: 0.5rem;
        font-size: 0.85rem;
        color: color-mix(in oklab, var(--color-base-content) 60%, transparent);
    }

    .block {
        margin-bottom: 2.25rem;
        line-height: 1.7;
        color: color-mix(in oklab, var(--color-base-content) 90%, transparent);
    }

    .block h2 {
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 0.6rem;
        color: var(--color-base-content);
    }

    .block ul {
        margin: 0.5rem 0 0 1.25rem;
        display: flex;
        flex-direction: column;
        gap: 0.35rem;
    }

    .callout {
        margin-top: 0.75rem;
        padding: 0.9rem 1.1rem;
        border-radius: 0.75rem;
        background: color-mix(in oklab, var(--color-primary) 12%, transparent);
        border-left: 3px solid var(--color-primary);
    }

    .code {
        margin-top: 0.75rem;
        padding: 1rem 1.25rem;
        border-radius: 0.75rem;
        overflow-x: auto;
        font-family: ui-monospace, "SF Mono", Menlo, monospace;
        font-size: 0.9rem;
        color: var(--color-base-content);
        background: color-mix(in oklab, var(--color-base-content) 8%, transparent);
        border: 1px solid color-mix(in oklab, var(--color-base-content) 12%, transparent);
    }

    .actions {
        display: flex;
        gap: 0.75rem;
        margin-top: 1rem;
    }

    @media (max-width: 48rem) {
        .content-screen {
            grid-template-columns: 1fr;
        }

        .toc {
            display: none;
        }
    }
</style>
