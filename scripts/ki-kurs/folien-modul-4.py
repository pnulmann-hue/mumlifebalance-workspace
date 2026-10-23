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
        ["Du hast einen eigenen Platz, der dir gehört.",
         "Alles liegt beisammen und wächst weiter.",
         "Sie darf deine Programme benutzen, nicht nur deine Dateien."]),
    "Die linke Spalte nimmt die Angst, die rechte macht neugierig. Geh sie in dieser "
    "Reihenfolge durch. Bei der rechten nicht sagen, dass es das vorher nicht gab — "
    "Dateien und eigene Befehle kann die Stufe davor inzwischen auch. Der Unterschied "
    "ist, dass hier ein Platz entsteht, der bleibt und über Monate wächst, statt "
    "einzelner Gespräche. Und dass sie bei dir rechnet: ein Video schneiden, Bilder "
    "herstellen, eine Seite bauen — das macht deine Maschine.")

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
    "Jeder Klick in der Reihenfolge, in der er kommt.",
    "🚨 Die Erstanmeldung kannst du nicht nachspielen — dein Konto läuft seit Monaten, und "
    "den Upgrade-Hinweis sieht nur, wer keines hat. Sag das offen: „Diesen Teil zeige ich "
    "dir auf den Folien, weil mein Konto schon steht.“ Ab der Ordnerwahl bist du wieder am "
    "Bildschirm — einen neuen, leeren Ordner aufmachen kannst du jederzeit.")

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

F["l42-anmelden"] = folie("l42-anmelden",
    eyebrow("Lektion 4.2")
    + h2("Installieren und anmelden")
    + liste([
        "<b>Herunterladen.</b> Es gibt je eine Fassung für Mac und für Windows. "
        "Datei öffnen, durchklicken, fertig.",
        "<b>App starten und anmelden</b> — mit demselben Konto, mit dem du im Chat "
        "arbeitest.",
        "<b>Oben auf den Reiter „Code“ klicken.</b> Links ist der Chat, daneben Cowork, "
        "daneben Code. Das sind die drei Stufen aus Modul 1, in einer App.",
      ], 32)
    + p("Die App bringt alles mit. Du installierst nichts weiter — kein Programm mit "
        "fremdem Namen, keine Kommandozeile.", 30, PETROL),
    "Die drei Reiter nebeneinander sind der beste Moment, um die Roadmap aus Modul 1 noch "
    "einmal zu zeigen: dieselbe App, drei Stufen. Das kannst du am Bildschirm zeigen, auch "
    "ohne neu anzumelden.")

F["l42-meldung"] = folie("l42-meldung",
    eyebrow("Lektion 4.2")
    + h2("Wenn beim ersten Mal eine Meldung kommt")
    + reihe([
        karte("„Upgrade nötig“", ["Der Reiter Code braucht ein bezahltes Abo.",
                                  "Welches, steht in Lektion 1.4."]),
        karte("„Melde dich online an“", ["Im Browser fertig anmelden,",
                                         "danach die App einmal",
                                         "schliessen und neu öffnen."], ORANGE),
        karte("Eine Fehlernummer", ["Zeig ihr die Meldung im Wortlaut",
                                    "und frag, was sie bedeutet.",
                                    "Das ist der Handgriff für alles."]),
      ])
    + beilage("Alle drei stehen im Setup-FAQ unter diesem Video — zusammen mit den Fragen, "
              "die beim Einrichten am häufigsten kommen."),
    "🚨 Diese Folie ersetzt das, was du nicht vorführen kannst. Geh die drei Karten ruhig "
    "durch und sag bei jeder, woran man sie erkennt. Die dritte ist die wichtigste: nicht "
    "selbst rätseln, sondern die Meldung hinkopieren und fragen.")

F["l42-schritte"] = folie("l42-schritte",
    eyebrow("Lektion 4.2")
    + h2("Deine erste Sitzung")
    + reihe([
        karte("1 · Auf diesem Rechner", ["Unter dem Eingabefeld steht eine Zeile",
                                         "mit Knöpfen. Der erste fragt, wo",
                                         "gearbeitet wird — du nimmst",
                                         "deinen eigenen Rechner."]),
        karte("2 · Ordner wählen", ["Der Knopf daneben: Ordner öffnen.",
                                    "Nimm den Platz, den du dir",
                                    "vorhin ausgesucht hast."], ORANGE),
        karte("3 · Erste Frage", ["Irgendetwas Einfaches.",
                                  zit("Was liegt in diesem Ordner?"),
                                  "Damit du siehst, dass sie",
                                  "wirklich hineinschaut."]),
      ])
    + beilage("Wenn etwas klemmt: Das Setup-FAQ liegt unter diesem Video — die zwölf Fragen, "
              "die beim Einrichten am häufigsten kommen."),
    "Ab hier bist du wieder am Bildschirm: Mach einen neuen, leeren Ordner auf und geh die "
    "drei Schritte wirklich durch. Das kannst du beliebig oft, auch mit bestehendem Konto. "
    "Wenn dabei etwas hakt, lass es drin und erklär es — genau das passiert ihr auch.")

