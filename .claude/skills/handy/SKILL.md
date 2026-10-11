---
name: handy
description: "neues Foto- und Videomaterial vom Handy holen und einsortieren (Album Content-Inbox)"
---
Hol mein neues Content-Material vom Handy.

## Was du tust

```bash
python scripts/handy/hol-content.py
```

Das liest das Album **`DCIM/Content-Inbox`** auf meinem S25 Ultra und legt ab:

| Was | Wohin | Wofür |
|---|---|---|
| Videos | `video/input/` | `/videoschnitt`, `/reels` |
| Fotos | `context/content-assets/inbox/YYYY-MM/` | `/karussell`, `/story` |
| Standbild pro Video | `context/content-assets/vorschau/` | damit **du** siehst, was drauf ist |
| Bericht | `context/content-assets-inbox.md` | Übersicht des Laufs |

Danach: **schau dir die Standbilder tatsächlich an** (Read auf die PNGs), bevor
du mir sagst, was da ist. Aus Dateinamen lässt sich nichts über den Inhalt
sagen. Dann berichte mir in einem Satz pro Clip, was drauf ist und wofür es
taugt (Talking Head / B-Roll / Foto fürs Karussell / Story-Bild).

## Andere Alben

```bash
python scripts/handy/hol-content.py --album Reel-Videos --zeigen   # nur auflisten
python scripts/handy/hol-content.py --album Businessfotos-Videos
```

Welche Alben es gibt und was drin liegt, steht in `context/content-assets-index.md`.

## Harte Regeln

- **Auf dem Handy wird nie gelöscht oder verschoben.** Das Skript kopiert nur.
  (Geht technisch auch nicht — CrossDevice erlaubt Schreiben und Anlegen, aber
  kein Löschen. Wenn auf dem Handy etwas weg soll, mache ich das selbst in der Galerie.)
- Was schon geholt wurde, steht in `context/content-assets-inbox-log.json` und wird
  übersprungen. Zweimal laufen lassen schadet nicht.
- Nichts davon geht ins Git — `video/**` und Bilddateien sind gitignored, das Repo ist public.
- Wenn das Handy nicht erreichbar ist, sag es mir, statt auf alte Dateien auszuweichen.

## Wenn ich sage „ich hab was Neues aufs Handy gelegt"

Dann läufst du das Skript, schaust dir die Vorschaubilder an und fragst, was ich
damit vorhabe — statt sofort etwas zu bauen.
