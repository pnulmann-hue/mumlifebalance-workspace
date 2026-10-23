#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Baut die Beilagen fuer den Kurs „Claude Code fuer Network-Mamas".

    python scripts/ki-kurs/beilagen-bauen.py

Schreibt nach outputs/produkte/ki-treppe/beilagen/. Wiederholbar.

Alles hier ist eigener Text. Aus fremden Kursen kommt nichts herein —
weder Formel-Sammlungen noch Vorlagen noch Beispiele.
"""
import io, os, sys

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
ZIEL = "outputs/produkte/ki-treppe/beilagen"

KOPF = "Claude Code fuer Network-Mamas · Mum Life Balance"

DATEIEN = {}

# ─────────────────────────────────────────────────────────── Roadmap

DATEIEN["roadmap-drei-stufen.md"] = """# Deine Roadmap — die drei Stufen

Du musst nicht bis nach oben. Auf jeder Stufe hast du am Ende etwas, das du
behältst, und du entscheidest selbst, ob du weitergehst.

---

## Stufe 1 · Claude Chat

**Was du benutzt:** den ganz normalen Chat im Browser oder auf dem Handy.

**Was du danach kannst:** Deine KI klingt nach dir, weil dein eigenes Wissen als
Projekt dort liegt statt in jedem Chat neu getippt zu werden.

**Was es kostet:** Zum Anfangen reicht ein Gratis-Konto.

**Woran du merkst, dass diese Stufe dran ist:** Du benutzt KI schon, aber du
baust jedes Ergebnis um.

---

## Stufe 2 · Claude Cowork

**Was du benutzt:** dieselbe Oberfläche, nur mit Dateien und Verbindungen.

**Was du danach kannst:** Die KI arbeitet mit deinen Dateien, hängt an deiner
eigenen Planung, und du hast einen Bot gebaut, ohne eine Zeile Code zu
schreiben.

**Was es kostet:** ein Abo im niedrigen zweistelligen Bereich pro Monat.

**Woran du merkst, dass diese Stufe dran ist:** Du tippst dieselben Angaben
immer wieder in den Chat, weil er sie nicht kennt.

**Wo sie aufhört:** Der Bot läuft nicht von selbst. Du musst ihn jedes Mal
anstossen.

---

## Stufe 3 · Claude Code

**Was du benutzt:** die Desktop-App mit deinem eigenen Arbeitsplatz. Kein
schwarzes Fenster.

**Was du danach kannst:** Eigene Befehle für Arbeiten, die du jede Woche machst.
Einen Bot, der morgens von selbst schreibt, auch wenn dein Laptop zu ist.

**Was es kostet:** das Abo plus ein paar Franken im Monat für den Ort, an dem
der Bot wohnt.

**Woran du merkst, dass diese Stufe dran ist:** Du machst dieselbe Arbeit zum
dritten Mal und denkst, das müsste doch von allein gehen.

---

> **Der Satz, der für alle drei gilt:** Die KI bereitet vor, du entscheidest und
> gibst den letzten Schliff. Das ändert sich auf keiner Stufe.
"""

# ─────────────────────────────────────────────────────── Begriffe

DATEIEN["begriffe-cheatsheet.md"] = """# Die Wörter, die dauernd vorkommen

Zum Ausdrucken und neben den Laptop hängen. Keine Fachsprache, nur das, was du
wirklich wissen musst, um mitzukommen.

---

## Beim Reden mit der KI

**Auftrag (Prompt)** — was du hineinschreibst. Je genauer, desto besser das
Ergebnis. Ein guter Auftrag hat drei Zutaten: wer du bist, was rauskommen soll,
und ein Beispiel für gut.

**Kontext** — alles, was die KI in diesem Moment über dich und die Aufgabe
weiss. Sie weiss nichts von sich aus. Was nicht drinsteht, existiert für sie
nicht.

**Kontextfenster** — wie viel sie auf einmal im Kopf behalten kann. Ist es voll,
fällt hinten etwas heraus. Deshalb lieber ein neues Gespräch anfangen als ein
endloses weiterführen.

**Token** — die Einheit, in der KI rechnet. Ungefähr ein halbes bis ein Wort.
Musst du nicht verstehen, taucht nur in Abrechnungen auf.

**Modell** — welche Ausgabe der KI du benutzt. Eine schnellere für Einfaches,
eine gründlichere für Schwieriges.

**Halluzination** — wenn sie etwas erfindet und dabei völlig überzeugt klingt.
Passiert vor allem bei Zahlen, Namen und Links. Alles, was du behauptest,
prüfst du selbst nach.

---

## Beim Arbeiten mit Dateien

**Projekt** — ein Ort, an dem dein Wissen liegen bleibt, damit du es nicht in
jedem Gespräch neu erklärst.

**Ordner / Arbeitsplatz** — bei Claude Code ein Ordner auf deinem Rechner, in
dem deine Dateien, dein Wissen und deine Befehle zusammenliegen.

