"""News-Fetcher — sammelt täglich aktuelle News für Patricia's Themen.

Themen (alle parallel):
- KI / Claude (Updates, neue Models, AI-News)
- Instagram (Algorithm, Features, Trends)
- Digitale Produkte / Solopreneur (Indie Hackers, Trends)
- Markt-Trends (allgemeine Business-News)
- YouTube-Videos der Woche zu diesen Themen

Output: kompakter News-Block (max 500-800 Zeichen) für Telegram-Briefing.
"""

from __future__ import annotations

import logging
from datetime import date, timedelta
from typing import Any

import httpx
from anthropic import Anthropic

import config

logger = logging.getLogger(__name__)


_client: Anthropic | None = None


def _get_client() -> Anthropic:
    global _client
    if _client is None:
        _client = Anthropic(api_key=config.ANTHROPIC_API_KEY)
    return _client


# ========================================
# Web-Search via Anthropic-Tool (Claude kann web_search nutzen)
# ========================================

def _search_via_claude(query: str, max_results: int = 3) -> str:
    """Nutzt Claude mit web_search-Tool um aktuelle News zu finden."""
    try:
        client = _get_client()
        response = client.messages.create(
            model=config.CLAUDE_MODEL,
            max_tokens=1500,
            tools=[{"type": "web_search_20250305", "name": "web_search", "max_uses": 3}],
            messages=[{
                "role": "user",
                "content": f"""Suche aktuelle News (letzte 7 Tage) zum Thema: {query}

Gib mir die TOP 3 wichtigsten Ergebnisse zurück, jeweils:
- Titel (max 80 Zeichen)
- 1 Satz worum es geht (max 120 Zeichen)
- Quelle/URL

KEINE allgemeine Erklärungen, nur die 3 Ergebnisse als Liste.
Format pro Ergebnis:
• [Titel]
  [1-Satz-Beschreibung] ([Quelle])
"""
            }],
        )

        # Extract Text — nur text-Blocks, robust gegen tool_use/tool_result
        text_parts = []
        for block in response.content:
            block_type = getattr(block, "type", None)
            if block_type == "text":
                text = getattr(block, "text", None)
                if text:
                    text_parts.append(text)

        return "\n".join(text_parts).strip()
    except Exception as e:
        logger.warning(f"Web-Search für '{query}' fehlgeschlagen: {e}")
        return ""


# ========================================
# Kategorien
# ========================================

def generate_query_topics(monatsplan: dict | None, wochenplan: dict | None) -> dict[str, str]:
    """Generiert dynamisch passende News-Queries basierend auf Patricia's
    aktuellem Monats-Trio + Wochenfokus.

    Nutzt Claude um aus dem Notion-Kontext relevante Search-Queries zu erzeugen.

    Returns: dict {Themen-Name: Search-Query}
    """
    # Kontext für Claude zusammenstellen
    kontext_parts = []
    if monatsplan:
        if monatsplan.get("monat"):
            kontext_parts.append(f"Monat: {monatsplan['monat']}")
        gross = monatsplan.get("gross_fokus")
        mini = monatsplan.get("mini_fokus")
        gratis = monatsplan.get("gratis_fokus")
        if gross:
            kontext_parts.append(f"Gross-Produkt-Fokus: {gross.get('name', '')}")
        if mini:
            kontext_parts.append(f"Mini-Produkt-Fokus: {mini.get('name', '')}")
        if gratis:
            kontext_parts.append(f"Gratis-Produkt-Fokus: {gratis.get('name', '')}")
        if monatsplan.get("begruendung_fokus"):
            kontext_parts.append(f"Begründung Fokus:\n{monatsplan['begruendung_fokus'][:600]}")

    if wochenplan:
        if wochenplan.get("fokus_der_woche"):
            kontext_parts.append(f"Wochenfokus: {wochenplan['fokus_der_woche'][:400]}")
        if wochenplan.get("sales_pattern"):
            kontext_parts.append(f"Sales-Pattern: {wochenplan['sales_pattern'][:400]}")

    kontext = "\n".join(kontext_parts) or "Solopreneur, Mama-Business, Online-Kurse"

    prompt = f"""Patricia ist Mama-Solopreneurin (Mum Life Balance). Sie braucht
einen wöchentlichen News-Bericht passend zu ihrem aktuellen Business-Fokus.

AKTUELLER BUSINESS-KONTEXT:
{kontext}

PATRICIA'S ZIELGRUPPE: erschöpfte Mamas, Network-Mamas, Mum-Solopreneurinnen,
die ein eigenes Online-Business aufbauen wollen.

Generiere 6 KONKRETE Web-Search-Queries die diese Woche besonders relevante
News liefern. Themen-Mix:
- 1-2 Queries zum aktuellen Wochen/Monats-Hauptprodukt
- 1 Query Solopreneur/Mama-Business-Trends
- 1 Query Zeitmanagement/Productivity oder Organisation
- 1 Query KI für Solopreneure/Mamas
- 1 Query Instagram-Marketing aktuell

Wichtig:
- Queries auf Englisch (mehr Quellen)
- Einbau von „2026" oder „this week" für Aktualität
- Konkret + spezifisch (nicht generic)

Output als JSON-Array mit 6 Objekten:
[
  {{"thema": "🚀 Solopreneur-Building", "query": "indie hackers solopreneur 2026 trends"}},
  ...
]

NUR das JSON-Array, kein Drumherum."""

    try:
        client = _get_client()
        response = client.messages.create(
            model=config.CLAUDE_MODEL,
            max_tokens=1200,
            messages=[{"role": "user", "content": prompt}],
        )

        text = ""
        for block in response.content:
            if getattr(block, "type", None) == "text":
                text += getattr(block, "text", "") or ""

        # JSON extrahieren
        import json, re
        text = text.strip()
        if text.startswith("```"):
            text = re.sub(r"^```(?:json)?\s*", "", text)
            text = re.sub(r"\s*```$", "", text).strip()

        data = json.loads(text)
        return {item["thema"]: item["query"] for item in data if "thema" in item and "query" in item}
    except Exception as e:
        logger.warning(f"Topic-Generation fehlgeschlagen: {e} — Fallback auf statische Themen")
        # Fallback
        return {
            "🤖 KI / Claude": "Claude AI Anthropic news this week 2026",
            "📱 Instagram": "Instagram algorithm updates 2026",
            "🚀 Solopreneur": "indie hackers solopreneur trends this week 2026",
            "🏠 Mama-Business": "mama business mum founder trends 2026",
            "⏰ Zeitmanagement": "productivity time management solopreneur 2026",
            "🎨 Content-Creator": "content creator trends 2026 instagram reels",
        }


