"""Notion-Lese-Modul fuer den Haushalts-Bot.

Liest die "🏠 Haushalts-Liste" (eine flache DB) komplett aus und gibt eine
Liste normalisierter Eintraege zurueck. Nutzt den Standard-REST-Endpoint
(databases.query) — funktioniert auf jedem Notion-Plan, anders als die
MCP-Bulk-Query (die einen Business-Plan braucht).
"""

from __future__ import annotations

import logging
from typing import Any

from notion_client import Client

import config

logger = logging.getLogger(__name__)

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
