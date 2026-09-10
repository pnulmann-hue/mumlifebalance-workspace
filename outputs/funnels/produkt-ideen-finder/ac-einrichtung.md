---
tags: [funnel]
---

# ActiveCampaign — Automation „Produkt-Ideen-Finder Brücke"

**Was sie macht:** fängt den Lead nach der Auslieferung auf, bringt ihn ins Gespräch,
pitcht am Tag 6 den 39er — und übergibt am Tag 8 an die bestehende 0€ Engine.
**Erstellt:** 2026-09-10

---

## Der Flow zum Zusammenklicken

```
TRIGGER: Tag 98 „produkt-ideen-finder-lead" hinzugefügt   ·   Läuft: Einmal

 ├─ START-CHECK: hat Tag 79 (mba-kauf)? → Automation sofort beenden
 │                                        (MBA-Käuferin kriegt aus keinem Funnel Mails)
 │
 ├─ ZIEL „Springen zu Ende" (feuert laufend, Position ganz oben):
 │     Tag 43 „digitales Produkt" → raus
 │     (wer den Minikurs schon hat, kriegt dessen Pitch nie)   ⚠️ Tag bestätigen, s.u.
 │
 │  ── Mail 1 „Auslieferung" läuft in der bestehenden Formular-Automation ──
 │
 ├─ 1 Tag warten
 ├─ WENN/SONST: „hat Link in Mail 1 geklickt?"
 │     JA   → Mail 2b „Was ist bei dir rausgekommen?"
 │     NEIN → Mail 2a „Der Finder liegt noch bei dir rum"
 │
 ├─ 2 Tage warten  (= Tag 3)
 ├─ Mail 3 „Deine Idee ist noch kein Produkt"
 │
 ├─ 3 Tage warten  (= Tag 6)
 ├─ Mail 4 „Von der Idee zu etwas, das man kaufen kann"   → ThriveCart 39
 │
 ├─ 2 Tage warten  (= Tag 8)
 ├─ Tag setzen: „ideen-finder-durchlaufen"   (neu anlegen)
 ├─ Tag setzen: 87 „Automation 0€ Produkt"   → startet Automation 72 (0€ Engine)
 └─ Ende
```

**Wichtig zur Wenn/Sonst-Bedingung:** In AC heisst die Bedingung *„Hat auf einen Link
in einer Nachricht geklickt"* → Kampagne = deine Auslieferungsmail. Damit sie greift,
muss im Auslieferungs-Mail **Link-Tracking an** sein.

---

## 🔴 Der Punkt, der vorher entschieden werden muss

Die 0€ Engine (Automation 72) startet mit **E1 und E2 — und die pitchen
„Finde dein Thema" (39)**. Eine Frau, die gerade den Ideen-Finder durchlaufen hat und
am Tag 6 den Minikurs „Vom Network-Wissen zum eigenen Produkt" angeboten bekam,
würde zwei Tage später den **zweiten 39er** sehen. Dazu einen, der sie thematisch
zurückschickt — ihr Thema hat sie ja gerade gefunden.

**Empfehlung: E1 + E2 überspringen.** Automation 72 hat schon ein „Springen zu M1"-Ziel,
über das Kurs-Käuferinnen die Brücke überspringen (Tags 41 · 51 · 39 · 71 · 44).
Dort einfach ergänzen:

> **ODER Tag besteht „ideen-finder-durchlaufen" → Springen zu M1**

Damit landet sie direkt im MBA-Track, wo die Engine ohnehin hinführt. Ein Klick,
keine neue Automation.

Die Alternative wäre, es so zu lassen und ihr beide 39er zu zeigen. Kann man machen,
liest sich aber wie ein Karussell.

---

## ⚠️ Was ich nicht selbst entscheiden konnte

**Der Kauf-Tag für „Vom Network-Wissen zum eigenen Produkt" fehlt in meiner Liste.**

Nach dem Muster deiner anderen Produkte (Automation-Tag ↔ Kauf-Tag) ist es
höchstwahrscheinlich **43 „digitales Produkt"**:

| Produkt | Automation-Tag | Kauf-Tag |
|---|---|---|
| Finde dein Thema | 46 | 41 |
| Expertin | 50 | 51 |
| Digitale Produktwelt | 49 | 44 |
| **Vom Network-Wissen zum eigenen Produkt** | **48** | **43?** |

Bitte kurz in ThriveCart nachschauen, welchen Tag der Checkout
`eigene-produkterstellung` setzt. Ohne das kann die Regel „wer den Kurs hat, kriegt
seine Mails nie" hier nicht greifen — und dann bekommt eine Käuferin am Tag 6 eine
Mail, die ihr etwas anbietet, das sie schon bezahlt hat.

---

## Reihenfolge beim Bauen

1. Tag `ideen-finder-durchlaufen` anlegen
2. Kauf-Tag klären (oben) und im „Springen zu Ende"-Ziel eintragen
3. Automation nach dem Schema oben zusammenklicken
4. Die vier HTML-Mails aus `mails/` reinkopieren (Betreffzeilen und Preheader stehen
   in [[mails-2-4-bruecke]])
5. In Automation 72 die „Springen zu M1"-Bedingung um den neuen Tag erweitern
6. **Selbst durchtesten:** eigene Adresse ins Formular → Auslieferung kommt →
   Link **nicht** klicken → am nächsten Tag muss 2a kommen. Zweite Adresse, Link
   klicken → 2b muss kommen.

---

## Stand der Links (geprüft 2026-09-10)

| Link | Status |
|---|---|
| `produkt-ideen-finder-service.vercel.app` | ✅ 200 |
| `mumlifebalance.ch/produkt-ideen-finder/` | ✅ 200 |
| `thrivecart.com/eigene-produkterstellung/` | ✅ 200 |
| `thrivecart.com/network-wissen-produkt/` | ❌ 404 — war im Tool hinterlegt, **ersetzt und neu ausgerollt** |

**Noch offen:** auf der Seite nach dem Eintragen (WP-Seite 4085) zeigt ein Knopf auf
`#zum-minikurs`, also ins Leere. Der Fix ist vorbereitet
(`scripts/wordpress/finder-knopf-verlinken.mjs` mit `PLATZHALTER=#zum-minikurs`),
mumlifebalance.ch hat die Verbindung beim Versuch aber abgewiesen. Muss nochmal
laufen, wenn der Server wieder Anfragen annimmt.

---

## 🔗 Verwandte Notizen

- [[mails-2-4-bruecke]] — die Mailtexte
- [[mail-1-auslieferung]] — die Mail davor
- [[loop-ketten-mails]] — die Kaskade, an die übergeben wird
- [[manychat-flow-STANDBEIN]] — der zweite Weg in denselben Funnel
