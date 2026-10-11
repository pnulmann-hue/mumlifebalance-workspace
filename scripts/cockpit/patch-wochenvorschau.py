"""
Baut die Wochen-Vorschau ins Cockpit.

Patricia will Tag fuer Tag sehen, was rausgeht — Cover, Hook, Caption, Hashtags,
und einen Freigabe-Knopf pro Beitrag. Die bestehenden Reiter sind nach Format
sortiert, nicht nach Tag.

Was der Patch aendert:
  1  neuer Reiter „Wochen-Vorschau"
  2  Datum an Reels und Karussells (gab es bisher nicht)
  3  Freigabe-Flag auch fuer Reels (Karussells hatten schon „textfrei")
  4  renderWoche(): Karten nach Datum sortiert, Reels und Karussells gemischt

Jede Ersetzung schlaegt laut fehl, wenn ihr Anker fehlt — lieber ein Abbruch
als eine halb gepatchte Datei.

Aufruf:
  python scripts/cockpit/patch-wochenvorschau.py [--pruefen]
"""
import io
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]
DATEI = ROOT / "outputs" / "cockpit" / "mlb-cockpit.html"

ERSETZUNGEN = []


def patch(name, alt, neu):
    ERSETZUNGEN.append((name, alt, neu))


# --------------------------------------------------------------------------
# 1 · Reiter
# --------------------------------------------------------------------------
patch("Reiter in der Navigation",
      '    { g: "Planen" },\n    { id: "posts", label: "Content-Planung" },',
      '    { g: "Planen" },\n'
      '    { id: "woche", label: "Wochen-Vorschau" },\n'
      '    { id: "posts", label: "Content-Planung" },')

patch("Router",
      '    else if (activeTab === "zahlen") renderZahlen(main);',
      '    else if (activeTab === "woche") renderWoche(main);\n'
      '    else if (activeTab === "zahlen") renderZahlen(main);')

# --------------------------------------------------------------------------
# 2 · Datum und Freigabe mitspeichern
# --------------------------------------------------------------------------
patch("Karussell speichern: Datum mit",
      '        typ: car.typ || "listicle", funnel: car.funnel || "TOF",\n'
      '        textfrei: !!car.textfrei, blotato: car.blotato || null,',
      '        typ: car.typ || "listicle", funnel: car.funnel || "TOF",\n'
      '        datum: car.datum || "",\n'
      '        textfrei: !!car.textfrei, blotato: car.blotato || null,')

patch("Reel speichern: Datum und Freigabe mit",
      '        name: r.name, hook: r.hook, unter: r.unter, pos: r.pos, brand: r.brand,\n'
      '        scrim: !!r.scrim, skript: r.skript || "", caption: r.caption || "",',
      '        name: r.name, hook: r.hook, unter: r.unter, pos: r.pos, brand: r.brand,\n'
      '        datum: r.datum || "", textfrei: !!r.textfrei,\n'
      '        scrim: !!r.scrim, skript: r.skript || "", caption: r.caption || "",')

patch("Reel laden: Datum und Freigabe uebernehmen",
      'var rl = { id: doc.id, name: d0.name || "Reel", hook: d0.hook || "", '
      'unter: d0.unter || "", pos: d0.pos || "unten", brand: d0.brand || "mlb_dark", '
      'scrim: d0.scrim !== false,',
      'var rl = { id: doc.id, name: d0.name || "Reel", hook: d0.hook || "", '
      'unter: d0.unter || "", pos: d0.pos || "unten", brand: d0.brand || "mlb_dark", '
      'datum: d0.datum || "", textfrei: !!d0.textfrei, scrim: d0.scrim !== false,')

patch("Karussell laden: Datum uebernehmen",
      'var car = { id: doc.id, name: d0.name || "Karussell", br',
      'var car = { id: doc.id, datum: d0.datum || "", name: d0.name || "Karussell", br')

