"""Baut das Archiv der geposteten Beitraege samt gemessenen Zahlen.

Ersetzt die Notion-Ansicht „Analyse" der Content-Management-Datenbank. Dort
standen neun Spalten, von denen Patricia **sieben von Hand** eingetragen hat:
Reichweite, Gespeichert, Gefaellt mir, Kommentare, neue Follower, URL und
Veroeffentlichungsdatum. Alle sieben liefert die Meta Graph API.

    python scripts/instagram-insights/holen.py     # Zahlen holen (regelmaessig!)
    python scripts/cockpit/gepostet-bauen.py       # -> gepostet.json
    # danach: ArtifactData set -> Sammlung "daten", Dokument "gepostet"

Ihre Eingabe bleiben genau zwei Dinge: **Bewertung** (Sterne) und **Notiz**
(in Notion hiess das Feld „A N A L Y S E"). Die stehen in `daten/gepostet-notizen`
und werden hier **nie** angefasst — dasselbe Muster wie `daten/produkt-details`.

🚨 **Das Archiv waechst, die API-Antwort nicht.** Die Graph API gibt die letzten
25 Beitraege zurueck. Wer nur den juengsten Abzug liest, verliert alles Aeltere —
und genau das konnte Notion besser, weil dort jede Zeile stehen blieb. Deshalb
werden **alle** Abzuege in `outputs/instagram-insights/` gelesen und je Beitrag
der zuletzt gesehene Stand behalten.

🚨 **Zahlen wachsen nach.** Ein Reel vom Montag hat am Dienstag mehr Reichweite
als am Montag. Beim Zusammenfuehren gewinnt deshalb der **neueste** Abzug, nicht
der erste — und je Beitrag steht dabei, von wann seine Zahlen sind.

🚨 **Die Engagement-Rate wird auf die Reichweite gerechnet, nicht auf die
Follower.** Bei zwei Konten mit rund 2'000 und rund 60 Followern waere die
Follower-Rate zweimal etwas anderes und nicht vergleichbar. Interaktionen je
erreichte Person ist die Zahl, die beide Profile vergleichbar macht.
"""

import glob
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]
QUELLE = ROOT / "outputs" / "instagram-insights"
GEPLANT = ROOT / "outputs" / "cockpit" / "inhalte-roh"

# Wie viele Zeichen vom Caption-Anfang fuer den Abgleich mit der Planung.
# 🚨 Kurz genug, dass eine spaetere Korrektur am Caption-Ende nichts kaputt
# macht, lang genug, dass zwei Beitraege nicht zufaellig gleich anfangen.
ABGLEICH_ZEICHEN = 38

# --- Reife und Recycling -----------------------------------------------
# 🚨 **Zahlen wachsen die ersten Tage noch.** Wer einen Beitrag am Tag nach dem
# Posten bewertet, bewertet den Start, nicht das Ergebnis. Erst ab hier gilt
# eine Zahl als ausgereift — bis dahin steht sie zwar da, zaehlt aber weder
# in den Median noch als Recycling-Kandidat.
REIF_AB_TAGEN = 7

# Fruehestens so lange nach dem Posten darf derselbe Inhalt wieder raus.
# Entspricht der 4-Wochen-Repost-Regel aus `reels-framework.md`.
RECYCLING_AB_TAGEN = 28

# Ab wann ein Beitrag „gut gelaufen" heisst. Beides **relativ zum eigenen
# Konto**: bei rund 2'000 gegen rund 60 Follower waere jede absolute Schwelle
# fuer eines der beiden Profile sinnlos.
RECYCLING_REACH_FAKTOR = 1.4   # das Wievielfache des eigenen Medians
RECYCLING_RATE = 1.5           # oder: Interaktionen je erreichte Person in %

# 🚨 **Eine hohe Rate allein reicht NICHT.** Beim ersten Lauf am 24.09.2026
# standen zwei Beitraege mit 112 und 89 Reichweite als Recycling-Kandidaten da —
# bei einem Median von 170. Ihre Rate lag ueber 1.5 %, weil zwei Interaktionen
# auf 112 erreichte Personen rechnerisch 1.8 % sind. Eine Quote wird umso
# zappeliger, je kleiner der Nenner ist; bei 89 Erreichten entscheidet ein
# einzelner Kommentar ueber „gut" oder „schlecht".
#
# Was wiederverwendet werden soll, hat **viele Leute erreicht UND bewegt**.
# Deshalb ist die Reichweite ab jetzt die Pflichtbedingung, und die Rate darf
# nur noch zusaetzlich qualifizieren.
RECYCLING_MIN_INTERAKTIONEN = 3   # unter dieser Zahl ist jede Quote Zufall

