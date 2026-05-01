# Story-Render-Bot — Patricia's Daily-Story-Automation

**Zweck:** Generiert Mo-So 06:30 automatisch eine 8-Slide-Instagram-Story-Sequenz und sendet sie an Patricias Telegram. Mix-Stil aus 5 Brand-Designed + 3 Foto-First-Slides. Liest Notion-Wochenplan + Monatsplan, achtet auf DISG-Käufertyp-Rotation, nutzt Patricias Shootingbilder + Stock-Fotos.

**Status:** ✅ End-to-End funktionsfähig. Lokal getestet 2026-05-01: 59s, 8 PNGs, ~$0.18 Tokens.

---

## Module-Übersicht

| File | Funktion |
|---|---|
| `bot.py` | Haupt-Einstiegspunkt — Telegram-Bot + APScheduler |
| `config.py` | Tokens, DB-IDs, Pfade, Profil-Rotation |
| `state.py` | In-Memory + persistente Sessions, Wochenlog, DISG-Tracking |
| `notion_reader.py` | Wochen + Monat + Jahr + Themen + Content-Mgmt aus Notion |
| `transcribe.py` | OpenAI Whisper für Patricia-Sprachnotizen |
| `claude_caller.py` | Anthropic Claude → generiert komplette slides.html |
| `render_caller.py` | Subprocess für `karussell-render/render-stories.js` (Puppeteer) |
| `task_daily_story.py` | Orchestrator: Notion → Claude → Render → Telegram |

---

## Schnellstart (lokal)

```powershell
cd "C:\Users\pnulm\Desktop\Mein Business\scripts\story-render-bot"

# 1. Setup-Check (alle Keys + Notion-Zugang)
python config.py
python notion_reader.py    # zeigt aktuellen Monats- + Wochenplan

# 2. Einmal-Test (generiert sofort eine Story und sendet sie an Telegram)
python task_daily_story.py mentoring
# oder
python task_daily_story.py doterra
# oder per Doppelklick:
test_run.bat mentoring

# 3. Daürbetrieb (Bot läuft, Cron Mo-So 06:30 aktiv)
python bot.py
# oder per Doppelklick:
start_bot.bat
```

**Wichtig:** Lokal-Betrieb braucht offenen PowerShell-Tab (Bot läuft im Vordergrund). Konsole zumachen = Bot stoppt.

---

## Telegram-Commands

| Command | Funktion |
|---|---|
| `/start` | Begrüssung |
| `/status` | Bot-Status, DISG heute, Modell, Whisper-Verfügbarkeit |
| `/run` | Sofort eine Story generieren (Profil aus Wochentag) |
| `/run mentoring` | Nur Mentoring-Story |
| `/run doterra` | Nur doTERRA-Story |
| `/notion` | Notion-Healthcheck (alle 5 DBs) |
| `<Sprachnotiz>` | Whisper transkribiert → in Session als Patricia-Input |
| `<Foto>` | Speichert für Story-Verwendung |
| `<Text>` | Wird als Patricia-Input für nächsten /run gemerkt |

---

## Workflow (was passiert beim Auto-Lauf 06:30)

1. **Profil bestimmen** aus Wochentag-Rotation (`config.TAGES_PROFIL_ROTATION`)
2. **Notion lesen** (gecached 24h):
   - Monatsplan: 3 Monatsziele, Launch-Fokus, Themenplanung-Body
   - Wochenplan: Fokus der Woche, Content-Säule
3. **DISG-Käufertyp** für heute aus `state.empfehle_disg_heute()` (Wochenrotation)
4. **Claude API** mit Pflicht-Lese-Liste (52k Token Input):
   - story-framework.md
   - julia-stories-die-verkaufen.md, julia-insta-stories-anleitung.md, julia-launch-kaeufertypen.md, julia-story-ideen.md
   - brandastic-kaeufertypen.md, nadja-story-prompts.md
   - saeulen-mentoring.md, brand-voice.md, hook-framework.md
   - active-funnels.json, ki-phrasen-blackliste.md
   - Bei doTERRA: kompletter `context/doterra/`-Ordner
5. **Claude liefert** komplette `slides.html` (~2.3k Token Output)
6. **Render-Pipeline** (`render-stories.js` mit Puppeteer): HTML → 8× PNG (1080×1920)
7. **Telegram-Versand** alle 8 PNGs einzeln mit Slide-Nummer
8. **Wochenlog** updaten (DISG getrackt für Rotation-Vermeidung)

**Dauer:** ~60s Ende-zu-Ende. **Kosten:** ~$0.18 pro Lauf (~$5.40/Monat).

---

## Output-Struktur

```
outputs/stories/
├── 2026-05-01-mentoring-pre-sale-sule-3-minikurs/
│   ├── slides.html           ← Claude-Output, direkt rendebar
│   ├── _user_prompt.md       ← Debug: was Claude gesehen hat
│   └── png/
│       ├── 01.png ... 08.png ← Instagram-postbar
├── _state/
│   ├── _active_session.json  ← offene Patricia-Session
└── wochen-log.json           ← DISG-Käufertyp-Tracking
└── wochen-kontext-KW18.json  ← Notion-Cache (24h)
```

