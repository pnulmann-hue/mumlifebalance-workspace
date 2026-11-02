---
tags: [plan, produkt, ki-kurs]
---

# Modul 5 aufnehmen — Skills, das Herzstück

**Erstellt:** 02.11.2026 · **Für:** KI-Kurs „Deine KI-Mitarbeiterin", Kapitel 5
**Stand:** Kapitel 1–4 sind aufgenommen, 5–10 offen. Modul 5 ist das nächste.

---

## Worum es geht

Patricia will Modul 5 aufnehmen. Im Inhaltsverzeichnis steht darüber:
*„Wer nur ein Kapitel mitnimmt, soll es dieses sein. Alles danach ist Anwendung."*

Acht Lektionen, **sechs davon mit Bildschirm-Demo**. Die Folien stehen, die
Sprechnotizen auch. Drei Dinge fehlen — und eines davon würde ein Nachdrehen
erzwingen, wenn es erst nach der Aufnahme auffällt.

---

## 🚨 Drei Dinge VOR der ersten Aufnahme

### 1 · Hinweis A fehlt in Modul 5 — das ist der kritische Punkt

Am 26.10. hat Patricia festgelegt: *„ich will dann im Kurs ja darauf hinweisen, dass
sie z.B. meine vollständigen Caption, Hook etc. Skills in den jeweiligen Kursen
bekommen"* — und der Hinweis läuft in **beide Richtungen** (`13-skills-weitergeben.md`).

**In `folien-modul-5.py` steht er nicht.** Die drei Stellen mit dem Wort „leer"
sprechen von einem leeren *Feld*, nicht von leeren Skills. Nachgesehen am 02.11.

Ohne diesen Hinweis nimmt sie das Kapitel auf, in dem sie die Skills weitergibt,
**ohne zu sagen, dass sie leer sind und wo die vollen liegen** — und muss nachdrehen.

→ **Eine Folie zwischen 5.8 und dem Abschluss**, plus zwei Sätze in der Sprechnotiz
von 5.2 (dort gibt sie die erste Skill-Datei mit). Wortlaut steht als Entwurf in
`outputs/produkte/ki-treppe/13-skills-weitergeben.md` unter „Hinweis A".

### 2 · Die Beilage zu 5.2 fehlt

Das Inhaltsverzeichnis verspricht bei 5.2: **„Mitgeben: genau diese Datei"** — den
Skill, den sie Zeile für Zeile auseinandernimmt. In `beilagen/` liegt
`cowork-projekt-kochassistent.md`, aber **kein Kochplan-Skill**.

