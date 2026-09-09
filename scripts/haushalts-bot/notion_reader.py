"""Notion-Lese-Modul fuer den Haushalts-Bot.

Liest die "🏠 Haushalts-Liste" (eine flache DB) komplett aus und gibt eine
Liste normalisierter Eintraege zurueck. Nutzt den Standard-REST-Endpoint
(databases.query) — funktioniert auf jedem Notion-Plan, anders als die
MCP-Bulk-Query (die einen Business-Plan braucht).

Zusaetzlich: lade_business_aufgaben() holt die offenen Eintraege aus der
Business-Aufgaben-DB, damit das Vorabend-Briefing privat UND Business zeigt.
"""

from __future__ import annotations

import logging
from typing import Any

import requests
from notion_client import Client

import config

logger = logging.getLogger(__name__)

# Lesefehler werden hier gesammelt, statt nur im Log zu landen. Das Briefing
# zeigt sie als eigenen Block — sonst sieht Patricia bei einem kaputten Zugriff
# nur einen leeren Abschnitt und haelt ihn faelschlich fuer "nichts geplant".
# Genau so blieb der Content-Read tagelang unbemerkt kaputt.
LESE_FEHLER: list[str] = []

_client: Client | None = None


def _get_client() -> Client:
    global _client
    if _client is None:
        if not config.NOTION_API_KEY:
            raise RuntimeError("NOTION_TOKEN fehlt")
        _client = Client(auth=config.NOTION_API_KEY)
    return _client


def _text(rich: list[dict]) -> str:
    if not rich:
        return ""
    return "".join(r.get("plain_text", "") for r in rich).strip()


def _prop(prop: dict) -> Any:
    if not prop:
        return None
    t = prop.get("type")
    if t == "title":
        return _text(prop["title"])
    if t == "rich_text":
        return _text(prop["rich_text"])
    if t == "select":
        s = prop.get("select")
        return s["name"] if s else None
    if t == "multi_select":
        return [o["name"] for o in prop.get("multi_select", [])]
    if t == "url":
        return prop.get("url")
    if t == "checkbox":
        return prop.get("checkbox", False)
    if t == "date":
        d = prop.get("date")
        return d.get("start") if d else None
    return None


def lade_haushalt_eintraege() -> list[dict[str, Any]]:
    """Holt alle Eintraege der Haushalts-Liste (paginiert).

    Returns Liste von Dicts:
      { aufgabe, bereich, wer, rhythmus, wochentag, fixes_datum, notiz, erledigt }
    """
    client = _get_client()
    eintraege: list[dict[str, Any]] = []
    cursor = None

    while True:
        kwargs: dict[str, Any] = {
            "database_id": config.NOTION_DB_HAUSHALT,
            "page_size": 100,
        }
        if cursor:
            kwargs["start_cursor"] = cursor
        try:
            res = client.databases.query(**kwargs)
        except Exception as e:
            logger.error(f"Haushalts-Liste konnte nicht gelesen werden: {e}")
            raise

        for page in res.get("results", []):
            p = page.get("properties", {})
            eintraege.append({
                "id": page.get("id"),
                "aufgabe": _prop(p.get("Aufgabe")) or "",
                "bereich": _prop(p.get("Bereich")),
                "wer": _prop(p.get("Wer")),
                "rhythmus": _prop(p.get("Rhythmus")),
                "wochentag": _prop(p.get("Wochentag")),
                "fixes_datum": _prop(p.get("Fixes Datum")),
                "notiz": _prop(p.get("Notiz")) or "",
                "erledigt": bool(_prop(p.get("Erledigt"))),
            })

        if res.get("has_more"):
            cursor = res.get("next_cursor")
        else:
            break

    return eintraege


def _query_datasource(data_source_id: str, filter_: dict | None = None) -> list[dict]:
    """Paginierte Abfrage ueber den data_sources-Endpoint (API 2025-09-03).

    Der alte databases/{id}/query lehnt Datenbanken mit mehreren Datenquellen
    ab ("multiple data sources are not supported in this API version") — genau
    das ist bei der Content-Management-DB der Fall. Der data_sources-Endpoint
    kennt dieses Problem nicht, ist aber in notion-client 2.2.1 noch nicht
    abgebildet, darum hier direkt per HTTP.
    """
    url = f"https://api.notion.com/v1/data_sources/{data_source_id}/query"
    headers = {
        "Authorization": f"Bearer {config.NOTION_API_KEY}",
        "Notion-Version": config.NOTION_VERSION,
        "Content-Type": "application/json",
    }
    pages: list[dict] = []
    cursor = None
    while True:
        body: dict[str, Any] = {"page_size": 100}
        if filter_:
            body["filter"] = filter_
        if cursor:
            body["start_cursor"] = cursor
        resp = requests.post(url, headers=headers, json=body, timeout=30)
        if not resp.ok:
            raise RuntimeError(f"Notion {resp.status_code}: {resp.text[:300]}")
        res = resp.json()
        pages.extend(res.get("results", []))
        if not res.get("has_more"):
            break
        cursor = res.get("next_cursor")
    return pages


