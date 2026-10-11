"""
Zeigt einen Kurs-Link (z.B. die Startklar-Werkstatt) in der Kurs-Karte an.

Das Cockpit rendert bisher nur Name, Lektionszahl und die Zahl der Lektionen
ohne Transkript. Ein Kurs kann aber ein Mitmach-Heft oder eine Kursplattform
haben, und genau die sucht Patricia im Alltag.

Neu ist das Feld `links` am Kurs:
    "links": [{"titel": "Werkstatt", "url": "https://..."}]

Es wird als Zeile unter dem Kursnamen ausgegeben, sobald die Karte offen ist.
Kurse ohne das Feld sehen unveraendert aus.

Aufruf:
  python scripts/cockpit/patch-kurs-werkstattlink.py
"""
import pathlib
import subprocess
import sys
import tempfile

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = pathlib.Path(__file__).resolve().parents[2]
SEITE = ROOT / "outputs" / "cockpit" / "mlb-cockpit.html"

ANKER = """        if (offenerKurs === k.name) {
          var koerper = karte.querySelector(".dkoerper");"""

NEU = """        if (offenerKurs === k.name) {
          var koerper = karte.querySelector(".dkoerper");
          // Links zum Kurs (Mitmach-Heft, Kursplattform) - nur wenn gepflegt
          if (k.links && k.links.length) {
            var lz = document.createElement("div");
            lz.className = "kurslinks";
            lz.innerHTML = k.links.map(function (v) {
              return '<a href="' + esc(v.url) + '" target="_blank" rel="noopener">'
                   + esc(v.titel || v.url) + '</a>';
            }).join(" · ");
            koerper.appendChild(lz);
          }"""

STIL_ANKER = "      raus.innerHTML = \"\";\n      kurse.kurse.forEach(function (k) {"


def main():
    text = SEITE.read_text(encoding="utf-8")

    if "kurslinks" in text:
        print("Schon gesetzt - nichts zu tun.")
        return

    if ANKER not in text:
        print("FEHLER: Anker nicht gefunden. Die Seite hat sich geaendert -")
        print("erst nachsehen, wo die Kurs-Karte gerendert wird.")
        sys.exit(1)

    text = text.replace(ANKER, NEU, 1)

    # Stil dazu, direkt vor dem schliessenden </style> des ersten Blocks
    stil = ("    .kurslinks{margin:0 0 10px;font-size:14px}\n"
            "    .kurslinks a{color:var(--petrol,#12828c);text-decoration:none;font-weight:600}\n"
            "    .kurslinks a:hover{text-decoration:underline}\n")
    i = text.find("</style>")
    if i == -1:
        print("FEHLER: kein </style> gefunden.")
        sys.exit(1)
    text = text[:i] + stil + text[i:]

    # 🚨 Vor dem Schreiben pruefen, ob das eingebettete Skript noch laeuft.
    # Ein deutsches Anfuehrungszeichen in einer JS-Zeichenkette hat hier schon
    # einmal die ganze Seite totgelegt.
    js = []
    rest = text
    while True:
        a = rest.find("<script")
        if a == -1:
            break
        a = rest.find(">", a) + 1
        b = rest.find("</script>", a)
        if b == -1:
            break
        js.append(rest[a:b])
        rest = rest[b + 9:]
    tmp = pathlib.Path(tempfile.gettempdir()) / "cockpit-pruefung.js"
    tmp.write_text("\n;\n".join(js), encoding="utf-8")
    pruef = subprocess.run(["node", "--check", str(tmp)], capture_output=True, text=True)
    if pruef.returncode != 0:
        print("FEHLER: das eingebettete Skript ist nach dem Patch kaputt:")
        print(pruef.stderr[:800])
        print("Die Seite wurde NICHT geaendert.")
        sys.exit(1)

    SEITE.write_text(text, encoding="utf-8")
    print("Gesetzt. node --check ist gruen.")
    print("Kurse mit einem Feld `links` zeigen die Zeile jetzt an.")


if __name__ == "__main__":
    main()
