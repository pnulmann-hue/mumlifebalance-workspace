# BRAND-CONFIG — Signature-Kurs-Design (Patricia / Mum Life Balance)

> Diese Datei legt fest, wie die Signature-Kurs-Seiten **aussehen**.
> Wie sie **klingen**, steht in `context/` — siehe `BRAND-VOICE.md` im selben Ordner.
>
> Das Design ist auf Patricias Marke umgeschrieben. Die Werte unten stehen so im
> `:root`-Block von `references/reference-page.html`. Wer sie ändert, ändert die
> Marke — das ist kein Design-Spielraum, sondern eine Entscheidung.

---

## 1. Farben — gesetzt, nicht variabel

| Rolle | Wofür | Wert |
|---|---|---|
| Creme (`--cream`) | heller Grund-Hintergrund | `#f1ecdd` |
| Creme 2 (`--cream2`) | zweiter Creme-Ton (Verläufe) | `#e7e0cd` |
| Zartes Petrol (`--blush`) | helle Akzent-Sektionen | `#dfe9e8` |
| Weiss (`--white`) | weisse Sektionen | `#ffffff` |
| Text (`--ink`) | Fliesstext **und** dunkle Kontrast-Sektion (`.bg-ink`) | `#0c1c30` |
| Petrol (`--gold`) | Eyebrows, Wert-Anker, Highlights | `#12828c` |
| Petrol hell (`--gold2`) | helle Petrol-Variante (Marquee) | `#9ecdd0` |
| Orange (`--pink`) | Buttons + Akzent | `#dc822e` |
| Orange tief (`--pink-deep`) | Verlauf/Hover auf dem Button, Highlight-`<em>` | `#b4661f` |
| Orange soft (`--pink-soft`) | zarte Akzentflächen (Badges, Ringe) | `#f7e2cd` |

**Warum die Variablen `--pink` und `--gold` heissen:** Das Design kam als Vorlage in
Rosé/Gold. Die Namen sind geblieben, damit ein späteres Update der Vorlage noch passt —
die **Werte** sind Patricias Marke. Nicht von den Namen irritieren lassen.

**Keine Abweichung:** Kein Gold, kein Pink, kein Gelb, keine fünfte Farbe. Wenn zwei
Seiten unterschiedlich wirken sollen, dann über Anordnung, Grösse und Bildanteil.

**Farb-Rhythmus:** Helle Töne (Weiss, zartes Petrol, Creme) und kräftige Breaks
(`.bg-ink` dunkel, `.parallax` mit Foto) wechseln sich ab — nie zwei gleiche
Sektionsfarben direkt untereinander. Die dunklen Breaks sparsam einsetzen.

## 2. Schrift

Zwei Schriften, geladen als Google-Fonts-Link im `<head>`:

- **Philosopher** — alle Überschriften, `<em>`-Highlights (kursiv), Statement-Bänder
- **Source Sans 3** — Fliesstext, Eyebrows, Buttons, Listen

Keine dritte Schrift. Dieselbe Kombination wie in den Karussells und Stories
(`scripts/karussell-render/brand-stories.css`), damit Feed und Verkaufsseite
zusammen wirken.

## 3. Marke & Links

- Name / Marke: **Patricia Ulmann — Mum Life Balance**
- Website: `https://mumlifebalance.ch`
- Checkout-Link: **pro Produkt aus `context/link-uebersicht.md` holen** — nie raten.
  Die Signature-Kurse liegen auf ThriveCart, z.B.:
  - Instagram-Kundenmaschine (333) → `https://mumlifebalance.thrivecart.com/instagram-kundenmaschine/`
  - Digitale Produktwelt (333) → `https://mumlifebalance.thrivecart.com/digitale-produktwelt/`
  - MBA-Bundle (997 / 1347) → `https://mumlifebalance.thrivecart.com/mba/`
  - Expertin statt Verkäuferin (97) → `https://mumlifebalance.thrivecart.com/expertin/`
- Rechtslinks im Footer (geprüft 13.09.2026, beide 200):
  - Impressum → `https://mumlifebalance.ch/impressum/`
  - Datenschutzerklärung → `https://mumlifebalance.ch/datenschutzerklaerung/`
  - AGB → ⚠️ **gibt es nicht.** `/agb/`, `/widerruf/` und `/nutzungsbedingungen/`
    liefern 404. Also **keinen AGB-Link in den Footer setzen**, der ins Leere führt.
    Falls ThriveCart beim Checkout eigene Bedingungen anzeigt, reicht das für den
    Kauf — eine eigene AGB-Seite wäre trotzdem sauberer.
- Tracking: Meta-Pixel und ThriveCart-Einstellungen siehe
  `reference_thrivecart-stripe-pixel-setup` und `scripts/meta-ads/.env`.
  Die ID nicht aus dem Gedächtnis einsetzen, sondern nachschlagen.

## 4. Bilder

In `references/assets/` mit diesen Namen ablegen, dann stimmen die Pfade der Vorlage:

- `dein-portrait.jpg` — Patricia (Hero-Hintergrund, „Über mich", Preisblock)
- `dein-hero.jpg` — Stimmungsfoto für die Parallax-Bänder
- `dein-mockup-transparent.png` — Produkt freigestellt (Hero)
- `dein-mockup.png` — Produkt mit Hintergrund (Showcase)
- `dein-beweis-1.png`, `dein-beweis-2.png`, … — **echte** Screenshots

**Foto-Quelle in dieser Reihenfolge:** aktuelles Foto aus
`context/content-assets/` → `context/Shootingbilder/` (1'007 echte Bilder) →
Stock nur für reine Atmosphäre. Keine KI-Bilder.

**Sicht-Prüfung vor der Abgabe:** Ist Patricias Gesicht frei? Verdeckt kein
Text-Kasten das Hauptmotiv? (CLAUDE.md, Visual-QA-Pflicht.)

---

## Was hier NICHT passiert

Die Ursprungs-Vorlage füllte fehlende Zahlen und Kundenstimmen mit „plausiblen
Beispielen" und markierte sie als Platzhalter. **Das gilt hier nicht.** Fehlt eine
Zahl, wird der Satz ohne Zahl formuliert; fehlt eine Stimme, bleibt die Sektion leer
oder draussen. Siehe den Vorrang-Block oben in `SKILL.md`.

Ebenso: **keine Geld-zurück-Garantie.** Die Garantie-Sektion wird nicht gebaut.
