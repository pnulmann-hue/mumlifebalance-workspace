#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Folien fuer Modul 5 — Skills, das Herzstueck.

    python scripts/ki-kurs/folien-modul-5.py <zielordner>
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from folien_basis import *

ZIEL = sys.argv[1] if len(sys.argv) > 1 else "folien-modul-5"
F = {}

F["cover"] = modulcover(5, "Skills",
    "Eine Arbeit einmal beschreiben und danach nur noch aufrufen. "
    "Alles, was danach kommt, ist Anwendung davon.",
    "Sag am Anfang: Wenn sie aus dem ganzen Kurs nur ein Modul mitnimmt, dann dieses. "
    "Das ist keine Werbung, das stimmt einfach.")

# ── 5.1 Was ein Skill ist ────────────────────────────────────────────
F["l51-titel"] = lektionstitel("l51-titel", "5.1", "Was ein Skill ist",
    "Ein Rezept, das die KI jedes Mal gleich abarbeitet.",
    "Steig damit ein, dass du einen aufrufst und sie zuschauen lässt, bevor du erklärst, "
    "was da gerade passiert ist.")

F["l51-rezept"] = folie("l51-rezept",
    eyebrow("Lektion 5.1")
    + h2("Das Bild dahinter")
    + p("Ein Rezept sagt, welche Zutaten du brauchst, in welcher Reihenfolge du sie nimmst "
        "und woran du merkst, dass es gut geworden ist.", 40)
    + p("Ein Skill macht genau das für eine Arbeit, die du regelmässig machst. Einmal "
        "aufgeschrieben, und danach rufst du ihn nur noch auf.", 36, GEDAEMPFT),
    "Bleib bei einem Bild und wechsle es nicht. Wer drei Vergleiche hört, behält keinen.")

F["l51-warum"] = folie("l51-warum",
    eyebrow("Lektion 5.1")
    + h2("Was sich dadurch ändert")
    + gegenueber(
        "Ohne Skill",
        ["Du erklärst jedes Mal von vorne, was du willst.",
         "Das Ergebnis schwankt, je nachdem wie gut du gerade formulierst.",
         "An einem müden Tag wird es schlechter."],
        "Mit Skill",
        ["Du rufst ihn auf und gibst nur noch das Thema mit.",
         "Das Ergebnis ist jedes Mal gleich aufgebaut.",
         "An einem müden Tag wird es trotzdem gut."]),
    "Der letzte Punkt rechts ist der, der zählt. Ein Skill ist besser als du selbst um "
    "zehn Uhr abends, und das darfst du auch so sagen.")

F["l51-weiter"] = weiter("l51-weiter", "Als Nächstes",
    "Ein Skill auseinandergenommen",
    "Wir gehen einen fertigen Zeile für Zeile durch, damit du siehst, woraus er besteht.",
    "Sag, dass sie beim nächsten Video nichts mitmachen muss. Erst schauen, dann bauen — "
    "das nimmt den Druck.")

# ── 5.2 Auseinandergenommen ──────────────────────────────────────────
F["l52-titel"] = lektionstitel("l52-titel", "5.2", "Auseinandergenommen",
    "Ein fertiger Skill, Zeile für Zeile.",
    "Nimm den Kochplan-Skill. Er ist privat, jede versteht sofort worum es geht, und "
    "niemand muss dabei über ihr Business nachdenken.")

F["l52-teile"] = folie("l52-teile",
    eyebrow("Lektion 5.2")
    + h2("Sechs Teile, immer dieselben")
    + liste([
        "<b>Kopf</b> — der Name und ein Satz, woran die KI erkennt, wann er dran ist.",
        "<b>Zweck</b> — was am Ende dasteht, in zwei Sätzen.",
        "<b>Was sie vorher liest</b> — bei fast allen mindestens dein Business-Brief.",
        "<b>Regeln</b> — deine Vorgaben und deine Verbote.",
        "<b>Was herauskommen soll</b> — ganz genau, mit Zahl und Form.",
        "<b>Ein Beispiel</b> — eines reicht, und es muss von dir sein.",
      ], 31),
    "Geh die sechs am Bildschirm durch, nicht auf der Folie. Die Folie ist nur die Landkarte "
    "daneben, damit sie den Faden nicht verliert.")

