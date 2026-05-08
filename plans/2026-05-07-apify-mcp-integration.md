# Plan: Apify MCP-Integration — Echte Daten für Konkurrenz, Hashtags, Painpoints

**Erstellt:** 2026-05-07
**Status:** APPROVED — wartet nur noch auf Apify-Token von Patricia, dann `/implement`
**Zweck:** Apify als MCP-Server einbinden, damit Patricias Skills (`/freitag-hooks`, `/montag`, `/produkt`, `/funnel`) auf echte Instagram-/Web-Daten zugreifen können statt auf Web-Such-Schätzungen.

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

## 3. Architektur — Was wo läuft

```
Patricia tippt /freitag-hooks
         ↓
Skill liest Wochenfokus aus Notion
         ↓
Skill ruft Apify-MCP auf:
   "Hol Top-5-Posts der letzten 7 Tage von 6 Konkurrenz-Accounts"
         ↓
Apify-Actor läuft 1-2 Min im Hintergrund
         ↓
Actor liefert JSON: Caption, Likes, Comments, Hashtags, Posting-Zeit
         ↓
Skill analysiert → "Konkurrenz-Hook der Woche" → fließt in Hook-Generator
         ↓
20 Hooks an Patricia via Telegram (jetzt mit echtem Inspirations-Anteil)
```

**Gleiche Mechanik in:**
- `/montag` — Konkurrenz-Performance-Check vor Wochen-Build
- `/produkt` Mode „Markt-Research" — Reddit-Scraping für Painpoints
- `/funnel` Mode 3 (Ads) — Konkurrenz-Ad-Library + Hashtag-Trends

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

## 5. Was Patricia tun muss (1x Setup)

### Schritt 1: Apify-Account anlegen (~5 Min)
1. Auf https://apify.com → „Sign up free" mit Patricias Business-Email
2. Email bestätigen
3. Im Dashboard: **Settings → Integrations → API token kopieren**
4. Patricia schickt mir den Token via Chat

### Schritt 2: MCP-Server aktivieren (~2 Min, ich mache das)
1. Ich packe den Token in `.claude/settings.local.json` (gitignored)
2. Ich registriere den Apify-MCP-Server in der Claude-Code-Konfiguration
3. Restart der Session → MCP-Tools verfügbar

### Schritt 3: Test-Lauf (~5 Min, ich mache das)
1. Ich rufe `apify/instagram-profile-scraper` für deinen eigenen Account `@patriciakoradi` auf (oder den Mentoring-Handle)
2. Verify: Bekommen wir saubere Followerzahl + die letzten 12 Posts?
3. Wenn ja: System läuft

### Schritt 4: Erste echte Konkurrenz-Analyse (~10 Min, ich mache das)
1. Ich scanne die 6 Top-Konkurrenz-Accounts aus der heutigen Liste
2. Liefere dir den ECHTEN Vergleich: Followerzahl, Top-5-Posts mit echten Hooks und Like-Zahlen
3. Du siehst sofort: jetzt sind die Zahlen real

**Aufwand für Patricia gesamt: ~10 Min** (Sign-up + Token schicken). Rest mache ich.

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

## 8. Test-Plan

**Test 1 — Eigene Profile (Sanity-Check):**
- Patricias Mentoring-Handle scrapen → Followerzahl matcht was sie sieht? ✓
- Patricias doTERRA-Handle dito ✓

**Test 2 — Linda-Bogadi-Validation:**
- @linda.bogadi scrapen → bekommen wir 2.490 oder ähnlich? Wenn ja: System ehrlich. Wenn nein: Actor justieren.

**Test 3 — Hashtag-Live-Test:**
- `#mumlifebalance` Top-Posts der letzten 7 Tage → Plausibilität prüfen
- `#aetherischeoele` dito

**Test 4 — Volle Konkurrenz-Analyse:**
- Alle 6 Top-3-Accounts (3 Mentoring + 3 doTERRA) scannen
- Output: Tabelle mit echten Followerzahlen, je 5 Top-Posts mit Hook + Like/Comment-Counts
- Diese Tabelle ersetzt die Web-Such-Liste von heute

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
| Setup (Schritt 1-3) | ~10 Min | ~15 Min | Heute, sobald grün |
| Test-Lauf (Schritt 4) | 0 Min (du checkst nur Output) | ~30 Min | Direkt nach Setup |
| Skill-Integration `/freitag-hooks` | 0 Min | ~45 Min | Diese Woche |
| Skill-Integration `/montag` | 0 Min | ~30 Min | Diese Woche |
| `/produkt` + `/funnel` Updates | 0 Min | ~45 Min | Nächste Woche |
| Cap- & Cache-Logging | 0 Min | ~30 Min | Diese Woche |

**Gesamt für dich:** ~10 Min zum Anstossen, dann zurücklehnen.

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
