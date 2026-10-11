# BRAND-CONFIG — KI-Design (Patricia / Mum Life Balance)

> Diese Datei legt fest, wie die KI-Produkt-Seiten **aussehen**.
> Wie sie **klingen**, steht in `context/` — siehe `BRAND-VOICE.md` im selben Ordner.
>
> Das lauteste der vier Designs: dunkelblauer Grund, Orange leuchtet. Für Bots,
> KI-Assistentinnen und alles, was mit KI im Mama-Alltag zu tun hat.

---

## 1. Farben — gesetzt, nicht variabel

| Rolle | Wofür | Wert |
|---|---|---|
| Grund (`--bg`) | Seiten-Hintergrund | `#0c1c30` |
| Grund 2 (`--bg2`) | zweite Sektionsfarbe | `#122a42` |
| Karte (`--card`) | Karten, Tool-Kacheln | `#16324c` |
| Linie (`--line`) | Ränder, Glows | `rgba(220,130,46,0.20)` |
| Orange (`--neon` / `--gold`) | Leuchtfarbe, Eyebrows, Zahlen | `#dc822e` |
| Petrol (`--violet`) | zweite Akzentfarbe | `#12828c` |
| Petrol hell (`--cyan`) | dritte Akzentfarbe, Kicker | `#4fc9d1` |
| Highlight-Verlauf (`--goldgrad`) | Überschriften-Spans (`.gold`, `<em>`) | `linear-gradient(90deg,#dc822e,#f0a45e,#f7c08f)` |
| Knopf-Verlauf (`--cta`) | Knöpfe | `linear-gradient(100deg,#b4661f,#dc822e,#f0a45e)` |
| Text (`--ink`) | Fliesstext auf Dunkel | `#f1ecdd` (Creme) |
| Gedämpft (`--muted`) | Nebentext | `#9aa8b3` |

**Warum die Variablen `--neon`, `--violet`, `--cyan`, `--goldgrad` heissen:** Namen aus
der Ursprungs-Vorlage (dort eine Pink/Violett/Cyan-Triade), beibehalten für spätere
Updates. Die **Werte** sind Orange und Petrol.

**Zwei Entscheidungen, die nicht zurückgedreht werden sollten:**

1. **Der Überschriften-Verlauf bleibt warm** (Orange → hell), läuft also nicht ins
   Petrol aus. Sonst verschwindet das letzte Wort der Überschrift im dunklen Grund.
2. **Die Knopfschrift ist dunkel** (`#0c1c30`), nicht weiss. Weiss auf Orange trägt
   nur 2,9:1 Kontrast, dunkel auf Orange rund 6:1 — und dunkel auf Orange ist ohnehin
   die Optik aus den Karussells.

**Keine Abweichung:** kein Gold, kein Pink, kein Gelb, keine fünfte Farbe.

**Farb-Rhythmus:** Sektionen wechseln zwischen `--bg` und `--bg2` — nie zwei gleich
hinterlegte direkt untereinander.

## 2. Schrift

- **Philosopher** — grosse Uppercase-Display-Headlines
- **Source Sans 3** — Fliesstext; gesperrt (`letter-spacing`) für Eyebrows,
  Tool-Nummern und Tech-Labels

Keine dritte Schrift.

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

In `references/assets/` ablegen. Das Design sieht eine KI-Figur oder ein Produkt-Visual
im Hero vor (`.figwrap`).

⚠️ **Hier ist die KI-Figur die Falle:** Patricias Marke lebt von echten Fotos, nicht von
generierten Bildern. Für ein KI-Produkt also **kein gerendertes Roboter-Gesicht**,
sondern Patricia selbst am Rechner, ein Screenshot des Bots oder eine schlichte
Produkt-Kachel. Foto-Quelle: `context/content-assets/` → `context/Shootingbilder/`.

Das „Trainiert-auf"-Zahlenband (`.stats`) **nur mit echten Zahlen füllen** — wie viele
Kurse, wie viele Vorlagen, wie lange im Einsatz. Fehlt eine Zahl, fällt die Kachel weg.

---

## Was hier NICHT passiert

Keine erfundenen Zahlen, keine erfundenen Kundenstimmen. Keine Geld-zurück-Garantie.
Siehe Vorrang-Block oben in `SKILL.md`.
