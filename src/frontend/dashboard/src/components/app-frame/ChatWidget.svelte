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
Global "Quick Chat" widget with three states:
  - minimised: a floating robot icon (FAB) bottom-right;
  - floating:  a small draggable chat window;
  - sidebar:   a docked, full-height panel on the right (via the expand button).

Chat runs over the WebSocket API (channel /ws/ai/chat) via the shared ai-chat
store; it connects lazily the first time the panel is opened. See
README-websocket-api.md.
-->
<script lang="ts">
    import {onMount} from "svelte";
    import {createAiChatStore} from "../../stores/ai-chat.store.js";
    import type {AiChatState} from "../../stores/ai-chat.store.js";
    import {renderMarkdown} from "../../data/markdown.js";

    type Mode = "floating" | "sidebar";

    // Notifies the shell whether the chat is currently docked as a sidebar, so
    // the page content can make room for it.
    let {onSidebarChange}: {onSidebarChange?: (docked: boolean) => void} = $props();

    let open = $state(false);
    let mode = $state<Mode>("floating");
    let pos = $state<{x: number; y: number} | null>(null);

    let dragOffset: {x: number; y: number} | null = null;

    // AI chat over WebSocket; connect lazily the first time the panel is opened.
    const chat = createAiChatStore();
    let chatState = $state<AiChatState>({
        connection: "disconnected",
        errorMessage: "",
        messages: [],
        sessions: [],
        activeSessionId: null,
    });
    let draft = $state("");
    let connectStarted = false;

    const connected = $derived(chatState.connection === "connected");

    function ensureConnected(): void {
        if (!connectStarted) {
            connectStarted = true;
            void chat.connect();
        }
    }

    async function send(): Promise<void> {
        const text = draft.trim();
        if (!text || !connected) {
            return;
        }

        draft = "";
        await chat.sendChatInput("markdown", text);
    }

    function notify(): void {
        onSidebarChange?.(open && mode === "sidebar");
    }

    onMount(() => {
        // Sync the shell on mount (e.g. after returning from the full chat page).
        notify();
        const unsubscribe = chat.subscribe((value) => {
            chatState = value;
        });
        return () => {
            unsubscribe();
            void chat.disconnect();
        };
    });

    function toggle(): void {
        open = !open;
        if (open) {
            ensureConnected();
        }
        notify();
    }

    function close(): void {
        open = false;
        notify();
    }

    function toggleMode(): void {
        // Expand -> dock as a full-height sidebar; collapse -> floating window.
        mode = mode === "floating" ? "sidebar" : "floating";
        pos = null;
        notify();
    }

    function onPointerMove(event: PointerEvent): void {
        if (!dragOffset) {
            return;
        }

        const maxX = Math.max(0, window.innerWidth - 360);
        const maxY = Math.max(0, window.innerHeight - 120);
        pos = {
            x: Math.min(Math.max(0, event.clientX - dragOffset.x), maxX),
            y: Math.min(Math.max(0, event.clientY - dragOffset.y), maxY),
        };
    }

    function onPointerUp(): void {
        dragOffset = null;
        window.removeEventListener("pointermove", onPointerMove);
        window.removeEventListener("pointerup", onPointerUp);
    }

    function startDrag(event: PointerEvent): void {
        // Only the floating window can be dragged.
        if (mode !== "floating") {
            return;
        }

        const panel = (event.currentTarget as HTMLElement).parentElement;
        if (!panel) {
            return;
        }

        const rect = panel.getBoundingClientRect();
        dragOffset = {x: event.clientX - rect.left, y: event.clientY - rect.top};
        pos = {x: rect.left, y: rect.top};
        window.addEventListener("pointermove", onPointerMove);
        window.addEventListener("pointerup", onPointerUp);
    }
</script>

