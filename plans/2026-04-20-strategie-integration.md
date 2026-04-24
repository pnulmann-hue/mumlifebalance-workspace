# Strategische doTERRA-Business-Planung + Bot-Integration

> **Erstellt:** 2026-04-20
> **Status:** Plan approved, noch nicht umgesetzt
> **Umfang:** 4 Phasen (A–D), ~6–8h aufgeteilt auf 3–4 Sessions

## Context

Patricia stagniert bei **~1 Kunde/Monat** (36 direkte Kunden nach 3 Jahren) und möchte gezielt wachsen. Sie hat **alles** in ihrem Kopf — aber **keine dokumentierte, lebende Strategie**, auf die sowohl sie selbst als auch ihr Business-Companion-Bot zurückgreifen können.

**Konkret fehlt:**
- Ein lebendes Strategie-System für **sie als Leaderin** (Jahr → Monat → Woche → Tag), das der Bot proaktiv nutzt
- **Phase 2** des Business Companion (Positionierungs-Workshop für das Team — geplant aber ungebaut)
- Integration von **Social Media** in die doTERRA-Strategie (aktuell entkoppelt)
- Aktuelle **Metriken** (`current-data.md` ist Vorlage, Zahlen fehlen)

**Ziel:** Patricia bekommt parallel (a) ihren Leaderin-Strategieplan und (b) die Phase 2 für ihr Team — beides im Bot verankert, proaktiv gecoacht, mit Social-Media-Integration.

## Patricias Entscheidungen

1. **Ort:** Notion + Markdown (beides — Notion für Lebendiges, Markdown für Stabiles)
2. **Tiefe:** Jahr / Monat / Woche / Tag (ihr bestehendes System)
3. **Fokus:** Parallel — Leaderin-Plan + Team-Companion Phase 2
4. **Coaching:** Proaktiv — Bot schaut rein und meldet sich

## ⚠️ Kritische Vorgabe: Team-Zugriff

**Patricias Team hat Zugriff auf bot.mumlifebalance.ch.** Daher strikte Trennung:

| Kategorie | Inhalt | Zugriff |
|---|---|---|
| `strategy-public` | Positionierungs-Philosophie, Upline-Prinzipien, Coaching-Methoden, Content-Frameworks | ✅ Team (im Companion-Bot) + Patricia |
| `strategy-private` | 40k-Ziele, Umsatzzahlen, OV, persönliche Team-Metriken, Jahresplan, Monats-Fokus, Wochen-Tasks | 🔒 **Nur Patricia** (via Telegram-Bot `@mumlifebalance_collector_bot`) |

**Implementierung:**
- RAG-Filter im Companion-Bot: `category IN ('product', 'business', 'strategy-public')` — niemals `strategy-private`
- Notion-DBs (Jahres-/Monats-/Wochen-Plan) werden direkt via Notion-API gelesen, NICHT in RAG ingestet
- `current-data.md` + Inhalt von `context/strategy/private/` werden NICHT ingestet

---

## Umsetzung in 4 Phasen

### Phase A: Strategie-Fundament dokumentieren (~90 Min)

**A1. Metriken erfassen** — `context/current-data.md` ausfüllen
- Aktueller Rang (Premier laut Genealogy-Daten), OV, Team-Grösse, aktive Direktkunden (32 aktiv laut AC)
- Instagram-Follower, Reichweite, Engagement (1 Referenzmonat)
- Monatsumsatz Stand Q1/Q2 2026

**A2. Leitbild + 40k-Ziel schärfen** — Neue Struktur `context/strategy/`
- `context/strategy/private/2026-leaderin-strategie.md` (privat, nicht ingest)
- Nord-Stern: 40k CHF Jahresumsatz (bereits in `strategy.md`)
- **Wie?** 3 Umsatzsäulen mit Zielbeiträgen (z.B. 45% doTERRA / 35% Kurse / 20% 1:1)
- Kritische Hebel: mehr Direktkunden, mehr qualifizierte Berater, Kurs-Launches
- Verbindung zu Gold-Rang (OV + Leg-Struktur, schon in `doterra-rang-anforderungen-europa.md`)
- `context/strategy/public/positionierungs-framework.md` (wird als `strategy-public` ingestet, Team-safe)

