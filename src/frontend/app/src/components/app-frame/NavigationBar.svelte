<!--
OpenBook: Interactive Online Textbooks
© 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.
-->

<!--
@component
Top navigation page of the application frame.
-->

<script lang="ts">
    import {i18n}        from "../../stores/i18n.js";
    import AvatarDefault from "./img/AvatarDefault.jpg";

    let avatar = $state(AvatarDefault);
</script>

<!-- Navbar -->
<div class="navbar border-0 bg-base-100/85 backdrop-blur-md top-0 sticky">
    <!-- Breadcrumb with current location -->
    <div class="flex-1">
        Breadcrumb
    </div>

    <!-- Page menu -->

    <!-- Search and user menu -->
    <div class="flex gap-2">
        <!-- Search input -->
        <input type="text" placeholder="{$i18n.ApplicationFrame.Search.Placeholder}" class="input input-bordered w-24 md:w-auth"/>

        <!-- User menu -->
        <div class="dropdown dropdown-end">
            <div tabindex="0" role="button" class="btn btn-ghost btn-circle avatar">
                <div class="w-10 rounded-full">
                    <img src="{avatar}" alt="{$i18n.ApplicationFrame.UserMenu.AltText}"/>
                </div>
            </div>
            <ul tabindex="-1" class="menu menu-sm dropdown-content bg-base-100 rounded-box z-1 mt-3 w-52 p-2 shadow">
                <li>
                    <a href="#/accounts/profile">{$i18n.ApplicationFrame.UserMenu.Profile}</a>
                </li>
                <li>
                    <a href="#/accounts/settings">{$i18n.ApplicationFrame.UserMenu.Settings}</a>
                </li>
                <li>
                    <a href="#/accounts/logout">{$i18n.ApplicationFrame.UserMenu.Logout}</a>
                </li>
            </ul>
        </div>
    </div>
</div>
