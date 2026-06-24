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
Profile edit page. Loads the current user and lets them update name, bio and
profile picture (REST), and request an e-mail change (allauth, verified).
Username is read-only; e-mail becomes active only after the verification link.
-->
<script lang="ts">
    import {onDestroy, onMount} from "svelte";
    import {push} from "svelte-spa-router";
    import {fetchCurrentUser} from "../../api/gamification.js";
    import {fetchEmailAddresses, requestEmailChange, saveProfile} from "../../api/profile.js";
    import type {EmailAddress} from "../../api/profile.js";
    import {dashboardStore} from "../../stores/dashboard.store.js";

    let isLoading = $state(true);
    let isSaving = $state(false);
    let errorMessage = $state("");
    let successMessage = $state("");

    let username = $state("");
    let firstName = $state("");
    let lastName = $state("");
    let description = $state("");
    let email = $state("");
    let originalEmail = $state("");

    let currentPictureUrl = $state<string | null>(null);
    let previewUrl = $state<string | null>(null);
    let pictureFile = $state<File | null>(null);
    let emails = $state<EmailAddress[]>([]);

    const previewSrc = $derived(previewUrl ?? currentPictureUrl);

    async function load(): Promise<void> {
        const user = await fetchCurrentUser();

        if (!user || !user.is_authenticated) {
            throw new Error("You are not signed in. Please log in to edit your profile.");
        }

        username = user.username;
        firstName = user.first_name ?? "";
        lastName = user.last_name ?? "";
        description = user.description ?? "";
        email = user.email ?? "";
        originalEmail = user.email ?? "";
        currentPictureUrl = user.picture ?? null;

        // E-mail list is informational; ignore failures (allauth optional).
        emails = await fetchEmailAddresses().catch(() => []);
    }

    onMount(() => {
        load()
            .catch((error: unknown) => {
                errorMessage = error instanceof Error ? error.message : String(error);
            })
            .finally(() => {
                isLoading = false;
            });
    });

    onDestroy(() => {
        if (previewUrl) {
            URL.revokeObjectURL(previewUrl);
        }
    });

    function onPickFile(event: Event): void {
        const input = event.currentTarget as HTMLInputElement;
        const file = input.files?.[0] ?? null;

        if (previewUrl) {
            URL.revokeObjectURL(previewUrl);
        }

        pictureFile = file;
        previewUrl = file ? URL.createObjectURL(file) : null;
    }

    async function save(): Promise<void> {
        if (!username || isSaving) {
            return;
        }

        isSaving = true;
        errorMessage = "";
        successMessage = "";

        try {
            await saveProfile(username, {firstName, lastName, description}, pictureFile);

            let message = "Profile saved.";

            if (email && email !== originalEmail) {
                await requestEmailChange(email);
                message += " A verification link was sent to the new e-mail address.";
            }

            if (previewUrl) {
                URL.revokeObjectURL(previewUrl);
            }

            pictureFile = null;
            previewUrl = null;
            await dashboardStore.refresh();
            await load();

            successMessage = message;
        } catch (error) {
            errorMessage = error instanceof Error ? error.message : String(error);
        } finally {
            isSaving = false;
        }
    }
</script>

