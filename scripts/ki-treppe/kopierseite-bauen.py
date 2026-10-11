#!/usr/bin/env python3
"""Baut aus 04-kursplattform-texte.md eine Seite mit Kopier-Knoepfen.

Jeder Abschnitt bekommt einen Knopf, der den Text MIT Formatierung in die
Zwischenablage legt (text/html plus text/plain als Rueckfall). In ThriveCart
Learn dann Strg+V — Absaetze und Fettungen kommen mit.

Titel und Beschreibung sind getrennt, weil die Plattform dafuer zwei Felder
hat. Genau daran haben wir bei Startklar gemerkt, dass ein Knopf fuer beides
nichts nuetzt.

Aufruf:
  python scripts/ki-treppe/kopierseite-bauen.py
  dann: preview_start {"name": "ki-kurs-texte"}  ->  http://localhost:4387
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
QUELLE = ROOT / "outputs" / "produkte" / "ki-treppe" / "04-kursplattform-texte.md"
ZIEL = ROOT / "outputs" / "produkte" / "ki-treppe" / "kurstexte" / "index.html"

# Was am 22.09.2026 schon in ThriveCart stand. Steht auf der Karte als Haken,
# damit sie nicht sucht, wo sie aufgehoert hat.
ERLEDIGT = {"1.1", "1.2", "1.3", "1.4", "1.5", "2.1", "2.2", "2.3"}


def auszeichnen(s):
    """Fett und Code als HTML. quote=False, sonst steht im Fliesstext
    ueberall &quot; statt eines Anfuehrungszeichens."""
    s = H.escape(s, quote=False)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    return s


def lesen():
    text = QUELLE.read_text(encoding="utf-8")
    bloecke = []

    # --- Begruessung -------------------------------------------------------
    m = re.search(r"^## Begr[^\n]*\n(.*?)(?=^## )", text, re.S | re.M)
    if m:
        roh = m.group(1)
        t = re.search(r"\*\*Überschrift:\*\*\s*(.+)", roh)
        zitat = "\n".join(
            z.lstrip("> ").rstrip()
            for z in roh.splitlines()
            if z.lstrip().startswith(">")
        ).strip()
        bloecke.append({
            "art": "seite", "nummer": "", "titel": t.group(1).strip() if t else "Begrüssung",
            "text": zitat, "kopf": "Begrüssung · erste Seite im Kurs", "fertig": False,
        })

    # --- Module mit ihren Lektionen ---------------------------------------
    for mod in re.finditer(r"^## (Modul\s+(\d+)[^\n]*)\n(.*?)(?=^## |\Z)", text, re.S | re.M):
        kopf, nr, rumpf = mod.group(1).strip(), mod.group(2), mod.group(3)

        zitat = "\n".join(
            z.lstrip("> ").rstrip()
            for z in rumpf.splitlines()
            if z.lstrip().startswith(">")
        ).strip()
        if zitat:
            bloecke.append({
                "art": "modul", "nummer": nr, "titel": kopf.split("·", 1)[-1].strip(),
                "text": zitat, "kopf": kopf, "fertig": False,
            })

        for zeile in re.finditer(r"^\|\s*\*\*([\d.]+)\s+([^*]+)\*\*\s*\|\s*(.+?)\s*\|\s*$",
                                 rumpf, re.M):
            num, titel, beschr = zeile.group(1), zeile.group(2).strip(), zeile.group(3).strip()
            bloecke.append({
                "art": "lektion", "nummer": num, "titel": titel, "text": beschr,
                "kopf": "Lektion " + num, "fertig": num in ERLEDIGT,
            })
    return bloecke


def karte(b, i):
    absaetze = "".join(
        "<p>" + auszeichnen(a.replace("\n", " ")) + "</p>"
        for a in re.split(r"\n\s*\n", b["text"]) if a.strip()
    )
    nutzlast = json.dumps({"html": absaetze, "text": b["text"]}, ensure_ascii=False)
    titelknopf = ("" if b["art"] == "seite" else
                  '<button class="k titel" data-t="' +
                  H.escape(json.dumps(b["titel"], ensure_ascii=False), quote=True) +
                  '">Titel kopieren</button>')
    return (
        '<article class="karte' + (" fertig" if b["fertig"] else "") +
        '" id="b' + str(i) + '">'
        '<header><span class="kopf">' + H.escape(b["kopf"], quote=False) + "</span>"
        + ('<span class="haken">steht schon drin</span>' if b["fertig"] else "") +
        "</header>"
        "<h2>" + H.escape(b["titel"], quote=False) + "</h2>"
        '<div class="text">' + absaetze + "</div>"
        '<div class="knoepfe">' + titelknopf +
        '<button class="k haupt" data-n=\'' + H.escape(nutzlast, quote=True).replace("'", "&#39;") +
        '\'>Beschreibung kopieren</button></div>'
        "</article>"
    )


def bauen():
    bloecke = lesen()
    if not bloecke:
        print("Nichts gefunden — stimmt der Aufbau der Quelldatei noch?")
        return 1

    lektionen = [b for b in bloecke if b["art"] == "lektion"]
    offen = [b for b in lektionen if not b["fertig"]]

    kopf = (
        '<!doctype html><html lang="de"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        "<title>KI-Kurs — Texte für ThriveCart</title>"
        '<link href="https://fonts.googleapis.com/css2?family=Philosopher:wght@700'
        '&family=Source+Sans+3:wght@400;600&display=swap" rel="stylesheet">'
        "<style>" + CSS + "</style></head><body>"
        "<header class=\"seitenkopf\"><h1>Texte für die Kursplattform</h1>"
        "<p>" + str(len(lektionen)) + " Lektionen · <strong>" + str(len(offen)) +
        " noch einzutragen</strong>. Knopf drücken, in ThriveCart ins Feld klicken, "
        "Strg&nbsp;+&nbsp;V. Fettungen und Absätze kommen mit.</p>"
        '<label class="filter"><input type="checkbox" id="nuroffen"> '
        "nur zeigen, was noch fehlt</label></header><main>"
    )
    mitte = "".join(karte(b, i) for i, b in enumerate(bloecke))
    return kopf + mitte + "</main><div class=\"hinweis\" id=\"hinweis\"></div><script>" + JS + "</script></body></html>"


CSS = """
:root{--creme:#f1ecdd;--petrol:#12828c;--blau:#0c1c30;--tief:#29556d;--orange:#dc822e;
  --linie:rgba(12,28,48,.14)}
