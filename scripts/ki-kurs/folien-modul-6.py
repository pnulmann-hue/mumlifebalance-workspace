#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Folien fuer Modul 6 — Bots, die von selbst laufen.

    python scripts/ki-kurs/folien-modul-6.py <zielordner>
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from folien_basis import *

ZIEL = sys.argv[1] if len(sys.argv) > 1 else "folien-modul-6"
F = {}

F["cover"] = modulcover(6, "Bots",
    "Derselbe Auftrag wie ein Skill. Nur ruft ihn niemand mehr auf.",
    "Der Unterschied zum letzten Modul ist klein und fühlt sich riesig an. "
    "Sag das gleich am Anfang, sonst erwarten sie etwas Kompliziertes.")

# ── 6.1 Vom Skill zum Bot ────────────────────────────────────────────
F["l61-titel"] = lektionstitel("l61-titel", "6.1", "Vom Skill zum Bot",
    "Ein Skill wartet auf dich. Ein Bot wartet auf die Uhrzeit.",
    "Halt es kurz. Die eigentliche Wirkung kommt in der nächsten Lektion, "
    "wenn sie die Nachrichten auf deinem Handy sieht.")

F["l61-drei"] = folie("l61-drei",
    eyebrow("Lektion 6.1")
    + h2("Drei Teile, mehr braucht es nicht")
    + reihe([
        karte("Der Auftrag", ["Was getan werden soll.",
                              "Das ist dein Skill — den hast du schon."]),
        karte("Der Wecker", ["Wann es getan werden soll.",
                             "Jeden Morgen um sieben. Jeden Freitag um acht."], ORANGE),
        karte("Der Briefkasten", ["Wo das Ergebnis ankommt.",
                                  "Bei mir: eine Nachricht aufs Handy."]),
      ]),
    "Zeig beim mittleren Punkt, wo der Zeitplan bei dir eingestellt ist. "
    "Dass es wirklich nur ein Feld mit einer Uhrzeit ist, glaubt sonst niemand.")

F["l61-weiter"] = weiter("l61-weiter", "Als Nächstes",
    "Meine Bots",
    "Bevor du einen baust, zeig ich dir, was bei mir läuft.",
    "Mach neugierig. Die nächste Lektion ist die, wegen der Leute dieses Modul "
    "überhaupt anschauen.")

# ── 6.2 Übersicht ────────────────────────────────────────────────────
F["l62-titel"] = lektionstitel("l62-titel", "6.2", "Was bei mir läuft",
    "Vier Bots, ein Handy. Alles ohne mein Zutun.",
    "Ganz am Handy filmen. Nicht auf Folien erklären, sondern durch die "
    "Nachrichten scrollen — das ist der Moment, in dem es klick macht.")

F["l62-vier"] = folie("l62-vier",
    eyebrow("Lektion 6.2")
    + h2("Vier Beispiele")
    + reihe([
        karte("Garten", ["Was gerade dran ist, mit Blick aufs Wetter."]),
        karte("Küche", ["Der Wochenplan und die Einkaufsliste."], ORANGE),
        karte("Business", ["Was diese Woche ansteht und was noch offen ist."]),
        karte("Haushalt", ["Am Abend, was morgen ansteht."], ORANGE),
      ], 24),
    "Sag bei jedem einen Satz, wofür er dir Arbeit abnimmt. Nicht wie er gebaut ist — "
    "das kommt in der nächsten Lektion.")

F["l62-gemein"] = folie("l62-gemein",
    eyebrow("Lektion 6.2")
    + h2("Was alle vier gemeinsam haben")
    + liste([
        "Sie machen etwas, das ich vorher jede Woche selbst gemacht habe.",
        "Sie melden sich von selbst, ich muss nicht daran denken.",
        "Sie schreiben mir, nicht anderen. Nach aussen geht nichts ohne mich.",
        "Keiner davon war am ersten Tag fertig.",
      ], 34),
    "Der dritte Punkt ist eine Haltung und keine Technik. Der vierte nimmt den Druck.")

F["l62-weiter"] = weiter("l62-weiter", "Als Nächstes",
    "Dein erster Bot",
    "Wir bauen einen von null bis zur ersten Nachricht auf deinem Handy.",
    "Sag, dass sie dafür ihr Handy bereitlegen soll. Wer mitmacht, hat am Ende "
    "der Lektion wirklich eine Nachricht.")

# ── 6.3 Erster Bot ───────────────────────────────────────────────────
F["l63-titel"] = lektionstitel("l63-titel", "6.3", "Dein erster Bot",
    "Von null bis zur ersten Nachricht.",
    "Geteilter Bildschirm plus Handy daneben. Nimm den einfachsten Bot, den du "
    "hast — lieber banal und er kommt an, als clever und sie steigt aus.")

