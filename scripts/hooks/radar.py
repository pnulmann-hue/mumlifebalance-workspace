"""Markt-Radar — warum ein Reel gelaufen ist, je Konto, mit Blick ins Video.

Patricia am 30.10.2026 über Content Radar: *„übernehme und analysiere bitte das system.
vielleicht können wir das für mich auch bauen?“* Plan: `plans/2026-10-30-markt-radar.md`,
Befund: `outputs/strategie/2026-10-30-content-radar-befund.md`.

**Was es macht (je Konto):**
1. die 10 stärksten und 5 schwächsten Reels gegen den Median des eigenen Kontos
2. drei Standbilder je Reel (0,2 s · 1 s · 3 s) per ffmpeg, sonst das Titelbild
3. Claude schreibt je Beitrag: warum es lief, Hook-Note, Bild-Note, was im Bild steht
4. Claude schreibt den Bericht: Hebel · sofort · vermeiden · Muster mit Zahlen
5. 🚨 der Bericht läuft durch `texte-pruefen.py` und eigene Regel-Prüfungen, bevor er
   abgelegt wird, und wird bei einem Fund einmal neu geschrieben
6. für ihr eigenes Konto: Reichweite nach Stunde und Wochentag (ab 5 Beiträgen je Feld)

**Was es bewusst nicht macht** (Befund vom 30.10.): Caption-Abbrüche als „Cliffhanger“
lesen — wir geben die volle Caption, und wo sie gekürzt ist, steht das dabei · „beste Zeit“
aus zwei Beiträgen · Zahlen erfinden · einen Wochenplan schreiben (das bleibt `/content`).

**Woher die Daten kommen:**
- eigenes Konto: alle Abzüge in `outputs/instagram-insights/*.json`, Videos frisch über die
  Meta-Schnittstelle (`media_url`, Zugang aus `scripts/meta-ads/.env`)
- andere Konten: der jüngste `outputs/apify-runs/tiefe-*.json`, in dem das Konto vorkommt.
  🚨 Die Video-Adressen von Instagram verfallen nach wenigen Tagen. Ist der Abzug alt,
  kommen keine Standbilder, nur der Text — das Skript sagt es dazu. Frisch holen:
  `.github/workflows/apify-tiefe.yml` (HANDLES anpassen, pushen).

    python scripts/hooks/radar.py                       # eigenes Konto + alle Kern-Konten
    python scripts/hooks/radar.py --konten juliamueller._,reichweitenherz
    python scripts/hooks/radar.py --nur-eigen
    python scripts/hooks/radar.py --ohne-ki             # nur Auswahl und Uhrzeit, kostet nichts

Ausgabe: `outputs/marktrecherche/radar/JJJJ-MM-TT-<konto>.md` (gitignored, zitiert fremde
Hooks) und `outputs/cockpit/abgleich/markt-radar/<konto>.json` + `_index.json` fürs Cockpit
(Sammlung `markt-radar`). Zwischenspeicher je Beitrag: `outputs/cockpit/abgleich/markt-radar/cache.json`.
"""

import argparse
import base64
import datetime
import glob
import json
import os
import re
import statistics
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path
from typing import List, Literal
from zoneinfo import ZoneInfo

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]
AUS_MD = ROOT / "outputs" / "marktrecherche" / "radar"
AUS_JSON = ROOT / "outputs" / "cockpit" / "abgleich" / "markt-radar"
BILDER = AUS_JSON / "bilder"
CACHE = AUS_JSON / "cache.json"
WATCHLIST = ROOT / "context" / "competitor-watchlist.json"

EIGEN = "mumlifebalance_patricia_ulmann"
MODELL = "claude-opus-5-5"
TOP, FLOP = 10, 5
MIN_BEITRAEGE = 8          # darunter gibt es für das Konto keinen Bericht
MIN_AUFRUFE = 200          # fremde Reels darunter zählen nicht (Zufall)
MIN_REIF_TAGE = 7          # eigene Reels jünger als das sind noch nicht ausgereift
MIN_FELD = 5               # Uhrzeit: so viele Beiträge braucht ein Feld
# Seit diesem Tag gilt die heutige Ausrichtung (dieselbe Grenze wie scripts/cockpit/gepostet-bauen.py).
# Davor lief die alte „Mama-Balance“-Linie — deren Zahlen sagen über heute nichts.
POSITIONIERUNG_AB = "2025-07-01"
ZEITEN = (0.2, 1.0, 3.0)
ZONE = ZoneInfo("Europe/Zurich")
TAGE = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]


