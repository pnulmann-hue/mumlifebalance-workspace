---
tags: [produkt, tech, web-tool]
---

# Tech-Stack: Wie das Web-Tool gebaut wird

**Kontext:** Patricia hat in der Variante-Entscheidung „Vollinteraktives Web-Tool" gewählt. Dieser File legt fest, welche Bausteine das Tool braucht, was sie kosten und in welcher Reihenfolge sie gebaut werden.

---

## Architektur-Übersicht

```
┌──────────────────────────────────────────────────────────────┐
│                        TEILNEHMERIN                          │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────┐
│             WordPress (mumlifebalance.ch/sichtbar)            │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  MemberPress (Auth + Drip-Content + Membership-Zonen)  │  │
│  │  ├─ Tages-Module (30 Lessons mit Drip-Schedule)        │  │
│  │  ├─ Progress-Tracker (built-in)                        │  │
│  │  └─ Streak-Logik (Custom-Field via WP-CodeSnippets)    │  │
│  └────────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  Custom-Plugin: „sichtbar-tools"                       │  │
│  │  ├─ Profil-Scanner (12-Fragen-Quiz + Score-Logik)      │  │
│  │  ├─ Hook-Generator (Claude-API-Aufruf)                 │  │
│  │  ├─ Caption-Generator (Claude-API)                     │  │
│  │  ├─ Reel-Drehbuch-Generator (Claude-API)               │  │
│  │  ├─ Keyword-Generator (Claude-API)                     │  │
│  │  ├─ Testimonial-Collector (Tally-Embed)                │  │
│  │  └─ Zertifikat-Generator (PDF via DomPDF)              │  │
│  └────────────────────────────────────────────────────────┘  │
└────┬─────────────────┬──────────────┬──────────────┬─────────┘
     │                 │              │              │
     ▼                 ▼              ▼              ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ ThriveCart  │ │ActiveCamp.  │ │  ManyChat   │ │   Circle    │
│ (Checkout)  │ │(30 Daily-   │ │(Push 10:00  │ │(Community + │
│             │ │  Mails)     │ │ + 21:00)    │ │  Coaching)  │
└─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘
                         │
                         ▼
                  ┌─────────────┐
                  │ Claude API  │
                  │ (Anthropic) │
                  └─────────────┘
```

---

## Komponenten im Detail

### 1. WordPress (Foundation)

**Bereits vorhanden:** mumlifebalance.ch läuft auf WordPress. Patricia hat Admin-Zugriff. CLI-Helper `scripts/wordpress/wp-api.js` existiert.

**Was zu tun ist:**
- Neue Sub-Site oder Unterseite: `mumlifebalance.ch/sichtbar/`
- Theme-konform: Patricia-Brand (Petrol/Creme + Philosopher/Source Sans 3)
- Login-geschützter Bereich (via MemberPress)

**Kosten:** 0 € (vorhanden)

---

### 2. MemberPress (Membership + Drip-Content)

**Warum MemberPress statt LearnDash?**

| Feature | MemberPress | LearnDash |
|---|---|---|
| Drip-Content (zeitgesteuert) | ✅ Built-in | ✅ |
| Stripe / PayPal-Integration | ✅ | ✅ |
| Quiz-Builder | ❌ (nicht im Core) | ✅ |
| Course-Format | ✅ via Courses-Add-on | ✅ Native |
| Affiliate-Marketing | ✅ via MemberPress Affiliates | ❌ (extra) |
| ActiveCampaign-Sync | ✅ via Integration | ✅ |
| Preis (Plus-Plan) | **179 $/Jahr** | 199 $/Jahr |
| Patricia hat es schon? | **Nein** | Nein |

**Empfehlung: MemberPress Plus** (179 $/Jahr ≈ CHF 165) — wegen Affiliate-Marketing-Built-in für späteren Affiliate-Aufbau und bessere AC-Integration. Quiz-Funktionalität bauen wir custom (Tally-Embed reicht).

**Alternative-Pfad (wenn Patricia später nicht 179$ jährlich zahlen will):**
- **MemberMouse Lite** (gratis, einfacher)
- **Restrict Content Pro** (99 $ Jahr)
- **Paid Memberships Pro** (Free / 297$ für Premium)

