/*
 * OpenBook: Interactive Online Textbooks - Server
 * © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 */

/**
 * Browser WebSocket wrapper with automatic reconnect (exponential backoff) and
 * action-based message routing. Mirrors the main app's client so the dashboard
 * can consume the same chanx-based WebSocket API (messages are JSON objects with
 * an `action` property). See README-websocket-api.md.
 */

/** Maximum number of connection attempts. */
const MAX_ATTEMPTS = 5;

/** Initial delay after the first failed attempt; doubled on each retry. */
const BASE_DELAY_MS = 250;

/** A connection that stays open at least this long counts as "stable". */
const STABLE_CONNECTION_MS = 4000;

/**
 * How many times to silently reconnect after the connection drops almost
 * immediately (server keeps closing it). After this, stop and report an error
 * instead of flapping between "connected" and "connecting" forever.
 */
const MAX_UNSTABLE_RETRIES = 4;

export type WSConnectionStatus = "disconnected" | "connecting" | "connected" | "wait_before_retry";

export type WSConnectionStatusListener = (status: WSConnectionStatus, reconnectInSec: number) => void | Promise<void>;

export type WSErrorHandler = (error: Event | Error) => void | Promise<void>;

export type WebSocketMessageAction = string;

/** Base type for any WebSocket message: an object with an `action` discriminator. */
export interface WebSocketMessage {
    action: WebSocketMessageAction;
}

export type WebSocketMessageHandler<MessageType extends WebSocketMessage = WebSocketMessage> = (
    message: MessageType,
) => void | Promise<void>;

/** Narrow a message union to the member with the matching `action`. */
type ExtractMessageByAction<Messages extends WebSocketMessage, Action extends string> =
    [Extract<Messages, {action: Action}>] extends [never]
        ? Messages & {action: Action}
        : Extract<Messages, {action: Action}>;

interface WebSocketServerErrorDetail {
    type?: string;
    msg?: string;
    loc?: unknown[];
}

interface WebSocketServerErrorMessage extends WebSocketMessage {
    action: "error";
    payload?: WebSocketServerErrorDetail[];
}

class WebSocketServerError extends Error {
    payload: WebSocketServerErrorDetail[];

    constructor(message: string, payload: WebSocketServerErrorDetail[] = [], cause?: unknown) {
        super(message, {cause});
        this.name = "WebSocketServerError";
        this.payload = payload;
    }
}

function isWebSocketServerErrorMessage(message: unknown): message is WebSocketServerErrorMessage {
    return (
        typeof message === "object" &&
        message !== null &&
        "action" in message &&
        (message as {action: unknown}).action === "error"
    );
}

function formatServerError(payload?: WebSocketServerErrorDetail[]): string {
    if (!Array.isArray(payload) || payload.length === 0) {
        return "Unknown WebSocket error.";
    }

    return payload
        .map(({type, msg, loc}) => {
            const reason = msg || "Unknown WebSocket error.";
            const suffix = Array.isArray(loc) && loc.length ? ` (${loc.map(String).join(".")})` : "";
            return type ? `${reason} [${type}]${suffix}` : `${reason}${suffix}`;
        })
        .join("\n");
}

/**
 * Typed WebSocket client. `SentMessages` / `ReceivedMessages` are the unions of
 * messages this channel sends and receives.
 */
export class WebSocketClient<SentMessages extends WebSocketMessage, ReceivedMessages extends WebSocketMessage> {
    #url: string;
    #socket?: WebSocket;
    #status: WSConnectionStatus = "disconnected";
    #statusListener?: WSConnectionStatusListener;
    #errorHandler?: WSErrorHandler;
    #messageHandlers: Map<WebSocketMessageAction, WebSocketMessageHandler> = new Map();
    #messageQueue: SentMessages[] = [];
    #openedAt = 0;
    #unstableRetries = 0;

    constructor(url: string) {
        this.#url = url;
    }

    /** Register a listener for connection status changes (replaces the previous one). */
    setConnectionStatusListener(listener: WSConnectionStatusListener): void {
        this.#statusListener = listener;
    }

    /** Register a handler for generic WebSocket errors (replaces the previous one). */
    setErrorHandler(handler: WSErrorHandler): void {
        this.#errorHandler = handler;
    }

    /** Register a handler for a given received message `action` (replaces the previous one). */
    setMessageHandler<Action extends ReceivedMessages["action"]>(
        action: Action,
        handler: WebSocketMessageHandler<ExtractMessageByAction<ReceivedMessages, Action>>,
    ): void {
        this.#messageHandlers.set(action, handler as WebSocketMessageHandler);
    }