# ---------------------------------------------------------------- Hilfen

def lies(p, leer=None):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except Exception:
        return leer


def schreib(p, daten):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(json.dumps(daten, ensure_ascii=False, indent=1), encoding="utf-8")
    tmp.replace(p)          # erst fertig schreiben, dann ersetzen: ein Fehler leert die alte Datei nicht


def median(werte):
    w = [x for x in werte if x is not None]
    return statistics.median(w) if w else 0


def anthropic_bereit():
    if not os.environ.get("ANTHROPIC_API_KEY"):
        env = ROOT / ".env"
        if env.exists():
            for zeile in env.read_text(encoding="utf-8").splitlines():
                if zeile.startswith("ANTHROPIC_API_KEY="):
                    os.environ["ANTHROPIC_API_KEY"] = zeile.split("=", 1)[1].strip().strip('"')
    return bool(os.environ.get("ANTHROPIC_API_KEY"))


def kern_konten():
    w = lies(WATCHLIST, {}) or {}
    return [a["handle"] for a in w.get("accounts", []) if a.get("nische") == "kern"
            and a["handle"] not in ("anni.hoffmann", "karriere.mum", "elke_mayr")]


# ---------------------------------------------------------------- Daten laden

def eigene_beitraege():
    """Je Beitrag der jüngste gesehene Stand über alle Abzüge — die API gibt nur die letzten heraus."""
    stand = {}
    for f in sorted(glob.glob(str(ROOT / "outputs" / "instagram-insights" / "*.json"))):
        d = lies(f, {}) or {}
        for k in d.get("konten", []):
            if k.get("handle") != EIGEN:
                continue
            for b in k.get("beitraege", []):
                b = dict(b, zahlen_vom=Path(f).stem)
                stand[b["id"]] = b
    heute = datetime.date.today()
    raus = []
    for b in stand.values():
        try:
            alter = (heute - datetime.date.fromisoformat(b["datum"])).days
        except Exception:
            continue
        raus.append({
            "id": b["id"], "konto": EIGEN, "typ": "Reel" if b.get("typ") == "REELS" else "Karussell/Bild",
            "datum": b["datum"], "zeitpunkt": b.get("zeitpunkt"), "link": b.get("link"),
            "caption": b.get("caption") or b.get("anfang") or "",
            "caption_gekuerzt": len(b.get("caption") or "") <= 95,
            "wert": b.get("reach") or 0, "masz": "Reichweite",
            "likes": b.get("likes") or 0, "kommentare": b.get("kommentare") or 0,
            "saves": b.get("saved") or 0, "shares": b.get("shares") or 0,
            "alter": alter, "reif": alter >= MIN_REIF_TAGE and b["datum"] >= POSITIONIERUNG_AB,
        })
    return raus


def markt_beitraege(handle):
    """Der jüngste Tiefen-Abzug, in dem das Konto vorkommt."""
    for f in sorted(glob.glob(str(ROOT / "outputs" / "apify-runs" / "tiefe-*.json")), reverse=True):
        d = lies(f, {}) or {}
        posts = [p for p in d.get("posts", []) if p.get("ownerUsername") == handle]
        if not posts:
            continue
        stand = d.get("date") or Path(f).stem[6:16]
        raus = []
        for p in posts:
            ist_reel = p.get("type") == "Video" and p.get("productType") == "clips"
            wert = p.get("videoPlayCount") or p.get("videoViewCount") or 0
            raus.append({
                "id": p.get("shortCode"), "konto": handle, "typ": "Reel" if ist_reel else "Karussell/Bild",
                "datum": (p.get("timestamp") or "")[:10], "zeitpunkt": p.get("timestamp"),
                "link": p.get("url"), "caption": p.get("caption") or "", "caption_gekuerzt": False,
                "wert": wert if ist_reel else (p.get("likesCount") or 0) + (p.get("commentsCount") or 0),
                "masz": "Aufrufe" if ist_reel else "Likes+Kommentare",
                "likes": max(p.get("likesCount") or 0, 0), "kommentare": p.get("commentsCount") or 0,
                "saves": None, "shares": None, "reif": True,
                "video_url": p.get("videoUrl"), "bild_url": p.get("displayUrl"),
                "dauer": p.get("videoDuration"),
            })
        return raus, stand, f
    return [], None, None


