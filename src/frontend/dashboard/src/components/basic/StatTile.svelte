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
A single stat: an emoji icon above a value, with an accessible label.
-->
<script lang="ts">
    let {icon, value, label}: {icon: string; value: string; label: string} = $props();
</script>

<div class="stat-tile" title={label}>
    <span class="stat-icon" aria-hidden="true">{icon}</span>
    <span class="stat-value">{value}</span>
    <span class="sr-only">{label}</span>
</div>

<style>
    .stat-tile {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.25rem;
    }

    .stat-icon {
        font-size: 1.5rem;
        line-height: 1;
        filter: drop-shadow(0 0 8px color-mix(in oklab, var(--color-primary) 50%, transparent));
    }

    .stat-value {
        font-weight: 700;
        font-size: 1.1rem;
        color: var(--color-base-content);
    }

    .sr-only {
        position: absolute;
        width: 1px;
        height: 1px;
        padding: 0;
        margin: -1px;
        overflow: hidden;
        clip: rect(0, 0, 0, 0);
        white-space: nowrap;
        border: 0;
    }
</style>
