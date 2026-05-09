# Finanzen — Sensible Daten

**Was hier rein gehört:** PayPal-Transaktionsberichte, Bank-Auszüge, Kreditkarten-Abrechnungen, sonstige Finanz-Quelldaten zur Auswertung durch Claude.

**Was hier NICHT passiert:** Diese Daten werden NIE committet. `.gitignore` blockt alles ausser dieser README.

---

## Struktur

```
context/finanzen/
├── README.md              ← diese Datei (committed)
├── 2026-04/               ← pro Monat ein Ordner (gitignored)
│   ├── paypal-transaktionen.csv
│   ├── bank-auszug.csv         (oder .pdf)
│   └── kreditkarte-abrechnung.pdf  (optional)
├── 2026-05/
│   └── …
```

---

## Workflow für Patricia (manuelle Stufe — Stufe 2)

### 1. PayPal-Transaktionsbericht exportieren

1. Login → https://www.paypal.com/de/cgi-bin/webscr?cmd=_history
2. Filter: **letzter Monat** (z.B. April: 1.4. – 30.4.)
3. Export **„Aktivitäts-Bericht (CSV)"** → speichern als `paypal-transaktionen.csv`
4. Ablegen in `context/finanzen/[YYYY-MM]/`

### 2. Bank-Auszug exportieren

(Schweizer Banken — je nach Anbieter:)
- **PostFinance / Raiffeisen / UBS / ZKB:** Online-Banking → Konto → Auszug → CSV-Export → Zeitraum letzter Monat
- Speichern als `bank-auszug.csv` (oder PDF wenn CSV nicht geht)

### 3. (Optional) Kreditkarten-Abrechnung

PDF aus dem Online-Portal → speichern als `kreditkarte-abrechnung.pdf`

### 4. Patricia sagt Claude: „Werte mir Finanzen April aus"

Claude:
1. Liest alle Files in `context/finanzen/2026-04/`
2. Parst PayPal + Bank (über `scripts/finanzen/parse-*.js`)
3. Kategorisiert Transaktionen (Business-Einnahme / Business-Kosten / privat / unklar)
4. Fragt bei unklaren Posten nach
5. Erstellt:
   - `outputs/finanzen/2026-04-summary.md` — Übersicht
   - Notion-Update der Monatsplanung-Page „Erkenntnis Kennzahlen-Analyse"

---

## Stufe 3 — Automatisierung (PayPal via GitHub Action)

PayPal-Transaktionen können monatlich automatisch via GitHub Action geholt werden.

**Setup:** siehe `plans/2026-05-09-cashflow-tracker.md` Stufe 3.

**Was bleibt manuell:** Bank-Export (Schweizer Banken haben keine offene API).

---

## Sicherheit

- `.gitignore` blockt alles in `context/finanzen/**` ausser README.
- Wenn versehentlich committet → sofort `git rm --cached` + new commit + Notion informieren.
- Niemals Finanz-Files in PR oder externe Tools laden.
- Workspace-Sandbox ist nicht-persistent — bei jeder Session ggf. neu hochladen.