F["l42-freigabe"] = folie("l42-freigabe",
    eyebrow("Lektion 4.2")
    + h2("Ein Knopf, den du gleich am Anfang kennen solltest")
    + p("In derselben Zeile unter dem Eingabefeld steht, wie viel sie ohne dich tun darf. "
        "Dieser Knopf entscheidet, ob du jede Änderung vorher siehst.", 36)
    + gegenueber(
        "Am Anfang",
        ["Stell ihn so ein, dass sie <b>fragt</b>, bevor sie eine Datei ändert.",
         "Du siehst jede Änderung und sagst Ja oder Nein.",
         "Langsamer — aber du verstehst, was passiert."],
        "Später",
        ["Wenn du Vertrauen hast, lässt du sie selbst machen.",
         "Dann steht hinterher da, was sie geändert hat,",
         "und du schaust es dir an."])
    + p("Es gibt auch eine Einstellung, in der sie nur einen Vorschlag schreibt und gar "
        "nichts anfasst. Die ist Gold wert, wenn du erst denken willst.", 30, PETROL),
    "Diese Folie habe ich dazugenommen, weil sie in keinem Anfängerkurs vorkommt und die "
    "erste Woche entscheidet. Wer mit „mach einfach“ anfängt, erschrickt beim ersten Mal. "
    "Zeig den Knopf am Bildschirm und schalt einmal hin und her.")

F["l42-weiter"] = weiter("l42-weiter", "Als Nächstes",
    "Dein Arbeitsplatz",
    "Wir schauen uns an, welche Ordner es gibt und wofür jeder da ist. Danach lädst du "
    "mein Grundgerüst herunter.",
    "Kurz halten, die Orientierung kommt auf der nächsten Folie. Sag nur, dass sie den Ordner "
    "nicht selbst anlegen muss — das nimmt schon hier Druck raus.")

# ── 4.3 Arbeitsplatz ─────────────────────────────────────────────────
F["l43-titel"] = lektionstitel("l43-titel", "4.3", "Dein Arbeitsplatz",
    "Fünf Ordner, und jeder hat genau eine Aufgabe.",
    "Diese Lektion läuft in zwei Hälften: erst die Folien durch — welcher Ordner wofür — "
    "und danach der Bildschirm, wo du dein Grundgerüst aufmachst und wir hineinschauen. "
    "Sag das vorher an, dann wartet niemand auf das Praktische, während du erklärst. Zeig "
    "am Bildschirm zuerst deinen eigenen Arbeitsplatz, dann das leere Gerüst — der "
    "Kontrast macht klar, wohin die Reise geht.")

F["l43-ordner"] = folie("l43-ordner",
    eyebrow("Lektion 4.3")
    + h2("Wo was hingehört")
    + liste([
        "<b>context</b> — dein Wissen. Der Business-Brief liegt hier, und alles, was die KI "
        "über dich wissen soll.",
        "<b>outputs</b> — was rauskommt. Captions, Folien, Pläne.",
        "<b>reference</b> — Material zum Nachschlagen, das du nicht selbst geschrieben hast.",
        "<b>scripts</b> — kleine Helfer, die immer dasselbe tun.",
        "<b>plans</b> — was sie vorhat, bevor sie es baut.",
      ], 30)
    + p("🚨 <b>Zwei füllst du, drei füllt sie.</b> In <b>context</b> und "
        "<b>reference</b> legst du etwas hinein. <b>outputs</b>, <b>plans</b> und "
        "<b>scripts</b> füllt sie — da musst du nichts tun.", 30, ORANGE),
    "Die Trennung von context und reference ist die wichtigste: Das eine ist deins, das "
    "andere hast du irgendwoher. 🚨 Und sag die orange Zeile wirklich — die Frage "
    "„was soll ich denn da reinschreiben?“ kommt bei plans und scripts garantiert, und "
    "die Antwort ist: nichts. Das macht sie.")

