---
tags: [videoschnitt, animationen, brand]
---

# Animations-Bibliothek — hinterlegte Stile für Reels

Damit Claude nicht bei jedem Reel neu fragt, wie es aussehen soll, stehen hier
**benannte Stile**. Im Briefing reicht dann der Name: „Reel 3, Stil **Beweis-Collage**".

Jeder Stil ist nach den vier Angaben beschrieben, die eine Animation überhaupt
erst brauchbar machen (Kapitel 06 des Jenya-Guides):
**Aussehen · Bewegung · Stelle · Sound.**

**Gebaut wird alles mit `scripts/videoschnitt/textebene.py`.** Was dort noch nicht
kann, steht beim Stil dabei — dann ist es ein Bau-Auftrag und keine Vorgabe.

---

## 1 · Kelsie-Textebene ✅ gebaut

Der Stil, den Patricias Mentorin vorgegeben hat. Für Talking Heads mit einem
betonten Wort pro Aussage.

| | |
|---|---|
| **Aussehen** | Zwei Zeilen auf Stoss. Oben dünn und klein (Poppins Light, 46 px, weiss). Darunter das betonte Wort gross und durchscheinend (Poppins Bold, Farbverlauf im Buchstaben, 62 % Deckkraft). Kein Zeilenabstand. |
| **Bewegung** | Auftritt abwechselnd: von links, von rechts, aufgepoppt. Ausblenden mit einem kurzen Weichzeichner am Ende. |
| **Stelle** | Auf dem gesprochenen Wort — `ab_wort` im Briefing, nie eine Sekundenzahl. |
| **Sound** | keiner. Der Text soll die Stimme nicht überlagern. |

**Dazu:** das grosse Wort liegt **hinter** Patricia. Braucht einmal
`npx hyperframes remove-background` auf den Rohschnitt.

---

## 1b · Kelsie-Textebene, volle Fassung 🔨 zu bauen

**Angesehen am 2026-09-10 auf `_k.elsie` (Profil + laufende Reels, über Chrome).**
Ihr tatsächliches System ist reicher als die Beschreibung, die Patricia bekommen
hat. Die vier Unterschiede, die den Look ausmachen:

**1 · Der Satz baut sich Wort für Wort auf.** Nicht der ganze Block auf einmal.
Erst steht „Every," allein, dann kommt „neighborhood," dazu, dann „lot". Jedes
Wort erscheint, wenn sie es sagt — dadurch liest man mit, statt vorauszulesen.

