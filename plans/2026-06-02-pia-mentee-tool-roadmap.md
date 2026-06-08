---
tags: [plan, mba, tools]
---

# Plan · PIA — KI-Mentorin für MBA-Mentees (Roadmap)

**Erstellt:** 2.6.2026
**Patricia-OK:** „Ich find's geil" (2.6.2026)
**Status:** Roadmap festgehalten, Stufe 0 wartet auf Start-Freigabe
**Volle Konzept-Doku:** [`../reference/aria-tool-mentee-konzept.md`](../reference/aria-tool-mentee-konzept.md)

## Vision

PIA (Patricia Intelligence Assistant) — die **erste KI-Mentorin SPEZIELL für Mamas im Network**, die parallel ein eigenes Standbein aufbauen wollen, ohne dem Network-Team zu schaden.

**Killer-USP (Patricia-Entscheidung 2.6.2026):** Network-spezialisiert. Kennt Firmen (doTERRA, Forever, Mary Kay, Ringana, Younique etc.), Rang-Sprache, Compliance-Regeln, Crossline-Dynamik, Team-Aufbau, Convention-Realität. Generische KI-Tools (ChatGPT, ARIA) verstehen das nicht.

Marketing-Pitch:
> „Die erste KI-Mentorin SPEZIELL für Mamas im Network. Patricia ist seit 2018 im Network + hat ihren KI-Stack reingebaut. PIA versteht Crossline-Situationen, Team-Aufbau, Compliance-Regeln deiner Firma und Mama-Realität — generische KI-Tools verstehen das nicht."

## Stufe 0 — Slash-Command `/mentee-onboard` (1 Tag)

**Ziel:** Patricia kann ab der nächsten Pilot-Mentee-Session (innerhalb dieser Woche) das Onboarding-Tool nutzen.

### Implementierungs-Schritte

1. **Skill-File anlegen:** `.claude/commands/mentee-onboard.md`
   - 35 Coaching-Fragen aus `context/patricia-vollprofil.md` extrahieren
   - **PLUS Network-spezifischer Frageblock** (siehe unten)
   - In sinnvolle Sets gruppieren (z.B. 6 Sets à 7 Fragen — Set 1 = Network-Basics)
   - Conversational-Flow: ein Set fragen → Antwort speichern → nächstes Set
2. **Output-Struktur:** `outputs/mentees/[mentee-slug]/profile.md`
   - YAML-Frontmatter mit Metadaten (Onboarding-Datum, MBA-Pilot-Phase, Network-Firma, etc.)
   - Strukturierte Sektionen: Profil · **Network-Setup (Firma/Rang/Team)** · **Network-Compliance** · Zielgruppe · Säulen · Story · Produkte · Ziele · Brand-Voice · Wo-stehst-du

### Network-spezifischer Frageblock (Pflicht in Onboarding Set 1)

