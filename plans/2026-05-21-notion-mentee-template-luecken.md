---
tags: [plan, produkt, mama-ceo]
---

# Plan — Notion-Mentee-Master-Template: 4 fehlende DBs ergänzen

**Datum:** 2026-05-21
**Status:** Bereit zur Umsetzung — wartet auf Notion-MCP-Reconnect
**Master-Template Page-ID:** `3637078e-8b7e-8121-9f95-d2b377b283a7`
**URL:** https://www.notion.so/3637078e8b7e81219f95d2b377b283a7

---

## Ziel

Die Mentee bekommt eine **schlanke, vereinfachte 1:1-Kopie** von Patricias 4-Stufen-Planungs-Hierarchie + Ziele-DB. Aufgaben aus dem Modul-1-Arbeitsblatt entsprechen **exakt** den Notion-DB-Properties → in Modul 2 Lektion 2.2 wird übertragen, nicht neu erfunden. Schema ist **API-clean** designed, damit Cockpit-Bot (Modul 2 Lektion 2.5) später automatisch befüllen kann.

---

## Aktueller Stand des Templates

**Schon enthalten:**
- 📘 Anleitung-Page (`3637078e-8b7e-81a0-85c8-eeb559924404`) — referenziert noch alte Säule-1/2-Sprache, muss aktualisiert werden
- 📅 Wochenplanung-DB (besteht, muss erweitert werden)
- ✅ Aufgaben-DB (besteht — Hütchen-Property aus alter Logik OK behalten)
- 📝 Content-Management-DB
- 🛍 Produkte-DB
- 🔁 Workflows-Page
- 🎯 Mama-CEO-Matrix-Page
- 📈 90-Tage-Tracker-Page
- BEISPIEL-Brain-Dump-Page (`3637078e-8b7e-815e9156fc290f6d5d98`) — alte Säule-2-Sprache, umbenennen auf „Modul 1 Lektion 1.3 · 10-Tasks-Audit"

**Fehlt komplett:**
1. ❌ Jahresplanung-DB
2. ❌ Monatsplanung-DB
3. ❌ Tagesplaner-DB
4. ❌ Ziele-DB
5. ❌ Relations zwischen den 4 Stufen
6. ❌ Wochenplanung-Erweiterung (CEO-Tag-Fokus + Power-Slot-Tabelle + Sonntag-Reset)

---

## Mapping — Arbeitsblatt Modul 1 → Notion-DBs

Aus `outputs/produkte/mama-ceo/04-arbeitsblaetter/mama-ceo-arbeitsblatt-modul-1.docx` (alle 5 Lektionen):

| # | Arbeitsblatt-Aufgabe | Notion-Ziel | Wann übertragen |
|---|---|---|---|
| 1.1 | Mama-CEO in deinen Worten definieren | Ziele-DB · Eintrag „Identität: Ich bin Mama-CEO" | Modul 2 L2.2 |
| 1.1 | Wichtigster Shift (Macherin→Entscheiderin etc.) | Ziele-DB · Eintrag „Mein Shift-Fokus 2026" | M2 L2.2 |
| 1.2 | „Wenn nur..."-Satz + Falle | Ziele-DB · Eintrag „Mein Sabotage-Satz" | M2 L2.2 |
| 1.2 | Glaubenssätze (Mama-Sein / Erfolg / Vereinbarkeit) | Ziele-DB · 3 Einträge Kategorie „Glaubenssatz" | M2 L2.2 |
| 1.2 | Neue Identität „Ich bin..." | Ziele-DB · Eintrag „Neue Identität", Status Aktiv | M2 L2.2 |
| 1.2 | 1 konkrete Sache diese Woche entscheiden | Aufgaben-DB · Entry mit Datum | M2 L2.2 |
| 1.3 | 5 CEO-Aufgaben für DICH konkret | Ziele-DB · 5 Einträge Kategorie „CEO-Aufgabe" | M2 L2.2 |
| 1.3 | 10-Tasks-Audit | **Bleibt im Arbeitsblatt** (einmalige Diagnose) | — |
| 1.3 | 1 Task delegieren/automatisieren | Aufgaben-DB · Status „delegieren" | M2 L2.2 |
| 1.4 | 7-Tage-Energie-Tracker | **Bleibt im Arbeitsblatt** (einmalige Diagnose) | — |
| 1.4 | 2 Power-Slots/Tag + Erschöpfung-Wand | Wochenplanung-DB · Body-Tabelle „Power-Slots Mo-So" | M2 L2.2 |
| 1.4 | Wochenrhythmus mit CEO-Fokus pro Tag | Wochenplanung-DB · Property „CEO-Tag-Fokus" | M2 L2.2 |
| 1.4 | Sonntag-Reset 5 Schritte | Wochenplanung-DB · Body-Template „Sonntag-Reset" | M2 L2.2 |
| 1.5 | Perfektions-Versteck identifiziert | Ziele-DB · Eintrag „Anti-Perfektion-Wächter" | M2 L2.2 |
| 1.5 | 12-Monats-Vision (Mittwoch Stunde-für-Stunde) | Jahresplanung-DB · 1. Eintrag „2026 · meine Vision" | M2 L2.2 |
| 1.5 | 3 Erfolgs-Metriken (Zeit/Energie/Zahl) | Jahresplanung-DB · 3 Properties | M2 L2.2 |
| 1.5 | EINE Sache diese Woche live (Datum+Uhrzeit) | Aufgaben-DB · Entry mit Date + Uhrzeit | M2 L2.2 |

