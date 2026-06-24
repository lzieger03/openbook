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
 * Read-only access to the course content authored in the teacher area: the ordered
 * course materials (each linking a textbook), the page ranges selected within each
 * material and the textbook pages that carry the actual content.
 */

import {apiGet} from "./client.js";

export type TextFormat = "TEXT" | "HTML" | "MD";

export interface SourceContent {
    type: "source";
    format: TextFormat;
    source: string;
    filename?: string;
}

export interface TextbookSkillDto {
    id: string;
    name: string;
    icon_path?: string;
}

export interface TextbookDto {
    id: string;
    name: string;
    slug: string;
    // Union of the skills trained by the textbook's pages (read-only, always present).
    skills?: TextbookSkillDto[];
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

export interface PageRangeDto {
    id: string;
    material: string;
    start_page: string | TextbookPageDto;
    end_page: string | TextbookPageDto;
    position: number;
}

export interface CourseMaterialDto {
    id: string;
    course: string;
    textbook: string | TextbookDto;
    position: number;
    page_ranges: string[];
}

export interface AssistantDocumentDto {
    id: string;
    course: string | null;
    textbook: string | null;
    title: string;
    file_name: string;
    mime_type: string;
    download_url: string;
    index_status: string;
}

interface Paginated<T> {
    results: T[];
}

function toList<T>(data: T[] | Paginated<T>): T[] {
    return Array.isArray(data) ? data : data.results;
}

/** Ordered course materials for a course, with the textbook reference expanded. */
export async function fetchMaterials(courseId: string): Promise<CourseMaterialDto[]> {
    const data = await apiGet<CourseMaterialDto[] | Paginated<CourseMaterialDto>>(
        "/api/content/course_materials/",
        {course: courseId, _expand: "textbook", _sort: "position", _page_size: "200"},
    );
    return toList(data);
}

/** Page ranges selected within a course material, ordered by position. */
export async function fetchPageRanges(materialId: string): Promise<PageRangeDto[]> {
    const data = await apiGet<PageRangeDto[] | Paginated<PageRangeDto>>(
        "/api/content/course_material_page_ranges/",
        {material: materialId, _sort: "position", _page_size: "200"},
    );
    return toList(data);
}

/** All pages of a textbook, ordered by their position within their parent. */
export async function fetchTextbookPages(textbookId: string): Promise<TextbookPageDto[]> {
    const data = await apiGet<TextbookPageDto[] | Paginated<TextbookPageDto>>(
        "/api/content/textbook_pages/",
        {textbook: textbookId, _sort: "position", _page_size: "500"},
    );
    return toList(data);
}

/** Downloadable source documents generated from one textbook in one course. */
export async function fetchTextbookDocuments(
    courseId: string,
    textbookId: string,
): Promise<AssistantDocumentDto[]> {
    const data = await apiGet<AssistantDocumentDto[] | Paginated<AssistantDocumentDto>>(
        "/api/assistant/documents/",
        {course: courseId, textbook: textbookId, _sort: "title", _page_size: "20"},
    );
    return toList(data);
}
