"""Konfiguration für PIA — Patricias KI-Mentorin fürs Bootcamp.

PIA ist ein MEHRBENUTZER-Telegram-Bot: jede Bootcamp-Teilnehmerin chattet privat
mit PIA, hat ihr eigenes Profil und bekommt ihre eigenen Ergebnisse (Bio, Hooks …).

Anders als Patricias Story-Bot (nur 1 Chat = Patricia) ist PIA für viele Userinnen
gleichzeitig offen — es gibt KEINE Chat-ID-Allowlist.

Setup:
    1. Neuen Telegram-Bot via @BotFather anlegen → Token in .env als PIA_BOT_TOKEN
    2. ANTHROPIC_API_KEY setzen
    3. (Optional) OPENAI_API_KEY für Sprachnotiz-Transkription
    4. python config.py   → Setup-Check
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# .env aus dem pia-bot-Ordner laden (lokales Testing). override=True, damit eine
# leere OS-Env-Variable die .env-Definition nicht blockiert.
BOT_DIR = Path(__file__).resolve().parent
WORKSPACE_ROOT = BOT_DIR.parent.parent  # scripts/pia-bot/.. /.. = workspace-root
load_dotenv(BOT_DIR / ".env", override=True)
load_dotenv(WORKSPACE_ROOT / ".env", override=False)  # Fallback: Workspace-.env

# ========================================
# Telegram (PIA-Bot — eigener Token, NICHT der Story-Bot-Token)
# ========================================
PIA_BOT_TOKEN = os.getenv("PIA_BOT_TOKEN", "")

# Optional: Admin-Chat-ID (Patricia) für Fehler-Pings + /admin-Statistik
ADMIN_CHAT_ID = int(os.getenv("PIA_ADMIN_CHAT_ID", "0") or "0")

# ========================================
# Anthropic Claude API
# ========================================
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
CLAUDE_MODEL = os.getenv("PIA_CLAUDE_MODEL", "claude-opus-4-8")

# ========================================
# OpenAI Whisper (Sprachnotiz-Transkription — optional)
# ========================================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# ========================================
# Pfade
# ========================================
DATA_DIR = BOT_DIR / "data"
USERS_DIR = DATA_DIR / "users"
CONTEXT_DIR = WORKSPACE_ROOT / "context"

# Wissens-Dateien für PIAs System-Prompt.
# WICHTIG: NUR Voice-/Stil-/Hook-Wissen — KEIN patricia-vollprofil.md
# (das ist intern und enthält Privates; PIAs Output geht an Kundinnen).
KNOWLEDGE_FILES = [
    "context/brand-voice.md",
    "context/hook-framework.md",
    "context/ki-phrasen-blackliste.md",
    "context/content-radar-juni-2026.md",
    "context/reichweiten-formel-mama-identity.md",
    "context/network-wissensbasis.md",
]

# ========================================
# Bootcamp-Meta
# ========================================
BOOTCAMP_GRUPPE_LINK = os.getenv("PIA_GRUPPE_LINK", "https://t.me/+HW6lvdlbTBhiOWM0")
BOOTCAMP_START = "Montag, 29. Juni"


def validate_setup() -> list[str]:
    """Prüft ob alle nötigen Env-Vars gesetzt sind. Gibt Liste der fehlenden zurück."""
    missing = []
    if not PIA_BOT_TOKEN:
        missing.append("PIA_BOT_TOKEN")
    if not ANTHROPIC_API_KEY:
        missing.append("ANTHROPIC_API_KEY")
    # OPENAI ist optional (nur für Sprachnotizen) → keine harte Anforderung
    if not WORKSPACE_ROOT.exists():
        missing.append(f"WORKSPACE_ROOT exists ({WORKSPACE_ROOT})")
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
    print("[OK] Setup vollstaendig")
    print(f"   Workspace:    {WORKSPACE_ROOT}")
    print(f"   PIA-Bot:      ...{PIA_BOT_TOKEN[-8:]}")
    print(f"   Claude-Model: {CLAUDE_MODEL}")
    print(f"   Whisper:      {'OK' if OPENAI_API_KEY else 'AUS (nur Text)'}")
    print(f"   Gruppe:       {BOOTCAMP_GRUPPE_LINK}")
