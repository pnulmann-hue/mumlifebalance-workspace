"""Reiter «Instagram → Testreels» (31.10.2026).

Patricia: *„kannst du mir im cockpit was einbauen, dass ich die testreelvarianten direkt
darin finde?“* · *„die idee ist, dass ich für jeden tag die fixfertigen testreels nach
datum sehe, die ich zum testen posten kann. die besten nehme ich selber in den feed.
paralell machen wir aber auch beiträge die so oder so gepostet werden“*.
Code und CSS liegen daneben in `testreels-reiter.js` / `.css`.

Wiederholbar: steht der Reiter schon drin, werden nur sein JS- und sein CSS-Block ersetzt
und fehlende Felder nachgetragen.

Was der Patch ausser dem Reiter noch macht:

1. **Das Cockpit lud nur 60 Reels** (`db.collection("reels").limit(60)`). In der Datenbank
   lagen am 31.10. aber 71, und die Abfrage liefert nach Kennung sortiert. Alles ab
   «kw45-…» fiel heraus, darunter die Radar-Reels. Dieselbe Falle wie beim Story-Limit
   (25.09.). Jetzt 500.
2. **Neue Felder in die feste Feldliste von saveReel und beim Lesen.** Was dort fehlt, ist
   nach dem nächsten Speichern weg (Lehre vom 16.09. und 18.09.).
3. **Testreels raus aus `alleBeitraege()`.** Sie belegen keinen Feed-Platz in der Woche,
   gehen nicht in „Freigeben“ und nicht in den Content-Kalender — die Feed-Beiträge laufen
   daneben weiter.

    python scripts/cockpit/patch-testreels.py [--datei <cockpit.html>]
"""

import os
import pathlib
import subprocess
import sys
import tempfile

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HIER = pathlib.Path(__file__).resolve().parent
ROOT = HIER.parents[1]
JS_DATEI = HIER / "testreels-reiter.js"
CSS_DATEI = HIER / "testreels-reiter.css"

JS_ANFANG = '''  /* ======================================================================
     Reiter "Testreels"'''
CSS_ANFANG = '''  /* ---------- Reiter „Testreels“'''

A_TABS = '''    { id: "radar", label: "Markt-Radar" },'''
N_TABS = A_TABS + '''
    { id: "testreels", label: "Testreels" },'''

A_BER = '''"gepostet", "markt", "radar"] },'''
N_BER = '''"gepostet", "markt", "radar", "testreels"] },'''

A_DISP = '''    else if (activeTab === "radar") renderMarktRadar(main);'''
N_DISP = A_DISP + '''
    else if (activeTab === "testreels") renderTestreels(main);'''

A_LIMIT = '''db.collection("reels").limit(60)'''
N_LIMIT = '''db.collection("reels").limit(500)'''

A_SAVE = '''blotato: r.blotato || null, updatedAt: r.updatedAt'''
N_SAVE = '''blotato: r.blotato || null,
        // Testreels und Rolle (31.10.2026, patch-testreels.py)
        rolle: r.rolle || "", quelle: r.quelle || "",
        trial: !!r.trial, testVon: r.testVon || "", testStand: r.testStand || "",
        testGepostetAm: r.testGepostetAm || "",
        testReichweite: (typeof r.testReichweite === "number") ? r.testReichweite : null,
        testKommentare: (typeof r.testKommentare === "number") ? r.testKommentare : null,
        testNotiz: r.testNotiz || "", testGewinner: !!r.testGewinner, testInFeed: !!r.testInFeed,
        updatedAt: r.updatedAt'''

