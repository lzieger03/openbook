<!--
OpenBook: Interactive Online Textbooks - Server
© 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.
-->

<!--
@component
Manual test page for gamification reward triggering and live user-impact checks.
-->
<script lang="ts">
    import {onMount} from "svelte";

    type RewardRecord = {
        id: string;
        reward_type: string;
        value: number;
        description: string;
    };

    type RewardEventRecord = {
        id: string;
        account: string;
        reward: string;
        event_type: string;
        points_delta: number;
        created_at: string;
        context: Record<string, unknown>;
    };

    let isLoading = $state(true);
    let isRefreshing = $state(false);
    let isTriggering = $state(false);

    let errorMessage = $state("");
    let infoMessage = $state("");

    let isAuthenticated = $state(false);
    let isStaff = $state(false);
    let currentUsername = $state("");

    let targetUsername = $state("");
    let userSearch = $state("");
    let userResults = $state([] as string[]);

    let rewards = $state([] as RewardRecord[]);
    let selectedRewardId = $state("");
    let customEventType = $state("");
    let contextJson = $state(JSON.stringify({source: "manual-gamification-test-page"}, null, 2));

    let currentPointTotal = $state<number | null>(null);
    let recentEvents = $state([] as RewardEventRecord[]);

    let beforePoints = $state<number | null>(null);
    let afterPoints = $state<number | null>(null);
    let expectedDelta = $state<number | null>(null);
    let actualDelta = $state<number | null>(null);
    let testPassed = $state<boolean | null>(null);
    let lastTriggerResponse = $state("");

    function getCsrfToken(): string {
        return document.cookie.match(/csrftoken=([\w]+)/)?.[1] || "";
    }

    function toErrorMessage(error: unknown): string {
        if (error instanceof Error) {
            return error.message;
        }

        return String(error);
    }

    async function requestJson(path: string, init: RequestInit = {}): Promise<any> {
        const headers = new Headers(init.headers);

        if (!headers.has("Accept")) {
            headers.set("Accept", "application/json");
        }

        if (init.body && !headers.has("Content-Type")) {
            headers.set("Content-Type", "application/json");
        }

        const method = (init.method || "GET").toUpperCase();

        if (!["GET", "HEAD", "OPTIONS"].includes(method)) {
            const csrfToken = getCsrfToken();

            if (csrfToken) {
                headers.set("X-CSRFToken", csrfToken);
            }
        }

        const response = await fetch(path, {
            ...init,
            headers,
            credentials: "same-origin",
        });

        const responseText = await response.text();
        let payload: any = null;

        if (responseText) {
            try {
                payload = JSON.parse(responseText);
            } catch {
                payload = responseText;
            }
        }

        if (!response.ok) {
            const detail = typeof payload === "object" && payload
                ? (payload.detail || JSON.stringify(payload, null, 2))
                : payload;

            throw new Error(`HTTP ${response.status}: ${detail || "Unknown error"}`);
        }

        return payload;
    }

    function selectedReward(): RewardRecord | undefined {
        return rewards.find((reward) => reward.id === selectedRewardId);
    }

    function rewardTypeById(rewardId: string): string {
        return rewards.find((reward) => reward.id === rewardId)?.reward_type || rewardId;
    }

    async function loadCurrentUser(): Promise<void> {
        const data = await requestJson("/api/auth/current_user/");

        isAuthenticated = Boolean(data?.is_authenticated);

        if (!isAuthenticated) {
            throw new Error("Du bist nicht eingeloggt. Bitte zuerst anmelden.");
        }

        currentUsername = String(data?.username || "");
        isStaff = Boolean(data?.is_staff);
        targetUsername = currentUsername;
    }

    async function loadRewards(): Promise<void> {
        const data = await requestJson("/api/gamification/rewards/?_page_size=200&_sort=reward_type");
        rewards = Array.isArray(data?.results) ? data.results : [];

        if (!selectedRewardId && rewards.length > 0) {
            selectedRewardId = rewards[0].id;
        }
    }

    async function loadPointTotalForTarget(): Promise<number | null> {
        if (!targetUsername.trim()) {
            return null;
        }

        if (!isStaff || targetUsername === currentUsername) {
            const meData = await requestJson("/api/gamification/account_points/me/");
            return Number(meData?.point_total ?? 0);
        }

        const params = new URLSearchParams({
            account: targetUsername,
            _page_size: "1",
        });

        const listData = await requestJson(`/api/gamification/account_points/?${params.toString()}`);
        const row = listData?.results?.[0];

        if (!row) {
            return null;
        }

        return Number(row.point_total ?? 0);
    }

    async function loadEventsForTarget(): Promise<void> {
        if (!targetUsername.trim()) {
            recentEvents = [];
            return;
        }

        const params = new URLSearchParams({
            account: targetUsername,
            _page_size: "10",
            _sort: "-created_at",
        });

        const listData = await requestJson(`/api/gamification/reward_events/?${params.toString()}`);
        recentEvents = Array.isArray(listData?.results) ? listData.results : [];
    }

    async function refreshTargetData(): Promise<void> {
        isRefreshing = true;
        errorMessage = "";

        try {
            currentPointTotal = await loadPointTotalForTarget();
            await loadEventsForTarget();
        } catch (error) {
            errorMessage = toErrorMessage(error);
        } finally {
            isRefreshing = false;
        }
    }

    async function searchUsers(): Promise<void> {
        if (!isStaff) {
            return;
        }

        errorMessage = "";

        try {
            const params = new URLSearchParams({
                _page_size: "20",
                _sort: "username",
            });

            if (userSearch.trim()) {
                params.set("username__icontains", userSearch.trim());
            }

            const data = await requestJson(`/api/auth/users/?${params.toString()}`);
            userResults = (data?.results || []).map((user: any) => String(user.username));
        } catch (error) {
            errorMessage = toErrorMessage(error);
        }
    }

    async function selectTargetUser(username: string): Promise<void> {
        targetUsername = username;
        await refreshTargetData();
    }

    async function triggerRewardEvent(): Promise<void> {
        infoMessage = "";
        errorMessage = "";
        testPassed = null;

        const reward = selectedReward();

        if (!reward) {
            errorMessage = "Bitte zuerst einen Reward auswählen.";
            return;
        }

        if (!targetUsername.trim()) {
            errorMessage = "Bitte einen Ziel-User angeben.";
            return;
        }

        let contextPayload: unknown = {};

        try {
            contextPayload = contextJson.trim() ? JSON.parse(contextJson) : {};
        } catch {
            errorMessage = "Context JSON ist ungültig.";
            return;
        }

        isTriggering = true;

        try {
            beforePoints = await loadPointTotalForTarget();

            const body: Record<string, unknown> = {
                reward: selectedRewardId,
                context: contextPayload,
            };

            if (customEventType.trim()) {
                body.event_type = customEventType.trim();
            }

            if (isStaff && targetUsername !== currentUsername) {
                body.account = targetUsername;
            }

            const response = await requestJson("/api/gamification/reward_events/trigger/", {
                method: "POST",
                body: JSON.stringify(body),
            });

            lastTriggerResponse = JSON.stringify(response, null, 2);

            await refreshTargetData();

            afterPoints = currentPointTotal;
            expectedDelta = Number(reward.value || 0);

            if (beforePoints != null && afterPoints != null) {
                actualDelta = afterPoints - beforePoints;
                testPassed = actualDelta === expectedDelta;
            } else {
                actualDelta = null;
                testPassed = null;
            }

            infoMessage = "Reward-Event wurde ausgelöst und die Daten wurden aktualisiert.";
        } catch (error) {
            errorMessage = toErrorMessage(error);
        } finally {
            isTriggering = false;
        }
    }

    onMount(async () => {
        isLoading = true;
        errorMessage = "";

        try {
            await loadCurrentUser();
            await loadRewards();

            if (isStaff) {
                await searchUsers();
            }

            await refreshTargetData();
        } catch (error) {
            errorMessage = toErrorMessage(error);
        } finally {
            isLoading = false;
        }
    });
