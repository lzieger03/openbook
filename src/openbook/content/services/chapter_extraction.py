# OpenBook: Interactive Online Textbooks
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
# Ledejna Salihi (@LedejnaSalihi)
# Lars Zieger (@lzieger03)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

"""
Split an uploaded script (a whole document) into chapters.

A teacher can upload one source file in the Content tab and have it turned into a
textbook automatically — this module finds the natural chapter boundaries so each
chapter becomes its own textbook page. It works on the three formats the textbook
editor can represent (Markdown, HTML, plain text) and always degrades gracefully:
if no headings are found the whole document is returned as a single chapter, so an
upload never silently loses content.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from io import BytesIO
import html
import re

# Cap how many chapters a single upload may produce, so a pathological document
# (e.g. an ordered list mistaken for headings) cannot create thousands of pages.
MAX_CHAPTERS = 300

# Chapter titles map onto TextbookPage.name (CharField(max_length=255)).
MAX_TITLE_LENGTH = 200


class ChapterExtractionError(ValueError):
    """Raised when an uploaded document cannot be turned into chapters."""


@dataclass(frozen=True)
class Chapter:
    """One extracted chapter: its heading text and the source it owns."""

    title: str
    source: str


def extract_chapters(source: str, text_format: str) -> list[Chapter]:
    """Split ``source`` into chapters according to its ``text_format``.

    ``text_format`` is one of the ``NameDescriptionMixin.TextFormatChoices`` values
    (``"MD"``, ``"HTML"``, ``"TEXT"``). Returns at least one chapter for any non-empty
    input; an empty/whitespace-only document yields an empty list.
    """
    text = (source or "").strip()
    if not text:
        return []

    if text_format == "HTML":
        chapters = _extract_html_chapters(text)
    elif text_format == "TEXT":
        chapters = _extract_text_chapters(text)
    else:  # Markdown is the default for everything else.
        chapters = _extract_markdown_chapters(text)

    # Fall back to a single chapter so an upload without recognizable headings still
    # produces a usable page instead of an error.
    if not chapters:
        chapters = [Chapter(title="", source=text)]

    return _finalize(chapters)


def extract_pdf_chapters(data: bytes) -> list[Chapter]:
    """Split an uploaded PDF into chapters.

    Prefers the PDF's own outline (bookmarks / table of contents) since that maps
    directly onto chapters; otherwise extracts the text and detects headings in it.
    The resulting pages are Markdown — extracted PDF text keeps its line breaks, which
    the textbook renderer preserves. Raises :class:`ChapterExtractionError` for a
    missing dependency, an unreadable file, or a PDF with no extractable text.
    """
    try:
        from pypdf import PdfReader
    except ImportError as error:  # pragma: no cover - depends on the deployment env
        raise ChapterExtractionError(
            "PDF support is not available on the server (the 'pypdf' package is missing)."
        ) from error

    try:
        reader = PdfReader(BytesIO(data))
        page_texts = [_normalize_pdf_text(page.extract_text() or "") for page in reader.pages]
    except Exception as error:
        raise ChapterExtractionError("The PDF could not be read. It may be corrupted or protected.") from error

    # Prefer the outline, but only when it actually yields text — a scanned PDF can
    # carry bookmarks while every page extracts to nothing.
    outline_chapters = [
        chapter for chapter in _chapters_from_pdf_outline(reader, page_texts) if chapter.source.strip()
    ]
    if outline_chapters:
        return _finalize(outline_chapters)

    full_text = "\n\n".join(text for text in page_texts if text).strip()
    if not full_text:
        raise ChapterExtractionError(
            "No text could be extracted from the PDF (a scanned/image-only PDF is not supported)."
        )

    chapters = _extract_text_chapters(full_text) or [Chapter(title="", source=full_text)]
    return _finalize(chapters)


# --- Markdown -----------------------------------------------------------------

# ATX headings: one to six leading '#', a space, the title, optional trailing '#'.
_MD_HEADING = re.compile(r"^(#{1,6})[ \t]+(.+?)[ \t]*#*$", re.MULTILINE)


def _extract_markdown_chapters(text: str) -> list[Chapter]:
    headings = [
        (match.start(), len(match.group(1)), match.group(2).strip())
        for match in _MD_HEADING.finditer(text)
    ]
    if not headings:
        return []

    level = _choose_split_level([level for _, level, _ in headings])
    splits = [(pos, title) for pos, heading_level, title in headings if heading_level == level]
    if not splits:
        return []

    return _slice_chapters(
        text=text,
        splits=splits,
        preamble_title=_preamble_title(headings, level, splits[0][0]),
    )


# --- HTML ---------------------------------------------------------------------

_HTML_HEADING = re.compile(r"<h([1-6])\b[^>]*>(.*?)</h\1>", re.IGNORECASE | re.DOTALL)
_HTML_TAG = re.compile(r"<[^>]+>")


def _extract_html_chapters(text: str) -> list[Chapter]:
    headings = [
        (match.start(), int(match.group(1)), _strip_html(match.group(2)))
        for match in _HTML_HEADING.finditer(text)
    ]
    if not headings:
        return []

    level = _choose_split_level([level for _, level, _ in headings])
    splits = [(pos, title) for pos, heading_level, title in headings if heading_level == level]
    if not splits:
        return []

    return _slice_chapters(
        text=text,
        splits=splits,
        preamble_title=_preamble_title(headings, level, splits[0][0]),
    )


def _strip_html(value: str) -> str:
    """Reduce inline HTML to its visible text (used for heading titles)."""
    return html.unescape(_HTML_TAG.sub("", value)).strip()


# --- Plain text ---------------------------------------------------------------

# Lines that look like a heading: a "Chapter/Kapitel/…"-style label (case-insensitive),
# or a short numbered line whose title starts with a capital ("1. Introduction",
# "2.3 Advanced Topics"). Requiring the capital — and the length guard below — keeps
# prose and lowercase ordered-list items ("1. apples") from looking like headings.
_TEXT_HEADING = re.compile(
    r"^[ \t]*(?:"
    r"(?i:chapter|kapitel|teil|part|abschnitt|section|lektion|lesson|unit)\b.*"
    r"|\d+(?:\.\d+)*[.)]?[ \t]+[A-ZÄÖÜ].*"
    r")$",
)
_MAX_TEXT_HEADING_LENGTH = 80


def _extract_text_chapters(text: str) -> list[Chapter]:
    lines = text.split("\n")
    indexes = [
        index
        for index, line in enumerate(lines)
        if line.strip()
        and len(line.strip()) <= _MAX_TEXT_HEADING_LENGTH
        and _TEXT_HEADING.match(line)
    ]

    # A single (or no) heading is not enough structure to split on.
    if len(indexes) < 2:
        return []

    chapters: list[Chapter] = []

    preamble = "\n".join(lines[: indexes[0]]).strip()
    if preamble:
        chapters.append(Chapter(title="Introduction", source=preamble))

    for position, start in enumerate(indexes):
        end = indexes[position + 1] if position + 1 < len(indexes) else len(lines)
        block = "\n".join(lines[start:end]).strip()
        chapters.append(Chapter(title=lines[start].strip(), source=block))

    return chapters


# --- PDF ----------------------------------------------------------------------

# Strip trailing whitespace before newlines and collapse runs of blank lines so the
# extracted text renders as tidy Markdown (line breaks are kept on purpose).
_PDF_TRAILING_WS = re.compile(r"[ \t]+\n")
_PDF_BLANK_RUN = re.compile(r"\n{3,}")


def _normalize_pdf_text(text: str) -> str:
    cleaned = text.replace("\x0c", "\n")
    cleaned = _PDF_TRAILING_WS.sub("\n", cleaned)
    cleaned = _PDF_BLANK_RUN.sub("\n\n", cleaned)
    return cleaned.strip()


def _chapters_from_pdf_outline(reader, page_texts: list[str]) -> list[Chapter]:
    """Build chapters from a PDF's bookmark outline, slicing text by page ranges."""
    try:
        outline = reader.outline
    except Exception:
        return []

    # Prefer the coarse top-level bookmarks; if there are too few, descend into the
    # full (nested) outline so a single "Contents" root with chapter children works.
    entries = _flatten_pdf_outline(reader, outline, top_level_only=True)
    if len(entries) < 2:
        entries = _flatten_pdf_outline(reader, outline, top_level_only=False)
    if len(entries) < 2:
        return []

    page_count = len(page_texts)
    chapters: list[Chapter] = []
    for position, (title, start_page) in enumerate(entries):
        start = max(0, min(start_page, page_count))
        end = entries[position + 1][1] if position + 1 < len(entries) else page_count
        # Always include at least the bookmark's own page, even when two bookmarks
        # share one page, so no content is dropped.
        end = max(end, start + 1)
        body = "\n\n".join(page_texts[start:end]).strip()
        chapters.append(Chapter(title=title, source=body))

    return chapters


