# Apify Konkurrenz-Scraper

Tägliches Instagram-Scraping über Apify. Liest `context/competitor-watchlist.json`, schreibt nach `outputs/apify-runs/`.

## Wie es läuft

- **Cron:** täglich 06:00 Schweiz (`.github/workflows/apify-scrape.yml`)
- **Manuell:** GitHub UI → Actions → Apify Competitor Scrape → Run workflow (optional Handles als Komma-Liste übergeben für Ad-hoc-Scrapes)
- **Lokal:** `APIFY_API_TOKEN=xxx node scrape-competitors.js`

## Kosten

Actor: `apify/instagram-profile-scraper`. Free-Tier hat 5 USD/Monat. 6 Accounts × täglich = ~1.80 USD/Monat. Hard-Cap (8 USD) wird in Plan section 7 verwaltet — wird via separates Verbrauchs-Logging implementiert sobald gemessen.

## Ergänzen

Neuen Account in `context/competitor-watchlist.json` als Eintrag hinzufügen, committen, pushen. Nächster Lauf zieht ihn mit.

## Output-Struktur

- `competitors-YYYY-MM-DD.json` — rohe Apify-Daten (alle Felder)
- `competitors-YYYY-MM-DD.md` — Patricia-lesbare Zusammenfassung mit Top 5 Posts pro Account
