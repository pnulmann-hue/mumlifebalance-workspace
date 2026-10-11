# -*- coding: utf-8 -*-
"""Tägliche Storys in die Wochen-Vorschau, und der Weg in den Bild-Editor für alles
(14.09.2026).

Patricias zwei Befunde:
1. „wo kommen die täglichen storys denn hin?" — Sie standen nur im Bild-Editor unter
   „Aus deiner Planung". In der Wochen-Vorschau, wo sie freitags prüft, fehlten sie.
2. „hier kann ich auf die funktionen vom bildeditor wieder nicht zugreifen" — Der Knopf
   „Im Bild-Editor bauen" gab es nur beim Karussell. Reels und Storys hatten keinen.

Also: Storys erscheinen Tag für Tag in der Wochen-Vorschau, und jede Karte führt in den
Bild-Editor. Storys werden dort nur freigegeben, nicht an Blotato gegeben — die postet
Patricia selbst vom Handy.

Wiederholbar.
"""
import io, os

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
PFAD = "outputs/cockpit/mlb-cockpit.html"
t = io.open(PFAD, encoding="utf-8").read()
vorher = t
getan, schon = [], []


def setze(alt, neu, was, marker):
    global t
    if alt in t:
        t = t.replace(alt, neu, 1)
        getan.append(was)
    elif marker in t:
        schon.append(was)
    else:
        print("!! Anker nicht gefunden:", was)


# 1 — Story merkt sich Datum und Freigabe
setze("""      db.collection("storys").doc(st.id).set({
        name: st.name, brand: st.brand, phase: st.phase || "", frames: st.frames, updatedAt: st.updatedAt
      })""",
      """      db.collection("storys").doc(st.id).set({
        name: st.name, brand: st.brand, phase: st.phase || "", frames: st.frames,
        datum: st.datum || "", textfrei: !!st.textfrei, updatedAt: st.updatedAt
      })""",
      "Story speichert Datum und Freigabe",
      marker='datum: st.datum || "", textfrei:')

setze("""          var st = { id: doc.id, name: d0.name || "Sequenz", brand: d0.brand || "mlb_dark", handle: d0.handle || "", phase: d0.phase || "", frames: d0.frames, updatedAt: d0.updatedAt || "" };""",
      """          var st = { id: doc.id, name: d0.name || "Sequenz", brand: d0.brand || "mlb_dark", handle: d0.handle || "", phase: d0.phase || "", frames: d0.frames, datum: d0.datum || "", textfrei: !!d0.textfrei, updatedAt: d0.updatedAt || "" };""",
      "Story liest Datum und Freigabe",
      marker='frames: d0.frames, datum: d0.datum')

# 2 — Storys wandern in die Wochen-Vorschau
setze("""    state.karussells.forEach(function (c) {
      var s1 = (c.slides && c.slides[0]) || {};
      beitraege.push({ art: "karussells", id: c.id, obj: c, format: "Karussell",
                       titel: c.name, hook: s1.headline || "",
                       unter: (c.slides ? c.slides.length : 0) + " Folien",
                       caption: c.caption || "", datei: "" });
    });""",
      """    state.karussells.forEach(function (c) {
      var s1 = (c.slides && c.slides[0]) || {};
      beitraege.push({ art: "karussells", id: c.id, obj: c, format: "Karussell",
                       titel: c.name, hook: s1.headline || "",
                       unter: (c.slides ? c.slides.length : 0) + " Folien",
                       caption: c.caption || "", datei: "" });
    });
    // Die taeglichen Storys gehoeren hierher, nicht nur in den Bild-Editor —
    // hier prueft Patricia am Freitag.
    state.storys.forEach(function (s) {
      var f1 = (s.frames && s.frames[0]) || {};
      beitraege.push({ art: "storys", id: s.id, obj: s, format: "Story",
                       titel: s.name, hook: f1.text || "",
                       unter: (s.frames ? s.frames.length : 0) + " Folien",
                       caption: "", datei: "" });
    });""",
      "Storys erscheinen in der Wochen-Vorschau",
      marker='art: "storys", id: s.id')

# 3 — Story-Folien auf der Karte zeigen
setze("""        (b.art === "karussells" ? '<div class="wk-folien"></div>' : "") +""",
      """        (b.art === "karussells" || b.art === "storys" ? '<div class="wk-folien"></div>' : "") +""",
      "Platz fuer die Story-Folien auf der Karte",
      marker='b.art === "karussells" || b.art === "storys" ? \'<div class="wk-folien">')

setze("""          (b.art === "karussells" ? '<button class="btn">Im Bild-Editor bauen</button>' : "") +""",
      """          '<button class="btn">Im Bild-Editor bauen</button>' +""",
      "Der Weg in den Bild-Editor gilt fuer alles",
      marker="'<button class=\"btn\">Im Bild-Editor bauen</button>' +\n          '<button class=\"btn'")

