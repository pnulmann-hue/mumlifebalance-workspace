---
tags: [videoschnitt]
---

# video/ — der Ordner, in dem geschnitten wird

Hier liegt alles zum Videoschnitt-Workflow (`/videoschnitt`).

```
video/
├── input/        ← dein Rohmaterial rein (einmal durchgesprochen, mit Versprechern)
├── transkripte/  ← Transkript + Schnittlisten, pro Video ein Unterordner
└── output/       ← Rohschnitt, Einzelclips für CapCut, Textebene
```

## Wichtig: nichts davon geht ins Git

Das Repo ist **public**. `video/**` ist komplett gitignored — Rohvideos,
Transkripte und Schnitte bleiben auf deinem Rechner. Nur diese README ist drin.

## Der kürzeste Weg

1. Video in `video/input/` legen
2. Im Chat: `/videoschnitt`
3. Ich transkribiere, lege dir die Schnittliste vor, du sagst „passt"
4. In `video/output/<datum-slug>/` liegen dann `rohschnitt.mp4`, `clips/` und `untertitel.srt`
5. Alle Dateien aus `clips/` markieren und in CapCut ziehen — Feinschliff, fertig

Deine Regeln stehen in [`context/videoschnitt-regeln.md`](../context/videoschnitt-regeln.md).
Wenn ein Schnitt etwas falsch macht, wird **die Datei** geändert, nicht der nächste Chat.

## Zwischenstände

Jeder Lauf schreibt einen eigenen Ordner mit Datum. Nichts wird überschrieben.
Es kommt der Moment, in dem die dritte Fassung schlechter ist als die zweite —
dann kannst du zurück.

Alte Ordner räumst du selbst weg, wenn du sie nicht mehr brauchst.
Videos sind gross, der Ordner wächst.
