"""Render-Caller — ruft scripts/karussell-render/render-stories.js als Subprocess.

Wandelt eine Story-HTML-Datei in 1-10 PNG-Folien (1080×1920, 9:16, Instagram-Story).

Outputs landen in einem Ordner, jede Folie als 01.png, 02.png, ...
"""

from __future__ import annotations

import logging
import shutil
import subprocess
from pathlib import Path

import config

logger = logging.getLogger(__name__)


def _node_executable() -> str:
    """Findet den passenden node-Befehl (Windows: node.exe via PATH)."""
    n = shutil.which("node")
    if not n:
        raise RuntimeError(
            "Node.js nicht im PATH gefunden. Render-Pipeline braucht Node 18+."
        )
    return n


def render_stories(html_path: str | Path, output_dir: str | Path,
                   timeout_sec: int = 180) -> dict:
    """Rendert eine Story-HTML zu PNG-Folien.

    Args:
        html_path: Pfad zur Story-HTML (z.B. outputs/stories/2026-05-01-mentoring/slides.html)
        output_dir: Ziel-Ordner für die PNGs (wird angelegt falls fehlend)
        timeout_sec: Subprocess-Timeout (Default 3 Min)

    Returns:
        {
          "ok": True/False,
          "slides_count": 8,
          "png_paths": ["01.png", "02.png", ...],
          "stdout": "...",
          "stderr": "...",
        }
    """
    html_path = Path(html_path).resolve()
    output_dir = Path(output_dir).resolve()

    if not html_path.exists():
        return {"ok": False, "error": f"HTML nicht gefunden: {html_path}",
                "slides_count": 0, "png_paths": []}

    output_dir.mkdir(parents=True, exist_ok=True)

    render_script = config.RENDER_SCRIPT
    if not render_script.exists():
        return {"ok": False, "error": f"render-stories.js nicht gefunden: {render_script}",
                "slides_count": 0, "png_paths": []}

    cmd = [
        _node_executable(),
        str(render_script),
        f"--input={html_path}",
        f"--output={output_dir}",
    ]

    logger.info(f"Render-Subprocess: {' '.join(cmd)}")

    try:
        result = subprocess.run(
            cmd,
            cwd=render_script.parent,  # für npm/node_modules-Auflösung
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=timeout_sec,
        )
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": f"Timeout nach {timeout_sec}s",
                "slides_count": 0, "png_paths": []}
    except Exception as e:
        return {"ok": False, "error": f"Subprocess-Fehler: {e}",
                "slides_count": 0, "png_paths": []}

    if result.returncode != 0:
        logger.error(f"Render-Fehler (Code {result.returncode}):\n{result.stderr}")
        return {
            "ok": False,
            "error": f"Render-Fehler (Code {result.returncode})",
            "slides_count": 0,
            "png_paths": [],
            "stdout": result.stdout,
            "stderr": result.stderr,
        }

    # Alle erstellten PNGs sammeln, sortiert
    pngs = sorted(output_dir.glob("*.png"))
    png_paths = [str(p) for p in pngs]

    logger.info(f"Render-OK: {len(png_paths)} PNGs in {output_dir}")

    return {
        "ok": True,
        "slides_count": len(png_paths),
        "png_paths": png_paths,
        "output_dir": str(output_dir),
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


# ========================================
# CLI-Tester
# ========================================
if __name__ == "__main__":
    import sys
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    if len(sys.argv) < 3:
        print("Nutzung: python render_caller.py <html-pfad> <output-ordner>")
        # Versuche bekannte Test-Story
        test_html = config.OUTPUTS_STORIES_DIR / "2026-05-01-mentoring-bio-check-mixstil-test" / "slides.html"
        test_out = config.OUTPUTS_STORIES_DIR / "2026-05-01-mentoring-bio-check-mixstil-test" / "png-render-test"
        if test_html.exists():
            print(f"\n[TEST-MODE] Rendere {test_html.name} → {test_out.name}")
            r = render_stories(test_html, test_out)
            print(f"\n  ok={r['ok']}  Slides={r['slides_count']}")
            if not r["ok"]:
                print(f"  Fehler: {r.get('error')}")
                if r.get("stderr"):
                    print(f"  Stderr:\n{r['stderr'][:500]}")
        sys.exit(0)

    r = render_stories(sys.argv[1], sys.argv[2])
    print(f"ok={r['ok']}  Slides={r['slides_count']}")
    if not r["ok"]:
        print(f"Fehler: {r.get('error')}")
        if r.get("stderr"):
            print(f"Stderr:\n{r['stderr']}")
