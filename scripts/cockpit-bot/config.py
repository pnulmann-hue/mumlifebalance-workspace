"""Cockpit-Bot Konfiguration.

Daily-Operator-Bot für Patricia. Lädt Tokens aus .env und stellt Notion-DB-IDs
+ Pflicht-Lese-Liste bereit.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# .env aus Workspace-Root laden
ROOT = Path(__file__).resolve().parent.parent.parent
load_dotenv(ROOT / ".env", override=True)

# ========================================
# Telegram
# ========================================
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_COCKPIT_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = int(os.getenv("TELEGRAM_CHAT_ID", "0"))

# ========================================
# Anthropic Claude API
# ========================================
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-haiku-4-5-20251001")

# ========================================
# Meta Marketing API (für Ads-Performance im Briefing)
# ========================================
META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN", "")
META_AD_ACCOUNT_ID = os.getenv("META_AD_ACCOUNT_ID", "")
META_CURRENCY = os.getenv("META_CURRENCY", "CHF")

# ========================================
# Notion API + DB-IDs (alle aus Patricia's Online Business Brain)
# ========================================
NOTION_API_KEY = os.getenv("NOTION_API_KEY", "")

NOTION_DB_WOCHENPLANUNG = "2ae7078e-8b7e-81ef-a769-cdb1a6584c70"
NOTION_DB_MONATSPLANUNG = "2ae7078e-8b7e-8171-a760-c233083c26b6"
NOTION_DB_JAHRESPLANUNG = "2ae7078e-8b7e-81d9-b5e1-c6bea76ac287"
NOTION_DB_TAGESPLANER = "2ae7078e-8b7e-8102-a640-c046d70a2ae7"
NOTION_DB_AUFGABEN = "2ae7078e-8b7e-81bd-b07a-deaa99c01b71"
NOTION_DB_ZIELE = "2ae7078e-8b7e-815a-a344-f98a4e3d91b3"
NOTION_DB_PRODUKTE = "2ae7078e-8b7e-81ef-aafa-f03993ef344f"
NOTION_DB_CONTENT_MGMT = "2ae7078e-8b7e-8134-9e36-f8c630a850f2"
NOTION_DB_REICHWEITEN = "2ae7078e-8b7e-81ef-87d3-cd86c9be558b"
NOTION_DB_KENNZAHLEN = "2ae7078e-8b7e-8170-83a9-d760d3e593b3"

# Statische Pages
NOTION_PAGE_WOCHENSTRUKTUR = "3587078e-8b7e-815c-abeb-d1259b8e9794"
NOTION_PAGE_CHEAT_SHEET = "35b7078e-8b7e-81ae-b74c-fc675e2697b7"

# ========================================
# Schedule (Europe/Zurich)
# ========================================
TIMEZONE = "Europe/Zurich"
MORNING_BRIEFING_TIME = {"hour": 6, "minute": 30}
LUNCH_REMINDER_TIME = {"hour": 12, "minute": 0}

# Schedule auf Mo-Fr (Sa+So = AUSZEIT laut Wochenstruktur)
WORKDAYS = [0, 1, 2, 3, 4]  # Mo=0 ... So=6

# ========================================
# Pfade
# ========================================
WORKSPACE_ROOT = ROOT
CONTEXT_DIR = ROOT / "context"

# ========================================
# Pflicht-Lese-Liste für Cockpit-Briefing
# ========================================
PFLICHT_LESE_LISTE = [
    "context/notion-business-brain.md",
    "context/brand-voice.md",
    "context/active-funnels.json",
    "context/patricia-vollprofil.md",
]

# ========================================
# Wochenrhythmus (aus Wochenstruktur 2026)
# ========================================
TAGES_PROFIL_ROTATION = {
    0: "mentoring",   # Mo
    1: "doterra",     # Di
    2: "mentoring",   # Mi
    3: "mentoring",   # Do
    4: "mentoring",   # Fr
    5: "frei",        # Sa
    6: "frei",        # So
}

HAUPTBROCKEN_ROTATION = {
    0: "Wochen-Content-Day (/montag) ODER Blog (1. Mo)",
    1: "doTERRA-Tag (Reaktivierung + Lifestyle)",
    2: "Business-Struktur (Bot/System/Automation)",
    3: "Produktentwicklung (Module / Salespage)",
    4: "Newsletter + Weiterbildung",
    5: "FREI",
    6: "FREI",
}


# ========================================
# Validation
# ========================================
def validate_setup() -> list[str]:
    missing = []
    if not TELEGRAM_BOT_TOKEN:
        missing.append("TELEGRAM_COCKPIT_BOT_TOKEN")
    if not TELEGRAM_CHAT_ID:
        missing.append("TELEGRAM_CHAT_ID")
    if not ANTHROPIC_API_KEY:
        missing.append("ANTHROPIC_API_KEY")
    if not NOTION_API_KEY:
        missing.append("NOTION_API_KEY")
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
    print("[OK] Cockpit-Bot Setup vollstaendig")
    print(f"   Telegram-Token: ...{TELEGRAM_BOT_TOKEN[-8:]}")
    print(f"   Chat-ID: {TELEGRAM_CHAT_ID}")
    print(f"   Claude-Model: {CLAUDE_MODEL}")
    print(f"   Schedule: Mo-Fr 06:30 + 12:00 {TIMEZONE}")