*{box-sizing:border-box}
body{margin:0;background:var(--creme);color:var(--blau);
  font-family:'Source Sans 3',sans-serif;font-size:16px;line-height:1.6}
.seitenkopf{background:#fff;border-bottom:3px solid var(--orange);
  padding:26px 24px 20px;position:sticky;top:0;z-index:5}
.seitenkopf h1{font-family:'Philosopher',serif;font-size:28px;margin:0 0 6px;font-weight:700}
.seitenkopf p{margin:0;color:var(--tief);font-size:15px;max-width:70ch}
.filter{display:inline-flex;align-items:center;gap:8px;margin-top:12px;
  font-size:14px;color:var(--tief);cursor:pointer}
main{max-width:860px;margin:0 auto;padding:22px 18px 80px}
.karte{background:#fff;border:1px solid var(--linie);border-radius:12px;
  padding:18px 20px;margin-bottom:14px;box-shadow:0 1px 2px rgba(12,28,48,.05)}
.karte.fertig{opacity:.55}
.karte header{display:flex;align-items:center;gap:10px;margin-bottom:4px}
.kopf{font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--petrol);
  font-weight:600}
.haken{font-size:11px;background:rgba(47,125,91,.14);color:#2f7d5b;
  padding:2px 9px;border-radius:999px;margin-left:auto}
