---
tags: [basteln, recherche, tools]
---

# Shop- & Ideen-Recherche — was geht, was nicht

**Getestet am 2026-08-18.** Hier steht, wie ich zu einem Stempelset die Hersteller-Ideen dazuhole — und wo die Grenzen sind.

---

## ✅ Scrapbook Forever — funktioniert vollautomatisch

**Shop:** `scrapbookforever-shop.de` (epages) · Schweiz-Versand nur über Händler wie [bigtime.ch](https://bigtime.ch/de/181_scrapbook-forever) oder [Lilly-Art](https://www.lilly-art.ch)

**Der Schlüssel: die Artikelnummer** (`SF363`, `SF370` …) — steht auf der Set-Verpackung.

### Was ich pro Set bekomme
| Daten | Beispiel SF363 |
|---|---|
| Set-Name | SF Stamps Happy Birthday |
| Preis + Altpreis | 7,50 € (statt 15,50 €) |
| **Exakter Inhalt mit Massen** | „A6, 1 Textstempel (7,5 × 1,0 cm) + 7 Motivstempel (1,5 × 1,5 bis 6,5 × 9,5 cm)" |
| **Beispielkarten des Design-Teams** | 12 Bilder |

→ **Die Beispielkarten sind die Bastelideen, die du meinst.** Ich kann sie herunterladen, *ansehen* und die Technik beschreiben.

### Nutzung
```bash
node scripts/basteln/sf-lookup.mjs SF363
```
```bash
node scripts/basteln/sf-lookup.mjs SF363 SF370 SF353 --bilder
```
- ohne `--bilder`: Markdown-Block mit Bild-URLs
- mit `--bilder`: lädt die Beispielkarten nach `context/persoenlich/basteln-shopbilder/<SF-Nr>/` — **gitignored**, dann kann ich sie lesen und die Techniken ins Inventar schreiben

**Kategorien im Shop:** SF Stamps A6 (150 Sets!) · A7 · A8 · Lavinia · Der kleine Yogi · Stencil · Stanzen · Farben · Stifte · Papier und Folien

---

## ⚠️ Wichtige Einschränkung: ausgelistete Sets (gelernt 2026-08-18)

**Der Hersteller-Shop führt nur das aktuelle Sortiment.** Getestet: SF108–SF126 geben alle die Startseite zurück, die Geburtstag-Kategorie hat nur noch 6 Sets. Patricias älteres Sortiment ist dort nicht mehr auffindbar.

**Ohne Artikelnummer auf der Verpackung ist ein altes Set praktisch nicht identifizierbar.** Händler-Restposten ([stempelmuehle.de](https://www.stempelmuehle.de/Stempel-Zubehoer/Stempel-S-Z/Scrapbook-Forever-Stempel/) hat SF-Nummern in der URL, [bigtime.ch](https://bigtime.ch/de/181_scrapbook-forever), [vohaerze.com](https://www.vohaerze.com/stempel-scrapbook-forever)) sind die einzige Chance — lohnt aber nur bei Motiv-Sets.

**Die entscheidende Unterscheidung:**

| Set-Typ | Braucht Hersteller-Ideen? | Vorgehen |
|---|---|---|
| **Textstempel-Set** (nur Sprüche) | ❌ nein | Foto reicht. Ich lese die Sprüche und baue Projekte direkt auf ihr Material |
| **Motiv-Set** (zum Kolorieren) | ✅ ja, hilfreich | Beispielkarten zeigen Kolorier- und Aufbau-Technik → `sf-lookup.mjs`, wenn das Set noch im Shop ist |

→ **Bei Textstempeln nie Zeit mit Nummern-Suche verbrennen.** Foto ansehen, Sprüche notieren, Projekte bauen.

---

## 📅 Kalender-Sets — die eigentliche Erklärung (gefunden 2026-08-18)

> ### 🚫 REGEL: YouTube ist für Claude nicht lesbar
> **Geprüft 2.9.2026** mit einem Perfect-Pearls-Video: YouTube liefert an Claude nur die Seitenhülle (Footer, Rechtstexte) — **kein Titel, keine Beschreibung, kein Transkript.** Gilt für alle YouTube-Links, auch die SF-Kalender-Videos.
>
> **Arbeitsteilung:** Patricia schaut, Claude legt ab. Links sammeln in [[technik-quellen]]. Wenn etwas Behaltenswertes drin ist → Screenshot oder zwei Sätze an Claude, dann kommt es als Technik-Notiz ins Register.

> ### 🚫 REGEL: Kalender-Sets haben KEINE Artikelnummer
> **Bestätigt von Patricia am 2026-08-20.** Sets aus SF-Advents-, Sommer- oder Jahreskalendern waren nie einzeln im Shop und tragen deshalb keine Artikelnummer — auch dann nicht, wenn sie noch original in der SF-Hülle stecken.
>
> **Konsequenz für mich:**
> - **Nie nach der Artikelnummer fragen**, wenn ein Set aus einem Kalender stammt.
> - `sf-lookup.mjs` läuft dort ins Leere — nicht anbieten.
> - Im Register und in Notion als `keine — Kalender-Set, nicht im Shop erhältlich` eintragen.
> - Betrifft im Bestand mindestens `1086`–`1090`, vermutlich auch weitere SF-Sets ohne Nummer.
>
> **Was stattdessen geht:** Patricia schickt Screenshots aus der Facebook-Ideengruppe oder aus den YouTube-Tag-Videos, ich werte sie aus. Oder wir arbeiten mit den Layout-Rezepten aus dem Register.


**Viele von Patricias Sets stammen aus SF-Kalendern, nicht aus dem Shop-Sortiment.** Deshalb sind sie nirgends zu finden.

- **Adventskalender:** 24 A7-Sonder-Sets pro Kalender (Coloration-, Silhouette- und Textstempel)
- **Jahreskalender:** eigene Serie mit allgemeinen Lebenssprüchen
- **Erkennungsmerkmal:** Lagernummer `WO1D38…` auf der Verpackung statt einer `SF___`-Artikelnummer. A7-Format.
- **Im Shop:** die A7-Kategorie führt nur noch **1** Set (geprüft 2026-08-18) — die Kalender-Sets sind weg

### Die Ideen dazu gibt es auf YouTube
**Kanal:** [@scrapbookforever6137](https://www.youtube.com/@scrapbookforever6137) — Format „**Scrapbook Forever TV**"

Belegte Serien:
- „Scrapbook Forever TV **Adventskalender 2022** Tag 1…" ([Tag 1](https://www.youtube.com/watch?v=pCtIIqiFUUc), [Tag 10](https://www.youtube.com/watch?v=nlJ1DkgH5p0), [Tag 19](https://www.youtube.com/watch?v=Y8Q74V6Mhj0))
- „Scrapbook Forever TV **Jahreskalender 2023** Tag 01…" ([Tag 01](https://www.youtube.com/watch?v=Dj6nOoCutMI), [Tag 02](https://www.youtube.com/watch?v=Z-f9eUTcLk8))

Pro Türchen ein Video, in dem das Set vorgestellt und bebastelt wird. Zusätzlich lief der Kalender live in der **Facebook-Ideengruppe** (Mo–Fr 8:00), am Wochenende als Bildposts.

**Grenzen:** YouTube liefert Videotitel („Tag 10"), aber keine Set-Namen — eine automatische Zuordnung Spruch → Türchen ist damit nicht möglich. Und die Videos selbst kann ich nicht ansehen, nur Metadaten lesen. Die Kanal-Übersicht lädt per Lazy-Load + Cookie-Wall; **Consent-Banner klicke ich nicht ohne Patricias Zustimmung**.

### Patricias Kalender (von ihr bestätigt 2026-08-18)

| Kalender | Status | Alle Tag-Videos |
|---|---|---|
| **Adventskalender 2021** | ✅ sicher dabei | [Suche öffnen](https://www.youtube.com/results?search_query=Scrapbook+Forever+TV+Adventskalender+2021+Tag) |
| **Sommerkalender 2022 ‚Chill mal ab‘** | ✅ sicher dabei | [Suche öffnen](https://www.youtube.com/results?search_query=Scrapbook+Forever+TV+Chill+mal+ab+Tag) |
| **Adventskalender 2022** | 🤔 glaubt ja | [Suche öffnen](https://www.youtube.com/results?search_query=Scrapbook+Forever+TV+Adventskalender+2022+Tag) |
| Jahreskalender 2023 | ❓ unklar — aber Set 2 passt dazu | [Suche öffnen](https://www.youtube.com/results?search_query=Scrapbook+Forever+TV+Jahreskalender+2023+Tag) |

**Belegte Direkt-Links (Stichproben):**
- Adventskalender 2021: [Tag 01](https://www.youtube.com/watch?v=xWL07g9zN_Y) · [Tag 14](https://www.youtube.com/watch?v=4cNGkvFm83w) · [Tag 20](https://www.youtube.com/watch?v=wVfCB4W4psA) · [Tag 24](https://www.youtube.com/watch?v=SeGo1DeWv0k)
- Adventskalender 2022: [Tag 1](https://www.youtube.com/watch?v=pCtIIqiFUUc) · [Tag 10](https://www.youtube.com/watch?v=nlJ1DkgH5p0) · [Tag 19](https://www.youtube.com/watch?v=Y8Q74V6Mhj0)
- Jahreskalender 2023: [Tag 01](https://www.youtube.com/watch?v=Dj6nOoCutMI) · [Tag 02](https://www.youtube.com/watch?v=Z-f9eUTcLk8)
- Sommerkalender-Ankündigung: [‚Chill mal ab‘ + Märzneuheiten](https://www.youtube.com/watch?v=5dJocrK7KEw)

**Vermuteter Zusammenhang:** Die 109 Dateien in `Digistamps/Elemente-Chillkröten` stammen wahrscheinlich aus dem Sommerkalender ‚Chill mal ab‘ — Name und Thema passen. Nicht bestätigt.

**Warum keine vollständige 24er-Liste:** YouTube zeigt pro Suche nur eine Auswahl und lädt den Rest per Lazy-Load, der in dieser Umgebung nicht greift. Die Kanal-Playlist-Seite steckt hinter einer Cookie-Wall, die ich nicht ohne Patricias Zustimmung wegklicke. Die Suchlinks oben sind der zuverlässige Weg — ein Klick, alle Tage der Serie.

### ❌ Getestet und gescheitert: Sets ueber die Videos identifizieren (2026-08-18)

Damit das niemand nochmal versucht — diese Wege sind tot:

| Versuch | Ergebnis |
|---|---|
| Video-Beschreibungen lesen | leer / laedt nicht |
| Videotitel auswerten | nur ‚Tag 10‘ — kein Set-Name |
| **Thumbnails ansehen** | 9 heruntergeladen und geprueft: zeigen **Arbeitsschritte**, keine Set-Uebersichten (z.B. Jahreskalender 2023 Tag 01 = Falzvorgang dunkelblaues Papier; Advent 2021 Tag 14 = Osterkoerbchen auf dem Envelope Punchboard) |
| Videos selbst ansehen | nicht moeglich — keine Videoanalyse |
| Kanal-Playlists | Cookie-Wall, wird nicht ohne Patricias Zustimmung geklickt |

**Fazit:** Eine automatische Zuordnung Spruch → Tuerchen gibt es nicht. Entweder Patricia sucht selbst per Klickliste, oder — besser — wir ueberspringen es: die Spruechefotos genuegen fuer Projektideen.

**Nebenfund mit Wert:** Das **Envelope Punchboard kann Koerbchen** (Advent 2021 Tag 14 zeigt genau das). Patricia hat eins — also eine Technik, die sie sofort kann.

**Für Textstempel-Sets ist das ohnehin unnötig** (siehe Tabelle oben): Foto reicht, ich lese die Sprüche.

---

## 🟡 Mundart Stempel — geht, aber ohne Automatik

**Shop:** [mundartstempel.ch](https://www.mundartstempel.ch/de/) (Gambio) — Schweizer Laden, geführt von zwei Schwestern

- **URL-Muster:** `mundartstempel.ch/de/<ID>.html` (z.B. `/de/28445.html` = Holzstempel Möwe Broder)
- **Kein Artikelnummern-System wie bei SF** → ich kann nicht von der Verpackung auf die URL schliessen
- **Aber:** der Shop hat eine eigene Kategorie **„Anleitungen"** — dort liegen ihre Bastelideen
- **Weg:** du schickst mir ein Foto → ich suche im Shop nach dem Namen → hole Beschreibung + Bilder

→ Kein Skript, weil das Nummern-Mapping fehlt. Bei Bedarf baue ich einen Suchwort-Lookup.

---

## ❌ Facebook-Gruppe „Scrapbook Forever Ideen" — nicht durchsuchbar

**Ehrliche Antwort: nein, das kann ich nicht.** Drei Gründe:

1. **Login-Wall.** Gruppen-Inhalte sind für nicht eingeloggte Zugriffe unsichtbar. Weder mein interner Browser noch `curl` kommen rein.
2. **Keine Chrome-Verbindung.** Es *gäbe* einen Weg — die „Claude in Chrome"-Erweiterung würde deinen eingeloggten Browser nutzen. Geprüft: aktuell **kein Chrome verbunden**.
3. **Selbst mit Zugang würde ich es nicht massenhaft tun.** Automatisiertes Abgrasen einer Gruppe verstösst gegen Facebooks Regeln, und die Posts gehören anderen Bastlerinnen — deren Fotos landen nicht in deinem Archiv, schon gar nicht in einem öffentlichen Repo.

### Was stattdessen funktioniert — und zwar sofort

**Screenshot-Weg (empfohlen):**
1. Du siehst in der Gruppe eine Idee, die dich packt → Screenshot
2. Ab in einen Ordner (z.B. OneDrive `Basteln/Ideen-FB/`) oder direkt an mich
3. Ich lese das Bild aus, beschreibe die Technik, prüfe gegen dein Inventar und trage's in [[projekt-ideen]] ein

Das ist nicht mal umständlicher — du musst die Idee ja sowieso erst gut finden. Und **ich beschreibe die Technik in Worten**, statt fremde Fotos zu sammeln: „Aquarell-Hintergrund, Motiv gestanzt, mit Foam-Pads erhöht" ist für dich beim Nachbauen brauchbarer als das Bild allein.

**Facebooks „Gespeicherte Beiträge"** als Sammelstelle nutzen und wir gehen sie gemeinsam durch, wenn du Zeit hast.

---

## ⚖️ Urheberrecht — meine Regel

| Was | Wohin |
|---|---|
| Shop-Beschreibungen, Set-Inhalte, Masse | ✅ ins Inventar (Fakten) |
| Links zu Hersteller-Seiten | ✅ ins Inventar |
| **Meine** Beschreibung einer Technik | ✅ ins Inventar |
| Fremde Produktfotos & Beispielkarten | 🔒 nur `context/persoenlich/` (gitignored) |
| Posts anderer Bastlerinnen 1:1 | ❌ gar nicht |

**Warum so streng:** Dieses Repo ist öffentlich. Fremde Bastelfotos darin wären ein echtes Problem — und zwar deins, nicht meins.

---

## 🔗 Verwandte Notizen
- [[inventar-physisch]] — hier landen die erfassten Sets
- [[projekt-ideen]] — hier landen die ausgewerteten Ideen
- [[README]]
