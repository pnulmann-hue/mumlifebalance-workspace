# Plan: Apify GitHub-Actions-Integration — Echte Daten für Konkurrenz, Hashtags, Painpoints

**Erstellt:** 2026-05-07
**Aktualisiert:** 2026-05-07 (Architektur-Wechsel: MCP-in-Session → GitHub Actions Cron, dauerhafte Lösung)
**Status:** PHASE-1-IMPLEMENTIERT — wartet auf APIFY_API_TOKEN als GitHub Repo-Secret
**Zweck:** Apify in GitHub Actions einbinden, damit täglich echte Konkurrenz-Daten ins Repo committet werden. Skills (`/freitag-hooks`, `/montag`, `/produkt`, `/funnel`) lesen die fertigen JSON-Files — keine Token-Eingabe pro Session, keine veralteten Web-Schätzungen mehr.

---

## 1. Was dieser Plan löst

**Aktuelles Problem (2026-05-07 Session):**
Bei der Konkurrenz-Recherche „Top Creator in deiner Nische" wurden Followerzahlen aus alten Influencer-Verzeichnissen rausgezogen — Linda Bogadi mit angeblich 15-30k, real 2.490. Patricias berechtigtes Bauchgefühl: „ohne Insta zu prüfen kommt nur erfundener Mist raus".

**Wurzel:**
Instagram hat keine offene API. WebSearch + WebFetch sehen nur Bio-Texte, alte Verzeichnisse, Sekundär-Erwähnungen. Echte Followerzahl, Like-Counts, Posting-Frequenz, virale Posts → unsichtbar.

**Lösung:**
Apify ist ein Marktplatz für „Actors" (vorgefertigte Scraping-Roboter). Sie haben einen offiziellen MCP-Server, der sich wie Notion/Canva/GitHub in Claude Code einbinden lässt. Danach kann ich aus jedem Skill auf Zuruf:
- Profil-Daten (Followerzahl, Bio, Posts) ziehen
- Top-Posts mit echten Engagement-Zahlen
- Hashtag-Performance live
- Kommentare als Lead-Quelle
- Reddit/Foren als Painpoint-Quelle
- Google-Trends, TikTok, YouTube — gleicher Aktor-Pool

---

## 2. Was Apify ist (kurz)

- **Plattform:** apify.com — Web-Scraping-as-a-Service
- **Pricing:** Free-Tier mit 5 USD Credits/Monat (reicht laut Schätzung für 200-500 Profil-Checks). Starter ab 49 USD/Monat falls Patricia mehr will.
- **MCP-Server:** Offiziell von Apify gepflegt, Standard-Integration in Claude Code
- **Datenschutz:** Apify scrapt nur **öffentliche** Daten — DSGVO-Graue-Zone bei Personenprofilen, deshalb Nutzungsfokus auf öffentliche Business-Accounts und aggregierte Daten

---

## 3. Architektur — GitHub Actions als Daten-Layer

```
Täglich 06:00 Schweiz (GitHub Actions Cron)
         ↓
.github/workflows/apify-scrape.yml startet
         ↓
Liest context/competitor-watchlist.json (6 Accounts)
         ↓
scripts/apify/scrape-competitors.js ruft Apify Actor:
   POST api.apify.com/v2/acts/apify~instagram-profile-scraper/run-sync-get-dataset-items
   (mit APIFY_API_TOKEN aus GitHub Secret)
         ↓
Actor liefert in 1-3 Min: Profile + letzte 25 Posts pro Account
         ↓
Script schreibt:
   outputs/apify-runs/competitors-YYYY-MM-DD.json (rohdaten)
   outputs/apify-runs/competitors-YYYY-MM-DD.md   (lesbare Summary mit Top 5 Posts)
         ↓
git commit + push (github-actions[bot])
         ↓
Ab jetzt verfügbar in jeder Claude-Session
         ↓
/freitag-hooks · /montag · /produkt · /funnel lesen die JSON-Files
   bei Bedarf zur Hook-Inspiration / Painpoint-Mining / Trend-Check
```

**Manueller Trigger** für Ad-hoc-Scrapes: GitHub UI → Actions → "Apify Competitor Scrape" → Run workflow → optional Handles als Komma-Liste eingeben.

**Skill-Integration (Phase 2):**
- `/freitag-hooks` liest jüngste Summary, zieht Hook-Inspiration aus Top-Posts
- `/montag` checkt Layout-/Format-Trends vor Build
- `/produkt` Mode „Markt-Research" — Reddit-Painpoints (separater Workflow Phase 3)
- `/funnel` Mode 3 (Ads) — Hashtag-Performance + Konkurrenz-Funnel-Beobachtung

---

## 4. Welche Apify-Actors wir nutzen (Initial-Set)

