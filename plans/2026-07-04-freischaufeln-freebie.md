---
tags: [produkt, funnel, freebie, freischaufeln, intern]
---

# Freischaufeln — 0€-Freebie (Web-App, Bio-Check-Zwilling)

**Datum:** 2026-07-04
**Status:** Bauplan — Patricia zur Freigabe
**Ziel:** Personalisiertes Web-Tool, das Network-Mamas ihren Familien-/Haushalts-Kram halbiert und daraus ein geschütztes **Business-Fenster** freischaufelt. Lead-Magnet der Zeit/Struktur-Treppe → führt in einen Minikurs → Mama-CEO (333) → MBA.
**Ersetzt:** das alte 12-seitige „To-Do-Liste halbieren"-Workbook (dessen Back-End — Easy Mumlife Academy 666/997, Mama Reset, 3 alte Minikurse — ist off-brand und fliegt raus).

---

## Kern-Entscheidungen (Patricia, 4.7.)

- **Name:** **Freischaufeln** (kein „KI" im Namen, kein „Powerslot")
- **Format:** echtes **KI-System** (keine Prompt-zum-Kopieren), personalisiert pro Nutzerin
- **Bau-Weg:** **Web-App wie Bio-Check** (Vercel + AC-Formular + Claude-Backend + Ergebnis-Seite)
- **Ziel-Verschiebung:** von „mehr Me-Time" → **Zeit fürs Business** (ohne Schuldgefühl)
- **Keyword:** `ZEIT` (ManyChat) · **Landing:** `mumlifebalance.ch/freischaufeln`

---

## Das Versprechen (Hero)

> „In 10 Minuten aus deinem Familien-Chaos ein echtes Zeitfenster fürs Business — ohne dass zuhause etwas liegen bleibt."

Einstieg = Schmerz (Mental Load, Liste quillt über, komme nie zum Business). Ergebnis = ein konkreter, geschützter Wochen-Block fürs Business + eine halbierte Mama-Liste.

---

## Der Ablauf (die 3 Schritte, vom System moderiert)

**0. Kurz-Intake (30 Sek, personalisiert das Ganze):**
Anzahl + Alter Kinder · Partner (und wie eingebunden) · Arbeitspensum · gewünschte Business-Stunden/Woche.

