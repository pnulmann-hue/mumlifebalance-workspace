---
name: planen
description: >-
  Planung über alle Zeiträume — Jahr, Quartal, Monat, Woche. Führt durch die
  Fragen, rechnet die Lücke zum Umsatzziel, legt den Bogen im Cockpit ab und
  baut daraus den Auftrag für /content. Dran bei /planen, „plan mir den Monat“,
  „Quartalsplanung“, „Jahresplanung“, „was ist diese Woche dran“.
---

# /planen — ein Kreislauf, vier Zeiträume

**Aufruf:** `/planen jahr` · `/planen quartal` · `/planen monat` · `/planen woche`
Ohne Angabe: den Zeitraum nehmen, der laut Tabelle unten fällig ist, und das sagen.

🗃 **Löst `/jahresplan`, `/monatsplan` und `/cockpit` ab** (Plan vom 02.11.2026,
`plans/2026-11-02-planungs-kreislauf.md`). Die drei liegen im Archiv; was an Regeln
drinsteckte, steht hier.

---

## Die Schärfungs-Kaskade

Patricia, 02.11.2026: *„im grundsatz will ich mal die jahresplanung machen mit ferien,
grundsatzthemen KI, mama ceo, instagram usw. und dann mach ich die quartalsplanung wo
ich noch etwas detaillierter den leadmagneten festsetze, workshop plane usw. und dann
die monatsplanung ganz ins detail mit beiträgen, storys usw.“*

| Zeitraum | Wie fein | Wann | Bogen im Cockpit |
|---|---|---|---|
| **Jahr** | Ferien · Grundsatzthemen · grobe Launch-Fenster · Umsatzziel | Dezember, mit Q1 | `daten/jahresplan` |
| **Quartal** | Leadmagnet · Workshops · welches Angebot wann · die drei Monatsthemen | letzter Monat des Quartals: Mär · Jun · Sep · Dez | `daten/quartalsbogen` |
| **Monat** | ganz ins Detail: Beiträge, Storys, Mails, Dreh-Liste | **am 29.** des Vormonats | `daten/monatsbogen` |
| **Woche** | nur Rahmen und Ausführung | Sonntagabend | `daten/wochenbogen` |

🚨 **Der ganze Content wird im MONAT gebaut, nicht in der Woche** — auch die
A/B-Varianten je Platz und die Hook-Prüfung (Patricia, 02.11.: *„ne die a/b varianten,
hooks prüfung usw. soll bitte auch pro monat geschaut werden“*). In der Woche entsteht
kein neuer Beitrag. Wöchentlich bleibt nur der **Treffer-Check**: hat ein Beitrag in
14 Tagen ≥ 2× den eigenen Median erreicht, gehören die nächsten zwei bis drei Plätze
Folge-Beiträgen — das meldet der tägliche Abgleich um 06:15, dafür braucht es keinen
eigenen Lauf.

🚨 **Alles landet im Cockpit, nichts in Notion** (Patricia, 02.11.: *„ich will nichts
mehr in notion. alles von notion, alle abläufe, alle fragen, soll im cockpit
abgebildet sein“*). Lesen aus Notion ist erlaubt, solange etwas nur dort liegt —
schreiben nicht.

🚨 **Je Bogen zwei Dokumente.** Der gerechnete Teil gehört dem Abgleich und wird
ersetzt; **`…-notizen` gehört Patricia und wird nie mit `set` überschrieben** —
dieselbe Regel wie `daten/produkt-details`.

---

## Die Fragen kommen aus einer Datei

**`scripts/jahresplan/fragen.json`** ist die eine Quelle für alle vier Zeiträume.
`python scripts/jahresplan/tool-bauen.py` baut daraus die Jahresplaner-Seite und den
Fragenblock unten; `python scripts/jahresplan/planen-skill-bauen.py` baut diesen Skill.
**Nie hier von Hand an den Fragen ändern** — nur in der JSON.

🚨 **Gefragt wird nur, was sich nicht ableiten lässt** (Patricias Entscheid, 02.11.).
Trägt eine Frage in der JSON ein Feld `quelle`, steht die Antwort beim Start schon da
und wird nur noch korrigiert. Die Quellen:

| `quelle` | kommt aus |
|---|---|
| `abgleich` | `outputs/cockpit/abgleich/` — Umsatz, Reichweite, Öffnungsraten |
| `gepostet` | `daten/gepostet` — was gut und was schlecht lief, gegen den eigenen Median |
| `planung-abgleich` | `planung-abgleichen.py` — was geplant war und keine Spur hat |
| `katalog` | `daten/katalog` — die Angebote mit Preis und Kette |
| `ideen-vorrat` | `context/ideen-vorrat.md` |
| `jahresplan` · `monatsplan` | der Bogen der nächstgrösseren Ebene |
| `tagebuch` | die sieben Tageseinträge der Woche (Learnings) |
| `termine` · `aufgaben` | `daten/termine` · `daten/aufgaben` |
| `downloads-aufraeumen.py` · `mails-sortieren-donnerstag` · `cockpit-kundinnen` | läuft von selbst, der Haken wird gesetzt statt gefragt |

---
## Jahr

*Im Dezember, zusammen mit dem ersten Quartal.*

#### So läuft das Gespräch

1. **Schritt für Schritt, höchstens drei Fragen auf einmal**, dann auf die Antwort warten. Wer bei
   einer Frage hängt, bekommt Sandras Beispiel aus `fragen.json` (Energie für Mamas ab 35), klar als
   Beispiel markiert, nie als Vorgabe.
2. **Leben zuerst.** Ferien, Familientermine und die eigene Zeit stehen im Plan, bevor ein einziges
   Angebot einen Monat bekommt. In Ferienwochen wird nicht verkauft.
3. **Ein Fokus-Angebot pro Monat**, dazu ein kostenloses Angebot zum selben Thema und kleine Angebote
   dazwischen. Grosse Angebote früh ankündigen, damit die Leute planen und sparen können.
4. **Reihenfolge nach dem Weg, den die Leute gehen:** erst das kostenlose Angebot, dann das kleine,
   dann das grosse. Ein Angebot, das ein anderes voraussetzt, kommt nach diesem.
5. **Rückwärts planen:** vom Verkaufsstart aus zurückrechnen, bis wann Seite, Kasse, Mails und
   Inhalte stehen müssen. Dieses Datum steht im Plan, nicht nur der Verkaufsstart.
6. **Ablauf eines Verkaufsmonats:** aufwärmen (3–7 Tage, über das Problem sprechen) → kurzes
   Vorab-Angebot für die Treuesten (rund 48 Stunden) → Verkauf (rund zwei Wochen) → Abschluss mit
   klarer Frist. Bei Patricia selbst laufen **Challenges besser als Masterclasses** (Entscheid 25.10.2026).
7. **Umsatz-Check:** Preis × geplante Verkäufe je Monat, zusammengezählt gegen das Ziel. Fehlt etwas,
   ehrlich sagen und drei Wege nennen (mehr Verkäufe, ein Verkaufsmonat mehr, Ziel anpassen). Keine
   geratenen Quoten, keine erfundenen Zahlen.
