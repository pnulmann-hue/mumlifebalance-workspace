"""Notion-Lese-Modul für Story-Render-Bot.

Liest Patricias Notion-DBs:
- Monatsplanung-DB (3 Monatsziele, Launch-Fokus)
- Wochenplanung-DB (Fokus der Woche, Content-Creation-Zelle)
- Content-Themenplanung-DB (welches Produkt aktuell beworben wird)
- Content-Management-DB (was wurde schon gepostet — Wiederholungs-Vermeidung)

Cache-Logik: 24h-Snapshot pro KW in outputs/stories/wochen-kontext-KW##.json.
Bei zweitem Aufruf am gleichen Tag → wird aus Cache gelesen, kein Notion-Roundtrip.
"""

from __future__ import annotations

import logging
from datetime import date, datetime
from typing import Any

from notion_client import Client

import config

# state-Modul nicht im Cockpit-Bot (kein Cache nötig, jeder Push frisch)
class _StubState:
    def get_wochen_kontext_cache(self, kw): return None
    def set_wochen_kontext_cache(self, kw, kontext): pass
state = _StubState()

logger = logging.getLogger(__name__)


# ========================================
# Client (lazy init)
# ========================================
_client: Client | None = None


def _get_client() -> Client:
    global _client
    if _client is None:
        if not config.NOTION_API_KEY:
            raise RuntimeError("NOTION_API_KEY fehlt in .env")
        _client = Client(auth=config.NOTION_API_KEY)
    return _client


# ========================================
# Helper: Notion-Property-Extraktion
# ========================================

def _text_from_rich_text(rich_text_list: list[dict]) -> str:
    """Extrahiert plain_text aus einer Notion rich_text/title-Liste."""
    if not rich_text_list:
        return ""
    return "".join(rt.get("plain_text", "") for rt in rich_text_list).strip()


def _prop_value(prop: dict) -> Any:
    """Universal-Extraktor für Notion-Properties."""
    if not prop:
        return None
    typ = prop.get("type")

    if typ == "title":
        return _text_from_rich_text(prop["title"])
    if typ == "rich_text":
        return _text_from_rich_text(prop["rich_text"])
    if typ == "select":
        sel = prop.get("select")
        return sel["name"] if sel else None
    if typ == "multi_select":
        return [s["name"] for s in prop.get("multi_select", [])]
    if typ == "checkbox":
        return prop.get("checkbox", False)
    if typ == "number":
        return prop.get("number")
    if typ == "date":
        d = prop.get("date")
        if not d:
            return None
        return {"start": d.get("start"), "end": d.get("end")}
    if typ == "url":
        return prop.get("url")
    if typ == "email":
        return prop.get("email")
    if typ == "status":
        s = prop.get("status")
        return s["name"] if s else None
    if typ == "relation":
        return [r["id"] for r in prop.get("relation", [])]
    if typ == "people":
        return [p.get("name", p.get("id", "")) for p in prop.get("people", [])]
    return None


def _extract_properties(page: dict) -> dict[str, Any]:
    """Wandelt Notion-Page in flaches Dict { property_name: value }."""
    out = {}
    for name, prop in page.get("properties", {}).items():
        out[name] = _prop_value(prop)
    return out


# ========================================
# Page-Body lesen (für Tabellen + Sub-Pages)
# ========================================

def _get_page_blocks(page_id: str) -> list[dict]:
    """Holt alle Blocks einer Page (max. 100, kein Pagination — reicht für Patricia)."""
    client = _get_client()
    try:
        result = client.blocks.children.list(block_id=page_id, page_size=100)
        return result.get("results", [])
    except Exception as e:
        logger.warning(f"Konnte Blocks für Page {page_id} nicht lesen: {e}")
        return []


def _block_to_text(block: dict) -> str:
    """Wandelt einen einzelnen Block in Text."""
    typ = block.get("type")
    data = block.get(typ, {})

    if typ in {"paragraph", "heading_1", "heading_2", "heading_3", "bulleted_list_item",
              "numbered_list_item", "quote", "callout", "to_do"}:
        return _text_from_rich_text(data.get("rich_text", []))
    if typ == "code":
        return _text_from_rich_text(data.get("rich_text", []))
    return ""


def _page_body_as_text(page_id: str, max_chars: int = 4000) -> str:
    """Liest komplette Page als zusammenhängenden Text (für KI-Kontext)."""
    blocks = _get_page_blocks(page_id)
    parts = []
    for b in blocks:
        txt = _block_to_text(b).strip()
        if txt:
            parts.append(txt)
        # Heading-Hierarchie als Marker
        if b.get("type", "").startswith("heading"):
            parts[-1] = f"\n## {parts[-1]}"
    text = "\n".join(parts)
    if len(text) > max_chars:
        text = text[:max_chars] + "\n[... gekürzt ...]"
    return text