**2 · Zwei Schriften im selben Block.** Die Verbindungswörter sind dünn und
kursiv („Every,", „that's", „than the rest."), das betonte Wort ist entweder
**Script kursiv** („neighborhood,") oder **fett in Versalien** („BETTER"). Der
Kontrast zwischen den beiden ist der eigentliche Effekt.

**3 · Die Akzentfarbe wechselt pro Block.** Bei ihr Violett, dann Gelbgrün, dann
Koralle — nicht eine Farbe durchs ganze Reel.
⚠️ **Für Patricia:** Petrol → Orange → Dunkelblau. **Kein Gelb**, das ist nicht
ihre Marke.

**4 · Vorne und hinten gemischt.** Das betonte, farbige Wort liegt **hinter**
ihr, die dünnen weissen Verbindungswörter **vor** ihr. Beides im selben Block.

| | |
|---|---|
| **Aussehen** | Pro Block 2–3 Zeilen, eng gestapelt und leicht überlappend. Dünn-kursiv in Weiss für die Verbindungswörter, das betonte Wort gross in der Akzentfarbe — abwechselnd Script kursiv oder fett in Versalien. |
| **Bewegung** | Wort für Wort, jedes auf seinem gesprochenen Wort. Kein gemeinsamer Auftritt. |
| **Stelle** | Jedes Wort einzeln über `ab_wort`. |
| **Sound** | keiner. |

**Was `textebene.py` dafür noch braucht:** Wort-für-Wort-Aufbau innerhalb eines
Blocks, eine zweite Schrift (Script) und die Farbrotation pro Block. Aktuell
baut das Skript den ganzen Block auf einmal mit einer Farbe.

---

## 2 · Beweis-Collage 🔨 zu bauen

Abgeschaut bei `_k.elsie` (Post DNiTQiExBW-, angesehen 2026-09-10). Der Trick
dort: Bewertungs-Screenshots liegen als **einheitlich eingefärbte** Karten im
Raum — dadurch wirken sie wie ein Design-Element und nicht wie hingeworfene
Screenshots. Genau das macht den Unterschied zwischen „ich zeig euch mal
Feedback" und einem Post, der teuer aussieht.

| | |
|---|---|
| **Aussehen** | Links oder rechts im Bild ein leicht überlappender **Stapel aus 4–5 Screenshots**, alle in **einer** Akzentfarbe eingefärbt (Petrol fürs Mentoring, Orange für doTERRA), abgerundete Ecken, weicher Schatten. Dazu zweizeiliger Text: oben eine dünne Grotesk in Weiss, darunter ein **Script-Wort in der Akzentfarbe**, leicht überlappend und nach rechts versetzt. |
| **Bewegung** | Die Karten kommen **nacheinander** ins Bild, jede um 0,12 s versetzt, leicht von unten mit minimaler Drehung. Der Text erscheint danach. |
| **Stelle** | Auf dem Satz, in dem Patricia auf den Beweis zeigt („was meine Mamas sagen", „das schreiben sie mir"). |
| **Sound** | pro Karte ein leiser Klick, danach nichts. |

**Material liegt bereit:** 13 Testimonials in
`outputs/produkte/mba-launch/img/testimonials/t01–t13.jpg` (im Workspace, geprüft
2026-09-10). Auf dem Handy gibt es aktuell **kein** Testimonials-Album mehr — der
Workspace ist die Quelle.

**Zwei Entscheidungen offen:**
- **Script-Schrift.** Patricias Brand hat keine. Vorschlag: `Caveat` (handschriftlich,
  passt zum Nahbar-Anspruch) — muss sie freigeben, es ist eine echte Brand-Erweiterung.
- **Einfärben oder Original?** Einfärben sieht besser aus, macht die Screenshots aber
  schlechter lesbar. Bei Kelsie sind sie auch nicht lesbar — sie sind Beweis, kein Text.

---

## 3 · Profil-Verweis 🔨 zu bauen

Für Reels, die auf die Bio zeigen („was du bei mir findest").

| | |
|---|---|
| **Aussehen** | Screenshot von Patricias Instagram-Profil als Karte im Bild, leicht gekippt, mit weichem Schatten. Die relevante Bio-Zeile bekommt einen **handgezogenen Kringel** in der Akzentfarbe. |
| **Bewegung** | Karte poppt auf, danach zeichnet sich der Kringel in ~0,5 s. |
| **Stelle** | Auf dem Satz, in dem sie die Bio nennt. |
| **Sound** | einmal Pop beim Auftauchen. |

**Was fehlt:** ein aktueller Profil-Screenshot. Patricia macht ihn und legt ihn in
`Content-Inbox` — dann hole ich ihn mit `/handy`.

---

## 4 · B-Roll-Minimal ✅ gilt schon

Patricias festgelegtes B-Roll-Format, hier nur der Vollständigkeit halber.

| | |
|---|---|
| **Aussehen** | Ein einziger normaler Alltagsclip, ~7 Sekunden, **nur der Hook** als Overlay. |
| **Bewegung** | keine. Kein Schnitt, keine Einblendungen. |
| **Stelle** | Hook steht von Anfang an. |
| **Sound** | **Trending-Sound aus Instagram, nativ gepostet.** |

⚠️ **Deshalb geht dieser Stil nicht über Blotato.** Trending-Sounds gibt es nur
beim Posten in der App. Wer B-Roll über Blotato plant, verliert genau den Hebel,
für den das Format gebaut ist. → B-Roll bleibt Handarbeit in der App.

---

## Wie ein Stil dazukommt

Patricia schickt einen Screenshot oder einen Link, Claude schaut ihn sich über
Chrome an (Instagram gibt ohne Login nichts raus — WebFetch reicht nicht) und
beschreibt ihn nach den vier Angaben. Dann kommt er hier rein.

**Nicht raten.** Wenn eine der vier Angaben unklar ist, wird gefragt.
„Mach eine schöne Animation dazu" ergibt Vorlagen-Optik.

---

## 🔗 Verwandte Notizen

- [[videoschnitt-regeln]] — die Schnitt-Regeln, auf denen das aufsetzt
- [[reels-framework]] — welcher Reel-Typ wann
- [[content-assets-index]] — wo das Material liegt
