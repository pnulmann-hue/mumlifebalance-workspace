---
name: videoschnitt
description: "Rohmaterial einmal in die Kamera sprechen, Claude macht den Rest: Schnitt nach meinen Regeln, CapCut-Projekt zum Nachziehen, aus meinen Korrekturen lernen, Hook/Untertitel/Animationen mit Ton, fertiges MP4. Dran bei /videoschnitt, „schneide mein Video“, „ich hab in CapCut nachjustiert“, „Bau mein Video fertig“."
---
## ⏱ Warum eine Runde 40 Minuten dauerte — und was sie kuerzt (16.09.2026)

*„wie können wir das optimieren, dass wir nicht für jedes video 40 min brauchen?"*

Die Zeit ging nicht ins Schneiden. Sie ging in die **Schleife**: Patricia hoert rein,
es klingt hart, Claude raet, baut neu, sie hoert wieder rein. Drei Sachen nehmen die
Schleife strukturell weg — alle automatisch, keine davon braucht ein Urteil:

1. **Ton-Blende an jeder Schnittkante** (40 ms rein und raus). Ein harter Schnitt setzt
   die Wellenform mitten in der Schwingung ab; das knackt, egal wie sauber die
   Wortgrenze liegt. Das war der groesste Teil dessen, was „scheisse" klang.
2. **Pegel ueber das ganze Stueck angleichen** (`loudnorm`), nicht je Abschnitt —
   sonst hebt ffmpeg einen leisen Abschnitt auf dasselbe Niveau wie einen lauten,
   und genau dann springt es beim Schnitt.
3. **EINE Datei zum Reinhoeren** (`rohschnitt.mp4`), nicht zehn. Sie hoert einmal durch
   und sagt eine Nummer. Dieselbe Datei zieht sie in CapCut, wenn sie ziehen will.

🚨 **CapCut NICHT ueber den Bildschirm steuern.** Am 16.09. wurde versucht, die
Abschnitte per Maus und Tastatur in CapCut zu importieren: Tutorial wegklicken,
Dateidialog, Pfad tippen — der Dialog nahm den Pfad nicht, mehrere Anlaeufe, nichts
gewonnen. **Das ist genau der 40-Minuten-Weg.** Entweder die Datei liegt fertig da und
sie zieht sie einmal rein, oder es laeuft ohne CapCut. Klick-Automatisierung in einer
fremden Oberflaeche ist nie die Abkuerzung.

🚨 **`afade=t=out` ist hier eine Falle.** `-ss` steht hinter `-i` (genaue Suche, sonst
findet Remotions Compositor keine Bilder), und dabei behaelt der Tonstrom seine
ORIGINAL-Zeitstempel. Ein `afade=t=out:st=1.7` auf einem Strom, der bei Sekunde 65
beginnt, ist laengst vorbei — das Ergebnis waren **zehn komplett stumme Dateien**.
`asetpts=PTS-STARTPTS` davor hat nicht geholfen. Was funktioniert:

```
afade=t=in:st=0:d=0.04,areverse,afade=t=in:st=0:d=0.04,areverse
```

Umdrehen, einblenden, zurueckdrehen — rechnet in Samples statt in Zeitstempeln.
**Gefunden wurde das nur, weil nach dem Bauen gemessen wurde.** Ohne die Messung waere
ein stummes Video rausgegangen, und die naechste Runde haette wieder 40 Minuten
gekostet. Nach jedem Tonfilter: Anfang, **Mitte** und Ende messen — die Mitte faengt
genau den Fall, wo ein Filter alles wegdreht.

---

## 🦋 Aus Jenyas Kurs „Dein Videoeditor ist Claude" (eingearbeitet 06.10.2026)

Der Kurs (4 Videos, Stan Store) baut auf ihrem PDF-Guide auf, der hier schon
steckte. **Neu** waren drei Dinge — alle drei sind jetzt eingebaut:

