"""Öl-Abend: Rückmelde- und Bestellblatt (A4) mit QR-Code aufs Handy-Formular.

Liest die Formular-Adresse aus outputs/doterra-strategie/oelabend/formular.json
(erzeugt von formular-anlegen.py) und baut HTML + PDF zum Ausdrucken.

    python scripts/oelabend/blatt-bauen.py                       # leer zum Ausfüllen
    python scripts/oelabend/blatt-bauen.py "5.11.2026, 19:30"    # mit Termin, eigene Datei
"""
import base64
import io
import json
import subprocess
import sys
from pathlib import Path

import qrcode

WURZEL = Path(__file__).resolve().parents[2]
ZIEL = WURZEL / "outputs" / "doterra-strategie" / "oelabend"
# Die Ankreuz-Optionen kommen aus formular-anlegen.py — eine Quelle für Papier und Handy
import importlib.util
spec = importlib.util.spec_from_file_location("f", Path(__file__).with_name("formular-anlegen.py"))
_f = importlib.util.module_from_spec(spec)
spec.loader.exec_module(_f)
OPTIONEN = {f["perstag"]: f.get("optionen", []) for f in _f.FELDER}


def qr_daten(adresse):
    bild = qrcode.make(adresse, box_size=10, border=1)
    puffer = io.BytesIO()
    bild.save(puffer, format="PNG")
    return "data:image/png;base64," + base64.b64encode(puffer.getvalue()).decode()


def kaestchen(liste, preise=False):
    zeilen = []
    for o in liste:
        preis = '<span class="preis">CHF ________</span>' if preise else ""
        zeilen.append(f'<li><span class="box"></span><span>{o}</span>{preis}</li>')
    return "\n".join(zeilen)