# ========================================
# Produkt-Resolver (für Relation-Felder im Monats-/Wochenplan)
# ========================================
# Cache, damit wir nicht jede Story-Generierung 4× die gleiche Produkt-Page laden
_produkt_cache: dict[str, dict[str, Any]] = {}


def resolve_produkt(page_id: str) -> dict[str, Any] | None:
    """Holt Name + Kategorie + Preis aus einer Produkte-DB-Page.

    Der Notion-Reader kriegt aus Relation-Feldern nur Page-IDs zurück.
    Diese Funktion löst eine ID zu einem brauchbaren Dict auf.

    Cache: pro Bot-Lauf wird jede Produkt-Page nur 1× geladen.
    """
    if not page_id:
        return None
    if page_id in _produkt_cache:
        return _produkt_cache[page_id]

    client = _get_client()
    try:
        page = client.pages.retrieve(page_id=page_id)
        props = _extract_properties(page)
        result = {
            "id": page_id,
            "name": props.get("Name", "(unbenannt)"),
            "kategorie": props.get("Kategorie"),  # Free Offer / Low / Mid / High Price Offer
            "preis": props.get("Preis"),
        }
        _produkt_cache[page_id] = result
        return result
    except Exception as e:
        logger.warning(f"Konnte Produkt-Page {page_id} nicht laden: {e}")
        return {"id": page_id, "name": "(Produkt nicht ladbar)", "kategorie": None, "preis": None}


def _resolve_produkt_liste(rel: Any) -> list[dict[str, Any]]:
    """Wandelt eine Relation-Property (Liste von Page-IDs) in Produkt-Dicts."""
    if not rel:
        return []
    if isinstance(rel, list):
        return [resolve_produkt(pid) for pid in rel if pid]
    return []


# ========================================
# Wochenplanung
# ========================================

def get_wochenplan_kw(kw: int, jahr: int = None) -> dict[str, Any] | None:
    """Lädt Wochenplan für KW.

    Patricia's Wochenplan-Titel sind Datum-basiert (z.B. „21.–30. April 2026"),
    NICHT „KW 18". Wir nutzen darum:
    1. Berechne Datum-Range für KW (Mo-So)
    2. Hol alle Wochenplan-Einträge (max 100)
    3. Match: Title enthält Datum aus Range, oder Zeitraum-Property überlappt mit KW
    """
    if jahr is None:
        jahr = datetime.now().year

    # KW → Mo-So Date-Range
    try:
        kw_start = date.fromisocalendar(jahr, kw, 1)  # Montag
        kw_end = date.fromisocalendar(jahr, kw, 7)    # Sonntag
    except ValueError:
        return None

    client = _get_client()
    try:
        # Hol alle Einträge (Patricia hat überschaubar viele)
        results = client.databases.query(
            database_id=config.NOTION_DB_WOCHENPLANUNG,
            page_size=100,
        ).get("results", [])

        # Match-Strategie 1: Zeitraum-Property überschneidet KW-Range
        candidates = []
        for page in results:
            props = _extract_properties(page)
            zeitraum = props.get("Zeitraum")
            if zeitraum and zeitraum.get("start"):
                try:
                    z_start = date.fromisoformat(zeitraum["start"][:10])
                    z_end_str = zeitraum.get("end") or zeitraum["start"]
                    z_end = date.fromisoformat(z_end_str[:10])
                    # Überlappung Check
                    if z_start <= kw_end and z_end >= kw_start:
                        candidates.append((page, props, "zeitraum_match"))
                except (ValueError, TypeError):
                    pass

        # Match-Strategie 2 (Fallback): Title enthält Tag aus KW-Range
        if not candidates:
            tage_im_range = [(kw_start + (kw_end - kw_start) * d / 6) for d in range(7)]
            for page in results:
                props = _extract_properties(page)
                title = ""
                for v in props.values():
                    if isinstance(v, str):
                        title = v
                        break
                # Suche Tag.Monat im Titel
                for t in [kw_start, kw_end]:
                    needles = [
                        f"{t.day}.{t.month}.",
                        f"{t.day}. ",
                        f"{t.day}.{t.month:02d}",
                    ]
                    if any(n in title for n in needles):
                        candidates.append((page, props, f"title_match:{title}"))
                        break

        if not candidates:
            logger.info(f"Kein Wochenplan für KW {kw} ({kw_start} – {kw_end}) gefunden")
            return None

        page, props, match_type = candidates[0]
        body = _page_body_as_text(page["id"], max_chars=3000)

        # NEUE FELDER: Wochen-Hauptprodukt (Relation) + Sales-Pattern (Text)
        hauptprodukt_rel = props.get("🎯 Wochen-Hauptprodukt") or props.get("Wochen-Hauptprodukt")
        hauptprodukte = _resolve_produkt_liste(hauptprodukt_rel)
        sales_pattern = props.get("📅 Sales-Pattern") or props.get("Sales-Pattern") or ""

        return {
            "id": page["id"],
            "properties": props,
            "fokus_der_woche": props.get("Fokus der Woche", ""),
            "zeitraum": props.get("Zeitraum"),
            "body_text": body,
            "match_type": match_type,
            "kw_range": f"{kw_start.isoformat()} – {kw_end.isoformat()}",
            # NEU
            "wochen_hauptprodukt": hauptprodukte[0] if hauptprodukte else None,
            "wochen_hauptprodukte_alle": hauptprodukte,
            "sales_pattern": sales_pattern,
        }
    except Exception as e:
        logger.error(f"Wochenplan-Lese-Fehler KW {kw}: {e}")
        return None