F["l43-zwei"] = folie("l43-zwei",
    eyebrow("Lektion 4.3")
    + h2("Die wichtigste Trennung im ganzen Arbeitsplatz")
    + gegenueber(
        "context — deins",
        ["Dein Business-Brief, deine Stimme, deine Tabus.",
         "Darf in deine Texte einfliessen.",
         "<b>Faustregel:</b> Was hier liegt, hast du geschrieben oder gesagt."],
        "reference — von anderen",
        ["Kursnotizen, Anleitungen, Vorlagen.",
         "Zum Nachschlagen, nicht zum Abschreiben.",
         "<b>Faustregel:</b> Was hier liegt, ist fremde Arbeit."])
    + p("🚨 Sie darf aus <b>reference</b> nie wörtlich abschreiben. Sonst landet fremder "
        "Text in deiner Caption — und du merkst es nicht.", 32, ORANGE)
    + p("Das ist die erste Regel, die du in deine Gedächtnis-Datei schreibst. Die kommt "
        "in der nächsten Lektion — merk dir den Satz bis dahin.", 28, GEDAEMPFT),
    "Das ist die Folie, die ich mir vor einem Jahr selbst gewünscht hätte. Bei mir lagen "
    "Kursunterlagen und eigene Notizen im selben Ordner. 🚨 Das Wort Gedächtnis-Datei "
    "fällt hier zum ersten Mal — sag in einem Halbsatz, was das ist: die eine Datei, die "
    "sie bei jedem Gespräch als Erstes liest. Hier nur erklären, am Bildschirm zeigen wir "
    "es gleich.")

F["l43-rest"] = folie("l43-rest",
    eyebrow("Lektion 4.3")
    + h2("Die drei anderen — und je eine Faustregel")
    + reihe([
        karte("outputs", ["Alles Fertige: Texte, Pläne, Listen.",
                          "<b>Kann weg</b>, ohne dass etwas kaputtgeht —",
                          "es lässt sich neu herstellen."]),
        karte("scripts", ["Kleine Programme, die stur",
                          "dasselbe tun. <b>Sie schreibt sie</b>,",
                          "wenn dich etwas zum dritten",
                          "Mal nervt."], ORANGE),
        karte("plans", ["Was sie vorhat, bevor sie baut.",
                        "<b>Sie schreibt den Plan</b>, du liest",
                        "ihn und sagst, was fehlt.",
                        "Spart den halben Nachmittag."]),
      ])
    + beilage("In jedem dieser Ordner liegt eine Liesmich-Datei. Du musst dir nichts "
              "merken — du machst den Ordner auf, und es steht drin."),
    "Nicht alle drei gleich lang besprechen. outputs versteht sich von selbst, scripts "
    "kommt in Modul 5 wieder, und bei plans sag den Satz mit dem halben Nachmittag — der "
    "bleibt hängen. Danach den Ordner am Bildschirm aufmachen und eine Liesmich zeigen.")

F["l43-geruest"] = folie("l43-geruest",
    eyebrow("Lektion 4.3")
    + h2("Das Grundgerüst")
    + p("Du musst das nicht selbst anlegen. Unter diesem Video liegt mein Gerüst mit allen "
        "Ordnern, einer vorbereiteten Gedächtnis-Datei und ein paar Befehlen zum Ausprobieren.", 38)
    + liste([
        "<b>1 · Leg den Ordner an einen Platz, den du wiederfindest.</b> "
        "Nicht in OneDrive, iCloud oder Dropbox.",
        "<b>2 · Füll die Gedächtnis-Datei aus.</b> Das ist die <b>CLAUDE.md</b> — die "
        "Datei, die sie bei jedem Gespräch als Erstes liest. Fünf Zeilen reichen für den "
        "Anfang, mehr dazu in der nächsten Lektion.",
        "<b>3 · Leg dein Wissen aus Kapitel 2 in context.</b> Vier Dateien, "
        "einfach hineinkopieren.",
      ], 30)
    + beilage("Das Grundgerüst liegt unter diesem Video — ZIP, einmal entpacken."),
    "Zeig den dritten Schritt wirklich. Der Moment, in dem sie merkt, dass die KI ihren "
    "Brief gelesen hat, ist der Moment, in dem Modul 2 sich auszahlt.")

