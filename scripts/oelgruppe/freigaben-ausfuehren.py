"""Führt aus, was Patricia im Cockpit unter doTERRA → Freigaben freigegeben hat.

    python scripts/oelgruppe/freigaben-ausfuehren.py --ordner <dump>          # zeigt nur, was anstünde
    python scripts/oelgruppe/freigaben-ausfuehren.py --ordner <dump> --los    # verschickt und plant ein

<dump> ist der Ablageordner von ArtifactData list (Sammlung doterra-freigaben, out_dir).
Status: entwurf -> freigegeben (ihr Klick) -> verschickt (Newsletter) / eingeplant (Saison-Beitrag).
Schreibt <dump>/rueckmeldung.json: die Felder, die danach mit ArtifactData update zurück ins Cockpit gehören.

Newsletter: Kampagne anlegen, Inhalt zurücklesen, dann erst scharf stellen.
🚨 campaign_status 1 verschickt SOFORT: AC überschreibt dabei sdate mit jetzt (gemessen 05.11.2026 an einer Testkampagne).
🚨 Bricht ab bei ✏️ im Text und wenn der Monat in stand.json schon verschickt ist: Eine Mail geht nie zweimal.
"""
import argparse
import datetime as dt
import json
import pathlib
import re
import subprocess
import sys
import urllib.parse
import urllib.request
from zoneinfo import ZoneInfo

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = pathlib.Path(__file__).resolve().parents[2]
STAND = ROOT / "outputs/newsletter/doterra-versand-stand.json"
ABSENDER = {"fromname": "Patricia Ulmann", "fromemail": "patricia@mumlifebalance.ch", "reply2": "patricia@mumlifebalance.ch"}
AC_ZONE = ZoneInfo("America/Chicago")  # Kontozeit in ActiveCampaign (-06:00 in den Kampagnen-Daten)


def zugang():
    env = {}
    for z in (ROOT / "04-projects/activecampaign-mcp/.env").read_text(encoding="utf-8").splitlines():
        if "=" in z and not z.startswith("#"):
            k, v = z.split("=", 1)
            env[k.strip()] = v.strip().strip('"')
    return env["AC_API_URL"].rstrip("/"), env["AC_API_KEY"]


def v1(aktion, werte):
    basis, schluessel = zugang()
    url = "%s/admin/api.php?api_action=%s&api_key=%s&api_output=json" % (basis, aktion, schluessel)
    a = json.load(urllib.request.urlopen(urllib.request.Request(url, data=urllib.parse.urlencode(werte).encode(), method="POST")))
    if a.get("result_code") != 1:
        raise RuntimeError("%s: %s" % (aktion, a.get("result_message")))
    return a


