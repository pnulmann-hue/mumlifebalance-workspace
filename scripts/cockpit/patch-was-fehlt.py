# -*- coding: utf-8 -*-
"""Zeigt auf jeder Wochenkarte, WAS fehlt und WER dran ist — und macht das
Nachliefern des Videos auf derselben Karte moeglich.

Anlass (Patricia, 18.09.2026): „es hat bei vielen reels kein reel drin. aber
auch keine notizen, dass ich noch was liefern muss. wo sehe ich, was zu tun ist
und wie liefere ich die reels nach?“

Der Befund dazu — drei Luecken, jede fuer sich unsichtbar:

🚨 1. Das Feld `hinweis` stand zwar in den hochgeladenen Beitraegen
   („⚠️ VIDEO FEHLT“), wurde aber weder gelesen noch gespeichert. Es tauchte
   also nirgends auf, und beim naechsten Speichern waere es weg gewesen.
   Ein Hinweis, den niemand sieht, ist kein Hinweis.

🚨 2. Das Sprechskript steht nur im Reel-Studio. Auf der Wochenkarte — dort,
   wo Patricia prueft — war nicht zu sehen, WAS sie sagen soll. Zum Drehen
   musste sie also erst das Werkzeug wechseln.

🚨 3. Es gab keinen Weg, ein gedrehtes Video von der Karte aus abzugeben.
   Die Clip-Ablage im Reel-Studio kann das, aber nur dort und nur ueber den
   Umweg „Clip in die Ablage, dann Reel oeffnen, dann antippen“.

Was dazukommt:
  · Aufgaben-Block oben in der Wochen-Vorschau: was fehlt, nach Tag sortiert,
    mit „von dir“ und „von mir“ getrennt.
  · Je Karte eine farbige Zeile mit dem, was fehlt.
  · Bei einem Sprechreel ohne Video: der Sprechtext aufklappbar daneben.
  · Knopf „Video hochladen“ direkt auf der Karte (bis 20 MiB).
  · `hinweis` wird endlich gespeichert und gelesen.

Wiederholbar. Schreibt erst daneben und ersetzt danach.
"""
import io
import os
import sys

ZIEL = os.path.join("outputs", "cockpit", "mlb-cockpit.html")


# ------------------------------------------------------------------ 1. CSS

CSS_ANKER = "  .wk-tagsfeld:focus { border-color: var(--teal); outline: none; }\n"

CSS_NEU = CSS_ANKER + """
  /* Was an einem Beitrag noch fehlt. Steht auf der Karte selbst — ein Hinweis
     in einer Liste woanders wird nicht gelesen. Rot heisst: du bist dran.
     Petrol heisst: das mache ich. */
  .wk-fehlt {
    border-left: 3px solid var(--crit); background: rgba(179, 71, 51, 0.09);
    padding: 9px 12px; border-radius: 0 8px 8px 0; font-size: 13px; margin: 2px 0;
  }
  .wk-fehlt.meins { border-left-color: var(--teal); background: var(--teal-soft); }
  .wk-fehlt b { display: block; margin-bottom: 2px; }
  .wk-sprech { margin-top: 8px; }
  .wk-sprech summary { cursor: pointer; font-size: 13px; color: var(--teal); }
  .wk-sprechtext {
    margin: 8px 0 0; padding: 11px 13px; background: var(--ground);
    border: 1px solid var(--line); border-radius: 8px; font: inherit;
    font-size: 13px; line-height: 1.62; white-space: pre-wrap;
    max-height: 300px; overflow-y: auto;
  }
  .wk-hochladen { margin-top: 8px; font-size: 12px; padding: 6px 12px; }

  /* Der Aufgaben-Block oben in der Wochen-Vorschau. */
  .tuliste { margin-bottom: 18px; }
  .tuzeile {
    display: grid; grid-template-columns: 96px 1fr auto; gap: 10px;
    padding: 7px 0; border-top: 1px solid var(--line); font-size: 13px;
    align-items: baseline;
  }
  .tuzeile:first-of-type { border-top: 0; }
  .tudatum { font-size: 12px; color: var(--ink-soft); font-variant-numeric: tabular-nums; }
  .tuwas { min-width: 0; }
  .tuwas span { color: var(--ink-soft); }
  .tuwer {
    font-size: 10px; letter-spacing: 0.08em; text-transform: uppercase;
    padding: 2px 9px; border-radius: 999px; white-space: nowrap;
  }
  .tuwer.du { background: var(--orange-soft); color: var(--orange); }
  .tuwer.ich { background: var(--teal-soft); color: var(--teal); }
  @media (max-width: 640px) { .tuzeile { grid-template-columns: 1fr auto; }
    .tudatum { grid-column: 1 / -1; } }
"""


