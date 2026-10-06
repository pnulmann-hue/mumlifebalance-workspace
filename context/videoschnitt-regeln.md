---
tags: [videoschnitt, regeln, content]
---

# Videoschnitt-Regeln — so schneidet Claude meine Videos

Das ist die **einzige Quelle** für den `/videoschnitt`-Skill. Jede Regel hier
entstand aus einem echten Durchgang, nicht aus einer Annahme. Wenn ein Rohschnitt
etwas falsch macht, wird **diese Datei** geändert — nicht der nächste Chat.

> Status: **Startfassung vom 2026-09-10.** Die Punkte in eckigen Klammern
> bestätigt oder korrigiert Patricia nach dem ersten echten Video.

---

## 1 · Wie ich rede

Ich spreche mein Rohmaterial **in einem Stück in die Kamera**, mit Versprechern
und mit Sätzen, die ich mehrmals sage, bis einer sitzt. Ich korrigiere mich beim
Sprechen nicht — das macht der Schnitt.

**Take-Regel (hart):** Wenn ich einen Satz mehrmals sage, gilt immer die
**letzte vollständige Version**. Alle Anläufe davor fliegen raus, ohne
Rückfrage. „Vollständig" heisst: der Satz ist zu Ende gesprochen, nicht
mittendrin abgebrochen.

Sonderfall: Wenn *keiner* der Anläufe vollständig ist, kommt der letzte in die
Schnittliste und wird dort als `⚠ kein vollständiger Take` markiert — dann
entscheide ich.

**Neuanlauf nach einer Pause** (aus Jenyas Kurs, Okt. 2026): Setze ich einen Satz
nach einer kurzen Pause neu an, ist das ein **neuer Anlauf, kein Satz mit Pause**.
Kehren dieselben ersten Wörter innerhalb einer Passage ein zweites Mal wieder,
wird ab der zweiten Stelle geschnitten und der Anfang verworfen.

---

## 2 · Was immer rausfliegt

