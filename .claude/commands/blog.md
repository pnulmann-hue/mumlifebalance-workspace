---
description: SEO-optimierter Blog-Post zum Monatsthema, mit Cascade-Output für Stories/Karussell/Reel/Newsletter
argument-hint: [konzept|komplett|aktualisieren] [optionale Thema-Spezifizierung]
allowed-tools: Read, Write, Edit, Grep, Glob, WebSearch, mcp__4800d39a-57ef-4b8c-ac59-912964e81676__notion-fetch, mcp__4800d39a-57ef-4b8c-ac59-912964e81676__notion-search
---

# /blog — Patricia's Blog-Skill (SEO + GEO + Cascade)

Generiert SEO-optimierte Blog-Posts zum Monatsfokus. Output ist NICHT nur ein Blog —
sondern eine **Content-Cascade** die die ganze Woche füttert (Stories, Karussell, Reel, Newsletter).

**Workflow:** 1× pro Monat (erster Mo). Nutzt Monats-Gross-Produkt aus Notion als Thema.

---

## 🚨 PFLICHT: Keine Stakkato-Sätze (Brand-Voice-Override)

Patricia hat MEHRFACH angemahnt — gilt für JEDEN Blog-Absatz UND alle Cascade-Outputs. Siehe `feedback_KRITISCH-keine-stakkato-saetze.md`.

❌ FALSCH: „Du bist erschöpft. Du schläfst nicht. Du funktionierst nur noch."
✅ RICHTIG: „Du bist erschöpft, schläfst kaum noch und funktionierst eigentlich nur noch — und du weisst genau dass das so nicht weitergeht."

