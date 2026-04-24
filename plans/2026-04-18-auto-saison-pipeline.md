# Automatisierte Saison-Pipeline für Telegramgruppe

**Erstellt:** 2026-04-18
**Status:** Plan — Umsetzung als nächster Schritt

---

## Kontext

Patricia postet saisonale Beiträge in ihre Telegramgruppe "Gesund durchs ganze Jahr mit ätherischen Ölen":
- 10 Beiträge pro Saison (Frühling, Sommer, Herbst, Winter)
- 1 Beitrag pro Woche über ~10 Wochen
- Inhalte basierend auf Enjoils-Heften + Patricias 5-Säulen-Ansatz

Aktuell macht sie das **manüll**. Zukünftig soll der Bot das komplett automatisieren — Patricia bekommt nur eine DM zum Prüfen und schreibt "OK" zum Freigeben.

## Ziel-Workflow

```
  7 Tage vor Saisonstart
         │
         ▼
  ┌─────────────────────┐
  │ Userbot (Railway)   │ Reminder fired
  │ generiert 10 Posts  │
  │ + Canva-Grafiken    │
  │ + Posting-Plan      │
  └──────────┬──────────┘
             │
             ▼
  ┌─────────────────────┐
  │ Speichert als       │
  │ "pending_approval"  │
  │ in Supabase         │
  └──────────┬──────────┘
             │
             ▼
  ┌─────────────────────┐
  │ DM an Patricia      │
  │ "10 Beiträge bereit │
  │  — schau sie dir an:│
  │  [Canva-Link]       │
  │  Datum 1: 1.6.      │
  │  Datum 2: 8.6.      │
  │  ...                │
  │  Mit 'OK' bestätige │
  │  ich die Pipeline"  │
  └──────────┬──────────┘
             │
  Patricia prüft in Canva,
  editiert Designs, löscht
  schlechte Varianten
             │
             ▼
  ┌─────────────────────┐
  │ Patricia: "OK"      │
  │ (oder "Änderungen:  │
  │  Post 3 umschreiben")│
  └──────────┬──────────┘
             │
             ▼
  ┌─────────────────────┐
  │ Bot: aktiviert      │
  │ Posting-Plan        │
  │ Status: "scheduled" │
  └──────────┬──────────┘
             │
             ▼
  ┌─────────────────────┐
  │ Userbot postet      │
  │ wöchentlich in die  │
  │ Telegramgruppe      │
  │ — automatisch       │
  └─────────────────────┘
```

---

## Komponenten die gebaut werden

### 1. Datenbank-Erweiterung (Supabase Migration 006)

```sql
create table scheduled_posts (
  id uuid primary key default gen_random_uuid(),
  plan_id uuid references content_plans(id),
  season text,            -- 'frühling', 'sommer', 'herbst', 'winter'
  year int,
  post_number int,        -- 1-10
  title text,
  content_markdown text,  -- Post-Text
  canva_design_id text,   -- Link zum Canva-Design
  canva_image_url text,   -- Finales Bild (exportiert)
  telegram_group_id bigint,
  scheduled_for timestamptz,
  status text check (status in ('draft','pending_approval','scheduled','posted','failed')),
  posted_at timestamptz,
  created_at timestamptz default now()
);

create table content_plans (
  id uuid primary key default gen_random_uuid(),
  season text,
  year int,
  status text check (status in ('generating','pending_approval','approved','active','completed')),
  generation_started_at timestamptz,
  approved_at timestamptz,
  telegram_group_id bigint,
  created_at timestamptz default now()
);
```

### 2. Content-Generator (Userbot / Railway)

**Trigger:** Saison-Reminder (7 Tage vor 1. März/Juni/September/Dezember)

**Logik:**
1. Erstellt neuen `content_plans` Eintrag (status=generating)
2. Holt Enjoils-Inhalte aus Supabase (category=product, source_file ilike Frühling/Sommer/...)
3. Für jeden der 10 Beiträge:
   - Claude generiert Text basierend auf Enjoils-Content + 5-Säulen + Patricias Stil
   - Speichert als `scheduled_posts` Eintrag
   - Berechnet `scheduled_for` (1 Beitrag/Woche ab Saisonstart)
