"""Mehrbenutzer-State für PIA.

Jede Teilnehmerin = ein Telegram-User = eine JSON-Datei unter data/users/<user_id>.json.

Profil-Struktur:
{
  "user_id": 12345,
  "name": "Sandra",
  "state": "onboarding" | "ready",
  "onboarding_step": 0,            # Index der nächsten Onboarding-Frage
  "profil": {                       # gesammelte Onboarding-Antworten
      "name": "...", "firma": "...", "thema": "...",
      "zielgruppe": "...", "lebensphase": "...", "stand": "..."
  },
  "outputs": { "bio": "...", "hooks": "...", ... },   # zuletzt generierte Ergebnisse
  "created_at": "...", "updated_at": "..."
}
"""

from __future__ import annotations

import json
import logging
from datetime import datetime
from typing import Any

import config

logger = logging.getLogger(__name__)

config.USERS_DIR.mkdir(parents=True, exist_ok=True)


def _user_file(user_id: int):
    return config.USERS_DIR / f"{user_id}.json"


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def load_user(user_id: int) -> dict[str, Any] | None:
    """Lädt das Profil einer Teilnehmerin (oder None falls neu)."""
    f = _user_file(user_id)
    if not f.exists():
        return None
    try:
        return json.loads(f.read_text(encoding="utf-8"))
    except Exception as e:
        logger.warning(f"Konnte User {user_id} nicht lesen: {e}")
        return None


def save_user(data: dict[str, Any]) -> None:
    data["updated_at"] = _now()
    f = _user_file(data["user_id"])
    f.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def create_user(user_id: int, name: str = "") -> dict[str, Any]:
    """Legt ein frisches Profil an (startet Onboarding bei Schritt 0)."""
    data = {
        "user_id": user_id,
        "name": name,
        "state": "onboarding",
        "onboarding_step": 0,
        "profil": {},
        "outputs": {},
        "created_at": _now(),
        "updated_at": _now(),
    }
    save_user(data)
    return data


def get_or_create(user_id: int, name: str = "") -> dict[str, Any]:
    return load_user(user_id) or create_user(user_id, name)


def reset_user(user_id: int, name: str = "") -> dict[str, Any]:
    """Setzt das Profil zurück (Onboarding von vorne)."""
    return create_user(user_id, name)


def set_answer(user_id: int, key: str, value: str) -> dict[str, Any]:
    data = get_or_create(user_id)
    data.setdefault("profil", {})[key] = value
    save_user(data)
    return data


def advance_onboarding(user_id: int) -> dict[str, Any]:
    data = get_or_create(user_id)
    data["onboarding_step"] = data.get("onboarding_step", 0) + 1
    save_user(data)
    return data


def mark_ready(user_id: int) -> dict[str, Any]:
    data = get_or_create(user_id)
    data["state"] = "ready"
    save_user(data)
    return data


def store_output(user_id: int, key: str, text: str) -> dict[str, Any]:
    data = get_or_create(user_id)
    data.setdefault("outputs", {})[key] = {"text": text, "zeit": _now()}
    save_user(data)
    return data


def all_users() -> list[dict[str, Any]]:
    """Alle Profile (für /admin-Statistik)."""
    out = []
    for f in sorted(config.USERS_DIR.glob("*.json")):
        try:
            out.append(json.loads(f.read_text(encoding="utf-8")))
        except Exception:
            pass
    return out
