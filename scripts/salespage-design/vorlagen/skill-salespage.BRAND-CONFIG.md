# BRAND-CONFIG — Skill-/Tool-Design (Patricia / Mum Life Balance)

> Diese Datei legt fest, wie die Tool-Verkaufsseiten **aussehen**.
> Wie sie **klingen**, steht in `context/` — siehe `BRAND-VOICE.md` im selben Ordner.
>
> Das dunkle der vier Designs. Für Produkte, bei denen das Werkzeug die Arbeit macht:
> Bots, Skills, Vorlagen-Pakete, alles mit Terminal- oder Software-Charakter.

---

## 1. Farben — gesetzt, nicht variabel

Dunkelblauer Grund, Petrol leuchtet.

| Rolle | Wofür | Wert |
|---|---|---|
| Grund (`--bg`) | Seiten-Hintergrund | `#0c1c30` |
| Grund 2 (`--bg2`) | zweite Sektionsfarbe, Ticker | `#12283d` |
| Karte (`--card`) | Karten, Blöcke | `#17324a` |
| Karte 2 (`--card2`) | gehobene Karten | `#1d3d58` |
| Linie (`--line`) | Ränder | `rgba(255,255,255,.09)` |
| Petrol hell (`--pink`) | Akzent, Ränder, Glow | `#2ba7b3` |
| Petrol leuchtend (`--pink-2`) | kursive Highlights auf Dunkel | `#6fd0d6` |
| Petrol (`--pink-deep`) | tiefer Akzent | `#12828c` |
| Verlauf (`--grad`) | Knopf, Ticker, Logo-Kachel | `linear-gradient(100deg,#0d626a,#12828c,#17949f)` |
| Text (`--ink`) | Fliesstext auf Dunkel | `#f1ecdd` (Creme) |
| Gedämpft (`--muted`) | Nebentext | `#9aa8b3` |

**Warum die Variablen `--pink` heissen:** Namen aus der Ursprungs-Vorlage, beibehalten
für spätere Updates. Die **Werte** sind Petrol.

**Der Knopf-Verlauf bleibt bewusst dunkel.** Ein helleres Petrol am Ende sähe schicker
aus, aber weisse Schrift darauf wäre nicht mehr sicher lesbar. Nicht aufhellen.

**Keine Abweichung:** kein Gold, kein Pink, kein Gelb, keine fünfte Farbe.

**Farb-Rhythmus:** Sektionen wechseln zwischen `--bg` und `--bg2` — nie zwei gleich
hinterlegte direkt untereinander.

## 2. Schrift

- **Philosopher** — Display-Headlines (uppercase) und kursive Highlight-Spans (`.serif`)
- **Source Sans 3** — Fliesstext
- **Space Mono** — Eyebrows, Labels, Terminal-Block, Preis-Anker

Space Mono ist hier eine **Funktion, keine Marken-Schrift**: Der Terminal-Mock im Hero
zerfällt ohne Festbreiten-Schrift. Sie kommt nur in Code-, Label- und Ticker-Elementen
vor, nie im Fliesstext. Wer sie nicht will, ersetzt sie durch Source Sans 3 und nimmt
den Terminal-Block raus — halb geht nicht.

## 3. Marke & Links

- Name / Marke: **Patricia Ulmann — Mum Life Balance**
- Website: `https://mumlifebalance.ch`
- Checkout-Link: **pro Produkt aus `context/link-uebersicht.md`** — nie raten.
- Rechtslinks im Footer (geprüft 13.09.2026, beide 200):
  - Impressum → `https://mumlifebalance.ch/impressum/`
  - Datenschutzerklärung → `https://mumlifebalance.ch/datenschutzerklaerung/`
  - AGB → ⚠️ **gibt es nicht.** `/agb/`, `/widerruf/` und `/nutzungsbedingungen/`
    liefern 404. Also **keinen AGB-Link in den Footer setzen**, der ins Leere führt.
    Falls ThriveCart beim Checkout eigene Bedingungen anzeigt, reicht das für den
    Kauf — eine eigene AGB-Seite wäre trotzdem sauberer.
- Tracking: siehe `reference_thrivecart-stripe-pixel-setup` und `scripts/meta-ads/.env`.

## 4. Bilder

In `references/assets/` ablegen. Für dieses Design trägt der Terminal-/Prompt-Mock den
Hero — ein Foto ist optional. Wenn eines rein soll: `context/content-assets/` →
`context/Shootingbilder/`. **Keine KI-Bilder.**

Ein Demo-Video wird **nicht** durch eine erfundene Vorschau ersetzt: entweder echtes
Video einbetten oder die Kachel weglassen.

---

## Was hier NICHT passiert

Keine erfundenen Zahlen, keine erfundenen Kundenstimmen. Keine Geld-zurück-Garantie —
die `.guar`-Sektion der Vorlage wird nicht gebaut. Siehe Vorrang-Block oben in `SKILL.md`.
