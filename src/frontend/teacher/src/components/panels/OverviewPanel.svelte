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
Overview tab: edit the course's database-backed settings. Saves via PATCH and
asks the parent to reload on success so the header stays in sync.
-->
<script lang="ts">
    import {onMount} from "svelte";

    import {fetchLibraryGroups, updateCourse} from "../../api/courses.js";
    import type {CourseDto, LibraryGroupDto, TextFormat} from "../../api/courses.js";
    import {toasts} from "../../stores/toast.store.js";

    let {course, onSaved}: {course: CourseDto; onSaved: () => void} = $props();

    let groups = $state<LibraryGroupDto[]>([]);
    let name = $state("");
    let slug = $state("");
    let description = $state("");
    let textFormat = $state<TextFormat>("MD");
    let groupId = $state("");
    let isTemplate = $state(false);
    let saving = $state(false);
    let loadingGroups = $state(true);
    let error = $state("");

    $effect(() => {
        course.id;
        name = course.name;
        slug = course.slug;
        description = course.description ?? "";
        textFormat = course.text_format;
        groupId = course.group;
        isTemplate = course.is_template;
    });

    onMount(() => {
        void loadGroups();
    });

    async function loadGroups(): Promise<void> {
        loadingGroups = true;
        try {
            groups = await fetchLibraryGroups();
        } catch (e) {
            error = e instanceof Error ? e.message : String(e);
        } finally {
            loadingGroups = false;
        }
    }

    async function save(): Promise<void> {
        if (!name.trim()) {
            error = "Course name is required.";
            return;
        }
        if (!slug.trim()) {
            error = "Course slug is required.";
            return;
        }
        if (!groupId) {
            error = "Library group is required.";
            return;
        }

        saving = true;
        error = "";
        message = "";

        try {
            await updateCourse(course.id, {
                name: name.trim(),
                slug: slug.trim(),
                description: description.trim(),
                text_format: textFormat,
                group: groupId,
                is_template: isTemplate,
            });
            toasts.success("Course saved.");
            onSaved();
        } catch (e) {
            error = e instanceof Error ? e.message : String(e);
        } finally {
            saving = false;
        }
    }
</script>

<div class="card bg-base-100 shadow-sm">
    <div class="card-body">
        {#if error}
            <div class="alert alert-error"><span>{error}</span></div>
        {/if}

        <label class="form-control w-full">
            <span class="label-text">Course name</span>
            <input class="input input-bordered w-full" type="text" bind:value={name} />
        </label>

        <label class="form-control w-full mt-3">
            <span class="label-text">Description</span>
            <textarea class="textarea textarea-bordered w-full" rows="5" bind:value={description}></textarea>
        </label>

        <!-- Less-used / technical settings, collapsed by default. -->
        <details class="advanced">
            <summary>Advanced settings</summary>

            <div class="settings-grid mt-3">
                <label class="form-control w-full">
                    <span class="label-text">Slug</span>
                    <input class="input input-bordered w-full" type="text" bind:value={slug} />
                </label>

                <label class="form-control w-full">
                    <span class="label-text">Library group</span>
                    <select class="select select-bordered w-full" bind:value={groupId} disabled={loadingGroups}>
                        {#each groups as group (group.id)}
                            <option value={group.id}>{group.name}</option>
                        {/each}
                    </select>
                </label>

                <label class="form-control w-full">
                    <span class="label-text">Text format</span>
                    <select class="select select-bordered w-full" bind:value={textFormat}>
                        <option value="MD">Markdown</option>
                        <option value="HTML">HTML</option>
                        <option value="TEXT">Plain text</option>
                    </select>
                </label>
            </div>

            <label class="label mt-3 cursor-pointer justify-start gap-3">
                <input class="checkbox checkbox-primary" type="checkbox" bind:checked={isTemplate} />
                <span class="label-text">Template course</span>
            </label>

            <dl class="meta-grid mt-4">
                <div>
                    <dt>Owner</dt>
                    <dd>{course.owner ?? "—"}</dd>
                </div>
                <div>
                    <dt>Created at</dt>
                    <dd>{course.created_at}</dd>
                </div>
                <div>
                    <dt>Modified at</dt>
                    <dd>{course.modified_at}</dd>
                </div>
            </dl>
        </details>

        <div class="card-actions justify-end mt-4">
            <button type="button" class="btn btn-primary" onclick={save} disabled={saving}>
                {#if saving}<span class="loading loading-spinner loading-sm"></span>{/if}
                Save changes
            </button>
        </div>
    </div>
</div>

<style>
    .settings-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 1rem;
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

    .meta-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 0.75rem 1rem;
        padding-top: 1rem;
        border-top: 1px solid color-mix(in oklab, var(--color-base-content) 12%, transparent);
    }

    dt {
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        color: color-mix(in oklab, var(--color-base-content) 58%, transparent);
    }

    dd {
        min-width: 0;
        overflow-wrap: anywhere;
        color: color-mix(in oklab, var(--color-base-content) 78%, transparent);
    }

    @media (max-width: 48rem) {
        .settings-grid,
        .meta-grid {
            grid-template-columns: 1fr;
        }
    }
</style>
