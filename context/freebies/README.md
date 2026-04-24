# Freebies — Wissensbasis für Content-Bezüge

## Zweck
Damit `/reels` und `/karussell` in Captions auf Patricias Freebies Bezug nehmen können (z.B. „Im Workbook zeige ich dir Schritt X"), brauchen sie Zugriff auf die Inhalte. Der `/freebies-sync`-Command analysiert alles hier und dokumentiert es in `context/patricia-freebies.md`.

## Ordnerstruktur

```
freebies/
├── mentoring/
│   ├── 0-fahrplan/                  # Keyword SYSTEM / FAHRPLAN
│   ├── 0-quiz/                      # Keyword QUIZ
│   ├── 0-starterguide/              # Keyword SICHTBAR / ANLEITUNG
│   ├── 0-lead-challenge/            # Keyword LEAD
│   ├── workbook-von-0-auf-echt/     # Keyword ECHT1
│   ├── minikurs-finde-dein-thema/   # Keyword THEMA
│   └── minikurs-vom-networkwissen/  # Keyword PRODUKT
└── doterra/
    └── 5-schritte-zur-freiheit/     # aktueller doTERRA-Freebie
```

## Wie Patricia einen neuen Freebie ablegt

1. Ordner anlegen mit sprechendem Namen (kleingeschrieben, Bindestriche)
2. Freebie-Datei(en) reinlegen (PDF, ZIP, DOCX, oder `.md` mit Notion/Drive-Link)
3. **Optional**: `README.md` im Unterordner mit:
   - Keyword (z.B. `QUIZ`)
   - Kurzbeschreibung (1-2 Sätze)
   - Transformation (vorher → nachher)
   - Next-Step-Produkt (wenn Lead-Magnet → wohin)
4. `/freebies-sync` aufrufen

## Externe Freebies (Notion, Google Drive, ThriveCart)

Wenn das Freebie **nicht lokal** liegt, eine `SOURCE.md` im Ordner anlegen:

```markdown
# [Freebie-Name]
Keyword: QUIZ
Zielgruppe: Mentoring
Hosted: Notion / GDrive / ThriveCart
URL: https://...
Zugriff: öffentlich / Login benötigt
```

Der `/freebies-sync`-Command fetcht öffentliche URLs oder nutzt Notion-MCP für Notion-Seiten.
