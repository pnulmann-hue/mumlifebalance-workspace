"""
Traegt die echten Business-Daten fuer das Cockpit zusammen.

Im Cockpit stand bisher ein Startbestand von Hand. Die richtigen Daten liegen
laengst im Workspace und in ActiveCampaign — sie waren nur nie verbunden.
Dieses Skript sammelt sie und legt sie als JSON-Dokumente ab; hochgeladen
werden sie danach mit `Artifact write_db`.

Quellen:
  context/active-funnels.json   Angebote, Preise, Links, Keywords, AC-Tags
  context/manychat-keywords.md  alle Keywords beider Profile
  outputs/finanzen/**           Umsatz pro Monat (falls vorhanden)
  ActiveCampaign                Listen und Automationen — direkt ueber die API,
                                Zugang aus 04-projects/activecampaign-mcp/.env.
                                Fehlt die, reicht `--ac ac-daten.json` als Ersatz

Aufruf:
  python scripts/cockpit/daten-abgleich.py [zielordner] [--ac ac-daten.json]
"""
import json
import re
import sys
from datetime import date
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]


def lade_funnels():
    p = ROOT / "context" / "active-funnels.json"
    if not p.exists():
        return []
    return json.loads(p.read_text(encoding="utf-8")).get("funnels", [])


def stufe_von(f):
    """Aus Typ und Preis die Stufe der Produkttreppe ableiten."""
    preis = f.get("preis_chf")
    # Nur eine ausdrueckliche Null ist ein Freebie. Fehlt der Preis, ist es ein
    # Angebot mit offenem Preis — sonst landen 333er-Kurse bei den Freebies.
    if preis in (0, "0") or "0€" in (f.get("typ") or ""):
        return "Freebie"
    try:
        p = float(preis)
    except (TypeError, ValueError):
        return "Angebot"
    if p <= 49:
        return "Mini-Kurs"
    if p <= 150:
        return "Kurs"
    if p <= 500:
        return "Signature-Kurs"
    return "Programm"


def produkte_bauen(funnels):
    """Jedes Angebot einmal, mit Preis, Link, Keyword und Status."""
    raus = []
    for f in funnels:
        quellen = f.get("traffic_quellen") or {}
        link = (quellen.get("wordpress_landing") or quellen.get("checkout")
                or quellen.get("tool_direct") or "")
        keyword = (quellen.get("manychat_keyword") or "").split(" (")[0]
        preis = f.get("preis_chf")
        raus.append({
            "id": "a-" + f["id"],
            "name": f.get("name", f["id"]),
            "stufe": stufe_von(f),
            "preis": "0" if preis in (0, "0") else ("CHF %s" % preis if preis else ""),
            "keyword": keyword,
            "link": link,
            "status": {"live": "Live", "in-aufbau": "In Arbeit"}.get(
                (f.get("status") or "").split("-")[0], f.get("status", "")),
        })
    return raus


def kurztext(wert, laenge=90):
    """Ein Feld als kurzer Text — egal ob dort Text, Liste oder Objekt steht.

    Die Funnel-Datei ist ueber Monate gewachsen, die Felder sind uneinheitlich.
    """
    if wert is None:
        return ""
    if isinstance(wert, dict):
        wert = " · ".join("%s: %s" % (k, v) for k, v in wert.items())
    elif isinstance(wert, (list, tuple)):
        wert = " · ".join(str(x) for x in wert)
    return str(wert)[:laenge]