# -------------------------------------------------- 2. wasFehlt + Aufgaben

FEHLT_ANKER = """  function wochenKarte(b) {
"""

FEHLT_NEU = '''  /* Was an einem Beitrag fehlt, und wer dafuer zustaendig ist.
     🚨 Die Arbeitsteilung ist fest: B-Roll baue ich aus vorhandenem Material,
     ein Sprechreel drehst du — dafuer steht der Sprechtext auf der Karte.
     Ohne diese Trennung wartet jede auf die andere. */
  function wasFehlt(b) {
    var o = b.obj, raus = [];
    if (b.art === "reels" && !b.videourl) {
      if ((o.videoart || "sprech") === "broll") {
        raus.push({ wer: "ich", was: "Video fehlt",
                    dazu: "B-Roll aus vorhandenem Material \\u2014 das baue ich. " +
                          "Sag es mir in der Zeile darunter, wenn es eilt." });
      } else {
        raus.push({ wer: "du", was: "Video fehlt \\u2014 du drehst es",
                    dazu: "Sprechtext steht darunter. Danach unten auf " +
                          "\\u201eVideo hochladen\\u201c, oder aufs Handy in das Album " +
                          "Content-Inbox legen." });
      }
    }
    if (b.art !== "storys" && !(b.caption || "").trim()) {
      raus.push({ wer: "ich", was: "Caption fehlt", dazu: "" });
    }
    if (b.art === "karussells" && !(o.slides || []).length) {
      raus.push({ wer: "ich", was: "Folien fehlen", dazu: "" });
    }
    if (!o.datum) {
      raus.push({ wer: "du", was: "Kein Datum",
                  dazu: "Ohne Datum kann nichts eingeplant werden." });
    }
    return raus;
  }

  /* Der Aufgaben-Block ueber der Liste: alles Offene auf einen Blick,
     nach Tag sortiert, getrennt nach „von dir“ und „von mir“. */
  function aufgabenBlock(beitraege) {
    var offen = [];
    beitraege.forEach(function (b) {
      wasFehlt(b).forEach(function (f) {
        offen.push({ b: b, f: f });
      });
    });
    if (!offen.length) {
      return '<div class="panel tuliste"><h2>Was zu tun ist</h2>' +
             '<div class="empty">Nichts offen \\u2014 jeder Beitrag hat Video, ' +
             'Caption und Datum.</div></div>';
    }
    offen.sort(function (x, y) {
      var a = x.b.obj.datum || "9999", c = y.b.obj.datum || "9999";
      return a < c ? -1 : (a > c ? 1 : 0);
    });
    var vonDir = offen.filter(function (x) { return x.f.wer === "du"; }).length;
    var vonMir = offen.length - vonDir;
    var h = '<div class="panel tuliste"><h2>Was zu tun ist</h2>' +
      '<p class="note">' + vonDir + ' von dir \\u00b7 ' + vonMir + ' von mir. ' +
      'Was bei dir steht, h\\u00e4lt den Beitrag auf \\u2014 alles andere l\\u00e4uft ' +
      'auch ohne dich weiter.</p>';
    offen.forEach(function (x) {
      h += '<div class="tuzeile">' +
        '<span class="tudatum">' +
          (x.b.obj.datum ? esc(tagName(x.b.obj.datum).slice(0, 2) + " " +
                               fmtDate(x.b.obj.datum)) : "ohne Datum") +
        '</span>' +
        '<span class="tuwas"><strong>' + esc(x.f.was) + '</strong> \\u2014 ' +
          esc(x.b.titel) + '</span>' +
        '<span class="tuwer ' + x.f.wer + '">' +
          (x.f.wer === "du" ? "von dir" : "von mir") + '</span>' +
        '</div>';
    });
    return h + '</div>';
  }

  function wochenKarte(b) {
'''