def v3(pfad, methode="GET", daten=None):
    basis, schluessel = zugang()
    koerper = json.dumps(daten).encode() if daten else None
    r = urllib.request.Request(basis + "/api/3" + pfad, data=koerper, method=methode,
                               headers={"Api-Token": schluessel, "Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(r))


def als_text(seite):
    t = re.sub(r"(?is)<(style|head).*?</\1>", " ", seite)
    t = re.sub(r"(?i)</(p|tr|h\d)>", "\n\n", t)
    t = re.sub(r"<[^>]+>", " ", t).replace("&nbsp;", " ")
    return re.sub(r"\n\s*\n+", "\n\n", re.sub(r"[ \t]+", " ", t)).strip()


def kampagne_anlegen(name, betreff, seite, listen, minuten=10):
    """Legt den Entwurf an und liest den Inhalt zurück. Eine leere Mail ist hier schon vorgekommen."""
    listenfelder = {"p[%d]" % l: l for l in listen}
    kopf = dict(ABSENDER, subject=betreff)
    msg = v1("message_add", dict(kopf, format="html", htmlconstructor="external", textconstructor="external",
                                 html=seite, text=als_text(seite), **listenfelder))
    sdate = (dt.datetime.now(AC_ZONE) + dt.timedelta(minutes=minuten)).strftime("%Y-%m-%d %H:%M:%S")
    kamp = v1("campaign_create", dict(kopf, type="single", name=name, sdate=sdate, status=0, public=0, tracklinks="all",
                                      **listenfelder, **{"m[%s]" % msg["id"]: 100}))
    # message_add mit „external“ lässt den Inhalt leer (Vorfall 02.11.), erst dieser Schritt schreibt ihn hinein
    v3("/messages/%s" % msg["id"], "PUT", {"message": {"html": seite, "text": als_text(seite), "subject": betreff, "htmlfetch": "now"}})
    zurueck = v3("/messages/%s" % msg["id"])["message"]
    if (zurueck.get("html") or "").strip() != seite.strip():
        raise RuntimeError("AC hat Nachricht %s anders gespeichert, nichts verschickt (Kampagne %s bleibt Entwurf)" % (msg["id"], kamp["id"]))
    return kamp["id"], msg["id"], sdate


def newsletter(doc, los):
    monat = doc["monat"]
    stand = json.loads(STAND.read_text(encoding="utf-8")) if STAND.exists() else {}
    if monat in stand:
        return {"status": "verschickt", "kampagne": stand[monat]["kampagne"], "versandAm": stand[monat]["sdate"]}
    if "✏️" in doc["html"]:
        raise RuntimeError("✏️ im Newsletter %s, nichts verschickt" % monat)
    betreff = doc["betreffe"][int(doc.get("betreffWahl") or 0)]
    print("Newsletter", monat, "·", betreff, "· Listen", doc["listen"])
    if not los:
        return None
    kid, mid, sdate = kampagne_anlegen(doc["titel"], betreff, doc["html"], doc["listen"])
    v1("campaign_status", {"id": kid, "status": 1})
    k = v3("/campaigns/%s" % kid)["campaign"]
    if str(k.get("status")) not in ("1", "2", "5"):
        raise RuntimeError("Kampagne %s steht auf Status %s statt geplant" % (kid, k.get("status")))
    stand[monat] = {"kampagne": kid, "nachricht": mid, "sdate": sdate, "betreff": betreff}
    STAND.write_text(json.dumps(stand, ensure_ascii=False, indent=1), encoding="utf-8")
    print("✓ Kampagne", kid, "geplant für", sdate, "(Kontozeit)")
    return {"status": "verschickt", "kampagne": kid, "versandAm": dt.datetime.now().isoformat(timespec="minutes"), "betreff": betreff}


def saison(paket, docs, los):
    ordner = ROOT / "outputs/telegram-posts" / paket
    nur = ",".join(str(d["nr"]) for d in docs)
    daten = ",".join("%d=%s" % (d["nr"], d["datum"]) for d in docs)
    print("Saison", paket, "· Beiträge", nur)
    if not los:
        return False
    subprocess.run("npx tsx src/saison-einplanen.ts \"%s\" --nur %s --datum %s" % (ordner, nur, daten),
                   shell=True, check=True, cwd=ROOT / "scripts/telegram-userbot")
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ordner", required=True)
    ap.add_argument("--los", action="store_true")
    a = ap.parse_args()
    dump = pathlib.Path(a.ordner)
    dateien = [f for f in dump.rglob("*.json") if f.name != "rueckmeldung.json"]
    docs = {f.stem: json.loads(f.read_text(encoding="utf-8")) for f in dateien}
    rueck, fehler = {}, []
    pakete = {}
    for did, d in docs.items():
        if d.get("status") != "freigegeben":
            continue
        if d.get("art") == "newsletter":
            try:
                r = newsletter(d, a.los)
                if r:
                    rueck[did] = r
            except Exception as e:
                fehler.append("%s: %s" % (did, e))
        elif d.get("art") == "saison":
            pakete.setdefault(d["paket"], []).append((did, d))
    for paket, liste in pakete.items():
        try:
            if saison(paket, [d for _, d in liste], a.los):
                for did, _ in liste:
                    rueck[did] = {"status": "eingeplant"}
        except Exception as e:
            fehler.append("%s: %s" % (paket, e))
    (dump / "rueckmeldung.json").write_text(json.dumps({"updates": rueck, "fehler": fehler}, ensure_ascii=False, indent=1), encoding="utf-8")
    print("Rückmeldung:", len(rueck), "Dokumente,", len(fehler), "Fehler")
    for f in fehler:
        print("🚨", f)
    if fehler:
        sys.exit(1)


if __name__ == "__main__":
    main()
