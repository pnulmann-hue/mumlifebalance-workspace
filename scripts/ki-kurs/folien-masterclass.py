#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Folien fuer die KI-Masterclass am Do 8.10.2026, 09:00 (rund 45 Minuten).

    python scripts/ki-kurs/folien-masterclass.py <zielordner>

Gebaut nach dem Drei-Phasen-Framework aus dem Elevate-Call:
  Phase 1 Framing   — Elefant, Zukunftsbild, Beweis, Fuer-wen, Trust
  Phase 2 Methode   — der KLEINSTE Teil: WAS, nie WIE
  Phase 3 Pitch     — der GROESSTE Block, lang und wiederholt

Leitsatz: Content minus 100, Emotion mal 100.

🚨 Patricias Leitplanken (aus der Anmeldeseite, 25.09.2026):
  „im webinar erklaere ich nicht wie sondern WAS moeglich ist."
  Keine erfundenen Zahlen · keine Geld-zurueck-Garantie · kein „Stell dir vor" ·
  keine Plaetze-Verknappung (nur Preis-Runden) · keine fremden Namen.

🚨 Preisstand am 8.10.: Fruehbucherin 277 bis Do 15.10. 23:59, danach 333.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from folien_basis import *

ZIEL = sys.argv[1] if len(sys.argv) > 1 else "folien-masterclass"
F = {}

# Fotos (hochgeladen am 05.10.2026, kuratiert aus den Shootingbildern)
FOTO_DENKEND  = "/_blob/f8d8e088bbc4ae7c539813e9ae0b6823"   # Profil, nachdenklich,
#                                                            16:9, Gesicht rechts
FOTO_ARBEITEND= "/_blob/e81aec1064b0ab81baca5e01464dbb7a"   # am Ufer, eng zugeschnitten
FOTO_STEG     = "/_blob/c55eea35e34f736182b383e02f364488"   # auf dem Steg, eng zugeschnitten
FOTO_FLAECHE  = "/_blob/3ec97031749de2b6b962f09d99e29812"   # am Pfosten, eng zugeschnitten
FOTO_LACHEND  = "/_blob/b596c1bb0f09e0871e4a6a0d657584f2"   # lachend im Schilf,
#                                                            16:9, Gesicht rechts


def grafik_quelle():
    return ('<svg viewBox="0 0 1500 330" width="1500" height="330" '
            'aria-label="Links: eine KI schoepft aus dem halben Internet und liefert '
            'Durchschnitt. Rechts: eine KI schoepft aus deinem Material und liefert deins.">'
            # linke Seite
            '<rect x="10" y="30" width="330" height="120" rx="18" fill="#e6e2d8"/>'
            '<text x="175" y="80" font-family="Arial" font-size="26" fill="#5c6b73" '
            'text-anchor="middle">das halbe Internet</text>'
            '<text x="175" y="115" font-family="Arial" font-size="20" fill="#8a949a" '
            'text-anchor="middle">Blogs, Posts, alles</text>'
            '<path d="M 350 90 L 470 90" stroke="#8a949a" stroke-width="5"/>'
            '<path d="M 470 90 l -16 -11 v 22 z" fill="#8a949a"/>'
            '<rect x="485" y="30" width="230" height="120" rx="18" fill="#d8d3c6"/>'
            '<text x="600" y="82" font-family="Arial" font-size="26" fill="#5c6b73" '
            'text-anchor="middle">Durchschnitt</text>'
            '<text x="600" y="117" font-family="Arial" font-size="20" fill="#8a949a" '
            'text-anchor="middle">klingt nach allen</text>'
            # Trennlinie
            '<line x1="750" y1="20" x2="750" y2="250" stroke="#d8d3c6" stroke-width="3" '
            'stroke-dasharray="10 10"/>'
            # rechte Seite
            '<rect x="790" y="30" width="330" height="120" rx="18" fill="#12828c"/>'
            '<text x="955" y="80" font-family="Arial" font-size="26" fill="#f1ecdd" '
            'text-anchor="middle">dein Material</text>'
            '<text x="955" y="115" font-family="Arial" font-size="20" fill="#bfd8d5" '
            'text-anchor="middle">dein Alltag, deine Worte</text>'
            '<path d="M 1130 90 L 1250 90" stroke="#12828c" stroke-width="5"/>'
            '<path d="M 1250 90 l -16 -11 v 22 z" fill="#12828c"/>'
            '<rect x="1265" y="30" width="225" height="120" rx="18" fill="#dc822e"/>'
            '<text x="1377" y="82" font-family="Arial" font-size="26" fill="#ffffff" '
            'text-anchor="middle">deins</text>'
            '<text x="1377" y="117" font-family="Arial" font-size="20" fill="#fdf0e2" '
            'text-anchor="middle">klingt nach dir</text>'
            '</svg>')


def grafik_zwischenschritt():
    return ('<svg viewBox="0 0 1500 400" width="1500" height="400" '
            'aria-label="Oben: Auftrag geht direkt zur Antwort. Unten: der Auftrag '
            'geht erst durch fuenf Wissensdateien und dann zur Antwort.">'
            # obere Reihe: kurzer Weg
            '<text x="10" y="34" font-family="Arial" font-size="23" fill="#8a949a">'
            'Im Chat</text>'
            '<rect x="10" y="52" width="250" height="86" rx="16" fill="#e6e2d8"/>'
            '<text x="135" y="104" font-family="Arial" font-size="24" fill="#5c6b73" '
            'text-anchor="middle">dein Auftrag</text>'
            '<path d="M 275 95 L 1150 95" stroke="#c9c2b4" stroke-width="5"/>'
            '<path d="M 1150 95 l -17 -11 v 22 z" fill="#c9c2b4"/>'
            '<rect x="1165" y="52" width="325" height="86" rx="16" fill="#d8d3c6"/>'
            '<text x="1327" y="104" font-family="Arial" font-size="24" fill="#5c6b73" '
            'text-anchor="middle">Antwort für alle</text>'
            # untere Reihe: Umweg ueber das Wissen
            '<text x="10" y="236" font-family="Arial" font-size="23" fill="#12828c">'
            'Mit Assistent</text>'
            '<rect x="10" y="254" width="250" height="86" rx="16" fill="#bfd8d5"/>'
            '<text x="135" y="306" font-family="Arial" font-size="24" fill="#29556d" '
            'text-anchor="middle">dein Auftrag</text>'
            '<path d="M 275 297 L 385 297" stroke="#12828c" stroke-width="5"/>'
            '<path d="M 385 297 l -17 -11 v 22 z" fill="#12828c"/>'
            '<rect x="400" y="212" width="700" height="170" rx="16" fill="#12828c"/>'
            '<text x="750" y="258" font-family="Arial" font-size="23" fill="#f1ecdd" '
            'text-anchor="middle">liest zuerst</text>'
            '<text x="750" y="296" font-family="Arial" font-size="21" fill="#bfd8d5" '
            'text-anchor="middle">Hook-Regeln &#183; deine Leute &#183; dein Angebot</text>'
            '<text x="750" y="330" font-family="Arial" font-size="21" fill="#bfd8d5" '
            'text-anchor="middle">wie du redest &#183; was nie vorkommt</text>'
            '<path d="M 1115 297 L 1150 297" stroke="#12828c" stroke-width="5"/>'
            '<path d="M 1150 297 l -17 -11 v 22 z" fill="#12828c"/>'
            '<rect x="1165" y="254" width="325" height="86" rx="16" fill="#dc822e"/>'
            '<text x="1327" y="306" font-family="Arial" font-size="24" fill="#ffffff" '
            'text-anchor="middle">Antwort für dich</text>'
            '</svg>')

