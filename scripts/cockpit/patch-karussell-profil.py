#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Karussell-Loader: die fuenf Felder zurueckholen, die er wegwirft.

🚨 Der Befund (21.09.2026): `saveCarousel` schreibt profil, kommentar,
kommentarStand, kommentarErledigt und kommentarAntwort in die Datenbank —
der Loader baut sein `car`-Objekt aber aus einer festen Feldliste, in der
keines davon vorkommt. Folge:

  1. Nach dem Laden ist `car.profil` undefined.
  2. `kartenProfil()` faellt auf "mentoring" zurueck.
  3. Die Wochen-Vorschau schluesselt die Plaetze mit `datum + "|" + profil`.
     → JEDES Karussell landet in der Mentoring-Spalte, die doTERRA-Plaetze
       an Di und Do bleiben leer. Immer. Egal was in der Datenbank steht.
  4. Beim naechsten Speichern schreibt die Seite `profil: ""` zurueck und
     loescht damit den Wert in der Datenbank.

Dieselbe Falle wie am 18.09. bei `saveReel` (Feld `hinweis`): eine feste
Feldliste ist die Stelle, an der neue Felder still verloren gehen.

Wiederholbar: laeuft der Patch zweimal, passiert beim zweiten Mal nichts.
"""
import io, os, re, subprocess, sys, tempfile

FELDER = ["profil", "kommentar", "kommentarStand", "kommentarErledigt", "kommentarAntwort"]
ZUSATZ = ' ' + ' '.join('%s: d0.%s || "",' % (f, f) for f in FELDER)
ANKER  = 'var car = { id: doc.id,'


def sicher_schreiben(pfad, text):
    """Nie open(pfad,"w") — bei einem Fehler waere die Datei leer."""
    ordner = os.path.dirname(os.path.abspath(pfad))
    fd, tmp = tempfile.mkstemp(dir=ordner, suffix=".tmp")
    try:
        with io.open(fd, "w", encoding="utf-8", newline="") as f:
            f.write(text)
        os.replace(tmp, pfad)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def js_pruefen(text):
    """node --check ueber das eingebettete Skript."""
    bloecke = re.findall(r"<script[^>]*>(.*?)</script>", text, re.S)
    if not bloecke:
        return "kein <script>-Block gefunden"
    fd, tmp = tempfile.mkstemp(suffix=".js")
    try:
        with io.open(fd, "w", encoding="utf-8") as f:
            f.write(max(bloecke, key=len))
        r = subprocess.run(["node", "--check", tmp], capture_output=True, text=True)
        return None if r.returncode == 0 else (r.stderr or r.stdout)[:800]
    finally:
        os.unlink(tmp)


def patchen(pfad):
    text = io.open(pfad, encoding="utf-8").read()
    if ANKER not in text:
        return "Anker nicht gefunden — hat sich der Loader geaendert?"
    # 🚨 Nur IM Karussell-Block pruefen. `profil: d0.profil` steht auch im
    # Reel-Loader — ein Test ueber die ganze Datei meldet "schon gepatcht",
    # obwohl nichts passiert ist. Genau das ist beim ersten Lauf passiert.
    block = re.search(r"var car = \{ id: doc\.id.*?\};", text, re.S)
    if not block:
        return "Karussell-Loader nicht gefunden"
    if ('%s: d0.%s' % (FELDER[0], FELDER[0])) in block.group(0):
        print("  schon gepatcht, nichts zu tun")
        return None
    neu = text.replace(ANKER, ANKER + ZUSATZ, 1)
    if neu == text:
        return "Ersetzung hat nichts geaendert"
    fehler = js_pruefen(neu)
    if fehler:
        return "node --check schlaegt fehl:\n" + fehler
    sicher_schreiben(pfad, neu)
    print("  gepatcht: " + ", ".join(FELDER))
    return None


def gegenprobe(pfad):
    """Loader und Saver muessen danach dieselben Felder kennen."""
    t = io.open(pfad, encoding="utf-8").read()
    lo = re.search(r"var car = \{ id: doc\.id.*?\};", t, re.S)
    sa = re.search(r'db\.collection\("karussells"\)\.doc\(car\.id\)\.set\(\{.*?\}\)', t, re.S)
    if not (lo and sa):
        return "Loader oder Saver nicht gefunden"
    lf = set(re.findall(r"(\w+):", lo.group(0)))
    sf = set(re.findall(r"(\w+):", sa.group(0)))
    fehlt = sorted(sf - lf)
    if fehlt:
        return "Saver schreibt weiter Felder, die der Loader wegwirft: %s" % fehlt
    print("  Gegenprobe: Loader kennt alle %d Felder des Savers" % len(sf))
    return None


if __name__ == "__main__":
    ziele = sys.argv[1:] or ["outputs/cockpit/mlb-cockpit.html"]
    schlecht = 0
    for p in ziele:
        print(p)
        for schritt in (patchen, gegenprobe):
            f = schritt(p)
            if f:
                print("  FEHLER: " + f)
                schlecht = 1
                break
    sys.exit(schlecht)