**1 · Der Rohschnitt kommt als fertiges CapCut-Projekt**, nicht als Clip-Haufen.

```bash
python scripts/videoschnitt/capcut-projekt.py anlegen video/transkripte/<slug>/cutlist.json
```

Legt in CapCut ein Projekt „Rohschnitt MM-TT <slug>" an: ein Stück je Abschnitt,
alle auf **dem Originalvideo** — darum lässt sich jede Kante in **beide** Richtungen
aufziehen (bei `clips/NN.mp4` ist hinter der Kante nichts mehr). Die Luft kommt aus
`schnitt.py`, nicht aus einer zweiten Rechnung.
🚨 **CapCut muss dabei geschlossen sein** — sonst schreibt es beim Beenden seine
Projektliste zurück und das neue Projekt verschwindet. Das Skript prüft das und bricht ab.
🚨 Vorlage ist ihr **jüngstes eigenes CapCut-Projekt mit Video** (nur gelesen). Im Repo
liegt bewusst keine, weil die Projektdateien Geräte-Kennungen tragen. Die
Projektliste wird vorher nach `root_meta_info.json.vor-claude` gesichert.
Getestet 06.10.2026 mit CapCut 9.5: Format ist lesbares JSON, Zeiten in Mikrosekunden.

**2 · Claude lernt aus ihren CapCut-Korrekturen** (Jenyas Prompt 4):

```bash
python scripts/videoschnitt/capcut-projekt.py vergleichen video/transkripte/<slug>/cutlist.json
```

Nachdem sie CapCut **ganz beendet** hat: Liste, was sie geändert hat (gelöscht ·
Kante länger/kürzer um wie viel · Stelle mitten raus, mit dem Wortlaut · Pause
eingefügt · Reihenfolge) → `capcut-korrekturen.md`. **Regelvorschlag erst ab zwei
gleichen Änderungen**, mit dem Median. **Eingetragen in `videoschnitt-regeln.md` wird
erst nach ihrem Ja.** Das ersetzt das „ich sag's dir beim dritten Mal" — sie muss
nichts mehr erklären, die Projektdatei sagt es.

Danach geht es wie gehabt weiter: Export aus CapCut → `aus-capcut.py` (transkribiert
den Export neu) → Gestaltung.

**3 · Stil aus mehreren Vorbild-Videos ableiten** — siehe Schritt 5d unten.

**So sagt Patricia es — Jenyas Prompts als kurze Sätze** (die lange Fassung steckt hier im Skill):

| Sie sagt | Claude macht | Jenyas Prompt |
|---|---|---|
| „Video liegt drin, schneide es" | transkribieren → Schnittliste zeigen → nach OK `schnitt.py` + `capcut-projekt.py anlegen` | 3 |
| „Ich hab in CapCut nachjustiert, schau was ich geändert hab" | `capcut-projekt.py vergleichen` → Liste + Regelvorschläge, eintragen erst nach Ja | 4 |
| „Export liegt drin, bau mein Video fertig" | `aus-capcut.py` → `grafik.json` → `vorschau.py` (A/B/C zeigen) → nach Wahl `--rendern` | 6, 7, Schluss |
| „Bei Sekunde 12 …" | nur diese Stelle ändern, Standbild zeigen | Feedback |
| „Analysier den Stil in video/inspo" | Schritt 5d | Stil-Prompts |

**Eigene Sounds:** `video/sounds/` — erkannt am Wort im Dateinamen (`pop` · `intro` ·
`typing`/`keyboard` · `woosh`/`whoosh`), umbenennen nicht nötig. Seit 06.10.2026 liegen dort
Patricias vier Pixabay-Klänge. Wann welcher kommt: `context/videoschnitt-regeln.md`, „Meine Töne“. **Vorbilder für den Stil:** `video/inspo/` (Screenshots,
Pinterest-Bilder, 3–5 Reels einer Creatorin). Beide Ordner sind gitignored.

