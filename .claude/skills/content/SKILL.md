---
name: content
description: "Der eine Instagram-Skill: schreibt Hooks, ein einzelnes Karussell, ein Reel-Skript oder den kompletten Content für eine Woche oder einen Monat — für Sandra, die Network-Mama um 23 Uhr — und legt alles fertig ins Cockpit."
---

# content v2.1

> **Eine Datei, der Reihe nach.** Schritt 1 bis 12, kein Schritt wird übersprungen.
>
> **Und dieser Skill liest alles.** Nicht „bei Bedarf", nicht „wenn du etwas Bestimmtes
> baust". Bei jedem Lauf werden alle Content-Skills und alle Wissensdateien vollständig
> geöffnet. Patricia am 14.09.2026: *„es muss aber einfach alles rein."*

---

## Wofür dieser Skill da ist

Er schreibt Patricias kompletten Instagram-Content für einen Zeitraum und legt ihn
fertig ins Cockpit, damit sie nur noch auswählt und freigibt. Eine Woche sind fünf
Beiträge pro Profil plus ein Story-Bogen; ein Monat vier Wochen plus eine Dreh-Liste.

**Und er ist die eine Stelle für jeden einzelnen Feedbeitrag** (seit 13.10.2026,
Patricia: *„ich stelle mir das halt schon so vor, dass ich einen skill habe für alles und
dann der inhalt der dazu gehört da drin ist“*). Drei Einzelaufträge, ohne die Woche:

| Sie sagt | Dann | Ausgabe |
|---|---|---|
| „Hooks zu X“ | TEIL 0 + TEIL 3 | 8–10 Hooks, Tabelle mit Stil · Säule · Format, zwei Test-Empfehlungen |
| „Karussell zu X“ | TEIL 0 + TEIL 3 + Schritt 6 Karussell | drei Cover-Varianten, Folien, Caption, Platzhalter |
| „Reel zu X“ | TEIL 0 + TEIL 3 + Schritt 6 Reel | drei Hook-Varianten, Clip-Idee, Ablauf in Sekunden, Caption |

Dabei gelten Beitrags-Check (Schritt 7) und Regeln (TEIL 6) genauso. Nicht dafür: ein
Blogartikel (→ `blog`).

---

## Die Säulen

Der Output steht und fällt an fünf Punkten. **Eine Säule schwach = das Ergebnis trägt
nicht** — dann wird überarbeitet, nicht ausgeliefert.

0. **Die Tagesfrage: Was gebe ich ihr heute mit?** Inspiration · einen krassen Tipp ·
   warum mit mir und dass es auch für sie möglich ist. Wird je Beitrag **benannt, bevor
   geschrieben wird**, und über die Woche kommen alle drei vor. Definition:
   `context/brand-voice.md`, Block „Die Tagesfrage“.
1. **Emotion UND konkreter Mehrwert** in jedem einzelnen Beitrag. Emotion öffnet die
   Tür, der konkrete Schritt baut das Vertrauen. Eine Haltung allein speichert niemand.
2. **Typ-Mix über die Woche.** Nie zwei Tage hintereinander derselbe Beitragstyp.
3. **Klarheit in drei Sekunden** — Thema und Welt, nicht nur ein ganzer Satz.
4. **Keyword als Haupt-CTA.** Mindestens drei Keyword-Beiträge pro Woche, genau eins
   pro Beitrag.
5. **Der Beitrags-Check.** Fünf Fragen, eine mit Nein und der Beitrag geht nicht raus —
   auch im Automatik-Lauf nicht.

---

## DER CONTENT-KREISLAUF — wann welche Info woher (seit 13.10.2026)

Patricia: *„nicht einfach als einmal erstellt und abgehakt ablegen, sondern daraus einen
sauberen Ablauf kreieren. von wo nimmst du wann welche infos.“* Sechs Stationen, die sich
im Kreis drehen. **Keine neue Routine:** jede Station hängt an etwas, das schon läuft.

| # | Station | Wann | Wer startet | liest | schreibt |
|---|---|---|---|---|---|
| 1 | **Verstehen** — Wettbewerb · Trends · Fragen der Zielgruppe · Zielgruppenbild mit Säulen | vierteljährlich (Jan · Apr · Jul · Okt), im `/monatsplan` dieses Monats | Patricia ruft `/monatsplan` | `context/competitor-watchlist.json` (Nische `kern`, **zuerst Julia Müller, `referenz: haupt`**) · jüngstes `outputs/apify-runs/competitors-*.json` · `outputs/marktrecherche/2026-10-04-hook-gesamtbericht.md` · WebSearch (Google Trends, Reddit, Foren) · Kommentare und DMs · `context/kundinnen-geschichten.md` | `outputs/zielgruppen-research/<datum>-*/` (vier Analysen) → verdichtet in `wissen/zielgruppe-kurz.md` + `wissen/hook-muster-markt.md` → Cockpit `daten/zielgruppe` (`scripts/cockpit/zielgruppe-bauen.py`) |
| 2 | **Monat planen** | letzter Sonntag im Vormonat | Patricia ruft `/monatsplan` | Station 1 · `outputs/cockpit/abgleich/auswertung.json` (Station 6) · `/strategie` · `active-funnels.json` | `outputs/monatsplaene/JJJJ-MM.md` |
| 3 | **Woche bauen** | Fr 08:00 | Task `content-woche-freitag` (oder `/content woche`) | Monatsplan · `wissen/*.md` · Hook-Paket (`scripts/hooks/beispiele.py`) · frischer Marktcheck · `wissen/hooks-schon-verwendet.md` · Bestperformer-Formel | Cockpit `karussells` / `reels` / `storys`, Varianten A/B |
| 4 | **Freigeben und posten** | täglich | Patricia: Freigabe-Knopf · 19:30 Task `kommentare-einarbeiten` · 20:00 Task `freigaben-einplanen-2000` | Cockpit `freigaben` | Blotato, Instagram |
| 5 | **Messen** | täglich 06:15 | Task `cockpit-daten-abgleich` | Meta Graph API (`holen.py`) · ThriveCart · ActiveCampaign | `auswertung.json` → Cockpit `daten/auswertung` (Bestperformer · Nachfrage je Thema · Diagnose · Stichwörter mit Umsatz) |
| 6 | **Auswerten und zurückführen** | monatlich in `/monatsplan` 4.5b, ein Beitrag zählt erst ab 7 Tagen | `/monatsplan` | `auswertung.json` | siehe Rückfluss unten |

**Der Rückfluss — was aus den Zahlen wohin geht:**

| Befund | geht nach | damit |
|---|---|---|
| Bestperformer-Formel (nur Merkmale, die in den Top 10 häufiger sind als überall) | Station 3, Hook- und Formatwahl | die nächste Woche baut auf dem, was nachweislich trägt |
| gepostete Hooks | `wissen/hooks-schon-verwendet.md` | kein Hook kommt zweimal |
| Thema mit viel Reichweite, aber ohne Speichern und Kommentare | Reichweiten-Beitrag, kein Produkt | Reichweite nicht mit Nachfrage verwechseln |
| Thema, das zwei Monate oben in der Nachfrage steht und kein Angebot hat | `/strategie hebel <Idee>` | Produktidee aus echten Daten, erst testen, dann bauen |
| Stichwort mit Eintragungen und Kauf | Lead-Beiträge der nächsten Woche | das Stichwort, das verkauft, kommt öfter |
| gut gelaufen und ≥28 Tage alt | Cockpit „Kann wieder raus“ | recyceln statt neu bauen |
| neuer Wortlaut aus Kommentaren und DMs | `wissen/zielgruppe-kurz.md` (ihre Wörter) | die Sprache bleibt die ihre |

**Die Projektdatenbank** — was in einem Claude-Projekt die Projektdateien wären, ist hier:
`wissen/*.md` (Zielgruppe, Hook-Muster, schon verwendete Hooks, Beispiel) ·
`context/brand-voice.md` · `context/kern-painpoint.md` · `context/ki-phrasen-blackliste.md` ·
`context/active-funnels.json` · `context/patricia-expertise.md` (Zahlen) ·
`auswertung.json` (was wirkt). **Ändert sich eine davon, gilt das ab dem nächsten Lauf.**

🚨 **Drei Lehren aus der ersten Auswertung**, die in jedem Durchgang gelten:
- **Jede Quote braucht eine Mindestbasis** (über dem eigenen Median und mindestens 3 Reaktionen).
- **Ein Merkmal der Top 10 zählt nur, wenn es dort häufiger ist als bei allen Beiträgen.**
  Lange Captions stehen in 7 der Top 10, aber auch bei 68 % aller Beiträge. Das ist kein Befund.
- **DMs liefert keine Schnittstelle.** Eintragungen über Stichwörter sind der beste Ersatz.

**Für die eigenen Kurse** steht derselbe Ablauf in Kundinnen-Sprache mit eigenen Prompts in
`outputs/produkte/ki-treppe/12-content-kreislauf-kursmaterial.md`.

---

## TEIL 0: FÜR WEN — Sandra um 23 Uhr (seit 13.10.2026)

Aus den drei Kurs-Skills, die Patricia im Kurs „Content Shortcut“ auf ihre Zielgruppenanalyse
gebaut hat (Hook-Generator, Karussell-Texter, Reels-Skript; Originale in
`context/Kurse/aktuelle kurse/Content-Shortcut/skills/`).

**Wissen, das vor jedem Beitrag gelesen wird** (beide Ordner gitignored, sie nennen fremde Konten):