F["l43-dateien"] = folie("l43-dateien",
    eyebrow("Lektion 4.3")
    + h2("Was du aus Kapitel 2 mitbringst")
    + reihe([
        karte("Dein Business-Brief", ["Die sechs Bausteine.",
                                      "Aus Lektion 2.3."]),
        karte("Die Buch-Technik", ["Was dabei herauskam,",
                                   "als sie dich gefragt hat.",
                                   "Aus Lektion 2.4."], ORANGE),
        karte("Deine Stimme", ["Die zwei, drei eigenen Texte.",
                               "Dazu deine Floskel-Liste.",
                               "Aus 2.5 und 2.2."]),
      ])
    + p("Alle vier in <b>context</b>, als einzelne Dateien. Liegt etwas als Word oder PDF "
        "vor, sag einfach: „Mach daraus eine Markdown-Datei.“", 30, PETROL),
    "Der wichtigste Satz hier: je eine eigene Datei, nicht alles in eine. Sie liest dann "
    "nur, was sie gerade braucht, und das hält die Antworten schneller und billiger. Sag "
    "dazu, wie ich meine benannt habe — business-brief, ueber-mich, meine-stimme, "
    "verbotene-woerter. Die Namen stehen auch im Grundgerüst in der Liesmich-Datei.")

F["l43-fragen"] = folie("l43-fragen",
    eyebrow("Lektion 4.3")
    + h2("Deine erste Sitzung: lass sie fragen")
    + p("Dein Arbeitsplatz steht. Der erste Auftrag stellt nichts her — er findet die "
        "Lücken und füllt sie.", 36)
    + p("„Schau dir alles an, was in context liegt. Sag mir zuerst, was du daraus "
        "schon über mich weisst. Dann stell mir eine Frage nach der anderen zu dem, "
        "was dir noch fehlt — und schreib meine Antworten selbst in die passende "
        "Datei.“", 32, PETROL)
    + gegenueber(
        "Du hast Kapitel 2 gemacht",
        ["Deine vier Dateien liegen in context.",
         "Sie fasst zusammen, was sie weiss —",
         "daran siehst du sofort, ob dein Brief taugt.",
         "Dann fragt sie nur noch, was fehlt."],
        "Du hast noch nichts drin",
        ["Dann geht derselbe Auftrag von vorne los.",
         "Sie fragt dich alles ab, eine Frage",
         "nach der anderen — und <b>legt die Dateien",
         "selbst an</b>. Du kopierst nichts."])
    + beilage("Der Auftrag steht als <b>Nummer 15</b> in deiner Prompt-Bibliothek — "
              "zum Kopieren, mit der Begründung zu jeder Zeile."),
    "Erst anschauen, dann fragen — sonst fragt sie nach Dingen, die längst im Brief "
    "stehen, und sie antworten zwanzig Minuten umsonst. Mach das live und lass sie "
    "wirklich ein paar Fragen stellen. Zwei Sachen dabei "
    "zeigen: dass sie zuerst zusammenfasst, was sie schon weiss, und dass sie deine "
    "Antworten selbst ablegt — du kopierst nichts. Antworte in ganzen Sätzen, so wie du "
    "reden würdest; wenn dir das Tippen zu lang dauert, sprich es ein und lass es "
    "umwandeln. 🚨 Die rechte Spalte ist wichtig für alle, die Kapitel 2 übersprungen "
    "haben: Derselbe Auftrag baut den Business-Brief auch von null auf. Dann dauert die "
    "erste Sitzung eine halbe Stunde — und danach steht alles.")

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

F["l44-wann"] = folie("l44-wann",
    eyebrow("Lektion 4.4")
    + h2("Was wird wann gelesen?")
    + reihe([
        karte("Die Gedächtnis-Datei", ["<b>Immer.</b>",
                                        "Bei jedem Gespräch,",
                                        "automatisch, ohne dass",
                                        "du etwas sagen musst.",
                                        "<b>Darum kurz halten.</b>"], ORANGE),
        karte("Die Dateien in context", ["<b>Wenn sie gebraucht werden.</b>",
                                         "Dein Business-Brief, deine",
                                         "Stimme, deine Tabus.",
                                         "<b>Hier darf es lang sein.</b>"]),
        karte("/start", ["<b>Wenn du es aufrufst.</b>",
                         "Dann schaut sie zusätzlich,",
                         "was zuletzt passiert ist",
                         "und was offen war."]),
      ])
    + p("🚨 Deine Antworten aus der Buch-Technik gehören <b>nicht</b> in die "
        "Gedächtnis-Datei. Dort steht nur der Verweis: „lies context/business-brief.md“. "
        "Alles, was mitgelesen wird, kostet bei jedem einzelnen Auftrag Zeit.", 30, ORANGE),
    "🚨 Das ist die Folie gegen den häufigsten Anfängerfehler: alles in die eine "
    "Datei schreiben, weil sie ja immer gelesen wird. Genau deshalb darf sie nicht lang "
    "werden. Das Bild dazu: Die Gedächtnis-Datei ist der Zettel am Kühlschrank, context "
    "ist der Aktenschrank. Auf dem Zettel steht, in welcher Schublade was liegt. Und sag "
    "den Unterschied zu /start deutlich — die Datei wird immer gelesen, /start ist der "
    "Tageseinstieg obendrauf.")