**Schritt 1 — Klarheit (das System legt vor = der Wow):**
Auf Basis des Intakes generiert das System eine **fertige, typische Haushalts-/Mama-Aufgaben-Liste für genau ihre Familiensituation** („in einer Familie wie deiner fällt üblich an: …"), sortiert nach dem **Mental-Load-Modell** (sichtbar / mental / emotional — aus Patricias Workbook). Sie liest, hakt ab, **ergänzt & streicht**, was bei ihr anders ist. Nimmt die leere-Seite-Angst, fühlt sich an, als kenne jemand ihren Alltag.

**Schritt 2 — Halbieren:**
Das System geht die Liste durch und schlägt pro Aufgabe eine Kategorie vor — **weg / delegieren / zusammenlegen / behalten** — mit konkreten Ideen (Wäsche 2× statt täglich, Einkauf online/Partner, keine 5-Sterne-Znüni-Box). Ergebnis: **halbierte Liste + Delegier-/Weg-Liste**.

**Schritt 3 — Wann, nicht alles auf einmal:**
Das System bündelt den *behaltenen* Haushalt in **feste Blöcke** („Haushalt Di + Do je 30 Min" statt über den Tag verzettelt) — und legt **aus der freigewordenen Zeit** ihr geschütztes **Business-Fenster** fest.

**Ergebnis (Deliverable):**
Ein „So sieht deine neue Woche aus"-Plan: Haushalts-Blöcke + Delegier-Liste + **dein Business-Fenster**. Screenshotbar auf der Ergebnis-Seite, optional als PDF per Mail.

**Offene Schleife → Minikurs:**
„Du hast dein Fenster — aber wie hältst du's, wenn die Woche verrücktspielt, und was machst du business-mässig genau darin? → das lernst du im Minikurs."

---

## Architektur (Bio-Check-Zwilling)

```
1. WordPress-Landing  mumlifebalance.ch/freischaufeln
   + AC-Formular (Name + E-Mail + DSGVO)   ── Keyword ZEIT / Link in Bio / DM
        │
        ▼
2. ActiveCampaign
   → Tag "Freischaufeln Lead"
   → Liste + Automation "Freischaufeln Auslieferung"
   → Mail 1: "Hier ist dein Freischaufeln-Link" (Token = Contact-Hash)
        │  User klickt Tool-Link
        ▼
3. Web-App auf Vercel  (freischaufeln.mumlifebalance.ch)
   Frontend: geführte Schritt-UI im Patricia-Brand (kein Chat-Wust, klare Schritte)
   Backend:  Vercel Function → Claude API (Sonnet) für Schritt 1+2 (Vorschlag + Kategorisierung)
   Output:   "Deine neue Woche"-Seite + optional PDF-Mail
   Pitch:    inline + Buttons → Minikurs (bzw. im Juli → MBA)
        Pitch-Klick setzt AC-Tag:
          "Freischaufeln → Minikurs-Interesse"
          "Freischaufeln → MBA-Interesse"
```

**Warum Web-App (nicht Prompt, nicht Telegram):** niedrigste Schwelle für IG-Traffic, fängt die **E-Mail als Lead** (AC), Ergebnis-Seite = Wow + Funnel-Brücke, bewährtes Bio-Check-Muster wiederverwendbar.

---

## Wiederverwendung aus Bio-Check

- Repo-Struktur `scripts/bio-check-bot/` als Vorlage → neues `scripts/freischaufeln/`
- AC-Tag-Endpoint (`api/tag.js`) fast 1:1
- Brand-CSS + Token-Link-Logik + AC-Anbindung übernehmen
- **Unterschied:** kein offener Chat, sondern **3 klare Schritte** mit KI-Vorschlägen dazwischen; Wissensbasis = das Workbook-Content (Mental-Load-Modell, Streich-Filter) statt Bio-Anatomie

---

## ActiveCampaign-Setup (neu anzulegen)

- Tag `Freischaufeln Lead` (neuer Eintrag)
- Tag `Freischaufeln abgeschlossen` (Plan generiert)
- Tag `Freischaufeln → Minikurs-Interesse`
- Tag `Freischaufeln → MBA-Interesse`
- Liste + Automation „Freischaufeln Auslieferung" (Mail 1 Link + Mail 2 Reminder — Texte liefere ich)
- ManyChat-Keyword `ZEIT` → DM mit Landing-Link

---

## Funnel-Anschluss (Julia-Treppe)

```
Freischaufeln (0€) → Minikurs "Powerslot-System" (~39) → Mama-CEO (333) → MBA
```

- **Der Minikurs existiert noch nicht.** Julia-Regel: Freebie + Minikurs fest gekoppelt, EINE offene Schleife (nicht drei wie im alten Workbook).
- **Juli:** die offene Schleife zeigt auf die **MBA** (Cart offen bis 27.7., Mama-CEO = der Zeit-Kurs steckt drin). Kein neuer Minikurs nötig, um Freischaufeln zu starten.
- **August:** den „Powerslot-System"-Minikurs (39) bauen → dann ist die Zeit-Treppe komplett und läuft evergreen (August-Motor).

---

## Phasen & Aufwand

| Phase | Inhalt | Aufwand |
|---|---|---|
| 1 | Web-App bauen (Frontend-Schritte + Claude-Backend + Ergebnis-Seite), lokal testbar | ~4–5 h Dev |
| 2 | AC-Tags via MCP + Automation-Anleitung + Mail-Texte | ~45 Min |
| 3 | WordPress-Landing `/freischaufeln` (Code liefere ich) + AC-Embed | ~1 h + Patricia einfügen |
| 4 | Vercel-Deploy + ENV + End-to-End-Test (Formular → Mail → Tool → Ergebnis → Pitch-Tag) | ~1 h |
| 5 | ManyChat `ZEIT` einrichten | ~20 Min |

**Realistische Timeline:** echter Build → Ziel **Ende Juli / Anfang August**. Für den **Juli-Feed-Block 1 (Bio-Check, 7.–18.7.)** brauchst du Freischaufeln noch nicht — der läuft mit dem fertigen Bio-Check. Freischaufeln wird das Asset für **Block 2 / August**.

---

## Offene Fragen zur Freigabe

1. **Subdomain** `freischaufeln.mumlifebalance.ch` ok? (DNS-Record)
2. **PDF ja/nein** — reicht dir die Ergebnis-Seite (screenshotbar), oder willst du zusätzlich ein PDF per Mail? (Seite allein = weniger Bau)
3. **Anthropic-Key** aus den bestehenden Bots wiederverwenden?
4. **Minikurs-Timing** — August für „Powerslot-System" bestätigt, oder willst du ihn früher?

---

## 🔗 Verwandte Notizen
- [[2026-04-23-bio-check-bot]] (Architektur-Vorlage)
- [[story-fahrplan-juli-2026]] · [[active-funnels]] (Freebie-Eintrag `todo-halbieren` → auf Freischaufeln umbenennen bei Go-Live)
