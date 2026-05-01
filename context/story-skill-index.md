# /story Skill — Vollständiger Index

**Stand:** 2026-05-01 · Single-Source-Index für GitHub-Actions-Reminder-Aktion und alle Skill-Folge-Arbeiten.
**Quelle-Skill:** `.claude/commands/story.md` (662 Zeilen)

---

## 1. Was kann /story (8 Modi)

1. **Tagesplan** — Standard-Hauptmodus: 6-8 Slides aus Patricia-Tagesinput, Käufertyp-rotiert, mit CTA.
2. **Sales-Day** — 8-12 Slides über den Tag verteilt während aktivem Launch (alle 7 Nadja-Personas).
3. **Story-Doktor** — aus 1-3 Sätzen Idee → Template-Match + 3 Hook-Varianten + 3-5 Slides.
4. **One-Slide-Tag** — Low-Effort: 1 Slide aus Julia-Säule-3 / Nadja-Pool, Soft-Link.
5. **Story-Serie** — 3-7 Tage dramaturgischer Bogen mit Cliff-Hangern, letzter Tag harter Pitch.
6. **Behind-the-Scenes** — aus Foto/Erlebnis: 3-5 Slides mit Pflicht-Soft-Link.
7. **Highlight-Pflege** — bestehende Highlights ordnen/aktualisieren/Cover-Vorschläge.
8. **Reaktiv** — auf DM-Antwort/Umfrage-Ergebnis: 1-2 Antwort-Slides + Folge-Story.

---

## 2. Pflicht-Regeln (komprimiert)

- **BÄM-Hook (Slide 1) Pflicht** — KEIN „Hallo / Guten Morgen / Hab grad / Bin grad / Sitze grad / Schaut mal / Heute zeige ich". Anti-Mainstream / konkrete Zahl / Provokation / Schmerz / kontroverse Behauptung. 1-Sekunden-Lese-Test.
- **Patricia-Sprachnotiz ist Roh-Material für Slide 2-3, NIEMALS direkt der Hook.** Hook ist die dramatische Wahrheit, abgeleitet aus dem Erlebnis.
- **CTA-Link Pflicht** — jede Sequenz hat mind. 1 Link aus `active-funnels.json` (Freebie ODER Produkt). Ausnahme nur „Reconnect-Modus" bei Engagement-Crash.
- **Käufertyp-Rotation** — alle 4 DISG-Achsen (Rot/Gelb/Grün/Blau) müssen jede Woche vorkommen.
- **Julia-Templates (1-10) als Bauplan** — keine Wellness-Talk, kein Garten-Romantik. Bauplan, nie 1:1 Copy-Paste.
- **PIE-Mittelteil** — Problem → Insight → Example. Privates ist Knochen, nicht Zucker.
- **Voice-Check 6 Punkte (vor Render):** Hook-Knall · Provokation Slide 3/4 · Knappheit letzte Slide · Foto-Schutz · Echte Umlaute/Du-Anrede · Patricia-Realität.
- **Foto-Priorität 3-stufig:** aktuelles Foto > Shootingbilder > Stock (nur personenfreie Atmosphäre).
- **Foto-Schutz:** Sticker NIE über Hauptmotiv (Gesicht/Bergpfel/Logo).
- **Mix-Stil 8-Slides:** 5 Brand-Designed + 3 Foto-First (Slide 2, 4, 5).
- **Kein Datum-Stempel auf Slides** (Memory-Regel).
- **doTERRA-Compliance:** keine Heilversprechen, „bei mir war"-Frame.
- **Echte Umlaute (ä/ö/ü), Schweizer ss, Du-Anrede.**
- **Keine erfundenen Zahlen** — nur aus `patricia-expertise.md` / `patricia-freebies.md` / Patricia-Input.
- **Max. 1 Story-Sequenz pro Tag** ohne explizite Anweisung.

---

## 3. Pflicht-Lese-Files beim Skill-Start

Story-spezifisch:
- `context/ki-phrasen-blackliste.md` — KI-Floskel-Filter (5-Punkte-Pflichtprüfung).
- `context/story-framework.md` — Zentrales Story-Wissen + 8 Modi + Visual-Pipeline.
- `context/julia-stories-die-verkaufen.md` — Slide-Goldformel + 7 Storytelling-Regeln.
- `context/julia-insta-stories-anleitung.md` — 10 Verkaufs-Templates.
- `context/julia-story-ideen.md` — 3-Säulen-Bibliothek (Expertise/Inspiration/Persönlichkeit).
- `context/brandastic-kaeufertypen.md` — DISG (4 Typen) + AIDA.
- `context/nadja-story-prompts.md` — 7 Käuferpersonas (Wilma/Werner/Isabell/Charlie/Petra/Stefan/Bärbel).

