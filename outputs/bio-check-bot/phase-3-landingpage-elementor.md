---
tags: [tools, bot]
---

# Phase 3 — WordPress-Landingpage in Elementor

**Stand:** 2026-04-23
**URL später:** `https://mumlifebalance.ch/bio-check`
**Stil-Vorbild:** Kati's visionaryBRAND Community (Problem → Lösung → Beweis → CTA)
**Adaptiert für:** Bio-Check-Bot + Patricia-Voice + Network-Mamas

---

## 🎨 Brand-Werte für Elementor-Theme-Einstellungen

Bevor du startest, **prüfe deine Elementor Site-Settings** (Hamburger-Menü oben links → Site Settings → Design System):

**Farben:**
| Name | Hex |
|---|---|
| Primary (Orange) | `#dc822e` |
| Secondary (Dunkelblau) | `#29556d` |
| Accent (Petrol) | `#12828c` |
| Background (Creme) | `#f1ecdd` |
| Text | `#0c1c30` |

**Typografie:**
- Primäre Schrift (Überschriften): **Philosopher** (Google Font — eventuell in Elementor → Site Settings → Typography hinzufügen)
- Sekundäre Schrift (Body): **Source Sans Pro** oder **Source Sans 3**

---

## 📐 Seitenstruktur (7 Sektionen)

```
1. Hero              → Headline + Sub + CTA-Button "Bio-Check starten"
2. Problem           → „Deine Bio verkauft gegen dich"
3. Solution          → Was der Bot macht (Schaufenster-Metapher)
4. Benefits          → 4 Bullet-Punkte (was bekommst du)
5. About Patricia    → Autorität + persönliche Story
6. CTA + Formular    → Das Anmelde-Formular (AC-Embed)
7. Footer            → Impressum/Datenschutz-Links
```

Geschätzte Build-Zeit in Elementor: **60-90 Min**.

---

## 🚀 Setup in WordPress

1. **WordPress einloggen** → Seiten → **Erstellen** → Neue Seite
2. Titel: `Bio-Check für Network-Mamas`
3. Slug: `/bio-check` (unter "Permalink")
4. Klick auf **Mit Elementor bearbeiten**
5. Layout wählen: **Elementor Canvas** (ohne Theme-Header/Footer — weniger Ablenkung)

---

## 🎬 Sektion 1 — Hero

**Elementor:** Neue Sektion → 2 Spalten (links Text 60%, rechts Bild 40%)

**Hintergrund:** Creme `#f1ecdd`
**Padding:** Top 80px · Bottom 60px

### Linke Spalte — Text

**Elementor-Widgets (von oben nach unten):**

1. **Heading (H1)** — Philosopher, 44-52px, Farbe `#29556d`
   ```
   Dein Bio-Check für Network-Mamas
   ```

2. **Heading (H2)** — Philosopher, 28-32px, Farbe `#dc822e`
   ```
   In 10 Minuten zu einer Bio, die wirklich verkauft
   ```

3. **Text-Editor** — Source Sans Pro, 18-20px, Farbe `#0c1c30`
   ```
   Deine Instagram-Bio entscheidet in 3 Sekunden, ob jemand bleibt — oder weiter scrollt. Ich zeig dir wie du aus „Krimskrams im Schaufenster" ein klares Versprechen machst, das deine Leute anzieht.
   ```

4. **Button** — Orange `#dc822e`, Weiß-Text, 16-18px, Padding 16px/32px, Border-Radius 12px
   - Text: `Jetzt kostenlosen Bio-Check starten 🌿`
   - Link: `#anmelden` (springt zum Formular unten)

5. **Text-Editor (klein)** — 13-14px, Farbe `#12828c`
   ```
   Kostenlos · 10 Minuten · Sofortiger PDF-Download per Mail
   ```

### Rechte Spalte — Bild

**Image-Widget** mit einem deiner Shootingbilder (authentisch, keine Stockfotos):
- Empfehlung: Foto von dir am Laptop / am Handy → wirkt mehr nach „Business-Mentorin"
- Alternative: Ein Mockup vom Bio-Check-Bot-Screenshot auf einem iPhone (kann ich dir als Illustration bauen, wenn du willst)

