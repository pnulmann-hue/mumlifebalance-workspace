# -*- coding: utf-8 -*-
"""Hängt den vollständigen Marken-Brief in beide Artifact-Seiten ein (14.09.2026).

Patricias Erwartung: „ich erwarte schon, dass content-studio auf alles zugreift, wie wenn
ich dir hier den befehl content gebe. also caption richtig, hook richtig, PIE strategie."

Der Brief wird von `wissen-bauen.py` aus den echten Quellen erzeugt und liegt als Dokument
`daten/wissen-voll` in der Datenbank des jeweiligen Artifacts. Beide Seiten lesen ihn beim
Öffnen und hängen ihn an jeden Auftrag. Fehlt er, arbeiten sie weiter wie vorher —
die Seite darf daran nicht scheitern.

Wiederholbar. Schon Gesetztes wird übersprungen.
"""
import io, os

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
getan, schon = [], []


def patch(pfad, paare, name):
    t = io.open(pfad, encoding="utf-8").read()
    vorher = t
    for alt, neu, was in paare:
        if alt in t:
            t = t.replace(alt, neu, 1)
            getan.append(name + ": " + was)
        elif neu.split("\n")[0].strip() in t:
            schon.append(name + ": " + was)
        else:
            print("!! Anker nicht gefunden in " + pfad + " — " + was)
    if t != vorher:
        io.open(pfad, "w", encoding="utf-8", newline="\n").write(t)


# ------------------------------------------------------------------ 1) Cockpit
COCKPIT = "outputs/cockpit/mlb-cockpit.html"

c_alt1 = "  var wissen = {};"
c_neu1 = ("  var wissen = {};\n"
          "  /* Der vollstaendige Marken-Brief. Kommt als Dokument aus der Datenbank,\n"
          "     erzeugt von scripts/cockpit/wissen-bauen.py aus den echten Quellen.\n"
          "     Fehlt er, laeuft die Seite mit den sieben Feldern weiter. */\n"
          "  var wissenVoll = null;")

c_alt2 = "    teile.push(HOOKREGELN);\n    return teile.join(\"\\n\\n\");"
c_neu2 = ("    teile.push(HOOKREGELN);\n"
          "    if (wissenVoll && wissenVoll.text) {\n"
          "      teile.push(\"DAS VOLLSTAENDIGE MARKENWISSEN (Stand \" +\n"
          "        (wissenVoll.stand || \"unbekannt\") + \")\\n\" + wissenVoll.text);\n"
          "    }\n"
          "    return teile.join(\"\\n\\n\");")

c_alt3 = ('      db.doc("daten/wissen").onSnapshot(function (snap) {')
c_neu3 = ('      db.doc("daten/wissen-voll").get().then(function (snap) {\n'
          '        if (snap.exists) { wissenVoll = snap.data(); lsSet("wissen-voll", wissenVoll); }\n'
          '      }).catch(function () {});\n'
          '      db.doc("daten/wissen").onSnapshot(function (snap) {')

c_alt4 = '  Object.assign(wissen, lsGet("wissen", {}) || {});'
c_neu4 = ('  Object.assign(wissen, lsGet("wissen", {}) || {});\n'
          '  wissenVoll = lsGet("wissen-voll", null);')

patch(COCKPIT, [
    (c_alt1, c_neu1, "Platz fuer den Brief"),
    (c_alt2, c_neu2, "Brief geht an jeden Auftrag mit"),
    (c_alt3, c_neu3, "Brief wird aus der Datenbank geholt"),
    (c_alt4, c_neu4, "Brief beim Start aus dem lokalen Speicher"),
], "Cockpit")

# -------------------------------------------------------------- 2) Bild-Editor
EDITOR = "outputs/_bild-editor/index.html"

e_alt1 = "  let wocheDaten = null, beitragDaten = null, entwurfDaten = null, themaAuto = \"\";"
e_neu1 = ("  let wocheDaten = null, beitragDaten = null, entwurfDaten = null, themaAuto = \"\";\n"
          "  // Der vollstaendige Marken-Brief aus der Datenbank. Fehlt er, reicht WISSEN.\n"
          "  let wissenVoll = null;")

e_alt2 = """      const [w, b, e] = await Promise.all([ db.doc("daten/woche").get(),
                                            db.doc("daten/beitraege").get(),
                                            db.doc("daten/entwuerfe").get() ]);"""
e_neu2 = """      const [w, b, e, v] = await Promise.all([ db.doc("daten/woche").get(),
                                               db.doc("daten/beitraege").get(),
                                               db.doc("daten/entwuerfe").get(),
                                               db.doc("daten/wissen-voll").get() ]);
      if (v.exists) wissenVoll = v.data();"""

e_alt3 = """    const auftrag =
`${WISSEN}"""
e_neu3 = """    const auftrag =
`${WISSEN}
${wissenVoll && wissenVoll.text ? "\\n== DAS VOLLSTAENDIGE MARKENWISSEN (Stand " + (wissenVoll.stand || "unbekannt") + ") ==\\n" + wissenVoll.text : ""}"""

patch(EDITOR, [
    (e_alt1, e_neu1, "Platz fuer den Brief"),
    (e_alt2, e_neu2, "Brief wird mitgeholt"),
    (e_alt3, e_neu3, "Brief geht an den Auftrag mit"),
], "Bild-Editor")

print("Geaendert:")
for z in getan:
    print("  +", z)
if schon:
    print("Schon so:")
    for z in schon:
        print("  =", z)
if not getan:
    print("  (nichts zu tun)")