**.md-Datei** — eine ganz normale Textdatei. Das `md` steht für eine einfache
Art, Überschriften und Listen zu schreiben. Du kannst sie mit jedem
Texteditor öffnen.

**CLAUDE.md** — die eine Datei in deinem Arbeitsplatz, in der steht, was die KI
immer wissen soll. Das Gedächtnis deines Arbeitsplatzes.

**Business-Brief** — dein eigenes Wissensdokument: wer du bist, für wen du da
bist, wie du klingst. Geht bei jedem Auftrag mit.

---

## Beim Automatisieren

**Skill** — eine Arbeit, die du einmal aufschreibst und danach nur noch
aufrufst. Wie ein Rezept, das jedes Mal gleich abgearbeitet wird.

**Slash-Befehl** — wie du einen Skill aufrufst: ein Schrägstrich und der Name,
zum Beispiel `/caption`.

**Agent** — eine KI, die selbst arbeitet statt nur zu antworten:
nachschauen, ändern, prüfen, weitermachen.

**Bot** — dasselbe, nur dass ihn niemand mehr aufrufen muss. Er meldet sich von
selbst, zum Beispiel auf Telegram.

**Hosting** — der Ort, an dem dein Bot wohnt, damit er auch läuft, wenn dein
Laptop zu ist. Kostet ein paar Franken im Monat.

**Stecker (Connector, MCP)** — eine Verbindung zwischen der KI und einem
anderen Programm, etwa deiner Planung oder deinem Mailprogramm. Einmal
einrichten, dann liest sie dort mit.

**Artifact** — eine kleine eigene Seite mit Datenbank, die die KI baut und
befüllt und die du bedienst. Auch vom Handy aus.

---

## Bei der Technik drumherum

**Terminal** — das schwarze Fenster mit dem Text. **Du brauchst es in diesem
Kurs nicht.** Falls du es irgendwo siehst: nicht erschrecken, es ist nur eine
andere Art, dasselbe zu tun.

**Zugangsschlüssel (API-Key)** — eine lange Zeichenfolge, mit der sich ein
Programm bei einem anderen ausweist. **Wer den Schlüssel hat, ist drin.**
Gehört nie in eine Datei, die du weitergibst.

**Abo-Stufen** — die KI gibt es gratis, in einer mittleren Stufe und in einer
grossen. Was du wann brauchst, steht in Lektion 1.4.

---

> **Ein Satz zum Mitnehmen:** Die KI ist eine Praktikantin. Sie ist schnell,
> fleissig und weiss erschreckend viel — aber sie kennt weder dich noch dein
> Business, solange du es ihr nicht sagst.
"""

# ─────────────────────────────────────────── Business-Brief

DATEIEN["business-brief-vorlage.md"] = """# Dein Business-Brief

Das eine Dokument, das ab jetzt bei jedem Auftrag mitgeht. Jeder Skill liest es,
jeder Bot bekommt es mit, und alles, was danach geschrieben wird, klingt danach.

---

## So kommst du dazu — drei Wege

**Der schnellste:** Kopiere den Auftrag weiter unten in Claude und lass dich
ausfragen. Nach zehn Minuten hast du einen fertigen Brief.

**Der gründliche:** Fülle die sechs Bausteine von Hand aus. Bei jedem steht ein
Beispiel, an dem du dich entlanghangeln kannst.

**Der ehrliche:** Fang mit dem Auftrag an, und bessere danach von Hand nach.
So mache ich es selbst.

---

## Der Auftrag zum Kopieren

Alles zwischen den Linien markieren und in Claude einfügen.

---

```
Du hilfst mir, meinen Business-Brief zu schreiben. Das ist ein Dokument über
mein Business, das du ab jetzt bei jeder Aufgabe mitliest.

Der Brief hat sechs Bausteine:
1. Wer ich bin
2. Für wen ich da bin (meine Kundschaft)
3. Was ich anbiete
4. Meine Themen — und meine Nicht-Themen
5. Wie ich klinge
6. Meine Tabus

Geh mit mir Baustein für Baustein durch. Regeln dabei:

- Stell mir immer nur EINE Frage und warte auf meine Antwort.
- Wenn meine Antwort allgemein bleibt, frag nach, bis sie konkret ist.
  Bei „Mamas die überfordert sind" fragst du weiter, bis eine bestimmte
  Frau mit einer bestimmten Lage dasteht.
- Frag nach Beispielen aus meinem Alltag, nicht nach Beschreibungen.
- Korrigier mich nicht und mach nichts schöner. Nimm meine Worte.

Wenn wir bei Baustein 5 sind, bitte mich um zwei, drei Texte, die ich selbst
geschrieben habe, und lies daraus, wie ich klinge.

Am Ende schreibst du den ganzen Brief als eine Datei. Danach fragst du mich,
was noch nicht stimmt, und änderst es.

Fang mit der ersten Frage an.
```

---

