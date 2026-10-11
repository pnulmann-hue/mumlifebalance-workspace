"""
Sammelt alles, was ein Angebot beruehrt, an einer Stelle.

Patricias Satz war: „mein Ziel ist einfach immer maximale Zeit sparen und jetzt
habe ich vieles verteilt." Genau das loest diese Datei. Zu jedem Angebot steht
danach im Cockpit:

  Datei         das PDF selbst, anklickbar (liegt als Anhang am Artifact)
  Funnel        wo es in der Produkttreppe haengt, mit Keyword und Liste
  Auslieferung  welche Automation es verschickt und mit welchen Mails
  Erwaehnt in   in welchen Beitraegen, Reels und Briefings davon die Rede ist
  Kurs          welche Lektionen dazugehoeren

Die Zuordnung laeuft ueber Namen und Keyword des Angebots. Was nicht sicher
zugeordnet werden kann, bleibt lieber leer als falsch.

Die Anhang-Adressen (`/_blob/...`) kommen nicht aus dem Dateisystem, sondern
entstehen beim Hochladen ins Artifact. Sie stehen deshalb hier als Tabelle und
werden beim naechsten Hochladen ergaenzt.

Aufruf:
  python scripts/cockpit/verknuepfen.py [zielordner]
"""
import json
import re
import sys
from datetime import date
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]

# Was hochgeladen wurde: Angebots-Kennung -> Anhang am Artifact.
# Ergaenzen, wenn eine weitere Datei hochgeladen wird.
ANHAENGE = {
    "a-0-euro-starterguide": [
        {"name": "Starterguide", "blob": "/_blob/43bb5e33cd93df89cb5955079b331ce3",
         "typ": "PDF", "seiten": 17}],
    "a-workbook-von-0-auf-echt": [
        {"name": "Workbook: Von 0 auf echt", "blob": "/_blob/45f60d981421530fea57e1c635546237",
         "typ": "PDF", "seiten": 25}],
    "a-lead-challenge": [
        {"name": "Lead-Challenge Workbook", "blob": "/_blob/bd461524b5b2efa42c9e3109449c0f42",
         "typ": "PDF", "seiten": 13}],
    "a-story-challenge": [
        {"name": "Story-Challenge Workbook", "blob": "/_blob/bcb120da59f69fcaba91934deeafa3b9",
         "typ": "PDF", "seiten": 20}],
    "a-storyideen-f-r-networkerinne": [
        {"name": "90 Storyideen für Networkerinnen", "blob": "/_blob/f4e65f7dcf7d82c94c07ca968a83cac3",
         "typ": "PDF", "seiten": 47}],
}

# Der Fahrplan gehoert zu keinem Angebot in der Liste, ist aber ein Freebie.
LOSE_DATEIEN = [
    {"name": "Dein 0€ Fahrplan", "blob": "/_blob/25a9e0c778b14319e666cf968eb123fe",
     "typ": "PDF", "seiten": 8, "notiz": "Keywords SYSTEM und FAHRPLAN"},
]

# Wo nach Erwaehnungen gesucht wird.
CONTENT = ["outputs/karussells", "outputs/reels", "outputs/stories",
           "outputs/montag", "outputs/freitag", "outputs/telegram-posts",
           "outputs/monatsplaene", "outputs/content-kalender"]

FUELLWORT = re.compile(r"\b(der|die|das|und|für|fuer|dein|deine|mit|als|zum|zur|von|in|im)\b")


def kerne(name):
    """Aus einem Angebotsnamen die Woerter, an denen man ihn erkennt."""
    n = name.lower()
    n = re.sub(r"\(.*?\)", " ", n)          # Klammer-Zusaetze weg
    n = n.split("—")[0].split("–")[0]       # alles nach dem Gedankenstrich weg
    n = FUELLWORT.sub(" ", n)
    n = re.sub(r"[^a-zäöüß0-9€\s-]+", " ", n)
    teile = [t for t in n.split() if len(t) > 3]
    return teile[:4]


def erwaehnungen(angebot, dateien):
    """In welchen Content-Dokumenten dieses Angebot vorkommt."""
    worte = kerne(angebot["name"])
    kw = (angebot.get("keyword") or "").lower()
    if not worte and not kw:
        return []

    # Das Keyword steht in Captions immer gross („Kommentier LEAD"). Klein
    # geschrieben steckt „lead" auch in „Leader" und „Leadmagnet" — das
    # wuerde Treffer erfinden, und ein falscher Treffer kostet mehr Zeit,
    # als er spart.
    kw_muster = re.compile(r"\b%s\b" % re.escape(kw.upper())) if len(kw) > 2 else None

    treffer = []
    for pfad, text in dateien:
        klein = text.lower()
        passt = bool(kw_muster and kw_muster.search(text)) or \
                (len(worte) >= 2 and sum(1 for w in worte if w in klein) >= 2) or \
                (len(worte) == 1 and len(worte[0]) > 6 and worte[0] in klein)
        if not passt:
            continue
        titel = ""
        for zeile in text.splitlines():
            if zeile.startswith("# "):
                titel = zeile[2:].strip()
                break
        treffer.append({"datei": pfad, "titel": titel[:80] or Path(pfad).stem})
    treffer.sort(key=lambda x: x["datei"], reverse=True)
    return treffer[:12]


