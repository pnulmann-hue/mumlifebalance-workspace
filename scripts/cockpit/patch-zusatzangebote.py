"""Reiter «Produkte → Upsell-Ersteller» (29.10.2026).

Patricia: *„ich brauche im cockpit drin unbedingt auch noch einen upsell,
downsell, crosssell ersteller“*. Produkt wählen → Claude (über `sample`) schlägt
Bump, Upsell, Downsell und Cross-Sell vor, aus bestehenden Produkten oder als
neues KI-Tool. Die Preis-Kette rechnet die Seite danach selbst nach.

Liest `daten/katalog` (Preise aus ThriveCart) und `daten/produkt-details`
(nur lesen). Schreibt nur in die eigene Sammlung `zusatzangebote`.

Code und CSS liegen daneben in `zusatzangebote-reiter.js` / `.css`.

    python scripts/cockpit/patch-zusatzangebote.py [--datei <cockpit.html>]
"""

import os
import pathlib
import subprocess
import sys
import tempfile

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HIER = pathlib.Path(__file__).resolve().parent
ROOT = HIER.parents[1]
JS_DATEI = HIER / "zusatzangebote-reiter.js"
CSS_DATEI = HIER / "zusatzangebote-reiter.css"

A_TABS = '''    { id: "katalog", label: "Angebots-Katalog" },'''
N_TABS = A_TABS + '''
    { id: "zusatzangebote", label: "Upsell-Ersteller" },'''

A_BER = '''tabs: ["katalog", "produkte",'''
N_BER = '''tabs: ["katalog", "zusatzangebote", "produkte",'''

A_DISP = '''    else if (activeTab === "katalog") renderKatalog(main);'''
N_DISP = A_DISP + '''
    else if (activeTab === "zusatzangebote") renderZusatzangebote(main);'''

JS_ANFANG = '''  /* ======================================================================
     Reiter "Zusatzangebote"'''
CSS_ANFANG = "  /* ---------- Upsell-Ersteller"
EINHAENGEN = '''  /* Reiter „Ideen von anderen": was bei den beobachteten Profilen deutlich'''


def ersetze(t, alt, neu, name):
    n = t.count(alt)
    if n != 1:
        sys.exit("🚨 «%s» kommt %dx vor — erwartet genau 1x. Nichts geändert." % (name, n))
    return t.replace(alt, neu, 1)


def pruefe_js(js, wo):
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
        f.write(js)
        tmp = f.name
    r = subprocess.run(["node", "--check", tmp], capture_output=True, text=True)
    os.unlink(tmp)
    if r.returncode != 0:
        sys.exit("🚨 node --check (%s): %s" % (wo, r.stderr or r.stdout))


def main():
    if "--datei" in sys.argv:
        ziel = pathlib.Path(sys.argv[sys.argv.index("--datei") + 1])
    else:
        ziel = ROOT / "outputs/cockpit/mlb-cockpit.html"
    js = JS_DATEI.read_text(encoding="utf-8")
    css = CSS_DATEI.read_text(encoding="utf-8")
    pruefe_js(js, JS_DATEI.name)

    t = ziel.read_text(encoding="utf-8")
    vorher = len(t)
    if "function renderZusatzangebote(" in t:
        # Schon eingebaut: JS-Block und CSS-Block ersetzen (wiederholbar).
        # Der Block endet beim nächsten Reiter-Kopf „/* =====“, sonst vor
        # EINHAENGEN. Andere Reiter (Gekaufte Kurse, Markt-Radar) stehen
        # dazwischen — bis EINHAENGEN zu ersetzen hätte sie am 31.10. gelöscht.
        a = t.find(JS_ANFANG)
        e = t.find(EINHAENGEN)
        naechster = t.find("\n  /* ======", a + len(JS_ANFANG))
        if 0 <= naechster < e:
            e = naechster + 1
        if a < 0 or e < a or t.count(JS_ANFANG) != 1:
            sys.exit("🚨 Den alten Reiter-Block nicht eindeutig gefunden. Nichts geändert.")
        t = t[:a] + js.rstrip() + "\n\n" + t[e:]
        # Der Block endet beim nächsten Abschnittskopf „/* ----------“ oder bei
        # </style>. Nicht einfach bis </style>: andere Reiter hängen ihr CSS
        # dahinter an (am 31.10. wäre sonst das CSS von „Gekaufte Kurse“ und
        # „Markt-Radar“ mitgelöscht worden).
        c = t.find(CSS_ANFANG)
        ende_style = t.find("</style>", c)
        naechster = t.find("\n  /* ----------", c + len(CSS_ANFANG))
        s = naechster + 1 if 0 <= naechster < ende_style else ende_style
        if c < 0 or s < c or t.count(CSS_ANFANG) != 1:
            sys.exit("🚨 Den alten CSS-Block nicht eindeutig gefunden. Nichts geändert.")
        t = t[:c] + css + t[s:]
        pruefe_js(t[t.rfind("<script>") + 8:t.rfind("</script>")], "ganze Seite")
        neu = ziel.with_suffix(".tmp")
        neu.write_text(t, encoding="utf-8")
        os.replace(neu, ziel)
        print("%s: Reiter erneuert, %d -> %d Zeichen, node --check grün" % (ziel.name, vorher, len(t)))
        return

    t = ersetze(t, A_TABS, N_TABS, "TABS")
    t = ersetze(t, A_BER, N_BER, "BEREICHE")
    t = ersetze(t, A_DISP, N_DISP, "Dispatcher")
    t = ersetze(t, EINHAENGEN, js.rstrip() + "\n\n" + EINHAENGEN, "renderZusatzangebote")

    i = t.rfind("</style>")
    if i < 0:
        sys.exit("🚨 kein </style> gefunden")
    t = t[:i] + css + t[i:]

    pruefe_js(t[t.rfind("<script>") + 8:t.rfind("</script>")], "ganze Seite")

    # Erst in eine Nebendatei, dann umbenennen — ein Fehler beim Schreiben
    # darf das Cockpit nicht leeren.
    neu = ziel.with_suffix(".tmp")
    neu.write_text(t, encoding="utf-8")
    os.replace(neu, ziel)
    print("%s: %d -> %d Zeichen, node --check grün" % (ziel.name, vorher, len(t)))


if __name__ == "__main__":
    main()
