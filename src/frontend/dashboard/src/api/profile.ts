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
 * Profile write operations. Editable profile fields live on the user REST
 * endpoint; e-mail addresses are managed through the separate allauth headless
 * API (changing an address triggers a verification mail).
 */

import {apiGet, apiSend} from "./client.js";

export interface ProfileFields {
    firstName: string;
    lastName: string;
    description: string;
}

export interface EmailAddress {
    email: string;
    verified: boolean;
    primary: boolean;
}

interface AllauthListResponse {
    data?: EmailAddress[];
}

/**
 * Update the editable profile fields of a user. When a picture file is supplied
 * the request is sent as multipart so the file can be uploaded in the same call.
 */
export async function saveProfile(
    username: string,
    fields: ProfileFields,
    picture: File | null,
): Promise<void> {
    const path = `/api/auth/users/${encodeURIComponent(username)}/`;

    if (picture) {
        const form = new FormData();
        form.set("first_name", fields.firstName);
        form.set("last_name", fields.lastName);
        form.set("description", fields.description);
        form.set("picture", picture);
        await apiSend<unknown>("PATCH", path, form, {formData: true});
        return;
    }

    await apiSend<unknown>("PATCH", path, {
        first_name: fields.firstName,
        last_name: fields.lastName,
        description: fields.description,
    });
}

/** List the current account's e-mail addresses (verified / primary flags). */
export async function fetchEmailAddresses(): Promise<EmailAddress[]> {
    const response = await apiGet<AllauthListResponse>("/auth-api/browser/v1/account/email");
    return response.data ?? [];
}

/**
 * Request an e-mail change. allauth adds the address and sends a verification
 * link; it becomes the primary address only after the user confirms it.
 */
export async function requestEmailChange(email: string): Promise<void> {
    await apiSend<unknown>("POST", "/auth-api/browser/v1/account/email", {email});
}
