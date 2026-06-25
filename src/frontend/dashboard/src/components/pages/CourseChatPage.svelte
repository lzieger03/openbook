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
Full-screen AI tutor page for a single course. Chat runs over the course-scoped
WebSocket API via the shared ai-chat store; the composer is enabled while connected
and the connection status is shown. See README-websocket-api.md.

Default presentation is full-screen; other modes (floating window, docked
sidebar, minimised icon) can be layered on later.
-->
<script lang="ts">
    import {onMount} from "svelte";
    import {push} from "svelte-spa-router";
    import {dashboardStore} from "../../stores/dashboard.store.js";
    import type {DashboardState} from "../../stores/dashboard.store.js";
    import {createAiChatStore} from "../../stores/ai-chat.store.js";
    import type {AiChatState} from "../../stores/ai-chat.store.js";
    import {renderMarkdown} from "../../data/markdown.js";

    let {params}: {params?: {id?: string}} = $props();

    let state = $state<DashboardState>({
        isLoading: true,
        errorMessage: "",
        user: null,
        stats: null,
        skills: [],
        courses: [],
    });

    // AI chat over the course-scoped WebSocket channel.
    const chat = createAiChatStore(() => params?.id);
    let chatState = $state<AiChatState>({
        connection: "disconnected",
        errorMessage: "",
        messages: [],
        sessions: [],
        activeSessionId: null,
        awaitingResponse: false,
    });
    let draft = $state("");
    // Whether the "Chats" section in the sidebar is expanded.
    let chatsExpanded = $state(true);
    // The scrollable messages container; kept pinned to the bottom on new content.
    let messagesEl = $state<HTMLDivElement>();

    // Auto-scroll to the latest message / typing indicator whenever they change.
    $effect(() => {
        // Touch the reactive values so the effect re-runs on new messages or while
        // the assistant is "typing".
        void chatState.messages.length;
        void chatState.awaitingResponse;

        const el = messagesEl;
        if (el) {
            requestAnimationFrame(() => {
                el.scrollTop = el.scrollHeight;
            });
        }
    });

    onMount(() => {
        const unsubscribeDashboard = dashboardStore.subscribe((value) => {
            state = value;
        });

        if (state.courses.length === 0) {
            dashboardStore.refresh();
        }

        const unsubscribeChat = chat.subscribe((value) => {
            chatState = value;
        });
        void chat.connect();

        return () => {
            unsubscribeDashboard();
            unsubscribeChat();
            void chat.disconnect();
        };
    });

    const courseName = $derived(
        state.courses.find((course) => course.id === params?.id)?.name ?? "this course",
    );

    // Side navigation. "Quizzes" is wired; the rest are placeholders for now.
    // "Chats" is its own expandable section below the nav.
    const navItems = $derived<Array<{icon: string; label: string; to?: string}>>([
        {icon: "🎮", label: "Games"},
        {icon: "🧠", label: "Quizzes", to: `/quiz/${params?.id ?? ""}`},
        {icon: "🎓", label: "Exams", to: `/exam/${params?.id ?? ""}`},
    ]);

    function onSelectSession(sessionId: string): void {
        if (sessionId !== chatState.activeSessionId) {
            void chat.openSession(sessionId);
        }
    }

    // Inline rename + filter state for the chat list.
    let editingSessionId = $state<string | null>(null);
    let editingTitle = $state("");
    let chatFilter = $state("");

    const filteredSessions = $derived.by(() => {
        const term = chatFilter.trim().toLowerCase();
        if (!term) {
            return chatState.sessions;
        }
        return chatState.sessions.filter((session) => session.title.toLowerCase().includes(term));
    });

    /** Focus + select an input as soon as it is rendered (for inline rename). */
    function autofocus(node: HTMLInputElement): void {
        node.focus();
        node.select();
    }

    function startRename(session: {id: string; title: string}): void {
        editingSessionId = session.id;
        editingTitle = session.title;
    }

    function commitRename(): void {
        const id = editingSessionId;
        const title = editingTitle.trim();
        editingSessionId = null;
        if (id && title) {
            void chat.renameSession(id, title);
        }
    }

    function cancelRename(): void {
        editingSessionId = null;
    }

    function onDeleteSession(session: {id: string; title: string}): void {
        if (confirm(`Delete the chat “${session.title}”? This cannot be undone.`)) {
            void chat.deleteSession(session.id);
        }
    }

    /** Short relative time for a chat's last activity (e.g. "5 min", "3 h", "2 d"). */
    function formatRelative(iso: string): string {
        const then = new Date(iso).getTime();
        if (!Number.isFinite(then)) {
            return "";
        }
        const diffSec = Math.max(0, Math.round((Date.now() - then) / 1000));
        if (diffSec < 60) return "just now";
        const min = Math.round(diffSec / 60);
        if (min < 60) return `${min} min`;
        const hours = Math.round(min / 60);
        if (hours < 24) return `${hours} h`;
        const days = Math.round(hours / 24);
        if (days < 7) return `${days} d`;
        return new Date(then).toLocaleDateString();
    }

    const connected = $derived(chatState.connection === "connected");
    const statusLabel = $derived(
        chatState.connection === "connected"
            ? "Online"
            : chatState.connection === "connecting"
                ? "Connecting…"
                : chatState.connection === "wait_before_retry"
                    ? "Reconnecting…"
                    : "Offline",
    );

    async function send(): Promise<void> {
        const text = draft.trim();
        if (!text || !connected) {
            return;
        }

        draft = "";
        await chat.sendChatInput("markdown", text);
    }
