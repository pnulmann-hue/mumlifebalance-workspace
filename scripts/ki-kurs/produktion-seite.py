# -*- coding: utf-8 -*-
"""Baut aus produktion.json die Artifact-Seite „Kursproduktion Easy KI".

    python scripts/ki-kurs/produktion-daten.py     # zuerst die Daten
    python scripts/ki-kurs/produktion-seite.py     # dann die Seite

Ausgabe: outputs/produkte/ki-treppe/produktion.html

Was die Seite kann: alle zehn Kapitel mit ihren 63 Lektionen, je Lektion die
Dreh-Notiz, der Stand des Lektionstextes und die Beilagen; dazu die Foliensätze
mit Link, die 19 Beilagen, die Abläufe mit Befehlen zum Kopieren, die Links und
was offen ist.

🚨 Der Haken „aufgenommen" und die Notizen gehören Patricia und liegen in der
   Artifact-Datenbank (`db`), nicht im Seitenquelltext. Ein Neubau der Seite
   darf ihren Stand nie überschreiben — deshalb steht in der eingebetteten
   Datei auch kein einziger Haken.

🚨 Keine Zugangsdaten auf der Seite. Die Links zeigen auf Seiten, die ohnehin
   einen Login verlangen.
"""
import html
import json
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = pathlib.Path(__file__).resolve().parents[2]
KURS = ROOT / "outputs" / "produkte" / "ki-treppe"


def e(s):
    return html.escape(str(s), quote=False)


def tage_bis(iso):
    """Wie viele Tage es noch sind — beim Bauen gerechnet, nicht im Browser.
    🚨 Der Wert altert, deshalb steht das Baudatum oben auf der Seite."""
    import datetime
    d = datetime.date.fromisoformat(iso) - datetime.date.today()
    if d.days < 0:
        return "vorbei"
    if d.days == 0:
        return "heute"
    if d.days == 1:
        return "morgen"
    return "noch %d Tage" % d.days


def fett(s):
    """**fett** der Dreh-Notizen als <b>, der Rest bleibt Text."""
    teile = e(s).split("**")
    return "".join(t if i % 2 == 0 else "<b>" + t + "</b>" for i, t in enumerate(teile))


def reich(text):
    """Aus dem Markdown-Text das HTML, das in ThriveCart hineingehoert.

    🚨 Das ist der Unterschied zwischen „kopieren" und „kopieren und dann
       siebenundsechzig Mal Sternchen wegputzen". Die Lektionstexte stehen als
       Markdown da; ThriveCart Learn hat aber ein Rich-Text-Feld. Wer den
       Rohtext einfuegt, hat ueberall `**fett**` als Sternchen stehen.
       Darum legt der Knopf text/html UND text/plain in die Zwischenablage —
       dasselbe Verfahren wie auf der Startklar-Kopierseite.
    🚨 `quote=False`, sonst steht im Fliesstext ueberall &quot;."""
    absaetze = []
    for a in re.split(r"\n\s*\n", text.strip()):
        z = e(a.strip())
        z = re.sub(r"`([^`]+)`", r"<code>\1</code>", z)
        z = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", z, flags=re.S)
        # Eine Aufzaehlung bleibt eine Aufzaehlung, sonst klebt sie zusammen.
        # 🚨 `all(Zeile faengt mit "- " an)` war zu streng: in der Quelle sind
        #    die Zeilen auf 80 Zeichen umgebrochen, also beginnt nur die ERSTE
        #    Zeile je Punkt mit dem Strich. Damit wurde aus jeder Aufzaehlung
        #    ein Absatz — und die Striche standen sichtbar im Text.
        zeilen = [l for l in z.split("\n") if l.strip()]
        if zeilen and zeilen[0].lstrip().startswith(("- ", "* ")):
            punkte = []
            for l in zeilen:
                if l.lstrip().startswith(("- ", "* ")):
                    punkte.append(l.lstrip()[2:].strip())
                elif punkte:
                    punkte[-1] += " " + l.strip()   # umgebrochene Fortsetzung
            absaetze.append("<ul>%s</ul>"
                            % "".join("<li>%s</li>" % x for x in punkte))
        else:
            absaetze.append("<p>%s</p>" % "<br>".join(zeilen))
    return "".join(absaetze)


# Was ThriveCart Learn auf der Lektionsseite zurueckstellt — gemessen am
# 23.10.2026 im Browser an der fertigen Seite, nicht vermutet:
#
#   ul, li   list-style-type: none · padding-left: 0 · margin: 0
#   p        margin-top: 0 · margin-bottom: 0
#
# Darum kam der HTML-Baustein beim ersten Einfuegen ohne Aufzaehlungspunkte
# und ohne Abstaende heraus (Patricia: „die aufzaehlungspunkte nicht drin und
# die abstaende auch nicht"). Das Markup war vollstaendig da — nur unsichtbar.
#
# 🚨 Gegenprobe vor dem Bauen: eine Probe mit Angaben DIREKT AM ELEMENT in die
#    Seite gehaengt und nachgemessen — `disc`, 22.4px Einzug, 16px Abstand
#    kamen an. Der Reset arbeitet also ohne `!important`, Inline gewinnt.
#    Haette er `!important`, waere der ganze Weg hinfaellig gewesen.
# 🚨 Nur fuer die HTML-Fassung. Die reiche Fassung geht in den TEXT-Baustein,
#    und dort formatiert ThriveCarts eigener Editor — Inline-Angaben waeren
#    dort bestenfalls wirkungslos.
def fuer_thrivecart(h):
    for alt, neu in (
        ("<p>", '<p style="margin:0 0 1em 0">'),
        ("<ul>", '<ul style="list-style:disc outside;padding-left:1.4em;'
                 'margin:0 0 1em 0">'),
        ("<li>", '<li style="display:list-item;list-style:disc outside;'
                 'margin-bottom:.4em">'),
        ("<code>", '<code style="background:#f1ecdd;padding:1px 4px;'
                   'border-radius:3px">'),
    ):
        h = h.replace(alt, neu)
    return h


