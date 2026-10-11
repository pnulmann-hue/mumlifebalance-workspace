"""Je Keyword die ganze Kette: Stichwort → Freebie → Tag mit Zahl → Angebot → die Posts.

Patricia am 25.09.2026: *„vor allem die verknüpften posts müssten dran. ich will
eine klare übersicht mit allen keywords rsp. die zu einem 0€ produkt führen mit
dem verlinkten produkt, wieviele da in der liste sind in active campaign rsp.
wieviele den TAG haben und dem „Manychat" keyword das eine automatische antwort
generiert auf instagram."* Und nachgeschoben: *„weil dann hat man im cockpit
auch mal eine übersicht, welcher TAG denn eigentlich wie oft erwähnt wurde."*

**Alle Angaben aus der Quelle, nichts geraten:**

| | woher |
|---|---|
| **Stichwort** | `traffic_quellen.manychat_keyword` je Funnel |
| **Freebie** + Seite | `name` und `traffic_quellen.wordpress_landing` |
| **Tags** mit Kontaktzahl | die **IDs** aus `ac_integration.tags`, live bei AC geholt |
| **Liste** mit Kontaktzahl | `ac_integration.liste_id` gegen `mailings.json` |
| **Automationen** | `auslieferung_automation_id` / `nurture_automation_id` |
| **Angebote danach** | `produkttreppe_anschluss` — **alle** Stufen, mit Preis und Checkout |
| **Posts, die es spielen** | die eigenen Beiträge, geplant **und** gepostet, mit Reichweite |

🚨 **Über IDs, nicht über Namen.** Der erste Anlauf hat Tags und Listen über
Namensähnlichkeit gesucht — und damit beim Bio-Check den Tag „0€ Bio-Check"
(8 Kontakte) als *den* Tag angezeigt. Der Funnel erklärt aber Tag **59**
(„Bio-Check Lead") als seinen Eintrags-Tag, und der steht auf **0**. Beides ist
wahr und es sind zwei verschiedene Dinge: was der Funnel benutzen soll, und was
tatsächlich gefüllt ist. Deshalb trägt jeder Tag `deklariert: true/false`, und
wo alle deklarierten leer sind, während ein gefundener nicht leer ist, steht ein
Befund dabei. Ein Name-Treffer, der als Quelle ausgegeben wird, verdeckt genau
das.

🚨 **`produkttreppe_anschluss` ist eine Liste, kein einzelnes Angebot.** Der
erste Anlauf las sie mit `ast.literal_eval` als Dict und bekam bei **allen
vierzehn** Keywords ein leeres Angebotsfeld — also genau die Angabe, um die
Patricia gebeten hat. Eine Spalte, die überall leer ist, sieht aus wie ein
Datenproblem beim Kunden und ist ein Lesefehler bei mir.

🚨 **Der MCP-Server für ActiveCampaign liefert 403.** Er liest die Zugangsdaten
nur beim Start, und der Schlüssel wurde am 13.09.2026 gewechselt. Dieses Skript
liest die `.env` selbst und kommt durch — wer sich auf die MCP-Tools verlässt,
hält den Zugang für kaputt.

🚨 **Gezählt wird gegen den Caption-Text, nicht gegen ein gepflegtes Feld.**
Ein Feld „welches Keyword" würde nie gepflegt; der Text ist da. Gesucht wird
das Stichwort in **Grossbuchstaben als ganzes Wort** — `BIO` trifft sonst
„Biografie", und `LEAD` jedes englische Wort.

🚨 **Ein Keyword ohne einen einzigen Beitrag ist der eigentliche Befund.**
Steht das Wort in keiner Caption, läuft die Automation leer, egal wie gut sie
gebaut ist. Das sieht man sonst nirgends, weil niemand rückwärts von der
Automation zum Content schaut.

    python scripts/cockpit/funnel-uebersicht-bauen.py [--zeigen]

Danach: ArtifactData set → Sammlung "daten", Dokument "funnel".
"""

import datetime
import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]
A = ROOT / "outputs" / "cockpit" / "abgleich"
ROH = ROOT / "outputs" / "cockpit" / "inhalte-roh"

_cache = {}


