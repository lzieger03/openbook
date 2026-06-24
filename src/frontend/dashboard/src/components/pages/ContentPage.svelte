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
Wiki-style course content page: a table of contents on the left and the readable
course material on the right. The material is the content authored by teachers in
the /teacher area (course materials → page ranges → textbook pages); it is loaded
and rendered via the content data layer. When a course has no authored content yet,
a friendly placeholder is shown instead.
-->
<script lang="ts">
    import {onMount} from "svelte";
    import {push} from "svelte-spa-router";
    import {dashboardStore} from "../../stores/dashboard.store.js";
    import type {DashboardState} from "../../stores/dashboard.store.js";
    import {loadCourseContent} from "../../data/course-content.js";
    import type {ContentMaterialView} from "../../data/course-content.js";

    let {params}: {params?: {id?: string}} = $props();

    let state = $state<DashboardState>({
        isLoading: true,
        errorMessage: "",
        user: null,
        stats: null,
        skills: [],
        courses: [],
    });

    let materials = $state<ContentMaterialView[]>([]);
    let contentLoading = $state(true);
    let contentError = $state("");

    onMount(() => {
        const unsubscribe = dashboardStore.subscribe((value) => {
            state = value;
        });

        if (state.courses.length === 0) {
            dashboardStore.refresh();
        }

        return unsubscribe;
    });

    // Reload the authored content whenever the course in the route changes.
    $effect(() => {
        const courseId = params?.id;

        if (!courseId) {
            materials = [];
            contentLoading = false;
            return;
        }

        contentLoading = true;
        contentError = "";

        loadCourseContent(courseId)
            .then((result) => {
                materials = result;
            })
            .catch((error: unknown) => {
                contentError = error instanceof Error ? error.message : String(error);
            })
            .finally(() => {
                contentLoading = false;
            });
    });

    const courseTitle = $derived(
        state.courses.find((course) => course.id === params?.id)?.name ?? "Course",
    );

    const hasContent = $derived(
        materials.some((material) => material.pages.length > 0 || material.documents.length > 0),
    );

    /** A stable DOM/anchor id for a page section. */
    function anchor(pageId: string): string {
        return `page-${pageId}`;
    }

    function scrollTo(id: string): void {
        document.getElementById(id)?.scrollIntoView({behavior: "smooth", block: "start"});
    }
</script>

