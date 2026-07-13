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

## 2. Segmente + Anrechnung (die Preis-Tabelle)

**MBA Pioneer-Preis: CHF 997** (danach 1347). Voller Kaufpreis wird abgezogen.

| Segment | AC-Tag | bezahlt | Anrechnung | **MBA-Restpreis** | 6 Raten (≈) | ThriveCart-Coupon |
|---|---|---|---|---|---|---|
| Instagram-Kundenmaschine | **39** | 333 | −333 | **664** | ~111/Mt | `KUMA-DRIN` |
| Mama-CEO (Pilot) | **71** | 249 | −249 | **748** | ~125/Mt | `CEO-DRIN-249` |
| Mama-CEO (regulär) | **71** | 333 | −333 | **664** | ~111/Mt | `CEO-DRIN-333` |
| Digitale Produktwelt | **44** | 333 | −333 | **664** | ~111/Mt | `DPW-DRIN` |

**Ausschliessen:** alle mit Tag **79** `mba-kauf` (haben die MBA schon).

### Sonderfälle
- **Mama-CEO (Tag 71):** unterscheidet Pilot (249) und regulär (333) nicht automatisch. Es ist eine kleine, dir bekannte Gruppe (die 5 Pilot-Mamas zahlten 249) → weise pro Person den richtigen Coupon zu. Im Zweifel grosszügig: `CEO-DRIN-333`.
- **Mehrfach-Käuferin (zwei enthaltene Kurse):** Anrechnung **stapelt**. Beispiel Instagram-Kundenmaschine + Mama-CEO = −666 → MBA für **331**. Diese wenigen Fälle: eigener Coupon `KOMBI-DRIN` (fixer Betrag pro Person) oder du machst es manuell. → **erst prüfen:** Kontakte mit Tag 39 UND 71 (bzw. 44) rausfiltern.
- **Tag 39 verifizieren:** Tag 39 „Instagram-Kundenmaschine" sollte die **Käuferinnen** sein (Parallele zu Tag 44 „digitale Produktwelt grosser Kurs"). Kurz gegen den ThriveCart-Käufer-Export prüfen, damit keine reinen Interessentinnen (Tag 63 = Klick, nicht Kauf) reinrutschen.

---

## 3. ThriveCart-Setup (einmalig, 5 Min)

Für jeden Coupon aus der Tabelle in ThriveCart einen **Festbetrags-Rabatt** anlegen (nicht Prozent):

1. ThriveCart → MBA-Produkt → **Coupons** → *Add coupon*
2. Typ: **Fixed amount**, Betrag = die Anrechnung (333 bzw. 249), Währung CHF
3. Code = aus Tabelle (`KUMA-DRIN` etc.), Gültigkeit **bis 27.7. 23:59**, gilt auch auf den Ratenplan
4. **Button-Link mit vorab gesetztem Coupon** bauen, damit die Frau nichts eintippen muss:
   `DEINE-THRIVECART-MBA-CHECKOUT-URL?coupon=KUMA-DRIN`
   *(In den Mails steht als Platzhalter `https://mumlifebalance.ch/mba/` — ersetze das durch deine echte ThriveCart-Checkout-URL mit `?coupon=…`. Den Code zusätzlich sichtbar in der Mail lassen als Fallback.)*

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
Die 4 HTML-Mails sind mit den **Instagram-Kundenmaschine-Zahlen (664 / ~111 / `KUMA-DRIN`)** gefüllt = Zero-Effort für das grösste Segment. Für Mama-CEO / DPW nur diese Stellen tauschen (im HTML als `<!-- SWAP -->` markiert):

| Token | IKM (default) | Mama-CEO Pilot | Mama-CEO regulär | DPW |
|---|---|---|---|---|
| Kursname | die Instagram-Kundenmaschine | Mama-CEO | Mama-CEO | die Digitale Produktwelt |
| Restpreis | 664 | 748 | 664 | 664 |
| Rate (6×) | 111 | 125 | 111 | 111 |
| Coupon | KUMA-DRIN | CEO-DRIN-249 | CEO-DRIN-333 | DPW-DRIN |
| „welche Stufe du schon hast" (Mail 2) | Sichtbarkeit (Stufe 1) | Zeit & Struktur (Stufe 2) | Zeit & Struktur (Stufe 2) | dein eigenes Angebot (Stufe 3) |

---

## 5. Umsatz-Beitrag (Realitäts-Check gegen 40k-Ziel)

Warme Bestandskundinnen konvertieren auf ein faires Upgrade-Angebot deutlich höher als kalte Leads. Grobe Rechnung: aus dem Pool der 3 Käufer-Gruppen reichen **5 Upgrades** → ca. **3'300–3'700 CHF**, die sonst nie geflossen wären — plus diese Frauen sind in der Pioneer-Runde gebunden (12 Monate Begleitung, höchste Bindung).

Zahlt direkt auf das MBA-Launchziel (8 Verkäufe) ein: die wärmsten Käuferinnen zuerst zu holen ist der günstigste Weg dorthin.

---

## 6. Assets

- `mails/mail-1-dein-kurs-ist-drin.html`
- `mails/mail-2-eine-stufe-zwei-fehlen.html`
- `mails/mail-3-was-der-rest-kostet.html`
- `mails/mail-4-anrechnung-laeuft-aus.html`

Alle im Onlinebusiness-Brand-Design, `%FIRSTNAME%`-Merge, Swiss ss, Patricia-Voice.

---

## 🔗 Verwandte Notizen
- [[mba-produktsteckbrief]] · [[challenge-launch-plan]] · [[mba-salespage]]
