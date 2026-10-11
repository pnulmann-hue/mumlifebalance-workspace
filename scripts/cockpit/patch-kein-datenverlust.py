"""Der Datenbank-Stand überschreibt die eigene Arbeit nicht mehr.

Patricia am 24.09.2026: *„wenn ich mal aus dem cockpit fliege, ist alles was ich
gemacht habe wieder weg"*.

🚨 **Zwei Fehler greifen ineinander, und zusammen löschen sie Arbeit.**

**1 · Der Abgleich beim Laden war bedingungslos:**

```js
if (seen[st.id]) Object.assign(seen[st.id], st);   // DB gewinnt — immer
```

Der Stand aus der Datenbank wird über den lokalen gelegt, **ohne zu prüfen,
welcher neuer ist**. Steht in der Datenbank eine ältere Fassung, ist die
neuere weg. Dasselbe Muster an allen drei Stellen: `storys`, `reels`,
`karussells`.

**2 · `lsSet` stand INNERHALB der 700-ms-Verzögerung.** Die lokale Sicherung
wartete also genauso lang wie das Schreiben in die Datenbank. Wer in diesem
Fenster die Seite verliert, hat nichts — weder lokal noch entfernt. Und beim
nächsten Öffnen kommt über Fehler 1 der alte Stand zurück.

**Der Ablauf, der Arbeit kostet:** tippen → wegklicken vor Ablauf der 700 ms →
neu öffnen → der alte Datenbank-Stand überschreibt das lokal Getippte. Beide
Fehler einzeln wären harmlos; zusammen sind sie ein Reisswolf.

**Was sich ändert:**

| | |
|---|---|
| `lsSet` | läuft **sofort**, nicht mehr verzögert — `localStorage` ist synchron und billig |
| Zusammenführen | nur, wenn der Datenbank-Stand **neuer** ist (`updatedAt`) |
| Vor dem Schliessen | `pagehide` und `visibilitychange` sichern alles Ausstehende |

🚨 **Nur das Schreiben in die Datenbank bleibt verzögert.** Das ist der teure
Teil, und 700 ms Sammeln sind dort richtig. Die lokale Sicherung zu verzögern
war nie ein Gewinn.

🚨 **Fehlt `updatedAt` auf einer Seite, gewinnt der lokale Stand.** Wer im
Zweifel die Datenbank gewinnen lässt, verliert Arbeit — und Arbeit
zurückzubekommen ist unmöglich, einen veralteten Anzeigestand zu erneuern
dagegen ein Klick.

    python scripts/cockpit/patch-kein-datenverlust.py [--pruefen] [--datei <pfad>]
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

# ------------------------------------------- 1 · Helfer: neuer gewinnt

ANKER = '''  function saveStory(st) {'''

HELFER = '''  /* 🚨 Der Stand aus der Datenbank darf die eigene Arbeit nur dann
     ueberschreiben, wenn er NEUER ist. Bis 24.09.2026 gewann er immer, und
     zusammen mit der verzoegerten lokalen Sicherung hat das Arbeit geloescht.
     Siehe Kopf von patch-kein-datenverlust.py.

     Fehlt updatedAt, gewinnt der lokale Stand: Arbeit zurueckzubekommen ist
     unmoeglich, einen veralteten Anzeigestand zu erneuern ein Klick. */
  function dbUebernehmen(lokal, ausDb) {
    if (!lokal) return ausDb;
    var a = lokal.updatedAt || "", b = ausDb.updatedAt || "";
    if (!b || b <= a) return lokal;          // lokal ist gleich alt oder neuer
    Object.assign(lokal, ausDb);
    return lokal;
  }

  /* Was noch nicht in der Datenbank ist. Wird vor dem Schliessen abgearbeitet. */
  var ausstehend = {};
  function sofortSichern() {
    Object.keys(ausstehend).forEach(function (k) {
      try { ausstehend[k](); } catch (e) {}
    });
    ausstehend = {};
  }
  window.addEventListener("pagehide", sofortSichern);
  document.addEventListener("visibilitychange", function () {
    if (document.visibilityState === "hidden") sofortSichern();
  });

  function saveStory(st) {'''

# ------------------------- 2 · lsSet sofort, DB verzoegert (drei Funktionen)

SAVES = [
    # (Name, alter Block, neuer Block)
    ("saveStory", '''    clearTimeout(saveTimers["st-" + st.id]);
    saveTimers["st-" + st.id] = setTimeout(function () {
      st.updatedAt = new Date().toISOString();
      lsSet("st-" + st.id, st);
      lsSet("storyliste", state.storys.map(function (x) { return x.id; }));
      if (!db) { setSaveState("lokal gespeichert", "off"); return; }''',
     '''    // 🚨 Lokal SOFORT — nur die Datenbank wird gesammelt.
    st.updatedAt = new Date().toISOString();
    lsSet("st-" + st.id, st);
    lsSet("storyliste", state.storys.map(function (x) { return x.id; }));
    clearTimeout(saveTimers["st-" + st.id]);
    saveTimers["st-" + st.id] = setTimeout(function () {
      delete ausstehend["st-" + st.id];
      if (!db) { setSaveState("lokal gespeichert", "off"); return; }'''),

    ("saveCarousel", '''    clearTimeout(saveTimers["kar-" + car.id]);
    saveTimers["kar-" + car.id] = setTimeout(function () {
      car.updatedAt = new Date().toISOString();
      lsSet("kar-" + car.id, car);
      lsSet("karliste", state.karussells.map(function (c) { return c.id; }));
      if (!db) { setSaveState("lokal gespeichert", "off"); return; }''',
     '''    car.updatedAt = new Date().toISOString();
    lsSet("kar-" + car.id, car);
    lsSet("karliste", state.karussells.map(function (c) { return c.id; }));
    clearTimeout(saveTimers["kar-" + car.id]);
    saveTimers["kar-" + car.id] = setTimeout(function () {
      delete ausstehend["kar-" + car.id];
      if (!db) { setSaveState("lokal gespeichert", "off"); return; }'''),

    ("saveReel", '''    clearTimeout(saveTimers["rl-" + r.id]);
    saveTimers["rl-" + r.id] = setTimeout(function () {
      r.updatedAt = new Date().toISOString();
      lsSet("rl-" + r.id, r);
      lsSet("reelliste", state.reels.map(function (x) { return x.id; }));
      if (!db) { setSaveState("lokal gespeichert", "off"); return; }''',
     '''    r.updatedAt = new Date().toISOString();
    lsSet("rl-" + r.id, r);
    lsSet("reelliste", state.reels.map(function (x) { return x.id; }));
    clearTimeout(saveTimers["rl-" + r.id]);
    saveTimers["rl-" + r.id] = setTimeout(function () {
      delete ausstehend["rl-" + r.id];
      if (!db) { setSaveState("lokal gespeichert", "off"); return; }'''),
]

# ------------------------------- 3 · Zusammenfuehren beim Laden

MERGES = [
    ("Storys", "if (seen[st.id]) Object.assign(seen[st.id], st); else state.storys.push(st);",
     "if (seen[st.id]) dbUebernehmen(seen[st.id], st); else state.storys.push(st);"),
    ("Reels", "if (seen[rl.id]) Object.assign(seen[rl.id], rl); else state.reels.push(rl);",
     "if (seen[rl.id]) dbUebernehmen(seen[rl.id], rl); else state.reels.push(rl);"),
]

# --------------------------------- 4 · Story-Felder vervollstaendigen

ALT_STORY_SAVE = '''        name: st.name, brand: st.brand, phase: st.phase || "", frames: st.frames,
        datum: st.datum || "", profil: st.profil || "",'''
NEU_STORY_SAVE = '''        name: st.name, brand: st.brand, phase: st.phase || "", frames: st.frames,
        datum: st.datum || "", profil: st.profil || "",
        // 🚨 Was hier fehlt, ist nach dem naechsten Speichern WEG. `blotato`
        // fehlte bis 24.09. als einziges der drei Formate.
        blotato: st.blotato || null,'''

ALT_STORY_LOAD = '''          var st = { id: doc.id, name: d0.name || "Sequenz", brand: d0.brand || "mlb_dark", handle: d0.handle || "", phase: d0.phase || "", frames: d0.frames, datum: d0.datum || "", textfrei: !!d0.textfrei, updatedAt: d0.updatedAt || "" };'''
NEU_STORY_LOAD = '''          // 🚨 Die Leseliste muss so lang sein wie die Schreibliste, sonst
          // kommen Felder nie an. profil, kommentar*, abgelehnt* und blotato
          // fehlten hier bis 24.09.2026.
          var st = { id: doc.id, name: d0.name || "Sequenz", brand: d0.brand || "mlb_dark", handle: d0.handle || "", phase: d0.phase || "", frames: d0.frames, datum: d0.datum || "", textfrei: !!d0.textfrei, profil: d0.profil || "", kommentar: d0.kommentar || "", kommentarStand: d0.kommentarStand || "", kommentarErledigt: d0.kommentarErledigt || "", kommentarAntwort: d0.kommentarAntwort || "", abgelehnt: !!d0.abgelehnt, abgelehntStand: d0.abgelehntStand || "", blotato: d0.blotato || null, updatedAt: d0.updatedAt || "" };'''


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
    if "dbUebernehmen" in s:
        print("  Schon eingebaut — nichts zu tun.")
        return

    s = setze(s, ANKER, HELFER, "Helfer")
    for name, alt, neu in SAVES:
        s = setze(s, alt, neu, name)
    for name, alt, neu in MERGES:
        s = setze(s, alt, neu, "Merge " + name)
    s = setze(s, ALT_STORY_SAVE, NEU_STORY_SAVE, "Story-Felder schreiben")
    s = setze(s, ALT_STORY_LOAD, NEU_STORY_LOAD, "Story-Felder lesen")

    # 🚨 Gegenprobe: kein bedingungsloses Object.assign mehr beim Laden.
    rest = len(re.findall(r"if \(seen\[\w+\.id\]\) Object\.assign", s))
    if rest:
        sys.exit("🚨 Es gibt noch %d bedingungslose Object.assign beim Laden." % rest)

    fehler = js_pruefen(s)
    if fehler:
        sys.exit("🚨 node --check meldet einen Fehler — NICHTS geschrieben:\n  %s"
                 % fehler)
    if nur_pruefen:
        print("  Syntax in Ordnung. Mit --pruefen wird nicht geschrieben.")
        return

    datei.write_text(s, encoding="utf-8")
    print("  Datenverlust behoben · %d KB" % (len(s) / 1024))
    print("  Lokal sofort · neuer Stand gewinnt · pagehide sichert Ausstehendes.")


if __name__ == "__main__":
    main()
