/*
 * OpenBook: Interactive Online Textbooks - Server
 * © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 */

// Entry point: apply theme, then mount the teacher app onto the page body.
import "./tailwind.css";
import "./index.css";

import {mount}      from "svelte";
import {initTheme}  from "./theme.js";
import TeacherApp   from "./components/TeacherApp.svelte";

initTheme();

mount(TeacherApp, {target: document.body});
