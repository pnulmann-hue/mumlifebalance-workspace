---
tags: [notion, business]
---

# Notion Business Brain — Master-Dokumentation

**Pflicht-Lese-Datei für alle Skills.** Beschreibt Patricias Notion-System,
welche DBs es gibt, wie sie zusammenhängen, welche Vorlagen genutzt werden.

**Stand:** 2026-05-02 · Erste Inventur (PLANUNG-Bereich vollständig, andere
Bereiche kommen in Folgesessions).

---

## Bereichs-Architektur (5 Cluster)

Patricias Business Brain ist in **5 Cluster** organisiert. Skills MÜSSEN diese
Cluster respektieren statt eigene Strukturen aufzubauen.

```
🗂️ ORGANISATION       Aufgaben · Mediathek · Kunden · Arbeitsbereiche ·
                       Wissensbereiche · Wirkbereiche
📅 PLANUNG             Ziele · Tagesplaner · Wochenplanung ·
                       Monatsplanung · Jahresplanung
🎁 PRODUKTE            Produkte · doTERRA Produkte · Material ·
                       Testimonials · Email-Vorlagen
📱 CONTENT MARKETING   Content-Plattformen · Content-Strategie ·
                       Content-Management
📈 UNTERNEHMEN         Reichweiten Tracking · Kostenpositionen ·
                       Kennzahlen monatlich · Branding
```

---

## PLANUNGS-HIERARCHIE (das Skelett)

Patricias Planung ist eine **5-Stufen-Hierarchie** vom Long-Term zum Tag.
Jeder Skill der Aktivitäten plant, MUSS in dieser Hierarchie denken.

```
┌─ JAHR  ────────────────────────── Jahresplanung
│                                   („Aktivität" pro Zeitraum, mit Status)
│
├─ QUARTAL  ────────────────────── Ziele (Quartals-Ziele Q1–Q4)
│                                   (Quartalsweise gegen Long-Term)
│
├─ MONAT  ──────────────────────── Monatsplanung
│                                   (3 Monatsziele + 3-Produkte-Treppe)
│
├─ WOCHE  ──────────────────────── Wochenplanung
│                                   (Wochen-Hauptprodukt + 5 Business-Säulen)
│
└─ TAG  ────────────────────────── Tagesplaner
                                    (Tagesfokus + Routinen + Reflexion)
```

### Hierarchie-Logik

- **Long-Term-Ziele** definieren wo Patricia in 2026/2027 stehen will
- **Quartalsziele** brechen das in 3-Monats-Zyklen
- **Monatsplan** picks 3 Monatsziele + Produkt-Trio (Gratis/Mini/Gross)
- **Wochenplan** definiert Wochen-Hauptprodukt + Säulen-Verteilung
- **Tagesplan** hat den Tagesfokus + Routinen + Reflexion am Abend

---

## DB-Inventur · Bereich PLANUNG

### 📅 Jahresplanung Mum Life Balance

**ID:** `2ae7078e-8b7e-81d9-b5e1-c6bea76ac287`
**Data-Source:** `2ae7078e-8b7e-81f9-adb5-000bb877b193`
**Zweck:** Aktivitäten-Liste übers Jahr (nicht Strategie-Page, sondern Tracking-Liste).

**Properties:**
| Property | Typ | Werte |
|---|---|---|
| Aktivität | Title | „Mama-CEO Launch" / „doTERRA-Onboarding" |
| Zeitraum | Date-Range | wann passiert es |
| Status | Select | Ferien / doTERRa / Mum Life Balance |
| Preisformat | Select | Mini / Mittel / Hochpreisig / 0€ |
| Privat | Checkbox | privates vs business |
| Produkte | Relation | → Produkte-DB |
| Ziele | Relation | → Ziele-DB |

**Views:**
- Default (gefiltert auf Mum Life Balance + Ferien)
- Zeitstrahl (Timeline-Ansicht)
- Abgeschlossen

**Nutzung durch Skills:**
- `/cockpit` Quartal-Modus liest hier alle Aktivitäten der nächsten 3 Monate
- `/produkt` Skill verlinkt neue Produkte mit Jahresplanungs-Aktivitäten

### 🎯 Ziele

