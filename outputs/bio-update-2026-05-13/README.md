# Bio-Update 2026-05-13 — Themen-Achse statt Stadium-Achse

**Auslöser:** Patricia entscheidet, dass die Aussen-Kommunikation auf das Themen-Modell umgestellt wird, weil die Zielgruppe es besser versteht. Die Stadium-Achse (Networkmarketing 2.0 / Hybrid / Mama Business) bleibt intern für die Funnel-Logik.

## Was in diesem Ordner liegt

| Datei | Zweck | Wer macht was |
|---|---|---|
| `instagram-bio.md` | Neuer Bio-Text + Begründung + Test-Hypothese | Patricia: in @patricianulmann-Bio einfügen (Profil bearbeiten → Steckbrief) |
| `wp-ueber-mich-draft.html` | Neue Über-mich-Seite für mumlifebalance.ch | Patricia: in WP-Admin neue Seite anlegen ODER bestehende `/ueber-mich` ersetzen, **als Draft speichern**, vor Publish prüfen |
| `README.md` | Diese Datei | — |

## Sandbox-Limits (kein Live-Push möglich)

- `mumlifebalance.ch` ist von dieser Web-Claude-Sandbox geblockt (`403 host_not_allowed`)
- `scripts/wordpress/.env` existiert nicht (gitignored, persistiert nicht zwischen Sessions)

→ **Alle 3 Updates müssen von Patricia manuell angewandt werden.** Falls regelmässige WP-Updates gewünscht sind, dafür eine GitHub Action mit `WP_APP_PASSWORD` als Secret aufsetzen (Pattern siehe `.github/workflows/apify-scrape.yml`).

## Reihenfolge

1. **Instagram-Bio** zuerst — kleinster Aufwand, sofortiger Test
2. **Über-mich-Seite** als Draft anlegen, gegenlesen, dann publish
3. **`context/saeulen-mentoring.md`** wurde bereits ergänzt (Themen-Achse parallel zur Stadium-Achse) — ab jetzt schreiben `/freitag-hooks`, `/montag`, `/karussell`, `/reels` automatisch mit dem neuen Themen-Mapping

## Folge-Tasks (nicht in diesem Update)

- [ ] Instagram-Highlights-Cover für die 3 Themen designen (Insta-Verkaufen / Onlinekurse / KI für Mamas)
- [ ] Linktree neu sortieren — pro Themen-Säule mind. 1 sichtbares Angebot
- [ ] „Verkaufs"-Beitrag im Feed pinnen (Bio-Check oder Workbook)
- [ ] Re-Check Performance: 2026-05-27 (Profil-Klicks, DMs, neue Follower-Demografie)