| Datei | Wofür |
|---|---|
| `.claude/skills/content/wissen/zielgruppe-kurz.md` | Phasen, Pain auf drei Ebenen, Gedanken um 23 Uhr, ihre Wörter, Einwände, die fünf Säulen, Formate, unbesetzte Themen |
| `.claude/skills/content/wissen/hook-muster-markt.md` | was bei der Konkurrenz trägt, was abgenutzt ist, Patricias Abgrenzung |
| `.claude/skills/content/wissen/hooks-schon-verwendet.md` | Hooks, die es schon gibt — **nicht wiederholen, nicht leicht umbauen** |
| `.claude/skills/content/wissen/beispiel-karussell.md` | Ton und Rhythmus auf Folien (mit Warnhinweis) |
| `outputs/zielgruppen-research/2026-10-12-content-shortcut/` | die vier Analysen im Volltext, für Zahlen und Zitate |

**Die Leserin heisst Sandra:** 36, zwei Kinder, 40 % Pensum, seit zwei Jahren bei einer
Wellness-Firma, verdient ein paar hundert Franken, ein guter Teil geht in die Eigenbestellung.
Ihr Mann nennt es „dein Ölhobby“. Sie ist weder naiv noch faul, ihr Einsatz folgt nur keinem
Plan. **Kern-Pain:** Sie steckt Zeit, Herz und Geld in etwas, das sie Business nennt, das aber
wie ein teures Hobby aussieht. Darunter die doppelte Abhängigkeit, vom Partner und von Firma,
Kompensationsplan und Upline.

**Drei Phasen:** die Frustrierte (will aufhören, bringt Reichweite) · die Suchende (will anders
weitermachen, wichtigste Followerin) · die Entschlossene (will es ernst meinen, die Kundin).

**Fünf Säulen:** 1 Personal Brand statt Copy-Paste (ca. 30 %) · 2 Plan B und eigenes Geld (25 %,
Patricias Revier) · 3 Business im echten Mama-Alltag (20 %) · 4 Eigenverantwortung statt
Hobbymodus (15 %, direkt ja, abwertend nie, ein Satz Hoffnung gehört dazu) · 5 Beweis und
Angebot (10 %). Roter Faden: vom Network-Business zur eigenen Marke, später zum eigenen Angebot.

**Der 23-Uhr-Test** gilt für jeden Hook, jede Folie, jede Caption: Sandra liegt müde im Bett,
Daumen auf dem Bildschirm. Hält sie an? Liest sie bis zum Schluss? Speichert sie es oder
schickt sie es einer Freundin? Ein Nein und die Stelle wird überarbeitet.

**Mikro statt Makro** (Patricia, 13.10.): Der Hook nimmt das kleine, konkrete Problem, nicht das
grosse Thema. Nicht „5 Hinweise, dass deine Bio nicht passt“, sondern „5 Ideen, woran es liegen
könnte, dass dir auf Insta keine potenziellen Kunden schreiben“. Das erste ist ein Thema, das
zweite ist ihr Abend.

