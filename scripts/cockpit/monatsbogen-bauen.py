"""Rechnet den Monatsbogen aus — den Teil, den niemand tippen sollte.

Ersetzt die Notion-Monatsplanung. Deren Vorlage hat sechs Abschnitte; der
zweite heisst „Analysen & Kennzahlen" und ist der Grund, warum der ganze Bogen
nicht gepflegt wird: bei September **und** Oktober 2026 standen „Erkenntnisse
Content-Analyse", „Erkenntnis Kennzahlen-Analyse" und „Learnings aus dem
letzten Monat" leer — waehrend die Monatsziele daneben sorgfaeltig ausformuliert
waren. Es lag nie an der Disziplin. Die Zahlen dafuer liegen in vier Werkzeugen.

    python scripts/cockpit/umsatz-bauen.py      # ThriveCart
    python scripts/cockpit/gepostet-bauen.py    # Instagram
    python scripts/cockpit/monatsbogen-bauen.py # -> monatsbogen.json

🚨 **Dieses Skript schreibt nur die gerechneten Zahlen.** Patricias Texte —
Reflexion, Monatsziele, Foki, Fazit — stehen in `daten/monatsbogen-notizen` und
werden hier **nie** angefasst. Dasselbe Muster wie `daten/gepostet-notizen`.

🚨 **Podcast und YouTube stehen in der Notion-Vorlage, macht sie aber nicht.**
Die Vorlage stammt aus einem fremden Kurs-Setup. Hier kommen nur die Kanaele
vor, die sie wirklich bespielt — sonst sind zwei von fuenf Zeilen immer leer
und der Bogen sieht dauerhaft unerledigt aus.

🚨 **Nur abgeschlossene Monate bekommen ein Urteil.** Der laufende Monat wird
gezeigt, aber als „laeuft noch" markiert: eine Reichweite am 3. des Monats mit
der eines vollen Monats zu vergleichen, erzeugt jedes Mal einen falschen Alarm.
"""

import json
import sys
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]

# Wie viele Monate rueckwaerts der Bogen zeigt.
MONATE_ZURUECK = 12


def lade(ordner: Path, name: str):
    p = ordner / name
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        print("  ⚠️ %s nicht lesbar (%s)" % (name, e))
        return None


