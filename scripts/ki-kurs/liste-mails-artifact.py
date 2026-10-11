# -*- coding: utf-8 -*-
"""Baut aus der Launch-Strecke eine Artifact-Seite zum Kopieren.

    python scripts/ki-kurs/liste-mails-bauen.py        # erst die Mails
    python scripts/ki-kurs/liste-mails-artifact.py     # dann die Seite
    # danach: Artifact publish mit outputs/produkte/ki-treppe/liste-mails/artifact.html

Je Mail eine Karte am Zeitstrahl: Datum, Betreff, Vorschautext, warum sie da
steht, Knöpfe für HTML und Betreff, aufklappbare Vorschau.

🚨 Die Seite wird ERZEUGT, nicht von Hand gepflegt. Ändert sich eine Mail, läuft
   erst `liste-mails-bauen.py` und dann dieses Skript — sonst stehen auf der
   Seite Texte, die so nirgends mehr rausgehen.

🚨 Keine Artifact-Fähigkeiten. Die Seite zeigt und kopiert, mehr nicht. `db`
   oder `assets` würden sie organisationsintern machen, und Patricia will sie
   am Handy aufmachen können.
"""
import html
import importlib.util
import json
import pathlib
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = pathlib.Path(__file__).resolve().parents[2]
QUELLE = ROOT / "outputs" / "produkte" / "ki-treppe" / "liste-mails"

_spec = importlib.util.spec_from_file_location(
    "liste_mails", ROOT / "scripts" / "ki-kurs" / "liste-mails-bauen.py")
_lm = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_lm)
MAILS = _lm.MAILS

