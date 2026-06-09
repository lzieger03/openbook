<!--
OpenBook: Interactive Online Textbooks
© 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.
-->

<!--
@component
Reusable shell for full-height chat side panes with semantic header and footer slots.
-->

<script lang="ts">
    import type {Snippet} from "svelte";
    import { i18n }       from "../../stores/i18n.js";

    interface Props {
        class?:    string;
        header?:   Snippet;
        footer?:   Snippet;
        children?: Snippet;
    }

    let {
        class: className = "",
        header,
        footer,
        children,
    }: Props = $props();

    const panelClass = $derived([
        "flex",
        "h-full",
        "min-h-0",
        "w-full",
        "flex-col",
        "overflow-hidden",
        "bg-base-200/70",
        className,
    ].filter(Boolean).join(" "));
</script>

<section class={panelClass} aria-label={$i18n.AiChat.PanelAriaLabel}>
    {#if header}
        <header class="border-b border-base-300/80 bg-base-100/90 px-5 py-4 backdrop-blur-sm">
            {@render header()}
        </header>
    {/if}

    <div class="flex min-h-0 flex-1 flex-col">
        {@render children?.()}
    </div>

    {#if footer}
        <footer class="border-t border-base-300/80 bg-base-100/92 p-4 backdrop-blur-sm">
            {@render footer()}
        </footer>
    {/if}
</section>
