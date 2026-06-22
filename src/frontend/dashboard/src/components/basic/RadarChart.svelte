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
SVG radar (spider) chart. Each axis is one skill; the value is its progress
percentage (0–100). Renders up to six axes. The viewBox carries extra padding
so axis labels near the edges are never clipped.
-->
<script lang="ts">
    interface RadarAxis {
        label: string;
        value: number;
    }

    interface Point {
        x: number;
        y: number;
    }

    let {data, max = 6}: {data: RadarAxis[]; max?: number} = $props();

    const size = 320;
    const center = size / 2;
    const radius = 100;
    const labelDistance = radius + 24;
    const rings = [0.25, 0.5, 0.75, 1];

    // Padding around the square chart so edge labels fit without clipping. The
    // left/right labels are the widest, so the horizontal padding is larger.
    const padX = 110;
    const padY = 44;
    const viewBox = `${-padX} ${-padY} ${size + padX * 2} ${size + padY * 2}`;

    const axes = $derived(data.slice(0, max));

    function point(index: number, count: number, distance: number): Point {
        const angle = (Math.PI * 2 * index) / count - Math.PI / 2;
        return {
            x: center + distance * Math.cos(angle),
            y: center + distance * Math.sin(angle),
        };
    }

    function clamp(value: number): number {
        return Math.min(100, Math.max(0, value));
    }

    function polygon(points: Point[]): string {
        return points.map((p) => `${p.x},${p.y}`).join(" ");
    }

    const ringShapes = $derived(
        rings.map((ratio) => polygon(axes.map((_, i) => point(i, axes.length, radius * ratio)))),
    );

    const spokes = $derived(axes.map((_, i) => point(i, axes.length, radius)));

    const valuePoints = $derived(axes.map((axis, i) => point(i, axes.length, (radius * clamp(axis.value)) / 100)));

    const valueShape = $derived(polygon(valuePoints));

    const labels = $derived(
        axes.map((axis, i) => ({...point(i, axes.length, labelDistance), label: axis.label})),
    );
</script>

{#if axes.length === 0}
    <p class="empty">No skill data yet.</p>
{:else}
    <svg viewBox={viewBox} class="radar" role="img" aria-label="Skill matrix">
        {#each ringShapes as ring, i (i)}
            <polygon points={ring} class="ring" class:outer={i === ringShapes.length - 1} />
        {/each}

        {#each spokes as spoke, i (i)}
            <line x1={center} y1={center} x2={spoke.x} y2={spoke.y} class="spoke" />
        {/each}

        <polygon points={valueShape} class="value" />

        {#each valuePoints as vertex, i (i)}
            <circle cx={vertex.x} cy={vertex.y} r="3.5" class="vertex" />
        {/each}

        {#each labels as item, i (i)}
            <text
                x={item.x}
                y={item.y}
                class="label"
                font-size="13"
                text-anchor={item.x < center - 1 ? "end" : item.x > center + 1 ? "start" : "middle"}
                dominant-baseline="middle"
            >
                {item.label}
            </text>
        {/each}
    </svg>
{/if}

<style>
    .radar {
        width: 100%;
        max-width: 28rem;
        height: auto;
        margin: 0 auto;
        display: block;
        /* Safety net so long axis labels are never hard-clipped. */
        overflow: visible;
    }

    .ring {
        fill: none;
        stroke: color-mix(in oklab, var(--color-base-content) 14%, transparent);
        stroke-width: 1;
    }

    .ring.outer {
        stroke: color-mix(in oklab, var(--color-base-content) 24%, transparent);
    }

    .spoke {
        stroke: color-mix(in oklab, var(--color-base-content) 14%, transparent);
        stroke-width: 1;
    }

    .value {
        fill: color-mix(in oklab, var(--color-success) 30%, transparent);
        stroke: var(--color-success);
        stroke-width: 2;
        stroke-linejoin: round;
    }

    .vertex {
        fill: var(--color-success);
    }

    .label {
        fill: color-mix(in oklab, var(--color-base-content) 80%, transparent);
        font-weight: 600;
    }

    .empty {
        text-align: center;
        color: color-mix(in oklab, var(--color-base-content) 60%, transparent);
        padding: 2rem 0;
    }
</style>
