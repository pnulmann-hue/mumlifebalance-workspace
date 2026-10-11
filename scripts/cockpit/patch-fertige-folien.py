#!/usr/bin/env python3
"""Die Freigabe uebernimmt fertige Folienbilder, statt sie neu zu zeichnen.

Bis 22.09.2026 rief der Freigabe-Knopf immer slideJpeg() und zeichnete jede Folie
aus headline/body neu. Karussells mit echten Screenshots, Bio-Karten oder
Markierungen verloren dabei genau das, was sie ausmacht.

Jetzt wird JE FOLIE entschieden: liegt unter karussells/<id>/bilder/slide-NN ein
Bild, wandert es unveraendert in die Freigabe. Fehlt es, wird wie bisher gezeichnet.
Damit funktioniert beides nebeneinander — ein Karussell, bei dem nur Folie 3 ein
echtes Bild hat, bekommt acht gezeichnete und eine uebernommene.

Wiederholbar. Prueft am Ende mit node --check.
"""
import re, subprocess, sys, tempfile, os

DATEI = "outputs/cockpit/mlb-cockpit.html"

ALT = '''      // Beim Karussell wandern die fertigen Folien mit — genau so, wie sie hier aussehen.
      if (b.art === "karussells" && b.obj.slides && b.obj.slides.length) {
        var i = 0, gesamt = b.obj.slides.length;
        freigabeKnopf.disabled = true;
        (function naechste() {
          if (i >= gesamt) { freigabeKnopf.disabled = false; steuerSchreiben(gesamt); return; }
          var nr = i++;
          freigabeKnopf.textContent = "lege Folie " + (nr + 1) + " von " + gesamt + " ab …";
          slideJpeg(b.obj, b.obj.slides[nr], nr, function (dataUrl) {
            db.doc("freigaben/" + b.id).collection("bilder")
              .doc("slide-" + String(nr + 1).padStart(2, "0"))
              .set({ dataUrl: dataUrl, nr: nr + 1 })
              .then(naechste)
              .catch(function () {
                freigabeKnopf.disabled = false;
                toast("Folie " + (nr + 1) + " liess sich nicht ablegen.");
                render();
              });
          });
        })();
        return;
      }'''

NEU = '''      // Beim Karussell wandern die fertigen Folien mit — genau so, wie sie hier aussehen.
      // Liegt am Beitrag ein fertiges Bild (Screenshot, Bio-Karte, Markierung), wird es
      // uebernommen statt neu gezeichnet. Nur wo keines liegt, zeichnet slideJpeg.
      if (b.art === "karussells" && b.obj.slides && b.obj.slides.length) {
        var gesamt = b.obj.slides.length;
        freigabeKnopf.disabled = true;
        freigabeKnopf.textContent = "schaue nach fertigen Folien …";
        fertigeFolien(b.id, function (fertig) {
          var i = 0;
          (function naechste() {
            if (i >= gesamt) { freigabeKnopf.disabled = false; steuerSchreiben(gesamt); return; }
            var nr = i++;
            var sid = "slide-" + String(nr + 1).padStart(2, "0");
            function ablegen(dataUrl) {
              db.doc("freigaben/" + b.id).collection("bilder").doc(sid)
                .set({ dataUrl: dataUrl, nr: nr + 1 })
                .then(naechste)
                .catch(function () {
                  freigabeKnopf.disabled = false;
                  toast("Folie " + (nr + 1) + " liess sich nicht ablegen.");
                  render();
                });
            }
            if (fertig[sid]) {
              freigabeKnopf.textContent = "übernehme Folie " + (nr + 1) + " von " + gesamt + " …";
              ablegen(fertig[sid]);
            } else {
              freigabeKnopf.textContent = "zeichne Folie " + (nr + 1) + " von " + gesamt + " …";
              slideJpeg(b.obj, b.obj.slides[nr], nr, ablegen);
            }
          })();
        });
        return;
      }'''

HELFER = '''
  /* Fertige Folienbilder am Beitrag holen (karussells/<id>/bilder/slide-NN).
     Ohne Datenbank oder bei einem Fehler kommt ein leeres Verzeichnis zurueck —
     dann zeichnet die Freigabe wie frueher. */
  function fertigeFolien(id, weiter) {
    var leer = {};
    if (!db) { weiter(leer); return; }
    db.doc("karussells/" + id).collection("bilder").limit(30).get()
      .then(function (snap) {
        var gefunden = {};
        snap.forEach(function (d) {
          var w = d.data && d.data();
          if (/^slide-[0-9]{2}$/.test(d.id) && w && w.dataUrl) gefunden[d.id] = w.dataUrl;
        });
        weiter(gefunden);
      })
      .catch(function () { weiter(leer); });
  }
'''

def main():
    s = open(DATEI, encoding="utf-8").read()

    if "function fertigeFolien(" in s:
        print("Der Patch liegt schon drin — nichts zu tun.")
        return 0

    if ALT not in s:
        print("FEHLER: Die erwartete Freigabe-Stelle steht nicht so in der Datei.")
        print("Nichts geaendert. Erst nachsehen, was sich geaendert hat.")
        return 1

    s = s.replace(ALT, NEU, 1)

    # Helfer neben renderStrip einhaengen
    anker = "  function renderStrip(strip, car) {"
    if anker not in s:
        print("FEHLER: Anker fuer den Helfer nicht gefunden."); return 1
    s = s.replace(anker, HELFER + "\n" + anker, 1)

    # Gegenprobe: das alte Verhalten darf nicht mehr als einziger Weg dastehen
    if s.count("fertigeFolien(") != 2:
        print("FEHLER: fertigeFolien kommt nicht genau zweimal vor (Definition + Aufruf).")
        return 1

    # JS aus der Seite ziehen und pruefen lassen
    m = re.search(r"<script>(.*?)</script>", s, re.S)
    if m:
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
            f.write(m.group(1)); tmp = f.name
        r = subprocess.run(["node", "--check", tmp], capture_output=True, text=True)
        os.unlink(tmp)
        if r.returncode != 0:
            print("FEHLER: node --check meldet einen Syntaxfehler. Nichts geschrieben.")
            print(r.stderr[:800]); return 1
        print("node --check: in Ordnung")
    else:
        print("WARNUNG: kein <script>-Block gefunden, Syntax nicht geprueft.")

    open(DATEI, "w", encoding="utf-8").write(s)
    print("Patch gesetzt. Danach publizieren:")
    print("  Artifact publish  file_path outputs/cockpit/mlb-cockpit.html")
    print("  url https://claude.ai/code/artifact/eeee48d5-3e50-4cff-8047-1ec5eccbb074")
    return 0

if __name__ == "__main__":
    sys.exit(main())
