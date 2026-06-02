/*
 * OpenBook: Interactive Online Textbooks - Server
 * © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 */

// Hash routes for the dashboard microfrontend.
import DashboardPage from "./pages/DashboardPage.svelte";
import ProfileEditPage from "./pages/ProfileEditPage.svelte";

export default {
    "/": DashboardPage,
    "/profile": ProfileEditPage,
    "*": DashboardPage,
};