8. **Woche:** jedes Monatsthema in vier Wochenthemen zerlegen. Jedes Wochenthema ist ein Teil der
   Veränderung, die das Angebot bringt. **Das Angebot ist das Werkzeug, die Veränderung ist das Ziel.**
   Dazu der feste Wochenrhythmus (Beiträge, Tage, Storys mit Persönlichem, Tipp, Geschichte, Einladung).
9. **Vierteljährlich nachschauen.** Der Plan darf sich ändern. Am Quartalsende Ist gegen Plan
   vergleichen und den Rest des Jahres anpassen.

#### Lücken-Check — vor dem Ergebnis, Pflicht

Patricia: *„dass er merkt anhand des einkommensziels muss man so oder soviel umsetzen … wo hat der
funnel eine lücke, wo müsste man was zusätzliches entwickeln, wie könnte man mehr geld reinholen"*.
Die Seite rechnet denselben Check mit festen Regeln (`luecken()` in `tool-vorlage.html`). Im Gespräch
gehst du weiter und begründest jede Lücke.

**Zuerst lesen, wenn vorhanden:** `.claude/skills/strategie/wissen/julia-stufen.md` und
das Stufen-Material in `.claude/skills/strategie/wissen/` (gitignored, zugekauft).
Einen eigenen 5k-Kurs gibt es im Material nicht, die Stufe 0 → 5k ist aus ihren Rückblicken
zusammengesetzt. Fehlt der Ordner (weitergegebener Skill), gelten die Kurzregeln unten.
🚨 In nichts, was eine Kundin liest, steht der Name der Mentorin. Die Regeln werden in eigenen Worten erklärt.

**1 · Stufe aus dem Monatsziel** (Jahresziel ÷ 12; „k“ heisst dort Monatsumsatz, nicht Jahresumsatz):

| Monatsziel | Was dort trägt |
|---|---|
| bis 5'000 | ein Angebot pro Monat im Mittelpunkt, im Vormonat anwärmen, täglich Storys mit Link; lückenlos live verkaufen, noch kein automatischer Funnel |
| 5'000–10'000 | fester Monatsrhythmus, drei Monate im Voraus geplant, Stammkundschafts-Preis, Live-Inhalte aufzeichnen und weiterverkaufen |
| 10'000–20'000 | mehrere Angebote nebeneinander: Verkaufsphasen + kurze Aktionen + wiederkehrende Einnahmen (Raten, Mitgliedschaft); kleine Angebote laufen ganzjährig |
| über 20'000 | Funnel mit Einstieg, Webinar und Mails ersetzt einzelne Launches; Zusatzangebote an jeder Kasse; regelmässig Mails |

**2 · Die Lücken, nach denen du suchst:** Monate ohne Verkauf (ausser Ferien) · kein kostenloser
Einstieg (oder einer, der nicht zum Verkaufsmonat passt) · kein kleines Angebot als erster Kauf ·
grosser Sprung in der Treppe ohne mittleres Angebot · Umsatz hängt an ein, zwei Monaten · an der
Kasse des grossen Angebots kein Zusatz (Bump deutlich günstiger, Upsell günstiger als das Hauptangebot,
gilt nur dort) · Ziel über Preis × Verkäufe nicht erreicht.

**3 · Was es zum Ziel braucht:** fehlender Betrag ÷ Preis = zusätzliche Verkäufe je Angebot. Mit ihrer
eigenen Kaufquote („von 100 Interessierten kaufen …“) die Zahl der Interessierten je Verkaufsmonat.
**Keine geratenen Quoten** — fehlt ihre, wird nachgefragt oder die Rechnung weggelassen.

**4 · Je Lücke ein nächster Schritt:** was zusätzlich entstehen soll (z. B. ein mittleres Angebot,
ein Bump, ein kostenloser Einstieg zum Thema), wann es im Jahr gebaut wird und was es bringt, mit ihren
Zahlen. Fast Cash (Angebot umformen, Secret Offer, Bestandskundschaft) nur als Werkzeug gegen ein Loch,
nicht als Plan.

#### Network — mit den eigenen Zahlen, weil jeder Vergütungsplan anders ist

Patricia: *„oft ist es ja so, dass sie im network vorerst ja nur ihr produkt verkaufen … was es braucht,
bis sie das erreichen. mit teamaufbau usw. … da ist ja jedes network verschieden"*.
Gefragt wird nach Ziel und Ist im Monat, was pro Person mit Monatsbestellung bleibt, was eine aktive
Teampartnerin bringt, und was im Vergütungsplan als Nächstes steht (sie darf die Seite hineinkopieren).
Gerechnet wird: fehlender Betrag über Kundschaft · über Team · gemischt. Ränge und Boni nur aus **ihrem**
Plan, nie aus dem Gedächtnis über eine Firma. Die Kundschaft der Networkerin heisst nie „Kundin“.

**Ohne eigenes Angebot** werden Network-Angebote eingetragen (Feld „Herkunft“): Testwoche mit Proben =
kostenloser Einstieg und Leadmagnet, Starterset = klein, Einschreibung mit Treueprogramm = gross. Der
Plan funktioniert damit vollständig. Patricias Empfehlung bleibt trotzdem stehen: **ein kleines eigenes
Angebot zum Thema als Türöffner** (Hybridmodell) — Leute lernen sie als Expertin kennen und bestellen
danach. Das wird als Hebel benannt, nicht als Pflicht.

#### Ergebnis

Eine Datei `plans/jahresplan-<jahr>.md` (bei Patricia; bei Kundinnen in ihrem eigenen Workspace) mit:
zwölf Monaten (Fokus · Thema · kostenloses Angebot · Vorbereitung bis · geplanter Umsatz), vier
Wochenthemen je Monat, einer Beispielwoche und dem Umsatz-Check. Patricias eigener Plan geht danach
über Modus 2 in die Master-Sicht.

---

## Quartal

*Im letzten Monat des laufenden Quartals: März → Q2 · Juni → Q3 · September → Q4 ·
Dezember → Q1.*

Das Quartal erfindet nichts neu — es ist **Feinschliff auf dem Jahresplan** (Patricia:
*„auch wenn wir von der jahresplanung sicher schon einiges übernommen haben. aber der
feinschliff oder anpassungen kommen im quartal“*).

**Ablauf:**

1. **Rückblick** über die vier Fragen (grösster Erfolg · stolzestes Kundenergebnis ·
   was schwer war und was geholfen hat · was anders werden soll).
2. **Die drei Monatsthemen** festlegen. Bewährtes Muster aufsteigend: Haltung ändern →
   Weg zeigen → umsetzen lassen. Drei zusammenhängende Themen tragen weiter als drei
   einzelne; Pflicht ist das Muster nicht.
3. **Je Monat Fokus-Angebot, kostenloses Angebot davor und Workshop-Termin.**
   Die Angebote kommen aus dem Katalog, nie aus dem Kopf.
