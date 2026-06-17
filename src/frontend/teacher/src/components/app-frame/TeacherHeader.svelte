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
Top application bar for the teacher area: brand on the left, theme toggle and the
signed-in teacher's name/avatar on the right. Deliberately plainer than the
student dashboard header.
-->
<script lang="ts">
    import type {TeacherUser} from "../../data/teacher.js";
    import {theme, toggleTheme} from "../../theme.js";

    let {
        user = null,
        brand = "OpenBook",
        logoSrc = "logo.png",
        pageLabel = "Teacher",
    }: {
        user?: TeacherUser | null;
        brand?: string;
        logoSrc?: string;
        pageLabel?: string;
    } = $props();
</script>

<header class="app-header">
    <div class="header-left">
        <img class="brand-logo" src={logoSrc} alt={`${brand} logo`} />
        <span class="brand-text">{brand}</span>
        <span class="page-label">{pageLabel}</span>
    </div>

    <div class="header-right">
        <button
            type="button"
            class="theme-toggle"
            aria-label={$theme === "dark" ? "Switch to light mode" : "Switch to dark mode"}
            onclick={toggleTheme}
        >
            {$theme === "dark" ? "☀️" : "🌙"}
        </button>

        {#if user}
            <span class="user-name">{user.fullName}</span>
            <span class="avatar-mark" aria-hidden="true">
                {#if user.avatarUrl}
                    <img src={user.avatarUrl} alt="" />
                {/if}
            </span>
        {/if}
    </div>
</header>

<style>
    .app-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
        padding: 0.75rem 1.5rem;
        background: var(--color-base-100);
        border-bottom: 1px solid color-mix(in oklab, var(--color-base-content) 12%, transparent);
    }

    .header-left {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        font-weight: 700;
    }

    .brand-logo {
        width: 2.2rem;
        height: 2.2rem;
        border-radius: 0.5rem;
        object-fit: contain;
    }

    .brand-text {
        font-size: 1.05rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .page-label {
        font-size: 0.85rem;
        font-weight: 500;
        color: var(--color-primary);
    }

    .header-right {
        display: flex;
        align-items: center;
        gap: 0.85rem;
    }

    .user-name {
        font-size: 0.9rem;
        color: color-mix(in oklab, var(--color-base-content) 80%, transparent);
    }

    .theme-toggle {
        display: grid;
        place-items: center;
        width: 2rem;
        height: 2rem;
        border-radius: 999px;
        font-size: 1rem;
        cursor: pointer;
        background: color-mix(in oklab, var(--color-base-200) 70%, transparent);
        border: 1px solid color-mix(in oklab, var(--color-base-content) 18%, transparent);
    }

    .theme-toggle:hover {
        border-color: color-mix(in oklab, var(--color-primary) 50%, transparent);
    }

    .avatar-mark {
        width: 1.9rem;
        height: 1.9rem;
        border-radius: 999px;
        overflow: hidden;
        background: color-mix(in oklab, var(--color-base-content) 18%, transparent);
    }

    .avatar-mark img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    @media (max-width: 40rem) {
        .app-header {
            flex-direction: column;
            gap: 0.6rem;
            text-align: center;
        }
    }
</style>
