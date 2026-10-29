---
name: jahresplan
description: "Jahresplanung: führt Schritt für Schritt durch Rückblick, Vision, Leben, Angebote, Jahr und Woche und macht daraus den Jahresplan mit Monats- und Wochenthemen (Modus planen). Dazu die Master-Sicht über alle Launches in context/jahresplan-2026.md, gelesen von /content woche, /reels, /karussell."
---
# /jahresplan — Master-Jahresplanung für Mum Life Balance

**Skill-Status:** SPEC (zu bauen ab nächster Session)
**Master-Datei:** `context/jahresplan-2026.md` (TBD — wird vom Skill erstellt)
**Phase-Tracker:** `context/active-funnels.json` (existiert, wird parallel gepflegt)
**Notion-DB:** TBD (Patricia liefert DB-ID beim ersten Lauf)

---

## Was dieser Skill macht

Der `/jahresplan`-Skill ist die **EINE Wahrheit** für „Wann passiert was im Jahr". Er aggregiert alle Launches, Produkte, Kampagnen und parallel laufenden Aktivitäten (Mentoring + doTERRA) in einer Tag-für-Tag-Sicht.

**Datenfluss:**

```
/produkt erstellt outputs/produkte/[slug]/07-launch-kalender.md
        ↓
/jahresplan launch [slug]  →  fügt Launch-Phasen ins Master-Markdown
        ↓
context/jahresplan-2026.md  ←→  Notion-Jahresplanung-DB
        ↓
`/content woche` · /reels · /karussell lesen Master + active-funnels.json
        ↓
Content-Skills wissen Tagesgenau, wo wir stehen
```

## Modus 0 — `/jahresplan planen` · das Jahr neu planen (seit 26.10.2026)

Patricia: *„es soll einfach für alle umsetzbar sein … von denen die wie ich so stark mit Claude
arbeiten und die, die es noch nicht tun"*. Deshalb gibt es **dieselben Fragen auf zwei Wegen**:

| Weg | Für wen | Wo |
|---|---|---|
| **Seite ohne Anmeldung** | alle, auch ohne Claude | `outputs/produkte/jahresplanung/jahresplaner.html`, als Artifact veröffentlicht, kostenlos |
| **dieser Modus** | wer mit Claude arbeitet (Patricia, MBA, Mama-CEO) | hier, im Gespräch |

Die Fragen stehen nur in `scripts/jahresplan/fragen.json`. `python scripts/jahresplan/tool-bauen.py`
baut daraus die Seite **und** den Block unten. Eine Frage ändern heisst: dort ändern, Skript laufen
lassen. Nie hier oder in der Seite von Hand.

### So läuft das Gespräch

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

### Lücken-Check — vor dem Ergebnis, Pflicht

Patricia: *„dass er merkt anhand des einkommensziels muss man so oder soviel umsetzen … wo hat der
funnel eine lücke, wo müsste man was zusätzliches entwickeln, wie könnte man mehr geld reinholen"*.
Die Seite rechnet denselben Check mit festen Regeln (`luecken()` in `tool-vorlage.html`). Im Gespräch
gehst du weiter und begründest jede Lücke.

**Zuerst lesen, wenn vorhanden:** `.claude/skills/strategie/wissen/julia-stufen.md` und
`julia-evergreen.md` (Julias 10k- und 20k-Masterclass, „Road to 50K“, 100k Blueprint, gitignored).
Einen eigenen 5k-Kurs gibt es im Material nicht, die Stufe 0 → 5k ist aus ihren Rückblicken
zusammengesetzt. Fehlt der Ordner (weitergegebener Skill), gelten die Kurzregeln unten.
🚨 In nichts, was eine Kundin liest, steht Julias Name. Die Regeln werden in eigenen Worten erklärt.

**1 · Stufe aus dem Monatsziel** (Jahresziel ÷ 12; „k“ heisst bei Julia Monatsumsatz):

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

### Network — mit den eigenen Zahlen, weil jeder Vergütungsplan anders ist

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

### Ergebnis

Eine Datei `plans/jahresplan-<jahr>.md` (bei Patricia; bei Kundinnen in ihrem eigenen Workspace) mit:
zwölf Monaten (Fokus · Thema · kostenloses Angebot · Vorbereitung bis · geplanter Umsatz), vier
Wochenthemen je Monat, einer Beispielwoche und dem Umsatz-Check. Patricias eigener Plan geht danach
über Modus 2 in die Master-Sicht.

### Regeln