**ID:** `2ae7078e-8b7e-815a-a344-f98a4e3d91b3`
**Data-Source:** `2ae7078e-8b7e-81cd-afc9-000b77bd9ff3`
**Zweck:** Zentrale Ziele-DB, hierarchisch organisiert.

**Properties:**
| Property | Typ | Werte |
|---|---|---|
| Name | Title | „CHF 40'000 Jahresumsatz" |
| Art des Ziels | Select | Long-term Goal / Habit Goal / Achievment Goal |
| Status | Select | Aktiv / Zurückgestellt / Erreicht |
| Jahr | Select | 2024–2028 |
| Quartal | Select | Q1–Q4 (optional, leer = Long-term) |
| Qualitatives Ziel | Text | Beschreibung |
| Quantitatives Ziel | Text | Messbare Zahl |
| Datum (erreicht) | Date | wann tatsächlich erreicht |
| Arbeitsbereich | Relation | → Arbeitsbereiche-DB |
| Produkt verknüpfen | Relation | → Produkte-DB |
| Jahresplanung | Relation | → Jahresplanung-DB |
| Projekte | Relation | → Projekte-DB |

**Views (wichtig für Skills):**
- **Aktive Ziele** (Default, gefiltert nach Status=Aktiv)
- **Q-Ziele aktiv** (Board, gruppiert nach Quartal)
- **Long term** (Board, gruppiert nach Jahr, ohne Quartal-Zuordnung)
- **Erreicht** + **Zurückgestellt** (Archive-Views)

