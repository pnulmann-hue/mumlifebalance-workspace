"""Der Bild-Editor verliert die Arbeit nicht mehr, wenn die Seite zugeht.

Patricia am 25.09.2026: *„wenn ich am story bearbeiten bin im bild-editor, dass
die story dann rausfliegt wenn ich rausgehe aus dem bild-editor. und dann muss
ich sie neu generieren und wieder von vorne anfangen"*.

🚨 **Der Bild-Editor speicherte gar nichts.** Null Vorkommen von `localStorage`
in der ganzen Seite. Die Folien leben ausschliesslich in der Variablen `folien`;
Seite zu, alles weg. Anders als im Cockpit war das kein Wettlauf zweier
Speicherwege — es gab schlicht keinen.

**Was gesichert wird:** `folien` (die ganze Abfolge mit allen Textbloecken),
`fmt` (Story · Reel-Cover · Karussell) und `aktiv` (welche Folie offen war).
Mehr braucht es nicht, `state` zeigt ohnehin auf `folien[aktiv]`.

**Wann:** bei jedem `render()` — das läuft nach jeder Änderung ohnehin. Und noch
einmal auf `pagehide`, für den Fall, dass die letzte Tastatureingabe kein
Neuzeichnen ausgelöst hat.

🚨 **Hochgeladene Fotos und Videos sind `data:`-URLs und sprengen den Speicher.**
`localStorage` fasst rund 5 MB; ein einziges Handyfoto als Text ist schnell
2 MB. Deshalb werden `photo`, `videoUrl` und `poster` **nur gesichert, wenn sie
auf eine Datei zeigen** (`assets/…`), nicht als eingebettete Daten. Ein
selbst hochgeladenes Bild muss nach dem Neuladen neu gewählt werden — **der
Text, die Blöcke, die Farben und die ganze Abfolge sind aber da.** Das ist der
Unterschied zwischen „zwei Klicks" und „von vorne anfangen".

🚨 **Wenn der Speicher trotzdem voll ist, sagt die Seite es.** Ein stiller
Fehlschlag wäre schlimmer als keiner: sie würde weiterarbeiten im Glauben, es
sei gesichert. Deshalb eine sichtbare Zeile statt eines Konsolen-Eintrags.

🚨 **Ein Wiederherstellen-Hinweis beim Öffnen, kein stilles Einsetzen.** Wer
den Editor mit einer neuen Idee aufmacht und die alte Abfolge vorfindet, hält
das für einen Fehler. Deshalb: Stand laden, oben eine Zeile „zuletzt
bearbeitet …" mit Knopf **Neu anfangen**.

    python scripts/cockpit/patch-editor-speichert.py [--pruefen]
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
DATEI = ROOT / "outputs" / "_bild-editor" / "index.html"

# ------------------------------------------------ 1 · Sichern und Laden

ALT_STATE = '''  let aktiv = 0;
  let state = folien[0];'''

NEU_STATE = '''  let aktiv = 0;
  let state = folien[0];

  /* ---------- Die Arbeit ueberlebt das Schliessen ----------
     🚨 Bis 25.09.2026 speicherte diese Seite NICHTS. Die Folien lagen nur in
     der Variablen oben; Seite zu, alles weg. Siehe Kopf von
     patch-editor-speichert.py. */
  const SPEICHER = "mlb-editor:stand";

  /* Eingebettete Bilder und Videos sprengen den Speicher (rund 5 MB gesamt,
     ein Handyfoto als Text schon 2 MB). Nur Verweise auf Dateien werden
     gesichert — der Text bleibt in jedem Fall erhalten. */
  function ohneGrossdaten(f) {
    const k = JSON.parse(JSON.stringify(f));
    if ((k.photo || "").startsWith("data:")) k.photo = "lounge.jpg";
    if ((k.videoUrl || "").startsWith("data:") || (k.videoUrl || "").startsWith("blob:")) {
      k.videoUrl = ""; k.videoName = ""; if (k.mode === "video") k.mode = "foto";
    }
    if ((k.poster || "").startsWith("data:")) k.poster = "";
    return k;
  }

  let speicherWarnung = false;
  function standSichern() {
    try {
      localStorage.setItem(SPEICHER, JSON.stringify({
        fmt: fmt, aktiv: aktiv, stand: new Date().toISOString(),
        folien: folien.map(ohneGrossdaten)
      }));
    } catch (e) {
      // 🚨 Ein stiller Fehlschlag waere schlimmer als keiner — sie wuerde
      // weiterarbeiten im Glauben, es sei gesichert.
      if (!speicherWarnung) {
        speicherWarnung = true;
        const w = document.createElement("div");
        w.style.cssText = "position:fixed;left:50%;bottom:18px;transform:translateX(-50%);"
          + "background:#8a2b1c;color:#fff;padding:10px 16px;border-radius:999px;"
          + "font-size:13px;z-index:99;box-shadow:0 4px 18px rgba(0,0,0,.3)";
        w.textContent = "Speicher voll — dein Stand wird gerade NICHT gesichert. "
          + "Lad die fertigen Bilder herunter, bevor du die Seite schliesst.";
        document.body.appendChild(w);
      }
    }
  }
  window.addEventListener("pagehide", standSichern);

  function standLaden() {
    let d = null;
    try { d = JSON.parse(localStorage.getItem(SPEICHER) || "null"); } catch (e) {}
    if (!d || !Array.isArray(d.folien) || !d.folien.length) return;
    folien = d.folien;
    fmt = d.fmt || "story";
    aktiv = Math.min(d.aktiv || 0, folien.length - 1);
    state = folien[aktiv];

    /* 🚨 Nicht stillschweigend einsetzen. Wer mit einer neuen Idee aufmacht
       und die alte Abfolge vorfindet, haelt das fuer einen Fehler. */
    const wann = d.stand ? new Date(d.stand) : null;
    const txt = wann
      ? wann.toLocaleDateString("de-CH", { day: "numeric", month: "long" })
        + " um " + wann.toLocaleTimeString("de-CH", { hour: "2-digit", minute: "2-digit" })
      : "zuletzt";
    const b = document.createElement("div");
    b.style.cssText = "position:fixed;left:50%;top:10px;transform:translateX(-50%);"
      + "background:#1E3A4C;color:#f1ecdd;padding:9px 16px;border-radius:999px;"
      + "font-size:13px;z-index:99;display:flex;gap:12px;align-items:center;"
      + "box-shadow:0 4px 18px rgba(0,0,0,.28)";
    b.innerHTML = "<span>Weiter bei deinem Stand von " + txt + " \\u00b7 "
      + folien.length + " Folien</span>";
    const n = document.createElement("button");
    n.textContent = "Neu anfangen";
    n.style.cssText = "background:none;border:1px solid rgba(241,236,221,.5);"
      + "color:inherit;border-radius:999px;padding:4px 12px;font:inherit;"
      + "font-size:12px;cursor:pointer";
    n.onclick = function () {
      folien = [neueFolie()]; aktiv = 0; state = folien[0];
      try { localStorage.removeItem(SPEICHER); } catch (e) {}
      b.remove(); render(); streifen();
    };
    b.appendChild(n);
    const weg = document.createElement("button");
    weg.textContent = "\\u2715";
    weg.style.cssText = n.style.cssText + ";border:0;padding:4px 6px";
    weg.onclick = function () { b.remove(); };
    b.appendChild(weg);
    document.body.appendChild(b);
  }'''

# ------------------------------------------------------- 2 · render sichert

ALT_RENDER = '''    fit();
    miniFuellen(aktiv);
    auftragZeigen();
    requestAnimationFrame(pruefeZonen);
  }'''

NEU_RENDER = '''    fit();
    miniFuellen(aktiv);
    auftragZeigen();
    standSichern();          // laeuft nach jeder Aenderung ohnehin
    requestAnimationFrame(pruefeZonen);
  }'''


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
    s = DATEI.read_text(encoding="utf-8")
    if "standSichern" in s:
        print("  Schon eingebaut — nichts zu tun.")
        return

    for name, alt, neu in (("Zustand", ALT_STATE, NEU_STATE),
                           ("render", ALT_RENDER, NEU_RENDER)):
        if s.count(alt) != 1:
            sys.exit("🚨 «%s» kommt %dx vor — erwartet 1x." % (name, s.count(alt)))
        s = s.replace(alt, neu, 1)

    # standLaden() muss NACH der ersten Zeichnung laufen, sonst fehlen die
    # Bedienelemente. Der letzte render()-Aufruf beim Start ist die Stelle.
    treffer = list(re.finditer(r"\n  render\(\);\s*\n", s))
    if not treffer:
        sys.exit("🚨 Kein Start-Aufruf von render() gefunden.")
    letzter = treffer[-1]
    s = (s[:letzter.end()]
         + "  standLaden();\n  if (typeof streifen === \"function\") streifen();\n"
         + s[letzter.end():])

    fehler = js_pruefen(s)
    if fehler:
        sys.exit("🚨 node --check meldet einen Fehler — NICHTS geschrieben:\n  %s"
                 % fehler)
    if "--pruefen" in sys.argv:
        print("  Syntax in Ordnung. Mit --pruefen wird nicht geschrieben.")
        return

    DATEI.write_text(s, encoding="utf-8")
    print("  Bild-Editor speichert · %d KB" % (len(s) / 1024))
    print("  Folien + Format + offene Folie · Hinweis beim Öffnen · Knopf „Neu anfangen“.")


if __name__ == "__main__":
    main()