- **Veränderung statt Zahlen:** nie Modul-, Kapitel- oder Lektionszahlen als Verkaufsargument.
- **Die Kundschaft der Kundin heisst nie „Kundin“** — Leute, Person, für wen du da bist.
- Warme, einfache Sprache, Schweizer ss, kein Stakkato.
- Die Herkunft der Struktur bleibt intern: `wissen/` ist gitignored und geht nie mit, wenn der Skill
  weitergegeben wird. In nichts, was eine Kundin liest, steht ein fremder Name.

### Die Fragen

<!-- FRAGEN:ANFANG (aus scripts/jahresplan/fragen.json, nicht von Hand) -->

### Schritt 1 · Rückblick — Wo stehst du?

*Bevor du nach vorne planst, schau ehrlich zurück. Was gut lief, darf bleiben. Was schwer war, darf sich ändern.*

- **Was ist dieses Jahr richtig gut gelaufen?** — Denk an Beiträge, Gespräche, Verkäufe und an Momente, in denen es sich leicht angefühlt hat.
- **Was hat sich schwer angefühlt oder nicht funktioniert?** — Ehrlich, nur für dich. Das ist der wichtigste Teil.
- **Wie hat sich Posten für dich angefühlt?** (Auswahl: Leicht, ich hatte immer etwas zu sagen · Geht so, an manchen Tagen ein Krampf · Meistens eine Pflicht)
- **Wie lebendig ist deine Community?** (Auswahl: Ich bekomme jeden Tag Nachrichten · Ab und zu schreibt jemand · Es ist ziemlich still)
- **Welches Angebot fühlt sich nicht mehr stimmig an, und was würdest du daran ändern?** — Du musst nichts streichen. Oft reicht es, etwas umzubauen.
- **Wo steht dein Business gerade?** (Auswahl: Im Aufbau: Angebote und Abläufe entstehen noch · Im Verbessern: es steht, jetzt wird es leichter und besser · Ein bisschen von beidem)
- **Wie viele Stunden pro Woche hast du wirklich fürs Business?** — Nicht die Wunschzahl. Die Zahl, die mit Kindern, Job und Haushalt übrig bleibt.

### Schritt 2 · Vision — Wofür willst du bekannt sein?

*Jetzt darfst du gross denken. Logisch muss hier noch nichts sein.*

- **Welche Frage soll jemand stellen, damit die Antwort dein Name ist?** — Zwei Menschen unterhalten sich. Die eine fragt: Kennst du jemanden, der mir bei … helfen kann? Die andere sagt deinen Namen. Wie lautet die Frage?
- **Was willst du nächstes Jahr unbedingt machen?** — Ein neuer Kanal, ein Event, ein eigenes Produkt, eine Reise. Schreib alles auf.
- **Dein Wort fürs neue Jahr** — Ein Wort, das du dir an den Kühlschrank hängen würdest.
- **Wie viel Umsatz wünschst du dir im ganzen Jahr?** — Freiwillig. Die Zahl hilft später beim Umsatz-Check.
- **Von 100 Interessierten kaufen bei dir ungefähr wie viele?** — Freiwillig und geschätzt reicht. Damit rechnet der Plan aus, wie viele Leute du für deine Verkäufe erreichen musst. Weisst du es nicht, lass es leer.

### Schritt 3 · Leben zuerst — Was steht schon fest?

*Dein Business passt sich deinem Leben an, nicht umgekehrt. Trag zuerst ein, was nicht verhandelbar ist.*

- **Ferien und Wochen, in denen wenig geht** — Schulferien, Urlaub, Feiertage, Zeiten mit Besuch.
- **Feste Familien- und Herzenstermine** — Geburtstage, Feste, Ausflüge, der Hochzeitstag.
- **Wann ist deine Zeit für dich?** — Eine feste Zeit pro Woche, die dir gehört. Auch eine Stunde zählt.

### Schritt 4 · Angebote — Was bietest du an?

*Schreib alle deine Angebote auf, vom kostenlosen bis zum grössten. Noch nichts Eigenes? Dann trag ein, was dein Network schon hat: eine Testwoche mit Proben als kostenlosen Einstieg, ein Starterset als kleines Angebot, die Einschreibung mit Treueprogramm als grosses. Das Angebot ist das Werkzeug. Die Veränderung bei den Leuten, für die du da bist, ist das Ziel.*

- Je Angebot: Name · Art · Herkunft · Preis · Wo steht die Person heute? · Wie sieht ihr Alltag danach aus? · Ein Satz, der das Angebot erklärt

