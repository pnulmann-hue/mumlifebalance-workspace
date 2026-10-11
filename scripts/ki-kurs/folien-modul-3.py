#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Folien fuer Modul 3 — Claude Cowork, die Mittelstufe.

    python scripts/ki-kurs/folien-modul-3.py <zielordner>
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from folien_basis import *

ZIEL = sys.argv[1] if len(sys.argv) > 1 else "folien-modul-3"
F = {}

F["cover"] = modulcover(3, "Claude Cowork",
    "Die KI arbeitet mit deinen Dateien und hängt an deiner eigenen Planung. "
    "Und du baust deinen ersten Bot.",
    "Sag gleich, dass hier nichts installiert wird. Es ist dieselbe Oberfläche wie im Chat, "
    "nur mit zwei Sachen mehr. Das nimmt die Hürde vor dem Wort Stufe.")

# ── 3.1 Was Cowork kann ──────────────────────────────────────────────
F["l31-titel"] = lektionstitel("l31-titel", "3.1", "Was Cowork kann,<br>was der Chat nicht kann",
    "Dateien, Verbindungen und mehrere Schritte am Stück.",
    "Steig mit einer Aufgabe ein, die im Chat wirklich scheitert. Zum Beispiel: "
    "" + zit("Schau in meine Planung und sag mir, was diese Woche ansteht") + " — der Chat kann das nicht, "
    "und das ist der ganze Unterschied.", groesse=78)

F["l31-unterschied"] = folie("l31-unterschied",
    eyebrow("Lektion 3.1")
    + h2("Derselbe Auftrag, zwei Stufen")
    + gegenueber(
        "Im Chat",
        ["Du tippst alles hinein, was sie wissen muss.",
         "Am Ende des Gesprächs ist es wieder weg.",
         "Eine Aufgabe, eine Antwort."],
        "In Cowork",
        ["Sie öffnet deine Dateien selbst.",
         "Sie merkt sich, was beim letzten Mal war.",
         "Sie arbeitet über mehrere Schritte durch."]),
    "Zeig das an einem echten Beispiel auf dem Bildschirm. Nimm eine Aufgabe aus deiner "
    "eigenen Woche, nicht ein ausgedachtes Beispiel.")

F["l31-dateien"] = folie("l31-dateien",
    eyebrow("Lektion 3.1")
    + h2("Was du ihr geben kannst")
    + reihe([
        karte("Dokumente", ["Dein Business-Brief, deine Kursunterlagen, ein Protokoll.",
                            "Sie liest sie und arbeitet damit weiter."]),
        karte("Tabellen", ["Deine Zahlen, eine Kundenliste ohne Namen, eine Planung."], ORANGE),
        karte("Verbindungen", ["Deine Planung, dein Kalender, dein Mailprogramm.",
                               "Einmal einrichten, dann liest sie dort mit."]),
      ]),
    "Bei den Tabellen ausdrücklich sagen: Kundendaten mit Namen und Adressen gehören nicht hinein. "
    "Modul 10 geht darauf ein, hier reicht der Satz.")

F["l31-weiter"] = weiter("l31-weiter", "Als Nächstes",
    "Deine erste Verbindung",
    "Wir hängen deine Planung an, damit sie weiss, was bei dir diese Woche ansteht.",
    "Sag kurz, dass das einmal eingerichtet wird und danach einfach da ist. "
    "Die Angst vor dem Wort Verbindung ist grösser als die Sache.")

# ── 3.2 Notion verbinden ─────────────────────────────────────────────
F["l32-titel"] = lektionstitel("l32-titel", "3.2", "Deine erste Verbindung",
    "Einmal einrichten, und ab dann liest sie deine eigene Planung.",
    "Wenn du nicht mit Notion arbeitest: sag es offen und zeig die Verbindung, die du wirklich "
    "benutzt. Das Prinzip ist bei allen gleich.")

F["l32-warum"] = folie("l32-warum",
    eyebrow("Lektion 3.2")
    + h2("Warum das mehr bringt als es klingt")
    + p("Ohne Verbindung tippst du jedes Mal ab, was diese Woche ansteht. "
        "Mit Verbindung schaut sie selbst nach.", 40)
    + liste([
        "Sie kennt deine Termine, ohne dass du sie aufzählst.",
        "Sie sieht, was offen ist, und kann danach fragen.",
        "Du bekommst Antworten zu deiner Lage, nicht zu einer allgemeinen.",
      ], 32),
    "Der Unterschied wird erst beim dritten Mal deutlich. Sag das ruhig — beim ersten Mal "
    "wirkt es wie ein netter Zusatz, danach will man es nicht mehr hergeben.")