def kopierblock(text, beschriftung="Text kopieren"):
    """Vorschau und Kopier-Knopf fuer einen Prosatext.

    🚨 Zwei Beschwerden an einem Tag, und beide kamen vom selben Fehler: der
       Text stand als rohes Markdown da. In der Vorschau sah man `**Sternchen**`,
       und beim Einfuegen in ThriveCart kamen sie mit, weil nur reiner Text in
       der Zwischenablage lag. Jetzt zeigt die Vorschau die Formatierung, und
       der Knopf legt text/html UND text/plain ab — ohne Sternchen in beiden.
    🚨 Nur fuer PROSA. Die Einbettung und die Befehle gehen weiter als reiner
       Text: ein iframe als text/html wuerde vom Zielfeld umgebaut."""
    h = reich(text)
    sicher = html.escape(h, quote=True)
    sicher_roh = html.escape(fuer_thrivecart(h), quote=True)
    return ('<div class="vorschau">%s</div>'
            '<button class="kopf-knopf" data-reich="%s">%s</button>'
            '<button class="kopf-knopf roh" data-roh="%s" '
            'title="Fuer den HTML-Baustein in ThriveCart: Element '
            '&lt;/&gt; HTML einfuegen und hier hineinkleben. Dann ist nichts '
            'nachzuformatieren.">als HTML</button>'
            % (h, sicher, e(beschriftung), sicher_roh))


