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
    import type {AiChatState, AiChatStore} from "../../stores/ai-chat.store.js";

    let {params}: {params?: {id?: string}} = $props();

    let state = $state<DashboardState>({
        isLoading: true,
        errorMessage: "",
        user: null,
        stats: null,
        skills: [],
        courses: [],
    });

    let chat: AiChatStore | undefined;
    let chatState = $state<AiChatState>({connection: "disconnected", errorMessage: "", messages: []});
    let draft = $state("");

    onMount(() => {
        const unsubscribeDashboard = dashboardStore.subscribe((value) => {
            state = value;
        });

        if (state.courses.length === 0) {
            dashboardStore.refresh();
        }

        chat = createAiChatStore(params?.id);
        const unsubscribeChat = chat.subscribe((value) => {
            chatState = value;
        });
        void chat.connect();

        return () => {
            unsubscribeDashboard();
            unsubscribeChat();
            void chat?.disconnect();
        };
    });

    const courseName = $derived(
        state.courses.find((course) => course.id === params?.id)?.name ?? "this course",
    );

    // Side navigation. "Quizzes" is wired; the rest are placeholders for now.
    const navItems = $derived<Array<{icon: string; label: string; to?: string}>>([
        {icon: "🎮", label: "Games"},
        {icon: "🧠", label: "Quizzes", to: `/quiz/${params?.id ?? ""}`},
        {icon: "🎓", label: "Exams"},
        {icon: "💬", label: "Chats"},
    ]);

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
        await chat?.sendChatInput("markdown", text);
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
    </aside>

    <main class="conversation">
        <div class="messages">
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
                    <div class="bubble" class:user={message.sender === "user"}>{message.content}</div>
                </div>
            {/each}
        </div>

        <div class="composer">
            <span class="status" class:online={connected}>
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
                    <button type="button" class="btn btn-primary" onclick={() => chat?.retry()}>Retry</button>
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

    .composer {
        flex: 0 0 auto;
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        padding: 1rem clamp(1rem, 6vw, 6rem) 1.25rem;
    }

    .status {
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

    .status.online {
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

    .status.online .status-dot {
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