def grafik_treppe():
    return ('<svg viewBox="0 0 1500 300" width="1500" height="300" '
            'aria-label="Drei Stufen: sie klingt wie du, sie macht es ohne dich, '
            'du baust Werkzeuge.">'
            '<rect x="40" y="200" width="420" height="80" rx="14" fill="#bfd8d5"/>'
            '<text x="250" y="250" font-family="Arial" font-size="28" fill="#29556d" '
            'text-anchor="middle">1 · klingt wie du</text>'
            '<rect x="500" y="120" width="420" height="160" rx="14" fill="#12828c"/>'
            '<text x="710" y="212" font-family="Arial" font-size="28" fill="#f1ecdd" '
            'text-anchor="middle">2 · ohne dich</text>'
            '<rect x="960" y="40" width="420" height="240" rx="14" fill="#dc822e"/>'
            '<text x="1170" y="172" font-family="Arial" font-size="28" fill="#ffffff" '
            'text-anchor="middle">3 · eigene Werkzeuge</text>'
            '</svg>')

def grafik_maschine():
    """Tank + Motor. Macht den Satz sichtbar: Kurs = Maschine, Academy = Treibstoff."""
    return ('<svg viewBox="0 0 1500 260" width="1500" height="260" '
            'aria-label="Ein Tank mit Inhalt speist einen Motor, der daraus '
            'Beiträge, Angebote und Werkzeuge macht.">'
            # Tank
            '<rect x="40" y="40" width="380" height="180" rx="18" fill="#dc822e"/>'
            '<text x="230" y="105" font-family="Arial" font-size="30" font-weight="700" '
            'fill="#ffffff" text-anchor="middle">Dein Inhalt</text>'
            '<text x="230" y="150" font-family="Arial" font-size="24" fill="#ffffff" '
            'text-anchor="middle">Wie Beiträge gebaut sind,</text>'
            '<text x="230" y="182" font-family="Arial" font-size="24" fill="#ffffff" '
            'text-anchor="middle">wer deine Leute sind</text>'
            # Rohr
            '<rect x="420" y="118" width="120" height="24" fill="#bfd8d5"/>'
            '<polygon points="540,106 590,130 540,154" fill="#bfd8d5"/>'
            # Motor
            '<rect x="600" y="40" width="380" height="180" rx="18" fill="#12828c"/>'
            '<text x="790" y="105" font-family="Arial" font-size="30" font-weight="700" '
            'fill="#f1ecdd" text-anchor="middle">Der Arbeitsplatz</text>'
            '<text x="790" y="150" font-family="Arial" font-size="24" fill="#f1ecdd" '
            'text-anchor="middle">liest ihn bei jedem Auftrag,</text>'
            '<text x="790" y="182" font-family="Arial" font-size="24" fill="#f1ecdd" '
            'text-anchor="middle">arbeitet auch ohne dich</text>'
            # Rohr
            '<rect x="980" y="118" width="100" height="24" fill="#bfd8d5"/>'
            '<polygon points="1080,106 1130,130 1080,154" fill="#bfd8d5"/>'
            # Ergebnis
            '<rect x="1140" y="40" width="320" height="180" rx="18" fill="#29556d"/>'
            '<text x="1300" y="105" font-family="Arial" font-size="30" font-weight="700" '
            'fill="#f1ecdd" text-anchor="middle">Was rauskommt</text>'
            '<text x="1300" y="150" font-family="Arial" font-size="24" fill="#f1ecdd" '
            'text-anchor="middle">Beiträge, Angebote,</text>'
            '<text x="1300" y="182" font-family="Arial" font-size="24" fill="#f1ecdd" '
            'text-anchor="middle">eigene Werkzeuge</text>'
            '</svg>')


def grafik_rechnung():
    """Die Preisrechnung als Balken - 1332 Kurswert gegen 1347 mit allem drin."""
    return ('<svg viewBox="0 0 1500 300" width="1500" height="300" '
            'aria-label="Vier Kurse zu 333 ergeben 1332. Die Academy kostet 1347 '
            'und enthaelt zusaetzlich 24 Calls und ein Jahr Begleitung.">'
            '<text x="40" y="46" font-family="Arial" font-size="26" fill="#29556d">'
            'Vier Kurse einzeln</text>'
            '<rect x="40" y="62" width="330" height="62" rx="10" fill="#bfd8d5"/>'
            '<rect x="378" y="62" width="330" height="62" rx="10" fill="#bfd8d5"/>'
            '<rect x="716" y="62" width="330" height="62" rx="10" fill="#bfd8d5"/>'
            '<rect x="1054" y="62" width="330" height="62" rx="10" fill="#bfd8d5"/>'
            '<text x="205" y="101" font-family="Arial" font-size="26" fill="#29556d" '
            'text-anchor="middle">333</text>'
            '<text x="543" y="101" font-family="Arial" font-size="26" fill="#29556d" '
            'text-anchor="middle">333</text>'
            '<text x="881" y="101" font-family="Arial" font-size="26" fill="#29556d" '
            'text-anchor="middle">333</text>'
            '<text x="1219" y="101" font-family="Arial" font-size="26" fill="#29556d" '
            'text-anchor="middle">333</text>'
            '<text x="1412" y="101" font-family="Arial" font-size="30" font-weight="700" '
            'fill="#29556d" text-anchor="middle">1332</text>'
            '<text x="40" y="186" font-family="Arial" font-size="26" fill="#29556d">'
            'Die Academy</text>'
            '<rect x="40" y="202" width="1344" height="62" rx="10" fill="#12828c"/>'
            '<text x="712" y="241" font-family="Arial" font-size="26" fill="#f1ecdd" '
            'text-anchor="middle">dieselben vier Kurse &#183; 24 Calls &#183; '
            'ein Jahr Begleitung</text>'
            '<text x="1412" y="241" font-family="Arial" font-size="30" font-weight="700" '
            'fill="#dc822e" text-anchor="middle">1347</text>'
            '</svg>')

def bildfolie(sid, bild, alt_text, inhalt, notiz, rechts=True, uebergang="fade"):
    """Halbe Seite Foto, halbe Seite Text. Nie Text ueber dem Gesicht."""
    # Die Zuschnitte haben schon das Rahmen-Verhaeltnis (0.922), es wird also
    # praktisch nichts mehr beschnitten. object-position haelt den Kopf oben,
    # falls ein spaeteres Foto doch wieder anders proportioniert ist.
    img = ('<img src="%s" alt="%s" style="width:760px; height:824px; '
           'object-fit:cover; object-position:center 28%%; border-radius:24px">'
           % (bild, alt_text))
    text = ('<div style="flex:1; display:flex; flex-direction:column; '
            'justify-content:center; gap:28px">%s</div>' % inhalt)
    reihe_ = (text + img) if rechts else (img + text)
    return folie(sid,
        '<div style="display:flex; gap:64px; align-items:center">%s</div>' % reihe_,
        notiz, uebergang=uebergang)

