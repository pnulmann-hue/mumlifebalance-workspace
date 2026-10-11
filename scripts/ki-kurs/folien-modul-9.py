#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Folien fuer Modul 9 — Dein Cockpit.

    python scripts/ki-kurs/folien-modul-9.py <zielordner>
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from folien_basis import *

ZIEL = sys.argv[1] if len(sys.argv) > 1 else "folien-modul-9"
F = {}

F["cover"] = modulcover(9, "Dein Cockpit",
    "Eine eigene kleine Seite, die Claude befüllt und die du bedienst.",
    "Zeig ganz am Anfang dein eigenes Cockpit auf dem Handy. Zwanzig Sekunden "
    "scrollen erklären mehr als fünf Minuten Reden.")

# ── 9.1 Was ein Artifact ist ─────────────────────────────────────────
F["l91-titel"] = lektionstitel("l91-titel", "9.1", "Was ein Artifact ist",
    "Eine kleine Seite mit Gedächtnis, die nur dir gehört.",
    "Lass den Fachbegriff nicht stehen, ohne ihn in einem Satz zu erklären. "
    "Und sag, dass sie dafür nichts installieren muss.")

F["l91-was"] = folie("l91-was",
    eyebrow("Lektion 9.1")
    + h2("Was daran anders ist")
    + gegenueber(
        "Ein Dokument",
        ["Text, den du liest.",
         "Änderungen machst du selbst, von Hand.",
         "Am Handy mühsam."],
        "Ein Cockpit",
        ["Knöpfe, Felder und Listen, die du bedienst.",
         "Claude schreibt hinein, du entscheidest.",
         "Am Handy gebaut, nicht nur irgendwie lesbar."]),
    "Der letzte Punkt rechts ist der praktische. Du gibst deinen Content "
    "zwischen zwei Terminen frei, nicht am Schreibtisch.")

F["l91-wofuer"] = folie("l91-wofuer",
    eyebrow("Lektion 9.1")
    + h2("Wofür sich das lohnt")
    + liste([
        "Alles, was du immer wieder abhakst oder freigibst.",
        "Jede Arbeit, bei der du sonst zwischen drei Programmen wechselst.",
        "Was du unterwegs am Handy brauchst und nicht am Schreibtisch.",
        "Und alles, was sich Zahlen oder Zustände merken soll.",
      ], 34),
    "Der vierte Punkt ist der, der ein Cockpit von einer hübschen Seite "
    "unterscheidet. Ein Gedächtnis macht es zum Werkzeug.")

F["l91-weiter"] = weiter("l91-weiter", "Als Nächstes",
    "Dein eigenes bauen",
    "Vom leeren Gerüst zur ersten Ansicht, live.",
    "Kurze Brücke, und sag, dass sie dafür kein Programmieren braucht. "
    "Sie beschreibt, was sie sehen will.")

# ── 9.2 Bauen ────────────────────────────────────────────────────────
F["l92-titel"] = lektionstitel("l92-titel", "9.2", "Dein eigenes bauen",
    "Du beschreibst, was du sehen willst. Claude baut die Seite.",
    "Nimm etwas Kleines und Echtes: eine Wochenliste, ein Abhak-Blatt. "
    "Ein zu grosses erstes Cockpit wird nie fertig.")

F["l92-weg"] = folie("l92-weg",
    eyebrow("Lektion 9.2")
    + h2("Der Weg")
    + reihe([
        karte("1 · Beschreiben", ["Was soll drauf sein, und was willst du damit tun?",
                                  "In ganzen Sätzen, wie einer Freundin."]),
        karte("2 · Bauen lassen", ["Claude schreibt die Seite und veröffentlicht sie für dich.",
                                   "Du bekommst eine Adresse."], ORANGE),
        karte("3 · Benutzen", ["Am Handy öffnen und ausprobieren.",
                               "Was fehlt, sagst du im Chat."]),
      ]),
    "Beim dritten Schritt betonen, dass Ändern normal ist. Das erste Cockpit "
    "ist ein Vorschlag, kein Ergebnis.")

F["l92-vorlage"] = folie("l92-vorlage",
    eyebrow("Lektion 9.2")
    + h2("Du musst nicht bei null anfangen")
    + p("Unter diesem Video liegt eine leere Cockpit-Vorlage: Reiter, Listen, "
        "Knöpfe und ein Gedächtnis — alles da, nur ohne deine Inhalte.", 40)
    + p("📎 Cockpit-Vorlage · Anleitung zum Anpassen", 30, PETROL),
    "Zeig, wo sie ihren eigenen Inhalt hineinschreibt. Und sag dazu, dass "
    "die Vorlage auf dem Handy schon funktioniert.")

