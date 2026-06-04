"""
Kleiner „schon gesendet"-Speicher, damit Artikel/Videos nicht an mehreren
Tagen hintereinander wiederkehren (relevant bei längeren Zeitfenstern).

Best-Effort: lebt als JSON-Datei neben dem Skript. Auf Railway überlebt sie
solange der Container läuft; nach einem Redeploy kann es einmalig zu
Wiederholungen kommen. Das ist bewusst simpel gehalten.
"""

import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

_STORE_PATH = Path(__file__).resolve().parent / "seen_links.json"
_MAX_KEEP = 600  # so viele zuletzt gesendete Links merken


def load_seen() -> set[str]:
    """Lädt die Menge bereits gesendeter Links."""
    try:
        data = json.loads(_STORE_PATH.read_text(encoding="utf-8"))
        return set(data.get("links", []))
    except (FileNotFoundError, json.JSONDecodeError):
        return set()
    except Exception:
        logger.exception("Konnte seen_links.json nicht lesen")
        return set()


def add_seen(new_links: list[str]) -> None:
    """Fügt frisch gesendete Links hinzu (mit Obergrenze)."""
    if not new_links:
        return
    existing = []
    try:
        data = json.loads(_STORE_PATH.read_text(encoding="utf-8"))
        existing = data.get("links", [])
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    except Exception:
        logger.exception("Konnte seen_links.json nicht lesen")

    # Neue ans Ende, Duplikate raus, auf _MAX_KEEP begrenzen (neueste behalten)
    combined = existing + [l for l in new_links if l not in existing]
    combined = combined[-_MAX_KEEP:]
    try:
        _STORE_PATH.write_text(json.dumps({"links": combined}), encoding="utf-8")
    except Exception:
        logger.exception("Konnte seen_links.json nicht schreiben")