    async #setConnectionStatus(status: WSConnectionStatus, reconnectInSec = 0): Promise<void> {
        this.#status = status;
        if (this.#statusListener) {
            await this.#statusListener(status, reconnectInSec);
        }
    }

    /**
     * Connect to the server, retrying up to `MAX_ATTEMPTS` times with increasing
     * delays. Throws if the connection cannot be established.
     */
    async connect(): Promise<void> {
        if (this.#status !== "disconnected") {
            return;
        }

        let lastError: unknown = null;
        let delayMs = BASE_DELAY_MS;

        for (let attempt = 1; attempt <= MAX_ATTEMPTS; attempt++) {
            lastError = null;

            try {
                await this.#setConnectionStatus("connecting");

                await new Promise((resolve, reject) => {
                    this.#socket = new WebSocket(this.#url);

                    this.#socket.addEventListener("open", async () => {
                        this.#openedAt = Date.now();
                        await this.#setConnectionStatus("connected");
                        for (const message of this.#messageQueue) {
                            await this.#send(message);
                        }
                        this.#messageQueue = [];
                        resolve(undefined);
                    });

                    this.#socket.addEventListener("close", () => {
                        this.#socket = undefined;

                        // Never connected: the outer attempt is still awaiting.
                        if (this.#status === "connecting") {
                            reject(new Error("WebSocket connection failed."));
                        }

                        // Caller deliberately disconnected.
                        if (this.#status === "disconnected") {
                            return;
                        }

                        // Connection lost. If it dropped almost immediately several
                        // times in a row, the server is closing it (e.g. a 1011) — stop
                        // flapping and report instead of reconnecting forever.
                        const uptime = Date.now() - this.#openedAt;

                        window.setTimeout(async () => {
                            await this.#setConnectionStatus("disconnected");

                            if (uptime < STABLE_CONNECTION_MS) {
                                this.#unstableRetries++;
                                if (this.#unstableRetries > MAX_UNSTABLE_RETRIES) {
                                    if (this.#errorHandler) {
                                        await this.#errorHandler(
                                            new Error("The assistant keeps dropping the connection. Please try again later."),
                                        );
                                    }
                                    return;
                                }
                                await new Promise((r) => setTimeout(r, BASE_DELAY_MS * 2 ** this.#unstableRetries));
                            } else {
                                this.#unstableRetries = 0;
                            }

                            try {
                                await this.connect();
                            } catch (error) {
                                console.error(error);
                                if (this.#errorHandler) {
                                    await this.#errorHandler(error as Error);
                                }
                            }
                        }, 0);
                    });

                    this.#socket.addEventListener("error", async (error: Event) => {
                        console.error(error);
                        if (this.#errorHandler) {
                            await this.#errorHandler(error);
                        }
                    });

                    this.#socket.addEventListener("message", async (event: MessageEvent) => {
                        try {
                            const message = JSON.parse(event.data as string) as WebSocketMessage;
                            if (!message.action) {
                                throw new Error("Received a WebSocket message without an `action`.");
                            }

                            if (isWebSocketServerErrorMessage(message)) {
                                const error = new WebSocketServerError(
                                    formatServerError(message.payload),
                                    message.payload ?? [],
                                    message,
                                );
                                console.error(error);
                                if (this.#errorHandler) {
                                    await this.#errorHandler(error);
                                }
                                return;
                            }

                            const handler = this.#messageHandlers.get(message.action);
                            if (!handler) {
                                console.warn('No handler for WebSocket action "%s".', message.action, message);
                                return;
                            }

                            await handler(message);
                        } catch (error) {
                            console.error(error);
                            if (this.#errorHandler) {
                                await this.#errorHandler(error as Error);
                            }
                        }
                    });
                });
            } catch (error) {
                lastError = error;
            }

            if ((this.#status as WSConnectionStatus) === "connected") {
                return;
            }

            await this.#setConnectionStatus("wait_before_retry", delayMs / 1000);
            await new Promise((resolve) => setTimeout(resolve, delayMs));
            delayMs *= 2;
            console.warn(`WebSocket retry ${attempt}/${MAX_ATTEMPTS} for ${this.#url}.`);
        }

        await this.#setConnectionStatus("disconnected");
        if (lastError instanceof Error) {
            throw lastError;
        }
        throw new Error("WebSocket connection failed.");
    }

    /** Disconnect and stop reconnecting until `connect()` is called again. */
    async disconnect(): Promise<void> {
        if (!this.#socket) {
            return;
        }
        await this.#setConnectionStatus("disconnected");
        this.#socket.close();
    }

    /** Reset the unstable-connection counter and try connecting again. */
    async retry(): Promise<void> {
        this.#unstableRetries = 0;
        await this.connect();
    }

    /** Send a message, or queue it until the connection is (re)established. */
    async send(message: SentMessages): Promise<void> {
        if (this.#status === "connected" && this.#socket) {
            await this.#send(message);
        } else {
            this.#messageQueue.push(message);
        }
    }

    async #send(message: SentMessages): Promise<void> {
        if (!this.#socket) {
            return;
        }
        this.#socket.send(JSON.stringify(message));
    }
}
