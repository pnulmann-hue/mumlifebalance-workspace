---
name: angebot
description: "Ein Angebot auf Knopfdruck: wenige Fragen, dann baut Claude in einem Durchgang das ganze Paket — Kursaufbau, Verkaufsseite, Bump/Upsell/Downsell, Mails, Storys, Stichwort-Automation, Anzeigentexte. Prüft auch bestehende Trichter gegen die Funnel-Checkliste und baut, was fehlt. Dran bei /angebot, „bau mir das ganze Paket für …“, „prüf den Trichter für …“, „Fokus nächster Monat ist …“."
---

# /angebot — das ganze Paket auf einen Knopf

**Aufruf:** `/angebot minikurs` · `/angebot kurs` · `/angebot freebie` · optional mit Thema dahinter
(`/angebot minikurs Storys ohne Kamera`). Ohne Art: einmal fragen.
**Nochmal bauen:** `/angebot nochmal <slug> [baustein]` — baut aus dem gespeicherten Bauplan
alles oder nur einen Baustein neu (z. B. `mails`).
**Trichter prüfen und ergänzen:** `/angebot trichter <produkt>` · `/angebot monat` (nimmt den
Fokus aus dem Monatsplan) — siehe Teil B unten. Prüft einen bestehenden Trichter Punkt für Punkt
und baut, was fehlt, veraltet ist oder laut Befund neu her muss.

**Anlass (27.10.2026):** Patricia sah in einer Story einer Mentorin ein Werkzeug „Business auf
Knopfdruck“ und wollte es für sich. Übernommen ist nur der **Ablauf** (Idee → ein Knopf → Paket
mit Haken), nicht Wortlaut, Aussehen oder Name.

🚨 **Dieser Skill schreibt keine eigenen Regeln.** Er ist die Klammer um die bestehenden Skills.
Jeder Baustein wird nach dem Skill gebaut, der dafür zuständig ist (Tabelle unten), und zwar
nach dessen `SKILL.md`. Ändert sich dort eine Regel, gilt sie hier automatisch. Ändert sich hier
etwas an einer Bau-Regel, ist es falsch eingetragen.

---

## Ablauf in drei Stationen

### Station 1 · Die Idee (Fragen — höchstens zwei Runden)

Zuerst **lesen, dann fragen.** Was im Workspace steht, wird nicht gefragt:

- `context/active-funnels.json` und `outputs/cockpit/abgleich/katalog.json` — was es schon gibt
  (Preise, Kassen, Stichwörter, laufende Funnels). **Keine Dopplung mit einem bestehenden
  Angebot**, sonst nachfragen.
- `context/patricia-expertise.md` — was in ihren Kursen schon gelehrt wird
- `context/kern-painpoint.md` · `context/brand-voice.md` · `context/patricia-vollprofil.md`
- `context/kundinnen-geschichten.md` — **nur** von dort echte Fälle und Stimmen
- `context/manychat-keywords.md` — welche Stichwörter vergeben sind
- der aktuelle Monatsplan in `outputs/monatsplaene/` — passt das Angebot in den Monat?

Dann mit `AskUserQuestion` (Knöpfe, wo es geht) nur das, was fehlt:

| # | Frage | nur bei |
|---|---|---|
| 1 | Profil: Mentoring oder doTERRA? | wenn aus dem Thema nicht klar |
| 2 | Für wen genau, und was ist nachher in ihrem Alltag anders (die **Veränderung**)? | immer |
| 3 | Der Schmerz davor — ihre Worte, ein konkreter Moment | immer |
| 4 | Was ist der Weg — die 3–5 Schritte, die du ihr zeigst? | Minikurs · Kurs |
| 5 | Preis (Minikurse **fix 39**, nicht fragen) und Kassenart (einmalig/Raten) | Kurs |
| 6 | Was kommt danach? Zwei Dinge: Bump/Upsell/Downsell **an der Kasse** (kleiner als das Hauptprodukt) und die **nächste Stufe**, die die Mails pitchen. Vorschläge aus dem Katalog mitgeben | immer |
| 7 | Gibt es eine echte Kundinnen-Stimme dazu? (sonst bleibt der Platz leer) | Minikurs · Kurs |
| 8 | Stichwort fürs Kommentar-Freebie — Vorschlag machen, gegen vergebene prüfen | Freebie |

