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
Landing page of the teacher area: lists the teacher's courses as cards and offers
a "New course" dialog. Each card links to the course detail page; courses can be
deleted from here after a confirmation step.
-->
<script lang="ts">
    import {onMount} from "svelte";
    import {push} from "svelte-spa-router";
    import {teacherStore} from "../../stores/teacher.store.js";
    import type {TeacherState} from "../../stores/teacher.store.js";
    import {createLibraryGroup, fetchLibraryGroups, slugify} from "../../api/courses.js";
    import type {LibraryGroupDto, TextFormat} from "../../api/courses.js";
    import Modal from "../basic/Modal.svelte";
    import {toasts} from "../../stores/toast.store.js";

    type GroupMode = "existing" | "new";

    let state = $state<TeacherState>({
        isLoading: true,
        errorMessage: "",
        user: null,
        courses: [],
    });

    // Create dialog state.
    let showCreate = $state(false);
    let groups = $state<LibraryGroupDto[]>([]);
    let name = $state("");
    let slug = $state("");
    let description = $state("");
    let textFormat = $state<TextFormat>("MD");
    let isTemplate = $state(false);
    let groupMode = $state<GroupMode>("existing");
    let groupId = $state("");
    let groupName = $state("");
    let groupSlug = $state("");
    let groupDescription = $state("");
    let groupParentId = $state("");
    let saving = $state(false);
    let formError = $state("");

    // Deletion in-flight indicator.
    let deletingId = $state<string | null>(null);

    // Filter the course list by name/description.
    let search = $state("");
    const filteredCourses = $derived.by(() => {
        const term = search.trim().toLowerCase();
        if (!term) {
            return state.courses;
        }
        return state.courses.filter(
            (course) =>
                course.name.toLowerCase().includes(term) ||
                course.description.toLowerCase().includes(term),
        );
    });

    onMount(() => {
        const unsubscribe = teacherStore.subscribe((value) => {
            state = value;
        });
        teacherStore.refresh();
        return unsubscribe;
    });

    async function openCreate(): Promise<void> {
        name = "";
        slug = "";
        description = "";
        textFormat = "MD";
        isTemplate = false;
        groupMode = "existing";
        groupId = "";
        groupName = "";
        groupSlug = "";
        groupDescription = "";
        groupParentId = "";
        formError = "";
        showCreate = true;

        try {
            groups = await fetchLibraryGroups();
            if (groups.length > 0 && groups[0]) {
                groupId = groups[0].id;
            } else {
                groupMode = "new";
            }
        } catch (error) {
            formError = error instanceof Error ? error.message : String(error);
        }
    }

    async function submitCreate(): Promise<void> {
        if (!name.trim()) {
            formError = "Please enter a course name.";
            return;
        }
        if (groupMode === "existing" && !groupId) {
            formError = "Please choose a library group.";
            return;
        }
        if (groupMode === "new" && !groupName.trim()) {
            formError = "Please enter a library group name.";
            return;
        }

        saving = true;
        formError = "";

        try {
            let selectedGroupId = groupId;

            if (groupMode === "new") {
                const createdGroup = await createLibraryGroup({
                    name: groupName.trim(),
                    slug: groupSlug.trim() || slugify(groupName),
                    description: groupDescription.trim(),
                    parent: groupParentId || null,
                    text_format: "MD",
                });
                selectedGroupId = createdGroup.id;
                groups = [...groups, createdGroup];
            }

            await teacherStore.create({
                name: name.trim(),
                slug: slug.trim() || slugify(name),
                description: description.trim(),
                group: selectedGroupId,
                text_format: textFormat,
                is_template: isTemplate,
            });
            showCreate = false;
            toasts.success(`Course “${name.trim()}” created.`);
        } catch (error) {
            formError = error instanceof Error ? error.message : String(error);
        } finally {
            saving = false;
        }
    }

    async function removeCourse(course: {id: string; name: string}): Promise<void> {
        if (!confirm(`Delete the course “${course.name}”? This cannot be undone.`)) {
            return;
        }
        deletingId = course.id;
        try {
            await teacherStore.remove(course.id);
            toasts.success(`Course “${course.name}” deleted.`);
        } catch (error) {
            toasts.error(error instanceof Error ? error.message : String(error));
        } finally {
            deletingId = null;
        }
    }
</script>

