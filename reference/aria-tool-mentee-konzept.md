---
tags: [tools, research, reference, mba]
---

# ARIA (Julia Trost) — Tool-Analyse + Patricia-Mentee-Konzept

**Analyse-Datum:** 2.6.2026
**URL:** https://aria.juliatrost.de/hub
**Tool-Name:** ARIA (Business-Compass „Business mit KI")
**Credits-Stand bei Patricia:** 200 übrig
**Patricia-Idee:** Mentees sollen das Tool mit IHREN Daten füttern → dann generiert es personalisiert → USP für MBA

---

## 1. Was ist ARIA?

Ein **End-to-End-Onboarding-Tool für Online-Business-Aufbau** mit KI-Assistentin „Aria" (Julia Trosts Avatar). Strukturiert in **6 sequenziellen Schritten** vom Nische-Finden bis zum 10K-Monat.

**Tagline:** „Du brauchst keine grosse Reichweite. Du brauchst das richtige System."

### Die 6 Module (sequenziell, jeweils mit Sperrlogik)

| # | Modul | Was es macht | Status |
|---|---|---|---|
| 1 | **Nischen Navigator** | Aria stellt 6 Fragen (3 Sets), findet Sweet-Spot-Nische | Frei zugänglich |
| 2 | **Produkt Werkstatt** | Baut Minikurs (<50€) oder Großkurs (ab 499€) — Outline + Inhalte | Verlangt Schritt 1 |
| 3 | **Funnel Builder** | Plant kompletten Verkaufs-Funnel | Verlangt Schritt 2 |
| 4 | **Landingpage Designer** | Generiert Sales/Opt-in/Checkout/Application/Thank-You-Seiten | Verlangt Schritt 2 |
| 5 | **Launch Studio** | Plant Launch-Kampagne | Verlangt Schritt 3/4 |
| 6 | **10K Roadmap** | Konkreter Skalierungs-Plan zum 10K-Monat | Endpunkt |

### Kern-UX

- **Conversational KI** — Aria fragt, User antwortet (6 Fragen pro Modul)
- **Bibliotheken** — jedes Modul hat eine eigene „Bibliothek" wo User's Antworten/Outputs gespeichert werden („Nischen-Bibliothek", „Produkt-Bibliothek", etc.)
- **Sperrlogik** — ohne abgeschlossenen Schritt 1 kein Zugriff auf Schritt 2 (zwingt durch die Reihenfolge)
- **Manueller Override** — User kann auch ohne Aria-Chat direkt eine Nische manuell anlegen
- **Mehrere Versuche** — User kann mehrere Nischen/Produkte parallel anlegen

### Tech-Stack (vermutet)

Vermutlich gleicher Stack wie Content Radar (gleicher Anbieter):
- Next.js Frontend
- LLM-Backend (vermutlich GPT-4o oder Claude Sonnet) für Aria-Chat
- Supabase oder ähnlich für User-Daten
- 200 Credits-Modell für Generierungen

### URL-Struktur

```
/hub                      → Willkommen + Übersicht
/hub/nischen-navigator    → Modul 1
/hub/produkt-werkstatt    → Modul 2
/hub/funnel-builder       → Modul 3
/hub/landingpage-designer → Modul 4
/hub/launch-studio        → Modul 5
/hub/10k-roadmap          → Modul 6
```

---

## 2. Vergleich: Content Radar vs. ARIA

| Aspekt | Content Radar | ARIA |
|---|---|---|
| **Fokus** | Content-Performance + Plan | Online-Business-Aufbau Schritt für Schritt |
| **Input** | Apify-Scrapes (Instagram-Daten) | User-Antworten in Conversational Chat |
| **Output** | Wochen-Content-Plan + Hooks | Nische, Produkt, Funnel, LP, Launch-Plan |
| **Anwender** | Bereits aktive Content-Creator | Anfängerinnen ohne Produkt/Nische |
| **Use-Case** | „Welcher Post wann?" | „Was soll ich überhaupt verkaufen?" |
| **Kombination** | Komplementär | Komplementär |

**Patricia-Insight:** Die zwei Tools decken zwei Phasen ab — ARIA fürs Setup (vor MBA-Pilot), Content Radar für laufende Optimierung (nach MBA-Pilot). Ein eigenes Patricia-Tool müsste BEIDE Phasen kombinieren.

---

## 2.5 🎯 KILLER-USP: Network-Spezialisierung (Patricia-Entscheidung 2.6.2026)

**Patricia-Schärfung:**
> „Ganz wichtig: mein Assistent soll aufs Network spezialisiert sein."

Das verändert die ganze Positionierung von „eigener KI-Tool-Konkurrent zu ARIA" zu **„nicht-vergleichbares Tool in einer eigenen Nische"**.

### Markt-Vergleich neu

| Tool | Zielgruppe | Spezialisierung |
|---|---|---|
| Julia Trost (ARIA) | Online-Business-Coaches generell | Keine — generisch |
| ChatGPT / Jasper | Alle | Keine |
| Coachen-Templates | Diverse | Generisch |
| **PIA (Patricia)** | **Mamas im Network** die parallel ein eigenes Standbein aufbauen | **Network Marketing + Online-Business-Hybrid** |

### Network-Spezifika die PIA „kann" (andere Tools nicht)

1. **Firmen-Wissen:** doTERRA, Forever, Mary Kay, Ringana, Younique etc. — jeweilige Produkte, Rang-System, Compliance-Regeln
2. **Rang-Sprache:** Beraterin/Diamant/Director/Crown — pro Firma anders
3. **Team-Aufbau-Dynamik:** Crossline-Situationen, Down-Line-Skalierung, Eltern-Linie
4. **Network-Pain-Points:**
   - Crossline-Beraterin steigt auf, du nicht
   - Familie versteht das System nicht
   - „bist du sicher dass das kein Pyramidensystem ist?"-Fragen
   - Convention-FOMO + Schuldgefühl
   - Compliance-Verbote „ich darf das nicht so sagen"
5. **Hybrid-Strategie:** Network + eigenes Standbein parallel — ohne dem Network-Team zu schaden (= Patricia's Sweet-Spot)
6. **Compliance-Filter pro Firma:** doTERRA → keine Heilversprechen, Forever → keine medizinischen Aussagen, etc.
7. **Hook-Patterns Network-spezifisch:** Convention-Erlebnisse, Compliance-Wendepunkte, Authentic-Selling vs DM-Spam

### Marketing-Pitch (neu)

> „Die erste KI-Mentorin SPEZIELL für Mamas im Network. Patricia hat 10+ Jahre Network-Erfahrung + KI-Stack reingebaut. PIA versteht Crossline-Situationen, Team-Aufbau, Compliance-Regeln deiner Firma und Mama-Realität — generische KI-Tools verstehen das nicht."

### Konsequenzen für die Build-Roadmap

**Onboarding-Fragen (Stufe 0) müssen Network-Spezifika abdecken:**
- Welche Network-Firma? (Dropdown mit den großen)
- Welche Position? (Beraterin / höhere Ränge — Firma-abhängig)
- Team-Größe + Crossline-Situation
- Compliance-Regeln deiner Firma (Free-Text + Selbstcheck)
- Network-Ziel: Rangaufstieg vs Standbein vs beides?
- Crossline-Pain: was triggert dich?

**System-Prompts (alle Stufen) müssen Network-Layer einbauen:**
- Compliance-Filter Mode 1: doTERRA (Patricia's eigene Compliance-Regeln aus Memory)
- Compliance-Filter Mode 2-N: andere Firmen (von Mentee gepflegt oder Standard)
- Network-Pattern-Bibliothek (statt nur Online-Business-Patterns)

**Differenzierung MBA-Bundle:**
- MBA bleibt für Mamas im Network + Onlinebusiness (Hybrid)
- PIA wird das ausführende Tool das die Hybrid-Strategie umsetzt
- Klare Botschaft: „MBA = du lernst die Hybrid-Strategie. PIA = führt sie für dich aus, jeden Tag."

---

## 2.6 🎯 KERN-LOGIK: Transformation > Produkt (Patricia-Schärfung 2.6.2026)

**Patricia-Mantra für PIA:**
> „Weg vom Produkt, hin zum Thema bzw. der Transformation des Kunden."

PIA arbeitet **nicht produktzentriert**. Sie arbeitet **transformationszentriert** — das Produkt (Network-Artikel oder digitaler Kurs) ist nur die Brücke.

### Transformation-Beispiele (statt Produkt-Features)

| Produkt | Transformation (was PIA verwendet) |
|---|---|
| Ätherisches Öl | „Ruhiger Schlaf für deine Kinder" |
| Hautpflege | „Du fühlst dich wieder schön in deiner Haut" |
| Network-Geschäft | „Selbstbestimmung ohne Familie zu verraten" |
| Online-Kurs | „Klarheit. Zeit. Eigenes Standbein." |

### Die 2-Pfade-Hybrid-Strategie

Patricia's Killer-Insight: nicht jede Mentee will/kann sofort eigene digitale Produkte bauen. PIA muss BEIDE Pfade abdecken.

**Pfad A: Mentee will Hybrid (Network + eigene Produkte)**
- Online-Kurs-Outline + Mini-Produkt-Test + Pricing-Strategie
- Funnel der BEIDES verkauft (eigenes Produkt + Network-Empfehlung)

**Pfad B: Mentee will (noch) keine eigenen Produkte — pur Network**
- Leadmagnet der die Transformation kommuniziert
- E-Mail-Sequenz die in der Transformation lebt + subtil zum Network-Produkt brückt
- KEIN „bau einen Kurs"-Druck (= das wäre Verrat an der Mentee-Realität)

**Pfad C: Unentschlossen**
- Mini-Test: Leadmagnet bauen + Antwort-Quote messen → erst dann entscheiden

### Content-Verkaufs-Logik: Brücke bauen, nicht pushen

Jeder PIA-Output (Hook, Caption, Story, Mail, Leadmagnet) hat:
- **Hauptteil = Transformation** (80%) — Mentee teilt Erfahrung, Mehrwert, Mini-Lesson
- **Brücke = Verkaufs-Slot** (20%) — subtil führen zu Network-Produkt oder digitalem Produkt
- **Pflicht-Filter:** keine „Kauf bei mir!"-Sprache · keine Heilversprechen · Compliance-konform

Vorbild: Patricia's `patricia-wendepunkt-story.md` — die ganze Doku ist Transformation mit „bei mir war"-Frame. Verkauf passiert durch Beweis, nicht Pitch.

### Was bedeutet das für die PIA-Module

Statt nur Hook+Caption-Generator brauchen wir konkret:

1. **Transformation-Mapper** — Mentee artikuliert WAS sie eigentlich vermittelt (statt Produkt-Features)
2. **Hybrid-Decision-Tree** — Pfad A/B/C wählen, mit kontextueller Beratung
3. **Leadmagnet-Builder** — PDF/Workbook/Mini-Video-Kurs mit Brücke
4. **Funnel-Architect** — E-Mail-Sequenz mit Cross-Pollination
5. **Content-Recycling-Maschine** — 1 Transformation → 7 Stories + 3 Reels + 1 Karussell + 5 Mails (alle mit Brücke)
6. **Brand-Voice-Filter pro Mentee** — Output klingt nach Mentee, nicht nach Patricia oder ChatGPT

---

## 3. 🎯 Patricia's Killer-Idee: „PIA" für MBA-Mentees

**Patricia's Insight (2.6.2026):**
> „Noch mehr Mehrwert wäre es natürlich, wenn meine Mentees das Tool zuerst mit ihren Daten füttern könnten."

### Was das konkret bedeuten würde

Statt dass die Mentee Patricia's MBA-Inhalte konsumiert und SELBST übersetzt auf ihre Situation — gibt ein Tool ihr die Vor-Übersetzung. Die Mentee:

1. Bucht MBA
2. Erhält Zugang zu **„PIA" (Patricia AI / Personalized Instagram Assistant)** als Bonus
3. Macht ein **15-Minuten-Onboarding mit PIA**:
   - Wer bist du? (Lebensphase, Kinder, Beruf, Network-Erfahrung)
   - Was ist deine Nische? (Network-Firma + Sub-Spezialisierung)
   - Wo stehst du gerade? (Follower, Anfragen, Umsatz)
   - Welche Säulen-Themen hast du? (analog zu Patricia's Pillar-System)
   - Wer ist deine Zielgruppe? (Sub-Avatar)
   - Was ist deine Story/Wendepunkt?
4. PIA speichert das als ihr **persönliches Mentee-Profil**
5. Mentee kann dann ihr ganzes MBA-Setup mit personalisierten Vorschlägen aus PIA bauen

### Was PIA dann generieren könnte (alle personalisiert auf Mentee)

- **Hook-Varianten** mit Mentee-realen Zahlen + Pattern aus Patricia's `content-radar-juni-2026.md`
- **Wochen-Content-Plan** mit Mentee-Wochenfokus + Mentee-Säulen
- **Bio-Generator** angepasst auf Mentee-Nische
- **Story-Sequenzen** mit Mentee-Käufertypen-Rotation
- **Funnel-Konzept** angepasst auf Mentee-Produkt-Treppe
- **Salespage-Texte** in Mentee-Voice
- **Reel-Drehbücher** mit Mentee-realen Alltagsszenen
- **Pre-Sale-Strategien** angepasst auf Mentee-Warmlist-Größe

### Warum das ein **USP-Killer** für MBA wäre

**Aktueller MBA-Stand:** 3 Kurse + Umsetzerinnen-Calls = Wissen + Begleitung
**Mit PIA dazu:** Wissen + Begleitung + **personalisiertes KI-Tool das nur Mentees haben**

Konkurrenz-Vergleich:
- Julia Trost hat ARIA — aber generisch für alle, nicht auf Julias spezifisches System kalibriert
- Sonstige Mama-Business-Coaches haben max Templates + Workbooks
- **Patricia hätte: Coach + KI-System das den Coach-Stil emuliert + auf Mentee personalisiert**

Das ist der erste DACH-Mama-Business-Coach mit eigenem KI-Mitarbeiter-System für Mentees. Marketing-Hebel:
> „Du bekommst nicht nur den Kurs — du bekommst PIA, deine persönliche KI-Mentorin, die das Mama-CEO-System auf DEINE Situation überträgt. Während du in den Calls lernst, baut PIA mit. 24/7."

---

## 4. Build-Konzept „PIA"

### MVP-Scope (3 Phasen)

**Phase 1 — Onboarding-Bot (5-7 Tage)**
- Conversational-UI (Web oder Telegram) wo Mentee 15-20 Fragen beantwortet
- Daten landen in `mentee_profiles` Tabelle (Supabase)
- Fragenset orientiert sich an Patricia's bewährtem Coaching-Interview (Mama-CEO Modul 1 = Profil-Schärfung)
- **Reuse:** Patricia's existierendes 35-Fragen-Coaching-Interview aus dem `patricia-vollprofil.md`-Memory

**Phase 2 — Content-Generator (5-7 Tage)**
- Hook + Caption Generator mit Mentee-Daten + Patricia-Patterns
- 3 Pattern-Varianten pro Hook (wie Content Radar es macht)
- Brand-Voice-Filter: Mentee-Voice (gespeichert) + Patricia-Grundregeln (Schweizer ss, keine Stakkato, keine Hype-Preise, kein Anti-Doctrine)
- **Reuse:** Patricia's `content-radar-juni-2026.md` als System-Prompt-Kontext

**Phase 3 — Funnel + Visual + Auto-Post (7-10 Tage)**
- Funnel-Generator (Lead-Magnet, Mail-Sequenz, Salespage-Text)
- Visual-Pipeline (PNG-Render für Karussells + Stories) — **bereits vorhanden**
- Auto-Post via Mentee's eigene Blotato/WP-Verbindung
- **Reuse:** Patricia's gesamter `scripts/` Ordner

### Architektur

```
┌─────────────────────────────────────────────────────────────┐
│ Mentee-Frontend: Next.js auf mumlifebalance.ch/pia          │
│ - Login (E-Mail/Pass, Mentee-Auth)                          │
│ - Onboarding-Chat mit PIA                                    │
│ - Dashboard: Content-Plan + Hooks + Captions + Funnel        │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ Backend: Next.js API Routes                                  │
│ - /api/onboard (Aria-style Conversational)                   │
│ - /api/generate-hooks (Mentee-Profile + Patricia-Patterns)   │
│ - /api/generate-funnel (Mentee-Produkt + Patricia-Methode)   │
│ - /api/render (Mentee-PNG-Outputs)                           │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ Daten-Layer: Supabase                                        │
│ - mentees, mentee_profiles, mentee_pillars                  │
│ - mentee_products, mentee_content, mentee_funnels            │
│ - patricia_knowledge (Embeddings aller context/-Files)        │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ AI-Layer:                                                    │
│ - Claude Sonnet (Conversational + Long-Context)              │
│ - System-Prompts: Patricia-Stil-Embedding aus context/-Files │
└─────────────────────────────────────────────────────────────┘
```

### Was Patricia bereits hat (Reuse-Inventur)

✅ **35-Fragen-Coaching-Interview** in `patricia-vollprofil.md` — direkt verwendbar für Mentee-Onboarding
✅ **Content-Radar-Patterns** in `content-radar-juni-2026.md` — als Generator-Prompt
✅ **5-Typen-Content-Formel** in `content-formel-5-typen.md` — als Klassifikator
✅ **Reichweiten-Formel** in `reichweiten-formel-mama-identity.md` — als Strategie-Layer
✅ **PNG-Render-Pipeline** in `scripts/karussell-render/` — direkt für Mentee-Outputs nutzbar
✅ **Mama-CEO Modul-1-Material** in `outputs/produkte/mama-ceo/` — als didaktische Begleitung
✅ **Julia-Trost-Methodik** in `reference/julia-trost/` — als zweiter Strategie-Layer
✅ **WordPress + Blotato + Notion-Integration** — für Mentee-Auto-Post wenn gewünscht

**Heisst:** ca. 70% des PIA-Tools liegt schon im Workspace. Was fehlt: Frontend + Mentee-Login + Patricia-Memory als Embedding.

### Aufwand-Schätzung

| Phase | Tage |
|---|---|
| Phase 1 (Onboarding) | 5-7 |
| Phase 2 (Content-Generator) | 5-7 |
| Phase 3 (Funnel + Visual + Post) | 7-10 |
| Frontend + Auth + Stripe-Integration | 5-7 |
| Testing mit 4 Pilot-Mentees | 3-5 |
| **TOTAL MVP** | **25-36 Tage** |

→ Realistisch in **6-8 Wochen** parallel zum Mama-CEO-Pilot machbar.

### Laufende Kosten (pro Mentee pro Monat)

- Anthropic API (Claude für Mentee-Generierungen): ~10-25 USD
- Supabase (gemeinsam, ein Tier): ~25 USD total
- Vercel Hosting: 0-20 USD total
- **TOTAL: ~10-25 USD pro Mentee/Monat**

→ Bei 990 CHF Pioneer-Preis und z.B. 20 Mentees in Runde 2 wäre das eine geringe Marge-Beeinträchtigung für den USP-Hebel.

---

## 5. Strategische Überlegungen

### Pro PIA bauen

- **USP-Killer** — niemand sonst im DACH-Mama-Business hat sowas
- **Mentee-Wow-Effekt** — die Mentee fühlt sich verstanden, hat sofort konkrete Outputs
- **Skalierung des Coachings** — Patricia muss nicht jeden Mentee einzeln durchcoachen
- **Daten-Goldmine** — sieht was Mentees fragen, wo sie hängen, optimiert MBA-Inhalte
- **Mögliche Vermarktung** — PIA als Standalone-Produkt nach MBA-Validierung verkaufbar
- **DEFENSIBILITY** — wenn andere Coaches PIA kopieren wollen, müssen sie Patricia's 100k+ Wörter Wissensbasis nachbauen

### Contra

- **6-8 Wochen Build** — parallel zum Mama-CEO-Pilot (1.6.) anstrengend
- **Wartungs-Aufwand** — Embeddings müssen aktualisiert werden wenn Patricia neue Memory-Files schreibt
- **Mentee-Erwartungs-Management** — PIA ist Werkzeug, nicht Ersatz für Patricia (= klare Kommunikation)
- **Initial-Cash-Out** — ggf. Entwickler engagieren wenn Claude Code alleine nicht reicht

### Mein Vorschlag — Stufen-Plan

**Stufe 0 — JETZT (1 Tag):** Mentee-Onboarding-Slash-Command in Claude Code bauen, der die 35 Fragen interaktiv stellt + Profil-Datei in `outputs/mentees/[name]/profile.md` speichert. Patricia kann das in Calls mit Pilot-Mentees nutzen.

**Stufe 1 — KW24-25 (5-7 Tage):** Content-Hook-Generator als Slash-Command, der aus Mentee-Profil + Patricia-Patterns 3 Hook-Varianten pro Post generiert. Patricia kann das für Pilot-Mentees als Service einsetzen.

**Stufe 2 — KW26-28 (10-14 Tage):** Telegram-Bot „PIA" baut, der Mentees direkt erreicht. Onboarding + Hook-Generator + Content-Plan-Generator. Pilot-Mentees können das nutzen, Patricia bekommt Logs zum Auswerten.

**Stufe 3 — Q3 2026 (15-20 Tage):** Web-Frontend bauen wenn Pilot-Phase positiv. Stripe-Integration für PIA-Add-On (z.B. „MBA + PIA für 1290 CHF Pioneer / 1647 Listenpreis").

---

## 6. Konkrete Frage an Patricia (zum Entscheiden)

1. **Stufe 0 jetzt anlegen?** (1 Tag — Slash-Command für 35-Fragen-Onboarding)
2. **Pilot-Mentees als Tester?** (4 Mama-CEO-Käuferinnen → werden Pilot-Tester für PIA)
3. **PIA-Branding final?** (PIA / Pia / Patricia-Assistent / anderes Name?)
4. **Web-Frontend Sommer 2026 oder Q3?**

---

## 🔗 Verwandte Notizen

- [[content-radar-tool-analyse]] — analoge Analyse von Julia Trosts ersten Tool
- [[../context/patricia-vollprofil]] — die 35-Fragen-Wissensbasis (Onboarding-Quelle)
- [[../context/content-radar-juni-2026]] — Hook-Patterns für Generator
- [[KRITISCH-mba-bundle-struktur|MBA-Bundle-Struktur]] — Pflicht für Mentee-Output
- [[KRITISCH-mama-ceo-outline-verbindlich]] — Mama-CEO Struktur (Vorlage für Mentee-Säulen)
