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
Top application bar: brand on the left, user avatar and a status pill on the right.
-->
<script lang="ts">
    import type {DashboardUser} from "../../data/dashboard.js";
    import {theme, toggleTheme} from "../../theme.js";

    let {
        user = null,
        brand = "ElisaAI",
        logoSrc = "logo.png",
        pageLabel = "Dashboard",
        statusLabel = "System online",
        statusDetail = "v2.0.2.5",
    }: {
        user?: DashboardUser | null;
        brand?: string;
        logoSrc?: string;
        pageLabel?: string;
        statusLabel?: string;
        statusDetail?: string;
    } = $props();
</script>

<header class="app-header">
    <div class="header-left">
        <img class="brand-logo" src={logoSrc} alt={`${brand} logo`} />
        <span class="brand-text">{brand}</span>
    </div>

    <div class="header-right">
        <button
            type="button"
            class="theme-switch"
            role="switch"
            aria-checked={$theme === "dark"}
            aria-label={$theme === "dark" ? "Switch to light mode" : "Switch to dark mode"}
            title={$theme === "dark" ? "Dark mode" : "Light mode"}
            onclick={toggleTheme}
        >
            <span class="switch-track">
                <span class="switch-thumb">
                    {#if $theme === "dark"}
                        <!-- Moon -->
                        <svg class="switch-icon" viewBox="0 0 24 24" aria-hidden="true">
                            <path
                                fill="currentColor"
                                d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"
                            />
                        </svg>
                    {:else}
                        <!-- Sun -->
                        <svg
                            class="switch-icon"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            stroke-width="2"
                            stroke-linecap="round"
                            aria-hidden="true"
                        >
                            <circle cx="12" cy="12" r="4.2" fill="currentColor" stroke="none" />
                            <line x1="12" y1="2.5" x2="12" y2="5" />
                            <line x1="12" y1="19" x2="12" y2="21.5" />
                            <line x1="2.5" y1="12" x2="5" y2="12" />
                            <line x1="19" y1="12" x2="21.5" y2="12" />
                            <line x1="5.3" y1="5.3" x2="7" y2="7" />
                            <line x1="17" y1="17" x2="18.7" y2="18.7" />
                            <line x1="18.7" y1="5.3" x2="17" y2="7" />
                            <line x1="7" y1="17" x2="5.3" y2="18.7" />
                        </svg>
                    {/if}
                </span>
            </span>
        </button>
        <span class="avatar-mark" aria-hidden="true">
            {#if user?.avatarUrl}
                <img src={user.avatarUrl} alt="" />
            {/if}
        </span>
        <span class="page-label">{pageLabel}</span>
        <span class="status-pill">
            <span class="status-dot" aria-hidden="true"></span>
            {statusLabel} // {statusDetail}
        </span>
    </div>
</header>

<style>
    .app-header {
        position: sticky;
        top: 0;
        z-index: 50;
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
        letter-spacing: 0.05em;
    }

    .brand-logo {
        width: 2.4rem;
        height: 2.4rem;
        border-radius: 0.6rem;
        object-fit: contain;
    }

    .brand-text {
        font-size: 1.05rem;
        text-transform: uppercase;
        color: var(--color-base-content);
    }

    .header-right {
        display: flex;
        align-items: center;
        gap: 0.85rem;
    }

    /* Pill toggle: a sun knob (light, left) that slides to a moon knob (dark, right). */
    .theme-switch {
        padding: 0;
        border: 0;
        background: none;
        line-height: 0;
        cursor: pointer;
        border-radius: 999px;
    }

    .switch-track {
        display: block;
        position: relative;
        width: 3.5rem;
        height: 1.9rem;
        border-radius: 999px;
        background: color-mix(in oklab, #f6c453 50%, var(--color-base-200));
        border: 1px solid color-mix(in oklab, var(--color-base-content) 12%, transparent);
        transition: background 0.25s ease, border-color 0.25s ease;
    }

    .theme-switch[aria-checked="true"] .switch-track {
        background: #0e2a40;
        border-color: color-mix(in oklab, #38bdf8 35%, transparent);
    }

    .switch-thumb {
        position: absolute;
        top: 50%;
        left: 0.2rem;
        transform: translateY(-50%);
        display: grid;
        place-items: center;
        width: 1.45rem;
        height: 1.45rem;
        border-radius: 999px;
        background: #f0b429;
        color: #fff;
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.3);
        transition: transform 0.25s ease, background 0.25s ease;
    }

    .theme-switch[aria-checked="true"] .switch-thumb {
        transform: translate(1.6rem, -50%);
        background: #38bdf8;
    }

    .switch-icon {
        width: 0.95rem;
        height: 0.95rem;
    }

    .theme-switch:hover .switch-track {
        border-color: color-mix(in oklab, var(--color-primary) 50%, transparent);
    }

    .theme-switch:focus-visible {
        outline: 2px solid var(--color-primary);
        outline-offset: 2px;
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

    .page-label {
        font-size: 0.9rem;
        color: var(--color-primary);
    }

    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.35rem 0.75rem;
        border-radius: 999px;
        border: 1px solid color-mix(in oklab, var(--color-base-content) 18%, transparent);
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        background: color-mix(in oklab, var(--color-base-200) 70%, transparent);
        color: color-mix(in oklab, var(--color-base-content) 80%, transparent);
    }

    .status-dot {
        width: 0.5rem;
        height: 0.5rem;
        border-radius: 999px;
        background: var(--color-success);
        box-shadow: 0 0 12px color-mix(in oklab, var(--color-success) 70%, transparent);
    }

    /* On narrow screens keep the header a single row but drop the secondary,
       space-hungry items so the brand, theme toggle and avatar always fit. */
    @media (max-width: 48rem) {
        .app-header {
            padding: 0.65rem 1rem;
        }

        .page-label,
        .status-pill {
            display: none;
        }
    }

    @media (max-width: 30rem) {
        .brand-text {
            display: none;
        }
    }
</style>
