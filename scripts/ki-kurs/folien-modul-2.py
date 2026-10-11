#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Folien fuer Modul 2 — Claude Chat, die Grundlage.

    python scripts/ki-kurs/folien-modul-2.py <zielordner>
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from folien_basis import *

ZIEL = sys.argv[1] if len(sys.argv) > 1 else "folien-modul-2"
F = {}

F["cover"] = modulcover(2, "Claude Chat",
    "Du bringst der KI bei, wer du bist. Das ist der Schritt, den die meisten überspringen.",
    "Sag am Anfang, dass wir hier noch nichts installieren. Das ganze Modul läuft im ganz normalen Chat, "
    "und trotzdem ist es der wichtigste Teil des Kurses.")

# ── 2.1 Die Praktikantin ─────────────────────────────────────────────
F["l21-titel"] = lektionstitel("l21-titel", "2.1", "Die Praktikantin",
    "Warum es fast nie an der KI liegt — und was ein guter Auftrag braucht.",
    "Steig mit einer eigenen Erfahrung ein: dein erster Versuch, dir etwas schreiben zu lassen, "
    "und was dabei rauskam.")

F["l21-zutaten"] = folie("l21-zutaten",
    eyebrow("Lektion 2.1")
    + h2("Drei Zutaten, immer dieselben")
    + reihe([
        karte("Wer du bist", ["Dein Business, deine Kundschaft, dein Ton.", "Ohne das schreibt sie für irgendwen."]),
        karte("Was rauskommen soll", ["So genau wie möglich. Wie viele Sätze, welche Form, welcher Zweck."], ORANGE),
        karte("Ein Beispiel für gut", ["Ein einziges reicht. Es bringt mehr als drei Absätze Erklärung."]),
      ]),
    "Diese drei kommen im ganzen Kurs wieder. Nummeriere sie beim Sprechen laut mit, "
    "damit sie hängen bleiben.")

F["l21-vergleich"] = folie("l21-vergleich",
    eyebrow("Lektion 2.1")
    + h2("Derselbe Auftrag, zweimal")
    + gegenueber(
        "Ohne die drei Zutaten",
        ["" + zit("Schreib mir eine Caption über Selbstständigkeit.") + "",
         "Was zurückkommt, passt auf jede und klingt nach niemandem."],
        "Mit den drei Zutaten",
        ["Wer du bist. Für wen. Was am Ende dastehen soll. Ein Beispiel dazu.",
         "Was zurückkommt, musst du noch anfassen — aber du wirfst es nicht weg."]),
    "Mach das live, nicht als Folie. Zeig beide Ergebnisse nebeneinander auf dem Bildschirm. "
    "Der Unterschied überzeugt besser als jede Erklärung.")

F["l21-satz"] = statement("l21-satz",
    ["Es liegt fast nie", "an der KI.", "Es liegt am Auftrag."],
    "Eine Praktikantin, die nichts über dein Business weiss, würde dir denselben Text abliefern.",
    "Der Satz nimmt Frust raus. Viele haben KI einmal probiert, waren enttäuscht und "
    "haben es der KI angelastet.")

F["l21-weiter"] = weiter("l21-weiter", "Als Nächstes",
    "Warum deine Texte nicht nach dir klingen",
    "Es gibt ein paar Muster, an denen man KI-Text sofort erkennt. Wenn du sie einmal gesehen hast, "
    "siehst du sie überall.",
    "Kurze Brücke.")

# ── 2.2 Warum die Texte nicht klingen ────────────────────────────────
F["l22-titel"] = lektionstitel("l22-titel", "2.2", "Warum deine Texte<br>nicht nach dir klingen",
    "Die Muster, an denen man KI-Text erkennt — und was du dagegen tust.",
    "Sag, dass sie das hier nicht nur für KI-Texte brauchen kann. Es schärft auch den Blick "
    "für die eigenen Texte.", groesse=78)

F["l22-muster"] = folie("l22-muster",
    eyebrow("Lektion 2.2")
    + h2("Drei Muster, die fast immer auftauchen")
    + liste([
        "<b>Der Gegensatz nach Schema.</b> " + zit("Nicht X, sondern Y.") + " In allen Spielarten. "
        "Sprachmodelle bauen das reflexartig, weil es klug klingt und leicht zu bauen ist.",
        "<b>Drei kurze Sätze hintereinander</b> mit gleichem Anfang. Klingt nach Motivationsposter.",
        "<b>Wörter, die nach Substanz klingen und keine haben.</b> Klarer Nutzen, echte Ergebnisse, "
        "individuelle Lösung, praxisnah.",
      ], 32),
    "Lies jedes Muster einmal laut vor, so wie es klingt. Beim Vorlesen merkt man es sofort, "
    "beim stillen Lesen oft nicht.")

