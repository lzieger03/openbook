"""Generate PNG flyers for ELISA information material."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from textwrap import wrap

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = ROOT / "docs" / "info_materials" / "img"
LOGO_PATH = OUTPUT_DIR / "Elisa Logo.png"

W, H = 1240, 1754
MARGIN = 82
CARD_RADIUS = 22

FONT_DIR = Path("C:/Windows/Fonts")
FONT_REGULAR = FONT_DIR / "segoeui.ttf"
FONT_BOLD = FONT_DIR / "segoeuib.ttf"
FONT_LIGHT = FONT_DIR / "segoeuil.ttf"


@dataclass(frozen=True)
class Palette:
    bg: str
    ink: str
    muted: str
    panel: str
    primary: str
    secondary: str
    accent: str
    pale: str


@dataclass(frozen=True)
class Flyer:
    filename: str
    audience: str
    title: str
    subtitle: str
    badge: str
    palette: Palette
    sections: list[tuple[str, list[str]]]
    workflow: list[str]
    footer: str
    footer_detail: str


def font(size: int, bold: bool = False, light: bool = False) -> ImageFont.FreeTypeFont:
    path = FONT_BOLD if bold else FONT_LIGHT if light else FONT_REGULAR
    return ImageFont.truetype(str(path), size)


def text_size(draw: ImageDraw.ImageDraw, text: str, selected_font: ImageFont.FreeTypeFont) -> tuple[int, int]:
    box = draw.textbbox((0, 0), text, font=selected_font)
    return box[2] - box[0], box[3] - box[1]


def rounded(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], radius: int, fill: str) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill)


def shadowed_rounded(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    radius: int,
    fill: str,
    shadow: str = "#d9e2ec",
) -> None:
    x1, y1, x2, y2 = box
    draw.rounded_rectangle((x1 + 8, y1 + 10, x2 + 8, y2 + 10), radius=radius, fill=shadow)
    draw.rounded_rectangle(box, radius=radius, fill=fill)


def draw_wrapped(
    draw: ImageDraw.ImageDraw,
    text: str,
    xy: tuple[int, int],
    selected_font: ImageFont.FreeTypeFont,
    fill: str,
    max_width: int,
    line_spacing: int = 8,
) -> int:
    x, y = xy
    words = text.split()
    lines: list[str] = []
    current = ""

    for word in words:
        candidate = f"{current} {word}".strip()
        if text_size(draw, candidate, selected_font)[0] <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word

    if current:
        lines.append(current)

    line_height = text_size(draw, "Ag", selected_font)[1] + line_spacing
    for line in lines:
        draw.text((x, y), line, font=selected_font, fill=fill)
        y += line_height

    return y


def draw_bullet_list(
    draw: ImageDraw.ImageDraw,
    items: list[str],
    xy: tuple[int, int],
    selected_font: ImageFont.FreeTypeFont,
    fill: str,
    bullet_fill: str,
    max_width: int,
) -> int:
    x, y = xy
    for item in items:
        draw.ellipse((x, y + 9, x + 12, y + 21), fill=bullet_fill)
        y = draw_wrapped(draw, item, (x + 28, y), selected_font, fill, max_width - 28, 7)
        y += 12
    return y


def draw_logo(image: Image.Image, box: tuple[int, int, int, int]) -> None:
    logo = Image.open(LOGO_PATH).convert("RGBA")
    x1, y1, x2, y2 = box
    max_w = x2 - x1
    max_h = y2 - y1
    logo.thumbnail((max_w, max_h), Image.Resampling.LANCZOS)
    lx = x1 + (max_w - logo.width) // 2
    ly = y1 + (max_h - logo.height) // 2
    image.paste(logo, (lx, ly), logo)


def draw_header(image: Image.Image, draw: ImageDraw.ImageDraw, flyer: Flyer) -> None:
    p = flyer.palette
    draw.rectangle((0, 0, W, 360), fill=p.primary)
    draw.polygon([(820, 0), (W, 0), (W, 360), (980, 360)], fill=p.secondary)
    draw.polygon([(930, 0), (W, 0), (W, 118), (970, 118)], fill=p.accent)
    draw.polygon([(0, 318), (W, 318), (W, 360), (0, 360)], fill="#ffffff")

    badge_font = font(28, bold=True)
    title_font = font(64, bold=True)
    subtitle_font = font(34)

    badge_w = text_size(draw, flyer.badge, badge_font)[0] + 42
    rounded(draw, (MARGIN, 74, MARGIN + badge_w, 126), 24, "#ffffff")
    draw.text((MARGIN + 21, 84), flyer.badge, font=badge_font, fill=p.primary)

    draw.text((MARGIN, 158), flyer.title, font=title_font, fill="#ffffff")
    draw.text((MARGIN, 250), flyer.subtitle, font=subtitle_font, fill="#eef6ff")

    logo_card = (952, 56, W - 74, 278)
    shadowed_rounded(draw, logo_card, 28, "#ffffff", "#1f3f5f")
    draw_logo(image, (972, 70, W - 94, 264))


def draw_section(
    draw: ImageDraw.ImageDraw,
    title: str,
    items: list[str],
    box: tuple[int, int, int, int],
    p: Palette,
) -> None:
    x1, y1, x2, y2 = box
    shadowed_rounded(draw, box, CARD_RADIUS, p.panel)
    draw.rectangle((x1, y1, x1 + 12, y2), fill=p.accent)
    draw.text((x1 + 36, y1 + 30), title, font=font(34, bold=True), fill=p.ink)
    draw_bullet_list(
        draw,
        items,
        (x1 + 36, y1 + 88),
        font(25),
        p.ink,
        p.accent,
        x2 - x1 - 72,
    )


def draw_workflow(draw: ImageDraw.ImageDraw, flyer: Flyer, y: int) -> int:
    p = flyer.palette
    draw.text((MARGIN, y), "Typischer Ablauf", font=font(34, bold=True), fill=p.ink)
    y += 60

    gap = 18
    tile_w = (W - 2 * MARGIN - gap * (len(flyer.workflow) - 1)) // len(flyer.workflow)
    tile_h = 130

    for idx, label in enumerate(flyer.workflow, start=1):
        x = MARGIN + (idx - 1) * (tile_w + gap)
        rounded(draw, (x, y, x + tile_w, y + tile_h), 18, p.pale)
        draw.ellipse((x + 22, y + 21, x + 62, y + 61), fill=p.primary)
        draw.text((x + 36, y + 27), str(idx), font=font(22, bold=True), fill="#ffffff", anchor="mm")

        lines = wrap(label, width=13)
        line_y = y + 72
        for line in lines[:2]:
            draw.text((x + tile_w // 2, line_y), line, font=font(21, bold=True), fill=p.ink, anchor="ma")
            line_y += 28

        if idx < len(flyer.workflow):
            ax = x + tile_w + 4
            ay = y + tile_h // 2
            draw.line((ax, ay, ax + gap - 8, ay), fill=p.muted, width=4)
            draw.polygon((ax + gap - 8, ay, ax + gap - 20, ay - 8, ax + gap - 20, ay + 8), fill=p.muted)

    return y + tile_h + 58


def draw_footer(draw: ImageDraw.ImageDraw, flyer: Flyer) -> None:
    p = flyer.palette
    y = H - 204
    shadowed_rounded(draw, (MARGIN, y, W - MARGIN, H - 72), 22, p.primary)
    draw.text((MARGIN + 34, y + 28), flyer.footer, font=font(27, bold=True), fill="#ffffff")
    draw_wrapped(
        draw,
        flyer.footer_detail,
        (MARGIN + 34, y + 78),
        font(22),
        "#eef6ff",
        W - 2 * MARGIN - 68,
        6,
    )


def render(flyer: Flyer) -> None:
    p = flyer.palette
    image = Image.new("RGB", (W, H), p.bg)
    draw = ImageDraw.Draw(image)

    draw_header(image, draw, flyer)

    y = 410
    section_h = 340
    col_gap = 34
    col_w = (W - 2 * MARGIN - col_gap) // 2
    boxes = [
        (MARGIN, y, MARGIN + col_w, y + section_h),
        (MARGIN + col_w + col_gap, y, W - MARGIN, y + section_h),
        (MARGIN, y + section_h + 34, MARGIN + col_w, y + 2 * section_h + 34),
        (MARGIN + col_w + col_gap, y + section_h + 34, W - MARGIN, y + 2 * section_h + 34),
    ]

    for box, (title, items) in zip(boxes, flyer.sections):
        draw_section(draw, title, items, box, p)

    workflow_y = y + 2 * section_h + 86
    draw_workflow(draw, flyer, workflow_y)
    draw_footer(draw, flyer)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    image.save(OUTPUT_DIR / flyer.filename, optimize=True)


def main() -> None:
    student = Flyer(
        filename="elisa-flyer-students.png",
        audience="Studierende",
        title="ELISA-AI f\u00fcr Studierende",
        subtitle="Dein KI-Lernbegleiter in OpenBook",
        badge="Info-Flyer f\u00fcr Lernende",
        palette=Palette(
            bg="#f7fafc",
            ink="#102033",
            muted="#64748b",
            panel="#ffffff",
            primary="#2563eb",
            secondary="#0f766e",
            accent="#f59e0b",
            pale="#e8f3ff",
        ),
        sections=[
            (
                "Was du nutzen kannst",
                [
                    "Student Dashboard mit Kursen, Lern\u00fcbersicht, Skills und Fortschritt.",
                    "Kurs-Chat f\u00fcr Fragen zu konkreten Kursinhalten.",
                    "Skriptansicht, Quiz, Exams und Lernspiele wie Memory oder Flashcards.",
                ],
            ),
            (
                "So lernst du damit",
                [
                    "Kurs \u00f6ffnen, Seite lesen und unklare Stellen gezielt nachfragen.",
                    "Quiz oder Exam starten, um dein Verst\u00e4ndnis zu pr\u00fcfen.",
                    "Fortschritt, Punkte, Level und Streaks als Orientierung nutzen.",
                ],
            ),
            (
                "Gute Fragen stellen",
                [
                    "Nenne Kurs, Thema und die konkrete Stelle, die unklar ist.",
                    "Bitte um Beispiele, Vergleiche oder eine kurze Wiederholung.",
                    "Stelle Folgefragen, wenn eine Antwort zu allgemein bleibt.",
                ],
            ),
            (
                "Wichtig zu wissen",
                [
                    "ELISA hilft beim Verstehen, ersetzt aber nicht eigenes Denken.",
                    "KI-Antworten und Quizfragen k\u00f6nnen falsch oder unvollst\u00e4ndig sein.",
                    "Pr\u00fcfe wichtige Aussagen mit Kursmaterial und Lehrendenhinweisen.",
                ],
            ),
        ],
        workflow=["Anmelden", "Kurs w\u00e4hlen", "Inhalt lesen", "ELISA fragen", "\u00dcben", "Fortschritt pr\u00fcfen"],
        footer="Ein Lernraum f\u00fcr Inhalte, Fragen und \u00dcbung",
        footer_detail=(
            "ELISA verbindet Kursmaterial, Chat, Quiz und Fortschritt, damit Lernen "
            "direkt am passenden Thema stattfindet."
        ),
    )

    teacher = Flyer(
        filename="elisa-flyer-teachers.png",
        audience="Lehrende",
        title="ELISA-AI f\u00fcr Lehrende",
        subtitle="Kurse vorbereiten, KI-Lernen begleiten",
        badge="Info-Flyer f\u00fcr Lehrende",
        palette=Palette(
            bg="#f8faf7",
            ink="#13221d",
            muted="#64748b",
            panel="#ffffff",
            primary="#0f766e",
            secondary="#1d4ed8",
            accent="#ea580c",
            pale="#e7f6f3",
        ),
        sections=[
            (
                "Was Sie vorbereiten",
                [
                    "Kurse im Teacher-Frontend anlegen oder bestehende Kurse \u00f6ffnen.",
                    "Eigene Lernmaterialien hochladen/importieren und Textbook-Seiten pflegen.",
                    "Skills vergeben und Studierende in Kurse einschreiben.",
                ],
            ),
            (
                "Didaktischer Einsatz",
                [
                    "Selbststudium mit Kursinhalt, Chat, Quiz und Exam strukturieren.",
                    "Studierenden klare Regeln f\u00fcr KI-Nutzung und Quellenpr\u00fcfung geben.",
                    "ELISA als Lernhilfe einsetzen, nicht als Bewertungsautomat.",
                ],
            ),
            (
                "Grundlage f\u00fcr KI",
                [
                    "Der Assistant arbeitet besser, wenn Kursmaterial vorhanden ist.",
                    "Quiz, Exam und Spiele h\u00e4ngen von lesbaren Kursinhalten ab.",
                    "Materialien m\u00fcssen fachlich und didaktisch sinnvoll vorbereitet sein.",
                ],
            ),
            (
                "Grenzen im PoC",
                [
                    "Reporting f\u00fcr Lehrende ist noch kein abgeschlossenes Produkt.",
                    "KI-generierte Antworten und Aufgaben m\u00fcssen gepr\u00fcft werden.",
                    "Lernstandsdaten nicht allein f\u00fcr Leistungsbewertung verwenden.",
                ],
            ),
        ],
        workflow=["Kurs anlegen", "Material pflegen", "Skills setzen", "Studierende einschreiben", "KI-Nutzung erkl\u00e4ren", "Lernen begleiten"],
        footer="Eigene Materialien werden zur Lernbasis",
        footer_detail=(
            "Hochgeladene Kursinhalte k\u00f6nnen Chat, Quiz, Exam und Lernspiele "
            "fachlich n\u00e4her an Ihre Veranstaltung bringen."
        ),
    )

    render(student)
    render(teacher)


if __name__ == "__main__":
    main()