# ========================================
# Monatsplanung
# ========================================

_MONATE = {
    1: "Januar", 2: "Februar", 3: "März", 4: "April",
    5: "Mai", 6: "Juni", 7: "Juli", 8: "August",
    9: "September", 10: "Oktober", 11: "November", 12: "Dezember",
}


def get_monatsplan(monat_nr: int = None, jahr: int = None) -> dict[str, Any] | None:
    """Lädt Monatsplan z.B. „Mai 2026"."""
    today = datetime.now()
    if monat_nr is None:
        monat_nr = today.month
    if jahr is None:
        jahr = today.year

    monat_name = _MONATE[monat_nr]
    suchterm = f"{monat_name} {jahr}"

    client = _get_client()
    try:
        results = client.databases.query(
            database_id=config.NOTION_DB_MONATSPLANUNG,
            filter={
                "property": "Monat + Jahr",
                "title": {"contains": suchterm},
            },
            page_size=5,
        ).get("results", [])

        if not results:
            # Fallback: nur Monatsname
            results = client.databases.query(
                database_id=config.NOTION_DB_MONATSPLANUNG,
                filter={
                    "property": "Monat + Jahr",
                    "title": {"contains": monat_name},
                },
                page_size=5,
            ).get("results", [])

        if not results:
            logger.info(f"Kein Monatsplan für {suchterm} gefunden")
            return None

        page = results[0]
        props = _extract_properties(page)
        body = _page_body_as_text(page["id"], max_chars=4000)

        # NEUE FELDER: 3-Produkte-Treppe (Julia Trost Methode)
        gratis_rel = props.get("🎁 Gratis-Fokus") or props.get("Gratis-Fokus")
        mini_rel = props.get("💸 Mini-Fokus") or props.get("Mini-Fokus")
        gross_rel = props.get("👑 Gross-Fokus") or props.get("Gross-Fokus")
        begruendung = props.get("✏️ Begründung Fokus") or props.get("Begründung Fokus") or ""

        gratis_p = _resolve_produkt_liste(gratis_rel)
        mini_p = _resolve_produkt_liste(mini_rel)
        gross_p = _resolve_produkt_liste(gross_rel)

        return {
            "id": page["id"],
            "monat": suchterm,
            "properties": props,
            "drei_monatsziele": props.get("3 Monatsziele", ""),
            "zeitraum": props.get("Zeitraum"),
            "body_text": body,
            # NEU: 3-Produkte-Treppe
            "gratis_fokus": gratis_p[0] if gratis_p else None,
            "mini_fokus": mini_p[0] if mini_p else None,
            "gross_fokus": gross_p[0] if gross_p else None,
            "begruendung_fokus": begruendung,
        }
    except Exception as e:
        logger.error(f"Monatsplan-Lese-Fehler {suchterm}: {e}")
        return None


# ========================================
# Aufgaben-DB (offene Tasks heute + Habit-Goals)
# ========================================