</script>

<div class="page">
    <h1>Gamification Manual Test</h1>
    <p class="intro">
        Nutze diese Seite, um manuell ein Punktevergabe-Event auszulösen und die Auswirkung
        auf einen User direkt zu prüfen (Point Total + Reward Events).
    </p>

    {#if errorMessage}
        <div class="alert error">{errorMessage}</div>
    {/if}

    {#if infoMessage}
        <div class="alert success">{infoMessage}</div>
    {/if}

    {#if isLoading}
        <div class="panel">Lade Testseite ...</div>
    {:else if !isAuthenticated}
        <div class="panel">Nicht eingeloggt. Bitte zuerst anmelden.</div>
    {:else}
        <div class="grid">
            <section class="panel">
                <h2>1) Testkontext</h2>
                <p><strong>Aktueller User:</strong> {currentUsername}</p>
                <p><strong>Staff:</strong> {isStaff ? "Ja" : "Nein"}</p>

                <label for="target-user">Ziel-User</label>
                <div class="row">
                    <input
                        id="target-user"
                        type="text"
                        bind:value={targetUsername}
                        readonly={!isStaff}
                        placeholder="username"
                    />
                    <button type="button" onclick={refreshTargetData} disabled={isRefreshing}>
                        {isRefreshing ? "Lade ..." : "Daten laden"}
                    </button>
                </div>

                {#if isStaff}
                    <label for="user-search">User suchen (Staff)</label>
                    <div class="row">
                        <input id="user-search" type="text" bind:value={userSearch} placeholder="z. B. lar" />
                        <button type="button" onclick={searchUsers}>Suchen</button>
                    </div>

                    {#if userResults.length > 0}
                        <div class="chips">
                            {#each userResults as username}
                                <button type="button" class="chip" onclick={() => selectTargetUser(username)}>
                                    {username}
                                </button>
                            {/each}
                        </div>
                    {/if}
                {/if}
            </section>

            <section class="panel">
                <h2>2) Event auslösen</h2>

                <label for="reward">Reward</label>
                <select id="reward" bind:value={selectedRewardId}>
                    {#each rewards as reward}
                        <option value={reward.id}>
                            {reward.reward_type} (+{reward.value} Punkte)
                        </option>
                    {/each}
                </select>

                <label for="event-type">Event Type (optional)</label>
                <input id="event-type" type="text" bind:value={customEventType} placeholder="z. B. manual_test_bonus" />

                <label for="context-json">Context JSON</label>
                <textarea id="context-json" rows="8" bind:value={contextJson}></textarea>

                <button type="button" class="primary" onclick={triggerRewardEvent} disabled={isTriggering || !selectedRewardId}>
                    {isTriggering ? "Trigger läuft ..." : "Reward Event triggern"}
                </button>
            </section>

            <section class="panel">
                <h2>3) Direkte Auswirkung</h2>
                <p><strong>Aktueller Punktestand:</strong> {currentPointTotal ?? "—"}</p>

                {#if testPassed !== null}
                    <div class="result" class:pass={testPassed} class:fail={!testPassed}>
                        <p><strong>Automatischer Check:</strong> {testPassed ? "PASS" : "FAIL"}</p>
                        <p>Vorher: {beforePoints ?? "—"}</p>
                        <p>Nachher: {afterPoints ?? "—"}</p>
                        <p>Erwartetes Delta: {expectedDelta ?? "—"}</p>
                        <p>Tatsächliches Delta: {actualDelta ?? "—"}</p>
                    </div>
                {/if}

                {#if lastTriggerResponse}
                    <h3>Trigger Response</h3>
                    <pre>{lastTriggerResponse}</pre>
                {/if}
            </section>

            <section class="panel full-width">
                <h2>4) Letzte Reward Events ({targetUsername})</h2>

                {#if recentEvents.length === 0}
                    <p>Keine Events gefunden.</p>
                {:else}
                    <div class="table-wrap">
                        <table>
                            <thead>
                                <tr>
                                    <th>Zeitpunkt</th>
                                    <th>Account</th>
                                    <th>Event Type</th>
                                    <th>Reward</th>
                                    <th>Delta</th>
                                </tr>
                            </thead>
                            <tbody>
                                {#each recentEvents as event}
                                    <tr>
                                        <td>{new Date(event.created_at).toLocaleString()}</td>
                                        <td>{event.account}</td>
                                        <td>{event.event_type}</td>
                                        <td>{rewardTypeById(event.reward)}</td>
                                        <td>{event.points_delta}</td>
                                    </tr>
                                {/each}
                            </tbody>
                        </table>
                    </div>
                {/if}
            </section>
        </div>
    {/if}
</div>

<style>
    .page {
        margin: 0 auto;
        padding: 1.5rem;
        width: min(1200px, 96%);
        box-sizing: border-box;
        color: rgb(34, 34, 34);
    }

    h1 {
        margin: 0 0 0.5rem 0;
    }

    .intro {
        margin: 0 0 1.25rem 0;
        color: rgb(80, 80, 80);
    }

    .grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
        gap: 1rem;
    }

    .panel {
        border: 1px solid rgb(220, 220, 220);
        border-radius: 0.5rem;
        padding: 1rem;
        background: white;
        color: rgb(34, 34, 34);
    }

    .full-width {
        grid-column: 1 / -1;
    }

    .row {
        display: flex;
        gap: 0.5rem;
        margin-bottom: 0.75rem;
    }

    label {
        font-weight: 600;
        display: block;
        margin: 0.5rem 0 0.35rem 0;
    }

    input,
    select,
    textarea,
    button {
        font: inherit;
    }

    input,
    select,
    textarea {
        width: 100%;
        border: 1px solid rgb(200, 200, 200);
        border-radius: 0.35rem;
        padding: 0.5rem 0.6rem;
        box-sizing: border-box;
        color: rgb(25, 25, 25);
        background: rgb(255, 255, 255);
    }

    textarea {
        font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
    }

    button {
        border: 1px solid rgb(190, 190, 190);
        border-radius: 0.35rem;
        background: rgb(245, 245, 245);
        color: rgb(34, 34, 34);
        padding: 0.5rem 0.75rem;
        cursor: pointer;
    }

    button:disabled {
        opacity: 0.6;
        cursor: not-allowed;
    }

    button.primary {
        margin-top: 0.75rem;
        background: rgb(14, 111, 180);
        border-color: rgb(14, 111, 180);
        color: white;
    }

    .chips {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
    }

    .chip {
        border-radius: 999px;
        padding: 0.25rem 0.65rem;
        background: rgb(239, 247, 255);
        border-color: rgb(194, 221, 248);
    }

    .alert {
        margin-bottom: 0.85rem;
        padding: 0.65rem 0.8rem;
        border-radius: 0.35rem;
        border: 1px solid;
    }

    .alert.error {
        background: rgb(255, 242, 242);
        border-color: rgb(245, 180, 180);
        color: rgb(140, 30, 30);
    }

    .alert.success {
        background: rgb(236, 251, 239);
        border-color: rgb(164, 222, 175);
        color: rgb(28, 104, 43);
    }

    .result {
        margin-top: 0.75rem;
        padding: 0.65rem 0.8rem;
        border-radius: 0.35rem;
        border: 1px solid;
    }

    .result.pass {
        background: rgb(236, 251, 239);
        border-color: rgb(164, 222, 175);
    }

    .result.fail {
        background: rgb(255, 242, 242);
        border-color: rgb(245, 180, 180);
    }

    .result p {
        margin: 0.2rem 0;
    }

    pre {
        margin-top: 0.5rem;
        max-height: 240px;
        overflow: auto;
        background: rgb(248, 248, 248);
        border: 1px solid rgb(226, 226, 226);
        border-radius: 0.35rem;
        padding: 0.75rem;
        font-size: 0.9em;
    }

    .table-wrap {
        overflow: auto;
    }

    table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 0.25rem;
    }

    th,
    td {
        border-bottom: 1px solid rgb(230, 230, 230);
        text-align: left;
        padding: 0.45rem;
        white-space: nowrap;
        color: rgb(34, 34, 34);
    }

    th {
        background: rgb(248, 248, 248);
    }
</style>