### Station 2 · Der Bauplan (ein einziger Stopp)

Aus den Antworten `00-bauplan.md` schreiben und **im Chat in zehn Zeilen zeigen**: Name ·
für wen · Veränderung · Preis · Kette (Bump · Upsell · Downsell mit Preisen) · Stichwort ·
Bausteine, die gleich entstehen. Darunter die Rechnung der Kette ausgeschrieben.

Frage: „Passt das — soll ich bauen?“ Das ist der grüne Knopf. **Danach kein Stopp mehr** bis
zum fertigen Paket. Korrekturen kommen am Schluss über `/angebot nochmal`.

### Station 3 · Die Umsetzung (alles in einem Durchgang)

Bausteine in dieser Reihenfolge bauen — jeder liest `00-bauplan.md`, nicht den Chat. Nach jedem
Baustein eine Zeile im Chat: `✓ Kursaufbau` usw., damit Patricia sieht, wo es steht.

---

## Die Bausteine je Art

| Nr | Baustein | Minikurs | Kurs | Freebie | gebaut nach | Datei |
|---|---|:-:|:-:|:-:|---|---|
| 01 | Kursaufbau / Freebie-Inhalt | ✓ | ✓ | ✓ | `/produkt` Modus 3a | `01-aufbau.md` |
| 02 | Verkaufsseite (13 Blöcke) bzw. Landingpage | ✓ | ✓ | ✓ | `/copywriting` inkl. „ThriveCart-Tipps“ | `02-salespage.md` |
| 03 | Bump · Upsell · Downsell | ✓ | ✓ | — | `/produkt` Modus 6 | `03-kasse.md` |
| 03 | Danke-Seite mit Angebot „nur hier“ | — | — | ✓ | CLAUDE.md „AC-Formulare“ | `03-danke-seite.md` |
| 04 | Mails | ✓ | ✓ | ✓ | `/copywriting` (Format E-Mail) | `04-mails.md` |
| 05 | Storys zum Verkaufen | ✓ | ✓ | ✓ | `/story` Modus 5 (Serie) | `05-storys.md` |
| 06 | Feed: 3 Beiträge mit Hook | ✓ | ✓ | ✓ | `/content` (Einzelauftrag) + `/hooks` | `06-feed.md` |
| 07 | Stichwort-Automation (Kommentar → DM) | ✓ | ✓ | ✓ | `/funnel` Mode 2 | `07-automation.md` |
| 08 | Meta-Anzeigentexte | ✓ | ✓ | ✓ | `/facebook-ads` (5 Texte · 5 Überschriften · 5 Beschreibungen) | `08-anzeigen.md` |
| 09 | Einrichte-Liste | ✓ | ✓ | ✓ | dieser Skill | `09-einrichten.md` |

**Was die Mails je Art sind:**
- Minikurs/Kurs: Bestätigung nach Kauf + 5 Nachkauf-Mails (Modus 6 in `/produkt`), der Pitch
  aufs Upsell erst, wenn der Kurs ein **neues** Problem geschaffen hat
- Freebie: Bestätigungsmail (**ein** Job: der Klick, kein Angebot) + 5 Begleit-Mails + Pitch

**Was in 09 steht:** alles, was Patricia von Hand einrichtet, mit Ort — ThriveCart-Produkt und
Bumps, WP-Seite (Entwurf), AC-Liste + **ein** Tag `0€ <Name>` bzw. `<Name>` + Automation,
ManyChat-Flow, Drive-Ordner. Pro Zeile ein Kästchen `- [ ]`.