---

## DB-Schemas

### 1. Jahresplanung

| Property | Typ | Optionen / Beschreibung |
|---|---|---|
| Name | Title | z.B. „2026 — meine Vision" |
| Jahr | Number | 2026 |
| Status | Select | Aktiv · Vergangen · Geplant |
| 12-Monats-Vision | Rich Text | Aus Arbeitsblatt 1.5 — der Mittwoch-Snapshot |
| Zeit-Metrik | Rich Text | „Mo/Mi/Fr 16h Schluss" etc. |
| Energie-Metrik | Rich Text | „Sonntagabend ohne Schuld ins Bett" |
| Zahl-Metrik | Rich Text | „CHF X Umsatz / Y Kundinnen / Z Runden" |
| Themen-Fokus | Multi-Select | frei wählbar |
| Monate | Relation | → Monatsplanung (1:n) |

**Default-Page:** „2026 — meine Vision" (leer, Mentee füllt aus)

---

### 2. Monatsplanung

| Property | Typ | Optionen / Beschreibung |
|---|---|---|
| Name | Title | z.B. „Juni 2026" |
| Monat | Date | Erster Tag des Monats |
| Hauptfokus | Rich Text | Was steht im Zentrum |
| Status | Select | Aktiv · Geschlossen · Geplant |
| 3 Hauptziele | Relation | → Ziele-DB |
| Jahr | Relation | → Jahresplanung (n:1) |
| Wochen | Relation | → Wochenplanung (1:n) |

**Default-Page:** „Juni 2026" (leer)

---

### 3. Tagesplaner

| Property | Typ | Optionen / Beschreibung |
|---|---|---|
| Name | Title | z.B. „Mi 28.5.26" |
| Datum | Date | **Pflicht für Cockpit-Bot** |
| Tagesfokus | Rich Text | DIE EINE Sache heute |
| Energie | Select | 🔴 erschöpft · 🟡 mittel · 🟢 frisch |
| Power-Slot genutzt? | Checkbox | für Bot-Auswertung |
| Reflexion (abends) | Rich Text | was lief, was bleibt |
| Woche | Relation | → Wochenplanung (n:1) |
| Aufgaben | Relation | → Aufgaben (1:n) |

**Default-Page:** ein Beispieltag mit gestelltem Inhalt (für Anschauung)

---

### 4. Ziele

| Property | Typ | Optionen / Beschreibung |
|---|---|---|
| Name | Title | z.B. „Ich bin Mama-CEO" |
| Kategorie | Select | Identität · CEO-Aufgabe · Glaubenssatz · Neue Identität · Vision · Metrik · Anti-Perfektion · Sabotage-Satz · Shift-Fokus |
| Beschreibung | Rich Text | freier Text aus Arbeitsblatt |
| Status | Select | Aktiv · Erreicht · Pausiert · Verworfen |
| Erstellt am | Created time | automatisch |
| Jahr | Relation | → Jahresplanung |

**Default-Pages (3 Stück, als Anschauungs-Vorlagen):**
1. „Identität: Ich bin Mama-CEO" (Kategorie: Identität, Status: Aktiv) — leer
2. „CEO-Aufgabe 1: Vision & Strategie" (Kategorie: CEO-Aufgabe, Status: Aktiv) — leer
3. „Mein Anti-Perfektion-Wächter" (Kategorie: Anti-Perfektion) — leer

---

### Wochenplanung-DB erweitern

**Neue Properties:**
- **CEO-Tag-Fokus** (Select): Strategie · Brand · Beziehungen · Entscheidungen · Reflexion · Reset
- **Monat** (Relation): → Monatsplanung

**Body-Template** (für jede neue Wochen-Page automatisch):

```
## Power-Slots diese Woche

| Tag | Power-Slot 1 | Power-Slot 2 | CEO-Fokus |
| Mo  |              |              | Strategie |
| Di  |              |              | Brand |
| Mi  |              |              | Beziehungen |
| Do  |              |              | Entscheidungen |
| Fr  |              |              | Reflexion |
| Sa  |              |              | — |
| So  |              |              | Reset |

## Sonntag-Reset (15 Min)

1. **Anerkennen** (3 Min): 3 Dinge die diese Woche liefen
2. **Loslassen** (2 Min): Was bleibt liegen — ohne Schuld
3. **5-Aufgaben-Check** (3 Min): Welche CEO-Aufgabe hatte Fokus? Welche fehlt?
4. **Power-Slots planen** (4 Min): Wann sind nächste Woche die 10 Slots? Mit Thema.
5. **EINE Sache** (3 Min): Was ist DIE Sache der nächsten Woche?
```

---

## Relations-Übersicht

