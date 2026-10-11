# -*- coding: utf-8 -*-
"""Legt die zwei Editoren zusammen (Patricias Entscheid vom 14.09.2026).

Das Cockpit hatte einen eigenen Karussell-Editor, der die Folien im Canvas
nachzeichnet. Daneben steht der Bild-Editor als eigenes Artifact, der die echte
Bühne exportiert und inzwischen mehr kann (mehrere Textbalken, Video mit
eingebranntem Text, eigene Bilder, Ideen, Speichern).

Zwei Editoren für dieselbe Sache sind genau das, was Patricia nicht will.
Deshalb: Cockpit = prüfen und freigeben, Bild-Editor = bauen.

Das Skript ist wiederholbar — schon gesetzte Änderungen werden übersprungen.
"""
import io, os, sys

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
PFAD = "outputs/cockpit/mlb-cockpit.html"
EDITOR = "https://claude.ai/code/artifact/21e66e0e-2576-41db-8c8d-f14d7079a1e0"

t = io.open(PFAD, encoding="utf-8").read()
vorher = t
getan, schon = [], []

# ---------------------------------------------------------------- 1) Reiter raus
alt = '    { id: "karussell", label: "Karussell-Editor" },\n'
if alt in t:
    t = t.replace(alt, "")
    getan.append("Reiter 'Karussell-Editor' aus der Navigation entfernt")
else:
    schon.append("Reiter war schon draussen")

# ------------------------------------------- 2) Knopf auf der Wochenkarte umbiegen
alt = ("""      felder[2].onclick = function () {
        activeCarousel = b.obj.id;
        activeTab = "karussell";
        render();
      };""")
neu = ("""      felder[2].onclick = function () {
        // Gebaut wird im Bild-Editor — hier wird nur geprüft und freigegeben.
        activeCarousel = b.obj.id;
        window.open(BILDEDITOR, "_blank", "noopener");
      };""")
if alt in t:
    t = t.replace(alt, neu)
    getan.append("Knopf auf der Wochenkarte oeffnet den Bild-Editor")
else:
    schon.append("Knopf war schon umgebogen")

alt = '<button class="btn">Im Editor öffnen</button>'
neu = '<button class="btn">Im Bild-Editor bauen</button>'
if alt in t:
    t = t.replace(alt, neu)
    getan.append("Knopf heisst jetzt 'Im Bild-Editor bauen'")

# ------------------------------------ 3) Der Weg aus dem Content-Studio ebenfalls
alt = ("""        state.karussells.unshift(car);
        activeCarousel = car.id;
        saveCarousel(car);
        activeTab = "karussell";
        render();
        toast("Karussell angelegt. Erst die Texte prüfen und freigeben, dann bauen.");""")
neu = ("""        state.karussells.unshift(car);
        activeCarousel = car.id;
        saveCarousel(car);
        activeTab = "woche";
        render();
        toast("Karussell angelegt. Texte prüfen und freigeben, gebaut wird im Bild-Editor.");""")
if alt in t:
    t = t.replace(alt, neu)
    getan.append("Content-Studio landet nach dem Anlegen in der Wochen-Vorschau")
else:
    schon.append("Content-Studio-Weg war schon gesetzt")

# ------------------------------------------- 4) Route ins Leere gibt es nicht mehr
alt = '    else if (activeTab === "karussell") renderKarussell(main);\n'
if alt in t:
    t = t.replace(alt, "")
    getan.append("Route auf den alten Editor entfernt")
else:
    schon.append("Route war schon entfernt")

# --------------- 4b) Zwei Stellen, die auf den entfernten Reiter horchten
# Die Folienbilder werden jetzt in der Wochen-Vorschau gezeichnet, nicht mehr im
# alten Editor — sonst erscheinen nachgeladene Bilder erst beim naechsten Klick.
alt = '            if (neu && activeTab === "karussell") render();'
neu = '            if (neu && activeTab === "woche") render();'
if alt in t:
    t = t.replace(alt, neu)
    getan.append("Nachgeladene Folienbilder zeichnen die Wochen-Vorschau neu")
else:
    schon.append("Folienbild-Nachladen war schon umgehaengt")

alt = '    window.claude.use("sample").then(function (s) { sampler = s; if (activeTab === "karussell") render(); }).catch(function () {});'
neu = '    window.claude.use("sample").then(function (s) { sampler = s; render(); }).catch(function () {});'
if alt in t:
    t = t.replace(alt, neu)
    getan.append("Schreib-Faehigkeit zeichnet die Seite neu, sobald sie da ist")
else:
    schon.append("Schreib-Faehigkeit war schon umgehaengt")

# ---------------------------------------------------------- 5) Adresse hinterlegen
if "var BILDEDITOR" not in t:
    anker = '  var activeTab = "uebersicht";'
    assert anker in t, "Anker fuer die Adresse nicht gefunden"
    t = t.replace(anker, '  var BILDEDITOR = "' + EDITOR + '";\n' + anker)
    getan.append("Adresse des Bild-Editors hinterlegt")
else:
    schon.append("Adresse war schon hinterlegt")

if t != vorher:
    io.open(PFAD, "w", encoding="utf-8", newline="\n").write(t)

print("Geaendert:")
for z in getan:
    print("  +", z)
if schon:
    print("Schon so:")
    for z in schon:
        print("  =", z)
if not getan:
    print("  (nichts zu tun)")
