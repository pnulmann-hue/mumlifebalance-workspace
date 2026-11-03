# -*- coding: utf-8 -*-
"""Baut .claude/skills/planen/SKILL.md aus den Abschnitten von /jahresplan und /monatsplan.

Schritt 2 des Plans plans/2026-11-02-planungs-kreislauf.md. Die uebernommenen
Abschnitte werden woertlich aus den Quell-Skills geschnitten, damit nichts neu
erfunden wird; nur der Rahmen (vier Zeitraeume, Cockpit statt Notion) ist neu.

Wiederholbar. Der Fragenblock selbst kommt aus scripts/jahresplan/tool-bauen.py
zwischen den FRAGEN-Marken - dieses Skript legt die Marken nur an.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
WURZEL = Path(__file__).resolve().parents[2]
JAHR = WURZEL / ".claude" / "skills" / "jahresplan" / "SKILL.md"
MONAT = WURZEL / ".claude" / "skills" / "monatsplan" / "SKILL.md"
ZIEL = WURZEL / ".claude" / "skills" / "planen" / "SKILL.md"

ANFANG = "<!-- FRAGEN:ANFANG (aus scripts/jahresplan/fragen.json, nicht von Hand) -->"
ENDE = "<!-- FRAGEN:ENDE -->"


def abschnitt(datei: Path, ueberschrift: str) -> str:
    """Schneidet einen Abschnitt heraus: ab der Ueberschrift bis zur naechsten
    gleicher oder hoeherer Ebene. Fehlt sie, bricht der Bau ab - ein stilles
    Weglassen hat am 19.09. einen Baustein um 1'100 Zeichen schrumpfen lassen."""
    text = datei.read_text(encoding="utf-8")
    zeilen = text.split("\n")
    treffer = [i for i, z in enumerate(zeilen) if z.strip() == ueberschrift.strip()]
    assert len(treffer) == 1, "%s: '%s' %d Mal gefunden" % (datei.name, ueberschrift, len(treffer))
    start = treffer[0]
    ebene = len(re.match(r"#+", zeilen[start]).group(0))
    for i in range(start + 1, len(zeilen)):
        m = re.match(r"(#+) ", zeilen[i])
        if m and len(m.group(1)) <= ebene:
            return "\n".join(zeilen[start:i]).rstrip() + "\n"
    return "\n".join(zeilen[start:]).rstrip() + "\n"


def tiefer(text: str) -> str:
    """Schiebt alle Ueberschriften eine Ebene nach unten, damit die uebernommenen
    Abschnitte unter die neuen Zeitraum-Kapitel passen."""
    return re.sub(r"^(#+) ", lambda m: "#" + m.group(1) + " ", text, flags=re.MULTILINE)


# Die Quell-Skills nennen die Mentorin namentlich. Dieser Skill liegt im oeffentlichen
# Repo und soll im KI-Kurs weitergegeben werden - der Name kommt beim Uebernehmen
# heraus, die Mechanik bleibt Wort fuer Wort stehen. Reihenfolge zaehlt: die laengeren
# Wendungen zuerst, sonst bleibt ein halber Satz stehen.
NAMEN_RAUS = [
    ("`julia-evergreen.md` (Julias 10k- und 20k-Masterclass, „Road to 50K“, 100k Blueprint, gitignored).",
     "das Stufen-Material in `.claude/skills/strategie/wissen/` (gitignored, zugekauft)."),
    ("\U0001F6A8 In nichts, was eine Kundin liest, steht Julias Name. Die Regeln werden in eigenen Worten erklärt.",
     "\U0001F6A8 In nichts, was eine Kundin liest, steht der Name der Mentorin. Die Regeln werden in eigenen Worten erklärt."),
    ("(Jahresziel ÷ 12; „k“ heisst bei Julia Monatsumsatz)",
     "(Jahresziel ÷ 12; „k“ heisst dort Monatsumsatz, nicht Jahresumsatz)"),
    ("**im Launch** nach dem Julia-Launch-Drehbuch (`story-plan.json` + `julia-launch-story-bausteine.md`), **sonst** nach den Julia-Story-Vorlagen (`julia-insta-stories-anleitung.md` etc.)",
     "**im Launch** nach dem Launch-Drehbuch (`story-plan.json` + die Launch-Story-Bausteine), **sonst** nach den Story-Vorlagen in `context/`"),
    ("**kein „Julia Trost\"-Name in Kunden-Output**",
     "**kein Mentorinnen-Name in Kunden-Output**"),
    ("kein „Julia\"-Name im Kunden-Output",
     "kein Mentorinnen-Name im Kunden-Output"),
]


