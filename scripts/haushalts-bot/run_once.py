"""Haushalts-Bot — One-Shot-Runner fuer GitHub Actions.

Liest die Haushalts-Liste, baut das Vorabend-Briefing fuer morgen und
schickt es via Telegram. Wird vom Workflow haushalt-vorabend.yml taeglich
um 19:00 (Europe/Zurich) aufgerufen.

Usage:
    python run_once.py          # baut + sendet
    python run_once.py --dry    # baut + druckt, sendet NICHT (Test)
"""

from __future__ import annotations

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

import requests

import config
import notion_reader
import briefing_builder


def sende_telegram(text: str) -> None:
    url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"
    resp = requests.post(
        url,
        json={
            "chat_id": config.TELEGRAM_CHAT_ID,
            "text": text,
            "disable_web_page_preview": True,
        },
        timeout=30,
    )
    if not resp.ok:
        raise RuntimeError(f"Telegram-Fehler {resp.status_code}: {resp.text}")


def main() -> None:
    dry = "--dry" in sys.argv

    missing = config.validate_setup()
    if missing and not dry:
        print("[FEHLT] Setup unvollstaendig:", ", ".join(missing), file=sys.stderr)
        sys.exit(1)

    eintraege = notion_reader.lade_haushalt_eintraege()
    print(f"[OK] {len(eintraege)} Eintraege aus Haushalts-Liste gelesen")

    text = briefing_builder.baue_vorabend_briefing(eintraege)

    if dry:
        print("\n----- DRY RUN (nicht gesendet) -----\n")
        print(text)
        return

    sende_telegram(text)
    print("[OK] Vorabend-Briefing gesendet")


if __name__ == "__main__":
    main()
