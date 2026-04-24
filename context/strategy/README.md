# context/strategy/ — Ingest-Regeln & Scope-Trennung

> **Kritisch:** Das Team hat Zugriff auf `bot.mumlifebalance.ch`. Daher strikte Trennung.
> **Zusätzlich kritisch:** Der Bot ist **doTERRA-only** — Patricias Mentoring-Business und Gesamt-Umsatzplanung gehört NIEMALS rein.

## Drei-Ebenen-Struktur

```
context/strategy/
├── README.md                                     # diese Datei
├── public/                                        # ✅ wird in Bot-RAG ingestet (category='strategy-public')
│   └── doterra-positionierungs-framework.md      # Scope-Prefix 'doterra-' im Dateinamen
│                                                  # + YAML-Frontmatter `scope: doterra`
│
└── private/                                       # ❌ NIE im Bot-RAG
    ├── bot-doterra/                               # → Patricias private doTERRA-Planung
    │   └── README.md                              # Bot liest via Notion-Tools direkt,
    │                                                sobald Zugriff auf doTERRA-DB geklärt
    └── leaderin-gesamt/                           # → Patricias Gesamt-Business (alle Säulen)
        ├── 2026-leaderin-strategie.md
        └── positionierungs-framework-mentoring.md # NICHT für doTERRA-Bot
```

## Namens- und Scope-Konvention für `public/`

**Regel:** Jede Datei in `public/` MUSS einen expliziten Scope-Prefix im Dateinamen haben:

| Prefix | Scope | Beispiel |
|---|---|---|
| `doterra-` | doTERRA-Beraterinnen (aktuell einziger Bot-Scope) | `doterra-positionierungs-framework.md` |

**Zusätzlich:** Jede `public/`-Datei MUSS ein YAML-Frontmatter-Header haben mit:
```yaml
---
scope: doterra
ingest_category: strategy-public
bot_audience: doterra-beraterinnen
NOT_for: mentoring, kurse, 1zu1, gesamt-business
---
```

Das erlaubt dem Ingest-Job und dem Bot-System-Prompt, **explizit** zu filtern: „Nur Dokumente mit `scope: doterra` heranziehen, wenn die Anfrage im doTERRA-Kontext steht."

## Drei Scopes, klar getrennt

| Scope | Inhalt | Wer sieht's |
|---|---|---|
| **Public (doTERRA-Team)** | doTERRA-Methodik, Regenerations-Positionierung, Coaching-Framework im doTERRA-Kontext | Team (Companion-Bot) + Patricia |
| **Private Bot-doTERRA** | Patricias eigene doTERRA-Zahlen, Gold-Plan, OV, Legs, Direktkunden | 🔒 Patricia (via Telegram-Bot) |
| **Private Leaderin-Gesamt** | Mentoring-Strategie, Kurs-Launches, 40k-Umsatzplanung über alle Säulen | 🔒 Patricia (NIE im Bot) |

## Faustregeln

- **`public/`** — doTERRA-Frameworks und Methodik. Nie Zahlen.
- **`private/bot-doterra/`** — doTERRA-spezifische private Daten (Rang, OV, Team). Werden vom Bot **nicht via RAG** gelesen, sondern **direkt via Notion-API** (strikt scoped auf Patricia).
- **`private/leaderin-gesamt/`** — Alles, was **nicht doTERRA** ist: Mentoring-Business, Kurse, 1:1, Gesamt-Umsatzziele. Darf den Bot nie berühren.

## Für den Ingest-Job (`scripts/ingest-business.ts` im `doterra-bot` Repo)

Pflegt nur Dateien ein, die **alle folgenden Kriterien** erfüllen:

1. Liegen in `context/strategy/public/`
2. Dateiname beginnt mit einem erlaubten Scope-Prefix (aktuell: `doterra-`)
3. YAML-Frontmatter vorhanden mit `scope: doterra` und `ingest_category: strategy-public`
4. Gesetzte Metadaten werden als Kategorie gespeichert (`documents.category='strategy-public'` + `documents.scope='doterra'`)

Alles andere (auch `public/*.md` ohne Prefix/Frontmatter) wird **übersprungen**. `private/` wird **komplett ausgeschlossen** (beide Unterordner).

## Bot-Verhalten (Phase B — RAG-Query)

Der Bot-System-Prompt erweitert den RAG-Filter um den Scope-Check:

```sql
SELECT * FROM documents
WHERE category IN ('product', 'business', 'strategy-public')
  AND (scope IS NULL OR scope = 'doterra')
```

So zieht der Bot **niemals** Strategie-Dokumente heran, die nicht für doTERRA ausgewiesen sind — selbst wenn sie versehentlich in der DB landen würden.

## Test (Phase B)

- Team-Frage „Was ist Patricias doTERRA-Positionierungsansatz?" → **muss** antworten (aus `doterra-positionierungs-framework.md`)
- Team-Frage „Was ist Patricias Gesamt-Umsatz?" → **muss nicht wissen** (Privacy-Check)
- Team-Frage „Wie ist Patricias Mentoring-Launch im März gelaufen?" → **muss nicht wissen** (Scope-Check: Mentoring gehört nicht in doTERRA-Bot)
- Team-Frage „Was ist Patricias Mentoring-Framework?" → **muss nicht wissen** (selbst wenn Inhalt existierte, würde der Scope-Check greifen)