- Der Vorlauf am Anfang, bis zum **ersten Wort des Hooks** (Kamera richten, Luft holen, „so, okay")
- Versprecher und abgebrochene Satzanfänge
- Alle Anläufe eines Satzes ausser dem letzten vollständigen (siehe oben)
- Pausen über **0,3 Sekunden** werden auf 0,3 s gekürzt (Jenyas Regel, seit 06.10.2026 — vorher flogen erst Löcher über 1,5 s raus)
- Räuspern, Husten, „ähm", „also ähm"
- Alles nach meinem Schlusssatz (der CTA ist das Ende, danach kommt nichts mehr)
- Füllwörter: „ähm“, „also ähm“, **„genau“ als Einzelwort**, **„okay“ am Satzanfang** (Jenyas Vorlage — ich ergänze meine eigenen)
- 🚨 Whisper lässt „ähm“ oft ganz weg. Dann steht es nicht im Transkript, ist aber hörbar — es sitzt in einer Lücke zwischen zwei Wörtern, und die Pausen-Regel oben kürzt es mit.

---

## 3 · Was bleibt, auch wenn es holprig ist

- **Der Hook** — die ersten Sätze, wortwörtlich so, wie ich sie gesprochen habe.
  Der ist vorher geschrieben und geübt. Nie glattziehen, nie kürzen, nie „verbessern".
- Der **Keyword-CTA am Schluss** („Kommentier mir …") — vollständig, inklusive
  des Keywords. Keywords stehen in `context/patricia-freebies.md`.
- **„also“, „eigentlich“, „nämlich“ mitten im Satz** — das gehört zu meiner Art zu reden.
- Kurze Denkpausen mitten im Satz bis 0,3 s.
- Meine Umgangssprache und der Schweizer Einschlag. Nichts hochdeutsch machen.
- [Fester Satz, der die Reihe benennt — falls ich sowas einführe]

---

## 4 · Wie eng geschnitten wird

- **120 ms** Luft vor dem ersten Wort einer Passage
- **350 ms** Luft nach dem letzten Wort
  (Jenyas Werte, seit 06.10.2026. Vorher 250 / 150 ms — hinten zu knapp, das schnitt Endsilben ab.)
- **Nie mitten in ein Wort schneiden.** Immer an der Wortgrenze aus `words.json`.
- Lieber ein Atemzug zu viel als ein Video, das gehetzt klingt. Gehetzt ist der
  häufigste Anfängerfehler.
- **Fehlt am Satzende eine Endsilbe, lieber 0,5 s Luft nach** statt 150 ms
  (Jenyas Regel — eine verschluckte Silbe klingt schlimmer als eine halbe Sekunde Ruhe).

> Ob die Werte für meine Stimme stimmen, zeigen meine CapCut-Korrekturen
> (`capcut-projekt.py vergleichen`) — dann wird hier nachgezogen.

---

## 4a · Wörter, die Whisper falsch hört

Steht im Transkript eines dieser Wörter, ist das rechte gemeint — im Untertitel
und in der Schnittliste wird es korrigiert:

| Whisper schreibt | gemeint ist |
|---|---|
| Cloud | Claude |
| ß | ss (Schweizer Schreibweise) |
| [ergänze ich, sobald mir ein Wort zweimal auffällt — z.B. doTERRA, Produktnamen, Keywords] | |

---

## 4b · Rhythmus und Ton

Eingearbeitet aus der Analyse von @alinascreatorclub (Sept. 2026) — ihre CapCut-
Bibliotheksnamen nützen uns nichts, aber die **Logik dahinter** ist übertragbar.
Unsere Sounds baut `textebene.py` selbst mit ffmpeg, damit keine Lizenzfrage entsteht.

### Der Grundsatz
**Ein Ton sitzt auf dem Moment, in dem sich im Bild etwas ändert — nie flächig
darüber.** Wenn ein Ton nicht sagen kann, zu welchem sichtbaren Ereignis er gehört,
gehört er nicht ins Video.

### 🎧 Meine Töne (Patricia, 06.10.2026) — gilt vor der Tabelle darunter

Die Klänge liegen in `video/sounds/` (meine Downloads, Pixabay). Erkannt am Dateinamen,
umbenennen nicht nötig. Gesetzt werden sie automatisch von `scripts/grafik/` (`toeneBauen`).

| Wann | Ton | Datei-Wort |
|---|---|---|
| etwas **Neues** erscheint: Wort, Einblendung, Animation | **Pop** | `pop` |
| **Anfang** — wenn der Hook erscheint | **Dramatic YouTube Intro** | `intro` |
| Text, der **sichtbar Buchstabe für Buchstabe geschrieben** wird | **Typing** | `typing` / `keyboard` |
| **Übergänge** zwischen Clips, Wörtern, Animationen | **Short Whoosh** | `woosh` / `whoosh` |

- **Das Intro kommt zum Hook** (Patricia: *„tiping passt ja nur, wenn was neu geschrieben
  wird“*), leise unter der Stimme (erster Test: 9 dB darüber, jetzt gedämpft).
  Typing nur bei echter Schreibmaschinen-Animation.
- **Untertitel bekommen keinen Pop** — ein Ton alle 0,3 s wäre Dauerrauschen.
- **Whoosh sparsam** (Patricia: *„etwas zu viele whooshs“*): höchstens **einer alle 8 s**, und
  keiner, wenn in 2 s Abstand schon ein anderer Ton liegt. Im Test-Reel: 7 → 3.
- **Lautstärke:** Effekte sitzen 2–6 dB **unter** meiner Stimme (Spitze −13 dB).
  Ist mir etwas zu laut oder leise, ändert Claude die Tabelle `LAUT` in
  `scripts/grafik/src/bausteine/Ton.tsx`, nicht das einzelne Reel.

### Wann welcher Ton (Ursprungs-Tabelle, für textebene.py / B-Roll-Altbestand)

| Was im Bild passiert | Ton | Wie er klingt |
|---|---|---|
| ein Wort oder eine Einblendung **poppt auf** | `pop` | kurzer runder Ton, 0.14 s |
| **Schnitt oder harter Zoom-Sprung** | `klick` | trockener Klick, 0.06 s |
| **weicher Übergang**, Schiebe-Bewegung | `whoosh` | Rauschbogen, 0.45 s |
| **Zahl, Punkt, Ergebnis** steht fest | `ding` | heller Ton, 0.60 s |
| **der Hook** in der ersten Sekunde | `klick` **oder gar nichts** | siehe unten |

**Charakter muss passen:** ein mechanischer Übergang bekommt einen mechanischen Ton,
ein weicher einen weichen. Pauschal auf alles denselben Whoosh zu legen ist genau der
Vorlagen-Effekt, den wir bei den Animationen auch vermeiden.

### Rhythmus

- **Untertitel:** ein bis zwei Wörter je Einblendung, also rund alle **0.6–0.8 s** ein
  Wechsel. Das macht `textebene.py` bereits wortgenau.
- **Bild- oder Perspektivwechsel alle 3–4 s.** Bei einem Sprechreel heisst das:
  Zoom-Sprung, eingeschobenes Bild oder ein B-Roll-Ausschnitt. Steht 8 Sekunden lang
  dasselbe Bild, steigen die Leute aus.
- **Jeder sichtbare Schnitt trägt einen Ton.** Ein Schnitt ohne Ton wirkt wie ein
  Fehler, kein Gestaltungsmittel.
- **Der Schnitt liegt auf der Sprechpause**, nie mitten im Wort — steht schon in
  Abschnitt 4 und bleibt die härtere Regel.

### 🚨 Die Grenzen — und die sind wichtiger als die Tabelle

**Auf Instagram läuft die Hälfte der Reels stumm oder mit fremder Musik drüber.** Ein
Sounddesign, das nur mit Ton funktioniert, ist an diesen Zuschauerinnen verlorene
Arbeit. Deshalb:

1. **Kein Ton auf B-Roll.** Patricia legt dort in der App die Musik drüber und postet
   selbst — unsere Effekte würden entweder überdeckt oder stören.
2. **Töne nur bei Sprechreels**, wo ihre Stimme läuft und keine laute Musik.
3. **Sparsam.** Höchstens ein Ton alle zwei bis drei Sekunden. Ein Reel, in dem es
   dauernd klickt und ploppt, klingt nach Vorlage — und das ist das Gegenteil von
   nahbar.
4. **Das Video muss ohne Ton funktionieren.** Erst prüfen, ob es stumm verständlich
   ist; der Ton ist die Zugabe, nie der Träger.

### Nicht übernommen
Ihre Schriftkombinationen (Bebas Neue, Times New Roman, Allura …) bleiben draussen —
Patricias Marke ist **Philosopher + Source Sans 3**, und daran wird nicht gerüttelt.

---

## 5 · Was ich zurückbekomme

1. **`rohschnitt.mp4`** — alles hintereinander, zum Anschauen und Prüfen
2. **`clips/01.mp4, 02.mp4 …`** — jede gute Stelle als eigener Clip. Die markiere
   ich alle auf einmal und ziehe sie in CapCut, dann kann ich jede Stelle einzeln
   anfassen, statt im fertigen Video herumzuschneiden.
3. **`untertitel.srt`** — auf den Schnitt umgerechnet, direkt in CapCut importierbar
4. **`schnittprotokoll.md`** — was drin ist, was rausflog, wie lang

---

## 6 · Bevor Claude mir etwas gibt, prüft es das selbst

- [ ] Ist der Hook vollständig und unverändert drin?
- [ ] Kommt jeder Satz **genau einmal** vor?
- [ ] Ergibt der Text von oben nach unten gelesen einen Ablauf **ohne Sprung**?
- [ ] Ist der CTA am Schluss vollständig, inklusive Keyword?
- [ ] Klingt kein Übergang gehetzt, und ist keine Endsilbe abgeschnitten?
- [ ] Ist der Rohschnitt kürzer als das Rohmaterial, aber nicht kürzer als der Inhalt hergibt?

Fällt einer dieser Punkte durch, wird nachgebessert **bevor** ich es sehe —
nicht danach.

---

## 7 · Zielformat

- **9:16**, 1080×1920, für Instagram Reels
- Zielängen: Reichweiten-Reel **15–30 s** · Mehrwert-Reel **30–60 s** ·
  B-Roll-Reel **~7 s** (nur der Hook gesprochen, der Rest steht in der Caption —
  siehe `feedback_broll-reel-format` im Memory)
- Zwei Profile mit unterschiedlicher Tonalität: **Mentoring** und **doTERRA**.
  Bei doTERRA gilt zusätzlich: keine Heilversprechen, „bei mir war"-Frame.

---

## 8 · Was ich sage und was ich selbst mache

**In den Chat sage ich nur, was ich mir beim nächsten Video sparen will** —
also alles, was ich zum dritten Mal von Hand korrigiere. Das wandert dann als
Regel hier hinein.

**Seit Okt. 2026 muss ich es gar nicht mehr sagen** (Jenyas Lern-Schleife):
Claude legt den Rohschnitt als CapCut-Projekt an, ich ziehe die Kanten, beende
CapCut, und Claude liest meine Änderungen aus der Projektdatei
(`scripts/videoschnitt/capcut-projekt.py vergleichen`). **Eine Regel entsteht
erst, wenn dieselbe Art Änderung mindestens zweimal vorkommt** — einmal ist
Geschmack bei diesem einen Video. Und **eingetragen wird erst, wenn ich den
Vorschlag bestätigt habe.** Nach rund zehn Videos sitzt es.

Einmalige Kleinigkeiten korrigiere ich selbst in CapCut. Das geht schneller,
als sie zu erklären. Genau deshalb lasse ich mir die Einzelclips geben und kein
fertiges Video.

---

## 🔗 Verwandte Notizen

- [[reels-framework]] — Viral-Mechanik, 3-Sekunden-Regel, Reel-Typen
- [[hook-framework]] — woraus der Hook gebaut ist, der hier unantastbar bleibt
- [[caption-formeln]] — was in die Caption gehört statt ins Video
- [[patricia-freebies]] — die Keywords für den CTA am Schluss
