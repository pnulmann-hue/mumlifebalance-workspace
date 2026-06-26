"""Lädt Patricias Voice-/Hook-Wissen für PIAs System-Prompt.

NUR Stil-/Hook-/Reichweiten-Wissen — KEIN patricia-vollprofil.md (intern + privat).
Wird einmal beim Start gecacht.
"""

from __future__ import annotations

import logging

import config

logger = logging.getLogger(__name__)

_cache: str | None = None


def _read(rel_path: str, max_chars: int = 7000) -> str:
    full = config.WORKSPACE_ROOT / rel_path
    if not full.exists():
        logger.info(f"Wissens-Datei fehlt (übersprungen): {rel_path}")
        return ""
    try:
        txt = full.read_text(encoding="utf-8")
        if len(txt) > max_chars:
            txt = txt[:max_chars] + "\n…(gekürzt)…"
        return txt
    except Exception as e:
        logger.warning(f"Konnte {rel_path} nicht lesen: {e}")
        return ""


def lade_wissen() -> str:
    """Baut den Wissens-Block aus den KNOWLEDGE_FILES (gecacht)."""
    global _cache
    if _cache is not None:
        return _cache
    teile = []
    for f in config.KNOWLEDGE_FILES:
        content = _read(f)
        if content:
            teile.append(f"\n## QUELLE: {f}\n{content}\n")
    _cache = "".join(teile)
    logger.info(f"Wissen geladen: {len(_cache)} Zeichen aus {len(config.KNOWLEDGE_FILES)} Dateien")
    return _cache
