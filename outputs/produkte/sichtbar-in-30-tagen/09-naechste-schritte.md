---
tags: [produkt, todo]
---

# Nächste Schritte — Sichtbar in 30 Tagen

**Erstellt:** 2026-05-26
**Konzept-Status:** Komplett (Files 00-08 fertig)
**Bau-Status:** Pre-Build (keine technische Implementation gestartet)

---

## Block A — Patricia muss entscheiden (kurzfristig, diese Woche)

1. **Launch-Datum: September 2026 oder Q1 2027?**
   - September: kürzere Bauzeit (12 Wo), schnellerer Cash-In, aber Risiko von Overload neben Säule-3-Pre-Sale
   - Q1 2027: mehr Bauzeit (8 Mo), saubere Trennung, aber späteres Cash-In
   - **Empfehlung:** Q1 2027 (16.2.2027 Cohort-Start) — mehr Puffer, sauberer aufgebaut, Frühlings-Anker passt

2. **Tech-Stack: MemberPress (179$/Jahr) bestätigen oder Alternative?**
   - Wenn Alternative: „Paid Memberships Pro Free" testen, dann ggf. Premium 297$ bei Bedarf
   - Wenn MemberPress: Lizenz heute kaufen, Setup nächste Woche starten

3. **Entwicklung: Mit Claude Code (selber) oder externe Entwicklerin (5-12k CHF)?**
   - Selber: 0 CHF Cash, mehr Patricia-Zeit (~30h verteilt über 8 Wochen)
   - Extern: 5-12k CHF, weniger Patricia-Zeit (~10h Briefing + Test)
   - **Empfehlung:** Starten mit Claude Code, bei Blockern (z.B. WordPress-Plugin-Sicherheit) gezielt extern dazuholen

4. **Beta-Cohort-Grösse: 5 oder 15 Frauen?**
   - 5: intensiv, jede Frau bekommt persönliche Aufmerksamkeit
   - 15: mehr Datenpunkte, repräsentativere Bugs
   - **Empfehlung:** 8-10 Frauen (Sweet Spot — repräsentativ aber nicht überlastend)

5. **Garantie-Modell: 7-Tage-Geld-zurück oder 14-Tage-Erfolgsversprechen?**
   - 7T Geld-zurück: niedrige Refund-Wahrscheinlichkeit, klassisch
   - 14T Erfolgsversprechen: Risiko-Umkehr für Skeptische, aber Refund-Missbrauch möglich
   - **Empfehlung:** 14-Tage-Erfolgsversprechen, weil im Mid-Premium-Segment (149 CHF) Sicherheit überzeugend ist

---

## Block B — Konzept-Erweiterungen (vor Bau-Start)

Diese Punkte müssten vor dem Bau noch geklärt werden, sind aber nicht Patricia-Blocker:

6. **Wunschkundinnen-Profil-Datenbank**
   - Tag 4 sammelt Daten — wo werden die persistiert?
   - Lösung: Custom-DB-Table in MemberPress oder Tally-Embed

7. **Live-Coaching-Call-Logistik**
   - Zoom-Webinar (für mehr als 100 Teilnehmer Pflicht)
   - Hot-Seat-Anmeldung 24h vorher — wie sammeln?
   - Vermutete Cohort-Grösse: 50-150 Frauen → Zoom-Webinar-Plan (16.99 $/Mo)

8. **Affiliate-Programm bauen oder später?**
   - Empfehlung: erst Cohort 1 abwarten (Daten sammeln), dann Cohort 2 mit Affiliates

9. **doTERRA-Cross-Pollination definieren**
   - Welcher Order Bump genau?
   - Sneak-Peek-Video produzieren (1 Min)

---

## Block C — Bau-Sprints (Reihenfolge)

### Sprint 1 (KW 33-34, Aug 2026 — oder bei Q1: KW 50-51 Dez 2026)
**Foundation:**
- [ ] WordPress-Sub-Site `/sichtbar/` anlegen
- [ ] MemberPress installieren + lizenzieren
- [ ] ThriveCart-Produkt anlegen mit 3-Stufen-Preisstaffel
- [ ] ActiveCampaign-Automation-Skelett (Trigger + Wait-Loops, ohne Inhalt)
- [ ] Salespage Erst-Entwurf (via `/salespage`-Skill aus Outline)

### Sprint 2 (KW 35-36, Aug-Sep 2026 — oder Q1: KW 52-1)
**Custom-Plugin Phase 1:**
- [ ] Plugin-Boilerplate erstellen
- [ ] Profil-Scanner (höchste Priorität — wird Tag 1+5+7+30 gebraucht)
- [ ] Streak-Tracker
- [ ] Dashboard-UI

### Sprint 3 (KW 37-38, Sep 2026 — oder Q1: KW 2-3)
**Custom-Plugin Phase 2:**
- [ ] Hook-Generator (Claude-API)
- [ ] Caption-Generator
- [ ] Reel-Drehbuch-Generator
- [ ] Keyword-Generator
- [ ] Testimonial-Collector
- [ ] Zertifikat-Generator