def ac(pfad):
    """🚨 .env direkt lesen — der MCP-Server hat den alten Schlüssel."""
    if pfad in _cache:
        return _cache[pfad]
    env = ROOT / "04-projects" / "activecampaign-mcp" / ".env"
    cfg = dict(l.strip().split("=", 1)
               for l in env.read_text(encoding="utf-8").splitlines()
               if "=" in l and not l.startswith("#"))
    r = urllib.request.Request(cfg["AC_API_URL"].rstrip("/") + "/api/3/" + pfad,
                               headers={"Api-Token": cfg["AC_API_KEY"]})
    # AC hat am 29.09.2026 mitten im Lauf mit 503 geantwortet und den ganzen
    # Abgleich gekippt. Drei Anlaeufe mit wachsender Pause - ein Schluckauf
    # beim Anbieter darf keine leere Auswertung erzeugen.
    letzter = None
    for versuch in range(3):
        try:
            _cache[pfad] = json.load(urllib.request.urlopen(r, timeout=45))
            return _cache[pfad]
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as e:
            letzter = e
            if isinstance(e, urllib.error.HTTPError) and e.code not in (429, 500, 502, 503, 504):
                raise
            if versuch < 2:
                print("   ActiveCampaign antwortet nicht (%s) - neuer Versuch in %d s"
                      % (getattr(e, "code", type(e).__name__), 5 * (versuch + 1)))
                time.sleep(5 * (versuch + 1))
    raise letzter


# 🚨 Welche Rolle ein Tag hat, entscheidet, ob er als Eintragung zaehlt.
# Belegt aus `ac_integration.tags` in active-funnels.json — nicht geraten.
# Siehe Kopf von scratchpad/eintragstag.py bzw. CLAUDE.md.
ROLLE_EINTRAG = {"lead", "eintrag", "optin", "anmeldung", "anmeldung_tag_id",
                 "energie_kickstart", "warteliste", "start"}
ROLLE_KUNDE = {"kunde", "vorteilskunde", "wellness_advocate", "kaeufer",
               "kaufer", "customer"}


def rollenart(rolle):
    r = (rolle or "").lower()
    if r in ROLLE_EINTRAG:
        return "eintrag"
    if r in ROLLE_KUNDE:
        return "kunde"
    return "danach"


def personen_im_tag(tid):
    """Die Kontakt-IDs eines Tags — nur IDs, keine Namen und keine Adressen.

    🚨 `tagid` ist der Filter, der wirkt. `filters[tag]` wird stumm ignoriert
    und gibt die ersten 100 von allen Zuordnungen zurück.
    """
    try:
        d = ac("contacts?tagid=%s&limit=100" % tid)
    except urllib.error.HTTPError:
        return None
    return {c["id"] for c in d.get("contacts", [])}


def zahl(x):
    """🚨 AC gibt subscriber_count als ZEICHENKETTE zurück. Ohne int() wäre
    ein Vergleich „8 > 11" stillschweigend falsch."""
    try:
        return int(x)
    except (TypeError, ValueError):
        return 0


def worte(t):
    r"""🚨 `split()` allein findet „bio" nicht in „0€ Bio-Check" — der
    Bindestrich trennt nicht. Deshalb über \W zerlegen."""
    return {w for w in re.split(r"\W+", t.lower()) if len(w) > 2}


def spielt(text, kw):
    """🚨 Ganzes Wort in Grossbuchstaben — sonst trifft BIO „Biografie"."""
    if not text or not kw:
        return False
    return re.search(r"(?<![A-ZÄÖÜ0-9])" + re.escape(kw.upper())
                     + r"(?![A-ZÄÖÜ0-9])", text) is not None


def saeubern(rohkeyword):
    """Nur das Stichwort, ohne Beiwerk.

    🚨 In `active-funnels.json` steht bei einem Funnel
    `"manychat_keyword": "STANDBEIN (Flow live seit 2026-09-11)"`. Ungefiltert
    sucht die Wortsuche dann nach dem ganzen Satz und findet **nichts** — aus
    26 geplanten Beiträgen wurden 0, und die Zeile sah aus wie ein toter
    Funnel. Ein Klammerzusatz in einem Datenfeld ist normal; ihn ungeprüft als
    Suchwort zu nehmen, ist der Fehler.
    """
    m = re.match(r"\s*([A-ZÄÖÜ][A-ZÄÖÜ0-9]{2,})", rohkeyword or "")
    return m.group(1) if m else ""


