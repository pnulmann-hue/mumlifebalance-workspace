#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Folien fuer Modul 7 — Social Media mit Claude Code.

    python scripts/ki-kurs/folien-modul-7.py <zielordner>
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from folien_basis import *

ZIEL = sys.argv[1] if len(sys.argv) > 1 else "folien-modul-7"
F = {}

F["cover"] = modulcover(7, "Social Media",
    "Ab hier kommt keine neue Technik mehr. Ab hier wird angewendet.",
    "Sag am Anfang, dass sie alles Nötige schon kann. Was jetzt kommt, sind "
    "Skills und Bots für einen bestimmten Zweck.")

# ── 7.1 Überblick ────────────────────────────────────────────────────
F["l71-titel"] = lektionstitel("l71-titel", "7.1", "Die Maschinen im Überblick",
    "Ein Skill je Format. Alle lesen dieselben Wissensdateien.",
    "Zeig den Ordner. Links die Skills, rechts die Wissensdateien daneben — "
    "das Bild trägt die ganze Lektion.")

F["l71-aufbau"] = folie("l71-aufbau",
    eyebrow("Lektion 7.1")
    + h2("Wie das zusammenhängt")
    + gegenueber(
        "Die Maschine",
        ["Ein Skill je Format: Caption, Story, Karussell, Reel.",
         "Er weiss, wie das Format gebaut ist.",
         "Den bekommst du fertig."],
        "Der Treibstoff",
        ["Deine Wissensdateien: deine Stimme, deine Zielgruppe, deine Verbote.",
         "Sie wissen, was bei dir hineingehört.",
         "Die füllst du."]),
    "Das ist der Gedanke, auf dem der ganze Kurs steht. Wiederhol ihn hier "
    "ruhig wörtlich, auch wenn er in Modul 1 schon kam.")

F["l71-leer"] = folie("l71-leer",
    eyebrow("Lektion 7.1")
    + h2("Deine Wissensdateien sind am Anfang leer")
    + p("Das ist so gewollt. Jede Datei hat eine Überschrift und darunter Platz — "
        "du füllst sie mit dem, was für dein Business gilt.", 40)
    + p("Was inhaltlich hineingehört, ist ein Thema für sich. Dafür gibt es die "
        "Instagram-Kundenmaschine. Hier geht es darum, dass die Maschine läuft.", 32, GEDAEMPFT),
    "Diesen Verweis machst du in diesem Modul mehrfach. Nicht entschuldigend, "
    "sondern als klare Aufteilung: hier das Werkzeug, dort der Inhalt.")

F["l71-weiter"] = weiter("l71-weiter", "Als Nächstes",
    "Caption und Story",
    "Und die Demonstration, die den Unterschied sichtbar macht.",
    "Kündige an, dass in der nächsten Lektion derselbe Skill zweimal läuft — "
    "einmal leer, einmal gefüllt.")

# ── 7.2 Caption und Story — die Demonstration ────────────────────────
F["l72-titel"] = lektionstitel("l72-titel", "7.2", "Caption und Story",
    "Derselbe Skill, zweimal. Einmal leer, einmal gefüllt.",
    "Die wichtigste Demonstration im ganzen Kurs. Lass dir Zeit und schneide "
    "hier nichts weg — beide Ergebnisse müssen ganz zu lesen sein.")

F["l72-versuch"] = folie("l72-versuch",
    eyebrow("Lektion 7.2")
    + h2("Der Versuch")
    + reihe([
        karte("Durchgang 1", ["Wissensdateien leer.",
                              "Der Skill läuft trotzdem und liefert eine Caption.",
                              "Sie ist brauchbar und klingt nach niemandem."]),
        karte("Durchgang 2", ["Dieselbe Aufgabe, Wissensdateien gefüllt.",
                              "Derselbe Skill, kein Wort daran geändert.",
                              "Die Caption klingt nach mir."], ORANGE),
      ]),
    "Lies beide Ergebnisse laut vor. Der Unterschied ist zu hören, nicht zu "
    "erklären — und genau darum geht es.")

F["l72-lehre"] = statement("l72-lehre",
    ["Die Maschine bestimmt,", "ob etwas herauskommt.", "Der Treibstoff bestimmt,", "ob es nach dir klingt."],
    "Beides brauchst du. Nur eins davon kann ich dir geben.",
    "Der zweite Satz ist der ehrlichste im Kurs. Sag ihn ohne Verkaufston.")