**Kleiner, aber übernommen:**
- **Whisper `large-v3-turbo`** ist jetzt Standard: fast so genau wie large-v3, etwa so
  schnell wie medium. Erster Lauf lädt ~1.6 GB. Für einen schnellen Durchlauf `--modell small`.
- **Modellwahl:** Planen, Regeln, Stil → Opus. Den Rohschnitt selbst kann Sonnet
  (spart Tokens). Umstellen unten beim Eingabefeld.
- **Ist der Schnitt eingespielt, geht Kleinkram direkt im Chat:** „Die Stelle über
  [Thema] hast du zu früh abgeschnitten, lass eine halbe Sekunde mehr stehen. Schneide
  neu und trag das als Regel ein." Dann ohne CapCut-Runde.
- **Fehlermeldung einfach reinkopieren:** „Das kommt gerade: […]. Was ist das und was
  machen wir?"

- **Ihre Schnitt-Zahlen gelten seit 06.10.2026** (Patricia: *„sie ist ja der Profi“*):
  0,12 s vor / 0,35 s nach, Pausen im Abschnitt auf 0,3 s gekürzt (`pausen_kappen` in
  `schnitt.py`, auch im CapCut-Projekt). Whisper-Standard ist jetzt `large-v3-turbo`.

**Bewusst nicht übernommen:**
- Ihr **„Sounds"-Ordner mit heruntergeladenen Klängen** als Pflicht — hier erzeugt
  `textebene.py` die Töne mit ffmpeg (keine Lizenzfrage). Will Patricia eigene Klänge:
  `video/sounds/` anlegen, Lizenz je Datei prüfen (Pixabay, Mixkit, Freesound, Uppbeat),
  dieselben fünf bis zehn durch alle Videos.
- Den **offiziellen Remotion-Skill** (`npx skills add remotion-dev/skills`) — hier
  läuft schon `remotion-motion-graphics`; zwei Skills für dieselbe Arbeit wären
  genau das Durcheinander, das die Skill-Ablage verhindern soll.

---

## 🎬 Der Feinschnitt gehoert Patricia — ueber CapCut (16.09.2026)

*„machst du das ueber capcut? weil dann muss ich nicht wegen jedem pups wieder
schreiben, sondern kann die schnittbalken selber nachjustieren. das empfiehlt ja
auch jey.."*

**Claude kann den Ton nicht hoeren.** Jede Runde „klingt das jetzt gut?" kostet sie
eine Nachricht und bringt ein Ergebnis, das Claude nicht beurteilen kann. Deshalb:

| Schritt | Wer |
|---|---|
| Abschnitte auswaehlen und schneiden | **Claude** (`kurzfassung.py`) |
| **Schnittkanten fein ziehen, bis es klingt** | **Patricia, in CapCut** |
| Textebene, Untertitel, Zoom, Einblendungen | **Claude** (`aus-capcut.py` + Remotion) |

```bash
python scripts/videoschnitt/aus-capcut.py --export video/input/<export>.mp4 --projekt video/output/<projekt>
```

🚨 **Das Skript transkribiert den Export NEU, statt Zeiten umzurechnen.** Verschiebt
sie einen Balken, stimmen die alten Wort-Zeitstempel nicht mehr — Umrechnen hiesse
raten, wo sie was gezogen hat. Eine Minute faster-whisper ist billiger als eine
Textebene, die neben dem Wort sitzt.

**Was Claude ihr mitgeben muss**, sonst kann sie nicht loslegen:
1. Die Abschnitte einzeln in `clips/`, durchnummeriert in Abspielreihenfolge
2. Eine `CAPCUT.md` im Projekt: Tabelle mit Nummer, Winkel und gesprochenem Satz
3. Den fertigen Befehl fuer Schritt 4 zum Kopieren
4. Den Hinweis **„in CapCut nur schneiden"** — keine Untertitel, keine Effekte,
   kein Text, kein Zoom. Das doppelt sich sonst mit der Textebene.