**A3. Notion-Struktur erweitern** — 3 neue Datenbanken in Notion
- **Jahresplan 2026 Business** (Quartals-Themen, 40k-Meilensteine, Gold-Weg)
- **Monats-Fokus** (pro Monat: 1 Hauptthema + 3 Teilziele + Erfolgskriterien)
- **Wochen-Aktivitäten** (KW → Tasks → Status → verknüpft mit Monatsziel)

### Phase B: Bot-Zugriff auf Strategie (~60 Min)

**B1. Neue Wissensbasis-Kategorien** — in Supabase `documents.category`
- Neue Werte: `strategy-public` (Team darf sehen), `strategy-private` (gibt es offiziell nicht im RAG, nur als Policy)
- Keine Migration nötig — `category` ist freies Text-Feld

**B2. Strategie-Dateien ingesten**
- Modify: `C:\Users\pnulm\doterra-bot\scripts\ingest-business.ts` → Kategorie-Parameter + Ordner-Ausschluss (`strategy/private/`)
- Nur `context/strategy/public/*.md` wird als `category='strategy-public'` eingepflegt

**B3. Business System-Prompt erweitern**
- File: `C:\Users\pnulm\doterra-bot\lib\business-system-prompt.ts`
- Neu: RAG-Filter erweitert zu `product`, `business`, `strategy-public`
- Beraterinnen sehen: Positionierungs-Philosophie als Kontext, aber **keine persönlichen Zahlen**

**B4. Notion-Integration vertiefen (Telegram-Bot only)**
- File: `C:\Users\pnulm\doterra-bot\lib\notion.ts` (existiert schon)
- Neue Tools (nur im Telegram-Bot-Chat-Flow verfügbar): `get_current_quarter_focus()`, `get_week_tasks()`, `mark_task_done()`
- Chat-Command im Telegram-Bot: `status` → zeigt aktueller Monats-Fokus + fällige Wochen-Tasks

### Phase C: Phase 2 des Business Companion bauen (~2–3h)

**C1. Neue Schritte 13–23** im geführten Pfad ergänzen
- File: `C:\Users\pnulm\doterra-bot\lib\business-system-prompt.ts` — `GUIDED_STEPS` erweitern
- Phase 2 Module: Diamantpapier-Workshop → Heldengeschichte → Nische finden → Lead-Magnet → Instagram-Profil → Content-Pillars → Erster Launch
- Wissensbasis liefert schon alles: `reference/julia-trost/`, `reference/awaken-a-star/`, `patricias-positionierungs-philosophie.md`

**C2. Content-Coach-Tool in bot-tools.ts**
- File: `C:\Users\pnulm\doterra-bot\lib\bot-tools.ts` (existiert)
- Neues Tool: `content_idea_from_pillar(pillar)` → liefert Reel-Hook, Karussell-Idee, Story-Sequenz
- Basis: `context/hook-framework.md` + Patricias 5 Säulen

### Phase D: Proaktives Coaching (~60 Min)

**D1. Wöchentlicher Strategie-Check-in** (neuer Reminder im Telegram-Bot)
- File: `C:\Users\pnulm\Desktop\Mein Business\scripts\telegram-userbot\src\reminders.ts`
- Jeden **Montag 08:00**: Bot liest aus Notion Monats-Fokus + offene Wochen-Tasks → DM:
  ```
  📌 Dein Monats-Fokus Mai: Instagram-Reichweite verdoppeln
  ✅ Letzte Woche: 4/5 Tasks erledigt
  📅 Diese Woche fällig: 3 Reels, 1 Teamcall, 2 Follow-ups
  ```

**D2. Fortschritts-Nudges**
- Bei stagnierenden Metriken (z.B. 0 neue Kunden in 2 Wochen): Bot fragt "Brauchst du Sparring?"
- Bei 2x übersprungenen Content-Tasks: Bot erinnert mit Content-Idee
- Basis: neue Supabase-Tabelle `weekly_snapshots` (Zahlen-Historie, privat)

