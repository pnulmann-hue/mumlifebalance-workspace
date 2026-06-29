# 🏠 Haushalts-Bot — Vorabend-Push

Zwilling des Cockpit-Bots, fürs Zuhause. Schickt Patricia **jeden Abend 19:00**
(Europe/Zurich) einen Vorabend-Überblick für den **nächsten Tag** aus der Notion
**🏠 Haushalts-Liste** — über einen **eigenen** Telegram-Bot (nicht der Cockpit-Bot).

## Warum Vorabend?
Schule (Turnsachen packen) und Termine lassen sich am Abend vorher vorbereiten.
Darum kündigt die Nachricht den *morgigen* Tag an.

## Was drinsteht
- 📌 **Dranbleiben** — überfällige einmalige Termine (z.B. Zahnarzt/Frauenarzt), bleiben oben bis `Erledigt = ja`
- 🏠 **Haushalt** — täglich / jeden 2. Tag / wöchentlich (Wochentag = morgen); Wochen-Tasks ohne festen Tag 1× zum Wochenstart (Mo)
- 👨‍👩‍👧 **Familie / Termine** — datierte Termine (morgen bis +3 Tage), Geburtstage 10–14 Tage vorher (Geschenk) + am Tag (Gratulieren)
- 🎒 **Schule** — Vorabend für morgen, mit Vorname
- 🧒 **Kinder-Ämtli** — „erinnere die Kinder …"
- 🧘 **Dein Slot** — Me-Time, als Schutz formuliert, nie mit Druck

Wochentage werden auch aus der **Notiz** gelesen (z.B. Krafttraining „Mo / Mi / Fr"),
wenn das Wochentag-Feld leer ist. Quartals-/Halbjahres-/Saison-Aufgaben kommen
NICHT im täglichen Push (kein Dauer-Nagging) — sie laufen über datierte Termine.

## Dateien
| Datei | Zweck |
|---|---|
| `config.py` | Tokens + DB-ID + Verhalten |
| `notion_reader.py` | Liest die Haushalts-Liste (REST, paginiert) |
| `briefing_builder.py` | Vorabend-Logik → Telegram-Text |
| `run_once.py` | Build + Senden (One-Shot für GitHub Actions) |

## Deployment (GitHub Actions)
Workflow: `.github/workflows/haushalt-vorabend.yml` — Cron `0 17 * * *` (= 19:00 CEST).
Manueller Test: GitHub → Actions → **Haushalt-Vorabend** → *Run workflow*.

### Benötigte GitHub-Secrets
| Secret | Inhalt |
|---|---|
| `TELEGRAM_HAUSHALT_BOT_TOKEN` | Token des eigenen Haushalts-Bots (via @BotFather) |
| `TELEGRAM_HAUSHALT_CHAT_ID` | Chat-ID (Patricias Chat mit dem Bot) |
| `NOTION_TOKEN` | bestehendes Secret — Integration muss Zugriff auf die Haushalts-Liste haben |

> **Wichtig:** Die „🏠 Haushalts-Liste" muss mit der Integration hinter `NOTION_TOKEN`
> geteilt sein (Notion → ••• → Verbindungen). Sonst liest der Bot 0 Einträge.

### Chat-ID herausfinden
1. Bei @BotFather neuen Bot anlegen → Token kopieren.
2. Dem neuen Bot in Telegram **eine Nachricht schreiben** (z.B. „hallo").
3. `https://api.telegram.org/bot<TOKEN>/getUpdates` im Browser öffnen → `chat.id` ablesen.

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
