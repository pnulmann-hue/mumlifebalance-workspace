"""Baut die Verkaufsseite des KI-Kurses „Easy KI für Networkerinnen — vom Chat zur Mitarbeiterin“.

Gleicher ki-salespage-Baukasten wie die Masterclass und DASSELBE CSS (.km-sp, liegt schon im
Customizer, gebaut von ki-masterclass-bauen.py). Hier nur Inhalt + ein paar Zusatzregeln unter
.km-sp.kurs (Datei ki-kurs.css, gehört ebenfalls in den Customizer).

    python scripts/salespage-design/ki-kurs-bauen.py
-> outputs/salespages/ki-kurs/ki-kurs-wp.html  (Seiteninhalt für WordPress)
   outputs/salespages/ki-kurs/ki-kurs.css      (Zusatz-CSS, in den Customizer)
   outputs/salespages/ki-kurs/index.html       (lokale Vorschau)

🔁 PHASE umstellen: "frueh" bis Do 15.10. (277 + 333), danach "regulaer" (333 einmalig oder in Raten).
"""
import json, pathlib, re, sys
sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "outputs/salespages/ki-kurs"
MC = ROOT / "outputs/salespages/ki-masterclass"

PHASE = "frueh"
KASSE = "https://mumlifebalance.thrivecart.com/ki-network/"   # ThriveCart-Kasse (seit 26.09.)
RATEN = ""               # 🚨 z. B. "3 × 119" — nur eintragen, was in ThriveCart genau so eingerichtet ist

MEDIEN = OUT / "medien.json"
medien = json.loads(MEDIEN.read_text(encoding="utf-8")) if MEDIEN.exists() else {}

HAKEN = '<svg width="13" height="10" viewBox="0 0 14 11"><path d="M1 5.5L5 9.5L13 1" stroke="#0c1c30" stroke-width="2.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>'
HAKEN_KLEIN = HAKEN.replace('width="13" height="10"', 'width="11" height="9"')

LEISTUNGEN = [
    "10 Kapitel mit über 60 Lektionen, Kapitel für Kapitel ab dem 1. November",
    "Vorlagen zum Mitnehmen: deine Roadmap, eine Vorlage für alles, was deine KI über dich wissen muss, und fertige Gerüste für Arbeitsplatz, Helfer und Übersichtsseite",
    "Feste Aufträge für Caption, Story, Karussell und Reel, die du mit deinem eigenen Wissen füllst",
    "Telegram-Gruppe mit Antworten jeden Dienstag und Donnerstag, sie bleibt auch nach den Calls",
    "2 Live-Calls am 19. November und am 10. Dezember, beide werden aufgezeichnet",
]
def liste():
    return "\n".join(f'          <li><span class="c">{HAKEN_KLEIN}</span>{x}</li>' for x in LEISTUNGEN)

def karte(best, tag, name, sub, preis, preis_sub, knopf, ghost=False):
    return f"""      <div class="pcard{' best' if best else ''}">
        {f'<div class="tag">{tag}</div>' if tag else ''}
        <div class="pn">{name}</div>
        <div class="ps">{sub}</div>
        <div class="pv">{preis}</div>
        <div class="pvs">{preis_sub}</div>
        <ul>
{liste()}
        </ul>
        {f'<a href="{KASSE}" class="btn' + (' ghost' if ghost else '') + f'">{knopf}</a>' if knopf else '<p class="pfine">Ab dem 16. Oktober an der Kasse, auch in Raten.</p>'}
      </div>"""

raten_text = f"oder in Raten zu {RATEN}" if RATEN else "einmalig oder in Raten, die Aufteilung siehst du an der Kasse"
if PHASE == "frueh":
    PREISBLOCK = '    <div class="price2">\n' + "\n".join([
        karte(True, "Frühbucherin · bis Do 15.10.", "Frühbucherpreis", "Für alle, die bis Donnerstag, 15. Oktober, dabei sind",
              "277 CHF", "einmalig · danach 333", "Zum Frühbucherpreis sichern"),
        karte(False, "", "Regulär", "Ab Freitag, 16. Oktober", "333 CHF", raten_text, None, ghost=True),
    ]) + "\n    </div>"
