/*
 * OpenBook: Interactive Online Textbooks
 * © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 */

import type { BreadcrumbsItem } from "../stores/breadcrumbs.js";
import type { RouteDetail }     from "svelte-spa-router";

// import {i18n}                   from "../stores/i18n.js";
import {breadcrumbs}            from "../stores/breadcrumbs.js";
import {wrap}                   from "svelte-spa-router/wrap";

const HOME_BREADCRUMB: BreadcrumbsItem = {
    href:  "#/",
    label: "Home",
};

/**
 * Set breadcrumbs for a route when it is matched.
 */
function setBreadcrumbsLine(items: BreadcrumbsItem[]) {
    return (_detail: RouteDetail): boolean => {
        breadcrumbs.set([HOME_BREADCRUMB, ...items]);
        return true;
    };
}

export default {
    "/": wrap({
        asyncComponent: () => import("./pages/home/HomePage.svelte"),
        conditions: [setBreadcrumbsLine([])],
    }),

    // "/book/page/:pageNumber": wrap({
    //     asyncComponent: () => import("./pages/book/BookContentPage.svelte"),
    //     conditions: [setPageNumber],
    // }),

    "*": wrap({
        asyncComponent: () => import("./pages/errors/NotFoundPage.svelte"),
        conditions: [setBreadcrumbsLine([
            {
                href:  "",
                label: "Not Found", //i18n.value.Error.Page.NotFound.Title,
            },
        ])],
    }),
};
