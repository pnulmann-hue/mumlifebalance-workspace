# Mindset & Energetik — Wissensbasis für Mama-CEO-Kurs

**Zweck:** Sammelt Patricias persönliche Energetik-/Mindset-Quellen, damit der `/produkt`-Skill und die Outline-Schärfung des Mama-CEO-Kurses genau auf diesen Inhalten aufsetzen — statt mit allgemeinen Platzhaltern zu arbeiten.

**Letzte Aktualisierung:** 2026-04-30
**Verwendet von:** `outputs/produkte/mama-ceo/06-energetik-mindset-integration.md` (folgt sobald Inhalte hier liegen)

---

## Ordner-Struktur

| Ordner | Quelle | Was hier rein soll |
|---|---|---|
| `aurachirurgie/` | Patricias Aurachirurgie-Kurs | Transkripte, PDFs, eigene Notizen, Übungs-Skripte |
| `elke-mayr/` | Elke Mayr Unterlagen | Workbook-PDFs, Coaching-Notizen, Methoden-Beschreibungen |
| `karriere-mum/` | KarriereMum-Programm/Material | Module, Workbooks, Methodik |
| `awaken-the-star-sternbauer/` | Christina Sternbauer · Awaken the Star | Modul-PDFs, Aufnahmen-Transkripte, eigene Notizen |

---

## Upload-Anleitung für Patricia

### Variante A — Direkt-Upload via Claude Code (Web)

1. **Im Chat** auf das Anhang-Icon klicken (📎)
2. Datei(en) auswählen (PDF, TXT, DOCX, MP3 — alles geht)
3. Im Prompt schreiben: „Speicher diese Datei in `reference/mindset/[ordner]/`"
4. Wiederhole für jede Quelle

### Variante B — Via Mac mit Git (lokal)

```bash
# Im lokalen Mum Life Balance Workspace
cd ~/Desktop/Mein\ Business/reference

# Aurachirurgie
cp -r [Aurachirurgie-Ordner] /Pfad/zum/Workspace/reference/mindset/aurachirurgie/

# Elke Mayr
cp -r [Elke-Mayr-Ordner] /Pfad/zum/Workspace/reference/mindset/elke-mayr/

# KarriereMum
cp -r [KarriereMum-Ordner] /Pfad/zum/Workspace/reference/mindset/karriere-mum/

# Awaken the Star
cp -r [Awaken-Star-Ordner] /Pfad/zum/Workspace/reference/mindset/awaken-the-star-sternbauer/

# Committen + pushen
cd /Pfad/zum/Workspace
git add reference/mindset/
git commit -m "Mindset-Quellen für Mama-CEO-Kurs hochgeladen"
git push
```

---

## Was passiert nach dem Upload

Sobald die Files im Repo liegen, kann der Assistent:

1. **Volltext lesen** und Patricias eigene Sprache extrahieren (Konzepte, Bilder, Übungen)
2. **Pro Modul** in der Mama-CEO-Outline gezielt 1 energetisch-Lektion + 1-2 Mindset-Slides ergänzen — mit konkreten Bezügen zu deinen Quellen
3. **Eine Datei** `outputs/produkte/mama-ceo/06-energetik-mindset-integration.md` erstellen, die genau aufzeigt: aus Quelle X kommt Methode Y in Lektion Z
4. **Zitate + Übungen** in Sprechnotizen einbauen, damit die Lektionen sich nach dir anhören (nicht nach generischer Mindset-Sprache)

---

## Was reicht (Minimum-Pflicht)

Pro Quelle braucht es mindestens **eines** dieser Formate:
- **Transkripte** (TXT/MD) — beste Qualität, kann direkt zitiert werden
- **PDFs** (Workbook, Module-Outline, Methode-Doku)
- **Eigene Notizen** (Markdown oder TXT, sogar handschriftlich-abgetippt geht)
- **MP3** (würde ich später transkribieren via Skript)

**Wenn du nur Notizen hast:** Tipp die 3-5 Kern-Konzepte pro Quelle in eine `kern-konzepte.md` rein. Beispiel:

```markdown
# Aurachirurgie — Kern-Konzepte (Patricias Notizen)

## 1. Aura-Klärung
- Methode: ...
- Wann anwenden: ...
- Anleitung: ...

## 2. Energie-Leck schliessen
- ...
```

---

## Status-Tracker

| Quelle | Im Repo? | Format | Letzter Upload |
|---|---|---|---|
| Aurachirurgie | ❌ in diesem Repo nicht gefunden (alle Branches durchsucht) | — | — |
| Elke Mayr | ❌ in diesem Repo nicht gefunden | — | — |
| KarriereMum | ❌ in diesem Repo nicht gefunden | — | — |
| Awaken the Star (Sternbauer) | ❌ in diesem Repo nicht gefunden | — | — |

**Hinweis 2026-04-30:** Patricia hat die Materialien laut eigener Aussage „in GitHub verschoben" — vermutlich in ein **anderes Repo** (möglicherweise ein Bot-Repo). Der Web-Claude-Sandbox kann nur auf `pnulmann-hue/mumlifebalance-workspace` zugreifen, nicht auf andere Repos. Patricia bitte: entweder (a) Files in dieses Repo kopieren, (b) Pfad/Repo-Name nennen so dass sie kopiert werden können, oder (c) Drag-and-Drop in den Chat.

---

## Verbindung zu vorhandenem Material

Bereits im Workspace — wird als zusätzliche Mindset-Wissensbasis genutzt:
- `reference/Laura Melina Seiler/` — 3 URL-Verweise (Glaubenssätze · Meditation · Morgenroutine)
- `reference/julia-trost/Transkripte Videocalls/` — Mindset-relevant: `Energie.txt`, `_sortiert/16 Kurse für 15€/Dein Mindset - 1143329299.txt`, `_sortiert/20k Strategie/Strategie + Mindset - 852442453.txt`, `_sortiert/Online Business Academy (OBA)/Dein Launch Mindset - 984218050.txt`
- `reference/Lina Duve Coaching/` — Coaching-Sales-Material (Bezug prüfen)
