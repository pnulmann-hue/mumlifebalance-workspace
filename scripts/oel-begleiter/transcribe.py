"""Whisper-Transkription für den Öl-Begleiter — Sprachnotizen der Testerinnen → Text.

Optional: wenn OPENAI_API_KEY fehlt, meldet is_available() False und der Bot bittet
um Text-Antworten.
"""

from __future__ import annotations

import logging
from pathlib import Path

import config

logger = logging.getLogger(__name__)

_client = None


def _get_client():
    global _client
    if _client is None:
        from openai import OpenAI
        if not config.OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY fehlt")
        _client = OpenAI(api_key=config.OPENAI_API_KEY)
    return _client


def is_available() -> bool:
    return bool(config.OPENAI_API_KEY)


def transkribiere_telegram_voice(file_path: str | Path) -> str:
    """Transkribiert eine Telegram-Voice (.ogg/Opus) zu deutschem Text."""
    file_path = Path(file_path)
    if not file_path.exists() or not is_available():
        return ""
    try:
        client = _get_client()
        with open(file_path, "rb") as f:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                language="de",
                response_format="text",
            )
        return str(transcript).strip()
    except Exception as e:
        logger.error(f"Whisper-Fehler: {e}")
        return ""
