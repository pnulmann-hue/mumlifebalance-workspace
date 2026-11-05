---
tags: [produkt]
---

# Dein erster Bot — der Auftrag und die vier Schritte

<!-- Ausgeliefert wird die Google-Doc-Fassung im Drive-Kursordner (Kennung in context/Kurse/aktuelle kurse/Easy-KI/beilagen-drive.json). Diese Datei ist die Inhalts-Quelle — eine Aenderung hier aendert nichts an dem, was die Teilnehmerin oeffnet. Doc nachziehen. -->

<!-- 🚨 Beilage zu Lektion 6.3, seit 04.11.2026. Bewusst KEIN Code und keine
     Vorlage zum Herunterladen: Lektion 4.2 verspricht „Du installierst nichts
     weiter", und eine startbare Vorlage braucht eine Laufzeit, die im Kurs
     niemand einrichtet. Hier steht nur, was man nach dem Video nochmal
     nachlesen will. -->

**Als Erstes: Datei → Kopie erstellen.** Dann ist dieses Dokument deines und du
kannst hineinschreiben.

---

Du baust diesen Bot nicht, du beschreibst ihn. Genau **eine** Sache machst du
selbst — den Schlüssel holen. Alles andere ist ein Gespräch.

Rechne mit zwanzig Minuten beim ersten Mal.

---

## Der Auftrag

Das tippst du in den Chat. Schreib ihn ab, statt ihn einzufügen — dann merkst du,
dass da kein Zauberwort steht.

> Ich möchte einen Bot, der mir jeden Morgen um sieben auf Telegram schreibt.
>
> Er soll mir ________________________________________________
>
> Ich habe einen Schlüssel vom Botvater. Erklär mir jeden Schritt, und frag
> nach, wenn dir etwas fehlt.

**Der letzte Halbsatz ist der wichtigste.** Ohne ihn baut sie drauflos und rät,
was du gemeint hast. Mit ihm fragt sie — und du musst nichts vorbereiten.

In die Lücke kommt, was du morgens lesen willst. Ein paar Ideen, falls dir gerade
nichts einfällt:

| Wenn du das willst | schreib hinein |
|---|---|
| ein ruhiger Start | die drei Dinge, die heute anstehen |
| Überblick | was gestern auf Instagram passiert ist |
| weniger Postfach | wer mir heute geschrieben hat, nur Absender und Betreff |
| ein Schubs | eine Frage, über die ich beim Kaffee nachdenken kann |

Fang mit etwas Privatem an. Dort merkst du sofort, ob es taugt, und es ist nichts
kaputt, wenn es danebengeht.

---

## Die vier Schritte

### 1 · Den Botvater fragen

Das ist der Teil, den dir niemand abnimmt: Telegram gibt den Schlüssel nur dir.

Öffne Telegram und such nach **@BotFather**. Schreib ihm `/newbot`.

Er antwortet auf Englisch — das ist die einzige Stelle im ganzen Kurs, an der das
so ist. Vier Zeilen musst du erkennen:

| Was er schreibt | Was er meint |
|---|---|
| *Choose a name for your bot* | Der Name, den du nachher im Chat siehst. Zum Beispiel **Mein Morgenbote**. Leerzeichen und Umlaute sind erlaubt |
| *Choose a username… must end in bot* | Die Adresse. Zum Beispiel **morgenbote_sandra_bot**. Gibt es sie schon, sagt er es und du nimmst eine andere |
| *Use this token to access the HTTP API* | Darunter steht dein Schlüssel |
| *Done! Congratulations* | Fertig, das war Schritt 1 |

Der Schlüssel ist eine lange Zeichenkette mit einem Doppelpunkt in der Mitte.
Lass das Fenster offen, du brauchst ihn gleich.

### 2 · Sagen, was du willst

Jetzt den Auftrag von oben in den Chat, mit deiner Lücke ausgefüllt.

### 3 · Antworten

Ab hier führt sie dich. Sie fragt ungefähr das:

| Sie fragt | Du antwortest |
|---|---|
| Wo ist dein Schlüssel? | Du gibst ihn ihr. Sie legt ihn an die richtige Stelle |
| Wem soll er schreiben? | Du schreibst deinem neuen Bot einmal *Hallo*, sie holt sich den Rest |
| Was soll in der Nachricht stehen? | In ganzen Sätzen, so wie du es einer Freundin erzählen würdest |
| Soll ich ihn einmal starten? | Ja |

Der Wortlaut ist bei dir anders als hier. Die vier Fragen sind dieselben.

### 4 · Aufs Handy schauen

Wenn die Nachricht ankommt, läuft er. **Das ist der Moment, an dem du fertig
bist** — alles danach ist Komfort.

---

## Der eine Satz, den du dir merkst

Beim Einrichten entsteht ein **Zugangsschlüssel**. Der gehört in die Datei, die
sie dafür anlegt.

Nie in ein Dokument.

Nie in eine Nachricht.

Nie in den Text deines Bots.

Sie macht das von selbst richtig. Du musst es nur einmal gesehen haben, damit du
es wiedererkennst. Warum es zählt, steht in Modul 10.

---

## Wenn keine Nachricht kommt

Das passiert, und es ist normal. Drei Stellen, in dieser Reihenfolge:

| Was los sein kann | Was du sagst |
|---|---|
| Er ist gar nicht losgegangen | *Läuft der Zeitplan überhaupt? Schau bitte nach* |
| Der Schlüssel stimmt nicht mehr | *Prüf bitte den Zugang, ich glaube der Schlüssel ist abgelaufen* |
| Er ist unterwegs gestolpert | *Schau bitte ins Protokoll und sag mir, woran es lag* |

Und wenn du im Protokoll nichts verstehst: kopier es hinein und frag, was es
bedeutet. Das ist kein Notbehelf, das ist der normale Weg.

---

## Dass er von selbst losgeht

Bis hierher startest du ihn noch selbst. Wie der Wecker dazukommt, steht in
Lektion **6.4** — und dort auch, was es kostet: auf deinem Rechner nichts, im
Netz rund fünf im Monat.

**Stell die erste Ausgabe absichtlich auf eine Uhrzeit, zu der du wach bist.**
Dann siehst du am selben Tag, ob es klappt, statt bis morgen früh zu warten.
