---
tags: [funnel]
---

# ManyChat BIO — Klick für Klick

---

## Folie 1

**Klick:** Automation → Flows → + New Flow
**Name:** `Bio-Check DM-Auslieferung`
**Channel:** Instagram

---

## Folie 2 — Nachricht eintippen

**Text:**

```
Hey {{first name}}! 🎯

Du willst deine Instagram-Bio einmal richtig durchchecken?

Das bekommst du:
✓ Dein Experten-Satz (3 Varianten)
✓ 5 fertige Bio-Vorschläge
✓ 3 Ideen für deine Pinned Posts
✓ Alles als PDF per Mail

Dauert 3 Minuten. 0 CHF.

Hier geht's los ⬇️
```

---

## Folie 3 — Button unten dran

**Klick:** + Add Button
**Button-Typ:** URL
**Button-Text:** `Zum Bio-Check 🚀`
**URL:**

```
https://mumlifebalance.ch/bio-check
```

---

## Folie 4 — Tag setzen

**Klick:** + Add Step → Action → Add Tag
**Tag:** `bio-check-lead-manychat`

---

## Folie 5 — Speichern

**Klick:** oben rechts **Publish**

---

## Folie 6 — Keyword anlegen

**Klick:** Automation → Keywords → + New Keyword
**Channel:** Instagram
**Keywords:** `BIO, bio, Bio`
**Match:** Exact Match
**Response:** Send Flow → `Bio-Check DM-Auslieferung`
**Klick:** Save

---

## Folie 7 — Testen

Zweit-Account: `BIO` per DM schicken → DM muss in 3 Sek da sein.

---

## Folie 8 — NACH dem Reel-Post

**Klick:** Growth Tools → + New → Instagram Comment Auto-Reply
**Post:** Launch-Reel auswählen
**Keyword:** `BIO`
**Public Reply:** `Hab dir grad geschickt ✨`
**Then send DM:** Flow `Bio-Check DM-Auslieferung`
**Klick:** Activate

---

## Fertig ✅
