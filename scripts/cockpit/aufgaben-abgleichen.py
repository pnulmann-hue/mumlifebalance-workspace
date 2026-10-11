"""Gleicht die Notion-Aufgaben gegen den Workspace ab.

Patricia am 24.09.2026: *„gleich doch ab mit deinem workspace, was noch
aktuell ist. hab ja alles mit dir erstellt"* — und sie hat recht: von 37
ueberfaelligen Aufgaben waren viele laengst erledigt, nur nie in Notion
abgehakt. Eine Liste, in der die Haelfte falsch ist, liest nach kurzer Zeit
niemand mehr.

🚨 **Nichts wird automatisch abgehakt.** Jeder Eintrag bekommt einen
**Beleg** — eine Datei, eine Zeile in CLAUDE.md, ein Verzeichnis — und im
Cockpit steht „sieht erledigt aus" mit genau diesem Beleg daneben. Bestaetigen
tut Patricia. Ein Haken, den eine Maschine gesetzt hat, ist derselbe Fehler wie
ein Haken, der fehlt: In beiden Faellen stimmt die Liste nicht mehr mit der
Wirklichkeit ueberein, und man merkt es erst, wenn es zu spaet ist.

🚨 **Drei Zustaende, nicht zwei.** Neben „belegt erledigt" gibt es
**„hinfaellig"**: Aufgaben, die keinen Sinn mehr ergeben, weil die
Entscheidung dahinter gekippt ist. Die gehoeren nicht abgehakt (sie wurden
nicht erledigt) und nicht stehengelassen (sie kommen nie dran).

    python scripts/cockpit/aufgaben-abgleichen.py
"""

import json
import sys
from datetime import datetime
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]

# Stichwort im Aufgabentitel -> (zustand, beleg)
# zustand: "erledigt" | "hinfaellig" | "teilweise"
# Recherchiert am 24.09.2026. Jeder Beleg ist nachpruefbar.
BEFUNDE = [
    ("Startklar 1/6", "erledigt",
     "Die Videos liegen in OneDrive (Startklar 1.1.mp4 …). CLAUDE.md: "
     "«Der Kurs ist aufgenommen (18.09.2026) — 13 Videos, 80 Minuten»."),
    ("Startklar 2/6", "erledigt",
     "Dieselbe Aufnahme-Session, 18.09.2026 — 13 Videos für alle Module."),
    ("Startklar 3/6", "erledigt",
     "Dieselbe Aufnahme-Session, 18.09.2026."),
    ("Startklar 4/6", "hinfaellig",
     "Die Aufgabe nennt ThriveCart Academy als Ziel. Am 15.09.2026 verworfen — "
     "die Plattform ist wieder offen (Memory «MBA NICHT auf ThriveCart "
     "Academy»). Neu entscheiden, nicht abhaken."),
    ("Startklar 6/6", "erledigt",
     "Acht Mail-Dateien in outputs/produkte/instagram-startklar/08-funnel/, "
     "gebaut mit mails-bauen.py am 18.09.2026."),
    ("Werkstatt: Prüfdienst", "erledigt",
     "CLAUDE.md: «Die Werkstatt ist live: https://startklar.mumlifebalance.ch "
     "(geprueft 17.09.2026)»."),
    ("Zugangscodes", "erledigt",
     "Sammelcode STARTKLAR_KUNDE, Patricias Entscheid 18.09.2026. "
     "🚨 Anders als in der Aufgabe geplant: NICHT über die Kauf-Mail, "
     "sondern im Kurs in der Lektion «Deine Werkstatt»."),
    ("KV-Speicher", "offen",
     "CLAUDE.md bestätigt das Gegenteil: «Es gibt aktuell KEINE Obergrenze.» "
     "Vor einem grösseren Launch fällig."),
    ("Schnitt-Regeln bestätigen", "erledigt",
     "context/videoschnitt-regeln.md existiert (7.8 KB, zuletzt 20.09.2026) "
     "und ist laut CLAUDE.md die SSOT der Pipeline."),
    ("erstes echtes Reel durch die Pipeline", "erledigt",
     "video/output/ enthält fertige Reels (2026-09-10-kw38-…). CLAUDE.md: "
     "«Getestet 2026-09-10: kompletter Durchlauf bis 1080×1920-MP4»."),
    ("Freistellen testen", "erledigt",
     "Ist fester Bestandteil der Textebene — CLAUDE.md nennt "
     "«npx hyperframes remove-background» als Pflichtschritt für das "
     "grosse Wort hinter Patricia."),
    ("welcher Skill als erster weitergegeben", "erledigt",
     ".claude/skills/_WEITERGABE-STATUS.md existiert mit Einstufung je Skill "
     "(«🟢 Kann fast so wie er ist weitergegeben werden»)."),
    ("Bewusstseinsstufen und Angles", "erledigt",
     "Im Hook-Skill enthalten (CLAUDE.md: «Bewusstseinsstufen 1–5 · Angles»), "
     "und der ist Pflichtlektüre in allen 14 Content-Skills."),
    ("Backoffice-Check", "erledigt",
     "doTERRA Rang-Tracker läuft seit 11.09.2026 aus dem Schlagdistanz-Bericht "
     "— der Stand steht im Cockpit unter doTERRA."),
    ("Notion-Eintrag in der Produkte-DB", "hinfaellig",
     "Notion wird abgelöst. Der Angebots-Katalog im Cockpit kommt direkt "
     "aus ThriveCart."),
    ("Sommerimpulse FB Gruppe", "hinfaellig",
     "Termin war der 22.06.2026, der Sommer ist vorbei. Falls das jährlich "
     "wiederkehrt, gehört es in den Jahresplan statt in eine Aufgabe."),
    ("Testimonial-Blöcke", "teilweise",
     "Vier freigegebene Kundenstimmen stehen seit 24.09. im Cockpit unter "
     "«Kundinnen & Leads» — zum Einsetzen bereit."),
    # Die Immun-Themenwoche lief vom 14. bis 18.09.2026 — Patricia am 24.09.:
    # „doch immunwoche ist ja auch längst durch". 🚨 Der Beleg steckt in den
    # **Zeitstempeln**: Tag 1 als PDF vom 14.09., Tag 2 bis 5 vom 18.09. — also
    # jeweils an dem Tag, an dem sie liefen. Dazu fünf Sprechtexte auf Mundart
    # (die spricht man, man schreibt sie nicht zum Spass) und ein
    # Teilnehmer-Zettel vom 14.09.
    ("Themenwoche vorbereiten", "erledigt",
     "Fünf PDFs, fünf Mundart-Sprechtexte und der Teilnehmer-Zettel liegen in "
     "outputs/freebies/immunwoche-2026-09/ — Tag 1 vom 14.09., der Rest bis "
     "zum 18.09."),
    ("Themenwoche Tag 1", "erledigt",
     "Immunsystem-und-dein-Teller.pdf, erstellt am 14.09.2026 — dem Tag, an "
     "dem Tag 1 dran war."),
    ("Themenwoche Tag 2", "erledigt",
     "Immunwoche-Tag2-Schlaf.pdf plus tag2.html und Mundart-Sprechtext."),
    ("Themenwoche Tag 3", "erledigt",
     "Immunwoche-Tag3-Bewegung-und-frische-Luft.pdf plus tag3.html."),
    ("Themenwoche Tag 4", "erledigt",
     "Immunwoche-Tag4-Die-Rituale-und-die-Öle.pdf plus tag4.html."),
    ("Themenwoche Tag 5", "erledigt",
     "Immunwoche-Tag5-Wenn-es-doch-mal-kommt.pdf plus tag5.html, vom "
     "18.09.2026 — dem Tag des Pitches."),
    # 🚨 Zwei aus derselben Woche bleiben OFFEN, weil ich dafuer keinen Beleg
    # habe. Sie mit abzuhaken, nur weil sie danebenstehen, waere geraten.
    ("Keyword „Immun", "offen",
     "Kein Beleg im Workspace. Die Woche kann auch nur über die "
     "Telegram-Gruppe gelaufen sein. Siehe die Regel, dass eine "
     "Keyword-Tabelle kein Nachweis ist — im ManyChat nachsehen."),
    ("Startgespräche führen", "offen",
     "Das ist die Nachbereitung nach dem Pitch am 18.09. Ob die Gespräche "
     "gelaufen sind, steht nirgends im Workspace."),
]


