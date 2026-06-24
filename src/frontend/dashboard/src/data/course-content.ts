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
 * Build the readable course content for the dashboard from the data a teacher
 * authored: the ordered course materials, the page ranges selected within each
 * material and the textbook pages that carry the content. Each page's source is
 * rendered to HTML here so the UI only has to display it.
 */

import MarkdownIt from "markdown-it";

import {fetchMaterials, fetchPageRanges, fetchTextbookDocuments, fetchTextbookPages} from "../api/content.js";
import type {AssistantDocumentDto, CourseMaterialDto, PageRangeDto, SourceContent, TextbookPageDto, TextFormat} from "../api/content.js";

export interface ContentPageView {
    id: string;
    title: string;
    format: TextFormat;
    // For MD/TEXT this is rendered, ready-to-inject HTML. For HTML it is the raw
    // authored markup, which the UI renders inside a sandboxed iframe.
    html: string;
}

export interface ContentMaterialView {
    id: string;
    title: string;
    documents: ContentDocumentView[];
    pages: ContentPageView[];
}

export interface ContentDocumentView {
    id: string;
    title: string;
    fileName: string;
    downloadUrl: string;
}

const markdownRenderer = new MarkdownIt({
    breaks: true,
    html: false,
    linkify: true,
    typographer: true,
});

function escapeHtml(value: string): string {
    return value
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;");
}

function isSourceContent(content: TextbookPageDto["content"]): content is SourceContent {
    return (
        typeof content === "object" &&
        content !== null &&
        "type" in content &&
        (content as {type?: unknown}).type === "source" &&
        "source" in content
    );
}

function readPageSource(page: TextbookPageDto): string {
    if (isSourceContent(page.content)) {
        return page.content.source;
    }
    return "";
}

/** Render a page's source to the HTML the dashboard displays. */
function renderPage(page: TextbookPageDto): ContentPageView {
    const format = page.text_format ?? "MD";
    const source = readPageSource(page);

    let html: string;
    if (format === "HTML") {
        html = source; // Rendered in a sandboxed iframe by the UI.
    } else if (format === "TEXT") {
        html = `<pre>${escapeHtml(source)}</pre>`;
    } else {
        html = markdownRenderer.render(source);
    }

    return {id: page.id, title: page.name, format, html};
}

/**
 * Flatten a textbook's page tree into reading order: roots first (by position),
 * each immediately followed by its descendants. Page ranges are resolved against
 * this order.
 */
function readingOrder(pages: TextbookPageDto[]): TextbookPageDto[] {
    const byParent = new Map<string | null, TextbookPageDto[]>();

    for (const page of pages) {
        const key = page.parent ?? null;
        const siblings = byParent.get(key) ?? [];
        siblings.push(page);
        byParent.set(key, siblings);
    }

    for (const siblings of byParent.values()) {
        siblings.sort((a, b) => a.position - b.position);
    }

    const ordered: TextbookPageDto[] = [];

    const visit = (parentId: string | null): void => {
        for (const page of byParent.get(parentId) ?? []) {
            ordered.push(page);
            visit(page.id);
        }
    };

    visit(null);

    // Any pages whose parent is missing from the set are appended so nothing is lost.
    if (ordered.length < pages.length) {
        const seen = new Set(ordered.map((page) => page.id));
        for (const page of pages) {
            if (!seen.has(page.id)) {
                ordered.push(page);
            }
        }
    }

    return ordered;
}

/** Extract the id from an API reference that may be a bare id or an expanded object. */
function refId(ref: string | {id: string}): string {
    return typeof ref === "string" ? ref : ref.id;
}

/** Resolve the pages selected by a material's ranges, in the order they appear. */
function pagesForMaterial(ordered: TextbookPageDto[], ranges: PageRangeDto[]): TextbookPageDto[] {
    // No ranges means the whole textbook is used.
    if (ranges.length === 0) {
        return ordered;
    }

    const indexById = new Map(ordered.map((page, index) => [page.id, index]));
    const selected: TextbookPageDto[] = [];
    const seen = new Set<string>();

    for (const range of [...ranges].sort((a, b) => a.position - b.position)) {
        const startIndex = indexById.get(refId(range.start_page));
        const endIndex = indexById.get(refId(range.end_page));

        if (startIndex === undefined || endIndex === undefined) {
            continue;
        }

        const from = Math.min(startIndex, endIndex);
        const to = Math.max(startIndex, endIndex);

        for (let i = from; i <= to; i++) {
            const page = ordered[i];
            if (page && !seen.has(page.id)) {
                seen.add(page.id);
                selected.push(page);
            }
        }
    }

    return selected;
}

function textbookTitle(material: CourseMaterialDto): string {
    if (typeof material.textbook === "string") {
        return "Material";
    }
    return material.textbook.name;
}

function renderDocument(document: AssistantDocumentDto): ContentDocumentView | null {
    if (!document.download_url) {
        return null;
    }

    return {
        id: document.id,
        title: document.title || document.file_name || "Download",
        fileName: document.file_name.split(/[\\/]/).pop() ?? document.file_name,
        downloadUrl: document.download_url,
    };
}

/** Load and render the full readable content of a course, grouped by material. */
export async function loadCourseContent(courseId: string): Promise<ContentMaterialView[]> {
    const materials = await fetchMaterials(courseId);
    materials.sort((a, b) => a.position - b.position);

    const result = await Promise.all(
        materials.map(async (material) => {
            const textbookId = refId(material.textbook);
            const [ranges, pages, documents] = await Promise.all([
                fetchPageRanges(material.id),
                fetchTextbookPages(textbookId),
                fetchTextbookDocuments(courseId, textbookId),
            ]);

            const ordered = readingOrder(pages);
            const selected = pagesForMaterial(ordered, ranges);

            return {
                id: material.id,
                title: textbookTitle(material),
                documents: documents
                    .map(renderDocument)
                    .filter((document): document is ContentDocumentView => document !== null),
                pages: selected.map(renderPage),
            };
        }),
    );

    // Drop materials that resolved to no pages or downloads so the UI only shows real content.
    return result.filter((material) => material.pages.length > 0 || material.documents.length > 0);
}
