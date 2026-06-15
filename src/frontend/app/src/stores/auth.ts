/*
 * OpenBook: Interactive Online Textbooks
 * © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 */

import type { authPaths }     from "./api.js";
import type { authSchemas }   from "./api.js";
import type { ClientWrapper } from "./api.js";

import api                    from "./api.js";
import { ReadableStore }      from "../utils/store.js";

export type AuthenticationStatus =
    authSchemas["AuthenticatedResponse"]  |
    authSchemas["AuthenticationResponse"] |
    authSchemas["SessionGoneResponse"]    |
    undefined;

export type LoginResult =
    | { success: true }
    | { success: false; errors: { code: string; param?: string; message: string }[] };

/**
 * Svelte readable store that periodically checks the authentication status of the user's
 * session with the backend. It tracks whether the user is logged in, logged out, or if
 * their session has timed out.
 */
export class AuthStore extends ReadableStore<AuthenticationStatus> {
    /**
     * API client wrapper for fetching the authentication session from the backend.
     */
    backend!: ClientWrapper<authPaths, "/auth-api/{client}/v1/auth/session">;

    private _initPromise: Promise<void> | null = null;

    /**
     * Initializes the authentication store with an initial status of `undefined`.
     * The real status becomes available once `init()` was called and will then
     * be periodically updated in background.
     */
    constructor() {
        super(undefined);
    }

    /**
     * Initializes the client API wrapper, runs the initial session check, and
     * registers a periodic interval to keep checking the session status.
     * Safe to call multiple times — initialization only runs once.
     */
    init(): Promise<void> {
        if (!this._initPromise) {
            this._initPromise = this._doInit();
        }
        return this._initPromise;
    }

    private async _doInit(): Promise<void> {
        this.backend = await api.auth("/auth-api/{client}/v1/auth/session", "error-return");
        await this.recheckAuthSession();

        // TODO: Backend setting for the check interval
        let check_interval_s = 300;
        window.setInterval(this.recheckAuthSession.bind(this), check_interval_s * 1000);
    }

    /**
     * Queries the backend API to retrieve the current session status and updates
     * the store value. This is called periodically after the `init()` method was
     * called. But it can also be called manually to force a recheck.
     */
    async recheckAuthSession() {
        if (!this.backend) return;

        let response = await this.backend.GET({
            params: {
                path: {
                    client: "browser"
                }
            },
        });

        this.set(response.data || response.error);
    }

    /**
     * Logs in with a username/email and password. Automatically rechecks the
     * session on success so the store value updates reactively.
     */
    async login(usernameOrEmail: string, password: string): Promise<LoginResult> {
        const loginBackend = await api.auth("/auth-api/{client}/v1/auth/login", "error-return");

        const credentials: authSchemas["Login"] = usernameOrEmail.includes("@")
            ? { email: usernameOrEmail, password }
            : { username: usernameOrEmail, password };

        const result = await loginBackend.POST({
            params: { path: { client: "browser" } },
            body:   credentials,
        });

        if (!result.error) {
            await this.recheckAuthSession();
            return { success: true };
        }

        const errorBody = result.error as { status?: number; errors?: { code: string; param?: string; message: string }[] } | undefined;

        // 409 = session conflict, e.g. already logged in — recheck and treat as success
        if (errorBody?.status === 409) {
            await this.recheckAuthSession();
            return { success: true };
        }

        return { success: false, errors: errorBody?.errors ?? [] };
    }
}

export const auth = new AuthStore();
