---
tags: [content, reels, videoschnitt]
---

# Sprechreels — Dreh-Anleitung (für Talking-Head im Kelsie-Stil)

> Für den vollautomatischen Reel-Weg: Du sprichst, wirfst die Clips ins Handy-Album
> **`DCIM/Sprechreels`**, Claude holt + schneidet + animiert automatisch.
> Abholung: `python scripts/handy/hol-content.py --album Sprechreels --ziel-video video/sprechreels`
> Danach: `/videoschnitt` auf die Clips in `video/sprechreels/`.

## Zwei Aufnahme-Arten
1. **Wissens-Dump (Hauptquelle):** 10–20 Min frei über deine Strategie/dein Wissen sprechen — unstrukturiert, mit Versprechern erlaubt. Claude fischt die stärksten Nuggets raus und macht daraus **viele** Reels. Einmal filmen = Wochen an Content.
2. **Geplante Sprechreels:** Zu einem konkreten Wochen-Angle liest du einen von Claude vorgelegten Sprechtext ab.

## Kameraposition & Bildausschnitt (fürs Kelsie-Layout)
Beim Kelsie-Stil steht ein **grosses Wort neben/hinter dir** und **Untertitel unten**. Dafür braucht das Bild Platz:

- **Abstand: halbnah, nicht Nahaufnahme.** Brust/Hüfte aufwärts im Bild — **kein enges Gesicht-Close-up** (sonst überdeckt das grosse Wort dein Gesicht; das hatten wir als Problem).
- **Kamera auf Augenhöhe**, Handy **hochkant (9:16)**, ~**1,5–2 m** Abstand (dein Mikro trägt den Ton auch von weiter weg).
- **Platz freilassen:** unteres Drittel bleibt frei (Untertitel), und **eine Seite / der Raum um deinen Kopf** frei (dort erscheint abwechselnd links/rechts das grosse Wort). Stell dich also **leicht aus der Mitte** oder lass genug Rand.
- **Kopffreiheit** oben lassen, nicht anschneiden.
- Licht **von vorne** (nicht im Rücken), Mikro nah.

## In die Kamera schauen — ja oder nein?
- **Sprechreel (Talking-Head): JA, direkt in die Linse.** Direkte Ansprache schafft Nähe und verkauft. Tipp: kleinen Punkt/Sticker neben die Linse kleben, dorthin sprechen wie zu einer Freundin — nicht auf dein eigenes Vorschaubild schauen.
- **B-Roll (stumme Alltagsclips): NEIN.** Da machst du die Sache, die Kamera schaut nur zu. (Diese Regel gilt **nur** für B-Roll, nicht für Sprechreels.)

## Abwechslung — woher sie kommt
Du musst **nicht** ständig die Position wechseln. Die Dynamik macht **der Schnitt**: Auto-Zoom (mal rein, mal harter Sprung), eingeschobene Bilder, B-Roll-Cutaways, wechselnde Texteinblendungen.
Wenn du trotzdem optische Abwechslung im Feed willst, dreh pro Session **2–3 Setups**:
- **A:** frontal, halbnah (Standard).
- **B:** leicht seitlich (~30–45°).
- **C:** ein Setup weiter weg / anderer Raum-Eck / anderes Oberteil.
Jedes Setup = ein Schwung Reels, die im Feed unterschiedlich aussehen.

## Damit der Schnitt sauber wird
- Vor jedem Gedanken **1–2 Sek Pause** (hilft beim Schneiden, 250-ms-Regel).
- Versprecher? **Kurz stoppen, ganzen Satz neu** — Claude erkennt den letzten vollständigen Take und nimmt den.
- **Ein Gedanke pro „Häppchen".** Sag deine Kernaussagen als saubere, für sich stehende Sätze — daraus werden die Hooks.
- Ruhig mehrere Themen hintereinander — Claude trennt sie beim Schneiden.

## 🔗 Verwandte Notizen
- [[videoschnitt-regeln]] · [[project_videoschnitt-pipeline]] · [[project_content-maschine-vollauto]]
