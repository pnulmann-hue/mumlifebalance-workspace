"""Baut die Öl-Wissensbasis (Artifact) aus context/doTERRA/Produktwissen/produkt-wissensbasis.json.

    python scripts/doterra/wissensbasis-bauen.py

Ausgabe: outputs/doterra-wissen/oel-wissen.html → mit dem Artifact-Tool (gleicher Pfad) neu veröffentlichen.
Neue Produkte nur in der JSON ergänzen, nie im HTML.
"""
import json
import pathlib

WS = pathlib.Path(__file__).resolve().parents[2]
QUELLE = WS / "context/doTERRA/Produktwissen/produkt-wissensbasis.json"
ZIEL = WS / "outputs/doterra-wissen/oel-wissen.html"

daten = json.loads(QUELLE.read_text(encoding="utf-8"))
pflicht = ["id", "name", "kategorie", "kurz", "anwendung", "kundinnentext"]
for p in daten["produkte"]:
    fehlt = [k for k in pflicht if not p.get(k)]
    assert not fehlt, f"{p.get('id')}: es fehlt {fehlt}"
ids = [p["id"] for p in daten["produkte"]]
assert len(ids) == len(set(ids)), "doppelte id"

# 🚨 Die Seite ist zum Teilen mit Kundinnen gedacht: Compliance-Hinweise und Patricias eigene Notizen
#    bleiben im Cockpit, hier kommen sie nicht mit.
oeffentlich = {k: v for k, v in daten.items() if k != "_info"}
oeffentlich["produkte"] = [{k: v for k, v in p.items() if k not in ("compliance", "patricia")}
                           for p in daten["produkte"]]
daten_js = json.dumps(oeffentlich, ensure_ascii=False).replace("</", "<\\/")

