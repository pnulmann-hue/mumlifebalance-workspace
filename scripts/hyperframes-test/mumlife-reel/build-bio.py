#!/usr/bin/env python3
"""
BIO B-Roll-Reel V2:
 - Multi-Clip B-Roll (Greens → Screen-Bio overlay → Avocado-Brot) — KEIN Loop
 - Captions MITTIG zentriert
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent
TRANSCRIPT = ROOT / "assets" / "bio-voiceover.json"
OUTPUT = ROOT / "index.html"

VOICEOVER = "assets/bio-voiceover.mp3"
BROLL_1   = "assets/bio-broll.mp4"      # Greens (37s)
BROLL_2   = "assets/bio-broll-2.mp4"    # Avocado-Brot (11s)
SCREEN    = "assets/bio-screen.mp4"     # Insta-Bio (29s)

# Cut-Plan
B1_START, B1_DUR = 0.0, 9.14      # Greens
SCREEN_START, SCREEN_DUR = 9.14, 20.86   # Insta-Bio overlay (until 30s)
B2_START, B2_DUR = 30.0, 11.0     # Avocado-Brot
# 41-45.64s: End-CTA-Card überdeckt

ACCENT = {"bio", "menti", "mentee", "schmerzpunkt", "transformation", "80", "bio-bot", "bio-bott", "kommentier", "kommentiere", "schick", "link"}

def strip_word(w): return w.strip()
def is_accent(w):
    c = re.sub(r"[^\wäöüÄÖÜß-]", "", w).lower()
    return c in ACCENT

def correct_word(w):
    repl = {
        "Menti": "Mentee", "menti": "Mentee",
        "Liedmagneten": "Lead-Magnet", "Liedmagnet": "Lead-Magnet",
        "Bio-Bott": "Bio-Bot", "bio-bott": "Bio-Bot",
        "Skrollen": "Scrollen", "skrollen": "scrollen",
    }
    return repl.get(w, w)

def load_words():
    data = json.loads(TRANSCRIPT.read_text(encoding="utf-8"))
    words = []
    for seg in data["segments"]:
        for w in seg.get("words", []):
            words.append({"word": correct_word(strip_word(w["word"])), "start": w["start"], "end": w["end"]})
    return words

words = load_words()
duration = max(w["end"] for w in words) + 0.4

phrases = []
cur = []
for w in words:
    cur.append(w)
    if len(cur) >= 4 or (len(cur) >= 2 and w["word"].rstrip().endswith((".", ",", "!", "?"))):
        phrases.append(cur); cur = []
if cur: phrases.append(cur)

def render_phrase(words_chunk):
    spans = []
    for w in words_chunk:
        cls = "w accent" if is_accent(w["word"]) else "w"
        spans.append(f'<span class="{cls}">{w["word"]}</span>')
    out = " ".join(spans)
    return out.replace(' <span class="w">-', '<span class="w">-').replace(' <span class="w accent">-', '<span class="w accent">-')

# End-CTA: starts when Avocado ends, runs to end of audio
cta_start = round(B2_START + B2_DUR, 2)   # 41.0
cta_dur = round(duration - cta_start, 2)  # ~4.64

caption_divs, tweens = [], []
for i, ph in enumerate(phrases):
    pid = f"cap-{i:02d}"
    s = round(ph[0]["start"], 2)
    next_s = phrases[i+1][0]["start"] if i+1 < len(phrases) else duration
    dur = round(min(next_s - s - 0.05, ph[-1]["end"] + 0.4 - s), 2)
    if dur < 0.4: dur = 0.4
    # Hide captions during End-CTA to avoid overlap
    if s >= cta_start - 0.3:
        continue
    html = render_phrase(ph)
    caption_divs.append(
        f'<div id="{pid}" class="clip caption" data-start="{s}" data-duration="{dur}" data-track-index="4">'
        f'<div class="bubble"><p class="text">{html}</p></div></div>'
    )
    tweens.append(f'tl.fromTo("#{pid} .bubble", {{ opacity: 0, y: 24, scale: 0.94 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.3, ease: "power3.out" }}, {s});')
    tweens.append(f'tl.fromTo("#{pid} .w", {{ opacity: 0, scale: 0.7 }}, {{ opacity: 1, scale: 1, duration: 0.22, ease: "back.out(2.5)", stagger: 0.04 }}, {s});')
    tweens.append(f'tl.fromTo("#{pid} .accent", {{}}, {{ "--hl": "100%", duration: 0.5, ease: "power2.out" }}, {s + 0.3});')
    exit_at = round(s + dur - 0.2, 2)
    tweens.append(f'tl.to("#{pid} .bubble", {{ opacity: 0, y: -16, duration: 0.2, ease: "power2.in" }}, {exit_at});')
    tweens.append(f'tl.set("#{pid}", {{ opacity: 0 }}, {round(s + dur, 2)});')

# Video crossfades
tweens.append(f'tl.fromTo("#bg-1", {{ opacity: 1 }}, {{ opacity: 0, duration: 0.3, ease: "power2.in" }}, {B1_START + B1_DUR - 0.15});')
tweens.append(f'tl.set("#bg-1", {{ opacity: 0 }}, {B1_START + B1_DUR});')

tweens.append(f'tl.fromTo("#screen-bio", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3, ease: "power2.out" }}, {SCREEN_START});')
tweens.append(f'tl.to("#screen-bio", {{ opacity: 0, duration: 0.3, ease: "power2.in" }}, {SCREEN_START + SCREEN_DUR - 0.3});')
tweens.append(f'tl.set("#screen-bio", {{ opacity: 0 }}, {SCREEN_START + SCREEN_DUR});')

tweens.append(f'tl.fromTo("#bg-2", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3, ease: "power2.out" }}, {B2_START - 0.15});')
tweens.append(f'tl.to("#bg-2", {{ opacity: 0, duration: 0.3, ease: "power2.in" }}, {B2_START + B2_DUR - 0.15});')
tweens.append(f'tl.set("#bg-2", {{ opacity: 0 }}, {B2_START + B2_DUR});')

# End-CTA card
tweens.append(f'tl.fromTo("#cta-final", {{ scale: 0.85, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.4, ease: "back.out(1.4)" }}, {cta_start});')
tweens.append(f'tl.to("#cta-final .pop", {{ scale: 1.08, duration: 0.35, yoyo: true, repeat: 4, ease: "power1.inOut" }}, {cta_start + 0.6});')

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
      :root {{ --petrol: #12828c; --dunkelblau: #29556d; --creme: #f1ecdd; --orange: #dc822e; --text: #0c1c30; }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #000; font-family: "Source Sans 3", sans-serif; color: var(--text); }}
      .bg-video {{ position: absolute; inset: 0; width: 1080px; height: 1920px; object-fit: cover; }}
      #bg-1 {{ z-index: 10; }}
      #bg-2 {{ z-index: 11; opacity: 0; }}
      #screen-bio {{ position: absolute; inset: 0; width: 1080px; height: 1920px; object-fit: cover; z-index: 30; opacity: 0; }}

      /* Captions MITTIG vertikal + horizontal — keine Crop-Gefahr */
      .caption {{ position: absolute; left: 60px; right: 60px; top: 50%; transform: translateY(-50%); display: flex; justify-content: center; z-index: 40; }}
      .bubble {{ background: var(--creme); padding: 36px 50px; border-radius: 28px; box-shadow: 0 18px 44px rgba(12,28,48,0.40); max-width: 960px; text-align: center; }}
      .bubble .text {{ font-family: "Source Sans 3"; font-weight: 600; font-size: 56px; line-height: 1.25; color: var(--text); }}
      .bubble .w {{ display: inline-block; margin-right: 0.18em; }}
      .bubble .w.accent {{ position: relative; color: var(--petrol); font-weight: 700; --hl: 0%; }}
      .bubble .w.accent::after {{ content: ""; position: absolute; left: -4px; bottom: 2px; width: var(--hl); height: 14px; background: rgba(220,130,46,0.45); z-index: -1; border-radius: 4px; }}

      /* End-CTA — auch mittig */
      #cta-final {{ position: absolute; left: 60px; right: 60px; top: 50%; transform: translate(0, -50%) scale(1); background: var(--creme); padding: 64px 80px; border-radius: 36px; box-shadow: 0 28px 70px rgba(12,28,48,0.50); text-align: center; z-index: 60; }}
      #cta-final .label {{ font-family: "Source Sans 3"; font-weight: 700; font-size: 42px; letter-spacing: 0.16em; text-transform: uppercase; color: var(--petrol); margin-bottom: 22px; }}
      #cta-final .headline {{ font-family: "Philosopher"; font-weight: 700; font-size: 168px; line-height: 1; color: var(--dunkelblau); }}
      #cta-final .headline .pop {{ color: var(--petrol); font-style: italic; display: inline-block; transform-origin: center; background: #fff; padding: 6px 32px; border-radius: 18px; }}

      .brand-footer {{ position: absolute; top: 30px; left: 0; right: 0; text-align: center; font-family: "Philosopher"; font-weight: 700; font-size: 26px; color: #fff; text-shadow: 0 2px 8px rgba(0,0,0,0.7); letter-spacing: 0.1em; z-index: 70; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{duration:.2f}" data-width="1080" data-height="1920">

      <video id="bg-1" class="clip bg-video" data-start="{B1_START}" data-duration="{B1_DUR}" data-track-index="1" src="{BROLL_1}" muted playsinline></video>
      <video id="bg-2" class="clip bg-video" data-start="{B2_START}" data-duration="{B2_DUR}" data-track-index="2" src="{BROLL_2}" muted playsinline></video>
      <video id="screen-bio" class="clip" data-start="{SCREEN_START}" data-duration="{SCREEN_DUR}" data-track-index="3" src="{SCREEN}" muted playsinline></video>
      <audio id="audio-track" class="clip" data-start="0" data-duration="{duration:.2f}" data-track-index="0" src="{VOICEOVER}"></audio>

      <div id="brand-footer" class="clip brand-footer" data-start="0" data-duration="{duration:.2f}" data-track-index="70">@mum.life.balance</div>

      {chr(10).join("      " + d for d in caption_divs)}

      <div id="cta-final" class="clip" data-start="{cta_start}" data-duration="{cta_dur}" data-track-index="60">
        <div class="label">Kommentier</div>
        <div class="headline"><span class="pop">BIO</span></div>
      </div>
    </div>

    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      {chr(10).join("      " + t for t in tweens)}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''
OUTPUT.write_text(template, encoding="utf-8")
print(f"Wrote {OUTPUT}")
print(f"Duration: {duration:.2f}s · Phrases (visible): {len(caption_divs)}")
print(f"Cut-Plan: B1 {B1_START}-{B1_START+B1_DUR} (Greens) | Screen {SCREEN_START}-{SCREEN_START+SCREEN_DUR} | B2 {B2_START}-{B2_START+B2_DUR} (Avocado) | CTA {cta_start}-{cta_start+cta_dur}")
