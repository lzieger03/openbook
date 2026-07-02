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
Renders the app-wide toast stack (bottom-right). Driven by the shared toast store.
-->
<script lang="ts">
    import {toasts} from "../../stores/toast.store.js";

    const icon = {success: "✓", error: "✕", info: "ℹ"} as const;
</script>

<div class="toast-stack" aria-live="polite" aria-atomic="false">
    {#each $toasts as toast (toast.id)}
        <div class="toast-item {toast.kind}" role="status">
            <span class="toast-icon" aria-hidden="true">{icon[toast.kind]}</span>
            <span class="toast-msg">{toast.message}</span>
            <button type="button" class="toast-close" aria-label="Dismiss" onclick={() => toasts.dismiss(toast.id)}>×</button>
        </div>
    {/each}
</div>

<style>
    .toast-stack {
        position: fixed;
        right: 1.25rem;
        bottom: 1.25rem;
        z-index: 100;
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        max-width: min(24rem, calc(100vw - 2rem));
    }

    .toast-item {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        padding: 0.7rem 0.85rem;
        border-radius: 0.7rem;
        background: var(--color-base-100);
        border: 1px solid color-mix(in oklab, var(--color-base-content) 15%, transparent);
        box-shadow: 0 8px 24px color-mix(in oklab, var(--color-base-content) 22%, transparent);
        animation: toast-in 0.18s ease;
    }

    .toast-icon {
        flex: 0 0 auto;
        display: grid;
        place-items: center;
        width: 1.5rem;
        height: 1.5rem;
        border-radius: 999px;
        font-size: 0.8rem;
        font-weight: 800;
        color: #fff;
    }

    .toast-item.success .toast-icon {
        background: var(--color-success);
    }

    .toast-item.error .toast-icon {
        background: var(--color-error);
    }

    .toast-item.info .toast-icon {
        background: var(--color-primary);
    }

    .toast-msg {
        flex: 1 1 auto;
        min-width: 0;
        font-size: 0.9rem;
        color: var(--color-base-content);
    }

    .toast-close {
        flex: 0 0 auto;
        border: none;
        background: none;
        cursor: pointer;
        font-size: 1.1rem;
        line-height: 1;
        color: color-mix(in oklab, var(--color-base-content) 55%, transparent);
    }

    .toast-close:hover {
        color: var(--color-base-content);
    }

    @keyframes toast-in {
        from {
            opacity: 0;
            transform: translateY(0.5rem);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
</style>