F["l52-genau"] = folie("l52-genau",
    eyebrow("Lektion 5.2")
    + h2("Der Teil, an dem es meistens scheitert")
    + gegenueber(
        "Zu ungenau",
        [zit("Gib mir ein paar Ideen"),
         "Mal drei, mal zwölf. Mal Stichworte, mal ganze Absätze.",
         "Du sortierst danach von Hand."],
        "Genau genug",
        [zit("Fünf Vorschläge, je höchstens zwei Sätze, ohne Einleitung"),
         "Jedes Mal fünf. Jedes Mal in derselben Form.",
         "Du nimmst einen und machst weiter."]),
    "Das ist der häufigste Grund, warum ein selbstgebauter Skill enttäuscht. "
    "Zeig beide Ergebnisse nebeneinander.")

F["l52-weiter"] = weiter("l52-weiter", "Als Nächstes",
    "Woran du erkennst, dass etwas ein Skill werden sollte",
    "Bevor du einen baust, brauchst du die richtige Arbeit dafür.",
    "Kündige an, dass sie gleich eine eigene Liste schreibt. Das ist die Vorarbeit für "
    "Lektion 5.4, und ohne sie steht sie dort vor einem leeren Feld.")

# ── 5.3 Was ein Skill werden sollte ──────────────────────────────────
F["l53-titel"] = lektionstitel("l53-titel", "5.3", "Welche Arbeit sich lohnt",
    "Nicht jede Aufgabe braucht einen Skill. Diese hier schon.",
    "Erzähl von einer Arbeit, die du früher jede Woche von Hand gemacht hast, und wie lange "
    "es gedauert hat, bis du sie endlich aufgeschrieben hast.")

F["l53-merkmale"] = folie("l53-merkmale",
    eyebrow("Lektion 5.3")
    + h2("Drei Merkmale")
    + reihe([
        karte("Du machst sie wieder", ["Mindestens dreimal ungefähr gleich.",
                                       "Einmalige Sachen lohnen sich nicht."]),
        karte("Sie hat eine Form", ["Du weisst, wie das Ergebnis aussehen soll.",
                                    "Sonst schreibst du die Form erst beim Bauen auf — auch gut."], ORANGE),
        karte("Sie nervt dich", ["Das ist das ehrlichste Merkmal.",
                                 "Was dich nervt, schiebst du auf."]),
      ]),
    "Die dritte Karte ist die, an der sie hängenbleiben soll. Was sie aufschiebt, ist fast "
    "immer der beste erste Skill.")

F["l53-liste"] = folie("l53-liste",
    eyebrow("Lektion 5.3")
    + h2("Deine Liste")
    + p("Halt das Video jetzt an und schreib auf, was du in einer normalen Woche mehrmals "
        "ungefähr gleich machst. Ohne zu sortieren, einfach untereinander.", 40)
    + p("Bei mir stand auf dieser Liste unter anderem: die Caption zu einem fertigen Beitrag, "
        "der Story-Bogen für den nächsten Tag, und die Frage, was diese Woche überhaupt "
        "ansteht.", 32, GEDAEMPFT),
    "Sag das mit dem Anhalten wirklich und lass danach zwei Sekunden Stille. "
    "Wer hier nichts aufschreibt, steht in 5.4 vor einem leeren Feld.")

F["l53-weiter"] = weiter("l53-weiter", "Als Nächstes",
    "Deinen ersten Skill bauen",
    "Such dir einen von deiner Liste aus. Am besten den, der dich am meisten nervt.",
    "Bitte sie, sich jetzt für einen zu entscheiden. Wer mit drei Ideen in die nächste "
    "Lektion geht, baut keinen davon.")

# ── 5.4 Bauen ────────────────────────────────────────────────────────
F["l54-titel"] = lektionstitel("l54-titel", "5.4", "Deinen ersten Skill bauen",
    "Von der Idee zur fertigen Datei, live mitgefilmt.",
    "Die ganze Lektion ist geteilter Bildschirm. Nimm eine Arbeit, die du selbst wirklich "
    "machst, damit die Zwischenschritte echt sind.")

