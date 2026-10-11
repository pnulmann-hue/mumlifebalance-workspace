# scripts/videoschnitt — die Schnitt-Pipeline

Drei Skripte. Alles läuft lokal, nichts wird hochgeladen, nichts kostet etwas.
Gesteuert wird die Pipeline über den Skill `/videoschnitt`
(`.claude/commands/videoschnitt.md`), die Regeln stehen in
`context/videoschnitt-regeln.md`.

## Voraussetzungen

Alles bereits installiert (Stand 2026-09-10):

| | Zweck | Prüfen mit |
|---|---|---|
| **ffmpeg / ffprobe** | schneiden, zusammenfügen, Audio extrahieren | `ffmpeg -version` |
| **faster-whisper** (Python) | Transkript mit Wort-Zeitstempeln | `python -c "import faster_whisper"` |
| **Node 18+** | HyperFrames für die Textebene | `node -v` |
| **CapCut Desktop** | Feinschliff | — |

Whisper-Modelle liegen im Cache unter `~/.cache/huggingface/hub`
(`small` und `medium` sind da). `large-v3` wird beim ersten Aufruf geladen.

---

## 1 · `transkribieren.py`

```bash
python scripts/videoschnitt/transkribieren.py                    # neuestes Video in video/input/
python scripts/videoschnitt/transkribieren.py mein-reel.mp4
python scripts/videoschnitt/transkribieren.py mein-reel.mp4 --modell large-v3
```

Erzeugt `video/transkripte/<slug>/`:

| Datei | Wofür |
|---|---|
| `saetze.md` | **das liest Claude** — Sätze nummeriert, mit Zeit, Pause davor, Take-Gruppe |
| `words.json` | jedes Wort mit Start/Ende — Grundlage für wortgenaue Schnitte |
| `cutlist-vorschlag.json` | erster Vorschlag nach „letzter vollständiger Take gewinnt" |
| `transkript.srt` / `.txt` | Untertitel und Fliesstext |
| `meta.json` | Dauer, Auflösung, FPS |