### Schritt 5 · Network — Was braucht dein Network-Ziel?

*Jedes Network zahlt anders, deshalb rechnet der Plan mit deinen eigenen Zahlen. Du findest sie in deiner Monatsabrechnung. Geschätzt reicht. Bist du nicht im Network, überspring diesen Schritt.*

- **Wie viel willst du im Monat aus dem Network verdienen?**
- **Wie viel verdienst du heute im Monat aus dem Network?**
- **Wie viel bleibt dir im Schnitt pro Person, die jeden Monat bei dir bestellt?** — Deine Provision auf die Bestellung, nicht der Bestellwert.
- **Wie viele Personen bestellen heute jeden Monat bei dir?**
- **Was bringt dir eine aktive Teampartnerin im Schnitt im Monat?** — Mit ihrer Kundschaft zusammen. Hast du noch kein Team, schätz, was in deinem Plan üblich ist, oder lass es leer.
- **Wie viele aktive Teampartnerinnen hast du heute?**
- **Was steht in deinem Vergütungsplan als Nächstes?** — Der nächste Rang, ein Bonus, was du dafür brauchst. Du kannst auch einfach die Seite aus deinem Vergütungsplan hineinkopieren. Das geht an deine KI mit.

### Schritt 6 · Jahr — Was kommt wann?

*Ein Fokus pro Monat. Dazu ein kostenloses Angebot, das zum Thema passt. In Ferienmonaten darf der Fokus klein sein oder ganz fehlen.*

- Je Monat: Fokus-Angebot · Thema oder Veränderung, über die du sprichst · Kostenloses Angebot dazu · Wie viele Verkäufe planst du?

### Schritt 7 · Woche — Wie sieht deine Woche aus?

*Der Monatsfokus wird erst in der Woche lebendig. Ein fester Rhythmus nimmt dir jeden Morgen die Frage ab, was du heute erzählst.*

- **Wie viele Beiträge willst du pro Woche posten?** — Lieber wenige gute als viele schnelle.
- **An welchen Tagen postest du?**
- **Wie oft machst du Storys?** (Auswahl: Jeden Tag · An Arbeitstagen · Zwei- bis dreimal pro Woche)
- **Was soll in einer normalen Woche vorkommen?** — Zum Beispiel: etwas Persönliches, ein Tipp, eine Geschichte von jemandem, dem du geholfen hast, eine Einladung.

<!-- FRAGEN:ENDE -->

---

## Modi für die Master-Sicht

### 🛑 Vor jedem Modus: den Workspace-Abgleich lesen

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

### Modus 1 — `/jahresplan status`

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

### Modus 2 — `/jahresplan launch [produkt-slug]`

**Zweck:** Neuen Launch in Master-Markdown eintragen

Liest:
- `outputs/produkte/[slug]/07-launch-kalender.md` (alle Phasen + Daten)
- `outputs/produkte/[slug]/00-briefing-FINAL.md` (Tagline + Preise)

Schreibt:
- Phasen ins `context/jahresplan-2026.md` (Monats-Tabelle + Tages-Detail)
- Markiert Konflikte mit existierenden Launches (Cart-Open-Überlappungen)

Fragt User:
- Soll Notion-DB-Eintrag synchron erstellt werden? (ja/nein)
- Konflikt mit Bio-Check-Pilot-Phase 22.-29.5.? (Lösungsvorschlag: Bio-Check pausieren)

### Modus 3 — `/jahresplan vorschau [monat]`

**Zweck:** Monats-Sicht — was kommt im Juni/Juli/etc.?

Liest:
- `context/jahresplan-2026.md`

Antwortet mit:
- Monats-Übersicht-Tabelle (Wochen-Spalten × Produkt-Zeilen)
- Konflikte/Überlappungen
- Ruhige Phasen (gut für Nesting/Audit/Pause)
- Empfohlene Next-Actions für Pre-Launch nächster Produkte

### Modus 4 — `/jahresplan konflikt-check`

**Zweck:** Überlappende Aktivitäten identifizieren

