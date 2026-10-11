---
name: remotion-motion-graphics
description: "Bewegte Grafik-Elemente mit Remotion bauen — animierte Einblendungen, Intro/Outro, Zahlen- und Text-Animationen, Uebergaenge, Logo-Bewegung. NUR fuer die Gestaltungsebene. Der Schnitt von Rohmaterial laeuft ueber /videoschnitt, das Konzept ueber /reels — dieser Skill wird von dort gerufen, nicht statt ihnen."
---

# Remotion Motion Graphics

## 🦋 So wird gearbeitet — Jenyas Ablauf (seit 06.10.2026, geht allem unten vor)

Aus Jenya Korks Kurs „Dein Videoeditor ist Claude", Teil 4. Patricia: *„ich finde das
macht mein skill noch nicht gut."* Der Befund: Es gab Bausteine, aber jedes Reel baute
ein **neues Wegwerf-Projekt** in einem Datumsordner, es gab **keine Auswahl** vor dem
Bau, und dieser Skill wusste nicht einmal, dass es die Bausteine gibt.

### Der eine Grafik-Ordner: `scripts/grafik/`

Jenyas Unterordner „grafik" — Remotion **einmal** eingerichtet, alle Reels laufen
darüber. **Nie wieder ein neues Remotion-Projekt pro Reel anlegen.**

| Baustein | Datei | Wofür | Varianten |
|---|---|---|---|
| **Hook** | `bausteine/Hook.tsx` | die ersten ~4 s, mittig | **A** Zwei Schriften · **B** Kelsie, Wort für Wort mit Verlauf · **C** Balken (Story-Stil) |
| **Untertitel** | `bausteine/Untertitel.tsx` | wortgenau, pausiert bei Einblendungen | **A** Zwei Schriften, betonte Wörter orange · **B** Aktives Wort leuchtet · **C** dunkler Balken |
| **Knallwort** | `bausteine/Einblendungen.tsx` | ein grosses Wort, optional Schilder | Ton `pop` |
| **Karte** | `bausteine/Einblendungen.tsx` | freigegebene Kundenstimme | Ton `whoosh` |
| **Clipfolge** | `bausteine/Clipfolge.tsx` | Material mit Auto-Zoom (jeder zweite Abschnitt) | — |
| **Look** | `bausteine/Einblendungen.tsx` | Farbkorrektur, Korn, Vignette — dezent | `stil.look: false` schaltet ab |
| **Ton** | `bausteine/Ton.tsx` | klick · pop · whoosh · ding, mit ffmpeg erzeugt | gleiche Rezepte wie `textebene.py` |

