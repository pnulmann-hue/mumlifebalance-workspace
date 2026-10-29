"""Story-Bibliothek: die Story von heute zuerst, dann der Reihe nach.

    python scripts/cockpit/patch-story-reihenfolge.py

Patricia, 27.10.2026: „kannst du mir die storys im cockpit noch so sortieren, dass immer
direkt die story vom tag kommt und dann der reihe nach? jetzt ist ein durcheinander“.
Bis dahin sortierte die Auswahl nach `updatedAt` — wer eine Story bearbeitet, schob sie
nach oben, und die Tage lagen kreuz und quer.

Reihenfolge: Heute (Mentoring vor doTERRA) · nächste Tage aufsteigend · ohne Datum ·
vorbei, jüngste zuerst. Die Auswahl zeigt das in Gruppen. Beim Öffnen steht die Story
von heute da, solange Patricia nicht selbst eine andere gewählt hat.
Wiederholbar: ein zweiter Lauf ändert nichts.
"""
import pathlib
import re
import subprocess
import sys

DATEI = pathlib.Path(__file__).resolve().parents[2] / "outputs" / "cockpit" / "mlb-cockpit.html"
MARKE = "/* @@story-reihenfolge */"

t = DATEI.read_text(encoding="utf-8")
if MARKE in t:
    print("schon eingebaut")
    sys.exit(0)

FUNK = MARKE + r'''
  var storyGewaehlt = false;
  function heuteIso() {
    var d = new Date();
    return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0");
  }
  function storyGruppe(st, heute) {
    var d = st.datum || "";
    if (!d) return 2;
    if (d === heute) return 0;
    return d > heute ? 1 : 3;
  }
  function storyReihe() {
    var heute = heuteIso();
    var prof = function (st) { return st.profil === "doterra" ? 1 : 0; };
    state.storys.sort(function (a, b) {
      var ga = storyGruppe(a, heute), gb = storyGruppe(b, heute);
      if (ga !== gb) return ga - gb;
      if (ga === 1 && a.datum !== b.datum) return a.datum < b.datum ? -1 : 1;
      if (ga === 3 && a.datum !== b.datum) return a.datum > b.datum ? -1 : 1;
      if (ga === 2) return (b.updatedAt || "") < (a.updatedAt || "") ? -1 : 1;
      return prof(a) - prof(b) || ((a.name || "") < (b.name || "") ? -1 : 1);
    });
  }

  function renderStorys(main) {'''

ers = [
    # 1 · Sortierfunktion vor die Bibliothek
    ("\n  function renderStorys(main) {", "\n  " + FUNK),
    # 2 · Auswahl in Gruppen
    ('''      state.storys.forEach(function (x) {
        var o = document.createElement("option");
        o.value = x.id; o.textContent = x.name + " (" + x.frames.length + ")";
        if (st && x.id === st.id) o.selected = true;
        pick.appendChild(o);
      });
      pick.onchange = function () { activeStory = pick.value; render(); };''',
     '''      storyReihe();
      var heute = heuteIso(), titel = ["Heute", "Nächste Tage", "Ohne Datum", "Vorbei"], gruppen = {};
      state.storys.forEach(function (x) {
        var g = storyGruppe(x, heute);
        if (!gruppen[g]) { gruppen[g] = document.createElement("optgroup"); gruppen[g].label = titel[g]; pick.appendChild(gruppen[g]); }
        var o = document.createElement("option");
        o.value = x.id; o.textContent = x.name + " (" + x.frames.length + ")";
        if (st && x.id === st.id) o.selected = true;
        gruppen[g].appendChild(o);
      });
      pick.onchange = function () { activeStory = pick.value; storyGewaehlt = true; render(); };'''),
    # 3 · nach dem Laden aus dem Browser
    ("  if (state.storys.length) activeStory = state.storys[0].id;\n",
     "  storyReihe();\n  if (state.storys.length) activeStory = state.storys[0].id;\n"),
    # 4 · nach dem Laden aus der Datenbank
    ('''        state.storys.sort(function (a, b) { return (b.updatedAt || "") < (a.updatedAt || "") ? -1 : 1; });
        if (!activeStory && state.storys.length) activeStory = state.storys[0].id;''',
     '''        storyReihe();
        if ((!activeStory || !storyGewaehlt) && state.storys.length) activeStory = state.storys[0].id;'''),
]
for alt, neu in ers:
    assert t.count(alt) == 1, ("nicht genau einmal gefunden", alt[:70], t.count(alt))
    t = t.replace(alt, neu)

# Gegenprobe: das Skript muss sich parsen lassen
skripte = re.findall(r"<script>(.*?)</script>", t, re.S)
probe = DATEI.with_name("_probe-story.js")
probe.write_text(max(skripte, key=len), encoding="utf-8")
try:
    r = subprocess.run(["node", "--check", str(probe)], capture_output=True, text=True)
finally:
    probe.unlink()
if r.returncode:
    sys.exit("Skript kaputt, nichts geschrieben:\n" + r.stderr)

DATEI.write_text(t, encoding="utf-8")
print("eingebaut: Heute · Nächste Tage · Ohne Datum · Vorbei")
