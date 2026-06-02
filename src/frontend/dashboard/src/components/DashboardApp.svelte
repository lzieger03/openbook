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
Application shell for the dashboard microfrontend: persistent header and footer
around the routed page content. The header avatar follows the shared store.
-->
<script lang="ts">
    import {onMount} from "svelte";
    import Router from "svelte-spa-router";
    import {dashboardStore} from "../stores/dashboard.store.js";
    import type {DashboardState} from "../stores/dashboard.store.js";
    import DashboardHeader from "./app-frame/DashboardHeader.svelte";
    import routes from "./routes.js";

    let state = $state<DashboardState>({
        isLoading: true,
        errorMessage: "",
        user: null,
        stats: null,
        skills: [],
        courses: [],
    });

    onMount(() => {
        // Subscribe so the header avatar/name stay in sync on every route.
        return dashboardStore.subscribe((value) => {
            state = value;
        });
    });
</script>

<div class="shell">
    <DashboardHeader user={state.user} />

    <main class="shell-content">
        <Router {routes} />
    </main>

    <footer class="shell-footer">
        <span>Copyright 2026 | OpenBook</span>
    </footer>
</div>

<style>
    .shell {
        flex: 1;
        min-height: 100vh;
        display: flex;
        flex-direction: column;
    }

    .shell-content {
        flex: 1;
        display: flex;
        flex-direction: column;
    }

    .shell-footer {
        margin-top: auto;
        padding: 1rem 1.5rem 1.5rem;
        text-align: center;
        font-size: 0.75rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: color-mix(in oklab, var(--color-base-content) 60%, transparent);
        border-top: 1px solid color-mix(in oklab, var(--color-base-content) 10%, transparent);
    }
</style>
