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
> „Die erste KI-Mentorin SPEZIELL für Mamas im Network. Patricia hat 10+ Jahre Network-Erfahrung + KI-Stack reingebaut. PIA versteht Crossline-Situationen, Team-Aufbau, Compliance-Regeln deiner Firma und Mama-Realität — generische KI-Tools verstehen das nicht."

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

## Stufe 1 — Hook-Generator (5-7 Tage, KW24-25)

**Ziel:** Aus Mentee-Profil + Patricia-Pattern-Wissen → 3 Hook-Varianten pro Post

### Was zu bauen ist

- Slash-Command `/mentee-hooks [name] [thema]`
- Liest `outputs/mentees/[name]/profile.md`
- Liest `context/content-radar-juni-2026.md` für Pattern-Liste
- Liest `context/reichweiten-formel-mama-identity.md` + `context/content-formel-5-typen.md`
- Generiert 3 Hook-Varianten in unterschiedlichen Pattern (z.B. Zeitanker · POV · Contrarian)
- Output: `outputs/mentees/[name]/hooks/[YYYY-MM-DD]-[thema].md`

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
