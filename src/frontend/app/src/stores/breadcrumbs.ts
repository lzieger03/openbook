/*
 * OpenBook: Interactive Online Textbooks
 * © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 */

import type { I18N }     from "../i18n/index.js";
import { WritableStore } from "../utils/store.js";

/**
 * A single item in the breadcrumbs line
 */
export type BreadcrumbsItem = {href:  string, label: string}

/**
 * Callback function to determine the breadcrumb items of the current page. Gets the
 * `i18n` store passed so that it will automatically be recalled when the user changes
 * the current language.
 */
export type BreadcrumbsCallback = (i18n: I18N) => BreadcrumbsItem[];

/**
 * Writable store for the current breadcrumbs callback function.
 */
export const breadcrumbs = new WritableStore<BreadcrumbsCallback>(() => []);
