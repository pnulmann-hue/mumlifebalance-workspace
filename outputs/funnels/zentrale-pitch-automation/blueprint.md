---
tags: [funnel, mba, pitch-automation, intern]
---

# Zentrale Pitch-Automation — Bauplan (Hybrid-Modell)

**Erstellt:** 2026-06-02
**Quelle-Recherche:** Julia-Trost-Transkripte (Funnelworkshop 20.1. / neuer Funnel, Jan 2026) + Email-Sequenz-PDF + Hormozi Copywriting-Bibel
**Modell-Entscheid Patricia (2026-06-02):** Hybrid (Freebies behalten + Julias Minikurs-Mechanik dahinter). Pitch-Ziel: beide Varianten zur Auswahl.

> ⚠️ INTERN — Mentorin-Name (Julia Trost) nie in Kundenoutput. Dieser Bauplan ist Strategie-intern.

---

## Die zwei korrigierten Grundwahrheiten (aus der Recherche)

1. **Pitch-Reihenfolge = aufsteigend (klein → gross), NICHT gross zuerst.** Sowohl Julia als auch Hormozi: erst ein kleiner Win, der ein neues Problem öffnet, das zum grossen Programm führt. Das „immer übers grosse Programm reden" gilt nur fürs Marketing-Messaging (Content/Stories/Webinar) — nicht für die Mail-Reihenfolge.
2. **Evergreen-Webinar-mit-Ads ist NICHT der aktuelle Kernweg.** In den neuesten Transkripten (Jan 2026) wird sogar von Webinar-Tools abgeraten. Der aktuelle Kern = Minikurs-Funnel. Das Webinar ist ein *optionaler* Brücken-Touchpoint, kein Pflicht-Element. Du musst nichts Neues bauen, um zu starten.

---

## Architektur (Hybrid) — so läuft's zusammen

```
                    6 FREEBIES (Top of Funnel — bleiben)
   Bio-Check · Lead-Challenge · Von 0 auf echt · Potenzial-Test
            · Starterguide · Story-Challenge
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
  LAYER 1: AUSLIEFERUNG (je 1 Automation pro Freebie)
  → Mail 1: Zugang/Freebie ausliefern + kurzes Willkommen
  → am Ende: Kontakt in die ZENTRALE Pitch-Automation übergeben
                          │
                          ▼
  LAYER 2: EINE ZENTRALE PITCH-AUTOMATION „0€ → MBA"
  → alle 0€-Leads laufen hier zusammen, egal aus welchem Freebie
  → aufsteigender Pitch (Minikurs → … → MBA)
  → EIN CTA pro Mail, alle 3-4 Tage
```

**Technisch in ActiveCampaign:**
- Jede Freebie-Auslieferungs-Automation endet mit Aktion *„Tag setzen: `0e-lead-aktiv`"* **oder** *„Zu Automation hinzufügen: Zentrale-Pitch"*.
- Die zentrale Pitch-Automation startet auf Trigger *„Tag `0e-lead-aktiv` hinzugefügt"*.
- Käufer werden per Tag aus der Sequenz genommen (Goal/Exit-Bedingung), damit niemand weiter gepitcht wird, der schon gekauft hat.

**Status Auslieferungs-Automationen (Stand heute):**

| Freebie | Keyword | AC-Automation | To-Do |
|---|---|---|---|
| Bio-Check | BIO | #58 + #59 | nur „→ Zentrale" anhängen |
| Lead-Challenge | LEAD | #47 | Inhalt prüfen + „→ Zentrale" anhängen |
| Von 0 auf echt | ECHT1 | #40 | Inhalt prüfen + „→ Zentrale" anhängen |
| Potenzial-Test | QUIZ | #52 | Inhalt prüfen + „→ Zentrale" anhängen |
| Starterguide | SICHTBAR | — | **neu bauen** (Auslieferung) |
| Story-Challenge | STORY | #45 (Anmelde) | Inhalt prüfen + „→ Zentrale" anhängen |

---

## Produkt-Treppe (Ist-Stand, Preise aus active-funnels.json)

| Stufe | Produkt | Preis |
|---|---|---|
| A (0€) | 6 Freebies | 0 |
| B | Finde dein Thema als Network-Mama | 39 |
| E | Expertin statt Verkäuferin | 97 |
| M | Instagram-Kundenmaschine / Mama-CEO | 333 (Mama-CEO Pilot 249) |
| Z | **MBA — Mum Business Academy** | 990 (Pioneer) / 1347 (Liste) |

---

## VARIANTE A — „Ziel = MBA direkt" (schnell, Julias ‚Ziel = grosser Kurs')

Die Sequenz nutzt den 39er-Minikurs als No-Brainer-Einstieg (dessen ThriveCart-Checkout via Offerbump + Upsell + Downsell ohnehin schon Richtung MBA arbeitet) und pitcht danach **direkt MBA**.

**5 Mails, alle 3-4 Tage. Jede Mail: Emotion + 1 konkreter Mehrwert-Tipp + 1 CTA.**

