"""Kopierseite für die Tool-Workshop-Mails: je Mail Betreff, Vorschautext, HTML-Code mit Kopier-Knopf und Vorschau.

    python scripts/tool-workshop/mails-bauen.py          # zuerst, baut die Mails
    python scripts/tool-workshop/kopierseite-bauen.py
-> outputs/produkte/tool-workshop/mails/kopierseite.html (per Doppelklick öffnen)

Die Seite trägt Zoom-Passwort und Gruppenlink in sich und ist deshalb gitignored
(outputs/produkte/tool-workshop/mails/*.html). Der HTML-Knopf legt den Code als reinen Text ab,
für das Feld „Eigenen Code einfügen“ in ActiveCampaign.
"""
import html
import importlib.util
import json
import pathlib
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("mb", ROOT / "scripts/tool-workshop/mails-bauen.py")
mb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mb)
ZIEL = ROOT / "outputs/produkte/tool-workshop/mails"

# Nach Automationen sortiert (Patricia 29.10.): B1–B3 hängen mit Warte-Schritten an der Workshop-Automation,
# so braucht es keine Kampagnen mit Tag-Segment.
GRUPPEN = [
    ("Automation 1 · Tool-Workshop", "Auslöser: Tag <b>Tool-Workshop</b> wird hinzugefügt. Einmal ausführen.", [
        ("B0", "Schritt 1 · sofort: E-Mail senden"),
        ("B1", "Schritt 2 · Warten bis Mo 9.11.2026, 18:00 · dann E-Mail senden"),
        ("B2", "Schritt 3 · Warten bis Mi 11.11.2026, 08:00 · dann E-Mail senden"),
        ("B3", "Schritt 4 · Warten bis Sa 14.11.2026, 09:00 · dann E-Mail senden (Start Produktwelt-Serie)"),
        ("B4", "Schritt 5 · Warten bis Mo 16.11.2026, 09:00 · dann E-Mail senden"),
        ("B5", "Schritt 6 · Warten bis Mi 18.11.2026, 09:00 · dann E-Mail senden"),
        ("B6", "Schritt 7 · Warten bis Fr 20.11.2026, 09:00 · dann E-Mail senden"),
        ("B7", "Schritt 8 · Warten bis So 22.11.2026, 18:00 · dann E-Mail senden · Ende"),
    ]),
    ("Automation 2 · Nischengenerator", "Auslöser: Tag <b>0€ Nischengenerator</b> wird hinzugefügt. Einmal ausführen. "
     "Als Ziel: Tag <b>Tool-Workshop</b> vorhanden → Automation beenden (wer gekauft hat, bekommt keine Werbung mehr).", [
        ("C0", "Schritt 1 · sofort: E-Mail senden"),
        ("C1", "Schritt 2 · 1 Tag warten · dann E-Mail senden"),
        ("C2", "Schritt 3 · 2 Tage warten · dann E-Mail senden"),
        ("C3", "Schritt 4 · 2 Tage warten · dann E-Mail senden"),
        ("C4", "Schritt 5 · 2 Tage warten · dann E-Mail senden · Ende"),
    ]),
    ("Keine Automation · Launch-Mails an deine Liste", "Diese drei verschickst du als normale Kampagne an die Liste (Entwürfe liegen unter Kampagnen). "
     "A3 ist auch die Letzter-Tag-Mail für alle aus dem Nischengenerator.", [
        ("A1", "Fr 30.10. · Anmeldung offen"), ("A2", "Fr 6.11. · nicht technisch"), ("A3", "Mo 9.11. · letzter Tag"),
    ]),
]

karten = []
for gname, gsatz, schritte in GRUPPEN:
  karten.append(f'<h2 class="gruppe">{gname}</h2><p class="gsatz">{gsatz}</p>')
  for kurz, wie in schritte:
      m = next(x for x in mb.MAILS if x["datei"].startswith(kurz))
      code = (ZIEL / m["datei"]).read_text(encoding="utf-8")
      e = lambda s: html.escape(s, quote=True)
      karten.append(f"""
  <section class="karte">
    <p class="kurz">{kurz}</p>
    <h2>{html.escape(m["name"], quote=False)}</h2>
    <p class="wie">{wie}</p>
    <div class="feld"><b>Betreff</b><span>{html.escape(m["betreff"], quote=False)}</span><button data-text="{e(m["betreff"])}">kopieren</button></div>
    <div class="feld"><b>Vorschautext</b><span>{html.escape(m["preheader"], quote=False)}</span><button data-text="{e(m["preheader"])}">kopieren</button></div>
    <div class="feld"><b>HTML-Code</b><span>für „Eigenen Code einfügen“</span><button class="stark" data-text="{e(code)}">HTML kopieren</button></div>
    <details><summary>Vorschau</summary><iframe srcdoc="{e(code)}" loading="lazy"></iframe></details>
  </section>""")