F["l92-gedaechtnis"] = folie("l92-gedaechtnis",
    eyebrow("Lektion 9.2")
    + h2("Das Gedächtnis ist der Unterschied")
    + p("Was du im Cockpit abhakst, bleibt abgehakt — auch wenn du die Seite "
        "schliesst und am nächsten Tag am Rechner öffnest.", 40)
    + p("Das ist der Grund, warum es ein Cockpit ist und keine Liste zum "
        "Anschauen. Claude kann später lesen, was du dort entschieden hast.", 32, GEDAEMPFT),
    "Der zweite Absatz ist die Brücke zur nächsten Lektion. Genau davon "
    "lebt der Abendlauf.")

F["l92-weiter"] = weiter("l92-weiter", "Als Nächstes",
    "Der Abendlauf",
    "Ein Bot, der abends abholt, was du im Cockpit freigegeben hast.",
    "Kurze Brücke, und sag dazu, dass jetzt alles zusammenkommt: "
    "Skill aus Modul 5, Bot aus Modul 6, Cockpit aus Modul 9.")

# ── 9.3 Wissen hineinbringen (NEU) ───────────────────────────────────
F["l93-titel"] = lektionstitel("l93-titel", "9.3", "Dein Wissen hineinbringen",
    "Eine Seite kommt nicht an deine Dateien. Trotzdem soll sie klingen wie du.",
    "Das ist der Kniff, der deine Seiten von hübschen Seiten unterscheidet. "
    "Nimm dir Zeit dafür, auch wenn es die unscheinbarste Lektion im Modul ist.")

F["l93-luecke"] = folie("l93-luecke",
    eyebrow("Lektion 9.3")
    + h2("Das Problem")
    + p("Deine Seite läuft im Netz. Dein Business-Brief, deine Skills und deine "
        "Wissensdateien liegen auf deinem Rechner. Die Seite kommt da nicht heran — "
        "und das ist gut so.", 40)
    + p("Wenn sie dir also Vorschläge schreiben soll, die nach dir klingen, muss "
        "das Wissen zu ihr kommen.", 34, PETROL),
    "Sag ausdrücklich, dass das keine Panne ist, sondern eine Schutzmauer. "
    "Sonst klingt es nach einem Mangel, den man umgeht.")

F["l93-wie"] = folie("l93-wie",
    eyebrow("Lektion 9.3")
    + h2("Wie es trotzdem geht")
    + reihe([
        karte("1 · Sammeln", ["Ein kleines Skript liest deine echten Dateien und "
                              "schreibt daraus einen Brief."]),
        karte("2 · Ablegen", ["Claude legt den Brief im Gedächtnis der Seite ab.",
                              "Einmal, nicht bei jedem Aufruf."], ORANGE),
        karte("3 · Mitgeben", ["Die Seite liest ihn beim Öffnen und hängt ihn "
                               "an jeden Auftrag."]),
      ]),
    "Zeig den Brief einmal aufgeklappt. Dass dort deine Stimme, deine Kundschaft "
    "und deine Verbote wirklich drinstehen, macht mehr Eindruck als die Erklärung.")

F["l93-preis"] = folie("l93-preis",
    eyebrow("Lektion 9.3")
    + h2("Drei Dinge, die du wissen musst")
    + liste([
        "<b>Es ist eine Kopie, keine Verbindung.</b> Änderst du eine Quelle, muss der "
        "Brief neu geschrieben werden. Dafür ist es ein Befehl, keine Handarbeit.",
        "<b>Hänge nur an, was gebraucht wird.</b> Bei mir hat jedes Format einen eigenen "
        "Block, und mitgeschickt wird immer nur der passende.",
        "<b>Das kostet.</b> Ein langer Brief geht bei jedem Auftrag mit, also dauert es "
        "länger und wird teurer. Bewusst entscheiden, nicht alles hineinkippen.",
      ], 30),
    "Der mittlere Punkt ist der, den man erst merkt, wenn es zäh wird. "
    "Bei mir hätte sonst jeder Auftrag zehntausende Zeichen mitgeschleppt, die er nicht braucht.")