---

## Regeln, die quer über alle Bausteine gelten

Sie stehen in den Skills und in CLAUDE.md — hier nur als Gedächtnisstütze, weil ein Paket an
neun Stellen dieselbe Zahl und denselben Namen tragen muss:

- **Eine Quelle:** Name, Preise, Stichwort, Termine stehen **nur** in `00-bauplan.md`. Die
  Bausteine übernehmen sie von dort. Am Schluss mit `grep` gegenprüfen, dass überall dieselben
  Werte stehen.
- **Preis-Kette:** Bump günstiger als das Hauptprodukt · Upsell teurer als der Bump, aber
  günstiger als das Hauptprodukt · Downsell günstiger als das Upsell. Jede Zahl mit Rechnung,
  keine Differenz erraten. Minikurse fix 39. **Keine Geld-zurück-Garantie.**
- **Veränderung statt Zahlen:** nie über Modul-, Lektions-, Kapitel- oder Call-Zahlen
  verkaufen. Im Kursaufbau stehen sie, in Verkaufstexten nicht.
- **Nichts erfinden:** keine Kundinnen-Stimme, keine Zahl, keine Alltagsszene, die nicht belegt
  ist. Leerer Platz mit `✏️ PLATZ:` statt Erfundenem.
- **Zwei Zielgruppen-Ebenen:** Patricias Kundinnen sind Mamas — deren Kundschaft nie.
- **Hooks** nur über `.claude/skills/hooks/SKILL.md`, inkl. letztem Check (fünf Fragen).
- **Stichwort:** neu oder vergeben? `context/manychat-keywords.md` ist kein Beleg, dass ein Flow
  läuft — in 09 steht immer „Flow in ManyChat anlegen und testen“.
- **Keine Mentorinnen-Namen**, kein Wortlaut aus gekauftem Material in den Texten.
- **Schweizer ss, echte Umlaute, CHF.**

---

## Ablage

```
outputs/produkte/<slug>/angebot/
├── 00-bauplan.md      # die eine Quelle für Name, Preise, Kette, Stichwort
├── 00-paket.md        # Übersicht mit Haken — das, was am Schluss im Chat steht
├── 01-aufbau.md … 09-einrichten.md
```

Gibt es `outputs/produkte/<slug>/` schon (bestehendes Produkt), kommt das Paket in den
Unterordner `angebot/` daneben und überschreibt nichts. Jede Datei beginnt mit dem Frontmatter `tags: [produkt]`
(Obsidian-Konvention).

---

## Abschluss — vor der Meldung „fertig“

1. `python scripts/cockpit/texte-pruefen.py --datei outputs/produkte/<slug>/angebot/0*.md`
   — jeden 🔴 umschreiben, jeden 🟠 anschauen.
2. Gegenprobe Werte: Name, Preise und Stichwort aus `00-bauplan.md` per `grep` in allen Dateien
   suchen; jede Abweichung korrigieren.
3. Hook-Check und Beitrags-Check (Lesearbeit) für 06 und die erste Story-Folie.
4. `bash scripts/obsidian-reindex.sh`
5. `00-paket.md` schreiben und im Chat zeigen:

```
✓ Kursaufbau            01-aufbau.md
✓ Verkaufsseite         02-salespage.md
✓ Bump · Upsell · Downsell
…
⚠️ 3 Plätze zum Ergänzen (✏️ PLATZ) — Stimme in Block 3, Foto Über-mich, …
```

Danach anbieten: gestaltete Verkaufsseite mit einem der Design-Skills, Beiträge ins Cockpit,
Mails in die Kopierseite. **Nichts geht ohne ihr Go live** — keine WP-Seite veröffentlichen,
nichts in ThriveCart, AC, ManyChat oder Blotato anlegen. Der Skill baut die Texte, eingerichtet
wird über die Liste in 09.

