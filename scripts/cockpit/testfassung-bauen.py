"""
Baut eine lokal lauffaehige Fassung des Cockpits fuer die Sichtpruefung.

Warum das noetig ist — zwei Gruende, die beide Zeit gekostet haben:

1) **Die Artifact-Umgebung setzt Kopf und Viewport selbst.** Die Quelldatei
   `mlb-cockpit.html` faengt direkt mit `<style>` an: kein `<!doctype>`, kein
   `<head>`, **kein `<meta name="viewport">`**. Oeffnet man sie lokal, rendert
   der Browser mit 980 px Breite — jede Handy-Pruefung an dieser Datei ist
   wertlos, egal welches Fenstermass eingestellt ist.

2) **Ein Artifact ohne Anmeldung kommt nicht an seine Datenbank.** Lokal
   liefert `claude.use("db")` nichts, und das Cockpit zeigt „Noch nichts da".
   Das Cockpit liest beim Start aber zuerst aus `localStorage` — also wird der
   echte Abgleich dort hineingelegt, und die Seite zeichnet mit echten Daten.

Das Ergebnis landet in `outputs/cockpit/abgleich/index.html` (gitignored) und
wird ueber den Server `cockpit-test` aus `.claude/launch.json` geoeffnet:

    preview_start {"name": "cockpit-test"}   ->  http://localhost:4381

🚨 Nur zum Ansehen. Was hier hineingelegt wird, ist eine Kopie — die echten
Daten liegen in der Artifact-Datenbank.

Aufruf:
  python scripts/cockpit/testfassung-bauen.py
"""
import json
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]
# Mit --neu wird die Vorschau-Fassung gebaut statt der Live-Stand. So laesst
# sich ein Umbau anschauen, ohne dass etwas veroeffentlicht wird.
SEITE = ROOT / "outputs" / "cockpit" / (
    "mlb-cockpit-neu.html" if "--neu" in sys.argv else "mlb-cockpit.html")
ABGLEICH = ROOT / "outputs" / "cockpit" / "abgleich"
ZIEL = ABGLEICH / "index.html"

# Datei im Abgleich  ->  Schluessel, unter dem das Cockpit sie erwartet.
SEEDS = {
    "links.json": "links",
    "katalog.json": "katalog",
    "kurse.json": "kurse",
    "doterra.json": "doterra",
    "umsatzplan.json": "umsatzplan",
    "verknuepfung.json": "verknuepfung",
    "clips.json": "clips",
    "instagram-zahlen.json": "ig-zahlen",
    "gepostet.json": "gepostet",
    "jahresplan.json": "jahresplan",
    "monatsbogen.json": "monatsbogen",
    "wochenbogen.json": "wochenbogen",
    "stimmen.json": "stimmen",
    "aufgaben.json": "aufgaben",
    "ziele.json": "ziele",
    "reichweite.json": "reichweite",
    "leads.json": "leads",
    "steuer.json": "steuer",
    "projekte.json": "projekte",
    "doterra-produkte.json": "doterra-produkte",
    "ideen-extern.json": "ideen-extern",
    "planung-abgleich.json": "planung-abgleich",
    # 🚨 Neue Datendatei gehoert hier nachgetragen, sonst ist der Reiter
    #    in der lokalen Pruefung leer (Lehre vom 24.09.2026).
    "launch.json": "launch",
    # 🚨 Ohne diesen Eintrag prueft die lokale Fassung den Funnel-Reiter
    # gegen einen alten Stand und zeigt andere Zahlen als das Cockpit.
    "funnel.json": "funnel",
}


# Beitraege liegen nicht als ein Dokument, sondern als Liste plus Einzelstuecke:
# "reelliste" haelt die IDs, "rl-<id>" den Beitrag. Ohne die hier ist die
# Wochen-Vorschau lokal leer und damit nicht pruefbar — genau die Ansicht, an der
# am meisten geaendert wird.
BEITRAEGE = {
    "reels":      ("reelliste",  "rl-"),
    "karussells": ("karliste",   "kar-"),
    "storys":     ("storyliste", "st-"),
}
ROH = ABGLEICH.parent / "inhalte-roh"


