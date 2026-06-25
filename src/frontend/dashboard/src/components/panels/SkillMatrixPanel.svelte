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
"Skills" panel: a list of the learner's skills, each showing its level and a
progress bar towards the next level — styled like the course list.
-->
<script lang="ts">
    import ProgressBar from "../basic/ProgressBar.svelte";
    import type {DashboardSkill} from "../../data/dashboard.js";

    let {skills}: {skills: DashboardSkill[]} = $props();

    const isEmpty = $derived(skills.length === 0);
</script>

<section class="card panel">
    <h2 class="panel-title">Skills</h2>

    <div class="panel-body">
        {#if isEmpty}
            <p class="empty">No skills yet. Complete tasks and quizzes in your courses to earn skills.</p>
        {:else}
            {#each skills as skill (skill.id)}
                <div class="skill-row">
                    <div class="skill-head">
                        <span class="skill-name">{skill.name}</span>
                        <span class="skill-level">Lv {skill.level}</span>
                    </div>
                    <div class="skill-bar">
                        <ProgressBar value={skill.progress} label={`${skill.name} progress`} />
                        <span class="skill-percent">{Math.round(skill.progress)}%</span>
                    </div>
                </div>
            {/each}
        {/if}
    </div>
</section>

<style>
    /* Fill the remaining height of the right column; the body scrolls if needed. */
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
        flex: 0 0 auto;
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        color: var(--color-base-content);
    }

    .panel-body {
        flex: 1;
        min-height: 0;
        overflow-y: auto;
        padding-right: 0.5rem;
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
        /* Firefox: keep the track transparent so the bar only shows on hover. */
        scrollbar-width: thin;
        scrollbar-color: transparent transparent;
    }

    .panel-body:hover {
        scrollbar-color: color-mix(in oklab, var(--color-base-content) 20%, transparent) transparent;
    }

    .panel-body::-webkit-scrollbar {
        width: 0.5rem;
    }

    .panel-body::-webkit-scrollbar-thumb {
        border-radius: 999px;
        background: transparent;
    }

    .panel-body:hover::-webkit-scrollbar-thumb {
        background: color-mix(in oklab, var(--color-base-content) 20%, transparent);
    }

    /* One skill per card, mirroring the course cards in "My Learning". */
    .skill-row {
        background: color-mix(in oklab, var(--color-base-200) 50%, transparent);
        border: 1px solid color-mix(in oklab, var(--color-base-content) 8%, transparent);
        border-radius: 1rem;
        padding: 0.9rem 1.1rem;
    }

    .skill-head {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 0.75rem;
        margin-bottom: 0.6rem;
    }

    .skill-name {
        font-size: 1.05rem;
        font-weight: 700;
        color: var(--color-base-content);
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .skill-level {
        flex: 0 0 auto;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.03em;
        padding: 0.15rem 0.6rem;
        border-radius: 999px;
        color: var(--color-primary-content);
        background: var(--color-primary);
        box-shadow: 0 0 12px color-mix(in oklab, var(--color-primary) 40%, transparent);
    }

    .skill-bar {
        display: grid;
        grid-template-columns: 1fr 3rem;
        align-items: center;
        gap: 0.75rem;
    }

    .skill-percent {
        font-weight: 700;
        text-align: right;
        color: var(--color-base-content);
    }

    .empty {
        color: color-mix(in oklab, var(--color-base-content) 60%, transparent);
        padding: 1.5rem 0;
    }
</style>
