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

## 🔍 Live-Befund aus ActiveCampaign (Chrome-Check 2026-06-02)

**Wichtig:** Patricia hat bereits eine aufsteigende Pitch-Kette gebaut — der MBA fehlt nur als Spitze.

Beispiel **„Von 0 auf echt" (#40)** — kompletter Flow:
```
Trigger Formular „Von 0 auf echt"
 → interne Benachrichtigung info@mumlifebalance.ch
 → AUSLIEFERUNG „Hier ist dein Workbook" (5 gesendet · 60% Öffnung · 60% Klick)
 → 1 Std warten → Tag „Automation Finde dein Thema"  → startet Funnel #53 (39)
 → 5 Tage warten → Tag „Automation IG Kundenmaschine" → startet Funnel #54 (333)
 → 7 Tage warten → Tag „Automation Expertin statt Verkäuferin" → startet Funnel #55 (97)
 → Automation endet
```

**Erkenntnisse:**
- Auslieferung + aufsteigender Pitch (39 → 333 → 97) sind schon da — das ist faktisch **Variante B in Teilen gebaut**.
- Die eigentlichen Pitch-Mails liegen in den Unter-Funnels **#53 / #54 / #55** (per Tag angestossen) — noch nicht inhaltlich geprüft.
- **MBA (997) kommt nirgends vor** → das ist die Hauptlücke.
- „Kurs-gekauft"-Ziele existieren bereits (Finde dein Thema = 540 · IG-Kundenmaschine = 562 · Expertin = 571) → Exit-bei-Kauf im Ansatz vorhanden.
- Konsequenz: **erweitern + bündeln** statt neu bauen — MBA als Spitze, dann zentralisieren.

**Verfügbare AC-Listen (für den Build):** doTERRA Interessenten (18), doTERRA Kunden (20), Kunden (16), Many-Chat Kontakte (23), Quiz-Kontakte (24), Regulärer Newsletter/Interessenten (2), Willkommenssequenz (3), Masterclass (19), Master SMS (22).

---

## Produkt-Treppe (Ist-Stand, Preise aus active-funnels.json)

| Stufe | Produkt | Preis |
|---|---|---|
| A (0€) | 6 Freebies | 0 |
| B | Finde dein Thema als Network-Mama (Minikurs) | 39 |
| Mittel | **3 grössere Kurse — je ein eigenes Thema** | je ~333 |
| · | Instagram-Kundenmaschine (Instagram → Kunden) | 333 |
| · | Digitale Produktwelt (eigenes Produkt erstellen) | 333 |
| · | Mama-CEO (Business neben Familie, 5 Säulen) | 333 |
| Z | **MBA — Mum Business Academy = BUNDLE über allen dreien** | 997 (Pioneer) / 1347 (Liste) |

> **Bestätigt 2026-06-02:** MBA ist das Bundle, das alle 3 grösseren Kurse abdeckt. Die 3 Kurse lösen je *ein* Problem → eignen sich perfekt als **gezielter Downsell** (je nach Einstiegs-Freebie/Pain), nicht als stumpfe Preistreppe.

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

**Plus:** Preissprung 39 → 997 ist gross → Mail 3-5 müssen stark Vertrauen aufbauen (Story + Stimmen + Webinar hilft enorm).
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
Webinar-Brücke → MBA 997, 3-4 Mails.

**Plus:** sanftere Preistreppe (39 → 333 → 997), 333er-Verkäufe finanzieren Ads, mehr Vertrauen.
**Minus:** längerer Weg zum grossen Umsatz, 2 Sequenzen statt 1 (mehr Bau-Aufwand).

---

## VARIANTE C — „Hoch ankern, dann gezielt downsellen" (Patricias Idee, empfohlen)

Nutzt aus, dass MBA das **Bundle über den 3 Kursen** ist: erst die Komplettlösung pitchen, wer die nicht will, kriegt den **einen** Kurs, der zu seinem Pain passt (Anker-Effekt — nach 997 wirken 333 klein).

