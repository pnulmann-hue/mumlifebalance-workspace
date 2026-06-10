---
tags: [funnel, links, freebies, moc]
---

# 🔗 Alle Freebie-Links — Mum Life Balance

**Stand:** 2026-06-10 · Netlify→WordPress-Migration abgeschlossen, alle Seiten live.
Single Source of Truth für alle 0€-Freebie-Landingpages + Auslieferung. Siehe auch `context/active-funnels.json`.

---

## Mentoring-Freebies (7)

| # | Freebie | WordPress-Link | ManyChat | AC-Form | Auslieferung |
|---|---------|----------------|----------|---------|--------------|
| 1 | **Bio-Check** | https://mumlifebalance.ch/bio-check | `BIO` | #47 | Bot + AC |
| 2 | **Instagram-Starterguide** | https://mumlifebalance.ch/instagram-starterguide | `SICHTBAR` / `ANLEITUNG` | #53 | AC → PDF (Drive) |
| 3 | **Story-Challenge** | https://mumlifebalance.ch/story-challenge | `STORY` | #45 | AC → PDF · **evergreen ohne Telegram**, Fragen per Mail/IG |
| 4 | **Lead-Challenge** | https://mumlifebalance.ch/lead-challenge | `LEAD` | #51 | AC → PDF + **Telegram-Kanal** |
| 5 | **Workbook „Von 0 auf echt"** | https://mumlifebalance.ch/von-0-auf-echt | `ECHT1` | #41 | AC → 25-Seiten-PDF |
| 6 | **Fahrplan (Produktposts → doppeltes Einkommen)** | https://mumlifebalance.ch/fahrplan | `SYSTEM` / `FAHRPLAN` | #49 | AC → PDF |
| 7 | **Potenzial-Test (Quiz)** | https://mumlifebalance.ch/potenzial-test | `QUIZ` | — (Jotform) | Quiz → Ergebnis direkt |

**Jotform-Quiz (Potenzial-Test):** https://eu.jotform.com/form/260726423595058

---

## PDF-/Asset-Links (für die AC-Auslieferungsmails)

| Freebie | PDF-Link | Hinweis |
|---------|----------|---------|
| Starterguide | https://drive.google.com/file/d/1AHPvD7LM8f4EtM5gF6bdhTWQNKhjvOyA/view | Drive-Freigabe „Jeder mit Link → Betrachter" prüfen |
| Fahrplan | https://docs.google.com/document/d/1EkNcSbx3nXAexoW8oqjfhQIazoDRWLsl/export?format=pdf | Direkter PDF-Export · Doc-Freigabe prüfen |
| Story-Challenge | ⏳ **fehlt noch** — Link in AC-Mail einsetzen | |
| Workbook / Lead / Bio-Check | bestehende AC-Automationen (von Patricia) | |

---

## 🔗 Bio-Link-Mapping (für `mumlifebalance.ch/bio`)

So sollen die Buttons auf der Link-in-Bio-Seite zeigen:

| Button-Text | Ziel-URL |
|-------------|----------|
| Bio-Check | https://mumlifebalance.ch/bio-check |
| Instagram-Starterguide | https://mumlifebalance.ch/instagram-starterguide |
| Story-Challenge | https://mumlifebalance.ch/story-challenge |
| Lead-Challenge | https://mumlifebalance.ch/lead-challenge |
| Workbook „Von 0 auf echt" | https://mumlifebalance.ch/von-0-auf-echt |
| Fahrplan | https://mumlifebalance.ch/fahrplan |
| Potenzial-Test | https://mumlifebalance.ch/potenzial-test |

> ⚠️ **Bekannter Bug:** Der „Starterguide"-Button auf `/bio` zeigt aktuell auf sich selbst (`/bio`) statt auf `/instagram-starterguide`. Muss korrigiert werden.

---

## Quell-Dateien im Workspace

| Freebie | Landingpage-Code |
|---------|------------------|
| Starterguide | `outputs/funnels/0-euro-starterguide/landing/` |
| Story-Challenge | `outputs/funnels/story-challenge/landing/` |
| Lead-Challenge | `outputs/funnels/lead-challenge/landing/` |
| Workbook | `outputs/funnels/workbook-von-0-auf-echt/landing/` |
| Fahrplan | `outputs/funnels/fahrplan/landing/` |
| Potenzial-Test | `outputs/funnels/potenzial-test/landing/` |

**Auslieferungsmails:** `outputs/hormozi/2026-06-10-auslieferungsmail-*.html` (Starterguide, Story-Challenge, Fahrplan)
