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
Section displaying available rewards.
-->

<script lang="ts">
    import RewardCard from "../cards/RewardCard.svelte";

    export let rewards: Array<{
        id: string;
        reward_type: string;
        value: number;
        description: string;
    }> = [];

    let showAddForm = false;
    let newRewardType = "";
    let newRewardValue = 0;
    let newRewardDesc = "";

    function addReward() {
        if (newRewardType.trim() && newRewardValue > 0) {
            rewards = [
                ...rewards,
                {
                    id: `reward-${Date.now()}`,
                    reward_type: newRewardType,
                    value: newRewardValue,
                    description: newRewardDesc,
                },
            ];
            newRewardType = "";
            newRewardValue = 0;
            newRewardDesc = "";
            showAddForm = false;
        }
    }
</script>

<div class="card bg-base-100 shadow-xl">
    <div class="card-body">
        <div class="flex items-center justify-between mb-6">
            <h2 class="card-title text-2xl">🏆 Available Rewards</h2>
            <button
                class="btn btn-success btn-sm"
                on:click={() => (showAddForm = !showAddForm)}
            >
                {showAddForm ? "Cancel" : "+ Create Reward"}
            </button>
        </div>

        {#if showAddForm}
            <div class="form-control gap-4 mb-6 p-4 bg-base-200 rounded-lg">
                <input
                    type="text"
                    placeholder="Reward type (e.g., quiz_completion, course_finish)"
                    class="input input-bordered"
                    bind:value={newRewardType}
                />
                <input
                    type="number"
                    placeholder="Points value"
                    class="input input-bordered"
                    bind:value={newRewardValue}
                    min="1"
                />
                <textarea
                    placeholder="Description (optional)"
                    class="textarea textarea-bordered h-20"
                    bind:value={newRewardDesc}
                ></textarea>
                <div class="flex gap-4">
                    <button
                        class="btn btn-success flex-1"
                        on:click={addReward}
                        disabled={!newRewardType.trim() || newRewardValue <= 0}
                    >
                        Create Reward
                    </button>
                </div>
            </div>
        {/if}

        {#if rewards.length === 0}
            <p class="text-center text-gray-500 py-8">
                No rewards yet. Create rewards to motivate users!
            </p>
        {:else}
            <div class="overflow-x-auto">
                <table class="table table-compact w-full">
                    <thead>
                        <tr>
                            <th>Reward Type</th>
                            <th class="text-right">Points</th>
                            <th>Description</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {#each rewards as reward (reward.id)}
                            <tr class="hover">
                                <td>
                                    <span class="badge badge-primary">
                                        {reward.reward_type}
                                    </span>
                                </td>
                                <td class="text-right font-bold text-lg">
                                    {reward.value}
                                </td>
                                <td class="text-sm text-gray-600">
                                    {reward.description || "-"}
                                </td>
                                <td>
                                    <div class="flex gap-2">
                                        <button class="btn btn-xs btn-ghost">Edit</button>
                                        <button class="btn btn-xs btn-ghost text-error"
                                            >Delete</button
                                        >
                                    </div>
                                </td>
                            </tr>
                        {/each}
                    </tbody>
                </table>
            </div>
        {/if}
    </div>
</div>
