"""Bei B-Roll und Story ist der Klick die Erledigung, nicht der Auftrag.

Patricia am 24.09.2026: *„also bei B-Rolls wenn ich freigegeben drücke, dann
habe ich sie auf meinem instagram-app auch eingeplant und die sollten dann
kommen"*.

🚨 **Sie hat recht, und ich habe es vorher falsch herum gebaut.** Die Gruppe
hiess „Du postest selbst", vier Einträge waren als *überfällig* markiert — in
Wahrheit waren sie längst draussen.

**Gegenprobe an den Instagram-Zahlen**, nicht am Gefühl:

| Beitrag | Termin | Instagram |
|---|---|---|
| `kw39-reel-m-mo-b` | 21.09. | **rausgegangen**, Reichweite 207 |
| `kw39-reel-m-mi-a` | 23.09. | **rausgegangen**, Reichweite 184 |
| die zwei doTERRA-Reels | 21./23.09. | nicht prüfbar, das Konto hängt nicht an der API |

**Was der Knopf wirklich bedeutet, hängt vom Format ab:**

| Format | „Freigeben" heisst |
|---|---|
| Karussell, Sprechreel | *plan es für mich ein* — der Lauf übergibt es an Blotato |
| **B-Roll, Story** | *ich habe es selbst in der App eingeplant* — erledigt |

Deshalb heisst der Knopf dort jetzt **„In der App eingeplant"**, die Meldung
danach bestätigt das, und die Einträge stehen unter **„Läuft von selbst"** statt
unter einer Aufgabenliste.

🚨 **Ein Knopf, der bei zwei Formaten dasselbe heisst und Verschiedenes tut, ist
der Fehler.** Dass beim B-Roll niemand etwas einplant, stand bisher nur im
Meldungstext nach dem Klick — auf der Karte war es unsichtbar.

🚨 **Die überfällig-Markierung fällt ersatzlos weg.** Bei einem Format, das sie
selbst postet, kann das Cockpit gar nicht wissen, ob es raus ist; eine Warnung,
die auf Unwissen beruht, ist schlechter als keine.

    python scripts/cockpit/patch-broll-ist-erledigt.py [--pruefen] [--datei <pfad>]
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

# ------------------------------------------------- 1 · Knopf sagt, was er tut

ALT_KNOPF = '''          '<button class="btn wk-frei' + (b.obj.textfrei ? "" : " primary") + '">' +
            (b.obj.textfrei ? "Freigabe zurücknehmen" : "Freigeben") + '</button>' +'''

NEU_KNOPF = '''          /* 🚨 Derselbe Knopf bedeutet je Format etwas anderes: beim Karussell
             „plan es fuer mich ein", beim B-Roll „hab ich selbst eingeplant".
             Siehe Kopf von patch-broll-ist-erledigt.py. */
          '<button class="btn wk-frei' + (b.obj.textfrei ? "" : " primary") + '">' +
            (selbstFormat(b)
              ? (b.obj.textfrei ? "Doch nicht eingeplant" : "In der App eingeplant")
              : (b.obj.textfrei ? "Freigabe zur\\u00fccknehmen" : "Freigeben")) +
          '</button>' +'''

# ---------------------------------------------- 2 · selbstFormat als Funktion

ANKER_FN = '''  function vorgabeZeit(art, profil) {'''
NEU_FN = '''  /* B-Roll und Story gehen nie ueber Blotato — die Instagram-Musik laesst
     sich nur in der App waehlen. Patricia plant sie dort selbst ein; ihr Klick
     im Cockpit ist die Meldung, dass das passiert ist. */
  function selbstFormat(b) {
    return b.art === "storys" ||
           (b.art === "reels" && b.obj.videoart === "broll");
  }

  function vorgabeZeit(art, profil) {'''

# ------------------------------------------------------ 3 · Meldung ehrlich

ALT_TOAST = '''            toast("Freigegeben. B-Roll planen wir nicht ein — lad ihn dir " +
                  "aufs Handy und poste ihn mit deiner Musik.");'''
NEU_TOAST = '''            toast("Notiert — du hast ihn in der App eingeplant. " +
                  "Ich fasse ihn nicht an.");'''

# ----------------------------------------- 4 · Gruppen: selbst = laeuft

ALT_GRUPPEN = '''    var selbst = frei.filter(selbstSache);
    var selbstFaellig = selbst.filter(function (b) {
      return b.obj.datum && b.obj.datum <= heuteISO;
    });
    // Freigegeben, aber der Termin ist durch und nichts rueckt nach: haengt.
    var haengt = frei.filter(function (b) {
      return !selbstSache(b) && DRAUSSEN.indexOf(draussenStatus(b)) < 0 &&
             zeitpunktVorbei(b);
    });
    var laeuft = frei.filter(function (b) {
      return !selbstSache(b) && haengt.indexOf(b) < 0;
    });'''

NEU_GRUPPEN = '''    /* 🚨 Was sie selbst in der App eingeplant hat, IST erledigt — dafuer
       steht ihr Klick. Eine Gruppe „du bist dran" waere eine Behauptung ueber
       etwas, das das Cockpit gar nicht sehen kann. */
    var selbst = frei.filter(selbstSache);
    // Freigegeben, aber der Termin ist durch und nichts rueckt nach: haengt.
    var haengt = frei.filter(function (b) {
      return !selbstSache(b) && DRAUSSEN.indexOf(draussenStatus(b)) < 0 &&
             zeitpunktVorbei(b);
    });
    var laeuft = frei.filter(function (b) { return haengt.indexOf(b) < 0; });'''

ALT_KACHELN = '''      tile("Du postest selbst", selbst.length,
           selbstFaellig.length ? selbstFaellig.length + " davon überfällig"
                                : "B-Roll und Storys") +
      tile("Läuft von selbst", laeuft.length, "eingeplant oder schon raus") +'''
NEU_KACHELN = '''      tile("Ist durch", laeuft.length,
           selbst.length ? selbst.length + " davon in deiner App"
                         : "eingeplant oder schon raus") +'''

ALT_AUFRUFE = '''    liste("Du postest selbst", selbstFaellig.length
      ? "B-Roll und Storys gehen nie \\u00fcber Blotato \\u2014 bei einem "
        + "Sieben-Sekunden-Clip ist die Musik der halbe Beitrag, und die "
        + "w\\u00e4hlst du nur in der App. " + selbstFaellig.length
        + " davon sind \\u00fcberf\\u00e4llig."
      : "Gehen nie \\u00fcber Blotato \\u2014 die Musik w\\u00e4hlst du in der App.",
      selbst, "du");

    liste("H\\u00e4ngt", "Freigegeben, aber der Zeitpunkt ist vorbei und nichts "
      + "r\\u00fcckt nach. Geht so nie raus \\u2014 nimm die Freigabe zur\\u00fcck "
      + "und gib sie neu, dann rutscht der Beitrag auf den n\\u00e4chsten Tag.",
      haengt, "du");

    liste("L\\u00e4uft von selbst", "Liegt bei Blotato oder ist schon raus. "
      + "Hier musst du nichts mehr tun.", laeuft, "ich");'''

NEU_AUFRUFE = '''    liste("H\\u00e4ngt", "Freigegeben, aber der Zeitpunkt ist vorbei und nichts "
      + "r\\u00fcckt nach. Geht so nie raus \\u2014 nimm die Freigabe zur\\u00fcck "
      + "und gib sie neu, dann rutscht der Beitrag auf den n\\u00e4chsten Tag.",
      haengt, "du");

    liste("Ist durch", selbst.length
      ? "Liegt bei Blotato oder ist schon raus. " + selbst.length + " davon hast "
        + "du selbst in der App eingeplant \\u2014 B-Roll und Storys gehen nie "
        + "\\u00fcber Blotato, weil die Musik nur dort w\\u00e4hlbar ist."
      : "Liegt bei Blotato oder ist schon raus. Hier musst du nichts mehr tun.",
      laeuft, "ich");'''

# Der Stand-Text in der Liste.
ALT_STAND = '''                  : s === "selber-posten" ? "B-Roll, wegen der Musik"'''
NEU_STAND = '''                  : s === "selber-posten" ? "in deiner App"'''


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
    if "selbstFormat" in s:
        print("  Schon eingebaut — nichts zu tun.")
        return

    s = setze(s, ANKER_FN, NEU_FN, "selbstFormat")
    s = setze(s, ALT_KNOPF, NEU_KNOPF, "Knopf")
    s = setze(s, ALT_TOAST, NEU_TOAST, "Meldung")
    s = setze(s, ALT_GRUPPEN, NEU_GRUPPEN, "Gruppen")
    s = setze(s, ALT_KACHELN, NEU_KACHELN, "Kacheln")
    s = setze(s, ALT_AUFRUFE, NEU_AUFRUFE, "Aufrufe")
    s = setze(s, ALT_STAND, NEU_STAND, "Stand-Text")

    # Gegenprobe: die falsche Behauptung darf nicht mehr stehen.
    # 🚨 Eng fassen. „überfällig" allein schlägt auf den Aufgaben-Reiter an,
    # wo das Wort völlig richtig steht — dieselbe Falle wie beim
    # Umlaut-Wächter und beim Download-Aufräumen: ein zu weites Muster fängt
    # zu viel, und nach dem dritten Fehlalarm liest niemand mehr hin.
    sichtbar = re.sub(r"//[^\n]*|/\*.*?\*/", "", s, flags=re.S)
    if "Du postest selbst" in sichtbar:
        sys.exit("🚨 «Du postest selbst» steht noch im sichtbaren Text.")
    if "selbstFaellig" in s:
        sys.exit("🚨 «selbstFaellig» wird noch benutzt — die Überfällig-"
                 "Behauptung wäre damit nicht weg.")

    fehler = js_pruefen(s)
    if fehler:
        sys.exit("🚨 node --check meldet einen Fehler — NICHTS geschrieben:\n  %s"
                 % fehler)
    if nur_pruefen:
        print("  Syntax in Ordnung. Mit --pruefen wird nicht geschrieben.")
        return

    datei.write_text(s, encoding="utf-8")
    print("  B-Roll gilt als erledigt · %d KB" % (len(s) / 1024))
    print("  Knopf heisst dort «In der App eingeplant», keine Überfällig-Warnung mehr.")


if __name__ == "__main__":
    main()
