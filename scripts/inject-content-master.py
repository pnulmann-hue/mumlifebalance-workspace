#!/usr/bin/env python3
"""Inject content-master integration block into 9 content skills."""
from pathlib import Path

BLOCK = '''
---

## 🔗 Master-Skill-Integration (content-master)

**`content-master`** (`.claude/skills/content-master/`) ist als allgemeiner Schreib-Master aktiv. Bei JEDEM Output gilt:

- **Konflikt-Regel:** Dieser Skill ist spezifischer für Patricia und gewinnt vor content-master.
- **Pflicht-Beitrag von content-master VOR Abgabe:**
  1. **Floskel-Scan** (content-master Teil 7): keine verbotenen Phrasen (Hier ist..., Faire Frage., easy peasy, Kein Tippfehler, Nicht weil X. Sondern weil Y. etc.)
  2. **Mensch-Check:** klingt der Output nach echtem Mensch oder nach KI-Schachtel?
  3. **4-Säulen-Check:** Stimme · Relevanz · Mehrwert · Klarheit — jede einzeln durchgegangen
- **Stimme-Quelle:** `.claude/skills/content-master/deine-marke.md` (zeigt auf `context/patricia-vollprofil.md` + `brand-voice.md` + `ki-phrasen-blackliste.md`)

**Für Werbeanzeigen separat:** `werbeanzeigentext-master` mit gleichem Konflikt-Mechanismus.
'''

skills_h1 = ['karussell.md', 'reels.md', 'story.md', 'montag.md', 'freitag-hooks.md', 'salespage.md', 'produkt.md']
skills_frontmatter = ['funnel.md', 'blog.md']

base = Path('C:/Users/pnulm/Desktop/Mein Business/.claude/commands')

for skill in skills_h1:
    p = base / skill
    if not p.exists():
        print(f'✗ {skill} not found'); continue
    text = p.read_text(encoding='utf-8')
    if 'Master-Skill-Integration' in text:
        print(f'⤫ {skill} already has block'); continue
    lines = text.split('\n', 1)
    new_text = lines[0] + '\n' + BLOCK + '\n' + lines[1]
    p.write_text(new_text, encoding='utf-8')
    print(f'✓ {skill}')

# For frontmatter skills, insert after closing ---
for skill in skills_frontmatter:
    p = base / skill
    if not p.exists():
        print(f'✗ {skill} not found'); continue
    text = p.read_text(encoding='utf-8')
    if 'Master-Skill-Integration' in text:
        print(f'⤫ {skill} already has block'); continue
    # Skip the frontmatter
    if text.startswith('---'):
        end = text.find('---', 3)
        if end != -1:
            after_fm = end + 3
            # Find first heading or just insert after frontmatter
            new_text = text[:after_fm] + '\n' + BLOCK + '\n' + text[after_fm:]
            p.write_text(new_text, encoding='utf-8')
            print(f'✓ {skill}')
        else:
            print(f'✗ {skill} bad frontmatter')
    else:
        # No frontmatter — insert at top
        new_text = BLOCK + '\n' + text
        p.write_text(new_text, encoding='utf-8')
        print(f'✓ {skill} (no frontmatter)')
