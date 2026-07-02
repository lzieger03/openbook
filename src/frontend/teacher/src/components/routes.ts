/*
 * OpenBook: Interactive Online Textbooks - Server
 * © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
 * Ledejna Salihi (@LedejnaSalihi)
 * Lars Zieger (@lzieger03)
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 */

// Hash routes for the teacher microfrontend.
import CourseListPage from "./pages/CourseListPage.svelte";
import CourseDetailPage from "./pages/CourseDetailPage.svelte";

export default {
    "/": CourseListPage,
    "/courses/:id": CourseDetailPage,
    "*": CourseListPage,
};
