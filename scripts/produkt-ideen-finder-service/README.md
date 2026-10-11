# Produkt-Ideen-Finder

Das Werkzeug hinter dem ManyChat-Keyword **STANDBEIN**. Eine Network-Mama schreibt
hinein, worüber sie mehr weiss als andere — und bekommt drei Ideen für ihr eigenes
digitales Produkt plus das komplette Inhaltsverzeichnis zu der Idee, die sie wählt.

**Seit 14.09.2026 ein Formular in drei Schritten**, kein Chat mehr:

```
1. Dein Thema   →   2. Deine Ideen   →   3. Inhaltsverzeichnis
   ein Feld          drei Karten          vier bis sechs Module
```

Die Chat-Version liegt vollständig in `_archiv-chat-version/` — sie brauchte sechs
Runden bis zur ersten Idee.

---

## Aufbau

| Datei | Was sie tut |
|---|---|
| `public/index.html` | die Seite: Kopf, Schritt-Anzeige, drei Bereiche |
| `public/app.js` | die Abläufe; **hier steht der ThriveCart-Link** (`KURS_LINK`) |
| `public/styles.css` | Patricias Farben und Schriften |
| `api/finder.js` | **ein** Endpunkt für alle drei Schritte, Modus steht im Body |
| `api/health.js` | Lebenszeichen |
| **`lib/wissen-produkterstellung.md`** | **Patricias Methode — steht vor jedem Schritt** |
| **`lib/pruefen.js`** | **die Qualitätsprüfung in Code** |
| `lib/nachbessern.js` | der Reparatur-Durchgang |
| `lib/*.test.mjs` | Testfälle dazu, laufen ohne API-Schlüssel |
| `lib/prompt-ideen.md` | Schritt 2 — die drei Ideen |
| `lib/prompt-titel.md` | „↻ Anderer Name" |
| `lib/prompt-gliederung.md` | Schritt 3 — das Inhaltsverzeichnis |
| `lib/prompt-nachbessern.md` | der Reparatur-Durchgang |

Jeder Prompt ist eine eigene Datei. Wer etwas am Ton oder an den Regeln ändern will,
ändert die Datei — nicht den Code.

---

## Das Wissen dahinter

Ohne Fachwissen baut so ein Werkzeug allgemeine Marketing-Kurse. `api/finder.js` stellt
deshalb **vor jeden** der drei Prompts die Datei `lib/wissen-produkterstellung.md`.

Darin steht Patricias eigene Methode aus „Vom Networkwissen zur digitalen Produktwelt" —
nicht angelesenes Marketing-Wissen:

- **die Schlüsselfrage:** welches Problem hat ihr Mensch, *bevor* er das Network-Produkt
  braucht
- **ihre fünf Schritte:** Idee · Struktur · Inhalt · Aufnahme · Hochladen.
  Das Werkzeug macht 1 und 2, der 39er-Kurs macht 3 bis 5.
- **der rote Faden in vier Schritten:** das Ende zuerst, rückwärts denken, Lücken prüfen,
  den Anfang setzen — plus der Streich-Test
- **der Minikurs-Aufbau:** Willkommen · 3–4 Kern-Module à 2–4 Lektionen · nächster
  Schritt. Dazu „mehr ist nicht unbedingt mehr" und der A-nach-D-Sprung.
- **jede Lektion in drei Teilen**, acht bis fünfzehn Minuten, ein Material pro Modul
- **die Namensformel**, nach der Ideen und Kurstitel gebaut werden:
  `[Name] — [Verb] [Ergebnis] [Zeitrahmen], ohne [Befürchtung], auch wenn [Einwand]`
- die Sprachregeln: Alltagssprache, ganze Sätze, Schweizer ss, keine erfundenen Zahlen,
  **keine Heilversprechen**, und nie gegen das Network argumentieren

Quellen im Repo: `context/Kurse/aktuelle kurse/Digitale Produktwelt/Transkripte/` und
`outputs/produkte/vom-networkwissen-zur-digitalen-produktwelt/`.
**Ändert sich dort etwas Grundsätzliches, gehört es hier nachgezogen.**

⚠️ In den `lib/`-Dateien stehen **keine fremden Mentorinnen-Namen und keine zugekauften
Kataloge** — das Repo ist öffentlich.

---

## Woher weiss das Werkzeug, dass die Idee gut ist?

In drei Stufen — und nur die mittlere scheitert wirklich.

**Stufe 1 · Der Prompt sagt, was gut heisst.** Am Ende von `prompt-ideen.md` stehen
sechs Fragen, die vor dem Absenden durchgegangen werden. Nützlich, aber allein zu wenig:
ein Modell, das seine eigene Arbeit bewertet, sagt fast immer „passt".

**Stufe 2 · `lib/pruefen.js` prüft in Code nach.** Kein Urteil über Geschmack, sondern
Dinge, die sich messen lassen:

| | |
|---|---|
| Name | höchstens drei Wörter, keiner doppelt |
| Versprechen | enthält **„ohne …"** und **„auch wenn …"** — sonst ist die Formel nicht fertig |
| „für wen" | zu kurz heisst zu allgemein |
| Problem | zu kurz heisst Stichwort statt Szene |
| Ergebnis | fängt es mit „mehr Klarheit / Selbstvertrauen / Motivation …" an, ist es ein Gefühl und nichts in der Hand |
| Heilversprechen | *heilt · lindert · hilft gegen · wirkt gegen · bekämpft …* |
| Fachwörter | *Positionierung · Sichtbarkeit · Funnel · Hybridmodell · skalieren …* |
| erfundene Zahlen | Zahl + *% / CHF / Franken / Kundinnen / Follower* — Zeitrahmen bleiben erlaubt |
| Stakkato | drei sehr kurze Sätze hintereinander |
| ß | Patricia schreibt Schweizer ss |
| Quellen | die drei Ideen kommen aus drei verschiedenen Ecken |
| Network | die Firma darf nicht im Namen oder im Versprechen stehen — sie ist Baustein, nicht Aufhänger |

Für das Inhaltsverzeichnis dasselbe: sechs bis acht Module · Modul 0 ist Willkommen ·
„Wenn es nicht läuft" ist da · „Dein nächster Schritt" ist da · zwei bis vier Lektionen
je Modul · Lektionsnummern passen zum Modul · Material je Modul · keine Lektion, die
nur „Einführung" oder „Grundlagen" heisst.

**Stufe 3 · Nachbessern.** Findet Stufe 2 etwas, geht der Entwurf **mit den konkreten
Beanstandungen** ein zweites Mal zu Claude (`prompt-nachbessern.md`). Danach wird erneut
geprüft und das Ergebnis nur übernommen, wenn es wirklich weniger Beanstandungen hat.
**Genau ein Durchgang** — wer zweimal nachbessert, dreht sich im Kreis und lässt die
Frau warten.

