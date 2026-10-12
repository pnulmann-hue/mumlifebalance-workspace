#!/usr/bin/env python3
"""Die acht B-Rolls fuer 13.-16.10.2026 (KW42 Rest) — Feed Mi + Fr je A/B und Trial Reels T1-T4.

Hooks aus outputs/content/KW42/hooks.md (Fassung 3, Tresor-Formeln). Stil wechselt
Marker -> Serif (context/videoschnitt-animationen.md, „Abwechslung ist Pflicht").
Beim Marker wechselt der Balken Orange -> Petrol -> Dunkelblau. Serif bleibt Orange:
Dunkelblau und Petrol als Schriftfarbe auf dem Clip fallen im Kontrast-Check durch (1,5-1,9:1).

Schritt 1: Konzept (Standbilder) fuer alle:   python scripts/content/kw42-brolls.py
Schritt 2: nach Sichtpruefung rendern:        python scripts/content/kw42-brolls.py --rendern [name ...]

Was ueber broll-bauen.py hinaus dazukommt (Patricia 11.10.: „B-Roll will ich animiert
haben"): Stil und Akzent je Reel, ein Aufruf am Schluss (`zusatz`, erst in den letzten
2,6 s) und bei der Verlosung drei Schritte, die nacheinander mit Pop aufgehen.
"""
import json
import pathlib
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
WURZEL = pathlib.Path(__file__).resolve().parents[2]
BAUEN = WURZEL / "scripts" / "content" / "broll-bauen.py"
TEXTEBENE = WURZEL / "scripts" / "videoschnitt" / "textebene.py"
AUS = WURZEL / "video" / "output" / "broll"

REELS = [
    dict(name="kw42-m-mi-a", clip="20260521_104709", ab=0.1, dauer=6.0, hoehe=52,
         stil="marker", akzent="orange",
         text="Das Peinliche? Ich war felsenfest überzeugt, dass die KI meine Texte schreibt.",
         betont="Umgeschrieben hab ich sie trotzdem jedes Mal.",
         zusatz="Kommentier STIMME"),
    dict(name="kw42-m-mi-b", clip="20260911_092813", ab=1.0, dauer=7.0, hoehe=52,
         stil="serif", akzent="orange",
         text="POV: Du öffnest ChatGPT motiviert",
         betont="und schliesst es 20 Minuten später mit einem Text, der klingt wie ein Prospekt.",
         zusatz="Kommentier STIMME"),
    dict(name="kw42-m-fr-a", clip="20260417_160229", ab=1.0, dauer=7.5, hoehe=50,
         stil="serif", akzent="orange",
         text="Unangenehme Wahrheit: Ich verdiene mit meinem Business noch weniger als früher im Büro.",
         betont="Und mein Mann macht trotzdem keinen Spruch mehr.",
         zusatz="Schick das einer Network-Freundin"),
    dict(name="kw42-m-fr-b", clip="20260727_135234", ab=2.0, dauer=7.0, hoehe=22,
         stil="marker", akzent="petrol",
         text="POV: Du hoffst heimlich, dass dich beim Familienessen niemand fragt,",
         betont="wie es mit deinem Network läuft.",
         zusatz="Schick das einer Network-Freundin"),
    dict(name="kw42-t1-di", clip="20260417_150517", ab=1.0, dauer=7.0, hoehe=50,
         stil="serif", akzent="orange",  # 12.10.: Marker-Balken war schief und zu tief

         text="Bei mir bekommst du keine Ausreden mehr für deinen Stillstand im Network.",
         betont="Wir finden den Weg raus oder wir lassen es.",
         zusatz="Folg mir, wenn du etwas Eigenes willst"),
    dict(name="kw42-t2-mi-verlosung", clip="20260522_180654", ab=1.0, dauer=9.0, hoehe=27, cta_y=50,
         stil="serif", akzent="orange",
         text="Ich verlose einen Platz in meinem KI-Kurs.",
         betont="So bist du dabei:",
         zusatz="Ziehung Do 22.10. · Regeln in der Caption",
         schritte=["1 · Folg mir",
                   "2 · Kommentier: Was soll dir die KI abnehmen?",
                   "3 · Teil das Reel mit einer Network-Freundin"]),
    dict(name="kw42-t3-do", clip="20260506_133307", ab=1.0, dauer=7.0, hoehe=50,
         stil="serif", akzent="orange",  # 12.10.: zweiter Teil im Balken zu gross, wie Fr-A

         text="Du brauchst nicht noch mehr Tipps fürs Network.",
         betont="Du musst aufhören, das meiste von dem zu machen, was dich nur Zeit kostet.",
         zusatz="Folg mir, wenn du etwas Eigenes willst"),
    dict(name="kw42-t4-fr", clip="20251008_150145", ab=1.0, dauer=7.0, hoehe=50,
         stil="serif", akzent="orange",
         text="Ich bin nicht diejenige, die dir fürs Network",
         betont="das nächste Wundermittel verspricht.",
         zusatz="Folg mir, wenn du etwas Eigenes willst"),
]


