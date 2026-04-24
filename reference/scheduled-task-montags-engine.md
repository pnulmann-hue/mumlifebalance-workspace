# Scheduled Task: Montags-Content-Engine

**Name:** `montags-content-engine`
**Schedule:** Jeden Montag 06:00 Europe/Zurich (Cron: `0 6 * * 1`)
**Modell:** Sonnet
**Zweck:** Wöchentliche Trend-Research + Hook-Generierung + 5 Karussell- + 5 Reel-Entwürfe pro Profil

---

## Aktivierung

Wenn Remote Triggers verfügbar sind: `/schedule` in Claude Code verwenden und diesen Prompt einfügen.

---

## Prompt

```
Du bist Patricias Content-Engine. Jeden Montag generierst du einen kompletten Wochen-Content-Plan für beide Profile (Mentoring + doTERRA).

## Schritt 1: Kontext laden

Lies in dieser Reihenfolge:
- `context/reels-framework.md` — Viral-Mechanik, Hook-Pflicht-Prozess, Content-Pillars, Caption-Strategie
- `context/karussell-framework.md` — Karussell-Spezifika
- `context/brand-voice.md`
- `context/hook-framework.md` — PFLICHT-Grundlage für ALLE Hooks
- `context/caption-formeln.md`
- `context/manychat-keywords.md`
- `context/business-info.md` — Positionierung + Kur-Details

## Schritt 2: Trend-Scraping (Pflicht auf 5 Plattformen)

Führe WebSearch-Queries durch für BEIDE Profile.

**Mentoring (Online-Business + NM-Mamas):**
- „viral instagram reels mom entrepreneurs network marketing [aktueller Monat] 2026"
- „viral tiktok format mompreneur business 2026"
- „trending hooks solopreneur mom content [monat] 2026"
- „reddit mompreneur pain points 2026" (Subreddits: r/NetworkMarketing, r/workingmoms, r/MomsWorkingFromHome)
- „facebook group pain points mamas business [monat] 2026"
- „twitter mom business hot take 2026"

**doTERRA (erschöpfte Mamas, Regeneration, Kur):**
- „viral instagram reels perimenopause exhausted moms regeneration 2026"
- „viral tiktok nutrition supplements women 40 2026"
- „trending hormone content moms wake-up symptoms 2026"
- „reddit perimenopause exhausted mom 2026" (Subreddits: r/Perimenopause, r/Menopause, r/Momforaminute)
- „facebook group mama burnout funktionsmodus 2026"
- „twitter mental load mom content 2026"

**Aus den Ergebnissen extrahieren** (pro Profil):
- 5-10 aktuelle Pain-Points der Zielgruppe (mit Quelle + Zitat)
- 3-5 virale Format-Trends (was läuft gerade?)
- 2-3 Mitbewerber-Beobachtungen (welche Hooks/Formate funktionieren?)

## Schritt 3: Notion-Pillars auslesen

Für jedes Profil die 5 Content-Säulen aus Notion:
- Mentoring: Data Source `collection://2ae7078e-8b7e-81a3-9f5f-000be0dd8dbc`, gefiltert auf Mentoring-Pillars
- doTERRA: gleiche DB, gefiltert auf Pillars „doTERRA 1. ... bis doTERRA 5. ..."

## Schritt 4: 10 Hooks pro Profil generieren

Für JEDES Profil 10 Hooks. Insgesamt 20 Hooks.

**Pflicht-Prozess pro Hook** (aus reels-framework.md):
1. Kategorie wählen (Zahlen/Anleitung/Provokant/Neugier/Identifikation) — alle 5 Kategorien mindestens 1x
2. Template aus `hook-framework.md` nehmen
3. Pain-Point aus Trend-Research einbaün (sehr spezifisch!)
4. 5-Regeln-Check (kurz/konkret/spannung/relevant/kein clickbait)
5. Viral-Mechanik-Check (Spannung/Shortcut/Beweis/Identität)

**Spezifitäts-Level (wie Patricia das will):**
- SCHLECHT: „3 Tipps für mehr Energie"
- GUT: „Wie du mit 500 Followern und einer 5-teiligen Story-Sequenz täglich 3 Verkäufe deines 287€-Produkts machst, ohne einmal ‚kauf jetzt' zu sagen"

Jeder Hook muss MESSBAR konkret sein (Zahlen, Zeiträume, spezifische Situationen).

## Schritt 5: 5 Karussell-Entwürfe pro Profil

Aus den 10 Hooks wähle die 5 stärksten pro Profil. Pro Karussell:
- Titel + Profil + Pillar + Folien-Anzahl (Default 9)
- Folien-Plan (siehe karussell-framework.md Template)
- Feed-Aesthetic-Check: letzte 6-9 Designs in Canva-Ordner „Gepostete Beiträge" (via Canva MCP `list-folder-items`) — Cover-Farbe so wählen dass Grid abwechselt
- Caption nach HVC-Formel + Pillar-Keyword aus manychat-keywords.md
- 5 Hashtags
- Asset-Hinweise (Canva-Template / eigene Fotos / Stock)
- Speichern: `outputs/karussells/wochenplan-YYYY-KW##-[profil].md`

