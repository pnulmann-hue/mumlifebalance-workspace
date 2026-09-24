---
tags: [produkt, ki, kurs]
---

# Die Foliensätze — alle zehn Module

**Stand:** 2026-09-23 · Gehört zu [[03-inhaltsverzeichnis]] und [[04-kursplattform-texte]]

Je Modul ein eigener Foliensatz, 1920×1080, in Patricias Marke
(Philosopher + Source Sans 3 · Petrol · Dunkelblau · Creme · Orange).
**Auf jeder Folie stehen Sprechnotizen** — was zu erzählen ist, was am
Bildschirm gezeigt wird und worauf zu achten ist.

| Modul | Folien | Lektionen | Link |
|---|---:|---:|---|
| 1 · Orientierung | 25 | 5 | https://claude.ai/artifact/LnABWRgZEU2Fhhm2FCzBH7 |
| 2 · Claude Chat | 31 | 7 | https://claude.ai/artifact/Sv1PQ8sHjL81UUt7mVjdQu |
| 3 · Claude Cowork | 22 | 5 | https://claude.ai/artifact/PkXYLdh86SBsKspgmfoJdV |
| 4 · Dein Arbeitsplatz | 29 | 7 | https://claude.ai/artifact/H2t9veSbsVwRvrBnwNRRC8 |
| 5 · Skills | 33 | 8 | https://claude.ai/artifact/9HBSNPBHNKe5tCiQxstF8U |
| 6 · Bots | 23 | 6 | https://claude.ai/artifact/1XTWypDWxRjnYaJcKRWYtG |
| 7 · Social Media | 36 | 8 | https://claude.ai/artifact/L8ZwiQpusSWVEwD2tab8bR |
| 8 · Produkte, Seiten, Mails | 21 | 5 | https://claude.ai/artifact/R42yY89PC29d4rpEsdSyL5 |
| 9 · Dein Cockpit | 22 | 5 | https://claude.ai/artifact/6m2o6CmrksWiRF8Bg2Woma |
| 10 · Sicherheit und das Ganze | 27 | 6 | https://claude.ai/artifact/36HjwKA4qvrppPn7pChu9T |
| **Summe** | **269** | **62** | |

Alle zehn sind **privat** — niemand sonst kann sie öffnen, solange sie nicht
über das Teilen-Menü der Seite freigegeben werden. Für die Aufnahme reicht das:
Folien in den Vollbild-Modus, Bildschirm aufnehmen, Sprechnotizen daneben.

## Wie sie gebaut sind

Nicht von Hand, sondern aus je einem Skript unter `scripts/ki-kurs/`:

```bash
python scripts/ki-kurs/folien-modul-5.py <ordner>
python scripts/ki-kurs/folien-pruefen.py <ordner>   # muss SAUBER melden
```

- `folien_basis.py` — die gemeinsamen Bausteine: Farben, Schriften, Kartenreihe,
  Gegenüberstellung, Lektionstitel, Aussage-Folie, Checkliste. Eine Änderung dort
  gilt für alle zehn Module.
- `folien-pruefen.py` — prüft **nur den sichtbaren Folientext** gegen die
  KI-Phrasen-Blackliste, dazu Dreier-Stakkato, Schriftgrössen unter 24 px und
  unbalancierte Anführungszeichen. Sprechnotizen bleiben aussen vor, die dürfen
  klingen, wie Patricia spricht.

🚨 **Das deutsche Schlusszeichen nie direkt tippen** — es rutscht als gerades
Zeichen durch und beendet dann die Python-Zeichenkette. Dafür gibt es `zit()`,
und ein Wächter meldet jede Folie mit ungleicher Zahl auf und zu.

🚨 **Auf den Folien stehen keine Aussagen und keine Metaphern von Patricia**
(Patricias Entscheid, 22.09.2026). Schaufenster, Bibliothek statt Katalog, der
Fisch in der Nische, Stadt-Land, das Sanitär-Beispiel und die Achterbahn gehören
in ihre anderen Kurse. Die Folie trägt die Struktur, die Stimme kommt beim
Sprechen dazu.

## 🔗 Verwandte Notizen

- [[02-kurs-konzept]]
- [[03-inhaltsverzeichnis]]
- [[04-kursplattform-texte]]
