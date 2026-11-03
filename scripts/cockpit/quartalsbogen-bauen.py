"""Rechnet den Quartalsbogen aus — der Zeitraum, der bisher ganz gefehlt hat.

Jahr, Monat und Woche hatten je ein Blatt; das Quartal nicht. Genau dazwischen
liegt aber die Entscheidung, die der Monat schon voraussetzt: welches Angebot in
welchem Monat im Mittelpunkt steht, welches kostenlose Angebot davor laeuft und
wann ein Workshop ist.

    python scripts/cockpit/umsatz-bauen.py        # ThriveCart
    python scripts/cockpit/gepostet-bauen.py      # Instagram
    python scripts/cockpit/planung-abgleichen.py  # Belege im Workspace
    python scripts/cockpit/quartalsbogen-bauen.py # -> quartalsbogen.json

Danach: ArtifactData set, Sammlung "daten", Dokument "quartalsbogen".

🚨 **Dieses Skript schreibt nur die gerechneten Zahlen.** Patricias Antworten —
Rueckblick, Monatsthemen, Workshop-Termine, was wegfaellt — stehen in
`daten/quartalsbogen-notizen` und werden hier **nie** angefasst. Dasselbe Muster
wie beim Monatsbogen und bei `daten/gepostet-notizen`.

🚨 **Das laufende Quartal bekommt kein Urteil.** Ein Quartal, das seit drei
Wochen laeuft, gegen ein volles zu stellen meldet jedes Mal einen Einbruch -
dieselbe Regel wie beim Monat und bei der Woche. Es steht als "laeuft noch" da.

🚨 **Die Fragen stehen nicht hier, sondern in `scripts/jahresplan/fragen.json`**
unter `zeitraeume.quartal`. Dieses Skript liest sie von dort und legt je Frage
ein leeres Feld an, damit Bogen und Skill nie auseinanderlaufen. Eine zweite
Fragenliste im Code waere genau der Fehler, den der Plan vermeiden will.

🚨 **"Keine Spur" heisst nicht "nicht passiert".** Was `planung-abgleichen.py`
ohne Beleg findet, ist ein Hinweis zum Nachsehen - nicht ein Urteil. Die
Entscheidung je Zeile trifft Patricia im Bogen.
"""

import json
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]
FRAGEN = ROOT / "scripts" / "jahresplan" / "fragen.json"

QUARTALE_ZURUECK = 8
# Der Monat, in dem das naechste Quartal geplant wird - Patricias Entscheid 02.11.2026.
PLANUNGSMONAT = {3: "Q2", 6: "Q3", 9: "Q4", 12: "Q1"}


def lade(ordner: Path, name: str):
    p = ordner / name
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        print("  ⚠️ %s nicht lesbar (%s)" % (name, e))
        return None