def zeigen(sid, nr, was, dauer, punkte, notiz):
    """Bildschirm-teilen-Folie. Steht waehrend des Zeigens NICHT im Bild —
    sie ist der Absprung. Die Angaben sind fuer Patricia."""
    return folie(sid,
        eyebrow("Bildschirm teilen · " + dauer, ORANGE)
        + h2(was, BLAU, 68)
        + liste(punkte, 32)
        + p("Danach zurück zu den Folien.", 28, PETROL),
        notiz)

# ═══════════════════════════════════════════════ PHASE 1 · FRAMING

# 🚨 Cover und Schluss sind VOLLBILD 1920x1080. Ein Hochformat-Foto
# verliert darin 63 Prozent der Hoehe - genau den Kopf. Beide Bilder sind
# deshalb 16:9 zugeschnitten, Gesicht rechts, weil der Text links liegt.
F["cover"] = folie("cover",
    '<img src="%s" alt="Patricia, Hand am Kinn" style="position:absolute; left:0; top:0; width:1920px; height:1080px; object-fit:cover">' % FOTO_DENKEND
    + '<div style="position:absolute; left:0; top:0; width:1920px; height:1080px; background:linear-gradient(100deg, %s 0%%, %s 52%%, transparent 86%%)"></div>' % (TINTE, TINTE)
    + '<div style="position:absolute; left:128px; top:150px; width:1000px; display:flex; flex-direction:column; gap:36px">'
    + eyebrow("Live-Masterclass · 8. Oktober, 9 Uhr", ORANGE)
    + ('<h1 style="font-family:%s; font-size:96px; font-weight:700; line-height:1.08; color:%s">'
       'Wie oft hast du<br>deiner KI dieses Jahr<br>schon erklärt,<br>wer du bist?</h1>' % (DISPLAY, CREME))
    + p("Patricia Ulmann · Mum Life Balance", 26, PETROL)
    + '</div>',
    "Lass die Folie stehen, bis alle da sind. Kein Vorgeplauder über Technik — "
    "erste Worte sind die Frage von der Folie, laut vorgelesen, dann eine Pause. "
    "Das Foto arbeitet für dich, du musst nichts erklären.",
    stil="background:%s; font-family:%s" % (TINTE, TEXT))

F["ziele"] = folie("ziele",
    eyebrow("Die nächsten 45 Minuten")
    + h2("Was du nachher weisst")
    + liste([
        "Warum deine KI nicht nach dir klingt — und dass es nicht an dir liegt.",
        "Was eine KI, die dich kennt, anders macht als die im Browser.",
        "Wie weit das gehen kann: bis zu Dingen, die ohne dich laufen.",
        "Und was dein erster Schritt ist, wenn du es willst.",
      ], 34)
    + p("Am Ende zeig ich dir, wo du das lernen kannst. Aber erst das andere.", 30, GEDAEMPFT),
    "Zwei Minuten, nicht mehr. Wer weiss, wohin es geht, bleibt dran. Und der letzte "
    "Satz nimmt die Spannung raus, ob ein Angebot kommt — ja, kommt, aber später.")

F["chat"] = folie("chat",
    eyebrow("Kurz bevor wir anfangen", ORANGE)
    + h2("Schreib mir ins Chatfenster,<br>wo du gerade sitzt.", BLAU, 68)
    + p("Küche, Auto, Sofa, Büro — egal. Ich will nur wissen, wer da ist.", 38)
    + p("Und wenn du magst: wie oft du KI in einer normalen Woche benutzt.", 34, PETROL),
    "Wirklich warten, bis etwas kommt — zwanzig, dreissig Sekunden. Wer einmal "
    "geschrieben hat, schreibt später beim Rätsel wieder und bleibt länger dabei. "
    "Lies zwei, drei Antworten laut vor, dann hat es sich schon gelohnt.")

F["elefant"] = folie("elefant",
    eyebrow("Der Elefant im Raum")
    + h2("Alle sagen, KI spart Zeit.<br>Bei dir kostet sie welche.", BLAU, 76)
    + p("Und du denkst, du machst etwas falsch.", 40, GEDAEMPFT),
    "Das ist der Satz, auf den sie gewartet haben, ohne es zu wissen. "
    "Sag ihn und halt zwei Sekunden still. Nicht sofort auflösen.")

F["szene"] = folie("szene",
    eyebrow("Das kennst du")
    + h2("Du tippst alles hinein.<br>Und schreibst es dann um.", BLAU, 72)
    + p("Dein Thema, für wen du schreibst, was du anbietest. Zurück kommt ein Text, "
        "der nach irgendwem klingt — nur nicht nach dir.", 40)
    + p("Am Montag fängst du wieder von vorne an.", 44, ORANGE),
    "Langsam sprechen, nach dem zweiten Satz hochschauen. Hier nicken sie mit. "
    "Die orange Zeile ist der eigentliche Punkt — sag sie und lass zwei Sekunden "
    "Stille, bevor du weitergehst.")

F["nicht-du"] = statement("nicht-du",
    ["Das liegt weder an dir", "noch an der KI.", "Es fehlen zwei Dinge."],
    "Und die kann man nachrüsten. Das zeig ich dir heute.",
    "Die Entlastung ist der Grund, warum sie bleiben. Sag es warm, nicht belehrend.")

F["zukunft"] = bildfolie("zukunft", FOTO_STEG, "Patricia sitzt am Wasser",
    eyebrow("Wie es stattdessen sein kann")
    + h2("Ein Freitagmorgen bei mir", BLAU, 64)
    + p("Ich setze mich hin, und die Vorschläge für die nächste Woche stehen schon da. "
        "In meiner Sprache, zu meinem Thema, mit meinen Angeboten darunter.", 36)
    + p("Ich lese, ändere was mir nicht passt, und gebe frei. Am Handy, zwischen zwei "
        "Terminen.", 34, PETROL),
    "Dein eigener Morgen, nicht ein Versprechen. Beschreib ihn so, wie er wirklich "
    "ist — mit dem Kaffee und dem Handy. Noch nichts zeigen, das kommt gleich.",
    rechts=False)

F["beweis"] = folie("beweis",
    eyebrow("Und das ist nicht theoretisch")
    + h2("Das schaust du dir gleich selbst an")
    + reihe([
        karte("Mein Cockpit", ["Die Seite, auf der ich freigebe.",
                               "Läuft am Handy."]),
        karte("Meine Assistenten", ["Für jede Arbeit, die ich jede Woche mache.",
                                    "Einmal beschrieben, dann nur noch aufgerufen."], ORANGE),
        karte("Mein Kochbot", ["Schickt mir den Wochenplan und die Einkaufsliste.",
                               "Ohne dass ich ihn frage."]),
      ]),
    "Kurz ankündigen, nicht erklären. Das ist der Appetithappen — gezeigt wird in "
    "Phase 2. Wer hier zu früh ins Detail geht, verliert den Bogen.")

