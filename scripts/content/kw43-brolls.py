#!/usr/bin/env python3
"""Die fuenf B-Rolls fuer 19.-23.10.2026 (KW43) nach Julia Muellers staerksten Reels.

Texte und Herkunft: outputs/content/KW43/julia-nachbau.md
Gebaut mit derselben Funktion wie KW42 (`bauen` aus kw42-brolls.py), damit es nur ein
Bauwerk fuer animierte B-Rolls gibt.

Schritt 1: Konzept (Standbilder):   python scripts/content/kw43-brolls.py [name ...]
Schritt 2: rendern:                 python scripts/content/kw43-brolls.py --rendern [name ...]
"""
import importlib.util
import pathlib
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
_pfad = pathlib.Path(__file__).with_name("kw42-brolls.py")
_spec = importlib.util.spec_from_file_location("kw42_brolls", _pfad)
kw42 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(kw42)

REELS = [
    dict(name="kw43-m-mo-story", clip="VID-20260524-WA0007", ab=0.0, dauer=9.0, hoehe=40,
         stil="serif", akzent="orange",
         text="Dickes SORRY, liebe doTERRA-, Fitline- & Ringana-Partnerinnen:",
         betont="Wenn ich in eurer Story den Shake, den Kinderausflug und das Unboxing sehe, kaufe ich nicht.",
         zusatz="Warum eure Storys ein Restaurant ohne Speisekarte sind – lies die Caption"),
    dict(name="kw43-m-di-liste", clip="20260911_092600", ab=2.0, dauer=7.0, hoehe=48,
         stil="serif", akzent="orange",
         text="Grosse Marken bauen heute Communities. Wir Networkerinnen schreiben noch Namenslisten.",
         betont="In fünf Jahren gibt es nur noch eins davon.",
         zusatz="Schick das einer Network-Freundin"),
    dict(name="kw43-m-mi-bio", clip="20260618_093828", ab=2.5, dauer=7.5, hoehe=42,
         stil="serif", akzent="orange",
         text="Liebe doTERRA-, LR- & Ringana-Partnerinnen: Euer Reel hat mich abgeholt. Dann tippe ich auf euer Profil und lese „Mama von zwei, lebe meinen Traum“.",
         betont="Und schon bin ich wieder weg.",
         zusatz="Kommentier BIO"),
    dict(name="kw43-m-do-droge", clip="20260417_160303", ab=0.0, dauer=8.0, hoehe=48,
         stil="marker", akzent="orange",
         text="Die neue Droge im Network:",
         betont="Partnerinnen von doTERRA, Fitline, LR & Ringana kommen reihenweise nicht mehr davon los …",
         zusatz="Schick das einer Network-Freundin"),
    dict(name="kw43-m-fr-upline", clip="20260426_120447", ab=0.0, dauer=9.4, hoehe=12.5,
         stil="serif", akzent="orange",
         text="Deine Upline zeigt das neue Auto und die Woche am Meer,",
         betont="während du heimlich rechnest, wie die nächste Mindestbestellung noch auf die Kreditkarte passt.",
         zusatz="Kommentier STANDBEIN"),
    # Kassenschluss KI-Kurs, Texte: outputs/content/KW43/ki-kurs-schluss.md
    dict(name="kw43-m-do-parkplatz", clip="20260623_091315", ab=0.0, dauer=5.8, hoehe=40,  # ab 6 s laufen Kinder ins Bild
         stil="serif", akzent="orange",
         text="Mein Büro war vor zwei Jahren",
         betont="der Parkplatz vor der Musikschule.",
         zusatz="Kommentier STIMME"),
    dict(name="kw43-m-fr-halbzwoelf", clip="VID_145730108_004600_892-ton", ab=1.0, dauer=8.0, hoehe=48,
         stil="serif", akzent="orange",
         text="Um halb zwölf ist bei mir Feierabend fürs Business.",
         betont="Danach gehört der Tag den vier Kindern.",
         zusatz="Kommentier STIMME"),
]


def main():
    rendern = "--rendern" in sys.argv
    namen = [a for a in sys.argv[1:] if not a.startswith("--")]
    for r in REELS:
        if namen and r["name"] not in namen:
            continue
        print(f"\n=== {r['name']} ===")
        kw42.bauen(r, rendern)


if __name__ == "__main__":
    main()
