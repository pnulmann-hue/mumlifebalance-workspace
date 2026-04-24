# Phase 2 — ActiveCampaign Setup Bio-Check-Bot

**Stand:** 2026-04-23
**Ziel:** Formular auf Landingpage → E-Mail mit Bot-Link → Chat durchlaufen → PDF-Mail → 3 Pitch-Mails als Nurture

---

## ✅ Was Claude schon vorbereitet hat (via MCP)

7 Tags in AC erstellt:

| Tag-ID | Name | Zweck |
|---|---|---|
| 59 | `Bio-Check Lead` | Hat sich eingetragen |
| 60 | `Bio-Check abgeschlossen` | Hat Bot durchlaufen + PDF erhalten |
| 61 | `Bio-Check → Thema-Interesse` | Pitch-Klick „Finde dein Thema" |
| 62 | `Bio-Check → Expertin-Interesse` | Pitch-Klick „Expertin statt Verkäuferin" |
| 63 | `Bio-Check → Kundenmaschine-Interesse` | Pitch-Klick „Instagram-Kundenmaschine" |
| 64 | `Bio-Check → Insta-DM` | Klickt auf Insta-Safety-Net |
| 65 | `Bio-Check → braucht Freebie-Hilfe` | ManyChat-Keyword „LEADMAGNET" |

---

## 🛠️ TEIL A — Was du jetzt im AC-UI baust (45 Min)

### A1 — Liste „Bio-Check Kontakte" erstellen

1. AC einloggen: https://mumlifebalance.activehosted.com
2. Oben: **Kontakte** → Links: **Listen** → **Liste hinzufügen** (oben rechts)
3. Name: `Bio-Check Kontakte`
4. Von (Absendername): `Patricia Ulmann`
5. Von (Absender-Mail): `info@mumlifebalance.ch` (oder was du sonst verwendest)
6. URL: `https://mumlifebalance.ch/bio-check`
7. Erinnerung (Reminder): `Du hast dich für den kostenlosen Bio-Check eingetragen.`
8. **Speichern**
9. **Liste-ID notieren** (erscheint in der URL, z.B. `.../lists/25` → ID = 25)

### A2 — Custom Field „bio_check_pdf_url" erstellen

Dieses Feld speichert pro Kontakt den Link zum generierten PDF.

