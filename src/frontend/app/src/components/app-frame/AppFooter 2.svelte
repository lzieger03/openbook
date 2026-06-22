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
Reusable application footer.
-->
<footer class="app-footer">
    <div class="footer-content">
        <span>Copyright 2026 | ElisaAI</span>
    </div>
</footer>

<style>
    .app-footer {
        padding: 1rem 1.5rem 1.5rem;
        border-top: 1px solid color-mix(in oklab, var(--color-base-content) 12%, transparent);
        background: var(--color-base-100);
    }

    .footer-content {
        text-align: center;
        font-size: 0.8rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: color-mix(in oklab, var(--color-base-content) 70%, transparent);
    }
</style>
