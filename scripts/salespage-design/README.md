# Salespage-Design-Bundle — Einrichtung

Vier fertige Verkaufsseiten-Designs als Claude-Skills, umgeschrieben auf Patricias Marke.

| Skill | Look | Wofür |
|---|---|---|
| `minikurs-salespage` | hell + verspielt · Petrol-Flächen, Orange-Knopf | Minikurse 19–39, Freebies, Vorlagen |
| `signature-kurs-salespage` | hell + editorial · Creme + viel Foto, Petrol-Anker | Flaggschiff-Kurse ab 97, mit Ratenzahlung |
| `skill-salespage` | dunkel + technisch · Dunkelblau, Petrol leuchtet | Bots, Tools, Vorlagen-Pakete |
| `ki-salespage` | dunkel + laut · Dunkelblau, Orange leuchtet | KI-Produkte, Assistentinnen |

Aufruf im Chat: „Bau mir eine Verkaufsseite für [Produkt] im Signature-Design."
Ergebnis ist eine fertige `index.html`, die überall gehostet werden kann.

---

## Verhältnis zu `/copywriting`

Die beiden überschneiden sich nicht:

- **`/copywriting`** liefert die **Texte** (seit 02.10.2026, löst `/salespage` ab) —
  für ThriveCart wie für eine eigene Seite.
- **Diese vier Skills** liefern eine **komplette gestaltete Seite** als HTML — für
  Landingpages auf WordPress oder wo sonst gehostet wird.

Sinnvolle Reihenfolge bei einem neuen Produkt: erst `/copywriting` für die Texte, dann
das passende Design-Skill für die Seite.

---

## Wo was liegt

```
.claude/skills/<design>/
├── SKILL.md                        Bauplan (mit Patricia-Vorrang-Block oben)
├── BRAND-CONFIG.md                 Farben, Schriften, Links — Patricias Werte
├── BRAND-VOICE.md                  Wegweiser auf context/ (kein Formular)
├── ZIELGRUPPE.md                   Wegweiser auf context/ (kein Formular)
└── references/
    ├── reference-page.html         die komplette Design-Vorlage
    ├── section-guide.md            Abschnitts-Katalog
    └── assets/                     hier die eigenen Bilder ablegen
```

**Alle vier Ordner sind gitignored** — genauso wie
`reference/salespage-designs-original/`. Das Paket ist gekauftes Fremdmaterial und
das Repo ist öffentlich. Die beiden Skripte hier bleiben versioniert, damit sich der
Zustand wiederherstellen lässt.

---

## Neu aufsetzen (z.B. auf einem anderen Rechner)

1. `Salespage-Design-Bundle.zip` entpacken nach `reference/salespage-designs-original/`
2. Die beiden Skripte laufen lassen:

```bash
python scripts/salespage-design/marke-anpassen.py && python scripts/salespage-design/regeln-anpassen.py
```

3. Sicht-Prüfung:

```bash
node scripts/salespage-design/vorschau-rendern.mjs
```

Beide Skripte lesen **immer** aus dem Original-Ordner und schreiben nach
`.claude/skills/`. Mehrfaches Laufen schadet nicht.

---

## Was die Skripte tun

### `marke-anpassen.py` — das Aussehen

Färbt `reference-page.html` um: Rosé/Gold/Pink/Neon raus, Petrol/Dunkelblau/Creme/Orange
rein. Tauscht die sieben Fremdschriften gegen Philosopher + Source Sans 3.

Zwei Dinge, die dabei absichtlich so sind:

- **`Space Mono` bleibt** im Skill-Design. Der Terminal-Block im Hero zerfällt ohne
  Festbreiten-Schrift — das ist eine Funktion, keine Marken-Schrift.
- **Zwei Knopf-Verläufe wurden gegenüber der Vorlage abgedunkelt bzw. auf dunkle
  Schrift gedreht.** Weisse Schrift auf hellem Petrol oder auf Orange trägt zu wenig
  Kontrast. Nicht zurückdrehen.

⚠️ **Fallstrick beim Erweitern:** In den Vorlagen stehen HTML-Entities wie `&#128293;`
(🔥) und `&#215;` (×). Die sehen aus wie Farbwerte. Deshalb ersetzt das Skript
ausschliesslich, was in seinen Zuordnungs-Tabellen namentlich steht — nie per Muster
über alle `#`-Werte — und prüft nach jedem Lauf, ob eine Entity beschädigt wurde.

### `regeln-anpassen.py` — der Inhalt

Schreibt `SKILL.md` und `references/section-guide.md` auf Patricias Regeln um und setzt
oben in jede `SKILL.md` einen **Vorrang-Block**, der bei jedem Widerspruch gewinnt.

Vier Regeln aus der Vorlage werden gedreht:

| Vorlage sagt | Hier gilt |
|---|---|
| „Kunden statt Kundinnen", generisches Maskulinum | **Kundinnen** — ihre Leute sind Mamas |
| fehlende Zahlen mit plausiblen Beispielen füllen | **nichts erfinden**, lieber eine Kachel weniger |
| Garantie/Widerruf optional einbaubar | **keine Geld-zurück-Garantie** auf digitale Produkte |
| deutsches ß | **Schweizer ss**, echte Umlaute |

### `vorschau-rendern.mjs` — die Sicht-Prüfung

Rendert je Design acht Bilder nach `outputs/salespage-designs/vorschau/`
(gitignored). Schaltet vorher die Einblend-Animationen scharf, sonst bleiben
Abschnitte im Bild leer, die in Wirklichkeit gefüllt sind.

Puppeteer kommt aus `scripts/karussell-render/node_modules` — keine zweite
Installation nötig.

---

## Was noch fehlt

- **Impressum, Datenschutz, AGB** stehen in keiner `BRAND-CONFIG.md`, weil sie auch
  in `context/link-uebersicht.md` fehlen. Vor dem ersten Livegang nachtragen — dort
  und hier.
- **Bilder.** Die `references/assets/` sind leer, deshalb zeigen die Vorschau-Bilder
  an manchen Stellen leere Rahmen. Sobald echte Fotos drin liegen, sieht die Seite
  vollständig aus.
