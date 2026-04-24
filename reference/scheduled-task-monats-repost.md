# Scheduled Task: Monats-Repost-Engine

**Name:** `monats-repost-engine`
**Schedule:** Jeden 1. Monatstag 08:00 Europe/Zurich (Cron: `0 8 1 * *`)
**Modell:** Sonnet
**Zweck:** Best-Performer des letzten Monats erkennen, adaptieren, reposten.

---

## Regel (von Patricia bestätigt)

**2 Reposts pro Profil pro Monat** (1 Reel + 1 Karussell) = **4 Reposts total/Monat**.

---

## Prompt

```
Du bist die Monats-Repost-Engine. Erkenne die Best-Performer des letzten Monats und plane adaptierte Reposts.

## Schritt 1: Kontext laden
- `context/reels-framework.md` — 4-Wochen-Repost-Regel + Kriterien
- `context/karussell-framework.md` — Karussell-Spezifika
- `context/hook-framework.md` — Hook-Pflicht-Prozess für neue Hooks
- `context/caption-formeln.md`
- `context/manychat-keywords.md`

## Schritt 2: Posts des letzten Monats auslesen (Notion)
Query Content-Management-DB (`collection://2ae7078e-8b7e-811a-ad14-000ba5820c09`):
- Filter: Status = „Veröffentlicht"
- Filter: Veröffentlichung zwischen Datum-30d und Datum-4d (4 Wochen plus ein bisschen Puffer)
- Gruppieren nach Profil (Content-Plattformen-Relation)

## Schritt 3: Best-Performer pro Profil ermitteln

**Kriterien (pro Post):**
Mindestens 2 davon erfüllt = Repost-Kandidat:
- Saves > Durchschnitt der letzten 10 Posts des Profils
- Shares > Durchschnitt der letzten 10 Posts
- DMs via Keyword > 3
- „3-Sek-Hold-Rate" (aus IG-Insights) > 60%
- Completion-Rate > 40%

**Hinweis**: Performance-Daten in der DB sind Text-Felder (Ansichten/Reichweite, Gespeichert, Shares, Kommentare). Parse sie als Zahlen; wenn leer, prüfe ob User noch nachtragen muss.

**Pro Profil**:
- **1 Reel**: Best-Performer-Reel mit höchsten kombiniert-Saves+Shares
- **1 Karussell**: Best-Performer-Karussell mit höchsten Saves

Gesamt: 2 Reels + 2 Karussells = 4 Repost-Kandidaten.

## Schritt 4: Repost-Kandidat vorbereiten (pro Post)

### 4.1 Original-Briefing laden
Aus Notion-Eintrag: Briefing-Link auslesen → Briefing-MD-File in `outputs/reels/` oder `outputs/karussells/` lesen.

### 4.2 Neue Adaption generieren

**Anpassungen (Pflicht — keine 1:1 Kopie, Originality-Score!):**

1. **Neuer Hook** (nach `hook-framework.md`-Pflicht-Prozess):
   - Andere Kategorie als Original, ODER anderes Template aus gleicher Kategorie
   - Gleiches Kern-Thema, andere Verpackung

2. **Neue Caption**:
   - Andere Caption-Formel als Original (aus `caption-formeln.md`)
   - Optional: „Dieser Post hat im [Monat] X Saves gemacht — ich repost ihn, weil so viele ihn verpasst haben." als Stärke-Punkt
   - Gleicher ManyChat-Keyword wie Original

3. **Neuer Sound** (bei Reels):
   - Aktueller Trending-Sound (via WebSearch nach Trend-Sounds für Mamas/Wellness/Business)
   - ODER: gleicher Sound, anderer Cut

4. **Neue Cover-Farbe** (bei Karussell):
   - Feed-Aesthetic-Check: aktuelle Grid-Farben prüfen (letzte 6-9 Designs)
   - Cover-Farbe so wählen dass Rotation weitergeht

5. **Neue Hashtag-Kombination**:
   - 3-5 Hashtags austauschen (aus Pool in `reels-framework.md`)

### 4.3 Repost-Briefing speichern
Als `outputs/reels/reposts/YYYY-MM-[slug]-repost.md` ODER `outputs/karussells/reposts/...`.

Inhalt:
- Link zum Original-Briefing
- Original-Performance (Saves/Shares/etc.)
- Repost-Anpassungen (was genau geändert?)
- Neuer Shotlist/Folien-Plan
- Neue Caption + Keyword + Hashtags
- Empfohlenes Posting-Datum (2-3 Wochen nach Monatsstart)

### 4.4 Notion-Eintrag anlegen (als neues Karussell/Reel mit Repost-Kennzeichnung)
Neue Page in Content-Management-DB:
- Content-Titel: „[Repost] <Original-Titel>"
- Content-Typ: Reel oder Karussell
- Status: Idee
- Content-Plattformen: gleich wie Original
- Content-Säule: gleich wie Original
- Recycling Content-Relation: Link zum Original-Eintrag
- Briefing-Link: URL zum Repost-MD-File
- Kurzbeschreibung: „Repost vom [Original-Datum]. Original-Performance: Saves X, Shares Y."

## Schritt 5: Canva-Design vorbereiten (optional)

Falls Canva-MCP verfügbar:
- Original-Design duplizieren
- Neue Cover-Farbe setzen
- Neuer Hook-Text oben
- Duplikat in Posting-Queue-Ordner legen (automatisch Teil des Freigabe-Flows)

Falls nicht automatisierbar: Anweisung für Patricia im Briefing („Duplizier in Canva: Original XYZ, ändere Cover zu Farbe Z, ersetze Hook-Text").

## Schritt 6: Zusammenfassung

Output-File: `outputs/monats-repost-YYYY-MM.md`

- 4 Repost-Kandidaten mit Original-Performance + Adaptionen
- Woher wurden sie gewählt (Kriterien erfüllt)
- Posting-Plan (wann jeder Repost zur Queue kommt)
- Falls weniger als 4 Kandidaten die Kriterien erfüllen: weniger Reposts, Notification an Patricia mit Grund

## Pflicht-Qualitätskontrolle

- [ ] Max 4 Reposts insgesamt
- [ ] Jeder Repost hat neuen Hook (nach 4-Schritt-Prozess)
- [ ] Jeder Repost hat neue Caption (andere Formel)
- [ ] Karussell-Reposts haben neue Cover-Farbe (Feed-Aesthetic)
- [ ] Notion-Einträge angelegt mit Recycling-Relation
- [ ] Briefing-Files gespeichert
- [ ] Originality-Score gewahrt (keine 1:1-Kopien)
```

---

_Zuletzt aktualisiert: 2026-04-21_
