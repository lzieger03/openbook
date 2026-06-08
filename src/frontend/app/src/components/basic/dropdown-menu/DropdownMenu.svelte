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
Semantic dropdown menu wrapper based on DaisyUI classes.

TODO: Implement keyboard navigation with arrow keys
-->

<script lang="ts">
    import type {Snippet} from "svelte";

    type Align    = "start" | "end";
    type Side     = "top" | "bottom" | "left" | "right";
    type MenuSize = "" | "sm" | "md" | "lg";

    const ALIGN_CLASSES: Record<Align, string> = {
        start: "dropdown-start",
        end:   "dropdown-end",
    };

    const SIDE_CLASSES: Record<Side, string> = {
        top:    "dropdown-top",
        bottom: "dropdown-bottom",
        left:   "dropdown-left",
        right:  "dropdown-right",
    };

    interface Props {
        class?:          string;
        align?:          Align;
        side?:           Side;
        open?:           boolean;
        hover?:          boolean;
        menuHorizontal?: boolean;
        menuSize?:       MenuSize;
        triggerClass?:   string;
        contentClass?:   string;
        contentRole?:    string;
        trigger?:        Snippet;
        children?:       Snippet;
    }

    let {
        align,
        side,
        open,
        hover            = false,
        menuHorizontal   = false,
        menuSize         = "",
        triggerClass     = "",
        contentClass     = "",
        contentRole      = "menu",
        class: className = "",
        trigger,
        children,
    }: Props = $props();

    const parentClasses = $derived(
        [
            "dropdown",
            align ? ALIGN_CLASSES[align] : "",
            side  ? SIDE_CLASSES[side]   : "",
            hover ? "dropdown-hover"     : "",
            className,
        ].filter(Boolean).join(" ")
    );

    const triggerClasses = $derived(
        [
            triggerClass,
        ].filter(Boolean).join(" ")
    );

    const contentClasses = $derived(
        [
            "dropdown-content",
            "menu",
            menuSize       ? `menu-${menuSize}` : "",
            menuHorizontal ? "menu-horizontal"  : "",
            contentClass,
        ].filter(Boolean).join(" ")
    );
</script>

<details class={parentClasses} {open}>
    <summary class={triggerClasses}>
        {@render trigger?.()}
    </summary>

    <ul class={contentClasses} role={contentRole}>
        {@render children?.()}
    </ul>
</details>
