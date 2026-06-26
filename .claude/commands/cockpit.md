---
description: Tägliches Morgenbriefing + Wochen/Monats/Quartals-Strategie-Sicht. Orchestriert /blog, /story, /karussell, /reels, /produkt, /funnel.
argument-hint: [heute|woche|monat|quartal]
---

# /cockpit — Patricias Planungs-Orchester

**Patricia-Zitat:** „Grobe Planung mit einem Bot — Detailplanung mit den Spezial-Skills."

Cockpit ist KEIN neuer Mega-Skill der alles selber macht. Cockpit ist ein **Dirigent**:
- Liest Patricias Notion-System (Tagesplaner, Wochenplan, Monatsplan, Ziele, Aufgaben)
- Erstellt strukturierte Briefings (Tag/Woche/Monat/Quartal)

---

## 🚨 PFLICHT: Keine Stakkato-Sätze (Brand-Voice-Override)

Patricia hat MEHRFACH angemahnt — gilt für JEDEN Cockpit-Output (Morgenbriefing, Wochenblick, Monatssicht). Bei aller Listen-Struktur des Cockpits müssen Fliesstexte (Reflexionen, Empfehlungen, „warum heute X zählt"-Begründungen) trotzdem flüssig wie ein Gespräch klingen. Siehe `feedback_KRITISCH-keine-stakkato-saetze.md`.

❌ FALSCH: „Du hast 3 Termine. Du hast 2 Posts. Du hast eine Story-Lücke."
✅ RICHTIG: „Du hast heute drei Termine und musst zwischendurch noch zwei Posts freigeben — plus deine Story ist heute Vormittag noch leer."

**Regeln:**
- NIE drei abgehackte Subject-Verb-Punkt-Sätze hintereinander in Reflexions-/Empfehlungs-Absätzen
- Konjunktionen verbinden („und da", „weil", „aber", „bis")
- Reine Aufgabe-Listen (Bullet Points, Tabellen) dürfen kurz und stakkato sein — das sind Listen, keine Statements
- Schweizer ss durchgängig

---
- Schickt Patricia bei Bedarf zu den Spezial-Skills (`/blog`, `/story`, `/karussell`, `/reels`, `/produkt`, `/funnel`, `/salespage`, `/wp`)

---

## Pflicht-Lese-Liste (IMMER vor Generierung)

```
1. context/notion-business-brain.md           (System-Architektur — wo was liegt)
2. context/brand-voice.md                      (Patricia's Tonalität für Briefings)
3. context/active-funnels.json                 (welche Funnels aktiv)
4. context/patricia-vollprofil.md              (Brand-Voice + Verbote)
```

Plus IMMER aktuelle Notion-Reads (siehe Modi unten).

---

## Modus-Erkennung

User-Input nach `/cockpit` analysieren:

| Eingabe | Modus | Wann nutzen |
|---|---|---|
| `/cockpit` (leer) | heute (Default) | Morgens, Tagesübersicht |
| `/cockpit heute` | Tagesblick | Morgens 06:30, beim Start |
| `/cockpit woche` | Wochenblick | Sonntag-Abend / Montag-Morgen |
| `/cockpit monat` | Monatsblick | 1. d. Monats |
| `/cockpit quartal` | Quartalsblick | 1.4. / 1.7. / 1.10. / 1.1. |

---

## MODUS: HEUTE — Morgenbriefing

### Phase 1 — Notion-Reads (parallel wo möglich)

```
A) Wochenstruktur-Page (3587078e-8b7e-815c-abeb-d1259b8e9794)
   → Welcher Tag = welches Profil? Welcher Hauptbrocken?
   → Tagesstruktur-Schema

B) Aktuelle Wochenplanung (KW = isocalendar(heute).week)
   → Wochen-Hauptprodukt (Relation zu Produkte-DB)
   → Sales-Pattern (Text)
   → Fokus der Woche
   
C) Aktueller Monatsplan (Monat von heute)
   → 3-Produkte-Trio (Gratis/Mini/Gross)
   → Begründung Fokus
   → 3 Monatsziele
   
D) Aufgaben-DB (Filter)
   → Status: Aktiv / Termin / Geplant
   → Datum: heute oder überfällig
   → Sortiert nach Priorität (Prio 1 zuerst)
   
E) Aufgaben-DB Vorlagen (für Profil heute)
   → Status: Vorlage
   → Filter z.B. Anmerkung enthält „doTERRA" wenn Di
   → Diese in Tagesplan kopieren
   
F) Ziele-DB
   → Aktive Habit Goals (täglich-Reminder)
   → Aktives Q-Ziel des aktuellen Quartals
```

### Phase 2 — Tagesplan zusammenstellen

**Format des Outputs:**

```markdown
🌅 [Wochentag] [DD.MM.YYYY] · KW [WW] · [Profil-Heute]

═══════════════════════════════════════
DIESE WOCHE
═══════════════════════════════════════

🎯 Wochen-Hauptprodukt:  [Name aus Notion]
📅 Sales-Pattern:        [Pattern-Text]
🏔️ Monats-Trio:
   🎁 Gratis: [Name]
   💸 Mini:   [Name]
   👑 Gross:  [Name]

═══════════════════════════════════════
HEUTE
═══════════════════════════════════════

🎭 Profil:        [Mentoring / doTERRA]
🟦 Hauptbrocken:  [aus Hauptbrocken-Rotation]
                  Mo: Wochen-Content (/montag) ODER Blog-Day (1. Mo)
                  Di: doTERRA (Reaktivierung + Lifestyle)
                  Mi: Business-Struktur (Bot/System)
                  Do: Produktentwicklung
                  Fr: Newsletter + Weiterbildung
🔁 Habit-Goals:   [aus Ziele-DB Habits aktiv]

═══════════════════════════════════════
TAGESBLOCK (3,5h, Mo-Fr 08:00-11:30)
═══════════════════════════════════════

08:00–08:15   📋 Tageshebel-Briefing (das hier lesen)
08:15–10:00   🟦 [Hauptbrocken-Aktion]
10:00–10:30   📱 Story rendern (mit /story-Bot, ~15-20 Min)
10:30–11:30   👤 Kundenarbeit: DMs + Mails + 1 Outreach

═══════════════════════════════════════
TOP 3 HEBEL HEUTE (nach Money-Making-First-Filter)
═══════════════════════════════════════

🟢 MONEY-MAKING (direkt verkaufsrelevant in <14 Tagen)
   • [Hebel mit konkreter Action] — erwartet: [DM-Antwort/Verkauf/Anmeldung]

🟡 BUILDING (Hebel mit Output in 4-12 Wochen)
   • [Hebel] — erwartet: [strategischer Wert]

⚪ ABLENKUNG-RISIKO (Patricia bewusst entscheiden ob heute)
   • [Aufgabe die nett wäre aber nicht 40k-Hebel ist]

**Julia-Filter:** Bei jeder Aktivität fragen: 
„Dient das meinem 40k-Ziel oder beschäftigt es mich nur?"

═══════════════════════════════════════
TASKS aus AUFGABEN-DB
═══════════════════════════════════════

🔴 Prio 1 (heute fällig oder überfällig):
   • [Task] — [Datum]
   • [Task]

🟡 Prio 2:
   • [Task]

🔁 Vorlagen-Tasks (recurring für heute):
   • [Vorlage 1]
   • [Vorlage 2]

═══════════════════════════════════════
SCHUTZ-ZEITEN
═══════════════════════════════════════

✋ NICHT heute:
   • [3 Sachen die ablenken würden]

💪 WENN NUR 2H ZEIT:
   [Der EINE Hebel der den Tag rettet]

🛏️ AUSZEIT:
   • Nachmittag ab 11:30 — Familie/Kids
   • [Falls Di] Nachmittag = AUSZEIT (Sauna, Frühstück, Freundinnen)

═══════════════════════════════════════
SKILL-TIPP
═══════════════════════════════════════

Heute brauchst du wahrscheinlich:
  → /[skill] — [Begründung warum heute relevant]
  → /[skill] — [Begründung]
```

### Phase 3 — Tagesplaner-Eintrag in Notion erstellen/updaten

**Tagesplaner-DB:** `2ae7078e-8b7e-8102-a640-c046d70a2ae7`
**Data-Source:** `2ae7078e-8b7e-812e-b9d0-000bedb4dcd3`

```
1. Search nach existierender Page mit Datum=heute
2. Falls vorhanden: update_page
   Falls nicht: create_pages mit Template
3. Setze:
   - Tag: "[DD.MM.YYYY] - [Wochentag]"
   - Datum: heute
   - Tagesfokus: [Hauptbrocken + Top-1-Hebel kombiniert]
   - Tag geplant: __YES__
```

### Phase 4 — Output an Patricia

Markdown-Briefing (oben) PLUS Hinweis:
```
📌 Tagesplaner in Notion erstellt: [Link]
🔄 Wenn was anders kommen soll: einfach mir sagen
```

---

## MODUS: WOCHE — Wochenblick

### Wann nutzen
- Sonntag-Abend (Vorschau auf nächste Woche)
- Montag-Morgen (Reflexion + Planung)
- Wenn Patricia tippt `/cockpit woche`

### Phase 1 — Reflexion letzte Woche (= eingebauter Performance-Check)

Notion-Reads:
```
A) Wochenplanung VORLETZTE Woche (KW-1)
   → Erfolge / Herausforderungen aus Wochenvorlage-Reflexion-Sektion
B) Tagesplaner-DB Einträge der letzten 7 Tage
   → "Wie war der Tag?" Sterne-Bewertung Durchschnitt
   → Pattern: an welchen Tagen Stories gemacht / nicht?
C) Aufgaben-DB
   → Was wurde abgeschlossen letzte Woche?
   → Was hängt in „Wartend"?
   → Überfällige Tasks?
D) Reichweiten-Tracking + Kennzahlen-monatlich
   → Aktuelle Stand vs. letzter Monat (Tendenz)
E) Content-Management-DB Performance der letzten 7 Tage
   → Top-Performer (Bewertung 4-5⭐) → was hat funktioniert?
   → Flops (Bewertung 1-2⭐ oder leer) → was nicht?
   → Pillar-Verteilung: welche Säule unterperformt?
F) ActiveCampaign-Daten (via MCP `mcp__activecampaign__*` — Katalog: reference/activecampaign-mcp-tools.md)
   → Newsletter-Öffnungsrate letzte Woche (analyze_campaigns / get_campaign_report)
   → Lead-Wachstum (list_lists Abonnenten-Zahl, find_inactive_contacts)
```

**Erkenntnis-Block (Performance-Hypothesen):**
Aus den Daten zieht Cockpit aktiv 3 Hypothesen:
1. „Was hat letzte Woche funktioniert?" (Pattern aus Top-Performern)
2. „Was hat NICHT funktioniert?" (Patterns aus Flops + Tag-Bewertungen unter 3⭐)
3. „Eine konkrete Hypothese für nächste Woche" (was ändern, was wiederholen)

**Julia-Filter:** „Eigenverantwortung als Befreiung" — bei jedem Flop nicht „Algorithmus schuld" sondern „Was an meinem Content / Hook / Angebot hat nicht funktioniert?"

### Phase 2 — Vorschau nächste Woche

```
A) Wochenplanung NÄCHSTE Woche (KW+1)
   → Falls existiert: lesen
   → Falls nicht: BUILD vorschlagen via /montag-Skill
B) Wochen-Hauptprodukt (aus KW+1-Plan oder Monatsplan-Logik abgeleitet)
C) Vorlagen-Aufgaben aus Aufgaben-DB
   → kopiere in nächste Woche pro Tag verteilt
```

### Output-Format

```markdown
📅 WOCHENBLICK · KW [WW]

═══════════════════════════════════════
RÜCKBLICK KW [WW-1]
═══════════════════════════════════════

✅ Erfolge:
   • [Aus Wochenplanung Reflexion]

⚠️ Herausforderungen:
   • [Aus Wochenplanung Reflexion]

📊 Tag-Bewertung Ø: ⭐⭐⭐⭐ (4.2/5)
🎯 Tasks abgeschlossen: 12 / 18 geplant
📈 Reichweite: +X Follower / +X Newsletter / Tendenz: ↑↓

═══════════════════════════════════════
VORSCHAU KW [WW+1] (oder AKTUELL)
═══════════════════════════════════════

🎯 Wochen-Hauptprodukt:  [Name]
📅 Sales-Pattern:        [Pattern]

🟦 TAGES-PLAN
   Mo: Wochen-Content / Blog (1. Mo) — Brocken: [...]
   Di: doTERRA — Phase [1/2/3] — Brocken: [...]
   Mi: Business-Struktur — Brocken: [...]
   Do: Produktentwicklung — Brocken: [...]
   Fr: Newsletter + Weiterbildung — Brocken: [...]
   Sa+So: FREI

═══════════════════════════════════════
3 HEBEL DIESER WOCHE
═══════════════════════════════════════

1. [Strategischer Hebel mit konkretem Output]
2. [Hebel]
3. [Hebel]

═══════════════════════════════════════
RECURRING-TASKS (aus Vorlagen)
═══════════════════════════════════════

[Liste der Vorlagen-Aufgaben verteilt auf Tage]

═══════════════════════════════════════
WARNUNGEN
═══════════════════════════════════════

⚠️ Aufholbedarf:
   • [Überfällige Tasks aus letzter Woche]
   • [Vernachlässigte Säulen]

🎯 Quartalsziel-Status:
   • [Q-Ziel] — Status auf Track / Risiko

═══════════════════════════════════════
NÄCHSTE SCHRITTE
═══════════════════════════════════════

Optional weitere Skills nutzen:
  → /montag — Wochen-Content-Session
  → [andere Skills basierend auf Hauptbrocken-Rotation]
```

### Notion-Update Wochenblick

Bot updatet Wochenplanung-Page (KW+1):
- Setzt „Erfolge letzte Woche" / „Herausforderung letzte Woche" aus Reflexion
- Falls Wochen-Hauptprodukt leer → Vorschlag aus Monatsplan-Trio

---

## MODUS: MONAT — Monatsblick

### Wann nutzen
- 1. d. Monats (Monatswechsel)
- Wenn Patricia tippt `/cockpit monat`

### Phase 1 — Reflexion letzten Monat

Notion-Reads:
```
A) Monatsplan VORMONAT
   → 3 Monatsziele: was wurde erreicht?
   → Erkenntnis Kennzahlen-Analyse / Content-Analyse
B) Kennzahlen-monatlich Vormonat
   → Umsatz vs. Vor-Vormonat
   → Gewinn / Marge
C) Reichweiten-Tracking Vormonat
   → Newsletter / Instagram / Website Veränderungen
D) Content-Management-DB
   → Top-Performer letzter Monat (Bewertung 4-5⭐)
   → Was nicht funktioniert hat
E) Aufgaben-DB
   → Letzten-Monats-Erledigt-Quote
```

### Phase 2 — Vorschau aktueller Monat

```
A) Monatsplan AKTUELL
   → 3-Produkte-Trio (Gratis/Mini/Gross)
   → Begründung Fokus
   → 3 Monatsziele
B) Jahresplanung-Aktivitäten dieses Monats
   → Aktive Phasen (z.B. doTERRA Phase 1, Mama-CEO Launch)
C) Quartalsziele Status (für Q-Quarter dieses Monats)
```

### Output-Format

```markdown
🏔️ MONATSBLICK · [MONAT YYYY]

═══════════════════════════════════════
RÜCKBLICK [VORMONAT]
═══════════════════════════════════════

🎯 3 Monatsziele — Status:
   1. [Ziel] — ✅ Erreicht / ⚠️ Teilweise / ❌ Nicht
   2. ...
   3. ...

💰 Umsatz: CHF XXX (Vormonat: CHF XXX, Tendenz: ↑↓)
📊 Marge: XX% 
🌱 doTERRA-Income: CHF XXX

📈 Reichweite-Δ (im Monat):
   • Newsletter: +/- X
   • Instagram Mentoring: +/- X Follower
   • Instagram doTERRA: +/- X Follower
   • Website-Besucher: X

🏆 Top-Performer-Content (Bewertung 4-5⭐):
   • [Content-Titel] — [Plattform] — [Reach]
   • ...

═══════════════════════════════════════
AKTUELLER MONAT [MONAT YYYY]
═══════════════════════════════════════

🎁 Gratis-Fokus: [Name]
💸 Mini-Fokus:   [Name]
👑 Gross-Fokus:  [Name]

✏️ Begründung Fokus:
[Text aus Monatsplan]

🎯 3 Monatsziele:
1. [Ziel]
2. [Ziel]
3. [Ziel]

═══════════════════════════════════════
PHASEN AKTIV (aus Jahresplanung)
═══════════════════════════════════════

[Liste der Aktivitäten mit Status=doTERRa/Mum Life Balance dieser Monat]

═══════════════════════════════════════
QUARTALSZIEL-STATUS
═══════════════════════════════════════

Q[X] [YYYY]:
   • [Q-Ziel] — Tendenz: 🟢 / 🟡 / 🔴
   • [Q-Ziel] — ...

═══════════════════════════════════════
NÄCHSTE SCHRITTE
═══════════════════════════════════════

Pflicht-Tasks für Anfang Monats:
  → Monatsplan-Vorlage Sektionen 1-6 durchgehen
  → /blog-Skill für Monatsthema starten (1. Mo)
  → Mediathek aufräumen
  → Cover-Bild für Monatsplan auswählen
```

---

## MODUS: QUARTAL — Quartalsblick

### Wann nutzen
- 1.4. / 1.7. / 1.10. / 1.1. (Quartalswechsel)
- Wenn Patricia tippt `/cockpit quartal`

### Phase 1 — Reflexion letztes Quartal

```
A) Ziele-DB
   → Q-Ziele letztes Quartal Status
   → Erreicht / Nicht erreicht
B) Jahresplanung
   → Aktivitäten letztes Quartal: was lief?
C) Kennzahlen-Aggregat über 3 Monate
   → Umsatz-Total Quartal vs. Q-1
   → 40k-Ziel-Stand: X% des Jahres
D) Long-Term-Goals Drift
   → Auf Track oder Korrektur nötig?
```

### Phase 2 — Plan kommendes Quartal

```
A) Q-Ziele-DB für nächstes Quartal
   → Falls noch nicht definiert: VORSCHLAG basierend auf Long-Term + Phasen
B) Jahresplanung für nächstes Quartal
   → Welche Aktivitäten geplant?
   → Lücken: was fehlt?
C) Themenplanung übernächster Monat
   → Gross-Produkt-Vorschau
```

### Output-Format

```markdown
🌅 QUARTALSBLICK · Q[X] YYYY

═══════════════════════════════════════
RÜCKBLICK Q[X-1] [YYYY]
═══════════════════════════════════════

🎯 Q[X-1] Ziele — Status:
   • [Ziel] — ✅ / ⚠️ / ❌
   • [Ziel] — ...

💰 Q[X-1] Umsatz-Aggregat: CHF XXX
   → 40k-Jahresziel-Stand: XX% (Sollte sein: 25/50/75/100%)

🏔️ Q[X-1] Aktivitäten Bilanz:
   • [Phase Name] — abgeschlossen / verschoben
   • ...

═══════════════════════════════════════
PLANUNG Q[X] [YYYY]
═══════════════════════════════════════

🎯 Q[X] Ziele (aus Ziele-DB):
   • [Ziel]
   • [Ziel]

🏔️ Q[X] Aktivitäten (aus Jahresplanung):
   • [Aktivität] — Zeitraum X-Y
   • ...

📅 Pro-Monats-Trio Vorschau:
   • [Monat 1]: Trio = ...
   • [Monat 2]: Trio = ...
   • [Monat 3]: Trio = ...

═══════════════════════════════════════
LONG-TERM-CHECK
═══════════════════════════════════════

🏆 Long-Term-Goals Status:
   • [Goal] — auf Track / Korrektur nötig
   • ...

═══════════════════════════════════════
STRATEGISCHE FRAGEN
═══════════════════════════════════════

Anregungen für Reflexion (Patricia beantwortet selbst):
  • Was hat das letzte Quartal mehr gebracht als erwartet?
  • Was hätte ich rückblickend anders priorisiert?
  • Welcher 1 Hebel würde Q[X] zum Erfolgsquartal machen?

═══════════════════════════════════════
NÄCHSTE SCHRITTE
═══════════════════════════════════════

  → Q-Ziele in Ziele-DB anlegen wenn noch nicht da
  → Jahresplanung-Aktivitäten ergänzen
  → /produkt für neues Produkt im Quartal
```

---

## Verlinkte Skills (Cockpit dirigiert dorthin)

```
🟦 /blog        — 1× pro Monat (1. Mo) Blog zum Monatsthema
📱 /story       — täglicher Story-Workflow
🎨 /karussell   — Karussell-Erstellung
🎬 /reels       — Reel-Briefing
📋 /montag      — Wochen-Content-Session
🛠️ /produkt    — Produktentwicklung (Hauptbrocken Do)
📊 /funnel      — Funnel-Strategie
💰 /salespage   — Sales-Pages
🌐 /wp          — WordPress-Push
```

Cockpit empfiehlt im Output welche Skills heute relevant sind — Patricia entscheidet welche sie startet.

---

## Anti-Halluzinations-Härtung

**ABSOLUT:** Keine erfundenen Zahlen.
- Reichweiten / Umsätze NUR aus Notion-Reads
- Bei fehlenden Daten: explizit „(noch nicht in Notion getrackt)" schreiben
- Tasks NUR aus Aufgaben-DB lesen, nicht selber erfinden
- Wenn Wochenplan / Monatsplan leer: Patricia fragen statt raten

---

## Ausnahme-Regel: Override aktiv

Wenn `/fokus`-Override gesetzt ist (siehe story-render-bot state.py):
→ Cockpit RESPEKTIERT den Override
→ Statt Wochenplan-Hauptprodukt aus Notion: Override-Thema nutzen
→ Sales-Pattern aus Override ableiten

---

## Best Practice für Patricia

**Morgens 06:30 (Mo-Fr):**
1. Claude Code öffnen
2. `/cockpit` tippen
3. Briefing lesen (~2 Min)
4. Tagesplaner ist automatisch in Notion eingerichtet
5. Top-1-Hebel anpacken im Deep-Work-Slot

**Sonntag-Abend:**
1. `/cockpit woche` → Vorschau nächste Woche
2. Falls Wochenplan leer: füllen oder /montag-Skill triggern

**1. d. Monats:**
1. `/cockpit monat` → strategische Sicht
2. Monatsplan-Vorlage in Notion durchgehen
3. /blog-Skill für Monatsthema starten

**1. d. Quartals (1.4./1.7./1.10./1.1.):**
1. `/cockpit quartal` → Long-Term-Check
2. Q-Ziele anlegen / aktualisieren
3. Jahresplanung-Aktivitäten review
