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
Semantic subtitle wrapper for DaisyUI card headers.
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

    const subtitleClass = $derived([
        "text-sm",
        "text-base-content/70",
        className,
    ].filter(Boolean).join(" "));
</script>

<p class={subtitleClass} {...props}>
    {@render children?.()}
</p>
