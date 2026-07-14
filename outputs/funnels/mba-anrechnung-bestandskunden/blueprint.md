---
tags: [funnel, mba, launch]
---

# MBA-Upgrade für Bestandskundinnen — „Dein Kurs ist schon drin"

> **Aktion:** Bestehende Käuferinnen der 3 grossen Kurse (Instagram-Kundenmaschine · Mama-CEO · Digitale Produktwelt) bekommen den **vollen Kaufpreis ihres Kurses an die MBA angerechnet** — sie zahlen nur die Differenz.
> **Kanal:** Eigene 4-teilige Mailsequenz, parallel zum offenen Cart. **Deadline: So 27.7. 23:59** (Ende Pioneer-Preis).
> Erstellt: 2026-07-13 · Modus /funnel 1+2.

---

## 1. Warum das funktioniert (die Kern-Logik)

Die MBA **enthält** genau diese 3 Kurse als Bestandteil (Stufe 1–3 der Treppe). Wer einen davon schon gekauft hat, besitzt bereits ein Stück der Academy. Es wäre schlicht unfair, ihn ein zweites Mal zu bezahlen.

Das ist kein „Rabatt aus Gnade", sondern **die logischste Sache der Welt** — und genau darum ist es die stärkste Botschaft an diese Gruppe:

> „Was du gekauft hast, zahlst du kein zweites Mal. Dein Kurs ist voll angerechnet — du zahlst nur die Differenz zum Rest."

Diese Anrechnung ist bereits offizielle MBA-Policy (`mba-produktsteckbrief.md`, §7). Diese Aktion **operationalisiert sie gezielt** für die wärmste Gruppe, die du hast: Menschen, die schon einmal bei dir gekauft haben.

**Pain, den wir treffen:** Sie hat sich Kurse gekauft, halb umgesetzt, verzettelt sich — kein roter Faden. Die MBA ist genau der Faden. Und ihr erster Kurs ist der Anfang davon, nicht verlorenes Geld.

---

## 2. Segmente + Anrechnung