Die Beschreibung der Stile (Aussehen · Bewegung · Stelle · Sound) steht in
**`context/videoschnitt-animationen.md`** — das ist Jenyas `stil.md`. Neuer Baustein
→ dort mit Namen und Zweck eintragen (Jenya: *„Damit du es nie wieder erklären musst"*).

### Ablauf je Reel

1. **Projekt = der Ordner des Reels** (z. B. `video/output/<datum>-<slug>/`) mit dem
   Material und einer `grafik.json`: `dauer`, `clips`, `woerter` (aus
   `words-schnitt.json`, Felder `text/startMs/endMs`), `hook {fein, kraeftig, sound}`,
   `betont`, `einblendungen`, `stil`.
2. **Vorgabe ist Stil B** (Hook „Kelsie, Wort für Wort“ + Untertitel „Aktives Wort“,
   Patricias Entscheid 06.10.2026: *„klar Stil B“*). Text-Oberkante bei **56 %** der
   Bildhöhe, unter dem Kinn (*„verdeckt etwas mein kinn“* — vorher 43 %).
   Varianten nur zeigen, wenn sie einen anderen Look will oder ein neuer Baustein dazukommt
   (Jenyas Prompt 6):
   `python scripts/grafik/vorschau.py <projekt>` → `vorschau/hook-varianten.jpg` und
   `vorschau/untertitel-varianten.jpg`, je A|B|C nebeneinander über einem echten Bild.
   **Selbst anschauen** (Standbild-Prüfung unten), dann Patricia zeigen.
3. **Sie wählt** („Hook B, Untertitel A") → in `grafik.json` unter `stil` eintragen.
4. `vorschau.py <projekt> --stellen` → je Einblendung und Schluss ein Standbild mit dem
   gewählten Stil. Prüfen.
5. **Dann erst bewegt:** `vorschau.py <projekt> --rendern` → `renders/reel.mp4`, danach
   `kante-suchen.py` und Standbilder (Pflicht, siehe unten).
   🤖 **Vor jedem Render prüft das Werkzeug selbst** (auch einzeln mit `--pruefen`):
   **Text am Bildrand** und **Text auf dem Gesicht** — OpenCV sucht alle 0,4 s ihr Gesicht
   im Videobild und zählt Textpixel darin. Bei einem Fund bricht der Render ab und nennt
   Sekunde und Kinnhöhe → `stil.hoehe` in `grafik.json` tiefer setzen.
   Getestet 06.10.2026 an beiden Enden: Text bei 40 % → 41 Funde, bei 56 % → keiner.
   Zwei Fallen, die dabei aufgefallen sind: Hände vor dem Bauch wurden als zweites Gesicht
   erkannt (jetzt zählt nur das oberste Gesicht in der oberen Bildhälfte), und ein zu grosser
   Kinn-Zuschlag (+38 %) meldete Text, der sauber unter dem Kinn stand (jetzt +12 %).
   Wo kein Gesicht erkannt wird (abgewandt, Bewegung), sagt das Werkzeug die Sekunde —
   dort Standbild anschauen. Braucht `pip install "opencv-python-headless<5"`
   (OpenCV 5 hat den Gesichtserkenner entfernt).
6. **Feedback mit Sekundenangabe** nehmen und genau so umsetzen: *„Bei Sekunde 12 steht
   die Einblendung zu kurz, lass sie eine Sekunde länger stehen. Der Klang ist zu laut."*
   Nur die genannte Stelle ändern, die Stelle danach wieder als Standbild zeigen.
7. **Was sie zweimal gleich korrigiert, wird Vorgabe im Baustein** — nicht im nächsten Chat.

Für den Kelsie-Stil mit Wort **hinter** Patricia (Freistellung) und die B-Rolls läuft
weiter `scripts/videoschnitt/textebene.py`, bis das hier nachgebaut und von ihr
freigegeben ist.

### Technik nachschlagen: der offizielle Remotion-Skill

Unter `references/remotion-offiziell/` liegt der **offizielle Skill der
Remotion-Macher** (v4.0.533, Jenyas Empfehlung), als Nachschlagewerk, nicht als eigener
Skill. Einstieg `ROUTER.md`. Gebraucht vor allem: `remotion-markup/` (Animation,
Timing, Audio, Schriften, `calculate-metadata.md`), `remotion-captions/`,
`remotion-render/`. **Bei jeder Remotion-Frage dort nachsehen statt raten.**
Er empfiehlt die **Studio-Vorschau im Browser** (`cd scripts/grafik && npx remotion
studio --public-dir=<projekt>`) — gut, wenn Patricia live mitschauen will.

> Die englischen Abschnitte weiter unten (Step 1–5, Five-layer stack, Ken Burns) sind
> aus dem Ursprungs-Skill für Erklärvideos. Für Sprechreels gilt der Ablauf hier oben;
> Korn und Vignette nur dezent (Baustein „Look"), das Material soll echt aussehen.

---

> ## 🇨🇭 VORRANG — Patricias Marke (ergaenzt vom Workspace, 15.09.2026)
>
> Dieser Skill kommt von aussen (MIT, haidrrrry). Er gilt vollstaendig, **ausser**
> an diesen Stellen — dort gewinnt der Workspace:
>
> 1. **Farben und Schriften kommen aus `assets/theme.ts`** und sind gesetzt:
>    Petrol #12828c · Dunkelblau #0c1c30 · Teal #29556d · Creme #f1ecdd ·
>    Orange #dc822e. **Kein Gelb, kein Gold, kein Pink.** Orange nur als Akzent.
> 2. **Format 1080x1920.** Der Hook gehoert in die **Mitte** — oben 0-12.5 % und
>    unten 82-100 % sind tote Zone (Instagram legt Caption und Knoepfe drueber).
> 3. **Text unter dem Kinn** (Oberkante 56 %, seit 06.10.2026 — „oberes Drittel" galt fuer
>    Cover ohne Person), nie in die tote Zone ab 82 %. Hoechstens **zwei**
>    Textelemente gleichzeitig. Blockwechsel spaetestens alle **3 Sekunden**.
> 4. **Nie heller Text ohne Balken oder Schatten auf hellem Grund.**
> 5. **Kein KI-erzeugtes Bildmaterial** als Ersatz fuer echte Aufnahmen. Gestaltete
>    Flaechen, Typo und Overlays ja — erfundene Szenen nein.
> 6. **Gesicht und Hauptmotiv bleiben frei.** Keine Textbox ueber Patricias Kopf
>    oder ueber dem Schluesselelement des Fotos.
> 7. **Regel 10 des Skills (rendern, Standbilder ziehen, hinschauen, korrigieren)
>    ist hier nicht optional.** Genau ihr Fehlen hat die bisherigen Reels ruiniert:
>    8 Sekunden unveraenderter cremefarbener Text auf hellem Gras, unten im Bild.
> 8. Deutsche Texte: echte Umlaute, Schweizer **ss** statt ss-Ersatz.
>
> ---
>
> ### 🛑 Die Standbild-Pruefung — jedes Mal, nie ueberspringen
>
> Nach jedem Render Standbilder ziehen und **wirklich anschauen**. Diese neun
> Punkte, in dieser Reihenfolge. Einer faellt durch → korrigieren, neu rendern,
> neu pruefen. Erst dann abgeben.
>
> 1. **Zerrissene Woerter.** Steht irgendwo ein einzelner Buchstabe allein auf der
>    naechsten Zeile? → `overflowWrap: "anywhere"` und `break-word` sind **verboten**.
>    Immer `overflowWrap: "normal"` + `wordBreak: "keep-all"` + `hyphens: "none"`.
>    Passt der Text dann nicht, wird das **Zeichen-Budget kleiner**, nicht das Wort
>    zerbrochen. *(Patricia, 15.09.2026: „mir fällt auf, dass einzelne buchstaben
>    abgeschnitten werden und einzeln auf der nächsten zeile stehen.")*
> 2. **Schriftgroesse.** Liest eine 50-Jaehrige das auf dem Handy? Im Zweifel zu
>    gross statt zu klein. Richtwerte bei 1080×1920: laufender Text ab **60 px**,
>    betontes Wort ab **96 px**, Hook-Knallzeile ab **130 px**.
> 3. **Rand.** Beruehrt Text den Bildrand? Nichts Wichtiges ausserhalb 86 % Breite.
> 4. **Tote Zonen.** Nichts Wichtiges oben 0–12.5 % und unten 82–100 %.
> 5. **Gesicht frei.** Keine Karte, kein Kasten, kein grosses Wort ueber Patricias
>    Kopf. Auch nicht halb.
> 6. **Zwei Texte uebereinander.** Laeuft der Untertitel weiter, waehrend eine
>    Einblendung steht? → Untertitel muss pausieren.
> 7. **Kontrast.** Heller Text auf hellem Grund ohne Schatten oder Balken ist
>    durchgefallen. Instagram komprimiert zusaetzlich.
> 8. **Hoechstens zwei Textelemente** gleichzeitig im Bild.
> 9. **Sichtbar vor dem Auftritt?** Steht etwas schon da, bevor es kommen soll, oder
>    noch, nachdem es weg sein sollte? → fehlendes `clamp`.
> 10. **🚨 Passt die Einblendung zum INHALT?** Jedes Emoji, jede Grafik, jede Karte
>    muss das tragen, was in DIESEM Moment gesprochen wird. Nicht was allgemein
>    zur Marke passt.
>    *(Patricia, 15.09.2026: „die kursfeedbacks … passen hier ja irgendwie nicht"
>    — Kundenstimmen ueber Instagram-Kurse unter einem Video ueber ihren
>    Network-Ausstieg. Und zum abstrakten KI-Bild: „das macht doch gar keinen Sinn.")*
>
>    **Der Test:** Wer nur diese zwei Sekunden sieht — versteht der etwas, oder
>    schaut er nur etwas an? Deko faellt durch. Eine Einblendung muss **sagen**,
>    nicht **schmuecken**.
>
>    Die Vorbilder machen das nie abstrakt: Kelsie blendet echte Bewertungen,
>    Hausfotos und Vorher-Nachher-Raster ein. Alles **Belege**.
>
> 11. **Schweizer ss.** Kein deutsches Sonderzeichen im Bild. Whisper transkribiert
>    damit — beim Bauen der Untertitel ersetzen, nicht hinterher suchen.

---

### 🤖 Die Rand-Pruefung laeuft automatisch — sie ist keine Stichprobe

**Punkt 3 von Hand zu pruefen funktioniert nicht.** Bei einem 58-Sekunden-Reel gibt
es rund 50 Textseiten; fuenf Standbilder anzuschauen deckt zehn Prozent ab. Genau so
ist am 15.09. Text rechts aus dem Bild gelaufen, obwohl die Regel schon dastand.

**Deshalb: `scripts/video-pruefung/rand-pruefen.py`** — laeuft im Remotion-Projekt
und prueft alle 0.4 Sekunden eine Stelle:

```bash
cd <remotion-projekt> && python <repo>/scripts/video-pruefung/rand-pruefen.py --takt 0.4
```

Das Skript rendert die Textebene **ohne Video** (Prop `nurText: true`, muss die
Komposition unterstuetzen) und misst den hellsten Punkt in den aeusseren 24 Pixeln je
Seite — **ueber Rohbytes, nicht ueber `signalstats`**. Alles ueber 60 ist Text am
Rand. Die Ausgabe nennt Frame und Sekunde.

**Pflicht vor jedem Render.** Erst wenn dort „kein Text am Rand" steht, wird gerendert.

### 🚨 Der Umbruch-Fehler, der zweimal durchging (15.09.2026)

**Wort-Elemente in JSX stehen ohne Leerzeichen nebeneinander.** Als `inline`
gesetzt sieht der Browser daraus EINE unteilbare Zeile und schiebt sie aus dem
Bild — auch wenn `maxWidth` gesetzt ist, auch wenn die Breiten-Rechnung zwei
Zeilen erlaubt hat.

```tsx
// FALSCH — bricht nie um:
<div style={{ maxWidth: "86%", textAlign: "center" }}>
  {tokens.map(t => <span style={{ marginRight: 14 }}>{t}</span>)}
</div>

// RICHTIG — jedes Wort ist ein Flex-Element und bricht von selbst:
<div style={{ display: "flex", flexWrap: "wrap", justifyContent: "center",
              alignItems: "baseline", columnGap: 14, width: "86%" }}>
  {tokens.map(t => <span>{t}</span>)}
</div>
```

**Merksatz:** Wortweise gesetzter Text wird **immer** als Flex-Zeile mit
`flexWrap: "wrap"` gebaut, nie als inline mit `marginRight`.

### 🚨 Eine Pruefung, die nicht fehlschlagen kann, ist schlimmer als keine

Die erste Fassung der Rand-Pruefung nutzte ffmpeg `signalstats` und griff das
Ergebnis per `grep -o "YMAX:[0-9]*"` ab. Das gab **nichts** zurueck — also meldete
sie bei jedem Lauf „kein Text am Rand", waehrend im fertigen Video drei Zeilen
sichtbar abgeschnitten waren. Patricia hat es gesehen, das Skript nicht.

**Regel: Jede neue Pruefung wird zuerst an einem bekannt FEHLERHAFTEN Stand
getestet.** Schlaegt sie dort nicht an, ist sie kaputt — nicht der Stand.
Beim Nachbauen gemessen: alter Stand **147**, korrigierter Stand **25**,
Schwelle **60**. Erst damit ist bewiesen, dass die Pruefung greift.

Die jetzige Fassung (`scripts/video-pruefung/rand-pruefen.py`) liest **Rohbytes**
und bildet das Maximum selbst — kein Parsen von Werkzeug-Ausgaben.

### 📐 Zeilenbreite wird gerechnet, nie geschaetzt

Eine feste Zeichenzahl je Seite geht schief, sobald betonte Woerter dabei sind —
die sind bei 96 px fast doppelt so breit wie feine bei 60 px. Richtig ist eine
Breiten-Rechnung je Wort:

```
BREITE_FEIN   = 30 px je Zeichen  (60 px Serife)
BREITE_BETONT = 56 px je Zeichen  (96 px Black)
ZEILE_MAX     = 1080 * 0.86       (86 % = 929 px)
```

🚨 **Wer die Schriftgroessen aendert, MUSS diese zwei Werte mitaendern.**
>
> **Geprueft wird an mindestens fuenf Stellen:** Hook (~Frame 45), fruehe Mitte,
> jede Einblendung einzeln, und kurz vor Schluss. Bei Reels ueber 30 s zusaetzlich
> alle ~15 Sekunden eine Stichprobe.
>
> Das bestehende `/videoschnitt` (Transkript, Rohschnitt, CapCut-Clips) bleibt
> zustaendig fuer den **Schnitt**. Dieser Skill ist fuer die **Bewegung und
> Gestaltung** darueber.

Remotion renders React components frame-by-frame into video. Code quality is not the
bottleneck — **motion design craft is**. Untrained generation produces linear easing,
opacity-only fades, simultaneous entrances, flat colors, and no texture. That is the
"generic AI video" look. This skill exists to prevent it.

## Non-negotiable rules (apply to EVERY composition)

1. **NEVER use linear interpolation.** Every `interpolate()` gets an easing curve;
   every entrance prefers `spring()`. Always `extrapolateLeft/Right: "clamp"`.
2. **Entrances animate 2–3 properties together** (opacity + translateY + scale).
   A lone fade is forbidden.
3. **Stagger everything.** Lists, words, rays, cards: 3–6 frame offsets. Nothing
   enters simultaneously.
4. **Exits exist and are faster than entrances** (~10 frames vs ~20).
5. **Five-layer stack in every scene**, bottom to top: background mesh → assets →
   graphics/type → color grade → grain + vignette. Never a flat solid background.
6. **Every still image gets Ken Burns** (slow scale 1→1.08 + pan). Every video asset
   uses `<OffthreadVideo>`, never `<Video>`.
7. **Idle elements breathe**: anything on screen >2s gets sin-wave micro-motion.
8. **All timing derives from `fps`** via `useVideoConfig()`. No magic frame numbers.
9. **One theme object** at the top of the project (colors, easings, spring presets,
   fonts). Never inline a hex color or easing in a component.
10. **Render, extract frames, LOOK at them, fix, re-render.** Never deliver an
    unverified render. This loop is mandatory — see Verification below.

## Workflow

### Step 1 — Scope
Determine: duration, fps (30 default; 60 only for heavy fast motion), dimensions
(1080×1920 Reels/Shorts, 1920×1080 landscape), what assets exist (images, footage,
audio, logos), and whether this is a new composition or an edit to an existing project.
If editing an existing project: read `src/` fully first, find the theme (or create one),
and refactor violations of the rules above before adding features.

### Step 2 — Setup
New project:
```bash
npm install remotion @remotion/cli react react-dom
# optional: @remotion/transitions @remotion/motion-blur @remotion/google-fonts
```
Copy `assets/theme.ts` from this skill into `src/theme.ts` and adjust the palette to
the user's brand. Structure: `src/index.ts` (registerRoot) → `src/Root.tsx`
(Composition, duration/fps/size) → `src/scenes/*.tsx` → `src/components/*.tsx`.
User assets go in `public/`, loaded via `staticFile()`.

### Step 3 — Build
Read `references/motion-patterns.md` for the reusable component implementations
(BgMesh, Grade, Grain, Vignette, KenBurns, WordReveal, Stagger, Counter, Spark,
transitions, parallax). Compose scenes from those patterns. For pacing, rhythm,
typography, color palettes, and sound design rules, read
`references/design-rules.md`.

Scene rhythm: HIT → hold (15–20 still frames) → build → HIT. Something must move
in the first 15 frames. Never >90 frames without a new visual element.

### Step 4 — Render
```bash
npx remotion render src/index.ts <CompId> out/video.mp4 --codec h264 --crf 17
```
Remotion needs a Chromium binary. If its auto-download fails (sandboxes, offline CI),
find one and pass it explicitly:
```bash
which chromium chromium-browser google-chrome 2>/dev/null
ls /opt/pw-browsers 2>/dev/null   # Playwright installs live here
npx remotion render ... --browser-executable=<path>
```
If full Chrome errors with "Old Headless mode has been removed", use a
`headless_shell` binary instead (Playwright ships one as
`chromium_headless_shell-*/chrome-linux/headless_shell`).

### Step 5 — VERIFY (mandatory, never skip)
Extract frames at key moments and visually inspect each one. The portable
method — works on machines with no system ffmpeg, renders the exact frame:
```bash
for f in 15 45 90 150; do
  npx remotion still src/index.ts <CompId> out/check_$f.png --frame $f --overwrite
done
```
If system ffmpeg IS available, extracting from the finished mp4 also verifies
the encode itself (`-ss` seeking is more portable than `select=` filters, whose
quoting breaks in some shells and in Remotion's bundled ffmpeg):
```bash
ffmpeg -v error -ss 1.5 -i out/video.mp4 -frames:v 1 check_1.png
```
Look for, and fix, in order of frequency:
- **Spacing bugs**: `gap`/`margin` in `em` resolves against the PARENT font-size
  (often 16px), not the text size — use px values in flex containers around big type.
- Text overflowing or touching frame edges (keep critical content in middle 75%
  vertically for 9:16 — platform UI covers top/bottom).
- Elements visible before their entrance or after their exit (missing clamp).
- Color/contrast failures: hero color on >1 element per frame, dim text unreadable
  over the grade.
- Layer order mistakes (grain/vignette must be on top, grade above content).
Fix → re-render → re-extract → re-inspect. Only deliver after a clean pass.
Then run the final checklist at the bottom of `references/design-rules.md`.

### Editing the user's existing footage
To enhance an existing mp4 (captions, grade, intro/outro) rather than build from
scratch: put the file in `public/`, render it as the asset layer with
`<OffthreadVideo src={staticFile("clip.mp4")} />`, set composition duration from the
clip length, and stack graphics/grade/grain above it. Get the clip's duration and fps
with `ffprobe` before setting up the composition. For word-synced captions over
speech, see the captions section of `references/motion-patterns.md`.

## Reference files
- `references/motion-patterns.md` — copy-paste component library: backgrounds,
  grade/grain/vignette, Ken Burns, text reveals, counters, transitions, parallax,
  audio sync, captions. Read before writing components.
- `references/design-rules.md` — palettes, typography rules, scene architecture,
  sound design, pre-delivery checklist. Read before designing scenes and before
  final delivery.
- `assets/theme.ts` — the theme template to copy into every project.

## Common failure modes to actively avoid
- **Emoji as icons.** Emoji render as full-color platform glyphs (green ✳️,
  blue 🌐) that ignore your palette and silently break the one-hero-color rule,
  and they sit on whatever background you gave them (orange mascot on orange
  tile = invisible). Draw glyphs with CSS/SVG in theme colors, or verify every
  emoji against the extracted frames.
- **No SFX assets is not a reason to ship silent.** Synthesize a minimal kit as
  16-bit WAVs from a Node script (noise-burst whoosh, pitch-drop pop, sine-thump
  kick/bass, detuned-sine pad) into `public/sfx/` — see `examples/scripts/` in
  the repo. Zero downloads, fully deterministic.
- Generating one giant component instead of themed, reusable pieces.
- `durationInFrames` mismatch between Composition and scene content (dead air).
- Forgetting `--overwrite` on re-renders, then inspecting the stale file.
- Fonts: never rely on system defaults for hero text; load a display font via
  `@remotion/google-fonts` or `@font-face` + `staticFile`.
- Trying to "describe" the result to the user instead of rendering and verifying it.