F["fuer-wen"] = folie("fuer-wen",
    eyebrow("Für wen die nächsten 40 Minuten sind")
    + gegenueber(
        "Nicht für dich, wenn",
        ["du eine Schritt-für-Schritt-Anleitung erwartest — die gibt es heute nicht.",
         "deine erste Unterhaltung mit einer KI noch vor dir liegt.",
         "dir dein Thema noch völlig unklar ist."],
        "Für dich, wenn",
        ["du KI schon benutzt und das Gefühl hast, da geht mehr.",
         "dich das Erklären jede Woche von vorne müde macht.",
         "neben allem anderen noch etwas Eigenes wachsen soll."]),
    "Die linke Spalte ehrlich vorlesen. Wer jetzt geht, wäre sowieso gegangen — und "
    "der Rest hört ab hier aufmerksamer zu.")

F["wer-ich-bin"] = bildfolie("wer-ich-bin", FOTO_ARBEITEND, "Patricia arbeitet draussen",
    eyebrow("Kurz zu mir")
    + h2("Warum ich das<br>gebaut habe", BLAU, 64)
    + p("Vier Kinder, ein Network nebenher, und ein eigenes Business zwischen Küche "
        "und Schulweg.", 36)
    + p("Ich hatte keine Zeit, jede Woche alles neu zu erklären. Also habe ich es "
        "einmal aufgeschrieben.", 34, GEDAEMPFT),
    "Zwei Sätze, nicht dein Lebenslauf. Sie soll denken „die hatte dasselbe Problem "
    "wie ich“, nicht „die ist weiter als ich“.")

F["ablauf"] = weiter("ablauf", "So läuft die nächste halbe Stunde",
    "Erst zeig ich dir die zwei Dinge, die fehlen",
    "Danach schaust du mir beim Arbeiten zu. Und am Schluss sag ich dir, wo du das lernen kannst.",
    "Ansagen, dass am Ende ein Angebot kommt. Wer es vorher weiss, fühlt sich nicht "
    "überfallen — und bleibt eher dran.")

# ═══════════════════════════════════════════════ WO DU STEHST

F["bisher"] = folie("bisher",
    eyebrow("Was du bisher machst")
    + h2("Du stellst Fragen.")
    + p("Du tippst etwas ein, bekommst eine Antwort, und wenn sie nicht passt, "
        "fragst du nochmal. So benutzen es fast alle.", 40)
    + p("Das ist Google mit besseren Sätzen.", 46, ORANGE),
    "Nicht belehrend sagen — fast alle machen es so, und es ist auch nicht falsch. "
    "Die orange Zeile ist der Moment, in dem sie merkt: da geht mehr. Pause danach.")

F["warum-durchschnitt"] = folie("warum-durchschnitt",
    eyebrow("Und warum das nie nach dir klingt")
    + h2("Eine KI, die dich nicht kennt,<br>kann nur den Durchschnitt", BLAU, 68)
    + p("Sie hat das halbe Internet gelesen. Also antwortet sie so, wie das halbe "
        "Internet schreibt — von allem ein bisschen, und nichts davon ist deins.", 40)
    + grafik_quelle()
    + p("Sie kann nicht wissen, was sie nicht hat.", 34, PETROL),
    "Die Grafik erklärt es in drei Sekunden — erst sie zeigen, dann den Satz darunter. "
    "Wer das verstanden hat, versteht danach jede der drei Stufen von selbst.")

# ═══════════════════════════════════════════════ DAS RAETSEL

F["kein-technikmensch"] = folie("kein-technikmensch",
    eyebrow("Einen Gedanken räume ich gleich weg")
    + h2("Du musst dafür nicht technisch sein.", BLAU, 72)
    + p("Du lernst auch nicht, wie Strom funktioniert, bevor du das Licht anmachst.", 40)
    + p("Ich kann nicht programmieren. Alles, was ich dir heute zeige, habe ich "
        "eingerichtet, indem ich geschrieben habe, was ich will.", 36, PETROL),
    "Der wichtigste frühe Satz. Wer die ganze Zeit denkt „das ist nichts für mich“, "
    "hört ab Minute zehn nicht mehr richtig zu. Deshalb kommt das hier und nicht "
    "erst bei den Einwänden am Schluss.")

F["raetsel"] = folie("raetsel",
    eyebrow("Kleines Rätsel")
    + h2("Zwei erste Zeilen. Eine ist von mir.")
    + gegenueber(
        "A",
        ["Du willst mehr Zeit für dein Business?",
         "Mit KI schaffst du in 30 Minuten, was vorher Stunden gedauert hat.",
         "Hier sind 5 Tipps, wie du sofort durchstartest."],
        "B",
        ["Zwischen Teamcall, Bestellungen und Hausaufgaben jetzt auch noch KI lernen?",
         "Meine erste Stunde pro Woche kam beim Menüplan zurück."]),
    "Lass sie raten — wirklich, im Chat. Zehn Sekunden. Fast alle erkennen B, und "
    "genau darum geht es: der Unterschied ist für jede sofort hörbar, aber kaum "
    "jemand weiss, woran er liegt. Das ist die Spannung, die den Mittelteil trägt.")

F["aufloesung"] = folie("aufloesung",
    eyebrow("Die Auflösung")
    + h2("B ist von mir. Und A auch —<br>nur ohne mein Material.", BLAU, 64)
    + p("Beide hat eine KI geschrieben. Bei A wusste sie nichts über mich, also hat "
        "sie genommen, was im Internet steht. Bei B hatte sie mein Material: meinen "
        "Alltag, meine Worte, meine Zahlen.", 40)
    + p("Derselbe Auftrag. Zweimal. Der Unterschied ist nur, was sie vorher wusste.", 36, ORANGE),
    "Das ist der Dreh- und Angelpunkt der ganzen Masterclass. Wenn jemand nur diesen "
    "Satz mitnimmt, hat es sich gelohnt. Zwei Sekunden Stille danach.")

F["was-passiert"] = folie("was-passiert",
    eyebrow("Was dabei wirklich passiert")
    + h2("Du tippst beide Male dasselbe:<br>„Mach mir einen Hook für Beitrag X.“", BLAU, 56)
    + grafik_zwischenschritt(),
    "Die Grafik ist der Kern der ganzen Masterclass. Zeig den oberen Weg und sag: "
    "„Das ist der ganze Vorgang. Sie liest deinen Satz und antwortet.“ Dann den "
    "unteren: „Der liest erst fünf Dinge über mich — und schreibt danach.“ "
    "Der Unterschied ist nicht die KI. Es ist der Zwischenschritt.")


F["paar-drei"] = folie("paar-drei",
    eyebrow("Und hier das zweite")
    + h2("Eine Behauptung gegen eine Szene", BLAU, 60)
    + gegenueber(
        "Nur im Chat gefragt",
        ["„Starte produktiv in die Woche! Mit guter Planung schaffst du mehr "
         "in weniger Zeit.“"],
        "Mit meinem Assistenten",
        ["„Sitzt du um acht schon am Handy und planst den Tag? Ich frühstücke um "
         "die Zeit gemütlich. Mein Plan liegt seit halb sieben bereit.“"])
    + p("<b>Der Unterschied:</b> Links keine einzige Uhrzeit. Rechts drei — und damit "
        "ein Bild, das man sofort vor sich sieht.", 32, PETROL),
    "Das ist der konkreteste der drei Vergleiche. Wer hier nachfragt „woher weiss sie "
    "die Uhrzeiten“ — aus meinem Material. Genau darum geht es.")

