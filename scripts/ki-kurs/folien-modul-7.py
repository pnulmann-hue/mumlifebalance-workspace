#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Folien für Modul 7 — Social Media mit Claude Code.

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

# 🚨 Am 04.11.2026 dazu. Patricia: „bei Reels habe ich ja die regel, dass er aus
#    meinem context ordner Videos holt … das kann ich beim einrichten ja nicht
#    zeigen, weil ich das alles schon habe. aber ich muss erklären was die
#    schritte sind, damit sie dahin kommen."
#    Dieselbe Lage wie der Botvater in 6.3: zeigen geht nicht, erklären schon.
# 🚨 Die Pfade stimmen so (nachgesehen in scripts/handy/hol-content.py):
#    Videos nach video/input/, Fotos nach context/content-assets/inbox/,
#    je Video ein Standbild nach context/content-assets/vorschau/.
F["l71-material"] = folie("l71-material",
    eyebrow("Lektion 7.1")
    + h2("Und wo dein Material liegt")
    + liste([
        "<b>Ein Album auf dem Handy.</b> Da wirfst du rein, was du verwenden willst — mehr sortierst du nie.",
        "<b>Ein Befehl holt es ab</b> und legt Videos und Fotos an ihren Platz.",
        "<b>Von jedem Video zieht sie ein Standbild.</b> Sie kann kein Video anschauen — aber ein Bild schon.",
      ], 30)
    + p("Der dritte Punkt ist der, an dem es bei mir vorher gehakt hat. Ohne "
        "Standbild rät sie aus dem Dateinamen, was auf dem Clip ist.", 28, PETROL),
    "🚨 Das kannst du nicht live einrichten — bei dir steht es seit einem Jahr. "
    "Zeig stattdessen dein Album am Handy und daneben den vollen Ordner, und "
    "sag die drei Schritte dazu. Die Anleitung liegt unter dem Video.")

F["l71-weiter"] = weiter("l71-weiter", "Als Nächstes",
    "Caption und Story",
    "Und die Demonstration, die den Unterschied sichtbar macht.",
    "Kündige an, dass in der nächsten Lektion derselbe Skill zweimal läuft — "
    "einmal leer, einmal gefüllt.")

# ── 7.1b Wie du die Dateien füllst ──────────────────────────────────
# 🚨 Neu am 04.11.2026, auf Patricias Wunsch: „ich will ihnen so auch einen
#    trick geben wie sie karussells, reels, storys, captions so lernen können
#    zu füllen." Als 7.1b und nicht als neue Nummer, damit 7.2 bis 7.8 bleiben
#    wie sie sind — das `b` gibt es im Kurs schon (2.3b).
# 🚨 Abgrenzung zu 7.1: dort steht „was inhaltlich hineingehört, ist ein Thema
#    für sich" und verweist auf die Instagram-Kundenmaschine. Hier geht es um
#    den HANDGRIFF, mit dem sie sich ihre eigenen Regeln holt — nicht darum,
#    was guten Content ausmacht. Die zwei müssen sauber getrennt bleiben,
#    sonst verkauft diese Lektion das andere Angebot weg.
F["l71b-titel"] = lektionstitel("l71b-titel", "7.1b", "Wie du die Dateien füllst",
    "Du hast das Material schon. Du hast es nur nie ausgewertet.",
    "Die Lektion, auf die sie gewartet haben. Alle sitzen irgendwann vor einer "
    "leeren Datei und wissen nicht, was hineingehört — hier kommt die Antwort.")

F["l71b-zweiwege"] = folie("l71b-zweiwege",
    eyebrow("Lektion 7.1b")
    + h2("Zwei Wege, und einer kommt zuerst")
    + gegenueber(
        "1 · Deine eigenen Beiträge",
        ["Fünf, die gut gelaufen sind.",
         "Die mit Reaktionen, nicht die schönsten.",
         "Ergebnis: deine eigene Handschrift, zum ersten Mal aufgeschrieben."],
        "2 · Beiträge von anderen",
        ["Wenn du denkst: so hätte ich das auch gern.",
         "Gut für Formate, die du noch nie gemacht hast.",
         "Ergebnis: eine Bauweise, die du noch nicht kanntest."]),
    "Bestehe auf der Reihenfolge. Wer mit fremden Beiträgen anfängt, baut sich "
    "eine Stimme zusammen, die ihr nicht gehört — und merkt es erst in drei "
    "Monaten.")

F["l71b-auftrag"] = folie("l71b-auftrag",
    eyebrow("Lektion 7.1b")
    + h2("Das sagst du")
    + ('<div style="background:#fdfcf8; padding:40px 44px; border-radius:18px; '
       'border-left:8px solid #12828c; display:flex; flex-direction:column; gap:18px">'
       '<p style="font-size:31px; line-height:1.5; color:#0c1c30">'
       'Hier sind fünf Beiträge von mir, die gut gelaufen sind. Sag mir, was '
       'sie gemeinsam haben — wie die erste Zeile gebaut ist, wie lang sie '
       'sind, wie sie aufhören, wie ich klinge.</p>'
       '<p style="font-size:31px; line-height:1.5; color:#0c1c30">'
       'Schreib mir daraus <b>Regeln</b> und trag sie in meinen '
       '<b>caption</b>-Skill ein.</p></div>')
    + p("Die Beiträge ziehst du als Bildschirmfotos in den Chat. Schneller geht "
        "es mit der Browser-Erweiterung — die zeige ich dir gleich.", 28, PETROL),
    "Zeig beides: erst Screenshots, weil das jede kann und nichts braucht. Dann "
    "die Erweiterung als Komfort. Sag ehrlich dazu, dass das die einzige Stelle "
    "im Kurs ist, an der sie etwas zusätzlich installiert — und dass sie es "
    "nicht muss.")

