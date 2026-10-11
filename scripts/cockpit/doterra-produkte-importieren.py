"""Holt «doTERRA Produkte» und «Wirkbereiche» einmalig ins Cockpit.

21 Öle und 22 Wirkbereiche, in Notion über Relationen verknüpft. Hier wird
daraus ein Nachschlagewerk in beide Richtungen: vom Öl zu seinen Bereichen und
vom Bereich zu den Ölen.

🚨 **DAS IST INTERNES NACHSCHLAGEN, NIE CONTENT.** Eine Tabelle, die Öle
Beschwerden zuordnet — Erkältung, Fieber, Angst, Kopfweh — ist genau das, was
doTERRA als Heilversprechen verbietet. Wer eine Zeile daraus in eine Caption
kopiert, hat ein Compliance-Problem. Deshalb steht die Warnung **im Cockpit
sichtbar** und nicht nur hier im Kommentar: eine Warnung, die niemand sieht, ist
keine.

Erlaubt bleibt Patricias «bei mir war»-Rahmen aus
`context/doterra/patricia-wendepunkt-story.md` — die eigene Erfahrung erzählen,
statt eine Wirkung zu behaupten.

🚨 **Einmal-Umzug, kein Abgleich.** `daten/doterra-produkte` gehört ab hier
Patricia. Der tägliche Lauf darf es nie mit `set` überschreiben.

🚨 **Die Verknüpfung ist halb fertig, und das wird angezeigt.** Nur 9 der 21 Öle
haben überhaupt Wirkbereiche; bei 12 steht nichts. Ein Nachschlagewerk, das
seine eigenen Lücken verschweigt, führt bei der Suche in die Irre — man denkt,
zu diesem Bereich gebe es kein Öl.

    python scripts/cockpit/doterra-produkte-importieren.py [zielordner]
    # danach: ArtifactData set -> Sammlung "daten", Dokument "doterra-produkte"
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


def main():
    ziel = Path(sys.argv[1]) if len(sys.argv) > 1 else \
        ROOT / "outputs" / "cockpit" / "abgleich"
    roh_datei = ziel / "doterra-roh.json"
    if not roh_datei.exists():
        sys.exit("doterra-roh.json fehlt — die holt Claude aus Notion.")
    roh = json.loads(roh_datei.read_text(encoding="utf-8"))

    produkte = roh.get("produkte") or []
    bereiche = roh.get("wirkbereiche") or []
    name_von = {p["u"]: p["name"] for p in produkte}

    # Bereich -> Öle
    b_liste = []
    for i, b in enumerate(sorted(bereiche, key=lambda x: x["name"])):
        oele = [name_von.get(u) for u in (b.get("p") or []) if name_von.get(u)]
        # 🚨 Eine Kennung ohne Namen heisst: das Produkt fehlt in der Liste.
        # Still weglassen wuerde die Zeile kuerzer und falsch machen.
        fehlend = [u for u in (b.get("p") or []) if not name_von.get(u)]
        b_liste.append({
            "id": "wb%02d" % i,
            "name": b["name"],
            "oele": sorted(oele),
            "anzahl": len(oele),
            "unbekannt": len(fehlend),
        })

    # Öl -> Bereiche (aus derselben Quelle rueckwaerts gerechnet, damit es
    # nicht zwei Listen gibt, die auseinanderlaufen koennen)
    zu_oel = {}
    for b in bereiche:
        for u in (b.get("p") or []):
            zu_oel.setdefault(u, []).append(b["name"])

    p_liste = []
    for i, p in enumerate(sorted(produkte, key=lambda x: x["name"])):
        bs = sorted(zu_oel.get(p["u"], []))
        p_liste.append({
            "id": "dp%02d" % i,
            "name": p["name"],
            "kategorie": p.get("kat") or "",
            "bereiche": bs,
            "anzahl": len(bs),
            "notizen": p.get("notizen") or 0,
        })

    ohne_bereich = [p for p in p_liste if not p["anzahl"]]
    leere_bereiche = [b for b in b_liste if not b["anzahl"]]

    daten = {
        "produkte": p_liste,
        "bereiche": b_liste,
        "stand": date.today().isoformat(),
        "ohne_bereich": len(ohne_bereich),
        "leere_bereiche": len(leere_bereiche),
        "quelle": "Notion «doTERRA Produkte» + «Wirkbereiche», einmalig "
                  "übernommen am 2026-09-24",
        "warnung": ("Internes Nachschlagen. Diese Zuordnung darf NIE in Caption, "
                    "Story, Mail oder Anzeige — eine Wirkung zu behaupten ist bei "
                    "doTERRA verboten. Erlaubt ist der «bei mir war»-Rahmen: die "
                    "eigene Erfahrung erzählen, nicht die Wirkung versprechen."),
        "hinweis": ("Die Verknüpfung ist halb fertig: %d von %d Ölen haben noch "
                    "keinen Wirkbereich." % (len(ohne_bereich), len(p_liste))),
        "gebaut": datetime.now().isoformat(timespec="seconds"),
    }

    (ziel / "doterra-produkte.json").write_text(
        json.dumps(daten, ensure_ascii=False, indent=2), encoding="utf-8")

    print("  %d Öle · %d Wirkbereiche" % (len(p_liste), len(b_liste)))
    print()
    print("  Öle mit den meisten Bereichen:")
    for p in sorted(p_liste, key=lambda x: -x["anzahl"])[:6]:
        print("    %-26s %2d  %s" % (p["name"], p["anzahl"],
                                     ", ".join(p["bereiche"][:4])[:62]))
    print()
    if ohne_bereich:
        print("  ⚠️ %d Öle ohne Wirkbereich: %s"
              % (len(ohne_bereich), ", ".join(p["name"] for p in ohne_bereich)))
    if leere_bereiche:
        print("  ⚠️ %d Bereiche ohne Öl: %s"
              % (len(leere_bereiche), ", ".join(b["name"] for b in leere_bereiche)))
    unbek = sum(b["unbekannt"] for b in b_liste)
    if unbek:
        print("  🚨 %d Verweise zeigen auf ein Produkt, das nicht in der Liste "
              "steht." % unbek)
    print()
    print("  🚨 %s" % daten["warnung"])
    print("\nAbgelegt in: %s" % (ziel / "doterra-produkte.json"))


if __name__ == "__main__":
    main()
