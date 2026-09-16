---
tags: [funnel, produkt, reference]
---

# Link-Übersicht — alle Angebote auf einen Blick

**Stand:** 16.09.2026 · **Alle Links am 16.09.2026 mit `curl` geprüft**, Status-Codes in der Spalte rechts.

**Vier Linkarten je Angebot** — genau die, die Patricia in der Story braucht:
**Landingpage** (mumlifebalance.ch) · **ThriveCart** (Kasse) · **Auslieferung** (was die Kundin bekommt: PDF, Bot, Tool) · **Telegram** (die Gruppe zum Angebot).
Ein `—` heisst: gibt es nicht. Eine Lücke bleibt sichtbar, statt geraten zu werden.
Bei jeder Änderung hier nachführen. Skills, die Links in Captions/Mails setzen, lesen diese Datei statt zu raten.

---

## 🌿 doTERRA — Profil „Mama Regeneration & Energie"

| Was | Keyword | Landingpage | Bestellen | Auslieferung | Telegram | Status |
|---|---|---|---|---|---|---|
| 🔗 **Bio-Link-Seite** (gehört in die Instagram-Bio) | — | https://mumlifebalance.ch/hormone/ | — | — | — | 🟢 200 · WP 4078 |
| **0€ Energie-Kickstart** | `ENERGIE` | https://mumlifebalance.ch/energie-kickstart/ | — | 3-Tage-Mail-Challenge, kein PDF | — | 🟢 200 · WP 3911 |
| **0€ Mini-Notfallapotheke** (10 S., 3 Hausmittel) | 🔴 fehlt | https://mumlifebalance.ch/mini-notfallapotheke-fuer-mamas/ | — | PDF, 22 MB · nur OneDrive, nicht in Drive | — | 🟢 200 · WP 2906 · Inhalt: `context/doterra/mini-notfallapotheke.md` |
| **E-Book ätherische Öle** | — | https://mumlifebalance.ch/ebook/ | — | E-Book (AC-Automation 29) | https://t.me/+Oh0T-nYDzUJmNTNk | 🟢 200 |
| **Guide doTERRA Business** | — | https://mumlifebalance.ch/mama-unternehmen/ | — | Guide (AC-Automation 28) | https://t.me/+Oh0T-nYDzUJmNTNk | 🟢 200 |
| **Mama wird Hausapothekerin** (Programm) | — | https://mumlifebalance.ch/mama-wird-hausapothekerin/ | kein Checkout | 61-S.-Workbook + MP3 + 5 Videos, ~159 MB | — | 🟢 **aktiv** — wird beim Kauf der Hausapotheke ausgeliefert · ⚠️ Seiteninhalt veraltet, Produkt nicht |
| **Startersets** | — | https://mumlifebalance.ch/startersets/ | — | — | — | 🟢 200 |
| **Produktpaket 21-Tage-Energie-Routine** | — | — | https://doterra.me/b0yKEX | — | — | 🟢 200 · vorgefüllter Warenkorb · ⚠️ nicht auf ≥150 PV geprüft |
| **Ölreise** | — | https://mumlifebalance.ch/oelreise/ | — | — | — | 🟢 200 · ⚠️ Inhalt veraltet |
| Öl-Wissen-Bot / Team-Companion | — | — | — | https://bot.mumlifebalance.ch | — | 🟢 200 · 🚫 **NUR Kundinnen und Team — nie öffentlich verlinken** |
| Telegram-Kanal „Gesund durchs ganze Jahr" | — | — | — | — | Chat-ID -1002221396127 | 🟢 live · ⚠️ **Einladungslink fehlt** |

### ✅ Erledigt am 24.08.2026 — die Seite ist online

Die Landingpage war seit dem 8. Juli als leerer Entwurf in WordPress (nur ein Platzhalter-Satz im Content). Am 24.08. wurde das fertige Markup per API eingespielt, das gescopte CSS in den Customizer gehängt und die Seite veröffentlicht. Beide Ansichten sind geprüft: mobil (375px) und Desktop (1280px) ohne horizontalen Überstand, Fotos geladen, AC-Formular 64 vollständig inklusive funktionierendem reCAPTCHA.

**Ein Fehler wurde dabei gefunden und behoben:** Das reCAPTCHA-Widget ist fest 304px breit und blähte auf dem Handy die Grid-Spalte auf 358px auf, weil Grid-Items standardmässig `min-width: auto` haben. Fix: `minmax(0,1fr)` plus `min-width:0` auf den Grid-Kindern, dazu das reCAPTCHA unter 430px auf 80 % skaliert.

⚠️ **Die Seite ab jetzt nicht mehr im WordPress- oder Elementor-Editor öffnen** — ein Speichern dort wirft den per API eingefügten Inhalt raus. Änderungen laufen über `scripts/wordpress/deploy-energie-kickstart.mjs`.

