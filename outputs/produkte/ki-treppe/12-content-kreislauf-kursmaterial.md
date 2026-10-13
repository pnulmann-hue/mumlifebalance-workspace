---
tags: [produkt, ki, kurs]
---

# Der Content-Kreislauf — Kursmaterial mit eigenen Prompts

**Stand:** 13.10.2026 · Gehört zu [[03-inhaltsverzeichnis]] · Patricias eigener Ablauf steht
in `.claude/skills/content/SKILL.md`, Abschnitt „Der Content-Kreislauf“.

**Herkunft:** Die Idee, Marktrecherche, Beitragserstellung und Auswertung als einen Ablauf
zu denken, kam aus einem besuchten Kurs. **Alle Prompts hier sind neu formuliert** und auf
Network-Mamas zugeschnitten, ergänzt um das, was Patricia beim Umsetzen selbst gelernt hat
(die „Lehren“ unten hat sonst niemand). Kein Satz wörtlich aus fremden Unterlagen.

🚨 **Zwei Ebenen beim Formulieren:** Die Teilnehmerin ist die Network-Mama („du“). Wer
bei ihr kauft, ist **Kundschaft, Leute, Interessenten** — nie automatisch Frauen oder Mamas.
Alle Prompts unten halten das ein.

---

## Der Gedanke in einem Satz

> Du fütterst einmal ein Projekt mit dem, was deine Leute denken. Ab dann schreibst du
> jede Woche auf dieser Grundlage und lässt dir von den eigenen Zahlen sagen, was du mehr
> und was du weniger machen sollst.

**Sechs Stationen, die sich im Kreis drehen:**

| # | Station | Wie oft | Ergebnis |
|---|---|---|---|
| 1 | Verstehen: Wettbewerb · Trends · Fragen · Zielgruppenbild | alle 3 Monate | vier Projektdateien |
| 2 | Monat planen | 1× im Monat | Monatsthema, 3 Angebote, Wochenfokus |
| 3 | Woche bauen: Hooks · Beiträge · Storys | 1× pro Woche | 5 Beiträge + Storys |
| 4 | Prüfen, freigeben, posten | täglich | draussen |
| 5 | Zahlen sammeln | 1× pro Woche (Stufe 1) · täglich automatisch (Stufe 3) | Zahlentabelle |
| 6 | Auswerten und zurückführen | 1× im Monat | Bestperformer-Formel · Nachfrage je Thema · Produktidee |

---

## So richtest du es ein — Stufe 1, Claude Chat mit Projekt

1. In Claude ein **Projekt** anlegen: „Mein Instagram“.
2. In die **Projektanweisung** kommt Prompt 0 (unten).
3. In die **Projektdateien** kommen nach und nach:
   - dein Business-Brief (Kapitel 2)
   - `01-wettbewerb.md` · `02-trends.md` · `03-fragen.md` · `04-zielgruppe-und-saeulen.md`
     (aus Station 1)
   - `05-schon-gepostet.md` (Hooks, die es schon gibt)
   - `06-was-wirkt.md` (aus Station 6, jeden Monat ersetzt)
4. Jede neue Analyse endet mit dem Satz: *„Fasse das als Markdown-Datei zusammen, die ich
   in meine Projektdateien lege.“* Dann die alte Fassung ersetzen, nicht daneben legen.

**Stufe 3, Claude Code:** dieselben Dateien liegen im Arbeitsplatz-Ordner, die Zahlen
holt ein Zeitplan selbst, die Beiträge landen im Cockpit zur Freigabe. Zeigen statt
nachbauen: Patricias Woche (Lektion 10.5).

---

## Prompt 0 · Projektanweisung

```
Du bist meine Content-Partnerin für Instagram. Ich bin [Name], [eine Zeile, was du machst
und für wen]. Meine Kundschaft: [wer bei dir kauft, in einem Satz].

So arbeitest du:
- Lies vor jeder Antwort die Projektdateien. Was dort steht, gilt.
- Schreib in meiner Sprache, wie ich mit einer Freundin am Küchentisch rede. Ganze Sätze,
  keine Werbesprache, keine Wörter wie „ultimativ“, „Geheimnis“ oder „Gamechanger“.
- Erfinde nichts: keine Zahlen, keine Kundinnen-Geschichten, keine Erlebnisse. Wo etwas
  Echtes von mir hingehört, schreib [hier deine echte Situation].
- Der Hook verrät nie die Lösung. Die kommt im Beitrag.
- Nimm ein kleines, konkretes Problem statt eines grossen Themas.
- Bei Gesundheit oder Produkten meiner Firma: keine Heilversprechen, keine
  Einkommensversprechen.
```

