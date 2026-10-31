---
tags: [produkt, salespage, jahresplanung]
---

# 02 · Anmeldeseite · Neustart 2027

**Gebaut**, nicht nur getextet: `python scripts/salespage-design/jahresplanung-bauen.py`
→ `outputs/salespages/jahresplanung/index.html` (lokal `preview_start jahresplanung-lp`, Port 4419).
Inhalt: `scripts/salespage-design/jahresplanung-body.html` — **dort** wird der Text geändert, nicht hier.

## Aufbau (Landingpage für ein Gratis-Angebot)

| Block | Inhalt |
|---|---|
| Hero | Kalenderblatt 31.12.2026 blättert auf 1.1.2027 · Kicker „Gratis-Workshop live · Donnerstag, 17. Dezember, 09:00 Uhr“ · H1 „Starte 2027 mit einem Plan, der um deine Familie herum gebaut ist“ · Knopf „Ich plane mit · gratis“ · Mockup |
| Wo es hakt | vier Sätze aus dem Schmerz im Bauplan |
| Ablauf | die sechs Schritte des Jahresplaners |
| Was du mitnimmst | Monatsübersicht · Umsatz-Check · Lücken-Check · Januar · Jahresplaner · Aufzeichnung |
| Warum mit mir | ✏️ **Patricia bestätigt:** „Bei mir kommen zuerst die Schulferien in den Kalender, dann die Geburtstage, dann meine Zeit.“ (abgeleitet aus dem Aufbau ihres Jahresplaners, nicht aus einem Zitat) · Workshop = offener MBA-Call |
| Für wen | vier Haken plus „nichts für dich, wenn du einen fertigen Plan erwartest“ |
| Anmelden | AC-Formular „0€ Jahresplanung“ (Platzhalter, bis die ID in `FORMULAR` steht) |
| FAQ | Kosten · nur Network · was brauche ich · nicht live · zeigen müssen |
| Schluss | zweite Funken-Fläche, „Dein Neustart beginnt mit einem Blatt Papier“ |

## Effekt

`jahresplanung-effekt.css`, reines CSS, weil WordPress Skripte blockt:
- **Kalenderblatt:** 31. Dezember 2026 (grau) klappt nach 1,4 s nach oben weg, darunter der 1. Januar 2027 (orange), der danach leise leuchtet
- **Funken:** zwölf Lichtpunkte steigen im Hero und im Schluss langsam auf und funkeln
- Bei „weniger Bewegung“ im Gerät: kein Blättern, keine Funken, nur das Endbild

Übernommen vom Vorbild ist nur die Idee (ein saisonaler Effekt im Hero, schwebendes Mockup). Wortlaut, Aufbau der
Texte und Gestaltung sind eigen.

## Mockup

`node scripts/salespage-design/jahresplanung-bild.mjs` → `outputs/salespages/jahresplanung/bild/hero.png`
(Laptop: Sandras Jahr 2027 · Tablet: Was schon feststeht · Tablet: Dein Januar · Handy: Kalenderblatt 1. Januar ·
Aufkleber „Live am 17. Dezember“, „2027 auf einem Blatt“, „gratis“). Für WP als webp hochladen, Adresse in `BILD_WP`.
