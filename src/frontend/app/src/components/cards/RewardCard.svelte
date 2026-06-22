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
Card displaying a reward with badge and details.
-->

<script lang="ts">
    export let data: {
        id: string;
        reward_type: string;
        value: number;
        description: string;
    };

    const rewardEmojis: Record<string, string> = {
        "quiz_completion": "❓",
        "course_finish": "🎓",
        "peer_help": "🤝",
        "streak": "🔥",
        "achievement": "🏅",
        "default": "⭐",
    };

    const emoji = rewardEmojis[data.reward_type] || rewardEmojis["default"];
</script>

<div class="card bg-base-200 shadow">
    <div class="card-body">
        <div class="flex items-start justify-between">
            <div class="flex-1">
                <h3 class="card-title text-lg">
                    {emoji} {data.reward_type}
                </h3>
                {#if data.description}
                    <p class="text-sm text-gray-600 mt-2">{data.description}</p>
                {/if}
            </div>
            <div class="text-right">
                <div class="badge badge-lg badge-success">
                    {data.value} pts
                </div>
            </div>
        </div>
    </div>
</div>