4. **Abgleich:** was vom Jahresplan noch keine Spur hat (`planung-abgleichen.py`) —
   je Zeile entscheidet sie: jetzt, wartet, oder hinfällig.
5. **Was bewusst wegfällt.** Ohne diese Antwort wird aus dem Plan eine Wunschliste.

**Danach:** Bogen nach `daten/quartalsbogen` schreiben und die drei Monatsthemen in
den Jahresplan zurückschreiben, damit die nächste Monatsplanung sie findet.

🚨 **Beim Vorausplanen gibt es keine eine richtige Zahl.** Die Methodik, an der sich
Patricia orientiert, sagt an fünf Stellen Verschiedenes (90 Tage · bis drei Monate ·
1–1,5 Monate · Quartale fein und das Jahr grob · sechs Monate). Es gilt Patricias
Entscheid: **Jahr grob, Quartal mittel, Monat fein.** Keine dieser Zahlen wird als
Regel hingeschrieben.

---

## Monat

*Am 29. des Vormonats. Der Lauf legt die Zahlen und die Diagnose vorher hin — zu beantworten sind nur die acht Fragen.*

### Phase 1 · Pflicht-Lektüre (5 Min, still)

Lies in dieser Reihenfolge:

1. `context/job-saeulen.md` — Soll-Mix pro Profil
2. `context/saeulen-mentoring.md` — Themen-Achse Mentoring + Block-Logik (Block A/B/C)
3. `context/business-info.md` — Beide Profile + Produkt-Treppe
4. `context/active-funnels.json` — Welche Funnels sind LIVE
5. `context/patricia-expertise.md` — keine Doppelung mit bestehenden Kursen
6. `context/brand-voice.md` — Tonalität für Hauptbotschaft
7. **Letzte 30 Tage:** `outputs/karussells/` + `outputs/reels/` + jüngstes `outputs/apify-runs/competitors-*.json` — was lief, was performte, was die Konkurrenz macht
8. **Monatsbogen des Vormonats** (`daten/monatsbogen` im Cockpit): Welche Ziele wurden erreicht, welche nicht

**Zusätzlich für die Content-Vorplanung (Phase 4.5) — Pflicht:**
9. `.claude/skills/hooks/SKILL.md` — der Hook-Master (Kundensprache, Stufen, Angles, PIE, Formeln, Verbote, letzter Check)
10. `context/content-formel-5-typen.md` — die 5 Content-Typen pro Woche
11. `context/reichweiten-posts-pattern.md` — Reichweiten-/Verbindungs-Posts (**mind. 2 von 5**)
12. jüngster **Content-Radar** (`context/content-radar-*.md`) — Format-Mix (Mentoring max 1 Karussell + Reels, doTERRA Reels-only), Zeitanker-Hook
13. `context/caption-formeln.md` — Caption-Struktur + Keyword-CTA
14. **Der Quartalsbogen** (`daten/quartalsbogen`) — Monatsthema, Fokus-Angebot und Workshop-Termin → die Content-Ideen müssen dazu passen
15. **Story-Vorlagen:** Launch → `outputs/produkte/mba-launch/story-plan.json` + `context/julia-launch-story-bausteine.md`; sonst → `context/julia-insta-stories-anleitung.md` + `julia-stories-die-verkaufen.md` + `julia-story-ideen.md`
16. Memory-Regeln: **keine Stakkato-Sätze** · keine erfundenen Zahlen · echte Umlaute/ss · doTERRA keine Heilversprechen · **kein Mentorinnen-Name in Kunden-Output**

---

### Phase 2 · Vormonats-Diagnose (10 Min)

Vor neuem Monat: was hat im vergangenen Monat gewirkt?

#### 2a) 🛑 PFLICHT — den Planungs-Abgleich lesen, BEVOR neu geplant wird

Patricia am 24.09.2026, nach dem ersten Abgleich: *„bei der nächsten planung
müssen wir das sicher beachten"*.

```bash
python scripts/cockpit/planung-abgleichen.py --zeigen
```

Das Skript hängt an jeden Jahresplan-Eintrag und jedes Ziel einen **Beleg aus
dem Workspace** — Produktordner, aktiver Funnel, ThriveCart-Status, Plan-Datei.
Im Cockpit stehen die Befunde unter **Planung → Jahresplan** und **→ Ziele**.

| Befund | was er für die neue Planung heisst |
|---|---|
| **belegt** | ist passiert — als Ausgangspunkt nehmen, nicht nochmal planen |
| **offen** | Termin liegt vorn — im neuen Monat einplanen oder streichen |
| **keine Spur** | **nachfragen.** Nie stillschweigend nochmal ansetzen und nie als gescheitert abbuchen |
| **Termin** | Ferien, Convention — Energie-Lage für Frage 8 |
| **abgelaufen** (Ziele) | Quartal vorbei, Status noch „Aktiv" — mit Patricia klären |

🚨 **Befund vom ersten Lauf (24.09.2026):** von 54 Jahresplan-Einträgen hatten
**22 keine Spur**, und **4 von 11 Zielen** trugen ein abgelaufenes Quartal bei
Status „Aktiv". Das ist keine Nachlässigkeit — es stand so in Notion und wurde
nie zurückgelesen. Wer ohne diesen Schritt plant, plant auf einem Stand, der
Monate alt sein kann.

🚨 **„Keine Spur" heisst NICHT „nicht passiert".** Ein Leadmagnet kann in
ManyChat leben, ohne je eine Datei zu bekommen. Der Befund ist eine **Frage an
Patricia**, kein Urteil — und bei der Planung wird sie gestellt, nicht
übergangen.

🚨 **Nichts automatisch abhaken.** Der Abgleich setzt keinen Status und darf
`daten/jahresplan` und `daten/ziele` nie überschreiben; die Befunde liegen
daneben in `daten/planung-abgleich`. Ein Haken, den eine Maschine gesetzt hat,
ist derselbe Fehler wie ein fehlender.

#### 2b) Den Monatsbogen des Vormonats lesen

Im Cockpit: `daten/monatsbogen` (gerechnet) und `daten/monatsbogen-notizen` (ihre Texte)

Aus Vormonats-Page abfragen:
- `3 Monatsziele` — wurden erreicht?
- `Erkenntnis Kennzahlen-Analyse` — was sagen die Zahlen?
- `Erkenntnisse Content-Analyse` — welche Posts performten?
- `Learnings aus dem letzten Monat` — was ändern wir?

#### 2c) Job-Mix-Compliance-Check Vormonat

In Content-Management-DB (`collection://2ae7078e-8b7e-811a-ad14-000ba5820c09`) filtern: `Veröffentlichung` im Vormonat + Profil. Dann:

- Wie viele A / B / C / D wurden tatsächlich gepostet?
- Stimmt das mit dem Vormonats-Soll-Mix überein?
- **Wenn D unter 15%:** Sales-Lücke — sollte diesen Monat höher gewichtet werden
- **Wenn C unter 17%:** Reichweite-Lücke — Pain-Hooks/Reels diesen Monat verstärken