**Regeln:**
- NIE drei abgehackte Subject-Verb-Punkt-Sätze hintereinander
- Konjunktionen verbinden Sätze („und da", „weil", „aber", „bis", „dann")
- DU-Anrede für Pain (nicht „Ich" — Leserin soll sich erkennen)
- Wie am Küchentisch mit einer Freundin geschrieben — auch wenn's ein SEO-Blog ist
- Schweizer ss durchgängig, kein deutsches ß
- **Diese Regel übersteuert SEO-/Hormozi-Default.** Keywords ja, abgehackte Sprach-Form NICHT.

Stakkato erlaubt NUR bei expliziten H2-/H3-Listen oder Aufzählungen — nicht im Fliesstext.

---

---

## Pflicht-Lese-Liste (IMMER vor Generierung)

```
1. reference/seo-blog/seo-blog-bible.md           (SEO 2026 + Hormozi-Hooks + Julia-Voice)
2. context/brand-voice.md                          (Patricia's Tonalität)
3. context/hook-framework.md                       (Hook-Kategorien)
4. context/ki-phrasen-blackliste.md                (was NIE schreiben)
5. context/active-funnels.json                     (welche CTAs/Funnels aktiv)
6. context/patricia-vollprofil.md                  (Brand-Voice, Wortschatz, Verbote)
7. context/notion-business-brain.md                (System-Verständnis)
8. reference/hormozi/copywriting-bible.md          (Hormozi-Frameworks)
9. context/julia-stories-die-verkaufen.md          (Storytelling)
```

**Bei doTERRA-Thema zusätzlich:**
```
context/doterra/patricia-wendepunkt-story.md
context/doterra/lifestyle-pyramide-offiziell.md
```

---

## Modus-Erkennung

User-Input nach `/blog` analysieren:

| Eingabe | Modus |
|---|---|
| `/blog` (leer) | komplett (Default) |
| `/blog konzept` | nur Outline + Recherche |
| `/blog komplett` | Full-Draft + Cascade |
| `/blog aktualisieren <slug>` | Bestehenden Blog refreshen |
| `/blog [thema]` | komplett mit User-Thema-Override |

---

## Schritt-für-Schritt-Workflow

### Phase 1 — Kontext laden (10 Sek)

1. **Pflicht-Lese-Liste** komplett laden (siehe oben)
2. **Notion lesen:**
   - Aktueller Monatsplan → Gross-Fokus-Produkt-Name
   - Aktuelle Wochenplanung → ergänzender Kontext
   - Active-Funnels-Eintrag des Gross-Produkts
3. **Heutiges Datum + KW** identifizieren
4. **Profil bestimmen:** aus Wochenstruktur (siehe Notion „Wochenstruktur Patricia 2026")

### Phase 2 — Thema-Validierung (mit Patricia)

**Kompakt fragen:**

```
📝 Blog-Briefing für [Monat]

Monats-Gross-Produkt: [aus Notion]
Vorgeschlagenes Thema: [abgeleitet aus Produkt-Transformation]

Bevor ich schreibe:
1. Stimmt das Thema oder anders schwerpunkten?
2. Hast du eine konkrete Story aus den letzten Wochen 
   die ich einbauen soll? (Voice-Notiz reicht)
3. Welcher Kunden-Pain soll diesen Blog hooken?
4. Ein konkreter Anker den DU einbringen willst (Beispiel/Zahl/Erlebnis)?
```

**Patricia antwortet → erst dann schreiben.**

### Phase 3 — Markt-Puls + Recherche (WebSearch)

**Patricia-Mantra:** „Ich will, dass meine Zielgruppe denkt, ich kann ihre Gedanken lesen."

**Vor jedem Blog ZWINGEND:**

#### 3a) Markt-Puls aufnehmen (echte Painpoints/Wünsche/Ziele/Herausforderungen)

WebSearch-Queries (mind. 4 verschiedene):

1. **Reddit-Puls:**
   - `site:reddit.com [Primärkeyword] frustration` 
   - `site:reddit.com [Zielgruppe] struggle 2026`
   - z.B. „site:reddit.com network marketing mama struggle"
   - Subreddits: r/Solopreneur, r/networking_marketing, r/MamaBusiness, r/Selbstständigkeit, r/digitalnomad

2. **Google-Trends + Ähnliche Suchanfragen:**
   - Was suchen Leute aktuell zum Thema?
   - „[Primärkeyword] 2026" — aktuelle Variationen
   - „warum [Pain] [Zielgruppe]" — Pain-Formulierungen

3. **Facebook-/Forum-Puls:**
   - „[Zielgruppe] facebook gruppe diskussion 2026"
   - Quora-Antworten wenn relevant

4. **Konkurrenz-Comments-Puls:**
   - Welche Themen kommen in Comments-Sections von Konkurrenten?
   - Was sind die häufigen Einwände?

#### 3b) Strukturierter Markt-Output

Bot extrahiert aus Recherche:

```markdown
## MARKT-PULS — [Thema] — [Datum]

### TOP 5 AKTUELLE PAINPOINTS
1. [Painpoint mit Zitat-Quelle aus Reddit/Forum]
2. ...

### TOP 3 AKTUELLE WÜNSCHE  
1. [Was die Zielgruppe gerade konkret will]
2. ...

### TOP 3 AKTUELLE ZIELE
1. [Was sie aktuell ERREICHEN wollen]
2. ...

### TOP 3 AKTUELLE HERAUSFORDERUNGEN
1. [Was sie gerade BLOCKIERT]
2. ...

### WORTSCHATZ DER ZIELGRUPPE
- Wie nennen SIE das Problem? (nicht Patricia's Sprache)
- Welche Wörter wiederholen sich?
- Welche Emotionen kommen durch?
```

#### 3c) Patricia-Validierung VOR Blog-Schreiben

Bot zeigt Patricia den Markt-Puls und fragt:

```
🔍 Markt-Recherche [Thema] — Top 5 aktuelle Painpoints:

1. [...]
2. [...]
3. [...]
4. [...]
5. [...]

Welcher davon (oder welche Kombination) trifft am meisten auf deine 
echten DMs/Comments zu? Hast du andere Painpoints die du aktuell siehst?
```

**Patricia bestätigt 1-2 Top-Painpoints** → DIESE sind der Hook + roter Faden.

#### 3d) Keyword-Recherche

Zusätzlich:
- Long-Tail-Keywords zum Thema
- Konkurrenz-Analyse („was rankt aktuell für Primärkeyword")
- Aktuelle Trends + Statistiken (mit Quellen-Link)

**WICHTIG:** Statistiken NUR übernehmen wenn Quelle solid (Forbes, HBR, Statista, etc.).
Niemals Statistiken erfinden.

#### 3e) Patricia's eigene Daten ergänzen

- Liest Reichweiten-Tracking-DB → was performt aktuell auf Patricia's Profilen?
- Liest Content-Management-DB → welche Patricia-Posts hatten zuletzt hohes Engagement?
- DAS sind weitere Indikatoren was die Zielgruppe gerade trifft.

### Phase 4 — Blog schreiben (Hauptarbeit)

**Struktur (nach SEO-Blog-Bible):**

```markdown
---
title: "[H1 max 60 Zeichen, SEO-optimiert]"
slug: "[primärkeyword-mit-bindestrich]"
meta_description: "[140-155 Zeichen, mit CTA]"
primary_keyword: "[Long-Tail Keyword]"
secondary_keywords: ["[Sek 1]", "[Sek 2]", "[Sek 3]"]
reading_time: "[X] Min"
date: 2026-MM-DD
author: Patricia Ulmann
category: [Mentoring / doTERRA]
related_funnel: [funnel-id aus active-funnels.json]
---

# [H1 — Hormozi-Hook]

## TL;DR
[Box mit 3-5 Bullet-Points der Kernaussagen — für AI-Quotability]

## Einleitung (1-3 Sätze, direkt in den Pain)

[Hook-Story-Einstieg mit konkretem Patricia-Anker]

## [H2 Sektion 1: erste Lehre]

[Story → Lehrwert]

## [H2 Sektion 2: zweite Lehre]

...

## [H2 Sektion 5-8 Ende: konkreter Pfad]

[Step-by-Step ODER konkrete Empfehlung]

## Fazit

[3-5 Sätze, Transformation des Lesers]

## Wie geht's weiter?

[CTA zum Monats-Gross-Produkt mit URL + ManyChat-Keyword]

## Häufige Fragen (FAQ)

### [Frage 1 — als H3]
[Antwort 50-100 Wörter]

### [Frage 2]
[Antwort]

[5-7 FAQ insgesamt]

---

**Über Patricia**
[Kurz-Bio mit Experience + Expertise — 50-80 Wörter]
```

**Regeln beim Schreiben:**

1. **Wörter-Range:** 1500-2500 (1800 ideal)
2. **Hook in H1:** Hormozi-Style aus seo-blog-bible.md
3. **Patricia-Voice:** Du-Form, konkrete Anker, Vulnerability
4. **Specific over Abstract:** Zahlen, Daten, Erlebnisse
5. **TL;DR-Box:** für GEO/AI-Search-Quotability
6. **FAQ-Sektion:** PFLICHT (Google ranking + Featured Snippets)
7. **Internal Links:** 3-5 zu anderen Blog-Posts oder Salespages
8. **External Links:** 1-2 zu Authority-Quellen (mit Quellen-Angabe)
9. **Bilder-Hinweis:** wo welche Bild-Idee gehört (Patricia macht das selbst)
10. **Anti-Halluzinations-Check:** ALLE Zahlen/Daten verifiziert

### Phase 5 — Cascade-Output erzeugen

**Direkt im Anschluss aus dem Blog generieren:**

```markdown
## 📱 Story-Hooks (für /story-Skill)

1. **Hook 1 (aus H1):**
   "[Hook-Text mit Bezug zum Blog]"
   Eyebrow: "[Eyebrow für Story-Slide]"

2. **Hook 2 (aus Pain-Sektion):**
   ...

3. **Hook 3 (aus CTA):**
   ...

## 🎨 Karussell-Konzept (für /karussell-Skill)

Cover: [Karussell-Cover-Hook]
Slide 2: [H2-Sektion 1 als Slide]
Slide 3: [H2-Sektion 2 als Slide]
Slide 4-7: [weitere H2-Sektionen]
Slide 8: TLDR
Slide 9: CTA mit Link

## 🎬 Reel-Konzept (für /reels-Skill)

Hook: [H1 als 5-Sekunden-Hook für Reel]
30-Sek-Skript:
[Aus TLDR-Box ableitbares Skript]
CTA: "Voller Blog auf [URL]"

## 📧 Newsletter-Snippet (~250 Wörter)

Subject: [Newsletter-Title basierend auf Blog]
Lead: [1-2 Sätze Hook]
[Story-Auszug aus Blog, max 200 Wörter]
[Bridge zum Blog: „Den ganzen Artikel mit Schritt-für-Schritt-Anleitung findest du hier: [URL]"]
CTA zum Monats-Gross-Produkt
```

### Phase 6 — Output-Speicherung (LOKAL)

**Speicher-Pfad:**
```
outputs/blogs/YYYY-MM-DD-[slug]/
├── blog.md                    (Haupt-Blog für WordPress-Import)
├── cascade.md                 (Story+Karussell+Reel+Newsletter)
├── seo-meta.json              (Title/Description/Keywords als JSON)
├── _briefing.md               (Patricias Original-Antworten archiviert)
└── images-todo.md             (Welche Bilder Patricia noch macht)
```

### Phase 7 — Notion-Push (PFLICHT, immer)

**Patricia-Regel:** „Der erarbeitete Inhalt ist auch immer in Notion abzulegen."

Alle 5 Content-Outputs (Blog + 3 Stories + 1 Karussell + 1 Reel + 1 Newsletter)
landen als Einträge in **Content-Management-DB** mit Recycling-Verknüpfung.

**Content-Management-DB:** 
`2ae7078e-8b7e-8134-9e36-f8c630a850f2`
Data-Source: `2ae7078e-8b7e-811a-ad14-000ba5820c09`

**Templates (vorhanden!):**
- Blogartikel: `2ae7078e-8b7e-813d-a01d-fbb4f62c568d`
- Story: `2bd7078e-8b7e-801b-8199-dcc5973bbaf6`
- Karussell: `2ae7078e-8b7e-8129-9916-e122b022261b`
- Reel: `2ae7078e-8b7e-8114-8538-e866fb94e8b6`
- Newsletter: `2ae7078e-8b7e-8197-9005-d7a9a4a1a295`

**Push-Reihenfolge:**

#### 7a) BLOG-Eintrag erstellen (Master)

```
Content-Titel: [Blog-H1]
Content-Typ: ["Blogartikel"]
Status: "Erstellung abgeschlossen"
Veröffentlichung: [geplantes Datum]
Content-Säule: [Relation zur passenden Säule aus Content-Strategie-DB]
Produkt Verknüpfung: [Relation zum Monats-Gross-Produkt]
Käufertypen: [welche Personas spricht der Blog an: Willi/Amelie/Ina/Zoe/Rudi/Frank]
Launch-Phase: [aktuelle Phase: Aufwärmphase/Secret Offer/Verkaufsphase/Nachkaufphase/Evergreen]
Ziel: [Verkaufen / Vertrauen aufbauen / Reichweite aufbauen / Expertise zeigen]
Keyword: [Primärkeyword]
Storyart: [Persönliche Geschichte / Schritt-für-Schritt / Mythos-Brecher / etc.]
Kurzbeschreibung: [Meta-Description aus SEO-Meta]
Briefing-Link: [Link zu outputs/blogs/.../blog.md]
URL veröffentlicht: [später, wenn auf WP live]

Page-Body: 
  Vollständiger Blog-Markdown (Patricia kann direkt in Notion lesen/editieren)
```

#### 7b) STORY-Einträge (3 Stück, Recycling)

Pro Story-Hook aus Cascade:

```
Content-Titel: [Story-Hook-Text]
Content-Typ: ["Story"]
Status: "Idee"
Storyart: [aus Hook abgeleitet]
Recycling Content: [Relation zum BLOG-Eintrag oben]
Content-Säule: [gleich wie Blog]
Produkt Verknüpfung: [gleich wie Blog]
Käufertypen: [aus Hook abgeleitet]
Launch-Phase: [gleich wie Blog]
Briefing-Link: [Link zur cascade.md]

Page-Body:
  - Hook-Text
  - Eyebrow-Vorschlag
  - Slide-Skelett (8 Slides)
  - Bezug zum Blog-Inhalt
```

#### 7c) KARUSSELL-Eintrag

```
Content-Titel: [Karussell-Cover-Text]
Content-Typ: ["Karussell"]
Status: "Idee"
Recycling Content: [Relation zum BLOG-Eintrag]
Content-Säule: [gleich wie Blog]
Produkt Verknüpfung: [gleich wie Blog]
Käufertypen: [gleich wie Blog]
Launch-Phase: [gleich wie Blog]
Briefing-Link: [Link zur cascade.md]

Page-Body:
  - Cover-Slide-Konzept
  - Slide 2-9 Konzepte (aus H2-Sektionen)
  - CTA-Slide-Konzept
```

#### 7d) REEL-Eintrag

```
Content-Titel: [Reel-Hook]
Content-Typ: ["Reel"]
Status: "Idee"
Recycling Content: [Relation zum BLOG-Eintrag]
... (gleich wie oben)

Page-Body:
  - 5-Sek-Hook
  - 30-Sek-Skript
  - Format-Vorschlag (Talking Head / B-Roll / Text-Overlay)
  - CTA
```

#### 7e) NEWSLETTER-Eintrag

```
Content-Titel: [Newsletter-Subject]
Content-Typ: ["Newsletter"]
Status: "Erstellung abgeschlossen"
Recycling Content: [Relation zum BLOG-Eintrag]
... (gleich wie oben)

Page-Body:
  - Vollständiger Newsletter-Text
  - Link zum Blog
  - CTA
```

#### 7f) Cascade-Verknüpfung sichtbar machen

Im BLOG-Eintrag → Recycling Content Relation (umgekehrt) wird automatisch
befüllt mit den 5 Cascade-Einträgen. Patricia sieht in Notion:

```
📰 Blog: „Wie ich als 4-fach-Mama..." [Blogartikel]
   └─ Recycling Content (5):
      🎬 Reel: „Die 30-Sek-Wahrheit über..."
      📱 Story 1: „Hey, kennst du diesen Moment..."
      📱 Story 2: „Was niemand dir sagt über..."
      📱 Story 3: „Wenn du nur eines mitnimmst..."
      🎨 Karussell: „5 Schritte für..."
      📧 Newsletter: „Mein Mai-Highlight"
```

→ 1 Klick zeigt die ganze Wochen-Pipeline aus 1 Blog.

### Phase 8 — Bestätigung an Patricia

```
✅ Blog-Cascade in Notion abgelegt:

  📰 Blog: [Notion-Link]
  📱 3 Stories: [Notion-Links]
  🎨 1 Karussell: [Notion-Link]
  🎬 1 Reel: [Notion-Link]  
  📧 1 Newsletter: [Notion-Link]

Lokal: outputs/blogs/[slug]/

Status: Blog "Erstellung abgeschlossen" — bereit für WP-Import.
        Stories/Karussell/Reel: "Idee" — Patricia validiert + plant.
        Newsletter: "Erstellung abgeschlossen" — bereit für AC-Import.

Nächste Schritte (optional):
  • /wp Push-Blog → WordPress-Draft
  • /story-Skill mit Story-Idee 1 starten
  • Karussell mit /karussell-Skill ausarbeiten
```

**Plus optional:** Direkt-Push zu WordPress als Draft via `/wp` Skill (wenn User wünscht).

---

## Aktualisierungs-Modus (`/blog aktualisieren <slug>`)

Bei bestehendem Blog der älter als 6 Monate ist oder schlecht performt:

1. **WordPress-Read:** Lade aktuellen Blog via `/wp`-Skill
2. **SEO-Audit:**
   - Keyword-Aktualität checken
   - Title/Description-Optimierung
   - FAQ-Sektion fehlt? → ergänzen
   - TL;DR-Box fehlt? → ergänzen
   - Internal Links zu neuen Posts → ergänzen
   - Daten/Statistiken aktualisieren
3. **Patricia-Check:** Was ist heute anders als bei Original-Erstellung?
4. **Update-Diff zeigen:** Was wird geändert + Begründung
5. **Push to WordPress:** als Draft, Patricia approved.

---

## Anti-Halluzinations-Härtung

**ABSOLUT KRITISCH** (Patricia hat das mehrfach betont):

Verboten:
- ❌ Erfundene Statistiken („87% der Mütter berichten...")
- ❌ Erfundene Quellen
- ❌ Erfundene Patricia-Zahlen (nur aus Patricia-Input oder patricia-expertise.md)
- ❌ Generische Klischees ohne konkreten Anker

Pflicht:
- ✅ JEDE Zahl wortgenau aus Quellen
- ✅ Bei Unsicherheit: schreib es OHNE Zahl
- ✅ Patricia's Geschichten aus ihrer Voice-Notiz wortgenau übernehmen

---

## Beispiel-Lauf (Mai 2026)

**User:** `/blog`

**Bot lädt:**
- Monatsplan Mai 2026 → Gross-Fokus = Mama-CEO
- Active-Funnels „mama-ceo" (existiert nicht — siehe TODO)
- Patricia-Vollprofil

**Bot fragt:**
> 📝 Blog-Briefing Mai 2026
> 
> Monats-Gross-Produkt: **Mama-CEO Signature Programm**
> Vorgeschlagenes Thema: „Wie du als Mama dein Business strukturierst — ohne 60-Stunden-Wochen"
> 
> Frage 1: passt das Thema?
> Frage 2: Welche Story aus dem Mai willst du einbauen?
> Frage 3: Was ist dein Kunden-Pain?
> Frage 4: Konkrete Zahl/Erlebnis das du beisteuerst?

**Patricia antwortet via Voice/Text** → Bot transkribiert → Bot baut Blog.

**Output (lokal):**
```
outputs/blogs/2026-05-04-mama-business-2-stunden-tag/
├── blog.md  (1850 Wörter, SEO-optimiert)
├── cascade.md  (Stories + Karussell + Reel + Newsletter)
├── seo-meta.json
├── _briefing.md
└── images-todo.md
```

**Patricia kann dann:**
1. Blog in WordPress importieren (manuell oder via `/wp`-Skill)
2. Stories/Karussell/Reel/Newsletter-Snippets in den Wochen-Content-Pipeline einspeisen
3. Cockpit nutzt Blog-Hooks für die Story-Briefings der KW1

---

## Verlinkte Skills

- **`/wp`** — Push Blog als Draft zu WordPress
- **`/story`** — Story-Hooks aus Cascade nutzen
- **`/karussell`** — Karussell-Konzept aus Cascade
- **`/reels`** — Reel-Briefing aus Cascade
- **`/montag`** — Wochen-Content-Session nutzt Blog-Cascade als Quelle (KW1 nach Blog-Day)
- **`/funnel`** — wenn Blog auf Funnel verweist, Funnel-Daten ergänzen