```
Freebie (0€) → ① Mehrwert (1-2 Mails) → ② Minikurs 39 (Win)
   → ③ MBA 997 (grosser Pitch + Webinar-Brücke)
   → ④ kein MBA? Downsell auf den EINEN passenden Kurs:
        BIO / LEAD / STORY   → Instagram-Kundenmaschine 333
        QUIZ / ECHT1         → Digitale Produktwelt 333
        Zeit / Familie       → Mama-CEO 333
```

**5-6 Mails, alle 3-4 Tage. Jede Mail: Emotion + 1 konkreter Tipp + 1 CTA.**

| # | Tag | Inhalt | CTA |
|---|---|---|---|
| 1 | 0-1 | Quick Win zum Freebie-Thema + 1 sofort umsetzbarer Tipp | (kein Pitch, nur Mehrwert) |
| 2 | 3 | Pain-in-Moment + Mini-Tutorial → No-Brainer Minikurs „Finde dein Thema" 39 | Minikurs 39 |
| 3 | 6 | Emotionale Wende-Story → das grosse Bild = MBA. Webinar-Einladung ODER MBA-Salespage | MBA / Webinar |
| 4 | 9 | MBA-Transformation + Käuferinnen-Stimmen + „MBA = alles aus einer Hand" | MBA |
| 5 | 12 | MBA-Deadline/Knappheit + P.S. | MBA |
| 6 (Downsell) | 15 | „MBA zu viel? Dann starte mit dem, was dich JETZT am meisten drückt" → der EINE getaggte Kurs | passender 333er |

**Diagnose-Downsell automatisch über AC-Tags:** Das Einstiegs-Freebie verrät den Pain → AC lenkt Mail 6 auf den passenden Kurs. Kein Auswahl-Überfluss (Hormozi: 1 Angebot, 1 CTA).

**Plus:** ankert hoch, schnell beim grossen Umsatz, nutzt die Bundle-Logik elegant.
**Minus:** Sprung 39 → 997 ist gross → **Webinar-Brücke vor dem MBA-Pitch hier fast Pflicht**.

---

## Was passiert am Ende, wenn nichts gekauft wurde (gilt für alle Varianten)

```
④ Downsell auch nicht gekauft?
   → ⑤ EXIT: Tag „pitch-durchlaufen-kein-kauf"
        → ALLGEMEINER VERTEILER (der „grosse Topf"):
           • laufende Mehrwert-Mails
           • Reichweiten-Posts holen weiter nach
           • PITCH-MAILS bei jedem LAUNCH (MBA-Cart, Aktionen) an die GANZE Liste
   → ⑥ periodisch (quartalsweise) RE-ENGAGEMENT + BEREINIGUNG:
        Nicht-Öffner reaktivieren → wer tot bleibt: raus (Zustellbarkeit + Kosten)
```

**Kernpunkt:** Der automatisierte Funnel endet, der **Verteiler ist endlos**. Genau das ist Patricias Juni-Plan — „viele Menschen rein, denen ich bei jedem Launch die Pitchmails schicke". Die meisten kaufen nicht beim ersten Kontakt, sondern beim dritten/fünften. Bereinigung schützt Zustellbarkeit + AC-Kosten (AC-Funktionen: Nicht-Öffner + inaktive Kontakte finden).

---

## Webinar — die Rolle (alle Varianten)

- Das Webinar ist der **Brücken-Touchpoint kurz VOR dem MBA-Pitch** — bei einem 997er-Produkt enorm hilfreich, aber **kein Blocker** für den Start.
- **Nicht zwingend evergreen-mit-Ads.** Für den Anfang reicht: MBA-Salespage direkt verlinken; Webinar später ergänzen.
- Dein Mai-Webinar pitchte den **333er (Mama-CEO)** — für MBA bräuchtest du einen angepassten Pitch (oder du nutzt es in Variante B als 333er-Brücke und baust das MBA-Webinar separat).

