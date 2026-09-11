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


## 7 · Was die Profile besser machen (angeschaut 2026-09-11)

Patricias Referenzen: **anka.klh** (26k in 5 Monaten, Personal Brand) und
**alinascreatorclub** (UGC/Creator). Dazu die zwei aus dem Workbook — Kelsie
(Textebene) und jenya_kork (B-Roll-Hooks).

### anka.klh — die ruhige, teure Optik

- **Eine Serif über alles**, zweifarbig: Creme für den Vorlauf, Gold/Akzent für
  das betonte Wort. „Serien über **Serien**" · „Der Folge-mir-Trend **killt deinen
  Account**" · „Die neue Instagram **Erfolgsfalle**"
- **Kleine kursive Unterzeile** unter der Headline, halb so gross
- **Serien-System:** „Folge 1", „Folge 3", „Woche 5/42" — macht aus Einzelposts
  eine Reihe, auf die man wartet
- **Gestapelte Info-Pillen** für Zwischenstände: „Ziel 1: … · Aktuell: 1.028 Follower"
- **Untertitel Wort für Wort**, immer nur eins, klein und mittig unten
- **Screenshot als Beweis** mitten im Reel, klein über dem Bild
- Kein einziger Schnitt in 76 Sekunden — die Ruhe ist Teil der Wirkung

### alinascreatorclub — der schnelle, verspielte Stil

- **Schrift-Mix innerhalb eines Satzes:** fette Sans + Serif kursiv Wort für Wort
  („**große** *Creator*")
- **Farbige Marker** hinter einzelnen Wörtern, Rosa/Creme
- **B-Roll mit Textblock oben** und ohne Sprechen — genau Patricias Format

### Was davon in die B-Roll-Pipeline gehört

| Baustein | Stand |
|---|---|
| Zweifarbige Serif-Headline (Creme + Akzent) | ✅ gebaut — `stil: serif` setzt das betonte Wort in der Akzentfarbe |
| Weicher Schleier statt Kasten | ✅ gebaut — `grund: "verlauf"`, läuft in seiner eigenen Fläche aus |
| **CTA erst am Schluss und allein** | ✅ gebaut — `zusatz` startet automatisch 2,6 s vor Ende, steuerbar über `zusatz_ab` |
| **Schnittwechsel alle 2–3 s** | ✅ über mehrere Segmente in der Schnittliste, auch aus **einer** Quelle an verschiedenen Stellen |
| Zoom je Schnitt | ✅ `zoom.modus: "auto"` nimmt die Clipgrenzen |
| Serien-Marker („Folge 1 von 3") | ⏳ als `elemente`-Chip möglich, noch nicht als eigener Baustein |
| Gestapelte Info-Pillen | ⏳ `elemente` mit `typ: "chip"`, Stapel-Layout fehlt |
| Wort-für-Wort-Untertitel (nur ein Wort) | ⏳ vorhanden sind Gruppen, Einzelwort fehlt |
| Schrift-Mix pro Wort | ⏳ offen |
| Screenshot-Einblendung | ⏳ offen — braucht einen Bild-Elementtyp |

**Wichtig:** Untertitel-Bausteine brauchen Sprache. Für B-Roll ohne Ton zählen
Schnitt, Zoom, Typo und der späte CTA — das ist der ganze Hebel.

---

## Das Cover-System ✅ festgelegt 2026-09-10

Gebaut mit `scripts/videoschnitt/cover.py`. **Zwei Arten im Wechsel**, damit der
Feed nicht jeden Tag gleich aussieht:

| Art | Aufbau |
|---|---|
| **foto** | Bild (Shootingbild oder Videostandbild) + weicher Farbschleier über dem ganzen Bild, der nach unten dichter wird, aber nie ganz zumacht |
| **farbe** | Vollfläche in einer Brandfarbe, ganz ohne Bild |

**Farbe rotiert automatisch:** Petrol → Dunkelblau → Orange. Merkzettel in
`outputs/reels/_cover-verlauf.json`.

**Typografie:** Philosopher für die Headline in Creme, **ein** Wort in Orange.
Source Sans 3 für die Unterzeile. Die Headline wird im Browser **eingepasst**,
nicht geschätzt — so gross wie möglich, höchstens drei Zeilen.

**Zwei Sachen, die leicht schiefgehen:**
- Der Schleier darf nicht als **Balken mit harter Kante** unten liegen. Er
  gehört über das ganze Bild, sonst sieht es nach Aufkleber aus.
- Instagram zeigt im Feed-Raster nur das **mittige 4:5** eines 9:16-Covers. Der
  Text muss innerhalb dieser Zone sitzen, sonst ist er im Raster abgeschnitten.

**Bildquelle:** 347 der 1007 Shootingbilder sind Hochformat — davon wird
ausgewählt, nicht vom Videostandbild. Ein Querformat-Foto geht auch, wenn
Patricia nicht mittig steht; der Zuschnitt wird dann pro Post entschieden.

---

## 🚨 Der Clip muss nicht das Thema zeigen — er muss die Metapher tragen

**Festgehalten am 2026-09-10, nachdem Claude es falsch herum gedacht hatte.**

Claude hatte zu einem Business-Hook einen passenden Clip gesucht, keinen
gefunden und daraus geschlossen, es fehle Material. Falsch. Patricias
Denkrichtung ist die umgekehrte:

> **Erst den Clip anschauen, dann den Hook finden, den dieser Clip möglich macht.**

Ihr Beispiel, an einem Blumenkohl im Garten:

> „Bevor du Gurken erntest, säst du doch Gurken aus, oder? Warum hast du dann das
> Gefühl, dass es bei deinem Networkbusiness und der Kundenfindung über Instagram
> anders läuft?"

Damit trägt ein Gemüse-Clip einen Business-Post. Das Bild ist die **Metapher**,
nicht die Illustration.

**Heisst konkret:** Strandspaziergang, Kochen, Wandern, Garten, Kinder — alles
brauchbar. Es gibt kein „unpassendes" Material, es gibt nur einen fehlenden
Gedanken dazu. Bevor Claude sagt, es fehle Material, schaut es sich erst an,
**wofür die vorhandenen Clips stehen könnten**.

**Wann ein Clip trotzdem nicht geht:** wenn er zu kurz ist (unter ~6 Sekunden
trägt kein Reel) oder wenn weder Bewegung noch Stimmung da ist, an der das Auge
hängen bleibt.

### Drei harte Regeln für jeden B-Roll-Hook

1. **In drei Sekunden muss klar sein, worum es geht.** Wer erst nach fünf
   Sekunden versteht, ist schon weg.
2. **Symptombewusst, problembewusst oder wunschbewusst — nie produktbewusst.**
   Die Leserin denkt in ihrem Symptom, nicht in Patricias Lösungswort.
   Siehe `feedback_hooks-symptombewusst-nicht-produktbewusst`.
3. **Der ganze Inhalt gehört in die Caption**, auf dem Bild steht nur der Hook.

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
