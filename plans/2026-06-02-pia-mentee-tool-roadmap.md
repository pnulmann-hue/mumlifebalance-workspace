---
tags: [plan, mba, tools]
---

# Plan · PIA — KI-Mentorin für MBA-Mentees (Roadmap)

**Erstellt:** 2.6.2026
**Patricia-OK:** „Ich find's geil" (2.6.2026)
**Status:** Roadmap festgehalten, Stufe 0 wartet auf Start-Freigabe
**Volle Konzept-Doku:** [`../reference/aria-tool-mentee-konzept.md`](../reference/aria-tool-mentee-konzept.md)

## Vision

Jede MBA-Mentee bekommt mit dem Kurs Zugang zu **PIA** (Patricia Intelligence Assistant) — eine personalisierte KI-Mentorin die das Mama-CEO-System auf ihre Situation überträgt.

Marketing-Pitch:
> „Du bekommst nicht nur den Kurs — du bekommst PIA, deine persönliche KI-Mentorin, die das Mama-CEO-System auf DEINE Situation überträgt. Während du in den Calls lernst, baut PIA mit. 24/7."

## Stufe 0 — Slash-Command `/mentee-onboard` (1 Tag)

**Ziel:** Patricia kann ab der nächsten Pilot-Mentee-Session (innerhalb dieser Woche) das Onboarding-Tool nutzen.

### Implementierungs-Schritte

1. **Skill-File anlegen:** `.claude/commands/mentee-onboard.md`
   - 35 Coaching-Fragen aus `context/patricia-vollprofil.md` extrahieren
   - In sinnvolle Sets gruppieren (z.B. 5 Sets à 7 Fragen)
   - Conversational-Flow: ein Set fragen → Antwort speichern → nächstes Set
2. **Output-Struktur:** `outputs/mentees/[mentee-slug]/profile.md`
   - YAML-Frontmatter mit Metadaten (Onboarding-Datum, MBA-Pilot-Phase, etc.)
   - Strukturierte Sektionen: Profil · Network-Firma · Zielgruppe · Säulen · Story · Produkte · Ziele · Brand-Voice · Wo-stehst-du
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
- ❌ Kein doTERRA-Profil (PIA ist Mentoring-only, doTERRA bleibt private)

## Nächster konkreter Schritt

→ Patricia gibt Start-OK für Stufe 0 → Slash-Command `/mentee-onboard` wird gebaut in einer Session.
