"""Schritt 2b des Einplan-Laufs als festes Skript (seit 2026-10-29).

Vorher hat der Task `freigaben-einplanen-2000` diesen Schritt jedes Mal mit einem
selbst getippten `cd … && python -c …` gemacht. Der Befehl war nicht freigegeben,
der Lauf blieb an der Rückfrage hängen, und vom 26. bis 29.10. ging nichts raus.
`python scripts/cockpit/*` ist freigegeben, also läuft dieses Skript ohne Rückfrage.

    python scripts/cockpit/freigabe-nachruecken.py --ordner outputs/cockpit/freigaben/<id> [--belegt <ordner>] [--trocken]

Liest  <ordner>/freigaben/<id>.json (die Steuerdatei, wie ArtifactData sie ablegt).
--belegt  Ordner mit karussells/*.json und reels/*.json aus dem Cockpit (ArtifactData
          list mit out_dir). Ohne ihn wird nur nach Wochentag nachgerückt, nicht nach
          freien Tagen.

Entscheidet, in dieser Reihenfolge:
  1. Schon auf Instagram?  Caption-Anfang gegen den neuesten Abzug in
     outputs/instagram-insights/ (nur Mentoring, doTERRA hängt nicht an der API).
     -> aktion "gepostet", Steuerdatei bleibt unverändert.
  2. Zeitpunkt mindestens eine Stunde voraus?  -> aktion "unveraendert".
  3. Neueres, zukünftiges Datum im Beitrag selbst?  -> dieses nehmen.
  4. Sonst nächster freier Platz: Mo/Mi/Fr Reel, Di/Do Karussell, Sa/So beides,
     Tag beim Profil frei, höchstens 28 Tage. Die Uhrzeit bleibt.
  -> aktion "nachgerueckt", Steuerdatei bekommt datum, zeitpunktISO und nachgerueckt.von.

Gibt zum Schluss genau eine Zeile JSON aus, die der Task liest.
"""
import argparse
import glob
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone

try:
    from zoneinfo import ZoneInfo
    ZH = ZoneInfo("Europe/Zurich")
except Exception:  # Windows ohne tzdata
    ZH = None

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REEL_TAGE = {0, 2, 4, 5, 6}
KAR_TAGE = {1, 3, 5, 6}


def umschrift(t):
    t = (t or "").lower()
    for a, b in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss")):
        t = t.replace(a, b)
    return re.sub(r"[^a-z0-9]", "", t)


def lies(p):
    with open(p, encoding="utf-8") as f:
        d = json.load(f)
    return d.get("data", d) if isinstance(d.get("data"), dict) else d


def zu_utc(datum, zeit):
    lokal = datetime.strptime(f"{datum} {zeit}", "%Y-%m-%d %H:%M")
    if ZH:
        return lokal.replace(tzinfo=ZH).astimezone(timezone.utc)
    # Rückfall: Sommerzeit letzter So im März bis letzter So im Oktober
    j = lokal.year
    def letzter_sonntag(m):
        d = datetime(j, m + 1, 1) - timedelta(days=1) if m < 12 else datetime(j, 12, 31)
        return d - timedelta(days=(d.weekday() + 1) % 7)
    sommer = letzter_sonntag(3).replace(hour=2) <= lokal < letzter_sonntag(10).replace(hour=3)
    return (lokal - timedelta(hours=2 if sommer else 1)).replace(tzinfo=timezone.utc)


def schon_gepostet(fg):
    if fg.get("profil", "mentoring") != "mentoring":
        return None, "nicht pruefbar (doTERRA hängt nicht an der API)"
    abzuege = sorted(glob.glob(os.path.join(ROOT, "outputs", "instagram-insights", "20*.json")))
    if not abzuege:
        return None, "kein Instagram-Abzug gefunden"
    with open(abzuege[-1], encoding="utf-8") as f:
        ig = json.load(f)
    kopf = umschrift(fg.get("caption", ""))[:60]
    if len(kopf) < 20:
        return None, "Caption zu kurz zum Vergleichen"
    for konto in ig.get("konten", []):
        for b in konto.get("beitraege", []):
            text = umschrift(b.get("caption") or b.get("anfang") or "")
            if text and (text.startswith(kopf) or kopf.startswith(text[:60])):
                return b, os.path.basename(abzuege[-1])
    return False, os.path.basename(abzuege[-1])


