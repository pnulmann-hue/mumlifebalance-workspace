# -*- coding: utf-8 -*-
"""Abdeckungs-Test gegen den AKTUELLEN Notion-Stand (nach den Fixes vom 7.9.).

Simuliert 400 Vorabend-Briefings und meldet jede offene Aufgabe, die im
ganzen Jahr kein einziges Mal auftaucht.
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.path.insert(0, r"C:\Users\pnulm\Desktop\Mein Business\scripts\haushalts-bot")
from datetime import date, timedelta
from collections import Counter
import briefing_builder as bb

# (Aufgabe, Bereich, Rhythmus, Wochentag, Datum, Wer, Notiz) — Stand Notion 7.9.2026
R = [
 # --- täglich ---
 ("Flusensieb reinigen","Haushalt","täglich",None,None,"Patricia","nach jedem Waschen"),
 ("Kochen","Haushalt","täglich",None,None,"Patricia",None),
 ("Eigenes Zimmer aufräumen","Kinder-Ämtli","täglich",None,None,"Kinder","Rhythmus bestätigen"),
 ("Altglas aus Küche in den Keller","Kinder-Ämtli","täglich",None,None,"Kinder",None),
 ("Karton + Altpapier in den Keller","Kinder-Ämtli","täglich",None,None,"Kinder","Entsorgung Mi-Abend"),
 ("Tisch abräumen","Kinder-Ämtli","täglich",None,None,"Kinder",None),
 ("Abtrocknen","Kinder-Ämtli","täglich",None,None,"Kinder",None),
 ("Geschirrspüler ausräumen","Kinder-Ämtli","täglich",None,None,"Kinder",None),
 ("Instrument üben (15 Min)","Kinder-Ämtli","täglich",None,None,"Kinder","3 Kinder · Patricia erinnert"),
 ("Wäsche waschen","Haushalt","jeden 2. Tag",None,None,"Patricia",None),
 # --- wöchentlich MIT Wochentag (neu gesetzt) ---
 ("EG-Räume: staubsaugen, wischen, staubwischen","Haushalt","wöchentlich","Mo",None,"Patricia",None),
 ("Wäsche bügeln","Haushalt","wöchentlich","Mo",None,"Patricia",None),
 ("Handtücher wechseln","Haushalt","wöchentlich","Mo",None,"Patricia",None),
 ("Zimmerpflanzen giessen","Haushalt","wöchentlich","Mo",None,"Patricia",None),
 ("OG-Räume saugen + abstauben","Haushalt","wöchentlich","Di",None,"Patricia",None),
 ("Geschirrtücher/Lappen wechseln","Haushalt","wöchentlich","Di",None,"Patricia",None),
 ("Niklaus Hauswirtschaft/Kochen — mittags NICHT zu Hause","Familie/Termin","wöchentlich","Di",None,"Patricia","ab 10:00 Hauswirtschaft"),
 ("Waschküche saugen + Boden aufnehmen","Haushalt","wöchentlich","Mi",None,"Patricia",None),
 ("Abluftfilter reinigen","Haushalt","wöchentlich","Mi",None,"Patricia",None),
 ("EG Toilette putzen","Haushalt","wöchentlich","Mi",None,"Patricia",None),
 ("WC-Papier + Seife nachfüllen","Haushalt","wöchentlich","Mi",None,"Patricia",None),
 ("Altglas + Büchsen entsorgen","Haushalt","wöchentlich","Mi",None,"Patricia","Mi-Abend"),
 ("Altpapier + Altkarton entsorgen","Haushalt","wöchentlich","Mi",None,"Patricia","Mi-Abend"),
 ("Kühlschrank + Kochinsel reinigen","Haushalt","wöchentlich","Do",None,"Patricia",None),
 ("Bad oben putzen","Haushalt","wöchentlich","Do",None,"Patricia",None),
 ("Einkaufen mit Mahlzeitenplanung","Haushalt","wöchentlich","Do",None,"Patricia",None),
 ("Wäsche falten + verräumen","Kinder-Ämtli","wöchentlich","Do",None,"Kinder","pro Waschgang"),
 ("Verwaltungsrat-Slot (Unterlagen/Mandat)","Selbst/Me-Time","wöchentlich","Fr",None,"Patricia","~2h"),
 ("Büro + restliche UG-Räume: saugen, wischen, abstauben","Haushalt","wöchentlich","Sa",None,"Patricia",None),
 ("Post + Papierkram sortieren","Haushalt","wöchentlich","Sa",None,"Patricia",None),
 ("UG saugen + aufnehmen","Kinder-Ämtli","wöchentlich","Sa",None,"Kinder","bestätigen"),
 ("Paar-Ritual / Zeit zu zweit","Selbst/Me-Time","wöchentlich","So",None,"Patricia","Sonntags-Wanderung"),
 # --- wöchentlich OHNE Wochentag ---
 ("Krafttraining","Selbst/Me-Time","wöchentlich",None,None,"Patricia","Mo / Mi / Fr · Zeit flexibel"),
 ("Halber Tag Auszeit","Selbst/Me-Time","wöchentlich",None,None,"Patricia","Ziel — Wochentag festlegen; kein Druck"),
 # --- monatlich ---
 ("Backofen reinigen","Haushalt","monatlich",None,None,"Patricia",None),
 ("Garage aufräumen","Haushalt","monatlich",None,None,"Patricia",None),
 ("Schlafzimmer Bettwäsche wechseln","Haushalt","monatlich",None,None,"Patricia","Anker: nach der Mens"),
 ("Batterien + Elektroschrott + Sonderzeug entsorgen","Haushalt","monatlich","Mi",None,"Patricia","mit Altkarton-Gang"),
 ("Eigene Bettwäsche wechseln","Kinder-Ämtli","monatlich",None,None,"Kinder","die Grossen selbst"),
 ("Freundinnen-Treffen","Selbst/Me-Time","monatlich",None,None,"Patricia","Ziel — regelmässig sehen (1×/Monat)"),
 ("Sauna","Selbst/Me-Time","monatlich",None,None,"Patricia","2× pro Monat, eher Herbst–Frühling"),
 # --- alle 3 Monate (Quartalsregel) ---
 ("Waschmaschinen-Reinigung","Haushalt","alle 3 Monate",None,None,"Patricia",None),
 ("Alle Wasserhähne entkalken","Haushalt","alle 3 Monate",None,None,"Patricia",None),
 ("Bügeleisen entkalken","Haushalt","alle 3 Monate",None,None,"Patricia",None),
 ("Fenster putzen","Haushalt","alle 3 Monate",None,None,"Patricia","quartalsweise"),
 ("Schultermine des Kindes ins System übertragen","Familie/Termin","alle 3 Monate",None,None,"Patricia","kommen pro Quartal"),
 # --- Saison (Notizen teils neu gesetzt) ---
 ("Alle Küchenschränke putzen","Haushalt","2x/Jahr",None,None,"Patricia","Frühling + Herbst"),
 ("Büro aufräumen","Haushalt","2x/Jahr",None,None,"Patricia","Frühling + Herbst"),
 ("Keller entrümpeln","Haushalt","2x/Jahr",None,None,"Patricia","Frühling + Herbst"),
 ("Gang: Spielzeugkasten räumen","Haushalt","3x/Jahr",None,None,"Patricia","Frühling + Sommer + Winter (vor Weihnachten Platz machen)"),
 ("Tumbler + Waschmaschine Wartung","Haushalt","jährlich",None,None,"Mann","Herbst"),
 ("Kleider-Grössen-Check Kinder","Saisonal","2x/Jahr",None,None,"Patricia","Frühling + Winter"),
 ("Reifenwechsel","Saisonal","2x/Jahr",None,None,"Mann","Frühling + Herbst"),
 ("Schuh-Grössen-Check Kinder","Saisonal","2x/Jahr",None,None,"Patricia","Frühling + Herbst"),
 ("Weihnachtsdeko raus / weg","Saisonal","jährlich",None,None,"Patricia","Dezember"),
 ("Fasnachts-Kostüm organisieren","Saisonal","jährlich",None,None,"Patricia","vor Fasnacht (Feb)"),
 ("Osternester / Oster-Deko","Saisonal","jährlich",None,None,"Patricia","vor Ostern"),
 ("Winterschuhe putzen, imprägnieren, verräumen","Saisonal","saisonal",None,None,"Patricia","vor Frühling"),
 ("Winterkleider waschen + verräumen, Frühlingsschuhe rein","Saisonal","saisonal",None,None,"Patricia","Frühling (UG Eingang)"),
 ("Sommersachen raus / Wintersachen rein","Saisonal","saisonal",None,None,"Patricia","Herbst (Gegenstück)"),
 ("Ski-/Winterausrüstung bereitmachen","Saisonal","saisonal",None,None,"Patricia","Herbst/Winter"),
 ("Badesachen + Sonnencreme/Hut bereit","Saisonal","saisonal",None,None,"Patricia","Frühling/Sommer"),
 ("Mützen gegen Baseballkappen tauschen","Saisonal","saisonal",None,None,"Patricia","Frühling"),
 ("Hecke schneiden","Aussen","jährlich",None,None,"Patricia","Herbst"),
 ("Laub / Herbst-Aufräumen","Aussen","jährlich",None,None,"Patricia","Herbst"),
 ("Steuererklärung","Familie/Termin","jährlich",None,None,"Patricia","Frühling"),
 ("Zahnkontrolle Patricia","Familie/Termin","jährlich",None,None,"Patricia","Sommer"),
 # --- datiert / einmalig / Geburtstage ---
 ("Adventsdeko + Adventskalender vorbereiten","Saisonal","jährlich",None,"2026-11-25","Patricia","Ende Nov"),
 ("Frauenarzt-Termin machen","Familie/Termin","einmalig",None,None,"Patricia","überfällig"),
 ("Zahnarzt-Termin anrufen (für Sommer)","Familie/Termin","einmalig",None,"2026-06-15","Patricia","JETZT im Juni anrufen"),
 ("Geburtstag Patenkind (Mann) — Geschenk besorgen","Geburtstag","jährlich",None,"2026-09-24","Patricia","Geschenk ~Mitte Sept"),
 ("Geburtstag Patenkind (Patricia) — Geschenk besorgen","Geburtstag","jährlich",None,"2026-11-06","Patricia","Geschenk ~Ende Okt"),
 ("Geburtstag Mann — Geschenk besorgen","Geburtstag","jährlich",None,"2026-06-24","Patricia","Geschenk ~Mitte Juni"),
]

EINTRAEGE = [{
    "id": str(i), "aufgabe": a, "bereich": b, "rhythmus": r, "wochentag": w,
    "fixes_datum": d, "notiz": n or "", "wer": p, "erledigt": False,
} for i, (a, b, r, w, d, p, n) in enumerate(R)]

gesehen: Counter = Counter()
start = date(2026, 9, 1)
for i in range(400):
    st = bb.baue_briefing_struktur(EINTRAEGE, heute=start + timedelta(days=i))
    for block in st["bloecke"]:
        for zeile in block["items"]:
            for e in EINTRAEGE:
                if e["aufgabe"] in zeile:
                    gesehen[e["aufgabe"]] += 1

alle = {e["aufgabe"] for e in EINTRAEGE}
fehlend = sorted(alle - set(gesehen))

print(f"Offene Aufgaben:        {len(alle)}")
print(f"Im Jahr mind. 1x drin:  {len(gesehen)}")
print(f"NIE sichtbar:           {len(fehlend)}")
if fehlend:
    print("\n--- FALLEN DURCH ---")
    for f in fehlend:
        e = next(x for x in EINTRAEGE if x["aufgabe"] == f)
        print(f"   x {f} | {e['rhythmus']} | WT={e['wochentag']} | Notiz={e['notiz'][:35]!r}")
else:
    print("\nAlles abgedeckt.")

print("\n--- Seltene (< 5 Nennungen im Jahr) ---")
for name, n in sorted(gesehen.items(), key=lambda t: t[1]):
    if n < 5:
        print(f"   {n:2}x  {name}")
