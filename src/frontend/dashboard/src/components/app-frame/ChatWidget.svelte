<!--
OpenBook: Interactive Online Textbooks - Server
© 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
Ledejna Salihi (@LedejnaSalihi)
Lars Zieger (@lzieger03)

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
    import type {AiChatState, ChatSessionSummary} from "../../stores/ai-chat.store.js";
    import {renderMarkdown} from "../../data/markdown.js";
    import {pageContext, formatPageContext} from "../../stores/page-context.store.js";
    import type {PageContext} from "../../stores/page-context.store.js";

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
        awaitingResponse: false,
    });
    let draft = $state("");
    let connectStarted = false;
    // The scrollable message area; kept pinned to the bottom on new content.
    let bodyEl = $state<HTMLDivElement>();

    // Whether the chat-history (sessions) panel is shown instead of the conversation.
    let showHistory = $state(false);

    // What the user is currently looking at, sent to the assistant as context.
    let currentContext = $state<PageContext | null>(null);

    const connected = $derived(chatState.connection === "connected");

    // Auto-scroll to the latest message / typing indicator whenever they change.
    $effect(() => {
        void chatState.messages.length;
        void chatState.awaitingResponse;

        const el = bodyEl;
        if (el) {
            requestAnimationFrame(() => {
                el.scrollTop = el.scrollHeight;
            });
        }
    });

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
        await chat.sendChatInput("markdown", text, formatPageContext(currentContext));
    }

    function onNewChat(): void {
        void chat.newChat();
        showHistory = false;
    }

    function onOpenSession(sessionId: string): void {
        if (sessionId !== chatState.activeSessionId) {
            void chat.openSession(sessionId);
        }
        showHistory = false;
    }

    function onDeleteSession(session: ChatSessionSummary): void {
        if (confirm(`Delete the chat “${session.title}”? This cannot be undone.`)) {
            void chat.deleteSession(session.id);
        }
    }

    /** Compact "x min ago" style timestamp for the history list. */
    function formatRelative(iso: string): string {
        const then = new Date(iso).getTime();
        if (Number.isNaN(then)) {
            return "";
        }
        const seconds = Math.round((Date.now() - then) / 1000);
        if (seconds < 60) return "just now";
        const minutes = Math.round(seconds / 60);
        if (minutes < 60) return `${minutes}m ago`;
        const hours = Math.round(minutes / 60);
        if (hours < 24) return `${hours}h ago`;
        const days = Math.round(hours / 24);
        if (days < 7) return `${days}d ago`;
        return new Date(iso).toLocaleDateString();
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
        const unsubscribeContext = pageContext.subscribe((value) => {
            currentContext = value;
        });
        return () => {
            unsubscribe();
            unsubscribeContext();
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
                    class:active={showHistory}
                    aria-label="Chat history"
                    aria-pressed={showHistory}
                    title="Chat history"
                    onclick={() => (showHistory = !showHistory)}
                >
                    <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                        <circle cx="12" cy="12" r="9" />
                        <path d="M12 7.5V12l3 2" />
                    </svg>
                </button>
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

        {#if showHistory}
            <div class="panel-body history">
                <div class="history-head">
                    <span class="history-title-label">Chat history</span>
                    <button type="button" class="new-chat" onclick={onNewChat}>+ New chat</button>
                </div>

                {#if chatState.sessions.length === 0}
                    <p class="history-empty">No saved chats yet. Send a message to start one.</p>
                {:else}
                    <ul class="history-list">
                        {#each chatState.sessions as session (session.id)}
                            <li class="history-row" class:active={session.id === chatState.activeSessionId}>
                                <button type="button" class="history-open" onclick={() => onOpenSession(session.id)} title={session.title}>
                                    <span class="history-name">{session.title}</span>
                                    <span class="history-time">{formatRelative(session.updated_at)}</span>
                                </button>
                                <button type="button" class="history-action" aria-label="Delete chat" title="Delete" onclick={() => onDeleteSession(session)}>✕</button>
                            </li>
                        {/each}
                    </ul>
                {/if}
            </div>
        {:else}
        <div class="panel-body" bind:this={bodyEl}>
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

            {#if chatState.awaitingResponse}
                <div class="message" aria-live="polite">
                    <img class="avatar" src="logo.png" alt="ElisaAI" />
                    <div class="bubble typing" aria-label="ElisaAI is typing">
                        <span class="typing-dot"></span>
                        <span class="typing-dot"></span>
                        <span class="typing-dot"></span>
                    </div>
                </div>
            {/if}
        </div>
        {/if}

        {#if !showHistory}
        <div class="composer">
            {#if !connected}
                <span class="coming-soon">{chatState.connection === "connecting" ? "Connecting…" : "Offline — reconnecting…"}</span>
            {/if}
            {#if currentContext && connected}
                <span class="context-chip" title={currentContext.label}>
                    <svg class="context-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                        <path d="M14 3v4a1 1 0 0 0 1 1h4" />
                        <path d="M5 3h9l5 5v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2z" />
                    </svg>
                    Using the current page as context
                </span>
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
        {/if}
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

    .icon-btn.active {
        background: color-mix(in oklab, var(--color-primary) 16%, transparent);
        color: var(--color-primary);
    }

    .icon-btn .icon {
        width: 1.05rem;
        height: 1.05rem;
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

    /* --- Chat history (clock icon) ------------------------------------- */

    .panel-body.history {
        gap: 0.4rem;
    }

    .history-head {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 0.5rem;
        padding-bottom: 0.4rem;
    }

    .history-title-label {
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: color-mix(in oklab, var(--color-base-content) 55%, transparent);
    }

    .new-chat {
        font-size: 0.78rem;
        font-weight: 600;
        padding: 0.25rem 0.6rem;
        border-radius: 999px;
        cursor: pointer;
        color: var(--color-primary);
        background: color-mix(in oklab, var(--color-primary) 12%, transparent);
        border: 1px solid color-mix(in oklab, var(--color-primary) 30%, transparent);
    }

    .new-chat:hover {
        background: color-mix(in oklab, var(--color-primary) 20%, transparent);
    }

    .history-empty {
        font-size: 0.85rem;
        color: color-mix(in oklab, var(--color-base-content) 55%, transparent);
        padding: 0.5rem 0.25rem;
    }

    .history-list {
        list-style: none;
        margin: 0;
        padding: 0;
        display: flex;
        flex-direction: column;
        gap: 0.25rem;
    }

    .history-row {
        display: flex;
        align-items: center;
        gap: 0.25rem;
        border-radius: 0.6rem;
        border: 1px solid transparent;
    }

    .history-row.active {
        background: color-mix(in oklab, var(--color-primary) 12%, transparent);
        border-color: color-mix(in oklab, var(--color-primary) 30%, transparent);
    }

    .history-open {
        flex: 1 1 auto;
        min-width: 0;
        display: flex;
        flex-direction: column;
        gap: 0.1rem;
        text-align: left;
        padding: 0.45rem 0.6rem;
        background: none;
        border: none;
        cursor: pointer;
        color: var(--color-base-content);
    }

    .history-open:hover {
        background: color-mix(in oklab, var(--color-base-content) 6%, transparent);
        border-radius: 0.6rem;
    }

    .history-name {
        font-size: 0.88rem;
        font-weight: 600;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .history-time {
        font-size: 0.72rem;
        color: color-mix(in oklab, var(--color-base-content) 50%, transparent);
    }

    .history-action {
        flex: 0 0 auto;
        display: grid;
        place-items: center;
        width: 1.7rem;
        height: 1.7rem;
        margin-right: 0.25rem;
        border-radius: 0.45rem;
        border: none;
        background: none;
        cursor: pointer;
        font-size: 0.8rem;
        color: color-mix(in oklab, var(--color-base-content) 45%, transparent);
    }

    .history-action:hover {
        color: var(--color-error);
        background: color-mix(in oklab, var(--color-error) 14%, transparent);
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

    /* Animated "assistant is typing" indicator. */
    .bubble.typing {
        display: inline-flex;
        align-items: center;
        gap: 0.28rem;
        padding: 0.7rem 0.85rem;
    }

    .typing-dot {
        width: 0.45rem;
        height: 0.45rem;
        border-radius: 999px;
        background: color-mix(in oklab, var(--color-base-content) 55%, transparent);
        animation: typing-bounce 1.2s infinite ease-in-out;
    }

    .typing-dot:nth-child(2) {
        animation-delay: 0.18s;
    }

    .typing-dot:nth-child(3) {
        animation-delay: 0.36s;
    }

    @keyframes typing-bounce {
        0%, 60%, 100% {
            transform: translateY(0);
            opacity: 0.5;
        }
        30% {
            transform: translateY(-0.25rem);
            opacity: 1;
        }
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

    /* Shows that the assistant is aware of the page the user is currently viewing. */
    .context-chip {
        align-self: flex-start;
        display: inline-flex;
        align-items: center;
        gap: 0.3rem;
        max-width: 100%;
        font-size: 0.7rem;
        font-weight: 600;
        padding: 0.15rem 0.55rem;
        border-radius: 999px;
        color: var(--color-primary);
        background: color-mix(in oklab, var(--color-primary) 12%, transparent);
        border: 1px solid color-mix(in oklab, var(--color-primary) 28%, transparent);
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .context-icon {
        flex: 0 0 auto;
        width: 0.85rem;
        height: 0.85rem;
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
