"""Content-Kalender mit Instagram-Abgleich, Archivregel, schlankere Leiste,
Freigeben in drei Spalten (16.10.2026).

Patricia, 16.10.: *„ich will im contentkalender, dass das abgeglichen wird"* ·
Aufräumregel *„ja bitte"* · Reels-Reiter *„kann nach mir raus"* · Ideenkasten
*„ich muss das nicht sehen"* · Ideen von anderen *„brauche ich eigentlich nicht"* ·
Freigegeben *„habe ich das jetzt freigegeben oder du??"*.

1. `tiContent` (Mein Tisch) wird ersetzt durch `kalender-abgleich.js`:
   7 Tage zurück, 14 voraus, je Beitrag gepostet / nicht gefunden / spontan.
2. **Archivregel:** Was mehr als 14 Tage über dem Datum liegt und nie
   freigegeben wurde, gilt als archiviert — es läuft durch `istAbgelehnt`, steht
   also überall dort NICHT mehr, wo Abgelehntes schon heute ausgeblendet wird,
   und unten in der Woche unter „Archiv“ mit Rückweg. Nichts wird gelöscht.
   „Zurückholen“ setzt `ausArchiv: true`, sonst fiele der Beitrag sofort zurück.
3. Reiter Reels, Ideenkasten und Ideen von anderen aus der Leiste (Code bleibt).
4. Freigeben: unten drei Spalten „1 · Von dir freigegeben → 2 · Von mir
   eingeplant → 3 · Draussen“.

Wiederholbar über @@-Marken.
    python scripts/cockpit/patch-kalender-archiv.py
"""
import os
import pathlib
import re
import subprocess
import sys
import tempfile

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HIER = pathlib.Path(__file__).resolve().parent
DATEI = HIER.parents[1] / "outputs" / "cockpit" / "mlb-cockpit.html"

KA_A, KA_E = "  /* @@kalender-anfang */\n", "  /* @@kalender-ende */\n"


def ersetze(s, alt, neu, name):
    if neu in s:
        return s
    if s.count(alt) != 1:
        sys.exit("FEHLER: %s — Stelle %d-mal gefunden" % (name, s.count(alt)))
    return s.replace(alt, neu)


