"""Holt die Notion-Ziele ins Cockpit — und stellt den Ist-Stand daneben.

🚨 **Das ist der eigentliche Punkt.** In Notion stand das Ziel „40000 Umsatz
mit Mumlifebalance" — und der tatsaechliche Umsatz stand in ThriveCart.
Zwischen beiden lag nie ein Blick, weil sie in verschiedenen Werkzeugen
wohnten. Ein Jahresziel ohne Ist-Stand daneben ist ein Wunsch, kein Ziel.

    python scripts/cockpit/ziele-bauen.py

🚨 **Nur messen, was wirklich gemessen ist.** Zwei Ziele bekommen einen
Ist-Wert: der Jahresumsatz (aus ThriveCart) und der doTERRA-Rang (aus dem
Schlagdistanz-Bericht). Alle anderen bleiben ohne Zahl — eine geschaetzte
Fortschrittsanzeige sieht in einer Tabelle genauso echt aus wie eine gemessene
und ist deshalb schlimmer als gar keine.

🚨 **Die Zeit laeuft mit.** Bei einem Jahresziel gehoert neben „wie viel ist
erreicht" die Frage „wie viel Jahr ist vorbei". 12 % vom Ziel im September
heisst etwas anderes als 12 % im Februar.
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


def lade(ordner: Path, name: str):
    p = ordner / name
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def main():
    ziel = Path(sys.argv[1]) if len(sys.argv) > 1 else \
        ROOT / "outputs" / "cockpit" / "abgleich"
    ziel.mkdir(parents=True, exist_ok=True)

    roh = lade(ziel, "ziele-roh.json")
    if not roh:
        sys.exit("ziele-roh.json fehlt — die holt Claude aus Notion.")
    umsatz = lade(ziel, "umsatz.json")
    doterra = lade(ziel, "doterra.json")

    heute = date.today()
    jahr = str(heute.year)
    # Wie viel vom Jahr ist vorbei — siehe Kopf.
    tag_im_jahr = heute.timetuple().tm_yday
    jahr_anteil = round(tag_im_jahr / 365 * 100)

    jahresumsatz = 0.0
    if umsatz:
        jahresumsatz = round(sum(m.get("umsatz") or 0
                                 for m in (umsatz.get("monate") or [])
                                 if (m.get("monat") or "").startswith(jahr)), 2)

    rang = (doterra or {}).get("ich", {}).get("rang") or ""

    liste = []
    for i, z in enumerate(roh.get("ziele") or []):
        e = dict(z)
        e["id"] = "zl%03d" % i
        e.pop("messen", None)
        e["ist"] = None
        e["ist_text"] = ""
        e["anteil"] = None

        if z.get("messen") == "umsatz_jahr" and z.get("zielwert"):
            e["ist"] = jahresumsatz
            e["anteil"] = round(jahresumsatz / z["zielwert"] * 100, 1)
            e["ist_text"] = ("CHF %s von %s — das Jahr ist zu %d %% vorbei"
                             % (format(int(jahresumsatz), ",d").replace(",", "'"),
                                format(int(z["zielwert"]), ",d").replace(",", "'"),
                                jahr_anteil))
            e["quelle_ist"] = "ThriveCart"
        elif z.get("messen") == "doterra_rang" and rang:
            e["ist_text"] = "Aktueller Rang: %s" % rang
            e["quelle_ist"] = "doTERRA Schlagdistanz-Bericht"

        liste.append(e)

    # Erreichte nach unten, sonst nach Quartal.
    liste.sort(key=lambda x: (x.get("status") == "Erreicht",
                              x.get("quartal") or "Z", x.get("name") or ""))

    daten = {
        "items": liste,
        "stand": heute.isoformat(),
        "jahr": jahr,
        "jahr_anteil": jahr_anteil,
        "quelle": "Notion «Ziele», einmalig übernommen — gepflegt wird hier",
        "hinweis": "Nur der Jahresumsatz und der doTERRA-Rang haben einen "
                   "gemessenen Ist-Stand. Beim Rest steht bewusst keine Zahl: "
                   "geschätzter Fortschritt sieht aus wie gemessener.",
        "gebaut": datetime.now().isoformat(timespec="seconds"),
    }

    (ziel / "ziele.json").write_text(
        json.dumps(daten, ensure_ascii=False, indent=2), encoding="utf-8")

    aktiv = [z for z in liste if z.get("status") != "Erreicht"]
    print("  %d Ziele (%d aktiv, %d erreicht)"
          % (len(liste), len(aktiv), len(liste) - len(aktiv)))
    print("  Das Jahr %s ist zu %d %% vorbei" % (jahr, jahr_anteil))
    print()
    for z in liste:
        if z.get("ist_text"):
            print("  %-46s %s" % (z["name"][:46], z["ist_text"]))
    if not umsatz:
        print("  ⚠️ Kein umsatz.json — der Jahresumsatz fehlt.")
    if not doterra:
        print("  ⚠️ Kein doterra.json — der Rang fehlt.")
    print("\nAbgelegt in: %s" % (ziel / "ziele.json"))


if __name__ == "__main__":
    main()
