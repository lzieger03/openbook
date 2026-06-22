<!--
OpenBook: Interactive Online Textbooks
© 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.
-->

<!--
@component
Full-screen login form shown to unauthenticated users.
-->

<script lang="ts">
    import Card         from "../../basic/card/Card.svelte";
    import CardActions  from "../../basic/card/CardActions.svelte";
    import CardBody     from "../../basic/card/CardBody.svelte";
    import CardHeader   from "../../basic/card/CardHeader.svelte";
    import CardSubtitle from "../../basic/card/CardSubtitle.svelte";
    import CardTitle    from "../../basic/card/CardTitle.svelte";

    import { auth }     from "../../../stores/auth.js";
    import { i18n }     from "../../../stores/i18n.js";

    let usernameOrEmail = $state("");
    let password        = $state("");
    let loading         = $state(false);
    let fieldErrors     = $state<Record<string, string>>({});
    let generalError    = $state("");

    async function handleSubmit(event: SubmitEvent) {
        event.preventDefault();
        loading      = true;
        fieldErrors  = {};
        generalError = "";

        const result = await auth.login(usernameOrEmail, password);

        if (result.success) {
            // If the user deep-linked into a specific in-app page (e.g.
            // #/gamification-test), stay in the app and render it. The auth store
            // already updated reactively, so ApplicationFrame swaps the login form
            // for the requested route — this also lets teachers/admins reach app
            // pages instead of always being bounced to a role frontend.
            const hashRoute = window.location.hash.replace(/^#/, "");

            if (hashRoute && hashRoute !== "/") {
                return;
            }

            // Otherwise let the server decide where to go based on the user's role
            // (teachers -> /teacher/, students -> /dashboard/index.html).
            window.location.href = "/post-login-redirect/";
            return;
        }

        if (!result.success) {
            for (const error of result.errors) {
                if (error.param) {
                    fieldErrors[error.param] = error.message;
                } else {
                    generalError = error.message;
                }
            }
            if (!generalError && Object.keys(fieldErrors).length === 0) {
                generalError = $i18n.Login.Error.Default;
            }
        }

        loading = false;
    }
</script>

<div class="flex flex-1 flex-col items-center justify-center bg-base-200 p-4">
    <Card variant="elevated" class="w-full max-w-md">
        <CardBody class="gap-6">
            <CardHeader class="items-center text-center">
                <div class="avatar mb-1">
                    <div class="flex w-16 items-center justify-center rounded-full bg-primary/10 ring ring-primary ring-offset-2 ring-offset-base-100">
                        <span class="text-4xl">📚</span>
                    </div>
                </div>
                <CardTitle class="text-3xl font-bold text-primary">OpenBook</CardTitle>
                <CardSubtitle class="text-base-content/70">{$i18n.Login.Subtitle}</CardSubtitle>
            </CardHeader>

            <form onsubmit={handleSubmit} class="flex flex-col gap-4" novalidate>
                {#if generalError}
                    <div class="alert alert-error" role="alert">
                        <i class="bi bi-exclamation-circle-fill"></i>
                        <span>{generalError}</span>
                    </div>
                {/if}

                <div class="form-control">
                    <label class="label" for="login-username">
                        <span class="label-text font-medium">{$i18n.Login.Username.Label}</span>
                    </label>
                    <input
                        id           = "login-username"
                        type         = "text"
                        class        = "input input-bordered"
                        class:input-error = {!!(fieldErrors["username"] ?? fieldErrors["email"])}
                        placeholder  = {$i18n.Login.Username.Placeholder}
                        bind:value   = {usernameOrEmail}
                        disabled     = {loading}
                        autocomplete = "username"
                        aria-describedby = {fieldErrors["username"] ?? fieldErrors["email"] ? "login-username-error" : undefined}
                    />
                    {#if fieldErrors["username"] ?? fieldErrors["email"]}
                        <div class="label" id="login-username-error">
                            <span class="label-text-alt text-error">{fieldErrors["username"] ?? fieldErrors["email"]}</span>
                        </div>
                    {/if}
                </div>

                <div class="form-control">
                    <label class="label" for="login-password">
                        <span class="label-text font-medium">{$i18n.Login.Password.Label}</span>
                    </label>
                    <input
                        id           = "login-password"
                        type         = "password"
                        class        = "input input-bordered"
                        class:input-error = {!!fieldErrors["password"]}
                        placeholder  = {$i18n.Login.Password.Placeholder}
                        bind:value   = {password}
                        disabled     = {loading}
                        autocomplete = "current-password"
                        aria-describedby = {fieldErrors["password"] ? "login-password-error" : undefined}
                    />
                    {#if fieldErrors["password"]}
                        <div class="label" id="login-password-error">
                            <span class="label-text-alt text-error">{fieldErrors["password"]}</span>
                        </div>
                    {/if}
                </div>

                <CardActions justify="center" class="mt-2">
                    <button
                        type     = "submit"
                        class    = "btn btn-primary btn-wide"
                        disabled = {loading}
                    >
                        {#if loading}
                            <span class="loading loading-spinner loading-sm" aria-hidden="true"></span>
                        {/if}
                        {$i18n.Login.Submit}
                    </button>
                </CardActions>
            </form>
        </CardBody>
    </Card>
</div>