# --- Ausreisser nach oben ------------------------------------------------
# 🚨 **Ein Einschlag ist kein Recycling-Fall.** Am 24.09.2026 lagen im Archiv
# zwei Beitraege mit 1'328 und 892 Reichweite bei einem Median von 170 — das
# 7.8- und 5.2-Fache. Danach kommt ein Sprung auf 2.4x. Solche Beitraege in
# derselben Liste wie „lief ordentlich" zu fuehren, heisst sie zu verlieren.
AUSREISSER_FAKTOR = 2.5

# 🚨 **Und beide hatten eine RATE von 0.45 %** — also weit unterdurchschnittlich.
# Viel Reichweite und viel Reaktion sind zwei verschiedene Funde:
#   • Reichweiten-Einschlag: der Hook zieht Fremde an, die Patricia nicht kennen.
#     Daraus baut man Reichweite — Serie, zweites Format, Anzeige.
#   • Reaktions-Einschlag: die eigene Leute antworten. Daraus baut man Leads —
#     derselbe Gedanke nochmal, diesmal mit Keyword-CTA.
# Wer beides in eine Zahl wirft, bekommt fuer beide den falschen Rat.
AUSREISSER_RATE = 2.5   # ab hier gilt die Reaktion als Einschlag

# 🚨 **Ein Einschlag muss selten sein, sonst ist er keiner.** Ueber die volle
# Historie (541 Beitraege, zwei Jahre) kamen mit den Regeln oben **123**
# Einschlaege heraus — 23 % aller Beitraege. Das ist keine Fundliste mehr,
# das ist eine Bestenliste mit zu langem Schwanz. Ursache: 2025 war ein
# starkes Jahr (87 davon), und der Median ueber zwei Jahre ist eine andere
# Basis als der ueber die letzten Wochen.
#
# Deshalb zwei getrennte Dinge:
#   • `einschlag_aktuell` — dasselbe, aber nur aus den letzten 90 Tagen.
#     Das ist die Arbeitsliste: gerade passiert, jetzt handeln.
#   • `bestenliste` — die staerksten ueberhaupt, zeitlos. Kein Handlungsdruck,
#     aber man sollte wissen, was je funktioniert hat.
EINSCHLAG_AKTUELL_TAGE = 90

# 🚨 **Recycling nur aus den letzten zwoelf Monaten.** Ueber die ganze
# Historie waeren es 223 Kandidaten — und die aeltesten stammen aus der alten
# Positionierung. Inhaltlich wiederverwenden kann man nur, was noch zur
# heutigen Ausrichtung passt.
RECYCLING_BIS_TAGEN = 365

# 🚨 **Beitraege aus der alten Positionierung sind keine Vorlage.** Patricia am
# 24.09.2026: *„die beiträge von der alten positionierung musst du nicht
# miteinbauen"*. Sie bleiben im Archiv — die Historie ist echt und gehoert ihr —
# aber sie erscheinen nicht als Einschlag, nicht in der Bestenliste und nicht
# als Recycling-Vorschlag. Was man wiederverwendet, muss zur heutigen
# Ausrichtung passen.
#
# Das Datum ist **aus den Daten gelesen, nicht geraten**: zaehlt man je Monat
# Beitraege mit Network-/Business-Vokabular gegen solche mit Mama-Balance-
# Vokabular, kippt es im Juli 2025 klar (5:0), davor liegt jeder Monat auf der
# alten Seite. Juni 2025 ist thematisch neutral, also der Uebergang.
# Stimmt das Datum nicht, ist hier die eine Stelle zum Aendern.
POSITIONIERUNG_AB = "2025-07-01"