**MBA Pioneer-Preis: CHF 997** (danach 1347). **Angerechnet wird immer der volle Betrag, den die Frau tatsächlich bezahlt hat** — Earlybird, Pilot oder Vollpreis. Die Mails nennen bewusst **keinen fixen Restbetrag** („du zahlst nur die Differenz"), damit es für alle stimmt. Die konkrete Anrechnung passiert über den ThriveCart-Coupon.

**Wichtig:** Coupons gehen **nach bezahltem Betrag**, nicht nach Kurs — weil innerhalb eines Kurses verschiedene Preise bezahlt wurden (z.B. Mama-CEO Earlybird 249 vs. final 333).

| Segment (Käuferinnen) | AC-Tag | typische Preispunkte | passender Coupon |
|---|---|---|---|
| Instagram-Kundenmaschine | **39** | meist 333 | `DRIN-333` |
| Mama-CEO | **71** | 249 (Earlybird/Pilot) · 333 (final) | `DRIN-249` / `DRIN-333` |
| Digitale Produktwelt | **44** | 333 | `DRIN-333` |

→ In der Praxis genügen fast sicher **zwei Coupons: `DRIN-249` und `DRIN-333`**. Falls du einen weiteren Preis kassiert hast (z.B. ein IKM-Earlybird), leg einfach `DRIN-<Betrag>` zusätzlich an.

**Ausschliessen:** alle mit Tag **79** `mba-kauf` (haben die MBA schon).

### Sonderfälle
- **Wer paid was?** Du weisst die Preispunkte aus deinem ThriveCart-Verkaufsexport (die 5 Pilot-Mamas = 249, der Rest = 333). Beim Versand die Käuferinnen entsprechend dem bezahlten Betrag dem richtigen Coupon zuordnen. Im Zweifel grosszügig: `DRIN-333`.
- **Mehrfach-Käuferin (zwei enthaltene Kurse):** Anrechnung **stapelt** (beide Kaufpreise zusammen). Wenige Fälle → eigener Personen-Coupon oder manuell. **Erst prüfen:** Kontakte mit Tag 39 UND 71 (bzw. 44).
- **Tag 39 verifizieren:** sollte die **Käuferinnen** sein (Parallele zu Tag 44 „digitale Produktwelt grosser Kurs"). Kurz gegen den ThriveCart-Export prüfen, damit keine reinen Interessentinnen (Tag 63 = Klick, nicht Kauf) reinrutschen.

---

## 3. ThriveCart-Setup (einmalig, 5 Min)

**Ablauf (NEU): Rabattcode auf Anfrage.** Die Mails enthalten keinen Link und keinen Code — jede Frau antwortet mit dem Wort **MBA** auf die Mail, und du schickst ihr persönlich den passenden Code + den Checkout-Link. So bekommt jede exakt ihren bezahlten Betrag angerechnet (Earlybird-safe), und du hast einen warmen 1:1-Kontakt statt eines anonymen Klicks.

Für jeden Preispunkt einen **Festbetrags-Rabatt** anlegen (nicht Prozent):

1. ThriveCart → MBA-Produkt → **Coupons** → *Add coupon*
2. Typ: **Fixed amount**, Betrag = der bezahlte Kaufpreis (z.B. 333, dann 249), Währung CHF
3. Code = `DRIN-333`, `DRIN-249` (und ggf. `DRIN-<weiterer Betrag>`), Gültigkeit **bis 27.7. 23:59**, gilt auch auf den Ratenplan
4. **Antwort-Handling:** Schreibt eine Frau „MBA", schaust du kurz, welchen Kurs/Preis sie hatte, und schickst ihr den passenden Code + `DEINE-THRIVECART-MBA-CHECKOUT-URL?coupon=DRIN-<Betrag>`. Fertige Antwort-Vorlage: siehe unten.

### Antwort-Vorlage (wenn jemand „MBA" schreibt)
> Wie schön, dass du dabei sein willst! 🧡 Dein [Kursname] ist voll angerechnet — du zahlst nur die Differenz. Hier ist dein persönlicher Rabattcode **DRIN-[Betrag]** und der direkte Link: [Checkout-Link mit ?coupon=…]. Der Code gilt bis Sonntag 27.7. 23:59. Wenn was unklar ist, schreib mir einfach.

---

## 4. AC-Setup + Sendeplan

### Segment bauen (pro Kurs eine Sendung)
In AC eine Sendung je Segment: **Kontakte mit Tag [39 / 71 / 44]** UND **nicht** Tag 79 (`mba-kauf`).

### Doppel-Beschallung vermeiden (empfohlen)
Diese Käuferinnen hängen evtl. auch in den allgemeinen Cart-Mails. Damit es persönlich bleibt statt spammig: In der Cart-Window-Automation einen **Conditional Split** — hat Kontakt Tag 39/71/44 → **raus aus den allgemeinen Cart-Blasts**, rein in diese dedizierte Sequenz. So kriegt jede Frau nur *eine* Stimme.

### Sendeplan (heute Mo 13.7. → Close So 27.7.)
| Mail | Datum/Zeit | Zweck |
|---|---|---|
| **1 — Dein Kurs ist schon drin** | Di 15.7. 08:00 | Reveal der Anrechnung, warm |
| **2 — Du hast eine Stufe, es fehlen zwei** | So 20.7. 09:00 | Treppen-Frame / roter Faden |
| **3 — Was dich der Rest wirklich kostet** | Do 24.7. 08:00 | Rechnung + Einwand Zeit + Beweis |
| **4 — Heute läuft deine Anrechnung aus** | So 27.7. 08:00 | Close-Tag: Preis steigt + Anrechnung endet |
| *(optional 4b — Letzter Aufruf)* | So 27.7. 21:30 | 2,5 h — kann `mba-cart-sequence/14-letzter-aufruf.html` recyceln |

### Mails pro Segment ausspielen
**Zwei fertige Sätze — kein Editieren nötig.** Die Mails enthalten weder Betrag noch Code (kommt per Antwort), sind aber pro Zielgruppe passend getextet:

- `mails-instagram-kundenmaschine/` → an die Käuferinnen mit Tag **39** (Mail 1 nennt „die Instagram-Kundenmaschine", Mail 2: ✅ Stufe 1 Sichtbarkeit)
- `mails-mama-ceo/` → an die Käuferinnen mit Tag **71** (Mail 1 nennt „Mama-CEO", Mail 2: ✅ Stufe 2 Zeit & Struktur)

Einfach HTML kopieren, als AC-Kampagne (Custom HTML) an das jeweilige Segment senden. Der Rabattcode wird erst auf ihre Antwort hin persönlich verschickt (siehe §3).

---

## 5. Umsatz-Beitrag (Realitäts-Check gegen 40k-Ziel)

Warme Bestandskundinnen konvertieren auf ein faires Upgrade-Angebot deutlich höher als kalte Leads. Grobe Rechnung: aus dem Pool der 3 Käufer-Gruppen reichen **5 Upgrades** → ca. **3'300–3'700 CHF**, die sonst nie geflossen wären — plus diese Frauen sind in der Pioneer-Runde gebunden (12 Monate Begleitung, höchste Bindung).

Zahlt direkt auf das MBA-Launchziel (8 Verkäufe) ein: die wärmsten Käuferinnen zuerst zu holen ist der günstigste Weg dorthin.

---

## 6. Assets

**→ Sendfertig, ohne Bearbeitung (das nimmst du):**
- `mails-instagram-kundenmaschine/` — 4 Mails für die IKM-Kundinnen (Tag 39)
- `mails-mama-ceo/` — 4 Mails für die Mama-CEO-Kundinnen (Tag 71)

*(Der Ordner `mails/` ist die Master-Vorlage — nur als Quelle, nicht zum Senden.)*

Alle im Onlinebusiness-Brand-Design, `%FIRSTNAME%`-Merge, Swiss ss, Patricia-Voice, keine käufer-spezifischen Beträge, kein Code/Link in der Mail (Rabattcode kommt per Antwort → Earlybird-safe, warmer 1:1-Kontakt).

---

## 🔗 Verwandte Notizen
- [[mba-produktsteckbrief]] · [[challenge-launch-plan]] · [[mba-salespage]]