🚨 **Wenn du ihn geschrieben hast, lies ihn einmal laut.** Was du so nie sagen
würdest, gehört geändert — sonst steht es ab jetzt in jedem Text.

---

# Die sechs Bausteine

Bei jedem steht, was hineingehört, und wie es bei **Sandra** aussieht. Sandra
gibt es nicht wirklich — sie ist erfunden, damit du an einem durchgehenden
Beispiel siehst, wie die Teile zusammenpassen.

---

## 1 · Wer ich bin

*Name, was du machst, seit wann. Und drei bis fünf Sätze, die eine Freundin über
dich sagen würde, wenn sie dich jemandem vorstellt.*

**Bei Sandra:**

> Sandra, 38, drei Kinder zwischen 4 und 11. Ich zeige Mamas ab 35, wie sie
> wieder durch den Tag kommen, ohne abends nur noch aufs Sofa zu fallen.
> Vorher war ich zwölf Jahre in der Spitex und kenne Schichtbetrieb mit Kindern
> von innen. Ich habe zwei Jahre gebraucht, bis ich kapiert habe, dass es nicht
> an mir lag. Ich rede gern Klartext und finde Selbstoptimierung anstrengend.

**Bei dir:**

```

```

---

## 2 · Für wen ich da bin

*Deine Kundschaft: Frauen, Männer, Familien, Firmen, wer auch immer es bei dir ist.
So genau wie möglich, auch wenn es sich eng anfühlt: in welcher Lage steckt diese
Person, was hat sie schon probiert, was denkt sie nachts um halb elf.*

**Bei Sandra** (ihre Kundschaft sind tatsächlich Mamas, das ist ihre Nische):

> Mama zwischen 33 und 45, ein bis drei Kinder, arbeitet 40 bis 80 Prozent.
> Sie steht morgens auf und ist schon müde. Sie hat Eisen prüfen lassen, sie
> war beim Arzt, es ist alles in Ordnung — und sie fühlt sich trotzdem, als
> würde sie durch Pudding laufen. Sie hat schon drei Sachen ausprobiert und
> nach zwei Wochen aufgehört, weil im Alltag keine Zeit dafür war.

**Der Satz, den sie selbst sagen würde:**

> „Ich funktioniere, aber ich lebe nicht."

**Bei dir:**

```

```

Und ihr Satz:

```
„"
```

---

## 3 · Was ich anbiete

*Jedes Angebot mit Namen, Preis und dem einen Ergebnis, das sie danach hat.
Keine Modul-Listen — was ändert sich für sie?*

**Bei Sandra:**

| Angebot | Preis | Was sie danach hat |
|---|---|---|
| 5 Morgen-Ideen | 0 | Einen Morgen, der nicht mit Hetze anfängt |
| Der Energie-Start | 29 | Drei Wochen, in denen sie merkt, was ihr wirklich Kraft zieht |
| Wieder wach | 240 | Einen Alltag, in dem sie um 16 Uhr noch da ist |

**Bei dir:**

| Angebot | Preis | Was sie danach hat |
|---|---|---|
| | | |
| | | |

---

## 4 · Meine Themen

*Worüber du sprichst, und ausdrücklich auch, worüber nicht. Das Zweite ist
wichtiger, als es aussieht.*

**Bei Sandra:**

> Ich spreche über: Energie im Alltag mit Kindern · Schlaf, der wirklich
> erholt · warum Disziplin nicht das Problem ist · kleine Umstellungen, die
> zwischen Tür und Angel passen.
>
> Ich spreche nicht über: Abnehmen · Sport-Programme · alles, was nach
> Selbstoptimierung klingt · Diagnosen.

**Bei dir:**

```
Ich spreche über:

Ich spreche nicht über:
```

---

## 5 · Wie ich klinge

*Duzen oder siezen. Lange Sätze oder kurze. Emojis oder keine. Was du oft
sagst. Und was du nie sagen würdest.*

**Bei Sandra:**

> Ich duze. Ich schreibe, wie ich rede — eher lange Sätze mit „und" und „weil"
> als abgehackte Zeilen. Kaum Emojis, höchstens mal eines am Schluss.
> Ich sage oft „ehrlich gesagt" und „bei mir war das so". Ich sage nie
> „Mindset", „Journey" oder „du schaffst das schon".

**Zwei, drei eigene Texte anhängen** — eine Caption, eine Mail, irgendetwas,
das du selbst geschrieben hast. Das bringt mehr als jede Beschreibung.

**Bei dir:**

```

```

```
Textprobe 1:

Textprobe 2:
```

---

## 6 · Meine Tabus

*Wörter, Behauptungen und Themen, die bei dir nie vorkommen. Wenn du im Network
bist, gehören die Regeln deines Partnerunternehmens hierher — die kennst du,
die KI nicht.*

**Bei Sandra:**

