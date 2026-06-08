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
Render markdown chat content as sanitized HTML with chat-specific typography.
-->

<script lang="ts">
    import MarkdownIt from "markdown-it";

    type ChatMarkdownTone = "assistant" | "user" | "muted";

    interface Props {
        class?: string;
        content?: string;
        tone?: ChatMarkdownTone;
    }

    const markdownRenderer = new MarkdownIt({
        breaks:      true,
        html:        false,
        linkify:     true,
        typographer: true,
    });

    let {
        class: className = "",
        content = "",
        tone    = "assistant",
    }: Props = $props();

    const rootClass = $derived([
        "chat-markdown",
        "max-w-none",
        "text-sm",
        "leading-6",
        "sm:text-[0.95rem]",
        tone === "user" ? "chat-markdown-user text-primary-content" : "text-base-content",
        tone === "muted" && "text-base-content/80",
        className,
    ].filter(Boolean).join(" "));

    const contentHtml = $derived(markdownRenderer.render(content));
</script>

<div class={rootClass}>
    {@html contentHtml}
</div>

<style>
    .chat-markdown :global(*) {
        overflow-wrap: anywhere;
    }

    .chat-markdown :global(> :first-child) {
        margin-top: 0;
    }

    .chat-markdown :global(> :last-child) {
        margin-bottom: 0;
    }

    .chat-markdown :global(p),
    .chat-markdown :global(ul),
    .chat-markdown :global(ol),
    .chat-markdown :global(pre),
    .chat-markdown :global(blockquote),
    .chat-markdown :global(table),
    .chat-markdown :global(h1),
    .chat-markdown :global(h2),
    .chat-markdown :global(h3),
    .chat-markdown :global(h4) {
        margin: 0.75rem 0;
    }

    .chat-markdown :global(ul),
    .chat-markdown :global(ol) {
        padding-left: 1.25rem;
    }

    .chat-markdown :global(li + li) {
        margin-top: 0.25rem;
    }

    .chat-markdown :global(a) {
        text-decoration: underline;
        text-underline-offset: 0.2em;
    }

    .chat-markdown :global(code) {
        border-radius: 0.5rem;
        background: color-mix(in srgb, var(--color-base-300) 60%, transparent);
        padding: 0.15rem 0.4rem;
        font-size: 0.9em;
    }

    .chat-markdown :global(pre) {
        overflow-x: auto;
        border-radius: 1rem;
        background: color-mix(in srgb, var(--color-base-300) 55%, transparent);
        padding: 0.875rem 1rem;
    }

    .chat-markdown :global(pre code) {
        background: transparent;
        padding: 0;
    }

    .chat-markdown :global(blockquote) {
        border-left: 3px solid color-mix(in srgb, var(--color-primary) 35%, transparent);
        padding-left: 0.875rem;
        opacity: 0.9;
    }

    .chat-markdown-user :global(a) {
        color: inherit;
    }

    .chat-markdown-user :global(code) {
        background: color-mix(in srgb, var(--color-primary-content) 18%, transparent);
    }

    .chat-markdown-user :global(pre) {
        background: color-mix(in srgb, var(--color-primary-content) 12%, transparent);
    }

    .chat-markdown-user :global(blockquote) {
        border-left-color: color-mix(in srgb, var(--color-primary-content) 40%, transparent);
    }
</style>