F["l44-regel"] = folie("l44-regel",
    eyebrow("Lektion 4.4")
    + h2("Wie sie wächst")
    + p("Du schreibst nicht alles auf einmal hinein. Du fängst mit fünf Zeilen an und "
        "ergänzt jedes Mal, wenn dich etwas zum dritten Mal geärgert hat.", 40)
    + p("Bei mir steht inzwischen jede Regel drin, die aus einem echten Fehler entstanden ist. "
        "Genau deshalb macht sie denselben Fehler kein viertes Mal.", 34, GEDAEMPFT)
    + beilage("Die leere Vorlage liegt unter diesem Video — sie steckt auch im Grundgerüst."),
    "Erzähl hier einen deiner eigenen Fehler und die Regel, die daraus wurde. "
    "Ein echtes Beispiel trägt die ganze Lektion.")

F["l44-satz"] = statement("l44-satz",
    ["Was dich dreimal ärgert,", "gehört als Regel hinein."],
    "Sonst ärgert es dich ein viertes Mal.",
    "Der Satz kommt in Modul 5 bei den Skills wieder. Setz ihn hier zum ersten Mal.")

# ── 4.4b Damit nichts verloren geht ──────────────────────────────────
F["l44b-titel"] = lektionstitel("l44b-titel", "4.4b", "Damit nichts verloren geht",
    "Dein Arbeitsplatz liegt auf deinem Rechner. Was passiert, wenn der kaputtgeht?",
    "Diese Frage kam in allen vier fremden Calls, die ich mir angeschaut habe, als "
    "häufigste — und sie wurde nirgends richtig beantwortet. Nimm dir die Zeit dafür.")

F["l44b-weg"] = folie("l44b-weg",
    eyebrow("Lektion 4.4b")
    + h2("Drei Arten, etwas zu verlieren")
    + reihe([
        karte("Das Gespräch", ["Du machst das Fenster zu,",
                               "und es ist weg.",
                               "Deshalb der Ordner."]),
        karte("Die Datei", ["Einmal überschrieben,",
                            "und die alte Fassung",
                            "gibt es nicht mehr."], ORANGE),
        karte("Der Rechner", ["Festplatte kaputt,",
                              "Laptop gestohlen.",
                              "Alles auf einmal."]),
      ])
    + p("Gegen das Erste hilft der Arbeitsplatz. Gegen die beiden anderen GitHub.",
        30, PETROL),
    "Die linke Karte haben sie schon verstanden — darum geht es seit Lektion 4.3. Die "
    "mittlere ist die, an die niemand denkt, und sie passiert am häufigsten. Erzähl, "
    "wenn du selbst einmal eine Fassung überschrieben hast, die du zurückhaben wolltest.")

F["l44b-was"] = folie("l44b-was",
    eyebrow("Lektion 4.4b")
    + h2("Was GitHub ist")
    + p("Ein Ort im Netz, an dem dein Arbeitsplatz zusätzlich liegt — und der sich "
        "zusätzlich merkt, was sich wann geändert hat.", 40)
    + p("Stell es dir vor wie eine Cloud für Ordner, die ein Gedächtnis hat. Du holst "
        "dir die Datei zurück — und auch die Fassung von vor drei Wochen.",
        34, GEDAEMPFT)
    + p("Es ist kostenlos, und du brauchst nichts davon zu verstehen. Du richtest es "
        "einmal ein und merkst danach nichts mehr davon.", 30, PETROL),
    "Das Wort Versionsverwaltung kommt hier nicht vor, und das ist Absicht. „Cloud mit "
    "Gedächtnis“ reicht völlig und bleibt hängen. Wer mehr wissen will, fragt nach.")

F["l44b-zwei"] = folie("l44b-zwei",
    eyebrow("Lektion 4.4b")
    + h2("Zwei Wörter, die sich ähnlich anhören")
    + gegenueber(
        "Git",
        ["Ein kleines Programm auf deinem Rechner.",
         "Es schreibt mit, was sich ändert.",
         "Auf dem Mac meistens schon da,",
         "unter Windows einmal installieren."],
        "GitHub",
        ["Der Ort im Netz, wo es dann liegt.",
         "Braucht ein Konto, kostenlos.",
         "Du siehst dort deine Dateien",
         "und wer wann was geändert hat."]),
    "Diese Verwechslung kostet in jedem Anfängerkurs eine halbe Stunde. Sag den Satz "
    "einmal ganz langsam: Git ist das Programm, GitHub ist der Ort. Wenn später die "
    "Meldung kommt „Git ist erforderlich“, wissen sie dann, was gemeint ist.")