F["muster"] = folie("muster",
    eyebrow("Beide Male dasselbe Prinzip")
    + h2("Woran du es immer erkennst")
    + reihe([
        karte("Eine Frage, die sie kennt", ["„Jeden Montag…“ · „Sitzt du um acht…“",
                                            "Nicht „Willst du produktiver werden?“"]),
        karte("Szene statt Thema", ["Montag. Acht Uhr. Halb sieben.",
                                    "Uhrzeiten, die man vor sich sieht."], ORANGE),
        karte("Dein Gegenbild daneben", ["„Meine KI weiss das seit Monaten.“",
                                         "Erst ihre Lage, dann deine."]),
      ]),
    "Die Zusammenfassung des Unterschieds — und alle drei Punkte stehen in den zwei "
    "Beispielen, die sie gerade gesehen hat. Keines davon kann eine KI erfinden: "
    "die Frage, die Uhrzeit und dein Gegenbild kommen aus deinem Material.")

F["eins-zeigen"] = zeigen("eins-zeigen", 1, "Das machen wir jetzt einmal live",
    "rund 5 Minuten",
    ["Ein frischer Chat bei ChatGPT. Mein Auftrag hinein, Ergebnis vorlesen.",
     "Zweiter frischer Chat. Jetzt lade ich erst meine Dateien hoch — "
     "wer meine Leute sind, wie ich rede, was ein guter Hook ist.",
     "Derselbe Auftrag, Wort für Wort. Zweites Ergebnis vorlesen.",
     "Beide nebeneinander. Und dann der Satz, auf den es ankommt."],
    "🚨 Beide Male WORTGLEICH derselbe Auftrag, und nie „berücksichtige "
    "meine Dateien“ sagen — sonst denkt jede, man muss nur besser prompten, und "
    "das ist genau der Irrtum, den ich hier auflöse. "
    "Der Auftrag: „Schreib mir einen Hook für ein Reel darüber, dass niemand "
    "auf meine Beiträge reagiert.“ "
    "Der Satz danach: „Das kannst du heute Abend selber machen. Nur — das "
    "Hochladen machst du dann jedes Mal wieder. Bei mir liegen diese Dateien an ihrem "
    "Platz und werden bei jedem einzelnen Auftrag gelesen, ohne dass ich etwas tue. "
    "Das ist Stufe eins.“ "
    "Die Dateien vorher in EINEN eigenen Ordner legen — beim Hochladen sieht man "
    "den Dateidialog, und darin sonst auch Ordnernamen, die niemanden etwas angehen. "
    "Die Inhalte selbst muss ich nicht zeigen.")


F["stufen"] = folie("stufen",
    eyebrow("Und das ist erst die erste Stufe", ORANGE)
    + h2("Drei Dinge, die eine KI kann,<br>wenn sie dich kennt", BLAU, 64)
    + reihe([
        karte("1 · Sie klingt wie du", ["Weil sie dein Material hat.",
                                        "Das hast du gerade gesehen."]),
        karte("2 · Sie macht es ohne dich", ["Zu einer festen Zeit, von selbst.",
                                             "Du musst nicht dran denken."], ORANGE),
        karte("3 · Du baust Werkzeuge", ["Kleine Helfer für deine Leute.",
                                         "Ohne eine Zeile zu programmieren."]),
      ])
    + grafik_treppe(),
    "Die Landkarte für den Rest. Sag dazu, dass Stufe 1 allein den Alltag schon "
    "ändert — niemand muss bis nach oben. Das nimmt die Angst vor dem Grossen.")

F["stufe-zwei"] = folie("stufe-zwei",
    eyebrow("Stufe zwei")
    + h2("Freitagmorgen, kurz nach sieben")
    + p("Auf meinem Handy liegt der Essensplan für die nächste Woche. Mit Einkaufsliste, "
        "sortiert nach Laden, und den Mengen für sechs Personen.", 40)
    + p("Ich habe ihn nicht bestellt. Er kommt jeden Freitag.", 44, ORANGE),
    "Das ist die Stufe, bei der es von Erklärung zu Zauberei kippt. Nicht erklären, "
    "wie es gebaut ist — nur, dass niemand es anstösst.")

F["zwei-zeigen"] = zeigen("zwei-zeigen", 2, "Mein Handy am Freitagmorgen",
    "rund 4 Minuten",
    ["Telegram aufmachen. Die Nachricht mit dem Essensplan aufklappen.",
     "Durchscrollen: sieben Abende, Einkaufsliste nach Laden, Mengen für sechs.",
     "Hochscrollen zu den anderen, die sich von selbst melden: morgens, abends, sonntags.",
      ],
    "Das Handy in die Kamera halten, nicht den Bildschirm spiegeln — es soll nach "
    "Alltag aussehen, nicht nach Vorführung. Einfach scrollen lassen und wenig dazu "
    "sagen. Hier macht es klick.")

F["stufe-drei"] = folie("stufe-drei",
    eyebrow("Stufe drei")
    + h2("Ich kann nicht programmieren.")
    + p("Und habe trotzdem ein Werkzeug gebaut, das meine Leute im Network jeden Tag "
        "benutzen. Eine eigene Seite, die sie durch dreissig Tage führt.", 40)
    + p("Ich habe es eingestellt, indem ich mit der KI geredet habe. Nichts anderes.", 36, PETROL),
    "Das ist der Satz, der Networkerinnen umhaut, weil sie alle denken, so etwas "
    "brauche einen Entwickler. Sag „geredet“ und nicht „beschrieben“ — es war ein "
    "Gespräch.")

F["drei-zeigen"] = zeigen("drei-zeigen", 3, "Das Werkzeug für meine Leute",
    "rund 5 Minuten",
    ["Die Begleitungs-Seite aufmachen: was eine Teilnehmerin dort sieht.",
     "Durch zwei, drei Tage klicken — Haken, Rezepte, was sich freischaltet.",
     "Dann das Cockpit: wo ich prüfe und freigebe, was rausgeht.",
      ],
    "Erst das Werkzeug für die Kundschaft, dann dein eigenes Cockpit — in dieser "
    "Reihenfolge. Sie soll zuerst sehen, was sie selbst anbieten könnte, und dann, "
    "wie du es steuerst.")

F["assistenten"] = folie("assistenten",
    eyebrow("Was man sich alles einrichten kann")
    + h2("Das läuft bei mir — in drei Sorten", BLAU, 64)
    + reihe([
        karte("Die auf Ansage schreiben", [
            "Beiträge für die ganze Woche.",
            "Captions, Reel-Skripte, Karussell-Folien.",
            "Verkaufsseiten und Mails.",
            "Rohschnitt für ein Video."]),
        karte("Die sich selbst melden", [
            "Morgens: was heute ansteht.",
            "Abends: was morgen dran ist.",
            "Freitags: der Essensplan mit Einkaufsliste.",
            "Sonntags: was die anderen in meiner Nische posten."], ORANGE),
        karte("Die für meine Leute arbeiten", [
            "Eine Seite, die durch dreissig Tage führt.",
            "Ein Werkzeug, das ihre Profil-Texte prüft.",
            "Antworten auf Kommentare, nach meinen Regeln."]),
      ]),
    "Das ist der Moment, in dem sie anfängt zu rechnen, was bei ihr ginge. Nimm dir "
    "Zeit und lies die mittlere Spalte wirklich vor — dass etwas von selbst kommt, "
    "ohne dass man dran denkt, ist für eine Mama das stärkste Argument.")