F["l72-story"] = folie("l72-story",
    eyebrow("Lektion 7.2")
    + h2("Story funktioniert gleich")
    + p("Derselbe Aufbau, andere Form: mehrere kurze Bilder nacheinander statt "
        "eines Textes.", 40)
    + liste([
        "Der Skill kennt den Aufbau einer Story-Abfolge.",
        "Deine Wissensdateien liefern Ton, Thema und deinen Handlungsaufruf.",
        "Beides kommt aus denselben Dateien wie bei der Caption.",
      ], 32),
    "Kurz halten. Wer die Demonstration von eben gesehen hat, braucht sie hier "
    "nicht nochmal. Zeig nur, dass dieselben Dateien auch die Story tragen.")

F["l72-weiter"] = weiter("l72-weiter", "Als Nächstes",
    "Karussell — vom Text zum fertigen Bild",
    "Jetzt wird aus Text etwas, das man posten kann.",
    "Kurze Brücke, und sag dazu, dass die Texte zuerst kommen und erst danach "
    "die Bilder. Das ist gleich die Kernaussage der nächsten Lektion.")

# ── 7.3 Karussell ────────────────────────────────────────────────────
F["l73-titel"] = lektionstitel("l73-titel", "7.3", "Karussell",
    "Vom Text zum fertigen Bild.",
    "Zwei Werkzeuge in einer Lektion — erst die Folientexte, dann der "
    "Bild-Editor. Zeig den Übergang, nicht jedes Werkzeug einzeln.")

F["l73-zweischritt"] = folie("l73-zweischritt",
    eyebrow("Lektion 7.3")
    + h2("Zwei Schritte")
    + reihe([
        karte("1 · Die Texte", ["Der Skill schreibt die Folien.",
                                "Du liest sie und änderst, was nicht stimmt.",
                                "Erst danach wird gebaut."]),
        karte("2 · Die Bilder", ["Die Texte gehen in den Bild-Editor.",
                                 "Dort wählst du Foto, Farbe und Textgrösse.",
                                 "Heraus kommen fertige Folien."], ORANGE),
      ]),
    "Sag deutlich, warum die Reihenfolge so ist: wer zuerst baut und dann liest, "
    "baut zehn Folien zweimal.")

F["l73-editor"] = folie("l73-editor",
    eyebrow("Lektion 7.3")
    + h2("Warum ein eigener Editor")
    + liste([
        "Dein Format, deine Farben, deine Schriften — jedes Mal gleich.",
        "Alle Folien auf einen Blick, nicht eine nach der anderen.",
        "Du siehst beim Tippen, wie es aussieht.",
        "Und am Ende lädst du alle auf einmal herunter.",
      ], 34),
    "Das ist ein Artifact, und wie du selbst eines baust, kommt in Modul 9. "
    "Hier nur zeigen, was es kann.")

F["l73-weiter"] = weiter("l73-weiter", "Als Nächstes",
    "Reel — Rohschnitt aus Rohmaterial",
    "Die Aufbaustufe dieses Moduls. Etwas mehr Einrichtung, dafür der grösste Gewinn.",
    "Sag das mit der Aufbaustufe schon hier, damit niemand überrascht ist. Und "
    "sag im selben Atemzug, dass man sie überspringen darf.")

# ── 7.4 Reel ─────────────────────────────────────────────────────────
F["l74-titel"] = lektionstitel("l74-titel", "7.4", "Reel",
    "Einmal frei sprechen, mit Versprechern. Den Rest macht die Maschine.",
    "Zeig ein echtes Vorher/Nachher. Das Rohmaterial mit deinen Versprechern "
    "darf ruhig peinlich sein — das ist der Punkt.")

F["l74-ablauf"] = folie("l74-ablauf",
    eyebrow("Lektion 7.4")
    + h2("Was passiert")
    + liste([
        "Du sprichst frei in die Kamera und wiederholst Sätze, so oft du willst.",
        "Die Maschine schreibt mit und erkennt, welcher Anlauf der letzte war.",
        "Sie legt dir die Schnittliste als Text vor.",
        "<b>Du gibst sie frei</b>, dann wird geschnitten.",
      ], 34),
    "Der vierte Punkt ist kein Zwischenschritt, den man auslassen kann. "
    "Ohne ihn schneidet sie Sätze weg, die du behalten wolltest.")

