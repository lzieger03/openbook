/*
 * OpenBook: Interactive Online Textbooks
 * © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 */

import type { Client }                 from "openapi-fetch";
import type { paths as authPaths }     from "./openapi/auth.js";
import type { paths as openbookPaths } from "./openapi/openbook.js";
import type { WebSocketMessage }       from "./websocket.js";

import createClient                    from "openapi-fetch";
import middlewares                     from "./middleware/index.js";
import { fetchWithRetry }              from "./retry.js";
import { WebSocketClient }             from "./websocket.js";

let _baseUrl = "";

function isLoopbackHost(hostname: string): boolean {
    return hostname === "localhost" || hostname === "127.0.0.1" || hostname === "::1";
}

function normalizeBaseUrl(value: string): string {
    let configuredUrl = new URL(value || window.location.origin, window.location.origin);
    const currentUrl = new URL(window.location.origin);

    if (
        isLoopbackHost(configuredUrl.hostname)
        && isLoopbackHost(currentUrl.hostname)
        && configuredUrl.protocol === currentUrl.protocol
        && configuredUrl.port === currentUrl.port
    ) {
        configuredUrl = currentUrl;
    }

    let url = configuredUrl.toString();

    while (url.endsWith("/")) {
        url = url.slice(0, url.length - 1);
    }

    return url;
}

/**
 * Call the well-known endpoint `server.url` to get the full API backend
 * base URL. The result will be cached. Note, that this is encapsulated
 * in a function to avoid a top-level import, which esbuild only supports
 * in the entry-point file.
 *
 * @returns Backend base URL
 */
async function getBaseUrl(): Promise<string> {
    if (_baseUrl) return _baseUrl;

    let response = await fetch("server.url");
    _baseUrl = normalizeBaseUrl((await response.text()).trim());

    return _baseUrl;
}

/**
 * Register middlewares for the given API client object.
 * @param client API client
 */
function registerMiddlewares<Paths extends object, Media extends `${string}/${string}`>(client: Client<Paths, Media>): void {
    for (let middleware of middlewares) {
        client.use(middleware);
    }
}

/**
 * Factory for pre-configured API client objects. Unfortunately, we must wrap access
 * in async accessor methods to avoid top-level imports in this file that would break
 * the esbuild build output: In mixed ESM/CommonJS projects, the esbuild esm output
 * format only supports top-level imports in the entry-point file.
 * */
export default {
    /**
     * Factory method for authentication API clients.
     * @returns API client for the authentication API
     */
    auth: async () => {
        let baseUrl = await getBaseUrl();
        let client  = createClient<authPaths>({baseUrl, fetch: fetchWithRetry});

        registerMiddlewares(client);
        return client;
    },

    /**
     * Factory method for OpenBook REST API clients.
     * @returns API client for the OpenBook REST API
     */
    openbook: async () => {
        let baseUrl = await getBaseUrl();
        let client  = createClient<openbookPaths>({baseUrl, fetch: fetchWithRetry});

        registerMiddlewares(client);
        return client;
    },

    /**
     * Factory method for new WebSocket clients.
     * @param suffix URL suffix (without the `/ws` prefix), e.g. `/ai/chat`
     * @returns A new WebSocket client for the OpenBook WebSocket API
     */
    ws: async <SentMessages extends WebSocketMessage, ReceivedMessages extends WebSocketMessage>(suffix: string) => {
        if (!suffix.startsWith("/")) suffix = `/${suffix}`;

        const wsUrl = new URL(`/ws${suffix}`, await getBaseUrl());
        if (wsUrl.protocol === "http:") wsUrl.protocol = "ws:";
        if (wsUrl.protocol === "https:") wsUrl.protocol = "wss:";

        return new WebSocketClient<SentMessages, ReceivedMessages>(wsUrl.toString());
    },
};
