"""
Claude API Integration — Redaktions-Modus.
Pro Ressort EIN API-Call: Claude wählt die für die Zielgruppe relevantesten
Meldungen aus und schreibt dazu Schlagzeile + 2-Satz-Einordnung.
"""

import logging
import re

import anthropic

from config_business import (
    ANTHROPIC_API_KEY,
    CLAUDE_MODEL,
    CURATION_PROMPT,
    MAX_PICKS_PER_CATEGORY,
    MAX_VIDEOS_PER_CATEGORY,
    ZIELGRUPPE,
)

logger = logging.getLogger(__name__)

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY, max_retries=5)


def strip_html(text: str) -> str:
    """Einfaches Entfernen von HTML-Tags."""
    return re.sub(r"<[^>]+>", "", text).strip()


def _parse_curation(raw: str) -> list[dict]:
    """Parst die Claude-Antwort in eine Liste von {index, title, text}."""
    if raw.strip().upper().startswith("KEINE"):
        return []

    picks = []
    for block in raw.split("---"):
        block = block.strip()
        if not block:
            continue
        index = title = text = None
        for line in block.splitlines():
            line = line.strip()
            if line.upper().startswith("INDEX:"):
                m = re.search(r"\d+", line)
                index = int(m.group()) if m else None
            elif line.upper().startswith("TITEL:"):
                title = line.split(":", 1)[1].strip()
            elif line.upper().startswith("TEXT:"):
                text = line.split(":", 1)[1].strip()
        if index is not None and title:
            picks.append({"index": index, "title": title, "text": text or ""})
    return picks


def curate_category(category: str, articles: list[dict]) -> list[dict]:
    """
    Wählt aus den Rohartikeln eines Ressorts die relevantesten aus und
    reichert sie mit Schlagzeile + Einordnung an. Gibt die fertigen
    (ausgewählten) Artikel zurück — inkl. Original-Link.
    """
    if not articles:
        return []

    # Roh-Meldungen nummeriert für den Prompt aufbereiten
    article_texts = []
    for i, article in enumerate(articles, 1):
        content = strip_html(article.get("content", ""))[:400]
        if not content:
            content = article["title"]
        tag = " (VIDEO)" if article.get("is_video") else ""
        article_texts.append(
            f"[{i}]{tag} Quelle: {article['source']}\n"
            f"    Titel: {article['title']}\n"
            f"    Anriss: {content}"
        )

    prompt = CURATION_PROMPT.format(
        zielgruppe=ZIELGRUPPE,
        category=category,
        max_picks=MAX_PICKS_PER_CATEGORY,
        max_videos=MAX_VIDEOS_PER_CATEGORY,
        articles="\n\n".join(article_texts),
    )

    try:
        response = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = response.content[0].text.strip()
    except anthropic.APIError:
        logger.exception("Claude API Fehler bei Redaktion von %s", category)
        return []

    picks = _parse_curation(raw)

    # Auswahl auf die echten Artikel mappen (Original-Link + Video-Flag behalten)
    result = []
    for pick in picks[:MAX_PICKS_PER_CATEGORY]:
        idx = pick["index"] - 1
        if 0 <= idx < len(articles):
            src = articles[idx]
            result.append({
                "title": pick["title"],
                "summary": pick["text"],
                "link": src["link"],
                "source": src["source"],
                "is_video": src.get("is_video", False),
            })
    return result


def curate_all(articles_by_category: dict[str, list[dict]]) -> dict[str, list[dict]]:
    """Redigiert alle Ressorts (ein API-Call pro Ressort)."""
    edited = {}
    for category, articles in articles_by_category.items():
        if not articles:
            edited[category] = []
            continue
        logger.info("%s: %d Rohmeldungen -> Redaktion...", category, len(articles))
        picks = curate_category(category, articles)
        logger.info("%s: %d Meldungen ausgewählt", category, len(picks))
        edited[category] = picks
    return edited