F["l44b-schritte"] = folie("l44b-schritte",
    eyebrow("Lektion 4.4b")
    + h2("Du machst es nicht selbst")
    + p("Du musst weder Git installieren noch wissen, was ein Repository ist. Du sagst "
        "einfach, was du willst:", 34)
    + p("„Ich will meinen Arbeitsplatz bei GitHub sichern. Ich habe noch nie damit "
        "gearbeitet. Führ mich Schritt für Schritt durch, und sag mir bei jedem Schritt, "
        "was ich anklicken muss.“", 32, PETROL)
    + p("Sie prüft, was auf deinem Rechner fehlt, schickt dich für das Konto einmal auf "
        "die Webseite und macht den Rest selbst.", 30, GEDAEMPFT),
    "Zeig das live und lass die Antwort wirklich stehen, auch wenn es ein paar Schritte "
    "sind. Genau hier sehen sie zum ersten Mal, dass sie Technik nicht lernen müssen, "
    "sondern beschreiben.")

F["l44b-privat"] = folie("l44b-privat",
    eyebrow("Lektion 4.4b")
    + h2("Die eine Stelle, bei der du aufpassen musst")
    + p("Beim Anlegen fragt GitHub, ob dein Arbeitsplatz <b>öffentlich</b> oder "
        "<b>privat</b> sein soll.", 40)
    + p("Öffentlich heisst wirklich öffentlich. Jeder im Netz kann hineinschauen — in "
        "deinen Business-Brief, deine Preise, deine Kundinnen-Namen.", 34)
    + p("Du nimmst privat. Frag ausdrücklich danach und lass dir zeigen, wo das steht.",
        34, ORANGE)
    + beilage("Der Auftrag oben und die Warnung mit privat stehen auch in der Liesmich "
              "im Grundgerüst — unter „Damit nichts verloren geht“."),
    "Das ist die wichtigste Minute der Lektion. Erzähl, dass mir das selbst passiert ist "
    "und wie ich es gemerkt habe — ein offenes Verzeichnis sieht genauso aus wie ein "
    "geschlossenes, man sieht es nur an einer kleinen Zeile. Modul 10 kommt darauf "
    "zurück.")

F["l44b-weiter"] = weiter("l44b-weiter", "Als Nächstes",
    "Die Befehle, die schon drin liegen",
    "Zwei Abläufe, die du nur noch aufrufst — einer davon pflegt dein Gedächtnis.",
    "Kurze Brücke. Mach neugierig auf /shutdown: der Befehl, der abends aufräumt und "
    "mitschreibt.")

# ── 4.4c Die Befehle ──────────────────────
F["l44c-titel"] = lektionstitel("l44c-titel", "4.4c", "Zwei Befehle, die den Tag einrahmen",
    "Sie liegen im Grundgerüst schon drin. Hier erfährst du, was sie tun.",
    "Das ist die Lektion, die in keinem Anfängerkurs vorkommt, den ich kenne — und sie "
    "macht den Unterschied zwischen einem Ordner und einer Arbeitsweise. Ruf beide einmal "
    "live auf, auch wenn es etwas dauert.")

F["l44c-was"] = folie("l44c-was",
    eyebrow("Lektion 4.4c")
    + h2("Was ein Befehl ist")
    + gegenueber(
        "Ohne Befehl",
        ["Jedes Mal, wenn du anfängst:",
         zit("Lies bitte meine Gedächtnis-Datei, schau in context, sag mir, was letzte "
             "Woche offen war …"),
         "Fünf Sätze, jeden Tag neu getippt."],
        "Mit Befehl",
        ["Du tippst " + zit("/start") + " und sie macht genau das.",
         "Der Ablauf steht einmal in einer Datei.",
         "Ändern willst du etwas? Dann änderst du die Datei, nicht deine Gewohnheit."])
    + p("Ein Befehl ist ein Ablauf, den du einmal beschreibst und danach nur noch aufrufst. "
        "Genau dasselbe Prinzip wie ein Skill in Modul 5 — bei mir liegen die beiden "
        "sogar als Skills.", 30, PETROL),
    "Sag den letzten Satz ruhig so: Befehl und Skill sind dasselbe Prinzip, nur an "
    "verschiedenen Stellen abgelegt. Dann wundert sich in Modul 5 niemand über das Wort.")