A_LESEN = '''videodatei: d0.videodatei || "", blotato: d0.blotato || null, updatedAt: d0.updatedAt || "" };'''
N_LESEN = ('''videodatei: d0.videodatei || "", blotato: d0.blotato || null, '''
           '''rolle: d0.rolle || "", quelle: d0.quelle || "", trial: !!d0.trial, testVon: d0.testVon || "", '''
           '''testStand: d0.testStand || "", testGepostetAm: d0.testGepostetAm || "", '''
           '''testReichweite: (typeof d0.testReichweite === "number") ? d0.testReichweite : null, '''
           '''testKommentare: (typeof d0.testKommentare === "number") ? d0.testKommentare : null, '''
           '''testNotiz: d0.testNotiz || "", testGewinner: !!d0.testGewinner, testInFeed: !!d0.testInFeed, updatedAt: d0.updatedAt || "" };''')

# Nachtrag fuer eine Fassung, die den ersten Lauf schon hat
A_SAVE2 = '''testNotiz: r.testNotiz || "", testGewinner: !!r.testGewinner,
        updatedAt: r.updatedAt'''
N_SAVE2 = '''testNotiz: r.testNotiz || "", testGewinner: !!r.testGewinner, testInFeed: !!r.testInFeed,
        updatedAt: r.updatedAt'''
A_LESEN2 = '''testGewinner: !!d0.testGewinner, updatedAt: d0.updatedAt || "" };'''
N_LESEN2 = '''testGewinner: !!d0.testGewinner, testInFeed: !!d0.testInFeed, updatedAt: d0.updatedAt || "" };'''

# Nachtrag 01.11.2026: der Prüfvermerk der Hook-Sperre reist mit (scripts/hooks/hook-sperre.py)
A_SAVE3 = '''testInFeed: !!r.testInFeed,
        updatedAt: r.updatedAt'''
N_SAVE3 = '''testInFeed: !!r.testInFeed, pruefung: r.pruefung || null,
        updatedAt: r.updatedAt'''
A_LESEN3 = '''testInFeed: !!d0.testInFeed, updatedAt: d0.updatedAt || "" };'''
N_LESEN3 = '''testInFeed: !!d0.testInFeed, pruefung: d0.pruefung || null, updatedAt: d0.updatedAt || "" };'''

A_ALLE = '''    state.reels.forEach(function (r) {
      beitraege.push({ art: "reels", id: r.id, obj: r, format: "Reel",'''
N_ALLE = '''    state.reels.forEach(function (r) {
      // Testreels haben ihren eigenen Reiter und belegen keinen Feed-Platz (31.10.2026).
      if (istTestreel(r)) return;
      beitraege.push({ art: "reels", id: r.id, obj: r, format: "Reel",'''

EINHAENGEN = '''  /* Reiter „Ideen von anderen": was bei den beobachteten Profilen deutlich'''


def ersetze(t, alt, neu, name):
    n = t.count(alt)
    if n != 1:
        sys.exit("🚨 «%s» kommt %dx vor — erwartet genau 1x. Nichts geändert." % (name, n))
    return t.replace(alt, neu, 1)


def pruefe_js(js, wo):
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
        f.write(js)
        tmp = f.name
    r = subprocess.run(["node", "--check", tmp], capture_output=True, text=True)
    os.unlink(tmp)
    if r.returncode != 0:
        sys.exit("🚨 node --check (%s): %s" % (wo, r.stderr or r.stdout))