F["l54-weg"] = folie("l54-weg",
    eyebrow("Lektion 5.4")
    + h2("Der Weg")
    + reihe([
        karte("1 · Beschreiben", ["Du erzählst der KI, was du regelmässig machst und wie das Ergebnis aussehen soll."]),
        karte("2 · Bauen lassen", ["Sie schreibt daraus den ersten Entwurf des Skills."], ORANGE),
        karte("3 · Ausprobieren", ["Einmal aufrufen und schauen, was herauskommt."]),
        karte("4 · Nachschärfen", ["Was dir nicht passt, wird zur Regel. Kommt in der nächsten Lektion."]),
      ]),
    "Sag beim vierten Schritt schon, dass der erste Entwurf nie sitzt. Das verhindert, "
    "dass sie beim ersten mittelmässigen Ergebnis aufgibt.")

F["l54-baukasten"] = folie("l54-baukasten",
    eyebrow("Lektion 5.4")
    + h2("Zwei Wege zum selben Ziel")
    + gegenueber(
        "Mit dem Baukasten",
        ["Es gibt einen eingebauten Helfer, der dich durch die sechs Teile führt.",
         "Schneller, und du vergisst keinen Teil.",
         "Gut für den ersten."],
        "Von Hand",
        ["Du kopierst das leere Gerüst und füllst es aus.",
         "Dauert länger und du verstehst dabei mehr.",
         "Gut ab dem zweiten."]),
    "Zeig beide, aber nimm für die Aufnahme den Baukasten. Wer zuschaut, soll ein "
    "Erfolgserlebnis haben und nicht eine Schreibübung.")

F["l54-satz"] = statement("l54-satz",
    ["Der erste Entwurf", "ist nie der richtige.", "Das ist kein Fehler,", "das ist der Ablauf."],
    "Du baust, probierst aus, schärfst nach. Dreimal, dann sitzt es.",
    "Genau hier steigen Leute aus, weil das erste Ergebnis mittelmässig ist. "
    "Sag vorher, dass das so gehört.")

F["l54-weiter"] = weiter("l54-weiter", "Als Nächstes",
    "Von Hand nachschärfen",
    "Jetzt machst du aus einem brauchbaren Skill deinen eigenen.",
    "Kurze Brücke. Der Unterschied zwischen brauchbar und deinem ist die nächste Lektion.")

# ── 5.5 Nachschärfen ─────────────────────────────────────────────────
F["l55-titel"] = lektionstitel("l55-titel", "5.5", "Von Hand nachschärfen",
    "Was ein Baukasten nie wissen kann: deine Regeln und deine Verbote.",
    "Zeig einen deiner echten Skills und scroll zu den Regeln. Dass dort zwanzig Zeilen "
    "stehen, sagt mehr als jede Erklärung.")

F["l55-regeln"] = folie("l55-regeln",
    eyebrow("Lektion 5.5")
    + h2("Wo du ansetzt")
    + liste([
        "<b>Was dich am Ergebnis gestört hat</b> — zu lang, zu glatt, falscher Einstieg.",
        "<b>Was immer gleich sein soll</b> — die Anrede, die Länge, wie es endet.",
        "<b>Was nie vorkommen darf</b> — Wörter, Behauptungen, Versprechen.",
        "<b>Woran du erkennst, dass es gut ist</b> — zwei bis fünf Fragen zum Abhaken.",
      ], 34),
    "Der letzte Punkt ist der, den kaum jemand macht und der am meisten bringt. "
    "Ein Skill, der sich selbst prüft, liefert anders ab.")

F["l55-verbote"] = folie("l55-verbote",
    eyebrow("Lektion 5.5")
    + h2("Verbote sind wichtiger als Vorgaben")
    + p("Was sie tun soll, findet sie meistens selbst heraus. Was sie auf keinen Fall tun "
        "soll, weiss sie nur, wenn es dort steht.", 40)
    + p("Bei mir steht in jedem Text-Skill, welche Wörter nie vorkommen dürfen. Ohne diese "
        "Liste schreibt jede KI dieselben drei Floskeln, die man ihr auf zwei Absätze "
        "anmerkt.", 34, GEDAEMPFT),
    "Verweis auf Modul 2, Lektion 2.2. Hier schliesst sich der Kreis: Was sie dort erkannt "
    "hat, wird jetzt zur Regel im Skill.")

