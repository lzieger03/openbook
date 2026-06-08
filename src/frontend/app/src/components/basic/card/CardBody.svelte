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
Semantic content wrapper for the body section of a DaisyUI card.
-->

<script lang="ts">
    import type {Snippet} from "svelte";

    interface Props {
        class?:    string;
        compact?:  boolean;
        children?: Snippet;
    }

    let {
        class: className = "",
        compact = false,
        children,
        ...props
    }: Props = $props();

    const bodyClass = $derived([
        "card-body",
        compact && "p-4",
        className
    ].filter(Boolean).join(" "));
</script>

<div class={bodyClass} {...props}>
    {@render children?.()}
</div>
