"""Öl-App, letzter Schritt — Daten fürs Artifact zusammenpacken und verknüpfen.

    python scripts/oel-app/app-bauen.py
    → danach Artifact publish: file_path outputs/oel-app/app/index.html,
      files {"daten/produkte.json", "daten/themen.json", "daten/tipps.json"} aus outputs/oel-app/app/daten/

Liest die Einträge aus outputs/oel-app/daten/ (produkte/, themen/, tipps.json) und verknüpft sie:
Produktnamen in Themen, Mischpartnern und Tipps werden zu Kennungen, freie Themenwörter der Produkte zu
Themen-Kennungen. Was sich nicht zuordnen lässt, bleibt als Text stehen (die App sucht dann danach).

Die Seite selbst (index.html) ist Quelle in scripts/oel-app/index.html und wird nur kopiert.
🚨 Das Artifact bleibt PRIVAT — Buchauszüge und Gruppen-Tipps. Nie über das Share-Menü freigeben.
"""
import json
import pathlib
import re
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
WS = pathlib.Path(__file__).resolve().parents[2]
DATEN = WS / "outputs/oel-app/daten"
APP = WS / "outputs/oel-app/app"
ANLIEGEN = WS / "context/doTERRA/Produktwissen/anliegen.json"
ZUSATZ = WS / "context/doTERRA/Produktwissen/oel-app-zusatzprodukte.json"


def norm(s):
    s = s.lower()
    for a, b in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss"), ("ō", "o")):
        s = s.replace(a, b)
    s = re.sub(r"doterra|™|®|\(.*?\)", "", s)
    return re.sub(r"[^a-z0-9]", "", s)