**Was zu tun ist:**
- MemberPress installieren + lizenzieren
- „Sichtbar in 30 Tagen"-Membership-Level anlegen
- 30 Lessons als Drip-Content anlegen (Tag X = Tag X-1 + 24h freigeschaltet)
- ThriveCart als Checkout via Webhook anbinden (Buyer-Tag in MemberPress importieren)

**Kosten:** **179 $/Jahr** (≈ CHF 165)

---

### 3. ThriveCart (Checkout)

**Bereits vorhanden** (Patricia nutzt es für alle Kurse).

**Was zu tun ist:**
- Neues Produkt „Sichtbar in 30 Tagen" anlegen
- 3-Stufen-Preisstaffel: Secret 67 / EB 97 / Final 149 (zeitlich gesteuert)
- Premium-Add-on als Order-Bump: +100 CHF (15-Min-Coaching-Slot)
- Upsell-Page nach Kauf: Instagram-Kundenmaschine mit Alumni-Discount

**Kosten:** 0 € (vorhanden)

---

### 4. ActiveCampaign (Daily-Mail-Sequenz)

**Bereits vorhanden** (Patricia hat AC + Automatisierungen).

**Was zu tun ist:**
- 30 Tages-Mails erstellen (eine pro Tag, geht um 06:00 raus)
- Automation „Posting-Challenge Cohort September 2026":
  - Trigger: ThriveCart-Tag „PostingChallenge-Sep2026"
  - Wait until Start-Datum (z.B. 8.9.2026 06:00)
  - Send Day-1-Email
  - Wait 24h
  - Send Day-2-Email
  - ... × 30
