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
import CourseChatPage from "./pages/CourseChatPage.svelte";
import QuizPage from "./pages/QuizPage.svelte";
import ExamPage from "./pages/ExamPage.svelte";
import ContentPage from "./pages/ContentPage.svelte";
import GamesPage from "./pages/GamesPage.svelte";
import MemoryGamePage from "./pages/MemoryGamePage.svelte";
import FlashcardsGamePage from "./pages/FlashcardsGamePage.svelte";
import HangmanGamePage from "./pages/HangmanGamePage.svelte";

export default {
    "/": DashboardPage,
    "/profile": ProfileEditPage,
    "/chat/:id": CourseChatPage,
    "/quiz/:id": QuizPage,
    "/exam/:id": ExamPage,
    "/content/:id": ContentPage,
    "/games/:id": GamesPage,
    "/games/:id/memory": MemoryGamePage,
    "/games/:id/flashcards": FlashcardsGamePage,
    "/games/:id/hangman": HangmanGamePage,
    "*": DashboardPage,
};
