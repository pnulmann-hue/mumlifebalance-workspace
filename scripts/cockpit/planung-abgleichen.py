"""Hängt an jeden Planungs-Eintrag einen Beleg aus dem Workspace — oder keinen.

Patricia am 24.09.2026: *„kannst du bitte auch den bereich planung mit den daten
aus dem workspace abgleichen? in notion waren teilweise inhalte veraltet"*.

**Der Jahresplan und die Ziele kamen einmalig aus Notion.** Dort stand, was
geplant war — nicht, was daraus geworden ist. Beim ersten Blick trug **kein
einziger** der 54 Einträge einen Status.

🚨 **Belegen, nicht abhaken.** Dieses Skript setzt keinen Haken. Es sucht je
Eintrag nach Spuren im Workspace und hängt sie an; was daraus folgt, entscheidet
Patricia. Ein Haken, den eine Maschine gesetzt hat, ist derselbe Fehler wie ein
fehlender — dieselbe Regel wie in `aufgaben-abgleichen.py`.

**Wo gesucht wird, in dieser Reihenfolge:**

| Quelle | was sie beweist |
|---|---|
| `outputs/produkte/<slug>/` | das Produkt wurde gebaut |
| `context/active-funnels.json` | der Funnel läuft |
| `outputs/cockpit/abgleich/katalog.json` | die Kasse steht (mit Status) |
| `plans/*.md` | es wurde geplant |
| `outputs/**` sonst | irgendetwas ist entstanden |

**Drei Befunde, nicht zwei:**

| | |
|---|---|
| **belegt** | es gibt Spuren, und der Eintrag ist vorbei oder läuft |
| **offen** | es gibt Spuren, aber der Termin liegt noch vorn |
| **keine Spur** | nichts gefunden — **Verdacht**, kein Urteil |

🚨 **„Keine Spur" heisst nicht „nicht passiert".** Ein Leadmagnet kann in
ManyChat leben, ohne je eine Datei zu bekommen. Der Befund ist eine Frage an
Patricia, und der Text im Cockpit sagt das.

🚨 **Namensabgleich mit Umschrift und Mindest-Deckung.** ä→ae vor dem Filtern,
sonst gilt „für" als etwas anderes als „fuer"; und mindestens **zwei** gemeinsame
Wörter, sonst passt „Minikurs" auf alles. Beides schon einmal gelernt — beim
Download-Aufräumen und in der Link-Zentrale.

    python scripts/cockpit/planung-abgleichen.py [--zeigen]

Danach: ArtifactData update → "daten"/"jahresplan" bzw. "ziele".
"""

import datetime
import json
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]
ABGLEICH = ROOT / "outputs" / "cockpit" / "abgleich"

# Wörter, die überall vorkommen und deshalb nichts unterscheiden.
STOPP = {"der", "die", "das", "und", "fuer", "mit", "von", "zum", "zur", "ein",
         "eine", "einen", "dein", "deine", "mehr", "als", "aus", "auf", "ins",
         "launch", "zyklus", "runde", "phase", "minikurs", "leadmagnet",
         "workbook", "mentoring", "doterra", "neu", "start"}


def umschrift(t):
    for a, b in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss")):
        t = t.replace(a, b).replace(a.upper(), b)
    return t.lower()


def woerter(t):
    return {w for w in re.findall(r"[a-z0-9]{4,}", umschrift(t))
            if w not in STOPP}


def deckung(a, b):
    """Gemeinsame Wörter — mindestens zwei, sonst ist es Zufall."""
    return len(woerter(a) & woerter(b))


def belegquellen():
    q = []

    # 1 · Gebaute Produkte
    pd = ROOT / "outputs" / "produkte"
    if pd.is_dir():
        for o in pd.iterdir():
            if o.is_dir() and not o.name.startswith("_"):
                n = len(list(o.rglob("*")))
                q.append({"art": "Produkt gebaut", "text": o.name,
                          "wo": "outputs/produkte/%s (%d Dateien)" % (o.name, n)})

    # 2 · Laufende Funnels
    fp = ROOT / "context" / "active-funnels.json"
    if fp.exists():
        d = json.load(open(fp, encoding="utf-8"))
        for f in (d if isinstance(d, list) else d.get("funnels", [])):
            if not isinstance(f, dict):
                continue
            q.append({"art": "Funnel aktiv",
                      "text": (f.get("name") or f.get("slug") or ""),
                      "wo": "active-funnels.json"})

    # 3 · Checkouts mit Status — der sagt am meisten
    kp = ABGLEICH / "katalog.json"
    if kp.exists():
        d = json.load(open(kp, encoding="utf-8"))
        for g in (d.get("gruppen") or d.get("kategorien") or []):
            for a in (g.get("angebote") or []):
                q.append({"art": "Checkout " + (a.get("status") or "?"),
                          "text": a.get("name", ""),
                          "wo": "ThriveCart · %s" % (a.get("status") or "?")})
        for a in (d.get("angebote") or []):
            q.append({"art": "Checkout " + (a.get("status") or "?"),
                      "text": a.get("name", ""),
                      "wo": "ThriveCart · %s" % (a.get("status") or "?")})

    # 4 · Pläne
    pp = ROOT / "plans"
    if pp.is_dir():
        for f in pp.glob("*.md"):
            q.append({"art": "Plan", "text": f.stem, "wo": "plans/" + f.name})

    return [x for x in q if x["text"]]


