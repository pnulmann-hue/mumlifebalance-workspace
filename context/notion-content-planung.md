---
tags: [notion, content]
---

# Notion-Content-Planung — Lese-Logik für /freitag-hooks + /daily-story-render

**Erstellt:** 2026-04-30
**Zweck:** Alle Skills, die Patricias Wochen-/Monatskontext brauchen, lesen aus diesen DBs.

---

## Drei zentrale Notion-DBs

### 1. Monatsplanung-DB (Top-Level-Strategie)

- **Database-URL:** `https://app.notion.com/p/2ae7078e8b7e8171a760c233083c26b6`
- **Data-Source:** `collection://2ae7078e-8b7e-81fc-acf7-000be291c92c`
- **Pages:** 1 pro Monat (z.B. „🚀 Mai 2026" `3367078e-8b7e-8132-ad06-cb6c942b2d01`)

**Properties pro Monat-Page:**
| Property | Typ | Was steht drin (Beispiel Mai 2026) |
|---|---|---|
| `Monat + Jahr` | Title | „Mai 2026" |
| `Zeitraum` | Date-Range | start: 2026-05-01, end: 2026-05-31 |
| `3 Monatsziele` | Text (mehrzeilig) | „1. Säule 3 «Dein Business-Rhythmus» (CHF 333) launchen — 15+ Käufe = CHF 5'000<br>2. Minikurs liefern<br>3. Umsetzerinnen aufbauen" |
| `Erkenntnis Kennzahlen-Analyse` | Text | (vom Vormonat) |
| `Erkenntnisse Content-Analyse` | Text | (vom Vormonat) |
| `Learnings aus dem letzten Monat` | Text | |

**Body-Block (für Stories wichtig):**
Im Block „Content Planung für den übernächsten Monat" → Section „Themenplanung | Fokus und Zielsetzung des Contents":
> „Steht ein Launch an, auf den du deinen Content ausrichten möchtest? Oder welches Produkt stellt dein Content in den Fokus?"

Verlinkt auf **Content-Themenplanung-DB** (siehe Punkt 3).

### 2. Wochenplanung-DB (operative Wochen-Steuerung)

- **Database-URL:** `https://app.notion.com/p/2ae7078e8b7e81efa769cdb1a6584c70`
- **Data-Source:** `collection://2ae7078e-8b7e-81e7-9083-000b01908eb5`
- **Pages:** 1 pro KW (z.B. „Wochenplanung KW 18 (27.4.–3.5.2026)")

**Properties:**
| Property | Typ | Bedeutung |
|---|---|---|
| `Woche` | Title | „Wochenplanung KW XX" |
| `Zeitraum` | Date-Range | KW-Start bis KW-Ende |
| `Fokus der Woche` | Text | **WICHTIGSTES FELD** — was ist der Wochenfokus |
| `Erfolge letzte Woche` | Text | |
| `Herausforderung letzte Woche` | Text | |
| `Contentplanung` | Checkbox | gemacht ja/nein |

**Body-Tabelle „Was planst du je Business-Säule?":**
| Säule | Was hier reinkommt |
|---|---|
| Kundenarbeit | |
| Produktentwicklung | |
| Business-Struktur aufbauen | |
| **Content-Creation** | ← **kritisch für Skills** |
| Weiterbildung | |

### 3. Content-Themenplanung-DB

- **Database-URL:** `https://app.notion.com/p/3a77078e8b7e826d9edd01b87c4545d3`
- **Verlinkt aus Monatsplanung-Body** unter „Themenplanung"
- Hier steht Patricias Themen-Planung pro Monat — welches Produkt wird beworben

(Felder werden bei erstem Zugriff aufgenommen — Schema noch nicht detailliert dokumentiert)

---

## Lese-Logik für Skills

### Universelle Lese-Funktion (Pseudocode)

```
function ladeNotionKontext(zielKW, profil = "beide"):
  # Schritt 1: Monatsplan für aktuellen Monat laden
  aktuellerMonat = berechneMonat(zielKW)  # z.B. "Mai 2026"
  monatPage = notion.search("Monatsplanung " + aktuellerMonat)
  monatsZiele = monatPage.properties["3 Monatsziele"]

  # Schritt 2: Wochenplan für Ziel-KW laden
  wochenPage = notion.search("Wochenplanung KW " + zielKW)

  if wochenPage existiert:
    wochenFokus = wochenPage.properties["Fokus der Woche"]
    contentSaeule = wochenPage.body.tabelle["Was planst du je Business-Säule?"].zeile["Content-Creation"]
  else:
    return { status: "wochenplan_fehlt", monatsZiele: monatsZiele }

  # Schritt 3: Content-Themenplanung lesen (falls referenziert)
  themenPlan = notion.queryDB("3a77078e-8b7e-826d-9edd-01b87c4545d3", filter={ Monat: aktuellerMonat })

  return {
    status: "ok",
    monatsZiele: monatsZiele,
    wochenFokus: wochenFokus,
    contentSaeule: contentSaeule,
    themenPlan: themenPlan
  }
```

### Fallback-Verhalten bei fehlenden Daten

| Fall | Skill-Verhalten |
|---|---|
| **Wochenplan existiert nicht** | Fragt Patricia per Telegram/Chat: „Keine Wochenplanung für KW X gefunden. Was ist diese Woche dein Fokus? Welches Produkt bewerben wir?" |
| **`Fokus der Woche` ist leer** | Gleiche Frage — Skill nutzt Monatsziele als Fallback-Hinweis |
| **`Content-Creation`-Zeile leer** | Fragt: „Im Wochenplan ist der Content-Bereich leer. Was möchtest du diese Woche im Content beackern?" |
| **Monatsplan komplett leer** | Fragt: „Kein Monatsplan für [Monat]. Was sind deine 3 Monatsziele?" |
| **Antwort cachen** | Skill speichert Antwort in `outputs/stories/wochen-vorwahl-KW##.json` — gilt für die ganze Woche |

### Wichtig: Zeitlicher Kontext

- **`/freitag-hooks` (Fr 08:00):** Plant für die KOMMENDE Woche (also KW+1). Liest den Wochenplan für KW+1, nicht aktuelle KW.
- **`/daily-story-render` (Mo-So 06:30):** Plant für HEUTE. Liest aktuelle KW.

```
Beispiel — Heute ist Fr, 2026-05-01 (KW 18):
  /freitag-hooks läuft → plant für KW 19 (04.05.–10.05.)
  /daily-story-render läuft am Mo 04.05. → liest KW 19 aus
```

---

## Cache-Strategie

Pro Skill-Lauf wird der gelesene Kontext gecached, um wiederholte Notion-Calls zu vermeiden.

### Cache-Datei: `outputs/stories/wochen-vorwahl-KW##.json`

```json
{
  "kw": 19,
  "zeitraum": "2026-05-04 bis 2026-05-10",
  "abgerufen_am": "2026-05-01T08:15:00Z",

  "monatsplan": {
    "monat": "Mai 2026",
    "ziele": "1. Säule 3 «Dein Business-Rhythmus» launchen ..."
  },

  "wochenplan": {
    "fokus_der_woche": "Säule 3 Pre-Sale-Phase: Warmlist mobilisieren",
    "content_creation": "Stories über Säule-3-Erfolg, 1 Karussell mit Workbook-Teaser, 2 Reels"
  },

  "themen_plan": {
    "produkt_im_fokus": "Säule 3 Signature Programm (CHF 333)",
    "freebie_funnel": "Workbook «Von 0 auf echt»",
    "manychat_keyword": "ECHT1"
  },

  "wochenvorwahl_stories": {
    "mentoring": {
      "Mo": { "thema_id": "M-S2", "hook": "..." },
      "Di": { "thema_id": "M-S5", "hook": "..." },
      ...
    },
    "doterra": {
      "Mo": { "thema_id": "D-S1", "hook": "..." },
      ...
    }
  }
}
```

### Cache-Invalidierung
- Bei jedem `/freitag-hooks`-Lauf: Cache für Ziel-KW (+1) wird neu erstellt
- Bei jedem `/daily-story-render`-Lauf: liest Cache, **fragt nicht erneut** (ausser Datei fehlt)
- Patricia kann manuell triggern „/story-cache-refresh" wenn sich Wochenplan ändert

---

## Implementation in Skills

### /freitag-hooks (Fr 08:00)

```
1. Lade Monatsplan für aktuellen Monat
2. Lade ODER erstelle Wochenplan-Skeleton für KW+1
3. Falls "Fokus der Woche" leer in KW+1:
   → sende Telegram-Nachricht:
     "Hi Patricia! Was ist nächste Woche (KW XX) dein Fokus?
      Monatsziel-Erinnerung: [Top-Ziel aus Monatsplan]
      Antworte mit 1-Satz-Fokus."
   → warte auf Antwort, speichere im Cache
4. Generiere 10 Hooks pro Profil (Karussell/Reel) + 7 Story-Themen pro Profil
5. Sende formatiertes Telegram mit Pick-Anleitung
```

### /daily-story-render (Mo-So 06:30)

```
1. Berechne heutigen Wochentag + KW
2. Lade Cache: wochen-vorwahl-KW##.json
3. Falls Cache fehlt:
   → fallback auf Direkt-Notion-Read (Wochenplan)
   → falls auch leer: Telegram-Notfall-Nachricht an Patricia
     "Hi! Kein Wochenplan + keine Vorwahl. Soll ich heute eine Default-Story machen?"
4. Lese vorgewählte Story-Themen für heutigen Wochentag (Mo/Di/Mi/...)
5. Generiere Slides für Mentoring + doTERRA
6. Render PNGs + sende einzeln per Telegram mit Sticker-/Umfrage-Captions
```

---

## Bot-Scope-Klärung

- **Monatsplan + Wochenplan:** beide Profile (Mentoring + doTERRA)
- **Content-Themenplanung-DB:** wahrscheinlich gemischt — Skill muss prüfen, ob Eintrag „Mentoring", „doTERRA" oder „beide" markiert ist
- **/freitag-hooks** liest BEIDE — sendet Hooks für beide Profile
- **/daily-story-render** rendert für BEIDE Profile (2 Story-Sequenzen pro Tag)

Wenn Patricia im Telegram „nur Mentoring heute" tippt → Skill rendert nur Mentoring an dem Tag.

---

## TODO bei erster echter Notion-Recherche

- [ ] Content-Themenplanung-DB Schema komplett erfassen
- [ ] Welche Property in Themenplanung-DB sagt „Profil" (Mentoring/doTERRA)?
- [ ] Welche Property sagt „Produkt"?
- [ ] Welche Property sagt „Status" (geplant/aktiv/durch)?
- [ ] Bei erstem `/freitag-hooks`-Lauf: erste Notion-Reads dokumentieren
