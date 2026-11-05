#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Folien für Modul 6 — Bots, die von selbst laufen.

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
    "Drei Bots, ein Handy. Alles ohne mein Zutun.",
    "Ganz am Handy filmen. Nicht auf Folien erklären, sondern durch die "
    "Nachrichten scrollen — das ist der Moment, in dem es klick macht.")

# 🚨 Am 04.11.2026 von vier auf drei gekürzt. Vorher standen hier Garten,
#    Küche, Business und Haushalt — den Haushalts-Bot gibt es aber nicht mehr
#    (der cron in `.github/workflows/haushalt-vorabend.yml` ist auskommentiert),
#    und der alte Cockpit-Bot ist seit dem 25.10.2026 aus. Zeigen lassen sich:
#    Garten (Railway, täglich) · Kochassistent (Do 18:00) · „Heute dran"
#    (Cloud-Routine, 07:00 und 20:00, seit dem 03.11.2026).
#    Ein Beispiel auf einer Folie, das es nicht mehr gibt, fällt beim Filmen
#    auf — spätestens, wenn sie es am Handy aufmachen will.
F["l62-drei"] = folie("l62-drei",
    eyebrow("Lektion 6.2")
    + h2("Drei Beispiele")
    + reihe([
        karte("Garten", ["Was gerade dran ist, mit Blick aufs Wetter."]),
        karte("Küche", ["Vier Fragen am Donnerstag, der Plan am Freitag."], ORANGE),
        karte("Business", ["Morgens und abends: was heute dran ist."]),
      ], 28),
    "Sag bei jedem einen Satz, wofür er dir Arbeit abnimmt. Nicht wie er gebaut ist — "
    "das kommt in der nächsten Lektion. Und sag dazu, dass zwei von den drei nichts "
    "mit Arbeit zu tun haben: das ist der Satz, der ihnen die Angst nimmt.")

F["l62-gemein"] = folie("l62-gemein",
    eyebrow("Lektion 6.2")
    + h2("Was alle drei gemeinsam haben")
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
    "hast — lieber banal und er kommt an, als clever und sie steigt aus. "
    "🚨 Schritt 1 kannst du nicht live zeigen, dein Bot steht ja schon. Dafür "
    "sind die nächsten zwei Folien da: sag ehrlich „den Teil habe ich vor "
    "einem Jahr gemacht, so sieht er aus“ und geh die Folie durch. "
    "Ab Schritt 2 bist du wieder live.")

# 🚨 Am 04.11.2026 umgebaut, auf Patricias Entscheid: „ich labere in den chat
#    was ich von ihm will und er macht es und fuehrt mich durch. ist ja viel
#    die einfachere variante. ich moechte eigentlich die zeigen."
#    Dasselbe hat sie in 5.4 schon entschieden („Zeig beide, aber nimm für die
#    Aufnahme den Baukasten").
#    Und es ist nicht nur die schoenere Variante: Lektion 4.2 verspricht „Die
#    App bringt alles mit. Du installierst nichts weiter." Eine Vorlage zum
#    Selberstarten braucht dagegen eine Laufzeit, die niemand installiert hat.
#    Wer redet, bekommt einen Bot in dem, was auf ihrem Rechner schon da ist.
F["l63-schritte"] = folie("l63-schritte",
    eyebrow("Lektion 6.3")
    + h2("Eins machst du selbst")
    + liste([
        "<b>Den Botvater fragen.</b> Nur du bekommst den Schlüssel — das nimmt dir niemand ab.",
        "<b>Sagen, was du willst.</b> In ganzen Sätzen, so wie du es einer Freundin erzählst.",
        "<b>Antworten.</b> Sie fragt nach, was ihr fehlt. Du musst nichts vorbereiten.",
        "<b>Aufs Handy schauen.</b> Wenn die Nachricht da ist, läuft er.",
      ], 30),
    "Sag die Überschrift wirklich so: EINS machst du selbst, und das ist der "
    "Botvater. Alles andere ist reden. Wer glaubt, sie müsse vier Dinge "
    "können, steigt hier aus.")

# 🚨 Diese zwei Folien sind am 04.11.2026 dazugekommen, weil Patricia Schritt 1
#    nicht live zeigen kann: ihr Bot existiert seit einem Jahr, und einen
#    zweiten anzulegen nur für die Kamera waere gespielt. Darum steht hier,
#    was der Botvater fragt und was Claude Code danach fragt — damit sie es
#    wiedererkennen, wenn es bei ihnen auf dem Bildschirm steht.
F["l63-botvater"] = folie("l63-botvater",
    eyebrow("Lektion 6.3 · Schritt 1")
    + h2("Was der Botvater fragt")
    + liste([
        "Du schreibst ihm <b>/newbot</b> — das ist alles, was du tippst.",
        "<b>„Choose a name for your bot“</b> — der Name, den du nachher im Chat siehst. <i>Mein Morgenbote.</i>",
        "<b>„Choose a username... must end in bot“</b> — die Adresse. <i>morgenbote_sandra_bot.</i> Gibt es sie schon, sagt er es und du nimmst eine andere.",
        "<b>„Use this token to access the HTTP API“</b> — darunter steht dein Schlüssel.",
      ], 29)
    + p("Er spricht Englisch. Das ist der einzige Ort im ganzen Kurs, an dem das "
        "so ist — und du brauchst nur diese vier Zeilen zu erkennen.", 28, PETROL),
    "Sag den letzten Satz wirklich. Englisch ist für viele die eigentliche "
    "Hürde, nicht die Technik. Und sag dazu, dass du diesen Teil vor einem "
    "Jahr gemacht hast — nicht so tun, als würdest du es gerade anlegen.")

