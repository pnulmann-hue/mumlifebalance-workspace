"""
doTERRA Bot Health Check
Prueft ob der Bot erreichbar ist und sendet bei Problemen eine Telegram-Nachricht.
"""
import os
import sys
import requests
from datetime import datetime
from pathlib import Path

# Konfiguration
BOT_URL = "https://doterra-bot.vercel.app"
CHAT_ENDPOINT = f"{BOT_URL}/chat"
TIMEOUT = 15

# Telegram-Credentials aus der .env-Datei des News-Bots lesen
env_file = Path(__file__).parent.parent / "telegram-news-bot" / ".env"
telegram_token = None
telegram_chat_id = None
if env_file.exists():
    for line in env_file.read_text(encoding="utf-8").splitlines():
        if line.startswith("TELEGRAM_BOT_TOKEN="):
            telegram_token = line.split("=", 1)[1].strip()
        elif line.startswith("TELEGRAM_CHAT_ID="):
            telegram_chat_id = line.split("=", 1)[1].strip()


def send_telegram_alert(message: str) -> None:
    """Sendet eine Alarm-Nachricht an Telegram."""
    if not telegram_token or not telegram_chat_id:
        print("[FEHLER] Telegram-Credentials nicht gefunden")
        return
    url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
    try:
        response = requests.post(
            url,
            json={
                "chat_id": telegram_chat_id,
                "text": message,
                "parse_mode": "HTML",
            },
            timeout=10,
        )
        response.raise_for_status()
        print(f"[OK] Alarm gesendet: {message[:60]}...")
    except Exception as e:
        print(f"[FEHLER] Telegram-Alarm fehlgeschlagen: {e}")


def check_bot() -> tuple[bool, str]:
    """Prueft ob der Bot erreichbar ist. Gibt (erfolg, fehlermeldung) zurueck."""
    try:
        response = requests.get(CHAT_ENDPOINT, timeout=TIMEOUT, allow_redirects=True)
        if response.status_code in (200, 307, 302):
            return True, ""
        return False, f"HTTP {response.status_code}"
    except requests.exceptions.Timeout:
        return False, "Timeout (>15s)"
    except requests.exceptions.ConnectionError:
        return False, "Verbindungsfehler"
    except Exception as e:
        return False, f"Fehler: {str(e)[:100]}"


def main() -> int:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    success, error = check_bot()

    if success:
        print(f"[{timestamp}] [OK] doTERRA Bot ist erreichbar")
        return 0

    # Bei Fehler: Telegram-Alarm senden
    message = (
        f"[ALARM] <b>doTERRA Bot ist offline!</b>\n\n"
        f"URL: {BOT_URL}\n"
        f"Fehler: {error}\n"
        f"Zeit: {timestamp}\n\n"
        f"Bitte Vercel-Dashboard pruefen."
    )
    print(f"[{timestamp}] [FEHLER] Bot nicht erreichbar: {error}")
    send_telegram_alert(message)
    return 1


if __name__ == "__main__":
    sys.exit(main())
