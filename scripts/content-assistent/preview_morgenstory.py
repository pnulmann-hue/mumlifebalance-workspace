"""Preview-Helfer: generiert + rendert die heutige Story LOKAL (ohne Telegram).

Zeigt wie die Morgenstory aussehen würde — für ein oder beide Profile.
Nutzt exakt dieselbe Pipeline wie der Bot (Launch-Engine + Monatsplan-MD + Claude + Render),
nur ohne Versand. Outputs landen in outputs/stories/preview-<datum>-<profil>/.

Nutzung:
    python preview_morgenstory.py                 # beide Profile (mentoring + doterra)
    python preview_morgenstory.py mentoring       # nur mentoring
    python preview_morgenstory.py doterra 2026-06-29   # doterra, simuliertes Datum
"""
from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import config
import notion_reader
import claude_caller
import render_caller
import launch_engine
import monatsplan_reader


def preview(profil: str, heute: date) -> dict:
    print(f"\n{'='*60}\n  PREVIEW: {profil}  ·  {heute.isoformat()} ({['Mo','Di','Mi','Do','Fr','Sa','So'][heute.weekday()]})\n{'='*60}")

    # Kontext bauen (Notion best-effort + Launch + Monatsplan-MD)
    try:
        kontext = notion_reader.lade_wochen_kontext()
    except Exception as e:
        print(f"  Notion-Teil uebersprungen: {e}")
        kontext = {"monatsplan": None, "wochenplan": None, "themen": []}
    # Launch + MD fuer das (evtl. simulierte) Datum frisch setzen
    kontext["launch"] = launch_engine.get_story_kontext(heute)
    kontext["monatsplan_md"] = monatsplan_reader.lade_monatsplan(heute, profil)

    lc = kontext["launch"]
    if lc.get("launch_aktiv"):
        print(f"  Modus: 🚀 LAUNCH ({lc['phase']}, Tag {lc.get('tag_im_launch')}) · Vorlage: {lc['julia_vorlage_key']}")
    else:
        print(f"  Modus: 📖 kein Launch · Julia-Vorlage: {lc['julia_vorlage_key']}")
    mp = kontext.get("monatsplan_md")
    print(f"  Monatsplan: {mp['datei'] if mp else '(keiner fuer dieses Profil)'}")

    slug = f"preview-{heute.isoformat()}-{profil}"
    res = claude_caller.generate_story_html(profil=profil, kontext=kontext, heute=heute, slug=slug)
    if not res.get("ok"):
        print(f"  [FEHLER Claude] {res.get('error')}")
        return res
    print(f"  HTML: {res['html_path']}  ({res['slide_count']} Slides, {res['tokens_out']} out-tokens)")

    out_dir = Path(res["output_dir"])
    rr = render_caller.render_stories(html_path=res["html_path"], output_dir=out_dir / "png")
    if not rr.get("ok"):
        print(f"  [FEHLER Render] {rr.get('error')}")
        return rr
    print(f"  PNGs: {rr['slides_count']} Stk in {out_dir / 'png'}")
    return {"ok": True, "html": str(res["html_path"]), "png_dir": str(out_dir / "png"), "pngs": rr.get("png_paths", [])}


if __name__ == "__main__":
    args = [a for a in sys.argv[1:]]
    heute = date.today()
    profile = ["mentoring", "doterra"]
    for a in args:
        if a in ("mentoring", "doterra"):
            profile = [a]
        else:
            try:
                heute = date.fromisoformat(a)
            except ValueError:
                pass

    ergebnisse = {}
    for p in profile:
        ergebnisse[p] = preview(p, heute)

    print(f"\n\n{'='*60}\n  ZUSAMMENFASSUNG\n{'='*60}")
    for p, r in ergebnisse.items():
        if r.get("ok"):
            print(f"  {p}: OK → {r['png_dir']}")
        else:
            print(f"  {p}: FEHLER → {r.get('error')}")
