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

import os
PHASE = os.environ.get("KI_PHASE", "regulaer")   # 🔁 seit 16.10.2026 regulaer · ab Sa 24.10.2026 „zu“ (KI_PHASE=zu)
KASSE = "https://mumlifebalance.thrivecart.com/ki-network/"   # ThriveCart-Kasse (seit 26.09.)
MBA_WEG = "https://mumlifebalance.ch/mba-webinar-replay/"     # Phase „zu“: Weg zur MBA über das Webinar
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
    "2 Live-Calls am 18. November und am 10. Dezember, beide werden aufgezeichnet",
]
if PHASE == "offen":   # ab 30.11.2026 ohne Daten (Patricia 23.10.)
    LEISTUNGEN[0] = "10 Kapitel mit über 60 Lektionen, alle sofort offen"
    LEISTUNGEN[4] = "2 Live-Calls, beide aufgezeichnet, damit du sie schauen kannst, wann es dir passt"
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
        karte(False, "", "Ratenzahlung", "Den Betrag aufteilen", RATEN or "in Raten",
              "gleicher Kurs, gleiche Begleitung" if RATEN else "aufgeteilt in Raten, die Aufteilung siehst du an der Kasse",
              "Mit Raten starten", ghost=True),
    ]) + "\n    </div>"
elif PHASE == "offen":
    # Ab Mo 30.11.2026: Kurs komplett, Kasse wieder offen (Patricia 23.10.: 333, auch in 2 Raten).
    # 2 × 166.50 steht so an der Kasse ki-network (geprüft 23.10.2026).
    RATEN = "2 × 166.50 CHF"
    PREISBLOCK = '    <div class="price2">\n' + "\n".join([
        karte(True, "Einmal zahlen", "Einmalzahlung", "Einmal zahlen, und alles gehört dir", "333 CHF", "einmalig", "Platz sichern"),
        karte(False, "", "Ratenzahlung", "Den Betrag in zwei Raten aufteilen", RATEN, "gleicher Kurs, gleiche Begleitung",
              "Mit Raten starten", ghost=True),
    ]) + "\n    </div>"
elif PHASE == "zu":
    # Ab Sa 24.10.2026: Kasse zu, bis der Kurs komplett ist. Der Weg führt zur MBA, in der Easy KI
    # schon dabei ist — über das Webinar, nie direkt auf die MBA-Kasse (Preis-Integrität 997/1347).
    PREISBLOCK = f"""    <div class="price2">
      <div class="pcard best">
        <div class="tag">Kasse gerade zu</div>
        <div class="pn">Easy KI für Networkerinnen</div>
        <div class="ps">In der Mum Business Academy ist der Kurs schon dabei</div>
        <div class="pv">333 CHF</div>
        <div class="pvs">sobald die Kasse wieder offen ist</div>
        <ul>
{liste()}
        </ul>
        <a href="{MBA_WEG}" class="btn">Mehr über die Mum Business Academy</a>
      </div>
    </div>"""
else:
    sys.exit("PHASE muss frueh, regulaer oder zu sein")

KASSE_SATZ = {
    "frueh": "Die Kasse ist bis Freitag, 23. Oktober, offen. Danach mache ich sie erst wieder auf, wenn der Kurs komplett ist.",
    "regulaer": "Die Kasse ist bis Freitag, 23. Oktober, offen. Danach mache ich sie erst wieder auf, wenn der Kurs komplett ist.",
    "zu": "Die Kasse ist gerade zu, weil ich jetzt mit der ersten Runde durch die zehn Kapitel gehe. Sobald der Kurs komplett ist, mache ich sie wieder auf.",
    "offen": "Der Kurs ist komplett, alle zehn Kapitel sind offen, und du kannst sofort loslegen.",
}[PHASE]