#### 2d) Output Phase 2 (intern)

```
Vormonat-Diagnose [Monat YYYY]:
- Job-Mix Mentoring tatsächlich: A=X B=X C=X D=X (Soll: 4/4/2/2)
- Job-Mix doTERRA tatsächlich: A=X B=X C=X D=X
- Beste Posts (Saves+Shares): [Top 3]
- Schlechteste Posts: [Bottom 2]
- Korrektur-Vorschlag für neuen Monat: [...]
```

---

### Phase 4 · Plan generieren (5 Min, still)

Aus den 8 Antworten + Phase-2-Diagnose generieren:

#### 4a) Wochenfokus-Skelett (4 Wochen)

| KW | Datum | Block | Produkt im Fokus | Job-Mix-Soll | Spezial |
|---|---|---|---|---|---|
| KW X | dd.mm.-dd.mm. | A (0€) | Bio-Check | 1A 1B 1C | Reichweite-Woche, Story zeigt eigene Nutzung |
| KW X+1 | dd.mm.-dd.mm. | B (Mini) | „Finde dein Thema" | 1A 1B 1C | Validation-Mails parallel |
| KW X+2 | dd.mm.-dd.mm. | C (Gross) | Premium-Bundle | 1A 1B 1D | Pre-Sale-Push |
| KW X+3 | dd.mm.-dd.mm. | C (Gross) | Premium-Bundle | 1A 1B 1D | Verknappung + Cases |

#### 4b) Hauptbotschaft als „Storyline"

Die Hauptbotschaft wird als roter Faden über die 4 Wochen gespannt:
- KW 1: Hauptbotschaft anteasern (Aha-Moment)
- KW 2: Methode dahinter zeigen
- KW 3: Beweise / Cases / Live-Building
- KW 4: Verknappung + Reflexion

#### 4c) Hooks-Vorschau (3 pro Woche, optional)

**Optional — nur wenn Patricia es will:** Skill schlägt 3 Hook-Richtungen pro Woche vor (nicht ausformuliert — nur Konzept). Damit hat `/content woche` jede Woche schon einen Anker.

→ **Default: NICHT machen.** `/content woche` soll wöchentlich frisch arbeiten. Nur auf explizite Patricia-Bitte.

---

### Phase 4.5 · Monats-Content-Vorplanung (NEU — der eigentliche Content)

> Hier entsteht der konkrete Monats-Content, damit Patricia in 1-2 Tagen alles abdrehen kann. Baut auf dem Quartalsbogen auf (Monatsthema + Fokus-Angebot + kostenloses Angebot davor).

#### 4.5a) Marktanalyse pro Profil (Pflicht — „ich kann ihre Gedanken lesen")

Pro Profil (Mentoring + doTERRA), ausgerichtet aufs **Monats-/Launch-Thema**:
- **Pain · Wunsch · Ziel · Herausforderung** der Zielgruppe
- Quellen: jüngstes `outputs/apify-runs/competitors-*.json` + `discovery-*.json`, bei Bedarf WebSearch (IG/Reddit/Google Trends), `context/patricia-vollprofil.md` + Zielgruppen-Research
- → 1 verdichteter Absatz pro Profil, der die Hooks speist (jeder Beitrag adressiert mind. 1 davon)
- **Markt-Radar neu laufen lassen** (seit 30.10.2026, einmal im Monat, hier und nicht als eigene Routine):
  `python scripts/hooks/radar.py`. Die Berichte liegen dann in `outputs/marktrecherche/radar/` und
  im Cockpit unter Instagram → Markt-Radar (Sammlung `markt-radar` per `ArtifactData batch set`).
  Die Hebel aus dem eigenen Bericht gehören in den Monatsplan. 🚨 Für Standbilder der fremden Konten
  braucht es einen frischen Tiefen-Scrape (`.github/workflows/apify-tiefe.yml`), weil Instagram die
  Video-Adressen nach wenigen Tagen sperrt. Die Uhrzeit-Auswertung ändert die Posting-Zeiten nie von
  selbst. Wechseln sie, dann nur nach Patricias Ja und an allen drei Stellen
  (`reels-framework.md` · `patch-postzeit.py` · CLAUDE.md).

**Vierteljährlich (Januar · April · Juli · Oktober) zusätzlich:** die vier Grundanalysen
neu machen (Wettbewerb · Trends · Fragen der Zielgruppe · Zielgruppenbild mit Säulen), siehe
**Station 1 im Content-Kreislauf** oben in `.claude/skills/content/SKILL.md`. Danach die
Dateien in `.claude/skills/content/wissen/` nachziehen.

#### 4.5b) Vormonats-Content-Analyse (Pflicht)

🔄 **Seit 13.10.2026 aus `outputs/cockpit/abgleich/auswertung.json`** (der tägliche Abgleich
rechnet sie, Cockpit → Instagram → Ausgewertet). Die Notion-Content-DB ist abgelöst.
- **Bestperformer-Formel** (`bestperformer`): Top 10 mit Mindestbasis, und welche Merkmale
  in den Top 10 häufiger sind als bei allen Beiträgen. Nur die übernehmen.
- **Nachfrage je Thema** (`nachfrage`): Speichern · Teilen · Kommentare je 1'000 Erreichte.
  Ein Thema mit viel Reichweite und null Speicherungen ist Reichweite, keine Nachfrage.
- **Diagnose** (`diagnose`): wo Reichweite ohne Reaktion war → dort fehlt der Grund zu antworten.
- **Stichwörter mit Umsatz** (`stichwoerter`): welches Stichwort Eintragungen und Käufe bringt.
  🚨 Die Umsatz-Spalte nie aufsummieren, eine Käuferin kann bei drei Stichwörtern stehen.
- **Produktideen-Check:** Gibt es ein Thema, das zwei Monate hintereinander oben in der
  Nachfrage steht und kein Angebot hat? → an `/strategie hebel <Idee>` weitergeben.

#### 4.5b+) Der Monat als Garten — Pflicht seit 22.10.2026

Die Regeln stehen **einmal** in `.claude/skills/content/SKILL.md`, Abschnitt **„Der Garten“**.
Hier nur, was der Monatsplan daraus festlegt:

1. **Der Stadtteil:** das Monats-/Launch-Thema als Ort in der immer gleichen Stadt
   („Network-Mama baut sich etwas Eigenes daneben auf“). **Alle Stichwörter des Monats führen
   dorthin.**
2. **Zwei bis drei Painpoints in die Mitte** — Gedanken um 23 Uhr aus
   `content/wissen/zielgruppe-kurz.md`, im Wortlaut. 🚨 **Nie das Werkzeug** (KI, Instagram,
   Öle, Kurs): niemand wacht auf und denkt „ich sollte KI nutzen“.
3. **Je Painpoint drei Striche** — Geschichte · neue Perspektive · Meinung — und jeder Strich
   als **Mikrogeschichte** (ein Moment, ein Ort, eine Uhrzeit, nur Belegtes).