**Patricias Eckdaten — nur diese sind belegt:** vier Kinder · Appenzellerland · 2018 mit Network
Marketing angefangen · 2021 aufgehört · 2023 neu gestartet mit doTERRA und Mum Life Balance,
diesmal mit eigenem Plan. Alles darüber hinaus (Szenen, Sätze des Mannes, Kundinnen-Nachrichten)
steht als **Platzhalter** da, zum Beispiel `[echte Situation einsetzen]`, oder der Hook trägt den
Vermerk **„(nur wenn's stimmt)“**. Ihr Mann macht keinen Spruch mehr; dass er „die Zahlen gesehen“
hat, stimmt **nicht**.

🚨 **Zwei Zielgruppen-Ebenen gelten auch hier.** Sandra ist Patricias Kundin. Wer bei Sandra
kauft, ist **Kundschaft, Leute, Interessenten** — nie „Kundinnen“. „Likes sind keine Käufe“,
nicht „keine Kundinnen“.

---

## TEIL 1: BRIEFING — der Kontext

| Feld | Woher |
|---|---|
| **Zeitraum** | Woche oder Monat — vom Aufruf |
| **Profil** | Mentoring, doTERRA oder beide |
| **Wochenfokus** | Notion-Wochenplanung `collection://2ae7078e-8b7e-81e7-9083-000b01908eb5`. **Oft nicht gepflegt** — dann Monatsplan, und in `quelle` schreiben, woher es kommt |
| **Monatsthema** | `outputs/monatsplaene/YYYY-MM-[profil].md` |
| **Angebot + Keyword** | `context/active-funnels.json` + `context/manychat-keywords.md` |
| **Launch-Lage** | `active-funnels.json` → normal · anwärmen · Türen auf · läuft · letzter Tag · danach |
| **Letzte vier Wochen** | `outputs/karussells/` + `outputs/reels/` |
| **Besonderheiten** | Ferien, reduzierte Woche, Krankheit — nur von Patricia |

### Briefing-Check

| Bereich | Frage | Warum es das Ergebnis verändert |
|---|---|---|
| Fokus | Worum geht es diese Woche in **einem Satz**? | Ohne das sind alle fünf Beiträge beliebig |
| Angebot | Welches Keyword führt wohin, und was bekommt sie dafür? | Der Beitrag wird **vom Angebot her** gebaut |
| Lage | Anwärmen oder verkaufen? | Entscheidet Bewusstseinsstufe und CTA-Härte |
| Vorwoche | Welche Themen und Typen waren dran? | Sonst dreimal hintereinander dasselbe |
| Material | Was liegt an Videos und Fotos? | Ein Reel ohne Material ist ein Auftrag, kein Beitrag |

**Faustregel, dass noch zu viel fehlt:** Wenn du den Wochenfokus nicht in einem Satz in
Patricias Sprache hinschreiben kannst, fehlt er. Dann fragst du — du denkst dir keinen aus.

---

## Standard-Output

Die feste Menge, ohne Rückfrage. **Pro Profil und Woche:**

| | Menge |
|---|---|
| Karussells | **6** — drei Slots, je Variante A und B |
| Reels | **4** — zwei Slots, je Variante A und B |
| Storys | **5** — eine je Wochentag, ausformuliert |
| Hooks in Schritt 4 | **14** — damit A und B verschiedene Angles haben |

**Warum doppelt:** Patricia pickt im Cockpit, statt Korrekturwünsche zu formulieren.
A und B haben **verschiedene Angles** — nie derselbe Gedanke in anderen Worten. Beide
vollständig gebaut, beide durch den Beitrags-Check. Beide dasselbe Datum, im Namen vorne
`A · ` bzw. `B · `. **Die Freigabe ist die Auswahl.**

**doTERRA: Reels only**, solange das Profil unter rund 300 Followern liegt.

Beim Monat: viermal diese Menge plus eine Dreh-Liste, nach Setting gruppiert.

---

## TEIL 2: BEWUSSTSEINSSTUFE

| Stufe | Sie weiss … | Dann gilt |
|---|---|---|
| **1 — unbewusst** | nur, dass etwas anstrengend ist | Szene und Gefühl, **kein** Fachwort, kein Angebot |
| **2 — symptombewusst** | dass es so nicht weitergeht | ihr Satz, nicht meine Antwort |
| **3 — lösungsbewusst** | dass es einen Weg gibt | hier wirkt der konkrete Schritt |
| **4 — angebotsbewusst** | dass es mich gibt | Beweis und Abgrenzung |
| **5 — kaufbereit** | dass sie will | Dringlichkeit und Preis — **nur Story und Mail, nie im Feed** |

**Zuordnung:** Reichweite = 1–2 · Lead = 2–3 · Story und Launch = 4–5.

**Die häufigste Verwechslung:** Ein Hook auf Stufe 1–2 darf das Lösungswort nicht
enthalten. „Sichtbarkeit", „Positionierung", „eigenes Thema", „digitale Produktwelt",
„Hybridmodell" sind **Antworten**, nicht Schmerzen. Sie gehören ab Zeile zwei.

| Fachwort | am Küchentisch |
|---|---|
| Hybridmodell | etwas Eigenes neben dem Network |
| Sichtbarkeit | dass die richtigen Leute dich finden |
| Positionierung | wofür Leute dich fragen sollen |
| eigenes Thema | worüber du wirklich Bescheid weisst |
| digitale Produktwelt | etwas, das verkauft, während du bei den Kindern bist |

---

## TEIL 3: HOOKS

Der volle Katalog steht in `.claude/skills/hooks/SKILL.md` und wird in Schritt 1
**vollständig gelesen**. Was hier steht, gilt immer.

### Die vier Fragen — der letzte Check

Jeder Hook läuft durch. Eine mit Nein und der **Hook** wird umgeschrieben, nie die
Caption nachgebessert.

1. Trifft es wirklich einen Schmerz?
2. Denkt sie „krass, wieso weiss die, was ich denke"?
3. Sagt man das so am Küchentisch zu einer Freundin?
4. **Ist die Lösung draussen?** Die Lösung kommt nie im Hook.

### Klarheit in drei Sekunden

> 🚨 Wer drei Sekunden vorbeiscrollt, muss wissen, **um welche Welt es geht.**
> „Du bist nicht mehr die Neue" kann alles heissen. „Über die Phase **im Network** redet
> keiner: Du bist nicht mehr die Neue, und verdienen tust du trotzdem noch nichts"
> verortet es sofort. (Patricias Korrektur vom 14.09.2026.)

### Im Bild steht der Hook vollständig ab Bild null

> 🚨 Gesprochen tragen Fragmente — die Stimme setzt die Pausen. **Geschrieben und
> stehend im Bild nicht.** Ein Hook, der sich über zwei Einblendungen aufbaut, zeigt in
> Sekunde eins ein Satzfragment. Untertitel allein sind **kein** Hook — die zeigen immer
> nur die letzten drei Wörter.

### Gegner, Geständnis oder Zitat (seit 13.10.2026)

Jeder Hook hat **mindestens eins** davon. Das ist das Muster aller Allzeit-Hits in der
Wettbewerbsanalyse; reine Ergebnisversprechen („So verdienst du mehr“) sind dort die
schwächsten Hooks, Einkommens-Belege die allerschwächsten.

- **Gegner:** eine Abhängigkeit, eine Methode, eine Ausrede, ein Denkfehler. **Nie** eine Firma,
  nie doTERRA, nie eine Person beim Namen, nie Sandra selbst. Feindbilder wechseln — eins, das
  jede Woche kommt, verliert die Überraschung.
- **Geständnis:** Ich-Form, ein konkreter Moment, ein Detail, das man sieht. Nur aus den
  belegten Eckdaten (TEIL 0), sonst „(nur wenn's stimmt)“.
- **Zitat:** wörtlicher Satz von ihr, ihrem Mann, der Upline, ihrem inneren Monolog.
  Fragen wirken **nur als Zitat**, abstrakte Fragen nicht.

| Stil | Mechanik |
|---|---|
| Geständnis / Story | Ich-Form, ein Moment, ein sichtbares Detail |
| Polarisierung | klare Haltung gegen eine verbreitete Methode oder Annahme |
| Pain mit Ironie | ihr Problem so konkret, dass es weh tut, mit Augenzwinkern |
| Zitat | ihr Satz, der des Mannes oder der Upline, dann eine Wendung |
| Erwartung drehen | was sie glaubt oder googelt, aufgreifen und kippen — **die Antwort kommt erst auf Folie 2 oder in der Caption** |
| Weichmacher aufspiessen | „nur nebenbei“, „mal schauen“, „eigentlich“ wörtlich nehmen |
| Frage mit Stachel | eine Frage, die sie sich nicht zu stellen traut — keine Quizfrage |
| Liste mit Gegner | Zahl plus Wertung, nie neutral |
| Zahl mit Haltung | eine nüchterne Zahl, die eine unbequeme Folgerung erzwingt (nur belegte Zahlen) |
| Swiss Angle | Franken, Pensum, AHV, Krankenkasse, Schweizer Zurückhaltung beim Reden über Geld |

**Länge:** 8 bis 18 Wörter, höchstens zwei Sätze, harte Grenze 22. Was länger werden will,
gehört in die Caption — aufs Cover kommt nur der Moment, der neugierig macht.

**Ihre Wörter im ersten Satz:** Eigenbestellung, Upline, nebenbei, mein Mann, posten,
Reichweite, Pensum, die Kinder, eigenes Geld, Plan B. **Nie:** Funnel, Conversion,
Positionierung, Skalierung, Lead-Magnet, Content-Säulen, Monetarisierung.

**Ausgabe beim Einzelauftrag „Hooks zu X“:** ein Satz Einordnung (welcher Pain, welcher Dreh),
dann 8–10 Hooks über mindestens fünf Stile und mindestens drei Säulen, keine Säule mehr als
vier:

| # | Hook | Stil | Säule | Format |
|---|---|---|---|---|

Danach in zwei, drei Sätzen: welche zwei zuerst testen und welcher als Trial Reel taugt.
Neue Hooks statt Varianten der alten, ausser sie will einen bestimmten umgebaut haben.

### Mischung

Bei 14 Hooks pro Profil: mindestens 3× P, 3× I, 3× E · mindestens vier Formel-Familien ·
**mindestens drei Angles**. Jeder Hook ist auf einen Befund aus dem Marktcheck oder den
Wochenfokus rückführbar — Quelle steht in der Tabelle, sonst ist er nicht fertig.

### Abgenommene Hooks fasst du nicht an

> 🚨 Was in der Auswahl steht, ist abgenommen. Passt ein Hook für ein Format nicht,
> **sagst du das** — du schreibst ihn nicht still um, auch nicht beim Kürzen fürs Bild.
> Muss die Bildzeile kürzer sein, legst du die gekürzte Fassung daneben und benennst,
> was rausfällt.

---

## TEIL 4: ANGLES

| Angle | Fragt |
|---|---|
| **Schmerz** | Was tut gerade weh? |
| **Ergebnis** | Was hat sie danach? |
| **Beweis** | Woran sieht man, dass es stimmt? |
| **Konträr** | Was glauben alle, das nicht stimmt? |
| **Identität** | Wer ist sie, wenn das gelöst ist? |
| **Neugier** | Was fehlt ihr an Information? |
| **Vergleich** | Was ist der Unterschied zwischen A und B? |

**Angle ≠ Formel-Familie.** Die Familie sagt, wie ein Hook *klingt* (Bekenntnis,
Zeitanker, Hot Take). Zehn Hooks können sieben Familien haben und trotzdem alle dasselbe
sagen. **Drei bis fünf Angles mischen.** Bei A und B eines Slots immer verschiedene.

---

## TEIL 5: AUFBAU — der Lauf, Schritt für Schritt

---

### SCHRITT 1 · Alles lesen — und das Leseprotokoll ausgeben

> 🚨 **Dieser Schritt endet mit einer sichtbaren Tabelle. Ohne sie ist der Lauf
> ungültig.**

**Die sechs Content-Skills — vollständig, jedes Mal:**

| Datei | Was daraus gebraucht wird |
|---|---|
| `.claude/skills/hooks/SKILL.md` | 16 Teile: Reichweiten-Hierarchie, Kundensprache, Bewusstseinsstufen, Angles, PIE, Formeln, Reveal-Frameworks, Vorlagen, Voice, Verbote, der letzte Check |
| `.claude/skills/karussell/SKILL.md` | vier Karussell-Typen, Funnel-Stufe, Folien-Aufbau, Feed-Ästhetik, der Cockpit-Weg |
| `.claude/skills/reels/SKILL.md` | Reel-Typen, Shotlist, Dreh-Anweisung, Hook-Prozess, Caption-Strategie |
| `.claude/skills/story/SKILL.md` | acht Modi, Slide-Aufbau, Käufertypen, CTA-Pflicht |
| `.claude/skills/caption/SKILL.md` | Captions nach Patricias exakten Vorgaben |
| `.claude/skills/visuals/SKILL.md` | Design-Bauplan, keine KI-Bilder |

**Die Wissensdateien — vollständig, jedes Mal:**

| Datei | Wofür |
|---|---|
| `context/patricia-vollprofil.md` | Stimme, Story, Werte — Single Source of Truth |
| `context/brand-voice.md` | Tonalität und Verbote |
| `context/content-formel-5-typen.md` | **die fünf Beitragstypen und der Wochen-Mix** |
| `context/job-saeulen.md` | Autorität · Story · Reichweite · Verkauf |
| `context/caption-formeln.md` | die fünf Caption-Strukturen, CTAs, Hashtags |
| `context/kern-painpoint.md` | Kernschmerz, drei Bedingungen, Übersetzungstabelle |
| `context/ki-phrasen-blackliste.md` | Floskel-Filter — **gewinnt bei Konflikt immer** |
| `context/patricia-expertise.md` | **die einzige Quelle für Zahlen** |
| `context/patricia-freebies.md` | was es zu verschenken gibt |
| `context/manychat-keywords.md` | welches Keyword wohin führt |
| `context/active-funnels.json` | was gerade läuft |
| `context/karussell-framework.md` | Folien-Struktur, Feed-Aesthetic |
| `context/reels-framework.md` | Viral-Mechanik, 3-Sekunden-Regel, Hashtags |
| `context/story-framework.md` | Story-Wissen, Visual-Pipeline |
| `context/content-radar-juni-2026.md` | was messbar funktioniert hat |
| `context/reichweiten-formel-mama-identity.md` | Reichweite über Mama-Identität |
| `.claude/skills/content/wissen/*.md` | **Sandra, ihre Gedanken und Wörter, die fünf Säulen, Hook-Muster, schon verwendete Hooks** (TEIL 0) |

**Sobald Video im Spiel ist, zusätzlich:** `context/sprechreels-drehanleitung.md` ·
`context/videoschnitt-regeln.md` · `context/videoschnitt-animationen.md` ·
`.claude/skills/videoschnitt/SKILL.md` · `.claude/skills/handy/SKILL.md`

**Bei doTERRA zusätzlich:** `context/doterra/patricia-wendepunkt-story.md` ·
`outputs/zielgruppen-research/doterra-2026-04-22.md`

**Dann gibst du das aus — eine Zeile je gelesener Datei:**

| Datei | Eine konkrete Regel daraus, wörtlich |
|---|---|
| `hooks/SKILL.md` | … |
| `karussell/SKILL.md` | … |
| `reels/SKILL.md` | … |
| `story/SKILL.md` | … |
| `caption/SKILL.md` | … |
| `visuals/SKILL.md` | … |
| `content-formel-5-typen.md` | … |
| `job-saeulen.md` | … |
| `caption-formeln.md` | … |
| `kern-painpoint.md` | … |
| `ki-phrasen-blackliste.md` | … |

Die Zeile muss **so in der Datei stehen**. Aus dem Gedächtnis zitieren gilt nicht. Kommt
sie dort nicht vor, war die Datei nicht offen — dann fängst du nochmal an.

> **Warum das hier steht:** Am 14.09.2026 ist eine komplette Wochenplanung im Müll
> gelandet. Fünf Beiträge, vier davon ohne einen einzigen konkreten Schritt, Captions
> achtmal zu lang, Keyword-Regel ignoriert, fünf Tage derselbe Typ. **Alles, was gefehlt
> hat, stand in diesen Dateien.** Die Anweisung „lies sie" stand auch schon da — sie
> liess sich nur stillschweigend überspringen. Ein Verweis wird übersprungen, ein
> Protokoll nicht.
>
> Und: **Dauer und Token spielen keine Rolle.** Patricia am 14.09.: *„mir ist furzegal
> wie lange die Contenterstellung braucht und was es an Tokens kostet. Es muss aber
> einfach alles rein."*

---

### SCHRITT 2 · Planung lesen

Briefing aus TEIL 1 füllen. Ausgabe: **eine Zeile je Profil** — zum Beispiel
„KW38 Mentoring: Launch-Woche Produkt-Ideen-Finder, Fokus X, Keyword STANDBEIN,
Quelle: Monatsplan September, weil die Notion-Wochenplanung leer ist."

**Steht nirgends ein Fokus, erfindest du keinen.**

---

### SCHRITT 3 · 🛑 Marktcheck

Pro Profil alle vier Dimensionen, mit **echtem Zitat und Quelle**.

| Dimension | Wo du suchst |
|---|---|
| **Pain** | Reddit DACH (r/Selbststaendig, r/Elternschaft, r/Mommit, r/perimenopause), Facebook-Gruppen, Kommentare unter Reels der Nische, DMs der letzten sieben Tage |
| **Wunsch** | Pinterest, Google Trends DACH, Captions der Top-Accounts |
| **Ziel** | LinkedIn Schweiz, Podcast-Themen der letzten 30 Tage, TikTok-Hashtags |
| **Herausforderung** | was in den Foren immer wieder scheitert, Einwände in Kommentaren |

Je Profil: 3–5 Pains · 3 Wünsche · 3 Ziele · 3 Herausforderungen. Pains markieren als
**chronisch** oder **akut**. Dann die Brücke zum Wochenfokus schlagen.

Frische Konkurrenz-Daten (`outputs/apify-runs/competitors-*.json`, jünger als 36 h)
dazunehmen, sonst Websuche.

🎯 **Hauptreferenz ist Julia Müller (@juliamueller._, `referenz: "haupt"` in der Watchlist).**
Patricia, 17.10.2026: *„unbedingt als referenz für zielgruppenrecherche und marktrecherche
… finde das fast am stärksten“*. Gleiche Zielgruppe (Networkerinnen), gleiche Gegner
(Namensliste, Upline-Methoden, Tagebuch-Storys). **Zuerst ihre Beiträge** der letzten Wochen
nach Aufrufen und Kommentaren gegen ihren eigenen Median sortieren (Titelbild-Hook über
`https://www.instagram.com/p/<code>/media/?size=l`, die Scrape-Bildlinks verfallen), dann
die anderen Nischen-Konten. Wird ein Beitrag von ihr nachgebaut: **Inhalt übernehmen, Wortlaut
nie** (Patricia, 17.10.), Firmenliste immer mit doTERRA, Kundschaft der Networkerinnen nie
„Kundinnen“, ihre Zahlen nicht übernehmen. Vorlage: `outputs/content/KW43/julia-nachbau.md`
+ `scripts/content/kw43-brolls.py`.

🚨 **Die wöchentlichen `outputs/marktrecherche/KW*-*.md` sind kein Beleg.** Alle 46 Läufe
bis KW40 melden „Reddit-Posts gescannt: 0“ — die Painpoints darin hat die KI aus
„generischen Patterns“ geschrieben. Als Quelle zählen nur echte Zitate mit Fundort und die
gemessenen Zahlen aus `…-hook-markt-analyse.md` (gefunden 04.10.2026).

Ablage: `outputs/content/KW[NN]/markt.md` — beim zweiten Lauf **überschreiben**.

🛑 Zeigen, auf „weiter" warten. *(Automatik-Lauf: durchlaufen.)*

---

### SCHRITT 4 · 🛑 Hooks

**Zuerst die Hook-Maschine** (TEIL 0 in `hooks/SKILL.md`, seit 04.10.2026):

```bash
python scripts/hooks/markt-analyse.py && python scripts/hooks/verkaufsdaten.py
python scripts/hooks/beispiele.py --profil mentoring --thema "<Wochenfokus>" --ziel beides
python scripts/hooks/beispiele.py --profil doterra --thema "<Wochenfokus>" --ziel reichweite
```

Dazu `context/hook-datensaetze.md` lesen (Psychologie · Positionierung · Angebote). Die Zeilen „Was gerade trägt“ aus dem Paket gelten für die ganze Woche. Stand 04.10.:
Identität und Stufe 1 tragen, Listen und Beweis-Einstiege nicht — **auch bei den drei
Lead-Posts** beginnt der Hook mit ihrem Satz, nicht mit dem Angebot.

**14 Hooks pro Profil**, gebaut mit dem Katalog aus `hooks/SKILL.md`, jeder durch den
letzten Check aus TEIL 3. **Jeder Hook nennt sein Vorbild aus dem Paket.**

| # | Profil | PIE | Hook | Formel | Angle | Stufe | Vorbild (Faktor) | Marktbezug |
|---|---|---|---|---|---|---|---|---|

Hooks aus dem Konkurrenz-Scrape dürfen übernommen werden, wenn sie zur Marke passen —
durch Blackliste und letzten Check, **Szene und Zahlen aus Patricias Leben**, Herkunft
in der Tabelle vermerkt.

🛑 Zeigen, auf „weiter" warten. Korrekturen ändern **nur die genannten** Hooks.

---

### SCHRITT 5 · Typ-Zettel — der Typ kommt vor dem Hook

> 🚨 **Zuerst steht fest, welcher Typ an welchem Tag läuft. Dann suchst du den Hook
> dazu.** Am 14.09. lief es andersrum: fünf gute Hooks gesucht, und dabei fünfmal
> denselben Typ gebaut.

**Die fünf Typen** (aus `content-formel-5-typen.md`):

| Typ | Funktion | Was er verlangt |
|---|---|---|
| **1 Lifestyle / Freiheit** | Reichweite, Identifikation | Bild oder Video von dir in einer freien Situation · Hook identifikationsstiftend · Caption 3–5 verbundene Sätze · offene Frage · **kein Produkt-CTA** |
| **2 Tutorial-Karussell** | Expertise, Saves, Keyword-Kommentare | **Cover sagt, was sie danach kann** — keine Meinung · Folien 2–7 **nummerierte Schritte mit echtem Praxiswert** · letzte Folie **ein** Keyword · **Caption höchstens zwei Sätze**, direkt auf den CTA |
| **3 Reel-CTA** | Traffic, Engagement | 15–30 Sek, du sprichst direkt in die Kamera · Caption 1–3 Sätze + ein Keyword |
| **4 Meinung / Provokation** | Reichweite durch Diskussion | Hook meinungsstark · Caption persönlich, Ich-Perspektive, ohne Entschuldigung · **kein direkter CTA** |
| **5 Social Proof / Ergebnis** | Glaubwürdigkeit, Conversion | Vorher/Nachher oder eigenes Ergebnis · Caption „Problem → Methode → Ergebnis" · doTERRA nur im „bei mir war"-Rahmen |

**Die vier Job-Säulen** (aus `job-saeulen.md`) laufen parallel dazu — jeder Beitrag ist
ein Thema × ein Job:

| Job | Was der Beitrag bewirken soll |
|---|---|
| **A Autorität** | sie soll denken: die weiss, wovon sie redet |
| **B Story** | sie soll sich wiedererkennen |
| **C Reichweite** | sie soll es weiterschicken |
| **D Verkauf** | sie soll den nächsten Schritt gehen |

**Regeln für den Zettel:**

- **Nie zwei Tage hintereinander derselbe Typ.**
- Über die Woche **mindestens ein** Reichweiten-Typ (1 oder 4) neben den Mehrwert-Typen.
- **Mindestens drei Keyword-Beiträge** pro Woche und Profil (Patricia, 14.09.2026).
- PIE im Fünfer-Pick: mindestens 1× P, 1× I, 1× E — geprüft an den **A-Varianten**.
- Job-Mix schief: **sagen, nicht still überschreiben.**

**Ausgabe:**

| Tag | Typ | Job | Hook A | Hook B | Angle A / B | CTA | Keyword |
|---|---|---|---|---|---|---|---|

---

### SCHRITT 6 · 🛑 Bauen

#### Karussell

Cover · 6–9 Inhalts-Folien · CTA-Folie · **maximal 10 Folien** (Blotato-Grenze).

Vier Typen: Listicle · Storytelling · Edukativ · Kontroverser Take. **Beim kontroversen
Take ist die Nuancierungs-Folie Pflicht.** Funnel-Stufe TOF/MOF/BOF festlegen.

**Das Cover stoppt oder nicht:** wenig Text, grosse fette Schrift, Schlüsselbegriff in
Grossbuchstaben, lesbar im Mini-Format, Marken-Look. Das Cover trägt den **ganzen Hook**,
nicht nur ein Schlagwort. **Drei Cover-Varianten** in verschiedenen Stilen, eine markiert als
verwendet, mit einem Satz warum.

#### Sieben Baupläne (seit 13.10.2026, aus dem Karussell-Texter)

6 bis 10 Folien, so lang, wie der Gedanke trägt. Eine Folie, die nur da ist, um eine Zahl zu
erreichen, kostet Wischer.

| Bauplan | Passt für | Aufbau |
|---|---|---|
| **Gedankengang mit Reibung** | Plan B, Eigenverantwortung, Partner | Cover mit Gegner → Folie 2 holt sie in einer Szene ab → ihre Fehlannahme → **in der Mitte die Wendung** → 2–3 Folien, was das konkret heisst → Hoffnungssatz → Aufruf |
| **Selbsttest** | Hobby oder Business, Profil-Check, Aufhören | Cover verspricht ehrliche Standortbestimmung → warum es unbequem ist → je Folie eine Frage mit einem Satz dahinter → Auswertung als Spiegel, ohne Punkte → nächster Schritt |
| **Liste mit Haltung** | Profil, Bio, „Dinge, die ich nicht mehr mache“ | je Folie ein Punkt **mit Begründung und Gegenmittel**, der unbequemste zuletzt |
| **Vorher/Nachher** | Bio, Namenszeile, Caption-Einstieg | typischer Fehler, ironisch → Vorher (erfunden, typisch, nie eine echte Person) → warum es nicht wirkt → Nachher mit Erklärung → Formel zum Selbermachen |
| **Geständnis** | Mama-Alltag, Plan B | Ich-Satz, der etwas zugibt → Szene → Wendepunkt → Lehre → erst am Ende die Übertragung auf sie. Nur Eckdaten, sonst Platzhalter |
| **Zahlen mit Haltung** | Rentenlücke, Teilzeit, Branchenrealität | stärkste Zahl mit Haltung → je Folie höchstens eine Zahl mit „Und was heisst das für dich?“ → Haltung statt Beratung, Hinweis auf Fachstelle, Quelle in der Caption |
| **Kundinnen-Frage** | Verkaufen, Likes ohne Käufe | Cover = die Frage als Zitat → ehrliche, etwas unbequeme Antwort über mehrere Folien. Als typische Frage kennzeichnen, ausser Patricia liefert ein echtes Zitat |

Dazu der **Mehrwert-Bauplan** unten (Beweis → Speichern-Folie → Vorher-Nachher-Paare → Keyword).

**Spannung über die Folien:** Folie 2 bestätigt das Cover **sofort** — kommt dort eine
Einleitung, ist sie weg. Nicht jede Folie mit „Aber …“ beenden, sonst merkt man die Masche:
mal eine Frage, mal eine Behauptung, mal ein halber Gedanke, der auf der nächsten aufgeht.
**Die vorletzte Folie ist der Satz, den sie einer Freundin schickt**, er muss allein stehen.
Pro Folie höchstens rund 35 Wörter, ganze Sätze statt Fragmente, kein Fazit, das alles
wiederholt. Jedes Karussell hat mindestens einen Satz, der Hoffnung macht.

**Caption-Länge: was Sinn ergibt** (Patricia, 13.10.). Gedankengang und Geständnis dürfen
lang werden, weil die Caption dort vertieft, was die Folien nur andeuten. Anleitung und
Liste bleiben kurz, weil der Wert auf den Folien steht.

#### Der Bauplan, der nachweislich Mehrwert liefert

Aus dem Konkurrenz-Scrape vom 14.09.2026 — ein Karussell mit 19 Kommentaren bei einer
Mentorin mit 23'500 Followern, und Patricias Urteil dazu: *„sie macht es so simpel, aber
SO viel Mehrwert ist in ihren Beiträgen."*

| Folie | Aufgabe |
|---|---|
| **1** | Ergebnis-Behauptung **plus Beweis** — ein echter Screenshot mit Zahlen, kein Text allein |
| **2** | die Behauptung in einem Satz |
| **3** | **ein Bild, das jeder versteht** — die Zeitung mit der schlechten Überschrift, der Zettel am schwarzen Brett |
| **4** | **eine eigene Folie nur fürs Speichern**, mit Lesezeichen-Symbol und der Begründung: „weil ab hier X kommt" |
| **5 bis 9** | der Wert als **Vorher-Nachher-Paare, nach Bereich sortiert** — jede findet ihre eigene Zeile |
| **10** | Keyword |

🚨 **Das Entscheidende ist der letzte Punkt: Das Keyword verspricht MEHR VOM GLEICHEN.**
Im Karussell stehen acht Paare, hinter dem Keyword liegen fünfzig. Der Beitrag **beweist**
damit den Wert des Freebies, statt ihn zu behaupten.

**Der Fehler vom 14.09. war genau hier:** fünf Schritte im Karussell, und dahinter ein
„Werkzeug". Anderer Gegenstand, kein Beweis. Wer die fünf Schritte gelesen hat, weiss
nicht, was sie hinter dem Keyword erwartet.

**Vorher-Nachher-Paare schlagen Erklärungen.** Man muss nichts verstehen, man sieht den
Unterschied. Und sortiert nach Bereich erkennt jede sofort ihre eigene Situation.

#### Reel

**Talking-Head:** sekundengenauer Sprechtext · unter 30 Sekunden · Setting candid, im
Alltag, nie posiert.

**B-Roll (Standard, seit 11.10.2026 animiert):** ein Clip aus Patricias Alltag, der Hook
steht **ganz und ab Bild null** im Bild, 6 bis 10 Sekunden. Optik wie das Reel „3 Wege“:
Serifenschrift, weicher Schleier, orange Wendung, langsame Zoomfahrt, nie in der Bildmitte
(Gesicht). Darauf Animation: bei langen Hooks Serif, Marker-Balken nur bei kurzer Wendung, der
Aufruf als Chip mit Pop in den letzten 2,5 Sekunden, bei Verlosungen Schritte nacheinander.
Gebaut über `broll-bauen.py` + `textebene.py`, Vorlage `scripts/content/kw42-brolls.py`.
🚨 **Das Video muss den Text nicht illustrieren** — nicht stundenlang nach passendem
Material suchen. Eine Clip-Idee, die zum Text zwinkert (Wäscheberg, Auto vor der Schule,
Laptop am Esstisch), ist schön, aber kein Muss.

**Talking-Head bekommt mindestens zwei gestaltete Elemente:** Kelsie-Textebene
(zwei Zeilen auf Stoss, klein oben, gross unten, grosses Wort hinter Patricia) ·
wortgenaue Untertitel mit orangem aktivem Wort · Auto-Zoom · eingefügte Bilder ·
Visualisierungen. Gesprochenes Hochdeutsch, so geschrieben, wie man spricht, 25 bis 45
Sekunden: Hook in den ersten zwei Sekunden → Problem → Wendung → ein konkreter Schritt →
ein Satz, der Mut macht → Abschluss.

**Reel-Skript (Ausgabe, auch beim Einzelauftrag „Reel zu X“):**

```
## Reel: [Arbeitstitel]
Säule: … | Leserin: Frustrierte / Suchende / Entschlossene | Format: B-Roll / Sprechreel | Länge: ca. … Sek.

Hook-Varianten
1. [Hook] (Mechanik: Gegner / Geständnis / Zitat / Erwartung drehen)
2. …
3. …
Empfehlung: Variante X, weil … (ein Satz)

Clip-Idee: was gefilmt wird, Winkel, Stimmung, Ton (zwei bis vier Sätze, keine Kindergesichter)

Ablauf
0–2 s | Bild: … | Text: [Hook]
2–6 s | Bild: … | Text: …
(bei Sprechreels zusätzlich: Gesprochen: …)

Caption … · Aufruf: …
Prüfen: Stimmt das so für dich? (nur wenn eine Ich-Szene drin ist)
```

**Animationen immer mit vier Angaben:** Aussehen · Bewegung · **Stelle (den Satz nennen,
nie die Sekunde)** · Sound.

**Erst Konzept, dann rendern:** `textebene.py --konzept` → prüfen → `--rendern`.

> 🚨 **Das Hook-Fenster wird in Einzelbildern geprüft, alle 0,3 Sekunden über die ersten
> drei Sekunden.** Nicht mit den fünf Bildern, die das Skript selbst aussucht — die
> zeigen genau die Momente, in denen alles fertig aussieht. Am 14.09. sind so drei Reels
> durchgegangen, in denen in Sekunde eins nur ein Satzfragment stand.

#### Caption — die fünf Strukturen

Die Caption **ergänzt** den Beitrag. Den Hook nicht wiederholen.

| Formel | Aufbau |
|---|---|
| **1 Behauptung + Beweis** | starke Aussage → „die meisten denken, das geht nicht" → Kontext → drei Punkte → „das ist kein Zufall, das ist System" → CTA |
| **2 Schritt für Schritt** | „So [Ergebnis] in [Zeitraum]" → Schritt 1–5 → „Das ist alles" → CTA |
| **3 Kontrast** | „Vor [Zeitraum]: drei Schmerzpunkte" → „Heute: drei Ergebnisse" → „Nicht mein Tag hat sich geändert, mein System" → CTA |
| **4 Storytelling kurz** | Szene (max. 2 Sätze) → Wendepunkt → Erkenntnis → Überleitung → CTA |
| **5 Listicle** | „[Zahl] Dinge, die ich früher gerne gewusst hätte" → 1–5 mit kurzer Erklärung → „Nummer X hat am meisten verändert" → CTA |

**Immer dabei:** Zeitanker als Einstieg · eine konkrete Zahl in den ersten zwei Sätzen,
**nur aus `patricia-expertise.md`** · ganze Sätze · echte Umlaute · Schweizer ss ·
höchstens fünf Hashtags mit `#mamabusiness` als Anker · **jede Caption ein anderer
Einstieg als die letzte**.

**Die Länge richtet sich nach dem Typ.** Typ 2: zwei Sätze. Typ 1: drei bis fünf.
Typ 4: so lang wie die Haltung braucht.

#### CTA

> **Jeder Beitrag verkauft — entweder Vertrauen oder aktiv.** Es gibt keinen Beitrag
> ohne Verkaufsabsicht (Patricia, 14.09.2026).

| Art | Was der Beitrag tut | CTA |
|---|---|---|
| **Vertrauen** | bezieht Stellung, erzählt eine echte Szene, gibt etwas mit | Teilen · Speichern · eine Frage, auf die man antworten will |
| **aktiv** | benennt den nächsten Schritt und macht ihn leicht | ein bestehendes Keyword |

**Vertrauens-CTA so schreiben, dass er null Denkarbeit kostet** (aus den Kursunterlagen
„Content Shortcut“, 13.10.2026):
- **Teilen an eine bestimmte Person:** „Schick das der Freundin, die auch jeden Abend um
  elf noch Firmenposts kopiert.“ Nicht „Teil den Beitrag“.
- **Kommentar als Wahl statt als Aufsatz:** „Eher Team Firmenvorlage oder Team eigene
  Worte?“ · „1 oder 2?“. Eine offene Frage wie „Was denkst du darüber?“ verlangt einen
  Text, und den schreibt öffentlich niemand.
- **Speichern mit Grund:** „Speicher dir das für den Abend, an dem du wieder vor dem leeren
  Feld sitzt.“

**Keyword-Regeln:** Grossbuchstaben, fett · **genau eins pro Beitrag** · eingebettet
(„Kommentier **STANDBEIN** und ich schick dir …") · nie eins erfinden · rotieren.

> 🚨 **Das Keyword steht in der ERSTEN Zeile der Caption, nicht am Schluss.**
>
> Instagram zeigt zwei Zeilen, dann „mehr anzeigen". Wer das Keyword in Absatz fünf
> setzt, erreicht nur die, die aufklappen.
>
> **Beleg aus dem Konkurrenz-Scrape vom 14.09.2026:** Der stärkste Beitrag der Mentorin
> hat **32 Likes und 128 Kommentare** — viermal so viele Kommentare wie Likes. Das
> Keyword steht dort in Zeile eins, direkt gefolgt von dem, was man dafür bekommt.
> Am Schluss steht es nochmal.
>
> **Und der Wert kommt trotzdem:** Sie verschenkt die komplette Methode in der Caption,
> fünf Schritte, nichts zurückgehalten. Das Verschenken frisst den Funnel nicht auf,
> es **beweist** ihn — 128 Leute fragen trotzdem nach dem Guide.
>
> **Aufbau also:** Zeile 1 Keyword plus Versprechen · dann die Methode in nummerierten
> Schritten · dann ein Satz, der zeigt, dass es bei dir funktioniert hat · dann das
> Keyword nochmal mit ⬇️.


| Mentoring | führt zu |
|---|---|
| `STANDBEIN` | Produkt-Ideen-Finder (0€ KI-Tool) |
| `SYSTEM` · `FAHRPLAN` | 0€ Fahrplan |
| `QUIZ` | 0€ Quiz |
| `SICHTBAR` · `ANLEITUNG` | 0€ Starterguide |
| `LEAD` | Lead-Challenge |
| `ECHT1` | Workbook „Von 0 auf echt" |
| `BIO` | Bio-Check |
| `ZEITFENSTER` | Freischaufeln |
| `THEMA` · `PRODUKT` | Minikurse (Mid) |

| doTERRA | führt zu |
|---|---|
| `ENERGIE` | Padlet + Kur-Einstieg |

**Kein Preis und kein Programmname im Feed.**

#### Design

- Cover im **ABAB-Rhythmus**: Vorlage ↔ Foto abwechselnd, Farbe rotieren
- **Kein Voll-Petrol-Cover bei Lead-Posts** mit Keyword-CTA
- Ist Patricia auf dem Foto: Gesicht und Hauptmotiv komplett frei
- **Keine fremden Gesichter im Bild** — Gruppenfotos an Wänden, Kinder, Teamfotos
- **Keine KI-Bilder.** Nur Vorlagen und echte Fotos.

🛑 Zeigen, auf „weiter" warten. Korrekturen ändern nur das Genannte.

---

### 🚨 Genau EIN Aufruf je Beitrag (seit 2026-09-19)

Entweder das **Stichwort** (Lead-Post) oder der **Share** (Reichweiten-Post). Nie
beides, und nie ein zweiter Gesprächs-CTA daneben.

**Warum das keine Geschmacksfrage ist:** Im Lead-Karussell der KW39 stand neben
„Kommentier STANDBEIN" noch „Schreib mir die Nummer in einen zweiten Kommentar" —
und die Caption musste danach einen ganzen Satz darauf verwenden zu erklären, dass
das Stichwort **allein stehen** muss, sonst springt die Automatik nicht an. Das ist
Erklärarbeit genau an der Stelle, an der konvertiert wird.

🚨 **Vor dem Schreiben prüfen, ob das Stichwort überhaupt irgendwohin führt.**
Stand 19.09.2026 haben **8 von 14** Stichwörtern kein Angebot dahinter
(`daten/funnel` im Cockpit): QUIZ · SICHTBAR · STORY · SYSTEM · FAHRPLAN ·
PRODUKT · THEMA · ANLEITUNG. Ein Beitrag mit einem dieser Wörter liefert ein
Freebie aus und danach passiert nichts. **Nur Stichwörter verwenden, hinter denen
ein Angebot steht.**

### 🚨 Jeder fünfte Beitrag ist ein Beweisbeitrag (seit 2026-09-19)

Ein eigener Beitragstyp, kein Nachsatz unter etwas anderem. Er braucht **alle drei**
Teile, sonst ist er keiner:

1. **Ausgangslage** — wo die Frau vorher stand, konkret
2. **Zeitraum** — „nach einer Woche", „nach dem dritten Post"
3. **Eine Zahl** — verkaufte Startersets, Anfragen, Gespräche

Dazu die **Einschränkungen**, unter denen es passiert ist: Kinder, Teilzeit, keine
Assistentin, keine Werbeanzeigen. Genau die machen das Ergebnis für meine
Zielgruppe überhaupt erst kopierbar.

🚨 **Ohne Beleg kein Beweisbeitrag.** Ein Zitat allein („Super Kurs!") ist keiner.
Fehlt Ausgangslage, Zeitraum oder Zahl, wird der Beitrag **nicht gebaut** — und
schon gar nichts dazuerfunden. Dann lieber ein Beitragstyp weniger.

### SCHRITT 7 · 🛑 Der Beitrags-Check

> 🚨 **Als Tabelle ausgeben, ein Beitrag pro Zeile. Nicht im Kopf prüfen.**
> Ein Nein und der Beitrag geht nicht raus.

**Vorher einmal als Sandra durchgehen** (TEIL 0): 23 Uhr, müde, Daumen auf dem Bildschirm.
Gibt es eine Folie oder eine Sekunde, bei der sie weiterwischt, ohne zu lesen? Und ein Satz
zurück: Klingt irgendetwas nach Werbebroschüre statt nach einer Sprachnachricht an eine
Freundin? Dann zuerst das umschreiben, dann die Tabelle.

| Beitrag | gibt ihr mit | berührt es | konkret mitnehmen | Grund zu speichern | Grund zu kommentieren | nur von ihr |
|---|---|---|---|---|---|---|

**Spalte „gibt ihr mit“** = die Tagesfrage: *Inspiration*, *Tipp* oder *Warum mit mir / möglich*. Steht dort nichts Benennbares, fängt der Beitrag bei mir an statt bei ihr, und er wird neu gedacht. Fehlt eins der drei in der ganzen Woche, wird ein Platz getauscht.

**1. Berührt es?** Trifft es ein Gefühl — Sehnsucht, Erleichterung, Wiedererkennen,
„endlich sagt das mal jemand"?

**2. Nimmt sie etwas Konkretes mit?** In diese Zelle gehört **die Sache selbst**, nicht
„ja". Eine Liste, ein Schritt, eine Vorlage, eine Frage zum Durchrechnen. Steht dort
keine benennbare Sache, ist die Antwort Nein. „Du brauchst ein System" ist kein Mehrwert.

**3. Warum sollte sie das speichern oder weiterschicken?** Blosses Wiedererkennen („ja,
kenn ich") reicht nicht. Drei benannte Hacks statt „ein paar Dinge, die bei mir laufen".

**4. Warum sollte sie kommentieren?** Ein Keyword allein ist kein Grund. Es braucht
etwas, worauf man antworten *will* — eine Frage, die sie betrifft, eine Haltung mit
Widerspruchspotenzial, oder eine **nummerierte Auswahl** („welches ist deins, 1 bis 5?").
Eine Zahl zu tippen ist die niedrigste Hürde, die es gibt.

**5. Name abdecken: Wäre das erkennbar von ihr?** (seit 30.09.2026) Könnte eine andere
freundliche Mentorin genau diesen Beitrag gepostet haben, ist die Antwort Nein. In die
Zelle gehört **die Stelle selbst**, die nur von Patricia sein kann: ein echtes Detail aus
ihrem Alltag, ein selbstironischer Satz, ein Seitenhieb oder eine Haltung, bei der eine
Leserin auch „nichts für mich“ sagen darf. Zeigen, nicht behaupten: „Folg mir, wenn du
Klartext willst“ zählt nicht. Nichts erfinden, sondern nur Szenen und Sätze, die belegt
sind. Regeln und Beispiele: Block „Persönlichkeit zeigen, nicht behaupten“ in
`context/brand-voice.md`.
*Anlass: Die 12 Posts vom 22. bis 30.09. hatten zusammen 1× gespeichert, 0× geteilt und
0 Kommentare. In keinem steckte Humor oder eine Kante. Am stärksten liefen die zwei, die
klar von ihr waren (Thermomix 435 und die Liste für ihren Mann 373).*

**Zusätzlich über die Woche:** keine Satzbausteine doppelt (derselbe Satz oder
derselbe CTA-Wortlaut in zwei Captions derselben Woche ist Skill-Handschrift) · mindestens ein emotionaler Ich-Story-Beitrag · keine
Themen-Wiederholung aus den letzten vier Wochen · vor einem Verkaufs-Block genug
Mehrwert-Runway.

---

### SCHRITT 8 · Story-Bogen

**Die Storys hängen an den Beiträgen.** Feed-Post abends → die Story am nächsten Morgen
greift ihn auf, erzählt die Szene dahinter oder beantwortet, was in den Kommentaren kam.
**Sie wiederholt ihn nie.**

Erst die Tabelle:

| Tag | knüpft an | Säule | Käufertyp | Idee in einem Satz |
|---|---|---|---|---|

**Dann jeden Tag ausbauen** — drei bis fünf Folien mit **ausformuliertem Text**, keine
Platzhalter in eckigen Klammern. Patricia tauscht das Bild und schärft eine Zeile nach.

Folienfolge: Szene → Reibung → Wendung → Punkt → CTA. **Der Sticker braucht eine echte
Wahl** — eine Umfrage mit zwei Möglichkeiten oder eine Frage, auf die man tippen will.
„Was meinst du?" ist keine.

**Pflicht über die Woche:** alle vier Käufertypen (Rot/Gelb/Grün/Blau) kommen vor, jede
Sequenz hat einen CTA-Link aus `active-funnels.json`.

**Wenn eine Sequenz ein Angebot direkt vorstellt** (aus den Kursunterlagen „Content
Shortcut“, 13.10.2026), dann in dieser Reihenfolge:
1. **Einstieg:** eine echte Kundenstimme (`context/kundinnen-geschichten.md`, nur mit
   Freigabe) **oder** ein Blick in die Werkstatt, also woran du gerade baust.
2. **Für wen:** zwei, drei ganz konkrete Situationen, in denen sie sich erkennt.
3. **Wie es danach ist:** der Zustand nach dem Angebot, in ihrem Alltag erzählt.
4. **Was drin ist:** darf beim gefühlsorientierten Käufertyp wegfallen.
5. **Aufruf:** „Reagier mit ❤️, dann schick ich dir alles“ oder Frage-Sticker.
6. *(optional)* Beweis von jemandem, der schon dabei ist. Gibt es keinen echten, fällt die
   Folie weg.

**Mini-Sprechstunde als Beziehungs- und Testinstrument:** „Ich schau mir diese Woche
**drei** Bios an, tipp auf den Sticker.“ Daraus kommen Gespräche, echte Sätze der
Zielgruppe und der Beleg, ob ein Thema als Angebot trägt, bevor es gebaut wird.

**Story-Einstiege, wenn nichts passiert ist:** ein Rat, den sie immer wieder hört · etwas,
bei dem du deine Meinung geändert hast · etwas, das nicht funktioniert hat · was du diese
Woche geschafft hast. Immer nur Echtes, nie eine Szene erfinden.

---

### SCHRITT 9 · Rohmaterial holen und Reels bauen

**Nachsehen, nicht fragen.**

```bash
python scripts/handy/hol-content.py
python scripts/handy/hol-content.py --album Sprechreels --ziel-video video/input
python scripts/handy/hol-content.py --album Reel-Videos --ziel-video video/reel-videos
```

Auf dem Handy wird **nie** gelöscht.

> 🚨 **Vorschaubilder wirklich anschauen** (`context/content-assets/vorschau/`), bevor du
> sagst, was auf einem Clip drauf ist. Am 14.09. wäre so fast eine Kuschelszene mit einem
> Kind unter dem Text „Runterkommen ist nicht Netflix" gelandet.

**Liegt ein Wissens-Dump in `DCIM/Sprechreels`** (10–20 Minuten frei gesprochen), fisch
die stärksten Stellen heraus — daraus werden mehrere Reels. Die stärkste Quelle im ganzen
Ablauf.

**Schnitt:** `transkribieren.py` → Schnittliste nach `videoschnitt-regeln.md` →
`schnitt.py` → `textebene.py --konzept` → prüfen → `--rendern`.

**Hat Patricia denselben Text in zwei Positionen gefilmt**, springt der Schnitt zwischen
ihnen. Die Regel „letzter vollständiger Take gewinnt" wird dafür bewusst ausgehebelt und
der Grund in die Schnittliste geschrieben.

**Fehlt Material:** nicht halb bauen, keinen Ersatz suchen. Telegram an Patricia mit
fertigem Sprechtext Wort für Wort, Setting, Dauer und Ablage-Ordner. **Der Rest der Woche
wird trotzdem gebaut.**

---

### SCHRITT 10 · Ablegen

**Dateien:** `outputs/content/KW[NN]/` — `markt.md` · `hooks.md` · `auswahl.md` ·
`beitraege.md` · `storys.md`. Immer dieselben Namen, ein zweiter Lauf **überschreibt**.
Frontmatter `tags: [content]`.

**Ins Cockpit** (`https://claude.ai/code/artifact/eeee48d5-3e50-4cff-8047-1ec5eccbb074`)
per `Artifact write_db` — alle drei Formate, jedes **mit `datum`**, alle `textfrei: false`:

| Sammlung | Felder |
|---|---|
| `karussells` | `name` (`A · ` / `B · ` voran) · `datum` · `brand` · `typ` · `funnel` · `caption` · `slides[{layout,headline,body}]` · `textfrei` |
| `reels` | `name` · `datum` · `hook` · `unter` · `skript` · `caption` · `videourl` · `coverfarbe` · `textfrei` |
| `storys` | `name` · `datum` · `brand` · `frames[{id,layout,text,cta,optA,optB}]` · `textfrei` |

**Ohne `datum` sortiert sich nichts in den Wochentag ein.**

🚨 **`typ` und `funnel` gegen die erlaubten Werte prüfen, bevor du schreibst.**
Das Cockpit kennt genau diese und sonst nichts:

| Feld | erlaubt | häufiger Fehler |
|---|---|---|
| `typ` | `listicle` · `story` · `edukativ` · `kontrovers` | `storytelling` (die Überschrift statt des Schlüssels) · `kontrast` (ist eine Bauweise, kein Typ) |
| `funnel` | `TOF` · `MOF` · `BOF` | alles auf `MOF`, weil nicht entschieden wurde |

Ein anderer Wert fällt **nicht** auf — das Auswahlfeld im Cockpit zeigt dann den
falschen Typ, und der Hinweistext darunter bleibt leer. Am 19.09.2026 waren drei
von zwölf Karussells so kaputt. Also: nach dem Schreiben die Werte nochmal
auflisten und mit der Tabelle oben vergleichen.

🚨 **Nicht die ganze Woche auf `MOF`.** Die Funnel-Stufe ist eine Entscheidung je
Beitrag. Stehen alle gleich, wurde nicht entschieden — die Reichweiten-Beiträge
gehören auf `TOF`.

**Fertige Reel-Videos** per `Artifact upload_asset` anhängen (unter 20 MiB) und die
zurückgegebene Adresse **unverändert** als `videourl` eintragen. Kein Telegram-Versand
für Reels — sie holt sie dort, wo sie prüft.

**In den Bild-Editor** (`https://claude.ai/code/artifact/21e66e0e-2576-41db-8c8d-f14d7079a1e0`),
Sammlung `daten`:

- **`woche`** — `kw`, `zeitraum`, `stand`, `quelle`, je Profil `fokus` (ein Satz in
  Patricias Sprache), `monatsthema`, `angebot`, `lage`
- **`beitraege`** — je Profil `gepostet` (aus `scripts/instagram-insights/holen.py`) und
  `geplant` (aus der Cockpit-Datenbank)
- **`entwuerfe`** — alle Karussells, Story-Bögen und Reel-Cover **beider Varianten**,
  je Folie `text` (grosser Balken) und `unter` (zweiter, kleinerer Balken)

**Auch neu bauen:** `python scripts/cockpit/wissen-bauen.py outputs/cockpit/abgleich`,
Ergebnis als `daten/wissen-voll` in **beide** Artifacts.

---

### SCHRITT 11 · Telegram

Über den Cockpit-Bot (`TELEGRAM_COCKPIT_BOT_TOKEN` in `.env`):

```
Freitag — die Woche steht zur Auswahl

Pro Tag zwei Varianten: 6 Karussells · 4 Reels · 5 Storys in der Wochen-Vorschau.
Du gibst frei, was passt — der Rest bleibt liegen.

Fehlt noch: [nur wenn wirklich etwas fehlt]
```

---

### SCHRITT 12 · Freigabe und Auslieferung

**Der Freigabe-Knopf in der Wochen-Vorschau IST das Go.** Kein Nachfragen im Chat.

`freigaben-einplanen-2000` zieht alle zwei Stunden alles auf `status: "wartet"`, prüft
trocken und plant über `scripts/cockpit/freigabe-zu-blotato.mjs` ein.

- **Immer zuerst `--trocken`.**
- **Storys nie einplanen** — die postet Patricia selbst vom Handy.
- Gibt sie **beide** Varianten eines Tages frei, gehen beide raus — die zweite zwei
  Stunden später, und ihr sagen.

---

## TEIL 6: REGELN UND VERBOTE

**Sprache**

- **Keine Stakkato-Sätze.** Verbunden schreiben, wie am Küchentisch.
- **Echte Umlaute, Schweizer ss statt ß.**
- **Freundin-Voice:** Würdest du das einer Mama-Freundin am Telefon so sagen?
- **Kein „Stell dir vor"** — direkt in die Szene einsteigen.
- **Keine abstrakten Verben ohne Handelnden** („es trägt noch nicht").
- **Kein Rätsel statt Aussage.** In drei Sekunden braucht es Klarheit.
- **Frage und Antwort direkt hintereinander** bringen Tempo: „Bringt mir das was? Ja. Aber
  nur, wenn …“ (aus den Kursunterlagen „Content Shortcut“).
- **Eigene Meinung gegen das Übliche:** „Alle sagen X. Ich sehe das anders, weil …“ —
  mit einem echten Grund aus ihrem Weg.
- **Offene Schleife nur mit echtem Erlebnis:** am Anfang andeuten, was gleich kommt, und
  es dann auch auflösen.

**Aus den Kursunterlagen bewusst NICHT übernommen** (13.10.2026, widerspricht den Regeln
hier): Powerwörter-Listen (ultimativ, magisch, Geheimnis, unglaublich — Blackliste) ·
Nutzen-Hooks mit der Lösung drin („Wie du X ohne Y …“) · Hooks mit „Studien zeigen“ oder
„Experten sind sich einig“ · gespielte Füllwörter, Satzabbrüche und englische Floskeln
(„ähm“, „Been there“) · Kundengeschichten mit Name und Umsatz als Muster, wenn es keine
echte gibt · Formulierungen wie „Investition“ statt Preis.

**Wahrheit**

- **Keine erfundenen Zahlen.** Gar keine. Nur aus `patricia-expertise.md`.
- **Keine erfundenen Anekdoten.** Keine DM, keine Kundin, kein Gespräch, das es nicht
  gab. Patricia am 14.09. zu einem erfundenen Posteingang: **„lüge. kenn ich so nicht."**
  Im Zweifel zweite Person statt erfundener Dritter: „Du kennst den Moment, wo …"
- **Keine fremden Zahlen, keine fremden Geschichten.** Von einem Konkurrenz-Beitrag darf
  die **Struktur** übernommen werden — Szene und Zahlen kommen aus Patricias Leben.

**Marke**

- Petrol · Dunkelblau · Creme · Orange. **Kein Gelb, kein Gold, kein Pink.**
- Philosopher + Source Sans 3.
- **Keine fremden Mentorinnen namentlich** in irgendetwas, das Patricia teilen könnte.
- **Keine Heilversprechen** bei doTERRA, alles im „bei mir war"-Rahmen.
- **Keine Netzwerkaufbau-Tipps** („besser recruiten") — es geht um das eigene Thema.

**Was du nie machst**

- Ohne Leseprotokoll schreiben
- Einen abgenommenen Hook still umschreiben
- Ein Video abnehmen, ohne das Hook-Fenster in Einzelbildern geprüft zu haben
- Ein neues Keyword erfinden, oder zwei in einen Beitrag setzen
- Einen Preis oder Programmnamen in den Feed schreiben
- Etwas einplanen, das nicht freigegeben ist
- Auf dem Handy löschen
- Eine zweite Datei danebenlegen, statt die bestehende zu ändern

---

## TEIL 7: OUTPUT-FORMAT

```markdown
## DI 15.9. · Karussell · Typ 2 (Tutorial) · Job A+D · Variante A
**Hook:** [wortgleich aus der Auswahl]
**Angle:** Beweis · **PIE:** E · **Stufe:** 3 · **Keyword:** STANDBEIN

### Folien
| # | Headline | Body |
|---|---|---|
| 1 | [was sie danach kann] | |
| 2 | Schritt 1: … | … |
| … | | |
| 9 | Kommentier STANDBEIN | [was sie dafür bekommt] |

### Caption
[zwei Sätze, direkt auf den CTA]

#mamabusiness #… (höchstens fünf)

### Design
Cover: [Vorlage oder Foto], Farbe [X] · ABAB-Check gegen Mo und Mi: ✅
```

Dazu je Lauf: Leseprotokoll · Hook-Tabelle · Typ-Zettel · Beitrags-Check-Tabelle.

---

## TEIL 8: EIN BEISPIEL

**Briefing:** KW38 Mentoring, Launch-Woche Produkt-Ideen-Finder, Keyword `STANDBEIN`,
Fokus „dein Thema hast du längst, es kommt dir nur zu normal vor".

**Typ-Zettel:** Mo Typ 1 · Di Typ 2 · Mi Typ 4 · Do Typ 3 · Fr Typ 2.
Kein Typ zweimal hintereinander, drei Keyword-Beiträge (Di, Do, Fr).

**Der Dienstag, Typ 2:**

- **Cover:** „In 20 Minuten weisst du, worüber du schreiben kannst." → sagt, was sie
  danach kann
- **Folien 2–7:** Schritt 1 bis 5, jeder mit einer Sache, die man heute tun kann
- **Folie 8:** „Kommentier STANDBEIN, dann schick ich dir das Arbeitsblatt dazu."
- **Caption:** *„Die meisten suchen monatelang nach einem Thema, das sie längst haben.
  Kommentier STANDBEIN, dann geh ich die fünf Schritte mit dir durch."* — zwei Sätze
- **Beitrags-Check:** berührt ✅ · konkret: **die fünf Schritte** ✅ · speichern: man
  will die Schritte wiederfinden ✅ · kommentieren: Keyword plus die Frage, bei welchem
  Schritt sie hängt ✅ · nur von ihr: ein echtes Detail aus ihrem Alltag im Einstieg ✅

**Der Gegenentwurf** — genau das, was am 14.09. durchfiel: Cover „Die meisten haben
längst ein Thema", neun Folien Haltung, kein Schritt, acht Absätze Caption.
Berührt ✅, konkret ❌, speichern ❌, kommentieren ❌.

---

## TEIL 9: TESTEN UND NACHSCHÄRFEN

**Woran du merkst, dass es funktioniert hat**

| Signal | Richtwert |
|---|---|
| Kommentare pro Beitrag | mehr als null — das ist der Ausgangsstand |
| Speicherungen | steigend gegenüber Ø 2 auf zwölf Beiträge |
| Engagement-Rate | von 0,3–0,5 % Richtung 1–3 % |
| Keyword-Kommentare | messbar in ManyChat |

**Was du dann änderst**

- Ein Hook-Muster, das zweimal getragen hat → `context/hook-formel-testlog.md`
- Eine Formulierung, die Patricia **zweimal** korrigiert → Regel in TEIL 6, nicht Notiz
  im nächsten Chat
- Eine Floskel, die sie beanstandet → `context/ki-phrasen-blackliste.md`
- Ein Beitragstyp, der dreimal floppt → raus aus dem Wochen-Mix

**Was der Lauf vom 14.09.2026 gelehrt hat** — und warum dieser Skill so aussieht:

| Fehler | Gegenmittel |
|---|---|
| Dateien nicht gelesen | Leseprotokoll mit wörtlichen Zitaten, Schritt 1 |
| Skills nur verwiesen statt gelesen | alle sechs vollständig, jedes Mal |
| fünf Beiträge, ein Typ | Typ-Zettel vor dem Hook, Schritt 5 |
| kein konkreter Schritt in vier von fünf | Beitrags-Check als Tabelle, die Sache selbst in die Zelle |
| Captions achtmal zu lang | Länge am Typ, Schritt 6 |
| Keyword-Regel ignoriert | mindestens drei, im Typ-Zettel geprüft |
| Hook im Video als Fragment | ganzer Satz ab Bild null, TEIL 3 |
| Video nur an fünf Standbildern geprüft | Hook-Fenster alle 0,3 Sekunden, Schritt 6 |
| B-Roll als Montage mit Kästchen gebaut | ein Clip, ein Textblock, keine Kästen, Schritt 6 |
| stundenlang inhaltlich passendes Material gesucht | das Video muss den Text nicht illustrieren |
| abgenommene Hooks umgeschrieben | Verbot in TEIL 3 |
| Anleitung über zwölf Dateien verteilt | diese Datei |

---

## Verwandt

- `.claude/skills/hooks/` · `karussell/` · `reels/` · `story/` · `caption/` · `visuals/`
  — werden hier **vollständig gelesen**, und sind ausserdem für einzelne Stücke da
- `.claude/skills/videoschnitt/` · `handy/` — sobald Video im Spiel ist
- `reference/_archiv-skills/content-alt-2026-09-14/` — die abgelöste Fassung