F["l63-schritte"] = folie("l63-schritte",
    eyebrow("Lektion 6.3")
    + h2("Vier Schritte")
    + liste([
        "<b>Den Botvater fragen.</b> Im Messenger selbst legst du deinen Bot an und bekommst dafür einen Schlüssel.",
        "<b>Den Schlüssel richtig ablegen.</b> Er gehört in die Datei daneben, nie in den Text selbst. Warum, kommt in Modul 10.",
        "<b>Den Auftrag schreiben.</b> Das kannst du schon — es ist ein Skill.",
        "<b>Einmal von Hand starten.</b> Wenn die Nachricht ankommt, stimmt alles.",
      ], 30),
    "Beim zweiten Schritt kurz innehalten und sagen, dass das die wichtigste "
    "Angewohnheit im ganzen Kurs ist. Ohne den Grund zu erklären, der kommt später.")

F["l63-geruest"] = folie("l63-geruest",
    eyebrow("Lektion 6.3")
    + h2("Du musst nicht bei null anfangen")
    + p("Unter diesem Video liegt ein Bot-Gerüst. Es ist ein fertiger Bot, dem nur "
        "dein Schlüssel und dein Auftrag fehlen.", 40)
    + p("📎 Bot-Gerüst · Schritt-für-Schritt-Anleitung", 30, PETROL),
    "Zeig, wo in der Datei ihr Schlüssel hinkommt und wo ihr Auftrag. "
    "Zwei Stellen, sonst nichts.")

F["l63-weiter"] = weiter("l63-weiter", "Als Nächstes",
    "Dass er morgens von selbst schreibt",
    "Bis hierher startest du ihn noch selbst. Jetzt übernimmt der Wecker.",
    "Kurze Brücke, aber sag dazu, dass ab hier das Gefühl kippt: bis jetzt hat sie "
    "einen Helfer, ab der nächsten Lektion hat sie eine Mitarbeiterin.")

# ── 6.4 Zeitplan ─────────────────────────────────────────────────────
F["l64-titel"] = lektionstitel("l64-titel", "6.4", "Dass er von selbst läuft",
    "Zwei Wege — einer gratis, einer kostet ein paar Franken.",
    "Sei bei den Kosten genau und sag die Zahl. Wer hier herumdruckst, wirkt, "
    "als würde er etwas verstecken.")

F["l64-wege"] = folie("l64-wege",
    eyebrow("Lektion 6.4")
    + h2("Zwei Wege")
    + gegenueber(
        "Auf deinem Rechner",
        ["Kostet nichts.",
         "Läuft nur, wenn der Rechner an ist.",
         "Gut zum Ausprobieren und für alles, was nicht täglich sein muss."],
        "Im Netz",
        ["Kostet bei mir rund fünf Franken im Monat.",
         "Läuft auch, wenn dein Rechner aus ist.",
         "Nötig für alles, was jeden Morgen um sieben da sein soll."]),
    "Sag, welchen Weg du für welchen Bot nimmst. Bei dir laufen nicht alle gleich, "
    "und genau das ist die ehrliche Antwort.")

F["l64-zeit"] = folie("l64-zeit",
    eyebrow("Lektion 6.4")
    + h2("Beim Zeitpunkt aufpassen")
    + liste([
        "Sommer- und Winterzeit verschieben dir den Bot um eine Stunde.",
        "Läuft er auf einem Rechner im Ausland, rechnet er in dessen Zeit.",
        "Ein Bot, der nachts um drei läuft, stört niemanden — auch dich nicht.",
      ], 34)
    + p("Stell die erste Ausgabe absichtlich auf eine Uhrzeit, zu der du wach bist. "
        "Dann siehst du am selben Tag, ob es klappt.", 32, PETROL),
    "Der letzte Satz ist der praktische Tipp. Wer den Bot auf sechs Uhr stellt, "
    "wartet bis zum nächsten Morgen auf die Antwort, ob er überhaupt läuft.")

F["l64-weiter"] = weiter("l64-weiter", "Als Nächstes",
    "Wenn der Bot schweigt",
    "Irgendwann kommt keine Nachricht. Dann schaust du an drei Stellen nach.",
    "Sag, dass das kommt und dass es normal ist. Wer darauf vorbereitet ist, "
    "hört nicht auf.")

# ── 6.5 Fehlersuche ──────────────────────────────────────────────────
F["l65-titel"] = lektionstitel("l65-titel", "6.5", "Wenn der Bot schweigt",
    "Drei Gründe decken fast alles ab.",
    "Erzähl von einem deiner Bots, der mal still war, und wie lange du gesucht "
    "hast. Ein echtes Beispiel nimmt die Angst.")

