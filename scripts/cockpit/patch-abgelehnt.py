# -*- coding: utf-8 -*-
"""Knopf „Abgelehnt" — Beiträge aussortieren, ohne sie zu verlieren.

Anlass (Patricia, 19.09.2026): *„mir noch nen knopf rein machen für abgelehnt,
dass das raus kommt oder so?"* — nachdem sie vorher gesagt hatte, sie habe zu
viele Entwürfe und einige sollen raus.

🚨 **Das ist der bessere Weg als Löschen durch Claude.** Ich hatte eine
Löschliste vorbereitet und dabei gesehen, dass sie im selben Moment mehrere
Karten bearbeitet (Cover-Höhen, „3 Wege" auf B-Roll und neues Datum). Wer unter
den Händen der anderen löscht, löscht irgendwann etwas Lebendiges. Ablehnen
gehört der, die es beurteilt.

**Wie es wirkt:**
  · Knopf **„Abgelehnt"** in der Fusszeile jeder Karte
  · Der Beitrag verschwindet aus Wochen-Vorschau, „Was zu tun ist" und
    „Fertig zum Posten"
  · Unten in der Wochen-Vorschau steht eine schmale Liste **„Abgelehnt (n)"**
    mit Knopf **„Zurückholen"** je Zeile
  · Nichts wird gelöscht — `abgelehnt: true` plus Zeitstempel am Beitrag

Zweite Änderung, die dazugehört: **„Kein Datum" ist nur dann eine Aufgabe, wenn
der Beitrag sonst fertig ist.** Sonst meldet jeder Beitrag im Vorrat eine
offene Aufgabe, und die Liste „Was zu tun ist" wird wertlos.
"""
import io
import os
import sys

ZIEL = os.path.join("outputs", "cockpit", "mlb-cockpit.html")


CSS_ANKER = "  .wk-tagsfeld:focus { border-color: var(--teal); outline: none; }\n"

CSS_NEU = CSS_ANKER + """
  /* Abgelehntes bleibt sichtbar, aber klein und unten. */
  .abliste { margin-top: 26px; opacity: 0.8; }
  .abliste h2 { font-family: var(--display); font-size: 16px; margin: 0 0 4px;
                font-weight: normal; color: var(--ink-soft); }
  .abzeile2 {
    display: grid; grid-template-columns: 92px 1fr auto; gap: 10px;
    padding: 7px 0; border-top: 1px solid var(--line); font-size: 13px;
    align-items: center;
  }
  .abzeile2:first-of-type { border-top: 0; }
  .abzeile2 .btn { font-size: 11.5px; padding: 4px 10px; }
"""


# ------------------------------------------- Abgelehnte herausfiltern

FILTER_ANKER = """  /* Ein leerer Entwurf ist kein Beitrag — weder eine Aufgabe noch etwas,
     das man freigeben koennte. */
  function istLeer(b) {"""

FILTER_NEU = """  /* Abgelehnt heisst: aus allen Arbeitsansichten raus, aber nicht geloescht.
     Das Feld bleibt am Beitrag, und „Zurueckholen" macht es rueckgaengig. */
  function istAbgelehnt(b) { return !!(b.obj || b).abgelehnt; }

  /* Ein leerer Entwurf ist kein Beitrag — weder eine Aufgabe noch etwas,
     das man freigeben koennte. */
  function istLeer(b) {"""

LISTE_ANKER = """    return beitraege;
  }
"""
LISTE_NEU = """    return beitraege;
  }

  /* Was in den Arbeitsansichten auftaucht. Abgelehntes nie. */
  function offeneBeitraege() {
    return alleBeitraege().filter(function (b) { return !istAbgelehnt(b); });
  }
"""


# ------------------------------------------ „Kein Datum" nur wenn fertig

DATUM_ANKER = """    if (!o.datum) {
      raus.push({ wer: "du", was: "Kein Datum",
                  dazu: "Ohne Datum kann nichts eingeplant werden." });
    }
    return raus;"""

DATUM_NEU = """    // 🚨 Ein Datum fehlt nur dann wirklich, wenn der Beitrag sonst fertig ist.
    // Sonst meldet jeder Beitrag aus dem Vorrat eine offene Aufgabe, und die
    // Liste „Was zu tun ist“ sagt nichts mehr.
    if (!o.datum && !raus.length) {
      raus.push({ wer: "du", was: "Kein Datum",
                  dazu: "Sonst ist alles da. Setz ein Datum, dann kann es raus." });
    }
    return raus;"""


