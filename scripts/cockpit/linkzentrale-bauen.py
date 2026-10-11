"""
Die Link-Zentrale: alle Links gebündelt, zum Kopieren.

Patricia: „ich muss z.B. auch immer die links suchen wenn ich in der story was
verlinken will. das nervt übelst." Und am 16.09.2026 praeziser:
„will immer den link zu dem was ausgeliefert wird, den link zur landingpage
unter mumlifebalance., allenfalls den link zu thrivecart, den link zur
telegramgruppe wie z.B. bei der storychallenge das bekommen sie ja."

Darum traegt jeder Eintrag **vier Linkarten** statt einer:

  landingpage   die Seite auf mumlifebalance.ch, auf die sie in der Story zeigt
  thrivecart    die Kasse
  auslieferung  was die Kundin wirklich bekommt — PDF, Bot, Tool
  telegram      die Gruppe zum Angebot

Gebaut aus drei Quellen, die es alle schon gibt:

  context/link-uebersicht.md   die gepflegte Wahrheit. **Diese Datei ist die
                               Quelle**, nicht das Cockpit. Wer einen Link
                               aendert, aendert ihn dort.
  katalog.json                 der echte Preis aus ThriveCart
  verknuepfung.json            die hinterlegten PDFs am Artifact (`/_blob/…`)

🚨 **Hier wird nichts erfunden.** Steht ein Link nicht in der Uebersicht, fehlt
er auch im Cockpit — mit einem sichtbaren Hinweis statt einer geratenen Adresse.
Ein toter Link in einer Story kostet mehr als eine Luecke.

🚨 **Die Spalten werden ueber die Kopfzeile gefunden, nicht ueber ihre
Position.** Sonst verschiebt eine neue Spalte in der Uebersicht stillschweigend
alle Werte um eins — und niemand sieht es, weil trotzdem etwas dasteht.

Aufruf:
  python scripts/cockpit/linkzentrale-bauen.py [zielordner]
"""
import json
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]
QUELLE = ROOT / "context" / "link-uebersicht.md"
ARTIFACT = "https://claude.ai/code/artifact/eeee48d5-3e50-4cff-8047-1ec5eccbb074"

GRUPPEN = [
    ("doterra", "doTERRA", "Profil Mama Regeneration & Energie"),
    ("freebie", "0-Euro-Freebies", "mit Keyword — das schickst du auf ein Kommentar-Stichwort"),
    ("bezahlt", "Bezahlte Angebote", "Checkout, Seite und Auslieferung"),
    ("seite", "Weitere Seiten", "Übersicht, Warteliste, Blog"),
    ("recht", "Rechtliches", "gehört in den Footer jeder Landingpage"),
]

# Kopfzeilen-Wort -> Feld im Eintrag. Alles andere wird ignoriert.
SPALTEN = {
    "freebie": "name", "produkt": "name", "was": "name",
    "keyword": "keyword", "preis": "preis",
    "landingpage": "landingpage",
    "thrivecart": "thrivecart", "checkout": "thrivecart", "bestellen": "thrivecart",
    "auslieferung": "auslieferung",
    "telegram": "telegram",
    "status": "status_text",
    "link": "landingpage",
}
LINKARTEN = ["landingpage", "thrivecart", "auslieferung", "telegram"]


def zellen(zeile):
    if not zeile.strip().startswith("|"):
        return None
    teile = [t.strip() for t in zeile.strip().strip("|").split("|")]
    if all(set(t) <= set("-: ") for t in teile):
        return None
    return teile


def sauber(text):
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text or "")
    text = text.replace("**", "").replace("`", "")
    text = re.sub(r"[\U0001F500-\U0001FAFF☀-➿️]", "", text)
    return re.sub(r"\s+", " ", text).strip()


def links_aus(text):
    """Alle Adressen einer Zelle — eine Zelle kann mehrere tragen (MBA)."""
    roh = re.findall(r"(?:https?://|/_blob/)[^\s|)\]]+", text or "")
    raus = []
    for u in roh:
        u = u.rstrip(".,·")
        if u.startswith("/_blob/"):
            u = ARTIFACT + u
        if u not in raus:
            raus.append(u)
    return raus


