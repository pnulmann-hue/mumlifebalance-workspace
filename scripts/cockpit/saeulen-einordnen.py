"""Rechnet den PIE-Mix der geposteten Beiträge — abgelesen, nicht gepflegt.

🚨 **Die Content-Säule war an keinem einzigen der 541 Beiträge gesetzt.** Die
Auswahlliste stand in Notion und steht jetzt im Cockpit, gefüllt wurde sie nie.
Damit lässt sich der Mix nicht *ablesen* — er muss abgeleitet werden.

Das ist dasselbe Muster wie bei Lead/Reichweite im Cockpit: **eine Ableitung,
die sichtbar dasteht, ist ehrlicher als ein Feld, dem niemand ansieht, dass es
leer ist.** Und sie kostet keine Pflege.

🚨 **Die Zuordnung ist ein Urteil, keine Messung.** Claude hat am 24.09.2026
alle 389 Hooks der aktuellen Positionierung gelesen und je einen Buchstaben
vergeben. Bei Mischformen entscheidet, was den Hook *trägt* — nicht, was
irgendwo in der Caption auch noch vorkommt. Wer anderer Meinung ist, ändert den
Buchstaben in `CODES`; die Reihenfolge ist die nach Datum sortierte Liste aus
`hooks-zum-einordnen.json`.

| | |
|---|---|
| **P — Persönlichkeit** | ihre Geschichte, ihr Alltag, ihre Vergangenheit |
| **I — Inspiration** | Spiegel, Mutmachen, Perspektivwechsel — ohne Anleitung |
| **E — Expertise** | Anleitung, Diagnose, Mechanismus, Schritte |

**Soll nach Julia-Trost-Logik: 35 / 35 / 30.**

    python scripts/cockpit/saeulen-einordnen.py [zielordner]
"""

import json
import sys
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]

NAME = {"P": "Persönlichkeit", "I": "Inspiration", "E": "Expertise"}
SOLL = {"P": 35, "I": 35, "E": 30}

# 389 Buchstaben, in Zehnergruppen — die Kommentare sind die Nummern aus
# hooks-zum-einordnen.json, damit sich jede Zeile zurückverfolgen lässt.
CODES = (
    "IIEPPIIPIP"   # 000
    "PPPPPIIIPP"   # 010
    "PPIIIEEIIP"   # 020
    "EIEEPPEEEE"   # 030
    "EPPIIIPPPP"   # 040
    "PEEEPPIIEE"   # 050
    "PIPPPEPPPP"   # 060
    "IPPIEIIIEP"   # 070
    "EEIEEEEPPP"   # 080
    "EEEEEPIEEE"   # 090
    "EEIIEPEEEE"   # 100
    "EIEPEEPEEI"   # 110
    "IPIEIPEEEE"   # 120
    "PIPEEPEEEE"   # 130
    "EEEEEEEEEE"   # 140
    "EEEPEIPPPI"   # 150
    "IPPEEEEEPE"   # 160
    "EPIEEIPEII"   # 170
    "IIPIEEEIEE"   # 180
    "EEEEEEEEEE"   # 190
    "PPEPPEEPEE"   # 200
    "EEEEEPIEEP"   # 210
    "EPEPIPPPEP"   # 220
    "PIPEIPEIPE"   # 230
    "PPPPPPPIEP"   # 240
    "EEEEPPPIPP"   # 250
    "PPPPPPEEEI"   # 260
    "IIEIIIPPPP"   # 270
    "EPEPPPPIEE"   # 280
    "PIIIEIIIIP"   # 290
    "PEIIEIPPEP"   # 300
    "EEIEIEEEEI"   # 310
    "IEPIIIPIEE"   # 320
    "EIEPIIPIII"   # 330
    "EIIEIPPPPP"   # 340
    "PPEIPPPIPP"   # 350
    "PPPEEIIIII"   # 360
    "IIIIIIEIII"   # 370
    "IIPPIPEPE"    # 380
)