def auswahl(posts, eigen):
    """Reels mit Faktor gegen den Median des Kontos — nie absolut, die Konten sind verschieden gross."""
    reels = [p for p in posts if p["typ"] == "Reel" and p["reif"]
             and (eigen or p["wert"] >= MIN_AUFRUFE)]
    if len(reels) < MIN_BEITRAEGE:
        return None
    m = median(p["wert"] for p in reels)
    for p in reels:
        p["faktor"] = round(p["wert"] / m, 2) if m else 0
        p["rate"] = round(100 * (p["likes"] + p["kommentare"] + (p["saves"] or 0) + (p["shares"] or 0)) / p["wert"], 2) if p["wert"] else 0
    reels.sort(key=lambda p: p["faktor"], reverse=True)
    # Derselbe Beitrag zweimal gepostet zählt einmal (der stärkere), sonst steht er doppelt in den Top 10
    gesehen, eindeutig = {}, []
    for p in reels:
        k = re.sub(r"\W+", "", p["caption"].lower())[:60]
        if k and k in gesehen:
            gesehen[k]["wiederholt"] = gesehen[k].get("wiederholt", 1) + 1
            continue
        gesehen[k] = p
        eindeutig.append(p)
    top = eindeutig[:TOP]
    # Schwächste nur mit genug Basis — bei 7 Reichweite misst die Zahl den Zufall
    boden = max(50, m * 0.15) if eigen else MIN_AUFRUFE
    flop = [p for p in eindeutig if p["wert"] >= boden and p not in top][-FLOP:]
    for p in top:
        p["gruppe"] = "top"
    for p in flop:
        p["gruppe"] = "flop"
    return {"median": m, "anzahl": len(reels), "masz": reels[0]["masz"], "top": top, "flop": flop}


# ---------------------------------------------------------------- Bilder

def meta_konten():
    sys.path.insert(0, str(ROOT / "scripts" / "instagram-insights"))
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("holen", ROOT / "scripts" / "instagram-insights" / "holen.py")
        holen = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(holen)
        return holen, holen.konten(holen.zugang())
    except SystemExit as e:
        print(f"  ⚠ Meta-Zugang: {e}")
    except Exception as e:
        print(f"  ⚠ Meta-Zugang: {e}")
    return None, []


def eigene_medien(p, holen, konten):
    for k in konten:
        if k.get("handle") == EIGEN:
            d = holen.hole(p["id"], k["token"], fields="media_url,thumbnail_url")
            return d.get("media_url"), d.get("thumbnail_url")
    return None, None


def laden(url, ziel):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=60) as r:
            ziel.write_bytes(r.read())
        return ziel.stat().st_size > 1000
    except Exception:
        return False


def standbilder(p, holen=None, konten=()):
    """Drei Standbilder (oder das Titelbild). Liegen schon welche da, werden sie wiederverwendet."""
    ordner = BILDER / p["konto"]
    ordner.mkdir(parents=True, exist_ok=True)
    vorhanden = sorted(ordner.glob(f"{p['id']}_*.jpg"))
    if vorhanden:
        return vorhanden, "video" if len(vorhanden) > 1 else "titelbild"
    video, bild = p.get("video_url"), p.get("bild_url")
    if p["konto"] == EIGEN and holen:
        video, bild = eigene_medien(p, holen, konten)
    with tempfile.TemporaryDirectory() as tmp:
        if video:
            datei = Path(tmp) / "v.mp4"
            if laden(video, datei):
                raus = []
                for i, t in enumerate(ZEITEN):
                    ziel = ordner / f"{p['id']}_{i}.jpg"
                    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(t), "-i", str(datei),
                                    "-frames:v", "1", "-vf", "scale=360:-2", "-q:v", "5", str(ziel)])
                    if ziel.exists():
                        raus.append(ziel)
                if raus:
                    return raus, "video"
        if bild:
            roh = Path(tmp) / "b.jpg"
            if laden(bild, roh):
                ziel = ordner / f"{p['id']}_0.jpg"
                subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(roh),
                                "-vf", "scale=360:-2", "-q:v", "5", str(ziel)])
                if ziel.exists():
                    return [ziel], "titelbild"
    return [], "keins"


def vorschau(bild):
    """Kleines Bild fürs Cockpit — ein Dokument darf nur 256 KB haben."""
    with tempfile.TemporaryDirectory() as tmp:
        ziel = Path(tmp) / "k.jpg"
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(bild), "-vf", "scale=150:-2",
                        "-q:v", "9", str(ziel)])
        if ziel.exists():
            return "data:image/jpeg;base64," + base64.b64encode(ziel.read_bytes()).decode()
    return None


# ---------------------------------------------------------------- Claude

