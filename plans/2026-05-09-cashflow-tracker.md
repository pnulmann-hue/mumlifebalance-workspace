# Plan: Cashflow-Tracker (PayPal + Bank → Monatsplan-Notion)

**Erstellt:** 2026-05-09
**Anlass:** /monatsplan-Lauf Mai 2026 — Patricia hatte April-Kosten nicht erfasst, will Cashflow ordentlicher ablegen
**Status:** Stufe 1+2 fertig (committed), Stufe 3 wartet auf Patricia (PayPal-Token + Workflow-Aktivierung)

---

## Ziel

Patricia kann monatlich (oder beim naechsten /monatsplan) auf einen klaren Cashflow-Snapshot zugreifen:
- Was ist reingekommen (PayPal + Bank)
- Was sind Business-Ausgaben (Tools/Services)
- Wie ist der Netto-Cashflow
- Notion-Block den sie/Claude in die Monatsplan-Page setzen kann

Ohne dass sensible Finanzdaten je in Git landen.

---

## Stufe 1 — April-Snapshot (heute, ✓ erledigt)

- Notion-Mai-Page → Property „Erkenntnis Kennzahlen-Analyse" mit dem was wir wissen gefuellt:
  - Umsatz April: CHF 184.28 (CHF 97 Mentoring-Mini + CHF 87.28 doTERRA-Sekundaerbonus)
  - Primaerbonus April ausstehend (Forderung)
  - Kosten + Gewinn: nicht erfasst — Track-Luecke
- `Finanz check-up` Property bleibt NO bis Bank-Cashflow-Check erfolgt

---

## Stufe 2 — Manueller Workflow (heute, ✓ erledigt)

### Was ich gebaut habe

```
context/finanzen/
├── README.md                    # Patricia-Anleitung wie sie Files exportiert + ablegt
├── .gitkeep
└── [YYYY-MM]/                   # gitignored — Patricia legt hier ab
    ├── paypal-transaktionen.csv
    └── bank-auszug.csv

scripts/finanzen/
├── README.md
├── package.json
├── parse-paypal.js              # CSV-Parser (DE/EN-Header)
├── parse-bank.js                # CH-Banken: PostFinance/Raiffeisen/UBS/ZKB/Migros
├── summary.js                   # kombiniert PayPal + Bank → Notion-Block
└── fetch-paypal-api.js          # Stufe-3-Code (siehe unten)
```

### Was Patricia/Claude tut (manueller Lauf)

```bash
# Patricia legt Files ab in context/finanzen/2026-04/
# Dann:
cd scripts/finanzen
npm install                            # einmalig
node parse-paypal.js 2026-04
node parse-bank.js 2026-04
node summary.js 2026-04
# Output: outputs/finanzen/2026-04/cashflow-summary.md
```

### Sicherheit

- `.gitignore`-Update: `context/finanzen/**` blockt alles ausser README
- PayPal/Bank-CSVs landen NIE in Git
- Bilanz-MD in `outputs/finanzen/` ist anonymisiert (keine IBANs etc.)

---

## Stufe 3 — Automatisierung PayPal (gebaut, wartet auf Patricia-Aktivierung)

### Was ich gebaut habe

- `scripts/finanzen/fetch-paypal-api.js` — holt Vormonats-Transaktionen via PayPal Reporting API v1, schreibt CSV im gleichen Format wie der manuelle Export
- `.github/workflows/paypal-monthly.yml` — laeuft am 1. jeden Monats 06:00 Schweiz, holt automatisch Vormonat
  - Raw-CSV: GitHub-Actions-Artifact (90 Tage retention, NICHT committed)
  - Bilanz-MD: committed in `outputs/finanzen/[YYYY-MM]/`

### Was Patricia tun muss (Aktivierung)

#### 1. PayPal-Developer-App erstellen

1. Login → https://developer.paypal.com/dashboard/applications/live
2. Apps & Credentials → „Create App" → Name z.B. „MumLifeBalance Cashflow"
3. App-Type: **Live** (nicht Sandbox — wir wollen echte Transaktionen)
4. Permissions: **Transaction Search** (Reporting API) muss aktiviert sein
   → Falls nicht in der Default-Liste: PayPal-Account-Limits pruefen, evtl. „Account Information" aktivieren oder PayPal-Support kontaktieren
5. Notiere `Client ID` und `Secret`