# 4 — Story-Folien zeichnen
setze("""    // Folien des Karussells zeichnen — dieselben Canvas-Slides wie im Editor
    var folienbox = karte.querySelector(".wk-folien");
    if (folienbox && b.obj.slides) {""",
      """    // Story-Folien zeichnen, mit Text zum Aendern daneben
    var storybox = karte.querySelector(".wk-folien");
    if (storybox && b.art === "storys" && b.obj.frames) {
      b.obj.frames.forEach(function (fr, i) {
        var sp = document.createElement("div");
        sp.className = "wk-folienkarte";
        var c = document.createElement("canvas");
        c.className = "wk-folie";
        sp.appendChild(c);
        renderStoryFrame(c, fr, b.obj, i, b.obj.frames.length);
        var nr = document.createElement("div");
        nr.className = "wk-folienr";
        nr.textContent = "Folie " + (i + 1);
        sp.appendChild(nr);
        var ta = document.createElement("textarea");
        ta.className = "wk-folienfeld";
        ta.rows = 3;
        ta.placeholder = "Text auf der Folie";
        ta.value = fr.text || "";
        ta.oninput = function () {
          fr.text = this.value;
          renderStoryFrame(c, fr, b.obj, i, b.obj.frames.length);
          saveStory(b.obj);
        };
        sp.appendChild(ta);
        storybox.appendChild(sp);
      });
    }

    // Folien des Karussells zeichnen — dieselben Canvas-Slides wie im Editor
    var folienbox = karte.querySelector(".wk-folien");
    if (folienbox && b.art === "karussells" && b.obj.slides) {""",
      "Story-Folien werden auf der Karte gezeichnet",
      marker="b.art === \"storys\" && b.obj.frames")

# 5 — Speichern je Art, und Storys gehen nicht an Blotato
setze("""    felder[0].onchange = function () {
      b.obj.datum = this.value;
      if (b.art === "reels") saveReel(b.obj); else saveCarousel(b.obj);
      render();
    };""",
      """    function merken() {
      if (b.art === "reels") saveReel(b.obj);
      else if (b.art === "storys") saveStory(b.obj);
      else saveCarousel(b.obj);
    }
    felder[0].onchange = function () {
      b.obj.datum = this.value;
      merken();
      render();
    };""",
      "Speichern kennt jetzt auch die Story",
      marker="function merken() {")

setze("""      felder[2].onclick = function () {
        // Gebaut wird im Bild-Editor — hier wird nur geprüft und freigegeben.
        activeCarousel = b.obj.id;
        window.open(BILDEDITOR, "_blank", "noopener");
      };""",
      """    felder[2].onclick = function () {
      // Gebaut wird im Bild-Editor — hier wird nur geprüft und freigegeben.
      if (b.art === "karussells") activeCarousel = b.obj.id;
      window.open(BILDEDITOR, "_blank", "noopener");
    };""",
      "Knopf in den Bild-Editor fuer jede Art",
      marker="if (b.art === \"karussells\") activeCarousel = b.obj.id;")

setze("""    if (b.art === "karussells") {
    felder[2].onclick""",
      """    felder[2].onclick""",
      "Bedingung um den Knopf entfernt",
      marker="    felder[2].onclick = function () {\n      // Gebaut wird")

setze("""      window.open(BILDEDITOR, "_blank", "noopener");
    };
    }
    var profilWahl""",
      """      window.open(BILDEDITOR, "_blank", "noopener");
    };
    var profilWahl""",
      "Klammer der alten Bedingung entfernt",
      marker='window.open(BILDEDITOR, "_blank", "noopener");\n    };\n    var profilWahl')

setze("""      var an = !b.obj.textfrei;
      b.obj.textfrei = an;
      if (b.art === "reels") saveReel(b.obj); else saveCarousel(b.obj);""",
      """      var an = !b.obj.textfrei;
      b.obj.textfrei = an;
      merken();

      // Storys postet Patricia selbst vom Handy — die gehen nie an Blotato.
      if (b.art === "storys") {
        toast(an ? "Story freigegeben" : "Freigabe zurückgenommen");
        render();
        return;
      }""",
      "Storys werden nur freigegeben, nicht eingeplant",
      marker="Storys postet Patricia selbst vom Handy")

setze("""        bl.status = "wartet";
          if (b.art === "reels") saveReel(b.obj); else saveCarousel(b.obj);""",
      """        bl.status = "wartet";
          merken();""",
      "Freigabe-Vermerk ueber merken()",
      marker='bl.status = "wartet";\n          merken();')

if t != vorher:
    io.open(PFAD, "w", encoding="utf-8", newline="\n").write(t)

print("Geaendert:")
for z in getan:
    print("  +", z)
if schon:
    print("Schon so:")
    for z in schon:
        print("  =", z)
if not getan:
    print("  (nichts zu tun)")
