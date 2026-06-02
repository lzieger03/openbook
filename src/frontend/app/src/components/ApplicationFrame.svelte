<!--
OpenBook: Interactive Online Textbooks - Server
© 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.
-->

<!--
@component
Root component of the application which defines the global application UI.
-->

<script lang="ts">
    import Router from "svelte-spa-router";
    import routes from "./routes.js";
    import AppHeader from "./app-frame/AppHeader.svelte";
    import AppFooter from "./app-frame/AppFooter.svelte";
</script>

<main class="app-frame">
    <AppHeader />
    <section class="app-content">
        <Router {routes} />
    </section>
    <AppFooter />
</main>

<style>
    .app-frame {
        flex: 1;
        min-height: 100vh;
        display: flex;
        flex-direction: column;
    }

    .app-content {
        flex: 1;
        display: flex;
        flex-direction: column;
    }
</style>