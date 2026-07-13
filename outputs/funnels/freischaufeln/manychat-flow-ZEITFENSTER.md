---
tags: [funnel, freischaufeln]
---

# ManyChat-Flow: Keyword `ZEITFENSTER`

**Funnel:** Freischaufeln (0€-Tool) · **Profil:** Mentoring (@mumlifebalance)
**Ziel:** Kommentar/DM „ZEITFENSTER" → Landing `mumlifebalance.ch/freischaufeln` (E-Mail-Lead) → Tool → geschütztes Business-Zeitfenster.
**Erstellt:** 2026-07-13

---

## 🔑 Keyword
- **Keyword:** `ZEITFENSTER` · Trigger words: `ZEITFENSTER`, `zeitfenster`, `Zeitfenster`
- **Match type:** Exact match
- **Konflikt-Check:** ✅ kein Konflikt mit bestehenden Keywords (SYSTEM · FAHRPLAN · QUIZ · PRODUKT · THEMA · SICHTBAR · ANLEITUNG · LEAD · ECHT1 · STORY · BIO · ENERGIE)

---

## Flow

### Block 1 — Begrüssung (DM sofort)
```
Hey {{first name}}! 🙌

Du hast ZEITFENSTER kommentiert — hier ist dein kleines Tool.

Du kippst deine typische Familien-Woche rein, es geht sie mit dir durch, halbiert die Liste (was weg darf, was jemand anderes übernimmt, was sich zusammenlegen lässt) und schaufelt dir am Ende ein festes Zeitfenster fürs Business frei.

Dauert ein paar Minuten und kostet 0 CHF.

Tipp kurz auf den Button, dann legst du los ⬇️
```

### Block 2 — Button
- **Text:** `Mein Zeitfenster holen 🚀`
- **URL:** `https://mumlifebalance.ch/freischaufeln?utm_source=instagram&utm_medium=manychat&utm_campaign=freischaufeln&utm_content=dm-keyword-zeitfenster`
- Link-Tracking: ON

### Block 3 — Tag + Custom Field
- Tag: `freischaufeln-lead-manychat` (in ManyChat anlegen)
- Custom Field: `freischaufeln_dm_sent_at` = {{current date/time}}

### Follow-up nach 2h (wenn Link NICHT geklickt)
```
Hey nochmal 👋

Du hattest mir vorhin ZEITFENSTER geschrieben — ich hoffe, der Link ist nicht untergegangen.

Hier nochmal direkt: https://mumlifebalance.ch/freischaufeln

Ehrlich, die paar Minuten sparen dir danach die ganze Woche das „ich komm ja doch nie dazu". Wenn deine Liste dich grad wieder auffrisst — genau dafür ist es. 💛

Fragen? Antworte einfach hier, ich bin da.
```
→ danach Tag `freischaufeln-reminder-sent`.

### Public Comment Auto-Reply (3 Varianten rotieren)
1. „Hab dir grad geschickt ✨"
2. „Check deine DMs 👀"
3. „Ist unterwegs zu dir 💌"

---

## Setup-Checkliste (vor KW29-Lead-Posts)
- [ ] Keyword-Rule `ZEITFENSTER` in ManyChat (Mentoring-Account, Exact match)
- [ ] DM-Flow (Block 1 + Button + Tag) gebaut
- [ ] Follow-up-Flow nach 2h
- [ ] Public Comment Auto-Reply aktiv
- [ ] **Selbst getestet:** Kommentar „ZEITFENSTER" → kommt die DM mit Link an?
- [ ] Landing `mumlifebalance.ch/freischaufeln` → AC-Formular feuert → Auslieferungs-Mail mit Tool-Link
- [ ] Tags `freischaufeln-lead-manychat` + `freischaufeln-reminder-sent` angelegt

---

## 🛑 Keyword-Rotation
`ZEITFENSTER` ist ab jetzt das feste Freischaufeln-Keyword (Julia-Regel: gleiches Keyword über mehrere Posts). KW29: Di + Mi + Fr tragen es.

## 🔗 Verwandte Notizen
- [[2026-07-04-freischaufeln-freebie]] · [[manychat-keywords]] · [[active-funnels]]
