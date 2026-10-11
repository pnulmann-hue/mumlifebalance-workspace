# -*- coding: utf-8 -*-
"""Eine Seite mit allen Launch-Mails: Vorschau plus HTML zum Kopieren.

    python scripts/ki-kurs/launch-mails-kopierseite.py
    # dann: preview_start {"name": "launch-mails"}   (Port 4402)

Quelle sind die Dateien in `outputs/cockpit/abgleich/mailentwuerfe/`, die
`mails-ins-cockpit.py` aus ActiveCampaign geholt hat. Es steht also der Stand
da, der wirklich rausgeht — inklusive MBA-Block und Datumskorrektur.

🚨 Nur Mails mit `quelle: "activecampaign"`. Daneben liegen aeltere Entwuerfe,
   und ein Entwurf auf einer Seite, die „so geht es raus" verspricht, ist
   genau die Falschaussage, die den ganzen Rest unglaubwuerdig macht.

Kopiert wird ueber `ClipboardItem` mit `text/html` UND `text/plain` — in einen
Code-Editor landet der Quelltext, in ein Rich-Text-Feld die gesetzte Mail.
"""
import html
import json
import re
import pathlib
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = pathlib.Path(__file__).resolve().parents[2]
QUELLE = ROOT / "outputs" / "cockpit" / "abgleich" / "mailentwuerfe"
ZIEL = ROOT / "outputs" / "produkte" / "ki-treppe" / "launch-mails"

# Welche Automationen zum laufenden Launch gehoeren, in der Reihenfolge, in der
# eine Interessentin sie erlebt. 🚨 Die Nummern sind AC-IDs; der Titel kommt
# aus den Daten, damit hier keine veraltete Schreibweise stehenbleibt.
LAUNCH = ["84", "83", "85", "74", "69"]