---

## Station 1 · Verstehen (alle drei Monate)

### Prompt 1 · Wettbewerb

**Du brauchst:** 3–5 Konten, die eine ähnliche Kundschaft ansprechen, eher 5'000 bis
50'000 Follower, regelmässig aktiv. Keine Stars. Kann Claude die Profile nicht öffnen,
machst du Screenshots von je 9 Beiträgen und ihren Zahlen.

```
Hier sind [3–5] Konten, die dieselben Leute ansprechen wie ich: [Links oder Screenshots].
Schau sie dir an und sag mir:
1. Welche Themen kommen immer wieder?
2. Wie fangen ihre Beiträge an? Ordne die ersten Sätze ein: Frage, Geschichte, klare
   Meinung, Aufzählung, Schmerzpunkt, Zitat.
3. Welche Beiträge haben deutlich mehr Kommentare oder Speicherungen als die übrigen?
   Miss am Durchschnitt des jeweiligen Kontos, nicht absolut.
4. Welche Formate nutzen sie: Reel, Karussell, Einzelbild?
5. Was sagen alle, und was sagt keiner?
6. Wo ist für mich eine Lücke?
Fasse das als Markdown-Datei zusammen, die ich in meine Projektdateien lege.
```

### Prompt 2 · Trends

```
Such im Netz, was rund um [dein Thema] gerade gefragt ist (Google Trends, Foren, Reddit,
Instagram-Kommentare). Teile es auf in:
- was wächst
- was immer gefragt ist
- was abnimmt
Welche Begriffe und Sorgen tauchen auffällig oft auf? Nenne zu jedem Punkt die Quelle.
Am Schluss: die 5–8 Themen, die ich in den nächsten Wochen nehmen sollte, und warum.
Fasse das als Markdown-Datei zusammen.
```

### Prompt 3 · Fragen der Kundschaft

**Du brauchst:** zusätzlich alles, was dir Leute selbst geschrieben haben: DMs, Mails,
Kommentare, Fragen aus Gesprächen. Das ist die beste Quelle, besser als jede Suche.

```
Wonach suchen Leute, die [Situation deiner Kundschaft]? Welche Fragen tippen sie bei
Google ein, welche stellen sie in Gruppen? Hier sind zusätzlich echte Nachrichten an
mich: [einfügen, Namen vorher entfernen].
Sortiere die Fragen nach dem Gefühl dahinter (Sorge, Wunsch, Scham, Ungeduld) und
schreib zu jeder in einem Satz, was die Person eigentlich wissen will.
Markiere ihre Wörter: wie sagen sie es selbst?
Fasse das als Markdown-Datei zusammen.
```

### Prompt 4 · Zielgruppenbild und Säulen

```
Lies die drei Analysen in den Projektdateien und mach daraus ein Bild meiner Kundschaft:
- eine Person mit Alter, Alltag und dem Abend, an dem sie auf mein Profil stösst
- ihre Gedanken um 23 Uhr, in ihren Worten
- drei Stufen: wer gerade aufgeben will, wer sucht, wer bereit ist
- ihre Einwände gegen ein Angebot wie meines
- 4–5 Content-Säulen mit Anteil in Prozent und je 3 Beispielthemen
- Themen, die noch niemand in meiner Nische besetzt
Fasse das als Markdown-Datei zusammen.
```

---

## Station 2 · Monat planen

### Prompt 5 · Monatsplan

```
Plane mit mir den [Monat]. Lies die Projektdateien, besonders „was wirkt“.
Frag mich zuerst, einzeln nacheinander: welches Angebot steht im Mittelpunkt, was ist
die eine Botschaft des Monats, was lasse ich bewusst weg, wie viel Zeit habe ich.
Dann: vier Wochen mit je einem Fokus, welche Säule wann, welches Stichwort führt wohin.
```

