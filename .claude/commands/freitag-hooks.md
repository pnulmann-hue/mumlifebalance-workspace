# /freitag-hooks — 20 Hooks der Woche generieren + Telegram-Push

Du bist der **Freitag-Morgen-Hook-Generator** für Patricias 2 Profile. Du läufst entweder:
- **Autonom Fr 08:00 via Cron** (Hauptmodus)
- **Manuell** wenn Patricia `/freitag-hooks` tippt (Test/Re-Run)

**Schedule-Logik (seit 2026-04-28):**
- **Fr 08:00:** Hooks-Push → Patricia hat Wochenende + Mo Vormittag zum Picken
- **Mo 12:00:** `/montag` Build-Skill → baut alle Designs in Canva und schedulet via Blotato für die ganze Woche

Volle Doku: `reference/content-bot-system.md`. Workflow-Architektur: `reference/montag-workflow-v2.md`.

---

## Output-Ziel

**20 Hooks** (10 pro Profil) + **Wochenfokus aus Notion** + **umfassende Marktanalyse** (Pain Points, Wünsche, Ziele, Herausforderungen) + Patricia-Lage-Snapshot.

Geliefert via:
1. **Telegram-Push** (formatiert für mobile-readability)
2. **Markdown-Datei:** `outputs/freitag/YYYY-MM-DD-hooks.md`

---

## Phase 1 · Pflicht-Lektüre (3 Min, still)

Lies in dieser Reihenfolge:

