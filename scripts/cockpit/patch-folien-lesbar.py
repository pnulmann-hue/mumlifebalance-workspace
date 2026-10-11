"""
Kleingedrucktes auf den Karussell-Folien lesbar machen.

Patricia, 28.09.2026: „ich kann das kleingeschriebene unter dem hook nicht lesen.
das hat mal dazu geführt, dass ich das karussell löschen musste, weil da irgendwie
stand: hier kannst du bei bedarf xy einfügen“.

Die Unterzeile auf der Titelfolie war 30 px in halbdurchsichtiger Farbe, der Text
auf der Schlussfolie ebenfalls halbdurchsichtig — am Handy nicht lesbar, und genau
dort steht auf der Schlussfolie das Kommentar-Stichwort. Dazu lief eine lange
Unterzeile in die Seitenzahl hinein.

Jetzt: Titelfolie 40 px in voller Textfarbe, höchstens drei Zeilen und nie tiefer
als die Fusszeile · Schlussfolie in voller Textfarbe.

  python scripts/cockpit/patch-folien-lesbar.py <cockpit.html> [<weitere.html> …]
Wiederholbar: bereits gepatchte Dateien werden erkannt und übersprungen.
"""
import sys
from pathlib import Path

ALT_HOOK = '''        if (slide.body) {
          ctx.fillStyle = b.muted;
          ctx.font = "30px " + b.body;
          var bl = wrap(ctx, slide.body, maxW);
          bl.slice(0, 4).forEach(function (ln, i) {
            ctx.fillText(ln, isZitat ? pad : pad, y + totalH + 78 + i * 42);
          });
        }'''
NEU_HOOK = '''        if (slide.body) {
          ctx.fillStyle = b.text; /* lesbar: volle Farbe, 40 px (28.09.2026) */
          ctx.font = "40px " + b.body;
          var bl = wrap(ctx, slide.body, maxW);
          var bTop = y + totalH + 92, bMax = Math.max(0, Math.floor((H - pad - 70 - bTop) / 54));
          bl.slice(0, Math.min(3, bMax)).forEach(function (ln, i) {
            ctx.fillText(ln, isZitat ? pad : pad, bTop + i * 54);
          });
        }'''
ALT_CTA = '''        ctx.font = bc.size + "px " + b.body;
        ctx.fillStyle = b.muted;
        bc.lines.forEach(function (ln, i) { ctx.fillText(ln, pad, cy + bc.size + i * bc.size * 1.42); });'''
NEU_CTA = '''        ctx.font = bc.size + "px " + b.body;
        ctx.fillStyle = b.text; /* lesbar: volle Farbe (28.09.2026) */
        bc.lines.forEach(function (ln, i) { ctx.fillText(ln, pad, cy + bc.size + i * bc.size * 1.42); });'''

for pfad in sys.argv[1:]:
    p = Path(pfad)
    t = p.read_text(encoding="utf-8")
    if "lesbar: volle Farbe, 40 px" in t:
        print(f"schon gepatcht: {p}")
        continue
    assert t.count(ALT_HOOK) == 1, f"Titelfolien-Stelle nicht eindeutig in {p}"
    assert t.count(ALT_CTA) == 1, f"Schlussfolien-Stelle nicht eindeutig in {p}"
    t = t.replace(ALT_HOOK, NEU_HOOK).replace(ALT_CTA, NEU_CTA)
    assert t.count("lesbar: volle Farbe") == 2
    p.write_text(t, encoding="utf-8")
    print(f"gepatcht: {p}")
