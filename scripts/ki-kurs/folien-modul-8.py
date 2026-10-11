#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Folien fuer Modul 8 — Produkte, Seiten und Mails.

    python scripts/ki-kurs/folien-modul-8.py <zielordner>
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from folien_basis import *

ZIEL = sys.argv[1] if len(sys.argv) > 1 else "folien-modul-8"
F = {}

F["cover"] = modulcover(8, "Produkte, Seiten<br>und Mails",
    "Dieselbe Mechanik wie beim Content. Anderer Zweck.",
    "Sag am Anfang, dass hier nichts Neues an Technik kommt. Wer Modul 5 und 7 "
    "hat, versteht dieses Modul in der Hälfte der Zeit.")

# ── 8.1 Überblick ────────────────────────────────────────────────────
F["l81-titel"] = lektionstitel("l81-titel", "8.1", "Die Maschinen",
    "Produkt, Verkaufsseite, Mailstrecke — je ein Skill.",
    "Zeig den Ordner wie in Modul 7. Dasselbe Bild, andere Namen — "
    "das ist genau die Botschaft.")

F["l81-drei"] = folie("l81-drei",
    eyebrow("Lektion 8.1")
    + h2("Drei Maschinen")
    + reihe([
        karte("Produkt", ["Von der Idee zur Gliederung.",
                          "Module, Lektionen, Arbeitsblätter."]),
        karte("Verkaufsseite", ["Von der Gliederung zur fertigen Seite.",
                                "Alle Textblöcke in einem Durchgang."], ORANGE),
        karte("Mails", ["Von der Verkaufsseite zur Strecke.",
                        "Was nach dem Kauf passiert."]),
      ]),
    "Sag, dass sie aufeinander aufbauen. Wer bei der Gliederung schludert, "
    "merkt es erst auf der Verkaufsseite.")

F["l81-verweis"] = folie("l81-verweis",
    eyebrow("Lektion 8.1")
    + h2("Und der Treibstoff?")
    + p("Wie eine Produkttreppe aufgebaut wird, was auf eine Verkaufsseite gehört "
        "und in welcher Reihenfolge die Mails kommen — das ist ein Thema für sich.", 40)
    + p("Dafür gibt es die digitale Produktwelt. Hier geht es darum, dass die "
        "Maschine läuft und wo du deine Antworten hineinschreibst.", 32, GEDAEMPFT),
    "Dieselbe Aufteilung wie in Modul 7. Ruhig aussprechen, nicht "
    "entschuldigend — das ist eine saubere Trennung und keine Lücke.")

F["l81-weiter"] = weiter("l81-weiter", "Als Nächstes",
    "Eine Verkaufsseite bauen lassen",
    "Von der Beschreibung zur fertigen Seite, in einem Durchgang.",
    "Kurze Brücke, und sag dazu, dass am Ende wirklich eine Seite dasteht, "
    "die man anschauen kann — kein Textentwurf.")

# ── 8.2 Verkaufsseite ────────────────────────────────────────────────
F["l82-titel"] = lektionstitel("l82-titel", "8.2", "Eine Verkaufsseite bauen",
    "Du beschreibst dein Angebot. Heraus kommt eine Seite.",
    "Live mitfilmen mit einem echten Angebot. Nimm eines, das du wirklich "
    "verkaufst, sonst fehlen dir mitten drin die Antworten.")

F["l82-ablauf"] = folie("l82-ablauf",
    eyebrow("Lektion 8.2")
    + h2("Was der Skill von dir will")
    + liste([
        "Für wen ist das Angebot, und was ändert sich für sie?",
        "Wie ist es aufgebaut — Module, Dauer, Format?",
        "Was hält sie bisher ab, und wie antwortest du darauf?",
        "Der Preis, und der Grund, warum genau jetzt.",
      ], 34)
    + p("Vier Fragen. Wer sie beantworten kann, hat die Seite schon fast.", 32, PETROL),
    "Halt kurz an und sag, dass die vierte Frage die schwerste ist. "
    "Wer darauf keine Antwort hat, hat kein Angebotsproblem, sondern ein Klarheitsproblem.")

