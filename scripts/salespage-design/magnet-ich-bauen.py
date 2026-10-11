"""Baut die Magnet-Ich-Salespage aus dem Signature-Baukasten.

CSS = der <style>-Block aus .claude/skills/signature-kurs-salespage/references/reference-page.html,
unveraendert, nur auf .mi-sp gescopt (WordPress laesst kein <style> in die Seite -> Customizer).
Dazu wenige, kommentierte Anpassungen am Schluss (Bildpfade, Handy-Hero mit freiem Gesicht).

    python scripts/salespage-design/magnet-ich-bauen.py
-> outputs/salespages/magnet-ich/magnet-ich.css + index.html (lokale Vorschau)
"""
import re, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
REF = ROOT / ".claude/skills/signature-kurs-salespage/references/reference-page.html"
OUT = ROOT / "outputs/salespages/magnet-ich"
SC = ".mi-sp"

def scope_sel(sel):
    sel = sel.strip()
    if sel in (":root", "html,body", "body", "html"): return SC
    if sel == "*": return f"{SC}, {SC} *"
    return f"{SC} {sel}"

def scope(css):
    out, i = [], 0
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    while i < len(css):
        j = css.find("{", i)
        if j < 0: break
        head = css[i:j].strip()
        if head.startswith("@keyframes"):
            depth, k = 1, j + 1
            while depth: depth += {"{": 1, "}": -1}.get(css[k], 0); k += 1
            out.append(css[i:k].strip()); i = k; continue
        if head.startswith("@media"):
            depth, k = 1, j + 1
            while depth: depth += {"{": 1, "}": -1}.get(css[k], 0); k += 1
            out.append(head + "{\n" + scope(css[j + 1:k - 1]) + "\n}"); i = k; continue
        k = css.find("}", j)
        body = css[j + 1:k].strip()
        sels = ", ".join(scope_sel(s) for s in head.split(","))
        out.append(f"{sels} {{ {body} }}"); i = k + 1
    return "\n".join(out)

ref = REF.read_text(encoding="utf-8")
css = ref[ref.index("<style>") + 7: ref.index("</style>")]
scoped = scope(css)
assert "url('assets/dein-portrait.jpg')" in scoped
scoped = scoped.replace("background-image:url('assets/dein-portrait.jpg');", "")  # Bild kommt inline je Seite

ANPASSUNG = f"""
/* === Magnet-Ich: Anpassungen gegenueber der Vorlage === */
/* Hero-Foto am Handy: als .hero-mock ueber dem Text statt dahinter, sonst liegt der Text auf dem Gesicht */
@media(max-width:820px){{ {SC} .hero-bg{{background-image:none !important;min-height:0;}} {SC} .hero-bg::before{{display:none;}} {SC} .hero-content{{justify-content:flex-start;gap:26px;}} {SC} .hero-mock{{width:100%;max-width:100%;border-radius:18px;filter:none;aspect-ratio:4/5;object-fit:cover;object-position:88% 30%;}} }}
/* Chat-Bubbles ohne Bild-Screenshots: Zitat etwas groesser */
{SC} .bubble p{{font-size:16px;}}
/* P.S. im Statement-Band */
{SC} .statement .ps{{max-width:640px;margin:34px auto 0;text-align:left;color:rgba(255,255,255,0.78);font-size:16px;border-top:1px solid rgba(255,255,255,0.14);padding-top:24px;}}
{SC} .statement .ps b{{color:#f2bd8a;}}
{SC} .statement .btn{{margin-top:34px;}}
"""
(OUT / "magnet-ich.css").write_text("/* === MAGNET-ICH-SALESPAGE (auto) === */\n" + scoped + ANPASSUNG, encoding="utf-8")

body = (OUT / "magnet-ich-inhalt.html").read_text(encoding="utf-8").replace("#CHECKOUT", "https://mumlifebalance.thrivecart.com/magnet-ich/")
fonts = re.search(r'<link href="https://fonts.googleapis.com[^>]+>', ref).group(0)
(OUT / "index.html").write_text(f'<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Magnet-Ich</title>{fonts}<style>body{{margin:0}}\n{(OUT / "magnet-ich.css").read_text(encoding="utf-8")}</style></head><body>{body}</body></html>', encoding="utf-8")
print("CSS", len(scoped), "Zeichen · index.html gebaut")
