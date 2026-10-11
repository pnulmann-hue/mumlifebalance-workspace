#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Folien fuer Modul 4 — Claude Code einrichten.

    python scripts/ki-kurs/folien-modul-4.py <zielordner>
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from folien_basis import *

ZIEL = sys.argv[1] if len(sys.argv) > 1 else "folien-modul-4"
F = {}

F["cover"] = modulcover(4, "Dein Arbeitsplatz",
    "Jetzt richtest du dir einen eigenen Platz ein, an dem dein Wissen, deine Dateien "
    "und deine Befehle zusammenliegen.",
    "Das ist das Modul, in dem die meisten aussteigen. Nimm dir hier mehr Zeit als sonst "
    "und springe keinen Schritt.")

# ── 4.1 Keine Angst ──────────────────────────────────────────────────
F["l41-titel"] = lektionstitel("l41-titel", "4.1", "Es ist kein Programmieren",
    "Was Claude Code wirklich ist — und was du dafür können musst.",
    "Sag den Satz gleich am Anfang: Du schreibst weiter Deutsch. Alles andere in dieser "
    "Lektion ist die Begründung dafür.")

F["l41-was"] = folie("l41-was",
    eyebrow("Lektion 4.1")
    + h2("Was sich ändert, was gleich bleibt")
    + gegenueber(
        "Bleibt gleich",
        ["Du schreibst Deutsch, in ganzen Sätzen.",
         "Du sagst, was rauskommen soll.",
         "Dein Business-Brief geht mit."],
        "Kommt dazu",
        ["Sie hat einen Ordner auf deinem Rechner, in dem alles liegt.",
         "Sie kann Dateien anlegen und ändern.",
         "Du kannst Arbeiten als Befehl ablegen."]),
    "Die linke Spalte nimmt die Angst, die rechte macht neugierig. Geh sie in dieser "
    "Reihenfolge durch.")

F["l41-angst"] = folie("l41-angst",
    eyebrow("Lektion 4.1")
    + h2("Was du dafür brauchst")
    + liste([
        "Einen Rechner. Ein Laptop reicht, es muss nichts Schnelles sein.",
        "Ein Abo, wie in Lektion 1.4 besprochen.",
        "Zwanzig Minuten für die Einrichtung.",
        "<b>Kein Vorwissen.</b> Wenn du weisst, was ein Ordner ist, reicht das.",
      ], 34),
    "Der letzte Punkt ist der einzige, der wirklich zählt. Sag ihn so, wie du ihn meinst — "
    "ohne Aufmunterungs-Ton, einfach als Tatsache.")

F["l41-weiter"] = weiter("l41-weiter", "Als Nächstes",
    "Einrichten, Schritt für Schritt",
    "Klick für Klick mitgefilmt. Mach das Video an und mach auf deinem Rechner parallel mit.",
    "Bitte sie ausdrücklich, jetzt den Laptop aufzuklappen. Wer diese Lektion nur anschaut, "
    "macht sie nie.")

# ── 4.2 Einrichten ───────────────────────────────────────────────────
F["l42-titel"] = lektionstitel("l42-titel", "4.2", "Einrichten",
    "Schritt für Schritt, in Echtzeit, ohne Sprung.",
    "Die ganze Lektion ist geteilter Bildschirm. Rede langsamer als sonst und warte nach "
    "jedem Klick einen Moment.")

F["l42-vorher"] = folie("l42-vorher",
    eyebrow("Lektion 4.2")
    + h2("Bevor du anfängst")
    + liste([
        "Leg dir deinen Business-Brief bereit — den aus Modul 2.",
        "Such dir einen Ort auf deinem Rechner, an dem der Ordner liegen soll.",
        "<b>Nimm keinen Cloud-Ordner.</b> Was dort liegt, wird überallhin kopiert, "
        "auch das, was du später nicht kopiert haben willst.",
        "Plan zwanzig Minuten ohne Unterbrechung ein.",
      ], 34),
    "Der dritte Punkt ist wichtiger als er klingt und kommt in Modul 10 wieder. Ein Arbeitsplatz "
    "in einer Cloud-Ablage hebelt später jede Ausschlussliste aus.")

F["l42-schritte"] = folie("l42-schritte",
    eyebrow("Lektion 4.2")
    + h2("Die vier Schritte")
    + reihe([
        karte("1 · Herunterladen", ["Die Desktop-App holen und öffnen."]),
        karte("2 · Anmelden", ["Mit dem Konto aus Modul 1."], ORANGE),
        karte("3 · Ordner wählen", ["Den Platz, den du dir vorhin ausgesucht hast."]),
        karte("4 · Erste Frage", ["Irgendetwas Einfaches, damit du siehst, dass es läuft."]),
      ]),
    "Vier Karten, vier Klicks. Wenn bei dir beim Aufnehmen etwas hakt, lass es drin und "
    "erklär es — genau das passiert ihr auch.")

