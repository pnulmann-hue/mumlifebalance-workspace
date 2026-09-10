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
