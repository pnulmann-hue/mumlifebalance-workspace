"""
Legt Google Drive und Canva als Fundstellen in die Cockpit-Suche.

Kopiert wird nichts. Was hier steht, ist ein Wegweiser mit Direktlink: Suche
nach einem Stichwort, und du siehst, dass es dazu einen Drive-Ordner oder ein
Canva-Design gibt — ein Klick, und du bist drin.

Die Daten kommen ueber die Connectoren herein (Drive `search_files`, Canva
`search-designs`) und werden hier eingetragen. Beide sind nicht aus einem
Skript erreichbar, deshalb stehen sie als Tabelle.

Was bewusst draussen bleibt:
  09 - Admin & Logins     Zugangsdaten haben in einer Cloud-Seite nichts verloren
  08 - Rezepte (privat)   privat
  Rezepte, Menuplanung    privat

Aufruf:
  python scripts/cockpit/fundstellen-bauen.py [zielordner]
"""
import json
import sys
from datetime import date
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]
DRIVE = "https://drive.google.com/drive/folders/"

# Ordner in Drive — Titel, Kennung, was drin liegt.
ORDNER = [
    ("01 - Zielgruppe & Positionierung", "1DE7ztqdxomatpFe9cdSfgqu29pXh1f_L",
     "Zielgruppen-Recherche, Positionierung, Avatar-Arbeit"),
    ("02 - Content Erstellung & Strategie", "1z2TZxHoMXUIUvtnlz6GAIz3AYQsCdQvQ",
     "Content-Strategie, Story-Bibliothek, Hook-Sammlungen"),
    ("03 - Prompts & KI-Tools", "1c_aWHM1lb-3_SuKmUJG8b4Anuv27Piq3",
     "Prompts, KI-Werkzeuge, Assistenten"),
    ("04 - Angebote, Verkauf & Funnels", "1Cd2a-UXjxC60fTuqbnEaQQ4ePkruSZqk",
     "Angebote, Verkaufsseiten, Funnel-Unterlagen, Nische finden"),
    ("05 - Freebies & Lead Magnets", "1Njjqrukd3pc3nseAVDDrTmhu9KdUSWmV",
     "Freebies und Leadmagnete"),
    ("05 · Story-Challenge", "1_vqer0RRALsbDOJUfoJU6BOeh2VanQmH",
     "Unterlagen der Story-Challenge"),
    ("06 - Learnings & Notizen", "11dC870M0ypcMmgLiKQHXPeDtUI53_zEs",
     "Learnings, Notizen, Mitschriften"),
    ("07 - Buecher & Nachschlagewerke", "13RjTgIo_Tbz2dhurQZz_wlPTf56mYG-1",
     "Bücher und Nachschlagewerke"),
    ("Produkte", "1zp6RZ1emLtetux9B0ygQ9awZufjUQNAk",
     "Oberordner aller Kurs-Unterlagen"),
    ("Produkte · Instagram-Kundenmaschine", "1t7Nf8BVfQLCUGJ_TmZUl7-HJcIQY-VsZ",
     "Kurssheets und Unterlagen zur Instagram-Kundenmaschine"),
    ("Produkte · IKM Transkripte", "10hUlE1-JzEBRU_ssdCsf8gKKwQ2CV_26",
     "Call-Transkripte der Instagram-Kundenmaschine"),
    ("Produkte · Mama-CEO", "1LFGlsY28dP3ZVQnDF_2EBEYCGubjTh7e",
     "Arbeitsblätter und Unterlagen zu Mama-CEO"),
    ("Produkte · Mama-CEO Säule 4", "1q1_h6Xrs_67S2mBjzTt8h8mg7Sc6yIuT",
     "Arbeitsblatt und Bonus-Vorlagen zu Säule 4, den KI-Mitarbeitern"),
    ("Produkte · Vom Networkwissen zur digitalen Produktwelt",
     "1qFMuKUyNi8VnQErlMkW6d29lP4oOZU9J", "Kursunterlagen"),
    ("Vom Produktwissen zur digitalen Produktwelt",
     "1zuax7FmIrFaCAPbHtaevHfqpkg6Org0p", "ältere Ablage zum selben Kurs"),
    ("doTERRA", "1MHk-5zX2ic9JiMbZGSrBAwtla52PMsIs",
     "doTERRA-Unterlagen"),
    ("Öl-Wissen", "1TuKVEpJK20aV1AuKuQSH10tbXMD7hZ68",
     "Produktwissen zu den Ölen"),
    ("Story", "15QxMlkP7Vr6hUBKPoa9N1w43dFo-jmF6",
     "Story-Material"),
    ("Freebies", "1jRoJ6Qq40czWDWYlIXojQjIVXmHRJtLG",
     "ältere Freebie-Ablage"),
    ("content der Verkauft — Julia Trost", "1Yhr8rkTVNRwqDJjtv1HnezYIEs840fAy",
     "fremder Kurs: Content der verkauft"),
]

