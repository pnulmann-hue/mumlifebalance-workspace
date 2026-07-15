"""Mehrbenutzer-State für den Öl-Begleiter.

Jede Testerin = ein Telegram-User = eine JSON-Datei unter data/users/<user_id>.json.

Profil-Struktur:
{
  "user_id": 12345,
  "name": "Sandra",
  "state": "onboarding" | "ready",
  "onboarding_step": 0,            # Index der nächsten Onboarding-Frage
  "profil": {                       # gesammelte Onboarding-Antworten
      "name": "...", "samples": "...", "wunsch": "...",
      "alltag": "...", "erfahrung": "..."
  },
  "start_date": "2026-07-15",       # Tag, an dem Tag 1 ausgeliefert wurde
  "delivered_day": 0,               # höchste bereits ausgelieferte Etappe (0..7)
  "last_delivery_date": "2026-07-15",  # Datum der letzten Auslieferung (max 1/Tag)
  "outputs": { "tag1": {...}, ... },   # zuletzt gesendete Etappen-Texte
  "created_at": "...", "updated_at": "..."
}
"""

from __future__ import annotations

import json
import logging
from datetime import date, datetime
from typing import Any

import config

logger = logging.getLogger(__name__)

config.USERS_DIR.mkdir(parents=True, exist_ok=True)

GESAMT_TAGE = 7


def _user_file(user_id: int):
    return config.USERS_DIR / f"{user_id}.json"


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def _today() -> str:
    return date.today().isoformat()


def load_user(user_id: int) -> dict[str, Any] | None:
    """Lädt das Profil einer Testerin (oder None falls neu)."""
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
        "start_date": None,
        "delivered_day": 0,
        "last_delivery_date": None,
        "outputs": {},
        "created_at": _now(),
        "updated_at": _now(),
    }
    save_user(data)
    return data


def get_or_create(user_id: int, name: str = "") -> dict[str, Any]:
    return load_user(user_id) or create_user(user_id, name)


def reset_user(user_id: int, name: str = "") -> dict[str, Any]:
    """Setzt das Profil zurück (Onboarding + Begleitung von vorne)."""
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
    """Onboarding fertig → Begleitung startet heute (Tag 1 folgt sofort)."""
    data = get_or_create(user_id)
    data["state"] = "ready"
    if not data.get("start_date"):
        data["start_date"] = _today()
    save_user(data)
    return data


def store_day(user_id: int, day_num: int, text: str) -> dict[str, Any]:
    """Speichert die ausgelieferte Etappe + rückt den Fortschritt vor."""
    data = get_or_create(user_id)
    data.setdefault("outputs", {})[f"tag{day_num}"] = {"text": text, "zeit": _now()}
    if day_num > data.get("delivered_day", 0):
        data["delivered_day"] = day_num
    data["last_delivery_date"] = _today()
    save_user(data)
    return data


def days_since_start(data: dict[str, Any]) -> int:
    """Wie viele Tage seit start_date vergangen sind (0 = heute gestartet)."""
    sd = data.get("start_date")
    if not sd:
        return 0
    try:
        start = date.fromisoformat(sd)
    except Exception:
        return 0
    return (date.today() - start).days


def faellige_etappe(data: dict[str, Any]) -> int:
    """Höchste Etappe, die nach Kalender heute fällig wäre (1..7)."""
    return min(GESAMT_TAGE, days_since_start(data) + 1)


def naechste_etappe(data: dict[str, Any]) -> int | None:
    """Nächste noch nicht ausgelieferte Etappe (1..7) oder None wenn durch."""
    d = data.get("delivered_day", 0)
    return d + 1 if d < GESAMT_TAGE else None


def schon_heute_geliefert(data: dict[str, Any]) -> bool:
    return data.get("last_delivery_date") == _today()


def store_output(user_id: int, key: str, text: str) -> dict[str, Any]:
    """Freitext-Ergebnis ablegen (z.B. Rückblick)."""
    data = get_or_create(user_id)
    data.setdefault("outputs", {})[key] = {"text": text, "zeit": _now()}
    save_user(data)
    return data


def all_users() -> list[dict[str, Any]]:
    """Alle Profile (für Tages-Push + /admin-Statistik)."""
    out = []
    for f in sorted(config.USERS_DIR.glob("*.json")):
        try:
            out.append(json.loads(f.read_text(encoding="utf-8")))
        except Exception:
            pass
    return out
