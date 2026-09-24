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

---

## 2 · Was immer rausfliegt

- Der Vorlauf am Anfang, bis zum **ersten Wort des Hooks** (Kamera richten, Luft holen, „so, okay")
- Versprecher und abgebrochene Satzanfänge
- Alle Anläufe eines Satzes ausser dem letzten vollständigen (siehe oben)
- Pausen, die länger als **1,5 Sekunden** sind
- Räuspern, Husten, „ähm", „also ähm"
- Alles nach meinem Schlusssatz (der CTA ist das Ende, danach kommt nichts mehr)
- [Meine typischen Füllwörter — ergänze ich nach dem ersten Durchgang]

---

## 3 · Was bleibt, auch wenn es holprig ist

- **Der Hook** — die ersten Sätze, wortwörtlich so, wie ich sie gesprochen habe.
  Der ist vorher geschrieben und geübt. Nie glattziehen, nie kürzen, nie „verbessern".
- Der **Keyword-CTA am Schluss** („Kommentier mir …") — vollständig, inklusive
  des Keywords. Keywords stehen in `context/patricia-freebies.md`.
- **Kurze Denkpausen mitten im Satz** — die gehören zu meiner Art zu reden.
  Nur echte Löcher (> 1,5 s) fliegen raus.
- Meine Umgangssprache und der Schweizer Einschlag. Nichts hochdeutsch machen.
- [Fester Satz, der die Reihe benennt — falls ich sowas einführe]

---

## 4 · Wie eng geschnitten wird

- **250 ms** Luft vor jedem Satzanfang
- **150 ms** Luft nach jedem Satzende
- **Nie mitten in ein Wort schneiden.** Immer an der Wortgrenze aus `words.json`.
- Lieber ein Atemzug zu viel als ein Video, das gehetzt klingt. Gehetzt ist der
  häufigste Anfängerfehler.

---

## 4b · Rhythmus und Ton

Eingearbeitet aus der Analyse von @alinascreatorclub (Sept. 2026) — ihre CapCut-
Bibliotheksnamen nützen uns nichts, aber die **Logik dahinter** ist übertragbar.
Unsere Sounds baut `textebene.py` selbst mit ffmpeg, damit keine Lizenzfrage entsteht.

### Der Grundsatz
**Ein Ton sitzt auf dem Moment, in dem sich im Bild etwas ändert — nie flächig
darüber.** Wenn ein Ton nicht sagen kann, zu welchem sichtbaren Ereignis er gehört,
gehört er nicht ins Video.

### Wann welcher Ton

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
- [ ] Klingt kein Übergang gehetzt (250 ms Luft überall eingehalten)?
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

Einmalige Kleinigkeiten korrigiere ich selbst in CapCut. Das geht schneller,
als sie zu erklären. Genau deshalb lasse ich mir die Einzelclips geben und kein
fertiges Video.

---

## 🔗 Verwandte Notizen

- [[reels-framework]] — Viral-Mechanik, 3-Sekunden-Regel, Reel-Typen
- [[hook-framework]] — woraus der Hook gebaut ist, der hier unantastbar bleibt
- [[caption-formeln]] — was in die Caption gehört statt ins Video
- [[patricia-freebies]] — die Keywords für den CTA am Schluss