def mails():
    raus = {}
    for f in sorted(QUELLE.glob("*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        if d.get("quelle") != "activecampaign":
            continue
        raus.setdefault(str(d.get("automation")), []).append(d)
    for k in raus:
        raus[k].sort(key=lambda d: d.get("reihenfolge", 0))
    return raus


CSS = """
:root{--creme:#f1ecdd;--petrol:#12828c;--blau:#0c1c30;--orange:#dc822e;
       --linie:rgba(12,28,48,.14)}
*{box-sizing:border-box}
body{margin:0;background:var(--creme);color:var(--blau);
     font:16px/1.6 "Source Sans 3","Segoe UI",system-ui,sans-serif}
header{background:var(--blau);color:var(--creme);padding:22px 26px}
header h1{font-family:Philosopher,Georgia,serif;font-weight:400;margin:0 0 4px;font-size:27px}
header p{margin:0;opacity:.85;font-size:14px}
main{max-width:1000px;margin:0 auto;padding:22px 18px 70px}
.auto{margin:0 0 30px}
.auto>h2{font-family:Philosopher,Georgia,serif;font-weight:400;font-size:22px;
         margin:26px 0 10px;padding-bottom:6px;border-bottom:2px solid var(--petrol)}
.karte{background:#fff;border:1px solid var(--linie);border-radius:14px;
       margin:0 0 14px;overflow:hidden}
.kopf{display:flex;gap:12px;align-items:baseline;flex-wrap:wrap;
      padding:13px 16px;background:#fbf8f1;border-bottom:1px solid var(--linie)}
.nr{font-family:Philosopher,Georgia,serif;font-size:19px;color:var(--petrol);min-width:26px;
     text-decoration:none}
.nr:hover{text-decoration:underline}
/* Angesprungene Karte hervorheben, sonst weiss man nach dem Klick nicht,
   wo man gelandet ist. */
.karte:target{box-shadow:0 0 0 3px var(--petrol)}
.name{font-weight:600}
.warten{font-size:12px;letter-spacing:.06em;text-transform:uppercase;
        background:rgba(18,130,140,.12);color:var(--petrol);padding:2px 10px;border-radius:999px}
.betreff{flex:1 1 100%;font-size:14px;color:#4d6076}
.betreff b{color:var(--blau)}
.knoepfe{display:flex;gap:8px;flex-wrap:wrap;padding:11px 16px}
button{font:inherit;font-size:13px;cursor:pointer;border:1px solid rgba(12,28,48,.28);
       background:#fff;border-radius:999px;padding:7px 15px}
button:hover{border-color:var(--petrol);color:var(--petrol)}
button.haupt{background:var(--petrol);border-color:var(--petrol);color:#fff}
button.fertig{background:#2f7d5b;border-color:#2f7d5b;color:#fff}
details>summary{cursor:pointer;padding:0 16px 12px;font-size:13px;color:var(--petrol)}
iframe{display:block;width:100%;height:620px;border:0;border-top:1px solid var(--linie);background:#fff}
.hinweis{background:rgba(220,130,46,.14);border-radius:10px;padding:11px 14px;
         font-size:14px;margin:0 0 18px}
"""

JS = r"""
function ablegen(knopf, roh, nurText){
  var alt = knopf.textContent;
  function fertig(){
    knopf.textContent = "kopiert ✓"; knopf.classList.add("fertig");
    setTimeout(function(){ knopf.textContent = alt; knopf.classList.remove("fertig"); }, 1800);
  }
  function einfach(){
    // Rückweg, wenn ClipboardItem fehlt oder abgelehnt wird.
    var t = document.createElement("textarea");
    t.value = roh; document.body.appendChild(t); t.select();
    try { document.execCommand("copy"); fertig(); }
    catch(e){ knopf.textContent = "ging nicht"; }
    t.remove();
  }
  if (nurText || !window.ClipboardItem || !navigator.clipboard || !navigator.clipboard.write) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(roh).then(fertig, einfach);
    } else { einfach(); }
    return;
  }
  // Zwei Formen im selben Vorgang: Quelltext für den Code-Editor, gesetzte
  // Mail für ein Rich-Text-Feld.
  var el = {
    "text/plain": new Blob([roh], {type:"text/plain"}),
    "text/html":  new Blob([roh], {type:"text/html"})
  };
  navigator.clipboard.write([new ClipboardItem(el)]).then(fertig, einfach);
}
document.addEventListener("click", function(e){
  var k = e.target.closest("button[data-feld]");
  if (!k) return;
  var karte = k.closest(".karte");
  var roh = karte.querySelector('script[type="text/plain"][data-' + k.dataset.feld + ']').textContent;
  ablegen(k, roh, k.dataset.feld !== "html");
});
"""


def anker(d):
    """Sprungmarke je Mail, damit es einen Link auf GENAU diese Karte gibt.
    Gebaut aus der Dokument-Kennung, also stabil ueber Neubauten hinweg."""
    return re.sub(r"[^a-z0-9]+", "-",
                  ("ki-launch-%s-%02d-%s" % (d.get("automation"), d.get("reihenfolge", 0),
                   (d.get("name") or "").lower()))).strip("-")[:60]


def karte(nr, d):
    h = d.get("html") or ""
    # 🚨 In ein <script type="text/plain"> kann kein </script> hinein — sonst
    #    endet der Block mitten in der Mail und der Rest landet als Seitentext.
    sicher = h.replace("</script", "<\\/script")
    return (
        '<div class="karte" id="%s">'
        '<div class="kopf">'
        '<a class="nr" href="#%s" title="Link auf genau diese Mail">%d</a>'
        '<span class="name">%s</span>'
        '<span class="warten">%s</span>'
        '<span class="betreff"><b>Betreff:</b> %s%s</span>'
        '</div>'
        '<div class="knoepfe">'
        '<button class="haupt" data-feld="html">HTML kopieren</button>'
        '<button data-feld="betreff">Betreff kopieren</button>'
        '%s'
        '</div>'
        '<details><summary>▸ Vorschau</summary>'
        '<iframe sandbox srcdoc="%s"></iframe></details>'
        '<script type="text/plain" data-html>%s</script>'
        '<script type="text/plain" data-betreff>%s</script>'
        '%s'
        '</div>'
    ) % (
        anker(d), anker(d), nr,
        html.escape(d.get("name") or "ohne Namen", quote=False),
        html.escape(d.get("warten") or "sofort", quote=False),
        html.escape(d.get("betreff") or "—", quote=False),
        (' &nbsp;·&nbsp; <i>%s</i>' % html.escape(d["preheader"], quote=False))
        if (d.get("preheader") or "").strip() else "",
        ('<button data-feld="vorschautext">Vorschautext kopieren</button>'
         if (d.get("preheader") or "").strip() else ""),
        html.escape(h, quote=True),
        sicher,
        html.escape(d.get("betreff") or "", quote=False),
        ('<script type="text/plain" data-vorschautext>%s</script>'
         % html.escape(d.get("preheader") or "", quote=False))
        if (d.get("preheader") or "").strip() else "",
    )


def main():
    alle = mails()
    fehlt = [a for a in LAUNCH if a not in alle]
    reihen = [a for a in LAUNCH if a in alle]
    # Was sonst noch aus AC da ist, kommt hinten dran — vollständig ist
    # besser als eine Auswahl, bei der man rät, was fehlt.
    reihen += sorted((a for a in alle if a not in LAUNCH),
                     key=lambda a: alle[a][0].get("automationName", ""))

    teile, gesamt = [], 0
    for aid in reihen:
        liste = alle[aid]
        name = liste[0].get("automationName") or ("Automation " + aid)
        karten = "".join(karte(i + 1, d) for i, d in enumerate(liste))
        teile.append('<section class="auto"><h2>%s <span class="warten">%d Mails</span></h2>%s</section>'
                     % (html.escape(name, quote=False), len(liste), karten))
        gesamt += len(liste)

    seite = (
        '<!doctype html><html lang="de"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>Launch-Mails zum Kopieren</title>'
        '<link href="https://fonts.googleapis.com/css2?family=Philosopher:wght@400'
        '&family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet">'
        '<style>%s</style></head><body>'
        '<header><h1>Launch-Mails zum Kopieren</h1>'
        '<p>%d Mails · Stand aus ActiveCampaign vom %s — das ist, was '
        'wirklich rausgeht.</p></header><main>'
        '<p class="hinweis">„HTML kopieren“ legt den Quelltext '
        '<b>und</b> die gesetzte Mail ab: in den Code-Editor von ActiveCampaign '
        'kommt der Quelltext, in ein Textfeld die fertige Mail. '
        'Die Reihenfolge je Automation ist der echte Ablauf, nicht die '
        'Kampagnen-Nummer.</p>'
        '%s</main><script>%s</script></body></html>'
    ) % (CSS, gesamt, __import__("datetime").date.today().strftime("%d.%m.%Y"),
         "".join(teile), JS)

    ZIEL.mkdir(parents=True, exist_ok=True)
    (ZIEL / "index.html").write_text(seite, encoding="utf-8")

    print("%d Mails aus %d Automationen" % (gesamt, len(reihen)))
    for aid in reihen[:8]:
        print("   %-44s %2d" % ((alle[aid][0].get("automationName") or aid)[:44], len(alle[aid])))
    if len(reihen) > 8:
        print("   … und %d weitere" % (len(reihen) - 8))
    if fehlt:
        print("\n⚠ Keine Mails gefunden fuer Automation: %s" % ", ".join(fehlt))
    print("\nGeschrieben: %s" % (ZIEL / "index.html").relative_to(ROOT))
    print('Ansehen:    preview_start {"name": "launch-mails"}   (Port 4402)')


if __name__ == "__main__":
    main()
