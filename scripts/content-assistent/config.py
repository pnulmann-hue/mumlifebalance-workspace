"""Konfiguration für Patricia's Story-Render-Bot.

Lädt Tokens + IDs aus .env. Wird von bot.py + allen tasks importiert.

Setup:
    1. Lokal: .env mit allen Tokens
    2. Railway: Environment Variables im Service-Setup
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# .env aus Workspace-Root laden (lokales Testing)
# override=True überschreibt eventuell vorhandene OS-Env-Variablen
# (sonst kann ein leerer OS-Env-Wert die .env-Definition blockieren)
ROOT = Path(__file__).resolve().parent.parent.parent  # scripts/content-assistent/.. /.. = workspace-root
load_dotenv(ROOT / ".env", override=True)

# ========================================
# Telegram (Patricias Content-Bot)
# ========================================
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_CONTENT_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = int(os.getenv("TELEGRAM_CHAT_ID", "0"))

# ========================================
# Anthropic Claude API
# ========================================
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-opus-4-8")

# ========================================
# OpenAI Whisper (Sprachnotiz-Transkription)
# ========================================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# ========================================
# Notion API
# ========================================
NOTION_API_KEY = os.getenv("NOTION_API_KEY", "")

# Notion-DB-IDs (Stand 2026-05-01, abgerufen via search-API)
NOTION_DB_WOCHENPLANUNG = "2ae7078e-8b7e-81ef-a769-cdb1a6584c70"
NOTION_DB_MONATSPLANUNG = "2ae7078e-8b7e-8171-a760-c233083c26b6"
NOTION_DB_JAHRESPLANUNG = "2ae7078e-8b7e-81d9-b5e1-c6bea76ac287"
NOTION_DB_CONTENT_MGMT = "2ae7078e-8b7e-8134-9e36-f8c630a850f2"
NOTION_DB_PRODUKTE = "2ae7078e-8b7e-81ef-aafa-f03993ef344f"
NOTION_DB_CONTENT_STRATEGIE = "2ae7078e-8b7e-8146-8f10-ec4786130b13"
NOTION_DB_CONTENT_PLATTFORMEN = "2ae7078e-8b7e-811c-9ba7-fe9503f0ecc2"
# Themenplanung: nicht als eigene DB, wird aus Monatsplanung-Body gelesen
NOTION_DB_THEMENPLANUNG = ""

# ========================================
# Pexels (Stock-Fotos Fallback)
# ========================================
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "")

# ========================================
# Schedule (Europe/Zurich)
# ========================================
TIMEZONE = "Europe/Zurich"
DAILY_STORY_TIME = {"hour": 6, "minute": 30}  # Mo-So 06:30

# ========================================
# Pfade (relativ zum Workspace-Root)
# ========================================
WORKSPACE_ROOT = ROOT
CONTEXT_DIR = ROOT / "context"
SHOOTINGBILDER_DIR = CONTEXT_DIR / "Shootingbilder"
STOCK_FOTOS_DIR = CONTEXT_DIR / "stock-fotos"
OUTPUTS_STORIES_DIR = ROOT / "outputs" / "stories"
MONATSPLAENE_DIR = ROOT / "outputs" / "monatsplaene"

# ========================================
# Launch-Engine (Julia-Trost-Launchkalender + Storyvorlagen)
# ========================================
# Strukturiertes Julia-Wissen: Phasen + Vorlagen-Anleitungen
JULIA_LAUNCH_KALENDER = CONTEXT_DIR / "julia-launch-kalender.json"
JULIA_STORY_VORLAGEN = CONTEXT_DIR / "julia-story-vorlagen.json"
# Materialisierte Tag-für-Tag-Launchpläne (zusätzlich werden outputs/produkte/**/story-plan.json
# automatisch entdeckt; diese Liste hat Vorrang)
LAUNCH_STORY_PLANS = [
    ROOT / "outputs" / "produkte" / "mba-launch" / "story-plan.json",
]
_BOT_DIR = Path(__file__).resolve().parent
_BUNDLE_RENDER = _BOT_DIR / "render"
_WORKSPACE_RENDER = ROOT / "scripts" / "karussell-render"

# Render-Pfade: erst Bundle (Railway), dann Workspace (lokal)
if (_BUNDLE_RENDER / "render-stories.js").exists():
    RENDER_SCRIPT = _BUNDLE_RENDER / "render-stories.js"
    BRAND_CSS = _BUNDLE_RENDER / "brand-stories.css"
elif (_WORKSPACE_RENDER / "render-stories.js").exists():
    RENDER_SCRIPT = _WORKSPACE_RENDER / "render-stories.js"
    BRAND_CSS = _WORKSPACE_RENDER / "brand-stories.css"
else:
    RENDER_SCRIPT = _WORKSPACE_RENDER / "render-stories.js"
    BRAND_CSS = _WORKSPACE_RENDER / "brand-stories.css"

# ========================================
# Profil-Konfiguration
# ========================================
PROFILE_MENTORING = "mentoring"
PROFILE_DOTERRA = "doterra"

# Wochentag → welches Profil ist heute dran (Standard, kann durch Notion überschrieben werden)
TAGES_PROFIL_ROTATION = {
    0: "mentoring",   # Montag
    1: "doterra",     # Dienstag
    2: "mentoring",   # Mittwoch
    3: "doterra",     # Donnerstag
    4: "mentoring",   # Freitag
    5: "doterra",     # Samstag
    6: "beide",       # Sonntag
}

# ========================================
# System-Prompts (werden in claude_caller geladen)
# ========================================
# Pflicht-Pfad-Liste die Claude bei jedem Lauf liest
PFLICHT_LESE_LISTE = [
    "context/story-framework.md",
    "context/julia-stories-die-verkaufen.md",
    "context/julia-insta-stories-anleitung.md",
    "context/julia-launch-kaeufertypen.md",
    "context/julia-story-ideen.md",
    "context/brandastic-kaeufertypen.md",
    "context/nadja-story-prompts.md",
    "context/saeulen-mentoring.md",
    "context/notion-content-planung.md",
    "context/brand-voice.md",
    "context/hook-framework.md",
    "context/ki-phrasen-blackliste.md",
    "context/active-funnels.json",
]

# Bei doTERRA-Profil zusätzlich
PFLICHT_LESE_LISTE_DOTERRA = [
    "context/doterra/patricia-wendepunkt-story.md",
    "context/doterra",  # ganzes Verzeichnis
]


# ========================================
# Validation
# ========================================
def validate_setup() -> list[str]:
    """Prüft ob alle nötigen Env-Vars gesetzt sind. Gibt Liste der fehlenden zurück."""
    missing = []
    if not TELEGRAM_BOT_TOKEN:
        missing.append("TELEGRAM_CONTENT_BOT_TOKEN")
    if not TELEGRAM_CHAT_ID:
        missing.append("TELEGRAM_CHAT_ID")
    if not ANTHROPIC_API_KEY:
        missing.append("ANTHROPIC_API_KEY")
    if not OPENAI_API_KEY:
        missing.append("OPENAI_API_KEY")
    if not NOTION_API_KEY:
        missing.append("NOTION_API_KEY")
    if not WORKSPACE_ROOT.exists():
        missing.append(f"WORKSPACE_ROOT exists ({WORKSPACE_ROOT})")
    if not RENDER_SCRIPT.exists():
        missing.append(f"RENDER_SCRIPT exists ({RENDER_SCRIPT})")
    return missing


if __name__ == "__main__":
    # Windows-Encoding-Fix: stdout auf UTF-8 erzwingen
    import sys

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    # Setup-Check beim direkten Aufruf
    missing = validate_setup()
    if missing:
        print("[FEHLT] Setup unvollstaendig:")
        for m in missing:
            print(f"   - {m}")
        exit(1)
    else:
        print("[OK] Setup vollstaendig")
        print(f"   Workspace: {WORKSPACE_ROOT}")
        print(f"   Telegram-Bot: ...{TELEGRAM_BOT_TOKEN[-8:]}")
        print(f"   Claude-Model: {CLAUDE_MODEL}")
        print(f"   Schedule: Mo-So 06:30 Europe/Zurich")