def beitraege_einlegen(zeilen, geladen):
    for ordner, (listenschluessel, praefix) in BEITRAEGE.items():
        p = ROH / ordner
        if not p.is_dir():
            continue
        ids = []
        for datei in sorted(p.glob("*.json")):
            roh = datei.read_text(encoding="utf-8")
            if "</script" in roh.lower():
                continue
            d = json.loads(roh)
            # Das Cockpit erwartet die eigene ID im Beitrag, nicht nur im Dateinamen.
            d.setdefault("id", datei.stem)
            ids.append(d["id"])
            zeilen.append("localStorage.setItem(%s,%s);"
                          % (json.dumps("mlb:" + praefix + d["id"]),
                             json.dumps(json.dumps(d, ensure_ascii=False))))
        if ids:
            zeilen.append("localStorage.setItem(%s,%s);"
                          % (json.dumps("mlb:" + listenschluessel),
                             json.dumps(json.dumps(ids))))
            geladen.append("%s (%d Stueck)" % (ordner, len(ids)))

    # 🚨 Die Sammlung „freigaben" ist seit 24.09.2026 die Quelle fuer den Stand
    # eines Beitrags — nicht mehr `beitrag.blotato`. Ohne sie faellt die
    # Testfassung auf das veraltete Feld zurueck und zeigt andere Zahlen als
    # das Live-Cockpit. Genau das ist beim ersten Lauf passiert: „Haengt 4"
    # statt 1, „Laeuft von selbst 6" statt 13.
    fp = ROH / "freigaben"
    if fp.is_dir():
        m = {}
        for datei in sorted(fp.glob("*.json")):
            roh = datei.read_text(encoding="utf-8")
            if "</script" in roh.lower():
                continue
            m[datei.stem] = json.loads(roh)
        if m:
            zeilen.append("localStorage.setItem(%s,%s);"
                          % (json.dumps("mlb:freigaben"),
                             json.dumps(json.dumps(m, ensure_ascii=False))))
            geladen.append("freigaben (%d Stueck)" % len(m))

    # Die Zuordnung Cockpit-Beitrag -> Instagram-Post (gepostet-zuordnen.py).
    zp = ABGLEICH / "gepostet-zuordnung.json"
    if zp.exists():
        z = json.loads(zp.read_text(encoding="utf-8"))
        zeilen.append("localStorage.setItem(%s,%s);"
                      % (json.dumps("mlb:ig-zuordnung"),
                         json.dumps(json.dumps(z, ensure_ascii=False))))
        geladen.append("ig-zuordnung (%d Treffer)" % len(z.get("zuordnung", {})))


# Die Listen-Reiter des Cockpits. Wird aus der Seite gelesen, damit die Liste
# nicht an zwei Stellen gepflegt werden muss.
def doc_keys(html: str) -> set:
    m = re.search(r"DOC_KEYS = \[(.*?)\]", html, re.S)
    return set(re.findall(r'"([^"]+)"', m.group(1))) if m else set()


def main():
    html = SEITE.read_text(encoding="utf-8")
    DOC_KEYS = doc_keys(html)

    zeilen, geladen = [], []
    for datei, schluessel in SEEDS.items():
        p = ABGLEICH / datei
        if not p.exists():
            continue
        roh = p.read_text(encoding="utf-8")
        # Ein „</script>" im Inhalt wuerde den Block vorzeitig schliessen.
        if "</script" in roh.lower():
            print("  übersprungen (enthält </script>): %s" % datei)
            continue
        # 🚨 **Die Listen-Reiter erwarten ein ARRAY, nicht das Dokument.**
        # Das Cockpit liest aus der Datenbank `snap.data().items` und legt nur
        # das Array in `state[...]`. Wer hier das ganze Dokument ablegt, setzt
        # `state.leads` auf ein Objekt — und der Reiter stirbt mit
        # „state.leads.filter is not a function". Genau das ist am 24.09.
        # passiert, und genau dafuer gibt es diese Testfassung.
        if schluessel in DOC_KEYS:
            try:
                d = json.loads(roh)
                if isinstance(d, dict) and isinstance(d.get("items"), list):
                    roh = json.dumps(d["items"], ensure_ascii=False)
            except Exception:
                pass
        zeilen.append('localStorage.setItem(%s,%s);'
                      % (json.dumps("mlb:" + schluessel), json.dumps(roh)))
        geladen.append("%s (%.0f KB)" % (schluessel, len(roh) / 1024))

    beitraege_einlegen(zeilen, geladen)

    kopf = ('<!doctype html><html lang="de"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1">'
            '<title>Cockpit — Testfassung</title>'
            '<script>try{' + "".join(zeilen) + '}catch(e){}</script>'
            '</head><body>')

    ZIEL.parent.mkdir(parents=True, exist_ok=True)
    ZIEL.write_text(kopf + html + "</body></html>", encoding="utf-8")

    print("  eingelegt: %s" % (", ".join(geladen) if geladen else "nichts"))
    print("\nGeschrieben: %s" % ZIEL)
    print("Ansehen:     preview_start {\"name\": \"cockpit-test\"} → http://localhost:4381")


if __name__ == "__main__":
    main()