def _flatten_pdf_outline(reader, outline, top_level_only: bool) -> list[tuple[str, int]]:
    """Flatten a (possibly nested) PDF outline to ``(title, page_index)`` in order."""
    entries: list[tuple[str, int]] = []

    for item in outline:
        if isinstance(item, list):
            if not top_level_only:
                entries.extend(_flatten_pdf_outline(reader, item, top_level_only=False))
            continue

        try:
            page_number = reader.get_destination_page_number(item)
        except Exception:
            page_number = None

        title = str(getattr(item, "title", "") or "").strip()
        if page_number is not None:
            entries.append((title, int(page_number)))

    return entries


# --- Shared helpers -----------------------------------------------------------

def _finalize(chapters: list[Chapter]) -> list[Chapter]:
    """Normalize titles, drop empties, and cap the number of chapters."""
    return [
        Chapter(title=_clean_title(chapter.title), source=chapter.source.strip())
        for chapter in chapters[:MAX_CHAPTERS]
        if chapter.source.strip()
    ]


def _choose_split_level(levels: list[int]) -> int:
    """Pick the heading level that best marks chapter boundaries.

    Prefer the highest-ranking level (smallest number) that occurs more than once —
    that is usually the chapter level, with a single top-level title sitting above it.
    If nothing repeats, fall back to the highest-ranking level present.
    """
    counts = Counter(levels)
    repeated = sorted(level for level, count in counts.items() if count >= 2)
    if repeated:
        return repeated[0]
    return min(counts)