4. **Die vier Wochen als Kreislauf:** W1 Inspiration · W2 Entdecken · W3 Community ·
   W4 Schubs (Kundinnen-Fall, echte Einwände, Kasse). Danach Loyalität: Käuferinnen hören
   vom nächsten Monat zuerst.
5. **Daraus die Dreh-Liste (4.5d)** für drei Tage: planen · aufnehmen · schneiden.
6. **Platz für Treffer freihalten:** Schlägt ein Beitrag ein (≥ 2× Median), gehen die nächsten
   zwei bis drei Plätze an Folge-Beiträge, bevor das Wochenthema weiterläuft (`/content` Schritt 2b).
   Der Monatsplan ist darum ein Gerüst, kein Fahrplan.

#### 4.5c) Pro Woche: 5 Beiträge (thema-matched)

Für **jede Woche** des Monats (Fokus + Produkt + Aufruf werden hier festgelegt und wandern in den Wochenbogen), je Beitrag mit
**Rolle** (1× Aufmerksamkeit · 2× Vertrauen · 2× Beziehung, siehe 4.5b+) und dem Painpoint aus der Mitte:
- **5 Beiträge** nach den **5 Content-Typen** (`content-formel-5-typen.md`)
- davon **mind. 2 = reine Reichweiten-/Verbindungs-Posts** (kein Verkauf, Share-Trigger, Mama-Identity — `reichweiten-posts-pattern.md`). CTA „Teile das in deiner Story", **kein** Keyword.
- die übrigen 3 = Mehrwert / Story / Sales passend zum **Wochen-Produkt**, mit **Keyword-CTA** —
  das Stichwort **nur am Schluss**, nie in Zeile 1 (seit 22.10.2026)
- **Format-Mix** (Content-Radar): Mentoring max 1 Karussell + Rest Reels · **doTERRA Reels-only**
- pro Beitrag festhalten: **Hook** (nach `hook-framework.md` + Olga-Pattern-Mix + Zeitanker + 8/10 + **keine Stakkato**) · Typ · Format · Ziel (Reichweite/Lead/Sales) · adressierter Painpoint (aus 4.5a)

#### 4.5d) Reel-Dreh-Liste (Batch — zum Abdrehen in 1-2 Tagen)

ALLE Reels des Monats in EINER Tabelle, gruppiert nach **Setting/Outfit**, damit Patricia sie am Stück filmen kann:

| # | Woche | Produkt | Hook (Slide 1) | Dreh-Anweisung / Sprechtext (wort-für-wort bei Talking-Head, sonst Shotlist) | Format/Setting | B-Roll |
|---|---|---|---|---|---|---|

→ So weiss Patricia vorab **genau, was sie aufnehmen muss**. Sprechtexte sind Dreh-Anweisung; die finale Caption feilt `/content woche` / `/reels`.

#### 4.5e) Story-Logik (täglich — NICHT vorab ausformulieren)

Stories kommen täglich über den Story-Bot + `/story`. Der Monatsplan hält pro Woche nur den **Story-Bogen** (Thema + Käufertyp-Rotation), nicht die fertigen Slides:
- **Im Launch-Fenster:** `/story` baut nach der **Funnel-/Launch-Strategie** — `outputs/produkte/mba-launch/story-plan.json` + `context/julia-launch-story-bausteine.md` (Tag für Tag, Slide für Slide).
- **Ausserhalb Launch:** `/story` baut nach den **Story-Vorlagen** — `context/julia-insta-stories-anleitung.md` (10 Templates) + `julia-stories-die-verkaufen.md` + `julia-story-ideen.md`.

#### 4.5f) Monats-Blogartikel + Newsletter (gehören in den Monatsplan)

- **Blogartikel (1×/Monat):** Thema zum Monats-/Launch-Fokus festlegen → wird via `/blog` erstellt (SEO + Cascade-Output, der Stories/Karussell/Reel/Newsletter speist). Hier festhalten: Thema · Keyword · Ziel-CTA.
- **Mail-Newsletter:** Rhythmus + Themen pro Woche festlegen.
  - **Im Launch:** die Launch-Mail-Sequenz (Webinar-Einladung → Confirmation → Sales → No-Show).
  - **Sonst:** Mehrwert-Newsletter, der auf den Wochenfokus + das aktuelle Produkt führt (1 Emotion + 1 konkreter Tipp + 1 CTA).
- Blog + Newsletter ziehen **denselben Painpoint/Pillar** wie die Posts (aus 4.5a/4.5c) → ein roter Faden über Blog · Newsletter · Posts · Stories. Regeln gelten überall: keine Stakkato, echte Umlaute/ss, keine erfundenen Zahlen, kein Mentorinnen-Name im Kunden-Output, doTERRA = Compliance.

---

### Phase 5 · Ablegen — im Cockpit, nicht in Notion

🔄 **Hier lag bis zum 02.11.2026 der Schritt „Notion-Monatsplan-Page füllen“.**
Ersetzt durch:

1. **`daten/monatsbogen`** — der gerechnete Teil: Säule, die drei Angebote,
   Block-Verteilung, Job-Mix-Soll, Ziel, was nicht läuft, Energie-Lage.
   Geschrieben mit `set`, gehört dem Abgleich.
2. **`daten/monatsbogen-notizen`** — Patricias eigene Texte. **Nur `update`, nie
   `set`.**
3. **`outputs/monatsplaene/JJJJ-MM-<profil>.md`** — das Briefing, das `/content monat`
   liest. Bleibt wie bisher.
4. **Telegram-Kurzmeldung**, dass der Bogen steht.

🚨 **Kein Skript und kein Skill schreibt mehr nach Notion.** Gegenprobe vor dem
Abschluss: `git grep -n "notion" .claude/skills/planen/` findet nur Lese- oder
Umzugs-Hinweise.

---

## Woche

*Sonntagabend. Der Lauf eröffnet die Woche selbst; beim Öffnen des Cockpits kommt der
Dialog mit den offenen Fragen.*

**In der Woche entsteht kein Content.** Was hier passiert:

1. **Rückblick** — Erfolge und Herausforderungen stehen aus den sieben Tageseinträgen
   schon da und werden nur korrigiert.
2. **Fokus der Woche** — ihre Antwort. Hauptprodukt, Aufruf und Verkaufsphase kommen
   aus dem Monatsbogen.
3. **Die fünf Business-Säulen** — Kundenarbeit · Produktentwicklung ·
   Business-Struktur · Content-Creation · Weiterbildung. Je Zeile ein Satz. Eine
   Woche, in der nur Content-Creation gefüllt ist, war keine Business-Woche.
4. **Die Woche einteilen** — Reihenfolge: zuerst das Private, dann die festen Termine,
   dann die Storys, zum Schluss die Lücken. Termine und offene Aufgaben stehen schon da.
5. **Ausblick auf zwei Wochen** inklusive Me-Time — als Termin, nicht als Absicht.
6. **Ordnungsroutinen.** Download-Ordner, Mails und Kundendaten laufen von selbst und
   sind beim Start schon abgehakt; Handarbeit bleiben Browser-Tabs und Papiernotizen.