F["l42-weiter"] = weiter("l42-weiter", "Als Nächstes",
    "Dein Arbeitsplatz",
    "Wir schauen uns an, welche Ordner es gibt und wofür jeder da ist. Danach lädst du "
    "mein Grundgerüst herunter.",
    "Kurz halten, die Orientierung kommt auf der nächsten Folie. Sag nur, dass sie den Ordner "
    "nicht selbst anlegen muss — das nimmt schon hier Druck raus.")

# ── 4.3 Arbeitsplatz ─────────────────────────────────────────────────
F["l43-titel"] = lektionstitel("l43-titel", "4.3", "Dein Arbeitsplatz",
    "Fünf Ordner, und jeder hat genau eine Aufgabe.",
    "Zeig zuerst deinen eigenen Arbeitsplatz, dann das leere Gerüst. Der Kontrast macht "
    "klar, wohin die Reise geht.")

F["l43-ordner"] = folie("l43-ordner",
    eyebrow("Lektion 4.3")
    + h2("Wo was hingehört")
    + liste([
        "<b>context</b> — dein Wissen. Der Business-Brief liegt hier, und alles, was die KI "
        "über dich wissen soll.",
        "<b>outputs</b> — was rauskommt. Captions, Folien, Pläne.",
        "<b>reference</b> — Material zum Nachschlagen, das du nicht selbst geschrieben hast.",
        "<b>scripts</b> — kleine Helfer, die immer dasselbe tun.",
        "<b>plans</b> — was du vorhast, bevor du es machst.",
      ], 32),
    "Die Trennung von context und reference ist die wichtigste: Das eine ist deins, das "
    "andere hast du irgendwoher. Das hilft dir später beim Aufräumen.")

F["l43-geruest"] = folie("l43-geruest",
    eyebrow("Lektion 4.3")
    + h2("Das Grundgerüst")
    + p("Du musst das nicht selbst anlegen. Unter diesem Video liegt mein Gerüst mit allen "
        "Ordnern, einer vorbereiteten Gedächtnis-Datei und ein paar Befehlen zum Ausprobieren.", 38)
    + liste([
        "Herunterladen, entpacken, an deinen Platz legen.",
        "Deinen Business-Brief in <b>context</b> hineinkopieren.",
        "Einmal aufrufen und schauen, ob sie ihn findet.",
      ], 32)
    + p("📎 Das Grundgerüst liegt unter diesem Video.", 30, PETROL),
    "Zeig den dritten Schritt wirklich. Der Moment, in dem sie merkt, dass die KI ihren "
    "Brief gelesen hat, ist der Moment, in dem Modul 2 sich auszahlt.")

F["l43-weiter"] = weiter("l43-weiter", "Als Nächstes",
    "Das Gedächtnis deines Arbeitsplatzes",
    "Eine einzige Datei, in der steht, was sie immer wissen soll.",
    "Kurze Brücke, aber mach neugierig: Diese Datei ist der Unterschied zwischen einem "
    "Ordner und einem Arbeitsplatz.")

# ── 4.4 CLAUDE.md ────────────────────────────────────────────────────
F["l44-titel"] = lektionstitel("l44-titel", "4.4", "Das Gedächtnis",
    "Die eine Datei, in der steht, was du nicht jedes Mal neu erklären willst.",
    "Zeig zuerst deine eigene und scroll langsam durch. Der Umfang macht mehr Eindruck als "
    "jede Erklärung — und sag dazu, dass sie über Monate gewachsen ist.")

F["l44-was"] = folie("l44-was",
    eyebrow("Lektion 4.4")
    + h2("Was hineingehört")
    + reihe([
        karte("Wer du bist", ["Ein Verweis auf deinen Business-Brief reicht.",
                              "Sie liest ihn dann selbst."]),
        karte("Wie du arbeitest", ["Deine Regeln, deine Verbote, dein Ton."], ORANGE),
        karte("Was wo liegt", ["Welcher Ordner wofür da ist, damit sie nichts sucht."]),
      ]),
    "Die mittlere Karte ist die, die über Monate wächst. Sag es jetzt schon, damit sie "
    "nicht versucht, am ersten Tag alles hineinzuschreiben.")

