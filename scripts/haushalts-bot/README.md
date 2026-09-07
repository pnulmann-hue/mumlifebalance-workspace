# 🏠 Haushalts-Bot — Vorabend-Push

Zwilling des Cockpit-Bots, fürs Zuhause. Schickt Patricia **jeden Abend 19:00**
(Europe/Zurich) einen Vorabend-Überblick für den **nächsten Tag** — privat aus der
Notion **🏠 Haushalts-Liste** und geschäftlich aus der **✅ Aufgaben**-DB — über einen
**eigenen** Telegram-Bot (nicht der Cockpit-Bot).

## Warum Vorabend?
Schule (Turnsachen packen) und Termine lassen sich am Abend vorher vorbereiten.
Darum kündigt die Nachricht den *morgigen* Tag an.

## Was drinsteht
- 📌 **Dranbleiben** — überfällige einmalige Termine (z.B. Zahnarzt/Frauenarzt), bleiben oben bis `Erledigt = ja`, gedeckelt auf 5
- 🏠 **Haushalt** — täglich / jeden 2. Tag / wöchentlich
- 👨‍👩‍👧 **Familie / Termine** — datierte Termine (morgen bis +3 Tage), Geburtstage 10–14 Tage vorher (Geschenk) + am Tag (Gratulieren)
- 🎒 **Schule** — Vorabend für morgen, mit Vorname
- 🧒 **Kinder-Ämtli** — die täglichen als eine „Ämtli-Runde"-Zeile, wöchentliche einzeln
- 💼 **Business** — offene Aufgaben mit Datum morgen + die 3 ältesten überfälligen
- 🧘 **Dein Slot** — Me-Time, als Schutz formuliert, nie mit Druck

### Wie der Rhythmus auf Tage verteilt wird
- **Wochentag gesetzt** → erscheint an diesem Tag.
- **Wochentag leer, aber Notiz nennt Tage** (z.B. Krafttraining „Mo / Mi / Fr") → an diesen Tagen.
- **Wochentag leer und Notiz ohne Tage** → die Aufgabe bekommt einen festen, aus ihrem
  Namen abgeleiteten Tag (Mo–Sa, `crc32`-Streuung). So verteilen sich die ~17 wöchentlichen
  Haushaltsaufgaben auf die Woche, statt jeden Montag als ein Block zu erscheinen.
- **monatlich ohne Datum** → fester Tag im Monat (1–28), gleiche Streuung.
- **jeden 2. Tag** → feste gerade/ungerade Tage je Aufgabe.
- **jährlich mit Datum** → als Jahrestag (kommt jedes Jahr wieder), nicht als Einmal-Termin.

Quartals-/Halbjahres-/Saison-Aufgaben kommen NICHT im täglichen Push (kein Dauer-Nagging)
— sie laufen über datierte Termine.

> **Schule wird nie gepinnt.** Ein vergangener Turn-/Schwimm-/Waldtag ist vorbei, auch wenn
> niemand „Erledigt" angehakt hat. (Genau das war bis 7.9.2026 der Bug: jeder abgelaufene
> Schultermin blieb dauerhaft unter „Dranbleiben" stehen und die Nachricht sah jeden Tag
> gleich aus.)

## Dateien
| Datei | Zweck |
|---|---|
| `config.py` | Tokens + DB-ID + Verhalten |
| `notion_reader.py` | Liest Haushalts-Liste + Business-Aufgaben (REST, paginiert) |
| `briefing_builder.py` | Vorabend-Logik → Telegram-Text |
| `pdf_builder.py` | Tageszeitungs-PDF („Mum Life Daily") |
| `run_once.py` | Build + Senden (One-Shot für GitHub Actions) |
| `test_abdeckung.py` | Prüft, ob jede offene Aufgabe im Jahr mindestens einmal auftaucht |

## Deployment (GitHub Actions)
Workflow: `.github/workflows/haushalt-vorabend.yml` — Cron `0 17 * * *` (= 19:00 CEST).
Manueller Test: GitHub → Actions → **Haushalt-Vorabend** → *Run workflow*.

### Benötigte GitHub-Secrets
| Secret | Inhalt |
|---|---|
| `TELEGRAM_HAUSHALT_BOT_TOKEN` | Token des eigenen Haushalts-Bots (via @BotFather) |
| `TELEGRAM_HAUSHALT_CHAT_ID` | Chat-ID (Patricias Chat mit dem Bot) |
| `NOTION_TOKEN` | bestehendes Secret — Integration muss Zugriff auf beide DBs haben |

> **Wichtig:** Die „🏠 Haushalts-Liste" **und** die „✅ Aufgaben"-DB müssen mit der
> Integration hinter `NOTION_TOKEN` geteilt sein (Notion → ••• → Verbindungen).
> Ohne Freigabe der Haushalts-Liste liest der Bot 0 Einträge; ohne Freigabe der
> Aufgaben-DB fehlt einfach der 💼-Block (der Push geht trotzdem raus).

### Chat-ID herausfinden
1. Bei @BotFather neuen Bot anlegen → Token kopieren.
2. Dem neuen Bot in Telegram **eine Nachricht schreiben** (z.B. „hallo").
3. `https://api.telegram.org/bot<TOKEN>/getUpdates` im Browser öffnen → `chat.id` ablesen.

## Abdeckungs-Test — taucht wirklich jede Aufgabe auf?

Der Bot kann eine Aufgabe nur nennen, wenn ihr Rhythmus einen Zeitpunkt ergibt.
`test_abdeckung.py` simuliert 400 Vorabend-Briefings und meldet jede Aufgabe,
die im ganzen Jahr **kein einziges Mal** vorkommt:

```bash
cd scripts/haushalts-bot && python test_abdeckung.py
```

Damit eine Aufgabe auslesbar ist, braucht sie **eines** davon:

| Rhythmus | nötig | sonst |
|---|---|---|
| täglich / jeden 2. Tag | nichts | — |
| wöchentlich | Wochentag-Feld | Notiz mit Tagen („Mo / Mi / Fr"), sonst fester Tag aus dem Namen |
| monatlich | nichts | fester Tag im Monat aus dem Namen |
| alle 3 Monate | nichts | erscheint zum Saisonwechsel (März/Juni/Sept/Dez) |
| saisonal, 2x/3x/Jahr, jährlich | **Saison in der Notiz** („Herbst", „Frühling + Winter", „Dezember", „vor Ostern") | **fällt durch — wird nie genannt** |
| einmalig | Fixes Datum oder „überfällig"/„jetzt" in der Notiz | fällt durch |
| nach Bedarf | — | fällt bewusst durch |

> Saison-Aufgaben ohne Saison-Angabe werden **nicht geraten**. Lieber nichts
> sagen als den falschen Monat behaupten. Der Test zeigt genau diese Fälle.

Ist die Saison-Liste länger als `SAISON_MAX`, wird sie **wöchentlich
durchrotiert** statt abgeschnitten — sonst hängt es an der zufälligen
Reihenfolge in Notion, welche Aufgabe nie drankommt.

## Lokaler Test
```bash
cd scripts/haushalts-bot
pip install -r requirements.txt
cp .env.example .env   # Werte eintragen
python config.py       # Setup-Check
python notion_reader.py  # liest + listet alle Einträge
python run_once.py --dry # baut Briefing, sendet NICHT
python run_once.py       # baut + sendet
```
