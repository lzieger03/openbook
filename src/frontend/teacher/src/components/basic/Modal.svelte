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
Lightweight dialog built on the DaisyUI modal classes. Shown when `open` is true;
closing is delegated to the parent via `onClose` so it stays a controlled component.
-->
<script lang="ts">
    import type {Snippet} from "svelte";

    let {
        open = false,
        title = "",
        onClose,
        children,
        actions,
    }: {
        open?: boolean;
        title?: string;
        onClose: () => void;
        children: Snippet;
        actions?: Snippet;
    } = $props();
</script>

{#if open}
    <div class="modal modal-open" role="dialog" aria-modal="true">
        <div class="modal-box">
            {#if title}
                <h3 class="text-lg font-bold">{title}</h3>
            {/if}

            <div class="py-4">
                {@render children()}
            </div>

            <div class="modal-action">
                {#if actions}
                    {@render actions()}
                {:else}
                    <button type="button" class="btn" onclick={onClose}>Close</button>
                {/if}
            </div>
        </div>
        <button
            type="button"
            class="modal-backdrop"
            aria-label="Close dialog"
            onclick={onClose}
        ></button>
    </div>
{/if}