<div class="content-screen">
    <aside class="toc">
        <button type="button" class="back" onclick={() => push(`/chat/${params?.id ?? ""}`)}>← Back to chat</button>

        <p class="toc-label">On this page</p>
        <nav class="toc-nav" aria-label="Table of contents">
            {#if hasContent}
                {#each materials as material (material.id)}
                    {#if material.pages.length > 0}
                        <p class="toc-group">{material.title}</p>
                        {#each material.pages as page (page.id)}
                            <button type="button" class="toc-link" onclick={() => scrollTo(anchor(page.id))}>
                                {page.title}
                            </button>
                        {/each}
                    {/if}
                {/each}
            {:else}
                <p class="muted">No sections yet.</p>
            {/if}
        </nav>
    </aside>

    <main class="article">
        <header class="article-head">
            <p class="eyebrow">Course content</p>
            <h1 class="article-title">{courseTitle}</h1>
        </header>

        {#if contentLoading}
            <p class="muted">Loading course content…</p>
        {:else if contentError}
            <p class="error">{contentError}</p>
        {:else if hasContent}
            {#each materials as material (material.id)}
                {#if material.documents.length > 0}
                    <section class="block downloads">
                        <h2>{material.title}</h2>
                        <div class="download-list">
                            {#each material.documents as document (document.id)}
                                <a class="download-link" href={document.downloadUrl} download>
                                    <span>{document.title}</span>
                                    {#if document.fileName}
                                        <small>{document.fileName}</small>
                                    {/if}
                                </a>
                            {/each}
                        </div>
                    </section>
                {/if}

                {#each material.pages as page (page.id)}
                    <section id={anchor(page.id)} class="block">
                        <h2>{page.title}</h2>
                        {#if page.format === "HTML"}
                            <iframe class="html-frame" title={page.title} sandbox="" srcdoc={page.html}></iframe>
                        {:else}
                            <!-- eslint-disable-next-line svelte/no-at-html-tags -->
                            <div class="prose">{@html page.html}</div>
                        {/if}
                    </section>
                {/each}
            {/each}
        {:else}
            <section class="block">
                <p class="placeholder-note">
                    📝 No content has been added to this course yet. Once your teacher publishes course
                    material in the teacher area, it will appear here.
                </p>
                <div class="actions">
                    <button type="button" class="btn btn-ghost" onclick={() => push(`/chat/${params?.id ?? ""}`)}>
                        Ask the tutor
                    </button>
                </div>
            </section>
        {/if}
    </main>
</div>

<style>
    .content-screen {
        flex: 1;
        min-height: 0;
        overflow: hidden;
        display: grid;
        grid-template-columns: 15rem minmax(0, 1fr);
        grid-template-rows: minmax(0, 1fr);
        width: 100%;
    }

    /* Sidebar stays put; it never scrolls. */
    .toc {
        min-height: 0;
        overflow: hidden;
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
        min-height: 0;
        overflow-y: auto;
    }

    .toc-group {
        margin-top: 0.6rem;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: color-mix(in oklab, var(--color-base-content) 70%, transparent);
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

    .downloads {
        padding-bottom: 1rem;
        border-bottom: 1px solid color-mix(in oklab, var(--color-base-content) 10%, transparent);
    }

    .download-list {
        display: flex;
        flex-wrap: wrap;
        gap: 0.75rem;
    }

    .download-link {
        display: inline-flex;
        flex-direction: column;
        gap: 0.15rem;
        max-width: 20rem;
        padding: 0.65rem 0.85rem;
        border: 1px solid color-mix(in oklab, var(--color-primary) 35%, transparent);
        border-radius: 0.5rem;
        color: var(--color-primary);
        text-decoration: none;
        background: color-mix(in oklab, var(--color-primary) 8%, transparent);
    }

    .download-link:hover {
        background: color-mix(in oklab, var(--color-primary) 14%, transparent);
    }

    .download-link small {
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        color: color-mix(in oklab, var(--color-base-content) 60%, transparent);
    }

    .error {
        color: var(--color-error, crimson);
    }

    .muted {
        color: color-mix(in oklab, var(--color-base-content) 60%, transparent);
        font-size: 0.9rem;
    }

    /* Rendered Markdown / plain-text content. Styling targets the injected HTML. */
    .prose :global(h1),
    .prose :global(h2),
    .prose :global(h3) {
        font-weight: 700;
        margin: 1rem 0 0.5rem;
    }

    .prose :global(h1) {
        font-size: 1.6rem;
    }

    .prose :global(h2) {
        font-size: 1.3rem;
    }

    .prose :global(h3) {
        font-size: 1.1rem;
    }

    .prose :global(p) {
        margin: 0.5rem 0;
    }

    .prose :global(ul),
    .prose :global(ol) {
        margin: 0.5rem 0 0.5rem 1.5rem;
    }

    .prose :global(li) {
        margin: 0.2rem 0;
    }

    .prose :global(a) {
        color: var(--color-primary);
        text-decoration: underline;
    }

    .prose :global(pre),
    .prose :global(code) {
        font-family: ui-monospace, "SF Mono", Menlo, monospace;
        font-size: 0.9rem;
    }

    .prose :global(pre) {
        margin-top: 0.75rem;
        padding: 1rem 1.25rem;
        border-radius: 0.75rem;
        overflow-x: auto;
        background: color-mix(in oklab, var(--color-base-content) 8%, transparent);
        border: 1px solid color-mix(in oklab, var(--color-base-content) 12%, transparent);
    }

    .prose :global(blockquote) {
        margin: 0.75rem 0;
        padding: 0.5rem 1rem;
        border-left: 3px solid var(--color-primary);
        background: color-mix(in oklab, var(--color-primary) 8%, transparent);
    }

    .html-frame {
        width: 100%;
        min-height: 24rem;
        border: 1px solid color-mix(in oklab, var(--color-base-content) 12%, transparent);
        border-radius: 0.5rem;
        background: var(--color-base-100);
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
