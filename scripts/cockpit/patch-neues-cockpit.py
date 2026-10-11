"""Der optische Umbau — Logo, Kopfbild, Navigation nach Arbeitsschritt.

Patricia am 24.09.2026: *„mir gefällt das cockpit optisch nicht. und vieles
macht jetzt nicht soo viel sinn. z.B. die übersicht."*

🚨 **Sie hatte bei der Übersicht recht, und der Grund war schlimmer als Optik.**
Die Startseite zählte `state.posts` (5 Einträge) und `state.ideen` (6) — beides
Überbleibsel aus der allerersten Fassung, die nie gepflegt wurden. Sie zeigte
ein «40/35/25-Verhältnis», das es nicht mehr gibt, dazu eine
«Archetypen-Abdeckung» ohne Daten. **Die Startseite rechnete mit Leichen.**
Deshalb wird sie hier nicht verschönert, sondern auf die Daten umgestellt, die
wirklich leben.

🚨 **Navigation nach Arbeitsschritt, nicht nach Werkzeug** (Patricias Entscheid):
Planen → Bauen → Freigeben → Ausgewertet. Vorher lagen Content-Studio,
Story-Studio und Reel-Studio nebeneinander, obwohl man dort dasselbe tut —
bauen. Und «Wochen-Vorschau», «Fertig zum Posten» und «Gepostet & Analyse»
waren drei Reiter für drei Zustände desselben Beitrags.

🚨 **Zwei Reiter fallen weg: «Content-Planung» und «Ideen & Hooks».** Sie haben
5 und 6 Einträge aus der Anfangszeit. Die Dokumente bleiben in der Datenbank —
nur aus der Leiste verschwinden sie. Ein Reiter, der nichts zeigt, kostet bei
jedem Blick eine halbe Sekunde.

🚨 **Das Logo wird als Datei eingebunden, nicht als Code eingebettet.** Die SVG
bringt eigene CSS-Klassen (`.cls-1` …) mit; inline im Dokument könnten die mit
der Seite kollidieren. Als `<img src>` ist sie in sich geschlossen.

    python scripts/cockpit/patch-neues-cockpit.py [--pruefen] [--datei <pfad>]
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

# ------------------------------------------------------------------ 1 · CSS

CSS_ANKER = "  .brandmark { padding: 0 8px; }"

CSS_NEU = r"""  /* ---------- Marke, Kopfbild, Luft (24.09.2026) ---------- */
  .brandmark { padding: 4px 8px 2px; }
  .brandmark .bm-logo { display: block; width: 100%; max-width: 176px; height: auto; }
  .brandmark .bm-sub {
    font-size: 10px; letter-spacing: 0.18em; text-transform: uppercase;
    color: var(--ink-soft); margin-top: 8px; padding-left: 2px;
  }
  /* Das Kopfbild traegt die Startseite. Patricia sitzt links im Bild,
     rechts ist Wasser - deshalb steht der Text rechts und das Bild wird
     linksbuendig beschnitten. */
  .hero {
    position: relative; border-radius: 16px; overflow: hidden;
    min-height: 210px; display: flex; align-items: flex-end;
    margin-bottom: 26px; box-shadow: var(--shadow);
    background: var(--surface-2);
  }
  .hero-bild {
    position: absolute; inset: 0;
    background-image: url("assets/s07.jpg");
    background-size: cover; background-position: 50% 28%;
  }
  .hero-schleier {
    position: absolute; inset: 0;
    background: linear-gradient(100deg,
      rgba(12,28,48,0.00) 0%, rgba(12,28,48,0.10) 34%,
      rgba(12,28,48,0.62) 62%, rgba(12,28,48,0.80) 100%);
  }
  .hero-text { position: relative; padding: 26px 30px; margin-left: auto; max-width: 62%; color: #fff; }
  .hero-gruss { font-size: 12px; letter-spacing: 0.16em; text-transform: uppercase; opacity: 0.85; margin: 0 0 6px; }
  .hero-text h1 { font-family: var(--display); font-size: 30px; line-height: 1.12; margin: 0 0 8px; color: #fff; }
  .hero-sub { margin: 0; font-size: 14px; line-height: 1.5; opacity: 0.92; max-width: 46ch; }
  @media (max-width: 760px) {
    .hero { min-height: 260px; }
    .hero-text { max-width: 100%; padding: 20px; }
    .hero-schleier { background: linear-gradient(180deg,
      rgba(12,28,48,0.05) 0%, rgba(12,28,48,0.30) 40%, rgba(12,28,48,0.84) 100%); }
    .hero-text h1 { font-size: 24px; }
  }
  /* Mehr Luft in der Leiste, damit die Gruppen als Gruppen lesbar sind. */
  .navgroup { padding: 18px 10px 5px; }
  .navbtn { padding-top: 9px; padding-bottom: 9px; }
  .navsub { padding-left: 26px; font-size: 13px; }
  .navsub::before {
    content: ""; position: absolute; left: 14px; top: 50%;
    width: 5px; height: 5px; margin-top: -2px; border-radius: 50%;
    background: var(--line-strong);
  }
  .navbtn { position: relative; }
  /* Die grossen Zahlen auf der Startseite duerfen atmen. */
  .hero + .tiles .t-num { font-size: 30px; }
  .jetzt { display: grid; gap: 14px; grid-template-columns: repeat(auto-fit, minmax(270px, 1fr)); margin-bottom: 24px; }
  .jetzt .karte { background: var(--surface); border: 1px solid var(--line); border-radius: var(--r); padding: 16px 18px; }
  .jetzt .karte h3 { margin: 0 0 10px; font-size: 13px; letter-spacing: 0.06em; text-transform: uppercase; color: var(--ink-soft); }
  .jetzt .zeile { display: flex; gap: 10px; align-items: baseline; padding: 5px 0; border-bottom: 1px solid var(--line); }
  .jetzt .zeile:last-child { border-bottom: 0; }
  .jetzt .zeile .wann { font-size: 12px; color: var(--ink-soft); min-width: 52px; font-variant-numeric: tabular-nums; }
  .jetzt .leer { color: var(--ink-soft); font-size: 13px; }
"""

# -------------------------------------------------------------- 2 · Marke

MARKE_ALT = """    <div class="brandmark">
      <div class="bm-name">Mum&nbsp;Life&nbsp;Balance</div>
      <div class="bm-sub">Cockpit</div>
    </div>"""

MARKE_NEU = """    <div class="brandmark">
      <img class="bm-logo" src="assets/logo.svg" alt="Mum Life Balance">
      <div class="bm-sub">Cockpit</div>
    </div>"""

# --------------------------------------------------------------- 3 · TABS

TABS_ALT_ANFANG = '  var TABS = ['
TABS_ALT_ENDE = '    { id: "suche", label: "Suchen" }\n  ];'

TABS_NEU = '''  /* Nach Arbeitsschritt sortiert, nicht nach Werkzeug (Patricia, 24.09.2026).
     Planen -> Bauen -> Freigeben -> Ausgewertet ist der Weg, den ein Beitrag
     nimmt; vorher lagen die drei Studios nebeneinander, obwohl man dort
     dasselbe tut. Die Reiter "Content-Planung" (state.posts) und
     "Ideen & Hooks" (state.ideen) sind raus - 5 und 6 Eintraege aus der
     Anfangszeit. Die Daten bleiben, nur die Leiste wird kuerzer. */
  var TABS = [
    { id: "uebersicht", label: "Heute" },
    { g: "Content" },
    { id: "woche", label: "Planen" },
    { id: "studio", label: "Bauen" },
    { id: "storys", label: "Storys", sub: true },
    { id: "reels", label: "Reels", sub: true },
    { id: "fertig", label: "Freigeben" },
    { id: "gepostet", label: "Ausgewertet" },
    { id: "ideenkasten", label: "Ideenkasten" },
    { g: "Planung" },
    { id: "launches", label: "Jahresplan" },
    { id: "monatsbogen", label: "Monatsbogen" },
    { id: "wochenbogen", label: "Wochenbogen" },
    { id: "aufgaben", label: "Aufgaben" },
    { id: "ziele", label: "Ziele" },
    { g: "Geschäft" },
    { id: "links", label: "Links & Material" },
    { id: "katalog", label: "Angebots-Katalog" },
    { id: "produkte", label: "Meine Notizen", sub: true },
    { id: "funnel", label: "Funnel & Keywords" },
    { id: "mailings", label: "Listen & Automationen" },
    { id: "leads", label: "Kundinnen & Leads" },
    { id: "zahlen", label: "Zahlen & Ziele" },
    { g: "doTERRA" },
    { id: "rangtracker", label: "Rang-Tracker" },
    { id: "team", label: "Team", sub: true },
    { g: "Nachschlagen" },
    { id: "kurse", label: "Kurs-Inhalte" },
    { id: "wissen", label: "Mein Wissen" },
    { id: "suche", label: "Suchen" }
  ];'''

# ------------------------------------------------------- 4 · Nav-Unterpunkt

NAV_ALT = '''      var b = document.createElement("button");
      b.className = "navbtn";'''
NAV_NEU = '''      var b = document.createElement("button");
      b.className = t.sub ? "navbtn navsub" : "navbtn";'''


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
    if "hero-schleier" in s:
        print("  Schon umgebaut — nichts zu tun.")
        return

    s = setze(s, CSS_ANKER, CSS_NEU.rstrip("\n"), "CSS-Anker")
    s = setze(s, MARKE_ALT, MARKE_NEU, "Markenzeichen")
    s = setze(s, NAV_ALT, NAV_NEU, "Nav-Knopf")

    # TABS als Ganzes ersetzen
    a = s.find(TABS_ALT_ANFANG)
    b = s.find(TABS_ALT_ENDE)
    if a < 0 or b < 0:
        sys.exit("🚨 TABS-Block nicht gefunden.")
    s = s[:a] + TABS_NEU + s[b + len(TABS_ALT_ENDE):]

    fehler = js_pruefen(s)
    if fehler:
        sys.exit("🚨 node --check meldet einen Fehler — NICHTS geschrieben:\n  %s"
                 % fehler)
    if nur_pruefen:
        print("  Syntax in Ordnung. Mit --pruefen wird nicht geschrieben.")
        return

    datei.write_text(s, encoding="utf-8")
    print("  Umbau in %s · %d KB" % (datei.name, len(s) / 1024))
    print("  Leiste: 27 Reiter → 24, nach Arbeitsschritt gruppiert.")
    print("  ⚠️ Die Übersicht selbst wird im zweiten Schritt ersetzt.")


if __name__ == "__main__":
    main()