F["l71b-grenze"] = folie("l71b-grenze",
    eyebrow("Lektion 7.1b")
    + h2("Die Bauweise ja. Die Sätze nie.")
    + gegenueber(
        "Das darfst du mitnehmen",
        ["Wie viele Folien.",
         "Wo der Aufruf steht.",
         "Dass Folie 1 eine Frage ist.",
         "Handgriffe gehören niemandem."],
        "Das nicht",
        ["Ganze Sätze.",
         "Formulierungen, die dir aufgefallen sind.",
         "Geborgte Sätze klingen nach jemand anderem.",
         "Und genau davon wolltest du ja weg."]),
    "Der letzte Punkt rechts ist das Argument, das zieht — nicht die Moral. "
    "Sag dazu: wenn du in derselben Nische abschaust, klingen am Ende alle "
    "gleich, und dann gibt es keinen Grund mehr, ausgerechnet dich zu lesen.")

F["l71b-weiter"] = weiter("l71b-weiter", "Als Nächstes",
    "Caption und Story",
    "Jetzt, wo die Dateien etwas enthalten, sieht man den Unterschied.",
    "Guter Übergang: in der nächsten Lektion läuft derselbe Skill zweimal, "
    "einmal leer und einmal gefüllt. Genau das haben sie gerade gebaut.")

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

# ── 7.2b Woher die Themen kommen ─────────────────────────────────────
# 🚨 Patricias Ablauf, nicht der übliche. Der Unterschied ist die
#    Beweispflicht: gemessen statt behauptet.
F["l72b-titel"] = lektionstitel("l72b-titel", "7.2b", "Woher die Themen kommen",
    "Die Maschine ist gebaut. Jetzt die Frage, worüber sie schreibt.",
    "Diese Lektion entscheidet über alles, was danach kommt. Eine gute "
    "Maschine mit schlechten Themen macht schnell viel Mittelmass.")

F["l72b-gemessen"] = folie("l72b-gemessen",
    eyebrow("Lektion 7.2b")
    + h2("Zwei Arten von „Trend“")
    + gegenueber(
        "Behauptet",
        ["„Laut Recherche ist X gerade gross.“",
         "Steht in einem Artikel.",
         "Darauf hat nie jemand reagiert."],
        "Gemessen",
        ["Ein Beitrag mit 300 Kommentaren.",
         "Und die Kommentare darunter.",
         "Da hat sich jemand wirklich geäussert."])
    + p("Beides heisst Trend. Nur das Zweite ist ein Beleg — und die Kommentare "
        "darunter sind echte Sätze von echten Leuten.", 28, PETROL),
    "Das ist der Kern der Lektion. Sag ausdrücklich, dass du nichts gegen "
    "Trends hast — im Gegenteil. Du willst nur die, bei denen man die Reaktion "
    "sehen kann.")

F["l72b-vier"] = folie("l72b-vier",
    eyebrow("Lektion 7.2b")
    + h2("Vier Dinge statt „Themen“")
    + liste([
        "<b>Schmerz</b> — was ihnen gerade wirklich wehtut.",
        "<b>Wunsch</b> — wie es stattdessen sein soll.",
        "<b>Ziel</b> — wohin sie eigentlich wollen.",
        "<b>Was scheitert</b> — was sie schon probiert haben, ohne Erfolg.",
      ], 32)
    + p("Je drei bis fünf. Danach hast du keine Themenliste, sondern Sätze, "
        "auf die du antworten kannst.", 28, GEDAEMPFT),
    "Der letzte Punkt ist der, den alle vergessen — und der beste. Wer weiss, "
    "was schon gescheitert ist, kann den Beitrag schreiben, auf den sie warten.")

F["l72b-prompt"] = folie("l72b-prompt",
    eyebrow("Lektion 7.2b")
    + h2("Das sagst du")
    + auftrag([
        "Bau mir einen Auftrag, der jeden <i>[Tag]</i> die Themen für meine "
        "Woche sucht.",
        "Such vier Dinge, je drei bis fünf, für <b>meine</b> Leute: Schmerz · "
        "Wunsch · Ziel · was bei ihnen immer wieder scheitert.",
        "Wo du suchst, in dieser Reihenfolge: in den Kommentaren unter den "
        "Beiträgen von <i>[Konto]</i> · in <i>[Foren, Gruppen]</i> · in meinen "
        "eigenen Nachrichten der letzten sieben Tage · erst dann im Netz.",
        "<b>Jeder Punkt braucht ein echtes Zitat mit Fundort.</b> Findest du "
        "keins, lässt du ihn weg.",
        "Frag nach, wenn dir eine Angabe fehlt.",
      ], 31, 17),
    "Tipp den Auftrag ein, nicht einfügen. Der vierte Block ist der, der "
    "diesen Auftrag von jedem anderen unterscheidet — betone ihn.")

