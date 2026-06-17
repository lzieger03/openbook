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
Card displaying user's account points and recent activity.
-->

<script lang="ts">
    export let data: {
        id: string;
        account_id: string;
        point_total: number;
        updated_at: string;
    };

    const pointsDisplay = data.point_total.toLocaleString();
    const lastUpdated = new Date(data.updated_at).toLocaleDateString();
</script>

<div class="card bg-gradient-to-r from-primary to-primary-focus shadow-xl">
    <div class="card-body text-primary-content">
        <div class="flex items-center justify-between">
            <div>
                <h2 class="card-title text-2xl">💰 Total Points</h2>
                <p class="text-xs opacity-75">Last updated: {lastUpdated}</p>
            </div>
            <div class="text-5xl font-bold">{pointsDisplay}</div>
        </div>

        <progress
            class="progress progress-accent w-full"
            value={data.point_total % 1000}
            max="1000"
        ></progress>
        <p class="text-sm opacity-75">
            {data.point_total % 1000}/1000 points to next milestone
        </p>
    </div>
</div>

<style>
    :global(.progress-accent) {
        @apply progress-accent;
    }
</style>
