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
Reusable DaisyUI card wrapper with configurable visual variants.
-->

<script lang="ts">
    import type {Snippet} from "svelte";

    type CardVariant = "default" | "bordered" | "elevated" | "compact";

    interface Props {
        class?:    string;
        variant?:  CardVariant;
        children?: Snippet;
    }

    let {
        class: className = "",
        variant = "default",
        children,
        ...props
    }: Props = $props();

    const variantClassMap: Record<CardVariant, string[]> = {
        default:  ["border", "border-base-300", "bg-base-100", "shadow-sm"],
        bordered: ["border-2", "border-base-300", "bg-base-100", "shadow-sm"],
        elevated: ["bg-base-100", "shadow-xl"],
        compact:  ["card-compact", "border", "border-base-300", "bg-base-100", "shadow-sm"],
    };

    const cardClass = $derived([
        "card",
        ...variantClassMap[variant],
        className,
    ].filter(Boolean).join(" "));
</script>

<div class={cardClass} {...props}>
    {@render children?.()}
</div>