F["l72b-beleg"] = folie("l72b-beleg",
    eyebrow("Lektion 7.2b")
    + h2("Warum ich darauf bestehe")
    + p("Bei mir hat ein Bericht <b>25 Wochen lang</b> jede Woche Schmerzpunkte "
        "gemeldet — und dabei <b>null Beiträge gelesen</b>.", 38, BLAU)
    + liste([
        "Die Berichte sahen gut aus. Die Sätze klangen echt.",
        "Es stand sogar eine Quelle dabei — nur nie eine Fundstelle.",
        "Aufgefallen ist es durch <b>Zufall</b>. Gesucht hat es niemand.",
      ], 29)
    + p("Darum: Zitat mit Fundort, sonst fällt der Punkt raus. Lieber drei "
        "belegte als zehn erfundene.", 28, PETROL),
    "Erzähl das als eigene Geschichte, nicht als Warnung. Es ist die "
    "überzeugendste Stelle der Lektion, weil es dir selbst passiert ist — "
    "und weil niemand danach gesucht hat. Genau das ist der Punkt: man "
    "sieht es einem Bericht nicht an.")

F["l72b-eigen"] = folie("l72b-eigen",
    eyebrow("Lektion 7.2b")
    + h2("Und dann schaust du auf dich")
    + liste([
        "<b>Welche deiner Beiträge</b> liefen besser als deine üblichen?",
        "<b>Was haben die gemeinsam</b> — Thema, erste Zeile, Format?",
        "<b>Immer gegen deinen eigenen Schnitt</b>, nie gegen fremde Zahlen.",
      ], 32)
    + p("Ein grosses Konto hat mit einem schwachen Beitrag mehr Reichweite als "
        "du mit deinem besten. Darum zählt nur dein eigener Vergleich.", 28, GEDAEMPFT),
    "Das ist der Punkt, an dem viele aufgeben, weil sie sich mit Grossen "
    "vergleichen. Sag klar: die einzige Zahl, die zählt, ist dein eigener "
    "Durchschnitt.")

F["l72b-weiter"] = weiter("l72b-weiter", "Als Nächstes",
    "Karussell — vom Text zum Bild",
    "Du hast die Themen. Jetzt wird daraus etwas, das man sieht.",
    "Überleitung kurz halten.")

# ── 7.3 Karussell ────────────────────────────────────────────────────
# ── 7.2c Die Verbindungen ────────────────────────────────
# 🚨 Diese Lektion fehlte. Ab 7.3 setzt das Modul drei Dinge voraus, die
#    vorher niemand erklaert hat. Bewusst kurz: vier Handgriffe, kein Vortrag.
F["l72c-titel"] = lektionstitel("l72c-titel", "7.2c", "Die Verbindungen",
    "Vier Handgriffe, einmal. Danach nie wieder.",
    "Die unspektakulärste Lektion des Moduls — und die, ohne die nichts "
    "Folgende funktioniert. Halt sie kurz und mach sie wirklich vor.")

F["l72c-was"] = folie("l72c-was",
    eyebrow("Lektion 7.2c")
    + h2("Was jetzt dazukommt")
    + liste([
        "<b>Canva anschliessen</b> — damit sie deine Designs sieht und bauen darf.",
        "<b>Den Posting-Dienst anschliessen</b> — damit überhaupt etwas rausgehen kann.",
        "<b>Eine geplante Aufgabe anlegen</b> — damit es ohne dich läuft.",
        "<b>Den ersten Lauf von Hand starten</b> — einmal, wegen der Nachfragen.",
      ], 32)
    + p("Alles vier machst du einmal. Danach kommt keiner dieser Schritte "
        "jemals wieder.", 28, PETROL),
    "Sag den letzten Satz wirklich. Die meisten steigen hier aus, weil es nach "
    "Technik aussieht — dabei sind es vier Klicks, die nie wiederkommen.")

F["l72c-canva"] = folie("l72c-canva",
    eyebrow("Lektion 7.2c · Handgriff 1 und 2")
    + h2("Anschliessen — zweimal verschieden")
    + gegenueber(
        "Canva",
        ["In den Einstellungen unter den Verbindungen.",
         "Einmal anmelden, fertig.",
         "Kein Schlüssel, kein Code."],
        "Der Posting-Dienst",
        ["Dort einen Schlüssel holen.",
         "Den gibst du einmal weiter.",
         "Instagram verbindest du <b>dort</b>, nicht hier."])
    + p("🚨 Der Schlüssel gehört in die Datei daneben, <b>nie in den Chat</b>. "
        "Was im Verlauf steht, steht für immer im Verlauf.", 28, PETROL),
    "Zeig beides auf dem Bildschirm. Der rote Hinweis ist eine eigene kleine "
    "Lektion — und sie gilt für jeden Schlüssel, den sie je bekommt.")

F["l72c-aufgabe"] = folie("l72c-aufgabe",
    eyebrow("Lektion 7.2c · Handgriff 3")
    + h2("Was eine geplante Aufgabe ist")
    + liste([
        "Ein Auftrag, den sie <b>von selbst</b> ausführt — täglich, wöchentlich, wie du willst.",
        "Du legst sie nicht selbst an: <b>du sagst, was passieren soll</b>, und sie richtet es ein.",
        "Du findest sie danach in der Seitenleiste und kannst sie jederzeit anhalten.",
      ], 30)
    + p("🚨 Läuft sie auf deinem Rechner, läuft sie nur, solange die App "
        "offen ist. Soll sie immer laufen, wohnt sie im Netz — wie dein Bot aus "
        "Modul 6.", 28, GEDAEMPFT),
    "Hier schliesst sich der Bogen zu 6.4. Sag ausdrücklich, dass sie keine "
    "Technik anlegt, sondern beschreibt — genau wie beim Bot.")

