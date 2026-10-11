"""Was bei anderen überdurchschnittlich lief — als Ideen ins Cockpit.

Patricia am 24.09.2026: *„geil wäre auch noch einen ideekasten wo du ja meine
konkurrenzprofile scrapps nach beitragsideen, die gut performt sind. da wäre
dann ein reiter cool mit „fertig bauen" und dieser befehl löst dann aus, dass du
mir ein b-Roll, sprechreel oder kaurssell machst"*.

**Die Daten liegen längst da** — `scripts/apify/` scrapt täglich 16 Accounts mit
je 12 Beiträgen nach `outputs/apify-runs/`. Gefehlt hat nur, dass sie jemand
ansieht.

🚨 **Apify liefert keine Reichweite**, nur Likes und Kommentare. Absolute Zahlen
sind damit wertlos: ein Account mit 40'000 Followern hat immer mehr Likes als
einer mit 2'000, ohne dass der Beitrag besser wäre. Gemessen wird deshalb
**gegen den eigenen Median des Accounts** — genau wie bei Patricias eigenen
Beiträgen.

| Stufe | Bedingung |
|---|---|
| auffällig | ≥ 1,8× eigener Median |
| eingeschlagen | ≥ 3× eigener Median |

🚨 **Mindestbasis, sonst misst die Quote Zufall.** Unter **15 Interaktionen**
zählt ein Beitrag nicht, und ein Account braucht mindestens 6 Beiträge, damit
sein Median etwas heisst. Dieser Fehler ist mir am 24.09. bei Patricias eigenen
Zahlen zweimal passiert — hier ist er von Anfang an drin.

🚨 **Pinned Posts fallen raus.** Ein angehefteter Beitrag sammelt monatelang
Likes und steht damit immer oben, ohne dass sein Inhalt besser wäre.

🚨 **Die Hooks werden nicht kopiert.** Was hier steht, ist die *Mechanik* —
welche Frage, welches Format, welcher Winkel. Szene, Zahlen und Sprache kommen
aus Patricias Leben. Das steht auch im Bau-Auftrag, den der Knopf auslöst.

    python scripts/cockpit/ideen-extern-bauen.py [--zeigen] [--tage 14]

Danach: ArtifactData set → Sammlung "daten", Dokument "ideen-extern".
"""

import datetime
import glob
import json
import re
import statistics
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]
RUNS = ROOT / "outputs" / "apify-runs"
ZIEL = ROOT / "outputs" / "cockpit" / "abgleich" / "ideen-extern.json"

MIN_INTERAKTIONEN = 15   # darunter misst die Quote Zufall
MIN_BEITRAEGE = 6        # darunter sagt ein Median nichts
AUFFAELLIG = 1.8
EINGESCHLAGEN = 3.0

FORMAT = {"Video": "reel", "Sidecar": "karussell", "Image": "bild"}


def tage_her(iso):
    try:
        d = datetime.datetime.fromisoformat(iso.replace("Z", "+00:00")).date()
    except Exception:
        return 999
    return (datetime.date.today() - d).days


def profil_von(username, watchlist):
    return watchlist.get(username, {}).get("profile", "")


