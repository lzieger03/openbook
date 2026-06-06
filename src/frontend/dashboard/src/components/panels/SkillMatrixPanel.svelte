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
"Skill Matrix" panel: radar chart of skill progress.
-->
<script lang="ts">
    import RadarChart from "../basic/RadarChart.svelte";
    import type {DashboardSkill} from "../../data/dashboard.js";

    let {skills}: {skills: DashboardSkill[]} = $props();

    const axes = $derived(skills.map((skill) => ({label: skill.name, value: skill.progress})));
</script>

<section class="card panel">
    <h2 class="panel-title">Skill Matrix</h2>
    <div class="matrix-body">
        <!-- Frontend-only: blur the (not yet reliable) radar and overlay a notice. -->
        <div class="matrix-chart" aria-hidden="true">
            <RadarChart data={axes} />
        </div>
        <div class="matrix-overlay" role="status">
            <span class="overlay-badge">🚧 Coming soon</span>
            <span class="overlay-note">The skill matrix is still being calibrated.</span>
        </div>
    </div>
</section>

<style>
    /* Fill the remaining height of the right column and centre the radar. */
    .panel {
        flex: 1;
        min-height: 0;
        display: flex;
        flex-direction: column;
        background: var(--color-base-100);
        border-radius: 1.25rem;
        padding: 1.75rem;
        box-shadow: 0 0 24px color-mix(in oklab, var(--color-primary) 10%, transparent);
    }

    .panel-title {
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        color: var(--color-base-content);
    }

    /* Centre the radar in the remaining space without stretching its aspect ratio. */
    .matrix-body {
        position: relative;
        flex: 1;
        min-height: 0;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    /* The chart still renders; it is just blurred while the feature is unfinished. */
    .matrix-chart {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100%;
        filter: blur(6px);
        opacity: 0.55;
        pointer-events: none;
        user-select: none;
    }

    .matrix-overlay {
        position: absolute;
        inset: 0;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        text-align: center;
        padding: 1rem;
    }

    .overlay-badge {
        padding: 0.4rem 1rem;
        border-radius: 999px;
        font-weight: 700;
        letter-spacing: 0.04em;
        color: var(--color-warning);
        background: color-mix(in oklab, var(--color-warning) 16%, transparent);
        border: 1px solid color-mix(in oklab, var(--color-warning) 40%, transparent);
    }

    .overlay-note {
        font-size: 0.85rem;
        color: color-mix(in oklab, var(--color-base-content) 70%, transparent);
    }
</style>