## Schritt 6: 5 Reel-Entwürfe pro Profil

Aus den 10 Hooks wähle 5 andere (oder überlappend) für Reels. Pro Reel:
- Titel + Profil + Pillar + Länge (7-15s für Cold Reach / 15-35s für Expertise)
- Reel-Typ (Talking Head / POV / Hot Take / Story / Anleitung)
- Shotlist Sekunde-für-Sekunde (aus reels-framework.md Template)
- Asset-Quelle pro Shot (Canva-Video / Stock / Neu aufnehmen)
- **Video-Bedarf-Flag**: Falls Patricia neu aufnehmen muss — konkrete Dreh-Anweisung mit exaktem Sprech-Text + Setup
- Caption + Keyword + 5 Hashtags
- Speichern: `outputs/reels/wochenplan-YYYY-KW##-[profil].md`

## Schritt 7: Notion-Einträge anlegen

Für JEDEN der 10 Entwürfe pro Profil (5 Karussells + 5 Reels):
- Neue Page in Content-Management-DB (`collection://2ae7078e-8b7e-811a-ad14-000ba5820c09`)
- Felder:
  - Content-Titel: Titel
  - Content-Typ: Reel oder Karussell
  - Status: Idee
  - Content-Plattformen: Relation zu „Instagram Mentoring" oder „Instagram doTERRA"
  - Content-Säule: Relation zur passenden Pillar
  - Storyart: passend (Mythos-Brecher / Persönliche Geschichte / etc.)
  - Ziel: passend (Expertise zeigen / Interaktion / Reichweite / etc.)
  - Keyword: aus manychat-keywords.md
  - Kurzbeschreibung: 1-2 Sätze zum Inhalt
  - Briefing-Link: URL zur MD-Datei
  - Veröffentlichung: leer (wird später nach Freigabe gesetzt)

## Schritt 8: Notification + Zusammenfassung

Erstelle eine Zusammenfassung als `outputs/montags-engine-YYYY-KW##.md`:

- Gesamt: 10 Karussells (5 Mentoring + 5 doTERRA) + 10 Reels (5 + 5)
- Wie viele brauchen neue Video-Aufnahmen? (pro Reel kennzeichnen)
- Wie viele nutzen existierende Canva-Assets?
- Top 3 stärkste Hooks pro Profil
- Trend-Erkenntnisse der Woche
- Offene Fragen an Patricia (falls welche)

Speichere die Zusammenfassung + logge sie am Ende.

## Schritt 9: Mentoring-Profil-Daten

Für Mentoring: Content-Säulen aus Patricias existierender Notion-Content-Strategie:
- „1. Positionierung im Networkmarketing 2.0"
- „2. Businessaufbau mit hybriden Einkommensströmen"
- „3. Mindset & Alltag: Mama, Business, Leadership"
- (+ Persönlichkeit / Inspiration / Expertise als Julia-Trost-Rollen-Tags)

Für doTERRA: Content-Säulen v2 (2026-04-21):
- „doTERRA 1. Der Wake-Up: Wenn dein Körper spricht"
- „doTERRA 2. Mama-Körper ab 35: Was du wirklich brauchst"
- „doTERRA 3. Zurück zu deiner Energie — deine 4 Säulen der Regeneration"
- „doTERRA 4. Mental Load & Stressmanagement"
- „doTERRA 5. Rückkehr zu dir — die neue Mama-Identität"

Pro Woche: min. 3 verschiedene Pillars abdecken pro Profil.

## Pflicht-Qualitätskontrolle am Ende

Bevor Session endet, prüfe:
- [ ] 20 Hooks, jede Kategorie mind. 2x vertreten?
- [ ] Alle Hooks spezifisch (mit Zahlen/Zeiträumen/Situationen)?
- [ ] 10 Karussell + 10 Reel-Briefings erstellt?
- [ ] Alle 20 Einträge in Notion Content-Management-DB angelegt?
- [ ] Feed-Aesthetic-Rotation pro Profil berücksichtigt?
- [ ] Pillar-Rotation über die Woche (min. 3 Pillars/Profil)?
- [ ] Jeder Entwurf hat ManyChat-Keyword?
- [ ] Video-Aufnahmen-Bedarf klar gekennzeichnet?

Am Ende: Notification an Patricia via Output-Zusammenfassung.
```

---

## Testlauf vor Aktivierung

1. Einmal manüll triggern via Claude Code (Prompt copy-paste)
2. Prüfen: Output-Qualität, Notion-Einträge, Asset-Hinweise
3. Feedback einbaün
4. Dann Cron aktivieren

---

_Zuletzt aktualisiert: 2026-04-21_
