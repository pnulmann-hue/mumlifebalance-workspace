#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Baut die vier Content-Befehle, die im KI-Kurs unter Lektion 7.1 liegen.

    python scripts/ki-kurs/content-maschinen-bauen.py [--zip]

Ergebnis: outputs/produkte/ki-treppe/content-maschinen/Content-Maschinen/
Patricia zieht den Ordner einmal in den Drive-Kursordner, danach kommt die
Kennung als `content_maschinen_zip` in `beilagen-drive.json`.

Warum ein Ordner und kein Google Doc: Das sind sieben Dateien in einer
Ordnerstruktur, die genau so im Arbeitsplatz liegen muss. Dasselbe Muster wie
das Arbeitsplatz-Grundgeruest aus 4.3. Und es ist unbedenklich, anders als eine
startbare Vorlage: eine SKILL.md ist Text, den Claude Code liest — es braucht
keine Laufzeit, die im Kurs niemand einrichtet.

🚨 Der Kurs liefert die Skills LEER aus. Das ist kein Sparen, das ist das
   Konzept („Maschine gegen Treibstoff", siehe 02-kurs-konzept.md): die
   Mechanik ist hier drin, der Inhalt ist ihre Arbeit. Deshalb kommt hier
   NICHTS von Patricias Wissen hinein — keine Hook-Formeln, keine Caption-
   Formeln, keine Beispiele aus ihrem Feed, keine Zahlen, keine Angebote.
   Und erst recht nichts aus zugekauften Kursen.

🚨 Jede der vier Dateien zeigt die SECHS TEILE aus Lektion 5.2 in genau der
   Reihenfolge, in der sie dort stehen. Das ist der Lerneffekt: sie hat die
   sechs Teile gehoert und sieht sie hier viermal wieder. Ein siebter
   Abschnitt („Der letzte Check") ist dabei und ausdruecklich als Zugabe
   markiert — sonst zaehlt jemand sieben und sucht, was sie verpasst hat.

🚨 Schweizer ss, nie ein deutsches ss-Zeichen. Das Skript prueft es am Ende.
"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

WURZEL = Path(__file__).resolve().parents[2]
ZIEL = (WURZEL / "outputs" / "produkte" / "ki-treppe" / "content-maschinen"
        / "Content-Maschinen")

# ── Der gemeinsame Kopf jeder SKILL.md ───────────────────────────────
# Die vier Wissensdateien aus Modul 2 heissen im Grundgeruest aus 4.3 genau
# so. Wer sie dort anders benannt hat, aendert es hier mit.
LIEST = """## Bevor du anfängst

Lies diese Dateien, bevor du irgendetwas schreibst:

- `context/business-brief.md` — wer du bist und für wen du da bist
- `context/meine-stimme.md` — deine Textproben
- `context/verbotene-woerter.md` — was nie vorkommen darf
- `context/meine-kundin.md` — wen du vor dir siehst
- `context/was-bei-mir-funktioniert.md` — was schon einmal gut lief

🚨 **Fehlt eine davon, sag es mir, bevor du anfängst.** Rate nicht, was
dringestanden hätte — ein geratener Brief klingt nach niemandem, und ich merke
es erst am fertigen Text. Die ersten drei kommen aus Modul 2, die letzten zwei
liegen bei diesem Download dabei.
"""

CHECK = """## Der letzte Check

*(Dieser Abschnitt gehört nicht zu den sechs Teilen. Er ist eine Zugabe — aber
er ist der Grund, warum du nicht jedes Ergebnis von Hand nachbessern musst.)*

Bevor du mir etwas gibst, beantworte diese Fragen. Eine mit Nein heisst:
nochmal.

1. [Deine Frage]
2. [Deine Frage]
3. Steht hier ein Wort aus `verbotene-woerter.md`?
"""


def skill(name, beschreibung, zweck, braucht, regeln, ausgabe, beispiel):
    return """---
name: %s
description: "%s"
---

# %s

> **Dieser Skill ist leer.** Die Technik steht, der Inhalt fehlt — und der
> Inhalt bist du. Ersetz alles in eckigen Klammern. Solange da noch Klammern
> stehen, bekommst du Durchschnitt zurück.

## Zweck

%s

%s
## Was ich wissen muss

%s
## Regeln

%s
## Was herauskommen soll

%s
## Beispiel

Ein einziges gutes Beispiel bringt mehr als drei Absätze Regeln. Es muss von
dir sein. Etwas von jemand anderem bringt dir Texte, die nach jemand anderem
klingen — und genau das wolltest du ja loswerden.

%s
%s""" % (name, beschreibung, name.capitalize(), zweck, LIEST, braucht,
         regeln, ausgabe, beispiel, CHECK)


# ── Die vier Maschinen ───────────────────────────────────────────────
DATEIEN = {}

DATEIEN["caption"] = skill(
    "caption",
    "Schreibt den Text unter einen Beitrag. Dran, wenn das Bild oder das Video "
    "schon steht und nur noch der Text fehlt.",
    "Aus einem fertigen Bild oder Video wird der Text darunter. Am Ende steht "
    "eine Caption, die ich so posten kann — kein Entwurf, den ich noch "
    "umbauen muss.",
    """Frag mich danach, wenn ich es nicht von selbst gesagt habe:

1. Worum geht es in dem Beitrag?
2. Was soll die Leserin danach tun? (Oder: gar nichts, er soll nur wirken.)
3. Für welches meiner Angebote schreibe ich gerade — oder für keines?
""",
    """Das sind deine Regeln. Schreib auf, wie du schreibst, und vor allem,
was nicht passieren darf.

- [Wie lang darf eine Caption bei dir sein?]
- [Wie fängt die erste Zeile an — und wie nie?]
- [Duzt du, siezt du, schreibst du Mundart?]
- [Wie viele Hashtags, und welche nie?]
- Nie: [was dich an fremden Captions stört]
- Nie: ein Wort aus `verbotene-woerter.md`
""",
    """Ganz genau, sonst bekommst du jedes Mal etwas anderes:

- **Drei Fassungen**, nicht eine. Ich will auswählen.
- Je Fassung: der Text, und darunter die Hashtags.
- [Wie lang? Schreib eine Zahl hin, nicht „eher kurz".]
- Keine Erklärung dazu, warum du es so geschrieben hast. Nur den Text.
""",
    """**Mein Beitrag war:** [beschreib ihn in einem Satz]

**Gute Caption dazu:**

> [Hier eine Caption von dir, die du gut findest. Eine reicht.]

**Und was daran gut ist:** [ein Satz — das ist für die KI wichtiger als die
Caption selbst]
""")

DATEIEN["story"] = skill(
    "story",
    "Baut einen Story-Bogen für einen Tag. Dran, wenn ich erzählen will, was "
    "heute war, und am Schluss zu etwas hinführen möchte.",
    "Aus einem Erlebnis oder einem Gedanken wird eine Folge von Story-Folien, "
    "die zusammen einen Bogen ergeben. Am Ende weiss ich, was auf jede Folie "
    "kommt und womit ich aufhöre.",
    """Frag mich danach:

1. Was ist heute passiert, oder worüber denke ich gerade nach?
2. Wohin soll es führen? (Ein Angebot, eine Frage, oder nirgendwohin.)
3. Wie viele Folien soll ich haben?
""",
    """- [Wie fängt bei dir eine Story an — und wie nie?]
- [Was zeigst du von deinem Alltag, und wo ist die Grenze?]
- [Wen nennst du beim Namen, wen nie?]
- Nie: eine Szene erfinden, die so nicht stattgefunden hat. Frag lieber nach.
- Nie: ein Wort aus `verbotene-woerter.md`
""",
    """- **Je Folie:** der Text, der aufs Bild kommt, und darunter in Klammern,
  was ich filmen oder fotografieren soll.
- [Wie viele Folien? Schreib eine Zahl hin.]
- Die letzte Folie ist der Schluss — sag dazu, was sie tun soll.
- Wo ich selbst etwas einsetzen muss, schreib ✏️ hin statt es zu erfinden.
""",
    """**Mein Tag war:** [ein Satz]

**Guter Bogen daraus:**

> Folie 1: [Text]
>
> Folie 2: [Text]
>
> Folie 3: [Text]
""")

DATEIEN["karussell"] = skill(
    "karussell",
    "Baut die Folien eines Karussells. Dran, wenn ein Gedanke zu lang für eine "
    "Caption ist und über mehrere Bilder gehen soll.",
    "Aus einem Thema werden die Texte für alle Folien eines Karussells, von "
    "der ersten bis zur letzten. Am Ende steht, was auf jedes Bild kommt.",
    """Frag mich danach:

1. Worum geht es?
2. Was soll sie nach der letzten Folie wissen oder tun?
3. Wie viele Folien?
""",
    """- [Wie viele Folien bei dir — und warum nicht mehr?]
- [Wie viel Text passt auf eine Folie? Schreib eine Zahl hin.]
- [Was steht auf der ersten Folie, was auf der letzten?]
- Nie: eine Folie, die nur „weiterwischen" sagt und sonst nichts.
- Nie: ein Wort aus `verbotene-woerter.md`
""",
    """- **Je Folie nummeriert:** die grosse Zeile, und darunter die kleine.
- [Wie viele Folien? Zahl.]
- Dazu die Caption, die unter das Karussell kommt.
- Keine Gestaltungsvorschläge — Farben und Schriften stehen schon fest.
""",
    """**Mein Thema war:** [ein Satz]

**Gutes Karussell daraus:**

> Folie 1: [grosse Zeile] / [kleine Zeile]
>
> Folie 2: [grosse Zeile] / [kleine Zeile]
>
> Folie 3: [grosse Zeile] / [kleine Zeile]
""")

DATEIEN["reels"] = skill(
    "reels",
    "Schreibt das Skript für ein Reel. Dran, wenn ich etwas in die Kamera "
    "sagen will oder einen kurzen Clip mit Text darüber brauche.",
    "Aus einer Idee wird ein Reel-Skript: was ich sage, was man sieht, und wie "
    "lang es dauert. Am Ende kann ich das Handy nehmen und loslegen.",
    """Frag mich danach:

1. Worum geht es?
2. Rede ich in die Kamera, oder läuft ein Clip mit Text darüber?
3. Wie lang soll es werden?
""",
    """- [Wie lang sind deine Reels? Schreib Sekunden hin.]
- [Sprichst du frei oder liest du ab?]
- [Was steht als Text im Bild, was sagst du nur?]
- Nie: ein Skript, das ich in der Zeit gar nicht sprechen kann. Rechne mit
  [deine Zahl] Wörtern pro Sekunde.
- Nie: ein Wort aus `verbotene-woerter.md`
""",
    """- **Die erste Zeile** — was im Bild steht und was ich dazu sage.
- **Das Skript**, Satz für Satz, so wie ich es sprechen soll.
- **Was man sieht** — je Abschnitt in Klammern dahinter, damit ich beim Filmen
  nicht mehr überlegen muss.
- **Die Länge in Sekunden**, gerechnet und nicht geschätzt.
- Dazu die Caption, so wie der Befehl `caption` sie schreiben würde.
""",
    """**Meine Idee war:** [ein Satz]

**Gutes Skript daraus:**

> [Erste Zeile]
>
> [Was du sagst, Satz für Satz]
>
> [Was man dabei sieht]
""")

# ── Die leeren Wissensdateien ────────────────────────────────────────
WISSEN = {}

WISSEN["meine-kundin.md"] = """# Meine Kundin

Eine Person, nicht eine Zielgruppe. Wenn du hier „Frauen zwischen 30 und 50"
schreibst, bekommst du Texte für Frauen zwischen 30 und 50 — und die liest
niemand.

## Wie sie heisst und wie alt sie ist

[Denk dir eine aus, die es so ähnlich wirklich gibt. Ein Name hilft mehr, als
du glaubst.]

## Was sie gerade umtreibt

[„Sie will mehr Umsatz" reicht nicht. Schreib das hin, was sie abends denkt,
bevor sie das Handy weglegt.]

## Was sie schon probiert hat

[Und warum es nicht funktioniert hat. Das ist der Teil, den fast alle
weglassen — und der Texte glaubwürdig macht.]

## Was sie mir nicht glaubt

[Ihre Einwände, in ihren Worten. Schreib sie auf, wie sie sie dir wirklich
sagen würde.]

## Wie sie redet

[Drei, vier Sätze, die du von ihr gehört hast. Aus einer Nachricht, aus einem
Gespräch, aus einem Kommentar. Wörtlich.]
"""

WISSEN["meine-angebote.md"] = """# Meine Angebote

Damit die Maschinen wissen, wohin sie führen sollen — und was sie nie
versprechen dürfen.

## Was ich anbiete

[Je Angebot: wie es heisst, was es kostet, und in einem Satz, was sich für sie
danach ändert. Nicht, was drin ist — was sich ändert.]

| Angebot | Preis | Was sich ändert |
|---|---|---|
| [Name] | [Preis] | [ein Satz] |
| [Name] | [Preis] | [ein Satz] |

## Was gerade dran ist

[Welches Angebot bewirbst du diesen Monat? Die Maschinen führen dann dorthin
statt irgendwohin.]

## Was ich nie verspreche

[Hier gehört alles hinein, was du rechtlich oder fachlich nicht sagen darfst.
Wenn dein Konto an einem Unternehmen hängt, steht das hier — und die
Maschinen halten sich daran.]
"""

WISSEN["was-bei-mir-funktioniert.md"] = """# Was bei mir funktioniert

Die Datei, die du am Anfang nicht füllen kannst. Fang trotzdem an.

## Beiträge, die gut liefen

[Nach jedem Beitrag, der überdurchschnittlich lief: eine Zeile hierher. Was es
war, und warum du glaubst, dass es lief.]

| Wann | Was es war | Warum es wohl lief |
|---|---|---|
| [Datum] | [ein Satz] | [ein Satz] |

## Beiträge, die nicht liefen

[Genauso wichtig. Die Maschinen lernen daraus, was sie lassen sollen.]

## Was ich dreimal korrigiert habe

[Sobald du etwas zum dritten Mal von Hand änderst, gehört es als Regel in den
jeweiligen Skill. Schreib es erst hier auf, dann trag es dort ein.]

| Was ich ändere | In welchem Skill steht es jetzt |
|---|---|
| [was] | [caption / story / karussell / reels] |
"""

LIESMICH = """# Deine vier Content-Maschinen

Vier Befehle — **caption**, **story**, **karussell**, **reels** — und darunter
Dateien mit deinem Wissen. Änderst du eine Datei, ändert sich das Ergebnis bei
allen vier. Das ist der ganze Trick: du pflegst ein Wissen und nicht vier
Maschinen.

## Was hier drin ist

| Ordner | Was | Was du tust |
|---|---|---|
| `.claude/skills/` | die vier Befehle | die Klammern ersetzen |
| `context/` | drei leere Wissensdateien | ausfüllen |

## So kommt es in deinen Arbeitsplatz

Beide Ordner gibt es bei dir schon — du hast sie in Modul 4 angelegt. Kopier
den Inhalt einfach hinein, dann liegt alles am richtigen Platz.

Danach Claude Code einmal neu starten. Vorher kennt sie die neuen Befehle
nicht.

**Und dann einmal fragen:** *„Welche Befehle hast du jetzt?"* Wenn die vier
dastehen, hat es geklappt.

## Warum die Dateien leer sind

Das ist nicht gespart, das ist der Punkt.

Die Mechanik steht hier drin — wann ein Befehl dran ist, was er lesen soll, was
herauskommen muss. Das ist die Maschine. Was sie herstellt, hängt davon ab, was
du hineinfüllst, und das kann dir niemand abnehmen. Fremde Formeln in deinen
Dateien ergeben Texte, die nach fremden Leuten klingen.

**Fang mit `context/meine-kundin.md` an.** Diese eine Datei macht den grössten
Unterschied von allen.

## Die sechs Teile

Jede der vier Dateien ist nach den sechs Teilen aus Lektion 5.2 gebaut, in
derselben Reihenfolge: **Kopf · Zweck · Bevor du anfängst · Regeln · Was
herauskommen soll · Beispiel.** Du siehst sie hier viermal — wenn du deinen
nächsten Skill selbst baust, erkennst du sie wieder.

Dazu hat jede einen siebten Abschnitt, **Der letzte Check**. Der gehört nicht
zu den sechs. Er ist eine Zugabe, und er ist der Grund, warum du nicht jedes
Ergebnis von Hand nachbessern musst.

## Wo du anfängst

1. `context/meine-kundin.md` ausfüllen. Nimm dir eine halbe Stunde.
2. `.claude/skills/caption/SKILL.md` öffnen und die Klammern ersetzen.
3. Einen Beitrag nehmen, den du schon hast, und `caption` darauf loslassen.
4. Was dir am Ergebnis nicht passt, wird eine Regel. Nicht beim nächsten Mal —
   sofort.

Die anderen drei machst du genauso, wenn du sie brauchst. Alle vier auf einmal
auszufüllen klingt gründlich und endet damit, dass keiner benutzt wird.
"""


SKILLS_LIESMICH = """# Die vier Befehle

Hier drin liegen vier Ordner, in jedem eine `SKILL.md`. Das ist alles, was
einen Befehl ausmacht: ein Ordner mit einer Textdatei.

| Ordner | Du rufst ihn auf mit | Er macht |
|---|---|---|
| `caption/` | `/caption` | den Text unter einen fertigen Beitrag |
| `story/` | `/story` | einen Story-Bogen für einen Tag |
| `karussell/` | `/karussell` | die Texte für alle Folien |
| `reels/` | `/reels` | das Skript für ein Reel |

## Was du tun musst

**Die eckigen Klammern ersetzen.** Jede `[...]` ist eine Frage an dich. Solange
sie dasteht, hat der Befehl an dieser Stelle keine Meinung — und du bekommst,
was alle bekommen.

Fang mit `caption/` an. Das ist der Befehl, den du am häufigsten brauchst, und
du merkst am schnellsten, ob die Regeln stimmen.

## Wie du weisst, dass es geklappt hat

Claude Code einmal neu starten, dann fragen: *„Welche Befehle hast du jetzt?"*

Stehen die vier da, liegt alles richtig. Fehlt einer, stimmt der Ordnername
nicht mit dem `name` ganz oben in seiner `SKILL.md` überein — die zwei müssen
gleich heissen.

## Der Aufbau, den du wiedererkennst

Alle vier sind nach den **sechs Teilen** gebaut, die du in Modul 5 gesehen hast,
in derselben Reihenfolge: Kopf · Zweck · Bevor du anfängst · Regeln · Was
herauskommen soll · Beispiel.

Dazu kommt **Der letzte Check**. Der gehört nicht zu den sechs — er ist eine
Zugabe, und er ist der Grund, warum du nicht jedes Ergebnis von Hand
nachbessern musst.

## Das Wichtigste

**Was du dreimal von Hand korrigierst, gehört als Regel in den Skill.** Nicht
beim nächsten Mal — sofort, solange du noch weisst, was dich gestört hat.
"""

CONTEXT_LIESMICH = """# Dein Wissen

Alle vier Befehle lesen dieselben Dateien. Änderst du eine, ändert sich das
Ergebnis bei allen vier. Das ist der ganze Trick: **du pflegst ein Wissen und
nicht vier Maschinen.**

## Welche Dateien gebraucht werden

| Datei | Woher sie kommt |
|---|---|
| `business-brief.md` | Modul 2.3 — du hast sie schon |
| `meine-stimme.md` | Modul 2.5 — deine Textproben |
| `verbotene-woerter.md` | Modul 2.2 — deine Floskel-Liste |
| `meine-kundin.md` | **neu, liegt hier dabei** |
| `meine-angebote.md` | **neu, liegt hier dabei** |
| `was-bei-mir-funktioniert.md` | **neu, liegt hier dabei** |

## Wenn die ersten drei bei dir fehlen

Dann hast du Modul 2 übersprungen oder die Dateien nicht in deinen Arbeitsplatz
kopiert. Beides lässt sich nachholen, und du solltest es tun, bevor du die
Befehle benutzt — ohne sie schreiben sie zwar, aber nach niemandem.

Die Befehle sagen dir von selbst Bescheid, wenn eine fehlt. Sie raten nicht.

## Womit du anfängst

**`meine-kundin.md`.** Diese eine Datei macht den grössten Unterschied von
allen. Nimm dir eine halbe Stunde und schreib über **eine** Person, nicht über
eine Zielgruppe.

Danach `meine-angebote.md` — damit die Befehle wissen, wohin sie führen sollen.

`was-bei-mir-funktioniert.md` bleibt am Anfang leer. Die füllt sich von selbst,
sobald du postest.

## Wie du sie füllst, wenn dir nichts einfällt

Dafür gibt es eine eigene Anleitung: **„So füllst du die Dateien"** liegt eine
Ebene höher. Darin steht der Weg über deine eigenen besten Beiträge — und der
über Beiträge, die dir bei anderen gefallen.
"""

FUELLEN = """# So füllst du die Dateien

Die Befehle sind fertig. Was sie herstellen, hängt an dem, was in deinen
Dateien steht — und davor sitzen die meisten erst mal ratlos.

Hier sind zwei Wege. **Nimm den ersten zuerst.**

---

## Weg 1 · Deine eigenen besten Beiträge

Das ist der bessere Weg, weil dabei etwas herauskommt, das wirklich nach dir
klingt. Du hast schon Material — du hast es nur nie ausgewertet.

**Such dir fünf eigene Beiträge, die gut liefen.** Nicht die, die dir am besten
gefallen. Die, bei denen etwas passiert ist: Kommentare, Nachrichten,
Speicherungen.

Mach Screenshots davon und zieh sie in den Chat. Dann sag:

> Hier sind fünf Beiträge von mir, die gut gelaufen sind. Schau sie dir an und
> sag mir, was sie gemeinsam haben — wie die erste Zeile gebaut ist, wie lang
> sie sind, wie sie aufhören, wie ich klinge.
>
> Schreib mir daraus Regeln für `.claude/skills/caption/SKILL.md` und trag sie
> dort unter **Regeln** ein. Frag nach, wenn du dir bei etwas nicht sicher bist.

**Was dabei herauskommt, ist deine eigene Handschrift** — nur zum ersten Mal
aufgeschrieben.

---

## Weg 2 · Beiträge, die dir bei anderen gefallen

Wenn dir ein Karussell begegnet und du denkst „so hätte ich das auch gern":
genau dann ist dieser Weg dran.

**Screenshots von allen Folien** (oder vom ganzen Beitrag), in den Chat ziehen,
und dann:

> Hier ist ein Karussell, das ich gut finde. Analysier die **Bauweise**: wie
> viele Folien, was steht auf der ersten, wie ist der Text aufgebaut, wo kommt
> der Aufruf, wie hört es auf.
>
> Schreib mir daraus Regeln für `.claude/skills/karussell/SKILL.md`.
>
> **Übernimm keine Sätze und keine Formulierungen — nur die Bauweise.**

### 🚨 Der letzte Satz ist kein Schmuck

Die **Bauweise** darfst du abschauen. Wie viele Folien, wo der Aufruf steht,
dass die erste Folie eine Frage ist — das sind Handgriffe, und Handgriffe
gehören niemandem.

Die **Sätze** nicht. Zwei Gründe, und der zweite ist der wichtigere:

1. Es ist abgeschrieben, und das fällt auf.
2. **Geborgte Sätze klingen nach der Person, von der du sie hast.** Du wolltest
   ja gerade weg davon, dass deine Texte nach irgendwem klingen.

Wenn du in derselben Nische unterwegs bist wie die Person, von der du
abschaust, wird es doppelt eng: dann klingen am Ende alle gleich, und niemand
hat noch einen Grund, ausgerechnet dich zu lesen.

### Schneller geht es mit der Browser-Erweiterung

Statt Screenshots zu machen, kannst du Claude direkt auf die Seite schauen
lassen. Das ist bequemer, und du brauchst es nicht — der Weg über Screenshots
funktioniert genauso gut.

**Das ist die einzige Stelle im ganzen Kurs, an der du etwas zusätzlich
installierst.** Du musst es nicht. Wenn du es tust, zeige ich dir im Video,
wie.

---

## Und dann das Wichtigste

Beide Wege geben dir einen **Anfang**, keine fertige Datei.

Lass den Befehl einmal laufen. Was dir am Ergebnis nicht passt, wird eine
Regel — sofort, nicht beim nächsten Mal. Nach drei, vier Runden steht eine
Datei, die wirklich deine ist.

**Das ist der ganze Kurs in einem Satz:** Den Unterschied macht, wie oft du ihr
gesagt hast, was du nicht wolltest. Die Maschine selbst hat jede.

---

## Dasselbe für die anderen drei

| Befehl | Wonach du analysieren lässt |
|---|---|
| `caption` | wie die erste Zeile gebaut ist · wie lang · wie sie aufhört · wie viele Hashtags |
| `story` | wie viele Folien · womit sie anfängt · wo der Bruch kommt · womit sie endet |
| `karussell` | wie viele Folien · was auf Folie 1 steht · wie viel Text je Folie · wo der Aufruf kommt |
| `reels` | wie die ersten drei Sekunden gebaut sind · wie lang · was im Bild steht und was nur gesagt wird |

Mach es nicht für alle vier auf einmal. Einer, bis er sitzt — dann der
nächste.
"""


def schreib(pfad: Path, text: str) -> None:
    pfad.parent.mkdir(parents=True, exist_ok=True)
    pfad.write_text(text, encoding="utf-8", newline="\n")


def main() -> None:
    schreib(ZIEL / "LIESMICH.md", LIESMICH)
    schreib(ZIEL / "So-fuellst-du-die-Dateien.md", FUELLEN)
    schreib(ZIEL / ".claude" / "skills" / "LIESMICH.md", SKILLS_LIESMICH)
    schreib(ZIEL / "context" / "LIESMICH.md", CONTEXT_LIESMICH)
    for name, text in DATEIEN.items():
        schreib(ZIEL / ".claude" / "skills" / name / "SKILL.md", text)
    for name, text in WISSEN.items():
        schreib(ZIEL / "context" / name, text)

    # 🚨 Gegenprobe. Drei Dinge, die hier nie stehen duerfen.
    verdacht = []
    fremde = ["julia", "trost", "kevin", "fiedler", "hormozi", "elke", "mayr",
              "nadja", "jenya", "mia pejic", "laura hersche", "anna"]
    for p in sorted(ZIEL.rglob("*.md")):
        t = p.read_text(encoding="utf-8")
        name = p.relative_to(ZIEL).as_posix()
        if "ß" in t:
            verdacht.append(name + " — deutsches ß, hier gilt ss")
        for f in fremde:
            if f in t.lower():
                verdacht.append(name + " — fremder Name: " + f)
        # Patricias eigene Marke gehoert auch nicht hinein — die Teilnehmerin
        # soll ihre eigene eintragen.
        for eigen in ["mum life balance", "doterra", "patricia", "mumlifebalance"]:
            if eigen in t.lower():
                verdacht.append(name + " — Patricias eigenes: " + eigen)

    dateien = sorted(p for p in ZIEL.rglob("*") if p.is_file())
    print("Content-Maschinen gebaut: " + ZIEL.relative_to(WURZEL).as_posix())
    for p in dateien:
        print("  %-42s %5d Zeichen"
              % (p.relative_to(ZIEL).as_posix(), len(p.read_text(encoding="utf-8"))))

    # Zaehlt die offenen Klammern — die sind hier erwuenscht, aber die Zahl
    # soll man sehen: null waere ein Zeichen, dass etwas zu fertig ist.
    offen = sum(p.read_text(encoding="utf-8").count("[")
                for p in dateien)
    print("")
    print("  %d Stellen zum Ausfuellen" % offen)

    if verdacht:
        print("")
        print("🚨 NICHT weitergeben:")
        for v in verdacht:
            print("   " + v)
        sys.exit(1)
    print("  Gegenprobe sauber: kein fremder Name, nichts Eigenes, kein ß.")

    if "--zip" in sys.argv:
        import zipfile
        ziel = ZIEL.parent / "Content-Maschinen.zip"
        with zipfile.ZipFile(ziel, "w", zipfile.ZIP_DEFLATED) as z:
            for p in dateien:
                z.write(p, "Content-Maschinen/" + p.relative_to(ZIEL).as_posix())
        print("  ZIP: " + ziel.relative_to(WURZEL).as_posix()
              + " (%d KB)" % (ziel.stat().st_size // 1024))


if __name__ == "__main__":
    main()