⚠️ **Offen:** Das PV-Paket hinter `doterra.me/b0yKEX` ist weiterhin nicht auf ≥ 150 PV geprüft.

---

## 💼 Mentoring — Profil „Mum Life Balance"

### 0€ Freebies

| Freebie | Keyword | Landingpage | ThriveCart | Auslieferung | Telegram | Status |
|---|---|---|---|---|---|---|
| Workbook „Von 0 auf echt" | `ECHT1` | https://mumlifebalance.ch/von-0-auf-echt/ | — | /_blob/45f60d981421530fea57e1c635546237 (PDF, 25 S.) | — | 🟢 200 (16.09.2026) · WP 3836 |
| 0€ Fahrplan „Von Produktposts zu doppeltem Einkommen" | `SYSTEM` / `FAHRPLAN` | https://mumlifebalance.ch/fahrplan/ | — | /_blob/25a9e0c778b14319e666cf968eb123fe (PDF) | — | 🟢 200 (16.09.2026) · WP 3842 |
| 0€ Starter-Guide Instagram | `SICHTBAR` / `ANLEITUNG` | https://mumlifebalance.ch/instagram-starterguide/ | — | /_blob/43bb5e33cd93df89cb5955079b331ce3 (PDF, 17 S.) | — | 🟢 200 |
| Lead-Challenge 3-Tage-Workbook | `LEAD` | https://mumlifebalance.ch/lead-challenge/ | https://mumlifebalance.thrivecart.com/challenge-lead-magnet/ | /_blob/bd461524b5b2efa42c9e3109449c0f42 (PDF, 13 S.) | https://t.me/+lXiK5ZAigFIzZWY0 | 🟢 200 (16.09.2026) · WP 3820 · AC-Automation 47 |
| Story-Challenge 7-Tage | `STORY` | https://mumlifebalance.ch/story-challenge/ | — | /_blob/bcb120da59f69fcaba91934deeafa3b9 (PDF, 20 S.) | https://t.me/+S-4YWyCtH45mZDE0 | 🟢 200 · ⚠️ ManyChat-Keyword noch nicht angelegt · AC-Automation 45 |
| 0€ Potenzial-Test / Quiz | `QUIZ` | https://mumlifebalance.ch/potenzial-test/ | — | Quiz auf der Seite · Danke: https://mumlifebalance.ch/dankesseite-potenzial-quiz/ | — | 🟢 200 |
| Bio-Check (interaktiver Bot) | `BIO` | https://mumlifebalance.ch/bio-check/ | — | https://bio-check-bot.vercel.app | — | 🟢 200 · 🚨 `bio-check.mumlifebalance.ch` löst **nicht** auf (16.09.2026) — nie verlinken |
| Freischaufeln / To-Do-Liste halbieren | `ZEIT` | https://mumlifebalance.ch/freischaufeln/ | — | https://freischaufeln.vercel.app | — | 🟢 200 |
| Produkt-Ideen-Finder (KI-Tool) | — | https://mumlifebalance.ch/produkt-ideen-finder/ → leitet auf `-los/` | — | https://produkt-ideen-finder-service.vercel.app/ | — | 🟢 200 · WP 4085 (4083 ist Entwurf) |
| Mama-Business-Bootcamp (5 Tage, PIA) | — | https://mumlifebalance.ch/bootcamp/ | — | https://mumlifebalance.ch/bootcamp-willkommen/ | https://t.me/+HW6lvdlbTBhiOWM0 | 🟢 200 · AC-Formular 60 |

### Bezahlte Angebote

