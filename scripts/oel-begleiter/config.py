"""Konfiguration für den Öl-Sample-Begleiter.

Der Öl-Begleiter ist ein MEHRBENUTZER-Telegram-Bot: Jede Person, die von Patricia
Öl-Pröbchen (Samples) bekommen hat, chattet privat mit dem Bot und wird 7 Tage lang
durchs Testen begleitet — jeden Morgen eine kleine Etappe.

Anders als Patricias Story-Bot (nur 1 Chat = Patricia) ist der Öl-Begleiter für viele
Testerinnen gleichzeitig offen — es gibt KEINE Chat-ID-Allowlist.

WICHTIG: Eigener BotFather-Bot (NICHT der Story-Bot, NICHT der PIA-Bot).

Setup:
    1. Neuen Telegram-Bot via @BotFather anlegen → Token in .env als OEL_BOT_TOKEN
    2. ANTHROPIC_API_KEY setzen
    3. (Optional) OPENAI_API_KEY für Sprachnotiz-Transkription
    4. python config.py   → Setup-Check
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# .env aus dem oel-begleiter-Ordner laden (lokales Testing). override=True, damit eine
# leere OS-Env-Variable die .env-Definition nicht blockiert.
BOT_DIR = Path(__file__).resolve().parent
WORKSPACE_ROOT = BOT_DIR.parent.parent  # scripts/oel-begleiter/.. /.. = workspace-root
load_dotenv(BOT_DIR / ".env", override=True)
load_dotenv(WORKSPACE_ROOT / ".env", override=False)  # Fallback: Workspace-.env

# ========================================
# Telegram (Öl-Begleiter — eigener Token!)
# ========================================
OEL_BOT_TOKEN = os.getenv("OEL_BOT_TOKEN", "")

# Optional: Admin-Chat-ID (Patricia) für Fehler-Pings + /admin-Statistik
ADMIN_CHAT_ID = int(os.getenv("OEL_ADMIN_CHAT_ID", "0") or "0")

# ========================================
# Anthropic Claude API
# ========================================
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
CLAUDE_MODEL = os.getenv("OEL_CLAUDE_MODEL", "claude-opus-4-8")

# ========================================
# OpenAI Whisper (Sprachnotiz-Transkription — optional)
# ========================================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# ========================================
# Tages-Push
# ========================================
# Uhrzeit (Stunde, lokal Europe/Zurich), zu der die tägliche Etappe rausgeht.
SEND_HOUR = int(os.getenv("OEL_SEND_HOUR", "8") or "8")
TIMEZONE = os.getenv("OEL_TIMEZONE", "Europe/Zurich")

# Wie Testerinnen am Ende Kontakt für die eigene Hausapotheke aufnehmen (Tag 7-Brücke).
# Kann Patricias Instagram-Handle, ein ManyChat-Keyword oder eine simple Anweisung sein.
PATRICIA_KONTAKT = os.getenv(
    "OEL_PATRICIA_KONTAKT",
    "schreib mir hier einfach HAUSAPOTHEKE, dann melde ich mich persönlich bei dir",
)

# ========================================
# Pfade
# ========================================
DATA_DIR = BOT_DIR / "data"
USERS_DIR = DATA_DIR / "users"
CONTEXT_DIR = WORKSPACE_ROOT / "context"

# Wissens-Dateien für den System-Prompt.
# NUR Voice-/Stil-/Compliance-Wissen — KEIN patricia-vollprofil.md
# (das ist intern + privat; der Bot-Output geht an fremde Testerinnen).
KNOWLEDGE_FILES = [
    "context/brand-voice.md",
    "context/ki-phrasen-blackliste.md",
    "context/network-wissensbasis.md",
]


def validate_setup() -> list[str]:
    """Prüft ob alle nötigen Env-Vars gesetzt sind. Gibt Liste der fehlenden zurück."""
    missing = []
    if not OEL_BOT_TOKEN:
        missing.append("OEL_BOT_TOKEN")
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
    print(f"   Oel-Bot:      ...{OEL_BOT_TOKEN[-8:]}")
    print(f"   Claude-Model: {CLAUDE_MODEL}")
    print(f"   Whisper:      {'OK' if OPENAI_API_KEY else 'AUS (nur Text)'}")
    print(f"   Tages-Push:   {SEND_HOUR:02d}:00 {TIMEZONE}")
    print(f"   Kontakt:      {PATRICIA_KONTAKT}")