# Statische Fallback-Themen wenn Topic-Generation komplett fehlschlägt
QUERIES_FALLBACK = {
    "🤖 KI / Claude": "Claude AI Anthropic news this week 2026",
    "📱 Instagram": "Instagram algorithm updates 2026",
    "🚀 Solopreneur": "indie hackers solopreneur trends this week 2026",
}


# ========================================
# News-Block für Briefing
# ========================================

def fetch_news_block(
    monatsplan: dict | None = None,
    wochenplan: dict | None = None,
    max_zeichen: int = 5000,
) -> str:
    """Sammelt ausführlichen Wochen-News-Bericht — themenbasiert aus Notion.

    Nutzt generate_query_topics um aus Patricia's aktuellem Monats-/Wochen-Fokus
    passende News-Themen abzuleiten. Pro Thema mehrere News mit Erkenntnis-Bezug.

    Wird Mo 06:30 aufgerufen.
    """
    # Themen dynamisch aus Notion-Kontext generieren
    themen = generate_query_topics(monatsplan, wochenplan)
    if not themen:
        themen = QUERIES_FALLBACK
    logger.info(f"News-Themen: {list(themen.keys())}")

    parts = []
    parts.append("# 📰 Wochen-News-Bericht")
    parts.append("")
    parts.append(f"_Themen abgeleitet aus deinem aktuellen Monats-Fokus + Wochenfokus._")
    parts.append("")

    for thema, query in themen.items():
        logger.info(f"  Suche: {thema}")
        result = _search_via_claude_extended(query)
        if not result:
            continue

        parts.append(f"## {thema}")
        parts.append("")
        parts.append(result)
        parts.append("")
        parts.append("---")
        parts.append("")

    block = "\n".join(parts)

    if len(block) > max_zeichen:
        block = block[:max_zeichen] + "\n\n... (gekürzt)"

    return block


def _search_via_claude_extended(query: str) -> str:
    """Wie _search_via_claude, aber liefert ausführlichere News pro Thema.

    3 News, je 4-6 Sätze Beschreibung, klickbarer Link, Erkenntnis-Bezug."""
    try:
        client = _get_client()
        response = client.messages.create(
            model=config.CLAUDE_MODEL,
            max_tokens=2000,
            tools=[{"type": "web_search_20250305", "name": "web_search", "max_uses": 3}],
            messages=[{
                "role": "user",
                "content": f"""Suche aktuelle News (letzte 7-14 Tage) zum Thema: {query}

Patricia ist Mama-Solopreneurin (Mum Life Balance) — sie baut Online-Kurse
für Network-Mamas auf, hat doTERRA-Standbein, will 40k CHF/Jahr erreichen.

Gib mir die TOP 3 wichtigsten Ergebnisse zurück. Pro News-Item:

**[Headline der News]**
[4-6 Sätze ausführliche Beschreibung — was passiert ist, warum es relevant
ist, welcher Trend dahinter steckt. Konkret, nicht generisch.]

🔗 Quelle: [vollständige URL]

💡 **Erkenntnis für Patricia:**
- [Konkrete Anwendung 1: Story-Hook / Karussell-Idee / Sales-Argument]
- [Konkrete Anwendung 2]

---

Format-Regeln:
- ALLE 3 News-Items im gleichen Format
- KEINE allgemeine Einleitung („Hier sind die News...")
- URLs IMMER vollständig (für klickbare Links)
- Erkenntnisse wirklich konkret + business-relevant für Patricia
- Auf DEUTSCH (Headlines können englisch bleiben falls Quelle englisch)
"""
            }],
        )

        text_parts = []
        for block in response.content:
            block_type = getattr(block, "type", None)
            if block_type == "text":
                text = getattr(block, "text", None)
                if text:
                    text_parts.append(text)

        return "\n".join(text_parts).strip()
    except Exception as e:
        logger.warning(f"Extended-Search für '{query}' fehlgeschlagen: {e}")
        return ""


def fetch_news_block_minimal() -> str:
    """Fallback wenn keine News-Quellen erreichbar:
    nur eine Header + Platzhalter."""
    return (
        "🎬 NEWS-BLOCK\n"
        "(News-Aggregator läuft beim nächsten Push)\n"
        "→ /news im Telegram-Chat für aktuelle Suche"
    )


if __name__ == "__main__":
    import sys
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    print("=== News-Fetcher Test ===")
    block = fetch_news_block()
    print(block)
    print()
    print(f"Länge: {len(block)} Zeichen")
