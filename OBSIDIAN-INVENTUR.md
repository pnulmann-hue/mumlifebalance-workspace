# 🔍 Was nicht in deinem Vault ist — Stand 2026-05-17

> Diese Notiz zeigt, **was auf GitHub liegt aber NICHT in deinem lokalen `main`** (= nicht in Obsidian sichtbar). Plus: lokale Dateien, die noch nicht auf GitHub gesichert sind.

**Repo:** `pnulmann-hue/mumlifebalance-workspace`

---

## 🚨 Teil 1: GitHub-Branches mit nicht-gemergten Inhalten

Diese 10 Branches haben **Arbeit, die nirgendwo sonst existiert**. Wenn du sie nicht synchronisierst, fehlt das in Obsidian und im Backup.

### A) Produkte (Sehr wichtig — komplette Konzepte)

#### 🥇 `build-product-page-WjrId` — Produkt **Mama-CEO** (49 Commits!)
- **Inhalt:** Komplettes Produkt-Briefing, Marktresearch, Modul-Outline, Validierung, Launch-Kalender, Funnel, 14-Mail-Plan, Webinar-Story-Visual, `/jahresplan`-Skill
- **Pfad:** `outputs/produkte/mama-ceo/`
- **GitHub:** [Branch ansehen](https://github.com/pnulmann-hue/mumlifebalance-workspace/tree/claude/build-product-page-WjrId)
- **Empfehlung:** ⭐ **In main mergen** — das ist dein größtes Produkt-Asset

#### 🥈 `build-product-page-fCpc0` — Produkt **Die Umsetzerinnen** (2 Commits)
- **Inhalt:** Continuity-Mitgliedschaft, Bundle-Konzept, Onboarding, Arbeitsblätter, KI-Assistent "Skalier-Bot", Pre-Launch-DMs, Pilot-Call-Plan
- **Pfad:** `outputs/produkte/die-umsetzerinnen-club/`
- **GitHub:** [Branch ansehen](https://github.com/pnulmann-hue/mumlifebalance-workspace/tree/claude/build-product-page-fCpc0)
- **Empfehlung:** ⭐ **In main mergen** — Premium-Bundle-Säule

### B) Operativ (Mittel wichtig)

#### `instagram-creator-analysis-RbNNt` — **Monatsplan Mai + Cashflow-Tracker + /monatsplan-Skill** (7 Commits)
- **Inhalt:** `/monatsplan` Slash-Command, Cashflow-Tracker-Plan (PayPal+CH-Bank), Content-Kalender 30 Tage, Mid-Month-Snapshot
- **Pfade:** `.claude/commands/monatsplan.md`, `outputs/monatsplaene/`, `scripts/finanzen/`, `context/finanzen/`
- **GitHub:** [Branch ansehen](https://github.com/pnulmann-hue/mumlifebalance-workspace/tree/claude/instagram-creator-analysis-RbNNt)
- **Empfehlung:** ⭐ **In main mergen** — Skill + Finanzen-Infrastruktur

#### `fix-bot-database-access-WR5LV` — **Kochbot-RAG-Backend** (2 Commits)
- **Inhalt:** Supabase-RAG-Backend für `/mealplan`, Anti-Halluzinations-Rules, Ingestion/Query-Scripts (Python)
- **Pfade:** `scripts/kochbot-rag/`, `.claude/commands/mealplan.md` (modifiziert)
- **GitHub:** [Branch ansehen](https://github.com/pnulmann-hue/mumlifebalance-workspace/tree/claude/fix-bot-database-access-WR5LV)
- **Empfehlung:** **Mergen wenn du den RAG-Bot wirklich nutzt** — sonst lassen

#### `prime-number-feature-F9MeL` — **Story-Render-Skript + Wander-Stories** (8 Commits)
- **Inhalt:** Python-Renderer für Story-PNGs (`scripts/story-render/`), Wander-Story-Visual-QA-Regeln, fertige Story-Slides (Wandern beide Profile)
- **Pfade:** `scripts/story-render/`, `outputs/stories/renders/`, `plans/2026-04-26-stories-skill.md`
- **GitHub:** [Branch ansehen](https://github.com/pnulmann-hue/mumlifebalance-workspace/tree/claude/prime-number-feature-F9MeL)
- **Empfehlung:** **Mergen** falls du den Story-Renderer brauchst (du hast inzwischen aber `scripts/karussell-render/`)

### C) Content-Slices (Klein — einzelne Outputs)

#### `add-story-feature-x0TxK` — **Story-Slides KW20** (7 Commits)
- **Inhalt:** Mama-CEO Tag-6 + Webinar-Tag-3 + Tag-5 Story-Slides mit PNGs und Fotos
- **Pfad:** `outputs/stories/2026-05-14-*`, `2026-05-15-*`
- **GitHub:** [Branch ansehen](https://github.com/pnulmann-hue/mumlifebalance-workspace/tree/claude/add-story-feature-x0TxK)
- **Empfehlung:** **Mergen** für vollständiges Story-Archiv

#### `webinar-visual-story-BYOFw` — **Mama-CEO Webinar Story-Sequenz** (3 Commits)
- **Inhalt:** Manus-Prompt für Webinar-Story-Sequenz
- **Pfad:** `outputs/stories/manus-prompt-mama-ceo-webinar.md`
- **GitHub:** [Branch ansehen](https://github.com/pnulmann-hue/mumlifebalance-workspace/tree/claude/webinar-visual-story-BYOFw)
- **Empfehlung:** **Mergen** (gehört zum Mama-CEO-Launch)

#### `build-menu-component-bUy8i` — **Mealplan KW18** (1 Commit)
- **Inhalt:** Wochenplan + Einkaufsliste KW18
- **Pfade:** `outputs/mealplans/2026-KW18-*.md`
- **GitHub:** [Branch ansehen](https://github.com/pnulmann-hue/mumlifebalance-workspace/tree/claude/build-menu-component-bUy8i)
- **Empfehlung:** **Mergen** (Vollständiges Mealplan-Archiv)

#### `instagram-reels-ai-helper-akFtE` — **Reel "KI-Mitarbeiter im Wartezimmer"** (1 Commit)
- **Inhalt:** Reel-Doktor-Briefing V2
- **Pfad:** `outputs/reels/2026-05-11-ki-mitarbeiter-pdf-wartezimmer.md`
- **GitHub:** [Branch ansehen](https://github.com/pnulmann-hue/mumlifebalance-workspace/tree/claude/instagram-reels-ai-helper-akFtE)
- **Empfehlung:** **Mergen** (gehört zur Reel-Sammlung)

#### `update-bio-pillars-e17gz` — **Bio-Update Themen-Achse** (1 Commit)
- **Inhalt:** Bio + Über-mich-Update auf Themen-Achse statt Stadium-Achse
- **Pfade:** `outputs/bio-update-2026-05-13/`, `context/saeulen-mentoring.md`
- **GitHub:** [Branch ansehen](https://github.com/pnulmann-hue/mumlifebalance-workspace/tree/claude/update-bio-pillars-e17gz)
- **Empfehlung:** **Mergen** falls schon umgesetzt — sonst Entscheidung

---

## 🟡 Teil 2: Lokal vorhanden, aber NICHT auf GitHub gesichert

Diese Dateien existieren in deinem lokalen `main` (= in Obsidian sichtbar), wurden aber noch nie commited. Wenn deine Festplatte stirbt, sind sie weg.

### Untracked Ordner / Files

- 🚨 `context/patricia-vollprofil.md` — **Pflicht-Lese-Datei (laut Memory) — nirgends gesichert!**
- 🚨 `context/notion-business-brain.md`
- `.claude/commands/blog.md` — Neuer Skill?
- `.claude/commands/cockpit.md` — Cockpit-Bot-Skill
- `outputs/ads/` — kompletter Ads-Ordner
- `outputs/doterra-strategie/` — kompletter doTERRA-Strategie-Ordner
- `outputs/freitag/2026-05-04-hooks-doterra-monatsfokus.md`
- `outputs/freitag/2026-05-04-hooks-mama-business-monatsfokus.md`
- `Business/` — was ist das? (sollte ich prüfen)

### Niemals nach GitHub
- `.secrets/` — bleibt lokal, korrekt so
- `.claude/worktrees/` — Worktrees, müssen nicht gesichert werden
- `.obsidian/` — Vault-Config, optional

### Modifiziert (= geändert, aber nicht commited)

Diese Dateien wurden seit dem letzten Commit verändert:
- `CLAUDE.md` (Workspace-Anleitung)
- `.claude/commands/freitag-hooks.md`, `funnel.md`, `hormozi.md`, `karussell.md`, `montag.md`, `produkt.md`, `reels.md`, `salespage.md`, `story.md` — **alle Skill-Definitionen!**
- `outputs/freitag/2026-05-15-hooks.md`
- 2 Plans

---

## 🎯 Empfohlene Reihenfolge

**Phase 1 — Lokales sichern (sofort, ~5 Min):**
1. Untracked Files commiten (besonders `patricia-vollprofil.md` + `notion-business-brain.md`)
2. Modifizierte Files commiten (Skill-Updates)
3. Push auf GitHub

**Phase 2 — GitHub-Branches synchronisieren (~15-30 Min):**
1. Erst die ⭐ markierten Branches mergen (Mama-CEO, Umsetzerinnen, Monatsplan)
2. Dann die kleineren Content-Branches
3. Optional die Tool-Branches (Kochbot-RAG, Story-Render) — nur wenn du sie nutzt

**Phase 3 — Aufräumen (~5 Min):**
1. Gemergte Branches lokal und remote löschen
2. Stale Worktrees in `.claude/worktrees/` aufräumen
3. Verifizieren in Obsidian dass alles da ist

---

## ⚠️ Risiken & Konflikte

Mehrere Branches verändern parallel:
- `CLAUDE.md` — wird in 3+ Branches geändert
- `.gitignore` — wird in 4+ Branches geändert
- `context/saeulen-mentoring.md` — wird in 2 Branches geändert

→ **Beim Mergen kann es Konflikte geben.** Ich kann pro Branch einzeln mergen und Konflikte für dich auflösen, damit du selbst nichts entscheiden musst.

---

**Stand:** 2026-05-17 · Erstellt von Claude bei Obsidian-Setup