4. Setzt `content_plans.status = pending_approval`
5. Triggert DM an Patricia

### 3. Canva Auto-Design

**Challenge:** MCP ist Claude-Code spezifisch. Railway-Userbot braucht direkte Canva API.

**Optionen:**

**A) Canva Connect API (OAuth)**
- OAuth-Flow initial einrichten
- Refresh-Token für Bot speichern
- Bot nutzt Token für designs
- Vorteil: Volle Canva-Power
- Aufwand: ~3-5h Setup

**B) Template-basiert mit Bild-Generierung**
- Bot generiert einfaches Bild mit OpenAI DALL-E 3 oder Replicate
- Kombiniert mit Text-Overlay via Canva-Template-Duplikation
- Vorteil: Einfacher
- Nachteil: Weniger "Mum Life Balance Look"

**C) Hybrid: MCP via Delegation**
- Bot ruft Vercel-Endpoint auf
- Vercel-Endpoint nutzt... eigentlich auch kein MCP
- ❌ Geht nicht

**Empfehlung: A) Canva Connect API**
— Initial-Setup 1x, danach läuft alles auto.

### 4. Canva Connect API Setup (einmalig)

1. Canva Developer Account erstellen (if not exists)
2. Neue App registrieren unter connect.canva.com/developers
3. OAuth redirect URI konfigurieren (Vercel endpoint)
4. Client ID + Secret in Railway env vars
5. Patricia macht 1x OAuth-Flow → Refresh Token wird gespeichert
6. Bot nutzt Refresh Token für alle künftigen Calls

### 5. DM-Approval-Flow (Bot-Chat Erweiterung)

Der bestehende Bot-Chat-Handler wird erweitert:
- Erkennt "OK" wenn ein `pending_approval` Plan existiert
- Erkennt "Änderungen:..." für Modifikationen
- Aktiviert Posting nach Freigabe

### 6. Auto-Posting Scheduler (Userbot)

**Logik (läuft stündlich):**
1. Query alle `scheduled_posts` mit `status=scheduled` und `scheduled_for <= now()`
2. Für jeden Post:
   - Bild herunterladen (aus Canva-Export)
   - Userbot postet in Telegramgruppe (mit Bild + Text)
   - Status auf `posted`, `posted_at` setzen
3. Bei Fehler: `status=failed`, DM an Patricia

### 7. Telegram-Gruppen ID ermitteln

Damit der Bot in "Gesund durchs ganze Jahr" postet, braucht er die Chat-ID.
→ Einmaliger Setup-Schritt: Patricia schreibt dort eine Nachricht, Userbot lauscht mit und speichert die ID.

---

## Phasen-Plan

### Phase 1: Basis (heute)
- [ ] DB-Migration 006
- [ ] `content_plans` + `scheduled_posts` Tabellen
- [ ] Text-Generator in Railway-Userbot
- [ ] Saison-Trigger im Reminder-System
- [ ] DM-Approval-Flow

### Phase 2: Auto-Posting (heute/morgen)
- [ ] Telegram-Gruppen-ID erfassen
- [ ] Userbot postet in Gruppe (per userbot, nicht Bot!)
- [ ] Stündlicher Scheduler
- [ ] Status-Tracking

### Phase 3: Canva-Automation (später)
- [ ] Canva Connect API Setup
- [ ] OAuth-Flow
- [ ] Auto-Design-Generierung
- [ ] Export & Bild-Upload

Phase 3 ist aufwändig — deshalb macht Phase 1+2 zürst Sinn. Patricia bekommt dann automatische Texte + Posting, erstellt Canva-Designs manüll (wie jetzt).

---

## Offene Fragen

1. Ist Canva Connect API ok (braucht einen 10min OAuth-Setup einmalig)?
2. Welche Wochentage/Uhrzeit für Posts? (z.B. immer Montag 09:00)
3. Text-only Posts wenn kein Canva-Bild vorhanden — OK?
4. Bei `failed` status: Retry oder nur DM?
