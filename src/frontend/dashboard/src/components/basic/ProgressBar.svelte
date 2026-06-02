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
Gradient progress bar driven by a percentage value (0–100).
-->
<script lang="ts">
    let {value, label = ""}: {value: number; label?: string} = $props();

    const percent = $derived(Math.min(100, Math.max(0, value)));
</script>

<div
    class="progress-track"
    role="progressbar"
    aria-valuenow={Math.round(percent)}
    aria-valuemin={0}
    aria-valuemax={100}
    aria-label={label}
>
    <div class="progress-fill" style="width: {percent}%"></div>
</div>

<style>
    .progress-track {
        height: 0.9rem;
        border-radius: 999px;
        overflow: hidden;
        background: color-mix(in oklab, var(--color-base-content) 12%, transparent);
    }

    .progress-fill {
        height: 100%;
        border-radius: 999px;
        background: linear-gradient(90deg, var(--color-warning), var(--color-success));
        box-shadow: 0 0 12px color-mix(in oklab, var(--color-success) 45%, transparent);
        transition: width 0.3s ease;
    }
</style>