def quartal_von(iso: str):
    """'2026-Q4' aus einem ISO-Datum."""
    try:
        d = date.fromisoformat(iso[:10])
        return "%04d-Q%d" % (d.year, (d.month - 1) // 3 + 1)
    except Exception:
        return None


def monate_von(schluessel: str):
    """Die drei Monatsnummern eines '2026-Q4'."""
    q = int(schluessel[-1])
    return [(q - 1) * 3 + 1, (q - 1) * 3 + 2, (q - 1) * 3 + 3]


def median(werte):
    w = sorted(x for x in werte if x)
    return w[len(w) // 2] if w else 0


def fragen_leer():
    """Je Frage aus fragen.json ein leeres Feld - eine Quelle, kein Zweitkatalog."""
    if not FRAGEN.exists():
        print("  ⚠️ fragen.json fehlt, Bogen ohne Fragenfelder")
        return [], []
    daten = json.loads(FRAGEN.read_text(encoding="utf-8"))
    q = (daten.get("zeitraeume") or {}).get("quartal")
    if not q:
        print("  ⚠️ zeitraeume.quartal fehlt in fragen.json")
        return [], []
    felder, monatsfelder = [], []
    for s in q["schritte"]:
        for f in s.get("fragen", []):
            felder.append({
                "id": f["id"], "frage": f["frage"], "hilfe": f.get("hilfe", ""),
                "schritt": s["titel"], "quelle": f.get("quelle", ""), "wert": "",
            })
        if "monate" in s:
            monatsfelder = [
                {"id": f["id"], "frage": f["frage"], "typ": f["typ"],
                 "optionen": f.get("optionen", []), "quelle": f.get("quelle", "")}
                for f in s["monate"]["felder"]
            ]
    return felder, monatsfelder


def main():
    ziel = Path(sys.argv[1]) if len(sys.argv) > 1 else \
        ROOT / "outputs" / "cockpit" / "abgleich"
    ziel.mkdir(parents=True, exist_ok=True)

    gepostet = lade(ziel, "gepostet-voll.json") or lade(ziel, "gepostet.json")
    umsatz = lade(ziel, "umsatz.json")
    abgleich = lade(ziel, "planung-abgleich.json")

    if not gepostet and not umsatz:
        sys.exit("Keine Daten da — erst gepostet-bauen.py und umsatz-bauen.py.")

    heute = date.today()
    lauf = quartal_von(heute.isoformat())

    quartale = defaultdict(lambda: {
        "beitraege": 0, "kommentare": 0,
        "umsatz": 0.0, "kaeufe": 0, "monate": {}, "profile": {},
    })

    # --- Instagram. 🚨 Das Feld heisst "reach", nicht "reichweite" - am 02.11. beim
    # ersten Lauf stand deshalb ueberall Median 0, und eine Null sieht aus wie ein
    # Befund. Darum unten der Waechter.
    # 🚨 Die beiden Konten werden NIE zusammengerechnet: rund 2'000 gegen rund 60
    # Followerinnen, ein gemeinsamer Median waere zweimal etwas anderes.
    if gepostet:
        je = defaultdict(lambda: defaultdict(list))
        for b in gepostet.get("beitraege") or []:
            if b.get("alte_positionierung"):
                continue
            k = quartal_von(b.get("datum") or "")
            if k:
                je[k][b.get("handle") or "ohne Konto"].append(b)
        for k, nach_konto in je.items():
            q = quartale[k]
            q["beitraege"] = sum(len(v) for v in nach_konto.values())
            q["kommentare"] = sum(b.get("kommentare") or 0
                                  for v in nach_konto.values() for b in v)
            for handle, liste in nach_konto.items():
                q["profile"][handle] = {
                    "beitraege": len(liste),
                    "reichweite_median": median([b.get("reach") for b in liste]),
                    "kommentare": sum(b.get("kommentare") or 0 for b in liste),
                    "ohne_kommentar": sum(1 for b in liste if not b.get("kommentare")),
                }

    # --- Umsatz
    if umsatz:
        for m in umsatz.get("monate") or []:
            monat = m.get("monat") or ""          # "2026-10"
            k = quartal_von(monat + "-01") if len(monat) == 7 else None
            if not k:
                continue
            q = quartale[k]
            q["umsatz"] += float(m.get("umsatz") or 0)
            q["kaeufe"] += int(m.get("kaeufe") or 0)
            q["monate"][monat] = {
                "umsatz": float(m.get("umsatz") or 0),
                "kaeufe": int(m.get("kaeufe") or 0),
            }

    felder, monatsfelder = fragen_leer()

    # --- Zeilen, jüngstes Quartal zuerst
    zeilen = []
    for k in sorted(quartale, reverse=True)[:QUARTALE_ZURUECK]:
        q = dict(quartale[k])
        q["quartal"] = k
        q["laeuft_noch"] = (k == lauf)
        if q["laeuft_noch"]:
            q["hinweis"] = "läuft noch — kein Vergleich mit vollen Quartalen"
        zeilen.append(q)

    # --- Was aus dem Jahresplan keine Spur hat
    # 🚨 planung-abgleich.json traegt "jahresplan" als DICT (Schluessel jp000, jp001 …)
    # und den Befund als "keine_spur" mit Unterstrich. Am 02.11. stand hier erst eine
    # Liste und "keine Spur" mit Leerzeichen - Ergebnis: 0 Funde, die wie ein Befund
    # aussahen. Ein leeres Feld ist immer erst ein Verdacht auf den eigenen Lesefehler.
    ohne_spur, abgleich_stand, abgleich_zaehler = [], "", {}
    if abgleich:
        abgleich_stand = abgleich.get("stand") or ""
        jp = abgleich.get("jahresplan") or {}
        if isinstance(jp, dict):
            for schluessel, e in sorted(jp.items()):
                befund = (e or {}).get("befund") or ""
                abgleich_zaehler[befund] = abgleich_zaehler.get(befund, 0) + 1
                if befund == "keine_spur":
                    ohne_spur.append({
                        "kennung": schluessel,
                        "befund": befund,
                        # Der Titel steht im Jahresplan-Dokument, nicht im Abgleich -
                        # das Cockpit setzt beides ueber die Kennung zusammen.
                        "titel_aus": "daten/jahresplan über die Kennung",
                        "hinweis": "keine Spur im Workspace — nachsehen, nicht abhaken",
                    })
        if abgleich_stand and abgleich_stand < (heute.replace(day=1).isoformat()):
            print("  ⚠️ planung-abgleich.json ist vom %s — vor der Quartalsplanung "
                  "planung-abgleichen.py neu laufen lassen" % abgleich_stand)

    naechstes = PLANUNGSMONAT.get(heute.month)
    bogen = {
        "stand": heute.isoformat(),
        "laufendes_quartal": lauf,
        "planung_fällig": bool(naechstes),
        "plant_jetzt": naechstes or "",
        "quelle": "quartalsbogen-bauen.py aus gepostet, umsatz und planung-abgleich",
        "fragen": felder,
        "monatsfelder": monatsfelder,
        "quartale": zeilen,
        "ohne_spur": ohne_spur[:30],
        "abgleich_stand": abgleich_stand,
        "abgleich_befunde": abgleich_zaehler,
        "hinweis_notizen": ("Patricias Antworten stehen in daten/quartalsbogen-notizen "
                            "und werden von diesem Lauf nie angefasst."),
    }

    # 🚨 Waechter gegen die stille Null: wenn Beitraege da sind, muss mindestens ein
    # Konto einen Median ueber 0 haben. Sonst wurde ein Feldname falsch gelesen - und
    # eine Null in einer Tabelle sieht genauso plausibel aus wie eine gemessene Zahl.
    mit_beitraegen = [z for z in zeilen if z["beitraege"]]
    if mit_beitraegen:
        hoechster = max((p["reichweite_median"]
                         for z in mit_beitraegen for p in z["profile"].values()),
                        default=0)
        assert hoechster > 0, \
            "Median ueberall 0 bei %d Beitraegen - Feldname falsch gelesen?" % \
            sum(z["beitraege"] for z in mit_beitraegen)

    p = ziel / "quartalsbogen.json"
    p.write_text(json.dumps(bogen, ensure_ascii=False, indent=1), encoding="utf-8")

    print("  %s (%d Zeichen)" % (p.name, len(p.read_text(encoding='utf-8'))))
    print("  laufendes Quartal: %s%s" % (
        lauf, "  ·  jetzt wird %s geplant" % naechstes if naechstes else ""))
    print("  %d Quartale gerechnet, %d Fragenfelder, %d ohne Spur"
          % (len(zeilen), len(felder), len(ohne_spur)))
    for z in zeilen[:4]:
        print("    %s  %2d Beiträge  CHF %8.2f%s" % (
            z["quartal"], z["beitraege"], z["umsatz"],
            "  (läuft noch)" if z["laeuft_noch"] else ""))
        for handle, pr in sorted(z["profile"].items()):
            print("        %-34s %2d Beiträge  Median %4d  %d ohne Kommentar"
                  % (handle[:34], pr["beitraege"], pr["reichweite_median"],
                     pr["ohne_kommentar"]))
    print()
    print("  Danach: ArtifactData set → Sammlung daten, Dokument quartalsbogen")


if __name__ == "__main__":
    main()
