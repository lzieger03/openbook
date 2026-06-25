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
Application shell for the teacher microfrontend: a persistent header and footer
around the routed page content. The header name/avatar follows the shared store.
-->
<script lang="ts">
    import {onMount} from "svelte";
    import Router from "svelte-spa-router";
    import {teacherStore} from "../stores/teacher.store.js";
    import type {TeacherState} from "../stores/teacher.store.js";
    import TeacherHeader from "./app-frame/TeacherHeader.svelte";
    import Toasts from "./basic/Toasts.svelte";
    import routes from "./routes.js";

    let state = $state<TeacherState>({
        isLoading: true,
        errorMessage: "",
        user: null,
        courses: [],
    });

    onMount(() => {
        // Subscribe so the header name/avatar stay in sync on every route.
        const unsubscribe = teacherStore.subscribe((value) => {
            state = value;
        });

        teacherStore.refresh();

        return unsubscribe;
    });
</script>

<div class="shell">
    <TeacherHeader user={state.user} />

    <main class="shell-content">
        <Router {routes} />
    </main>

    <footer class="shell-footer">
        <span>Copyright 2026 | OpenBook</span>
    </footer>

    <Toasts />
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