seite = """<!doctype html><html lang="de"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Tool-Workshop · Mails kopieren</title>
<style>
:root{--petrol:#12828c;--blau:#29556d;--nacht:#0c1c30;--creme:#f1ecdd;--orange:#dc822e;--linie:#e2dccb}
*{box-sizing:border-box}body{margin:0;background:var(--creme);color:var(--nacht);font:16px/1.5 'Segoe UI',Arial,sans-serif;padding:24px 16px}
main{max-width:860px;margin:0 auto}h1{font-family:Georgia,serif;color:var(--blau);margin:0 0 6px}
.lead{margin:0 0 24px;color:#4f5d68}
.karte{background:#fff;border:1px solid var(--linie);border-radius:16px;padding:20px;margin:0 0 18px}
.kurz{display:inline-block;margin:0 0 6px;background:var(--orange);color:#fff;font-weight:700;border-radius:999px;padding:2px 12px;font-size:13px}
.gruppe{font-family:Georgia,serif;color:var(--blau);font-size:26px;margin:34px 0 4px}.gsatz{margin:0 0 14px}
h2{font-size:20px;margin:0 0 4px}.wie{margin:0 0 14px;color:var(--petrol);font-weight:600}
.feld{display:flex;gap:12px;align-items:center;border-top:1px solid var(--linie);padding:10px 0;flex-wrap:wrap}
.feld b{width:120px;flex:none}.feld span{flex:1;min-width:180px}
button{border:1px solid var(--blau);background:#fff;color:var(--blau);border-radius:999px;padding:7px 16px;font-weight:600;cursor:pointer}
button.stark{background:var(--blau);color:#fff}button.ok{background:var(--petrol);border-color:var(--petrol);color:#fff}
details{margin-top:10px}summary{cursor:pointer;color:var(--blau);font-weight:600}
.handfeld{width:100%;height:140px;margin:6px 0 10px;border:2px solid var(--orange);border-radius:10px;padding:10px;font:13px/1.4 Consolas,monospace}
iframe{width:100%;height:640px;border:1px solid var(--linie);border-radius:10px;margin-top:10px;background:#fff}
</style></head><body><main>
<h1>Tool-Workshop · Mails kopieren</h1>
<p class="lead">Sortiert nach Automation, in der Reihenfolge der Schritte. „HTML kopieren“ legt den Code für das Feld „Eigenen Code einfügen“ in ActiveCampaign ab. 🔒 Diese Seite enthält Zoom- und Gruppenlink: nicht weitergeben.</p>
KARTEN
</main><script>
document.querySelectorAll("button[data-text]").forEach(b => b.addEventListener("click", async () => {
  const alt = b.textContent;
  // Eine als Datei geöffnete Seite darf je nach Browser nicht über navigator.clipboard schreiben:
  // dann über ein verstecktes Textfeld und execCommand, das geht dort immer.
  let ok = false;
  try { await navigator.clipboard.writeText(b.dataset.text); ok = true; } catch (e) {}
  if (!ok) {
    const f = document.createElement("textarea");
    f.value = b.dataset.text; f.setAttribute("readonly", ""); f.style.position = "fixed"; f.style.opacity = "0";
    document.body.appendChild(f); f.select(); f.setSelectionRange(0, f.value.length);
    try { ok = document.execCommand("copy"); } catch (e) {}
    f.remove();
  }
  if (ok) { b.textContent = "kopiert ✓"; b.classList.add("ok"); }
  else {
    // Letzter Weg: sichtbares Feld, schon markiert, Strg+C (am Mac Cmd+C) genügt.
    let f = b.parentElement.nextElementSibling;
    if (!f || !f.classList.contains("handfeld")) {
      f = document.createElement("textarea"); f.className = "handfeld"; f.readOnly = true;
      b.parentElement.after(f);
    }
    f.value = b.dataset.text; f.focus(); f.select();
    b.textContent = "markiert: Strg+C drücken";
  }
  setTimeout(() => { b.textContent = alt; b.classList.remove("ok"); }, ok ? 1800 : 6000);
}));
</script></body></html>""".replace("KARTEN", "\n".join(karten))

ziel = ZIEL / "kopierseite.html"
ziel.write_text(seite, encoding="utf-8")
print("->", ziel)
