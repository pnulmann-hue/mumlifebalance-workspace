"""Notion-Writer — schreibt Tagesplaner-Pages mit Volltext-Briefing.

Wird von bot.py aufgerufen NACH Briefing-Generierung:
1. Notion-Tagesplaner-Page erstellen (oder updaten falls existiert)
2. Tagesfokus-Property setzen
3. Body mit Volltext-Briefing + News-Block füllen
4. URL der Page zurückgeben → wird in Telegram-Push verlinkt
"""

from __future__ import annotations

import logging
from datetime import date
from typing import Any

from notion_client import Client

import config

logger = logging.getLogger(__name__)


_client: Client | None = None


def _get_client() -> Client:
    global _client
    if _client is None:
        if not config.NOTION_API_KEY:
            raise RuntimeError("NOTION_API_KEY fehlt")
        _client = Client(auth=config.NOTION_API_KEY)
    return _client


# ========================================
# Tagesplaner-Page erstellen / updaten
# ========================================

def find_existing_tagesplaner_page(heute: date) -> str | None:
    """Findet existierende Tagesplaner-Page für ein Datum oder None."""
    client = _get_client()
    try:
        results = client.databases.query(
            database_id=config.NOTION_DB_TAGESPLANER,
            filter={
                "property": "Datum",
                "date": {"equals": heute.isoformat()},
            },
            page_size=5,
        ).get("results", [])
        if results:
            return results[0]["id"]
        return None
    except Exception as e:
        logger.warning(f"Tagesplaner-Search-Fehler: {e}")
        return None


def create_or_update_tagesplaner(
    heute: date,
    tagesfokus: str,
    volltext_briefing: str,
) -> str | None:
    """Erstellt neue Tagesplaner-Page oder updatet bestehende.

    Returns: Notion-Page-URL oder None bei Fehler.
    """
    client = _get_client()
    wochentag = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So'][heute.weekday()]
    title = f"{heute.strftime('%d.%m.%Y')} - {wochentag}"

    existing_id = find_existing_tagesplaner_page(heute)

    try:
        if existing_id:
            # Update: nur Properties + Body neu setzen
            client.pages.update(
                page_id=existing_id,
                properties={
                    "Tagesfokus": {
                        "rich_text": [{"text": {"content": tagesfokus[:1900]}}],
                    },
                    "Tag geplant": {"checkbox": True},
                },
            )
            # Body löschen + neu schreiben
            _replace_page_body(existing_id, volltext_briefing)
            return f"https://www.notion.so/{existing_id.replace('-', '')}"
        else:
            # Create: neue Page anlegen
            new_page = client.pages.create(
                parent={"database_id": config.NOTION_DB_TAGESPLANER},
                properties={
                    "Tag": {
                        "title": [{"text": {"content": title}}],
                    },
                    "Datum": {
                        "date": {"start": heute.isoformat()},
                    },
                    "Tagesfokus": {
                        "rich_text": [{"text": {"content": tagesfokus[:1900]}}],
                    },
                    "Tag geplant": {"checkbox": True},
                },
                children=_briefing_to_blocks(volltext_briefing),
            )
            page_id = new_page["id"]
            return f"https://www.notion.so/{page_id.replace('-', '')}"
    except Exception as e:
        logger.error(f"Tagesplaner-Create/Update-Fehler: {e}")
        return None


# ========================================
# Body-Verarbeitung
# ========================================

def _replace_page_body(page_id: str, volltext: str):
    """Löscht alten Body, schreibt neuen."""
    client = _get_client()
    try:
        # Alle Children-Blocks holen
        children = client.blocks.children.list(block_id=page_id, page_size=100)
        for block in children.get("results", []):
            try:
                client.blocks.delete(block_id=block["id"])
            except Exception:
                pass

        # Neue Blocks schreiben
        new_blocks = _briefing_to_blocks(volltext)
        if new_blocks:
            # Notion-API erlaubt max 100 children per call
            client.blocks.children.append(
                block_id=page_id,
                children=new_blocks[:100],
            )
    except Exception as e:
        logger.warning(f"Body-Replace-Fehler: {e}")


def _briefing_to_blocks(volltext: str) -> list[dict]:
    """Wandelt Markdown-Briefing in Notion-Blocks.

    Heuristik:
    - Zeilen mit '##' am Anfang → Heading 2
    - Zeilen mit '###' am Anfang → Heading 3
    - Zeilen die mit '🔗' enthalten → Bookmark/Link-Block
    - URLs im Text → erkennen + als clickbar formatieren
    - Listen mit '•' / '-' / '*' → Bulleted-List
    - Rest → Paragraph
    """
    blocks = []
    lines = volltext.split("\n")
    i = 0

    while i < len(lines):
        line = lines[i].rstrip()
        stripped = line.lstrip()

        if not stripped:
            i += 1
            continue

        # Heading 2
        if stripped.startswith("## "):
            blocks.append({
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": stripped[3:]}}],
                },
            })
        # Heading 3
        elif stripped.startswith("### "):
            blocks.append({
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{"type": "text", "text": {"content": stripped[4:]}}],
                },
            })
        # Heading 1 (selten)
        elif stripped.startswith("# "):
            blocks.append({
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [{"type": "text", "text": {"content": stripped[2:]}}],
                },
            })
        # Bulleted-List (•, -, *)
        elif stripped[0:2] in ("• ", "- ", "* "):
            content = stripped[2:]
            blocks.append({
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": _line_with_links_to_rich_text(content),
                },
            })
        # Divider
        elif stripped.startswith("---"):
            blocks.append({"object": "block", "type": "divider", "divider": {}})
        # Quote/Callout
        elif stripped.startswith(">"):
            blocks.append({
                "object": "block",
                "type": "quote",
                "quote": {
                    "rich_text": [{"type": "text", "text": {"content": stripped[1:].strip()}}],
                },
            })
        # Standard Paragraph mit Link-Erkennung
        else:
            blocks.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": _line_with_links_to_rich_text(stripped),
                },
            })

        i += 1

    return blocks


def _line_with_links_to_rich_text(line: str) -> list[dict]:
    """Erkennt URLs in einer Zeile und macht sie klickbar.

    Notion-rich-text-Format: Liste von Text-Objekten, einige mit href.
    """
    import re
    url_pattern = r'(https?://[^\s\)]+)'
    parts = re.split(url_pattern, line)

    rich = []
    for part in parts:
        if not part:
            continue
        if re.match(url_pattern, part):
            # Es ist eine URL
            rich.append({
                "type": "text",
                "text": {"content": part, "link": {"url": part}},
                "annotations": {"color": "blue"},
            })
        else:
            # Plain text — Notion erlaubt max 2000 chars per text-object
            rich.append({
                "type": "text",
                "text": {"content": part[:2000]},
            })

    if not rich:
        rich = [{"type": "text", "text": {"content": line[:2000]}}]
    return rich


# ========================================
# CLI-Test
# ========================================
if __name__ == "__main__":
    import sys
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    test_volltext = """## Tagesbriefing Test

Heute ist ein Test-Tag.

### News
• Claude Update: Anthropic hat etwas neues released.
  → Quelle: https://www.anthropic.com/news/claude-2026

• Instagram: Neuer Algorithmus.
  → https://socialmediatoday.com/test
"""
    print("=== Notion-Writer Test ===")
    url = create_or_update_tagesplaner(date.today(), "Test-Fokus", test_volltext)
    print(f"Notion-URL: {url}")