def content_laden():
    raus = []
    for ordner in CONTENT:
        p = ROOT / ordner
        if not p.exists():
            continue
        for f in p.rglob("*.md"):
            if "_INDEX" in f.name:
                continue
            try:
                raus.append((f.relative_to(ROOT).as_posix(),
                             f.read_text(encoding="utf-8", errors="replace")))
            except OSError:
                continue
    return raus


def funnel_von(angebot, funnels):
    """Der Funnel-Eintrag zu diesem Angebot, wenn es einen gibt."""
    kennung = angebot["id"].replace("a-", "", 1)
    for f in funnels:
        if f.get("id") == kennung:
            quellen = f.get("traffic_quellen") or {}
            ac = f.get("ac_integration") or {}
            anschluss = f.get("produkttreppe_anschluss") or f.get("produkttreppe") or ""
            if isinstance(anschluss, list):
                anschluss = anschluss[0] if anschluss else ""
            return {
                "typ": f.get("typ", ""),
                "status": f.get("status", ""),
                "keyword": (quellen.get("manychat_keyword") or "").split(" (")[0],
                "landing": quellen.get("wordpress_landing") or "",
                "liste": ac.get("liste_id"),
                "automation": (ac.get("automation_id")
                               or ac.get("auslieferung_automation_id")
                               or ac.get("nurture_automation_id")),
                "anschluss": str(anschluss)[:120],
            }
    return None


def auslieferung(nummer, ziel):
    """Die Mails, die diese Automation verschickt."""
    if not nummer:
        return []
    p = Path(ziel) / ("mails-%s.json" % nummer)
    if not p.exists():
        return []
    d = json.loads(p.read_text(encoding="utf-8"))
    return [{"betreff": m.get("betreff", ""), "gebaut": m.get("gebaut", "")}
            for m in d.get("items", [])]


def lektionen_zu(angebot, kursdatei):
    """Die Lektionen, wenn das Angebot ein Kurs ist."""
    if not Path(kursdatei).exists():
        return None
    d = json.loads(Path(kursdatei).read_text(encoding="utf-8"))
    worte = set(kerne(angebot["name"]))
    for k in d.get("kurse", []):
        if worte & set(kerne(k["name"])):
            return {"kurs": k["name"], "anzahl": len(k["lektionen"])}
    return None


def main():
    ziel = Path(sys.argv[1]) if len(sys.argv) > 1 else \
        ROOT / "outputs" / "cockpit" / "abgleich"
    ziel.mkdir(parents=True, exist_ok=True)

    pfad = ziel / "produkte.json"
    if not pfad.exists():
        sys.exit("produkte.json fehlt — erst daten-abgleich.py laufen lassen.")
    angebote = json.loads(pfad.read_text(encoding="utf-8"))["items"]

    fdatei = ROOT / "context" / "active-funnels.json"
    funnels = json.loads(fdatei.read_text(encoding="utf-8")).get("funnels", []) \
        if fdatei.exists() else []

    print("  Content-Dokumente lesen …")
    inhalte = content_laden()
    print("  %d Dokumente durchsucht" % len(inhalte))

    raus = {}
    for a in angebote:
        f = funnel_von(a, funnels)
        eintrag = {
            "dateien": ANHAENGE.get(a["id"], []),
            "funnel": f,
            "mails": auslieferung(f.get("automation") if f else None, ziel),
            "erwaehnt": erwaehnungen(a, inhalte),
            "kurs": lektionen_zu(a, ziel / "kurse.json"),
        }
        if any(eintrag.values()):
            raus[a["id"]] = eintrag

    (ziel / "verknuepfung.json").write_text(json.dumps(
        {"werte": raus, "lose": LOSE_DATEIEN, "stand": date.today().isoformat()},
        ensure_ascii=False, indent=2), encoding="utf-8")

    mit_datei = sum(1 for v in raus.values() if v["dateien"])
    mit_mails = sum(1 for v in raus.values() if v["mails"])
    mit_text = sum(1 for v in raus.values() if v["erwaehnt"])
    print("\n  %d Angebote verknüpft" % len(raus))
    print("    %2d mit anklickbarer Datei" % mit_datei)
    print("    %2d mit Auslieferungs-Mails" % mit_mails)
    print("    %2d mit Erwähnungen im Content" % mit_text)
    print("\nAbgelegt in: %s" % (ziel / "verknuepfung.json"))


if __name__ == "__main__":
    main()
