# Stand Ende Tag — 2026-04-30

**Letzte Session:** 30.04.2026 (Mittwoch)
**Nächste Session:** 01.05.2026 (Donnerstag) — Patricia plant `/freitag-hooks` als nächsten Skill

---

## ✅ Was heute fertig wurde

### 1. Story-Skill (`/story`) komplett live

**Skill-Datei:** `.claude/commands/story.md`
- 8 Modi (Tagesplan / Sales-Day / Story-Doktor / One-Slide / Story-Serie / BTS / Highlight-Pflege / Reaktiv)
- **Hook-Knall-Pflicht** als verbindliche Regel (NIE „Guten Morgen / hab grad / sitze grad")
- **6-Punkte-Voice-Check** vor jedem Render
- **Pflicht-Lookup vor Produkt-Erwähnung** (active-funnels.json + patricia-freebies.md)
- **Julia-Templates verbindlich** (10 Stück, alle dokumentiert)

### 2. Scheduled Task `daily-story-render`

- **Cron:** Mo-So 06:34 Europe/Zurich
- **Pfad:** `C:\Users\pnulm\.claude\scheduled-tasks\daily-story-render\SKILL.md`
- **Doku:** `reference/scheduled-task-daily-story-render.md`
- **Ablauf:** Telegram-Frage 06:34 → Patricia-Sprachnotiz → Whisper → Julia-Template-Match → 6-8 Slides → Voice-Check → Render → Telegram-PNG-Versand

### 3. Wissensbasis (alle in `context/`)

| File | Inhalt |
|---|---|
| `saeulen-mentoring.md` | Patricias 3 Säulen (Networkmarketing 2.0 / Hybridmodell / Mama Business) + Hauptprodukte + Quellen-Mapping |
| `julia-stories-die-verkaufen.md` | Slide-Struktur + 7 Storytelling-Regeln |
| `julia-insta-stories-anleitung.md` | 10 Verkaufs-Templates |
| `julia-story-ideen.md` | 3-Säulen-Bibliothek (Expertise/Inspiration/Persönlichkeit) |
| **`julia-launch-kaeufertypen.md`** (NEU) | **Julia 6 Launch-Käufertypen — Willi/Amelie/Ina/Frank/Rudi/Zoe + Wochenrotation für Launches** |
| `brandastic-kaeufertypen.md` | DISG + AIDA |
| `nadja-story-prompts.md` | 7 Käuferpersonas (Sample) |
| `story-framework.md` | Zentrales Story-Wissen |
| `notion-content-planung.md` | Notion-Lese-Logik (Monatsplan + Wochenplan + Themenplanung) |

### 4. Visual-Pipeline

- **`scripts/karussell-render/brand-stories.css`** — 8 Slide-Templates + **Foto-Schutz-Safe-Zones**
- **`scripts/karussell-render/render-stories.js`** — bereits dynamisch, rendert 1080×1920 PNGs
- **`scripts/content-bot/telegram-send.js`** — erweitert um `sendPhoto` + Mediagroup

### 5. Memory-Regeln (global, skill-übergreifend)

- `feedback_hook-knall-pflicht.md` — Slide 1 / Reel-Cover / Caption-Anfang NIE Begrüssung
- `feedback_pflicht-lookup-vor-produkt-erwaehnung.md` — Bevor Produkt genannt: active-funnels.json + freebies/expertise lesen
- `feedback_foto-schutz-overlays.md` — Sticker/Text NIE über Hauptmotiv
- `feedback_story-skill-regeln.md` — CTA + Käufertyp-Rotation
- `project_story-skill.md` — Skill-Status

### 6. Test-Lauf erfolgreich (Bio-Check Story)

**8 Slides gerendert + via Telegram an Patricia gesendet:**
- Pfad: `outputs/stories/2026-04-30-tagesplan-mentoring-bio-check/slides-png/`
- Slide 5 mit echtem Foto (Patricia mit Pusteblume)
- Korrigiert über 3 Iterationen: „Bug" → „Und genau da verlierst du" · Petrol → Orange auf Dunkelblau · Sticker-Layout entzerrt

### 7. Plan-Doc + Drive

- Plan: `plans/2026-04-30-story-skill.md`
- Drive: 3 Dokumente in „Claude Code Mastery Transkripte"-Ordner (Übersicht + Brand Voice + Werbeanzeigen)

---

## ⏳ Was offen ist (für nächste Sessions)

### Lücken in der Wissensbasis (Patricia will alle drin)

| Lücke | Status | Priorität | Aufwand |
|---|---|---|---|
| Nadja Grunenberg Volltext (98 Seiten) | ⚠️ nur Sample | Mittel | ~30 Min |
| Julia Vorlagen Story LML.pdf (119 MB) | ❌ nicht extrahiert | Hoch | ~1-2 h (OCR) |
| Julia Instagram Story Strategie 2.0 (28 Transkripte-Ordner) | ❌ nicht extrahiert | Hoch | ~2-3 h |
| Julia Minikurse Story.pdf | ❌ Bild-PDF, OCR nötig | Niedrig | skip empfohlen |

### Skills die noch fehlen (Skill-Pyramide vervollständigen)

```
/monatsplan (NEU)            → 1× pro Monat
   ↓ schreibt Säule + 3 Produkte (0€/Mini/Gross) in Notion-Monatsplan
   ↓
/freitag-hooks (NEU)         → Jeden Freitag 08:00
   ↓ Marktrecherche zur Säule der Woche + 3 Karussells + 2 Reels + Telegram-Push
   ↓
/daily-story-render          → Mo-So 06:34 ✅ LÄUFT
```

### Klärungsfragen für nächste Session

**Vor `/freitag-hooks`-Build:**
1. Skill-Name `/freitag-hooks` oder anders?
2. `/montag-hooks` umbenennen zu `/freitag-hooks` oder parallel?
3. Block-Verteilung: Variante A (KW1=0€ / KW2=Mini / KW3-4=Gross) oder B (Tag-für-Tag-Mix)?
4. Konkurrenz-Profile pro Säule (Patricia liefert IG-Profile)
5. Hashtag-Pools pro Säule (Patricia bestätigt oder korrigiert)

**Vor `/monatsplan`-Build:**
1. Skill-Name `/monatsplan` oder anders?
2. Trigger: A (manuell) / B (Cron 25.) / C (Hybrid)?
3. Konversations-Channel: Claude-Code-Chat oder Telegram?

**doTERRA-Notion-Klärung:**
- Patricia hat gesagt: doTERRA wird auch im Content-Bot + auch über Notion geplant. Jahresplanung im selben Notion.
- → Nächste Session: Profil-Property in Notion-Wochenplan + Jahresplanung-DB ID rausfinden + Skill so erweitern dass beide Profile sauber filterbar sind

### Notion-Erweiterungs-Vorschlag (Patricia muss machen)

In **Monatsplanung-DB** Properties ergänzen:
- `Säule des Monats` (Select 1/2/3)
- `0€-Produkt` (Text)
- `Mini-Produkt` (Text)
- `Grosses Produkt` (Text)
- `Block-Verteilung` (Text)
- `Profil` (Select Mentoring/doTERRA — falls beide Profile gemeinsam geplant)

---

## 🚀 Was morgen früh passiert

**06:34 (automatisch):**
- `daily-story-render` Cron läuft
- Du bekommst Telegram-Push: „Guten Morgen! Heute: [Thema]. Was war heute / gestern bei dir?"
- Du antwortest mit Sprachnotiz oder Text
- Skill rendert 6-8 Slides nach Julia-Template
- PNGs landen per Telegram bei dir + in `outputs/stories/`

**Wenn etwas schiefgeht:**
- Wochen-Vorwahl fehlt (kein `/freitag-hooks` gelaufen) → Skill fragt direkt nach Profil + Produkt
- Notion-Wochenplan KW 18 ist Garten → Skill nimmt Monatsziel als Fallback ODER fragt
- Erste Tools-Permissions sind noch nicht erlaubt → Skill kann pausieren

**Patricia kann auch:**
- Heute Abend / morgen früh die Bio-Check-Story posten (PNGs sind ready)
- Quiz-Sticker auf Slide 6 ergänzen (4 Bio-Optionen)
- Link-Sticker auf Slide 8 ergänzen (`mumlifebalance.ch/bio-check`)

---

## 📋 Session-Start-Checklist für morgen

1. `/prime` ausführen (lädt CLAUDE.md + context)
2. Diese Status-Datei lesen: `plans/2026-04-30-status-ende-tag.md`
3. Memory-Eintrag prüfen: `project_story-skill.md`
4. Wenn nächster Skill `/freitag-hooks`: 5 Klärungsfragen oben beantworten

---

_Schluss-Notiz: Patricia ist fertig für heute. Story-Skill ist Test-erfolgreich. Alles gespeichert. Morgen geht's weiter mit dem nächsten Skill._
