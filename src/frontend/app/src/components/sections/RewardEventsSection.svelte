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
Section displaying recent reward events and activity timeline.
-->

<script lang="ts">
    export let events: Array<{
        id: string;
        account_id: string;
        reward_id: string;
        event_type: string;
        points_delta: number;
        created_at: string;
        context: Record<string, unknown>;
    }> = [];

    const eventEmojis: Record<string, string> = {
        "quiz_completed": "❓",
        "course_finished": "🎓",
        "peer_helped": "🤝",
        "streak_maintained": "🔥",
        "achievement_unlocked": "🏅",
        "default": "📌",
    };

    function getEventEmoji(eventType: string): string {
        return eventEmojis[eventType] || eventEmojis["default"];
    }

    function formatDate(dateString: string): string {
        const date = new Date(dateString);
        const now = new Date();
        const diffMs = now.getTime() - date.getTime();
        const diffMins = Math.floor(diffMs / 60000);
        const diffHours = Math.floor(diffMs / 3600000);
        const diffDays = Math.floor(diffMs / 86400000);

        if (diffMins < 60) {
            return `${diffMins}m ago`;
        } else if (diffHours < 24) {
            return `${diffHours}h ago`;
        } else if (diffDays < 7) {
            return `${diffDays}d ago`;
        }
        return date.toLocaleDateString();
    }
</script>

<div class="card bg-base-100 shadow-xl">
    <div class="card-body">
        <h2 class="card-title text-2xl mb-6">📊 Recent Activity</h2>

        {#if events.length === 0}
            <p class="text-center text-gray-500 py-8">
                No reward events yet. Complete activities to earn rewards!
            </p>
        {:else}
            <div class="timeline timeline-vertical">
                {#each events as event, index}
                    <div class="timeline-item">
                        <div class="timeline-start text-sm font-bold">
                            {formatDate(event.created_at)}
                        </div>
                        <div class="timeline-middle">
                            <div class="bg-primary rounded-full w-8 h-8 flex items-center justify-center text-white text-lg">
                                {getEventEmoji(event.event_type)}
                            </div>
                        </div>
                        <div class="timeline-end mb-10">
                            <div class="card bg-base-200">
                                <div class="card-body p-4">
                                    <div class="flex items-center justify-between">
                                        <div>
                                            <h4 class="font-bold capitalize">
                                                {event.event_type.replace(/_/g, " ")}
                                            </h4>
                                            <p class="text-sm text-gray-600">
                                                {#each Object.entries(event.context) as [key, value]}
                                                    <span class="badge badge-sm mr-2">
                                                        {key}: {value}
                                                    </span>
                                                {/each}
                                            </p>
                                        </div>
                                        <div class="text-right">
                                            <div
                                                class="text-2xl font-bold {event.points_delta > 0
                                                    ? 'text-success'
                                                    : 'text-error'}"
                                            >
                                                {event.points_delta > 0 ? "+" : ""}{event.points_delta}
                                            </div>
                                            <span class="text-xs text-gray-500">points</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                {/each}
            </div>
        {/if}
    </div>
</div>
