# Mama-CEO — Handoff für nächste Session

**Stand: 2026-04-30 abends · Patricia geht schlafen**

---

## Patricias Auftrag für die nächste Session

> „Ich möchte gerne, dass du den gesamten Kursaufbau nochmals von 0 prüfst anhand der neuen Unterlagen und auch die Marktrecherche nochmals sauber machst und mir das Ergebnis zeigst."

**Heißt konkret:** Re-Evaluation des Mama-CEO-Kurses (Briefing, Markt-Research, Modul-Outline, Validierungs-Plan) — diesmal **fundiert mit den heute eingetroffenen Mentoren-Quellen**, nicht aus der Hüfte.

---

## Was heute (2026-04-30) erreicht wurde

### Mentoren-Wissensbasis ist endlich auf GitHub

Nach längerem Push-Theater (4.32 GB → reduziert auf 950 MB durch Auslassen der 9 Files >100 MB) liegen jetzt **245 Files** im Repo unter `reference/`:

| Mentor | Files | Inhalt |
|---|---|---|
| **Aurachirurgie** | 34 | Geld-Mindset-Transkripte (Geld kreieren, Ich bin diszipliniert, Universum kennt kein nein, Aurafeld Cleaning, Disziplin-Mindset etc.) |
| **Brandastic** | 18 | Brand Story Maxi, Epiphany Bridge Skript, Markenkern, Persönlichkeitstypen + AIDA, Email-Sequenzen, Webinar-Vorlage, Hook/Headline-Beispiele |
| **Elke Mayr** | 45 | Contentselling (4 Module + 6 Baukästen), Teamaufbauchallenge (30 Tage), Finde dein Thema fürs Network |
| **Karriere Mum** | 29 | Workbooks: Zielgruppe, USP, Elevator-Pitch, Wertekompass, Glaubenssätze, MoneyMindset, Manifest, Hütchenspiel, Eisenhower-Pareto, Habit-Tracker, Hashtagwunder |
| **awaken a star** | 63 | Sales-Skript ATS, Lieblingskundin, Hölle-Himmel-Avatar, SPIN, Einwandbehandlung, Heldengeschichte, Werbetexte, Kommunikationskompass |
| **Networkmarketing-Training** | 6 | 5-Tage-Workbook + Fahrplan |
| **Workbookkurs** | 9 | Rauhnächte-Material (Sonja Kopplin) |
| **Nadja Grunenberg** | 3 | Social Media Kalender + Story Prompts |
| **GO VIRAL** | 3 | Präsentations-PDFs (ohne den 104 MB Workbook Reel) |
| **julia-trost** | komplett <100 MB | 30+ PDFs + 818 Transkripte + methodik.md |

### Was NICHT im Repo ist (Files >100 MB — GitHub-Limit)