REGELN = """Patricias feste Regeln (sie gelten für JEDEN Vorschlag, den du machst):
- Sie schreibt für Mamas im Network und mit eigenem Business. Deren Kundschaft ist NICHT weiblich: nie „deine Kundin“, sondern „deine Kundschaft“, „die Leute, für die du schreibst“.
- Das Stichwort (Kommentier WORT) steht NUR am Schluss einer Caption, nie am Anfang oder im Hook.
- Genau ein Aufruf je Beitrag.
- Kein Stakkato: ganze Sätze, keine Ein-Satz-Zeilen, keine Empfehlung „ein Satz pro Zeile“.
- Keine erfundenen Zahlen, Beträge, Kundinnen oder Erfolge. Zahlen nur, wenn sie belegt sind.
- „Nicht X, sondern Y“ ist verboten, auch umschrieben.
- Nie das Werkzeug im Hook (KI, Instagram, Kurs, Öle, Freebie).
- Jeder Hook hat einen Gegner, ein Geständnis oder ein Zitat. Der Gegner ist das System, die Upline, der Job — nie die Leserin.
- Keine Namen fremder Network-Firmen (sie ist selbst Beraterin).
- „Folge mir, wenn …“ als Einstieg ist bei ihr gemessen gefloppt.
- Schweizer Schreibweise: ss statt ß."""

ANLEITUNG_POST = """Du analysierst ein Instagram-Reel für Patricia (Mentorin für Mamas im Network).
Du bekommst: die Caption, die Zahlen, den Faktor gegen den Median des Kontos (1,0 = normal), ob es zu den
stärksten oder schwächsten des Kontos gehört, und bis zu drei Standbilder (0,2 s · 1 s · 3 s) oder das Titelbild.

Schreib auf Deutsch, Schweizer ss, sachlich, ohne Floskeln:
- warum: 2–3 Sätze, warum dieser Beitrag so lief. Stütz dich auf das, was du siehst und liest. Rate nicht über
  den Algorithmus. Ist die Caption als gekürzt markiert, werte das Ende NICHT als Absicht.
- hook: der Einstieg in eigenen Worten (Text im Bild, sonst erste Caption-Zeile), höchstens 20 Wörter, wörtlich wenn lesbar
- hook_note und bild_note: 1–10
- text_im_bild: was in den ersten Sekunden als Text zu sehen ist, wörtlich, sonst leer
- gesicht: ob eine Person zu sehen ist und wie (z.B. „spricht in die Kamera, lacht“), sonst „keins“
- ort: wo es aufgenommen ist, wenige Wörter
- muster: 1–3 kurze Stichworte, was den Beitrag ausmacht (z.B. „Zitat“, „Alltagsszene“, „Geständnis mit Jahreszahl“)"""

ANLEITUNG_BERICHT = """Du schreibst für Patricia den Bericht zu einem Instagram-Konto, auf Deutsch, Schweizer ss,
in ganzen Sätzen, ohne Floskeln und ohne KI-Wörter (eintauchen, Gamechanger, entfesseln …).
Du bekommst je Reel die Analyse, die Zahlen und den Faktor gegen den Median des Kontos — die stärksten und die schwächsten.

Jede Aussage braucht einen Beleg aus diesen Daten (Faktor, Anzahl, Beispiel-Hook). Keine Aussage über Beiträge,
die du nicht bekommen hast. Trenne Reichweite (Faktor) und Reaktion (Rate): ein Beitrag kann weit laufen und
trotzdem keine Reaktion bekommen — sag es, wenn das so ist.

Ist es ein FREMDES Konto: Schreib, was Patricia daraus für IHREN Content mitnehmen kann. Ist es IHR Konto: Schreib,
was sie ändern sollte.

""" + REGELN + """

Ein Vorschlag, der eine dieser Regeln bricht, gehört nicht in den Bericht, auch wenn das Konto damit Erfolg hat.
Dann steht er unter „passt nicht zu dir“ mit dem Grund."""


def client_holen():
    try:
        import anthropic
        return anthropic.Anthropic(), anthropic
    except ImportError:
        return None, None


