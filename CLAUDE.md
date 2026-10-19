# CLAUDE.md

Diese Datei gibt Claude Code (claude.ai/code) Anweisungen für die Arbeit in diesem Repository.

---

## Was das hier ist

Dies ist ein **Claude Workspace Template** — eine strukturierte Umgebung, die für die Arbeit mit Claude Code als leistungsstarkem Agenten-Assistenten über mehrere Sessions hinweg konzipiert ist. Der Benutzer startet wiederholt neue Claude Code Sessions und verwendet `/start` zu Beginn jeder Session, um den wesentlichen Kontext ohne Ballast zu laden.

**Diese Datei (CLAUDE.md) ist das Fundament.** Sie wird automatisch am Anfang jeder Session geladen. Halte sie aktuell — sie ist die Single Source of Truth dafür, wie Claude diesen Workspace verstehen und darin arbeiten soll.

---

## Die Claude-User-Beziehung

Claude arbeitet als **Agenten-Assistent** mit Zugriff auf die Workspace-Ordner, Kontext-Dateien, Commands und Outputs. Die Beziehung ist:

- **User**: Definiert Ziele, liefert Kontext zu seiner Rolle/Funktion und steürt die Arbeit über Commands
- **Claude**: Liest Kontext, versteht die Ziele des Users, führt Commands aus, produziert Outputs und pflegt die Workspace-Konsistenz

Claude sollte sich immer über `/start` am Session-Start orientieren, dann mit vollem Bewusstsein dafür handeln, wer der User ist, was er erreichen möchte und wie dieser Workspace das unterstützt.

---

## Workspace-Struktur

```
.
├── CLAUDE.md              # Diese Datei — Kern-Kontext, immer geladen
├── .claude/
│   └── skills/            # Alle Skills — je Skill ein Ordner
│       ├── start/
│       │   ├── SKILL.md      # das Herzstück, das Claude liest
│       │   └── Anleitung.md  # Kundendokument fürs Weitergeben
│       ├── karussell/
│       └── _WEITERGABE-STATUS.md  # intern: welcher Skill darf raus
├── context/               # Hintergrund-Kontext über den User und das Projekt
│                          # (Vom User mit Rolle, Zielen, Strategien befüllen)
├── plans/                 # Implementierungspläne erstellt von /create-plan
├── outputs/               # Arbeitsergebnisse und Deliverables
├── reference/             # Vorlagen, Beispiele, wiederverwendbare Patterns
└── scripts/               # Automatisierungsskripte (falls zutreffend)
```

**Verzeichnisse:**

| Verzeichnis  | Zweck                                                                                   |
| ------------ | --------------------------------------------------------------------------------------- |
| `context/`   | Wer der User ist, seine Rolle, aktuelle Prioritäten, Strategien. Gelesen von `/start`. |
| `plans/`     | Detaillierte Implementierungspläne. Erstellt mit `/create-plan`, umgesetzt mit `/implement`. |
| `outputs/`   | Deliverables, Analysen, Reports und Arbeitsergebnisse.                                 |
| `reference/` | Hilfreiche Dokumentation, Vorlagen und Patterns für verschiedene Workflows.            |
| `scripts/`   | Automatisierungs- und Tooling-Skripte.                                                 |
| `_MOCs/`     | Maps of Content für Obsidian-Vault — thematische Dashboards. **Nicht editieren ohne CLAUDE.md zu prüfen.** |

---

## 🟦 Obsidian-Vault-Konvention (PFLICHT für alle Skills, seit 2026-05-17)

Patricia nutzt den Workspace **als Obsidian-Vault**. Damit der Wissens-Graph sauber bleibt, MUSS jeder Skill der neue MD-Files in `outputs/` (oder anderen vault-relevanten Ordnern) erstellt **zwei Dinge** tun:

### 1. Frontmatter-Tags am Anfang der Datei

Direkt als erste Zeilen, vor dem `# Title`:

```markdown
---
tags: [tag1, tag2, tag3]
---

# Eigentlicher Titel
...
```

**Standard-Tags pro Ordner:**

| Ordner | Tags |
|---|---|
| `outputs/karussells/` | `[content, karussell]` |
| `outputs/reels/` | `[content, reels]` |
| `outputs/stories/**/` | `[content, story]` |
| `outputs/content/` | `[content]` — Ergebnisse von `/content` |
| `outputs/freitag/` | `[content, freitag-hooks]` — Altbestand |
| `outputs/montag/` | `[content, montag-build]` — Altbestand |
| `outputs/mealplans/` | `[mealplan]` |
| `outputs/produkte/**/` | `[produkt]` |
| `outputs/funnels/**/` | `[funnel]` |
| `outputs/salespages/` | `[produkt, salespage]` |
| `outputs/marktrecherche/` | `[research]` |
| `outputs/zielgruppen-research/` | `[research]` |
| `outputs/doterra-strategie/` | `[doterra]` |
| `outputs/ads/` | `[ads]` |
| `outputs/monatsplaene/` | `[monatsplan]` |
| `outputs/content-kalender/` | `[content]` |
| `outputs/instagram-insights/` | `[content, insights]` |
| `outputs/garten/` | `[garten]` |
| `outputs/calls/` | `[call]` |
| `outputs/telegram-posts/` | `[content, telegram]` |
| `outputs/sonstige/` | `[misc]` |
| `outputs/strategie/` | `[strategie]` — gitignored |
| `outputs/bio-update-*/` | `[brand]` |
| `outputs/bio-check-bot/` | `[tools, bot]` |
| `outputs/samples/` | `[content, samples]` |
| `outputs/julia-trost-sync/` | `[externe-wissen, julia-trost]` |
| `outputs/praesentationen/` | `[produkt]` |
| `context/*.md` | situativ — siehe bestehende Files |

Bei Bedarf zusätzliche Tags ergänzen (z.B. `mentoring` / `doterra` für Profil-Unterscheidung, oder Spezial-Themen).

### 2. Eintrag im `_INDEX.md` des Ordners

Jeder vault-relevante Ordner hat ein `_INDEX.md`. Nach dem Erstellen einer neuen Datei den Dateinamen als Wiki-Link **alphabetisch sortiert** in die `## Dateien`-Sektion eintragen:

```markdown
- [[2026-05-17-mein-neuer-output]]
```

### 3. Optional: "Verwandte Notizen"-Block

Bei wichtigen Kern-Files am Ende einen Block mit Wiki-Links zu Nachbar-Files anhängen:

```markdown
---

## 🔗 Verwandte Notizen

- [[andere-relevante-notiz]]
- [[_MOCs/MOC-Thema|Themen-Map]]
```

### Auto-Pflege als Sicherheitsnetz

- **Lokal:** `bash scripts/obsidian-reindex.sh` generiert alle `_INDEX.md` neu und prüft Frontmatter-Tags. Kann jederzeit laufen, ist idempotent.
- **Remote:** `.github/workflows/obsidian-reindex.yml` läuft täglich 23:00 (Cron) als Sicherheitsnetz und committed automatisch falls Files den Tags-/Index-Anforderungen nicht entsprechen.

→ Skills die das hier ignorieren erzeugen Lücken im Graph, die der Auto-Reindex einmal pro Tag schliesst. Trotzdem: **selber sauber arbeiten ist immer besser** als auf den Cron warten.

---

## 🟥 Zwei Zielgruppen-Ebenen — die Kundschaft ihrer Kundinnen ist NICHT weiblich

Patricia hat es „schon hundertmal gesagt“ (zuletzt 25.09.2026, davor 14.08., 10.08.,
08.06.). Die Regel stand nur im Gedächtnis, deshalb griff sie nie dort, wo geschrieben wird.

| Ebene | Wer | Wortwahl |
|---|---|---|
| **Patricias Kundinnen** | Mamas im Network / mit eigenem Business | Kundin, Mama, sie, Frauen — ✓ |
| **Deren Kundschaft** | wer auch immer bei ihnen kauft — Männer, Firmen, Familien | Kundschaft, Leute, Person, Interessenten, Zielgruppe, „für wen du schreibst“ — **nie** Kundin, Frauen, Mamas, kein Kund:innen |

🚨 **Die Falle:** Sobald ein Text Patricias Kundin mit „du“ anspricht, ist „deine Kundin“
fast immer die zweite Ebene und damit falsch. Gilt für Tools, Kursbeilagen, Folien,
Hooks, Salespages, Prompts. Die Regel „Kundinnen statt Kunden“ in den Salespage-Skills
meint **nur** Patricias eigene Kundinnen.
Am 25.09. steckte der Fehler in der eigenen Kursbeilage (Business-Brief „Meine Kundin“,
Quelle `scripts/ki-kurs/beilagen-bauen.py`) und wurde von dort in den Stimm-Check kopiert.
Details: Memory `feedback_KRITISCH-zielgruppen-ebenen.md`.

---

## 🟩 Skill-Standard (PFLICHT für jeden neuen Skill, seit 2026-09-13)

Jeder Skill ist ein **Ordner** unter `.claude/skills/<name>/` mit genau zwei Dateien:

```
<name>/
├── SKILL.md      # Herzstück — das liest Claude
└── Anleitung.md  # Kundendokument — nur fürs Weitergeben
```

**`SKILL.md` beginnt mit Frontmatter** (ohne das wird der Skill nicht gefunden):

```markdown
---
name: <ordnername, exakt gleich>
description: "Ein Satz, woran Claude erkennt, wann dieser Skill dran ist."
---
```

Darunter gehören hinein: Zweck · wo das Business-Wissen liegt · Wunschkundin ·
Schmerzpunkte · Einwände · Stimme · **Regeln** (echte Zahlen, längere Sätze statt
Stakkato, KI-Floskel-Verbot) · gewünschter **Output** (z.B. „5 Texte, 5 Überschriften,
5 Beschreibungen") · ein **Beispiel** · feste **Angles**.

**`Anleitung.md`** gibt die Vogelperspektive plus Installation in drei Schritten:
Ordner kopieren → Claude neu starten → Platzhalter ersetzen. Sie ist ein
**Kundendokument** — also niemals fremde Mentorinnen namentlich, keine privaten
Daten, keine Datenbank-Kennungen. Für den Eigengebrauch reicht die `SKILL.md` allein.

Generator für die Anleitungen: `scripts/skills/anleitungen-generieren.py` — dort je
Skill den Eintrag ergänzen und einmal laufen lassen, statt Anleitungen von Hand zu
schreiben. Welcher Skill weitergegeben werden darf, steht in
`.claude/skills/_WEITERGABE-STATUS.md`.

🚨 **Die 7 zugekauften Skills** (`chatgpt-ads`, `facebook-ads`, `copywriting` und die
4 Salespage-Designs) bekommen **keine** Weitergabe-Anleitung — das wäre
Weiterverteilung fremder Arbeit. Alle sind gitignored (Repo public).

### 🎯 Hooks: ein Prozess für alle Skills (seit 2026-09-13)

**Jeder Skill, der einen Hook schreibt, liest zuerst `.claude/skills/hooks/SKILL.md`.**
Der Verweis ist als Pflicht-Block in **allen 14 eigenen Content-Skills** eingebaut:
`content` · `caption` · `reels` · `karussell` · `story` · `blog` ·
`monatsplan` · `funnel` · `produkt` · `copywriting`.

Der Hook-Skill (rund 1'050 Zeilen, 16 Teile) ist **die eine Stelle** für alles, was mit
der ersten Zeile zu tun hat: Kundensprache und Kern-Painpoint · Bewusstseinsstufen 1–5 ·
Angles · PIE-Mix · 80 Kalender-Formeln mit Beispielen · 27 Hook-Formeln mit Testdaten ·
10 Reveal-Frameworks · 50 Vorlagen in fünf Säulen · Voice-Kniffe · Verbote · Prüfskript.
Die alten `context/hook-*.md` sind nur noch **Herkunft** und tragen oben einen Verweis
hierher; laufend gepflegt werden weiter `hook-formel-testlog.md` (Testergebnisse) und
`ki-phrasen-blackliste.md` (Vollversion).

**🛑 Der letzte Check** am Ende des Skills ist die Abnahme für jeden Hook — **fünf**
Fragen, eine mit Nein und der Hook wird umgeschrieben (nie die Caption nachgebessert):
trifft es wirklich einen Schmerz · denkt sie „krass, wieso weiss die, was ich denke“ ·
sagt man das so am Küchentisch zu einer Freundin · **stimmt der Bezug zwischen den
beiden Zeilen** · **ist die Lösung draussen** (die Lösung kommt nie im Hook).

🚨 **Die fünfte Frage kam am 20.09.2026 dazu — und gefunden hat den Fehler Patricia,
nicht der Check.** Der Hook lautete: *„Im zweiten Jahr hat mich keiner mehr angerufen.
Die Zahlen waren **trotzdem** dieselben.“* Gemeint war „niemand meldet sich mehr **und**
es bewegt sich nichts“ — dagestanden ist das Gegenteil: *niemand rief an, aber es lief
gleich gut*. **Ein Bindewort hat den Sinn gedreht**, und die anderen vier Fragen schlagen
dabei nicht an: der Schmerz stimmt, die Sprache stimmt, die Lösung ist draussen.
Jedes *trotzdem · obwohl · aber · dabei · sondern* laut gegenlesen und prüfen, ob dort
wirklich ein Gegensatz steht. Bei einem **B-Roll** wiegt das doppelt: der ganze Hook steht
sieben Sekunden unverändert im Bild, und was man zweimal lesen muss, wird weggewischt.

Zwei Begriffe, die nicht verwechselt werden dürfen:
- **Familie** = wie ein Hook *klingt* (Bekenntnis, Zeitanker, Hot Take)
- **Angle** = aus welcher *Richtung* geschaut wird (Schmerz · Ergebnis · Beweis ·
  Konträr · Identität · Neugier · Vergleich)

Zehn Hooks können sieben Familien haben und trotzdem alle dasselbe sagen.
**Mindestens 3 Angles mischen** — sonst erreicht ein ganzes Set dieselben Frauen.
Die **Bewusstseinsstufe** (Reichweite 1–2 · Lead 2–3 · Story/Launch 4–5) entscheidet,
ob der Hook ihre Frage stellt oder schon meine Antwort gibt.

---

## Commands

### 🧭 Welcher Skill für welchen Auftrag (seit 2026-10-02)

Patricia: *„mir ist es einfach wichtig, dass wir eine saubere skillablage haben. nicht
dass es ein durcheinander gibt, wenn ich einen auftrag gebe."* **Je Auftrag ist genau
ein Skill zuständig.** Überschneiden sich zwei, wird einer archiviert — nicht beide
gepflegt.

| Auftrag | Skill |
|---|---|
| Instagram-Woche oder -Monat | `/content` |
| einzelnes Reel · Karussell · Story · Caption | `/reels` · `/karussell` · `/story` · `/caption` |
| nur Hooks, erste Zeilen, Kundensprache | `/hooks` |
| **Verkaufstext**: Verkaufsseite (ThriveCart, 13 Blöcke), Mail-Strecke, VSL, Text überarbeiten | **`/copywriting`** |
| gestaltete Verkaufsseite als HTML | einer der 4 Design-Skills (nach `/copywriting`) |
| **Meta-Anzeige**: Text, aufsetzen, testen, skalieren | **`/facebook-ads`** (Kevin + Werbeanzeigentext Master + Julias Pipeline) |
| ChatGPT-Anzeigen | `/chatgpt-ads` |
| Produkt, Treppe, Launch · Funnel-Technik | `/produkt` · `/funnel` |
| Engpass, Entscheidung, nächster Schritt | `/strategie` |
| Blog | `/blog` |

🗃 **Archiviert am 02.10.2026** (`reference/_archiv-skills/`): `/salespage`, `/hormozi`,
`content-master`, `werbeanzeigentext-master` — in `/copywriting` aufgegangen, ausser
`werbeanzeigentext-master`: der steht Wort für Wort als Ergänzung in **`/facebook-ads`**,
zusammen mit Julias Copywriting-Pipeline als Qualitätsprüfung für Anzeigen.
`/salespage` steht dort als Abschnitt **„ThriveCart-Tipps"** (13 Blöcke, Interviewfragen,
Ausgabeformat). 🚨 **Julias Text im Skill bleibt Wort für Wort unverändert** (Patricia:
*„nichts wird überschrieben von julias inhalt. ich will mich grundsätzlich an ihren skill
halten. sie hat ja erfolg damit"*) — eigene Regeln nur als markierte Ergänzung.
Die Hormozi-Bibel (`reference/hormozi/copywriting-bible.md`) bleibt als Nachschlagewerk.
🚨 Dabei kam heraus: `content-master` und `werbeanzeigentext-master` (gekauft) **lagen
getrackt im öffentlichen Repo** (seit Commit a4b0c41). Jetzt aus dem Index genommen und
gitignored — in der Git-Historie bleiben sie sichtbar.

### /start und /shutdown — Anfang und Ende jeder Session (seit 2026-10-04)

**`/start`** liest Repo-Stand (inkl. Lock-Datei-Check), die geänderten Dateien der
letzten drei Tage, `patricia-interview-2026-10.md`, `business-info`, `strategy`,
`personal-info` und die Termine der nächsten 14 Tage — fasst in rund 15 Zeilen zusammen
und fragt *„Woran arbeiten wir heute?“*. Ändert nichts.

**`/shutdown`** räumt nur sicheren Müll weg (Rest wird gefragt), zieht CLAUDE.md,
`context/` und das Gedächtnis nach, lässt `obsidian-reindex.sh` laufen, prüft auf
Schlüssel und Personendaten, **committet und pusht** (der Aufruf ist der Auftrag dazu),
berichtet und verabschiedet sich.

Herkunft: Ordner-Vorlage aus Julias Claude-Kurs (dort `/start` + `/shutdown`; dieser
Workspace stammt aus derselben Vorlage). **`/prime` ist darin aufgegangen** und liegt in
`reference/_archiv-skills/prime-alt/` — es las noch die Kontextdateien vom Mai.
Keine Weitergabe-Anleitung (Herkunft Kursmaterial).

🚨 **Das auto-sync sichert nur `outputs/`, `context/`, `plans/`, `reference/`.** Skills,
`scripts/`, `.github/` und CLAUDE.md kommen nur über `/shutdown` auf GitHub — am
04.10.2026 lagen dort rund 100 nie gesicherte Änderungen. `/shutdown` stagt deshalb alles
Nicht-Ausgeschlossene (ausser gelöschten Dateien) und macht vorher eine Schlüssel- und
Personendaten-Gegenprobe.

### Sicherung der ausgeschlossenen Dateien (`scripts/sicherung/`, seit 2026-10-04)

Was `.gitignore` von GitHub fernhält (Schlüssel, `context/persoenlich/`, Finanzen,
Strategie, Cockpit-Abgleich, gekaufte Kurse, Fotos, Videos — rund 63 GB), hatte **keine
Sicherung**. Jetzt: verschlüsseltes 7-Zip-Archiv (AES-256, Dateinamen verschlüsselt) in
`OneDrive\Workspace-Sicherung\` — **Kern** (~4 GB, ohne Fotos/Video/Audio) **So 21:00** wöchentlich,
4 Stände · **Medien** (~59 GB) **Sa 21:00 alle 4 Wochen**, 1 Stand. Windows-Aufgabenplanung
(„Workspace-Sicherung Kern/Medien“), holt verpasste Läufe beim nächsten Start nach.
Erster Kern-Lauf 04.10.2026: 2,7 GB, geprüft. Gebaut in `%TEMP%`, mit `7z t` geprüft,
dann verschoben und per `attrib +U` nur online gehalten (C: hat wenig Platz).

```bash
powershell -ExecutionPolicy Bypass -File scripts/sicherung/sichern.ps1 [-Medien] [-Probe]
```

🚨 **Passwort in `scripts/sicherung/.env`** (`SICHERUNG_PASSWORT`), von Patricia selbst
gesetzt, nie im Chat. Vergessen = Sicherung verloren. Wiederherstellen: siehe
`scripts/sicherung/README.md`. Nie gesichert: `.claude/worktrees/` (25 GB temporär),
`node_modules`, Render-Zwischenstände.

### /create-plan [anforderung]

**Zweck:** Detaillierten Implementierungsplan erstellen, bevor Änderungen gemacht werden.

Verwenden beim Hinzufügen neuer Funktionalität, Commands, Skripte oder bei strukturellen Änderungen. Erzeugt ein gründliches Plan-Dokument in `plans/`, das Kontext, Begründung und schrittweise Aufgaben erfasst.

Beispiel: `/create-plan Wettbewerbs-Analyse-Command hinzufügen`

### /implement [plan-pfad]

**Zweck:** Einen mit /create-plan erstellten Plan umsetzen.

Liest den Plan, führt jeden Schritt der Reihe nach aus, validiert die Arbeit und aktualisiert den Plan-Status.

Beispiel: `/implement plans/2026-01-28-wettbewerbs-analyse-command.md`

### /content — der eine Content-Skill (seit 2026-09-14)

**Aufruf:** `/content woche` · `/content monat`

**Zweck:** Schreibt den kompletten Content für den gewählten Zeitraum — Marktcheck,
Hooks, Reels, Karussells, Captions, Design-Bauplan, Story-Bogen. **Der Rhythmus ist ein
Parameter, kein eigener Skill.** Eine Woche sind 5 Beiträge, ein Monat vier Wochen plus
Dreh-Liste zum Abfilmen an ein, zwei Tagen.

**Zwei Betriebsarten:**
- **🤖 Automatik (Normalfall):** Fr 08:00 über den **Scheduled Task
  `content-woche-freitag`** — laeuft ohne Stopps durch, legt alle drei Formate in die
  Wochen-Vorschau und die drei Dokumente in den Bild-Editor, Telegram-Push.
  🚨 **Nicht die GitHub-Action `freitag-hooks.yml`** — deren Cron ist seit 13.07.2026
  auskommentiert, und eine Action kommt ohnehin nicht an die Artifact-Datenbank.
  Ein Scheduled Task laeuft nur, solange die App offen ist; ist sie Freitag um 8 zu,
  laeuft er beim naechsten Start nach.
- **🛑 Begleitet:** Beim Aufruf im Chat hält der Skill an jedem Stopp-Punkt an und
  wartet auf „weiter“. Sinnvoll bei Launch oder neuem Thema.

**Ablauf (9 Phasen):** Planung lesen (Monatsplan, Wochenfokus, Funnels, letzte 4 Wochen)
→ 🛑 Marktcheck (Pain/Wunsch/Ziel/Herausforderung je Profil, mit Zitat und Quelle)
→ 🛑 Hooks (über den Hook-Skill) → Auswahl (5 Slots **je Profil**: **3 Reels, 2 Karussells** — Patricias Entscheid 19.09.2026, vorher umgekehrt; Job-Mix-Check)
→ **je Slot zwei fertige Varianten A/B** (seit 14.09.2026 — Patricia pickt im Cockpit,
die Freigabe ist die Auswahl)
→ 🛑 Bauen → Story-Bogen → Dreh-Liste (nur Monat) → Rohmaterial vom Handy
→ Ablegen und einplanen.

**🎯 Die Tagesfrage** (seit 30.09.2026, vor jeder Story und jedem Post): *Was gebe ich meiner Kundin heute mit?* Inspiration · einen krassen Tipp · warum mit mir und dass es auch für sie möglich ist. Wird je Beitrag benannt, bevor geschrieben wird, über die Woche alle drei. Die eine Definition steht oben in `context/brand-voice.md`, Verweise in `/content`, `/story`, `/caption`.

**🛑 Der Beitrags-Check** (Phase 6) ist die Qualitätsabnahme — gilt auch im
Automatik-Lauf. Fünf Fragen, eine mit Nein und der Beitrag wird überarbeitet:
berührt es · nimmt sie etwas Konkretes mit · warum sollte sie das speichern oder
weiterschicken · warum sollte sie kommentieren · **Name abdecken: wäre das erkennbar
von ihr?** (seit 30.09.2026, Regeln im Block „Persönlichkeit zeigen“ in `context/brand-voice.md`).
*(Hintergrund: Engagement lag bei 0.3–0.5 %, Richtwert 1–3 %. Befund der Profil-Analyse:
zu nüchtern und zu abstrakt — weder berührt noch konkret weitergeholfen.)*

**CTA nach der 3+2-Regel (seit 15.09.2026):** 3 Lead-Posts mit **Keyword-CTA**,
2 Reichweiten-Posts mit **Share-CTA**. Die Reichweiten-Posts bleiben frei von
Verkaufs- und Keyword-CTA — sie sind der Zulauf, damit die drei Lead-Posts nicht
in eine leere Community fallen.

🚨 **Das ersetzt die alte 3+1-Regel** (3 Reichweite / 1 Lead). Patricias Entscheid
vom 15.09.2026: der Engpass liegt vorne im Trichter, deshalb Lead-Fokus.
Wenn die Reichweite darunter einbricht, ist **das** der Grund — nicht die Hooks.

**Reels:** kein langweiliges Reel, auch B-Roll nicht (bestätigt 11.10.: *„B-Roll will ich animiert haben durch dich"*) — mindestens zwei gestaltete
Elemente (Kelsie-Textebene, wortgenaue Untertitel, Auto-Zoom, eingefügte Bilder,
Visualisierungen). Animationen immer mit den **vier Angaben** beschreiben: Aussehen ·
Bewegung · Stelle (den Satz nennen, nie die Sekunde) · Sound. Erst Konzept, dann rendern.
Dreh- und Kameraregeln: `context/sprechreels-drehanleitung.md`. Der **Wissens-Dump**
(10–20 Min frei sprechen) ist die stärkste Quelle — einmal filmen ergibt Wochen an Content.

**Fehlt ein Talking-Head-Video:** Telegram-Nachricht mit fertigem Sprechtext, Setting und
Dauer. Der Rest der Woche wird trotzdem gebaut.

**Auslieferung:** Karussells direkt über Blotato · Reels plus Titelbild per Telegram
aufs Handy · Captions und Hashtags bleiben im Cockpit zum Kopieren.
**Nichts einplanen ohne ausdrückliches Go.**

**Hooks aus dem Konkurrenz-Scrape dürfen übernommen werden** (seit 2026-09-14), wenn sie
zur Marke passen — durch Blackliste und letzten Check, Szene und Zahlen aus Patricias
Leben, Herkunft in der Hook-Tabelle vermerken.

🗃 **Abgelöst und archiviert** (`reference/_archiv-skills/`): `freitag-hooks`,
`montag`, `content-monat`, `content-bauen`, `monats-hooks`. Sie unterschieden sich nur
im Zeitraum; vier davon wurden faktisch nie benutzt. Was an Regeln drinsteckte, ist in
`/content` übernommen — siehe `reference/_archiv-skills/README.md`.

### 🧹 Feed-Regeln aufräumen — ein Skill für Beiträge (seit 2026-10-11, im Umbau)

**Patricia:** *„es ist ein durcheinander, viele skills und viele vorschriften"* · *„ich stelle
mir einen instagram-content-assistenten vor, der EINEN SKILL hat wo alles drin steht"* ·
*„lege nicht noch eine neue routine und noch einen neuen skill an"*.
Inventur vom 11.10.: **238 Regeln** für Feedbeiträge, **56 Widersprüche**, 13 abgelöste noch
in Dateien, 110 Festlegungen aus Chats. Befund: Mentoring seit 1.8. **84 Beiträge, 77 ohne
Kommentar** — Engpass ist Reaktion, nicht Reichweite.
**Checkliste mit Patricias Entscheiden:** `outputs/strategie/2026-10-11-feed-regeln-checkliste.md`
(gitignored, Coach-Namen; Rohlisten in `feed-inventur/`). Teil A = 21 Regeln nach Gewicht mit
Prüffrage (Mehrwert zuerst · **Mikro statt Makro** · Punkt A → Weg → Punkt B …), Teil B = 15
Entscheide (5 Beiträge je Profil, 3 Lead + 2 Reichweite, Listen ja, Stichwort Anfang + Schluss,
letzter Check = ganze Checkliste …). **Nächster Schritt:** hooks/caption/reels/karussell/visuals
gehen in `/content` auf; was gilt, steht nur noch dort. ⚠️ Offen: B5, B9, welche Karussell-Typen.
**Mikro/Makro** stammt aus einer Profil-Analyse von **Laura Hersche** (Bildschirmaufnahme 07.10.,
Transkript `nachbau/2026-10-07-mentorin-mikro-makro/`). **B-Roll wird seit 11.10. animiert.**
Anna (@die.erfolgstexterei, Kurs „Content Shortcut") steht seit 11.10. in der Kern-Nische.
**13.10.: `/content` v2.1 ist der eine Instagram-Skill** — auch für Einzelaufträge („Hooks / Karussell /
Reel zu X“). Eingebaut aus Patricias drei Kurs-Skills (Originale in `context/Kurse/aktuelle kurse/Content-Shortcut/skills/`):
TEIL 0 mit Leserin **Sandra** und 23-Uhr-Test, fünf Säulen, Mikro statt Makro, belegte Eckdaten (4 Kinder,
2018/2021/2023) · Hook-Regel **Gegner, Geständnis oder Zitat** mit zehn Stilen · **sieben Karussell-Baupläne**
· Reel-Skript-Format. Wissen in `.claude/skills/content/wissen/` (gitignored, fremde Konten). Entscheide: 3+2-Regel
mit Stichwort bleibt · Lösung erst ab Folie 2 · Caption-Länge nach Sinn. ⚠️ Offen: `hooks`, `karussell`, `reels`,
`caption` archivieren, damit nicht zwei Stellen Hooks schreiben.
Dazu am 13.10. die drei Begleit-PDFs (Copyformeln · Sales Guide · KI-Brandvoice) geprüft: übernommen sind
CTA ohne Denkarbeit, Verkaufs-Story in 6 Folien, Mini-Sprechstunde, Frage-Antwort/Meinung/Open Loop; bewusst
nicht Powerwörter, Nutzen-Hooks, Studien-Hooks, gespielte Füllwörter. Liste: `context/Kurse/aktuelle kurse/Content-Shortcut/unterlagen/`.
**Der Content-Kreislauf** (13.10.): sechs Stationen Verstehen → Monat → Woche → Posten → Messen → Auswerten, mit Quellen
und Rückfluss, steht oben in `/content`; Station 1 vierteljährlich und Station 6 laufen in `/monatsplan` (4.5a/4.5b,
liest `auswertung.json`). Kursfassung mit eigenen Prompts: `outputs/produkte/ki-treppe/12-content-kreislauf-kursmaterial.md`.

### Die Hook-Maschine — erst die Zahlen, dann schreiben (seit 2026-10-04)

**Anlass:** Apeli-Webinar (Maxi Raabe, „Luma“). Seine „revolutionäre KI“ ist ein langer Prompt
plus Kontext plus Beispiel-Datenbank; Prompt und Kontext hatten wir, die Datenbank fehlte.
Plan: `plans/2026-10-04-hook-maschine.md`. Transkript: `nachbau/2026-10-04-apeli-webinar/` (gitignored).

```bash
python scripts/hooks/markt-analyse.py      # eigene + Markt-Beiträge, Faktor gegen Konto-Median, Claude-Etiketten (Cache)
python scripts/hooks/verkaufsdaten.py      # Lead-Beiträge: Kommentar-Rate, Eintragungen je Stichwort, Verkaufssignale im Markt
python scripts/hooks/beispiele.py --profil mentoring --thema "<Fokus>"   # das Paket, das vor jedem Hook gelesen wird
```

**Ihre Nische** (von Patricia benannt, `nische: kern` in `context/competitor-watchlist.json`): Mentorinnen,
die Networkerinnen und Selbständigen Social Media und Verkauf beibringen — Julia, Reichweitenherz, Nikoleta,
Fühlbarmacherin, Katrin Hill, Dascha (Anni Hoffmann und karriere.mum sind für den Scraper gesperrt).
🚨 **Nie Networkerinnen als Vergleich vorschlagen** — das sind ihre Kundinnen.
Weitere Bausteine: `scripts/apify/scrape-tiefe.js` + `.github/workflows/apify-tiefe.yml` (einmalig ~200
Beiträge je Konto, Push der yml löst aus, eine Datei je Lauf — am 04.10. haben sich drei Läufe überschrieben)
· `scripts/hooks/bild-hooks.py` (Hook vom Titelbild lesen, bei 761 von 795 Nischen-Beiträgen stand er dort)
· `scripts/hooks/themen-analyse.py` (welche Gedanken, Gefühle, Einwände die Nische aufgreift und welche ziehen)
· `context/hook-datensaetze.md` (Psychologie · Positionierung · Angebote).
**Gesamtbericht: `outputs/marktrecherche/2026-10-04-hook-gesamtbericht.md`** — Dialog und Ereignis tragen
überall, Schmerz-Angle und Du-Szene nirgends; Gedanken mit Kraft sind Umfeld, Anschreiben, Kamera-Scham,
Vergleich; KI ist ein schwaches Hook-Thema (0,91).

Eingebaut als **TEIL 0 im Hook-Skill** und in **`/content` Schritt 4** (damit auch im Freitag-Task).
Jeder Hook nennt sein **Vorbild** aus dem Paket. Berichte: `outputs/marktrecherche/2026-10-04-hook-*.md`.

**Befund 04.10. (Mentoring):** Identität gewinnt (1,16; Markt 1,33), Schmerz — ihr häufigster Angle — 0,72 ·
Stufe 1 = 1,2 → Stufe 4 = 0,53 · Listen 0,45 · Ich als Spiegel trägt, Ich als Beweis (0,56) nicht ·
**101 von 129 Lead-Beiträgen hatten null Kommentare.**
🚨 **Die wöchentlichen `outputs/marktrecherche/KW*.md` haben in allen 46 Läufen 0 Reddit-Posts gelesen** —
die Painpoints darin sind erfunden („generisches Pattern“), nie als Beleg zitieren. Der Generator dazu ist
nicht im Repo gefunden worden (läuft vermutlich remote).
🚨 Fremde Verkaufsdaten gibt es nicht; „Verkaufsdaten“ heisst hier: ihre eigenen plus Verkaufssignale im Markt.

### /strategie — der Business-Stratege (seit 2026-09-24)

**Zweck:** Die eine Stelle über allen Bau- und Planungs-Skills. Beantwortet: *Was ist
gerade der Engpass zwischen mir und 40'000 CHF — und was tue ich als Nächstes?*
Liest die Abgleich-Dateien in `outputs/cockpit/abgleich/` (Umsatz, Monatsbogen, Ziele,
Katalog, Gepostet, Reichweite, Mailings, Funnel), geht **fünf feste Angles** durch
(Ziel-Lücke · Zulauf · Umwandlung · Angebot & Warenkorb · Zeit & Fokus) und endet mit
**einem** Engpass, einer Empfehlung samt Aufwand, Messgrösse in 14 Tagen und dem, was
dafür wegfallen darf.

**Aufruf:** `/strategie` (Standort) · `entscheid <Frage>` · `restjahr` · `hebel <Idee>` ·
`rueckblick` · `stufe` · `ohne-launch`. Führt nichts aus, schickt zum passenden Skill.

**Anlass:** *„ich habe immer nur dann umsatz, wenn ich einen launch habe.“* Deshalb misst
jeder Standort den **Sockel** (Umsatz ausserhalb der Launch-Fenster, Raten am Monatsanfang).

**Julias Roadmap** steckt in `.claude/skills/strategie/wissen/` (gitignored, Fremdmaterial):
`julia-stufen.md` (Stufen, Fast Cash, 24 Diagnose-Fragen) · `julia-evergreen.md`
(Warenkorb, Automationen, 13 Schritte „wenn man bisher nur launcht“) · `julia-mentoring.md`
(25 Prinzipien, 29 Fehler aus 16 Calls). 🚨 **„k“ heisst bei ihr Monatsumsatz** — 40k/Jahr
ist ihre Stufe 0→5k. 🚨 Unter 10–15k/Monat rät sie zu **lückenlosem Live-Launchen**, nicht
zu Evergreen. 🚨 Die Transkripte haben Vorrang vor `reference/julia-trost/methodik.md`,
dessen Skalierungs-Leiter Funnel und Liste zu früh ansetzt.

🚨 **Output nach `outputs/strategie/` — der ganze Ordner ist gitignored.** In der
`SKILL.md` selbst stehen keine echten Zahlen, weil sie getrackt ist. Nur Eigengebrauch,
keine Anleitung.md.

### Magnet-Ich-Onboarding (seit 2026-09-24)

Kundinnen des 1:1 **Magnet-Ich** (333, 3 Wochen) beantworten die 9 Vorbereitungsfragen
auf einer Artifact-Seite **ohne Fähigkeiten** und schicken sie per Knopf als
WhatsApp an Patricia (`wa.me`-Link, Entwurf bleibt per `localStorage` auf dem Gerät):
https://claude.ai/artifact/MBpprtwLrrgQzenaiPoBny — muss über das Share-Menü öffentlich
geteilt werden, sonst kann die Kundin sie nicht öffnen.
🚨 **Ein Artifact kann keine Antworten von Kundinnen speichern** — `db` schreiben nur
Organisationsmitglieder oder eingeladene claude.ai-Konten. Deshalb der Rückweg über WhatsApp.
**Salespage** (seit 24.09.2026): Texte `outputs/salespages/magnet-ich-salespage.md` (13
Blöcke, `/salespage`), gebaut im **Signature-Design** → WP-Seite **4251** `/magnet-ich/`
(Entwurf, `elementor_canvas`). Markup `outputs/salespages/magnet-ich/magnet-ich-inhalt.html` aus den Bausteinen der
`reference-page.html`. 🚨 **Das CSS wird nicht geschrieben, sondern aus der Vorlage gezogen:**
`python scripts/salespage-design/magnet-ich-bauen.py` nimmt den `<style>`-Block der Vorlage
unverändert, scopt ihn auf `.mi-sp` und hängt die wenigen Anpassungen kommentiert an →
`magnet-ich.css` (gehört in den Customizer). Patricia am 24.09.: *„halte dich exakt an den
skill bitte“* — der erste Bau hatte eigenes CSS und fünf Pflicht-Abschnitte ausgelassen.
Bild-URLs in `medien.json`. Deploy: `node --env-file=.env deploy-magnet-ich.mjs` (wiederholbar, lädt nur
fehlende Bilder hoch). 🔁 Herbst-Aktion (3 Plätze, Start-Calls ab 19.10., Anmeldung bis
27.09. → dritter Call) steht im Hero, bei den Boni, im Preisblock, in der FAQ und im
letzten Aufruf — nach der Aktion dort austauschen.
📉 **Ergebnis Herbst-Aktion: kein Verkauf** (Patricia, 28.09.2026). Seit 28.09. steht die Seite
als normales Angebot ohne Aktion (Frist, 3 Plätze, dritter Call raus); auch der Herbst-Kasten
in den Nachkauf-Mails 0 und 3 ist entfernt.
🚨 **Am Handy liegt das Hero-Foto als eigenes `<img>` über dem Text**, nicht dahinter —
als Hintergrund lag der lange Hook über dem Gesicht.

**Nachkauf-Mails** (seit 25.09.2026): `python scripts/magnet-ich/mails-bauen.py` →
`outputs/produkte/magnet-ich/mails/` (Tag 0 Willkommen + Link zum Onboarding, Tag 3
Erinnerung). Gerüst wird aus `scripts/startklar/mails-bauen.py` **importiert**, nicht
kopiert. Ersetzt in AC-Automation **42 „Magnet-ich“** die alte Mail 375 (Drive-PDF mit
Lorem auf S. 14, Instagram-Link `hhttps://`). 🔁 Kasten „Herbst 2026“ nach der Aktion löschen.
**Im Cockpit** unter „Listen & Automationen“ → Nr. 42 („neue Fassung“): echte HTML-Vorschau
plus Knöpfe HTML/Betreff/Vorschautext. `python scripts/magnet-ich/mails-ins-cockpit.py` →
JSON je Mail in `outputs/cockpit/abgleich/mailentwuerfe/` → `ArtifactData batch set`,
Sammlung **`mailentwuerfe`** (gehört nicht dem Abgleich). Anzeige gesetzt mit
`scripts/cockpit/patch-mailentwuerfe.py` — taugt für jede Automation, Feld `automation`.

### Launch-Storys als Gerüst (seit 2026-09-25)

**Patricia:** *„dass die storys im grundgerüst mit dem inhalt abgespeichert sind im
cockpit, dass ich nicht jedes mal überlegen muss.“* Für jeden Launch-Tag liegt eine
fertige Story-Sequenz im Cockpit (Story-Studio) **und** im Bild-Editor („Aus deiner
Planung“ → Tag → Mentoring). ✏️ markiert die Stelle für den Alltag von heute.
`python scripts/launch/storys-ki-launch.py` → `outputs/cockpit/abgleich/launch-storys/`
→ `ArtifactData batch set` (Sammlung `storys`, Kennung `kw<NN>-story-m-ki-<tag>`) und
`daten/entwuerfe` im Bild-Editor ergänzen. Das wiederverwendbare Gerüst (Phasen,
Story-Arten, Wochenrhythmus) liegt in `.claude/skills/strategie/wissen/launch-story-geruest.md`
(gitignored, aus dem Launch-Workbook) — für Mama-CEO und MBA einfach ein neues `TAGE`
im Skript. 🚨 **Das Cockpit lädt nur 60 Story-Sequenzen** (`db.collection("storys").limit(60)`),
Stand 25.09.: 54. Vor dem nächsten Launch das Limit erhöhen oder alte Storys archivieren.
🚨 Herbstferien: **28.09.–16.10.** laut Cockpit-Jahresplan (Patricias „letzter Tag vor
den Herbstferien“ war Fr 25.09.) — der Launch-Kalender nannte fälschlich 5.–16.10.

### Story-Bibliothek im Cockpit — Gestaltung je Folie (seit 2026-10-08, Version 91/92)

**Patricia:** *„ich hätte das im übrigen immer noch gerne in der storybibliothek unter dem
cockpit selber und nicht separat"* — Storys werden **im Cockpit** (Instagram → Storys)
gestaltet und exportiert. Je Folie unter **„Gestalten“**: Schrift (Philosopher · kursiv ·
Source Sans leicht · fett) · links/Mitte/rechts · Textbalken ohne/Zeilen/Karte ·
**Hintergrund** Foto/Dunkelblau/Creme/Petrol/Orange (bei Foto die 12 Shootingbilder oder
eigenes Foto, Zoom/Lage, Schleier) · Höhe · Grösse · **Platz für Sticker**. Layouts
**learning**, **kurs** (Haken-Liste), **bonus** (orange Pille). Felder: `eyebrow` · `text` ·
`punkte` · `klein` · `pille` · `notiz` (✏️, nie im Bild) · `sticker`/`stickerText` ·
**`extra`** (Version 93: Liste freier Textblöcke `{text, pos, groesse, schrift, balken}`,
angelegt über **„+ Textblock“** — dazu „+ Zeile oben / + Pille / + Haken-Liste“ auf jeder Folie).
**Version 94 (Patricia am Handy: „etwas fummelig“ · „jeden textblock einzeln bearbeiten“ ·
„lockerer und unterschiedlicher“):** Fokus-Ansicht — oben Miniaturen, darunter EINE Folie,
Vorschau bleibt beim Scrollen stehen · je Textblock (1 = Haupttext, dann `extra`) eigener Kasten
mit Schrift · Ausrichtung · Balken · **Farbe** (`farbe`: creme/weiss/dunkel/petrol/orange — mit
Balken die Fläche, ohne die Schrift) · Höhe · Grösse. **Neigung seit V95 wieder raus** (Patricia: *„muss ich nicht einstellen“*), `dreh` wird nicht mehr gezeichnet.
🚨 **Storys wurden nie in die Datenbank gespeichert, sobald eine Folie gezeichnet war**: an jeder
Folie hängt zur Laufzeit `__draw` (Funktion), die DB nimmt nur JSON → „nur lokal gespeichert“.
Seit V94 speichert `saveStory` über `framesSauber()` (alles mit `__` raus).
🚨 **Vorschläge abwechslungsreich gestalten:** keine zwei Folien hintereinander mit gleichem
Hintergrund, gleicher Ausrichtung und gleicher Schrift; ab und zu leicht geneigt.
🚨 **Sticker werden nie gemalt** — gestrichelter Platz nur in der Vorschau. Altes `cta`
wird von `stilVon()` zur Sticker-Fläche. Kein gemalter Fortschrittsbalken, kein Handle.
🚨 **Dunkelblau ist `#29556d`** (brand-identity.md), **`#0c1c30` ist die Textfarbe** —
bis 08.10. stand die Textfarbe als Hintergrund in „Mum Life Balance dunkel“ und im
Story-Hintergrund (Patricia: *„nicht das richtige blau“*).
Quelle: `scripts/cockpit/story-bibliothek.js` + `story-karte.js`, eingesetzt mit
`patch-story-bibliothek.py` (Neulauf frischt beide Blöcke auf, setzt Storys-Limit 200 und
das Dunkelblau). Launch-Bausteine `foto() · learning() · kurs() · bonus() · platz()` in
`scripts/launch/storys-ki-launch.py`; Käufertypen je Sequenz: Ina/Amelie persönlich ·
Willi Learning · Frank Kurs-/Fakten-Karte · Zoe Bonus/Frist · Rudi nur mit echten Käufen.
🚨 Der Abend des 8.10. steht nur im Cockpit (`storys/kw41-story-m-ki-do`, Folien 7–16).
**Launch-Storys durchgestalten:** `python scripts/launch/storys-gestalten.py <storys-ordner> --ziel <ordner> --ab 2026-10-09 --bis 2026-10-23 --nur-name <id>`
wechselt je Folie Foto · Creme · Dunkelblau · Petrol-Zitat · Orange-CTA, setzt Haken-Listen als Kurs-Karte,
Fragen/Umfragen mit Sticker-Platz und benennt jede Story „9.10. · Freitag · KI-Launch · …“. 🚨 Der Wortlaut
bleibt unverändert — das Skript bricht ab, sobald ein Wort fehlt oder dazukommt. Danach `ArtifactData batch update`
mit `if_version` (am 08.10. 27 Storys, 14 neu gestaltet, der 8.10. selbst nur umbenannt).
**Käufertypen-Gegenprobe (seit 08.10.2026):** `python scripts/launch/storys-mitmacherin.py <quelle> --ziel <ordner>`
hängt den 15 Story-Tagen der Verkaufsphase die Folie `s-dabei` **vor** die letzte an (5 Wortlaute, 3 Looks im
Wechsel). 🚨 Anlass: in allen **139 Folien** der 19 KI-Launch-Tage kam **die Mitmacherin** („wer ist schon
dabei") **nicht ein einziges Mal** vor — weil die Storys vor dem ersten Kauf geschrieben wurden und sich
Social Proof nicht vorschreiben lässt. Die Folie ist ein **Platz**, kein Inhalt: Anweisung in `notiz`
(Screenshot, Vornamen nur mit Okay, ohne echten Kauf Folie weglassen). Befund und Wochen-Matrix:
`outputs/produkte/ki-treppe/11-kaeufertypen-in-den-storys.md`.
🚨 **`layout` muss zum `hg` passen** — `bild` nur mit `hg: "foto"`, sonst `text`. Sichtbar ist der Fehler nicht
(der Hintergrund kommt aus `hg`), aber `storys-gestalten.py` stuft nach `layout` ein und legt sonst später ein
Foto unter. Gültige Werte: `hg` = foto · creme · dunkel · petrol · orange, `balken` = aus · zeilen · karte.

🗃 Erster Anlauf über WordPress + AC-Formular verworfen (Patricia: „das geht doch
einfacher“): WP-Entwurf 4243 und AC-Felder `MI_*` (IDs 10–18) liegen noch.

### KI-Launch-Funnel — Stimm-Check + Masterclass (seit 2026-09-25)

**Übersicht mit allem Offenen:** `outputs/produkte/ki-treppe/09-funnel-geruest.md`.
Masterclass **Do 8.10.2026, 09:00** (AC-Formular 69, Tag „0€ KI Webinar“ 100). Stimm-Check = 0€-Tool in
`scripts/stimm-check/` (Zwilling von Freischaufeln, lokal: `preview_start stimm-check`, Port 4397),
Tag „0€ Stimmcheck“ (105), AC-Automation **83**. **Tool live:** https://stimm-check.vercel.app/ (seit 26.09., Deploy `cd scripts/stimm-check && npx vercel --prod --yes`, kein Tages-Limit). 🚨 **Patricia will je Funnel EINEN Tag** — keine Zwischen-Tags für Klicks oder Abschluss (25.09.). Seiten: `/stimm-check/` 4262 im **Minikurs-Baukasten** (CSS aus der Vorlage auf `.sc-sp`
gescopt, `scripts/salespage-design/stimm-check-bauen.py`, Formular 71 als iframe) · `/stimm-check-los/`
4263 · `/ki-masterclass/` 4266 im **ki-salespage-Baukasten** (`scripts/salespage-design/ki-masterclass-bauen.py`, Scope `.km-sp`, WP lädt „Source Sans Pro“, nicht „Source Sans 3“) · `/ki-kurs/` 4286 Verkaufsseite (gleiches `.km-sp`-CSS, `ki-kurs-bauen.py`, 🔁 `PHASE` am 16.10. auf `regulaer`) · `/ki-masterclass-danke/` 4258 in der **.pif-Gestaltung** (CSS schon
im Customizer). 🚨 Die Vorlage blendet Abschnitte per JavaScript ein (`.rev`) — WordPress blockt
Skripte, deshalb im CSS immer sichtbar. 🚨 `.pr-val` ist der **durchgestrichene** Gegenwert, nie für
eine andere Zahl benutzen. Mails: `scripts/ki-kurs/masterclass-mails-bauen.py` → Kopierseite
`preview_start ki-masterclass-mail`.
🚨 **Einfache Sprache auf beiden KI-Seiten** (Patricia, 28.09.): Zielgruppe sind Networkerinnen, die KI bisher wie Google benutzen. Leitsatz „Da geht so viel mehr“; Skill = „fester Auftrag“, Bot = „Helfer, der sich von selbst meldet“, Cockpit = „deine Übersicht“, Fachwörter nur mit Erklärung. Die **Plattform für die Kundschaft** (Begleitung zur Energie-Routine als Artifact) ist Station 2 der Masterclass und Lektion **9.3** im Kurs. Lokale Vorschau Kursseite: `preview_start ki-kurs-lp` (Port 4400).
**Launch-Feed (seit 28.09.):** 19 Mentoring-Beiträge 30.9.–23.10. (11 Reels, davon **ein** Sprechreel Fr 9.10., 8 Karussells), eine Variante je Platz, aus `scripts/launch/feed-ki-launch.py` → `outputs/cockpit/abgleich/launch-feed/` → Cockpit (`kw4N-reel-m-*-ki` / `kw4N-kar-m-*-ki`). Flop-Befund dazu: `outputs/content/KW40/launch-feed-befund.md` (Karussells nie über 223 Reichweite · „Folge mir, wenn…“ als Zeile 1 gefloppt · ein Aufruf je Caption). Die KW40-Karussells liegen als Variante neben den schon bei Blotato eingeplanten.
🚨 **`/produkt-ideen-finder-los/` nie umbauen** — Live-Danke-Seite des STANDBEIN-Funnels.
🚨 **Sonnet 5 denkt vor der Antwort:** mit `max_tokens: 3000` kam die Antwort leer zurück.
Im Stimm-Check `thinking: disabled` + 10'000 Token — halbiert die Wartezeit.
🚨 **Die Schreibsprache folgt der Textprobe**, nicht der Selbstbeschreibung: „Mundart-Wörter“
ergab sonst eine ganze Caption auf Schweizerdeutsch.

#### Der Launch läuft — Termine, Pin-Beitrag, MBA-Upsell (Stand 2026-10-19)

**Kursstart 1.11.2026, Kasse schliesst 23.10.** Die beiden Live-Calls: **Mi 18. November**
(vorher Do 19.11., verschoben am 16.10. — Patricia: *„KI Kurs verschieben vom November!!“*) und
**10. Dezember**, beide werden aufgezeichnet.
Deploy der Seite: `node --env-file=.env deploy-ki-kurs-lp.mjs` in `scripts/wordpress`.

🚨 **Ein verschobener Termin steht an SIEBEN Stellen, nicht an einer.** Am 16.10. habe ich nur
die Verkaufsseite geändert; beim Aufräumen am 19.10. lag der alte 19.11. noch in sechs weiteren
Dateien — darunter die **Willkommens-Mail in AC-Automation „KI Kurs" (85)**, die jede neue
Käuferin bekommt. Die Liste zum Abarbeiten bei jeder Terminänderung:
`scripts/salespage-design/ki-kurs-bauen.py` (Verkaufsseite) · `ki-kurs-checkout-bauen.py`
(Zeitplan am Checkout) · `outputs/salespages/ki-kurs-checkout-texte.md` und
`ki-kurs-checkout/textbloecke.md` (handgeschriebene Textquellen, kein Generator) ·
`scripts/ki-kurs/mails-bauen.py` (Willkommens-Mail) · `folien-masterclass.py` ·
`regiezettel-bauen.py`. Danach die Generatoren **laufen lassen** und mit `grep` gegenprüfen,
dass das alte Datum nirgends mehr steht.
🚨 **Der Mailtext in ActiveCampaign ist kein Generator-Ausgang** — er muss dort von Hand
ersetzt werden (`outputs/produkte/ki-kurs/mails/mail-00-willkommen.html`, Kopierseite
`preview_start ki-masterclass-mail`). Eine Datei im Workspace zu korrigieren ändert nichts an
dem, was verschickt wird.
🚨 **Die Raten-Karte nennt bewusst keine Aufteilung** („in Raten, die Aufteilung siehst du an der
Kasse“). `RATEN` in `ki-kurs-bauen.py` wird nur gefüllt, was in ThriveCart genau so eingerichtet
ist — und `/products/52/pricing_options` antwortet mit **403** (dreimal geprüft, beim Upsell geht
dieselbe Abfrage). Eine erfundene Staffel sieht auf einer Verkaufsseite aus wie eine echte.

**Der angepinnte Beitrag zum 0€-Stimm-Check:** `scripts/launch/pin-karussell-stimme.py` baut
Folien und Caption für Cockpit und Bild-Editor, die Bilder kommen aus
`outputs/karussells/pin-stimme/karussell-pin-stimme.html` über `scripts/karussell-render/render.js`.
Titelbild macht Patricia selbst (Manus). Linie der drei Pins: **Creme-Grund, Philosopher dunkel,
Orange als einziger Akzent, kein Petrol** — Details im Gedächtnis
[[feedback_pin-beitraege-titel-cover]].

**Aufs Handy schicken:** `python scripts/telegram/senden.py --bilder <png …> --text-datei
<caption.txt> --titel "<Zeile>"` (seit 08.10.2026). Als **Foto**, nicht als Datei — nur dann
landet es in der Galerie, von wo Instagram hochlädt. Caption als eigene Nachricht (im Album sind
nur 1024 Zeichen erlaubt), höchstens 10 Bilder je Album. Zugang aus der `.env` im Wurzelverzeichnis.

**Das MBA-Upsell am KI-Kurs-Checkout** (ThriveCart-Produkt **52**, Upsell **11**): Wer den KI-Kurs
für 277 kauft, bekommt die Mum Business Academy direkt danach — **zusammen 997 statt 1347**, also
**720 als Upsell-Preis**. Texte und Gestaltung liegen in `outputs/salespages/mba-upsell/`
(`mba-upsell.html` zum Ansehen, `mba-upsell-block.html` für das HTML-Feld in ThriveCart; die
einzeilige Fassung daneben lässt sich über die Zwischenablage einfügen). Dass die 277 bei späterem
Nachbuchen angerechnet werden, steht **nicht** auf der Seite (Patricias Entscheid, 16.10.).

🚨 **Offen und falsch im System:** Das Upsell steht in ThriveCart auf **997 statt 720** — mein
Fehler vom 16.10. Ich hatte „die MBA ist noch falsch drin“ als veralteten Preis gelesen und
720 für 997 − 277 gehalten; gemeint war das Gegenteil: **277 + 720 = 997 ist die Rechnung**, und
die 720 waren richtig. Solange das so steht, bucht die Kasse 277 zu viel ab. Patricia hat
ThriveCart danach selbst übernommen (*„weisst du was, ich mach es selbst“*).
**Die Lehre:** bei einer Preiszahl, die nicht aufgeht, erst die Rechnung aufschreiben und
nachfragen — nie aus einer Differenz schliessen, welcher von zwei Werten gemeint ist.
⚠️ Ebenfalls offen: der Tag in ActiveCampaign aufs Upsell (sonst bekommen Käuferinnen weiter
Werbung für etwas, das sie schon haben) und `/mba/` nennt noch „drei Kurse“ gegen CHF 999.

### Kommentar-Antwort — der ManyChat-Ersatz (seit 2026-09-28, im Aufbau)

**Patricia:** *„ja bitte manychatersatz starten. und erstmal nur für stimme.“* ManyChat löst bei jedem Kommentar aus, in dem das Wort vorkommt („ich **stimme** dir zu“). Der Dienst entscheidet erst über Regeln (`lib/entscheiden.mjs`, 27 Gegenproben in `test/`), nur unklare Fälle gehen an Claude Haiku. Live unter `https://kommentar-antwort.vercel.app/api/webhook` (Vercel-Projekt `kommentar-antwort`), Meta-App „Mum Life Balance Bot“ (984115153982698) mit Produkt Instagram. 🚨 Antwortet erst mit `SCHARF=ja`; vorher nur Protokoll in den Vercel-Logs. 🚨 Ohne Meta-App-Review nur für Konten mit App-Rolle. ManyChat läuft parallel weiter, STIMME dort nie einrichten. Plan: `plans/2026-09-28-manychat-ersatz-stimme.md`.

### Kundinnen-Geschichten (seit 2026-09-30)

Echte Fälle für Säule 2 („Will ich das? Geht das für mich?“) sammeln sich in
`context/kundinnen-geschichten.md`: Vorlage je Fall (Vorher · Schritt · Nachher ·
Wortlaut · Freigabe · passt zu). 🚨 **Keine Klarnamen dort** (Repo public), die stehen in
`context/persoenlich/kundinnen-namen.md`. 🚨 **Patricias Nacherzählung ist kein Zitat.**
Wortlaut nur aus abgetippter Sprachnachricht oder Screenshot. Ohne Freigabe nur anonym.
Content-Skills lesen die Datei, bevor sie eine Kundinnen-Geschichte schreiben, und
erfinden nie einen Fall.

### /monatsplan (Strategie-Layer seit 2026-05-09 · Content-Vorplanung seit 2026-06-07)

**Zweck:** Den **Strategie-Layer** für einen kompletten Monat festschnüren — UND seit 2026-06 den **kompletten Monats-Content vorplanen** (Phase 4.5), damit Patricia in 1-2 Tagen alle Reels für den ganzen Monat abdrehen kann.

**Phase 4.5 (Content-Vorplanung) liefert:** Marktanalyse pro Profil · Vormonats-Content-Analyse (Top/Flop) · pro Woche 5 Beiträge (5 Content-Typen, nach der **3+2-Regel**: 3 Lead-Posts mit Keyword-CTA + 2 reine Reichweiten-Posts mit Share-CTA, Hooks nach `hook-framework`-Regeln, Format-Mix Content-Radar) thema-matched zum Wochen-Produkt · **Reel-Dreh-Liste zum Batch-Filmen** · **Monats-Blogartikel** (via /blog) · **Mail-Newsletter** (Launch-Sequenz oder Mehrwert). **Stories bleiben täglich** über `/story` (im Launch nach Julia-Launch-Drehbuch, sonst nach Julia-Story-Vorlagen). Speist die Notion-Wochenpläne, die der Story-Bot liest.

**Wann ausführen:** Letzter Sonntag des Vor-Monats (z.B. 28.4. für Mai).

**8-Fragen-Interview liefert:**
1. Säule des Monats (Mentoring 1/2/3 oder doTERRA Pillar)
2. 3 zu bewerbende Produkte (0€ / Mini / Gross)
3. Block-Verteilung (Variante A: KW1=A, KW2=B, KW3-4=C — empfohlen)
4. Hauptbotschaft des Monats (1-2 Sätze als roter Faden)
5. Job-Mix-Soll (Standard / Pre-Sale-Modus / eigener Mix)
6. KPI-Ziel (Verkäufe + Followerinnen + ManyChat-Trigger)
7. Was läuft NICHT (bewusste Auslassung statt Gießkanne)
8. Energie-Lage (Schulferien, reduzierte Wochen)

**Vor dem Interview Phase 2 — Vormonats-Diagnose:**
- Notion-Monatsplan vom Vormonat lesen
- Job-Mix-Compliance-Check (was wurde tatsächlich gepostet?)
- Top/Bottom-Posts identifizieren
- Korrektur-Vorschlag für neuen Monat

**Output:**
- Notion-Monatsplan-Page (`collection://2ae7078e-8b7e-81fc-acf7-000be291c92c`) gefüllt
- `outputs/monatsplaene/YYYY-MM.md` mit 4-Wochen-Briefing für `/content`
- Optional Telegram-Push der Kurz-Zusammenfassung

**Warum nicht 30 Posts auf einmal bauen?** Live-Posts (BTS, Telegram-Call-Reaktionen) brauchen Frische. Trends auf Reddit/IG müssen reagiert werden. Pre-Sale-Signale aus Woche 1 ändern Wochen 2-4. Deshalb: **Strategie monatlich, Konkretion wöchentlich.**

### /videoschnitt (seit 2026-09-10)

**Zweck:** Rohmaterial **einmal in die Kamera sprechen** — mit Versprechern und
mehrfach wiederholten Sätzen — und Claude macht daraus den Rohschnitt. Ersetzt
das Suchen-Schneiden-Ärgern (~1 Std/Video) durch ~5 Min Feinschliff in CapCut.

**Ablauf (5 Schritte):**
1. Video in `video/input/` → `python scripts/videoschnitt/transkribieren.py`
   (faster-whisper lokal, Wort-Zeitstempel, Take-Gruppen-Erkennung)
2. **Schnittliste vorlegen** — Claude liest `saetze.md`, wendet die Regeln an und
   zeigt die Liste als Text. Patricia gibt frei. **Pflicht-Schritt, nie überspringen.**
3. `python scripts/videoschnitt/schnitt.py <cutlist.json>` → `rohschnitt.mp4` +
   `clips/01.mp4 …` (für CapCut) + `untertitel.srt` + `words-schnitt.json` + Protokoll
4. **Feinschliff in CapCut — Patricias Teil, seit 16.09.2026.** Claude liefert die
   Abschnitte in `clips/` plus eine `CAPCUT.md` (Tabelle: Nummer, Winkel, gesprochener
   Satz) und den fertigen Befehl. Sie zieht die Schnittbalken, bis es klingt,
   exportiert 1080×1920/30fps nach `video/input/` — **in CapCut nur schneiden**, keine
   Untertitel, keine Effekte, kein Zoom. Dann:
   `python scripts/videoschnitt/aus-capcut.py --export <export>.mp4 --projekt <ordner>`
   🚨 Das Skript **transkribiert den Export neu** statt Zeiten umzurechnen — nach einem
   verschobenen Balken stimmen die alten Wort-Zeitstempel nicht mehr, und Umrechnen
   hiesse raten. Grund fuer den ganzen Weg: **Claude kann den Ton nicht hoeren**, also
   gehoert der Schnitt dorthin, wo jemand hoert. Wer lieber Zahlen tippt als Balken
   zieht, nimmt `schnittliste.md` + `scripts/videoschnitt/kurzfassung.py bauen`.
5. **Finish** via `textebene.py` → HyperFrames-Projekt → fertiges MP4:
   **Auto-Zoom** (jeder zweite Clip Fahrt hinein, dazwischen harter Sprung) +
   **wortgenaue Untertitel** (aktives Wort orange, pausieren automatisch wenn eine
   Einblendung steht) + **Textebene im Kelsie-Blevins-Stil** (zwei Zeilen auf Stoss,
   Poppins Light klein oben / Bold gross unten, durchscheinend mit Farbverlauf,
   Einblendung startet auf dem gesprochenen Wort, grosses Wort **hinter** Patricia —
   braucht `npx hyperframes remove-background`, Auftritt abwechselnd links/rechts/pop).
   **Damit ist CapCut optional, nicht Pflicht.**
6. **Freie Animationen** (Kapitel 06 des Guides): Fuer alles ausserhalb des
   Kelsie-Bausteins IMMER die **vier Fragen** stellen — Aussehen (typ/farbe/
   flaeche/kursiv) · Bewegung (pulsieren/links/rechts/pop/hoch) · Stelle
   (`ab_wort`, den Satz nennen, nie die Sekunde) · **Sound**
   (klick/pop/whoosh/ding, mit ffmpeg erzeugt statt heruntergeladen).
   „Mach eine schoene Animation dazu" ergibt Vorlagen-Optik.
7. **Erst Konzept, dann Render:** `--konzept` legt Standbilder ueber dem echten
   Material in `finish/konzept/` ab. Selbst pruefen (Visual-QA), Patricia zeigen,
   dann erst `--rendern`.

**Regeln = SSOT:** `context/videoschnitt-regeln.md`. Take-Regel „letzter
vollständiger Take gewinnt", Hook bleibt wortwörtlich, 120 ms Luft vor / 350 ms nach
jedem Satz, Pausen auf 0,3 s (Jenyas Werte seit 06.10.2026), nie mitten in ein Wort schneiden. **Wenn ein Schnitt etwas falsch
macht, wird die Regel-Datei geändert — nicht der nächste Chat.** Was Patricia
dreimal von Hand korrigiert, gehört als Regel hinein.

**Jenyas Kurs „Dein Videoeditor ist Claude" (Stan Store, eingearbeitet 06.10.2026)**
brachte drei Neuerungen: `python scripts/videoschnitt/capcut-projekt.py anlegen <cutlist>`
legt den Rohschnitt **direkt als CapCut-Projekt** an (Stücke auf dem Original, Kanten in
beide Richtungen ziehbar) · `… vergleichen <cutlist>` liest nach dem Nachziehen ihre
Änderungen aus der Projektdatei und schlägt **ab zwei gleichen Änderungen** eine Regel
vor, eingetragen erst nach ihrem Ja · **Stil-Analyse über 3–5 Vorbild-Videos** (Schritt 5d).
Dazu Whisper `large-v3-turbo`. 🚨 CapCut muss beim Anlegen und Vergleichen **geschlossen**
sein. Kurstexte lokal in `context/Kurse/aktuelle kurse/Jenya-Videoeditor/` (gitignored).

**Grafik-Ebene nach Jenyas Teil 4 (seit 06.10.2026): ein fester Remotion-Ordner `scripts/grafik/`**
statt eines Wegwerf-Projekts je Reel. Bausteine Hook · Untertitel (je Variante A/B/C) ·
Knallwort · Karte · Clipfolge · Look · Ton, beschrieben in `context/videoschnitt-animationen.md`
(Jenyas `stil.md`). Ablauf: `python scripts/grafik/vorschau.py <projekt>` zeigt A|B|C als
Standbild → Patricia wählt (`stil` in `grafik.json`) → `--stellen` → `--rendern` (prüft vorher
automatisch den Bildrand). Einmalig `cd scripts/grafik && npm install`. Der offizielle
Remotion-Skill liegt als Nachschlagewerk unter
`.claude/skills/remotion-motion-graphics/references/remotion-offiziell/` (kein eigener Skill).
🚨 Nie in den Projektordner rendern (er ist Remotions public-dir, der Lauf bricht ab).
**Vorgabe Stil B** (Hook „Kelsie, Wort für Wort“ + Untertitel „Aktives Wort“), Text-Oberkante 56 %
(unter dem Kinn). Vor jedem Render prüft `vorschau.py` selbst **Bildrand und Gesicht** (OpenCV,
alle 0,4 s; `pip install "opencv-python-headless<5"`) und bricht bei einem Fund ab.

**Herkunft — der Jenya-Kork-Guide „Claude als Videoeditor"** (16 Seiten, in
`Downloads/_fuer-drive/03 - Prompts & KI-Tools/claudealsvideoeditor (1).pdf`)
ist hier **vollständig umgesetzt** und braucht nicht neu aufgesetzt zu werden:
Ordner `input`/`output` mit lokalem Claude Code · die sechs Fragen als
`videoschnitt-regeln.md` · „letzter vollständiger Take gewinnt" · Hook
wortwörtlich · Millisekunden Luft vor dem Satzanfang · nie mitten ins Wort ·
CapCut-Projekt statt fertigem Video (`clips/NN.mp4` + `CAPCUT.md`) · die vier
Animations-Fragen (Aussehen · Bewegung · Stelle · Sound) · „erst Konzept über
echtem Material, dann rendern" (`--konzept`) · daraus ein Skill.
🚨 **Nicht verwechseln** mit `claudealsvideoeditor.pdf` (ohne „(1)") — das ist
ein **Herr-Tech-Guide** für einen ganz anderen Weg: Reels von der KI erfinden
lassen (Nano Banana + Veo3, vier API-Anbieter, ~3–4 $ je Reel). Der passt nicht
zu Patricias Marke, weil ihre Reichweite von echten Szenen lebt.
Der Guide deckt **Sprechreels** ab; für B-Roll (ein Clip, ein Hook, kein
Schnitt) steht dort nichts.

**Schneller Alternativweg:** Submagic-MCP (`removeBadTakes` + `removeSilencePace`
+ Untertitel + Zooms in einem Aufruf). Kostet Credits, braucht eine öffentliche
Video-URL und folgt Patricias Regeln nicht. Gut als **Finisher nach** dem lokalen
Schnitt. **Nie ohne Patricias OK hochladen oder rendern.**

**Ordner:** `video/input/` · `video/transkripte/` · `video/output/` —
komplett gitignored (Repo ist public).
Doku: `scripts/videoschnitt/README.md` · Skill: `.claude/skills/videoschnitt/SKILL.md`

### /nachbau (seit 2026-09-15)

**Zweck:** Ein fremdes Reel zerlegen und seine **Bauweise** fuer Patricias eigenes
Material neu bauen. Entstanden aus der Herr-Tech-Anleitung „Video-Generator", aber
auf ihren Bestand zugeschnitten.

```bash
python scripts/nachbau/zerlegen.py <URL oder Datei> --slug <name>
```

Liefert in `nachbau/<datum>-<slug>/`: Video, Eckdaten, Szenenwechsel (ffmpeg),
**ein Standbild je Einstellung**, Transkript mit Wort-Zeitstempeln, `analyse.md`.
**Laeuft komplett lokal — kein Schluessel, keine Kosten.** Transkription ueber
faster-whisper; der OpenAI-Whisper-Schluessel aus fremden Anleitungen wird nicht
gebraucht.

🚨 **„Bau mir das nach" heisst bauen** — direkt zum Briefing, keine Analyse davor.
Eine Zerlegung gibt es nur auf Ansage. Steht als Pflicht-Block oben im Skill.

🚨 **Instagram gibt Videos nur eingeloggt heraus.** yt-dlp kommt an Chrome-Cookies
seit Version 127 nicht mehr ran, Edge nur bei geschlossenem Browser, cobalt.tools
verlangt einen Schluessel. Loesung: Erweiterung „Get cookies.txt LOCALLY" →
`scripts/nachbau/cookies.txt`, das Skript findet sie selbst. YouTube und TikTok
laden direkt.

🚨 **`nachbau/` ist gitignored** — fremdes Material, Repo ist oeffentlich. Nur das
fertige Briefing darf nach `outputs/`.

**Offen (Teil 2, Generieren):** Google AI Studio (Bilder, ~2 Rp.) und Fal.ai
(Video, ~50 Rp. je Clip). Vorhanden sind Anthropic, FFmpeg, Node 24, yt-dlp,
faster-whisper. Details: `scripts/nachbau/README.md`.

**Bei Vergleichen mit anderen Accounts:** nach **Verkaufssignalen** sortieren
(Keyword-CTA, Bio-Link auf einen Checkout, Launch-Sprache, Preise) — nie nach
Likes und Kommentaren. Der Discovery-Lauf in `scripts/apify/` bewertet nach
Hashtag-Reichweite und findet damit Influencerinnen, keine Verkaeuferinnen.

### /handy (seit 2026-09-10)

**Zweck:** Neues Foto-/Videomaterial vom Handy holen, ohne dass Patricia etwas
am PC sortieren muss. **Ein** Album auf dem Handy — `DCIM/Content-Inbox` — dort
wirft sie in der Galerie alles rein, was für Content verwendet werden soll.

`python scripts/handy/hol-content.py` holt daraus:
Videos → `video/input/` · Fotos → `context/content-assets/inbox/YYYY-MM/` ·
**Standbild je Video** → `context/content-assets/vorschau/` (damit Claude den
Inhalt sieht statt nur Dateinamen) · Bericht → `context/content-assets-inbox.md`.

**Regeln:** Auf dem Handy wird nie gelöscht oder verschoben — CrossDevice
erlaubt Schreiben und Anlegen, aber **kein Löschen** (`WinError 395`). Schon
Geholtes steht im Merkzettel `context/content-assets-inbox-log.json`, mehrfaches
Laufen schadet nicht. **Vorschaubilder wirklich anschauen**, bevor Claude sagt,
was auf dem Material drauf ist.

### Cockpit-Artifact — Content-Pipeline (seit 2026-09-10)

**Das Cockpit ist der Ort, an dem Patricia geplanten Content abnimmt.**
URL `https://claude.ai/code/artifact/eeee48d5-3e50-4cff-8047-1ec5eccbb074`,
Quelle im Repo `outputs/cockpit/mlb-cockpit.html`, Aenderungen ueber
`scripts/cockpit/patch-karussell.py` (nachvollziehbare Patches statt Handarbeit).

**Ablauf:** Claude schreibt Karussell-Vorschlaege per `Artifact write_db` in die
Sammlung `karussells` → Patricia bearbeitet sie im Cockpit (auch am Handy,
getestet) → sie gibt **erst die Texte** frei, dann mit Datum/Uhrzeit/Profil
**fuer Blotato** → sagt es im Chat → Claude liest `freigaben` und laesst
`scripts/cockpit/freigabe-zu-blotato.mjs` laufen (WordPress-Upload → Blotato-Media
→ Blotato-Post mit `scheduledTime`).

- Fotos als Slide-Hintergrund: `python scripts/cockpit/foto-ins-cockpit.py <foto> --slide <slideId>`
  erzeugt ein Dokument unter 180 KB; danach in `karussells/<carId>/bilder` schreiben.
- **Immer zuerst `--trocken`** laufen lassen.
- 🔄 **Seit 11.10.2026 gehen Sprechreels WIEDER über Blotato** (Patricia: *„doch
  sprechreels sollen auch über blotato raus"*) — Karussells + Sprechreels über Blotato,
  B-Roll und Storys postet sie selbst. ⚠️ **Offen:** Der 20:00-Task lässt `typ: "reel"`
  noch liegen und muss auf `videoart: "sprech"` umgestellt werden. Der Absatz darunter ist
  für Sprechreels überholt.
- 🚨🚨 *(abgelöst 11.10. für Sprechreels)* **Seit 25.09.2026 gehen NUR Karussells über Blotato** (Patricia: *„achtung du
  musst nur karussells einplanen"*). Auch Sprechreels postet sie selbst in der App. Der
  20:00-Task lässt jede Freigabe mit `typ: "reel"` liegen. Anlass: Ich hatte ein
  Sprechreel (`reel-kw38-mo`) eingeplant und musste den Blotato-Plan wieder löschen
  (`DELETE /v2/schedules/<id>`). ⚠️ Offen: Das Cockpit legt Sprechreels bei der Freigabe
  noch als `wartet` ab und zeigt „wartet auf 20:00“. Richtig wäre `selber-posten` wie
  beim B-Roll.
- *Vorher:* **Nur Sprechreels und Karussells gehen über Blotato** (Patricia, 16.09.2026:
  *„du musst nur sprechreels und karussells über blotato einplanen. b-roll mach ich
  wegen der musik selber“*). **Der Grund ist die Musik:** Instagram-Audio lässt sich nur
  in der App wählen, und bei einem Sieben-Sekunden-B-Roll ist die Musik der halbe
  Beitrag. Feld **`videoart`** am Reel (`sprech` | `broll`) mit Auswahl auf der
  Wochenkarte; bei `broll` legt die Freigabe `status: "selber-posten"` ab statt
  `"wartet"`, und der Einplan-Task lässt ihn damit in Ruhe.
- 🚨 **Knopf „Hab ich selbst gepostet“** auf jeder freigegebenen Karte → setzt
  `gepostet-von-hand`. **Ohne das entsteht ein Doppelpost:** am 16.09. hat Patricia das
  Dienstags-Reel von Hand über die App gepostet, die Freigabe stand aber weiter auf
  `"wartet"` — der Task hätte es um 20:00 ein zweites Mal eingeplant.
  Gesetzt mit `scripts/cockpit/patch-videoart.py`.

- 🚨 **Seit 14.09.2026: Der Freigabe-Knopf in der Wochen-Vorschau IST das Go.**
  Er legt Folien, Caption, Datum und Profil ab; der Scheduled Task
  `freigaben-einplanen-2000` zieht taeglich um 20:00 alles auf `status: "wartet"`,
  prueft trocken, plant ein und meldet per Telegram. **Kein Nachfragen im Chat.**
  Storys nie — die postet Patricia selbst. Die alte Regel „nie ohne ausdrueckliches Go"
  gilt weiter fuer alles andere (Mails, Ads, Seiten).
- Das Skript blockt Zeitpunkte in der Vergangenheit, fehlende Captions und
  mehr als 10 Folien.

Volle Doku: Abschnitt „Der Cockpit-Weg" in `.claude/skills/karussell/SKILL.md`.

🚨 **`window.open()` ist im Artifact-Rahmen blockiert — lautlos** (gefunden 16.09.2026).
Der Knopf „Im Bild-Editor bauen“ tat deshalb nichts, und weil nichts passierte, hat
Patricia nie etwas fertiggebaut und folglich nie etwas freigegeben. **Ein Link, den die
Person selbst anklickt (`<a target="_blank" rel="noopener">`), geht durch.** Dazu
`a.btn { display:inline-block; text-decoration:none }`, sonst sitzt er schief.

🚨 **„Cover bauen“ gehört in den Bild-Editor, nicht ins Reel-Studio.** Das
Reel-Studio zieht ein **Standbild aus dem Video**. Patricia will aber ein Cover aus
ihren **Shootingbildern** — wechselbares Bild, freier Text, verschiebbare Texthöhe,
wahlweise Verlauf, Unifarbe oder gar kein Verlauf. Das kann nur der Bild-Editor.
(Am 16.09. erst falsch intern verdrahtet, noch am selben Tag mit
`patch-cover-bildeditor.py` korrigiert.)

🚨 **Auf dem Reel-Cover steht ein HOOK, nicht der Beitragsname.** Patricia,
16.09.: *„auf das Reelcover muss auch ein hook. kann abgekürzter sein als im video
aber auch ein hook.“* Der erste Anlauf hat den Namen genommen („Sieben Uhr vierzig“) —
das ist eine Überschrift und zieht niemanden in ein Video. Die gekürzten Cover-Hooks
stehen in `outputs/content/KW38/cover-hooks.json`, **aus dem `hook`-Feld des Reels
gekürzt**, nichts neu behauptet. Das Skript warnt, wenn zu einem Reel keiner da ist.

**Der Beitrag geht beim Sprung nicht verloren** — das war der ursprüngliche Einwand
und er ist ausgeräumt: `scripts/cockpit/reel-cover-entwuerfe.py` legt **jedes Reel als
Reel-Cover und jedes Karussell als Folienfolge** in `daten/entwuerfe` der
Bild-Editor-Datenbank. Drüben stehen sie unter „Aus deiner Planung“. Das Reel-Studio
bleibt für den Fall, dass wirklich ein Videobild gewollt ist.

Gesetzt mit `scripts/cockpit/patch-wochenkarte-bauen.py` (wiederholbar, arbeitet gegen
die **Live-Fassung** — `outputs/cockpit/mlb-cockpit.html` war bis dahin ab Zeile 3126
auseinandergelaufen und ist jetzt wieder gleich).

🚨 **Vor jedem Publish `node --check` über das eingebettete Skript laufen lassen.**
Beim ersten Anlauf hat ein deutsches Anführungszeichen die JS-Zeichenkette beendet —
die ganze Seite wäre tot gewesen. In JS-Strings als `„` und `“` schreiben.

### Texte pruefen: `scripts/cockpit/texte-pruefen.py` (seit 2026-09-16)

🚨 **Eine Blacklisten-Pruefung aus dem Gedaechtnis prueft das, woran man
gerade denkt.** Am 16.09. habe ich mit einem selbstgetippten Muster
`Nicht .{0,40}, sondern` geprueft und **1 von 4** Treffern gefunden. Deshalb steht
die Liste aus `context/ki-phrasen-blackliste.md` jetzt als Code.

```bash
python scripts/cockpit/texte-pruefen.py            # alle
python scripts/cockpit/texte-pruefen.py --nur reel-kw38-mi
```

**Vier Tarnungen, die einzeln nachgeruestet werden mussten** — jede hat beim ersten
Lauf einen echten Fund verdeckt:

| Tarnung | Beispiel aus dem Bestand |
|---|---|
| über die **Satzgrenze** | „Nicht weil etwas war. **Sondern** weil …“ |
| Kontrast **ohne** „sondern“ | „Die meisten scheitern nicht am Wissen. Sie scheitern daran …“ |
| mit **Doppelpunkt** statt Punkt | „… war nicht mehr Fleiss: Es war die Frage …“ |
| „Stell dir … vor“ **getrennt** | „Stell dir zwei Zettel am schwarzen Brett vor.“ |

**Jede neue Regel zuerst an einem bekannt fehlerhaften Satz testen, und dazu an
einer Gegenprobe, die NICHT anschlagen darf.** Ein Muster, das alles findet, ist
genauso wertlos wie eins, das nichts findet — nach dem dritten Fehlalarm liest
niemand mehr hin.

🚨 **Die drei Formate sind verschieden gebaut.** Eine Story hat keine Caption
und keinen Hook, sondern `frames`; ein Karussell hat den Hook in Folie 1, nicht im
Feld `hook`. Ohne diese Unterscheidung meldet der Pruefer **17 Fehlalarme**.

**Was er nicht kann:** der 🛑 Beitrags-Check (berührt es · nimmt sie etwas Konkretes
mit · Grund zu speichern · Grund zu kommentieren · nur von ihr) und der Hook-Check bleiben
Lesearbeit. Das Skript sagt das am Ende jedes Laufs selbst.

### 🚨 Zwei stille Fehler in der Freigabe (gefunden und behoben 16.09.2026)

Patricia: *„wenn ich es jetzt um 19.50 freigebe, wirds dann noch gepostet? nicht
oder?“* — Sie hatte recht, und beide Ursachen waren auf der Karte **unsichtbar**.

**1 · Die Uhrzeit stand nirgends.** Auf der Wochenkarte liessen sich nur Datum und
Profil setzen; die Zeit kam aus `bl.zeit || (art === "reels" ? "18:00" : "07:30")`.
Der Einplan-Task läuft um **20:00**, und Blotato lehnt Zeitpunkte in der Vergangenheit
ab — **ein am selben Tag freigegebenes Reel konnte damit nie rausgehen.** Nicht
manchmal, nie. Und die Freigabe meldete trotzdem „Freigegeben und abgelegt“.

Behoben mit `scripts/cockpit/patch-postzeit.py`: **Zeitfeld neben dem Datum** ·
Vorgabe nach den echten Posting-Zeiten (Reel Mentoring **21:00**, Reel doTERRA
**21:30**, Karussell **07:30** — alle nach dem 20:00-Lauf) · und eine **Warnung**,
wenn der Zeitpunkt schon vorbei ist, mit `status: "zeitpunkt-vorbei"` statt
`"wartet"`, damit der Task es überspringt statt daran zu scheitern.

**2 · Das Profil auf der Karte war immer „Mentoring“.** Die Auswahl las nur
`blotato.profil` — das ist bei fast allen Beiträgen leer. Das **eigene Feld `profil`
des Beitrags wurde ignoriert**, also standen auch die neun doTERRA-Reels auf
Mentoring. Wer so freigibt, plant sie **aufs falsche Konto**. Jetzt über
`kartenProfil(o)`: `blotato.profil` → `o.profil` → `"mentoring"`.

**Die Lehre:** Was beim Freigeben entscheidet, muss auf der Karte **stehen**. Ein
Vorgabewert tief im Code ist kein Standard, sondern eine unsichtbare Annahme — und
eine Erfolgsmeldung, die nur sagt „abgelegt“, verdeckt jedes Mal, dass nichts
passieren wird.

🚨 **Blacklisten-Prüfung über Satzgrenzen hinweg.** Das Muster
`Nicht .{0,40}, sondern` fand **1 von 4** Treffern — „Nicht weil etwas war. **Sondern**
weil …“ steht als zwei Sätze da. Richtig ist
`[Nn]icht[^.!?]{0,80}[,.]\s*[Ss]ondern`. Drei Captions waren betroffen und sind
korrigiert.

### Die Clip-Ablage im Reel-Studio (seit 2026-09-17)

**Patricia:** *„ich will die clips ändern können, wie ich auch die bilder ändern
kann“* · *„kann ich sie auch selber rauswerfen und ersetzen?“*

Ein Streifen im Reel-Studio, gebaut wie der Foto-Streifen: **antippen** setzt den
Clip ans Reel, **✕** wirft ihn aus der Ablage, **+ eigener Clip** lädt einen dazu.

| | |
|---|---|
| **Die Datei** | Anhang am Artifact (`assets`), ausgeliefert unter `/_blob/<id>` |
| **Die Liste** | `daten/clips` (`db`) — **das ist das Verzeichnis** |

🚨 **`assets.list()` taugt nicht als Quelle** — dort stehen Grösse und Typ,
aber keine Namen. Wer daraus die Auswahl baut, zeigt eine Wand aus Kennungen.

🚨 **Der gespeicherte Wert kommt in zwei Formen.** Die Seite legt die blosse
Liste ab, der Abgleich und die Datenbank das ganze Dokument `{clips: […]}`. Wer nur
eine Form annimmt, bekommt `clips.forEach is not a function` — und weil der Fehler
mitten im Zeichnen kommt, fehlt danach der halbe Reiter. Deshalb `clipListe(x)`,
die beides annimmt. **Genau das hat die lokale Testfassung gefunden**, bevor es live
ging.

🚨 **Löschen ist endgültig und gilt für alle Ansichten.** Der Knopf prüft
vorher, ob ein Beitrag den Clip benutzt, und verweigert dann — sonst zeigt eine
Wochenkarte auf eine Datei, die es nicht mehr gibt. `assets.delete` und das
Entfernen aus der Liste passieren in derselben Handlung.

**20 MiB je Datei** (SVG 2 MiB). Ein Handy-Video von 40 Sekunden reisst das; der
Uploader sagt es vorher. Startbestand: 6 Clips, auf B-Roll-Länge geschnitten
(1–12 MB je Stück) — `scripts/cockpit/patch-clipstreifen.py`.

**Das Vorschaubild kommt aus dem Video selbst** (`<video preload="metadata">`
zeigt das erste Bild) — kein zweiter Anhang je Clip.

### „Was zu tun ist" und der Rückweg fürs Video (seit 2026-09-18)

**Patricia:** *„es hat bei vielen reels kein reel drin. aber auch keine notizen,
dass ich noch was liefern muss. wo sehe ich, was zu tun ist und wie liefere ich
die reels nach?"*

Sie hatte recht, und es waren **drei Lücken, jede für sich unsichtbar**:

🚨 **Das Feld `hinweis` wurde nie gespeichert und nie gelesen.** In den
hochgeladenen Beiträgen stand „⚠️ VIDEO FEHLT" — das Feld fehlte aber in der
Feldliste von `saveReel` *und* beim Lesen. Also war es nirgends sichtbar und wäre
beim nächsten Speichern verschwunden. **Ein Hinweis, den niemand sieht, ist kein
Hinweis.** (Dieselbe Falle wie am 16.09. bei `kommentar` und `profil` — die feste
Feldliste in `saveReel` ist die Stelle, an der neue Felder still verloren gehen.)

🚨 **Das Sprechskript stand nur im Reel-Studio**, nicht auf der Wochenkarte. Genau
dort, wo sie das fehlende Video bemerkt, war nicht zu sehen, was sie sagen soll.

🚨 **Es gab keinen Weg, ein gedrehtes Video von der Karte aus abzugeben.** Die
Clip-Ablage kann das, aber nur im Reel-Studio und nur über den Umweg
„hochladen → Reel öffnen → antippen".

**Was jetzt da ist** (`scripts/cockpit/patch-was-fehlt.py`, wiederholbar):

| | |
|---|---|
| **Aufgaben-Block** oben in der Wochen-Vorschau | alles Offene nach Tag sortiert, getrennt in **von dir** (orange) und **von mir** (petrol), mit Zählung oben |
| **Fehlt-Zeile je Karte** | rot = sie ist dran, petrol = Claude ist dran, mit Satz dazu, was zu tun ist |
| **Sprechtext aufklappbar** | bei Sprechreel ohne Video, direkt auf der Karte |
| **Knopf „Video hochladen"** | links unter dem Cover, bis 20 MiB, hängt die Datei sofort ans Reel |

🚨 **Die Arbeitsteilung steht in `wasFehlt()` und ist fest:** B-Roll ohne Video
ist **Claudes** Aufgabe (wird aus vorhandenem Material gebaut), ein Sprechreel
ohne Video ist **Patricias** (Sprechtext steht auf der Karte). Ohne diese Trennung
wartet jede auf die andere — genau das war seit KW38 der Fall.

**Zwei Wege, ein Video nachzuliefern:**
1. **Fertiger kurzer Clip** → Knopf auf der Karte. Sofort dran, sie sieht ihn
   direkt in der Vorschau.
2. **Rohmaterial mit Versprechern** → Handy-Album `DCIM/Content-Inbox`, dann holt
   `scripts/handy/hol-content.py` es nach `video/input/` und `/videoschnitt`
   macht den Rohschnitt. 🚨 **Das läuft nicht von selbst** — das Skript läuft auf
   ihrem Rechner und braucht eine offene Session. Sie muss es also ansagen.

**Leere Entwürfe („Neues Reel" ohne Hook, Caption und Folien) stehen nicht in der
Aufgabenliste.** Beim ersten Lauf waren es drei Phantom-Aufgaben ganz oben.

### Cover direkt auf der Wochenkarte (seit 2026-09-19)

**Patricia:** *„kann ich die cover bitte nicht direkt in der wochenvorschau
machen? da lade ich ja auch das video runter"*

Sie hat recht — Video holen, Cover bauen und freigeben gehören zu **einem**
Beitrag. Der Sprung in den Bild-Editor war ein Werkzeugwechsel mitten im
Handgriff. Jede Reel-Karte hat jetzt einen aufklappbaren Block **„Cover bauen"**:
Vorschau · Hook und Unterzeile als Felder · Regler für Höhe und Schriftgrösse ·
Streifen mit den zwölf Shootingbildern · eigenes Foto · Abdunkeln · **Cover
speichern** (PNG).

**Das meiste war schon da, nur nie auf der Karte.** `renderReelCanvas()`
zeichnet das Cover seit jeher (Reel-Studio), und `coverhook`, `coverunter`,
`texty`, `textskala`, `scrim`, `coverfarbe` hängen längst am Reel. Gefehlt haben
**die Fotos** und **die Bedienung** — nicht die Mechanik. Deshalb zeichnet der
Block mit **derselben Funktion**; zwei Zeichnungen desselben Covers wären beim
nächsten Umbau auseinandergelaufen.

🚨 **Das Foto wird beim Anklicken sofort abgelegt** (`saveImage`), nicht erst
beim Herunterladen. Sonst stünde auf der Karte weiter „Noch kein Cover" und die
Blotato-Freigabe ginge ohne Titelbild raus.

🚨 **Text-Vorgabe 68 % statt Mitte.** Bei einem Hochformat-Porträt sitzt das
Gesicht im oberen Drittel — ein Block in der Mitte legt sich genau darüber. Beim
ersten Render war das sofort sichtbar. Die Zeichnung begrenzt nach unten ohnehin
gegen die Caption-Zone, tiefer als erlaubt kann es also nicht rutschen.

Die Fotos liegen als veröffentlichte Dateien an **beiden** Artifacts
(`assets/s01.jpg`–`s12.jpg`). Skript: `scripts/cockpit/patch-cover-auf-der-karte.py`.

### Bildvorschlag je Cover (seit 2026-09-19)

**Patricia:** *„ich will, dass du mir für jedes reel ein standbild aus meinem
shooting mit dem hook drauf vorschlägst. und bei bedarf soll ich das bild ändern
können. sowie auch den hooktext anpassen, vergrössern, verkleinern, verschieben."*

Bisher lud „Aus deiner Planung" nur den **Text**. Das Bild blieb auf
`lounge.jpg` — dem Vorgabewert der Seite. Es lag also bei jedem Cover derselbe
Hintergrund, und der Vorschlag war in Wahrheit keiner.

**Jetzt bringt jeder Cover-Entwurf `foto`, `fotoText`, `farbe`, `grad`, `fs` und
`pos` mit.** Alles nur als Startwert — Foto über den Streifen, Text im Feld,
Grösse und Höhe über die Regler unter dem Bild.

Zwölf weitere Shootingbilder als `assets/s01.jpg`–`s12.jpg`
(`scripts/cockpit/patch-cover-fotovorschlag.py`). Vorher waren es neun, davon
vier schwarzweiss — zu wenig für vierzehn Cover.
Zuordnung: `scripts/cockpit/cover-fotos-zuordnen.py`.

🚨 **Das Bild sagt mit.** Beim ersten Lauf stand die lachende Pusteblume auf
*„Das wird schon wieder, du hast halt vier Kinder." Hat es nicht.* — einem
Schmerz-Hook. Deshalb ist **ruhig die Vorgabe**; nur wenn der Text erkennbar
nach vorne zeigt (geändert · besser · kostet nichts · endlich), darf eine
heitere Aufnahme darunter. Andersherum wäre es riskanter: ein heiterer Hook auf
einem ruhigen Bild stört niemanden, umgekehrt schon.

🚨 **Ein zu enger Vorrat ist derselbe Fehler wie ein falsches Bild.** Der erste
Versuch teilte je Profil 3 ruhige / 3 heitere — und weil fast jeder Hook ein
Schmerz-Hook ist, blieben drei Bilder für zwölf Cover und wiederholten sich an
Folgetagen. Gesperrt sind jetzt nur die zwei wirklich heiteren Aufnahmen.

🚨 **Zuordnung gierig, nicht reihum.** Reihum scheitert, sobald die Zahl der
Cover pro Tag wechselt (3 · 3 · 1 · 3 · 2). Gierig heisst: das erlaubte Bild
nehmen, das am längsten nicht dran war und weder heute noch am **kalendarischen**
Vortag vorkommt. *Kalendarisch* ist der Punkt — der 16. und der 18. galten erst
fälschlich als Folgetage und haben den Vorrat ohne Grund eingeengt.

🚨 **Verlauf 62 statt 76.** Bei 76 lag ein oranger Schleier über dem ganzen
Foto, und von den Shootingbildern blieb kaum etwas übrig. Am Standbild
entschieden, nicht am Zahlenwert.

**Kein Petrol auf einem Cover** — welche Beiträge Lead-Posts sind, steht im
Entwurf nicht drin, und dort ist Petrol verboten. Wo die Unterscheidung fehlt,
gilt die strengere Regel. Es wechseln Dunkelblau und Orange.

### 🚨 Zwei Generationen derselben Beiträge (gefunden 2026-09-18)

**Patricia:** *„ich habe da teilweise festgestellt, dass komische sätze stehen in
den vorbereiteten slides. die gar keinen sinn ergeben."*

In `daten/entwuerfe` des Bild-Editors lagen **zwei Generationen** derselben
KW38-Beiträge nebeneinander — eine ältere aus einem Lauf mit **umschriebenen
Umlauten**, und mit ihr kamen zusammengekürzte Sätze:

| | alt (`kw38-kar-fr-a`) | neu (`kar-kw38-kar-fr-a`) |
|---|---|---|
| Folie 1 | „Fuenf Beitraege ohne ein einziges Produkt." | „Fünf Beiträge, die du posten kannst, ohne ein Produkt zu zeigen." |
| Folie 7 | „Zu klein heisst nur:" + „du kannst es ohne Nachdenken." | „Wenn der Satz sich zu klein anfühlt, ist er meistens richtig." |

🚨 **In einem Auswahlfeld mit über dreissig Zeilen sieht man das nicht.** Beide
standen untereinander, fast gleich benannt — man erwischt die halbe Zeit die
alte. Genau das ist passiert. Der Umbau auf **Tag zuerst, dann Entwurf** hat das
Problem sichtbar gemacht, weil plötzlich zwei Einträge am selben Tag standen.

`scripts/cockpit/entwuerfe-pruefen.py` prüft seitdem drei Dinge und entfernt mit
`--putzen` die kaputte Generation: umschriebene Umlaute · Doppelte am selben Tag ·
Sätze, die über `text` und `unter` zerrissen sind. Befund: **6 von 64 entfernt**,
die Beiträge im Cockpit selbst waren sauber.

🚨 **Die Ausnahmeliste ist bei dieser Prüfung die halbe Arbeit.** „bauen",
„dauert", „Frauen", „heute", „zuerst", „Abenteuer" und **„unbequemer"** enthalten
ae/oe/ue völlig zu Recht — „unbequemer" war beim ersten Lauf über die
Cockpit-Beiträge der einzige Treffer, und er war falsch. Jede Regel gegen einen
bekannt fehlerhaften Satz **und** eine Gegenprobe testen, die nicht anschlagen
darf.

Ebenso bewusst **nicht** automatisch gelöscht: zwei Einträge am selben Tag mit
ähnlichem Namen, bei denen keiner umschriebene Umlaute hat — „Letzter Bestelltag
— Sofa" und „— Handy" sind zwei echte Varianten und liegen bei 67 % Namensdeckung.

### Die Wochen-Vorschau ist der eine Ort (Tagesplan gestrichen, 2026-09-19)

**Patricia:** *„kannst du mir bitte den tagesplan streichen? ich will im wochenplan
für jeden tag einen button wo ich die verschiedenen varianten pro tag umstellen
kann."* — und nachgeschoben: *„wochenvorschau passt schon. da müssen einfach noch
die verschiedenen varianten rein."*

Der **Tagesplan vom selben Morgen ist raus.** Er war eine zweite Ansicht auf
dieselbe Sache; zwei Ansichten auf dieselben Daten laufen beim nächsten Umbau
auseinander, und man sucht jedes Mal, in welcher man gerade steht.

**Fester Rhythmus, beide Profile** (Patricias Entscheid): Mo · Mi · Fr Reel,
Di · Do Karussell. Der Tag sagt das Format, das spart pro Tag eine Frage. Passt
ein Beitrag nicht zum Tag, steht es als Hinweis auf dem Platz — gesperrt ist
nichts.

| | |
|---|---|
| **Zehn Plätze** | 5 Tage × 2 Profile, je Platz ein Beitrag als volle Karte |
| **Wechseln** | Varianten darunter: was noch am selben Tag liegt, dann der Vorrat. Antippen legt die Variante drauf, die bisherige fällt in die Ideenliste |
| **Anderes Datum** | Datumsfeld auf der Karte, übernimmt und setzt eine bestehende Freigabe zurück |
| **Löschen** | endgültig, in zwei Klicks (Patricias Entscheid gegen „ab in die Ideenliste") |
| **Unten** | „Was wann rausgeht" über **alle** Wochen · „Ideenliste" mit Datumsfeld je Zeile |

🚨 **Zwei Soll-Zeilen je Profil, nicht eine.** Oben stehen `3 Reels · 2 Karussells`
**und** `3 Lead · 2 Reichweite`. Die Formatzahl sagt über Konversion nichts — wie
viele Beiträge in einen Funnel führen, schon. Ohne die zweite Zeile hängt im
Cockpit eine Zahl, die nicht die Zahl ist, auf die es ankommt.

🚨 **Lead oder Reichweite wird abgelesen, nicht gepflegt.** Ein Stichwort in
Grossbuchstaben im CTA macht den Beitrag zum Lead-Post. Ein neues Feld wäre
sauberer und würde nie gepflegt; eine Ableitung, die auf **jeder Karte sichtbar
steht**, ist ehrlicher als eine Angabe, der man nicht ansieht, dass sie fehlt.
Der Satz unter der Bilanz sagt das ausdrücklich.

🚨 **Kein `confirm()` und kein `prompt()`.** Im Artifact-Rahmen kann ein Modal
blockiert sein — lautlos. Ein Löschknopf, der nichts tut, ist schlimmer als
keiner. Deshalb Löschen in zwei Klicks (der zweite verfällt nach acht Sekunden)
und ein eingeblendetes Datumsfeld statt einer Eingabeaufforderung.

🚨 **Neu einplanen setzt Freigabe und Blotato-Status zurück.** Sonst lässt der
20:00-Lauf den Beitrag liegen, weil er als erledigt gilt, und sie wartet auf
einen Post, der nie kommt.

**Die Woche oben zeigt nur eine Woche** — deshalb stehen unten alle Termine über
alle Wochen. Sonst wäre der Umbau ein Verlust: vorher war alles auf einer Seite.

Skript: `scripts/cockpit/patch-wochenplan-varianten.py` (wiederholbar, prüft mit
`node --check` und mit einer Gegenprobe, dass kein Tagesplan-Rest übrig bleibt).
🗃 `patch-tagesplan.py` bleibt als Herkunft liegen, läuft aber ins Leere.


### Reiter „Fertig zum Posten" (seit 2026-09-18)

**Patricia:** *„kannst du noch einen reiter machen fertig zum posten, dass ich
sehe, was ich direkt freigeben kann?"*

Die Wochen-Vorschau zeigt alles nebeneinander — wer freigeben will, scrollt sich
durch die halbfertigen durch. Dieser Reiter zeigt nur, was schon steht:

| Gruppe | Was drin ist |
|---|---|
| **Kann raus** | Feed-Beitrag, nichts fehlt, Zeitpunkt in der Zukunft — volle Karte mit Freigeben-Knopf |
| **Fertig, aber das Datum ist durch** | alles steht, nur der Zeitpunkt ist vorbei |
| **Storys — die postest du selbst** | fertige Storys, Zeitpunkt in der Zukunft |
| **Schon freigegeben** | kompakte Liste mit Stand (wartet auf 20:00 · selbst gepostet · B-Roll) |

**Die Zahl am Reiter ist die Antwort auf „was kann raus"** und zählt nur Feed.

🚨 **Storys gehören nicht in dieselbe Zahl.** Beim ersten Lauf stand „Kann raus:
27" da — darin steckten 20 Storys, die nie über Blotato gehen. Feed freigeben und
Story posten sind zwei verschiedene Handlungen; in einer Zahl vermischt ist die
Zahl grösser als die Arbeit dahinter. Nach der Trennung: 17 Feed · 10 Storys.

🚨 **„Datum ist durch" ist eine eigene Gruppe, kein Randfall.** Ein Beitrag mit
vergangenem Zeitpunkt sieht fertig aus, die Freigabe meldet „abgelegt", und der
20:00-Lauf überspringt ihn — weil Blotato nichts in der Vergangenheit annimmt.
Beim ersten Lauf waren das **9 von 26** fertigen Beiträgen.

Gebaut aus **denselben Karten** wie die Wochen-Vorschau (`wochenKarte`), nicht als
zweite Ansicht — sonst wäre es beim nächsten Umbau auseinandergelaufen. Dafür ist
die Beitragsliste als `alleBeitraege()` herausgezogen.
Skript: `scripts/cockpit/patch-fertig-tab.py`.

### Die Kommentarzeile — der Rückweg von der Karte zu Claude (seit 2026-09-16)

**Patricia:** *„wäre es auch möglich eine kommentarzeile reinzutippen, die du dann
ausliest? wenn mir z.B. das video nicht gefällt oder du die caption neu schreiben
sollst? und das automatisch siehst anpasst und mir wieder aktualisierst und auf
telegram schreibst, dass der beitrag aktualisiert wurde und zur freigabe steht?“*

Jede Karte in der Wochen-Vorschau hat jetzt eine Zeile **„Was soll ich ändern?“** plus
Knopf **„An Claude“**. Vier Felder am Beitrag:

| Feld | wer schreibt | Inhalt |
|---|---|---|
| `kommentar` | Patricia | was geändert werden soll |
| `kommentarStand` | Cockpit | wann (ISO) |
| `kommentarErledigt` | Claude | wann eingearbeitet (ISO) |
| `kommentarAntwort` | Claude | was tatsächlich geändert wurde |

🚨 **Offen/erledigt wird über die Zeitstempel entschieden, nie über ein
Häkchen** — sonst bleibt ein zweiter Kommentar zum selben Beitrag unbemerkt, weil der
erste schon als erledigt gilt. Der Kommentar wird beim Einarbeiten **nicht gelöscht**;
er bleibt als Verlauf stehen.

Abgeholt vom Scheduled Task **`kommentare-einarbeiten`** (täglich **19:30**, also eine
halbe Stunde vor `freigaben-einplanen-2000` — damit ist alles eingearbeitet, bevor der
Einplan-Task die Freigaben abholt). Auftrag: `reference/scheduled-task-kommentare.md`.
Gebaut mit `scripts/cockpit/patch-kommentarzeile.py`.

**Drei Grenzen sind im Auftrag verdrahtet:** der Task setzt **nie** `textfrei`
(Freigeben bleibt ihr Klick), plant **nichts** ein, und löscht **nichts**. Was sich
nicht per Text lösen lässt — „Video passt nicht“ — wird nicht durch etwas anderes
ersetzt, sondern in `kommentarAntwort` beantwortet, samt Sprechtext für den neuen Dreh.

**Lokal prüfbar:** `testfassung-bauen.py` legt seit 16.09. auch **Reels, Karussells und
Storys** aus `outputs/cockpit/inhalte-roh/` in den `localStorage` (`reelliste` +
`rl-<id>`, `karliste` + `kar-<id>`, `storyliste` + `st-<id>`). Vorher war die
Wochen-Vorschau lokal leer — ausgerechnet die Ansicht, an der am meisten geändert wird.

### Sprechen statt tippen — der Rückkanal am Cockpit-Bot (seit 2026-09-24)

**Anlass:** eine Werbeanzeige, die Patricia auf dem Handy mitgeschnitten hat. Darin
spricht jemand seinem Dashboard eine Sprachnotiz aufs Handy und bekommt eine Antwort
aus den eigenen Zahlen. Bis dahin nahm der Cockpit-Bot **nur feste Befehle**
(`/cockpit`, `/news`) — wer ihm etwas schrieb, bekam keine Antwort. Die Nachricht fiel
ins Leere, und genau das war die Lücke: sie sieht unterwegs, dass ein Beitrag noch
nicht frei ist, und kann nichts tun.

```
Sie:  „was steht heute an?"              -> Antwort aus Cockpit-Stand + Notion
Sie:  🎤 „bei Mittwoch die Caption neu"   -> Auftrag, Claude arbeitet ihn 19:30 ein
```

| Datei | Job |
|---|---|
| `scripts/cockpit-bot/rueckkanal.py` | Sprache → Text · Absicht deuten · Antwort bauen · Auftrag ablegen |
| `scripts/cockpit-bot/patch-rueckkanal.py` | hängt beides in `bot.py` ein (wiederholbar, prüft mit `ast.parse`) |
| `scripts/cockpit/stand-fuer-bot.py` | die Brücke: schreibt `cockpit-stand.json` neben den Bot |

🚨 **Der Bot kommt nicht an die Artifact-Datenbank.** Er läuft als Worker auf
Railway; die Beiträge liegen im Artifact und sind nur über `ArtifactData` erreichbar,
also nur aus Claude Code heraus. **Es gibt keinen Schlüssel, der das ändert — es gibt
schlicht keine Schnittstelle dorthin.** Deshalb die Brücke: Claude holt die Beiträge
nach `outputs/cockpit/inhalte-roh/`, `stand-fuer-bot.py` macht daraus einen Auszug,
und der liegt **im Repo neben dem Bot**, wo Railway ihn mitdeployt.

🚨 **Der Auszug trägt ein Datum, und der Bot sagt es, sobald er zwei Tage alt ist.**
Ein alter Stand sieht aus wie ein aktueller und ist deshalb gefährlicher als keiner.

🚨 **Der Bot meldet nie „erledigt".** Er nimmt entgegen, sonst nichts — er setzt
kein `textfrei`, plant nichts ein und löscht nichts. Eine Bestätigung, die nach
Erledigung klingt, ist genau der Fehler, an dem am 16.09. die Freigabe gescheitert ist.

🚨 **Ohne Datum ist nichts eine Aufgabe** — weder offen noch fertig. Beim ersten
Test standen fünf „Sprechreel drehen" ganz oben, die in Wahrheit nur nicht
ausgewählte A/B-Varianten aus der Freitagsproduktion waren. Eine Aufgabe, die keine
ist, kostet Vertrauen in die ganze Liste. Die Aufteilung **wer ist dran** ist
dieselbe wie `wasFehlt()` im Cockpit und darf nicht auseinanderlaufen: B-Roll ohne
Video ist Claudes Sache, ein Sprechreel ohne Video ihre.

🚨 **Der Rückkanal-Handler wird ZULETZT angemeldet und schliesst Befehle aus**
(`filters.TEXT & ~filters.COMMAND`). Sonst verschluckt er `/cockpit`, und die festen
Befehle antworten nie mehr.

⚠️ **Offen: Sprachnotizen brauchen `OPENAI_API_KEY`** — der wurde am 13.09.2026
gewechselt und liegt nicht mehr bei Railway. Ohne ihn **antwortet der Bot ehrlich**
und bittet um Text, statt so zu tun, als hätte er zugehört. **Text funktioniert heute,
ohne neue Abhängigkeit.**

### Was Instagram misst — im Reiter „Zahlen & Ziele" (seit 2026-09-24)

Bis dahin war „Zahlen & Ziele" reine Handarbeit: Umsatz, Verkäufe und
Listenwachstum trug Patricia selbst ein. Die **gemessenen** Zahlen holt
`scripts/instagram-insights/holen.py` längst über die Meta Graph API — sie endeten
aber in einer Markdown-Datei, die niemand aufmacht.

```bash
python scripts/instagram-insights/holen.py     # Zahlen holen
python scripts/cockpit/zahlen-bauen.py         # -> instagram-zahlen.json
# danach: Artifact write_db -> Sammlung "daten", Dokument "instagram"
```

🚨 **Die rote Warnung ist der eigentliche Wert.** Eine Zahl ohne Datum daneben
sieht immer aktuell aus. Ab drei Tagen steht der Block rot da und nennt den Befehl
zum Nachholen — sonst entscheidet sie auf einem Stand von letzter Woche.

🚨 **Median UND Mittelwert.** Ein Reel mit 1'328 Aufrufen zieht den Schnitt auf 272,
während der Median bei 182 liegt. Wer nur den Schnitt zeigt, behauptet eine
Reichweite, die die normale Woche nie hat. Nichts wird hochgerechnet, und die beiden
Konten bleiben getrennt — bei rund 2'000 gegen rund 60 Follower wäre ein gemeinsamer
Wert irreführend.

### 🚨 Ein zweites Dokument darf nie heissen wie ein bestehendes Feld

Der Instagram-Block hiess beim ersten Anlauf `daten/zahlen` und legte im Browser
`mlb:zahlen` ab. **`state.zahlen` ist im Cockpit aber schon Patricias händische
Umsatz-Tabelle — ein Array.** Das Objekt hat sie überschrieben, `renderZahlen`
stürzte mit `state.zahlen.slice is not a function` ab, **der ganze Reiter war tot**
und der Zähler in der Leiste verschwand.

Gefunden hat das die **lokale Testfassung** (`scripts/cockpit/testfassung-bauen.py`),
bevor es live ging. Umbenannt auf `daten/instagram` · `igzahlen` · `mlb:ig-zahlen`.

**Vor jedem neuen `daten/<name>` einmal gegen die bestehenden Namen prüfen** — die
Liste steht in `DOC_KEYS` und in den `lsGet`-Aufrufen ganz unten in `mlb-cockpit.html`.
Ein Name, den es schon gibt, zerstört nicht die neue Ansicht, sondern die alte.

### Notion ablösen — Reiter „Gepostet & Analyse" (seit 2026-09-24)

**Patricias Ziel:** *„ziel für mich wäre, dass ich notion ablösen kann. also auch
gepostete beiträge sehen würde mit der analyse im anschluss […] eigentlich jedes
einzelne blatt, also nicht genau so benannt wie in notion aber in der vision dahinter"* —
und die Grenze dazu: *„ja für ds private behalte ich notion vorerst. aber ich will nicht
alles separat pflegen"*.

**Die Landkarte über alle 25 geschäftlichen Notion-Blätter:**
`plans/2026-09-24-notion-abloesen.md`. Privat (Haushalts-Liste, Tagesplaner-Privatteil,
Garten) bleibt in Notion und wird nicht angefasst.

🚨 **Die Anforderung ist nicht Vollständigkeit, sondern: jedes Feld hat genau einen
Ort.** Wo beides gepflegt werden müsste, wird eine Seite stillgelegt — nie beides
synchron gehalten. Zwei Ansichten auf dieselben Daten laufen beim nächsten Umbau
auseinander (siehe Tagesplan, gestrichen 19.09.).

```bash
python scripts/instagram-insights/holen.py     # Zahlen holen
python scripts/cockpit/gepostet-bauen.py       # -> gepostet.json
# danach: ArtifactData set -> Sammlung "daten", Dokument "gepostet"
```

**Sieben von neun Spalten der Notion-Ansicht „Analyse" fallen als Handarbeit weg** —
Reichweite, Gespeichert, Gefällt mir, Kommentare, neue Follower, URL und Datum kommen
aus der Meta Graph API. Ihre Eingabe bleiben **Bewertung** und **Fazit**, dazu die vier
Einordnungsfelder Content-Säule · Überthema · Produkt · Launch-Phase.

🚨 **Die Auswahllisten sind aus Notion abgeschrieben, nicht erfunden** — Content-Säulen
`Persönlichkeit / Inspiration / Expertise` (Soll 35/35/30), die sechs Überthemen, die
fünf Launch-Phasen. Sie stehen als `FELDER` in `gepostet-bauen.py` und reisen **mit den
Daten** ins Cockpit; im Seitencode steht keine Kopie, die nachgezogen werden müsste.

🚨 **Das Archiv wächst, die API-Antwort nicht.** Die Graph API gibt die letzten 25
Beiträge. Wer nur den jüngsten Abzug liest, verliert alles Ältere — genau das konnte
Notion besser. Deshalb werden **alle** Abzüge in `outputs/instagram-insights/` gelesen
und je Beitrag der zuletzt gesehene Stand behalten; beim ersten Lauf waren das **27
Beiträge aus 3 Abzügen**. Je Beitrag steht dabei, von wann seine Zahlen sind — ein Reel
vom Montag hat am Dienstag mehr Reichweite.

🚨 **Zwei Dokumente, nicht eins.** `daten/gepostet` gehört dem Abgleich und wird ersetzt;
`daten/gepostet-notizen` gehört Patricia. Der Abgleich darf es **nie** schreiben —
dasselbe Muster wie `daten/produkt-details`.

🚨 **Die Rate wird auf die Reichweite gerechnet, nicht auf die Follower.** Bei rund
2'000 gegen rund 60 Follower wäre die Follower-Rate zweimal etwas anderes. Interaktionen
je erreichte Person macht beide Profile vergleichbar. Richtwert 1–3 %.

**Erster Befund aus den echten Daten:** der stärkste Beitrag (407 Reichweite, 2,46 %)
beginnt mit einer **Frage**; acht Beiträge mit „Folge mir, wenn…" liegen alle unter
1,8 %. Das bestätigt [[feedback_KRITISCH-frage-in-zeile-eins]] an gemessenen Zahlen.

**Drei Stufen, nicht eine** (seit 24.09.2026, auf Patricias Nachfrage *„da müssen wir
aber irgend einen mechanismus einbauen mit beiträgen, die mega performt haben"*):

| Stufe | Bedingung | Was passiert |
|---|---|---|
| **ausgereift** | ab 7 Tagen | zählt erst jetzt in den Median |
| **gut gelaufen** | über eigenem Median **und** (1,4× Median oder ≥1,5 % Rate) | Stern auf der Karte |
| **eingeschlagen** | ab 2,5× Median oder ≥2,5 % Rate | eigener Block ganz oben, mit Vorschlägen |
| **kann wieder raus** | gut gelaufen **und** ≥28 Tage her | Knopf „Nochmal bringen" |

🚨 **Ein Einschlag ist kein Recycling-Fall, und die 28-Tage-Sperre gilt dort nicht.**
Sie schützt davor, denselben Beitrag zu früh zu wiederholen — einen Gedanken in einem
anderen Format neu zu bauen ist kein Wiederholen.

🚨 **Reichweite und Reaktion sind zwei verschiedene Funde.** Die beiden Einschläge im
Bestand (1'328 und 892 bei Median 170) hatten eine Rate von **0,45 %** — viele Fremde
haben es gesehen, kaum jemand reagiert. Daraus folgt etwas anderes (Serie, zweites
Format, Anzeige) als aus einem Beitrag, auf den die eigenen Leute antworten (Lead-Post
mit Keyword). Der Block sagt deshalb die Art dazu und gibt je Art andere Vorschläge.

🚨 **Jede Quote braucht eine Mindestbasis — dieser Fehler ist mir am 24.09. ZWEIMAL
passiert.** Erst standen zwei Beiträge mit 112 und 89 Reichweite als Recycling-Kandidaten
da (Median 170), weil 2 Interaktionen auf 112 rechnerisch 1,8 % sind. Nach dem Fix
rutschte derselbe Fehler bei der Einschlag-Regel wieder durch (89 Reichweite, 3,37 %).
Seitdem ist **Reichweite über dem eigenen Median Pflichtbedingung** für beide Stufen,
die Quote darf nur zusätzlich qualifizieren, und unter 3 Interaktionen zählt sie nicht.
Je kleiner der Nenner, desto mehr misst eine Quote den Zufall.

🚨 **Alles relativ zum eigenen Konto**, nie absolut — bei rund 2'000 gegen rund 60
Follower wäre jede feste Schwelle für eines der beiden Profile sinnlos.

**Die Routine läuft im täglichen `cockpit-daten-abgleich`** (06:15), nicht als eigener
Task: `holen.py --anzahl 60` → `gepostet-bauen.py` → in die Datenbank, plus eine
Telegram-Meldung, wenn ein Beitrag gerade reif geworden ist **und** gut lief. Keine
Meldung, wenn nichts reif wurde — ein tägliches „heute nichts" wird weggewischt, und
dann auch das, was zählt.

🚨 **Die 25 Beiträge waren nie eine API-Grenze**, sondern die Vorgabe `--anzahl` im
Skript. Auf dem Mentoring-Konto liegen **321 Beiträge**, alle abrufbar; `holen.py` hat
seit 24.09. Paginierung und `--alle`. Chrome hilft hier nicht — Reichweite und
Gespeichert stehen im Seiten-HTML überhaupt nicht, die gibt es nur über die API.
⚠️ Ein Lauf über die ganze Historie braucht je Beitrag einen eigenen Insights-Abruf und
läuft in ein 10-Minuten-Zeitlimit; er gehört ohne Limit in den Hintergrund.

Skripte: `gepostet-bauen.py` → `patch-gepostet.py` → `patch-recycling.py` →
`patch-einschlag.py` (alle wiederholbar, `node --check`).
🚨 **Neue Datendatei gehört in `testfassung-bauen.py` nachgetragen**, sonst ist der
Reiter in der lokalen Prüfung leer.

### Der Funnel-Reiter — vom Stichwort bis zum Beitrag (seit 2026-09-25)

**Patricia:** *„ich will eine klare übersicht mit allen keywords rsp. die zu einem
0€ produkt führen mit dem verlinkten produkt, wieviele da in der liste sind in
active campaign rsp. wieviele den TAG haben und dem „Manychat" keyword das eine
automatische antwort generiert auf instagram."* · *„vor allem die verknüpften
posts müssten dran."* · *„weil dann hat man im cockpit auch mal eine übersicht,
welcher TAG denn eigentlich wie oft erwähnt wurde."*

```bash
python scripts/cockpit/funnel-uebersicht-bauen.py --zeigen
# danach: ArtifactData set -> Sammlung "daten", Dokument "funnel"
```

Je Zeile ein Stichwort, aufgeklappt die ganze Kette: **Seite** · **alle
Tag-Stufen mit Kontaktzahl** · **Liste** · **Automationen** · **alle
Anschluss-Angebote mit Preis und Kasse** · **die Beiträge, die das Wort
spielen** — geplante mit Datum, gepostete mit Reichweite und Link.

🚨 **Über die IDs, nicht über Namensähnlichkeit.** Der erste Anlauf suchte Tags
über den Namen und zeigte beim Bio-Check „0€ Bio-Check" (8 Kontakte) als *den*
Tag. Der Funnel erklärt aber Tag **59** („Bio-Check Lead") als seinen Eintrag,
und der steht auf **0**. Beides ist wahr und es sind zwei verschiedene Dinge.
Jeder Tag trägt jetzt `deklariert: true/false`, und wo der **Eintrags-Tag** leer
ist, während ein nicht erklärter gefüllt ist, steht ein Befund dabei: *da tagt
etwas anderes als die Automation*. Über **alle** deklarierten zu prüfen findet
genau diesen Fall nie, weil irgendeiner immer gefüllt ist.

🚨 **`produkttreppe_anschluss` ist eine Liste, kein einzelnes Angebot.** Mit
`ast.literal_eval` als Dict gelesen, war das Angebotsfeld bei **allen vierzehn**
Keywords leer — also genau die Angabe, um die Patricia gebeten hat. Eine Spalte,
die überall leer ist, sieht aus wie ein Datenproblem und ist ein Lesefehler.

🚨 **Ein Klammerzusatz im Datenfeld kippt die Wortsuche.** In
`active-funnels.json` steht `"manychat_keyword": "STANDBEIN (Flow live seit
2026-09-11)"`. Ungefiltert wurde nach dem ganzen Satz gesucht — aus 26 geplanten
Beiträgen wurden 0, und die Zeile sah aus wie ein toter Funnel.

🚨 **Fünf von vierzehn Stichwörtern hängen an keinem Funnel.** SYSTEM, FAHRPLAN,
THEMA, PRODUKT und ANLEITUNG stehen nur in `context/manychat-keywords.md`. Wer
allein `active-funnels.json` liest, verliert sie — und dass sie fehlen, sieht man
der Übersicht nicht an. Sie kommen ohne AC-Zahlen, aber **mit** ihren Beiträgen.

🚨 **Der Stand gehört an JEDE Zeile.** Die Ladeschleife im Cockpit nimmt vom
Dokument nur `items`; ein Stand-Datum daneben kommt nie an, und die Zahlen stehen
ohne Datum da — also als wären sie von heute.

**Befund beim ersten Lauf (25.09.2026):** **4 Stichwörter laufen völlig leer** —
`STORY`, `QUIZ`, `FAHRPLAN`, `SYSTEM`: Automation gebaut, Tag angelegt, und kein
einziger Beitrag nennt das Wort. Dazu `ENERGIE` mit 23 geplanten Beiträgen und
`STANDBEIN` mit 26 — die Reichweite ist also da, es hängt an der Freigabe.

🚨 **Der Abgleich hat beim ersten Lauf sieben Mailstrecken gelöscht**, weil das
Skript je Zeile ein frisches Dict anlegte statt den Eingangs-Eintrag zu
übernehmen. `sequenz` pflegt `daten-abgleich.py` aus `active-funnels.json`.
**Ein Feld, das ein anderes Skript pflegt, wird weitergetragen, nicht neu
erfunden** — zurückgeholt aus der Datenbank-Fassung.

🚨 **Umlaute und deutsche Anführungszeichen nie über ein Bash-Heredoc in Python
schicken.** Pythons stdin ist auf Windows cp1252; `„…"` kommt verstümmelt an, der
Vergleichstext passt nicht, und die Ersetzung läuft still ins Leere. Für solche
Patches ein Skript schreiben statt eines Heredocs.

Skripte: `funnel-uebersicht-bauen.py` → `patch-funnel-uebersicht.py`.
🗃 Die alte Ketten-Ansicht bleibt als `renderFunnelKetten` stehen und springt
ein, solange die Daten noch ohne `posts_geplant` kommen.

🚨 **Und ein Fund beim Gegenlesen der Live-Fassung:** der Datenverlust-Fix vom
24.09. wurde bei **Karussells** nie angewendet — dort gewann der Stand aus der
Datenbank weiter bedingungslos (`Object.assign` statt `dbUebernehmen`). Genau
dort tippt Patricia Caption und Folientexte auf der Wochenkarte. Behoben in
Version 78.

#### 🚨 Der Keyword-Zähler war blind — die Caption wurde nie ganz gespeichert

**Patricia, 25.09.2026:** *„zu story eine ergänzung. ich habe sehr wohl einen
post, der story kommentiert hat"* — sie hatte recht, und es betraf **alle**
Stichwörter.

`holen.py` speicherte je Beitrag nur `anfang` — die ersten **90 Zeichen** der
Caption (`sauber(text, laenge=90)`). **Der Keyword-Aufruf steht immer am Ende**
(„Kommentier STORY, dann schick ich dir…"). Gesucht wurde also genau dort, wo er
nie steht. Die wenigen Treffer vorher waren Zufall — Beiträge, die schon in der
ersten Zeile mit „Kommentier THEMA" anfangen.

| | vorher | nachher |
|---|---:|---:|
| STORY | 0 | **11** Beiträge, 3'885 Reichweite |
| FAHRPLAN | 0 | 4 |
| SICHTBAR | 0 | 2 |
| LEAD | 1 | 3 |
| BIO | 0 | 2 |
| „läuft leer" | 4 | **2** |

`holen.py` legt seit 25.09. zusätzlich `caption` ab (`anfang` bleibt für Anzeige
und Zuordnung), `funnel-uebersicht-bauen.py` liest die volle Caption aus **allen**
Rohabzügen, je Beitrag der jüngste Stand.

🚨 **285 ältere Beiträge liegen weiter nur mit 90 Zeichen vor** — das Skript sagt
das bei jedem Lauf und nennt `holen.py --alle`. Eine Zahl, die auf unvollständigen
Daten beruht, muss das selbst dazusagen.

🚨 **Die Lehre:** eine Kürzung beim Speichern ist unsichtbar. Sie sieht wie ein
Anzeigedetail aus und wird zur Falschaussage, sobald jemand das Feld durchsucht.
**Wer ein Feld kürzt, speichert daneben das Ganze.**

#### 🚨 Der Sprung zum Beitrag hat nie funktioniert

Patricia: *„kannst du die verlinkung machen zu den beiträgen bitte"* — beim Bauen
kam heraus, dass der bestehende Sprung seit dem 24.09. tot war, und zwar zweifach:

- **`springeZuBeitrag` stand INNERHALB von `renderUebersicht`.** `unterBlock`
  ruft sie auf — eine andere Funktion im selben Modul, die eine verschachtelte
  nie sieht. Die Zeile dort lautete `if (typeof springeZuBeitrag === "function")`,
  und **genau diese Abfrage war immer falsch**. Der Klick auf einen Hook in „Was
  wann rausgeht" tat nichts, ohne Fehler in der Konsole.
  🚨 **Ein `typeof`-Schutz um einen Aufruf macht einen kaputten Aufruf unsichtbar.**
- **Das Datum kam aus `blo(b.obj).datum`** — dem alten Blotato-Feld aus dem
  Karussell-Editor, das bei fast allen Beiträgen leer ist. Das echte Datum setzt
  die Wochenkarte in `obj.datum`. Gemessen: von 16 Zeilen auf der Übersicht
  trugen **6** ein Datum, nach dem Fix **10** (die übrigen sechs haben wirklich
  keins). Dieselbe Stelle sortiert die Übersicht.

Jetzt gibt es `datumVon(b)` als die eine Stelle, `beitragNach(id)` als Brücke,
und `springeZuBeitrag` steht im Modul-Scope. Im Funnel-Reiter ist jeder geplante
Beitrag anklickbar: Sprung in seine Woche, Platz aufgeklappt. Ohne Datum sagt ein
Hinweis, dass er in der Ideenliste steht — eine stumme Ansicht sieht aus wie ein
toter Klick.

Skript: `patch-beitrag-verlinken.py` (wiederholbar, mit Gegenprobe, dass
`springeZuBeitrag` genau einmal vorkommt und kein `blo()`-Datum übrig ist).

#### Die Eintrags-Tags — und warum ManyChat nicht mitmisst (29.09.2026)

**Patricia:** *„ich habe den Tag 0€ Bio Check für Bio, 0€ Businessfahrplan für
Fahrplan, 0€ Idee für Ideen-check, 0€ Lead-Challenge für Lead Challenge, 0€
Potenzial Test, 0€ Starterguide, 0€ Stimmcheck, 0€ StoryChallenge"* · *„also das
ist jetzt in AC"* — und direkt danach: *„in manychat ist es anders"*.

**Das Muster ist einheitlich: jeder Eintrags-Tag in AC heisst „0€ <Name>".** Die
Funnel-Definition nannte vorher andere („Bio-Check Lead", 0 Kontakte), deshalb
stand in der Auswertung überall eine Null. Jetzt hängen `eintrag_tag_name` und
`eintrag_tag_id` an jedem Funnel in `active-funnels.json` — **über die ID, nicht
über den Namen**, denn ein Tag lässt sich umbenennen.

| Freebie | AC-Tag | ID |
|---|---|---:|
| Bio-Check | 0€ Bio-Check | 66 |
| Story-Challenge | 0€ Story-Challenge | 69 |
| Lead-Challenge | 0€ Lead-Challenge | 42 |
| Produkt-Ideen-Finder | 0€ Idee | 97 |
| Starterguide | 0€ Starterguide | 68 |
| Stimm-Check | 0€ Stimmcheck | 105 |
| Potenzial-Test | 0€ Potenzial Test | 45 |
| Business-Fahrplan | 0€ Businessfahrplan | 67 |

🚨 **ManyChat hat eigene Tags, und sie heissen anders.** Nachgesehen über die
ManyChat-API (66 Tags): dort steht `0 € Story-Challenge` **mit Leerzeichen**,
dazu `0€ Starterguide geöffnet`, `E-Book 0 auf echt`, `Selbsttest Business`,
`quiz_started`. **Für Bio-Check, Lead-Challenge, Idee, Stimmcheck,
Potenzial-Test und Businessfahrplan gibt es in ManyChat gar keinen Tag.**

🚨 **Und die ManyChat-API gibt keine Kontaktzahl je Tag heraus** — nur die
Liste. Die Messung des Messenger-Schritts ist damit über die Schnittstelle
**nicht möglich**, egal wie die Tags heissen.

**Was die Spalte „im Tag" deshalb misst:** Eintragungen in die **Mailliste**,
nicht Reaktionen auf den Kommentar. Wer im Messenger antwortet und die
Mailadresse nicht hinterlässt, fehlt. **Die Zahl ist eine Untergrenze** — das
steht als Feld `misst` im Dokument, damit niemand eine Konversion daraus
rechnet, die zwei verschiedene Dinge vergleicht.

🚨 **Zwei Stichwörter können sich einen Tag teilen** — `SICHTBAR` und
`ANLEITUNG` zeigen beide auf den Starterguide, `FAHRPLAN` und `SYSTEM` auf den
Business-Fahrplan. Die Zahl gehört dann dem **Freebie**, nicht dem Stichwort;
**wer die Spalte aufsummiert, zählt doppelt**. Das Feld `geteilte_tags` im
Dokument nennt sie.

**Stand 29.09.2026 — die Ausgangslage für 5k:**

| Stichwort | Beiträge | in der Liste | je Beitrag |
|---|---:|---:|---:|
| **BIO** | 10 | **9** | **0,9** |
| STORY | 15 | 4 | 0,3 |
| STANDBEIN | 4 | 2 | 0,5 |
| LEAD | 8 | 2 | 0,2 |
| SICHTBAR | 8 | 1 | 0,1 |
| ECHT1 | 27 | ~3 | 0,1 |
| QUIZ · FAHRPLAN · ENERGIE | 5 · 14 · 1 | 0 | — |

**Über alle Freebies zusammen 19 Eintragungen.** BIO bringt bei einem Drittel
der Beiträge das Dreifache von ECHT1.

⚠️ **Offen:** `ECHT1` hat keinen benannten Tag — gefüllt ist „Workbook von 0 auf
echt" (3), der Name passt nicht ins 0€-Muster. `THEMA` (20 Beiträge) und
`PRODUKT` (11) haben gar keinen, das sind aber Minikurse statt Freebies.

🚨 **AC antwortete mitten im Lauf mit 503 und kippte den ganzen Abgleich.**
`ac()` macht jetzt drei Anläufe mit wachsender Pause und bricht nur bei einem
echten Fehler ab — ein Schluckauf beim Anbieter darf keine leere Auswertung
erzeugen.

##### 🚨 Aufgeräumt in AC — und was dabei fast schiefgegangen wäre (30.09.2026)

**Patricia:** *„mich regt es mega auf, dass du bei biocheck so viele verschiedene
tags eröffnet habe"* — sie hatte recht: beim Bio-Check-Aufbau im April sind
**acht** Tags auf einen Schlag entstanden (IDs 59–66), **fünf davon leer**. Die
Regel „je Funnel EIN Tag" steht seit dem 25.09. in dieser Datei; der Altbestand
wurde nie aufgeräumt.

**Gelöscht (0 Kontakte, von keinem Code und keiner Automation gesetzt):**
„Bio-Check Lead" 59 · „→ Expertin-Interesse" 62 · „→ Kundenmaschine-Interesse" 63 ·
„→ Insta-DM" 64 · „→ braucht Freebie-Hilfe" 65 · „produkt-ideen-finder-lead" 98.
Der Bio-Check hat jetzt **drei** Tags, alle gefüllt: Eintrag (9) · abgeschlossen
(5) · Thema-Interesse (2). Die toten IDs sind auch aus `active-funnels.json` und
der Bundle-Kopie heraus.

🚨 **Dass Tag 59 leer war, ist der Beleg, dass er nichts auslöst.** Automation
„0€ Bio-Check" hat 9 Kontakte — käme sie von Tag 59, wären es null. Ein leerer
Tag kann trotzdem Trigger sein; dann ist die Automation ohnehin tot. **Vor dem
Löschen gegen die Automation prüfen, nicht nur die Kontaktzahl lesen.**

##### 🚨 `multientry=1` — ein neuer Tag schickt die Mails nochmal

Patricia wollte die zwei Story-Challenge-Tags zusammenlegen und hat selbst den
Finger auf die Stelle gelegt: *„da muss ich noch prüfen, ob dann auch die mail
rausgeht wenn sie sich anmelden. es soll ja trotzdem der ganze ablauf
funktionieren."*

**Gemessen: alle sechs geprüften Automationen haben `multientry=1`** — dieselbe
Person darf mehrfach durchlaufen. Bei „0€ Story Challenge" ist das schon
passiert: `entered=10` bei **8** Kontakten. Wer den fünf Leuten von Tag 40 den
Tag 69 dazugibt, löst die Willkommens-Strecke **ein zweites Mal** aus.

**Deshalb bleibt AC unberührt und die Anzeige legt zusammen:**
`eintrag_tag_ids: [69, 40]` am Funnel, der Builder holt je Tag die Kontakt-IDs
und bildet die **Vereinigung**.

🚨 **Vereinigen, nicht addieren.** 5 + 4 sind **8 Personen**, nicht 9 — eine
trägt beide Tags. Addieren hätte genau die Zahl, um die es geht, um eine Person
zu hoch gemacht.

🚨 **`filters[tag]` und `filters[automation]` werden von AC stumm ignoriert.**
Der erste Anlauf meldete bei **jedem** Tag „97 Kontakte" und bei **jeder**
Automation „77" — die API hatte jedes Mal die ersten 100 von *allen*
Zuordnungen geliefert. Die Filter, die wirken, heissen **`tagid`** und
**`seriesid`** an `/contacts`. Gegenprobe ist `subscriber_count`: kommt eine
andere Zahl heraus, ist die Abfrage kaputt. **Gleiche Zahl bei jeder Zeile ist
nie ein Befund, sondern immer ein Lesefehler.**

**Was die Deckung zeigt** (Personen in der Automation gegen Tag-Träger):
„0€ Story Challenge" enthält **alle** von Tag 40 **und alle** von Tag 69 —
beide Wege kommen an. „Bio-Check PDF" deckt sich exakt mit „Bio-Check
abgeschlossen" (5/5), „0€ Von 0 auf echt" exakt mit „Workbook von 0 auf echt"
(3/3) — das bestätigt `ECHT1` → Tag 36.
🚨 **„Bio-Check abgeschlossen" ist deshalb kein Zähler, sondern hängt an der
PDF-Auslieferung** — nie löschen.

**Stand 30.09.2026:**

| Stichwort | Beiträge | in der Liste | je Beitrag |
|---|---:|---:|---:|
| **BIO** | 11 | **9** | **0,8** |
| STORY | 15 | 8 | 0,5 |
| STANDBEIN | 4 | 2 | 0,5 |
| STIMME | 2 | 1 | 0,5 |
| LEAD | 8 | 2 | 0,2 |
| ECHT1 | 27 | 3 | 0,1 |
| SICHTBAR | 8 | 1 | 0,1 |

⚠️ **Offen:** ob die zwei Story-Tags in AC wirklich verschmolzen werden — das
kostet fünf doppelte Mailstrecken und ist Patricias Entscheidung. `THEMA` (20
Beiträge) und `PRODUKT` (11) haben weiter keinen Tag.

### Notion ablösen — der Umzug (seit 2026-09-24)

**Patricias Ziel:** *„ziel für mich wäre, dass ich notion ablösen kann"* · *„ja für ds
private behalte ich notion vorerst. aber ich will nicht alles separat pflegen"* ·
*„einfach der reihe nach alles weiter umsetzen"*.

**Landkarte über alle 25 geschäftlichen Blätter:** `plans/2026-09-24-notion-abloesen.md`.
Privat (Haushalts-Liste, Tagesplaner-Privatteil, Garten) bleibt in Notion.

🚨 **Die Anforderung ist nicht Vollständigkeit, sondern: jedes Feld hat genau einen
Ort.** Wo beides gepflegt werden müsste, wird eine Seite stillgelegt.

| Notion-Blatt | Cockpit | Skript |
|---|---|---|
| Content-Management (30 Felder) | Gepostet & Analyse | `gepostet-bauen.py` |
| Jahresplanung (7) | Jahresplan | `jahresplan-importieren.py` |
| Monatsplanung (12) | Monatsbogen | `monatsbogen-bauen.py` |
| Wochenplanung (12) | Wochenbogen | `wochenbogen-bauen.py` |
| Aufgaben (21) | Aufgaben | `aufgaben-bauen.py` + `aufgaben-abgleichen.py` |
| Ziele (12) | Ziele | `ziele-bauen.py` |
| Kennzahlen (15) | Zahlen & Ziele | `umsatz-bauen.py` |
| Reichweiten-Tracking (11) | Zahlen & Ziele | `reichweite-bauen.py` |
| Kunden (16) + Testimonials (7) | Kundinnen & Leads | `kunden-importieren.py` |

**Was an Handarbeit wegfällt:** je Beitrag Reichweite · Gespeichert · Gefällt mir ·
Kommentare · neue Follower · URL · Datum. Dazu Monatsumsatz, Öffnungsrate,
Newsletter-Zahlen. **Genau die Felder, die in Notion seit Monaten leer standen** —
nicht aus Nachlässigkeit, sondern weil die Zahlen in vier Werkzeugen lagen.

🚨 **Einmalig importieren, dann gehört es ihr.** Jahresplan, Aufgaben, Ziele und
Kundinnen sind **Umzüge, keine Abgleiche**. Die Dokumente gehören Patricia; der
tägliche Abgleich darf sie nie mit `set` überschreiben. Die Liste der geschützten
Dokumente steht im Task `cockpit-daten-abgleich`.

🚨 **Zwei Dokumente je Bogen.** `daten/monatsbogen` (gerechnet, Abgleich) und
`daten/monatsbogen-notizen` (ihre Texte). Dasselbe bei Woche und bei `gepostet`.

#### Neue Quellen, die vorher niemand angezapft hat

**ThriveCart `/transactions`** — 85 Transaktionen, Umsatz je Monat und Produkt.
🚨 `amount` ist in **Rappen** (20500 = CHF 205). 🚨 Paginierung über `?page=2`;
`offset` und `start` werden stillschweigend ignoriert und liefern wieder Seite 1.
🚨 **Kundendaten werden gar nicht erst gelesen** — jede Zeile trägt Name, E-Mail,
Adresse und IP mit. 🚨 `charge` ist ein Kauf, `rebill`/`finish` sind Raten: für
„wie viele Kundinnen" nur `charge` zählen, sonst zählt eine Ratenzahlerin dreimal.

**ActiveCampaign-Kampagnen** — 351 Stück, Öffnungsraten je Monat.
🚨 **Der MCP-Server liefert 403**, weil er die Zugangsdaten nur beim Start liest und
der Schlüssel am 13.09. gewechselt wurde. Die Skripte lesen die `.env` selbst und
kommen durch — wer sich auf die MCP-Tools verlässt, hält den Zugang für kaputt.
🚨 **Automations-Mails sind keine Newsletter.** Die meisten der 351 gehen an *eine*
Empfängerin. Getrennt wird an der Empfängerzahl (ab 5). 🚨 Öffnungsrate auf die
**Zugestellten**, nicht auf die Listengrösse — sonst sinkt sie jedes Mal, wenn die
Liste wächst.

#### Was die Zahlen sofort gezeigt haben

🚨 **CHF 4'927 von 40'000 bei 73 % des Jahres.** Das Ziel stand in Notion, der Umsatz
in ThriveCart — dazwischen lag nie ein Blick. Der Balken im Ziele-Reiter trägt
deshalb eine senkrechte Marke für „so viel Jahr ist vorbei": ohne sie sagt 12 % nichts.

🚨 **Mehr Beiträge, weniger Reichweite.** Februar: 12 Beiträge, Median 348, CHF 1'283.
Juni: 54 Beiträge, Median 155, CHF 0. August: 52 Beiträge, Median 135, CHF 241.
Auf Wochenebene noch deutlicher (KW30: 4 Beiträge / 409 · KW35: 28 Beiträge / 120).
Das ist ein **Befund, keine Erklärung** — aber die Frage war vorher nicht stellbar.

🚨 **37 von 53 offenen Aufgaben waren überfällig, 21 davon längst erledigt.**
Patricia: *„gleich doch ab mit deinem workspace, was noch aktuell ist."*
`aufgaben-abgleichen.py` sucht je Aufgabe einen **Beleg** im Workspace und hängt ihn
an; abgehakt wird nichts. **Ein Haken, den eine Maschine gesetzt hat, ist derselbe
Fehler wie ein fehlender.** Drei Zustände, nicht zwei: dazu kommt **hinfällig** für
Aufgaben, deren Entscheidung gekippt ist (ThriveCart Academy, Notion-Eintrag).
🚨 Wiederkehrende Aufgaben stehen mehrfach in der Liste — ein Stichwort-Treffer hätte
die Oktober-Runde des Backoffice-Checks als erledigt markiert. Ein Befund gilt nur
für Termine, die vorbei sind.

#### 🚨 Personendaten im Cockpit (seit 24.09.2026)

Auf Patricias ausdrücklichen Wunsch stehen **32 Klarnamen und 3 E-Mail-Adressen**
im Cockpit, dazu vier Kundenstimmen. **Ab jetzt darf der Link nicht mehr
weitergegeben werden.**

Telefon, Adresse, Geburtstag und URL sind **nicht** übernommen — sie waren in Notion
bei allen 34 Einträgen leer. Eine Spalte zu bauen, die dauerhaft leer aussieht und
trotzdem nach sensiblen Daten verlangt, wäre das Schlechteste aus beidem.

Die Rohdaten liegen in `outputs/cockpit/abgleich/kunden-roh.json` — **nicht im
Skript**, wie seit dem 13.09. vorgeschrieben. Beide Ordner sind gitignored.

🚨 **Die Notion-Testimonials sind faktisch leer** (drei Einträge, einer „Super Kurs!").
Die echten stehen in der MBA-Salespage, die öffentlich ist — damit freigegeben.

#### 🚨 Die Testfassung muss stimmen, sonst ist sie wertlos

Sie legte für Listen-Reiter das **ganze Dokument** in den Speicher statt nur `items`.
Ergebnis: `state.leads.filter is not a function`, Reiter tot — dieselbe Falle wie
beim `state.zahlen`-Zusammenstoss am selben Morgen. Sie liest jetzt `DOC_KEYS` aus
dem Cockpit selbst und packt das Array aus. **Jede neue Datendatei gehört in
`testfassung-bauen.py` nachgetragen.**

🚨 **Konsolenfehler in einem wiederverwendeten Tab sind oft Altlasten.** Zweimal an
diesem Tag sah ein längst behobener Fehler aus wie ein neuer. Gegenprobe im frischen
Tab, bevor etwas repariert wird, das ganz ist.

### Bild-Editor — Story, Reel-Cover und Karussell-Folien (seit 2026-09-14)

**Artifact:** https://claude.ai/code/artifact/21e66e0e-2576-41db-8c8d-f14d7079a1e0
**Quelle:** `outputs/_bild-editor/index.html` + `assets/`

**Der eine Editor für alle drei Bildformate** — Story **1080×1920**, Reel-Cover
**1080×1920** und Karussell-Folie **1080×1350**. Foto aus den Shootings **oder frisch
hochgeladen** · **Video als Hintergrund** (Story/Cover) mit Stelle-Regler · Verlauf oder
Unifarbe in Brandfarbe · **Textbalken** in Patricias Story-Stil mit Deckkraft und Breite ·
Text frei tippbar, Schriftgrösse und **Höhe verschiebbar** · **Sticker-Zonen** als
Hilfslinien mit Warnung, wenn der Text hineinragt.

**Die ganze Abfolge auf einen Blick:** über der Bühne liegt ein Streifen mit allen Folien
als echte Miniaturen — Folie anlegen, kopieren, verschieben, löschen. So sieht Patricia
das komplette Karussell bzw. den ganzen Story-Bogen, nicht nur ein Bild. **Alle Folien als
Bilder** erzeugt die ganze Serie am Stück.

**Mehrere Textbalken je Folie:** Leiste oben im Textbalken-Feld — `+ Balken` legt einen
zweiten an, jeder mit eigener Höhe, Farbe, Deckkraft und Schriftgrösse. Patricias Muster
dahinter: Folie **Kopieren**, dann **+ Balken**, damit der Text über mehrere Storys
mitwächst statt auf einmal dazustehen. Die Zonen-Warnung nennt den betroffenen Balken.
🚨 Beim Kopieren einer Folie müssen die Balken **echt kopiert** werden (`folieKopie`) —
ein `Object.assign` allein teilt das Array, und die Kopie ändert dann das Original mit.

**Ideen-Vorschläge:** Profil wählen (Mentoring/doTERRA), Thema eintippen, Lage wählen
(normaler Tag · anwärmen · Türen auf · Launch läuft · letzter Tag · danach), dann
**Idee schreiben lassen** → eine komplette Story-Abfolge, **fertig ausformuliert**, mit
Sticker- und CTA-Vorschlag; **Als Folien übernehmen** schreibt sie in den Streifen.

Das läuft über die Artifact-Fähigkeit **`sample`**: die Seite trägt einen
**Wissensbrief** (Konstante `WISSEN`) und fragt damit Claude direkt. Im Brief stehen
Kern-Painpoint und die vier Gedanken der Network-Mama, die Regel „**die Gegenspielerin
ist der Job, nicht das Network**", die drei Bedingungen mit Patricias Antwortsätzen, die
Angebotsliste, die zehn doTERRA-Schmerzpunkte mit ihren Szenen, Stimme und Verbote.
Quellen: `context/kern-painpoint.md` · `brand-voice.md` · `active-funnels.json` ·
`outputs/zielgruppen-research/doterra-2026-04-22.md` — im Editor **ohne fremde Namen und
ohne Zahlen**, weil die Seite teilbar ist. **Wenn sich dort etwas ändert, gehört es in
`WISSEN` nachgezogen.**

Fällt `sample` aus (keine Freigabe, Limit), greift ein **Bauplan-Vorrat** von rund 35
Abfolgen mit Platzhaltern — die Karte sagt, woher die Idee kommt.

**Der Wochenfokus kommt über die Artifact-Datenbank** (Fähigkeit `db`, Dokument
`daten/woche`). Ein Artifact kommt weder an Notion noch an die Dateien, deshalb **legt
Claude den Fokus dort ab** und die Seite liest ihn: sie zeigt „Diese Woche (KW 38): …",
belegt das Thema-Feld und die Lage vor und hängt den Block wörtlich an den Auftrag. Ein
von Hand getipptes Thema wird nie überschrieben; eine automatisch gesetzte Zeile wechselt
mit dem Profil. Geschrieben wird das in **`/content` Phase 9, Schritt 1b** — Format und
Regeln stehen dort.

🚨 **Die Notion-Wochenplanung ist oft nicht gepflegt.** Am 14.09. war die letzte
gefüllte Woche **KW35** (25.–31. August), für die laufende KW38 stand dort nichts. Der
Fokus kam deshalb aus den Monatsplänen. Das Feld `quelle` im Dokument muss immer sagen,
woher die Angaben stammen — **nie einen Wochenfokus erfinden**.

**Anschluss an den letzten Beitrag** (Umschalter „Woran knüpft die Story an?"): zweites
Dokument **`daten/beitraege`** mit je Profil `gepostet` (Datum, Typ, **`thema`** als ein
Satz, Caption-Anfang, Link, Reichweite) und `geplant` (Datum, Name, Hook, CTA). Quellen:
**gepostet** aus `scripts/instagram-insights/holen.py`, **geplant** aus der
**Cockpit-Datenbank** (`Artifact read_db`, Sammlung `karussells`). Im Auftrag steht dann
Patricias Regel dazu: *Feed abends, Story am nächsten Morgen greift ihn auf* — die Story
wiederholt den Beitrag nie, sie nimmt einen Gedanken heraus und führt zum CTA.

🚨 **Zwei Artifacts sind nie verbunden.** Cockpit und Bild-Editor haben getrennte
Datenbanken, und keine Seite darf in die andere schauen. Jede Brücke läuft über Claude:
lesen mit `read_db` beim einen, schreiben mit `write_db` beim anderen.

**Arbeitsteilung seit 14.09.2026 (Patricias Entscheid):**
**Cockpit = prüfen, freigeben, einplanen** (dort hängt Blotato) ·
**Bild-Editor = bauen und herunterladen.**
Der Karussell-Editor im Cockpit ist **entfernt**; „Im Bild-Editor bauen" auf der
Wochenkarte öffnet jetzt den Bild-Editor. Umgesetzt mit
`scripts/cockpit/patch-editor-zusammenlegen.py` (wiederholbar). Die Funktion
`renderKarussell` bleibt als toter Code stehen, weil `renderSlide` und die Helfer auch
von der Wochen-Vorschau gebraucht werden.
⚠️ **Noch offen:** Story-Studio und Reel-Studio liegen weiterhin im Cockpit und
überschneiden sich mit dem Bild-Editor. Vor dem nächsten Umbau mit Patricia klären.

### Das Markenwissen in den Artifacts (seit 2026-09-14)

Patricias Anspruch: *„ich erwarte schon, dass content-studio auf alles zugreift, wie wenn
ich dir hier den befehl content gebe. also caption richtig, hook richtig, PIE strategie."*

Eine Artifact-Seite kommt nicht an `context/` und nicht an die Skills. Deshalb wird der
Brief **aus den echten Quellen erzeugt** und als Dokument `daten/wissen-voll` in **beide**
Artifact-Datenbanken geschrieben:

```bash
python scripts/cockpit/wissen-bauen.py outputs/cockpit/abgleich
# danach: Artifact write_db → Sammlung "daten", Dokument "wissen-voll", file_path wissen-voll.json
```

**Zehn Bausteine, rund 99'500 Zeichen (104 KB):** Stimme · Kern-Schmerz Mentoring · die
zehn doTERRA-Schmerzen · Caption-Formeln mit CTA und Hashtags · Job-Säulen ·
**der komplette Hook-Skill** · verbotene Sprache · was nachweislich wirkt ·
Kommentar-Stichwörter · laufende Angebote.

🚨 **Der Hook-Skill geht vollständig mit** — Patricia am 14.09.: *„ich will alle ideen
drin haben."* Also alle 16 Teile: die vier Säulen, Reichweiten-Hierarchie, Briefing,
Kundensprache, Bewusstseinsstufen, Angles, PIE mit den rund 80 Kalender-Formeln, die
27 Formeln, die 10 Reveal-Frameworks, die 50 Vorlagen, der Voice-Layer, Verbote,
Hook-Check, CTA-Regel, Standard-Output, Beispiel, Testen, Kurz-Checkliste und der letzte
Check. **Draussen bleibt nur die Quellen-Liste am Schluss** — dort stehen die fremden
Kurse namentlich. Deshalb auch: **beide Seiten bleiben privat.**

Weil der Skill TEIL 6 enthält, gibt es **keinen eigenen PIE-Baustein** — sonst stünde der
Pflicht-Mix zweimal im Auftrag.

**Dazu ein Block je Format** im selben Dokument unter `formate` (Patricia, 14.09.:
*„bei reels wäre dann aber das wissen aus skill reel wichtig, bei karussell das von
karussell und bei story der storyskill"*):

| Format | Zeichen | Quellen |
|---|---|---|
| `reel` | ~26'000 | `reels-framework.md` (Viral-Mechanik, 3-Sekunden-Regel, Struktur-Formel, On-Screen-Text, Ton, Schnitt, Licht, Dreh-Anweisung, Hook-Prozess, Cover, Untertitel, Rechtliches, Serien, Posting-Zeiten, Hashtags) + `sprechreels-drehanleitung.md` |
| `karussell` | ~13'200 | `karussell-framework.md` (**die vier Typen**, **Funnel-Stufe**, **erst Texte freigeben**, Spezifika, Feed-Aesthetic, Bauweisen, Doktor-Checkliste, Briefing-Vorlage) |
| `story` | ~28'000 | `story-framework.md` (Kernregeln, Slide-Struktur, Käufertypen, die 8 Modi) + die 10 Verkaufs-Templates + die 3-Säulen-Ideenbibliothek |

🚨 **Der Karussell-Skill wirkte im Chat, aber nicht im Cockpit** (behoben 19.09.2026).
Patricias Frage: *„der karussell skill müsste doch aber schon beim erstellen von
karussells eingreifen, oder?"* — Nachgeprüft an den Daten: `typ` und `funnel` sind
bei allen 12 Karussells gesetzt und die Nuancierungsfolie steht bei den kontroversen
drin. Der Skill greift also, **wenn `/content` im Chat läuft**. Im Cockpit nicht:
`wissen-bauen.py` liest `context/karussell-framework.md`, **nicht** die `SKILL.md`.
Die vier Typen, die Funnel-Pflicht und „erst Texte freigeben" standen nur im Skill
und kamen dort nie an. Jetzt stehen sie **im Framework** und damit in beiden.

🚨 **Zwei konkurrierende Typ-Listen waren die Ursache für kaputte Daten.** Das
Framework hatte **sechs** Typen (inkl. „Kontrast"), Skill und Cockpit **vier** — und
der Cockpit-Schlüssel heisst `story`, die Skill-Überschrift „Storytelling". Drei von
zwölf Karussells trugen dadurch einen Wert, den das Auswahlfeld nicht kennt: es zeigte
den **falschen** Typ, und der Hinweistext blieb leer. Die vier sind jetzt die Liste,
die sechs sind als **Bauweisen** darunter einsortiert. Korrigiert wurden
`kw39-kar-fr-a` (→ `edukativ`), `kw39-kar-fr-b` und `kw38-kar-fr-b` (→ `story`).

🚨 **`abschnitte()` liess fehlende Titel stillschweigend weg.** Beim Umbenennen eines
Abschnitts wurde der Karussell-Baustein von 10'700 auf 9'576 Zeichen **kleiner** — das
fällt nur auf, wenn jemand auf die Zahl schaut. Das Skript **warnt jetzt** je nicht
gefundenem Titel. Neue Abschnitte in einer Quelle müssen in `FORMATE` nachgetragen
werden, sonst kommen sie nie im Cockpit an.

`wissenText(format)` hängt **nur den passenden** Block an — nie alle drei, sonst schleppt
jeder Auftrag 65'000 Zeichen mit, die er nicht braucht. Gesetzt durch
`scripts/cockpit/patch-format-wissen.py`, das zugleich **Reel als Format im
Content-Studio** ergänzt (Titelbild-Hook · Unterzeile · Sprechskript · Caption ·
Bildidee, plus Knopf „Als Reel anlegen" ins Reel-Studio).

⚠️ **Preis der Vollständigkeit:** rund 28'000 Token für den allgemeinen Brief plus 3'000
bis 8'000 fürs Format gehen bei jedem Auftrag mit. Das Schreiben dauert länger und kostet
mehr. Wenn das stört, ist der Hebel, TEIL 6 und TEIL 9 wieder auf Auszüge zu kürzen —
nicht die Mechanik.

*(Am 14.09. hat Patricia gefragt, ob Angles, Hook-Ideen und „wie ein Hook allgemein zu
sein hat" enthalten sind. Angles ja, die vier Säulen und der Formel-Kasten fehlten.
Bei solchen Fragen **nachsehen, nicht behaupten** — das Skript sagt in seiner Ausgabe,
was drin ist.)*

Beide Seiten lesen das Dokument beim Öffnen und hängen es an **jeden** Auftrag; fehlt es,
laufen sie mit ihrem eingebauten Kurzwissen weiter. Zusätzlich nimmt das Content-Studio
jeden Entwurf selbst ab (letzter Check + Beitrags-Check), gesetzt durch
`scripts/cockpit/patch-hookregeln.py`; eingehängt wird es durch
`scripts/cockpit/patch-wissen-voll.py`.

🚨 **Zwei Grenzen sind im Bauskript verdrahtet und dürfen nicht gelockert werden:**
- **Keine Namen fremder Mentorinnen** — die Seiten sind teilbar. Das Skript ersetzt sie
  und **bricht ab**, wenn einer durchrutscht. (Beim ersten Lauf ist „Julias" durch die
  Wortgrenze geschlüpft; darum steht dort jetzt `\w*` plus eine Genitiv-Regel.)
- **Keine zugekauften Kataloge** — aus dem Hook-Skill kommt nur die Mechanik, nicht die
  27 Formeln, nicht die Kalender-Formeln, nicht die Beispiele.

**Ändert sich eine Quelle, Skript laufen lassen und das Dokument neu schreiben.** Es ist
eine erzeugte Kopie, keine Verbindung — aber nichts, was von Hand gepflegt werden müsste.

**Fertige Beiträge landen als `daten/entwuerfe` im Editor** und erscheinen dort als Liste
**„Aus deiner Planung"** — ein Tipp und das ganze Karussell bzw. der Story-Bogen steht im
Folien-Streifen, im richtigen Format. `text` wird der grosse Balken, `unter` ein zweiter,
kleinerer darunter. Geschrieben in **`/content` Phase 9, Schritt 1c**. Ohne das müsste
Patricia jede Folie abtippen — das war bis 14.09. die Lücke zwischen Planung und Bauen.

**Der Ideen-Katalog steckt in `WISSEN` und hat zwei Hälften** (Patricia, 14.09.):
- **Launch-Lagen** (anwärmen · Türen auf · läuft · letzter Tag · danach) kommen aus dem
  **Launch-Workbook** der Mentorin: Phasen-Muster plus die sechs Käufertypen mit ihrem
  jeweiligen Story-Fokus.
- **Normale Tage** kommen aus **Patricias eigenem Workbook „90 Storyideen"**
  (`outputs/produkte/storyideen-networkerinnen/workbook-print.html`) — acht Kapitel mit dem
  Mix ❤️ Nähe · 💡 Mehrwert · 📨 Einladung.

Ohne diese Listen erfindet Claude das Format frei und landet immer bei denselben zwei, drei
Bauarten. Neue Muster gehören dort ergänzt, nicht in den Auftrag. 🚨 **Im Editor stehen
keine Mentorinnen-Namen** — die Seite ist teilbar.

🚨 **Reel-Cover ist 9:16, nicht 4:5.** Das Cover ist so gross wie das Reel selbst; im
Profil-Raster zeigt Instagram nur den mittleren **3:4**-Ausschnitt, unten liegen Caption
und Bedienknöpfe drüber. Deshalb markiert der Editor oben 0–12.5 % und unten 82–100 % als
tote Zone — **der Hook gehört in die Mitte**. (Bis 14.09. stand dort fälschlich 1080×1350.)

**Zwei Regeln beim Ändern:**
1. **Die Vorschau ist der Export.** Die echte 1080er-Bühne wird per `transform: scale()`
   verkleinert gezeigt und mit `html2canvas` genau so exportiert. Nie das Bild im Canvas
   nachbauen — dabei weicht der Zeilenumbruch ab.
2. **`document.fonts.ready` vor dem Export abwarten**, sonst misst der Browser mit der
   Ersatzschrift.

3. **Video nie ins `innerHTML` zurückschreiben.** Das `<video>` hängt in einem Cache je
   Datei und wird nach jedem Zeichnen wieder eingesetzt — sonst lädt es bei jedem
   Reglerzug neu. Streifen und Export leben vom **Standbild** der gewählten Stelle.

**Video mit eingebranntem Text — direkt aufs Handy (seit 2026-09-14).** Über die
Fähigkeit **`downloads`** gibt die Seite eine fertige Datei ab. Der Weg, der das möglich
macht: die Textebene wird **einmal** per `html2canvas` ohne Videobild abgezogen
(`inhalt(s, false, true)` liefert nur Verlauf und Balken) und dann über **jedes**
Videobild auf eine 1080er-Leinwand gelegt; `canvas.captureStream(30)` plus die Tonspur
aus einem `MediaElementSource` (bewusst **nicht** an die Boxen gehängt, sonst hört sie
sich selbst) gehen in einen `MediaRecorder`, das Ergebnis an `downloads.save()`.
Dadurch sitzt der Text exakt wie in der Vorschau — **nie den Text im Canvas nachbauen**.
Getestet 14.09.: 1080×1920, 10,6 s, Ton in Stereo, MP4.

Drei Fallen, die dabei Zeit gekostet haben:
- **`v.currentTime = 0` feuert kein `seeked`**, wenn das Video schon auf 0 steht — jedes
  Warten auf ein Medien-Ereignis braucht ein Zeitlimit daneben (`hoechstens`).
- Die Aufnahme läuft in **Echtzeit**: ein 30-Sekunden-Video braucht 30 Sekunden.
  Bei 60 s wird abgeschnitten, weil eine Story nicht mehr trägt.
- `createMediaElementSource` geht **einmal je Seite** — deshalb liegt sie in `tonQuelle`.

Bilder kann ein Artifact ebenfalls nicht per Link abgeben — das fertige Bild erscheint
deshalb gross auf der Seite und wird per Langdruck gespeichert. Der frühere Auftragstext
für den Chat erscheint nur noch, wenn `downloads` nicht verfügbar ist; gebrannt würde dann
über `scripts/videoschnitt/textebene.py` und per Telegram geschickt.

Lokal ansehen: `.claude/launch.json` → `bild-editor` (Port 4370).

🗃 Der frühere `_titelbild-editor` ist darin aufgegangen (gleiche Artifact-Adresse),
archiviert unter `reference/_archiv-skills/_titelbild-editor-alt/`.

### /garten

**Zweck:** Persönlicher Gartenassistent und Permakultur-Berater starten.

Lädt den Garten-Kontext (Standort Appenzellerland, 920 m, Permakultur-Philosophie) und greift auf die Notion-Datenbanken (Samen, Beetplan, Gartentagebuch, Wissensarchiv) zu. Gibt einen aktuellen Status, zeigt was ansteht und fragt, was heute im Garten geplant ist. Berücksichtigt Mondkalender, Mischkultur, Fruchtfolge und die kurze alpine Vegetationsperiode.

### /basteln (Hobby, seit 2026-08-18)

**Zweck:** Persönlicher Bastel-Assistent für Papierbasteln — Material-Überblick, Projekt-Ideen aus **eigenem** Bestand, Anlass-Vorlauf und doTERRA-Verpackungen.

**Löst drei Probleme:** kein Überblick (8'070 digitale Dateien + volle Schubladen) · nie vorbereitet bei Geburtstagen · Pinterest-Ideen nicht auf eigenes Material gematcht.

**Wissensgrundlagen** (in `context/basteln/`):
- `README.md` — Systemlogik + Arbeitsregeln
- `inventar-digital.md` — vollständiger Katalog: 467 Verpackungs-Dateien (21 Bauformen), 343 Karten, 70 Anhänger, 2'287 digitale Papiere, ~60 Digistamp-Themenwelten, Gonis-Techniken
- `inventar-stempel.md` — ⭐ **Herzstück:** ID-System (**vierstellig mit Typ-Block:** 1000er Clearstamps, 2000er Holzstempel, 3000er Stanzen, 4000er Schablonen, 5000er Embossing, 6000er Werkzeuge, 7000er Farben — physisch in 10er-Bündeln mit Gummi und Bündel-Kärtchen), Tag-Vokabular, Erfassungs-Workflow. Physische Ablage nach Nummer, thematische Suche macht Claude über die Tags. Antwort immer mit Nummer + Typ
- `inventar-physisch.md` — Werkzeuge/Papier/Farben (wird per Foto gefüllt)
- `projekt-ideen.md` — Projekt-Matches + Anlass-Material-Matrix
- `shop-recherche.md` — wie Hersteller-Ideen dazukommen (was geht, was nicht)
- `stempelsets-sf.md` — erfasste Scrapbook-Forever-Sets mit Technik-Auswertung
- `context/persoenlich/basteln-anlaesse.md` — Anlass-Liste, **gitignored** (Namen/Geburtsdaten)

**7 Modi:** „Was schenke ich X?" · Inventar erfassen (Foto) · Set-Recherche · Pinterest-Check · Bastel-Check (Vorlauf) · doTERRA-Verpackung · Batch-Session planen.

**Setup:** Silhouette-Plotter (Print&Cut kalibriert) · Envelope- + Gift-Bag-Punchboard · Copic-Marker · Quellen Mundart Stempel (CH) / Scrapbook Forever / Gonis.

**Digitale Quelle:** `C:\Users\pnulm\OneDrive\Dokumente\Patricia\Hobby\Basteln\`

**Nicht möglich (getestet 2026-08-18):** Pinterest-Pins scrapen (nur App-Shell, Pins hinter Login) · Facebook-Gruppen durchsuchen · Sets über die Kalender-YouTube-Videos identifizieren. → Patricia schickt Screenshots, Claude wertet aus.

**Harte Regeln:** nur vorhandenes Material vorschlagen · Dateipfade und IDs mitgeben · keine Nummern erfinden · keine Masse erfinden · doTERRA-Öle bleiben im Original-Etikett, keine Wirkversprechen · fremde Produktfotos nur in `context/persoenlich/` (Repo ist public).

### /berufswahl (Familie, seit 2026-09-03)

**Zweck:** Richtungs-Kompass für einen Jugendlichen aus Patricias Familie, der noch keine Idee hat, in welche Richtung er will. **Alle Personendaten** (Name, Alter, Klasse, Schule, Zielschule, Termine) liegen ausschliesslich in `context/persoenlich/berufswahl/` — gitignored, weil das Repo public ist. Skill und Wissensbasis bleiben personenfrei.

**Kein Berufstest.** Ein Interessentest in dem Alter misst vor allem, was jemand zufällig schon erlebt hat. Stattdessen sammelt der Skill über Monate/Jahre Datenpunkte auf **5 Achsen** (Material · Modus · Antrieb · Kontext · **Umsetzung**) und fragt konsequent nach **Tätigkeiten, nie nach Berufen**.

**8 Modi:** Start-Gespräch (einmalig) · Wochen-Impuls (2-4 Fragen, alle 1-2 Wochen) · Erlebnis nachbesprechen (5 feste Fragen nach Schnuppern/Kurs/Projekt) · Richtungen zeigen (ab ≥10 Beobachtungen, immer Gymi- UND Lehr-Weg) · Reinschnupper-Plan (genau ein nächster Schritt) · Eltern-Auswertung (2×/Jahr) · Gymi-Entscheid-Check · **Vertiefung Interessenbereich** (zerlegt einen Test-Label wie «Forschung» in etwas Testbares).

**Wissensgrundlagen** (in `context/berufswahl/`, public — keine persoenlichen Daten):
- `README.md` — Systemlogik, 4 Achsen, 10 harte Arbeitsregeln, realistischer Rhythmus
- `fragen-pool.md` — Start-Blöcke, Wochen-Rotation, Erlebnis-Fragen, **Abbruch-Nachbesprechung** (für Vorhaben, die nicht passiert sind), Umformulierungen bei „keine Ahnung", verbotene Fragen
- `bildungswege-ch.md` — 3 Hauptwege rückwärts gedacht, Übersetzungs-Tabelle Achse→Richtung→Weg, Gymi-Situation Appenzellerland/Ostschweiz
- **README zusätzlich:** 5. Achse «Umsetzung» · Ursachen-Tabelle a–e für «macht nichts fertig», inkl. **(e) Abhängigkeit** (konnte gar nicht allein anfangen) — zuerst (e) prüfen, sonst landet man reflexhaft bei Ursachen, die im Kind liegen · «Labels sind das Gegenteil von Hilfe» · Sonderfall «vielseitig Interessierter»
- `reinschnuppern-katalog.md` — Möglichkeiten in 4 Aufwand-Stufen + Anfrage-Vorlage
- `vertiefung-interessenbereiche.md` — pro Interessenbereich 4 **trennende** Fragen (Forschung, Technik, Informatik, Natur, Menschen, Wirtschaft, Gestaltung, Handwerk) + Regel 0: ein Test-Label ist eine Hypothese, kein Befund

**Persoenliche Daten** (in `context/persoenlich/berufswahl/`, **gitignored** — Repo ist public): `profil.md` · `erlebnis-log.md` · `richtungen.md` · `fertig-liste.md` (nur was fertig geworden ist — Gegengewicht zum Eltern-Label «der Theoretiker», in fünf Jahren mehr wert als jedes Interessenprofil) · `schnupper-plan.md` (Schnuppern variiert **das Medium, nicht das Thema** — jede Idee beantwortet eine offene Frage).

**Harte Regeln:** max 4 Fragen pro Runde · nie einen Beruf zuweisen (nur Hypothese + Test) · „keine Ahnung" ist gültig · nichts bewerten (Gamen ist ein Datenpunkt) · kein Druck im Ton · **keine erfundenen Termine/Fristen/Löhne** — immer per WebSearch auf berufsberatung.ch oder die Schul-Website · nach jeder Runde die Datei aktualisieren.

**Nächster Ausbaustufe (offen):** Telegram-Bot analog Garten-Bot, damit der Wochen-Impuls von selbst aufs Handy kommt.

### /mealplan

**Zweck:** Persönlicher Kochassistent und Meal Planning Bot starten.

Lädt das vollständige Briefing (`context/meal-planning-bot.md`) und startet den Kochassistenten. Kann:
- Wochenpläne erstellen (Mittag + Abend, 5-6 Personen, Protein-Tracking)
- Spontan-Kochen ("Ich hab X, Y, Z — was mach ich?")
- Einkaufslisten generieren (Migros-sortiert, Aktionen integriert)
- Projektmodus (Saürteig, Pasta, Meal Prep, Gartenverarbeitung)
- Wöchentliches Ernährungs-Coaching (Themenrotation)
- Quick-Archiv (Rezepte aus Fotos/Screenshots speichern)
- To-Go/Wandertag-Planung

Output wird in `outputs/mealplans/` gespeichert.

### /produkt

**Zweck:** All-in-One-Produkterstellung, Funnel-Bau und Launch-Management nach Julia Trosts Methodik — für Patricias Onlinebusiness (primär) und optional fürs Network (doTERRA).

**Drei Nordsterne:**
1. **40'000 CHF/Jahr-Ziel** — jeder Strategie-Output zeigt Umsatzbeitrag + Realitäts-Check (Kaufmengen).
2. **Jedes Produkt trifft EINEN markt-validierten Painpoint** — **Markt-Research-Phase vorher** (WebSearch auf Google Trends, Reddit, Social Media, KI-Welt).
3. **A→B→E→M→Z-Treppen-Logik** — Freebie (A→B) · Miniprodukt (B→E) · Mittleres (E→M) · Grosses (M→Z). Keine Überlappungen, ein Sprung pro Produkt.

**Notion-Produkte-DB** (`2ae7078e-8b7e-81ef-aafa-f03993ef344f`): Jedes erarbeitete Produkt wird als DB-Eintrag vorbereitet (Felder: Produktname/Typ/Status/Zielgruppe/Painpoint/Sprung/Learnings/Dauer/Preis/Module/Format/Launch-Datum/Umsatzbeitrag). Siehe `context/notion-produkte-db.md`. Notion-MCP noch nicht angebunden — aktuell Block-Output zum manuellen Übertragen.

Fragt IMMER zuerst: „Für welches Business?" (Onlinebusiness / Network). Lädt dann den passenden Kontext + Julia-Trost-Wissen. Arbeitet iterativ über 9 Modi:

1. **Produkttreppe entwerfen** — 4-Stufen-Strategie (0€ → Minikurs → Signature → Premium) mit Preisen, Titeln, Transformation, Abhängigkeiten
2. **Produktidee validieren** — Warmlist-Check, Pre-Sale, DM-Texte, Story-Umfragen („erst verkaufen, dann erstellen")
3. **Einzelprodukt entwickeln** — Modul-Outline + Canva-Folien + Sprechnotizen + Arbeitsblätter (.docx für Google Drive) + KI-Assistent-Check pro Kurs
4. **Preis-Validierungs-Zyklus** — 3-Stufen-Staffel (Secret/Early-Bird/Final) mit Timeline und Ankündigungs-Messaging
5. **Launch-Content-Kalender** — 7-Tage-Rhythmus × 6 Content-Typen × Käufer-Archetypen (Willi/Amelie/Ina/Zoe/Rudi/Frank), inkl. Mid-Launch-0€-Masterclass
6. **Funnel bauen** — Checkout + 2-3 Offer Bumps + Bundle + Upsell/Downsell + 5-Mail-Sequenz nach Julias Vorlagen
7. **Sales-Page (ThriveCart)** — ruft `/copywriting` (Format Landingpage) mit Vorbefüllung aus Produkt-Briefing auf
8. **Angebotsseite Homepage** — Textblöcke + Struktur für Patricias Website
9. **KI-Assistent für Kurs konzipieren** — GPT/Bot als Bonus/Upsell (Basis-Anleitung + Framework + System-Prompt + Test-Dialoge)

**Tool-Integrationen:** Canva MCP (`mcp__d7e69b1e-*`) für Präsentationen · docx-Skill für Arbeitsblätter (Google Drive) · optional Notion bei Launch-Kalender.

**Wissensgrundlagen:** `reference/julia-trost/methodik.md` (Pflicht) + alle Julia-PDFs (Produkterstellung, Launchen, Salespages, Email-Funnel, Minikurse, Secret-Offer, Automationen) + `context/patricia-expertise.md` (keine Dopplungen mit bestehenden Kursen!) + `context/Kurse/aktuelle kurse/` + `brand-voice.md` + `business-info.md`.

Output: `outputs/produkte/[slug]/` mit 10 Unterordnern/Dateien (siehe `outputs/produkte/README.md`).

### /story

**Zweck:** Daily Story Sales Companion — täglicher Story-Begleiter, der nach Julia-Trost-Methodik + Brandastic-Käufertypen + Nadja-Personas **fertige Story-Slides als PNG** in Patricias Brand liefert.

**Zwei Kernregeln:**
1. **Jede Story-Sequenz hat einen CTA-Link** — Freebie ODER bezahltes Produkt aus `active-funnels.json`. Keine Story ohne Verkaufsabsicht.
2. **Käufertyp-Rotation über die Woche** — alle 4 DISG-Achsen (Rot/Gelb/Grün/Blau) müssen jede Woche vorkommen.

**8 Modi:**
1. **Tagesplan** (Standard) — 3-5 Slides für heute aus deinem Input
2. **Sales-Day** — kompletter 24h-Verkaufstag während aktivem Launch (8-12 Slides)
3. **Story-Doktor** — aus roher Idee → Hook + Slide-Aufbau + CTA
4. **One-Slide-Tag** — Low-Effort, 1 Slide aus Julia/Nadja-Pool
5. **Story-Serie** — 3-7 Tage Story-Bogen mit Cliff-Hanger
6. **Behind-the-Scenes** — aus Foto/Erlebnis Slides + Verkaufsbrücke
7. **Highlight-Pflege** — Highlights ordnen + aktualisieren + Cover
8. **Reaktiv** — auf Reaktionen/Antworten reagieren

**Wissensgrundlagen** (in `context/`):
- `story-framework.md` — Zentrales Wissen, 8 Modi, Visual-Pipeline
- `julia-stories-die-verkaufen.md` — Slide-Struktur + 7 Storytelling-Regeln
- `julia-insta-stories-anleitung.md` — 10 Verkaufs-Templates
- `julia-story-ideen.md` — 3-Säulen-Bibliothek (Expertise/Inspiration/Persönlichkeit)
- `brandastic-kaeufertypen.md` — DISG (4 Typen) + AIDA
- `nadja-story-prompts.md` — 7 Käuferpersonas (Wilma/Werner/Isabell/Charlie/Petra/Stefan/Bärbel)

**Visual-Pipeline (Pfad B: HTML → PNG):**
- Skill generiert `slides.html` mit Templates aus `scripts/karussell-render/brand-stories.css` (8 Slide-Templates: Hook/Story-Text/Zitat/Frage/CTA/BTS/Vorher-Nachher/Countdown)
- `render-stories.js` rendert PNGs (1080×1920) — direkt Instagram-Story-postbar
- Brand-Variants: Mentoring (Petrol-Akzent) vs. doTERRA (Orange-Akzent)
- Foto-Auswahl aus `context/Shootingbilder/`

**Notion-Anbindung:**
- Skill liest Wochenplan aus Wochenplanung-DB (`collection://2ae7078e-8b7e-81e7-9083-000b01908eb5`)
- Liest `Fokus der Woche` + Body-Tabelle „Was planst du je Business-Säule?" → Content-Creation
- Cache in `outputs/stories/wochen-kontext-KW##.json`

**Output:** `outputs/stories/YYYY-MM-DD-[modus]-[profil]-[slug]/` mit `briefing.md` + `slides.html` + `slides-png/`

**Beispiel-HTML mit allen 8 Templates:** `outputs/stories/_template-beispiel/slides.html`

### /hormozi und /salespage — archiviert (02.10.2026)

Beide sind in **`/copywriting`** aufgegangen und liegen unter `reference/_archiv-skills/`. Die Hormozi-Bibel (`reference/hormozi/copywriting-bible.md`) bleibt als Verstärker zum Nachschlagen und wird von `/content`, `/karussell`, `/reels`, `/story`, `/produkt`, `/funnel` und `/copywriting` weiter gelesen. Bisherige Ausgaben bleiben in `outputs/hormozi/` und `outputs/salespages/`.

### Salespage-Designs — 4 fertige Verkaufsseiten-Baukästen (seit 2026-09-13)

**Zweck:** Wo `/copywriting` die **Texte** liefert, liefern diese vier
Skills eine **komplette gestaltete HTML-Seite**. Sinnvolle Reihenfolge bei einem neuen
Produkt: erst `/copywriting` für die Texte, dann das passende Design für die Seite.

Aufruf im Chat, kein Slash-Command: „Bau mir eine Verkaufsseite für [Produkt] im
Signature-Design."

| Skill | Look | Wofür |
|---|---|---|
| `minikurs-salespage` | hell + verspielt · Petrol-Flächen, Orange-Knopf | Minikurse 19–39, Freebies, Vorlagen |
| `signature-kurs-salespage` | hell + editorial · Creme + viel Foto, Petrol-Anker | Flaggschiff-Kurse ab 97, mit Ratenzahlung |
| `skill-salespage` | dunkel + technisch · Dunkelblau, Petrol leuchtet | Bots, Tools, Vorlagen-Pakete |
| `ki-salespage` | dunkel + laut · Dunkelblau, Orange leuchtet | KI-Produkte, Assistentinnen |

**Alle vier sind auf Patricias Marke umgeschrieben** — Petrol/Dunkelblau/Creme/Orange,
Philosopher + Source Sans 3. Kein Gold, kein Pink, kein Gelb. Unterschieden werden sie
über Helligkeit, Bildanteil und Rhythmus, nicht über Fremdfarben.

**Vier Regeln der Ursprungs-Vorlage sind gedreht** (steht als Vorrang-Block oben in
jeder `SKILL.md`): Kundinnen statt Kunden · **nichts erfinden** statt „plausible
Beispielwerte" · **keine Geld-zurück-Garantie** · Schweizer ss.

🚨 **Die vier Skill-Ordner und `reference/salespage-designs-original/` sind gitignored.**
Gekauftes Fremdmaterial, und das Repo ist öffentlich. Wiederherstellbar über zwei
versionierte Skripte:

```bash
python scripts/salespage-design/marke-anpassen.py && python scripts/salespage-design/regeln-anpassen.py
```

Sicht-Prüfung: `node scripts/salespage-design/vorschau-rendern.mjs` → acht Bilder je
Design nach `outputs/salespage-designs/vorschau/` (ebenfalls gitignored).

Volle Doku: `scripts/salespage-design/README.md`.

### /karussell

**Zweck:** Instagram-Karussells planen, bauen und fixen — mit Folien-Plan, Feed-Aesthetic-Check und Notion-Integration.

Zwillingsbruder von `/reels`. Fragt IMMER zürst das Profil ab (Mentoring vs. doTERRA), prüft Canva-Grid-Farben für Feed-Aesthetic-Rotation, baut Hooks strikt nach `.claude/skills/hooks/SKILL.md`, legt Notion-Einträge in der Content-Management-DB an.

**Seit 2026-09-10 (Jenya-Kork-Guide eingearbeitet):** vier feste Karussell-Typen
(Listicle · Storytelling · Edukativ · Kontroverser Take — bei letzterem ist die
**Nuancierungs-Folie Pflicht**), **Funnel-Stufe** TOF/MOF/BOF als Pflicht-Frage,
und vor allem **Schritt C2: Texte freigeben lassen, bevor irgendetwas gebaut
wird**. Gezielt korrigieren („nur Folie 4, Rest bleibt") statt alles neu rendern.
Was Patricia zweimal korrigiert, wird Regel in `karussell-framework.md`.
Bewusste Abweichung vom Guide: **keine KI-Bilder** — Folien kommen aus der
HTML-Render-Pipeline mit echten Fotos, dadurch ist der Text gesetzt statt
gezeichnet (keine verrutschten Buchstaben).

6 Modi:
- Karussell-Konzept aus Idee (komplettes Folien-Briefing)
- Rohmaterial → Karussell (aus vorhandenen Canva-Assets)
- Hook-Brainstorm (10 Varianten)
- Karussell-Doktor (Kritik + 3 Fixes)
- Wochen-Plan (3-5 Ideen)
- Batch-Design-Mode

Wissensgrundlagen: `context/karussell-framework.md` + alle Reels-Grundlagen.

Output: `outputs/karussells/YYYY-MM-DD-[slug].md` + Notion-Eintrag.

### /reels

**Zweck:** Reel-Videos planen, bauen und fixen — mit sekunden-genaün Briefings.

Patricias Reel-Produzent. Fragt **immer zürst** das Profil ab (Onlinebusiness/Mentoring vs. Network/doTERRA), recherchiert aktuelle virale Formate auf anderen Kanälen (WebSearch IG/TikTok/FB), baut Hooks strikt nach `.claude/skills/hooks/SKILL.md`, nutzt bevorzugt Patricias eigene Canva-Videos und ergänzt mit Stock-B-Roll. Wenn nötig gibt er konkrete **Dreh-Anweisungen** mit exaktem zu sprechenden Text.

5 Modi:
- **Reel-Konzept aus Idee** — volles Briefing (Hook + Shotlist + Dreh-Anweisung + Caption + CTA + 5 Hashtags)
- **Rohmaterial → Reel** — Cut-Reihenfolge aus vorhandenen Clips
- **Hook-Brainstorm** — 10 Hook-Varianten nach Framework
- **Reel-Kritik / Reel-Doktor** — Diagnose + 3 konkrete Fixes
- **Wochen-Reel-Plan** — 3-5 Reel-Ideen

Wissensgrundlagen:
- `context/reels-framework.md` — Viral-Mechanik 2026, 3-Sek.-Regel, Reel-Typen, Hook-Pflicht-Prozess, Talking-Head-Anweisungen, Caption-Strategie, Top-5-Hashtags pro Profil
- `context/brand-voice.md` / `.claude/skills/hooks/SKILL.md` / `context/caption-formeln.md`
- `reference/julia-trost/methodik.md` + `Reels to Cash.pdf` + `Stories die verkaufen.pdf` (Kaufpsychologie in Captions)

Output wird in `outputs/reels/` gespeichert.

### /funnel

**Zweck:** Funnel-Stratege für Mum Life Balance. Plant, baut und orchestriert komplette Funnel über 5 Modi: Strategie · Bauen · Werbeanzeigen · Launch · Analyse.

Live seit 2026-04-24. Verbindet alle 7 Systeme: WordPress (`/wp`) · ActiveCampaign (MCP) · ManyChat (Pro-API) · Thrivecart · Notion Produkte-DB · Canva (MCP) · Content-Assistenten (`/content`, `/reels`, `/karussell` lesen `context/active-funnels.json`).

**Wissensbasis:**
- Komplette Julia-Trost-Kurs-Transkripte (`reference/julia-trost/Transkripte Videocalls/_sortiert/`): Leadgewinnung, Werbeanzeigen (IG Reichweiten Booster), Magnetisch Verkaufen, Automationen, 100k Blueprint, Online Business Academy, Digitale Produktwelt, Instagram Story Strategie, ARIA (KI), Forever Fans, Minikurse als Umsatzbooster, 16 Kurse für 15€
- Alle Julia-Trost-PDFs (Mail-Vorlagen, Salespages, Launch Queen, Produkttreppe, Secret Offer, Checkout, Webinar-Skript)
- Patricia's komplette Kurs-Wissensbasis + Brand-Regeln + Memory-Feedback

**Aktuelle Funnels (Register `context/active-funnels.json`):**
Bio-Check · Lead-Challenge · Workbook „Von 0 auf echt" · 0€ Potenzial-Test · 0€ Starterguide · Story-Challenge · doTERRA Energie-Kur.

**Ablauf:**
1. User tippt `/funnel` → Skill fragt Modus (Plan / Bau / Ads / Launch / Analyse / list)
2. In Mode 3 (Ads) ALS PFLICHT-SCHRITT 0: Painpoint-Analyse (AC-Signale + Instagram-Engagement + DMs + Reddit/Google-Trends) → empfiehlt passenden Funnel zum Bewerben
3. Output in `outputs/funnels/[slug]/` und Update `active-funnels.json`

### /jahresplan

**Zweck:** Master-Jahres-Sicht über alle Launches/Produkte/Kampagnen — verknüpft mit Notion-Jahresplanung-DB. Wird von `/content`, `/reels`, `/karussell`, `/funnel` als Wochen-Kontext gelesen.

**Status:** SPEC angelegt am 2026-05-01 — Implementierung folgt in nächster Session sobald Patricia die Notion-Jahresplanung-DB-ID liefert.

**5 Modi:**
1. `/jahresplan status` — „Wo stehe ich heute?" (aktuelle KW + parallele Produkte + nächste Meilensteine)
2. `/jahresplan launch [slug]` — neuen Launch ins Master-Markdown + Notion eintragen
3. `/jahresplan vorschau [monat]` — Monats-Sicht mit Konflikten
4. `/jahresplan konflikt-check` — überlappende Aktivitäten identifizieren
5. `/jahresplan notion-sync` — manueller Sync mit Notion-Jahresplanung-DB

**Datenfluss:** `/produkt` → `outputs/produkte/[slug]/07-launch-kalender.md` → `/jahresplan launch` → `context/jahresplan-2026.md` ←→ Notion. Phase-Marker maschinenlesbar in `context/active-funnels.json`.

**Volle Doku:** `.claude/skills/jahresplan/SKILL.md`.

### /wp

**Zweck:** WordPress-Helfer für `mumlifebalance.ch` — Seiten erstellen, aktualisieren, Medien hochladen, Menüs pflegen. Vollautomatisch via REST API.

Live seit 2026-04-24. Admin-Vollzugriff (Patricia, ID 2). Credentials in `scripts/wordpress/.env` (gitignored).

Typische Use-Cases:
- „Erstelle eine Angebotsseite für [Produkt]" → neue WP-Seite als Draft mit Patricia-Voice + Brand-Farben
- „Aktualisiere die Über-mich-Seite mit [Text]" → In-Place-Update
- „Lade Foto [X] hoch und nutze auf Seite [Y]"
- „Liste alle Seiten auf" · „Veröffentliche [slug]" · „Zeig mir Seite [slug]"

**CLI-Helper** `scripts/wordpress/wp-api.js`:
```bash
cd scripts/wordpress && node --env-file=.env wp-api.js <command>
```
Commands: `whoami`, `list-pages [search]`, `get-page <id/slug>`, `set-status <id> <publish|draft|private|trash>`, `delete-page <id>`, `upload-media <pfad>`, `list-media`, `list-menus`

**Node-Module** mit allen Funktionen importierbar — siehe `scripts/wordpress/wp-api.js`.

**Regeln:**
- Neue Seiten IMMER als `status: draft` → Patricia prüft und publiziert selbst
- Landingpages in Patricia-Brand (Creme #f1ecdd + Philosopher + Source Sans 3 + Schaufenster-Metapher + Transformation-Sprache)
- HTML-Content in `<!-- wp:html -->` verpacken (Gutenberg)
- Fotos aus `context/Shootingbilder/` bevorzugen (100+ authentische)
- Bei bestehender Slug: `createOrUpdatePage()` — updatet statt dupliziert

Bereits deployed: `https://mumlifebalance.ch/bio-check` (Seite 3346).

---

### /copywriting (zugekauft, seit 2026-10-02)

**Die eine Pipeline für Verkaufstexte** — Landingpage, VSL-Skript, Mail-Sequenz,
Anzeigentext, Sales Letter. Übernommen, wie die Mentorin sie liefert (Briefing-Check →
Awareness-Stufe 1–5 → Lead-Typ + Framework → Draft → 4 Prüf-Layer inkl. Anti-KI-Check
mit 13 Markern), ergänzt nur um Patricias Daten:
`.claude/skills/copywriting/BRAND-VOICE.md` und `ZIELGRUPPE.md` sind ausgefüllt
(Stimme, Verbote, echte Beweise, Preise aus ThriveCart, beide Profile, Einwände).

**Vorrang-Block oben in der `SKILL.md`** — fünf Stellen, an denen Patricias Regeln
gewinnen: keine Geld-zurück-Garantie · Hooks über den Hook-Skill · zwei
Zielgruppen-Ebenen · Marktbezug Pflicht · Blackliste/`texte-pruefen.py` zusätzlich.
„Kein Monat ohne Verkauf" ist seit Interview A1 (02.10.2026) geklärt: bevorzugt
*„keinen Monat mehr ohne Einkommen aus meiner Selbständigkeit"*, doTERRA zählt mit.
„Vierstellig pro Monat" ist seit A1b gestrichen (stimmt ohne Launch nicht).

🚨 **Julias Text bleibt Wort für Wort** (Patricia, 02.10.2026: *„nichts wird
überschrieben von julias inhalt. ich will mich grundsätzlich an ihren skill halten. sie
hat ja erfolg damit"*). Eigenes steht nur in zwei markierten Ergänzungen: dem
Vorrang-Block oben und dem Abschnitt **„ThriveCart-Tipps"** unten (der frühere
`/salespage`: Interviewfragen, 13 Blöcke, Hormozi je Block, Ausgabeformat). Bei jeder
Änderung gegen `reference/copywriting-original/copywriting/SKILL.md` prüfen, dass keine
Zeile des Originals fehlt oder verändert ist.

🚨 **Gitignored** (`.claude/skills/copywriting/`, Original in
`reference/copywriting-original/`) — Fremdmaterial, Repo public, keine Anleitung.md.
Ändert sich `context/brand-voice.md` oder ein Preis, die beiden Dateien nachziehen.

### /facebook-ads (zugekauft)

**Zweck:** Meta-Werbung (Facebook/Instagram) nach **Kevin Fiedlers „Facebook Ads Lab"**-Testsystem — Testkampagne, 4S-Copy-Formel, Analyse-Tabelle, Skalierung, AOV.

Dran, wenn Patricia eine Meta-Anzeige **planen, texten, aufsetzen, auswerten oder skalieren** will. Kevin ist der Struktur-/Test-Layer; Patricias Marke + Regeln haben Vorrang (Freundin-Voice, Schweizer ss, keine erfundenen Zahlen; **Anzeigen verlinken immer auf die eigene Domain** `mumlifebalance.ch/<slug>` mit Pixel, nie direkt auf ThriveCart; Ziel-Link vor Start per `curl -I` testen). **Seit 02.10.2026 die eine Stelle für Meta-Anzeigen — Text und Kampagne.** Am Ende zwei
wörtlich übernommene Ergänzungen: der frühere `werbeanzeigentext-master` (Briefing,
Hook-Längen je Platzierung, 5 Angles, Überschriften und Beschreibungen, DACH-Trigger,
Testen) und Julias Copywriting-Pipeline (Briefing-Check, Bewusstseinsstufe, Pre-Flight
Layer 2–4, Anti-KI-Check). Reihenfolge bei Widerspruch: Vorrang-Block → Kevin → Julia →
Werbeanzeigentext Master. Kevins Text und die Ergänzungen sind unverändert.

🚨 **Gekauftes Fremdmaterial** (Transkripte in `context/Kurse/aktuelle kurse/Kevin-Facebook-Ads-Lab/`, gitignored) → **keine Weitergabe-Anleitung.**

### /freebies-sync

**Zweck:** Freebies / 0€-Produkte / Workbooks / Challenges aus `context/freebies/` in die zentrale Wissensdatei `context/patricia-freebies.md` synchronisieren — damit die Content-Skills nicht nur den Titel, sondern die **Inhalte** eines Freebies referenzieren können. Aufrufen, wenn ein neues Freebie dazugekommen ist.

### /kurse-sync

**Zweck:** Neues Kurs-Wissen aus `context/Kurse/aktuelle kurse/` in `context/patricia-expertise.md` synchronisieren (neue Kurse oder neue Lektionen, mtime-geprüft, Explore-Agent pro Kurs). Aufrufen, wenn Patricia einen Kurs neu ablegt oder um Lektionen erweitert — hält die Expertise-Basis aktuell, ohne Dopplungen mit bestehenden Kursen.

### /visuals

**Zweck:** Design-**Bauplan** für die Visuals (Canva-ready) — Cover, Inhalts-Folien, Reel-Standbilder. **Erzeugt keine Bilder**, sondern sagt Folie für Folie, was in die Canva-Vorlage kommt. Feste Regeln: **keine KI-Bilder**, ABAB-Feed-Rhythmus (Template↔Foto), Cover-Farbe rotieren, Gesicht/Hauptmotiv frei, Lead-Post nie dunkel-vollflächig. (Für fertig gerenderte Bilder statt Bauplan → Bild-Editor / Cockpit.)

## Kritische Anweisung: Diese Datei pflegen

**Wann immer Claude Änderungen am Workspace macht, MUSS Claude prüfen, ob CLAUDE.md aktualisiert werden muss.**

Nach jeder Änderung — ob Commands, Skripte, Workflows oder Strukturänderungen — frage:

1. Fügt diese Änderung neue Funktionalität hinzu, die Benutzer kennen müssen?
2. Ändert sie die oben dokumentierte Workspace-Struktur?
3. Sollte ein neuer Command aufgelistet werden?
4. Braucht context/ neue Dateien dafür?

Falls ja, aktualisiere die entsprechenden Abschnitte. Diese Datei muss immer den aktuellen Zustand des Workspace widerspiegeln, damit zukünftige Sessions genaün Kontext haben.

**Beispiele für Änderungen, die CLAUDE.md-Updates erfordern:**

- Neuen Slash-Command hinzufügen → im Commands-Abschnitt ergänzen
- Neuen Output-Typ erstellen → in Workspace-Struktur dokumentieren oder Abschnitt erstellen
- Skript hinzufügen → Zweck und Verwendung dokumentieren
- Workflow-Patterns ändern → entsprechende Dokumentation aktualisieren

---

## Für Benutzer, die dieses Template herunterladen

Um diesen Workspace an deine eigenen Bedürfnisse anzupassen, fülle deine Kontext-Dokumente in `context/` aus und passe sie nach Bedarf an. Verwende dann `/create-plan` zum Planen und `/implement` zum Umsetzen struktureller Änderungen. So bleibt alles synchron — besonders CLAUDE.md, die immer den aktuellen Zustand des Workspace widerspiegeln muss.

---

## Session-Workflow

1. **Start**: `/start` ausführen, um Kontext zu laden
2. **Arbeiten**: Commands verwenden oder Claude direkt mit Aufgaben beauftragen
3. **Änderungen planen**: `/create-plan` vor größeren Ergänzungen verwenden
4. **Umsetzen**: `/implement` zum Ausführen von Plänen verwenden
5. **Pflegen**: Claude aktualisiert CLAUDE.md und context/ während sich der Workspace weiterentwickelt
6. **Ende**: `/shutdown` räumt auf, zieht Doku nach, committet und pusht

---

## Scripts

### Karussell-Render-Pipeline (`scripts/karussell-render/`)

**Pfad B: HTML als Single-Source-of-Truth → 11 Instagram-PNGs (1080×1350, 4:5).**

Rendert eine Karussell-HTML-Vorlage zu Instagram-postbaren PNG-Folien. Ersetzt den Canva-AI-Generate-Weg (der das erarbeitete Design nicht 1:1 nachbauen konnte — Canva-API erlaubt u.a. keine Font-Family-Änderungen via `perform-editing-operations`).

- **Sprache:** Node.js 18+ (ES Modules), Puppeteer 23
- **Setup:** `cd scripts/karussell-render && npm install`
- **Nutzung:**
  ```
  node render.js --input="../../outputs/samples/karussell-<slug>.html" --slug=<slug>
  ```
- **Defaults:** Input = `outputs/samples/karussell-v3-preview.html`, Output = `outputs/karussells/renders/YYYY-MM-DD-<slug>/`
- **Output:** `01.png`, `02.png`, …, `11.png` — alle exakt 1080×1350, direkt Instagram-postbar
- **CSS-Zoom-Trick:** Die HTML-Vorlage ist für 340px-Grid-Anzeige designed. Render-Script injiziert `zoom: 3.1765` auf `.slide`, damit Chromium alles proportional auf 1080×1350 hochskaliert (Fonts, Padding, Positionen).
- **Image-Loading:** Warte explizit auf alle `<img>`-Elemente (file://-Bilder werden sonst nicht von `networkidle0` erfasst).

**Pipeline-Integration:** Wird von `/karussell` Schritt D nach dem Briefing getriggert.

**Phase 2 (geplant):** Nach dem Rendern werden die 11 PNGs automatisch als editierbares Canva-Design hochgeladen (via `upload-asset-from-url`), damit Patricia Feinjustierungen im Canva-UI machen kann.

### Apify Konkurrenz-Scraper (`scripts/apify/`, live seit 2026-05-07)

**Echte Instagram-Daten via GitHub Actions Cron** — löst die Sandbox-Limits-Lücke. Kein Token-Reset zwischen Sessions, weil Apify-Token als GitHub Repo-Secret lebt.

**Zwei Workflows:**

#### A) Watchlist-Scrape (`apify-scrape.yml`) — täglich
- **Cron:** täglich 06:00 Schweiz
- **Input:** `context/competitor-watchlist.json` (definierte Konkurrenz-Accounts)
- **Output:** `outputs/apify-runs/competitors-YYYY-MM-DD.{json,md}` — Profil + 25 letzte Posts mit Engagement
- **Manueller Ad-hoc:** GitHub UI → Run workflow → optional Komma-Liste an Handles
- **Actor:** `apify/instagram-profile-scraper`
- **Kosten:** ~1.80 USD/Monat bei 6 Accounts täglich

#### B) Creator-Discovery (`apify-discover.yml`) — monatlich + on-demand
- **Cron:** 1. des Monats, 06:00 Schweiz
- **Input:** `context/discovery-keywords.json` (Hashtags pro Nische: Mentoring + doTERRA)
- **Output:** `outputs/apify-runs/discovery-YYYY-MM-DD-{niche}.{json,md}` — ranked List der Top-Creator unter Nischen-Hashtags, Top-25 mit Profil-Daten angereichert
- **Manueller Trigger:** GitHub UI → "Apify Creator Discovery" → niche=both/mentoring/doterra
- **Actors:** `apify/instagram-hashtag-scraper` + `apify/instagram-profile-scraper`
- **Kosten:** ~1.50 USD pro Lauf
- **Zweck:** Findet die ECHTEN Top-Creator deiner Nische (statt geraten zu werden) — Score = `Hashtag-Erscheinungen × 1000 + Total-Likes`

**Wenn ein Skill aktuelle Konkurrenz-Daten braucht:** das jüngste `outputs/apify-runs/competitors-*.json` lesen (sortiert nach Datum). Älter als 36h → WebSearch-Fallback und Hinweis an Patricia.

**Wenn ein Skill die Top-Performer einer Nische braucht (z.B. neue Hook-Trends):** das jüngste `outputs/apify-runs/discovery-*-{niche}.json` lesen.

#### C) Telegram-Digest (`apify-telegram-digest.yml`) — wöchentlich (live seit 2026-06-30)
- **Cron:** Sonntag 19:00 Schweiz (`0 17 * * 0`) + `workflow_dispatch` für Sofort-Test
- **Script:** `scripts/apify/telegram-digest.js` (ESM, nur `fetch`, keine npm-Pakete)
- **Was es tut:** liest den neuesten `competitors-*.md`, lässt **Claude (`claude-opus-4-8`, raw HTTP) als Konkurrenz-Scout** die relevanten Erkenntnisse + 1-2 Content-Ideen rausziehen (Patricia-Voice) und schickt sie per **Telegram** an Patricia. Schliesst die Lücke, dass der tägliche Scrape bisher ungesehen im Repo lag.
- **Secrets:** `ANTHROPIC_API_KEY` + `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID` (alle bereits vorhanden)
- **Sofort testen:** GitHub UI → „Apify Telegram Digest" → Run workflow.

Plan: `plans/2026-05-07-apify-mcp-integration.md`.

### Instagram-Zahlen (`scripts/instagram-insights/`, live seit 2026-09-14)

**Holt Reichweite, Speicherungen und Geteilt-Zahlen pro Beitrag** über die Meta
Graph API — genau die Zahlen, die sonst nur in der Instagram-App stehen und
deshalb nie in der Notion-Content-DB landen. Schliesst die Lücke, dass jeder
Monatsrückblick bisher ohne Content-Performance auskommen musste.

```bash
python scripts/instagram-insights/holen.py              # letzte 25 Beiträge
python scripts/instagram-insights/holen.py --storys     # nur aktive Storys
```

Output: `outputs/instagram-insights/JJJJ-MM-TT.md` + `.json`. Nur
Python-Standardbibliothek.

🚨 **Storys laufen nach 24 Stunden ab.** Instagram gibt Story-Zahlen nur
heraus, solange die Story aktiv ist — wer zwei Tage später schaut, bekommt sie
nie mehr. Für dauerhaftes Story-Tracking muss das Skript **täglich abends**
laufen (GitHub Action, Muster `apify-scrape.yml`). Beiträge dagegen sind auch
Wochen später abrufbar.

**Zugang:** `META_ACCESS_TOKEN` aus `scripts/meta-ads/.env` — kein Schlüssel im
Code. Der Token **läuft alle 60 Tage ab** (aktuell bis 13.11.2026), Erneuerung
Schritt für Schritt im README.

**Zwei Stolpersteine, die Zeit gekostet haben:**
- `instagram_business_account` kommt **nur mit dem Seiten-Token** zurück, nicht
  mit dem Nutzer-Token — auch wenn die Verknüpfung besteht. Das Skript holt den
  Seiten-Token selbst.
- Eine Facebook-Seite trägt **genau ein** Instagram-Konto. Für beide Profile
  braucht es beide Seiten.

**Offen:** Das doTERRA-Profil @patricia_ulmann hängt noch nicht als
Professional-Account an der Seite *Mama.energise* und kam im Freigabe-Dialog
nicht mit — sobald das steht, holt das Skript es ohne Änderung mit. Ausserdem
fehlt noch der Übertrag in die Content-Management-DB.

Doku: `scripts/instagram-insights/README.md`.

### Mails sortieren (seit 2026-10-01)

**Gmail** (pnulmann@gmail.com) über den Gmail-Connector: Labels `📰 Newsletter & Werbung`,
`💼 Business & Verkäufe`, `💰 Finanzen`, `🔐 Konto & Sicherheit`, `🔧 Technik & Bots`,
`🍎 Rezepte & Ernährung`, `doTERRA`, `Privat`, `INBOX/Garteninfos`. Werbung/Technik/Rezepte/Garten
werden archiviert, der Rest bleibt im Posteingang, ungelesen bleibt ungelesen.
**GMX und info@** sind nicht am Connector und werden nicht weitergeleitet (Patricias Wunsch) →
`python scripts/mail-sortieren/sortieren.py` (IMAP, Probelauf, mit `--los` scharf), dieselben Regeln
als Ordner `Sortiert/…`. Zugang in `scripts/mail-sortieren/.env`, Bericht nach
`outputs/mail-sortieren/` (gitignored). 🚨 Nie löschen, nie gelesen markieren. Doku im README daneben.
🚨 **GMX lässt keine weiteren Ordner zu** (`quota exceeded` beim CREATE) → dort gehen Belege nach
`INBOX/Rechnungen`, Betrug nach `INBOX/Zu löschen`, Pakete nach `Archiv` (Zuordnung `ordner` in `KONTEN`).
**Ziel (Patricia, 01.10.):** im Posteingang nur, was sie selbst prüfen muss. Gelesenes wandert nach
„Erledigt“ (GMX: `Archiv`, Gmail: Label `✅ Erledigt`), ausser Mails von Menschen jünger als 14 Tage.
**Läuft wöchentlich** als Scheduled Task `mails-sortieren-donnerstag` (Do 07:00, nur bei offener App).
🚨 **Fähigkeiten erst nach dem Login lesen** — info@ nennt MOVE/UIDPLUS vorher nicht, sonst wird nur kopiert.

### Belege und Steuer-Export (`scripts/finanzen/`, seit 2026-09-24)

**Patricia:** *„belege müssen aber mitabgelegt werden oder verknüpft werden.
muss das ja alles belegen"* — und sie hatte recht: Bis dahin gab es einen
**Index mit 32 Tabellenzeilen und keine einzige Belegdatei.** Bei einer
Nachfrage vom Steueramt zählt das Dokument, nicht die Liste.

| Skript | Job |
|---|---|
| `beleg-auspacken.py` | holt die PDF-Belege aus Gmail-RAW-Antworten, benennt sie, liest den Betrag aus dem PDF |
| `meta-werbekosten.py` | Werbeausgaben aus dem Meta-Werbekonto — kommen **nie** per Mail |
| `steuer-export.py` | ein Befehl → Ordner mit Übersicht, beide CSV, Lückenliste und Kopien aller Belege |
| `scripts/cockpit/steuer-fuer-cockpit.py` | dieselbe Bilanz je Jahr als `daten/steuer` fürs Cockpit |

```bash
python scripts/finanzen/steuer-export.py 2026 --zip
```

🚨 **Der Umweg über die Datei ist der ganze Trick beim Belegholen.** Eine Mail
mit zwei PDF-Anhängen sind rund 215'000 Zeichen base64 — das passt in keinen
Kontext. Mit `messageFormat: RAW` ist die Antwort zu gross und wird vom
Werkzeug **als Datei** abgelegt; genau die liest das Skript. Der Beleg kommt im
Original heraus, ohne je durch den Kontext zu laufen. Mit `PLAIN_TEXT` bekommt
man nur den Mailtext und keine Anhänge, mit `MINIMAL` nicht einmal den Betrag.

🚨 **Die Stripe-Links in der Mail verfallen.** „Download invoice" und „Download
receipt" antworten nach ein paar Wochen mit `HTTP 400 · This URL has expired` —
geprüft an einem Juni-Beleg. Der **Anhang** verfällt nicht. Wer sich auf den
Link verlässt, merkt es erst, wenn er den Beleg braucht.

🚨 **Ohne PDF ist die Mail der Beleg.** ManyChat hängt keines an und schreibt
die Rechnung in den Mailtext; die Originalmail wird als `.eml` abgelegt. Ein
selbstgebautes PDF daraus wäre kein Original mehr, sondern eine Abschrift.

🚨 **Rechnung und Quittung sind zwei Dateien, aber EIN Posten.** Stripe hängt
beide an. Nur die Quittung nennt den bezahlten Betrag, die Rechnung die
Leistung. Wer beide zählt, verdoppelt die Kosten. Gruppiert wird nach Datum und
Anbieter.

🚨 **Werbekosten fehlen, wenn man die Buchhaltung aus dem Postfach baut.** Meta
rechnet über das Werbekonto ab. Befund vom 24.09.2026: **CHF 834 allein 2026**,
davon stand **eine einzige Zeile** in den Büchern (Januar, aus Notion — und für
Januar weist das Werbekonto gar nichts aus, das gehört geprüft). Die Zahlen
holt die Schnittstelle, die **Rechnungs-PDFs nicht** — die liegen im Business
Manager unter Abrechnung und müssen von Hand dazu.

🚨 **`$37 .31`** — im PDF-Text steht ein Leerzeichen vor dem Punkt, weil die
Zahl dort aus zwei Stücken gesetzt ist. Ein Muster ohne Zwischenraum findet den
Betrag nicht, **und ein fehlender Betrag sieht aus wie ein fehlender Beleg**.

🚨 **Kein Gewinn, wo ein Beleg fehlt, und USD wird nie umgerechnet.** Dieselbe
Regel wie im Monatsbogen. Der echte Frankenbetrag steht auf der
Kreditkartenabrechnung und weicht vom Tageskurs ab; ein selbst umgerechneter
Betrag sieht aus wie ein belegter.

🚨 **Der ganze Export ist gitignored** (`outputs/finanzen/steuer-*/` **und**
`steuer-*.zip`). Die PDFs waren über `**/*.pdf` schon draussen — **das ZIP und
die `00-uebersicht.md` mit Umsatz je Produkt aber nicht.** Repo ist öffentlich.

**Der Knopf im Cockpit** steht unter „Zahlen & Ziele" ganz unten: je Jahr
Einnahmen, Kosten, Gewinn und **wie viele Posten keinen Beleg haben**, dazu die
Ausgaben als CSV. 🚨 Er gibt die **Zahlen** ab, nicht die Dateien — ein Artifact
kommt nicht an den Dateiordner, und das steht auch dort. Ein Knopf, der
„Steuer-Export" heisst und die Hälfte weglässt, ohne es zu sagen, ist schlimmer
als keiner.

🚨 **Google Play ist ein eigener Abrechnungskanal** (gefunden 24.09.2026,
weil Patricia sagte: *„ne microsoft 365 und meta verified habe ich immer noch"*).
Beide Abos laufen — aber der Absender ist `googleplay-noreply@google.com`, nicht
der Anbieter, und bezahlt wird per PayPal über **pnulmann@gmx.ch**, eine zweite
Adresse. Eine Suche nach `from:microsoft` findet nichts und lässt ein laufendes
Abo gekündigt aussehen. Belegt: **Microsoft 365 Personal CHF 9.95/Monat** und
**Meta Verified (Instagram) CHF 13.95/Monat**. Dort liegen auch CapCut, Telegram
Premium und **SKYWORK AI zu CHF 11 pro Woche** — die drei sind bewusst **nicht
gebucht**, weil die Zuordnung geschäftlich/privat offen ist.

🚨 **„meta" hat Meta Verified verschluckt.** Beim Nachtragen der Abos wurde
gegen Doppelbuchung mit dem ersten Wort des Namens geprüft — und `„meta" in
„meta ads"` ist wahr. Dadurch fehlte Meta Verified **in genau den Monaten mit
Werbung**, und die Ausgabe sah trotzdem plausibel aus. Jedes Abo trägt jetzt ein
eigenes Erkennungswort (`verified`, nicht `meta`). Dasselbe Muster wie beim
Download-Aufräumen: **ein zu kurzes Muster fängt zu viel.**

🚨 **Abgeleitet ist nicht belegt.** Bei einem monatlichen Abo mit festem
Preis und Belegen am Anfang und Ende des Zeitraums sind die Monate dazwischen
sicher — aber sie tragen `abgeleitet: true` und **keine Datei**. Ein
abgeleiteter Posten darf nie als nachgewiesen zählen.

**Stand 24.09.2026:** Juni–September lückenlos belegt, 29 Originalbelege.
Februar–Mai, Dezember/Januar und die Werbung stehen als Zahl da, **ohne Datei**
— 52 von 68 Posten. Einnahmen CHF 4'928, Ausgaben CHF 2'588 plus USD 1'784 offen.

---

### Cashflow-Tracker (`scripts/finanzen/`, live seit 2026-05-09)

**Monatliche Cashflow-Auswertung** für Patricias Business — kombiniert PayPal + Schweizer-Bank-Auszug zu einem Notion-Block für die Monatsplanung.

**Drei Stufen:**

#### Stufe 1 — Snapshot in Notion (manuell)
Beim `/monatsplan`-Lauf: was Patricia weiss in „Erkenntnis Kennzahlen-Analyse"-Property eintragen.

#### Stufe 2 — Manueller Workflow (CSV → Bilanz)
1. Patricia exportiert PayPal-Transaktionsbericht + Bank-Auszug als CSV
2. Ablegen in `context/finanzen/[YYYY-MM]/` (gitignored, sensibel)
3. Lauf:
   ```bash
   cd scripts/finanzen && npm install
   node parse-paypal.js 2026-04
   node parse-bank.js 2026-04
   node summary.js 2026-04
   ```
4. Output: `outputs/finanzen/[YYYY-MM]/cashflow-summary.md` mit Notion-Block zum Reinkopieren

**Bank-Format-Detection:** PostFinance, Raiffeisen, UBS, ZKB, Migros Bank automatisch erkannt. Andere Banken: `parse-bank.js` Funktion `detectFormat` erweitern.

#### Stufe 3 — PayPal-Automatisierung via GitHub Action (`paypal-monthly.yml`)
- **Cron:** 1. jeden Monats 06:00 Schweiz → holt Vormonats-Transaktionen
- **API:** PayPal Reporting API v1 (`fetch-paypal-api.js`)
- **Secrets:** `PAYPAL_CLIENT_ID` + `PAYPAL_CLIENT_SECRET` (PayPal Developer Live-App)
- **Output:** Raw-CSV als GitHub-Action-Artifact (90d retention, NICHT committed) + Bilanz-MD committed in `outputs/finanzen/`
- **Aktivierung:** siehe `plans/2026-05-09-cashflow-tracker.md` Stufe 3

**Sicherheit:**
- `.gitignore` blockt `context/finanzen/**` ausser README — Finanz-Daten landen NIE im Git
- Bilanz-MDs in `outputs/finanzen/` sind anonymisiert (IBAN/Konto-Nummern entfernt)
- Bank bleibt manuell (kein Open-Banking in CH)

**Wenn Patricia bei `/monatsplan` Cashflow-Bilanz braucht:** das jüngste `outputs/finanzen/[YYYY-MM]/cashflow-summary.md` lesen. Wenn fehlt: Patricia erinnern dass CSV-Export fehlt (Stufe 2) oder GitHub-Action nicht gelaufen (Stufe 3).

Plan: `plans/2026-05-09-cashflow-tracker.md`.

### ActiveCampaign MCP-Server (`04-projects/activecampaign-mcp/`, v2 seit 2026-06-12)

MCP-Server, der Claude direkten Zugriff auf ActiveCampaign gibt — registriert in `.mcp.json` als Server `activecampaign` (Tools: `mcp__activecampaign__*`). **24 Tools** in 6 Gruppen: Kontakte (suchen/details/anlegen/inaktive/non-opener/nach-Tag-löschen), Tags (list/create/`tag_contact`/`untag_contact`), Listen (list/`create_list`/`subscribe_to_list`/`unsubscribe_from_list`), Custom Fields (`list_custom_fields`/`set_custom_field`), Kampagnen (list/report/analyze/`create_campaign`/`send_campaign`), Automationen (list/`add_contact_to_automation`/`build_product_funnel`).

- **Credentials:** `04-projects/activecampaign-mcp/.env` (gitignored) — `AC_API_URL` + `AC_API_KEY`. Werden zusätzlich aus der `env`-Sektion in `.mcp.json` injiziert.
- **API:** V3 (`Api-Token`-Header) Standard; V1 (legacy) nur für `create_campaign`/Funnel-Mails (V3 liefert dort 405).
- **send_campaign nur auf expliziten Befehl** — sendet/plant echte E-Mails.
- **Kontakt-Tools** akzeptieren `contact_id` ODER `email`.
- **Migration:** ersetzt den Vorgänger unter `scripts/activecampaign-mcp/` (17 Tools) als Superset. Der alte Ordner bleibt nur, weil die `bulk-upload-*.mjs`-Skripte dort die Credentials aus `.mcp.json` lesen.
- **🟢 Für ALLE Skills verfügbar:** Die Tools sind global da (kein „Verbinden" nötig). Tool-Katalog mit Pflicht-Args + Listen-IDs + Limits: **`reference/activecampaign-mcp-tools.md`** — jeder Skill, der AC braucht (`/funnel`, `/cockpit`, `/produkt`, Bots), liest diese Datei statt zu raten.
- **Doku:** `04-projects/activecampaign-mcp/README.md`.

### Salespage-Design-Aufbereitung (`scripts/salespage-design/`, seit 2026-09-13)

Drei Skripte, die aus dem gekauften Design-Bundle vier markenkonforme Skills bauen.
Sie lesen **immer** aus `reference/salespage-designs-original/` und schreiben nach
`.claude/skills/` — mehrfaches Laufen schadet nicht.

- `marke-anpassen.py` — färbt die vier `reference-page.html` um (Rosé/Gold/Pink/Neon →
  Petrol/Dunkelblau/Creme/Orange) und tauscht sieben Fremdschriften gegen Philosopher +
  Source Sans 3. **`Space Mono` bleibt** im Skill-Design, weil der Terminal-Block ohne
  Festbreiten-Schrift zerfällt. Zwei Knopf-Verläufe wurden gegenüber der Vorlage
  abgedunkelt bzw. auf dunkle Schrift gedreht — sonst trägt die Schrift zu wenig
  Kontrast. Nicht zurückdrehen.
- `regeln-anpassen.py` — schreibt `SKILL.md` + `section-guide.md` auf Patricias Regeln
  um, setzt den Vorrang-Block obenauf und kopiert die handgeschriebenen
  `BRAND-CONFIG`/`BRAND-VOICE`/`ZIELGRUPPE` aus `vorlagen/` dazu.
- `vorschau-rendern.mjs` — acht Bilder je Design für die Sicht-Prüfung. Schaltet vorher
  die Einblend-Animationen scharf, sonst bleiben gefüllte Abschnitte im Bild leer.
  Puppeteer kommt aus `scripts/karussell-render/node_modules`.

⚠️ **Fallstrick beim Erweitern der Farbtabellen:** In den Vorlagen stehen HTML-Entities
wie `&#128293;` (🔥) und `&#215;` (×). Die sehen aus wie Farbwerte. Deshalb ersetzt das
Skript nur, was namentlich in seinen Tabellen steht — nie per Muster über alle
`#`-Werte — und prüft nach jedem Lauf, ob eine Entity beschädigt wurde.

Doku: `scripts/salespage-design/README.md`.

### Bastel-Set-Lookup (`scripts/basteln/`, seit 2026-08-18)

**Holt zu einer Scrapbook-Forever-Artikelnummer den Set-Inhalt und die Beispielkarten des Design-Teams.** Schliesst die Lücke „ich hab das Set, aber keine Idee dazu".

- **Sprache:** Node.js (ESM, nur `fetch` — keine npm-Pakete)
- **Nutzung:**
  ```bash
  node scripts/basteln/sf-lookup.mjs SF363
  node scripts/basteln/sf-lookup.mjs SF363 SF370 --bilder
  ```
- **Liefert:** Set-Name · Preis + Altpreis · exakte Inhaltsangabe mit Massen · URLs aller Beispielkarten (typisch 12 pro Set)
- **`--bilder`:** lädt die Beispielkarten nach `context/persoenlich/basteln-shopbilder/<Nr>/` (**gitignored** — Urheberrecht, Repo ist public). Claude liest sie und beschreibt die Techniken in eigenen Worten.
- **Shop:** epages, per `curl` erreichbar (kein Browser nötig). Mundart Stempel (Gambio) hat kein Nummern-System → dort Suchwort-Recherche.
- **Facebook-Gruppen sind nicht scrapebar** (Login-Wall + fremde Inhalte) → Screenshot-Weg, siehe `context/basteln/shop-recherche.md`.

### Digitales Bastel-Material durchsuchen (`scripts/basteln/digi-index.py`, seit 2026-09-02)

**Macht Patricias ~8'000 digitale Bastel-Dateien durchsuchbar** — Digistamps, Plotter-Vorlagen, Verpackungen, digitale Papiere. Schliesst die Lücke, dass `inventar-digital.md` nur die Themenwelten listet, nicht die einzelnen Motive.

- **Sprache:** Python 3 (nur Standardbibliothek)
- **Index aufbauen** (nach Materialzukauf):
  ```bash
  python scripts/basteln/digi-index.py --neu-aufbauen
  ```
- **Suchen:**
  ```bash
  python scripts/basteln/digi-index.py badewanne
  python scripts/basteln/digi-index.py schmetterling --limit 40
  python scripts/basteln/digi-index.py hochzeit --ordner
  ```
- **Umfang:** 5'251 Motive aus 292 Themenwelten (PNG/SVG/DXF mit gleichem Namen zusammengefasst). Sucht in Dateinamen **und** Ordnernamen.
- **Index:** `context/basteln/digi-index.json` — committed, dadurch auch ohne Zugriff auf den OneDrive-Ordner nutzbar
- **Quelle:** `C:\Users\pnulm\OneDrive\Dokumente\Patricia\Hobby\Basteln\`

**`/basteln` Modus 0 nutzt das Skript verbindlich** — nie aus `inventar-digital.md` raten, immer suchen.

### B-Roll bauen (`scripts/content/broll-bauen.py`, seit 2026-09-18)

**Ein Clip, ein Hook, sonst nichts** — das Format, das Patricia selbst postet.

🚨 **Seit 19.09.2026 laeuft das ueber denselben Generator wie die Sprechreels**
(`scripts/videoschnitt/textebene.py`). Vorher hatte das B-Roll ein eigenes
Textwerk aus ffmpeg-drawtext: schlichter Text, kein Schleier. Patricia dazu:
*„auch bei den anderen B-Roll Reels finde ich den Hook halt nicht schoen"* —
und als Referenz *„das B-Roll vom 3 Wege ohne Namensliste finde ich absolut
super"*. Genau das **ist** die Textebene. Jetzt gibt es **ein** Textwerk statt
zwei, und es ist das, das ihr gefaellt: Serifenschrift, weicher Schleier,
orange Akzentzeile, langsame Zoomfahrt.

```bash
python scripts/content/broll-bauen.py --clip 20260521_104644     --ab 1.0 --dauer 7.0 --auto     --text "Kann mir mal jemand erklaeren, warum im Network alle so tun,"     --betont "als waere der Anfang das Schwere?" --name kw39-m-mo-b
# Standbilder anschauen, dann dasselbe nochmal mit --rendern
```

`--text` ist die weisse Anlaufzeile, `--betont` die orange Wendung. Hat ein
Hook keine Wendung, bleibt `--betont` leer und es steht nur der weisse Block da.

🚨 **Der Hook steht ab Bild null, ohne Einblendung** (seit 29.09.2026, Patricia:
*„mich stört, dass der text erst später eingeblendet wird“*). Vorher kam er nach
0,3 s mit Fade, die orange Zeile noch später — ganz lesbar erst nach rund einer
Sekunde. Jetzt `ab_sek: 0` plus `sofort: true` im Hook (`textebene.py`, `hook_anims`).

🚨 **Es gibt KEINE Vorgabe „mittig" mehr.** Frueher hiess es `--y 0 = mittig`,
und bei einem Hochformat-Video **ist** die Mitte das Gesicht. Genau so sind am
18.09. zehn KW39-B-Rolls mit dem Hook quer ueber Patricias Gesicht entstanden —
die Regel „am echten Standbild entscheiden" stand da laengst in der Doku, aber
der bequeme Weg war der falsche. Jetzt bricht das Skript ohne `--hoehe` oder
`--auto` ab.

**`--auto` sucht die ruhigste Stelle** ueber zwei Groessen je Bildzeile:
**Struktur** (Helligkeitswechsel innerhalb der Zeile — Gesicht, Haare, Muster)
und **Bewegung** (Streuung ueber mehrere Bilder — die Wand steht still, der
Mensch nicht). Beide zeigen von der Person weg. Das ist ein **Vorschlag**, die
Abnahme bleibt das Standbild.

🚨 **`--auto` findet die ruhigste Zeile, nicht die freie** (gelernt 20.09.2026).
Steht die Person vor einer glatten Holzwand oder unter einer Decke, ist die
ruhigste Zeile **oben** — und genau dort ist ihr Kopf. Bei zwei von fuenf
KW39-B-Rolls lag der Hook auf Patricias Gesicht (`--hoehe 12.5` und `18.8`,
beide von `--auto` gesetzt). Es gibt keine Gesichtserkennung im Skript, und eine
Zahl, die ein Skript ausgerechnet hat, sieht genauso plausibel aus wie eine
gepruefte. **Jedes Standbild wirklich anschauen** — bei einem Porträt im
Hochformat sitzt das Gesicht typisch zwischen 13 und 40 %, der Block gehoert
dann auf 44–48 %. `12.5` (die Untergrenze) ist immer ein Warnsignal: dort ist
`--auto` an die Zonengrenze gelaufen, statt eine ruhige Stelle zu finden.

🚨 **Ein Clip ohne Tonspur rendert nicht** (20.09.2026). Das Konzept laeuft
sauber durch, der Render bricht ab mit `1 composition asset(s) do not match their
authored media element type` — dreimal, weil es kein Zufall ist. Ursache war ein
Handyvideo mit **nur einer Videospur** (`VID_20260411_101118_284`). Der Generator
legt das Video als Medienelement mit Ton an, und ohne Audiospur passt der Typ nicht.
Fix — eine stille Spur dazu, einmal umkodiert:
```bash
ffmpeg -i video/input/<clip>.mp4 -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=48000 \n  -shortest -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a aac -b:a 96k video/input/<clip>-ton.mp4
```
Pruefen laesst sich das vorher in einer Zeile — fehlt `codec_type=audio`, ist es der Fall:
`ffprobe -v error -show_entries stream=codec_type -of csv=p=0 video/input/<clip>.mp4`

🚨 **Kurze Quellclips kippen den Bau, ohne es zu sagen** (20.09.2026). Reicht
`--ab` plus `--dauer` bis ans Clip-Ende oder darueber, fehlt beim Standbild-Ziehen
das letzte Bild und der Lauf bricht mit einem `FileNotFoundError` auf eine
Einzelbild-Datei ab — dreimal hintereinander, weil es kein Zufall ist. Betroffen
waren `20260803_172338` (7.23 s) und `VID_20260411_101118_284` (5.60 s).
**Vor dem Bau die Laenge pruefen** und `--dauer` so waehlen, dass rund 0.2 s Rest
bleiben:
`ffprobe -v error -show_entries format=duration -of csv=p=0 video/input/<clip>.mp4`
Ein B-Roll von 5 Sekunden ist besser als keines — die Laenge ist verhandelbar,
das Clip-Ende nicht.

🚨 **Der Bauplan wird gespeichert** (`video/output/broll/<name>/bauplan.json`).
Bei den ersten zehn war er das nicht, und weil der Text eingebrannt ist, musste
der Quellclip per Bildvergleich zurueckgesucht werden. Eine Korrektur ist jetzt
eine geaenderte Zahl statt einer Rekonstruktion.

### Animiertes B-Roll und fertige Karussell-Bilder (seit 2026-10-12)

**Oktober-Plan 13.–30.10.:** `outputs/content/KW42/markt.md` (Ziel 3'000 Follower, Hebel, Entscheide:
Trial Reels täglich, keine Werbung, BIO 1×/Woche, Verlosung als Trial Reel) · `hooks.md` (Fassung 3:
Tresor-Formeln aus `reference/content-tresor-reichweitenherz.md`, **kein Set 1**, Mikro statt Makro,
Drei-Sekunden-Test, Du-Form erlaubt) · `beitraege-13-16.md`.
**B-Roll animiert** (Patricia 11.10.): `scripts/content/kw42-brolls.py` baut je Reel über
`broll-bauen.py` + `textebene.py` — Stil Marker/Serif im Wechsel (Serif nur Orange, Petrol/Dunkelblau
fallen im Kontrast durch), Marker-Balken wischt unter dem schon lesbaren Hook auf, Aufruf als Chip
mit Pop in den letzten 2,5 s (der `zusatz` wird beim Marker gar nicht gezeichnet), Verlosungs-Schritte
nacheinander. Neu in `textebene.py`: Element-Feld `umbruch` (langer Chip bricht um statt abzuschneiden).
Für den Upload mit crf 25 verkleinern (`video/output/broll/kw42-ig/`), Assets ≤ 15 MB.
**Karussells „richtig gebaut“:** `scripts/karussell-render/folien.mjs` (Philosopher + Source Sans,
`gross: true` für lesbare Fliesstexte) → JPEG-dataUrl je Folie nach `karussells/<id>/bilder/slide-NN`.
Die Freigabe nimmt diese Bilder statt neu zu zeichnen (`fertigeFolien`). Folienzahl muss zur Zahl der
`slides` passen. 🚨 Der Cockpit-Zeichner selbst kennt nur Georgia/Trebuchet und verkleinert den
Versalien-Hook nur nach Höhe, nicht nach Breite — ein langes Wort („NETWORK-EINKOMMEN“) läuft in
der Vorschau über den Rand; Leerzeichen nach dem Bindestrich lässt ihn umbrechen.
🚨 **Bis Version 97 nahm die Freigabe die fertigen Bilder NIE** — `fertigeFolien()` rief
`snap.forEach` auf, die Datenbank liefert `snap.docs`; der Fehler ging still im `.catch` unter.
Behoben in Version 98 (`patch-fertige-folien-docs.py`, setzt `patch-fertige-folien.py` vom 22.09. voraus). Gegenprobe nach jeder Freigabe:
`freigaben/<id>/bilder/slide-01` lesen und ansehen.

### Quellclip zurueckfinden (`scripts/content/quelle-finden.py`, seit 2026-09-19)

Fuer fertige B-Rolls **ohne** Bauplan: findet Quellclip und Startzeit ueber
Bildvergleich gegen `video/input/`.

```bash
python scripts/content/quelle-finden.py video/output/kw39/*.mp4
```

🚨 **Der Textbereich wird ausgeblendet.** Die helle Schrift liegt bei jedem
B-Roll an derselben Stelle und liesse sonst alle Clips gleich aehnlich aussehen.

🚨 **Ein ffmpeg-Aufruf je Clip, nicht je Einzelbild.** Der erste Anlauf brauchte
**8 Minuten 40** fuer zehn Reels, weil er 1'840 Mal ffmpeg startete. Mit einem
Aufruf je Clip und zwischengespeicherten Miniaturen (`video/output/_bildindex`)
sind es **17 Sekunden**.

**Zwei Stufen, weil eine nicht reicht:** der Index tastet alle zwei Sekunden ab —
das findet den richtigen *Clip*, aber die Startzeit liegt bis zu einer Sekunde
daneben. Die Feinsuche tastet danach nur noch den Gewinnerclip in 0.2-Schritten
ab. Ohne sie kam beim bekannten Testfall `--ab 0.0` statt der richtigen 0.9.

Unter Naehe 0.90 meldet das Skript „von Hand nachsehen" — bei zehn KW39-B-Rolls
traf das genau einen.


### Videoschnitt-Pipeline (`scripts/videoschnitt/`, live seit 2026-09-10)

Drei lokale Skripte hinter `/videoschnitt` — kein Upload, keine Kosten:

- `transkribieren.py` — faster-whisper (CPU) → `words.json` (Wort-Zeitstempel),
  `saetze.md` (nummerierte Sätze mit Pausen + Take-Gruppen), `cutlist-vorschlag.json`,
  `.srt`/`.txt`. Erkennt Doppel-Takes über Satz-Ähnlichkeit **und** Neuanlauf-Muster
  („Aber du hast keine … Aber du hast kein Thema…").
- `schnitt.py` — freigegebene `cutlist.json` → `rohschnitt.mp4` + `clips/NN.mp4`
  (alle mit identischen Encoding-Parametern, sonst scheitert das Zusammenfügen) +
  umgerechnete `untertitel.srt` + `words-schnitt.json` + `schnittprotokoll.md`.
- `kurzfassung.py` — `liste` schreibt eine bearbeitbare `schnittliste.md`
  (an/Winkel/von/bis/gesprochener Satz), `bauen` macht daraus die Abschnitte. Die
  **Luft vor dem Satz wird gesucht**, nicht gerechnet: rueckwaerts bis zur naechsten
  Stille, hoechstens 0.6 s.
- `aus-capcut.py` — nimmt Patricias CapCut-Export, transkribiert ihn **neu** und legt
  die Remotion-Textebene exakt darueber. Zoom-Abschnitte findet ffmpeg ueber die
  Szenenwechsel. Alle Abschnitte zeigen auf dieselbe Datei und tragen `abDatei`, das
  Reel.tsx als `trimBefore` durchreicht.
- `textebene.py` — baut aus `finish.json` ein HyperFrames-Projekt mit fünf Ebenen
  (Video mit Zoom → grosses Wort → freigestellte Person → kleine Zeile → Untertitel)
  und rendert mit `--rendern` zum fertigen MP4 in `finish/renders/`.
  Schriftgrösse skaliert automatisch; Person und Hintergrund bekommen identische
  Zoom-Bewegung; Untertitel weichen Einblendungen aus.

**Getestet 2026-09-10:** kompletter Durchlauf bis 1080×1920-MP4 mit Ton, mit Zoom
und wortgenauen Untertiteln, `hyperframes check` grün
(0 Fehler, 0 Warnungen, Kontrast 6/6 WCAG AA).

### Startklar — Handybildschirm ins Zoom-Video (`scripts/startklar/`, seit 2026-09-17)

**Der Kurs „Startklar" wurde über Zoom aufgenommen, die Handy-Klickanleitungen
parallel auf dem Handy** — ohne den Bildschirm in Zoom zu teilen. In den
Zoom-Teilen 2–5 ist deshalb nur Ton und Webcam, das Hauptbild ist schwarz.
`bauen.py` legt die passende Bildschirmaufnahme dort hinein: Handy links auf
voller Bildhöhe, Webcam daneben, Hintergrund Dunkelblau.

🚨 **Die Tonspur der Handyaufnahmen ist digital still (−91 dB)** — Samsung nimmt
nur den Medienton auf. Damit fällt die Synchronisation über Tonabgleich aus, und
der Versatz muss von Hand kommen. Die Startwerte in `sync.json` stammen aus dem
**Wortlaut im Zoom-Ton** („Wir starten wieder die Bildschirmaufnahme") und stehen
je Teil im Feld `notiz` — **nie einen Versatz ohne Beleg eintragen**.

🚨 **Die Zeitstempel in Samsung-Bildschirmaufnahmen sind Endzeiten, nicht
Startzeiten.** Mit „Start" überlappen sich zwei Aufnahmen, was nicht sein kann;
mit „Ende" geht die Reihenfolge lückenlos auf. Gegenprobe ist die **Uhr in der
Statusleiste** der Aufnahme selbst — die ist bei jedem Handyvideo der sicherste
Zeitanker.

**Eingepasst wird im Sync-Editor**, nicht im Chat: `preview_start
{"name": "startklar-sync"}` → Port 4382. Zeigt das Endlayout mit echtem Ton,
Regler plus `[`/`]` in 0,1-Sekunden-Schritten, läuft auf kleinen Vorschaudateien.
Das folgt derselben Regel wie der CapCut-Feinschnitt: **Claude hört den Ton
nicht**, also gehört das Einpassen dorthin, wo jemand hört.

`--probe` rendert nur 40 Sekunden ab 8 Sekunden vor dem Einblenden — Übergang
prüfen in einer halben Minute statt zwölf.

Ordner `video/startklar/` (gitignored, Repo ist public).
Doku: `scripts/startklar/README.md`.

**Die Texte fuer die Kursplattform** (ThriveCart Learn) stehen in
`outputs/produkte/instagram-startklar/10-kursplattform-texte.md` — Begruessung,
Werkstatt-Block, Modul- und Lektionstexte. Daraus baut
`scripts/startklar/text-fuer-kursplattform.py "Lektion 1.2"` das HTML mit
Absaetzen, Fettungen und Links; Titel und Text kommen getrennt, weil die
Plattform dafuer zwei Felder hat.

**Alle Texte auf einer Seite mit Kopier-Knopf:**
`python scripts/startklar/kopierseite-bauen.py` → `preview_start {"name": "startklar-texte"}`
(Port 4383). Jeder Abschnitt hat einen Knopf, der `text/html` **und** `text/plain`
per `ClipboardItem` ablegt — in der Plattform reicht dann Strg+V, Ueberschrift und
Fettungen kommen mit. Bei Lektionen und Modulen wird der **Titel getrennt**
ausgegeben, weil die Plattform dafuer ein eigenes Feld hat; bei Begruessung und
Werkstatt steht er als `<h2>` im HTML.

🚨 **Im Fliesstext `html.escape(..., quote=False)`** — sonst steht ueberall
`&quot;` statt eines Anfuehrungszeichens. Das wird zwar richtig angezeigt, ist
beim Nachbearbeiten aber unlesbar. Die Adresse im Link wird einzeln gesichert,
weil sie in ein Attribut geht.

**Der Kurs ist aufgenommen (18.09.2026)** — 13 Videos, 80 Minuten, in OneDrive unter
`Business/Kurse/Startklar`. `python scripts/startklar/transkribieren.py` legt daraus
Transkripte zu den anderen Kursen in `context/Kurse/aktuelle kurse/Startklar/Transkripte/`.
🚨 **Die Dateinamen muessen dem Muster `NN-lektion-M-L-titel` folgen**, sonst erkennt
`kurse-indexieren.py` Modul und Lektion nicht — die Titel stehen als Tabelle `TITEL` im
Skript, `--umbenennen` stellt vorhandene Dateien um. Mit `small` transkribiert; Eigennamen
und Schweizer Faerbung sitzen nicht immer („Schaufelstern" statt „Schaufenster"), fuer die
Suche reicht es. `--modell medium` waere genauer und dauert rund dreimal so lang.

🚨 **Die Werkstatt liegt an ZWEI Stellen.** Quelle ist
`outputs/produkte/instagram-startklar/04-arbeitsblaetter/startklar-werkstatt.html`,
ausgeliefert wird `scripts/startklar-service/public/index.html` (dieselbe Datei plus
HTML-Kopf). Wer nur die Quelle aendert, aendert nichts an dem, was die Kaeuferinnen
sehen. `python scripts/startklar/werkstatt-ausliefern.py` uebertraegt, danach
`cd scripts/startklar-service && npx vercel --prod`.

**An 26 Feldern liegt ein ausformuliertes Beispiel** mit Knopf „Als Start uebernehmen"
(`scripts/startklar/werkstatt-beispiele.py`, wiederholbar). Alle gehoeren derselben
erfundenen Person — **Sandra, Energie fuer Mamas ab 35**. Das ist Absicht: bei einem
anderen Thema je Feld sieht niemand, wie die Teile zusammengehoeren. Kein `placeholder`,
weil der beim Tippen verschwindet und sich nicht kopieren laesst.

🚨 **Anlass war ein falsches Verkaufsversprechen.** Die Salespage sagte „fertige
Beispiele fuer jedes Feld", die Werkstatt hatte 13 kurze Hinweise und **ein** Beispiel.
**Vor jedem Versprechen auf einer Verkaufsseite im Produkt nachzaehlen** — hier waren es
42 Felder, und die Zahl stand in zwei Minuten fest.

**Die Werkstatt ist live:** `https://startklar.mumlifebalance.ch` (geprueft
17.09.2026), der Pruef-Dienst dahinter laeuft auf
`startklar-service.vercel.app`.

**Der Zugangscode ist ein Sammelcode: `STARTKLAR_KUNDE`** (Patricias Entscheid
18.09.2026). Er steht im Kurs in der Lektion „Deine Werkstatt" — **nicht in der
Kauf-Mail**, dort kommt keiner mit.

🚨 **Der Code deckt nur die ausfuehrliche Rueckmeldung ab.** Die zwoelf
Stationen pruefen im Browser und laufen ohne Code — deshalb konnte Patricia am
18.09. einfach anfangen und hat sich gefragt, wozu der Code ueberhaupt da ist.
Nur der Block „Mein Blick drauf" geht ueber Claude und kostet je Aufruf.

🚨 **Geaenderte Vercel-Variablen greifen erst nach einem neuen Deploy** —
`npx vercel env rm/add` allein aendert am Live-Dienst nichts. Immer danach
`npx vercel --prod` und mit einem `curl` gegen `/api/pruefen` gegenpruefen.

🚨 **Es gibt aktuell KEINE Obergrenze.** `MAX_PRUEFUNGEN` greift nur mit
KV-Speicher, und bei Vercel haengen nur `ANTHROPIC_API_KEY`, `KONTAKT_HINWEIS`
und `ZUGANGSCODES` — kein `KV_REST_API_URL`. Wer den Sammelcode weitergibt,
kann das Guthaben verbrauchen. Vor einem groesseren Launch KV anhaengen.

Die Antworten der Kaeuferinnen liegen nur in deren `localStorage`; der Dienst
speichert nichts.

### Die Nachkauf-Strecke (`scripts/startklar/mails-bauen.py`, seit 2026-09-18)

**Acht Mails vom Kauf bis zur Uebergabe an die Engine**, erzeugt aus einem
Skript statt acht getippter Dateien — das Geruest (Outlook-Tabellen, Farben,
Fuss) ist ueberall gleich, und wer es achtmal kopiert, aendert spaeter siebenmal.

```bash
python scripts/startklar/mails-bauen.py          # alle Mails + Kopierseite
python scripts/startklar/mails-bauen.py --liste  # nur die Strecke anzeigen
```

Ausgabe nach `outputs/produkte/instagram-startklar/08-funnel/`, Ansicht ueber
`preview_start {"name": "startklar-mail"}` (Port 4386): je Mail eine Karte mit
Wartezeit, Betreff und Knoepfen fuer ganzes HTML, nur Rumpf und Betreff.

| Tag | Wartezeit | Job |
|---|---|---|
| 0 | sofort | Auslieferung |
| 2 | +2 Tage | Bio-Station, damit sie dranbleibt |
| 4 | +2 Tage | **der Tipp** — Frage in Zeile eins, 2,6× gemessen. Kein Verkauf |
| 6 | +2 Tage | erstes Reel, sieben Sekunden |
| 9 | +3 Tage | Rueckmeldung einholen (Kundenstimme + Antwort-Signal) |
| 12 | +3 Tage | **der Pitch** — Instagram-Kundenmaschine 333 |
| 15 | +3 Tage | der Einwand „bin noch nicht so weit" |
| 20 | +5 Tage | Tag setzen → Automation 72 (Engine, Loop 1) |

🚨 **Hormozi ist der Struktur-Layer, Patricias Stimme der Ton.** Wo beide
sich widersprechen, gewinnt die Stimme: Hormozi will Saetze unter 15 Woertern,
Patricia will kein Stakkato. Also Hormozis Reihenfolge (Schmerz → Moment →
Mechanismus → Angebot → **ein** CTA → P.S.) in ganzen Saetzen.

🚨 **Der Pitch an Tag 12 steht auf Hormozis „Pain is the pitch" samt
Ausnahme:** nach einem Gewinn darf man nur verkaufen, wenn der gelieferte Wert
ein **neues** Problem geschaffen hat. Genau das ist hier der Fall — das Profil
steht, deshalb kommen Reaktionen, mit denen sie nichts anfangen kann. Deshalb
steht Tag 9 (Gewinn benennen lassen) unmittelbar davor.

🚨 **Kein Kurslink in Mail 0.** Die Zugangsdaten verschickt ThriveCart
selbst; die Mail sagt nur, dass die andere kommt, und fuehrt in die Werkstatt.

🚨 **Keine Nachfass-Mail mit den 90 Storyideen** (Patricias Einwand,
18.09.2026). Im **Storyideen-Checkout** liegt ein Upsell auf die
Instagram-Kundenmaschine fuer **97** — wer die Mail anklickt, sieht acht Tage
nach dem 333er-Pitch denselben Kurs fuer 97 und wartet ab dann auf den naechsten
Preis. Stattdessen geht sie direkt in die Engine: Loop 1 pitcht ohnehin
„Finde dein Thema" fuer 39, und das taucht nirgends guenstiger auf.
**Vor jedem Mail-Angebot pruefen, was im Ziel-Checkout als Upsell haengt.**

🚨 **Loop 6 bleibt an** (Patricias Entscheid, 18.09.2026). Ich hatte
verlangt, ihn abzuklemmen, weil der IKM-Pitch sonst „drei Wochen spaeter"
nochmal kaeme. **Die Zahl war aus einer Notiz uebernommen und nie nachgerechnet.**
Die echte Taktung: je Loop 5 Mails im Zwei-Tage-Takt, also rund zehn Tage —
Loop 6 startet erst nach den Loops 1 bis 5, **gut zwei Monate** nach dem Pitch
an Tag 12, mit fuenf Mehrwert-Mails davor. Das ist ein zweiter Anlauf, kein
Doppel-Pitch. Wer gekauft hat, steigt ueber GoalA von selbst aus.
**Vor einer Warnung ueber Zeitabstaende die Taktung nachrechnen**, statt eine
Zahl aus einer aelteren Notiz zu uebernehmen.

🚨 **Bei Mail 12 fehlt eine Kundenstimme.** In den Unterlagen steht nur
„Super Kurs!". Der Platz ist absichtlich leer gelassen — nie einen Namen
erfinden.

🚨 **Der Umlaut-Waechter laeuft bei jedem Bau mit.** Am 18.09. stand
„so **haettest** du es geschrieben" dreimal in Mail 4 — im Text, den die
Kaeuferin liest. Gefunden hat es Patricia, nicht die Selbstpruefung. Deshalb
prueft das Skript jetzt seinen **sichtbaren** Ausgabetext (Kommentare und Tags
raus) gegen eine Liste bekannter Umschreibungen und meldet jeden Fund.
Echte ae/oe/ue-Woerter (bauen, dauert, neues, zuerst) stehen bewusst nicht in
der Liste — nach dem dritten Fehlalarm liest niemand mehr hin. Geprueft an
einem bekannt fehlerhaften Stand **und** an einer Gegenprobe, die nicht
anschlagen darf.

### Die Begleitung zur Energie-Routine (`scripts/begleitung/`, seit 2026-09-24)

**Das Artifact, das die Teilnehmerinnen der 30-Tage-Energie-Routine durch die dreissig
Tage führt.** https://claude.ai/artifact/16dg1sYzwKdjvHhAqVpA7u

```bash
python scripts/begleitung/cockpit-bauen.py
preview_start {"name": "energie-begleitung"}   # Port 4394
```

| Datei | Inhalt |
|---|---|
| `cockpit-bauen.py` | Markup, CSS, JS, Prüfungen |
| `inhalte.py` | Wochen · Haken (`abWoche`) · Vorrat · Protein-Tabelle · Mengenwörter |
| `bibliothek.py` | 46 Artikel (je mit `tag`) und 30 Tagesimpulse |

Die **120 Rezepte** liegen in vier Markdowns (`12-30-fruehstuecke`, `17-mittagessen`,
`18-abendessen`, `19-zwischenmahlzeiten`) und laufen durch **denselben Parser** wie die
Webseiten: `scripts/rezepte/bauen.py`, Funktion `lies(pfad)`.

🚨 **Die Führung ist der Kern** (Patricias Ansage, 24.09.): Jeden Tag schaltet
mindestens ein Bibliotheks-Artikel frei, die Checkliste wächst über die Wochen (drei
Haken in Woche 1, nicht fünf), der Vorrat kommt gestaffelt. **Die Rezepte sind als
Einzige von Tag 1 an vollständig** — *„die sollten schon von anfang an drin sein."*
Verschlossene Artikel stehen sichtbar da („ab Tag 18") und lassen sich nicht öffnen;
oben steht, warum, sonst wirkt ein Regal voller grauer Zeilen wie eine leere Seite.

🚨 **Keine Artifact-Fähigkeiten.** `db` oder `assets` machen eine Seite
organisationsintern — für Kundinnen unbrauchbar. Alles läuft über `localStorage` und
bleibt auf ihrem Gerät. Das Bauskript **warnt**, wenn `capabilities` oder
`claude.use(` in der Seite landen, und meldet doppelte `id`-Attribute.

🚨 **Nur grünes Material.** Patricias Rezepte, ihr Plan, Fakten aus ihren Büchern mit
Autor und Titel, ihre Immunwoche. **Kein Satz aus den bezahlten Coachings** — Herkunft
und Grenze in `context/persoenlich/ernaehrungswissen/`. Keine Heilversprechen, keine
Diagnosen; **Hormonersatztherapie kommt bewusst nicht vor**, obwohl das Buch ein
Kapitel dazu hat.

🚨 **Drei Fallen, die schon zugeschnappt sind:**
- **`str.replace` ohne Gegenprobe läuft still ins Leere.** Drei Ersetzungen hatten ein
  Leerzeichen zu viel im Suchtext — die ganze Freischaltung funktionierte nicht, und
  der Bau meldete trotzdem Erfolg. Immer `assert alt in t` **und**
  `assert t.count(alt) == 1`.
- **Backslashes in JS-Regex** laufen durch Heredoc, Python und f-String. Den Bau mit
  `python -W error::SyntaxWarning` laufen lassen, damit er abbricht statt still etwas
  Kaputtes zu erzeugen. Beim Ersetzen `chr(92)` statt Literalen.
- **Einheiten als ganzes Wort prüfen.** `rest.indexOf("g") === 0` hält **„grosse"** und
  **„Gurken"** für Gramm — aus 24 Kartoffeln wurden 25.

**Der Portionsrechner** skaliert von **6 Personen** (so sind die Rezepte geschrieben,
steht als Marke auf jeder Karte). Gerundet nach Einheit, kleine Mengen wechseln von kg
auf g und von l auf ml, Ein- und Mehrzahl über die Tabelle `MENGENWORT`.
**Gegenprobe nach jeder Änderung:** bei 6 Personen muss jede der 120 Familienzeilen
exakt dem Rohtext entsprechen.

**Verkaufsseite nachgezogen (24.09.):** 120 Rezepte, Begleitung auf dem Handy, 46 Artikel,
Vorratsliste, Protein-Tabelle. Ausgespielt über `scripts/wordpress/deploy-energieroutine.mjs`
— 🚨 das Skript setzte früher jede Seite auf `draft` und hätte die Live-Seite vom Netz
genommen; jetzt behält eine bestehende Seite ihren Status.
⚠️ **Offen:** Das Artifact ist **privat** — die Freigabe läuft über das
Share-Menü und kann Claude nicht übernehmen.

Volle Doku: `outputs/produkte/doterra-mama-energie/20-begleitung-artifact.md`.

### Kochbot-RAG (`scripts/kochbot-rag/`)

Supabase-basierte Vector-Datenbank für Patricias Rezepte (~1900 PDFs in `rezepte/`) und Kochwissen (MyBodyAdvice, 7hauben-Brotkurse in `kochwissen/`). Macht den `/mealplan`-Slash-Command auch in der Web-Claude-Sandbox einsatzfähig — die PDFs selbst sind via `.gitignore` ausgeschlossen, die Embeddings liegen bei Supabase und werden via API abgerufen.

- **Sprache:** Python 3.11+
- **Stack:** OpenAI `text-embedding-3-small` (1536 dim) + Supabase pgvector + `pypdf` + `tiktoken`
- **Setup-Anleitung:** `scripts/kochbot-rag/README.md`
- **Schema:** `scripts/kochbot-rag/schema.sql` einmalig im Supabase SQL Editor ausführen
- **Ingest (lokal, einmalig):** `python ingest.py` — liest `rezepte/` + `kochwissen/`, embeddet, schreibt nach Supabase. Idempotent (skipped bekannte Dateien), `--force` überschreibt
- **Query (überall):** `python scripts/kochbot-rag/query.py "<Anfrage>" --top 5 [--folder rezepte|kochwissen] [--format json]`
- **Benötigte ENV** (`scripts/kochbot-rag/.env`, gitignored): `SUPABASE_URL`, `SUPABASE_SERVICE_KEY`, `OPENAI_API_KEY`

Der `/mealplan`-Slash-Command ruft `query.py` automatisch vor jeder Rezept-Empfehlung auf, statt Rezepte zu erfinden. Falls die `.env` in der Web-Claude-Sandbox fehlt (sie persistiert nicht zwischen Sessions): Patricia darauf hinweisen statt aufgeben.

### Telegram News-Bot (`scripts/telegram-news-bot/`) — „Mum Life Daily" (Tageszeitung seit 2026-06-04)

**Tägliche, kuratierte News-Ausgabe als PDF per Telegram** — wie eine Tageszeitung, aber nur mit dem, was für Mama-Unternehmerinnen zählt. 5 Ressorts: 📸 Instagram & Social Media · 💼 Online-Business & Marketing · 🤝 Network Marketing · ⏳ Zeitmanagement & Mama-CEO-Struktur · 🤖 KI & Claude Code. Quellen: RSS + Google News **+ YouTube-Videos** pro Ressort.

Statt stumpfer Zusammenfassung **redigiert Claude wie eine Chefredakteurin**: wählt pro Ressort die für die Zielgruppe relevantesten Beiträge aus (inkl. max. 2 Videos; Steuerung über `ZIELGRUPPE` in `config.py`), filtert Rauschen (Gadgets, US-Politik, Krypto) und schreibt Schlagzeile + ausführlichen Absatz „warum für eine Mama mit Online-Business relevant". Ausgabe ist ein **PDF** (klickbare Links, Brand-Farben, Video-Markierung) mit kurzer Telegram-Begleitnachricht; Textfassung als Fallback.

- **Sprache:** Python 3.11+
- **Module:** `config.py` (Feeds + YouTube-Kanäle + Zielgruppen-Profil + Schedule), `feeds.py` (RSS-Abruf), `youtube.py` (Kanal-Videos), `summarizer.py` (Redaktions-Logik), `pdf.py` (reportlab-PDF), `store.py` (Anti-Wiederholung), `bot.py` (Versand/Scheduler)
- **Lokal testen:** `python bot.py --now` (sofortige Ausgabe)
- **Dauerbetrieb:** `python bot.py` (täglich 07:00 Zürich; `DIGEST_FREQUENCY=weekly` als Fallback)
- **Feeds:** RSS + Google-News-RSS (robust, deutschsprachig — z.B. „Claude Code"-Suche) + YouTube-Kanal-RSS. Langsame Ressorts/Videos haben längeres Zeitfenster (`CATEGORY_AGE_DAYS`, `VIDEO_AGE_DAYS`).
- **Deployment:** Railway via `Procfile` (env: `DIGEST_FREQUENCY=daily`, `SCHEDULE_HOUR=7`, `TIMEZONE=Europe/Zurich`). `requirements.txt` enthält `reportlab`.
- **Setup-Anleitung:** `scripts/telegram-news-bot/README.md`

### PIA — KI-Mentorin-Bot fürs Bootcamp (`scripts/pia-bot/`, seit 2026-06-16)

**Mehrbenutzer-Telegram-Bot** für das 5-Tage-MBA-Bootcamp (29.6.–3.7.). Anders als alle anderen Bots (nur Patricia) ist PIA für **viele Teilnehmerinnen gleichzeitig** offen — jede chattet privat, durchläuft ein 6-Fragen-Onboarding (Network-spezifisch) und holt sich pro Tag ihre personalisierte Mission: `/bio` (Tag 1) · `/hooks` (Tag 2) · `/struktur` (Tag 3) · `/leadmagnet` (Tag 4) · `/roterfaden` (Tag 5). Output in der Stimme der Teilnehmerin.

- **Sprache:** Python 3.11+ · python-telegram-bot 21 · Anthropic + (optional) OpenAI-Whisper
- **Architektur:** `bot.py` (Handler, Onboarding-Flow, Voice) · `onboarding.py` (6 Fragen) · `store.py` (Profile pro Userin als JSON in `data/users/`) · `pia_brain.py` (Claude-Generatoren) · `knowledge.py` (Voice-/Hook-Wissen — **kein** privates Vollprofil) · `config.py`
- **Regeln eingebaut:** Freundin-Voice, kein Stakkato, Schweizer ss, keine erfundenen Zahlen, Transformation statt Produkt, Network-Compliance (keine Heilversprechen), keine Mentoren-Namen.
- **Env:** `PIA_BOT_TOKEN` (eigener BotFather-Bot, NICHT der Story-Bot) + `ANTHROPIC_API_KEY` (+ optional `OPENAI_API_KEY`, `PIA_ADMIN_CHAT_ID`).
- **Status:** Code fertig + Bio-Generierung live getestet. Offen: BotFather-Token + Railway-Deploy + Testrunde. Doku: `scripts/pia-bot/README.md`. Launch-Logik: `outputs/produkte/mba-launch/challenge-launch-plan.md`.

🔄 **Update: Dieser Telegram-Bot ist der geparkte Vorgänger.** Das eigentliche PIA ist ein **Web-Tool** — **eigenes Repo `C:\Users\pnulm\pia`** (nicht in diesem Workspace), live auf **pia.mumlifebalance.ch**, ARIA-Style mit fester Seitenleiste. Enthält die Grundlagen-Werkstätten (Bio · Leadmagnet · Hooks · Fahrplan · roter Faden · Content-Woche) + die vollen **MBA-Werkstätten** (Produkt · Funnel · Salespage · Content & Launch · Mama-CEO · Verkaufsgespräch · Story · Reel · Karussell · Content-Monat), eine editierbare **„Mein Business"-Kontextseite** mit Dokument-Upload, Slide-Studio, Branding, Wins/Testimonials und Telegram-Erinnerung. Next.js + Supabase + Claude, Deploy `cd ~/pia && npx vercel --prod --yes`.
  - **Zugang** über `profiles.tier` (Supabase): Standard **`mba`** (jede neue Anmeldung hat Vollzugang, weil der Link nur in der MBA geteilt wird). Alte Bootcamp-Konten stehen auf **`expired`** und müssen bei MBA-Kauf einzeln freigeschaltet werden — über `pia.mumlifebalance.ch/admin/freischalten` (Gate: `PIA_ADMIN_EMAIL`) oder per Service-Key-Skript.
  - **Envs (Vercel):** `ANTHROPIC_API_KEY`, `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, `PIA_ADMIN_EMAIL`, `CRON_SECRET`, `TELEGRAM_WEBHOOK_SECRET` gesetzt; **offen (schlafend):** `OPENAI_API_KEY` (Sprachnotiz/Whisper) + `PIA_BOT_TOKEN` + `NEXT_PUBLIC_PIA_BOT_USERNAME` (Telegram-Erinnerung). Details im Memory [[project_pia-mentee-tool]] + `~/pia/docs/`.

### Haushalts-Bot — Vorabend-Push (`scripts/haushalts-bot/`, seit 2026-06-29)

**Privater Zwilling des Cockpit-Bots fürs Zuhause.** Schickt Patricia **jeden Abend 19:00** (Europe/Zurich) einen Vorabend-Überblick für den **nächsten Tag** aus der Notion **🏠 Haushalts-Liste** (DB `745ae127-1f03-4dc0-83d4-a6a8058d99dc`, im Privat-Bereich „🏡 Privat & Familie") — über einen **eigenen** Telegram-Bot (nicht der Cockpit-Bot).

- **Sprache:** Python 3.12 · `notion-client` (REST `databases.query`, plan-unabhängig) + `requests` (Telegram)
- **Module:** `config.py` · `notion_reader.py` (liest Liste paginiert) · `briefing_builder.py` (Vorabend-Logik) · `run_once.py` (Build + Senden)
- **Briefing-Gruppen:** 📌 Dranbleiben (überfällige einmalige Termine bis `Erledigt=ja`) · 🏠 Haushalt · 👨‍👩‍👧 Familie/Termine · 🎒 Schule (Vorabend, mit Vorname) · 🧒 Kinder-Ämtli · 🧘 Dein Slot (Me-Time ohne Druck). Wochentage werden auch aus der Notiz gelesen (z.B. Krafttraining „Mo/Mi/Fr"). Quartals-/Saison-Aufgaben kommen NICHT täglich (kein Nagging).
- **Deployment:** GitHub Action `.github/workflows/haushalt-vorabend.yml`, Cron `0 17 * * *` (= 19:00 CEST / 18:00 CET) + `workflow_dispatch` für Test.
- **Secrets:** `TELEGRAM_HAUSHALT_BOT_TOKEN`, `TELEGRAM_HAUSHALT_CHAT_ID`, `NOTION_TOKEN` (Integration muss Zugriff auf die Haushalts-Liste haben).
- **Doku:** `scripts/haushalts-bot/README.md`. Konzept-Hintergrund: `outputs/produkte/mama-ceo/bonus-haushalts-helfer-bot-PATRICIA.md` (das war „Stufe 2").

### Instagram Content-Engine (Automatisiert, v2 seit 2026-04-21)

**Vollautomatisches Content-System für beide Profile** (Mentoring + doTERRA). Weekly Content-Generation + Daily Auto-Posting + Monthly Best-Performer-Repost. Gesteürt durch 3 Scheduled Tasks + 2 Assistenten (`/reels`, `/karussell`).

**Content-Grundlagen** (in `context/`):
- `brand-voice.md` — Tonalität, Schreibregeln, Kernbotschaft, Beispieltexte
- `caption-formeln.md` — 5 Caption-Strukturen + CTA-Varianten + Hashtag-Strategie
- `.claude/skills/hooks/SKILL.md` — die eine Quelle für Hooks (die alte `context/hook-framework.md` ist weg, Herkunft liegt in `reference/_archiv-skills/hook-framework-alt.md`)
- `job-saeulen.md` — **Wirkungs-Achse** (Autorität / Story / Reichweite / Sales) — Pflicht-Layer parallel zur Themen-Achse, jeder Post = 1 Thema × 1 Job
- `reels-framework.md` — Viral-Mechanik 2026, 3-Sek-Regel, Pillars, Posting-Zeiten, Performance-Tracking, 4-Wochen-Repost-Regel
- `karussell-framework.md` — Karussell-Spezifika, Folien-Struktur, Feed-Aesthetic
- `manychat-keywords.md` — ManyChat-Keywords pro Pillar (SYSTEM/QUIZ/PRODUKT/THEMA/SICHTBAR/ANLEITUNG/LEAD/ECHT1 für Mentoring, ENERGIE für doTERRA)
- `notion-content-db.md` — DB-IDs, Pillar-IDs, Pflicht-Felder-Mapping
- `business-info.md` — Positionierung beider Profile, Produkt-Paket, Zielgruppen

**Notion-Architektur:**
- **Content-Management-DB** (`2ae7078e-8b7e-811a-ad14-000ba5820c09`) — alle Posts
- **Content-Strategie-DB** (`2ae7078e-8b7e-81a3-9f5f-000be0dd8dbc`) — Pillars (3 Mentoring + 5 doTERRA + Julia-Trost-Rollen)
- **Content-Plattformen-DB** (`2ae7078e-8b7e-8103-81e2-000b93a36fc7`) — Instagram Mentoring / Instagram doTERRA / Facebookgruppe / Telegramgruppe

**Canva-Ordnerstruktur:**
- `Instagram Karussells` (ID: `FAHG78rHy1g`) — Hauptordner
  - `Posting Queue` (ID: `FAHG7yBZfpE`) — Freigegebene Designs hier ablegen (Titel muss `[OK]` enthalten)
  - `Gepostete Beiträge` (ID: `FAHG7-zV3Cw`) — Archiv nach dem Posten

**Scheduled Tasks** (Prompt-Files in `reference/`):
- **Montags-Content-Engine** (`scheduled-task-montags-engine.md`) — Mo 06:00: Trend-Scraping auf 5 Plattformen (IG/TikTok/FB/Reddit/Twitter), 20 spezifische Hooks (10 pro Profil, strikt nach `.claude/skills/hooks/SKILL.md`), 10 Karussell- + 10 Reel-Entwürfe, Feed-Aesthetic-Check, Notion-Einträge
- **Posting-Queue** (`scheduled-task-posting-queue.md`) — Täglich 07:00: Canva-Queue prüfen, Freigabe-Check (`[OK]` im Titel), Caption generieren, via **Blotato API** (`reference/blotato-setup.md`) zur Zielgruppen-Zeit posten, Design verschieben, Notion aktualisieren. **Halb-Automatik-Modus** bis Blotato-Account-IDs in `.env` eingetragen.
- **Monats-Repost** (`scheduled-task-monats-repost.md`) — 1. Monatstag 08:00: Best-Performer (Saves+Shares+DMs) des letzten Monats erkennen, 4 Reposts pro Monat (2 pro Profil = 1 Reel + 1 Karussell), adaptieren (neuer Hook + neue Caption + neue Cover-Farbe), Notion-Eintrag mit Recycling-Relation

**Manülle Assistenten** (statt Scheduled):
- `/reels` — Einzel-Reel-Briefing, Hook-Brainstorm, Reel-Doktor, Wochen-Plan, Batch-Dreh
- `/karussell` — Analog für Karussells

**ManyChat-Integration:**
Jede Caption enthält ein Keyword (z.B. „Kommentier **ENERGIE**") das eine Automation auslöst → DM mit 0€-Produkt / Minikurs / Padlet-Link.

**Blotato (Instagram Auto-Post):**
- API-Key in `.env` (gitignored)
- Setup-Doku: `reference/blotato-setup.md`
- Flow: Canva-Export → Blotato Media-Upload → POST /v2/posts mit scheduledTime
- **Offen**: Key rotieren + Account-IDs abrufen (2 Instagram-Profile)

**Posting-Zeiten:**
- Mentoring: Di/Mi/Fr 07:30 oder 21:00
- doTERRA: Mo/Mi/Sa 21:30

**Freigabe-Flow:**
1. Montags-Engine erstellt 20 Entwürfe + Briefings in `outputs/reels/` + `outputs/karussells/` + Notion-Einträge (Status „Idee")
2. Patricia wählt die besten, erstellt Designs in Canva
3. Design in „Posting Queue" legen, Titel mit `[OK]` markieren = Freigabe
4. Daily Task prüft Queue + postet via Blotato zur Zielgruppen-Zeit
5. Monats-Repost reaktiviert Best-Performer nach 4 Wochen

**Voraussetzungen:** Canva MCP Server (verbunden), Notion MCP (verbunden), Blotato API via curl/HTTP (Key in .env gespeichert, Account-IDs noch abzurufen)

---

## 🚨 Zugangsdaten und Personendaten — nie in den Code (gelernt am 2026-09-13)

**Was passiert war:** Der ActiveCampaign-Schlüssel stand im Klartext in zwei Skripten,
dazu 32 doTERRA-Kundinnen mit Namen, privaten Mailadressen, Telefonnummern und
Kundennummern. Alles über das öffentliche Repo ohne Login abrufbar. Ein alter
OpenAI-Schlüssel lag ebenfalls offen. Aufgefallen ist es niemandem — gefunden wurde es
nur, weil einmal jemand gezielt nachgesehen hat.

**Die drei Regeln, die daraus folgen:**

1. **Kein Schlüssel im Code.** Zugangsdaten kommen aus `process.env` / `os.environ`,
   der Wert steht ausschliesslich in einer `.env` (die sind über `**/.env` ausgeschlossen).
   Fehlt der Schlüssel, bricht das Skript mit einem Hinweis ab — nie mit einem
   eingebauten Wert weiterlaufen.
2. **Keine Daten anderer Menschen im Code.** Namen, Mailadressen, Telefonnummern,
   Kundennummern gehören in eine ausgeschlossene Datei daneben, die das Skript liest.
   Muster: `scripts/activecampaign-mcp/doterra-kunden.json` — ausgeschlossen über
   `scripts/**/kunden*.json` und `scripts/**/kontakte*.json`.
3. **Zusagen an Kundinnen gelten auch im Repo.** Steht bei einer Kundenstimme
   „keine Freigabe / nur intern", dann gehört sie in eine ausgeschlossene Datei —
   nicht in eine, die jede lesen kann.

**Wenn doch einmal ein Schlüssel im Repo gelandet ist:** Entfernen reicht nicht.
Git behält jede frühere Fassung, und wer ihn in der Zwischenzeit kopiert hat, kann ihn
weiter benutzen. Der Schlüssel muss **gewechselt** werden — bei ActiveCampaign über
Einstellungen → Developer → *Reset API Key*, bei OpenAI über platform.openai.com →
API keys → Revoke. Danach den neuen an **allen** Stellen eintragen; beim
ActiveCampaign-Schlüssel sind das `04-projects/activecampaign-mcp/.env` **und**
`.mcp.json`. Der MCP-Server liest seine Zugangsdaten nur beim Start — nach dem Wechsel
Claude Code neu starten, sonst kommt weiter ein 403.

**Vor jedem Umzug in die Öffentlichkeit prüfen:** ob Schlüssel, Mailadressen,
Telefonnummern oder fremde Personendaten in getrackten Dateien stehen. `git grep` über
die getrackten Dateien reicht dafür — es muss nur jemand daran denken.

### 🚨 Zweite Workspace-Kopie in OneDrive (gefunden 2026-09-16)

Unter `OneDrive/Dokumente/Patricia/Arbeit&Politik/Business/mumlifebalance-workspace/`
liegt ein **kompletter Abzug des Workspace vom 29./30. April 2026** — mit `.git`,
`.claude` und 1'797 Dateien. Darin im Klartext:

| Datei | Was |
|---|---|
| `.mcp.json` | ActiveCampaign-Schlüssel **und** Notion-Schlüssel |
| `reference/julia-trost/Transkripte Videocalls/transkribieren_batch2.py` | OpenAI-Schlüssel `sk-proj-…` |
| `reference/julia-trost/Transkripte Videocalls/transkribieren_fix.py` | OpenAI-Schlüssel |
| `scripts/transcribe/transcribe.js` | OpenAI-Schlüssel |

**Der Stand ist von VOR der Aufräumaktion am 13.09.2026.** Die Schlüssel, die damals
gewechselt wurden (ActiveCampaign, OpenAI), sind hier noch in der alten Fassung —
also vermutlich tot. 🚨 **Der Notion-Schlüssel wurde nie gewechselt** und ist damit
wahrscheinlich weiter gültig.

**Gegenprobe im Live-Repo ist sauber:** `.mcp.json` steht in `.gitignore` (Zeile 311)
und ist nicht getrackt; `git grep` über die getrackten Dateien findet keinen Schlüssel.

**Die Lehre:** Eine Kopie des Workspace in einer Cloud-Ablage umgeht jedes
`.gitignore`. Was dort nicht im Repo landet, landet trotzdem in OneDrive. Bevor
irgendwo ein Workspace-Abzug abgelegt wird, gehören `.mcp.json`, jede `.env` und die
Skripte mit eingebauten Schlüsseln heraus.

---

## ⚠️ Bekannte Sandbox-Limits (Web-Claude)

**Wichtig für jede Session — bevor du Patricia versprichst etwas live zu pushen:**

### Outbound-Hosts: Allowlist-Restriction
Die Web-Claude-Sandbox (claude.ai/code) blockiert Outbound-Requests zu nicht-erlaubten Hosts mit `403 host_not_allowed`. Betroffen u.a.:
- `mumlifebalance.ch` (WordPress)
- `mumlifebalance.activehosted.com` (ActiveCampaign)
- Vermutlich auch andere Patricia-Domains

**Workaround heute:** Code-Änderungen ins Git pushen + Patricia kopiert manuell in WP/AC.
**Echte Lösung:** GitHub Actions als Deployer einrichten (Secret = WP_APP_PASSWORD), oder lokaler MCP-Server bei Patricia.

### `.env`-Files persistieren NICHT zwischen Sessions
Web-Claude resetet alle gitignored Files. Heisst:
- `scripts/wordpress/.env` muss Patricia in jeder neuen Session frisch erstellen
- Gilt analog für `scripts/manychat/.env`, `scripts/bio-check-bot/.env` etc.

**Vorgehen wenn Patricia direkten WP/AC/MC-Push will:**
1. Erst prüfen ob `.env` existiert: `ls scripts/wordpress/.env`
2. Wenn nicht: Patricia bittet App-Password zu schicken → in `.env` schreiben → nach Push wieder löschen
3. Beim Push prüfen ob Sandbox-403 kommt → wenn ja: ehrlich sagen + Workaround anbieten

### Pattern: GitHub Actions als dauerhafte Lösung
Für alle Tools, die zwischen Sessions persistieren müssen (Tokens, regelmäßige Scrapes, Posten zu externen APIs): **Token als GitHub Repo-Secret hinterlegen, Workflow im `.github/workflows/` läuft per Cron oder workflow_dispatch.**

Live-Beispiele in diesem Repo:
- `apify-scrape.yml` — täglicher Konkurrenz-Scrape (Secret: `APIFY_API_TOKEN`)
- `freitag-hooks.yml` — wöchentlicher Content-Lauf, ruft jetzt `/content woche` (Dateiname historisch) (Secrets: `ANTHROPIC_API_KEY`, `BLOTATO_API_KEY`, `NOTION_TOKEN`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`)
- `montag-build.yml` — Montag-Content-Build
- `story-reminder-daily.yml` — tägliche Story-Erinnerung

**Wenn ein neues Tool dauerhaft benötigt wird:** lege es als GitHub Action an, statt es im Sandbox-`.env` laufen zu lassen.

### Was hilft als Bot-Vorbereitung
- Vor Live-Aktionen IMMER zuerst Limits checken statt Patricia falsche Hoffnung machen
- HTML-Embed-Blöcke (z.B. `outputs/bio-check-bot/ac-form-embed.html`) bereitstellen → Patricia kann manuell einfügen
- Bei Form-Code-Updates IMMER auch GitHub-Raw-URL liefern für schnelles Kopieren

---

## Notizen

- Kontext minimal aber ausreichend halten — kein Bloat
- Pläne in `plans/` mit datierten Dateinamen für die Historie
- Outputs nach Typ/Zweck in `outputs/` organisiert
- Referenzmaterialien in `reference/` zur Wiederverwendung

---

## Visual-QA-Pflicht für Bild-Outputs

**Bevor gerenderte Bilder/Slides/Designs an Patricia gehen, IMMER selbst durchchecken** — egal ob Story-Slide, Karussell-Folie, Reel-Cover oder Sales-Page-Banner:

1. **Gesicht-Check:** Wenn Patricia im Bild ist — ist ihr Gesicht komplett unverdeckt? Berührt eine Text-Box ihren Kopf?
2. **Hauptmotiv-Check:** Wird das Schlüsselelement des Fotos (Säntis-Gipfel, Wasserfall, Blume, Logo) von Text/Box verdeckt?
3. **Story-Arc-Check (bei Slide-Sequenzen):** Ergibt die Abfolge einen Bogen (Hook → Reibung → Wendung → Punkt → CTA), oder ist's nur eine Slideshow von Statements?
4. **Brand-Check:** Stimmen Farben (Petrol/Creme/Dunkelblau/Orange), Schriften (Philosopher + Source Sans 3), Tonalität?
5. **🚨 Feed-Aesthetic ABAB-Rhythmus (PFLICHT seit 2026-06-11):** Feed-Sequenz muss **strikt abwechseln** — `Template → Foto → Template → Foto → Template → Foto …`. **NIE 2 Templates in Folge. NIE 2 reine Foto-Posts in Folge.** Template = Cover ohne Person (Voll-Petrol/Creme/Orange/Dunkelblau mit Typo). Foto = Cover mit Patricia oder Lifestyle-Foto als Hauptmotiv. **Templates rotieren in der Farbe** (Grün→Beige→Blau→Orange), **Fotos nicht zweimal das gleiche**. Pflicht-Check vor jedem Cover-Build: letzte 2 + nächste 2 geplante Posts. Plus 🚨 **Petrol/Grün-Cover NIE bei Lead-Posts** mit Keyword-CTA (`feedback_KRITISCH-petrol-cover-nicht-bei-leadposts.md`). Doku: `feedback_KRITISCH-feed-aesthetic-3-in-folge.md`.

6. **🚨 Bei Video zusaetzlich (seit 15.09.2026):** nach jedem Render Standbilder
   ziehen und anschauen — **zerrissene Woerter** (nie `overflowWrap: anywhere`),
   **Schriftgroesse** (laufender Text ab 60 px, betont ab 96 px, Hook ab 130 px),
   **zwei Texte uebereinander**, **Gesicht frei**, **tote Zonen** oben 0–12.5 % und
   unten 82–100 %, **Schweizer ss** (Whisper liefert das deutsche Zeichen), und
   **passt die Einblendung zum Inhalt** — wer nur diese zwei Sekunden sieht, muss
   etwas *verstehen*, nicht nur etwas *anschauen*. Deko faellt durch.

   🚨 **Ein Schleier hinter Text braucht einen Radius unter 50 %** (gelernt
   19.09.2026). Patricia: *„ist nur schade, dass mir im gesicht dieser strich
   durchlaeuft wo du glaube ich was hinterlegt hast."* Der weiche Verlauf hinter
   dem Hook hatte 55 % senkrecht und 70 % waagrecht — der Weg bis zur eigenen
   Boxkante sind aber 50 %. Also endete er **ausserhalb** der Flaeche und wurde
   an deren Kante abgeschnitten, mit rund 4 % Restdeckung. Das ist ein starrer
   Strich quer durchs Bild, und er lag auf ihrer Augenhoehe.

   **Die Box zu vergroessern hilft NICHT** — beide Werte sind Prozent derselben
   Box und wachsen mit. Nur der Radius zaehlt. Reichweite kommt ueber die
   groessere Flaeche bei kleinerem Radius.

   Gepruefte Stelle: `scripts/videoschnitt/textebene.py`, `.grund-verlauf::before`
   und `.hook-zusatz.gross`. **Im selben Generator steckte ein zweiter Verlauf
   mit demselben Fehler** (62 %) — den haette keine Sichtpruefung gefunden.

   🤖 **Und das wird gemessen:** `python scripts/video-pruefung/kante-suchen.py
   <video.mp4>` mittelt zwoelf Bilder (loescht alles Bewegte aus) und meldet jede
   waagrechte Kante, deren Helligkeitssprung ueber **mindestens 92 % der Breite**
   dasselbe Vorzeichen hat. Eine Textkante ist oertlich und faellt raus. Getestet
   an beiden Enden: am alten Render schlaegt es an (y=704, Sprung 2.25), am
   neuen und am Rohmaterial schweigt es. **Pflicht nach jedem Render.**

   🚨 **Ein Fund ist ein Hinweis, kein Urteil** (20.09.2026). Das Skript kann einen
   **steilen weichen Verlauf** nicht von einer harten Kante unterscheiden, und ein
   **echter Horizont** im Bild ist ebenfalls eine durchlaufende waagrechte Kante.
   Bei einem Fund gehoert ein Blick aufs Bild dazu, nicht nur auf die Zahl:
   `ffmpeg -ss <sek> -i <video> -vf "crop=1080:260:0:<y-130>,scale=1080:520,eq=contrast=2.2" -frames:v 1 <ziel>.png`
   — bei 2.2-fachem Kontrast ist ein Strich sofort als Strich zu sehen, ein Verlauf
   bleibt ein Verlauf. Belegter Fall: `kw39-d-mi-a` meldete y=534 mit Sprung **1.25**,
   im Bild war es der weiche Schleierrand ueber der Landschaft. Zum Vergleich: der
   kaputte Render vom 19.09. hatte Sprung **2.25**. **Unter rund 1.5 erst schauen,
   dann entscheiden.**

   🤖 **Der Rand wird maschinell geprueft, nicht per Stichprobe:**
   `python scripts/video-pruefung/rand-pruefen.py --takt 0.4` im Remotion-Projekt —
   rendert die Textebene ohne Video und misst alle 0.4 s die aeusseren 24 Pixel
   ueber Rohbytes. **Jede neue Pruefung zuerst an einem bekannt fehlerhaften Stand
   testen** — schlaegt sie dort nicht an, ist sie kaputt.
   **Pflicht vor jedem Render.** Volle Elf-Punkte-Liste im Vorrang-Block von
   `.claude/skills/remotion-motion-graphics/SKILL.md`.

Bei Fund: erst nachjustieren, dann ausliefern. **Nie Entwürfe rausgeben, die offensichtliche Probleme haben.** Patricia muss nicht das Visual-QA für Claude machen.

(Hintergrund: 2026-04-26 wurden Wander-Stories rausgegeben mit verdecktem Gesicht und verdecktem Säntis-Gipfel — und ohne Story-Arc. 2026-06-11 hatte der Mentoring-Feed 3 grüne Petrol-Lead-Cover in Folge mit unterirdischer Reichweite, dazu mehrfach gleiche Cover-Farbe ohne Rhythmus. Lehre: Selbst-Prüfung ist Pflicht-Schritt vor Output.)

### Cockpit-Datenabgleich (`scripts/cockpit/daten-abgleich.py`, seit 2026-09-11)

**Das Cockpit zeigt jetzt echte Daten statt eines Startbestands von Hand.**
Ein Lauf sammelt und schreibt drei Dokumente:

| Dokument | Inhalt | Quelle |
|---|---|---|
| `daten/produkte` | alle Angebote mit Stufe, Preis, Keyword, Link | `context/active-funnels.json` + `context/link-uebersicht.md` |
| `daten/funnel` | Keyword → Freebie → Liste/Automation → Angebot | `context/manychat-keywords.md` + Funnels |
| `daten/mailings` | Listen mit Kontaktzahl, alle Automationen mit Status | ActiveCampaign API |

```bash
python scripts/cockpit/daten-abgleich.py outputs/cockpit/abgleich
```

Danach die drei JSON-Dateien mit `Artifact write_db` (`db_op: batch`) in die
Sammlung `daten` schreiben. Der AC-Zugang kommt aus
`04-projects/activecampaign-mcp/.env`; fehlt er, laufen Produkte und Keywords
trotzdem durch.

**Läuft täglich automatisch** als Scheduled Task `cockpit-daten-abgleich`
(06:15, nur solange die App offen ist). Der Task liest und schreibt
ausschliesslich in die Cockpit-Datenbank — keine Mails, keine AC-Änderungen.

**Der Ordner `outputs/cockpit/abgleich/` ist gitignored** (Repo ist public).

Zusätzlich holt `scripts/cockpit/suchindex-bauen.py` einen Volltext-Index über
`context/`, `outputs/`, `reference/` und `plans/` (rund 7'900 Abschnitte) nach
`suche/<NN>`. Privates, Persönliches, Finanzen und fremde Transkripte bleiben
draussen.

**Harte Grenzen der Artifact-Datenbank:** ein Dokument max. 256 KB, eine
Schreib-Anfrage max. 1 MB. Deshalb sind Mails und Suchindex auf viele
Dokumente verteilt.

**Neue Reiter im Cockpit:**

| Reiter | Was | Wem gehört es |
|---|---|---|
| Listen & Automationen | Listen mit Kontaktzahl, Automationen zum Aufklappen mit allen Mailtexten | Abgleich — reine Anzeige |
| Angebote | Tabelle plus Detailkarte je Angebot: Kursinhalt, Order Bump, Upsell, Downsell, Notiz | **Patricia** — nie überschreiben |
| Ideenkasten | Was noch nicht umgesetzt ist, mit Bereich, Status und Aufwand | **Patricia** |
| Suchen | Stichwort → alle Fundstellen im Workspace | Abgleich |

🚨 **`daten/produkt-details` und `daten/ideenkasten` darf der Abgleich NIE
schreiben.** Dort stehen Patricias eigene Einträge; ein `set` löscht sie.

Gebaut mit `scripts/cockpit/patch-mailings-tab.py` und
`scripts/cockpit/patch-arbeitswerkzeug.py`; einmalig befüllt mit
`scripts/cockpit/startinhalt-bauen.py`.

### doTERRA Rang-Tracker (`scripts/cockpit/doterra-tracker-bauen.py`, seit 2026-09-11)

**Eigener Bereich im Cockpit, getrennt vom Mentoring.** Zeigt Patricias Weg
zu Gold entlang ihrer drei Qualifikations-Beine — Miriam Gätzi-Widmer,
Corinne Heimgartner, Melanie Kunz — mit der exakten Zahl, die je Bein fehlt,
und den Leuten darunter, die Volumen machen.

**Rangvoraussetzungen** (belegt aus `context/doterra/business-building-guide.pdf`
S. 108 und `Business Companion/train-guide.pdf` S. 6/7 — nie raten):

| Rang | PV | OV | Beine |
|---|---|---|---|
| Executive | 100 | 2.000 | — |
| Elite | 100 | 3.000 | — |
| Premier | 100 | 5.000 | 2 × Executive |
| Silver | 100 | — | 3 × Elite |
| Gold | 100 | — | 3 × Premier |

**Datenweg:** doTERRA hat keine offene Schnittstelle. Die Zahlen kommen aus
dem **Schlagdistanz-Bericht** im Back Office
(`index.cfm?Fuseaction=evo_Modules.QueryReport&QryID=EliteStriking&QueryType=StrikingDistance`)
— er liefert PV, OV und Bein-Zähler je Person. Ergänzend der
**Teamqualifikationsbericht** (`QryID=Qualifier`) für die Platzierungs-Struktur.
Claude holt beides über die Chrome-Anbindung aus Patricias eingeloggtem
Browser; der Text landet in `context/doterra/backoffice/schlagdistanz-<JJJJMM>.txt`.

```bash
python scripts/cockpit/doterra-tracker-bauen.py outputs/cockpit/abgleich
```
→ `doterra.json` → `daten/doterra` im Cockpit. Reiter: **doTERRA → Rang-Tracker**.

🚨 **`context/doterra/backoffice/` ist gitignored** — echte Namen und Umsätze
des Teams, und das Repo ist public.

**Achtung bei der Struktur:** Der Schlagdistanz-Bericht gruppiert nach
**Enroller**, der Teamqualifikationsbericht nach **Sponsor/Platzierung**. Für
die Rang-Qualifikation zählt die Platzierung. Mirella Castellazzi und Michelle
Berger erscheinen deshalb je nach Bericht an verschiedenen Stellen.

### Bereich doTERRA im Cockpit (seit 2026-10-13, Version 99)

Patricia: *„das ölwissen würde ich gerne vorerst in mein cockpit integrieren"* · Symptomcheck *„in ALLEN
Unterlagen. büchern, zeitschriften usw."* · *„gleiches auch fürs business. mit steps"* · Rising-Leaders-Gruppe
*„mit vielen aufträgen unter anderem neue berater anzuziehen"*. Eigener Bereich oben (Rang + Team sind
von Mama-CEO umgezogen), gebaut mit `scripts/cockpit/patch-doterra-bereich.py` (+ `doterra-bereich.js/.css`).

| Reiter | Inhalt | Quelle → Datenbank |
|---|---|---|
| **Öl-Wissen** | Produkte, Duft, Anwendung, Satz für Kundinnen, „So nicht sagen“, Öl-Abende | `context/doTERRA/Produktwissen/produkt-wissensbasis.json` → `wissensbasis-bauen.py` → `doterra-wissen/produkte` |
| **Anliegen** | Symptom-Suche über **alle** Unterlagen: 38 Anliegen, je bis 24 Stellen mit Quelle/Seite, welche Öle wie viele Quellen nennen, Block Ernährung/Hormone, Kundinnen-Satz | `anliegen.json` + `scripts/doterra/anliegen-bauen.py` → `doterra-wissen/anliegen-NN` |
| **Business-Wege** | 8 Abläufe, 67 Schritte zum Abhaken, 26 Vorlagen (einschreiben, LRP, betreuen, reaktivieren, Öl-Abend, Beraterin gewinnen, Onboarding 30 Tage, Rang bis Gold) | `context/doTERRA/business-wege.json` → `doterra-wissen/wege` |
| **Rising Leaders** | Aufträge mit Frist · Beraterinnen-Liste (Idee → Gespräch → Infos → eingeschrieben → eingearbeitet) · Eingang „Neu aus Telegram“ | `daten/rising-leaders` — 🚨 **gehört Patricia, Abgleich schreibt nie** |

**Anliegen-Bibliothek:** liest Bücher (`context/doTERRA/wissen/*.md`), E-Books, Enjoils-Hefte,
Produktwissen, `context/persoenlich/ernaehrungswissen/`, `kochwissen/*.md|pdf`. **Scans** liest die in
Windows eingebaute Texterkennung (`scripts/doterra/ocr-windows.ps1`, über `anliegen-bauen.py --ocr`,
Zwischenspeicher `outputs/cockpit/abgleich/ocr/`, 2213 Seiten am 13.10.). 🚨 Die Auszüge sind
Buchtext mit Heilaussagen → nur im privaten Cockpit, Ausgabe gitignored. Nach aussen geht nur
`kundinnen` aus `anliegen.json`. 🚨 Bücher ohne Absätze werden an Satzgrenzen geteilt, sonst gewinnt ein
ganzes Kapitel jedes Anliegen; dasselbe Buch unter zwei Dateinamen wird über den Textanfang erkannt.

**Telegram-Abgleich** (`scripts/telegram-userbot/src/abgleich.ts`, nur lesend, alle **Gruppen und
Kanäle**, keine Einzelchats): eigene Anmeldung `TELEGRAM_SESSION_ABGLEICH` (einmalig
`npm run abgleich-anmelden`, Patricia tippt selbst) — 🚨 nie die Session des alten Userbots
mitbenutzen, gleichzeitige Nutzung kann Telegram sperren. Läuft als **Schritt 4 im Task
`cockpit-daten-abgleich`**: Claude sortiert in auftrag/tipp/training → `doterra-wissen/eingang`;
Patricia übernimmt oder verwirft im Cockpit; übernommene Tipps/Trainings arbeitet der Task in die
JSON-Quellen ein (`telegram/eingearbeitet.json`).

**Öffentliche Fassung Öl-Wissen** (zum Teilen mit Kundinnen, ohne `compliance`/`patricia`):
https://claude.ai/artifact/XfZKXY3kd7qRg71B9ZEzvM — gleiche Quelle, `wissensbasis-bauen.py`, dann
`outputs/doterra-wissen/oel-wissen.html` neu veröffentlichen. Teilen nur über Patricias Share-Menü.
🚨 Texte aus Team-Grafiken nie wörtlich (fremdes Konto), Gesundheitsaussagen raus, keine erfundene
Ich-Erfahrung — was Patricia selbst nutzt, steht im Feld `patricia`.
Monats-Newsletter: `outputs/newsletter/2026-MM-aktionen-doterra.md`; Booklet und Flyer liegen in der
WP-Mediathek (Drive-Upload geht nicht über 25 MB, Booklet vorher mit pypdf verkleinern).

### ThriveCart-Anbindung (`scripts/cockpit/thrivecart-holen.py`, seit 2026-09-11)

**Order Bumps, Upsells und Downsells kommen jetzt aus der Quelle statt aus Prosa.**

- **Zugang:** `04-projects/thrivecart/.env` → `TC_API_KEY`
  (ThriveCart → Einstellungen → API & Webhooks → API tokens)
- **Basis:** `https://thrivecart.com/api/external` · Header `Authorization: Bearer <token>`
- **Limit:** 60 Anfragen pro Minute
- **Belegt aus** dem offiziellen SDK `github.com/thrivecart/php-api`, `src/Api.php` —
  nicht geraten.

| Weg | Liefert |
|---|---|
| `/ping` | Konto (mumlifebalance, ID 39035) |
| `/products` · `/products/<id>` | Produkte; das Detail nennt `slug`, `payment_currency`, **`upsell_ids`, `downsell_ids`** |
| `/bumps` | Order Bumps — das Feld `url` sagt, an welchem Checkout sie hängen |
| `/upsells` · `/downsells` | nur `id` + `name`, die Zuordnung kommt aus dem Produkt-Detail |
| `/<art>/<id>/pricing_options` | Preise (nur mit `--preise`, kostet je einen Aufruf) |
| `/transactions` | Umsätze — noch nicht angebunden |

```bash
python scripts/cockpit/thrivecart-holen.py outputs/cockpit/abgleich
```
→ `thrivecart.json`. `daten-abgleich.py` heftet das danach über den
Checkout-Slug an die Angebote (`tc_bumps`, `tc_upsells`, `tc_downsells`) und
das Cockpit zeigt es in der Angebots-Karte als **„Am Checkout hängt"**.

Diese Felder gehören dem Abgleich. Patricias eigene Notizen liegen getrennt in
`daten/produkt-details` und werden nicht angefasst.

**Stand 11.09.2026:** 37 Produkte · 15 Bumps · 8 Upsells · 3 Downsells,
14 Produkte mit Anhang. Produkt 51 „Untitled product" steht auf `test`.

### Cockpit als Nachschlagewerk (seit 2026-09-11)

**Alles, was verstreut lag, ist jetzt an einem Faden.** Fünf Bausteine:

| Skript | Baut | Landet in |
|---|---|---|
| `kurse-indexieren.py` | 6 Kurse, 118 Lektionen, Stichwort-Register | `daten/kurse` |
| `arbeitsblaetter-verknuepfen.py` | 50 Drive-Arbeitsblätter an die passende Lektion | `daten/kurse` |
| `verknuepfen.py` | pro Angebot: Datei, Funnel, Mails, Erwähnungen, Kurs | `daten/verknuepfung` |
| `fremdwissen-indexieren.py` | 1'917 Wegweiser in fremde Kurse (nur Fundstelle) | `suche/f*` |
| `chat-ideen-sammeln.py` + `-einpflegen.py` | Ideen aus 101 Chats | `daten/ideenkasten` |
| `fundstellen-bauen.py` | Drive-Ordner und Canva-Designs mit Direktlink | `suche/x00` |
| `drive-inventar.py` | 187 Drive-**Dateien** mit Art und Direktlink, 100 als fremd markiert | `suche/x01` |
| `fremdwissen-drive.py` | Register der Kurs-Handouts aus Drive — Überschrift plus eine Zeile | `suche/fd` |
| `downloads-aufraeumen.py` | räumt den ganzen Download-Ordner in 13 Schubladen | lokal, `Downloads/_*` |
| `praesentationen-bereitstellen.py` | Kurs-Unterlagen aus `outputs/` für Drive vorsortieren | lokal, `Downloads/_fuer-drive/` |
| `katalog-bauen.py` | Angebote in Schubladen mit ThriveCart-Preis und Kette | `daten/katalog` |

🚨 **Ordner, die mit `_` beginnen, sind Archiv und werden übersprungen.** In
„Digitale Produktwelt" lagen unter `Transkripte/_archiv-zoom-mai/` die alten
Zoom-Marathon-Aufnahmen vom Mai; ohne Filter stand jede Lektion aus Modul 3
bis 6 zweimal im Cockpit (32 statt 24 Lektionen).

🚨 **Die Dateinummer ist NICHT die Kursreihenfolge.** Bei der Produktwelt ist
Datei `01` die Lektion **2.3** und Datei `07` die Willkommens-Lektion **0.1**.
Die echte Zuordnung steht in
`context/Kurse/aktuelle kurse/Digitale Produktwelt/Transkripte/README.md` und
ist als Tabelle `MODULE` in `kurse-indexieren.py` hinterlegt. Wer nach
Dateinummer sortiert oder Arbeitsblätter danach zuordnet, liegt bei jedem
zweiten falsch.

🚨 **ThriveCart liefert keine Kursstruktur.** Die Schnittstelle kennt Produkte,
Bumps, Upsells und Transaktionen — Module und Lektionen gibt es dort nicht.
Alles, was im Reiter „Kurs-Inhalte" steht, kommt aus den Transkript-Dateien.

**Kurs-Stichwörter werden gerechnet, nicht gepflegt:** häufig in dieser Lektion,
selten in allen anderen, plus die Titelwörter. Umlaute sind egal — die Dateien
heissen „huetchenmethode", gesucht wird „Hütchenmethode".

**Fremdes Material ist markiert.** Julia Trost, Elke Mayr, Karriere Mum und die
anderen stehen nur als Wegweiser drin: Datei, Seite, eine Zeile zum
Wiedererkennen. **Kein Inhalt.** Im Cockpit orange umrandet — was dort steht,
darf nie in einem Kundendokument landen.

**Auslieferungs-PDFs liegen als Anhang am Artifact** (`/_blob/…`, 20 MB je
Datei): Starterguide, Von 0 auf echt, Lead-Challenge, Story-Challenge,
Fahrplan, 90 Storyideen. Neue Datei → `Artifact upload_asset`, dann die
zurückgegebene Adresse in `ANHAENGE` in `verknuepfen.py` eintragen.

🚨 **Sechs Dokumente darf der Abgleich nie schreiben:** `daten/produkt-details`,
`daten/ideenkasten`, `daten/doterra`, `daten/ketten`, `daten/umsatzplan` und
`suche/x00`.

### Angebots-Katalog, Ketten und der Weg zum Monatsziel (seit 2026-09-16)

**Der Reiter „Angebots-Katalog" zeigt, was Patricia hat, was es kostet und was
daran hängt.** Zwei Begriffe, die nicht verwechselt werden dürfen:

| | |
|---|---|
| **Kategorie** | was ein Angebot *ist* — Freebie · Tipp · Prompt · Mini-Kurs · Kurs · Signature · Programm |
| **Rolle** | wo es *eingesetzt* wird — als Bump, als Upsell, als Downsell |

Die Content-Box ist ein Mini-Kurs für 17 **und** der Order Bump an drei
Checkouts. 🚨 **Ein Produkt hat je Einsatzort einen anderen Preis** — „Finde
dein Thema" kostet einzeln 39, als Bump mal 27 mal 39, als Upsell 25. Das ist
kein Datenfehler, sondern die Mechanik.

**Ebenso wenig verwechseln:**
- **Befund** — was ThriveCart heute wirklich ausliefert. Kommt vom Abgleich,
  reine Anzeige (`daten/katalog`).
- **Plan** — was Patricia bauen will. Gehört ihr (`daten/ketten`), wird beim
  Anklicken eines Angebots gebaut. Der Knopf „Stand aus ThriveCart übernehmen"
  kopiert den Befund als Startpunkt hinein.
Die Differenz zwischen beiden ist die Arbeitsliste. Wer beides in ein Feld
schreibt, sieht nie, was noch fehlt.

**„Weg zum Monatsziel"** (in „Zahlen & Ziele", `daten/umsatzplan`) rechnet
bewusst **zwei Zahlen statt einer**: *vorsichtig* (nur das Angebot) und *mit
ganzer Kette* (Bump und Upsell mitgenommen). 🚨 **Keine geratene Bump-Quote
einbauen.** Es gibt noch keine eigene Statistik dazu, und eine geratene Zahl
sieht in einer Tabelle genauso echt aus wie eine gemessene. Sobald
`/transactions` von ThriveCart angebunden ist, kann daraus ein echter Wert
werden.

Skripte: `katalog-bauen.py` → `patch-katalog.py` → `patch-kette-klickbar.py` →
`patch-kette-feinschliff.py` → `patch-umsatzplan.py` → `patch-katalog-links.py`.

🚨 **Seite ≠ Produkt.** In `link-uebersicht.md` steht `/mama-wird-hausapothekerin`
als „Inhalt veraltet". Das gilt für die **WordPress-Seite** — das gleichnamige
**Programm** (61-Seiten-Workbook, MP3, 5 Videos, rund 159 MB) ist aktiv und wird
ausgeliefert, sobald jemand die doTERRA-Hausapotheke kauft. Aus einer veralteten
Landingpage nie schliessen, das Produkt dahinter sei tot — nachfragen. Inhalte:
`context/doterra/mama-wird-hausapothekerin.md` und
`context/doterra/mini-notfallapotheke.md`.

**Vorlagen zum Weitergeben** stehen im Katalog unter *Tipp* und *Prompt*. 🚨
Dort landet nur, was Patricia nachweislich gehört — die Bonus-Vorlagen aus
Mama-CEO Säule 4 und die Prompts aus ihrem eigenen Produktwelt-Kurs. Bei einem
„Kopie von …"-Dokument aus Drive weiss niemand mehr, aus wessen Kurs es stammt;
solche Dateien sind über die Suche findbar, aber nicht als weitergebbar
ausgezeichnet.

### Download-Ordner aufräumen (`downloads-aufraeumen.py`, seit 2026-09-16)

**876 Dateien, 17 GB, in 13 beschrifteten Schubladen.** Die Wurzel ist leer.

🚨 **Claude kann nichts nach Drive hochladen.** Der Connector nimmt Dateien nur
als eingebetteten Inhalt an (`base64Content`) — bei einer 24-MB-PDF geht das
nicht. Deshalb liegt das Geschäftliche in `Downloads/_fuer-drive/<Ordnername>/`
und Patricia zieht je Ordner einmal. Danach `drive-inventar.py` neu laufen
lassen, damit die Dateien mit echtem Link in der Cockpit-Suche stehen.

🚨 **Es wird nur verschoben, nie gelöscht.** Was weg kann, liegt in
`_dubletten`, `_programme` und `_muell` — löschen ist Patricias Entscheidung.

🚨 **Die Reihenfolge der Regeln ist die Sicherung:** erst Zugangsdaten, dann
privat, dann Dubletten, dann Geschäft, zuletzt die Dateiart. Wer nach Endung
zuerst sortiert, schiebt eine Scheidungsurkunde nach `_dokumente`, weil sie
halt eine PDF ist.

🚨 **Umlaute umschreiben, nicht wegwerfen.** Beim Dubletten-Abgleich wurde
`re.sub(r"[^a-z0-9]", "", name.lower())` benutzt — dabei wird aus „für" ein
„fr", und der Dateiname „…-fuer-…" gilt als etwas anderes. Dadurch blieben
Dubletten unerkannt. Richtig ist erst ä→ae, ö→oe, ü→ue, ß→ss, dann filtern
(Funktion `umschrift`). Gilt für jeden Namensvergleich in diesem Workspace.

🚨 **Muster eng fassen.** „kunden" fing beim ersten Lauf auch
Instagram-**Kunden**maschine, flyer_neu**kunden** und **Kunden**paket und hätte
drei Geschäftsdateien in den Privat-Ordner geschoben. Jedes Muster nach dem
Schreiben einmal gegen die echte Dateiliste prüfen.

**Zwei Funde, die dabei aufgefallen sind (16.09.2026):**
- `www.instagram.com_cookies.txt` und `kurse.juliatrost.de_cookies.txt` lagen
  offen im Download-Ordner. Das sind **Sitzungs-Token** — wer die Datei hat,
  ist eingeloggt, ohne das Passwort zu kennen. Sie stammen aus `/nachbau`;
  das Werkzeug legt sie bei Bedarf neu an. Liegen in `_zugangsdaten/` und
  gehören gelöscht.
- `patricia-kunden.csv` und `.json` — Namen und Mailadressen von Kundinnen.
  Dieselbe Regel wie für den Code: **Daten anderer Menschen nie in eine
  geteilte Ablage.** Liegen in `_privat/Kundendaten/`.

**Draussen bleiben:** `context/persoenlich/`, `strategy/private/`, die
Finanzordner, in Drive „09 - Admin & Logins" und alles Private. Gilt auch für
den Chat-Index — dort steckt dasselbe nochmal, nur unsortiert.

### Die Link-Zentrale — vier Linkarten je Angebot (seit 2026-09-16)

**Patricias wunder Punkt:** *„ich muss z.B. auch immer die links suchen wenn ich
in der story was verlinken will. das nervt übelst."* Und danach präziser:
*„will immer den link zu dem was ausgeliefert wird, den link zur landingpage
unter mumlifebalance., allenfalls den link zu thrivecart, den link zur
telegramgruppe wie z.B. bei der storychallenge das bekommen sie ja."*

Der Reiter **„Links & Material"** liegt deshalb direkt unter Übersicht und zeigt
je Angebot **vier Linkarten**, jede mit eigenem Kopier-Knopf:

| Art | Was | Beispiel |
|---|---|---|
| **Seite** | die Landingpage auf mumlifebalance.ch | `/lead-challenge/` |
| **Kasse** | ThriveCart | `/challenge-lead-magnet/` |
| **Das kriegt sie** | die Auslieferung: PDF, Bot, Tool | „Lead-Challenge Workbook · 13 Seiten" |
| **Gruppe** | die Telegram-Gruppe zum Angebot | `t.me/+lXiK5ZAigFIzZWY0` |

🚨 **Die Quelle ist `context/link-uebersicht.md`**, nicht das Cockpit. Ein
falscher Link wird dort korrigiert, dann läuft `linkzentrale-bauen.py`.

🚨 **Die Spalten werden über die Kopfzeile gefunden, nicht über ihre Position.**
Sonst verschiebt eine neue Spalte stillschweigend alle Werte um eins — und
niemand sieht es, weil trotzdem etwas dasteht.

**Was der Umbau am 16.09. ans Licht gebracht hat** — die alte Fassung kannte
genau einen Link je Angebot und hat damit die Hälfte verschwiegen:

- **Fast jedes Freebie hat eine eigene Landingpage.** „Von 0 auf echt" (WP 3836),
  Fahrplan (3842), Lead-Challenge (3820) standen in der Übersicht als „über
  ManyChat" ohne Link. Alle drei sind live.
- **Die Mini-Notfallapotheke hat eine Seite** — `/mini-notfallapotheke-fuer-mamas/`
  (WP 2906). In der Notiz stand „keine Landingpage". Das war falsch.
- **Die Lead-Challenge hat eine ThriveCart-Seite** (`/challenge-lead-magnet/`),
  obwohl sie ein 0€-Freebie ist.
- **Neun Angebote haben eine eigene Telegram-Gruppe.** Die Einladungslinks
  standen nirgends in der Doku — sie stecken in den ActiveCampaign-Mails
  (`mails-NN.json` im Abgleich, Zuordnung über `nummer` in `mailings.json`).
- **Das Evergreen-Webinar liegt auf Vimeo**, nicht in Drive:
  `vimeo.com/1214949645`, eingebettet auf `/mba-webinar-replay/` (WP 4025). Es
  geht über die Mail-Automationen **72 · 74 · 75 · 79** raus. 🚨 Die 599-MB-MP4
  im Kursordner ist die **Quelldatei** und gehört nicht nach Drive — eine Datei,
  die als Video schon ausgeliefert wird, ist nicht „fehlend". Vor dem
  Bereitstellen einer grossen Mediendatei immer prüfen, ob sie längst
  irgendwo eingebettet ist.
- 🚨 **`bio-check.mumlifebalance.ch` löst nicht auf** (Status 000). Der lebende
  Bot ist `bio-check-bot.vercel.app`. Nie die tote Adresse verlinken.

- **`/angebote/` ist die Landingpage der Einzelkurse.** Sie haben keinen eigenen
  Slug, stehen aber alle auf der Angebots-Seite, sortiert nach den drei Säulen —
  mit Sprungmarken: `#positionierung` (Expertin, Magnet-Ich, Finde dein Thema,
  Instagram-Kundenmaschine) · `#aufbau` (Mama-Business, Vom Network-Wissen,
  Digitale Produktwelt) · `#mama` (Mama-Zeit, Familienorga, Aus Nebenbei wird
  Business). 🚨 **Kein eigener Slug heisst nicht: keine Seite.** Vor „hat keine
  Landingpage" immer die Sammelseite durchsehen.
- **Vier Angebote fehlten ganz in der Übersicht**, obwohl sie auf `/angebote/`
  verkauft werden: Magnet-Ich (333) · Dein starkes Mama-Business (777) ·
  Mama-Zeit (37) · Familienorga for real (37).
- 🚨 **„Aus Nebenbei wird Business" hat zwei Checkouts** — Produkt 30
  `/aus-nebenbei-wird-business` und Produkt 29 `/aus-nebenbei`. Beide antworten
  mit 200, beide 777. Die Angebote-Seite verlinkt Produkt 29. Einer gehört
  stillgelegt, sonst laufen die Verkäufe auf zwei Konten.

**Der Checkout-Zustand kommt aus ThriveCart, nicht aus Prosa** (Patricia,
16.09.: *„du siehst auf thrivecart welche angebote gerade online sind oder
entwürfe oder einfach deaktiviert"*). Das Feld `status` in `katalog.json` kennt
drei Werte:

| Zustand | Was der Checkout tut | Stand 16.09. |
|---|---|---:|
| `live` | nimmt echtes Geld | 27 |
| `test` | zeigt die Seite, bucht aber **nichts** ab | 3 |
| `disabled` | ist abgeschaltet | 7 |

Die Link-Zentrale zeigt bei `test` und `disabled` eine rote Fahne plus einen
Satz, was das heisst, und zählt oben „Kassen offen".

🚨 **Der Anlass war ein echter Fehler:** „Dein starkes Mama-Business" (777,
Produkt 33) steht auf `test` und ist trotzdem von `/angebote/` verlinkt. Wer
dort kauft, bezahlt nichts, und die Seite sieht dabei völlig normal aus. **Vor
jedem „das kannst du verlinken" den Status prüfen** — nie aus einem 200er
schliessen, dass die Kasse Geld nimmt.

🚨 **Status ≠ Positionierung.** Mama-Zeit, Familienorga, Selbstbewusst als Mama,
Grenzen setzen, Mama-Reset, Easy Mumlife Academy und Network Academy stehen auf
`live`, gehören aber zur **alten Ausrichtung**. Beides gehört getrennt notiert:
ob die Kasse läuft, und ob das Angebot noch beworben wird.

Dubletten, die dabei aufgefallen sind: Mama-Zeit zweimal live (Produkt 5 für 77,
Produkt 9 für 37) · Easy Mumlife Academy zweimal live (18 für 666, 27 für 444) ·
Aus Nebenbei wird Business zweimal live (29 und 30, beide 777).

Von 32 auf **80 Links** und 42 Einträge. **Kein Angebot ohne Seite.**

Skripte: `linkzentrale-bauen.py` → `patch-linkzentrale.py` →
`patch-linkzentrale-vier-arten.py` → `patch-linkzentrale-feinschliff.py`.

**Namensabgleich mit Mindest-Deckung:** „Lead-Challenge 3-Tage-Workbook" und
„Lead-Challenge Workbook" enthalten einander nicht. Darum zusätzlich über
gemeinsame Wörter — aber **mindestens zwei**, sonst passt „Challenge" allein auf
Lead- und Story-Challenge gleichermassen.

### Die Inhalte gehören in den Workspace, nicht nur in die Datenbank (seit 2026-09-16)

**Ein Artifact ist kein Backup.** Keine Historie, kein Git — wer versehentlich ein
`set` drüberschreibt, hat den Text verloren. Bis zum 16.09. lagen **alle** fertigen
Beiträge ausschliesslich dort. Patricia: *„bitte alle inhalte speichern, dass sie im
workspace drin sind“*.

Zwei Schritte, weil ein Python-Skript nicht an die Artifact-Datenbank kommt:

1. **Claude holt die Rohdaten** mit `ArtifactData list` — Sammlungen `reels`,
   `karussells`, `storys`, `daten` — nach `outputs/cockpit/inhalte-roh/`
   (`out_dir` schreibt je Dokument eine JSON-Datei).
2. `python scripts/cockpit/inhalte-sichern.py` macht daraus lesbares Markdown in
   `outputs/content/KW38/cockpit-reels.md` · `-karussells.md` · `-storys.md` — mit
   allen Folien und Captions im Wortlaut.

🚨 **`outputs/cockpit/inhalte-roh/` ist gitignored.** Darin liegt
`daten/doterra.json` mit **echten Teamnamen und Umsätzen**, dazu Mailtexte und
Telegram-Einladungslinks — das Repo ist öffentlich. Die Beitrags-Markdowns sind
unbedenklich, das ist Content, der ohnehin auf Instagram geht.

**Befund beim ersten Lauf (16.09.):** 22 Reels · 6 Karussells · 10 Story-Bögen ·
**`freigaben` leer**. Nur **4 von 22 Reels** haben ein Video. Und **sechs Beiträge
hatten kein `profil`** — die tauchen in keiner Profil-gefilterten Liste auf und
lassen sich nicht über Blotato einplanen. Bei einem fehlenden Profil ist das
Kommentar-Stichwort die verlässliche Quelle (`STANDBEIN` → Mentoring, `ENERGIE`
→ doTERRA), **nie der Bauchentscheid**.

### 🚨 Zwei Schemata für Karussell-Folien — nicht verwechseln (20.09.2026)

| Wo | Felder je Folie |
|---|---|
| **Cockpit**, Sammlung `karussells` | `{headline, body, layout}` — `layout` ist `hook`, `text` oder `cta` |
| **Bild-Editor**, `daten/entwuerfe` | `{text, unter}` — `text` wird der grosse Balken, `unter` der kleinere |

Wer im Cockpit nach `text`/`unter` sucht, bekommt **leere Folien zurück und hält das
Karussell für unfertig**. Genau das ist mir am 20.09. passiert — ich war einen Schritt
davon entfernt, sechs vollständige Karussells als „leer“ zu melden. Ein leeres Feld ist
immer erst ein Verdacht auf den **eigenen Lesefehler**, nicht auf fehlende Daten:
`json.load(...)` und einmal `list(o.keys())` ausgeben, bevor irgendetwas behauptet wird.

### 🚨 Vor jedem `set` prüfen, ob die Kennung schon vergeben ist

Am 20.09. sollten vier neue **doTERRA**-Karussells als `kw39-kar-di-a` … abgelegt
werden. Unter genau diesen Kennungen lagen bereits die **Mentoring**-Karussells — ein
`set` hätte sie wortlos überschrieben, und `karussells` trägt kein Profil im Namen.
Gefunden hat es eine Gegenprobe gegen die vorher gelesene Liste, nicht das Gedächtnis.
**Profil gehört in die Kennung**, so wie bei den Reels: `kw39-kar-d-di-a` für doTERRA,
`kw39-kar-di-a` für Mentoring. Und: `set` ersetzt, `update` ergänzt — bei einem
Dokument, das es geben könnte, ist `update` die harmlosere Wahl.

### Der Cockpit-Umbau — Fliessband statt vier Ansichten (Version 76, 24./25.09.2026)

**Patricias Bild:** *„Ich prüfe, gebe frei und sie rutschen dann weiter in den
nächsten Reiter freigegeben und sobald sie auf insta gepostet sind, rutschen sie
auf gepostet. Die auswertung kannst du dann ja da pro Post machen. Alle, die gut
liefen, kommen dann auf eine Liste nach 4 Wochen erneut einplanen."*

**Planen → Freigegeben → Unterwegs → Gepostet → Recycling.** Drei Stationen gab
es schon; gefehlt hat die Verbindung zwischen Station 2 und 3.

#### 🚨 Der schwerste Fund: das Cockpit hat Arbeit gelöscht

**Patricia:** *„wenn ich mal aus dem cockpit fliege, ist alles was ich gemacht
habe wieder weg."* Zwei Fehler, die einzeln harmlos sind:

1. **`lsSet` stand INNERHALB der 700-ms-Verzögerung.** Die lokale Sicherung
   wartete genauso lang wie das Schreiben in die Datenbank.
2. **Beim Laden gewann die Datenbank bedingungslos:**
   `if (seen[st.id]) Object.assign(seen[st.id], st);` — ohne zu prüfen, welcher
   Stand neuer ist. Derselbe Code bei `storys`, `reels` und `karussells`.

**Zusammen ein Reisswolf:** tippen → wegklicken vor Ablauf der 700 ms → neu
öffnen → der alte Stand legt sich über das Getippte.

Behoben: `lsSet` läuft sofort, `dbUebernehmen()` vergleicht `updatedAt`,
`pagehide` sichert Ausstehendes. **Gemessen an beiden Ständen** — am alten
steht das Getippte nach dem Tippen *nicht* im Speicher, am neuen schon.

🚨 **Fehlt `updatedAt`, gewinnt der lokale Stand.** Arbeit zurückzubekommen ist
unmöglich, einen veralteten Anzeigestand zu erneuern ein Klick.

#### 🚨 Sieben Schreibstellen, null Lesestellen

Die Freigabe schreibt nach `freigaben/<id>` — **gelesen hat das Cockpit die
Sammlung nie.** Angezeigt wurde `beitrag.blotato.status`, und den aktualisiert
niemand. Belegter Fall: `kw39-kar-di-a` stand auf „wartet", während in
`freigaben` `status: "geplant"` mit Blotato-Kennung lag. **Der Beitrag war am
22.09. längst draussen** (54 Reichweite) — im Cockpit sah er aus wie
liegengeblieben. Seitdem ist `freigaben` die Quelle (`draussenStatus(b)`),
`blotato` nur noch Rückfall.

#### 🚨 „Datum ist durch" war eine Sackgasse, die sich täglich neu bildet

Karussell-Vorgabezeit **07:30**, Einplan-Lauf alle zwei Stunden ab 08:00 — wer
um zehn freigibt, ist für heute grundsätzlich zu spät. Am 24.09. betraf das
fünf Beiträge. Patricia: *„überlege dir bei den ganzen beitragsgeschichten was
gescheiteres."*

**Neu: die Freigabe ist die Entscheidung, das Datum nur ein Wunsch.**
`naechsterSlot(b)` sucht den nächsten Platz — Format passt zum Wochentag,
Zeitpunkt mindestens eine Stunde voraus, Platz frei, höchstens 28 Tage.
Nachgerückt wird **beim Freigeben**, nicht beim Anzeigen: was in `freigaben`
steht, muss der Zeitpunkt sein, an dem es wirklich rausgeht.

🚨 **Die Vorschau braucht einen Merkzettel.** Ohne ihn rechnet jeder Beitrag für
sich und vier bekommen denselben Tag angezeigt. `slotVorschau` wird bei jedem
`render()` geleert.

#### 🚨 Bei B-Roll und Story ist der Klick die Erledigung

**Patricia:** *„wenn ich freigegeben drücke, dann habe ich sie auf meinem
instagram-app auch eingeplant."* Belegt an den Zahlen: beide prüfbaren B-Rolls
waren draussen (21.09. → 207, 23.09. → 184). Meine Gruppe „Du postest selbst"
mit vier „überfälligen" war schlicht falsch.

Der Knopf heisst dort jetzt **„In der App eingeplant"**. Ein Knopf, der bei zwei
Formaten dasselbe heisst und Verschiedenes tut, ist der Fehler.

#### Die Zuordnung Beitrag → Instagram-Post

`scripts/cockpit/gepostet-zuordnen.py` verbindet beide Welten über den
**Caption-Anfang** (die API gibt `anfang` heraus, wörtlich gleich). Das Datum
ist nur Gegenprobe. Ergebnis nach `daten/gepostet-zuordnung`.

🚨 **Umschrift vor dem Filtern** (ä→ae), **Sternchen und Leerzeichen raus** —
im Cockpit steht `Kommentier **STANDBEIN**`, Instagram liefert
`Kommentier STANDBEIN`. Ohne das findet der Abgleich genau die Lead-Posts nicht.

🚨 **Das doTERRA-Konto hängt nicht an der API.** Eine fehlende Zuordnung heisst
dort **nicht** „nicht gepostet" — das steht auch so auf der Karte.

#### Reiter „Ideen von anderen" mit Bau-Knopf

`ideen-extern-bauen.py` misst die gescrapten Konkurrenz-Posts **gegen den
eigenen Median des jeweiligen Kontos** — absolute Likes sagen nichts, wenn ein
Konto zwanzigmal so gross ist. Drei Knöpfe je Idee (B-Roll · Sprechreel ·
Karussell) legen einen Auftrag in `bauauftraege`, den der 19:30-Task abholt
(Teil 2 seines Auftrags).

🚨 **Nach Likes sortieren findet Zitatkacheln.** Ganz oben standen „Ich trage
schon genug ❤️" (19× Median) und „Orlando, here I come!". Einzelbilder und
Captions unter 200 Zeichen fallen deshalb raus. Von 1'098 Beiträgen bleiben
**11, davon zwei wirklich übertragbar** — der Reiter heisst deshalb „Ideen von
anderen" und nicht „Top-Content".

#### Planung gegen den Workspace prüfen

**Patricia:** *„in notion waren teilweise inhalte veraltet"* · *„bei der nächsten
planung müssen wir das sicher beachten."*

`planung-abgleichen.py` hängt an jeden Jahresplan-Eintrag und jedes Ziel einen
**Beleg** — Produktordner, aktiver Funnel, ThriveCart-Status, Plan-Datei.
Befund vom ersten Lauf: **22 von 54 Einträgen ohne Spur**, **4 von 11 Zielen**
mit abgelaufenem Quartal bei Status „Aktiv". Eingebaut als **Pflicht-Schritt 2a
in `/monatsplan`** und als Block vor Modus 1 in `/jahresplan`.

🚨 **Belegen, nicht abhaken** — und die Befunde liegen in
`daten/planung-abgleich`, **nie** in `daten/jahresplan` oder `daten/ziele`.
🚨 **„Keine Spur" heisst NICHT „nicht passiert"** (ManyChat-Freebies haben keine
Datei). 🚨 **Ein Ziel belegt man mit Zahlen, nicht mit Dateien** — der erste
Lauf meldete „40'000 Umsatz" als „keine Spur". 🚨 **Ferien und Conventions sind
keine Vorhaben.**

#### Die Skripte (alle wiederholbar, alle mit `node --check`)

| Skript | Was |
|---|---|
| `patch-kein-datenverlust.py` + `patch-ausstehend-fuellen.py` | lokal sofort, neuer Stand gewinnt, `pagehide` |
| `patch-freigaben-lesen.py` | `freigaben` wird gelesen · Termine klickbar · Datumsfeld je Zeile |
| `patch-nachruecken.py` + `patch-slot-vorschau.py` | Zeitpunkt rückt nach statt zu verfallen |
| `patch-broll-ist-erledigt.py` | „In der App eingeplant" statt „Freigeben" |
| `patch-fliessband.py` | Gepostetes rutscht aus „Unterwegs" heraus, mit Reichweite |
| `patch-woche-aufraeumen.py` + `patch-karte-entruempeln.py` | 85 → 2 Aufgabenzeilen · 13 → 5 Knöpfe je Karte |
| `patch-nav-aufklappen.py` + `patch-nav-unterpunkte.py` | Gruppen klappen auf · Storys/Reels nur unter „Bauen" |
| `patch-ideen-extern.py` · `ideen-extern-bauen.py` | Ideenkasten mit Bau-Knopf |
| `planung-abgleichen.py` · `patch-planung-befunde.py` | Workspace-Belege an Jahresplan und Zielen |
| `gepostet-zuordnen.py` | Beitrag ↔ Instagram-Post |

Die alte Fassung liegt als `outputs/cockpit/_alt-mlb-cockpit-2026-09-25.html`.

#### 🚨 Vier Fallen, die an diesem Tag mehrfach zugeschnappt sind

- **Heredocs zerstören Backslashes.** `"\\n"` wird zum echten Zeilenumbruch, und
  die Datei ist kaputt. Für alles mit Escapes die Write/Edit-Werkzeuge nehmen.
- **Ein deutsches Anführungszeichen beendet den String** — `„Keine Spur"` mit
  ASCII-Schlusszeichen ist ein Syntaxfehler. Immer `„…“` paarweise.
- **Eine Gegenprobe darf nur den sichtbaren Text prüfen.** Zweimal hat eine
  Prüfung auf den eigenen Quellkommentar angeschlagen, einmal auf den
  Aufgaben-Reiter, wo „überfällig" völlig richtig steht. Kommentare vorher
  herausfiltern und das Muster eng fassen.
- **Die Testfassung muss die neuen Daten kennen.** `freigaben`, `ig-zuordnung`,
  `ideen-extern` und `planung-abgleich` mussten in `testfassung-bauen.py`
  nachgetragen werden — ohne sie prüfte die lokale Fassung gegen veraltete
  Felder und zeigte andere Zahlen als das Live-Cockpit.

🚨 **Und ein Fund ausserhalb des Cockpits: das Git war seit dem 16.09.
blockiert** — eine `\.git/index.lock` von einem abgestürzten Prozess, 0 Bytes,
acht Tage alt. Seitdem lief kein auto-sync. Dadurch war der lokale Stand 20
Commits zurück, und ich hielt den täglichen Apify-Scrape für ausgefallen; er
lief die ganze Zeit. **Vor jeder Aussage über „läuft nicht" erst `git fetch`.**


### Mein Tisch — die Startseite mit PIA (seit 2026-10-08, Version 84)

Nach dem Vorbild eines „CEO Table“ (fremder Kurs, nur der Aufbau übernommen, Farben
ihre: Verlauf Dunkelblau → Petrol, helle Karten, Philosopher + Source Sans 3 jetzt im
ganzen Cockpit). Vier Karten plus Helferinnen-Leiste: **PIA** (Patricias Name für die
Assistentin; trägt über `sample` Aufgaben und Termine selbst ein, sonst nichts) ·
**Aufgaben Business/Privat** (neues Feld `bereich` an `daten/aufgaben`) · **Kalender +
Tagesliste** (neues Dokument **`daten/termine`, gehört Patricia — der Abgleich darf es nie
schreiben**) · **Content-Kalender 14 Tage** · **KI-Helferinnen** nach Academy-Säulen
(Instagram · Produkte · Mama-CEO · KI · Privat), je mit „Hier fragen“ oder „Befehl kopieren“.
Skript: `scripts/cockpit/patch-mein-tisch.py`. Fällt `renderTisch` um, springt die alte
Startseite ein.
**Version 85 — fünf Bereiche oben statt Seitenleiste** (`patch-bereiche.py`, setzt den
Tisch-Patch voraus): Mein Tisch · Instagram · Produkte · Mama-CEO · KI, darunter Unterreiter
als Pillen, Inhalte auf hellem Blatt, je Bereich die Helferinnen der Säule. Reiter-Kennungen
unverändert. **KI → „PIA & Team“**: PIA, „Am Tisch – Aufträge“, alle Helferinnen.
🚨 **PIA legt Aufträge an Claude als Aufgabe mit `fuerClaude: true` ab** — `/start` liest
sie (Schritt 2b) und nennt sie zuerst.
**Version 86** (`patch-offene-chats.py`): kein Umsatz mehr auf der Startseite (Patricia zeigt
das Cockpit Kundinnen) · unter Aufgaben der Block **„Angefangen, nicht fertig“** aus
`daten/offene-chats` — je Claude-Code-Chat worum · fertig · offen · nächster Schritt, mit
„Als Aufgabe übernehmen“ / „Erledigt“ / „Verwerfen“ und Link zurück in den Chat. Erzeugt von
Claude über `list_sessions` + `list_events` (erster Stand 08.10.: 36 Chats, 21 offen).
🚨 **Beim Neu-Erzeugen den `status` bestehender Einträge übernehmen** (gleiche Session-`id`),
sonst kommt jeder verworfene Chat zurück. Kopie: `outputs/cockpit/abgleich/offene-chats.json`.
🚨 **Version 88 (`patch-auftauen.py`): die Artifact-Datenbank liefert `data()` EINGEFROREN**
(`db.d.ts` 0.2.43). Unter `"use strict"` warf jede Änderung daran — PIA konnte nichts
eintragen, und Abhaken, Notizen, Jahresplan, Folientexte fielen nach dem Laden aus der
Datenbank still aus. Lokal unsichtbar, weil die Testfassung aus `localStorage` lädt. Seitdem
läuft jeder `*.data()`-Aufruf durch `tief()`. **Reihenfolge der Patches ab der Fassung vor dem
Tisch:** `patch-mein-tisch` → `patch-bereiche` → `patch-offene-chats` → `patch-auftauen` →
`patch-erledigt` (Version 89: Unterreiter **Mama-CEO → Erledigt**, nach Tag gruppiert, Haken weg =
zurück zu den offenen; Aufgaben und Tisch zeigen nur noch Offenes). ⚠️ Offen: Telegram-Sprachnachricht → Tisch (Bot schreibt heute nach Notion),
Reiter im Academy-Aufbau mit Kursinhalt plus Helferinnen.

### Version 102 — Kalender gegen Instagram, Archiv, schlankere Leiste (seit 2026-10-16)

Patricia ging Reiter für Reiter durch. **Content-Kalender auf Mein Tisch** zeigt 7 Tage zurück und
14 voraus: je Beitrag ✅ gepostet (mit Erreicht · Rate · Gespeichert, „noch nicht ausgereift“ unter
7 Tagen) · ⚠️ nicht rausgegangen · 📌 direkt auf Instagram (spontan, nicht im Cockpit geplant).
Gepostetes steht am **echten** Postdatum. Quelle `daten/gepostet-zuordnung` aus
`gepostet-zuordnen.py` (jetzt auch ohne Freigabe, plus unscharfer Zweitvergleich, plus
`letzte_posts` der letzten 21 Tage) — läuft im täglichen Abgleich, vorher `inhalte-roh` frisch holen.
Code `scripts/cockpit/kalender-abgleich.js`, eingesetzt mit `patch-kalender-archiv.py`.
**Archivregel:** mehr als 14 Tage über dem Datum und nie freigegeben = archiviert (über
`istAbgelehnt`, nichts gelöscht, „Zurückholen“ setzt `ausArchiv`). **Leiste Instagram:** Reels,
Ideenkasten und Ideen von anderen raus. Der Ideenkasten lebt als `context/ideen-vorrat.md` weiter
(gelesen von `/strategie` und `/monatsplan` Frage 7). **Freigeben:** drei Spalten
„1 · Von dir freigegeben → 2 · Von mir eingeplant → 3 · Draussen“.
🚨 **Die Automatik war vom 10. bis 16.10. tot:** Die Scheduled Tasks durften nur fünf wörtlich
erlaubte Befehle; alles Neuere und jedes `cd … &&` blieb an einer Rückfrage hängen, die unbeaufsichtigt
niemand beantwortet — und der Lauf meldete trotzdem „erfolgreich“. Folge: Daten sechs Tage alt, das
Karussell vom 15.10. nicht gepostet. Jetzt Platzhalter-Erlaubnisse in `.claude/settings.local.json`
(`python scripts/cockpit/*`, `scripts/instagram-insights/*`, `scripts/doterra/*`, `scripts/telegram/senden.py`,
`node scripts/cockpit/freigabe-zu-blotato.mjs`, `ArtifactData`) und in den Task-Dateien die Regel
**„jeder Befehl einzeln, kein cd, kein &&“** plus Telegram-Meldung bei jedem gescheiterten Schritt.
⚠️ `daten/kurse` steht bei 253 von 256 KB — vor dem nächsten Kurs aufteilen.

### Reiter „Instagram → Zielgruppe & Markt“ (seit 2026-10-12, Version 96)

Die Analysen aus Annas Kurs „Content Shortcut“ (Zielgruppe · Fragen · Wettbewerb · Trends,
dazu „Auf einen Blick“ mit dem Abgleich zu Patricias Themen T1–T3) liegen als Markdown in
`outputs/zielgruppen-research/2026-10-12-content-shortcut/` (**gitignored**, nennt fremde Coaches)
und als `daten/zielgruppe` im Cockpit. `python scripts/cockpit/zielgruppe-bauen.py` →
`ArtifactData set` → Reiter über `patch-zielgruppe.py` (Code in `zielgruppe-reiter.js/.css`,
kleiner Markdown-Leser). Browser-Schlüssel `mlb:zg-markt`. **Quelle ist das Markdown.**
⚠️ Offen: ob Säule 2 der Analyse (gegen Firma/Upline) provokativ sein darf — Patricia unschlüssig.
Kursprompts zum Nachschlagen: `context/Kurse/aktuelle kurse/Content-Shortcut/`.

### Funnel-Checkliste und der Launch-Reiter (seit 2026-10-08)

**Die Checkliste** liegt als eigenes Artifact:
https://claude.ai/artifact/YViQzGgPqr3AiufeA35Ev3 — **131 Punkte in 9 Phasen**
(Bevor du baust · Die Kasse · ActiveCampaign · Die Seiten · Die Mails · Der
Zulauf · **Der Launch** · **Das Webinar** · Nach dem Start), je Funnel
abhakbar, Stand in `db`. Gebaut von `scripts/cockpit/funnel-checkliste-bauen.py`.
Jeder Punkt trägt, woher er kommt: `erfahrung` (25, eigene Fehler aus dieser
Datei) oder `methodik` (106, aus den gekauften Kursunterlagen — **nur die
Mechanik, nie der Wortlaut, keine fremden Namen**, die Seite ist teilbar).

**Grundlage:** die vollständige Durchsicht der Methodik am 08.10.2026,
**117 Befunde** in `outputs/marktrecherche/2026-10-08-julia-funnel-durchsicht.md`
— alle funnel-relevanten Transkripte (Automationen · Launchen · Digitale
Produktwelt · Magnetisch Verkaufen · 100k Blueprint · Produktkommunikation)
plus acht Vorlagen-PDFs. Eingearbeitet mit
`scripts/cockpit/patch-funnel-checkliste-julia.py`.

🚨 **Ein Punkt war falsch und ist korrigiert:** Das **Upsell ist nicht teurer
als das Hauptprodukt.** Die Reihenfolge lautet: Bump günstiger als das
Hauptprodukt · Upsell teurer als der Bump, **aber immer noch günstiger als das
Hauptprodukt** · Downsell günstiger als das Upsell. Jedes davon trägt seinen
eigenen Streichpreis.

🚨 **Secret Offer ist keine Preisstufe.** Es sagt **nicht**, um was es geht:
„es gibt etwas, tipp auf den Sticker“ — und wer tippt, bekommt den Link per
Nachricht; in der Mail bekommt ihn, wer antwortet. Belohnt wird das Vertrauen.
Zwei Tage, danach Frühbucher für alle. **Vom Secret zum Frühbucher ein kleiner
Schritt, vom Frühbucher zum regulären Preis ein grosser** — bei 199/277/333
ist es heute umgekehrt (78 gegen 56).

🚨 **Drei Lücken im eigenen ManyChat-Aufbau** (Befunde 81–85): es gibt drei
Auslöser, nicht einen (Kommentar · **Story-Antwort** · **Direktnachricht**) ·
ein **Zähltag** unterscheidet das erste vom zweiten Mal und schickt den Warmen
die längere Nachricht · in der DM stehen **zwei** Links (das Freebie *und*
„arbeite mit mir“, gemessen 60 % / 30 %), nicht einer.

🚨 **Dateinamen in „Launchen" stimmen nicht mit dem Inhalt** — „Webinar
Nachbereitung" enthält die Launch-Planungstabelle, „Flash Sales" die fünf
Phasen, „Warteliste" die Diagnose bei Nichtverkauf. Immer den Inhalt prüfen,
nie den Namen. Und „Glasklare Produktkommunikation" ist zu zwei Dritteln ein
**Canva-Kurs**.

**Der Reiter „Launch"** liegt unter **Produkte** (nicht unter Instagram — ein
Launch gehört zum Angebot, nicht zum Kanal): wo stehe ich (laufende Phase,
Tage bis zur nächsten, die Aufgaben dieser Phase, Preis-Gegenprobe) ·
Käufertypen diese Woche (sechs Kacheln, über eine Woche sollen alle sechs
vorkommen) · der Fahrplan über die fünf Phasen · Launches anlegen.
Skript `scripts/cockpit/patch-launch-reiter.py`, Code daneben in
`launch-reiter.js` + `.css` (als eigene Dateien, damit `node --check` sie
direkt prüfen kann). Neues Dokument **`daten/launch` — gehört Patricia**, der
Abgleich schreibt dort nie hinein.

✅ **Veröffentlicht am 08.10.2026 als Version 90**, zusammen mit
`patch-entwurf-quelle.py`.

🚨 **Zwischen Bauen und Veröffentlichen wurde `mlb-cockpit.html` auf den
Live-Stand zurückgesetzt** — beide Patches waren weg, obwohl beide Skripte
Erfolg gemeldet hatten und der Reiter lokal lief. Gefunden nur durch einen
Zeilenvergleich der Live-Fassung gegen die lokale. **Vor jedem Publish diffen,
nicht auf die Erfolgsmeldung des Patch-Skripts vertrauen** — ein Skript sagt,
was es getan hat, nicht, ob es danach noch dasteht. Hergang in
`outputs/cockpit/OFFEN-noch-nicht-veroeffentlicht.md`.

🚨 **Das Cockpit steht auf „Anyone with the link"**, obwohl seit dem 24.09.2026
32 Klarnamen und 3 Mailadressen darin liegen. Ändern kann das nur Patricia
selbst über das Share-Menü der Seite.

### Sichtprüfung des Cockpits — lokal, mit echten Daten

```bash
python scripts/cockpit/testfassung-bauen.py
# dann: preview_start {"name": "cockpit-test"} → http://localhost:4381
```

🚨 **Die Quelldatei allein taugt nicht für eine Handy-Prüfung.**
`mlb-cockpit.html` beginnt direkt mit `<style>` — kein `<!doctype>`, kein
`<head>`, **kein Viewport-Meta**. Das setzt die Artifact-Umgebung selbst. Lokal
geöffnet rendert der Browser mit 980 px, und jede Handy-Prüfung an dieser Datei
ist wertlos, egal welches Fenstermass eingestellt ist.

Die Testfassung setzt den Kopf davor und legt den echten Abgleich in
`localStorage` — das Cockpit liest beim Start von dort, bevor die Datenbank
drüberkommt. Ergebnis liegt in `outputs/cockpit/abgleich/index.html`
(gitignored).
