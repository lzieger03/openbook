/*
 * OpenBook: Interactive Online Textbooks
 * © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 */

import {spawn}     from "node:child_process";
import path        from "node:path";
import process     from "node:process";
import url         from "node:url";
import {parseArgs} from "node:util";
import fs          from "node:fs/promises";
import fsSync      from "node:fs";

const args = parseArgs({
    options: {
        u: {type: "string"},
        d: {type: "string"},
        o: {type: "string"},
        p: {type: "string"},
    }
});

const config = {
    baseUrl:    args.values.u || "http://localhost:8000",
    djangoRoot: args.values.d || "",
    outputDir:  args.values.o || "",
    python:     args.values.p || "python",
}

if (!config.outputDir) {
    console.error("Output directory not given. Argument -o missing!");
    process.exit(1);
}

const endpoints = [
    {
        url:        `${config.baseUrl}/api/schema/`,
        outputFile: "openbook.yaml",
        label:      "OpenBook REST API YAML schema",
    },
    {
        url:        `${config.baseUrl}/api/schema/?format=json`,
        outputFile: "openbook.json",
        label:      "OpenBook REST API JSON schema",
    },
    {
        url:        `${config.baseUrl}/auth-api/openapi.yaml`,
        outputFile: "auth.yaml",
        label:      "Authentication API YAML schema",
    },
    {
        url:        `${config.baseUrl}/auth-api/openapi.json`,
        outputFile: "auth.json",
        label:      "Authentication API JSON schema",
    },
];

let serverProcess = null;

try {
    await fs.mkdir(config.outputDir, {recursive: true});

    if (config.djangoRoot) {
        serverProcess = spawn(config.python, ["manage.py", "runserver", "--noreload"], {
            cwd:   config.djangoRoot,
            stdio: "inherit",
        });

        await waitForServerReady(`${config.baseUrl}/api/schema/?format=json`, serverProcess);
    }

    for (let endpoint of endpoints) await download(endpoint);
    console.log(`OpenAPI specs synchronized to ${config.outputDir}`);
} finally {
    if (serverProcess) await stopServer(serverProcess);
}

/**
 * Waits for the Django development server to be ready by polling a health endpoint.
 *
 * @param {string} healthUrl - The URL endpoint to poll for server readiness
 * @param {ChildProcess} serverProcess - The spawned server process
 * @returns {Promise<void>} Resolves when the server is ready
 * @throws {Error} If the server exits unexpectedly or times out after 30 seconds
 */
async function waitForServerReady(healthUrl, serverProcess) {
    const timeoutMs = 30_000;
    const pollIntervalMs = 500;
    const startTime = Date.now();

    while (Date.now() - startTime < timeoutMs) {
        if (serverProcess.exitCode !== null) {
            throw new Error(`Django server exited unexpectedly with code ${serverProcess.exitCode}`);
        }

        try {
            const response = await fetch(healthUrl);
            if (response.ok) return;
        } catch {
            // Ignore connection errors while waiting for server start.
        }

        await wait(pollIntervalMs);
    }

    throw new Error(`Timed out while waiting for Django server at ${healthUrl}`);
}

/**
 * Downloads an OpenAPI schema file from a URL and saves it to the output directory.
 *
 * @param {Object} options - Download options
 * @param {string} options.url - The URL to download the schema from
 * @param {string} options.outputFile - The filename to save the schema as
 * @param {string} options.label - A human-readable label for logging
 * @returns {Promise<void>} Resolves when the file has been written
 * @throws {Error} If the HTTP request fails or the file write fails
 */
async function download({url, outputFile, label}) {
    const destination = path.join(config.outputDir, outputFile);
    const response = await fetch(url);

    if (!response.ok) {
        throw new Error(`Failed to download ${label} from ${url}: HTTP ${response.status}`);
    }

    const body = await response.text();
    await fs.writeFile(destination, body, "utf8");
    console.log(`Downloaded ${label} -> ${destination}`);
}

/**
 * Gracefully stops the Django development server process.
 * Sends SIGTERM first and waits up to 5 seconds before forcing SIGKILL if needed.
 *
 * @param {ChildProcess} child - The server process to stop
 * @returns {Promise<void>} Resolves when the process has been terminated
 */
async function stopServer(child) {
    if (!child || child.killed) return;

    child.kill("SIGTERM");

    await Promise.race([
        new Promise(resolve => child.once("exit", resolve)),
        wait(5_000).then(() => {
            if (!child.killed) child.kill("SIGKILL");
        }),
    ]);
}

/**
 * Returns a promise that resolves after the specified delay.
 *
 * @param {number} ms - The delay in milliseconds
 * @returns {Promise<void>} Resolves after the specified delay
 */
function wait(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
