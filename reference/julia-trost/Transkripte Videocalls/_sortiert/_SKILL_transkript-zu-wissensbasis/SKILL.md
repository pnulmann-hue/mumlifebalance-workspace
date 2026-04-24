---
name: transkript-zu-wissensbasis
description: Wandelt rohe Video-Transkripte (von Kursen, Mentorings, Tutorials) in eine saubere, strukturierte Wissensbasis für Bots um. Nutze diesen Skill immer, wenn .txt-Transkripte aufgeräumt, in Markdown überführt, mit Metadaten versehen oder als Bot-Wissensgrundlage vorbereitet werden sollen. Triggert auch bei Formulierungen wie "aus meinen Transkripten eine Wissensbasis bauen", "Transkripte für meinen Custom GPT vorbereiten", "Videoinhalte für Bot-Training aufbereiten" oder wenn Patricia Julias Kursordner verarbeiten möchte. Der Stil der Sprecherin bleibt erhalten – es wird nicht neu geschrieben, sondern aufgeräumt.
---

# Transkript zu Wissensbasis

Dieser Skill verarbeitet rohe .txt-Transkripte (typischerweise aus automatischer Video-Transkription) und erzeugt pro Eingabedatei zwei Ausgaben:

1. Eine aufgeräumte Markdown-Datei, die als Bot-Wissensgrundlage hochgeladen werden kann.
2. Eine JSON-Datei mit Metadaten – Thema, Strategien, Tools, Handlungsanweisungen – für spätere Filterung und Indexierung.

## Kontext: Patricia, Julia und zwei Quellen

Patricia ist Mentorin für Mamas im Network Marketing, die sich ein echtes Online-Business aufbauen wollen. Ihr Ansatz ist eine Hybridstrategie: Network Marketing kann Teil sein, aber parallel wird eine eigene Personal Brand aufgebaut.

Patricia hat ihr Business-Know-how bei **Julia Trost** gelernt. Deshalb gibt es zwei unterschiedliche Quellen von Transkripten, die dieser Skill verarbeitet – und er muss sie klar auseinanderhalten:

**Quelle 1: Julia Trost (das Lern-Fundament)**
Die Ordner unter `_sortiert/` (100k Blueprint, ARIA, Launch Queen, OBA, Reels to Cash etc.) stammen aus Julias Kursen und Mentorings. Das ist Patricias Wissens-Basis. Hier bleibt Julias Stimme unverändert – wir räumen nur sprachlich auf. Inhaltlich geht es um Online-Business, Launch-Strategien, Content, Instagram, Sales, KI-Tools (ChatGPT, ARIA, ManyChat), digitale Produkte.

**Quelle 2: Patricia (die Anwendung im eigenen Kontext)**
Kommt in Phase 2 dazu, wenn Patricia ihre eigenen Kurse transkribiert. Hier wird deutlich, wie Patricia Julias Learnings in den Kontext "Mamas im Network Marketing" übersetzt. Das ist Patricias USP – nicht die Strategien allein, sondern die Übersetzung. Patricias Stil (siehe "Patricias Stil" unten) muss hier besonders sorgfältig erhalten bleiben, weil die Bots später genau so klingen sollen wie sie.

**Warum die Unterscheidung wichtig ist:** Im fertigen Wissensspeicher muss für jeden Baustein erkennbar sein, ob er von Julia oder von Patricia kommt. Das verhindert Zitier-Fehler (Patricia will Julias Konzepte nicht als ihre eigenen ausgeben), macht Lernpfade nachvollziehbar und erlaubt es später, Bots zu bauen, die entweder nur Patricias Stimme nutzen oder das volle Wissen mit sauberer Attribution.

## Patricias Stil (relevant für Quelle 2)

Wenn Patricia-Transkripte verarbeitet werden, gelten diese Stil-Merkmale, die erhalten bleiben müssen:
- Du-Form, längere fließende Sätze statt Drei-Wort-Stakkato
- Direkt und klar, auch mal konfrontativ – aber immer mit motivierendem Unterton
- Humor, Ironie, kleine Seitenhiebe; manchmal sarkastisch
- Keine typischen KI-Muster: keine Bullet-Ketten mit Emoji-Präfixen, kaum Überschriften-Inflation, sparsam mit Emojis (nur einfache Smilies, selten)
- Haltung: Selbstverantwortung, Handlung, Umsetzung. Patricia verachtet wolkige Ratgeber-Phrasen – wenn das Original etwas direkt sagt, darf die Wissensbasis das nicht weichspülen.

Julias Stil unterscheidet sich davon in Details, ist aber in der Tonalität ähnlich (locker, direkt, humorvoll, du-Form). Bei Julia-Material die konkrete Tonalität des Transkripts spiegeln; nicht versuchen, Julia wie Patricia klingen zu lassen oder umgekehrt.

## Der Kernkonflikt, den dieser Skill löst

Rohe Auto-Transkripte sind für Bots schlecht geeignet: sie strotzen vor Füllwörtern, abgebrochenen Sätzen, Versprechern, doppelten Gedanken und "hier siehst du"-Verweisen auf Bildschirme, die der Bot nicht sehen kann. Gleichzeitig enthalten sie echtes Gold: Strategien, Frameworks, konkrete Beispiele, die Denkweise der Sprecherin.