F["l44-regel"] = folie("l44-regel",
    eyebrow("Lektion 4.4")
    + h2("Wie sie wächst")
    + p("Du schreibst nicht alles auf einmal hinein. Du fängst mit fünf Zeilen an und "
        "ergänzt jedes Mal, wenn dich etwas zum dritten Mal geärgert hat.", 40)
    + p("Bei mir steht inzwischen jede Regel drin, die aus einem echten Fehler entstanden ist. "
        "Genau deshalb macht sie denselben Fehler kein viertes Mal.", 34, GEDAEMPFT)
    + p("📎 Die leere Vorlage liegt unter diesem Video.", 30, PETROL),
    "Erzähl hier einen deiner eigenen Fehler und die Regel, die daraus wurde. "
    "Ein echtes Beispiel trägt die ganze Lektion.")

F["l44-satz"] = statement("l44-satz",
    ["Was dich dreimal ärgert,", "gehört als Regel hinein."],
    "Sonst ärgert es dich ein viertes Mal.",
    "Der Satz kommt in Modul 5 bei den Skills wieder. Setz ihn hier zum ersten Mal.")

# ── 4.5 Sprechen ─────────────────────────────────────────────────────
F["l45-titel"] = lektionstitel("l45-titel", "4.5", "Wie du mit ihr sprichst",
    "Drei Gewohnheiten, die den Unterschied machen.",
    "Kurze Lektion, aber sie spart ihr viel Frust. Nimm für jede Gewohnheit ein Beispiel "
    "aus deinem eigenen Alltag.")

F["l45-regeln"] = folie("l45-regeln",
    eyebrow("Lektion 4.5")
    + h2("Drei Gewohnheiten")
    + liste([
        "<b>Sag, was rauskommen soll, nicht wie sie es machen soll.</b> Sie kennt den Weg "
        "meistens besser als du.",
        "<b>Ein Ding pro Auftrag.</b> Zwei Aufgaben in einem Satz werden beide halb erledigt.",
        "<b>Lass sie fragen.</b> Wenn etwas unklar ist, soll sie nachhaken statt zu raten.",
      ], 34),
    "Die dritte ist die unbekannteste. Zeig, wie du das in deine Gedächtnis-Datei schreibst, "
    "damit sie es von selbst macht.")

F["l45-beispiel"] = folie("l45-beispiel",
    eyebrow("Lektion 4.5")
    + h2("Derselbe Auftrag, zwei Arten")
    + gegenueber(
        "Zu eng gefasst",
        [zit("Mach eine Tabelle mit drei Spalten und schreib in die erste die Woche"),
         "Sie baut genau das — auch wenn es für deine Frage gar nicht passt."],
        "Am Ergebnis entlang",
        [zit("Ich will auf einen Blick sehen, was diese Woche offen ist"),
         "Sie schlägt vor, wie das am besten aussieht, und du sagst Ja oder Nein."]),
    "Das ist der häufigste Anfängerfehler und niemand merkt ihn, weil das Ergebnis ja "
    "irgendwie stimmt. Es ist nur nicht das beste.")

F["l45-weiter"] = weiter("l45-weiter", "Als Nächstes",
    "Wenn es nicht klappt",
    "Was du machst, wenn Murks rauskommt — und die drei Fehler, die am Anfang alle machen.",
    "Kündige an, dass jetzt der Frust-Teil kommt. Dass du ihn überhaupt ansprichst, "
    "nimmt ihm die Hälfte.")

# ── 4.6 Wenn es nicht klappt ─────────────────────────────────────────
F["l46-titel"] = lektionstitel("l46-titel", "4.6", "Wenn es nicht klappt",
    "Was du tust, wenn Murks rauskommt.",
    "Erzähl von einem eigenen Fall, in dem du zehn Minuten nachgebessert hast, statt neu "
    "anzusetzen. Das macht die Lektion glaubwürdig.")

F["l46-fehler"] = folie("l46-fehler",
    eyebrow("Lektion 4.6")
    + h2("Die drei Fehler am Anfang")
    + reihe([
        karte("Zu viel auf einmal", ["Drei Aufgaben in einem Auftrag.",
                                     "Ergebnis: alle drei halb."]),
        karte("Zu wenig Kontext", ["Sie weiss nicht, für wen der Text ist.",
                                   "Ergebnis: passt auf jede."], ORANGE),
        karte("Endloses Gespräch", ["Nach dreissig Runden fällt hinten etwas heraus.",
                                    "Ergebnis: sie widerspricht sich."]),
      ]),
    "Beim dritten: erklär kurz das Kontextfenster aus dem Cheatsheet. Das ist die Erklärung, "
    "die sonst nie jemand gibt.")

