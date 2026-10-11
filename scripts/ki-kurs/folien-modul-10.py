#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Folien fuer Modul 10 — Sicherheit, Grenzen und das Ganze.

    python scripts/ki-kurs/folien-modul-10.py <zielordner>
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from folien_basis import *

ZIEL = sys.argv[1] if len(sys.argv) > 1 else "folien-modul-10"
F = {}

F["cover"] = modulcover(10, "Sicherheit,<br>Grenzen,<br>das Ganze",
    "Was nie in einen Arbeitsplatz gehört, was du verantwortest — und wie bei mir eine echte Woche abläuft.",
    "Kein Abspann. Sag am Anfang, dass die erste Lektion die ist, die in "
    "keinem anderen KI-Kurs vorkommt, und warum.")

# ── 10.1 Was nie hineingehört ────────────────────────────────────────
F["la1-titel"] = lektionstitel("la1-titel", "10.1", "Was nie hineingehört",
    "Zugangsschlüssel und die Daten anderer Menschen.",
    "Erzähl die Geschichte mit Datum und Zahlen. Sie ist dir passiert, "
    "und genau deshalb glaubt sie dir hier jede.")

F["la1-geschichte"] = folie("la1-geschichte",
    eyebrow("Lektion 10.1")
    + h2("Was bei mir passiert ist")
    + liste([
        "Ein Zugangsschlüssel stand im Klartext mitten im Text eines Skripts.",
        "Daneben 32 Kundinnen mit Namen, Mailadressen und Telefonnummern.",
        "Alles davon war öffentlich abrufbar, ohne Anmeldung.",
        "<b>Gefunden hat es niemand — bis einmal jemand gezielt nachgesehen hat.</b>",
      ], 32),
    "Der letzte Punkt ist der wichtigste. Es war kein Angriff und kein Alarm. "
    "Es lag einfach da, und niemand hat gemerkt, dass es da lag.")

F["la1-regeln"] = folie("la1-regeln",
    eyebrow("Lektion 10.1")
    + h2("Die drei Regeln daraus")
    + reihe([
        karte("Kein Schlüssel im Text", ["Zugangsdaten kommen aus der Datei daneben.",
                                         "Fehlt sie, soll das Programm abbrechen."]),
        karte("Keine fremden Daten", ["Namen, Mailadressen, Nummern gehören in eine "
                                      "Datei, die nicht mitgeht."], ORANGE),
        karte("Zusagen gelten", ["Steht bei einer Kundenstimme nur intern, "
                                 "dann heisst das auch hier nur intern."]),
      ]),
    "Zeig danach am Bildschirm, wie ein Schlüssel richtig liegt. Zwei Zeilen, "
    "und der ganze Unterschied.")

F["la1-cloud"] = folie("la1-cloud",
    eyebrow("Lektion 10.1")
    + h2("Und noch eine Falle")
    + p("Eine Kopie deines Arbeitsplatzes in einer Cloud-Ablage umgeht jede "
        "Schutzregel, die du eingerichtet hast.", 40)
    + p("Bei mir lag ein kompletter Abzug vom April in der Cloud — mit allen "
        "Schlüsseln, die ich längst gewechselt hatte. Bevor irgendwo eine Kopie "
        "abgelegt wird, gehören die Zugangsdateien heraus.", 32, GEDAEMPFT),
    "Das überrascht die meisten. Man denkt an das eine Verzeichnis und "
    "vergisst, dass die Sicherung alles mitnimmt.")

F["la1-weiter"] = weiter("la1-weiter", "Als Nächstes",
    "Wenn doch etwas passiert ist",
    "Löschen reicht nicht. Was du stattdessen tust.",
    "Kurze Brücke, ohne Drama. Wer schon einen Fehler gemacht hat, soll "
    "hier zuhören statt sich zu schämen.")

# ── 10.2 Wenn etwas passiert ist ─────────────────────────────────────
F["la2-titel"] = lektionstitel("la2-titel", "10.2", "Wenn doch etwas passiert ist",
    "Löschen reicht nicht — der Schlüssel muss gewechselt werden.",
    "Ruhig bleiben im Ton. Das ist eine Anleitung, keine Standpauke — und "
    "sag dazu, dass dir genau das passiert ist.")