def main():
    ziel = Path(sys.argv[1]) if len(sys.argv) > 1 else \
        ROOT / "outputs" / "cockpit" / "abgleich"
    p = ziel / "aufgaben.json"
    if not p.exists():
        sys.exit("aufgaben.json fehlt — erst aufgaben-bauen.py.")
    d = json.loads(p.read_text(encoding="utf-8"))

    from datetime import date
    heute = date.today().isoformat()

    treffer = {"erledigt": 0, "hinfaellig": 0, "teilweise": 0, "offen": 0}
    for a in d.get("items") or []:
        titel = a.get("aufgabe") or ""
        # 🚨 **Wiederkehrende Aufgaben stehen mehrfach in der Liste.**
        # „doTERRA: Backoffice-Check" gibt es zum 20.09. UND zum 20.10., „Mums
        # Bestellung" zum 10.09. und 10.10. Ein Stichwort-Treffer haette die
        # Oktober-Runde als erledigt markiert — und dann faellt sie aus, weil
        # sie ja angeblich schon gemacht wurde. Ein Befund gilt nur fuer
        # Termine, die bereits vorbei sind.
        if (a.get("datum") or "9999") > heute:
            continue
        for stichwort, zustand, beleg in BEFUNDE:
            if stichwort.lower() in titel.lower():
                a["befund"] = zustand
                a["beleg"] = beleg
                treffer[zustand] = treffer.get(zustand, 0) + 1
                break

    d["abgeglichen"] = datetime.now().isoformat(timespec="seconds")
    d["befund_hinweis"] = ("Abgeglichen gegen den Workspace. Nichts ist "
                           "automatisch abgehakt — der Beleg steht daneben, "
                           "bestätigen musst du.")
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")

    ohne = [a for a in d["items"] if not a.get("befund") and not a.get("erledigt")]
    print("  %d sehen erledigt aus (mit Beleg)" % treffer["erledigt"])
    print("  %d sind hinfällig — Entscheidung dahinter ist gekippt" % treffer["hinfaellig"])
    print("  %d teilweise erledigt" % treffer["teilweise"])
    print("  %d bestätigt offen" % treffer["offen"])
    print("  %d ohne Befund — die musst du selbst anschauen" % len(ohne))
    print()
    for a in d["items"]:
        if a.get("befund") in ("erledigt", "hinfaellig"):
            print("  [%-10s] %s" % (a["befund"], a["aufgabe"][:62]))
    print("\nAktualisiert: %s" % p)


if __name__ == "__main__":
    main()