CSS = """
/* Zeitstrahl in einer Spalte: das Datum links, die Mail rechts. Die Abfolge
   IST die Information — deshalb ein Strahl und keine Kachelwand. */
:root {
  --grund: #f3efe4;  --blatt: #fbf8f1;  --blatt-2: #ebe4d3;
  --tinte: #0c1c30;  --tinte-weich: #5f6f80;
  --linie: rgba(12,28,48,.14);
  --petrol: #12828c; --petrol-weich: rgba(18,130,140,.12);
  --orange: #dc822e; --orange-weich: rgba(220,130,46,.15);
  --warn: #b56a24;
  --display: "Philosopher", Georgia, "Times New Roman", serif;
  --body: "Source Sans 3", "Segoe UI", system-ui, sans-serif;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --grund: #0c1c30; --blatt: #12283f; --blatt-2: #1a3450;
    --tinte: #f1ecdd; --tinte-weich: #a8bccb;
    --linie: rgba(241,236,221,.16);
    --petrol: #35a8b2; --petrol-weich: rgba(53,168,178,.16);
    --orange: #eb9a4f; --orange-weich: rgba(235,154,79,.18);
    --warn: #d9a84b;
    color-scheme: dark;
  }
}
:root[data-theme="dark"] {
  --grund: #0c1c30; --blatt: #12283f; --blatt-2: #1a3450;
  --tinte: #f1ecdd; --tinte-weich: #a8bccb;
  --linie: rgba(241,236,221,.16);
  --petrol: #35a8b2; --petrol-weich: rgba(53,168,178,.16);
  --orange: #eb9a4f; --orange-weich: rgba(235,154,79,.18);
  --warn: #d9a84b;
  color-scheme: dark;
}
* { box-sizing: border-box; }
body {
  margin: 0; background: var(--grund); color: var(--tinte);
  font-family: var(--body); font-size: 16px; line-height: 1.6;
  -webkit-font-smoothing: antialiased;
}
.huelle { max-width: 860px; margin: 0 auto; padding-block: 28px 80px; padding-left: 16px; padding-right: 16px; }

header h1 {
  font-family: var(--display); font-weight: 400; font-size: clamp(28px, 6vw, 40px);
  line-height: 1.12; margin: 0 0 8px; text-wrap: balance;
}
header .unter { margin: 0; color: var(--tinte-weich); font-size: 15px; max-width: 60ch; }
.zahlen { display: flex; gap: 10px; flex-wrap: wrap; margin: 18px 0 0; }
.zahl {
  background: var(--blatt); border: 1px solid var(--linie); border-radius: 999px;
  padding: 6px 14px; font-size: 13px; color: var(--tinte-weich);
}
.zahl b { color: var(--tinte); font-family: var(--display); font-size: 16px; margin-right: 5px; }

.hinweis {
  background: var(--orange-weich); border-radius: 12px; padding: 14px 18px;
  margin: 24px 0 0; font-size: 14.5px; line-height: 1.7;
}
.hinweis b { color: var(--warn); }

.strahl { margin: 34px 0 0; display: flex; flex-direction: column; gap: 18px; }

.mail {
  background: var(--blatt); border: 1px solid var(--linie); border-radius: 16px;
  overflow: hidden; display: grid; grid-template-columns: 92px minmax(0, 1fr);
}
@media (max-width: 560px) { .mail { grid-template-columns: 1fr; } }
.wann {
  background: var(--blatt-2); padding: 18px 12px; text-align: center;
  display: flex; flex-direction: column; align-items: center; gap: 3px;
  border-right: 1px solid var(--linie);
}
@media (max-width: 560px) {
  .wann { flex-direction: row; justify-content: flex-start; gap: 10px;
          border-right: 0; border-bottom: 1px solid var(--linie); text-align: left;
          padding: 10px 16px; }
}
.wann .nr {
  font-family: var(--display); font-size: 22px; line-height: 1; color: var(--petrol);
}
.wann .tag { font-size: 12px; color: var(--tinte-weich); font-variant-numeric: tabular-nums; }
.wann .uhr { font-size: 11px; color: var(--tinte-weich); opacity: .8; }

.koerper { padding: 18px 20px 20px; min-width: 0; }
.betreff {
  font-family: var(--display); font-size: 20px; line-height: 1.3; margin: 0 0 6px;
  text-wrap: balance;
}
.vorschautext { margin: 0 0 12px; font-size: 14px; color: var(--tinte-weich); font-style: italic; }
.warum {
  border-left: 3px solid var(--petrol); background: var(--petrol-weich);
  border-radius: 0 10px 10px 0; padding: 10px 14px; margin: 0 0 14px;
  font-size: 14px; line-height: 1.65;
}
.knoepfe { display: flex; gap: 8px; flex-wrap: wrap; }
button {
  font: inherit; font-size: 13.5px; cursor: pointer; border-radius: 999px;
  border: 1px solid var(--linie); background: var(--blatt-2); color: var(--tinte);
  padding: 8px 16px;
}
button:hover { border-color: var(--petrol); color: var(--petrol); }
button.haupt { background: var(--petrol); border-color: var(--petrol); color: #fff; }
button.haupt:hover { filter: brightness(1.08); color: #fff; }
button.fertig { background: #2f7d5b; border-color: #2f7d5b; color: #fff; }
button:focus-visible { outline: 2px solid var(--petrol); outline-offset: 2px; }

details { margin: 14px 0 0; }
summary { cursor: pointer; font-size: 13.5px; color: var(--petrol); }
summary::marker { color: var(--petrol); }
iframe {
  display: block; width: 100%; height: 520px; border: 1px solid var(--linie);
  border-radius: 10px; background: #fff; margin: 12px 0 0;
}
pre.roh {
  margin: 12px 0 0; padding: 12px 14px; background: var(--blatt-2);
  border-radius: 10px; overflow-x: auto; font-size: 12px; line-height: 1.5;
  max-height: 260px; white-space: pre-wrap; word-break: break-all;
}
footer { margin: 40px 0 0; padding-top: 20px; border-top: 1px solid var(--linie);
         font-size: 13.5px; color: var(--tinte-weich); line-height: 1.7; }
@media (prefers-reduced-motion: reduce) { * { transition: none !important; } }
"""