HTML = r"""<title>Öl-Wissen</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Philosopher:ital,wght@0,400;0,700;1,400&family=Source+Sans+3:wght@400;600;700&display=swap">
<style>
/* Layout: ruhige Nachschlage-Seite. Kopf mit Suche + Filter, darunter Karten in einer Spalte (breit: zwei). Öl-Abende als eigener Streifen oben. */
:root {
  --bg: #f6f2e7; --card: #fffdf8; --fg: #0c1c30; --muted: #5a6670; --line: #e3dccb;
  --blue: #29556d; --petrol: #2f7a78; --orange: #c86a24; --chip: #ebe4d3; --warn-bg: #fbeee3; --warn: #8a4512;
  --display: "Philosopher", Georgia, serif; --body: "Source Sans 3", "Segoe UI", Arial, sans-serif;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --bg: #0f1a22; --card: #16242e; --fg: #ede7d8; --muted: #9fb0ba; --line: #253642;
  --blue: #8ec1d6; --petrol: #6cc2bd; --orange: #f0a061; --chip: #1f313c; --warn-bg: #2b2018; --warn: #f2b685; color-scheme: dark } }
:root[data-theme="dark"] {
  --bg: #0f1a22; --card: #16242e; --fg: #ede7d8; --muted: #9fb0ba; --line: #253642;
  --blue: #8ec1d6; --petrol: #6cc2bd; --orange: #f0a061; --chip: #1f313c; --warn-bg: #2b2018; --warn: #f2b685; color-scheme: dark }
* { box-sizing: border-box }
body { background: var(--bg); color: var(--fg); font-family: var(--body); font-size: 16px; line-height: 1.55; margin: 0 }
.wrap { max-width: 980px; margin: 0 auto; padding-inline: 16px; padding-block: 28px 60px }
header h1 { font-family: var(--display); font-size: clamp(30px, 6vw, 44px); margin: 0; color: var(--blue); text-wrap: balance }
header p { margin: 6px 0 0; color: var(--muted); max-width: 62ch }
.stand { font-size: 13px; color: var(--muted); letter-spacing: .04em }
.abende { margin-top: 22px; border: 1px solid var(--line); background: var(--card); border-radius: 14px; padding: 18px 20px; display: grid; gap: 10px }
.abende h2 { font-family: var(--display); font-size: 22px; margin: 0; color: var(--orange) }
.termine { display: flex; flex-wrap: wrap; gap: 8px }
.termin { border: 1px solid var(--line); border-radius: 10px; padding: 6px 12px; font-variant-numeric: tabular-nums; font-weight: 600 }
.termin.naechster { border-color: var(--orange); color: var(--orange) }
.termin.vorbei { opacity: .45; text-decoration: line-through; font-weight: 400 }
.abende .zeile { display: flex; flex-wrap: wrap; gap: 10px; align-items: center }
.werkzeug { position: sticky; top: env(safe-area-inset-top, 0px); background: var(--bg); padding-block: 14px; z-index: 2; display: grid; gap: 10px; margin-top: 18px }
#suche { width: 100%; font: inherit; padding: 11px 14px; border-radius: 10px; border: 1px solid var(--line); background: var(--card); color: var(--fg) }
#suche:focus-visible, button:focus-visible, a:focus-visible { outline: 2px solid var(--petrol); outline-offset: 2px }
.chips { display: flex; flex-wrap: wrap; gap: 6px }
.chip { font: inherit; font-size: 14px; border: 0; background: var(--chip); color: var(--fg); border-radius: 999px; padding: 6px 13px; cursor: pointer }
.chip[aria-pressed="true"] { background: var(--blue); color: var(--bg) }
.liste { display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%, 420px), 1fr)); gap: 14px; margin-top: 6px }
.karte { background: var(--card); border: 1px solid var(--line); border-radius: 14px; padding: 18px 20px; display: grid; gap: 10px; align-content: start; min-width: 0 }
.kopf { display: flex; justify-content: space-between; gap: 10px; align-items: baseline; flex-wrap: wrap }
.karte h3 { font-family: var(--display); font-size: 23px; margin: 0; line-height: 1.2 }
.dt { color: var(--muted); font-size: 14px }
.kat { font-size: 12px; text-transform: uppercase; letter-spacing: .08em; color: var(--petrol); font-weight: 700 }
.aktion { font-size: 14px; background: var(--warn-bg); color: var(--warn); border-radius: 8px; padding: 6px 10px }
.meta { font-size: 14px; color: var(--muted) }
.meta b { color: var(--fg); font-weight: 600 }
.karte ul { margin: 0; padding-left: 1.1em; display: grid; gap: 4px }
.hinweis { font-size: 14px; border-left: 3px solid var(--petrol); padding-left: 10px }
details { font-size: 14px; border-top: 1px solid var(--line); padding-top: 8px }
summary { cursor: pointer; font-weight: 600; color: var(--muted) }
.kt { font-size: 15px; background: var(--bg); border-radius: 10px; padding: 10px 12px; margin: 8px 0 0 }
.knopf { font: inherit; font-size: 14px; font-weight: 600; border: 1px solid var(--blue); color: var(--blue); background: transparent; border-radius: 999px; padding: 6px 14px; cursor: pointer; text-decoration: none; display: inline-block }
.knopf:hover { background: var(--blue); color: var(--bg) }
.verbot { color: var(--warn) }
.leer { color: var(--muted); padding: 30px 0 }
@media (prefers-reduced-motion: no-preference) { .knopf, .chip { transition: background .15s, color .15s } }
</style>

<div class="wrap">
  <header>
    <div class="stand" id="stand"></div>
    <h1>Öl-Wissen</h1>
    <p>Was drin ist, wie es riecht und wie du es im Familienalltag anwendest. Fragen dazu? Schreib mir einfach.</p>
  </header>

  <section class="abende" aria-labelledby="abende-t">
    <h2 id="abende-t"></h2>
    <div class="termine" id="termine"></div>
    <div class="zeile"><span class="meta" id="abende-text"></span></div>
    <div class="zeile"><a class="knopf" id="flyer" target="_blank" rel="noopener">Flyer öffnen</a><button class="knopf" id="abend-kopieren" type="button">Einladung kopieren</button></div>
  </section>

  <div class="werkzeug">
    <input id="suche" type="search" placeholder="Suchen: Produkt, Duft, Anwendung … z. B. „Diffuser“ oder „Haut“" autocomplete="off">
    <div class="chips" id="chips" role="group" aria-label="Kategorie"></div>
  </div>
  <div class="liste" id="liste"></div>
</div>

<script>
const D = __DATEN__;
const $ = (s) => document.querySelector(s);
const esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const tage = ["So","Mo","Di","Mi","Do","Fr","Sa"];
const datum = (iso) => { const d = new Date(iso + "T12:00:00"); return tage[d.getDay()] + " " + d.getDate() + "." + (d.getMonth()+1) + "."; };

$("#stand").textContent = "STAND " + datum(D.stand).slice(3) + D.stand.slice(0,4) + " · " + D.produkte.length + " PRODUKTE";

// Öl-Abende
const W = D.workshops, heute = new Date().toISOString().slice(0,10);
const kommend = W.termine.filter((t) => t >= heute);
$("#abende-t").textContent = W.titel + " · " + W.zeit;
$("#termine").innerHTML = W.termine.map((t) => '<span class="termin ' + (t < heute ? "vorbei" : t === kommend[0] ? "naechster" : "") + '">' + datum(t) + "</span>").join("");
$("#abende-text").textContent = W.text;
$("#flyer").href = W.flyer;
const einladung = () => "Hey 💛 ich mache wieder meine Öl-Abende bei mir zuhause, jeweils um 20 Uhr: " + kommend.map(datum).join(", ") + ". Gemütlich zusammensitzen, ausprobieren, und du mischst dir deinen eigenen Roller zum Mitnehmen. Magst du kommen? Hier der Flyer: " + W.flyer;
kopierKnopf($("#abend-kopieren"), einladung);

function kopierKnopf(btn, textFn) {
  btn.addEventListener("click", async () => {
    const t = textFn(), alt = btn.textContent;
    try { await navigator.clipboard.writeText(t); btn.textContent = "Kopiert"; }
    catch (e) { const ta = document.createElement("textarea"); ta.value = t; document.body.append(ta); ta.select(); try { document.execCommand("copy"); btn.textContent = "Kopiert"; } catch (_) { btn.textContent = "Bitte markieren"; } ta.remove(); }
    setTimeout(() => (btn.textContent = alt), 1600);
  });
}

// Filter
const kats = ["Alle", ...new Set(D.produkte.map((p) => p.kategorie))];
let kat = "Alle";
try { kat = localStorage.getItem("oel-kat") || "Alle"; if (!kats.includes(kat)) kat = "Alle"; } catch (e) {}
$("#chips").innerHTML = kats.map((k) => '<button type="button" class="chip" data-k="' + esc(k) + '">' + esc(k) + "</button>").join("");
$("#chips").addEventListener("click", (e) => { const b = e.target.closest(".chip"); if (!b) return; kat = b.dataset.k; try { localStorage.setItem("oel-kat", kat); } catch (_) {} zeichne(); });
$("#suche").addEventListener("input", zeichne);

function karte(p) {
  const meta = [p.duft && "<b>Duft:</b> " + esc(p.duft), p.inhalt && "<b>Drin:</b> " + esc(p.inhalt), p.groesse && "<b>Grösse:</b> " + esc(p.groesse)].filter(Boolean).join(" · ");
  return '<article class="karte">' +
    '<div class="kat">' + esc(p.kategorie) + "</div>" +
    '<div class="kopf"><h3>' + esc(p.name) + '</h3><span class="dt">' + esc(p.deutsch || "") + "</span></div>" +
    (p.aktion ? '<div class="aktion">' + esc(p.aktion) + "</div>" : "") +
    "<div>" + esc(p.kurz) + "</div>" +
    (meta ? '<div class="meta">' + meta + "</div>" : "") +
    "<ul>" + p.anwendung.map((a) => "<li>" + esc(a) + "</li>").join("") + "</ul>" +
    (p.hinweis ? '<div class="hinweis">' + esc(p.hinweis) + "</div>" : "") +
    "<details><summary>Kurz gesagt</summary><p class=\"kt\">" + esc(p.kundinnentext) + '</p><button class="knopf" type="button" data-copy="' + esc(p.id) + '">Text kopieren</button></details>' +
    "</article>";
}

function zeichne() {
  document.querySelectorAll(".chip").forEach((b) => b.setAttribute("aria-pressed", b.dataset.k === kat));
  const q = $("#suche").value.trim().toLowerCase();
  const treffer = D.produkte.filter((p) => (kat === "Alle" || p.kategorie === kat) && (!q || JSON.stringify(p).toLowerCase().includes(q)));
  $("#liste").innerHTML = treffer.length ? treffer.map(karte).join("") : '<p class="leer">Nichts gefunden. Anderes Wort versuchen oder Filter auf „Alle“.</p>';
  $("#liste").querySelectorAll("[data-copy]").forEach((b) => kopierKnopf(b, () => D.produkte.find((p) => p.id === b.dataset.copy).kundinnentext));
}
zeichne();
</script>
"""