> Nie verwenden: heilt · lindert · wirkt gegen · Erfolgsgarantie ·
> „in nur 7 Tagen".
>
> Nie behaupten: dass ein Produkt etwas heilt oder eine Krankheit beeinflusst ·
> dass jemand anderes ein bestimmtes Einkommen erreichen wird · Zahlen, die
> ich nicht selbst erlebt habe.

**Bei dir:**

```
Nie verwenden:

Nie behaupten:
```

---

> **Die Prüffrage, wenn du fertig bist:** Könnte jemand, der dich nicht kennt,
> mit diesem Dokument einen Text schreiben, den deine Kundschaft für deinen hält?
> Wenn nein, fehlt fast immer Baustein 5.
"""

# ────────────────────────────────────────────────── Buch-Technik

DATEIEN["buch-technik-auftrag.md"] = """# Die Buch-Technik — der Auftrag zum Kopieren

Wenn du vor dem leeren Business-Brief sitzt und nicht weisst, wo anfangen:
Lass die KI fragen, statt selbst zu formulieren.

**So gehst du vor:** Kopiere den Auftrag unten in ein neues Gespräch. Antworte
in ganzen Sätzen, so wie du reden würdest. Lass sie mindestens drei Runden
nachfragen, bevor sie schreibt.

---

```
Du schreibst ein Buch über mich und mein Business. Bevor du eine Zeile
schreibst, willst du mich richtig kennen.

Stell mir Fragen. Eine nach der anderen, nicht alle auf einmal. Frag nach,
wenn meine Antwort zu allgemein ist — besonders bei allem, was nach
Marketing-Sprache klingt. Frag nach Beispielen, nach Situationen, nach
Sätzen, die ich wirklich gesagt habe.

Du willst am Ende sechs Dinge wissen:
1. Wer ich bin und wie ich hierhergekommen bin
2. Für wen ich arbeite, so genau wie möglich
3. Was ich anbiete und was die Kundin danach hat
4. Worüber ich spreche und worüber ausdrücklich nicht
5. Wie ich klinge — meine Wörter, meine Satzlänge, mein Ton
6. Was bei mir nie vorkommt

Fang mit der ersten Frage an. Hör nicht auf zu fragen, solange du zu einem
der sechs Punkte noch raten müsstest.
```

---

**Wenn sie genug hat**, sagst du:

```
Gut. Schreib mir daraus mein Wissensdokument, in sechs Abschnitten, genau in
der Reihenfolge oben. Schreib in meinen Worten, nicht in deinen. Wo du etwas
nicht weisst, schreib „offen" hin statt etwas zu erfinden.
```

---

> **Warum das besser funktioniert als selber tippen:** Beim Antworten auf eine
> konkrete Frage fällt dir ein, was dir vor dem leeren Blatt nicht einfällt.
> Und das „offen" am Schluss zeigt dir genau, wo du noch nachdenken musst.
"""

# ────────────────────────────────────────────────── Skill-Gerüst

DATEIEN["skill-geruest.md"] = """---
name: dein-skill-name
description: "Ein Satz, woran die KI erkennt, wann dieser Skill dran ist."
---

# [Name des Skills]

> Leeres Gerüst. Ersetze alles in eckigen Klammern.
> Dateiname und `name` oben müssen gleich sein.

## Zweck

[Was diese Arbeit erledigt, in zwei Sätzen. Was am Ende dasteht, nicht wie du
dorthin kommst.]

## Bevor du anfängst

[Welche Dateien die KI zuerst lesen soll. Bei den meisten Skills mindestens
dein Business-Brief.]

- `business-brief.md`
- [weitere Datei]

## Was ich wissen muss

[Welche Angaben du beim Aufruf mitgibst. Wenn eine fehlt, soll die KI nachfragen
statt raten.]

1. [Angabe]
2. [Angabe]

## Regeln

[Deine Regeln. Das ist der Teil, der diesen Skill zu deinem macht. Schreib auch
auf, was NICHT passieren darf.]

- [Regel]
- [Regel]
- Nie: [Verbot]

## Was herauskommen soll

[Ganz genau. Wie viele Stücke, in welcher Form, wie lang. „Fünf Vorschläge, je
höchstens zwei Sätze" statt „ein paar Ideen".]

## Beispiel

[Ein einziges gutes Beispiel bringt mehr als drei Absätze Erklärung. Nimm etwas,
das du selbst gemacht hast und gut findest.]

**Eingabe:**
```
[...]
```

**Gutes Ergebnis:**
```
[...]
```

## Der letzte Check

[Zwei bis fünf Fragen, die vor der Abgabe beantwortet sein müssen. Eine mit Nein
heisst: nochmal.]

1. [Frage]
2. [Frage]

---

> **Die wichtigste Regel für dich selbst:** Was du dreimal von Hand korrigierst,
> gehört als Regel hier hinein. Sonst korrigierst du es ein viertes Mal.
"""

# ───────────────────────────────────────────── Sicherheits-Checkliste

DATEIEN["sicherheits-checkliste.md"] = """# Was nie in einen Arbeitsplatz gehört

