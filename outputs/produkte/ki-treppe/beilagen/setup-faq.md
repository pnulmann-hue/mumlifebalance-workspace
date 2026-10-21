---
tags: [produkt]
---

# Wenn beim Einrichten etwas klemmt

Die Fragen, die beim Einrichten am häufigsten kommen — und was ich dazu sage.
Beilage zu Kapitel 4.

Wenn deine Frage nicht dabei ist: **stell sie Claude selbst.** Das ist keine
Ausrede, sondern der wichtigste Handgriff in diesem Kurs. Schreib einfach hinein,
was du siehst — auch die Fehlermeldung im Wortlaut — und frag, was das heisst.

---

## Bevor du anfängst

**Was brauche ich überhaupt?**

Einen Rechner, ein Abo und zwanzig Minuten. Welches Abo und was es kostet, steht
in Lektion 1.4 — ich rechne dort vor, was ich selbst zahle und wofür.

**Was ist der Unterschied zwischen Claude, Cowork und Claude Code?**

Es sind drei Stufen derselben Sache, und du hast sie in den Kapiteln 2, 3 und 4
der Reihe nach kennengelernt:

Im **Chat** schreibst du, sie antwortet. Alles, was sie wissen soll, tippst du
hinein. In **Cowork** arbeitet sie mit deinen Dateien und hängt an deiner
Planung. In **Claude Code** hast du einen eigenen Arbeitsplatz auf deinem
Rechner, der bleibt und wächst — und sie darf dort deine Programme benutzen.

**Ich selbst arbeite nur mit Claude Code.** Die beiden Stufen davor zeige ich
dir trotzdem, und zwar aus zwei Gründen: Du verstehst damit, was ein guter
Auftrag ist, bevor es technisch wird. Und wenn dir eine der beiden reicht, hast
du trotzdem etwas gewonnen — das habe ich in Lektion 3.4 so gemeint, wie ich es
gesagt habe.

**Brauche ich das schwarze Fenster, von dem alle reden?**

Nein. Wir arbeiten die ganze Zeit in der normalen App. Das Terminal gibt es,
aber du brauchst es für nichts, was in diesem Kurs vorkommt.

---

## Einrichten

**Macht es einen Unterschied, wo der Ordner liegt?**

Für die Technik nicht. Für dich schon: Nimm einen Platz, den du wiederfindest,
und leg ihn **nicht** in einen Ordner, der automatisch in die Cloud kopiert wird
— also nicht in OneDrive, iCloud oder Dropbox.

Der Grund dafür kommt in Kapitel 10 ausführlich: In deinem Arbeitsplatz landen
mit der Zeit Dinge, die nirgendwohin kopiert werden sollen. Wenn der ganze
Ordner in der Cloud liegt, hebelt das jede spätere Ausschlussliste aus.

**Muss ich die Ordnerstruktur genau so übernehmen?**

Nein, aber ich empfehle es dir für den Anfang. Die fünf Ordner — `context`,
`outputs`, `reference`, `scripts`, `plans` — haben je eine Aufgabe, und ab
Kapitel 5 gehe ich davon aus, dass sie so heissen. Wenn du später merkst, dass
du etwas anders brauchst, änderst du es.

**Ich habe zwei Geschäfte. Zwei Ordner oder einer?**

Zwei. Und in jeder Gedächtnis-Datei steht dann, worum es in diesem Ordner geht.
Sonst mischt sie dir die beiden Welten, und du merkst es erst am fertigen Text.

**Es kommt eine Meldung, dass Git fehlt.**

Git ist ein kleines Hilfsprogramm, das deine Änderungen mitschreibt. Auf einem
Mac ist es meistens schon da, unter Windows musst du es einmal installieren.
Die Meldung sagt dir in der Regel selbst, woher — und wenn nicht, zeig sie
Claude und frag.

**Brauche ich GitHub?**

Nicht für diesen Kurs. GitHub ist ein Ort im Netz, an dem dein Arbeitsplatz
zusätzlich liegt — praktisch, wenn der Laptop kaputtgeht oder du an zwei
Rechnern arbeitest. Du kannst das jederzeit später einrichten.

🚨 Wenn du es tust: **Ein öffentliches Repository ist wirklich öffentlich.**
Jeder kann hineinschauen. Was dort nicht hingehört, steht in Kapitel 10.