```
Jahresplanung (1) ───< Monatsplanung (n)
Monatsplanung (1) ───< Wochenplanung (n)
Wochenplanung (1) ───< Tagesplaner (n)
Tagesplaner (1) ───< Aufgaben (n)
Ziele (n) >─── Jahresplanung (1)
Ziele (n) >─── Monatsplanung (1)  [via 3-Hauptziele]
```

Mentee sieht: „Wenn ich diesen Monat einen Eintrag mache, sehe ich automatisch welches Jahr, welche Wochen, welche Tagespläne dazugehören."

---

## Cockpit-Bot-Tauglichkeit (für Modul 2 L2.5)

Schema ist API-clean:
- **Datumsfelder** = echte `Date`-Properties → Bot kann `today()` / `this_week()` queryen
- **Status/Kategorie** = `Select` mit begrenzten Options → Bot kann nicht falsch schreiben
- **Energie** = `Select` mit Emoji-Optionen → einfach für Bot zu setzen
- **Relations** sauber kaskadiert → Bot kann „erstelle Tagesplaner-Eintrag für morgen, verbinde automatisch mit aktueller KW" ausführen
- **Rich Text** für freie Beschreibungen → Bot kann längere Inhalte schreiben

**Beispiel-Bot-Aktion in M2 L2.5:**
> „Erstelle Tagesplaner-Eintrag für morgen mit Tagesfokus 'Salespage publishen', verbinde mit aktueller KW, lege 3 Aufgaben an mit Hütchen 'CEO'."

---

## Anleitung-Page Update (`3637078e-8b7e-81a0-85c8-eeb559924404`)

**Was raus muss:**
- Alle „Säule 1 / Säule 2"-Referenzen → durch „Modul 1 / Modul 2" ersetzen
- Alte Hauptthemen aus dem Karriere-Mum-Mentoring → durch Mama-CEO-Sprache

**Neue Struktur:**
1. Willkommen — du hast das Mama-CEO Master-Template dupliziert
2. Was du in Modul 1 NICHT mit Notion machst (= ausschliesslich Arbeitsblatt)
3. Was du in Modul 2 L2.2 hier befüllst (Übertrags-Liste)
4. Wie die 4 Stufen + Ziele zusammenhängen (kurzes Diagramm)
5. Wie der Cockpit-Bot später hier reinkommt (Teaser für M2 L2.5)

---

## „BEISPIEL — Brain Dump"-Page (`3637078e-8b7e-815e9156fc290f6d5d98`) umbauen

**Neuer Titel:** „BEISPIEL — Modul 1 Lektion 1.3 · 10-Tasks-Audit"

**Neuer Inhalt:**
- Erklärung dass diese Page einmalig als Anschauung dient
- 10-Tasks-Audit-Tabelle mit Beispiel-Werten (aus Patricias eigener Praxis)
- Hinweis: „Du machst dieses Audit IM ARBEITSBLATT, nicht hier — das hier ist nur die Anschauung wie es aussehen kann"

---

## Umsetzungs-Reihenfolge

1. **Auth-Check** — retrieve Master-Template-Page (verifizieren dass Token funktioniert)
2. **Jahresplanung-DB** anlegen + 1 Default-Page „2026 — meine Vision"
3. **Monatsplanung-DB** anlegen + 1 Default-Page „Juni 2026"
4. **Ziele-DB** anlegen + 3 Default-Pages (Identität · CEO-Aufgabe 1 · Anti-Perfektion)
5. **Tagesplaner-DB** anlegen + 1 Beispieltag
6. **Wochenplanung-DB** updaten (neue Properties + Body-Template via patch-block-children)
7. **Relations** zwischen den 4 Stufen herstellen (Jahr↔Monat, Monat↔Woche, Woche↔Tag, Ziele↔Jahr/Monat)
8. **Anleitung-Page** überschreiben (alte Säule-Sprache raus)
9. **Brain-Dump-Page** umbenennen + Inhalt updaten
10. **Verifikation:** retrieve alle DBs, check Properties + Relations

**Geschätzte Dauer mit funktionierendem MCP:** ~15-20 Min

---

## Was nach diesem Plan offen bleibt (separate Tasks)

- ⏭ **Arbeitsblatt Modul 2** (.docx) bauen — wartet bis Lektion 2.4-Aufnahme da ist
- ⏭ **Cockpit-Bot-System-Prompt-Vorlage** (.md) als Download für L2.5
- ⏭ **Patricias eigener Business-Brief** als Beispiel für L2.4

---

## 🔗 Verwandte Notizen

- `outputs/produkte/mama-ceo/01-inhaltsverzeichnis.md`
- `outputs/produkte/mama-ceo/04-arbeitsblaetter/mama-ceo-arbeitsblatt-modul-1.docx`
- `.claude/worktrees/cranky-gagarin-5de31b/outputs/produkte/mama-ceo/12-thrivecart-modul-1-und-2.md`
- Memory: `reference_patricia-notion-planung.md` · `feedback_modul-1-papier-modul-2-notion.md` · `project_mama-ceo-modulbau.md`