# --------------------------------------------------------------------------
# 3 · Stil fuer die Wochenkarten
# --------------------------------------------------------------------------
patch("Stil der Wochenkarten",
      "  /* Text-Freigabe */",
      """  /* ---------- Wochen-Vorschau ---------- */
  .wochentag { margin-bottom: 22px; }
  .wt-kopf { display: flex; align-items: baseline; gap: 10px; margin-bottom: 10px; }
  .wt-kopf .wt-name { font-family: var(--display); font-size: 18px; }
  .wt-kopf .wt-datum { font-size: 12px; color: var(--ink-soft); font-variant-numeric: tabular-nums; }
  .wkarte {
    display: grid; grid-template-columns: 190px 1fr; gap: 18px;
    background: var(--surface); border: 1px solid var(--line); border-radius: var(--r);
    padding: 16px 18px; margin-bottom: 12px; box-shadow: var(--shadow);
    border-left: 3px solid var(--orange);
  }
  .wkarte.frei { border-left-color: var(--good); }
  @media (max-width: 760px) { .wkarte { grid-template-columns: 1fr; } }
  .wkarte .wk-bild { width: 100%; border-radius: 8px; display: block; background: var(--surface-2); }
  .wkarte .wk-leer {
    aspect-ratio: 9/16; border: 1px dashed var(--line-strong); border-radius: 8px;
    display: flex; align-items: center; justify-content: center; text-align: center;
    color: var(--ink-soft); font-size: 12px; padding: 10px;
  }
  .wk-haupt { min-width: 0; display: flex; flex-direction: column; gap: 10px; }
  .wk-zeile { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }
  .wk-hook { font-family: var(--display); font-size: 17px; line-height: 1.3; }
  .wk-unter { font-size: 13px; color: var(--ink-soft); }
  .wk-caption {
    white-space: pre-wrap; font-size: 13px; line-height: 1.6; background: var(--ground);
    border: 1px solid var(--line); border-radius: 8px; padding: 11px 13px;
    max-height: 168px; overflow-y: auto; margin: 0;
  }
  .wk-tags { font-size: 12px; color: var(--teal); word-break: break-word; }
  .wk-fuss { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }
  .wk-fuss input[type="date"] {
    background: var(--ground); border: 1px solid var(--line); border-radius: 7px;
    padding: 6px 8px; font-size: 12px;
  }
  .wk-datei { font-size: 12px; color: var(--ink-soft); font-family: var(--body); }

  /* Text-Freigabe */""")

