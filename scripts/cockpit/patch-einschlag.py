"""Hebt Beitraege heraus, die eingeschlagen sind — und sagt, was daraus wird.

Patricia am 24.09.2026: *„da müssen wir aber irgend einen mechanismus einbauen
mit beiträgen, die mega performt haben."*

🚨 **Ein Einschlag ist kein Recycling-Fall.** Im Archiv lagen zwei Beitraege mit
1'328 und 892 Reichweite bei einem Median von 170 — das 7.8- und 5.2-Fache.
Danach kommt ein Sprung auf 2.4x. So etwas in derselben Liste wie „lief
ordentlich" zu fuehren, heisst es zu verlieren.

🚨 **Und die 28-Tage-Sperre gilt hier NICHT.** Sie schuetzt davor, denselben
Beitrag zu frueh nochmal zu posten. Einen Gedanken in einem anderen Format neu
zu bauen ist kein Wiederholen — darauf muss niemand vier Wochen warten.

🚨 **Reichweite und Reaktion sind zwei verschiedene Funde.** Beide Einschlaege
hatten eine Rate von 0.45 %, also weit unterdurchschnittlich: viele Fremde haben
es gesehen, wenige reagiert. Daraus folgt etwas anderes als aus einem Beitrag,
auf den die eigenen Leute antworten. Wer beides gleich behandelt, gibt fuer
beide den falschen Rat.

Aufruf:
  python scripts/cockpit/patch-einschlag.py [--pruefen]
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
SEITE = ROOT / "outputs" / "cockpit" / "mlb-cockpit.html"

ALT_FUNK = "  function gpRecyclingBlock(liste) {"
NEU_FUNK = '''  /* Was aus einem Einschlag wird — je nachdem, WAS eingeschlagen ist. */
  var EINSCHLAG_RAT = {
    reichweite: {
      titel: "Reichweite",
      satz: "Viele Fremde haben das gesehen. Der Hook zieht Leute an, die dich " +
            "noch nicht kennen.",
      was: ["Denselben Gedanken als zweites Format bauen — lief es als Reel, " +
            "nimm ein Karussell.",
            "Eine Serie daraus machen: derselbe Aufhänger, andere Szene.",
            "Wenn du eine Anzeige testen willst, ist das dein bester Kandidat — " +
            "er hat organisch bewiesen, dass er zieht."]
    },
    reaktion: {
      titel: "Reaktion",
      satz: "Deine eigenen Leute haben geantwortet. Das Thema trifft die, die " +
            "dir schon folgen.",
      was: ["Daraus einen Lead-Post bauen: derselbe Gedanke, diesmal mit " +
            "Keyword-CTA.",
            "In der Story nachfassen und fragen, was genau sie daran kennen.",
            "Als Mail an die Liste — wer hier reagiert, liest auch dort."]
    },
    beides: {
      titel: "Reichweite und Reaktion",
      satz: "Selten. Viele Fremde haben es gesehen UND deine Leute haben " +
            "reagiert.",
      was: ["Nimm ihn als Vorlage — Aufbau, Länge, Tonfall.",
            "Zweites Format bauen und als Lead-Post mit Keyword ausspielen.",
            "Für eine Anzeige der beste Kandidat, den du hast."]
    }
  };

  function gpEinschlagBlock(liste) {
    var treffer = liste.filter(function (b) {
      return b.einschlag && !(gepostetNotizen[b.id] || {}).ausgewertet;
    }).sort(function (x, y) { return (y.faktor || 0) - (x.faktor || 0); });
    if (!treffer.length) return null;

    var box = document.createElement("div");
    box.className = "panel gpein";
    box.style.marginBottom = "18px";
    box.innerHTML = "<h2>Das hier ist eingeschlagen <span class=\\"gpzahl orange\\">" +
      treffer.length + "</span></h2>" +
      '<p class="note">Weit über deinem Schnitt. Hier lohnt sich mehr als ' +
      'nochmal posten — und darauf musst du keine vier Wochen warten, solange ' +
      'du es neu baust statt zu wiederholen.</p>';

    treffer.slice(0, 5).forEach(function (b) {
      var rat = EINSCHLAG_RAT[b.einschlag_art] || EINSCHLAG_RAT.reichweite;
      var k = document.createElement("div");
      k.className = "gpeinkarte";
      var h =
        '<div class="gpeinkopf">' +
          '<span class="gpfaktor">' + (b.faktor || "?") + '×</span>' +
          '<span class="gpeinart">' + esc(rat.titel) + '</span>' +
          '<span class="gpdatum">' + esc(b.datum) + ' · vor ' +
            b.alter_tage + ' Tagen</span>' +
          '<span class="gpreach">' + (b.reach || 0).toLocaleString("de-CH") +
            ' Reichweite</span>' +
        '</div>' +
        '<p class="gpeintext">' + esc(b.hook || b.anfang || "") + '</p>' +
        '<p class="note">' + esc(rat.satz) + '</p>' +
        '<ul class="gpeinliste">' +
          rat.was.map(function (w) { return "<li>" + esc(w) + "</li>"; }).join("") +
        '</ul>';
      k.innerHTML = h;

      var leiste = document.createElement("div");
      leiste.className = "gpeinknoepfe";

      var a = document.createElement("button");
      a.className = "btn primary";
      a.textContent = "Daraus mehr machen";
      a.onclick = function () {
        state.ideen.unshift({
          id: uid("i"),
          typ: "Einschlag",
          saeule: (gepostetNotizen[b.id] || {}).saeule || SAEULEN[0],
          text: (b.hook || b.anfang || "").slice(0, 200),
          quelle: "schlug am " + b.datum + " ein (" + b.reach + " Reichweite, " +
                  b.faktor + "× dein Median) — " + rat.was[0],
          status: "Offen"
        });
        saveList("ideen");
        a.disabled = true;
        a.textContent = "in der Ideenliste";
        toast("In den Ideenvorrat gelegt, mit dem Vorschlag dabei.");
      };
      leiste.appendChild(a);

      if (b.link) {
        var l = document.createElement("a");
        l.className = "btn";
        l.href = b.link; l.target = "_blank"; l.rel = "noopener";
        l.textContent = "Beitrag ansehen";
        leiste.appendChild(l);
      }

      // 🚨 Kein Loeschen, sondern „abgehakt". Der Beitrag bleibt im Archiv —
      // nur aus dieser Liste verschwindet er, damit sie nicht jeden Tag
      // dieselben zwei sieht.
      var w = document.createElement("button");
      w.className = "btn ghost";
      w.textContent = "Hab ich ausgewertet";
      w.onclick = function () {
        if (!gepostetNotizen[b.id]) gepostetNotizen[b.id] = {};
        gepostetNotizen[b.id].ausgewertet = todayISO();
        notizSpeichern();
        render();
      };
      leiste.appendChild(w);

      k.appendChild(leiste);
      box.appendChild(k);
    });
    return box;
  }

  function gpRecyclingBlock(liste) {'''

ALT_EIN = '''    var recBox = gpRecyclingBlock(liste);'''
NEU_EIN = '''    var einBox = gpEinschlagBlock(liste);
    var recBox = gpRecyclingBlock(liste);'''

ALT_EIN2 = '''    listenPanel.parentNode.insertBefore(recBox, listenPanel);'''
NEU_EIN2 = '''    listenPanel.parentNode.insertBefore(recBox, listenPanel);
    if (einBox) listenPanel.parentNode.insertBefore(einBox, recBox);'''

ALT_KACHEL = '''      tile("Kann wieder raus",'''
NEU_KACHEL = '''      tile("Eingeschlagen",
           liste.filter(function (b) {
             return b.einschlag && !(gepostetNotizen[b.id] || {}).ausgewertet;
           }).length,
           "weit über deinem Schnitt") +
      tile("Kann wieder raus",'''

ALT_CSS = "  .gprec { border-left: 3px solid var(--teal); }"
NEU_CSS = """  .gpein { border-left: 3px solid var(--orange); }
  .gpzahl.orange { background: var(--orange); }
  .gpeinkarte { border-top: 1px solid var(--line); padding: 12px 0 4px; }
  .gpein .gpeinkarte:first-of-type { border-top: 0; }
  .gpeinkopf { display: flex; align-items: baseline; gap: 12px; flex-wrap: wrap; }
  .gpfaktor {
    font-family: var(--display); font-size: 21px; color: var(--orange);
    font-variant-numeric: tabular-nums;
  }
  .gpeinart {
    font-size: 10px; letter-spacing: 0.08em; text-transform: uppercase;
    color: var(--orange); background: var(--orange-soft);
    padding: 2px 9px; border-radius: 999px;
  }
  .gpeinkopf .gpreach { margin-left: auto; font-size: 13px; color: var(--ink-soft); }
  .gpeintext {
    font-family: var(--display); font-size: 16px; line-height: 1.35;
    margin: 7px 0 4px;
  }
  .gpeinliste { margin: 6px 0 0; padding-left: 19px; font-size: 13px; line-height: 1.6; }
  .gpeinliste li { margin-bottom: 2px; }
  .gpeinknoepfe { display: flex; gap: 8px; flex-wrap: wrap; margin: 11px 0 4px; }
  .gpeinknoepfe .btn { font-size: 12px; padding: 6px 12px; }
  .gprec { border-left: 3px solid var(--teal); }"""

ERSETZUNGEN = [
    ("Block und Ratschläge", ALT_FUNK, NEU_FUNK),
    ("Block bauen", ALT_EIN, NEU_EIN),
    ("Block einhängen", ALT_EIN2, NEU_EIN2),
    ("Kachel", ALT_KACHEL, NEU_KACHEL),
    ("Aussehen", ALT_CSS, NEU_CSS),
]


def node_pruefen(html):
    bloecke = re.findall(r"<script>(.*?)</script>", html, re.S)
    if not bloecke:
        return "kein <script>-Block gefunden"
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False,
                                     encoding="utf-8") as f:
        f.write(max(bloecke, key=len))
        pfad = f.name
    try:
        r = subprocess.run(["node", "--check", pfad], capture_output=True, text=True)
        return "" if r.returncode == 0 else (r.stderr or "").strip()[:600]
    except FileNotFoundError:
        return ""
    finally:
        Path(pfad).unlink(missing_ok=True)


def main():
    nur_pruefen = "--pruefen" in sys.argv
    html = SEITE.read_text(encoding="utf-8")
    vorher = len(html)

    if "function gpEinschlagBlock" in html:
        sys.exit("Der Einschlag-Block ist schon drin — nichts zu tun.")
    if "function gpRecyclingBlock" not in html:
        sys.exit("ABBRUCH — erst `patch-recycling.py` laufen lassen.")

    for name, alt, neu in ERSETZUNGEN:
        n = html.count(alt)
        if n == 0:
            sys.exit("ABBRUCH — Fundstelle fehlt: %s" % name)
        if n > 1:
            sys.exit("ABBRUCH — Fundstelle %dx vorhanden: %s" % (n, name))
        html = html.replace(alt, neu)
        print("  %-22s ersetzt" % name)

    fehler = node_pruefen(html)
    if fehler:
        sys.exit("ABBRUCH — Node meldet einen Syntaxfehler:\n%s" % fehler)
    print("\n  Node --check: in Ordnung")

    if nur_pruefen:
        print("\nPROBELAUF — nichts geschrieben.")
        return
    SEITE.write_text(html, encoding="utf-8")
    print("\nGeschrieben: %s  (%d -> %d Zeichen)" % (SEITE, vorher, len(html)))


if __name__ == "__main__":
    main()
