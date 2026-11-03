"""Öl-Abend: Felder, Tag und Formular in ActiveCampaign anlegen (wiederholbar).

Legt nur an, was fehlt — Felder werden über ihren perstag erkannt, der Tag über
seinen Namen, das Formular über seinen Namen. Schreibt die Formular-Nummer nach
outputs/doterra-strategie/oelabend/formular.json, damit das Papierblatt den QR-Code
auf die richtige Adresse legt.

    python scripts/oelabend/formular-anlegen.py [--trocken]
"""
import json
import os
import sys
import urllib.request
from pathlib import Path

WURZEL = Path(__file__).resolve().parents[2]
ZIEL = WURZEL / "outputs" / "doterra-strategie" / "oelabend"
TROCKEN = "--trocken" in sys.argv

LISTE = "18"            # doTERRA Interessenten
TAG = "Öl-Abend"
FORMULAR = "Öl-Abend · Rückmeldung und Bestellung"
DATENSCHUTZ_FELD = "9"  # „Datenschutz d“ — dieselbe Zustimmung wie beim Energie-Kickstart

FELDER = [
    {"perstag": "OEL_WOHNORT", "type": "text", "title": "Öl-Abend · Wohnort"},
    {"perstag": "OEL_GEFALLEN", "type": "textarea", "title": "Öl-Abend · Heute hat mir besonders gefallen"},
    {"perstag": "OEL_LIEBLINGSDUFT", "type": "text", "title": "Öl-Abend · Mein Lieblingsduft heute"},
    {"perstag": "OEL_INFOS", "type": "checkbox", "title": "Öl-Abend · Ich möchte mehr wissen über",
     "optionen": ["Öle für Kinder", "Hausapotheke und Basisöle", "Gefühle und innere Ruhe",
                  "Zeit für mich als Mama", "Ein Business mit doTERRA"]},
    {"perstag": "OEL_SETS", "type": "checkbox", "title": "Öl-Abend · Diese Sets interessieren mich",
     "optionen": ["Hausapotheke (10 Basisöle)", "Kids Collection", "Family Essentials"]},
    {"perstag": "OEL_WUNSCHOELE", "type": "text", "title": "Öl-Abend · Einzelne Öle, die ich gern hätte"},
    {"perstag": "OEL_SCHRITT", "type": "checkbox", "title": "Öl-Abend · Mein nächster Schritt",
     "optionen": ["Ich bestelle heute und bekomme das Buch „Kraft der Natur“ geschenkt",
                  "Ich schlafe noch eine Nacht darüber",
                  "Ich möchte selbst einen Öl-Abend machen und mir das Gastgeberinnen-Geschenk sichern",
                  "Ich bin schon Kundin oder Beraterin",
                  "Die Öle sind gerade nichts für mich"]},
    {"perstag": "OEL_FRAGEN", "type": "textarea", "title": "Öl-Abend · Fragen und Rückmeldungen"},
]


def env():
    for zeile in (WURZEL / "04-projects" / "activecampaign-mcp" / ".env").read_text(encoding="utf-8").splitlines():
        if "=" in zeile and not zeile.strip().startswith("#"):
            k, v = zeile.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"'))
    if not os.environ.get("AC_API_KEY"):
        sys.exit("AC_API_KEY fehlt in 04-projects/activecampaign-mcp/.env")


def ac(pfad, daten=None, methode=None):
    url = os.environ["AC_API_URL"].rstrip("/") + "/api/3/" + pfad
    body = json.dumps(daten).encode("utf-8") if daten is not None else None
    req = urllib.request.Request(url, data=body, method=methode or ("POST" if body else "GET"),
                                 headers={"Api-Token": os.environ["AC_API_KEY"], "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8") or "{}")


def feld_anlegen(f, bestehend):
    if f["perstag"] in bestehend:
        print(f"  ✓ Feld da: {f['title']} ({bestehend[f['perstag']]})")
        return bestehend[f["perstag"]]
    print(f"  + Feld neu: {f['title']}")
    if TROCKEN:
        return "?"
    neu = ac("fields", {"field": {"type": f["type"], "title": f["title"], "perstag": f["perstag"], "visible": 1}})
    fid = neu["field"]["id"]
    ac("fieldRels", {"fieldRel": {"field": fid, "relid": 0}})
    if f.get("optionen"):
        ac("fieldOption/bulk", {"fieldOptions": [{"field": fid, "label": o, "value": o, "orderid": i + 1}
                                                 for i, o in enumerate(f["optionen"])]})
    return fid