F["l55-weiter"] = weiter("l55-weiter", "Als Nächstes",
    "Was dreimal korrigiert wird, wird eine Regel",
    "Der Punkt, an dem ein Skill anfängt, besser zu werden als du an einem müden Tag.",
    "Kurze Brücke, aber mach neugierig. Das ist der Gedanke, der den ganzen Kurs trägt.")

# ── 5.6 Dreimal ──────────────────────────────────────────────────────
F["l56-titel"] = lektionstitel("l56-titel", "5.6", "Dreimal korrigiert,<br>dann eine Regel",
    "Wie ein Skill über Monate besser wird.",
    "Erzähl hier einen deiner echten Fehler und die Regel, die daraus wurde. "
    "Ein Beispiel trägt die ganze Lektion.", groesse=78)

F["l56-ablauf"] = folie("l56-ablauf",
    eyebrow("Lektion 5.6")
    + h2("Wie das im Alltag aussieht")
    + liste([
        "Du rufst den Skill auf und korrigierst am Ergebnis dieselbe Kleinigkeit.",
        "Beim zweiten Mal ärgert es dich.",
        "<b>Beim dritten Mal schreibst du es als Regel in den Skill.</b>",
        "Ab dem vierten Mal passiert es nicht mehr.",
      ], 34),
    "Der Trick ist, es nicht zu verschieben. Die Regel zu schreiben dauert zwei Minuten, "
    "die Korrektur jedes Mal fünf.")

F["l56-satz"] = statement("l56-satz",
    ["Ein Skill, der ein Jahr alt ist,", "weiss mehr über dein Business", "als jede neue KI."],
    "Weil jede Regel darin aus einem Fehler entstanden ist, den du nicht nochmal machen willst.",
    "Das ist der Satz, der erklärt, warum sich der ganze Aufwand lohnt. "
    "Lass ihn stehen.")

F["l56-weiter"] = weiter("l56-weiter", "Als Nächstes",
    "Achtung bei Skills aus dem Internet",
    "Es gibt fertige Skills zum Herunterladen. Worauf du vorher schaust.",
    "Kurze Brücke, aber ernst im Ton. Das ist ein Sicherheitsthema und kein Nebensatz.")

# ── 5.7 Fremde Skills ────────────────────────────────────────────────
F["l57-titel"] = lektionstitel("l57-titel", "5.7", "Skills aus dem Internet",
    "Du lädst fremde Anweisungen in deinen Arbeitsplatz.",
    "Sag gleich, dass es gute fremde Skills gibt und dass du selbst welche benutzt. "
    "Es geht ums Hinschauen, nicht ums Abraten.")

F["l57-pruefen"] = folie("l57-pruefen",
    eyebrow("Lektion 5.7")
    + h2("Worauf du schaust")
    + liste([
        "<b>Lies ihn, bevor du ihn benutzt.</b> Es ist eine Textdatei, du verstehst sie.",
        "<b>Was darf er anfassen?</b> Nur lesen ist harmlos, ändern und löschen nicht.",
        "<b>Schickt er etwas weg?</b> Alles, was Daten nach draussen gibt, gehört geprüft.",
        "<b>Woher kommt er?</b> Bei einem Skill aus einer unbekannten Quelle bist du "
        "vorsichtiger als bei einem aus einem Kurs, den du gekauft hast.",
      ], 31),
    "Der erste Punkt ist der wichtigste und der einfachste. Viele laden etwas herunter, "
    "ohne je hineinzuschauen — dabei steht dort ganz normaler Text.")

F["l57-satz"] = statement("l57-satz",
    ["Ein Skill ist eine Anweisung,", "die deine KI befolgt.", "Lies sie, bevor du sie gibst."],
    "Das dauert zwei Minuten und erspart dir den Rest.",
    "Kurz und bestimmt, ohne Drohton. Sag dazu, dass du selbst fremde Skills benutzt "
    "und jeden einmal ganz gelesen hast, bevor er bei dir gelaufen ist.")