Bei mir lagen Zugangsschlüssel im Klartext und die Daten von zweiunddreissig
Kundinnen offen abrufbar. Aufgefallen ist es niemandem. Gefunden wurde es nur,
weil einmal jemand gezielt nachgesehen hat.

Diese Liste ist das, was ich daraus gelernt habe.

---

## Die drei Regeln

**1 · Kein Zugangsschlüssel im Text einer Datei.**
Schlüssel kommen aus einer eigenen Datei daneben, die ausdrücklich nicht
mitgegeben wird. Fehlt der Schlüssel, soll dein Skript abbrechen und es sagen —
nie mit einem eingebauten Ersatzwert weiterlaufen.

**2 · Keine Daten anderer Menschen im Arbeitsplatz.**
Namen, Mailadressen, Telefonnummern, Kundennummern gehören in eine eigene
Datei, die ebenfalls nicht mitgeht. Auch wenn es nur drei Leute sind.

**3 · Zusagen an Kundinnen gelten auch hier.**
Wenn jemand dir ein Feedback mit „nur intern" gegeben hat, dann gilt das auch
für die Datei, in der du es sammelst.

---

## Die Liste zum Durchgehen

- [ ] Steht irgendwo ein Zugangsschlüssel im Klartext?
- [ ] Steht irgendwo eine fremde Mailadresse oder Telefonnummer?
- [ ] Liegen Kundenlisten oder Bestelldaten im Arbeitsplatz?
- [ ] Gibt es eine Datei mit gespeicherten Anmeldedaten aus dem Browser?
- [ ] Steht in einer Datei etwas, das du einer Kundin über eine andere Kundin
      nicht zeigen würdest?
- [ ] Wenn du deinen Arbeitsplatz irgendwohin kopierst, etwa in eine
      Cloud-Ablage: kommen dabei Dateien mit, die du ausgeschlossen hattest?

Die letzte Frage ist die, die am häufigsten übersehen wird. **Eine Kopie in
einer Cloud-Ablage umgeht jede Ausschlussliste.**

---

## Wenn doch einmal etwas offen lag

**Löschen reicht nicht.** Wer den Schlüssel in der Zwischenzeit kopiert hat,
kann ihn weiter benutzen, auch wenn die Datei weg ist.

1. **Schlüssel wechseln**, nicht entfernen. Bei den meisten Anbietern steht das
   unter Einstellungen als „zurücksetzen" oder „widerrufen".
2. **Den neuen Schlüssel überall eintragen**, wo der alte stand. Meistens ist
   das mehr als eine Stelle.
3. **Programme neu starten**, die den Schlüssel beim Start einlesen. Sonst
   arbeiten sie weiter mit dem alten und du wunderst dich über Fehlermeldungen.

---

## Was die KI schreibt, verantwortest du

Wenn du im Network arbeitest, gelten die Regeln deines Partnerunternehmens auch
für einen Text, den du nicht selbst getippt hast:

- [ ] Keine Aussage darüber, dass etwas eine Krankheit heilt, lindert oder
      verhindert
- [ ] Keine Einkommensversprechen, weder für dich noch für andere
- [ ] Keine erfundenen Erfahrungsberichte, auch keine „eine Kundin sagte"
- [ ] Keine Zahl, die du nicht belegen kannst

**Schreib diese Punkte als Verbote in deinen Business-Brief.** Dann prüft die KI
selbst mit, statt dass du es jedes Mal nachlesen musst.
"""

# ───────────────────────────────────────────── Floskel-Liste

DATEIEN["floskel-liste-vorlage.md"] = """# Woran man KI-Text erkennt

Leere Vorlage für deinen Arbeitsplatz. Die Muster unten sind der Anfang — die
Liste wird deine, sobald du deine eigenen Lieblingsärgernisse einträgst.

**So benutzt du sie:** Leg die Datei in deinen Arbeitsplatz und verweise in
jedem Text-Skill darauf. Dann prüft die KI ihren eigenen Text dagegen, bevor du
ihn siehst.

---

## Die Muster, die fast immer auftauchen

**Der Gegensatz nach Schema.** „Nicht X, sondern Y." In allen Varianten: es
geht nicht um … sondern um …, das Problem ist nicht … das Problem ist …,
weniger … mehr … Sprachmodelle bauen das reflexartig, weil es klug klingt und
leicht zu bauen ist.
→ *Korrektur:* zwei eigene Sätze daraus machen.

**Drei kurze Sätze hintereinander mit gleichem Anfang.** Klingt nach
Motivationsposter, nicht nach Mensch.
→ *Korrektur:* einen Punkt vertiefen statt drei aufzählen.

**Wörter, die nach Substanz klingen und keine haben.** Klarer Nutzen, echte
Ergebnisse, konkreter Plan, individuelle Lösung, praxisnah, auf Augenhöhe.
→ *Korrektur:* im selben Satz sagen, was genau gemeint ist.