def status_aus(text):
    if "🔴" in text:
        return "tot"
    if "⚠️" in text or "🚨" in text:
        return "achtung"
    if "🟢" in text or "200" in text:
        return "live"
    return ""


def uebersicht_lesen():
    if not QUELLE.exists():
        sys.exit("Fehlt: %s" % QUELLE)
    eintraege = []
    gruppe, kopf = None, None

    for zeile in QUELLE.read_text(encoding="utf-8").splitlines():
        k = zeile.strip()

        if k.startswith("## ") and "doTERRA — Profil" in k:
            gruppe, kopf = "doterra", None
            continue
        if k.startswith("### "):
            kopf = None
            if "Freebies" in k:
                gruppe = "freebie"
            elif "Bezahlte" in k:
                gruppe = "bezahlt"
            elif "Sonstige Seiten" in k:
                gruppe = "seite"
            elif "Rechtliches" in k:
                gruppe = "recht"
            else:
                gruppe = None
            continue
        if k.startswith("## ") and "Mentoring" not in k:
            gruppe, kopf = None, None
            continue
        if not gruppe:
            continue

        z = zellen(zeile)
        if not z:
            continue

        # Erste Zeile einer Tabelle ist die Kopfzeile.
        if kopf is None:
            kopf = [SPALTEN.get(sauber(c).lower(), "") for c in z]
            if "name" not in kopf:
                kopf = None      # keine Tabelle, die uns gehoert
            continue

        roh = {}
        for feld, wert in zip(kopf, z):
            if feld:
                roh[feld] = wert

        name = sauber(roh.get("name", ""))
        if not name:
            continue

        e = {
            "gruppe": gruppe,
            "name": name,
            "keyword": sauber(roh.get("keyword", "")).replace("/", " oder ").strip(" —"),
            "preis": sauber(roh.get("preis", "")).strip(" —"),
            "status": status_aus(roh.get("status_text", "")),
            "hinweis": sauber(roh.get("status_text", "")),
        }
        for art in LINKARTEN:
            zelle = roh.get(art, "")
            e[art] = links_aus(zelle)
            # Auslieferung ist manchmal Text statt Adresse („3-Tage-Mail-Challenge")
            wortlaut = sauber(re.sub(r"(?:https?://|/_blob/)\S+", "", zelle)).strip(" —·")
            if wortlaut and wortlaut != "—":
                e[art + "_text"] = wortlaut
        # Der Haupt-Link fuers Suchfeld: Landingpage, sonst Kasse, sonst Auslieferung.
        e["link"] = next((e[a][0] for a in LINKARTEN if e.get(a)), "")
        eintraege.append(e)
    return eintraege


def schluessel(name):
    k = (name or "").lower()
    k = re.sub(r"\(.*?\)", " ", k)
    k = re.sub(r"[^a-zäöüß0-9 ]+", " ", k)
    return re.sub(r"\s+", " ", k).strip()