def post_analysieren(client, anthropic, p, bilder, art):
    from pydantic import BaseModel

    class Analyse(BaseModel):
        warum: str
        hook: str
        hook_note: int
        bild_note: int
        text_im_bild: str
        gesicht: str
        ort: str
        muster: List[str]

    inhalt = []
    for b in bilder:
        inhalt.append({"type": "image", "source": {"type": "base64", "media_type": "image/jpeg",
                                                   "data": base64.b64encode(Path(b).read_bytes()).decode()}})
    zahlen = (f"Konto: {p['konto']} · {p['masz']}: {p['wert']} · Faktor gegen Median: {p['faktor']} · "
              f"Gruppe: {'stärkste' if p['gruppe'] == 'top' else 'schwächste'} des Kontos · Likes {p['likes']} · "
              f"Kommentare {p['kommentare']}" + (f" · Gespeichert {p['saves']} · Geteilt {p['shares']}" if p['saves'] is not None else "")
              + f" · Interaktionsrate {p['rate']} %")
    text = (f"{zahlen}\nBilder: {len(bilder)} ({art})\n"
            f"Caption{' (GEKÜRZT gespeichert — Ende nicht werten)' if p.get('caption_gekuerzt') else ''}:\n{p['caption'][:2500]}")
    inhalt.append({"type": "text", "text": text})
    try:
        r = client.messages.parse(model=MODELL, max_tokens=4000, output_config={"effort": "low"},
                                  system=ANLEITUNG_POST, messages=[{"role": "user", "content": inhalt}],
                                  output_format=Analyse)
    except (anthropic.APIStatusError, anthropic.APIConnectionError) as e:
        print(f"    ⚠ {p['id']}: {e.__class__.__name__}")
        return None
    return r.parsed_output.model_dump() if r.parsed_output else None


def bericht_schreiben(client, anthropic, konto, ausw, eigen, funde=None, vorher=None):
    from pydantic import BaseModel

    class Hebel(BaseModel):
        titel: str
        aufwand: Literal["klein", "mittel", "gross"]
        wirkung: int
        beleg: str

    class Punkt(BaseModel):
        text: str
        beleg: str

    class Bericht(BaseModel):
        zusammenfassung: str
        hebel: List[Hebel]
        sofort: List[str]
        vermeiden: List[Punkt]
        muster: List[Punkt]
        passt_nicht: List[Punkt]

    zeilen = []
    for p in ausw["top"] + ausw["flop"]:
        a = p.get("analyse") or {}
        zeilen.append(f"[{p['gruppe']}] Faktor {p['faktor']} · Rate {p['rate']} % · {p['masz']} {p['wert']} · "
                      f"Hook-Note {a.get('hook_note', '?')} · Bild-Note {a.get('bild_note', '?')}\n"
                      f"  Hook: {a.get('hook') or p['caption'][:120]}\n  Bild: {a.get('text_im_bild', '')} | "
                      f"{a.get('gesicht', '')} | {a.get('ort', '')}\n  Muster: {', '.join(a.get('muster', []))}\n"
                      f"  Warum: {a.get('warum', '')}")
    kopf = (f"{'IHR EIGENES' if eigen else 'FREMDES'} Konto: @{konto} · {ausw['anzahl']} Reels ausgewertet · "
            f"Median {ausw['masz']}: {round(ausw['median'])}\n\n")
    nachricht = kopf + "\n\n".join(zeilen)
    if funde:
        nachricht += ("\n\nDEIN ERSTER ENTWURF hatte diese Regelverstösse. Schreib den Bericht neu, ohne sie:\n"
                      + "\n".join(f"- {f}" for f in funde) + "\n\nErster Entwurf:\n" + vorher)
    try:
        r = client.messages.parse(model=MODELL, max_tokens=12000, output_config={"effort": "medium"},
                                  system=ANLEITUNG_BERICHT, messages=[{"role": "user", "content": nachricht}],
                                  output_format=Bericht)
    except (anthropic.APIStatusError, anthropic.APIConnectionError) as e:
        print(f"  ⚠ Bericht @{konto}: {e.__class__.__name__}")
        return None
    return r.parsed_output.model_dump() if r.parsed_output else None


# ---------------------------------------------------------------- Regelprüfung

EIGENE_PRUEFUNGEN = [
    (r"(?i)ein satz,? (eine?|pro) (zeile|umbruch)|zeilenumbr\w* nach jedem satz|jeder satz (auf )?eine eigene zeile", "Stakkato-Empfehlung"),
    (r"(?i)(als|im) (erste[nr]?|allerersten) satz[^.]{0,60}(kommentier|stichwort|keyword)|stichwort[^.]{0,40}(an den anfang|zu beginn|als ersten)", "Stichwort am Anfang"),
    (r"(?i)\bdeine?n? kundin(nen)?\b", "„deine Kundin“ (zweite Ebene)"),
    (r"(?i)folge mir,? wenn", "„Folge mir, wenn“"),
    (r"ß", "ß statt ss"),
    (r"(?i)\b(ringana|fitline|lr health|more nutrition|esn|pm-international|herbalife|young living)\b", "fremde Firma beim Namen"),
]