F["l32-schritte"] = folie("l32-schritte",
    eyebrow("Lektion 3.2")
    + h2("Wie es geht")
    + liste([
        "In den Einstellungen die Verbindung suchen und auswählen.",
        "Anmelden und bestätigen, worauf sie zugreifen darf.",
        "<b>Nur die Bereiche freigeben, die sie wirklich braucht.</b> Alles andere bleibt zu.",
        "Einmal ausprobieren: eine Frage stellen, deren Antwort nur in deiner Planung steht.",
      ], 34),
    "Klick für Klick mitfilmen, ohne Sprung. Beim dritten Punkt kurz innehalten — "
    "das ist der Moment, in dem viele einfach alles freigeben.")

F["l32-weiter"] = weiter("l32-weiter", "Als Nächstes",
    "Dein erster Bot",
    "Wir bauen zusammen einen Helfer fürs Zuhause. Ohne eine Zeile Code.",
    "Mach neugierig. Für die meisten ist das der Punkt, an dem es aufhört, abstrakt zu sein.")

# ── 3.3 Erster Bot ───────────────────────────────────────────────────
F["l33-titel"] = lektionstitel("l33-titel", "3.3", "Dein erster Bot",
    "Ohne eine Zeile Code — und etwas, wo nichts kaputtgehen kann.",
    "Sag, warum wir mit etwas Privatem anfangen: Wenn beim Haushalt etwas schiefgeht, "
    "ärgert sich niemand. Beim Business schon.")

F["l33-was"] = folie("l33-was",
    eyebrow("Lektion 3.3")
    + h2("Was wir bauen")
    + reihe([
        karte("Er liest", ["Deine Liste mit dem, was ansteht — Haushalt, Termine, Schulsachen."]),
        karte("Er sortiert", ["Was heute dran ist, was morgen, was warten kann."], ORANGE),
        karte("Er sagt es dir", ["In einer Nachricht, die du morgens lesen kannst."]),
      ]),
    "Zeig zuerst das Ergebnis, dann den Weg dorthin. Wenn sie sieht, was rauskommt, "
    "hört sie beim Bauen besser zu.")

F["l33-auftrag"] = folie("l33-auftrag",
    eyebrow("Lektion 3.3")
    + h2("Der Auftrag dahinter")
    + p("Ein Bot ist kein Programm. Er ist ein Auftrag, den du einmal richtig aufschreibst.", 40)
    + liste([
        "<b>Was er anschauen soll</b> — deine Liste.",
        "<b>Was er daraus machen soll</b> — sortieren nach heute, morgen, später.",
        "<b>Wie das Ergebnis aussehen soll</b> — kurz, ohne Einleitung, zum Überfliegen.",
        "<b>Was er nie tun soll</b> — nichts löschen und nichts verschicken.",
      ], 32)
    + p("📎 Den fertigen Auftrag zum Kopieren findest du unter diesem Video.", 30, PETROL),
    "Der letzte Punkt ist der wichtigste und wird immer vergessen. Ein Bot ohne Verbote "
    "macht irgendwann etwas, das du nicht wolltest.")

F["l33-satz"] = statement("l33-satz",
    ["Du hast gerade", "etwas gebaut,", "das für dich arbeitet."],
    "Ohne eine Zeile Code, in einer Viertelstunde.",
    "Lass den Moment stehen. Für viele ist das der erste Punkt im ganzen Kurs, an dem sie "
    "sich selbst etwas zutrauen.")

F["l33-weiter"] = weiter("l33-weiter", "Als Nächstes",
    "Wo Cowork aufhört",
    "Eine Sache kann dein Bot noch nicht — und das ist der ehrliche Grund für die nächste Stufe.",
    "Kündige an, dass jetzt eine Grenze kommt. Dass du sie selbst benennst, macht den Rest "
    "des Kurses glaubwürdiger.")

# ── 3.4 Grenze ───────────────────────────────────────────────────────
F["l34-titel"] = lektionstitel("l34-titel", "3.4", "Wo Cowork aufhört",
    "Was diese Stufe kann, was sie nicht kann, und wie du entscheidest.",
    "Kurze, ehrliche Lektion. Kein Verkaufsgespräch für Stufe 3.")

F["l34-grenze"] = folie("l34-grenze",
    eyebrow("Lektion 3.4")
    + h2("Die eine Sache, die fehlt")
    + p("Dein Bot läuft, wenn du ihn anstösst. Am Montagmorgen musst du die Oberfläche öffnen "
        "und ihn losschicken.", 40)
    + p("Was du eigentlich willst, ist eine Nachricht auf dem Handy, bevor du überhaupt "
        "aufgestanden bist. Dafür braucht er einen Ort, an dem er wohnt, und den bekommt er "
        "auf der nächsten Stufe.", 34, GEDAEMPFT),
    "Sag das ohne Druck. Wer den Bot morgens selbst anstösst, hat trotzdem etwas gewonnen.")