# 🚨 **Ein Artifact-Dokument darf hoechstens 256 KB gross sein.** Mit allen
# 541 Beitraegen waren es 432 KB — der Schreibvorgang waere abgelehnt worden.
# Und 541 Karten untereinander sind ohnehin keine Ansicht.
#
# Deshalb zwei Dateien:
#   • `gepostet.json`       — was ins Cockpit geht: die juengeren Beitraege.
#   • `gepostet-voll.json`  — das ganze Archiv, bleibt im Workspace.
# Median, Bestenliste und Zaehlungen werden **ueber alles** gerechnet und dann
# mitgegeben — sonst waere der Median der eines Ausschnitts.
COCKPIT_TAGE = 400

# Patricias Einordnungsfelder — die vier, die sie am 24.09. genannt hat, plus
# die drei aus demselben Notion-Schema. 🚨 Die Optionen sind **abgeschrieben aus
# Notion**, nicht erfunden: Content-Strategie-DB und die select-Felder der
# Content-Management-DB, gelesen am 24.09.2026. Wer hier eine Option dazu
# erfindet, bekommt eine Auswahl, die niemand je gepflegt hat.
FELDER = [
    {"k": "saeule", "l": "Content-Säule",
     "opt": ["Persönlichkeit", "Inspiration", "Expertise"],
     "hinweis": "PIE — Soll 35 / 35 / 30"},
    {"k": "ueberthema", "l": "Überthema",
     "opt": ["Networkmarketing 2.0", "Hybridmodell", "Mama-CEO",
             "Zurück zu deiner Energie", "Wake-Up — wenn dein Körper spricht",
             "Rückkehr zu dir"]},
    {"k": "produkt", "l": "Zahlt ein auf", "opt": "__angebote__",
     "hinweis": "kommt aus dem Angebots-Katalog"},
    {"k": "launchphase", "l": "Launch-Phase",
     "opt": ["", "Aufwärmphase", "Secret Offer", "Verkaufsphase",
             "Nachkaufphase", "Evergreen"],
     "hinweis": "nur wenn gerade einer lief"},
    {"k": "jobsaeule", "l": "Job-Säule",
     "opt": ["A-Autorität", "B-Story", "C-Reichweite", "D-Sales"]},
    {"k": "ziel", "l": "Ziel",
     "opt": ["Persönlichkeit zeigen", "Interaktion fördern", "Expertise zeigen",
             "Vertrauen aufbauen", "Reichweite aufbauen", "Verkaufen"]},
    {"k": "bewertung", "l": "Bewertung",
     "opt": ["", "⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"]},
]


def umschrift(s: str) -> str:
    """ae/oe/ue/ss zuerst, dann filtern.

    🚨 Wer direkt `[^a-z0-9]` filtert, macht aus „für" ein „fr" und findet den
    Treffer „fuer" nicht mehr. Dieselbe Falle wie beim Download-Aufraeumen.
    """
    s = s.lower()
    for a, b in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss")):
        s = s.replace(a, b)
    return re.sub(r"[^a-z0-9]", "", s)


def abzuege() -> list:
    """Alle Abzuege, aeltester zuerst — der neueste ueberschreibt."""
    raus = []
    for p in sorted(glob.glob(str(QUELLE / "20*.json"))):
        try:
            d = json.loads(Path(p).read_text(encoding="utf-8"))
        except Exception as e:
            print("  ⚠️ %s nicht lesbar (%s)" % (Path(p).name, e))
            continue
        raus.append((d.get("stand") or Path(p).stem, d))
    return raus


def geplante_beitraege() -> list:
    """Was im Cockpit geplant war — fuer die Bruecke Hook -> Reichweite."""
    raus = []
    for art in ("reels", "karussells"):
        ordner = GEPLANT / art
        if not ordner.is_dir():
            continue
        for datei in ordner.glob("*.json"):
            try:
                b = json.loads(datei.read_text(encoding="utf-8"))
            except Exception:
                continue
            cap = (b.get("caption") or "").strip()
            if not cap:
                continue
            raus.append({
                "id": b.get("id", datei.stem),
                "name": (b.get("name") or "")[:70],
                "hook": (b.get("hook") or "")[:160],
                "art": "Reel" if art == "reels" else "Karussell",
                "profil": b.get("profil") or "",
                "schluessel": umschrift(cap)[:ABGLEICH_ZEICHEN],
            })
    return raus