def bezahlte_aus_linkliste():
    """Die verkauften Angebote aus context/link-uebersicht.md.

    Sie stehen nicht in active-funnels.json, weil dort nur die Funnels selbst
    gefuehrt werden — die Kurse dahinter tauchen dort nur als Anschluss auf.

    Die Spalten werden ueber die Kopfzeile gefunden, nicht ueber ihre
    Position. Am 16.09.2026 kam die Tabelle von vier auf sieben Spalten
    (Name | Preis | Landingpage | ThriveCart | Auslieferung | Telegram |
    Status) — der ThriveCart-Link rutschte damit von Spalte 3 auf Spalte 4,
    und alle sieben bezahlten Angebote fielen still aus dem Cockpit.
    """
    p = ROOT / "context" / "link-uebersicht.md"
    if not p.exists():
        return []

    def zellen(zeile):
        z = zeile.strip()
        if not z.startswith("|"):
            return None
        return [t.strip() for t in z.strip("|").split("|")]

    raus = []
    spalten = None   # {name, preis, kasse} — Indizes der aktuellen Tabelle
    for zeile in p.read_text(encoding="utf-8").splitlines():
        teile = zellen(zeile)
        if teile is None:
            spalten = None          # Tabelle zu Ende
            continue
        if all(re.fullmatch(r":?-{2,}:?", t) for t in teile if t):
            continue                # Trennzeile
        klein = [t.lower() for t in teile]
        if any("thrivecart" in t for t in klein) and not any(
                "https://" in t for t in klein):
            # Kopfzeile: hier steht "ThriveCart" als Wort, nicht als Link.
            spalten = {
                "name": 0,
                "preis": next((i for i, t in enumerate(klein)
                               if "preis" in t), None),
                "kasse": next(i for i, t in enumerate(klein)
                              if "thrivecart" in t),
            }
            continue
        if not spalten or spalten["preis"] is None:
            continue                # Tabelle ohne Preisspalte = keine Angebote
        if max(spalten.values()) >= len(teile):
            continue
        link = teile[spalten["kasse"]]
        if "thrivecart" not in link:
            continue                # "—" heisst: kein eigener Checkout
        link = re.search(r"https://[^\s|]+", link)
        if not link:
            continue
        link = link.group(0)

        name = teile[spalten["name"]].replace("**", "").strip()
        # Ein Zusatz in Klammern beschreibt den Bump, nicht das Produkt.
        zusatz = re.search(r"\(([^)]*)\)\s*$", name)
        bump = zusatz.group(1).strip() if zusatz else ""
        if zusatz:
            name = name[:zusatz.start()].strip()

        preis = teile[spalten["preis"]]
        zahl = re.search(r"\d{2,4}", preis)
        raus.append({
            "id": "a-" + re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")[:28],
            "name": name,
            "stufe": stufe_von({"preis_chf": zahl.group(0) if zahl else None}),
            "preis": ("CHF " + zahl.group(0)) if zahl else preis,
            "keyword": "",
            "link": link,
            "bumphinweis": bump,
            "status": "Live",
        })
    return raus


def naechste_stufe(f):
    """Was nach dem Freebie kommt. Das Feld ist mal Text, mal Liste."""
    wert = f.get("produkttreppe_anschluss") or f.get("produkttreppe") or ""
    if isinstance(wert, list):
        wert = wert[0] if wert else ""
    return str(wert).split(" →")[0].strip()


def automation_id_von(ac_feld):
    """Die Automations-Nummer eines Funnels — das Feld heisst je nach Alter
    des Eintrags anders."""
    for schluessel in ("automation_id", "auslieferung_automation_id",
                       "nurture_automation_id"):
        wert = ac_feld.get(schluessel)
        if wert:
            return str(wert)
    return ""


def keywords_bauen(funnels, ac=None):
    """Keyword-Tabelle: was loest was aus, und haengt eine Automation dran."""
    aus_datei = {}
    p = ROOT / "context" / "manychat-keywords.md"
    if p.exists():
        for zeile in p.read_text(encoding="utf-8").splitlines():
            m = re.match(r"\|\s*`([A-ZÄÖÜ0-9]+)`\s*\|\s*([^|]+)\|\s*([^|]*)\|", zeile)
            if m:
                aus_datei[m.group(1)] = (m.group(2).strip(), m.group(3).strip())

    # Nummern in Namen uebersetzen, damit in der Tabelle „Liste 24" nicht als
    # Zahl steht, sondern als „Quiz-Kontakte".
    listen_namen, auto_namen = {}, {}
    for l in (ac or {}).get("listen", []):
        listen_namen[str(l["nummer"])] = l["name"]
    for a in (ac or {}).get("automationen", []):
        auto_namen[str(a["nummer"])] = a["name"]

    raus, gesehen = [], set()
    for f in funnels:
        kw = ((f.get("traffic_quellen") or {}).get("manychat_keyword") or "").split(" (")[0]
        if not kw or kw in gesehen:
            continue
        gesehen.add(kw)
        acf = f.get("ac_integration") or {}
        liste = str(acf.get("liste_id") or "")
        auto = automation_id_von(acf)
        teile = []
        if liste:
            teile.append("Liste " + listen_namen.get(liste, liste))
        if auto:
            teile.append(auto_namen.get(auto, "Automation " + auto))
        raus.append({
            "id": "f-" + f["id"],
            "keyword": kw,
            "freebie": f.get("name", ""),
            "angebot": naechste_stufe(f),
            "automation": " · ".join(teile) or "noch keine",
            "sequenz": kurztext(f.get("mail_sequenz")),
        })
    # Keywords, die in der Liste stehen, aber zu keinem Funnel gehoeren
    for kw, (wohin, notiz) in aus_datei.items():
        if kw in gesehen:
            continue
        raus.append({"id": "f-kw-" + kw.lower(), "keyword": kw, "freebie": wohin,
                     "angebot": "", "automation": notiz[:90], "sequenz": ""})
    return raus