ZIEL.parent.mkdir(parents=True, exist_ok=True)
ZIEL.write_text(HTML.replace("__DATEN__", daten_js), encoding="utf-8")
print(f"{ZIEL.relative_to(WS)} · {len(daten['produkte'])} Produkte")

# Dieselben Daten fürs Cockpit (doTERRA → Öl-Wissen / Business-Wege):
# → ArtifactData batch set, Sammlung "doterra-wissen", Dokumente "produkte" und "wege".
COCKPIT = WS / "outputs/cockpit/abgleich/oelwissen"
COCKPIT.mkdir(parents=True, exist_ok=True)
(COCKPIT / "produkte.json").write_text(json.dumps(
    {"produkte": daten["produkte"], "workshops": daten.get("workshops"), "stand": daten.get("stand")},
    ensure_ascii=False), encoding="utf-8")
WEGE = WS / "context/doTERRA/business-wege.json"
if WEGE.exists():
    wege = json.loads(WEGE.read_text(encoding="utf-8"))
    (COCKPIT / "wege.json").write_text(json.dumps(wege, ensure_ascii=False), encoding="utf-8")
    print(f"Cockpit: produkte.json + wege.json ({len(wege.get('wege', []))} Wege)")
else:
    print("Cockpit: produkte.json (business-wege.json fehlt noch)")
