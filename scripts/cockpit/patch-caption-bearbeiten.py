# -*- coding: utf-8 -*-
"""Macht die Caption auf der Wochenkarte aenderbar — und repariert nebenbei
den Knopf „Hab ich selbst gepostet“.

Anlass (Patricia, 18.09.2026): „ich kann die caption hier nicht anpassen“.
Die Caption stand auf der Wochenkarte in einem <pre> — also nur zum Lesen.
Geaendert werden konnte sie nur im Reel-Studio, und beim Karussell seit dem
14.09. gar nicht mehr, weil der Karussell-Editor aus dem Cockpit raus ist.
Genau dort, wo sie geprueft und freigegeben wird, war sie festgenagelt.

🚨 Zweiter Fund beim Lesen derselben Funktion: die Fusszeile spricht ihre
Knoepfe ueber den INDEX an (`felder[felder.length - 1]` = Freigeben). Sobald
ein Beitrag freigegeben ist, kommt dahinter aber noch „Hab ich selbst
gepostet“ — und damit war der LETZTE Knopf nicht mehr Freigeben. Folge:
„Freigabe zuruecknehmen“ tat nichts, und „Hab ich selbst gepostet“ hat
stattdessen die Freigabe umgeschaltet. Der Vermerk `gepostet-von-hand` wurde
also nie gesetzt — genau der Vermerk, der den Doppelpost verhindert.
Jetzt haengen alle drei Knoepfe an einer eigenen Klasse.

Wiederholbar: jeder Schritt prueft vorher, ob er schon getan ist.
Schreibt erst in eine Datei daneben und ersetzt das Original danach.
"""
import io
import os
import sys

ZIEL = os.path.join("outputs", "cockpit", "mlb-cockpit.html")


# ---------------------------------------------------------------- Bausteine

CSS_ALT = """  .wk-caption {
    white-space: pre-wrap; font-size: 13px; line-height: 1.6; background: var(--ground);
    border: 1px solid var(--line); border-radius: 8px; padding: 11px 13px;
    max-height: 168px; overflow-y: auto; margin: 0;
  }
"""

CSS_NEU = """  /* Seit 18.09.2026 ein Textfeld statt eines <pre>. Die Caption wird auf
     dieser Karte geprueft und auf dieser Karte freigegeben — also gehoert sie
     hier auch aenderbar. Die Hashtags stehen in einer eigenen Zeile darunter,
     damit der Text oben lesbar bleibt. */
  .wk-caption {
    display: block; width: 100%; font-family: var(--body); font-size: 13px;
    line-height: 1.6; background: var(--ground); color: inherit;
    border: 1px solid var(--line); border-radius: 8px; padding: 11px 13px;
    min-height: 170px; resize: vertical; margin: 0;
  }
  .wk-caption:focus { border-color: var(--teal); outline: none; }
  .wk-tagsfeld {
    display: block; width: 100%; font-family: var(--body); font-size: 12px;
    color: var(--teal); background: var(--ground); border: 1px solid var(--line);
    border-radius: 8px; padding: 7px 11px;
  }
  .wk-tagsfeld:focus { border-color: var(--teal); outline: none; }
"""

MARKUP_ALT = (
    "        '<pre class=\"wk-caption\">' + esc(zerlegt.text || \"Noch keine Caption.\") + '</pre>' +\n"
    "        (zerlegt.tags ? '<div class=\"wk-tags\">' + esc(zerlegt.tags) + '</div>' : \"\") +\n"
)

MARKUP_NEU = (
    "        // Storys haben keine Caption — dort waere das Feld eine Einladung,\n"
    "        // Text zu schreiben, der nirgendwo ankommt.\n"
    "        (b.art === \"storys\" ? \"\" :\n"
    "          '<textarea class=\"wk-caption\" placeholder=\"Caption \\u2014 hier direkt \\u00e4nderbar\">' +\n"
    "            esc(zerlegt.text) + '</textarea>' +\n"
    "          '<input class=\"wk-tagsfeld\" placeholder=\"#hashtags\" value=\"' +\n"
    "            esc(zerlegt.tags) + '\">') +\n"
)

HANDLER_ANKER = """    // 🚨 Das Zeitfeld bleibt draussen: darunter wird ueber den Index
    // angesprochen (felder[0] Datum, felder[1] Kopieren, letztes Freigeben).
    var felder = karte.querySelectorAll(".wk-fuss input:not(.wk-zeit), .wk-fuss button");
    function merken() {
"""

