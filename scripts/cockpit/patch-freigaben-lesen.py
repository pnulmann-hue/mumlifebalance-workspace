"""Das Cockpit liest endlich seine eigene Freigabe-Sammlung.

🚨 **Sieben Schreibstellen, null Lesestellen** (gefunden 24.09.2026, nachdem
Patricia fragte: *„dienstagkarussells gingen nicht raus?"*).

Die Freigabe schreibt nach `freigaben/<id>` — mit `status`, `blotatoId`,
`eingeplantAm`, `datum`, `zeit`. **Das Cockpit hat diese Sammlung nie gelesen.**
Angezeigt wurde stattdessen `beitrag.blotato.status`, und den aktualisiert
niemand. Deshalb stand auf der Karte weiter „wartet", während in `freigaben`
längst `geplant` mit Blotato-Kennung lag.

**Der belegte Fall:** `kw39-kar-di-a` — am Beitrag `blotato: {status:"wartet"}`,
in `freigaben` `status:"geplant"`, `eingeplantAm: 2026-09-19T20:12`. Der Beitrag
**ist am 22.09. rausgegangen** (54 Reichweite, Caption stimmt wörtlich mit dem
Instagram-Abzug überein). Im Cockpit sah er aus wie liegengeblieben.

🚨 **Zwei Orte für denselben Zustand sind immer ein Fehler** — dieselbe Lehre
wie beim gestrichenen Tagesplan. `freigaben` ist die Wahrheit, weil der
Einplan-Task dort hineinschreibt. `blotato` am Beitrag bleibt nur als Rückfall,
wenn die Sammlung nicht geladen ist.

**Was der Patch tut:**

| | |
|---|---|
| lädt `freigaben` beim Start | einmal, in `freigaben` (Objekt id → Dokument), mit `localStorage`-Rückfall |
| `istDraussen(b)` | liest jetzt den echten Status, nicht mehr `blotato` |
| `tpStand(b)` | sagt „Ist raus", „Eingeplant" oder „Postest du selbst" statt nur „Freigegeben" |
| „Was wann rausgeht" | **Datumsfeld je Zeile** und **Klick auf den Hook** springt zur Karte |

Patricia dazu: *„bei der übersicht was wann rausgeht brauche ich auch die
verlinkung zum beitrag. dann könnte ich neue daten setzen."* Beides ist drin —
das Feld für den schnellen Weg, der Klick, wenn sie den ganzen Beitrag sehen
will.

    python scripts/cockpit/patch-freigaben-lesen.py [--pruefen] [--datei <pfad>]
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

# ------------------------------------------- 1 · istDraussen auf freigaben

ALT_FN = '''  var DRAUSSEN = ["geplant", "gepostet-von-hand", "selber-posten"];
  function istDraussen(b) {
    var o = (b.obj || b), bl = o.blotato || {};
    return DRAUSSEN.indexOf(bl.status) >= 0;
  }
  function draussenGrund(b) {
    var bl = ((b.obj || b).blotato) || {};
    return bl.status === "geplant" ? "bei Blotato eingeplant"
      : bl.status === "gepostet-von-hand" ? "von dir gepostet"
      : bl.status === "selber-posten" ? "B-Roll — postest du selbst"
      : "";
  }'''

NEU_FN = '''  var DRAUSSEN = ["geplant", "gepostet-von-hand", "selber-posten"];

  /* 🚨 Die Wahrheit steht in der Sammlung „freigaben", nicht am Beitrag.
     Dort schreibt der Einplan-Task hinein; `beitrag.blotato` aktualisiert
     niemand. Siehe Kopf von patch-freigaben-lesen.py. */
  var freigaben = {};

  function freigabeVon(b) {
    var id = (b && b.id) || "";
    return (id && freigaben[id]) || null;
  }
  function draussenStatus(b) {
    var f = freigabeVon(b);
    if (f && f.status) return f.status;
    // Rueckfall, solange die Sammlung nicht geladen ist.
    return (((b.obj || b).blotato) || {}).status || "";
  }
  function istDraussen(b) {
    return DRAUSSEN.indexOf(draussenStatus(b)) >= 0;
  }
  function draussenGrund(b) {
    var s = draussenStatus(b);
    return s === "geplant" ? "bei Blotato eingeplant"
      : s === "gepostet-von-hand" ? "von dir gepostet"
      : s === "selber-posten" ? "B-Roll — postest du selbst"
      : "";
  }'''

# ------------------------------------------------------- 2 · tpStand ehrlich

ALT_STAND = '''  function tpStand(b) {
    if (b.obj.textfrei) return { text: "Freigegeben", art: "gut" };'''

NEU_STAND = '''  function tpStand(b) {
    // Was draussen ist, zuerst - „Freigegeben" sagt nichts darueber, ob es
    // auch wirklich rausging.
    if (istDraussen(b)) {
      var s = draussenStatus(b);
      return { text: s === "geplant" ? "Eingeplant"
                   : s === "gepostet-von-hand" ? "Ist raus"
                   : "Postest du selbst", art: "gut" };
    }
    if (zeitpunktVorbei(b) && b.obj.textfrei)
      return { text: "Freigegeben, Zeitpunkt durch", art: "warn" };
    if (b.obj.textfrei) return { text: "Freigegeben", art: "gut" };'''

# ------------------------------- 3 · Termin-Zeile: Datumsfeld und Sprung

ALT_ZEILE = '''          '<span class="uehook">' + esc(b.hook || b.titel) + '</span>' +
          '<span class="tp-stand ' + s.art + '">' + esc(s.text) + '</span>';
        plan.appendChild(z);'''

NEU_ZEILE = '''          '<span class="uehook klickbar" title="Beitrag öffnen">' +
            esc(b.hook || b.titel) + '</span>' +
          '<span class="tp-stand ' + s.art + '">' + esc(s.text) + '</span>' +
          '<input type="date" class="uedat" value="' + esc(b.obj.datum || "") + '" ' +
            'title="Anderes Datum setzen">';
        // Patricia, 24.09.2026: „brauche ich auch die verlinkung zum beitrag.
        // dann könnte ich neue daten setzen." Beides - das Feld fuer den
        // schnellen Weg, der Klick fuer den ganzen Beitrag.
        z.querySelector(".uehook").onclick = function () {
          if (typeof springeZuBeitrag === "function") springeZuBeitrag(b);
        };
        z.querySelector(".uedat").onchange = function () {
          if (this.value) umplanen(b, this.value);
        };
        plan.appendChild(z);'''

# ---------------------------------------------------------- 4 · Laden

ALT_LADE = '      db.collection("reels").limit(60).get().then(function (qs) {'
NEU_LADE = '''      /* Die Freigabe-Sammlung - bis 24.09.2026 wurde sie nur beschrieben. */
      db.collection("freigaben").limit(300).get().then(function (qs) {
        var m = {};
        qs.docs.forEach(function (doc) { m[doc.id] = doc.data() || {}; });
        freigaben = m;
        lsSet("freigaben", m);
        render();
      }).catch(function () {});
      db.collection("reels").limit(60).get().then(function (qs) {'''

ALT_INIT = '  DOC_KEYS.forEach(function (k) { state[k] = lsGet(k, []); });'
NEU_INIT = '''  DOC_KEYS.forEach(function (k) { state[k] = lsGet(k, []); });
  freigaben = lsGet("freigaben", {}) || {};'''

# ------------------------------------------------------------------ 5 · CSS

ALT_CSS = "  .wslot.durch { opacity: 0.62; }"
NEU_CSS = '''  .uehook.klickbar { cursor: pointer; }
  .uehook.klickbar:hover { text-decoration: underline; color: var(--teal); }
  .uezeile .uedat { font-size: 12px; padding: 2px 4px; }
  .wslot.durch { opacity: 0.62; }'''


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
    if "freigabeVon" in s:
        print("  Schon eingebaut — nichts zu tun.")
        return

    s = setze(s, ALT_FN, NEU_FN, "istDraussen")
    s = setze(s, ALT_STAND, NEU_STAND, "tpStand")
    s = setze(s, ALT_ZEILE, NEU_ZEILE, "Termin-Zeile")
    s = setze(s, ALT_LADE, NEU_LADE, "Ladestelle")
    s = setze(s, ALT_INIT, NEU_INIT, "Init")
    s = setze(s, ALT_CSS, NEU_CSS, "CSS")

    fehler = js_pruefen(s)
    if fehler:
        sys.exit("🚨 node --check meldet einen Fehler — NICHTS geschrieben:\n  %s"
                 % fehler)
    if nur_pruefen:
        print("  Syntax in Ordnung. Mit --pruefen wird nicht geschrieben.")
        return

    datei.write_text(s, encoding="utf-8")
    print("  freigaben wird gelesen · %d KB" % (len(s) / 1024))
    print("  Stand kommt aus der Sammlung · Termine klickbar · Datumsfeld je Zeile.")


if __name__ == "__main__":
    main()