**Die Pointe nach dem Doppelpunkt.** Ein Satz baut auf, der Doppelpunkt
verspricht die Auflösung, und dann kommt eine Allgemeinheit.

**Etwas passiert, ohne dass jemand etwas tut.** „Da entsteht etwas." „An dem
Punkt, an dem es kippt."
→ *Korrektur:* wer tut was, und was passiert dabei wirklich.

---

## Deine eigenen

*Trag hier ein, was DIR beim Gegenlesen auffällt. Jedes Mal, wenn du beim Lesen
denkst „so würde ich das nie sagen", kommt es hierher.*

| So nicht | So sage ich es |
|---|---|
| | |
| | |
| | |

---

## Die Prüfung vor jeder Abgabe

1. Steht irgendwo ein Gegensatz nach dem Schema oben?
2. Stehen drei gleich gebaute Sätze hintereinander?
3. Steht ein Wort aus der Hülsen-Liste, ohne dass danach steht, was gemeint ist?
4. Lies den Text laut. Klingt er wie ein Mensch oder wie ein Poster?

**Eine Frage mit Ja heisst: nochmal.**

---

> **Der einzige Test, der wirklich zählt:** Würdest du diesen Satz so zu einer
> Freundin am Küchentisch sagen? Wenn nein, schreib ihn um.
"""

# ───────────────────────────────────────────── Checklisten je Modul

CHECK = {
1: ("Orientierung", [
  "Ich weiss, welche der drei Stufen bei mir gerade dran ist",
  "Ich habe das Begriffe-Cheatsheet ausgedruckt oder offen",
  "Ich weiss, was mich das im Monat kostet, und habe entschieden, womit ich anfange",
  "Ich habe ein Konto und komme hinein",
]),
2: ("Claude Chat", [
  "Ich habe einen Auftrag geschrieben, der alle drei Zutaten enthält",
  "Mein Business-Brief ist ausgefüllt — alle sechs Bausteine",
  "Zwei bis drei eigene Textproben hängen dran",
  "Ich habe ein Projekt angelegt und den Business-Brief hineingelegt",
  "Ich habe einen Text erzeugt, den ich so verwenden würde",
]),
3: ("Claude Cowork", [
  "Ich weiss, wann Cowork mehr bringt als der Chat",
  "Meine Planung ist angehängt und wird gelesen",
  "Ich habe einen Helfer gebaut, der etwas für mich tut",
  "Ich habe entschieden, ob ich auf Stufe 3 weitergehe",
]),
4: ("Claude Code einrichten", [
  "Claude Code läuft bei mir und ich komme hinein",
  "Ich habe das Grundgerüst heruntergeladen und geöffnet",
  "Ich weiss, wofür jeder Ordner da ist",
  "Meine CLAUDE.md ist ausgefüllt",
  "Ich habe einen Auftrag gegeben, der durchgelaufen ist",
]),
5: ("Skills", [
  "Ich kann sagen, was ein Skill ist und woraus er besteht",
  "Ich habe eine Liste mit Arbeiten, die ich dreimal gleich mache",
  "Ich habe einen eigenen Skill gebaut",
  "Ich habe ihn einmal von Hand nachgeschärft",
  "Ich weiss, worauf ich bei fremden Skills schaue",
]),
6: ("Bots", [
  "Mein Bot schreibt mir auf dem Handy",
  "Er läuft auch, wenn mein Laptop zu ist",
  "Ich weiss, wo ich nachschaue, wenn er schweigt",
  "Ich weiss, was er mich im Monat kostet",
]),
7: ("Social Media", [
  "Die Content-Skills liegen in meinem Arbeitsplatz",
  "Ich habe eine Wissensdatei mit meinem eigenen Wissen gefüllt",
  "Ich habe den Unterschied leer gegen gefüllt selbst gesehen",
  "Ich habe festgelegt, was bei mir geprüft wird, bevor etwas rausgeht",
  "Ich weiss, woran ich erkenne, dass ein Beitrag Murks ist",
]),
8: ("Produkte, Seiten und Mails", [
  "Die Produkt-Skills liegen in meinem Arbeitsplatz",
  "Ich habe eine Verkaufsseite bauen lassen und angeschaut",
  "Ich weiss, wie sie online geht",
  "Ich habe entschieden, ob ich meinen Mail-Anbieter anhänge",
]),
9: ("Dein Cockpit", [
  "Mein Cockpit steht und zeigt etwas an",
  "Ich weiss, was abends automatisch passiert",
  "Ich habe eine Regel dafür, wenn ich etwas von Hand mache",
]),
}

for nr, (titel, punkte) in CHECK.items():
    zeilen = "\n".join("- [ ] " + p for p in punkte)
    DATEIEN["checkliste-modul-%d.md" % nr] = """# Checkliste Modul %d · %s

Geh das hier durch, bevor du weitermachst. Was noch offen ist, holst du jetzt
nach — später wird es nicht leichter.

%s

---