CSS = """
/* Aufbau: eine Spalte, Kapitel als aufklappbare Karten, Status als Chips.
   Farben und Schriften sind Patricias Marke. */
:root {
  --creme: #f1ecdd; --petrol: #12828c; --blau: #29556d;
  --tinte: #0c1c30; --orange: #dc822e;
  --grund: #faf8f2; --flaeche: #ffffff; --kante: #e2dccb;
  --text: #0c1c30; --leise: #5c6b7a;
  --display: Philosopher, Georgia, serif;
  --body: "Source Sans 3", "Segoe UI", system-ui, sans-serif;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --grund: #0b1722; --flaeche: #132231; --kante: #24394d;
  --text: #eee8d9; --leise: #9fb3c4; --creme: #eee8d9;
  --petrol: #3fb0ba; --orange: #f0a259; --blau: #7fa8c0;
  color-scheme: dark;
} }
:root[data-theme="dark"] {
  --grund: #0b1722; --flaeche: #132231; --kante: #24394d;
  --text: #eee8d9; --leise: #9fb3c4; --creme: #eee8d9;
  --petrol: #3fb0ba; --orange: #f0a259; --blau: #7fa8c0;
  color-scheme: dark;
}
* { box-sizing: border-box; }
body { background: var(--grund); color: var(--text); font-family: var(--body);
       font-size: 16px; line-height: 1.55; margin: 0; }
.wrap { max-width: 860px; margin: 0 auto;
        padding-left: max(16px, env(safe-area-inset-left, 0px));
        padding-right: max(16px, env(safe-area-inset-right, 0px));
        padding-block: 28px 64px; }
h1, h2, h3 { font-family: var(--display); text-wrap: balance; margin: 0; }
h1 { font-size: clamp(28px, 6vw, 40px); line-height: 1.1; }
h2 { font-size: 23px; margin-block: 36px 14px; }
.eyebrow { font-size: 11px; letter-spacing: .16em; text-transform: uppercase;
           color: var(--petrol); font-weight: 600; }
.unter { color: var(--leise); margin-block: 6px 0; }

/* Fortschritt */
.stand { display: flex; flex-wrap: wrap; gap: 10px; margin-block: 20px 0; }
.zahl { flex: 1 1 140px; min-width: 0; background: var(--flaeche);
        border: 1px solid var(--kante); border-radius: 10px; padding: 12px 14px; }
.zahl b { font-family: var(--display); font-size: 26px; display: block;
          font-variant-numeric: tabular-nums; line-height: 1.1; }
.zahl span { font-size: 13px; color: var(--leise); }
.balken { height: 8px; background: var(--kante); border-radius: 99px;
          overflow: hidden; margin-top: 14px; }
.balken i { display: block; height: 100%; background: var(--petrol); width: 0; }

/* Etappen — was bis wann fertig sein muss */
.etappen { display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
           gap: 9px; }
.etappe { background: var(--flaeche); border: 1px solid var(--kante);
          border-radius: 11px; padding: 12px 14px; min-width: 0;
          display: flex; flex-direction: column; gap: 6px; }
.etappe.dran { border-color: var(--orange); border-width: 2px; }
.ekopf { display: flex; flex-wrap: wrap; gap: 4px 8px; align-items: baseline; }
.ekopf b { font-family: var(--display); font-size: 17px; }
.etage { font-size: 12px; color: var(--orange); margin-left: auto; white-space: nowrap; }
.ekap { font-size: 13px; color: var(--leise); font-variant-numeric: tabular-nums; }
.estand { font-weight: 600; }
.ebalken { height: 6px; background: var(--kante); border-radius: 99px; overflow: hidden; }
.ebalken i { display: block; height: 100%; width: 0; background: var(--petrol); }
.etappe.fertig .ebalken i { background: var(--orange); }
.enotiz { font-size: 12.5px; color: var(--leise); }
.kfrei { font-weight: 400; font-size: 12px; color: var(--leise); }

/* Termine */
.termine { display: grid; gap: 8px; }
.termin { display: flex; flex-wrap: wrap; gap: 4px 12px; align-items: baseline;
          background: var(--flaeche); border: 1px solid var(--kante);
          border-left: 4px solid var(--petrol); border-radius: 8px; padding: 10px 13px; }
.termin.jetzt { border-left-color: var(--orange); }
.termin b { font-variant-numeric: tabular-nums; min-width: 128px; }
.termin span { color: var(--leise); font-size: 14px; flex: 1 1 200px; min-width: 0; }

/* Kapitel */
details.kap { background: var(--flaeche); border: 1px solid var(--kante);
              border-radius: 12px; margin-bottom: 10px; }
details.kap > summary { cursor: pointer; list-style: none; padding: 14px 16px;
                        display: flex; gap: 12px; align-items: center; }
details.kap > summary::-webkit-details-marker { display: none; }
details.kap > summary::after { content: "\\25be"; margin-left: auto; color: var(--leise); }
details.kap[open] > summary::after { content: "\\25b4"; }
.knr { font-family: var(--display); font-size: 20px; color: var(--petrol);
       min-width: 26px; font-variant-numeric: tabular-nums; }
.ktitel { font-weight: 600; flex: 1 1 auto; min-width: 0; }
.kmeta { font-size: 12px; color: var(--leise); white-space: nowrap; }
.kinhalt { padding: 0 16px 14px; border-top: 1px solid var(--kante); }
.folienzeile { display: flex; flex-wrap: wrap; gap: 8px; align-items: center;
               padding: 12px 0; font-size: 14px; }
.folienzeile a { color: var(--petrol); font-weight: 600; }

/* Lektionen */
.lek { border-top: 1px solid var(--kante); padding: 11px 0; display: grid;
       grid-template-columns: auto 1fr; gap: 4px 11px; }
.lek input[type=checkbox] { width: 20px; height: 20px; accent-color: var(--petrol);
                            margin: 2px 0 0; cursor: pointer; }
.lkopf { display: flex; flex-wrap: wrap; gap: 4px 9px; align-items: baseline; }
.lnr { font-variant-numeric: tabular-nums; color: var(--leise); font-size: 13px;
       min-width: 30px; }
.ltitel { font-weight: 600; }
.lek.fertig .ltitel { color: var(--leise); text-decoration: line-through; }
.lnotiz { grid-column: 2; font-size: 13.5px; color: var(--leise); }
.chips { grid-column: 2; display: flex; flex-wrap: wrap; gap: 6px; }
.chip { font-size: 11px; padding: 2px 8px; border-radius: 99px;
        border: 1px solid var(--kante); color: var(--leise); }
.chip.ja { border-color: var(--petrol); color: var(--petrol); }
.chip.pdf { border-color: var(--orange); color: var(--orange); }
a.chip { text-decoration: none; }
a.chip:hover { background: var(--grund); }
a.kachel { text-decoration: none; color: var(--text); display: block; }
a.kachel:hover { border-color: var(--petrol); }
a.kachel b { color: var(--petrol); }
.kachel code { font-size: 11.5px; color: var(--leise); word-break: break-all; }
.notizfeld { grid-column: 2; width: 100%; font: inherit; font-size: 14px;
             background: transparent; color: var(--text);
             border: 1px dashed var(--kante); border-radius: 7px;
             padding: 6px 9px; resize: vertical; min-height: 34px; }
.notizfeld:focus { border-style: solid; border-color: var(--petrol); outline: none; }

/* Der Text, der in ThriveCart unter dem Video steht */
.ltext { grid-column: 2; font-size: 13px; }
.ltext > summary { cursor: pointer; color: var(--petrol); list-style: none;
                   padding: 3px 0; }
.ltext > summary::-webkit-details-marker { display: none; }
/* 🚨 Hier stand bis zum 22.10.2026 content: "¸e  " — ein Escape, das irgendwann
   durch ein Heredoc gelaufen und dabei zu Buchstabensalat geworden ist. Vor
   jedem aufklappbaren Text stand dadurch „, e". */
.ltext > summary::before { content: "\\25b8  "; }
.ltext[open] > summary::before { content: "\\25be  "; }
.ltext pre { white-space: pre-wrap; font-family: var(--body); font-size: 13.5px;
             line-height: 1.5; }
.ltext.fehlt { color: var(--orange); padding: 3px 0; }
.kapmodul { grid-column: auto; margin: 12px 0 0; }

/* Beilagen, Abläufe, Links */
.raster { display: grid; grid-template-columns: repeat(auto-fill, minmax(230px, 1fr));
          gap: 9px; }
.kachel { background: var(--flaeche); border: 1px solid var(--kante);
          border-radius: 10px; padding: 11px 13px; min-width: 0; }
.kachel b { display: block; font-size: 14.5px; }
.kachel span { font-size: 12px; color: var(--leise); }
.ablauf { background: var(--flaeche); border: 1px solid var(--kante);
          border-radius: 10px; padding: 13px 15px; margin-bottom: 9px; }
.ablauf h3 { font-size: 16px; }
pre { background: var(--grund); border: 1px solid var(--kante); border-radius: 7px;
      padding: 9px 11px; overflow-x: auto; font-size: 13px; margin: 9px 0 0;
      font-family: ui-monospace, "Cascadia Mono", Consolas, monospace; }
.kopf-knopf { font: inherit; font-size: 12px; background: none; cursor: pointer;
              border: 1px solid var(--kante); border-radius: 6px; padding: 3px 9px;
              color: var(--leise); margin-top: 8px; }
.kopf-knopf:hover { border-color: var(--petrol); color: var(--petrol); }
.kopf-knopf.roh { margin-left: 6px; opacity: .75; }
.kopf-knopf.roh:hover { opacity: 1; }
.linkliste { display: grid; gap: 7px; }
.linkliste a { display: flex; flex-wrap: wrap; gap: 3px 10px; align-items: baseline;
               background: var(--flaeche); border: 1px solid var(--kante);
               border-radius: 9px; padding: 10px 13px; text-decoration: none;
               color: var(--text); }
.linkliste a:hover { border-color: var(--petrol); }
.linkliste b { color: var(--petrol); min-width: 150px; }
.linkliste span { font-size: 13px; color: var(--leise); flex: 1 1 160px; min-width: 0; }
.offen { background: var(--flaeche); border: 1px solid var(--kante);
         border-left: 4px solid var(--orange); border-radius: 9px;
         padding: 11px 14px; margin-bottom: 8px; }
.offen b { display: block; }
.offen span { font-size: 13.5px; color: var(--leise); }
.fuss { margin-top: 44px; padding-top: 16px; border-top: 1px solid var(--kante);
        font-size: 13px; color: var(--leise); }
a:focus-visible, summary:focus-visible, button:focus-visible,
input:focus-visible, textarea:focus-visible {
  outline: 2px solid var(--orange); outline-offset: 2px; }
@media (prefers-reduced-motion: reduce) { * { transition: none !important; } }

/* Zwei Felder je Lektion, weil ThriveCart zwei hat: Titel und Beschreibung.
   Der Titel-Knopf sitzt in der Kopfzeile, damit er beim Kopieren dort ist, wo
   der Titel steht — nicht unten bei der Beschreibung. */
.lkopf { align-items: baseline; }
.titelknopf { font: inherit; font-size: 11px; background: none; cursor: pointer;
              border: 1px solid var(--kante); border-radius: 6px;
              padding: 2px 7px; color: var(--leise); margin-left: auto;
              flex: 0 0 auto; }
.titelknopf:hover { border-color: var(--petrol); color: var(--petrol); }
.vidzeile { display: flex; gap: 8px; align-items: center; margin-top: 7px;
            flex-wrap: wrap; }
.vidzeile label { font-size: 12px; color: var(--leise); flex: 0 0 auto; }
.vidfeld { font: inherit; font-size: 13px; flex: 1 1 200px; min-width: 0;
           background: var(--grund); color: var(--text);
           border: 1px solid var(--kante); border-radius: 7px; padding: 5px 9px; }
.vidfeld:hover { border-color: var(--petrol); }
.vidzeile a { font-size: 12px; color: var(--petrol); }
.namensfeld { font-size: 14px; flex: 1 1 200px; min-width: 0;
              background: var(--grund); border: 1px solid var(--kante);
              border-radius: 7px; padding: 5px 9px; }

/* Begrüssung und Kasse: Textkarten, bei denen das Kopieren der Zweck ist. */
.textkarte { background: var(--flaeche); border: 1px solid var(--kante);
             border-radius: 11px; padding: 15px 18px; margin-bottom: 10px; }
.textkarte > h3 { font-family: Philosopher, serif; font-size: 19px;
                  margin-bottom: 3px; display: flex; gap: 9px;
                  align-items: baseline; flex-wrap: wrap; }
.textkarte .bnr { background: var(--petrol); color: var(--grund); border-radius: 6px;
                  font-family: "Source Sans 3", sans-serif; font-size: 12px;
                  padding: 1px 8px; flex: 0 0 auto; }
.textkarte pre { white-space: pre-wrap; font: inherit; font-size: 14.5px;
                 line-height: 1.55; background: var(--grund);
                 border: 1px solid var(--kante); border-radius: 8px;
                 padding: 11px 13px; margin-top: 9px; overflow-wrap: break-word; }
.textkarte .bhinweis { display: block; font-size: 13px; color: var(--orange);
                       margin-top: 9px; }
.textkarte .bnotiz { display: block; font-size: 13px; color: var(--leise);
                     margin-top: 5px; }
.textkarte .kein { font-size: 13.5px; color: var(--leise); margin-top: 7px; }
.folienliste { display: grid; gap: 7px; margin-bottom: 8px; }
.folienliste a { display: flex; gap: 4px 12px; align-items: baseline;
                 flex-wrap: wrap; background: var(--flaeche);
                 border: 1px solid var(--kante); border-radius: 9px;
                 padding: 9px 13px; text-decoration: none; color: var(--text); }
.folienliste a:hover { border-color: var(--petrol); }
.folienliste .fnr { background: var(--blau); color: var(--grund); border-radius: 6px;
                    font-size: 12px; padding: 1px 8px; flex: 0 0 auto; }
.folienliste b { flex: 1 1 140px; min-width: 0; }
.folienliste span { font-size: 13px; color: var(--leise); flex: 0 0 auto; }

/* Die Vorschau zeigt den Text SO, wie er in ThriveCart aussehen wird —
   Fettungen fett, keine Sternchen. Vorher stand hier rohes Markdown. */
.vorschau { background: var(--grund); border: 1px solid var(--kante);
            border-radius: 8px; padding: 12px 14px; margin-top: 9px;
            font-size: 14.5px; line-height: 1.6; overflow-wrap: break-word; }
.vorschau p { margin: 0 0 9px; }
.vorschau p:last-child, .vorschau ul:last-child { margin-bottom: 0; }
.vorschau ul { margin: 0 0 9px; padding-left: 20px; }
.vorschau li { margin-bottom: 4px; }
.vorschau strong { font-weight: 600; color: var(--text); }
.vorschau code { background: var(--flaeche); border: 1px solid var(--kante);
                 border-radius: 4px; padding: 1px 5px; font-size: 0.9em; }
.ltext .vorschau { font-size: 13.5px; }
"""


