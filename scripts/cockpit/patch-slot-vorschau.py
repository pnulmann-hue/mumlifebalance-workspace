"""Zwei Beiträge dürfen nicht auf denselben Tag rutschen.

🚨 **Gefunden in der eigenen Sichtprüfung, 24.09.2026:** Nach dem Einbau des
Nachrückens stand in der Liste **viermal „Geht Mo 28.09. raus"**. Dort ist aber
genau ein Platz.

**Die Ursache:** `naechsterSlot(b)` prüft, welche Tage durch *gesetzte* Daten
belegt sind — nicht, welche es gerade selbst an andere Beiträge vergeben hat.
Jeder Aufruf rechnet für sich allein und kommt deshalb auf dieselbe Antwort.

Beim **Freigeben** stimmt es trotzdem, weil dort `b.obj.datum` sofort gesetzt
wird und der nächste Beitrag den Tag als belegt sieht. Falsch ist nur die
**Vorschau** — und eine Anzeige, die vier Beiträgen denselben Tag verspricht, ist
schlimmer als gar keine: sie sieht aus wie eine Zusage.

**Der Merkzettel `slotVorschau`** läuft innerhalb eines Zeichendurchlaufs mit:
jeder Fund wird eingetragen und beim nächsten Aufruf mitgeprüft. Zurückgesetzt
wird er am Anfang von `render()` — sonst schleppt die Seite nach zehn Durchläufen
eine Belegung mit, die niemand gesetzt hat.

🚨 **Der Merkzettel gilt nur für die Vorschau.** Beim Freigeben zählt weiter das
echte Datum, sonst würde ein Zeichendurchlauf entscheiden, wohin ein Beitrag
geht.

Dazu eine Kleinigkeit, die seit dem Umbau des Tasks falsch dastand: der
Einplan-Lauf läuft **alle zwei Stunden von 8 bis 22 Uhr**, nicht mehr nur um
20:00. An drei Stellen stand noch die alte Zeit.

    python scripts/cockpit/patch-slot-vorschau.py [--pruefen] [--datei <pfad>]
"""

import re
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]

ALT_FN = '''  function naechsterSlot(b) {
    var zeit = (b.obj.blotato && b.obj.blotato.zeit) ||
               vorgabeZeit(b.art, kartenProfil(b.obj));
    var profil = kartenProfil(b.obj);'''

NEU_FN = '''  /* 🚨 Merkzettel fuer EINEN Zeichendurchlauf: was die Vorschau schon an
     andere Beitraege vergeben hat. Ohne ihn bekommen vier Beitraege denselben
     Tag angezeigt, und dort ist genau ein Platz. Siehe Kopf von
     patch-slot-vorschau.py. Zurueckgesetzt in render(). */
  var slotVorschau = {};

  function naechsterSlot(b, merken2) {
    var zeit = (b.obj.blotato && b.obj.blotato.zeit) ||
               vorgabeZeit(b.art, kartenProfil(b.obj));
    var profil = kartenProfil(b.obj);'''

ALT_BELEGT = '''      belegt[x.obj.datum] = true;
    });'''
NEU_BELEGT = '''      belegt[x.obj.datum] = true;
    });
    // Dazu, was die Vorschau in diesem Durchlauf schon vergeben hat.
    Object.keys(slotVorschau).forEach(function (k) {
      var teil = k.split("|");
      if (teil[1] === profil && teil[2] !== b.id) belegt[teil[0]] = true;
    });'''

ALT_RET = '''      if (isNaN(wann) || wann.getTime() < frueheste) continue;
      return { datum: iso, zeit: zeit, verschoben: iso !== b.obj.datum };'''
NEU_RET = '''      if (isNaN(wann) || wann.getTime() < frueheste) continue;
      if (merken2 !== false) slotVorschau[iso + "|" + profil + "|" + b.id] = true;
      return { datum: iso, zeit: zeit, verschoben: iso !== b.obj.datum };'''

# Beim Freigeben zaehlt das echte Datum, nicht der Vorschau-Merkzettel.
ALT_FREIGABE = '        var slot = naechsterSlot(b);'
NEU_FREIGABE = '        var slot = naechsterSlot(b, false);'

# render() setzt den Merkzettel zurueck.
ALT_RENDER = '''  function render() {'''
NEU_RENDER = '''  function render() {
    // Jeder Durchlauf rechnet neu — sonst schleppt die Seite eine Belegung
    // mit, die niemand gesetzt hat.
    slotVorschau = {};'''

# Der Einplan-Lauf ist laengst alle zwei Stunden, nicht mehr nur um 20:00.
ZEITEN = [
    ('tile("Schon freigegeben", frei.length, "wartet auf 20:00")',
     'tile("Schon freigegeben", frei.length, "wartet auf den nächsten Lauf")'),
]


def setze(text, alt, neu, name):
    n = text.count(alt)
    if n != 1:
        sys.exit("🚨 «%s» kommt %dx vor — erwartet genau 1x. Nichts geändert."
                 % (name, n))
    return text.replace(alt, neu, 1)


def js_pruefen(html):
    for i, block in enumerate(re.findall(r"<script[^>]*>(.*?)</script>", html, re.S)):
        if len(block.strip()) < 200:
            continue
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False,
                                         encoding="utf-8") as f:
            f.write(block)
            p = f.name
        r = subprocess.run(["node", "--check", p], capture_output=True, text=True)
        Path(p).unlink(missing_ok=True)
        if r.returncode != 0:
            return "Block %d: %s" % (i, (r.stderr or "")[:700])
    return ""


def main():
    nur_pruefen = "--pruefen" in sys.argv
    datei = ROOT / "outputs" / "cockpit" / "mlb-cockpit-neu.html"
    if "--datei" in sys.argv:
        datei = Path(sys.argv[sys.argv.index("--datei") + 1])

    s = datei.read_text(encoding="utf-8")
    if "slotVorschau" in s:
        print("  Schon eingebaut — nichts zu tun.")
        return

    s = setze(s, ALT_FN, NEU_FN, "naechsterSlot")
    s = setze(s, ALT_BELEGT, NEU_BELEGT, "Belegung")
    s = setze(s, ALT_RET, NEU_RET, "Rueckgabe")
    s = setze(s, ALT_FREIGABE, NEU_FREIGABE, "Freigabe")
    s = setze(s, ALT_RENDER, NEU_RENDER, "render")
    for alt, neu in ZEITEN:
        if s.count(alt) == 1:
            s = s.replace(alt, neu, 1)
        else:
            print("  ⚠️ Zeitangabe nicht eindeutig (%dx) — übersprungen." % s.count(alt))

    fehler = js_pruefen(s)
    if fehler:
        sys.exit("🚨 node --check meldet einen Fehler — NICHTS geschrieben:\n  %s"
                 % fehler)
    if nur_pruefen:
        print("  Syntax in Ordnung. Mit --pruefen wird nicht geschrieben.")
        return

    datei.write_text(s, encoding="utf-8")
    print("  Slot-Vorschau eingebaut · %d KB" % (len(s) / 1024))
    print("  Jeder Beitrag bekommt einen eigenen Tag in der Vorschau.")


if __name__ == "__main__":
    main()