Repariert wird **so klein wie möglich**: Betreffen alle Beanstandungen einzelne Ideen
oder einzelne Module, geht auch nur das Kaputte zurück — ein paar Sekunden statt einer
halben Minute, und die guten Teile können dabei nicht beschädigt werden. Nur eine
Beanstandung, die das Ganze betrifft („die drei Ideen kommen nicht aus drei Quellen",
„es müssen sechs bis acht Module sein"), schickt den kompletten Entwurf zurück.

🚨 **Der Zeit-Wächter.** `maxDuration` steht bei 60 Sekunden, der erste Entwurf braucht
gemessen 20 bis 36. Deshalb rechnet `nachbessern.js` mit, wie viel Zeit noch da ist, und
lässt die Reparatur aus, wenn sie nicht mehr sicher hineinpasst — lieber der erste
Entwurf als eine abgewürgte Funktion, bei der gar nichts ankommt. Genau daran ist die
erste Fassung gescheitert: die Prüfung fand etwas, die Reparatur kam nie dazu. Erst der
kleine Zuschnitt hat es hineinpassen lassen.

Was am Ende offen bleibt, steht in `meta.offen` und in den Vercel-Logs. Nichts davon
sieht die Nutzerin; sie bekommt das beste Ergebnis, das durchkam.

### Und was das Werkzeug ehrlicherweise NICHT weiss

Ob jemand für die Idee **bezahlt**. Das kann kein Modell vom Schreibtisch aus wissen,
und so zu tun als ob wäre der eigentliche Fehler.

Deshalb hat jede Idee das Feld **`beleg_check`**: eine Prüfung, die die Frau heute
selbst machen kann — mit Suchwort, Frage und Schwelle. „Tipp ‚wie machst du' in die
Chat-Suche; mehr als drei Treffer aus drei Monaten heisst, das Thema ist da." Das ist
Patricias eigener Schritt 1 („Woher weiss ich, dass das gefragt ist?"), und es ist die
einzige ehrliche Antwort auf die Frage.

**Selbst testen** — beide laufen ohne API-Schlüssel und ohne Kosten:

```bash
cd "scripts/produkt-ideen-finder-service" && node lib/pruefen.test.mjs && node lib/nachbessern.test.mjs
```

`pruefen.test.mjs` hält einen absichtlich schlechten Entwurf gegen einen guten.
**Der gute muss 0 Beanstandungen haben** — kommt dort etwas, ist die Prüfung zu streng
geworden und wirft brauchbare Ideen weg. `nachbessern.test.mjs` prüft die Mechanik der
Reparatur mit einer Attrappe statt Claude: dass nur das Kaputte zurückgeht, dass die
guten Teile unberührt bleiben, dass eine Reparatur verworfen wird, die nichts besser
macht, und dass bei zu wenig Zeit gar nicht erst gerufen wird.

### Gemessen am 14.09.2026 (echte Läufe gegen die API)

| Schritt | Dauer | Rein/Raus |
|---|---|---|
| Ideen | 33–37 s, mit Reparatur 45 s | ~4'800 / ~1'700 Token |
| Inhaltsverzeichnis | 22–28 s | ~4'800 / ~1'600 Token |
| Anderer Name | ~3 s | ~3'700 / ~110 Token |

Vier Läufe: dreimal kam der erste Entwurf sauber durch, einmal fing die Prüfung eine
Idee namens **„Ölritual"** — das Network-Produkt als Aufhänger — und die Reparatur hat
sie ersetzt. Genau dafür ist sie da.

---

## Eine Abweichung, die bewusst so ist

Patricia hat als Vorbild eine Gliederung mit acht Modulen geschickt. Ihre eigene
Kurs-Regel sagt dagegen „maximal fünf Lektionen" für einen Minikurs, an anderer Stelle
„drei bis vier Module à drei bis fünf Lektionen".

Das Werkzeug fährt die **mittlere Linie**: Modul 0 Willkommen · ein Modul gegen die
grösste Sorge · drei bis vier Kern-Module · „Wenn es nicht läuft" · „Dein nächster
Schritt" — also sechs bis acht Blöcke, aber nur drei bis vier davon unterrichten
wirklich. Damit sieht es aus wie ihr Vorbild und verletzt ihre Regel nicht.

Soll es kürzer werden: in `lib/prompt-gliederung.md` die Kern-Module auf zwei bis drei
setzen. Steht an einer Stelle, nicht im Code.

---

## Starten

```bash
npm install
npx vercel dev          # lokal, braucht ANTHROPIC_API_KEY
npx vercel --prod       # veröffentlichen
```

Nötig ist nur **`ANTHROPIC_API_KEY`**. Die ActiveCampaign-Schlüssel aus
`.env.example` braucht die Formular-Version nicht mehr (siehe unten).

---

## Drei Entscheidungen, die hinter dem Umbau stehen

### 1. Das Inhaltsverzeichnis wird verschenkt

Die alte Fassung hatte das ausdrücklich verboten: *„Verrate NIE den ganzen Bauplan.
Kein Inhaltsverzeichnis, keine Modulliste."* Patricia hat das am 14.09. gedreht, und
das Argument trägt:

> *„Im Kurs lernen sie ja dann, wie sie ihn erstellen, wo sie ihn hosten und verkaufen.
> Schon nicht ganz dasselbe."*

Ein Inhaltsverzeichnis ist eine Reihenfolge. Der 39er-Kurs ist die Umsetzung — aufnehmen,
hochladen, Checkout, verkaufen. Das Werkzeug beweist, dass die Reihenfolge steht; der
Kurs ist der Weg dorthin. Deshalb steht die Angebots-Karte auch **erst auf Schritt 3**:
wer bis dahin gekommen ist, hat einen Plan und die Frage „und wie jetzt?".

Belegt wird das durch den Konkurrenz-Scrape vom 14.09.: der Beitrag, der die komplette
Methode in fünf Schritten verschenkt, hat 128 Kommentare geholt. Verschenken frisst den
Trichter nicht auf — es beweist ihn.

### 2. Keine E-Mail-Abfrage mehr

Die Leads kommen über das ManyChat-Keyword, **bevor** jemand den Link überhaupt
bekommt. Ein zweites Formular davor kostet nur Abbrüche. `api/lead.js` liegt im Archiv,
falls die Strecke je zurück soll.

### 3. 🚨 Kein extended thinking im Prompt-Aufruf

Das Vorbild-Tool der Mentorin lief am 14.09. in einen Fehler: *„Die KI hat keine
lesbare Antwort geschickt."* Grund ist im Netzwerk-Mitschnitt zu sehen — der Server hat
extended thinking an, der Antwort-Strom beginnt mit einem `thinking`-Block, der die
Laufzeit der Funktion aufbraucht, und beim Browser kommt kein einziges `text_delta` an.

`api/finder.js` fragt deshalb **ohne** thinking, mit gedeckelten `max_tokens` je Schritt
und prüft `stop_reason === 'max_tokens'`, bevor es parst. Das nicht wieder aufmachen.

---

## Wenn etwas nicht geht

| Was zu sehen ist | Woran es meistens liegt |
|---|---|
| „Das Werkzeug ist gerade nicht erreichbar" | `ANTHROPIC_API_KEY` fehlt in den Vercel-Variablen |
| „Die Antwort kam nur halb an" | `max_tokens` im betroffenen Modus zu knapp |
| `prompt-*.md nicht gefunden` | `includeFiles: "lib/**"` in `vercel.json` fehlt |
| Angebots-Knopf führt ins Leere | `KURS_LINK` oben in `public/app.js` setzen |
