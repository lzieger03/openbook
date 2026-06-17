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
Overview tab: edit the course's name and description. Saves via PATCH and asks
the parent to reload on success so the header stays in sync.
-->
<script lang="ts">
    import {updateCourse} from "../../api/courses.js";
    import type {CourseDto} from "../../api/courses.js";

    let {course, onSaved}: {course: CourseDto; onSaved: () => void} = $props();

    let name = $state(course.name);
    let description = $state(course.description ?? "");
    let saving = $state(false);
    let message = $state("");
    let error = $state("");

    async function save(): Promise<void> {
        if (!name.trim()) {
            error = "Course name is required.";
            return;
        }

        saving = true;
        error = "";
        message = "";

        try {
            await updateCourse(course.id, {name: name.trim(), description: description.trim()});
            message = "Saved.";
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
        {#if message}
            <div class="alert alert-success"><span>{message}</span></div>
        {/if}

        <label class="form-control w-full">
            <span class="label-text">Course name</span>
            <input class="input input-bordered w-full" type="text" bind:value={name} />
        </label>

        <label class="form-control w-full mt-3">
            <span class="label-text">Description</span>
            <textarea class="textarea textarea-bordered w-full" rows="5" bind:value={description}></textarea>
        </label>

        <div class="card-actions justify-end mt-4">
            <button type="button" class="btn btn-primary" onclick={save} disabled={saving}>
                {#if saving}<span class="loading loading-spinner loading-sm"></span>{/if}
                Save changes
            </button>
        </div>
    </div>
</div>