F["l93-grenze"] = folie("l93-grenze",
    eyebrow("Lektion 9.3")
    + h2("Und eine Grenze, die zählt")
    + p("Eine solche Seite kann geteilt werden. Wer den Link hat, sieht auch, was im "
        "Gedächtnis steht.", 40)
    + liste([
        "Keine fremden Namen im Brief.",
        "Keine Zugangsdaten, nie.",
        "Nichts, was du einer Kundin zugesagt hast, nur intern zu behalten.",
      ], 32),
    "Bei mir prüft das Skript das selbst und bricht ab, wenn ein Name durchrutscht. "
    "Verweis auf Modul 10 — dort kommt die ganze Regel.")

F["l93-weiter"] = weiter("l93-weiter", "Als Nächstes",
    "Der Abendlauf",
    "Ein Bot, der abends abholt, was du im Cockpit freigegeben hast.",
    "Kurze Brücke, und sag dazu, dass jetzt alles zusammenkommt: "
    "Skill aus Modul 5, Bot aus Modul 6, Cockpit aus Modul 9.")

# ── 9.4 Abendlauf ────────────────────────────────────────────────────
F["l94-titel"] = lektionstitel("l94-titel", "9.4", "Der Abendlauf",
    "Das Stück, das Cockpit und Bot verbindet.",
    "Zeig einen echten Lauf mit der Meldung, die danach bei dir ankommt. "
    "Das ist der Moment, in dem die drei Module zusammengehen.")

F["l94-ablauf"] = folie("l94-ablauf",
    eyebrow("Lektion 9.4")
    + h2("Was er tut")
    + liste([
        "<b>Er liest</b>, was im Cockpit auf freigegeben steht.",
        "<b>Er prüft</b> jeden Eintrag trocken, bevor er etwas macht.",
        "<b>Er arbeitet</b> nur das ab, was die Prüfung bestanden hat.",
        "<b>Er meldet</b> dir, was er gemacht hat und was liegengeblieben ist.",
      ], 34),
    "Der vierte Punkt ist der, den man beim Bauen weglässt und später vermisst. "
    "Ein Bot ohne Rückmeldung ist ein Bot, dem man nicht traut.")

F["l94-trocken"] = folie("l94-trocken",
    eyebrow("Lektion 9.4")
    + h2("Warum er zuerst trocken prüft")
    + p("Trocken heisst: er geht alles durch und macht noch nichts. Erst wenn "
        "alles sauber ist, läuft er richtig.", 40)
    + p("Bei mir hat das schon Einträge aufgehalten, bei denen der Zeitpunkt "
        "vorbei war oder ein Bild fehlte. Ohne die Prüfung wäre der ganze "
        "Lauf mitten drin gescheitert.", 32, GEDAEMPFT),
    "Gib ihr den Tipp mit, das bei jedem eigenen Bot so zu bauen. "
    "Erst schauen, dann tun — kostet drei Zeilen.")

F["l94-weiter"] = weiter("l94-weiter", "Als Nächstes",
    "Mehr als eine Seite",
    "Bei mir sind es zwei — und sie kommen nie aneinander heran.",
    "Kurze Brücke, und sag dazu, dass die nächste Lektion eine Aufbaustufe ist. "
    "Eine Seite reicht für den Anfang völlig.")

# ── 9.5 Mehr als eine Seite (NEU) ────────────────────────────────────
F["l95-titel"] = lektionstitel("l95-titel", "9.5", "Mehr als eine Seite",
    "Bei mir sind es zwei — und sie reden nicht miteinander.",
    "Aufbaustufe. Sag das, damit niemand denkt, sie müsse jetzt sofort eine "
    "zweite bauen. Eine reicht für den Anfang völlig.")

F["l95-teilung"] = folie("l95-teilung",
    eyebrow("Lektion 9.5")
    + h2("Warum zwei")
    + gegenueber(
        "Die eine prüft",
        ["Was diese Woche ansteht.",
         "Lesen, ändern, freigeben, einplanen.",
         "Hier hängt der Versand dran."],
        "Die andere baut",
        ["Bilder, Folien, Titelbilder.",
         "Foto wählen, Text setzen, herunterladen.",
         "Hier hängt nichts dran, was rausgeht."]),
    "Sag den Unterschied zur Doppelung: zwei Ansichten auf dieselbe Sache laufen "
    "auseinander, zwei Werkzeuge für verschiedene Arbeiten nicht.")

