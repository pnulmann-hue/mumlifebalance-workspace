#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Baut die Begleit-Seite fuer die 30-Tage-Energie-Routine.

Fuer die **Teilnehmerinnen**, nicht fuer Patricia. Inhalte kommen aus `inhalte.py`
und aus denselben Rezeptquellen wie die Webseiten (`scripts/rezepte/bauen.py`) —
eine Quelle, ein Parser.

🚨 **Keine Artifact-Faehigkeiten.** Sobald eine Seite `db` oder `assets` deklariert,
kommen nur angemeldete Leute aus der Organisation hinein, und fuer Kundinnen ist sie
damit unbrauchbar. Alles Eingetragene laeuft ueber `localStorage`: bleibt auf dem
Geraet, kommt nie bei Patricia an, und wer das Geraet wechselt, faengt von vorne an.
Genau das steht auch auf der Seite — eine Zusage, die die Technik nicht halten kann,
waere schlimmer als gar keine.

    python scripts/begleitung/cockpit-bauen.py
"""
import io, os, sys, html, json, re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
HIER = os.path.dirname(os.path.abspath(__file__))
WURZEL = os.path.dirname(os.path.dirname(HIER))
sys.path.insert(0, os.path.join(WURZEL, "scripts", "rezepte"))
sys.path.insert(0, HIER)
from bauen import lies, fett
from inhalte import (WOCHEN, TAGLICH, KRAFT, VORRAT, PROTEIN, MENGENWORT,
                     ABSCHLUSS, HINWEIS, TELEGRAM)
from bibliothek import BIBLIOTHEK, IMPULSE

ZIEL = os.path.join(WURZEL, "outputs", "produkte", "doterra-mama-energie", "begleitung")
def _q(name):
    return os.path.join(WURZEL, "outputs/produkte/doterra-mama-energie", name)

# Je Mahlzeit eine Datei. Die fruehere Sammeldatei `17-mittag-abend-snacks.md`
# ist damit abgeloest und geloescht — zwei Staende derselben Rezepte waeren beim
# naechsten Aendern auseinandergelaufen.
QUELLEN = [
    (_q("12-30-fruehstuecke.md"), {"Form 1": "fruehstueck", "Form 2": "fruehstueck",
                                   "Form 3": "fruehstueck"}),
    (_q("17-mittagessen.md"), {"Form 4": "mittag"}),
    (_q("18-abendessen.md"), {"Form 5": "abend"}),
    (_q("19-zwischenmahlzeiten.md"), {"Form 6": "snack"}),
]
MAHLZEIT = {"fruehstueck": "Frühstück", "mittag": "Mittag", "abend": "Abend", "snack": "Znüni"}


def alle_rezepte():
    """Alle Gruppen aus beiden Quellen, jede mit ihrer Mahlzeit-Art."""
    aus = []
    for pfad, zuordnung in QUELLEN:
        for g in lies(pfad):
            art = next((v for k, v in zuordnung.items() if g["titel"].startswith(k)), "sonst")
            g["art"] = art
            aus.append(g)
    return aus


def rezept_karte(r, art):
    marken = [f'<span class="pill art">{MAHLZEIT.get(art, art)}</span>']
    if r.get("zeit"):
        marken.append(f'<span class="pill zeit">{html.escape(r["zeit"])}</span>')
    if r.get("proteinkopf"):
        marken.append(f'<span class="pill prot">{html.escape(r["proteinkopf"])} Protein</span>')
    # Die Familienzeile traegt ihren Rohtext mit, damit der Rechner sie umrechnen
    # kann, ohne dass die Formatierung (fette Marken) im Weg steht.
    mengen = ""
    if r.get("familie"):
        mengen += (f'<div class="menge fam" data-roh="{html.escape(r["familie"], quote=True)}">'
                   f'<span class="fam-marke">Für 6 Personen</span> '
                   f'<span class="fam-text">{fett(r["familie"])}</span></div>')
    if r.get("einzeln"):
        mengen += (f'<div class="menge"><span>Einzelportion</span> '
                   f'{fett(r["einzeln"])}</div>')
    extras = "".join(
        f'<p class="extra"><span>{marke}:</span> {fett(r[k])}</p>'
        for k, marke in (("kinder", "Bei meinen vier"), ("warum", "Warum"),
                         ("vorher", "Vorbereiten")) if r.get(k))
    # Suchtext: alles, wonach jemand suchen koennte, in einem Attribut
    such = " ".join([r.get("name", ""), MAHLZEIT.get(art, ""), r.get("familie", ""),
                     r.get("einzeln", ""), r.get("zubereitung", "")]).lower()
    return (f'<article class="rez" data-art="{art}" data-such="{html.escape(such, quote=True)}">'
            f'<div class="rez-kopf"><span class="rez-nr">{html.escape(r["nr"])}</span>'
            f'<h3>{fett(r["name"])}</h3></div>'
            f'<div class="pills">{"".join(marken)}</div>'
            f'<div class="mengen">{mengen}</div>'
            f'<p class="zub">{fett(r.get("zubereitung", ""))}</p>{extras}</article>')


def bauen():
    gruppen = alle_rezepte()
    anzahl = sum(len(g["rezepte"]) for g in gruppen)

    haken = "".join(
        f'<label class="hak" for="h-{p["id"]}" data-woche="{p["abWoche"]}">'
        f'<input type="checkbox" id="h-{p["id"]}" data-tag="{p["id"]}">'
        f'<span class="box" aria-hidden="true"></span>'
        f'<span class="hak-txt"><b>{html.escape(p["txt"])}</b>'
        f'<em>{html.escape(p["hint"])}</em></span></label>' for p in TAGLICH)

    wochen_karten = "".join(
        f'<section class="woche ton-{w["ton"]}" data-woche="{w["nr"]}">'
        f'<header><span class="w-nr">Woche {w["nr"]}</span>'
        f'<span class="w-tage">{html.escape(w["tage"])}</span>'
        f'<h3>{html.escape(w["titel"])}</h3></header>'
        f'<p class="w-ziel">{html.escape(w["ziel"])}</p>'
        + "".join(f"<p>{t}</p>" for t in w["text"])
        + f'<p class="w-merkst"><span>Was du merkst</span> {html.escape(w["merkst"])}</p>'
        + '<p class="w-lies"><span>Diese Woche lesen</span> '
        + " · ".join(f'<a href="#w-{i}" data-lies="{i}">{titel_von(i)}</a>' for i in w["lies"])
        + "</p></section>" for w in WOCHEN)

    rezept_gruppen = "".join(
        f'<section class="gruppe" data-art="{g["art"]}">'
        f'<h3 class="g-titel">{html.escape(g["titel"])}</h3>'
        f'<p class="g-unter">{html.escape(g["unter"])}</p>'
        f'<div class="rez-raster">'
        + "".join(rezept_karte(r, g["art"]) for r in g["rezepte"])
        + "</div></section>" for g in gruppen)

    regale = "".join(
        f'<section class="regal ton-{r["ton"]}">'
        f'<h3 class="r-titel">{html.escape(r["regal"])}</h3>'
        + "".join(
            f'<details class="wis" id="w-{s["id"]}" data-tag="{s["tag"]}">'
            f'<summary><b>{html.escape(s["titel"])}</b>'
            f'<em class="kurz">{html.escape(s["kurz"])}</em>'
            f'<em class="schloss" hidden></em></summary>'
            f'<div class="wis-in">'
            + "".join(f"<p>{t}</p>" for t in s["text"])
            + f'<p class="q">{s["quelle"]}</p></div></details>' for s in r["stuecke"])
        + "</section>" for r in BIBLIOTHEK)

    vorrat = "".join(
        f'<section class="vor ton-{g["ton"]}" data-woche="{g["abWoche"]}">'
        f'<h3>{html.escape(g["titel"])}</h3>'
        f'<p class="v-hin">{html.escape(g["hinweis"])}</p><ul class="v-liste">'
        + "".join(
            f'<li><label for="v-{i}-{j}">'
            f'<input type="checkbox" id="v-{i}-{j}" data-vor="{i}-{j}">'
            f'<span class="box klein" aria-hidden="true"></span>'
            f'<span><b>{html.escape(was)}</b><em>{html.escape(warum)}</em></span>'
            f"</label></li>" for j, (was, warum) in enumerate(g["zeilen"]))
        + "</ul></section>" for i, g in enumerate(VORRAT["gruppen"]))

    proteintabelle = "".join(
        f'<h4 class="pg">{html.escape(g["titel"])}</h4>'
        f'<table class="ptab"><thead><tr><th>Lebensmittel</th>'
        f'<th class="z">je 100 g</th><th>übliche Portion</th><th class="z">macht</th>'
        f"</tr></thead><tbody>"
        + "".join(
            f'<tr><td>{html.escape(n)}</td><td class="z">{p100} g</td>'
            f'<td>{html.escape(port)}</td><td class="z hv">{pp} g</td></tr>'
            for n, p100, port, pp in g["zeilen"])
        + "</tbody></table>" for g in PROTEIN["gruppen"])

    mengenwort_js = json.dumps(MENGENWORT, ensure_ascii=False)
    tage_liste = json.dumps([p["id"] for p in TAGLICH])
    wochen_js = json.dumps([{"nr": w["nr"], "titel": w["titel"], "ziel": w["ziel"],
                             "merkst": w["merkst"]} for w in WOCHEN], ensure_ascii=False)
    impulse_js = json.dumps({str(k): {"titel": v[0], "text": v[1]}
                             for k, v in IMPULSE.items()}, ensure_ascii=False)

    # Ohne Benutzernamen kein Knopf — ein Link ins Leere ist schlimmer als keiner.
    telegram_knopf = (f'<a class="teilen" id="an-patricia" data-name="{html.escape(TELEGRAM)}" '
                      f'target="_blank" rel="noopener" hidden>Per Telegram an Patricia schicken</a>'
                      if TELEGRAM else "")
    if not TELEGRAM:
        print("  Hinweis: TELEGRAM in inhalte.py ist leer — der Teilen-Knopf fehlt.")

    return f"""<meta charset="utf-8">
