---
tags: [skill, vorlage]
---

# Vorlage: So ist eine SKILL.md aufgebaut

Bauprinzip für jeden neuen Skill und für den Umbau der bestehenden.
Interne Arbeitsvorlage — **gehört nicht in ein Kundenpaket.**

Die Reihenfolge ist kein Schmuck. Sie bildet ab, wie ein Skill denkt:
erst wissen für wen, dann wissen was fehlt, dann erst schreiben.

---

## Das Gerüst

```markdown
---
name: <ordnername, exakt gleich>
description: "Ein Satz, woran Claude erkennt, wann dieser Skill dran ist."
---

# <Name> v1.0

## Wofür dieser Skill da ist
Ein Absatz. Welches Problem er löst, und wofür er ausdrücklich nicht da ist.

## Die Säulen
Drei bis fünf Punkte, an denen der Output steht oder fällt.
Dazu ein Satz: "Eine Säule schwach = das Ergebnis trägt nicht."

## TEIL 1: BRIEFING — der Kontext
Eine ausfüllbare Vorlage, die die Nutzerin einmal pro Produkt anlegt.
Produkt · Zielgruppe · Beweis · Angebot · Stimme.

### Briefing-Check
Tabelle: Bereich | Frage | Warum es das Ergebnis verändert.
Plus eine Faustregel, woran man merkt, dass noch zu viel fehlt.

## Standard-Output
Die feste Menge, die ohne Rückfrage geliefert wird.
Beispiel: 5 Texte, 5 Überschriften, 5 Beschreibungen.

## TEIL 2: BEWUSSTSEINSSTUFE
Wo steht die Person gerade — und was ändert das an Ton und Länge?

## TEIL 3: HOOKS
Die Hook-Typen dieses Skills, mit Längen je Platzierung.

## TEIL 4: ANGLES
Die Perspektiven, aus denen mehrere Stücke entstehen.
Drei bis fünf mischen, nicht fünf Varianten derselben Perspektive.

## TEIL 5: AUFBAU
Der Bogen des eigentlichen Stücks, Zeile für Zeile mit Aufgabe.

## TEIL 6: REGELN UND VERBOTE
Echte Zahlen statt erfundener · längere Sätze statt Stakkato ·
KI-Floskeln, die nie vorkommen · Schweizer ss.

## TEIL 7: OUTPUT-FORMAT
Wie das Ergebnis aussieht, wenn es fertig ist. Als Muster zum Kopieren.

## TEIL 8: EIN BEISPIEL
Ein durchgerechnetes Stück von Briefing bis Ergebnis.

## TEIL 9: TESTEN UND NACHSCHÄRFEN
Woran man merkt, dass es funktioniert hat — und was man dann ändert.
```

---

## Die drei Stellen, an denen meine alten Skills abweichen

Beim Umbau sind das die Punkte, die tatsächlich fehlen — Zweck, Wissensquellen,
Stimme und Regeln stehen meistens schon drin.

**1. Briefing statt festes Profil.**
Meine Skills laden `patricia-vollprofil.md` und schreiben immer für dieselbe
Person. Ein weitergebbarer Skill fragt den Kontext ab und arbeitet mit dem,
was die Nutzerin einträgt. Für den Eigengebrauch darf beides nebeneinander
stehen: Profil als Standard, Briefing als Überschreibung.

**2. Bewusstseinsstufe.**
Kennt die Person ihr Problem schon? Kennt sie mich? Das ändert Hook-Stil und
Textlänge stärker als jede Formulierungsregel. Fehlt in allen meinen Skills.
→ Verwandt: die Regel, dass Hooks symptombewusst sein müssen und nicht
produktbewusst. Die Bewusstseinsstufe ist der Rahmen dahinter.

**3. Angle als Achse, nicht nur Hook-Muster.**
Mein Hook-Pattern-Mix sorgt dafür, dass Hooks unterschiedlich *klingen*.
Ein Angle ist die Perspektive dahinter — Schmerz, Ergebnis, Beweis, konträre
These, Identität. Fünf Hooks aus einem Angle sind fünf Varianten desselben
Textes. Drei bis fünf Angles mischen.

---

## Feste Output-Menge

„Mach mir ein paar Varianten" führt zu drei halbherzigen. Eine feste Zahl im
Skill führt zu fünf, die durchdacht sind. Die Zahl gehört in die SKILL.md,
nicht in die Anfrage.

---

## Verwandt

- `_WEITERGABE-STATUS.md` — welcher Skill darf raus, und was muss vorher weg
- `CLAUDE.md`, Abschnitt „Skill-Standard" — Ordnerform und Frontmatter
- `scripts/skills/anleitungen-generieren.py` — erzeugt die Anleitung.md