def main():
    katalog = json.loads((DATEN / "katalog.json").read_text(encoding="utf-8"))["produkte"]
    produkte = []
    for p in katalog:
        f = DATEN / "produkte" / f"{p['id']}.json"
        produkte.append(json.loads(f.read_text(encoding="utf-8")) if f.exists() else dict(p, unfertig=True))
    anl = json.loads(ANLIEGEN.read_text(encoding="utf-8"))["anliegen"]
    themen = []
    for a in anl:
        f = DATEN / "themen" / f"{a['id']}.json"
        if f.exists():
            themen.append(json.loads(f.read_text(encoding="utf-8")))
    tipps = json.loads((DATEN / "tipps.json").read_text(encoding="utf-8")) if (DATEN / "tipps.json").exists() else []

    # Namen → Kennung: englisch, deutsch, Kennung selbst. Touch-Varianten verlieren gegen das Öl.
    namen = {}
    for p in sorted(produkte, key=lambda x: "touch" in x["id"]):
        for n in (p["name"], p.get("deutsch", ""), p["id"].replace("-", " ")):
            k = norm(n)
            if len(k) >= 3:
                namen.setdefault(k, p["id"])

    # deutsche und alte Namen aus den Büchern (Zedernholz → cedarwood …)
    for n, i in json.loads(ZUSATZ.read_text(encoding="utf-8"))["namen"].items():
        namen[norm(n)] = i

    def pid(name):
        name = re.sub(r"\(.*?\)", "", name).split("/")[0]  # „Wintergrün (nicht in der Produktliste)“
        k = norm(name)
        if k in namen:
            return namen[k]
        k2 = re.sub(r"(oel|ol|oil|essentialoil|mischung|blend)$", "", k)
        return namen.get(k2)

    thema_wort = {}
    for a in anl:
        thema_wort[norm(a["name"])] = a["id"]
        for teil in re.split(r"[&,:]", a["name"]):
            if len(norm(teil)) >= 4:
                thema_wort.setdefault(norm(teil), a["id"])
        for s in a["suche"]:
            if len(s) >= 4:
                thema_wort.setdefault(norm(s), a["id"])

    def tid(wort):
        k = norm(wort)
        if k in thema_wort:
            return thema_wort[k]
        for w, i in thema_wort.items():
            if len(w) >= 5 and (w in k or k in w):
                return i
        return None

    for p in produkte:
        if (APP / "bilder" / f"{p['id']}.jpg").exists():  # aus fotos-bauen.py
            p["foto"] = f"bilder/{p['id']}.jpg"
        p["passt_zu"] = [{"n": n, "id": pid(n)} for n in p.get("passt_zu", [])]
        p["themen"] = [{"n": n, "id": tid(n)} for n in p.get("themen", [])]
    for t in themen:
        for e in t["empfehlungen"]:
            e["id"] = pid(e["produkt"])
    ids = {a["id"] for a in anl}
    for t in tipps:
        t["produkte"] = [{"n": n, "id": pid(n)} for n in t.get("produkte", [])]
        t["themen"] = [i for i in t.get("themen", []) if i in ids]

    # Der vollständige Durchgang (wissen-ausziehen.py): jede Aussage zu einem Öl je Produkt in eine eigene
    # Datei, die die App erst beim Öffnen des Produkts lädt — alles in produkte.json wäre zu schwer fürs Handy.
    je_produkt, auszug_rezepte = {}, []
    for f in sorted((DATEN / "auszug").glob("*.json")):
        a = json.loads(f.read_text(encoding="utf-8"))
        for s in a["aussagen"]:
            for i in {pid(n) for n in s["produkte"]} - {None}:
                je_produkt.setdefault(i, []).append({k: s[k] for k in ("art", "text", "quelle", "wo")})
        for r in a["rezepte"]:
            auszug_rezepte.append(dict(r, quelle=f"{r['quelle']}, {r['wo']}" if r.get("wo") else r["quelle"]))
    (APP / "daten" / "wissen").mkdir(parents=True, exist_ok=True)
    for alt in (APP / "daten" / "wissen").glob("*.json"):  # sonst bleibt ein Produkt mit altem Stand stehen
        alt.unlink()
    for p in produkte:
        liste = je_produkt.get(p["id"], [])
        p["alles_n"] = len(liste)
        if liste:
            (APP / "daten" / "wissen" / f"{p['id']}.json").write_text(
                json.dumps(liste, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    if je_produkt:
        print(f"Vollständiger Durchgang: {sum(map(len, je_produkt.values()))} Aussagen zu {len(je_produkt)} Produkten, "
              f"{len(auszug_rezepte)} Rezepte")

    rezepte = rezepte_sammeln(produkte, themen, tipps, auszug_rezepte)

    APP.joinpath("daten").mkdir(parents=True, exist_ok=True)
    gruppen = list(dict.fromkeys(a["gruppe"] for a in anl))
    for name, inhalt in (("produkte", produkte), ("themen", {"gruppen": gruppen, "themen": themen}),
                         ("tipps", tipps), ("rezepte", rezepte)):
        (APP / "daten" / f"{name}.json").write_text(json.dumps(inhalt, ensure_ascii=False, separators=(",", ":")),
                                                    encoding="utf-8")
    shutil.copy(pathlib.Path(__file__).with_name("index.html"), APP / "index.html")

    offen_p = sum(1 for p in produkte if p.get("unfertig"))
    ohne = sum(1 for p in produkte for x in p["passt_zu"] if not x["id"])
    alle = sum(len(p["passt_zu"]) for p in produkte)
    print(f"Produkte {len(produkte)} (ohne Eintrag: {offen_p}) · Themen {len(themen)} · Tipps {len(tipps)}")
    print(f"Mischpartner zugeordnet: {alle - ohne}/{alle}")
    for f in sorted((APP / "daten").glob("*.json")):
        print(f"  {f.name}: {f.stat().st_size / 1e6:.1f} MB")


# Trägeröle und Kapseln: stehen in vielen Rezepten, gehören aber nicht zu „hast du alle Öle da?“
GRUNDZUTAT = {"fractionated-coconut-oil", "castor-oil", "veggie-caps"}
GRUND = re.compile(r"wasser|jojoba|mandel|traeger|massage|aloe|flasche|pflanzen|basis|johanniskraut|calophyllum|essig|"
                   r"hanf|macadamia|hagebutte|hamamelis|shampoo|milch|alkohol|wodka|vitamin|fco|oliven|kokos|honig|salz|"
                   r"glycerin|shea|wachs|natron|zucker|seife|tonerde|duschgel|lotion|creme|auf \d+ ?ml|scan")


def falten(s):
    s = s.lower()
    for a, b in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss"), ("ō", "o"), ("™", ""), ("®", "")):
        s = s.replace(a, b)
    return s


def rezepte_sammeln(produkte, themen, tipps, auszug=()):
    """Alle Rezepte aus Produkten, Themen und Gruppen-Tipps, je Zutat das Produkt dahinter.

    Für „Was mische ich heute?“: ein Rezept geht, wenn jede Öl-Zutat im Vorrat ist. Zutaten ohne Produkt
    (Wasser, Salz, Honig) zählen nicht; eine Zeile mit Tropfen, aber ohne bekanntes Öl, heisst „unbekannt“ —
    dann zeigt die App das Rezept nie als „alles da“, statt eine Zutat zu verschweigen.
    """
    alias = json.loads(ZUSATZ.read_text(encoding="utf-8"))["namen"]
    muster = []
    for p in produkte:
        namen = [re.sub(r"d[oō]TERRA", "", p["name"], flags=re.I)]
        # deutsche Beinamen zählen auch — „Klärende Mischung“ ist Purify; nur das nackte Wort „Mischung“ nicht
        if p.get("deutsch") and not re.search(r"kollektion|kapseln|kit\b", p["deutsch"], re.I):
            namen += [x for x in p["deutsch"].split(",") if falten(x).strip() not in ("mischung", "")]
        for n in namen:
            n = falten(n).strip()
            if len(n) >= 3:
                muster.append((n, p["id"]))
    for n, i in alias.items():
        muster.append((falten(n), i))
    muster.sort(key=lambda x: -len(x[0]))
    muster = [(re.compile(r"(?<![a-z])" + re.escape(n) + r"(?![a-z])"), i) for n, i in muster]

    def zuordnen(zeile):
        z, ids = falten(zeile), []
        tropfen = re.search(r"tropfen|trpf|drops|\bml\b", z) is not None
        # „frische Kräuter wie Rosmarin“ ist eine Küchenzutat, kein Öl — ohne Tropfenangabe nicht zuordnen
        if not tropfen and re.search(r"frisch|getrocknet|blaett|blatt|zweig|saft|schale|kraeuter|pulver|gemahlen|"
                                     r"\d\s*(g|el|tl|stueck|prise)\b|\b(el|tl)\b", z):
            return [], False
        z = re.sub(r"([a-z]{3,})-?oele?\b", r"\1", z)  # „Zitronenöl“ → „zitronen“, findet dann Zitrone
        z = re.sub(r"\bzitronen\b", "zitrone", z)
        for rx, i in muster:
            if rx.search(z):
                ids.append(i)
                z = rx.sub(" ", z)  # „Wild Orange“ nicht nochmals als „Orange“ zählen
        if not ids and GRUND.search(z):  # Wasser, Jojoba, Sprühflasche … fehlen nie im Sinn von „Öl fehlt“
            return [], False
        # 🚨 „Klärende Mischung“ ohne Tropfen ist trotzdem ein Öl, das fehlen kann
        unbekannt = not ids and (tropfen or re.search(r"mischung|touch|roll-?on", z) is not None)
        return ids, unbekannt

    roh = []
    for p in produkte:
        roh += [dict(r, herkunft=("p", p["id"])) for r in p.get("rezepte", [])]
    for t in themen:
        roh += [dict(r, herkunft=("t", t["id"])) for r in t.get("rezepte", [])]
    for t in tipps:
        if t.get("art") == "Rezept" or t.get("zutaten"):
            roh.append({"titel": t["titel"], "zutaten": t.get("zutaten", []), "anleitung": t["text"],
                        "quelle": t.get("chat", ""), "herkunft": ("x", t["id"])})

    for r in auszug:  # aus wissen-ausziehen.py: alle Rezepte aus allen Quellen
        roh.append({"titel": r["titel"], "zutaten": r["zutaten"], "anleitung": r["anleitung"],
                    "quelle": r["quelle"], "herkunft": ("q", "")})

    aus, gesehen = [], set()
    for r in roh:
        ids, offen, zeilen = [], [], []
        for z in r.get("zutaten", []):
            i, u = zuordnen(z)
            ids += i
            if u:
                offen.append(z)
            # je Zeile: Text, Öle darin (ohne Trägeröl), nicht zugeordnet ja/nein — für ✓ und „fehlt“ in der App
            zeilen.append([z, [x for x in i if x not in GRUNDZUTAT], bool(u)])
        unbekannt = offen  # die App zeigt diese Zeilen als „nicht zugeordnet“
        oele = sorted(set(ids) - GRUNDZUTAT)
        if not oele:
            continue
        schluessel = (falten(r["titel"])[:40], tuple(oele))
        if schluessel in gesehen:
            continue
        gesehen.add(schluessel)
        aus.append({"titel": r["titel"], "zeilen": zeilen, "anleitung": r.get("anleitung", ""),
                    "quelle": r.get("quelle", ""), "oele": oele, "unbekannt": unbekannt,
                    "von": "|".join(r["herkunft"])})
    print(f"Rezepte: {len(aus)} mit Öl-Zutaten (aus {len(roh)}), {sum(bool(r["unbekannt"]) for r in aus)} mit unbekannter Zutat")
    return aus


if __name__ == "__main__":
    main()