F["l82-design"] = folie("l82-design",
    eyebrow("Lektion 8.2")
    + h2("Und das Aussehen?")
    + p("Deine Farben, deine Schriften und dein Aufbau stehen in einer Datei. "
        "Der Skill liest sie mit, also sieht jede Seite aus wie deine.", 40)
    + p("Einmal eingerichtet, gilt das für alles, was danach kommt.", 34, GEDAEMPFT),
    "Zeig kurz die Datei mit den Farben. Dass man das einmal festlegt und nie "
    "wieder anfasst, ist der eigentliche Gewinn.")

F["l82-weiter"] = weiter("l82-weiter", "Als Nächstes",
    "Auf die eigene Website bringen",
    "Die Seite liegt bis hierher nur bei dir auf dem Rechner.",
    "Kurze Brücke. Der nächste Schritt ist der, vor dem die meisten "
    "zurückschrecken, und er ist der einfachste.")

# ── 8.3 Auf die Website ──────────────────────────────────────────────
F["l83-titel"] = lektionstitel("l83-titel", "8.3", "Auf die eigene Website",
    "Hochladen, Adresse einrichten, anschauen.",
    "Zeig es an deiner echten Website. Und zeig, dass die Seite zuerst "
    "unveröffentlicht liegt, bevor irgendjemand sie sieht.")

F["l83-schritte"] = folie("l83-schritte",
    eyebrow("Lektion 8.3")
    + h2("Drei Schritte")
    + liste([
        "<b>Als Entwurf anlegen.</b> Die Seite ist da, aber noch für niemanden sichtbar.",
        "<b>Anschauen und korrigieren.</b> Am Rechner und am Handy.",
        "<b>Veröffentlichen.</b> Das machst du selbst, mit einem Klick.",
      ], 34)
    + p("Nichts geht online, solange du nicht darauf gedrückt hast — "
        "dieselbe Regel wie beim Posten.", 32, PETROL),
    "Der Verweis auf Modul 7 ist wichtig. Es ist dieselbe Haltung, "
    "nur an einer anderen Stelle.")

F["l83-handy"] = folie("l83-handy",
    eyebrow("Lektion 8.3")
    + h2("Am Handy anschauen, immer")
    + p("Die meisten deiner Kundinnen lesen die Seite auf dem Handy, zwischen "
        "zwei Dingen. Was am Rechner gut aussieht, kann dort zerfallen.", 40)
    + liste([
        "Passt die Überschrift auf zwei Zeilen?",
        "Ist der Kaufknopf sichtbar, ohne lange zu scrollen?",
        "Sind die Absätze kurz genug zum Überfliegen?",
      ], 32),
    "Zeig es am eigenen Handy, nicht in einer Vorschau. Eine echte "
    "Handy-Ansicht findet Dinge, die keine Vorschau zeigt.")

F["l83-weiter"] = weiter("l83-weiter", "Als Nächstes",
    "Mails und Verteiler anbinden",
    "Was passiert, nachdem jemand gekauft hat.",
    "Kurze Brücke, und sag vorweg, dass hier ein Zugang dranhängt — "
    "das ist die eine Stelle im Kurs, wo es nicht ohne geht.")

# ── 8.4 Mails ────────────────────────────────────────────────────────
F["l84-titel"] = lektionstitel("l84-titel", "8.4", "Mails und Verteiler",
    "Die Verbindung zu deinem Mailanbieter.",
    "Sei hier ehrlich über die Voraussetzung. Wer keinen Mailanbieter hat, "
    "kann die Lektion anschauen und später zurückkommen.")

F["l84-zugang"] = folie("l84-zugang",
    eyebrow("Lektion 8.4")
    + h2("Was du dafür brauchst")
    + liste([
        "Einen Mailanbieter, bei dem deine Liste liegt.",
        "Einen Zugangsschlüssel von dort — den holst du in dessen Einstellungen.",
        "Und die Regel aus Modul 6: der Schlüssel gehört in die Datei daneben.",
      ], 34)
    + p("Ohne Mailanbieter kannst du die Mails trotzdem schreiben lassen und "
        "von Hand einsetzen. Nur das Eintragen fällt dann weg.", 32, PETROL),
    "Der letzte Satz hält die zurück, die noch keinen Anbieter haben. "
    "Die Lektion ist auch ohne Anbindung etwas wert.")

