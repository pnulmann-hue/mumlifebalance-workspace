# GitHub Actions — Autonome Content-Pipeline

**Live seit 2026-04-28** — Patricia braucht keine Claude-Session mehr offen.

## Was läuft hier

| Workflow | Schedule (UTC) | Schedule (Schweiz Sommer / Winter) | Was passiert |
|---|---|---|---|
| `freitag-hooks.yml` | Fr 06:00 | Fr 08:00 / Fr 07:00 | 20 Hooks + Marktanalyse + Wochenfokus → Telegram |
| `montag-build.yml` | Mo 10:00 | Mo 12:00 / Mo 11:00 | Build 10 Designs + Schedule via Blotato für Mo/Mi/Fr |
| `story-reminder-daily.yml` | Mo-So 04:30 | 06:30 / 05:30 | Daily Telegram-DM mit Profil/Modus/DISG/Produkt + State-File |

> **Hinweis Sommer-/Winterzeit:** GitHub Actions läuft in UTC. Schweiz wechselt zwischen CET (UTC+1) und CEST (UTC+2). Im Winter laufen die Workflows 1 Stunde früher als im Sommer (07:00 / 11:00 statt 08:00 / 12:00). Wenn du das im Winter korrigieren willst: `cron: '0 7 * * 5'` für Fr und `cron: '0 11 * * 1'` für Mo.

> **Cron-Verzögerung:** GitHub Actions Cron-Trigger sind nicht punktgenau — typisch 5-15 Min Verzögerung, in Spitzenzeiten auch mal 30+ Min. Für diese Workflows OK.

## Setup für Patricia (einmalig)

### 1. GitHub Secrets setzen

Auf **github.com/pnulmann-hue/mumlifebalance-workspace** → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**.

Folgende Secrets brauchst du:

| Secret-Name | Wert | Wofür |
|---|---|---|
| `ANTHROPIC_API_KEY` | dein Anthropic API-Key (`sk-ant-...`) | Für Claude Code in den Hooks/Build-Actions |
| `BLOTATO_API_KEY` | aus `.env` deines lokalen Workspace (`BLOTATO_API_KEY`) | Für Auto-Schedule |
| `NOTION_TOKEN` | dein Notion Integration Token (`ntn_...`) | Für Wochenfokus-Lesen |
| `TELEGRAM_BOT_TOKEN` | aus `@mumlifebalance_collector_bot` | Für Hooks-Push (freitag-hooks + montag-build) |
| `TELEGRAM_CHAT_ID` | deine Telegram-Chat-ID (für DMs) | Für Hooks-Push |
| `CANVA_TOKEN` | aus deinem Canva-MCP-Setup (falls separates OAuth) | Für Build (sonst über MCP) |
| `STORY_BOT_TOKEN` | aus `Patricia_content_bot` | Für Daily Story-Reminder |
| `STORY_CHAT_ID` | Patricia's Chat-ID mit Patricia_content_bot | Für Daily Story-Reminder |

### 2. Anthropic API-Key holen

- https://console.anthropic.com/settings/keys
- „Create Key" → kopieren → als `ANTHROPIC_API_KEY` in GitHub Secrets

### 3. Erste Test-Trigger

Beide Workflows haben `workflow_dispatch:` → du kannst sie manuell triggern:

- GitHub → **Actions** → **Freitag-Hooks-Engine** → **Run workflow**
- GitHub → **Actions** → **Montag-Build-und-Schedule** → **Run workflow**

Wenn das einmal grün durchläuft, ist alles korrekt eingerichtet.

### 4. Output-Verifikation

Nach erfolgreichem Run findest du:
- `outputs/freitag/YYYY-MM-DD-hooks.md` — die 20 Hooks
- `outputs/freitag/markt-analyse-KW##.md` — Markt-Befunde
- Telegram-DM mit Hook-Übersicht
- Bei /montag: `outputs/montag/YYYY-MM-DD-build.md` + Blotato-Submission-IDs

## Patricia's Workflow ab sofort

1. **Fr ~08:00:** Telegram-DM mit 20 Hooks landet bei dir
2. **Sa-So:** lesen + reflektieren in Ruhe
3. **Mo bis 11:00:** Pick eintragen — entweder
   - Telegram-Reply mit `Mentoring: M1K, M3K... | doTERRA: D2K, D4R...`
   - **ODER** als Datei `outputs/montag/YYYY-MM-DD-pick.md` direkt im Repo (commit + push)
4. **Mo 12:00:** GitHub Actions baut alles + scheduled via Blotato
5. **Mo 19:30 / Mi 19:30 / Fr 19:30:** Posts gehen automatisch live (durch Blotato)

→ Du brauchst nichts mehr in Canva manuell verschieben oder via Claude-Session triggern.

## Backup-Plan wenn ein Workflow failed

GitHub schickt dir bei failed Runs automatisch eine Mail. Wenn das passiert:

1. Klick auf den failed Run → Log lesen → Fehler identifizieren
2. Häufigste Fehler:
   - **Missing Secret** → in Settings → Secrets nachtragen
   - **Anthropic API rate limit** → 1h warten, manuell re-triggern
   - **Notion-Token expired** → neuen Token generieren
3. Manuell triggern via `workflow_dispatch` sobald gefixt

## Kosten-Check

- **GitHub Actions:** kostenlos für public repos (2000 Min/Monat für private). Diese 2 Workflows brauchen ~30-60 Min/Woche → easy im Free-Tier.
- **Anthropic API:** Kostet pro Run. Schätzung: ~$0.50-2 pro Workflow-Run = ~$8-30/Monat für beide.
- **Blotato:** läuft schon, keine zusätzlichen Kosten.