F["l65-gruende"] = folie("l65-gruende",
    eyebrow("Lektion 6.5")
    + h2("Wo du nachschaust")
    + reihe([
        karte("1 · Der Wecker", ["Ist der Zeitplan überhaupt aktiv?",
                                 "Am häufigsten, und am schnellsten geprüft."]),
        karte("2 · Der Schlüssel", ["Abgelaufen oder beim Umziehen nicht mitgekommen.",
                                    "Steht dann so im Protokoll."], ORANGE),
        karte("3 · Der Auftrag", ["Er lief, aber er ist unterwegs gestolpert.",
                                  "Auch das steht im Protokoll."]),
      ]),
    "Zeig, wo bei dir das Protokoll steht. Dass man dort nachlesen kann, was passiert "
    "ist, wissen die wenigsten.")

F["l65-fragen"] = folie("l65-fragen",
    eyebrow("Lektion 6.5")
    + h2("Und wenn du im Protokoll nichts verstehst")
    + p("Dann kopierst du es und gibst es Claude. Sie liest solche Meldungen besser "
        "als jeder Mensch und sagt dir in einem Satz, was fehlt.", 40)
    + p("Das ist kein Notbehelf. Das ist der normale Weg, und ich mache es "
        "genauso.", 34, GEDAEMPFT),
    "Das wirklich so sagen. Viele glauben, sie müssten es selbst verstehen, "
    "und geben deshalb auf.")

# ── 6.6 Zusammenfassung ──────────────────────────────────────────────
F["l66-titel"] = lektionstitel("l66-titel", "6.6", "Zusammenfassung",
    "Ein Bot ist ein Skill mit Wecker und Briefkasten.",
    "Kurz halten. Und ansagen, dass ab Modul 7 nichts Neues mehr an Technik kommt, "
    "sondern nur noch Anwendung.")

F["l66-bilanz"] = folie("l66-bilanz",
    eyebrow("Lektion 6.6")
    + h2("Das steht jetzt")
    + liste([
        "Ein eigener Bot, der dir schreibt.",
        "Ein Zeitplan, der ihn ohne dich startet.",
        "Das Wissen, wo du nachschaust, wenn nichts kommt.",
        "Und die Gewissheit, dass nach aussen nichts geht, was du nicht gesehen hast.",
      ], 34),
    "Der letzte Punkt ist die Überleitung zu Modul 7 und zur Freigabe. "
    "Sprich ihn betont.")

F["l66-checkliste"] = checkliste("l66-checkliste", "6.6", [
    "Mein Bot schreibt mir eine Nachricht",
    "Er läuft zu einer festen Zeit, ohne dass ich etwas tue",
    "Mein Schlüssel liegt in der Datei daneben, nie im Text selbst",
    "Ich weiss, wo das Protokoll steht",
  ], 6,
  "Der dritte Punkt ist der, bei dem du nicht nachgeben darfst. Alles andere "
  "kann man nachholen, das nicht.")

F["l66-weiter"] = folie("l66-weiter",
    eyebrow("Modul 7", ORANGE)
    + ('<h2 style="font-family:%s; font-size:84px; font-weight:700; line-height:1.15; color:%s">'
       'Social Media<br>mit Claude Code</h2>' % (DISPLAY, CREME))
    + p("Ab hier kommt keine neue Technik mehr. Ab hier wird angewendet, was du "
        "in Modul 5 und 6 gelernt hast.", 36, PETROL),
    "Sag den zweiten Satz wirklich. Ab Modul 7 hört das Lernen auf und das "
    "Arbeiten fängt an, und das ist eine gute Nachricht.",
    stil=SEK_DUNKEL, uebergang="push")


ORDER = ["cover",
 "l61-titel","l61-drei","l61-weiter",
 "l62-titel","l62-vier","l62-gemein","l62-weiter",
 "l63-titel","l63-schritte","l63-geruest","l63-weiter",
 "l64-titel","l64-wege","l64-zeit","l64-weiter",
 "l65-titel","l65-gruende","l65-fragen",
 "l66-titel","l66-bilanz","l66-checkliste","l66-weiter"]

SECTIONS = {
 "auftakt": {"description": "Worum es in Modul 6 geht.", "start": "cover"},
 "l61": {"description": "Lektion 6.1 — der Unterschied zwischen Skill und Bot.", "start": "l61-titel"},
 "l62": {"description": "Lektion 6.2 — vier Bots, die bei Patricia laufen.", "start": "l62-titel"},
 "l63": {"description": "Lektion 6.3 — den ersten Bot bauen.", "start": "l63-titel"},
 "l64": {"description": "Lektion 6.4 — Zeitplan und Kosten.", "start": "l64-titel"},
 "l65": {"description": "Lektion 6.5 — Fehlersuche, wenn nichts kommt.", "start": "l65-titel"},
 "l66": {"description": "Lektion 6.6 — Bilanz und Checkliste vor Modul 7.", "start": "l66-titel"},
}

schreibe(ZIEL, "Modul 6 — Bots", F, ORDER, SECTIONS)