---

## Notion-Setup (einmalig)

Die Integration „Claude Code Workspace" muss Zugriff auf folgende DBs haben:
- ✅ Wochenplanung (`2ae7078e-8b7e-81ef-a769-cdb1a6584c70`)
- ✅ Monatsplanung (`2ae7078e-8b7e-8171-a760-c233083c26b6`)
- ✅ Jahresplanung Mum Life Balance (`2ae7078e-8b7e-81d9-b5e1-c6bea76ac287`)
- ✅ Content-Management (`2ae7078e-8b7e-8134-9e36-f8c630a850f2`)
- ✅ Produkte (`2ae7078e-8b7e-81ef-aafa-f03993ef344f`)

Healthcheck: `python notion_reader.py` zeigt alle 5 mit `[OK]`.

---

## Dauerbetrieb-Optionen

### Option 1: Lokal mit Windows-Auto-Start (empfohlen für jetzt)
1. Erstelle eine Verknüpfung von `start_bot.bat`
2. Lege sie in `shell:startup` (Win+R → `shell:startup`)
3. Bot startet bei jedem PC-Start automatisch
4. **Limit:** PC muss 06:30 an sein, sonst kein Auto-Lauf

### Option 2: Windows Aufgabenplanung (Task Scheduler)
- Tägliche Aufgabe „06:25" → startet `start_bot.bat`
- Bot lebt 30 Min, feuert 06:30, läuft weiter bis Ctrl-C oder Reboot
- **Limit:** PC muss 06:25 an sein

### Option 3: Railway-Deploy (24/7 Cloud)
**Komplex** — Patricia hat ~16 GB Photos (Shootingbilder + doTERRA), die der Bot braucht. Railway-Container haben Storage-Limits + Photo-Push wäre langsam.
Lösungswege (für separate Session):
- a) Photos auf S3/R2/Wasabi auslagern, Bot lädt on-demand
- b) Nur Stock-Fotos (69 MB) ins Repo, Shootingbilder via separater Mount
- c) Render-Service auf eigenem VPS (4 GB RAM, Linux + Node + Chromium)

→ siehe `deploy_to_railway.py` als Skelett für (a) wenn Photo-Storage geklärt ist.

---

## Kosten

Bei 1× Story-Lauf pro Tag (Mo-So) mit Mix-Stil:

| Service | Pro Lauf | Pro Monat |
|---|---|---|
| Anthropic Claude | $0.15–0.20 | **$5–6** |
| OpenAI Whisper (1 Sprachnotiz) | $0.006 | **$0.20** |
| Notion API | gratis | **$0** |
| Pexels (kein API-Aufruf, nur Disk) | gratis | **$0** |
| **Hosting (Lokal)** | — | **$0** |
| **Hosting (Railway, Hobby)** | — | $5 |
| **Gesamt (lokal)** | | **~$5–6 / Monat** |

---

## Troubleshooting

**`python config.py` zeigt fehlende Env-Vars**
→ `.env` im Workspace-Root prüfen, alle 5 Keys: `TELEGRAM_CONTENT_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `NOTION_API_KEY`.

**`python notion_reader.py` zeigt `[FEHLER]` für eine DB**
→ Notion → Integrations → „Claude Code Workspace" → Zugriff auf die DB freigeben (3-Punkte-Menü „Add connections").

**Render-Pipeline crasht**
→ Node 18+ installiert? `node --version` checken.
→ Puppeteer-Chromium fehlt? `cd ../karussell-render && npm install`.

**Claude liefert kein gültiges HTML**
→ `_raw_response.txt` im Output-Ordner anschauen.
→ Ggf. Prompt zu lang (Token-Limit). Pflicht-Lese-Liste in `config.py` reduzieren.

**Kein Telegram-Push bei /run**
→ Bot-Token korrekt? `python -c "from telegram import Bot; import config; print(Bot(config.TELEGRAM_BOT_TOKEN).get_me())"`

---

## Nächste Verbesserungen (Backlog)

- [ ] Sprachnotiz-Pre-Empt: Patricia kann abends 21:00 Sprachnotiz senden, Bot generiert direkt für nächsten Morgen
- [ ] Patricia-Foto-Integration: bei Foto-Upload wird das Foto in Slide 2 oder 5 verwendet
- [ ] /freitag-hooks-Skill: Vorwoche-Planung mit 7 Story-Themen pro Tag
- [ ] Wochenplan-Fokus-Auto-Update: bei leerem Wochenplan-Fokus fragt Bot Patricia nach
- [ ] Story-Doctor-Modus: Patricia kritisiert Slide X, Bot regeneriert nur diese eine Slide
- [ ] Railway-Deploy mit S3-Photo-Storage
