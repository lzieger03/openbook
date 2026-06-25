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
Section displaying user skills with levels and progress.
-->

<script lang="ts">
    import SkillCard from "../cards/SkillCard.svelte";

    export let skills: Array<{
        id: string;
        name: string;
        description: string;
        icon_path: string;
        level: number;
        progress: number;
    }> = [];
</script>

<div class="card bg-base-100 shadow-xl">
    <div class="card-body">
        <div class="flex items-center justify-between mb-6">
            <h2 class="card-title text-2xl">⭐ Your Skills</h2>
        </div>

        {#if skills.length === 0}
            <p class="text-center text-gray-500 py-8">
                No skill progress found.
            </p>
        {:else}
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {#each skills as skill (skill.id)}
                    <SkillCard data={skill} />
                {/each}
            </div>
        {/if}
    </div>
</div>
