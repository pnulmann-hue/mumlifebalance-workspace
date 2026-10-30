---
tags: [plan, content, research]
---

# Markt-Radar: die Auswertung von Content Radar, nachgebaut

Stand 30.10.2026 · Status: **gebaut für das eigene Konto (Cockpit V112)**. Offen ist der frische Scrape für
die fremden Konten. Entschieden ohne Rückfrage: nur Reels, Konten wie vorgeschlagen, Credits bleiben liegen.

## 1 · Worum es geht

Patricia: *„übernehme und analysiere bitte das system. vielleicht können wir das für mich auch bauen?“*
Content Radar zeigt je Konto, **welche Reels gelaufen sind und warum**: Punktzahl je Beitrag, ein Absatz
„warum“, Muster mit Zahlen, Hook-Vorlagen und beste Uhrzeit. Wir bauen diese Auswertung auf ihren eigenen
Daten nach, für ihr Konto und ihre Nische, monatlich neu und ohne Credits. Den Generator bauen wir nicht nach.

## 2 · Warum

- Content Radar ist eingestellt. Übrig sind 85 Credits, also noch etwa eine Analyse.
- Der Bericht hat beim Lesen Fehler gezeigt. Er liest gekürzte Captions und hält den Abbruch für einen
  „Cliffhanger“. Seine Uhrzeiten beruhen auf 2–3 Beiträgen je Stunde. Der Generator erfindet Zahlen
  („4.200 € verdient“, „47 Mamas“).
- Die Hook-Maschine (`scripts/hooks/markt-analyse.py`) misst schon den Faktor gegen den Konto-Median und
  setzt Etiketten. Es fehlen vier Teile: der Blick ins Video, das „Warum“ je Beitrag, ein lesbarer Bericht
  und die Uhrzeit.
