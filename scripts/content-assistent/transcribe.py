"""Whisper-Transkription für Patricia-Sprachnotizen.

Patricia kann via Telegram eine Sprachnotiz schicken — der Bot lädt sie runter
und transkribiert sie mit OpenAI Whisper API zu deutschem Text.

Wenn OPENAI_API_KEY leer ist, wird die Funktion als „nicht verfügbar" gemeldet —
der Bot funktioniert dann nur mit Text-Antworten.
"""

from __future__ import annotations

import logging
from pathlib import Path

from openai import OpenAI

import config

logger = logging.getLogger(__name__)


_client: OpenAI | None = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        if not config.OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY fehlt in .env (Sprachnotizen deaktiviert)")
        _client = OpenAI(api_key=config.OPENAI_API_KEY)
    return _client


def is_available() -> bool:
    """Prüft ob Whisper-Transkription möglich ist."""
    return bool(config.OPENAI_API_KEY)


def transkribiere_audio(audio_path: str | Path, sprache: str = "de") -> str:
    """Transkribiert eine Audio-Datei zu Text.

    Args:
        audio_path: Pfad zur Audio-Datei (.ogg, .mp3, .wav, .m4a, etc.)
        sprache: ISO-639-1 Sprachcode (Default „de" für Deutsch)

    Returns:
        Transkribierter Text (gestrippt) oder „" bei Fehler.
    """
    audio_path = Path(audio_path)
    if not audio_path.exists():
        logger.error(f"Audio-Datei nicht gefunden: {audio_path}")
        return ""

    if not is_available():
        logger.warning("Whisper nicht verfügbar (kein OPENAI_API_KEY)")
        return ""

    try:
        client = _get_client()
        with open(audio_path, "rb") as f:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                language=sprache,
                response_format="text",
            )
        # API gibt bei response_format="text" den String direkt zurück
        text = str(transcript).strip()
        logger.info(f"Whisper-Transkription erfolgreich: {len(text)} Zeichen")
        return text
    except Exception as e:
        logger.error(f"Whisper-Fehler bei {audio_path}: {e}")
        return ""


def transkribiere_telegram_voice(file_path: str | Path) -> str:
    """Wrapper für Telegram-Voice-Messages (.ogg/.opus).

    Telegram schickt Voice-Messages als .ogg mit Opus-Codec — Whisper unterstützt
    das nativ (`OpenAI Whisper API supports flac, m4a, mp3, mp4, mpeg, mpga, oga, ogg, wav, webm`).
    """
    return transkribiere_audio(file_path, sprache="de")


# ========================================
# CLI-Tester
# ========================================
if __name__ == "__main__":
    import sys
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    print(f"Whisper verfügbar: {'[OK]' if is_available() else '[NEIN]'}")
    print(f"OPENAI_API_KEY-Länge: {len(config.OPENAI_API_KEY)}")

    if len(sys.argv) > 1:
        audio = sys.argv[1]
        print(f"\nTranskribiere: {audio}")
        text = transkribiere_audio(audio)
        print(f"\n--- Transkript ---\n{text}\n--- Ende ---")
    else:
        print("\nNutzung: python transcribe.py <pfad-zur-audio-datei>")