F["l63-reden"] = folie("l63-reden",
    eyebrow("Lektion 6.3 · Schritt 2")
    + h2("Das sagst du")
    + ('<div style="background:#fdfcf8; padding:44px 48px; border-radius:18px; '
       'border-left:8px solid #12828c; display:flex; flex-direction:column; gap:20px">'
       '<p style="font-size:34px; line-height:1.5; color:#0c1c30">'
       'Ich möchte einen Bot, der mir jeden Morgen um sieben auf Telegram '
       'schreibt. Er soll mir <i>[das hier schreibst du selbst]</i>.</p>'
       '<p style="font-size:34px; line-height:1.5; color:#0c1c30">'
       'Ich habe einen Schlüssel vom Botvater. Erklär mir jeden Schritt, '
       'und <b>frag nach, wenn dir etwas fehlt</b>.</p></div>')
    + p("Mehr ist es nicht. Der letzte Halbsatz ist der wichtigste: ab da "
        "führt sie dich.", 28, PETROL),
    "Lies den Auftrag laut vor und tipp ihn dann wirklich ein — nicht "
    "einfügen, tippen. Sie soll sehen, dass da kein Zauberwort steht. "
    "Und betone den letzten Halbsatz: der macht aus einem Auftrag ein "
    "Gespräch.")

F["l63-gefuehrt"] = folie("l63-gefuehrt",
    eyebrow("Lektion 6.3 · Schritt 2 bis 4")
    + h2("Du wirst gefragt, nicht geprüft")
    + liste([
        "<b>„Wo ist dein Schlüssel?“</b> — du sagst es ihr, sie legt ihn an die richtige Stelle.",
        "<b>„Wem soll er schreiben?“</b> — du schreibst deinem Bot einmal <i>Hallo</i>, sie holt die Nummer.",
        "<b>„Was soll in der Nachricht stehen?“</b> — das ist dein Auftrag. Ganze Sätze, kein Fachwort.",
        "<b>„Soll ich ihn einmal starten?“</b> — du sagst ja und schaust aufs Handy.",
      ], 29)
    + p("Der Wortlaut ist bei dir anders als bei mir. Die vier Fragen sind "
        "dieselben — und du antwortest nur.", 28, PETROL),
    "Das ist die wichtigste Folie der Lektion. Wer hier glaubt, sie müsse "
    "etwas abtippen können, steigt aus. Sag ausdrücklich: du tippst keinen "
    "einzigen Befehl ab ausser /newbot.")

F["l63-geruest"] = folie("l63-geruest",
    eyebrow("Lektion 6.3")
    + h2("Der eine Satz, den du nicht vergessen darfst")
    # 🚨 Hier stand bis zum 04.11.2026 eine Vorlage zum Herunterladen. Raus,
    #    weil Lektion 4.2 verspricht „Du installierst nichts weiter" — und eine
    #    Vorlage zum Selberstarten bricht genau dieses Versprechen. Was bleibt,
    #    ist das, was man nach dem Video nochmal nachlesen will.
    + p("Beim Einrichten entsteht ein Zugangsschlüssel. Er gehört in die Datei, "
        "die sie dafür anlegt — nie in ein Dokument, nie in eine Nachricht.", 36)
    + p("Sie macht das von selbst richtig. Du musst es nur einmal gesehen haben, "
        "damit du es wiedererkennst.", 30, GEDAEMPFT)
    + beilage("Der Auftrag zum Kopieren und die vier Schritte zum Nachlesen"),
    "Das ist die einzige Stelle, an der du streng bist. Sag den Grund NICHT — "
    "der kommt in Modul 10. Sag nur, dass es die wichtigste Angewohnheit im "
    "ganzen Kurs ist.")

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
        # 🚨 In einer Karte ist nur ein Drittel Breite. „Ist der Zeitplan
        #    überhaupt aktiv?" und „Er lief, aber er ist unterwegs gestolpert."
        #    kippten zwischen den Schriften von zwei auf eine Zeile und
        #    liefen dadurch aus der Karte heraus. Kurz ist hier Pflicht.
        karte("1 · Der Wecker", ["Ist der Zeitplan aktiv?",
                                 "Am häufigsten, und am schnellsten geprüft."]),
        karte("2 · Der Schlüssel", ["Abgelaufen oder beim Umziehen nicht mitgekommen.",
                                    "Steht dann so im Protokoll."], ORANGE),
        karte("3 · Der Auftrag", ["Er ist unterwegs gestolpert.",
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
 "l62-titel","l62-drei","l62-gemein","l62-weiter",
 "l63-titel","l63-schritte","l63-botvater","l63-reden","l63-gefuehrt","l63-geruest","l63-weiter",
 "l64-titel","l64-wege","l64-zeit","l64-weiter",
 "l65-titel","l65-gruende","l65-fragen",
 "l66-titel","l66-bilanz","l66-checkliste","l66-weiter"]

SECTIONS = {
 "auftakt": {"description": "Worum es in Modul 6 geht.", "start": "cover"},
 "l61": {"description": "Lektion 6.1 — der Unterschied zwischen Skill und Bot.", "start": "l61-titel"},
 "l62": {"description": "Lektion 6.2 — drei Bots, die bei Patricia laufen.", "start": "l62-titel"},
 "l63": {"description": "Lektion 6.3 — den ersten Bot bauen.", "start": "l63-titel"},
 "l64": {"description": "Lektion 6.4 — Zeitplan und Kosten.", "start": "l64-titel"},
 "l65": {"description": "Lektion 6.5 — Fehlersuche, wenn nichts kommt.", "start": "l65-titel"},
 "l66": {"description": "Lektion 6.6 — Bilanz und Checkliste vor Modul 7.", "start": "l66-titel"},
}

schreibe(ZIEL, "Modul 6 — Bots", F, ORDER, SECTIONS)