**Hierarchie-Regel:**
1. Long-Term-Ziele = Jahr gesetzt, Quartal LEER
2. Quartals-Ziele = Jahr + Quartal gesetzt
3. Habit Goals = recurring (z.B. „1× / Monat Reflexion")

**Nutzung durch Skills:**
- `/cockpit` Quartal-Modus liest aktive Q-Ziele dieses Quartals
- `/cockpit` Monatsblick prüft welche Q-Ziele in diesem Monat angegangen werden müssen
- Bei jeder Story/Karussell-Generation sollte Bot wissen welche Long-Term-Ziele dahinterstehen

### 📅 Monatsplanung

**ID:** `2ae7078e-8b7e-81d9-b5e1-c6bea76ac287` (DB) / `2ae7078e-8b7e-8171-a760-c233083c26b6` (Page-Container)
**Data-Source:** `2ae7078e-8b7e-81fc-acf7-000be291c92c`

**Properties (erweitert 2026-05-02):**
| Property | Typ |
|---|---|
| Monat + Jahr | Title |
| Zeitraum | Date-Range |
| 3 Monatsziele | Text |
| 🎁 Gratis-Fokus | Relation → Produkte |
| 💸 Mini-Fokus | Relation → Produkte |
| 👑 Gross-Fokus | Relation → Produkte |
| ✏️ Begründung Fokus | Text |
| Erkenntnis Kennzahlen-Analyse | Text (Vormonats-Daten) |
| Erkenntnisse Content-Analyse | Text (Vormonats-Daten) |
| Learnings aus dem letzten Monat | Text |
| Finanz check-up | Checkbox |
| Regelmäßige Aufgaben geplant | Checkbox |

**Vorlage Monatsplanung** (`2ae7078e-8b7e-81e8-9e5f-c912e9c8d4b5`):

Die Vorlage hat **6 strukturierte Sektionen**, die jeden Monat abgearbeitet werden:

```
1. 🪞 REFLEXION DES LETZTEN MONATS
   - Was waren deine Erfolge?
   - Was waren deine Herausforderungen?
   - Größtes Learning oben eintragen

2. 📊 ANALYSEN & KENNZAHLEN
   - Online Business Kennzahlen (Umsatz / Kosten / Gewinn)
   - Reichweiten Tracking (Newsletter / Instagram / Website / YouTube / Podcast)
   - Content-Analyse (was funktioniert / was nicht)
   - Persönlicher Finanz-Check-Up (Cashflow, Budget, ausstehende Zahlungen)

3. 🎯 ÜBERBLICK & ZIELE
   - Überblick mit Jahresplanung
   - Quartalsziele anschauen
   - Top 3 Monatsziele definieren

4. 📂 PROJEKTPLANUNG
   - Hat jedes aktive Projekt mind. 1 aktive Aufgabe?

5. 🔁 REGELMÄSSIGE AUFGABEN
   - Recurring Tasks für den Monat erstellen
   - Nächste Monats- + 4 Wochenplanungen vorbereiten

6. 📱 CONTENT-PLANUNG (für übernächsten Monat)
   - Plattformen + Frequenz
   - Themenplanung („Welches Produkt im Fokus?")
   - Ideen-Datenbank durchsehen
   - Redaktionsplan erstellen
```

**Skill-Integration:**
- `/cockpit` Monat-Modus führt Patricia durch diese 6 Sektionen
- `/montag` liest Sektion 6 (Content-Planung) für Wochen-Content
- Skills DÜRFEN NICHT eigene Monats-Strukturen aufbauen — sie pflegen die Vorlage

### 📅 Wochenplanung

**ID:** `2ae7078e-8b7e-81ef-a769-cdb1a6584c70` (DB)
**Data-Source:** `2ae7078e-8b7e-81e7-9083-000b01908eb5`

**Properties (erweitert 2026-05-02):**
| Property | Typ |
|---|---|
| Woche | Title (Datum-basiert, z.B. „4.–10. Mai 2026 (KW 19)") |
| Zeitraum | Date-Range |
| Fokus der Woche | Text (Free-Text) |
| 🎯 Wochen-Hauptprodukt | Relation → Produkte |
| 📅 Sales-Pattern | Text (welcher Tag was bewerben) |
| Erfolge letzte Woche | Text |
| Herausforderung letzte Woche | Text |
| Contentplanung | Checkbox |
| Mails check up | Checkbox |
| Downloadordner aufgeräumt | Checkbox |
| Internet Tabs geschlossen | Checkbox |

**Vorlage Wochenplanung** (`2ae7078e-8b7e-8121-8a9e-d178942cc1b7`):

```
1. 🪞 REFLEXION DER LETZTEN WOCHE
   - Tägliche Routinen + Learnings + Journaling-Übersicht
   - Erfolge / Herausforderungen → nach oben übertragen

2. 🎯 PLANUNG DER NÄCHSTEN WOCHE
   2.1 Fokus für die nächste Woche definieren
   2.2 Was planst du je Business-Säule?
       → 5 Säulen: Kundenarbeit · Produktentwicklung ·
                   Business-Struktur · Content-Creation · Weiterbildung
   2.3 Wochenplanung (Termine + Tasks aus Aufgaben-DB)
   2.4 Ausblick auf nächste 2 Wochen + Me-Time einplanen

3. 🧹 ORDNUNGSROUTINEN
   3.1 Allgemeine Ordnung (Downloads · Tabs · Mails · Notizen)
   3.2 Kundendaten aktualisieren
```

**5-Säulen-System (KRITISCH):**
Jede Woche wird Content + Aktivitäten in 5 Säulen organisiert:

| Säule | Was reinkommt |
|---|---|
| **Kundenarbeit** | 1:1-Coaching, DMs, Kunden-Onboarding |
| **Produktentwicklung** | Module aufnehmen, Salespages, neue Produkte |
| **Business-Struktur aufbauen** | Systeme, Automationen, Bots, WordPress |
| **Content-Creation** | Stories, Reels, Karussells, Newsletter |
| **Weiterbildung** | Kurse, Bücher, Podcasts |

**Skill-Integration:**
- `/cockpit` Tagesblick liest Wochen-Hauptprodukt + Sales-Pattern (heute schon implementiert)
- `/cockpit` Wochenblick führt Patricia durch die 5 Säulen + Reflexion
- `/montag` (existing skill) deckt Säule „Content-Creation" ab

### 📅 Tagesplaner

**ID:** `2ae7078e-8b7e-8102-a640-c046d70a2ae7`
**Data-Source:** `2ae7078e-8b7e-812e-b9d0-000bedb4dcd3`
**Zweck:** Eine Page pro Tag mit Tagesfokus + Routinen + Abend-Reflexion.

**Properties:**
| Property | Typ | Bedeutung |
|---|---|---|
| Tag | Title | „17.12.2025" |
| Datum | Date | |
| Tagesfokus | Text | DAS Hauptthema des Tages |
| Tag geplant | Checkbox | morgens als „erledigt" markieren |
| Story gemacht, Beitrag veröffentlicht | Checkbox | Content-Output |
| Blick auf Morgen | Checkbox | abends Vorschau gemacht |
| Wie war der Tag? | Select 1–5 ⭐ | Abend-Reflexion |
| Learning des Tages | Text | Tageslernen |
| Jornaling | Text | Freier Text |
| Sport Gymondo | Checkbox | persönliche Routine |
| EFT | Checkbox | persönliche Routine |
| Auraimpulse gelesen | Checkbox | persönliche Routine |
| Essensplanung 100gr Proteine | Checkbox | persönliche Routine |

**Skill-Integration:**
- `/cockpit` Morgen-Modus erstellt eine neue Tagesplaner-Page (oder updatet sie)
  - Setzt **Tagesfokus** automatisch aus Wochen-Hauptprodukt + Sales-Pattern
  - Setzt **Tag geplant** = ✅ nach Morgenbriefing
- `/cockpit` Abend-Modus (optional) hilft Patricia mit Reflexion + „Blick auf Morgen"

---

## Wochenstruktur (Default-Rhythmus)

Verknüpft mit der separaten Page **„Wochenstruktur Patricia 2026"**
(`3587078e-8b7e-815c-abeb-d1259b8e9794`).

```
Mo   08:00–11:30 Mentoring (3,5h)
Di   08:00–11:30 doTERRA (3,5h) | Nachmittag AUSZEIT
Mi   08:00–11:30 Mentoring (3,5h)
Do   08:00–11:30 Mentoring (3,5h)
Fr   08:00–11:30 Mentoring (3,5h) | Nachmittag Bonus-Slot
Sa+So FREI

Verteilung: 80% Mentoring (14h) / 20% doTERRA (3,5h)
```

**Vormittag-Schema (jeder Tag):**
```
08:00–08:15  Tageshebel klären
08:15–10:00  Deep-Work am Hauptbrocken
10:00–10:30  Story rendern (mit Content-Assistent)
10:30–11:30  Output: posten, DMs in 1 Block, Mails
```

---

## Skill-Regeln (für ALLE Bots)

### Pflicht beim Start jedes Skills
1. Lade **diese Datei** als Pflicht-Lese (in System-Prompt einbauen)
2. Lese ggf. spezifische DB-Schemata (bei größeren Aktionen)
3. Respektiere die Hierarchie: Tag → Woche → Monat → Quartal → Jahr

### Was Skills nie tun dürfen
- ❌ Eigene Monats-/Wochen-Strukturen aufbauen → IMMER die Vorlagen nutzen
- ❌ Bei Patricia konkrete Daten erfinden (Halluzinations-Verbot)
- ❌ Wochen-Hauptprodukt ignorieren → das definiert was diese Woche bewerben
- ❌ Profile vermischen am gleichen Tag (Mo+Mi+Do+Fr Mentoring, Di doTERRA)

### Was Skills proaktiv tun sollen
- ✅ Bei Story/Karussell/Reel-Gen: Wochen-Hauptprodukt + Sales-Pattern lesen
- ✅ Bei Tageshebel: Wochen-Säulen-Verteilung respektieren
- ✅ Bei Reflexionen: in Wochenplan/Monatsplan-Vorlage eintragen
- ✅ Tagesplaner-Eintrag jeden Morgen erstellen (durch Cockpit)

### 🔴 Pflicht: ALLE Content-Outputs in Notion ablegen

**Patricia-Regel:** „Der erarbeitete Inhalt ist auch immer in Notion abzulegen."

Jeder Skill der Content erzeugt (Blog, Story, Karussell, Reel, Newsletter, Podcast,
YouTube) MUSS einen Eintrag in der **Content-Management-DB** anlegen. Lokal in
`outputs/...` ist NUR Backup/Werkstatt — Notion ist Single Source of Truth.

**Content-Management-DB:**
- ID: `2ae7078e-8b7e-8134-9e36-f8c630a850f2`
- Data-Source: `2ae7078e-8b7e-811a-ad14-000ba5820c09`
- Hat **10 vorbereitete Templates** (Blogartikel, Story, Karussell, Reel, Newsletter, Einzelpost, Podcast, YouTube, Idee)

**Pflicht-Felder beim Anlegen:**
| Feld | Inhalt |
|---|---|
| Content-Titel | Hook / Headline |
| Content-Typ | Multi-Select aus Liste |
| Status | Idee / Geplant / Erstellung begonnen / Erstellung abgeschlossen / Veröffentlicht |
| Content-Säule | Relation → Content-Strategie-DB |
| Produkt Verknüpfung | Relation → Produkte-DB (Wochen-Hauptprodukt) |
| Käufertypen | Multi-Select aus Julia-Trost-Liste (Willi/Amelie/Ina/Zoe/Rudi/Frank) |
| Launch-Phase | Aufwärmphase / Secret Offer / Verkaufsphase / Nachkaufphase / Evergreen |
| Storyart (bei Story) | Persönliche Geschichte / Kunden-Transformation / Mythos-Brecher / etc. |
| Recycling Content | Self-Relation für Cascade-Verknüpfung (z.B. Story aus Blog) |
| Briefing-Link | URL zum lokalen `outputs/...`-Ordner |

**Cascade-Logik via Recycling-Relation:**

Wenn ein Skill mehrere Content-Outputs aus einer Quelle erzeugt (z.B. /blog
generiert Blog + 3 Stories + 1 Karussell + 1 Reel + 1 Newsletter):

1. Master-Eintrag (Blog) ZUERST anlegen
2. Cascade-Einträge mit `Recycling Content` → Relation zum Master
3. Patricia sieht in Notion auf einen Blick die ganze Pipeline

**Performance-Tracking:**

Nach Veröffentlichung wird der Eintrag um Performance-Daten ergänzt:
- Ansichten / Reichweite
- Gespeichert / Gefällt mir / Kommentare
- neue Follower
- Bewertung (1-5 ⭐)
- A N A L Y S E (Erkenntnis: was funktionierte)

→ Cockpit-Monatsblick + zukünftiger `/business-check`-Skill nutzen das für Trends.

---

## DB-Inventur · Bereich ORGANISATION

### 📋 Aufgaben

**ID:** `2ae7078e-8b7e-81bd-b07a-deaa99c01b71`
**Data-Source:** `2ae7078e-8b7e-81a2-a070-000b54019c80`
**Zweck:** Operative Aufgaben mit Hierarchie + Abhängigkeiten + Vorlagen für recurring Tasks.

**Properties:**
| Property | Typ | Werte |
|---|---|---|
| Aufgabe | Title | |
| Status | Select | Vorlage / Geplant / Aktiv / Wartend / Regelmäßig / Termin / Abgeschlossen |
| Priorität | Select | Quick Win / Prio 1 / Prio 2 / Prio 3 |
| Datum | Date+Time | wann fällig |
| Erledigt (für Projekte) | Checkbox | |
| Erledigt ✅ | Button | One-Click-Done |
| Überfällig? | Formula | auto |
| Anmerkung | Text | |
| Element (übergeordnet) | Relation (self) | Hierarchie |
| Element (untergeordnet) | Relation (self) | Hierarchie |
| Blockiert | Relation (self) | Abhängigkeiten |
| Blockiert von | Relation (self) | Abhängigkeiten |
| Arbeitsbereich | Relation | → Arbeitsbereiche |
| Projekte | Relation | → Projekte |
| Produkt | Relation | → Produkte |
| Kunden / Kontakte | Relation | → Kunden |
| Content Erstellung | Relation | → Content-Management |
| Notizen / Emails | Relations | → Notizen, Email-Vorlagen |
| Person | People | Assignee |

**Wichtig — Vorlagen-Workflow:**
Patricia hat **Vorlagen-Aufgaben** (Status = „Vorlage"). Diese werden in Wochenplanungen kopiert für recurring Tasks (z.B. „Mails check up", „Downloadordner aufräumen").

**Skill-Integration:**
- `/cockpit` Tagesblick listet Aufgaben mit Datum=heute, Status=Aktiv/Termin
- Cockpit-Wochenplanung kopiert Vorlagen-Aufgaben in die nächste Woche
- Skills die Tasks erstellen sollen: Status=„Geplant", Priorität setzen, Arbeitsbereich verknüpfen

### 🏠 Arbeitsbereiche

**ID:** `2ae7078e-8b7e-8150-addd-fd1e154456a8`
**Data-Source:** `2ae7078e-8b7e-819b-848d-000b097a63c2`
**Zweck:** Zentrale „Hub"-Vernetzung — bündelt Projekte, Notizen, Wiki, Mediathek, Ziele pro Lebens-/Business-Bereich.

**Properties:** Name (Title), Archiv, + Relations zu: Mediathek · Notizen · Projekte · Unternehmens-Wiki · Ziele

**Konzept:** Ein Arbeitsbereich (z.B. „Mum Life Balance Mentoring", „doTERRA", „Privat") ist die ÜBERGEORDNETE Kategorie für alles was darunter passiert. Tasks, Ziele, Projekte sind IMMER mit einem Arbeitsbereich verknüpft.

**Skill-Integration:**
- Profil-Switching im Cockpit basiert auf Arbeitsbereich (Mentoring vs doTERRA)
- Bei jeder Task-/Ziel-Erstellung soll Skill den Arbeitsbereich setzen

### 📚 Mediathek · Kunden und Kontakte · Wissensbereiche · Wirkbereiche

(Schema noch nicht detailliert — werden bei Bedarf gefetched)

| DB | ID | Zweck (vermutet) |
|---|---|---|
| Mediathek | `2ae7078e-8b7e-8141-b268-c45542881883` | Bilder, PDFs, Vorlagen-Speicher |
| Kunden und Kontakte | `2ae7078e-8b7e-811a-bc8c-c38eeff4b5ba` | CRM (Mentoring + doTERRA) |
| Wissensbereiche | `2ae7078e-8b7e-8186-b6be-cc523090355a` | Wissens-Tags |
| Wirkbereiche | `2b57078e-8b7e-80ef-a119-dfbf50a68311` | doTERRA Wirkbereiche (Gefäßsystem, Hormone, etc.) |

---

## DB-Inventur · Bereich CONTENT MARKETING

### 🎯 Content-Strategie

**ID:** `2ae7078e-8b7e-8146-8f10-ec4786130b13`
**Data-Source:** `2ae7078e-8b7e-81a3-9f5f-000be0dd8dbc`
**Zweck:** Definiert die Content-Säulen (Pillars) + Themenbereiche + Beitragsarten mit prozentualer Verteilung.

**Properties:**
| Property | Typ | Werte |
|---|---|---|
| Content Säule | Title | „Networkmarketing 2.0" / „Mama-CEO" |
| Typ | Select | **Content-Säule** / **Fester Themenbereich** / **Beitragsart** |
| Aktiv | Checkbox | aktuell aktiv ja/nein |
| Anteil | Number (Prozent) | wieviel % des Contents soll diese Säule sein |
| Anmerkung | Text | |
| Content-Management | Relation | → posts dazu |

**KRITISCH:** Das ist die **Content-Pillar-Definition**. Jede Story/Reel/Karussell sollte einer Säule zugeordnet werden. Skill müssen Anteils-Verteilung respektieren (z.B. 40% Säule X, 30% Säule Y, 30% Säule Z).

### 📱 Content-Plattformen

**ID:** `2ae7078e-8b7e-811c-9ba7-fe9503f0ecc2`
**Data-Source:** `2ae7078e-8b7e-8103-81e2-000b93a36fc7`
**Zweck:** Plattform-Liste mit Frequenz-Vorgabe (Instagram Mentoring, Instagram doTERRA, Facebook-Gruppe, Telegram-Gruppe).

(Schema noch nicht detailliert)

### 📝 Content-Management

**ID:** `2ae7078e-8b7e-8134-9e36-f8c630a850f2`
**Data-Source:** `2ae7078e-8b7e-811a-ad14-000ba5820c09`
**Zweck:** Was wurde gepostet — alle Posts mit Plattform, Säule, Performance.

**Skill-Integration:**
- Story-Bot prüft ob Hook in den letzten 14 Tagen schon kam
- Repost-Logik nutzt Best-Performer

(Schema teilweise dokumentiert in `notion-content-db.md`)

---

## DB-Inventur · Bereich UNTERNEHMEN

### 📈 Reichweiten Tracking

**ID:** `2ae7078e-8b7e-81ef-87d3-cd86c9be558b`
**Data-Source:** `2ae7078e-8b7e-81d2-8f7b-000b8f6a7d08`
**Zweck:** Monatliche KPIs aller Reichweiten-Kanäle.

**Properties:**
| Metrik | Typ |
|---|---|
| Monat & Jahr | Title |
| Zeitraum | Date |
| Newsletter Abonnenten | Number |
| Gesendete Newsletter | Number |
| Öffnungsrate Newsletter | % (Ring) |
| Instagram Follower | Number |
| Instagram erreichte Konten | Number |
| Instagram Interaktionen | Number |
| Website Besucher | Number |
| doTERRA Neukunden | Number |
| doTERRA Botschafterinnen | Number |

**Skill-Integration:**
- `/cockpit` Monatsblick zeigt Reichweiten-Δ vs Vormonat
- Geplanter `/business-check`-Skill liest hier alle Daten
- Repost-Logik filtert Posts nach hoher Reichweite

### 💰 Kennzahlen monatlich

**ID:** `2ae7078e-8b7e-8170-83a9-d760d3e593b3`
**Data-Source:** `2ae7078e-8b7e-8184-a86f-000ba2dfde59`
**Zweck:** Monatliche Finanz-KPIs (Umsatz pro Produkt + Kosten + Gewinn + Marge).

**Properties:**
| Metrik | Typ |
|---|---|
| Monat & Jahr | Title |
| Zeitraum | Date |
| Umsatz Expertin statt Verkäuferin | CHF |
| Umsatz Instagram-Kundenmaschine | CHF |
| Umsatz Minikurs „Finde dein Thema" | CHF |
| Umsatz gesamt | CHF |
| Kosten Freelancer | CHF |
| Kosten Tools | CHF |
| Kosten Werbung | CHF |
| Kosten Fortbildung | CHF |
| Kosten gesamt | Formula |
| Gewinn | CHF |
| Gewinn doTERRA | CHF (separat) |
| Gewinnmarge | Formula (%) |

**TODO für Patricia:** Aktuelle Produkte fehlen (Bio-Check, Mama-CEO, Workbook „Von 0 auf echt") — Schema muss bei Launch erweitert werden.

**Skill-Integration:**
- `/cockpit` Monatsblick zeigt Umsatz-Δ + 40k-Jahresziel-Tracking
- `/cockpit` Quartalsblick aggregiert + zeigt vs Quartalsziele

### 💸 Kostenpositionen · 🎨 Branding

| DB | ID | Zweck |
|---|---|---|
| Kostenpositionen | `2ae7078e-8b7e-8136-8351-c7e21b45a664` | Detail-Liste Einzel-Ausgaben |
| Branding | `2ae7078e-8b7e-8188-8287-e21c5fdf5935` | Brand-Assets (Farben, Schriften, Logos) |

(Schema noch nicht detailliert)

---

## DB-Inventur · Bereich PRODUKTE

### 🎁 Produkte (Hauptkatalog)

**ID:** `2ae7078e-8b7e-81ef-aafa-f03993ef344f`
**Data-Source:** `2ae7078e-8b7e-818c-9da2-000b09bae568`

**Properties (wichtigste):**
| Property | Typ | Werte |
|---|---|---|
| Name | Title | |
| Kategorie | Select | **Free Offer** / **Low Price Offer** / **Mid Price Offer** / **High Price Offer** |
| Preis | Number (CHF) | |
| Archiv | Checkbox | |
| Content-Themenplanung | Relation | |
| Aufgaben / Emails / Kunden / Material / Mediathek / Notizen / Projekte / Testimonials / Ziele | Relations | |

**Kategorie-Mapping (Julia-Trost-Treppe):**
- Free Offer → 🎁 Gratis-Fokus im Monatsplan
- Low/Mid Price Offer → 💸 Mini-Fokus
- High Price Offer → 👑 Gross-Fokus

**Skill-Integration:**
- `/produkt` Skill verwaltet diese DB direkt
- `/cockpit` liest Wochen-Hauptprodukt aus Relation
- Story/Reel/Karussell-Bots lesen Funnel-Daten aus active-funnels.json (parallel)

### 🌿 doTERRA Produkte · 📦 Material · 🌟 Testimonials · 📧 Email-Vorlagen

| DB | ID | Zweck |
|---|---|---|
| doTERRA Produkte | `2b57078e-8b7e-805a-9233-e8719abdc6cf` | Öl-Liste mit Wirkbereich |
| Material | `2ae7078e-8b7e-8158-973a-fbe0478f262c` | Kurs-Material, Module |
| Testimonials | `2ae7078e-8b7e-8102-85ea-d065aff208cb` | Kundenstimmen pro Produkt |
| Email-Vorlagen | `2ae7078e-8b7e-813a-a54c-dcbff517c39f` | Mail-Vorlagen für Sequenzen |

(Schema noch nicht detailliert)

---

## Weitere Sub-DBs (in Vorlagen referenziert)

Die Monats- und Wochenplanungs-Vorlagen referenzieren weitere kleinere DBs:

| DB-Zweck | ID |
|---|---|
| Online Business Kennzahlen (in Monatsplan-Vorlage) | `2ae7078e-8b7e-816e-a993-cf9eb860e3cc` |
| Reichweiten-Inline (Monatsplan) | `2ae7078e-8b7e-8172-b95d-ca53f29bc480` |
| Content-Analyse (Monatsplan) | `2ae7078e-8b7e-810b-b672-c12e1abbd3f1` |
| Inline-Wochenplan-Aufgaben | `2ae7078e-8b7e-8104-aad2-f004d92a558d` |
| Routinen-Wochenreflexion | `2ae7078e-8b7e-81b1-a001-e5f947881c89` |
| Kunden-Updates (Wochenvorlage) | `2ae7078e-8b7e-817c-884a-d02e0a55ea59` |
| Themenplanung (Monatsplan) | `2ae7078e-8b7e-81bd-aec0-d9fb4c9cd22d` |
| Ideen-Datenbank | `2ae7078e-8b7e-811a-8cc5-e6f56726fa2e` |
| Redaktionsplan | `2ae7078e-8b7e-816a-979e-ee798279139d` |
| Plattformen-Frequenz | `2ae7078e-8b7e-814d-9086-d881a581da2e` |
| Regelmäßige Aufgaben | `2ae7078e-8b7e-81f2-9188-f74e3b7ddf7b` |
| Quartalsziele-View | `2ae7078e-8b7e-8193-9c79-f7cdddd806e1` |
| Jahresplanung-Inline | `2ae7078e-8b7e-81b2-a62c-ef6aeaa2c249` |
| Projekte-Inline | `2ae7078e-8b7e-8117-a55b-ec988ad09db6` |

---

## Offene Inventur-Themen (nächste Sessions)

Folgende DBs/Vorlagen sind noch nicht detailliert dokumentiert — fetchen wenn ein Skill sie braucht:

- [ ] **Content-Plattformen** Schema (Frequenz pro Plattform-Eintrag)
- [ ] **Content-Management** komplettes Schema (teilweise dokumentiert in notion-content-db.md)
- [ ] **Kunden und Kontakte** (Kategorien, Tags, Pipeline-Stages)
- [ ] **Mediathek**, **Wissensbereiche**, **Wirkbereiche**
- [ ] **doTERRA Produkte**, **Material**, **Testimonials**, **Email-Vorlagen**
- [ ] **Tagesplaner-Vorlage** im Detail
- [ ] **Synced-Blocks** der Monats-Vorlage (welche Daten kommen woher)

---

## Änderungsprotokoll

- **2026-05-02 V1:** Bereich PLANUNG vollständig (Jahresplanung, Ziele, Monatsplanung mit 6-Sektionen-Vorlage, Wochenplanung mit 5-Säulen-Vorlage, Tagesplaner). Wochenstruktur 2026 verknüpft. Schema-Erweiterung Mai-Trio (Gratis/Mini/Gross-Fokus, Wochen-Hauptprodukt, Sales-Pattern).
- **2026-05-02 V2:** Bereiche ORGANISATION (Aufgaben, Arbeitsbereiche), CONTENT MARKETING (Content-Strategie mit Pillar-System, Content-Plattformen, Content-Management), UNTERNEHMEN (Reichweiten Tracking, Kennzahlen monatlich) detailliert. PRODUKTE-Bereich (Hauptkatalog) dokumentiert. Restliche DBs gelistet mit IDs für späteren Detailabruf.