---

## Teil B · Trichter prüfen und ergänzen (`/angebot trichter` · `/angebot monat`)

**Anlass (27.10.2026), Patricia:** *„wenn ich z.B. nächsten monat digitale produktwelt im fokus
habe … dann wird mir ein trichter gebaut … oder schon ein bestehendes genommen und dann wird nach
den punkten alles geprüft“* — und dazu: *„es müsste aber auch möglich sein was neues zu bauen wenn
zb die analyse ergibt, dass es nötig ist“*.

Bestehende Trichter veralten still: ein Termin vom Frühling auf der letzten Workbook-Seite, eine
Mail, die aufs falsche Angebot zeigt, Modulzahlen statt Veränderung. Dieser Teil findet das, bevor
eine Kundin es findet, und baut dann nur, was nötig ist.

### B1 · Was geprüft wird

- `/angebot monat` → Fokus aus `outputs/monatsplaene/<JJJJ-MM>-mentoring.md` (bzw. `-doterra`)
  des **kommenden** Monats lesen (ab dem 20. eines Monats, sonst der laufende). Steht dort mehr
  als ein Angebot, das grösste nehmen und den Einstieg dazu.
- `/angebot trichter <produkt>` → das genannte Produkt.

Dann den **ganzen Weg** zum Produkt zusammensuchen, rückwärts von der Kasse:
Kasse (ThriveCart-Status aus `outputs/cockpit/abgleich/katalog.json`, Bumps/Upsells) ·
Verkaufsseite · Einstiege (alle Freebies, deren `produkttreppe_anschluss` in
`context/active-funnels.json` auf das Produkt zeigt, plus Danke-Seiten mit Angebot) ·
Workbooks/Auslieferung · Mails (Bestätigung, Begleitung, Pitch — Generator-Skripte und
`outputs/funnels/`) · Stichwort und Flow (`context/manychat-keywords.md`) · Storys und Feed
des Monats im Cockpit · Termine im Monatsplan.

### B2 · Die Prüfung

Prüfliste erzeugen — dieselben Punkte wie auf der Funnel-Checkliste-Seite, damit beides nie
auseinanderläuft:

```bash
python scripts/cockpit/funnel-checkliste-bauen.py --punkte > outputs/produkte/<slug>/angebot/00-pruefliste-roh.md
```

Jeden Punkt gegen die **echten Inhalte** prüfen, nicht gegen die Beschreibung in CLAUDE.md:
Seiten über die WP-REST-Schnittstelle oder `curl` lesen, Workbooks öffnen, Mails im Generator
oder in `outputs/` lesen, Preise aus ThriveCart. Je Punkt einer von fünf Befunden:

| | heisst | mit |
|---|---|---|
| ✅ | passt | Fundstelle |
| ⚠️ | veraltet oder falsch | Fundstelle **und** Zitat der falschen Stelle |
| ❌ | fehlt | was fehlt und wo es hingehört |
| ➖ | trifft hier nicht zu | ein Halbsatz warum (z. B. „kein Webinar geplant“) |
| ❓ | nicht prüfbar | warum (z. B. „AC-Mail liegt nur in ActiveCampaign“) |

Zusätzlich immer, auch wenn kein Punkt danach fragt: **Termine und Preise** in allen Teilen gegen
den Monatsplan (`grep` über alle Fundstellen) und **Veränderung statt Zahlen** (Modul-, Kapitel-,
Lektions-, Call-Zahlen in Verkaufstexten).

🚨 **❓ ist kein ✅.** Was nur in ActiveCampaign, ManyChat oder ThriveCart steht und über keine
Schnittstelle lesbar ist, bleibt ❓ und geht als Prüfauftrag in die Einrichte-Liste.
🚨 **Ein Befund braucht eine Fundstelle.** „Scheint zu passen“ gibt es nicht.