def main():
    s = DATEI.read_text(encoding="utf-8")
    js = (HIER / "kalender-abgleich.js").read_text(encoding="utf-8")

    # 1 · Kalender
    if KA_A in s:
        s = re.sub(re.escape(KA_A) + ".*?" + re.escape(KA_E), lambda m: KA_A + js + KA_E, s, flags=re.S)
    else:
        m = re.search(r"  /\* ---------- Content-Kalender ---------- \*/\n.*?(?=  /\* ---------- Helferinnen ---------- \*/)", s, re.S)
        if not m:
            sys.exit("FEHLER: alter Content-Kalender nicht gefunden")
        s = s[:m.start()] + KA_A + js + KA_E + "\n" + s[m.end():]

    # 2 · Archivregel
    s = ersetze(s,
        "  function istAbgelehnt(b) { return !!(b.obj || b).abgelehnt; }",
        "  function istAbgelehnt(b) { return !!(b.obj || b).abgelehnt || istVerfallen(b); }\n"
        "  /* Archivregel (16.10.2026): mehr als 14 Tage über dem Datum und nie\n"
        "     freigegeben. Gelöscht wird nichts; „Zurückholen“ setzt ausArchiv. */\n"
        "  function istVerfallen(b) {\n"
        "    var o = b.obj || b;\n"
        "    if (o.ausArchiv || o.textfrei || !o.datum || freigabeVon(b)) return false;\n"
        "    var g = new Date(); g.setDate(g.getDate() - 14);\n"
        "    var iso = g.getFullYear() + \"-\" + String(g.getMonth() + 1).padStart(2, \"0\") + \"-\" +\n"
        "              String(g.getDate()).padStart(2, \"0\");\n"
        "    return o.datum < iso;\n"
        "  }",
        "Archivregel")
    s = ersetze(s,
        "      ab.innerHTML = '<h2>Abgelehnt (' + abgelehnt.length + ')</h2>' +\n"
        "        '<p class=\"note\">Aus allen Arbeitsansichten raus, aber nicht gel\\u00f6scht.</p>';",
        "      ab.innerHTML = '<h2>Archiv (' + abgelehnt.length + ')</h2>' +\n"
        "        '<p class=\"note\">Abgelehnt oder mehr als 14 Tage über dem Datum und nie freigegeben. ' +\n"
        "        'Aus allen Arbeitsansichten raus, aber nicht gel\\u00f6scht.</p>';",
        "Archiv-Überschrift")
    s = ersetze(s,
        "          b.obj.abgelehnt = false;\n          if (b.art === \"reels\") saveReel(b.obj);",
        "          b.obj.abgelehnt = false;\n          b.obj.ausArchiv = true;\n          if (b.art === \"reels\") saveReel(b.obj);",
        "Zurückholen")

    # 3 · Leiste
    s = ersetze(s,
        'tabs: ["woche", "studio", "storys", "reels", "fertig", "gepostet", "ideenkasten", "ideenextern", "markt"] },',
        'tabs: ["woche", "studio", "storys", "fertig", "gepostet", "markt"] },',
        "Instagram-Leiste")
    for zeile in ('    { id: "reels", label: "Reels", sub: true },\n',
                  '    { id: "ideenkasten", label: "Ideenkasten" },\n',
                  '    { id: "ideenextern", label: "Ideen von anderen" },\n'):
        if zeile in s:
            s = s.replace(zeile, "")

    # 4 · Freigeben in drei Spalten
    alt = s[s.find('    liste("Unterwegs", selbst.length'):]
    alt = alt[:alt.find('      gepostet, "ich");\n') + len('      gepostet, "ich");\n')]
    if "@@fb-board" not in s:
        if not alt.startswith('    liste("Unterwegs"'):
            sys.exit("FEHLER: Freigeben-Listen nicht gefunden")
        neu = (
            "    /* @@fb-board — drei Spalten, wer dran ist steht im Titel (16.10.2026). */\n"
            "    var board = document.createElement(\"div\");\n"
            "    board.className = \"fb-board\";\n"
            "    box.appendChild(board);\n"
            "    var warten = laeuft.filter(function (b) { return DRAUSSEN.indexOf(draussenStatus(b)) < 0 && b.art !== \"storys\"; });\n"
            "    var eingeplant = laeuft.filter(function (b) { return warten.indexOf(b) < 0; });\n"
            "    [[\"1 · Von dir freigegeben\", \"Du hast auf Freigeben gedrückt. Mein nächster Lauf (alle zwei Stunden) plant es bei Blotato ein.\", warten],\n"
            "     [\"2 · Von mir eingeplant\", \"Bei Blotato eingeplant — oder in deiner App, wenn es ein B-Roll oder eine Story ist. Du musst nichts mehr tun.\", eingeplant],\n"
            "     [\"3 · Draussen\", \"Auf Instagram wiedergefunden, mit Zahlen. Die Auswertung steht unter „Ausgewertet“ und im Content-Kalender.\", gepostet]\n"
            "    ].forEach(function (sp) {\n"
            "      var c = document.createElement(\"div\");\n"
            "      c.className = \"fb-spalte\";\n"
            "      board.appendChild(c);\n"
            "      box = c;\n"
            "      if (sp[2].length) liste(sp[0], sp[1], sp[2], \"ich\");\n"
            "      else c.innerHTML = '<div class=\"wt-kopf\"><span class=\"wt-name\">' + esc(sp[0]) + '</span><span class=\"wt-datum\">0</span></div>' +\n"
            "        '<p class=\"note\">' + esc(sp[1]) + '</p>';\n"
            "    });\n")
        s = s.replace(alt, neu)

    # CSS
    css = ("  /* @@kalender-css */\n"
           "  .ti-post.ka-vorbei { opacity: .88; }\n"
           "  .ti-post.ka-heute { border-left: 3px solid var(--orange); padding-left: 8px; }\n"
           "  .fb-board { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 14px; margin-top: 8px; }\n"
           "  .fb-spalte { min-width: 0; }\n")
    if "@@kalender-css" not in s:
        anker = "  .page-head { display: flex;"
        if s.count(anker) != 1:
            sys.exit("FEHLER: CSS-Anker")
        s = s.replace(anker, css + anker)

    for muss in ("function kaZeile(", "function istVerfallen(", "@@fb-board", "letzte_posts"):
        if muss not in s:
            sys.exit("FEHLER: Gegenprobe fehlt: " + muss)
    if '"ideenextern", "markt"' in s:
        sys.exit("FEHLER: Leiste nicht umgestellt")

    teile = re.findall(r"<script>(.*?)</script>", s, re.S)
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
        f.write(max(teile, key=len))
        tmp = f.name
    r = subprocess.run(["node", "--check", tmp], capture_output=True, text=True)
    os.unlink(tmp)
    if r.returncode != 0:
        sys.exit("FEHLER node --check:\n" + r.stderr[:800])
    neu = DATEI.with_suffix(".tmp")
    neu.write_text(s, encoding="utf-8")
    os.replace(neu, DATEI)
    print("node --check: in Ordnung · geschrieben:", DATEI)


if __name__ == "__main__":
    main()