### Sprint 4 (KW 39-40, Sep-Okt 2026 — oder Q1: KW 4-5)
**Inhalts-Befüllung:**
- [ ] 30 Tages-Videos aufnehmen (5-7 Min × 30 = ~3-4 Tage Aufnahme bei 8h/Tag)
- [ ] Schnitt + Upload
- [ ] 30 ActiveCampaign-Mails schreiben + scheduln
- [ ] Canva-Templates (20+ Designs, Patricia-Brand)
- [ ] PDFs (Workbook-Seiten pro Tag)

### Sprint 5 (KW 41-42, Okt 2026 — oder Q1: KW 6)
**Beta + Polish:**
- [ ] 8-10 Beta-Userinnen rekrutieren (kostenlos / 30 CHF)
- [ ] Beta-Cohort durchführen (30 Tage)
- [ ] Bug-Fix-Runde
- [ ] UX-Optimierungen aus Beta-Feedback
- [ ] Circle-Community-Setup
- [ ] ManyChat-Push-Flows

### Sprint 6 (KW 43-44, Okt-Nov 2026 — oder Q1: KW 7)
**Pre-Launch-Marketing:**
- [ ] Aufwärm-Content (5 Karussells + 4 Reels) produzieren
- [ ] Webinar-Slides + Aufnahme-Setup
- [ ] Salespage final (mit Beta-Testimonials)
- [ ] Mid-Launch-Webinar abhalten
- [ ] Secret Offer öffnen → Public-Launch

---

## Block D — Skill-Aufrufe (was nächste Sessions tun)

In zukünftigen Sessions kann Patricia diese Skill-Commands aufrufen, um Bestandteile zu verfeinern:

| Command | Zweck | Wann sinnvoll |
|---|---|---|
| `/salespage` | Salespage final ausformulieren | Nach Sprint 4, sobald Beta-Testimonials da sind |
| `/hormozi` Mode 7 (Landingpage) | Salespage durch Hormozi-Filter laufen lassen | Nach erstem Salespage-Draft |
| `/funnel` Mode 2 (Bauen) | Funnel-Bau im Detail (Webhooks, AC-Automations) | Sprint 1-3 |
| `/funnel` Mode 4 (Launch) | Launch-Plan operationalisieren | Sprint 5-6 |
| `/produkt` Mode 9 (KI-Assistent) | Hook-Generator-System-Prompt verfeinern | Sprint 2-3 |
| `/karussell` | Aufwärm-Karussells bauen | Sprint 6 |
| `/reels` | Aufwärm-Reels bauen | Sprint 6 |
| `/jahresplan launch sichtbar-in-30-tagen` | In Jahresplan eintragen | Nach Launch-Datum-Entscheidung |

---

## Block E — Sofortige Mini-Aktionen (heute / diese Woche)

Was Patricia in <60 Min selbst tun kann:

1. **Notion-Produkte-DB-Eintrag anlegen** (5 Min) — Block aus `08-notion-eintrag.md` kopieren
2. **Domain-Pfad reservieren** (2 Min) — `mumlifebalance.ch/sichtbar` als Weiterleitung vorbereiten
3. **Markt-Research-Lücken schliessen** (30 Min):
   - Julian Heck + Kirsten Biema + Lena Busch Preise manuell recherchieren
   - Google Trends 3 Suchbegriffe checken
4. **Wunschkundinnen-Quick-Test** (15 Min): 3 Frauen aus Warmlist fragen „Was hindert dich am täglichen Posten?"
5. **Diesen File-Set Patricia durchlesen** (45 Min) und Feedback in `09-naechste-schritte.md` ergänzen

---

## Block F — Was NICHT als nächstes machen

❌ **Nicht** Videos aufnehmen bevor Konzept finalisiert ist (Risiko: 30 Videos müssen neu, wenn Tagesreihenfolge ändert)

❌ **Nicht** ThriveCart-Produkt anlegen ohne Tech-Stack-Entscheidung (sonst Doppelarbeit)

❌ **Nicht** Aufwärm-Content posten bevor Salespage live und Cart open-bar ist

❌ **Nicht** öffentlich ankündigen bevor Beta-Cohort durch ist (Markt-Spannung aufbauen, dann sauber liefern)

❌ **Nicht** parallel Säule-3-Premium-Bundle-Launch im selben Zeitfenster (Aufmerksamkeits-Splitting)

---

## Erfolgs-Kriterien für Konzept-Phase (Stand 2026-05-26)

- [x] Markt-Research durchgeführt + Lücke identifiziert
- [x] Treppen-Position klar (B→E, CHF 149)
- [x] 30 Tagesaufgaben strukturiert
- [x] Tech-Stack designed mit Kosten
- [x] Salespage-Outline (12 Blöcke)
- [x] Launch-Kalender mit konkretem Datum
- [x] Funnel-Architektur inkl. Bridges + Bumps + Upsells
- [x] Notion-DB-Eintrag vorbereitet
- [ ] Patricia liest und gibt Feedback
- [ ] Bau-Sprints starten (nach Patricia-OK)

---

## Patricia-Feedback-Sektion

(Patricia trägt hier ihre Anmerkungen ein, bevor Bau startet)

### Was passt?

(Patricia)

### Was muss anders?

(Patricia)

### Welche Entscheidungen aus Block A werden getroffen?

(Patricia)

---

## 🔗 Verwandte Notizen

- [[00-briefing]]
- [[01-produkttreppe]]
- [[03-konzept-30-tage]]
- [[04-tech-stack-web-tool]]
- [[06-launch-kalender]]
