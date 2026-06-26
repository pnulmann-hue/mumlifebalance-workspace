#!/usr/bin/env python3
"""
Reel-Cover-Generator (1080×1920).

Usage:
  python render-cover.py --photo "201" --hook "ALS MAMA-CEO IM NETWORK EIN BUSINESS AUFZIEHEN" --pop "NEXT LEVEL SHIT!!!!" --sub ""
  python render-cover.py --photo "201" --hook-file briefing.json

Output: cover-output/[slug]-cover.png
"""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import os
from datetime import datetime

ROOT = Path(__file__).parent
WORKSPACE = ROOT.parent.parent
PHOTOS_DIR = WORKSPACE / "context" / "Shootingbilder"
OUTPUT_DIR = ROOT / "covers"
OUTPUT_DIR.mkdir(exist_ok=True)

TEMPLATE_HTML = """<!doctype html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <style>
    @font-face {{ font-family: "Philosopher"; font-style: normal; font-weight: 700; src: url("../../scripts/hyperframes-test/mumlife-reel/assets/fonts/Philosopher-700.woff2") format("woff2"); }}
    @font-face {{ font-family: "Source Sans 3"; font-style: normal; font-weight: 300 700; src: url("../../scripts/hyperframes-test/mumlife-reel/assets/fonts/SourceSans3-Variable.woff2") format("woff2-variations"); }}
    :root {{
      --petrol: #12828c;
      --dunkelblau: #29556d;
      --creme: #f1ecdd;
      --orange: #dc822e;
    }}
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #000; }}
    .cover {{
      position: absolute; inset: 0;
      width: 1080px; height: 1920px;
      overflow: hidden;
    }}
    .bg {{
      position: absolute; inset: 0;
      width: 100%; height: 100%;
      object-fit: cover;
      z-index: 1;
    }}
    .gradient {{
      position: absolute; inset: 0;
      background: linear-gradient(180deg,
        rgba(0,0,0,0.0) 0%,
        rgba(0,0,0,0.1) 35%,
        rgba(0,0,0,0.55) 65%,
        rgba(0,0,0,0.85) 100%);
      z-index: 2;
    }}
    .text-block {{
      position: absolute;
      bottom: 180px;
      left: 60px;
      right: 60px;
      z-index: 3;
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
    }}
    .hook {{
      font-family: "Philosopher", serif;
      font-weight: 700;
      font-size: 88px;
      line-height: 1.05;
      color: #fff;
      text-shadow: 0 6px 18px rgba(0,0,0,0.7);
      letter-spacing: 0.005em;
      margin-bottom: 24px;
      max-width: 960px;
    }}
    .pop {{
      font-family: "Philosopher", serif;
      font-style: italic;
      font-weight: 700;
      font-size: 110px;
      line-height: 1.0;
      color: var(--orange);
      text-shadow: 0 6px 20px rgba(0,0,0,0.7);
      max-width: 960px;
    }}
    .sub {{
      font-family: "Source Sans 3", sans-serif;
      font-weight: 600;
      font-size: 36px;
      color: var(--creme);
      margin-top: 28px;
      opacity: 0.9;
      text-shadow: 0 2px 8px rgba(0,0,0,0.7);
      max-width: 900px;
    }}
  </style>
</head>
<body>
  <div class="cover">
    <img class="bg" src="{photo}" alt="">
    <div class="gradient"></div>
    <div class="text-block">
      {hook_html}
      {pop_html}
      {sub_html}
    </div>
  </div>
</body>
</html>
"""


def render(photo_num, hook, pop, sub, slug=None):
    # Find photo
    photo_files = list(PHOTOS_DIR.glob(f"{photo_num} - *.jpg"))
    if not photo_files:
        print(f"❌ Photo '{photo_num}' not found in {PHOTOS_DIR}")
        sys.exit(1)
    photo_path = photo_files[0].resolve().as_uri()

    # Build text blocks
    hook_html = f'<div class="hook">{hook}</div>' if hook else ""
    pop_html = f'<div class="pop">{pop}</div>' if pop else ""
    sub_html = f'<div class="sub">{sub}</div>' if sub else ""

    html = TEMPLATE_HTML.format(
        photo=photo_path,
        hook_html=hook_html,
        pop_html=pop_html,
        sub_html=sub_html,
    )

    # Write HTML to temp
    work_html = OUTPUT_DIR / f"_work_{slug or 'cover'}.html"
    work_html.write_text(html, encoding="utf-8")

    # Render via puppeteer/playwright (use chrome headless)
    output_png = OUTPUT_DIR / f"{slug or 'cover'}-{photo_num}.png"

    # Use playwright if available, else chrome headless
    render_script = f"""
const puppeteer = require('puppeteer');
(async () => {{
  const browser = await puppeteer.launch({{ headless: 'new' }});
  const page = await browser.newPage();
  await page.setViewport({{ width: 1080, height: 1920, deviceScaleFactor: 1 }});
  await page.goto('file:///{work_html.resolve().as_posix()}', {{ waitUntil: 'networkidle0', timeout: 30000 }});
  await new Promise(r => setTimeout(r, 1000));
  await page.screenshot({{ path: '{output_png.resolve().as_posix()}', type: 'png', omitBackground: false, fullPage: false }});
  await browser.close();
}})();
"""
    js_path = OUTPUT_DIR / "_render.js"
    js_path.write_text(render_script, encoding="utf-8")

    # Find puppeteer — use karussell-render which has node_modules
    cmd_dir = WORKSPACE / "scripts" / "karussell-render"

    result = subprocess.run(
        ["node", str(js_path.resolve())],
        cwd=str(cmd_dir),
        capture_output=True,
        text=True,
        env={**os.environ, "NODE_PATH": str(cmd_dir / "node_modules")},
    )
    if result.returncode != 0:
        print(f"❌ Render failed:\n{result.stderr}")
        sys.exit(1)

    print(f"✓ Cover saved: {output_png}")
    return output_png


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--photo", required=True, help="Shooting photo number (e.g. 201)")
    ap.add_argument("--hook", required=True, help="Main hook text (top)")
    ap.add_argument("--pop", default="", help="Pop-italic-text (bottom, orange)")
    ap.add_argument("--sub", default="", help="Optional sub-text below pop")
    ap.add_argument("--slug", default=None, help="Output slug")
    args = ap.parse_args()

    render(args.photo, args.hook, args.pop, args.sub, args.slug)


if __name__ == "__main__":
    main()