F["l74-regel"] = folie("l74-regel",
    eyebrow("Lektion 7.4")
    + h2("Die Regel dahinter")
    + p("Wenn du einen Satz dreimal sagst, gewinnt der letzte vollständige Anlauf.", 44, BLAU)
    + p("So sprichst du beim Drehen ohne Druck: geht ein Satz daneben, holst du "
        "einfach Luft und sagst ihn nochmal. Die Maschine nimmt den letzten.", 34, GEDAEMPFT),
    "Sag dazu, dass diese eine Regel das Drehen komplett verändert hat. "
    "Vorher hast du jeden Versprecher neu angesetzt.")

F["l74-aufbau"] = folie("l74-aufbau",
    eyebrow("Lektion 7.4")
    + h2("Ehrlich zur Einrichtung")
    + liste([
        "Dafür müssen drei Programme auf deinem Rechner sein.",
        "Die Anleitung dazu liegt unter diesem Video, Schritt für Schritt.",
        "Es kostet einen Nachmittag. Einmal.",
        "Wenn dir das gerade zu viel ist: überspring die Lektion und komm später zurück.",
      ], 34),
    "Der letzte Punkt ist wichtig. Wer hier hängenbleibt, hört sonst beim ganzen "
    "Modul auf — dabei sind 7.5 bis 7.7 die wertvolleren Lektionen.")

F["l74-weiter"] = weiter("l74-weiter", "Als Nächstes",
    "Freigabe statt Autopilot",
    "Die Lektion, wegen der bei mir seit über einem Jahr nichts schiefgegangen ist.",
    "Werde hier ernst im Ton. Was jetzt kommt, ist die wichtigste Haltung "
    "im ganzen Kurs.")

# ── 7.5 Freigabe ─────────────────────────────────────────────────────
F["l75-titel"] = lektionstitel("l75-titel", "7.5", "Freigabe statt Autopilot",
    "Bei mir geht nichts nach draussen, das ich nicht gesehen habe.",
    "Erzähl, warum das bei dir keine Vorsichtsmassnahme ist, sondern eine "
    "Voraussetzung. Ohne den Grund klingt es nach Ängstlichkeit.")

F["l75-warum"] = folie("l75-warum",
    eyebrow("Lektion 7.5")
    + h2("Warum das bei uns anders ist")
    + p("Mein Instagram-Konto hängt an einem Partnerunternehmen. Ein unbedachter "
        "Satz über ein Produkt kostet mich mehr, als mir eine automatisch "
        "geschriebene Woche je einbringt.", 40)
    + p("Wer nur für sich selbst schreibt, kann anders entscheiden. Wir nicht.", 34, PETROL),
    "Das ist der Satz, der diesen Kurs von jedem Technikkurs unterscheidet. "
    "Niemand sonst denkt beim Automatisieren an den Partnervertrag.")

F["l75-wie"] = folie("l75-wie",
    eyebrow("Lektion 7.5")
    + h2("Wie das praktisch aussieht")
    + reihe([
        karte("Vorschlag", ["Die Maschine legt fertige Beiträge ab.",
                            "Sichtbar, lesbar, änderbar."]),
        karte("Freigabe", ["Du liest, änderst, gibst frei.",
                           "Ein Knopf. Das ist dein Ja."], ORANGE),
        karte("Abendlauf", ["Nimmt am Abend nur das Freigegebene.",
                            "Alles andere bleibt liegen."]),
      ]),
    "Zeig den Knopf. Dass die Freigabe wirklich nur ein Klick ist, macht den "
    "Unterschied zwischen Vorsicht und Mehrarbeit.")

F["l75-satz"] = statement("l75-satz",
    ["Die Maschine schlägt vor.", "Den Knopf drückst du."],
    "Das ist die ganze Sicherheitsarchitektur, und sie reicht.",
    "Kurz sprechen und die Folie zwei Sekunden stehen lassen. Wer sonst nichts "
    "aus diesem Modul behält, soll diesen Satz behalten.")

F["l75-weiter"] = weiter("l75-weiter", "Als Nächstes",
    "Automatisiertes Posten",
    "Was nach deiner Freigabe von selbst passiert.",
    "Kurze Brücke, und sag dazu, dass ab dem Knopf wirklich nichts mehr von "
    "Hand passiert — auch nicht das Hochladen der Bilder.")

