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
Semantic header wrapper for the leading content of a DaisyUI card.
-->

<script lang="ts">
    import type {Snippet} from "svelte";

    interface Props {
        class?:    string;
        children?: Snippet;
    }

    let {
        class: className = "",
        children,
        ...props
    }: Props = $props();

    const headerClass = $derived([
        "flex",
        "flex-col",
        "gap-2",
        className,
    ].filter(Boolean).join(" "));
</script>

<div class={headerClass} {...props}>
    {@render children?.()}
</div>