Die Abschnitte bekommen **gesuchte Luft** vorne (`kurzfassung.py` geht vom
Satzanfang rueckwaerts bis zur Stille, hoechstens 0.6 s) — damit hat sie Material
zum Ziehen in beide Richtungen. Eine feste Zahl schnitt sonst ins Einatmen.

**Der Weg ohne CapCut bleibt:** `schnittliste.md` im Projekt, eine Tabelle mit
`von`/`bis` in Sekunden, die sie aendert und neu bauen laesst.

---

## 🚦 Arbeitsteilung (Patricias Entscheid 15.09.2026)

| Ebene | Wer macht es |
|---|---|
| **Konzept, Hook, Sprechtext, Caption** | `/reels` |
| **Schnitt** — Transkript, Take-Auswahl, Rohschnitt, Clips | **dieser Skill** (`transkribieren.py`, `schnitt.py`) |
| **Gestaltung** — Textebene, Untertitel, Zoom, Animationen | **`remotion-motion-graphics`** ← neuer Standard |

**Seit 06.10.2026 läuft die Gestaltung über den festen Ordner `scripts/grafik/`**
(Jenyas Teil 4): Varianten A/B/C als Standbild → Wahl → bewegt. Ablauf im
Skill `remotion-motion-graphics`, oberster Block.

**`textebene.py` (HyperFrames) ist ab jetzt Altbestand.** Es bleibt lauffaehig,
solange Remotion den Kelsie-Stil nicht kann — ein funktionierendes Werkzeug wird
nicht abgeschaltet, bevor der Ersatz steht. Aber: **neue Gestaltungsarbeit wird in
Remotion gebaut, nicht in textebene.py.**

### Was in Remotion noch nachgebaut werden muss

- [ ] **Kelsie-Textebene** — zwei Zeilen auf Stoss, Poppins Light klein oben /
      Bold gross unten, durchscheinend mit Farbverlauf, Einblendung startet auf dem
      gesprochenen Wort, grosses Wort **hinter** Patricia (Freistellung noetig)
- [ ] **Wortgenaue Untertitel** — aktives Wort orange, weichen Einblendungen aus
- [ ] **Auto-Zoom** — jeder zweite Clip Fahrt hinein, dazwischen harter Sprung
- [ ] **Freistellung der Person** (bisher `npx hyperframes remove-background`)

Solange ein Punkt offen ist, laeuft dieser Teil weiter ueber `textebene.py`.
Abgehakt wird erst, wenn Patricia das Ergebnis gesehen und freigegeben hat.

🚨 **Und der Grund fuer die Umstellung — Regel 10 des Remotion-Skills:**
*rendern, Standbilder ziehen, hinschauen, korrigieren, neu rendern. Nie einen
ungeprueften Render abgeben.* Genau diese Schleife hat gefehlt. Am 14.09. ging ein
Reel raus mit 8 Sekunden unveraendertem cremefarbenem Text auf hellem Gras, unten
im Bild — gegen drei eigene Regeln, und niemand hat hingeschaut.

---

Du bist mein Videoeditor. Ich spreche mein Rohmaterial **in einem Stück in die
Kamera**, mit Versprechern und mit Sätzen, die ich mehrmals sage. Du machst
daraus einen sauberen Rohschnitt — nach **meinen Regeln**, nicht nach deinem
Geschmack.

## Zuerst lesen (Pflicht)

- `context/videoschnitt-regeln.md` — **die Regeln.** Take-Regel, was rausfliegt,
  was bleibt, wie eng geschnitten wird, die Selbstprüfung. Bei Konflikt gewinnt diese Datei.