# ------------------------------------------ 3. Aufgaben-Block einhaengen

WOCHE_ANKER = """      '<div class="head-actions"><span class="chip">' + frei + ' von ' + beitraege.length +
      ' freigegeben</span></div></div>' +
      '<div id="wliste"></div>';
"""

WOCHE_NEU = """      '<div class="head-actions"><span class="chip">' + frei + ' von ' + beitraege.length +
      ' freigegeben</span></div></div>' +
      aufgabenBlock(beitraege) +
      '<div id="wliste"></div>';
"""


# --------------------------------------------- 4. Karte: Zeilen + Upload

KARTE_ANKER = """        auftragsZeile(b.obj) +
        '<div class="wk-fuss">' +
"""

KARTE_NEU = """        // Was fehlt, steht ueber der Fusszeile — direkt dort, wo Patricia
        // sonst freigeben wuerde.
        wasFehlt(b).map(function (f) {
          return '<div class="wk-fehlt' + (f.wer === "ich" ? " meins" : "") + '">' +
            '<b>' + (f.wer === "du" ? "\\u270d\\ufe0f Von dir: " : "\\u23f3 Von mir: ") +
            esc(f.was) + '</b>' + (f.dazu ? esc(f.dazu) : "") + '</div>';
        }).join("") +
        // Der Sprechtext gehoert dorthin, wo sie das Video vermisst.
        (b.art === "reels" && !b.videourl && (b.obj.videoart || "sprech") !== "broll"
            && (b.obj.skript || "").trim()
          ? '<details class="wk-sprech"><summary>Sprechtext anzeigen</summary>' +
            '<pre class="wk-sprechtext">' + esc(b.obj.skript) + '</pre></details>'
          : "") +
        auftragsZeile(b.obj) +
        '<div class="wk-fuss">' +
"""

# Der Upload-Knopf kommt in die Spalte unter dem Cover, zu „Video speichern“.
HOCH_ANKER = """      farbwahl += '<div class="wk-holen">' +
        (b.videourl ? '<button class="btn" data-holen="video">Video speichern</button>' : "") +
"""

HOCH_NEU = """      farbwahl += '<div class="wk-holen">' +
        (b.videourl ? '<button class="btn" data-holen="video">Video speichern</button>' : "") +
        // 🚨 Der Rueckweg: ein gedrehtes Video von der Karte aus abgeben.
        // Ohne das musste Patricia ins Reel-Studio wechseln und dort den
        // Umweg ueber die Clip-Ablage nehmen.
        (assetsAPI
          ? '<label class="btn filebtn wk-hochladen' + (b.videourl ? "" : " primary") + '">' +
            '<span>' + (b.videourl ? "Video ersetzen" : "Video hochladen") + '</span>' +
            '<input type="file" accept="video/mp4,video/quicktime,video/webm"></label>'
          : "") +
"""


# ------------------------------------------------- 5. Upload-Handler

HANDLER_ANKER = """    karte.querySelectorAll(".farbknopf").forEach(function (kn) {
"""

HANDLER_NEU = '''    /* Video nachliefern. Laedt als Anhang ans Artifact und haengt die
       Adresse an den Beitrag. 🚨 20 MiB je Datei — das sagt der Knopf
       vorher, statt den Fehler von der Schnittstelle zu holen, wenn der
       Upload schon laeuft. Ein Handyvideo von ueber ~40 Sekunden reisst das. */
    var hochFeld = karte.querySelector(".wk-hochladen input");
    if (hochFeld) {
      hochFeld.onchange = function () {
        var f = this.files && this.files[0];
        if (!f) return;
        if (f.size > 20 * 1024 * 1024) {
          toast("Zu gross (" + Math.round(f.size / 1048576) + " MB). " +
                "H\\u00f6chstens 20 MB \\u2014 k\\u00fcrzer schneiden, oder leg es aufs " +
                "Handy in das Album Content-Inbox, dann hole ich es.");
          this.value = "";
          return;
        }
        var lab = karte.querySelector(".wk-hochladen span");
        if (lab) lab.textContent = "l\\u00e4dt \\u2026";
        assetsAPI.upload(f).then(function (res) {
          b.obj.videourl = "/_blob/" + res.id;
          b.obj.videodatei = f.name;
          merken();
          toast("Video ist dran. Schau es dir an, dann kannst du freigeben.");
          render();
        }).catch(function (e) {
          if (lab) lab.textContent = "Video hochladen";
          toast("Hochladen ging nicht (" + ((e && e.code) || "unbekannt") + ").");
        });
      };
    }

    karte.querySelectorAll(".farbknopf").forEach(function (kn) {
'''