HANDLER_NEU = """    // Caption und Hashtags aendern und speichern. Die drei Speicher-Funktionen
    // warten 700 ms ab, es geht also nicht je Buchstabe eine Anfrage raus.
    // 🚨 Kein render() dabei — das baut die Karte neu, und der Cursor waere weg.
    var capFeld = karte.querySelector(".wk-caption");
    var tagFeld = karte.querySelector(".wk-tagsfeld");
    if (capFeld) {
      var capSchreiben = function () {
        var text = capFeld.value.replace(/\\s+$/, "");
        var tags = tagFeld ? tagFeld.value.trim() : "";
        var ganz = tags ? (text + "\\n\\n" + tags) : text;
        b.obj.caption = ganz;
        // 🚨 Auch die Kopie in der Liste nachziehen: daraus liest „Caption
        // kopieren“, und daran haengt die Pruefung beim Freigeben.
        b.caption = ganz;
        merken();
      };
      capFeld.oninput = capSchreiben;
      if (tagFeld) tagFeld.oninput = capSchreiben;
    }

    // 🚨 Frueher wurden die Knoepfe der Fusszeile ueber den Index angesprochen
    // (felder[0] Datum, felder[1] Kopieren, letztes Freigeben). Sobald ein
    // Beitrag freigegeben war, stand hinter „Freigeben“ aber noch „Hab ich
    // selbst gepostet“ — der Freigabe-Handler lag also auf dem falschen Knopf.
    // Jetzt haengt jeder an seiner eigenen Klasse.
    function merken() {
"""

# Die drei Knoepfe in der Fusszeile bekommen eine eigene Klasse.
KNOPF_ERSETZUNGEN = [
    ("""          '<input type="date" value="' + esc(b.obj.datum || "") + '">' +""",
     """          '<input type="date" class="wk-datum" value="' + esc(b.obj.datum || "") + '">' +"""),
    ("""          '<button class="btn">Caption kopieren</button>' +""",
     """          '<button class="btn wk-kopieren">Caption kopieren</button>' +"""),
    ("""          '<button class="btn' + (b.obj.textfrei ? "" : " primary") + '">' +
            (b.obj.textfrei ? "Freigabe zurücknehmen" : "Freigeben") + '</button>' +""",
     """          '<button class="btn wk-frei' + (b.obj.textfrei ? "" : " primary") + '">' +
            (b.obj.textfrei ? "Freigabe zurücknehmen" : "Freigeben") + '</button>' +"""),
]

ZUGRIFF_ERSETZUNGEN = [
    ("""    felder[0].onchange = function () {""",
     """    karte.querySelector(".wk-datum").onchange = function () {"""),
    ("""    felder[1].onclick = function () {""",
     """    karte.querySelector(".wk-kopieren").onclick = function () {"""),
    ("""    var freigabeKnopf = felder[felder.length - 1];""",
     """    var freigabeKnopf = karte.querySelector(".wk-frei");"""),
]


def main():
    if not os.path.isfile(ZIEL):
        sys.exit("Nicht gefunden: " + ZIEL)

    with io.open(ZIEL, encoding="utf-8") as f:
        text = f.read()

    getan = []
    offen = []

    def tausche(alt, neu, name):
        nonlocal text
        if neu.strip() and neu in text:
            getan.append(name + " (war schon gesetzt)")
            return
        if alt not in text:
            offen.append(name + " — Anker nicht gefunden")
            return
        if text.count(alt) != 1:
            offen.append(name + " — Anker %dx vorhanden" % text.count(alt))
            return
        text = text.replace(alt, neu)
        getan.append(name)

    tausche(CSS_ALT, CSS_NEU, "CSS: Caption als Textfeld")
    tausche(MARKUP_ALT, MARKUP_NEU, "Karte: Textfeld statt <pre>")
    tausche(HANDLER_ANKER, HANDLER_NEU, "Handler: Caption speichern")
    for i, (alt, neu) in enumerate(KNOPF_ERSETZUNGEN, 1):
        tausche(alt, neu, "Knopf-Klasse %d/3" % i)
    for i, (alt, neu) in enumerate(ZUGRIFF_ERSETZUNGEN, 1):
        tausche(alt, neu, "Zugriff ueber Klasse %d/3" % i)

    for z in getan:
        print("  ok    " + z)
    for z in offen:
        print("  OFFEN " + z)
    if offen:
        sys.exit("\nAbgebrochen — nichts geschrieben.")

    # 🚨 Erst daneben schreiben, dann ersetzen. Ein fehlgeschlagener
    # Schreibvorgang darf die Datei nicht leer zuruecklassen.
    tmp = ZIEL + ".neu"
    with io.open(tmp, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    os.replace(tmp, ZIEL)
    print("\nGeschrieben: %s (%d Zeichen)" % (ZIEL, len(text)))


if __name__ == "__main__":
    main()