def get_offene_tasks_heute(heute: date = None, limit: int = 15) -> list[dict[str, Any]]:
    """Lädt offene Tasks für heute oder überfällig aus Aufgaben-DB."""
    if heute is None:
        heute = date.today()

    client = _get_client()
    try:
        results = client.databases.query(
            database_id=config.NOTION_DB_AUFGABEN,
            page_size=50,
        ).get("results", [])

        tasks = []
        for page in results:
            props = _extract_properties(page)
            status = props.get("Status")
            if status in ("Abgeschlossen", "Vorlage"):
                continue
            datum = props.get("Datum")
            faellig = False
            if datum and datum.get("start"):
                try:
                    d_start = date.fromisoformat(datum["start"][:10])
                    if d_start <= heute:
                        faellig = True
                except (ValueError, TypeError):
                    pass

            if faellig or status in ("Aktiv", "Termin", "Wartend"):
                tasks.append({
                    "id": page["id"],
                    "aufgabe": props.get("Aufgabe", ""),
                    "status": status,
                    "prioritaet": props.get("Priorität", "Prio 3"),
                    "datum": datum,
                })

        # Sort: Prio 1 first
        prio_order = {"Quick Win": 0, "Prio 1": 1, "Prio 2": 2, "Prio 3": 3}
        tasks.sort(key=lambda t: prio_order.get(t["prioritaet"], 99))
        return tasks[:limit]
    except Exception as e:
        logger.error(f"Aufgaben-DB-Lese-Fehler: {e}")
        return []


def get_aktive_habit_goals() -> list[dict[str, Any]]:
    """Lädt aktive Habit Goals aus Ziele-DB."""
    client = _get_client()
    try:
        results = client.databases.query(
            database_id=config.NOTION_DB_ZIELE,
            page_size=30,
        ).get("results", [])

        habits = []
        for page in results:
            props = _extract_properties(page)
            if props.get("Status") == "Aktiv" and props.get("Art des Ziels") == "Habit Goal":
                habits.append({
                    "id": page["id"],
                    "name": props.get("Name", ""),
                    "qualitativ": props.get("Qualitatives Ziel", ""),
                })
        return habits
    except Exception as e:
        logger.error(f"Ziele-DB-Lese-Fehler: {e}")
        return []


# ========================================
# Content-Themenplanung
# ========================================

def get_themen_planung_aktuell(monat_nr: int = None, jahr: int = None) -> list[dict[str, Any]]:
    """Lädt aktuelle Themenplanungs-Einträge.

    Themenplanung ist (Stand 2026-05-01) keine eigene DB sondern eine Sektion
    im Monatsplanung-Body. Diese Funktion ist Stub für spätere Erweiterung.
    """
    if not config.NOTION_DB_THEMENPLANUNG:
        return []
    client = _get_client()
    try:
        results = client.databases.query(
            database_id=config.NOTION_DB_THEMENPLANUNG,
            page_size=50,
        ).get("results", [])

        out = []
        for page in results:
            props = _extract_properties(page)
            out.append({
                "id": page["id"],
                "properties": props,
            })
        return out
    except Exception as e:
        logger.error(f"Themenplanung-Lese-Fehler: {e}")
        return []


def get_jahresplan(jahr: int = None) -> dict[str, Any] | None:
    """Lädt Jahresplan (Master-Strategie). Sucht „Jahresplanung 2026"."""
    if jahr is None:
        jahr = datetime.now().year
    client = _get_client()
    try:
        results = client.databases.query(
            database_id=config.NOTION_DB_JAHRESPLANUNG,
            page_size=10,
        ).get("results", [])
        if not results:
            return None

        # Filter clientseitig: Title enthält das Jahr
        ziel_pages = []
        for page in results:
            props = _extract_properties(page)
            title = ""
            for v in props.values():
                if isinstance(v, str) and str(jahr) in v:
                    title = v
                    break
            if title:
                ziel_pages.append((page, props, title))

        if not ziel_pages and results:
            # Fallback: erste Page nehmen
            page = results[0]
            props = _extract_properties(page)
            ziel_pages = [(page, props, "Jahresplan")]

        page, props, title = ziel_pages[0]
        body = _page_body_as_text(page["id"], max_chars=5000)
        return {
            "id": page["id"],
            "jahr": jahr,
            "title": title,
            "properties": props,
            "body_text": body,
        }
    except Exception as e:
        logger.error(f"Jahresplan-Lese-Fehler {jahr}: {e}")
        return None


def get_aktuelle_produkte_im_launch() -> list[dict[str, Any]]:
    """Lädt Produkte aus DB die aktuell im Launch sind (Status = Launching/Pre-Sale)."""
    client = _get_client()
    try:
        results = client.databases.query(
            database_id=config.NOTION_DB_PRODUKTE,
            page_size=20,
        ).get("results", [])

        out = []
        for page in results:
            props = _extract_properties(page)
            status = props.get("Status", "") or ""
            if any(k in str(status).lower() for k in ["launch", "pre-sale", "aktiv", "live"]):
                out.append({
                    "id": page["id"],
                    "properties": props,
                })
        return out
    except Exception as e:
        logger.error(f"Produkte-Lese-Fehler: {e}")
        return []


