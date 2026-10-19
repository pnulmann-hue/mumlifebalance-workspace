"""Verbindet freigegebene Cockpit-Beiträge mit den echten Instagram-Posts.

Patricia am 24.09.2026: *„Ich prüfe, gebe frei und sie rutschen dann weiter in
den nächsten Reiter freigegeben und sobald sie auf insta gepostet sind, rutschen
sie auf gepostet. Die auswertung kannst du dann ja da pro Post machen. Alle, die
gut liefen, kommen dann auf eine Liste nach 4 Wochen erneut einplanen für
contentrecycling"*.

**Das Fliessband hat vier Stationen, und drei gab es schon:**

| Station | im Cockpit | woher |
|---|---|---|
| Planen | Wochen-Vorschau | Sammlung `reels` / `karussells` / `storys` |
| Freigegeben | Freigeben-Reiter | Sammlung `freigaben` |
| **Gepostet** | Gepostet & Analyse | Meta Graph API |
| Recycling | Knopf „Nochmal bringen" | dieselben Zahlen, ab 28 Tagen |

🚨 **Gefehlt hat die Verbindung zwischen Station 2 und 3.** Das sind zwei
getrennte Welten: hier die Beiträge, die Patricia gebaut hat, dort 541
Instagram-Posts aus der API. Nichts rutscht weiter, weil niemand weiss, dass
Beitrag X und Post Y dasselbe sind.

**Zugeordnet wird über den Caption-Anfang**, nicht über das Datum: die API gibt
je Post `anfang` (die ersten rund 90 Zeichen der Caption) heraus, und die ist
wörtlich dieselbe wie im Cockpit. Das Datum dient nur als Gegenprobe.

🚨 **Normalisiert wird mit Umschrift, nicht mit Wegwerfen.** `re.sub(r"[^a-z0-9]",
"", …)` macht aus „für" ein „fr" und aus „fuer" etwas anderes — dann gilt
dieselbe Caption als zwei verschiedene. Erst ä→ae, ö→oe, ü→ue, ß→ss, dann
filtern. Gilt für jeden Namensvergleich in diesem Workspace.

🚨 **Sternchen und Leerzeichen fallen raus.** Im Cockpit steht
`Kommentier **STANDBEIN**`, Instagram liefert `Kommentier STANDBEIN`. Ohne das
findet der Abgleich genau die Lead-Posts nicht — also die, auf die es ankommt.

🚨 **Das doTERRA-Konto hängt nicht an der API.** Für dessen Beiträge kann es
keine Zuordnung geben, und das Skript sagt es, statt sie stillschweigend als
„nicht gepostet" zu führen. Eine fehlende Zuordnung heisst dort **nicht**, dass
nichts rausging.

    python scripts/cockpit/gepostet-zuordnen.py [--zeigen]

Danach: ArtifactData set → Sammlung "daten", Dokument "gepostet-zuordnung".
"""

import glob
import json
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]
ROH = ROOT / "outputs" / "cockpit" / "inhalte-roh"
INSIGHTS = ROOT / "outputs" / "instagram-insights"
ZIEL = ROOT / "outputs" / "cockpit" / "abgleich" / "gepostet-zuordnung.json"

# Wie viele Zeichen des Caption-Anfangs verglichen werden. Die API liefert rund
# 90; kuerzer als 40 wird es mehrdeutig, laenger als 60 schlaegt jede kleine
# Korrektur im Cockpit durch.
LAENGE = 55


def umschrift(t: str) -> str:
    """ä→ae … und dann nur Buchstaben und Ziffern. Siehe Kopf des Skripts."""
    for a, b in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss"),
                 ("Ä", "ae"), ("Ö", "oe"), ("Ü", "ue")):
        t = t.replace(a, b)
    return re.sub(r"[^a-z0-9]", "", t.lower())


def schluessel(text: str) -> str:
    return umschrift(text or "")[:LAENGE]


def instagram_posts():
    """Alle Abzuege lesen, je Post den zuletzt gesehenen Stand behalten."""
    posts = {}
    konten = {}
    for p in sorted(glob.glob(str(INSIGHTS / "*.json"))):
        d = json.load(open(p, encoding="utf-8"))
        for k in d.get("konten", []):
            konten[k.get("handle", "?")] = True
            for b in k.get("beitraege", []):
                b = dict(b)
                b["konto"] = k.get("handle", "")
                b["stand"] = d.get("stand", "")
                posts[b["id"]] = b
    return posts, sorted(konten)