def ac_zugang():
    """API-Adresse und Schluessel aus der .env des AC-MCP-Servers lesen.

    Die Datei ist gitignored und liegt nur auf Patricias Rechner. Fehlt sie,
    laeuft der Abgleich ohne ActiveCampaign weiter statt abzubrechen.
    """
    p = ROOT / "04-projects" / "activecampaign-mcp" / ".env"
    if not p.exists():
        return None, None
    werte = {}
    for zeile in p.read_text(encoding="utf-8").splitlines():
        if "=" in zeile and not zeile.lstrip().startswith("#"):
            k, v = zeile.split("=", 1)
            werte[k.strip()] = v.strip().strip('"').strip("'")
    return werte.get("AC_API_URL"), werte.get("AC_API_KEY")


def ac_holen():
    """Listen und Automationen direkt bei ActiveCampaign abfragen."""
    url, key = ac_zugang()
    if not url or not key:
        return None

    def api(pfad):
        anfrage = Request(url.rstrip("/") + "/api/3/" + pfad,
                          headers={"Api-Token": key, "Accept": "application/json"})
        with urlopen(anfrage, timeout=30) as antwort:
            return json.loads(antwort.read().decode("utf-8"))

    try:
        listen = api("lists?limit=100").get("lists", [])
        autos = api("automations?limit=100").get("automations", [])
    except (URLError, HTTPError, TimeoutError, OSError, ValueError) as fehler:
        print("  ActiveCampaign nicht erreichbar: %s" % fehler)
        return None
    return {"listen": listen, "automationen": autos}


def kontaktzahlen(ids):
    """Wie viele Kontakte auf jeder Liste sind.

    Die Listen-Antwort selbst enthaelt keine Zahl, deshalb pro Liste eine
    Abfrage mit `limit=1` — gezaehlt wird nur die Gesamtzahl im Kopf.
    """
    url, key = ac_zugang()
    if not url or not key:
        return {}
    raus = {}
    for lid in ids:
        try:
            anfrage = Request(
                "%s/api/3/contacts?listid=%s&limit=1&status=1" % (url.rstrip("/"), lid),
                headers={"Api-Token": key, "Accept": "application/json"})
            with urlopen(anfrage, timeout=30) as antwort:
                d = json.loads(antwort.read().decode("utf-8"))
            raus[str(lid)] = int((d.get("meta") or {}).get("total") or 0)
        except (URLError, HTTPError, TimeoutError, OSError, ValueError):
            continue
    return raus


def mailtexte_holen():
    """Alle Mails, die an einer Automation haengen — mit Betreff und Text.

    In ActiveCampaign ist auch eine Automations-Mail eine „Kampagne"; das Feld
    `automation` sagt, zu welcher sie gehoert. Der geschriebene Text steckt
    nochmal eine Ebene tiefer unter `messages`. Gespeichert wird die
    Text-Fassung, nicht das HTML — Patricia will die Mail lesen, nicht das
    Layout ansehen.
    """
    url, key = ac_zugang()
    if not url or not key:
        return {}

    def api(pfad):
        anfrage = Request(url.rstrip("/") + "/api/3/" + pfad,
                          headers={"Api-Token": key, "Accept": "application/json"})
        with urlopen(anfrage, timeout=60) as antwort:
            return json.loads(antwort.read().decode("utf-8"))

    try:
        # Achtung: `campaignMessages` an der Kampagne sind NICHT die Nummern
        # der Nachrichten, sondern die der Verbindungsstuecke. Welche Nachricht
        # dahintersteckt, steht nur im mitgelieferten Block gleichen Namens.
        kampagnen, bruecke, weiter = [], {}, 0
        while True:
            d = api("campaigns?limit=100&offset=%d&include=campaignMessages" % weiter)
            kampagnen += d.get("campaigns", [])
            for cm in d.get("campaignMessages", []):
                bruecke[str(cm["id"])] = str(cm.get("messageid") or "")
            if len(d.get("campaigns", [])) < 100:
                break
            weiter += 100

        # Alle Mailtexte auf einen Schlag, statt einzeln pro Kampagne.
        texte, weiter = {}, 0
        while True:
            d = api("messages?limit=100&offset=%d" % weiter)
            for m in d.get("messages", []):
                texte[str(m["id"])] = m
            if len(d.get("messages", [])) < 100:
                break
            weiter += 100
    except (URLError, HTTPError, TimeoutError, OSError, ValueError) as fehler:
        print("  Mailtexte nicht abrufbar: %s" % fehler)
        return {}

    raus = {}
    for c in kampagnen:
        auto = str(c.get("automation") or "")
        if not auto:
            continue
        for cmid in (c.get("campaignMessages") or []):
            mid = bruecke.get(str(cmid))
            m = texte.get(str(mid)) if mid else None
            if not m:
                continue
            raus.setdefault(auto, []).append({
                "id": str(mid),
                "name": c.get("name", ""),
                "betreff": m.get("subject", ""),
                "text": mailtext_von(m),
                "gebaut": (c.get("cdate") or "")[:10],
            })
    for auto in raus:
        raus[auto].sort(key=lambda x: x["gebaut"])
    return raus


