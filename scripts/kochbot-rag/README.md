# Kochbot-RAG — Rezeptdatenbank fuer den `/mealplan`-Slash-Command

Macht Patricias Rezept-PDFs (~1900 Stueck in `rezepte/`) und Kochwissen-PDFs
(MyBodyAdvice, 7hauben-Brotkurse) per Supabase + pgvector durchsuchbar — von
ueberall, auch aus der Web-Claude-Sandbox heraus.

```
rezepte/*.pdf       ─┐
kochwissen/*.pdf    ─┤
                     ▼
              [ ingest.py ]   ──── OpenAI text-embedding-3-small ───►  Supabase.documents
                                                                            │
                                                                            ▼
              [ query.py "Quark Pancakes" ]  ◄────  /mealplan-Slash-Command ────  Patricia
```

---

## Setup (einmalig)

### 1. Supabase-Projekt anlegen

1. Auf [supabase.com](https://supabase.com) ein neues Projekt erstellen
   (Free-Tier reicht — die Daten sind klein genug).
2. **Settings → Database → SQL Editor** oeffnen.
3. Den Inhalt von [`schema.sql`](./schema.sql) komplett ausfuehren.
   Das aktiviert die `vector`-Erweiterung, legt die Tabelle `documents` an
   und registriert die Funktion `match_documents`.
4. **Settings → API** kopieren:
   - **Project URL** → `SUPABASE_URL`
   - **service_role secret** (NICHT der `anon`-Key!) → `SUPABASE_SERVICE_KEY`

### 2. OpenAI-Key besorgen

[platform.openai.com → API Keys](https://platform.openai.com/api-keys).
Embedding mit `text-embedding-3-small` kostet ~0.02 USD pro Million Tokens —
1900 Rezept-PDFs einmalig embedden landet typischerweise unter 1 USD.

### 3. `.env` erstellen

```bash
cd scripts/kochbot-rag
cp .env.example .env
# Werte einsetzen — die .env wird durch .gitignore geschuetzt
```

### 4. Python-Dependencies installieren

```bash
cd scripts/kochbot-rag
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 5. PDFs ingesten (einmalig, lokal wo die PDFs liegen)

```bash
python ingest.py
```

- Liest `rezepte/` und `kochwissen/` aus dem Workspace-Root.
- Idempotent: bereits ingestete Dateien werden uebersprungen.
- Mit `--force` werden bestehende Eintraege geloescht und neu erzeugt.
- Mit `--folder rezepte|kochwissen` nur ein Ordner verarbeiten.
- Dauer: ~5-15 Minuten fuer 1900 PDFs (haengt von OpenAI-Rate-Limits ab).

---

## Suchen (CLI)

```bash
python query.py "proteinreiche Quark-Pancakes"
python query.py "Sauerteig falten Stockgare" --folder kochwissen --top 8
python query.py "Zucchini verarbeiten" --format json
```

Threshold-Default: `0.3` (Cosine-Similarity, 0.0 = irrelevant, 1.0 = identisch).
Per `--threshold 0.5` strenger filtern, per `MATCH_THRESHOLD=0.2` in `.env`
permanent lockerer machen.

---

## Integration mit `/mealplan`

Der Slash-Command (`.claude/commands/mealplan.md`) ruft `query.py` auf, sobald
ein Rezept oder Kochwissen gebraucht wird. Beispiel-Flow:

1. Patricia: „Ich hab Quark, Eier, Haferflocken — was kann ich machen?"
2. `/mealplan` ruft `python scripts/kochbot-rag/query.py "Quark Eier Haferflocken Fruehstueck"` auf.
3. Top-5-Treffer aus Patricias eigenen Rezepten + 7hauben + MyBodyAdvice.
4. Claude formuliert Antwort auf Basis der Treffer (statt sich Rezepte auszudenken).

**Wichtig fuer die Web-Claude-Sandbox:** `.env`-Files persistieren nicht zwischen
Sessions. Patricia muss die `.env` jeweils neu erstellen oder die Werte einmal in
den Session-Env-Vars hinterlegen. Lokale Claude-Code-Sessions sind unproblematisch.

---

## Architektur-Entscheidungen

- **OpenAI text-embedding-3-small (1536 dim):** Beste Qualitaet pro Cent fuer
  deutsche Texte. Anthropic bietet keine eigenen Embeddings.
- **Chunk-Groesse 800 Tokens / 150 Overlap:** Standard fuer Rezepte (1 Rezept =
  1-3 Chunks); Kochwissen-Dokumente werden noch sinnvoll segmentiert.
- **pgvector + ivfflat:** Schnell genug fuer < 100k Chunks, kein dediziertes
  Vector-DB-Hosting noetig.
- **service_role Key:** noetig zum Schreiben in `documents`. Wird nur lokal +
  in der Slash-Command-Session verwendet, nie in Frontend-Code.

---

## Troubleshooting

**„rezepte/ existiert nicht — uebersprungen"** beim Ingesten in der
Web-Claude-Sandbox: Korrekt. Die Ordner sind via `.gitignore` ausgeschlossen
und nur lokal vorhanden. `ingest.py` MUSS lokal laufen.

**„0 Treffer" bei sinnvoller Suche:** Threshold zu hoch — versuch
`--threshold 0.2`, oder ueberpruefe ob `ingest.py` ueberhaupt durchgelaufen ist
(Supabase Table Editor → `documents` → row count).

**OpenAI Rate-Limit beim Ingesten:** `EMBED_BATCH = 100` in `ingest.py` reduzieren,
oder Sleep zwischen Batches einbauen. Tier-1-Account hat 3.500 Requests/Min.
