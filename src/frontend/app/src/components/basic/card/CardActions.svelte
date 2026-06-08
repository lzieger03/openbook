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
Semantic wrapper for DaisyUI card actions.
-->

<script lang="ts">
    import type {Snippet} from "svelte";

    interface Props {
        class?: string;
        justify?: "start" | "center" | "end" | "between";
        children?: Snippet;
    }

    let {
        class: className = "",
        justify = "end",
        children,
        ...props
    }: Props = $props();

    const justifyClassMap = {
        start: "justify-start",
        center: "justify-center",
        end: "justify-end",
        between: "justify-between",
    };

    const actionsClass = $derived([
        "card-actions",
        justifyClassMap[justify],
        className,
    ].filter(Boolean).join(" "));
</script>

<div class={actionsClass} {...props}>
    {@render children?.()}
</div>