> **Wenn ein Punkt offen bleibt:** Schreib dir auf, woran es gehakt hat, und
> geh zur Lektion zurück. Das kostet zehn Minuten und spart dir eine Woche
> Herumprobieren.
""" % (nr, titel, zeilen)

# ─────────────────────────────────────────────────────────── schreiben

os.makedirs(ZIEL, exist_ok=True)
# ─────────────────────────────────── Cowork-Auftrag (3.3)

DATEIEN["cowork-erster-bot.md"] = """# Dein erster Helfer in Cowork

Noch kein Bot, der von selbst läuft — aber schon einer, der dir eine Arbeit
abnimmt, die du sonst jede Woche von Hand machst.

**Was du dafür brauchst:** Claude Cowork und deinen Business-Brief.
Sonst nichts. Kein Programm, keine Installation.

---

## Schritt 1 · Business-Brief bereitlegen

Leg die Datei in den Ordner, mit dem Cowork arbeitet. Wenn du sie noch nicht
hast, komm später zurück — ohne sie klingt alles nach niemandem.

## Schritt 2 · Den Auftrag einfügen

Alles zwischen den Linien kopieren, die eckigen Klammern durch deine Angaben
ersetzen.

---

```
Lies zuerst meinen Business-Brief im Ordner.

Deine Aufgabe: [was er für dich tun soll, in einem Satz]

So soll das Ergebnis aussehen:
- [Form, Länge, Anzahl]
- [was immer dabei sein muss]
- [was nie vorkommen darf]

Bevor du anfängst, sag mir in zwei Sätzen, was du verstanden hast.
Wenn dir etwas fehlt, frag danach, statt es dir auszudenken.
```

---

## Schritt 3 · Einmal laufen lassen und meckern

Das erste Ergebnis ist selten gut. Sag genau, was dich stört — „zu lang",
„klingt nicht nach mir", „fang nicht mit einer Frage an". Dann nochmal.

## Schritt 4 · Den Auftrag nachschärfen

Was du zweimal bemängelt hast, schreibst du in den Auftrag hinein. Ab jetzt
musst du es nicht mehr sagen.

---

## So sieht es bei Sandra aus

Sandra ist erfunden — 38, drei Kinder, seit zwei Jahren im Network, und sie
baut ihr eigenes Thema auf: Energie für Mamas ab 35.

```
Lies zuerst meinen Business-Brief im Ordner.

Deine Aufgabe: Aus meinen Notizen der Woche drei Themen herausziehen, über
die ich auf Instagram sprechen könnte.

So soll das Ergebnis aussehen:
- Drei Themen, je ein Satz worum es geht und ein Satz warum es meine
  Kundin interessiert
- Jedes Thema muss aus meinen Notizen kommen, nicht aus deinem Wissen
- Keine Tipps zum Netzwerkaufbau, keine Aussagen über Produkte

Bevor du anfängst, sag mir in zwei Sätzen, was du verstanden hast.
Wenn dir etwas fehlt, frag danach, statt es dir auszudenken.
```

**Was Sandra danach geändert hat:** Nach dem zweiten Durchgang kam
„und schreib die Themen so auf, wie ich sie einer Freundin am Telefon
erzählen würde" dazu. Seitdem passt der Ton.

---

> **Heb dir diesen Auftrag auf.** In Modul 5 wird genau daraus dein erster
> Skill — dieselben Sätze, nur an einem festen Platz, damit du sie nie
> wieder tippen musst.
"""

# ─────────────────────────────────── CLAUDE.md-Vorlage (4.4)

DATEIEN["claude-md-vorlage.md"] = """# Deine CLAUDE.md — das Gedächtnis deines Arbeitsplatzes

Diese Datei liegt ganz oben in deinem Arbeitsplatz und wird bei **jedem**
Gespräch automatisch gelesen. Alles, was hier steht, musst du nie wieder
erklären.

**Der Unterschied zum Business-Brief:** Der Brief sagt, wer du bist und wie du
klingst. Diese Datei sagt, wie in deinem Arbeitsplatz gearbeitet wird — wo was
liegt, welche Regeln gelten, was es gibt.

---

## So füllst du sie — der Auftrag zum Kopieren

```
Ich baue gerade meinen Arbeitsplatz auf und möchte meine CLAUDE.md schreiben.
Das ist die Datei, die du bei jedem Gespräch als Erstes liest.

Stell mir dafür Fragen, eine nach der anderen:

1. Was mache ich beruflich, in einem Satz?
2. Welche Ordner habe ich und was liegt jeweils darin?
3. Welche Dateien sollst du immer mitlesen?
4. Welche Regeln gelten bei mir immer — Sprache, Anrede, Schreibweise?
5. Was soll nie passieren, ohne dass ich vorher gefragt werde?
6. Was gibt es bei mir, das du sonst nicht erraten könntest?

Wenn eine Antwort zu allgemein ist, frag nach. Schreib am Ende die ganze
Datei, kurz und in meinen Worten. Keine Überschrift ohne Inhalt.
```

---