1. `context/ki-phrasen-blackliste.md` — KI-Floskel-Verbote (gilt für jeden Hook)
2. `context/hook-framework.md` — die 5 Hook-Kategorien (Zahlen / Anleitung / Provokant / Neugier / Identifikation)
3. `context/brand-voice.md` — Patricia-Tonalität
4. `context/patricia-expertise.md` — einzige Quelle für Patricia-Zahlen
5. `context/patricia-freebies.md` — aktive Lead-Magnete + DM-Keywords
6. `context/business-info.md` — beide Profile + Zielgruppen
7. `reference/content-bot-system.md` — IDs + Workflow
8. **Memory-Regeln:** alle `feedback_*.md` Files (besonders: keine erfundenen Zahlen, Hooks-Inspiration-nicht-Copypaste, Karussell-max-10-Folien, schweben-statt-hovern, PIE-Strategie-Themen-Variation)
9. **Letzte 4 Wochen:** `outputs/karussells/` + `outputs/reels/` — was haben wir kürzlich gepostet (Doppelung vermeiden)
10. ⭐ **`reference/hormozi/copywriting-bible.md`** — **Hormozi-Bonus-Layer (seit 2026-05-04)**. Wende auf JEDEN der 20 Hooks an: **(a)** Validity-×-Utility-Filter (Hook ist WAHR UND ändert Verhalten? Wenn nur eines davon → streichen, neuen generieren), **(b)** Pain-is-the-Pitch (mind. 6 der 20 Hooks beschreiben Schmerz in einem konkreten MOMENT, nicht abstrakt — „Du stehst um 5:30 in der Küche" statt „Du bist erschöpft"), **(c)** Streue über die 20 Hooks alle 8 Hormozi-Hook-Kategorien (Schock-Statistik, Konträre Meinung, Spez. Versprechen, Curiosity Gap, Pain-Frage, Identifikation, Bevor-Nachher, „Wie X ohne Y") — nicht nur Patricias 5 Kategorien, **(d)** mind. 2 Hooks aktivieren ++/−− × Self/Friends/Enemies-Status-Frame, **(e)** mind. 1 Hook nutzt Authority-Stack-Pattern (3 spezifische Zahlen). **Brand-Voice + doTERRA-Compliance bleiben Pflicht.**

### Wenn doTERRA-Content (Profil @patricia_ulmann) — ZUSÄTZLICHE PFLICHT-LESEN

VOR jeder Caption / Folie / Hook für doTERRA:

- `context/doterra/patricia-wendepunkt-story.md` — Patricias eigene Wendepunkt-Story = Single Source of Truth für jede doTERRA-Aussage
- `context/doterra/lifestyle-pyramide-offiziell.md` — die offizielle 6-Ebenen-Struktur (NUR INTERN für Compliance-Schutz, nie als „doTERRA Pyramide" namentlich nennen)
- `context/doterra/` — komplette Wissensbasis (PDFs, Bücher, doTERRA-Schulungen, Lifestyle-Pyramide). Auch die Unter-Ordner: Basicinfos, Produktwissen, Emotionen und Öle, Mama wird Hausapothekerin, Testwoche, Werbematerial, Ölschule, öltipps
- Memory: `feedback_doterra-compliance-no-heilversprechen.md` — Strikte Compliance-No-Gos (keine Heilversprechen, „bei mir war"-Frame, Lifestyle-Bubble)
- Memory: `feedback_KRITISCH-doterra-keine-erfundenen-fakten.md` — Keine medizinischen Erfindungen
- Memory: `feedback_skills-pflicht-doterra-wissensbasis.md` — Pflicht-Lese-Reihenfolge

**NIE doTERRA-Content erstellen ohne diese Quellen geprüft zu haben.** Bei Unsicherheit: Patricia fragen, nicht raten.

---

## Phase 2 · Wochenfokus aus Notion lesen (2 Min, still)

**PFLICHT vor jeder Hook-Generation.** Patricia plant pro Woche einen Fokus in Notion. Die Hooks sollen DARAUF einzahlen — nicht random sein.

### Wochenplanung-DB

- **Data-Source:** `collection://2ae7078e-8b7e-81e7-9083-000b01908eb5`
- **Aktuelle KW finden:** Filter auf `Zeitraum` enthält heute (Freitag = Ende der KW oder Start der nächsten — checke welche Woche „aktiv" ist; Bot soll Hooks für die KOMMENDE Woche liefern, nicht die laufende)
- **Pflicht-Felder lesen:**
  - **Fokus der Woche** (Hauptthema)
  - Body-Tabelle „Was planst du je Business-Säule?" → Content-Creation-Spalte
  - Aktiver Funnel zum Bewerben
  - Geplante Verkaufs-Aktionen / Launches

### Output Phase 2 (intern)

```
🎯 Wochenfokus KW [N+1]:
- Hauptthema: [aus Notion]
- Mentoring-Säule: [aus Body-Tabelle]
- doTERRA-Säule: [aus Body-Tabelle]
- Aktiver Funnel: [Name + Keyword]
- Verkaufs-Trigger der Woche: [Promo / Bonus / Launch / nichts spezielles]
```

→ Cache: `outputs/freitag/wochen-kontext-KW[N+1].json`

**Wenn Notion nicht verbunden oder kein Wochenfokus eingetragen:**
- Patricia direkt fragen via Telegram-Reply: „Was ist dein Fokus für KW [N+1]?"
- Ohne Fokus keine Hook-Generation — sonst wird's wieder mono.

---

## Phase 3 · Umfassende Marktanalyse (20 Min, still)

**PFLICHT seit 2026-04-28.** Nicht mehr nur Trend-Scraping, sondern eine echte Markt-Analyse je Profil. Ziel: aktuelle **Painpoints, Wünsche, Ziele und Herausforderungen** der Zielgruppe identifizieren — passend zum Wochenfokus aus Phase 2.

### Methodische Tiefe — pro Profil 4 Dimensionen scannen

Für jedes Profil (Mentoring + doTERRA) ALLE 4 Dimensionen abdecken:

#### 3a) PAIN POINTS (was tut weh? was nervt? was raubt Energie?)

**Quellen:**
- **Reddit DACH:** r/Selbststaendig, r/Elternschaft, r/Mommit, r/Multilevel (Negative-Pattern als Vermeidungs-Liste), r/perimenopause, r/WorkingMoms
- **Facebook-Gruppen:** „Network Marketing Mama", „Mama-Selbständigkeit Schweiz", „Hormone in Balance"
- **Instagram-Comments** unter Reels mit ähnlicher Zielgruppe (suche via Hashtag-Search)
- **DMs/Mails der letzten 7 Tage** — Patricia-Telegram-Bot (`bot.mumlifebalance.ch`) hat Monitor-Funktion. Falls aktiv: lese letzte 7 Tage.

**Output Pain-Point-Section:**
- 3-5 echte Schmerzpunkte je Profil mit konkretem Originalzitat (kurz, anonymisiert)
- Markiere: chronisch (immer da) vs. akut (gerade getriggert)

#### 3b) WÜNSCHE (was wollen sie haben/erleben/sein?)

**Quellen:**
- **Pinterest-Suche:** Mama-Coach-Boards, Energie-Mama-Boards (was wird gespeichert?)
- **Google-Trends Schweiz/DACH:** „[Thema] + ich will" — suche Steigungen letzte 30 Tage
- **Konkurrenz-Captions** (top-3 Mama-Coaches): welche Sehnsüchte sprechen sie an?

**Output Wünsche-Section:**
- 3 Top-Wünsche je Profil
- Markiere: erreichbar (Quick Win) vs. langfristig (Vollbild-Transformation)

#### 3c) ZIELE (wo wollen sie hin? wo sehen sie sich in 6-12 Monaten?)

**Quellen:**
- **LinkedIn Mama-Posts** (Schweiz-Filter): Karriere-Wechsel-Geschichten, Selbständigkeits-Geschichten
- **Podcast-Themen** der letzten 30 Tage in Mama-Solopreneurin-Welt
- **TikTok #ZieleMama, #JahreswechselMama, #SelbstständigMitKindern**

**Output Ziele-Section:**
- 3 Hauptziel-Cluster je Profil

#### 3d) HERAUSFORDERUNGEN (was steht zwischen ihnen und dem Ziel?)

**Quellen:**
- Was scheitert immer wieder in den Foren-Posts?
- Welche Einwände kommen in Kommentaren („das ist ja nur was für die mit Geld" / „ich hab keine Zeit" / „bei mir geht das eh nicht weil...")
- **Patricia-Kunden-DM-Patterns** (falls Telegram-Monitor verfügbar)

**Output Herausforderungen-Section:**
- 3 Top-Hürden je Profil (machst du sie zu Hook-Themen!)

### Output Phase 3 — Markt-Analyse-Bericht

```
📊 MARKT-ANALYSE KW [N+1]

🔵 MENTORING (Network-Marketing-Mamas + Mamas die Kleinkinderphase verlassen):

Pain Points:
1. [Schmerz] — Quelle: [Reddit/FB/Insta] — Originalzitat: „..."
2. ...
3. ...

Wünsche:
1. [Wunsch] — Quelle: ...
2. ...
3. ...

Ziele:
1. [Ziel] — Quelle: ...
2. ...
3. ...

Herausforderungen:
1. [Hürde] — wie sie sich äussert: „..."
2. ...
3. ...

🟠 doTERRA (Mamas in Vormenopause, Funktionsmodus, 35+):
[gleiche Struktur]

→ Brücke zum Wochenfokus aus Phase 2:
- Welche Pain Points / Wünsche / Ziele / Herausforderungen passen zum Wochenfokus?
- Daraus ergeben sich automatisch die 10 Hook-Themen pro Profil.
```

→ Cache: `outputs/freitag/markt-analyse-KW[N+1].md`

---

## Phase 4 · Patricia-Lage-Snapshot (5 Min)

### 4a) Aktive Funnels prüfen
Lies `context/active-funnels.json` — welcher Funnel ist gerade live, welches Freebie pusht?

### 4b) Notion-Verkaufsfokus
Notion Content-Management-DB (`2ae7078e-8b7e-811a-ad14-000ba5820c09`) + Produkte-DB (`2ae7078e-8b7e-81ef-aafa-f03993ef344f`):
- Filter: „Wochen-Fokus" oder „Aktiv im Verkauf" für KW [N+1]
- Dokumentiere: Welches Produkt/Freebie ist nächste Woche im Fokus?

### 4c) Letzte 4 Wochen Performance
Schau in `outputs/karussells/` + `outputs/reels/`: welche Hook-Typen wurden zuletzt gepostet? Vermeide direkte Wiederholung.

---

## Phase 5 · 20 Hooks generieren (15 Min, still)

**Pro Profil 10 Hooks**, nummeriert M1-M10 (Mentoring) und D1-D10 (doTERRA).

**Direkte Verknüpfung Pflicht:** Jeder Hook MUSS auf einen konkreten Befund aus Phase 2 (Wochenfokus) ODER Phase 3 (Markt-Analyse: Pain/Wunsch/Ziel/Herausforderung) zurückgeführt werden können. Verknüpfung in der Kategorie-Spalte vermerken (z.B. „Pain-Point #2" oder „Wochenfokus-Hauptthema").

### 🎯 Julia-Trost-Hook-Prinzipien (PFLICHT seit 2026-04-27)

Julia's Cover-Regel (aus „IG Reichweiten Booster"): **„Spezifisch, provozierend. Metapher vermeiden."**

**„BILD-Zeitungs-Headline-Prinzip":** Hook muss in 1 Sekunde gelesen UND verstanden sein. Wie eine Bild-Schlagzeile — direkt, scroll-stoppend, eindeutig. Wenn der Scroller „Was?" denkt → Hook ist tot.

**„Ein Satz, eine Zahl, ein Punkt":** Julia's Klarheits-Formel. Ein konkreter Aspekt, eine konkrete Zahl, ein konkreter Punkt. Nicht 3 abstrakte Sachen verschachtelt.

**Karussell-Hook ≠ Reel-Hook (zwei verschiedene Jobs!):**

| | Karussell-Hook [K] | Reel-Hook [R] |
|---|---|---|
| **Job** | Warme Follower konvertieren | Kalte Reichweite gewinnen |
| **Stil** | Mehrwert SOFORT spürbar | Polarisieren / Hot-Take / POV |
| **Gut wenn...** | Konkrete Zahl + klare Lehre | Identifikation / Bragging / Kritiker-Konter |
| **Beispiel-Pattern** | „5 Sätze in deiner Bio die niemand klickt." | „Crossline: 'Mit Kindern kannst du nichts.' Ich: …" |

### Pro Hook MUSS gelten

- ✅ **1-Sekunden-Test bestanden:** Fremder Scroller versteht Hook beim ersten Sehen ohne Kontext (siehe `feedback_hooks-1-sekunde-verstaendlich.md`)
- ✅ **Keine Insider-Metaphern** aus Patricia's Lehrwelt (Schaufenster, Bibliothek, Fisch-in-der-Nische, Stadt-Land) im Hook selbst — die gehören in Caption/Folien wo sie Kontext bekommen
- ✅ Max 80 Zeichen (Cover-tauglich)
- ✅ Aus einer der Hook-Kategorien (5 Standard + 4 Julia-Erweiterungen — siehe `context/hook-framework.md`)
- ✅ Direkt aus Patricias echter Realität ODER aus Phase-3-Markt-Analyse-Befund
- ✅ Patricia-Voice (deutsch, Schweizer ss, echte Umlaute, intim, ehrlich)
- ✅ KEINE Blackliste-Verletzungen
- ✅ KEINE erfundenen Zahlen
- ✅ Direkt-Bezug zum Wochenfokus aus Phase 2 — mindestens 3-4 Hooks pro Profil zahlen direkt ein

### Hook-Mix pro Profil (Empfehlung)

- 3 **Karussell-tauglich [K]** — Mehrwert + Zahl im Hook spürbar
- 3 **Reel-tauglich [R]** — provozieren, polarisieren, Identifikation
- 4 **Wildcards** (kann Patricia frei zuweisen)

**PIE-Pflicht-Mix (kritisch — siehe `feedback_KRITISCH-pie-strategie-themen-variation.md`):**
- mind. 3 Persönlichkeit (eigene Story / Behind-the-Scenes / Aha-Moment)
- mind. 3 Inspiration (Bragging / Vorher-Nachher / Vision)
- mind. 3 Expertise (Tipps / Listicle / How-To)
- 1 Wild

**Themen-Variation-Pflicht:** mind. 2 verschiedene Pillars/Themen pro Profil. Niemals 10 Hooks zum gleichen Thema.

### Hook-Vielfalt prüfen

Bevor du sendest:
- **PIE-Mix:** mind. 3-3-3-1 wie oben
- Sind die 5 Standard-Kategorien + die 4 Julia-Erweiterungen abgedeckt?
- Wiederholt sich das Satzmuster (z.B. 5× „Du brauchst keine X")? → variieren
- Gibt's mindestens 1 Provokation, 1 Identifikation, 1 Zahl/Fakt pro Profil?
- **Selbsttest pro Hook:** Würde diese Headline auf der Bild-Titelseite stehen können? Wenn nein → zu abstrakt.

### Kontrast-Hook-Zusammenhang-Check (siehe `feedback_kontrast-hooks-zusammenhang.md`)

Bei jedem Hook der zwei Bilder/Sätze gegenüberstellt (You-Can-Be-Both / Kritiker-Kommentar / Vorher-Nachher / Bragging mit Widerstand):

> **PFLICHT-FRAGE:** Würde ein Fremder beim 1-Sek-Lesen kapieren dass die zwei Bilder ZUSAMMENGEHÖREN UND inwiefern?

Wenn nein → eines davon einbauen:
1. **Verbindendes Wort:** „UND", „GLEICHZEITIG", „BEIDES", „AM SELBEN TAG"
2. **Watch-me-Form:** „[Zitat] — Watch me." oder „Hier ist meine Antwort."
3. **Pronomen-Klammer:** „Sie sagen X. Ich Y."

---

## Phase 6 · Markdown speichern + Telegram-Push (5 Min)

### 6a) Markdown speichern
`outputs/freitag/YYYY-MM-DD-hooks.md` mit Struktur:

```markdown
# Hooks der Woche · KW [N+1] · [YYYY-MM-DD]

## Wochenfokus (aus Notion)

- **Hauptthema:** ...
- **Mentoring-Säule:** ...
- **doTERRA-Säule:** ...
- **Aktiver Funnel:** ...
- **Verkaufs-Trigger:** ...

## Markt-Analyse (Kurzform)

**Mentoring:** Pain · Wunsch · Ziel · Herausforderung (je 1 Stichwort)
**doTERRA:** Pain · Wunsch · Ziel · Herausforderung (je 1 Stichwort)

→ Volle Markt-Analyse: `outputs/freitag/markt-analyse-KW[N+1].md`

---

## Mentoring · 10 Hooks (@mumlifebalance_patricia_ulmann)

| # | Empfehlung | Hook | Kategorie | PIE | Bezug zu Phase 2/3 |
|---|---|---|---|---|---|
| M1 | [K] | [Hook-Text] | Provokation | E | Wochenfokus-Hauptthema |
| M2 | [R] | [Hook-Text] | Identifikation | P | Pain-Point #2 |
| ... |

## doTERRA · 10 Hooks (@patricia_ulmann)

[analog]

---

## Pick-Anleitung

Antworte im Chat oder via Telegram-Reply mit:

`Mentoring: M1K, M3K, M5R, M7K, M9R | doTERRA: D2K, D4R, D6K, D8K, D10R`

K = Karussell, R = Reel-Cover. Wähle 5 pro Profil.

⏰ Mo 12:00 läuft `/montag` automatisch + baut alle Designs in Canva und schedulet via Blotato für Di-Sa.
Du hast Zeit zum Picken: jetzt (Fr) bis Mo 11:00.
```

### 6b) Telegram-Push
Format kompakt:

```
🚀 Hooks der Woche · KW [N+1]

🎯 Wochenfokus: [Hauptthema aus Notion]
🔵 Mentoring-Säule: [...]
🟠 doTERRA-Säule: [...]

📊 Markt-Analyse:
🔵 Mentoring Pain: [Stichwort] · Wunsch: [Stichwort]
🟠 doTERRA Pain: [Stichwort] · Wunsch: [Stichwort]

—————————————————

🔵 MENTORING

M1 [K] [Hook]
M2 [K] [Hook]
M3 [K] [Hook]
M4 [R] [Hook]
M5 [R] [Hook]
M6 [R] [Hook]
M7 [Wild] [Hook]
M8 [Wild] [Hook]
M9 [Wild] [Hook]
M10 [Wild] [Hook]

—————————————————

🟠 doTERRA

D1 [K] [Hook]
... (analog)

—————————————————

✅ Pick 5 pro Profil bis Mo 11:00:

Mentoring: M1K, M3K, M5R, M7K, M9R | doTERRA: D2K, D4R, D6K, D8K, D10R

⏰ Mo 12:00 läuft /montag automatisch + Build + Schedule für Di-Sa
📂 Volle Markt-Notes: outputs/freitag/YYYY-MM-DD-hooks.md
```

Sende via:
```bash
node scripts/content-bot/telegram-send.js --text="$(cat /tmp/freitag-telegram.txt)"
```

(Text vorher in `/tmp/freitag-telegram.txt` schreiben.)

---

## Anti-Pattern (was Claude NIE macht)

- ❌ Hooks erfinden ohne Patricia-Realität
- ❌ Hook-Patterns 1:1 von Konkurrenz kopieren
- ❌ Mehr als 3 Hooks aus derselben Kategorie pro Profil
- ❌ Hooks die direkt eine Caption sind
- ❌ Telegram-Push ohne `outputs/freitag/`-Datei
- ❌ Hooks generieren ohne Wochenfokus aus Notion (Phase 2 ist Pflicht)
- ❌ Markt-Analyse skippen wegen Zeitdruck

---

## Wenn etwas schief geht

- Notion nicht verbunden / Wochenfokus leer → Patricia via Telegram fragen
- WebSearch fehlschlägt → ohne Markt-Analyse weiter, in Datei vermerken
- Telegram-Send fehlschlägt → in `outputs/freitag/YYYY-MM-DD-hooks.md` ist alles, Patricia kriegt es beim nächsten /montag mit
