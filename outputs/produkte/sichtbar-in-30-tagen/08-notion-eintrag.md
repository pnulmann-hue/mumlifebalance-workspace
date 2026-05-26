---
tags: [produkt, notion]
---

# Notion-Produkte-DB — Eintrag „Sichtbar in 30 Tagen"

**Bezug:** Notion-Produkte-DB `2ae7078e-8b7e-81ef-aafa-f03993ef344f` (siehe `context/notion-produkte-db.md`).

**Anwendung:** Diesen Block in Notion kopieren oder via Notion-MCP-API anlegen.

---

## Block zum Reinkopieren

### Properties

| Property | Wert |
|---|---|
| **Produktname** | Sichtbar in 30 Tagen |
| **Slug** | sichtbar-in-30-tagen |
| **Untertitel** | Die Posting-Challenge für Mamas, die Anfragen wollen statt Likes |
| **Typ** | Tripwire / Mid-Premium (B→E-Sprung) |
| **Business** | Mentoring (Onlinebusiness) |
| **Status** | Konzept (Pre-Build) |
| **Säule** | 1 — Networkmarketing 2.0 |
| **Themen-Achse** | T1 — Verkaufen über Instagram |
| **Zielgruppe** | NM-Mamas + Solo-Selbstständige, 30-45, inkonsistentes Posten, 0-2 Anfragen/Wo |
| **Painpoint (Hauptzitat)** | „Ich poste und niemand reagiert" |
| **Wunsch** | Sichtbar werden, Anfragen kriegen, ohne Pitchen verkaufen |
| **Sprung (Trost-Treppe)** | B → E (von „Idee" zu „erstes Angebot live + Posting-Rhythmus") |
| **Format** | Interaktives Web-Tool (WordPress + MemberPress + Custom-Plugin + 2 Live-Calls) |
| **Dauer** | 30 Tage Cohort + Lifetime-Zugang zum Tool |
| **Preis (Final)** | CHF 149 |
| **Preis (Early Bird)** | CHF 97 |
| **Preis (Secret Offer)** | CHF 67 |
| **Premium-Add-on** | + CHF 100 (15-Min-1:1-Coaching) → CHF 249 |
| **Module** | 30 Tagesmodule in 4 Wochen-Akten (Schaufenster / Hook / Gespräch / Verkaufen) |
| **Launch-Datum (Cart-Open)** | 26.8.2026 (Secret) / 29.8.2026 (Public) |
| **Cohort-Start** | 8.9.2026 |
| **Cohort-Ende** | 8.10.2026 |
| **Wiederholungs-Cohort** | März 2027 |
| **Evergreen-Modus** | Geplant ab Q1 2027 |
| **Umsatzbeitrag (realistisch erste Cohort)** | CHF 14'300 |
| **Umsatzbeitrag (pro Jahr bei 2 Cohorts + Evergreen)** | CHF 35'000 - 60'000 |
| **Beitrag zum 40k-Jahresziel** | 35-90% (Hauptträger im Mentoring-Portfolio) |
| **Anschluss-Produkt (Upsell)** | Instagram-Kundenmaschine (CHF 333, Alumni-Code 50 CHF Rabatt) |
| **ManyChat-Keyword** | SICHTBAR |
| **AC-Tag (Buyer)** | PostingChallenge-{Cohort-Bezeichnung} |
| **Salespage-URL** | mumlifebalance.ch/sichtbar |
| **Workspace-Files** | `outputs/produkte/sichtbar-in-30-tagen/` (00-09) |

### Learnings (nach Erst-Cohort zu pflegen)

(Wird nach September 2026 gefüllt)

- [ ] Tatsächliche Käufer-Anzahl Secret / EB / Final
- [ ] Completion-Rate (% die Tag 30 erreichten)
- [ ] Top 3 Drop-Off-Tage (wo gaben Frauen auf?)
- [ ] Order-Bump-Conversion-Raten (real)
- [ ] Upsell-Rate zu Instagram-Kundenmaschine
- [ ] Cohort-NPS
- [ ] Patricia-Persönliche-Learnings („Was hätte ich besser machen können")

### Notion-Relations (manuell oder via API)

- → Relation zu **Salespage-DB** (wenn vorhanden)
- → Relation zu **Content-Management-DB** (alle Aufwärm-Posts)
- → Relation zu **Wochenplanung-DB** (KW 33-36 als Launch-Wochen markieren)
- → Relation zu **Funnel-Stratege-DB** (mit Strategie-Doku verlinken)

---

## Notion-MCP-API-Aufruf (für späteren Auto-Sync)

Wenn Notion-MCP funktioniert (Tools sind verfügbar laut System-Reminder), kann der Eintrag automatisiert angelegt werden:

```javascript
// Pseudo-Aufruf, in eigenständiger Session ausführen:
mcp__notion__API-post-page({
  parent: { database_id: "2ae7078e-8b7e-81ef-aafa-f03993ef344f" },
  properties: {
    "Produktname": { title: [{ text: { content: "Sichtbar in 30 Tagen" } }] },
    "Typ": { select: { name: "Tripwire / Mid-Premium" } },
    "Status": { select: { name: "Konzept" } },
    "Preis": { number: 149 },
    "Säule": { select: { name: "1 — Networkmarketing 2.0" } },
    "Launch-Datum": { date: { start: "2026-09-08" } },
    // ... etc
  }
})
```

→ Patricia entscheidet, ob sie das manuell oder via API anlegt. Empfehlung: manuell für erste Erstellung (Notion-Property-Namen müssen exakt matchen), API für spätere Status-Updates.

---

## Status-Update-Schedule

| Datum | Status-Update |
|---|---|
| 2026-05-26 (heute) | „Konzept" |
| 2026-06-15 (nach Tech-Stack-Decision) | „In Bau" |
| 2026-08-15 (Beta-Cohort startet) | „Beta-Testing" |
| 2026-08-29 (Public-Launch) | „Im Launch" |
| 2026-10-08 (Cohort-Ende) | „Cohort 1 abgeschlossen" |
| 2027-01-01 (Evergreen-Vorbereitung) | „Im Evergreen-Aufbau" |

---

## 🔗 Verwandte Notizen

- [[00-briefing]]
- [[notion-produkte-db]]
- [[06-launch-kalender]]