# ========================================
# Content-Management (was wurde schon gepostet)
# ========================================

def get_letzte_gepostete_stories(profil: str = None, limit: int = 14) -> list[dict[str, Any]]:
    """Lädt die letzten X Story-Posts aus Content-Management-DB.

    Für Wiederholungs-Vermeidung — Hook/Thema sollte sich nicht innerhalb 14 Tagen wiederholen.
    """
    client = _get_client()
    try:
        results = client.databases.query(
            database_id=config.NOTION_DB_CONTENT_MGMT,
            page_size=limit * 2,  # mehr holen, weil filter clientseitig
            sorts=[{"timestamp": "created_time", "direction": "descending"}],
        ).get("results", [])

        out = []
        for page in results[:limit]:
            props = _extract_properties(page)
            out.append({
                "id": page["id"],
                "properties": props,
            })
        return out
    except Exception as e:
        logger.error(f"Content-Mgmt-Lese-Fehler: {e}")
        return []


# ========================================
# Haupt-Funktion: Wochenkontext für heute
# ========================================

def lade_wochen_kontext(kw: int = None, force_refresh: bool = False) -> dict[str, Any]:
    """Lädt kompletten Wochenkontext (Monats + Wochen + Themen) — gecached.

    Returns:
      {
        "kw": 18,
        "monatsplan": {...} | None,
        "wochenplan": {...} | None,
        "themen": [...],
        "abgerufen_am": "ISO-timestamp",
      }
    """
    if kw is None:
        kw = datetime.now().isocalendar().week

    # Cache-Check
    if not force_refresh:
        cached = state.get_wochen_kontext_cache(kw)
        if cached:
            logger.info(f"Wochenkontext KW {kw} aus Cache (frisch < 24h)")
            return cached

    logger.info(f"Lade Wochenkontext KW {kw} aus Notion...")
    monatsplan = get_monatsplan()
    wochenplan = get_wochenplan_kw(kw)
    themen = get_themen_planung_aktuell()

    kontext = {
        "kw": kw,
        "monatsplan": monatsplan,
        "wochenplan": wochenplan,
        "themen": themen,
    }

    # Cache schreiben
    state.set_wochen_kontext_cache(kw, kontext)
    return kontext


# ========================================
# Health-Check
# ========================================

def healthcheck() -> dict[str, Any]:
    """Prüft ob alle 4 DBs erreichbar sind."""
    client = _get_client()
    out = {"ok": True, "details": {}}

    dbs = {
        "Wochenplanung": config.NOTION_DB_WOCHENPLANUNG,
        "Monatsplanung": config.NOTION_DB_MONATSPLANUNG,
        "Jahresplanung": config.NOTION_DB_JAHRESPLANUNG,
        "Content-Management": config.NOTION_DB_CONTENT_MGMT,
        "Produkte": config.NOTION_DB_PRODUKTE,
    }

    for name, db_id in dbs.items():
        try:
            r = client.databases.query(database_id=db_id, page_size=1)
            count = len(r.get("results", []))
            out["details"][name] = {"ok": True, "sample_count": count}
        except Exception as e:
            out["ok"] = False
            out["details"][name] = {"ok": False, "error": str(e)}

    return out


# ========================================
# CLI-Tester
# ========================================
if __name__ == "__main__":
    import sys
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    print("=== Notion-Reader Healthcheck ===")
    hc = healthcheck()
    print(f"Gesamt: {'[OK]' if hc['ok'] else '[FEHLER]'}")
    for name, info in hc["details"].items():
        status = "[OK]" if info["ok"] else "[FEHLER]"
        if info["ok"]:
            print(f"  {status} {name} (Sample: {info['sample_count']})")
        else:
            print(f"  {status} {name} — {info['error']}")

    print("\n=== Aktueller Monatsplan ===")
    m = get_monatsplan()
    if m:
        print(f"  Monat: {m['monat']}")
        print(f"  Ziele: {m['drei_monatsziele'][:200]}")
    else:
        print("  Kein Monatsplan gefunden.")

    print("\n=== Aktueller Wochenplan ===")
    kw = datetime.now().isocalendar().week
    w = get_wochenplan_kw(kw)
    if w:
        print(f"  KW: {kw}")
        print(f"  Fokus: {w['fokus_der_woche'][:200]}")
    else:
        print(f"  Kein Wochenplan für KW {kw} gefunden.")
