"""
Claude API Integration für Artikel-Zusammenfassungen.
Batch-Modus: Alle Artikel in einem API-Call zusammenfassen (spart ~95% Kosten).
"""

import logging
import re
import time

import anthropic

from config import ANTHROPIC_API_KEY, CLAUDE_MODEL, SUMMARY_PROMPT_BATCH

logger = logging.getLogger(__name__)

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY, max_retries=5)


def strip_html(text: str) -> str:
    """Einfaches Entfernen von HTML-Tags."""
    return re.sub(r"<[^>]+>", "", text).strip()


def summarize_batch(articles: list[dict]) -> list[str]:
    """Fasst eine Liste von Artikeln in einem einzigen API-Call zusammen."""
    # Artikel-Texte für den Prompt vorbereiten
    article_texts = []
    for i, article in enumerate(articles, 1):
        content = strip_html(article.get("content", ""))[:500]
        if not content:
            content = article["title"]
        article_texts.append(f"[{i}] Titel: {article['title']}\nInhalt: {content}")

    prompt = SUMMARY_PROMPT_BATCH.format(articles="\n\n".join(article_texts))

    try:
        response = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = response.content[0].text.strip()
        # Antwort in einzelne Zusammenfassungen aufteilen
        summaries = []
        for block in raw.split("---"):
            block = block.strip()
            if not block:
                continue
            # [1], [2] etc. am Anfang entfernen
            block = re.sub(r"^\[\d+\]\s*", "", block)
            summaries.append(block)
        return summaries

    except anthropic.APIError:
        logger.exception("Claude API Fehler bei Batch-Zusammenfassung")
        return ["Zusammenfassung nicht verfügbar."] * len(articles)


def summarize_articles(articles_by_category: dict[str, list[dict]]) -> dict[str, list[dict]]:
    """
    Fasst alle Artikel per Batch-API-Call zusammen (ein Call pro Kategorie).
    """
    for category, articles in articles_by_category.items():
        if not articles:
            continue

        logger.info("%s: %d Artikel zusammenfassen (Batch)...", category, len(articles))
        summaries = summarize_batch(articles)

        for i, article in enumerate(articles):
            if i < len(summaries):
                article["summary"] = summaries[i]
            else:
                article["summary"] = "Zusammenfassung nicht verfügbar."

    return articles_by_category
