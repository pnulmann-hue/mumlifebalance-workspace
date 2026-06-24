---
tags: [plan, bot, cockpit, story]
---

# Bauplan: Cockpit + tägliche Story → EIN zuverlässiger Morgen-Push (Variante B)

**Erstellt:** 2026-06-22 · **Status:** geplant (eigene Bau-Session)
**Patricia-Entscheid:** Variante **B** — morgens kommt der **fertige Story-Vorschlag** (gerendert), und wenn sie ein Erlebnis/Foto reingeben will, **antwortet sie → wird neu gerendert.**
**Problem (von Patricia bestätigt):** Technik/Zustellung. Die tägliche Story kommt unzuverlässig.

---

## Diagnose (Ist-Zustand)

Morgens feuern **mehrere Scheduler auf zwei Schienen** um ~06:30:

| Schiene | Läuft drauf | Zuverlässigkeit |
|---|---|---|
| **GitHub Actions (Cron)** | Cockpit-Briefing (`.github/workflows/cockpit-daily.yml` → `scripts/cockpit-bot/run_once.py`) · Story-Reminder-JS (`story-reminder-daily.yml` → `scripts/story-reminder/send-daily-reminder.js`) | 🟢 stabil |
| **Railway (Dauer-Worker)** | Content-/Story-Bot APScheduler (`scripts/content-assistent/bot.py`, `Procfile: worker: python bot.py`) | 🔴 fragil |

**Warum die Story flakt (Railway-Schiene):**
- Worker teilt sich knappes 5-$-Hobby-Budget mit 4 weiteren Bots.
- npm-Install + Puppeteer-Render (HTML→PNG) beim Lauf → RAM/CPU-hungrig, Timeout-/Crash-Risiko.
- **Keine Retry-Logik** bei Telegram- oder Render-Fehler → Push kommt einfach nicht.
- Konkurriert mit dem GitHub-Story-Reminder → mal nichts, mal doppelt.

⚠️ **Vor dem Umbau verifizieren:** real prüfen, welche Scheduler tatsächlich feuern (die „bis zu 3 Pushes"-Annahme stammt aus Code-Lektüre), damit nichts Funktionierendes abgeschaltet wird.

---

## Ziel-Architektur (B)

**Alles auf die stabile Schiene (GitHub Actions) + ein leichter Listener für die Verfeinerung.**

### 1. Morgen-Push — GitHub Action, 06:30 (zuverlässig)
- Neue/erweiterte Action `daily-morning.yml` (ein Job):
  1. liest Notion Wochen-/Monatsplan + `active-funnels.json` + Launch-Engine (`story-plan.json`) — **einmal**, geteilt (statt heute 2× separat).
  2. baut **Tagesbriefing** (wie Cockpit heute) **und** generiert daraus den **Story-Vorschlag** (`slides.html`).
  3. **rendert die PNGs in CI** (Puppeteer — läuft bereits zuverlässig in Freitag-/Montag-Build).
  4. schickt **EINEN** Telegram-Push (Content-Bot-Token): Tagesplan + fertige Story-Slides + Zeile „antworte mit Erlebnis/Foto, dann bau ich's um".
- **Abschalten:** APScheduler-Morgen-Job im Railway-Content-Bot + redundanter `story-reminder-daily.yml`.

### 2. Verfeinerungs-Listener (event-getrieben statt flakiger Polling-Worker)
- Content-Bot von **Railway-Polling → Telegram-Webhook auf Vercel** umziehen (serverless, wie `bio-check-bot`): kein schlafender Worker, kein geteiltes Budget, feuert pro Nachricht.
- Antwort von Patricia (Text/Foto) → Webhook speichert Input → triggert **Re-Render via GitHub `repository_dispatch`** (CI rendert, schickt neue PNGs). Hält Serverless leicht, Rendern bleibt auf der bewährten CI-Schiene.
- **Alternative (einfacher, falls Webhook+Dispatch zu viel):** EINEN dedizierten, gehärteten Railway-Worker NUR als Listener behalten (Scheduling raus, eigenes Budget). Behält etwas Railway-Fragilität.

### 3. Gemeinsames Core-Modul
- Notion-Plan-Read + Profil-/Launch-Logik in **ein** Modul (`daily_core`) faktorisieren, das Morgen-Job und Listener teilen → killt doppelte Notion-Reads + auseinanderlaufende Profil-Logik.

---

## Bau-Schritte (für die Session)

1. **Verifizieren** welche Scheduler real feuern (Live-Bots nicht blind abschalten).
2. `daily_core` bauen (Plan-Read + Story-Draft-Generierung, geteilt).
3. `daily-morning.yml` bauen: Briefing + Story-Render + ein Push. **2–3 Tage parallel** zum Alten laufen lassen + vergleichen.
4. Listener auf Vercel-Webhook + `repository_dispatch`-Render umstellen (oder Railway-Listener härten).
5. Alt-Scheduler abschalten (Railway-Morgen-Job + `story-reminder-daily.yml`), sobald neuer Push bewährt.
6. **Eine Woche beobachten.**

## Offene Knackpunkte / Risiken
- **Foto-in-CI:** Patricias hochgeladenes Foto muss für den CI-Render erreichbar sein (Webhook legt's ab — z.B. Commit ins Repo oder Storage). Trickreichster Teil von B.
- GitHub-Secret für Content-Bot-Token (TELEGRAM_* gibt's schon).
- Puppeteer in CI (Fonts/Brand-CSS mitliefern — wie im Karussell-Render).
- Während Bootcamp-Launch (KW27) **keine** Live-Bot-Umbauten → Bau besser nach Cart-Close (ab ~7.7.).

## Verwandte Notizen
- [[project_cockpit-bot-live]] · [[project_content-bot-launch-engine]] · [[project_bot-architektur-juni-2026]] · [[reference_bot-hosting-map]]