<div class="profile">
    <header class="head">
        <h1 class="title">Edit Profile</h1>
        <button type="button" class="btn btn-ghost btn-sm" onclick={() => push("/")}>← Back to Dashboard</button>
    </header>

    {#if isLoading}
        <div class="status-box" role="status" aria-live="polite">
            <span class="loading loading-spinner loading-lg"></span>
            <p>Loading your profile…</p>
        </div>
    {:else if errorMessage && !username}
        <div class="status-box" role="alert">
            <p class="error">{errorMessage}</p>
        </div>
    {:else}
        <form class="card form" onsubmit={(event) => {event.preventDefault(); save();}}>
            <div class="avatar-row">
                <span class="avatar-mark" aria-hidden="true">
                    {#if previewSrc}
                        <img src={previewSrc} alt="" />
                    {/if}
                </span>
                <div class="avatar-actions">
                    <label class="field-label" for="picture">Profile picture</label>
                    <input id="picture" class="file-input file-input-bordered file-input-sm" type="file" accept="image/*" onchange={onPickFile} />
                </div>
            </div>

            <label class="field">
                <span class="field-label">Username</span>
                <input class="input input-bordered" type="text" value={username} readonly />
                <span class="hint">Username cannot be changed.</span>
            </label>

            <div class="two-col">
                <label class="field">
                    <span class="field-label">First name</span>
                    <input class="input input-bordered" type="text" bind:value={firstName} autocomplete="given-name" />
                </label>
                <label class="field">
                    <span class="field-label">Last name</span>
                    <input class="input input-bordered" type="text" bind:value={lastName} autocomplete="family-name" />
                </label>
            </div>

            <label class="field">
                <span class="field-label">Description</span>
                <textarea class="textarea textarea-bordered" rows="4" bind:value={description}></textarea>
            </label>

            <label class="field">
                <span class="field-label">E-mail</span>
                <input class="input input-bordered" type="email" bind:value={email} autocomplete="email" />
                <span class="hint">Changing your e-mail sends a verification link; it activates after you confirm.</span>
            </label>

            {#if emails.length > 0}
                <ul class="email-list">
                    {#each emails as entry (entry.email)}
                        <li>
                            {entry.email}
                            <span class="badge badge-sm {entry.verified ? 'badge-success' : 'badge-warning'}">
                                {entry.verified ? "verified" : "unverified"}
                            </span>
                            {#if entry.primary}<span class="badge badge-sm badge-primary">primary</span>{/if}
                        </li>
                    {/each}
                </ul>
            {/if}

            {#if errorMessage}
                <p class="error" role="alert">{errorMessage}</p>
            {/if}
            {#if successMessage}
                <p class="success" role="status">{successMessage}</p>
            {/if}

            <div class="actions">
                <button type="submit" class="btn btn-primary" disabled={isSaving}>
                    {#if isSaving}<span class="loading loading-spinner loading-sm"></span>{/if}
                    Save changes
                </button>
            </div>
        </form>
    {/if}
</div>

<style>
    .profile {
        flex: 1;
        min-height: 0;
        overflow-y: auto;
        max-width: 42rem;
        width: 100%;
        margin: 0 auto;
        padding: 2rem 1.5rem 1rem;
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
    }

    .head {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
    }

    .title {
        font-size: 1.6rem;
        font-weight: 800;
        color: var(--color-base-content);
    }

    .form {
        background: var(--color-base-100);
        border-radius: 1rem;
        padding: 1.5rem;
        display: flex;
        flex-direction: column;
        gap: 1.1rem;
        box-shadow: 0 0 24px color-mix(in oklab, var(--color-primary) 10%, transparent);
    }

    .avatar-row {
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    .avatar-mark {
        width: 4rem;
        height: 4rem;
        flex: 0 0 auto;
        border-radius: 999px;
        overflow: hidden;
        background: color-mix(in oklab, var(--color-base-content) 18%, transparent);
        box-shadow: 0 0 16px color-mix(in oklab, var(--color-primary) 30%, transparent);
    }

    .avatar-mark img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    .avatar-actions {
        display: flex;
        flex-direction: column;
        gap: 0.35rem;
    }

    .field {
        display: flex;
        flex-direction: column;
        gap: 0.35rem;
    }

    .field-label {
        font-size: 0.85rem;
        font-weight: 600;
        color: color-mix(in oklab, var(--color-base-content) 80%, transparent);
    }

    .two-col {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
    }

    .hint {
        font-size: 0.75rem;
        color: color-mix(in oklab, var(--color-base-content) 60%, transparent);
    }

    .email-list {
        list-style: none;
        margin: 0;
        padding: 0;
        display: flex;
        flex-direction: column;
        gap: 0.35rem;
        font-size: 0.85rem;
        color: var(--color-base-content);
    }

    .email-list li {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .error {
        color: var(--color-error);
        font-weight: 600;
    }

    .success {
        color: var(--color-success);
        font-weight: 600;
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

    .actions {
        display: flex;
        justify-content: flex-end;
    }

    @media (max-width: 40rem) {
        .two-col {
            grid-template-columns: 1fr;
        }
    }
</style>