### Live → Evergreen (der schlaue Doppel-Nutzen, Patricia 2026-06-02)

Das **Live-Webinar im MBA-Launch wird aufgezeichnet** und danach als **Evergreen-Webinar** im Funnel eingesetzt. Ein Dreh, zwei Funktionen: Launch-Event + dauerhaftes Funnel-Asset.

```
LIVE-Webinar im MBA-Launch  →  aufzeichnen
        ↓
Aufzeichnung = Evergreen-Webinar im Funnel
(Mail 3 Variante C / Mail 6 Variante B)
```

**Warum Live zuerst:** echte Fragen, echte Einwände, echte Energie. Genau die Live-Reaktionen machen die Aufzeichnung später stark — besser als ein am Schreibtisch geskriptetes Webinar.

**3 Punkte beim Umbau Live → Evergreen:**
1. **Harte Launch-Daten raus.** „Cart schliesst Sonntag" / „heute Abend Schluss" stimmt evergreen nicht mehr → Stellen rausschneiden ODER den Pitch-Teil am Ende sauber neu aufnehmen und dranhängen.
2. **Eigene Dringlichkeit für Evergreen.** Ohne Live-Cart-Close → **rollende Frist ab Eintritt** (z.B. Bonus/Preisvorteil läuft 72h nach dem Anschauen ab). Technisch via ThriveCart-Countdown oder Deadline-Tool, kein WebinarJam nötig.
3. **Preis im Evergreen-Pitch anpassen.** Launch = Pioneer 997. Nach Pioneer-Phase = 1347 ODER ein eigenes Evergreen-Angebot festlegen — sonst verspricht die Aufzeichnung einen Preis, den es nicht mehr gibt.

**Link-Swap statt Mail-Umschreiben:** In beiden Sequenzen steht der Platzhalter `[WEBINAR-LINK]`. Während des Launches → Live-Anmeldung. Danach → Replay-Seite. Die Mails bleiben Wort für Wort gleich.

**Idealer Aufnahme-Zeitpunkt:** der MBA-Launch selbst. Danach steht das Evergreen-Asset fertig.

---

## Hormozi-Layer (gilt für jede Mail)

- **Genau 1 CTA pro Mail** (ein Verb, ein Link). Mehrere CTAs = Anti-Pattern.
- **Pain-in-Moment-Einstieg** statt Allgemeinplatz — aber Patricia-Voice (keine Stakkato, du-Anrede, Konjunktionen).
- **Downsell nur als Reaktion** auf Nicht-Kauf, nie als geplanter Standardweg.
- **EMOTION + MEHRWERT** in jeder Mail (Juni-Pflicht): berühren UND konkreten Tipp mitgeben.

---

## Offene Entscheidungen / nächste Schritte

- [ ] **Variante B oder C wählen** (A = direkt-MBA ohne Diagnose-Downsell ist abgehängt) → dann schreibe ich die Mails aus (Brand-Voice, deutsch, ss, keine Stakkato, kein Mentorin-Name)
- [ ] Bestehende Auslieferungs-Automationen (#47/#40/#52/#45) inhaltlich in AC prüfen (kann API nicht lesen — Patricia zeigt oder bestätigt)
- [ ] Tag `0e-lead-aktiv` + Goal/Exit-Bedingung in AC anlegen
- [ ] Starterguide-Auslieferung neu bauen
- [ ] ThriveCart-Checkout der Minikurse auf Offerbump + Upsell MBA + Downsell prüfen
- [ ] **MBA-Launch-Webinar aufzeichnen** → danach als Evergreen umbauen (Launch-Daten raus, rollende Frist, Preis anpassen) + `[WEBINAR-LINK]` auf Replay-Seite umstellen
- [ ] (Optional, später) MBA-Webinar als Brücken-Touchpoint

---

## 🔗 Verwandte Notizen

- [[2026-06|Juni-Monatsplan]]
- [[reichweiten-formel-mama-identity]]