elif PHASE == "regulaer":
    PREISBLOCK = '    <div class="price2">\n' + "\n".join([
        karte(True, "Einmal zahlen", "Einmalzahlung", "Einmal zahlen, und alles gehört dir", "333 CHF", "einmalig", "Platz sichern"),
        karte(False, "", "Ratenzahlung", "Den Betrag aufteilen", RATEN or "333 CHF",
              "gleicher Kurs, gleiche Begleitung" if RATEN else "aufgeteilt in Raten, die Aufteilung siehst du an der Kasse",
              "Mit Raten starten", ghost=True),
    ]) + "\n    </div>"
else:
    sys.exit("PHASE muss frueh oder regulaer sein")

ZUSATZ = """/* === KI-KURS-VERKAUFSSEITE: Zusatz zu .km-sp (auto) === */
.km-sp.kurs .pgrid.zwei .pcard2 h3{margin-top:2px;}
.km-sp.kurs .persona + .persona{margin-top:22px;}
.km-sp.kurs .stats + .persona{margin-top:26px;}
.km-sp.kurs .mba{max-width:900px;margin:30px auto 0;background:var(--card);border:1px solid rgba(18,130,140,0.5);border-radius:18px;padding:22px 26px;}
.km-sp.kurs .mba p{margin:0 0 10px;color:var(--muted);font-size:15.5px;}
.km-sp.kurs .mba p:last-child{margin:0;}
.km-sp.kurs .mba b{color:#f1ecdd;}
"""
(OUT / "ki-kurs.css").write_text(ZUSATZ, encoding="utf-8")

inhalt = (OUT / "ki-kurs-inhalt.html").read_text(encoding="utf-8")
def fuellen(html, hero, about):
    html = re.sub(r"<!--.*?-->\s*", "", html, count=1, flags=re.S)
    for k, v in (("{{PREISBLOCK}}", PREISBLOCK), ("{{KASSE}}", KASSE), ("{{BILD_HERO}}", hero), ("{{BILD_ABOUT}}", about),
                 ("{{HAKEN_KLEIN}}", HAKEN_KLEIN), ("{{HAKEN}}", HAKEN)):
        html = html.replace(k, v)
    rest = re.findall(r"\{\{[A-Z_]+\}\}", html)
    assert not rest, rest
    return html

if medien.get("kk-hero.jpg") and medien.get("kk-about.jpg"):
    (OUT / "ki-kurs-wp.html").write_text(fuellen(inhalt, medien["kk-hero.jpg"], medien["kk-about.jpg"]), encoding="utf-8")
else:
    print("⚠ Bilder noch nicht hochgeladen — ki-kurs-wp.html nicht gebaut")

mc_css = (MC / "ki-masterclass.css").read_text(encoding="utf-8")
fonts = '<link href="https://fonts.googleapis.com/css2?family=Philosopher:ital,wght@0,400;0,700;1,400;1,700&family=Source+Sans+3:ital,wght@0,300;0,400;0,600;0,700;1,400;1,600&display=swap" rel="stylesheet">'
(OUT / "index.html").write_text(
    f'<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
    f'<title>KI-Kurs · Vorschau</title>{fonts}<style>body{{margin:0}}\n{mc_css}\n{ZUSATZ}</style></head>'
    f'<body>{fuellen(inhalt, "assets/kk-hero.jpg", "assets/kk-about.jpg")}</body></html>', encoding="utf-8")

sichtbar = re.sub(r"<[^>]+>", " ", re.sub(r"<!--.*?-->", "", inhalt + PREISBLOCK, flags=re.S))
muster = (r"ß", r"[Ss]tell dir[^.!?]{0,60}vor", r"\bsondern\b", r"Kund:innen", r"[Nn]icht[^.!?]{0,80}[,.]\s*[Ss]ondern",
          r"deine Kundin", r"Hier ist", r"\b(?:ae|oe|ue)\w*")
funde = [m for m in muster if re.search(m, sichtbar)]
print("Phase", PHASE, "· Kasse", KASSE, "· Raten", RATEN or "offen", "· Sprachpruefung:", "sauber" if not funde else funde)