Patricia-spezifisch:
- `context/patricia-expertise.md` — Methoden, Beispiele, validierte Zahlen.
- `context/patricia-freebies.md` — Cross-Referenz Freebies.
- `context/brand-voice.md`, `context/hook-framework.md`, `context/caption-formeln.md`, `context/business-info.md`.
- `context/active-funnels.json` — aktuell aktive Funnels.
- `context/manychat-keywords.md` — Story-CTA-Keywords.

Bei doTERRA zusätzlich:
- `context/doterra/patricia-wendepunkt-story.md` (Single Source of Truth).
- `context/doterra/` (komplett: Pyramide, Ölschule, Compliance).
- Memorys: `feedback_doterra-compliance-no-heilversprechen`, `feedback_KRITISCH-doterra-keine-erfundenen-fakten`.

Memorys (immer aktiv): `feedback_keine-erfundenen-zahlen`, `feedback_umlaute-echte`, `feedback_hooks-inspiration-nicht-copypaste`, `feedback_transformation-statt-features`, `feedback_brand-metaphern-patricia`, `feedback_foto-schutz-overlays`, `feedback_foto-quellen-priorisierung`, `feedback_kein-datum-auf-slides`, `feedback_hook-knall-pflicht`.

---

## 4. Daten-Quellen die der Skill braucht

- **Notion — Wochenplanung-DB** `collection://2ae7078e-8b7e-81e7-9083-000b01908eb5`. Liest Property `Fokus der Woche` + Body-Tabelle „Was planst du je Business-Säule? → Content-Creation". Cache: `outputs/stories/wochen-kontext-KW##.json`.
- **Notion — weitere DBs:** Aufgaben (`3167078e-8b7e-80baa770dc1a6c38c41e`), Tagesplaner (`3167078e-8b7e-8065a8a2f3ebe4e485e8`), Content-Management (`2ae7078e-8b7e-811a-ad14-000ba5820c09`), Produkte (`2ae7078e-8b7e-81ef-aafa-f03993ef344f`).
- **`context/active-funnels.json`** — Status (`live-launch-woche` / `live` / `launching`), `traffic_quellen.wordpress_landing`, `manychat_keyword`, `launch_window`, `produkttreppe_anschluss`. Bei mehreren aktiven Funnels: Patricia fragen.
- **`outputs/stories/wochen-log.json`** — Käufertyp-Tracking pro Tag (`{ "YYYY-MM-DD": { profil, modus, disg, nadja_persona, story_saeule, slug, slides } }`). Skill ergänzt nach jedem Lauf.
- **`outputs/stories/wochen-kontext-KW##.json`** — Notion-Wochenplan-Cache (kw + monatsplan + wochenplan + fokus_der_woche + zeitraum + abgerufen_am). Gültig für ganze Woche.
- **`outputs/stories/_state/wochen-fokus-override.json`** — Manueller Override (kw + thema + funnel_id + produkt + gesetzt_am).
- **`outputs/stories/_state/briefing-pending.json`** — Zustand des laufenden Telegram-Dialogs (profil + briefing_text + fragen + kontext_snapshot + gesendet_am + patricia_antworten[] + patricia_fotos[] + patricia_videos[] + status).
- **`outputs/stories/_uploads/`** — Patricia-Fotos die per Telegram an `Patricia_content_bot` ankommen.
- **`context/Shootingbilder/`** — >1000 Patricia-Fotos.
- **`context/stock-fotos/{atmosphaere-mentoring,atmosphaere-doterra,atmosphaere-universell}/`** + `_metadata.json` pro Kategorie.
- **Patricia-Input-Quelle:** Telegram-DM an `Patricia_content_bot` (Sprachnotiz → `scripts/transcribe/transcribe.js` → Text), oder direkt-Text im Chat, oder „standard" → Skill zieht aus `julia-story-ideen.md`.

---

## 5. Visual-Pipeline (HTML → PNG)

