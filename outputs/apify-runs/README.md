# Apify Scrape Outputs

Hier landen täglich die Konkurrenz-Daten via Apify (siehe `scripts/apify/`).

## Dateien

- `competitors-YYYY-MM-DD.json` — rohe Apify-Daten, vollständig (Folge-Skills lesen das)
- `competitors-YYYY-MM-DD.md` — Patricia-lesbare Zusammenfassung mit Top 5 Posts je Account

## Lesen für Skills

Wenn ein Skill aktuelle Konkurrenz-Daten braucht (z.B. `/freitag-hooks`, `/montag`), liest er die jüngste `competitors-*.json` aus diesem Ordner. Falls Daten älter als 36h: WebSearch-Fallback und Hinweis an Patricia.

## Aufräumen

Files älter als 90 Tage können gelöscht werden — historische Trends siehst du dann nur noch via JSON-Diff in Git-History.