F["l34-entscheidung"] = folie("l34-entscheidung",
    eyebrow("Lektion 3.4")
    + h2("Woran du merkst, welche Stufe dran ist")
    + gegenueber(
        "Bleib bei Cowork, wenn",
        ["Du ein, zwei Sachen hast, die du regelmässig machst.",
         "Es dir nichts ausmacht, sie selbst anzustossen.",
         "Du gerade keine Zeit für Neues hast."],
        "Geh weiter, wenn",
        ["Du dieselbe Arbeit zum dritten Mal machst.",
         "Du willst, dass etwas läuft, während du schläfst.",
         "Du eigene Befehle für deine Wochenarbeit willst."]),
    "Lies beide Spalten vor und lass ihr einen Moment. Wer sich hier ehrlich einordnet, "
    "bricht später nicht ab.")

F["l34-satz"] = statement("l34-satz",
    ["Wenn dir das hier reicht,", "ist das völlig in Ordnung."],
    "Du hast eine KI, die deine Sachen kennt, und einen Helfer, der dir Arbeit abnimmt.",
    "Meine es so. Wer das Gefühl hat, aufhören zu dürfen, kommt eher wieder als jemand, "
    "der sich durchgedrückt fühlt.")

# ── 3.5 Zusammenfassung ──────────────────────────────────────────────
F["l35-titel"] = lektionstitel("l35-titel", "3.5", "Zusammenfassung",
    "Was jetzt bei dir steht — und was du entschieden hast.",
    "Kurze Lektion, drei bis vier Minuten.")

F["l35-bilanz"] = folie("l35-bilanz",
    eyebrow("Lektion 3.5")
    + h2("Das nimmst du mit")
    + reihe([
        karte("Eine Verbindung", ["Deine Planung hängt dran und wird gelesen."]),
        karte("Ein Helfer", ["Er sortiert dir, was ansteht, wenn du ihn anstösst."], ORANGE),
        karte("Eine Entscheidung", ["Du weisst, ob du auf Stufe 3 weitergehst oder hier bleibst."]),
      ]),
    "Geh die drei durch. Die dritte Karte ist die wichtigste — sie soll das bewusst "
    "entschieden haben und nicht einfach weiterklicken.")

F["l35-checkliste"] = checkliste("l35-checkliste", "3.5", [
    "Ich weiss, wann Cowork mehr bringt als der Chat",
    "Meine Planung ist angehängt und wird gelesen",
    "Ich habe einen Helfer gebaut, der etwas für mich tut",
    "Ich habe entschieden, ob ich auf Stufe 3 weitergehe",
  ], 3,
  "Beim letzten Punkt sagen: Beide Antworten sind richtig. Wer hier ehrlich Nein sagt, "
  "soll trotzdem ein gutes Gefühl haben.")

F["l35-weiter"] = folie("l35-weiter",
    eyebrow("Modul 4", ORANGE)
    + ('<h2 style="font-family:%s; font-size:84px; font-weight:700; line-height:1.15; color:%s">'
       'Claude Code —<br>dein Arbeitsplatz</h2>' % (DISPLAY, CREME))
    + p("Jetzt richtest du dir einen eigenen Platz ein, an dem dein Wissen, deine Dateien "
        "und deine Befehle zusammenliegen. Über die Desktop-App, ohne schwarzes Fenster.", 36, PETROL),
    "Nimm die Technik-Angst gleich hier vorweg. Ein Satz reicht, bewiesen wird es in Modul 4.",
    stil=SEK_DUNKEL, uebergang="push")


ORDER = ["cover",
 "l31-titel","l31-unterschied","l31-dateien","l31-weiter",
 "l32-titel","l32-warum","l32-schritte","l32-weiter",
 "l33-titel","l33-was","l33-auftrag","l33-satz","l33-weiter",
 "l34-titel","l34-grenze","l34-entscheidung","l34-satz",
 "l35-titel","l35-bilanz","l35-checkliste","l35-weiter"]

SECTIONS = {
 "auftakt": {"description": "Worum es in Modul 3 geht.", "start": "cover"},
 "l31": {"description": "Lektion 3.1 — was Cowork kann und der Chat nicht.", "start": "l31-titel"},
 "l32": {"description": "Lektion 3.2 — die eigene Planung anhängen.", "start": "l32-titel"},
 "l33": {"description": "Lektion 3.3 — der erste Bot ohne Code.", "start": "l33-titel"},
 "l34": {"description": "Lektion 3.4 — wo diese Stufe aufhört.", "start": "l34-titel"},
 "l35": {"description": "Lektion 3.5 — Bilanz und Checkliste vor Modul 4.", "start": "l35-titel"},
}

schreibe(ZIEL, "Modul 3 — Claude Cowork", F, ORDER, SECTIONS)