Oder: Ein Bild aus `context/Shootingbilder/` (du kennst den Bestand besser als ich)

**Mobile:** Rechte Spalte unter linke stapeln

---

## 🧠 Sektion 2 — Problem Awareness

**Elementor:** Neue Sektion, 1 Spalte, volle Breite
**Hintergrund:** Weiß
**Padding:** Top 80px · Bottom 80px
**Container-Breite:** Max 760px (zentriert)

### Widgets:

1. **Heading (H2)** — Philosopher, 36-44px, Farbe `#29556d`, zentriert
   ```
   Du postest, postest, postest — und trotzdem kommen keine Anfragen
   ```

2. **Text-Editor** — Source Sans Pro, 18-20px, Zeilenhöhe 1.6, Farbe `#0c1c30`
   ```
   Kennst du das?

   Du machst Content. Du zeigst deine Produkte. Du gibst Tipps. Und trotzdem — die Menschen, die auf deinem Profil landen, folgen dir nicht. Oder folgen dir, fragen aber nie nach.

   Die Wahrheit ist unbequem: Deine Bio ist das erste, was sie lesen. In 3 Sekunden entscheidet sich, ob sie bleiben oder weiter scrollen.

   Und wenn in deinem Schaufenster „Ich verkaufe Öle / Shakes / Putzmittel" steht — denken sie „aha, Verkäuferin" und gehen weiter. So einfach.

   **Niemand wacht morgens auf und denkt: Shit, ich brauche unbedingt Öle. 😅**

   Aber viele Mamas wachen auf mit einem konkreten Problem: „Ich schlafe seit Monaten schlecht", „Ich halt den Mental Load nicht mehr aus", „Ich hab keine Energie mehr". DAS ist dein Thema. Und DAS muss in deine Bio.
   ```

3. **Spacer** — 20px

4. **Button** — Orange, 16px, „Outline"-Stil (Transparenter Hintergrund, orangener Rand)
   - Text: `Ich will meine Bio fixen 🌿`
   - Link: `#anmelden`

---

## ✨ Sektion 3 — Solution

**Elementor:** Neue Sektion, 1 Spalte, Creme `#f1ecdd` Hintergrund
**Padding:** Top 80px · Bottom 80px
**Container:** Max 760px

### Widgets:

1. **Heading (H2)** — Philosopher, 36-44px, Farbe `#29556d`, zentriert
   ```
   Der Bio-Check macht das in 10 Minuten
   ```

2. **Text-Editor** — 18px
   ```
   Ich hab einen interaktiven Bot gebaut, der dich Schritt für Schritt durch deine Bio führt. Entweder er **analysiert deine bestehende Bio** und zeigt dir wo's hakt — oder er hilft dir **komplett neu zu bauen**, wenn du bei 0 startest.

   Er fragt dich 8 Schlüsselfragen (basierend auf meiner Methodik aus „Finde dein Thema" + Julia Trosts Instagram-A-Z-Framework) — und liefert dir am Ende:
   ```

3. **Icon-List** (Elementor-Widget) mit 5 Items
   Icon: ✓ in Orange, Text in Dunkelblau
   - `Deinen persönlichen Experten-Satz in 3 Varianten`
   - `5 fertige Bio-Vorschläge (150 Zeichen, copy-paste-ready)`
   - `3 Pinned-Posts-Ideen für dein Schaufenster`
   - `Struktur für deine Highlights-Alben`
   - `Alles als schönes PDF per E-Mail`

4. **Heading (H3)** — 24-28px, Farbe `#dc822e`, zentriert
   ```
   Warum ich das baue?
   ```

5. **Text-Editor** — kursiv
   ```
   Weil ich sehe, wie viele Mamas im Network Jahre verlieren, weil sie sich über ihr Produkt definieren statt über ihr Thema. Das muss nicht sein. Und dein Business verdient mehr.
   ```

---

## ⭐ Sektion 4 — Benefits (4 Karten)

**Elementor:** Neue Sektion, 1 Spalte (aber innerhalb: Flexbox mit 4 Karten)
**Hintergrund:** Weiß
**Padding:** Top 80px · Bottom 80px

