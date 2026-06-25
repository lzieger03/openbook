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
import html
import re

# Cap how many chapters a single upload may produce, so a pathological document
# (e.g. an ordered list mistaken for headings) cannot create thousands of pages.
MAX_CHAPTERS = 300

# Chapter titles map onto TextbookPage.name (CharField(max_length=255)).
MAX_TITLE_LENGTH = 200


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

    return [
        Chapter(title=_clean_title(chapter.title), source=chapter.source.strip())
        for chapter in chapters[:MAX_CHAPTERS]
        if chapter.source.strip()
    ]


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


# --- Shared helpers -----------------------------------------------------------

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
