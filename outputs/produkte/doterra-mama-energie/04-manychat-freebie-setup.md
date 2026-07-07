---
tags: [produkt, doterra, tools]
---

# ⚙️ Freebie-Auslieferung — Setup (E-Mail-first, Weg B)

**Entscheidung 2026-07-06:** Auslieferung **per E-Mail** (ManyChat sammelt nur ein). Schöner + ausführlicher gestaltbar, kein Instagram-24h-Fenster-Problem, baut die E-Mail-Liste.

**Rollen:**
- **ManyChat** = Eingangstür auf Instagram (Keyword `ENERGIE` → E-Mail abfragen)
- **ActiveCampaign** = Auslieferung (3 Mails über 3 Tage) · Liste **18 „doTERRA Interessenten"**
- **Mail-Texte:** [05-freebie-mails-kickstart.md](05-freebie-mails-kickstart.md)

**Schon angelegt (von mir via AC-Zugang):** Tag `energie-kickstart` (ID **84**) · Tag `routine-interesse` (ID **85**)

---

## Der Flow auf einen Blick

```
Reel/Post-Kommentar „ENERGIE"
   │  ManyChat Keyword-Trigger (Comment + DM)
   ▼
[MC] Willkommens-DM  +  E-Mail abfragen
   │  → E-Mail an AC Liste 18  +  Tag „energie-kickstart" (84)
   ▼
AC-Automation „doTERRA · 3-Tage-Kickstart"  (Trigger: Tag 84)
   ├─ Mail Tag 1  (Protein)          → sofort
   ├─ warten bis nächster Tag 07:30
   ├─ Mail Tag 2  (Bewegung)         → +24h
   ├─ warten bis nächster Tag 07:30
   └─ Mail Tag 3  (Schlaf + Paket)   → +48h  · CTA: Paket-Link (Cart)

Bestellung im Cart  →  du meldest dich PERSÖNLICH (neue Einschreibung im doTERRA-Backoffice)
```

---

## Teil 1 — ManyChat (du, ~5 Min)

### 1. Keyword `ENERGIE`
- Instagram → **Keywords** → `ENERGIE` · Auslöser **Kommentar + DM** · Match „enthält"
- *(Kommentar-Trigger pusht deinen Post im Algorithmus — Reichweiten-Bonus.)*

### 2. Willkommens-DM + E-Mail abfragen
Nachricht:
> Hey, schön bist du dabei! 🌿 Ich schick dir meinen 3-Tage-Energie-Kickstart per Mail (da kann ich dir mehr mitgeben als hier in der DM). An welche Adresse darf ich? 💌

- **ManyChat-Aktion „E-Mail erfassen"** (Feld E-Mail, mit Validierung)
- **Danach-Aktion:** *ActiveCampaign → Subscribe to List 18* **+** *Add Tag `energie-kickstart` (84)*
  - (Falls die AC-Verbindung in ManyChat noch nicht steht: einmalig unter Settings → Integrations → ActiveCampaign verbinden.)
- Bestätigungs-DM:
> Perfekt, hab ich! 🌸 Tag 1 ist grad unterwegs in dein Postfach — schau auch kurz im Spam, falls er sich versteckt. Bis gleich!

### 3. Kein ROUTINE-Keyword mehr nötig
Du meldest dich nach der Bestellung **persönlich** — die Bestellung kommt als neue Einschreibung in dein doTERRA-Backoffice. Also **kein** ManyChat-ROUTINE-Flow nötig. (Tag `routine-interesse` (85) bleibt ungenutzt, kann gelöscht werden.)

---

## Teil 2 — ActiveCampaign-Automation (du im UI, ~10 Min · Mails liefere ich)

**Automation neu:** „doTERRA · 3-Tage-Kickstart"
- **Trigger:** *Tag added → `energie-kickstart` (84)*  (sauberer als Listen-Trigger)
- **Schritte:**
  1. **E-Mail „Tag 1 — Protein"** → sofort senden
  2. **Warten** bis „nächster Tag, 07:30"
  3. **E-Mail „Tag 2 — Bewegung"**
  4. **Warten** bis „nächster Tag, 07:30"
  5. **E-Mail „Tag 3 — Schlaf + Brücke"**
  6. **Tag hinzufügen** `kickstart-abgeschlossen` *(optional, für Auswertung — sag Bescheid, ich lege den Tag auch an)*
- Mail-Texte: [05-freebie-mails-kickstart.md](05-freebie-mails-kickstart.md)
- **Fertiges HTML zum Einfügen** (doTERRA-Design, Orange-Header):
  - Tag 1 → `mails/tag-1-protein.html`
  - Tag 2 → `mails/tag-2-bewegung.html`
  - Tag 3 → `mails/tag-3-schlaf.html`
  - Vorlage: `context/mail-design-doterra.html`
- In AC: Mail-Schritt → „Quellcode/HTML" → HTML-Datei-Inhalt reinkopieren → Betreff aus [05](05-freebie-mails-kickstart.md) setzen.

> ⚠️ **Warum du das im UI machst:** AC lässt das Bauen von Automationen (Wartezeiten + Mail-Reihenfolge) nicht über die Schnittstelle zu — ich kann Tags/Kontakte/Entwürfe anlegen, aber die Automation selbst klickst du zusammen. Ich hab dir jeden Schritt oben vorgegeben.

---

## Was noch offen ist

- [ ] ManyChat: `ENERGIE`-Flow bauen (Anleitung oben)
- [ ] ManyChat↔AC-Integration prüfen/verbinden (E-Mail → Liste 18 + Tag 84)
- [ ] AC-Automation „doTERRA · 3-Tage-Kickstart" bauen (3 Mails + 2 Wartezeiten)
- [ ] Mails ins Brand-Design bringen (ich adaptiere Template auf doTERRA-Orange, wenn gewünscht)
- [ ] Deine Sprachnotiz/Selfie optional in Mail 1 einbetten (macht's persönlich)
- [ ] 1 Reel/Post „Kommentier ENERGIE" (Opt-in-Text in [02-freebie-3-tage-kickstart.md](02-freebie-3-tage-kickstart.md))

---

## 🔗 Verwandte
- [[05-freebie-mails-kickstart]] · [[02-freebie-3-tage-kickstart]] · [[03-automatisierung-ki-konzept]] · [[01-produkttreppe]]