- Der Befund vom 30.10. ist derselbe wie im Oktober: Ihre Reels werden gesehen (Ø 8'000 Views), aber es
  reagiert fast niemand (Ø 16 Likes). Der Bericht muss deshalb Reaktion und Reichweite getrennt zeigen.

## 3 · Die Schritte

1. **Daten prüfen.** Liefert `scrape-tiefe.js` für Reels eine `videoUrl`? In der Datei vom 08.10. stehen
   `displayUrl` und `videoViewCount`, eine Video-Adresse habe ich nicht gesehen. Falls sie fehlt, kommt sie
   als Feld in den Scrape, sonst bleibt es beim Titelbild.
2. **Top-Reels je Konto wählen** (neu: `scripts/hooks/radar.py`). Grundlage ist die Hook-Datenbank. Gewählt
   werden je Konto die 10 Reels mit dem höchsten Faktor gegen den eigenen Median und dazu die 5 schwächsten
   zum Vergleich. Es gelten die Mindestbasen der Hook-Maschine (ab 6 Beiträgen, ab 200 Views).
3. **Blick ins Video.** Mit ffmpeg drei Standbilder ziehen (0 s · 1 s · 3 s). Claude liest Text im Bild,
   Gesicht/Mimik und Ort. Ist kein Video da, nimmt Claude das Titelbild aus `bild-hooks.py`.
4. **„Warum lief das“ je Beitrag.** Claude bekommt die volle Caption, die Bilder, die Zahlen und den Faktor
   und schreibt einen Absatz dazu. Dazu kommen Hook-Note und Bild-Note. Ergebnisse gehen in einen Cache,
   wie bei den Etiketten.
5. **Bericht je Konto.** Er hat diese Teile: Zusammenfassung · 3–5 Hebel (Aufwand/Wirkung) · sofort
   umsetzbar · vermeiden · Muster mit Zahlen · beste/schwächste Stunde und beste/schwächste Tage.
   Reichweite und Reaktion stehen getrennt.
6. **Gegen ihre Regeln prüfen, bevor er gezeigt wird.** Jeder Vorschlag läuft durch `texte-pruefen.py`. Dazu
   kommt ein eigener Abgleich mit den Pflichtregeln aus `/content`: Stichwort nur am Schluss, kein Stakkato,
   keine erfundenen Zahlen, kein „Nicht X, sondern Y“. Was durchfällt, wird umgeschrieben oder gestrichen.
7. **Uhrzeit aus den eigenen Zahlen.** Grundlage ist `timestamp` aus `holen.py`, alle Abzüge. Gerechnet wird
   die Reichweite je Stunde und je Wochentag, mit mindestens 5 Beiträgen je Feld. Darunter steht dort „zu
   wenig Daten“. Die Werte werden getrennt nach Reel und Karussell gezeigt.
8. **Reiter im Cockpit:** Instagram → **Markt-Radar** (`patch-markt-radar.py` + `markt-radar-reiter.js/.css`).
   Er zeigt je Konto eine Karte mit dem Bericht und je Beitrag Zahlen, Standbild und das „Warum“. Daten liegen
   in `daten/markt-radar` (eigene Konten) bzw. in der Sammlung `markt-radar`, je Konto ein Dokument unter 200 KB.
9. **Monatlich laufen lassen.** Der Lauf kommt als Schritt in `/monatsplan` 4.5a, kein neuer Scheduled Task
   (Patricia: keine neuen Routinen). `/content` Schritt 4 liest die Hebel des jüngsten Berichts mit.
10. **Doku:** CLAUDE.md, Abschnitt Hook-Maschine, ergänzen und `testfassung-bauen.py` nachtragen.

## 4 · Woran wir merken, dass es fertig ist

- **Gegenprobe, die anschlagen muss:** Bei Patricias Konto steht „Ich liebe Empfehlungsmarketing …“ unter den
  Top 3, „Die meisten nutzen Instagram …“ unter den schwächsten. So hat es auch Content Radar gefunden.
- **Gegenprobe, die nicht anschlagen darf:** Kein Bericht nennt eine abgeschnittene Caption einen
  „Cliffhanger“. Keine Stunde mit weniger als 5 Beiträgen wird „beste Zeit“. Kein Vorschlag setzt das
  Stichwort an den Anfang.
- Für die Kern-Konten aus der Watchlist gibt es je einen Bericht im Cockpit, am Handy lesbar.
- `node --check` läuft ohne Fehler, die lokale Testfassung zeigt den Reiter, und kein anderer Reiter bricht.

## 5 · Was bewusst nicht dazugehört

- **Kein Generator** für Wochenplan oder Bio. Das bleibt `/content` und der Bio-Check.
- **Keine Hook-Bibliothek** mit 30 Vorlagen. Die hat der Hook-Skill schon.
- **Kein neuer Scrape-Dienst.** Die Daten kommen aus Apify wie bisher.
- **Keine TikTok-Konten.**
- **Kein Weitergeben an Kundinnen.** Die Berichte nennen fremde Konten, deshalb bleibt das Cockpit privat.

## 6 · Was es berührt

| Datei / Ort | Änderung |
|---|---|
| `scripts/apify/scrape-tiefe.js` | evtl. Feld `videoUrl` (Schritt 1) |
| `scripts/hooks/markt-analyse.py` · `hook-datenbank.json` | wird gelesen, nicht umgebaut |
| `scripts/hooks/radar.py` | **neu** (Schritte 2–7) |
| `scripts/cockpit/patch-markt-radar.py` + `markt-radar-reiter.js/.css` | **neu** (Schritt 8) |
| `scripts/cockpit/testfassung-bauen.py` | neuer Eintrag in `SEEDS` |
| `.claude/skills/monatsplan/SKILL.md` 4.5a · `.claude/skills/content/SKILL.md` Schritt 4 | je ein Verweis |
| CLAUDE.md, Abschnitt „Die Hook-Maschine“ | ergänzen |
| `outputs/marktrecherche/` | Berichte, gitignored, weil sie fremde Hooks zitieren |

🚨 **Wo dasselbe sonst noch steht:** Posting-Zeiten stehen in `context/reels-framework.md`, in den
Cockpit-Vorgaben (`patch-postzeit.py`: Reel 21:00, Karussell 07:30) und in CLAUDE.md („Posting-Zeiten“).
Die Uhrzeit-Auswertung ändert sie **nicht** von selbst. Wechseln würde sie erst nach Patricias Ja, und dann
an allen drei Stellen gleichzeitig.

## Offene Fragen an Patricia

1. Welche Konten kommen in den Radar? Mein Vorschlag sind dein Mentoring-Konto plus die Kern-Nische aus der
   Watchlist, also Julia Müller, reichweitenherz, Anna, Nikoleta, Fühlbarmacherin, Katrin Hill und Dascha.
2. Sollen auch Karussells ausgewertet werden, oder wie bei Content Radar nur Reels?
3. Was machen wir mit den restlichen 85 Credits, zum Beispiel einen letzten Lauf als Vergleich zum Nachbau?

**Kosten grob:** Apify wie bisher. Für Claude kosten 8 Konten × 15 Reels mit je drei Bildern pro Lauf im
niedrigen einstelligen Dollar-Bereich. Zweite Läufe kosten wegen des Caches nur die neuen Beiträge.