def video_block(l):
    """Was unter der Lektion zum Video steht.

    🚨 Liegt das Video bei Vimeo, gibt es hier NICHTS zu tippen — dann ist der
       Einbettungs-Code das, was sie braucht. Ein leeres Eingabefeld daneben
       hätte ausgesehen, als wäre noch etwas offen."""
    v = l.get("video")
    if v:
        return ('<div class="vidzeile"><label>Video</label>'
                '<a href="%s" target="_blank" rel="noopener">bei Vimeo ansehen '
                '(%s) ↗</a></div>'
                '<details class="ltext"><summary>Einbettung für ThriveCart'
                '</summary><pre>%s</pre>'
                '<button class="kopf-knopf">Einbettung kopieren</button>'
                '</details>'
                % (e(v["link"]), e(v["dauer"]), e(v["einbettung"])))
    return ('<div class="vidzeile"><label for="f%s">Video</label>'
            '<input class="vidfeld" id="f%s" type="text" '
            'placeholder="noch nicht aufgenommen — Notiz oder Link"></div>'
            % (e(l["nr"]), e(l["nr"])))


def kapitel_html(k):
    lek = []
    for l in k["lektionen"]:
        chips = []
        if l["text_drin"]:
            chips.append('<span class="chip ja">Text in ThriveCart</span>')
        else:
            chips.append('<span class="chip">Text fehlt</span>')
        for b in l["beilagen"]:
            # 🚨 Der Text kommt aus einer Markdown-Tabelle und trug seine
            #    Sternchen bis zum 22.10. sichtbar mit. fett() macht daraus
            #    eine Fettung — e() allein hat sie stehen lassen.
            if b["link"]:
                chips.append('<a class="chip pdf" href="%s" target="_blank" '
                             'rel="noopener">\U0001f4ce %s ↗</a>'
                             % (e(b["link"]), fett(b["was"])))
            else:
                chips.append('<span class="chip">\U0001f4ce %s — fehlt</span>'
                             % fett(b["was"]))
        if l.get("video"):
            chips.append('<span class="chip ja">Video liegt</span>')
        if l["neu"]:
            chips.append('<span class="chip">neu vorgeschlagen</span>')
        if l["beilagen"] and not l["beilage_im_text"]:
            chips.append('<span class="chip pdf">Text nennt die Beilage nicht</span>')

        # Der Text, der in ThriveCart unter dem Video steht — zum Kopieren.
        if l["plattformtext"]:
            text_block = ('<details class="ltext"><summary>Text unter dem Video'
                          '</summary>%s</details>'
                          % kopierblock(l["plattformtext"]))
        else:
            text_block = ('<div class="ltext fehlt">⚠ Für diese Lektion gibt es '
                          'noch keinen Text unter dem Video.</div>')
        lek.append(
            '<div class="lek" data-nr="%s">'
            '<input type="checkbox" id="v%s" aria-label="Lektion %s aufgenommen">'
            '<div class="lkopf"><span class="lnr">%s</span>'
            '<span class="ltitel" data-titel="1">%s</span>'
            '<button class="titelknopf" type="button">Titel kopieren</button></div>'
            '<div class="lnotiz">%s</div>'
            '<div class="chips">%s</div>'
            '%s'
            '%s'
            '<textarea class="notizfeld" id="n%s" rows="1" '
            'placeholder="Notiz zur Aufnahme …"></textarea>'
            '</div>'
            % (e(l["nr"]), e(l["nr"]), e(l["nr"]), e(l["nr"]), e(l["titel"]),
               fett(l["notiz"]) or "—", "".join(chips), text_block,
               video_block(l), e(l["nr"])))

    # Der Kapitelname ist in ThriveCart ein eigenes Feld — deshalb hier ein
    # eigener Knopf. Im <summary> wäre er nicht anklickbar, ohne das Kapitel
    # auf- und zuzuklappen.
    modul = ('<div class="vidzeile"><label>Kapitelname</label>'
             '<span class="namensfeld" data-titel="1">%s</span>'
             '<button class="titelknopf" type="button">Titel kopieren</button></div>'
             % e("%d · %s" % (k["nr"], k["titel"])))
    if k["modultext"]:
        modul += ('<details class="ltext kapmodul"><summary>Modultext — steht '
                  'oben im Kapitel</summary>%s</details>'
                  % kopierblock(k["modultext"]))

    folien = ""
    if k["link"]:
        warnung = ""
        if k["folien_lektionen"] and k["folien_lektionen"] != len(k["lektionen"]):
            warnung = ('<span class="chip pdf">Foliensatz kennt %d von %d Lektionen</span>'
                       % (k["folien_lektionen"], len(k["lektionen"])))
        folien = ('<div class="folienzeile"><a href="%s" target="_blank" '
                  'rel="noopener">Foliensatz öffnen ↗</a>'
                  '<span class="kmeta">%d Folien</span>%s</div>'
                  % (e(k["link"]), k["folien"], warnung))

    return ('<details class="kap"><summary>'
            '<span class="knr">%d</span>'
            '<span class="ktitel">%s<br><span class="kfrei">frei ab %s</span></span>'
            '<span class="kmeta" data-kapitel="%d">0/%d</span></summary>'
            '<div class="kinhalt">%s%s%s</div></details>'
            % (k["nr"], e(k["titel"]), e(k["etappe"]),
               k["nr"], len(k["lektionen"]), modul, folien, "".join(lek)))