F["l72c-erster"] = folie("l72c-erster",
    eyebrow("Lektion 7.2c · Handgriff 4")
    + h2("Den ersten Lauf startest du selbst")
    + p("Beim ersten Mal fragt sie nach Erlaubnis — darf ich Canva lesen, darf "
        "ich etwas einplanen. Diese Fragen musst du einmal beantworten.", 34, BLAU)
    + liste([
        "Aufgabe suchen, <b>einmal von Hand starten</b>, alle Nachfragen durchklicken.",
        "Danach läuft sie allein.",
        "Am nächsten Tag <b>nachschauen</b>, ob wirklich etwas passiert ist.",
      ], 29)
    + p("Ohne das steht sie jeden Abend still — und meldet trotzdem, dass alles "
        "gut gelaufen sei.", 28, PETROL),
    "Das ist der häufigste Grund, warum so etwas scheinbar läuft und doch "
    "nichts tut. Mir ist genau das passiert, sechs Tage lang. Erzähl es.")

F["l72c-weiter"] = weiter("l72c-weiter", "Als Nächstes",
    "Karussell — vom Text zum Bild",
    "Die Verbindungen stehen. Jetzt wird wirklich gebaut.",
    "Kurz überleiten.")

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

# 🚨 Am 04.11.2026 dazu, auf Patricias Wunsch: „ich möchte beide varianten
#    zeigen." Canva ist der Weg, den jede sofort gehen kann — sie hat Canva
#    schon und muss nichts bauen. Der eigene Editor ist der Weg für später.
#    Patricia hat beide selbst benutzt; den Canva-Weg früher, bevor sie auf
#    den eigenen Editor umgestiegen ist.
F["l73-zweiwege"] = folie("l73-zweiwege",
    eyebrow("Lektion 7.3")
    + h2("Für die Bilder gibt es zwei Wege")
    + gegenueber(
        # 🚨 Drei Zeilen je Spalte, nicht mehr. Mit vier war die Folie 1244
        #    statt 1080 hoch und unten abgeschnitten (gemessen 04.11.2026).
        "Über Canva",
        ["Du hast es schon und musst nichts bauen.",
         "Deine Vorlage mit deinen Schriften — sie füllt nur.",
         "Der Weg, mit dem du anfängst."],
        "Über einen eigenen Editor",
        ["Du baust ihn selbst — das kommt in Modul 9.",
         "Dafür sitzt jede Folie auf den Punkt gleich.",
         "Der Weg, auf den du später umsteigst."]),
    # 🚨 Hier stand eine vierte Zeile „Dasselbe gilt für Storys und
    #    Reel-Titelbilder." — damit war die Folie 1130 statt 1080 hoch. Der
    #    Satz steht jetzt in der Sprechnotiz und im Lektionstext, wo er
    #    nichts verdrängt.
    "Sag ehrlich, dass du selbst beide gegangen bist — erst Canva, dann der "
    "eigene Editor. Und warum du gewechselt hast. Das nimmt dem zweiten Weg "
    "das Elitäre und dem ersten das Billige. "
    "🚨 Und sag dazu: dasselbe gilt für Storys und Reel-Titelbilder — "
    "entweder eine Vorlage je Art in Canva, oder etwas Eigenes, das die "
    "Folie zeichnet. Sonst fragen sie genau das in der Gruppe.")

F["l73-canva"] = folie("l73-canva",
    eyebrow("Lektion 7.3 · Weg 1")
    + h2("So läuft es über Canva")
    + liste([
        "<b>Du baust ein Muster-Karussell</b> in Canva, von Hand, wie immer.",
        "<b>Du gibst Claude den Link dazu.</b> Sie schaut es sich an und baut danach.",
        "<b>Drei Ordner:</b> fertig · zum Posten · gepostet. Nichts geht zweimal raus.",
        "<b>Die Caption</b> hängst du als Kommentar ans Design.",
      ], 30)
    + p("🚨 Beim ersten Mal legt sie gern eine Seite statt eines Karussells an. "
        "Dann sagst du einfach, wie viele Seiten du willst.", 28, PETROL),
    "Zeig deine eigene Vorlage. Und sag dazu, dass sie die Schriften NICHT "
    "selbst setzen kann — darum baust du die Vorlage von Hand und sie füllt "
    "nur. Genau daran bin ich früher gescheitert, als ich es umgekehrt "
    "versucht habe.")

# 🚨 Am 04.11.2026 dazu, auf Patricias Wunsch: „das gilt z.B. auch für die
#    karussells. eine schritt für schritt anleitung was sie zu tun hat und was
#    sie claude code geben muss." Der Prompt steht hier und im Lektionstext, die
#    Schritte in der Anleitung unter dem Video — derselbe Bau wie 6.3.
F["l73-prompt"] = folie("l73-prompt",
    eyebrow("Lektion 7.3 · Weg 1")
    + h2("Das sagst du")
    + auftrag([
        "In Canva liegt mein Muster-Karussell: <i>[Link]</i>. Schau dir "
        "Schriften, Farben und den Aufbau an.",
        "Damit baust du die Folien, die mein <b>Karussell-Auftrag</b> "
        "geschrieben hat — gleiche Schriften, gleiche Farben, <i>[Zahl]</i> Seiten.",
        "Leg mir die Folientexte <b>zuerst als Text</b> vor. Erst wenn ich sie "
        "freigebe, füllst du die Vorlage.",
        "Das fertige Design kommt in den Ordner <b>Zum Posten</b>, die Caption "
        "hängst du als <b>Kommentar</b> ans Design.",
        "<b>Ergänz das in meinem Karussell-Auftrag</b>, damit du es ab jetzt "
        "immer so machst. Frag nach, wenn dir eine Angabe fehlt.",
      ], 31, 17),
    "Der zweite Block ist die Brücke zu 7.1 — ohne ihn denkt sie sich die "
    "Folientexte neu aus, und das ganze Wissen aus den Dateien bleibt liegen. "
    "Der letzte macht aus einmal bauen eine Routine. Wortlaut steht unter dem "
    "Video.")

