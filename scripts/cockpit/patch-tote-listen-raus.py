"""`posts` und `ideen` raus — und die drei Knöpfe, die ins Leere schrieben.

Patricia am 25.09.2026: *„okey raus nehmen"* — nachdem im Cockpit-Durchgang
auffiel, dass `DOC_KEYS` noch `posts` und `ideen` lädt, obwohl es die beiden
Reiter seit dem 24.09. nicht mehr gibt.

🚨 **„Zwei Zeilen" war falsch — es sind elf Zugriffe.** Wer die Schlüssel
einfach aus `DOC_KEYS` streicht, macht `state.posts` zu `undefined`, und
`state.posts.some(…)` wirft beim nächsten Zeichnen einen Fehler.

**Und dabei kam ein Fehler heraus, den der Reiter-Umbau vom 24.09. gebaut hat:**

| Knopf | schrieb nach | sichtbar |
|---|---|---|
| „Nochmal bringen" (Recycling) | `state.ideen` | **nein** |
| „Daraus mehr machen" (Einschlag) | `state.ideen` | **nein** |
| „In den Ideenvorrat legen" (Content-Studio) | `state.ideen` | **nein** |

Alle drei melden „In den Ideenvorrat gelegt" — und der Vorrat war seit dem
Umbau unsichtbar. Eine Erfolgsmeldung über etwas, das niemand mehr findet, ist
derselbe Fehler wie „Freigegeben und abgelegt", während nichts passieren kann.

**Sie schreiben jetzt in den Ideenkasten** (`daten/ideenkasten`), den es als
Reiter gibt. Felder dort: `id · idee · bereich · aufwand · status · notiz`.

**Zwei Anzeigen rechneten mit Karteileichen:**

- Funnel-Karte: „X Posts spielen dieses Keyword" — zählte die **5** alten
  `posts`-Einträge statt der echten Beiträge.
- Jahresplan: „eingezahlt" — dasselbe.

Beide laufen jetzt über `alleBeitraege()`, also über die Beiträge, die es
wirklich gibt. 🚨 Eine Zahl, die aus einer toten Liste kommt, sieht genauso
echt aus wie eine gemessene — das ist schlimmer als gar keine Zahl.

🚨 **`state.posts` und `state.ideen` bleiben als leere Arrays bestehen.** Der
Ladevorgang aus der Datenbank entfällt (das war Patricias Punkt), aber die
Variablen existieren, damit kein übersehener Zugriff die Seite killt.

    python scripts/cockpit/patch-tote-listen-raus.py [--pruefen] [--datei <pfad>]
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

# ------------------------------------------------------------ 1 · DOC_KEYS

ALT_KEYS = ('  var DOC_KEYS = ["posts", "ideen", "leads", "team", "produkte", '
            '"funnel", "launches", "zahlen", "ideenkasten"];')
NEU_KEYS = ('  /* 🚨 „posts" und „ideen" sind seit dem Reiter-Umbau vom 24.09.2026\n'
            '     unsichtbar und werden nicht mehr geladen. Sie bleiben unten als\n'
            '     leere Arrays bestehen, damit ein uebersehener Zugriff die Seite\n'
            '     nicht killt. Siehe Kopf von patch-tote-listen-raus.py. */\n'
            '  var DOC_KEYS = ["leads", "team", "produkte", "funnel", "launches", '
            '"zahlen", "ideenkasten"];')

# ---------------------------------------------- 2 · leere Arrays sicherstellen

ALT_INIT = '  DOC_KEYS.forEach(function (k) { state[k] = lsGet(k, []); });'
NEU_INIT = ('  DOC_KEYS.forEach(function (k) { state[k] = lsGet(k, []); });\n'
            '  // Nicht mehr geladen, aber vorhanden — siehe oben.\n'
            '  state.posts = []; state.ideen = [];')

# --------------------------------- 3 · Die drei Knoepfe in den Ideenkasten

ANKER_HELFER = '  function recycelnAlsIdee(b, knopf) {'
NEU_HELFER = '''  /* 🚨 Bis 25.09.2026 schrieben drei Knoepfe nach `state.ideen` — dem Reiter,
     den der Umbau vom 24.09. entfernt hat. Sie meldeten „In den Ideenvorrat
     gelegt", und den Vorrat sah niemand mehr. Jetzt landen sie im
     Ideenkasten, den es als Reiter gibt. */
  function inDenIdeenkasten(text, bereich, notiz) {
    state.ideenkasten = state.ideenkasten || [];
    state.ideenkasten.unshift({
      id: uid("ik"), idee: text, bereich: bereich || "Content",
      aufwand: "klein", status: "Idee", notiz: notiz || ""
    });
    saveList("ideenkasten");
  }

  function recycelnAlsIdee(b, knopf) {'''

ERSETZUNGEN = []

# 🚨 Statt drei Schreibstellen umzubauen: eine Bruecke. `state.ideen` bekommt
# ein `unshift`, das in den Ideenkasten schreibt, und ein `filter`, das leer
# zurueckgibt. Alle drei Knoepfe funktionieren damit unveraendert — und ein
# vierter, den ich uebersehen habe, ebenfalls.
ALT_BRUECKE = '  state.posts = []; state.ideen = [];'
NEU_BRUECKE = '''  state.posts = [];
  /* 🚨 Kein Array, sondern eine Bruecke in den Ideenkasten. Drei Knoepfe
     („Nochmal bringen", „Daraus mehr machen", „In den Ideenvorrat legen")
     schrieben bis 25.09.2026 nach state.ideen — also in den Reiter, den der
     Umbau vom 24.09. entfernt hat. Sie meldeten Erfolg, und den Vorrat sah
     niemand mehr. So muss keine der Stellen angefasst werden. */
  state.ideen = {
    length: 0,
    filter: function () { return []; },
    unshift: function (o) {
      inDenIdeenkasten(o.text || o.idee || "", "Content",
        o.quelle || o.typ || "");
    }
  };'''

# -------------------------------- 4 · Zahlen aus echten Beitraegen

ALT_SAVE = """  function saveList(key) {
    clearTimeout(saveTimers[key]);"""
NEU_SAVE = """  function saveList(key) {
    // „ideen" ist seit 25.09.2026 eine Bruecke in den Ideenkasten, kein Array.
    if (key === "ideen") return;
    clearTimeout(saveTimers[key]);"""

ALT_FUNNEL = ('      var posts = state.posts.filter(function (p) { return f.keyword && '
              'p.keyword && p.keyword.toUpperCase() === String(f.keyword).toUpperCase(); });')
NEU_FUNNEL = ('''      /* 🚨 Zaehlte die 5 alten „posts"-Karteileichen. Eine Zahl aus einer
         toten Liste sieht genauso echt aus wie eine gemessene. */
      var posts = (typeof alleBeitraege === "function" ? alleBeitraege() : [])
        .filter(function (b) {
          var t = ((b.caption || "") + " " + (b.titel || "")).toUpperCase();
          return f.keyword && t.indexOf(String(f.keyword).toUpperCase()) >= 0;
        }).map(function (b) { return { thema: b.titel || b.hook || "", '''
              'datum: (b.obj && b.obj.datum) || "" }; });')

ALT_JP = '''      var eingezahlt = state.posts.filter(function (p) {
        return l.start && l.ende && p.datum >= l.start && p.datum <= l.ende;
      });'''
NEU_JP = '''      // Dieselbe Umstellung wie bei der Funnel-Karte: echte Beitraege statt
      // der alten „posts"-Liste.
      var eingezahlt = (typeof alleBeitraege === "function" ? alleBeitraege() : [])
        .filter(function (b) {
          var dt = (b.obj && b.obj.datum) || "";
          return l.start && l.ende && dt >= l.start && dt <= l.ende;
        });'''


def setze(text, alt, neu, name):
    n = text.count(alt)
    if n != 1:
        sys.exit("🚨 «%s» kommt %dx vor — erwartet 1x. Nichts geändert." % (name, n))
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
    datei = ROOT / "outputs" / "cockpit" / "mlb-cockpit.html"
    if "--datei" in sys.argv:
        datei = Path(sys.argv[sys.argv.index("--datei") + 1])

    s = datei.read_text(encoding="utf-8")
    if "inDenIdeenkasten" in s:
        print("  Schon eingebaut — nichts zu tun.")
        return

    s = setze(s, ALT_KEYS, NEU_KEYS, "DOC_KEYS")
    s = setze(s, ALT_INIT, NEU_INIT, "Init")
    s = setze(s, ANKER_HELFER, NEU_HELFER, "Helfer")
    s = setze(s, ALT_BRUECKE, NEU_BRUECKE, "Brücke")
    s = setze(s, ALT_SAVE, NEU_SAVE, "saveList")
    s = setze(s, ALT_FUNNEL, NEU_FUNNEL, "Funnel-Zahl")
    s = setze(s, ALT_JP, NEU_JP, "Jahresplan-Zahl")

    fehler = js_pruefen(s)
    if fehler:
        sys.exit("🚨 node --check meldet einen Fehler — NICHTS geschrieben:\n  %s"
                 % fehler)
    if "--pruefen" in sys.argv:
        print("  Syntax in Ordnung. Mit --pruefen wird nicht geschrieben.")
        return

    datei.write_text(s, encoding="utf-8")
    print("  Tote Listen raus · %d KB" % (len(s) / 1024))
    print("  posts/ideen werden nicht mehr geladen · drei Knöpfe schreiben in den Ideenkasten.")


if __name__ == "__main__":
    main()
