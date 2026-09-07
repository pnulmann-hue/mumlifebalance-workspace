"""PDF-Ausgabe des Vorabend-Briefings — „Mum Life Daily · Vorabend".

Tageszeitungs-Layout mit reportlab (pure Python, laeuft auf GitHub Actions).
Rendert dieselbe Struktur, die auch die Telegram-Kurzfassung nutzt — Text und
PDF koennen also nie inhaltlich auseinanderlaufen.

Emojis werden bewusst entfernt: die PDF-Standardfonts (Helvetica) koennen sie
nicht rendern und wuerden schwarze Kaesten zeichnen. Statt Emoji-Titeln
verwenden die Ressorts die Marker aus BLOCK_META.
"""

from __future__ import annotations

import logging
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    ListFlowable,
    ListItem,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)

from briefing_builder import _strip_emoji

logger = logging.getLogger(__name__)

# Brand-Farben (Mum Life Balance) — kein Gelb, das gehoert nicht zur Brand.
PETROL = HexColor("#2b6b70")
DUNKELBLAU = HexColor("#1f3a4d")
ORANGE = HexColor("#d98a3d")
CREME = HexColor("#f1ecdd")
GRAU = HexColor("#6b6b6b")
TEXT = HexColor("#2b2b2b")

# Ressorts, die am Abend noch Handlung ausloesen -> Orange statt Petrol.
DRINGEND = {"pinned", "schule", "content_feed", "content_story"}

_OUT_DIR = Path(__file__).resolve().parent


def _styles() -> dict[str, ParagraphStyle]:
    return {
        "kicker": ParagraphStyle(
            "kicker", fontName="Helvetica-Bold", fontSize=9.5,
            textColor=ORANGE, leading=12, spaceAfter=2),
        "title": ParagraphStyle(
            "title", fontName="Helvetica-Bold", fontSize=26,
            textColor=PETROL, leading=30, spaceAfter=2),
        "datum": ParagraphStyle(
            "datum", fontName="Helvetica", fontSize=12,
            textColor=DUNKELBLAU, leading=16, spaceAfter=1),
        "thema": ParagraphStyle(
            "thema", fontName="Helvetica-Oblique", fontSize=10,
            textColor=GRAU, leading=13, spaceAfter=8),
        "section": ParagraphStyle(
            "section", fontName="Helvetica-Bold", fontSize=11.5,
            textColor=white, backColor=PETROL, leading=18,
            borderPadding=(4, 6, 4, 6), spaceBefore=13, spaceAfter=7,
            alignment=TA_LEFT, keepWithNext=True),
        "section_dringend": ParagraphStyle(
            "section_dringend", fontName="Helvetica-Bold", fontSize=11.5,
            textColor=white, backColor=ORANGE, leading=18,
            borderPadding=(4, 6, 4, 6), spaceBefore=13, spaceAfter=7,
            alignment=TA_LEFT, keepWithNext=True),
        "item": ParagraphStyle(
            "item", fontName="Helvetica", fontSize=10,
            textColor=TEXT, leading=14, spaceAfter=2),
        "fuss": ParagraphStyle(
            "fuss", fontName="Helvetica-Oblique", fontSize=9.5,
            textColor=GRAU, leading=13, spaceBefore=14),
        "quelle": ParagraphStyle(
            "quelle", fontName="Helvetica", fontSize=7.5,
            textColor=GRAU, leading=10, alignment=TA_RIGHT, spaceBefore=10),
    }


def _item_paragraph(text: str, stil: ParagraphStyle) -> Paragraph:
    """Eine Briefing-Zeile — Emoji raus, Sonderzeichen escaped."""
    sauber = _strip_emoji(text)
    return Paragraph(escape(sauber), stil)


def baue_pdf(struktur: dict, out_path: str | Path | None = None) -> str:
    """Baut das Vorabend-PDF und gibt den Dateipfad zurueck."""
    s = _styles()
    if out_path is None:
        out_path = _OUT_DIR / f"vorabend-{struktur['morgen'].isoformat()}.pdf"
    out_path = Path(out_path)

    doc = SimpleDocTemplate(
        str(out_path), pagesize=A4,
        topMargin=18 * mm, bottomMargin=16 * mm,
        leftMargin=18 * mm, rightMargin=18 * mm,
        title=f"Vorabend {struktur['datum_lang']}",
        author="Mum Life Balance",
    )

    story: list = []
    story.append(Paragraph("VORABEND-AUSGABE", s["kicker"]))
    story.append(Paragraph("Mum Life Daily", s["title"]))
    story.append(HRFlowable(width="100%", thickness=1.4, color=PETROL,
                            spaceBefore=4, spaceAfter=6))
    story.append(Paragraph(f"Morgen ist {escape(struktur['datum_lang'])}", s["datum"]))

    if struktur["tagesthema"]:
        thema = _strip_emoji(struktur["tagesthema"])
        story.append(Paragraph(
            f"Business-Tag: {escape(thema)} — Arbeitsfenster am Vormittag.",
            s["thema"]))
    else:
        story.append(Paragraph("Kein Business-Tag — Wochenende.", s["thema"]))

    if not struktur["hat_inhalt"]:
        story.append(Paragraph(
            "Morgen ist wenig los. Goenn dir einen ruhigen Tag.", s["item"]))
    else:
        for block in struktur["bloecke"]:
            stil = s["section_dringend"] if block["key"] in DRINGEND else s["section"]
            liste = ListFlowable(
                [ListItem(_item_paragraph(x, s["item"]), leftIndent=10)
                 for x in block["items"]],
                bulletType="bullet", bulletFontSize=6, bulletColor=PETROL,
                leftIndent=12, spaceAfter=2,
            )
            # Ressort-Balken nie allein am Seitenende stehen lassen: Titel und
            # die Liste wandern zusammen auf die naechste Seite.
            story.append(KeepTogether([
                Paragraph(escape(block["marker"]), stil),
                liste,
            ]))

        if any(b["key"] == "slot" for b in struktur["bloecke"]):
            story.append(Paragraph(
                "Dein Slot ist Schutz, kein Druck — nimm ihn dir, wenn er passt.",
                s["fuss"]))

    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=0.6, color=CREME))
    story.append(Paragraph(
        "Quellen: Notion — Haushalts-Liste, Aufgaben, Content-Management",
        s["quelle"]))

    doc.build(story)
    logger.info(f"PDF gebaut: {out_path}")
    return str(out_path)
