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
Content tab: add textbooks to a course and write their pages. Designed to be
straightforward — one input adds a textbook; clicking a textbook opens a simple
two-pane editor (a list of its pages on the left, the page editor on the right).
Attaching an existing textbook is a secondary, collapsed option.
-->
<script lang="ts">
    import MarkdownIt from "markdown-it";

    import {loadMaterials} from "../../data/teacher.js";
    import type {CourseMaterialView} from "../../data/teacher.js";
    import {
        addMaterial,
        createSkill,
        createTextbook,
        createTextbookPage,
        deleteMaterial,
        deleteTextbookPage,
        fetchSkills,
        fetchTextbookPages,
        fetchTextbooks,
        moveMaterial,
        updateTextbook,
        updateTextbookPage,
        uploadTextbookFile,
    } from "../../api/content.js";
    import type {SkillDto, SourceContent, TextbookDto, TextbookPageDto} from "../../api/content.js";
    import {slugify} from "../../api/courses.js";
    import type {TextFormat} from "../../api/courses.js";

    let {courseId, courseGroupId}: {courseId: string; courseGroupId: string} = $props();

    let materials = $state<CourseMaterialView[]>([]);
    let textbooks = $state<TextbookDto[]>([]);
    let isLoading = $state(true);
    let error = $state("");
    let message = $state("");

    // Add-textbook form (just a name — slug/format/description use sensible defaults).
    let newTextbookName = $state("");
    let creatingTextbook = $state(false);

    // Upload-script: turn one whole document into a textbook with one page per chapter.
    let uploadingScript = $state(false);

    // Attach-existing form (secondary option).
    let attachTextbookId = $state("");
    let attaching = $state(false);

    // Inline textbook renaming (one at a time, keyed by course-material id).
    let renamingId = $state<string | null>(null);
    let renameValue = $state("");
    let renameSaving = $state(false);

    // Per-textbook page editing (one textbook expanded at a time).
    let expandedId = $state<string | null>(null);
    let pagesLoading = $state(false);
    let pages = $state<TextbookPageDto[]>([]);

    // Page editing.
    let selectedPageId = $state("");
    let pageName = $state("");
    let pageTextFormat = $state<TextFormat>("MD");
    let editorSource = $state("");
    let editorFilename = $state("");
    let editorMode = $state<"edit" | "preview">("edit");
    let editorSaving = $state(false);
    let editorMessage = $state("");
    let newPageName = $state("");
    let creatingPage = $state(false);
    let deletingPageId = $state<string | null>(null);

    // Skill tagging: the global catalog plus the ids selected for the current page.
    let skillCatalog = $state<SkillDto[]>([]);
    let pageSkillIds = $state<string[]>([]);
    let skillSearch = $state("");
    let creatingSkill = $state(false);

    const selectedSkills = $derived(skillCatalog.filter((skill) => pageSkillIds.includes(skill.id)));

    // Unselected skills matching the search term (capped so the dropdown stays small).
    const skillMatches = $derived.by(() => {
        const term = skillSearch.trim().toLowerCase();
        if (!term) {
            return [];
        }
        return skillCatalog
            .filter((skill) => !pageSkillIds.includes(skill.id) && skill.name.toLowerCase().includes(term))
            .slice(0, 8);
    });

    // Offer to create a skill when the search term matches no existing skill by name.
    const canCreateSkill = $derived.by(() => {
        const term = skillSearch.trim();
        if (!term) {
            return false;
        }
        return !skillCatalog.some((skill) => skill.name.toLowerCase() === term.toLowerCase());
    });

    const markdownRenderer = new MarkdownIt({
        breaks: true,
        html: false,
        linkify: true,
        typographer: true,
    });

    const selectedPage = $derived(pages.find((page) => page.id === selectedPageId) ?? null);

    // Textbooks not yet part of this course, offered under "attach existing".
    const attachableTextbooks = $derived(
        textbooks.filter((textbook) => !materials.some((material) => material.textbookId === textbook.id)),
    );

    async function load(): Promise<void> {
        isLoading = true;
        error = "";

        try {
            [materials, textbooks, skillCatalog] = await Promise.all([
                loadMaterials(courseId),
                fetchTextbooks(),
                fetchSkills(),
            ]);
        } catch (e) {
            error = e instanceof Error ? e.message : String(e);
        } finally {
            isLoading = false;
        }
    }

    $effect(() => {
        void courseId;
        load();
    });

    function nextPosition(): number {
        return materials.reduce((max, m) => Math.max(max, m.position), 0) + 1;
    }

    /** Create a brand-new textbook from just a name and open it for editing. */
    async function onCreateTextbook(): Promise<void> {
        const name = newTextbookName.trim();
        if (!name) {
            return;
        }
        if (!courseGroupId) {
            error = "This course has no library group. Choose one in Overview first.";
            return;
        }

        creatingTextbook = true;
        error = "";
        message = "";

        try {
            const textbook = await createTextbook({
                name,
                slug: slugify(name),
                description: "",
                text_format: "MD",
                group: courseGroupId,
            });
            await addMaterial(courseId, textbook.id, nextPosition());

            textbooks = [...textbooks, textbook].sort((a, b) => a.name.localeCompare(b.name));
            materials = await loadMaterials(courseId);
            newTextbookName = "";
            message = `Added “${textbook.name}”. Now add some pages.`;

            const material = materials.find((candidate) => candidate.textbookId === textbook.id);
            if (material) {
                await toggleExpand(material);
            }
        } catch (e) {
            error = e instanceof Error ? e.message : String(e);
        } finally {
            creatingTextbook = false;
        }
    }

    /**
     * Upload a whole script and let the server split it into chapters, creating a
     * textbook with one page per chapter. The new textbook is then opened so the
     * teacher can review and edit the generated chapters.
     */
    async function onUploadScript(event: Event): Promise<void> {
        const input = event.currentTarget as HTMLInputElement;
        const file = input.files?.[0];
        if (!file) {
            return;
        }
        if (!courseGroupId) {
            error = "This course has no library group. Choose one in Overview first.";
            input.value = "";
            return;
        }

        uploadingScript = true;
        error = "";
        message = "";

        try {
            const result = await uploadTextbookFile(courseId, file);
            materials = await loadMaterials(courseId);
            textbooks = await fetchTextbooks();

            const created = materials.find((candidate) => candidate.textbookId === result.textbook);
            if (created) {
                await toggleExpand(created);
            }

            const count = result.pages_created ?? 0;
            message = `Imported “${file.name}” — created ${count} ${count === 1 ? "chapter" : "chapters"}.`;
        } catch (e) {
            error = e instanceof Error ? e.message : String(e);
        } finally {
            uploadingScript = false;
            input.value = "";
        }
    }

    /** Attach an existing textbook to this course. */
    async function onAttachTextbook(): Promise<void> {
        if (!attachTextbookId) {
            return;
        }

        attaching = true;
        error = "";
        message = "";

        try {
            await addMaterial(courseId, attachTextbookId, nextPosition());
            await load();
            message = "Textbook attached.";
            attachTextbookId = "";
        } catch (e) {
            error = e instanceof Error ? e.message : String(e);
        } finally {
            attaching = false;
        }
    }

    /** Begin renaming a textbook (prefills the input with its current name). */
    function startRename(material: CourseMaterialView): void {
        renamingId = material.id;
        renameValue = material.textbookName;
    }

    function cancelRename(): void {
        renamingId = null;
        renameValue = "";
    }

    /** Persist a renamed textbook and refresh the affected lists. */
    async function saveRename(material: CourseMaterialView): Promise<void> {
        const name = renameValue.trim();
        if (!name || name === material.textbookName) {
            cancelRename();
            return;
        }

        renameSaving = true;
        error = "";
        message = "";

        try {
            await updateTextbook(material.textbookId, {name});
            materials = await loadMaterials(courseId);
            textbooks = (await fetchTextbooks()).sort((a, b) => a.name.localeCompare(b.name));
            message = `Renamed to “${name}”.`;
            cancelRename();
        } catch (e) {
            error = e instanceof Error ? e.message : String(e);
        } finally {
            renameSaving = false;
        }
    }

    async function onRemoveTextbook(material: CourseMaterialView): Promise<void> {
        if (!confirm(`Remove “${material.textbookName}” from this course?`)) {
            return;
        }

        error = "";
        try {
            await deleteMaterial(material.id);
            if (expandedId === material.id) {
                expandedId = null;
            }
            await load();
        } catch (e) {
            error = e instanceof Error ? e.message : String(e);
        }
    }

    /** Move a textbook one step up or down to reorder the reading list. */
    async function move(index: number, direction: -1 | 1): Promise<void> {
        const material = materials[index];
        const target = materials[index + direction];

        if (!material || !target) {
            return;
        }

        error = "";
        try {
            await moveMaterial(material.id, direction === -1 ? "up" : "down");
            await load();
        } catch (e) {
            error = e instanceof Error ? e.message : String(e);
        }
    }

    async function toggleExpand(material: CourseMaterialView): Promise<void> {
        if (expandedId === material.id) {
            expandedId = null;
            return;
        }

        expandedId = material.id;
        pagesLoading = true;
        resetEditor();

        try {
            pages = await fetchTextbookPages(material.textbookId);
            if (pages.length > 0 && pages[0]) {
                selectPage(pages[0].id);
            }
        } catch (e) {
            error = e instanceof Error ? e.message : String(e);
        } finally {
            pagesLoading = false;
        }
    }

    function resetEditor(): void {
        selectedPageId = "";
        pageName = "";
        pageTextFormat = "MD";
        editorSource = "";
        editorFilename = "";
        editorMode = "edit";
        editorMessage = "";
        newPageName = "";
        pageSkillIds = [];
        skillSearch = "";
    }

    /** Toggle a skill on the page currently being edited. */
    function togglePageSkill(skillId: string): void {
        pageSkillIds = pageSkillIds.includes(skillId)
            ? pageSkillIds.filter((id) => id !== skillId)
            : [...pageSkillIds, skillId];
    }

    /** Attach a skill from the search results and reset the search field. */
    function addPageSkill(skillId: string): void {
        if (!pageSkillIds.includes(skillId)) {
            pageSkillIds = [...pageSkillIds, skillId];
        }
        skillSearch = "";
    }

    /** Create a new skill from the current search term, then attach it to the page. */
    async function createAndAddSkill(): Promise<void> {
        const name = skillSearch.trim();
        if (!name || creatingSkill) {
            return;
        }

        creatingSkill = true;
        error = "";

        try {
            const skill = await createSkill(name);
            skillCatalog = [...skillCatalog, skill].sort((a, b) => a.name.localeCompare(b.name));
            addPageSkill(skill.id);
        } catch (e) {
            error = e instanceof Error ? e.message : String(e);
        } finally {
            creatingSkill = false;
        }
    }

    function isSourceContent(content: TextbookPageDto["content"]): content is SourceContent {
        return (
            typeof content === "object" &&
            content !== null &&
            "type" in content &&
            (content as {type?: unknown}).type === "source" &&
            "source" in content
        );
    }

    function readPageSource(page: TextbookPageDto): string {
        if (isSourceContent(page.content)) {
            return page.content.source;
        }

        if (Object.keys(page.content).length === 0) {
            return "";
        }

        return JSON.stringify(page.content, null, 4);
    }

    function selectPage(pageId: string): void {
        const page = pages.find((candidate) => candidate.id === pageId);
        if (!page) {
            resetEditor();
            return;
        }

        selectedPageId = page.id;
        pageName = page.name;
        pageTextFormat = page.text_format ?? "MD";
        editorSource = readPageSource(page);
        editorFilename = isSourceContent(page.content) ? (page.content.filename ?? "") : "";
        pageSkillIds = [...(page.skills ?? [])];
        skillSearch = "";
        editorMode = "edit";
        editorMessage = "";
    }

    function nextPagePosition(): number {
        return pages.reduce((max, page) => Math.max(max, page.position), 0) + 1;
    }

    function makeContent(filename = editorFilename): SourceContent {
        return {
            type: "source",
            format: pageTextFormat,
            source: editorSource,
            ...(filename ? {filename} : {}),
        };
    }

    async function onCreatePage(material: CourseMaterialView): Promise<void> {
        const name = newPageName.trim();
        if (!name) {
            return;
        }

        creatingPage = true;
        error = "";
        editorMessage = "";

        try {
            const created = await createTextbookPage({
                textbook: material.textbookId,
                position: nextPagePosition(),
                name,
                text_format: "MD",
                content: {type: "source", format: "MD", source: ""},
                skills: [],
            });
            pages = await fetchTextbookPages(material.textbookId);
            selectPage(created.id);
            newPageName = "";
            editorMessage = "Page created — write its content below.";
        } catch (e) {
            error = e instanceof Error ? e.message : String(e);
        } finally {
            creatingPage = false;
        }
    }

    /** Permanently delete a page from the textbook (with confirmation). */
    async function onDeletePage(material: CourseMaterialView, page: TextbookPageDto): Promise<void> {
        if (!confirm(`Delete the page “${page.name}”? This cannot be undone.`)) {
            return;
        }

        deletingPageId = page.id;
        error = "";
        editorMessage = "";

        try {
            await deleteTextbookPage(page.id);
            pages = await fetchTextbookPages(material.textbookId);

            // Keep a sensible selection: stay on the current page if it still exists,
            // otherwise fall back to the first remaining page (or clear the editor).
            if (page.id === selectedPageId) {
                if (pages.length > 0 && pages[0]) {
                    selectPage(pages[0].id);
                } else {
                    resetEditor();
                }
            }
        } catch (e) {
            error = e instanceof Error ? e.message : String(e);
        } finally {
            deletingPageId = null;
        }
    }

    async function onSavePage(): Promise<void> {
        if (!selectedPageId) {
            return;
        }
        if (!pageName.trim()) {
            error = "Page title is required.";
            return;
        }

        editorSaving = true;
        error = "";
        editorMessage = "";

        try {
            const updated = await updateTextbookPage(selectedPageId, {
                name: pageName.trim(),
                text_format: pageTextFormat,
                content: makeContent(),
                skills: pageSkillIds,
            });
            pages = pages.map((page) => (page.id === updated.id ? updated : page));
            selectPage(updated.id);
            editorMessage = "Saved.";
        } catch (e) {
            error = e instanceof Error ? e.message : String(e);
        } finally {
            editorSaving = false;
        }
    }

    function formatFromFilename(filename: string): TextFormat {
        const lower = filename.toLowerCase();
        if (lower.endsWith(".html") || lower.endsWith(".htm")) {
            return "HTML";
        }
        if (lower.endsWith(".txt")) {
            return "TEXT";
        }
        return "MD";
    }

    async function onFileSelected(event: Event): Promise<void> {
        const input = event.currentTarget as HTMLInputElement;
        const file = input.files?.[0];
        if (!file) {
            return;
        }

        editorFilename = file.name;
        pageTextFormat = formatFromFilename(file.name);
        if (!pageName.trim()) {
            pageName = file.name.replace(/\.[^.]+$/, "");
        }
        editorSource = await file.text();
        editorMessage = `Imported ${file.name}.`;
        input.value = "";
    }

    function escapeHtml(value: string): string {
        return value
            .replaceAll("&", "&amp;")
            .replaceAll("<", "&lt;")
            .replaceAll(">", "&gt;")
            .replaceAll('"', "&quot;");
    }

    const previewHtml = $derived(
        pageTextFormat === "HTML"
            ? editorSource
            : pageTextFormat === "TEXT"
              ? `<pre>${escapeHtml(editorSource)}</pre>`
              : markdownRenderer.render(editorSource),
    );
