#!/usr/bin/env python3
"""Umsatz je Kommentar-Stichwort — welches Stichwort bringt Käufe, nicht nur Kommentare.

Patricia, 13.10.2026 (aus dem Kurs „Content Shortcut“): *„dann geht sie einen schritt
weiter und vergleicht die umsätze pro thema. du hast ja die anbindung zu thrivecart.“*

Der Weg: Wer ein Stichwort kommentiert und sich einträgt, bekommt in ActiveCampaign
den Eintrags-Tag des Freebies (`eintrag_tag_id` in active-funnels.json). Kauft dieselbe
Person danach bei ThriveCart, gehört der Umsatz zu diesem Stichwort.

🚨 Mailadressen werden nur im Speicher verglichen, als Hash, und nie abgelegt. Die
Ausgabe enthält ausschliesslich Summen je Stichwort — keine Namen, keine Adressen.

🚨 Was das NICHT misst: Wer kommentiert, aber sich nicht einträgt, fehlt. Wer über
einen Story-Link oder die Bio kauft, ohne je ein Stichwort benutzt zu haben, landet
bei „ohne Stichwort“. Die Zahl ist also eine Untergrenze je Stichwort. Auf einen
einzelnen Beitrag lässt sich ein Kauf nicht zurückführen — mehrere Beiträge spielen
dasselbe Stichwort, und ActiveCampaign weiss nicht, welcher es war.

    python scripts/cockpit/umsatz-je-stichwort.py [--ab 2026-06-30]
→ outputs/cockpit/abgleich/umsatz-stichwort.json (gitignored)
"""
import argparse
import hashlib
import importlib.util
import json
import re
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]
HIER = Path(__file__).resolve().parent
ZIEL = ROOT / "outputs" / "cockpit" / "abgleich" / "umsatz-stichwort.json"


def lade(name, datei):
    spec = importlib.util.spec_from_file_location(name, str(HIER / datei))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


tc = lade("tc", "thrivecart-holen.py")
umsatz = lade("umsatz", "umsatz-bauen.py")      # alle_transaktionen()
fu = lade("fu", "funnel-uebersicht-bauen.py")    # ac() mit drei Anläufen


def h(mail):
    return hashlib.sha256((mail or "").strip().lower().encode("utf-8")).hexdigest()


def stichwort(roh):
    """„STANDBEIN (Flow live seit …)“ -> STANDBEIN. Ein Klammerzusatz hat die
    Wortsuche schon einmal gekippt (CLAUDE.md, Funnel-Reiter)."""
    m = re.match(r"\s*([A-ZÄÖÜ0-9]{2,})", roh or "")
    return m.group(1) if m else None


def funnel_tags():
    af = json.loads((ROOT / "context" / "active-funnels.json").read_text(encoding="utf-8"))
    liste = af if isinstance(af, list) else af.get("funnels") or []
    raus = defaultdict(lambda: {"tags": set(), "freebie": ""})
    def suche(o, schluessel):
        """Die Felder liegen je nach Funnel oben oder unter ac_integration/traffic_quellen."""
        if isinstance(o, dict):
            if schluessel in o:
                yield o[schluessel]
            for v in o.values():
                yield from suche(v, schluessel)
        elif isinstance(o, list):
            for v in o:
                yield from suche(v, schluessel)

    for f in liste:
        kw = next((stichwort(w) for w in suche(f, "manychat_keyword")
                   if isinstance(w, str) and stichwort(w)), None)
        ids = set()
        for w in suche(f, "eintrag_tag_ids"):
            ids |= set(w or [])
        for w in suche(f, "eintrag_tag_id"):
            if w:
                ids.add(w)
        if kw and ids:
            raus[kw]["tags"] |= {int(i) for i in ids}
            raus[kw]["freebie"] = raus[kw]["freebie"] or f.get("name") or f.get("id") or ""
    return raus