F["la2-warum"] = folie("la2-warum",
    eyebrow("Lektion 10.2")
    + h2("Warum Löschen nicht reicht")
    + p("Die Verlaufsgeschichte deines Arbeitsplatzes behält jede frühere Fassung. "
        "Wer den Schlüssel in der Zwischenzeit kopiert hat, kann ihn weiter "
        "benutzen — auch wenn er bei dir längst weg ist.", 40)
    + p("Deshalb: wechseln, nicht löschen.", 40, PETROL),
    "Dieser Satz ist die ganze Lektion. Alles andere ist die Anleitung dazu.")

F["la2-schritte"] = folie("la2-schritte",
    eyebrow("Lektion 10.2")
    + h2("Was du tust")
    + liste([
        "<b>Beim Anbieter neu ausstellen.</b> Meist in den Einstellungen unter Entwickler.",
        "<b>Den alten sperren</b>, wenn das geht.",
        "<b>Den neuen überall eintragen</b> — und überall heisst wirklich überall.",
        "<b>Neu starten.</b> Viele Programme lesen den Schlüssel nur beim Start.",
      ], 32),
    "Der letzte Punkt hat mich selbst eine halbe Stunde gekostet. Ich habe "
    "gewechselt und trotzdem eine Fehlermeldung bekommen — bis ich neu gestartet habe.")

F["la2-weiter"] = weiter("la2-weiter", "Als Nächstes",
    "Was du verantwortest",
    "Die KI schreibt. Unterschreiben tust du.",
    "Kurze Brücke, und werde ernst. Für Network-Mamas ist die nächste Lektion "
    "wichtiger als alles Technische davor.")

# ── 10.3 Compliance ──────────────────────────────────────────────────
F["la3-titel"] = lektionstitel("la3-titel", "10.3", "Was du verantwortest",
    "Die KI schreibt. Dein Name steht darunter.",
    "Erzähl, warum das bei uns schärfer ist als bei anderen. Der Vertrag mit "
    "dem Partnerunternehmen gilt für jeden Satz, auch den automatisch erzeugten.")

F["la3-verbote"] = folie("la3-verbote",
    eyebrow("Lektion 10.3")
    + h2("Was nie herausgehen darf")
    + liste([
        "<b>Heilversprechen.</b> Kein Produkt heilt, lindert oder behandelt etwas.",
        "<b>Einkommensversprechen.</b> Keine Zahl, die jemand anderes erreichen soll.",
        "<b>Fremde Zahlen und Namen</b> ohne Erlaubnis — auch keine erfundenen.",
        "<b>Alles, was dein Partnerunternehmen untersagt.</b> Diese Liste kennst du, die KI nicht.",
      ], 31),
    "Der letzte Punkt ist der, der in die eigene Wissensdatei gehört. "
    "Zeig, wo sie diese Liste hinschreibt, damit jeder Skill sie mitliest.")

F["la3-formulierung"] = folie("la3-formulierung",
    eyebrow("Lektion 10.3")
    + h2("Wie du es stattdessen sagst")
    + gegenueber(
        "Geht nicht",
        ["Das Öl hilft gegen Kopfschmerzen.",
         "Damit verdienst du 500 im Monat.",
         "Meine Kundin hat es geheilt."],
        "Geht",
        ["Bei mir gehört es zum Abend dazu.",
         "Was bei mir dabei herausgekommen ist, erzähle ich offen.",
         "Sie hat mir erzählt, wie es bei ihr war."]),
    "Der Unterschied ist immer derselbe: du sprichst über dich, nicht über "
    "die Wirkung. Das trägt und ist trotzdem ehrlich.")

F["la3-weiter"] = weiter("la3-weiter", "Als Nächstes",
    "Was KI nicht kann",
    "Damit du sie nicht dort einsetzt, wo sie nichts zu suchen hat.",
    "Kurze Brücke. Die nächste Lektion nimmt Druck raus statt welchen "
    "aufzubauen — und sie erklärt, warum du nicht überflüssig wirst.")

# ── 10.4 Was KI nicht kann ───────────────────────────────────────────
F["la4-titel"] = lektionstitel("la4-titel", "10.4", "Was KI nicht kann",
    "Und warum das eine gute Nachricht ist.",
    "Ruhig und ohne Warnton. Das ist die Lektion, nach der viele erleichtert "
    "sind — sie sind nicht überflüssig geworden.")

