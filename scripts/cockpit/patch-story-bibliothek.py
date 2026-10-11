"""Story-Bibliothek im Cockpit: schönere erste Vorschläge, Gestaltung je Folie (08.10.2026).

Patricia: *„ich hätte gerne, dass der erste vorschlag von dir noch etwas schöner
daherkommt, gerade auch die slides, wo es dann effektiv um den kurs geht … die
schriften nach meinem branding … texte zentriert, rechts oder links … mit
textbalken oder ohne … sticker, umfragen etc."* — und: *„ich hätte das im
übrigen immer noch gerne in der storybibliothek unter dem cockpit selber und
nicht separat"*.

Ersetzt im Cockpit den Story-Zeichner und die Folienkarte durch zwei Dateien
daneben (eigene Dateien, damit `node --check` sie einzeln prüfen kann):
  story-bibliothek.js  renderStoryFrame + Stil-Vorgaben je Layout
  story-karte.js       storyCard mit „Gestalten“, Export mit Warten auf Foto+Schrift

Neu je Folie: schrift (Philosopher · kursiv · Source Sans leicht · fett) ·
align (links/Mitte/rechts) · balken (ohne/Zeilen/Karte) · hg (Foto/dunkel/
creme/petrol/orange) · foto (Shootingbild s01–s12) · pos · groesse · verlauf ·
sticker + stickerText (nur Platzhalter in der Vorschau, im Export leer) ·
eyebrow · pille · punkte · klein · notiz (✏️-Hinweis, nie im Bild).
Neue Layouts: learning · kurs · bonus.

🚨 Ältere Folien hatten den Sticker-Hinweis in `cta` und bekamen ihn als
orange Pille INS Bild gemalt. `stilVon()` macht daraus die Sticker-Fläche.

Läuft nach den Tisch-Patches; berührt den Launch-Reiter (andere Sitzung) nicht.

    python scripts/cockpit/patch-story-bibliothek.py [--datei <pfad>]
"""

import argparse
import importlib.util
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HIER = Path(__file__).resolve().parent
ROOT = HIER.parents[1]
MARKE = "Story-Bibliothek (08.10.2026)"

ALT_ZEICHNER_START = ("  /* =========================================================\n"
                      "     Story-Rendering (1080 x 1920)\n")
ALT_ZEICHNER_ENDE = ("  /* =========================================================\n"
                     "     Story-Studio\n")
ALT_KARTE_START = "  function storyCard(st, fr, i) {\n"
NEU_ZEICHNER_START = ("  /* =========================================================\n"
                      "     Story-Rendering (1080 x 1920) — Story-Bibliothek")
NEU_KARTE_START = "  /* Eine Folie in der Story-Bibliothek"
FOKUS_START = "  /* Fokus-Ansicht (08.10.2026"
ALT_KARTE_ENDE = ("  /* =========================================================\n"
                  "     Mein Wissen\n")

CSS_ANKER = "  .storystrip {"
CSS = """  /* Story-Bibliothek (08.10.2026) */
  .storystrip .storycard { flex: 0 0 280px; }
  .sc-notiz { font-size: 12.5px; background: var(--orange-soft, #fbeadb); border-left: 3px solid #dc822e;
              padding: 6px 8px; border-radius: 6px; }
  .sc-gestalten summary { cursor: pointer; font-weight: 600; font-size: 13px; padding: 4px 0; }
  .sc-gestalten[open] { display: flex; flex-direction: column; gap: 8px; }
  .sc-seg span { display: block; font-size: 11px; letter-spacing: .06em; text-transform: uppercase;
                 color: var(--ink-soft); margin-bottom: 3px; }
  .sc-seg > div { display: flex; gap: 4px; flex-wrap: wrap; }
  .sc-seg button { flex: 1 1 0; min-width: 34px; min-height: 30px; border: 1px solid var(--line);
                   background: var(--surface); border-radius: 8px; cursor: pointer; font-size: 13px; }
  .sc-seg button[aria-pressed="true"] { outline: 2px solid #dc822e; outline-offset: 1px; }
  .sc-seg select, .sc-seg input { width: 100%; margin-top: 4px; }
  .sc-fotos { display: flex; flex-wrap: wrap; gap: 4px; }
  .sc-fotos img { width: 38px; height: 52px; object-fit: cover; border-radius: 6px; cursor: pointer;
                  border: 2px solid transparent; }
  .sc-fotos img.sel { border-color: #dc822e; }
  .sc-fotos .filebtn { width: 100%; margin-top: 4px; }
  .sc-extra { border: 1px dashed var(--line-strong); border-radius: 8px; padding: 6px 8px;
              display: flex; flex-direction: column; gap: 6px; }
  .sc-extrakopf { display: flex; align-items: center; font-size: 11px; letter-spacing: .06em;
                  text-transform: uppercase; color: var(--ink-soft); }
  .sc-extrakopf .btn { margin-left: auto; }
  .sc-plus { display: flex; flex-wrap: wrap; gap: 4px; }
  .sc-plus .btn { font-size: 12px; padding: 4px 8px; border: 1px dashed var(--line-strong); }
"""