🚨 Vor jedem Versprechen im Produkt nachzählen (Lehre vom 18.09., damals waren es
„fertige Beispiele für jedes Feld", die es nicht gab).

→ Entweder die Datei anlegen, **oder** 5.2 am vorhandenen `skill-geruest.md` plus
einem echten kleinen Skill zeigen und das Versprechen im Inhaltsverzeichnis anpassen.
Patricias Entscheid.

### 3 · Die Checkliste zu 5.7 fehlt

Versprochen: **„Mitgeben: Checkliste 'fremden Skill prüfen'"**. In
`checklisten-alle.md` steht dazu genau **eine Abhak-Zeile** („Ich weiss, worauf ich bei
fremden Skills schaue"), in `sicherheits-checkliste.md` nichts zum Thema.

→ Die Checkliste schreiben. Das Material dafür ist da, in CLAUDE.md belegt: SKILL.md
lesen · mitgelieferte Skripte ansehen · Claude fragen „was tut das genau, greift es auf
Schlüssel oder das Internet zu?" · prüfen, ob der Skill nach aussen schreibt.

---

## Was schon steht

| | |
|---|---|
| **Folien** | 8 Lektionstitel, rund 31 Folien, je mit Sprechnotiz. `python scripts/ki-kurs/folien-modul-5.py <ordner>` |
| **Beilage 5.8** | `beilagen/skill-geruest.md` — das leere Gerüst |
| **Demo-Ordner** | `scripts/ki-kurs/demo-ordner-bauen.py` — zeigt nur, was gezeigt werden soll, mit Wächter gegen fremde Namen und echte Zahlen |
| **Lektionstexte** | im Inhaltsverzeichnis für alle acht Lektionen angelegt |

---

## Was sie am Bildschirm zeigt — je Lektion

🚨 **Sobald der Bildschirm geteilt ist, sieht sie die Sprechnotizen nicht mehr.** Für
die Masterclass gibt es dafür einen Regie-Zettel (`regiezettel-bauen.py`), **für die
Kursmodule nicht**. Der gehört vor dem Dreh gebaut — eine A4-Seite je Modul: Lektion ·
was auf der Folie steht · was zu zeigen ist.

| Lektion | Bildschirm | Material — und was heute dazugekommen ist |
|---|---|---|
| **5.1** Was ein Skill ist | ✅ | Einen Aufruf mit Schrägstrich tippen und zuschauen lassen. **`/planen woche`** ist dafür gut: kurz, sichtbar, und er fragt |
| **5.2** Auseinandergenommen | ✅ | Einen Skill Zeile für Zeile: Kopf · Zweck · Regeln · Ergebnis · Beispiel. **Siehe Punkt 2 oben** |
| **5.3** Woran du es erkennst | ✅ | Ihre ehrliche Liste. **Neu heute:** drei Skills für einen Auftrag (`jahresplan` · `monatsplan` · `cockpit`) — genau das Erkennungszeichen |
| **5.4** Ersten Skill bauen | ✅ | Skill Creator live, von der Idee zur Datei |
| **5.5** Von Hand nachschärfen | ✅ | **Neu heute:** die neun Beschreibungen, die sagen, wofür ein Skill zuständig ist — das weiss kein Creator |
| **5.6** Dreimal korrigiert = Regel | ✅ | **Neu heute, drei echte Fälle:** „otion" fing „Emotion" · Median 0 statt `reach` · umschriebene Umlaute. Alle drei sind heute als Gegenprobe in den Code gegangen |
| **5.7** Fremde Skills | ✅ | Einen fremden Skill aufmachen und prüfen. **Siehe Punkt 3 oben** |
| **5.8** Zusammenfassung | — | Nur Folien plus das leere Gerüst |

**Der Glücksfall:** 5.3, 5.5 und 5.6 brauchen echte Beispiele aus ihrem Alltag — und
die sind heute beim Bauen von `/planen` entstanden. Nichts davon ist erfunden.

---

## Reihenfolge am Drehtag

Nicht 5.1 bis 5.8 der Reihe nach, sondern **nach Aufwand gruppiert** — damit sie nicht
zwischen Reden und Klicken hin und her springt:

1. **Block A — nur Folien** (rund 20 Min): 5.1 Einstieg · 5.3 · 5.6 · 5.8
2. **Block B — Bildschirm** (rund 35 Min): 5.2 · 5.4 · 5.5 · 5.7
3. **Block C — der Hinweis** (5 Min): die neue Folie aus Punkt 1

🚨 Zwischen den Blöcken die Aufnahme **nicht** stoppen, sondern durchlaufen lassen und
den Versprecher wiederholen — `/videoschnitt` nimmt den letzten vollständigen Take.

---

## Woran wir merken, dass es fertig ist

- Alle acht Lektionen liegen als Video im Vimeo-Ordner „Easy KI" und tragen das Muster
  `NN-lektion-5-N-titel`, sonst findet `kurse-indexieren.py` Modul und Lektion nicht.
- `python scripts/ki-kurs/vimeo-transkripte.py` holt die Untertitel, und die
  Zuordnung Video → Lektion steht **belegt** in der `LEKTION`-Tabelle, nicht geraten.
  🚨 Der Beleg ist der Schlusssatz: jedes Video kündigt das nächste an.
- `produktion-daten.py` zeigt je Lektion eine Zeichenzahl **über 1'000** — bei 4.4 waren
  es durch einen Trennstrich mitten im Text einmal 213 statt 4'997, und die Seite sah
  trotzdem normal aus.
- Der Fachkurs-Hinweis steht im Video **und** im Lektionstext bei 5.2 und 5.8.
- Die drei Beilagen von Kapitel 5 sind in Drive und über die Produktionsseite
  aufrufbar — 🚨 als **Google Doc**, wo etwas hineingeschrieben wird, nicht als PDF
  (Lehre vom 22.10.: 17 von 21 lagen im falschen Format).

---

## Was bewusst nicht dazugehört

- **Kapitel 6–10.** Eines nach dem anderen.
- **Der Schnitt.** Läuft über `/videoschnitt`, nicht über diesen Plan.
- **Die vollen Skills.** Die gehen in die Fachkurse, nicht hier (Patricias Entscheid
  vom 26.10.) — hier wird nur darauf hingewiesen.
- **Die sieben zugekauften Skills.** Gehen nie raus, auch nicht leer.

---

## Was es berührt

| Datei | Was |
|---|---|
| `scripts/ki-kurs/folien-modul-5.py` | die Hinweis-Folie dazu |
| `outputs/produkte/ki-treppe/beilagen/` | zwei fehlende Beilagen |
| `outputs/produkte/ki-treppe/03-inhaltsverzeichnis.md` | 5.2 anpassen, falls die Datei nicht kommt |
| `scripts/ki-kurs/regiezettel-bauen.py` | Regie-Zettel für Kursmodule, nicht nur die Masterclass |
| `scripts/ki-kurs/vimeo-transkripte.py` | `LEKTION`-Tabelle um 5.1–5.8 ergänzen, mit Beleg |
| `outputs/produkte/ki-treppe/13-skills-weitergeben.md` | Hinweis A abhaken, sobald er drin ist |

---

## 🔗 Verwandte Notizen

- [[13-skills-weitergeben]] — welcher Skill in welchem Kurs, und der Hinweis in beide Richtungen
- [[03-inhaltsverzeichnis]] — Kapitel 5 im Detail
- [[2026-11-02-planungs-kreislauf]] — dort ist heute das Demo-Material für 5.3, 5.5 und 5.6 entstanden