F["l22-korrektur"] = folie("l22-korrektur",
    eyebrow("Lektion 2.2")
    + h2("Was du stattdessen machst")
    + gegenueber(
        "Der Gegensatz nach Schema",
        ["" + zit("Du bist nicht zu leise, sondern deine Botschaft ist zu unscharf.") + ""],
        "Zwei eigene Sätze daraus",
        ["" + zit("Du bist nicht zu leise. Deine Botschaft ist zu unscharf.") + ""])
    + p("Dieselbe Aussage, nur ohne das Muster. Das ist die ganze Korrektur.", 30, GEDAEMPFT),
    "Zeig genau diesen einen Handgriff. Er reicht für die meisten Fälle, und sie kann ihn sofort anwenden.")

F["l22-warum"] = folie("l22-warum",
    eyebrow("Lektion 2.2")
    + h2("Warum das zählt")
    + p("Deine Leserin erkennt das Muster, ohne es benennen zu können. Sie liest zwei Absätze und "
        "hat das Gefühl, dass da niemand sitzt.", 38)
    + p("Bei Content, der verkaufen soll, ist das teuer. Sie klickt weiter, und du weisst nie, warum.", 34, GEDAEMPFT)
    + p("📎 Die Liste dieser Muster liegt als Vorlage unter diesem Video. Sie kommt später in "
        "deinen Arbeitsplatz, damit die KI ihren eigenen Text dagegen prüft.", 30, PETROL),
    "Der letzte Satz ist der Ausblick auf Modul 7. Nicht weiter ausführen, nur setzen.")

F["l22-weiter"] = weiter("l22-weiter", "Als Nächstes",
    "Dein Business-Brief",
    "Jetzt kommt das Dokument, das ab hier bei jedem Auftrag mitgeht.",
    "Kurze Brücke. Bau ein bisschen Spannung auf — das ist die wichtigste Lektion des Moduls.")

# ── 2.3 Business-Brief ───────────────────────────────────────────────
F["l23-titel"] = lektionstitel("l23-titel", "2.3", "Dein Business-Brief",
    "Das eine Dokument, das ab jetzt bei jedem Auftrag mitgeht.",
    "Sag klar: Wenn sie aus diesem ganzen Modul nur eine Sache macht, dann diese.")

F["l23-bausteine-a"] = folie("l23-bausteine-a",
    eyebrow("Die sechs Bausteine · 1 bis 3")
    + h2("Wer, für wen, was")
    + reihe([
        karte("1 · Wer ich bin", ["Was du machst, seit wann.", "Und wie eine Freundin dich vorstellen würde."]),
        karte("2 · Für wen ich da bin", ["Nicht " + zit("alle") + ". In welcher Lage diese Person steckt und was sie nachts denkt."], ORANGE),
        karte("3 · Was ich anbiete", ["Jedes Angebot mit dem einen Ergebnis, das sie danach hat."]),
      ]),
    "Bei Baustein 2 ausdrücklich sagen, dass " + zit("Mamas") + " nicht reicht. Das ist der Fehler, "
    "den fast alle machen.")

F["l23-bausteine-b"] = folie("l23-bausteine-b",
    eyebrow("Die sechs Bausteine · 4 bis 6")
    + h2("Themen, Ton, Tabus")
    + reihe([
        karte("4 · Meine Themen", ["Worüber du sprichst — und ausdrücklich auch, worüber nicht."]),
        karte("5 · Wie ich klinge", ["Deine Wörter, deine Satzlänge, dein Ton.", "Plus zwei, drei eigene Textproben."], ORANGE),
        karte("6 · Meine Tabus", ["Was bei dir nie vorkommt.", "Im Network gehören die Regeln deines Partners hierher."]),
      ]),
    "Baustein 5 ist der, der den Unterschied macht. Baustein 6 wird unterschätzt und "
    "spart dir später Ärger — Modul 10 kommt darauf zurück.")

F["l23-satz"] = statement("l23-satz",
    ["Könnte jemand,", "der dich nicht kennt,", "damit einen Text schreiben,", "den deine Kundschaft", "für deinen hält?"],
    "Wenn nein, fehlt Baustein 5.",
    "Das ist die Prüffrage am Ende. Lass sie stehen und sprich erst weiter, wenn sie gelesen ist.",
    zusatz="📎 Die Vorlage mit allen sechs Bausteinen liegt unter diesem Video.")

F["l23-weiter"] = weiter("l23-weiter", "Als Nächstes",
    "Die Buch-Technik",
    "Falls du jetzt vor einem leeren Dokument sitzt: In der nächsten Lektion lässt du die KI fragen, "
    "statt selbst zu formulieren.",
    "Nimm den Einwand vorweg, den sie gerade hat.")

