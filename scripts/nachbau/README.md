# Nachbau — fremde Reels zerlegen und für eigenes Material neu bauen

**Zweck:** Ein Reel, das nachweislich verkauft oder Kommentare holt, in seine
Bausteine zerlegen — Hook, Schnittrhythmus, Bildsprache, CTA — und daraus ein
Briefing für Patricias **eigenes** Material machen.

Nicht kopieren. Die Bauweise übernehmen, Szene und Zahlen kommen aus ihrem Leben.

---

## Schritt 1 — Zerlegen

```bash
# Lokale Datei (geht immer)
python scripts/nachbau/zerlegen.py pfad/zum/video.mp4 --slug beispiel

# YouTube / TikTok (laden direkt)
python scripts/nachbau/zerlegen.py "https://www.tiktok.com/@name/video/123"

# Instagram (braucht Cookies, siehe unten)
python scripts/nachbau/zerlegen.py "https://www.instagram.com/reel/XXXX/"
```

**Optionen**

| Option | Wofür |
|---|---|
| `--slug name` | Ordnername festlegen |
| `--schwelle 0.20` | feiner schneiden (Standard 0.30, 0.45 = grob) |
| `--modell medium` | genaueres Transkript, dauert länger |
| `--ohne-text` | Transkript überspringen |
| `--raster 1` | **zusaetzlich alle 1 s ein Standbild** in `raster/`, benannt nach der Sekunde — fuer zeitgenaues Nachbauen von Animationen („Sekunde 2 bis 5, hier springt der Text rein") |
| `--cookies datei` | eigene cookies.txt |
| `--browser edge` | Cookies aus dem Browser (Browser muss zu sein) |

**Ergebnis** in `nachbau/<datum>-<slug>/`:

```
video.mp4      das Video
meta.json      Dauer, Auflösung, Quelle, Beschreibung
words.json     jedes Wort mit Zeitstempel
analyse.json   maschinenlesbar
analyse.md     ← das liest Claude
bilder/        ein Standbild je Einstellung
```

Läuft **komplett lokal**. Kein API-Schlüssel, keine Kosten.
Transkription über faster-whisper auf der CPU.

---

## Schritt 2 — Claude liest und baut nach

Im Chat: *„Schau dir `nachbau/<slug>/` an und bau mir das für mein Material nach."*

Claude schaut die **Standbilder wirklich an** (nicht nur die Dateinamen), benennt
den Mechanismus und schreibt ein Briefing: Hook · Sprechtext · Schnittfolge ·
Titelbild · Caption · CTA — alles in Patricias Stimme, mit ihren Szenen.

---

## 🔐 Instagram: Cookies einmal einrichten

Instagram gibt Videos nur eingeloggt heraus. yt-dlp kommt an **Chrome**-Cookies
seit Version 127 nicht mehr ran (App-Bound Encryption, yt-dlp Issue #10927),
**Edge** klappt nur, wenn der Browser geschlossen ist.

**Der verlässliche Weg — einmal zwei Minuten:**

1. Browser-Erweiterung **„Get cookies.txt LOCALLY"** installieren
2. Auf `instagram.com` gehen (eingeloggt), Erweiterung → Export
3. Datei ablegen als `scripts/nachbau/cookies.txt`

Danach findet das Skript sie von selbst, jedes Mal.

**Ohne Cookies:** Video von Hand laden (z.B. über einen Downloader deiner Wahl)
und die Datei übergeben. Dauert 20 Sekunden und geht immer.

*(cobalt.tools als API geht nicht mehr — die verlangen seit 2025 einen Schlüssel.)*

---

## 🚨 Regeln

- **`nachbau/` ist gitignored.** Das Repo ist öffentlich, die Videos sind fremdes
  Material. Nur das fertige Briefing für Patricias eigenes Material darf nach
  `outputs/`.
- **Nie den Text übernehmen.** Der Hook wird durch die Blackliste und den letzten
  Check gedreht, Szene und Zahlen kommen aus Patricias Leben.
  Siehe Regel *Hooks = Inspiration, nicht Copy-Paste*.
- **Herkunft vermerken.** In jedem Briefing steht, von welchem Beitrag die Idee kommt.

---

## Was noch fehlt (Teil 2: Generieren)

Der Analyse-Teil steht. Für den Generier-Teil — aus dem Briefing automatisch
Bilder und Videoclips bauen — fehlen zwei Zugänge:

| Anbieter | Wofür | Wo | Kosten |
|---|---|---|---|
| Google AI Studio | Bildgenerierung (Nano Banana) | `aistudio.google.com/apikey` | ~2 Rp. je Bild |
| Fal.ai | Videogenerierung (Veo3 Lite / Kling) | `fal.ai/dashboard/keys` | ~50 Rp. je Clip |

**Vorhanden sind bereits:** Anthropic-Schlüssel (in `.env`), FFmpeg, Node 24,
yt-dlp, faster-whisper. Whisper läuft lokal — der OpenAI-Schlüssel aus fremden
Anleitungen wird hier **nicht** gebraucht.

**Arbeitsregel wenn Teil 2 kommt:** erst alle Bilder fertig machen (billig zum
Ausprobieren), dann erst Videos rendern (teuer). Bei beiden Anbietern ein
Ausgabe-Limit setzen, bevor der Schlüssel kopiert wird.