Ergebnis: `00-befund.md` — oben die Kurzfassung (je Befund die Zahl, dann die ⚠️ und ❌ nach
Gewicht), darunter die volle Liste.

### B3 · Die Entscheidung: flicken, neu bauen oder neuer Trichter

Aus dem Befund folgt **je Baustein** eine von drei Empfehlungen:

| Empfehlung | wann |
|---|---|
| **flicken** | Der Baustein trägt, nur Stellen sind veraltet (Datum, Preis, Link, Zahlen) |
| **neu bauen** | Der Baustein fehlt, oder mehr als ein Drittel seiner Punkte ist ⚠️/❌, oder er verkauft das falsche Angebot |
| **neuer Trichter** | Kein Einstieg führt aufs Produkt · der Einstieg passt nicht zum Monatsfokus · oder die Zahlen sagen, dass er nicht trägt (Eintragungen je Beitrag aus `outputs/cockpit/abgleich/funnel.json`, Verkäufe aus ThriveCart) |

„Neuer Trichter“ heisst: ein neues Freebie mit allem Drum und Dran — dann läuft **Teil A** mit
`freebie`, und der Bauplan nimmt das Produkt als Anschluss. Der Befund sagt, **warum** der alte
Einstieg nicht reicht, mit Zahl.

**Der eine Stopp wie in Teil A:** Befund in rund zehn Zeilen im Chat zeigen — wie viele Punkte
passen, die wichtigsten ⚠️ und ❌, und je Baustein flicken / neu / neuer Trichter. Frage:
„Soll ich so bauen?“ Danach ohne Stopp.

### B4 · Bauen

- **flicken:** in der **Quelle** ändern (Generator-Skript, Markdown, WP-Bauskript), nie im
  Ausgabe-HTML allein, und den Generator laufen lassen. Was nur in einem fremden System steht
  (AC-Mailtext, Workbook in Canva, ThriveCart), kommt als Zeile mit altem und neuem Wortlaut in
  `09-einrichten.md` — eine korrigierte Datei ändert nichts an dem, was verschickt wird.
- **neu bauen:** nach Teil A, Baustein-Tabelle, mit `00-bauplan.md` aus dem Befund (Name, Preis,
  Termine aus Monatsplan und Katalog — nicht neu erfragen, was dort steht).
- **Storys und Feed des Monats:** nur prüfen und Abweichungen melden, wenn sie schon im Cockpit
  liegen. Neu gebaut wird nur, was im Monat fehlt — `/content` bleibt für die Wochen zuständig.

Ablage im selben Ordner wie Teil A: `outputs/produkte/<slug>/angebot/` mit `00-befund.md`,
`00-bauplan.md`, den Bausteinen und `09-einrichten.md`. Abschluss wie Teil A (Text-Prüfung,
Werte-Gegenprobe, Reindex, `00-paket.md` im Chat). Nichts geht live ohne ihr Go.

---

## Beispiel (verkürzt)

> `/angebot minikurs Storys, die verkaufen, ohne dass man sich zeigt`
>
> Claude liest Katalog und Funnels, sieht: „90 Storyideen“ und die Story-Challenge gibt es,
> fragt nur noch nach Veränderung, Schmerz-Moment, Weg und Kundinnen-Stimme. Bauplan: „Story ohne
> Gesicht“, 39 · Bump Content-Box 17 (< 39) · Upsell „Finde dein Thema“ 25 (> 17, < 39) ·
> nächste Stufe in den Mails: Instagram-Kundenmaschine · Stichwort GESICHT (frei).
> Patricia: „passt“. Danach neun Haken, eine Einrichte-Liste, zwei ✏️-Plätze.
> *(Preise im Beispiel aus dem Katalog vom Oktober 2026 — beim echten Lauf neu lesen.)*

🔗 [[produkt]] · [[copywriting]] · [[funnel]] · [[story]] · [[facebook-ads]] · [[hooks]]