# ── 2.4 Buch-Technik ─────────────────────────────────────────────────
F["l24-titel"] = lektionstitel("l24-titel", "2.4", "Die Buch-Technik",
    "Lass die KI fragen, statt vor dem leeren Blatt zu sitzen.",
    "Sag ehrlich, dass du selbst so angefangen hast. Das leere Dokument bremst mehr Frauen "
    "als alles Technische.")

F["l24-wie"] = folie("l24-wie",
    eyebrow("Lektion 2.4")
    + h2("So läuft es ab")
    + liste([
        "Du sagst der KI, sie schreibe ein Buch über dich und wolle dich vorher richtig kennen.",
        "Sie stellt Fragen. <b>Eine nach der anderen</b>, nicht alle auf einmal.",
        "Du antwortest in ganzen Sätzen, so wie du reden würdest.",
        "Nach mindestens drei Runden lässt du sie daraus dein Wissensdokument schreiben.",
      ], 34),
    "Zeig das live. Lass sie wirklich drei Runden fragen und antworte selbst — "
    "das ist überzeugender als der Prompt allein.")

F["l24-offen"] = folie("l24-offen",
    eyebrow("Lektion 2.4")
    + h2("Der Kniff am Schluss")
    + p("Sag ihr: <b>Wo du etwas nicht weisst, schreib " + zit("offen") + " hin statt etwas zu erfinden.</b>", 40)
    + p("Damit bekommst du zwei Sachen auf einmal: ein Dokument, in dem nichts Erfundenes steht, "
        "und eine Liste mit genau den Stellen, über die du noch nachdenken musst.", 34, GEDAEMPFT)
    + p("📎 Den ganzen Auftrag zum Kopieren findest du unter diesem Video.", 30, PETROL),
    "Das ist der Teil, den kaum jemand macht. Betone ihn — er verhindert, dass sie mit einem "
    "hübschen, aber falschen Dokument weitergeht.")

F["l24-weiter"] = weiter("l24-weiter", "Als Nächstes",
    "Deine Stimme einfangen",
    "Zwei, drei eigene Texte reichen, damit die KI deinen Ton trifft.",
    "Kurze Brücke.")

# ── 2.5 Stimme ───────────────────────────────────────────────────────
F["l25-titel"] = lektionstitel("l25-titel", "2.5", "Deine Stimme einfangen",
    "Warum zwei, drei eigene Texte mehr bringen als jede Beschreibung.",
    "Sag, dass " + zit("schreib locker und nahbar") + " nichts bewirkt. Das schreibt jede in ihren Prompt.")

F["l25-proben"] = folie("l25-proben",
    eyebrow("Lektion 2.5")
    + h2("Was du anhängst")
    + liste([
        "<b>Eine Caption</b>, die du selbst geschrieben hast und gut findest.",
        "<b>Eine Mail</b> an deine Liste oder an eine Kundin.",
        "<b>Irgendetwas Längeres</b> — ein Blogtext, ein Beitrag, eine Sprachnachricht abgetippt.",
      ], 34)
    + p("Wichtig ist nur, dass es wirklich von dir ist. Ein Text, den dir jemand anders geschrieben hat, "
        "bringt dir die Stimme von jemand anderem zurück.", 32, GEDAEMPFT),
    "Der letzte Satz klingt banal und passiert ständig. Viele hängen einen Text an, den eine "
    "Agentur oder eine Vorlage geliefert hat.")

F["l25-merken"] = folie("l25-merken",
    eyebrow("Lektion 2.5")
    + h2("Woran du merkst, dass es sitzt")
    + gegenueber(
        "Klingt noch nicht",
        ["Du liest den Text und denkst: stimmt schon alles.",
         "Du baust trotzdem jeden zweiten Satz um."],
        "Sitzt",
        ["Du liest den Text und hörst dich selbst.",
         "Du änderst noch ein, zwei Stellen — und schickst ihn ab."]),
    "Die rechte Spalte ist das realistische Ziel. Nicht versprechen, dass sie nie wieder etwas ändert.")

F["l25-weiter"] = weiter("l25-weiter", "Als Nächstes",
    "Projekte statt Einzelchats",
    "Damit dein Wissen liegen bleibt, statt dass du es in jedem neuen Gespräch wieder eintippst.",
    "Kurze Brücke.")

# ── 2.6 Projekte ─────────────────────────────────────────────────────
F["l26-titel"] = lektionstitel("l26-titel", "2.6", "Projekte statt Einzelchats",
    "Einmal eingerichtet, und du fängst nicht mehr bei null an.",
    "Frag sie, wie oft sie schon denselben Absatz über ihr Business in einen Chat getippt hat. "
    "Das ist der Schmerz, den diese Lektion löst.")

