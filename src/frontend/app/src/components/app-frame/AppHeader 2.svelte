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
Reusable application header with primary navigation.
-->
<script lang="ts">
    import {push} from "svelte-spa-router";

    export let brand = "ElisaAI";
    export let links: Array<{label: string; href: string}> = [
        {label: "Dashboard", href: "/dashboard"},
    ];
    export let statusLabel = "System online";
    export let statusDetail = "v2.0.2.5";

    function goTo(href: string): void {
        // The dashboard is a separate microfrontend bundle, not an in-app hash
        // route, so navigate the browser to it instead of using the SPA router.
        if (href.startsWith("/dashboard")) {
            window.location.href = "/dashboard/index.html";
            return;
        }

        push(href);
    }
</script>

<header class="app-header">
    <div class="header-left">
        <div class="brand-mark" aria-hidden="true"></div>
        <div class="brand-text">
            {brand}
        </div>
    </div>

    <nav class="header-nav" aria-label="Primary">
        {#each links as link (link.href)}
            <button class="btn btn-ghost btn-sm" type="button" onclick={() => goTo(link.href)}>
                {link.label}
            </button>
        {/each}
    </nav>

    <div class="header-right">
        <span class="status-pill">
            <span class="status-dot" aria-hidden="true"></span>
            {statusLabel} // {statusDetail}
        </span>
    </div>
</header>

<style>
    .app-header {
        display: grid;
        grid-template-columns: auto 1fr auto;
        align-items: center;
        gap: 1rem;
        padding: 0.75rem 1.5rem;
        background: var(--color-base-100);
        border-bottom: 1px solid color-mix(in oklab, var(--color-base-content) 12%, transparent);
    }

    .header-left {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.05em;
    }

    .brand-mark {
        width: 2rem;
        height: 2rem;
        border-radius: 0.75rem;
        background: linear-gradient(135deg,
            color-mix(in oklab, var(--color-primary) 80%, transparent),
            color-mix(in oklab, var(--color-secondary) 70%, transparent)
        );
        box-shadow: 0 0 20px color-mix(in oklab, var(--color-primary) 35%, transparent);
    }

    .brand-text {
        font-size: 1.05rem;
        text-transform: uppercase;
    }

    .header-nav {
        display: flex;
        justify-content: center;
        gap: 0.5rem;
    }

    .header-right {
        display: flex;
        justify-content: flex-end;
    }

    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.35rem 0.75rem;
        border-radius: 999px;
        border: 1px solid color-mix(in oklab, var(--color-base-content) 18%, transparent);
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        background: color-mix(in oklab, var(--color-base-200) 70%, transparent);
    }

    .status-dot {
        width: 0.5rem;
        height: 0.5rem;
        border-radius: 999px;
        background: var(--color-success);
        box-shadow: 0 0 12px color-mix(in oklab, var(--color-success) 70%, transparent);
    }

    @media (max-width: 720px) {
        .app-header {
            grid-template-columns: 1fr;
            justify-items: center;
            text-align: center;
        }

        .header-nav {
            flex-wrap: wrap;
        }
    }
</style>
