"""Monatsplan-MD-Leser — liest Patricias verbindlichen Monatsplan aus der lokalen
Markdown-Datei (Single Source of Truth, Entscheidung Patricia 2026-06-09).

Quelle: outputs/monatsplaene/[YYYY-MM]-mentoring-monatsplan*.md
- Wählt bei mehreren Versionen die NEUESTE (mtime) → v2 schlägt v1 automatisch.
- Extrahiert: Monats-Header, Phasen-Logik-Tabelle, und den KW-Block für HEUTE
  (inkl. Wochen-Pillar) → konkreter thematischer Kontext für die Story.

Reine Datei-/Text-Logik, KEIN API-Key nötig → via `python monatsplan_reader.py` testbar.
"""

from __future__ import annotations

import logging
import re
from datetime import date, datetime
from pathlib import Path
from typing import Any

import config

logger = logging.getLogger(__name__)

_MONATE = {
    1: "01", 2: "02", 3: "03", 4: "04", 5: "05", 6: "06",
    7: "07", 8: "08", 9: "09", 10: "10", 11: "11", 12: "12",
}


def _monatsplaene_dir() -> Path:
    return config.WORKSPACE_ROOT / "outputs" / "monatsplaene"


def finde_monatsplan_datei(heute: date, profil: str = "mentoring") -> Path | None:
    """Findet die aktuellste Monatsplan-MD für den Monat von heute.

    Bevorzugt das Profil im Dateinamen (mentoring/doterra); fällt sonst auf
    irgendeinen Monatsplan des Monats zurück. Bei mehreren: neueste mtime.
    """
    d = _monatsplaene_dir()
    if not d.is_dir():
        return None
    yyyymm = f"{heute.year}-{_MONATE[heute.month]}"

    kandidaten = [
        p for p in d.glob(f"{yyyymm}*.md")
        if "monatsplan" in p.name.lower()
    ]
    if not kandidaten:
        return None

    # Profil-Treffer bevorzugen
    profil_treffer = [p for p in kandidaten if profil.lower() in p.name.lower()]
    pool = profil_treffer or kandidaten

    # Neueste Datei (mtime) gewinnt → v2 schlägt v1
    pool.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return pool[0]


def _aktueller_kw_block(text: str, heute: date) -> tuple[str, str]:
    """Extrahiert den KW-Abschnitt für heute aus dem Markdown.

    KW-Header sehen aus wie: '## 📅 KW24 · 8.-14.6. — REICHWEITE ...'
    Returnt (kw_block_text, wochen_pillar).
    """
    kw = heute.isocalendar().week
    lines = text.splitlines()

    # Finde Start-Index des KW-Headers
    start = None
    header_re = re.compile(r"^##\s.*KW\s?0*(\d{1,2})\b", re.IGNORECASE)
    for i, ln in enumerate(lines):
        m = header_re.match(ln)
        if m and int(m.group(1)) == kw:
            start = i
            break
    if start is None:
        return "", ""

    # Block bis zum nächsten '## ' (gleiche Ebene) oder Datei-Ende
    block = [lines[start]]
    for ln in lines[start + 1:]:
        if ln.startswith("## "):
            break
        block.append(ln)
    block_text = "\n".join(block).strip()

    # Wochen-Pillar herausziehen
    pillar = ""
    pm = re.search(r"\*\*Wochen-Pillar:\*\*\s*(.+)", block_text)
    if pm:
        pillar = pm.group(1).strip()
    return block_text, pillar


def _heutiger_tagesslot(kw_block: str, heute: date) -> str:
    """Versucht den heutigen Tages-Block (### Mo 8.6. ...) aus dem KW-Block zu ziehen."""
    if not kw_block:
        return ""
    tag = heute.day
    monat = heute.month
    lines = kw_block.splitlines()
    # Tages-Header wie '### Di 9.6.' oder '### Mo 29.6. · TAG 1 ...'
    tag_re = re.compile(rf"^###\s.*\b{tag}\.{monat}\.", re.IGNORECASE)
    start = None
    for i, ln in enumerate(lines):
        if tag_re.match(ln):
            start = i
            break
    if start is None:
        return ""
    block = [lines[start]]
    for ln in lines[start + 1:]:
        if ln.startswith("### ") or ln.startswith("## "):
            break
        block.append(ln)
    return "\n".join(block).strip()


def lade_monatsplan(heute: date | None = None, profil: str = "mentoring") -> dict[str, Any] | None:
    """Lädt den Monatsplan aus der MD-Datei und extrahiert den heute relevanten Teil.

    Returns:
      {
        "datei": "2026-06-mentoring-monatsplan-v2-bootcamp.md",
        "monat": "2026-06",
        "header": "<erste Zeilen / Pivot-Hinweis>",
        "phasen_logik": "<Phasen-Tabelle falls vorhanden>",
        "kw": 24,
        "wochen_pillar": "...",
        "kw_block": "<kompletter KW-Abschnitt für heute>",
        "tagesslot": "<heutiger Tages-Block falls vorhanden>"
      }
      oder None wenn keine Datei gefunden.
    """
    if heute is None:
        heute = date.today()

    pfad = finde_monatsplan_datei(heute, profil)
    if not pfad:
        logger.info(f"Kein Monatsplan-MD für {heute.year}-{_MONATE[heute.month]} ({profil}) gefunden")
        return None

    try:
        text = pfad.read_text(encoding="utf-8")
    except Exception as e:
        logger.error(f"Monatsplan-MD nicht lesbar: {e}")
        return None

    # Header = bis zur ersten KW-/Phasen-Sektion (max ~1200 Zeichen)
    header_split = re.split(r"\n##\s", text, maxsplit=1)
    header = header_split[0].strip()[:1200]

    # Phasen-Logik-Tabelle (Abschnitt mit 'Phasen-Logik')
    phasen_logik = ""
    pm = re.search(r"##\s.*Phasen-Logik.*?(?=\n##\s|\Z)", text, re.DOTALL | re.IGNORECASE)
    if pm:
        phasen_logik = pm.group(0).strip()[:1500]

    kw_block, pillar = _aktueller_kw_block(text, heute)
    tagesslot = _heutiger_tagesslot(kw_block, heute)

    return {
        "datei": pfad.name,
        "pfad": str(pfad),
        "monat": f"{heute.year}-{_MONATE[heute.month]}",
        "header": header,
        "phasen_logik": phasen_logik,
        "kw": heute.isocalendar().week,
        "wochen_pillar": pillar,
        "kw_block": kw_block[:2500],
        "tagesslot": tagesslot[:1200],
    }


# ========================================
# CLI-Tester (kein API-Key nötig)
# ========================================
if __name__ == "__main__":
    import sys
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    if len(sys.argv) > 1:
        heute = date.fromisoformat(sys.argv[1])
    else:
        heute = date.today()

    print(f"=== Monatsplan-Reader Test für {heute.isoformat()} ===\n")
    mp = lade_monatsplan(heute)
    if not mp:
        print("Keine Monatsplan-Datei gefunden.")
        sys.exit(0)

    print(f"Datei: {mp['datei']}")
    print(f"Monat: {mp['monat']} · KW {mp['kw']}")
    print(f"Wochen-Pillar: {mp['wochen_pillar'] or '(nicht gefunden)'}")
    print(f"\n--- KW-Block (gekürzt) ---\n{mp['kw_block'][:800]}")
    print(f"\n--- Heutiger Tagesslot ---\n{mp['tagesslot'] or '(kein Tages-Block für heute gefunden)'}")
