---
tags: [produkt, doterra, tools]
---

# ⚙️ Freebie-Auslieferung — ManyChat-Setup (Weg B, schnell live)

**Ziel:** 3-Tage-Energie-Kickstart automatisch ausliefern, mit dem, was du hast (ManyChat + ActiveCampaign). Kein PDF, kein Bot-Bau nötig.

**Der Trick wegen Instagram-24h-Fenster:** ManyChat startet + liefert Tag 1 sofort in der DM (im Fenster) und holt die E-Mail. **Tag 2 + Tag 3 kommen per E-Mail** (kein Zeitfenster) über AC-Liste 18.

Texte kommen 1:1 aus [02-freebie-3-tage-kickstart.md](02-freebie-3-tage-kickstart.md).

---

## Der Flow auf einen Blick

```
Reel/Post-Kommentar „ENERGIE"
        │  (ManyChat Keyword-Trigger, Comment + DM)
        ▼
[MC 1] Willkommens-DM  ── Button „Ja, ich bin dabei! 🌿"
        │
        ▼
[MC 2] TAG 1 sofort (Protein-Frühstück)   ← noch im 24h-Fenster
        │
        ▼
[MC 3] „Damit Tag 2 + 3 sicher ankommen: deine beste E-Mail?"
        │  (E-Mail erfassen → an AC Liste 18 + Automation starten)
        ▼
   ┌──────────────── ActiveCampaign ────────────────┐
   │  Mail Tag 2 (Bewegung/8000 Schritte) +24h 07:30 │
   │  Mail Tag 3 (Schlaf + Brücke ROUTINE) +48h 07:30│
   └─────────────────────────────────────────────────┘
        │
        ▼
Antwort „ROUTINE"  → 21-Tage-Info + Tag „routine-interesse" + Notiz an dich
```

---

## Teil 1 — ManyChat einrichten

### Schritt 1: Keyword-Trigger `ENERGIE`
- **Instagram → Keywords →** neues Keyword `ENERGIE`
- Auslöser: **Kommentar** (unter Post/Reel) **UND** Direktnachricht
- Match: „enthält" (fängt auch „Energie!" / „energie bitte")
- Aktion: startet die Automation unten
- *(Reichweiten-Bonus: Kommentar-Trigger pusht deinen Post im Algorithmus.)*

### Schritt 2: [MC 1] Willkommens-Nachricht
> Hey, schön bist du dabei. 🌿
> Ganz ehrlich: Ich war jahrelang in diesem Funktionsmodus — Kinder, Haushalt, Business — und hab gar nicht mehr gemerkt, wie leer ich eigentlich war. Bis mir mit 36 büschelweise die Haare ausgingen und ich am Nachmittag nur noch funktioniert hab.
> Die nächsten 3 Tage zeig ich dir, was mir geholfen hat, da rauszukommen. Nichts Kompliziertes. Nur das, was ich wirklich lebe.

- **Button/Quick Reply:** „Ja, ich bin dabei! 🌿" → führt zu [MC 2]
- **Tag setzen:** `kickstart-gestartet`
- 💡 Optional: eine **Sprachnotiz** von dir als Audio anhängen — macht's sofort persönlich.

### Schritt 3: [MC 2] TAG 1 (sofort, im 24h-Fenster)
- Kompletter **Tag-1-Text** aus dem Freebie-Doc (Protein-Frühstück, 30g, 1/3-Teller-Regel, Warum-Erklärung).
- Am Ende überleiten zu [MC 3].
- **Tag setzen:** `kickstart-tag1-gesehen`

### Schritt 4: [MC 3] E-Mail erfassen (damit Tag 2+3 ankommen)
> Damit Tag 2 und Tag 3 sicher bei dir landen (Instagram spinnt da manchmal 🙈), schick ich sie dir per Mail — an welche Adresse darf ich? 💌

- ManyChat **E-Mail-Frage** (User-Input Feld `E-Mail`)
- Aktion: **E-Mail → ActiveCampaign, Liste 18 „doTERRA Interessenten"** + Tag `energie-kickstart` (löst AC-Automation aus, Teil 2)
- Bestätigung:
> Perfekt, hab ich. Morgen früh kommt Tag 2 — und da wird's spannend. Bis dann! 🌸

- **Tag setzen:** `kickstart-email-erfasst`

### Schritt 5: Brücken-Keyword `ROUTINE`
- Neues Keyword `ROUTINE` (kommt in der Tag-3-Mail als CTA)
- Antwort: kurze 21-Tage-Info + **Tag `routine-interesse`** + optional **Benachrichtigung an dich** (ManyChat → dein Telegram/Notiz), damit du das Gespräch aufnimmst.

---

## Teil 2 — ActiveCampaign (Tag 2 + 3 per Mail)

**Automation:** „doTERRA — 3-Tage-Kickstart" · Auslöser: Tag `energie-kickstart` (aus ManyChat)

| Mail | Timing | Inhalt | Betreff-Idee |
|---|---|---|---|
| **Tag 2** | +24h, morgens 07:30 | Tag-2-Text (Bewegung / 8000 Schritte / Schlaf-Brücke) | „Der unterschätzte Schlaf-Hebel 🚶‍♀️" |
| **Tag 3** | +48h, morgens 07:30 | Tag-3-Text (Schlaf, erholt aufwachen) + **Brücke** mit CTA „Antworte ROUTINE / schreib mir ROUTINE" | „Warum du erschöpft aufwachst 💛" |

- Design: dein doTERRA-Mail-Template (Brand-Farben).
- **Wichtig:** Betreff = Hook (nicht „Tag 2"). Kein Heilversprechen.
- Tag am Ende: `kickstart-abgeschlossen`.

---

## Teil 3 — Tags-Übersicht (für spätere Auswertung + Retargeting)

| Tag | Bedeutung |
|---|---|
| `kickstart-gestartet` | hat Willkommen bekommen |
| `kickstart-tag1-gesehen` | Tag 1 in DM erhalten |
| `kickstart-email-erfasst` | E-Mail da, in Mail-Drip |
| `kickstart-abgeschlossen` | alle 3 Tage durch |
| `routine-interesse` | will mehr zum 21-Tage-Paket → dein Follow-up |

→ Wer nach `kickstart-abgeschlossen` NICHT `routine-interesse` hat → später sanft nachfassen.

---

## Was du/wir noch tun müssen

- [ ] Prüfen, ob Keyword `ENERGIE` in ManyChat schon existiert (laut Freebies-Doku Status unklar) — ggf. neu anlegen
- [ ] `ROUTINE`-Keyword anlegen
- [ ] AC-Automation „doTERRA 3-Tage-Kickstart" bauen (2 Mails) — kann ich texten/aufsetzen
- [ ] ManyChat↔AC-Verbindung prüfen (E-Mail-Übergabe an Liste 18)
- [ ] Deine 1–3 Sprachnotizen aufnehmen (optional, macht's stark persönlicher)
- [ ] 1 Reel/Post mit CTA „Kommentier ENERGIE" (Opt-in-Text im Freebie-Doc)

**Kann ich übernehmen:** die 2 AC-Mails texten + (falls du mir den ManyChat/AC-Zugang gibst bzw. `.env` da ist) den Flow via API aufsetzen. Sonst liefere ich dir alles copy-paste-fertig zum Zusammenklicken.

---

## 🔗 Verwandte
- [[02-freebie-3-tage-kickstart]] · [[03-automatisierung-ki-konzept]] · [[01-produkttreppe]]