#### 2. GitHub Repo Secrets eintragen

GitHub Repo (pnulmann-hue/mumlifebalance-workspace) → Settings → Secrets and variables → Actions → New repository secret:
- `PAYPAL_CLIENT_ID` = (aus Schritt 1)
- `PAYPAL_CLIENT_SECRET` = (aus Schritt 1)

#### 3. Workflow testen

GitHub → Actions → „PayPal Monthly Cashflow" → Run workflow → optional: month=2026-04 fuer Backfill April

→ Erwarteter Output:
- Workflow gruen ✓
- Artifact `paypal-raw-2026-04` zum Download verfuegbar
- Commit auf claude/instagram-creator-analysis-RbNNt mit `outputs/finanzen/2026-04/paypal-summary.md` und `cashflow-summary.md`

#### 4. Wenn Workflow rot:

- Logs lesen — typischer Fehler: Reporting-API nicht aktiviert
- Falls so: PayPal-Support kontaktieren oder API-Permission im Dashboard pruefen
- Fallback: weiter manuell (Stufe 2) bis API-Permission da

---

## Stufe 4 — Bank-Automatisierung (NICHT gebaut — kein Open-Banking in CH)

### Warum nicht

Schweizer Banken haben (ausser Hypothekarbank Lenzburg, Yapeal und ein paar Fintechs) keine offene API. Patricia muesste:
- Open-Banking-fähige Bank wechseln (zu aufwendig)
- ODER Banken-Aggregator nutzen (Bexio, Klara, Banana — kostenpflichtig)
- ODER manuell bleiben (heute der pragmatische Weg)

**Empfehlung:** Manueller Bank-CSV-Export bleibt — dauert 2 Min/Monat. Patricia macht das Anfang Monat zusammen mit dem PayPal-Action-Run.

---

## Stufe 5 — Auto-Notion-Update (geplant, nicht gebaut)

Ziel: Bilanz wird nach Cashflow-Run automatisch in die Monatsplan-Notion-Page geschrieben (Property „Erkenntnis Kennzahlen-Analyse").

### Setup

- Notion-Token als Repo-Secret `NOTION_TOKEN` (existiert bereits fuer freitag-hooks)
- Erweiterung in `summary.js`: nach Erstellen der MD ruft es Notion API auf, sucht die Monatsplan-Page (`Monat + Jahr` matcht YYYY-MM), updated Property
- Workflow `paypal-monthly.yml` zusatzlich: nach `node summary.js` einen Schritt `node notion-update.js`

### Wann bauen

Erst wenn Stufe 3 stabil laeuft (mind. 1 erfolgreicher Monatsdurchlauf). Dann hierauf aufbauen, nicht parallel.

---

## Akzeptanz-Kriterien

| # | Kriterium | Status |
|---|---|---|
| 1 | `context/finanzen/` ist gitignored, `.gitignore` erlaubt nur README | ✓ |
| 2 | `parse-paypal.js` parst DE/EN-CSV-Format | ✓ |
| 3 | `parse-bank.js` erkennt PostFinance/Raiffeisen/UBS/ZKB/Migros automatisch | ✓ |
| 4 | `summary.js` produziert Notion-Block fuer Monatsplan | ✓ |
| 5 | GitHub-Action `paypal-monthly.yml` laeuft monatlich am 1. | ✓ (deployed, wartet auf Secrets) |
| 6 | Patricia hat PayPal-Token als Secret hinterlegt | ⏳ Patricia |
| 7 | Erster erfolgreicher Workflow-Run mit echten Daten | ⏳ Patricia |
| 8 | April-Bilanz aus echten Daten in Notion-Mai-Page | ⏳ nach Stufe-2-Lauf oder Stufe-3-Backfill |

---

## Naechste Schritte (Patricia)

1. **Diese Woche:** PayPal-Developer-App erstellen + Secrets in GitHub setzen + Test-Workflow-Run fuer April
2. **Wenn Workflow gruen:** April-Bank-CSV exportieren + in `context/finanzen/2026-04/` ablegen + manuellen Lauf
3. **Anfang Juni:** automatischer Mai-Run sollte am 1.6. um 06:00 laufen — Patricia checkt Output
4. **Bei naechstem /monatsplan-Lauf (Ende Mai fuer Juni):** Bilanz Mai ist automatisch in Notion ✓
