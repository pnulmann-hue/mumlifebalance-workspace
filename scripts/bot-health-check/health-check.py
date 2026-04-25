"""
Bot Health Check (Multi-Bot)
Prueft alle konfigurierten Bots und sendet bei Problemen Telegram-Alarme.

Erweitern: Neuen Bot in BOTS-Liste eintragen (Name, URL, Erfolgs-Statuscodes,
optional JSON-Body-Erwartung fuer strikte Health-Endpoints).
"""
import sys
import requests
from datetime import datetime
from pathlib import Path

# Konfiguration: Liste der zu pruefenden Bots
BOTS = [
    {
        "name": "doTERRA Bot",
        "url": "https://doterra-bot.vercel.app/chat",
        "expect_status": [200, 307, 302],
        "expect_json": None,
    },
    {
        "name": "Bio-Check Bot",
        "url": "https://bio-check-bot.vercel.app/api/health",
        "expect_status": [200],
        # Strenger Check: Health-Endpoint MUSS status="ok" liefern
        # (sonst fehlt eine ENV-Var oder system-prompt.md ist nicht ladbar)
        "expect_json": {"status": "ok"},
    },
]
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


def check_bot(bot: dict) -> tuple[bool, str]:
    """Prueft einen Bot. Gibt (erfolg, fehlermeldung) zurueck."""
    try:
        response = requests.get(bot["url"], timeout=TIMEOUT, allow_redirects=True)
        if response.status_code not in bot["expect_status"]:
            return False, f"HTTP {response.status_code}"
        if bot.get("expect_json"):
            try:
                data = response.json()
                for key, expected in bot["expect_json"].items():
                    if data.get(key) != expected:
                        return False, f"JSON {key}={data.get(key)!r} (erwartet {expected!r})"
            except ValueError:
                return False, "Antwort ist kein JSON"
        return True, ""
    except requests.exceptions.Timeout:
        return False, "Timeout (>15s)"
    except requests.exceptions.ConnectionError:
        return False, "Verbindungsfehler"
    except Exception as e:
        return False, f"Fehler: {str(e)[:100]}"


def main() -> int:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    failures = []

    for bot in BOTS:
        success, error = check_bot(bot)
        if success:
            print(f"[{timestamp}] [OK] {bot['name']} erreichbar")
        else:
            print(f"[{timestamp}] [FEHLER] {bot['name']}: {error}")
            failures.append((bot, error))

    if not failures:
        return 0

    for bot, error in failures:
        message = (
            f"[ALARM] <b>{bot['name']} ist offline!</b>\n\n"
            f"URL: {bot['url']}\n"
            f"Fehler: {error}\n"
            f"Zeit: {timestamp}\n\n"
            f"Bitte Vercel-Dashboard pruefen."
        )
        send_telegram_alert(message)
    return 1


if __name__ == "__main__":
    sys.exit(main())
