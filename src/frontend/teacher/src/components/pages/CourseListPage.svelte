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

    // Confirmation for deleting a course.
    let deletingId = $state<string | null>(null);

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
        } catch (error) {
            formError = error instanceof Error ? error.message : String(error);
        } finally {
            saving = false;
        }
    }

    async function confirmDelete(id: string): Promise<void> {
        try {
            await teacherStore.remove(id);
        } finally {
            deletingId = null;
        }
    }
</script>

<div class="page">
    <header class="top">
        <h1 class="title">My Courses</h1>
        <button type="button" class="btn btn-primary" onclick={openCreate}>+ New course</button>
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
        <div class="status-box">
            <p>No courses yet. Create your first course to get started.</p>
            <button type="button" class="btn btn-primary btn-sm" onclick={openCreate}>+ New course</button>
        </div>
    {:else}
        <ul class="course-grid">
            {#each state.courses as course (course.id)}
                <li class="card bg-base-100 shadow-sm">
                    <div class="card-body">
                        <h2 class="card-title">{course.name}</h2>
                        {#if course.description}
                            <p class="desc">{course.description}</p>
                        {/if}
                        <p class="meta">{course.materialCount} material(s)</p>

                        <div class="card-actions">
                            <button
                                type="button"
                                class="btn btn-sm btn-primary"
                                onclick={() => push(`/courses/${course.id}`)}
                            >
                                Manage
                            </button>

                            {#if deletingId === course.id}
                                <button type="button" class="btn btn-sm btn-error" onclick={() => confirmDelete(course.id)}>
                                    Confirm delete
                                </button>
                                <button type="button" class="btn btn-sm btn-ghost" onclick={() => (deletingId = null)}>
                                    Cancel
                                </button>
                            {:else}
                                <button type="button" class="btn btn-sm btn-ghost" onclick={() => (deletingId = course.id)}>
                                    Delete
                                </button>
                            {/if}
                        </div>
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

        <div class="divider my-4">Library group</div>

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
    }

    .title {
        font-size: clamp(1.4rem, 3vw, 2rem);
        font-weight: 800;
    }

    .course-grid {
        list-style: none;
        margin: 0;
        padding: 0;
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(18rem, 1fr));
        gap: 1rem;
    }

    .desc {
        font-size: 0.9rem;
        color: color-mix(in oklab, var(--color-base-content) 75%, transparent);
    }

    .meta {
        font-size: 0.8rem;
        color: color-mix(in oklab, var(--color-base-content) 60%, transparent);
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

    @media (max-width: 42rem) {
        .settings-grid {
            grid-template-columns: 1fr;
        }
    }
</style>