def bericht_md(konto, ausw, b, eigen, stand, art_info):
    t = ["---", "tags: [research, content, radar]", "---", "",
         f"# Markt-Radar · @{konto}" + (" (dein Konto)" if eigen else ""), "",
         f"Stand {datetime.date.today().isoformat()} · Daten vom {stand} · {ausw['anzahl']} Reels · "
         f"Median {ausw['masz']} {round(ausw['median'])} · {art_info}", "",
         "## Zusammenfassung", "", b["zusammenfassung"], "", "## Die wichtigsten Hebel", ""]
    for h in b["hebel"]:
        t.append(f"- **{h['titel']}** (Aufwand {h['aufwand']}, Wirkung {h['wirkung']}/10) — {h['beleg']}")
    t += ["", "## Sofort umsetzbar", ""] + [f"{i}. {s}" for i, s in enumerate(b["sofort"], 1)]
    t += ["", "## Das vermeiden", ""] + [f"- {v['text']} — {v['beleg']}" for v in b["vermeiden"]]
    t += ["", "## Muster mit Zahlen", ""] + [f"- **{m['text']}** — {m['beleg']}" for m in b["muster"]]
    if b.get("passt_nicht"):
        t += ["", "## Passt nicht zu dir", ""] + [f"- {m['text']} — {m['beleg']}" for m in b["passt_nicht"]]
    return "\n".join(t) + "\n"


