#!/usr/bin/env python3
"""Inject Reichweitenherz-Patterns into content skills."""
from pathlib import Path

BLOCK = '''
---

## 🎯 Reichweitenherz-Patterns (Pflicht seit 2026-06-09)

> Quelle: `memory/feedback_KRITISCH-reichweitenherz-patterns.md`
> Patricia explizit: "die Hooks gefallen mir VIEL besser als das was du mir vorgelegt hast."

### Hook-Pattern Pflicht-Layer

✅ **TUN — Reichweitenherz-Stil:**
- **Konkrete Antagonist-Figur** statt abstrakte Schmerz-Begriffe
  - „die Mamas auf dem Pausenplatz" / „die Schwiegermutter" / „die Ex-Kolleginnen aus dem Büro"
  - NICHT: „Mama im Network" allein (zu abstrakt)
- **POV-Format** als Reichweite-Variante
  - „POV: Wenn [konkrete Antagonist-Gruppe] meine Stories schauen:"
- **Multiple-Choice A/B/C/D** mit D als humorvolle Pointe (Emoji 🙄/🥱)
- **Zeit + Ort + Szene** („Sonntagabend 21 Uhr, du sitzt am Sofa") statt abstrakte Begriffe
- **Echte Wortwahl** („superbroke", „Sicherung durchbrennt") statt Coach-Sprache
- **Markt-Lüge namentlich** („Beauty-Influencerin redet ein..." / „perfekte Instagram-Mamas mit 5-Uhr-Me-Time")

❌ **NICHT mehr — zu abstrakt:**
- „Du musst nicht Experte sein..."
- „Es gibt 5 Dinge die..."
- „Lerne wie du..."
- Hook ohne konkrete Antagonist-Figur
- Abstrakte Schmerz-Begriffe ohne Szene

### Reichweitenherz 4-Schritte-Karussell-Formel

**Schritt 1: 5-Minuten-Realitäts-Scan** → konkrete Tageszeit + Ort + Szene (nicht „Mama Mental Load" als Begriff, sondern „Kind schreit am Bein, Waschmaschine piept, Brotdose packen")

**Schritt 2: Ungefilterter Sprachnachrichten-Sound** → echte Wortwahl, wie die Kundin ihrer besten Freundin erzählt (Schimpfwörter erlaubt)

**Schritt 3: 3-Phasen-Aufbruch** pro Beispiel:
- **Symptom** (was die Person konkret erlebt)
- **Markt-Lüge** (was Coaches/Gurus/Influencerinnen einreden)
- **Nackte Wahrheit** (deine ehrliche Diagnose + warum die Markt-Lüge Quatsch ist)

**Schritt 4: Brich den „Experten Look"** → Beste-Freundinnen-Kontrast (dunkler Filter, schlichte Schrift, unperfektes Real-Life) statt Hochglanz-Canva. „Das Auge der Kundin scannt in 0,3 Sek: ‚Coach der was verkaufen will → Scroll' oder ‚echte Freundin → Weiterlesen'."

### Anwendung

- **Karussells:** ein Karussell pro Monat nach 4-Schritte-Formel + 3 konkrete Beispiele aus Zielgruppen-Realität
- **Reels (Reichweite):** POV-Multiple-Choice + Lifestyle-B-Roll + Caption mit „Netflix-Serie"-Reframe
- **Captions:** 3-Phasen-Aufbruch (Symptom/Markt-Lüge/Nackte Wahrheit) als Caption-Struktur, auch ohne Karussell
- **Hooks:** vor JEDEM Hook-Brainstorm prüfen: gibt es eine konkrete Antagonist-Figur? Zeit + Ort + Szene? Markt-Lüge namentlich?
'''

skills = ['karussell.md', 'reels.md', 'montag.md', 'freitag-hooks.md']
base = Path('C:/Users/pnulm/Desktop/Mein Business/.claude/commands')

for skill in skills:
    p = base / skill
    if not p.exists():
        print(f'MISSING {skill}'); continue
    text = p.read_text(encoding='utf-8')
    if 'Reichweitenherz-Patterns' in text:
        print(f'SKIP {skill} (already has block)'); continue
    # Insert after the Master-Skill-Integration block (or after H1 if not present)
    marker = 'Stimme · Relevanz · Mehrwert · Klarheit'  # last line of master-block
    idx = text.find(marker)
    if idx != -1:
        # Find end of that line
        eol = text.find('\n', idx)
        new_text = text[:eol+1] + BLOCK + text[eol+1:]
    else:
        # Just after H1
        lines = text.split('\n', 1)
        new_text = lines[0] + '\n' + BLOCK + '\n' + (lines[1] if len(lines) > 1 else '')
    p.write_text(new_text, encoding='utf-8')
    print(f'OK {skill}')