# ------------------------------------------------- 6. hinweis speichern

SAVE_ANKER = """        videoart: r.videoart || "sprech",
"""
SAVE_NEU = """        videoart: r.videoart || "sprech",
        // 🚨 Bis 18.09. fehlte `hinweis` hier UND beim Lesen. Die Notiz
        // „VIDEO FEHLT“ stand in den hochgeladenen Beitraegen, war aber
        // unsichtbar und waere beim naechsten Speichern verschwunden.
        hinweis: r.hinweis || "",
"""

LESE_ANKER = """videoart: d0.videoart || "sprech","""
LESE_NEU = """videoart: d0.videoart || "sprech", hinweis: d0.hinweis || "","""


# ------------------------------------------------- 7. Nachbesserungen

# 🚨 Leere Entwuerfe („Neues Reel“, nichts drin) standen dreimal in der
# Aufgabenliste und haben sie oben aufgeblaeht. Auf der Karte duerfen sie
# bleiben — in der To-do-Liste haben sie nichts verloren.
LEER_ANKER = """    var offen = [];
    beitraege.forEach(function (b) {
      wasFehlt(b).forEach(function (f) {
        offen.push({ b: b, f: f });
      });
    });"""

LEER_NEU = """    var offen = [];
    beitraege.forEach(function (b) {
      // Ein leerer Entwurf ist keine Aufgabe.
      var leer = !(b.hook || "").trim() && !(b.caption || "").trim() &&
                 !((b.obj.slides || []).length) && !((b.obj.frames || []).length);
      if (leer) return;
      wasFehlt(b).forEach(function (f) {
        offen.push({ b: b, f: f });
      });
    });"""

# Der Knopf sitzt links unter dem Cover, nicht unten.
ORT_ANKER = """                    dazu: "Sprechtext steht darunter. Danach unten auf " +
                          "\\u201eVideo hochladen\\u201c, oder aufs Handy in das Album " +
                          "Content-Inbox legen." });"""

ORT_NEU = """                    dazu: "Sprechtext steht darunter. Fertig gedreht: links " +
                          "unter dem Cover auf \\u201eVideo hochladen\\u201c \\u2014 oder " +
                          "roh mit Versprechern ins Handy-Album Content-Inbox, " +
                          "dann hole und schneide ich es." });"""


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

    tausche(CSS_ANKER, CSS_NEU, "CSS fuer Aufgaben und Hinweise")
    tausche(FEHLT_ANKER, FEHLT_NEU, "wasFehlt() + aufgabenBlock()")
    tausche(WOCHE_ANKER, WOCHE_NEU, "Aufgaben-Block oben einhaengen")
    tausche(KARTE_ANKER, KARTE_NEU, "Karte: Fehlt-Zeilen + Sprechtext")
    tausche(HOCH_ANKER, HOCH_NEU, "Karte: Knopf Video hochladen")
    tausche(HANDLER_ANKER, HANDLER_NEU, "Upload-Handler")
    tausche(SAVE_ANKER, SAVE_NEU, "hinweis speichern")
    tausche(LESE_ANKER, LESE_NEU, "hinweis lesen")
    tausche(LEER_ANKER, LEER_NEU, "leere Entwuerfe aus der Liste nehmen")
    tausche(ORT_ANKER, ORT_NEU, "Hinweistext: Knopf sitzt links unter dem Cover")

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
