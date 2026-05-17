# CLAUDE.md

Diese Datei gibt Claude Code (claude.ai/code) Anweisungen für die Arbeit in diesem Repository.

---

## Was das hier ist

Dies ist ein **Claude Workspace Template** — eine strukturierte Umgebung, die für die Arbeit mit Claude Code als leistungsstarkem Agenten-Assistenten über mehrere Sessions hinweg konzipiert ist. Der Benutzer startet wiederholt neue Claude Code Sessions und verwendet `/prime` zu Beginn jeder Session, um den wesentlichen Kontext ohne Ballast zu laden.

**Diese Datei (CLAUDE.md) ist das Fundament.** Sie wird automatisch am Anfang jeder Session geladen. Halte sie aktuell — sie ist die Single Source of Truth dafür, wie Claude diesen Workspace verstehen und darin arbeiten soll.

---

## Die Claude-User-Beziehung

Claude arbeitet als **Agenten-Assistent** mit Zugriff auf die Workspace-Ordner, Kontext-Dateien, Commands und Outputs. Die Beziehung ist:

- **User**: Definiert Ziele, liefert Kontext zu seiner Rolle/Funktion und steürt die Arbeit über Commands
- **Claude**: Liest Kontext, versteht die Ziele des Users, führt Commands aus, produziert Outputs und pflegt die Workspace-Konsistenz

Claude sollte sich immer über `/prime` am Session-Start orientieren, dann mit vollem Bewusstsein dafür handeln, wer der User ist, was er erreichen möchte und wie dieser Workspace das unterstützt.

---

## Workspace-Struktur