- Bei Streak-Drop (3 Tage kein „fertig"-Klick): Rückhol-Mail mit Patricia-Voice

**Kosten:** 0 € (vorhanden)

---

### 5. ManyChat (Daily-Push-Reminder)

**Bereits vorhanden** (Patricia nutzt für alle Funnels).

**Was zu tun ist:**
- Opt-in beim Tool-Onboarding („Möchtest du tägliche Erinnerungen via WhatsApp/Instagram-DM?")
- Daily-Push um 10:00: „Heute ist Tag X. Bereit?"
- Streak-Warning um 21:00: „Du hast Tag X noch nicht abgehakt — 10 Min reichen"

**Kosten:** 0 € (vorhanden)

---

### 6. Circle (Community)

**Geplant** für Premium-Bundle (siehe `saeulen-mentoring.md`) — Posting-Challenge kann es als erste echte Anwendung nutzen.

**Was zu tun ist:**
- Circle-Workspace anlegen (oder mit Premium-Bundle-Workspace teilen mit Sub-Spaces)
- 5 Räume: Tagesreflexionen / Hook-Battle / Feedback / Wins / Patricia antwortet
- Cohort-Frauen werden via API/Webhook nach ThriveCart-Kauf eingeladen

**Kosten:** **89 $/Monat** Basic-Plan (≈ CHF 82) — fällt sowieso für Premium-Bundle an, also nicht extra zurechenbar

---

### 7. Custom-Plugin „sichtbar-tools" (das Herzstück)

**Das ist die eigentliche „Interaktivität"** — ein eigenes WordPress-Plugin mit 6 Sub-Modulen.

#### 7.1 Profil-Scanner

**Logik:**
- 12-Fragen-Quiz mit gewichteten Antworten
- Score-Berechnung 0-100 nach 6 Pflicht-Kriterien (Bio-Klarheit / Highlights / Gepinnte / Konsistenz / Hook-Qualität / CTA-Vorhandensein)
- Speichert Score pro Tag (Tag 1, 5, 7, 30) in Custom-DB-Table
- Vorher-Nachher-Graph in Dashboard

**Tech:** PHP/WordPress + Chart.js für Visualisierung. Daten in Custom-Table `wp_sichtbar_scores`.

**Bauzeit:** 2-3 Tage.

#### 7.2 Hook-Generator (Premium-Feature, Tag 9)

**Logik:**
- User-Input: Hauptthema + Hook-Kategorie-Wunsch (oder „alle 8")
- Wunschkundin-Daten aus DB werden mit-injiziert
- Claude-API-Aufruf mit Patricia-System-Prompt (Brand-Voice + 8 Hook-Kategorien + Blackliste)
- Output: 10 Hooks im UI

**System-Prompt-Skizze:**
```
Du bist Patricias Content-Assistent. Du generierst Instagram-Hooks
für ihre Posting-Challenge-Teilnehmerin.

Patricias 8 Hook-Kategorien: [Liste]
Patricias Brand-Voice: [aus brand-voice.md]
KI-Phrasen-Blackliste: [Pflicht-Check]

Teilnehmerin-Daten:
- Thema: {thema}
- Wunschkundin: {wunschkundin}
- Expertensatz: {expertensatz}

Generiere 10 Hooks (je 1 pro Kategorie wenn möglich) für ein
Karussell zu „{thema}". Max 12 Wörter pro Hook.
```

**Tech:** PHP-Backend ruft Claude-API auf (curl), zeigt Output via Vanilla-JS im Frontend. API-Key in WP-Options (verschlüsselt).

**Kostenkontrolle:** 5 Generierungen pro Teilnehmerin pro Tag (Soft-Limit). Bei 150 Teilnehmerinnen × 5 × 30 Tage = max 22'500 API-Calls × ~$0.01 (Claude Sonnet 4.6 input/output ≈ 500 tokens) = **max $225 pro Cohort**.

**Bauzeit:** 3-4 Tage.

#### 7.3 Caption-Generator

**Logik:** Analog Hook-Generator, aber mit 5-Strukturen-Caption-Formeln + Story-Input.

**Bauzeit:** 1 Tag (Wiederverwendung Hook-Generator-Struktur).

#### 7.4 Reel-Drehbuch-Generator

**Logik:** 15-Sek-Talking-Head-Skripte. Input: Hook + Body-Tipp. Output: 3 verschiedene Drehbücher mit Sekunden-Marken.

**Bauzeit:** 1 Tag.

#### 7.5 Keyword-Generator

**Logik:** Schlägt 5 ManyChat-Keywords zum Hauptthema vor, plus Beispiel-Bot-Antworten.

**Bauzeit:** 0.5 Tage.

#### 7.6 Testimonial-Collector

**Logik:** Embedded Tally-Form mit personalisierten Feldern (Name der Teilnehmerin im Pre-Fill). Antworten landen in WP-Datenbank.

**Bauzeit:** 0.5 Tage (Tally hostet das Form).

#### 7.7 Zertifikat-Generator

**Logik:** Tag 30 → Klick → DomPDF generiert PDF mit Patricia-Brand, Teilnehmerin-Name, Final-Score, Datum.

**Bauzeit:** 0.5 Tage.

---

## Optional aber empfohlen: Streak-Tracker / Dashboard

**Logik:**
- Tages-Klicks („Heute fertig") in Custom-DB-Table
- Dashboard zeigt: aktueller Streak (X Tage in Folge) + Gesamt-Streak (X von 30 abgehakt)
- Badges für Meilensteine (7 / 14 / 21 / 30)
- Optional: Wochen-Leaderboard in Circle für Gamification

**Bauzeit:** 2 Tage.

---

## Gesamt-Bauzeit-Schätzung

| Komponente | Bauzeit |
|---|---|
| MemberPress-Setup + 30 Lessons anlegen (Templates) | 3 Tage |
| ThriveCart-Setup + 3-Stufen-Preis | 0.5 Tage |
| ActiveCampaign 30 Daily-Mails | 5 Tage (Schreiben + Aufsetzen) |
| ManyChat-Push-Flows | 1 Tag |
| Circle-Setup | 1 Tag |
| Custom-Plugin (alle 7 Module) | **9-10 Tage** |
| 30 Tages-Videos (Patricia spricht) | **10-15 Tage** (5-7 Min pro Video × 30 = ~6h Aufnahme + Schnitt) |
| Templates-Bibliothek (Canva) | 3 Tage |
| Salespage | 2 Tage |
| Test + Bug-Fix mit Beta-Cohort | 5 Tage |
| **Gesamt** | **~40 Tage** (8 Wochen Volltime / 16 Wochen halbtags) |

---

## Kosten-Übersicht (laufend pro Jahr)

| Komponente | Kosten |
|---|---|
| MemberPress Plus | CHF 165/Jahr |
| Claude API (max 4 Cohorts à 150 Frauen) | CHF ~1'000/Jahr |
| Circle | CHF 985/Jahr (sowieso für Premium-Bundle geplant — nicht extra) |
| ThriveCart, ActiveCampaign, ManyChat, WordPress | 0 (vorhanden) |
| **Total NEUE Kosten** | **~CHF 1'165/Jahr** |

**Einmalig:**
- Plugin-Entwicklung (extern): wenn Patricia es coden lässt → CHF 5'000-12'000 (je nach Entwicklerin)
- Plugin-Entwicklung (mit Claude Code): CHF 0 — aber Patricia muss testen + Bugs reporten
- Video-Aufnahmen (Selbstdreh): 0
- Canva-Templates: 0 (Canva-Pro hat Patricia)

**Break-Even:** Bei CHF 149 Final-Preis = **8 Käuferinnen** decken die Jahreskosten. Realistisch ab 50+ Käuferinnen pro Cohort = klar profitabel.

---

## Build-Reihenfolge (Sprint-Plan)

### Sprint 1 (Wochen 1-2): Foundation
- WordPress-Setup `/sichtbar/`
- MemberPress installieren + 30 Leer-Lessons anlegen
- ThriveCart-Produkt + 3-Stufen-Pricing
- ActiveCampaign-Automation-Skelett

### Sprint 2 (Wochen 3-4): Custom-Plugin
- Plugin-Boilerplate
- Profil-Scanner
- Hook-Generator (das wichtigste KI-Feature zuerst)
- Streak-Tracker

### Sprint 3 (Wochen 5-6): Inhalts-Befüllung
- 30 Tages-Videos aufnehmen + schneiden
- 30 ActiveCampaign-Mails schreiben
- Templates-Bibliothek (Canva)
- Restliche Plugin-Module (Caption / Reel / Keyword / Testimonial / Zertifikat)

### Sprint 4 (Wochen 7-8): Polish + Beta
- Beta-Cohort mit 5-10 Frauen (gratis / 30 CHF Beta-Preis)
- Bug-Fix-Runde
- Salespage finalisieren
- ManyChat + Circle integrieren

### Sprint 5 (Wochen 9-10): Launch
- Aufwärm-Content (2 Wochen vor Launch)
- Webinar (Tag -3)
- Cart-Open (7 Tage)
- Cohort-Start

---

## Risiken & Mitigation

| Risiko | Wahrscheinlichkeit | Mitigation |
|---|---|---|
| **Claude-API-Kosten explodieren** | Mittel | Soft-Limit 5 Generierungen/Tag/User · Caching wiederkehrender Themen · Quartals-Review |
| **MemberPress-Bugs** | Niedrig | Beta-Cohort testet ausgiebig vor Public-Launch |
| **Patricia hat keine Zeit für 30 Videos** | Hoch | Realistisch: max 3 Tage à 10 Videos = 6h Aufnahme pro Tag. Lieber 30 Tage à 1 Video pro Tag bauen, dann erst launchen |
| **Circle-Lernkurve für Teilnehmerinnen** | Mittel | Onboarding-Video Tag 1 erklärt Circle in 3 Min |
| **Beta-Cohort findet kritische UX-Probleme** | Hoch erwünscht | 5 Frauen freiwillig, bekommen lebenslangen Zugang + späteren 1:1-Call |

---

## Was Patricia entscheiden muss

1. **MemberPress Plus (179$/Jahr) okay?** Oder günstigere Alternative (z.B. Paid Memberships Pro Free)?
2. **Eigene Entwicklung mit Claude Code** oder **externe Entwicklerin** (CHF 5-12k)?
3. **Claude-API-Account auf Anthropic** anlegen — Patricia muss Zahlungsmittel hinterlegen (auf Pay-as-you-go läuft das nicht ohne Karte)
4. **Beta-Cohort-Grösse:** 5 Frauen (klein, intensiv) oder 15 (mehr Datenpunkte, mehr Aufwand)?
5. **Erst-Launch-Datum:** September 2026 realistisch? Falls nicht: Q1 2027 mit 12 Wochen Bauzeit als Puffer.

---

## 🔗 Verwandte Notizen

- [[00-briefing]]
- [[03-konzept-30-tage]]
- [[06-launch-kalender]]