<title>30-Tage-Energie-Routine</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Philosopher:wght@400;700&family=Source+Sans+3:ital,wght@0,400;0,600;0,700;1,400&display=swap">
<style>
:root {{
  --creme:#f1ecdd; --creme-tief:#e7e0cd; --papier:#fbf9f3;
  --tinte:#0c1c30; --tinte-weich:#3d5260; --grau:#6f6a5e;
  --petrol:#12828c; --petrol-hell:#dfe9e8; --petrol-tief:#0d5f66;
  --orange:#dc822e; --orange-tief:#a85c17; --orange-weich:#f7e2cd;
  --linie:rgba(12,28,48,.10); --linie-stark:rgba(12,28,48,.22);
  --grund:var(--creme); --flaeche:var(--papier);
  --serif:'Philosopher','Palatino Linotype',Georgia,serif;
  --sans:'Source Sans 3','Segoe UI',system-ui,-apple-system,sans-serif;
}}
@media (prefers-color-scheme: dark) {{
  :root:not([data-theme="light"]) {{
    --creme:#111c26; --creme-tief:#0b141c; --papier:#18242f;
    --tinte:#eee7d6; --tinte-weich:#b9c4cc; --grau:#8f9aa3;
    --petrol:#4fb3bb; --petrol-hell:#16333a; --petrol-tief:#7fd0d6;
    --orange:#eb9c50; --orange-tief:#f0b077; --orange-weich:#33241a;
    --linie:rgba(238,231,214,.13); --linie-stark:rgba(238,231,214,.30);
    --grund:#0b141c; --flaeche:#141f29;
  }}
}}
:root[data-theme="dark"] {{
  --creme:#111c26; --creme-tief:#0b141c; --papier:#18242f;
  --tinte:#eee7d6; --tinte-weich:#b9c4cc; --grau:#8f9aa3;
  --petrol:#4fb3bb; --petrol-hell:#16333a; --petrol-tief:#7fd0d6;
  --orange:#eb9c50; --orange-tief:#f0b077; --orange-weich:#33241a;
  --linie:rgba(238,231,214,.13); --linie-stark:rgba(238,231,214,.30);
  --grund:#0b141c; --flaeche:#141f29;
}}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--grund); color:var(--tinte);
  font-family:var(--sans); font-size:17px; line-height:1.62;
  -webkit-font-smoothing:antialiased; }}
.wrap {{ max-width:980px; margin:0 auto; padding-inline:18px; }}
h1,h2,h3 {{ font-family:var(--serif); font-weight:400; text-wrap:balance; margin:0; }}
a {{ color:var(--petrol-tief); }}

/* Kopf */
.kopf {{ background:var(--flaeche); border-bottom:1px solid var(--linie); }}
.kopf .wrap {{ padding-block:24px 18px; }}
.marke {{ font-size:11px; letter-spacing:.2em; text-transform:uppercase;
  color:var(--petrol); font-weight:700; }}
.kopf h1 {{ font-size:clamp(26px,5vw,38px); line-height:1.1; margin:5px 0 0; }}
.zaehler {{ display:flex; flex-wrap:wrap; align-items:baseline; gap:6px 14px; margin-top:14px; }}
.tagzahl {{ font-family:var(--serif); font-size:38px; line-height:1;
  color:var(--orange-tief); font-variant-numeric:tabular-nums; }}
.tagzahl small {{ font-size:15px; color:var(--grau); font-family:var(--sans); }}
.fokus {{ font-size:15px; color:var(--tinte-weich); }}
.fokus b {{ color:var(--petrol-tief); }}
.balken {{ height:6px; border-radius:99px; background:var(--creme-tief);
  overflow:hidden; margin-top:12px; }}
.balken i {{ display:block; height:100%; background:var(--petrol); width:3.33%;
  transition:width .35s ease; }}

/* Reiter */
.reiter {{ position:sticky; top:env(safe-area-inset-top, 0px); z-index:5;
  background:var(--flaeche); border-bottom:1px solid var(--linie); }}
.reiter .wrap {{ display:flex; gap:2px; overflow-x:auto; padding-block:0;
  scrollbar-width:none; }}
.reiter .wrap::-webkit-scrollbar {{ display:none; }}
.reiter button {{ flex:0 0 auto; background:none; border:0; cursor:pointer;
  font-family:var(--sans); font-size:15px; font-weight:600; color:var(--grau);
  padding:13px 11px; border-bottom:2.5px solid transparent; white-space:nowrap; }}
.reiter button[aria-selected="true"] {{ color:var(--tinte); border-color:var(--orange); }}
.reiter button:focus-visible {{ outline:2px solid var(--petrol); outline-offset:-4px; }}

main .wrap {{ padding-block:24px 56px; }}
.blatt[hidden] {{ display:none !important; }}

/* Heute */
.start {{ display:flex; flex-wrap:wrap; align-items:center; gap:10px;
  background:var(--petrol-hell); border-radius:14px; padding:13px 16px;
  font-size:15px; margin-bottom:22px; }}
.start label {{ font-weight:600; }}
.start input {{ font:inherit; padding:7px 10px; border-radius:9px;
  border:1px solid var(--linie-stark); background:var(--flaeche); color:var(--tinte); }}
.haken {{ display:flex; flex-direction:column; gap:9px; }}
.hak {{ display:flex; gap:13px; align-items:flex-start; cursor:pointer;
  background:var(--flaeche); border:1px solid var(--linie); border-radius:14px;
  padding:14px 16px; }}