def regeln_pruefen(md):
    """Blackliste über texte-pruefen.py plus die Regeln, die dort nicht stehen. Gibt die Funde zurück."""
    funde = []
    # „Passt nicht zu dir“ darf die verbotenen Dinge nennen — dort stehen sie als Warnung
    pruefteil = md.split("## Passt nicht zu dir")[0]
    for muster, name in EIGENE_PRUEFUNGEN:
        for m in re.finditer(muster, pruefteil):
            funde.append(f"{name}: „{pruefteil[max(0, m.start() - 40):m.end() + 40].strip()}“")
    with tempfile.TemporaryDirectory() as tmp:
        f = Path(tmp) / "bericht.md"
        f.write_text(pruefteil, encoding="utf-8")
        r = subprocess.run([sys.executable, str(ROOT / "scripts" / "cockpit" / "texte-pruefen.py"), "--datei", str(f)],
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        for zeile in r.stdout.splitlines():
            # nur echte Funde — die Schlusszeile „🔴 0 muss weg“ trägt das Zeichen auch
            if zeile.strip().startswith("🔴"):
                funde.append("Blackliste: " + zeile.strip(" 🔴"))
    return funde


# ---------------------------------------------------------------- Uhrzeit

def uhrzeit(posts):
    """Reichweite nach Stunde und Wochentag, getrennt nach Format, nur mit genug Beiträgen je Feld."""
    raus = {}
    for typ in ("Reel", "Karussell/Bild"):
        ps = [p for p in posts if p["typ"] == typ and p["reif"] and p.get("zeitpunkt") and p["wert"]]
        if not ps:
            continue
        gesamt = median(p["wert"] for p in ps)
        stunden, tage = {}, {}
        for p in ps:
            z = datetime.datetime.strptime(p["zeitpunkt"][:19], "%Y-%m-%dT%H:%M:%S").replace(
                tzinfo=datetime.timezone.utc).astimezone(ZONE)
            stunden.setdefault(z.hour, []).append(p["wert"])
            tage.setdefault(TAGE[z.weekday()], []).append(p["wert"])

        def tabelle(gruppen, reihenfolge):
            zeilen = []
            for k in reihenfolge:
                w = gruppen.get(k, [])
                if not w:
                    continue
                zeilen.append({"feld": k, "anzahl": len(w), "median": round(median(w)),
                               "faktor": round(median(w) / gesamt, 2) if gesamt else 0,
                               "genug": len(w) >= MIN_FELD})
            return zeilen

        st = tabelle(stunden, range(24))
        tg = tabelle(tage, TAGE)
        genug = [z for z in st if z["genug"]]
        raus[typ] = {
            "beitraege": len(ps), "median": round(gesamt), "stunden": st, "tage": tg,
            "beste_stunde": max(genug, key=lambda z: z["median"]) if genug else None,
            "schwaechste_stunde": min(genug, key=lambda z: z["median"]) if genug else None,
        }
    return raus


def uhrzeit_md(u):
    t = ["", "## Uhrzeit (aus deinen eigenen Zahlen)", "",
         f"Gezählt wird ein Feld erst ab {MIN_FELD} Beiträgen. Massstab ist der Median der Reichweite, "
         "nicht der Durchschnitt, sonst kippt ein einziger Ausreisser das Bild.", ""]
    for typ, w in u.items():
        t.append(f"**{typ}** ({w['beitraege']} Beiträge, Median {w['median']}):")
        if w["beste_stunde"]:
            b, s = w["beste_stunde"], w["schwaechste_stunde"]
            t.append(f"- stärkste Stunde {b['feld']}:00 (Median {b['median']}, {b['anzahl']} Beiträge) · "
                     f"schwächste {s['feld']}:00 (Median {s['median']}, {s['anzahl']} Beiträge)")
        else:
            t.append("- zu wenig Beiträge je Stunde für eine Aussage")
        t.append("- Wochentage: " + " · ".join(
            f"{z['feld']} {z['median']}" + ("" if z["genug"] else f" ({z['anzahl']}, zu wenig)") for z in w["tage"]))
        t.append("")
    return "\n".join(t)


# ---------------------------------------------------------------- Ablauf

def konto_auswerten(konto, ki, cache, holen, mkonten):
    eigen = konto == EIGEN
    if eigen:
        posts, stand, quelle = eigene_beitraege(), datetime.date.today().isoformat(), "Meta-Schnittstelle"
    else:
        posts, stand, quelle = markt_beitraege(konto)
    if not posts:
        print(f"@{konto}: keine Daten — übersprungen")
        return None
    ausw = auswahl(posts, eigen)
    if not ausw:
        print(f"@{konto}: zu wenig Reels (unter {MIN_BEITRAEGE}) — übersprungen")
        return None
    alt = (datetime.date.today() - datetime.date.fromisoformat(stand)).days if stand else 0
    print(f"@{konto}: {ausw['anzahl']} Reels, Median {round(ausw['median'])}, Daten vom {stand}"
          + (f" — {alt} Tage alt, Video-Adressen vermutlich verfallen" if alt > 3 and not eigen else ""))
    arten = {}
    for p in ausw["top"] + ausw["flop"]:
        bilder, art = standbilder(p, holen, mkonten)
        arten[art] = arten.get(art, 0) + 1
        p["bilder"] = [str(b.relative_to(ROOT)) for b in bilder]
        p["bild_art"] = art
        schl = f"{konto}:{p['id']}"
        if ki and (schl not in cache or (cache[schl].get("_bilder", 0) < len(bilder))):
            a = post_analysieren(*ki, p, bilder, art)
            if a:
                a["_bilder"] = len(bilder)
                cache[schl] = a
                schreib(CACHE, cache)
        p["analyse"] = cache.get(schl)
    art_info = "Bilder: " + ", ".join(f"{v}× {k}" for k, v in arten.items())
    print(f"  {art_info}")
    ergebnis = {"konto": konto, "eigen": eigen, "stand": stand, "quelle": str(quelle), "ausw": ausw,
                "art_info": art_info, "bericht": None, "funde": []}
    if eigen:
        ergebnis["uhrzeit"] = uhrzeit(posts)
    if not ki:
        return ergebnis
    b = bericht_schreiben(*ki, konto, ausw, eigen)
    if not b:
        return ergebnis
    md = bericht_md(konto, ausw, b, eigen, stand, art_info)
    funde = regeln_pruefen(md)
    if funde:
        print(f"  {len(funde)} Regelverstösse im ersten Entwurf — neu geschrieben")
        b2 = bericht_schreiben(*ki, konto, ausw, eigen, funde, md)
        if b2:
            b, md = b2, bericht_md(konto, ausw, b2, eigen, stand, art_info)
            funde = regeln_pruefen(md)
    ergebnis["bericht"], ergebnis["funde"] = b, funde
    if funde:
        print(f"  ⚠ {len(funde)} Verstösse bleiben — stehen im Bericht oben")
    return ergebnis


def ablegen(e):
    konto, ausw = e["konto"], e["ausw"]
    if e["bericht"]:
        md = bericht_md(konto, ausw, e["bericht"], e["eigen"], e["stand"], e["art_info"])
        if e["funde"]:
            md = md.replace("## Zusammenfassung", "> ⚠ Noch offene Regelverstösse:\n" +
                            "\n".join(f"> - {f}" for f in e["funde"]) + "\n\n## Zusammenfassung", 1)
        if e.get("uhrzeit"):
            md += uhrzeit_md(e["uhrzeit"])
        md += "\n## Die Beiträge\n\n"
        for p in ausw["top"] + ausw["flop"]:
            a = p.get("analyse") or {}
            md += (f"### {'▲' if p['gruppe'] == 'top' else '▼'} Faktor {p['faktor']} · {p['masz']} {p['wert']} · "
                   f"Rate {p['rate']} % · {p['datum']}\n\n**Hook:** {a.get('hook') or p['caption'][:120]}  \n"
                   f"**Im Bild:** {a.get('text_im_bild') or '—'} · {a.get('gesicht', '')} · {a.get('ort', '')}  \n"
                   f"**Warum:** {a.get('warum', '—')}  \n[Zum Beitrag]({p['link']})\n\n")
        AUS_MD.mkdir(parents=True, exist_ok=True)
        (AUS_MD / f"{datetime.date.today().isoformat()}-{konto}.md").write_text(md, encoding="utf-8")
    beitraege = []
    for p in ausw["top"] + ausw["flop"]:
        a = p.get("analyse") or {}
        bild = vorschau(ROOT / p["bilder"][0]) if p.get("bilder") else None
        beitraege.append({k: p.get(k) for k in ("id", "gruppe", "datum", "link", "wert", "masz", "faktor", "rate",
                                                 "likes", "kommentare", "saves", "shares", "bild_art", "wiederholt")}
                         | {"hook": a.get("hook") or p["caption"][:140], "warum": a.get("warum"),
                            "hook_note": a.get("hook_note"), "bild_note": a.get("bild_note"),
                            "text_im_bild": a.get("text_im_bild"), "gesicht": a.get("gesicht"),
                            "ort": a.get("ort"), "muster": a.get("muster", []), "bild": bild})
    doc = {"konto": konto, "eigen": e["eigen"], "stand": e["stand"], "erstellt": datetime.date.today().isoformat(),
           "anzahl": ausw["anzahl"], "median": round(ausw["median"]), "masz": ausw["masz"],
           "bilder": e["art_info"], "bericht": e["bericht"], "funde": e["funde"],
           "uhrzeit": e.get("uhrzeit"), "beitraege": beitraege}
    roh = json.dumps(doc, ensure_ascii=False)
    while len(roh.encode("utf-8")) > 240_000 and any(b.get("bild") for b in beitraege):
        for b in reversed(beitraege):          # zu gross: zuerst die Bilder der schwächsten weglassen
            if b.get("bild"):
                b["bild"] = None
                break
        roh = json.dumps(doc, ensure_ascii=False)
    schreib(AUS_JSON / f"{konto}.json", doc)
    return {"konto": konto, "eigen": e["eigen"], "stand": e["stand"], "anzahl": ausw["anzahl"],
            "median": round(ausw["median"]), "masz": ausw["masz"],
            "zusammenfassung": (e["bericht"] or {}).get("zusammenfassung", "")[:400]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--konten", help="Komma-Liste statt eigenes Konto + Kern-Nische")
    ap.add_argument("--nur-eigen", action="store_true")
    ap.add_argument("--ohne-ki", action="store_true")
    a = ap.parse_args()
    konten = [EIGEN] if a.nur_eigen else ([k.strip() for k in a.konten.split(",")] if a.konten else [EIGEN] + kern_konten())
    ki = None
    if not a.ohne_ki:
        if anthropic_bereit():
            ki = client_holen()
            if not ki[0]:
                ki = None
        if not ki:
            print("⚠ Kein Claude-Zugang — nur Auswahl und Uhrzeit.")
    holen, mkonten = meta_konten() if EIGEN in konten else (None, [])
    cache = lies(CACHE, {}) or {}
    index = lies(AUS_JSON / "_index.json", {"konten": []}) or {"konten": []}
    alt = {k["konto"]: k for k in index.get("konten", [])}
    for konto in konten:
        e = konto_auswerten(konto, ki, cache, holen, mkonten)
        if e:
            alt[konto] = ablegen(e)
    index = {"stand": datetime.date.today().isoformat(), "konten": sorted(alt.values(), key=lambda k: (not k["eigen"], k["konto"]))}
    schreib(AUS_JSON / "_index.json", index)
    print(f"\n→ {AUS_JSON.relative_to(ROOT)} ({len(index['konten'])} Konten) · Berichte in {AUS_MD.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
