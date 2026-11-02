---
tags: [plan, planung, cockpit, monatsplan, jahresplan]
---

# Der Planungs-Kreislauf — ein Skill, vier Zeiträume, kein Notion mehr

**Erstellt:** 02.11.2026 · **Löst ab:** `plans/2026-09-14-monatsabschluss-automatik.md`
(nie gebaut, „Gebaut wird: nach dem Startklar-Launch ab 22.9.") — dessen Phasen A/B/C,
die vier Ebenen und die beiden bestätigten doTERRA-Entscheide werden **übernommen**,
nicht neu erfunden.

---

## Worum es geht

Patricia: *„dann gibt es nen skill mit monatsplanung, jahresplanung, quartalsplanung
usw. das alles am liebsten unter dem oberthema planung"* · *„ich will nichts mehr in
notion. alles von notion, alle abläufe, alle fragen, soll im cockpit abgebildet sein"* ·
*„auch hier fehlt mir die automation dahinter. wann werden fragen geklärt, zahlen
abgefüllt"*.

Ein Skill **`/planen jahr | quartal | monat | woche`**. Je Zeitraum ein Bogen im
Cockpit, die Fragen als geführter Dialog statt leerer Felder, die Zahlen füllt der
Abgleich, ein Task eröffnet den Zeitraum. Notion kommt nirgends mehr vor.

## Warum

Drei Dinge, an denen man es heute merkt:

1. **Es gibt keinen Task für die Planung.** Darum steht im Novemberplan wörtlich
   *„Kein geschlossener `/monatsplan`-Durchlauf"* — beide Novemberpläne sind im Chat
   entstanden, nicht über den Skill.
2. **Der Wochenbogen im Cockpit zeigt eine alte Woche.** Niemand eröffnet die neue.
3. **Notion hat gefragt, indem es leere Felder hingestellt hat** — und genau deshalb
   standen sie monatelang leer. Ein Feld füllt niemand. Eine Frage beantwortet man.

Dazu fehlt das **Quartal** ganz, obwohl Julias Material dazu eindeutig ist:
*„ohne Quartalsplanung keine 10k"*.

---

## Die drei Schärfungsstufen (Patricias Entscheid, 02.11.2026)

> *„im grundsatz will ich mal die jahresplanung machen mit ferien, grundsatzthemen KI,
> mama ceo, instagram usw. und dann mach ich die quartalsplanung wo ich noch etwas
> detaillierter den leadmagneten festsetze, workshop plane usw. und dann die
> monatsplanung ganz ins detail mit beiträgen, storys usw."*

| Zeitraum | Wie fein | Wann |
|---|---|---|
| **Jahr** | Ferien · Grundsatzthemen (KI · Mama-CEO · Instagram · doTERRA) · grobe Launch-Fenster · Umsatzziel | Dezember, zusammen mit Q1 |
| **Quartal** | Leadmagnet festsetzen · Workshops terminieren · welches Angebot wann · Monatsthemen der drei Monate | **letzter Monat des laufenden Quartals**: Mär → Q2 · Jun → Q3 · Sep → Q4 · Dez → Q1 |
| **Monat** | ganz ins Detail: Beiträge, Storys, Mails, Dreh-Liste | **am 29.** (Patricias Entscheid) |
| **Woche** | Rahmen + Ausführung, kein neuer Content | Sonntagabend |

🚨 **Der ganze Content wird im MONAT gebaut, nicht in der Woche** — Patricia, 02.11.:
*„eigentlich plane ich den content für den ganzen monat"* und auf die Rückfrage
*„ne die a/b varianten, hooks prüfung usw. soll bitte auch pro monat geschaut werden"*.
Also auch die A/B-Varianten je Platz und die Hook-Prüfung (`hook-sperre.py`,
Markt-Paket, Vorbilder) laufen **einmal im Monat** statt wöchentlich.

**Damit wird `content-woche-freitag` überflüssig.** Übergang, damit keine Lücke
entsteht: der Task **bleibt an**, bis `/planen monat` steht und einmal durchgelaufen
ist — dann wird er abgeschaltet und archiviert, nicht vorher. Sonst baut drei Wochen
lang nichts mehr automatisch.

**Warum Monat und nicht Woche** (Patricia war unsicher, 02.11.: *„bin mir voll
unsicher. mein veto ja immer: so wenig aufwand wie möglich. monatsplanung wäre mir
schon symphatischer"*). Drei Belege statt Geschmack:

1. **Der Freitags-Task lief vom 18.09. bis 02.11. nicht — und es ist niemandem
   aufgefallen.** Ein Taktgeber, dessen Ausfall man nicht merkt, war keiner.
2. **Die Begründung für „wöchentlich" trifft hier nicht.** Sie steht in CLAUDE.md
   („Live-Posts brauchen Frische, Trends müssen reagiert werden, Pre-Sale-Signale aus
   Woche 1 ändern Wochen 2–4"), aber Patricias Beiträge leben von eigenen Szenen und
   Hooks aus dem Markt-Paket, nicht von Tagestrends. Reaktionsfähig bleibt sie über
   Testreels und Storys, und ein Platz lässt sich jederzeit umhängen.
3. **Julia baut im Block:** *„Unternehmertum: einmal durchziehen, dann chillen"* —
   20 Stunden am Stück für drei Monate Content. Dazu aus `zeit.md`:
   *„eins, zwei, drei zu viel"*, eine Stunde fokussiert schlägt einen Tag Herumtrödeln.

🚨 **Eine Sache bleibt wöchentlich — der Treffer-Check.** Hat ein Beitrag in 14 Tagen
≥ 2× den eigenen Median erreicht, gehören die nächsten zwei bis drei Plätze
Folge-Beiträgen (`/content` Schritt 2b). Das braucht **keinen eigenen Task**: der
tägliche Abgleich um 06:15 sieht die Zahlen ohnehin und meldet es per Telegram.

🚨 **Zwei Sätze in CLAUDE.md werden damit falsch** und gehören nachgezogen:
„Strategie monatlich, Konkretion wöchentlich" (Abschnitt `/monatsplan`) und
„🤖 Automatik (Normalfall): Fr 08:00" (Abschnitt `/content`).

### Der Tag — Routinen und Journaling (Patricia, 02.11.: „der ganze workflow soll da rein")

Die Vorlage verlinkt eine Tagesansicht; das ist der **Tagesplaner**
(`2ae7078e-8b7e-8102-a640-c046d70a2ae7`), 13 Felder:

| Business | Privat |
|---|---|
| `Tagesfokus` · `Tag geplant` · `Learning des Tages` · `Story gemacht, Beitrag veröffentlicht` · `Blick auf Morgen` | `Jornaling` *(so geschrieben)* · `Wie war der Tag?` (⭐1–5) · `Sport Gymondo` · `EFT` · `Auraimpulse gelesen` · `Essensplanung 100gr Proteine` |

**Beides kommt mit**, aber getrennt platziert:

- Die **Business-Felder** gehören auf Mein Tisch in die Zone „Heute".
- Die **privaten Routinen und das Journaling** bekommen einen eigenen Reiter im
  Bereich Privat — 🚨 **nicht** auf die Startseite, weil Patricia das Cockpit
  Kundinnen zeigt.
- Die Tageseinträge **füttern die Wochen-Reflexion**: „Erfolge letzte Woche" und
  „Herausforderung letzte Woche" werden aus den sieben Learnings vorbelegt, statt
  gefragt zu werden. Genau das meint „nur fragen, was sich nicht ableiten lässt".

✅ **Das Cockpit steht privat** (Patricia bestätigt, 02.11.2026). Damit darf das
Journaling hinein. Die widersprüchliche Stelle in CLAUDE.md („steht auf Anyone with the
link") ist am 02.11. korrigiert.

✅ **Der Notion-Tagesplaner wird stillgelegt** (Patricia, 02.11.: *„wird stillgelegt.
will es nur noch übers cockpit machen"*) — also kein Zweitort, nach der Regel „jedes
Feld hat genau einen Ort". Die Notion-DB bekommt einen Umzugshinweis und bleibt nur
noch Archiv, wie die Garten-Datenbanken seit dem 25.10.

---

## Was in jeden Bogen gehört

### Jahr
Der **Jahresplaner existiert schon** als Artifact (`5d3M…`, Patricias Testfassung mit
ihren 17 Angeboten und den Schulferien 2027). Er zieht als **Jahr-Bogen** ins Cockpit
um; die teilbare Kundinnen-Seite (`72vi…`) bleibt separat als Freebie zum Workshop am
17.12. Schritte wie heute: Rückblick · Vision · Leben zuerst · Angebote · Jahr · Woche,
plus 12-Monats-Übersicht, Umsatz-Check und Lücken-Check.

### Quartal (neu)
Kein neuer Fragenkatalog, sondern **Feinschliff auf dem Jahresplan** — Patricia:
*„auch wenn wir von der jahresplanung sicher schon einiges übernommen haben. aber der
feinschliff oder anpassungen kommen im quartal"*. Deckt sich mit Julia:
*„Pläne dürfen verändert werden; man steckt nicht fest."*

- Rückblick auf das Quartal: **grösster Erfolg · stolzeste Kundenerfolge ·
  Herausforderungen und Lösungen · was kommt im nächsten Quartal**
  (Julias eigene Rückblick-Fragen)
- die drei **Monatsthemen** des Quartals — Julias Muster: Mindset → Strategie →
  Umsetzung
- je Monat: **Leadmagnet** und **Workshop/Launch-Fenster** festsetzen
- Abgleich: was vom Jahresplan noch nicht passiert ist

### Monat
Kommt aus `/monatsplan` und dem Plan vom 14.09., unverändert in der Sache:
Phase 2 Vormonats-Diagnose · Phase 3 die acht Fragen · Phase 4.5 Content-Vorplanung
mit Dreh-Liste · Recycling-Vorschläge. **Phase 5 schreibt künftig ins Cockpit statt
nach Notion.**

### Woche — das steht in ihrer Notion-Vorlage (am 02.11. nachgelesen)

**Vorlage:** Seite „Vorlage Wochenplanung" `3167078e-8b7e-80e2-99a4-d6272bd3cdc4`
in der DB `2ae7078e-8b7e-81ef-a769-cdb1a6584c70`.

Zwölf Felder: `Woche` · `Zeitraum` · `Fokus der Woche` · `🎯 Wochen-Hauptprodukt` ·
`Wochen-CTA` · `📅 Sales-Pattern` · `Erfolge letzte Woche` ·
`Herausforderung letzte Woche` · vier Haken (`Contentplanung` · `Mails check up` ·
`Downloadordner aufgeräumt` · `Internet Tabs geschlossen`).

Dazu im Körper drei Blöcke:

| Block | Inhalt |
|---|---|
| **Reflexion der letzten Woche** | Erfolge · Herausforderungen · Routinen und Learnings |
| **Planung der nächsten Woche** | Fokus · **„Was planst du je Business-Säule?"** als Tabelle mit fünf Zeilen (Kundenarbeit · Produktentwicklung · Business-Struktur aufbauen · Content-Creation · Weiterbildung) · Wochenplanung (Kalender-Termine, regelmässige Aufgaben, To-dos auf Tage verteilen, überfällige neu terminieren) · **Ausblick 2 Wochen** inkl. Me-Time |
| **Ordnungsroutinen** | Download-Ordner · Browser-Tabs · Mails · Papiernotizen · Kundendaten aktualisieren |

🚨 **Drei der vier Ordnungs-Haken laufen längst automatisch** — Download-Ordner über
`downloads-aufraeumen.py`, Mails über den Task `mails-sortieren-donnerstag` (Do 07:00),
Kundendaten über den Cockpit-Reiter. Der Bogen **setzt diese Haken selbst**, statt
danach zu fragen. Handarbeit bleiben nur Browser-Tabs und Papiernotizen.

---

## Die Schritte

1. ✅ **`fragen.json` auf vier Zeiträume erweitern.** *(02.11., Jahr unverändert übernommen, Seite und Skill byte-identisch gegengeprüft)* Heute liegen dort nur die
   Jahres-Fragen (`scripts/jahresplan/fragen.json`), und sie sind **die eine Quelle**
   für Seite, Skill und künftig Cockpit-Bogen. Dazu kommen Quartal, Monat (die acht aus
   `/monatsplan`) und Woche (die Felder und Blöcke oben).
2. ✅ **`/planen` als Skill anlegen** *(02.11., 636 Zeilen aus den drei Vorgängern übernommen, Bauskript `scripts/jahresplan/planen-skill-bauen.py`; Namen und Notion-Quellen beim Übernehmen herausgezogen, Gegenprobe an beiden Enden getestet)*, `jahr|quartal|monat|woche` als Parameter. Inhalte
   aus `/jahresplan` und `/monatsplan` hineinziehen, **nichts neu schreiben**. Der
   Fragenblock wird wie heute zwischen den `FRAGEN`-Marken erzeugt.
3. **Vier Bögen im Cockpit.** Monat und Woche existieren (`monatsbogen-bauen.py`,
   `wochenbogen-bauen.py`), Jahr kommt aus dem Jahresplaner-Artifact, Quartal ist neu.
   Je Bogen ein eigenes Dokument, **gehört Patricia** — der Abgleich schreibt nie mit
   `set` darüber (dieselbe Regel wie `daten/produkt-details`).
4. **Der Dialog als Pop-up.** Ist der Bogen des laufenden Zeitraums leer oder vom
   vorherigen, kommt beim Öffnen des Cockpits ein Dialog: eine Frage nach der anderen,
   kein Formular mit zwölf Feldern. Danach steht der Bogen.
5. **Vier Tasks, die den Zeitraum eröffnen.** Muster ist `cockpit-daten-abgleich`:
   Zahlen holen, Diagnose schreiben, Fragen hinlegen, Telegram. Woche Sonntagabend ·
   Monat am 29. · Quartal im letzten Monat des Quartals · Jahr im Dezember.
6. **Notion abklemmen.** `/monatsplan` Phase 5a schreibt heute in die
   Notion-Monatsplanung — das wird der Cockpit-Bogen. Danach: kein Skill und kein
   Skript schreibt mehr nach Notion.
7. **Mein Tisch auf drei Zonen.** Oben eine Zeile **Heute** (Termin · fälliger Beitrag ·
   offene Planungsfrage, sonst nichts) · Mitte **Diese Woche** (Fokus, die fünf Plätze
   je Profil, was fehlt, roter Punkt bei offener Frage) · unten eingeklappt **zum
   Nachschlagen** (Aufgaben, offene Chats, Kalender, Helferinnen).
8. **`cockpit` archivieren**, erst jetzt — sein Text ist bis dahin die einzige
   geschriebene Vorlage für den Quartalsblick.
9. **`jahresplan` und `monatsplan` archivieren**, Beschreibungen und CLAUDE.md
   nachziehen.

---

## Woran wir merken, dass es fertig ist

- `/planen quartal` im Dezember erzeugt einen Q1-Bogen, und **Patricia plant ihr
  eigenes Q1 damit** — vor dem Workshop am 17.12., wo sie dasselbe zeigt.
- **Gegenprobe, die anschlagen muss:** `git grep -il "notion"` über `.claude/skills/`
  findet in `/planen` **keine** Schreibstelle mehr (Lesen aus Notion ist erlaubt,
  solange etwas nur dort liegt).
- **Gegenprobe, die NICHT anschlagen darf:** nach dem Umbau zeigt
  `python scripts/cockpit/testfassung-bauen.py` + lokale Prüfung alle vier Bögen mit
  Inhalt, und kein Reiter wirft einen Konsolenfehler.
- Ein Blick ins Cockpit am Montagmorgen beantwortet „was ist heute dran" in **einer
  Zeile**, ohne Scrollen. Das war der Grund, warum es den Push-Bot gebraucht hat.
- Die vier Tasks stehen in `list_scheduled_tasks` auf `enabled: true` und haben je
  einen Lauf mit Ergebnis.

---

## Was bewusst nicht dazugehört

- **Der Content selbst.** Den baut `/content` (Monat) — `/planen` setzt nur den Rahmen.
- **`/strategie`.** Bleibt ein eigener Skill: das ist eine Frage („was ist der
  Engpass"), kein Zeitraum.
- **Das Private.** Haushalts-Liste, Tagesplaner-Privatteil und Garten bleiben, wo sie
  sind (Patricia, 24.09.: *„ja für ds private behalte ich notion vorerst"*).
- **Keine neue Routine, kein zweiter Ort.** Alles, was es schon gibt, wird
  weiterverwendet, nicht danebengelegt.

---

## Was es berührt

| Datei | Was |
|---|---|
| `.claude/skills/jahresplan/` · `monatsplan/` · `cockpit/` | gehen in `/planen` auf, danach Archiv |
| `scripts/jahresplan/fragen.json` + `tool-bauen.py` | eine Quelle, künftig drei Ausgänge |
| `scripts/cockpit/monatsbogen-bauen.py` · `wochenbogen-bauen.py` · `patch-*` | Bögen und Dialog |
| `scripts/cockpit/patch-mein-tisch.py` | drei Zonen |
| Artifact `5d3M…` (Jahresplaner Patricia) | zieht als Jahr-Bogen ins Cockpit |
| Artifact `72vi…` (Kundinnen-Seite) | bleibt, ist das Workshop-Freebie |
| `CLAUDE.md` | Abschnitte `/monatsplan`, `/jahresplan`, Skill-Tabelle, Notion-Ablösung |
| `plans/2026-09-24-notion-abloesen.md` | Stand nachziehen |
| `plans/2026-09-14-monatsabschluss-automatik.md` | Verweis „abgelöst durch diesen Plan" |

🚨 **Dieselbe Aussage steht an mehreren Stellen** (Lehre vom 19.10.): der Planungs-
Rhythmus steht in CLAUDE.md, in `/monatsplan`, in `/jahresplan`, in den Task-Dateien
und in der Kursfassung `scripts/ki-kurs/grundgeruest-bauen.py`. Wird er geändert,
gehören **alle** nachgezogen und per `grep` gegengeprüft.

🚨 **Die DB-ID der Wochenplanung in CLAUDE.md ist falsch.** Dort steht
`2ae7078e-8b7e-81e7-9083-000b01908eb5`; die echte ist
`2ae7078e-8b7e-81ef-a769-cdb1a6584c70`. Beim Umbau korrigieren oder — besser — ganz
entfernen, wenn Notion abgeklemmt ist.

---

## Julias Methodik — was übernommen wird und wo sie sich widerspricht

Patricia, 02.11.: *„alles nach der strategie von julia trost … wir haben die
ausdrückliche erlaubnis und aufforderung alles von ihr zu kopieren."* Also 1:1
übernommen, Quelle `reference/julia-trost/learnings/themen/jahresplan.md` und `zeit.md`:

- **„ohne Quartalsplanung keine 10k"**
- **„Pläne dürfen verändert werden; man steckt nicht fest"** — eine neue Idee darf den
  Januar und das Folgejahr umwerfen
- **Quartalsthemen** Mindset → Strategie → Umsetzung über die drei Monate
- **Kalender-Struktur:** Wochenzeilen, pro Monat ein Blatt, Spalten Stories · E-Mail ·
  Feed · Launch-Phase · Minikurs · Sonstiges
- **Rückblick-Fragen:** grösster Erfolg · stolzeste Kundenerfolge · Herausforderungen
  und Lösungen · was kommt im nächsten Quartal
- **Struktur-Reihenfolge** (aus `zeit.md`): Privates zuerst in den Monat, dann feste
  Termine, dann Storys, dann die Lücken füllen
- **Kapazität:** „eins, zwei, drei zu viel" — eine Stunde fokussiert bringt mehr als
  ein Tag Herumtrödeln, eine Deadline hilft

🚨 **Beim Vorausplanen sagt Julia fünf verschiedene Dinge**, und ihr eigenes Themenbuch
führt den Widerspruch auf: *„immer 90 Tage vor"* · *„bis drei Monate im Voraus"* ·
*„1–1,5 Monate"* · *„Quartale anschauen, das Jahr grob"* · *„Quartalsplanung alle drei
Monate"* · *„früher drei Monate, jetzt sechs"*. **Hier gilt Patricias Entscheid**
(Jahr grob, Quartal mittel, Monat fein) — keine dieser Zahlen wird als *die* Regel
hingeschrieben.

---

## Entschieden am 02.11.2026

1. **Der ganze Content läuft im Monat** — inklusive A/B-Varianten und Hook-Prüfung.
   `content-woche-freitag` bleibt an, bis `/planen monat` einmal durchgelaufen ist,
   danach aus.
2. **Das Pop-up fragt nur, was sich nicht ableiten lässt.** Alles andere wird
   vorbelegt und steht zum Korrigieren da.
3. **Journaling und Tagesroutinen kommen mit** — Business-Felder auf Mein Tisch,
   Privates in einen eigenen Reiter, und die Tageseinträge belegen die
   Wochen-Reflexion vor.

4. **Der Content wird im Monat gebaut, nicht in der Woche** — Begründung oben.
   Wöchentlich bleibt nur der Treffer-Check, und den macht der 06:15-Abgleich.
5. **Das Cockpit steht privat**, das Journaling darf hinein.
6. **Der Notion-Tagesplaner wird stillgelegt**, kein Zweitort.

## Offen — gehört Patricia

Zum jetzigen Stand nichts mehr. Der Plan ist entscheidungsreif; was beim Bauen
auftaucht, kommt hierher.

---

## 🔗 Verwandte Notizen

- [[2026-09-14-monatsabschluss-automatik]] — abgelöst, Inhalt übernommen
- [[2026-09-24-notion-abloesen]] — die Landkarte über alle 25 Blätter
- [[2026-10-26-reihenfolge-nov-bis-jan]]