def median(werte):
    w = sorted(x for x in werte if x)
    return w[len(w) // 2] if w else 0


def main():
    ziel = Path(sys.argv[1]) if len(sys.argv) > 1 else \
        ROOT / "outputs" / "cockpit" / "abgleich"
    ziel.mkdir(parents=True, exist_ok=True)

    # Das VOLLE Archiv lesen, nicht den Cockpit-Ausschnitt — sonst fehlen
    # aeltere Monate, und der Vergleich „besser als letztes Jahr" geht nicht.
    gepostet = lade(ziel, "gepostet-voll.json") or lade(ziel, "gepostet.json")
    umsatz = lade(ziel, "umsatz.json")
    jahresplan = lade(ziel, "jahresplan.json")
    kosten = lade(ziel, "kosten.json")

    if not gepostet and not umsatz:
        sys.exit("Weder Instagram- noch ThriveCart-Daten da. Erst die beiden "
                 "anderen Skripte laufen lassen.")

    heute = date.today()
    lauf = heute.strftime("%Y-%m")

    monate = defaultdict(lambda: {
        "beitraege": 0, "reichweite_median": 0, "reichweite_summe": 0,
        "gespeichert": 0, "geteilt": 0, "kommentare": 0,
        "bester": None, "schwaechster": None,
        "umsatz": 0.0, "kaeufe": 0, "top_produkt": "",
        "kosten": None, "kosten_usd": 0.0, "gewinn": None,
        "follower_ende": None, "launches": [],
    })

    # --- Content
    if gepostet:
        je_monat = defaultdict(list)
        for b in gepostet.get("beitraege") or []:
            # 🚨 Alte Positionierung fliesst nicht in die Monatsauswertung —
            # sonst vergleicht sie Monate, in denen sie etwas anderes gemacht hat.
            if b.get("alte_positionierung"):
                continue
            if b.get("datum"):
                je_monat[b["datum"][:7]].append(b)
        for m, liste in je_monat.items():
            e = monate[m]
            e["beitraege"] = len(liste)
            e["reichweite_median"] = median([b.get("reach") or 0 for b in liste])
            e["reichweite_summe"] = sum(b.get("reach") or 0 for b in liste)
            e["gespeichert"] = sum(b.get("saved") or 0 for b in liste)
            e["geteilt"] = sum(b.get("shares") or 0 for b in liste)
            e["kommentare"] = sum(b.get("kommentare") or 0 for b in liste)
            nach = sorted(liste, key=lambda b: -(b.get("reach") or 0))
            def knapp(b):
                return {"datum": b.get("datum", ""), "reach": b.get("reach") or 0,
                        "rate": b.get("rate"), "anfang": (b.get("anfang") or "")[:88],
                        "link": b.get("link", "")}
            e["bester"] = knapp(nach[0])
            mitreich = [b for b in nach if (b.get("reach") or 0) > 0]
            if len(mitreich) > 1:
                e["schwaechster"] = knapp(mitreich[-1])

        # Follower-Stand je Abzug -> letzter bekannter Wert je Monat
        for handle, f in (gepostet.get("follower") or {}).items():
            for punkt in f.get("verlauf") or []:
                m = (punkt.get("stand") or "")[:7]
                if m:
                    monate[m]["follower_ende"] = punkt.get("wert")

    # --- Umsatz
    if umsatz:
        for m in umsatz.get("monate") or []:
            e = monate[m["monat"]]
            e["umsatz"] = m.get("umsatz") or 0
            e["kaeufe"] = m.get("kaeufe") or 0

    # --- Kosten und Gewinn
    # 🚨 `kosten` bleibt None, wo nichts erfasst ist — und dann gibt es auch
    # keinen Gewinn. Umsatz minus unvollstaendige Kosten ergaebe eine Zahl, die
    # aussieht wie ein Gewinn und zu hoch ist. Eine fehlende Zahl merkt man,
    # eine falsche nicht.
    if kosten:
        for k in kosten.get("monate") or []:
            e = monate[k["monat"]]
            e["kosten"] = k.get("chf") or 0
            e["kosten_usd"] = k.get("usd") or 0
            e["gewinn"] = round((e["umsatz"] or 0) - e["kosten"], 2)

    # --- Was laut Jahresplan in dem Monat lief
    if jahresplan:
        for eintr in jahresplan.get("eintraege") or []:
            if eintr.get("bereich") == "ferien":
                continue
            m = (eintr.get("start") or "")[:7]
            if m:
                monate[m]["launches"].append(eintr.get("name", "")[:60])

    # --- Zusammenstellen, jüngster zuerst
    # 🚨 Keine Monate aus der Zukunft. Der Jahresplan traegt Eintraege fuer
    # Oktober bis Dezember bei — die landeten als Zeilen mit lauter Nullen im
    # Rueckblick und sahen aus wie drei katastrophale Monate.
    schluessel = sorted([m for m in monate if m <= lauf], reverse=True)[:MONATE_ZURUECK]
    liste = []
    for m in schluessel:
        e = dict(monate[m])
        e["monat"] = m
        e["laeuft_noch"] = (m == lauf)
        liste.append(e)

    # --- Veränderung zum Vormonat, aber nur zwischen abgeschlossenen Monaten
    nach_m = {e["monat"]: e for e in liste}
    for e in liste:
        j, mm = e["monat"].split("-")
        vor = "%04d-%02d" % ((int(j), int(mm) - 1) if int(mm) > 1 else (int(j) - 1, 12))
        v = nach_m.get(vor)
        # 🚨 Kein Vergleich mit oder gegen den laufenden Monat.
        if v and not e["laeuft_noch"] and not v["laeuft_noch"]:
            e["vs_vormonat"] = {
                "umsatz": round(e["umsatz"] - v["umsatz"], 2),
                "reichweite_median": e["reichweite_median"] - v["reichweite_median"],
                "beitraege": e["beitraege"] - v["beitraege"],
            }

    daten = {
        "stand": heute.isoformat(),
        "laufender_monat": lauf,
        "monate": liste,
        "waehrung": (umsatz or {}).get("waehrung", "CHF"),
        # Nur die Kanaele, die sie wirklich bespielt — siehe Kopf.
        "kanaele": ["Instagram", "Newsletter", "Website"],
        "kosten_luecken": (kosten or {}).get("luecken") or [],
        "kosten_hinweis": (kosten or {}).get("hinweis", ""),
        "quellen": {
            "umsatz": "ThriveCart",
            "content": "Meta Graph API",
            "launches": "Jahresplan im Cockpit",
        },
        "gebaut": datetime.now().isoformat(timespec="seconds"),
    }

    (ziel / "monatsbogen.json").write_text(
        json.dumps(daten, ensure_ascii=False, indent=2), encoding="utf-8")

    print("  %d Monate gerechnet" % len(liste))
    print()
    print("  %-9s %9s %6s %8s %9s %s"
          % ("Monat", "Umsatz", "Käufe", "Beiträge", "Reichw.", ""))
    for e in liste:
        print("  %-9s %9.2f %6d %8d %9d %s"
              % (e["monat"], e["umsatz"], e["kaeufe"], e["beitraege"],
                 e["reichweite_median"], "← läuft noch" if e["laeuft_noch"] else ""))
    print("\nAbgelegt in: %s" % (ziel / "monatsbogen.json"))


if __name__ == "__main__":
    main()