# Canva — nur benannte Designs, Dubletten zusammengefasst.
CANVA = [
    ("20260501-doterra-3-naehrstoffe-ab-35", "hrZZriRn-9n5EVo", 7),
    ("Workbook Story-Challenge", "csjTZkj9wlUXMv1", 20),
    ("MBA — Pitch-Story-Slides", "ZBviOLTWXYYo1F0", 10),
    ("📒 Workbook Vorlagen", "EeL10dNKhZbUq0m", 114),
    ("Reels Test 1", "oWl10My5wMLQqBH", 109),
    ("Feed Beiträge", "O1CenXmC9qULunE", 20),
    ("So würde ich starten", "98nZBJUOwlXqYGo", 16),
    ("Mentoring Fr 24.04 — 10.000 Follower Thema", "qyw6B8CKJPA20IP", 11),
    ("doTERRA Fr 24.04 — Perimenopause mit Ü35", "h7k6BK6Gef6gOUo", 11),
    ("doTERRA Mi 22.04 — 5 Energie-Killer", "UEPNuXgyXymTWQD", 11),
    ("Vorlage Claude", "Fmj3EIYveqebZlL", 11),
    ("Karussell — 5 Sätze, nach denen Freundinnen aufhören zu kaufen",
     "8Wv4xmYi7SLRyMO", 11),
    ("Do M3 Reel Cover — Posten-Angst", "7LBEaGhH5SNlLZO", 1),
    ("Reel-Vorlage", "JYq8nlZ2U6e3WBF", 8),
    ("Instagram-Beitrag — Die 5 Säulen der Gesundheit", "sC5b4oATObo9fuy", 1),
    ("Instagram-Beitrag — Wild Orange, das Öl für Neuanfänge", "nXKG4jQIv-WfaAl", 4),
    ("Instagram-Beitrag — Haut-Reset für den Frühling", "XZlY0M56uf0tYG8", 1),
    ("Instagram-Beitrag — Ölziehen, der stille Held der Morgenroutine",
     "eQv4dvtQSkvZ6o-", 1),
    ("Instagram-Beitrag — Stoffwechsel auf Frühling umstellen", "EQfLsdFYcgZk160", 4),
    ("Instagram-Beitrag — Frühjahrs-Reset ganz sanft", "wth20hiNoMxOVzb", 1),
    ("Instagram-Beitrag — Kühler Kopf, entspannt durch den Sommer",
     "zfmeyK30x_XPnW-", 6),
    ("Instagram-Beitrag — Sommer-Inspirationen mit ätherischen Ölen",
     "KSQu2m0Uhxyy8JN", 1),
    ("Instagram-Beitrag — Fussbad-Ritual", "lXsZAN2YiVEOiFn", 1),
]


def main():
    ziel = Path(sys.argv[1]) if len(sys.argv) > 1 else \
        ROOT / "outputs" / "cockpit" / "abgleich"
    ziel.mkdir(parents=True, exist_ok=True)

    eintraege = []
    for titel, kennung, was in ORDNER:
        eintraege.append({
            "d": DRIVE + kennung,
            "t": titel,
            "a": was,
            "b": "Drive",
        })
    for titel, kennung, seiten in CANVA:
        eintraege.append({
            "d": "https://www.canva.com/d/" + kennung,
            "t": titel,
            "a": "Canva-Design, %d %s" % (seiten, "Seite" if seiten == 1 else "Seiten"),
            "b": "Canva",
        })

    heute = date.today().isoformat()
    (ziel / "fundstellen.json").write_text(json.dumps(
        {"items": eintraege, "stand": heute}, ensure_ascii=False),
        encoding="utf-8")

    print("  %d Drive-Ordner · %d Canva-Designs" % (len(ORDNER), len(CANVA)))
    print("\nAbgelegt in: %s" % (ziel / "fundstellen.json"))


if __name__ == "__main__":
    main()
