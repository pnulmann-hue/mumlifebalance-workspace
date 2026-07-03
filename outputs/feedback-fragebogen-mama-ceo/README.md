# Feedback-Fragebogen — Mama-CEO

**Zweck:** Strukturiertes Feedback von Mama-CEO-Absolventinnen einsammeln → Testimonials für Sales-Page + Programm-Verbesserung. Baugleich mit dem Instagram-Kundenmaschine-Formular, nur mit Mama-CEO-Fragen.

**Anreiz für Teilnahme:** 50%-Rabattcode `MAMACEO50` auf einen Minikurs (siehe Schritt 3 zur ThriveCart-Einrichtung).

> ⚠️ Nicht verwechseln: `MAMACEO50` = Feedback-Belohnung (Minikurs). `MAMACEO` (ohne 50) ist der Teilnehmerinnen-Code für die MBA in der „So geht's weiter"-Lektion. Zwei verschiedene Coupons.

---

## Was du hier hast

| Datei | Zweck |
|---|---|
| `index.html` | Der Fragebogen — 8 Fragen, ca. 5 Min Ausfüllzeit |
| `success.html` | Danke-Seite mit Rabattcode `MAMACEO50` (Kopier-Button) |
| `netlify.toml` | Netlify-Config (Build + Security-Header) |
| `README.md` | Diese Anleitung |

---

## Schritt 1 — Auf Netlify hosten (5 Minuten)

### Option A: Drag & Drop (einfachster Weg)
1. Geh auf **[app.netlify.com/drop](https://app.netlify.com/drop)** (gratis Account).
2. **Diesen ganzen Ordner** (`feedback-fragebogen-mama-ceo`) per Drag & Drop ins Drop-Feld ziehen.
3. Netlify deployt automatisch → du bekommst eine URL wie `https://schoener-name-123.netlify.app`.
4. **Site umbenennen:** Site settings → Site information → Change site name → z.B. `feedback-mama-ceo`.

### Option B: Custom Domain (später)
`feedback-mamaceo.mumlifebalance.ch` → Site settings → Domain management → CNAME beim Provider setzen.

> 💡 Wenn du schon eine Netlify-Site fürs IKM-Formular hast, mach für Mama-CEO **eine eigene neue Site** (eigener Ordner = eigenes Formular „feedback-mama-ceo").

---

## Schritt 2 — E-Mail-Benachrichtigung einrichten
1. Netlify-Dashboard → **Site settings → Forms → Form notifications**.
2. **Add notification → Email notification**.
3. Form: `feedback-mama-ceo` · Email: `pnulmann@gmail.com` → speichern.

Ab jetzt kommt jede Antwort als Mail + steht im Dashboard unter **Forms**.

---

## Schritt 3 — Rabattcode in ThriveCart anlegen
1. ThriveCart → **Coupons & Discounts** → neuen Coupon.
2. **Code:** `MAMACEO50` · **Rabatt:** 50% · **Gilt für:** deine Minikurse · **Max/Kunde:** 1 · **Gültig:** z.B. 30 Tage.
3. Speichern — **vor dem ersten Versand testen**, dass der Code funktioniert.

---

## Schritt 4 — Link an deine Absolventinnen verteilen

**Kanäle:** AC-E-Mail an alle Mama-CEO-Käuferinnen (Pilot-Mamas) · DM · in der ThriveCart-Kursplattform.

**Beispiel-Mail (Patricia-Voice):**
> Betreff: Darf ich dich was fragen? (5 Minuten + Geschenk drin 💛)
>
> Hey [VORNAME],
>
> du hast Mama-CEO durch — und ich brauche grad mal 5 Minuten von dir.
>
> Ich entwickle das Programm gerade weiter und dein ehrliches Feedback macht den Unterschied. Was hat sich verändert? Was hat geknallt? Was hat gefehlt?
>
> Hier geht's lang: [LINK]
>
> Als Dankeschön gibt's am Ende einen 50%-Rabattcode für einen meiner Minikurse — versprochen, kein Kleingedrucktes.
>
> Es sind wirklich nur 8 Fragen. Lieben Dank!
> Patricia

---

## Schritt 5 — Auswertung (mach ich für dich)
1. Netlify → **Forms → feedback-mama-ceo → Download as CSV**.
2. CSV in den Workspace legen (z.B. `outputs/feedback-fragebogen-mama-ceo/antworten/`).
3. Sag „Patricia: werte das Mama-CEO-Feedback aus" → ich liefere:
   - **Testimonial-Top-Liste** (Frage 8, nur mit Erlaubnis, Vorname + Handle)
   - **Vorher-Problem-Cluster** (Frage 1) → Marketing-Hooks
   - **Konkrete-Ergebnisse** (Frage 3) → Sales-Page-Bullets
   - **Konzept-Ranking** (Frage 4) → was kam an
   - **Verbesserungs-To-Dos** (Frage 7)
   - **NPS-Score** (Frage 6) + **Zufriedenheits-Heatmap** (Frage 5)

---

## Datenschutz / DSGVO
- Honeypot-Spamschutz eingebaut · Erlaubnis-Felder sind Opt-in (Standard = nicht angekreuzt).
- Email nur für den Rabattcode nutzen. Anonyme Antworten (ohne Name/Erlaubnis) rein intern behandeln.

## Anpassungen
- **Rabattcode tauschen:** in `success.html` an 2 Stellen (`<div class="code">` + Anleitung-Liste) `MAMACEO50` ersetzen.
- **Fragen ändern:** `index.html` editieren → Ordner neu auf Netlify ziehen.
- **Brand-Farben:** CSS-Variablen oben (`--petrol`, `--orange` …).

## Checkliste vor Go-Live
- [ ] Auf Netlify deployed (eigene Site, nicht die IKM-Site überschreiben)
- [ ] Site umbenannt
- [ ] E-Mail-Notification `feedback-mama-ceo` → pnulmann@gmail.com aktiviert
- [ ] Test-Submit gemacht → Mail kam an? Success-Seite erscheint?
- [ ] `MAMACEO50` in ThriveCart angelegt + getestet