# --------------------------------------------------------------------------
# 4 · Die Ansicht selbst
# --------------------------------------------------------------------------
patch("renderWoche",
      "  function renderNav() {",
      """  /* =========================================================
     Wochen-Vorschau: Tag fuer Tag, Reels und Karussells gemischt
     ========================================================= */
  var wochenbilder = {};          // beitragId -> dataURL des Covers
  var wochenbilderGeholt = {};

  function wochenBildHolen(art, id) {
    if (!db || wochenbilderGeholt[id]) return;
    wochenbilderGeholt[id] = true;
    db.doc(art + "/" + id).collection("bilder").doc("cover").get()
      .then(function (d) {
        var u = d && d.data && (d.data() || {}).dataUrl;
        if (!u) return;
        wochenbilder[id] = u;
        if (activeTab === "woche") render();
      }).catch(function () {});
  }

  var WOCHENTAGE = ["Sonntag", "Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag"];

  function tagName(iso) {
    var t = new Date(iso + "T12:00:00");
    return isNaN(t) ? "" : WOCHENTAGE[t.getDay()];
  }

  function hashtagsTrennen(caption) {
    var text = String(caption || "");
    var zeilen = text.split("\\n");
    for (var i = zeilen.length - 1; i >= 0; i--) {
      var z = zeilen[i].trim();
      if (!z) continue;
      if (z.indexOf("#") === 0) {
        return { text: zeilen.slice(0, i).join("\\n").replace(/\\s+$/, ""), tags: z };
      }
      break;
    }
    return { text: text, tags: "" };
  }

  function renderWoche(main) {
    var beitraege = [];
    state.reels.forEach(function (r) {
      beitraege.push({ art: "reels", id: r.id, obj: r, format: "Reel",
                       titel: r.name, hook: r.hook || "", unter: r.unter || "",
                       caption: r.caption || "", datei: r.videodatei || "" });
    });
    state.karussells.forEach(function (c) {
      var s1 = (c.slides && c.slides[0]) || {};
      beitraege.push({ art: "karussells", id: c.id, obj: c, format: "Karussell",
                       titel: c.name, hook: s1.headline || "",
                       unter: (c.slides ? c.slides.length : 0) + " Folien",
                       caption: c.caption || "", datei: "" });
    });

    beitraege.forEach(function (b) { wochenBildHolen(b.art, b.id); });

    var mitDatum = beitraege.filter(function (b) { return b.obj.datum; })
      .sort(function (a, b) { return a.obj.datum < b.obj.datum ? -1 : 1; });
    var ohneDatum = beitraege.filter(function (b) { return !b.obj.datum; });
    var frei = beitraege.filter(function (b) { return b.obj.textfrei; }).length;

    main.innerHTML =
      '<div class="page-head"><div><h1>Wochen-Vorschau</h1>' +
      '<p>Jeder Beitrag so, wie er rausgeht: Cover, Hook, Caption und Hashtags. ' +
      'Trag ein Datum ein, dann sortiert er sich in den Tag ein. Freigeben heisst, ' +
      'dass die Texte stehen — Reels lädst du dir danach aufs Handy und postest von dort.</p></div>' +
      '<div class="head-actions"><span class="chip">' + frei + ' von ' + beitraege.length +
      ' freigegeben</span></div></div>' +
      '<div id="wliste"></div>';

    var liste = main.querySelector("#wliste");

    if (!beitraege.length) {
      liste.innerHTML = '<div class="panel"><div class="empty">Noch keine Beiträge da. ' +
        'Sobald welche im Reel- oder Karussell-Studio liegen, stehen sie hier.</div></div>';
      return;
    }

    var letzterTag = "";
    mitDatum.forEach(function (b) {
      if (b.obj.datum !== letzterTag) {
        letzterTag = b.obj.datum;
        var kopf = document.createElement("div");
        kopf.className = "wt-kopf";
        kopf.innerHTML = '<span class="wt-name">' + esc(tagName(b.obj.datum)) + '</span>' +
                         '<span class="wt-datum">' + esc(b.obj.datum) + '</span>';
        liste.appendChild(kopf);
      }
      liste.appendChild(wochenKarte(b));
    });

    if (ohneDatum.length) {
      var kopf2 = document.createElement("div");
      kopf2.className = "wt-kopf";
      kopf2.innerHTML = '<span class="wt-name">Ohne Datum</span>' +
                        '<span class="wt-datum">' + ohneDatum.length + ' Beiträge</span>';
      liste.appendChild(kopf2);
      ohneDatum.forEach(function (b) { liste.appendChild(wochenKarte(b)); });
    }
  }

  function wochenKarte(b) {
    var zerlegt = hashtagsTrennen(b.caption);
    var karte = document.createElement("div");
    karte.className = "wkarte" + (b.obj.textfrei ? " frei" : "");

    var bild = wochenbilder[b.id]
      ? '<img class="wk-bild" src="' + wochenbilder[b.id] + '" alt="">'
      : '<div class="wk-leer">Noch kein Vorschaubild</div>';

    karte.innerHTML =
      '<div>' + bild + '</div>' +
      '<div class="wk-haupt">' +
        '<div class="wk-zeile">' +
          '<span class="chip' + (b.format === "Reel" ? "" : " orange") + '">' + b.format + '</span>' +
          '<strong>' + esc(b.titel) + '</strong>' +
        '</div>' +
        (b.hook ? '<div class="wk-hook">' + esc(b.hook) + '</div>' : "") +
        (b.unter ? '<div class="wk-unter">' + esc(b.unter) + '</div>' : "") +
        '<pre class="wk-caption">' + esc(zerlegt.text || "Noch keine Caption.") + '</pre>' +
        (zerlegt.tags ? '<div class="wk-tags">' + esc(zerlegt.tags) + '</div>' : "") +
        (b.datei ? '<div class="wk-datei">Datei: ' + esc(b.datei) + '</div>' : "") +
        '<div class="wk-fuss">' +
          '<input type="date" value="' + esc(b.obj.datum || "") + '">' +
          '<button class="btn">Caption kopieren</button>' +
          '<button class="btn' + (b.obj.textfrei ? "" : " primary") + '">' +
            (b.obj.textfrei ? "Freigabe zurücknehmen" : "Freigeben") + '</button>' +
        '</div>' +
      '</div>';

    var felder = karte.querySelectorAll(".wk-fuss input, .wk-fuss button");
    felder[0].onchange = function () {
      b.obj.datum = this.value;
      if (b.art === "reels") saveReel(b.obj); else saveCarousel(b.obj);
      render();
    };
    felder[1].onclick = function () {
      var t = b.caption || "";
      if (navigator.clipboard) {
        navigator.clipboard.writeText(t).then(function () { toast("Caption kopiert"); },
                                              function () { toast("Kopieren hat nicht geklappt"); });
      }
    };
    felder[2].onclick = function () {
      b.obj.textfrei = !b.obj.textfrei;
      if (b.art === "reels") saveReel(b.obj); else saveCarousel(b.obj);
      toast(b.obj.textfrei ? "Freigegeben" : "Freigabe zurückgenommen");
      render();
    };
    return karte;
  }

  function renderNav() {""")


def main():
    nur_pruefen = "--pruefen" in sys.argv
    s = io.open(DATEI, encoding="utf-8").read()
    vorher = len(s)
    for name, alt, neu in ERSETZUNGEN:
        if alt not in s:
            sys.exit("Anker fehlt fuer: %s\n  gesucht: %s" % (name, alt[:110]))
        if s.count(alt) > 1:
            sys.exit("Anker mehrdeutig (%dx) fuer: %s" % (s.count(alt), name))
        s = s.replace(alt, neu, 1)
        print("  OK  %s" % name)
    print("\nLaenge %d -> %d (%+d)" % (vorher, len(s), len(s) - vorher))
    if nur_pruefen:
        print("PRUEFLAUF — nichts geschrieben.")
        return
    io.open(DATEI, "w", encoding="utf-8").write(s)
    print("Geschrieben: %s" % DATEI)


if __name__ == "__main__":
    main()