def main():
    info = json.loads((ZIEL / "formular.json").read_text(encoding="utf-8"))
    termin = sys.argv[1] if len(sys.argv) > 1 else ""
    datum = f"<span>Öl-Abend vom <b>{termin}</b></span>" if termin else "<span>Öl-Abend vom</span><i></i>"
    name = "rueckmeldeblatt-" + "-".join(reversed(termin.split(",")[0].split("."))) if termin else "rueckmeldeblatt"
    html = f"""<!doctype html>
<html lang="de"><head><meta charset="utf-8">
<title>Öl-Abend · Rückmeldung</title>
<link href="https://fonts.googleapis.com/css2?family=Philosopher:wght@400;700&family=Source+Sans+3:wght@400;600&display=swap" rel="stylesheet">
<style>
  @page {{ size: A4; margin: 0; }}
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; font-family: "Source Sans 3", sans-serif; color: #0c1c30; font-size: 10.5pt; }}
  .seite {{ width: 210mm; height: 297mm; padding: 13mm 15mm 11mm; background: #fff; display: flex; flex-direction: column; }}
  .kopf {{ display: flex; justify-content: space-between; align-items: flex-start; gap: 8mm;
          border-bottom: 2px solid #e8833a; padding-bottom: 4mm; }}
  h1 {{ font-family: "Philosopher", serif; font-size: 23pt; margin: 0 0 1.5mm; color: #29556d; }}
  .unter {{ margin: 0; }}
  .abend {{ margin-top: 2.5mm; }}
  .qr {{ text-align: center; font-size: 8.5pt; width: 32mm; flex: none; }}
  .qr img {{ width: 28mm; height: 28mm; display: block; margin: 0 auto 1mm; }}
  h2 {{ font-family: "Philosopher", serif; font-size: 12.5pt; color: #29556d; margin: 4.5mm 0 1.5mm; }}
  .linie {{ display: flex; align-items: flex-end; gap: 2mm; margin: 2.6mm 0; }}
  .linie span {{ white-space: nowrap; }}
  .linie i {{ flex: 1; border-bottom: 1px solid #9aa7ad; height: 4.5mm; }}
  .zwei {{ display: grid; grid-template-columns: 1fr 1fr; gap: 0 8mm; }}
  ul {{ list-style: none; margin: 0; padding: 0; }}
  li {{ display: flex; align-items: center; gap: 2.5mm; margin: 1.6mm 0; }}
  .box {{ width: 3.8mm; height: 3.8mm; border: 1.3px solid #29556d; border-radius: 1mm; flex: none; }}
  .preis {{ margin-left: auto; color: #29556d; }}
  .geschenk {{ background: #f1ecdd; border-radius: 3mm; padding: 3mm 4mm; margin-top: 4.5mm; }}
  .geschenk h2 {{ margin-top: 0; }}
  .geschenk li span:nth-child(2) b {{ color: #c96a24; }}
  .leer {{ border-bottom: 1px solid #9aa7ad; height: 7mm; }}
  .fuss {{ margin-top: auto; text-align: center; font-family: "Philosopher", serif; color: #29556d; font-size: 11.5pt; }}
</style></head>
<body><div class="seite">
  <div class="kopf">
    <div>
      <h1>Schön, warst du heute dabei</h1>
      <p class="unter">Erzähl mir kurz, wie es dir gefallen hat und was du gern hättest.</p>
      <div class="linie abend">{datum}<span>bei</span><i></i></div>
    </div>
    <div class="qr"><img src="{qr_daten(info['adresse'])}" alt="QR-Code">Lieber am Handy?<br>Einfach scannen.</div>
  </div>

  <div class="zwei">
    <div class="linie"><span>Vorname, Name</span><i></i></div>
    <div class="linie"><span>Wohnort</span><i></i></div>
    <div class="linie"><span>E-Mail</span><i></i></div>
    <div class="linie"><span>Handy (freiwillig)</span><i></i></div>
  </div>

  <div class="zwei">
    <div>
      <h2>Heute hat mir besonders gefallen</h2>
      <div class="leer"></div><div class="leer"></div>
    </div>
    <div>
      <h2>Mein Lieblingsduft heute</h2>
      <div class="leer"></div><div class="leer"></div>
    </div>
  </div>

  <div class="zwei">
    <div>
      <h2>Ich möchte mehr wissen über</h2>
      <ul>{kaestchen(OPTIONEN["OEL_INFOS"])}</ul>
    </div>
    <div>
      <h2>Diese Sets interessieren mich</h2>
      <ul>{kaestchen(OPTIONEN["OEL_SETS"], preise=True)}</ul>
      <div class="linie"><span>Einzelne Öle</span><i></i></div>
    </div>
  </div>

  <div class="geschenk">
    <h2>Mein nächster Schritt</h2>
    <ul>
      <li><span class="box"></span><span>Ich bestelle <b>heute</b> und bekomme das Buch <b>„Kraft der Natur“</b> geschenkt.</span></li>
      <li><span class="box"></span><span>Ich schlafe noch eine Nacht darüber.</span></li>
      <li><span class="box"></span><span>Ich möchte selbst einen <b>Öl-Abend</b> machen und mir das <b>Gastgeberinnen-Geschenk</b> sichern.</span></li>
      <li><span class="box"></span><span>Ich bin schon Kundin oder Beraterin.</span></li>
      <li><span class="box"></span><span>Die Öle sind gerade nichts für mich.</span></li>
    </ul>
  </div>

  <h2>Fragen und Rückmeldungen</h2>
  <div class="leer"></div><div class="leer"></div>

  <ul style="margin-top:3mm"><li><span class="box"></span><span>Ich möchte Patricias E-Mails mit Wissen und Angeboten rund um ätherische Öle bekommen. Abmelden geht jederzeit.</span></li></ul>

  <p class="fuss">Danke dir für deine Zeit und dein Vertrauen · Patricia</p>
</div></body></html>"""
    pfad = ZIEL / f"{name}.html"
    pfad.write_text(html, encoding="utf-8")
    subprocess.run(["node", str(Path(__file__).with_name("pdf.mjs")), str(pfad), str(ZIEL / f"{name}.pdf")],
                   check=True, cwd=WURZEL)
    print("→", ZIEL / f"{name}.pdf")


if __name__ == "__main__":
    main()
