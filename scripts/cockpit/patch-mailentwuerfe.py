"""
Neue Mail-Fassungen im Cockpit: unter „Listen & Automationen“ steht bei der
passenden Automation die neue Mail mit echter HTML-Vorschau und Knöpfen für
HTML, Betreff und Vorschautext — oberhalb dessen, was heute in ActiveCampaign
steckt.

  python scripts/cockpit/patch-mailentwuerfe.py [datei ...]

Ohne Angabe wird outputs/cockpit/mlb-cockpit.html gepatcht. Wiederholbar: ist
der Patch schon drin, passiert nichts.

Daten: Sammlung `mailentwuerfe` (je Mail ein Dokument mit `automation`,
`betreff`, `html` …), geschrieben von scripts/magnet-ich/mails-ins-cockpit.py.
🚨 Die Vorschau läuft im iframe mit `sandbox=""` — keine Skripte, kein Zugriff
auf die Seite. `srcdoc` wird per JS gesetzt, nicht als Attribut, sonst müsste
das ganze Mail-HTML maskiert durch innerHTML.
"""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
MARKE = "mailEntwuerfeVerdrahten"

ERSETZUNGEN = [
    # 1 · CSS neben den bestehenden Mailkarten
    (
        "  /* ---------- Mailtexte ---------- */\n",
        "  /* ---------- Mailtexte ---------- */\n"
        "  .mentwuerfe { margin-bottom: 4px; }\n"
        "  .mailkarte.mentwurf { border-color: var(--orange); background: var(--surface); }\n"
        "  .mentwurf .mailkopf { background: var(--orange-soft); border-radius: 8px 8px 0 0; }\n"
        "  .mentwurfinfo { padding: 8px 12px 0; font-size: 12.5px; color: var(--ink-soft); line-height: 1.55; }\n"
        "  .mentwurfknoepfe { display: flex; flex-wrap: wrap; gap: 8px; padding: 10px 12px; }\n"
        "  .mentwurfvorschau { display: block; width: 100%; height: 560px; border: 0;\n"
        "    border-top: 1px solid var(--line); background: #fff; border-radius: 0 0 8px 8px; }\n"
        "  .dneu { color: var(--orange); font-weight: 700; }\n",
    ),
    # 2 · bestehende Liste umbenennen, neue davor
    (
        "  function mailListe(nummer) {\n",
        "  /* Neue Mail-Fassungen von Claude, noch nicht in ActiveCampaign.\n"
        "     Sammlung `mailentwuerfe` — siehe scripts/cockpit/patch-mailentwuerfe.py. */\n"
        "  var mailEntwuerfe = null;\n"
        "  function mailEntwuerfeHolen() {\n"
        "    if (!db || mailEntwuerfe) return;\n"
        "    mailEntwuerfe = [];\n"
        "    db.collection(\"mailentwuerfe\").limit(50).get().then(function (qs) {\n"
        "      mailEntwuerfe = qs.docs.map(function (d) { var x = d.data() || {}; x.id = d.id; return x; });\n"
        "      if (activeTab === \"mailings\") render();\n"
        "    }).catch(function () {});\n"
        "  }\n"
        "  function entwuerfeFuer(nummer) {\n"
        "    return (mailEntwuerfe || []).filter(function (e) {\n"
        "      return String(e.automation) === String(nummer);\n"
        "    }).sort(function (a, b) { return (a.reihenfolge || 0) - (b.reihenfolge || 0); });\n"
        "  }\n"
        "  function mailListe(nummer) {\n"
        "    var neu = entwuerfeFuer(nummer);\n"
        "    if (!neu.length) return mailListeAC(nummer);\n"
        "    return '<div class=\"mentwuerfe\"><p class=\"note\">Neue Fassung von mir, noch nicht in ' +\n"
        "      'ActiveCampaign. Schau dir die Vorschau an, kopier das HTML und setz es in der ' +\n"
        "      'Automation ein.</p>' +\n"
        "      neu.map(function (e) {\n"
        "        return '<div class=\"mailkarte mentwurf\" data-entwurf=\"' + esc(e.id) + '\">' +\n"
        "          '<div class=\"mailkopf\"><strong>' + esc(e.betreff || \"Ohne Betreff\") + '</strong>' +\n"
        "          '<span class=\"note\">' + esc(e.warten || \"\") + '</span></div>' +\n"
        "          '<div class=\"mentwurfinfo\">' + esc(e.wann || \"\") +\n"
        "          (e.betreff2 ? '<br>Zweiter Betreff: ' + esc(e.betreff2) : \"\") +\n"
        "          (e.preheader ? '<br>Vorschautext: ' + esc(e.preheader) : \"\") + '</div>' +\n"
        "          '<div class=\"mentwurfknoepfe\">' +\n"
        "          '<button class=\"btn primary\" data-kopie=\"html\">HTML kopieren</button>' +\n"
        "          '<button class=\"btn\" data-kopie=\"betreff\">Betreff kopieren</button>' +\n"
        "          (e.preheader ? '<button class=\"btn\" data-kopie=\"preheader\">Vorschautext kopieren</button>' : \"\") +\n"
        "          '</div><iframe class=\"mentwurfvorschau\" sandbox=\"\" title=\"Vorschau der Mail\"></iframe></div>';\n"
        "      }).join(\"\") +\n"
        "      '<p class=\"note\" style=\"margin-top:16px\">Und das steckt heute in ActiveCampaign:</p></div>' +\n"
        "      mailListeAC(nummer);\n"
        "  }\n"
        "  function mailEntwuerfeVerdrahten(box) {\n"
        "    Array.prototype.forEach.call(box.querySelectorAll(\"[data-entwurf]\"), function (k) {\n"
        "      var e = (mailEntwuerfe || []).filter(function (x) {\n"
        "        return x.id === k.getAttribute(\"data-entwurf\");\n"
        "      })[0];\n"
        "      if (!e) return;\n"
        "      var f = k.querySelector(\"iframe\");\n"
        "      if (f) f.srcdoc = e.html || \"\";\n"
        "      Array.prototype.forEach.call(k.querySelectorAll(\"[data-kopie]\"), function (b) {\n"
        "        b.onclick = function (ev) {\n"
        "          ev.stopPropagation();\n"
        "          inDieZwischenablage(e[b.getAttribute(\"data-kopie\")] || \"\", b);\n"
        "        };\n"
        "      });\n"
        "    });\n"
        "  }\n"
        "  function mailListeAC(nummer) {\n",
    ),
    # 3 · Daten holen, sobald der Reiter gezeichnet wird
    (
        "  function renderMailings(main) {\n",
        "  function renderMailings(main) {\n    mailEntwuerfeHolen();\n",
    ),
    # 4 · Hinweis im Kopf der Automation
    (
        "        ' · Nr. ' + esc(String(a.nummer)) + '</span></button>' +\n",
        "        ' · Nr. ' + esc(String(a.nummer)) +\n"
        "        (entwuerfeFuer(a.nummer).length ? ' · <span class=\"dneu\">neue Fassung</span>' : \"\") +\n"
        "        '</span></button>' +\n",
    ),
    # 5 · nach dem Zeichnen verdrahten
    (
        "        karte.querySelector(\".dkoerper\").innerHTML = mailListe(a.nummer);\n",
        "        karte.querySelector(\".dkoerper\").innerHTML = mailListe(a.nummer);\n"
        "        mailEntwuerfeVerdrahten(karte.querySelector(\".dkoerper\"));\n",
    ),
]


def patchen(pfad):
    roh = pfad.read_bytes().decode("utf-8")
    crlf = "\r\n" in roh
    t = roh.replace("\r\n", "\n")
    if MARKE in t:
        print("  schon drin:", pfad)
        return
    for alt, neu in ERSETZUNGEN:
        assert t.count(alt) == 1, "nicht genau einmal gefunden: %r" % alt[:60]
        t = t.replace(alt, neu)
    if crlf:
        t = t.replace("\n", "\r\n")
    pfad.write_bytes(t.encode("utf-8"))
    print("  gepatcht:", pfad)


if __name__ == "__main__":
    ziele = [pathlib.Path(p) for p in sys.argv[1:]] or [ROOT / "outputs/cockpit/mlb-cockpit.html"]
    for z in ziele:
        patchen(z)
