# Schritt 3 — das Inhaltsverzeichnis

Du hast eben das Fundament gelesen. Halte dich daran, besonders an **den roten Faden**,
**Wie ein Minikurs aufgebaut ist** und die **Sprachregeln**.

Sie hat sich für **eine** der drei Ideen entschieden. Jetzt baust du das
Inhaltsverzeichnis für ihren Minikurs.

---

## Bau die Struktur rückwärts

Bevor du eine Zeile schreibst:

1. Schreib dir das **Endergebnis** hin — was hält sie am Schluss in den Händen?
2. Geh **rückwärts**: welcher Schritt muss davor kommen, und davor, und davor?
3. Prüf die **Lücken**: hält der Sprung von jedem Schritt zum nächsten?
4. Setz den **Anfang**: wo steht sie heute?

Erst dann schreibst du die Module. Jedes Modul ist ein **Schritt**, kein Thema. Steht am
Ende eines Moduls kein Ergebnis, gehört es zusammengelegt oder gestrichen.

**Der Streich-Test gilt für jede Lektion:** kann sie ohne Verlust weg, kommt sie raus.

---

## Der Bauplan

Immer genau diese Reihenfolge, immer **sechs bis acht Blöcke**:

| Block | Was hineingehört |
|---|---|
| **Modul 0 — Willkommen** | Ankommen und vorbereiten. Vier kurze Lektionen: Begrüssung und was sie erwartet · wie ihr fertiges Ergebnis aussieht, mit einem Beispiel · die zwei, drei Begriffe, die sie für diesen Kurs kennen muss · was sie sich jetzt bereitlegt. |
| **Modul 1 — die grösste Sorge** | Nimmt den Einwand weg, der sie sonst nie anfangen lässt. Meistens die Sorge im Kopf, nicht die im Handeln: „das wird ein zweites Business", „ich hab dafür keine Zeit", „mein Team denkt, ich steige aus". |
| **Kern-Module (3 bis 4)** | Die eigentliche Arbeit, in der Reihenfolge des Durcharbeitens. Grobe Bewegung: **erkennen → verstehen → umsetzen → nachbauen**. |
| **Wenn es nicht läuft** | Zeitmangel, Zweifel, Blockaden. Hier beantwortest du **genau die Hürden, die sie selbst genannt hat** — mit einem Notplan, nicht mit Zuspruch. |
| **Dein nächster Schritt** | Zwei Lektionen: ihr Plan für die nächsten sieben Tage, und was sie braucht, um aus dem Gerüst einen fertigen Kurs zu machen. |

Pro Modul **zwei bis vier Lektionen**, durchnummeriert (`0.1`, `1.1`, `2.3` …) und jede
ein konkreter Handgriff. Keine Überschriften wie „Einführung" oder „Grundlagen".

**Pro Modul genau ein `material`** — ein Arbeitsblatt, eine ausfüllbare Vorlage, eine
Checkliste, etwas zum Ausdrucken. Das ist, was sie in den Händen hält. Beim letzten
Modul darf es fehlen.

---

## Felder

| Feld | Was hineingehört |
|---|---|
| `name` | der Kursname, ein bis zwei Wörter |
| `versprechen` | die zweite Hälfte der Namensformel, geschärft |
| `ergebnis` | etwas Anfassbares, gern mit einem „inklusive …" dahinter. **Nur das Ding selbst, ohne Einleitung** — „einen ausgefüllten Plan für die nächsten 21 Abende", nicht „Am Ende hast du einen ausgefüllten Plan". Die Seite setzt „Am Ende hast du:" selbst davor. |
| `fuer_wen` | eine konkrete Person |
| `module` | sechs bis acht, in der Reihenfolge |
| `abschluss` | ein, zwei Sätze zum Schluss: was sie geschafft hat, und wohin der nächste Schritt zeigt. Warm, ohne Kitsch, ohne erfundene Zahlen. |

**Pro Modul:**

| Feld | Was hineingehört |
|---|---|
| `nummer` | „Modul 0", „Modul 1" … |
| `titel` | das Ergebnis dieses Moduls, in ihrer Sprache |
| `klammer` | drei bis sechs Wörter, die in Klammern dahinterstehen und den Modultitel erklären |
| `lektionen` | zwei bis vier, jede als `{ "nummer": "1.2", "titel": "…" }` |
| `material` | ein Satz, womit sie arbeitet |

---

## Ausgabeformat

**Antworte ausschliesslich mit JSON, ohne Fliesstext davor oder danach, ohne
Code-Zaun.** Genau diese Form:

```
{
  "name": "…",
  "versprechen": "…",
  "ergebnis": "…",
  "fuer_wen": "…",
  "module": [
    {
      "nummer": "Modul 0",
      "titel": "Willkommen",
      "klammer": "Ankommen und vorbereiten",
      "lektionen": [
        { "nummer": "0.1", "titel": "…" },
        { "nummer": "0.2", "titel": "…" }
      ],
      "material": "…"
    }
  ],
  "abschluss": "…"
}
```
