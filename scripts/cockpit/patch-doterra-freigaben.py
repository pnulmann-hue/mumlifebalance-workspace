"""Reiter doTERRA → Freigaben (05.11.2026): Monats-Newsletter und Saison-Beiträge freigeben.

Patricia: *„das erstellte e-mail sollst du im artefact cockpit irgendwo ablegen, dass ich es freigeben kann“* ·
*„auch hier ins artefact ablegen mit freigabeknopf“*. Sammlung `doterra-freigaben`, Ausführung im Task
`doterra-freigaben-ausfuehren`. Auf Mein Tisch steht ein Punkt in „Heute dran“, solange etwas wartet.

    python scripts/cockpit/patch-doterra-freigaben.py [--datei <cockpit.html>]

Wiederholbar: Ein Neulauf ersetzt nur den eigenen Code-Block und das eigene CSS.
"""
import os
import pathlib
import re
import subprocess
import sys
import tempfile

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HIER = pathlib.Path(__file__).resolve().parent
ROOT = HIER.parents[1]
VON, BIS = "/* DF-ANFANG */", "/* DF-ENDE */"
CSS_VON, CSS_BIS = "/* DF-CSS-ANFANG */", "/* DF-CSS-ENDE */"
EINHAENGEN = "  /* ---------- Rising Leaders: Aufträge + Beraterinnen ---------- */"
ERSATZ = [
    ('    { id: "academy", label: "Ölschule-Calls" },',
     '    { id: "academy", label: "Ölschule-Calls" },\n    { id: "dtfreigaben", label: "Freigaben" },', "Reiterliste"),
    ('tabs: ["oelwissen", "anliegen", "bizwege", "rising", "academy", "rangtracker", "team"]',
     'tabs: ["dtfreigaben", "oelwissen", "anliegen", "bizwege", "rising", "academy", "rangtracker", "team"]', "Bereich"),
    ('    else if (activeTab === "academy") renderAcademy(main);',
     '    else if (activeTab === "academy") renderAcademy(main);\n    else if (activeTab === "dtfreigaben") renderDtFreigaben(main);', "Dispatch"),
    ('    if (tfFaellig()) P.push({ art: "doterra", titel: "Team-Funke für diese Woche"',
     '    if (!dfDocs) dfHolen();\n'
     '    if (dfOffen().length) P.push({ art: "doterra", titel: "doTERRA: " + dfOffen().length + " zur Freigabe", klein: "Newsletter oder Saison-Beiträge warten auf dein Ja.", gehe: "dtfreigaben", dringend: true });\n'
     '    if (tfFaellig()) P.push({ art: "doterra", titel: "Team-Funke für diese Woche"', "Heute dran"),
]


def pruefe_js(js, wo):
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
        f.write(js)
        tmp = f.name
    r = subprocess.run(["node", "--check", tmp], capture_output=True, text=True)
    os.unlink(tmp)
    if r.returncode != 0:
        sys.exit("🚨 node --check (%s): %s" % (wo, r.stderr or r.stdout))


def main():
    ziel = pathlib.Path(sys.argv[sys.argv.index("--datei") + 1]) if "--datei" in sys.argv else ROOT / "outputs/cockpit/mlb-cockpit.html"
    js = (HIER / "doterra-freigaben.js").read_text(encoding="utf-8")
    css = (HIER / "doterra-freigaben.css").read_text(encoding="utf-8")
    pruefe_js("(function(){" + js + "})();", "doterra-freigaben.js")
    t = ziel.read_text(encoding="utf-8")
    block = "  " + VON + "\n" + js.rstrip() + "\n  " + BIS + "\n"
    cssblock = "\n  " + CSS_VON + css.rstrip() + "\n  " + CSS_BIS + "\n"
    if VON in t:
        t = re.sub(re.escape("  " + VON) + r"\n.*?" + re.escape(BIS) + r"\n", lambda m: block, t, count=1, flags=re.S)
        t = re.sub(r"\n  " + re.escape(CSS_VON) + r".*?" + re.escape(CSS_BIS) + r"\n", lambda m: cssblock, t, count=1, flags=re.S)
    else:
        for alt, neu, name in ERSATZ:
            if t.count(alt) != 1:
                sys.exit("🚨 «%s» kommt %dx vor, erwartet 1x. Nichts geändert." % (name, t.count(alt)))
            t = t.replace(alt, neu, 1)
        if t.count(EINHAENGEN) != 1:
            sys.exit("🚨 Einhängestelle nicht eindeutig")
        t = t.replace(EINHAENGEN, block + "\n" + EINHAENGEN, 1)
        i = t.rfind("</style>")
        t = t[:i] + cssblock + t[i:]
    pruefe_js(t[t.rfind("<script>") + 8:t.rfind("</script>")], "ganze Seite")
    neu = ziel.with_suffix(".tmp")
    neu.write_text(t, encoding="utf-8")
    os.replace(neu, ziel)
    print(ziel.name, len(t), "Zeichen, node --check grün")


if __name__ == "__main__":
    main()