- `context/reels-framework.md` — Reel-Typen, 3-Sekunden-Regel, Ziellängen
- `.claude/skills/hooks/SKILL.md` — der Hook-Master (Kundensprache, Stufen, Angles, PIE, Formeln, Verbote, letzter Check)
- `context/patricia-freebies.md` — die Keywords, mit denen meine Videos enden
- **Bei doTERRA:** `context/doterra/patricia-wendepunkt-story.md` + Compliance
  (keine Heilversprechen, „bei mir war"-Frame)

Frag mich am Anfang, falls unklar: **welches Profil** (Mentoring / doTERRA),
**welcher Reel-Typ**, und ob ich das **Skript** habe (mit Skript wird der Schnitt
deutlich besser, weil du weisst, welche Sätze überhaupt vorkommen sollen).

---

## Der Ablauf

### Schritt 1 · Transkribieren

Ich lege mein Rohvideo in `video/input/`. Dann:

```bash
python scripts/videoschnitt/transkribieren.py
```

Ohne Argument nimmt es das neueste Video im Ordner. Läuft lokal (faster-whisper,
CPU) — nichts wird hochgeladen, nichts kostet etwas. Ein 5-Minuten-Video braucht
grob 3–6 Minuten. Für einen schnellen Durchlauf: `--modell small`.

Es entsteht `video/transkripte/<slug>/` mit:
- `saetze.md` — **das liest du**: jeder Satz nummeriert, mit Zeitstempel, Pause
  davor und Take-Gruppe. Doppelte Anläufe sind bereits als `WEG` markiert.
- `words.json` — jedes Wort mit Zeitstempel (Basis für wortgenaue Schnitte)
- `cutlist-vorschlag.json` — ein erster Vorschlag nach der Take-Regel
- `transkript.srt` / `.txt`

### Schritt 2 · Schnittliste vorlegen (Pflicht, nicht überspringen)

Du liest `saetze.md`, wendest `context/videoschnitt-regeln.md` an und legst mir
die Schnittliste **als Text** vor, bevor irgendetwas gerendert wird:

- Welche Sätze drinbleiben, in welcher Reihenfolge
- Was rausfliegt und **warum** (Doppel-Take, Abbruch, Füllwort, zu lange Pause)
- Die erwartete Länge des Rohschnitts
- Der Hook wortwörtlich, damit ich sehe, dass er unangetastet ist

Der automatische Vorschlag ist ein Vorschlag, kein Urteil. Prüfe ihn:
- Hat die Automatik einen Take erwischt, der inhaltlich besser war als der letzte?
- Wurde eine bewusste Wiederholung (Stilmittel) fälschlich als Doppelung erkannt?
- Ist der CTA am Schluss vollständig, inklusive Keyword?

Ich sage „passt" oder korrigiere. Erst dann:

### Schritt 3 · Schneiden

Schreib die freigegebene Liste als `cutlist.json` neben das Transkript
(gleiches Format wie `cutlist-vorschlag.json`, Feld `segmente` mit
`start`/`ende`/`text`) und lauf:

```bash
python scripts/videoschnitt/schnitt.py video/transkripte/<slug>/cutlist.json
```

Ergebnis in `video/output/YYYY-MM-DD-<slug>/`:
- `rohschnitt.mp4` — zum Anschauen
- `clips/01.mp4, 02.mp4 …` — **alle markieren, in CapCut ziehen**, CapCut
  sortiert nach Dateiname
- `untertitel.srt` — auf den Schnitt umgerechnet
- `words-schnitt.json` — Wort-Zeitstempel auf der neuen Zeitachse
- `schnittprotokoll.md` — was drin ist, was rausflog

**Will sie selbst nachziehen, gleich danach das CapCut-Projekt anlegen**
(`capcut-projekt.py anlegen`, siehe Jenya-Block oben) — das ist bequemer als
`clips/` reinzuziehen, und nur so lassen sich ihre Korrekturen danach auslesen.

**Jede Version bleibt als eigener Ordner stehen.** Es kommt der Moment, in dem
die dritte Fassung schlechter ist als die zweite — dann will ich zurück können.

### Schritt 4 · Mein Feinschliff in CapCut (optional)

**Nur wenn ich will.** Schritt 5 liefert ein fertiges, postbares Video — CapCut
brauche ich nur, wenn ich noch von Hand ran will: knappe Clipenden aufziehen,
hakelige Übergänge mit einer Mini-Pause entschärfen, die ersten zwei Sekunden
separat prüfen.

**Was ich dir sage und was ich selbst mache:** In den Chat kommt nur, was ich mir
beim *nächsten* Video sparen will. Wenn ich dieselbe Sache **dreimal** von Hand
korrigiert habe, ist das keine Kleinigkeit mehr — dann trag es als Regel in
`context/videoschnitt-regeln.md` ein. Einmalige Sachen mache ich selbst.

### Schritt 5 · Das Finish — Zoom, Untertitel, Textebene

Hier entsteht das fertige Video. Alles in einer Datei (`finish.json`), alles in
einem Render.

**Zoom.** `"zoom": {"modus": "auto", "staerke": 1.07}` — jeder zweite Clip
bekommt eine langsame Fahrt hinein, dazwischen ein harter Sprung auf eine engere
Einstellung. Durchgehend zoomen wirkt seekrank, gar nicht zoomen wirkt statisch.
Für gezielte Betonungen `"modus": "manuell"` mit `abschnitte`.

**Untertitel.** `"untertitel": {"an": true}` — wortgenau, max. 4 Wörter pro
Zeile, das gerade gesprochene Wort in Orange. Sie pausieren automatisch,
solange eine Einblendung steht. **Prüf den Text:** Whisper schreibt Schweizer
Ausdrücke und Produktnamen gern falsch, und ein falsches Wort im Untertitel
fällt jedem auf.

**Die Textebene** — mein Stil, verbindlich:

- **Zwei Zeilen:** oben dünn und klein (Poppins Light), darunter das betonte Wort
  gross und durchscheinend, mit **Farbverlauf im Buchstaben**
- Die zwei Zeilen sitzen **fast auf Stoss**, kein Zeilenabstand
- Jede Einblendung erscheint **auf dem Wort, das ich gerade sage**
- Das **grosse Wort liegt hinter mir**, die kleine Zeile davor
- Auftritt **abwechselnd**: von links, von rechts, aufgepoppt

Du schreibst eine `finish.json` (Format steht im Kopf von `textebene.py`) und
lässt sie bauen:

```bash
python scripts/videoschnitt/textebene.py video/output/<ordner>/finish.json --pruefen
python scripts/videoschnitt/textebene.py video/output/<ordner>/finish.json --rendern
```

`--pruefen` läuft `hyperframes check` (Lint, Runtime, Layout, Motion, Kontrast).
**Erst prüfen, dann rendern** — der Check fängt Überlappungen, unlesbare
Kontraste und kaputte Animationen ab, bevor du Minuten in einen Render steckst.
Das fertige MP4 landet in `finish/renders/`.

Für „das grosse Wort **hinter mir**" braucht es mich freigestellt — einmalig:

```bash
npx hyperframes remove-background video/output/<ordner>/rohschnitt.mp4
```

Das Ergebnis als `person_alpha` in die `textebene.json` eintragen. Ohne diesen
Schritt liegt der Text **vor** mir statt dahinter — sag mir das dann auch, statt
so zu tun, als wäre es dasselbe.

**Wortwahl der Einblendungen:** Das grosse Wort ist das **betonte** Wort des
Satzes, nicht irgendeins. Die kleine Zeile führt darauf hin und ergänzt es —
sie wiederholt es nicht. Zusammen gelesen ergeben beide Zeilen einen Satz.
Kurze Wörter wirken; ab etwa 12 Zeichen schrumpft die Schrift automatisch,
das sieht schwächer aus — dann lieber ein kürzeres Wort wählen.

### Schritt 5b · Freie Animationen — die vier Fragen

Für alles, was **nicht** der Kelsie-Baustein ist (ein pulsierender
Aufnahmepunkt, ein Glas-Kästchen, ein eingeflogener Hinweis), frag mich
**diese vier Sachen** — und zwar alle vier. „Mach eine schöne Animation dazu"
ergibt etwas, das aussieht wie aus einer Vorlage.

1. **Wie sieht das Element aus?** Form, Farbe, Rand, Transparenz.
   → `typ` (`punkt` / `chip` / `notiz`) · `farbe` · `flaeche`
   (`glas` / `voll` / `keine`) · `kursiv` · `groesse`
2. **Wie bewegt es sich?** „Pulsierender Aufnahmepunkt" ist eine Anweisung,
   „animiert" ist keine. → `bewegung`: `pulsieren` / `links` / `rechts` /
   `pop` / `hoch` / `keine`
3. **An welcher Stelle taucht es auf?** **Den Satz nennen, nicht die Sekunde.**
   → `ab_wort` (das Element erscheint auf diesem gesprochenen Wort)
4. **Welcher Sound gehört dazu?** Ohne Angabe kommt keiner.
   → `sound`: `klick` / `pop` / `whoosh` / `ding` / `keiner`.
   Die Sounds werden mit ffmpeg erzeugt, nicht heruntergeladen — keine
   Lizenzfragen, keine fehlenden Dateien.

Wenn sie auf ein Vorbild-Video zeigt, ist das mehr wert als jede Beschreibung —
frag danach.

### Schritt 5c · Erst Konzept zeigen, dann bauen

**Vor** dem Render:

```bash
python scripts/videoschnitt/textebene.py <spec> --konzept
```

Das legt Standbilder über ihrem **echten** Material in `finish/konzept/` ab —
genau an den Stellen, wo die Elemente auftauchen. Schau sie dir selbst an
(Gesicht frei? Hauptmotiv frei? sitzt es an der richtigen Stelle?), zeig sie
ihr, und erst wenn sie passt, rendere. Ein Render dauert Minuten, ein
Standbild Sekunden.

### Schritt 5d · Stil aus Vorbildern ableiten (Jenya, Teil 4)

Wenn Patricia einen neuen Look will oder auf eine Creatorin zeigt:

- **Drei bis fünf Videos**, nie eins — sonst lässt sich Stil nicht von Zufall
  trennen. Ablage `nachbau/<datum>-stil-<name>/` (gitignored, fremdes Material).
  Laden über `scripts/nachbau/zerlegen.py` oder Bildschirmaufnahme.
- **Messen, nicht schätzen:** wo sich etwas bewegt, mindestens **vier Bilder je
  Sekunde** ziehen (`ffmpeg -vf fps=4`). Je Einblendung festhalten: wann sie kommt
  und wie lange sie steht · wie sie erscheint und verschwindet, wie schnell · wo im
  Bild, wie gross im Verhältnis zur Bildbreite, vor oder hinter der Person · Schrift,
  Farben mit Code, Formen, Schatten, Durchsichtigkeit · Ton dazu · Schnitt- und Zoomtakt.
- **Vergleichen:** in jedem Video gleich = **der Stil** · nur einmal = **Zufall** ·
  die drei bis fünf Merkmale, an denen man ihn sofort erkennt.
- Ergebnis als `stil-analyse.md` (Tabelle je Video + Zusammenfassung), dann
  **in Patricias Marke übersetzen** (Philosopher + Source Sans 3, Petrol/Dunkelblau/
  Creme/Orange) und fragen, was sie übernehmen will. **Anpassen, nicht kopieren.**
- Für Bewegung braucht es ein **Video** als Referenz — ein Bild zeigt nicht, wie sich
  etwas bewegt.
- Was sie freigibt, wird ein **wiederverwendbarer Baustein** mit Namen und Zweck
  (Jenya: „Damit du es nie wieder erklären musst").

---

## Der schnelle Weg: Submagic

Wenn es **nicht** meinem Regelwerk folgen muss, sondern nur schnell gehen soll,
geht es auch über Submagic (MCP ist verbunden): `removeBadTakes` +
`removeSilencePace` + Untertitel + Magic Zooms in einem Aufruf.

**Wann welcher Weg:**

| | lokal (Schritte 1–5) | Submagic |
|---|---|---|
| Meine Regeln (Hook wortwörtlich, letzter Take, Luft und Pausen) | ja, exakt | nein, Blackbox |
| Kosten | keine | Credits pro Render |
| Video muss hochgeladen werden | nein | ja, braucht eine öffentliche URL |
| Untertitel, Zooms, B-Roll, direkt posten | nein | ja |
| Einzelclips für CapCut | ja | nein |

**Beides kombiniert ist oft das Beste:** lokal nach meinen Regeln schneiden,
das Ergebnis dann für Untertitel/Zooms/Posting durch Submagic schicken.
Der Upload braucht eine öffentliche URL — Google Drive geht (Drive-MCP ist
verbunden), Freigabe-Link erzeugen und den an Submagic geben.
**Frag mich vorher**, bevor du etwas hochlädst oder einen Render startest, der
Credits kostet.

---

## Harte Regeln

- **Nie mitten in ein Wort schneiden** — immer an Wortgrenzen aus `words.json`.
- **Der Hook bleibt wortwörtlich.** Auch wenn er holprig klingt. Er ist vorher
  geschrieben und geübt.
- **Keine erfundenen Zeitstempel.** Jeder Schnittpunkt stammt aus dem Transkript.
- **Keine Rohschnitte ausliefern, die die Selbstprüfung aus den Regeln nicht
  bestehen** (Abschnitt 6 in `context/videoschnitt-regeln.md`). Ich soll nicht
  das Qualitätsmanagement für dich machen.
- **Nichts hochladen ohne mein OK.** Weder zu Submagic noch zu Drive noch sonst wohin.
- `video/**` ist gitignored. Mein Rohmaterial gehört nicht in ein öffentliches Repo —
  auch nicht „nur das Transkript".
- Wenn etwas nicht geht, sag es. Kein „ist gerendert", wenn nur die HTML-Datei da liegt.

## Wenn es hakt

| Symptom | Ursache | Fix |
|---|---|---|
| Der Schnitt wirft die falschen Stellen raus | Eine Regel ist zu ungenau formuliert | In `videoschnitt-regeln.md` nachschärfen. „Nimm die beste Version" ist keine Regel, „die letzte vollständige gewinnt" ist eine. |
| Es klingt gehetzt | Zu eng geschnitten | `pause_max` in der cutlist erhöhen (0.3 → 0.45) oder `padding_vor` (0.12 → 0.2) |
| Endsilbe abgeschnitten | Whisper setzt das Wortende zu früh | `padding_nach` auf 0.5 (Jenya) |
| Doppel-Takes werden nicht erkannt | Ich habe zwischen den Anläufen nicht neu angesetzt | Anlauf-Erkennung in `transkribieren.py` (`PAUSE_GRENZE`, `AEHNLICHKEIT`) anpassen |
| Transkript versteht mich schlecht | Modell zu klein oder Ton zu leise | `--modell large-v3-turbo` (oder `large-v3`), oder näher ans Mikro |
| CapCut findet das Video nicht | Datei verschoben oder umbenannt | in CapCut einmal „Medien verknüpfen" und das Video wählen |
| Neues CapCut-Projekt fehlt in der Liste | CapCut lief beim Anlegen | CapCut ganz beenden, `capcut-projekt.py anlegen` mit neuem `--name` nochmal |
| Einblendung sitzt auf dem falschen Wort | `words-schnitt.json` fehlt oder ist vom Rohmaterial statt vom Schnitt | `schnitt.py` neu laufen lassen, `words` in der textebene.json prüfen |