</script>

<div class="card bg-base-100 shadow-sm">
    <div class="card-body">
        <h2 class="card-title">Course content</h2>
        <p class="muted">Add textbooks and write their pages. Learners read them top to bottom.</p>

        {#if error}
            <div class="alert alert-error"><span>{error}</span></div>
        {/if}
        {#if message}
            <div class="alert alert-success"><span>{message}</span></div>
        {/if}

        <!-- Primary action: add a textbook with just a name. -->
        <div class="add-textbook">
            <input
                class="input input-bordered flex-1"
                type="text"
                bind:value={newTextbookName}
                placeholder="New textbook name, e.g. Chapter 1: HTML Basics"
                disabled={creatingTextbook}
                onkeydown={(event) => {
                    if (event.key === "Enter") {
                        event.preventDefault();
                        onCreateTextbook();
                    }
                }}
            />
            <button
                type="button"
                class="btn btn-primary"
                onclick={onCreateTextbook}
                disabled={creatingTextbook || !newTextbookName.trim() || !courseGroupId}
            >
                {#if creatingTextbook}<span class="loading loading-spinner loading-sm"></span>{/if}
                + Add textbook
            </button>
        </div>

        <!-- Power action: upload a whole script and auto-build a chapter per heading. -->
        <div class="upload-script">
            <label class="upload-script-btn" class:busy={uploadingScript}>
                <span class="upload-icon" aria-hidden="true">
                    {#if uploadingScript}
                        <span class="loading loading-spinner loading-sm"></span>
                    {:else}
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M12 15V4" />
                            <path d="m7.5 8.5 4.5-4.5 4.5 4.5" />
                            <path d="M5 15v3a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-3" />
                        </svg>
                    {/if}
                </span>
                <span class="upload-text">
                    <span class="upload-title">
                        {uploadingScript ? "Extracting chapters…" : "Upload a script"}
                    </span>
                    <span class="upload-sub">
                        Drops a whole document in and splits it into chapters automatically.
                    </span>
                </span>
                <input
                    class="sr-only"
                    type="file"
                    accept=".md,.markdown,.html,.htm,.txt,.pdf,text/markdown,text/html,text/plain,application/pdf"
                    disabled={uploadingScript || !courseGroupId}
                    onchange={onUploadScript}
                />
            </label>
            <p class="muted upload-hint">Supported formats: PDF, Markdown, HTML and plain text (.pdf, .md, .html, .txt).</p>
        </div>

        {#if attachableTextbooks.length > 0}
            <details class="attach">
                <summary>Or attach an existing textbook</summary>
                <div class="attach-row">
                    <select class="select select-bordered flex-1" bind:value={attachTextbookId}>
                        <option value="">Choose a textbook…</option>
                        {#each attachableTextbooks as textbook (textbook.id)}
                            <option value={textbook.id}>{textbook.name}</option>
                        {/each}
                    </select>
                    <button
                        type="button"
                        class="btn btn-ghost"
                        onclick={onAttachTextbook}
                        disabled={attaching || !attachTextbookId}
                    >
                        {#if attaching}<span class="loading loading-spinner loading-sm"></span>{/if}
                        Attach
                    </button>
                </div>
            </details>
        {/if}

        {#if isLoading}
            <div class="center-row"><span class="loading loading-spinner"></span></div>
        {:else if materials.length === 0}
            <div class="empty">
                <p class="empty-title">No content yet</p>
                <p class="muted">Type a name above and hit “Add textbook” to create your first one.</p>
            </div>
        {:else}
            <ol class="tb-list">
                {#each materials as material, index (material.id)}
                    {@const open = expandedId === material.id}
                    <li class="tb" class:open>
                        <div class="tb-head">
                            {#if renamingId === material.id}
                                <div class="tb-rename">
                                    <span class="tb-index">{index + 1}</span>
                                    <!-- svelte-ignore a11y_autofocus -->
                                    <input
                                        class="input input-bordered input-sm flex-1"
                                        type="text"
                                        bind:value={renameValue}
                                        autofocus
                                        disabled={renameSaving}
                                        onkeydown={(event) => {
                                            if (event.key === "Enter") {
                                                event.preventDefault();
                                                saveRename(material);
                                            } else if (event.key === "Escape") {
                                                cancelRename();
                                            }
                                        }}
                                    />
                                    <button
                                        type="button"
                                        class="btn btn-xs btn-primary"
                                        onclick={() => saveRename(material)}
                                        disabled={renameSaving || !renameValue.trim()}
                                    >
                                        {#if renameSaving}<span class="loading loading-spinner loading-xs"></span>{/if}
                                        Save
                                    </button>
                                    <button type="button" class="btn btn-xs btn-ghost" onclick={cancelRename} disabled={renameSaving}>Cancel</button>
                                </div>
                            {:else}
                                <button type="button" class="tb-main" onclick={() => toggleExpand(material)}>
                                    <span class="tb-index">{index + 1}</span>
                                    <span class="tb-name">{material.textbookName}</span>
                                    <span class="chev" aria-hidden="true">{open ? "▾" : "▸"}</span>
                                </button>

                                <span class="tb-actions">
                                    <button type="button" class="btn btn-xs btn-ghost" disabled={index === 0} onclick={() => move(index, -1)} aria-label="Move up">↑</button>
                                    <button type="button" class="btn btn-xs btn-ghost" disabled={index === materials.length - 1} onclick={() => move(index, 1)} aria-label="Move down">↓</button>
                                    <button type="button" class="btn btn-xs btn-ghost" onclick={() => startRename(material)} aria-label="Rename textbook">Rename</button>
                                    <button type="button" class="btn btn-xs btn-ghost text-error" onclick={() => onRemoveTextbook(material)} aria-label="Remove textbook">Remove</button>
                                </span>
                            {/if}
                        </div>

                        {#if open}
                            <div class="tb-body">
                                {#if pagesLoading}
                                    <div class="center-row"><span class="loading loading-spinner loading-sm"></span></div>
                                {:else}
                                    <div class="editor-layout">
                                        <!-- Left: page list + add page -->
                                        <aside class="page-list">
                                            <div class="page-list-title">Pages</div>
                                            {#if pages.length === 0}
                                                <p class="muted page-empty">No pages yet.</p>
                                            {:else}
                                                <ul class="pages">
                                                    {#each pages as page (page.id)}
                                                        <li class="page-row">
                                                            <button
                                                                type="button"
                                                                class="page-item"
                                                                class:active={page.id === selectedPageId}
                                                                onclick={() => selectPage(page.id)}
                                                            >
                                                                {page.name}
                                                            </button>
                                                            <button
                                                                type="button"
                                                                class="page-delete"
                                                                aria-label={`Delete page ${page.name}`}
                                                                title="Delete page"
                                                                disabled={deletingPageId === page.id}
                                                                onclick={() => onDeletePage(material, page)}
                                                            >
                                                                {#if deletingPageId === page.id}
                                                                    <span class="loading loading-spinner loading-xs"></span>
                                                                {:else}
                                                                    ✕
                                                                {/if}
                                                            </button>
                                                        </li>
                                                    {/each}
                                                </ul>
                                            {/if}

                                            <div class="add-page">
                                                <input
                                                    class="input input-bordered input-sm flex-1"
                                                    type="text"
                                                    bind:value={newPageName}
                                                    placeholder="New page title"
                                                    onkeydown={(event) => {
                                                        if (event.key === "Enter") {
                                                            event.preventDefault();
                                                            onCreatePage(material);
                                                        }
                                                    }}
                                                />
                                                <button
                                                    type="button"
                                                    class="btn btn-sm btn-primary"
                                                    onclick={() => onCreatePage(material)}
                                                    disabled={creatingPage || !newPageName.trim()}
                                                    aria-label="Add page"
                                                >
                                                    {#if creatingPage}<span class="loading loading-spinner loading-xs"></span>{:else}+{/if}
                                                </button>
                                            </div>
                                        </aside>

                                        <!-- Right: page editor -->
                                        <div class="editor">
                                            {#if !selectedPage}
                                                <div class="editor-placeholder">
                                                    <p class="muted">
                                                        {pages.length === 0
                                                            ? "Add your first page on the left to start writing."
                                                            : "Select a page on the left, or add a new one."}
                                                    </p>
                                                </div>
                                            {:else}
                                                {#if editorMessage}
                                                    <div class="alert alert-success alert-sm"><span>{editorMessage}</span></div>
                                                {/if}

                                                <div class="editor-row">
                                                    <label class="form-control flex-1">
                                                        <span class="label-text">Page title</span>
                                                        <input class="input input-bordered input-sm w-full" type="text" bind:value={pageName} />
                                                    </label>
                                                    <label class="form-control format-control">
                                                        <span class="label-text">Format</span>
                                                        <select class="select select-bordered select-sm" bind:value={pageTextFormat}>
                                                            <option value="MD">Markdown</option>
                                                            <option value="HTML">HTML</option>
                                                            <option value="TEXT">Plain text</option>
                                                        </select>
                                                    </label>
                                                </div>

                                                <div class="form-control w-full">
                                                    <span class="label-text">Skills trained by this page</span>

                                                    {#if selectedSkills.length > 0}
                                                        <div class="skill-tags">
                                                            {#each selectedSkills as skill (skill.id)}
                                                                <span class="skill-tag selected">
                                                                    {skill.name}
                                                                    <button
                                                                        type="button"
                                                                        class="skill-remove"
                                                                        aria-label={`Remove ${skill.name}`}
                                                                        onclick={() => togglePageSkill(skill.id)}
                                                                    >
                                                                        ×
                                                                    </button>
                                                                </span>
                                                            {/each}
                                                        </div>
                                                    {/if}

                                                    <input
                                                        class="input input-bordered input-sm w-full mt-2"
                                                        type="text"
                                                        bind:value={skillSearch}
                                                        placeholder="Search skills, or type a new name to create one…"
                                                    />

                                                    {#if skillSearch.trim()}
                                                        <div class="skill-results">
                                                            {#each skillMatches as skill (skill.id)}
                                                                <button type="button" class="skill-result" onclick={() => addPageSkill(skill.id)}>
                                                                    {skill.name}
                                                                </button>
                                                            {/each}

                                                            {#if canCreateSkill}
                                                                <button type="button" class="skill-result create" disabled={creatingSkill} onclick={createAndAddSkill}>
                                                                    {#if creatingSkill}<span class="loading loading-spinner loading-xs"></span>{/if}
                                                                    + Create “{skillSearch.trim()}”
                                                                </button>
                                                            {:else if skillMatches.length === 0}
                                                                <p class="muted skill-hint">No matching skills.</p>
                                                            {/if}
                                                        </div>
                                                    {/if}
                                                </div>

                                                <div class="editor-toolbar">
                                                    <div class="editor-tabs">
                                                        <button type="button" class="btn btn-sm" class:btn-primary={editorMode === "edit"} onclick={() => (editorMode = "edit")}>Write</button>
                                                        <button type="button" class="btn btn-sm" class:btn-primary={editorMode === "preview"} onclick={() => (editorMode = "preview")}>Preview</button>
                                                    </div>
                                                    <label class="btn btn-sm import-btn">
                                                        <span class="import-icon" aria-hidden="true">
                                                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                                                <path d="M12 15V4" />
                                                                <path d="m7.5 8.5 4.5-4.5 4.5 4.5" />
                                                                <path d="M5 15v3a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-3" />
                                                            </svg>
                                                        </span>
                                                        <span>Import file</span>
                                                        <input class="sr-only" type="file" accept=".md,.markdown,.html,.htm,.txt,text/markdown,text/html,text/plain" onchange={onFileSelected} />
                                                    </label>
                                                </div>

                                                {#if editorMode === "edit"}
                                                    <textarea
                                                        class="textarea textarea-bordered editor-source"
                                                        bind:value={editorSource}
                                                        placeholder="Write Markdown, HTML, or import a .md/.html/.txt file."
                                                    ></textarea>
                                                {:else if pageTextFormat === "HTML"}
                                                    <iframe class="preview-frame" title="HTML preview" sandbox="" srcdoc={previewHtml}></iframe>
                                                {:else}
                                                    <div class="preview-prose">{@html previewHtml}</div>
                                                {/if}

                                                <div class="editor-actions">
                                                    <span class="muted">{editorFilename ? `Imported from ${editorFilename}` : ""}</span>
                                                    <button type="button" class="btn btn-sm btn-primary" onclick={onSavePage} disabled={editorSaving}>
                                                        {#if editorSaving}<span class="loading loading-spinner loading-xs"></span>{/if}
                                                        Save page
                                                    </button>
                                                </div>
                                            {/if}
                                        </div>
                                    </div>
                                {/if}
                            </div>
                        {/if}
                    </li>
                {/each}
            </ol>
        {/if}
    </div>
</div>

<style>
    .muted {
        color: color-mix(in oklab, var(--color-base-content) 60%, transparent);
        font-size: 0.85rem;
    }

    /* --- Add textbook --------------------------------------------------- */

    .add-textbook {
        display: flex;
        gap: 0.5rem;
        margin: 0.75rem 0 0.25rem;
    }

    .attach {
        margin-bottom: 0.5rem;
    }

    .attach summary {
        cursor: pointer;
        font-size: 0.85rem;
        color: color-mix(in oklab, var(--color-base-content) 70%, transparent);
        padding: 0.25rem 0;
        width: fit-content;
    }

    .attach-row {
        display: flex;
        gap: 0.5rem;
        margin-top: 0.5rem;
    }

    /* --- Upload script -------------------------------------------------- */

    .upload-script {
        margin: 0.25rem 0 0.75rem;
    }

    /* A dashed "drop zone" style label that doubles as the file picker button. */
    .upload-script-btn {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        width: 100%;
        padding: 0.75rem 1rem;
        border: 1.5px dashed color-mix(in oklab, var(--color-primary) 45%, transparent);
        border-radius: 0.75rem;
        background: color-mix(in oklab, var(--color-primary) 7%, transparent);
        cursor: pointer;
        text-align: left;
        transition: background 0.18s ease, border-color 0.18s ease, transform 0.12s ease;
    }

    .upload-script-btn:hover {
        background: color-mix(in oklab, var(--color-primary) 13%, transparent);
        border-color: var(--color-primary);
        transform: translateY(-1px);
    }

    .upload-script-btn:focus-within {
        outline: 2px solid var(--color-primary);
        outline-offset: 2px;
    }

    .upload-script-btn.busy {
        cursor: progress;
        opacity: 0.85;
    }

    .upload-icon {
        flex: 0 0 auto;
        display: grid;
        place-items: center;
        width: 2.4rem;
        height: 2.4rem;
        border-radius: 0.6rem;
        color: var(--color-primary-content);
        background: var(--color-primary);
    }

    .upload-icon svg {
        width: 1.25rem;
        height: 1.25rem;
    }

    .upload-script-btn:hover .upload-icon svg {
        transform: translateY(-1px);
        transition: transform 0.18s ease;
    }

    .upload-text {
        display: flex;
        flex-direction: column;
        min-width: 0;
    }

    .upload-title {
        font-weight: 700;
        color: var(--color-primary);
    }

    .upload-sub {
        font-size: 0.85rem;
        color: color-mix(in oklab, var(--color-base-content) 65%, transparent);
    }

    .upload-hint {
        margin-top: 0.35rem;
    }

    .center-row {
        display: flex;
        justify-content: center;
        padding: 1.5rem 0;
    }

    .empty {
        text-align: center;
        padding: 2.5rem 1rem;
        border: 1px dashed color-mix(in oklab, var(--color-base-content) 18%, transparent);
        border-radius: 0.75rem;
        margin-top: 0.5rem;
    }

    .empty-title {
        font-weight: 700;
        margin-bottom: 0.25rem;
    }

    /* --- Textbook list -------------------------------------------------- */

    .tb-list {
        list-style: none;
        margin: 0.75rem 0 0;
        padding: 0;
        display: flex;
        flex-direction: column;
        gap: 0.6rem;
    }

    .tb {
        border: 1px solid color-mix(in oklab, var(--color-base-content) 12%, transparent);
        border-radius: 0.75rem;
        overflow: hidden;
    }

    .tb.open {
        border-color: color-mix(in oklab, var(--color-primary) 40%, transparent);
    }

    .tb-head {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 0.6rem 0.5rem 0.4rem;
    }

    /* The textbook title row is one big toggle button. */
    .tb-main {
        flex: 1 1 auto;
        min-width: 0;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 0.35rem 0.5rem;
        border-radius: 0.5rem;
        background: none;
        border: 0;
        cursor: pointer;
        text-align: left;
        transition: background 0.15s ease;
    }

    .tb-main:hover {
        background: color-mix(in oklab, var(--color-base-content) 6%, transparent);
    }

    .tb-index {
        flex: 0 0 auto;
        display: grid;
        place-items: center;
        width: 1.6rem;
        height: 1.6rem;
        border-radius: 999px;
        font-size: 0.8rem;
        font-weight: 700;
        background: color-mix(in oklab, var(--color-primary) 20%, transparent);
        color: var(--color-primary);
    }

    .tb-name {
        flex: 1 1 auto;
        min-width: 0;
        font-weight: 600;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .chev {
        flex: 0 0 auto;
        color: color-mix(in oklab, var(--color-base-content) 55%, transparent);
    }

    .tb-actions {
        flex: 0 0 auto;
        display: flex;
        gap: 0.15rem;
    }

    /* Inline rename row: index chip + text field + Save/Cancel, filling the head. */
    .tb-rename {
        flex: 1 1 auto;
        display: flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.1rem 0.25rem;
    }

    .tb-body {
        padding: 0 0.6rem 0.75rem;
        border-top: 1px solid color-mix(in oklab, var(--color-base-content) 10%, transparent);
    }

    /* --- Two-pane editor ------------------------------------------------ */

    .editor-layout {
        display: grid;
        grid-template-columns: minmax(11rem, 14rem) minmax(0, 1fr);
        gap: 1rem;
        margin-top: 0.75rem;
    }

    .page-list {
        display: flex;
        flex-direction: column;
        gap: 0.4rem;
    }

    .page-list-title {
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: color-mix(in oklab, var(--color-base-content) 55%, transparent);
    }

    .page-empty {
        margin: 0.25rem 0;
    }

    .pages {
        list-style: none;
        margin: 0;
        padding: 0;
        display: flex;
        flex-direction: column;
        gap: 0.2rem;
    }

    /* Each page row: the selectable label plus a delete button that appears on hover. */
    .page-row {
        display: flex;
        align-items: center;
        gap: 0.2rem;
    }

    .page-item {
        flex: 1 1 auto;
        min-width: 0;
        text-align: left;
        padding: 0.4rem 0.6rem;
        border-radius: 0.5rem;
        border: 1px solid transparent;
        background: none;
        cursor: pointer;
        font-size: 0.9rem;
        color: var(--color-base-content);
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        transition: background 0.15s ease, border-color 0.15s ease;
    }

    .page-item:hover {
        background: color-mix(in oklab, var(--color-base-content) 6%, transparent);
    }

    .page-item.active {
        background: color-mix(in oklab, var(--color-primary) 14%, transparent);
        border-color: color-mix(in oklab, var(--color-primary) 35%, transparent);
        font-weight: 600;
    }

    .page-delete {
        flex: 0 0 auto;
        display: grid;
        place-items: center;
        width: 1.6rem;
        height: 1.6rem;
        border-radius: 0.4rem;
        border: none;
        background: none;
        cursor: pointer;
        font-size: 0.8rem;
        line-height: 1;
        color: color-mix(in oklab, var(--color-base-content) 45%, transparent);
        opacity: 0;
        transition: opacity 0.15s ease, background 0.15s ease, color 0.15s ease;
    }

    /* Reveal the delete button when hovering the row, focusing it, or on the active page. */
    .page-row:hover .page-delete,
    .page-delete:focus-visible,
    .page-item.active + .page-delete {
        opacity: 1;
    }

    .page-delete:hover {
        color: var(--color-error);
        background: color-mix(in oklab, var(--color-error) 14%, transparent);
    }

    .page-delete:disabled {
        opacity: 1;
        cursor: not-allowed;
    }

    .add-page {
        display: flex;
        gap: 0.35rem;
        margin-top: 0.25rem;
    }

    .editor {
        min-width: 0;
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
    }

    .editor-placeholder {
        display: grid;
        place-items: center;
        min-height: 12rem;
        border: 1px dashed color-mix(in oklab, var(--color-base-content) 18%, transparent);
        border-radius: 0.5rem;
        padding: 1rem;
        text-align: center;
    }

    .editor-row {
        display: flex;
        gap: 0.75rem;
        align-items: flex-end;
    }

    .format-control {
        flex: 0 0 auto;
        width: 10rem;
    }

    .editor-toolbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 0.5rem;
    }

    .editor-tabs {
        display: flex;
        gap: 0.4rem;
    }

    /* Make the file import stand out as the quick way to fill a page: a soft
       primary chip that fills and lifts on hover. */
    .import-btn {
        gap: 0.5rem;
        font-weight: 600;
        color: var(--color-primary);
        border: 1px solid color-mix(in oklab, var(--color-primary) 40%, transparent);
        background: color-mix(in oklab, var(--color-primary) 10%, transparent);
        box-shadow: 0 1px 2px color-mix(in oklab, var(--color-base-content) 10%, transparent);
        transition:
            background 0.18s ease,
            border-color 0.18s ease,
            color 0.18s ease,
            transform 0.12s ease,
            box-shadow 0.18s ease;
    }

    .import-btn:hover {
        color: var(--color-primary-content);
        background: var(--color-primary);
        border-color: var(--color-primary);
        transform: translateY(-1px);
        box-shadow: 0 6px 16px color-mix(in oklab, var(--color-primary) 40%, transparent);
    }

    .import-btn:active {
        transform: translateY(0);
        box-shadow: 0 1px 2px color-mix(in oklab, var(--color-primary) 30%, transparent);
    }

    .import-btn:focus-within {
        outline: 2px solid var(--color-primary);
        outline-offset: 2px;
    }

    .import-icon {
        display: grid;
        place-items: center;
    }

    .import-icon svg {
        width: 1.05rem;
        height: 1.05rem;
    }

    /* Nudge the arrow upward on hover for a subtle "uploading" feel. */
    .import-btn:hover .import-icon svg {
        transform: translateY(-1px);
        transition: transform 0.18s ease;
    }

    .editor-source,
    .preview-frame,
    .preview-prose {
        width: 100%;
        min-height: 18rem;
    }

    .editor-source {
        font-family: ui-monospace, "SF Mono", Menlo, Monaco, Consolas, "Liberation Mono", monospace;
        line-height: 1.5;
        resize: vertical;
    }

    .preview-frame,
    .preview-prose {
        border: 1px solid color-mix(in oklab, var(--color-base-content) 12%, transparent);
        border-radius: 0.5rem;
        background: var(--color-base-100);
    }

    .preview-frame {
        display: block;
    }

    .preview-prose {
        padding: 1rem;
        overflow: auto;
        line-height: 1.6;
    }

    .preview-prose :global(h1),
    .preview-prose :global(h2),
    .preview-prose :global(h3) {
        margin-bottom: 0.5rem;
        font-weight: 700;
    }

    .preview-prose :global(h1) {
        font-size: 1.5rem;
    }

    .preview-prose :global(h2) {
        font-size: 1.25rem;
    }

    .editor-actions {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
    }

    /* --- Skills picker -------------------------------------------------- */

    .skill-tags {
        display: flex;
        flex-wrap: wrap;
        gap: 0.4rem;
        margin-top: 0.35rem;
    }

    .skill-tag {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        font-size: 0.8rem;
        padding: 0.2rem 0.7rem;
        border-radius: 999px;
        color: var(--color-base-content);
        background: color-mix(in oklab, var(--color-base-content) 8%, transparent);
        border: 1px solid color-mix(in oklab, var(--color-base-content) 15%, transparent);
    }

    .skill-tag.selected {
        color: var(--color-primary-content);
        background: var(--color-primary);
        border-color: var(--color-primary);
    }

    .skill-remove {
        display: grid;
        place-items: center;
        width: 1.1rem;
        height: 1.1rem;
        border-radius: 999px;
        line-height: 1;
        cursor: pointer;
        color: inherit;
        background: color-mix(in oklab, currentColor 18%, transparent);
    }

    .skill-remove:hover {
        background: color-mix(in oklab, currentColor 32%, transparent);
    }

    .skill-results {
        display: flex;
        flex-wrap: wrap;
        gap: 0.4rem;
        margin-top: 0.5rem;
    }

    .skill-result {
        font-size: 0.8rem;
        padding: 0.25rem 0.7rem;
        border-radius: 0.5rem;
        cursor: pointer;
        color: var(--color-base-content);
        background: color-mix(in oklab, var(--color-base-content) 6%, transparent);
        border: 1px solid color-mix(in oklab, var(--color-base-content) 15%, transparent);
        transition: background 0.15s ease, border-color 0.15s ease;
    }

    .skill-result:hover:not(:disabled) {
        border-color: color-mix(in oklab, var(--color-primary) 45%, transparent);
        background: color-mix(in oklab, var(--color-primary) 10%, transparent);
    }

    .skill-result.create {
        color: var(--color-primary);
        border-color: color-mix(in oklab, var(--color-primary) 40%, transparent);
        border-style: dashed;
    }

    .skill-result:disabled {
        opacity: 0.6;
        cursor: not-allowed;
    }

    .skill-hint {
        margin-top: 0.35rem;
    }

    /* --- Responsive ----------------------------------------------------- */

    @media (max-width: 48rem) {
        .add-textbook,
        .attach-row,
        .editor-row,
        .editor-actions {
            flex-direction: column;
            align-items: stretch;
        }

        .format-control {
            width: 100%;
        }

        .editor-layout {
            grid-template-columns: 1fr;
        }

        .tb-actions {
            flex-wrap: wrap;
        }
    }
</style>