# ----------------------------------------------- Knopf in der Fusszeile

KNOPF_ANKER = """          (b.obj.textfrei && b.art !== "storys"
            ? '<button class="btn wk-selbst">Hab ich selbst gepostet</button>'
            : "") +
        '</div>' +
"""

KNOPF_NEU = """          (b.obj.textfrei && b.art !== "storys"
            ? '<button class="btn wk-selbst">Hab ich selbst gepostet</button>'
            : "") +
          '<button class="btn wk-ablehnen">Abgelehnt</button>' +
        '</div>' +
"""

HANDLER_ANKER = """    var zeitFeld = karte.querySelector(".wk-zeit");
"""

HANDLER_NEU = """    var abKnopf = karte.querySelector(".wk-ablehnen");
    if (abKnopf) {
      abKnopf.onclick = function () {
        b.obj.abgelehnt = true;
        b.obj.abgelehntStand = new Date().toISOString();
        merken();
        toast("Aussortiert. Steht unten unter „Abgelehnt“ und ist zur\\u00fcckholbar.");
        render();
      };
    }

    var zeitFeld = karte.querySelector(".wk-zeit");
"""


# ------------------------------------- Wochen-Vorschau: Liste am Schluss

WOCHE_ANKER = """  function renderWoche(main) {
    var beitraege = alleBeitraege();
"""
WOCHE_NEU = """  function renderWoche(main) {
    var alleMit = alleBeitraege();
    var abgelehnt = alleMit.filter(istAbgelehnt);
    var beitraege = alleMit.filter(function (b) { return !istAbgelehnt(b); });
"""

ENDE_ANKER = """    if (ohneDatum.length) {
      var kopf2 = document.createElement("div");
      kopf2.className = "wt-kopf";
      kopf2.innerHTML = '<span class="wt-name">Ohne Datum</span>' +
                        '<span class="wt-datum">' + ohneDatum.length + ' Beiträge</span>';
      liste.appendChild(kopf2);
      ohneDatum.forEach(function (b) { liste.appendChild(wochenKarte(b)); });
    }
  }
"""

ENDE_NEU = """    if (ohneDatum.length) {
      var kopf2 = document.createElement("div");
      kopf2.className = "wt-kopf";
      kopf2.innerHTML = '<span class="wt-name">Im Vorrat, ohne Datum</span>' +
                        '<span class="wt-datum">' + ohneDatum.length + ' Beiträge</span>';
      liste.appendChild(kopf2);
      ohneDatum.forEach(function (b) { liste.appendChild(wochenKarte(b)); });
    }

    // Aussortiertes zuunterst, klein, mit Rueckweg.
    if (abgelehnt.length) {
      var ab = document.createElement("div");
      ab.className = "panel abliste";
      ab.innerHTML = '<h2>Abgelehnt (' + abgelehnt.length + ')</h2>' +
        '<p class="note">Aus allen Arbeitsansichten raus, aber nicht gel\\u00f6scht.</p>';
      abgelehnt.sort(function (x, y) {
        return (y.obj.abgelehntStand || "") < (x.obj.abgelehntStand || "") ? -1 : 1;
      }).forEach(function (b) {
        var z = document.createElement("div");
        z.className = "abzeile2";
        z.innerHTML = '<span class="tudatum">' + esc(b.format) + '</span>' +
          '<span>' + esc(b.titel) + '</span>';
        var zurueck = document.createElement("button");
        zurueck.className = "btn";
        zurueck.textContent = "Zur\\u00fcckholen";
        zurueck.onclick = function () {
          b.obj.abgelehnt = false;
          if (b.art === "reels") saveReel(b.obj);
          else if (b.art === "storys") saveStory(b.obj);
          else saveCarousel(b.obj);
          toast("Wieder da.");
          render();
        };
        z.appendChild(zurueck);
        ab.appendChild(z);
      });
      liste.appendChild(ab);
    }
  }
"""


# --------------------------------- „Fertig zum Posten" ohne Abgelehnte

FERTIG_ANKER = """    var alle = alleBeitraege().filter(function (b) { return !istLeer(b); });"""
FERTIG_NEU = """    var alle = offeneBeitraege().filter(function (b) { return !istLeer(b); });"""

ZAHL_ANKER = """  function fertigAnzahl() {
    return alleBeitraege().filter(function (b) {"""
ZAHL_NEU = """  function fertigAnzahl() {
    return offeneBeitraege().filter(function (b) {"""