F["l73-stammvorlage"] = folie("l73-stammvorlage",
    eyebrow("Lektion 7.3 · der wichtigste Satz")
    + h2("Deine Vorlage wird nie überschrieben")
    + liste([
        "Claude kann ein Canva-Design <b>nicht kopieren</b> — dafür gibt es kein Werkzeug.",
        "Es geht trotzdem, über einen Umweg. Den Namen dafür findest du in der Anleitung.",
        "<b>Sag ihr einmal</b>, dass die Vorlage immer geklont wird und selbst unangetastet bleibt.",
        "Und schreib denselben Satz in deine <b>Gedächtnis-Datei</b> — dann weiss jede neue Sitzung Bescheid.",
      ], 29)
    + p("Ohne diesen Satz passiert eins von zwei Dingen: sie sagt „das kann ich "
        "nicht“, oder sie überschreibt dein Original.", 28, PETROL),
    "Hier schliesst sich der Kreis zu Lektion 4.4. Sag das ausdrücklich: Das "
    "ist der Moment, in dem man zum ersten Mal merkt, wofür die "
    "Gedächtnis-Datei gut ist — ein Satz dort, und das Thema ist für immer "
    "erledigt.")

F["l73-editor"] = folie("l73-editor",
    eyebrow("Lektion 7.3 · Weg 2")
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

# 🚨 Am 04.11.2026 dazu, auf Patricias Wunsch: „ich will jetzt nicht alles bis
#    ins detail erklären. aber halt einfach, dass es grundsätzlich möglich ist.
#    dass er über capcut schneiden kann." Darum zwei Folien und nicht sechs:
#    was danach noch geht, und wie sie ihren Stil beibringt.
F["l74-mehr"] = folie("l74-mehr",
    eyebrow("Lektion 7.4")
    + h2("Und danach geht noch mehr")
    + liste([
        "<b>Untertitel</b>, Wort für Wort mitlaufend — nicht als Block, sondern mitgesprochen.",
        "<b>Zoom-Fahrten</b>, damit ein Sprechvideo nicht steht.",
        "<b>Text im Bild</b>, der auf dem gesprochenen Wort erscheint.",
        "<b>Animationen</b> — und zwar in deinem Stil, nicht im Vorlagen-Stil.",
      ], 30)
    + p("Das zeige ich hier nicht Schritt für Schritt. Du sollst nur wissen, "
        "dass es geht, und dass du es nicht von Hand machen musst.", 28, GEDAEMPFT),
    "Zeig ein fertiges Beispiel und lass es laufen. Mehr nicht. Wer hier "
    "jeden Handgriff sehen will, fragt danach — und dann hast du die "
    "Anleitung unter dem Video.")

F["l74-vorbild"] = folie("l74-vorbild",
    eyebrow("Lektion 7.4")
    + h2("Wie sie deinen Stil lernt")
    + liste([
        "<b>Du suchst drei bis fünf Videos</b>, deren Machart dir gefällt.",
        "<b>Sie zieht die Bauweise heraus</b> — Schnitttempo, wo Text steht, wie lang eine Einstellung bleibt.",
        "<b>Daraus werden Regeln</b>, und ab dann baut sie so.",
        "<b>Den Feinschnitt ziehst du selbst</b> — in CapCut, mit der Maus.",
      ], 30)
    + p("Das ist derselbe Handgriff wie in 7.1b. Du zeigst ein Vorbild, sie "
        "holt die Bauweise heraus — nie die fertigen Sätze oder Bilder.", 28, PETROL),
    "Die Brücke zu 7.1b wirklich ziehen. Wenn sie EINMAL verstehen, dass "
    "Vorbild zeigen und Bauweise herausziehen bei allem funktioniert, haben "
    "sie den wertvollsten Handgriff des ganzen Kurses.")

# 🚨 Am 04.11.2026 dazu, auf Patricias Wunsch: „was mir noch fehlt ist
#    z.B. bei 7.4 ein Prompt für Claude code." Derselbe Bau wie l63-reden in
#    Modul 6 — Auftrag in ganzen Sätzen, und der letzte Halbsatz macht daraus
#    ein Gespräch. Wortlaut steht auch im Lektionstext, damit er kopierbar ist.
F["l74-prompt"] = folie("l74-prompt",
    eyebrow("Lektion 7.4")
    + h2("Das sagst du")
    + auftrag([
        "Ich filme meine Reels frei in einem Stück und wiederhole Sätze, bis "
        "einer sitzt. Ich korrigiere mich beim Sprechen nicht.",
        "Schneide nach diesen Regeln: Sage ich einen Satz mehrmals, gilt der "
        "<b>letzte vollständige</b> Anlauf · der <b>Hook</b> am Anfang bleibt "
        "wortwörtlich, der <b>Aufruf</b> am Schluss vollständig · raus fliegen "
        "Vorlauf, Versprecher, lange Pausen und alles nach meinem Schlusssatz.",
        "Leg mir die <b>Schnittliste als Text</b> vor. Geschnitten wird erst "
        "nach meiner Freigabe. Heraus kommen der Rohschnitt <b>und die "
        "einzelnen Stücke</b>, damit ich den Feinschnitt selbst ziehen kann.",
        "<b>Schreib die Regeln in eine Datei und mach daraus einen festen "
        "Auftrag</b>, damit ich das nie wieder erklären muss.",
        "Schau zuerst, was auf meinem Rechner schon da ist, und sag mir, was "
        "ich brauche. Erklär mir jeden Schritt, und frag nach, wenn dir eine "
        "Angabe fehlt.",
      ], 30, 16),
    "Der vierte Block ist der Bogen zu Modul 5: ohne ihn ist es einmal "
    "schneiden, mit ihm hat sie ab morgen einen Schnitt-Skill. Der zweite "
    "Block sind deine eigenen Regeln — die machen den Schnitt erst zu deinem. "
    "Wortlaut steht unter dem Video.")

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
    # 🚨 Gekuerzt am 04.11.2026: mit dem vollen Satz brauchte der Block mit der
    #    Ersatzschrift drei Zeilen und mit Philosopher zwei — und lief damit im
    #    Praesentationsmodus über die Zeile darunter.
    + p("Mein Instagram-Konto hängt an einem Partnerunternehmen. Ein unbedachter "
        "Satz kostet mich mehr, als eine automatisch geschriebene Woche je "
        "einbringt.", 40)
    + p("Wer nur für sich selbst schreibt, kann anders entscheiden. Wir nicht.", 34, PETROL),
    "Das ist der Satz, der diesen Kurs von jedem Technikkurs unterscheidet. "
    "Niemand sonst denkt beim Automatisieren an den Partnervertrag.")

