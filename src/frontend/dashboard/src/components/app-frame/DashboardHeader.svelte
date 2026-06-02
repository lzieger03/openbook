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

    let {
        user = null,
        brand = "ElisaAI",
        pageLabel = "Dashboard",
        statusLabel = "System online",
        statusDetail = "v2.0.2.5",
    }: {
        user?: DashboardUser | null;
        brand?: string;
        pageLabel?: string;
        statusLabel?: string;
        statusDetail?: string;
    } = $props();
</script>

<header class="app-header">
    <div class="header-left">
        <span class="brand-mark" aria-hidden="true"></span>
        <span class="brand-text">{brand}</span>
    </div>

    <div class="header-right">
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

    .brand-mark {
        width: 2rem;
        height: 2rem;
        border-radius: 0.6rem;
        background: linear-gradient(135deg,
            color-mix(in oklab, var(--color-primary) 80%, transparent),
            color-mix(in oklab, var(--color-secondary) 70%, transparent));
        box-shadow: 0 0 18px color-mix(in oklab, var(--color-primary) 35%, transparent);
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

    @media (max-width: 40rem) {
        .app-header {
            flex-direction: column;
            gap: 0.75rem;
            text-align: center;
        }
    }
</style>
