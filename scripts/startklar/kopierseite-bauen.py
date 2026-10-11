"""
Baut aus 10-kursplattform-texte.md eine Seite mit Kopier-Knoepfen.

Jeder Abschnitt bekommt einen Knopf, der den Text MIT Formatierung in die
Zwischenablage legt (text/html plus text/plain als Rueckfall). In ThriveCart
dann einfach Strg+V - Ueberschrift, Absaetze und Fettungen kommen mit.

Aufruf:
  python scripts/startklar/kopierseite-bauen.py
  dann: preview_start {"name": "startklar-texte"}  ->  http://localhost:4383
"""
import html as H
import json
import pathlib
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = pathlib.Path(__file__).resolve().parents[2]
QUELLE = ROOT / "outputs" / "produkte" / "instagram-startklar" / "10-kursplattform-texte.md"
ZIEL = ROOT / "outputs" / "produkte" / "instagram-startklar" / "kurstexte" / "index.html"


def auszeichnen(s):
    # quote=False: im Fliesstext bleibt " ein ", sonst steht ueberall &quot;
    s = H.escape(s, quote=False)
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)",
               lambda m: '<a href="%s">%s</a>' % (H.escape(m.group(2), quote=True), m.group(1)), s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    return s


def abschnitte():
    text = QUELLE.read_text(encoding="utf-8")
    teile = re.split(r"^#{2,3} (.+)$", text, flags=re.M)
    raus = []
    for i in range(1, len(teile), 2):
        name, roh = teile[i].strip(), teile[i + 1]

        titel, zeilen = None, []
        for z in roh.splitlines():
            z = z.strip()
            if z.startswith("**Überschrift:**"):
                titel = z.replace("**Überschrift:**", "").strip()
                continue
            if z.startswith(">"):
                zeilen.append(z[1:].strip())
            elif not z or z.startswith("---"):
                zeilen.append("")

        absaetze, puffer = [], []
        for z in zeilen:
            if z:
                puffer.append(z)
            elif puffer:
                absaetze.append(" ".join(puffer))
                puffer = []
        if puffer:
            absaetze.append(" ".join(puffer))

        if not absaetze:
            continue

        # Titel gehoert bei Lektionen und Modulen ins eigene Feld der Plattform,
        # bei Begruessung und Werkstatt aber mit ins HTML.
        eigenes_feld = name.startswith(("Lektion", "Modul", "Abschlusstext"))
        html_teile = []
        if not eigenes_feld and (titel or name):
            html_teile.append("<h2>%s</h2>" % H.escape(titel or name))
        html_teile += ["<p>%s</p>" % auszeichnen(a) for a in absaetze]

        raus.append({
            "name": name,
            "titelfeld": titel or name,
            "eigenesFeld": eigenes_feld,
            "html": "\n".join(html_teile),
            "text": "\n\n".join(([titel] if titel and not eigenes_feld else [])
                                + [a.replace("**", "") for a in absaetze]),
        })
    return raus


