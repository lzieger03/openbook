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
 * Course content editing: the ordered list of course materials (each linking a
 * textbook to a course) and the page ranges selected within each material.
 * Textbooks and their pages are read-only lookups used to build those links.
 */

import {apiGet, apiSend} from "./client.js";
import {slugify} from "./courses.js";
import type {TextFormat} from "./courses.js";

export interface SourceContent {
    type: "source";
    format: TextFormat;
    source: string;
    filename?: string;
}

export interface TextbookDto {
    id: string;
    name: string;
    slug: string;
    description?: string;
    text_format?: TextFormat;
    group?: string;
}

export interface TextbookPageDto {
    id: string;
    textbook: string;
    parent: string | null;
    name: string;
    description: string;
    text_format: TextFormat;
    position: number;
    content: SourceContent | Record<string, unknown>;
}

export interface CourseMaterialDto {
    id: string;
    course: string;
    textbook: string | TextbookDto;
    position: number;
    page_ranges: string[];
}

export interface PageRangeDto {
    id: string;
    material: string;
    start_page: string | TextbookPageDto;
    end_page: string | TextbookPageDto;
    position: number;
}

export interface TextbookUploadResult {
    textbook: string;
    material: string;
    document: string;
    index_status: string;
}

interface Paginated<T> {
    results: T[];
}

function toList<T>(data: T[] | Paginated<T>): T[] {
    return Array.isArray(data) ? data : data.results;
}

/* ---- Textbook lookups -------------------------------------------------- */

export async function fetchTextbooks(): Promise<TextbookDto[]> {
    const data = await apiGet<TextbookDto[] | Paginated<TextbookDto>>("/api/content/textbooks/", {
        _page_size: "200",
        _sort: "name",
    });
    return toList(data);
}

export async function createTextbook(fields: {
    name: string;
    slug?: string;
    description?: string;
    text_format: TextFormat;
    group: string;
}): Promise<TextbookDto> {
    const slug = fields.slug?.trim() || slugify(fields.name);
    const {slug: _slug, ...payloadFields} = fields;

    return apiSend<TextbookDto>("POST", "/api/content/textbooks/", {
        description: "",
        ...payloadFields,
        slug,
    });
}

export async function uploadTextbookFile(
    courseId: string,
    file: File,
    fields: {
        name?: string;
        slug?: string;
        description?: string;
    } = {},
): Promise<TextbookUploadResult> {
    const form = new FormData();
    form.append("file", file);

    if (fields.name?.trim()) {
        form.append("name", fields.name.trim());
    }
    if (fields.slug?.trim()) {
        form.append("slug", fields.slug.trim());
    }
    if (fields.description?.trim()) {
        form.append("description", fields.description.trim());
    }

    return apiSend<TextbookUploadResult>(
        "POST",
        `/api/content/courses/${encodeURIComponent(courseId)}/upload_textbook/`,
        form,
        {formData: true},
    );
}

export async function fetchTextbookPages(textbookId: string): Promise<TextbookPageDto[]> {
    const data = await apiGet<TextbookPageDto[] | Paginated<TextbookPageDto>>(
        "/api/content/textbook_pages/",
        {textbook: textbookId, _sort: "position", _page_size: "500"},
    );
    return toList(data);
}

export async function createTextbookPage(fields: {
    textbook: string;
    parent?: string | null;
    position: number;
    name: string;
    description?: string;
    text_format: TextFormat;
    content: SourceContent;
}): Promise<TextbookPageDto> {
    return apiSend<TextbookPageDto>("POST", "/api/content/textbook_pages/", {
        parent: null,
        description: "",
        ...fields,
    });
}

export async function updateTextbookPage(
    id: string,
    fields: {
        name?: string;
        description?: string;
        text_format?: TextFormat;
        content?: SourceContent;
    },
): Promise<TextbookPageDto> {
    return apiSend<TextbookPageDto>("PATCH", `/api/content/textbook_pages/${encodeURIComponent(id)}/`, fields);
}

/* ---- Course materials -------------------------------------------------- */

export async function fetchMaterials(courseId: string): Promise<CourseMaterialDto[]> {
    const data = await apiGet<CourseMaterialDto[] | Paginated<CourseMaterialDto>>(
        "/api/content/course_materials/",
        {course: courseId, _expand: "textbook", _sort: "position", _page_size: "200"},
    );
    return toList(data);
}

export async function addMaterial(
    courseId: string,
    textbookId: string,
    position: number,
): Promise<CourseMaterialDto> {
    return apiSend<CourseMaterialDto>("POST", "/api/content/course_materials/", {
        course: courseId,
        textbook: textbookId,
        position,
    });
}

export async function updateMaterialPosition(id: string, position: number): Promise<CourseMaterialDto> {
    return apiSend<CourseMaterialDto>("PATCH", `/api/content/course_materials/${encodeURIComponent(id)}/`, {
        position,
    });
}

/** Move a material one step up or down in the syllabus (atomic swap on the server). */
export async function moveMaterial(id: string, direction: "up" | "down"): Promise<CourseMaterialDto> {
    return apiSend<CourseMaterialDto>("POST", `/api/content/course_materials/${encodeURIComponent(id)}/move/`, {
        direction,
    });
}

export async function deleteMaterial(id: string): Promise<void> {
    await apiSend<void>("DELETE", `/api/content/course_materials/${encodeURIComponent(id)}/`);
}

/* ---- Page ranges within a material ------------------------------------- */

export async function fetchPageRanges(materialId: string): Promise<PageRangeDto[]> {
    const data = await apiGet<PageRangeDto[] | Paginated<PageRangeDto>>(
        "/api/content/course_material_page_ranges/",
        {material: materialId, _expand: "start_page,end_page", _sort: "position", _page_size: "200"},
    );
    return toList(data);
}

export async function addPageRange(
    materialId: string,
    startPageId: string,
    endPageId: string,
    position: number,
): Promise<PageRangeDto> {
    return apiSend<PageRangeDto>("POST", "/api/content/course_material_page_ranges/", {
        material: materialId,
        start_page: startPageId,
        end_page: endPageId,
        position,
    });
}

export async function deletePageRange(id: string): Promise<void> {
    await apiSend<void>("DELETE", `/api/content/course_material_page_ranges/${encodeURIComponent(id)}/`);
}