def main():
    if not ROH.joinpath("freigaben").is_dir():
        sys.exit("🚨 outputs/cockpit/inhalte-roh/freigaben fehlt — erst mit "
                 "ArtifactData list holen.")

    posts, konten = instagram_posts()
    nach_schluessel = {}
    for b in posts.values():
        s = schluessel(b.get("anfang", ""))
        if s:
            nach_schluessel.setdefault(s, []).append(b)

    zuordnung, offen, nicht_pruefbar = {}, [], []
    for datei in sorted(ROH.glob("freigaben/*.json")):
        f = json.load(open(datei, encoding="utf-8"))
        bid = datei.stem
        if f.get("status") == "zurueckgezogen":
            continue
        s = schluessel(f.get("caption", ""))
        treffer = nach_schluessel.get(s, [])
        if treffer:
            b = treffer[0]
            zuordnung[bid] = {
                "igId": b["id"], "link": b.get("link", ""),
                "datum": b.get("datum", ""), "typ": b.get("typ", ""),
                "reach": b.get("reach"), "likes": b.get("likes"),
                "kommentare": b.get("kommentare"), "saved": b.get("saved"),
                "shares": b.get("shares"),
                "interaktionen": b.get("total_interactions"),
                "stand": b.get("stand", ""),
            }
            # 🚨 Gegenprobe ueber das Datum: weicht es um mehr als drei Tage ab,
            # ist es vermutlich ein Recycling desselben Textes, kein Treffer.
            if f.get("datum") and b.get("datum"):
                if abs(_tage(f["datum"]) - _tage(b["datum"])) > 3:
                    zuordnung[bid]["unsicher"] = "Datum weicht ab"
        elif (f.get("profil") or "") == "doterra":
            nicht_pruefbar.append((bid, f.get("datum", ""), f.get("name", "")))
        else:
            offen.append((bid, f.get("datum", ""), f.get("name", "")))

    # 🚨 Seit 16.10.2026 auch Beiträge OHNE Freigabe (Patricia postet B-Roll und
    # manchmal ganze Beiträge selbst in der App). Sonst fehlt im Content-Kalender
    # genau das, was sie von Hand rausgeschickt hat.
    belegt = {z["igId"] for z in zuordnung.values()}
    for sammlung in ("reels", "karussells"):
        for datei in sorted(ROH.glob(sammlung + "/*.json")):
            bid = datei.stem
            if bid in zuordnung:
                continue
            o = json.load(open(datei, encoding="utf-8"))
            s = schluessel(o.get("caption", ""))
            treffer = [b for b in nach_schluessel.get(s, []) if b["id"] not in belegt] if s else []
            if not treffer:
                continue
            b = treffer[0]
            belegt.add(b["id"])
            zuordnung[bid] = {
                "igId": b["id"], "link": b.get("link", ""),
                "datum": b.get("datum", ""), "typ": b.get("typ", ""),
                "reach": b.get("reach"), "likes": b.get("likes"),
                "kommentare": b.get("kommentare"), "saved": b.get("saved"),
                "shares": b.get("shares"),
                "interaktionen": b.get("total_interactions"),
                "stand": b.get("stand", ""), "ohne_freigabe": True,
            }
            if o.get("datum") and b.get("datum") and abs(_tage(o["datum"]) - _tage(b["datum"])) > 3:
                zuordnung[bid]["unsicher"] = "Datum weicht ab"

    # Zweiter Durchgang, unschärfer: Patricia passt Captions vor dem Posten oft
    # noch an, dann stimmt der Anfang nicht mehr wörtlich. Gleiches Datum (±1 Tag),
    # gleiches Format und mindestens 40 % gemeinsame Wörter im Anfang reichen dann.
    def woerter(t):
        return set(w for w in re.findall(r"[a-zäöüß]{4,}", (t or "").lower()))
    kandidaten = []
    for sammlung, fmt in (("reels", "REELS"), ("karussells", "FEED")):
        for datei in sorted(ROH.glob(sammlung + "/*.json")):
            bid = datei.stem
            if bid in zuordnung:
                continue
            o = json.load(open(datei, encoding="utf-8"))
            f = {}
            fp = ROH / "freigaben" / (bid + ".json")
            if fp.exists():
                f = json.load(open(fp, encoding="utf-8"))
            datum = f.get("datum") or o.get("datum")
            if not datum or (o.get("profil") or f.get("profil")) == "doterra":
                continue
            text = " ".join([o.get("hook") or "", o.get("caption") or "", f.get("caption") or ""])
            kandidaten.append((bid, datum, fmt, woerter(text[:400])))
    for b in posts.values():
        if b["id"] in belegt or not b.get("datum") or _tage(b["datum"]) < _tage(_heute()) - 60:
            continue
        wb = woerter(b.get("caption") or b.get("anfang") or "")
        best, wert = None, 0.0
        for bid, datum, fmt, w in kandidaten:
            if bid in zuordnung or fmt != b.get("typ") or abs(_tage(datum) - _tage(b["datum"])) > 1 or not w or not wb:
                continue
            j = len(w & wb) / max(1, min(len(w), len(wb)))
            if j > wert:
                best, wert = bid, j
        if best and wert >= 0.4:
            belegt.add(b["id"])
            zuordnung[best] = {
                "igId": b["id"], "link": b.get("link", ""),
                "datum": b.get("datum", ""), "typ": b.get("typ", ""),
                "reach": b.get("reach"), "likes": b.get("likes"),
                "kommentare": b.get("kommentare"), "saved": b.get("saved"),
                "shares": b.get("shares"),
                "interaktionen": b.get("total_interactions"),
                "stand": b.get("stand", ""), "unscharf": round(wert, 2),
            }

    # Die Instagram-Posts der letzten 21 Tage — für den Rückblick im
    # Content-Kalender: was ist wirklich rausgegangen, auch Spontanes.
    rueck = {}
    for bid, z in zuordnung.items():
        rueck[z["igId"]] = bid
    grenze = _tage(_heute()) - 21
    letzte = []
    for b in posts.values():
        if not b.get("datum") or _tage(b["datum"]) < grenze:
            continue
        reach = b.get("reach") or 0
        inter = b.get("total_interactions")
        if not isinstance(inter, (int, float)):
            inter = sum(b.get(k) or 0 for k in ("likes", "kommentare", "saved", "shares"))
        letzte.append({
            "igId": b["id"], "link": b.get("link", ""), "datum": b["datum"],
            "zeitpunkt": b.get("zeitpunkt", ""), "typ": b.get("typ", ""),
            "medientyp": b.get("medientyp", ""), "anfang": (b.get("anfang") or "")[:90],
            "reach": b.get("reach"), "saved": b.get("saved"), "shares": b.get("shares"),
            "kommentare": b.get("kommentare"),
            "rate": round(100 * inter / reach, 2) if reach else None,
            "reif": _tage(_heute()) - _tage(b["datum"]) >= 7,
            "beitrag": rueck.get(b["id"]), "stand": b.get("stand", ""),
        })
    letzte.sort(key=lambda x: x.get("zeitpunkt") or x["datum"])

    ergebnis = {
        "stand": _heute(),
        "konten_mit_api": konten,
        "zuordnung": zuordnung,
        "letzte_posts": letzte,
        "nicht_pruefbar": [{"id": a, "datum": b, "name": c}
                           for a, b, c in nicht_pruefbar],
        "ohne_treffer": [{"id": a, "datum": b, "name": c}
                         for a, b, c in offen if a not in zuordnung],
    }
    ZIEL.parent.mkdir(parents=True, exist_ok=True)
    ZIEL.write_text(json.dumps(ergebnis, ensure_ascii=False, indent=1),
                    encoding="utf-8")

    print("Instagram-Posts gelesen: %d  (Konten mit API: %s)"
          % (len(posts), ", ".join(konten) or "keine"))
    print("Zugeordnet:      %d" % len(zuordnung))
    print("Nicht prüfbar:   %d  (doTERRA — Konto hängt nicht an der API)"
          % len(nicht_pruefbar))
    print("Ohne Treffer:    %d" % len(offen))
    print("→ %s" % ZIEL)

    if "--zeigen" in sys.argv:
        print("\n--- zugeordnet ---")
        for bid, z in sorted(zuordnung.items(), key=lambda x: x[1]["datum"]):
            warn = "  ⚠️ " + z["unsicher"] if z.get("unsicher") else ""
            print("  %s  %-22s reach=%-5s %s%s"
                  % (z["datum"], bid, z.get("reach"), z.get("typ", ""), warn))
        if offen:
            print("\n--- ohne Treffer (Mentoring) ---")
            for bid, d, n in offen:
                print("  %s  %-22s %s" % (d or "—", bid, n[:40]))
        if nicht_pruefbar:
            print("\n--- doTERRA, nicht prüfbar ---")
            for bid, d, n in nicht_pruefbar:
                print("  %s  %-22s %s" % (d or "—", bid, n[:40]))


def _tage(iso):
    import datetime
    return datetime.date(*map(int, iso.split("-"))).toordinal()


def _heute():
    import datetime
    return datetime.date.today().isoformat()


if __name__ == "__main__":
    main()