def _query_all(
    database_id: str,
    filter_: dict | None = None,
    data_source_id: str | None = None,
) -> list[dict]:
    """Holt alle Zeilen — bevorzugt ueber die Data-Source, sonst klassisch.

    Die Data-Source-Variante deckt auch Mehrquellen-Datenbanken ab; schlaegt
    sie fehl (z.B. weil die Integration die Quelle nicht sieht), faellt der
    Aufruf auf databases.query zurueck.
    """
    if data_source_id:
        try:
            return _query_datasource(data_source_id, filter_)
        except Exception as e:
            logger.warning(
                f"Data-Source-Abfrage fehlgeschlagen ({e}) — versuche databases.query"
            )

    client = _get_client()
    pages: list[dict] = []
    cursor = None
    while True:
        kwargs: dict[str, Any] = {"database_id": database_id, "page_size": 100}
        if filter_:
            kwargs["filter"] = filter_
        if cursor:
            kwargs["start_cursor"] = cursor
        res = client.databases.query(**kwargs)
        pages.extend(res.get("results", []))
        if not res.get("has_more"):
            break
        cursor = res.get("next_cursor")
    return pages


def lade_business_aufgaben() -> list[dict[str, Any]]:
    """Holt die offenen Business-Aufgaben (Status offen, nicht abgehakt).

    Gibt [] zurueck (statt zu werfen), wenn die DB nicht erreichbar ist —
    ein fehlender Business-Teil darf den Vorabend-Push nie verhindern.

    Returns Liste von Dicts:
      { aufgabe, status, prioritaet, datum, anmerkung }
    """
    filter_ = {
        "and": [
            {"property": "Erledigt (für Projekte)", "checkbox": {"equals": False}},
            {"or": [
                {"property": "Status", "select": {"equals": s}}
                for s in config.BUSINESS_STATUS_OFFEN
            ]},
        ]
    }
    try:
        pages = _query_all(
            config.NOTION_DB_AUFGABEN, filter_, config.NOTION_DS_AUFGABEN
        )
    except Exception as e:
        logger.warning(f"Business-Aufgaben konnten nicht gelesen werden: {e}")
        LESE_FEHLER.append(f"Business-Aufgaben nicht lesbar: {e}")
        return []

    aufgaben: list[dict[str, Any]] = []
    for page in pages:
        p = page.get("properties", {})
        aufgaben.append({
            "id": page.get("id"),
            "aufgabe": _prop(p.get("Aufgabe")) or "",
            "status": _prop(p.get("Status")),
            "prioritaet": _prop(p.get("Priorität")),
            "datum": _prop(p.get("Datum")),
            "anmerkung": _prop(p.get("Anmerkung")) or "",
        })
    return aufgaben


def lade_content_plan(von: str, bis: str) -> list[dict[str, Any]]:
    """Holt die Content-Eintraege mit Veroeffentlichungs-Datum im Bereich.

    Gibt [] zurueck (statt zu werfen), wenn die DB nicht erreichbar ist.

    Returns Liste von Dicts:
      { titel, typen, profil, status, datum, keyword, saeule, storyart,
        canva, briefing }
    """
    filter_ = {
        "and": [
            {"property": "Veröffentlichung", "date": {"on_or_after": von}},
            {"property": "Veröffentlichung", "date": {"on_or_before": bis}},
        ]
    }
    try:
        pages = _query_all(
            config.NOTION_DB_CONTENT, filter_, config.NOTION_DS_CONTENT
        )
    except Exception as e:
        logger.warning(f"Content-Plan konnte nicht gelesen werden: {e}")
        LESE_FEHLER.append(f"Content-Plan nicht lesbar: {e}")
        return []

    eintraege: list[dict[str, Any]] = []
    for page in pages:
        p = page.get("properties", {})
        eintraege.append({
            "id": page.get("id"),
            "titel": _prop(p.get("Content-Titel")) or "",
            "typen": _prop(p.get("Content-Typ")) or [],
            "profil": _prop(p.get("Profil")),
            "status": _prop(p.get("Status")),
            "datum": _prop(p.get("Veröffentlichung")),
            "keyword": _prop(p.get("Keyword")) or "",
            "storyart": _prop(p.get("Storyart")),
            "canva": _prop(p.get("Canva-Link")),
            "briefing": _prop(p.get("Briefing-Link")),
        })
    return eintraege


if __name__ == "__main__":
    import sys
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    eintraege = lade_haushalt_eintraege()
    print(f"{len(eintraege)} Eintraege gelesen:\n")
    for e in eintraege:
        flag = "[x]" if e["erledigt"] else "[ ]"
        print(f"  {flag} {e['aufgabe']} | {e['bereich']} | {e['rhythmus']} | "
              f"{e['wochentag']} | {e['fixes_datum']} | Wer={e['wer']}")

    business = lade_business_aufgaben()
    print(f"\n{len(business)} offene Business-Aufgaben:\n")
    for b in business:
        print(f"  - {b['aufgabe']} | {b['status']} | {b['prioritaet']} | {b['datum']}")

    from datetime import date, timedelta
    heute = date.today()
    content = lade_content_plan(heute.isoformat(), (heute + timedelta(days=7)).isoformat())
    print(f"\n{len(content)} Content-Eintraege in den naechsten 7 Tagen:\n")
    for c in content:
        print(f"  - {c['datum']} | {c['typen']} | {c['profil']} | {c['status']} | {c['titel']}")