## Der Aufbau — fünf Teile

### 1 · Was das hier ist

*Zwei, drei Sätze. Wer du bist, was in diesem Arbeitsplatz passiert.*

**Bei Sandra:**

> Hier arbeitet Sandra. Ich zeige Mamas ab 35, wie sie wieder durch den Tag
> kommen. Nebenher bin ich seit zwei Jahren im Network, aber mein Thema ist
> Energie, nicht das Produkt. In diesem Arbeitsplatz entstehen meine
> Instagram-Beiträge, meine Mails und meine Angebote.

### 2 · Wo was liegt

*Deine Ordner, je eine Zeile.*

**Bei Sandra:**

```
context/    mein Business-Brief, meine Stimme, meine Tabus
outputs/    alles Fertige — Beiträge, Mails, Angebote
reference/  Vorlagen und Beispiele, die ich wiederverwende
```

### 3 · Was immer mitgelesen wird

*Die Dateien, ohne die kein Auftrag funktioniert.*

**Bei Sandra:**

> Lies bei jeder Aufgabe zuerst `context/business-brief.md` und
> `context/meine-tabus.md`.

### 4 · Meine Regeln

*Was immer gilt — auch wenn ich es nicht dazusage.*

**Bei Sandra:**

> - Antworte auf Deutsch, in Schweizer Schreibweise mit ss statt ß.
> - Duzen, nie siezen.
> - Keine erfundenen Zahlen. Wenn du eine brauchst und keine hast, frag.
> - Keine Aussagen darüber, was ein Produkt bewirkt.
> - Nichts veröffentlichen, ohne dass ich es vorher gesehen habe.
> - Aus `reference` nie wörtlich abschreiben. Das ist Material von anderen —
>   zum Nachschlagen, nicht für meine Texte.

### 5 · Was ich gerade vorhabe

*Der Teil, der sich am häufigsten ändert. Hier steht, woran du arbeitest.*

**Bei Sandra:**

> Im Oktober baue ich mein erstes bezahltes Angebot, den Energie-Start für 29.
> Alles, was ich bis dahin schreibe, soll darauf hinführen.

---

## Deine Fassung

Kopiere das hier in deine `CLAUDE.md` und ersetze die Inhalte.

```markdown
# CLAUDE.md

## Was das hier ist


## Wo was liegt


## Was immer mitgelesen wird


## Meine Regeln


## Was ich gerade vorhabe

```

---

> **Die wichtigste Angewohnheit:** Was dich dreimal geärgert hat, schreibst du
> als Regel hinein. Nach drei Monaten ist diese Datei mehr wert als jede
> Anleitung, die du kaufen kannst — weil jede Zeile darin aus einem echten
> Ärgernis entstanden ist.
"""

gesamt = 0
for name, inhalt in sorted(DATEIEN.items()):
    pfad = os.path.join(ZIEL, name)
    with io.open(pfad, "w", encoding="utf-8", newline="\n") as f:
        f.write(inhalt.rstrip() + "\n")
    gesamt += len(inhalt)
    print("  %-34s %6d Zeichen" % (name, len(inhalt)))

print("")
print("%d Dateien, %d Zeichen -> %s" % (len(DATEIEN), gesamt, ZIEL))

# Umlaut-Waechter: umschriebene Umlaute im Kundentext sind ein Fehler
import re
AUSNAHMEN = ("bauen","dauert","Frauen","heute","zuerst","Abenteuer","neues","neue",
             "genaue","blaue","graue","schaue","nachschaue","anschauen","Auge","auch",
             "auf","aus","auss","laut","Haus","Maus","raus","draussen","brauchst",
             "brauche","brauchen","Frau","schauen","aufschreiben","Aufwand",
             "dauernd","individuell","individuelle","aktuell","Aktuelle","Manuell",
             "baue","baust","baut","gebaut","Umbau","aufbaue","aufbaut",
             "glaube","glaubt","erlaubt","kaufe","kauft","gekauft","laufe",
             "laeuft" if False else "laufen","laufend","Verlauf","schauen",
             "genau","genauso","schlau","grau","blau","Frauen","Pause",
             "Pausen","zuhause","Hause","Sofa" if False else "Bauart",
             "manuell","visuell","Duell","Statue","neuer","neuen","teuer","Steuer")
muster = re.compile(r"\b\w*(ae|oe|ue)\w*\b")
funde = []
for name, inhalt in DATEIEN.items():
    for w in muster.findall(inhalt) and muster.finditer(inhalt):
        wort = w.group(0)
        if wort.lower() in [a.lower() for a in AUSNAHMEN]:
            continue
        if any(wort.lower().startswith(a.lower()) for a in AUSNAHMEN):
            continue
        funde.append((name, wort))
if funde:
    print("")
    print("Umlaut-Waechter - bitte pruefen:")
    for name, wort in funde[:20]:
        print("  %-34s %s" % (name, wort))
else:
    print("Umlaut-Waechter: sauber.")