SEITE = """<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Startklar Kurstexte</title>
<link href="https://fonts.googleapis.com/css2?family=Philosopher:wght@700&family=Source+Sans+3:wght@400;600&display=swap" rel="stylesheet">
<style>
  :root{ --nacht:#0c1c30; --blau:#29556d; --petrol:#12828c;
         --creme:#f1ecdd; --orange:#dc822e; --linie:rgba(12,28,48,.14); }
  *{box-sizing:border-box}
  body{ margin:0; background:var(--creme); color:var(--nacht);
        font-family:'Source Sans 3',system-ui,sans-serif; font-size:16px; line-height:1.6; }
  header{ background:var(--nacht); color:var(--creme); padding:20px 24px; }
  h1{ font-family:Philosopher,serif; margin:0 0 6px; font-size:24px; }
  header p{ margin:0; opacity:.8; font-size:15px; }
  .wrap{ max-width:820px; margin:0 auto; padding:24px 20px 60px; }
  .karte{ background:#fff; border:1px solid var(--linie); border-radius:12px;
          padding:18px 20px; margin-bottom:18px; }
  .kopf{ display:flex; align-items:baseline; gap:12px; flex-wrap:wrap; margin-bottom:4px; }
  .kopf h2{ font-family:Philosopher,serif; font-size:19px; margin:0; }
  .feld{ font-size:13px; opacity:.65; }
  .titelzeile{ background:rgba(18,130,140,.09); border-radius:7px;
               padding:8px 12px; margin:10px 0 14px; font-size:15px;
               display:flex; align-items:center; gap:10px; flex-wrap:wrap; }
  .titelzeile b{ font-weight:600; }
  .vorschau{ border-left:3px solid var(--petrol); padding-left:14px; }
  .vorschau p{ margin:0 0 10px; }
  .vorschau h2{ font-family:Philosopher,serif; font-size:18px; margin:0 0 10px; }
  button{ background:var(--blau); color:var(--creme); border:0; border-radius:7px;
          padding:8px 15px; cursor:pointer; font:600 15px 'Source Sans 3',sans-serif; }
  button:hover{ background:var(--petrol); }
  button.klein{ background:transparent; color:var(--blau); border:1px solid var(--linie);
                padding:5px 11px; font-size:14px; }
  button.klein:hover{ background:rgba(18,130,140,.12); color:var(--nacht); }
  button.fertig{ background:var(--orange); }
  .reihe{ display:flex; gap:10px; margin-top:14px; flex-wrap:wrap; align-items:center; }
  .hinweis{ font-size:14px; opacity:.7; }
  a{ color:var(--petrol); }
</style>
</head>
<body>
<header>
  <h1>Startklar &middot; Texte f&uuml;r die Kursplattform</h1>
  <p>Knopf dr&uuml;cken, dann in ThriveCart mit Strg+V einf&uuml;gen &ndash; &Uuml;berschrift, Abs&auml;tze und Fettungen kommen mit.</p>
</header>
<div class="wrap" id="liste"></div>

<script>
const DATEN = __DATEN__;

function karte(a, i){
  const el = document.createElement('div');
  el.className = 'karte';
  const titelzeile = a.eigenesFeld
    ? '<div class="titelzeile"><span>Titelfeld:</span> <b>' + a.titelfeld + '</b>' +
      '<button class="klein" data-titel="' + i + '">Titel kopieren</button></div>'
    : '';
  el.innerHTML =
    '<div class="kopf"><h2>' + a.name + '</h2></div>' +
    titelzeile +
    '<div class="vorschau">' + a.html + '</div>' +
    '<div class="reihe">' +
      '<button data-kopieren="' + i + '">Text kopieren</button>' +
      '<span class="hinweis">mit Formatierung</span>' +
    '</div>';
  return el;
}

async function kopieren(html, text, knopf){
  try {
    await navigator.clipboard.write([new ClipboardItem({
      'text/html': new Blob([html], {type:'text/html'}),
      'text/plain': new Blob([text], {type:'text/plain'})
    })]);
  } catch(e) {
    // Rueckfall: nur Text, falls der Browser ClipboardItem nicht mag
    try { await navigator.clipboard.writeText(text); }
    catch(e2) { alert('Kopieren hat nicht geklappt. Markier den Text von Hand.'); return; }
  }
  const alt = knopf.textContent;
  knopf.textContent = 'Kopiert';
  knopf.classList.add('fertig');
  setTimeout(() => { knopf.textContent = alt; knopf.classList.remove('fertig'); }, 1500);
}

const liste = document.getElementById('liste');
DATEN.forEach((a, i) => liste.appendChild(karte(a, i)));

liste.addEventListener('click', async ev => {
  const b = ev.target.closest('button');
  if (!b) return;
  if (b.dataset.kopieren !== undefined){
    const a = DATEN[+b.dataset.kopieren];
    await kopieren(a.html, a.text, b);
  }
  if (b.dataset.titel !== undefined){
    const a = DATEN[+b.dataset.titel];
    await kopieren('<p>' + a.titelfeld + '</p>', a.titelfeld, b);
  }
});
</script>
</body>
</html>
"""


def main():
    teile = abschnitte()
    ZIEL.parent.mkdir(parents=True, exist_ok=True)
    seite = SEITE.replace("__DATEN__", json.dumps(teile, ensure_ascii=False))
    ZIEL.write_text(seite, encoding="utf-8")
    print("%d Abschnitte -> %s" % (len(teile), ZIEL))
    for t in teile:
        print("   %-55s %s" % (t["name"], "Titel getrennt" if t["eigenesFeld"] else "Titel im HTML"))


if __name__ == "__main__":
    main()
