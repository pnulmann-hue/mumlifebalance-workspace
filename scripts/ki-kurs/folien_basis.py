#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gemeinsame Bausteine fuer alle Foliensaetze des Kurses
„Claude Code fuer Network-Mamas".

Jedes Modul-Skript importiert von hier und schreibt nur noch seine Inhalte:

    from folien_basis import *
    FOLIEN = {}
    FOLIEN["cover"] = modulcover(1, "Orientierung", "Untertitel", "Notiz")
    ...
    schreibe(ZIEL, "Modul 1 — Orientierung", FOLIEN, ORDER, SECTIONS)

Format: Slides-Artifact-Typ, 1920x1080, alle Stile inline aus dem erlaubten
Satz (keine margin, kein var(), keine em/rem, Schriftgroesse nie unter 24px).
"""
import io, json, os

# ── Marke ────────────────────────────────────────────────────────────
GRUND     = "#f7f4ec"   # Creme, leicht getont
CREME     = "#f1ecdd"
BLAU      = "#29556d"   # Dunkelblau
PETROL    = "#12828c"
ORANGE    = "#dc822e"
TINTE     = "#0c1c30"
GEDAEMPFT = "#5c6b73"
HELL      = "#fdfcf8"

DISPLAY = "'Philosopher', Georgia, serif"
TEXT    = "'Source Sans 3', Verdana, sans-serif"

# 🚨 Diese beiden Schriften muessen auf dem Rechner INSTALLIERT sein, sobald
#    jemand die Praesentation als PowerPoint oeffnet (Patricias Befund vom
#    20.10.2026). Im Browser holt die Folie sie von hier; PowerPoint kann das
#    nicht und ersetzt sie durch eine breitere. Dann braucht ein Satz, der mit
#    Philosopher in eine Zeile passt, zwei — der Textrahmen behaelt aber seine
#    Hoehe, und der Rest legt sich ueber den naechsten Block:
#
#        Dein Business, deine Kundin, dein Ton.
#        Ton.
#        Ohne das schreibt sie fuer irgendwen.   <- halb verdeckt
#
#    Dieselbe Ursache zerreisst die Buchstabenabstaende in den Ueberschriften
#    („D rei Z utaten“). Im Browser ist nichts davon zu sehen — wer den Fehler
#    dort sucht, sucht am falschen Ort.
#
#    Welche Stellen das trifft, misst scripts/ki-kurs/folien-platz-pruefen.mjs:
#    es rendert jede Folie einmal mit und einmal ohne die Schriften und meldet
#    jeden Block, dessen Zeilenzahl dabei kippt.
HREF = ("https://fonts.googleapis.com/css2?family=Philosopher:wght@400;700"
        "&family=Source+Sans+3:wght@300;400;600;700&display=swap")

SEK = ("background:%s; color:%s; font-family:%s; padding:128px; "
       "display:flex; flex-direction:column; gap:40px") % (GRUND, TINTE, TEXT)
SEK_DUNKEL = ("background:%s; color:%s; font-family:%s; padding:128px; "
              "display:flex; flex-direction:column; justify-content:center; gap:32px") % (BLAU, CREME, TEXT)


def zit(t):
    """Deutsche Anfuehrungszeichen — nie direkt tippen, sonst bricht die Zeichenkette."""
    return "„" + t + "“"


# ── Bausteine ────────────────────────────────────────────────────────
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

def gegenueber(links_titel, links, rechts_titel, rechts):
    """Zwei Spalten — links das Uebliche, rechts das Bessere."""
    def spalte(titel, zeilen, akzent, grund):
        z = "".join('<p style="font-size:28px; line-height:1.5; color:%s">%s</p>' % (TINTE, x) for x in zeilen)
        return ('<div style="flex:1; display:flex; flex-direction:column; gap:16px; background:%s; '
                'padding:36px; border-radius:18px; border-top:6px solid %s">'
                '<h3 style="font-family:%s; font-size:34px; font-weight:700; color:%s">%s</h3>%s</div>'
                % (grund, akzent, DISPLAY, BLAU, titel, z))
    return ('<div style="display:flex; gap:32px; align-items:stretch">%s%s</div>'
            % (spalte(links_titel, links, GEDAEMPFT, CREME),
               spalte(rechts_titel, rechts, PETROL, HELL)))

def folie(sid, inhalt, notiz, stil=None, uebergang="fade"):
    s = stil or SEK
    a = '<aside>%s</aside>' % notiz if notiz else ""
    return '<section id="%s" data-transition="%s" style="%s">%s%s</section>' % (sid, uebergang, s, inhalt, a)


# ── Wiederkehrende Folientypen ───────────────────────────────────────
def modulcover(nr, titel, unterzeile, notiz):
    return folie("cover",
        eyebrow("Claude Code für Network-Mamas", ORANGE)
        + ('<h1 style="font-family:%s; font-size:132px; font-weight:700; line-height:1.05; color:%s">'
           'Modul %d<br>%s</h1>' % (DISPLAY, CREME, nr, titel))
        + p(unterzeile, 38, CREME)
        + '<div style="flex:1"></div>'
        + p("Patricia Ulmann · Mum Life Balance", 26, PETROL),
        notiz, stil=SEK_DUNKEL)

def lektionstitel(sid, nr, titel, unterzeile, notiz, groesse=88):
    return folie(sid,
        eyebrow("Lektion " + nr) + h2(titel, BLAU, groesse) + p(unterzeile, 38, GEDAEMPFT),
        notiz)

def statement(sid, zeilen, unterzeile, notiz, zusatz=None):
    inhalt = ('<h2 style="font-family:%s; font-size:92px; font-weight:700; line-height:1.15; color:%s">%s</h2>'
              % (DISPLAY, CREME, "<br>".join(zeilen)))
    if unterzeile:
        inhalt += p(unterzeile, 34, PETROL)
    if zusatz:
        inhalt += p(zusatz, 30, CREME)
    return folie(sid, inhalt, notiz, stil=SEK_DUNKEL, uebergang="push")

def weiter(sid, eyebrow_text, titel, unterzeile, notiz):
    return folie(sid,
        eyebrow(eyebrow_text, ORANGE) + h2(titel) + p(unterzeile, 36, GEDAEMPFT),
        notiz)

def checkliste(sid, nr, punkte, modulnr, notiz):
    return folie(sid,
        eyebrow("Lektion " + nr)
        + h2("Bevor du weitermachst")
        + liste(punkte, 34)
        + beilage("Die Checkliste zum Abhaken liegt unter diesem Video."),
        notiz)


# ── Schreiben ────────────────────────────────────────────────────────
def schreibe(ziel, titel, folien, order, sections, stand="2026-09-22T09:00:00Z"):
    os.makedirs(os.path.join(ziel, "project", "slides"), exist_ok=True)

    fehlt = [s for s in order if s not in folien]
    extra = [s for s in folien if s not in order]
    if fehlt or extra:
        print("ACHTUNG  fehlt: %s   nicht in ORDER: %s" % (fehlt, extra))

    deck = {
        "v": 4,
        "createdOnFiles": {"v": 1, "at": stand},
        "title": titel,
        "order": order,
        "sections": sections,
        "faces": {
            "philosopher": {"family": "Philosopher", "href": HREF},
            "source-sans-3": {"family": "Source Sans 3", "href": HREF},
        },
        "designSystems": [],
    }
    with io.open(os.path.join(ziel, "project", "deck.json"), "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(deck, ensure_ascii=False, indent=1))

    for sid in order:
        with io.open(os.path.join(ziel, "project", "slides", sid + ".html"), "w",
                     encoding="utf-8", newline="\n") as f:
            f.write(folien[sid])

    # Groessen-Waechter: nichts unter 24px
    import re
    klein = set()
    for sid in order:
        for m in re.finditer(r"font-size:(\d+)px", folien[sid]):
            if int(m.group(1)) < 24:
                klein.add((sid, m.group(1)))
    if klein:
        print("ACHTUNG  Schrift unter 24px:", sorted(klein)[:10])

    # Anfuehrungs-Waechter: das deutsche Schlusszeichen rutscht beim Tippen
    # leicht als gerades " durch und beendet dann die Python-Zeichenkette.
    for sid in order:
        auf = folien[sid].count("„")
        zu  = folien[sid].count("“")
        if auf != zu:
            print("ACHTUNG  %s: %d Anfuehrung auf, %d zu — zit() benutzen" % (sid, auf, zu))

    print("%d Folien + deck.json -> %s" % (len(order), ziel))
    print("  %s" % titel)
    for k, v in sections.items():
        print("    %-10s ab %s" % (k, v["start"]))
    return len(order)


# ── Download-Vermerke ────────────────────────────────────────────────
# 🚨 Patricia am 22.10.2026: „ich will dass in der praesentation jeweils der
#    vermerk auf die downloads steht, damit ich es nicht vergesse zu sagen."
#    Deshalb zwei Dinge, nicht eins:
#      1 · beilage() setzt die Zeile auf die Lektionsfolie selbst
#      2 · downloads() baut am Modulende eine Uebersichtsfolie
#    Die Zeile allein reicht nicht — beim Aufnehmen scrollt sie durch und die
#    kleine Petrol-Zeile unten geht unter. Die Uebersichtsfolie ist der Halt.
def beilage(text, farbe=ORANGE):
    """Die Download-Zeile auf einer Lektionsfolie — orange, damit sie auffaellt."""
    return ('<div style="display:flex; gap:14px; align-items:center; background:%s; '
            'padding:20px 28px; border-radius:14px; border-left:6px solid %s">'
            '<span style="font-size:30px">📎</span>'
            '<p style="font-size:28px; font-weight:600; line-height:1.4; color:%s">%s</p></div>'
            % (HELL, farbe, TINTE, text))

def downloads(sid, modulnr, posten, notiz):
    """Uebersichtsfolie: alles, was in diesem Modul unter einem Video liegt.

    posten = Liste von (lektion, name) — in der Reihenfolge des Moduls.
    """
    zeilen = "".join(
        '<div style="display:flex; gap:28px; align-items:baseline; background:%s; '
        'padding:22px 28px; border-radius:14px">'
        '<span style="font-size:28px; font-weight:700; color:%s; min-width:110px">%s</span>'
        '<span style="font-size:28px; line-height:1.4; color:%s">%s</span></div>'
        % (HELL, PETROL, lek, TINTE, name) for lek, name in posten)
    return folie(sid,
        eyebrow("Modul %d · zum Mitnehmen" % modulnr, ORANGE)
        + h2("Das liegt unter den Videos")
        + ('<div style="display:flex; flex-direction:column; gap:14px">%s</div>' % zeilen)
        + p("Sag bei jeder Lektion laut, dass die Datei darunter liegt. Wer sie nicht "
            "herunterlädt, macht die Übung nicht.", 28, GEDAEMPFT),
        notiz)
