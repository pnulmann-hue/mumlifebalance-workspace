"""Baut die Anmeldeseite des Tool-Workshops im KI-Design.

Kopf und CSS kommen unverändert aus der Story-Generator-Seite (dasselbe Design),
der Inhalt aus tool-workshop-body.html daneben. Texte: outputs/produkte/tool-workshop/angebot/02-salespage.md

    python scripts/salespage-design/tool-workshop-bauen.py
-> outputs/salespages/tool-workshop/index.html
"""
import pathlib, sys
sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parents[2]
vorlage = (ROOT / "outputs/salespages/story-generator/index.html").read_text(encoding="utf-8")
inhalt = (ROOT / "scripts/salespage-design/tool-workshop-body.html").read_text(encoding="utf-8")

kopf = vorlage[: vorlage.index("<!-- HERO -->")]
ende = vorlage[vorlage.index("</footer>") + len("</footer>"):]

ERS = [
    ("STORY<b>&middot;</b>GENERATOR", "TOOL<b>&middot;</b>WORKSHOP"),
    ("F&uuml;r 17 CHF / 17 &euro; holen</a>", "Ich bin dabei &middot; 39 CHF / 39 &euro;</a>"),
]
for alt, neu in ERS:
    assert kopf.count(alt) == 1, alt
    kopf = kopf.replace(alt, neu)
import re
kopf = re.sub(r"<title>.*?</title>", "<title>Tool-Workshop</title>", kopf, count=1, flags=re.S)

ziel = ROOT / "outputs/salespages/tool-workshop/index.html"
ziel.parent.mkdir(parents=True, exist_ok=True)
seite = kopf + inhalt + ende
ziel.write_text(seite, encoding="utf-8")
print("→", ziel)

# WordPress-Fassung: dasselbe CSS liegt schon im Customizer (Block STORY-GENERATOR-VERKAUFSSEITE,
# gescopt auf .sg-sp). Darum nur den Inhalt in .sg-sp packen, kein eigenes CSS.
body = seite[seite.index("<body>") + 6: seite.index("</body>")].strip()
body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
wp = f'<div class="sg-sp">\n{body}\n</div>'
assert "<style" not in wp and "<script" not in wp
(ziel.parent / "tool-workshop-wp.html").write_text(wp, encoding="utf-8")
print("→ WP-Inhalt", len(wp), "Zeichen")

# Danke-Seite nach dem Kauf (ThriveCart leitet nach Kasse, Upsell und Downsell dorthin):
# Termine, Vorbereitung wie in Mail B0, das MBA-Webinar als ruhiger zweiter Block.
danke_kopf = kopf.replace("Ich bin dabei &middot; 39 CHF / 39 &euro;</a>", "Zum Nischengenerator</a>")
danke_kopf = danke_kopf.replace('href="#preis" class="cta"', 'href="https://mlb-nischengenerator.vercel.app" class="cta"')
assert "Zum Nischengenerator" in danke_kopf and "mlb-nischengenerator" in danke_kopf
danke_kopf = re.sub(r"<title>.*?</title>", "<title>Willkommen im Tool-Workshop</title>", danke_kopf, count=1, flags=re.S)
danke = danke_kopf + (ROOT / "scripts/salespage-design/tool-workshop-danke-body.html").read_text(encoding="utf-8") + ende
(ziel.parent / "danke.html").write_text(danke, encoding="utf-8")
body = danke[danke.index("<body>") + 6: danke.index("</body>")].strip()
body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
wp = f'<div class="sg-sp">\n{body}\n</div>'
assert "<style" not in wp and "<script" not in wp
(ziel.parent / "tool-workshop-danke-wp.html").write_text(wp, encoding="utf-8")
print("→ Danke-Seite", len(wp), "Zeichen")