Skill schreibt `outputs/stories/[ordner]/slides.html` mit Template-Klassen aus `scripts/karussell-render/brand-stories.css` (8 Templates: `template-hook` · `template-story` · `template-zitat` · `template-frage` · `template-cta` · `template-bts` · `template-vorher-nachher` · `template-countdown`). Foto-First-Variante: `template-foto-overlay` mit `box-creme/box-petrol/box-schwarz`. Body-Klasse `profil-mentoring` (Petrol) oder `profil-doterra` (Orange). Render via `node scripts/karussell-render/render-stories.js --input=... --output=...` → 1080×1920 PNGs (Instagram-Story-postbar) in `outputs/stories/[ordner]/slides-png/01.png ... NN.png`. Beispiel-HTML mit allen 8 Templates: `outputs/stories/_template-beispiel/slides.html`. Alternativer Render `render-storyboard.js` für 1080×2400 (Reel-Storyboards, nicht für Stories).

---

## 6. DISG-Käufertyp-Rotation

| Typ | Motivation | Trigger | Bei Stories |
|---|---|---|---|
| **Rot — Dominant** | hinzu (Status, Erfolg) | direkt, pushy, Vorteil sofort | Zahlen, Erfolgs-Screenshots, knappe Hooks |
| **Gelb — Initiativ** | hinzu (Spass, Selbstausdruck) | locker, neugierig machen | Persönliche Einblicke, Quiz/Schieber-Sticker |
| **Grün — Stetig** | wegvon (Konflikt) | Samthandschuhe, Wir-Sprache | Community, Mama-Realität, Sicherheit |
| **Blau — Gewissenhaft** | wegvon (Fehler) | Fakten, Schritt-für-Schritt | Daten, Testimonial mit Zahlen, FAQ |

**Wochenrotation-Standard** (überschreibbar bei Launch):
| Tag | Haupt | Sekundär |
|---|---|---|
| Mo | Grün | Gelb |
| Di | Rot | Blau |
| Mi | Gelb | Grün |
| Do | Blau | Rot |
| Fr | Gelb | Grün |
| Sa | Grün | Gelb |
| So | Rot | Blau |

**Wie weiss der Skill welche Achse heute dran ist?** Liest `outputs/stories/wochen-log.json`, prüft welche DISG-Achsen die letzten 7 Tage angesprochen wurden, wählt unterrepräsentierte → fällt zurück auf Standardtabelle wenn Log leer. Aktualisiert Log nach Lauf.

**DISG → Nadja-Persona:** Rot=Charlie/Stefan · Gelb=Isabell · Grün=Werner/Petra · Blau=Wilma/Bärbel.

---

## 7. Was ein Daily-Reminder (06:30 Schweiz) wissen muss

**Vor dem Reminder zu lesen:**
1. Aktuelle KW berechnen → `outputs/stories/wochen-kontext-KW##.json` lesen (oder Notion-Search wenn Cache fehlt).
2. `outputs/stories/_state/wochen-fokus-override.json` (manueller Override hat Vorrang).
3. `context/active-funnels.json` → welcher Funnel hat Status `live-launch-woche` oder `launching`?
4. `outputs/stories/wochen-log.json` → welche DISG-Achse fehlt heute.
5. Wochentag → Modus-Vorschlag.

**Modus-Vorschlag pro Wochentag (Standard, überschreibbar bei aktivem Launch):**
- Mo-Sa: **Tagesplan**.
- Wenn ein Funnel `status=launching` oder `live-launch-woche` mit `tag_X_datum` heute: **Sales-Day**.
- Wenn Patricia gestern „kein Bock" tippte oder nichts antwortet: **One-Slide-Tag**.
- So: Tagesplan mit Reflexions-Akzent (Rot+Blau).

**Output-Form (Telegram-DM-Text an `Patricia_content_bot`):**
```
🌅 Guten Morgen, Patricia!

Heute: [Wochentag, Datum]
Profil: [Mentoring/doTERRA]
Aktives Produkt: [Name aus Wochenvorwahl/Override/active-funnels]
Käufertyp heute: [DISG-Achse + Nadja-Persona]
Story-Säule: [Expertise/Inspiration/Persönlichkeit]

Bevor ich rendere — was war heute / gestern bei dir?
• Was hast du erlebt? (Konflikt, Erfolg, peinlicher Moment, Erkenntnis, Familien-Szene, …)
• Hast du grad einen Gedanken zum Thema?
• Oder soll ich aus deinem Standard-Pool ziehen? Tipp dann nur "standard".

Schick mir Sprachnotiz (Wispr Flow) oder kurz tippen.
```
Schreibt Zustand parallel in `outputs/stories/_state/briefing-pending.json` (status `warten_auf_antwort`).