# ── 7.6 Posten ───────────────────────────────────────────────────────
F["l76-titel"] = lektionstitel("l76-titel", "7.6", "Automatisiertes Posten",
    "Abends freigegeben, am Morgen draussen.",
    "Zeig den ganzen Weg an einem echten Beitrag. Von der Freigabe bis zum "
    "Post auf dem Handy.")

F["l76-abend"] = folie("l76-abend",
    eyebrow("Lektion 7.6")
    + h2("Der Abendlauf")
    + liste([
        "<b>Tagsüber</b> liest du die Vorschläge und gibst frei, was passt.",
        "<b>Um acht</b> holt der Abendlauf alles Freigegebene ab.",
        "<b>Er prüft</b> zuerst trocken: Zeitpunkt in der Zukunft, Text da, Bilder da.",
        "<b>Dann plant er ein</b> und meldet dir, was er gemacht hat.",
      ], 32),
    "Der dritte Punkt ist der, den man beim Bauen vergisst. Eine Prüfung vorher "
    "ist der Unterschied zwischen einer Meldung und einem Rätsel am nächsten Tag.")

F["l76-stolper"] = folie("l76-stolper",
    eyebrow("Lektion 7.6")
    + h2("Zwei Stolpersteine, die ich selbst hatte")
    + gegenueber(
        "Der Zeitpunkt war vorbei",
        ["Am selben Abend freigegeben, für denselben Abend geplant.",
         "Der Dienst nimmt nichts in der Vergangenheit an.",
         "Die Freigabe meldete trotzdem Erfolg."],
        "Doppelt gepostet",
        ["Von Hand gepostet, die Freigabe stand aber weiter auf offen.",
         "Der Abendlauf hätte es ein zweites Mal eingeplant.",
         "Seitdem gibt es einen Knopf für hab ich selbst gemacht."]),
    "Beide Geschichten ehrlich erzählen. Sie zeigen, dass Automatisierung nicht "
    "heisst, dass man nicht mehr hinschaut.")

F["l76-weiter"] = weiter("l76-weiter", "Als Nächstes",
    "Wenn die KI Murks baut",
    "Woran du erkennst, dass ein Text von einer Maschine kommt — und was dagegen hilft.",
    "Kurze Brücke. Die nächste Lektion ist die, die sie am häufigsten "
    "wiederholen wird.")

# ── 7.7 Murks ────────────────────────────────────────────────────────
F["l77-titel"] = lektionstitel("l77-titel", "7.7", "Wenn die KI Murks baut",
    "Automatisch erzeugter Text wird schlecht, sobald niemand mehr liest.",
    "Zeig einen echten Fund aus deinem Prüfskript. Ein Beispiel aus deinem "
    "eigenen Material wiegt schwerer als jede Warnung.")

F["l77-muster"] = folie("l77-muster",
    eyebrow("Lektion 7.7")
    + h2("Woran man es erkennt")
    + liste([
        "Immer dieselben Satzmuster, quer durch alle Beiträge.",
        "Grosse Wörter ohne Inhalt dahinter.",
        "Drei Sätze in Folge, die alle gleich anfangen.",
        "Eine Behauptung mit einer Zahl, die nirgends herkommt.",
      ], 34),
    "Der letzte Punkt ist der gefährlichste, weil er stimmen könnte. "
    "Jede Zahl gehört überprüft, bevor sie rausgeht.")

F["l77-skript"] = folie("l77-skript",
    eyebrow("Lektion 7.7")
    + h2("Deshalb prüft ein Skript mit")
    + p("Du sammelst deine eigenen Muster in einer Liste, und ein kleines Prüfskript "
        "geht damit über jeden Text, bevor er rausgeht.", 40)
    + p("📎 Die Prüf-Mechanik liegt als Vorlage unter diesem Video. Die Liste füllst "
        "du mit dem, was dich an deinen eigenen Texten stört.", 30, PETROL),
    "Sag, warum ein Skript und nicht dein Gedächtnis: eine Prüfung aus dem Kopf "
    "findet das, woran man gerade denkt.")

F["l77-grenze"] = folie("l77-grenze",
    eyebrow("Lektion 7.7")
    + h2("Was ein Skript nicht kann")
    + liste([
        "Berührt es sie?",
        "Nimmt sie etwas Konkretes mit?",
        "Warum sollte sie das speichern oder weiterschicken?",
        "Warum sollte sie darunter etwas schreiben?",
      ], 36)
    + p("Diese vier Fragen bleiben deine Arbeit. Dauert zwei Minuten je Beitrag.", 32, PETROL),
    "Das ist deine Qualitätsabnahme. Eine Frage mit Nein, und der Beitrag wird "
    "überarbeitet statt gepostet.")

