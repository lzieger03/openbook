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
Section displaying user skills with levels and progress.
-->

<script lang="ts">
    import SkillCard from "../cards/SkillCard.svelte";

    export let skills: Array<{
        id: string;
        account_id: string;
        name: string;
        level: number;
        progress: number;
    }> = [];

    let showAddForm = false;
    let newSkillName = "";
    let newSkillLevel = 1;

    function addSkill() {
        if (newSkillName.trim()) {
            skills = [
                ...skills,
                {
                    id: `skill-${Date.now()}`,
                    account_id: "current-user",
                    name: newSkillName,
                    level: newSkillLevel,
                    progress: 0,
                },
            ];
            newSkillName = "";
            newSkillLevel = 1;
            showAddForm = false;
        }
    }
</script>

<div class="card bg-base-100 shadow-xl">
    <div class="card-body">
        <div class="flex items-center justify-between mb-6">
            <h2 class="card-title text-2xl">⭐ Your Skills</h2>
            <button
                class="btn btn-primary btn-sm"
                on:click={() => (showAddForm = !showAddForm)}
            >
                {showAddForm ? "Cancel" : "+ Add Skill"}
            </button>
        </div>

        {#if showAddForm}
            <div class="form-control gap-4 mb-6 p-4 bg-base-200 rounded-lg">
                <input
                    type="text"
                    placeholder="Skill name (e.g., Python, Leadership, Design)"
                    class="input input-bordered"
                    bind:value={newSkillName}
                />
                <div class="flex gap-4">
                    <select class="select select-bordered flex-1" bind:value={newSkillLevel}>
                        {#each [1, 2, 3, 4, 5] as level}
                            <option value={level}>Level {level}</option>
                        {/each}
                    </select>
                    <button
                        class="btn btn-success"
                        on:click={addSkill}
                        disabled={!newSkillName.trim()}
                    >
                        Add
                    </button>
                </div>
            </div>
        {/if}

        {#if skills.length === 0}
            <p class="text-center text-gray-500 py-8">
                No skills yet. Start adding skills to track your progress!
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