<div class="page">
    <header class="top">
        <div class="top-titles">
            <h1 class="title">My Courses</h1>
            {#if !state.isLoading && !state.errorMessage}
                <span class="count-pill">{state.courses.length}</span>
            {/if}
        </div>
        <div class="top-actions">
            {#if state.courses.length > 6}
                <input class="course-search input input-bordered input-sm" type="search" placeholder="Search courses…" bind:value={search} />
            {/if}
            <button type="button" class="btn btn-primary" onclick={openCreate}>+ New course</button>
        </div>
    </header>

    {#if state.isLoading}
        <div class="status-box" role="status" aria-live="polite">
            <span class="loading loading-spinner loading-lg"></span>
            <p>Loading your courses…</p>
        </div>
    {:else if state.errorMessage}
        <div class="status-box" role="alert">
            <p class="error">{state.errorMessage}</p>
            <button type="button" class="btn btn-sm" onclick={() => teacherStore.refresh()}>Retry</button>
        </div>
    {:else if state.courses.length === 0}
        <div class="empty">
            <span class="empty-icon" aria-hidden="true">📚</span>
            <p class="empty-title">No courses yet</p>
            <p class="empty-hint">Create your first course to start building content, quizzes and exams.</p>
            <button type="button" class="btn btn-primary" onclick={openCreate}>+ New course</button>
        </div>
    {:else if filteredCourses.length === 0}
        <div class="empty">
            <p class="empty-title">No courses match “{search}”.</p>
        </div>
    {:else}
        <ul class="course-grid">
            {#each filteredCourses as course (course.id)}
                <li class="course-card">
                    <button type="button" class="card-open" onclick={() => push(`/courses/${course.id}`)}>
                        <div class="card-head">
                            <h2 class="card-name">{course.name}</h2>
                            {#if course.isTemplate}
                                <span class="status-badge template">Template</span>
                            {:else if course.materialCount === 0}
                                <span class="status-badge empty-badge">Empty</span>
                            {:else}
                                <span class="status-badge active">Active</span>
                            {/if}
                        </div>

                        {#if course.description}
                            <p class="card-desc">{course.description}</p>
                        {:else}
                            <p class="card-desc muted">No description yet.</p>
                        {/if}

                        <div class="card-stats">
                            <span class="stat" title="Textbooks">📚 {course.materialCount}</span>
                            <span class="stat" title="Skills">🎯 {course.skills.length}</span>
                        </div>

                        {#if course.skills.length > 0}
                            <div class="card-skills">
                                {#each course.skills.slice(0, 3) as skill (skill.id)}
                                    <span class="skill-tag">{skill.name}</span>
                                {/each}
                                {#if course.skills.length > 3}
                                    <span class="skill-tag more">+{course.skills.length - 3}</span>
                                {/if}
                            </div>
                        {/if}
                    </button>

                    <div class="card-foot">
                        <button type="button" class="btn btn-sm btn-primary" onclick={() => push(`/courses/${course.id}`)}>
                            Open course →
                        </button>
                        <button
                            type="button"
                            class="btn btn-sm btn-ghost text-error"
                            disabled={deletingId === course.id}
                            onclick={() => removeCourse(course)}
                        >
                            {#if deletingId === course.id}<span class="loading loading-spinner loading-xs"></span>{/if}
                            Delete
                        </button>
                    </div>
                </li>
            {/each}
        </ul>
    {/if}
</div>

<Modal open={showCreate} title="New course" onClose={() => (showCreate = false)}>
    {#snippet children()}
        {#if formError}
            <div class="alert alert-error mb-3"><span>{formError}</span></div>
        {/if}

        <label class="form-control w-full">
            <span class="label-text">Course name</span>
            <input class="input input-bordered w-full" type="text" bind:value={name} placeholder="e.g. Introduction to Databases" />
        </label>

        <div class="divider my-4">Library group</div>
        <p class="modal-hint">Every course lives in a library group. Pick an existing one or create a new one.</p>

        <div class="join w-full">
            <button
                type="button"
                class="btn join-item flex-1"
                class:btn-primary={groupMode === "existing"}
                disabled={groups.length === 0}
                onclick={() => (groupMode = "existing")}
            >Existing</button>
            <button
                type="button"
                class="btn join-item flex-1"
                class:btn-primary={groupMode === "new"}
                onclick={() => (groupMode = "new")}
            >Create new</button>
        </div>

        {#if groupMode === "existing"}
            <label class="form-control w-full mt-3">
                <span class="label-text">Library group</span>
                <select class="select select-bordered w-full" bind:value={groupId}>
                    {#each groups as group (group.id)}
                        <option value={group.id}>{group.name}</option>
                    {/each}
                </select>
            </label>
        {:else}
            <label class="form-control w-full mt-3">
                <span class="label-text">Group name</span>
                <input class="input input-bordered w-full" type="text" bind:value={groupName} placeholder="e.g. Web Development" />
            </label>
        {/if}

        <!-- Everything below is optional; sensible defaults are used otherwise. -->
        <details class="advanced">
            <summary>Advanced settings</summary>

            <label class="form-control w-full mt-3">
                <span class="label-text">Course slug</span>
                <input class="input input-bordered w-full" type="text" bind:value={slug} placeholder={slugify(name)} />
            </label>

            <label class="form-control w-full mt-3">
                <span class="label-text">Description</span>
                <textarea class="textarea textarea-bordered w-full" rows="3" bind:value={description}></textarea>
            </label>

            <div class="settings-grid mt-3">
                <label class="form-control w-full">
                    <span class="label-text">Text format</span>
                    <select class="select select-bordered w-full" bind:value={textFormat}>
                        <option value="MD">Markdown</option>
                        <option value="HTML">HTML</option>
                        <option value="TEXT">Plain text</option>
                    </select>
                </label>

                <label class="label cursor-pointer justify-start gap-3">
                    <input class="checkbox checkbox-primary" type="checkbox" bind:checked={isTemplate} />
                    <span class="label-text">Template course</span>
                </label>
            </div>

            {#if groupMode === "new"}
                <label class="form-control w-full mt-3">
                    <span class="label-text">Group slug</span>
                    <input class="input input-bordered w-full" type="text" bind:value={groupSlug} placeholder={slugify(groupName)} />
                </label>

                <label class="form-control w-full mt-3">
                    <span class="label-text">Parent group</span>
                    <select class="select select-bordered w-full" bind:value={groupParentId}>
                        <option value="">No parent</option>
                        {#each groups as group (group.id)}
                            <option value={group.id}>{group.name}</option>
                        {/each}
                    </select>
                </label>

                <label class="form-control w-full mt-3">
                    <span class="label-text">Group description</span>
                    <textarea class="textarea textarea-bordered w-full" rows="3" bind:value={groupDescription}></textarea>
                </label>
            {/if}
        </details>
    {/snippet}

    {#snippet actions()}
        <button type="button" class="btn btn-ghost" onclick={() => (showCreate = false)} disabled={saving}>Cancel</button>
        <button type="button" class="btn btn-primary" onclick={submitCreate} disabled={saving}>
            {#if saving}<span class="loading loading-spinner loading-sm"></span>{/if}
            Create
        </button>
    {/snippet}
</Modal>

<style>
    .page {
        width: 90%;
        max-width: 80rem;
        margin: 0 auto;
        padding: 1.5rem 0 2rem;
        display: flex;
        flex-direction: column;
        gap: 1.25rem;
    }

    .top {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
        flex-wrap: wrap;
    }

    .top-titles {
        display: flex;
        align-items: center;
        gap: 0.6rem;
    }

    .title {
        font-size: clamp(1.4rem, 3vw, 2rem);
        font-weight: 800;
    }

    .count-pill {
        font-size: 0.85rem;
        font-weight: 700;
        padding: 0.1rem 0.6rem;
        border-radius: 999px;
        color: var(--color-primary);
        background: color-mix(in oklab, var(--color-primary) 14%, transparent);
    }

    .top-actions {
        display: flex;
        align-items: center;
        gap: 0.6rem;
    }

    .course-search {
        width: 14rem;
        max-width: 50vw;
    }

    /* Empty / onboarding state. */
    .empty {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.5rem;
        text-align: center;
        padding: 3.5rem 1rem;
        border: 1px dashed color-mix(in oklab, var(--color-base-content) 18%, transparent);
        border-radius: 1rem;
    }

    .empty-icon {
        font-size: 2.5rem;
    }

    .empty-title {
        font-size: 1.2rem;
        font-weight: 800;
    }

    .empty-hint {
        color: color-mix(in oklab, var(--color-base-content) 60%, transparent);
        margin-bottom: 0.5rem;
    }

    .course-grid {
        list-style: none;
        margin: 0;
        padding: 0;
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(18rem, 1fr));
        grid-auto-rows: 1fr;
        gap: 1rem;
    }

    /* A course is a card: a big clickable body + a footer with actions. */
    .course-card {
        display: flex;
        flex-direction: column;
        height: 100%;
        border-radius: 1rem;
        background: var(--color-base-100);
        border: 1px solid color-mix(in oklab, var(--color-base-content) 12%, transparent);
        box-shadow: 0 4px 14px color-mix(in oklab, var(--color-base-content) 8%, transparent);
        overflow: hidden;
        transition: transform 0.12s ease, border-color 0.2s ease, box-shadow 0.2s ease;
    }

    .course-card:hover {
        transform: translateY(-3px);
        border-color: color-mix(in oklab, var(--color-primary) 45%, transparent);
        box-shadow: 0 10px 24px color-mix(in oklab, var(--color-primary) 18%, transparent);
    }

    .card-open {
        flex: 1 1 auto;
        display: flex;
        flex-direction: column;
        gap: 0.6rem;
        align-items: flex-start;
        text-align: left;
        padding: 1.25rem 1.25rem 0.75rem;
        background: none;
        border: none;
        cursor: pointer;
        color: var(--color-base-content);
        width: 100%;
    }

    .card-open:focus-visible {
        outline: 2px solid var(--color-primary);
        outline-offset: -2px;
    }

    .card-head {
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        gap: 0.5rem;
        width: 100%;
    }

    .card-name {
        font-size: 1.15rem;
        font-weight: 700;
        line-height: 1.3;
    }

    .status-badge {
        flex: 0 0 auto;
        font-size: 0.65rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        padding: 0.15rem 0.5rem;
        border-radius: 999px;
    }

    .status-badge.active {
        color: var(--color-success);
        background: color-mix(in oklab, var(--color-success) 16%, transparent);
    }

    .status-badge.template {
        color: var(--color-warning);
        background: color-mix(in oklab, var(--color-warning) 16%, transparent);
    }

    .status-badge.empty-badge {
        color: color-mix(in oklab, var(--color-base-content) 60%, transparent);
        background: color-mix(in oklab, var(--color-base-content) 10%, transparent);
    }

    .card-desc {
        font-size: 0.9rem;
        line-height: 1.45;
        color: color-mix(in oklab, var(--color-base-content) 78%, transparent);
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }

    .card-desc.muted {
        font-style: italic;
        color: color-mix(in oklab, var(--color-base-content) 45%, transparent);
    }

    .card-stats {
        display: flex;
        gap: 0.85rem;
        font-size: 0.85rem;
        font-weight: 600;
        color: color-mix(in oklab, var(--color-base-content) 70%, transparent);
    }

    .card-skills {
        display: flex;
        flex-wrap: wrap;
        gap: 0.35rem;
        margin-top: auto;
    }

    .skill-tag {
        font-size: 0.72rem;
        font-weight: 600;
        padding: 0.1rem 0.55rem;
        border-radius: 999px;
        color: var(--color-primary);
        background: color-mix(in oklab, var(--color-primary) 12%, transparent);
        border: 1px solid color-mix(in oklab, var(--color-primary) 28%, transparent);
    }

    .skill-tag.more {
        color: color-mix(in oklab, var(--color-base-content) 60%, transparent);
        background: color-mix(in oklab, var(--color-base-content) 8%, transparent);
        border-color: transparent;
    }

    .card-foot {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 0.5rem;
        padding: 0.75rem 1.25rem 1.1rem;
        border-top: 1px solid color-mix(in oklab, var(--color-base-content) 8%, transparent);
    }

    .status-box {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 1rem;
        padding: 4rem 1rem;
        text-align: center;
        color: color-mix(in oklab, var(--color-base-content) 70%, transparent);
    }

    .error {
        color: var(--color-error);
        font-weight: 600;
        text-align: center;
    }

    .settings-grid {
        display: grid;
        grid-template-columns: minmax(0, 1fr) auto;
        align-items: end;
        gap: 1rem;
    }

    .modal-hint {
        font-size: 0.85rem;
        color: color-mix(in oklab, var(--color-base-content) 60%, transparent);
        margin: -0.5rem 0 0.75rem;
    }

    .advanced {
        margin-top: 1rem;
        border-top: 1px solid color-mix(in oklab, var(--color-base-content) 12%, transparent);
        padding-top: 0.5rem;
    }

    .advanced summary {
        cursor: pointer;
        font-size: 0.9rem;
        font-weight: 600;
        color: color-mix(in oklab, var(--color-base-content) 75%, transparent);
        padding: 0.25rem 0;
        list-style: revert;
    }

    @media (max-width: 42rem) {
        .settings-grid {
            grid-template-columns: 1fr;
        }
    }
</style>