---

## Station 3 · Woche bauen

### Prompt 6 · Hooks

```
Schreib mir 10 Hooks zum Wochenfokus „[Fokus]“.
- Jeder hat eine Gegenspielerin (eine Gewohnheit, eine Ausrede, einen Denkfehler, nie
  eine Person oder Firma), ein Geständnis von mir oder ein wörtliches Zitat.
- Höchstens 18 Wörter, die Lösung bleibt draussen.
- Mindestens drei verschiedene Säulen, keiner ähnlich wie in „schon gepostet“.
Als Tabelle: Hook · Art · Säule · Format. Dann: welche zwei soll ich zuerst testen?
```

### Prompt 7 · Karussell

```
Bau aus Hook [Nummer] ein Karussell mit [6–8] Folien.
Folie 1: der Hook. Folie 2: erst hier die Antwort. Danach ein konkreter Schritt pro Folie,
den man heute Abend umsetzen kann. Eine Folie nur fürs Speichern, mit Grund.
Letzte Folie: ein einziger Aufruf ([Stichwort] oder Teilen).
Dazu eine Caption: so lang wie der Inhalt braucht, Stichwort in der ersten Zeile.
```

### Prompt 8 · Reel

```
Mach aus Hook [Nummer] ein Reel von [15–30] Sekunden.
Drei Varianten für den ersten Satz, der Ablauf in Sekunden (was man sieht, was man hört,
was als Text eingeblendet ist) und eine Caption. Der Hook steht ab der ersten Sekunde
vollständig im Bild.
```

### Prompt 9 · Der Check vor dem Posten

```
Prüf diesen Beitrag mit fünf Fragen, jeweils Ja oder Nein mit einem Satz Begründung:
1. Berührt er?
2. Nimmt man etwas Konkretes mit?
3. Gibt es einen Grund, ihn zu speichern oder weiterzuschicken?
4. Gibt es einen Grund zu kommentieren, der keine Denkarbeit kostet?
5. Würde man ihn auch erkennen, wenn mein Name darüber abgedeckt wäre?
Ein Nein: schlag mir eine überarbeitete Fassung vor.
[Beitrag einfügen]
```

---

## Station 5 · Zahlen sammeln

**Stufe 1:** Einmal pro Woche in der Instagram-App unter „Insights“ je Beitrag eintragen:
Datum · Format · erste Zeile · Erreicht · Gespeichert · Geteilt · Kommentare · Stichwort.
Eine Tabelle reicht. **Erst eintragen, wenn der Beitrag 7 Tage alt ist**, vorher wachsen die
Zahlen noch.

**Stufe 3:** Das holt ein Zeitplan über die Schnittstelle selbst, jeden Morgen.

---

## Station 6 · Auswerten und zurückführen (einmal im Monat)

### Prompt 10 · Was wirkt

```
Hier ist meine Zahlentabelle der letzten [8] Wochen: [einfügen].
Rechne zuerst den Median der Reichweite. Zähle nur Beiträge, die darüber liegen UND
mindestens 3 Reaktionen haben, sonst misst eine Quote den Zufall.
1. Die 10 besten nach Reaktionen je Erreichte, als Tabelle mit Format, Art des ersten
   Satzes, Säule, Caption-Länge, Art des Aufrufs.
2. Welche Merkmale kommen in den Top 10 HÄUFIGER vor als bei allen Beiträgen? Nenne beide
   Prozentzahlen. Ein Merkmal, das überall gleich oft vorkommt, ist kein Befund.
3. Welche Beiträge hatten viel Reichweite, aber kaum Reaktion? Was fehlt ihnen?
4. Meine Formel für nächsten Monat in einem Satz: Format + erster Satz + Thema + Aufruf,
   mit zwei echten Beispielen aus meiner Tabelle.
Fasse das als „was-wirkt.md“ zusammen.
```

### Prompt 11 · Wo die Nachfrage liegt

