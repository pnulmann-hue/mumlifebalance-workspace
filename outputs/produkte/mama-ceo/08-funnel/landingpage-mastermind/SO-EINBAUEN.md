# Mama-CEO-Webinar Landingpage — Setup-Anleitung

## Was du brauchst (3 Files in einem Ordner)

```
mama-ceo-webinar/
├── index.html       ← die Page (siehe unten)
├── hero.jpg         ← Foto Nr. 22 (am Wasser, Kaffeetasse)
└── patricia.jpg     ← Foto Nr. 410 (im Schilf, Lederjacke)
```

---

## Schritt-für-Schritt für Mac

### 1. Neuen Ordner machen
- Auf dem Schreibtisch: Rechtsklick → **„Neuer Ordner"**
- Name: `mama-ceo-webinar`

### 2. Die zwei Fotos rein
- Foto Nr. 22 → in den Ordner kopieren → **umbenennen zu `hero.jpg`**
- Foto Nr. 410 → in den Ordner kopieren → **umbenennen zu `patricia.jpg`**
- Wichtig: Genau diese Namen, klein geschrieben, mit `.jpg` am Ende

(Beim Umbenennen: Klick auf Datei → **Enter-Taste** → neuen Namen tippen → Enter)

### 3. Die index.html anlegen
- Im Ordner `mama-ceo-webinar`: Rechtsklick → **„Neues Dokument"** wenn vorhanden, oder via TextEdit:
  - **TextEdit öffnen** (Spotlight: Cmd+Space → „TextEdit" → Enter)
  - **Format → In reinen Text umwandeln** (Cmd+Shift+T)
  - Code aus dem Chat kopieren (Copy-Button am Code-Block) und einfügen
  - **Cmd+S** speichern als `index.html` IM Ordner `mama-ceo-webinar`
  - Falls Dialog kommt „.txt verwenden?" → **„.html verwenden"** klicken

### 4. Anschauen
- Im Ordner `mama-ceo-webinar`: **Doppelklick auf `index.html`**
- Browser öffnet sich → **Page erscheint mit deinen Fotos** ✨

### 5. Live ins Web (optional)
- Geh auf **app.netlify.com/drop**
- Den ganzen Ordner `mama-ceo-webinar` per Drag&Drop ins Fenster ziehen
- Netlify gibt dir sofort eine Live-URL — die kannst du teilen

---

## Wenn Foto-Namen anders sind

Falls du die Fotos NICHT zu `hero.jpg` / `patricia.jpg` umbenennen kannst (z.B. weil sie schon die Namen `IMG-22.jpg` und `IMG-410.jpg` haben):

In der `index.html` nach diesen zwei Stellen suchen:
```css
url('hero.jpg') center/cover no-repeat,
```
und
```css
url('patricia.jpg') center/cover no-repeat,
```

Ersetzen mit deinen tatsächlichen Datei-Namen.

---

## Fehlerbehebung

❌ **Browser zeigt nur die Hintergrundfarbe, kein Foto:**
→ Foto liegt nicht im selben Ordner wie `index.html` ODER hat anderen Namen. Datei-Namen prüfen.

❌ **Browser zeigt nur Code statt Page:**
→ Datei wurde als `.txt` statt `.html` gespeichert. Im Finder umbenennen: Klick auf Datei → Enter → `.txt` zu `.html` ändern → bestätigen.

❌ **Foto ist verzerrt / falsch geschnitten:**
→ Foto hat ungewöhnliches Seitenverhältnis. CSS macht automatisch `cover` (vollständig füllen) — der Hauptgegenstand sollte mittig im Foto sein.