def tag_traeger(tid):
    """Alle Kontakte eines Tags mit Mail-Hash und Datum der Tag-Vergabe."""
    raus, versatz = {}, 0
    while True:
        d = fu.ac("contacts?tagid=%d&limit=100&offset=%d" % (tid, versatz))
        kontakte = d.get("contacts", [])
        for c in kontakte:
            datum = None
            try:
                ct = fu.ac("contacts/%s/contactTags" % c["id"]).get("contactTags", [])
                datum = min((x.get("cdate") or "")[:10] for x in ct
                            if str(x.get("tag")) == str(tid)) or None
            except (ValueError, Exception):
                datum = (c.get("cdate") or "")[:10] or None
            raus[h(c.get("email"))] = datum or (c.get("cdate") or "")[:10]
        if len(kontakte) < 100:
            break
        versatz += 100
    return raus


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--ab", default="2026-06-30", help="Zeitraum ab (wie die Beitragsdaten)")
    a = p.parse_args()

    roh, _ = umsatz.alle_transaktionen(tc.schluessel())
    kaeufe = []
    for x in roh:
        datum = (x.get("date") or "")[:10]
        if not datum:
            continue
        mail = (x.get("customer") or {}).get("email") or ""
        kaeufe.append({
            "datum": datum,
            "betrag": (x.get("amount") or 0) / 100.0,      # Rappen -> Franken
            "art": x.get("transaction_type") or "?",
            "produkt": (x.get("item_name") or "")[:60],
            "person": h(mail) if mail else None,
            "waehrung": x.get("currency") or "?",
        })
        # die Mailadresse selbst wird hier verworfen
    im_zeitraum = [k for k in kaeufe if k["datum"] >= a.ab]
    gesamt = sum(k["betrag"] for k in im_zeitraum)
    charges = [k for k in im_zeitraum if k["art"] == "charge"]

    zugeordnet_personen = set()
    kaeufer_je_kw = {}
    zeilen = []
    for kw, info in sorted(funnel_tags().items()):
        traeger = {}
        for tid in info["tags"]:
            for person, datum in tag_traeger(tid).items():
                if person not in traeger or (datum and datum < traeger[person]):
                    traeger[person] = datum
        passend = [k for k in im_zeitraum
                   if k["person"] in traeger and k["datum"] >= (traeger[k["person"]] or "0")]
        kaeufer = {k["person"] for k in passend if k["art"] == "charge"}
        zugeordnet_personen |= {k["person"] for k in passend}
        produkte = defaultdict(float)
        for k in passend:
            produkte[k["produkt"]] += k["betrag"]
        kaeufer_je_kw[kw] = kaeufer
        zeilen.append({
            "stichwort": kw,
            "freebie": info["freebie"],
            "eintragungen": len(traeger),
            "kaeuferinnen": len(kaeufer),
            "kaeufe": sum(1 for k in passend if k["art"] == "charge"),
            "umsatz": round(sum(k["betrag"] for k in passend), 2),
            "produkte": [{"name": n, "umsatz": round(b, 2)}
                         for n, b in sorted(produkte.items(), key=lambda z: -z[1])][:5],
        })
        print("  %-12s %3d Eintragungen · %2d Käuferinnen · CHF %8.2f"
              % (kw, len(traeger), len(kaeufer), zeilen[-1]["umsatz"]))

    # 🚨 Dieselbe Käuferin kann mehrere Eintrags-Tags tragen. Dann steht ihr Kauf bei
    # jedem dieser Stichwörter — die Spalte darf nicht aufsummiert werden.
    for z in zeilen:
        eigene = kaeufer_je_kw.get(z["stichwort"], set())
        z["geteilt_mit"] = sorted(k for k, s in kaeufer_je_kw.items()
                                  if k != z["stichwort"] and eigene & s)
    ohne = sum(k["betrag"] for k in im_zeitraum if k["person"] not in zugeordnet_personen)
    daten = {
        "stand": date.today().isoformat(),
        "ab": a.ab,
        "waehrung": "CHF",
        "misst": ("Umsatz von Personen, die den Eintrags-Tag eines Stichworts tragen und "
                  "NACH der Eintragung gekauft haben. Untergrenze: wer kommentiert, sich aber "
                  "nicht einträgt, fehlt. Nicht je Beitrag zurechenbar."),
        "gesamt": {"umsatz": round(gesamt, 2), "kaeufe": len(charges),
                   "bestellwert": round(sum(k["betrag"] for k in charges) / len(charges), 2)
                   if charges else 0,
                   "ohne_stichwort": round(ohne, 2),
                   "anteil_ohne_stichwort": round(100 * ohne / gesamt, 1) if gesamt else None},
        "stichwoerter": sorted(zeilen, key=lambda z: -z["umsatz"]),
    }
    ZIEL.write_text(json.dumps(daten, ensure_ascii=False, indent=1), encoding="utf-8")
    print("Gesamt seit %s: CHF %.2f · %d Käufe · ohne Stichwort %.0f %%"
          % (a.ab, gesamt, len(charges), daten["gesamt"]["anteil_ohne_stichwort"] or 0))
    print("->", ZIEL)


if __name__ == "__main__":
    main()