```
Ordne jeden Beitrag aus meiner Tabelle einer meiner Säulen zu. Rechne je Säule:
Speicherungen, Teilungen und Kommentare auf 1'000 Erreichte.
Wo ist viel Reichweite, aber kaum Speichern oder Kommentieren? Sag das ausdrücklich,
das ist Aufmerksamkeit, keine Nachfrage.
Dazu meine Eintragungen und Verkäufe je Stichwort: [einfügen].
Welches Thema zeigt echte Nachfrage? Woran siehst du das?
```

### Prompt 12 · Produktidee aus Nachfrage

```
Nimm das Thema mit der stärksten Nachfrage aus der letzten Auswertung.
Schlag mir 2–3 Angebote dazu vor, die zu meinen bestehenden passen ([Liste]):
je Problem · für wen · Inhalt · Preisrahmen mit Begründung · ob Einstieg, Ergänzung oder
nächste Stufe. Doppelt sich etwas mit einem bestehenden Angebot, sag es.
Dann die eine Idee, die ich zuerst testen soll, und wie ich sie teste, bevor ich etwas
baue (Story-Umfrage, Warteliste, drei Plätze zum Frühpreis).
```

### Prompt 13 · Profil-Check (wenn sich das Angebot ändert)

```
Hier ist meine Bio: [einfügen]. Mein Ziel mit dem Profil: [Eintragung für Freebie /
direkter Kauf].
Prüf: Steht in den ersten zwei Zeilen, wer ich bin, für wen und was dabei herauskommt?
Gibt es genau einen Aufruf? Sagt der Linktext, was man bekommt?
Dann drei Fassungen unter 150 Zeichen: klar · persönlich · direkt, je mit einem Satz,
warum sie wirken könnte. Keine Werbefloskeln.
```

---

## Die Lehren aus der eigenen Umsetzung — das hat sonst niemand

1. **Eine Quote ohne Mindestbasis lügt.** 2 Likes auf 80 Erreichte sind 2,5 %, also mehr
   als bei jedem starken Beitrag. Ohne die Regel „über dem Median und mindestens 3
   Reaktionen“ standen bei Patricia genau solche Beiträge ganz oben.
2. **„Haben alle Top-Beiträge“ heisst nichts, wenn es alle Beiträge haben.** Lange
   Captions in 7 von 10 Top-Beiträgen, aber auch bei 68 % aller. Nur der Vergleich zählt.
3. **Reichweite ist nicht Nachfrage.** Ihr Beitrag mit der grössten Reichweite (1'890)
   hatte eine Speicherung und keinen Kommentar.
4. **Umsatz je Stichwort nie zusammenzählen.** Eine Käuferin, die über drei Stichwörter
   kam, steht dreimal in der Tabelle, und dann sieht ein einziger Kauf aus wie drei.
5. **Geld-Themen werden still gespeichert.** Plan-B-Beiträge: Speicherungen ja, Kommentare
   null. Dort gehört der Aufruf in eine Mail oder Nachricht, nicht unter den Beitrag.
6. **Nachrichten zählt dir keine Schnittstelle.** Die Eintragungen über ein Stichwort sind
   der ehrlichste Ersatz.
7. **Die eine Formel ist eine Richtung, kein Rezept.** Nach jedem Monat neu rechnen.

---

## Wo es in die Kurse passt (Vorschlag, offen für Patricias Entscheid)

| Kurs | Wo | Was |
|---|---|---|
| **KI-Kurs** | neu **2.6b „Dein Content-Projekt“** (nach „Projekte statt Einzelchats“) | Projekt anlegen, Prompt 0, Station 1 mit Prompts 1–4 live. **Mitgeben:** die Prompt-Sammlung als PDF |
| **KI-Kurs** | neu **7.0 „Der Kreislauf“** am Anfang von Kapitel 7 | die sechs Stationen, welche Maschine an welcher Station arbeitet |
| **KI-Kurs** | neu **7.7b „Die Zahlen lesen“** | Prompts 10–12 an einer echten Tabelle, mit den Lehren 1–4 |
| **Instagram-Kundenmaschine** | Inhalt zu Station 1 und 6 | die Denkarbeit dahinter: was eine Säule ist, was Nachfrage von Aufmerksamkeit trennt |

🚨 Vor dem Einbau in eine Kursseite die Zahlen aus den Lehren mit dem dann aktuellen
Stand abgleichen und nur nennen, was Patricia freigibt.