JS = """
const STAND = {aufgenommen: {}, notizen: {}, videos: {}};
let db = null, version = null, bereit = false;

function zeichneStand() {
  let fertig = 0;
  document.querySelectorAll(".lek").forEach(el => {
    const nr = el.dataset.nr;
    const an = !!STAND.aufgenommen[nr];
    el.querySelector("input").checked = an;
    el.classList.toggle("fertig", an);
    const nf = el.querySelector(".notizfeld");
    if (document.activeElement !== nf) nf.value = STAND.notizen[nr] || "";
    const vf = el.querySelector(".vidfeld");
    if (vf && document.activeElement !== vf) vf.value = STAND.videos[nr] || "";
    if (an) fertig++;
  });
  document.querySelectorAll("[data-kapitel]").forEach(el => {
    const kap = el.dataset.kapitel;
    const alle = [...document.querySelectorAll(".lek")].filter(
      l => l.dataset.nr.split(".")[0] === kap);
    const an = alle.filter(l => STAND.aufgenommen[l.dataset.nr]).length;
    el.textContent = an + "/" + alle.length;
  });
  const alle = document.querySelectorAll(".lek").length;
  document.getElementById("zahl-videos").textContent = fertig;
  document.getElementById("balken-videos").style.width =
    (alle ? Math.round(fertig / alle * 100) : 0) + "%";

  // Je Etappe: wie viele ihrer Lektionen sind aufgenommen. Die erste Etappe,
  // die noch nicht fertig ist, wird hervorgehoben — das ist die, die dran ist.
  let dranGesetzt = false;
  document.querySelectorAll(".etappe").forEach(el => {
    const kapitel = el.dataset.kap.split(",");
    const lek = [...document.querySelectorAll(".lek")].filter(
      l => kapitel.includes(l.dataset.nr.split(".")[0]));
    const an = lek.filter(l => STAND.aufgenommen[l.dataset.nr]).length;
    el.querySelector(".estand").textContent = an + " von " + lek.length + " aufgenommen";
    el.querySelector(".ebalken i").style.width =
      (lek.length ? Math.round(an / lek.length * 100) : 0) + "%";
    const komplett = lek.length > 0 && an === lek.length;
    el.classList.toggle("fertig", komplett);
    el.classList.toggle("dran", !komplett && !dranGesetzt);
    if (!komplett) dranGesetzt = true;
  });
}

async function speichern() {
  if (!db) return;
  const hinweis = document.getElementById("speicher");
  try {
    const ref = db.doc("fortschritt/stand");
    await ref.set({...STAND, geaendert: new Date().toISOString()});
    hinweis.textContent = "gespeichert · " +
      new Date().toLocaleTimeString("de-CH", {hour: "2-digit", minute: "2-digit"});
  } catch (err) {
    hinweis.textContent = "konnte nicht speichern — nochmal antippen";
  }
}

let warten = null;
function merken() {
  clearTimeout(warten);
  document.getElementById("speicher").textContent = "…";
  warten = setTimeout(speichern, 700);
}

document.addEventListener("change", ev => {
  const lek = ev.target.closest?.(".lek");
  if (!lek || ev.target.type !== "checkbox") return;
  STAND.aufgenommen[lek.dataset.nr] = ev.target.checked;
  if (!ev.target.checked) delete STAND.aufgenommen[lek.dataset.nr];
  zeichneStand(); merken();
});

document.addEventListener("input", ev => {
  const lek = ev.target.closest?.(".lek");
  if (!lek) return;
  const nr = lek.dataset.nr;
  const wert = ev.target.value.trim();
  // Zwei Felder je Lektion: die Notiz und der Platz für die Aufnahme.
  const topf = ev.target.classList.contains("notizfeld") ? STAND.notizen
             : ev.target.classList.contains("vidfeld")   ? STAND.videos : null;
  if (!topf) return;
  if (wert) topf[nr] = wert; else delete topf[nr];
  merken();
});

// 🚨 Der Knopf schrieb nach jedem Kopieren „Befehl kopieren" zurück — auch am
//    Lektionstext und am Modultext, wo er „Text kopieren" heisst. Also stand
//    nach einem Klick an sechzig Stellen das falsche Wort. Darum wird die
//    eigene Beschriftung vorher gemerkt.
// 🚨 Zwei Sorten Knopf, und sie duerfen nicht verwechselt werden:
//    Prosa (data-reich) geht als text/html MIT text/plain in die Ablage, damit
//    die Fettungen in ThriveCart ankommen. Einbettungs-Code und Befehle gehen
//    als reiner Text — ein iframe als text/html wuerde vom Zielfeld umgebaut
//    statt eingefuegt.
async function indieAblage(knopf, quelle) {
  const alt = knopf.dataset.alt || knopf.textContent;
  knopf.dataset.alt = alt;
  const html = knopf.dataset.reich || null;
  const text = (quelle.innerText || quelle.textContent || "").trim();
  let fertig = false, mitForm = false;
  try {
    if (html && window.ClipboardItem && navigator.clipboard?.write) {
      await navigator.clipboard.write([new ClipboardItem({
        "text/html": new Blob([html], {type: "text/html"}),
        "text/plain": new Blob([text], {type: "text/plain"})
      })]);
      fertig = true; mitForm = true;
    } else {
      await navigator.clipboard.writeText(text);
      fertig = true;
    }
  } catch (err) {
    // Die reiche Fassung kann gesperrt sein — dann wenigstens den Text.
    try { await navigator.clipboard.writeText(text); fertig = true; }
    catch (e2) { fertig = false; }
  }
  if (fertig) {
    knopf.textContent = mitForm ? "kopiert — mit Formatierung" : "kopiert";
  } else {
    const r = document.createRange();
    r.selectNodeContents(quelle);
    const s = getSelection(); s.removeAllRanges(); s.addRange(r);
    knopf.textContent = "markiert — jetzt kopieren";
  }
  setTimeout(() => { knopf.textContent = alt; }, 2200);
}

// 🚨 Der zweite Knopf legt das HTML als REINEN TEXT ab, nicht als text/html.
//    Er zielt auf den HTML-Baustein im ThriveCart-Lektionseditor (Elemente:
//    Button, Download, Heading, Text, …, </> HTML). Dort gehoert Markup als
//    Zeichen hinein — als text/html wuerde das Feld es sofort wieder rendern
//    und man haette denselben Formatierungs-Aerger wie im Text-Baustein.
async function rohKopieren(knopf) {
  const alt = knopf.dataset.alt || knopf.textContent;
  knopf.dataset.alt = alt;
  try {
    await navigator.clipboard.writeText(knopf.dataset.roh);
    knopf.textContent = "HTML kopiert";
  } catch (err) {
    knopf.textContent = "ging nicht";
  }
  setTimeout(() => { knopf.textContent = alt; }, 2200);
}

document.addEventListener("click", ev => {
  const titel = ev.target.closest(".titelknopf");
  if (titel) {
    // Der Titel steht in derselben Zeile, nicht davor.
    const quelle = titel.closest(".lkopf, .vidzeile, h3")
                        ?.querySelector("[data-titel]");
    if (quelle) indieAblage(titel, quelle);
    return;
  }
  const knopf = ev.target.closest(".kopf-knopf");
  if (knopf && knopf.dataset.roh) { rohKopieren(knopf); return; }
  if (knopf && knopf.previousElementSibling) {
    indieAblage(knopf, knopf.previousElementSibling);
  }
});

(async () => {
  zeichneStand();
  db = await window.claude?.use?.("db");
  const hinweis = document.getElementById("speicher");
  if (!db) { hinweis.textContent = "nur ansehen — Haken werden nicht gespeichert"; return; }
  try {
    const doc = await db.doc("fortschritt/stand").get();
    const d = doc?.data?.();
    if (d) {
      STAND.aufgenommen = {...(d.aufgenommen || {})};
      STAND.notizen = {...(d.notizen || {})};
      STAND.videos = {...(d.videos || {})};
      zeichneStand();
    }
    hinweis.textContent = "Haken, Video-Links und Notizen werden gespeichert";
  } catch (err) {
    hinweis.textContent = "Stand konnte nicht geladen werden";
  }
  bereit = true;
})();
"""


