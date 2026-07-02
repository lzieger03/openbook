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
Card displaying a single skill with progress visualization.
-->

<script lang="ts">
    export let data: {
        id: string;
        name: string;
        description: string;
        icon_path: string;
        level: number;
        progress: number;
    };

    const skillEmojis: Record<string, string> = {
        "python": "🐍",
        "javascript": "📘",
        "design": "🎨",
        "leadership": "👑",
        "communication": "💬",
        "teamwork": "🤝",
        "problem solving": "🧩",
        "default": "⭐",
    };

    const emoji = skillEmojis[data.name.toLowerCase()] || skillEmojis["default"];

    function getLevelColor(level: number): string {
        switch (level) {
            case 1:
                return "badge-warning";
            case 2:
                return "badge-info";
            case 3:
                return "badge-primary";
            case 4:
                return "badge-success";
            case 5:
                return "badge-accent";
            default:
                return "badge-ghost";
        }
    }
</script>

<div class="card bg-base-200 shadow">
    <div class="card-body p-4">
        <div class="flex items-start justify-between mb-3">
            <div>
                <h3 class="card-title text-lg">
                    {#if data.icon_path}
                        <img src={data.icon_path} alt="" class="inline-block w-5 h-5 mr-1 rounded-sm align-middle" />
                    {:else}
                        {emoji}
                    {/if}
                    {data.name}
                </h3>
                {#if data.description}
                    <p class="text-sm text-gray-600 mt-1">{data.description}</p>
                {/if}
            </div>
            <div class={`badge ${getLevelColor(data.level)}`}>
                Level {data.level}
            </div>
        </div>

        <div class="space-y-2">
            <div class="flex justify-between text-sm">
                <span class="text-gray-600">Progress</span>
                <span class="font-semibold">{data.progress.toFixed(1)}%</span>
            </div>
            <progress
                class="progress w-full"
                value={data.progress}
                max="100"
            ></progress>
        </div>

    </div>
</div>

<style>
    :global(.progress) {
        @apply progress-primary;
    }
</style>