# Phase „offen“: Die Seite wurde für die erste Runde mit Startdaten geschrieben (Kapitel Woche für Woche,
# Live-Calls am 18.11. und 10.12.). Ab der Wiedereröffnung ist das Vergangenheit — Patricia: „ob bei keiner
# seite noch irgend ein datum steht“. Jede Stelle wird genau einmal ersetzt, sonst bricht der Bau ab.
OFFEN_TEXTE = [
    ("Start am 1. November", "Sofort alle Kapitel offen"),
    ("Kapitel, die Woche für Woche aufgehen, damit du Schritt für Schritt mitkommst",
     "Kapitel, die aufeinander aufbauen, damit du Schritt für Schritt mitkommst"),
    ("Die Kapitel gehen nacheinander auf. So kommst du in deinem Tempo durch, und niemand springt ans Ende, bevor der Arbeitsplatz steht.",
     "Alle zehn Kapitel sind offen, sobald du drin bist. Du gehst sie der Reihe nach durch, in deinem Tempo, und so steht dein Arbeitsplatz, bevor die festen Aufträge kommen."),
    ("<b>So 1. November:</b> Kapitel 1 bis 3,", "<b>Kapitel 1 bis 3:</b>"),
    ("<b>Mo 9. November:</b> Kapitel 4 und 5,", "<b>Kapitel 4 und 5:</b>"),
    ("<b>Mo 16. November:</b> Kapitel 6 und 7,", "<b>Kapitel 6 und 7:</b>"),
    ("<b>Mi 18. November, abends:</b> erster Live-Call, zu Arbeitsplatz und erstem festen Auftrag — wird aufgezeichnet",
     "<b>Zwei Live-Calls:</b> zu Arbeitsplatz, festen Aufträgen und allen Fragen zum ganzen Kurs, beide aufgezeichnet"),
    ("<b>Mo 23. November:</b> Kapitel 8 und 9,", "<b>Kapitel 8 und 9:</b>"),
    ("<b>Mo 30. November:</b> Kapitel 10, und der Kurs ist komplett", "<b>Kapitel 10:</b> Sicherheit und das Ganze"),
    ('      <div class="b"><span class="c">{{HAKEN}}</span><div><b>Do 10. Dezember, abends:</b> zweiter Live-Call, für alle Fragen zum ganzen Kurs — wird aufgezeichnet</div></div>\n', ""),
    ("<summary>Warum geht nicht alles auf einmal auf?</summary><div class=\"a\">Damit du Schritt für Schritt mitkommst. Jedes Kapitel baut auf dem vorherigen auf, und wer den Arbeitsplatz überspringt, hängt später bei den festen Aufträgen fest. Ab dem 30. November ist alles offen, und dann gehst du in deinem Tempo weiter.</div>",
     "<summary>Muss ich alles auf einmal machen?</summary><div class=\"a\">Nein. Alle Kapitel sind offen, aber sie bauen aufeinander auf. Geh sie der Reihe nach durch, denn wer den Arbeitsplatz überspringt, hängt später bei den festen Aufträgen fest.</div>"),
    ("Dazu kommen die zwei Live-Calls am 18. November und am 10. Dezember. Beide werden aufgezeichnet, du kannst sie also auch später schauen — schick deine Frage vorher in die Gruppe, dann beantworte ich sie im Call.",
     "Dazu kommen die zwei Live-Calls, beide aufgezeichnet, damit du sie schauen kannst, wann es dir passt."),
    ("Dann hast du den Kurs schon. Er kommt ab dem 1. November in deinen Bereich, ohne dass du etwas zahlst.",
     "Dann hast du den Kurs schon. Er liegt in deinem Bereich, ohne dass du etwas zahlst."),
    ("Nein, du hast ihn schon. Er kommt ab dem 1. November in deinen Bereich.", "Nein, du hast ihn schon. Er liegt in deinem Bereich."),
]

def offen_umbauen(html):
    for alt, neu in OFFEN_TEXTE:
        n = html.count(alt)
        assert n == 1, f"Phase offen: Stelle {n}× gefunden — {alt[:60]!r}"
        html = html.replace(alt, neu)
    html, n = re.subn(r' <span class="neu">ab \d{1,2}\.1[01]\.</span>', "", html)
    assert n == 10, f"Phase offen: {n} Kapitel-Daten statt 10"
    rest = re.findall(r"\d{1,2}\. ?(?:Oktober|November|Dezember)|\b\d{1,2}\.1[0-2]\.", re.sub(r"<[^>]+>", " ", html + PREISBLOCK))
    assert not rest, f"Phase offen: Datum übrig {rest}"
    return html

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
    if PHASE == "offen":
        html = offen_umbauen(html)
    for k, v in (("{{PREISBLOCK}}", PREISBLOCK), ("{{KASSE_SATZ}}", KASSE_SATZ), ("{{KASSE}}", KASSE),("{{BILD_HERO}}", hero), ("{{BILD_ABOUT}}", about),
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
