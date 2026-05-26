"""Cockpit-Bot — One-Shot-Runner fuer GitHub Actions.

Wird vom Workflow .github/workflows/cockpit-daily.yml aufgerufen.
Ersetzt den Long-Running APScheduler-Loop aus bot.py.

Usage:
    python run_once.py morgen           # Tagesbriefing (Mo-Fr) / Auszeit-Push (Sa+So)
    python run_once.py mittag           # Mittag-Check (Mo-Fr)
    python run_once.py woche-reminder   # Sonntag-Abend-Reminder
    python run_once.py monat-reminder   # 1. d. Monats Reminder
    python run_once.py quartal-reminder # Quartalswechsel Reminder

Wiederverwendung: Importiert bot.py und ruft dessen async-Funktionen direkt auf.
bot.py loest beim Import den Setup-Check aus -- fehlende Secrets fuehren zu
sofortigem Exit, was in GitHub Actions als rotes X sichtbar wird.
"""

from __future__ import annotations

import asyncio
import sys
from datetime import date


WOCHE_REMINDER = (
    "🌅 Sonntag-Abend.\n\n"
    "Zeit fuer deinen Wochenblick. Tipp '/cockpit woche' in Claude Code "
    "(Desktop oder Mobile App) — ich fuehre dich durch:\n\n"
    "• Rueckblick letzte Woche (Tag-Bewertungen, Erfolge, Flops)\n"
    "• Vorschau neue Woche (Hauptprodukt, 5 Saeulen, Termine)\n"
    "• Performance-Hypothesen fuer naechste Woche\n\n"
    "Plant ca. 30 Min ein."
)

MONAT_REMINDER = (
    "🏔️ Monatswechsel — {datum}\n\n"
    "Zeit fuer Monatsplanung. Tipp '/cockpit monat' in Claude Code:\n\n"
    "• Rueckblick letzter Monat (Umsatz, Reichweiten, Top-Content, "
    "Job-Mix-Compliance)\n"
    "• Neuer Monat: Saeule + 3-Produkte-Trio (Gratis/Mini/Gross) + "
    "3 Monatsziele + Hauptbotschaft\n"
    "• Verknuepfung mit Jahresplanung-Aktivitaeten\n\n"
    "Plant ca. 30-45 Min ein. Das ist der Strategie-Layer der die naechsten "
    "4 Wochen /freitag-hooks und /montag-Build steuert."
)

QUARTAL_REMINDER = (
    "🌅 Quartalswechsel — {datum}\n\n"
    "Zeit fuer Quartalsblick + Long-Term-Check. Tipp '/cockpit quartal' "
    "in Claude Code:\n\n"
    "• Q-Ziele-Status (was erreicht, was nicht)\n"
    "• 40k-Jahresziel-Stand vs. Soll\n"
    "• Naechstes Quartal: Aktivitaeten aus Jahresplanung + neue Q-Ziele + "
    "3 Monats-Trio-Vorschau\n\n"
    "Plant ca. 45-60 Min ein. Strategische Sicht, kommt nur 4x im Jahr — "
    "lohnt sich."
)


async def main():
    if len(sys.argv) < 2:
        print("Usage: python run_once.py <modus>", file=sys.stderr)
        print(
            "Modi: morgen | mittag | woche-reminder | monat-reminder | quartal-reminder",
            file=sys.stderr,
        )
        sys.exit(2)

    modus = sys.argv[1]

    # bot.py-Import loest validate_setup() aus -- fehlende Secrets crashen hier
    import bot  # noqa: E402

    today_str = date.today().strftime("%d.%m.%Y")

    if modus == "morgen":
        await bot.task_morgen_briefing()
    elif modus == "mittag":
        await bot.task_mittag_reminder()
    elif modus == "woche-reminder":
        await bot._send_telegram(WOCHE_REMINDER)
    elif modus == "monat-reminder":
        await bot._send_telegram(MONAT_REMINDER.format(datum=today_str))
    elif modus == "quartal-reminder":
        await bot._send_telegram(QUARTAL_REMINDER.format(datum=today_str))
    else:
        print(f"Unbekannter Modus: {modus}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    asyncio.run(main())