def main():
    ziel = Path(sys.argv[1]) if len(sys.argv) > 1 else \
        ROOT / "outputs" / "cockpit" / "abgleich"
    ziel.mkdir(parents=True, exist_ok=True)

    alle = abzuege()
    if not alle:
        sys.exit("Keine Abzuege in %s — erst `python scripts/instagram-insights/holen.py`"
                 % QUELLE)

    # Beitraege ueber alle Abzuege zusammenfuehren. Schluessel ist die
    # Instagram-ID, damit ein geaenderter Caption-Anfang nichts doppelt anlegt.
    beitraege = {}
    follower_verlauf = {}

    for stand, d in alle:
        for k in d.get("konten") or []:
            handle = k.get("handle", "")
            if k.get("follower"):
                follower_verlauf.setdefault(handle, {})[stand] = k["follower"]
            for b in k.get("beitraege") or []:
                bid = b.get("id")
                if not bid:
                    continue
                reach = b.get("reach") or 0
                inter = b.get("total_interactions") or 0
                beitraege[bid] = {
                    "id": bid,
                    "handle": handle,
                    "datum": b.get("datum", ""),
                    "typ": b.get("typ", ""),
                    "link": b.get("link", ""),
                    "anfang": b.get("anfang") or "",
                    "reach": reach,
                    "likes": b.get("likes") or 0,
                    "kommentare": b.get("kommentare") or 0,
                    "saved": b.get("saved") or 0,
                    "shares": b.get("shares") or 0,
                    "interaktionen": inter,
                    # Auf die Reichweite gerechnet, siehe Kopf.
                    "rate": round(inter / reach * 100, 2) if reach else None,
                    "zahlen_vom": stand,
                }

    # Bruecke zur Planung: welcher Hook hat diese Reichweite erzeugt?
    plan = geplante_beitraege()
    getroffen = 0
    for b in beitraege.values():
        s = umschrift(b["anfang"])[:ABGLEICH_ZEICHEN]
        if not s:
            continue
        for p in plan:
            if p["schluessel"] and p["schluessel"] == s:
                b["geplant_als"] = p["name"]
                b["hook"] = p["hook"]
                b["art"] = p["art"]
                getroffen += 1
                break

    liste = sorted(beitraege.values(), key=lambda x: x["datum"], reverse=True)

    # Alter und Reife je Beitrag.
    heute = date.today()
    for b in liste:
        try:
            b["alter_tage"] = (heute - date.fromisoformat(b["datum"])).days
        except Exception:
            b["alter_tage"] = None
        b["reif"] = b["alter_tage"] is not None and b["alter_tage"] >= REIF_AB_TAGEN

    # Median je Konto — und zwar nur ueber die ausgereiften Beitraege.
    # 🚨 Ein Beitrag von gestern zieht den Median sonst nach unten und laesst
    # die ganze Woche schlechter aussehen, als sie ist.
    medianwerte = {}
    for handle in set(b["handle"] for b in liste):
        werte = sorted(b["reach"] for b in liste
                       if b["handle"] == handle and b["reif"] and b["reach"] > 0)
        medianwerte[handle] = werte[len(werte) // 2] if werte else 0

    for b in liste:
        b["alte_positionierung"] = bool(b["datum"] and b["datum"] < POSITIONIERUNG_AB)

    for b in liste:
        m = medianwerte.get(b["handle"], 0)
        b["median_konto"] = m
        # Pflicht: mindestens der eigene Median. Darueber hinaus entweder
        # deutlich mehr Reichweite oder eine gute Rate mit genug Substanz.
        ueber_median = bool(m) and b["reach"] >= m
        deutlich = bool(m) and b["reach"] >= m * RECYCLING_REACH_FAKTOR
        starke_rate = (b["rate"] is not None and b["rate"] >= RECYCLING_RATE
                       and b["interaktionen"] >= RECYCLING_MIN_INTERAKTIONEN)
        b["gut_gelaufen"] = bool(b["reif"] and not b["alte_positionierung"]
                                 and ueber_median and (deutlich or starke_rate))

        # Einschlag — und welcher Art. Siehe Kommentar bei AUSREISSER_FAKTOR.
        b["faktor"] = round(b["reach"] / m, 2) if m else None
        weit_oben = bool(m) and b["reach"] >= m * AUSREISSER_FAKTOR
        # 🚨 Auch hier die Reichweite als Pflichtbasis — derselbe Fehler wie
        # bei `starke_rate`, und ich bin zweimal hineingelaufen: ein Beitrag
        # mit 89 Erreichten und 3 Interaktionen stand als „Einschlag" da, weil
        # das rechnerisch 3.37 % sind. **Jede Quote braucht eine Mindestbasis,
        # sonst misst sie den Zufall.**
        viel_reaktion = (ueber_median
                         and b["rate"] is not None and b["rate"] >= AUSREISSER_RATE
                         and b["interaktionen"] >= RECYCLING_MIN_INTERAKTIONEN)
        b["einschlag"] = bool(b["reif"] and not b["alte_positionierung"]
                              and (weit_oben or viel_reaktion))
        if not b["einschlag"]:
            b["einschlag_art"] = ""
        elif weit_oben and viel_reaktion:
            b["einschlag_art"] = "beides"
        elif weit_oben:
            b["einschlag_art"] = "reichweite"
        else:
            b["einschlag_art"] = "reaktion"
        b["einschlag_aktuell"] = bool(b["einschlag"]
                                      and b["alter_tage"] is not None
                                      and b["alter_tage"] <= EINSCHLAG_AKTUELL_TAGE)
        # Kandidat heisst: gut gelaufen UND lange genug her.
        b["recycling"] = bool(b["gut_gelaufen"]
                              and b["alter_tage"] is not None
                              and RECYCLING_AB_TAGEN <= b["alter_tage"] <= RECYCLING_BIS_TAGEN)

    # Follower-Zuwachs je Konto zwischen erstem und letztem Abzug.
    # 🚨 Nur ausweisen, wenn es mindestens zwei Staende gibt — sonst waere die
    # Zahl eine Behauptung.
    follower = {}
    for handle, staende in follower_verlauf.items():
        punkte = sorted(staende.items())
        follower[handle] = {
            "verlauf": [{"stand": s, "wert": w} for s, w in punkte],
            "aktuell": punkte[-1][1],
            "zuwachs": (punkte[-1][1] - punkte[0][1]) if len(punkte) > 1 else None,
            "seit": punkte[0][0] if len(punkte) > 1 else None,
        }

    neuster = alle[-1][0]
    try:
        alter = (date.today() - date.fromisoformat(neuster)).days
    except Exception:
        alter = None

    daten = {
        "stand": neuster,
        "alter_tage": alter,
        "veraltet": alter is not None and alter >= 3,
        "abzuege": [s for s, _ in alle],
        "beitraege": liste,
        "follower": follower,
        # Die Auswahllisten reisen mit den Daten mit. Sonst stuenden sie im
        # Cockpit-Code und muessten bei jeder Aenderung von Hand nachgezogen
        # werden — genau die Doppelpflege, die hier abgeschafft wird.
        "felder": FELDER,
        "bestenliste": [b["id"] for b in sorted(
            [x for x in liste if x["reif"] and not x["alte_positionierung"]],
            key=lambda x: -(x["reach"] or 0))[:10]],
        "regeln": {
            "reif_ab_tagen": REIF_AB_TAGEN,
            "recycling_ab_tagen": RECYCLING_AB_TAGEN,
            "reach_faktor": RECYCLING_REACH_FAKTOR,
            "rate": RECYCLING_RATE,
            "min_interaktionen": RECYCLING_MIN_INTERAKTIONEN,
            "ausreisser_faktor": AUSREISSER_FAKTOR,
            "ausreisser_rate": AUSREISSER_RATE,
            "einschlag_aktuell_tage": EINSCHLAG_AKTUELL_TAGE,
            "recycling_bis_tagen": RECYCLING_BIS_TAGEN,
            "positionierung_ab": POSITIONIERUNG_AB,
        },
        "median_je_konto": medianwerte,
        "quelle": "outputs/instagram-insights (%d Abzüge)" % len(alle),
        "holen_mit": "python scripts/instagram-insights/holen.py",
        "gebaut": datetime.now().isoformat(timespec="seconds"),
    }

    (ziel / "gepostet-voll.json").write_text(
        json.dumps(daten, ensure_ascii=False, indent=2), encoding="utf-8")

    fuers_cockpit = dict(daten)
    fuers_cockpit["beitraege"] = [
        b for b in liste
        if b["alter_tage"] is not None and b["alter_tage"] <= COCKPIT_TAGE]
    fuers_cockpit["archiv_gesamt"] = len(liste)
    fuers_cockpit["archiv_datei"] = "outputs/cockpit/abgleich/gepostet-voll.json"
    # 🚨 Die Bestenliste darf nur Kennungen nennen, die auch mitkommen —
    # sonst zeigt das Cockpit leere Plaetze.
    dabei = set(b["id"] for b in fuers_cockpit["beitraege"])
    fuers_cockpit["bestenliste"] = [i for i in daten["bestenliste"] if i in dabei]

    # 🚨 Ohne `indent` — das spart rund ein Drittel und bringt die Datei unter
    # die 256-KB-Grenze. Diese Datei geht in die Datenbank, niemand liest sie
    # von Hand; die lesbare Fassung ist `gepostet-voll.json`.
    # Ausserdem raus: `median_konto` (steht schon in `median_je_konto`) und
    # `interaktionen` (die Rate daraus ist bereits gerechnet).
    for b in fuers_cockpit["beitraege"]:
        b.pop("median_konto", None)
        b.pop("interaktionen", None)
    (ziel / "gepostet.json").write_text(
        json.dumps(fuers_cockpit, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8")

    kb = (ziel / "gepostet.json").stat().st_size / 1024
    if kb > 250:
        print("  ⚠️ %.0f KB — ueber der 256-KB-Grenze. COCKPIT_TAGE senken." % kb)
    print("  Cockpit: %d Beitraege (%.0f KB) · Archiv: %d Beitraege"
          % (len(fuers_cockpit["beitraege"]), kb, len(liste)))

    print("  %d Abzüge gelesen: %s" % (len(alle), ", ".join(daten["abzuege"])))
    alt_anz = len([b for b in liste if b.get("alte_positionierung")])
    print("  %d Beiträge im Archiv (%d davon aus der alten Positionierung, "
          "vor %s — bleiben drin, aber nie als Vorschlag)"
          % (len(liste), alt_anz, POSITIONIERUNG_AB))
    reif = [b for b in liste if b["reif"]]
    gut = [b for b in liste if b["gut_gelaufen"]]
    rec = [b for b in liste if b["recycling"]]
    print("  %d ausgereift (mindestens %d Tage alt)" % (len(reif), REIF_AB_TAGEN))
    print("  %d davon überdurchschnittlich gelaufen" % len(gut))
    print("  %d davon alt genug zum Wiederverwenden (ab %d Tagen)"
          % (len(rec), RECYCLING_AB_TAGEN))
    ein = [b for b in liste if b["einschlag_aktuell"]]
    if ein:
        print("")
        print("  🎯 %d Einschl%s in den letzten %d Tagen:"
              % (len(ein), "ag" if len(ein) == 1 else "äge", EINSCHLAG_AKTUELL_TAGE))
        for b in sorted(ein, key=lambda x: -(x["faktor"] or 0))[:6]:
            print("     %s  %5d  %sx Median  %s%%  [%s]  %s"
                  % (b["datum"], b["reach"], b["faktor"], b["rate"],
                     b["einschlag_art"], b["anfang"][:38]))
    print("  %d davon einem geplanten Beitrag zugeordnet" % getroffen)
    if plan and not getroffen:
        print("  ⚠️ Keine Zuordnung — Caption im Cockpit anders als auf Instagram?")
    for h, f in follower.items():
        zu = ("  %+d seit %s" % (f["zuwachs"], f["seit"])) if f["zuwachs"] is not None \
             else "  (Zuwachs erst ab dem zweiten Abzug)"
        print("  @%s: %d Follower%s" % (h, f["aktuell"], zu))
    if daten["veraltet"]:
        print("\n  ⚠️ Die Zahlen sind %d Tage alt." % alter)
    print("\nAbgelegt in: %s" % (ziel / "gepostet.json"))


if __name__ == "__main__":
    main()