F["l95-tagesplan"] = folie("l95-tagesplan",
    eyebrow("Lektion 9.5")
    + h2("Was ich dabei falsch gemacht habe")
    + p("Ich hatte eine Wochen-Ansicht und eine Tages-Ansicht auf dieselben Beiträge. "
        "Beide zeigten dasselbe, nur anders sortiert.", 40)
    + p("Beim nächsten Umbau liefen sie auseinander, und ich habe jedes Mal gesucht, "
        "in welcher ich gerade stehe. Die Tages-Ansicht ist heute gestrichen.", 32, GEDAEMPFT),
    "Die Regel daraus: eine Sache, eine Ansicht. Trennen darfst du nach Arbeit, "
    "nie nach Sortierung.")

F["l95-bruecke"] = folie("l95-bruecke",
    eyebrow("Lektion 9.5")
    + h2("Die Brücke bist du")
    + p("Zwei solche Seiten kommen nie aneinander heran. Keine kann in die andere "
        "hineinschauen — auch das ist eine Schutzmauer.", 40)
    + p("Soll etwas hinüber, liest Claude es bei der einen und schreibt es bei der "
        "anderen hinein. Bei mir geht so die Wochenplanung in den Bild-Editor.", 34, PETROL),
    "Zeig das einmal an einem echten Beitrag. Dass sie im Editor unter " + zit("Aus deiner Planung")
    + " steht, ohne dass die Seiten verbunden sind, ist der Aha-Moment.")

F["l95-fallen"] = folie("l95-fallen",
    eyebrow("Lektion 9.5")
    + h2("Drei Fallen, die mich Zeit gekostet haben")
    + liste([
        "<b>Ein Knopf, der ein neues Fenster aufmacht, tut nichts.</b> Er wird blockiert, "
        "und zwar lautlos. Ein Link, den du selbst anklickst, geht durch.",
        "<b>Sicherheitsabfragen können blockiert sein.</b> Ein Löschknopf, der nichts tut, "
        "ist schlimmer als keiner — deshalb bei mir zwei Klicks statt einer Nachfrage.",
        "<b>Ein neues Feld verschwindet still</b>, wenn es beim Speichern nicht mit "
        "aufgezählt ist. Zweimal passiert, beide Male erst Wochen später gemerkt.",
      ], 29),
    "Die gemeinsame Lehre: alle drei scheitern ohne Fehlermeldung. Nach jedem Umbau "
    "einmal selbst durchklicken, nicht nur anschauen.")

F["l95-weiter"] = weiter("l95-weiter", "Als Nächstes",
    "Wenn zwei Sachen dasselbe tun",
    "Der einzige Fehler, den man nicht sieht, bevor er passiert.",
    "Mach neugierig und sag, dass du die nächste Geschichte selbst erlebt hast. "
    "Sie ist der Grund für einen Knopf, den es vorher nicht gab.")

# ── 9.6 Doppelt ──────────────────────────────────────────────────────
F["l96-titel"] = lektionstitel("l96-titel", "9.6", "Wenn zwei dasselbe tun",
    "Von Hand gepostet — und der Abendlauf hätte es nochmal gemacht.",
    "Erzähl die Geschichte ganz, mit Datum. Sie ist die beste Lektion "
    "über Automatisierung, die du hast, und sie ist dir passiert.")

F["l96-geschichte"] = folie("l96-geschichte",
    eyebrow("Lektion 9.6")
    + h2("Was passiert ist")
    + liste([
        "Ich habe ein Reel abends von Hand über die App gepostet.",
        "Im Cockpit stand die Freigabe weiter auf offen — ich hatte sie nicht angefasst.",
        "Der Abendlauf um acht hätte denselben Beitrag ein zweites Mal eingeplant.",
        "Aufgefallen ist es nur, weil ich zufällig hingeschaut habe.",
      ], 34),
    "Der letzte Punkt ist der eigentliche Schrecken. Nicht der Fehler, "
    "sondern dass ihn niemand gemeldet hätte.")

F["l96-lehre"] = statement("l96-lehre",
    ["Wenn zwei Wege zum selben Ziel führen,", "muss einer dem anderen sagen,", "dass er schon da war."],
    "Bei mir ist das heute ein Knopf: hab ich selbst gemacht.",
    "Das ist die allgemeine Regel hinter der Geschichte. Sie gilt für "
    "jede Automatisierung, die neben einem Handgriff steht.")