| Actor | Zweck | Geschätzte Kosten/Lauf |
|-------|-------|------------------------|
| `apify/instagram-profile-scraper` | Profil + Followerzahl + Bio | ~0.01 USD pro Profil |
| `apify/instagram-post-scraper` | Posts mit Likes/Comments/Caption | ~0.005 USD pro Post |
| `apify/instagram-hashtag-scraper` | Top-Posts unter Hashtag | ~0.05 USD pro Hashtag-Run |
| `apify/instagram-comment-scraper` | Kommentare als Lead-Quelle | ~0.01 USD pro Post |
| `apify/reddit-scraper-lite` | Painpoints aus Subreddits | ~0.10 USD pro Lauf |
| `apify/google-search-scraper` | Konkurrenz-SEO + Sales-Pages | ~0.05 USD pro Query |

**Realistischer Monats-Verbrauch bei wöchentlicher Nutzung:**
- Wöchentlich 10 Konkurrenz-Profile + je 25 Posts = 4 × (10 × 0.01 + 250 × 0.005) = ~5.40 USD
- Monatlich 5 Hashtag-Runs = 0.25 USD
- Monatlich 2 Reddit-Painpoint-Runs = 0.20 USD
- **Total ≈ 6 USD/Monat** → knapp über Free-Tier

→ **Empfehlung:** Start mit Free-Tier, nach 4 Wochen Verbrauch prüfen, ggf. Starter-Plan.

---

## 5. Was Patricia tun muss (1× Setup, dann nie wieder)

### Schritt 1: Apify-Account anlegen (~5 Min)
1. Auf https://apify.com → „Sign up free" mit Business-Email
2. Email bestätigen
3. Im Dashboard: **Settings → Integrations → API token kopieren**

### Schritt 2: Token als GitHub Repo-Secret hinterlegen (~2 Min)
1. GitHub UI: `pnulmann-hue/mumlifebalance-workspace` → **Settings → Secrets and variables → Actions → New repository secret**
2. Name: `APIFY_API_TOKEN`
3. Value: der Token aus Schritt 1
4. Save

**Damit ist das Setup abgeschlossen.** Token lebt sicher im Repo-Secret, persistiert dauerhaft, taucht nie in einer Session oder einem Commit auf. Identisches Pattern wie `ANTHROPIC_API_KEY`, `BLOTATO_API_KEY` etc. die bereits genutzt werden.

### Schritt 3 (sobald Branch gemerged): Erster Test-Lauf (~3 Min)
1. GitHub UI → **Actions → "Apify Competitor Scrape" → Run workflow**
2. Optional: Handles-Feld leer lassen → scrapt komplette Watchlist (6 Accounts)
3. Workflow läuft 1-3 Min, committed Ergebnisse nach `outputs/apify-runs/`
4. Patricia oder ich öffnen `competitors-YYYY-MM-DD.md` und sehen ECHTE Daten

**Aufwand für Patricia gesamt: ~10 Min** einmalig.

---

## 6. Integration in bestehende Skills (Phase 2, nach Test-Lauf)

### `/freitag-hooks` (Priorität 1)
**Ergänzung:** Vor Hook-Generierung scant der Skill 6-10 Konkurrenz-Profile, extrahiert die 3 best-performenden Hooks der Woche. Diese fließen als „Konkurrenz-Inspiration" in den Generator. Patricias Brand-Voice bleibt Filter — kein Klauen, sondern Pattern-Adaption.

### `/montag` (Priorität 1)
**Ergänzung:** Build-Phase prüft, ob Konkurrenz-Karussells/Reels diese Woche neue Layout-Trends zeigen. Findet sich ein klarer Trend → wird als Vorschlag (nicht Pflicht) eingeflochten.

### `/produkt` Mode „Markt-Research" (Priorität 2)
**Ergänzung:** Statt nur WebSearch auf Google-Trends → echtes Reddit-Scraping (r/Mompreneurs, r/EssentialOils, r/SAHM). Ergebnis: Original-Sätze von echten Müttern, die Patricias nächster Painpoint-Hook werden.

### `/funnel` Mode 3 — Ads (Priorität 2)
**Ergänzung:** Vor jeder Ad-Empfehlung ein Hashtag-Performance-Check + Konkurrenz-Funnel-Beobachtung (welche Freebies bewerben sie gerade?).

### `/karussell` & `/reels` (Priorität 3, optional)
**Ergänzung:** Hook-Brainstorm-Modus kann auf Wunsch Konkurrenz-Hooks als Variations-Quelle einbeziehen.

---

## 7. Kosten-Cap und Sicherheits-Limits

**Hard-Limits in jedem Skill:**
- Max. 1 Apify-Run pro Skill-Aufruf, außer Patricia gibt explizit „mehr" frei
- Logging in `outputs/apify-runs/YYYY-MM-Verbrauch.md` — am Monatsende einsehbar
- Wenn `APIFY_MONTHLY_CAP` (default: 8 USD) erreicht → Skills kippen auf WebSearch zurück und melden Patricia
- Cache: 24h-Cache pro Profil-Scrape, damit `/freitag-hooks` und `/montag` nicht zweimal die gleiche Konkurrenz scannen