# ── 5.8 Zusammenfassung ──────────────────────────────────────────────
F["l58-titel"] = lektionstitel("l58-titel", "5.8", "Zusammenfassung",
    "Was jetzt bei dir steht — und was du ab hier immer wieder tun wirst.",
    "Kurze Lektion, aber sag deutlich, dass Modul 5 das Handwerk war und alles ab Modul 6 "
    "nur noch Anwendung davon ist.")

F["l58-bilanz"] = folie("l58-bilanz",
    eyebrow("Lektion 5.8")
    + h2("Das nimmst du mit")
    + reihe([
        karte("Ein eigener Skill", ["Für eine Arbeit, die du wirklich jede Woche machst."]),
        karte("Eine Liste", ["Mit den nächsten, die du bauen willst."], ORANGE),
        karte("Eine Gewohnheit", ["Was dich dreimal stört, wird zur Regel."]),
      ]),
    "Die dritte Karte ist die, die sie in einem Jahr noch benutzt. Alles andere ist Werkzeug.")

F["l58-checkliste"] = checkliste("l58-checkliste", "5.8", [
    "Ich kann sagen, was ein Skill ist und woraus er besteht",
    "Ich habe eine Liste mit Arbeiten, die ich dreimal gleich mache",
    "Ich habe einen eigenen Skill gebaut",
    "Ich habe ihn einmal von Hand nachgeschärft",
    "Ich weiss, worauf ich bei fremden Skills schaue",
  ], 5,
  "Beim dritten Punkt nicht weichspülen. Wer hier keinen eigenen Skill hat, hat das "
  "Modul angeschaut statt gemacht.")

F["l58-weiter"] = folie("l58-weiter",
    eyebrow("Modul 6", ORANGE)
    + ('<h2 style="font-family:%s; font-size:84px; font-weight:700; line-height:1.15; color:%s">'
       'Bots,<br>die von selbst laufen</h2>' % (DISPLAY, CREME))
    + p("Der Unterschied zwischen einem Skill und einem Bot ist klein: Beim Bot ruft ihn "
        "niemand mehr auf.", 36, PETROL),
    "Ein Satz reicht. Modul 6 ist für viele der Punkt, an dem es sich zum ersten Mal wie "
    "Zauberei anfühlt.",
    stil=SEK_DUNKEL, uebergang="push")


ORDER = ["cover",
 "l51-titel","l51-rezept","l51-warum","l51-weiter",
 "l52-titel","l52-teile","l52-genau","l52-weiter",
 "l53-titel","l53-merkmale","l53-liste","l53-weiter",
 "l54-titel","l54-weg","l54-baukasten","l54-satz","l54-weiter",
 "l55-titel","l55-regeln","l55-verbote","l55-weiter",
 "l56-titel","l56-ablauf","l56-satz","l56-weiter",
 "l57-titel","l57-pruefen","l57-satz",
 "l58-titel","l58-bilanz","l58-checkliste","l58-weiter"]

SECTIONS = {
 "auftakt": {"description": "Worum es in Modul 5 geht.", "start": "cover"},
 "l51": {"description": "Lektion 5.1 — was ein Skill ist.", "start": "l51-titel"},
 "l52": {"description": "Lektion 5.2 — ein Skill Zeile für Zeile.", "start": "l52-titel"},
 "l53": {"description": "Lektion 5.3 — welche Arbeit sich lohnt.", "start": "l53-titel"},
 "l54": {"description": "Lektion 5.4 — den ersten Skill bauen.", "start": "l54-titel"},
 "l55": {"description": "Lektion 5.5 — von Hand nachschärfen.", "start": "l55-titel"},
 "l56": {"description": "Lektion 5.6 — aus Korrekturen werden Regeln.", "start": "l56-titel"},
 "l57": {"description": "Lektion 5.7 — Vorsicht bei fremden Skills.", "start": "l57-titel"},
 "l58": {"description": "Lektion 5.8 — Bilanz und Checkliste vor Modul 6.", "start": "l58-titel"},
}

schreibe(ZIEL, "Modul 5 — Skills", F, ORDER, SECTIONS)