---

## Wenn es klemmt

**Ein Befehl wird nicht erkannt.**

Prüf zuerst, ob du im richtigen Ordner bist — die Befehle aus dem Grundgerüst
gibt es nur dort. Steht oben in der App ein anderer Ordnername, wähl den
richtigen aus.

**Sie findet meinen Business-Brief nicht.**

Dann liegt er nicht dort, wo sie sucht, oder die Gedächtnis-Datei sagt ihr
nicht, dass es ihn gibt. Beides prüfst du am schnellsten, indem du fragst:
*„Welche Dateien liegen in context, und was steht in meiner Gedächtnis-Datei
über meinen Business-Brief?"*

**Das Ergebnis ist Murks.**

Fang ein neues Gespräch an und schreib den Auftrag neu, statt ihn mit
Nachfragen geradezubiegen. Warum das besser ist, steht in Lektion 4.6.

**Mitten in der Arbeit kommt eine Rückfrage, ob sie etwas darf.**

Das ist Absicht. Sie fragt, bevor sie etwas auf deinem Rechner ändert. Lies
nach, was sie vorhat, und sag ja oder nein. Wenn dich dieselbe Frage zum
dritten Mal nervt, erlaubst du sie dauerhaft — dann kommt sie nicht wieder.

---

## Deine Dateien

**Kann ich an zwei Rechnern arbeiten?**

Ja, aber dein Arbeitsplatz liegt auf einem davon. Für den zweiten brauchst du
GitHub oder du kopierst den Ordner. Fang mit einem an.

**Soll ich meine Videos in den Arbeitsplatz legen?**

Nur, wenn du wirklich damit arbeiten willst — Videos sind gross und füllen dir
die Festplatte. Wenn es dir um das gesprochene Wort geht, lass sie
transkribieren und behalte nur den Text. Der ist ein Tausendstel so gross und
durchsuchbar.

**Was passiert mit meinen Daten?**

Dein Arbeitsplatz liegt auf deinem Rechner. Was sie liest, um deine Frage zu
beantworten, geht zur Beantwortung an Anthropic — wie bei jeder Frage im Chat
auch. Was dort nichts zu suchen hat, gehört gar nicht erst in den Arbeitsplatz.
Kapitel 10 geht das in Ruhe durch.

**Kann ich einschränken, worauf sie zugreifen darf?**

Ja. Sie sieht nur den Ordner, den du ausgewählt hast — nicht deinen ganzen
Rechner. Und innerhalb davon kannst du einzelne Ordner ausschliessen. Auch das
steht in Kapitel 10.

---

## Was ich oft gefragt werde

**Muss ich etwas vom Programmieren verstehen?**

Nein. Du schreibst weiter Deutsch, in ganzen Sätzen. Wenn du weisst, was ein
Ordner ist, reicht das — das meine ich genau so, wie es dasteht.

**Ich habe Angst, etwas kaputtzumachen.**

Kannst du, deshalb fängst du mit etwas an, bei dem nichts kaputtgehen kann.
Genau darum ist der erste Helfer in Kapitel 3 ein Haushalts-Bot und kein
Werkzeug für deine Kundinnen.

**Wie lange dauert das alles?**

Das Einrichten zwanzig Minuten. Bis es sich wirklich lohnt, ein paar Wochen —
weil dein Arbeitsplatz erst dann genug über dich weiss. Meine Gedächtnis-Datei
ist über Monate gewachsen, nicht an einem Nachmittag entstanden.

**Ich komme nicht weiter und finde die Antwort nirgends.**

Dann schreib mir. Du hast den Kurs gekauft, nicht ein Video-Paket.

---

## Die wichtigste Gewohnheit

Wenn du eine Fehlermeldung siehst, lies sie nicht nur — **zeig sie ihr.**
Kopier den Wortlaut hinein und frag, was er bedeutet und was du tun sollst.

Das klingt zu einfach, um die Antwort auf alles zu sein. Ist es aber bei den
meisten Fragen, die hier oben stehen.

---

## 🔗 Verwandte Notizen

- [[03-inhaltsverzeichnis]]
- [[claude-md-vorlage]]
- [[checkliste-modul-4]]