def belegte_tage(ordner, profil, eigene_id, freigaben_ordner):
    tage = set()
    # Andere Freigaben desselben Laufs liegen als Nachbarordner daneben. Ihr Datum
    # zählt mit, sonst rücken zwei Karussells auf denselben Tag (gefunden beim ersten Test).
    for p in glob.glob(os.path.join(os.path.dirname(os.path.abspath(freigaben_ordner)), "*", "freigaben", "*.json")):
        if os.path.splitext(os.path.basename(p))[0] == eigene_id:
            continue
        try:
            b = lies(p)
        except Exception:
            continue
        if (b.get("profil") or "mentoring") == profil and b.get("datum") and b.get("status") != "gepostet-von-hand":
            tage.add(b["datum"][:10])
    if not ordner:
        return tage
    for art in ("karussells", "reels"):
        for p in glob.glob(os.path.join(ordner, art, "*.json")):
            if os.path.splitext(os.path.basename(p))[0] == eigene_id:
                continue
            try:
                b = lies(p)
            except Exception:
                continue
            if b.get("abgelehnt") or not b.get("datum"):
                continue
            if (b.get("profil") or "mentoring") == profil:
                tage.add(b["datum"][:10])
    return tage


def beitrag_datum(ordner, eigene_id):
    if not ordner:
        return None
    for art in ("karussells", "reels"):
        p = os.path.join(ordner, art, f"{eigene_id}.json")
        if os.path.exists(p):
            return (lies(p).get("datum") or "")[:10] or None
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ordner", required=True)
    ap.add_argument("--belegt")
    ap.add_argument("--trocken", action="store_true")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    dateien = glob.glob(os.path.join(a.ordner, "freigaben", "*.json"))
    if len(dateien) != 1:
        print(json.dumps({"aktion": "fehler", "grund": f"{len(dateien)} Steuerdateien in {a.ordner}/freigaben"}))
        sys.exit(1)
    pfad = dateien[0]
    fid = os.path.splitext(os.path.basename(pfad))[0]
    with open(pfad, encoding="utf-8") as f:
        roh = json.load(f)
    fg = roh.get("data", roh) if isinstance(roh.get("data"), dict) else roh

    treffer, quelle = schon_gepostet(fg)
    if treffer:
        print(json.dumps({"aktion": "gepostet", "id": fid, "link": treffer.get("link"),
                          "datum": treffer.get("datum"), "quelle": quelle}, ensure_ascii=False))
        return

    jetzt = datetime.now(timezone.utc)
    zeit = fg.get("zeit") or "07:30"
    alt = fg.get("zeitpunktISO")
    if alt and datetime.fromisoformat(alt.replace("Z", "+00:00")) >= jetzt + timedelta(hours=1):
        print(json.dumps({"aktion": "unveraendert", "id": fid, "zeitpunktISO": alt,
                          "gepostet_pruefung": quelle}, ensure_ascii=False))
        return

    neu_datum = None
    wunsch = beitrag_datum(a.belegt, fid)
    if wunsch and zu_utc(wunsch, zeit) >= jetzt + timedelta(hours=1):
        neu_datum, weg = wunsch, "Datum aus dem Beitrag"
    else:
        tage = KAR_TAGE if fg.get("typ") == "karussell" else REEL_TAGE
        belegt = belegte_tage(a.belegt, fg.get("profil") or "mentoring", fid, a.ordner)
        heute = (jetzt.astimezone(ZH) if ZH else jetzt).date()
        for i in range(0, 29):
            d = heute + timedelta(days=i)
            ds = d.isoformat()
            if d.weekday() in tage and ds not in belegt and zu_utc(ds, zeit) >= jetzt + timedelta(hours=1):
                neu_datum, weg = ds, "nächster freier Platz"
                break
    if not neu_datum:
        print(json.dumps({"aktion": "kein-platz", "id": fid, "grund": "kein freier Platz in 28 Tagen"}, ensure_ascii=False))
        return

    iso = zu_utc(neu_datum, zeit).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    fg.update({"datum": neu_datum, "zeit": zeit, "zeitpunktISO": iso, "nachgerueckt": {"von": alt}})
    if not a.trocken:
        with open(pfad, "w", encoding="utf-8") as f:
            json.dump(roh, f, ensure_ascii=False, indent=2)
    print(json.dumps({"aktion": "nachgerueckt", "id": fid, "von": alt, "datum": neu_datum, "zeit": zeit,
                      "zeitpunktISO": iso, "weg": weg, "gepostet_pruefung": quelle,
                      "geschrieben": not a.trocken}, ensure_ascii=False))


if __name__ == "__main__":
    main()