| Produkt | Preis | Landingpage | ThriveCart | Auslieferung | Telegram | Status |
|---|---|---|---|---|---|---|
| **Storyideen für Networkerinnen** (+ Content-Box-Bump 17) | 19 | https://mumlifebalance.ch/storyideen/ | https://mumlifebalance.thrivecart.com/storyideen/ | /_blob/f4e65f7dcf7d82c94c07ca968a83cac3 (PDF, 47 S.) | — | 🟢 200 · Seite WP 4032 (v2 seit 16.09.) |
| **Content-Box** (30 Hook-Vorlagen) | 17 | https://mumlifebalance.ch/content-box/ | https://mumlifebalance.thrivecart.com/content-box/ | PDF-Workbook | — | 🟢 200 · WP 3913 · läuft vor allem als Bump |
| Finde dein Thema als Network-Mama | 39 | — | https://mumlifebalance.thrivecart.com/thema-finden/ | — | — | 🟢 200 · ⚠️ keine Landingpage |
| Vom Network-Wissen zum eigenen Produkt | 39 | — | https://mumlifebalance.thrivecart.com/eigene-produkterstellung/ | — | https://t.me/+ukSgKKB5hZdiNTQ0 | 🟢 200 · AC-Automationen 48 + 51 |
| Expertin statt Verkäuferin | 97 | — | https://mumlifebalance.thrivecart.com/expertin/ | — | — | 🟢 200 · ⚠️ keine Landingpage |
| Instagram-Kundenmaschine | 333 | — | https://mumlifebalance.thrivecart.com/instagram-kundenmaschine/ | — | https://t.me/+s6yEn-RiXZw3Nzg8 | 🟢 200 · AC-Automation 44 |
| Mama-CEO | 333 | https://mumlifebalance.ch/mama-ceo/ | https://mumlifebalance.thrivecart.com/mama-ceo/ | — | https://t.me/+ZLzeEEok6A02MjRk | 🟢 200 · WP 3444 · AC-Automation 62 |
| Digitale Produktwelt | 333 | — | https://mumlifebalance.thrivecart.com/digitale-produktwelt/ | — | https://t.me/+ukSgKKB5hZdiNTQ0 | 🟢 200 |
| **MBA (Bundle)** | Pioneer 997 / Liste 1347 | https://mumlifebalance.ch/mba/ · Warteliste https://mumlifebalance.ch/mba-warteliste/ · Replay https://mumlifebalance.ch/mba-webinar-replay/ | https://mumlifebalance.thrivecart.com/mba/ | — | — | 🟢 200 · ⚠️ nie aus Evergreen zum 1347er-Link |
| 1:1 „Aus Nebenbei wird Business" | Beta 777 statt 1500 | — | https://mumlifebalance.thrivecart.com/aus-nebenbei-wird-business/ | — | — | 🟢 200 |

### Sonstige Seiten

| Was | Link | Status |
|---|---|---|
| Angebots-Übersicht | https://mumlifebalance.ch/angebote | 🟢 200 |
| MBA-Warteliste | https://mumlifebalance.ch/mba-warteliste | 🟢 200 |
| Blog | https://mumlifebalance.ch/blog/ | 🟢 200 |

### Rechtliches — gehört in den Footer jeder Landingpage

| Was | Link | Status |
|---|---|---|
| Impressum | https://mumlifebalance.ch/impressum/ | 🟢 200 (geprüft 13.09.2026) |
| Datenschutzerklärung | https://mumlifebalance.ch/datenschutzerklaerung/ | 🟢 200 (geprüft 13.09.2026) |
| AGB | — | 🔴 **existiert nicht** — `/agb/`, `/widerruf/`, `/nutzungsbedingungen/` liefern 404 |

⚠️ **Keinen AGB-Link in einen Footer setzen**, solange die Seite nicht existiert — ein toter Rechtslink ist schlimmer als keiner. Beim Verkauf greifen bis dahin die Bedingungen, die ThriveCart im Checkout anzeigt.

⚠️ **Preis-Integrität MBA:** Nie aus einem Evergreen-Produkt direkt zum 1347er-Link verlinken — das widerspricht dem 997er-Event-Preis.

---

## 🔗 Die Bio-Link-Seite — /hormone/

**Live seit 24.08.2026.** Das ist der einzige Link, der in die Instagram-Bio des doTERRA-Profils gehört. Aufbau in der Reihenfolge, in der eine Frau denkt:

1. **Hero** — Foto, Positionierungssatz, die drei Symptome als Chips („müde trotz Schlaf", „Haare im Bürstenkamm", „Kopf wie in Watte")
2. **Block „Für dich"** — der Energie-Kickstart als grosse orange Karte, darunter die Einladung zur DM
3. **Der Brückensatz** — *„Ich hab mit meinem eigenen Körper angefangen. Heute greift meine ganze Familie darauf zurück."*
4. **Block „Für deine Familie"** — Hausapothekerin, Mini-Notfallapotheke, Ölreise
5. **Kontakt** — Instagram-DM und E-Mail

**Warum diese Reihenfolge:** Das Hormon-Thema ist der Eingang, die Hausapotheke die Erweiterung. Wer über ein Reel kommt, findet oben genau ihr Problem; wer schon Kundin ist, scrollt zum zweiten Block. Damit bleibt die Positionierung vorne scharf, ohne dass die bestehenden Familien-Angebote verloren gehen.

**Regel für diese Seite:** kein Markenname, kein Preis, kein Shop-Link — und **kein Link auf den Bot**, der ist Kundinnen und Team vorbehalten. Alle ausgehenden Links am 24.08. geprüft, alle 200.

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
- **Den Öl-Bot öffentlich verlinken** — `bot.mumlifebalance.ch` heißt „Patricia's doTERRA-Assistentin“, nennt die Marke im ersten Satz und zeigt einen Team-Login. Der Link gehört in die Willkommens-Mail nach dem Kauf, nie auf eine öffentliche Seite.

---

## 🔗 Verwandte Notizen
- [[2026-strategie-einschreibungen-botschafterinnen]] · [[2026-09-doterra]] · [[energie-story-profil]] · [[doterra-jahresrhythmus]]