F["ersparnis"] = folie("ersparnis",
    eyebrow("Und was das bringt")
    + h2("Nicht schneller tippen.<br>Gar nicht mehr tippen.", BLAU, 64)
    + gegenueber(
        "Was vorher jedes Mal war",
        ["Überlegen, womit du anfängst.",
         "Suchen, was du letztes Mal geschrieben hast.",
         "Erklären, wer du bist und für wen.",
         "Dran denken, dass es überhaupt dran ist."],
        "Was davon bleibt",
        ["Lesen und entscheiden, ob es passt.",
         "Ändern, was dir nicht gefällt.",
         "Freigeben.",
         "Sonst nichts."])
    + p("Zwei Zahlen, die ich wirklich gemessen habe: Der Rohschnitt für ein Video "
        "hat mich rund eine Stunde gekostet, jetzt sind es fünf Minuten Feinschliff. "
        "Und die erste Stunde pro Woche kam beim Essensplan zurück.", 30, PETROL),
    "🚨 Nur diese zwei Zahlen nennen — sie sind belegt. Keine weiteren erfinden, auch "
    "wenn danach gefragt wird; dann lieber sagen „das habe ich nicht gemessen“. "
    "Die rechte Spalte ist das eigentliche Versprechen: lesen, ändern, freigeben.")

F["freigabe"] = folie("freigabe",
    eyebrow("Eine Sache, die mir wichtig ist")
    + h2("Nichts geht raus, das ich nicht gesehen habe")
    + p("Mein Konto hängt an einem Partnerunternehmen. Ein unbedachter Satz kostet mich "
        "mehr, als mir eine automatisch geschriebene Woche je einbringt.", 40)
    + p("Deshalb schlägt die Maschine vor, und den Knopf drücke ich.", 36, PETROL),
    "Das ist dein Unterschied zu jedem Technikkurs — und für Network-Mamas der Grund, "
    "dir zu glauben. Zeig den Freigabe-Knopf im Cockpit.")

F["bogen"] = folie("bogen",
    eyebrow("Zusammengefasst")
    + h2("Drei Stufen, und auf jeder hast du etwas")
    + reihe([
        karte("1 · Sie weiss, wer du bist", ["Dein Wissen liegt da, statt jede Woche "
                                             "neu getippt zu werden."]),
        karte("2 · Sie weiss, was zu tun ist", ["Einmal beschrieben. Danach ein Aufruf."], ORANGE),
        karte("3 · Sie fängt von selbst an", ["Zu einer festen Zeit, ohne dass du "
                                              "daran denkst."]),
      ]),
    "Die Landkarte. Sag dazu: niemand muss bis nach oben, und Stufe 1 allein ändert "
    "schon den Alltag. Das nimmt die Angst vor dem Grossen.")

# ═══════════════════════════════════════════════ PHASE 3 · PITCH (groesster Block)

F["uebergang"] = statement("uebergang",
    ["Du sitzt seit vierzig Minuten", "hier und hörst zu.", "Das machen die wenigsten."],
    "Also hast du einen Grund. Und der ist mehr wert als jede Technik.",
    "Das ist der stärkste Übergang, den es gibt: erst Anerkennung, dann das Angebot. "
    "Sag es warm und meine es auch so — wer um neun Uhr morgens vierzig Minuten "
    "zuhört, hat wirklich einen Grund. Kein Tempowechsel.")

F["anderer-weg"] = folie("anderer-weg",
    eyebrow("Und jetzt die Frage")
    + h2("Was wäre, wenn du das<br>nicht allein herausfinden müsstest?", BLAU, 60)
    + p("Wenn jemand dir zeigt, in welcher Reihenfolge es geht. Wenn du fragen kannst, "
        "sobald du hängst. Und wenn du nicht wieder bei einem Kurs landest, der "
        "ungeschaut liegen bleibt.", 40)
    + p("Genau dafür habe ich das gebaut, was jetzt kommt.", 36, PETROL),
    "Die zweite Hälfte der Brücke. Die drei Dinge sind genau die drei Gründe, warum "
    "Kurse liegen bleiben — und deine Begleitung ist die Antwort darauf. Erst danach "
    "fällt der Name des Kurses.")

F["warum-nicht-allein"] = folie("warum-nicht-allein",
    eyebrow("Könntest du das auch allein herausfinden?")
    + h2("Ja. Ich habe ein Jahr gebraucht.")
    + p("Und in diesem Jahr habe ich jeden Fehler gemacht, den man machen kann — "
        "Schlüssel offen liegen lassen, Beiträge doppelt gepostet, Stunden in Dinge "
        "gesteckt, die ich danach weggeworfen habe.", 40)
    + p("Das musst du nicht nachmachen.", 36, PETROL),
    "Ehrlich, nicht als Drohung. Deine Fehler sind dein stärkstes Argument — und sie "
    "sind echt, deshalb trägt der Satz.")

F["kurs"] = bildfolie("kurs", FOTO_FLAECHE, "Patricia am Pfosten",
    eyebrow("Der Kurs", ORANGE)
    + ('<h2 style="font-family:%s; font-size:76px; font-weight:700; line-height:1.12; color:%s">'
       'Vom Chat zur<br>Mitarbeiterin</h2>' % (DISPLAY, BLAU))
    + p("Von der ersten Unterhaltung bis zu einem Arbeitsplatz, in dem dein Wissen "
        "liegt und Dinge ohne dich laufen.", 36, GEDAEMPFT),
    "Den Namen einmal sagen und die Folie stehen lassen. Noch kein Preis — "
    "erst soll das Bild wirken.", rechts=False)

F["start"] = folie("start",
    eyebrow("So läuft es ab", ORANGE)
    + h2("Start am 1. November")
    + reihe([
        karte("1 · November", ["Die ersten Module sind da.",
                               "Du fängst mit Modul 1 an, in deinem Tempo."]),
        karte("2 · Die Gruppe", ["Eine Gruppe, in der du jede Frage stellen kannst.",
                                  "Ich bin die, die antwortet."], ORANGE),
        karte("3 · Zweimal live", ["Do 19. November und Do 10. Dezember, abends.",
                                "Beide werden aufgezeichnet.",
                                   "Du bringst mit, wo du hängst."]),
      ]),
    "Das ist der Unterschied zu einem Kurs, den man kauft und allein liegen lässt. "
    "Sag die Gruppe und die beiden Termine deutlich — danach fragt niemand mehr, "
    "ob sie das allein schafft.")

F["begleitung"] = statement("begleitung",
    ["Du bist damit", "nicht allein."],
    "Eine Gruppe für jede Frage, und zweimal sehen wir uns live.",
    "Das ist dein stärkstes Argument und es kostet dich am meisten — sag es "
    "deshalb mit Nachdruck und nicht nebenbei.")

