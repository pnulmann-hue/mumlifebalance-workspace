"""Baut die Stimm-Check-Landingpage aus dem Minikurs-Baukasten.

CSS = der <style>-Block aus .claude/skills/minikurs-salespage/references/reference-page.html,
unveraendert, nur auf .sc-sp gescopt (WordPress laesst kein <style> in die Seite -> Customizer).
Gleiches Verfahren wie scripts/salespage-design/magnet-ich-bauen.py — die Scope-Funktion wird
von dort importiert, nicht kopiert.

    python scripts/salespage-design/stimm-check-bauen.py
-> outputs/salespages/stimm-check/stimm-check.css   (in den Customizer)
   outputs/salespages/stimm-check/stimm-check-wp.html (Seiteninhalt fuer WordPress)
   outputs/salespages/stimm-check/index.html       (lokale Vorschau)
"""
import importlib.util, json, pathlib, re, sys
sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parents[2]
REF = ROOT / ".claude/skills/minikurs-salespage/references/reference-page.html"
OUT = ROOT / "outputs/salespages/stimm-check"
SC = ".sc-sp"

# scope() aus dem Magnet-Ich-Bau leihen, ohne dessen Hauptteil auszufuehren
quelle = (ROOT / "scripts/salespage-design/magnet-ich-bauen.py").read_text(encoding="utf-8")
funktionen = quelle[quelle.index("def scope_sel"):quelle.index("ref = REF.read_text")]
ns = {"re": re, "SC": SC}
exec(funktionen, ns)
scope = ns["scope"]

FORMULAR = "https://mumlifebalance.activehosted.com/f/71"
MEDIEN = OUT / "medien.json"   # WP-Adressen der Bilder, schreibt das Deploy-Skript
medien = json.loads(MEDIEN.read_text(encoding="utf-8")) if MEDIEN.exists() else {}
BILD_PATRICIA = "https://mumlifebalance.ch/wp-content/uploads/2026/09/mi-about.jpg"

ref = REF.read_text(encoding="utf-8")
css = ref[ref.index("<style>") + 7: ref.index("</style>")]
scoped = scope(css)

# Handy: die Vorlage stapelt Blase, Bild und drei Zahlenkarten untereinander — fünf
# Bildschirme lang. Hier bleibt es eine Collage: Blase über dem Bild, die drei Zahlen
# als Reihe, die leicht verdreht über die Unterkante des Bildes greift. (Patricia, 28.09.)
MOBIL_COLLAGE = f"""/* Handy: Collage statt Stapel */
@media (max-width: 860px) {{
  {SC} .collage {{ display:grid; grid-template-columns:repeat(3,1fr); gap:10px; max-width:420px; margin-left:auto; margin-right:auto; }}
  {SC} .collage .el {{ max-width:none; width:auto; }}
  {SC} .collage .e-bubble {{ grid-column:1 / -1; order:-2; justify-self:center; transform:rotate(-3deg); margin-bottom:-22px; z-index:6; font-size:14px; }}
  {SC} .collage .carousel-main {{ grid-column:1 / -1; order:-1; width:80%; }}
  {SC} .collage .stat {{ order:0; margin-top:-38px; z-index:6; padding:12px 10px; text-align:center; }}
  {SC} .collage .stat .n {{ font-size:26px; }}
  {SC} .collage .stat .l {{ font-size:10px; letter-spacing:.5px; }}
  {SC} .collage .e-tl {{ transform:rotate(-4deg); }}
  {SC} .collage .e-ml {{ transform:rotate(2deg); margin-top:-26px; }}
  {SC} .collage .e-mr {{ transform:rotate(-2deg); }}
}}
"""

ANPASSUNG = f"""
/* === Stimm-Check: Anpassungen gegenueber der Vorlage === */
/* Einblend-Effekt braucht JavaScript, WordPress blockt <script> -> immer sichtbar */
{SC} .rev{{opacity:1 !important;transform:none !important;}}
/* Hero-Bild ist ein hoher Ergebnis-Ausschnitt, kein quadratisches Mockup */
{SC} .carousel-main img{{height:auto;max-height:520px;object-fit:contain;background:transparent;}}
/* Elementor-Kit faerbt jede Ueberschrift (.elementor-kit-5 h1) -> Farbe wieder von der Sektion erben.
   :is() haelt die Spezifitaet niedrig, damit die Klassen der Vorlage (.story-head usw.) weiter gewinnen. */
{SC} :is(h1,h2,h3,h4,h5,h6){{color:inherit;}}
/* Preisblock ohne Streichpreis: „kostenlos“ als Wort statt Zahl */
{SC} .pl-price .now{{font-size:40px;}}
/* WordPress laedt „Source Sans Pro“ (nicht „Source Sans 3“) -> sonst faellt der Text auf Arial */
{SC}{{font-family:'Source Sans 3','Source Sans Pro','Helvetica Neue',Arial,sans-serif;}}
{MOBIL_COLLAGE}"""
(OUT / "stimm-check.css").write_text("/* === STIMM-CHECK-LANDINGPAGE (auto) === */\n" + scoped + ANPASSUNG, encoding="utf-8")

inhalt = (OUT / "stimm-check-inhalt.html").read_text(encoding="utf-8")
def fuellen(html, ergebnis_bild):
    html = html.replace("{{FORMULAR}}", FORMULAR).replace("{{BILD_PATRICIA}}", BILD_PATRICIA).replace("{{BILD_ERGEBNIS}}", ergebnis_bild)
    rest = re.findall(r"\{\{[A-Z_]+\}\}", html)
    assert not rest, rest
    return html

wp_bild = medien.get("stimm-ergebnis.png", "")
if wp_bild:
    (OUT / "stimm-check-wp.html").write_text(fuellen(inhalt, wp_bild), encoding="utf-8")
else:
    print("⚠ stimm-ergebnis.png noch nicht hochgeladen — stimm-check-wp.html nicht gebaut")

fonts = re.search(r'<link href="https://fonts.googleapis.com[^>]+>', ref).group(0)
(OUT / "index.html").write_text(
    f'<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
    f'<title>Stimm-Check · Vorschau</title>{fonts}<style>body{{margin:0}}\n{(OUT / "stimm-check.css").read_text(encoding="utf-8")}</style></head>'
    f'<body>{fuellen(inhalt, "assets/stimm-ergebnis.png")}</body></html>', encoding="utf-8")

# Sprachpruefung auf dem sichtbaren Text
text = re.sub(r"<[^>]+>", " ", re.sub(r"<!--.*?-->", "", inhalt, flags=re.S))
funde = [m for m in (r"ß", r"[Ss]tell dir[^.!?]{0,60}vor", r"\bsondern\b", r"Kund:innen") if re.search(m, text)]
print("CSS", len(scoped), "Zeichen · index.html gebaut · Sprachpruefung:", "sauber" if not funde else funde)
