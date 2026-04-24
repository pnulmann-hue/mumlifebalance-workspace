# ManyChat-Flow: Keyword `BIO`

**Funnel:** Bio-Check · **Profil:** Mentoring (Instagram @mumlifebalance bzw. Patricias Mentoring-Account)
**Status:** TODO — einrichten vor dem Launch heute Nachmittag
**Erstellt:** 2026-04-24

---

## 🔑 Keyword

- **Keyword:** `BIO`
- **Rolle:** DM-Trigger + Comment-Auto-Reply
- **Konflikt-Check:** ✅ kein Konflikt mit bestehenden Keywords (SYSTEM · FAHRPLAN · QUIZ · PRODUKT · THEMA · SICHTBAR · ANLEITUNG · LEAD · ECHT1 · STORY · ENERGIE)

---

## 🧭 Flow-Architektur

```
Trigger (Comment ODER DM mit „BIO")
  ↓
1. Öffentlicher Auto-Reply auf Kommentar
  ↓
2. DM-Begrüßung (Bild + kurzer Text)
  ↓
3. Link-Button zum Bio-Check-Bot
  ↓
4. Follow-up nach 2 Std (wenn nicht geklickt)
  ↓
5. Tag setzen: „bio-check-lead-manychat"
  ↓ (optional, später)
6. Weitergabe an AC → Liste 2 + Tag 59
```

---

## Schritt-für-Schritt in ManyChat einrichten

### Schritt 1 — Keyword-Rule erstellen

1. ManyChat Dashboard → **Automation → Keywords**
2. **+ New Keyword Rule**
3. Name: `Bio-Check (BIO)`
4. Channel: **Instagram** (beide Profile? Nein — nur Mentoring für jetzt)
5. Trigger words: `BIO`, `bio`, `Bio`
6. Match type: **Exact match** (nicht „contains", sonst reagiert auf Wörter wie „Biografie" etc.)
7. Response flow: → **Create new flow** (siehe Schritt 2)

### Schritt 2 — DM-Flow bauen

**Flow-Name:** `Bio-Check DM-Auslieferung`

**Block 1 — Begrüßung (ohne Verzögerung):**

```
Hey {{first name}}! 🎯

Du willst deine Instagram-Bio einmal richtig durchchecken?
Kurze Frage stellen, alle Antworten geben — und raus kommt:

✓ Dein Experten-Satz (3 Varianten)
✓ 5 fertige Bio-Vorschläge (copy-paste-ready)
✓ 3 Ideen für deine Pinned Posts
✓ Alles als PDF per Mail

Dauert ca. 3 Minuten. Kostet 0 CHF.

Hier geht's los ⬇️
```

**Block 2 — Button:**

- Button-Text: `Zum Bio-Check 🚀`
- Button-URL: `https://mumlifebalance.ch/bio-check?utm_source=instagram&utm_medium=manychat&utm_campaign=bio-check-launch&utm_content=dm-keyword-bio`
- Link-Tracking: ON

**Block 3 — Tag + Custom Field setzen:**

- Tag hinzufügen: `bio-check-lead-manychat` (in ManyChat anlegen)
- Custom Field: `bio_check_dm_sent_at` = {{current date/time}}

### Schritt 3 — Follow-up nach 2h (wenn Link nicht geklickt)

**Trigger:** Bedingung „Hat Link NICHT geklickt in 2h"

**Block:**

```
Hey nochmal 👋

Du hattest mir vorhin BIO geschrieben — bin mir nicht sicher, ob der Link unterging.

Hier nochmal direkt: https://mumlifebalance.ch/bio-check

Ist heute gratis. Dauert drei Minuten. Falls du später mal nicht weißt, was in deine Bio soll — dann willst du das PDF. Versprochen. 🙌

Bei Fragen: einfach antworten, ich bin hier.
```

**Dann:** Tag setzen `bio-check-reminder-sent` für interne Analyse.

### Schritt 4 — Public Comment Auto-Reply

Wenn jemand öffentlich unter dem Reel `BIO` schreibt, soll ein kurzer öffentlicher Reply + DM zurückgehen:

**Öffentlicher Reply-Text** (rotieren lassen, ManyChat kann 3 Varianten):

1. *„Hab dir grad geschickt ✨"*
2. *„Check deine DMs 👀"*
3. *„Gleich in deinen Nachrichten 💌"*

**+ DM** gemäß Block 1–3 oben.

### Schritt 5 — AC-Integration (optional, später)

**Jetzt (MVP):** ManyChat-Flow reicht. Die AC-Integration kommt via Landing-Page-Submission (User füllt Bot aus → AC-Formular 47 feuert → Tag 59 + 60).

**Später (Week 2 Optimierung):**
- ManyChat → Zapier → AC direkt (für Leads, die das Keyword schreiben aber nicht bis zum Bot-Submit kommen)
- Damit hast du auch die „Neugierig geklickt, nicht abgeschlossen"-Kohorte als Lead.

---

## ⚙️ Setup-Checkliste

Vor Launch heute Nachmittag:

- [ ] Keyword-Rule `BIO` in ManyChat erstellt (Mentoring-Account)
- [ ] DM-Flow mit 3 Blocks gebaut (Begrüßung + Button + Tag)
- [ ] Follow-up-Flow nach 2h gebaut
- [ ] Public Comment Auto-Reply aktiviert
- [ ] Selbst getestet: Kommentar unter alten Post + Keyword-DM → kommt DM an?
- [ ] URL mit UTM-Parametern korrekt (bio-check.ch geht auf Thrivecart bzw. WordPress-Landing)
- [ ] Tag `bio-check-lead-manychat` in ManyChat angelegt
- [ ] `context/manychat-keywords.md` ist um `BIO` ergänzt (Claude erledigt)

---

## 📋 API-Option (falls du's lieber automatisch willst)

Falls du den Flow per Script statt manuell willst:

```bash
cd /home/user/mumlifebalance-workspace/scripts/manychat
node --env-file=.env mc-api.js create-tag "bio-check-lead-manychat"
```

**ABER:** ManyChat erlaubt via API nur Tags + Custom Fields + Subscribers — Flows + Keywords müssen im UI gebaut werden. Also: Anlage des eigentlichen Flows = manuell.

---

## 🔍 Erfolgs-Metriken (Check nach 24h / 7 Tagen)

| Metrik | Ziel Tag 1 | Ziel Woche 1 |
|---|---|---|
| DM-Keywords empfangen (`BIO`) | ≥ 15 | ≥ 50 |
| Link-Klickrate | ≥ 70% | ≥ 65% |
| Bot-Abschluss-Rate | ≥ 50% | ≥ 45% |
| Follow-up-Klicks (nach 2h-Reminder) | ≥ 25% | ≥ 20% |

Daten holen via:
- ManyChat Dashboard → Flow Analytics
- AC → Liste 2 „Bio-Check" Tag-Zählung (`lead`: 59 / `abgeschlossen`: 60)

---

## 🛑 Wichtig: Keyword-Rotation

Julia-Trost-Regel: **gleiches Keyword über mehrere Posts hinweg konsistent nutzen**. Nicht bei jedem Reel ein neues Wort erfinden.

→ `BIO` ist jetzt für mindestens **6 Wochen** das Bio-Check-Keyword. Bei jedem Reel/Karussell, der auf den Bio-Check zielt, CTA: „Kommentier **BIO**".

Zweitrang-Keywords für Bio-Check-Content (wenn `BIO` zu oft benutzt wurde):
- `SCHAUFENSTER` (optional, bei reiner Metapher-Content)
