/*
 * OpenBook: Interactive Online Textbooks
 * © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 */

import * as i18n from "./stores/i18n.js";
import {untrack} from "svelte";

declare global {
    interface Window {
        /**
         * Public exports for usage in the study books
         */
        OpenBook: {
            /**
             * Get translated texts or customize the translations
             */
            i18n: typeof i18n;
        },

        /**
         * Workaround for a possible bug in svelte compilation with esbuild.
         * svelte-spa-router in its `Router.svelte` file imports `untrack` from svelte,
         * but it seems not to be compiled in.
         */
        untrack: typeof untrack,
    }
}

window.OpenBook = {i18n};
window.untrack  = untrack;
