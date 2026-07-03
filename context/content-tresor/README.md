---
tags: [externe-wissen, kurs-extrakt, content, vorlagen]
---

# Content-Tresor — Vorlagen & Patricias Varianten

Ausgelesen aus dem Trello-Board **„Content Tresor von Reichweitenherz"** (Julia Ströhmann). Aufbereitet, damit die Content-Skills bei der Planung darauf zugreifen können.

## Dateien

| Datei | Inhalt | Für wen |
|---|---|---|
| `tresor-vorlagen.json` | **50 Roh-Vorlagen** (10 Sets × 5 Säulen) + Anleitung + CTA-Kompass-Mapping + Säulen-Emotionen | Maschinenlesbar für Skills |
| `tresor-vorlagen.md` | Dieselben 50 Sets lesbar zum Durchblättern | Patricia |
| `patricia-varianten.json` | **Fertige, in Brand-Voice adaptierte** Hook+Caption-Fassungen | **Der Content-Bot** |

## Die 5 Content-Säulen (= die 5 Set-Typen)

| Säule | Emotion beim Leser | CTA-Typ |
|---|---|---|
| 💃 Identifikation | „Ja, genau so bin ich" (100 % ertappt) | Folgen |
| 👑 Positionierung | Tabu/unbequeme Wahrheit, geschockt + fasziniert | Folgen (Gesinnung) |
| 💡 Mehrwert | brutaler Aha-Moment | Speichern/Teilen/Folgen |
| 📖 Storytelling | extreme Bilder im Kopf, heftige Emotion | Folgen |
| 💸 Verkauf | Wunschvorstellung + Transformation, „das brauche ich JETZT" | nächste Funnel-Stufe |

## So nutzt der Bot das (bei `/monatsplan` Phase 4.5 & `/freitag-hooks`)

1. **Erst `patricia-varianten.json` prüfen** — gibt es für Säule + Profil + Thema schon eine fertige, freigegebene Variante? → direkt einplanen.
2. **Sonst aus `tresor-vorlagen.json`** das passende Set der Säule nehmen, die `[…]`-Platzhalter mit dem Wochen-Thema/Painpoint füllen und **in Brand-Voice adaptieren** (`brand-voice.md` + `ki-phrasen-blackliste.md` + `hook-framework.md`).
3. **Neue Adaption zurückschreiben** in `patricia-varianten.json` (Status `test`), damit sie wiederverwendbar wird und Patricia sie nach dem Test auf `freigegeben`/`verworfen` setzen kann.

## Regeln bei jeder Adaption (Pflicht)

- Schweizer **ss**, echte Umlaute
- **Kein Dreier-Stakkato**, keine KI-Floskeln → `ki-phrasen-blackliste.md`
- **Keine erfundenen Zahlen** (nur echte aus `patricia-expertise.md` / Input)
- Beste-Freundin-Ton, Fliesstext
- Zeitanker-Hooks bevorzugt (Content-Radar), max 5 Hashtags, `#mamabusiness` Pflicht-Anker
- Visual: Emotions-Sets (Identifikation/Storytelling) = dunkler Filter + weisse Schrift; Mehrwert = hell/schnell/harte Kontraste

## Eintrag in `patricia-varianten.json` — Schema

```json
{
  "id": "<saeule>-set<N>-<profil>-<lfd>",
  "quelle_set": { "saeule": "...", "set": 1, "idShort": 1, "shortUrl": "..." },
  "profil": "mentoring | doterra",
  "saeule_content": "identifikation | positionierung | mehrwert | storytelling | verkauf",
  "thema": "...", "painpoint": "...",
  "hooks": [ { "variante": "...", "pattern": "...", "text": "...", "einsatz": "..." } ],
  "caption": "...", "cta": "...", "cta_typ": "...",
  "status": "test | freigegeben | verwendet | verworfen",
  "erstellt_am": "YYYY-MM-DD", "notizen": "..."
}
```