# Stichwoerter, die an keinem Funnel in active-funnels.json haengen, aber einen
# echten Eintrags-Tag haben. Patricia am 29.09.2026. FAHRPLAN und SYSTEM zeigen
# beide auf den Business-Fahrplan, ANLEITUNG auf denselben Starterguide wie
# SICHTBAR.
# 🚨 Zwei Stichwoerter koennen sich einen Tag teilen. Die Zahl gehoert dann dem
# FREEBIE, nicht dem Stichwort — wer die Spalte aufsummiert, zaehlt doppelt.
DOKU_EINTRAGSTAG = {
    "FAHRPLAN": 67,      # 0€ Businessfahrplan
    "SYSTEM": 67,        # derselbe
    "ANLEITUNG": 68,     # 0€ Starterguide — wie SICHTBAR
}


def keywords_aus_doku():
    """Die Stichwort-Tabellen aus `context/manychat-keywords.md`.

    🚨 Nicht jedes Keyword hängt an einem Funnel in `active-funnels.json`.
    SYSTEM, FAHRPLAN, THEMA, PRODUKT und ANLEITUNG stehen nur in der Doku —
    wer allein die Funnels liest, verliert fünf von vierzehn Stichwörtern,
    und dass sie fehlen, sieht man an der Übersicht nicht.
    """
    raus = {}
    p = ROOT / "context" / "manychat-keywords.md"
    if not p.exists():
        return raus
    for zeile in p.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\|\s*`([A-ZÄÖÜ][A-ZÄÖÜ0-9]{2,})`\s*\|([^|]*)\|([^|]*)\|", zeile)
        if m:
            raus.setdefault(m.group(1), {"loest_aus": m.group(2).strip(),
                                         "ziel": m.group(3).strip()})
    return raus


def eigene_beitraege():
    """Geplante Beiträge aus dem Rohabzug, gepostete mit Reichweite."""
    geplant = []
    for ordner in ("reels", "karussells", "storys"):
        p = ROH / ordner
        if not p.is_dir():
            continue
        for f in sorted(p.glob("*.json")):
            d = json.load(open(f, encoding="utf-8"))
            txt = d.get("caption") or ""
            # 🚨 Eine Story hat keine Caption, sondern `frames`; ein Karussell
            # trägt den Hook in Folie 1. Ohne das findet der Abgleich in einer
            # ganzen Formatgruppe nichts und das Keyword sieht ungespielt aus.
            for fr in (d.get("frames") or []):
                txt += " " + (fr.get("text") or "") + " " + (fr.get("cta") or "")
            for sl in (d.get("slides") or []):
                txt += " " + (sl.get("headline") or "") + " " + (sl.get("body") or "")
            geplant.append({"id": f.stem, "name": d.get("name", f.stem),
                            "datum": d.get("datum", ""), "text": txt,
                            "art": ordner})
    # 🚨 Die VOLLE Caption aus den Rohabzuegen. `gepostet.json` traegt nur
    # `anfang` — die ersten 90 Zeichen —, und der Keyword-Aufruf steht IMMER am
    # Ende („Kommentier STORY"). Am 25.09.2026 habe ich deshalb STORY als „laeuft
    # leer" gemeldet, obwohl elf Beitraege es spielen; FAHRPLAN vier. Patricia hat
    # es gemerkt, nicht die Pruefung.
    # Alle Abzuege lesen, der juengste gewinnt je Beitrag.
    captions = {}
    for f in sorted((ROOT / "outputs" / "instagram-insights").glob("*.json")):
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        for k in d.get("konten", []):
            for x in k.get("beitraege", []) or []:
                voll = (x.get("caption") or "").strip()
                if voll:
                    captions[x.get("id")] = voll

    gepostet = []
    gp = A / "gepostet.json"
    if gp.exists():
        for b in json.load(open(gp, encoding="utf-8")).get("beitraege", []):
            i = b.get("id")
            gepostet.append({"id": i, "datum": b.get("datum", ""),
                             # volle Caption, wo vorhanden; sonst ehrlich der Anfang
                             "text": captions.get(i) or b.get("anfang", "") or "",
                             "ganz": i in captions,
                             "anfang": b.get("anfang", "") or "",
                             "reach": b.get("reach"), "rate": b.get("rate"),
                             "link": b.get("link", "")})
    return geplant, gepostet


