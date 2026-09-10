---
tags: [funnel]
---

# ManyChat-Flow: Keyword `STANDBEIN`

**Funnel:** Produkt-Ideen-Finder · **Profil:** Mentoring (@mumlifebalance_patricia_ulmann)
**Status:** TODO — einrichten, bevor der erste Lead-Post rausgeht
**Erstellt:** 2026-09-10

---

## 🔑 Keyword

- **Keyword:** `STANDBEIN`
- **Rolle:** DM-Trigger + öffentliche Kommentar-Antwort
- **Warum nicht `IDEE`:** zu alltäglich. „Idee" tippt jemand versehentlich in einem
  normalen Kommentar und löst die Automation aus. `STANDBEIN` ist das Versprechen
  selbst und passiert nicht aus Versehen.
- **Konflikt-Check:** ✅ kollidiert mit keinem bestehenden Keyword
  (SYSTEM · FAHRPLAN · QUIZ · PRODUKT · THEMA · SICHTBAR · ANLEITUNG · LEAD ·
  ECHT1 · STORY · BIO · ENERGIE)
- **Match-Typ:** **Exact match.** Nicht „contains" — sonst reagiert es auf
  „Standbeine", „zweites Standbein" mitten im Satz.

---

## 🧭 Aufbau

```
Trigger (Kommentar ODER DM mit „STANDBEIN")
  ↓
1. Öffentliche Antwort auf den Kommentar
  ↓
2. DM: Begrüssung
  ↓
3. Button zur Landingpage
  ↓
4. Tag setzen: produkt-ideen-finder-lead-manychat
  ↓
5. Erinnerung nach 3 Std, wenn nicht geklickt
```

---

## Schritt 1 — Keyword-Regel

1. ManyChat → **Automation → Keywords → + New Keyword Rule**
2. Name: `Produkt-Ideen-Finder (STANDBEIN)`
3. Channel: **Instagram**, nur Mentoring-Profil
4. Trigger words: `STANDBEIN`, `Standbein`, `standbein`
5. Match type: **Exact match**
6. Response flow → neuer Flow (Schritt 2)

---

## Schritt 2 — DM-Flow

**Flow-Name:** `Produkt-Ideen-Finder Auslieferung`

### Block 1 — Begrüssung

```
Hey {{first name}} 💡

Schön, dass du dir das anschaust.

Der Produkt-Ideen-Finder ist ein kleines Tool, das dir in etwa fünf Minuten
zeigt, welches eigene Produkt eigentlich schon in dir steckt — eins, in das
dein Network-Produkt einfach als Teil der Lösung reinfliesst.

Du gibst nichts auf und musst niemanden anschreiben. Du stellst nur etwas
Eigenes daneben.

Hier geht's los ⬇️
```

### Block 2 — Button

- Button-Text: `Zum Produkt-Ideen-Finder 💡`
- Button-URL:
  `https://mumlifebalance.ch/produkt-ideen-finder/?utm_source=instagram&utm_medium=manychat&utm_campaign=produkt-ideen-finder&utm_content=dm-keyword-standbein`
- Link-Tracking: **ON**

> ⚠️ **Auf die Landingpage verlinken, nicht direkt aufs Tool.** Auf der
> Landingpage sitzt das ActiveCampaign-Formular — nur darüber landet die
> Mailadresse in deiner Liste. Wer direkt zum Tool geht, macht das Gespräch und
> bleibt trotzdem unbekannt.

### Block 3 — Tag setzen

- Tag: `produkt-ideen-finder-lead-manychat` (in ManyChat neu anlegen)
- Custom Field: `finder_dm_gesendet_am` = {{current date/time}}

---

## Schritt 3 — Erinnerung nach 3 Stunden

**Bedingung:** Link in 3 Std **nicht** geklickt.

```
Hey nochmal 👋

Ich hatte dir vorhin den Produkt-Ideen-Finder geschickt — vielleicht ist die
Nachricht untergegangen.

Hier direkt: https://mumlifebalance.ch/produkt-ideen-finder/

Fünf Minuten, kostenlos, und am Ende hast du eine konkrete Idee statt eines
vagen Gefühls. Falls dir gerade eine Frage dazu im Kopf rumgeht: einfach
antworten, ich lese hier selbst mit.
```

**Danach:** Tag `finder-erinnerung-gesendet` für die Auswertung.

---

## Schritt 4 — Öffentliche Kommentar-Antwort

ManyChat lässt drei Varianten rotieren, damit es unter dem Post nicht nach
Automat aussieht:

1. *„Ist unterwegs zu dir ✨"*
2. *„Schau mal in deine Nachrichten 💌"*
3. *„Hab dir grad geschrieben 👀"*

Dazu läuft der DM-Flow aus Schritt 2.

---

## ⚙️ Checkliste vor dem ersten Lead-Post

- [ ] Keyword-Regel `STANDBEIN` angelegt, **Exact match**
- [ ] DM-Flow mit drei Blöcken gebaut
- [ ] Tag `produkt-ideen-finder-lead-manychat` in ManyChat angelegt
- [ ] Erinnerung nach 3 Std gebaut
- [ ] Öffentliche Kommentar-Antwort aktiviert
- [ ] **Selbst getestet:** von einem zweiten Konto `STANDBEIN` kommentieren →
      kommt die DM an, führt der Button auf die Landingpage?
- [ ] **Ganzen Weg getestet:** Landingpage → eintragen → Tool → Gespräch →
      Lead liegt in ActiveCampaign (Liste 2, Tag 98)
- [ ] `context/manychat-keywords.md` ergänzt ✅ (erledigt 2026-09-10)

---

## Was am Funnel noch offen ist

| | Stand 2026-09-10 |
|---|---|
| Landingpage | ✅ live, mit AC-Formular f/66 |
| Seite nach dem Eintragen | ✅ live, Knopf zeigt aufs Tool |
| Tool (Vercel) | ✅ läuft, alle Schlüssel gesetzt, Chat antwortet |
| ManyChat-Flow | ⏳ dieser hier |
| **Minikurs-Link** | ❌ **tot.** Der Finder pitcht am Ende den 39er-Minikurs, der hinterlegte Checkout gibt 404. Muss an zwei Stellen ersetzt werden: `MINIKURS_URL` im Vercel-Projekt und `#zum-minikurs` auf der Seite nach dem Eintragen. |

---

## 🔗 Verwandte Notizen

- [[manychat-keywords]] — die verbindliche Keyword-Liste
- [[manychat-flow-BIO]] — derselbe Aufbau für den Bio-Check
- [[2026-09-mentoring]] — der Monatsplan, in dem dieser Launch steht
