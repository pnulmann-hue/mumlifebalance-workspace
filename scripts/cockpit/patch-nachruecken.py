"""Ein freigegebener Beitrag rutscht nach, statt liegenzubleiben.

Patricia am 24.09.2026: *„und bei freigegeben sind wieder beiträge wo steht
datum ist durch. überlege dir bei den ganzen beitragsgeschichten was
gescheiteres bitte"*.

🚨 **Sie hat recht, und es ist kein Anzeigeproblem.** „Datum ist durch" war eine
**Sackgasse, die sich ständig neu bildet**: jeder Beitrag trägt Datum plus feste
Uhrzeit, und sobald die Uhrzeit vorbei ist, geht er nie mehr raus. Bei einem
Karussell ist die Vorgabezeit **07:30** — wer um zehn Uhr freigibt, ist für
heute grundsätzlich zu spät. Der Beitrag steht dann fertig da, sieht fertig aus,
und passiert nichts. Am 24.09. betraf das fünf Beiträge auf einmal.

**Der bessere Gedanke: Die Freigabe ist die Entscheidung, das Datum nur ein
Wunsch.** Ist der Zeitpunkt vorbei, rutscht der Beitrag auf den nächsten Platz,
der zu ihm passt — und das Cockpit sagt, auf welchen.

**`naechsterSlot(b)` sucht ihn nach drei Regeln:**

| | |
|---|---|
| Format passt zum Tag | Mo · Mi · Fr Reel, Di · Do Karussell (`WOCHENRHYTHMUS`) |
| Zeitpunkt in der Zukunft | mit einer Stunde Luft, damit der 2-Stunden-Lauf ihn erwischt |
| Platz ist frei | kein anderer Beitrag desselben Profils an diesem Tag |

🚨 **Nur bis 28 Tage voraus.** Findet sich bis dahin nichts, bleibt es bei der
alten Anzeige — eine Endlosschleife wäre schlimmer als ein ehrliches „such dir
selbst einen Tag".

🚨 **Nachgerückt wird beim Freigeben, nicht beim Anzeigen.** Was in
`freigaben` steht, muss der Zeitpunkt sein, an dem es wirklich rausgeht; eine
Anzeige, die etwas anderes sagt als die Datenbank, ist genau der Fehler vom
16.09. („Freigegeben und abgelegt", während nichts passieren konnte).

🚨 **`status: "zeitpunkt-vorbei"` entsteht nicht mehr.** Der Wert bleibt im Code
nur, um alte Einträge lesen zu können.

    python scripts/cockpit/patch-nachruecken.py [--pruefen] [--datei <pfad>]
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

# ------------------------------------------------------ 1 · naechsterSlot

ANKER_FN = '''  /* Fertig heisst: nichts fehlt und noch nicht freigegeben. */'''

NEU_FN = '''  /* 🚨 Ein freigegebener Beitrag rutscht nach, statt liegenzubleiben.
     Siehe Kopf von patch-nachruecken.py: „Datum ist durch" war eine Sackgasse,
     die sich jeden Tag neu bildet. Die Freigabe ist die Entscheidung, das
     Datum nur ein Wunsch. */
  function naechsterSlot(b) {
    var zeit = (b.obj.blotato && b.obj.blotato.zeit) ||
               vorgabeZeit(b.art, kartenProfil(b.obj));
    var profil = kartenProfil(b.obj);
    // Eine Stunde Luft, damit der Zwei-Stunden-Lauf den Zeitpunkt sicher
    // erwischt - sonst rutscht er auf etwas, das beim naechsten Lauf schon
    // wieder vorbei ist.
    var frueheste = Date.now() + 3600000;

    // Welche Tage sind mit diesem Profil schon belegt?
    var belegt = {};
    alleBeitraege().forEach(function (x) {
      if (x.id === b.id || istAbgelehnt(x) || !x.obj.datum) return;
      if (kartenProfil(x.obj) !== profil) return;
      belegt[x.obj.datum] = true;
    });

    var start = new Date((b.obj.datum || todayISO()) + "T00:00:00");
    if (isNaN(start)) start = new Date();
    for (var i = 0; i <= 28; i++) {
      var d = new Date(start.getTime());
      d.setDate(d.getDate() + i);
      var wt = (d.getDay() + 6) % 7;          // 0 = Montag
      if (wt > 4) continue;                    // Wochenende: kein Feed-Platz
      if (b.art !== "storys" && WOCHENRHYTHMUS[wt] !== b.art) continue;
      var iso = d.getFullYear() + "-" +
        String(d.getMonth() + 1).padStart(2, "0") + "-" +
        String(d.getDate()).padStart(2, "0");
      if (belegt[iso]) continue;
      var wann = new Date(iso + "T" + zeit);
      if (isNaN(wann) || wann.getTime() < frueheste) continue;
      return { datum: iso, zeit: zeit, verschoben: iso !== b.obj.datum };
    }
    return null;   // nichts gefunden - lieber ehrlich als endlos suchen
  }

  /* Fertig heisst: nichts fehlt und noch nicht freigegeben. */'''

# ---------------------------------------------------- 2 · Freigabe rueckt nach

ALT_FREI = '''      var bl = b.obj.blotato || (b.obj.blotato = {});
      var profil = kartenProfil(b.obj);
      var zeit = (zeitFeld && zeitFeld.value) || bl.zeit || vorgabeZeit(b.art, profil);
      bl.zeit = zeit;
      var wann = new Date(b.obj.datum + "T" + zeit);'''

NEU_FREI = '''      var bl = b.obj.blotato || (b.obj.blotato = {});
      var profil = kartenProfil(b.obj);
      var zeit = (zeitFeld && zeitFeld.value) || bl.zeit || vorgabeZeit(b.art, profil);
      bl.zeit = zeit;
      var wann = new Date(b.obj.datum + "T" + zeit);

      /* 🚨 Nachruecken passiert HIER, beim Freigeben - nicht beim Anzeigen.
         Was in „freigaben" steht, muss der Zeitpunkt sein, an dem es wirklich
         rausgeht. Eine Anzeige, die etwas anderes sagt als die Datenbank, ist
         der Fehler vom 16.09. */
      var nachgerueckt = "";
      if (!isNaN(wann) && wann.getTime() < Date.now()) {
        var slot = naechsterSlot(b);
        if (slot) {
          b.obj.datum = slot.datum;
          zeit = bl.zeit = slot.zeit;
          wann = new Date(slot.datum + "T" + slot.zeit);
          nachgerueckt = tagName(slot.datum).slice(0, 2) + " " + fmtDate(slot.datum) +
                         " um " + slot.zeit;
          merken();
        }
      }'''

ALT_VORBEI = '      var vorbei = !isNaN(wann) && wann.getTime() < Date.now();'
NEU_VORBEI = '''      // Nach dem Nachruecken ist das normalerweise falsch. Bleibt es wahr,
      // hat naechsterSlot in 28 Tagen nichts gefunden.
      var vorbei = !isNaN(wann) && wann.getTime() < Date.now();'''

# ------------------------------------------------------------ 3 · tpStand

ALT_STAND = '''    if (zeitpunktVorbei(b) && b.obj.textfrei)
      return { text: "Freigegeben, Zeitpunkt durch", art: "warn" };
    if (b.obj.textfrei) return { text: "Freigegeben", art: "gut" };
    var fehlt = wasFehlt(b);
    if (!fehlt.length) {
      return zeitpunktVorbei(b)
        ? { text: "Fertig, aber der Zeitpunkt ist durch", art: "warn" }
        : { text: "Fertig — kann raus", art: "gut" };
    }'''

NEU_STAND = '''    if (b.obj.textfrei) return { text: "Freigegeben", art: "gut" };
    var fehlt = wasFehlt(b);
    if (!fehlt.length) {
      // Statt einer Sackgasse sagen, wohin der Beitrag rutscht.
      if (zeitpunktVorbei(b)) {
        var sl = naechsterSlot(b);
        return sl
          ? { text: "Geht " + tagName(sl.datum).slice(0, 2) + " " +
                    fmtDate(sl.datum) + " raus", art: "gut" }
          : { text: "Kein freier Tag — setz eins", art: "warn" };
      }
      return { text: "Fertig — kann raus", art: "gut" };
    }'''

# -------------------------------------------------- 4 · Fertig-Reiter

ALT_GRUPPEN = '''    var kannRaus = feed.filter(function (b) { return !zeitpunktVorbei(b); }).sort(nachDatum);
    var durch = feed.filter(zeitpunktVorbei).sort(nachDatum);'''
NEU_GRUPPEN = '''    // 🚨 Keine eigene Sackgassen-Gruppe mehr - was fertig ist, kann raus,
    // und der Zeitpunkt rueckt beim Freigeben nach.
    var kannRaus = feed.slice().sort(nachDatum);
    var durch = feed.filter(zeitpunktVorbei);'''

ALT_KACHEL = '''      tile("Datum ist durch", durch.length,
           durch.length ? "fertig, aber neu datieren" : "keiner") +'''
NEU_KACHEL = '''      tile("Rutscht nach", durch.length,
           durch.length ? "Zeitpunkt vorbei — geht auf den nächsten Tag"
                        : "alle Zeitpunkte liegen vorn") +'''

ALT_TEXT = '''      '<p>Nur was schon steht \\u2014 Video da, Caption da, Datum da. ' +
      'Freigeben geht hier genauso wie in der Wochen-Vorschau: Datum und ' +
      'Uhrzeit pr\\u00fcfen, Profil pr\\u00fcfen, freigeben. Um 20:00 wird ' +
      'eingeplant, was bis dahin freigegeben ist.</p></div></div>' +'''
NEU_TEXT = '''      '<p>Nur was schon steht \\u2014 Video da, Caption da, Datum da. ' +
      'Alle zwei Stunden wird eingeplant, was freigegeben ist. ' +
      '<strong>Ist der Zeitpunkt vorbei, rutscht der Beitrag auf den n\\u00e4chsten ' +
      'passenden Tag</strong> \\u2014 du musst nichts neu datieren.</p></div></div>' +'''

ALT_GRUPPE_AUFRUF = '''    gruppe("Kann raus", "", kannRaus);
    gruppe("Fertig, aber das Datum ist durch",
           "Hier steht alles. Nur der Zeitpunkt ist vorbei, und Instagram nimmt "
           + "keinen Zeitpunkt in der Vergangenheit. Setz ein neues Datum, dann "
           + "kannst du freigeben.", durch);'''
NEU_GRUPPE_AUFRUF = '''    gruppe("Kann raus", durch.length
      ? durch.length + " davon haben einen Zeitpunkt in der Vergangenheit. Die "
        + "rutschen beim Freigeben auf den nächsten passenden Tag — auf der Karte "
        + "steht, auf welchen."
      : "", kannRaus);'''

ALT_LEER = '''    if (!kannRaus.length && !durch.length && !frei.length) {'''
NEU_LEER = '''    if (!kannRaus.length && !frei.length) {'''


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
    if "naechsterSlot" in s:
        print("  Schon eingebaut — nichts zu tun.")
        return

    s = setze(s, ANKER_FN, NEU_FN, "naechsterSlot")
    s = setze(s, ALT_FREI, NEU_FREI, "Freigabe")
    s = setze(s, ALT_VORBEI, NEU_VORBEI, "vorbei-Kommentar")
    s = setze(s, ALT_STAND, NEU_STAND, "tpStand")
    s = setze(s, ALT_GRUPPEN, NEU_GRUPPEN, "Gruppen")
    s = setze(s, ALT_KACHEL, NEU_KACHEL, "Kachel")
    s = setze(s, ALT_TEXT, NEU_TEXT, "Einleitung")
    s = setze(s, ALT_GRUPPE_AUFRUF, NEU_GRUPPE_AUFRUF, "Gruppen-Aufruf")
    s = setze(s, ALT_LEER, NEU_LEER, "Leer-Fall")

    # Gegenprobe: die Sackgasse darf als Text nicht mehr vorkommen.
    # 🚨 Nur den SICHTBAREN Text prüfen. Beim ersten Lauf schlug die
    # Gegenprobe auf den eigenen Quellkommentar an — dieselbe Falle wie beim
    # Umlaut-Wächter in mails-bauen.py.
    sichtbar = re.sub(r"//[^\n]*|/\*.*?\*/", "", s, flags=re.S)
    rest = sichtbar.count("Datum ist durch") + sichtbar.count("Zeitpunkt ist durch")
    if rest:
        sys.exit("🚨 „Datum ist durch“ steht noch %dx im Text." % rest)

    fehler = js_pruefen(s)
    if fehler:
        sys.exit("🚨 node --check meldet einen Fehler — NICHTS geschrieben:\n  %s"
                 % fehler)
    if nur_pruefen:
        print("  Syntax in Ordnung. Mit --pruefen wird nicht geschrieben.")
        return

    datei.write_text(s, encoding="utf-8")
    print("  Nachrücken eingebaut · %d KB" % (len(s) / 1024))
    print("  Freigegeben heisst: geht raus. Der Tag rückt nach, wenn er durch ist.")


if __name__ == "__main__":
    main()