ALT_STRIP = '  function renderStoryStrip(strip, st) {\n    strip.innerHTML = "";\n    st.frames.forEach(function (fr, i) { strip.appendChild(storyCard(st, fr, i)); });\n    var add = document.createElement("button");\n    add.className = "addslide";\n    add.textContent = "+ Folie";\n    add.onclick = function () {\n      st.frames.push({ id: uid("fr"), layout: "text", text: "", zoom: 1, ox: 0, oy: 0 });\n      saveStory(st); renderStoryStrip(strip, st);\n    };\n    strip.appendChild(add);\n  }\n\n'

CSS_FOKUS = """  /* Fokus-Ansicht (V94): Miniaturen oben, eine Folie gross, Vorschau bleibt stehen */
  .storystrip.st-neu { display: block; overflow: visible; }
  .st-leiste { display: flex; gap: 8px; overflow-x: auto; padding: 4px 2px 14px; }
  .st-mini { flex: 0 0 64px; position: relative; padding: 0; border: 2px solid transparent;
             border-radius: 9px; background: none; cursor: pointer; }
  .st-mini canvas { display: block; width: 60px; height: auto; border-radius: 7px; background: #29556d; }
  .st-mini span { position: absolute; left: 4px; top: 4px; font-size: 10px; line-height: 1.5;
                  background: rgba(12,28,48,.72); color: #fff; border-radius: 99px; padding: 0 6px; }
  .st-mini.an { border-color: #dc822e; }
  .st-neue { border: 1px dashed var(--line-strong); color: var(--ink-soft); font-size: 12px;
             min-height: 106px; }
  .storystrip.st-neu .storycard { width: 100%; flex: none; display: grid; overflow: visible;
                       grid-template-columns: minmax(240px, 360px) minmax(0, 1fr); }
  .st-neu .storycard > .sc-head { grid-column: 1 / -1; }
  .st-neu .storycard canvas.sc-gross { position: sticky; top: 76px; align-self: start;
                                       width: 100%; height: auto; }
  @media (max-width: 760px) {
    .storystrip.st-neu .storycard { grid-template-columns: 1fr; }
    .st-neu .storycard canvas.sc-gross { top: 118px; z-index: 5; width: auto; height: 46vh;
      margin: 0 auto; box-shadow: 0 6px 18px rgba(0,0,0,.25); border-radius: 10px; }
  }
"""

ERSETZUNGEN = [
    # Neue Folien behalten alle Felder (vorher wurden Gestaltungsfelder abgeschnitten)
    ('        return { id: uid("fr"), layout: f.layout || "text", text: f.text || "", cta: f.cta || "", '
     'optA: f.optA || "", optB: f.optB || "", zoom: 1, ox: 0, oy: 0 };\n',
     '        return Object.assign({ layout: "text", text: "", cta: "", optA: "", optB: "", zoom: 1, ox: 0, oy: 0 },\n'
     '          tief(f), { id: uid("fr") });\n'),
    ("'<div class=\"page-head\"><div><h1>Story-Studio</h1>' +\n"
     "      '<p>Story-Sequenzen im Hochformat, mit Fragebox und Umfrage als echtem Bildelement. "
     "Exportiert als PNG, die Sticker legst du in Instagram nur noch drüber, wenn du sie klickbar willst.</p></div>' +\n",
     "'<div class=\"page-head\"><div><h1>Story-Bibliothek</h1>' +\n"
     "      '<p>Jede Folie lässt sich unter „Gestalten“ anpassen: Schrift, links/Mitte/rechts, mit oder ohne "
     "Textbalken, Foto aus deinem Shooting. Die gestrichelte Fläche ist der Platz für deinen Sticker — "
     "im Bild bleibt sie leer, den echten Sticker setzt du in Instagram drauf.</p></div>' +\n"),
    ("'<button class=\"btn primary\" id=\"stexport\">Alle Frames exportieren</button>' +\n",
     "'<button class=\"btn primary\" id=\"stexport\">Alle Folien als Bilder</button>' +\n"),
    ("      st.frames.push({ id: uid(\"fr\"), layout: \"text\", text: \"\", cta: \"\", optA: \"\", optB: \"\", "
     "zoom: 1, ox: 0, oy: 0 });\n",
     "      st.frames.push({ id: uid(\"fr\"), layout: \"text\", text: \"\", zoom: 1, ox: 0, oy: 0 });\n"),
    ("    add.textContent = \"+ Frame\";\n", "    add.textContent = \"+ Folie\";\n"),
    # 🚨 Nur 60 Sequenzen wurden geladen — mit den Launch-Storys fiel die neueste raus
    ('db.collection("storys").limit(60)', 'db.collection("storys").limit(200)'),
    # Schriften: Philosopher kursiv und Source Sans leicht dazuladen
    ("family=Philosopher:wght@400;700&family=Source+Sans+3:wght@400;600;700&display=swap",
     "family=Philosopher:ital,wght@0,400;0,700;1,400&family=Source+Sans+3:wght@300;400;600;700&display=swap"),
]