---

## 8. Was beim Trigger (workflow_dispatch) reinkommt von Patricia

Erwartete Inputs:
- **`modus`** (string, default `tagesplan`): `tagesplan` / `sales-day` / `doktor` / `1-slide` / `serie` / `bts` / `highlights` / `reaktiv`.
- **`profil`** (string, default `mentoring`): `mentoring` / `doterra`.
- **`patricia_input`** (string, optional): Plain-Text der Sprachnotiz/Tippnotiz. Roh-Material für Slide 2-3, **nie direkt Hook**.
- **`foto_pfad`** (string, optional): Pfad in `outputs/stories/_uploads/` falls Patricia Foto geschickt hat.
- **`funnel_override`** (string, optional): Funnel-ID aus `active-funnels.json` falls nicht der defaultmässig aktive verwendet werden soll.
- **`tage`** (number, optional, nur für `serie`): 3, 5 oder 7.

**Was muss der Skill damit tun:**
1. Profil-Pflicht-Reads laden (siehe §3).
2. Wenn `patricia_input` leer → Tagesplan-Reminder posten und auf Antwort warten (nicht weiter rendern).
3. Wenn `patricia_input` = `"standard"` → aus `julia-story-ideen.md` Säule 3 + `nadja-story-prompts.md` ziehen.
4. Wenn `patricia_input` Text → gegen 10 Julia-Templates matchen (siehe story.md Schritt 5: persönlich+Produkt=T10, Misserfolg=T7, Kunden-Erfolg=T2, Aha=T1, Anti-Mainstream=T9, letzter Launch-Tag=T8, frustriert=T6, Meme=T5, Spiegelung=T3, Warnung=T4).
5. 6-8 Slides bauen nach Pflicht-Aufbau (Hook→PIE→Glaubenssatz→Insight→Sticker→Lösung→CTA).
6. 6-Punkte-Voice-Check (Hook-Knall, Provokation, Knappheit, Foto-Schutz, Sprache, Patricia-Realität). Hook-Fail = Skill schreibt neu, fragt nicht.
7. Foto-Wahl 3-stufig (Upload > Shootingbilder > Stock).
8. `slides.html` schreiben mit Mix-Stil 5+3.
9. `render-stories.js` aufrufen → PNGs.
10. PNGs einzeln per Telegram an Patricia (mit Sticker-Empfehlung pro Slide, Position relativ zum Foto-Hauptmotiv, Umfrage-Optionen).
11. `wochen-log.json` updaten (DISG + Persona + Säule + Slug).
12. `briefing.md` speichern.

---

## 9. Offene Lücken / TODOs

- **`render-stories.js` Default-Input** zeigt auf `outputs/funnels/bio-check/launch/tag-0-stories-folien.html` statt eines neutralen Story-Defaults — bei Aufruf ohne `--input` läuft der falsche Pfad.
- **`scripts/transcribe/transcribe.js`** wird in story.md erwähnt (Sprachnotiz-Transkription), Existenz nicht verifiziert in dieser Indexierung.
- **`outputs/stories/wochen-vorwahl-KW##.json`** wird in story.md Modus-1-Schritt 1 erwähnt („vom Freitag-Bericht") — keine solche Datei vorhanden, nur `wochen-kontext-KW##.json`. Mechanik (Freitag-Bericht-Job) existiert offenbar noch nicht.
- **Notion-Eintrag-Schreibphase** (story-framework.md „Phase 2") ist optional und nicht implementiert — Skill schreibt aktuell keinen Content-Management-DB-Eintrag.
- **Highlight-Pflege-Output (Modus 7)** ist als `outputs/stories/highlights-[profil]-stand-YYYY-MM-DD.md` spezifiziert, aber kein Beispiel/Template im Workspace.
- **`brand-stories.css` Template `template-foto-overlay`** wird in story.md Schritt 8 referenziert, in `_template-beispiel/slides.html` aber nicht verwendet — Mix-Stil-Pflicht im Beispiel nicht gezeigt.
- **Sales-Day-Modus liest `outputs/funnels/[slug]/launch-plan.md`** — muss bei GitHub-Action-Trigger explizit geprüft werden (existiert nicht für jeden Funnel automatisch).
- **`active-funnels.json`-Status-Werte uneinheitlich** (`live`, `live-launch-woche`, geplant ist auch `launching` laut story.md) — bei Sales-Day-Trigger-Logik aufpassen.