**Datenschutz:**
- Keine Speicherung von Email-Adressen oder Personendaten aus Kommentar-Scrapes ohne expliziten Use-Case
- Kommentar-Scraping nur für Public-Business-Accounts und nur als Aggregat („127 Kommentare zum Thema X")
- Niemals Privatprofile, niemals private Hashtags

---

## 8. Test-Plan (nach Token-Hinterlegung)

**Test 1 — Smoke-Test über manuellen Workflow-Trigger:**
- GitHub UI → Run workflow mit leerem Handles-Feld
- Erwartung: Workflow läuft grün, neuer Commit in `outputs/apify-runs/`

**Test 2 — Linda-Bogadi-Validation (Ad-hoc):**
- Run workflow mit Handles-Input: `linda.bogadi`
- Erwartung: Followerzahl ≈ 2.490 (matcht was Patricia auf IG sieht)
- Wenn ja: System ist ehrlich. Wenn deutlich abweichend: Actor-Konfiguration prüfen.

**Test 3 — Eigene Profile (Sanity-Check):**
- Run workflow mit Patricias Mentoring- und doTERRA-Handles
- Erwartung: Followerzahlen matchen die Realität
- Bonus: Gibt erste Selbst-Daten für spätere Wachstums-Tracking

**Test 4 — Cron-Lauf am nächsten Morgen:**
- 06:00 Schweiz: Workflow läuft automatisch
- Neuer Commit von `github-actions[bot]` mit Datum
- Patricia kriegt täglich ohne Eingriff frische Konkurrenz-Daten

---

## 9. Patricias Entscheidungen (2026-05-07)

1. **Plan:** Free-Tier zum Start, 4 Wochen testen
2. **Watchlist:** Top 6 aus heutiger Recherche
   - Mentoring: Caroline Preuss, Julia Trost, Katharina Lewald
   - doTERRA: Heilkunstwerk, Aroma Mama, AROMA 1x1
   - → wird in `context/competitor-watchlist.json` festgehalten
3. **Lead-Scraping:** Erlaubt, nur Aggregat-Daten (keine Personenbezogenheit)
4. **Cache:** 24h (Default)

**Noch offen:** Apify-API-Token von Patricia (Schritt 1 in Section 5)

---

## 10. Aufwand-Schätzung

| Phase | Aufwand Patricia | Aufwand Claude | Wann |
|-------|-----------------|----------------|------|
| Phase 1: Infrastruktur (Watchlist, Script, Workflow) | 0 | ~60 Min | **erledigt 2026-05-07** |
| Patricia: Apify-Account + Repo-Secret | ~10 Min | 0 | wartet |
| Patricia: Branch mergen | ~1 Min | 0 | wartet |
| Test-Läufe via Workflow-Dispatch | ~3 Min | 0 | nach Merge |
| Phase 2: `/freitag-hooks` liest JSON | 0 | ~45 Min | nach erstem grünen Lauf |
| Phase 2: `/montag` liest JSON | 0 | ~30 Min | nach erstem grünen Lauf |
| Phase 3: Reddit-Painpoint-Workflow | 0 | ~45 Min | wenn Phase 1+2 stabil |
| Phase 3: `/funnel` Mode 3 Hashtag-Trends | 0 | ~30 Min | wenn Phase 1+2 stabil |

**Gesamt für Patricia:** ~14 Min einmalig, dann läuft alles automatisch und dauerhaft.

---

## 11. Erfolgs-Kriterien

Nach Phase 1 abgeschlossen heisst:
- [ ] Apify-MCP läuft, ich kann auf Zuruf jedes Public-Profil scannen
- [ ] Test-Lauf zeigt: Followerzahlen matchen die Realität (Linda-Bogadi-Test bestanden)
- [ ] `/freitag-hooks` zieht ab nächstem Freitag echte Konkurrenz-Hooks ein
- [ ] Verbrauchs-Log existiert, Patricia weiss jederzeit wieviel sie verbraucht
- [ ] Die heutige Top-10-Liste wird ersetzt durch eine echte Daten-Liste

---

## 12. Was NICHT in diesem Plan steckt (bewusst)

- TikTok-Scraping (kann später dazu, jetzt nicht)
- LinkedIn-Scraping (Patricia ist nicht stark drauf, später)
- Email-Funnel-Reverse-Engineering (rechtliche Grauzone, separater Plan)
- Auto-DM auf Lead-Listen (das macht ManyChat schon, nicht doppeln)
- Eigene Custom-Apify-Actors schreiben (overkill für Phase 1)