# -------------------------------------------- abgelehnt mitspeichern

SAVE_ANKER = """        hinweis: r.hinweis || "",
"""
SAVE_NEU = """        hinweis: r.hinweis || "",
        abgelehnt: !!r.abgelehnt, abgelehntStand: r.abgelehntStand || "",
"""

LESE_ANKER = """videoart: d0.videoart || "sprech", hinweis: d0.hinweis || "","""
LESE_NEU = ("""videoart: d0.videoart || "sprech", hinweis: d0.hinweis || "", """
            """abgelehnt: !!d0.abgelehnt, abgelehntStand: d0.abgelehntStand || "",""")

KAR_SAVE_ANKER = """        textfrei: !!car.textfrei, blotato: car.blotato || null,
        slides: car.slides, caption: car.caption || "", updatedAt: car.updatedAt"""
KAR_SAVE_NEU = """        textfrei: !!car.textfrei, blotato: car.blotato || null,
        abgelehnt: !!car.abgelehnt, abgelehntStand: car.abgelehntStand || "",
        slides: car.slides, caption: car.caption || "", updatedAt: car.updatedAt"""

KAR_LESE_ANKER = """textfrei: !!d0.textfrei, blotato: d0.blotato || null, caption: d0.caption || "","""
KAR_LESE_NEU = ("""textfrei: !!d0.textfrei, blotato: d0.blotato || null, """
                """abgelehnt: !!d0.abgelehnt, abgelehntStand: d0.abgelehntStand || "", """
                """caption: d0.caption || "",""")

ST_SAVE_ANKER = """        textfrei: !!st.textfrei, updatedAt: st.updatedAt"""
ST_SAVE_NEU = """        textfrei: !!st.textfrei,
        abgelehnt: !!st.abgelehnt, abgelehntStand: st.abgelehntStand || "",
        updatedAt: st.updatedAt"""


def main():
    if not os.path.isfile(ZIEL):
        sys.exit("Nicht gefunden: " + ZIEL)
    with io.open(ZIEL, encoding="utf-8") as f:
        text = f.read()

    getan, offen = [], []

    def tausche(alt, neu, name):
        nonlocal text
        if neu in text:
            getan.append(name + " (war schon gesetzt)")
            return
        if text.count(alt) != 1:
            offen.append("%s — Anker %dx gefunden" % (name, text.count(alt)))
            return
        text = text.replace(alt, neu)
        getan.append(name)

    tausche(CSS_ANKER, CSS_NEU, "CSS fuer die Abgelehnt-Liste")
    tausche(FILTER_ANKER, FILTER_NEU, "istAbgelehnt()")
    tausche(LISTE_ANKER, LISTE_NEU, "offeneBeitraege()")
    tausche(DATUM_ANKER, DATUM_NEU, "„Kein Datum“ nur wenn sonst fertig")
    tausche(KNOPF_ANKER, KNOPF_NEU, "Knopf in der Fusszeile")
    tausche(HANDLER_ANKER, HANDLER_NEU, "Handler fuer Ablehnen")
    tausche(WOCHE_ANKER, WOCHE_NEU, "Wochen-Vorschau filtert")
    tausche(ENDE_ANKER, ENDE_NEU, "Abgelehnt-Liste am Schluss")
    tausche(FERTIG_ANKER, FERTIG_NEU, "Fertig-Reiter filtert")
    tausche(ZAHL_ANKER, ZAHL_NEU, "Zahl am Reiter filtert")
    tausche(SAVE_ANKER, SAVE_NEU, "Reel speichert abgelehnt")
    tausche(LESE_ANKER, LESE_NEU, "Reel liest abgelehnt")
    tausche(KAR_SAVE_ANKER, KAR_SAVE_NEU, "Karussell speichert abgelehnt")
    tausche(KAR_LESE_ANKER, KAR_LESE_NEU, "Karussell liest abgelehnt")
    tausche(ST_SAVE_ANKER, ST_SAVE_NEU, "Story speichert abgelehnt")

    for z in getan:
        print("  ok    " + z)
    for z in offen:
        print("  OFFEN " + z)
    if offen:
        sys.exit("\nAbgebrochen — nichts geschrieben.")

    tmp = ZIEL + ".neu"
    with io.open(tmp, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    os.replace(tmp, ZIEL)
    print("\nGeschrieben: %s (%d Zeichen)" % (ZIEL, len(text)))


if __name__ == "__main__":
    main()