def main():
    tage = 14
    if "--tage" in sys.argv:
        tage = int(sys.argv[sys.argv.index("--tage") + 1])

    laeufe = sorted(glob.glob(str(RUNS / "competitors-*.json")))
    if not laeufe:
        sys.exit("🚨 Keine Scrape-Läufe in outputs/apify-runs/.")

    wl = {}
    p = ROOT / "context" / "competitor-watchlist.json"
    if p.exists():
        for a in json.load(open(p, encoding="utf-8")).get("accounts", []):
            wl[a["handle"]] = a

    # Alle Laeufe lesen, je Beitrag den zuletzt gesehenen Stand behalten —
    # ein Beitrag von gestern hat heute mehr Likes.
    posts, konten = {}, {}
    for datei in laeufe:
        d = json.load(open(datei, encoding="utf-8"))
        for a in d.get("results", []):
            u = a.get("username")
            if not u:
                continue
            konten[u] = {
                "username": u, "name": a.get("fullName") or u,
                "follower": a.get("followersCount") or 0,
                "profil": profil_von(u, wl),
                "label": wl.get(u, {}).get("label", u),
            }
            for b in (a.get("latestPosts") or []):
                if b.get("isPinned"):
                    continue          # sammelt monatelang, sagt nichts
                b = dict(b)
                b["_konto"] = u
                posts[b.get("id") or b.get("shortCode")] = b

    # Je Konto der eigene Median.
    je_konto = {}
    for b in posts.values():
        je_konto.setdefault(b["_konto"], []).append(b)

    # 🚨 Offizielle Firmen-Accounts und Patricias eigene Profile sind keine
    # Referenz. Steht als `ideenquelle: false` in der Watchlist — Patricia am
    # 25.09.2026: „doterra dach community ist eine blöde seite. das sind keine
    # referenzbeiträge für mich."
    gesperrt = {h for h, a in wl.items() if a.get("ideenquelle") is False}

    ideen = []
    for u, liste in je_konto.items():
        if u in gesperrt:
            continue
        werte = [(x.get("likesCount") or 0) + (x.get("commentsCount") or 0)
                 for x in liste]
        werte = [w for w in werte if w >= 0]
        if len(werte) < MIN_BEITRAEGE:
            continue
        med = statistics.median(werte) or 1
        for b in liste:
            inter = (b.get("likesCount") or 0) + (b.get("commentsCount") or 0)
            if inter < MIN_INTERAKTIONEN:
                continue
            faktor = inter / med
            if faktor < AUFFAELLIG:
                continue
            alt = tage_her(b.get("timestamp", ""))
            if alt > tage:
                continue
            cap = (b.get("caption") or "").strip()
            if "--alle" not in sys.argv and not brauchbar(b, cap):
                continue
            ideen.append({
                "id": b.get("shortCode") or b.get("id"),
                "konto": u,
                "label": konten[u]["label"],
                "profil": konten[u]["profil"],
                "follower": konten[u]["follower"],
                "format": FORMAT.get(b.get("type"), "bild"),
                "hook": erste_zeile(cap),
                "caption": cap[:600],
                "likes": b.get("likesCount") or 0,
                "kommentare": b.get("commentsCount") or 0,
                "interaktionen": inter,
                "median_konto": round(med),
                "faktor": round(faktor, 1),
                "stufe": "eingeschlagen" if faktor >= EINGESCHLAGEN else "auffällig",
                "tage_her": alt,
                "datum": (b.get("timestamp") or "")[:10],
                "link": b.get("url", ""),
                "hashtags": (b.get("hashtags") or [])[:6],
            })

    ideen.sort(key=lambda x: -x["faktor"])

    ergebnis = {
        "stand": datetime.date.today().isoformat(),
        "quelle": Path(laeufe[-1]).name,
        "zeitraum_tage": tage,
        "regeln": {
            "mindest_interaktionen": MIN_INTERAKTIONEN,
            "mindest_beitraege": MIN_BEITRAEGE,
            "auffaellig_ab": AUFFAELLIG,
            "eingeschlagen_ab": EINGESCHLAGEN,
        },
        "ideen": ideen,
    }
    ZIEL.parent.mkdir(parents=True, exist_ok=True)
    ZIEL.write_text(json.dumps(ergebnis, ensure_ascii=False, indent=1),
                    encoding="utf-8")

    print("Läufe gelesen: %d  ·  Beiträge: %d  ·  Konten: %d"
          % (len(laeufe), len(posts), len(je_konto)))
    print("Ideen (letzte %d Tage): %d  davon eingeschlagen: %d"
          % (tage, len(ideen),
             len([i for i in ideen if i["stufe"] == "eingeschlagen"])))
    print("→ %s" % ZIEL)

    if "--zeigen" in sys.argv:
        for i in ideen[:14]:
            print("\n  %sx Median · %s · %s · %s (%d Follower)"
                  % (i["faktor"], i["format"], i["datum"], i["label"],
                     i["follower"]))
            print("    %s" % i["hook"][:95])


def brauchbar(b, cap):
    """🚨 Nach Likes sortieren findet Zitatkacheln, keine Content-Ideen.

    Beim ersten Lauf standen ganz oben: „Ich trage schon genug ❤️",
    „Manifestieren ist schön.", „Orlando, here I come!" — alle mit dem 10- bis
    19-fachen des Median. Das sind Spruchbilder und Reiseposts. Sie werden
    geteilt, weil sie ein Gefühl treffen, und taugen als Vorlage für einen
    Lead-Post überhaupt nicht.

    Dieselbe Lehre wie beim Discovery-Lauf in CLAUDE.md: nach Verkaufssignalen
    schauen, nicht nach Likes.
    """
    # Ein Einzelbild ist fast immer eine Spruchkachel. Reel und Karussell
    # tragen Inhalt.
    if FORMAT.get(b.get("type")) == "bild":
        return False
    # Ein Hook ohne Text darunter ist kein Beitrag, sondern eine Behauptung.
    if len(cap) < 200:
        return False
    # Reines Privates: ein Satz plus Hashtags.
    zeilen = [z for z in cap.splitlines() if len(z.strip()) > 20]
    return len(zeilen) >= 2


def erste_zeile(cap):
    """Die erste Zeile ist der Hook — leere Zeilen und Emojis am Anfang weg."""
    for z in cap.split("\n"):
        z = z.strip()
        z = re.sub(r"^[^\w„\"'(]+", "", z)
        if len(z) > 8:
            return z
    return cap[:80]


if __name__ == "__main__":
    main()