**Danach:** `daten/wochenbogen` (gerechnet) und `daten/wochenbogen-notizen` (ihre
Texte), dazu der Wochenfokus nach `daten/woche`, den der Bild-Editor liest.

---

## Die Master-Sicht über alle Zeiträume

#### 🛑 Vor jedem Modus: den Workspace-Abgleich lesen

Patricia am 24.09.2026: *„bei der nächsten planung müssen wir das sicher
beachten"*.

```bash
python scripts/cockpit/planung-abgleichen.py --zeigen
```

Der Jahresplan kam einmalig aus Notion und sagt, was **geplant** war — nicht,
was daraus geworden ist. Der Abgleich hängt an jeden Eintrag einen Beleg aus
dem Workspace und schreibt die Befunde nach `daten/planung-abgleich`; im
Cockpit stehen sie als Fähnchen an jeder Zeile.

🚨 **Erster Lauf: 22 von 54 Einträgen ohne Spur.** Wer ohne diesen Schritt
plant, baut auf einem Stand auf, der Monate alt sein kann.

🚨 **„Keine Spur" ist eine Frage, kein Urteil** — ein Leadmagnet kann in
ManyChat leben, ohne je eine Datei zu bekommen. Vor dem Umplanen nachfragen,
nie stillschweigend nochmal ansetzen.

🚨 **`daten/jahresplan` und `daten/ziele` gehören Patricia.** Der Abgleich
schreibt nie hinein und setzt keinen Status.

#### Modus 1 — `/jahresplan status`

**Zweck:** „Wo stehe ich heute?"

Liest:
- **`daten/planung-abgleich`** — was belegt ist und was keine Spur hat
- `context/jahresplan-2026.md` für Wochen-Kontext
- `context/active-funnels.json` für aktuelle Phasen
- Datums-Logik aus aktuellem System-Datum

Antwortet mit:
- Aktuelle KW + Tag
- Alle parallel laufenden Produkte/Launches mit Phasen
- Diese Woche zu erledigen (aus active-funnels.json `phase_history`)
- Nächste Meilensteine (nächsten 14 Tage)

**Beispiel-Output:**
```
KW 19, Donnerstag 8.5.2026

PARALLEL AKTIV:
- Mama-CEO: Pre-Launch W1 Validierung (bis 8.5.) → ab Fr W2 Anwarming
- Bio-Check: Pilot-Phase Tag 14 → Retargeting möglich
- doTERRA: keine aktive Kampagne

NÄCHSTE MEILENSTEINE:
- 9.5.: Mama-CEO Pre-Launch W2 startet (Sales-Page-Bau)
- 16.5.: Mastermind-Anmelde-Page live
- 22.5. 09:00: Mama-CEO CART-OPEN
- 26.5. 09:00: KI-MASTERMIND LIVE
```

#### Modus 2 — `/jahresplan launch [produkt-slug]`

**Zweck:** Neuen Launch in Master-Markdown eintragen

Liest:
- `outputs/produkte/[slug]/07-launch-kalender.md` (alle Phasen + Daten)
- `outputs/produkte/[slug]/00-briefing-FINAL.md` (Tagline + Preise)

Schreibt:
- Phasen ins `context/jahresplan-2026.md` (Monats-Tabelle + Tages-Detail)
- Markiert Konflikte mit existierenden Launches (Cart-Open-Überlappungen)

Fragt User:
- Soll der Launch gleich in den Quartalsbogen eingetragen werden? (ja/nein)
- Konflikt mit Bio-Check-Pilot-Phase 22.-29.5.? (Lösungsvorschlag: Bio-Check pausieren)

#### Modus 3 — `/jahresplan vorschau [monat]`

**Zweck:** Monats-Sicht — was kommt im Juni/Juli/etc.?

Liest:
- `context/jahresplan-2026.md`

Antwortet mit:
- Monats-Übersicht-Tabelle (Wochen-Spalten × Produkt-Zeilen)
- Konflikte/Überlappungen
- Ruhige Phasen (gut für Nesting/Audit/Pause)
- Empfohlene Next-Actions für Pre-Launch nächster Produkte

#### Modus 4 — `/jahresplan konflikt-check`

**Zweck:** Überlappende Aktivitäten identifizieren

