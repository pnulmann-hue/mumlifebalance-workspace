#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Baut die Folien fuer Modul 1 des Kurses „Claude Code fuer Network-Mamas".

    python scripts/ki-kurs/folien-modul-1.py <zielordner>

Schreibt <zielordner>/project/deck.json und <zielordner>/project/slides/*.html
im Folienformat des Slides-Typs. Wiederholbar.
"""
import io, json, os, sys

ZIEL = sys.argv[1] if len(sys.argv) > 1 else "folien-modul-1"

# ── Marke ────────────────────────────────────────────────────────────
GRUND   = "#f7f4ec"   # Creme, leicht getont
CREME   = "#f1ecdd"
BLAU    = "#29556d"   # Dunkelblau
PETROL  = "#12828c"
ORANGE  = "#dc822e"
TINTE   = "#0c1c30"
GEDAEMPFT = "#5c6b73"
HELL    = "#fdfcf8"

DISPLAY = "'Philosopher', Georgia, serif"
TEXT    = "'Source Sans 3', Verdana, sans-serif"

SEK = ("background:%s; color:%s; font-family:%s; padding:128px; "
       "display:flex; flex-direction:column; gap:40px") % (GRUND, TINTE, TEXT)
SEK_DUNKEL = ("background:%s; color:%s; font-family:%s; padding:128px; "
              "display:flex; flex-direction:column; justify-content:center; gap:32px") % (BLAU, CREME, TEXT)

def eyebrow(t, farbe=PETROL):
    return ('<p style="font-size:26px; font-weight:600; letter-spacing:3px; '
            'text-transform:uppercase; color:%s">%s</p>' % (farbe, t))

def h2(t, farbe=BLAU, groesse=72):
    return ('<h2 style="font-family:%s; font-size:%dpx; font-weight:700; '
            'line-height:1.1; color:%s">%s</h2>' % (DISPLAY, groesse, farbe, t))

def p(t, groesse=32, farbe=None, gewicht=400):
    return ('<p style="font-size:%dpx; font-weight:%d; line-height:1.45; color:%s">%s</p>'
            % (groesse, gewicht, farbe or TINTE, t))

def liste(punkte, groesse=32):
    z = "".join('<li style="line-height:1.5">%s</li>' % x for x in punkte)
    return ('<ul style="font-size:%dpx; color:%s; display:flex; flex-direction:column; gap:18px">%s</ul>'
            % (groesse, TINTE, z))

def karte(titel, zeilen, akzent=PETROL):
    inhalt = "".join('<p style="font-size:28px; line-height:1.45; color:%s">%s</p>' % (TINTE, z) for z in zeilen)
    return ('<div style="flex:1; display:flex; flex-direction:column; gap:14px; background:%s; '
            'padding:36px; border-radius:18px; border-top:6px solid %s">'
            '<h3 style="font-family:%s; font-size:38px; font-weight:700; color:%s">%s</h3>%s</div>'
            % (HELL, akzent, DISPLAY, BLAU, titel, inhalt))

def reihe(karten, abstand=32):
    return '<div style="display:flex; gap:%dpx; align-items:stretch">%s</div>' % (abstand, "".join(karten))

def folie(sid, inhalt, notiz, stil=None, uebergang="fade"):
    s = stil or SEK
    a = '<aside>%s</aside>' % notiz if notiz else ""
    return '<section id="%s" data-transition="%s" style="%s">%s%s</section>' % (sid, uebergang, s, inhalt, a)


FOLIEN = {}

# ── Auftakt ──────────────────────────────────────────────────────────
FOLIEN["cover"] = folie("cover",
    eyebrow("Claude Code für Network-Mamas", ORANGE)
    + ('<h1 style="font-family:%s; font-size:132px; font-weight:700; line-height:1.05; color:%s">'
       'Modul 1<br>Orientierung</h1>' % (DISPLAY, CREME))
    + p("Wo die Reise hingeht, was die Wörter bedeuten und was dich das im Monat kostet.", 38, CREME)
    + '<div style="flex:1"></div>'
    + p("Patricia Ulmann · Mum Life Balance", 26, PETROL),
    "Ruhig anfangen. Kein Intro-Gedudel. Sag in einem Satz, dass wir hier noch nichts installieren, "
    "sondern uns zuerst orientieren. Das nimmt Druck raus.",
    stil=SEK_DUNKEL)

# ── Lektion 1.1 ──────────────────────────────────────────────────────
FOLIEN["l11-titel"] = folie("l11-titel",
    eyebrow("Lektion 1.1")
    + h2("Schön, dass du da bist", BLAU, 88)
    + p("Was am Ende dieses Kurses bei dir steht — und warum ich von einer Mitarbeiterin rede.", 38, GEDAEMPFT),
    "Hier stellst du dich nicht vor, das kennt sie schon. Geh direkt darauf ein, warum sie hier sitzt: "
    "Sie benutzt KI wahrscheinlich schon und ärgert sich über die Ergebnisse.")

FOLIEN["l11-ergebnis"] = folie("l11-ergebnis",
    eyebrow("Lektion 1.1")
    + h2("Das hast du am Ende")
    + reihe([
        karte("Ein Arbeitsplatz", ["An dem dein eigenes Wissen liegt, statt dass du es jedes Mal neu tippst."]),
        karte("Ein eigener Befehl", ["Für eine Arbeit, die du jede Woche sowieso machst."], ORANGE),
        karte("Ein Bot, der läuft", ["Er schreibt dir morgens, auch wenn dein Laptop zu ist."]),
      ]),
    "Diese drei Sachen sind das Versprechen des Kurses. Nenn sie konkret und lass sie stehen — "
    "sie kommen in Modul 10 nochmal, dann als Bilanz.")

FOLIEN["l11-bild"] = folie("l11-bild",
    ('<h2 style="font-family:%s; font-size:96px; font-weight:700; line-height:1.15; color:%s">'
     'Du stellst dir keine<br>Software hin.<br>Du stellst jemanden ein.</h2>' % (DISPLAY, CREME))
    + p("Eine Praktikantin ist schnell, fleissig und weiss erschreckend viel. "
        "Sie kennt nur weder dich noch dein Business, solange du es ihr nicht sagst.", 34, PETROL),
    "Das ist das Bild, das durch den ganzen Kurs trägt. Erklär kurz, warum es passt: "
    "eine Praktikantin bekommt eine Einführung, Beispiele und Regeln. Genau das bauen wir in Modul 2.",
    stil=SEK_DUNKEL, uebergang="push")

FOLIEN["l11-abgrenzung"] = folie("l11-abgrenzung",
    eyebrow("Lektion 1.1")
    + h2("Drei Dinge vorweg")
    + liste([
        "<b>Du musst nichts programmieren.</b> Du schreibst Deutsch. Das schwarze Fenster, "
        "das du vielleicht mal auf einem Screenshot gesehen hast, brauchst du hier nicht.",
        "<b>Wir gehen über drei Stufen, und auf jeder gibt es ein Ergebnis.</b> "
        "Wer nach der ersten aufhört, hat trotzdem etwas, das sie behält.",
        "<b>Ich habe das neben vier Kindern gelernt</b>, mit achtzehn Stunden Woche und "
        "ohne technische Ausbildung.",
      ], 34),
    "Die drei Punkte nehmen die drei häufigsten Ausreden vorweg. Sag den dritten ohne Pathos — "
    "als Tatsache, nicht als Motivationsspruch.")

FOLIEN["l11-weiter"] = folie("l11-weiter",
    eyebrow("Als Nächstes", ORANGE)
    + h2("Deine Roadmap — die drei Stufen")
    + p("In der nächsten Lektion schauen wir uns an, welche Stufe bei dir gerade dran ist. "
        "Und warum niemand bis ganz nach oben muss.", 36, GEDAEMPFT),
    "Kurze Brücke, höchstens zwanzig Sekunden. Nicht zusammenfassen, was gerade war.")

# ── Lektion 1.2 ──────────────────────────────────────────────────────
FOLIEN["l12-titel"] = folie("l12-titel",
    eyebrow("Lektion 1.2")
    + h2("Deine Roadmap", BLAU, 88)
    + p("Chat, Cowork, Code. Drei Stufen — und auf jeder ein Ergebnis, das du behältst.", 38, GEDAEMPFT),
    "Sag gleich am Anfang, dass sie sich hier für eine Stufe entscheidet und nicht für den ganzen Weg.")

FOLIEN["l12-uebersicht"] = folie("l12-uebersicht",
    eyebrow("Lektion 1.2")
    + h2("Die drei Stufen")
    + reihe([
        karte("1 · Claude Chat", ["Deine KI klingt nach dir.", "Gratis-Konto reicht zum Anfangen."]),
        karte("2 · Claude Cowork", ["Sie arbeitet mit deinen Dateien.", "Dein erster Bot, ohne Code."], ORANGE),
        karte("3 · Claude Code", ["Eigener Arbeitsplatz, eigene Befehle.", "Ein Bot, der von selbst läuft."]),
      ]),
    "Geh die drei einmal von links nach rechts durch, je zwanzig Sekunden. "
    "Die Einzelheiten kommen gleich auf den nächsten Folien.")

FOLIEN["l12-stufe1"] = folie("l12-stufe1",
    eyebrow("Stufe 1 · Claude Chat")
    + h2("Deine KI klingt nach dir")
    + liste([
        "<b>Was du benutzt:</b> den ganz normalen Chat im Browser oder auf dem Handy.",
        "<b>Was du danach kannst:</b> dein eigenes Wissen liegt als Projekt dort, "
        "statt in jedem Gespräch neu getippt zu werden.",
        "<b>Woran du merkst, dass sie dran ist:</b> du benutzt KI schon und baust jedes Ergebnis um.",
      ], 34),
    "Das ist die Stufe, auf der die meisten stehen, ohne es zu wissen. "
    "Betone den letzten Punkt — daran erkennt sie sich wieder.")

FOLIEN["l12-stufe2"] = folie("l12-stufe2",
    eyebrow("Stufe 2 · Claude Cowork")
    + h2("Sie arbeitet mit deinen Sachen")
    + liste([
        "<b>Was dazukommt:</b> Dateien, eine Verbindung zu deiner Planung, mehrere Schritte am Stück.",
        "<b>Was du danach hast:</b> einen Bot, den du ohne eine Zeile Code gebaut hast.",
        "<b>Wo sie aufhört:</b> Er läuft nicht von selbst. Du musst ihn jedes Mal anstossen.",
      ], 34),
    "Der letzte Punkt ist wichtig und wird oft verschwiegen. Sag ihn offen — "
    "er ist der ehrliche Grund für Stufe 3 und nimmt den Verkaufsdruck raus.")

FOLIEN["l12-stufe3"] = folie("l12-stufe3",
    eyebrow("Stufe 3 · Claude Code")
    + h2("Dein eigener Arbeitsplatz")
    + liste([
        "<b>Was du benutzt:</b> die Desktop-App. Kein schwarzes Fenster, du schreibst weiter Deutsch.",
        "<b>Was du danach kannst:</b> eigene Befehle für Arbeiten, die du jede Woche machst.",
        "<b>Und:</b> ein Bot, der morgens von selbst schreibt, auch wenn dein Laptop zu ist.",
      ], 34),
    "Hier kommt die häufigste Angst: das sei doch Programmieren. Nimm sie direkt vorweg, "
    "in einem Satz, und zeig es in Modul 4 statt es hier zu beweisen.")

FOLIEN["l12-satz"] = folie("l12-satz",
    ('<h2 style="font-family:%s; font-size:92px; font-weight:700; line-height:1.15; color:%s">'
     'Auf jeder Stufe<br>ein Gewinn.<br>Niemand muss bis nach oben.</h2>' % (DISPLAY, CREME))
    + p("📎 Die Roadmap zum Ausdrucken liegt unter diesem Video.", 32, PETROL),
    "Das ist der Satz, der die Angst nimmt. Lass ihn zwei Sekunden stehen, bevor du weitersprichst. "
    "Verweis am Schluss auf die Beilage.",
    stil=SEK_DUNKEL, uebergang="push")

# ── Lektion 1.3 ──────────────────────────────────────────────────────
FOLIEN["l13-titel"] = folie("l13-titel",
    eyebrow("Lektion 1.3")
    + h2("Die Wörter, die<br>dauernd vorkommen", BLAU, 82)
    + p("Einmal in Ruhe erklärt, so wie ich es einer Freundin am Küchentisch sagen würde.", 38, GEDAEMPFT),
    "Sag ehrlich, dass das der langweiligste Teil des Kurses ist und warum er trotzdem am Anfang steht: "
    "Ohne die Wörter versteht sie ab Modul 3 die Hälfte nicht.")

FOLIEN["l13-reden"] = folie("l13-reden",
    eyebrow("Beim Reden mit der KI")
    + h2("Auftrag, Kontext, Halluzination")
    + liste([
        "<b>Auftrag (Prompt)</b> — was du hineinschreibst. Drei Zutaten: wer du bist, "
        "was rauskommen soll, und ein Beispiel für gut.",
        "<b>Kontext</b> — alles, was sie gerade über dich weiss. Was nicht drinsteht, "
        "existiert für sie nicht.",
        "<b>Halluzination</b> — wenn sie etwas erfindet und dabei überzeugt klingt. "
        "Vor allem bei Zahlen, Namen und Links.",
      ], 32),
    "Beim dritten Punkt ein eigenes Beispiel erzählen, wenn dir eines einfällt. "
    "Das bleibt besser hängen als die Definition.")

FOLIEN["l13-dateien"] = folie("l13-dateien",
    eyebrow("Beim Arbeiten mit Dateien")
    + h2("Projekt, Arbeitsplatz, Business-Brief")
    + liste([
        "<b>Projekt</b> — ein Ort, an dem dein Wissen liegen bleibt.",
        "<b>Arbeitsplatz</b> — bei Claude Code ein Ordner auf deinem Rechner, in dem deine Dateien, "
        "dein Wissen und deine Befehle zusammenliegen.",
        "<b>CLAUDE.md</b> — die eine Datei darin, in der steht, was die KI immer wissen soll.",
        "<b>Business-Brief</b> — dein eigenes Wissensdokument. Geht bei jedem Auftrag mit.",
      ], 32),
    "Der Business-Brief kommt in Modul 2 ausführlich. Hier reicht der Satz, dass er das wichtigste "
    "Dokument im ganzen Kurs ist.")

FOLIEN["l13-automat"] = folie("l13-automat",
    eyebrow("Beim Automatisieren")
    + h2("Skill, Agent, Bot")
    + liste([
        "<b>Skill</b> — eine Arbeit, die du einmal aufschreibst und danach nur noch aufrufst.",
        "<b>Agent</b> — eine KI, die selbst arbeitet statt nur zu antworten, über mehrere Schritte: "
        "nachschauen, ändern, prüfen, weitermachen.",
        "<b>Bot</b> — dasselbe, nur dass ihn niemand mehr aufrufen muss.",
        "<b>Hosting</b> — der Ort, an dem dein Bot wohnt, damit er läuft, wenn du schläfst.",
      ], 32),
    "Der Unterschied zwischen Skill und Bot ist der, den die meisten nicht kennen. "
    "Eine Bemerkung reicht — Modul 6 zeigt es.")

FOLIEN["l13-terminal"] = folie("l13-terminal",
    ('<h2 style="font-family:%s; font-size:96px; font-weight:700; line-height:1.15; color:%s">'
     'Das schwarze Fenster<br>brauchst du hier nicht.</h2>' % (DISPLAY, CREME))
    + p("Falls du es irgendwo siehst: nicht erschrecken. Es ist nur eine andere Art, dasselbe zu tun.", 34, PETROL)
    + p("📎 Das Cheatsheet mit allen Wörtern liegt unter diesem Video.", 30, CREME),
    "Diese Folie ist die wichtigste der Lektion. Genau dieses Bild hält die meisten Frauen ab. "
    "Sag es klar und geh weiter, ohne dich zu rechtfertigen.",
    stil=SEK_DUNKEL, uebergang="push")

# ── Lektion 1.4 ──────────────────────────────────────────────────────
FOLIEN["l14-titel"] = folie("l14-titel",
    eyebrow("Lektion 1.4")
    + h2("Was das kostet", BLAU, 88)
    + p("Die Zahlen offen auf dem Tisch, damit du selbst rechnen kannst.", 38, GEDAEMPFT),
    "Kein Herumreden. Die Frage kommt sowieso, und wer sie offen beantwortet, wirkt glaubwürdiger.")

FOLIEN["l14-tabelle"] = folie("l14-tabelle",
    eyebrow("Lektion 1.4")
    + h2("Was auf welcher Stufe anfällt")
    + ('<table style="font-family:%s; font-size:30px; color:%s; border-radius:14px">'
       '<tr style="background:%s">'
       '<th style="width:26%%; padding:18px; text-align:left; color:%s">Stufe</th>'
       '<th style="width:40%%; text-align:left; color:%s">Was du brauchst</th>'
       '<th style="width:34%%; text-align:left; color:%s">Ungefähr im Monat</th></tr>'
       '<tr><td>1 · Chat</td><td>Konto</td><td>gratis zum Anfangen</td></tr>'
       '<tr style="background:%s"><td>2 · Cowork</td><td>Abo</td><td>rund 20 bis 23</td></tr>'
       '<tr><td>3 · Code</td><td>Abo plus Hosting für den Bot</td><td>Abo plus rund 5</td></tr>'
       '</table>' % (TEXT, TINTE, BLAU, CREME, CREME, CREME, HELL))
    + p("Alles in Franken, Stand heute. Bei den Anbietern ändert sich das gelegentlich — "
        "schau kurz nach, bevor du dich entscheidest.", 28, GEDAEMPFT),
    "Sag ausdrücklich, dass die Zahlen sich ändern können. Das schützt dich, wenn der Kurs "
    "in einem halben Jahr noch läuft.")

FOLIEN["l14-rechnung"] = folie("l14-rechnung",
    eyebrow("Lektion 1.4")
    + h2("Die Rechnung, die ich für mich gemacht habe")
    + p("Ein Abo kostet weniger als eine einzige Stunde bezahlte Hilfe. Die Frage ist also nicht, "
        "ob du es dir leisten kannst.", 40, TINTE)
    + p("Die Frage ist, ob du in dem Monat wirklich etwas damit machst. Wenn du gerade weisst, "
        "dass du keine Zeit hast: fang mit Stufe 1 an und lass das Abo, bis du dranbleibst.", 34, GEDAEMPFT),
    "Das ist der ehrliche Rat, den du selber gerne gehört hättest. Er kostet dich einen Verkauf "
    "und bringt dir Vertrauen.")

FOLIEN["l14-weiter"] = folie("l14-weiter",
    eyebrow("Als Nächstes", ORANGE)
    + h2("Zusammenfassung und Checkliste")
    + p("Wir schauen, was jetzt bei dir stehen sollte, bevor wir in Modul 2 an deinen "
        "Business-Brief gehen.", 36, GEDAEMPFT),
    "Kurze Brücke.")

# ── Lektion 1.5 ──────────────────────────────────────────────────────
FOLIEN["l15-titel"] = folie("l15-titel",
    eyebrow("Lektion 1.5")
    + h2("Zusammenfassung", BLAU, 88)
    + p("Was jetzt bei dir steht — und was du holst, bevor du weitergehst.", 38, GEDAEMPFT),
    "Ganz kurze Lektion, drei bis vier Minuten. Nicht alles nochmal erzählen.")

FOLIEN["l15-bilanz"] = folie("l15-bilanz",
    eyebrow("Lektion 1.5")
    + h2("Das nimmst du mit")
    + reihe([
        karte("Deine Stufe", ["Du weisst, ob bei dir gerade Chat, Cowork oder Code dran ist."]),
        karte("Die Wörter", ["Du verstehst, was Auftrag, Skill, Agent und Bot bedeuten."], ORANGE),
        karte("Die Kosten", ["Du weisst, was auf dich zukommt, und hast entschieden, womit du anfängst."]),
      ]),
    "Geh die drei Karten durch und frag nach jeder: Ist das bei dir wirklich so? "
    "Das ist die Überleitung zur Checkliste.")

FOLIEN["l15-checkliste"] = folie("l15-checkliste",
    eyebrow("Lektion 1.5")
    + h2("Bevor du weitermachst")
    + liste([
        "Ich weiss, welche der drei Stufen bei mir gerade dran ist",
        "Ich habe das Begriffe-Cheatsheet ausgedruckt oder offen",
        "Ich weiss, was mich das im Monat kostet, und habe entschieden, womit ich anfange",
        "Ich habe ein Konto und komme hinein",
      ], 34)
    + p("📎 Die Checkliste zum Abhaken liegt unter diesem Video.", 30, PETROL),
    "Bitte sie ausdrücklich, das jetzt zu machen und nicht später. Später heisst nie.")

FOLIEN["l15-weiter"] = folie("l15-weiter",
    eyebrow("Modul 2", ORANGE)
    + ('<h2 style="font-family:%s; font-size:84px; font-weight:700; line-height:1.15; color:%s">'
       'Claude Chat —<br>die Grundlage</h2>' % (DISPLAY, CREME))
    + p("Jetzt bringst du der KI bei, wer du bist. Das ist der Schritt, den die meisten überspringen "
        "und der hinterher alles entscheidet.", 36, PETROL),
    "Mach neugierig auf den Business-Brief, ohne ihn schon zu erklären. "
    "Ein Satz reicht: ohne ihn bleibt jeder Text austauschbar.",
    stil=SEK_DUNKEL, uebergang="push")


# ── Reihenfolge und Abschnitte ───────────────────────────────────────
ORDER = ["cover",
 "l11-titel","l11-ergebnis","l11-bild","l11-abgrenzung","l11-weiter",
 "l12-titel","l12-uebersicht","l12-stufe1","l12-stufe2","l12-stufe3","l12-satz",
 "l13-titel","l13-reden","l13-dateien","l13-automat","l13-terminal",
 "l14-titel","l14-tabelle","l14-rechnung","l14-weiter",
 "l15-titel","l15-bilanz","l15-checkliste","l15-weiter"]

SECTIONS = {
 "auftakt": {"description": "Worum es in Modul 1 geht.", "start": "cover"},
 "l11": {"description": "Lektion 1.1 — was am Ende des Kurses bei ihr steht.", "start": "l11-titel"},
 "l12": {"description": "Lektion 1.2 — die drei Stufen und welche gerade dran ist.", "start": "l12-titel"},
 "l13": {"description": "Lektion 1.3 — die Begriffe, die im Kurs dauernd vorkommen.", "start": "l13-titel"},
 "l14": {"description": "Lektion 1.4 — was die drei Stufen im Monat kosten.", "start": "l14-titel"},
 "l15": {"description": "Lektion 1.5 — Bilanz und Checkliste vor Modul 2.", "start": "l15-titel"},
}

HREF = ("https://fonts.googleapis.com/css2?family=Philosopher:wght@400;700"
        "&family=Source+Sans+3:wght@300;400;600;700&display=swap")

DECK = {
 "v": 4,
 "createdOnFiles": {"v": 1, "at": "2026-09-22T08:30:00Z"},
 "title": "Modul 1 — Orientierung",
 "order": ORDER,
 "sections": SECTIONS,
 "faces": {
   "philosopher": {"family": "Philosopher", "href": HREF},
   "source-sans-3": {"family": "Source Sans 3", "href": HREF},
 },
 "designSystems": [],
}

# ── schreiben ────────────────────────────────────────────────────────
os.makedirs(os.path.join(ZIEL, "project", "slides"), exist_ok=True)
with io.open(os.path.join(ZIEL, "project", "deck.json"), "w", encoding="utf-8", newline="\n") as f:
    f.write(json.dumps(DECK, ensure_ascii=False, indent=1))

fehlt = [s for s in ORDER if s not in FOLIEN]
extra = [s for s in FOLIEN if s not in ORDER]
if fehlt or extra:
    print("ACHTUNG  fehlt in FOLIEN: %s   nicht in ORDER: %s" % (fehlt, extra))

for sid in ORDER:
    with io.open(os.path.join(ZIEL, "project", "slides", sid + ".html"), "w",
                 encoding="utf-8", newline="\n") as f:
        f.write(FOLIEN[sid])

print("%d Folien + deck.json -> %s" % (len(ORDER), ZIEL))
for k, v in SECTIONS.items():
    n = sum(1 for s in ORDER if s.startswith(v["start"].split("-")[0]))
    print("  %-8s ab %-12s %2d Folien" % (k, v["start"], n))
