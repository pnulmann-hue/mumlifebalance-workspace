"""Haushalts-Bot Konfiguration.

Vorabend-Begleiter fuer Patricia (Zwilling des Cockpit-Bots, fuers Zuhause).
Liest die Notion-DB "🏠 Haushalts-Liste" und schickt jeden Abend 19:00 einen
Vorabend-Ueberblick fuer den naechsten Tag via Telegram.

Eigener Telegram-Bot (NICHT der Cockpit-Bot) — Tokens via GitHub Secrets:
  TELEGRAM_HAUSHALT_BOT_TOKEN, TELEGRAM_HAUSHALT_CHAT_ID, NOTION_TOKEN
"""

import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    ROOT = Path(__file__).resolve().parent.parent.parent
    load_dotenv(ROOT / ".env", override=True)
except Exception:
    ROOT = Path(__file__).resolve().parent.parent.parent

# ========================================
# Telegram (eigener Haushalts-Bot)
# ========================================
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_HAUSHALT_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_HAUSHALT_CHAT_ID", "")

# ========================================
# Notion
# ========================================
# Wiederverwendung des bestehenden NOTION_TOKEN-Secrets (Fallback NOTION_API_KEY).
# WICHTIG: Die Integration hinter diesem Token muss Zugriff auf die
# "🏠 Haushalts-Liste" haben (in Notion -> ••• -> Verbindungen freigeben).
NOTION_API_KEY = os.getenv("NOTION_TOKEN", "") or os.getenv("NOTION_API_KEY", "")

# 🏠 Haushalts-Liste (Database-ID) im Privat-Bereich "🏡 Privat & Familie"
NOTION_DB_HAUSHALT = "745ae127-1f03-4dc0-83d4-a6a8058d99dc"

# ✅ Aufgaben (Business-Brain) — liefert den Business-Teil des Vorabend-Briefings.
# Data-Source: collection://2ae7078e-8b7e-81a2-a070-000b54019c80
NOTION_DB_AUFGABEN = "2ae7078e-8b7e-81bd-b07a-deaa99c01b71"

# ========================================
# Verhalten
# ========================================
TIMEZONE = "Europe/Zurich"

# Lookahead fuer datierte Termine (Tage ab morgen)
TERMIN_LOOKAHEAD_TAGE = 3
# Geburtstage: Geschenk-Erinnerung X-Y Tage vorher
GEBURTSTAG_VORLAUF_MIN = 10
GEBURTSTAG_VORLAUF_MAX = 14

# Wiederkehrende Aufgaben OHNE festen Wochentag werden deterministisch ueber
# diese Tage verteilt, statt alle am Montag als "diese Woche dran" zu landen.
WOCHEN_SLOTS = ["Mo", "Di", "Mi", "Do", "Fr", "Sa"]

# Schutz gegen wucherndes "Dranbleiben": max. so viele Pins pro Nachricht.
PINNED_MAX = 5

# Business: welche Status als offen gelten + wie viele Ueberfaellige gezeigt werden
BUSINESS_STATUS_OFFEN = ["Geplant", "Aktiv", "Wartend", "Termin"]
BUSINESS_UEBERFAELLIG_MAX = 3


def validate_setup() -> list[str]:
    missing = []
    if not TELEGRAM_BOT_TOKEN:
        missing.append("TELEGRAM_HAUSHALT_BOT_TOKEN")
    if not TELEGRAM_CHAT_ID:
        missing.append("TELEGRAM_HAUSHALT_CHAT_ID")
    if not NOTION_API_KEY:
        missing.append("NOTION_TOKEN")
    return missing


if __name__ == "__main__":
    import sys
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    missing = validate_setup()
    if missing:
        print("[FEHLT] Setup unvollstaendig:")
        for m in missing:
            print(f"   - {m}")
        sys.exit(1)
    print("[OK] Haushalts-Bot Setup vollstaendig")
    print(f"   Telegram-Token: ...{TELEGRAM_BOT_TOKEN[-6:]}")
    print(f"   Chat-ID: {TELEGRAM_CHAT_ID}")
    print(f"   Haushalts-DB: {NOTION_DB_HAUSHALT}")
    print(f"   Aufgaben-DB:  {NOTION_DB_AUFGABEN}")
