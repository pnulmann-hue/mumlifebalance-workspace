---
tags: [produkt]
---

# outputs/produkte/ — Produkterstellungs-Outputs

Alle Deliverables aus dem `/produkt`-Command landen hier — ein Ordner pro Produkt.

## Konvention

```
outputs/produkte/[kebab-slug-des-produkts]/
├── 00-briefing.md              # Kurz-Zusammenfassung: Name, Zielgruppe, Transformation, Preis, Launch-Datum
├── 01-produkttreppe.md         # Modus 1: strategische 4-Stufen-Landkarte
├── 02-validierung.md           # Modus 2: Warmlist-Check, Pre-Sale, DM-Texte
├── 03-canva-briefing/          # Modus 3b: Folien-Texte + Sprechnotizen pro Modul
│   ├── modul-01.md
│   └── ...
├── 04-arbeitsblätter/          # Modus 3c: .docx für Google Drive
├── 05-ki-assistent/            # Modus 9: GPT-Konzept (Basis + Framework + System-Prompt)
├── 06-preis-validierung.md     # Modus 4: 3-Stufen-Staffel + Messaging
├── 07-launch-kalender.md       # Modus 5: 7-Tage-Rhythmus über 2–4 Wochen
├── 08-funnel/                  # Modus 6: Checkout + Bumps + Upsell/Downsell + 5-Mail-Sequenz
├── 09-salespage.md             # Modus 7: ThriveCart-Blöcke (+ Spiegel in outputs/salespages/)
└── 10-angebotsseite.md         # Modus 8: Homepage-Angebotsseite
```

## Slug-Beispiele

- `mompreneur-minikurs`
- `content-die-verkauft`
- `vom-network-zum-eigenen-produkt-signature`

## Verwendung

1. Session starten → `/prime`
2. `/produkt` aufrufen
3. Business wählen (Onlinebusiness / Network)
4. Modus wählen
5. Outputs landen automatisch hier
