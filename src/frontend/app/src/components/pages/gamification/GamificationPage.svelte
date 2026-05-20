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
Gamification dashboard showing rewards, account points, skills, and reward events.
-->

<script lang="ts">
    import { onMount } from "svelte";
    import RewardsSection from "../../sections/RewardsSection.svelte";
    import SkillsSection from "../../sections/SkillsSection.svelte";
    import AccountPointsCard from "../../cards/AccountPointsCard.svelte";
    import RewardEventsSection from "../../sections/RewardEventsSection.svelte";

    interface AccountPoints {
        id: string;
        account_id: string;
        point_total: number;
        updated_at: string;
    }

    interface Reward {
        id: string;
        reward_type: string;
        value: number;
        description: string;
    }

    interface Skill {
        id: string;
        account_id: string;
        name: string;
        level: number;
        progress: number;
    }

    interface RewardEvent {
        id: string;
        account_id: string;
        reward_id: string;
        event_type: string;
        points_delta: number;
        created_at: string;
        context: Record<string, unknown>;
    }

    let accountPoints: AccountPoints | null = null;
    let rewards: Reward[] = [];
    let skills: Skill[] = [];
    let rewardEvents: RewardEvent[] = [];
    let loading = true;
    let error: string | null = null;

    onMount(async () => {
        try {
            // TODO: Replace with actual API calls once viewsets are created
            // For now, using mock data
            accountPoints = {
                id: "mock-id",
                account_id: "current-user",
                point_total: 1250,
                updated_at: new Date().toISOString(),
            };

            rewards = [
                {
                    id: "reward-1",
                    reward_type: "quiz_completion",
                    value: 50,
                    description: "Reward for completing a quiz",
                },
                {
                    id: "reward-2",
                    reward_type: "course_finish",
                    value: 200,
                    description: "Reward for completing a course",
                },
                {
                    id: "reward-3",
                    reward_type: "peer_help",
                    value: 25,
                    description: "Reward for helping a peer",
                },
            ];

            skills = [
                {
                    id: "skill-1",
                    account_id: "current-user",
                    name: "Problem Solving",
                    level: 3,
                    progress: 45.5,
                },
                {
                    id: "skill-2",
                    account_id: "current-user",
                    name: "Communication",
                    level: 2,
                    progress: 72.0,
                },
                {
                    id: "skill-3",
                    account_id: "current-user",
                    name: "Teamwork",
                    level: 4,
                    progress: 15.3,
                },
            ];

            rewardEvents = [
                {
                    id: "event-1",
                    account_id: "current-user",
                    reward_id: "reward-1",
                    event_type: "quiz_completed",
                    points_delta: 50,
                    created_at: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
                    context: { quiz_id: "q-101", score: 95 },
                },
                {
                    id: "event-2",
                    account_id: "current-user",
                    reward_id: "reward-3",
                    event_type: "peer_helped",
                    points_delta: 25,
                    created_at: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(),
                    context: { peer_id: "user-42", topic: "calculus" },
                },
            ];

            loading = false;
        } catch (err) {
            error = String(err);
            loading = false;
        }
    });
</script>

<div class="container mx-auto p-6">
    <div class="mb-8">
        <h1 class="text-4xl font-bold mb-2">🎮 Gamification Dashboard</h1>
        <p class="text-lg text-gray-600">
            Track your progress, earn rewards, and develop your skills!
        </p>
    </div>

    {#if loading}
        <div class="flex justify-center items-center h-64">
            <span class="loading loading-spinner loading-lg"></span>
        </div>
    {:else if error}
        <div class="alert alert-error">
            <svg
                xmlns="http://www.w3.org/2000/svg"
                class="stroke-current shrink-0 h-6 w-6"
                fill="none"
                viewBox="0 0 24 24"
            >
                <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M10 14l-2-2m0 0l-2-2m2 2l2-2m-2 2l-2 2m8-8l2 2m0 0l2 2m-2-2l-2 2m2-2l2-2"
                />
            </svg>
            <span>{error}</span>
        </div>
    {:else}
        <!-- Main metrics row -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            {#if accountPoints}
                <AccountPointsCard data={accountPoints} />
            {/if}

            <div class="card bg-base-100 shadow-xl">
                <div class="card-body">
                    <h2 class="card-title text-2xl">⭐ Skills</h2>
                    <p class="text-4xl font-bold text-primary">{skills.length}</p>
                    <p class="text-sm text-gray-500">Active skills</p>
                </div>
            </div>

            <div class="card bg-base-100 shadow-xl">
                <div class="card-body">
                    <h2 class="card-title text-2xl">🏆 Rewards</h2>
                    <p class="text-4xl font-bold text-secondary">{rewards.length}</p>
                    <p class="text-sm text-gray-500">Available rewards</p>
                </div>
            </div>
        </div>

        <!-- Skills section -->
        <div class="mb-8">
            <SkillsSection {skills} />
        </div>

        <!-- Rewards section -->
        <div class="mb-8">
            <RewardsSection {rewards} />
        </div>

        <!-- Recent events section -->
        <div class="mb-8">
            <RewardEventsSection events={rewardEvents} />
        </div>
    {/if}
</div>

<style>
    :global(body) {
        @apply bg-base-200;
    }
</style>