F["l96-regel"] = folie("l96-regel",
    eyebrow("Lektion 9.6")
    + h2("Was du daraus mitnimmst")
    + liste([
        "Überleg bei jedem Bot, was passiert, wenn du dasselbe von Hand machst.",
        "Gib ihm einen Weg, das zu erfahren — ein Feld, ein Knopf, ein Häkchen.",
        "Lass ihn melden, was er getan hat, auch wenn es nichts war.",
        "Und schau die ersten zwei Wochen jeden Tag hin.",
      ], 34),
    "Der letzte Punkt ist unbequem und trotzdem richtig. Zwei Wochen "
    "hinschauen, dann darf man loslassen.")

# ── 9.7 Zusammenfassung ──────────────────────────────────────────────
F["l97-titel"] = lektionstitel("l97-titel", "9.7", "Zusammenfassung",
    "Hier laufen Skill, Bot und deine Entscheidung zusammen.",
    "Kurz halten. Und ansagen, dass Modul 10 kein Anhang ist, sondern "
    "die Lektion, wegen der man den Kurs weiterempfiehlt.")

F["l97-bilanz"] = folie("l97-bilanz",
    eyebrow("Lektion 9.7")
    + h2("Das steht jetzt")
    + reihe([
        karte("Ein Cockpit", ["Deine eigene Seite, am Handy bedienbar."]),
        karte("Ein Gedächtnis", ["Was du entscheidest, bleibt stehen."], ORANGE),
        karte("Ein Abendlauf", ["Holt ab, was du freigegeben hast, und meldet sich."]),
      ]),
    "Sag beim mittleren, dass genau das der Unterschied zu jeder Notiz-App ist: "
    "Claude kann es lesen und danach handeln.")

F["l97-checkliste"] = checkliste("l97-checkliste", "9.7", [
    "Ich habe ein eigenes Cockpit, und sei es ein kleines",
    "Ich habe es am Handy geöffnet und benutzt",
    "Was ich abhake, ist beim nächsten Öffnen noch abgehakt",
    "Ich weiss, was passiert, wenn ich dasselbe von Hand mache",
  ], 9,
  "Der zweite Punkt ist der, den alle überspringen. Ein Cockpit, das nur "
  "am Rechner funktioniert, wird nach zwei Wochen nicht mehr geöffnet.")

F["l97-weiter"] = folie("l97-weiter",
    eyebrow("Modul 10", ORANGE)
    + ('<h2 style="font-family:%s; font-size:84px; font-weight:700; line-height:1.15; color:%s">'
       'Sicherheit, Grenzen<br>und das Ganze</h2>' % (DISPLAY, CREME))
    + p("Was nie in einen Arbeitsplatz gehört, was du verantwortest und wie bei "
        "mir eine echte Woche abläuft.", 36, PETROL),
    "Sag, dass Modul 10 kein Abspann ist. Die erste Lektion darin ist die, "
    "die in keinem anderen Kurs vorkommt.",
    stil=SEK_DUNKEL, uebergang="push")


ORDER = ["cover",
 "l91-titel","l91-was","l91-wofuer","l91-weiter",
 "l92-titel","l92-weg","l92-vorlage","l92-gedaechtnis","l92-weiter",
 "l93-titel","l93-luecke","l93-wie","l93-preis","l93-grenze","l93-weiter",
 "l94-titel","l94-ablauf","l94-trocken","l94-weiter",
 "l95-titel","l95-teilung","l95-tagesplan","l95-bruecke","l95-fallen","l95-weiter",
 "l96-titel","l96-geschichte","l96-lehre","l96-regel",
 "l97-titel","l97-bilanz","l97-checkliste","l97-weiter"]

SECTIONS = {
 "auftakt": {"description": "Worum es in Modul 9 geht.", "start": "cover"},
 "l91": {"description": "Lektion 9.1 — was ein Artifact ist.", "start": "l91-titel"},
 "l92": {"description": "Lektion 9.2 — das eigene Cockpit bauen.", "start": "l92-titel"},
 "l93": {"description": "Lektion 9.3 — wie dein Wissen in die Seite kommt.", "start": "l93-titel"},
 "l94": {"description": "Lektion 9.4 — der Abendlauf.", "start": "l94-titel"},
 "l95": {"description": "Lektion 9.5 — zwei Seiten und die Brücke dazwischen.", "start": "l95-titel"},
 "l96": {"description": "Lektion 9.6 — die Doppelpost-Geschichte und was folgt.", "start": "l96-titel"},
 "l97": {"description": "Lektion 9.7 — Bilanz und Checkliste vor Modul 10.", "start": "l97-titel"},
}

schreibe(ZIEL, "Modul 9 — Dein Cockpit", F, ORDER, SECTIONS)