def main():
    if "--datei" in sys.argv:
        ziel = pathlib.Path(sys.argv[sys.argv.index("--datei") + 1])
    else:
        ziel = ROOT / "outputs/cockpit/mlb-cockpit.html"
    js = JS_DATEI.read_text(encoding="utf-8").rstrip() + "\n\n"
    css = CSS_DATEI.read_text(encoding="utf-8")
    pruefe_js(js, JS_DATEI.name)

    t = ziel.read_text(encoding="utf-8")
    if "function renderMarktRadar(" not in t:
        sys.exit("🚨 Markt-Radar-Reiter fehlt — zuerst patch-markt-radar.py.")
    vorher = len(t)

    if "function renderTestreels(" not in t:
        t = ersetze(t, A_TABS, N_TABS, "TABS")
        t = ersetze(t, A_BER, N_BER, "BEREICHE")
        t = ersetze(t, A_DISP, N_DISP, "Dispatcher")
        t = ersetze(t, A_LIMIT, N_LIMIT, "Reels-Limit")
        t = ersetze(t, A_SAVE, N_SAVE, "saveReel-Feldliste")
        t = ersetze(t, A_LESEN, N_LESEN, "Reels lesen")
        t = ersetze(t, EINHAENGEN, js + EINHAENGEN, "renderTestreels")
        i = t.rfind("</style>")
        t = t[:i] + css + t[i:]
    else:
        # JS-Block ersetzen: vom eigenen Kopf bis zum naechsten Reiter-Kopf
        a = t.find(JS_ANFANG)
        e = t.find(EINHAENGEN, a)
        if a < 0 or e < 0 or t.count(JS_ANFANG) != 1:
            sys.exit("🚨 JS-Block der Testreels nicht eindeutig gefunden.")
        t = t[:a] + js + t[e:]
        # CSS-Block ersetzen: vom eigenen Kopf bis zum naechsten Kommentar oder </style>
        a = t.find(CSS_ANFANG)
        if a < 0 or t.count(CSS_ANFANG) != 1:
            sys.exit("🚨 CSS-Block der Testreels nicht eindeutig gefunden.")
        kandidaten = [x for x in (t.find("\n  /*", a + 10), t.find("</style>", a)) if x > 0]
        e = min(kandidaten)
        t = t[:a] + css.rstrip("\n") + t[e:]
        if "testInFeed: !!r.testInFeed" not in t:
            t = ersetze(t, A_SAVE2, N_SAVE2, "saveReel testInFeed")
        if "testInFeed: !!d0.testInFeed" not in t:
            t = ersetze(t, A_LESEN2, N_LESEN2, "lesen testInFeed")

    if "pruefung: r.pruefung" not in t:
        t = ersetze(t, A_SAVE3, N_SAVE3, "saveReel pruefung")
    if "pruefung: d0.pruefung" not in t:
        t = ersetze(t, A_LESEN3, N_LESEN3, "lesen pruefung")
    if "if (istTestreel(r)) return;" not in t:
        t = ersetze(t, A_ALLE, N_ALLE, "alleBeitraege")

    # Gegenproben: jedes Testfeld muss beim Schreiben UND beim Lesen stehen.
    for feld in ("testStand", "testVon", "testReichweite", "testKommentare", "testInFeed", "rolle", "pruefung"):
        if ("%s: r.%s" % (feld, feld)) not in t and ("%s: (typeof r.%s" % (feld, feld)) not in t \
                and ("%s: !!r.%s" % (feld, feld)) not in t:
            sys.exit("🚨 %s fehlt in saveReel" % feld)
        if ("%s: d0.%s" % (feld, feld)) not in t and ("%s: (typeof d0.%s" % (feld, feld)) not in t \
                and ("%s: !!d0.%s" % (feld, feld)) not in t:
            sys.exit("🚨 %s fehlt beim Lesen" % feld)
    if A_LIMIT in t or N_LIMIT not in t:
        sys.exit("🚨 Reels-Limit steht noch auf 60")
    for marke in ("function renderTestreels(", "function renderIdeenExtern(", "function renderMarktRadar(",
                  "function renderZusatzangebote(", "function renderGekauft("):
        if t.count(marke) != 1:
            sys.exit("🚨 %s kommt %dx vor" % (marke, t.count(marke)))

    pruefe_js(t[t.rfind("<script>") + 8:t.rfind("</script>")], "ganze Seite")

    # Erst in eine Nebendatei, dann umbenennen — ein Fehler beim Schreiben
    # darf das Cockpit nicht leeren.
    neu = ziel.with_suffix(".tmp")
    neu.write_text(t, encoding="utf-8")
    os.replace(neu, ziel)
    print("%s: %d -> %d Zeichen, node --check grün" % (ziel.name, vorher, len(t)))


if __name__ == "__main__":
    main()