.karte h2{font-family:'Philosopher',serif;font-size:21px;margin:0 0 8px;font-weight:700}
.text p{margin:0 0 9px;color:#22364c}
.text p:last-child{margin-bottom:0}
code{background:var(--creme);border-radius:4px;padding:1px 6px;font-size:.92em}
.knoepfe{display:flex;gap:8px;flex-wrap:wrap;margin-top:14px}
.k{border:1px solid rgba(12,28,48,.28);background:#fff;color:var(--blau);
  border-radius:8px;padding:8px 15px;font:inherit;font-size:14px;cursor:pointer}
.k:hover{border-color:var(--petrol);color:var(--petrol)}
.k.haupt{background:var(--petrol);border-color:var(--petrol);color:#fff}
.k.haupt:hover{filter:brightness(1.08);color:#fff}
.k.fertig{background:#2f7d5b;border-color:#2f7d5b;color:#fff}
.hinweis{position:fixed;left:50%;bottom:24px;transform:translateX(-50%);
  background:var(--blau);color:var(--creme);padding:10px 20px;border-radius:999px;
  font-size:14px;opacity:0;transition:opacity .16s;pointer-events:none}
.hinweis.an{opacity:1}
"""

JS = """
var hinweis = document.getElementById('hinweis'), uhr;
function sagen(t){ hinweis.textContent=t; hinweis.classList.add('an');
  clearTimeout(uhr); uhr=setTimeout(function(){hinweis.classList.remove('an');},1700); }

function quittieren(k){ var alt=k.textContent; k.textContent='kopiert'; k.classList.add('fertig');
  setTimeout(function(){k.textContent=alt;k.classList.remove('fertig');},1300); }

/* Erst ClipboardItem mit HTML, damit Fettungen mitkommen. Wo das gesperrt ist,
   der schlichte Weg ueber ein verstecktes Feld. */
function kopieren(html, text, knopf){
  function altweg(){
    var f=document.createElement('textarea'); f.value=text;
    f.style.position='fixed'; f.style.opacity='0';
    document.body.appendChild(f); f.select();
    var ok=false; try{ok=document.execCommand('copy');}catch(e){}
    f.remove();
    if(ok){quittieren(knopf); sagen('Kopiert — ohne Formatierung.');}
    else sagen('Kopieren ging nicht. Text markieren und von Hand kopieren.');
  }
  if(window.ClipboardItem && navigator.clipboard && navigator.clipboard.write){
    navigator.clipboard.write([new ClipboardItem({
      'text/html': new Blob([html],{type:'text/html'}),
      'text/plain': new Blob([text],{type:'text/plain'})
    })]).then(function(){quittieren(knopf); sagen('Kopiert — mit Formatierung.');}, altweg);
    return;
  }
  altweg();
}

document.querySelectorAll('.k.haupt').forEach(function(k){
  k.onclick=function(){ var n=JSON.parse(k.getAttribute('data-n'));
    kopieren(n.html, n.text, k); };
});
document.querySelectorAll('.k.titel').forEach(function(k){
  k.onclick=function(){ var t=JSON.parse(k.getAttribute('data-t'));
    kopieren('<p>'+t+'</p>', t, k); };
});
document.getElementById('nuroffen').onchange=function(){
  var nur=this.checked;
  document.querySelectorAll('.karte').forEach(function(a){
    a.hidden = nur && a.classList.contains('fertig');
  });
};
"""

if __name__ == "__main__":
    html = bauen()
    if html == 1:
        sys.exit(1)
    ZIEL.parent.mkdir(parents=True, exist_ok=True)
    ZIEL.write_text(html, encoding="utf-8")
    bl = lesen()
    lek = [b for b in bl if b["art"] == "lektion"]
    print(f"{len(bl)} Bloecke: {len(lek)} Lektionen, "
          f"{len([b for b in lek if not b['fertig']])} davon offen")
    print(f"-> {ZIEL.relative_to(ROOT)}")
    print('Ansehen: preview_start {"name": "ki-kurs-texte"}')