Prüft:
- Cart-Open-Phasen aus active-funnels.json (alle Produkte)
- Live-Events (Webinar/Mastermind/Challenge)
- Patricia-Kapazität (z.B. „Patricia kann nicht 2 Live-Calls am gleichen Tag")

Antwortet mit:
- Liste aller Konflikte (Datum + Produkte)
- Lösungsvorschläge (verschieben, parallel laufen lassen, eines pausieren)

### Modus 5 — `/jahresplan notion-sync`

**Zweck:** Manueller Sync mit Notion-Jahresplanung-DB

Liest:
- `context/jahresplan-2026.md` (Quelle)
- Notion-DB-ID (aus User-Input oder gespeicherter Konfig)

Schreibt:
- Neue/aktualisierte Pages in Notion-Jahresplanung-DB
- Verknüpfungen zu Notion-Produkte-DB
- Updated `_meta.last_sync_with_notion` in Master-Markdown

---

## Datei-Struktur `context/jahresplan-2026.md` (zu erstellen)

```markdown
# Jahresplan 2026 — Master-Sicht Mum Life Balance

**Stand:** 2026-05-XX
**Letzte Aktualisierung:** [Datum]
**Quelle der Wahrheit:** Diese Datei + `active-funnels.json`
**Notion-Sync:** [Datum + DB-Link]

## Q1 (Jan-Mrz) — RÜCKBLICK
[Zusammenfassung: was lief, was Lehre gezogen]

## Q2 (Apr-Jun) — AKTIV
### April 2026
[Bio-Check Launch]

### Mai 2026
**Hauptfokus:** Mama-CEO Pilot-Launch
**Mit Bio-Check parallel** (Tag 8-30 Pilot-Phase)

#### KW 19 (2.-8.5.)
| Tag | Mama-CEO | Bio-Check | doTERRA | Notes |
|---|---|---|---|---|
| Do 2.5. | Story-Umfrage Tagline-A/B | Tag 8 | — | Beide Profile aktiv |
| Fr 3.5. | Urmotiv-Call #1 | — | — | |
[...]

#### KW 22 (Launch-Week)
[...]

### Juni 2026
[Premium 1:1 Strategie-Skill aufsetzen, Säule-3-Pilot läuft, Säule 4-Aufnahmen]

## Q3 (Jul-Sep) — GEPLANT
[Mama-CEO Final-Launch September, Säulen-Auslieferung Pilot]

## Q4 (Okt-Dez) — VORLÄUFIG
[Premium 1:1 Launch, Minikurse extrahieren]
```

---

## Wie andere Skills den Jahresplan nutzen

### `/content woche` (Wochen-Content)

Liest beim Start:
1. `context/jahresplan-2026.md` für Wochen-Kontext
2. `context/active-funnels.json` für Phase-Marker
3. Antwortet: „Diese Woche ist Mama-CEO Pre-Launch W2 + Bio-Check Tag 11. Empfohlene Pillars: Brandastic-Story (Mama-CEO) + Retargeting-Bio-Tipps (Bio-Check)."

### `/reels` und `/karussell`

Lesen optional auf User-Befehl: „Schau in den Jahresplan und gib mir 3 Reel-Ideen für die kommende Mama-CEO-Pre-Launch-W3."

Liest dann:
1. Master-Datei (Wochen-Plan)
2. active-funnels.json (Pillar pro Phase)
3. Produkt-Briefing für Brand-Bausteine

### `/funnel`

Liest beim Strategie-Modus:
- Master-Datei für Cart-Open-Konflikte
- active-funnels.json für ManyChat-Keyword-Konflikte

---

## Implementierungs-TODO (für nächste Session)

1. **`context/jahresplan-2026.md` v0 anlegen** mit aktuellen Q1-Q2-Daten (Bio-Check + Mama-CEO + doTERRA-Plätze leer)
2. **Skill-Logik in claude-Hooks** integrieren (lesen + schreiben automatisiert)
3. **Notion-DB-ID** von Patricia holen — welche existiert (Jahresplanung)?
4. **Notion-Sync-Mechanismus** definieren (push vs. pull, manuell vs. automatisch)
5. **CLAUDE.md** updaten (Skill in Commands-Sektion ergänzen)
6. **Stop-Hook erweitern** (`stop-hook-git-check.sh`) — bei Master-Datei-Änderungen Notion-Sync vorschlagen

---

## Patricia-Hinweise

- Du musst NICHTS manuell synchronisieren — Skills lesen automatisch
- Wenn du dem Content-Assistenten sagen willst „schau in den Jahresplan", reicht das — die Skills wissen wo
- Notion-Update läuft via `/jahresplan notion-sync` (manuell, einmal pro Woche)
- Konfliktwarnung: bevor du `/produkt launch` machst, läuft auto-Konflikt-Check

---

**Status:** Skill-Spec, Implementierung erfolgt in nächster Session sobald Patricia die Notion-Jahresplanung-DB-ID liefert.