# ── 7.8 Zusammenfassung ──────────────────────────────────────────────
F["l78-titel"] = lektionstitel("l78-titel", "7.8", "Zusammenfassung",
    "Die Maschinen laufen. Der Treibstoff ist deine Arbeit.",
    "Fass zusammen und sag klar, wo es für den Inhalt weitergeht. "
    "Kein Verkaufston, nur die Adresse.")

F["l78-bilanz"] = folie("l78-bilanz",
    eyebrow("Lektion 7.8")
    + h2("Das steht jetzt")
    + reihe([
        karte("Vier Maschinen", ["Caption, Story, Karussell, Reel — alle laufen."]),
        karte("Ein Prüfweg", ["Skript für die Muster, vier Fragen für dich."], ORANGE),
        karte("Eine Regel", ["Nichts geht raus, was du nicht freigegeben hast."]),
      ]),
    "Die dritte Karte ist die, die bleibt, auch wenn sich die Werkzeuge ändern.")

F["l78-checkliste"] = checkliste("l78-checkliste", "7.8", [
    "Ich habe einen Content-Skill laufen lassen",
    "Ich habe mindestens eine Wissensdatei gefüllt",
    "Ich habe den Unterschied zwischen leer und gefüllt selbst gesehen",
    "Bei mir geht nichts raus ohne meine Freigabe",
  ], 7,
  "Der dritte Punkt ist der, der hängenbleibt. Wer den Unterschied selbst "
  "erzeugt hat, füllt danach die anderen Dateien von allein.")

F["l78-weiter"] = folie("l78-weiter",
    eyebrow("Modul 8", ORANGE)
    + ('<h2 style="font-family:%s; font-size:84px; font-weight:700; line-height:1.15; color:%s">'
       'Produkte, Seiten<br>und Mails</h2>' % (DISPLAY, CREME))
    + p("Dieselbe Mechanik, anderer Zweck: von der Produktidee bis zur fertigen "
        "Verkaufsseite auf deiner Website.", 36, PETROL),
    "Kurz. Und sag dazu, dass die Inhalte für Modul 8 in der digitalen "
    "Produktwelt stehen — dieselbe Aufteilung wie hier.",
    stil=SEK_DUNKEL, uebergang="push")


ORDER = ["cover",
 "l71-titel","l71-aufbau","l71-leer","l71-weiter",
 "l72-titel","l72-versuch","l72-lehre","l72-story","l72-weiter",
 "l73-titel","l73-zweischritt","l73-editor","l73-weiter",
 "l74-titel","l74-ablauf","l74-regel","l74-aufbau","l74-weiter",
 "l75-titel","l75-warum","l75-wie","l75-satz","l75-weiter",
 "l76-titel","l76-abend","l76-stolper","l76-weiter",
 "l77-titel","l77-muster","l77-skript","l77-grenze",
 "l78-titel","l78-bilanz","l78-checkliste","l78-weiter"]

SECTIONS = {
 "auftakt": {"description": "Worum es in Modul 7 geht.", "start": "cover"},
 "l71": {"description": "Lektion 7.1 — Maschine und Treibstoff im Überblick.", "start": "l71-titel"},
 "l72": {"description": "Lektion 7.2 — derselbe Skill leer und gefüllt.", "start": "l72-titel"},
 "l73": {"description": "Lektion 7.3 — Karussell vom Text zum Bild.", "start": "l73-titel"},
 "l74": {"description": "Lektion 7.4 — Reel-Rohschnitt aus Rohmaterial.", "start": "l74-titel"},
 "l75": {"description": "Lektion 7.5 — warum nichts ohne Freigabe rausgeht.", "start": "l75-titel"},
 "l76": {"description": "Lektion 7.6 — der Abendlauf und zwei Stolpersteine.", "start": "l76-titel"},
 "l77": {"description": "Lektion 7.7 — KI-Muster erkennen und prüfen.", "start": "l77-titel"},
 "l78": {"description": "Lektion 7.8 — Bilanz und Checkliste vor Modul 8.", "start": "l78-titel"},
}

schreibe(ZIEL, "Modul 7 — Social Media", F, ORDER, SECTIONS)
