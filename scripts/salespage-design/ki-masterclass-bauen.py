"""Baut die Anmeldeseite der KI-Masterclass aus dem ki-salespage-Baukasten.

CSS = der <style>-Block aus .claude/skills/ki-salespage/references/reference-page.html,
unveraendert, nur auf .km-sp gescopt (WordPress laesst kein <style> in die Seite -> Customizer).
Scope-Funktion aus magnet-ich-bauen.py geliehen, nicht kopiert — wie beim Stimm-Check.

    python scripts/salespage-design/ki-masterclass-bauen.py
-> outputs/salespages/ki-masterclass/ki-masterclass.css     (in den Customizer)
   outputs/salespages/ki-masterclass/ki-masterclass-wp.html (Seiteninhalt fuer WordPress)
   outputs/salespages/ki-masterclass/index.html             (lokale Vorschau)
"""
import json, pathlib, re, sys
sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parents[2]
REF = ROOT / ".claude/skills/ki-salespage/references/reference-page.html"
OUT = ROOT / "outputs/salespages/ki-masterclass"
SC = ".km-sp"

quelle = (ROOT / "scripts/salespage-design/magnet-ich-bauen.py").read_text(encoding="utf-8")
ns = {"re": re, "SC": SC}
exec(quelle[quelle.index("def scope_sel"):quelle.index("ref = REF.read_text")], ns)
scope = ns["scope"]

FORMULAR = "https://mumlifebalance.activehosted.com/f/69"
MEDIEN = OUT / "medien.json"   # WP-Adressen der Bilder, schreibt das Deploy-Skript
medien = json.loads(MEDIEN.read_text(encoding="utf-8")) if MEDIEN.exists() else {}

ref = REF.read_text(encoding="utf-8")
css = ref[ref.index("<style>") + 7: ref.index("</style>")]
scoped = scope(css)
# body::before (Raster + Leuchten) gehoert an den Seiten-Container, nicht an ein body darin
assert f"{SC} body::before" in scoped
scoped = scoped.replace(f"{SC} body::before", f"{SC}::before")

ANPASSUNG = f"""
/* === KI-Masterclass: Anpassungen gegenueber der Vorlage === */
/* Container traegt, was in der Vorlage am body hing */
{SC}{{position:relative;isolation:isolate;}}
/* WordPress laedt „Source Sans Pro“ (nicht „Source Sans 3“) -> sonst faellt der Text auf Arial */
{SC}{{--sans:'Source Sans 3','Source Sans Pro',Arial,sans-serif;--tech:'Source Sans 3','Source Sans Pro',sans-serif;}}
/* Elementor-Kit faerbt Ueberschriften und Absaetze -> doppelte Klasse gewinnt */
{SC}{SC} :is(h1,h2){{color:#f1ecdd;}}
{SC}{SC} h3{{color:#f1ecdd;}}
{SC}{SC} p,{SC}{SC} li,{SC}{SC} summary{{font-family:var(--sans);}}
/* Hero-Visual ist ein Foto, keine freigestellte Figur */
{SC} .figwrap img{{border-radius:24px;aspect-ratio:4/5;object-fit:cover;object-position:50% 20%;width:100%;}}
/* Vier Stationen als 2x2 statt 3 Spalten */
{SC} .pgrid.zwei{{grid-template-columns:1fr 1fr;max-width:900px;}}
@media(max-width:620px){{ {SC} .pgrid.zwei{{grid-template-columns:1fr;}} }}
/* Stat-Werte mit Einheit etwas kleiner, damit „18 Std.“ in eine Zeile passt */
{SC} .stat .v{{font-size:clamp(30px,5vw,44px);white-space:nowrap;}}
/* Fuer-wen: Nachsatz */
{SC} .persona .nicht{{margin:22px 0 0;color:var(--muted);font-size:14.5px;border-top:1px solid var(--line);padding-top:16px;}}
/* Liste im Ueber-mich-Block */
{SC} .inliste{{margin:0 0 14px;padding-left:20px;color:var(--muted);font-size:16px;}}
{SC} .inliste li{{margin-bottom:6px;}}
{SC} .inliste b{{color:#f1ecdd;}}
/* Anmeldung: Preis-Wort statt Zahl, Formular-Karte mit AC-iframe */
{SC} .pcard .pv{{font-size:clamp(40px,7vw,56px);}}
{SC} .pcard .pfine{{color:var(--muted);font-size:13.5px;margin:0;}}
{SC} .formkarte iframe{{width:100%;min-height:840px;border:0;border-radius:14px;background:#fff;margin-top:6px;}}
"""
(OUT / "ki-masterclass.css").write_text("/* === KI-MASTERCLASS-ANMELDESEITE (auto) === */\n" + scoped + ANPASSUNG, encoding="utf-8")

