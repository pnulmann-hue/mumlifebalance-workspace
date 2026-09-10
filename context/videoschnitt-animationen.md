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

## 4 · Marker-Hook ✅ gebaut — **der Jenya-B-Roll-Stil**

Angesehen am 2026-09-10 bei `jenya_kork` (Post Dciv4ZggNX9). **Das ist B-Roll mit
gestaltetem Text** — genau das Format, das Patricia für ihre B-Roll-Reels will.

Sie sitzt am Schreibtisch und schreibt auf Klebezettel, **von der Seite gefilmt,
nicht in die Kamera**. Kein gesprochenes Wort. Der ganze Inhalt steht in der
Caption („Meine Strategie für die nächsten 70 Tage ↓"), der Ton ist ein
Trending-Audio.

| | |
|---|---|
| **Aussehen** | Hook in zwei Teilen, mittig-links im Bild. Erster Teil weiss und fett mit dunkler Kontur („was ist"). Zweiter Teil mit einem **Marker-Balken in der Akzentfarbe dahinter** („der Plan?"), leicht schief wie mit dem Textmarker gezogen. Darunter eine **kleine dünne Zeile** in Weiss, die die Frage konkretisiert. |
| **Bewegung** | Der Marker-Balken **wischt von links nach rechts auf**, ~0,35 s, danach steht alles still. Sonst keine Bewegung. |
| **Stelle** | Ab Sekunde 0. Der Hook steht das ganze Reel. |
| **Sound** | Trending-Audio, in der App gewählt. |

**Für Patricia:** Marker-Balken in Petrol oder Orange, weisse Schrift darauf.

---

## 5 · Serif-Mix ✅ gebaut — **der zweite Jenya-Stil**

Ebenfalls B-Roll, ebenfalls ohne Sprechen: sie läuft durch einen Raum, oder eine
Aufsicht auf einen Kaffee in ihrer Hand. Der Text steht **mittig oben**.

| | |
|---|---|
| **Aussehen** | Zentrierter Textblock, drei bis vier Zeilen, weiss in einer normalen Grotesk — und **genau ein Wort in kursiver Serifenschrift**, deutlich grösser („Ich habe aus *Claude* meinen besten Social Media Manager gemacht."). Unten rechts ein kleiner kursiver Serif-Zusatz („*wirklich?*") und darunter eine kleine Zeile, die auf die Caption zeigt. |
| **Bewegung** | Sehr ruhig: der Block blendet weich auf, das Serif-Wort kommt einen Tick später. |
| **Stelle** | Ab Sekunde 0. |
| **Sound** | Trending-Audio, in der App gewählt. |

**Gute Nachricht zur Schrift:** Dafür braucht es keine neue. **Philosopher
kursiv** — Patricias eigene Display-Schrift — macht genau diesen Effekt. Die
Caveat-Frage von oben erübrigt sich damit für diesen Stil.

---

## 6 · B-Roll-Minimal ✅ gilt schon

Die schlichteste Fassung, wenn es schnell gehen muss: ein Alltagsclip, ~7 Sek,
nur der Hook als schlichtes Overlay, Inhalt in der Caption, Trending-Sound.

⚠️ **Alle B-Roll-Stile (4, 5, 6) gehen nicht über Blotato.** Trending-Sounds gibt
es nur beim Posten in der App.

**Aber der Text kommt trotzdem von mir:** Ich rendere den Clip **mit
eingebranntem Overlay**, Patricia lädt ihn in der App hoch und wählt dort den
Sound. Sie muss also nichts selbst gestalten — nur hochladen und Ton wählen.

---

## Beim Drehen: jede B-Roll-Handlung mehrfach

Bei B-Roll wird **nicht gesprochen** — deshalb darf dieselbe Handlung beliebig
oft wiederholt werden. Patricia filmt jede Szene **zwei- bis dreimal von
verschiedenen Positionen** (von rechts, von links, näher dran), ohne etwas anders
zu machen. Daraus schneidet Claude einen Clip mit Perspektivwechsel statt einer
statischen Einstellung.

Das ist der billigste Qualitätssprung überhaupt: kein Equipment, keine neue
Fähigkeit, nur zweimal aufstehen.

Bei **Talking Head geht das nicht** — derselbe Satz wäre nie zweimal gleich, der
Ton würde nicht zum Bild passen. Dort bringen Zoom und Textebene die Bewegung.

**Gehört in jedes B-Roll-Drehbriefing.**

---

## Abwechslung ist Pflicht

**Kein Reel sieht aus wie das davor.** Vor jedem Build schaut Claude in
`outputs/reels/_stil-verlauf.md` nach, welche Stile zuletzt liefen, und nimmt
einen anderen. Rotiert wird auf drei Ebenen:

| Ebene | Wechselt |
|---|---|
| **Stil bei Talking Head** | Kelsie-Textebene → Beweis-Collage → Profil-Verweis |
| **Stil bei B-Roll** | Marker-Hook → Serif-Mix → B-Roll-Minimal |
| **Akzentfarbe** | Petrol → Orange → Dunkelblau (kein Gelb) |
| **Schrift des betonten Worts** | Philosopher kursiv ↔ fett in Versalien |
| **Auftritt** | von links → von rechts → aufgepoppt |

Wenn ein Stil zweimal hintereinander sinnvoll wäre, wird das begründet — nicht
stillschweigend gemacht.

---

## Zwei Vorbilder, zwei Systeme (geprüft 2026-09-10)

Wichtig zu trennen, sonst mischt man die falschen Zutaten:

**Kelsie Blevins (`_k.elsie`)** — fast ausschliesslich **Talking Head**. Von rund
zwanzig angesehenen Reels ist praktisch jedes sie selbst, sprechend, mit dem
Wort-für-Wort-Textsystem darüber (95'000 bis 1,2 Millionen Aufrufe). Echte B-Roll
gibt es bei ihr nur vereinzelt und läuft schlechter.
→ **Stile 1 und 1b gehören auf Talking Heads.**

**Jenya Kork (`jenya_kork`)** — das Gegenteil: **B-Roll ohne ein gesprochenes
Wort**, sie am Schreibtisch, beim Gehen, ein Kaffee von oben. Der gesamte Inhalt
steht in der Caption, der Hook ist **gestaltet** (Marker-Balken oder
Serif-Mix), der Ton ist Trending-Audio.
→ **Stile 4 und 5 gehören auf B-Roll.**

Das heisst: **B-Roll muss nicht schlicht sein.** Patricias eigene Regel („ein
Clip, nur der Hook als Overlay, Inhalt in der Caption") ist damit nicht verletzt
— Jenya hält sie ein, sie lässt den Hook nur gut aussehen. Genau das übernehmen
wir.

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