.hak input, .v-liste input {{ position:absolute; opacity:0; width:0; height:0; }}
.box {{ flex:0 0 auto; width:25px; height:25px; border-radius:8px; margin-top:1px;
  border:2px solid var(--linie-stark); background:var(--grund); position:relative; }}
.box.klein {{ width:21px; height:21px; border-radius:7px; }}
input:checked + .box {{ background:var(--petrol); border-color:var(--petrol); }}
input:checked + .box::after {{ content:""; position:absolute; left:8px; top:3px;
  width:6px; height:12px; border:solid #fff; border-width:0 2.5px 2.5px 0;
  transform:rotate(42deg); }}
.box.klein::after {{ left:6px !important; top:2px !important; width:5px !important;
  height:10px !important; }}
input:focus-visible + .box {{ outline:2px solid var(--petrol); outline-offset:2px; }}
.hak-txt {{ display:flex; flex-direction:column; }}
.hak-txt em {{ font-style:normal; font-size:13.5px; color:var(--grau); }}
.hak input:checked ~ .hak-txt b {{ color:var(--petrol-tief); }}

.kraft {{ margin-top:9px; background:var(--orange-weich);
  border:1px solid var(--orange); border-radius:14px; padding:14px 16px;
  display:flex; flex-wrap:wrap; align-items:center; gap:12px; }}
.kraft em {{ font-style:normal; font-size:13.5px; color:var(--grau); display:block; }}
.punkte {{ display:flex; gap:7px; margin-left:auto; }}
.punkte button {{ width:34px; height:34px; border-radius:50%; cursor:pointer;
  border:2px solid var(--orange); background:transparent; color:var(--orange-tief);
  font:600 15px var(--sans); }}
