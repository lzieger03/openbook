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

The reader shows one page at a time (single-page view). Learners move between pages
with the Previous/Next controls or by picking an entry from the table of contents,
so only the current page scrolls — never the whole textbook at once.
-->
<script lang="ts">
    import {onMount} from "svelte";
    import {push} from "svelte-spa-router";
    import {dashboardStore} from "../../stores/dashboard.store.js";
    import type {DashboardState} from "../../stores/dashboard.store.js";
    import {loadCourseContent} from "../../data/course-content.js";
    import type {ContentMaterialView} from "../../data/course-content.js";
    import {completeCourse, fetchLearningState, markPageCompleted, recordPageOpened} from "../../api/learning.js";

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

    // Index of the entry currently shown in the single-page reader.
    let currentIndex = $state(0);

    // Learning progress for this course.
    let completedPageIds = $state<string[]>([]);
    let courseCompleted = $state(false);
    let completingCourse = $state(false);
    let markBusyPageId = $state<string | null>(null);
    let actionError = $state("");
    // Non-reactive: avoids re-sending "page opened" for the same page.
    let lastOpenedPageId: string | null = null;

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
        actionError = "";
        completedPageIds = [];
        courseCompleted = false;
        lastOpenedPageId = null;
        currentIndex = 0;

        void loadLearningState(courseId);

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

    // A single reading entry shown one-at-a-time: either a material's downloads or one page.
    type DownloadsEntry = {
        kind: "downloads";
        id: string;
        materialId: string;
        materialTitle: string;
        documents: ContentMaterialView["documents"];
    };
    type PageEntry = {
        kind: "page";
        id: string;
        materialId: string;
        materialTitle: string;
        page: ContentMaterialView["pages"][number];
    };
    type ReadingEntry = DownloadsEntry | PageEntry;

    // Flatten materials into reading order: each material's downloads first, then its pages.
    const entries = $derived.by<ReadingEntry[]>(() => {
        const list: ReadingEntry[] = [];
        for (const material of materials) {
            if (material.documents.length > 0) {
                list.push({
                    kind: "downloads",
                    id: `downloads-${material.id}`,
                    materialId: material.id,
                    materialTitle: material.title,
                    documents: material.documents,
                });
            }
            for (const page of material.pages) {
                list.push({
                    kind: "page",
                    id: page.id,
                    materialId: material.id,
                    materialTitle: material.title,
                    page,
                });
            }
        }
        return list;
    });

    const currentEntry = $derived(entries[currentIndex] ?? null);
    const isFirstEntry = $derived(currentIndex <= 0);
    const isLastEntry = $derived(currentIndex >= entries.length - 1);
    // Only count actual pages for the "Page X of Y" indicator (downloads are not pages).
    const pageEntries = $derived(entries.filter((entry) => entry.kind === "page"));
    const currentPageNumber = $derived(
        currentEntry?.kind === "page"
            ? pageEntries.findIndex((entry) => entry.id === currentEntry.id) + 1
            : 0,
    );

    // Keep the selected index within bounds when the content changes.
    $effect(() => {
        if (entries.length === 0) {
            return;
        }
        if (currentIndex > entries.length - 1) {
            currentIndex = entries.length - 1;
        }
    });

    // Record a page as opened whenever it becomes the current entry.
    $effect(() => {
        const entry = currentEntry;
        if (entry?.kind === "page") {
            openPage(entry.id);
        }
    });

    /** Load the learner's saved progress (completed pages + course completion). */
    async function loadLearningState(courseId: string): Promise<void> {
        try {
            const learningState = await fetchLearningState(courseId);
            completedPageIds = learningState?.completed_pages ?? [];
            courseCompleted = learningState?.is_completed ?? false;
        } catch {
            // Progress is non-critical; fall back to "nothing completed yet".
        }
    }

    function isPageCompleted(pageId: string): boolean {
        return completedPageIds.includes(pageId);
    }

    /** Report that the learner opened a page (best-effort, deduplicated). */
    function openPage(pageId: string): void {
        const courseId = params?.id;
        if (!courseId || !pageId || pageId === lastOpenedPageId) {
            return;
        }
        lastOpenedPageId = pageId;
        void recordPageOpened(courseId, pageId).catch(() => {});
    }

    /** Mark a single page as completed and reflect the server's updated list. */
    async function onMarkComplete(pageId: string): Promise<void> {
        const courseId = params?.id;
        if (!courseId) {
            return;
        }
        markBusyPageId = pageId;
        actionError = "";
        try {
            const learningState = await markPageCompleted(courseId, pageId);
            completedPageIds = learningState.completed_pages ?? completedPageIds;
        } catch (error) {
            actionError = error instanceof Error ? error.message : String(error);
        } finally {
            markBusyPageId = null;
        }
    }

    /** Complete the course (awards points server-side) and refresh the dashboard. */
    async function onCompleteCourse(): Promise<void> {
        const courseId = params?.id;
        if (!courseId || courseCompleted) {
            return;
        }
        completingCourse = true;
        actionError = "";
        try {
            const learningState = await completeCourse(courseId);
            courseCompleted = learningState.is_completed;
            // Completion grants course points/level, so reload the dashboard data.
            dashboardStore.refresh();
        } catch (error) {
            actionError = error instanceof Error ? error.message : String(error);
        } finally {
            completingCourse = false;
        }
    }

    /** Show the entry at the given index, scrolling the reader back to the top. */
    function goToIndex(index: number): void {
        if (index < 0 || index > entries.length - 1) {
            return;
        }
        currentIndex = index;
        document.querySelector(".article-scroll")?.scrollTo({top: 0, behavior: "auto"});
    }

    /** Show a specific entry (page or downloads) by its id. */
    function goToEntry(entryId: string): void {
        const index = entries.findIndex((entry) => entry.id === entryId);
        if (index !== -1) {
            goToIndex(index);
        }
    }

    function goToPrevious(): void {
        goToIndex(currentIndex - 1);
    }

    function goToNext(): void {
        goToIndex(currentIndex + 1);
    }

    /** Turn a page title into a safe file name. */
    function safeFileName(title: string): string {
        const base = title.trim().replace(/[\\/:*?"<>|]+/g, "_").replace(/\s+/g, " ").slice(0, 100);
        return (base || "page") + ".html";
    }

    /** Wrap one page's content as an HTML section (heading + body). */
    function pageSectionHtml(page: PageEntry["page"]): string {
        // For HTML pages the html is the authored markup; for MD/TEXT it is rendered HTML.
        const body = page.format === "HTML" ? page.html : `<div class="prose">${page.html}</div>`;
        return `<section>\n<h1>${escapeHtml(page.title)}</h1>\n${body}\n</section>`;
    }

    /** Wrap section HTML in a complete, downloadable HTML document. */
    function buildHtmlDocument(title: string, bodyHtml: string): Blob {
        const document_ =
            "<!DOCTYPE html>\n" +
            '<html lang="en">\n<head>\n<meta charset="utf-8">\n' +
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n' +
            `<title>${escapeHtml(title)}</title>\n` +
            "<style>body{font-family:system-ui,sans-serif;line-height:1.7;max-width:48rem;margin:2rem auto;padding:0 1rem;}" +
            "section{margin-bottom:3rem;}" +
            "pre{background:#f3f3f3;padding:1rem;border-radius:.5rem;overflow:auto;}</style>\n" +
            `</head>\n<body>\n${bodyHtml}\n</body>\n</html>\n`;
        return new Blob([document_], {type: "text/html;charset=utf-8"});
    }

    /** Trigger a browser download for the given blob and file name. */
    function triggerDownload(blob: Blob, fileName: string): void {
        const url = URL.createObjectURL(blob);
        const anchor = document.createElement("a");
        anchor.href = url;
        anchor.download = fileName;
        document.body.appendChild(anchor);
        anchor.click();
        anchor.remove();
        URL.revokeObjectURL(url);
    }

    /** Download the current page as a standalone HTML file the learner can keep. */
    function downloadPage(page: PageEntry["page"]): void {
        triggerDownload(buildHtmlDocument(page.title, pageSectionHtml(page)), safeFileName(page.title));
    }

    /** Download the whole textbook (every page, in reading order) as one HTML file. */
    function downloadTextbook(): void {
        const sections = entries
            .filter((entry): entry is PageEntry => entry.kind === "page")
            .map((entry) => pageSectionHtml(entry.page))
            .join("\n");
        triggerDownload(buildHtmlDocument(courseTitle, sections), safeFileName(courseTitle));
    }

    /** Minimal HTML-escaping for values injected into the downloaded document. */
    function escapeHtml(value: string): string {
        return value
            .replaceAll("&", "&amp;")
            .replaceAll("<", "&lt;")
            .replaceAll(">", "&gt;")
            .replaceAll('"', "&quot;");
    }
</script>

<!-- Download icon: a circle with a downward arrow (reused by all download buttons). -->
{#snippet downloadIcon()}
    <svg
        class="download-icon"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"
        stroke-linejoin="round"
        aria-hidden="true"
    >
        <circle cx="12" cy="12" r="9" />
        <path d="M12 7.5v7" />
        <path d="m8.5 11 3.5 3.5 3.5-3.5" />
    </svg>
{/snippet}

<div class="content-screen">
    <aside class="toc">
        <button type="button" class="back" onclick={() => push(`/chat/${params?.id ?? ""}`)}>← Back to chat</button>

        <p class="toc-label">Contents</p>
        <nav class="toc-nav" aria-label="Table of contents">
            {#if hasContent}
                {#each materials as material (material.id)}
                    {#if material.pages.length > 0 || material.documents.length > 0}
                        <p class="toc-group">{material.title}</p>
                        {#if material.documents.length > 0}
                            <button
                                type="button"
                                class="toc-link"
                                class:active={currentEntry?.id === `downloads-${material.id}`}
                                onclick={() => goToEntry(`downloads-${material.id}`)}
                            >
                                <span class="toc-link-text">⬇ Downloads</span>
                            </button>
                        {/if}
                        {#each material.pages as page (page.id)}
                            <button
                                type="button"
                                class="toc-link"
                                class:active={currentEntry?.id === page.id}
                                onclick={() => goToEntry(page.id)}
                            >
                                <span class="toc-link-text">{page.title}</span>
                                {#if isPageCompleted(page.id)}<span class="toc-check" aria-label="completed">✓</span>{/if}
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
        <!-- Scrollable reading area: only this region scrolls, the pager stays put. -->
        <div class="article-scroll">
            <header class="article-head">
                <div class="article-head-text">
                    <p class="eyebrow">Course content</p>
                    <h1 class="article-title">{courseTitle}</h1>
                </div>
                {#if hasContent && pageEntries.length > 0}
                    <button type="button" class="download-btn textbook-download" onclick={downloadTextbook}>
                        {@render downloadIcon()}
                        <span>Download textbook</span>
                    </button>
                {/if}
            </header>

            {#if contentLoading}
                <p class="muted">Loading course content…</p>
            {:else if contentError}
                <p class="error">{contentError}</p>
            {:else if hasContent && currentEntry}
                <!-- Single-page reader: only the current entry is shown. -->
                {#if currentEntry.kind === "downloads"}
                    <section class="block downloads">
                        <h2>{currentEntry.materialTitle} — Downloads</h2>
                        <div class="download-list">
                            {#each currentEntry.documents as document (document.id)}
                                <a class="download-link" href={document.downloadUrl} download>
                                    <span>{document.title}</span>
                                    {#if document.fileName}
                                        <small>{document.fileName}</small>
                                    {/if}
                                </a>
                            {/each}
                        </div>
                    </section>
                {:else}
                    <section class="block">
                        <div class="page-head">
                            <h2>{currentEntry.page.title}</h2>
                            <div class="page-actions">
                                <button
                                    type="button"
                                    class="download-btn"
                                    onclick={() => downloadPage(currentEntry.page)}
                                >
                                    {@render downloadIcon()}
                                    <span>Download</span>
                                </button>
                                {#if isPageCompleted(currentEntry.page.id)}
                                    <span class="done-badge">✓ Completed</span>
                                {:else}
                                    <button
                                        type="button"
                                        class="btn btn-sm btn-ghost mark-btn"
                                        onclick={() => onMarkComplete(currentEntry.page.id)}
                                        disabled={markBusyPageId === currentEntry.page.id}
                                    >
                                        {#if markBusyPageId === currentEntry.page.id}<span class="loading loading-spinner loading-xs"></span>{/if}
                                        Mark complete
                                    </button>
                                {/if}
                            </div>
                        </div>
                        {#if currentEntry.page.format === "HTML"}
                            <iframe class="html-frame" title={currentEntry.page.title} sandbox="" srcdoc={currentEntry.page.html}></iframe>
                        {:else}
                            <!-- eslint-disable-next-line svelte/no-at-html-tags -->
                            <div class="prose">{@html currentEntry.page.html}</div>
                        {/if}
                    </section>
                {/if}

                {#if actionError}
                    <p class="error">{actionError}</p>
                {/if}
            {:else if hasContent}
                <p class="muted">Select a page from the contents to start reading.</p>
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
        </div>

        {#if !contentLoading && !contentError && hasContent && currentEntry}
            <!-- Reader navigation: always pinned to the bottom of the reading area. -->
            <nav class="pager" aria-label="Page navigation">
                <button type="button" class="btn btn-ghost" onclick={goToPrevious} disabled={isFirstEntry}>
                    ← Previous
                </button>

                {#if currentPageNumber > 0}
                    <span class="pager-status">Page {currentPageNumber} of {pageEntries.length}</span>
                {/if}

                {#if isLastEntry}
                    {#if courseCompleted}
                        <span class="done-note">🎉 Completed</span>
                    {:else}
                        <button type="button" class="btn btn-primary" onclick={onCompleteCourse} disabled={completingCourse}>
                            {#if completingCourse}<span class="loading loading-spinner loading-sm"></span>{/if}
                            Complete course
                        </button>
                    {/if}
                {:else}
                    <button type="button" class="btn btn-primary" onclick={goToNext}>
                        Next →
                    </button>
                {/if}
            </nav>
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
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 0.5rem;
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

    /* The page currently shown in the reader. */
    .toc-link.active {
        background: color-mix(in oklab, var(--color-primary) 22%, transparent);
        color: var(--color-base-content);
        font-weight: 600;
    }

    .toc-link-text {
        min-width: 0;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }

    .toc-check {
        flex: 0 0 auto;
        color: var(--color-success);
        font-weight: 700;
    }

    /* Flex column: a scrollable reading area on top, the pager fixed at the bottom. */
    .article {
        min-height: 0;
        display: flex;
        flex-direction: column;
    }

    .article-scroll {
        flex: 1;
        min-height: 0;
        overflow-y: auto;
        padding: 2.5rem 0;
    }

    /* Content text spans ~90% of the content view. */
    .article-scroll > * {
        width: 90%;
        margin-left: auto;
        margin-right: auto;
    }

    .article-head {
        display: flex;
        align-items: flex-end;
        justify-content: space-between;
        gap: 1rem;
        margin-bottom: 2rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid color-mix(in oklab, var(--color-base-content) 12%, transparent);
    }

    .article-head-text {
        min-width: 0;
    }

    .textbook-download {
        flex: 0 0 auto;
    }

    /* Outlined pill that clearly reads as a button, with the download icon. */
    .download-btn {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.4rem 0.85rem;
        border-radius: 999px;
        border: 1px solid color-mix(in oklab, var(--color-primary) 45%, transparent);
        background: color-mix(in oklab, var(--color-primary) 8%, transparent);
        color: var(--color-primary);
        font-size: 0.85rem;
        font-weight: 600;
        line-height: 1;
        cursor: pointer;
        transition:
            background 0.15s ease,
            border-color 0.15s ease,
            transform 0.05s ease;
    }

    .download-btn:hover {
        background: color-mix(in oklab, var(--color-primary) 18%, transparent);
        border-color: var(--color-primary);
    }

    .download-btn:active {
        transform: translateY(1px);
    }

    .download-btn:focus-visible {
        outline: 2px solid var(--color-primary);
        outline-offset: 2px;
    }

    .download-icon {
        width: 1.05rem;
        height: 1.05rem;
        flex: 0 0 auto;
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

    /* Page heading row: title on the left, the mark-complete control on the right. */
    .page-head {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
        margin-bottom: 0.6rem;
    }

    .page-head h2 {
        margin-bottom: 0;
    }

    /* Right-aligned controls for the current page (download + mark complete). */
    .page-actions {
        flex: 0 0 auto;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .mark-btn {
        flex: 0 0 auto;
    }

    .done-badge {
        flex: 0 0 auto;
        font-size: 0.8rem;
        font-weight: 700;
        padding: 0.2rem 0.6rem;
        border-radius: 999px;
        color: var(--color-success);
        background: color-mix(in oklab, var(--color-success) 15%, transparent);
        border: 1px solid color-mix(in oklab, var(--color-success) 35%, transparent);
    }

    /* Reader navigation bar: fixed as the last row of the reading area, so it
       always sits flush at the bottom regardless of how short the page is. */
    .pager {
        flex: 0 0 auto;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
        /* Pad the sides so its contents line up with the 90% page text column. */
        padding: 1rem 5%;
        border-top: 1px solid color-mix(in oklab, var(--color-base-content) 12%, transparent);
        background: transparent;
    }

    .pager-status {
        font-size: 0.85rem;
        font-weight: 600;
        color: color-mix(in oklab, var(--color-base-content) 65%, transparent);
    }

    .done-note {
        font-size: 1.1rem;
        font-weight: 700;
        color: var(--color-success);
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
