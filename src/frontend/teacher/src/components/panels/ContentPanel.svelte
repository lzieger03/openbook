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
Content tab: manage the ordered course materials (each linking a textbook) and,
per material, the textbook pages and their content. Materials can be added,
reordered (by swapping positions) and removed. The whole linked textbook is used
in the course.
-->
<script lang="ts">
    import MarkdownIt from "markdown-it";

    import {loadMaterials} from "../../data/teacher.js";
    import type {CourseMaterialView} from "../../data/teacher.js";
    import {
        addMaterial,
        createTextbook,
        createTextbookPage,
        deleteMaterial,
        fetchTextbookPages,
        fetchTextbooks,
        moveMaterial,
        updateTextbookPage,
    } from "../../api/content.js";
    import type {SourceContent, TextbookDto, TextbookPageDto} from "../../api/content.js";
    import {slugify} from "../../api/courses.js";
    import type {TextFormat} from "../../api/courses.js";

    let {courseId, courseGroupId}: {courseId: string; courseGroupId: string} = $props();

    let materials = $state<CourseMaterialView[]>([]);
    let textbooks = $state<TextbookDto[]>([]);
    let isLoading = $state(true);
    let error = $state("");

    // Add-material form.
    let newTextbookId = $state("");
    let addingMaterial = $state(false);
    let newMaterialName = $state("");
    let newMaterialSlug = $state("");
    let newMaterialDescription = $state("");
    let newMaterialFormat = $state<TextFormat>("MD");
    let creatingMaterial = $state(false);
    let materialMessage = $state("");

    // Per-material page editing (one material expanded at a time).
    let expandedId = $state<string | null>(null);
    let pagesLoading = $state(false);
    let pages = $state<TextbookPageDto[]>([]);

    // Page source editing.
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

    const markdownRenderer = new MarkdownIt({
        breaks: true,
        html: false,
        linkify: true,
        typographer: true,
    });

    const selectedPage = $derived(pages.find((page) => page.id === selectedPageId) ?? null);
    const newMaterialSlugPlaceholder = $derived(slugify(newMaterialName));

    async function load(): Promise<void> {
        isLoading = true;
        error = "";

        try {
            [materials, textbooks] = await Promise.all([loadMaterials(courseId), fetchTextbooks()]);
            if (textbooks.length > 0 && textbooks[0] && !newTextbookId) {
                newTextbookId = textbooks[0].id;
            }
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

    async function onAddMaterial(): Promise<void> {
        if (!newTextbookId) {
            return;
        }

        addingMaterial = true;
        error = "";
        materialMessage = "";

        try {
            await addMaterial(courseId, newTextbookId, nextPosition());
            await load();
        } catch (e) {
            error = e instanceof Error ? e.message : String(e);
        } finally {
            addingMaterial = false;
        }
    }

    function resetMaterialForm(): void {
        newMaterialName = "";
        newMaterialSlug = "";
        newMaterialDescription = "";
        newMaterialFormat = "MD";
    }

    async function onCreateMaterial(): Promise<void> {
        if (!newMaterialName.trim()) {
            error = "Please enter a material name.";
            return;
        }
        if (!courseGroupId) {
            error = "This course has no library group. Choose one in Overview before creating material.";
            return;
        }

        creatingMaterial = true;
        error = "";
        materialMessage = "";

        try {
            const textbook = await createTextbook({
                name: newMaterialName.trim(),
                slug: newMaterialSlug.trim() || newMaterialSlugPlaceholder,
                description: newMaterialDescription.trim(),
                text_format: newMaterialFormat,
                group: courseGroupId,
            });
            await addMaterial(courseId, textbook.id, nextPosition());

            textbooks = [...textbooks, textbook].sort((a, b) => a.name.localeCompare(b.name));
            materials = await loadMaterials(courseId);
            newTextbookId = textbook.id;
            resetMaterialForm();
            materialMessage = "Material created.";

            const material = materials.find((candidate) => candidate.textbookId === textbook.id);
            if (material) {
                await toggleExpand(material);
            }
        } catch (e) {
            error = e instanceof Error ? e.message : String(e);
        } finally {
            creatingMaterial = false;
        }
    }

    async function onDeleteMaterial(id: string): Promise<void> {
        error = "";
        try {
            await deleteMaterial(id);
            if (expandedId === id) {
                expandedId = null;
            }
            await load();
        } catch (e) {
            error = e instanceof Error ? e.message : String(e);
        }
    }

    /** Move a material one step up or down to reorder the list. */
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
            error = "Please enter a page name.";
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
                text_format: pageTextFormat,
                content: makeContent(),
            });
            pages = await fetchTextbookPages(material.textbookId);
            selectPage(created.id);
            newPageName = "";
            editorMessage = "Page created.";
        } catch (e) {
            error = e instanceof Error ? e.message : String(e);
        } finally {
            creatingPage = false;
        }
    }

    async function onSavePage(): Promise<void> {
        if (!selectedPageId) {
            error = "Please select a page.";
            return;
        }
        if (!pageName.trim()) {
            error = "Page name is required.";
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
            });
            pages = pages.map((page) => (page.id === updated.id ? updated : page));
            selectPage(updated.id);
            editorMessage = "Page saved.";
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
        <p class="muted">Attach textbooks to this course and edit their pages and content.</p>

        {#if error}
            <div class="alert alert-error"><span>{error}</span></div>
        {/if}

        {#if materialMessage}
            <div class="alert alert-success"><span>{materialMessage}</span></div>
        {/if}

        <div class="material-tools">
            <section class="material-create" aria-labelledby="create-material-title">
                <div class="section-head">
                    <h3 id="create-material-title">Create material</h3>
                </div>

                <div class="material-form-grid">
                    <label class="form-control w-full">
                        <span class="label-text">Material name</span>
                        <input class="input input-bordered w-full" type="text" bind:value={newMaterialName} placeholder="e.g. Chapter 1" />
                    </label>

                    <label class="form-control w-full">
                        <span class="label-text">Slug</span>
                        <input class="input input-bordered w-full" type="text" bind:value={newMaterialSlug} placeholder={newMaterialSlugPlaceholder} />
                    </label>

                    <label class="form-control w-full">
                        <span class="label-text">Format</span>
                        <select class="select select-bordered w-full" bind:value={newMaterialFormat}>
                            <option value="MD">Markdown</option>
                            <option value="HTML">HTML</option>
                            <option value="TEXT">Plain text</option>
                        </select>
                    </label>

                    <label class="form-control w-full material-description">
                        <span class="label-text">Description</span>
                        <textarea class="textarea textarea-bordered w-full" rows="3" bind:value={newMaterialDescription}></textarea>
                    </label>
                </div>

                <div class="tool-actions">
                    <button
                        type="button"
                        class="btn btn-primary"
                        onclick={onCreateMaterial}
                        disabled={creatingMaterial || !newMaterialName.trim() || !courseGroupId}
                    >
                        {#if creatingMaterial}<span class="loading loading-spinner loading-sm"></span>{/if}
                        Create material
                    </button>
                </div>
            </section>

            <section class="material-attach" aria-labelledby="attach-material-title">
                <div class="section-head">
                    <h3 id="attach-material-title">Attach existing textbook</h3>
                </div>

                <div class="add-row">
                    <select class="select select-bordered" bind:value={newTextbookId}>
                        {#each textbooks as textbook (textbook.id)}
                            <option value={textbook.id}>{textbook.name}</option>
                        {/each}
                    </select>
                    <button type="button" class="btn btn-ghost" onclick={onAddMaterial} disabled={addingMaterial || !newTextbookId}>
                        {#if addingMaterial}<span class="loading loading-spinner loading-sm"></span>{/if}
                        Attach
                    </button>
                </div>
            </section>
        </div>

        {#if isLoading}
            <span class="loading loading-spinner"></span>
        {:else if materials.length === 0}
            <p class="muted">No materials yet. Create material above to start building this course.</p>
        {:else}
            <ol class="material-list">
                {#each materials as material, index (material.id)}
                    <li class="material">
                        <div class="material-head">
                            <span class="pos">{index + 1}</span>
                            <span class="name">{material.textbookName}</span>

                            <span class="material-actions">
                                <button type="button" class="btn btn-xs btn-ghost" disabled={index === 0} onclick={() => move(index, -1)} aria-label="Move up">↑</button>
                                <button type="button" class="btn btn-xs btn-ghost" disabled={index === materials.length - 1} onclick={() => move(index, 1)} aria-label="Move down">↓</button>
                                <button type="button" class="btn btn-xs btn-ghost" onclick={() => toggleExpand(material)}>
                                    {expandedId === material.id ? "Hide pages" : "Edit pages"}
                                </button>
                                <button type="button" class="btn btn-xs btn-ghost text-error" onclick={() => onDeleteMaterial(material.id)}>Remove</button>
                            </span>
                        </div>

                        {#if expandedId === material.id}
                            <div class="ranges">
                                {#if pagesLoading}
                                    <span class="loading loading-spinner loading-sm"></span>
                                {:else}
                                    <div class="page-editor">
                                        <div class="editor-head">
                                            <div>
                                                <h3>Page editor</h3>
                                                <p class="muted">Edit Markdown, HTML, or plain text content for the selected textbook page.</p>
                                            </div>
                                            <label class="btn btn-sm btn-ghost">
                                                Import file
                                                <input class="sr-only" type="file" accept=".md,.markdown,.html,.htm,.txt,text/markdown,text/html,text/plain" onchange={onFileSelected} />
                                            </label>
                                        </div>

                                        {#if editorMessage}
                                            <div class="alert alert-success alert-sm"><span>{editorMessage}</span></div>
                                        {/if}

                                        <div class="editor-grid">
                                            <label class="form-control w-full">
                                                <span class="label-text">Existing page</span>
                                                <select class="select select-bordered select-sm" bind:value={selectedPageId} onchange={(event) => selectPage(event.currentTarget.value)}>
                                                    <option value="">Select page</option>
                                                    {#each pages as page (page.id)}
                                                        <option value={page.id}>{page.name}</option>
                                                    {/each}
                                                </select>
                                            </label>

                                            <label class="form-control w-full">
                                                <span class="label-text">Create page</span>
                                                <div class="join w-full">
                                                    <input class="input input-bordered input-sm join-item flex-1" type="text" bind:value={newPageName} placeholder="New page title" />
                                                    <button type="button" class="btn btn-sm btn-primary join-item" onclick={() => onCreatePage(material)} disabled={creatingPage || !newPageName.trim()}>
                                                        {#if creatingPage}<span class="loading loading-spinner loading-xs"></span>{/if}
                                                        Add
                                                    </button>
                                                </div>
                                            </label>
                                        </div>

                                        <div class="editor-grid mt-3">
                                            <label class="form-control w-full">
                                                <span class="label-text">Page title</span>
                                                <input class="input input-bordered input-sm w-full" type="text" bind:value={pageName} disabled={!selectedPage} />
                                            </label>

                                            <label class="form-control w-full">
                                                <span class="label-text">Format</span>
                                                <select class="select select-bordered select-sm w-full" bind:value={pageTextFormat}>
                                                    <option value="MD">Markdown</option>
                                                    <option value="HTML">HTML</option>
                                                    <option value="TEXT">Plain text</option>
                                                </select>
                                            </label>
                                        </div>

                                        <div class="editor-tabs mt-3">
                                            <button type="button" class="btn btn-sm" class:btn-primary={editorMode === "edit"} onclick={() => (editorMode = "edit")}>Edit</button>
                                            <button type="button" class="btn btn-sm" class:btn-primary={editorMode === "preview"} onclick={() => (editorMode = "preview")}>Preview</button>
                                        </div>

                                        {#if editorMode === "edit"}
                                            <textarea
                                                class="textarea textarea-bordered editor-source"
                                                bind:value={editorSource}
                                                disabled={!selectedPage}
                                                placeholder="Write Markdown, HTML, or import a .md/.html/.txt file."
                                            ></textarea>
                                        {:else if pageTextFormat === "HTML"}
                                            <iframe class="preview-frame" title="HTML preview" sandbox="" srcdoc={previewHtml}></iframe>
                                        {:else}
                                            <div class="preview-prose">{@html previewHtml}</div>
                                        {/if}

                                        <div class="editor-actions">
                                            <span class="muted">{editorFilename ? `Imported from ${editorFilename}` : "Content is stored on the selected textbook page."}</span>
                                            <button type="button" class="btn btn-sm btn-primary" onclick={onSavePage} disabled={editorSaving || !selectedPage}>
                                                {#if editorSaving}<span class="loading loading-spinner loading-xs"></span>{/if}
                                                Save page
                                            </button>
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
    .material-tools {
        display: grid;
        grid-template-columns: minmax(0, 2fr) minmax(16rem, 1fr);
        gap: 1rem;
        margin: 0.75rem 0 1rem;
    }

    .material-create,
    .material-attach {
        min-width: 0;
        padding: 1rem;
        border: 1px solid color-mix(in oklab, var(--color-base-content) 12%, transparent);
        border-radius: 0.5rem;
    }

    .section-head {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
        margin-bottom: 0.75rem;
    }

    .section-head h3 {
        font-weight: 700;
    }

    .material-form-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 0.75rem;
    }

    .material-description {
        grid-column: 1 / -1;
    }

    .tool-actions {
        display: flex;
        justify-content: flex-end;
        margin-top: 0.75rem;
    }

    .add-row {
        display: flex;
        gap: 0.5rem;
    }

    .add-row select {
        min-width: 0;
        flex: 1 1 auto;
    }

    .material-list {
        list-style: none;
        margin: 0;
        padding: 0;
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }

    .material {
        border: 1px solid color-mix(in oklab, var(--color-base-content) 12%, transparent);
        border-radius: 0.6rem;
        padding: 0.6rem 0.8rem;
    }

    .material-head {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }

    .pos {
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

    .name {
        font-weight: 600;
    }

    .material-actions {
        margin-left: auto;
        display: flex;
        gap: 0.25rem;
    }

    .ranges {
        margin-top: 0.75rem;
        padding-top: 0.75rem;
        border-top: 1px dashed color-mix(in oklab, var(--color-base-content) 15%, transparent);
    }

    .page-editor {
        margin-top: 1rem;
        padding-top: 1rem;
        border-top: 1px dashed color-mix(in oklab, var(--color-base-content) 15%, transparent);
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
    }

    .editor-head {
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        gap: 1rem;
    }

    .editor-head h3 {
        font-weight: 700;
    }

    .editor-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 0.75rem;
    }

    .editor-tabs {
        display: flex;
        gap: 0.5rem;
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

    .muted {
        color: color-mix(in oklab, var(--color-base-content) 60%, transparent);
        font-size: 0.85rem;
    }

    @media (max-width: 48rem) {
        .material-tools,
        .material-form-grid {
            grid-template-columns: 1fr;
        }

        .add-row,
        .material-head,
        .editor-head,
        .editor-actions {
            align-items: stretch;
            flex-direction: column;
        }

        .material-actions {
            margin-left: 0;
            flex-wrap: wrap;
        }

        .editor-grid {
            grid-template-columns: 1fr;
        }
    }
</style>