JS = r"""
function ablegen(knopf, text, nurText) {
  var alt = knopf.textContent;
  function gut() {
    knopf.textContent = "kopiert ✓"; knopf.classList.add("fertig");
    setTimeout(function () { knopf.textContent = alt; knopf.classList.remove("fertig"); }, 1800);
  }
  function auswaehlen() {
    // Rückweg, wenn die Zwischenablage abgelehnt wird: Text markieren,
    // damit sie ihn selbst kopieren kann.
    var f = document.createElement("textarea");
    f.value = text; f.setAttribute("readonly", "");
    f.style.position = "fixed"; f.style.top = "-1000px";
    document.body.appendChild(f); f.select();
    try { document.execCommand("copy"); gut(); }
    catch (e) { knopf.textContent = "ging nicht — Vorschau öffnen"; }
    f.remove();
  }
  if (!navigator.clipboard) { auswaehlen(); return; }
  if (nurText || !window.ClipboardItem || !navigator.clipboard.write) {
    navigator.clipboard.writeText(text).then(gut, auswaehlen);
    return;
  }
  // Zwei Formen: Quelltext für den Code-Editor, gesetzte Mail für ein Textfeld.
  try {
    navigator.clipboard.write([new ClipboardItem({
      "text/plain": new Blob([text], { type: "text/plain" }),
      "text/html": new Blob([text], { type: "text/html" })
    })]).then(gut, function () { navigator.clipboard.writeText(text).then(gut, auswaehlen); });
  } catch (e) { auswaehlen(); }
}

document.addEventListener("click", function (e) {
  var k = e.target.closest("button[data-feld]");
  if (!k) return;
  var karte = k.closest(".mail");
  var quelle = karte.querySelector('script[type="text/plain"][data-' + k.dataset.feld + ']');
  if (!quelle) return;
  ablegen(k, quelle.textContent, k.dataset.feld !== "html");
});

// Die Vorschau erst beim Aufklappen befüllen — acht Mails gleichzeitig zu
// rendern macht die Seite auf dem Handy träge.
document.addEventListener("toggle", function (e) {
  var d = e.target;
  if (d.tagName !== "DETAILS" || !d.open) return;
  var rahmen = d.querySelector("iframe");
  if (!rahmen || rahmen.dataset.gefuellt) return;
  var q = d.closest(".mail").querySelector('script[data-html]');
  rahmen.setAttribute("srcdoc", q.textContent);
  rahmen.dataset.gefuellt = "1";
}, true);
"""


def sichtbar(h):
    t = re.sub(r"(?is)<(style|script)[^>]*>.*?</\1>", " ", h)
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", t))).strip()


def notiz_kurz(m):
    """Die erste inhaltliche Zeile der Notiz — warum diese Mail da steht."""
    for z in (m.get("notiz") or "").strip().splitlines():
        z = z.strip()
        if z and not z.startswith("🚨"):
            return z
    return ""


def karte(i, m):
    pfad = QUELLE / m["datei"]
    roh = pfad.read_text(encoding="utf-8")
    # 🚨 In einem <script type="text/plain"> darf kein </script> stehen —
    #    sonst endet der Block mitten in der Mail und der Rest landet als
    #    Seitentext. Dieselbe Falle wie auf der lokalen Kopierseite.
    sicher = roh.replace("</script", "<\\/script")
    tag, uhr = (m["tag"].split("·") + [""])[:2]
    return (
      '<article class="mail">'
      '<div class="wann"><span class="nr">%d</span>'
      '<span class="tag">%s</span>%s</div>'
      '<div class="koerper">'
      '<h2 class="betreff">%s</h2>'
      '<p class="vorschautext">Vorschautext: %s</p>'
      '%s'
      '<div class="knoepfe">'
      '<button class="haupt" data-feld="html">HTML kopieren</button>'
      '<button data-feld="betreff">Betreff</button>'
      '<button data-feld="vorschautext">Vorschautext</button>'
      '</div>'
      '<details><summary>Vorschau anzeigen</summary><iframe loading="lazy" '
      'title="Vorschau: %s"></iframe></details>'
      '<script type="text/plain" data-html>%s</script>'
      '<script type="text/plain" data-betreff>%s</script>'
      '<script type="text/plain" data-vorschautext>%s</script>'
      '</div></article>'
    ) % (
      i,
      html.escape(tag.strip(), quote=False),
      ('<span class="uhr">%s</span>' % html.escape(uhr.strip(), quote=False)) if uhr.strip() else "",
      html.escape(m["betreff"], quote=False),
      html.escape(m["preheader"], quote=False),
      ('<p class="warum">%s</p>' % html.escape(notiz_kurz(m), quote=False)) if notiz_kurz(m) else "",
      html.escape(m["betreff"], quote=True),
      sicher,
      html.escape(m["betreff"], quote=False),
      html.escape(m["preheader"], quote=False),
    )


