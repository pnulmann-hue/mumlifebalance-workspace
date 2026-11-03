"""Baut die Anmeldeseite „Neustart 2027 · Jahresplanungs-Workshop“ (Do 17.12.2026, 09:00) und die Danke-Seite.

Kopf und CSS kommen unverändert aus der Story-Generator-Seite (dasselbe dunkle Design wie der Tool-Workshop),
der Inhalt aus jahresplanung-body.html / jahresplanung-danke-body.html, der Neujahrs-Effekt (Kalenderblatt,
Funken) aus jahresplanung-effekt.css. Texte und Werte: outputs/produkte/jahresplanung/angebot/00-bauplan.md

    python scripts/salespage-design/jahresplanung-bauen.py
-> outputs/salespages/jahresplanung/index.html + danke.html (lokal ansehen: preview_start jahresplanung-lp)
-> …-wp.html: Inhalt für WordPress, in .sg-sp verpackt. Das Effekt-CSS gehört als eigener Block
   „NEUSTART-2027-EFFEKT“ in den Customizer (die Story-Generator-CSS liegt dort schon).
"""
import pathlib, re, sys
sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parents[2]
HIER = ROOT / "scripts/salespage-design"

# Nach dem Anlegen eintragen: AC-Formular-ID und die WP-Adresse des Hero-Bilds (webp).
FORMULAR = 76            # AC-Formular „0€ Jahresplanung“ (angelegt 01.11.2026)
BILD_WP = "https://mumlifebalance.ch/wp-content/uploads/2026/11/neustart-2027-mockup.webp"  # WP-Medium 4468

vorlage = (ROOT / "outputs/salespages/story-generator/index.html").read_text(encoding="utf-8")
effekt = (HIER / "jahresplanung-effekt.css").read_text(encoding="utf-8")
kopf = vorlage[: vorlage.index("<!-- HERO -->")]
ende = vorlage[vorlage.index("</footer>") + len("</footer>"):]

for alt, neu in [
    ("STORY<b>&middot;</b>GENERATOR", "NEUSTART<b>&middot;</b>2027"),
    ("F&uuml;r 17 CHF / 17 &euro; holen</a>", "Ich plane mit &middot; gratis</a>"),
    ('href="#preis" class="cta"', 'href="#anmelden" class="cta"'),
]:
    assert kopf.count(alt) == 1, alt
    kopf = kopf.replace(alt, neu)
assert kopf.count("</style>") == 1
kopf = kopf.replace("</style>", effekt + "\n</style>")


def formular(lokal):
    if FORMULAR:
        return (f'<iframe src="https://mumlifebalance.activehosted.com/f/{FORMULAR}" title="Anmeldung zum Jahresplanungs-Workshop" '
                'style="width:100%;min-height:700px;border:0;border-radius:14px;margin-top:30px;background:#fff;"></iframe>')
    # Platzhalter, solange das Formular in AC noch nicht angelegt ist
    return ('<div style="max-width:560px;margin:30px auto 0;background:#fffdf8;color:#0c1c30;border-radius:18px;padding:28px;text-align:left;">'
            '<p style="font-weight:800;margin:0 0 14px;">Hier kommt das Anmeldeformular hin</p>'
            '<p style="margin:0 0 8px;">Vorname · E-Mail · Häkchen Datenschutz · Knopf „Ich plane mit“</p>'
            '<p style="margin:0;color:#5d6b78;font-size:15px;">AC-Formular „0€ Jahresplanung“, Tag „0€ Jahresplanung“, Liste Mentoring, '
            'Weiterleitung nach dem Absenden auf /neustart-2027-danke/.</p></div>')


ziel = ROOT / "outputs/salespages/jahresplanung"
ziel.mkdir(parents=True, exist_ok=True)


def bauen(body_datei, titel, name, cta_alt=None, cta_neu=None):
    k = re.sub(r"<title>.*?</title>", f"<title>{titel}</title>", kopf, count=1, flags=re.S)
    if cta_alt:
        assert k.count(cta_alt) == 1
        k = k.replace(cta_alt, cta_neu)
    inhalt = (HIER / body_datei).read_text(encoding="utf-8")
    lokal = inhalt.replace("BILD_HERO", "bild/hero.png").replace("FORMULAR_EINBETTUNG", formular(True))
    seite = k + lokal + ende
    (ziel / f"{name}.html").write_text(seite, encoding="utf-8")
    # WordPress: nur der Inhalt, in .sg-sp, ohne Stil und Skript
    wp_inhalt = inhalt.replace("BILD_HERO", BILD_WP or "BILD_HERO_FEHLT").replace("FORMULAR_EINBETTUNG", formular(False))
    body = (k + wp_inhalt + ende)
    body = body[body.index("<body>") + 6: body.index("</body>")].strip()
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    wp = f'<div class="sg-sp">\n{body}\n</div>'
    assert "<style" not in wp and "<script" not in wp
    (ziel / f"{name}-wp.html").write_text(wp, encoding="utf-8")
    print("→", ziel / f"{name}.html", "· WP", len(wp), "Zeichen")


bauen("jahresplanung-body.html", "Neustart 2027 · Jahresplanungs-Workshop", "index")
bauen("jahresplanung-danke-body.html", "Bestätige deine Anmeldung · Neustart 2027", "danke",
      'href="#anmelden" class="cta">Ich plane mit &middot; gratis</a>',
      'href="https://mumlifebalance.ch/mba/" class="cta">Die Academy ansehen</a>')
bauen("jahresplanung-bestaetigt-body.html", "Du bist dabei · Neustart 2027", "bestaetigt",
      'href="#anmelden" class="cta">Ich plane mit &middot; gratis</a>',
      'href="https://mumlifebalance.ch/mba/" class="cta">Die Academy ansehen</a>')
(ziel / "neustart-2027-effekt.css").write_text(effekt, encoding="utf-8")

# Gegenprobe: verbotene Muster im sichtbaren Text
for name in ("index.html", "danke.html", "bestaetigt.html"):
    text = re.sub(r"<[^>]+>", " ", (ziel / name).read_text(encoding="utf-8"))
    for muster in ["ß", r"[Nn]icht[^.!?]{0,80}[,.]\s*[Ss]ondern", "deine Kundin"]:
        if re.search(muster, text):
            print("⚠️", name, "enthält", muster)
if not FORMULAR:
    print("⚠️ FORMULAR fehlt noch — Platzhalter eingesetzt")
if not BILD_WP:
    print("⚠️ BILD_WP fehlt noch — WP-Fassung trägt BILD_HERO_FEHLT")
