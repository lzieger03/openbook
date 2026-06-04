/*
 * OpenBook: Interactive Online Textbooks
 * © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 */

import type { BreadcrumbsCallback } from "../stores/breadcrumbs.js";
import { breadcrumbs }              from "../stores/breadcrumbs.js";
import { wrap }                     from "svelte-spa-router/wrap";

/**
 * Set breadcrumbs callback for a matched route and prefix it with a fixed
 * item for the home page.
 */
function _breadcrumbs(fn?: BreadcrumbsCallback) {
    return function() {
        breadcrumbs.set((i18n) => {
            let result = [{ href: "#/", label: i18n.Home.Title }];
            if (fn) result = [...result, ...fn(i18n)];
            return result;
        });

        return true;
    }
}

export default {
    "/": wrap({
        asyncComponent: () => import("./pages/home/HomePage.svelte"),
        conditions: [_breadcrumbs()],
    }),

    "*": wrap({
        asyncComponent: () => import("./pages/errors/NotFoundPage.svelte"),
        conditions: [_breadcrumbs(i18n => [{ href: "", label: i18n.Error.Page.NotFound.Title }])],
    }),
};
