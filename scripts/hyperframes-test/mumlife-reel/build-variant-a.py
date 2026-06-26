#!/usr/bin/env python3
"""
Variant A — Pure Kinetic-Typography Reel (no Patricia video).
9 Brand-Cards (~2s each) that pop through in sequence. Total ~18s.
No face → no face-cover concern. Brand-only.
"""
from pathlib import Path

ROOT = Path(__file__).parent
OUTPUT = ROOT / "index.html"

# Each card: (id, bg, duration, html, exit-style)
CARDS = [
    # (id, bg-class, duration, html-content)
    ("c1-hook", "bg-creme", 2.0, '''
        <div class="flame">🔥</div>
        <div class="label">Bootcamp</div>
        <div class="title">5 Tage<br/><span class="italic-pop">Klarheit.</span></div>
        <div class="date-pill">29.6. – 3.7.</div>
    '''),
    ("c2-zielgruppe", "bg-petrol", 2.2, '''
        <div class="label-white">Für jede Mama,</div>
        <div class="subline">die zwischen Bügelwäsche und Network</div>
        <div class="big-italic">ihren roten Faden sucht.</div>
    '''),
    ("c3-no-webinar", "bg-creme", 1.5, '''
        <div class="x-stamp">❌</div>
        <div class="no-line">Kein Webinar.</div>
    '''),
    ("c4-no-studium", "bg-creme", 1.5, '''
        <div class="x-stamp">❌</div>
        <div class="no-line">Kein zweites Studium.</div>
    '''),
    ("c5-no-strategie", "bg-creme", 1.5, '''
        <div class="x-stamp">❌</div>
        <div class="no-line">Keine Strategie&shy;-Power-Hour.</div>
    '''),
    ("c6-tage-pill", "bg-petrol", 2.2, '''
        <div class="label-white">Du brauchst nur</div>
        <div class="big-number">5</div>
        <div class="big-word">Tage.</div>
    '''),
    ("c7-pia", "bg-creme", 2.2, '''
        <div class="label">Mit deiner KI-Mentorin</div>
        <div class="pia-name">PIA<span class="pia-dot">.</span></div>
        <div class="subline-small">Sie baut deine Bio. Deine Hooks.<br/>Deine Wochenstruktur.</div>
    '''),
    ("c8-kostenlos", "bg-orange", 2.0, '''
        <div class="big-word-white">Das Ganze</div>
        <div class="huge-zero">0<span class="chf-mark">CHF</span></div>
    '''),
    ("c9-cta", "bg-dunkelblau", 2.5, '''
        <div class="label-white">Anmeldung</div>
        <div class="cta-headline">Link in<br/><span class="italic-orange">der Bio.</span></div>
        <div class="arrow-row">
          <div class="arrow-line"></div>
          <div class="arrow-head"></div>
        </div>
    '''),
]

# Build clip divs (sequential, each is full-screen)
total = 0
clip_divs = []
tweens = []
for i, (cid, bg, dur, html) in enumerate(CARDS):
    start = total
    # Trim 0.05s off all but last to prevent end-equals-next-start lint error
    clip_dur = dur - 0.05 if i < len(CARDS) - 1 else dur
    clip_divs.append(
        f'<div id="{cid}" class="clip card {bg}" data-start="{start:.2f}" data-duration="{clip_dur:.2f}" data-track-index="1">\n{html}\n</div>'
    )
    # Bubble/card entry: scale + opacity
    tweens.append(
        f'tl.fromTo("#{cid} > *", '
        f'{{ opacity: 0, y: 40 }}, '
        f'{{ opacity: 1, y: 0, duration: 0.4, stagger: 0.12, ease: "back.out(1.7)" }}, {start + 0.05:.2f});'
    )
    # Exit fade
    if i < len(CARDS) - 1:
        tweens.append(
            f'tl.to("#{cid} > *", {{ opacity: 0, duration: 0.25, ease: "power2.in" }}, {start + dur - 0.3:.2f});'
        )
    total += dur

duration = total
print(f"Variant A duration: {duration:.2f}s · cards: {len(CARDS)}")

html_tweens = "\n      ".join(tweens)
html_clips = "\n      ".join(clip_divs)