F["l44c-paar"] = folie("l44c-paar",
    eyebrow("Lektion 4.4c")
    + h2("Morgens und abends")
    + reihe([
        karte("/start", ["Am Anfang jeder Sitzung.",
                         "Sie schaut, was im Arbeitsplatz liegt",
                         "und was zuletzt offen war.",
                         "Dann fragt sie: woran arbeiten wir heute?"]),
        karte("/shutdown", ["Am Ende jeder Sitzung.",
                            "Sie räumt auf, schreibt in die Gedächtnis-Datei,",
                            "was dazugelernt wurde,",
                            "und sichert alles."], ORANGE),
      ])
    + p("Ohne /shutdown wächst deine Gedächtnis-Datei nicht. Dann erklärst du ihr in vier "
        "Wochen wieder dasselbe wie heute.", 30, PETROL),
    "Das ist der wichtigste Satz der Lektion. Die Gedächtnis-Datei wächst nicht von "
    "selbst — sie wächst, weil abends jemand hineinschreibt. Erzähl, dass bei mir rund "
    "hundert Änderungen nie gesichert waren, weil ich den Befehl wochenlang nicht "
    "aufgerufen habe.")

F["l44c-mehr"] = folie("l44c-mehr",
    eyebrow("Lektion 4.4c")
    + h2("Und für alles, was grösser ist")
    + p("Erinner dich an „zu viel auf einmal“. Dagegen gibt es zwei weitere Befehle, die "
        "du aufrufen kannst, sobald ein Vorhaben grösser ist als ein Auftrag.", 36)
    + liste([
        "<b>/create-plan</b> — sie schreibt auf, was sie vorhat, in Schritten. Du liest "
        "es und sagst, was daran nicht stimmt. Erst dann wird gebaut.",
        "<b>/implement</b> — arbeitet den Plan ab, Schritt für Schritt, und hakt ihn ab. "
        "Du siehst nach jedem Schritt, wo sie steht.",
      ], 32)
    + p("Der Plan bleibt als Datei in <b>plans</b> liegen. Du kannst in drei Wochen "
        "nachlesen, warum etwas so gebaut wurde.", 30, GEDAEMPFT)
    + beilage("Alle vier Befehle liegen im Grundgerüst aus Lektion 4.3 — du musst keinen "
              "davon schreiben."),
    "Nimm ein eigenes Beispiel, bei dem du ohne Plan angefangen hast und es danach zweimal "
    "umbauen musstest. Und sag klar: die ersten zwei brauchst du ab morgen, diese zwei "
    "erst, wenn etwas grösser wird. Sonst versucht sie alle vier gleichzeitig zu lernen.")

F["l44c-ablauf"] = folie("l44c-ablauf",
    eyebrow("Lektion 4.4c")
    + h2("Deine erste halbe Stunde — in dieser Reihenfolge")
    + liste([
        "<b>1 ·</b> Ordner entpackt an seinem Platz, nicht in der Cloud.",
        "<b>2 ·</b> Claude Code öffnen, Reiter <b>Code</b>, auf diesem Rechner, Ordner wählen.",
        "<b>3 ·</b> Den Freigabe-Knopf auf <b>fragen</b> stellen.",
        "<b>4 ·</b> " + zit("Was liegt in diesem Ordner?") + " — sie nennt die fünf Ordner. "
        "Jetzt weisst du, dass sie ihn sieht.",
        "<b>5 ·</b> Deine vier Dateien aus Kapitel 2 in <b>context</b> kopieren. "
        "Im Datei-Fenster, nicht in Claude.",
        "<b>6 ·</b> Der grosse Auftrag: lesen, zusammenfassen, dich ausfragen, "
        "die Antworten selbst ablegen. <b>Nummer 15</b> in der Prompt-Bibliothek.",
        "<b>7 ·</b> Die Gedächtnis-Datei schreiben lassen — <b>Nummer 16</b> in der "
        "Prompt-Bibliothek.",
        "<b>8 ·</b> " + zit("/shutdown") + " — damit du siehst, dass mitgeschrieben wird.",
      ], 28)
    + p("GitHub kommt noch nicht. Das richtest du ein, sobald hier etwas liegt, dessen "
        "Verlust dir wehtun würde.", 28, PETROL),
    "🚨 Das ist dein Drehbuch für den Bildschirmteil — geh es in genau dieser "
    "Reihenfolge durch. Zwei Stellen, bei denen die meisten stolpern: Schritt 5 passiert "
    "im Datei-Fenster, nicht im Chat (das sagt niemand, und alle versuchen es erst im "
    "Chat). Und Schritt 4 wirkt überflüssig, ist aber der Moment, in dem sie merken, "
    "dass sie im richtigen Ordner sind — die häufigste Ursache für "
    "„sie findet meine Dateien nicht“ ist ein falsch gewählter Ordner. Sag dazu, dass "
    "die halbe Stunde für Schritt 6 draufgeht und das gut angelegt ist.")

