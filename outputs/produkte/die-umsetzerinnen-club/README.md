---
tags: [produkt]
---

# Die Umsetzerinnen — Output-Übersicht

**Status:** Konzept-Phase abgeschlossen · bereit für Patricia-Review · dann Pre-Launch
**Erarbeitet:** 2026-04-28 via `/produkt` Modus 3

---

## Struktur dieses Ordners

| # | Datei | Zweck |
|---|---|---|
| 00 | `00-briefing.md` | **Master-Briefing (v2)** — alle Konzept-Entscheidungen + Umsatz-Realitäts-Check |
| 00 | `00-markt-research.md` | Markt-Signal-Bericht (Painpoints, Wettbewerb, Benchmarks 2026) |
| 01 | `01-konzept-2-stufen.md` | Light + Bundle visualisiert (Ein-Pager für Sales-Page) |
| 02 | `02-onboarding.md` | 7-Tage-Onboarding-Flow + E-Mail-Sequenz + Patricia-DM-Vorlage |
| 03 | `03-canva-briefing/` | Folien + Sprechnotizen für Welcome-Videos + Q1-Call |
| 03a | `03-canva-briefing/onboarding-folien.md` | Lektion 0.1, 0.2, 0.3 — alle 16 Folien |
| 03b | `03-canva-briefing/q1-call-2-monat-1-funnel-optimierung.md` | Erster Lehr-Call: 20 Folien |
| 04 | `04-arbeitsblaetter/_build.py` | Python-Skript — generiert beide .docx neu (`python3 _build.py`) |
| 04 | `04-arbeitsblaetter/30-tage-sprint.docx` | Arbeitsblatt zur Lektion 0.2 *(via .gitignore — Build aus _build.py)* |
| 04 | `04-arbeitsblaetter/q1-funnel-audit.docx` | Begleit-Arbeitsblatt zum Q1-Call *(via .gitignore — Build aus _build.py)* |
| 05 | `05-ki-assistent/skalier-bot-konzept.md` | Custom GPT / Claude Project — Konzept + System-Prompt + Test-Dialoge |
| 06 | `06-bundle-funnel.md` | Bundle „Mompreneur ALL-IN" — Sales-Page-Skelett + Offer-Bumps + Upsell |
| 07 | `07-pre-launch-listen-aufbau.md` | 4-6-Wochen-Plan: Story-Sequenz · Masterclass · DM-Sprint |
| 08 | `08-soft-launch-dm-texte.md` | 10 fertige DM-Templates für die Soft-Launch-Phase |
| 09 | `09-notion-eintrag.md` | DB-Block (manuell) für beide Produkte (Membership + Bundle) |

---

## Patricia-Nächste-Schritte

### Sofort (vor Pre-Launch)
- [ ] **Lese 00-briefing.md** — Konzept-Lock?
- [ ] **Übertrage Notion-DB-Einträge** aus `09-notion-eintrag.md` in deine Produkte-DB
- [ ] **Erstelle Skalier-Bot** (Custom GPT) gemäss `05-ki-assistent/skalier-bot-konzept.md` — ~3-4 h einmalig

### Pre-Launch-Phase (Wochen -6 bis -2)
- [ ] **Story-Sequenz** posten (5 Tage, siehe `07-pre-launch-listen-aufbau.md`)
- [ ] **Masterclass-Landingpage** auf WordPress / ThriveCart bauen
- [ ] **Masterclass live** halten + Replay verfügbar
- [ ] **DM-Sprint** (7 Tage Anschreib-Challenge)

### Launch (Wochen -2 bis 0)
- [ ] **Founding-Mail** an Liste senden (Template in `08-soft-launch-dm-texte.md` Block 8)
- [ ] **Onboarding-Videos** in Canva produzieren (Briefings in `03-canva-briefing/onboarding-folien.md`)
- [ ] **Telegram-Kanal** anlegen
- [ ] **Member-Hub** in Padlet/Notion einrichten
- [ ] **ThriveCart-Subscription** anlegen für CHF 39/Monat (+ Founding-Coupon CHF 29)
- [ ] **Bundle-Sales-Page** — über `/salespage` zu 13 Blöcken ausbauen

### Live-Betrieb (ab Woche 0)
- [ ] **Erster Behind-the-Scenes-Call** durchführen
- [ ] **Erster Q1-Lehr-Call** „Funnel-Optimierung" (Briefing in `03-canva-briefing/q1-call-2-monat-1-funnel-optimierung.md`)
- [ ] **Tag-7-DMs** an alle neuen Mitglieder senden

---

## Offene strategische Aufgaben (für spätere `/produkt`-Sessions)

1. **Minikurs (B → E, 37-49 CHF) bauen** — Patricia hat aktuell keine Stufe zwischen Freebie und 333er-Kurs. Julia: „Stufe 2 zuerst" — der Minikurs ist deutlich höher priorisiert als nice-to-have.
2. **Sales-Page für Membership + Bundle** über `/salespage` zu vollständigen 13 ThriveCart-Blöcken ausbauen
3. **doTERRA-Membership-Variante** (separates Business) — basiert auf Energie-Kur als Continuity-Format
