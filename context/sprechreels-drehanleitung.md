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

## Deine Szenen — was dein eigenes Material hergibt

Aus 221 Vorschaubildern deiner Clips (Stand 20.09.2026). **Keine erfundenen Orte** —
das sind Ecken, an denen du schon gefilmt hast.

| | Ort | Woran du ihn erkennst | Taugt fürs Kelsie-Layout? |
|---|---|---|---|
| **A** | Grau-grüne Wand, Zimmerpflanze links, sitzend | dein jetziges Standard-Setup, rosa Shirt | ⚠️ **so wie bisher nicht** — zu nah und zu mittig |
| **B** | Weisse glatte Wand, stehend | heller Pulli, ganze Figur | ✅ viel Platz · ⚠️ helles Oberteil auf weiss = Freistellen schwierig |
| **C** | Weisse Rauputzwand, sitzend | | ✅ |
| **D** | Schreibtisch an heller Holzwand, Bildschirm | | ✅ wenn du seitlich sitzt |
| **E** | Esstisch mit Blick in die Küche, Holzdecke, Hängelampen | Laptop, Tiefe im Raum | ✅✅ **das beste Bild** — wirkt nicht gestellt |
| **F** | Küche, dunkelgrüne Fronten, Granitfläche | | ✅ dunkler Hintergrund, Kontrast stimmt |
| **G** | Terrasse an der Holzwand, Sonne | | ✅ · Gegenlicht prüfen |
| **H** | Garten / Wiese mit Hügelblick | Appenzellerland | ✅ Wiedererkennung · ⚠️ Wind auf dem Mikro |
| **I** | Trainingsraum, Holzdecke, Hanteln | | ⚠️ nur wenn das Thema Energie ist |
| **J** | Berg, Wanderung | | ⚠️ Ton im Wind, nur kurze Sätze |

### 🚨 Was an Setup A nicht stimmt

Auf deinen bisherigen Sprechclips sitzt du **mittig und nah** — Brustbild, Kopf fast in
der Bildmitte. Beim Kelsie-Layout steht das grosse Wort **hinter dir**, links oder
rechts abwechselnd. Wenn du mittig und gross im Bild bist, gibt es diesen Platz nicht,
und das Wort landet auf dir. Das ist derselbe Fehler wie bei den B-Rolls, nur eine
Stufe früher: **im Bild, nicht im Schnitt.**

Zwei Handgriffe lösen es, den Ort musst du nicht wechseln:
1. **Kamera einen guten Meter weiter weg** — Hüfte aufwärts statt Brust aufwärts.
2. **Setz dich aus der Mitte**, ein Drittel nach links oder rechts. Die freie Seite ist
   die Bühne für das Wort.

### 🚨 Freistellen braucht Kontrast

Das grosse Wort liegt hinter dir, dafür wird deine Silhouette ausgeschnitten
(`npx hyperframes remove-background`). Das misslingt, wenn Person und Hintergrund
dieselbe Helligkeit oder Farbe haben — dann franst die Kante aus oder es fehlt ein
Stück Haar.

| geht gut | wird heikel |
|---|---|
| rosa/lachs Shirt auf grau-grüner Wand | beiger Pulli auf weisser Wand |
| dunkles Top auf heller Holzwand | braune Haare vor dunkler Holzwand |
| helles Oberteil in der dunklen Küche | gemustertes Oberteil vor unruhigem Hintergrund |

**Faustregel: eine Stufe Unterschied zwischen dir und der Wand.** Wenn die Wand hell
ist, zieh etwas Dunkles an — und umgekehrt.

### Eine Dreh-Session, drei Szenen

Nicht mehr. Drei reichen für einen Feed, der nicht gleich aussieht, und sind an einem
Nachmittag zu schaffen:

- **Szene 1 — E (Esstisch):** der Wissens-Dump, 10–20 Minuten frei sprechen. Das ist
  die Hauptquelle, daraus werden die meisten Reels.
- **Szene 2 — A oder C (Wand, sitzend), anderes Oberteil:** die geplanten Sprechtexte.
- **Szene 3 — F oder G (Küche oder Terrasse), im Stehen:** die kurzen Sachen, ein
  Gedanke pro Clip.

Zwischen den Szenen **Oberteil wechseln** — im Feed sieht man dann drei verschiedene
Tage, obwohl es einer war.

## Damit der Schnitt sauber wird
- Vor jedem Gedanken **1–2 Sek Pause** (hilft beim Schneiden, 250-ms-Regel).
- Versprecher? **Kurz stoppen, ganzen Satz neu** — Claude erkennt den letzten vollständigen Take und nimmt den.
- **Ein Gedanke pro „Häppchen".** Sag deine Kernaussagen als saubere, für sich stehende Sätze — daraus werden die Hooks.
- Ruhig mehrere Themen hintereinander — Claude trennt sie beim Schneiden.

## 🔗 Verwandte Notizen
- [[videoschnitt-regeln]] · [[project_videoschnitt-pipeline]] · [[project_content-maschine-vollauto]]
