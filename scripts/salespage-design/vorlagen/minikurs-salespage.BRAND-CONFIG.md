# BRAND-CONFIG — Minikurs-Design (Patricia / Mum Life Balance)

> Diese Datei legt fest, wie die Minikurs-Seiten **aussehen**.
> Wie sie **klingen**, steht in `context/` — siehe `BRAND-VOICE.md` im selben Ordner.
>
> Das Design ist auf Patricias Marke umgeschrieben. Die Werte unten stehen so im
> `:root`-Block von `references/reference-page.html`.

---

## 1. Farben — gesetzt, nicht variabel

Das hellste und freundlichste der vier Designs: Petrol trägt die Fläche, Orange den Knopf.

| Rolle | Wofür | Wert |
|---|---|---|
| Petrol (`--black`) | kräftige Hauptfarbe, Voll-Sektionen (`.sec-dark`) | `#12828c` |
| Weiss (`--cream` / `--white`) | helle Sektionen, Karten | `#ffffff` |
| Orange (`--gold`) | Knöpfe, Badges, Akzent | `#dc822e` |
| Orange hell (`--gold-2`) | helle Akzentvariante | `#f2c08a` |
| Text (`--ink`) | Text auf hell | `#0c1c30` |
| Gedämpft (`--muted`) | Nebentext | `#5c6b75` |
| Petrol zart (`--muted-light`) | zarte Flächen, Trenner | `#c9e2e3` |
| Creme | Creme-Sektionen (`.sec-cream`) | `#f1ecdd` |

**Warum die Variablen `--black` und `--gold` heissen:** Namen aus der Ursprungs-Vorlage,
beibehalten für spätere Updates. Die **Werte** sind Patricias Marke.

**Keine Abweichung:** kein Gold, kein Pink, kein Gelb, keine fünfte Farbe.

**Farb-Rhythmus:** Die Sektionen wechseln zwischen `.sec-dark` (Petrol),
`.sec-berry` (Petrol-Variante) und `.sec-cream` (hell) — nie zwei gleiche direkt
untereinander. Der Footer ist Petrol, also darf die letzte Content-Sektion davor
keine Petrol-Fläche sein.

## 2. Schrift

- **Philosopher** — alle Überschriften (`h1`, `h2`, `h3`, `.disp`)
- **Source Sans 3** — Fliesstext, Labels, Buttons

Keine dritte Schrift. Gleiche Kombination wie Karussells und Stories.

## 3. Marke & Links

- Name / Marke: **Patricia Ulmann — Mum Life Balance**
- Website: `https://mumlifebalance.ch`
- Checkout-Link: **pro Produkt aus `context/link-uebersicht.md`** — nie raten.
  Minikurse liegen bei 19–39 CHF, z.B.:
  - Storyideen für Networkerinnen (19, mit Content-Box-Bump 17) → `https://mumlifebalance.thrivecart.com/storyideen/`
  - Finde dein Thema als Network-Mama (39) → `https://mumlifebalance.thrivecart.com/thema-finden/`
  - Vom Network-Wissen zum eigenen Produkt (39) → `https://mumlifebalance.thrivecart.com/eigene-produkterstellung/`
- **Preis-Regel:** Alle Minikurse kosten **39 CHF fix, ohne Early-Bird und ohne Rabatt.**
  Der „Warum jetzt"-Grund kommt über einen monatlich wechselnden Bonus, nicht über den Preis.
  (Ausnahme: Storyideen als 19-CHF-Einstieg.)
- Rechtslinks im Footer (geprüft 13.09.2026, beide 200):
  - Impressum → `https://mumlifebalance.ch/impressum/`
  - Datenschutzerklärung → `https://mumlifebalance.ch/datenschutzerklaerung/`
  - AGB → ⚠️ **gibt es nicht.** `/agb/`, `/widerruf/` und `/nutzungsbedingungen/`
    liefern 404. Also **keinen AGB-Link in den Footer setzen**, der ins Leere führt.
    Falls ThriveCart beim Checkout eigene Bedingungen anzeigt, reicht das für den
    Kauf — eine eigene AGB-Seite wäre trotzdem sauberer.
- Tracking: siehe `reference_thrivecart-stripe-pixel-setup` und `scripts/meta-ads/.env`.

## 4. Bilder

In `references/assets/` ablegen (Namen siehe Vorlage). Foto-Quelle in dieser Reihenfolge:
aktuelles Foto aus `context/content-assets/` → `context/Shootingbilder/` → Stock nur
für Atmosphäre. **Keine KI-Bilder.**

Sicht-Prüfung vor der Abgabe: Gesicht frei? Hauptmotiv unverdeckt? (CLAUDE.md)

---

## Was hier NICHT passiert

Keine erfundenen Zahlen, keine erfundenen Kundenstimmen — auch nicht als markierte
Platzhalter. Keine Geld-zurück-Garantie. Siehe Vorrang-Block oben in `SKILL.md`.
