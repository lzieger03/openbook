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
A learning list row: round icon, label, and a chevron action button.
-->
<script lang="ts">
    let {label, iconPath = "", onOpen}: {label: string; iconPath?: string; onOpen?: () => void} = $props();

    const initial = $derived(label.trim().charAt(0).toUpperCase() || "?");
</script>

<div class="learning-row">
    <span class="row-icon" aria-hidden="true">
        {#if iconPath}
            <img src={iconPath} alt="" />
        {:else}
            {initial}
        {/if}
    </span>

    <span class="row-label">{label}</span>

    <button
        type="button"
        class="btn btn-circle btn-sm btn-primary row-action"
        aria-label={`Open ${label}`}
        onclick={() => onOpen?.()}
    >
        ›
    </button>
</div>

<style>
    .learning-row {
        display: flex;
        align-items: center;
        gap: 0.85rem;
        padding: 0.6rem 0.25rem;
    }

    .row-icon {
        display: grid;
        place-items: center;
        width: 2.5rem;
        height: 2.5rem;
        flex: 0 0 auto;
        border-radius: 999px;
        font-weight: 700;
        color: var(--color-primary-content);
        background: color-mix(in oklab, var(--color-primary) 70%, transparent);
        box-shadow: 0 0 12px color-mix(in oklab, var(--color-primary) 40%, transparent);
        overflow: hidden;
    }

    .row-icon img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    .row-label {
        flex: 1 1 auto;
        color: var(--color-base-content);
    }

    .row-action {
        flex: 0 0 auto;
    }
</style>