def main():
    funnels = json.load(open(ROOT / "context" / "active-funnels.json",
                             encoding="utf-8")).get("funnels", [])
    mail = json.load(open(A / "mailings.json", encoding="utf-8"))
    listen_nr = {str(l.get("nummer")): l for l in mail.get("listen", [])}
    autos_nr = {str(a.get("nummer")): a for a in mail.get("automationen", [])}
    alle_tags_ac = ac("tags?limit=500").get("tags", [])

    geplant, gepostet = eigene_beitraege()
    heute = datetime.date.today().isoformat()
    zeilen = []

    for f in funnels:
        tq = f.get("traffic_quellen") or {}
        kw = saeubern(tq.get("manychat_keyword"))
        if not kw:
            continue
        acx = f.get("ac_integration") or {}
        ms = f.get("mail_sequenz")
        frei = f.get("name") or ""

        # --- Tags: zuerst die DEKLARIERTEN über ihre ID, dann Namensfunde.
        tags, gesehen = [], set()

        # 🚨 Der von Patricia benannte Eintrags-Tag (29.09.2026) hat Vorrang vor
        # allem anderen. Er steht als `eintrag_tag_id` am Funnel und wird über
        # die ID geholt — ein Tag lässt sich umbenennen, die ID bleibt.
        # Mehrere Tags fuer dasselbe Freebie: die Personen vereinigen.
        eids = acx.get("eintrag_tag_ids") or []
        if len(eids) > 1:
            menge, namen, unvollstaendig = set(), [], False
            for tid in eids:
                try:
                    et = ac("tags/%s" % tid).get("tag") or {}
                except urllib.error.HTTPError:
                    continue
                if not et:
                    continue
                namen.append(et.get("tag"))
                gesehen.add(et.get("tag"))
                wer = personen_im_tag(tid)
                if wer is None:
                    unvollstaendig = True
                else:
                    menge |= wer
            if namen:
                tags.append({"tag": " + ".join(namen),
                             "kontakte": len(menge),
                             "rolle": "lead", "art": "eintrag", "deklariert": True,
                             "benannt": True, "mehrere": True,
                             "unvollstaendig": unvollstaendig})
        eid = acx.get("eintrag_tag_id")
        if eid and not any(x.get("mehrere") for x in tags):
            try:
                et = ac("tags/%s" % eid).get("tag") or {}
            except urllib.error.HTTPError:
                et = {}
            if et:
                gesehen.add(et.get("tag"))
                tags.append({"tag": et.get("tag"),
                             "kontakte": zahl(et.get("subscriber_count")),
                             "rolle": "lead", "art": "eintrag", "deklariert": True,
                             "benannt": True})
        for rolle, tid in sorted((acx.get("tags") or {}).items()):
            if not tid:
                continue
            try:
                t = ac("tags/%s" % tid).get("tag") or {}
            except urllib.error.HTTPError:
                continue
            if not t:
                continue
            gesehen.add(t.get("tag"))
            tags.append({"tag": t.get("tag"), "kontakte": zahl(t.get("subscriber_count")),
                         "rolle": rolle, "art": rollenart(rolle), "deklariert": True})
        for t in alle_tags_ac:
            name = t.get("tag") or ""
            if name in gesehen or not frei:
                continue
            # Mindest-Deckung zwei Wörter — „Challenge" allein passt auf Lead-
            # und Story-Challenge gleichermassen.
            if len(worte(name) & worte(frei)) >= 2 or kw.lower() in worte(name):
                tags.append({"tag": name, "kontakte": zahl(t.get("subscriber_count")),
                             "rolle": "", "art": "namensfund", "deklariert": False})
        tags.sort(key=lambda t: (not t["deklariert"], -t["kontakte"]))

        dekl = [t for t in tags if t["deklariert"]]
        gefunden = [t for t in tags if not t["deklariert"]]
        # 🚨 Der Befund, den die Namenssuche verdeckt hätte: der Funnel erklärt
        # seine Tags, sie sind leer, und daneben liegt ein gefüllter mit
        # demselben Namen. Dann tagt etwas anderes als die Automation.
        befund = ""
        # 🚨 Entscheidend ist der EINTRAGS-Tag, nicht die Gesamtheit. Beim
        # Bio-Check stehen „abgeschlossen" (5) und „Thema-Interesse" (2) auf
        # Werten, der erklärte Eintrags-Tag „Bio-Check Lead" aber auf 0 —
        # während der nicht erklärte „0€ Bio-Check" 8 trägt. Wer über alle
        # deklarierten prüft, findet genau diesen Fall nie, weil irgendeiner
        # immer gefüllt ist.
        eintrag = [t for t in dekl if t["art"] == "eintrag"]
        pruef = eintrag or [t for t in dekl if t["art"] == "danach"]
        if pruef and not any(t["kontakte"] for t in pruef) \
                and any(t["kontakte"] for t in gefunden):
            voll = max(gefunden, key=lambda t: t["kontakte"])
            befund = ("Der Tag, den dieser Funnel als Eintrag erklärt (%s), steht "
                      "auf 0 — gefüllt ist „%s“ mit %d, und den nennt der Funnel "
                      "nicht. Da tagt etwas anderes als die Automation."
                      % (", ".join('„%s“' % x["tag"] for x in pruef),
                         voll["tag"], voll["kontakte"]))
        # 🚨 NUR der Eintrags-Tag. `max(tags)` nahm den groessten — bei ENERGIE
        # war das `doterra-kunde` mit 31, also Kundinnen statt Eintragungen.
        spitze = max(eintrag, key=lambda t: t["kontakte"]) if eintrag else None
        # 🚨 Wo der erklaerte Tag leer ist, aber ein namensgleicher gefuellt:
        # die Zahl zeigen, aber als Vermutung kennzeichnen. Ein Strich hiesse
        # „keine Daten" — die Daten sind da und haengen nur am falschen Namen.
        moegliche = [x for x in gefunden if x["kontakte"]]
        vermutet = max(moegliche, key=lambda x: x["kontakte"]) if moegliche else None
        benannt = any(x.get("benannt") for x in tags)
        # Ein benannter Tag ist eine Ansage, keine Vermutung — auch bei 0.
        unsicher = (not benannt) and bool(vermutet) and not (spitze and spitze["kontakte"])
        if benannt:
            spitze = [x for x in tags if x.get("benannt")][0]
        # Warum steht dort ein Strich? Das muss die Ansicht sagen koennen.
        warum_kein_tag = ""
        if not eintrag:
            warum_kein_tag = ("kein Eintrags-Tag hinterlegt" if dekl
                              else "dieser Funnel nennt gar keine Tags")

        # --- Liste und Automationen über ihre Nummer, nicht über den Namen.
        li = listen_nr.get(str(acx.get("liste_id") or ""))
        auto = []
        for feld in ("auslieferung_automation_id", "nurture_automation_id"):
            a = autos_nr.get(str(acx.get(feld) or ""))
            if a:
                auto.append({"name": a.get("name"), "status": a.get("status"),
                             "mails": a.get("mails"),
                             "rolle": "Auslieferung" if "ausliefer" in feld else "Nurture"})

        # --- Alle Anschluss-Angebote, nicht nur eines.
        angebote = [{"stufe": x.get("stufe"), "produkt": x.get("produkt"),
                     "preis": x.get("preis"), "checkout": x.get("thrivecart", "")}
                    for x in (f.get("produkttreppe_anschluss") or [])
                    if isinstance(x, dict)]

        gpl = [b for b in geplant if spielt(b["text"], kw)]
        gps = [b for b in gepostet if spielt(b["text"], kw)]
        reich = [b["reach"] for b in gps if b.get("reach")]

        # --- Auswertung: wie oft gespielt, wann zuletzt, was es gebracht hat.
        mit_datum = sorted([b for b in gps if b.get("datum")],
                           key=lambda b: b["datum"])
        zuletzt = mit_datum[-1]["datum"] if mit_datum else ""
        tage_her = None
        if zuletzt:
            try:
                tage_her = (datetime.date.today()
                            - datetime.date.fromisoformat(zuletzt)).days
            except ValueError:
                tage_her = None
        vor90 = (datetime.date.today() - datetime.timedelta(days=90)).isoformat()
        gespielt_90 = sum(1 for b in mit_datum if b["datum"] >= vor90)

        je_monat = {}
        for b in mit_datum:
            je_monat[b["datum"][:7]] = je_monat.get(b["datum"][:7], 0) + 1

        reich_sortiert = sorted(reich)
        median = (reich_sortiert[len(reich_sortiert) // 2]
                  if reich_sortiert else None)

        # 🚨 Kontakte je Beitrag ist ein ANHALTSPUNKT, keine saubere Konversion:
        # der Tag füllt sich auch über Landingpage, Story und Mail, und er ist
        # kumulativ über die ganze Zeit. Trotzdem die einzige Zahl, die sagt, ob
        # ein Stichwort überhaupt etwas einbringt.
        spitzenzahl = (spitze or {}).get("kontakte") or (vermutet or {}).get("kontakte")
        je_beitrag = (round(spitzenzahl / len(mit_datum), 1)
                      if spitzenzahl and mit_datum else None)

        zeilen.append({
            "id": f.get("id"), "keyword": kw, "freebie": frei,
            "status": f.get("status", ""), "profil": f.get("profile", ""),
            "seite": tq.get("wordpress_landing", "") or tq.get("bot_direct", ""),
            "tags": tags, "tag": (spitze or {}).get("tag", ""),
            "tag_kontakte": (spitze or {}).get("kontakte"),
            "tag_befund": befund,
            "warum_kein_tag": warum_kein_tag,
            "tag_vermutet": (vermutet or {}).get("kontakte"),
            "tag_vermutet_name": (vermutet or {}).get("tag", ""),
            "tag_unsicher": unsicher,
            "tag_benannt": benannt,
            "tag_notiz": acx.get("eintrag_tag_notiz", ""),
            # Kaufstatus getrennt — gehoert nie in die Eintrags-Spalte.
            "kunden_tags": [t for t in tags if t["art"] == "kunde"],
            "liste": (li or {}).get("name", ""), "liste_kontakte": (li or {}).get("kontakte"),
            "automationen": auto,
            # 🚨 `mail_sequenz` ist bei manchen Funnels ein Dict, bei anderen
            # eine blosse Zeichenkette. Ein `.get()` darauf bricht den ganzen
            # Lauf ab — bei einer Quelle von Hand gepflegt ist ein Feld nie
            # sicher von einem Typ.
            "mail_status": (ms.get("status") or "") if isinstance(ms, dict) else str(ms or ""),
            "angebote": angebote,
            "posts_geplant": [{"id": b["id"], "name": b["name"], "datum": b["datum"],
                               "art": b["art"]} for b in gpl],
            "posts_gepostet": [{"id": b["id"], "datum": b["datum"], "reach": b["reach"],
                                "rate": b["rate"], "link": b["link"],
                                "anfang": (b.get("anfang") or b["text"])[:70]}
                               for b in gps],
            "reichweite_summe": sum(reich) if reich else 0,
            "reichweite_median": median,
            "gespielt": len(mit_datum),
            "gespielt_90": gespielt_90,
            "zuletzt": zuletzt,
            "tage_her": tage_her,
            "je_monat": je_monat,
            "kontakte_je_beitrag": je_beitrag,
            # 🚨 Der Stand gehoert an JEDE Zeile. Das Cockpit liest vom Dokument
            # nur `items` — ein Feld daneben kommt nie an, und Zahlen ohne Datum
            # sehen immer aus wie von heute.
            "stand": heute,
        })

    # 🚨 Was nur in der Doku steht, gehoert trotzdem in die Uebersicht — sonst
    # fehlen fuenf von vierzehn Stichwoertern und niemand sieht, dass sie fehlen.
    # Sie kommen ohne AC-Zahlen, aber MIT ihren Posts: die Wortsuche braucht
    # keinen Funnel-Eintrag, und gerade hier ist „spielt es ueberhaupt jemand"
    # die interessante Frage.
    doku = keywords_aus_doku()
    schon = {z["keyword"] for z in zeilen}
    for kw, d in sorted(doku.items()):
        if kw in schon:
            continue
        gpl = [b for b in geplant if spielt(b["text"], kw)]
        gps = [b for b in gepostet if spielt(b["text"], kw)]
        reich = [b["reach"] for b in gps if b.get("reach")]
        dtag = None
        if DOKU_EINTRAGSTAG.get(kw):
            try:
                x = ac("tags/%s" % DOKU_EINTRAGSTAG[kw]).get("tag") or {}
                if x:
                    dtag = {"tag": x.get("tag"),
                            "kontakte": zahl(x.get("subscriber_count")),
                            "rolle": "lead", "art": "eintrag",
                            "deklariert": True, "benannt": True}
            except urllib.error.HTTPError:
                pass
        mit_datum = sorted([b for b in gps if b.get("datum")],
                           key=lambda b: b["datum"])
        zuletzt = mit_datum[-1]["datum"] if mit_datum else ""
        tage_her = None
        if zuletzt:
            try:
                tage_her = (datetime.date.today()
                            - datetime.date.fromisoformat(zuletzt)).days
            except ValueError:
                tage_her = None
        vor90 = (datetime.date.today() - datetime.timedelta(days=90)).isoformat()
        je_monat = {}
        for b in mit_datum:
            je_monat[b["datum"][:7]] = je_monat.get(b["datum"][:7], 0) + 1
        rs = sorted(reich)
        zeilen.append({
            "reichweite_median": rs[len(rs) // 2] if rs else None,
            "gespielt": len(mit_datum),
            "gespielt_90": sum(1 for b in mit_datum if b["datum"] >= vor90),
            "zuletzt": zuletzt, "tage_her": tage_her, "je_monat": je_monat,
            "kontakte_je_beitrag": None,
            "id": "kw-" + kw.lower(), "keyword": kw,
            "freebie": d["loest_aus"], "status": "", "profil": "",
            "seite": "", "tags": [dtag] if dtag else [],
            "tag": (dtag or {}).get("tag", ""),
            "tag_kontakte": (dtag or {}).get("kontakte"),
            "tag_benannt": bool(dtag),
            "tag_befund": "", "liste": "", "liste_kontakte": None,
            "automationen": [], "mail_status": "", "angebote": [],
            "nur_doku": True, "ziel": d["ziel"],
            "posts_geplant": [{"id": b["id"], "name": b["name"], "datum": b["datum"],
                               "art": b["art"]} for b in gpl],
            "posts_gepostet": [{"id": b["id"], "datum": b["datum"], "reach": b["reach"],
                                "rate": b["rate"], "link": b["link"],
                                "anfang": (b.get("anfang") or b["text"])[:70]}
                               for b in gps],
            "reichweite_summe": sum(reich) if reich else 0,
            "stand": heute,
        })

    # 🚨 Zwei Funnels auf demselben Stichwort — ManyChat kann je Keyword nur EINE
    # Automation auslösen, der zweite läuft ins Leere. Gefunden am 25.09.2026:
    # „STIMME" gehört dem Stimm-Check UND „Easy KI für Networkerinnen".
    zaehler = {}
    for z in zeilen:
        zaehler.setdefault(z["keyword"], []).append(z["freebie"])
    doppelt = {k: v for k, v in zaehler.items() if len(v) > 1}
    for z in zeilen:
        z["doppelt_mit"] = [f for f in doppelt.get(z["keyword"], [])
                            if f != z["freebie"]]

    # 🚨 Teilen sich zwei Stichwoerter einen Tag, gehoert die Zahl dem Freebie.
    proTag = {}
    for z in zeilen:
        if z.get("tag"):
            proTag.setdefault(z["tag"], []).append(z["keyword"])
    geteilt = {k: v for k, v in proTag.items() if len(v) > 1}
    for z in zeilen:
        z["tag_geteilt_mit"] = [k for k in geteilt.get(z.get("tag") or "", [])
                                if k != z["keyword"]]

    zeilen.sort(key=lambda z: -(z["tag_kontakte"] or 0))
    raus = {"stand": heute,
            "quelle": "context/active-funnels.json + ActiveCampaign (live, über die IDs)",
            "misst": ("Eintragungen in die Mailliste (ActiveCampaign), nicht "
                      "Reaktionen auf den Kommentar. ManyChat setzt eigene Tags mit "
                      "anderen Namen und gibt über die Schnittstelle keine Zahlen "
                      "heraus — wer im Messenger antwortet und die Mailadresse nicht "
                      "hinterlässt, fehlt hier. Die Zahl ist eine Untergrenze."),
            "hinweis": ("Tags und Listen kommen über die IDs aus active-funnels.json, "
                        "nicht über Namensähnlichkeit. `deklariert: false` heisst: "
                        "dieser Tag passt namentlich zum Freebie, der Funnel nennt ihn "
                        "aber nicht. Die Posts werden gegen den Caption-Text gezählt — "
                        "das Stichwort in GROSSBUCHSTABEN als ganzes Wort."),
            "doppelte_keywords": doppelt,
            "geteilte_tags": geteilt,
            "items": zeilen}
    (A / "funnel.json").write_text(json.dumps(raus, ensure_ascii=False, indent=1),
                                   encoding="utf-8")

    ganz = sum(1 for b in gepostet if b.get("ganz"))
    print("Keywords: %d · geplante Beiträge: %d · gepostete: %d (%d mit voller Caption)"
          % (len(zeilen), len(geplant), len(gepostet), ganz))
    if ganz < len(gepostet):
        print("   ⚠️  %d ältere Beiträge liegen nur mit den ersten 90 Zeichen vor — "
              "ein Keyword am Caption-Ende wird dort nicht gefunden.\n"
              "      Nachholen: python scripts/instagram-insights/holen.py --alle"
              % (len(gepostet) - ganz))
    print("→ %s" % (A / "funnel.json"))

    if "--zeigen" not in sys.argv:
        return

    print("\n%-11s %-29s %5s %5s  %3s/%3s  %6s  %s"
          % ("KEYWORD", "FREEBIE", "TAG", "LIST", "gpl", "gps", "REICHW", "ANGEBOT"))
    for z in zeilen:
        print("%-11s %-29s %5s %5s  %3d/%3d  %6s  %s"
              % (z["keyword"], (z["freebie"] or "—")[:29],
                 z["tag_kontakte"] if z["tag_kontakte"] is not None else "—",
                 z["liste_kontakte"] if z["liste_kontakte"] is not None else "—",
                 len(z["posts_geplant"]), len(z["posts_gepostet"]),
                 z["reichweite_summe"] or "—",
                 " · ".join("%s %s" % (a["produkt"][:22], a["preis"])
                            for a in z["angebote"][:2]) or "—"))
    print("\n%-11s %6s %6s %9s %9s %8s %9s"
          % ("KEYWORD", "gesamt", "90 Tg", "zuletzt", "Median", "im Tag", "je Beitr."))
    for z in sorted(zeilen, key=lambda x: -(x["gespielt"] or 0)):
        print("%-11s %6s %6s %9s %9s %8s %9s"
              % (z["keyword"], z["gespielt"] or "—", z["gespielt_90"] or "—",
                 ("vor %d T" % z["tage_her"]) if z["tage_her"] is not None else "nie",
                 z["reichweite_median"] or "—",
                 (("~%d" % z["tag_vermutet"]) if z.get("tag_unsicher")
                  else (z["tag_kontakte"] if z["tag_kontakte"] is not None else "—")),
                 z["kontakte_je_beitrag"] or "—"))
    unklar = [z for z in zeilen if z.get("tag_unsicher")]
    if unklar:
        print("\n🚨 Der Funnel erklärt einen Tag, gefüllt ist ein anderer — "
              "die Zahl steht mit ~ und gehört geprüft:")
        for z in unklar:
            print("   %-11s erklärt „%s“ (0)  →  gefüllt „%s“ (%d)"
                  % (z["keyword"], z["tag"] or "keiner",
                     z["tag_vermutet_name"], z["tag_vermutet"]))

    if doppelt:
        print("\n🚨 Dasselbe Stichwort für zwei Angebote — ManyChat kann nur eins "
              "ausliefern:")
        for k, v in doppelt.items():
            print("   %-11s %s" % (k, "  UND  ".join(x[:40] for x in v)))

    brach = [z for z in zeilen
             if z["gespielt"] and z["tage_her"] is not None and z["tage_her"] > 30]
    if brach:
        print("\n💤 Seit über einem Monat nicht mehr gespielt:")
        for z in sorted(brach, key=lambda x: -x["tage_her"]):
            print("   %-11s zuletzt vor %3d Tagen · %d Kontakte im Tag"
                  % (z["keyword"], z["tage_her"], z["tag_kontakte"] or 0))

    ohne = [z for z in zeilen if not z["posts_geplant"] and not z["posts_gepostet"]]
    if ohne:
        print("\n🚨 Kein einziger Beitrag spielt diese Keywords — die Automation "
              "läuft leer:")
        for z in ohne:
            print("   %-11s %s" % (z["keyword"], z["freebie"][:46]))
    for z in zeilen:
        if z["tag_befund"]:
            print("\n🚨 %s: %s" % (z["keyword"], z["tag_befund"]))


if __name__ == "__main__":
    main()
