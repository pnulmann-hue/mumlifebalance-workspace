"""
PDF-Erzeugung der Tagesausgabe mit reportlab (pure Python, läuft auf Railway).
Klickbare Links, Brand-Farben, Video-Markierung. Umlaute via Standard-Fonts.
"""

import logging
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    HRFlowable,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)

from config import (
    PDF_FILENAME,
    PDF_INTRO,
    PDF_SUBTITLE,
    PDF_TITLE,
)

logger = logging.getLogger(__name__)

# Brand-Farben (Mum Life Balance)
TEAL = HexColor("#2b6b70")
DARK = HexColor("#1f3a4d")
ACCENT = HexColor("#d98a3d")
GREY = HexColor("#6b6b6b")

_OUT_DIR = Path(__file__).resolve().parent

# Ressort -> kurzer Text-Marker (Emojis rendern in PDF-Standardfonts nicht)
SECTION_MARKERS = {
    "Instagram & Social Media": "SOCIAL",
    "Online-Business & Marketing": "BUSINESS",
    "Network Marketing": "NETWORK",
    "Zeitmanagement & Mama-CEO-Struktur": "STRUKTUR",
    "KI & Claude Code": "KI",
}


def _styles():
    return {
        "title": ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=26,
                                 textColor=TEAL, leading=30, spaceAfter=2),
        "subtitle": ParagraphStyle("subtitle", fontName="Helvetica", fontSize=11.5,
                                    textColor=DARK, leading=15, spaceAfter=1),
        "date": ParagraphStyle("date", fontName="Helvetica", fontSize=10,
                                textColor=GREY, leading=13, spaceAfter=6),
        "intro": ParagraphStyle("intro", fontName="Helvetica-Oblique", fontSize=9.5,
                                 textColor=GREY, leading=13, spaceAfter=10),
        "section": ParagraphStyle("section", fontName="Helvetica-Bold", fontSize=13,
                                   textColor=white, backColor=TEAL, leading=20,
                                   borderPadding=(5, 6, 5, 6), spaceBefore=14,
                                   spaceAfter=8, alignment=TA_LEFT),
        "item_title": ParagraphStyle("item_title", fontName="Helvetica-Bold", fontSize=12,
                                      textColor=DARK, leading=15, spaceAfter=3),
        "body": ParagraphStyle("body", fontName="Helvetica", fontSize=10,
                               textColor=HexColor("#2b2b2b"), leading=14.5, spaceAfter=3),
        "meta": ParagraphStyle("meta", fontName="Helvetica", fontSize=8.5,
                               textColor=GREY, leading=12, spaceAfter=12),
    }


def build_pdf(articles_by_category: dict[str, list[dict]], date_str: str, date_iso: str) -> str:
    """Baut die Tagesausgabe als PDF und gibt den Dateipfad zurück."""
    s = _styles()
    out_path = _OUT_DIR / PDF_FILENAME.format(date=date_iso)

    doc = SimpleDocTemplate(
        str(out_path), pagesize=A4,
        topMargin=18 * mm, bottomMargin=18 * mm,
        leftMargin=18 * mm, rightMargin=18 * mm,
        title=f"{PDF_TITLE} — {date_str}", author="Mum Life Daily",
    )

    flow = []
    flow.append(Paragraph(PDF_TITLE, s["title"]))
    flow.append(Paragraph(escape(PDF_SUBTITLE), s["subtitle"]))
    flow.append(Paragraph(escape(date_str), s["date"]))
    flow.append(HRFlowable(width="100%", thickness=1.2, color=ACCENT, spaceAfter=8))
    flow.append(Paragraph(escape(PDF_INTRO), s["intro"]))

    for category, items in articles_by_category.items():
        if not items:
            continue
        marker = SECTION_MARKERS.get(category, "")
        head = f"{marker}  —  {category}" if marker else category
        flow.append(Paragraph(escape(head), s["section"]))

        for art in items:
            is_video = art.get("is_video", False)
            tag = '<font color="#d98a3d"><b>VIDEO &middot; </b></font>' if is_video else ""
            flow.append(Paragraph(tag + escape(art["title"]), s["item_title"]))

            if art.get("summary"):
                flow.append(Paragraph(escape(art["summary"]), s["body"]))

            src = escape(art.get("source", ""))
            link = escape(art.get("link", ""))
            label = "Video ansehen" if is_video else "Weiterlesen"
            meta = f'Quelle: {src} &nbsp;|&nbsp; ' \
                   f'<a href="{link}"><font color="#d98a3d">{label} &rarr;</font></a>'
            flow.append(Paragraph(meta, s["meta"]))

    doc.build(flow)
    logger.info("PDF erstellt: %s", out_path)
    return str(out_path)