F["l84-strecke"] = folie("l84-strecke",
    eyebrow("Lektion 8.4")
    + h2("Was eine Strecke ausmacht")
    + reihe([
        karte("Ausliefern", ["Was sie gekauft hat, und wie sie hinkommt.",
                             "Sofort nach dem Kauf."]),
        karte("Dranbleiben", ["Kleine Schritte über die ersten Tage.",
                              "Damit sie wirklich anfängt."], ORANGE),
        karte("Weitergehen", ["Erst wenn sie einen Gewinn hat.",
                              "Nie vorher."]),
      ]),
    "Die dritte Karte ist eine Haltungsfrage. Wer am zweiten Tag das nächste "
    "Produkt anbietet, verkauft einmal und nie wieder.")

F["l84-weiter"] = weiter("l84-weiter", "Als Nächstes",
    "Zusammenfassung",
    "Was jetzt steht, und was aus der Produktwelt dazukommt.",
    "Kurze Brücke, und nimm dir für die Zusammenfassung wirklich nur zwei "
    "Minuten. Wer bis hier gekommen ist, will weiterbauen statt zuhören.")

# ── 8.5 Zusammenfassung ──────────────────────────────────────────────
F["l85-titel"] = lektionstitel("l85-titel", "8.5", "Zusammenfassung",
    "Drei Maschinen mehr — und dieselbe Regel wie überall.",
    "Kurz halten, und die Freigabe-Regel nochmal nennen. Sie gilt hier "
    "genauso wie beim Posten.")

F["l85-bilanz"] = folie("l85-bilanz",
    eyebrow("Lektion 8.5")
    + h2("Das steht jetzt")
    + liste([
        "Eine Gliederung für ein Produkt, das du bauen willst.",
        "Eine Verkaufsseite in deinen Farben, als Entwurf.",
        "Eine Mailstrecke für die Zeit nach dem Kauf.",
        "Und niemand sieht etwas davon, bis du es veröffentlichst.",
      ], 34),
    "Der letzte Punkt ist der rote Faden durch den ganzen Kurs. "
    "Sag ihn jedes Mal mit.")

F["l85-checkliste"] = checkliste("l85-checkliste", "8.5", [
    "Ich habe eine Verkaufsseite als Entwurf gebaut",
    "Sie steht in meinen Farben und Schriften",
    "Ich habe sie am Handy angeschaut",
    "Ich weiss, wo mein Zugangsschlüssel liegt und wo nicht",
  ], 8,
  "Beim letzten Punkt nicht nachgeben. Wer den Schlüssel falsch ablegt, "
  "merkt es nie — bis es zu spät ist.")

F["l85-weiter"] = folie("l85-weiter",
    eyebrow("Modul 9", ORANGE)
    + ('<h2 style="font-family:%s; font-size:84px; font-weight:700; line-height:1.15; color:%s">'
       'Dein Cockpit</h2>' % (DISPLAY, CREME))
    + p("Eine eigene kleine Seite, die Claude befüllt und die du bedienst. "
        "Der Ort, an dem bei mir alles zusammenläuft.", 36, PETROL),
    "Mach neugierig. Modul 9 ist das, was die anderen Kurse nicht haben, "
    "und für viele der eigentliche Grund, dranzubleiben.",
    stil=SEK_DUNKEL, uebergang="push")


ORDER = ["cover",
 "l81-titel","l81-drei","l81-verweis","l81-weiter",
 "l82-titel","l82-ablauf","l82-design","l82-weiter",
 "l83-titel","l83-schritte","l83-handy","l83-weiter",
 "l84-titel","l84-zugang","l84-strecke","l84-weiter",
 "l85-titel","l85-bilanz","l85-checkliste","l85-weiter"]

SECTIONS = {
 "auftakt": {"description": "Worum es in Modul 8 geht.", "start": "cover"},
 "l81": {"description": "Lektion 8.1 — die drei Maschinen im Überblick.", "start": "l81-titel"},
 "l82": {"description": "Lektion 8.2 — eine Verkaufsseite bauen lassen.", "start": "l82-titel"},
 "l83": {"description": "Lektion 8.3 — die Seite auf die eigene Website bringen.", "start": "l83-titel"},
 "l84": {"description": "Lektion 8.4 — Mails und Verteiler anbinden.", "start": "l84-titel"},
 "l85": {"description": "Lektion 8.5 — Bilanz und Checkliste vor Modul 9.", "start": "l85-titel"},
}

schreibe(ZIEL, "Modul 8 — Produkte, Seiten und Mails", F, ORDER, SECTIONS)