def main():
    fehlt = [m["datei"] for m in MAILS if not (QUELLE / m["datei"]).exists()]
    if fehlt:
        print("🚨 Diese Mails fehlen — erst liste-mails-bauen.py laufen lassen:")
        for f in fehlt:
            print("   " + f)
        sys.exit(1)

    karten = "".join(karte(i, m) for i, m in enumerate(MAILS, 1))
    zeichen = sum(len((QUELLE / m["datei"]).read_text(encoding="utf-8")) for m in MAILS)

    seite = (
      '<title>Launch-Strecke Easy KI</title>'
      '<link rel="preconnect" href="https://fonts.googleapis.com">'
      '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
      '<link href="https://fonts.googleapis.com/css2?family=Philosopher:wght@400;700'
      '&family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet">'
      '<style>%s</style>'
      '<div class="huelle">'
      '<header>'
      '<h1>Acht Mails an die &uuml;brige Liste</h1>'
      '<p class="unter">F&uuml;r alle, die <strong>nicht</strong> in der Masterclass waren '
      'und keinen Stimm-Check gemacht haben. Jede Mail hat ein Angebot und einen Link, '
      'so wie es sein soll &mdash; kein reiner Newsletter.</p>'
      '<div class="zahlen">'
      '<span class="zahl"><b>8</b>Mails</span>'
      '<span class="zahl"><b>10.&ndash;23.</b>Oktober</span>'
      '<span class="zahl"><b>277</b>bis 15.10., danach 333</span>'
      '<span class="zahl"><b>2</b>am Schlusstag</span>'
      '</div>'
      '<p class="hinweis"><b>Vor dem Versand:</b> In Mail&nbsp;5 steht ein leerer '
      'Beweis-Kasten mit der Aufschrift &bdquo;Hier geh&ouml;rt ein Screenshot hin&ldquo;. '
      'Setz dort einen abfotografierten Chat ein &mdash; oder l&ouml;sch den Kasten. '
      'Erfunden habe ich keinen, und ohne das Ja der Kundin geh&ouml;rt auch keiner rein.</p>'
      '</header>'
      '<main class="strahl">%s</main>'
      '<footer>'
      '<p><strong>Was in diesen Mails steht, ist belegt.</strong> Vier Kinder, '
      'achtzehn Stunden Woche, keine technische Ausbildung, der Kochbot, das Cockpit '
      'und der Doppelpost-Fehler &mdash; alles aus den Kursunterlagen. '
      'Die Kundin in Mail&nbsp;3 steht anonym und als '
      'Zusammenfassung drin, weil ihre Freigabe noch aussteht und ihr Wortlaut '
      'unabgetippt auf dem Handy liegt.</p>'
      '<p>&bdquo;HTML kopieren&ldquo; legt den Quelltext <strong>und</strong> die '
      'gesetzte Mail ab: in den Code-Editor von ActiveCampaign kommt der Quelltext, '
      'in ein Textfeld die fertige Mail.</p>'
      '</footer>'
      '</div>'
      '<script>%s</script>'
    ) % (CSS, karten, JS)

    ziel = QUELLE / "artifact.html"
    ziel.write_text(seite, encoding="utf-8")
    print("%d Mails · %d Zeichen Mail-HTML · Seite %d KB" % (
        len(MAILS), zeichen, len(seite) // 1024))
    print("Geschrieben: %s" % ziel.relative_to(ROOT))
    print("\nDanach: Artifact publish mit dieser Datei.")


if __name__ == "__main__":
    main()