F["l26-was"] = folie("l26-was",
    eyebrow("Lektion 2.6")
    + h2("Was in dein Projekt gehört")
    + liste([
        "<b>Dein Business-Brief</b> — der aus Lektion 2.3.",
        "<b>Deine Textproben</b> — die aus Lektion 2.5.",
        "<b>Deine Angebote</b> mit Preisen und Links, falls du sie oft brauchst.",
        "<b>Was nicht hineingehört:</b> Zugangsdaten und alles, was Daten anderer Menschen enthält.",
      ], 34),
    "Der letzte Punkt kommt in Modul 10 ausführlich. Hier reicht ein Satz, damit sie es "
    "von Anfang an richtig macht.")

F["l26-satz"] = statement("l26-satz",
    ["Ab jetzt weiss sie,", "wer du bist —", "in jedem Gespräch."],
    "Du erklärst es einmal. Danach weiss sie es.",
    "Das ist der Moment, an dem die Arbeit aus Modul 2 sich auszahlt. Lass ihn wirken.")

# ── 2.7 Zusammenfassung ──────────────────────────────────────────────
F["l27-titel"] = lektionstitel("l27-titel", "2.7", "Zusammenfassung",
    "Was jetzt bei dir steht — und was stehen muss, bevor du weitergehst.",
    "Kurze Lektion. Nicht alles nochmal erzählen.")

F["l27-bilanz"] = folie("l27-bilanz",
    eyebrow("Lektion 2.7")
    + h2("Das nimmst du mit")
    + reihe([
        karte("Dein Business-Brief", ["Sechs Bausteine, ausgefüllt.", "Mit Textproben dran."]),
        karte("Dein Projekt", ["Dein Wissen liegt dort und geht bei jedem Auftrag mit."], ORANGE),
        karte("Dein Blick", ["Du erkennst KI-Muster im Text — auch in deinen eigenen."]),
      ]),
    "Geh die drei durch und frag nach jeder: Ist das bei dir wirklich schon so?")

F["l27-checkliste"] = checkliste("l27-checkliste", "2.7", [
    "Ich habe einen Auftrag geschrieben, der alle drei Zutaten enthält",
    "Mein Business-Brief ist ausgefüllt — alle sechs Bausteine",
    "Zwei bis drei eigene Textproben hängen dran",
    "Ich habe ein Projekt angelegt und den Business-Brief hineingelegt",
    "Ich habe einen Text erzeugt, den ich so verwenden würde",
  ], 2,
  "Bitte sie ausdrücklich, den Business-Brief jetzt fertigzumachen. Alles ab Modul 4 baut darauf auf, "
  "und mit einem halben Brief wird der ganze Rest halb.")

F["l27-weiter"] = folie("l27-weiter",
    eyebrow("Modul 3", ORANGE)
    + ('<h2 style="font-family:%s; font-size:84px; font-weight:700; line-height:1.15; color:%s">'
       'Claude Cowork —<br>die Mittelstufe</h2>' % (DISPLAY, CREME))
    + p("Jetzt arbeitet die KI mit deinen Dateien und hängt an deiner eigenen Planung. "
        "Und du baust deinen ersten Bot, ohne eine Zeile Code.", 36, PETROL),
    "Mach neugierig auf den Bot. Das ist für die meisten der Punkt, an dem es konkret wird.",
    stil=SEK_DUNKEL, uebergang="push")


ORDER = ["cover",
 "l21-titel","l21-zutaten","l21-vergleich","l21-satz","l21-weiter",
 "l22-titel","l22-muster","l22-korrektur","l22-warum","l22-weiter",
 "l23-titel","l23-bausteine-a","l23-bausteine-b","l23-satz","l23-weiter",
 "l24-titel","l24-wie","l24-offen","l24-weiter",
 "l25-titel","l25-proben","l25-merken","l25-weiter",
 "l26-titel","l26-was","l26-satz",
 "l27-titel","l27-bilanz","l27-checkliste","l27-weiter"]

SECTIONS = {
 "auftakt": {"description": "Worum es in Modul 2 geht.", "start": "cover"},
 "l21": {"description": "Lektion 2.1 — die drei Zutaten eines guten Auftrags.", "start": "l21-titel"},
 "l22": {"description": "Lektion 2.2 — woran man KI-Text erkennt.", "start": "l22-titel"},
 "l23": {"description": "Lektion 2.3 — der Business-Brief in sechs Bausteinen.", "start": "l23-titel"},
 "l24": {"description": "Lektion 2.4 — die Buch-Technik zum Ausfüllen.", "start": "l24-titel"},
 "l25": {"description": "Lektion 2.5 — die eigene Stimme einfangen.", "start": "l25-titel"},
 "l26": {"description": "Lektion 2.6 — Projekte statt Einzelchats.", "start": "l26-titel"},
 "l27": {"description": "Lektion 2.7 — Bilanz und Checkliste vor Modul 3.", "start": "l27-titel"},
}

schreibe(ZIEL, "Modul 2 — Claude Chat", F, ORDER, SECTIONS)