1. Oben: **Kontakte** → Links: **Felder** → **Feld hinzufügen**
2. Feldname: `bio_check_pdf_url`
3. Typ: **Textfeld** (oder „Single-line Text")
4. Sichtbar: nicht nötig (kein Haken bei „In Formular anzeigen")
5. **Speichern**
6. **Field-ID notieren** (in der URL oder in der Liste, z.B. `12`)

**⚠️ Wichtig:** Diese Field-ID musst du gleich in Vercel als ENV eintragen — siehe Teil C.

### A3 — Formular „Bio-Check Anmeldung" erstellen

1. Links: **Website** → **Formulare** → **Neues Formular hinzufügen**
2. Name: `Bio-Check Anmeldung`
3. Aktion: **Abonnieren** (Subscribe)
4. Liste: `Bio-Check Kontakte` (die von A1)
5. Formular-Typ: **Eingebettetes Formular** (Inline)
6. **Erstellen**

**Felder einbauen** (Formular-Editor):
- **Vorname** (required)
- **E-Mail** (required)
- Checkbox: *„Ich möchte den kostenlosen Bio-Check und Patricias E-Mail-Tipps rund um Positionierung und Instagram erhalten. Ich kann mich jederzeit abmelden. Datenschutz: [Link zu mumlifebalance.ch/datenschutz]"* (required)

**Actions (rechts oben im Editor: „Aktionen"):**
- Tag hinzufügen: `Bio-Check Lead`
- Optional: Automation starten („Bio-Check Auslieferung" — bauen wir in A4)

**Nach dem Absenden:**
- Option: Weiterleitung auf Danke-Seite `https://mumlifebalance.ch/bio-check-danke`
  (oder simple Success-Message: *„Super! In den nächsten Minuten kommt deine Mail mit dem Bot-Link. Check auch den Spam-Ordner."*)

**Integration-Code generieren:**
- Oben rechts: **Integrieren** → **Eingebettet (iframe)** oder **HTML-Code**
- Kopieren — den brauchen wir in Phase 3 (WordPress-Landingpage)

### A4 — Automation 1: „Bio-Check Auslieferung"

1. Oben: **Automationen** → **Neue Automation**
2. Name: `Bio-Check Auslieferung`
3. Von Grund auf neu erstellen (**Start from scratch**)

**Trigger (Startbedingung):**
- **Tag wird hinzugefügt** → Tag: `Bio-Check Lead`
- Läuft: **Einmal** (One time)

**Schritte:**

```
1. Warten: 1 Minute
2. E-Mail senden: [Mail 1 — siehe Teil B]
3. Warten: 24 Stunden
4. Bedingung: Hat Tag "Bio-Check abgeschlossen"?
   JA → Ende (bei der PDF-Automation weiter)
   NEIN → weiter zu Schritt 5
5. E-Mail senden: [Mail 2 — 24h-Reminder]
6. Ende
```

Aktiv schalten: **Aktivieren** (oben rechts)

### A5 — Automation 2: „Bio-Check PDF + Nurture"

1. **Automationen** → **Neue Automation**
2. Name: `Bio-Check PDF + Nurture`

**Trigger:**
- **Tag wird hinzugefügt** → `Bio-Check abgeschlossen`

**Schritte:**

```
1. Warten: 1 Minute
2. E-Mail senden: [Mail 3 — PDF-Lieferung]
3. Warten: 2 Tage
4. Bedingung: Hat Tag "Bio-Check → Thema-Interesse"?
   JA → Ende (Funnel 53 läuft schon)
   NEIN → weiter
5. E-Mail senden: [Mail 4 — Pitch 1 "Finde dein Thema"]
6. Warten: 3 Tage
7. Bedingung: Hat Tag "Bio-Check → Expertin-Interesse"?
   JA → Ende (Funnel 55 läuft schon)
   NEIN → weiter
8. E-Mail senden: [Mail 5 — Pitch 2 "Expertin statt Verkäuferin"]
9. Warten: 4 Tage
10. Bedingung: Hat Tag "Bio-Check → Kundenmaschine-Interesse"?
    JA → Ende (Funnel 54 läuft schon)
    NEIN → weiter
11. E-Mail senden: [Mail 6 — Pitch 3 "Instagram-Kundenmaschine"]
12. Ende
```

Aktiv schalten.

---

## 📧 TEIL B — Die 6 E-Mails (Copy-Paste ready)

### Mail 1 — Auslieferung (direkt nach Anmeldung)

**Betreff:** Dein Bio-Check ist startklar 🌿

**Preview-Text:** In 5-10 Min zu einer Bio, die wirklich verkauft

**Body:**

```
Hey %FIRSTNAME%,

schön, dass du da bist. Dein Bio-Check wartet auf dich.

Kurz, damit du weisst was dich erwartet:

In den nächsten 5-10 Minuten schauen wir uns deine Instagram-Bio an — entweder die bestehende (wir polieren) oder wir bauen eine neue von Grund auf. Am Ende hast du:

🌟 Deinen Experten-Satz in 3 Varianten
📱 5 fertige Bio-Vorschläge, copy-paste-ready
📌 3 Pinned-Posts-Ideen
🗂️ Struktur für deine Highlights
🎁 Alles als PDF per Mail zurück

Hier geht's los:

👉 https://bio-check.mumlifebalance.ch/?e=%EMAIL%&n=%FIRSTNAME%

(Falls der Link bei dir nicht klickbar ist: einfach komplett kopieren und in die Browser-Adressleiste.)

Keine Hektik. Du kannst jederzeit pausieren und später weitermachen.

Und eine kleine Sache zum Anfang — stell dir vor:

Du gehst an eine Hochzeit. Du hast ein richtig geiles violettes Kleid. Nur die Schuhe fehlen. Du läufst durch die Stadt und weisst: Ich brauche einen Schuh. Würdest du in einen Laden gehen, wo im Schaufenster lauter Krimskrams liegt? Nein. Du gehst da rein, wo klar ist: Hier gibt es Schuhe.

Deine Instagram-Bio ist dein Schaufenster. Genau DAS bauen wir heute.

Bis gleich auf der anderen Seite 💛

Patricia

—
mumlifebalance · Patricia Ulmann
Mentorin für Mamas im Network Marketing
```

---

### Mail 2 — 24h Reminder (wenn Bot nicht durchgelaufen)

**Betreff:** Dein Bio-Check wartet noch auf dich ✨

**Preview-Text:** 5 Minuten, dann hast du Klarheit

**Body:**

```
Hey %FIRSTNAME%,

gestern hast du dich für den Bio-Check eingetragen — aber ich sehe, du hast ihn noch nicht durchgezogen. Kein Druck. Ich weiss, Mama-Alltag.

Aber eine Erinnerung, warum du's trotzdem heute machen solltest:

Jeder Tag, an dem deine Bio „Krimskrams im Schaufenster" zeigt, verlierst du potenzielle Kundinnen. Nicht weil sie nicht interessiert wären — sondern weil sie in 3 Sekunden nicht verstehen, wofür du stehst. Und dann scrollen sie weiter.

5-10 Minuten. Mehr nicht. Und du hast danach:

• Deinen Experten-Satz
• 5 copy-paste-ready Bio-Vorschläge
• Struktur für Pinned Posts + Highlights
• Dein PDF zum Nachlesen

👉 https://bio-check.mumlifebalance.ch/?e=%EMAIL%&n=%FIRSTNAME%

Nimm dir die Zeit. Ich verspreche dir, es lohnt sich.

Patricia 💛
```

---

### Mail 3 — PDF-Lieferung (direkt nach Bot-Abschluss)

**Betreff:** 🎁 Dein Bio-Check PDF ist fertig

**Preview-Text:** Alle Ergebnisse gesammelt, zum Download + Ausdrucken

**Body:**

```
Hey %FIRSTNAME%,

fertig! Hier ist dein persönliches Bio-Check-PDF:

👉 %BIO_CHECK_PDF_URL%

(klick oder rechte Maustaste → Link kopieren, falls du's lieber direkt herunterlädst)

Drin findest du:
• Deinen Experten-Satz in 3 Varianten
• Deine 5 Bio-Vorschläge, copy-paste-ready
• Ideen für deine 3 Pinned Posts
• Struktur für deine Highlights
• Deine nächsten Schritte

Mein Tipp:
Druck das PDF aus oder hab's offen auf dem Handy, während du deine Bio aktualisierst. Die Varianten sind fertig zum Einsetzen — aussuchen, einsetzen, fertig.

Und dann schau auf dein Profil mit anderen Augen:
Ist die Zeile 4 klar? Dein CTA? Die Kasse in deinem Laden?

Wenn ja: Go.
Wenn nein: Schreib mir — ich helf dir.

Patricia 💛

—
PS: Wenn dir was beim Umsetzen auffällt oder unklar ist, einfach hier antworten. Ich lese jede Mail selbst.
```

---

### Mail 4 — Pitch 1: Finde dein Thema (+2 Tage)

**Betreff:** Die Frage, die deine ganze Bio klärt

**Preview-Text:** Wenn dein Thema noch nicht 100% sitzt

**Body:**

```
Hey %FIRSTNAME%,

wie läuft's mit deiner neuen Bio? Ich hoffe, du hast schon eine Variante in dein Profil eingesetzt.

Wenn nicht: Vielleicht ist noch eine Frage offen, die ich immer wieder höre.

„Ich weiss gar nicht, was genau mein Thema IST."

Wenn du das gerade denkst — das ist kein Fehler. Das ist der häufigste Knoten bei Network-Mamas überhaupt. Weil wir uns so lange über unser Produkt definiert haben, dass der Schritt zum eigenen Thema sich fremd anfühlt.

Aber stell dir vor:

Du öffnest morgens Instagram und weisst sofort, worüber du heute schreibst. Weil dein Thema klar ist.

Jemand fragt dich auf dem Spielplatz: „Was machst du beruflich?" — und du antwortest in EINEM Satz, der genau die richtigen Ohren erreicht.

Du bist nicht mehr eine von 10.000 Öl-/Shake-/Putzmittel-Verkäuferinnen. Du bist DIE für [dein konkretes Thema].

Genau dafür hab ich vor ein paar Jahren meinen Minikurs gebaut: Finde dein Thema als Network-Mama — in 60 Minuten.

🎯 60 Min Video-Kurs
🎯 Die Themen-Landkarte für Networkerinnen
🎯 Die 4 Quellen deiner Expertise
🎯 Die Experten-Satz-Formel

Für 39 CHF.

👉 https://mumlifebalance.thrivecart.com/thema-finden/

Du darfst dein eigenes Thema HABEN — UND im Network bleiben. Keine Entweder-Oder-Entscheidung.

Patricia 💛
```

---

### Mail 5 — Pitch 2: Expertin statt Verkäuferin (+5 Tage)

**Betreff:** Warum Verkaufen sich oft so komisch anfühlt

**Preview-Text:** Der Unterschied zwischen Verkäuferin und Expertin

**Body:**

```
Hey %FIRSTNAME%,

kurze Frage: Fühlt es sich manchmal komisch an, wenn du auf Instagram über dein Produkt redest? So als würdest du dich aufdrängen?

Wenn ja — willkommen im Club. Ich kenn das selber.

Das kommt nicht daher, dass du falsch wärst. Das kommt daher, dass du in einer Rolle bist, die nicht zu dir passt: Verkäuferin.

Aber es gibt eine andere Rolle. Und in der fühlt sich dein Business völlig anders an:

Expertin.

Der Unterschied?

Verkäuferin pusht. Expertin wird gefragt.
Verkäuferin wiederholt Produktargumente. Expertin erzählt Geschichten.
Verkäuferin verfolgt. Expertin wird empfohlen.
Verkäuferin ist abhängig vom Partnerunternehmen. Expertin baut ihr eigenes Ding.

Stell dir vor, in 3 Monaten:

• Drei Fremde schreiben dir pro Woche: „Du hast mich endlich verstanden. Wie arbeiten wir zusammen?"
• Du postest nicht mehr aus Druck — du postest, weil du was zu sagen hast
• Deine DMs füllen sich mit echten Fragen, nicht Smalltalk
• Wenn dein Partnerunternehmen morgen die Produktpalette ändert — bleibst du ruhig. Weil DU die Marke bist, nicht das Produkt

Genau das ist mein Kurs „Expertin statt Verkäuferin". Der Weg vom Produkt-Pushen zum Empfohlen-werden.

Inklusive: Ich schaue dir am Ende persönlich über die Schulter und gebe dir Rückmeldung zu deinem Profil.

Für 97 CHF.

👉 https://mumlifebalance.thrivecart.com/expertin/

Patricia 💛
```

---

### Mail 6 — Pitch 3: Instagram-Kundenmaschine (+9 Tage)

**Betreff:** Wenn du bereit bist fürs volle System

**Preview-Text:** 8 Wochen mit mir persönlich dran

**Body:**

```
Hey %FIRSTNAME%,

du hast jetzt deine Bio. Du kennst den Unterschied zwischen Verkäuferin und Expertin. Super Basis.

Aber vielleicht denkst du gerade: „Patricia, ich weiss jetzt was, aber ich bin überfordert mit der Umsetzung. Ich brauch jemanden, der mich wirklich an die Hand nimmt."

Dafür hab ich die Instagram-Kundenmaschine.

Das ist mein 8-Wochen-Begleitprogramm — kein Selbstlernkurs, sondern Begleitung mit mir.

Stell dir vor, in 8 Wochen:

• Montags weisst du, was du die ganze Woche postest. Keine „was mach ich heute wieder"-Schleife.
• Instagram nimmt dir keine Energie mehr — es bringt dich weiter. Max 4-5 Std/Woche.
• Aus Reaktionen werden Gespräche. Aus Gesprächen Kundinnen. Ohne dass du einen einzigen Verkaufs-Skript nutzen musstest.
• Wenn du unsicher bist, schreibst du in die Telegram-Gruppe. Ich antworte. Deine Mitstreiterinnen antworten.
• Die 4 Live-Calls geben dir Klarheit genau da, wo du gerade feststeckst.
• Du hast das erste Mal das Gefühl: Mein Business läuft. Nicht perfekt. Aber es läuft.

Für 333 CHF.

👉 https://mumlifebalance.thrivecart.com/instagram-kundenmaschine/

Ehrlich: Nicht für jede ist das der richtige nächste Schritt. Wenn du gerade Bio + Basics brauchst, bleib bei „Finde dein Thema" oder „Expertin". Wenn du aber bereit bist fürs volle System mit mir persönlich dran — hier geht's rein.

Patricia 💛

—
PS: Wenn du unsicher bist ob das Programm für dich passt: Schreib mir kurz auf Instagram (@mumlifebalance_patricia_ulmann), dann finden wir's gemeinsam raus.
```

---

## ⚙️ TEIL C — Nach dem Setup noch 2 Sachen in Vercel

Sobald du die Custom-Field-ID aus AC hast (aus Teil A2), in Vercel eintragen:

1. https://vercel.com/patricia-doterra/bio-check-bot/settings/environment-variables
2. **Hinzufügen**:
   - Schlüssel: `AC_FIELD_PDF_URL`
   - Wert: die ID aus A2 (z.B. `12`)
   - Produktion + Vorschau
   - **Speichern**
3. Im Terminal: `npx vercel --prod --yes` (oder ich übernehm's)

---

## 🧪 Testlauf End-to-End

Nach dem Setup testen:

1. Auf die Landingpage (kommt in Phase 3) oder direkt das Formular öffnen
2. Mit einer **anderen E-Mail** als der Haupt-E-Mail eintragen
3. Prüfen: Kommt Mail 1 nach 1 Min?
4. Link klicken → Bot durchlaufen
5. Prüfen: Kommt Mail 3 mit PDF-Link?
6. 2 Tage warten: Kommt Mail 4?

Wenn's irgendwo hängt → AC → Automationen → auf die Automation klicken → „Kontakte in dieser Automation" → Status prüfen.

---

## 📝 Offene Punkte

- **Custom Field ID** aus AC notieren + in Vercel ENV setzen
- **Liste-ID** notieren für Formular-Zuordnung
- **Danke-Seite** auf WordPress erstellen (kommt in Phase 3)
- **Test-E-Mail** mit echter Durchlauf

---

## Was kommt danach (Phase 3)

- WordPress-Landingpage `/bio-check` mit eingebettetem Formular
- Custom Domain `bio-check.mumlifebalance.ch`
- End-to-End-Test
- Launch 🚀
