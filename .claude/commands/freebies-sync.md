# /freebies-sync — Patricias Freebies analysieren

Patricia hat 0€-Produkte, Workbooks, Minikurse und Challenges, die via ManyChat-Keywords ausgeliefert werden. Damit der Content-Assistent in Reels/Karussells/Captions sinnvoll auf Freebies Bezug nehmen kann (nicht nur den Titel erwähnen, sondern Inhalte referenzieren), brauchen wir Zugriff + Analyse.

Dieser Command synct neue oder aktualisierte Freebies aus `context/freebies/` in eine zentrale Wissensdatei `context/patricia-freebies.md`.

---

## Erwartete Ordnerstruktur

```
context/freebies/
├── mentoring/
│   ├── 0-fahrplan/                # Keyword SYSTEM / FAHRPLAN
│   │   ├── fahrplan.pdf
│   │   └── README.md              # optional: Kurz-Beschreibung, Ziel, CTA-Flow
│   ├── 0-quiz/                    # Keyword QUIZ
│   ├── 0-starterguide/            # Keyword SICHTBAR / ANLEITUNG
│   ├── 0-lead-challenge/          # Keyword LEAD
│   ├── workbook-von-0-auf-echt/   # Keyword ECHT1
│   ├── minikurs-finde-dein-thema/ # Keyword THEMA
│   └── minikurs-vom-networkwissen/# Keyword PRODUKT
└── doterra/
    ├── 5-schritte-zur-freiheit/   # aktueller doTERRA-Freebie
    └── padlet-zurück-zu-deiner-energie/  # Kur-Vorstufe mit Padlet-Link
```

Falls Freebies als PDF/ZIP vorliegen: direkt ablegen. Falls als Notion-Seite / Google-Drive-Link: `.md`-Datei mit `SOURCE: [URL]` als Zeiger-Datei anlegen.

---

## Ablauf

### Schritt 1: Bestandsaufnahme

1. Lies `context/patricia-freebies.md` (falls vorhanden, sonst neu anlegen).
2. Scanne `context/freebies/` rekursiv auf Freebie-Unterordner.
3. Vergleiche: Welche sind neu? Welche wurden aktualisiert (mtime)?

### Schritt 2: Analyse pro Freebie

Pro Freebie extrahiere:
- **Name** + **Keyword** (aus ManyChat) + **Zielgruppe** (Mentoring/doTERRA)
- **Ziel des Freebies** (was lernt/bekommt die Person?)
- **Kern-Inhalte** (3-7 Haupt-Punkte, Bullet-Liste)
- **Transformation** (vorher → nachher)
- **Sprache/Ton** (typische Phrasen, falls PDF-Analyse möglich)
- **Next-Step** (wohin führt es? → Minikurs, Kur, 1:1?)
- **Content-Bezug** (Zu welchen Content-Pillars passt es?)

Bei PDFs: `Read`-Tool nutzen. Bei Notion-Links: via Notion-MCP fetchen. Bei Google-Drive: ggf. mit User klären (evtl. Link extrahieren via WebFetch).

### Schritt 3: Integration in `patricia-freebies.md`

Struktur der Datei:

```markdown
# Patricias Freebies — Inhalte + Content-Bezüge

## Mentoring-Profil

### [Name] (Keyword: XYZ)
- **Zielgruppe**: Mamas im NM, die ...
- **Ziel**: Die Leserin kann nach dem Freebie ...
- **Inhalte**: [3-7 Bullets]
- **Transformation**: Von X → zu Y
- **Next-Step**: Führt zu [Produkt]
- **Content-Bezug**: Pillars X, Y
- **Pfad**: `context/freebies/mentoring/xyz/...`

### [Weiteres Freebie]
...

## doTERRA-Profil
...

## Cross-Referenz für /reels + /karussell
| Thema | Passendes Freebie | CTA-Keyword |
|-------|-------------------|-------------|
| Positionierung | Workbook Von 0 auf echt | ECHT1 |
| ... | ... | ... |
```

### Schritt 4: Bestätigung

Zeige Patricia:
- Neue Freebies: Liste
- Aktualisierte Freebies: Liste
- Link zur `patricia-freebies.md`
- Neue Cross-Referenz-Einträge

### Schritt 5: Memory + Commands aktualisieren

- Ergänze `memory/project_content-engine.md` wenn neue Freebies live sind
- `context/manychat-keywords.md` prüfen: stimmen Keyword ↔ Freebie noch überein?
- `/reels` und `/karussell` Commands laden `patricia-freebies.md` bereits via framework — **keine Änderung nötig**, wenn das File-Pfad konsistent ist

---

## Regeln

1. **Keine Dubletten** — wenn ein Freebie schon analysiert ist und mtime unverändert, überspringen.
2. **PDFs mit `Read` analysieren** — nicht Binärdaten in patricia-freebies.md schreiben, nur Synthese.
3. **Notion-Links**: Via MCP fetchen, Inhalte synthetisieren.
4. **Backup**: Vor Write die alte Datei nach `context/_archiv/patricia-freebies-YYYY-MM-DD.md`.
5. **Content-Bezug ist Pflicht** — jedes Freebie muss Pillars zugeordnet sein (damit der Reel-Assistent weiss wann er es empfehlen soll).

---

$ARGUMENTS