F["l44c-weiter"] = weiter("l44c-weiter", "Als Nächstes",
    "Wie du mit ihr sprichst",
    "Drei Gewohnheiten, die dir viel Nachbessern ersparen.",
    "Kurze Brücke — und ein letzter Satz zu den Befehlen: Sie sind der Beweis dafür, "
    "dass sich eine Arbeit beschreiben lässt. Genau das machen wir in Modul 5 mit deinen "
    "eigenen Arbeiten.")

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
        karte("Zwei Befehle", ["/start am Morgen,",
                               "/shutdown am Abend."]),
      ]),
    "Die dritte Karte ist die, die sie am ehesten wieder vergisst. Sag, dass sie in "
    "Modul 5 sofort wieder gebraucht wird.")

F["l47-downloads"] = downloads("l47-downloads", 4, [
    ("4.2", "Setup-FAQ — „Wenn beim Einrichten etwas klemmt“ (PDF)"),
    ("4.3", "Arbeitsplatz-Grundgerüst — ZIP mit den fünf Ordnern, je einer Liesmich, "
            "der Gedächtnis-Datei und den Befehlen"),
    ("4.4", "Die Gedächtnis-Datei einzeln, leer zum Ausfüllen"),
    ("4.4b", "GitHub-Anleitung — Klick für Klick"),
    ("4.7", "Checkliste Modul 4"),
  ],
  "Diese Folie ist für mich, nicht für sie: Beim Aufnehmen nenne ich jede Datei an ihrer "
  "Lektion, und hier sehe ich auf einen Blick, ob ich eine vergessen habe. Zum Schluss "
  "einmal durchgehen und sagen: Wenn du eine davon noch nicht hast, hol sie jetzt.")

F["l47-checkliste"] = checkliste("l47-checkliste", "4.7", [
    "Claude Code läuft bei mir und ich komme hinein",
    "Ich habe das Grundgerüst heruntergeladen und geöffnet",
    "Ich weiss, wofür jeder Ordner da ist",
    "Meine Gedächtnis-Datei ist ausgefüllt",
    "Ich habe einen Auftrag gegeben, der durchgelaufen ist",
    "Ich habe /start und /shutdown einmal ausprobiert",
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
 "l42-titel","l42-vorher","l42-anmelden","l42-meldung","l42-schritte","l42-freigabe",
 "l42-weiter",
 "l43-titel","l43-ordner","l43-zwei","l43-rest","l43-geruest","l43-dateien",
 "l43-fragen","l43-weiter",
 "l44-titel","l44-was","l44-wann","l44-regel","l44-satz",
 "l44b-titel","l44b-weg","l44b-was","l44b-zwei","l44b-schritte","l44b-privat","l44b-weiter",
 "l44c-titel","l44c-was","l44c-paar","l44c-mehr","l44c-ablauf","l44c-weiter",
 "l45-titel","l45-regeln","l45-beispiel","l45-weiter",
 "l46-titel","l46-fehler","l46-neu","l46-satz",
 "l47-titel","l47-bilanz","l47-downloads","l47-checkliste","l47-weiter"]

SECTIONS = {
 "auftakt": {"description": "Worum es in Modul 4 geht.", "start": "cover"},
 "l41": {"description": "Lektion 4.1 — warum das kein Programmieren ist.", "start": "l41-titel"},
 "l42": {"description": "Lektion 4.2 — einrichten, Schritt für Schritt.", "start": "l42-titel"},
 "l43": {"description": "Lektion 4.3 — die Ordner und das Grundgerüst.", "start": "l43-titel"},
 "l44": {"description": "Lektion 4.4 — die Gedächtnis-Datei.", "start": "l44-titel"},
 "l44b": {"description": "Lektion 4.4b — Sicherung mit GitHub.", "start": "l44b-titel"},
 "l44c": {"description": "Lektion 4.4c — die Befehle aus dem Grundgerüst.", "start": "l44c-titel"},
 "l45": {"description": "Lektion 4.5 — wie man mit ihr spricht.", "start": "l45-titel"},
 "l46": {"description": "Lektion 4.6 — was tun, wenn es nicht klappt.", "start": "l46-titel"},
 "l47": {"description": "Lektion 4.7 — Bilanz und Checkliste vor Modul 5.", "start": "l47-titel"},
}

schreibe(ZIEL, "Modul 4 — Dein Arbeitsplatz", F, ORDER, SECTIONS)
