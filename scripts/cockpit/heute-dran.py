"""Heute dran — die Liste von Mein Tisch als Telegram-Nachricht (03.11.2026).

Patricia: *„wie können wir gewährleisten, dass mir die dinge aufploppen?“* Im Cockpit
steht die Liste ganz oben auf Mein Tisch (`heutedran.js`). Dieses Skript baut daraus
die Nachricht für den Morgen (07:00) und die kurze Erinnerung am Abend (20:00).
Es läuft in der Cloud-Routine „Cockpit: Heute dran (Telegram)“, Auftrag
`reference/scheduled-task-heute-dran.md`.

🚨 Dieselbe Logik wie `heutedran.js` — wer dort eine Quelle ändert, zieht sie hier nach.
   Bewusst nicht dabei: die Beiträge, die auf sie warten. Das rechnet nur das Cockpit
   (`wasFehlt()`), die Cloud müsste sonst fünf Sammlungen lesen.

Eingang: der Ordner, in den die Routine mit `ArtifactData get … out_dir` die Dokumente
legt — `<ordner>/daten/aufgaben.json`, `termine.json`, `rising-leaders.json`,
`wochenbogen-notizen.json`, `tagebuch.json`. Fehlt eins, fällt der Teil still weg.

    python3 scripts/cockpit/heute-dran.py --ordner /tmp/hd [--abend] [--datei /tmp/hd.txt]

Ohne offenen Punkt schreibt das Skript nichts und endet mit Code 3 — dann wird nichts
geschickt. Ein tägliches „heute nichts“ wischt man weg, und dann auch das, was zählt.
"""

import argparse
import datetime as dt
import json
import pathlib
import re
import sys
from zoneinfo import ZoneInfo

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HIER = pathlib.Path(__file__).resolve().parent
COCKPIT = "https://claude.ai/artifact/WWF7EWhCiAf2cVi1vytGFM"


def lies(ordner, name):
    p = ordner / "daten" / (name + ".json")
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {}


def lies_ti(ordner):
    p = ordner / "doterra-wissen" / "team-impulse.json"
    try:
        return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
    except Exception:
        return {}


def abschluss_ids():
    # Die Punkte des Monatsabschlusses stehen nur in tagesrunde.js — dort lesen statt abschreiben.
    t = (HIER / "tagesrunde.js").read_text(encoding="utf-8")
    block = t[t.index("TR_ABSCHLUSS = ["):]
    block = block[:block.index("];")]
    return re.findall(r'id: "([a-z-]+)"', block)


def kw(d):
    j, w, _ = d.isocalendar()
    return "%d-KW%02d" % (j, w)


def punkte(ordner, jetzt, abend):
    heute = jetzt.date()
    iso = heute.isoformat()
    tag = heute.isoweekday() % 7          # Sonntag = 0 wie in JS
    P = []

    tm = [t for t in lies(ordner, "termine").get("items", []) if t.get("datum") == iso]
    tm.sort(key=lambda t: t.get("zeit") or "99")
    if tm and not abend:
        P.append("📅 " + " · ".join(((t.get("zeit") + " ") if t.get("zeit") else "") + (t.get("titel") or "") for t in tm))

    T = (lies(ordner, "tagebuch").get("tage") or {}).get(iso, {})
    if abend:
        if not (T.get("learning") or "").strip() or not (T.get("morgen") or "").strip():
            P.append("✍️ Dein Tag in zwei Sätzen: was du geschafft hast und was morgen das Wichtigste ist")
    elif (T.get("fokus") or "").strip():
        P.append("🎯 Dein Fokus heute: " + T["fokus"].strip())
    else:
        P.append("✍️ Was ist heute dein Fokus?")

    w_tag = heute + dt.timedelta(days=1) if (tag == 0 and jetzt.hour >= 15) else heute
    wn = lies(ordner, "wochenbogen-notizen").get("werte") or {}
    if not ((wn.get(kw(w_tag)) or {}).get("fokus") or "").strip() and (tag != 0 or jetzt.hour >= 15):
        P.append("✍️ Fokus der Woche fehlt noch")

    r = lies(ordner, "rising-leaders")
    t = (r.get("tagesrunde") or {}).get(iso, {})
    n = sum(1 for k in ("biz", "person", "kundin") if t.get(k))
    if n < 3:
        P.append("🌿 doTERRA-Tagesrunde %d/3" % n)
    # Fürs Team: Montag eine Aufgabe, Donnerstag ein Impuls (dieselbe Regel wie tiImpulsOffen in teamimpuls.js).
    grenze = (heute - dt.timedelta(days=3)).isoformat()
    stand = r.get("impulse") or {}
    for x in lies_ti(ordner).get("items", []):
        if grenze <= x.get("datum", "") <= iso and not (stand.get(x.get("id")) or {}).get("verschickt"):
            P.append("🌿 Team-%s schicken: %s" % ("Aufgabe" if x.get("art") == "aufgabe" else "Impuls", x.get("titel") or ""))
    if heute.day >= 24:
        ids = abschluss_ids()
        A = (r.get("abschluss") or {}).get(iso[:7], {})
        fertig = sum(1 for i in ids if A.get(i))
        if fertig < len(ids):
            P.append("🌿 Monatsabschluss %d/%d — am Ersten fällt das Volumen auf null" % (fertig, len(ids)))

    if not abend:
        af = [a for a in lies(ordner, "aufgaben").get("items", [])
              if not a.get("erledigt") and a.get("bereich") != "Privat"]
        for a in [a for a in af if a.get("datum") == iso][:3]:
            P.append("☑️ " + (a.get("aufgabe") or "Aufgabe"))
        ueber = [a for a in af if a.get("datum") and a["datum"] < iso]
        if ueber:
            P.append("☑️ %d Aufgaben überfällig" % len(ueber))
    return P


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ordner", required=True)
    ap.add_argument("--abend", action="store_true")
    ap.add_argument("--datei")
    ap.add_argument("--jetzt", help="zum Testen, z. B. 2026-11-03T07:00")
    a = ap.parse_args()

    zone = ZoneInfo("Europe/Zurich")
    jetzt = dt.datetime.fromisoformat(a.jetzt).replace(tzinfo=zone) if a.jetzt else dt.datetime.now(zone)
    P = punkte(pathlib.Path(a.ordner), jetzt, a.abend)
    # Nur Info-Zeilen (Termin, Fokus) sind kein Grund für eine Nachricht.
    offen = [p for p in P if not p.startswith(("📅", "🎯"))]
    if not offen:
        print("Nichts offen — keine Nachricht.")
        sys.exit(3)

    kopf = "Noch offen für heute:" if a.abend else "Heute dran:"
    text = kopf + "\n\n" + "\n".join(P) + "\n\nIm Cockpit: " + COCKPIT
    if a.datei:
        pathlib.Path(a.datei).write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