**D3. Quartals-Review**
- 1x/Quartal Mega-DM: "Q1 ist rum. Hier deine Zahlen vs. Ziel. Reflexion?"
- Patricia antwortet → Bot speichert in Notion unter "Quartals-Review"

---

## Kritische Dateien

| Datei | Was ändert sich |
|---|---|
| `context/current-data.md` | Zahlen ausfüllen |
| `context/strategy/public/` (neu) | Team-sichere Strategie-Dokumente |
| `context/strategy/private/` (neu) | Patricias private Strategie (NICHT ingestet) |
| `C:\Users\pnulm\doterra-bot\lib\business-system-prompt.ts` | Phase 2 Schritte + Strategie-Kontext-Block |
| `C:\Users\pnulm\doterra-bot\lib\bot-tools.ts` | Content-Coach-Tool + Notion-Helpers |
| `C:\Users\pnulm\doterra-bot\lib\notion.ts` | Quarter-Focus + Week-Tasks Functions |
| `C:\Users\pnulm\doterra-bot\scripts\ingest-business.ts` | Kategorien-Support + Private-Ordner-Ausschluss |
| `scripts/telegram-userbot/src/reminders.ts` | Strategie-Check-in + Nudges + Quartals-Review |

## Bereits vorhandene Bausteine (wiederverwenden)

- **12-Schritte-Pfad** (Phase 1) läuft in `business-system-prompt.ts` ✅
- **Positionierungs-Philosophie**, **Team-Wissen**, **doTERRA-Rang-Anforderungen** in Wissensbasis ✅
- **Notion-Integration** über bestehenden Token + `lib/notion.ts` ✅
- **Telegram-Bot-Chat** mit Tool-Use + RAG ✅
- **Reminders-Infrastruktur** (Teamcall, Saison, Newsletter) ✅

## Verifikation

**Phase A fertig wenn:**
- `current-data.md` hat echte Zahlen
- In Notion existieren 3 DBs (Jahresplan, Monats-Fokus, Wochen-Aktivitäten) mit Einträgen für Q2/Mai/KW18
- `context/strategy/public/` + `context/strategy/private/` angelegt mit Content

**Phase B fertig wenn:**
- Beraterin-Frage im Companion-Bot: "Was ist Patricias Positionierungsansatz?" → liefert Antwort aus `strategy-public`
- Beraterin-Frage: "Was ist Patricias aktueller Umsatz?" → Bot weiss es NICHT (Privacy-Check bestanden)
- Patricia fragt Telegram-Bot `status` → kriegt Monats-Fokus + Wochen-Tasks aus Notion

**Phase C fertig wenn:**
- Business Companion zeigt Schritte 13+ an (in `/dashboard` im Fortschrittsbalken)
- Test-Beraterin durchläuft Schritt "Diamantpapier" und bekommt Workshop-Chat

**Phase D fertig wenn:**
- Nächster Montag 08:00: Strategie-DM kommt
- Simulierte Stagnation → Bot fragt nach
- Quartalswechsel → Review-DM

## Session-Plan zum Umsetzen

| Session | Phase | Zeit |
|---|---|---|
| 1 | A (Metriken + Strategie-Docs + Notion-DBs) | ~90 Min |
| 2 | B (Bot-Zugriff + Category-Filter + Notion-Tools) | ~60 Min |
| 3 | C (Companion Phase 2 + Content-Coach) | ~2–3h |
| 4 | D (Proaktives Coaching + Reminders + Reviews) | ~60 Min |

**Gesamt:** ~6–8h, nach jeder Session ein funktionierender Zwischenstand.

---

## Historie

- 2026-04-20: Plan erstellt in Session nach Newsletter-Pipeline + doTERRA-Kunden-Import
- Original-Plan-File: `C:\Users\pnulm\.claude\plans\ich-w-rde-gerne-mit-warm-seahorse.md`
- User-Entscheidungen via AskUserQüstion dokumentiert
- Team-Zugriff-Policy in `feedback_team-zugriff.md` festgehalten
