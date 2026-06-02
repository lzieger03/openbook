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
    <RadarChart data={axes} />
</section>

<style>
    .panel {
        background: var(--color-base-100);
        border-radius: 1rem;
        padding: 1.5rem;
        box-shadow: 0 0 24px color-mix(in oklab, var(--color-primary) 10%, transparent);
    }

    .panel-title {
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 1rem;
        color: var(--color-base-content);
    }
</style>