```
.
├── CLAUDE.md              # Diese Datei — Kern-Kontext, immer geladen
├── .claude/
│   └── commands/          # Slash-Commands, die Claude ausführen kann
│       ├── prime.md       # /prime — Session-Initialisierung
│       ├── create-plan.md  # /create-plan — Implementierungspläne erstellen
│       └── implement.md   # /implement — Pläne umsetzen
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
| `context/`   | Wer der User ist, seine Rolle, aktuelle Prioritäten, Strategien. Gelesen von `/prime`. |
| `plans/`     | Detaillierte Implementierungspläne. Erstellt mit `/create-plan`, umgesetzt mit `/implement`. |
| `outputs/`   | Deliverables, Analysen, Reports und Arbeitsergebnisse.                                 |
| `reference/` | Hilfreiche Dokumentation, Vorlagen und Patterns für verschiedene Workflows.            |
| `scripts/`   | Automatisierungs- und Tooling-Skripte.                                                 |

---

## Commands

### /prime

**Zweck:** Neue Session mit vollem Kontext-Bewusstsein initialisieren.

Am Anfang jeder Session ausführen. Claude wird:

1. CLAUDE.md und Kontext-Dateien lesen
2. Verständnis von User, Workspace und Zielen zusammenfassen
3. Bereitschaft zur Unterstützung bestätigen

### /create-plan [anforderung]

**Zweck:** Detaillierten Implementierungsplan erstellen, bevor Änderungen gemacht werden.

Verwenden beim Hinzufügen neuer Funktionalität, Commands, Skripte oder bei strukturellen Änderungen. Erzeugt ein gründliches Plan-Dokument in `plans/`, das Kontext, Begründung und schrittweise Aufgaben erfasst.

Beispiel: `/create-plan Wettbewerbs-Analyse-Command hinzufügen`

### /implement [plan-pfad]

**Zweck:** Einen mit /create-plan erstellten Plan umsetzen.

Liest den Plan, führt jeden Schritt der Reihe nach aus, validiert die Arbeit und aktualisiert den Plan-Status.

Beispiel: `/implement plans/2026-01-28-wettbewerbs-analyse-command.md`

### /freitag-hooks · /montag (Content-Pipeline — Voll-Auto seit 2026-05-15)

**Zweck:** Vollautomatische Wochenplanung der Instagram-Posts — **alles in einem Rutsch Fr 08:00.**

**Schedule (cron-driven):**
- **Fr 08:00 → `/freitag-hooks` (VOLL-AUTO seit 2026-05-15):**
  1. Marktanalyse (Pain/Wunsch/Ziel/Herausforderung pro Profil)
  2. Wochenfokus aus Notion lesen
  3. 20 Hooks generieren (10/Profil) — Stakkato-Pflicht-Check aktiv
  4. **Default-Pick algorithmisch** (5+5 deterministisch — Wochenfokus-Priorität, PIE-3-3-3-1, Launch-Boost wenn aktiv)
  5. **Build** aller 4 Karussell-Briefings + Render der PNGs
  6. **Schedule via WordPress + Blotato** für Mo-Sa der nächsten Woche
  7. **Reel-Drehbuch-Master** für die R-Picks
  8. Telegram-Push: „Wochenpaket fertig — du hast Wochenende für Override"

- **Patricia-Override am Wochenende** via Chat:
  - `"KW [N+1] abbrechen + neu picken"` → Skill canceln Blotato + lässt neu picken
  - `"M3 raus, M7 rein"` → einzelner Post-Swap + Reschedule
  - `"Caption M3 ändern: [Text]"` → Caption-Update lokal + Blotato
  - `"Reschedule M3 auf Di"` → Slot-Verschiebung

- **`/montag` ist Plan B** (Fallback wenn Fr-Auto fehlschlägt) — kann manuell getriggert werden für 5+5-Pick-Build.

**Harte Commitments:**
- Zero invented numbers (nur Input oder `patricia-expertise.md`)
- Zero AI-generated Visuals (nur `merge-designs` auf Templates)
- doTERRA-Pflicht: alle Compliance-Memorys + `context/doterra/patricia-wendepunkt-story.md` lesen vor jedem Build
- PIE-Mix Pflicht (3-3-3-1 pro Profil)
- Themen-Variation Pflicht (mind. 2 Pillars pro Profil pro Woche)
- Wochenfokus aus Notion ist Hook-Generator-Quelle
- **Olga-Hook-Pattern-Mix (PFLICHT seit 2026-05-09):** Über die 10 Hooks pro Profil mind. 4 verschiedene Pattern aus Bekenntnis / Contrarian / Curiosity-Gap / Konkrete Zahl / Anti-Hook / Vorher-Nachher. Verhindert dass alle Hooks gleich klingen.

Volle Doku: `reference/montag-workflow-v2.md`.

### /monatsplan (Strategie-Layer seit 2026-05-09)

**Zweck:** Den **Strategie-Layer** für einen kompletten Monat in ~30 Min festschnüren — damit `/freitag-hooks` jede Woche frisch und reaktiv arbeitet, aber innerhalb einer klaren Monats-Storyline.

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
- `outputs/monatsplaene/YYYY-MM.md` mit 4-Wochen-Briefing für /freitag-hooks
- Optional Telegram-Push der Kurz-Zusammenfassung

**Warum nicht 30 Posts auf einmal bauen?** Live-Posts (BTS, Telegram-Call-Reaktionen) brauchen Frische. Trends auf Reddit/IG müssen reagiert werden. Pre-Sale-Signale aus Woche 1 ändern Wochen 2-4. Deshalb: **Strategie monatlich, Konkretion wöchentlich.**

### /garten

**Zweck:** Persönlicher Gartenassistent und Permakultur-Berater starten.

Lädt den Garten-Kontext (Standort Appenzellerland, 920 m, Permakultur-Philosophie) und greift auf die Notion-Datenbanken (Samen, Beetplan, Gartentagebuch, Wissensarchiv) zu. Gibt einen aktuellen Status, zeigt was ansteht und fragt, was heute im Garten geplant ist. Berücksichtigt Mondkalender, Mischkultur, Fruchtfolge und die kurze alpine Vegetationsperiode.

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
7. **Sales-Page (ThriveCart)** — ruft `/salespage` mit Vorbefüllung aus Produkt-Briefing auf
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

### /hormozi

**Zweck:** Copywriting-Doktor nach Alex Hormozi. Nimmt einen bestehenden Text (Caption, Salespage-Block, Mail, Hook, Bio, CTA, Story-Slide, Headline, Werbeanzeige …) und überarbeitet ihn nach Hormozis 7 Frameworks + 12 Persuasion Hacks + Schreibregeln — **ohne Patricias Brand-Voice zu zerstören**.

Hormozi ist hier der STRUKTUR- und PERSUASION-Layer; Patricias warme/empowernde Tonalität bleibt zwingend erhalten.

**9 Modi:**
1. **Doktor** (Standard) — Diagnose + zwei Varianten (sicher / mutig) + Change-Log mit Hormozi-Begründungen
2. **Hook-Battle** — 10 Hook-Varianten nach 10 verschiedenen Hormozi-Hook-Kategorien
3. **Headline-MAGIC** — MAGIC-Offer-Formula (Magnet+Avatar+Goal+Interval+Container) + Lead-Magnet-Naming-Formula
4. **Value-Equation-Audit** — Angebot durchleuchten: Traumergebnis · Erfolgswahrscheinlichkeit · Zeit-Verzögerung · Aufwand
5. **CLOSER-DM** — DM-Antwort nach CLOSER-Framework (Clarify · Label · Overview · Sell · Explain · Reinforce)
6. **4-Pass-Edit** — für lange Texte (Salespages, Mails, Blog): Struktur → Substanz → Klarheit → Empathie
7. **Ad-Bauplan** — Werbeanzeige nach 14-Bausteine-Anatomie (Qualifizierung → Hook → Bold Claim → Reason Why → Pain Stack → Reframe → Unique Mechanism → Authority Stack → Logische Urgency → Lead-Magnet-CTA) + Compliance-Check Meta/doTERRA
8. **Landingpage-Bauplan** — Lead-Capture (8-Block-Mini-Sales-Letter) ODER Sales-Page (12-Block-Long-Form) — Hero/Pain/Dystopie/Mechanism/Success-Event/Authority/Container/Preis/Urgency/FAQ/CTA/P.S.
9. **Funnel-Komplett** — Ad + Landingpage + Danke-Seite + 5 Mails + CLOSER-Anruf-Skript in einem Rutsch

**Wissensgrundlagen:**
- `reference/hormozi/copywriting-bible.md` — alle 7 Frameworks + 12 Persuasion Hacks + Schreibregeln + Anti-Patterns + 4-Pass-Edit-Prozess (verdichtet aus $100M Offers, $100M Leads, ACQ Ads/Closer Handbook, „The Game"-Podcast Ep 245/563/927, LinkedIn/X-Posts, David-Perell-Interview)
- `context/brand-voice.md` + `context/business-info.md` + `context/hook-framework.md`

**Pflicht am Start:** Texttyp · Profil (Mentoring/doTERRA) · Ziel · Avatar · Original-Text.

**Brand-Voice-Pakt:** Hormozi-Defaults wie „Bro/Loser/Crush it", aggressives Repel oder All-Caps werden zu Patricia-konformer Sprache übersetzt. doTERRA-Compliance (keine Heilversprechen) immer eingehalten.

**Bonus-Layer-Integration (seit 2026-05-04):** Die Hormozi-Bibel ist als Pflicht-Lektüre in **alle 8 Content-Skills** eingebaut — `/freitag-hooks`, `/karussell`, `/reels`, `/story`, `/montag`, `/produkt`, `/salespage`, `/funnel`. Jeder Skill wendet die jeweils relevanten Hormozi-Sektionen automatisch an (z.B. `/freitag-hooks` nutzt 8 Hook-Kategorien + Validity×Utility-Filter, `/salespage` nutzt 12-Block-Long-Form-Struktur, `/funnel` Mode 3 delegiert die Ad-Copy explizit an `/hormozi` Modus 7). **Hormozi ist Verstärker, nicht Ersatz** — Brand-Voice + doTERRA-Compliance + Julia-Trost-Strategie haben weiter Vorrang.

Output: `outputs/hormozi/YYYY-MM-DD-[texttyp]-[slug].md` mit Original + Diagnose + Variante A/B + Change-Log + angewandte Frameworks.

### /salespage

**Zweck:** Komplette Sales-Page nach Julia Trosts Methodik erstellen.

Führt ein strukturiertes Interview (Angebot, Zielgruppe, Transformation, Story, Module, FAQ) und generiert dann 13 fertige Textblöcke — copy-paste-ready für ThriveCart. Basiert auf Julias "Salespages die verkaufen"-Framework inkl. Kaufpsychologie, Storytelling und Trigger.

Output wird in `outputs/salespages/` gespeichert.

### /karussell

**Zweck:** Instagram-Karussells planen, bauen und fixen — mit Folien-Plan, Feed-Aesthetic-Check und Notion-Integration.

Zwillingsbruder von `/reels`. Fragt IMMER zürst das Profil ab (Mentoring vs. doTERRA), prüft Canva-Grid-Farben für Feed-Aesthetic-Rotation, baut Hooks strikt nach `context/hook-framework.md`, legt Notion-Einträge in der Content-Management-DB an.

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

Patricias Reel-Produzent. Fragt **immer zürst** das Profil ab (Onlinebusiness/Mentoring vs. Network/doTERRA), recherchiert aktuelle virale Formate auf anderen Kanälen (WebSearch IG/TikTok/FB), baut Hooks strikt nach `context/hook-framework.md`, nutzt bevorzugt Patricias eigene Canva-Videos und ergänzt mit Stock-B-Roll. Wenn nötig gibt er konkrete **Dreh-Anweisungen** mit exaktem zu sprechenden Text.

5 Modi:
- **Reel-Konzept aus Idee** — volles Briefing (Hook + Shotlist + Dreh-Anweisung + Caption + CTA + 5 Hashtags)
- **Rohmaterial → Reel** — Cut-Reihenfolge aus vorhandenen Clips
- **Hook-Brainstorm** — 10 Hook-Varianten nach Framework
- **Reel-Kritik / Reel-Doktor** — Diagnose + 3 konkrete Fixes
- **Wochen-Reel-Plan** — 3-5 Reel-Ideen

Wissensgrundlagen:
- `context/reels-framework.md` — Viral-Mechanik 2026, 3-Sek.-Regel, Reel-Typen, Hook-Pflicht-Prozess, Talking-Head-Anweisungen, Caption-Strategie, Top-5-Hashtags pro Profil
- `context/brand-voice.md` / `context/hook-framework.md` / `context/caption-formeln.md`
- `reference/julia-trost/methodik.md` + `Reels to Cash.pdf` + `Stories die verkaufen.pdf` (Kaufpsychologie in Captions)

Output wird in `outputs/reels/` gespeichert.

### /funnel

**Zweck:** Funnel-Stratege für Mum Life Balance. Plant, baut und orchestriert komplette Funnel über 5 Modi: Strategie · Bauen · Werbeanzeigen · Launch · Analyse.

Live seit 2026-04-24. Verbindet alle 7 Systeme: WordPress (`/wp`) · ActiveCampaign (MCP) · ManyChat (Pro-API) · Thrivecart · Notion Produkte-DB · Canva (MCP) · Content-Assistenten (`/montag`, `/reels`, `/karussell` lesen `context/active-funnels.json`).

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

**Zweck:** Master-Jahres-Sicht über alle Launches/Produkte/Kampagnen — verknüpft mit Notion-Jahresplanung-DB. Wird von `/montag`, `/reels`, `/karussell`, `/funnel` als Wochen-Kontext gelesen.

**Status:** SPEC angelegt am 2026-05-01 — Implementierung folgt in nächster Session sobald Patricia die Notion-Jahresplanung-DB-ID liefert.

**5 Modi:**
1. `/jahresplan status` — „Wo stehe ich heute?" (aktuelle KW + parallele Produkte + nächste Meilensteine)
2. `/jahresplan launch [slug]` — neuen Launch ins Master-Markdown + Notion eintragen
3. `/jahresplan vorschau [monat]` — Monats-Sicht mit Konflikten
4. `/jahresplan konflikt-check` — überlappende Aktivitäten identifizieren
5. `/jahresplan notion-sync` — manueller Sync mit Notion-Jahresplanung-DB

**Datenfluss:** `/produkt` → `outputs/produkte/[slug]/07-launch-kalender.md` → `/jahresplan launch` → `context/jahresplan-2026.md` ←→ Notion. Phase-Marker maschinenlesbar in `context/active-funnels.json`.

**Volle Doku:** `.claude/commands/jahresplan.md`.

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

1. **Start**: `/prime` ausführen, um Kontext zu laden
2. **Arbeiten**: Commands verwenden oder Claude direkt mit Aufgaben beauftragen
3. **Änderungen planen**: `/create-plan` vor größeren Ergänzungen verwenden
4. **Umsetzen**: `/implement` zum Ausführen von Plänen verwenden
5. **Pflegen**: Claude aktualisiert CLAUDE.md und context/ während sich der Workspace weiterentwickelt

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

Plan: `plans/2026-05-07-apify-mcp-integration.md`.

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

### Telegram News-Bot (`scripts/telegram-news-bot/`)

Wöchentlicher News-Digest-Bot, der Artikel aus RSS-Feeds (Onlinemarketing & KI) sammelt, mit Claude zusammenfasst und per Telegram sendet.

- **Sprache:** Python 3.11+
- **Konfiguration:** `config.py` (Feeds, Schedule), `.env` (API-Keys)
- **Lokal testen:** `python bot.py --now` (sofortiger Digest)
- **Daürbetrieb:** `python bot.py` (wöchentlicher Schedule)
- **Deployment:** Railway/Render via `Procfile`
- **Setup-Anleitung:** `scripts/telegram-news-bot/README.md`

### Instagram Content-Engine (Automatisiert, v2 seit 2026-04-21)

**Vollautomatisches Content-System für beide Profile** (Mentoring + doTERRA). Weekly Content-Generation + Daily Auto-Posting + Monthly Best-Performer-Repost. Gesteürt durch 3 Scheduled Tasks + 2 Assistenten (`/reels`, `/karussell`).

**Content-Grundlagen** (in `context/`):
- `brand-voice.md` — Tonalität, Schreibregeln, Kernbotschaft, Beispieltexte
- `caption-formeln.md` — 5 Caption-Strukturen + CTA-Varianten + Hashtag-Strategie
- `hook-framework.md` — Hook-Kategorien (Zahlen, Anleitungen, Provokant, Neugier, Identifikation)
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
- **Montags-Content-Engine** (`scheduled-task-montags-engine.md`) — Mo 06:00: Trend-Scraping auf 5 Plattformen (IG/TikTok/FB/Reddit/Twitter), 20 spezifische Hooks (10 pro Profil, strikt nach `hook-framework.md`), 10 Karussell- + 10 Reel-Entwürfe, Feed-Aesthetic-Check, Notion-Einträge
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
- `freitag-hooks.yml` — wöchentliche Hook-Generierung (Secrets: `ANTHROPIC_API_KEY`, `BLOTATO_API_KEY`, `NOTION_TOKEN`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`)
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
