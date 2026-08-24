---
tags: [funnel, produkt, reference]
---

# Link-Übersicht — alle Angebote auf einen Blick

**Stand:** 24.08.2026 · **Alle Links am 24.08.2026 mit `curl` geprüft**, Status-Codes unten.
Bei jeder Änderung hier nachführen. Skills, die Links in Captions/Mails setzen, lesen diese Datei statt zu raten.

---

## 🌿 doTERRA — Profil „Mama Regeneration & Energie"

| Was | Link | Status |
|---|---|---|
| 🔗 **Bio-Link-Seite** (das gehört in die Instagram-Bio) | https://mumlifebalance.ch/hormone/ | 🟢 **live seit 24.08.2026** (WP 4078) · mobil geprüft |
| **0€ Freebie: 3-Tage-Energie-Kickstart** | https://mumlifebalance.ch/energie-kickstart/ | 🟢 **live seit 24.08.2026** (WP 3911) · mobil + Desktop geprüft |
| Keyword-Weg zum selben Freebie | Kommentar/DM **`ENERGIE`** → ManyChat-Flow | 🟢 live (Flow „0€ Produkt Energie-Kickstart") |
| **Produktpaket 21-Tage-Energie-Routine** | https://doterra.me/b0yKEX | 🟢 200 — vorgefüllter Warenkorb |
| Öl-Wissen-Bot / Team-Companion | https://bot.mumlifebalance.ch | 🟢 200 |
| Ältere doTERRA-Seiten | /mama-wird-hausapothekerin · /oelreise | 🟢 200 (Inhalt veraltet, passt nicht zur neuen Positionierung) |
| Telegram-Kanal „Gesund durchs ganze Jahr" | Chat-ID -1002221396127 | 🟢 live · ⚠️ **Einladungslink fehlt in der Doku** — bitte nachtragen |

### ✅ Erledigt am 24.08.2026 — die Seite ist online

Die Landingpage war seit dem 8. Juli als leerer Entwurf in WordPress (nur ein Platzhalter-Satz im Content). Am 24.08. wurde das fertige Markup per API eingespielt, das gescopte CSS in den Customizer gehängt und die Seite veröffentlicht. Beide Ansichten sind geprüft: mobil (375px) und Desktop (1280px) ohne horizontalen Überstand, Fotos geladen, AC-Formular 64 vollständig inklusive funktionierendem reCAPTCHA.

**Ein Fehler wurde dabei gefunden und behoben:** Das reCAPTCHA-Widget ist fest 304px breit und blähte auf dem Handy die Grid-Spalte auf 358px auf, weil Grid-Items standardmässig `min-width: auto` haben. Fix: `minmax(0,1fr)` plus `min-width:0` auf den Grid-Kindern, dazu das reCAPTCHA unter 430px auf 80 % skaliert.

⚠️ **Die Seite ab jetzt nicht mehr im WordPress- oder Elementor-Editor öffnen** — ein Speichern dort wirft den per API eingefügten Inhalt raus. Änderungen laufen über `scripts/wordpress/deploy-energie-kickstart.mjs`.

⚠️ **Offen:** Das PV-Paket hinter `doterra.me/b0yKEX` ist weiterhin nicht auf ≥ 150 PV geprüft.

---

## 💼 Mentoring — Profil „Mum Life Balance"

### 0€ Freebies

| Freebie | Keyword | Link | Status |
|---|---|---|---|
| Workbook „Von 0 auf echt" | `ECHT1` | über ManyChat | — |
| 0€ Fahrplan „Von Produktposts zu doppeltem Einkommen" | `SYSTEM` / `FAHRPLAN` | über ManyChat | — |
| 0€ Starter-Guide Instagram | `SICHTBAR` / `ANLEITUNG` | https://mumlifebalance.ch/instagram-starterguide | 🟢 200 |
| Lead-Challenge 3-Tage-Workbook | `LEAD` | über ManyChat | — |
| Story-Challenge 7-Tage | `STORY` | https://mumlifebalance.ch/story-challenge/ | 🟢 200 · ⚠️ ManyChat-Keyword noch nicht angelegt |
| 0€ Potenzial-Test / Quiz | `QUIZ` | https://mumlifebalance.ch/potenzial-test/ | 🟢 200 |
| Bio-Check (interaktiver Bot) | `BIO` | https://mumlifebalance.ch/bio-check | 🟢 200 |
| Freischaufeln / To-Do-Liste halbieren | `ZEIT` | https://mumlifebalance.ch/freischaufeln | 🟢 200 |

### Bezahlte Angebote

| Produkt | Preis | Checkout | Status |
|---|---|---|---|
| **Storyideen für Networkerinnen** (+ Content-Box-Bump 17) | 19 | https://mumlifebalance.thrivecart.com/storyideen/ | 🟢 200 |
| Finde dein Thema als Network-Mama | 39 | https://mumlifebalance.thrivecart.com/thema-finden/ | 🟢 200 |
| Expertin statt Verkäuferin | 97 | https://mumlifebalance.thrivecart.com/expertin/ | 🟢 200 |
| Instagram-Kundenmaschine | 333 | https://mumlifebalance.thrivecart.com/instagram-kundenmaschine/ | 🟢 200 |
| Mama-CEO | Preis prüfen | https://mumlifebalance.thrivecart.com/mama-ceo/ | 🟢 200 |
| Digitale Produktwelt | Preis prüfen | https://mumlifebalance.thrivecart.com/digitale-produktwelt/ | 🟢 200 |
| **MBA (Bundle)** | Pioneer 997 / Liste 1347 | https://mumlifebalance.thrivecart.com/mba/ | 🟢 200 |
| 1:1 „Aus Nebenbei wird Business" | Beta 777 statt 1500 | https://mumlifebalance.thrivecart.com/aus-nebenbei-wird-business/ | 🟢 200 |

### Sonstige Seiten

| Was | Link | Status |
|---|---|---|
| Angebots-Übersicht | https://mumlifebalance.ch/angebote | 🟢 200 |
| MBA-Warteliste | https://mumlifebalance.ch/mba-warteliste | 🟢 200 |
| Blog | https://mumlifebalance.ch/blog/ | 🟢 200 |

⚠️ **Preis-Integrität MBA:** Nie aus einem Evergreen-Produkt direkt zum 1347er-Link verlinken — das widerspricht dem 997er-Event-Preis.

---

## 🔗 Die Bio-Link-Seite — /hormone/

**Live seit 24.08.2026.** Das ist der einzige Link, der in die Instagram-Bio des doTERRA-Profils gehört. Aufbau in der Reihenfolge, in der eine Frau denkt:

1. **Hero** — Foto, Positionierungssatz, die drei Symptome als Chips („müde trotz Schlaf", „Haare im Bürstenkamm", „Kopf wie in Watte")
2. **Block „Für dich"** — der Energie-Kickstart als grosse orange Karte, darunter die Einladung zur DM
3. **Der Brückensatz** — *„Ich hab mit meinem eigenen Körper angefangen. Heute greift meine ganze Familie darauf zurück."*
4. **Block „Für deine Familie"** — Hausapothekerin, Mini-Notfallapotheke, Ölreise, Wissens-Tool
5. **Kontakt** — Instagram-DM und E-Mail

**Warum diese Reihenfolge:** Das Hormon-Thema ist der Eingang, die Hausapotheke die Erweiterung. Wer über ein Reel kommt, findet oben genau ihr Problem; wer schon Kundin ist, scrollt zum zweiten Block. Damit bleibt die Positionierung vorne scharf, ohne dass die bestehenden Familien-Angebote verloren gehen.

**Regel für diese Seite:** kein Markenname, kein Preis, kein Shop-Link. Alle acht ausgehenden Links am 24.08. geprüft, alle 200.

**Ändern:** `scripts/wordpress/deploy-bio-link-seite.mjs` — nicht im WP-Editor öffnen.

---

## 🌉 Wie du doTERRA verbindest, ohne dass es nach doTERRA aussieht

Das ist die eigentliche Kunst, und sie hat eine einfache Regel:

> **doTERRA ist nie ein Ziel, immer eine Antwort.**
> Die Marke taucht erst auf, wenn jemand von sich aus gefragt hat.

### Die fünf Stufen — und wo die Marke erlaubt ist

| Stufe | Was die Frau sieht | doTERRA sichtbar? |
|---|---|---|
| **1. Feed** | Nur dein Thema: Hormone, Müdigkeit, Haarausfall, dein Leben | ❌ **Nie.** Kein Produktname, kein Logo, kein Fläschchen im Bild als Hauptmotiv |
| **2. Bio-Link** | Deine eigene Seite auf deiner eigenen Domain | ❌ **Nie.** Der Bio-Link darf niemals auf doterra.me oder mydoterra zeigen |
| **3. Freebie** | Dein Wissen: Protein, Bewegung, Schlaf | 🟡 Höchstens beiläufig als „was ich selbst nehme" |
| **4. DM / Gespräch** | Du fragst, sie erzählt, du hörst zu | 🟡 Erst wenn **sie** fragt „was nimmst du denn?" |
| **5. Cart-Link** | Das konkrete Paket | ✅ Jetzt ist es richtig — sie hat danach gefragt |

Der ganze Trick liegt zwischen Stufe 2 und 4: Wenn dein Bio-Link auf deine eigene Seite führt und diese Seite von *ihrem* Problem handelt statt von deinem Produkt, dann fühlt sich der ganze Weg wie Hilfe an und nicht wie ein Verkaufstrichter. Sobald der Bio-Link direkt in den doTERRA-Shop zeigt, kippt alles — dann bist du wieder die Beraterin, die was verkaufen will, und genau davor läuft deine Zielgruppe weg.

### Was auf deine Bio-Link-Seite gehört

Die Seite muss in drei Sekunden sagen: *„Ich weiss, wie du dich fühlst, und es hat einen Namen."* Konkret:

1. **Die Symptom-Liste als Überschrift** — müde trotz Schlaf, Haare im Bürstenkamm, Kopf wie in Watte. Sie soll nicken.
2. **Der Reframe** — das kann hormonell sein, es fängt früher an als alle denken, du bist nicht kaputt.
3. **Deine Geschichte in drei Sätzen** — Hormontest mit 35, was du geändert hast, wo du heute stehst.
4. **Ein einziger nächster Schritt** — das 3-Tage-Freebie. Nicht drei Optionen, eine.
5. **Kein Produkt, kein Preis, keine Marke.**

Diese Seite ist seit dem 24.08.2026 live: https://mumlifebalance.ch/energie-kickstart/ — sie gehört als Ziel in die Bio-Link-Seite.

### Der Satz, der die Brücke im Gespräch baut

Wenn sie fragt, was du nimmst, verkaufst du nicht das Produkt, sondern deine Begleitung:

> *„Ich nehm ein paar Sachen täglich, aber ehrlich gesagt bringt dir die Liste allein wenig — bei mir hat erst die Kombination aus Nährstoffen und dem, was ich sonst geändert hab, wirklich was bewegt. Wenn du magst, schau ich mir mit dir zusammen an, was bei dir dran wäre."*

Das ist dein Anker-Prinzip in einem Satz: Das Produkt kriegt sie überall, den Weg gibt es nur bei dir.

### Drei Dinge, die die Brücke kaputt machen

- **Bio-Link direkt in den Shop** — der häufigste Fehler und der teuerste
- **Produktfotos im Feed** — sobald Fläschchen das Hauptmotiv sind, bist du wieder Verkäuferin
- **Das Paket anbieten, bevor sie gefragt hat** — dann ist es ein Pitch, kein Rat

---

## 🔗 Verwandte Notizen
- [[2026-strategie-einschreibungen-botschafterinnen]] · [[2026-09-doterra]] · [[energie-story-profil]] · [[doterra-jahresrhythmus]]
