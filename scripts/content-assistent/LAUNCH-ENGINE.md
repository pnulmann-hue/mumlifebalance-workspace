# Content-Bot: Launch-Engine + Monatsplan-Anbindung

**Eingebaut:** 2026-06-09 · Löst das Problem „Bot liefert generische Stories statt monats-/launch-basiert".

## Was der Bot jetzt jeden Tag tut

Bei jedem Story-Lauf (06:30-Cron, `/run`, `/run schnell`) lädt `notion_reader.lade_wochen_kontext()` zusätzlich zwei lokale, tagesaktuelle Quellen (kein Notion-Sync nötig, kein API-Key):

1. **`launch_engine.get_story_kontext(heute)`** entscheidet:
   - **Launch aktiv?** → folgt dem **Julia-Launchkalender**: zieht aus dem materialisierten
     `outputs/produkte/**/story-plan.json` den Tageseintrag (Phase + feste Julia-Vorlage + Ziel + CTA)
     und reichert ihn mit der Vorlagen-Anleitung aus `context/julia-launch-kalender.json` an.
   - **Kein Launch?** → wählt eine **Julia-Storyvorlage** aus `context/julia-story-vorlagen.json`
     (Wochentag-Rotation, 3 Säulen Expertise/Inspiration/Persönlichkeit), CTA auf ein 0€-Freebie.
2. **`monatsplan_reader.lade_monatsplan(heute)`** liest den verbindlichen Plan aus
   `outputs/monatsplaene/[YYYY-MM]-mentoring-monatsplan*.md` (neueste Version gewinnt → v2 schlägt v1),
   extrahiert Wochen-Pillar + KW-Block + heutigen Tagesslot.

Beides wird in `claude_caller.build_user_prompt()` + `generate_briefing_anfrage()` injiziert.
**Prioritäts-Reihenfolge:** Patricia-`/fokus`-Override > Launch-Plan > Monatsplan-MD > Notion.

Bei aktivem Launch setzt `resolve_profil()` automatisch das Launch-Profil (mentoring),
ausser Patricia gibt per `/run mentoring|doterra` explizit eines vor.

## Wenn ein NEUER Launch kommt

1. Lege `outputs/produkte/<launch>/story-plan.json` an (Vorlage: `mba-launch/story-plan.json`).
   Felder pro Tag: `datum`, `phase`, `julia_vorlage` (Schlüssel aus `julia-launch-kalender.json`),
   `titel`, `story_ziel`, `kaeufertyp`, `cta`, `cta_keyword`, `profil`.
2. Phasen-Fenster (`phasen.aufwaermphase/verkaufsphase/nachkaufphase` mit `von`/`bis`) setzen.
3. Fertig — `launch_engine` entdeckt jeden `story-plan.json` unter `outputs/produkte/**` automatisch
   (Dateien mit „archiv" im Namen werden ignoriert). Optional explizit in `config.LAUNCH_STORY_PLANS`.

## Testen (ohne API-Key)

```
cd scripts/content-assistent
python launch_engine.py 2026-06-29     # Phasen-Durchlauf + Prompt-Block für ein Datum
python monatsplan_reader.py 2026-06-09 # zeigt erkannten Monatsplan + Tagesslot
```

## Deploy (Railway)

Die neuen Dateien müssen committet sein, dann Railway-Redeploy. Der Bot liest Context/Outputs
über `config.WORKSPACE_ROOT` (= Repo-Root) — dieselbe Mechanik wie die bestehende Pflicht-Lese-Liste.

## Dateien

| Datei | Rolle |
|---|---|
| `launch_engine.py` | Launch-Erkennung + Vorlagen-Auswahl + Prompt-Block |
| `monatsplan_reader.py` | Liest Monatsplan-MD (Single Source of Truth) |
| `context/julia-launch-kalender.json` | Julia-Phasen + Vorlagen-Anleitungen (Launch) |
| `context/julia-story-vorlagen.json` | Julia-Vorlagen-Rotation (Nicht-Launch) |
| `outputs/produkte/mba-launch/story-plan.json` | Materialisierter Bootcamp-Launch 15.6.–9.7. |