**Take-Erkennung:** Sätze werden an Satzzeichen und an Pausen > 0.45 s getrennt.
Zusätzlich greift eine **Neuanlauf-Erkennung**: taucht der Satzanfang mitten im
Satz noch einmal auf („Aber du hast keine … Aber du hast kein Thema…"), wird
dort getrennt. Danach werden ähnliche Sätze (Ähnlichkeit ≥ 0.72 oder gemeinsamer
Anfang) zu Take-Gruppen zusammengefasst und der letzte **vollständige** Take
gewinnt. Stellschrauben oben im Skript: `PAUSE_GRENZE`, `AEHNLICHKEIT`,
`LOOKAHEAD_SAETZE`.

Laufzeit auf CPU grob: `small` ≈ 0.5× Echtzeit, `medium` ≈ 1× Echtzeit.

---

## 2 · `schnitt.py`

```bash
python scripts/videoschnitt/schnitt.py video/transkripte/<slug>/cutlist.json
python scripts/videoschnitt/schnitt.py <cutlist> --slug mein-reel --nur-clips
```

Erzeugt `video/output/YYYY-MM-DD-<slug>/`:

| Datei | Wofür |
|---|---|
| `rohschnitt.mp4` | alles hintereinander, zum Anschauen |
| `clips/01.mp4 …` | jede gute Stelle einzeln — alle markieren, in CapCut ziehen |
| `untertitel.srt` | auf den Schnitt umgerechnet |
| `words-schnitt.json` | Wort-Zeitstempel auf der **neuen** Zeitachse (für die Textebene) |
| `schnittprotokoll.md` | was drin ist, was rausflog, wie lang |
| `cutlist.json` | die verwendete Liste, zum Nachvollziehen |

**Montage aus mehreren Clips:** Jedes Segment darf eine eigene `quelle` haben.
Damit entsteht aus mehreren Handy-Clips ein Reel — z.B. erst der Clip vom
Auspflanzen, dann der vom Ernten, damit die Metapher als Bildfolge dasteht statt
als Behauptung. Clips mit unterschiedlicher Aufloesung oder Querformat werden
automatisch auf das Zielformat (Standard 1080×1920) skaliert und beschnitten.
Ton kommt nur mit, wenn **alle** Quellen eine Tonspur haben.

**Format der `cutlist.json`:**

```json
{
  "quelle": "video/input/mein-reel.mp4",
  "words": "video/transkripte/mein-reel/words.json",
  "padding_vor": 0.25,
  "padding_nach": 0.15,
  "regel": "letzter vollstaendiger Take gewinnt",
  "segmente": [
    {"nr": 1, "start": 3.12, "ende": 7.44, "text": "Der Hook."}
  ]
}
```

Alle Clips werden mit identischen Parametern neu kodiert (gleiche Auflösung,
FPS, `yuv420p`, Audio 48 kHz Stereo). Ohne das schlägt das Zusammenfügen fehl.
Überlappende oder direkt aneinandergrenzende Segmente werden automatisch
zusammengezogen, statt sie doppelt zu schneiden.

---

## 3 · `textebene.py` — das Finish (Zoom + Untertitel + Textebene)

```bash
python scripts/videoschnitt/textebene.py video/output/<ordner>/finish.json
python scripts/videoschnitt/textebene.py <spec> --pruefen    # nur validieren
python scripts/videoschnitt/textebene.py <spec> --rendern    # bis zum fertigen MP4
```

Baut ein HyperFrames-Projekt in `video/output/<ordner>/finish/` mit fünf Ebenen:

1. Rohschnitt — bekommt die **Zoom-Bewegung**
2. das **grosse** betonte Wort (Poppins Bold, durchscheinend, Farbverlauf im Buchstaben)
3. Patricia freigestellt *(optional)* — dadurch liegt das Wort **hinter** ihr
4. die **kleine** dünne Zeile (Poppins Light) — liegt vor ihr
5. **wortgenaue Untertitel** *(optional)* — das gerade gesprochene Wort in Orange

Das gerenderte MP4 landet in `finish/renders/`. Damit ist CapCut **optional**.

**Spezifikation:**

```json
{
  "video": "video/output/2026-09-10-reel/rohschnitt.mp4",
  "words": "video/output/2026-09-10-reel/words-schnitt.json",
  "person_alpha": "video/output/2026-09-10-reel/person.webm",
  "profil": "mentoring",
  "position": 46,
  "zoom":       {"modus": "auto", "staerke": 1.07, "fokus": "50% 42%"},
  "untertitel": {"an": true, "position": 74},
  "einblendungen": [
    {"klein": "das ist kein", "gross": "ZEITPROBLEM", "ab_wort": "Zeitproblem", "dauer": 2.2}
  ]
}
```

### Textebene

- `ab_wort` — die Einblendung startet auf diesem Wort (Treffer werden der Reihe
  nach vergeben, Umlaute und Beugungen werden toleriert). Alternativ `ab_sek`.
- `auftritt` — `links` / `rechts` / `pop`. Weglassen = automatisch abwechselnd.
- `position` — vertikale Lage in Prozent (Standard 46).
- `profil` — `mentoring` (Creme → Petrol → Dunkelblau) oder `doterra`
  (Creme → Orange → Dunkelblau). Brand hat **kein Gelb**.
- Beide Zeilen sitzen auf Stoss (`line-height: 0.84`). Die Schriftgrösse des
  grossen Worts skaliert automatisch, damit lange Wörter im Bild bleiben.

### Zoom

`"modus": "auto"` nimmt die **Clipgrenzen** aus `words-schnitt.json`: jeder
zweite Clip bekommt eine langsame Fahrt hinein, dazwischen sitzt ein harter
Sprung auf eine engere Einstellung. Das ist der Rhythmus, den ein Mensch
schneiden würde — durchgehend zoomen wirkt seekrank, gar nicht zoomen wirkt statisch.

- `staerke` — Endvergrösserung der Fahrt (1.0–1.30, Standard 1.07). Sprünge
  liegen 0.02 darüber.
- `fokus` — `transform-origin`, Standard `50% 42%` (Gesichtshöhe, nicht Bildmitte)
- `"modus": "aus"` schaltet ab. `"modus": "manuell"` mit `abschnitte`
  (`ab_wort`/`ab_sek`, `dauer`, `art`: `fahrt`|`sprung`) für gezielte Betonungen.
- Die freigestellte Ebene bekommt **exakt dieselbe** Bewegung, sonst laufen
  Person und Hintergrund auseinander.

### Freie Elemente (Kapitel 06 des Guides)

Alles, was nicht der Kelsie-Baustein ist. Jedes Element braucht die **vier
Angaben**: Aussehen · Bewegung · Stelle · Sound.

```json
"elemente": [
  {"typ": "punkt", "text": "AUFNAHME", "farbe": "#dc822e", "flaeche": "glas",
   "bewegung": "pulsieren", "ab_wort": "aufnehmen", "dauer": 3.2,
   "wo": {"x": 50, "y": 13}, "sound": "klick"},
  {"typ": "chip", "text": "Glas-Look", "farbe": "#f1ecdd", "kursiv": true,
   "bewegung": "links", "ab_wort": "Glas", "dauer": 2.4,
   "wo": {"x": 50, "y": 30}, "sound": "pop"}
]
```

- `typ` — `punkt` (Punkt + Beschriftung) · `chip` (Text in Pille) · `notiz` (Panel)
- `flaeche` — `glas` (Frostglas mit dunkler Basis) · `voll` (Dunkelblau) · `keine`
- `bewegung` — `pulsieren` · `links` · `rechts` · `pop` · `hoch` · `keine`
- `wo` — Position in Prozent, Bezugspunkt ist die Mitte des Elements
- `sound` — `klick` · `pop` · `whoosh` · `ding` · `keiner`

**Sounds werden mit ffmpeg erzeugt**, nicht heruntergeladen (`SOUNDS` oben im
Skript): keine Lizenzfragen, keine fehlenden Dateien, immer identisch.
Gesamtlautstärke über `"sound": {"lautstaerke": 0.55}`.

Beim Pulsieren bewegt sich nur der Punkt, nicht die Beschriftung — sonst
wackelt der Text mit und wird unlesbar.

### Konzept-Vorschau

```bash
python scripts/videoschnitt/textebene.py <spec> --konzept
```

Legt Standbilder über dem **echten** Material in `finish/konzept/` ab, genau an
den Stellen, wo Elemente und Einblendungen auftauchen (plus ein Kontaktbogen).
Erst anschauen, dann rendern — ein Render dauert Minuten, ein Standbild Sekunden.

### Untertitel

Gruppen von max. 4 Wörtern / 1.8 s, getrennt an Pausen > 0.6 s. Das gerade
gesprochene Wort wird orange, danach wieder weiss.

- Eine Gruppe endet spätestens dort, wo die nächste beginnt — sonst stehen zwei
  Zeilen übereinander.
- **Untertitel pausieren automatisch, solange eine Einblendung steht** (mehr als
  30 % Überlappung). Sonst steht unten „Kommentier mir MAMA", während oben gross
  MAMA liegt — zweimal derselbe Satz im Bild.
- Die dunkle Unterlage hinter der Zeile ist Absicht: ohne sie fällt das orange
  Wort auf hellem Videobild unter 3:1 Kontrast.

**Für „hinter mir" braucht es die freigestellte Ebene:**

```bash
npx hyperframes remove-background video/output/<ordner>/rohschnitt.mp4
```

Ohne sie liegt der Text vor ihr — das Skript sagt das auch beim Lauf.

---

## Bekannte Stolperstellen

- **Umlaute in der Konsole:** alle drei Skripte stellen `stdout` auf UTF-8. Ohne
  das bricht Windows (cp1252) beim ersten `→` mit `UnicodeEncodeError` ab.
- **HyperFrames-Lint:** `<video>` darf nicht gleichzeitig `muted` und
  `data-has-audio="true"` haben. Der Hintergrund-Clip läuft deshalb ohne `muted`,
  die freigestellte Ebene mit `data-volume="0"`.
- **GSAP-Aufrufe** werden als Text zusammengesetzt — bei Änderungen darauf achten,
  dass die geschweiften Klammern nicht doppelt landen. `--pruefen` fängt das ab.
- **Erster HyperFrames-Lauf** lädt Chromium und das npm-Paket, das dauert ein paar
  Minuten. Danach ist es im Cache.
- **`<audio>` braucht zwingend eine `id`.** Ohne sie findet der Renderer das
  Audio nicht und die Stelle ist im fertigen Video **stumm** — ohne Fehlermeldung.
  `--pruefen` fängt das ab.
- **Keyframes:** `schnitt.py` erzwingt einen Keyframe pro Sekunde (`-g`,
  `-keyint_min`, `-sc_threshold 0`). Ohne das meldet der Renderer „sparse
  keyframes" und einzelne Bilder frieren ein.
- **Pulsieren** als eine Tween mit `repeat`/`yoyo` bauen, nicht als Kette
  einzelner Tweens — sonst stossen die Enden aufeinander und der Lint meldet
  überlappende Tweens.