# Die Quell-Skills lesen Plan und Wochenfokus aus Notion. Seit dem 02.11.2026 liegen
# beide im Cockpit (Patricia: "ich will nichts mehr in notion"). Der Umzug passiert
# hier beim Uebernehmen, damit im Skill keine Notion-Quelle mehr steht. Historische
# Saetze ("es stand so in Notion", "kam einmalig aus Notion") bleiben - die erklaeren,
# warum etwas so ist, und zeigen nirgends hin.
NOTION_RAUS = [
    ("8. **Vormonats-Notion-Plan** (falls vorhanden): Welche Ziele wurden erreicht, welche nicht",
     "8. **Monatsbogen des Vormonats** (`daten/monatsbogen` im Cockpit): Welche Ziele wurden erreicht, welche nicht"),
    ("14. **Wochenpläne der aktuellen Monatswochen aus Notion** (Wochenplanung-DB) — Fokus + Produkt + Wochen-CTA (vom Story-Bot/uns gesetzt) → die Content-Ideen müssen dazu passen",
     "14. **Der Quartalsbogen** (`daten/quartalsbogen`) — Monatsthema, Fokus-Angebot und Workshop-Termin → die Content-Ideen müssen dazu passen"),
    ("### 2b) Notion-Monatsplan vom Vormonat lesen",
     "### 2b) Den Monatsbogen des Vormonats lesen"),
    ("Notion-DB: `collection://2ae7078e-8b7e-81fc-acf7-000be291c92c`",
     "Im Cockpit: `daten/monatsbogen` (gerechnet) und `daten/monatsbogen-notizen` (ihre Texte)"),
    ("Baut auf den Wochenplänen aus Notion auf (Fokus + Produkt + CTA pro Woche).",
     "Baut auf dem Quartalsbogen auf (Monatsthema + Fokus-Angebot + kostenloses Angebot davor)."),
    ("Für **jede Woche** des Monats (Fokus + Produkt + CTA aus dem Notion-Wochenplan), je Beitrag mit",
     "Für **jede Woche** des Monats (Fokus + Produkt + Aufruf werden hier festgelegt und wandern in den Wochenbogen), je Beitrag mit"),
    ("- Soll Notion-DB-Eintrag synchron erstellt werden? (ja/nein)",
     "- Soll der Launch gleich in den Quartalsbogen eingetragen werden? (ja/nein)"),
]


def namen_raus(text: str) -> str:
    for alt, neu in NAMEN_RAUS + NOTION_RAUS:
        text = text.replace(alt, neu)
    return text


KOPF = """---
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
"""

SCHLUSS = """
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
"""