| # | Tag | Inhalt | CTA |
|---|---|---|---|
| 1 | 0-1 | Quick Win zum Freebie-Thema + 1 sofort umsetzbarer Tipp → sanfter No-Brainer-Pitch Minikurs „Finde dein Thema" (39) | Minikurs 39 |
| 2 | 3 | Pain-in-Moment + Mini-Tutorial → Minikurs-Dringlichkeit (Rabatt/Bonus läuft 48h) | Minikurs 39 |
| 3 | 6 | Emotionale Wende-Story (deine echte) → Brücke zum grossen Bild = MBA. Webinar-Einladung ODER MBA-Salespage | MBA / Webinar |
| 4 | 9 | MBA-Transformation + Käuferinnen-Stimmen + „für wen / für wen nicht" | MBA |
| 5 | 12 | MBA-Knappheit/Deadline + persönliches P.S. | MBA |
| Downsell | nach Nicht-Kauf | Ratenzahlung MBA ODER zurück auf 333er | MBA-Rate / 333 |

**Plus:** Preissprung 39 → 990 ist gross → Mail 3-5 müssen stark Vertrauen aufbauen (Story + Stimmen + Webinar hilft enorm).
**Minus:** weniger Zwischen-Cashflow zum Ads-Finanzieren.

---

## VARIANTE B — „Sanfte Treppe" (mehr Vertrauensaufbau + Zwischen-Cashflow)

Leads laufen erst in **EIN Mid-Offer mit Rabatt** (genau Julias Favorit), dann für Nicht-Käufer weiter zu MBA.

**Phase 1 — zentrale Sequenz (5 Mails):**

| # | Tag | Inhalt | CTA |
|---|---|---|---|
| 1 | 0-1 | Quick Win + Tipp → Minikurs „Finde dein Thema" (39) | Minikurs 39 |
| 2 | 3 | Pain + Mini-Tutorial → Minikurs-Deadline | Minikurs 39 |
| 3 | 6 | Story → Mid-Offer Mama-CEO 333 mit Rabatt (No-Brainer-Mid) | Mama-CEO 333 |
| 4 | 9 | Mama-CEO-Wert + Stimmen | Mama-CEO 333 |
| 5 | 12 | Mama-CEO-Deadline + P.S. | Mama-CEO 333 |

**Phase 2 — Anschluss-Sequenz „→ MBA" (für 333-Nicht-Käufer + als Upsell für 333-Käufer):**
Webinar-Brücke → MBA 990, 3-4 Mails.

**Plus:** sanftere Preistreppe (39 → 333 → 990), 333er-Verkäufe finanzieren Ads, mehr Vertrauen.
**Minus:** längerer Weg zum grossen Umsatz, 2 Sequenzen statt 1 (mehr Bau-Aufwand).

---

## Webinar — die Rolle (beide Varianten)

- Das Webinar ist der **Brücken-Touchpoint kurz VOR dem MBA-Pitch** — bei einem 990er-Produkt enorm hilfreich, aber **kein Blocker** für den Start.
- **Nicht zwingend evergreen-mit-Ads.** Für den Anfang reicht: MBA-Salespage direkt verlinken; Webinar später ergänzen.
- Dein Mai-Webinar pitchte den **333er (Mama-CEO)** — für MBA bräuchtest du einen angepassten Pitch (oder du nutzt es in Variante B als 333er-Brücke und baust das MBA-Webinar separat).

---

## Hormozi-Layer (gilt für jede Mail)

- **Genau 1 CTA pro Mail** (ein Verb, ein Link). Mehrere CTAs = Anti-Pattern.
- **Pain-in-Moment-Einstieg** statt Allgemeinplatz — aber Patricia-Voice (keine Stakkato, du-Anrede, Konjunktionen).
- **Downsell nur als Reaktion** auf Nicht-Kauf, nie als geplanter Standardweg.
- **EMOTION + MEHRWERT** in jeder Mail (Juni-Pflicht): berühren UND konkreten Tipp mitgeben.

---

## Offene Entscheidungen / nächste Schritte

- [ ] **Variante A oder B wählen** → dann schreibe ich die Mails aus (Brand-Voice, deutsch, ss, keine Stakkato, kein Mentorin-Name)
- [ ] Bestehende Auslieferungs-Automationen (#47/#40/#52/#45) inhaltlich in AC prüfen (kann API nicht lesen — Patricia zeigt oder bestätigt)
- [ ] Tag `0e-lead-aktiv` + Goal/Exit-Bedingung in AC anlegen
- [ ] Starterguide-Auslieferung neu bauen
- [ ] ThriveCart-Checkout der Minikurse auf Offerbump + Upsell MBA + Downsell prüfen
- [ ] (Optional, später) MBA-Webinar als Brücken-Touchpoint

---

## 🔗 Verwandte Notizen

- [[2026-06|Juni-Monatsplan]]
- [[reichweiten-formel-mama-identity]]
