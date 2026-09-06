# ActiveCampaign-Report

Zieht die AC-Kennzahlen und legt sie als Markdown in `outputs/activecampaign/` ab.

**Warum als GitHub Action und nicht über den MCP-Connector:** Die Web-Claude-Sandbox blockt
`*.activehosted.com` mit `403 host_not_allowed`, und `.env`-Files überleben keine Session.
Die Action läuft ausserhalb der Sandbox — die Zahlen liegen danach im Repo und jede Session
liest sie einfach, egal ob gerade ein Connector verbindet oder nicht. Gleiches Muster wie
`apify-scrape.yml` und `paypal-monthly.yml`.

## Einrichtung (einmalig)

Zwei Repo-Secrets anlegen unter **Settings → Secrets and variables → Actions → New repository secret**:

| Secret | Wert | Wo du ihn findest |
|---|---|---|
| `AC_API_URL` | `https://<dein-konto>.activehosted.com` (ohne Slash am Ende) | ActiveCampaign → Einstellungen → Entwickler → **URL** |
| `AC_API_KEY` | der lange Schlüssel | ActiveCampaign → Einstellungen → Entwickler → **Key** |

`TELEGRAM_BOT_TOKEN` und `TELEGRAM_CHAT_ID` sind im Repo schon vorhanden und werden für den
Wochen-Push mitgenutzt. Fehlen sie, läuft der Report trotzdem — nur ohne Telegram.

## Wann er läuft

- **Automatisch:** montags 06:00 Schweizer Zeit, inkl. Telegram-Zusammenfassung
- **Manuell:** GitHub → Actions → „ActiveCampaign Report" → *Run workflow*

## Was im Report steht

- **Auf einen Blick:** Kontakte gesamt, neu in 7 und 30 Tagen, Ø neue Kontakte pro Woche,
  Ø Öffnungs- und Klickrate — jeweils mit Delta gegen den letzten Lauf
- **Listen:** Abonnentinnen, Zuwachs 30 Tage, Veränderung seit dem letzten Report
- **Tags:** die eigentliche Intake-Sicht — pro Freebie/Funnel-Einstieg, sortiert nach Zuwachs
- **Kampagnen:** letzte 15 versendete mit Versand, Öffnungs- und Klickrate, Abmeldungen
- **Beobachtungen:** rein regelbasiert aus den eigenen Zahlen — Listen und Tags ohne Zuwachs,
  Kampagnen unter dem eigenen Schnitt. Keine fremden Benchmarks, keine erfundenen Zahlen.

`_snapshot.json` hält den letzten Stand fest, damit der nächste Lauf die Deltas rechnen kann.

## Datenschutz

Der Report enthält **ausschliesslich Aggregate** — keine E-Mail-Adressen, keine Namen, keine
Kontakt-IDs. Das ist Absicht, weil dieses Repo öffentlich ist.

Wenn dir auch die aggregierten Zahlen (Listengrössen, Kampagnen-Betreffzeilen) zu offen sind:
`outputs/activecampaign/` in die `.gitignore` aufnehmen und den Commit-Schritt aus dem Workflow
entfernen — dann kommt der Wochenwert nur noch per Telegram.

## Lokal testen

```bash
AC_API_URL=https://dein-konto.activehosted.com AC_API_KEY=… \
  node scripts/activecampaign-report/fetch-report.mjs
```
