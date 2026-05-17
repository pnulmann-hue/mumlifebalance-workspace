"""State-Management für Story-Render-Bot.

Speichert in-memory + persistent:
- Aktive Story-Session (wer wartet auf wen)
- Wochenlog (DISG-Käufertypen-Tracking)
- Wochen-Vorwahl-Cache (von /freitag-hooks)
- Patricia-Antwort-Pending

Persistent gespeichert in: outputs/stories/_state/
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

import config

STATE_DIR = config.OUTPUTS_STORIES_DIR / "_state"
STATE_DIR.mkdir(parents=True, exist_ok=True)


# ========================================
# Aktive Session
# ========================================
# Wenn der Bot Patricia eine Frage gestellt hat und auf Antwort wartet,
# speichern wir das hier — Patricia kann auch 30 Min später antworten.

class Session:
    """Eine offene Story-Session — wartet auf Patricia-Antwort."""

    def __init__(self, profil: str, kontext: dict):
        self.profil = profil  # "mentoring" / "doterra" / "beide"
        self.kontext = kontext  # alles was der Skill schon weiss (Säule, Produkt, …)
        self.created_at = datetime.now().isoformat()
        self.patricia_input: str | None = None  # Text aus Sprachnotiz oder Direkt
        self.patricia_foto: str | None = None  # Pfad zu hochgeladenem Foto
        self.status = "warten_auf_input"  # warten_auf_input / generiere / fertig / skipped


_active_session: Session | None = None
_session_file = STATE_DIR / "_active_session.json"


def get_active_session() -> Session | None:
    """Liest aktive Session (in-memory oder von Disk)."""
    global _active_session
    if _active_session:
        return _active_session
    if _session_file.exists():
        try:
            data = json.loads(_session_file.read_text(encoding="utf-8"))
            s = Session(data["profil"], data.get("kontext", {}))
            s.created_at = data.get("created_at")
            s.patricia_input = data.get("patricia_input")
            s.patricia_foto = data.get("patricia_foto")
            s.status = data.get("status", "warten_auf_input")

            # Sessions älter als 6h verfallen
            if s.created_at:
                age = datetime.now() - datetime.fromisoformat(s.created_at)
                if age > timedelta(hours=6):
                    clear_active_session()
                    return None

            _active_session = s
            return s
        except Exception:
            return None
    return None


def set_active_session(profil: str, kontext: dict) -> Session:
    """Startet eine neue Session."""
    global _active_session
    _active_session = Session(profil, kontext)
    _persist_session()
    return _active_session


def update_session(input_text: str | None = None, foto_path: str | None = None, status: str | None = None):
    s = get_active_session()
    if not s:
        return
    if input_text is not None:
        s.patricia_input = input_text
    if foto_path is not None:
        s.patricia_foto = foto_path
    if status is not None:
        s.status = status
    _persist_session()


def clear_active_session():
    global _active_session
    _active_session = None
    if _session_file.exists():
        _session_file.unlink()


def _persist_session():
    s = _active_session
    if not s:
        return
    data = {
        "profil": s.profil,
        "kontext": s.kontext,
        "created_at": s.created_at,
        "patricia_input": s.patricia_input,
        "patricia_foto": s.patricia_foto,
        "status": s.status,
    }
    _session_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


# ========================================
# Wochenlog (DISG-Käufertypen-Tracking)
# ========================================
# Speichert pro Tag welcher DISG-Käufertyp + Julia-Template angesprochen wurde.
# Skill nutzt das für Rotation: alle 4 DISG-Achsen pro Woche, kein Käufertyp 3 Tage in Folge.

_log_file = config.OUTPUTS_STORIES_DIR / "wochen-log.json"


def get_wochenlog() -> dict[str, Any]:
    if _log_file.exists():
        try:
            return json.loads(_log_file.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def add_to_wochenlog(datum: str, eintrag: dict):
    """Fügt Tageseintrag zum Wochenlog hinzu."""
    log = get_wochenlog()
    log[datum] = eintrag
    _log_file.parent.mkdir(parents=True, exist_ok=True)
    _log_file.write_text(json.dumps(log, indent=2, ensure_ascii=False), encoding="utf-8")


def disg_letzte_3_tage() -> list[str]:
    """Gibt DISG-Achsen der letzten 3 Tage zurück (für Rotation-Vermeidung)."""
    log = get_wochenlog()
    today = datetime.now().date()
    out = []
    for delta in [1, 2, 3]:
        d = (today - timedelta(days=delta)).isoformat()
        if d in log:
            disg = log[d].get("disg")
            if disg:
                out.append(disg)
    return out


def disg_diese_woche() -> set[str]:
    """Welche DISG-Achsen sind diese Woche schon abgedeckt."""
    log = get_wochenlog()
    today = datetime.now().date()
    monday = today - timedelta(days=today.weekday())
    out = set()
    for delta in range(7):
        d = (monday + timedelta(days=delta)).isoformat()
        if d in log:
            disg = log[d].get("disg")
            if disg:
                out.add(disg)
    return out


def empfehle_disg_heute() -> str:
    """Welcher DISG-Käufertyp soll heute angesprochen werden?

    Logik:
    - Wenn diese Woche < 4 verschiedene DISG-Achsen → bevorzugt fehlende
    - Sonst: rotation aus Standard-Wochenrotation
    """
    standard_rotation = {
        0: "Grün",      # Mo: Stetig
        1: "Rot",       # Di: Dominant
        2: "Gelb",      # Mi: Initiativ
        3: "Blau",      # Do: Gewissenhaft
        4: "Gelb",      # Fr
        5: "Grün",      # Sa
        6: "Rot",       # So
    }
    today = datetime.now().date()
    diese_woche = disg_diese_woche()
    alle = {"Rot", "Gelb", "Grün", "Blau"}
    fehlend = alle - diese_woche

    # Wenn es Achsen gibt die diese Woche fehlen, bevorzuge die
    if fehlend and today.weekday() >= 3:  # Ab Donnerstag-Logik einschalten
        # Welche fehlt am ehesten? → die in der Standard-Rotation für diesen Tag,
        # falls die fehlt; sonst irgendeine der fehlenden
        std = standard_rotation.get(today.weekday(), "Grün")
        if std in fehlend:
            return std
        return next(iter(fehlend))

    return standard_rotation.get(today.weekday(), "Grün")


# ========================================
# Wochenfokus-Override (Patricia kann via /fokus setzen)
# ========================================
# Überschreibt den Notion-Wochenplan-Fokus für die aktuelle KW.
# Beispiel: Patricia tippt "/fokus bio-check" → ab jetzt nutzt der Bot
# Bio-Check als Fokus, ignoriert was im Notion-Wochenplan-Body steht.

_fokus_file = STATE_DIR / "wochen-fokus-override.json"


def get_wochen_fokus_override(kw: int = None) -> dict[str, Any] | None:
    """Liest aktuellen Fokus-Override falls existent + nicht abgelaufen."""
    if not _fokus_file.exists():
        return None
    try:
        data = json.loads(_fokus_file.read_text(encoding="utf-8"))
    except Exception:
        return None
    # Override gilt nur für die KW in der er gesetzt wurde
    if kw is None:
        kw = datetime.now().isocalendar().week
    if data.get("kw") != kw:
        return None
    return data


def set_wochen_fokus_override(thema: str, funnel_id: str = None,
                              produkt: str = None, kw: int = None) -> dict[str, Any]:
    """Setzt einen Fokus-Override für die aktuelle KW.

    thema:    Freitext, was diese Woche der Story-Fokus ist
    funnel_id: optional, ID aus active-funnels.json (z.B. "bio-check")
    produkt:  optional, Produkt-Name falls anders als funnel
    """
    if kw is None:
        kw = datetime.now().isocalendar().week
    data = {
        "kw": kw,
        "thema": thema,
        "funnel_id": funnel_id,
        "produkt": produkt,
        "gesetzt_am": datetime.now().isoformat(),
    }
    _fokus_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return data


def clear_wochen_fokus_override():
    if _fokus_file.exists():
        _fokus_file.unlink()


# ========================================
# Briefing-State (Sparringpartner-Modus)
# ========================================
# Bot speichert: hat er heute schon eine Briefing-Frage gestellt? Wartet er auf
# Patricia-Antwort? Oder ist die Antwort schon da?

_briefing_file = STATE_DIR / "briefing-pending.json"


def set_briefing_pending(profil: str, briefing_text: str, fragen: list[str],
                        kontext_snapshot: dict = None) -> dict[str, Any]:
    """Speichert: Bot hat Briefing geschickt, wartet auf Patricia-Antwort."""
    data = {
        "profil": profil,
        "briefing_text": briefing_text,  # was Bot gefragt hat
        "fragen": fragen,                # Liste der Fragen
        "kontext_snapshot": kontext_snapshot or {},  # Wochenkontext zum Zeitpunkt der Frage
        "gesendet_am": datetime.now().isoformat(),
        "patricia_antworten": [],         # gesammelte Antworten (Voice/Text)
        "patricia_fotos": [],             # gesammelte Foto-Pfade
        "patricia_videos": [],            # gesammelte Video-Pfade
        "status": "warten_auf_antwort",
    }
    _briefing_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return data


def get_briefing_pending() -> dict[str, Any] | None:
    """Liest aktuelles Briefing falls vorhanden."""
    if not _briefing_file.exists():
        return None
    try:
        data = json.loads(_briefing_file.read_text(encoding="utf-8"))
        # Briefings älter als 12h verfallen
        gesendet = datetime.fromisoformat(data["gesendet_am"])
        if datetime.now() - gesendet > timedelta(hours=12):
            clear_briefing_pending()
            return None
        return data
    except Exception:
        return None


def add_patricia_antwort(text: str = None, foto: str = None, video: str = None):
    """Fügt eine Patricia-Antwort zum aktuellen Briefing hinzu."""
    data = get_briefing_pending()
    if not data:
        return None
    if text:
        data["patricia_antworten"].append({"text": text, "zeit": datetime.now().isoformat()})
    if foto:
        data["patricia_fotos"].append(foto)
    if video:
        data["patricia_videos"].append(video)
    _briefing_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return data


def clear_briefing_pending():
    if _briefing_file.exists():
        _briefing_file.unlink()


# ========================================
# Wochen-Vorwahl-Cache (von /freitag-hooks)
# ========================================
# Wird gefüllt wenn /freitag-hooks läuft. Bot liest beim daily-render.

def get_wochen_vorwahl(kw: int) -> dict[str, Any] | None:
    """Lese Wochen-Vorwahl-Cache für KW."""
    f = config.OUTPUTS_STORIES_DIR / f"wochen-vorwahl-KW{kw:02d}.json"
    if f.exists():
        try:
            return json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            return None
    return None


def get_wochen_kontext_cache(kw: int) -> dict[str, Any] | None:
    """Lese Wochen-Kontext-Cache (Notion-Snapshot, wird täglich erneuert)."""
    f = config.OUTPUTS_STORIES_DIR / f"wochen-kontext-KW{kw:02d}.json"
    if f.exists():
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            # Cache älter als 24h → expired
            if "abgerufen_am" in data:
                age = datetime.now() - datetime.fromisoformat(data["abgerufen_am"])
                if age > timedelta(hours=24):
                    return None
            return data
        except Exception:
            return None
    return None


def set_wochen_kontext_cache(kw: int, data: dict):
    f = config.OUTPUTS_STORIES_DIR / f"wochen-kontext-KW{kw:02d}.json"
    f.parent.mkdir(parents=True, exist_ok=True)
    data["abgerufen_am"] = datetime.now().isoformat()
    f.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