F["l75-wie"] = folie("l75-wie",
    eyebrow("Lektion 7.5")
    + h2("Wie das praktisch aussieht")
    + reihe([
        # 🚨 In einer Karte ist nur ein Drittel Breite — kurz halten, sonst
        #    kippt die Zeile zwischen den Schriften und läuft aus der Karte.
        karte("Vorschlag", ["Sie legt fertige Beiträge ab.",
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

# 🚨 Am 04.11.2026 dazu, auf Patricias Wunsch: „ich hatte ja eine weile, dass
#    die storys per Telegrambot gekommen sind. die fertigen folien. aber auch
#    mal nur die texte. beide varianten will ich zeigen."
#    Wichtig als Gegengewicht zu 7.5: nicht alles muss gepostet werden.
#    Manches soll nur bei ihr ankommen.
F["l76-ankommen"] = folie("l76-ankommen",
    eyebrow("Lektion 7.6")
    + h2("Nicht alles muss gepostet werden")
    + reihe([
        # 🚨 Drei Karten, also ein Drittel Breite — jede Zeile kurz halten,
        #    sonst kippt sie zwischen den Schriften und läuft aus der Karte.
        karte("Liegen bleiben", ["Er wartet auf dich.",
                                 "Für alles, was du selbst posten willst."]),
        karte("Fertig aufs Handy", ["Die gebauten Folien kommen als Nachricht.",
                                    "Du lädst sie direkt hoch."], ORANGE),
        karte("Nur die Texte", ["Du bekommst den Wortlaut.",
                                "Die Folien baust du selbst."]),
      ], 28)
    + p("🚨 Die Bilder müssen als <b>Foto</b> kommen, nicht als Datei — nur dann "
        "landen sie in der Galerie, und nur von dort lädt Instagram sie hoch.", 28, PETROL),
    "Erzähl, dass du alle drei schon hattest, und wann welche dran ist. Die "
    "mittlere ist die, die sie am meisten überrascht: die Folien liegen "
    "morgens fertig auf dem Handy. Der rote Hinweis hat mich selbst einen "
    "Abend gekostet.")

F["l76-blotato"] = folie("l76-blotato",
    eyebrow("Lektion 7.6")
    + h2("Wenn es wirklich von selbst rausgehen soll")
    + liste([
        "Dafür braucht es einen <b>Dienst dazwischen</b> — Instagram lässt niemanden direkt posten.",
        "Du holst dort einen <b>Schlüssel</b> und gibst ihn Claude. Ein Satz, keine Einrichtung.",
        "🚨 <b>Instagram verbindest du in dem Dienst</b>, nicht in Claude.",
        "Der Weg ist dreiteilig: sie baut das Bild, der Dienst nimmt es, Instagram zeigt es.",
      ], 29)
    + p("Und wenn du das nicht willst: lass trotzdem Bild, Thema und Caption "
        "bauen und plan selbst ein. Du verlierst nur den letzten Handgriff.", 28, GEDAEMPFT),
    "Der letzte Satz ist wichtig. Ein kostenpflichtiger Dienst darf nie die "
    "Bedingung dafür sein, dass der Rest des Kurses etwas bringt. Nenn den "
    "Preis, wenn sie fragen — nicht von dir aus.")

F["l76-zwei"] = folie("l76-zwei",
    eyebrow("Lektion 7.6")
    + h2("Es sind zwei Aufträge, nicht einer")
    + reihe([
        karte("Wöchentlich", ["Sucht die Themen.",
                               "Schreibt die Entwürfe.",
                               "Legt sie dir hin."]),
        karte("Täglich", ["Schaut in „Zum Posten“.",
                           "Plant ein, was du freigegeben hast.",
                           "Räumt danach auf."], ORANGE),
      ])
    + p("Dazwischen stehst du: Du ziehst, was fertig ist, in den Ordner. "
        "<b>Dieser Handgriff ist deine Freigabe.</b>", 28, PETROL),
    "Die Trennung ist wichtig. Bauen und Posten in einem Auftrag heisst: du "
    "kannst nicht mehr dazwischen. Zwei Aufträge heissen: du entscheidest "
    "jeden Tag neu, ohne etwas anhalten zu müssen.")

F["l76-prompt"] = folie("l76-prompt",
    eyebrow("Lektion 7.6 · der tägliche Auftrag")
    + h2("Das sagst du")
    + auftrag([
        "In Canva habe ich drei Ordner: <b>Fertig · Zum Posten · Gepostet</b>. "
        "Leg sie an, falls es sie nicht gibt, und merk dir ihre Kennungen.",
        "Bau mir einen Auftrag, der täglich um <i>[Uhrzeit]</i> läuft: Schau in "
        "<b>Zum Posten</b> — ist er leer, hörst du auf.",
        "Je Design: Die <b>Caption steht als Kommentar</b>. Fehlt sie, "
        "schreibst du sie aus den Folientexten. Dann <b>prüf trocken</b>: "
        "Caption da, alle Folien da, Zeitpunkt in der Zukunft.",
        "Exportier das Design <b>als Bild</b>, plan den Beitrag für "
        "<i>[Uhrzeit]</i> am nächsten Tag ein, schieb das Design nach "
        "<b>Gepostet</b> und schreib mir, was du gemacht hast.",
        "Grenzen: nur Designs, keine Unterordner · höchstens <i>[Zahl]</i> am "
        "Tag · geht etwas schief, <b>bleibt das Design liegen</b>.",
      ], 29, 15),
    "Drei Stellen betonen: der Trockenlauf (sonst plant er Vergangenes ein und "
    "meldet trotzdem Erfolg), das Bild (von Canva direkt zum Einplanen geht "
    "nicht), und die Obergrenze — ohne sie kippt dir ein voller Ordner an "
    "einem Tag raus.")

F["l76-ersterlauf"] = folie("l76-ersterlauf",
    eyebrow("Lektion 7.6")
    + h2("Den ersten Lauf startest du von Hand")
    + p("Sonst hängt er bei der ersten Berechtigung — und meldet trotzdem, "
        "dass alles gut gelaufen sei.", 38, BLAU)
    + liste([
        "Einmal selbst starten und alle Nachfragen durchklicken.",
        "Danach läuft er allein.",
        "Prüf am nächsten Tag, ob wirklich etwas eingeplant wurde.",
      ], 30)
    + p("Mich hat genau das sechs Tage gekostet. Der Auftrag lief jeden Abend, "
        "stand still und meldete Erfolg.", 28, PETROL),
    "Diese Folie ist aus eigener Erfahrung, also erzähl sie auch so. Es ist "
    "der häufigste Grund, warum so ein Auftrag scheinbar läuft und doch "
    "nichts tut.")

F["l76-stolper"] = folie("l76-stolper",
    eyebrow("Lektion 7.6")
    + h2("Zwei Stolpersteine, die ich selbst hatte")
    + gegenueber(
        # 🚨 Zwei Spalten, also halbe Breite. Die erste Zeile jeder Spalte war
        #    zu lang und kippte zwischen den Schriften von zwei auf eine Zeile.
        "Der Zeitpunkt war vorbei",
        ["Abends freigegeben, für denselben Abend geplant.",
         "Der Dienst nimmt nichts in der Vergangenheit an.",
         "Die Freigabe meldete trotzdem Erfolg."],
        "Doppelt gepostet",
        ["Von Hand gepostet, Freigabe stand weiter auf offen.",
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
# ── 7.7b Recycling ───────────────────────────────────────────────────
# 🚨 Patricias Entscheid 04.11.2026: „ja nehmen wir trotzdem rein".
#    Ihr System ist hier stärker als das übliche, weil es am eigenen
#    Median misst statt an festen Zahlen.
F["l77b-titel"] = lektionstitel("l77b-titel", "7.7b", "Nochmal rausgehen",
    "Dein bester Beitrag hat die meisten nie erreicht.",
    "Die entspannteste Lektion des Moduls: hier entsteht Content ohne jede "
    "neue Arbeit.")

F["l77b-warum"] = folie("l77b-warum",
    eyebrow("Lektion 7.7b")
    + h2("Warum das kein Schummeln ist")
    + liste([
        "Instagram zeigt einen Beitrag nur einem Teil deiner Leute.",
        "Vier Wochen später ist er bei fast allen aus dem Kopf.",
        "Und es sind <b>neue</b> dazugekommen, die ihn nie gesehen haben.",
      ], 32)
    + p("Was gut lief, hat es verdient, nochmal zu laufen. Das ist der "
        "günstigste Content, den du je machst.", 28, PETROL),
    "Nimm die Scham raus. Viele denken, Wiederholen sei peinlich — in "
    "Wahrheit sieht es fast niemand zum zweiten Mal.")

F["l77b-median"] = folie("l77b-median",
    eyebrow("Lektion 7.7b")
    + h2("„Gut gelaufen“ heisst: besser als deine eigenen")
    + gegenueber(
        "Feste Zahlen",
        ["„Ab 10'000 Aufrufen.“",
         "Bei einem grossen Konto Alltag.",
         "Bei dir vielleicht nie."],
        "Dein eigener Schnitt",
        ["Besser als deine üblichen.",
         "Wächst mit, wenn du wächst.",
         "Gilt ab dem ersten Monat."])
    + p("Zwei Regeln dazu: erst <b>nach einer Woche</b> bewerten — vorher ist "
        "ein Beitrag nicht fertig gelaufen. Und <b>frühestens nach vier "
        "Wochen</b> wiederholen.", 28, GEDAEMPFT),
    "Das ist der Unterschied zu allem, was sie sonst lesen. Erklär kurz, "
    "warum feste Zahlen Unsinn sind, sobald zwei verschieden grosse Konten "
    "dieselbe Regel benutzen.")

F["l77b-prompt"] = folie("l77b-prompt",
    eyebrow("Lektion 7.7b")
    + h2("Das sagst du")
    + auftrag([
        "Bau mir einen Auftrag, der einmal im Monat schaut, welche meiner "
        "Beiträge <b>besser liefen als meine üblichen</b>.",
        "Zählen sollen Reichweite, Kommentare, Gespeichertes und Geteiltes — "
        "immer im Vergleich zu meinem <b>eigenen Durchschnitt</b>, nie zu "
        "fremden Zahlen.",
        "Nimm nur Beiträge, die <b>mindestens eine Woche</b> draussen sind und "
        "die ich seit <b>vier Wochen</b> nicht wiederholt habe.",
        "Leg mir eine Liste vor: Beitrag, Zahlen, warum er lief. <b>Ich suche "
        "aus</b>, was nochmal rausgeht.",
        "Zu jedem schreibst du mir eine <b>neue erste Zeile</b> — gleicher "
        "Inhalt, anderer Einstieg. Frag nach, wenn dir eine Angabe fehlt.",
      ], 30, 16),
    "Der vierte Block ist dieselbe Haltung wie in 7.5 — sie legt vor, du "
    "entscheidest. Der fünfte ist der Trick: derselbe Beitrag mit neuem "
    "Einstieg wirkt neu, auch für die, die ihn schon kannten.")

F["l77b-weiter"] = weiter("l77b-weiter", "Als Nächstes",
    "Was jetzt bei dir läuft",
    "Die Bilanz — und die Checkliste, bevor es weitergeht.",
    "Kurz überleiten.")

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
 "l71-titel","l71-aufbau","l71-leer","l71-material","l71-weiter",
 "l71b-titel","l71b-zweiwege","l71b-auftrag","l71b-grenze","l71b-weiter",
 "l72-titel","l72-versuch","l72-lehre","l72-story","l72-weiter",
 "l72b-titel","l72b-gemessen","l72b-vier","l72b-prompt","l72b-beleg","l72b-eigen","l72b-weiter",
 "l72c-titel","l72c-was","l72c-canva","l72c-aufgabe","l72c-erster","l72c-weiter",
 "l73-titel","l73-zweischritt","l73-zweiwege","l73-canva","l73-prompt","l73-stammvorlage","l73-editor","l73-weiter",
 "l74-titel","l74-ablauf","l74-regel","l74-mehr","l74-vorbild","l74-aufbau","l74-prompt","l74-weiter",
 "l75-titel","l75-warum","l75-wie","l75-satz","l75-weiter",
 "l76-titel","l76-abend","l76-zwei","l76-ankommen","l76-blotato",
 "l76-prompt","l76-ersterlauf","l76-stolper","l76-weiter",
 "l77-titel","l77-muster","l77-skript","l77-grenze",
 "l77b-titel","l77b-warum","l77b-median","l77b-prompt","l77b-weiter",
 "l78-titel","l78-bilanz","l78-checkliste","l78-weiter"]

SECTIONS = {
 "auftakt": {"description": "Worum es in Modul 7 geht.", "start": "cover"},
 "l71": {"description": "Lektion 7.1 — Maschine und Treibstoff im Überblick.", "start": "l71-titel"},
 "l71b": {"description": "Lektion 7.1b — wie sie die Wissensdateien füllt.", "start": "l71b-titel"},
 "l72": {"description": "Lektion 7.2 — derselbe Skill leer und gefüllt.", "start": "l72-titel"},
 "l72b": {"description": "Lektion 7.2b — woher die Themen kommen.", "start": "l72b-titel"},
 "l72c": {"description": "Lektion 7.2c — Canva, Posting-Dienst und geplante Aufgaben anschliessen.", "start": "l72c-titel"},
 "l73": {"description": "Lektion 7.3 — Karussell vom Text zum Bild.", "start": "l73-titel"},
 "l74": {"description": "Lektion 7.4 — Reel-Rohschnitt aus Rohmaterial.", "start": "l74-titel"},
 "l75": {"description": "Lektion 7.5 — warum nichts ohne Freigabe rausgeht.", "start": "l75-titel"},
 "l76": {"description": "Lektion 7.6 — der Abendlauf und zwei Stolpersteine.", "start": "l76-titel"},
 "l77": {"description": "Lektion 7.7 — KI-Muster erkennen und prüfen.", "start": "l77-titel"},
 "l77b": {"description": "Lektion 7.7b — gut Gelaufenes nochmal rausschicken.", "start": "l77b-titel"},
 "l78": {"description": "Lektion 7.8 — Bilanz und Checkliste vor Modul 8.", "start": "l78-titel"},
}

schreibe(ZIEL, "Modul 7 — Social Media", F, ORDER, SECTIONS)