def lauf(befehl):
    print("  $", " ".join(str(b) for b in befehl)[:160])
    subprocess.run([str(b) for b in befehl], check=True)


def bauen(r, rendern):
    ordner = AUS / r["name"]
    # Schritt 1: Clip schneiden + finish.json (Konzept) ueber das bestehende Werkzeug
    if not (ordner / "finish.json").exists():
        lauf([sys.executable, BAUEN, "--clip", r["clip"], "--ab", r["ab"], "--dauer", r["dauer"],
              "--text", r["text"], "--betont", r["betont"], "--name", r["name"],
              "--hoehe", r["hoehe"]])
    spec = json.loads((ordner / "finish.json").read_text(encoding="utf-8"))
    h = spec["hook"]
    h.update(stil=r["stil"], akzent=r["akzent"], position=float(r["hoehe"]),
             oben=r["text"], betont=r["betont"], zusatz=r.get("zusatz", ""),
             sofort=True, ab_sek=0.0)
    h.pop("zusatz_allein", None)
    # Schluss: der Hook blendet 2,6 s vor Ende aus, der Aufruf steht dann gross und
    # allein. Lief er mit, lag er beim Serif-Stil auf der orangen Zeile.
    # Der Aufruf kommt als eigene Einblendung (Chip mit Pop), nicht als `zusatz`:
    # beim Marker-Stil zeichnet textebene.py den zusatz gar nicht, beim Serif-Stil
    # war er klein und blass (Sichtpruefung 12.10.).
    cta = h.get("zusatz", "")
    h["zusatz"] = ""
    if cta:
        h["dauer"] = round(r["dauer"] - 2.6, 2)
    # Aufruf erst am Schluss und dann allein (Vorgabe von textebene.py). Mit
    # zusatz_allein=False lag er beim Serif-Stil auf der orangen Zeile (Layout-Check 12.10.).
    elemente = []
    for i, s in enumerate(r.get("schritte", [])):
        elemente.append({"typ": "chip", "text": s, "flaeche": "glas", "groesse": 48, "umbruch": True,
                         "bewegung": "links" if i % 2 == 0 else "rechts",
                         "sound": "pop", "ab_sek": 1.4 + i * 1.3,
                         "dauer": r["dauer"] - 2.85 - (1.4 + i * 1.3),
                         "wo": {"x": 50, "y": 48 + i * 10}})
    if cta:
        elemente.append({"typ": "chip", "text": cta, "flaeche": "glas", "groesse": 62, "umbruch": True,
                         "bewegung": "pop", "sound": "pop",
                         "ab_sek": round(r["dauer"] - 2.5, 2), "dauer": 2.4,
                         "wo": {"x": 50, "y": r.get("cta_y", 50)}})
    spec["elemente"] = elemente
    (ordner / "finish.json").write_text(json.dumps(spec, ensure_ascii=False, indent=2),
                                        encoding="utf-8")
    (ordner / "bauplan.json").write_text(json.dumps({**r, "rendern": rendern},
                                                    ensure_ascii=False, indent=2),
                                         encoding="utf-8")
    lauf([sys.executable, TEXTEBENE, ordner / "finish.json",
          "--rendern" if rendern else "--konzept"])


def main():
    rendern = "--rendern" in sys.argv
    namen = [a for a in sys.argv[1:] if not a.startswith("--")]
    for r in REELS:
        if namen and r["name"] not in namen:
            continue
        print(f"\n=== {r['name']} ===")
        bauen(r, rendern)


if __name__ == "__main__":
    main()
