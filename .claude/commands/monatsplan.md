---
description: /monatsplan — Strategie-Layer für den nächsten Monat (1× pro Monat, ~30 Min)
---

# /monatsplan

**Zweck:** Den **Strategie-Layer** für einen kompletten Monat festschnüren. Damit `/freitag-hooks` jede Woche frisch und reaktiv arbeitet — aber innerhalb einer klaren Monats-Storyline.

**Wann ausführen:** Letzter Sonntag des Vor-Monats (z.B. 28.4. für Mai). Idealerweise vor dem ersten `/freitag-hooks` des Monats.

**Output:** Notion-Monatsplan-Page (Updates / Neu) + `outputs/monatsplaene/YYYY-MM.md` + Briefing für die 4 Wochen-Freitage.

> **Neu (seit 2026-06): Monats-Content-Vorplanung.** Patricia will EINMAL pro Monat alles vorplanen, damit sie in **1-2 Tagen alle Reels für den ganzen Monat abdrehen** kann. Deshalb erzeugt dieser Skill jetzt zusätzlich (Phase 4.5): **Marktanalyse + Content-Ideen pro Woche** (thema-matched zum Launch) + eine **Reel-Dreh-Liste zum Batch-Filmen** + die **Rückblick-Analyse** des Vormonats.
>
> **Stories bleiben täglich** (Frische) — sie kommen über den Story-Bot + `/story`: **im Launch** nach dem Julia-Launch-Drehbuch (`story-plan.json` + `julia-launch-story-bausteine.md`), **sonst** nach den Julia-Story-Vorlagen (`julia-insta-stories-anleitung.md` etc.). Die wöchentlichen Posts/Reels stehen als Monats-Skelett; `/freitag-hooks` verfeinert sie nur noch mit Live-Trends.

---

## Output-Ziel

Am Ende dieses Skills hat Patricia:

1. **Säule des Monats** entschieden (1/2/3 Mentoring · Wake-Up/Mama-Körper/4-Säulen/Mental-Load/Identität doTERRA)
2. **3 zu bewerbende Produkte** zugeordnet (0€ / Mini / Gross — laut `context/saeulen-mentoring.md` Block-Logik)
3. **Block-Verteilung** definiert (KW1 = Block A · KW2 = Block B · KW3-4 = Block C — oder Variante B)
4. **Hauptbotschaft** des Monats in 1-2 Sätzen (verbindet alle Posts)
5. **Job-Mix-Soll** pro Profil festgelegt (z.B. Mentoring 4A/4B/2C/2D — oder Pre-Sale-modifiziert 3A/3B/2C/4D)
6. **KPI-Ziel** (z.B. „6 Pre-Sale-Verkäufe + 80 neue Followerinnen + 25 ManyChat-Trigger")
7. **Notion-Monatsplan-Page** ist gefüllt
8. **Output-MD** in `outputs/monatsplaene/YYYY-MM.md`

---

## Phase 1 · Pflicht-Lektüre (5 Min, still)

Lies in dieser Reihenfolge:

1. `context/job-saeulen.md` — Soll-Mix pro Profil
2. `context/saeulen-mentoring.md` — Themen-Achse Mentoring + Block-Logik (Block A/B/C)
3. `context/business-info.md` — Beide Profile + Produkt-Treppe
4. `context/active-funnels.json` — Welche Funnels sind LIVE
5. `context/patricia-expertise.md` — keine Doppelung mit bestehenden Kursen
6. `context/brand-voice.md` — Tonalität für Hauptbotschaft
7. **Letzte 30 Tage:** `outputs/karussells/` + `outputs/reels/` + jüngstes `outputs/apify-runs/competitors-*.json` — was lief, was performte, was die Konkurrenz macht
8. **Vormonats-Notion-Plan** (falls vorhanden): Welche Ziele wurden erreicht, welche nicht

**Zusätzlich für die Content-Vorplanung (Phase 4.5) — Pflicht:**
9. `context/hook-framework.md` — Hook-Regeln + Olga-Pattern-Mix + 8/10-Standard
10. `context/content-formel-5-typen.md` — die 5 Content-Typen pro Woche
11. `context/reichweiten-posts-pattern.md` — Reichweiten-/Verbindungs-Posts (**mind. 2 von 5**)
12. jüngster **Content-Radar** (`context/content-radar-*.md`) — Format-Mix (Mentoring max 1 Karussell + Reels, doTERRA Reels-only), Zeitanker-Hook
13. `context/caption-formeln.md` — Caption-Struktur + Keyword-CTA
13b. **Content-Tresor** (`context/content-tresor/`) — Hook+Caption-Vorlagen-Pool (50 Sets × 5 Säulen). **Reihenfolge:** zuerst `patricia-varianten.json` prüfen (fertige, freigegebene Fassungen für Säule+Profil+Thema → direkt einplanen), sonst passendes Set aus `tresor-vorlagen.json` nehmen, Platzhalter `[…]` mit Wochen-Thema/Painpoint füllen, **in Brand-Voice adaptieren** und die Adaption als Status `test` in `patricia-varianten.json` zurückschreiben. CTA-Typ pro Säule aus dem CTA-Kompass (im JSON). Details: `context/content-tresor/README.md`.
14. **Wochenpläne der aktuellen Monatswochen aus Notion** (Wochenplanung-DB) — Fokus + Produkt + Wochen-CTA (vom Story-Bot/uns gesetzt) → die Content-Ideen müssen dazu passen
15. **Story-Vorlagen:** Launch → `outputs/produkte/mba-launch/story-plan.json` + `context/julia-launch-story-bausteine.md`; sonst → `context/julia-insta-stories-anleitung.md` + `julia-stories-die-verkaufen.md` + `julia-story-ideen.md`
16. Memory-Regeln: **keine Stakkato-Sätze** · keine erfundenen Zahlen · echte Umlaute/ss · doTERRA keine Heilversprechen · **kein „Julia Trost"-Name in Kunden-Output**

---

## Phase 2 · Vormonats-Diagnose (10 Min)

Vor neuem Monat: was hat im vergangenen Monat gewirkt?

### 2a) Notion-Monatsplan vom Vormonat lesen

Notion-DB: `collection://2ae7078e-8b7e-81fc-acf7-000be291c92c`

Aus Vormonats-Page abfragen:
- `3 Monatsziele` — wurden erreicht?
- `Erkenntnis Kennzahlen-Analyse` — was sagen die Zahlen?
- `Erkenntnisse Content-Analyse` — welche Posts performten?
- `Learnings aus dem letzten Monat` — was ändern wir?

### 2b) Job-Mix-Compliance-Check Vormonat

In Content-Management-DB (`collection://2ae7078e-8b7e-811a-ad14-000ba5820c09`) filtern: `Veröffentlichung` im Vormonat + Profil. Dann:

- Wie viele A / B / C / D wurden tatsächlich gepostet?
- Stimmt das mit dem Vormonats-Soll-Mix überein?
- **Wenn D unter 15%:** Sales-Lücke — sollte diesen Monat höher gewichtet werden
- **Wenn C unter 17%:** Reichweite-Lücke — Pain-Hooks/Reels diesen Monat verstärken

### 2c) Output Phase 2 (intern)

```
Vormonat-Diagnose [Monat YYYY]:
- Job-Mix Mentoring tatsächlich: A=X B=X C=X D=X (Soll: 4/4/2/2)
- Job-Mix doTERRA tatsächlich: A=X B=X C=X D=X
- Beste Posts (Saves+Shares): [Top 3]
- Schlechteste Posts: [Bottom 2]
- Korrektur-Vorschlag für neuen Monat: [...]
```

---

## Phase 3 · Strategie-Interview (10 Min)

Die 8 Fragen — Patricia antwortet (Sprachnotiz Wispr Flow oder direkt). Skill ergänzt mit Empfehlung wo nötig.

### Frage 1: Welche Säule prägt diesen Monat?

**Mentoring-Optionen:** Säule 1 (NWM 2.0) · Säule 2 (Hybridmodell) · Säule 3 (Mama Business)
**doTERRA-Optionen:** Wake-Up · Mama-Körper 35+ · 4 Säulen · Mental Load · Identität

**Empfehlung-Logik:** Wenn Pre-Sale läuft → Premium-Bundle = Säule 3 / Mama Business. Wenn Validation-Phase doTERRA → Wake-Up als Anker.

### Frage 2: Welche 3 Produkte werden beworben?

| Block | Produkt-Typ | Beispiele |
|---|---|---|
| **0€** | Lead-Magnet | Bio-Check / Workbook / 0€-Starterguide / Lead-Challenge |
| **Mini** | 27-97 CHF | „Finde dein Thema in 60 Min" / „IG-Kundenmaschine" / 30-Tage-Energie-Kur-Mini |
| **Gross** | 297-1.500 CHF | Magnet-ich 1:1 / Premium-Bundle / „Vom Networkwissen zur Produktwelt" |

→ Aus `context/active-funnels.json` ablesen + abfragen welche Patricia priorisieren will.

### Frage 3: Block-Verteilung — Variante A oder B?

**Variante A (Wochen-Blöcke — empfohlen):**
- KW 1: Block A (0€-Push, Reichweite + Liste)
- KW 2: Block B (Mini-Push, Validation + Cash)
- KW 3-4: Block C (Gross-Push, Hauptverkauf)

**Variante B (Tag-für-Tag-Mix):**
- Pro Tag wechselt der Bewerbungs-Fokus
- Komplexer, aber realistischer wenn 0€-Funnel laufend Leads bringt

→ Skill empfiehlt A, außer Patricia sagt explizit B.

### Frage 4: Hauptbotschaft des Monats?

**Format:** 1-2 Sätze. Verbindet alle 12 Posts. Wirkt wie ein „Album-Titel" für den Monat.

**Beispiele:**
- Mai 2026 Mentoring: *„Premium ist nicht teurer Stundenlohn. Premium ist Transformation in einem Container — und ich baue meinen gerade live."*
- Juni 2026 doTERRA: *„Vormenopause ist kein Tabu mehr. Sie ist deine Einladung, dich neu zu kennenzulernen — bevor dein Körper es für dich entscheidet."*

→ Falls Patricia keine hat: Skill schlägt 3 Varianten vor basierend auf Säule + Produkt.

### Frage 5: Job-Mix-Soll für diesen Monat?

**Default (laut `job-saeulen.md`):**
- Mentoring: 4A/4B/2C/2D = 33/33/17/17
- doTERRA Aufbau: 4A/4B/4C/0D = 33/33/33/0
- doTERRA Launch: 4A/4B/3C/1-2D = 33/33/25/8-15

**Modifikatoren:**
- **Pre-Sale-Monat:** D auf 25% (3D), C auf 8% (1C) — mehr Sales-Druck
- **Reichweite-Push (neue Phase):** C auf 33% (4C), A auf 25% (3A)
- **Storytelling-Monat:** B auf 42% (5B), A auf 17% (2A)

→ Skill fragt: „Standard, Pre-Sale-Modus oder eigener Mix?"

### Frage 6: KPI-Ziel?

**Empfohlene KPIs:**
- Verkäufe (Stück / CHF)
- Neue Followerinnen
- ManyChat-Keyword-Trigger (Funnel-Eintritte)
- Saves auf Top-Karussell (= Methoden-Stärke)
- DM-Replies auf Top-Story (= Story-Resonanz)

**Format:** „X Verkäufe + Y Followerinnen + Z ManyChat-Trigger"

### Frage 7: Was läuft NICHT diesen Monat?

Bewusste Entscheidungen was ausgeklammert wird:
- Welche Säule pausiert?
- Welches Produkt wird nicht erwähnt?
- Welche Plattform/Format wird ausgesetzt?

→ Verhindert Gießkanne. Macht Fokus konkret.

### Frage 8: Persönliche Energie-Lage

- Wie viele Wochen sind „voll arbeitsfähig"?
- Gibt's Schulferien / Familien-Ereignisse / Krankheiten in Sicht?
- Wenn 1-2 Wochen reduziert: Plan dafür anpassen (mehr Recycling, weniger neue Aufnahmen)

---

## Phase 4 · Plan generieren (5 Min, still)

Aus den 8 Antworten + Phase-2-Diagnose generieren:

### 4a) Wochenfokus-Skelett (4 Wochen)

| KW | Datum | Block | Produkt im Fokus | Job-Mix-Soll | Spezial |
|---|---|---|---|---|---|
| KW X | dd.mm.-dd.mm. | A (0€) | Bio-Check | 1A 1B 1C | Reichweite-Woche, Story zeigt eigene Nutzung |
| KW X+1 | dd.mm.-dd.mm. | B (Mini) | „Finde dein Thema" | 1A 1B 1C | Validation-Mails parallel |
| KW X+2 | dd.mm.-dd.mm. | C (Gross) | Premium-Bundle | 1A 1B 1D | Pre-Sale-Push |
| KW X+3 | dd.mm.-dd.mm. | C (Gross) | Premium-Bundle | 1A 1B 1D | Verknappung + Cases |

### 4b) Hauptbotschaft als „Storyline"

Die Hauptbotschaft wird als roter Faden über die 4 Wochen gespannt:
- KW 1: Hauptbotschaft anteasern (Aha-Moment)
- KW 2: Methode dahinter zeigen
- KW 3: Beweise / Cases / Live-Building
- KW 4: Verknappung + Reflexion

### 4c) Hooks-Vorschau (3 pro Woche, optional)

**Optional — nur wenn Patricia es will:** Skill schlägt 3 Hook-Richtungen pro Woche vor (nicht ausformuliert — nur Konzept). Damit hat `/freitag-hooks` jede Woche schon einen Anker.

→ **Default: NICHT machen.** /freitag-hooks soll wöchentlich frisch arbeiten. Nur auf explizite Patricia-Bitte.

---

## Phase 4.5 · Monats-Content-Vorplanung (NEU — der eigentliche Content)

> Hier entsteht der konkrete Monats-Content, damit Patricia in 1-2 Tagen alles abdrehen kann. Baut auf den Wochenplänen aus Notion auf (Fokus + Produkt + CTA pro Woche).

### 4.5a) Marktanalyse pro Profil (Pflicht — „ich kann ihre Gedanken lesen")

Pro Profil (Mentoring + doTERRA), ausgerichtet aufs **Monats-/Launch-Thema**:
- **Pain · Wunsch · Ziel · Herausforderung** der Zielgruppe
- Quellen: jüngstes `outputs/apify-runs/competitors-*.json` + `discovery-*.json`, bei Bedarf WebSearch (IG/Reddit/Google Trends), `context/patricia-vollprofil.md` + Zielgruppen-Research
- → 1 verdichteter Absatz pro Profil, der die Hooks speist (jeder Beitrag adressiert mind. 1 davon)

### 4.5b) Vormonats-Content-Analyse (Pflicht)

Aus Content-Management-DB (`collection://2ae7078e-8b7e-811a-ad14-000ba5820c09`) + `outputs/reels/` + `outputs/karussells/`:
- **Top 3** (Saves/Shares/Reach) — was wiederholen?
- **Flop 2** — was lassen?
- Welche **Typen / Themen / Hook-Muster** liefen? → fliesst in die Ideen für den neuen Monat

### 4.5c) Pro Woche: 5 Beiträge (thema-matched)

Für **jede Woche** des Monats (Fokus + Produkt + CTA aus dem Notion-Wochenplan):
- **5 Beiträge** nach den **5 Content-Typen** (`content-formel-5-typen.md`)
- davon **mind. 2 = reine Reichweiten-/Verbindungs-Posts** (kein Verkauf, Share-Trigger, Mama-Identity — `reichweiten-posts-pattern.md`). CTA „Teile das in deiner Story", **kein** Keyword.
- die übrigen 3 = Mehrwert / Story / Sales passend zum **Wochen-Produkt**, mit **Keyword-CTA**
- **Format-Mix** (Content-Radar): Mentoring max 1 Karussell + Rest Reels · **doTERRA Reels-only**
- pro Beitrag festhalten: **Hook** (nach `hook-framework.md` + Olga-Pattern-Mix + Zeitanker + 8/10 + **keine Stakkato**) · Typ · Format · Ziel (Reichweite/Lead/Sales) · adressierter Painpoint (aus 4.5a)

### 4.5d) Reel-Dreh-Liste (Batch — zum Abdrehen in 1-2 Tagen)

ALLE Reels des Monats in EINER Tabelle, gruppiert nach **Setting/Outfit**, damit Patricia sie am Stück filmen kann:

| # | Woche | Produkt | Hook (Slide 1) | Dreh-Anweisung / Sprechtext (wort-für-wort bei Talking-Head, sonst Shotlist) | Format/Setting | B-Roll |
|---|---|---|---|---|---|---|

→ So weiss Patricia vorab **genau, was sie aufnehmen muss**. Sprechtexte sind Dreh-Anweisung; die finale Caption feilt `/freitag-hooks` / `/reels`.

### 4.5e) Story-Logik (täglich — NICHT vorab ausformulieren)

Stories kommen täglich über den Story-Bot + `/story`. Der Monatsplan hält pro Woche nur den **Story-Bogen** (Thema + Käufertyp-Rotation), nicht die fertigen Slides:
- **Im Launch-Fenster:** `/story` baut nach der **Funnel-/Launch-Strategie** — `outputs/produkte/mba-launch/story-plan.json` + `context/julia-launch-story-bausteine.md` (Tag für Tag, Slide für Slide).
- **Ausserhalb Launch:** `/story` baut nach den **Story-Vorlagen** — `context/julia-insta-stories-anleitung.md` (10 Templates) + `julia-stories-die-verkaufen.md` + `julia-story-ideen.md`.

### 4.5f) Monats-Blogartikel + Newsletter (gehören in den Monatsplan)

- **Blogartikel (1×/Monat):** Thema zum Monats-/Launch-Fokus festlegen → wird via `/blog` erstellt (SEO + Cascade-Output, der Stories/Karussell/Reel/Newsletter speist). Hier festhalten: Thema · Keyword · Ziel-CTA.
- **Mail-Newsletter:** Rhythmus + Themen pro Woche festlegen.
  - **Im Launch:** die Launch-Mail-Sequenz (Webinar-Einladung → Confirmation → Sales → No-Show).
  - **Sonst:** Mehrwert-Newsletter, der auf den Wochenfokus + das aktuelle Produkt führt (1 Emotion + 1 konkreter Tipp + 1 CTA).
- Blog + Newsletter ziehen **denselben Painpoint/Pillar** wie die Posts (aus 4.5a/4.5c) → ein roter Faden über Blog · Newsletter · Posts · Stories. Regeln gelten überall: keine Stakkato, echte Umlaute/ss, keine erfundenen Zahlen, kein „Julia"-Name im Kunden-Output, doTERRA = Compliance.

---

## Phase 5 · Speichern

### 5a) Notion-Monatsplan-Page (neu / Update)

In Monatsplanung-DB (`collection://2ae7078e-8b7e-81fc-acf7-000be291c92c`):

**Bei neuem Monat:** Page anlegen mit Title „🚀 [Monat] [Jahr]" + Zeitraum + Properties.

**Properties füllen:**
- `3 Monatsziele` ← KPI-Ziel ausgeschrieben
- `Erkenntnis Kennzahlen-Analyse` ← aus Phase 2b (Job-Mix-Compliance)
- `Erkenntnisse Content-Analyse` ← Top/Bottom-Posts Vormonat
- `Learnings aus dem letzten Monat` ← Korrekturen für neuen Monat

**Body-Block strukturiert:**

```
## Hauptbotschaft des Monats
[1-2 Sätze]

## Säule des Monats
- Mentoring: Säule X — [Name]
- doTERRA: [Pillar-Name]

## Block-Verteilung
- KW X: Block A — Produkt: [...]
- KW X+1: Block B — Produkt: [...]
- KW X+2/3: Block C — Produkt: [...]

## Job-Mix-Soll
- Mentoring: XA / XB / XC / XD
- doTERRA: XA / XB / XC / XD

## Was nicht passiert
- [...]
```

### 5b) Output-MD speichern

Pfad: `outputs/monatsplaene/YYYY-MM.md`

**Vorlage:**

```markdown
# Monatsplan [Monat YYYY]

**Erstellt:** YYYY-MM-DD
**Zeitraum:** dd.mm.YYYY – dd.mm.YYYY
**Notion-Page:** [Link]

---

## Strategie auf einen Blick

**Säule des Monats (Mentoring):** [...]
**Säule des Monats (doTERRA):** [...]
**Hauptbotschaft:** [1-2 Sätze]
**KPI-Ziel:** [...]

---

## Vormonats-Diagnose

[Aus Phase 2 — was hat gewirkt, was nicht]

---

## Block-Verteilung über die 4 Wochen

[Tabelle aus 4a]

---

## Job-Mix-Soll

[Mentoring + doTERRA in Tabelle]

---

## Was läuft NICHT diesen Monat

[Aus Phase 3 Frage 7]

---

## Energie-Lage

[Aus Phase 3 Frage 8 — voll arbeitsfähige Wochen + Adaptionen]

---

## Briefing für /freitag-hooks (4 Wochen)

### KW [X] (dd.mm.-dd.mm.) — Block [A/B/C]
- **Wochenfokus:** [...]
- **Produkt im Fokus:** [...]
- **Job-Mix-Soll:** [...]
- **Special:** [z.B. „Reichweite-Woche, BTS-Story zeigt eigene Nutzung"]

[wiederholen für KW X+1, X+2, X+3]

---

## CTA für nächste Schritte

1. Sonntag dieser Woche: ersten `/freitag-hooks` mit diesem Monatsbriefing laufen lassen
2. Patricia pickt 5 Hooks pro Profil → /montag baut
3. Mid-Month-Check (Mi der KW X+1): Live-Performance vs. KPI-Ziel — ggf. Block-Verteilung in KW X+2/3 anpassen
4. Ende Monat: nächster `/monatsplan`-Lauf nutzt diesen als Vormonats-Referenz
```

### 5c) Telegram-Push (optional)

Falls Patricia es will: Kurz-Zusammenfassung (Säule + Hauptbotschaft + KPI-Ziel) als Telegram-Nachricht.

---

## Anti-Pattern (was Claude NIE macht)

- ✅ Monats-Content vorplanen ist JETZT erwünscht: Ideen + Hooks pro Woche (5 Beiträge, ≥2 Reichweiten) + **Reel-Dreh-Liste** zum Batch-Filmen.
- ❌ ABER: **Stories NIE vorab ausformulieren** — die kommen täglich frisch über `/story` (Launch = Drehbuch, sonst = Story-Vorlagen).
- ❌ Reel-Sprechtexte sind **Dreh-Anweisung**, nicht die endgültige Caption (die feilt /freitag-hooks/​/reels).
- ❌ Hauptbotschaft erfinden ohne Patricia zu fragen
- ❌ Block-Verteilung Variante B empfehlen ohne Erklärung
- ❌ KPI-Zahlen erfinden (immer Patricia fragen oder Vormonat als Anker)
- ❌ Vormonats-Diagnose überspringen (kritisch für Korrektur)
- ❌ Notion-Monatsplan-Page neu anlegen wenn schon eine existiert (immer erst suchen)
- ❌ Pre-Sale-Modus annehmen ohne Patricia-Bestätigung

---

## Wenn etwas schief geht

- **Notion-DB nicht erreichbar:** Patricia bittet Schreib-Access zu prüfen. Skill macht trotzdem Output-MD lokal.
- **Vormonats-Daten fehlen:** Skill fragt Patricia nach den 3 wichtigsten Erkenntnissen
- **Patricia hat keine klare Säule:** Skill schlägt 2 Varianten vor + lässt sie wählen
- **Mehr als 1 Produkt pro Block:** OK, aber Hauptbotschaft muss zu BEIDEN passen — sonst trennen

---

## Verbindung zu anderen Skills

| Skill | Was nutzt es vom Monatsplan |
|---|---|
| `/freitag-hooks` | Wochenfokus + Produkt + Job-Mix-Soll aus Monats-Briefing |
| `/montag` | Block-Verteilung um zu wissen was beworben wird |
| `/karussell` + `/reels` | Hauptbotschaft als roten Faden |
| `/story` | Säule des Monats für Story-Sequenzen |
| `/funnel` | Welche Funnels diesen Monat aktiviert sind |

→ **Wenn der Monatsplan fehlt:** Andere Skills laufen trotzdem, aber ohne Monats-Storyline. Telegram-Reminder am 28. jeden Monats: „Monatsplan für [Folgemonat] schon gemacht? `/monatsplan` ausführen."
