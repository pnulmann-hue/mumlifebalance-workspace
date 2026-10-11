"""Macht aus der Notion-Aufgabenliste die Aufgaben im Cockpit.

Die Notion-Datenbank hat **21 Felder**, von denen fuenf tragen: Aufgabe, Datum,
Status, Prioritaet, Anmerkung. Der Rest sind Verknuepfungen auf andere Notion-
Datenbanken, die beim Umzug ohnehin verschwinden.

    python scripts/cockpit/aufgaben-bauen.py
    # danach: ArtifactData set -> daten/aufgaben

🚨 **Das Feld „Überfällig?" wird NICHT uebernommen.** Es ist in Notion eine
Formel, und die API liefert dafuer nur eine unlesbare `formulaResult://…`-Kennung
— fuer jede Zeile eine andere. Ueberfaellig wird hier aus Datum und heute
gerechnet; das ist ohnehin ehrlicher, weil es sich jeden Tag von selbst
aktualisiert.

🚨 **Der Bot-Rueckkanal legt weiter in Notion ab.** Er laeuft auf Railway und
kommt nicht an die Artifact-Datenbank — das aendert kein Schluessel. Notion
bleibt deshalb sein **Eingangskorb**, nicht die Aufgabenliste: der taegliche
Abgleich holt neue Eintraege hier herueber, gepflegt wird im Cockpit.

🚨 **Nur die 100 neuesten.** Die Notion-API gibt im Zeilen-Modus hoechstens 100
Zeilen und keinen Cursor. Abgedeckt ist 2026-06-09 bis 2027-01-01; aeltere
offene Aufgaben fehlen. Wenn welche auftauchen, gehoeren sie von Hand nach.
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

# Notion-Prioritaet -> was im Cockpit steht.
PRIO = {"Prio 1": "Hoch", "Prio 2": "Mittel", "Prio 3": "Tief",
        "Quick Win": "Quick Win"}


def main():
    ziel = Path(sys.argv[1]) if len(sys.argv) > 1 else \
        ROOT / "outputs" / "cockpit" / "abgleich"
    ziel.mkdir(parents=True, exist_ok=True)

    p = ziel / "aufgaben-roh.json"
    if not p.exists():
        sys.exit("aufgaben-roh.json fehlt — die holt Claude aus Notion.")
    roh = json.loads(p.read_text(encoding="utf-8"))

    heute = date.today().isoformat()
    offen, erledigt = [], 0

    for i, x in enumerate(roh.get("results") or []):
        titel = (x.get("Aufgabe") or "").strip()
        if not titel:
            continue
        status = x.get("Status") or ""
        if status == "Abgeschlossen":
            erledigt += 1
            continue
        wann = (x.get("date:Datum:start") or "")[:10]
        offen.append({
            "id": "af%03d" % i,
            "aufgabe": titel[:160],
            "datum": wann,
            "status": status or "Geplant",
            "prio": PRIO.get(x.get("Priorität") or "", "Mittel"),
            # 🚨 Selbst gerechnet, nicht aus Notion — siehe Kopf.
            "ueberfaellig": bool(wann and wann < heute),
            "notiz": (x.get("Anmerkung") or "")[:600],
            "quelle": "Notion",
        })

    offen.sort(key=lambda a: (not a["ueberfaellig"], a["datum"] or "9999"))

    ueber = [a for a in offen if a["ueberfaellig"]]
    nach_prio = {}
    for a in offen:
        nach_prio[a["prio"]] = nach_prio.get(a["prio"], 0) + 1

    daten = {
        "items": offen,
        "stand": heute,
        "erledigt_uebersprungen": erledigt,
        "ueberfaellig": len(ueber),
        "nach_prio": nach_prio,
        "quelle": roh.get("_hinweis", ""),
        "hinweis": "Gepflegt wird hier. Notion ist nur noch der Eingangskorb "
                   "des Telegram-Bots — der kommt nicht an diese Datenbank.",
        "gebaut": datetime.now().isoformat(timespec="seconds"),
    }

    (ziel / "aufgaben.json").write_text(
        json.dumps(daten, ensure_ascii=False, indent=2), encoding="utf-8")

    print("  %d offene Aufgaben (%d abgeschlossene übersprungen)"
          % (len(offen), erledigt))
    print("  %d überfällig" % len(ueber))
    print("  %s" % " · ".join("%s %d" % kv for kv in sorted(nach_prio.items())))
    print()
    print("  Am längsten überfällig:")
    for a in ueber[:6]:
        print("    %s  %-9s %s" % (a["datum"], a["prio"], a["aufgabe"][:58]))
    print("\nAbgelegt in: %s" % (ziel / "aufgaben.json"))


if __name__ == "__main__":
    main()