def main():
    d = json.loads((KURS / "produktion.json").read_text(encoding="utf-8"))
    z = d["zahlen"]

    termine = "".join(
        '<div class="termin%s"><b>%s</b> %s <span>%s</span></div>'
        % (" jetzt" if i == 0 else "", e(t["wann"]), e(t["was"]), e(t["notiz"]))
        for i, t in enumerate(d["termine"]))

    beilagen = "".join(
        # 🚨 Eine Beilage, die es nur als Google Doc gibt, hat keine KB-Zahl.
        #    „PDF · 0 KB" hätte dort gestanden — eine Angabe, die zweimal
        #    falsch ist. Darum sagt `notiz`, was es wirklich ist.
        ('<a class="kachel" href="%s" target="_blank" rel="noopener">'
         '<b>%s ↗</b><span>%s</span></a>'
         % (e(b["link"]), e(b["titel"]),
            e(b["notiz"]) if b.get("notiz") else "PDF · %d KB" % b["kb"])) if b["link"] else
        ('<div class="kachel"><b>%s</b><span>%s</span></div>'
         % (e(b["titel"]),
            "PDF liegt da, hängt aber nicht am Artifact" if b["pdf"]
            else "⚠ noch kein PDF — nur %s.md" % e(b["name"])))
        for b in d["beilagen"])

    # Die Etappen der Verkaufsseite. Die Zahl je Etappe rechnet das Skript
    # in der Seite aus den Haken aus — sie steht nicht im Quelltext.
    etappen = "".join(
        '<div class="etappe" data-kap="%s"><div class="ekopf"><b>%s</b>'
        '<span class="etage">%s</span></div>'
        '<div class="ekap">Kapitel %s · <span class="estand">…</span></div>'
        '<div class="ebalken"><i></i></div>'
        '<span class="enotiz">%s</span></div>'
        % (",".join(str(n) for n in et["kapitel"]), e(et["wann"]),
           tage_bis(et["iso"]), " und ".join(str(n) for n in et["kapitel"]),
           e(et["notiz"]))
        for et in d["etappen"])

    dokumente = "".join(
        '<div class="kachel"><b>%s</b><span>%s<br><code>%s</code></span></div>'
        % (e(dk["was"]), e(dk["notiz"]), e(dk["pfad"])) for dk in d["dokumente"])

    ablaeufe = "".join(
        '<div class="ablauf"><h3>%s</h3><p class="unter">%s</p>'
        '<pre>%s</pre><button class="kopf-knopf">Befehl kopieren</button></div>'
        % (e(a["was"]), fett(a["notiz"]), e("\n".join(a["befehle"])))
        for a in d["ablaeufe"])

    links = "".join(
        '<a href="%s" target="_blank" rel="noopener"><b>%s</b>'
        '<span>%s</span></a>' % (e(l["url"]), e(l["was"]), e(l["notiz"]))
        for l in d["links"])

    offen = "".join(
        '<div class="offen"><b>%s — %s</b><span>%s</span></div>'
        % (e(o["was"]), e(o["stand"]), e(o["warum"])) for o in d["offen"])

    # Die erste Seite im Kursbereich. Zwei Felder, wie bei jeder Lektion.
    b = d["begruessung"]
    begruessung = (
        '<div class="textkarte"><h3><span class="bnr">Titel</span>'
        '<span data-titel="1">%s</span>'
        '<button class="titelknopf" type="button">Titel kopieren</button></h3>'
        '%s</div>'
        % (e(b["titel"]), kopierblock(b["text"])))

    # Die Textblöcke der Kasse. 🚨 Ein Block ohne Text ist kein Fehler — Block 3
    #    ist das Bild. Eine leere Kopierfläche wäre dort irreführend.
    kasse = "".join(
        '<div class="textkarte"><h3><span class="bnr">%d</span>%s</h3>%s%s%s</div>'
        % (bl["nr"], e(bl["was"]),
           kopierblock(bl["text"]) if bl["text"] else
           '<p class="kein">Kein Text — hier kommt etwas anderes hin.</p>',
           '<span class="bhinweis">%s</span>' % fett(bl["hinweis"]) if bl["hinweis"] else "",
           '<span class="bnotiz">%s</span>' % fett(bl["notiz"]) if bl["notiz"] else "")
        for bl in d["kasse"])

    folienliste = "".join(
        '<a href="%s" target="_blank" rel="noopener">'
        '<span class="fnr">%d</span><b>%s</b>'
        '<span>%d Folien · %d Lektionen ↗</span></a>'
        % (e(p["link"]), p["nr"], e(p["titel"]), p["folien"], p["lektionen"])
        for p in d["praesentationen"])

    seite = (
        '<title>Kursproduktion Easy KI</title>\n'
        '<meta name="claude:viewport-fit-sides" content="cover">\n'
        '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
        '<link href="https://fonts.googleapis.com/css2?family=Philosopher:wght@400;700'
        '&family=Source+Sans+3:wght@400;600&display=swap" rel="stylesheet">\n'
        '<style>%s</style>\n'
        '<div class="wrap">\n'
        '<p class="eyebrow">Produktion · Stand %s</p>\n'
        '<h1>%s</h1>\n'
        '<p class="unter">Alles zum Kurs an einem Ort. Hak beim Aufnehmen ab — '
        'der Stand bleibt, auch wenn du die Seite zumachst. '
        '<span id="speicher" style="color:var(--petrol)">…</span></p>\n'
        '<div class="stand">'
        # 🚨 Zwei verschiedene Zahlen, und das muss dastehen: die erste ist
        #    gemessen (so viele Lektionen haben ein Video bei Vimeo), die
        #    zweite sind ihre eigenen Haken. Unter einer Überschrift wäre eine
        #    davon falsch.
        '<div class="zahl"><b>%d / %d</b><span>Videos liegen bei Vimeo</span></div>'
        '<div class="zahl"><b><span id="zahl-videos">0</span> / %d</b>'
        '<span>von dir abgehakt</span></div>'
        '<div class="zahl"><b>%d / %d</b><span>Lektionstexte in ThriveCart</span></div>'
        '<div class="zahl"><b>%d</b><span>Folien in %d Kapiteln</span></div>'
        '<div class="zahl"><b>%d</b><span>Beilagen</span></div>'
        '</div>\n'
        '<div class="balken"><i id="balken-videos"></i></div>\n'
        '<h2>Was bis wann fertig sein muss</h2>\n'
        '<p class="unter">So steht es auf der Verkaufsseite — die Käuferinnen '
        'haben das gelesen.</p>\n<div class="etappen">%s</div>\n'
        '<h2>Die nächsten Termine</h2>\n<div class="termine">%s</div>\n'
        '<h2>Die erste Seite im Kurs</h2>\n'
        '<p class="unter">Das liest sie, bevor sie Modul 1 aufmacht.</p>\n%s\n'
        '<h2>Die zehn Kapitel</h2>\n'
        '<p class="unter">Je Lektion alles, was in ThriveCart hineingehört: '
        'Titel, Text unter dem Video, Beilagen — und ein Platz für die '
        'Aufnahme.</p>\n%s\n'
        '<h2>Die zehn Foliensätze</h2>\n'
        '<p class="unter">Alle privat. Für die Aufnahme in den Vollbild-Modus, '
        'Sprechnotizen daneben.</p>\n<div class="folienliste">%s</div>\n'
        '<h2>Beilagen</h2>\n'
        '<p class="unter">Alle als PDF am Artifact — ein Tipp und sie gehen auf. '
        '\U0001f6a8 Im Drive-Ordner lagen am 19.10. nur die Rohtexte.</p>\n'
        '<div class="raster">%s</div>\n'
        '<h2>Texte und Dateien im Workspace</h2>\n<div class="raster">%s</div>\n'
        '<h2>Die Kasse — Block für Block</h2>\n'
        '<p class="unter">Die kurze Fassung. Alles Lange steht auf '
        '<code>mumlifebalance.ch/ki-kurs/</code>.</p>\n%s\n'
        '<h2>Abläufe</h2>\n%s\n'
        '<h2>Links</h2>\n<div class="linkliste">%s</div>\n'
        '<h2>Was offen ist</h2>\n%s\n'
        '<p class="fuss">Gebaut aus dem Workspace — Kapitel und Lektionen aus '
        'dem Inhaltsverzeichnis, der Stand der Lektionstexte aus der Kopierseite, '
        'die Beilagen aus dem Ordner. Neu bauen mit '
        '<code>produktion-daten.py</code> und <code>produktion-seite.py</code>. '
        'Haken und Notizen bleiben dabei erhalten.</p>\n'
        '</div>\n<script>%s</script>\n'
        % (CSS, e(d["stand"]), e(d["kurs"]),
           z.get("videos", 0), z["lektionen"],
           z["lektionen"], z["texte_drin"], z["lektionen"],
           z["folien"], z["kapitel"], z["beilagen"],
           etappen, termine, begruessung,
           "".join(kapitel_html(k) for k in d["kapitel"]),
           folienliste, beilagen, dokumente, kasse, ablaeufe, links, offen, JS))

    ziel = KURS / "produktion.html"
    ziel.write_text(seite, encoding="utf-8")
    print("%d Zeichen -> %s" % (len(seite), ziel))
    # 🚨 Muster eng fassen: "API" ohne Wortgrenze fing "Kapiteln", "token" fing
    #    den Begriff aus Lektion 1.3. Nach dem dritten Fehlalarm liest niemand
    #    mehr hin — dann meldet der Waechter auch den echten Fund umsonst.
    import re as _re
    verdacht = [
        ("Schluessel", r"(?i)(api[_-]?key|secret|bearer\s|sk-[a-z0-9]{8})"),
        ("Mailadresse", r"[\w.+-]+@[\w-]+\.[a-z]{2,}"),
        ("Telefonnummer", r"\+41\s?7\d"),
    ]
    for name, muster in verdacht:
        tr = _re.findall(muster, seite)
        if tr:
            print("⚠ %s in der Seite: %s" % (name, tr[:3]))
    print("Haken in der Datei:", seite.count('checked'))


if __name__ == "__main__":
    main()
