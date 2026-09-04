---
tags: [ads, chatgpt-ads]
---

# ChatGPT-Ads — 90 Storyideen (19 CHF)

> Erste Anzeigen für den neuen OpenAI-/ChatGPT-Ads-Kanal (Konto steht seit 4.9.2026).
> **Message-Match-Prinzip:** Anzeige und Verkaufsseite sprechen dieselbe Sprache — Know-Like-Trust
> („kennen, mögen, vertrauen"). Der passende Seiten-Block liegt in
> `outputs/salespages/90-storyideen-networkerinnen-salespage.md` → **Block 6B „Warum Storys verkaufen"**.

---

## Warum ChatGPT-Ads für genau dieses Produkt passen

- **Intent statt Störung:** Auf Meta unterbrichst du jemanden beim Scrollen. Hier tippt jemand mit
  *Absicht* eine Frage — „was soll ich als Networkerin posten?" — und deine Antwort-Karte erscheint.
  Das ist die kaufbereiteste Sekunde, die es gibt.
- **Direktverkauf hat hier eine echte Chance** (anders als die pausierte kalte Meta-Verkaufsanzeige),
  weil die Person das Problem gerade selbst formuliert. Trotzdem: erste Runde auf **Klicks** optimieren.
- **First Mover:** Der Kanal ist in der DACH-Nische noch leer.

## Format-Regeln (Antwort-Karte)

| Element | Limit | Sichtbar (Faustregel) | Hinweis |
|---|---|---|---|
| **Titel** | ≤ 50 Zeichen | ~25 | Das Wichtigste in die ersten 25 Zeichen |
| **Beschreibung** | ≤ 100 Zeichen | ~50 | Nutzen + Preis früh nennen |
| **Bild** | quadratisch ≥ 1024 px | — | **kein Video** — die quadratischen Storyideen-Motive wiederverwenden |
| **Optimierung** | — | — | Start: **Klicks** · Budget ab 25 $/Tag |

**Landing-Link (mit UTM):**
`https://mumlifebalance.thrivecart.com/storyideen/?utm_source=chatgpt&utm_campaign=fruehstart`

---

## Die Anzeigen-Varianten

Alle vier zielen auf denselben Kern-Suchintent („was/wie poste ich als Networkerin"), decken aber
verschiedene der drei Jobs ab. Titel bewusst unter 40 Zeichen, damit nichts abgeschnitten wird.

### V1 — Ratlosigkeit (Einstieg, breitester Schmerz)
- **Titel:** Nie wieder ratlos vor der Story
- **Beschreibung:** 90 fertige Storyideen für Networkerinnen — sichtbar werden, ohne dein Produkt zu pushen. 19 CHF.

### V2 — Verkaufen ohne nerven (Job: Vertrauen)
- **Titel:** Über Storys verkaufen, ohne zu nerven
- **Beschreibung:** Storys bauen das Vertrauen, das online kauft. 90 Ideen, aus denen du täglich schöpfst. 19 CHF.

### V3 — Kauf-bereit / konkret (Job: Kennenlernen)
- **Titel:** Fertige Storyideen für Networkerinnen
- **Beschreibung:** Schluss mit Rätselraten: 90 Ideen in 8 Anlässen + Kompass, welche du wann nimmst. 19 CHF.

### V4 — Nahbarkeit (Job: Mögen)
- **Titel:** Zeig dich, nicht nur dein Produkt
- **Beschreibung:** So wirst du als Mensch sichtbar — und die richtigen Menschen hören zu. 90 Storyideen. 19 CHF.

---

## Testplan

1. **Runde 1:** V1 + V3 zuerst (höchster Intent) auf **Klicks**, gleiches quadratisches Bild.
2. Nach ~50–100 Klicks: schwächeren Titel raus, V2 oder V4 dazu.
3. Erst wenn das Conversion-Event auf der Danke-Seite steht (Startklar-Technik), auf **Kauf** umstellen.

## Technik-Setup (Startklar-Checkliste) — Stand 4.9.2026

**Konto:** freigeschaltet, Werbekonto `adacct_6a96b51ecb548190b365b2153f85373a` (Mum Life Balance).
Entwurfs-Kampagne „Mum Life Balance campaign" (Typ Klicks, noch nicht bereitgestellt).

- [x] **Punkt 3 — robots.txt (OAI-AdsBot):** bereits ok. ThriveCart blockt nur fremde `/private-*`-Pfade, WordPress nur `/wp-admin/`. `/storyideen` ist frei → OAI-AdsBot darf crawlen. **Nichts zu tun.**
- [x] **Punkt 4 — Pixel angelegt:** „Mum Life Balance Pixel", Pixel-ID `VanFa9UJwn47VgwSWc1goK`
- [x] **Punkt 5 — Conversion-Ereignis angelegt:** „Kauf Storyideen", Schlüssel `order_created`, Attributionsfenster 30 Tage
- [ ] **Basiscode in ThriveCart einbauen** (Checkout → Tracking, Kopfbereich) — auf Verkaufs-/Checkout-Seite:
  ```html
  <script>!function(w,d,s,u){if(w.oaiq)return;var q=function(){q.q.push(arguments)};q.q=[];w.oaiq=q;var j=d.createElement(s);j.async=1;j.src=u;var f=d.getElementsByTagName(s)[0];f.parentNode.insertBefore(j,f)}(window,document,"script","https://bzrcdn.openai.com/sdk/oaiq.min.js");oaiq("init",{pixelId:"VanFa9UJwn47VgwSWc1goK"});</script>
  ```
- [ ] **Event-Code auf der Danke-/Erfolgsseite** (nach dem Basiscode) — feuert nur bei Kauf:
  ```html
  <script>oaiq("track","order_created");</script>
  ```
  *(Stufe 2 später: Bestellwert mitschicken → `oaiq("track","order_created",{value:19,currency:"CHF"});`)*
- [ ] **Punkt 6 — noindex** der Danke-/Erfolgsseite (ThriveCart-Erfolgsseiten sind i. d. R. eh nicht indexiert — beim Einbau prüfen)
- [ ] **Punkt 7 — Messung prüfen** mit „Pixel Helper"-Browser-Erweiterung (Besuch + Event grün)
- [ ] **Punkt 8 — UTM** am Anzeigen-Link: `?utm_source=chatgpt&utm_campaign=fruehstart` (beim Kampagnen-Bau)
- [ ] **Schritt 4 (OpenAI):** Conversion-Ereignis mit der Kampagne verknüpfen (beim Deploy)
- [x] **Verkaufsseite:** Block 6B „Warum Storys verkaufen" live (Message-Match-Anker)

**Nächster Schritt:** Basiscode + Event-Code in ThriveCart einbauen (Checkout → Tracking), dann mit Pixel Helper testen.

---

## 🔗 Verwandte Notizen
- [[90-storyideen-networkerinnen-salespage]] — Block 6B ist der Message-Match-Anker
- [[2026-08-28-storyideen-mama-nebenbei]] — Meta-Pendant (pausiert)
