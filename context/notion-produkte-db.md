# Notion Produkte-DB — Felder & Mapping

**DB-URL:** https://www.notion.so/2ae7078e8b7e81efaafaf03993ef344f?v=2ae7078e8b7e818f9d79000cab96bd3b
**DB-ID:** `2ae7078e-8b7e-81ef-aafa-f03993ef344f`

Diese Datei dokumentiert die Struktur von Patricias zentraler Produkt-Datenbank in Notion. Wird von `/produkt` bei jedem neuen Produkt verwendet, um die richtigen Fragen zu stellen und den DB-Eintrag vorzubereiten.

---

## Pflicht-Felder (Working Set)

Basierend auf Patricias Angabe „Zielgruppe, Dauer, Preis, Learnings etc." — die exakte, vollständige Feldliste wird beim ersten Produkt-Lauf mit Patricia verifiziert und hier aktualisiert.

**Erwartete Felder (nach Julia-Trost-DB-Konvention):**

| Feld | Typ | Beschreibung | Pflicht bei /produkt? |
|---|---|---|---|
| **Produktname** | Title | Titel mit Ziel drin (nicht generisch) | ✅ Pflicht |
| **Typ / Kategorie** | Select | Freebie (0€) / Minikurs (37-49 CHF) / Signature (199-555) / Premium (1'199+) / 1:1 | ✅ Pflicht |
| **Status** | Select | Idee / Validierung / In Erstellung / Launch / Live / Archiv | ✅ Pflicht |
| **Zielgruppe** | Text / Multi | Konkrete Wunschkundin (nicht „Mamas", sondern „Mamas im Network Marketing, die...") | ✅ Pflicht |
| **Painpoint** | Text | EIN spezifischer Schmerzpunkt, den das Produkt adressiert | ✅ Pflicht |
| **Kern-Transformation (A → ?)** | Text | Wohin bringt das Produkt die Kundin? (B / E / M / Z entlang der Treppe) | ✅ Pflicht |
| **Learnings** | Text / Multi | 3-5 konkrete Learnings die die Kundin am Ende hat | ✅ Pflicht |
| **Dauer** | Text / Number | Länge des Kurses / Zugriffsdauer / Durcharbeitungszeit | ✅ Pflicht |
| **Preis (CHF)** | Number | Finaler Preis | ✅ Pflicht |
| **Preis-Staffel** | Text | Secret / Early Bird / Final (siehe Modus 4) | optional |
| **Module / Lektionen** | Text / Relation | Grobstruktur | ✅ Pflicht |
| **Format** | Select / Multi | Video / PDF / Audio / Live-Call / Community | ✅ Pflicht |
| **Freebie / Vorgängerprodukt** | Relation | Welches Produkt kommt davor in der Treppe? | optional |
| **Upsell / Folgeprodukt** | Relation | Welches Produkt kommt danach? | optional |
| **KI-Assistent (Bonus)** | Text | Gibt es einen Kurs-Bot? Welcher? | optional |
| **Launch-Datum** | Date | Geplant oder real | optional |
| **Plattform** | Select | ThriveCart / elopage / Teachable / Website / Padlet | optional |
| **Sales-Page URL** | URL | Link zur Sales-Page | optional |
| **Markt-Research-Notiz** | Text | Kurze Zusammenfassung der Painpoint-Validierung aus Web/Social | empfohlen |
| **Umsatz-Beitrag (Ziel)** | Number | Geplanter Jahresumsatz dieses Produkts (Beitrag zum 40k-Ziel) | empfohlen |

---

## Eintrags-Protokoll (für /produkt)

**Bei jedem Produkt-Durchlauf:**

1. **Prüfen:** Existiert das Produkt schon in der DB? (Patricia fragen, oder via Notion-MCP suchen sobald verbunden)
2. **Neuen Eintrag vorbereiten:** Alle Pflicht-Felder aus den vorherigen Modi sammeln.
3. **Output-Format generieren:**
   ```
   📋 NOTION-DB-EINTRAG VORBEREITET:

   Produktname: ...
   Typ: ...
   Status: ...
   Zielgruppe: ...
   Painpoint: ...
   Kern-Transformation (A → ?): ...
   Learnings:
     - ...
     - ...
   Dauer: ...
   Preis (CHF): ...
   Module:
     1. ...
   Format: ...
   Markt-Research-Notiz: ...
   Umsatz-Beitrag (Ziel): ... CHF/Jahr (X % des 40k-Ziels)

   → Manuell in Notion DB einfügen: [DB-URL]
   ```
4. **Alternativ (sobald Notion-MCP verbunden):** Direkt per API-Call in die DB schreiben.

---

## Strukturelle Prüfung vor neuer Produktidee

Bevor ein neues Produkt entwickelt wird, prüfe gegen die bestehende DB:

- [ ] Gibt es schon ein ähnliches Produkt? (Dopplung vermeiden)
- [ ] Ist die Produkttreppe lückenhaft? (z.B. fehlt ein Minikurs zwischen Freebie und Signature?)
- [ ] Welcher Painpoint ist noch NICHT adressiert? (Lücken-Analyse)
- [ ] Decken die existierenden Produkte die A→B→E→M→Z-Logik sauber ab?

---

## A → B → E → M → Z — Patricias Treppen-Logik

Patricia denkt ihre Produkttreppe so:

```
A  (Ausgangspunkt: Kundin ist hier)
↓
B  (Freebie 0€ → erster Sprung)
↓
E  (Miniprodukt → zweites Level)
↓
M  (mittleres Produkt → Kernsprung)
↓
Z  (grosses Produkt → Zielpunkt)
```

**Kritisch:**
- Jedes Produkt muss **genau einen Sprung** machen — keine Überlappungen mit der nächsten Stufe.
- Das Freebie muss neugierig auf das Miniprodukt machen (Sprung B → E ist leicht).
- Das Miniprodukt muss zeigen, dass Z ohne das mittlere Produkt nicht erreichbar ist (Wertigkeits-Logik).
- Jedes Produkt spiegelt genau **einen Painpoint** wider, der auf dem Markt validiert ist.

---

## Update-Hinweis

**Wenn Patricia die exakte Notion-DB-Struktur teilt, aktualisiere diese Datei** mit den echten Feldnamen, Select-Optionen und Pflichtfeldern. Solange das nicht geschehen ist, arbeite mit der erwarteten Struktur oben.
