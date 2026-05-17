# Wochenplan KW 20 (12.–18. Mai 2026)

**Erstellt:** 2026-05-11 (Montag, manuell statt Auto-Skill)
**Wochenfokus:** Mama-CEO-Mastermind + kostenloses Webinar daraus

---

## 📅 Posting-Schedule (Blotato)

| Tag | Zeit | Profil | Format | Inhalt | Datei |
|---|---|---|---|---|---|
| **Mo 11.05.** | (bereits gepostet) | 🔵 Mentoring | Reel | (eigener Reel, nicht aus diesem Pool) | — |
| **Mo 11.05.** | 21:30 | 🟠 doTERRA | Reel | **D9** — Schlaflos + Haare + Augen + Transformation | (manuell drehen, Skript im Chat) |
| **Di 12.05.** | 19:30 | 🔵 Mentoring | Karussell (8 Slides) | **M3** — Spital + System hält | [`2026-05-12-mentoring-m3-spital-system.md`](../karussells/2026-05-12-mentoring-m3-spital-system.md) |
| **Mi 14.05.** | 19:30 | 🔵 Mentoring | Reel | **M6** — Teilzeit + paar hundert + Weg raus | (drehen aus Hooks-Datei) |
| **Mi 14.05.** | 21:30 | 🟠 doTERRA | Karussell (9 Slides) | **D1** — Convention-Haarbürste | [`2026-05-14-doterra-d1-convention.md`](../karussells/2026-05-14-doterra-d1-convention.md) |
| **Do 15.05.** | 19:30 | 🔵 Mentoring | Karussell (8 Slides) | **M2** — Trainingshose | [`2026-05-15-mentoring-m2-trainingshose.md`](../karussells/2026-05-15-mentoring-m2-trainingshose.md) |
| **Fr 16.05.** | 19:30 | 🔵 Mentoring | Reel | **M9** — 5:15 + Pancakes + Bali-Kontrast | (drehen aus Hooks-Datei) |
| **Sa 17.05.** | 21:30 | 🟠 doTERRA | Karussell (8 Slides) | **D2** — 4 Säulen | [`2026-05-17-doterra-d2-vier-saeulen.md`](../karussells/2026-05-17-doterra-d2-vier-saeulen.md) |

---

## 📦 Posting-Bilanz

**Mentoring (@mumlifebalance):** 5 Posts
- 1 Reel (Mo, schon gepostet)
- 1 Karussell (Di)
- 1 Reel (Mi)
- 1 Karussell (Do)
- 1 Reel (Fr)

**doTERRA:** 3 Posts
- 1 Reel (Mo, heute drehen)
- 1 Karussell (Mi)
- 1 Karussell (Sa)

**Gesamt: 8 Posts in KW 20.**

---

## 🤖 GitHub Action: `/montag` Build & Schedule

**Bei der Auslösung des Workflows passiert Folgendes:**
1. Lädt `context/patricia-vollprofil.md` (1322 Zeilen) — Pflicht-Lese ist verdrahtet ✓
2. Lädt Hooks aus `outputs/freitag/2026-05-11-hooks.md`
3. Lädt 4 Karussell-Briefings aus `outputs/karussells/`
4. Generiert Canva-Designs aus den 4 Karussell-Files (via Canva-MCP / API)
5. Pushed zu Blotato mit dem obigen Schedule
6. Reels-Slots bleiben **manuell** (Patricia dreht selbst — kein Auto-Push)

**Verfügbare GitHub Secrets (laut CLAUDE.md):**
- `BLOTATO_API_KEY` ✓
- `NOTION_TOKEN` ✓
- `ANTHROPIC_API_KEY` ✓
- ggf. Canva-Tokens (prüfen)

**Auslösung manuell:**
1. GitHub → Repo → Actions
2. Workflow „Montag Build" auswählen
3. „Run workflow" Button → Branch `main` → Run
4. Status-Tab beobachten (sollte 3-8 Min dauern)
5. Bei Erfolg: Blotato-UI prüfen — Posts müssen für die Slots oben angelegt sein

**Falls Fehler:**
- Action-Logs lesen
- Häufig: Canva-Token-Refresh nötig
- Oder: Blotato Account-IDs fehlen → Halb-Automatik (siehe `reference/blotato-setup.md`)

---

## ⚠️ Falls GitHub Action nicht funktioniert (Fallback)

Manueller Workflow:
1. Karussell-Files lesen → Slides in Canva designen (Brand-Master-Templates)
2. PNG-Export
3. In Blotato-UI manuell hochladen + Schedule setzen
4. Reels: Patricia dreht selbst aus den Hooks-Skripten

---

## 🔒 Audit-Übersicht (alle 4 Karussells)

**Patricia-Anker-Total:** 12+ konkrete Anker aus Vollprofil
**Erfundene Zahlen:** 0 ✅
**Brand-Voice-Verbote eingehalten:** ✅ (kein „Implementer-DNA", kein „Manifestieren", kein „6-stellig" als Positiv-Frame)
**doTERRA-Compliance:** ✅ alle Hooks im „bei mir war's"-Frame, keine Heilversprechen
**Mama-Spital-Compliance:** ✅ nur „familiär", keine „Mama"/„Krebs"-Erwähnung
**Family-Reality:** ✅ alle Kinder Schulalter (keine Kita-Frames)
**Blotato-Limit max 10 Slides:** ✅ alle Karussells 8-9 Slides