1. Welche Network-Firma? (doTERRA / Forever / Mary Kay / Ringana / Younique / Mōdere / dōTeam / Andere)
2. Aktuelle Position/Rang in der Firma?
3. Wie groß ist dein Team aktuell? (1st Line + Gesamt-Down-Line)
4. Bist du grad in einer Crossline-Situation, die dich triggert? (Free-Text)
5. Welche Compliance-Regeln muss deine Firma einhalten? (z.B. keine Heilversprechen, keine medizinischen Aussagen, keine Einkommens-Versprechen — Mehrfachauswahl + Free-Text)
6. Was ist dein Ziel im Network? (Rangaufstieg / paralleles Standbein / beide / Ausstieg planen)
7. Wo erlebst du den größten Reibungspunkt? (Familie versteht's nicht / Compliance fühlt sich eng an / Crossline-Vergleich / Team-Aufbau-Plateau / Konflikt mit eigenem Standbein / Anderes)
3. **Index aktualisieren:** `outputs/mentees/_INDEX.md` und Tag `[mentee-profil]`
4. **Pilot-Test:** Patricia spielt es zuerst mit ihrem eigenen Profil durch (Kalibrierung) — dann mit einer der 4 Pilot-Mentees

### Akzeptanzkriterien

- [ ] Slash-Command `/mentee-onboard [name]` startet die Konversation
- [ ] Alle 35 Fragen werden gestellt — entweder einzeln oder als Set
- [ ] Antworten landen strukturiert in `outputs/mentees/[name]/profile.md`
- [ ] Patricia hat den Workflow einmal selbst durchgespielt
- [ ] Skill nutzt Patricia-Voice (Du-Anrede, warm, kein Hype)
- [ ] Skill-Doku in CLAUDE.md ergänzt

## Stufe 0.5 — Transformation-Mapper + Hybrid-Decision (1-2 Tage, sofort nach Onboarding)

**Ziel:** Bevor PIA Content generiert, klärt sie WAS die Mentee verkauft (Transformation, nicht Produkt) und WIE (Pfad A/B/C).

### Was zu bauen ist

- Slash-Command `/mentee-transformation [name]`
- Liest `outputs/mentees/[name]/profile.md`
- Stellt Fragen-Set in 2 Phasen:

**Phase 1 — Transformation-Mapping** (5 Fragen):
1. Welches Problem löst dein Network-Produkt für deine Kundin? (NICHT was es IST — sondern was es VERÄNDERT)
2. Wie fühlt sich deine Kundin VOR dem Produkt? (3 Adjektive + 1 Situation)
3. Wie fühlt sie sich DANACH? (3 Adjektive + 1 Situation)
4. Was würde sie über sich selbst sagen, wenn sie's geschafft hat? (1 Satz)
5. Welches Wissen aus deinem Network könntest du auch ohne Produkt vermitteln? (= Kerntransformation)

**Phase 2 — Hybrid-Entscheidung** (3 Fragen):
1. Hast du Lust auf eigene digitale Produkte? (Ja / Nein / Vielleicht)
2. Wenn ja: was ist näher dran — Mini-Produkt (9-37€) oder Großkurs (ab 499€)?
3. Wenn nein/vielleicht: würdest du erstmal einen Leadmagnet bauen + testen welche Resonanz da ist?

**Output:** `outputs/mentees/[name]/transformation.md`
- 3-5 Transformation-Statements (in Mentee-Voice)
- Pfad-Entscheidung (A/B/C)
- Empfohlene nächste Stufe für PIA

## Stufe 1 — Content-Generator mit Brücke (5-7 Tage, KW24-25)

**Ziel:** Aus Mentee-Profil + Transformation + Patricia-Pattern → Content mit eingebauter Brücke zum Produkt

### Was zu bauen ist

- Slash-Command `/mentee-content [name] [thema]`
- Liest `outputs/mentees/[name]/profile.md` + `transformation.md`
- Liest `context/content-radar-juni-2026.md`, `reichweiten-formel-mama-identity.md`, `content-formel-5-typen.md`
- Generiert:
  - 3 Hook-Varianten (Pattern-Mix: Zeitanker · POV · Contrarian)
  - Caption mit 80/20-Struktur (Transformation/Brücke)
  - Story-Sequenz-Vorschlag (5-6 Slides) mit Brücke am Ende
  - CTA: subtil zum Network-Produkt ODER digitalen Produkt (je nach Pfad)
- Output: `outputs/mentees/[name]/content/[YYYY-MM-DD]-[thema].md`

**80/20-Regel als Pflicht-Filter:**
- Hauptteil = Mentee-Erfahrung + Mehrwert + Mini-Lesson zur Transformation
- Brücke = sanfte Überleitung zu Produkt/Empfehlung — Patricia-Frame „bei mir war"
- Verboten: „Kauf bei mir!"-Sprache, Heilversprechen, Compliance-Verstösse

## Stufe 1.5 — Leadmagnet-Builder (3-5 Tage, KW25-26)

**Ziel:** Mentee bekommt einen Lead-Magnet der die Transformation vermittelt + zum Produkt brückt

### Was zu bauen ist

- Slash-Command `/mentee-leadmagnet [name]`
- Liest `transformation.md` + Pfad-Entscheidung
- Generiert je nach Pfad:
  - **Pfad A:** Lead-Magnet → Mini-Produkt → Großkurs (Treppe)
  - **Pfad B:** Lead-Magnet → Network-Empfehlung (E-Mail-Sequenz mit Brücke)
  - **Pfad C:** Lead-Magnet als „Resonanz-Test" mit Frage am Ende: „Würdest du dazu einen Kurs kaufen?"
- Liefert: Lead-Magnet-Outline (PDF/Workbook/Mini-Video-Kurs)
- Plus: Landingpage-Text (Opt-in) + Thank-You-Text + 5-Mail-Sequenz mit Brücke
- Output: `outputs/mentees/[name]/leadmagnet/[slug]/`

## Stufe 1.7 — Content-Recycling-Maschine (2-3 Tage, KW26)

**Ziel:** 1 Transformation → 1 Woche Content (Stories + Reels + Karussell + Mails)

### Was zu bauen ist

- Slash-Command `/mentee-recycle [name] [transformation-slug]`
- Nimmt EINE Transformation-Statement
- Generiert:
  - 7 Story-Slides (über die Woche verteilt, mit unterschiedlichen Käufertypen)
  - 3 Reels-Hooks (Zeitanker · POV · Contrarian — alle mit Brücke)
  - 1 Karussell-Briefing (Listicle oder Vorher-Nachher)
  - 5 Mails (E-Mail-Sequenz mit subtiler Brücke)
- Alle Outputs lesen die Brand-Voice der Mentee + Network-Compliance-Filter
- Output: `outputs/mentees/[name]/content/week-[KW]/`

## Stufe 2 — Telegram-Bot „PIA" (10-14 Tage, KW26-28)

**Ziel:** Mentees können direkt mit PIA chatten (kein Patricia-Bottleneck mehr)

### Was zu bauen ist

- Telegram-Bot in `scripts/pia-bot/` (analog zu `cockpit-bot` und `content-companion-service`)
- Auth via Telegram-Username + Mentee-Whitelist
- 3 Hauptkommandos: `/onboard`, `/hooks`, `/plan`
- Backend: Supabase für Multi-Mentee-State

## Stufe 3 — Web-Frontend (15-20 Tage, Q3 2026)

**Ziel:** PIA als Standalone-Add-On verkaufbar (z.B. „MBA + PIA für 1290 CHF Pioneer")

### Was zu bauen ist

- Next.js-App auf `mumlifebalance.ch/pia` (oder eigene Subdomain)
- Login + Onboarding-Wizard (analog ARIA)
- Dashboard mit Content-Plan + Hooks + Funnel-Übersicht
- Stripe-Integration für Pricing
- Mentee-Profil-Editor (kann Daten nachträglich anpassen)

## Risk Register

| Risiko | Wahrscheinlichkeit | Mitigation |
|---|---|---|
| Mentee-Erwartungs-Management („PIA ersetzt Patricia") | mittel | klare Kommunikation: PIA = Werkzeug, nicht Coach |
| Memory-Pflege aufwändig | hoch | Embedding-Pipeline automatisieren ab Stufe 2 |
| Datenschutz (DSGVO bei Mentee-Daten) | hoch | Supabase EU-Region · ToS für Mentees vor Onboarding |
| Konflikt mit Mama-CEO-Pilot Energie | mittel | Stufe 0 + 1 jetzt, Stufe 2 + 3 erst nach Pilot-Abschluss |

## Erfolgs-Metriken (zum Messen)

- **Stufe 0-1:** Wie viele Pilot-Mentees nutzen es? Wie zufrieden? (Telegram-Feedback)
- **Stufe 2:** DAU/MAU der Pilot-Mentees · Hook-Quality-Rating
- **Stufe 3:** Conversion-Rate PIA-Add-On bei MBA-Käuferinnen · Churn nach 90 Tagen

## Was wir NICHT machen (Scope-Schutz)

- ❌ Kein eigener Insta-Scraper im PIA-Tool (nutzen Patricia's Apify-Pipeline)
- ❌ Keine Visual-Generation in PIA (nutzen `scripts/karussell-render/`)
- ❌ Kein eigenes Notion-Backend (Mentee bringt eigenes Notion mit oder nutzt PIA-eigene DB)
- ❌ Kein Auto-Post in Stufe 0-2 (nur in Stufe 3)
- ❌ **Kein generisches Online-Business-Tool wie ARIA** — PIA bleibt fokussiert auf Network-Mama-Hybrid-Strategie
- ❌ **Keine Branchen außerhalb Network** (kein Fitness-Coaching, kein Solopreneur-allgemein) — schützt die Positionierung

## Nächster konkreter Schritt

→ Patricia gibt Start-OK für Stufe 0 → Slash-Command `/mentee-onboard` wird gebaut in einer Session.