Prüft:
- Cart-Open-Phasen aus active-funnels.json (alle Produkte)
- Live-Events (Webinar/Mastermind/Challenge)
- Patricia-Kapazität (z.B. „Patricia kann nicht 2 Live-Calls am gleichen Tag")

Antwortet mit:
- Liste aller Konflikte (Datum + Produkte)
- Lösungsvorschläge (verschieben, parallel laufen lassen, eines pausieren)

### 🗃 Modus 5 — Notion-Abgleich, gestrichen

Hier stand `/jahresplan notion-sync`. **Entfallen am 02.11.2026** — die Planung lebt
im Cockpit, es gibt keine zweite Stelle mehr, mit der abgeglichen werden müsste.

---

### Wie andere Skills den Jahresplan nutzen

#### `/content woche` (Wochen-Content)

Liest beim Start:
1. `context/jahresplan-2026.md` für Wochen-Kontext
2. `context/active-funnels.json` für Phase-Marker
3. Antwortet: „Diese Woche ist Mama-CEO Pre-Launch W2 + Bio-Check Tag 11. Empfohlene Pillars: Brandastic-Story (Mama-CEO) + Retargeting-Bio-Tipps (Bio-Check)."

#### `/reels` und `/karussell`

Lesen optional auf User-Befehl: „Schau in den Jahresplan und gib mir 3 Reel-Ideen für die kommende Mama-CEO-Pre-Launch-W3."

Liest dann:
1. Master-Datei (Wochen-Plan)
2. active-funnels.json (Pillar pro Phase)
3. Produkt-Briefing für Brand-Bausteine

#### `/funnel`

Liest beim Strategie-Modus:
- Master-Datei für Cart-Open-Konflikte
- active-funnels.json für ManyChat-Keyword-Konflikte

---

<!-- FRAGEN:ANFANG (aus scripts/jahresplan/fragen.json, nicht von Hand) -->

## Die Fragen, Zeitraum für Zeitraum

*Erzeugt aus `scripts/jahresplan/fragen.json` — nie hier von Hand ändern.*

### Jahr — Das grobe Gerüst

**Wann:** im Dezember, zusammen mit dem ersten Quartal

*Das Jahr bleibt grob: wann Ferien sind, welche Grundsatzthemen laufen, in welchen Monaten ein Angebot im Mittelpunkt steht und was am Ende zusammenkommen soll. Fein wird es erst im Quartal und im Monat.*

**1 · Rückblick — Wo stehst du?**

- **Was ist dieses Jahr richtig gut gelaufen?** — Denk an Beiträge, Gespräche, Verkäufe und an Momente, in denen es sich leicht angefühlt hat.
- **Was hat sich schwer angefühlt oder nicht funktioniert?** — Ehrlich, nur für dich. Das ist der wichtigste Teil.
- **Wie hat sich Posten für dich angefühlt?** (Auswahl: Leicht, ich hatte immer etwas zu sagen · Geht so, an manchen Tagen ein Krampf · Meistens eine Pflicht)
- **Wie lebendig ist deine Community?** (Auswahl: Ich bekomme jeden Tag Nachrichten · Ab und zu schreibt jemand · Es ist ziemlich still)
- **Welches Angebot fühlt sich nicht mehr stimmig an, und was würdest du daran ändern?** — Du musst nichts streichen. Oft reicht es, etwas umzubauen.
- **Wo steht dein Business gerade?** (Auswahl: Im Aufbau: Angebote und Abläufe entstehen noch · Im Verbessern: es steht, jetzt wird es leichter und besser · Ein bisschen von beidem)
- **Wie viele Stunden pro Woche hast du wirklich fürs Business?** — Nicht die Wunschzahl. Die Zahl, die mit Kindern, Job und Haushalt übrig bleibt.

**2 · Vision — Wofür willst du bekannt sein?**

- **Welche Frage soll jemand stellen, damit die Antwort dein Name ist?** — Zwei Menschen unterhalten sich. Die eine fragt: Kennst du jemanden, der mir bei … helfen kann? Die andere sagt deinen Namen. Wie lautet die Frage?
- **Was willst du nächstes Jahr unbedingt machen?** — Ein neuer Kanal, ein Event, ein eigenes Produkt, eine Reise. Schreib alles auf.
- **Dein Wort fürs neue Jahr** — Ein Wort, das du dir an den Kühlschrank hängen würdest.
- **Wie viel Umsatz wünschst du dir im ganzen Jahr?** — Freiwillig. Die Zahl hilft später beim Umsatz-Check.
- **Von 100 Interessierten kaufen bei dir ungefähr wie viele?** — Freiwillig und geschätzt reicht. Damit rechnet der Plan aus, wie viele Leute du für deine Verkäufe erreichen musst. Weisst du es nicht, lass es leer.

**3 · Leben zuerst — Was steht schon fest?**

- **Ferien und Wochen, in denen wenig geht** — Schulferien, Urlaub, Feiertage, Zeiten mit Besuch.
- **Feste Familien- und Herzenstermine** — Geburtstage, Feste, Ausflüge, der Hochzeitstag.
- **Wann ist deine Zeit für dich?** — Eine feste Zeit pro Woche, die dir gehört. Auch eine Stunde zählt.

**4 · Angebote — Was bietest du an?**

- Je Angebot: Name · Art · Herkunft · Preis · Wo steht die Person heute? · Wie sieht ihr Alltag danach aus? · Ein Satz, der das Angebot erklärt

**5 · Network — Was braucht dein Network-Ziel?**

- **Wie viel willst du im Monat aus dem Network verdienen?**
- **Wie viel verdienst du heute im Monat aus dem Network?**
- **Wie viel bleibt dir im Schnitt pro Person, die jeden Monat bei dir bestellt?** — Deine Provision auf die Bestellung, nicht der Bestellwert.
- **Wie viele Personen bestellen heute jeden Monat bei dir?**
- **Was bringt dir eine aktive Teampartnerin im Schnitt im Monat?** — Mit ihrer Kundschaft zusammen. Hast du noch kein Team, schätz, was in deinem Plan üblich ist, oder lass es leer.
- **Wie viele aktive Teampartnerinnen hast du heute?**
- **Was steht in deinem Vergütungsplan als Nächstes?** — Der nächste Rang, ein Bonus, was du dafür brauchst. Du kannst auch einfach die Seite aus deinem Vergütungsplan hineinkopieren. Das geht an deine KI mit.

**6 · Jahr — Was kommt wann?**

- Je Monat: Fokus-Angebot · Thema oder Veränderung, über die du sprichst · Kostenloses Angebot dazu · Wie viele Verkäufe planst du?

**7 · Woche — Wie sieht deine Woche aus?**

- **Wie viele Beiträge willst du pro Woche posten?** — Lieber wenige gute als viele schnelle.
- **An welchen Tagen postest du?**
- **Wie oft machst du Storys?** (Auswahl: Jeden Tag · An Arbeitstagen · Zwei- bis dreimal pro Woche)
- **Was soll in einer normalen Woche vorkommen?** — Zum Beispiel: etwas Persönliches, ein Tipp, eine Geschichte von jemandem, dem du geholfen hast, eine Einladung.

### Quartal — Die nächsten drei Monate schärfen

**Wann:** im letzten Monat des laufenden Quartals: März, Juni, September, Dezember

*Das Quartal erfindet nichts neu. Du nimmst deinen Jahresplan und machst ihn für die nächsten drei Monate scharf: welches Angebot wann, welches kostenlose Angebot davor, wann ein Workshop. Pläne darf man ändern - du steckst nicht fest.*

**1 · Rückblick — Was waren die letzten drei Monate?**

- **Was war dein grösster Erfolg in diesem Quartal?** — Eine Sache, nicht fünf. Es darf auch etwas Kleines sein, das sich gross angefühlt hat.
- **Auf welches Ergebnis bei einer Person, mit der du gearbeitet hast, bist du am stolzesten?** — Das ist dein Material für das nächste Quartal - und oft der Satz, der verkauft.
- **Was war schwer - und was hat geholfen?** — Beide Hälften aufschreiben. Die Lösung vergisst man sonst bis zum nächsten Mal.
- **Was willst du im nächsten Quartal anders machen?** — Ein Satz. Wenn dir fünf einfallen, nimm den, der am meisten ändert.

**2 · Die drei Monatsthemen — Woran arbeiten die nächsten drei Monate?**

- Je Monat: Thema des Monats · Was soll der Monat bewegen? · Fokus-Angebot · Kostenloses Angebot davor · Workshop oder Live-Termin

**3 · Was offen ist — Was aus dem Jahresplan liegt noch da?**

- **Was vom Jahresplan ist noch nicht passiert?** — Steht schon da, weil der Abgleich es gegen den Workspace geprüft hat. Du streichst, was nicht mehr gilt.  ·  steht schon da aus `planung-abgleich`
- **Was lässt du in diesem Quartal bewusst weg?** — Ohne diese Antwort wird aus einem Quartalsplan eine Wunschliste.

### Monat — Der Monat ganz ins Detail

**Wann:** am 29. des Vormonats  🔒 nur intern, geht in keine teilbare Seite

*Hier wird aus dem Quartalsthema ein Monat mit Beiträgen, Storys, Mails und Dreh-Liste. Die Zahlen des Vormonats und die Diagnose stehen schon da, wenn du anfängst - beantworten musst du nur die acht Fragen.*

**1 · Vormonats-Diagnose — Was die Zahlen sagen**

- **Zahlen des Vormonats** — Aus ThriveCart, der Instagram-Schnittstelle und ActiveCampaign.  ·  steht schon da aus `abgleich`
- **Was lief gut, was nicht** — Gegen den eigenen Median gerechnet, nicht absolut.  ·  steht schon da aus `gepostet`
- **Was war geplant und ist nicht passiert** — Belegt gegen den Workspace, nicht abgehakt.  ·  steht schon da aus `planung-abgleich`

**2 · Die acht Fragen — Zehn Minuten, dann steht der Monat**

- **Welche Säule prägt diesen Monat?** (Auswahl: Säule 1 (NWM 2.0) · Säule 2 (Hybridmodell) · Säule 3 (Mama Business) · Wake-Up · Mama-Körper 35+ · 4 Säulen · Mental Load · Identität) — Die ersten drei sind Mentoring, die übrigen doTERRA.
- **Welche drei Angebote werden beworben?** — Je eines kostenlos, klein und gross. Die Liste kommt aus dem Katalog - du wählst.  ·  steht schon da aus `katalog`
- **Wie verteilst du sie über die Wochen?** (Auswahl: Wochen-Blöcke: Woche 1 kostenlos, Woche 2 klein, Woche 3 und 4 gross · Tag-für-Tag gemischt) — Wochen-Blöcke sind der Normalfall. Gemischt lohnt sich, wenn das kostenlose Angebot laufend Eintragungen bringt.
- **Was ist die Hauptbotschaft des Monats?** — Ein bis zwei Sätze, die alle Beiträge verbinden. Wie ein Albumtitel.
- **Welcher Job-Mix?** (Auswahl: Standard · Verkaufs-Monat · Reichweite-Push · Geschichten-Monat · eigener Mix) — Standard heisst gleich viel Autorität und Geschichte, weniger Reichweite und Verkauf.
- **Was soll am Monatsende dastehen?** — Verkäufe, neue Followerinnen, Eintragungen über Stichwörter. Eine Zahl je Grösse, keine Wunschliste.
- **Was läuft diesen Monat bewusst NICHT?** — Vorschläge stehen schon da - aus dem Ideen-Vorrat. Du entscheidest, was wartet.  ·  steht schon da aus `ideen-vorrat`
- **Wie viele Wochen bist du wirklich arbeitsfähig?** — Ferien und Termine stehen schon da. Bei reduzierten Wochen wird mehr wiederverwendet und weniger neu gedreht.  ·  steht schon da aus `jahresplan`

### Woche — Der Rahmen für sieben Tage

**Wann:** Sonntagabend  🔒 nur intern, geht in keine teilbare Seite

*In der Woche entsteht kein neuer Content - der steht im Monatsplan. Hier wird nur gerahmt: Rückblick, Fokus, was je Säule dran ist, und die Ordnung. Was sich ableiten lässt, steht schon da.*

**1 · Die Woche, die war — Erfolge und Herausforderungen**

- **Was waren deine Erfolge in der letzten Woche?** — Aus den Learnings der sieben Tage zusammengezogen.  ·  steht schon da aus `tagebuch`
- **Was waren deine Herausforderungen in der letzten Woche?** — Dazu, was geholfen hat - sonst steht beim nächsten Mal dasselbe da.  ·  steht schon da aus `tagebuch`

**2 · Die Woche, die kommt — Fokus, Angebot, Aufruf**

- **Was ist dein Fokus für diese Woche?** — Ein Satz. Woran merkst du am Sonntag, dass die Woche gut war?
- **Welches Angebot steht diese Woche im Mittelpunkt?**  ·  steht schon da aus `monatsplan`
- **Welcher Aufruf läuft diese Woche?** — Das Stichwort oder der Link, auf den die Beiträge zeigen.  ·  steht schon da aus `monatsplan`
- **In welcher Phase steht der Verkauf?** — Anwärmen, Türen auf, läuft, letzter Tag, danach - oder nichts davon.  ·  steht schon da aus `monatsplan`

**3 · Was planst du je Business-Säule? — Fünf Zeilen, je ein Satz**

- Je Säule (Kundenarbeit · Produktentwicklung · Business-Struktur aufbauen · Content-Creation · Weiterbildung): Was ist dran?

**4 · Die Woche einteilen — Termine, Aufgaben, Tage**

- [ ] Hauptkalender angeschaut: welche Termine stehen diese Woche an?  ·  wird gesetzt aus `termine`
- [ ] Regelmässige Aufgaben eingeplant
- [ ] Offene Aufgaben auf die Wochentage verteilt  ·  wird gesetzt aus `aufgaben`
- [ ] Überfällige Aufgaben neu terminiert  ·  wird gesetzt aus `aufgaben`
- [ ] Fehlende Aufgaben ergänzt

**5 · Ausblick auf zwei Wochen — Was kommt danach?**

- **Welche Termine stehen in den nächsten zwei Wochen - und musst du dich auf etwas vorbereiten?** — Steht schon da. Du ergänzt nur, was Vorbereitung braucht.  ·  steht schon da aus `termine`
- **Wann ist diese Woche Zeit für dich?** — Als Termin, nicht als Absicht. Was nicht im Kalender steht, kommt nicht.

**6 · Ordnungsroutinen — Was aufgeräumt gehört**

- [ ] Download-Ordner geleert und abgelegt  ·  wird gesetzt aus `downloads-aufraeumen.py`
- [ ] Mails durchgesehen und sortiert  ·  wird gesetzt aus `mails-sortieren-donnerstag`
- [ ] Kundendaten aktuell  ·  wird gesetzt aus `cockpit-kundinnen`
- [ ] Content für die Woche steht  ·  wird gesetzt aus `monatsplan`
- [ ] Browser-Tabs geschlossen, Wichtiges gespeichert
- [ ] Papiernotizen durchgegangen und übertragen

<!-- FRAGEN:ENDE -->

---

## Was dieser Skill NICHT macht

- **Den Content selbst.** Den baut `/content monat` — `/planen` setzt den Rahmen und
  übergibt ihn.
- **Die Engpass-Frage.** Das ist `/strategie`: „was bringt gerade am meisten“ ist kein
  Zeitraum.
- **Das Private.** Haushalts-Liste und Garten bleiben, wo sie sind.
- **Nach Notion schreiben.** Nie.

## Regeln

- **Keine erfundenen Zahlen, Termine oder Preise.** Was nicht belegt ist, bleibt leer
  und wird als Frage gestellt.
- **Ferien und Termine sind keine Vorhaben** — sie begrenzen den Plan, sie füllen ihn
  nicht.
- **Ein Plan darf sich ändern.** Eine neue Idee darf das Quartal umwerfen; dann wird
  der Bogen neu geschrieben, nicht ein zweiter angelegt.
- **Was Patricia getippt hat, gewinnt.** Ein vorbelegtes Feld wird überschrieben, ein
  von ihr geändertes nie.

## 🔗 Verwandte

- `plans/2026-11-02-planungs-kreislauf.md` — der Bauplan dazu
- `/content monat` — baut die Beiträge aus dem Monatsbogen
- `/strategie` — die Engpass-Frage über allen Zeiträumen
- `/angebot` — baut ein Angebot, das hier als Fokus auftaucht
