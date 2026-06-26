# PIA — KI-Mentorin fürs 5-Tage-Bootcamp

PIA ist ein **Mehrbenutzer-Telegram-Bot**. Jede Bootcamp-Teilnehmerin chattet privat mit ihr, durchläuft ein kurzes Onboarding (6 Fragen) und holt sich pro Tag ihre personalisierte Mission ab. Der Wow-Kern: Sie erlebt die Transformation live — PIA baut **ihre** Bio, **ihre** Hooks, **ihren** roten Faden, in **ihrer** Stimme.

Unterschied zum Story-Bot (`scripts/content-assistent/`): Der Story-Bot ist nur für Patricia (1 Chat). PIA ist für viele Userinnen gleichzeitig offen (keine Chat-ID-Allowlist), jede mit eigenem Profil.

## Die 5 Tage (Bootcamp 29.6.–3.7.)

| Tag | Command | PIA generiert |
|---|---|---|
| 1 | `/bio` | Thema auf den Punkt + fertige Instagram-Bio |
| 2 | `/hooks` | 3 Hooks für ihr Thema |
| 3 | `/struktur` | Mini-Wochenstruktur + KI-Impuls |
| 4 | `/leadmagnet` | Leadmagnet-Skelett (Titel + Versprechen + Format) |
| 5 | `/roterfaden` | roter Faden + Brücke zum nächsten Schritt |

Dazu: `/start` (Onboarding), `/profil`, `/neu`, `/hilfe`, `/admin` (nur Patricia). Freier Text/Sprachnotiz → PIA antwortet im Kontext ihres Profils.

## Architektur

```
bot.py          Telegram-Handler (Mehrbenutzer, Onboarding-Flow, Tages-Commands, Voice)
onboarding.py   die 6 Onboarding-Fragen
store.py        Profile pro Userin als JSON (data/users/<user_id>.json)
pia_brain.py    Claude-Generatoren (Bio/Hooks/Struktur/Leadmagnet/roter Faden) + freie Frage
knowledge.py    lädt Patricias Voice-/Hook-Wissen (NICHT das private Vollprofil)
transcribe.py   Whisper-Transkription für Sprachnotizen (optional)
config.py       Env + Pfade
```

**Wissensbasis:** PIA lädt nur Voice-/Stil-/Hook-Dateien (`brand-voice.md`, `hook-framework.md`, `ki-phrasen-blackliste.md`, `content-radar-juni-2026.md`, `reichweiten-formel-mama-identity.md`). Bewusst **kein** `patricia-vollprofil.md` — das ist intern/privat, PIAs Output geht an Kundinnen.

**Eingebaute Regeln:** Freundin-Voice, kein Stakkato, Schweizer ss, keine erfundenen Zahlen, Transformation statt Produkt, Network-Compliance (keine Heilversprechen), Output in der Stimme der Teilnehmerin, keine Mentoren-Namen.

## Setup (lokal testen)

```bash
cd scripts/pia-bot
pip install -r requirements.txt
cp .env.example .env      # dann .env ausfüllen
python config.py          # Setup-Check
python bot.py             # Bot starten (Ctrl-C beendet)
```

### Was in die `.env` muss
1. **`PIA_BOT_TOKEN`** — einen **neuen** Bot bei [@BotFather](https://t.me/BotFather) anlegen (`/newbot` → Name z.B. „PIA – deine KI-Mentorin") → Token kopieren. **Nicht** der Story-Bot-Token.
2. **`ANTHROPIC_API_KEY`** — für die Generierung.
3. `OPENAI_API_KEY` — optional, nur für Sprachnotizen.
4. `PIA_ADMIN_CHAT_ID` — optional, Patricias Chat-ID für `/admin`.

## Deployment (Railway — wie die anderen Bots)

Tokens als Repo-Secrets / Service-Env-Variablen hinterlegen (persistieren zwischen Sessions, anders als die lokale `.env`). `Procfile` startet `worker: python bot.py`.

1. Railway-Service auf den Ordner `scripts/pia-bot/` zeigen lassen
2. Env-Variablen setzen: `PIA_BOT_TOKEN`, `ANTHROPIC_API_KEY`, (optional `OPENAI_API_KEY`, `PIA_ADMIN_CHAT_ID`)
3. Deploy → PIA läuft 24/7

> **Daten-Hinweis:** Profile liegen als JSON unter `data/users/`. Auf Railway ist das ephemer (geht bei Redeploy verloren). Für den 5-Tage-Bootcamp ist das okay (kurzlebig). Für Dauerbetrieb später: Railway-Volume mounten oder auf Supabase umstellen.

## Status (Stand 16.6.2026)

- ✅ Code fertig + getestet (Bio-Generierung live gegen Claude verifiziert)
- ⏳ **Offen:** BotFather-Token anlegen + `.env`/Railway füllen + deployen
- ⏳ Testrunde mit Patricia + 1-2 Pilot-Mamas (Qualitäts-Gate, 24.-26.6.)

Volle Launch-Logik: [[../../outputs/produkte/mba-launch/challenge-launch-plan]]