.punkte button[aria-pressed="true"] {{ background:var(--orange); color:#fff; }}
.punkte button:focus-visible {{ outline:2px solid var(--tinte); outline-offset:2px; }}

.impuls {{ background:linear-gradient(135deg,var(--tinte) 0%,#14314f 70%,var(--petrol-tief) 100%);
  color:var(--creme); border-radius:16px; padding:20px 22px; margin-bottom:22px; }}
.impuls .label {{ color:var(--orange); }}
.impuls h2 {{ font-size:clamp(21px,3.6vw,27px); color:#fff; margin-bottom:7px; line-height:1.2; }}
.impuls p {{ margin:0; color:rgba(255,255,255,.88); }}

.neu {{ margin-top:22px; background:var(--petrol-hell); border-radius:14px; padding:15px 18px; }}
.neu .label {{ color:var(--petrol-tief); }}
.neu a {{ display:block; padding:7px 0; font-weight:600; border-bottom:1px solid var(--linie); }}
.neu a:last-child {{ border-bottom:0; }}
.neu .k {{ display:block; font-weight:400; font-size:14px; color:var(--grau); }}

/* Noch nicht freigeschaltet: sichtbar, dass etwas kommt — aber nicht zu oeffnen */
.wis.zu {{ opacity:.55; }}
.wis.zu summary {{ cursor:default; }}
.wis.zu summary b {{ font-size:17px; }}
.schloss {{ font-style:normal; font-size:13px; font-weight:700; color:var(--orange-tief);
  letter-spacing:.08em; text-transform:uppercase; }}
.vor.zu {{ opacity:.55; }}
.vor.zu .v-liste {{ display:none; }}
.regal-zahl {{ font-size:13.5px; color:var(--grau); font-weight:400; }}

.merk {{ margin-top:22px; background:var(--flaeche); border-left:3px solid var(--orange);
  border-radius:0 14px 14px 0; padding:15px 18px; }}
.merk span.label, .notiz span.label, .w-merkst span, .w-lies span {{
  display:block; font-size:11px; letter-spacing:.16em; text-transform:uppercase;
  color:var(--orange-tief); font-weight:700; margin-bottom:5px; }}
.w-merkst span, .w-lies span {{ display:inline; letter-spacing:.14em; margin-right:6px; }}

.notiz {{ margin-top:22px; background:var(--flaeche); border:1px solid var(--linie);
  border-radius:14px; padding:16px 18px; }}
.notiz textarea {{ width:100%; min-height:82px; font:inherit; font-size:16px;
  border:1px solid var(--linie-stark); border-radius:10px; padding:11px 13px;
  background:var(--grund); color:var(--tinte); resize:vertical; }}
.notiz .hint {{ font-size:13.5px; color:var(--grau); margin:8px 0 0; }}
a.teilen {{ display:inline-block; margin-top:12px; padding:9px 17px; border-radius:100px;
  background:var(--petrol); color:var(--grund); text-decoration:none; font-weight:600;
  font-size:14.5px; }}
.tagebuch {{ margin-top:26px; }}
.tagebuch h3 {{ font-size:22px; margin-bottom:10px; }}
.eintrag {{ background:var(--flaeche); border-left:3px solid var(--petrol);
  border-radius:0 12px 12px 0; padding:12px 16px; margin-bottom:9px; }}
.eintrag b {{ display:block; font-size:13px; color:var(--petrol-tief);
  text-transform:uppercase; letter-spacing:.1em; }}
.leer {{ color:var(--grau); font-size:15px; }}
.geraet {{ margin-top:26px; font-size:13.5px; color:var(--grau);
  border-top:1px solid var(--linie); padding-top:15px; }}

/* Plan */
.gitter {{ display:grid; grid-template-columns:repeat(10,1fr); gap:6px;
  margin:0 0 26px; }}
.gitter div {{ aspect-ratio:1; border-radius:8px; background:var(--creme-tief);
  display:flex; align-items:center; justify-content:center;
  font-size:12px; font-weight:600; color:var(--grau);
  font-variant-numeric:tabular-nums; border:1px solid transparent; }}
.gitter div.teil {{ background:var(--petrol-hell); color:var(--petrol-tief); }}
.gitter div.voll {{ background:var(--petrol); color:#fff; }}
.gitter div.heute {{ border-color:var(--orange); font-weight:700; }}
.legende {{ display:flex; flex-wrap:wrap; gap:14px; font-size:13.5px;
  color:var(--grau); margin:-16px 0 26px; }}
.legende i {{ width:13px; height:13px; border-radius:4px; display:inline-block;
  margin-right:5px; vertical-align:-2px; }}
.woche {{ background:var(--flaeche); border:1px solid var(--linie);
  border-radius:16px; padding:21px; margin-bottom:15px; }}
.woche header {{ display:flex; flex-wrap:wrap; align-items:baseline; gap:5px 12px;
  margin-bottom:9px; }}
.w-nr {{ font-size:11px; letter-spacing:.17em; text-transform:uppercase;
  font-weight:700; color:var(--petrol); }}
.ton-orange .w-nr, .ton-orange .r-titel::after {{ color:var(--orange-tief); }}
.ton-blau .w-nr {{ color:var(--tinte-weich); }}
.w-tage {{ font-size:13px; color:var(--grau); }}
.woche h3 {{ flex-basis:100%; font-size:26px; }}
.w-ziel {{ font-size:18px; margin:0 0 11px; padding-left:14px;
  border-left:3px solid var(--petrol); }}
.ton-orange .w-ziel {{ border-color:var(--orange); }}
.ton-blau .w-ziel {{ border-color:var(--tinte-weich); }}
.woche p {{ margin:0 0 11px; }}
.w-merkst, .w-lies {{ font-size:15px; color:var(--tinte-weich); margin:12px 0 0 !important; }}
.woche.jetzt {{ border-color:var(--petrol); box-shadow:0 0 0 2px var(--petrol-hell); }}

/* Rezepte */
.suchzeile {{ position:sticky; top:calc(46px + env(safe-area-inset-top, 0px));
  z-index:4; background:var(--grund); padding-block:12px; margin-bottom:8px; }}
.suchzeile input[type="search"] {{ width:100%; font:inherit; font-size:16px;
  padding:11px 14px; border-radius:12px; border:1px solid var(--linie-stark);
  background:var(--flaeche); color:var(--tinte); }}
.chips {{ display:flex; flex-wrap:wrap; gap:7px; margin-top:9px; }}
.chips button {{ font:600 14px var(--sans); padding:7px 14px; border-radius:99px;
  border:1px solid var(--linie-stark); background:var(--flaeche);
  color:var(--tinte-weich); cursor:pointer; }}
.chips button[aria-pressed="true"] {{ background:var(--petrol); border-color:var(--petrol);
  color:#fff; }}
.chips button:focus-visible {{ outline:2px solid var(--orange); outline-offset:2px; }}
.treffer {{ font-size:14px; color:var(--grau); margin:10px 0 0; }}
.personen {{ display:flex; align-items:center; gap:8px; margin-top:10px;
  font-size:15px; flex-wrap:wrap; }}
.personen label {{ font-weight:600; }}
.personen button {{ width:34px; height:34px; border-radius:10px; cursor:pointer;
  border:1px solid var(--linie-stark); background:var(--flaeche); color:var(--tinte);
  font:600 19px var(--sans); line-height:1; }}
.personen input {{ width:58px; font:600 16px var(--sans); text-align:center;
  padding:7px 4px; border-radius:10px; border:1px solid var(--linie-stark);
  background:var(--flaeche); color:var(--tinte); }}
.personen button:focus-visible, .personen input:focus-visible {{
  outline:2px solid var(--petrol); outline-offset:1px; }}
.personen span {{ font-size:13.5px; color:var(--grau); }}
.fam-marke {{ color:var(--petrol-tief); font-weight:700; }}
.menge.fam.um .fam-marke {{ color:var(--orange-tief); }}

.ptabelle {{ background:var(--flaeche); border:1px solid var(--linie);
  border-radius:15px; margin-bottom:26px; overflow:hidden; }}
.ptabelle summary {{ cursor:pointer; padding:16px 18px; list-style:none;
  display:flex; flex-direction:column; gap:3px; }}
.ptabelle summary::-webkit-details-marker {{ display:none; }}
.ptabelle summary b {{ font-family:var(--serif); font-size:21px; font-weight:400; }}
.ptabelle summary em {{ font-style:normal; font-size:14.5px; color:var(--grau); }}
.ptabelle[open] summary {{ border-bottom:1px solid var(--linie); }}
.ptab-in {{ padding:6px 18px 18px; }}
.pg {{ font-family:var(--serif); font-weight:400; font-size:19px; margin:18px 0 7px;
  color:var(--petrol-tief); }}
.ptab {{ width:100%; border-collapse:collapse; font-size:14.5px;
  font-variant-numeric:tabular-nums; }}
.ptab th {{ text-align:left; font-size:11.5px; letter-spacing:.1em;
  text-transform:uppercase; color:var(--grau); font-weight:700;
  padding:0 8px 6px 0; border-bottom:1px solid var(--linie); }}
.ptab td {{ padding:7px 8px 7px 0; border-bottom:1px solid var(--linie);
  vertical-align:top; }}
.ptab .z {{ text-align:right; padding-right:0; white-space:nowrap; }}
.ptab .hv {{ font-weight:700; color:var(--orange-tief); }}
.pschluss {{ font-size:14.5px; color:var(--tinte-weich); margin:16px 0 0; }}
.gruppe {{ margin-bottom:32px; }}
.g-titel {{ font-size:24px; }}
.g-unter {{ color:var(--grau); margin:4px 0 16px; }}
.rez-raster {{ display:grid; gap:13px; grid-template-columns:repeat(auto-fill,minmax(290px,1fr)); }}
.rez {{ background:var(--flaeche); border:1px solid var(--linie); border-radius:15px;
  padding:18px; }}
.rez-kopf {{ display:flex; gap:10px; align-items:baseline; }}
.rez-nr {{ font-family:var(--serif); color:var(--petrol); font-weight:700; font-size:15px; }}
.rez h3 {{ font-size:20px; line-height:1.24; }}
.pills {{ display:flex; flex-wrap:wrap; gap:6px; margin:10px 0 11px; }}
.pill {{ font-size:12.5px; font-weight:600; border-radius:99px; padding:4px 11px; }}
.pill.art {{ background:var(--tinte); color:var(--creme); }}
.pill.zeit {{ background:var(--petrol-hell); color:var(--petrol-tief); }}
.pill.prot {{ background:var(--orange-weich); color:var(--orange-tief); }}
.mengen {{ border-left:3px solid var(--orange); padding-left:13px; margin-bottom:11px; }}
.menge {{ font-size:15px; margin-bottom:3px; }}
.menge span {{ color:var(--petrol-tief); font-weight:700; }}
.zub {{ margin:0 0 11px; font-size:15.5px; }}
.extra {{ font-size:14.5px; color:var(--tinte-weich); margin:0 0 7px; line-height:1.55; }}
.extra span {{ font-weight:700; color:var(--tinte); }}

/* Vorrat */
.vor {{ background:var(--flaeche); border:1px solid var(--linie); border-radius:16px;
  padding:20px; margin-bottom:14px; }}
.vor h3 {{ font-size:23px; }}
.v-hin {{ font-size:15px; color:var(--grau); margin:5px 0 14px; }}
.v-liste {{ list-style:none; margin:0; padding:0; display:flex;
  flex-direction:column; gap:8px; }}
.v-liste label {{ display:flex; gap:12px; align-items:flex-start; cursor:pointer; }}
.v-liste em {{ font-style:normal; font-size:13.5px; color:var(--grau); display:block; }}
.v-liste input:checked ~ span b {{ color:var(--grau); text-decoration:line-through; }}

/* Wissen */
.bib-hinweis {{ background:var(--orange-weich); border-radius:14px;
  padding:14px 18px; margin:0 0 24px; font-size:15.5px; color:var(--orange-tief); }}
.bib-hinweis b {{ color:var(--tinte); }}
.regal {{ margin-bottom:26px; }}
.r-titel {{ font-size:24px; margin-bottom:11px; padding-bottom:7px;
  border-bottom:2px solid var(--petrol-hell); }}
.wis {{ background:var(--flaeche); border:1px solid var(--linie); border-radius:14px;
  margin-bottom:8px; overflow:hidden; }}
.wis summary {{ cursor:pointer; padding:15px 18px; list-style:none;
  display:flex; flex-direction:column; gap:3px; }}
.wis summary::-webkit-details-marker {{ display:none; }}
.wis summary b {{ font-family:var(--serif); font-size:20px; font-weight:400;
  line-height:1.25; }}
.wis summary em {{ font-style:normal; font-size:14.5px; color:var(--grau); }}
.wis[open] summary {{ border-bottom:1px solid var(--linie); }}
.wis[open] summary b {{ color:var(--petrol-tief); }}
.wis summary:focus-visible {{ outline:2px solid var(--petrol); outline-offset:-3px; }}
.wis-in {{ padding:15px 18px 17px; }}
.wis-in p {{ margin:0 0 11px; }}
.q {{ font-size:13.5px; color:var(--grau); margin:13px 0 0 !important;
  padding-top:10px; border-top:1px solid var(--linie); }}
.wis:target, .wis.leuchtet {{ border-color:var(--orange);
  box-shadow:0 0 0 2px var(--orange-weich); }}
.abschluss {{ background:var(--petrol-hell); border-radius:16px; padding:21px;
  margin-top:24px; }}
.abschluss h3 {{ font-size:23px; margin-bottom:9px; }}
.abschluss p {{ margin:0 0 10px; }}
.hinweis {{ font-size:13.5px; color:var(--grau); margin-top:28px;
  border-top:1px solid var(--linie); padding-top:15px; }}

@media (max-width:540px) {{
  body {{ font-size:16px; }}
  .rez-raster {{ grid-template-columns:1fr; }}
  .gitter {{ grid-template-columns:repeat(6,1fr); }}
}}
@media (prefers-reduced-motion: reduce) {{ * {{ transition:none !important; }} }}
</style>

<header class="kopf"><div class="wrap">
  <div class="marke">Mum Life Balance</div>
  <h1>30-Tage-Energie-Routine</h1>
  <div class="zaehler">
    <div class="tagzahl"><span id="tagzahl">1</span><small id="tagzusatz"> von 30</small></div>
    <div class="fokus">Diese Woche: <b id="fokus">Essen</b> — <span id="fokusziel"></span></div>
  </div>
  <div class="balken"><i id="balken"></i></div>
</div></header>

<nav class="reiter"><div class="wrap" role="tablist" aria-label="Bereiche">
  <button role="tab" aria-selected="true" aria-controls="b-heute" id="t-heute">Heute</button>
  <button role="tab" aria-selected="false" aria-controls="b-plan" id="t-plan">Dein Plan</button>
  <button role="tab" aria-selected="false" aria-controls="b-rez" id="t-rez">Rezepte</button>
  <button role="tab" aria-selected="false" aria-controls="b-vor" id="t-vor">Vorrat</button>
  <button role="tab" aria-selected="false" aria-controls="b-wis" id="t-wis">Bibliothek</button>
</div></nav>

<main><div class="wrap">

  <div class="blatt" id="b-heute" role="tabpanel" aria-labelledby="t-heute">
    <div class="start">
      <label for="startdatum">Dein Starttag</label>
      <input type="date" id="startdatum">
      <span id="startnotiz" class="leer"></span>
    </div>
    <section class="impuls" id="impuls">
      <span class="label">Dein Schritt heute</span>
      <h2 id="impuls-titel"></h2>
      <p id="impuls-text"></p>
    </section>

    <div class="haken">{haken}</div>
    <div class="kraft" data-woche="2" hidden>
      <div><b>{html.escape(KRAFT["txt"])}</b><em>{html.escape(KRAFT["hint"])}</em></div>
      <div class="punkte" id="kraftpunkte" role="group" aria-label="Krafttraining diese Woche">
        <button type="button" data-k="1" aria-pressed="false">1</button>
        <button type="button" data-k="2" aria-pressed="false">2</button>
        <button type="button" data-k="3" aria-pressed="false">3</button>
      </div>
    </div>

    <div class="merk"><span class="label">Was du diese Woche merkst</span>
      <p id="merkst" style="margin:0"></p></div>

    <section class="neu" id="neu" hidden>
      <span class="label">Heute neu in der Bibliothek</span>
      <div id="neu-liste"></div>
    </section>

    <div class="notiz"><span class="label">Was ist dir heute aufgefallen?</span>
      <textarea id="tagesnotiz" placeholder="Auch Kleinigkeiten. Dass du die Treppe genommen hast. Dass du um vier noch Geduld hattest."></textarea>
      <p class="hint">Am Tag 25 liest du das alles zusammen durch. Das ist eindrücklicher
      als jede Waage.</p>
      {telegram_knopf}</div>

    <div class="tagebuch"><h3>Was sich bisher verändert hat</h3>
      <div id="eintraege"></div></div>

    <p class="geraet">Alles, was du hier einträgst, bleibt nur auf diesem Gerät gespeichert.
    Ich sehe es nicht, und auf einem anderen Handy fängst du wieder bei null an — das ist
    Absicht, es soll dich niemand kontrollieren.</p>
  </div>

  <div class="blatt" id="b-plan" role="tabpanel" aria-labelledby="t-plan" hidden>
    <div class="gitter" id="gitter" aria-label="Deine dreissig Tage"></div>
    <p class="legende">
      <span><i style="background:var(--creme-tief)"></i>offen</span>
      <span><i style="background:var(--petrol-hell)"></i>teilweise</span>
      <span><i style="background:var(--petrol)"></i>alles abgehakt</span>
      <span><i style="background:transparent;border:2px solid var(--orange)"></i>heute</span>
    </p>
    {wochen_karten}
  </div>

  <div class="blatt" id="b-rez" role="tabpanel" aria-labelledby="t-rez" hidden>
    <div class="suchzeile">
      <input type="search" id="suche" placeholder="Suchen — Zutat, Name, „ohne Herd“ …"
             aria-label="Rezepte durchsuchen">
      <div class="chips" id="chips" role="group" aria-label="Nach Mahlzeit filtern">
        <button type="button" data-f="alle" aria-pressed="true">Alle</button>
        <button type="button" data-f="fruehstueck" aria-pressed="false">Frühstück</button>
        <button type="button" data-f="mittag" aria-pressed="false">Mittag</button>
        <button type="button" data-f="abend" aria-pressed="false">Abend</button>
        <button type="button" data-f="snack" aria-pressed="false">Znüni</button>
      </div>
      <div class="personen">
        <label for="personen">Für wie viele?</label>
        <button type="button" id="p-minus" aria-label="weniger Personen">−</button>
        <input type="number" id="personen" min="1" max="20" value="6" inputmode="numeric">
        <button type="button" id="p-plus" aria-label="mehr Personen">+</button>
        <span id="p-notiz"></span>
      </div>
      <p class="treffer" id="treffer"></p>
    </div>

    <details class="ptabelle">
      <summary><b>{html.escape(PROTEIN["kopf"])}</b>
        <em>{html.escape(PROTEIN["einleitung"])}</em></summary>
      <div class="ptab-in">
        {proteintabelle}
        {"".join(f"<p class='pschluss'>{x}</p>" for x in PROTEIN["schluss"])}
      </div>
    </details>

    {rezept_gruppen}
  </div>

  <div class="blatt" id="b-vor" role="tabpanel" aria-labelledby="t-vor" hidden>
    <h2 style="font-size:clamp(24px,4vw,32px);margin-bottom:12px">{html.escape(VORRAT["kopf"])}</h2>
    {"".join(f'<p style="margin:0 0 12px">{t}</p>' for t in VORRAT["einleitung"])}
    <p class="treffer" id="vortreffer" style="margin:0 0 20px"></p>
    {vorrat}
    <div class="abschluss">
      {"".join(f"<p>{t}</p>" for t in VORRAT["schluss"])}
    </div>
  </div>

  <div class="blatt" id="b-wis" role="tabpanel" aria-labelledby="t-wis" hidden>
    <p class="bib-hinweis" id="bib-hinweis"></p>
    {regale}
    <section class="abschluss"><h3>{html.escape(ABSCHLUSS["kopf"])}</h3>
    {"".join(f"<p>{t}</p>" for t in ABSCHLUSS["text"])}</section>
    <p class="hinweis">{html.escape(HINWEIS)}</p>
  </div>

</div></main>

<script>
(function () {{
  "use strict";
  var TAGE = {tage_liste};
  var WOCHEN = {wochen_js};
  var IMPULSE = {impulse_js};

  // localStorage kann werfen (privates Fenster, blockierte Seitendaten) — beides
  // abfangen, die Seite muss ohne genauso laufen.
  function hol(k, ersatz) {{
    try {{ var v = localStorage.getItem(k); return v === null ? ersatz : v; }}
    catch (e) {{ return ersatz; }}
  }}
  function leg(k, v) {{ try {{ localStorage.setItem(k, v); }} catch (e) {{}} }}

  function iso(d) {{
    return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0")
         + "-" + String(d.getDate()).padStart(2, "0");
  }}
  var heute = new Date(); heute.setHours(0, 0, 0, 0);
  var MONATE = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli",
                "August", "September", "Oktober", "November", "Dezember"];
  var heuteIso = iso(heute);

  var feldStart = document.getElementById("startdatum");
  // Wer in Monat M kauft, startet am 10. von M+1 (Bestellschluss Ende Vormonat),
  // und den Link bekommt sie gleich beim Kauf. Deshalb: beim ERSTEN Oeffnen der
  // 10. des naechsten Monats — und sofort festhalten. Ohne das Festhalten wuerde
  // der Starttag bei jedem Oeffnen neu gerechnet und mitten in der Runde springen.
  function rundenStart(d) {{
    return iso(new Date(d.getFullYear(), d.getMonth() + 1, 10));
  }}
  var start = hol("enr.start", "");
  var ersterBesuch = !start;
  if (!/^\\d{{4}}-\\d{{2}}-\\d{{2}}$/.test(start)) start = rundenStart(heute);
  if (ersterBesuch) leg("enr.start", start);
  feldStart.value = start;

  function startDatum() {{
    var s = new Date(feldStart.value + "T00:00:00");
    return isNaN(s) ? heute : s;
  }}
  function tagNummer() {{
    var n = Math.floor((heute - startDatum()) / 86400000) + 1;
    return Math.min(30, Math.max(1, n));
  }}
  function wocheNummer() {{ return Math.min(4, Math.ceil(tagNummer() / 7)); }}
  function datumVonTag(n) {{
    var d = new Date(startDatum().getTime()); d.setDate(d.getDate() + n - 1); return d;
  }}
  function wochenSchluessel() {{ return feldStart.value + ".w" + wocheNummer(); }}

  function zeichneKopf() {{
    var t = tagNummer(), w = WOCHEN[wocheNummer() - 1];
    var bis = Math.round((startDatum() - heute) / 86400000);
    document.getElementById("tagzahl").textContent = bis > 0 ? bis : t;
    document.getElementById("tagzusatz").textContent =
      bis > 1 ? " Tage bis zum Start" : (bis === 1 ? " Tag bis zum Start" : " von 30");
    document.getElementById("balken").style.width = (bis > 0 ? 0 : t / 30 * 100).toFixed(1) + "%";
    document.getElementById("fokus").textContent = w.titel;
    document.getElementById("fokusziel").textContent = w.ziel;
    document.getElementById("merkst").textContent = w.merkst;
    var s = startDatum(), notiz = document.getElementById("startnotiz");
    notiz.textContent = s > heute
      ? "Deine Runde startet am " + s.getDate() + ". " + MONATE[s.getMonth()] + ". "
        + "Bis dahin kannst du schon einkaufen (Reiter Vorrat) und dir drei Frühstücke "
        + "aussuchen. Stimmt das Datum nicht, änderst du es hier."
      : (t >= 30 ? "Letzter Tag." : "");
    document.querySelectorAll(".woche").forEach(function (el) {{
      el.classList.toggle("jetzt", Number(el.dataset.woche) === wocheNummer());
    }});
  }}

  // 🚨 Der Kern der Fuehrung: Was noch nicht dran ist, steht nicht im Weg.
  // Haken erscheinen erst ab ihrer Woche, Artikel erst ab ihrem Tag, Vorrats-
  // gruppen erst ab ihrer Woche. Die Rezepte sind bewusst AUSGENOMMEN — die
  // sind von Tag 1 an vollstaendig da.
  function zeichneFreischaltung() {{
    var t = tagNummer(), w = wocheNummer();

    document.querySelectorAll(".hak[data-woche]").forEach(function (el) {{
      el.hidden = Number(el.dataset.woche) > w;
    }});
    var kr = document.querySelector(".kraft");
    kr.hidden = Number(kr.dataset.woche) > w;

    var neu = [];
    document.querySelectorAll(".wis[data-tag]").forEach(function (el) {{
      var n = Number(el.dataset.tag), zu = n > t;
      el.classList.toggle("zu", zu);
      el.querySelector(".kurz").hidden = zu;
      var s = el.querySelector(".schloss");
      s.hidden = !zu;
      s.textContent = "ab Tag " + n;
      if (zu) el.open = false;
      if (n === t) neu.push(el);
    }});

    document.querySelectorAll(".vor[data-woche]").forEach(function (el) {{
      var zu = Number(el.dataset.woche) > w;
      el.classList.toggle("zu", zu);
      var h = el.querySelector(".v-hin");
      h.textContent = zu ? "Kommt in Woche " + el.dataset.woche + " dazu."
                         : h.dataset.echt;
    }});

    // Zaehler je Regal: wie viel ist offen
    document.querySelectorAll(".regal").forEach(function (r) {{
      var alle = r.querySelectorAll(".wis").length;
      var offen = r.querySelectorAll(".wis:not(.zu)").length;
      var z = r.querySelector(".regal-zahl");
      z.textContent = offen < alle ? " " + offen + " von " + alle : "";
    }});

    // Der Hinweis oben in der Bibliothek. Ohne ihn sieht ein Regal voller
    // verschlossener Zeilen am Tag 1 nach einer leeren Seite aus statt nach etwas,
    // auf das man sich freut.
    var alleArt = document.querySelectorAll(".wis").length;
    var offenArt = document.querySelectorAll(".wis:not(.zu)").length;
    document.getElementById("bib-hinweis").innerHTML = offenArt >= alleArt
      ? "<b>Alle " + alleArt + " Stücke sind offen.</b> Die Bibliothek gehört jetzt dir — "
        + "auch nach den dreissig Tagen."
      : "<b>" + offenArt + " von " + alleArt + " Stücken sind offen.</b> Jeden Tag kommt "
        + "mindestens eines dazu. Das ist Absicht: Alles auf einmal liest sowieso niemand, "
        + "und das meiste ergibt erst Sinn, wenn du die Woche davor erlebt hast.";

    // „Heute neu"
    var kasten = document.getElementById("neu"), liste = document.getElementById("neu-liste");
    liste.textContent = "";
    kasten.hidden = neu.length === 0;
    neu.forEach(function (el) {{
      var a = document.createElement("a");
      a.href = "#" + el.id;
      a.textContent = el.querySelector("summary b").textContent;
      var k = document.createElement("span");
      k.className = "k";
      k.textContent = el.querySelector(".kurz").textContent;
      a.appendChild(k);
      a.addEventListener("click", function (e) {{
        e.preventDefault(); zeige("t-wis"); el.open = true;
        el.classList.add("leuchtet");
        setTimeout(function () {{ el.classList.remove("leuchtet"); }}, 2400);
        el.scrollIntoView({{ behavior: "smooth", block: "start" }});
      }});
      liste.appendChild(a);
    }});
  }}

  // Vor dem 10. ist noch kein Tag 1 — kein Impuls, der „heute" sagt, keine
  // Checkliste, und das Paket ist vielleicht noch gar nicht da.
  function vorStart() {{ return startDatum() > heute; }}
  function zeichneImpuls() {{
    document.querySelector(".haken").hidden = vorStart();
    if (vorStart()) {{
      document.getElementById("impuls-titel").textContent = "Bevor es losgeht";
      document.getElementById("impuls-text").textContent =
        "Am Starttag öffnet sich hier dein erster Schritt. Bis dahin: schau dich in den Rezepten um, "
        + "kauf die Sachen aus dem Vorrat für Woche 1 ein und stell dein Paket dorthin, wo du es "
        + "morgens siehst. Mehr brauchst du vorher nicht.";
      return;
    }}
    var i = IMPULSE[String(tagNummer())];
    if (!i) return;
    document.getElementById("impuls-titel").textContent = i.titel;
    document.getElementById("impuls-text").textContent = i.text;
  }}

  function zeichneHaken() {{
    TAGE.forEach(function (id) {{
      document.getElementById("h-" + id).checked =
        hol("enr." + heuteIso + "." + id, "") === "1";
    }});
    var k = Number(hol("enr.kraft." + wochenSchluessel(), "0"));
    document.querySelectorAll("#kraftpunkte button").forEach(function (b) {{
      b.setAttribute("aria-pressed", Number(b.dataset.k) <= k ? "true" : "false");
    }});
  }}

  function zeichneGitter() {{
    var g = document.getElementById("gitter");
    g.textContent = "";
    for (var n = 1; n <= 30; n++) {{
      var d = iso(datumVonTag(n));
      var voll = 0;
      TAGE.forEach(function (id) {{ if (hol("enr." + d + "." + id, "") === "1") voll++; }});
      var el = document.createElement("div");
      el.textContent = n;
      el.title = "Tag " + n + " · " + d.split("-").reverse().join(".");
      if (voll >= TAGE.length) el.className = "voll";
      else if (voll > 0) el.className = "teil";
      if (d === heuteIso) el.className += " heute";
      g.appendChild(el);
    }}
  }}

  var feldNotiz = document.getElementById("tagesnotiz");
  function zeichneTagebuch() {{
    feldNotiz.value = hol("enr.notiz." + heuteIso, "");
    var kasten = document.getElementById("eintraege");
    kasten.textContent = "";
    var gefunden = 0;
    for (var n = 30; n >= 1; n--) {{
      var d = iso(datumVonTag(n));
      if (d === heuteIso) continue;
      var txt = hol("enr.notiz." + d, "").trim();
      if (!txt) continue;
      gefunden++;
      var e = document.createElement("div"); e.className = "eintrag";
      var b = document.createElement("b");
      b.textContent = "Tag " + n + " · " + d.split("-").reverse().join(".");
      var p = document.createElement("p"); p.style.margin = "3px 0 0";
      p.textContent = txt;                       // textContent, nie innerHTML
      e.appendChild(b); e.appendChild(p); kasten.appendChild(e);
    }}
    if (!gefunden) {{
      var leer = document.createElement("p"); leer.className = "leer";
      leer.textContent = "Hier sammelt sich, was du oben einträgst. Noch ist es leer — "
        + "und genau das ändert sich in den nächsten Wochen.";
      kasten.appendChild(leer);
    }}
  }}

  TAGE.forEach(function (id) {{
    document.getElementById("h-" + id).addEventListener("change", function () {{
      leg("enr." + heuteIso + "." + id, this.checked ? "1" : "0");
      zeichneGitter();
    }});
  }});
  document.querySelectorAll("#kraftpunkte button").forEach(function (b) {{
    b.addEventListener("click", function () {{
      var n = Number(b.dataset.k);
      var jetzt = Number(hol("enr.kraft." + wochenSchluessel(), "0"));
      leg("enr.kraft." + wochenSchluessel(), String(n === jetzt ? n - 1 : n));
      zeichneHaken();
    }});
  }});
  // Bleibt privat, ausser sie will es teilen: ein Link, den sie selbst antippt
  // (window.open ist im Artifact-Rahmen lautlos blockiert).
  var knopfTg = document.getElementById("an-patricia");
  function zeichneTeilen() {{
    if (!knopfTg) return;
    var txt = feldNotiz.value.trim();
    knopfTg.hidden = !txt || vorStart();
    knopfTg.href = "https://t.me/" + knopfTg.dataset.name + "?text="
      + encodeURIComponent("Tag " + tagNummer() + " meiner Energie-Routine:\\n\\n" + txt);
  }}
  feldNotiz.addEventListener("input", function () {{
    leg("enr.notiz." + heuteIso, feldNotiz.value);
    zeichneTeilen();
  }});
  feldStart.addEventListener("change", function () {{
    if (feldStart.value) leg("enr.start", feldStart.value);
    zeichneKopf(); zeichneHaken(); zeichneGitter(); zeichneTagebuch();
    zeichneFreischaltung(); zeichneImpuls();
  }});

  // Vorratsliste
  document.querySelectorAll("[data-vor]").forEach(function (el) {{
    el.checked = hol("enr.vorrat." + el.dataset.vor, "") === "1";
    el.addEventListener("change", function () {{
      leg("enr.vorrat." + el.dataset.vor, el.checked ? "1" : "0");
      zaehleVorrat();
    }});
  }});
  function zaehleVorrat() {{
    var alle = document.querySelectorAll("[data-vor]");
    var an = 0;
    alle.forEach(function (e) {{ if (e.checked) an++; }});
    document.getElementById("vortreffer").textContent =
      an + " von " + alle.length + " abgehakt";
  }}

  // ---- Portionsrechner -------------------------------------------------
  // Die Rezepte sind fuer SECHS geschrieben. Der Rechner skaliert von dort —
  // 🚨 nicht von einer geratenen Familiengroesse. Steht als Marke auf der Karte,
  // damit nie unklar ist, worauf sich eine Menge bezieht.
  var BASIS = 6;
  var BRUCH = {{ "½": 0.5, "¼": 0.25, "¾": 0.75, "⅓": 1/3, "⅔": 2/3 }};
  var MEHRZAHL = {mengenwort_js};
  var EINZAHL = {{}};
  Object.keys(MEHRZAHL).forEach(function (m) {{ EINZAHL[MEHRZAHL[m]] = m; }});

  // „1 Äpfel" und „2 Dose Tomaten" sind das Erste, was auffaellt. Ein optionales
  // Adjektiv davor wird uebersprungen („2 grosse Kartoffeln").
  function zahlwort(rest, n) {{
    var m = rest.match(/^(\\s*)((?:[a-zäöüß]+e\\s+)?)([A-Za-zÄÖÜäöüß][\\wÄÖÜäöüß-]*)/);
    if (!m) return rest;
    var wort = m[3], neuWort = wort;
    if (n === 1 && MEHRZAHL[wort]) neuWort = MEHRZAHL[wort];
    else if (n > 1 && EINZAHL[wort]) neuWort = EINZAHL[wort];
    if (neuWort === wort) return rest;
    return m[1] + m[2] + neuWort + rest.slice(m[0].length);
  }}

  function zahlAus(s) {{
    if (BRUCH[s] !== undefined) return BRUCH[s];
    return parseFloat(s.replace(",", "."));
  }}
  function huebsch(n) {{
    if (Math.abs(n - 0.5) < 0.01) return "½";
    if (Math.abs(n - 0.25) < 0.01) return "¼";
    if (Math.abs(n - 0.75) < 0.01) return "¾";
    var s = (Math.round(n * 10) / 10).toString();
    return s.replace(".", ",");
  }}
  // Runden nach Einheit: Gramm grob, Esslöffel halb, Stückzahlen ganz.
  // Ohne das stehen dort „0,67 Dosen Tomaten" und „233,33 g Skyr".
  // Gibt [Zahl, evtl. geaenderte Einheit] zurueck — kleine Mengen wechseln von
  // kg auf g und von l auf ml, sonst steht dort „0,2 kg Magerquark".
  function runde(n, rest) {{
    var e = (rest.trim().toLowerCase().match(/^[a-zäöü]+/) || [""])[0];
    if (e === "kg") {{
      if (n < 1) return [String(Math.round(n * 1000 / 10) * 10), rest.replace(/^(\\s*)kg/, "$1g")];
      return [huebsch(Math.round(n * 10) / 10), rest];
    }}
    if (e === "l") {{
      if (n < 1) return [String(Math.round(n * 1000 / 10) * 10), rest.replace(/^(\\s*)l/, "$1ml")];
      return [huebsch(Math.round(n * 10) / 10), rest];
    }}
    if (e === "ml")
      return [String(n >= 100 ? Math.round(n / 10) * 10 : Math.round(n / 5) * 5), rest];
    if (e === "g")
      return [String(n >= 100 ? Math.round(n / 10) * 10
                   : n >= 20 ? Math.round(n / 5) * 5 : Math.max(1, Math.round(n))), rest];
    if (e === "el" || e === "tl")
      return [huebsch(Math.max(0.5, Math.round(n * 2) / 2)), rest];
    return [String(Math.max(1, Math.round(n))), rest];  // Eier, Dosen, Äpfel
  }}
  function skaliere(text, faktor) {{
    return text.split("·").map(function (teil) {{
      var m = teil.match(/^(\\s*)(\\d+(?:[.,]\\d+)?|[½¼¾⅓⅔])(\\s*)/);
      if (!m) return teil;                       // „Zimt", „Olivenöl" — bleibt
      var n = zahlAus(m[2]);
      if (!isFinite(n)) return teil;
      var rest = teil.slice(m[0].length);
      var paar = runde(n * faktor, rest);
      var gerundet = paar[0], neuerRest = paar[1];
      var alsZahl = parseFloat(gerundet.replace("½", "0.5").replace(",", "."));
      return m[1] + gerundet + m[3] + zahlwort(neuerRest, alsZahl);
    }}).join("·");
  }}

  var feldPersonen = document.getElementById("personen");
  feldPersonen.value = hol("enr.personen", String(BASIS));
  function zeichnePortionen() {{
    var n = Math.min(20, Math.max(1, parseInt(feldPersonen.value, 10) || BASIS));
    var f = n / BASIS;
    document.querySelectorAll(".menge.fam").forEach(function (el) {{
      var roh = el.dataset.roh;
      el.querySelector(".fam-marke").textContent =
        "Für " + n + (n === 1 ? " Person" : " Personen");
      el.querySelector(".fam-text").textContent = n === BASIS ? roh : skaliere(roh, f);
      el.classList.toggle("um", n !== BASIS);
    }});
    document.getElementById("p-notiz").textContent = n === BASIS
      ? "so sind die Rezepte geschrieben"
      : "umgerechnet · gerundet";
  }}
  feldPersonen.addEventListener("input", function () {{
    leg("enr.personen", feldPersonen.value); zeichnePortionen();
  }});
  document.getElementById("p-minus").addEventListener("click", function () {{
    feldPersonen.value = Math.max(1, (parseInt(feldPersonen.value, 10) || BASIS) - 1);
    feldPersonen.dispatchEvent(new Event("input"));
  }});
  document.getElementById("p-plus").addEventListener("click", function () {{
    feldPersonen.value = Math.min(20, (parseInt(feldPersonen.value, 10) || BASIS) + 1);
    feldPersonen.dispatchEvent(new Event("input"));
  }});

  // Rezept-Suche
  var feldSuche = document.getElementById("suche");
  var filter = "alle";
  function filtern() {{
    var q = feldSuche.value.trim().toLowerCase();
    var sichtbar = 0;
    document.querySelectorAll(".rez").forEach(function (r) {{
      var passt = (filter === "alle" || r.dataset.art === filter)
               && (!q || r.dataset.such.indexOf(q) >= 0);
      r.hidden = !passt;
      if (passt) sichtbar++;
    }});
    document.querySelectorAll(".gruppe").forEach(function (g) {{
      g.hidden = !g.querySelector(".rez:not([hidden])");
    }});
    var t = document.getElementById("treffer");
    t.textContent = (q || filter !== "alle")
      ? sichtbar + (sichtbar === 1 ? " Rezept" : " Rezepte")
      : "{anzahl} Rezepte — Frühstück, Mittag, Abend und Znüni";
  }}
  feldSuche.addEventListener("input", filtern);
  document.querySelectorAll("#chips button").forEach(function (b) {{
    b.addEventListener("click", function () {{
      filter = b.dataset.f;
      document.querySelectorAll("#chips button").forEach(function (x) {{
        x.setAttribute("aria-pressed", x === b ? "true" : "false");
      }});
      filtern();
    }});
  }});

  // Reiter
  var knoepfe = Array.prototype.slice.call(document.querySelectorAll('[role="tab"]'));
  function zeige(id) {{
    knoepfe.forEach(function (b) {{
      var an = b.id === id;
      b.setAttribute("aria-selected", an ? "true" : "false");
      document.getElementById(b.getAttribute("aria-controls")).hidden = !an;
    }});
    leg("enr.reiter", id);
  }}
  knoepfe.forEach(function (b) {{
    b.addEventListener("click", function () {{ zeige(b.id); }});
    b.addEventListener("keydown", function (e) {{
      var i = knoepfe.indexOf(b),
          n = e.key === "ArrowRight" ? i + 1 : e.key === "ArrowLeft" ? i - 1 : -1;
      if (n >= 0 && n < knoepfe.length) {{
        e.preventDefault(); knoepfe[n].focus(); zeige(knoepfe[n].id);
      }}
    }});
  }});

  // Ein verschlossener Artikel oeffnet nicht. preventDefault auf dem Summary-Klick
  // ist der einzige Weg, der ohne Kampf mit dem Browser auskommt.
  document.querySelectorAll(".wis summary").forEach(function (s) {{
    s.addEventListener("click", function (e) {{
      if (s.parentElement.classList.contains("zu")) e.preventDefault();
    }});
  }});

  // Regal-Zaehler und Originaltext der Vorrats-Hinweise sichern
  document.querySelectorAll(".r-titel").forEach(function (h) {{
    var z = document.createElement("span"); z.className = "regal-zahl"; h.appendChild(z);
  }});
  document.querySelectorAll(".v-hin").forEach(function (h) {{ h.dataset.echt = h.textContent; }});

  // „Diese Woche lesen" springt in die Bibliothek und klappt das Stueck auf
  document.querySelectorAll("[data-lies]").forEach(function (a) {{
    a.addEventListener("click", function (e) {{
      e.preventDefault();
      var ziel = document.getElementById("w-" + a.dataset.lies);
      if (!ziel) return;
      zeige("t-wis");
      ziel.open = true;
      ziel.classList.add("leuchtet");
      setTimeout(function () {{ ziel.classList.remove("leuchtet"); }}, 2400);
      ziel.scrollIntoView({{ behavior: "smooth", block: "start" }});
    }});
  }});

  var gemerkt = hol("enr.reiter", "t-heute");
  zeige(document.getElementById(gemerkt) ? gemerkt : "t-heute");
  zeichneKopf(); zeichneHaken(); zeichneGitter(); zeichneTagebuch();
  zeichneFreischaltung(); zeichneImpuls(); zaehleVorrat(); zeichneTeilen();
  zeichnePortionen(); filtern();
}})();
</script>
"""


def titel_von(kennung):
    for regal in BIBLIOTHEK:
        for s in regal["stuecke"]:
            if s["id"] == kennung:
                return html.escape(s["titel"])
    return kennung


def main():
    os.makedirs(ZIEL, exist_ok=True)
    seite = bauen()
    pfad = os.path.join(ZIEL, "index.html")
    open(pfad, "w", encoding="utf-8").write(seite)

    rez = seite.count('class="rez"')
    wis = seite.count('class="wis"')
    vor = seite.count("data-vor=")
    print(f"  {pfad}")
    print(f"  {len(seite)/1024:.1f} KB · {rez} Rezepte · {wis} Wissens-Artikel · "
          f"{vor} Vorratszeilen")

    for verboten in ("capabilities", "claude.use("):
        if verboten in seite:
            print(f'  🚨 WARNUNG: "{verboten}" in der Seite — das macht sie '
                  f"organisationsintern und damit für Kundinnen unbrauchbar")
    # Doppelte DOM-Kennungen zerlegen Anker und Beschriftungen — lautlos.
    ids = re.findall(r'\bid="([^"]+)"', seite)
    dopp = sorted({i for i in ids if ids.count(i) > 1})
    if dopp:
        print(f"  🚨 WARNUNG: doppelte id-Attribute: {', '.join(dopp)}")


if __name__ == "__main__":
    main()
