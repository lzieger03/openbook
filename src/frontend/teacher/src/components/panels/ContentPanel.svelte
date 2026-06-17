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
per material, the page ranges selected within that textbook. Materials can be
added, reordered (by swapping positions) and removed; page ranges can be added
and removed.
-->
<script lang="ts">
    import {loadMaterials, loadPageRanges} from "../../data/teacher.js";
    import type {CourseMaterialView, PageRangeView} from "../../data/teacher.js";
    import {
        addMaterial,
        addPageRange,
        deleteMaterial,
        deletePageRange,
        fetchTextbookPages,
        fetchTextbooks,
        updateMaterialPosition,
    } from "../../api/content.js";
    import type {TextbookDto, TextbookPageDto} from "../../api/content.js";

    let {courseId}: {courseId: string} = $props();

    let materials = $state<CourseMaterialView[]>([]);
    let textbooks = $state<TextbookDto[]>([]);
    let isLoading = $state(true);
    let error = $state("");

    // Add-material form.
    let newTextbookId = $state("");
    let addingMaterial = $state(false);

    // Per-material page-range editing (one expanded at a time).
    let expandedId = $state<string | null>(null);
    let ranges = $state<PageRangeView[]>([]);
    let rangesLoading = $state(false);
    let pages = $state<TextbookPageDto[]>([]);
    let startPageId = $state("");
    let endPageId = $state("");
    let addingRange = $state(false);

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

        try {
            await addMaterial(courseId, newTextbookId, nextPosition());
            await load();
        } catch (e) {
            error = e instanceof Error ? e.message : String(e);
        } finally {
            addingMaterial = false;
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

    /** Swap the position of a material with its neighbour to reorder the list. */
    async function move(index: number, direction: -1 | 1): Promise<void> {
        const target = index + direction;
        const a = materials[index];
        const b = materials[target];

        if (!a || !b) {
            return;
        }

        error = "";
        try {
            await Promise.all([updateMaterialPosition(a.id, b.position), updateMaterialPosition(b.id, a.position)]);
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
        rangesLoading = true;
        startPageId = "";
        endPageId = "";

        try {
            [ranges, pages] = await Promise.all([
                loadPageRanges(material.id),
                fetchTextbookPages(material.textbookId),
            ]);
            if (pages.length > 0 && pages[0]) {
                startPageId = pages[0].id;
                endPageId = pages[pages.length - 1]?.id ?? pages[0].id;
            }
        } catch (e) {
            error = e instanceof Error ? e.message : String(e);
        } finally {
            rangesLoading = false;
        }
    }

    async function onAddRange(materialId: string): Promise<void> {
        if (!startPageId || !endPageId) {
            return;
        }

        addingRange = true;
        error = "";

        try {
            const position = ranges.reduce((max, r) => Math.max(max, r.position), 0) + 1;
            await addPageRange(materialId, startPageId, endPageId, position);
            ranges = await loadPageRanges(materialId);
        } catch (e) {
            error = e instanceof Error ? e.message : String(e);
        } finally {
            addingRange = false;
        }
    }

    async function onDeleteRange(materialId: string, rangeId: string): Promise<void> {
        error = "";
        try {
            await deletePageRange(rangeId);
            ranges = await loadPageRanges(materialId);
        } catch (e) {
            error = e instanceof Error ? e.message : String(e);
        }
    }
</script>

<div class="card bg-base-100 shadow-sm">
    <div class="card-body">
        <h2 class="card-title">Course content</h2>
        <p class="muted">Attach textbooks and define which page ranges belong to this course.</p>

        {#if error}
            <div class="alert alert-error"><span>{error}</span></div>
        {/if}

        <!-- Add material -->
        <div class="add-row">
            <select class="select select-bordered" bind:value={newTextbookId}>
                {#each textbooks as textbook (textbook.id)}
                    <option value={textbook.id}>{textbook.name}</option>
                {/each}
            </select>
            <button type="button" class="btn btn-primary" onclick={onAddMaterial} disabled={addingMaterial || !newTextbookId}>
                {#if addingMaterial}<span class="loading loading-spinner loading-sm"></span>{/if}
                Add textbook
            </button>
        </div>

        {#if isLoading}
            <span class="loading loading-spinner"></span>
        {:else if materials.length === 0}
            <p class="muted">No materials yet. Add a textbook to start building this course.</p>
        {:else}
            <ol class="material-list">
                {#each materials as material, index (material.id)}
                    <li class="material">
                        <div class="material-head">
                            <span class="pos">{index + 1}</span>
                            <span class="name">{material.textbookName}</span>
                            <span class="muted">{material.pageRangeCount} range(s)</span>

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
                                {#if rangesLoading}
                                    <span class="loading loading-spinner loading-sm"></span>
                                {:else}
                                    {#if ranges.length > 0}
                                        <ul class="range-list">
                                            {#each ranges as range (range.id)}
                                                <li>
                                                    <span>{range.startPageName} &rarr; {range.endPageName}</span>
                                                    <button type="button" class="btn btn-xs btn-ghost text-error" onclick={() => onDeleteRange(material.id, range.id)}>×</button>
                                                </li>
                                            {/each}
                                        </ul>
                                    {:else}
                                        <p class="muted">No page ranges yet — the whole textbook is used.</p>
                                    {/if}

                                    <div class="range-add">
                                        <label>
                                            <span class="label-text">From</span>
                                            <select class="select select-bordered select-sm" bind:value={startPageId}>
                                                {#each pages as page (page.id)}
                                                    <option value={page.id}>{page.name}</option>
                                                {/each}
                                            </select>
                                        </label>
                                        <label>
                                            <span class="label-text">To</span>
                                            <select class="select select-bordered select-sm" bind:value={endPageId}>
                                                {#each pages as page (page.id)}
                                                    <option value={page.id}>{page.name}</option>
                                                {/each}
                                            </select>
                                        </label>
                                        <button type="button" class="btn btn-sm btn-primary" onclick={() => onAddRange(material.id)} disabled={addingRange || pages.length === 0}>
                                            Add range
                                        </button>
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
    .add-row {
        display: flex;
        gap: 0.5rem;
        margin: 0.5rem 0 1rem;
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

    .range-list {
        list-style: none;
        margin: 0 0 0.75rem;
        padding: 0;
        display: flex;
        flex-direction: column;
        gap: 0.3rem;
    }

    .range-list li {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 0.5rem;
        font-size: 0.9rem;
    }

    .range-add {
        display: flex;
        align-items: flex-end;
        gap: 0.5rem;
        flex-wrap: wrap;
    }

    .range-add label {
        display: flex;
        flex-direction: column;
        gap: 0.15rem;
    }

    .muted {
        color: color-mix(in oklab, var(--color-base-content) 60%, transparent);
        font-size: 0.85rem;
    }
</style>
