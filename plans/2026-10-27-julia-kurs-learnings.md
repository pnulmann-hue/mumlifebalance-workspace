---
tags: [plan, julia-trost]
---

# Julias Kurse als vollständige Learnings — und je Business-Schritt ein Skill

**Stand:** 27.10.2026 · **Status:** Phase 0 läuft

Patricia: *„ich möchte ja möglichst viel vom wissen, das ich mir hier von julia erworben habe,
über meine skills für mein business abrufen"* · *„für jeden kurs eine md-datei mit den wichtigen
learnings (nichts auslassen)"* · *„ich will für jeden step in meinem business einen skill"*.

**Ausdrücklich nicht in diesem Plan:** Weitergabe an MBA-Kundinnen (Patricia, 27.10.:
*„vorerst will ich nichts weitergeben"*). Die Skills bekommen trotzdem den Aufbau nach dem
Skill-Standard, die Anleitung bleibt aber liegen.

---

## Warum

- Die Transkripte sind **600 Dateien in 38 Ordnern, rund 17 MB** — kein Skill kann das bei
  einem Auftrag lesen.
- Heute zeigen die Skills fast alle auf `reference/julia-trost/methodik.md`, eine alte
  Zusammenfassung, die Funnel und Liste zu früh ansetzt. Aufbereitetes Wissen haben nur
  `/strategie` (drei Dateien) und `/jahresplan` (ein Transkript).
- Die Learnings-Datei je Kurs wird **einmal** gelesen und danach von beliebig vielen Skills genutzt.

🗃 Vorgänger: `_sortiert/_SKILL_transkript-zu-wissensbasis/` (April 2026) hat Transkripte nur
**aufgeräumt**, nicht verdichtet, und ist bei zwei Kursen stehengeblieben
(`_wissensbasis_preview/`). Wird nicht weitergeführt.

---

## Phase 0 · Transkripte fertig machen

- [ ] Abschreiben der letzten Videos aus „Verkaufen mit Liebe" abwarten (Stand: 11 von 15)
- [ ] Die 22 Wortsalat-Einträge in `transkripte-abgleich.json` wieder markieren
      (`abschreiben.py` überschreibt die Datei)
- [ ] `transkripte-bericht-2026-10-27.md` mit den Zahlen nachziehen,
      „Verkaufen mit Liebe" in `was-neu-2026-10-27.md` ergänzen

## Phase 1 · Die Learnings je Kurs, vollständig

**Ablage:** `reference/julia-trost/learnings/<kurs>.md` — gitignored über `reference/julia-trost/**`.

**Aufbau jeder Datei:**

```markdown
---
tags: [externe-wissen, julia-trost]
---

# <Kurs> — Learnings

Umfang: N Lektionen, N Transkripte · Lücken: <Wortsalat, fehlende Videos>
Gehört zu den Schritten: <Positionierung · Angebot · Freebie · Funnel · …>
Vorlagen dazu: `Vorlagen/<Kurs>/…`

## Überblick (nur zur Orientierung, ersetzt nichts darunter)

## Lektion für Lektion
### <Modul / Lektion>
- Regel / Zahl / Checkliste / Beispiel / empfohlene Formulierung
  — Fundstelle: <Datei>, <Zeitmarke>

## Widersprüche zu anderen Kursen
```

**Regeln fürs Schreiben**

1. **Vollständig, keine Zusammenfassung.** Patricia, 27.10.: *„nicht nur EIN Fazit. Sondern die
   Learnings aus dem Kurs festgehalten. Vollständig."* Jede Regel, Zahl, Liste, jedes Beispiel,
   jeder Ablauf und jede Begründung kommt hinein — wer die Datei liest, muss das Video nicht mehr
   schauen. Raus fällt nur das Drumherum: Füllwörter, Wiederholungen, Begrüssungen, Werbung für
   andere Kurse, Technikprobleme, „seht ihr das?".
2. **Je Aussage eine Fundstelle** (Datei, Zeitmarke aus der `.vtt`, wo vorhanden).
3. **Zahlen und Preise wörtlich**, mit Währung — nie runden, nie umrechnen.
4. **Keine eigene Meinung in den Learnings.** Was Julia sagt, steht da; Patricias Abweichungen
   gehören in die Skills, nicht hierher.
5. **Lücken benennen** — Wortsalat-Videos und fehlende Transkripte stehen oben im Umfang.
6. **Widersprüche festhalten**, nicht auflösen (Beispiel: 1k-Stufe „1:1 plus 0€-E-Book" in
   den Videos gegen „1:1 ohne Minikurs" in den Stufen-Tabellen).

**Vorgehen**

- Helfer im Hintergrund, je Kurs einer; grosse Kurse (OBA 1,9 MB, Werbeanzeigen,
  Mentoring Gruppe, Verkaufen mit Liebe) werden nach Modulen geteilt und danach zusammengeführt.
- Reihenfolge nach dem, was im November gebraucht wird:
  1. Launchen · Verkaufen mit Liebe · Magnetisch Verkaufen · Automationen ·
     Automatisiere deine Angebote · Leadgewinnung · Digitale Produktwelt · Minikurse ·
     Die Minikurs Strategie · Instagram Story Strategie 2.0
  2. 100k Blueprint · OBA · 10k / 20k / Road to 50K · Mentoring Gruppe · Forever Fans
  3. Content (der verkauft) · Content Recycling · Reels to Cash · IG Reichweiten Booster ·
     Glasklare Produktkommunikation · 16 Kurse für 15€
  4. Werbeanzeigen · Erfolgreiche Werbeanzeigen · ARIA · ChatGPT · Manychat-Vorlagen
  5. Rest (Bonus-Lektionen, Sonstiges, Erfolgreich ins neue Jahr, Einzeldateien)

## Phase 1b · Themenbücher statt Kursbücher (Patricia, 27.10.)

*„schau welche themen in den kursen vorkommen und pack den inhalt in das entsprechende thema.
wenn etwas ja schon drin steht, musst du es nicht doppelt aufführen"*

- **Stufe 1** bleibt je Kurs (Auftrag für die Helfer: `reference/julia-trost/learnings/_AUFTRAG.md`),
  aber jeder Punkt trägt Themen-Marken (`#launch #funnel …`). Die Kursdatei ist Zwischenstufe und
  Fundstellen-Quelle.
- **Stufe 2:** je Thema ein Buch `reference/julia-trost/learnings/themen/<thema>.md`. Darin jeder
  Punkt **einmal**, nach Unterthemen geordnet; sagen zwei Kurse dasselbe, steht es einmal mit beiden
  Fundstellen. Widersprüche zwischen Kursen eigener Abschnitt.
- Die Wissensbibliothek im Cockpit zeigt die Themenbücher; die Kursdateien nur noch zum Nachschlagen.
- Neuer Kurs später: Stufe 1 für ihn, dann in Stufe 2 nur Neues ergänzen.

## Phase 2 · Gegenlesen

- [ ] Je Datei zwei Lektionen ganz gegen das Transkript lesen: fehlt eine Regel, ein
      Beispiel oder ein Schritt, ist die Datei nicht fertig (Vollständigkeit vor Kürze)

- [ ] Je Datei: Zahl der behandelten Lektionen = Zahl der Transkripte (minus benannte Lücken)
- [ ] Je Datei fünf Stichproben: Zahl oder Regel gegen das Transkript prüfen
- [ ] Prüfung auf erfundene Inhalte: jede Aussage ohne Fundstelle fliegt raus

## Phase 3 · Themen-Register

`reference/julia-trost/learnings/_register.md` — Thema → welche Kurse, welche Abschnitte.
Viele Themen kommen mehrfach vor (Launch in fünf Kursen); das Register zeigt, wo.

## Phase 4 · Landkarte Business-Schritte → Skills

Zum Abnehmen durch Patricia, bevor gebaut wird. Arbeitsentwurf:

Positionierung → Angebotstreppe → Freebie → Funnel & Mails → Verkaufsseite & Kasse →
Launch → Storys → Content → Werbung → Stufe & Strategie → Jahresplan → Mama-CEO & Zeit

Je Schritt genau ein Skill. Die Landkarte zeigt, welche es schon gibt
(`/funnel`, `/copywriting`, `/story`, `/strategie`, `/jahresplan`, `/content`, `/produkt`,
`/angebot`, `/facebook-ads` …), welche fehlen und welche doppelt sind.

## Phase 5 · Skills anbinden

- [ ] Jeder Skill bekommt einen Pflicht-Block: „Vor dem Bauen die Learnings zu Schritt X lesen
      und im Ergebnis nennen, welche Regel angewendet wurde."
- [ ] Reihenfolge bei Widerspruch bleibt: Patricias eigene Regeln → Learnings → `methodik.md`
      (nur noch Herkunft).
- [ ] Für Einzelfragen darf der Skill die Transkripte gezielt nach Stichwort durchsuchen und
      nennt die Fundstelle.
- [ ] Je Skill drei, vier Prüffragen, die Julia im Kurs klar beantwortet — der Skill muss ihre
      Antwort liefern, sonst fehlt eine Regel.
- [ ] Neue Skills nach dem Skill-Standard (Ordner, `SKILL.md`, `Anleitung.md`).
- [ ] CLAUDE.md nachziehen.

## Offen

- Kosten: das Lesen der rund 17 MB ist der grosse Posten — kursweise, über mehrere Sitzungen.
- Neue Kurse später: eine Learnings-Datei dazuschreiben, Register und betroffene Skills nachziehen.
