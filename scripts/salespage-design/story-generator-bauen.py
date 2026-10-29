"""Macht aus der Story-Generator-Verkaufsseite die WordPress-Fassung.

Quelle ist outputs/salespages/story-generator/index.html (KI-Design, dort wird Text geaendert).
Das CSS wird unveraendert auf .sg-sp gescopt (WordPress laesst kein <style> in die Seite -> Customizer).
Scope-Funktion aus magnet-ich-bauen.py geliehen, wie bei ki-masterclass-bauen.py.

    python scripts/salespage-design/story-generator-bauen.py
-> outputs/salespages/story-generator/story-generator.css      (in den Customizer)
   outputs/salespages/story-generator/story-generator-wp.html  (Seiteninhalt fuer WordPress)
"""
import pathlib, re, sys
sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "outputs/salespages/story-generator"
SC = ".sg-sp"

quelle = (ROOT / "scripts/salespage-design/magnet-ich-bauen.py").read_text(encoding="utf-8")
ns = {"re": re, "SC": SC}
exec(quelle[quelle.index("def scope_sel"):quelle.index("ref = REF.read_text")], ns)
scope = ns["scope"]

seite = (OUT / "index.html").read_text(encoding="utf-8")
css = seite[seite.index("<style>") + 7: seite.index("</style>")]
scoped = scope(css)
assert f"{SC} body::before" in scoped
scoped = scoped.replace(f"{SC} body::before", f"{SC}::before")

ANPASSUNG = f"""
/* === Story-Generator: Anpassungen fuer WordPress === */
{SC}{{position:relative;isolation:isolate;background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.7;overflow-x:hidden;}}
/* WordPress laedt „Source Sans Pro“ (nicht „Source Sans 3“) */
{SC}{{--sans:'Source Sans 3','Source Sans Pro',Arial,sans-serif;--tech:'Source Sans 3','Source Sans Pro',sans-serif;}}
/* Elementor-Kit faerbt Ueberschriften und Absaetze -> doppelte Klasse gewinnt */
{SC}{SC} :is(h1,h2){{color:#f1ecdd;}}
{SC}{SC} h3{{color:#f1ecdd;}}
{SC}{SC} p,{SC}{SC} li,{SC}{SC} summary{{font-family:var(--sans);}}
"""

body = seite[seite.index("<body>") + 6: seite.index("</body>")].strip()
body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
wp = f'<div class="{SC[1:]}">\n{body}\n</div>'
assert "<style" not in wp and "<script" not in wp

(OUT / "story-generator.css").write_text("/* === STORY-GENERATOR-VERKAUFSSEITE (auto) === */\n" + scoped + ANPASSUNG, encoding="utf-8")
(OUT / "story-generator-wp.html").write_text(wp, encoding="utf-8")
print("CSS", len(scoped), "Zeichen · WP-Inhalt", len(wp), "Zeichen")