def ausschneiden(t, start, ende, neu):
    assert t.count(start) == 1, "Anfang fehlt/mehrdeutig: " + start[:60]
    a = t.index(start)
    b = t.index(ende, a)
    return t[:a] + neu + t[b:]


def patchen(t: str) -> str:
    if MARKE in t:
        # Nachbesserung: die beiden eigenen Blöcke durch den aktuellen Stand ersetzen
        z = (HIER / "story-bibliothek.js").read_text(encoding="utf-8").replace("\r\n", "\n")
        k = (HIER / "story-karte.js").read_text(encoding="utf-8").replace("\r\n", "\n")
        t = ausschneiden(t, NEU_ZEICHNER_START, ALT_ZEICHNER_ENDE, z)
        # Ab V94 beginnt der Karten-Block mit der Fokus-Ansicht davor — sonst
        # bliebe sie bei jedem Neulauf doppelt stehen.
        start = FOKUS_START if FOKUS_START in t else NEU_KARTE_START
        t = ausschneiden(t, start, ALT_KARTE_ENDE, k)
        t = t.replace('db.collection("storys").limit(60)', 'db.collection("storys").limit(200)')
        # 🚨 #0c1c30 ist Patricias TEXTfarbe, kein Hintergrund. Ihr Dunkelblau ist #29556d
        # (context/brand-identity.md). Patricia 08.10.: „nicht das richtige blau“.
        t = t.replace('bg: "#0c1c30", bg2: "#12283f", text: "#f1ecdd"', 'bg: "#29556d", bg2: "#1f4458", text: "#f1ecdd"')
        # Fokus-Ansicht (V94): alte Streifen-Funktion raus, Speichern ohne __-Felder
        t = t.replace(ALT_STRIP, "")
        t = t.replace("name: st.name, brand: st.brand, phase: st.phase || \"\", frames: st.frames,",
                      "name: st.name, brand: st.brand, phase: st.phase || \"\", frames: framesSauber(st.frames),")
        assert t.count("function renderStoryStrip(") == 1
        if "/* Fokus-Ansicht (V94)" in t:
            # Der Fokus-Block steht direkt vor dem .storystrip-Anker: bis dorthin ersetzen
            a0 = t.index("  /* Fokus-Ansicht (V94)")
            a1 = t.index(CSS_ANKER, a0)
            t = t[:a0] + t[a1:]
        assert t.count(CSS_ANKER) == 1
        t = t.replace(CSS_ANKER, CSS_FOKUS + CSS_ANKER)
        # CSS nachziehen: alles aus CSS, was noch fehlt, vor den .storystrip-Anker setzen
        if ".sc-extra {" not in t:
            rest = CSS[CSS.index("  .sc-extra {"):]
            assert t.count(CSS_ANKER) == 1
            t = t.replace(CSS_ANKER, rest + CSS_ANKER)
        print("Schon gepatcht — Zeichner und Karte aufgefrischt.")
        return t
    assert "function tief(x)" in t, "Erst patch-auftauen laufen lassen."
    zeichner = (HIER / "story-bibliothek.js").read_text(encoding="utf-8").replace("\r\n", "\n")
    karte = (HIER / "story-karte.js").read_text(encoding="utf-8").replace("\r\n", "\n")
    assert MARKE in zeichner
    t = ausschneiden(t, ALT_ZEICHNER_START, ALT_ZEICHNER_ENDE, zeichner)
    t = ausschneiden(t, ALT_KARTE_START, ALT_KARTE_ENDE, karte)
    assert t.count(CSS_ANKER) == 1, "CSS-Anker fehlt"
    t = t.replace(CSS_ANKER, CSS + CSS_ANKER)
    for alt, neu in ERSETZUNGEN:
        assert t.count(alt) == 1, "Anker fehlt oder ist mehrdeutig: " + alt[:80]
        t = t.replace(alt, neu)
    assert t.count("function renderStoryFrame(") == 1
    assert t.count("function storyCard(") == 1
    return t


def main():
    spec = importlib.util.spec_from_file_location("tisch", HIER / "patch-mein-tisch.py")
    tisch = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tisch)

    ap = argparse.ArgumentParser()
    ap.add_argument("--datei", default=str(ROOT / "outputs/cockpit/mlb-cockpit.html"))
    args = ap.parse_args()
    pfad = Path(args.datei)
    roh = pfad.read_bytes().decode("utf-8")
    crlf = "\r\n" in roh
    t = roh.replace("\r\n", "\n")
    neu = patchen(t)
    if neu == t:
        return
    tisch.node_check(neu)
    # Gegenprobe: der Launch-Reiter der anderen Sitzung muss unverändert drin sein
    if "Reiter Launch" in t:
        assert "Reiter Launch" in neu
    pfad.write_bytes((neu.replace("\n", "\r\n") if crlf else neu).encode("utf-8"))
    print("Story-Bibliothek eingebaut:", pfad)


if __name__ == "__main__":
    main()