F["la4-drei"] = folie("la4-drei",
    eyebrow("Lektion 10.4")
    + h2("Drei Dinge bleiben bei dir")
    + reihe([
        karte("Beziehung", ["Die Frau, die dir schreibt, will dich.",
                            "Eine Antwort aus der Maschine merkt sie."]),
        karte("Entscheidung", ["Was du anbietest und für wen.",
                               "Das kann dir niemand abnehmen."], ORANGE),
        karte("Deine Stimme", ["Sie kann sie nachahmen, wenn du sie ihr gibst.",
                               "Erfinden kann sie sie nicht."]),
      ]),
    "Sag beim dritten, dass genau das der Treibstoff aus Modul 7 ist. "
    "Der Kreis schliesst sich hier.")

F["la4-praktisch"] = folie("la4-praktisch",
    eyebrow("Lektion 10.4")
    + h2("Und ganz praktisch")
    + liste([
        "Sie hört den Ton in deinem Video nicht.",
        "Sie sieht nicht, ob dein Gesicht auf dem Bild frei ist.",
        "Sie weiss nicht, wie sich ein Dienstagabend mit vier Kindern anfühlt.",
        "Und sie erfindet lieber etwas, als zuzugeben, dass sie etwas nicht weiss.",
      ], 34),
    "Der letzte Punkt ist der, der dich am meisten Zeit kosten kann. "
    "Jede Zahl und jeder Name gehört geprüft, auch wenn es plausibel aussieht.")

F["la4-weiter"] = weiter("la4-weiter", "Als Nächstes",
    "Wie bei mir alles zusammenhängt",
    "Eine echte Woche, von Freitagmorgen bis zum fertigen Beitrag.",
    "Mach neugierig. Das ist die Lektion, wegen der Leute den Kurs weiterempfehlen.")

# ── 10.5 Die echte Woche ─────────────────────────────────────────────
F["la5-titel"] = lektionstitel("la5-titel", "10.5", "Eine echte Woche",
    "Von Freitagmorgen bis zum Beitrag am Montag.",
    "Hier wird mitgeschaut, nicht nachgebaut. Sag das gleich, sonst hält "
    "die halbe Klasse an und versucht, Schritt für Schritt mitzukommen.")

F["la5-woche"] = folie("la5-woche",
    eyebrow("Lektion 10.5")
    + h2("Der Ablauf")
    + liste([
        "<b>Freitag früh</b> schreibt die Maschine die Vorschläge für die nächste Woche.",
        "<b>Über den Tag</b> lese ich sie am Handy und gebe frei, was passt.",
        "<b>Abends um acht</b> holt der Abendlauf das Freigegebene ab und plant es ein.",
        "<b>Am Wochenende</b> baue ich die Bilder und schneide die Videos.",
        "<b>Montagmorgen</b> ist der erste Beitrag draussen, ohne dass ich etwas tue.",
      ], 30),
    "Zeig jeden Schritt am echten Bildschirm. Nicht erklären, was passiert — "
    "zeigen, wie es aussieht, wenn es passiert.")

F["la5-teile"] = folie("la5-teile",
    eyebrow("Lektion 10.5")
    + h2("Was davon aus welchem Modul kommt")
    + liste([
        "Die Vorschläge kommen aus <b>Skills</b> — Modul 5.",
        "Dass sie freitags von selbst laufen, ist ein <b>Bot</b> — Modul 6.",
        "Freigeben und einplanen läuft über das <b>Cockpit</b> — Modul 9.",
        "Bilder und Videos machen die <b>Content-Maschinen</b> — Modul 7.",
        "Und über allem steht die <b>Freigabe</b>, die immer bei mir bleibt.",
      ], 30),
    "Diese Folie ist die Belohnung für alle, die durchgehalten haben. "
    "Lass dir hier Zeit.")

F["la5-satz"] = statement("la5-satz",
    ["Die Maschine nimmt mir", "die Arbeit ab,", "nicht die Entscheidung."],
    "Genau deshalb kann ich sie laufen lassen, ohne nachts wach zu liegen.",
    "Das ist der Satz, mit dem der Kurs steht und fällt. Sag ihn langsam "
    "und lass danach eine Pause.")

# ── 10.6 Wie es weitergeht ───────────────────────────────────────────
F["la6-titel"] = lektionstitel("la6-titel", "10.6", "Wo du weitermachst",
    "Welche Maschine welchen Treibstoff braucht — und wo der steht.",
    "Kein Verkaufsgespräch. Sag es wie eine Wegbeschreibung: hier ist das "
    "Werkzeug, dort sind die Inhalte, du entscheidest.")