template = f'''<!doctype html>
<html lang="de" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      @font-face {{ font-family: "Philosopher"; font-style: normal; font-weight: 400; src: url("assets/fonts/Philosopher-400.woff2") format("woff2"); }}
      @font-face {{ font-family: "Philosopher"; font-style: normal; font-weight: 700; src: url("assets/fonts/Philosopher-700.woff2") format("woff2"); }}
      @font-face {{ font-family: "Source Sans 3"; font-style: normal; font-weight: 300 700; src: url("assets/fonts/SourceSans3-Variable.woff2") format("woff2-variations"); }}
      :root {{
        --petrol: #12828c;
        --dunkelblau: #29556d;
        --creme: #f1ecdd;
        --orange: #dc822e;
        --text: #0c1c30;
      }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: var(--creme); font-family: "Source Sans 3", sans-serif; color: var(--text); }}

      .card {{
        position: absolute; inset: 0;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        padding: 80px;
        text-align: center;
      }}
      .bg-creme     {{ background: var(--creme); color: var(--text); }}
      .bg-petrol    {{ background: var(--petrol); color: #fff; }}
      .bg-orange    {{ background: var(--orange); color: #fff; }}
      .bg-dunkelblau{{ background: var(--dunkelblau); color: #fff; }}

      /* === c1 Hook === */
      .flame {{ font-size: 140px; margin-bottom: 12px; }}
      .label {{ font-family: "Source Sans 3"; font-weight: 700; font-size: 48px; letter-spacing: 0.16em; text-transform: uppercase; color: var(--petrol); margin-bottom: 28px; }}
      .label-white {{ font-family: "Source Sans 3"; font-weight: 700; font-size: 48px; letter-spacing: 0.16em; text-transform: uppercase; color: #fff; margin-bottom: 28px; }}
      .title {{ font-family: "Philosopher"; font-weight: 700; font-size: 168px; line-height: 0.95; color: var(--dunkelblau); margin-bottom: 40px; }}
      .italic-pop {{ color: var(--petrol); font-style: italic; }}
      .date-pill {{ background: #fff; color: var(--petrol); padding: 18px 48px; border-radius: 22px; font-family: "Source Sans 3"; font-weight: 700; font-size: 84px; box-shadow: 0 14px 36px rgba(18, 130, 140, 0.3); }}

      /* === c2 Zielgruppe === */
      .subline {{ font-family: "Source Sans 3"; font-weight: 400; font-size: 56px; line-height: 1.3; color: #fff; opacity: 0.95; margin-bottom: 32px; max-width: 860px; }}
      .big-italic {{ font-family: "Philosopher"; font-weight: 700; font-style: italic; font-size: 120px; line-height: 1.05; color: #fff; }}

      /* === c3-c5 No-Lines === */
      .x-stamp {{ font-size: 220px; margin-bottom: 24px; }}
      .no-line {{ font-family: "Philosopher"; font-weight: 700; font-size: 130px; line-height: 1.05; color: var(--text); }}

      /* === c6 5 Tage === */
      .big-number {{ font-family: "Philosopher"; font-weight: 700; font-size: 560px; line-height: 0.85; color: #fff; }}
      .big-word {{ font-family: "Philosopher"; font-weight: 700; font-style: italic; font-size: 200px; line-height: 1; color: #fff; }}

      /* === c7 PIA === */
      .pia-name {{ font-family: "Philosopher"; font-weight: 700; font-size: 360px; line-height: 1; color: var(--petrol); letter-spacing: -0.02em; margin-bottom: 28px; }}
      .pia-dot {{ color: var(--orange); }}
      .subline-small {{ font-family: "Source Sans 3"; font-weight: 400; font-size: 48px; line-height: 1.3; color: var(--text); opacity: 0.8; max-width: 860px; }}

      /* === c8 Kostenlos === */
      .big-word-white {{ font-family: "Philosopher"; font-weight: 700; font-size: 144px; line-height: 1; color: #fff; margin-bottom: 24px; }}
      .huge-zero {{ font-family: "Philosopher"; font-weight: 700; font-size: 720px; line-height: 0.85; color: #fff; position: relative; display: inline-block; }}
      .chf-mark {{ position: absolute; top: 80px; right: -200px; font-size: 96px; transform: rotate(8deg); background: #fff; color: var(--orange); padding: 10px 28px; border-radius: 16px; }}

      /* === c9 CTA === */
      .cta-headline {{ font-family: "Philosopher"; font-weight: 700; font-size: 144px; line-height: 1.05; color: #fff; margin-bottom: 40px; }}
      .italic-orange {{ color: var(--orange); font-style: italic; }}
      .arrow-row {{ display: flex; align-items: center; justify-content: center; gap: 10px; height: 60px; }}
      .arrow-line {{ width: 280px; height: 10px; background: var(--orange); border-radius: 5px; transform-origin: left center; }}
      .arrow-head {{ width: 0; height: 0; border-top: 28px solid transparent; border-bottom: 28px solid transparent; border-left: 44px solid var(--orange); }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{duration:.2f}" data-width="1080" data-height="1920">

      {html_clips}

    </div>

    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});

      {html_tweens}

      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''
OUTPUT.write_text(template, encoding="utf-8")
print(f"Wrote {OUTPUT}")
