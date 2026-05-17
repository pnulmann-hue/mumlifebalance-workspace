# Mealplan — Cron-Optionen (für später, falls vollautomatisch gewünscht)

**Aktueller Default (kostenlos, läuft):**
Du tippst Freitags `/mealplan` in Claude Code → läuft in 5-10 Min mit allen Skill v3 Regeln. Wochenpläne werden in `outputs/mealplans/` gespeichert (= deine Wissensdatenbank für Anti-Doppelung). Original-Rezept-PDFs aus deinem Google Drive werden via Drive-MCP gefunden (kostenlos). PDF mit klickbaren Links kommt per Telegram.

Falls du irgendwann Vollautomatik willst, hier die zwei Optionen:

---

## Option A — Lokaler Scheduled Task (kostenfrei)

Läuft auf deinem Computer in Claude Code. Vorteil: alle MCPs verfügbar, kostenlos.
Nachteil: Claude Code muss zum Cron-Zeitpunkt offen sein (sonst läuft beim nächsten Öffnen nach).

**Setup (du klickst 1× im UI auf „Bestätigen"):**
1. Sag mir „Setze den Freitags-Cron lokal auf"
2. Ich rufe `mcp__scheduled-tasks__create_scheduled_task` auf
3. Im UI erscheint ein Bestätigungs-Dialog → du klickst „Erlauben"
4. Cron-Expression: `0 8 * * 5` (Fr 08:00 Schweiz)
5. Fertig. Läuft ab nächstem Freitag jedes Mal.

---

## Option B — GitHub Action (Cloud, vollständig)

Läuft in GitHub Actions ohne dass dein PC offen sein muss.

**Voraussetzung:** Google Service Account (Cloud-Setup ~10 Min). Service Account ist kostenlos, aber Google verlangt Kreditkarte für Projekt-Aktivierung (auch wenn nie was abgebucht wird — Free-Tier deckt 99% ab).

Wenn du dich dazu durchringst, sag „GH Action Mealplan aufsetzen" — ich baue Workflow + Drive-CLI neu.

---

**Empfehlung kurzfristig:** Manuell `/mealplan` jeden Freitag tippen. Falls genervt von der manuellen Eingabe → Option A in 1 Klick.