### Überschrift:

1. **Heading (H2)** — Philosopher, 36-44px, zentriert
   ```
   Das bringt dir der Bio-Check
   ```

2. **Text-Editor** (klein) — zentriert, 16px, grau
   ```
   Nach 10 Minuten kannst du:
   ```

### 4 Benefit-Karten (Elementor Container oder Flexbox, 2×2 auf Desktop, 1×4 auf Mobil)

Jede Karte:
- Hintergrund: Creme `#f1ecdd`
- Border-Radius: 14px
- Padding: 28px
- Icon oben (großes Emoji oder Font-Awesome, Orange)
- Heading (H3) — 22px, Dunkelblau
- Text — 16px

**Karte 1:**
- Icon: 🎯
- Heading: `Klarheit statt Rätselraten`
- Text: `Du weisst endlich genau, wofür du stehst — und kannst es in einem Satz erklären. Ohne „äääh".`

**Karte 2:**
- Icon: 📱
- Heading: `Eine Bio, die verkauft`
- Text: `5 Varianten in deiner Tonalität, die du direkt einsetzen kannst. Keine Copy-Paste-Texte, sondern auf dich zugeschnitten.`

**Karte 3:**
- Icon: 🏬
- Heading: `Ein Schaufenster, das anzieht`
- Text: `Pinned Posts + Highlights passend zu deiner Bio. Ein komplettes Set-up, nicht nur ein Text.`

**Karte 4:**
- Icon: 🎁
- Heading: `PDF zum Nachlesen`
- Text: `Alles landet bei dir in der Mailbox. Drucken, durchgehen, umsetzen — in deinem Tempo.`

---

## 👋 Sektion 5 — About Patricia

**Elementor:** 2-Spalten-Sektion (links Bild 40%, rechts Text 60%)
**Hintergrund:** Creme `#f1ecdd`
**Padding:** Top 80px · Bottom 80px

### Linke Spalte — Bild

- Dein Profilbild (Shootingbild, warm, lächelnd)
- Runde Maske oder sanfte Border-Radius 20px
- Max-Width 360px

### Rechte Spalte — Text

1. **Heading (H2)** — 32-36px, Philosopher, Farbe `#29556d`
   ```
   Hey, ich bin Patricia 🌿
   ```

2. **Text-Editor** — 18px
   ```
   Ich bin 4-fach-Mama, doTERRA-Botschafterin (seit 7 Jahren im Network) und Mentorin für Networkerinnen, die aus ihrem Hobby ein echtes Business bauen wollen — zeitlich UND finanziell unabhängig.

   Mein Weg hat mich viele Fehler gekostet, bevor ich's verstanden hab: Es geht NIE ums Produkt. Es geht immer um das Problem, das du mit dem Produkt gelöst hast — das ist dein Thema.

   Seitdem begleite ich andere Network-Mamas auf diesem Weg. Und der Bio-Check ist der kleinste, aber ehrlichste erste Schritt, den ich dir geben kann.

   **Mein Ziel:** Finanzielle Unabhängigkeit für Mamas — ein für alle Mal. Ohne dass sie ihre Kinder nicht selber betreuen können.
   ```

3. **Button** (klein, Secondary-Style)
   - Text: `Mehr über mich →`
   - Link: `https://mumlifebalance.ch/ueber-mich` (oder deine Über-mich-Seite)

---

## 🎯 Sektion 6 — CTA + Anmelde-Formular

**Elementor:** Neue Sektion, volle Breite, dunkler Hintergrund für Kontrast
**Hintergrund:** Dunkelblau `#29556d`
**Padding:** Top 80px · Bottom 80px
**Anker-ID:** `anmelden` (Elementor-Widget-Einstellung → Advanced → ID)

### Widgets:

1. **Heading (H2)** — Philosopher, 36-44px, Farbe Weiß, zentriert
   ```
   Bereit für deinen Bio-Check?
   ```

