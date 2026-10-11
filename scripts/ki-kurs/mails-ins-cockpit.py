# -*- coding: utf-8 -*-
"""Holt die Launch-Mails aus ActiveCampaign ins Cockpit.

    python scripts/ki-kurs/mails-ins-cockpit.py
    # danach: ArtifactData batch set → Sammlung "mailentwuerfe", file_path je Datei

Anders als bei Magnet-Ich ist die Quelle hier **ActiveCampaign**, nicht eine
lokale Datei: Diese Mails sind dort schon gebaut, und was im Cockpit steht,
soll der Stand sein, der wirklich rausgeht.

Je Mail ein Dokument mit Betreff, Vorschauzeile, Versandstelle und dem ganzen
HTML zum Kopieren. Das Cockpit zeigt sie unter „Listen & Automationen" bei der
Automation, zu der sie gehören.

🚨 Die Reihenfolge kommt aus dem Ablauf der Automation, nicht aus der
   Kampagnen-Nummer. „Pitch KI Kurs" hat eine kleinere Nummer als
   „Pitch KI Kurs 2", aber dazwischen liegen zwei andere Mails.

🚨 Die Sammlung `mailentwuerfe` gehört diesem Skript und dem Magnet-Ich-Skript,
   NICHT dem täglichen Abgleich. Ein `set` von dort würde sie löschen.

🚨 Ein Artifact-Dokument darf höchstens 256 KB haben. Eine Mail liegt bei
   rund 18 KB — das Skript warnt trotzdem, falls eine aus der Reihe fällt.
"""
import json
import pathlib
import re
import sys
import urllib.error
import urllib.request

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = pathlib.Path(__file__).resolve().parents[2]
ZIEL = ROOT / "outputs" / "cockpit" / "abgleich" / "mailentwuerfe"

# Welche Automationen ins Cockpit sollen.
# Ohne Angabe: alle aktiven, die überhaupt Mails verschicken (Patricias Wunsch
# vom 08.10.2026 — „will von allen funnels die aktuelle mail in meinem cockpit").
AUTOMATIONEN = None


def alle_automationen():
    """Alle Automationen mit mindestens einer Mail, aktive zuerst."""
    d = ac("automations?limit=200").get("automations", [])
    raus = []
    for a in d:
        raus.append((int(a["id"]), a.get("name") or "ohne Namen",
                     a.get("status") == "1"))
    raus.sort(key=lambda x: (not x[2], x[1].lower()))
    return raus

GRENZE = 256 * 1024


def zugang():
    env = {}
    for z in (ROOT / "04-projects/activecampaign-mcp/.env").read_text(encoding="utf-8").splitlines():
        m = re.match(r"\s*([A-Z_]+)\s*=\s*(.+?)\s*$", z)
        if m:
            env[m.group(1)] = m.group(2).strip("\"'")
    assert env.get("AC_API_KEY"), "AC-Zugang fehlt in der .env"
    return env["AC_API_URL"].rstrip("/"), env["AC_API_KEY"]


U, K = zugang()


def ac(pfad):
    r = urllib.request.Request(U + "/api/3/" + pfad, headers={"Api-Token": K})
    for versuch in range(3):
        try:
            return json.load(urllib.request.urlopen(r))
        except urllib.error.HTTPError as e:
            if e.code < 500 or versuch == 2:
                raise
            import time
            time.sleep(1 + versuch)


def ablauf(aid):
    """Mails in der Reihenfolge, in der sie wirklich rausgehen, mit der
    Wartezeit davor."""
    bl = ac("automations/%s/blocks?limit=100" % aid).get("automationBlocks", [])
    bl.sort(key=lambda b: int(b.get("ordernum") or b.get("id") or 0))
    raus, warten = [], ""
    for b in bl:
        t, p = b.get("type"), (b.get("params") or {})
        if t == "wait":
            warten = ("%s %s später" % (p.get("waittime"), p.get("waitdurt"))
                      if p.get("waittype") == "for" else "zu festem Termin")
        elif t == "send":
            raus.append((p.get("campaignid"), warten))
            warten = ""
    return raus


def main():
    ZIEL.mkdir(parents=True, exist_ok=True)
    gesamt, gross = 0, []

    # --nur 83 84 holt gezielt einzelne Automationen nach. Ein Lauf ueber alle
    # 40 dauert Minuten; nach einer Textaenderung an EINER Mail ist das
    # Verschwendung — und je laenger er dauert, desto eher laesst man ihn weg
    # und arbeitet danach mit einem veralteten Stand weiter.
    nur = []
    if "--nur" in sys.argv:
        nur = [a for a in sys.argv[sys.argv.index("--nur") + 1:] if a.isdigit()]

    liste = AUTOMATIONEN
    if liste is None:
        liste = [(i, n) for i, n, aktiv in alle_automationen()]
        if nur:
            liste = [(i, n) for i, n in liste if str(i) in nur]
            print("Nur Automation %s\n" % ", ".join(nur))
        else:
            print("%d Automationen gefunden\n" % len(liste))

    for aid, aname in liste:
        folge = ablauf(aid)
        if not folge:
            continue                      # Automationen ohne Mail überspringen
        print("=" * 68)
        print("Automation %s  (%s) — %d Mails" % (aname, aid, len(folge)))
        for i, (cid, warten) in enumerate(folge):
            c = ac("campaigns/%s" % cid)["campaign"]
            ms = ac("campaigns/%s/campaignMessages" % cid).get("campaignMessages", [])
            if not ms:
                print("   %-30s keine Nachricht" % c.get("name")); continue
            msg = ac("messages/%s" % ms[0]["message"])["message"]
            h = msg.get("html") or ""

            kennung = "ki-launch-%s-%02d-%s" % (
                aid, i, re.sub(r"[^a-z0-9]+", "-", (c.get("name") or "").lower()).strip("-")[:34])
            doc = {
                # 🚨 sagt dem Cockpit, dass das der Live-Stand ist und nicht
                #    ein Entwurf, der noch eingebaut werden muss
                "quelle": "activecampaign",
                "automation": str(aid),
                "automationName": aname,
                "reihenfolge": i,
                "name": c.get("name"),
                "warten": warten or "sofort",
                "betreff": msg.get("subject") or "",
                "preheader": msg.get("preheader_text") or "",
                "campaignId": cid,
                "messageId": ms[0]["message"],
                "html": h,
            }
            groesse = len(json.dumps(doc, ensure_ascii=False).encode("utf-8"))
            if groesse > GRENZE:
                gross.append((kennung, groesse))
            (ZIEL / (kennung + ".json")).write_text(
                json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
            print("   %-30s %-18s %3d KB  %s" % (
                (c.get("name") or "")[:30], warten or "sofort", groesse // 1024, kennung))
            gesamt += 1

    print()
    print("%d Mails → %s" % (gesamt, ZIEL.relative_to(ROOT)))
    if gross:
        print("🚨 Über 256 KB (Artifact-Grenze): %s" % gross)
        sys.exit(1)
    print("\nDanach im Chat:")
    print("  ArtifactData batch set · Sammlung „mailentwuerfe“ · je Datei ein Dokument")


if __name__ == "__main__":
    main()
