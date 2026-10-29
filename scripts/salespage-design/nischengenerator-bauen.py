"""Baut die Anmeldeseite des Nischengenerators und ihre Danke-Seite im KI-Design.

Kopf und CSS kommen unverändert aus der Story-Generator-Seite (dasselbe Design wie der
Tool-Workshop), der Inhalt aus nischengenerator-body.html und nischengenerator-danke-body.html.
Das Formular ist AC-Formular 75 „0€ Nischengenerator“ (Bestätigungsmail, danach Weiterleitung
zum Tool, nach dem Absenden auf die Danke-Seite).

    python scripts/salespage-design/nischengenerator-bauen.py
-> outputs/salespages/nischengenerator/index.html · danke.html · *-wp.html
"""
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parents[2]
vorlage = (ROOT / "outputs/salespages/story-generator/index.html").read_text(encoding="utf-8")
kopf_roh = vorlage[: vorlage.index("<!-- HERO -->")]
ende = vorlage[vorlage.index("</footer>") + len("</footer>"):]
ZIEL = ROOT / "outputs/salespages/nischengenerator"
ZIEL.mkdir(parents=True, exist_ok=True)

SEITEN = [
    ("nischengenerator-body.html", "index.html", "nischengenerator-wp.html", "Nischengenerator",
     '<a href="#anmelden" class="cta">Gratis loslegen</a>'),
    ("nischengenerator-danke-body.html", "danke.html", "nischengenerator-danke-wp.html", "Fast geschafft",
     '<a href="https://mumlifebalance.thrivecart.com/tool-workshop/" class="cta">Tool-Workshop &middot; 39 CHF</a>'),
]

for quelle, datei, wpdatei, titel, knopf in SEITEN:
    kopf = kopf_roh
    for alt, neu in [("STORY<b>&middot;</b>GENERATOR", "NISCHEN<b>&middot;</b>GENERATOR"),
                     ('<a href="#preis" class="cta">F&uuml;r 17 CHF / 17 &euro; holen</a>', knopf)]:
        assert kopf.count(alt) == 1, alt
        kopf = kopf.replace(alt, neu)
    kopf = re.sub(r"<title>.*?</title>", "<title>%s</title>" % titel, kopf, count=1, flags=re.S)
    inhalt = (ROOT / "scripts/salespage-design" / quelle).read_text(encoding="utf-8")
    seite = kopf + inhalt + ende
    (ZIEL / datei).write_text(seite, encoding="utf-8")
    # WordPress: CSS liegt im Customizer (Block STORY-GENERATOR-VERKAUFSSEITE, Scope .sg-sp)
    body = seite[seite.index("<body>") + 6: seite.index("</body>")].strip()
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    wp = '<div class="sg-sp">\n%s\n</div>' % body
    assert "<style" not in wp and "<script" not in wp
    (ZIEL / wpdatei).write_text(wp, encoding="utf-8")
    print("→", ZIEL / datei, "· WP", len(wp), "Zeichen")