def main():
    ziel = Path(sys.argv[1]) if len(sys.argv) > 1 else \
        ROOT / "outputs" / "cockpit" / "abgleich"
    hooks = json.loads((ziel / "hooks-zum-einordnen.json").read_text(encoding="utf-8"))

    if len(CODES) != len(hooks):
        sys.exit("🚨 %d Buchstaben, aber %d Beiträge. Eine Zeile fehlt oder ist "
                 "zu viel — nichts gerechnet." % (len(CODES), len(hooks)))

    voll = json.loads((ziel / "gepostet-voll.json").read_text(encoding="utf-8"))
    zahlen = {b["id"]: b for b in voll["beitraege"]}

    for h, c in zip(hooks, CODES):
        h["saeule"] = c

    gesamt = Counter(h["saeule"] for h in hooks)
    n = len(hooks)

    # Je Quartal, damit ein Verlauf sichtbar wird statt nur ein Durchschnitt.
    def quartal(d):
        return "%s-Q%d" % (d[:4], (int(d[5:7]) - 1) // 3 + 1)

    proq = defaultdict(Counter)
    for h in hooks:
        if h.get("datum"):
            proq[quartal(h["datum"])][h["saeule"]] += 1

    # 🚨 Reichweite je Säule: die eigentliche Frage ist nicht nur «wie ist der
    # Mix», sondern «welche Säule trägt überhaupt».
    reich = defaultdict(list)
    raten = defaultdict(list)
    for h in hooks:
        b = zahlen.get(h["id"])
        if b and b.get("reif") and b.get("reach"):
            reich[h["saeule"]].append(b["reach"])
            if b.get("rate") is not None:
                raten[h["saeule"]].append(b["rate"])

    def median(xs):
        if not xs:
            return None
        s = sorted(xs)
        m = len(s) // 2
        return s[m] if len(s) % 2 else (s[m - 1] + s[m]) / 2

    liste = []
    for k in ("P", "I", "E"):
        ist = round(gesamt[k] / n * 100)
        liste.append({
            "kuerzel": k,
            "name": NAME[k],
            "anzahl": gesamt[k],
            "ist_prozent": ist,
            "soll_prozent": SOLL[k],
            "abweichung": ist - SOLL[k],
            "median_reichweite": median(reich[k]),
            "median_rate": round(median(raten[k]), 2) if raten[k] else None,
        })

    quartale = []
    for q in sorted(proq):
        c = proq[q]
        s = sum(c.values())
        quartale.append({"quartal": q, "beitraege": s,
                         **{NAME[k].lower(): round(c[k] / s * 100) for k in "PIE"}})

    daten = {
        "saeulen": liste,
        "quartale": quartale,
        "beitraege": n,
        "stand": date.today().isoformat(),
        "quelle": "Abgeleitet aus dem Hook, nicht gepflegt — Claude 24.09.2026",
        "hinweis": ("Die Content-Säule war an keinem Beitrag gesetzt. Diese "
                    "Einordnung ist ein Urteil aus dem Hook, keine Messung. "
                    "Die Reichweiten daneben sind gemessen."),
        "gebaut": datetime.now().isoformat(timespec="seconds"),
    }
    (ziel / "saeulen.json").write_text(
        json.dumps(daten, ensure_ascii=False, indent=2), encoding="utf-8")

    print("  %d Beiträge der aktuellen Positionierung\n" % n)
    print("  %-16s %6s %7s %7s %12s %8s"
          % ("Säule", "Anzahl", "Ist", "Soll", "Median Reich", "Rate"))
    for e in liste:
        print("  %-16s %6d %6d %% %6d %% %12s %7s"
              % (e["name"], e["anzahl"], e["ist_prozent"], e["soll_prozent"],
                 e["median_reichweite"] if e["median_reichweite"] else "—",
                 ("%.2f %%" % e["median_rate"]) if e["median_rate"] else "—"))
    print()
    print("  Verlauf je Quartal:")
    print("  %-9s %7s %8s %8s %8s" % ("", "Beitr.", "Persönl.", "Inspir.", "Expert."))
    for q in quartale:
        print("  %-9s %7d %7d %% %7d %% %7d %%"
              % (q["quartal"], q["beitraege"], q["persönlichkeit"],
                 q["inspiration"], q["expertise"]))
    print("\nAbgelegt in: %s" % (ziel / "saeulen.json"))


if __name__ == "__main__":
    main()