</script>

<div class="chat-screen">
    <aside class="sidebar">
        <button type="button" class="back" onclick={() => push("/")}>← Dashboard</button>

        <button type="button" class="content-cta" onclick={() => push(`/content/${params?.id ?? ""}`)}>
            <span aria-hidden="true">📖</span>
            <span>Content</span>
        </button>

        <nav class="nav" aria-label="Sections">
            {#each navItems as item (item.label)}
                <button
                    type="button"
                    class="nav-item"
                    disabled={!item.to}
                    onclick={() => item.to && push(item.to)}
                >
                    <span class="nav-icon" aria-hidden="true">{item.icon}</span>
                    <span class="nav-label">{item.label}</span>
                    {#if !item.to}<span class="soon">soon</span>{/if}
                </button>
            {/each}
        </nav>

        <section class="chats">
            <button
                type="button"
                class="chats-header"
                aria-expanded={chatsExpanded}
                onclick={() => (chatsExpanded = !chatsExpanded)}
            >
                <span class="nav-icon" aria-hidden="true">💬</span>
                <span class="nav-label">Chats</span>
                <span class="chev" aria-hidden="true">{chatsExpanded ? "▾" : "▸"}</span>
            </button>

            {#if chatsExpanded}
                <div class="chats-body">
                    <button type="button" class="new-chat" onclick={() => chat.newChat()}>
                        <span aria-hidden="true">＋</span> New chat
                    </button>

                    {#if chatState.sessions.length > 3}
                        <input
                            class="chat-search"
                            type="search"
                            placeholder="Search chats…"
                            bind:value={chatFilter}
                        />
                    {/if}

                    {#if chatState.sessions.length === 0}
                        <p class="chats-empty">No saved chats yet.</p>
                    {:else if filteredSessions.length === 0}
                        <p class="chats-empty">No chats match “{chatFilter}”.</p>
                    {:else}
                        <ul class="chat-list">
                            {#each filteredSessions as session (session.id)}
                                <li class="chat-row" class:active={session.id === chatState.activeSessionId}>
                                    {#if editingSessionId === session.id}
                                        <input
                                            class="chat-rename"
                                            type="text"
                                            bind:value={editingTitle}
                                            maxlength="120"
                                            onkeydown={(event) => {
                                                if (event.key === "Enter") { event.preventDefault(); commitRename(); }
                                                else if (event.key === "Escape") { event.preventDefault(); cancelRename(); }
                                            }}
                                            onblur={commitRename}
                                            use:autofocus
                                        />
                                    {:else}
                                        <button
                                            type="button"
                                            class="chat-item"
                                            class:active={session.id === chatState.activeSessionId}
                                            title={session.title}
                                            onclick={() => onSelectSession(session.id)}
                                        >
                                            <span class="chat-title">{session.title}</span>
                                            <span class="chat-time">{formatRelative(session.updated_at)}</span>
                                        </button>
                                        <span class="chat-actions">
                                            <button type="button" class="chat-action" aria-label="Rename chat" title="Rename" onclick={() => startRename(session)}>✎</button>
                                            <button type="button" class="chat-action danger" aria-label="Delete chat" title="Delete" onclick={() => onDeleteSession(session)}>✕</button>
                                        </span>
                                    {/if}
                                </li>
                            {/each}
                        </ul>
                    {/if}
                </div>
            {/if}
        </section>
    </aside>

    <main class="conversation">
        <div class="messages" bind:this={messagesEl}>
            <div class="message">
                <img class="avatar" src="logo.png" alt="ElisaAI assistant" />
                <div class="bubble">
                    System online. I am <strong>ElisaAI</strong>. Ready to help you with
                    <strong>{courseName}</strong> — what topic shall we analyse today?
                </div>
            </div>

            {#each chatState.messages as message (message.id)}
                <div class="message" class:user={message.sender === "user"}>
                    {#if message.sender === "assistant"}
                        <img class="avatar" src="logo.png" alt="ElisaAI assistant" />
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
                    <img class="avatar" src="logo.png" alt="ElisaAI assistant" />
                    <div class="bubble typing" aria-label="ElisaAI is typing">
                        <span class="typing-dot"></span>
                        <span class="typing-dot"></span>
                        <span class="typing-dot"></span>
                    </div>
                </div>
            {/if}
        </div>

        <div class="composer">
            <span class="conn-status" class:online={connected}>
                <span class="status-dot" aria-hidden="true"></span>
                {statusLabel}
            </span>
            <form class="composer-row" onsubmit={(event) => {event.preventDefault(); send();}}>
                <button type="button" class="composer-add" aria-label="Add attachment" disabled>+</button>
                <input
                    class="composer-input"
                    type="text"
                    placeholder={connected ? "Message" : "Connecting…"}
                    bind:value={draft}
                    disabled={!connected}
                />
                <button
                    type="submit"
                    class="composer-send"
                    aria-label="Send message"
                    disabled={!connected || draft.trim().length === 0}
                >→</button>
            </form>
            <p class="disclaimer">ElisaAI 2026 // ElisaAI may generate misinformation. Please verify all information.</p>
        </div>

        {#if chatState.errorMessage}
            <div class="error-overlay" role="alert">
                <div class="error-card">
                    <span class="error-icon" aria-hidden="true">🔌</span>
                    <h2 class="error-title">Assistant unavailable</h2>
                    <p class="error-text">{chatState.errorMessage}</p>
                    <button type="button" class="btn btn-primary" onclick={() => chat.retry()}>Retry</button>
                </div>
            </div>
        {/if}
    </main>
</div>

<style>
    .chat-screen {
        flex: 1;
        min-height: 0;
        overflow: hidden;
        display: grid;
        grid-template-columns: 16rem 1fr;
        grid-template-rows: minmax(0, 1fr);
        width: 100%;
    }

    /* Sidebar stays put; only the conversation scrolls. */
    .sidebar {
        min-height: 0;
        overflow: hidden;
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
        padding: 1.5rem 1rem;
        border-right: 1px solid color-mix(in oklab, var(--color-base-content) 10%, transparent);
        background: color-mix(in oklab, var(--color-base-100) 60%, transparent);
    }

    .back {
        align-self: flex-start;
        background: none;
        border: none;
        cursor: pointer;
        font-weight: 600;
        color: var(--color-primary);
    }

    .back:focus-visible {
        outline: 2px solid var(--color-primary);
        outline-offset: 2px;
    }

    .content-cta {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        padding: 0.85rem 1rem;
        border-radius: 0.85rem;
        border: 1px solid color-mix(in oklab, var(--color-primary) 55%, transparent);
        font-size: 1.05rem;
        font-weight: 700;
        cursor: pointer;
        color: var(--color-primary-content);
        background: var(--color-primary);
        box-shadow: 0 0 18px color-mix(in oklab, var(--color-primary) 45%, transparent);
        transition: transform 0.12s ease;
    }

    .content-cta:hover {
        transform: translateY(-2px);
    }

    .content-cta:focus-visible {
        outline: 2px solid var(--color-base-content);
        outline-offset: 2px;
    }

    .nav {
        display: flex;
        flex-direction: column;
        gap: 0.35rem;
    }

    .nav-item {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 0.65rem 0.75rem;
        border-radius: 0.75rem;
        background: transparent;
        border: none;
        color: var(--color-base-content);
        cursor: pointer;
    }

    .nav-item:hover:not(:disabled) {
        background: color-mix(in oklab, var(--color-primary) 14%, transparent);
    }

    .nav-item:focus-visible {
        outline: 2px solid var(--color-primary);
        outline-offset: 2px;
    }

    .nav-item:disabled {
        cursor: not-allowed;
        opacity: 0.6;
    }

    .nav-icon {
        font-size: 1.1rem;
    }

    .nav-label {
        flex: 1 1 auto;
        text-align: left;
        font-weight: 600;
    }

    .soon {
        font-size: 0.65rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: color-mix(in oklab, var(--color-base-content) 50%, transparent);
    }

    /* Expandable "Chats" section: takes the remaining sidebar height and scrolls. */
    .chats {
        display: flex;
        flex-direction: column;
        min-height: 0;
        flex: 1 1 auto;
    }

    .chats-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        width: 100%;
        padding: 0.65rem 0.75rem;
        border-radius: 0.75rem;
        background: transparent;
        border: none;
        color: var(--color-base-content);
        cursor: pointer;
    }

    .chats-header:hover {
        background: color-mix(in oklab, var(--color-primary) 14%, transparent);
    }

    .chats-header .chev {
        color: color-mix(in oklab, var(--color-base-content) 55%, transparent);
    }

    .chats-body {
        display: flex;
        flex-direction: column;
        gap: 0.35rem;
        min-height: 0;
        overflow-y: auto;
        padding: 0.25rem 0.25rem 0.25rem 0.5rem;
    }

    .new-chat {
        display: flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.45rem 0.65rem;
        border-radius: 0.6rem;
        border: 1px dashed color-mix(in oklab, var(--color-primary) 45%, transparent);
        background: color-mix(in oklab, var(--color-primary) 8%, transparent);
        color: var(--color-primary);
        font-weight: 600;
        font-size: 0.85rem;
        cursor: pointer;
    }

    .new-chat:hover {
        background: color-mix(in oklab, var(--color-primary) 16%, transparent);
    }

    .chats-empty {
        font-size: 0.8rem;
        color: color-mix(in oklab, var(--color-base-content) 55%, transparent);
        padding: 0.25rem 0.4rem;
    }

    .chat-search {
        width: 100%;
        padding: 0.4rem 0.6rem;
        border-radius: 0.55rem;
        border: 1px solid color-mix(in oklab, var(--color-base-content) 15%, transparent);
        background: color-mix(in oklab, var(--color-base-100) 70%, transparent);
        color: var(--color-base-content);
        font-size: 0.8rem;
    }

    .chat-list {
        list-style: none;
        margin: 0;
        padding: 0;
        display: flex;
        flex-direction: column;
        gap: 0.15rem;
    }

    /* A chat row: the selectable item plus rename/delete actions revealed on hover. */
    .chat-row {
        display: flex;
        align-items: center;
        gap: 0.15rem;
        border-radius: 0.55rem;
        border: 1px solid transparent;
    }

    .chat-row.active {
        background: color-mix(in oklab, var(--color-primary) 16%, transparent);
        border-color: color-mix(in oklab, var(--color-primary) 35%, transparent);
    }

    .chat-item {
        flex: 1 1 auto;
        min-width: 0;
        display: flex;
        flex-direction: column;
        gap: 0.05rem;
        text-align: left;
        padding: 0.4rem 0.55rem;
        border-radius: 0.5rem;
        border: none;
        background: transparent;
        color: color-mix(in oklab, var(--color-base-content) 80%, transparent);
        cursor: pointer;
        font-size: 0.85rem;
    }

    .chat-row:not(.active):hover {
        background: color-mix(in oklab, var(--color-base-content) 6%, transparent);
    }

    .chat-row.active .chat-item {
        color: var(--color-base-content);
        font-weight: 600;
    }

    .chat-title {
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .chat-time {
        font-size: 0.68rem;
        font-weight: 400;
        color: color-mix(in oklab, var(--color-base-content) 50%, transparent);
    }

    .chat-actions {
        display: flex;
        gap: 0.1rem;
        flex: 0 0 auto;
        opacity: 0;
        transition: opacity 0.15s ease;
    }

    .chat-row:hover .chat-actions,
    .chat-row.active .chat-actions,
    .chat-action:focus-visible {
        opacity: 1;
    }

    .chat-action {
        display: grid;
        place-items: center;
        width: 1.5rem;
        height: 1.5rem;
        border: none;
        border-radius: 0.4rem;
        background: none;
        cursor: pointer;
        font-size: 0.75rem;
        color: color-mix(in oklab, var(--color-base-content) 55%, transparent);
    }

    .chat-action:hover {
        background: color-mix(in oklab, var(--color-base-content) 12%, transparent);
        color: var(--color-base-content);
    }

    .chat-action.danger:hover {
        background: color-mix(in oklab, var(--color-error) 16%, transparent);
        color: var(--color-error);
    }

    .chat-rename {
        flex: 1 1 auto;
        min-width: 0;
        padding: 0.35rem 0.5rem;
        border-radius: 0.5rem;
        border: 1px solid color-mix(in oklab, var(--color-primary) 45%, transparent);
        background: var(--color-base-100);
        color: var(--color-base-content);
        font-size: 0.85rem;
    }

    .conversation {
        position: relative;
        display: flex;
        flex-direction: column;
        min-height: 0;
        background: var(--color-base-200);
    }

    .messages {
        flex: 1;
        min-height: 0;
        overflow-y: auto;
        display: flex;
        flex-direction: column;
        gap: 1.25rem;
        padding: 2rem clamp(1rem, 6vw, 6rem);
    }

    .message {
        display: flex;
        align-items: flex-start;
        gap: 0.85rem;
        max-width: 56rem;
    }

    .message.user {
        margin-left: auto;
        justify-content: flex-end;
    }

    .avatar {
        width: 2.75rem;
        height: 2.75rem;
        flex: 0 0 auto;
        border-radius: 999px;
        object-fit: cover;
    }

    .bubble {
        padding: 1rem 1.25rem;
        border-radius: 1rem;
        border-top-left-radius: 0.25rem;
        line-height: 1.55;
        color: var(--color-base-content);
        background: color-mix(in oklab, var(--color-base-100) 85%, transparent);
        border: 1px solid color-mix(in oklab, var(--color-primary) 30%, transparent);
        box-shadow: 0 0 18px color-mix(in oklab, var(--color-primary) 12%, transparent);
        white-space: pre-wrap;
    }

    .bubble.user {
        color: var(--color-primary-content);
        background: var(--color-primary);
        border-color: transparent;
        border-top-left-radius: 1rem;
        border-bottom-right-radius: 0.25rem;
    }

    /* Animated "assistant is typing" indicator. */
    .bubble.typing {
        display: inline-flex;
        align-items: center;
        gap: 0.3rem;
        padding: 0.9rem 1.1rem;
    }

    .typing-dot {
        width: 0.5rem;
        height: 0.5rem;
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
            transform: translateY(-0.28rem);
            opacity: 1;
        }
    }

    /* Rendered Markdown content: the HTML structure provides the spacing, so drop the
       raw-text pre-wrap and style the injected elements. */
    .bubble.md {
        white-space: normal;
    }

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
        margin: 0.9rem 0 0.4rem;
    }

    .bubble.md :global(h1) { font-size: 1.3rem; }
    .bubble.md :global(h2) { font-size: 1.15rem; }
    .bubble.md :global(h3) { font-size: 1.05rem; }

    .bubble.md :global(p) {
        margin: 0.5rem 0;
    }

    .bubble.md :global(ul),
    .bubble.md :global(ol) {
        margin: 0.5rem 0 0.5rem 1.4rem;
    }

    .bubble.md :global(li) {
        margin: 0.2rem 0;
    }

    .bubble.md :global(a) {
        color: var(--color-primary);
        text-decoration: underline;
    }

    .bubble.md :global(code) {
        font-family: ui-monospace, "SF Mono", Menlo, Monaco, monospace;
        font-size: 0.85em;
        padding: 0.1rem 0.35rem;
        border-radius: 0.35rem;
        background: color-mix(in oklab, var(--color-base-content) 12%, transparent);
    }

    .bubble.md :global(pre) {
        margin: 0.6rem 0;
        padding: 0.85rem 1rem;
        border-radius: 0.6rem;
        overflow-x: auto;
        background: color-mix(in oklab, var(--color-base-content) 12%, transparent);
        border: 1px solid color-mix(in oklab, var(--color-base-content) 14%, transparent);
    }

    .bubble.md :global(pre code) {
        padding: 0;
        background: none;
        font-size: 0.85rem;
    }

    .bubble.md :global(blockquote) {
        margin: 0.6rem 0;
        padding: 0.3rem 0.9rem;
        border-left: 3px solid var(--color-primary);
        background: color-mix(in oklab, var(--color-primary) 10%, transparent);
    }

    .composer {
        flex: 0 0 auto;
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        padding: 1rem clamp(1rem, 6vw, 6rem) 1.25rem;
    }

    .conn-status {
        align-self: center;
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: color-mix(in oklab, var(--color-base-content) 60%, transparent);
    }

    .status-dot {
        width: 0.5rem;
        height: 0.5rem;
        border-radius: 999px;
        background: color-mix(in oklab, var(--color-base-content) 40%, transparent);
    }

    .conn-status.online {
        color: var(--color-success);
    }

    /* Centered overlay shown when the assistant connection gives up. */
    .error-overlay {
        position: absolute;
        inset: 0;
        z-index: 5;
        display: grid;
        place-items: center;
        padding: 1.5rem;
        background: color-mix(in oklab, var(--color-base-300) 55%, transparent);
        backdrop-filter: blur(4px);
    }

    .error-card {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.85rem;
        max-width: 26rem;
        width: 100%;
        text-align: center;
        padding: 2rem;
        border-radius: 1.25rem;
        background: var(--color-base-100);
        border: 1px solid color-mix(in oklab, var(--color-warning) 35%, transparent);
        box-shadow: 0 0 40px color-mix(in oklab, var(--color-warning) 18%, transparent);
    }

    .error-icon {
        font-size: 2.5rem;
        line-height: 1;
    }

    .error-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: var(--color-base-content);
    }

    .error-text {
        line-height: 1.5;
        color: color-mix(in oklab, var(--color-base-content) 75%, transparent);
    }

    .conn-status.online .status-dot {
        background: var(--color-success);
        box-shadow: 0 0 10px color-mix(in oklab, var(--color-success) 70%, transparent);
    }

    .composer-row {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 0.5rem 0.75rem;
        border-radius: 999px;
        background: color-mix(in oklab, var(--color-base-100) 80%, transparent);
        border: 1px solid color-mix(in oklab, var(--color-primary) 35%, transparent);
        box-shadow: 0 0 18px color-mix(in oklab, var(--color-primary) 12%, transparent);
    }

    .composer-add,
    .composer-send {
        display: grid;
        place-items: center;
        width: 2.25rem;
        height: 2.25rem;
        flex: 0 0 auto;
        border-radius: 999px;
        border: none;
        font-size: 1.2rem;
        cursor: pointer;
        color: var(--color-primary-content);
        background: color-mix(in oklab, var(--color-primary) 70%, transparent);
    }

    .composer-add:disabled,
    .composer-send:disabled {
        cursor: not-allowed;
        opacity: 0.6;
    }

    .composer-input {
        flex: 1 1 auto;
        background: transparent;
        border: none;
        color: var(--color-base-content);
        font-size: 1rem;
        padding: 0.5rem 0.25rem;
    }

    .composer-input:focus {
        outline: none;
    }

    .disclaimer {
        text-align: center;
        font-size: 0.7rem;
        letter-spacing: 0.04em;
        color: color-mix(in oklab, var(--color-base-content) 55%, transparent);
    }

    @media (max-width: 48rem) {
        .chat-screen {
            grid-template-columns: 1fr;
        }

        .sidebar {
            display: none;
        }
    }
</style>
