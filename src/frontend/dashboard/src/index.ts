/*
 * OpenBook: Interactive Online Textbooks - Server
 * © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 */

// Entry point: apply theme, then mount the dashboard onto the page body.
import "./tailwind.css";
import "./index.css";

import {mount}    from "svelte";
import {initTheme} from "./theme.js";
import DashboardApp from "./components/DashboardApp.svelte";

initTheme();

mount(DashboardApp, {target: document.body});