F["la6-drei"] = folie("la6-drei",
    eyebrow("Lektion 10.6")
    + h2("Drei Richtungen")
    + reihe([
        karte("Content", ["Hooks, Captions, Story-Aufbau, Reichweite.",
                          "Steht in der Instagram-Kundenmaschine."]),
        karte("Produkte", ["Produkttreppe, Preise, Verkaufsseiten, Launch.",
                           "Steht in der digitalen Produktwelt."], ORANGE),
        karte("Struktur", ["Wochenrhythmus, Planung, das ganze Cockpit.",
                           "Steht in Mama-CEO."]),
      ]),
    "Und sag dazu, dass alles zusammen in der Academy liegt, falls jemand "
    "nicht einzeln wählen will. Einmal, ohne Nachdruck.")

F["la6-jetzt"] = folie("la6-jetzt",
    eyebrow("Lektion 10.6")
    + h2("Und jetzt?")
    + liste([
        "Nimm eine Arbeit, die dich diese Woche genervt hat.",
        "Mach einen Skill daraus, auch wenn er unfertig ist.",
        "Lass ihn dreimal laufen und schreib auf, was dich stört.",
        "Dann steht deine erste Regel, und ab da wird es von allein besser.",
      ], 34),
    "Das ist der letzte Auftrag. Konkret, klein und diese Woche machbar — "
    "wer mit einem grossen Vorhaben aus einem Kurs geht, fängt nie an.")

F["la6-checkliste"] = checkliste("la6-checkliste", "10.6", [
    "Meine Zugangsschlüssel liegen in der Datei daneben, nirgends sonst",
    "In meinem Arbeitsplatz stehen keine Daten anderer Menschen",
    "Meine Compliance-Regeln stehen in einer Wissensdatei",
    "Ich weiss, welche Arbeit ich als Nächstes zu einem Skill mache",
  ], 10,
  "Die ersten beiden Punkte sind nicht verhandelbar. Bei den anderen "
  "darf man nachziehen, bei diesen nicht.")

F["la6-schluss"] = folie("la6-schluss",
    eyebrow("Geschafft", ORANGE)
    + ('<h2 style="font-family:%s; font-size:96px; font-weight:700; line-height:1.15; color:%s">'
       'Du hast jetzt<br>einen Arbeitsplatz,<br>der dir gehört.</h2>' % (DISPLAY, CREME))
    + p("Was darin steht, hast du hineingeschrieben. Und er wird mit jeder "
        "Regel besser, die du ergänzt.", 36, PETROL),
    "Zum Schluss nichts mehr erklären. Bedank dich, sag einen Satz darüber, "
    "was du als Nächstes von ihr sehen willst, und hör auf.",
    stil=SEK_DUNKEL, uebergang="push")


ORDER = ["cover",
 "la1-titel","la1-geschichte","la1-regeln","la1-cloud","la1-weiter",
 "la2-titel","la2-warum","la2-schritte","la2-weiter",
 "la3-titel","la3-verbote","la3-formulierung","la3-weiter",
 "la4-titel","la4-drei","la4-praktisch","la4-weiter",
 "la5-titel","la5-woche","la5-teile","la5-satz",
 "la6-titel","la6-drei","la6-jetzt","la6-checkliste","la6-schluss"]

SECTIONS = {
 "auftakt": {"description": "Worum es in Modul 10 geht.", "start": "cover"},
 "la1": {"description": "Lektion 10.1 — was nie in einen Arbeitsplatz gehört.", "start": "la1-titel"},
 "la2": {"description": "Lektion 10.2 — wenn doch ein Schlüssel offen lag.", "start": "la2-titel"},
 "la3": {"description": "Lektion 10.3 — was du für jeden Satz verantwortest.", "start": "la3-titel"},
 "la4": {"description": "Lektion 10.4 — die Grenzen der KI.", "start": "la4-titel"},
 "la5": {"description": "Lektion 10.5 — eine echte Woche von Anfang bis Ende.", "start": "la5-titel"},
 "la6": {"description": "Lektion 10.6 — wo es weitergeht und was als Nächstes dran ist.", "start": "la6-titel"},
}

schreibe(ZIEL, "Modul 10 — Sicherheit, Grenzen und das Ganze", F, ORDER, SECTIONS)
