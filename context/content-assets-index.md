---
tags: [content, assets, tools]
---

# Content-Assets-Index — Foto- & Video-Pool

**Zweck:** Single Source of Truth, welches Bild-/Video-Material wo liegt — für Story- und Reel-Planung. Gepflegt am 2026-06-15. Handy = Samsung S25 Ultra, erreichbar vom PC über `C:\Users\pnulm\CrossDevice\S25 Ultra von Patricia\storage`.

> ⚠️ Claude kann den Handy-Speicher vom PC aus lesen/schreiben (CrossDevice), aber **nicht erkennen, was schon gepostet wurde**, und Fotos nur an Stichproben per Auge prüfen (sonst nur Dateinamen). Kuratieren = gemeinsam mit Patricia.

---

## 📸 STORY-BILDER (fertiger Pool)

| Pfad (Handy) | Inhalt | Anzahl |
|---|---|---|
| `DCIM/Storybilder` | kuratierte Story-Bilder + Shooting-Auswahl (`schöniaugeblick`-Serie) | **150** |
| `DCIM/Testimonials` | Testimonial-Screenshots | 13 |
| `DCIM/Vorher nachher` | Vorher/Nachher | 1 |

→ **Default-Quelle für `/story`.** Brand-Foto-Hierarchie beachten (aktuelles Foto > Shooting > Stock).

---

## 🎬 REEL-VIDEOS

| Pfad (Handy) | Inhalt | Anzahl | Status |
|---|---|---|---|
| `DCIM/Reel-Videos` | Talking-Head-Rohclips 09.06. (`VID_2026…_bsl`) + Bootcamp-Promo-Talking-Head | **12** | ✅ konsolidiert 15.06. (aus OneDrive kopiert) |
| `DCIM/Camera` (Videos) | gemischt privat + Business, **noch zu triagieren** | 130 | ⏳ Patricia markiert reel-taugliche |
| `DCIM/Screen recordings` | Screen-Recordings | 29 | ⏳ |

→ **Default-Quelle für `/reels`** = `DCIM/Reel-Videos`. OneDrive-Originale der 12 Clips bleiben vorerst als Backup in `OneDrive\` (löschen erst nach Patricias OK).

---

## 🗄️ ROH-ARCHIVE (zum Rausziehen, nicht kuratiert)

| Pfad | Inhalt | Anzahl |
|---|---|---|
| `DCIM/Shooting` (Handy) | komplettes Foto-Shooting-Archiv (roh) | 963 |
| `DCIM/Camera` (Handy) | Kamera-Rolle gemischt | 596 |
| `Pictures/Canva` (Handy) | Canva-Exporte (Bilder) | 316 |
| `context/Shootingbilder/` (Workspace) | Shooting-Auswahl im Repo (für Render-Pipelines) | — |
| `OneDrive\Instagram Content\` | Karussells / Reels / Storys (PC, teils leer) | — |
| `OneDrive\Bilder\Instagram_Videos\` | ältere IG-Videos nach Jahr | 8 |

---

## ⚠️ Canva-Reels-Ordner

Patricias Canva-Ordner mit gesammelten Reel-Videos lässt sich **nicht automatisch herunterladen** — die Canva-API exportiert nur fertige Designs, keine hochgeladenen Roh-Videos. Gefunden wurde nur der Ordner „Instagram Reels-Covers" (Cover-Bilder). → Reel-Videos aus Canva muss Patricia manuell exportieren, falls gebraucht. Die Reel-Rohclips liegen aber ohnehin schon unter `DCIM/Reel-Videos`.

---

## 📋 To-do / offen

- [ ] Patricia triagiert die 130 `Camera`-Videos → reel-taugliche nach `DCIM/Reel-Videos` verschieben
- [ ] Nach Bestätigung: OneDrive-Original-Clips löschen (Patricias „Verschieben")
- [ ] Story-Bilder bei Bedarf weiter ausdünnen (schon gepostete raus) — manuell durch Patricia

## 🔗 Verwandte Notizen

- [[feedback_foto-quellen-priorisierung]]
- [[feedback_hook-test-bekenntnis-gewinnt]]