{#if open}
    <section
        class="panel"
        class:floating={mode === "floating"}
        class:sidebar={mode === "sidebar"}
        style={mode === "floating" && pos ? `left:${pos.x}px; top:${pos.y}px; right:auto; bottom:auto;` : ""}
    >
        <header class="panel-header" role="toolbar" tabindex="-1" aria-label="Chat window controls" onpointerdown={startDrag}>
            <span class="panel-title">{mode === "sidebar" ? "Quiz Chat" : "Quick Chat"}</span>
            <div class="panel-actions">
                <button
                    type="button"
                    class="icon-btn"
                    aria-label={mode === "sidebar" ? "Float chat" : "Dock chat to sidebar"}
                    onclick={toggleMode}
                >
                    {mode === "sidebar" ? "↙" : "↗"}
                </button>
                <button type="button" class="icon-btn" aria-label="Close chat" onclick={close}>✕</button>
            </div>
        </header>

        <div class="panel-body">
            <div class="message">
                <img class="avatar" src="logo.png" alt="ElisaAI" />
                <div class="bubble">
                    System online. I am <strong>ElisaAI</strong>. Ready to process your queries.
                    What topic shall we analyse today?
                </div>
            </div>

            {#each chatState.messages as message (message.id)}
                <div class="message" class:user={message.sender === "user"}>
                    {#if message.sender === "assistant"}
                        <img class="avatar" src="logo.png" alt="ElisaAI" />
                    {/if}
                    {#if message.format === "markdown"}
                        <!-- eslint-disable-next-line svelte/no-at-html-tags -->
                        <div class="bubble md" class:user={message.sender === "user"}>{@html renderMarkdown(message.content)}</div>
                    {:else}
                        <div class="bubble" class:user={message.sender === "user"}>{message.content}</div>
                    {/if}
                </div>
            {/each}
        </div>

        <div class="composer">
            {#if !connected}
                <span class="coming-soon">{chatState.connection === "connecting" ? "Connecting…" : "Offline — reconnecting…"}</span>
            {/if}
            <form class="composer-row" onsubmit={(event) => {event.preventDefault(); send();}}>
                <button type="button" class="composer-add" aria-label="Add" disabled>+</button>
                <input
                    class="composer-input"
                    type="text"
                    placeholder="Message"
                    bind:value={draft}
                    disabled={!connected}
                />
                <button
                    type="submit"
                    class="composer-send"
                    aria-label="Send"
                    disabled={!connected || draft.trim().length === 0}
                >→</button>
            </form>
            <p class="disclaimer">ElisaAI may generate misinformation. Please verify all information.</p>
        </div>
    </section>
{/if}

<button type="button" class="fab" class:hidden={open} aria-label="Open Quick Chat" onclick={toggle}>
    <img src="logo.png" alt="" />
</button>

<style>
    .fab {
        position: fixed;
        right: 1.5rem;
        bottom: 1.5rem;
        z-index: 60;
        width: 3.75rem;
        height: 3.75rem;
        border-radius: 999px;
        padding: 0;
        border: 2px solid color-mix(in oklab, var(--color-primary) 60%, transparent);
        background: var(--color-base-100);
        cursor: pointer;
        overflow: hidden;
        box-shadow: 0 0 22px color-mix(in oklab, var(--color-primary) 45%, transparent);
        transition: transform 0.15s ease;
    }

    .fab:hover {
        transform: scale(1.06);
    }

    .fab.hidden {
        display: none;
    }

    .fab img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        /* Mirror the robot so it faces the other way — only on the closed launcher
           (the in-panel .avatar images keep their original orientation). */
        transform: scaleX(-1);
    }

    .panel {
        position: fixed;
        z-index: 61;
        display: flex;
        flex-direction: column;
        background: var(--color-base-100);
        border: 1px solid color-mix(in oklab, var(--color-primary) 30%, transparent);
        box-shadow: 0 0 32px color-mix(in oklab, var(--color-primary) 30%, transparent);
        overflow: hidden;
    }

    .panel.floating {
        right: 1.5rem;
        bottom: 1.5rem;
        width: 22.5rem;
        height: 32rem;
        max-width: calc(100vw - 2rem);
        max-height: calc(100vh - 2rem);
        border-radius: 1.25rem;
    }

    /* Docked, full-height sidebar (expand). */
    .panel.sidebar {
        top: 0;
        right: 0;
        bottom: 0;
        width: min(28rem, 100vw);
        height: 100vh;
        border-radius: 0;
        border: none;
        border-left: 1px solid color-mix(in oklab, var(--color-primary) 30%, transparent);
    }

    .panel-header {
        flex: 0 0 auto;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
        padding: 0.75rem 1rem;
        border-bottom: 1px solid color-mix(in oklab, var(--color-base-content) 10%, transparent);
    }

    .panel.floating .panel-header {
        cursor: grab;
    }

    .panel.floating .panel-header:active {
        cursor: grabbing;
    }

    .panel-title {
        font-weight: 700;
        letter-spacing: 0.03em;
        color: var(--color-base-content);
    }

    .panel-actions {
        display: flex;
        gap: 0.35rem;
    }

    .icon-btn {
        display: grid;
        place-items: center;
        width: 1.75rem;
        height: 1.75rem;
        border-radius: 0.5rem;
        border: none;
        background: transparent;
        color: color-mix(in oklab, var(--color-base-content) 70%, transparent);
        cursor: pointer;
    }

    .icon-btn:hover {
        background: color-mix(in oklab, var(--color-base-content) 10%, transparent);
        color: var(--color-base-content);
    }

    .panel-body {
        flex: 1;
        min-height: 0;
        overflow-y: auto;
        padding: 1rem;
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
    }

    .message {
        display: flex;
        align-items: flex-start;
        gap: 0.6rem;
    }

    .message.user {
        justify-content: flex-end;
    }

    .avatar {
        width: 2.25rem;
        height: 2.25rem;
        flex: 0 0 auto;
        border-radius: 999px;
        object-fit: cover;
    }

    .bubble {
        padding: 0.75rem 0.9rem;
        border-radius: 0.9rem;
        border-top-left-radius: 0.25rem;
        line-height: 1.5;
        color: var(--color-base-content);
        background: color-mix(in oklab, var(--color-primary) 12%, transparent);
        border: 1px solid color-mix(in oklab, var(--color-primary) 28%, transparent);
    }

    /* Rendered Markdown content inside a chat bubble. */
    .bubble.md :global(:first-child) {
        margin-top: 0;
    }

    .bubble.md :global(:last-child) {
        margin-bottom: 0;
    }

    .bubble.md :global(h1),
    .bubble.md :global(h2),
    .bubble.md :global(h3) {
        font-weight: 700;
        line-height: 1.3;
        margin: 0.8rem 0 0.35rem;
    }

    .bubble.md :global(h1) { font-size: 1.15rem; }
    .bubble.md :global(h2) { font-size: 1.05rem; }
    .bubble.md :global(h3) { font-size: 1rem; }

    .bubble.md :global(p) {
        margin: 0.45rem 0;
    }

    .bubble.md :global(ul),
    .bubble.md :global(ol) {
        margin: 0.45rem 0 0.45rem 1.3rem;
    }

    .bubble.md :global(li) {
        margin: 0.15rem 0;
    }

    .bubble.md :global(a) {
        color: var(--color-primary);
        text-decoration: underline;
    }

    .bubble.md :global(code) {
        font-family: ui-monospace, "SF Mono", Menlo, Monaco, monospace;
        font-size: 0.85em;
        padding: 0.1rem 0.3rem;
        border-radius: 0.3rem;
        background: color-mix(in oklab, var(--color-base-content) 12%, transparent);
    }

    .bubble.md :global(pre) {
        margin: 0.5rem 0;
        padding: 0.7rem 0.85rem;
        border-radius: 0.5rem;
        overflow-x: auto;
        background: color-mix(in oklab, var(--color-base-content) 12%, transparent);
        border: 1px solid color-mix(in oklab, var(--color-base-content) 14%, transparent);
    }

    .bubble.md :global(pre code) {
        padding: 0;
        background: none;
        font-size: 0.8rem;
    }

    .bubble.md :global(blockquote) {
        margin: 0.5rem 0;
        padding: 0.25rem 0.8rem;
        border-left: 3px solid var(--color-primary);
        background: color-mix(in oklab, var(--color-primary) 10%, transparent);
    }

    .composer {
        flex: 0 0 auto;
        display: flex;
        flex-direction: column;
        gap: 0.4rem;
        padding: 0.75rem;
        border-top: 1px solid color-mix(in oklab, var(--color-base-content) 10%, transparent);
    }

    .coming-soon {
        align-self: center;
        font-size: 0.7rem;
        color: var(--color-warning);
    }

    .composer-row {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.35rem 0.5rem;
        border-radius: 999px;
        background: color-mix(in oklab, var(--color-base-200) 80%, transparent);
        border: 1px solid color-mix(in oklab, var(--color-primary) 30%, transparent);
    }

    .composer-add,
    .composer-send {
        display: grid;
        place-items: center;
        width: 1.9rem;
        height: 1.9rem;
        flex: 0 0 auto;
        border-radius: 999px;
        border: none;
        cursor: not-allowed;
        color: var(--color-primary-content);
        background: color-mix(in oklab, var(--color-primary) 70%, transparent);
    }

    .composer-input {
        flex: 1 1 auto;
        background: transparent;
        border: none;
        color: var(--color-base-content);
        padding: 0.25rem;
    }

    .composer-input:focus {
        outline: none;
    }

    .disclaimer {
        text-align: center;
        font-size: 0.65rem;
        color: color-mix(in oklab, var(--color-base-content) 55%, transparent);
    }
</style>
