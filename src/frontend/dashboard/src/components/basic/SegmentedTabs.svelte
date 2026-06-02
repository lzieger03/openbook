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
Segmented tab row. Tabs not equal to the active one can be disabled (v1 only
wires the "Current" tab; the others are inert placeholders).
-->
<script lang="ts">
    let {
        tabs,
        active,
        disabledTabs = [],
        onSelect,
    }: {
        tabs: readonly string[];
        active: string;
        disabledTabs?: readonly string[];
        onSelect?: (tab: string) => void;
    } = $props();
</script>

<div role="tablist" class="seg-tabs" aria-label="Learning views">
    {#each tabs as tab (tab)}
        <button
            type="button"
            role="tab"
            class="seg-tab"
            class:active={tab === active}
            aria-selected={tab === active}
            disabled={disabledTabs.includes(tab)}
            onclick={() => onSelect?.(tab)}
        >
            {tab}
        </button>
    {/each}
</div>

<style>
    .seg-tabs {
        display: inline-flex;
        gap: 0.25rem;
    }

    .seg-tab {
        padding: 0.25rem 0.75rem;
        border-radius: 0.5rem;
        font-size: 0.85rem;
        font-weight: 600;
        letter-spacing: 0.04em;
        color: color-mix(in oklab, var(--color-base-content) 65%, transparent);
        background: transparent;
        cursor: pointer;
    }

    .seg-tab:hover:not(:disabled) {
        color: var(--color-base-content);
    }

    .seg-tab.active {
        color: var(--color-primary);
        background: color-mix(in oklab, var(--color-primary) 16%, transparent);
    }

    .seg-tab:disabled {
        cursor: not-allowed;
        opacity: 0.45;
    }

    .seg-tab:focus-visible {
        outline: 2px solid var(--color-primary);
        outline-offset: 2px;
    }
</style>