Der Skill muss also beides gleichzeitig können: aufräumen, ohne zu glätten. Das Ergebnis soll sich lesen, als hätte jemand die gesprochenen Worte mitgeschrieben und sauber getippt – nicht als hätte eine KI den Text neu verfasst.

## Workflow

### Schritt 1: Input verstehen

Prüfe zuerst, was genau verarbeitet werden soll:

- Ein einzelnes Transkript? → Verarbeite diese eine Datei.
- Ein einzelner Kursordner (z.B. "ARIA")? → Alle .txt-Dateien in diesem Ordner.
- Mehrere Ordner oder der gesamte `_sortiert`-Baum? → Bestätige kurz mit der Userin, bevor du stundenlang Material durchrechnest.

Wenn unklar, frage nach. Bei vielen Dateien: schlage vor, mit einer oder zwei Beispieldateien anzufangen, damit die Userin das Ergebnis reviewen kann, bevor der ganze Batch läuft.

### Schritt 2: Quelle bestimmen

Ermittle für jede Datei, ob sie von Julia Trost oder von Patricia stammt. Regeln:

- Liegt die Datei unter `_sortiert/` (also im Julia-Trost-Ökosystem)? → `source_speaker: "Julia Trost"`.
- Stammt die Datei aus einem Ordner, den Patricia explizit als ihre eigenen Inhalte markiert hat (z.B. `Patricia_Kurse/`, `_meine_transkripte/` oder mit einer Datei wie `SOURCE.txt` im Ordner, die das deklariert)? → `source_speaker: "Patricia"`.
- Unklar? Frag nach, bevor du verarbeitest. Falsche Attribution ist hier wirklich teuer.

### Schritt 3: Jede Datei klassifizieren

Bevor du aufräumst, erkenne den Typ des Transkripts – das bestimmt die Gliederung:

- **Strategie-Vortrag**: Die Sprecherin erklärt ein Konzept oder eine Methode (z.B. "Fast Cash Teil 1"). → Gliederung nach den Kernpunkten der Strategie.
- **Tech-Tutorial / Screen-Recording**: Die Sprecherin zeigt Schritt für Schritt etwas am Bildschirm (z.B. "ARIA Content", "KI ChatGPT Grundlagen"). → Gliederung nach Arbeitsschritten, Prompts und Einstellungen möglichst wörtlich erhalten.
- **Welcome / Onboarding**: Einführungstexte, die eher Überblick geben. → Als Kurzübersicht strukturieren.
- **Q&A / Live-Call**: Fragen-Antwort-Format. → Nach Fragen gliedern.

Nimm den offensichtlichsten Typ. In Zweifelsfällen: Strategie-Vortrag ist der sichere Default.

### Schritt 4: Aufräumen – was raus darf und was bleiben muss

**Raus:**

- Füllwörter und Geräuschwörter: "ja", "so", "okay" als Satzanfang, "halt", "irgendwie" (wenn überflüssig), "weißt du", "ne?", dreifache "liebe, liebe, liebe"
- Rein oral-verbindende Wendungen ohne Inhalt: "und das ist eben auch", "und eben auch"
- Doppelte Gedanken direkt hintereinander (wenn die Sprecherin denselben Satz leicht anders nochmal sagt – nimm die klarere Variante)
- Offensichtliche Transkriptionsfehler (z.B. "area" statt "ARIA", "Culture Actions" statt "Call to Actions", "Hochsätze" statt "Hooks", "Causale" statt "Carousel")
- Verweise auf Unsichtbares ohne Information ("hier siehst du das", "klick dich einfach mal durch") – nur wenn sie rein visuell sind. Wenn sie Handlung beschreiben ("klick auf den Button X"), bleiben sie drin.

**Bleibt:**

- Die Art zu sprechen der jeweiligen Sprecherin: Du-Form, längere Sätze, direkte Ansprache
- Humor, Ironie, kleine Seitenhiebe
- Konkrete Zahlen, Preise, Produktnamen, Timings
- Beispiele mit echten Details
- Motivations-Passagen – nicht rauskürzen, nur entschlacken
- Konkrete Handlungsanweisungen und Prompts (die sind gerade bei Tech-Tutorials das Wertvollste)

**Goldene Regel:** Wenn du zwischen "drin lassen" und "rausnehmen" zögerst, lass es drin. Lieber 10% zu viel als den Stil kaputt machen. Es ist kein Essay, den du lektorierst – es ist gesprochene Expertise, die lesbar werden soll.

### Schritt 5: Markdown-Struktur erzeugen

Nutze dieses Template als Grundgerüst:

```markdown
# [Titel, abgeleitet aus Dateiname + Inhalt]

**Quelle:** [Julia Trost | Patricia]
**Kurs/Ordner:** [Ordnername]
**Typ:** [Strategie-Vortrag | Tech-Tutorial | Welcome | Q&A]
**Kernthema:** [In einem Satz]

## Zusammenfassung

[3-5 Sätze, was in diesem Transkript vermittelt wird. Im Stil der Sprecherin – nicht neutral-distanziert.]

## Inhalt

### [Abschnittsüberschrift 1]

[Aufgeräumter Fließtext]

### [Abschnittsüberschrift 2]

[...]

## Zentrale Take-aways

- [3-7 Kernaussagen in knappen Sätzen – im Stil der Sprecherin, nicht als generische Bullets]

## Konkrete Handlungsanweisungen

[Falls im Transkript Schritt-für-Schritt-Anleitungen vorkommen, hier als nummerierte Liste. Sonst weglassen.]

## Genannte Strategien & Frameworks

[Falls benannte Strategien vorkommen (z.B. "Fast Cash Fusion Strategie") – hier kurz mit Definition. Sonst weglassen.]

## Erwähnte Tools

[Liste der genannten Tools mit einem Satz Kontext. Sonst weglassen.]
```

Überschriften sollen den Inhalt beschreiben, nicht generisch sein. Also nicht "Teil 1", "Teil 2", sondern "Die erste Fast-Cash-Strategie: 1:1-Angebote umtransformieren".

### Schritt 6: JSON-Metadaten erzeugen

Nebenbei pro Datei ein JSON mit diesem Schema:

```json
{
  "title": "string",
  "source_file": "Originaldateiname.txt",
  "source_speaker": "Julia Trost | Patricia",
  "course": "Ordnername",
  "type": "strategie | tutorial | welcome | qa",
  "core_topic": "string",
  "summary": "string (3-5 Sätze)",
  "key_takeaways": ["string", ...],
  "strategies_frameworks": [
    {"name": "string", "description": "string"}
  ],
  "tools": [
    {"name": "string", "context": "string"}
  ],
  "action_steps": ["string", ...],
  "related_topics": ["string", ...],
  "patricia_anwendungsnotiz": "string (nur bei Patricia-Quelle: wie übersetzt Patricia Julias Frameworks hier in den Network-Marketing-Mamas-Kontext? Wenn sich das aus dem Transkript ablesen lässt.)",
  "word_count_original": 0,
  "word_count_cleaned": 0
}
```

Felder ohne Inhalt als leere Arrays/Strings lassen, nicht weglassen – das macht die spätere Weiterverarbeitung einfacher.

### Schritt 7: Ausgabestruktur

Lege die Ergebnisse spiegelbildlich zur Eingabestruktur ab:

```
_wissensbasis/
├── 100k Blueprint/
│   ├── Fast Cash Teil 1.md
│   ├── Fast Cash Teil 1.json
│   ├── Fast Cash Teil 2.md
│   └── ...
├── ARIA/
│   ├── ARIA Content.md
│   ├── ARIA Content.json
│   └── ...
└── _index.json   (wird am Ende gebaut – Gesamtübersicht aller Einträge)
```

Der `_index.json` ist die Gesamt-Inhaltsübersicht: Titel, Kurs, Thema, Schlagworte, Quelle pro Eintrag. Damit kann Patricia später entscheiden, welche Inhalte in welchen Bot gehören.

### Schritt 8: Kontrollausgabe

Am Ende der Verarbeitung zeig Patricia kurz:

- Wie viele Dateien verarbeitet wurden
- Wo die Ergebnisse liegen (als klickbarer computer://-Link)
- Eine stichprobenartige Vorschau: öffne eine der Markdown-Dateien und zeige die ersten ~20 Zeilen, damit sie sofort sieht, ob der Stil passt

## Qualitätsprüfungen vor Abschluss

Geh diese Checkliste mental durch, bevor du "fertig" sagst:

- Liest sich das Markdown, als hätte die Sprecherin es selbst aufgeschrieben? Oder klingt es wie ein ChatGPT-Text mit Bulletpoints und Power-Adjektiven? Letzteres ist ein Fehler.
- Sind konkrete Zahlen, Preise und Produktnamen erhalten?
- Bei Tech-Tutorials: Sind die Prompts und Schritte wörtlich übernommen, oder wurden sie zu allgemeinen Beschreibungen verwässert? Prompts müssen wörtlich erhalten bleiben.
- Ist das JSON valide und enthält es die wichtigsten Metadaten?

## Was dieser Skill nicht tut

- Er fügt keine Inhalte hinzu, die nicht im Transkript stehen. Wenn etwas unklar ist, bleibt es unklar – wir erfinden nichts dazu.
- Er macht keine stilistische Neubearbeitung im Sinne von "schöner machen". Der authentische Stil ist das Feature, nicht der Bug.
- Er aggregiert nicht automatisch themenverwandte Inhalte aus verschiedenen Dateien. Das ist ein separater Schritt, der später kommt, wenn Patricia das will.

## Hinweis für den Umgang mit Patricia

Patricia mag klare Ansagen und wenig Drumherum. Wenn du während der Verarbeitung auf Entscheidungen stößt (z.B. "dieses Transkript ist halb auf Deutsch, halb English – wie soll ich das behandeln?"), dann frag direkt und mit konkretem Vorschlag, nicht in offener Form. Sie entscheidet schnell, wenn die Optionen klar sind.