def anreichern(eintraege, ziel):
    kat = ziel / "katalog.json"
    if kat.exists():
        nach_slug = {}
        for a in json.loads(kat.read_text(encoding="utf-8"))["angebote"]:
            if a.get("slug"):
                nach_slug[a["slug"]] = a
        for e in eintraege:
            for u in e.get("thrivecart", []):
                slug = [t for t in u.split("/") if t][-1].lower()
                a = nach_slug.get(slug)
                if a:
                    e["tc_preis"] = a.get("preis")
                    e["waehrung"] = a.get("waehrung") or "CHF"
                    e["kategorie"] = a.get("kategorie", "")
                    # ThriveCart sagt selbst, ob ein Checkout laeuft. Das gehoert
                    # nicht von Hand gepflegt — „test" nimmt kein echtes Geld,
                    # „disabled" nimmt gar nichts. Wer das nicht sieht, schickt
                    # Kundinnen auf eine Kasse, die nichts abbucht.
                    e["tc_status"] = a.get("status") or ""
                    break

    vk = ziel / "verknuepfung.json"
    if vk.exists():
        werte = json.loads(vk.read_text(encoding="utf-8")).get("werte", {})
        nach_name = {}
        for _, v in werte.items():
            for d in (v.get("dateien") or []):
                nach_name.setdefault(schluessel(d["name"]), []).append(d)
        # Teilstring allein reicht nicht: „Lead-Challenge 3-Tage-Workbook"
        # und „Lead-Challenge Workbook" enthalten einander nicht. Darum
        # zusaetzlich ueber gemeinsame Woerter, mit einer Mindest-Deckung.
        def woerter(s):
            return {w for w in s.split() if len(w) > 3}

        for e in eintraege:
            k = schluessel(e["name"])
            kw = woerter(k)
            bester, punkte = None, 0
            for name, dateien in nach_name.items():
                if not name or len(name) < 6:
                    continue
                if name in k or k in name:
                    bester, punkte = dateien, 99
                    break
                gemeinsam = kw & woerter(name)
                # Mindestens zwei geteilte Woerter, sonst passt „Challenge"
                # allein auf Lead- und Story-Challenge gleichermassen.
                if len(gemeinsam) >= 2 and len(gemeinsam) > punkte:
                    bester, punkte = dateien, len(gemeinsam)
            if bester:
                e.setdefault("dateien", []).extend(bester)
    return eintraege


def main():
    ziel = Path(sys.argv[1]) if len(sys.argv) > 1 else \
        ROOT / "outputs" / "cockpit" / "abgleich"
    ziel.mkdir(parents=True, exist_ok=True)

    eintraege = anreichern(uebersicht_lesen(), ziel)

    (ziel / "links.json").write_text(json.dumps({
        "eintraege": eintraege,
        "gruppen": [{"id": g, "name": n, "hinweis": h} for g, n, h in GRUPPEN],
        "linkarten": [
            {"id": "landingpage", "name": "Landingpage", "kurz": "Seite"},
            {"id": "thrivecart", "name": "ThriveCart", "kurz": "Kasse"},
            {"id": "auslieferung", "name": "Auslieferung", "kurz": "Das kriegt sie"},
            {"id": "telegram", "name": "Telegram-Gruppe", "kurz": "Gruppe"},
        ],
        "quelle": "context/link-uebersicht.md",
        "stand": date.today().isoformat(),
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    z = Counter(e["gruppe"] for e in eintraege)
    art = Counter(a for e in eintraege for a in LINKARTEN if e.get(a))
    tc = Counter(e.get("tc_status") for e in eintraege if e.get("tc_status"))
    print("  %d Einträge" % len(eintraege))
    for g, n, _ in GRUPPEN:
        if z[g]:
            print("    %-24s %2d" % (n, z[g]))
    print("\n  Linkarten belegt:")
    for a in LINKARTEN:
        print("    %-16s %2d" % (a, art[a]))

    print("\n  Checkout-Zustand laut ThriveCart:")
    for zustand in ("live", "test", "disabled"):
        if tc[zustand]:
            print("    %-10s %2d" % (zustand, tc[zustand]))
    nicht_live = [(e["name"], e["tc_status"]) for e in eintraege
                  if e.get("tc_status") and e["tc_status"] != "live"]
    if nicht_live:
        print("\n  🚨 Verlinkt, aber der Checkout nimmt kein echtes Geld:")
        for n, s in nicht_live:
            print("      %-44s %s" % (n[:44], s))

    luecken = [e["name"] for e in eintraege
               if not e.get("landingpage") and e["gruppe"] in ("freebie", "bezahlt")]
    if luecken:
        print("\n  Ohne Landingpage:")
        for n in luecken:
            print("      %s" % n)
    tot = [e["name"] for e in eintraege if e["status"] == "tot"]
    if tot:
        print("\n  🔴 Tot laut Übersicht: %s" % ", ".join(tot))
    print("\nAbgelegt in: %s" % (ziel / "links.json"))


if __name__ == "__main__":
    main()
