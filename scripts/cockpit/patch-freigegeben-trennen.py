"""„Schon freigegeben" war drei verschiedene Dinge in einem Topf.

Patricia am 24.09.2026: *„also unter freigegeben ist alles, wo ich nichts mehr
tun muss?"* — **Nein.** Und das war an der Liste nicht zu sehen.

**Was in den 16 Einträgen wirklich steckte** (live aus `freigaben` gelesen):

| Status | Anzahl | wer ist dran |
|---|---:|---|
| `geplant` | 12 | **niemand** — liegt bei Blotato, geht von selbst raus |
| `selber-posten` | 6 | **Patricia** — B-Roll, sie postet selbst wegen der Musik |
| `wartet`, Termin vorbei | 1 | **niemand** — hängt, geht nie mehr raus |
| `gepostet-von-hand` | 1 | erledigt |

🚨 **Vier der sechs B-Rolls hatten einen Termin, der schon vorbei war** — 21.09.
und 23.09. Sie standen unter „freigegeben", sahen erledigt aus und warteten in
Wirklichkeit auf sie. Das ist derselbe Fehlertyp wie „Datum ist durch": ein
Zustand, der nach *fertig* aussieht und keiner ist.

🚨 **`reel-kw38-mo` steht seit dem 18.09. auf `wartet`.** Der Termin ist vorbei,
Blotato nimmt nichts in der Vergangenheit — der Beitrag geht nie mehr raus, und
niemand hat es gemerkt. Er bekommt eine eigene Gruppe, weil er weder läuft noch
auf jemanden wartet.

**Drei Gruppen statt einer:**

| Gruppe | Inhalt |
|---|---|
| **Du postest selbst** | B-Roll und Storys · überfällige zuerst, rot markiert |
| **Hängt** | freigegeben, aber der Termin ist vorbei und nichts rückt nach |
| **Läuft von selbst** | bei Blotato eingeplant oder schon gepostet |

🚨 **Der Status kommt aus `draussenStatus(b)`**, also aus der Sammlung
`freigaben` — nicht mehr aus `b.obj.blotato`. Die alte Liste las `blotato`, und
das war der Grund, warum dort „wartet auf 20:00" stand, während der Beitrag
längst eingeplant war.

    python scripts/cockpit/patch-freigegeben-trennen.py [--pruefen] [--datei <pfad>]
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

# ---------------------------------------------------------- 1 · Kacheln

ALT_KACHEL = '''      tile("Schon freigegeben", frei.length, "wartet auf den nächsten Lauf") +'''
NEU_KACHEL = '''      tile("Du postest selbst", selbst.length,
           selbstFaellig.length ? selbstFaellig.length + " davon überfällig"
                                : "B-Roll und Storys") +
      tile("Läuft von selbst", laeuft.length, "eingeplant oder schon raus") +'''

# ------------------------------------------------- 2 · Gruppen berechnen

ALT_BERECHNUNG = '''    var frei = alle.filter(function (b) { return b.obj.textfrei; }).sort(nachDatum);'''
NEU_BERECHNUNG = '''    var frei = alle.filter(function (b) { return b.obj.textfrei; }).sort(nachDatum);

    /* 🚨 „Freigegeben" war drei verschiedene Dinge in einem Topf. Siehe Kopf
       von patch-freigegeben-trennen.py. Der Status kommt aus der Sammlung
       „freigaben", nicht aus b.obj.blotato — das war der alte Lesefehler. */
    var heuteISO = todayISO();
    function selbstSache(b) {
      return b.art === "storys" || draussenStatus(b) === "selber-posten";
    }
    var selbst = frei.filter(selbstSache);
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

# ------------------------------------------------------- 3 · Die Liste

ALT_LISTE = '''    // Freigegebenes nur als Liste — die vollen Karten braucht hier niemand mehr.
    if (frei.length) {
      var kopf = document.createElement("div");
      kopf.className = "wt-kopf";
      kopf.innerHTML = '<span class="wt-name">Schon freigegeben</span>' +
                       '<span class="wt-datum">' + frei.length + '</span>';
      box.appendChild(kopf);
      var panel = document.createElement("div");
      panel.className = "panel tuliste";
      var h = "";
      frei.forEach(function (b) {
        var bl = b.obj.blotato || {};
        var stand = bl.status === "gepostet-von-hand" ? "selbst gepostet"
                  : bl.status === "selber-posten" ? "postest du selbst (Musik)"
                  : bl.status === "geplant" ? "eingeplant"
                  : bl.status === "zeitpunkt-vorbei" ? "Zeitpunkt vorbei"
                  : b.art === "storys" ? "Story \\u2014 postest du selbst"
                  : "wartet auf 20:00";
        h += '<div class="tuzeile">' +
          '<span class="tudatum">' +
            (b.obj.datum ? esc(tagName(b.obj.datum).slice(0, 2) + " " +
                               fmtDate(b.obj.datum)) : "ohne Datum") +
            (bl.zeit ? " " + esc(bl.zeit) : "") + '</span>' +
          '<span class="tuwas"><strong>' + esc(b.titel) + '</strong> <span>\\u00b7 ' +
            esc(kartenProfil(b.obj) === "doterra" ? "doTERRA" : "Mentoring") +
            '</span></span>' +
          '<span class="tuwer ' +
            (stand === "wartet auf 20:00" || stand === "eingeplant" ? "ich" : "du") +
            '">' + esc(stand) + '</span>' +
          '</div>';
      });
      panel.innerHTML = h;
      box.appendChild(panel);
    }
  }'''

NEU_LISTE = '''    /* Drei Gruppen statt einer — wer dran ist, steht im Titel. */
    function liste(titel, unter, eintraege, wer) {
      if (!eintraege.length) return;
      var kopf = document.createElement("div");
      kopf.className = "wt-kopf";
      kopf.innerHTML = '<span class="wt-name">' + esc(titel) + '</span>' +
                       '<span class="wt-datum">' + eintraege.length + '</span>';
      box.appendChild(kopf);
      if (unter) {
        var n = document.createElement("p");
        n.className = "note";
        n.style.margin = "0 0 10px";
        n.textContent = unter;
        box.appendChild(n);
      }
      var panel = document.createElement("div");
      panel.className = "panel tuliste";
      var h = "";
      eintraege.forEach(function (b) {
        var s = draussenStatus(b);
        var zeit = (freigabeVon(b) || {}).zeit ||
                   (b.obj.blotato && b.obj.blotato.zeit) || "";
        var spaet = b.obj.datum && b.obj.datum <= heuteISO;
        var stand = s === "gepostet-von-hand" ? "selbst gepostet"
                  : s === "geplant" ? "eingeplant"
                  : b.art === "storys" ? "Story"
                  : s === "selber-posten" ? "B-Roll, wegen der Musik"
                  : "wartet";
        h += '<div class="tuzeile">' +
          '<span class="tudatum">' +
            (b.obj.datum ? esc(tagName(b.obj.datum).slice(0, 2) + " " +
                               fmtDate(b.obj.datum)) : "ohne Datum") +
            (zeit ? " " + esc(zeit) : "") + '</span>' +
          '<span class="tuwas"><strong>' + esc(b.titel) + '</strong> <span>\\u00b7 ' +
            esc(kartenProfil(b.obj) === "doterra" ? "doTERRA" : "Mentoring") +
            '</span></span>' +
          '<span class="tuwer ' + wer + '">' +
            esc(wer === "du" && spaet ? stand + " \\u2014 \\u00fcberf\\u00e4llig" : stand) +
          '</span></div>';
      });
      panel.innerHTML = h;
      box.appendChild(panel);
    }

    liste("Du postest selbst", selbstFaellig.length
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
      + "Hier musst du nichts mehr tun.", laeuft, "ich");
  }'''


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
    if "selbstFaellig" in s:
        print("  Schon getrennt — nichts zu tun.")
        return

    s = setze(s, ALT_BERECHNUNG, NEU_BERECHNUNG, "Berechnung")
    s = setze(s, ALT_KACHEL, NEU_KACHEL, "Kacheln")
    s = setze(s, ALT_LISTE, NEU_LISTE, "Liste")

    # Gegenprobe: die alte Sammelgruppe darf nicht mehr im sichtbaren Text stehen.
    sichtbar = re.sub(r"//[^\n]*|/\*.*?\*/", "", s, flags=re.S)
    if "Schon freigegeben" in sichtbar:
        sys.exit("🚨 „Schon freigegeben“ steht noch im sichtbaren Text.")

    fehler = js_pruefen(s)
    if fehler:
        sys.exit("🚨 node --check meldet einen Fehler — NICHTS geschrieben:\n  %s"
                 % fehler)
    if nur_pruefen:
        print("  Syntax in Ordnung. Mit --pruefen wird nicht geschrieben.")
        return

    datei.write_text(s, encoding="utf-8")
    print("  Freigegeben getrennt · %d KB" % (len(s) / 1024))
    print("  Du postest selbst · Hängt · Läuft von selbst.")


if __name__ == "__main__":
    main()
