"""Rechnet den Wochenbogen aus — Ersatz fuer die Notion-Wochenplanung.

Dieselbe Geschichte wie beim Monatsbogen: in Notion waren „Erfolge letzte
Woche" und „Herausforderung letzte Woche" **in jeder Woche leer**, waehrend
Fokus, CTA und Sales-Pattern sorgfaeltig ausformuliert dastanden. Und die
letzte gepflegte Woche war **KW35** (25.–31. August) — seit einem Monat nichts.

    python scripts/cockpit/wochenbogen-bauen.py

🚨 **Der Wochenfokus hat ab jetzt genau eine Quelle: das Cockpit.** Der
Bild-Editor liest ihn aus **seiner** Datenbank (`daten/woche` dort, anderes
Artifact) — zwei Artifacts sind nie verbunden, die Bruecke laeuft ueber Claude.
Die Richtung ist: **Cockpit → Bild-Editor**, nie zurueck. Wer den Fokus drueben
aendert, verliert ihn beim naechsten Uebertrag.

🚨 **ISO-Wochen, nicht „Tag durch sieben".** Eine Woche laeuft Montag bis
Sonntag, und der Jahreswechsel liegt mitten drin: der 29.12.2025 gehoert zur
KW 1 von 2026. `date.isocalendar()` weiss das, jede selbstgebaute Rechnung
nicht.

🚨 **Die laufende Woche bekommt keinen Vergleich** — dieselbe Regel wie beim
Monat. Am Dienstag stehen zwei Beitraege da; das gegen eine volle Woche zu
stellen meldet jedes Mal einen Einbruch.
"""

import json
import sys
from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]

WOCHEN_ZURUECK = 16


def lade(ordner: Path, name: str):
    p = ordner / name
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        print("  ⚠️ %s nicht lesbar (%s)" % (name, e))
        return None


def kw_von(iso: str):
    """(Jahr, Woche) nach ISO — siehe Kopf."""
    try:
        j, w, _ = date.fromisoformat(iso[:10]).isocalendar()
        return "%04d-KW%02d" % (j, w)
    except Exception:
        return None


def spanne(schluessel: str):
    """Montag und Sonntag einer '2026-KW39'-Kennung."""
    j, w = int(schluessel[:4]), int(schluessel[-2:])
    mo = date.fromisocalendar(j, w, 1)
    return mo.isoformat(), (mo + timedelta(days=6)).isoformat()


def median(werte):
    w = sorted(x for x in werte if x)
    return w[len(w) // 2] if w else 0


def main():
    ziel = Path(sys.argv[1]) if len(sys.argv) > 1 else \
        ROOT / "outputs" / "cockpit" / "abgleich"
    ziel.mkdir(parents=True, exist_ok=True)

    gepostet = lade(ziel, "gepostet-voll.json") or lade(ziel, "gepostet.json")
    umsatz = lade(ziel, "umsatz.json")
    jahresplan = lade(ziel, "jahresplan.json")

    if not gepostet and not umsatz:
        sys.exit("Keine Daten da — erst gepostet-bauen.py und umsatz-bauen.py.")

    heute = date.today()
    lauf = "%04d-KW%02d" % heute.isocalendar()[:2]

    wochen = defaultdict(lambda: {
        "beitraege": 0, "reichweite_median": 0, "gespeichert": 0,
        "geteilt": 0, "kommentare": 0, "bester": None,
        "umsatz": 0.0, "kaeufe": 0, "laeuft": [],
    })

    if gepostet:
        je = defaultdict(list)
        for b in gepostet.get("beitraege") or []:
            if b.get("alte_positionierung"):
                continue
            k = kw_von(b.get("datum") or "")
            if k:
                je[k].append(b)
        for k, liste in je.items():
            e = wochen[k]
            e["beitraege"] = len(liste)
            e["reichweite_median"] = median([b.get("reach") or 0 for b in liste])
            e["gespeichert"] = sum(b.get("saved") or 0 for b in liste)
            e["geteilt"] = sum(b.get("shares") or 0 for b in liste)
            e["kommentare"] = sum(b.get("kommentare") or 0 for b in liste)
            top = sorted(liste, key=lambda b: -(b.get("reach") or 0))[0]
            e["bester"] = {"datum": top.get("datum", ""),
                           "reach": top.get("reach") or 0,
                           "anfang": (top.get("anfang") or "")[:88],
                           "link": top.get("link", "")}

    if umsatz:
        for t in umsatz.get("tage") or []:
            k = kw_von(t.get("datum") or "")
            if k:
                wochen[k]["umsatz"] += t.get("umsatz") or 0
                wochen[k]["kaeufe"] += t.get("kaeufe") or 0

    # Was in dieser Woche laut Jahresplan lief (Zeitraum ueberlappt).
    if jahresplan:
        for eintr in jahresplan.get("eintraege") or []:
            if eintr.get("bereich") == "ferien":
                continue
            a, b = eintr.get("start"), eintr.get("ende") or eintr.get("start")
            if not a:
                continue
            for k in list(wochen.keys()) + [lauf]:
                mo, so = spanne(k)
                if a <= so and b >= mo and eintr["name"] not in wochen[k]["laeuft"]:
                    wochen[k]["laeuft"].append(eintr["name"][:60])

    schluessel = sorted([k for k in wochen if k <= lauf], reverse=True)[:WOCHEN_ZURUECK]
    if lauf not in schluessel:
        schluessel.insert(0, lauf)

    liste = []
    for k in schluessel:
        e = dict(wochen[k])
        mo, so = spanne(k)
        e.update({"kw": k, "von": mo, "bis": so, "laeuft_noch": k == lauf,
                  "umsatz": round(e["umsatz"], 2)})
        liste.append(e)

    nach = {e["kw"]: e for e in liste}
    for e in liste:
        j, w = int(e["kw"][:4]), int(e["kw"][-2:])
        vorher = date.fromisocalendar(j, w, 1) - timedelta(days=7)
        vk = "%04d-KW%02d" % vorher.isocalendar()[:2]
        v = nach.get(vk)
        if v and not e["laeuft_noch"] and not v["laeuft_noch"]:
            e["vs_vorwoche"] = {
                "umsatz": round(e["umsatz"] - v["umsatz"], 2),
                "reichweite_median": e["reichweite_median"] - v["reichweite_median"],
                "beitraege": e["beitraege"] - v["beitraege"],
            }

    daten = {
        "stand": heute.isoformat(),
        "laufende_woche": lauf,
        "wochen": liste,
        "waehrung": (umsatz or {}).get("waehrung", "CHF"),
        "hinweis": "Der Wochenfokus wird hier gepflegt. Der Bild-Editor bekommt "
                   "ihn über Claude — Richtung Cockpit → Bild-Editor, nie zurück.",
        "gebaut": datetime.now().isoformat(timespec="seconds"),
    }

    (ziel / "wochenbogen.json").write_text(
        json.dumps(daten, ensure_ascii=False, indent=2), encoding="utf-8")

    print("  %d Wochen gerechnet" % len(liste))
    print()
    print("  %-11s %-23s %8s %6s %9s" % ("KW", "Zeitraum", "Umsatz", "Beitr", "Reichw."))
    for e in liste[:10]:
        print("  %-11s %s bis %s %8.2f %6d %9d %s"
              % (e["kw"], e["von"], e["bis"], e["umsatz"], e["beitraege"],
                 e["reichweite_median"], "← läuft" if e["laeuft_noch"] else ""))
    print("\nAbgelegt in: %s" % (ziel / "wochenbogen.json"))


if __name__ == "__main__":
    main()