def _preamble_title(
    headings: list[tuple[int, int, str]],
    level: int,
    first_split_pos: int,
) -> str:
    """Title for content before the first chapter heading.

    Reuse the nearest higher-level heading (e.g. the document's ``# Title``) when
    present, otherwise label it generically.
    """
    above = [title for pos, heading_level, title in headings if heading_level < level and pos < first_split_pos]
    return above[-1] if above and above[-1] else "Introduction"


def _slice_chapters(
    text: str,
    splits: list[tuple[int, str]],
    preamble_title: str,
) -> list[Chapter]:
    """Cut ``text`` into chapters at each split position, keeping any preamble."""
    chapters: list[Chapter] = []

    preamble = text[: splits[0][0]].strip()
    if preamble:
        chapters.append(Chapter(title=preamble_title, source=preamble))

    for position, (start, title) in enumerate(splits):
        end = splits[position + 1][0] if position + 1 < len(splits) else len(text)
        chapters.append(Chapter(title=title, source=text[start:end].strip()))

    return chapters


def _clean_title(title: str) -> str:
    """Normalize whitespace and clamp a heading to the page-name length limit."""
    cleaned = " ".join((title or "").split())
    if len(cleaned) > MAX_TITLE_LENGTH:
        cleaned = cleaned[:MAX_TITLE_LENGTH].rstrip()
    return cleaned