2. **Text-Editor** — 18-20px, Farbe `#f1ecdd`, zentriert, max 560px
   ```
   Trag dich unten ein und du bekommst in wenigen Minuten deinen persönlichen Bot-Link per Mail. Keine Kosten. Kein Abo. Keine versteckte Agenda.

   Am Ende hast du eine Bio, mit der du dich nicht mehr verstecken musst.
   ```

3. **Spacer** — 20px

4. **HTML-Widget** mit dem AC-Formular-Embed-Code

   Elementor-Widget **HTML** einfügen und folgenden Code einsetzen (hol den konkreten Embed-Code aus AC → Forms → Bio-Check Anmeldung → „Integrate" → „HTML"):

   ```html
   <div style="max-width:480px;margin:0 auto;background:#f1ecdd;padding:32px;border-radius:14px;">
     <!-- AC-Embed-Code hier einfügen -->
     <!-- z.B. <script src="https://mumlifebalance.activehosted.com/f/embed.php?id=XX"></script> -->
   </div>
   ```

   **Alternative falls AC-Standard-Form zu hässlich:** Baue das Formular in Elementor Pro's **Form-Widget** und stell AC als Integration ein (Elementor Pro → Actions after Submit → ActiveCampaign).

5. **Text-Editor (klein)** — 12-13px, Farbe `#f1ecdd`, zentriert
   ```
   Deine Daten sind bei mir sicher. Du kannst dich jederzeit abmelden. Datenschutz: [Link]
   ```

---

## 🦶 Sektion 7 — Footer

**Elementor:** Kleine Sektion, Creme `#f1ecdd`
**Padding:** Top 40px · Bottom 40px
**Container:** Max 760px, zentriert

### Widgets:

1. **Text-Editor** — klein, zentriert, 14px, Farbe `#29556d`
   ```
   © 2026 Patricia Ulmann · mumlifebalance
   [Impressum](/impressum) · [Datenschutz](/datenschutz)
   ```

---

## 📱 Mobile Optimierung

Nach dem Bau — **Elementor Responsive-Ansicht** oben rechts (Tablet/Mobil-Icon) prüfen:

- **Hero:** Bild unter Text stapeln (auf Tablet+Mobil)
- **Benefit-Karten:** 2×2 auf Tablet, 1×4 auf Mobil
- **About Patricia:** Bild zentriert oben, Text darunter auf Mobil
- **Schriftgrössen:** Überschriften auf Mobil um 20-30% reduzieren (Elementor hat Responsive-Settings pro Widget)

---

## ✅ Checklist vor Launch

- [ ] AC-Formular-Embed eingebaut und getestet (Test-Eintragung mit echter Mail)
- [ ] Mail 1 kommt an nach Anmeldung
- [ ] Alle Links funktionieren (Button → Formular-Anker)
- [ ] Mobile-Ansicht ok
- [ ] Impressum + Datenschutz verlinkt
- [ ] SEO-Meta: Titel + Beschreibung gesetzt (Yoast SEO oder RankMath)
  - Titel: `Bio-Check für Network-Mamas | mumlifebalance.ch`
  - Beschreibung: `Kostenloser interaktiver Bio-Check. In 10 Min zu einer Instagram-Bio, die verkauft. Für Network-Mamas von Patricia Ulmann.`
- [ ] Favicon / Logo passt
- [ ] Ladezeit getestet (pagespeed.web.dev) — unter 3s ist Ziel

---

## 🎨 Zusatz: Bilder für die Seite

Wenn du Bilder brauchst, die ich **live rendern** kann:

- **Bot-Mockup auf iPhone-Screen** — kann ich als HTML/SVG generieren wenn du willst
- **Feature-Icons** — Emojis reichen aber meist

Für echte Patricia-Fotos: deine eigenen Shootingbilder aus `context/Shootingbilder/` — die sind authentischer als jedes Stock-Foto.

---

## 🤔 Wenn du Elementor nicht komplett magst

**Alternative:** Ich bau dir eine komplette HTML/CSS-Seite als Single-File, die du in einem **HTML-Widget** auf einer leeren Elementor-Seite einfügst. Dann musst du gar nichts selbst bauen — nur Copy-Paste.

Sag Bescheid, welchen Weg du willst.