HAKEN = '<svg width="13" height="10" viewBox="0 0 14 11"><path d="M1 5.5L5 9.5L13 1" stroke="#0c1c30" stroke-width="2.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>'
HAKEN_KLEIN = HAKEN.replace('width="13" height="10"', 'width="11" height="9"')

inhalt = (OUT / "ki-masterclass-inhalt.html").read_text(encoding="utf-8")
def fuellen(html, hero, about):
    html = re.sub(r"<!--.*?-->\s*", "", html, count=1, flags=re.S)
    for k, v in (("{{FORMULAR}}", FORMULAR), ("{{BILD_HERO}}", hero), ("{{BILD_ABOUT}}", about),
                 ("{{HAKEN_KLEIN}}", HAKEN_KLEIN), ("{{HAKEN}}", HAKEN)):
        html = html.replace(k, v)
    rest = re.findall(r"\{\{[A-Z_]+\}\}", html)
    assert not rest, rest
    return nachher(html) if PHASE == "nachher" else html

# 🔁 Ab Do 8.10. 09:00: KM_PHASE=nachher — Formular 69 raus (sonst bekommt eine Neuanmeldung alle
# vergangenen Mails der Automation 84 auf einmal), Weg zur Aufzeichnung über den Stimm-Check
# (Automation 83, Zweig „ab 8.10.“: S1b sofort, S2b mit der Aufzeichnung am nächsten Tag).
import os
PHASE = os.environ.get("KM_PHASE", "vorher")
ANMELDEN_NACHHER = """<section id="anmelden" style="background:var(--bg2);">
  <div class="wrap">
    <p class="eyebrow">Die Masterclass war am 8. Oktober</p>
    <h2 class="disp">Hol dir die <span class="gold">Aufzeichnung</span></h2>
    <p class="lead" style="margin:20px auto 0;max-width:720px;">Die Aufzeichnung bekommst du per Mail, wenn du dir den kostenlosen Stimm-Check holst. In rund 15 Minuten weiss deine KI, wie du klingst, und am nächsten Tag kommt die Masterclass in dein Postfach.</p>
    <div class="btnrow"><a href="https://mumlifebalance.ch/stimm-check/" class="btn">&rarr; Stimm-Check und Aufzeichnung holen</a><a href="https://mumlifebalance.ch/ki-kurs/" class="btn ghost">Direkt zum Kurs</a></div>
  </div>
</section>"""
def nachher(html):
    paare = [
        ('Kostenlose Live-Masterclass &middot; Do 8. Oktober &middot; 9 Uhr', 'Die Masterclass als Aufzeichnung'),
        ('Am Donnerstagmorgen zeige ich dir live, was sonst noch alles geht', 'In meiner Masterclass zeige ich dir, was sonst noch alles geht'),
        ('Du schaust einfach zu und gehst mit einer Idee raus', 'Du schaust einfach zu, wann es dir passt, und gehst mit einer Idee raus'),
        ('45 Minuten über Zoom</span>', 'rund 45 Minuten</span>'),
        ('Aufzeichnung am selben Tag</span>', 'per Mail, zusammen mit dem Stimm-Check</span>'),
        ('Am Donnerstag zeige ich dir, wie sie für mich arbeiten.', 'In der Aufzeichnung siehst du, wie sie für mich arbeiten.'),
        ('und genau das zeige ich dir am Donnerstag.', 'und genau das zeige ich dir in der Masterclass.'),
        ('Am Donnerstag siehst du, wie so etwas entsteht', 'In der Masterclass siehst du, wie so etwas entsteht'),
        ('Was du am Donnerstag siehst', 'Was du in der Aufzeichnung siehst'),
        ('am Donnerstag zeige ich dir nichts, was ich nicht selbst jeden Tag benutze.', 'in der Masterclass zeige ich dir nichts, was ich nicht selbst jeden Tag benutze.'),
        ('Am Donnerstag wird nichts programmiert.', 'In der Masterclass wird nichts programmiert.'),
        ('Bevor du dich anmeldest, <span class="gold">kurz&nbsp;geklärt</span>', 'Fragen, <span class="gold">kurz&nbsp;geklärt</span>'),
        ('Komm gern. Den Kurs, den ich am Ende vorstelle', 'Schau sie dir gern an. Den Kurs, den ich am Ende vorstelle'),
        ('Am Donnerstag siehst du es live.', 'In der Aufzeichnung siehst du es selbst.'),
    ]
    for a, b in paare:
        assert html.count(a) >= 1, a[:60]
        html = html.replace(a, b)
    html = re.sub(r'\s*<details><summary>Ich kann am Donnerstag nicht\..*?</details>', '', html, count=1, flags=re.S)
    html = html.replace('&rarr; Ich bin am Donnerstag dabei', '&rarr; Zur Aufzeichnung').replace('&rarr; Platz sichern', '&rarr; Zur Aufzeichnung')
    html = html.replace('class="cta">Platz sichern</a>', 'class="cta">Zur Aufzeichnung</a>')
    html, n = re.subn(r'<section id="anmelden".*?</section>', ANMELDEN_NACHHER, html, count=1, flags=re.S)
    assert n == 1
    assert "activehosted.com/f/69" not in html and "Donnerstag" not in re.sub(r"<[^>]+>", " ", html), "Rest vom Vorher"
    return html