def main():
    env()
    ZIEL.mkdir(parents=True, exist_ok=True)

    alle = ac("fields?limit=100")["fields"]
    bestehend = {x["perstag"]: x["id"] for x in alle}
    ids = {f["perstag"]: feld_anlegen(f, bestehend) for f in FELDER}

    tags = ac("tags?search=" + urllib.request.quote(TAG))["tags"]
    tag = next((t for t in tags if t["tag"] == TAG), None)
    if tag:
        print(f"  ✓ Tag da: {TAG} ({tag['id']})")
    else:
        print(f"  + Tag neu: {TAG}")
        if not TROCKEN:
            tag = ac("tags", {"tag": {"tag": TAG, "tagType": "contact", "description": "Rückmeldung von einem Öl-Abend"}})["tag"]

    formulare = ac("forms?limit=100")["forms"]
    vorhanden = next((x for x in formulare if x["name"] == FORMULAR), None)
    if vorhanden:
        print(f"  ✓ Formular da: {FORMULAR} ({vorhanden['id']})")
        fid = vorhanden["id"]
    else:
        print(f"  + Formular neu: {FORMULAR}")
        if TROCKEN:
            return
        vorlage = ac("forms/64")["form"]
        datenschutz = next(c for c in vorlage["cfields"] if str(c.get("id")) == DATENSCHUTZ_FELD)
        cfields = [
            {"type": "header", "header": "Schön, warst du heute dabei", "class": "_field_header"},
            {"type": "html", "header": "undefined", "class": "_field_html",
             "html": "Erzähl mir kurz, wie es dir gefallen hat und was du gern hättest. "
                     "Wer heute bestellt, bekommt von mir das Buch „Kraft der Natur“ geschenkt."},
            {"type": "firstname", "header": "Vorname", "default_text": "", "required": True, "class": "_field_firstname"},
            {"type": "lastname", "header": "Nachname", "default_text": "", "required": False, "class": "_field_lastname"},
            {"id": "email", "type": "email", "header": "E-Mail", "default_text": "", "required": True, "class": "_field_email"},
            {"type": "phone", "header": "Handynummer (freiwillig)", "default_text": "", "required": False, "class": "_field_phone"},
        ]
        for f in FELDER:
            cfields.append({"id": str(ids[f["perstag"]]), "type": f["type"], "header": f["title"].split(" · ", 1)[1],
                            "required": False, "class": "_field_" + f["perstag"].lower()})
        cfields.append(dict(datenschutz, header="Mails von mir", title="Mails von mir"))
        neu = dict(vorlage)
        for k in ("id", "links", "cdate", "udate", "entries", "public_url", "embed_code", "address", "aid"):
            neu.pop(k, None)
        neu.update({
            "name": FORMULAR,
            "button": "Abschicken",
            "thanks": "Danke dir! Ich melde mich in den nächsten Tagen bei dir.",
            "submit": "open-url",
            "submitdata": {"url": "https://mumlifebalance.ch/oelabend-danke/"},  # WP 4478
            "cfields": cfields,
            "actiondata": {"actions": [
                {"title": "Tag hinzufügen", "type": "add-a-tag", "tag": TAG},
                {"options": {}, "dealcurrency": "chf", "type": "subscribe-to-list", "list": LISTE,
                 "listName": "doTERRA Interessenten"},
            ]},
            "options": {"blanks_overwrite": False, "confaction": "redirect", "useBgColor": True,
                        "useBgImage": False, "sendoptin": False},
        })
        fid = ac("forms", {"form": neu})["form"]["id"]
        print(f"  → Formular {fid}")

    adresse = f"https://mumlifebalance.activehosted.com/f/{fid}"
    (ZIEL / "formular.json").write_text(json.dumps({"formular": fid, "adresse": adresse, "tag": TAG,
                                                     "felder": ids}, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Adresse:", adresse)


if __name__ == "__main__":
    main()