def suchen(name, quellen):
    treffer = []
    for q in quellen:
        d = deckung(name, q["text"])
        if d >= 2:
            treffer.append((d, q))
    treffer.sort(key=lambda x: -x[0])
    return [{"art": q["art"], "wo": q["wo"], "deckung": d}
            for d, q in treffer[:4]]


TERMIN_WORTE = ("ferien", "convention", "event", "messe", "geburtstag",
                "feiertag", "urlaub", "weihnacht")


def ist_termin(e):
    """🚨 Ferien und Conventions hinterlassen nie eine Workspace-Spur.

    Beim ersten Lauf standen „Sportferien Kids", „Fruehlingsferien" und
    „Convention doTERRA" unter „keine Spur" — als waere dort etwas versaeumt
    worden. Ein Termin ist aber kein Vorhaben, und Laerm in einer Befundliste
    kostet das Vertrauen in die ganze Liste.
    """
    if (e.get("bereich") or "").lower() == "ferien":
        return True
    t = umschrift(e.get("name") or "")
    return any(w in t for w in TERMIN_WORTE)


def quartal_vorbei(q, heute):
    """Q1 endet am 31.3., Q2 am 30.6., Q3 am 30.9., Q4 am 31.12."""
    enden = {"Q1": "-03-31", "Q2": "-06-30", "Q3": "-09-30", "Q4": "-12-31"}
    if q not in enden:
        return False
    return heute[:4] + enden[q] < heute


def ziel_befund(e, heute):
    """🚨 Ein Ziel belegt man mit Zahlen, nicht mit Dateien.

    Beim ersten Lauf standen 10 von 11 Zielen unter „keine Spur" - darunter
    „40000 Umsatz mit Mumlifebalance". Ein Umsatzziel hat natuerlich keinen
    Produktordner. Der Abgleich war die falsche Frage, und eine Befundliste,
    die fast alles beanstandet, liest niemand zweimal.

    Maschinell pruefbar ist etwas anderes: ob das Quartal vorbei ist, waehrend
    das Ziel noch auf „Aktiv" steht. Genau das ist die Veraltung - Q2-Ziele
    standen Ende September noch als aktiv da.
    """
    q = (e.get("quartal") or "").upper()
    st = (e.get("status") or "").lower()
    if q and quartal_vorbei(q, heute) and st in ("aktiv", "offen", "laeuft"):
        return "abgelaufen"
    return "nicht_messbar"


def main():
    heute = datetime.date.today().isoformat()
    quellen = belegquellen()
    bericht = {}

    for name, feld in (("jahresplan", "eintraege"), ("ziele", "items")):
        p = ABGLEICH / (name + ".json")
        if not p.exists():
            continue
        d = json.load(open(p, encoding="utf-8"))
        eintraege = d.get(feld) or []
        zahlen = {"belegt": 0, "offen": 0, "keine_spur": 0,
                  "termin": 0, "abgelaufen": 0, "nicht_messbar": 0}

        for e in eintraege:
            titel = e.get("name") or e.get("titel") or ""
            spuren = suchen(titel, quellen)
            e["belege"] = spuren
            start = e.get("start") or e.get("faellig") or ""
            kuenftig = bool(start and start > heute)
            if name == "ziele":
                e["befund"] = ziel_befund(e, heute)
            elif name == "jahresplan" and ist_termin(e):
                e["befund"] = "termin"
            elif spuren and not kuenftig:
                e["befund"] = "belegt"
            elif kuenftig:
                e["befund"] = "offen"
            else:
                # 🚨 Verdacht, kein Urteil — siehe Kopf des Skripts.
                e["befund"] = "keine_spur"
            zahlen[e["befund"]] += 1

        d["abgeglichen"] = heute
        d["abgleich_zahlen"] = zahlen
        # 🚨 Deutsche Anführungszeichen paarweise: das schliessende " ist ein
        # ganz normales ASCII-Zeichen und beendet den String. Also „…“ mit
        # typografischem Schlusszeichen, nie „…".
        d["abgleich_hinweis"] = (
            "Belege aus dem Workspace, automatisch gesucht. „Keine Spur“ heisst "
            "NICHT „nicht passiert“ — ein Leadmagnet kann in ManyChat leben, ohne "
            "je eine Datei zu bekommen. Der Befund ist eine Frage, kein Urteil.")
        p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
        bericht[name] = (zahlen, eintraege)

        teile = [k + " " + str(v) for k, v in zahlen.items() if v]
        print("%-11s %d Einträge  ·  %s" % (name, len(eintraege), " · ".join(teile)))

    print("\nBelegquellen durchsucht: %d" % len(quellen))

    if "--zeigen" in sys.argv:
        for name, (z, eintraege) in bericht.items():
            interessant = ("abgelaufen" if name == "ziele" else "keine_spur")
            ohne = [e for e in eintraege if e.get("befund") == interessant]
            if not ohne:
                continue
            print("\n--- %s · keine Spur im Workspace (%d) ---" % (name, len(ohne)))
            for e in sorted(ohne, key=lambda x: x.get("start") or "")[:16]:
                print("  %s  %s" % ((e.get("start") or "—")[:10],
                                    (e.get("name") or e.get("titel") or "")[:62]))


if __name__ == "__main__":
    main()