if medien.get("km-hero.jpg") and medien.get("km-about.jpg"):
    (OUT / "ki-masterclass-wp.html").write_text(fuellen(inhalt, medien["km-hero.jpg"], medien["km-about.jpg"]), encoding="utf-8")
else:
    print("⚠ Bilder noch nicht hochgeladen — ki-masterclass-wp.html nicht gebaut")

fonts = re.search(r'<link href="https://fonts.googleapis.com[^>]+>', ref).group(0)
(OUT / "index.html").write_text(
    f'<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
    f'<title>KI-Masterclass · Vorschau</title>{fonts}<style>body{{margin:0}}\n{(OUT / "ki-masterclass.css").read_text(encoding="utf-8")}</style></head>'
    f'<body>{fuellen(inhalt, "assets/km-hero.jpg", "assets/km-about.jpg")}</body></html>', encoding="utf-8")

# Sprachpruefung auf dem sichtbaren Text
text = re.sub(r"<[^>]+>", " ", re.sub(r"<!--.*?-->", "", inhalt, flags=re.S))
muster = (r"ß", r"[Ss]tell dir[^.!?]{0,60}vor", r"\bsondern\b", r"Kund:innen", r"[Nn]icht[^.!?]{0,80}[,.]\s*[Ss]ondern",
          r"deine Kundin", r"\b(?:ae|oe|ue)\w*", r"Hier ist")
funde = [m for m in muster if re.search(m, text)]
print("CSS", len(scoped), "Zeichen · index.html gebaut · Sprachpruefung:", "sauber" if not funde else funde)