F["module"] = folie("module",
    eyebrow("Was drin ist")
    + h2("Zehn Module, von vorne aufgebaut")
    + reihe([
        karte("Die Grundlage", ["Dein Wissen kommt einmal hinein — und bleibt.",
                                "Orientierung, Chat, dein eigener Arbeitsplatz."]),
        karte("Das Herzstück", ["Assistenten bauen, die deine Arbeit übernehmen.",
                                "Und Helfer, die sich von selbst melden."], ORANGE),
        karte("Die Anwendung", ["Beiträge, Seiten, Produkte, Mails.",
                                "Deine eigene Übersicht. Und Sicherheit."]),
      ]),
    "Nicht zehn Zeilen vorlesen. Drei Blöcke, je ein Satz — wer mehr wissen will, "
    "findet die Liste auf der Seite.")

F["mitbekommst"] = folie("mitbekommst",
    eyebrow("Und das kommt mit")
    + h2("Du fängst nicht bei null an")
    + reihe([
        karte("Meine Assistenten", ["Dieselben Dateien, mit denen ich arbeite.",
                                    "Zum Kopieren, leer für deine Inhalte."]),
        karte("Fertige Aufträge", ["Zum Kopieren und Einsetzen.",
                                   "Mit einem Beispiel bei jedem Feld."], ORANGE),
        karte("Gerüste", ["Arbeitsplatz, Helfer, deine eigene Übersicht.",
                          "Aufgebaut, nur ohne deine Sachen."]),
      ]),
    "Betone „dieselben Dateien“ — nicht nachgebaute Beispiele, sondern die echten, "
    "mit denen du heute gearbeitet hast.")

F["anker"] = folie("anker",
    eyebrow("Was das wert ist")
    + h2("Eine ehrliche Rechnung")
    + p("Meine drei grossen Kurse kosten je 333. Das hier ist der vierte — und der "
        "einzige, bei dem ich die ganze Zeit mit dabei bin.", 40)
    + liste([
        "Zehn Module, rund 60 Lektionen.",
        "Meine Assistenten und Gerüste zum Kopieren.",
        "Eine Gruppe, die bleibt, und zwei Live-Calls.",
      ], 32),
    "Kein ausgedachter Mondpreis. Der Anker ist deine eigene Preistreppe, und die "
    "kann jede nachprüfen. Der dritte Punkt ist der, den die anderen drei nicht haben.")

F["preis"] = folie("preis",
    eyebrow("Erste Runde · bis Donnerstag, 15. Oktober", ORANGE)
    + ('<h2 style="font-family:%s; font-size:150px; font-weight:700; line-height:1; color:%s">'
       '277</h2>' % (DISPLAY, CREME))
    + p("Statt 333. Start ist der 1. November, und die Gruppe bleibt auch danach.", 38, PETROL)
    + p("Ab Freitag, 16. Oktober, kostet er 333 — denselben Preis wie meine anderen drei.", 30, CREME),
    "Den Preis nennen und STEHEN LASSEN. Nicht entschuldigen, nicht relativieren, "
    "nicht sofort weiterklicken. Drei Sekunden Stille sind hier richtig. Das "
    "Startdatum gehört dazu, damit niemand heute Abend Zugang erwartet.",
    stil=SEK_DUNKEL, uebergang="push")

F["grund"] = folie("grund",
    eyebrow("Warum die erste Runde günstiger ist")
    + h2("Das ist bei mir immer so")
    + p("Wer in der ersten Runde dabei ist, zahlt am wenigsten. Dafür bist du in der "
        "Gruppe, die ich am engsten begleite — und deine Fragen formen mit, wie der "
        "Kurs danach aussieht.", 40)
    + p("Ab dem 16. Oktober gilt der normale Preis.", 34, GEDAEMPFT),
    "Das ist dein Prinzip und keine Masche — sag es genau so. Wer dich länger kennt, "
    "hat das bei deinen anderen Kursen schon erlebt.")

# ---------------------------------------------------------------------------
# Die Academy als zweiter Weg. Kein Zusatzangebot, sondern die andere Haelfte:
# der Kurs ist die Maschine, die Academy ist der Treibstoff.
# Preis und Raten am 05.10.2026 aus ThriveCart geprueft: 1347 einmal,
# 6 x 224.50 (= genau 1347, kein Aufschlag), Checkout /mba ist live.
# ---------------------------------------------------------------------------

F["maschine"] = folie("maschine",
    eyebrow("Und jetzt die ehrliche Einordnung")
    + h2("Ein Kurs allein macht noch keinen Inhalt")
    + p("Was ich dir heute gezeigt habe, war immer dasselbe Muster: Die KI wurde gut, "
        "als sie wusste, wie ein guter Hook aussieht, wer meine Leute sind und was ich "
        "verkaufe. Dieses Wissen musste erst irgendwo herkommen.", 36)
    + gegenueber(
        "Der KI-Kurs",
        ["Zeigt dir, <b>wie</b> du deinen Inhalt hineinbekommst.",
         "Der Arbeitsplatz, der Brief, die Assistenten, die Werkzeuge.",
         "Die Maschine — du füllst sie mit dem, was du schon hast."],
        "Die Academy",
        ["Ist <b>der Inhalt selbst.</b>",
         "Wie Beiträge gebaut sind, wie ein Angebot verkauft, wie ein Business "
         "in einen Mama-Alltag passt.",
         "Der Treibstoff — und zusammen ergibt es mein System."])
    + grafik_maschine(),
    "Das ist der wichtigste Satz im ganzen Pitch und er muss ruhig kommen, nicht als "
    "Verkaufssatz. Sag ihn so: wer schon Inhalt hat, kommt mit dem Kurs weit. Wer bei "
    "null anfängt, füllt eine Maschine mit nichts. Keine Angst machen — "
    "einordnen.")

F["mba-inhalt"] = folie("mba-inhalt",
    eyebrow("Was in der Academy steckt")
    + h2("Drei Kurse, und in jedem ein ganzer Bereich")
    + reihe([
        karte("Instagram-Kundenmaschine", [
            "Wie ein Beitrag aufgebaut sein muss.",
            "Wie gute Hooks zustande kommen.",
            "Der ganze Auftritt — genau das Wissen, mit dem meine Assistenten "
            "arbeiten."]),
        karte("Digitale Produktwelt", [
            "Vom ersten Freebie bis zur Produkttreppe.",
            "Wie du Produkte baust, die jemand kauft.",
            "Der ganze Mechanismus dahinter."], ORANGE),
        karte("Mama-CEO", [
            "Strategien und Pläne, damit das Business in den Mama-Alltag passt.",
            "Darin steht unter anderem, wie du einen Kochassistenten so trainierst, "
            "dass er dir wirklich hilft."]),
      ])
    + p("Dazu kommt ab jetzt der KI-Kurs als vierter. Vorher waren es drei.", 34, PETROL),
    "Je Kurs ein Satz, nicht mehr — sie soll merken, dass hinter jedem Kasten ein "
    "ganzer Bereich liegt. Beim Kochassistenten kurz stehen bleiben: das verbindet die "
    "Academy mit dem, was sie vorhin auf meinem Handy gesehen hat.")