Diese 9 Files liegen nur auf Patricias Desktop (`C:\Users\pnulm\Desktop\Mein Business\reference\`):

- `GO VIRAL/GO VIRAL - Workbook Reel.pdf` (104 MB)
- `julia-trost/Launch Queen.pdf` (1.4 GB) ← Riesen-File, vermutlich Video-Aufzeichnung
- `julia-trost/Launch Queen (1).pdf` (1.1 GB)
- `julia-trost/alle unterlagen julia trost.pdf` (235 MB)
- `julia-trost/Das ultimative VML Workbook.pdf` (218 MB)
- `julia-trost/Vorlagen Story LML.pdf` (149 MB)
- `julia-trost/31_Verkaufsstrategienneu[1].pdf` (149 MB)
- `julia-trost/Produktkommunikation - Produkttreppe_Zusammenführen.pdf` (127 MB)
- `julia-trost/Launch queen workbook.pdf` (113 MB)

**Lösung dafür: Lokales Claude Code Setup auf Patricias PC** (nicht heute geschafft):
1. Node.js LTS von https://nodejs.org/ installieren
2. PowerShell: `npm install -g @anthropic-ai/claude-code`
3. PowerShell: `cd "C:\Users\pnulm\Desktop\Mein Business"` → `claude` starten
4. Dann hat Claude direkten Filesystem-Zugriff auf alle Riesen-Files

### Branch-Status

- **`main`** — `533af24 Mentoren-Wissensbasis ohne Files >100 MB` (gepusht ✅)
- **`claude/build-product-page-WjrId`** — `2a4a54f Merge remote-tracking branch 'origin/main'` (gepusht ✅)

Auf dem WjrId-Branch arbeiten wir am Mama-CEO. Mentoren sind dort verfügbar.

### Bereits vorhandene Mama-CEO-Materialien (werden geprüft, nicht verloren)

- `00-briefing.md` — umfangreich (Transformation, Avatar, Format, Preise, Umsatz-Beitrag)
- `00-markt-research.md` — 139 Zeilen (DACH-Mama-Quellen, vor Mentoren-Zugriff erstellt)
- `01-modul-outline.md` — 251 Zeilen (5 Module, 23 Lektionen, Aufnahme-Plan, Pilot-Empfehlung Modul 1)
- `02-validierung.md` — 386 Zeilen (Story-Umfrage + DM-Sequenz)

Diese Dateien werden in der Re-Evaluation **geprüft + ggf. überarbeitet**, nicht überschrieben.

---

## Plan für die nächste Session

**Empfohlener Einstieg:** Patricia tippt `/produkt` oder ich starte direkt mit dem Re-Eval.

### Phase 1 — Mentoren-Quellen sichten (5 Agents parallel, ~10 Min)

1. **Karriere Mum** — Avatar-Tiefe, USP-Methodik, Mindset-Übungen, Inhalts-Risiko (Dopplung)
2. **Brandastic** — Brand-Story-Frame, Epiphany-Bridge-Storytelling, Käufertypen + AIDA
3. **awaken a star** — Avatar (Hölle/Himmel), Lieblingskundin, Sales-Skript, SPIN, Einwandbehandlung
4. **Aurachirurgie** — Geld-Mindset-Reframes (für Modul 5 / Bonus)
5. **Elke Mayr + Networkmarketing-Training** — Network-spezifische Logik (Contentselling, Teamaufbau, 5-Tage-Mindset-Sprint)

### Phase 2 — Markt-Research 2026 neu (WebSearch, ~10 Min)

- Aktuelle 2026-Trends DACH-Mama-Solopreneurs
- KI-für-Mamas-Trend (Patricias USP-Anker)
- Mental-Load + Burnout 2026 (Update zu früheren Quellen)
- Reddit/Foren: was googelt die Zielgruppe?
- Konkurrenz-Check: DACH-Mama-Coaches mit ähnlichem Angebot (Mama-CEO/Operations/KI)

### Phase 3 — Synthese (Schreibarbeit, ~30 Min)

- `00-markt-research.md` **neu** schreiben (mit Mentoren-Quellen-Belegen + 2026-WebSearch)
- `00-briefing.md` **prüfen** — wo Inputs aus Mentoren das Bild schärfen, einarbeiten
- `01-modul-outline.md` **prüfen** — passt die 5-Modul-Struktur noch? Hero-Modul richtig? Lektions-Tiefe stimmig mit Mentoren-Methodik?
- **Diff-Empfehlung** für Patricia: alt vs. neu, was ändert sich, was bleibt, warum

### Phase 4 — Patricia-Review

Patricia bekommt die neue Version + Diff vorgelegt, freigibt oder ändert.

---

## Wichtige Open Items (über Mama-CEO hinaus)

1. **Lokales Claude Code Setup** (15 Min) — gibt Patricia dauerhaften Vollzugriff auf ihren Desktop für mich, ohne Push-Theater. Nodes.js installieren ist Schritt 1.
2. **9 Riesen-Files** (>100 MB) bleiben aussen vor, bis Lokal-Setup steht — oder wir nutzen Git LFS später (kostet ~5 USD/Monat).

---

## Tonfall-Notiz für Patricia

Patricia hat heute viel Frustration durchlebt (Push-Theater, OneDrive-Locks, PowerShell-Zickereien). Beim Wieder-Einstieg morgen: **direkt loslegen, kein „erinnerst du dich?"** — sie weiss es noch. **Erstes Output: ein klares „Was hab ich heute zu liefern"** in 3-5 Zeilen, dann legt sie los oder gibt frei.
