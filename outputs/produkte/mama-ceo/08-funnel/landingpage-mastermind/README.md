---
tags: [produkt]
---

# Mama-CEO KI-Mastermind — Landingpage (Netlify-Ready)

**Webinar-Titel:** „In 90 Min: Dein Mama-Leben mit KI-Assistenten umkrempeln"
**Datum:** Mi 20. Mai 2026, 09:00 Uhr
**Ziel:** mind. 100 Anmeldungen bis Mi 20.5.

---

## Was hier drin ist

```
landingpage-mastermind/
├── index.html      ← die komplette Page (Single File, Inline-CSS)
└── README.md       ← diese Datei
```

Eine einzige `index.html` mit allem drin. Kein Build-Tool, keine Dependencies.

---

## Schritt 1 — Lokal anschauen (vor dem Deploy)

```bash
cd outputs/produkte/mama-ceo/08-funnel/landingpage-mastermind
open index.html
```

Oder doppelklicke `index.html` im Finder. Funktioniert in jedem Browser.

**Was du siehst:**
- Vollständige Page mit Brand-Style (Creme + Philosopher + Source Sans 3)
- 2 Foto-Platzhalter (Hero + About) — die musst du noch ersetzen
- 1 AC-Form-Platzhalter — den musst du mit ActiveCampaign-Embed füllen

---

## Schritt 2 — ActiveCampaign-Formular anlegen

1. Login bei **mumlifebalance.activehosted.com**
2. Menü: **Site → Forms → Create**
3. **Inline-Form** wählen (NICHT Modal/Floating Bar)
4. Felder hinzufügen:
   - **Vorname** (Pflicht, Type: Text)
   - **E-Mail** (Pflicht, Type: Email)
   - Optional: **Dein grösster Mental-Load-Punkt?** (Type: Textarea, optional)
5. **Actions** (unten):
   - Add Tag: `mama-ceo-mastermind-anmeldung`
   - Subscribe to List: deine Hauptliste (ID 2 vermutlich)
6. **Style** (rechts oben): einfach lassen — wir stylen via Page-CSS
7. **Save & Publish**
8. **Embed-Code kopieren** → HTML-Variante (nicht JavaScript-Variante)
9. **Form-ID merken** (steht im Embed-Code wie `_form_XX`)

---

## Schritt 3 — AC-Form in `index.html` einbauen