F["mba-preis"] = folie("mba-preis",
    eyebrow("Wenn du alles willst")
    + h2("Die Mum Business Academy")
    + reihe([
        karte("Drin sind", [
            "Vier Kurse: Instagram-Kundenmaschine, Digitale Produktwelt, Mama-CEO "
            "und der KI-Kurs.",
            "Ein Jahr Begleitung in der Telegramgruppe.",
            "Jeden Monat ein Call mit mir — Fragen, Austausch, Learnings.",
            "Jeden Monat ein Call mit einer Expertin: KI, Finanzen als Frau und Mama, "
            "Aurachirurgie und was Mamas im Business sonst beschäftigt."]),
        karte("Was sie kostet", [
            "Vier Kurse zu 333 sind <b>1332</b>.",
            "Die Academy kostet <b>1347</b> — und darin sind die vierundzwanzig "
            "Calls und das Jahr Begleitung.",
            "<b>Oder sechs Raten zu 224.50.</b> Das ist derselbe Betrag, nicht mehr.",
            "Bisher waren es drei Kurse für diesen Preis. Ab heute vier."], ORANGE),
      ])
    + grafik_rechnung(),
    "Die Rechnung laut vorlesen, in dieser Reihenfolge: erst 1332, dann 1347. Dann "
    "stehen lassen. Die Raten anschliessend mit dem Grund, nicht als Technik: ich "
    "weiss, wie es ist, wenn man nicht viel auf einmal ausgeben will, weil der Verdienst "
    "noch nicht da ist. Keine Frist erfinden — 1347 ist der normale Preis, neu ist "
    "der vierte Kurs.")

F["mba"] = folie("mba",
    eyebrow("Zwei Dinge, die du wissen sollst")
    + h2("Fair bleibt fair")
    + liste([
        "<b>Wenn du meine Academy hast, ist dieser Kurs für dich gratis dabei.</b> "
        "Du brauchst heute gar nichts zu tun.",
        "<b>Und wenn du heute den Kurs nimmst und später die Academy</b>, rechne ich "
        "dir an, was du heute bezahlst. Voll, nicht anteilig. Du zahlst nichts zweimal.",
      ], 34),
    "Beides laut sagen. Die Academy-Frauen fühlen sich gesehen statt übergangen, und "
    "wer überlegt, hat kein Risiko, zweimal zu zahlen.")

F["einwaende"] = folie("einwaende",
    eyebrow("Was du jetzt vielleicht denkst")
    + gegenueber(
        "Der Gedanke",
        ["„Ich bin nicht technisch.“",
         "„Ich habe keine Zeit für noch einen Kurs.“",
         "„An den Call-Abenden kann ich nicht.“",
         "„Was, wenn ich allein nicht weiterkomme?“"],
        "Meine Antwort",
        ["Du schreibst Deutsch, sonst nichts. Das Einrichten machen wir zusammen, Klick für Klick.",
         "Du schaust die Module in deinem Tempo. Nach Modul 2 hast du schon etwas, das bleibt.",
         "Beide Calls werden aufgezeichnet. Schick deine Frage vorher in die Gruppe, "
         "dann beantworte ich sie im Call — auch wenn du nicht dabei bist.",
         "Dafür ist die Gruppe da. Dienstags und donnerstags antworte ich dort — "
         "ich selbst, nicht ein Team."]),
    "Die vier kommen immer. Vorwegnehmen ist stärker als abwarten. Beim dritten "
    "kurz stehen bleiben — „ich kann an dem Abend nicht“ ist der Einwand, den "
    "die meisten gar nicht aussprechen, und er ist mit einem Satz vom Tisch.")

F["schritt"] = folie("schritt",
    eyebrow("Was jetzt zu tun ist")
    + h2("Ein Schritt, nicht drei")
    + p("Der Link steht im Chat und kommt gleich nach der Masterclass noch per Mail. "
        "Du klickst, du trägst dich ein — und am 1. November geht es los.", 40)
    + p("Wenn du eine Frage hast, schreib sie mir. Ich antworte selbst.", 36, PETROL),
    "Ein Aufruf, nicht mehrere. Link in den Chat setzen, während du das sagst — und "
    "danach wirklich für Fragen da sein.")

F["fragen"] = folie("fragen",
    eyebrow("Jetzt du")
    + h2("Was möchtest du noch wissen?")
    + p("Schreib es in den Chat. Ich bleibe, bis alles beantwortet ist.", 38, GEDAEMPFT),
    "Lass die Folie lange stehen. Wer jetzt fragt, ist am nächsten dran — und jede "
    "Antwort hören alle anderen mit. Der Preis darf hier nochmal fallen.")

F["schluss"] = folie("schluss",
    '<img src="%s" alt="Patricia lachend" style="position:absolute; left:0; top:0; width:1920px; height:1080px; object-fit:cover">' % FOTO_LACHEND
    + '<div style="position:absolute; left:0; top:0; width:1920px; height:1080px; background:linear-gradient(80deg, %s 0%%, %s 50%%, transparent 84%%)"></div>' % (TINTE, TINTE)
    + '<div style="position:absolute; left:128px; top:300px; width:960px; display:flex; flex-direction:column; gap:32px">'
    + eyebrow("Erste Runde bis 15. Oktober", ORANGE)
    + ('<h2 style="font-family:%s; font-size:80px; font-weight:700; line-height:1.15; color:%s">'
       'Du musst nicht<br>alles können.<br>Nur einmal anfangen.</h2>' % (DISPLAY, CREME))
    + p("Der Link liegt im Chat. 277 bis zum 15. Oktober, Start am 1. November.", 32, PETROL)
    + '</div>',
    "Letzte Folie, bleibt stehen, solange der Raum offen ist. Preis, Frist und "
    "Startdatum stehen drauf — damit auch wer später die Aufzeichnung schaut alles "
    "beisammen hat.",
    stil="background:%s; font-family:%s" % (TINTE, TEXT), uebergang="push")


ORDER = ["cover","ziele","chat",
 "elefant","szene","nicht-du","bisher","warum-durchschnitt","kein-technikmensch",
 "raetsel","aufloesung","was-passiert","paar-drei","muster","eins-zeigen",
 "stufen","stufe-zwei","zwei-zeigen","stufe-drei","drei-zeigen",
 "assistenten","ersparnis","freigabe",
 "zukunft","fuer-wen","wer-ich-bin",
 "uebergang","anderer-weg","warum-nicht-allein","kurs","start","begleitung","module",
 "mitbekommst","anker","preis","grund","maschine","mba-inhalt","mba-preis","mba","einwaende","schritt","fragen","schluss"]

SECTIONS = {
 "rahmen": {"description": "Ziele, Chat-Aktivierung, der Elefant im Raum.", "start": "cover"},
 "raetsel": {"description": "Zwei erste Zeilen, eine ist echt — und was dabei passiert.", "start": "raetsel"},
 "stufen": {"description": "Drei Stufen, jede mit einem live gezeigten Beweis.", "start": "stufen"},
 "bruecke": {"description": "Anerkennung, dann die Frage, dann das Angebot.", "start": "uebergang"},
}

schreibe(ZIEL, "KI-Masterclass — 8. Oktober", F, ORDER, SECTIONS)
