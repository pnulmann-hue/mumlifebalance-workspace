"""Haushalts-Bot — One-Shot-Runner fuer GitHub Actions.

Liest Haushalts-Liste, Business-Aufgaben und Content-Plan, baut daraus das
Vorabend-Briefing fuer morgen und schickt es als PDF ("Mum Life Daily") mit
kurzer Telegram-Begleitnachricht. Wird vom Workflow haushalt-vorabend.yml
taeglich um 19:00 (Europe/Zurich) aufgerufen.

Usage:
    python run_once.py            # baut PDF + sendet
    python run_once.py --dry      # baut alles, sendet NICHT (PDF bleibt liegen)
    python run_once.py --text     # sendet nur Text, kein PDF (Fallback)
"""

from __future__ import annotations

import sys
from datetime import date, timedelta

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


def sende_telegram_pdf(pfad: str, caption: str) -> None:
    """Schickt das PDF mit Begleittext (Caption max. 1024 Zeichen)."""
    url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendDocument"
    with open(pfad, "rb") as f:
        resp = requests.post(
            url,
            data={"chat_id": config.TELEGRAM_CHAT_ID, "caption": caption[:1024]},
            files={"document": f},
            timeout=60,
        )
    if not resp.ok:
        raise RuntimeError(f"Telegram-Fehler {resp.status_code}: {resp.text}")


def main() -> None:
    dry = "--dry" in sys.argv
    nur_text = "--text" in sys.argv

    missing = config.validate_setup()
    if missing and not dry:
        print("[FEHLT] Setup unvollstaendig:", ", ".join(missing), file=sys.stderr)
        sys.exit(1)

    eintraege = notion_reader.lade_haushalt_eintraege()
    print(f"[OK] {len(eintraege)} Eintraege aus Haushalts-Liste gelesen")

    business = notion_reader.lade_business_aufgaben()
    print(f"[OK] {len(business)} offene Business-Aufgaben gelesen")

    morgen = (date.today() + timedelta(days=1)).isoformat()
    content = notion_reader.lade_content_plan(morgen, morgen)
    print(f"[OK] {len(content)} Content-Eintraege fuer morgen gelesen")

    struktur = briefing_builder.baue_briefing_struktur(
        eintraege, business=business, content=content
    )
    text = briefing_builder.baue_vorabend_briefing(eintraege, struktur=struktur)
    caption = briefing_builder.baue_kurzfassung(struktur)

    if nur_text:
        if dry:
            print("\n----- DRY RUN (Text, nicht gesendet) -----\n")
            print(text)
            return
        sende_telegram(text)
        print("[OK] Vorabend-Briefing als Text gesendet")
        return

    # PDF bauen — schlaegt das fehl, geht der Push trotzdem als Text raus.
    pdf_pfad = None
    try:
        import pdf_builder
        pdf_pfad = pdf_builder.baue_pdf(struktur)
        print(f"[OK] PDF gebaut: {pdf_pfad}")
    except Exception as e:
        print(f"[WARN] PDF fehlgeschlagen ({e}) — sende Text", file=sys.stderr)

    if dry:
        print("\n----- DRY RUN (nicht gesendet) -----\n")
        print("--- Caption ---")
        print(caption)
        print("\n--- Volltext ---")
        print(text)
        if pdf_pfad:
            print(f"\n--- PDF liegt unter: {pdf_pfad}")
        return

    if pdf_pfad:
        sende_telegram_pdf(pdf_pfad, caption)
        print("[OK] Vorabend-Briefing als PDF gesendet")
    else:
        sende_telegram(text)
        print("[OK] Vorabend-Briefing als Text gesendet (PDF-Fallback)")


if __name__ == "__main__":
    main()
