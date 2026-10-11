#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Der Regie-Zettel fuer die KI-Masterclass am 8.10.2026.

    python scripts/ki-kurs/regiezettel-bauen.py
    preview_start {"name": "masterclass-regie"}      # Port 4401

Warum als eigene Seite und nicht als Folie: **sobald Patricia den Bildschirm
teilt, sieht sie die Folien nicht mehr.** Genau dann braucht sie die Angabe,
was zu zeigen ist. Also gehoert das auf Papier oder auf den zweiten Schirm.

Eine A4-Seite, quer gelesen: Uhrzeit · was auf der Folie steht · was sie tut.
Die drei Bildschirm-Bloecke sind orange hinterlegt und koennen nicht
uebersehen werden.
"""
import io, os

ZIEL = "outputs/produkte/ki-treppe/masterclass-regie.html"

CREME, BLAU, PETROL, ORANGE, TINTE = "#f1ecdd", "#29556d", "#12828c", "#dc822e", "#0c1c30"

# (ab Minute, Titel, was Patricia tut, Bildschirm?)
ABLAUF = [
 ("0", "Cover — die Frage",
  "Warten, bis alle da sind. Dann die Frage von der Folie laut vorlesen und eine "
  "Pause machen. Kein Vorgeplauder über Technik.", False),
 ("2", "Der Elefant · Die Szene · Es liegt nicht an dir",
  "„Alle sagen, KI spart Zeit. Bei dir kostet sie welche.“ Dann die Szene, dann die "
  "Entlastung. Hier nicken sie mit.", False),
 ("5", "Du stellst Fragen · Sie kann nur den Durchschnitt",
  "„Das ist Google mit besseren Sätzen.“ — Pause. Dann die Grafik: links das halbe "
  "Internet, rechts dein Material. Langsam, das ist das Fundament.", False),
 ("8", "DAS RÄTSEL — zwei erste Zeilen",
  "Raten lassen, wirklich im Chat. Zehn Sekunden warten. Dann auflösen: beide sind "
  "von einer KI, nur wusste sie einmal nichts über mich.", False),
 ("11", "Paar zwei · Paar drei · Das Prinzip",
  "Zwei weitere Vergleiche, je mit dem Unterschied darunter. Dann die drei Prinzipien: "
  "Szene statt Thema · Zahl statt Versprechen · zugeben statt behaupten.", False),
 ("15", "BILDSCHIRM 1 — derselbe Auftrag zweimal",
  "Auftrag OHNE Vorwissen laufen lassen, Ergebnis vorlesen. Dann Brief aufklappen, "
  "20 Sekunden scrollen. Auftrag nochmal MIT Brief. Beide nebeneinander vorlesen. "
  "Nicht erklären, WIE der Brief entsteht.", True),
 ("20", "Drei Stufen",
  "Die Landkarte mit der Treppen-Grafik. Dazu: Stufe 1 allein ändert den Alltag "
  "schon, niemand muss bis nach oben.", False),
 ("22", "Stufe zwei — Freitagmorgen, kurz nach sieben",
  "Der Essensplan liegt auf dem Handy. „Ich habe ihn nicht bestellt. Er kommt jeden "
  "Freitag.“", False),
 ("23", "BILDSCHIRM 2 — mein Handy am Freitagmorgen",
  "Telegram aufmachen, die Nachricht mit dem Essensplan aufklappen und durchscrollen: "
  "sieben Abende, Einkaufsliste nach Laden, Mengen für sechs. Dann hochscrollen zu den "
  "anderen, die sich von selbst melden — morgens, abends, sonntags. Handy in die Kamera, "
  "nicht spiegeln.", True),
 ("27", "Stufe drei — ich kann nicht programmieren",
  "„Und habe trotzdem ein Werkzeug gebaut, das meine Leute täglich benutzen.“ Sag "
  "„geredet“, nicht „beschrieben“.", False),
 ("28", "BILDSCHIRM 3 — das Werkzeug für meine Leute",
  "Die Begleitungs-Seite: was eine Teilnehmerin sieht. Durch zwei, drei Tage klicken. "
  "DANN das Cockpit, wo du prüfst und freigibst. In dieser Reihenfolge.", True),
 ("33", "Nichts geht raus ohne mich · Ein Freitagmorgen · Für wen · Kurz zu mir",
  "Das Partnerunternehmen nennen — dein Unterschied zu jedem Technikkurs. Dann dein "
  "Morgen, die ehrliche „für wen nicht“-Spalte, zwei Sätze zu dir.", False),
 ("37", "Du hast gesehen, was möglich ist · Ich habe ein Jahr gebraucht",
  "Ruhig bleiben, kein Tempowechsel.", False),
 ("38", "Der Kurs · Start 1. November · Du bist damit nicht allein",
  "Name sagen, Folie wirken lassen. Dann die drei Punkte: 1. November die ersten Module, "
  "die Gruppe mit Antworten dienstags und donnerstags, und die zwei Calls am 19. November "
  "und 10. Dezember. Dass beide aufgezeichnet werden, laut sagen — das räumt den "
  "Termin-Einwand weg, bevor er kommt.", False),
 ("40", "Module · Das kommt mit · Die ehrliche Rechnung · 277",
  "Drei Blöcke statt zehn Zeilen. Dann die Rechnung, dann der Preis — und STEHEN "
  "LASSEN. Drei Sekunden Stille. „Die erste Runde ist bei mir immer die günstigste.“", False),
 ("43", "Ein Kurs allein macht noch keinen Inhalt",
  "Die Einordnung: der Kurs ist die Maschine, die Academy ist der Inhalt. Ruhig sagen, "
  "nicht als Verkaufssatz. Wer schon Inhalt hat, kommt mit dem Kurs weit.", False),
 ("44", "Was in der Academy steckt · Die Academy 1347",
  "Drei Kurse, je ein Satz — beim Kochassistenten in Mama-CEO kurz stehen bleiben, "
  "das verbindet mit dem Handy von vorhin. Dann die Rechnung LAUT: vier Kurse zu 333 "
  "sind 1332, die Academy kostet 1347, und darin sind 24 Calls und ein Jahr Begleitung. "
  "Stehen lassen. Dann die sechs Raten zu 224.50 — mit dem Grund, nicht als Technik.", False),
 ("46", "Fair bleibt fair · Einwände · Ein Schritt",
  "Academy gratis dabei, Anrechnung. Die drei Einwände vorwegnehmen. Link in den Chat, "
  "während du es sagst.", False),
 ("48", "Was möchtest du noch wissen?",
  "Folie lange stehen lassen. Bleiben, bis alles beantwortet ist.", False),
]

MERKEN = [
 "Kein Wie. Wenn jemand fragt: „genau das machen wir im Kurs zusammen.“",
 "Nie sagen, dass der Kurs noch entsteht. Start ist der 1. November, fertig.",
 "277 bis Donnerstag, 15. Oktober. Ab 16. Oktober 333.",
 "Academy-Kundinnen: der Kurs ist für sie gratis dabei — das laut sagen.",
 "Nie von „zwei Monaten“ reden — die Gruppe bleibt auch danach. "
 "Calls: Do 19.11. und Do 10.12., beide aufgezeichnet.",
 "Keine erfundenen Zahlen. Keine Garantie. Keine Plätze-Verknappung.",
 "Der Essensplan-Push läuft seit 5. Oktober wieder — Freitag früh, automatisch.",
 "Academy 1347 oder sechs Raten zu 224.50. 1347 ist der NORMALE Preis — "
 "keine Frist behaupten. Neu ist, dass der KI-Kurs als vierter dazukommt.",
]


def zeile(ab, titel, tun, schirm):
    grund = "#fdf4ea" if schirm else "#ffffff"
    rand  = ORANGE if schirm else "#e3ddd0"
    marke = ('<div style="font:700 11pt/1.2 Arial; color:%s; letter-spacing:.5px; '
             'text-transform:uppercase; margin-bottom:3px">Bildschirm teilen</div>' % ORANGE) if schirm else ""
    return ('<tr>'
            '<td style="background:%s; border-top:2px solid %s; padding:9px 8px 9px 0; '
            'font:700 15pt/1 Arial; color:%s; width:52px; vertical-align:top">%s</td>'
            '<td style="background:%s; border-top:2px solid %s; padding:9px 10px; '
            'vertical-align:top; width:235px">%s'
            '<div style="font:700 11.5pt/1.3 Arial; color:%s">%s</div></td>'
            '<td style="background:%s; border-top:2px solid %s; padding:9px 0 9px 10px; '
            'vertical-align:top; font:10.5pt/1.45 Arial; color:#333">%s</td>'
            '</tr>' % (grund, rand, BLAU, ab, grund, rand, marke, BLAU, titel,
                       grund, rand, tun))


HTML = """<!doctype html>
<html lang="de"><head><meta charset="utf-8">
<title>Regie-Zettel · KI-Masterclass 8. Oktober</title>
<style>
  @page { size: A4; margin: 12mm 14mm; }
  body { font-family: Arial, sans-serif; color:%(TINTE)s; margin:0; padding:18px 22px; background:#fff; }
  h1 { font:700 21pt/1.15 Arial; color:%(BLAU)s; margin:0 0 2px; }
  .unter { font:10.5pt/1.4 Arial; color:#666; margin:0 0 14px; }
  table { border-collapse:collapse; width:100%%; }
  .merk { margin-top:16px; border:2px solid %(PETROL)s; border-radius:8px; padding:11px 14px; background:#f4faf9; }
  .merk h2 { font:700 12pt/1.2 Arial; color:%(PETROL)s; margin:0 0 7px; text-transform:uppercase; letter-spacing:.6px; }
  .merk ul { margin:0; padding-left:17px; }
  .merk li { font:10.5pt/1.5 Arial; margin-bottom:3px; }
  .fuss { margin-top:12px; font:9.5pt/1.4 Arial; color:#888; }
  @media print { body { padding:0; } .noprint { display:none; } }
</style></head>
<body>
<h1>Regie-Zettel &middot; KI-Masterclass</h1>
<p class="unter">Donnerstag, 8. Oktober 2026, 9 Uhr &middot; rund 45 Minuten &middot;
Minutenangaben ab Beginn. <b>Drei Bildschirm-Blöcke, orange markiert.</b></p>
<table>%(ZEILEN)s</table>
<div class="merk">
  <h2>Was immer gilt</h2>
  <ul>%(MERKEN)s</ul>
</div>
<p class="fuss">Die Folien liegen unter claude.ai &middot; Sprechnotizen stehen auf jeder
Folie &middot; dieser Zettel gehört auf Papier oder den zweiten Bildschirm, weil die
Folien beim Teilen nicht mehr sichtbar sind.</p>
</body></html>
""" % {
  "TINTE": TINTE, "BLAU": BLAU, "PETROL": PETROL,
  "ZEILEN": "".join(zeile(*z) for z in ABLAUF),
  "MERKEN": "".join("<li>%s</li>" % m for m in MERKEN),
}

os.makedirs(os.path.dirname(ZIEL), exist_ok=True)
with io.open(ZIEL, "w", encoding="utf-8", newline="\n") as f:
    f.write(HTML)

# Umlaut-Waechter ueber den sichtbaren Text
import re
sichtbar = re.sub(r"<[^>]+>", " ", HTML)
sichtbar = re.sub(r"<style>.*?</style>", " ", sichtbar, flags=re.S)
AUSNAHMEN = ("bauen","dauert","Frauen","heute","zuerst","auch","auf","aus","laut",
             "draussen","brauchst","Frau","schauen","genau","Pause","baue","baut",
             "glaube","kaufe","laufen","Verlauf","neues","neue","Arial")
uml = re.compile(r"\b\w*(ae|oe|ue)\w*\b")
funde = [m.group(0) for m in uml.finditer(sichtbar)
         if not any(m.group(0).lower().startswith(a.lower()) for a in AUSNAHMEN)]
print("%d Zeilen -> %s" % (len(ABLAUF), ZIEL))
print("Bildschirm-Bloecke:", sum(1 for z in ABLAUF if z[3]))
print("Umlaut-Waechter:", "sauber." if not funde else "PRUEFEN: %s" % set(funde))