F["l46-neu"] = folie("l46-neu",
    eyebrow("Lektion 4.6")
    + h2("Neu ansetzen schlägt nachbessern")
    + p("Wenn das Ergebnis danebenliegt, ist die Versuchung gross, es mit drei Nachfragen "
        "geradezubiegen. Meistens wird es dabei schlechter.", 40)
    + liste([
        "Neues Gespräch aufmachen.",
        "Den Auftrag umschreiben, nicht ergänzen.",
        "Ein Beispiel dazulegen, wie gut aussieht.",
      ], 34),
    "Zeig das live an einem Fall, der wirklich danebengeht. Ein misslungener Versuch im "
    "Video ist mehr wert als drei gelungene.")

F["l46-satz"] = statement("l46-satz",
    ["Es liegt am Auftrag,", "nicht an dir."],
    "Und einen Auftrag kannst du ändern.",
    "Viele geben an dieser Stelle auf, weil sie denken, sie seien zu blöd dafür. "
    "Sag diesen Satz so deutlich wie möglich.")

# ── 4.7 Zusammenfassung ──────────────────────────────────────────────
F["l47-titel"] = lektionstitel("l47-titel", "4.7", "Zusammenfassung",
    "Was jetzt bei dir steht, bevor wir an die Skills gehen.",
    "Kurze Lektion, drei bis vier Minuten. Wichtig ist nur, dass der Arbeitsplatz wirklich "
    "läuft, bevor sie weitergeht.")

F["l47-bilanz"] = folie("l47-bilanz",
    eyebrow("Lektion 4.7")
    + h2("Das nimmst du mit")
    + reihe([
        karte("Ein Arbeitsplatz", ["Claude Code läuft, die Ordner stehen, dein Wissen liegt drin."]),
        karte("Ein Gedächtnis", ["Deine erste Fassung der Gedächtnis-Datei."], ORANGE),
        karte("Drei Gewohnheiten", ["Am Ergebnis entlang, ein Ding pro Auftrag, fragen lassen."]),
      ]),
    "Die dritte Karte ist die, die sie am ehesten wieder vergisst. Sag, dass sie in "
    "Modul 5 sofort wieder gebraucht wird.")

F["l47-checkliste"] = checkliste("l47-checkliste", "4.7", [
    "Claude Code läuft bei mir und ich komme hinein",
    "Ich habe das Grundgerüst heruntergeladen und geöffnet",
    "Ich weiss, wofür jeder Ordner da ist",
    "Meine Gedächtnis-Datei ist ausgefüllt",
    "Ich habe einen Auftrag gegeben, der durchgelaufen ist",
  ], 4,
  "Wenn der erste Punkt offen ist, soll sie nicht weitermachen. Alles ab hier setzt einen "
  "laufenden Arbeitsplatz voraus.")

F["l47-weiter"] = folie("l47-weiter",
    eyebrow("Modul 5", ORANGE)
    + ('<h2 style="font-family:%s; font-size:84px; font-weight:700; line-height:1.15; color:%s">'
       'Skills —<br>das Herzstück</h2>' % (DISPLAY, CREME))
    + p("Jetzt kommt das Modul, wegen dem du hier bist. Eine Arbeit einmal beschreiben und "
        "danach nur noch aufrufen.", 36, PETROL),
    "Bau Spannung auf. Modul 5 ist das, was sie am längsten benutzen wird.",
    stil=SEK_DUNKEL, uebergang="push")


ORDER = ["cover",
 "l41-titel","l41-was","l41-angst","l41-weiter",
 "l42-titel","l42-vorher","l42-schritte","l42-weiter",
 "l43-titel","l43-ordner","l43-geruest","l43-weiter",
 "l44-titel","l44-was","l44-regel","l44-satz",
 "l45-titel","l45-regeln","l45-beispiel","l45-weiter",
 "l46-titel","l46-fehler","l46-neu","l46-satz",
 "l47-titel","l47-bilanz","l47-checkliste","l47-weiter"]

SECTIONS = {
 "auftakt": {"description": "Worum es in Modul 4 geht.", "start": "cover"},
 "l41": {"description": "Lektion 4.1 — warum das kein Programmieren ist.", "start": "l41-titel"},
 "l42": {"description": "Lektion 4.2 — einrichten, Schritt für Schritt.", "start": "l42-titel"},
 "l43": {"description": "Lektion 4.3 — die Ordner und das Grundgerüst.", "start": "l43-titel"},
 "l44": {"description": "Lektion 4.4 — die Gedächtnis-Datei.", "start": "l44-titel"},
 "l45": {"description": "Lektion 4.5 — wie man mit ihr spricht.", "start": "l45-titel"},
 "l46": {"description": "Lektion 4.6 — was tun, wenn es nicht klappt.", "start": "l46-titel"},
 "l47": {"description": "Lektion 4.7 — Bilanz und Checkliste vor Modul 5.", "start": "l47-titel"},
}

schreibe(ZIEL, "Modul 4 — Dein Arbeitsplatz", F, ORDER, SECTIONS)