def bauen() -> str:
    teile = [KOPF]

    # ---- Jahr
    teile.append("## Jahr\n\n*Im Dezember, zusammen mit dem ersten Quartal.*\n\n")
    teile.append(namen_raus(tiefer(abschnitt(JAHR, "### So läuft das Gespräch"))))
    teile.append("\n")
    teile.append(namen_raus(tiefer(abschnitt(JAHR, "### Lücken-Check — vor dem Ergebnis, Pflicht"))))
    teile.append("\n")
    teile.append(namen_raus(tiefer(abschnitt(
        JAHR, "### Network — mit den eigenen Zahlen, weil jeder Vergütungsplan anders ist"))))
    teile.append("\n")
    teile.append(namen_raus(tiefer(abschnitt(JAHR, "### Ergebnis"))))
    teile.append("\n---\n\n")

    # ---- Quartal (neu, deshalb hier im Klartext - es gibt keine Quelle dafuer)
    teile.append("""## Quartal

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

""")

    # ---- Monat
    teile.append("## Monat\n\n*Am 29. des Vormonats. Der Lauf legt die Zahlen und die "
                 "Diagnose vorher hin — zu beantworten sind nur die acht Fragen.*\n\n")
    for titel in ["## Phase 1 · Pflicht-Lektüre (5 Min, still)",
                  "## Phase 2 · Vormonats-Diagnose (10 Min)",
                  "## Phase 4 · Plan generieren (5 Min, still)",
                  "## Phase 4.5 · Monats-Content-Vorplanung (NEU — der eigentliche Content)"]:
        teile.append(namen_raus(tiefer(abschnitt(MONAT, titel))))
        teile.append("\n")

    teile.append("""### Phase 5 · Ablegen — im Cockpit, nicht in Notion

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

""")

    # ---- Woche
    teile.append("""## Woche

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

""")

    # ---- Master-Sicht aus /jahresplan
    teile.append("## Die Master-Sicht über alle Zeiträume\n\n")
    teile.append(namen_raus(tiefer(abschnitt(JAHR, "### 🛑 Vor jedem Modus: den Workspace-Abgleich lesen"))))
    teile.append("\n")
    for titel in ["### Modus 1 — `/jahresplan status`",
                  "### Modus 2 — `/jahresplan launch [produkt-slug]`",
                  "### Modus 3 — `/jahresplan vorschau [monat]`",
                  "### Modus 4 — `/jahresplan konflikt-check`"]:
        teile.append(namen_raus(tiefer(abschnitt(JAHR, titel))))
        teile.append("\n")
    teile.append("""### 🗃 Modus 5 — Notion-Abgleich, gestrichen

Hier stand `/jahresplan notion-sync`. **Entfallen am 02.11.2026** — die Planung lebt
im Cockpit, es gibt keine zweite Stelle mehr, mit der abgeglichen werden müsste.

---

""")
    teile.append(namen_raus(tiefer(abschnitt(JAHR, "## Wie andere Skills den Jahresplan nutzen"))))

    teile.append("\n" + ANFANG + "\n" + ENDE + "\n")
    teile.append(SCHLUSS)
    return "".join(teile)


text = bauen()
ZIEL.parent.mkdir(parents=True, exist_ok=True)

# Marken fuer tool-bauen.py muessen genau einmal drinstehen
assert text.count(ANFANG) == 1 and text.count(ENDE) == 1, "FRAGEN-Marken fehlen oder doppelt"
# Keine fremden Namen - der Skill wird im KI-Kurs leer weitergegeben
for verboten in ["Julia", "Trost", "Hersche", "Pejic"]:
    assert verboten not in text, "fremder Name im Skill: %s" % verboten
# Notion darf nur noch historisch oder als Verbot vorkommen, nie als Quelle.
# Diese Wendungen sind geprueft und erlaubt - alles andere laesst den Bau abbrechen.
HARMLOS = (
    "nichts in Notion", "mehr in notion", "Lesen aus Notion", "nicht in Notion",
    "stand so in Notion", "kam einmalig aus Notion", "Notion-Content-DB ist abgel",
    "Notion-Monatsplan-Page", "mehr nach Notion", "Notion-Abgleich, gestrichen",
    "notion-sync", "Nach Notion schreiben",
    'git grep -n "notion"',   # die Gegenprobe im Skill selbst
)
# Muster eng fassen: "otion" faengt auch "Emotion" - am 02.11. beim ersten Lauf passiert.
NOTION = re.compile(r"\bnotion\b", re.I)
for zeile in text.splitlines():
    if not NOTION.search(zeile):
        continue
    assert any(h in zeile for h in HARMLOS), "Notion als Quelle: %s" % zeile.strip()[:90]
# Schweizer ss
assert "ß" not in text, "deutsches scharfes s im Skill"

ZIEL.write_text(text, encoding="utf-8")
print("  %s (%d Zeilen, %d Zeichen)" % (ZIEL.name, text.count("\n") + 1, len(text)))
print("  Fragenblock einsetzen: python scripts/jahresplan/tool-bauen.py")
