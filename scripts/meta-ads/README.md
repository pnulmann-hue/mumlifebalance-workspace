# Meta Ads API — Setup für Mum Life Balance

Ermöglicht zwei Sachen:
1. **Eigene Meta Ads automatisch managen** (Marketing API)
2. **Wettbewerbs-Ads durchsuchen** (Ad Library API)

## Was der Bot damit kann

- `whoami` — prüft Token-Gültigkeit
- `list-campaigns` — alle Kampagnen + Status + Budget
- `insights <campaign-id> <days>` — Performance (Impressions, CTR, CPL, ROAS)
- `pause-campaign <id>` / `activate-campaign <id>` — Kampagnen steuern
- `set-budget <id> <chf>` — Tagesbudget ändern
- `competitors <keyword> [country]` — Meta Ad Library durchsuchen (z.B. "Julia Trost", "Network Mama")
- `page-ads <page-id>` — alle aktuellen Ads einer spezifischen Mitbewerber-Page
- `analyze [days]` — **Auto-Analyse + Empfehlungen** (Winner/Loser + Vorschläge für Boost/Pause)

## Setup (einmalig, ~30 Min)

### 1. Meta Business Manager + App

1. https://business.facebook.com öffnen → dein Business-Account auswählen
2. **Business-Einstellungen** (Zahnrad oben rechts) → **Systembenutzer** → **Hinzufügen**
   - Name: `Claude Ads Bot`
   - Rolle: **Administrator**
3. Beim neuen System-Benutzer: **Assets zuweisen** → **Werbekonten** → dein Ad Account → Vollzugriff
4. **Token erstellen:**
   - Beim System-Benutzer: **Token erstellen**
   - App auswählen (falls keine: Meta Developer Portal → neue App anlegen, Typ „Business")
   - Permissions anhaken:
     - `ads_read` (lesen)
     - `ads_management` (schreiben/pausieren/Budget)
     - `business_management`
     - `pages_read_engagement` (für Page-Ads)
   - **„Zugriffstoken generieren"** → KOPIEREN (wird nur 1x gezeigt!)

### 2. Ad Account ID finden

- Meta Ads Manager öffnen → die Account-ID steht in der URL: `https://adsmanager.facebook.com/adsmanager/?act=1234567890`
- Format in `.env`: `act_1234567890` (mit `act_` Prefix!)

### 3. Eintragen in `.env`

```bash
# scripts/meta-ads/.env
META_ACCESS_TOKEN=EAAxxxxxxxxxxxxxxxxx  # der System-User-Token
META_AD_ACCOUNT_ID=act_1234567890
META_CURRENCY=CHF
```

### 4. Testen

```bash
cd scripts/meta-ads
node --env-file=.env meta-api.js whoami
# → "Meta-User: System-Benutzer Name"

node --env-file=.env meta-api.js list-campaigns
# → Liste deiner Kampagnen

node --env-file=.env meta-api.js analyze 7
# → Performance-Report letzte 7 Tage + Empfehlungen
```

## Sicherheit

**Der System-User-Token gibt Vollzugriff auf dein Werbekonto** — also auch Geld ausgeben.

- Token niemals in Git committen (`.env` ist gitignored)
- Token nie in Chat/E-Mail teilen
- Token kann im Business Manager → System-Benutzer → „Tokens zurückziehen" sofort widerrufen werden
- Empfehlung: Budget-Limit pro Kampagne setzen, damit der Bot nicht „durchgeht"

## Token-Lebensdauer

System-User-Tokens sind **permanent** (laufen nicht ab). Einmal einrichten, dauerhaft nutzen.

## Wettbewerbsanalyse via Ad Library (kein Login nötig)

Für die Ad Library reicht der Token auch — der Endpoint `/ads_archive` ist öffentlich zugänglich.

```bash
# Was schalten andere Mentorinnen gerade?
node --env-file=.env meta-api.js competitors "Network Marketing Mama" DE
node --env-file=.env meta-api.js competitors "Instagram Business" CH
node --env-file=.env meta-api.js competitors "Expertin Positionierung" DE

# Direkt eine Wettbewerber-Page abgrasen
node --env-file=.env meta-api.js page-ads 123456789  # (Page-ID)
```

## Integration in `/funnel` Mode 3

Wenn Credentials gesetzt sind, nutzt der `/funnel` Skill automatisch:
1. **Beim Painpoint-Check (Schritt 0):** `competitors` + `page-ads` um zu sehen was die Konkurrenz gerade testet
2. **Beim Signal-Check (Schritt 1):** `analyze` der eigenen Ads → Winner/Loser identifizieren
3. **Beim Launch:** Nach 3-5 Tagen automatisch `analyze` laufen lassen → Empfehlungen

## Troubleshooting

- **„(#100) Missing permissions":** Token hat nicht alle Permissions → neu generieren mit korrekten Scopes
- **„(#2) Service temporarily unavailable":** Meta-API ist manchmal flakey, einfach nochmal versuchen
- **„Invalid OAuth 2.0 Access Token":** Token abgelaufen/widerrufen → neu generieren
- **„(#200) The user hasn't authorized the application":** Ad Account ist nicht dem System-User zugewiesen → Business-Einstellungen prüfen