Öffne `index.html` und suche diesen Block (Sektion „Anmeldung"):

```html
<div class="ac-form-slot">
  <strong>📌 AC-Formular hier einfügen</strong>
  ...
</div>
```

**Ersetze den ganzen Block** mit dem AC-Embed-Code, den du gerade kopiert hast.

**Wenn deine Form-ID nicht `_form_47` ist:**
Suche im `<style>`-Block (oben in `index.html`) alle Stellen mit `._form_47` und ersetze mit deiner ID. Das stylt das Form passend zur Brand.

---

## Schritt 4 — Fotos einbauen

### Hero-Foto (oben rechts)

Suche in `index.html`:
```html
<div class="hero-photo">
  [Patricia-Foto Hero...]
</div>
```

Ersetze mit:
```html
<div class="hero-photo" style="background-image: url('hero.jpg'); background-size: cover; background-position: center;"></div>
```

Lege `hero.jpg` direkt in den Ordner `landingpage-mastermind/`.
**Empfehlung:** Foto im Format 4:5 (z.B. 800×1000px), warm-lächelnd, Setup-Vibe.

### About-Foto (Sektion „Wer das hier hält")

Gleiches Pattern, suche `<div class="about-photo">` und ersetze mit:
```html
<div class="about-photo" style="background-image: url('patricia.jpg'); background-size: cover; background-position: center;"></div>
```

`patricia.jpg` im selben Ordner. **Format quadratisch** (z.B. 600×600px), persönlich.

### Fotos aus deinem Workspace

Du hast 100+ Fotos in `context/Shootingbilder/`. Wähle:
- **Hero:** authentisch, am Laptop oder mit Kaffee, lächelnd
- **About:** persönlicher (z.B. mit Kindern oder draussen)

Kopiere die zwei Fotos in den `landingpage-mastermind/`-Ordner und benenne sie `hero.jpg` und `patricia.jpg`.

---

## Schritt 5 — Auf Netlify deployen

### Variante A: Drag & Drop (schnellste Methode)

1. Geh auf **app.netlify.com**
2. Login (oder Account erstellen)
3. Auf der Hauptseite: **„Add new site" → „Deploy manually"**
4. **Drag & Drop** den ganzen Ordner `landingpage-mastermind/` in das gestrichelte Rechteck
5. Netlify gibt dir sofort eine URL (z.B. `https://merry-cookie-12345.netlify.app`)
6. **Custom Domain einrichten:** Site Settings → Domain Management → „Add custom domain" → `ki-mastermind.mumlifebalance.ch` (Subdomain bei deinem DNS-Provider als CNAME auf Netlify-URL setzen)

### Variante B: Git-verbunden (für spätere Updates einfacher)

1. Pushe diesen Ordner auf GitHub
2. Netlify → „Add new site" → „Import an existing project"
3. GitHub-Repo verbinden
4. Build Command: leer lassen
5. Publish Directory: `outputs/produkte/mama-ceo/08-funnel/landingpage-mastermind`
6. Deploy

---

## Schritt 6 — Vor Live-Schalten testen

**Checkliste:**
- [ ] AC-Form funktioniert: Test-Anmeldung machen, prüfen ob Tag `mama-ceo-mastermind-anmeldung` gesetzt wird
- [ ] Bestätigungs-Mail kommt an (in AC-Automation eingerichtet?)
- [ ] Mobile-Layout sieht gut aus (am Handy öffnen)
- [ ] Alle Links funktionieren (Instagram, Footer)
- [ ] Hero-Foto + About-Foto laden schnell
- [ ] Datum + Zeit korrekt: **Mi 20. Mai 2026, 09:00 Uhr**

---

## ManyChat-Integration (parallel)

In ManyChat ein Keyword `MASTERMIND` aktivieren:

**Trigger:** User schreibt „MASTERMIND" in DM
**Bot-Antwort:**
1. „Hi! Schön, dass du dabei bist. Ich schick dir gleich die Details zum 90-Min-Mastermind am Mi 20.5. 09:00 — kostenlos."
2. Frage: „Was beschäftigt dich gerade am meisten als Mama-Unternehmerin?" (sammelt Vorab-Fragen für Q&A)
3. **Action:** Tag in AC: `mama-ceo-mastermind-anmeldung` (gleicher Tag wie Form-Anmeldung)
4. Bestätigungs-Mail mit Zoom-Link wird dann via AC-Automation automatisch versendet

---

## Was kommt noch (für nächste Session)

- AC-Automation: Bestätigungs-Mail + 4 Touchpoints (24h vor / 2h vor / direkt nach Mastermind)
- Pitch-Slides Mastermind (18-22 Slides Canva)
- Zoom-Webinar-Link erstellen + an Anmelder versenden
- Reels (Brandastic-Story · Live-Demo · Falsch-vs-Richtig)
- Karussell „Schuld-Spirale 8 Folien"
- Aufwärmphase-Mails #1-3

→ Siehe `_NAECHSTE-SCHRITTE.md` und `07-launch-kalender.md`.

---

## Brand-Farben (für Konsistenz)

```css
--creme: #f1ecdd        /* Hauptbackground */
--creme-soft: #e8dfc7   /* Sekundär-Background, Highlights */
--ink: #2c2c2c          /* Haupttext */
--terracotta: #9a4a2e   /* CTA-Buttons, Akzente */
--gold: #b89456         /* Bonus-Box Akzent */
```

**Schriften:**
- Headlines: Philosopher (Google Fonts)
- Body: Source Sans 3 (Google Fonts)
- Beide werden automatisch geladen — kein Setup nötig.

---

**Fragen?** Sag „Page-Anpassung" und beschreib was du ändern willst — dann mach ich's.
