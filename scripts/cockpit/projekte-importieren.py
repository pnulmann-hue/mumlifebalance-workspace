"""Holt die Notion-Datenbank «Projekte» einmalig ins Cockpit.

24 Projekte mit Zeitraum, Status und den Aufgaben, die daran hängen.

🚨 **Einmal-Umzug, kein Abgleich.** Ab hier gehört `daten/projekte` Patricia.
Der tägliche `cockpit-daten-abgleich` darf es **nie** mit `set` überschreiben —
dieselbe Regel wie bei `daten/ideenkasten`, `daten/jahresplan` und
`daten/aufgaben`.

🚨 **Nur 2 von 24 Projekten stehen auch im Jahresplan.** Das wurde vorher
geprüft, weil ein Projekte-Block sonst eine zweite Ansicht auf dieselben Daten
gewesen wäre — genau der Fehler, der den Tagesplan am 19.09. gekostet hat. Die
beiden Doppelten sind „Rauhnächte Familienreise" und die Masterclass; sie
bleiben in beiden, weil der Jahresplan die Zeitachse zeigt und der
Projekte-Block die Aufgaben dahinter.

🚨 **Das Feld «Status» ist in Notion ein E-Mail-Feld.** Irgendwann wurde der
Typ verstellt, und seitdem ist es ein freies Textfeld: es stehen „Idee",
„Aktiv", „abgeschlossen", einmal `"Idee"` **mit Anführungszeichen** und
elfmal gar nichts drin. Deshalb wird hier normalisiert statt übernommen — und
leer heisst **nicht** „erledigt", sondern „nie gesetzt".

    python scripts/cockpit/projekte-importieren.py [zielordner]
    # danach: ArtifactData set -> Sammlung "daten", Dokument "projekte"
"""

import json
import sys
from datetime import date, datetime
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]

# Notion-Wert -> Cockpit-Zustand. Siehe Kopf: der Wert kommt aus einem
# E-Mail-Feld und ist deshalb unsauber.
ZUSTAND = {
    "idee": "Idee",
    "aktiv": "Läuft",
    "abgeschlossen": "Fertig",
    "": "Ohne Status",
}


def zustand(roh):
    # Anführungszeichen und Leerraum weg — «"Idee"» ist dasselbe wie «Idee».
    s = (roh or "").strip().strip('"').strip().lower()
    return ZUSTAND.get(s, roh.strip() or "Ohne Status")


def main():
    ziel = Path(sys.argv[1]) if len(sys.argv) > 1 else \
        ROOT / "outputs" / "cockpit" / "abgleich"
    roh_datei = ziel / "projekte-roh.json"
    if not roh_datei.exists():
        sys.exit("projekte-roh.json fehlt — die holt Claude aus Notion.")
    roh = json.loads(roh_datei.read_text(encoding="utf-8"))

    heute = date.today().isoformat()
    liste = []
    for i, p in enumerate(roh.get("projekte") or []):
        von, bis = p.get("von") or "", p.get("bis") or ""
        liste.append({
            "id": "pr%03d" % i,
            "name": p["name"],
            "zustand": zustand(p.get("status")),
            "prio": p.get("prio") or "",
            "typ": p.get("typ") or "",
            "von": von,
            "bis": bis,
            "aufgaben": p.get("aufgaben") or 0,
            "ziele": p.get("ziele") or 0,
            "produkt": p.get("produkt") or 0,
            "laeuft": bool(von and bis and von <= heute <= bis),
            "vorbei": bool(bis and bis < heute),
        })

    # Laufende zuerst, dann kommende, dann Vergangenes — rückwärts.
    def rang(x):
        return (0 if x["laeuft"] else (1 if not x["vorbei"] else 2),
                x["von"] if not x["vorbei"] else "")
    liste.sort(key=lambda x: (rang(x)[0], rang(x)[1] or "9999"))

    laeuft = [x for x in liste if x["laeuft"]]
    kommt = [x for x in liste if not x["laeuft"] and not x["vorbei"]]
    vorbei = [x for x in liste if x["vorbei"]]
    ohne_status = [x for x in liste if x["zustand"] == "Ohne Status"]

    daten = {
        "items": liste,
        "stand": heute,
        "laeuft": len(laeuft),
        "kommt": len(kommt),
        "vorbei": len(vorbei),
        "quelle": "Notion «Projekte», einmalig übernommen am 2026-09-24 — "
                  "gepflegt wird ab hier hier",
        "hinweis": ("«Ohne Status» heisst: in Notion stand nichts drin, nicht "
                    "dass es erledigt wäre. Das Feld war dort ein E-Mail-Feld "
                    "und liess jeden Text zu."),
        "gebaut": datetime.now().isoformat(timespec="seconds"),
    }

    (ziel / "projekte.json").write_text(
        json.dumps(daten, ensure_ascii=False, indent=2), encoding="utf-8")

    print("  %d Projekte · %d laufen · %d kommen · %d vorbei"
          % (len(liste), len(laeuft), len(kommt), len(vorbei)))
    print()
    for x in liste:
        marke = "▶" if x["laeuft"] else ("·" if not x["vorbei"] else " ")
        print("  %s %-56s %-12s %s%s"
              % (marke, x["name"][:56], x["zustand"],
                 "%s→%s" % (x["von"][2:], x["bis"][2:]) if x["von"] else "",
                 "  %d Aufgaben" % x["aufgaben"] if x["aufgaben"] else ""))
    if ohne_status:
        print()
        print("  ⚠️ %d Projekte ohne Status — in Notion war das Feld leer."
              % len(ohne_status))
    print("\nAbgelegt in: %s" % (ziel / "projekte.json"))


if __name__ == "__main__":
    main()