def mailtext_von(m):
    """Den lesbaren Text einer Mail — notfalls aus dem HTML gewonnen.

    Manche Mails haben keine Textfassung; dort steht nur ein Platzhalter wie
    „fetch:". Dann wird das HTML entkleidet, sonst stuende im Cockpit Kauderwelsch.
    """
    text = (m.get("text") or "").strip()
    if text and not text.lower().startswith("fetch:"):
        return saubere_zeilen(text)

    html = m.get("html") or ""
    if not html:
        return ""
    html = re.sub(r"(?is)<(script|style|head)[^>]*>.*?</\1>", " ", html)
    html = re.sub(r"(?i)<br\s*/?>|</p>|</div>|</tr>|</h[1-6]>", "\n", html)
    html = re.sub(r"(?s)<[^>]+>", " ", html)
    for zeichen, ersatz in (("&nbsp;", " "), ("&amp;", "&"), ("&lt;", "<"),
                            ("&gt;", ">"), ("&quot;", '"'), ("&#39;", "'")):
        html = html.replace(zeichen, ersatz)
    return saubere_zeilen(re.sub(r"[^\S\n]{2,}", " ", html))


def saubere_zeilen(text, grenze=6000):
    """Leerzeilen-Wueste aus dem Editor zusammenschieben, damit die Mail im
    Cockpit lesbar ist."""
    # Mail-Programme fuellen den Vorschautext mit unsichtbaren Zeichen auf.
    # Im Cockpit sind das nur Luecken ohne Sinn.
    text = re.sub(r"[​‌‍ ﻿]+", " ", text)
    text = re.sub(r"[^\S\n]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text[:grenze]


def ac_bauen(pfad):
    """Listen und Automationen aufbereiten — erst live, sonst aus der Datei."""
    d = ac_holen()
    if d is None:
        if not pfad or not Path(pfad).exists():
            return None
        d = json.loads(Path(pfad).read_text(encoding="utf-8"))
    # Das Anlegedatum heisst in der API `cdate`; die MCP-Ausgabe nennt es
    # `created`. Beides zulassen, damit auch eine alte Datei noch passt.
    def seit(x):
        return (x.get("cdate") or x.get("created") or "")[:10]

    zahlen = kontaktzahlen([l["id"] for l in d.get("listen", [])])
    listen = [{"id": "l-" + str(l["id"]), "nummer": l["id"], "name": l["name"],
               "kontakte": zahlen.get(str(l["id"]), ""), "seit": seit(l)}
              for l in d.get("listen", [])]
    mails = mailtexte_holen()
    autos = [{"id": "au-" + str(a["id"]), "nummer": a["id"], "name": a["name"],
              "status": "aktiv" if str(a.get("status")) == "1" else "gestoppt",
              "mails": len(mails.get(str(a["id"]), [])), "seit": seit(a)}
             for a in d.get("automationen", [])]
    ac_bauen.mailtexte = mails
    return {"listen": listen, "automationen": autos,
            "stand": date.today().isoformat()}


def alle_produkte(funnels):
    """Funnels und verkaufte Kurse zusammen, ohne Doppelte."""
    def schluessel(name):
        """Name auf das Wesentliche eindampfen, damit Dubletten auffallen.

        „MBA (Bundle)" und „Mum Business Academy (MBA)" sind dasselbe Produkt.
        """
        k = re.sub(r"[^a-zäöü ]+", " ", name.lower())
        k = re.sub(r"(bundle|der|die|das|fuer|für|als|network|mama|mamas)", " ", k)
        k = re.sub(r"\s+", " ", k).strip()
        if "mba" in k or "mum business academy" in k:
            return "mba"
        return k[:18]

    raus = produkte_bauen(funnels)
    bekannt = [schluessel(p["name"]) for p in raus]
    for p in bezahlte_aus_linkliste():
        k = schluessel(p["name"])
        # Praefix zaehlt als gleich: "ceo" und "ceo moeglichkeit schaffen"
        # sind derselbe Kurs, nur einmal ausfuehrlicher benannt.
        if any(k.startswith(b) or b.startswith(k) for b in bekannt if b):
            continue
        bekannt.append(k)
        raus.append(p)
    reihe = {"Freebie": 0, "Mini-Kurs": 1, "Kurs": 2, "Signature-Kurs": 3,
             "Programm": 4, "Angebot": 5}
    raus.sort(key=lambda x: (reihe.get(x["stufe"], 9), x["name"]))
    return raus


def thrivecart_anhaengen(produkte, ziel):
    """Was am Checkout haengt, an die Angebote heften.

    Kommt aus `thrivecart-holen.py`. Diese Felder gehoeren dem Abgleich —
    Patricias eigene Notizen liegen getrennt in `daten/produkt-details` und
    werden nicht angefasst.
    """
    quelle = Path(ziel) / "thrivecart.json"
    if not quelle.exists():
        return 0

    d = json.loads(quelle.read_text(encoding="utf-8"))

    def kennung(url):
        """Der Teil der Checkout-Adresse, der das Produkt benennt."""
        teile = [t for t in str(url or "").split("/") if t]
        return teile[-1].lower() if teile and "thrivecart" in str(url) else ""

    nach_slug = {}
    for tp in d.get("products", []):
        k = tp.get("slug") or kennung(tp.get("url"))
        if k:
            nach_slug[k.lower()] = tp

    getroffen = 0
    for a in produkte:
        tp = nach_slug.get(kennung(a.get("link")))
        if not tp:
            continue
        getroffen += 1
        a["tc_bumps"] = tp.get("bumps") or []
        a["tc_upsells"] = tp.get("upsells") or []
        a["tc_downsells"] = tp.get("downsells") or []
        a["tc_status"] = tp.get("status", "")
    return getroffen


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    ziel = Path(args[0]) if args else ROOT / "outputs" / "cockpit" / "abgleich"
    ac_pfad = None
    if "--ac" in sys.argv:
        ac_pfad = sys.argv[sys.argv.index("--ac") + 1]
    ziel.mkdir(parents=True, exist_ok=True)

    funnels = lade_funnels()
    if not funnels:
        sys.exit("context/active-funnels.json fehlt oder ist leer.")

    heute = date.today().isoformat() + "T00:00:00.000Z"
    angebote = alle_produkte(funnels)
    getroffen = thrivecart_anhaengen(angebote, ziel)
    if getroffen:
        print("  %d Angebote mit ThriveCart verbunden" % getroffen)
    ac = ac_bauen(ac_pfad)
    dateien = {
        "produkte.json": {"items": angebote, "updatedAt": heute},
        "funnel.json": {"items": keywords_bauen(funnels, ac), "updatedAt": heute},
    }
    if ac:
        dateien["mailings.json"] = dict(ac, updatedAt=heute)
        # Ein Dokument je Automation, damit einzelne Mails nachladbar bleiben
        # und kein Riesen-Dokument entsteht.
        for nummer, mails in (getattr(ac_bauen, "mailtexte", {}) or {}).items():
            dateien["mails-%s.json" % nummer] = {"automation": nummer,
                                                 "items": mails, "updatedAt": heute}

    mailzahl = 0
    for name, inhalt in sorted(dateien.items()):
        (ziel / name).write_text(json.dumps(inhalt, ensure_ascii=False, indent=2),
                                 encoding="utf-8")
        anzahl = len(inhalt.get("items") or inhalt.get("automationen") or [])
        if name.startswith("mails-"):
            mailzahl += anzahl
            continue
        print("  %-16s %3d Eintraege" % (name, anzahl))
    if mailzahl:
        print("  %-16s %3d Mails in %d Automationen"
              % ("mails-*.json", mailzahl,
                 len([n for n in dateien if n.startswith("mails-")])))
    if not ac:
        print("\n  (ohne ActiveCampaign — mit --ac ac-daten.json dazunehmen)")
    print("\nAbgelegt in: %s" % ziel.resolve())


if __name__ == "__main__":
    main()
