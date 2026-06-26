#!/usr/bin/env python3
"""
Bootcamp B-Roll-Reel V2:
 - Multi-Clip B-Roll (Garten → Notion overlay → Küche → Saft → Pfannkuchen) — KEIN Loop
 - Captions MITTIG zentriert
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent
TRANSCRIPT = ROOT / "assets" / "bc-voiceover.json"
OUTPUT = ROOT / "index.html"

VOICEOVER = "assets/bc-voiceover.mp3"
B1  = "assets/bc-broll.mp4"     # Garten (14s)
B2  = "assets/bc-broll-2.mp4"   # Küche/Topf (18s)
B3  = "assets/bc-broll-3.mp4"   # Saft (12s)
B4  = "assets/bc-broll-4.mp4"   # Pfannkuchen (7s)
SCREEN = "assets/bc-screen.mp4" # Notion (33s)

# Cut-Plan (Audio = 79s)
B1_START, B1_DUR = 0.0, 6.0      # Garten (von 14s nur 6s)
SCREEN_START, SCREEN_DUR = 6.0, 33.0    # Notion overlay (bis 39s)
B2_START, B2_DUR = 39.0, 18.0    # Küche (39-57s)
B3_START, B3_DUR = 57.0, 12.0    # Saft (57-69s)
B4_START, B4_DUR = 69.0, 7.0     # Pfannkuchen (69-76s)
# 76-78.92s: End-CTA-Card überdeckt

ACCENT = {"bootcamp", "bio", "pia", "ki-mentorin", "kostenlos", "lead-magnet", "liedmagnet", "29.", "3.", "juni", "5"}

def strip_word(w): return w.strip()
def is_accent(w):
    c = re.sub(r"[^\wäöüÄÖÜß-]", "", w).lower()
    return c in ACCENT

def correct_word(w, start_time):
    """Fix Whisper-Errors + „29. Juli → 29. Juni" verbal slip."""
    repl = {
        "Liedmagneten": "Lead-Magnet", "Liedmagnet": "Lead-Magnet",
        "Skrollen": "Scrollen", "skrollen": "scrollen",
        "Pia": "PIA",
    }
    w = repl.get(w, w)
    if w.lower() == "juli" and start_time > 73 and start_time < 76:
        return "Juni"
    return w

def load_words():
    data = json.loads(TRANSCRIPT.read_text(encoding="utf-8"))
    words = []
    for seg in data["segments"]:
        for w in seg.get("words", []):
            words.append({"word": correct_word(strip_word(w["word"]), w["start"]), "start": w["start"], "end": w["end"]})
    return words

words = load_words()
duration = max(w["end"] for w in words) + 0.5

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

cta_start = round(B4_START + B4_DUR, 2)   # 76.0
cta_dur = round(duration - cta_start, 2)  # ~2.92

caption_divs, tweens = [], []
for i, ph in enumerate(phrases):
    pid = f"cap-{i:02d}"
    s = round(ph[0]["start"], 2)
    next_s = phrases[i+1][0]["start"] if i+1 < len(phrases) else duration
    dur = round(min(next_s - s - 0.05, ph[-1]["end"] + 0.4 - s), 2)
    if dur < 0.4: dur = 0.4
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

# Video crossfades (kill each as next begins)
def fade_out(elem_id, at, hide_at):
    tweens.append(f'tl.fromTo("#{elem_id}", {{ opacity: 1 }}, {{ opacity: 0, duration: 0.3, ease: "power2.in" }}, {at});')
    tweens.append(f'tl.set("#{elem_id}", {{ opacity: 0 }}, {hide_at});')

def fade_in(elem_id, at):
    tweens.append(f'tl.fromTo("#{elem_id}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3, ease: "power2.out" }}, {at});')

fade_out("bg-1", B1_START + B1_DUR - 0.15, B1_START + B1_DUR)

fade_in("screen-bc", SCREEN_START)
tweens.append(f'tl.to("#screen-bc", {{ opacity: 0, duration: 0.3, ease: "power2.in" }}, {SCREEN_START + SCREEN_DUR - 0.3});')
tweens.append(f'tl.set("#screen-bc", {{ opacity: 0 }}, {SCREEN_START + SCREEN_DUR});')

fade_in("bg-2", B2_START - 0.15)
fade_out("bg-2", B2_START + B2_DUR - 0.15, B2_START + B2_DUR)

fade_in("bg-3", B3_START - 0.15)
fade_out("bg-3", B3_START + B3_DUR - 0.15, B3_START + B3_DUR)

fade_in("bg-4", B4_START - 0.15)
fade_out("bg-4", B4_START + B4_DUR - 0.15, B4_START + B4_DUR)

# End-CTA
tweens.append(f'tl.fromTo("#cta-final", {{ scale: 0.85, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.4, ease: "back.out(1.4)" }}, {cta_start});')
tweens.append(f'tl.to("#cta-final .pop", {{ scale: 1.08, duration: 0.35, yoyo: true, repeat: 3, ease: "power1.inOut" }}, {cta_start + 0.6});')

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
      #bg-3 {{ z-index: 12; opacity: 0; }}
      #bg-4 {{ z-index: 13; opacity: 0; }}
      #screen-bc {{ position: absolute; inset: 0; width: 1080px; height: 1920px; object-fit: cover; z-index: 30; opacity: 0; }}

      .caption {{ position: absolute; left: 60px; right: 60px; top: 50%; transform: translateY(-50%); display: flex; justify-content: center; z-index: 40; }}
      .bubble {{ background: var(--creme); padding: 36px 50px; border-radius: 28px; box-shadow: 0 18px 44px rgba(12,28,48,0.40); max-width: 960px; text-align: center; }}
      .bubble .text {{ font-family: "Source Sans 3"; font-weight: 600; font-size: 56px; line-height: 1.25; color: var(--text); }}
      .bubble .w {{ display: inline-block; margin-right: 0.18em; }}
      .bubble .w.accent {{ position: relative; color: var(--petrol); font-weight: 700; --hl: 0%; }}
      .bubble .w.accent::after {{ content: ""; position: absolute; left: -4px; bottom: 2px; width: var(--hl); height: 14px; background: rgba(220,130,46,0.45); z-index: -1; border-radius: 4px; }}

      #cta-final {{ position: absolute; left: 60px; right: 60px; top: 50%; transform: translate(0, -50%) scale(1); background: var(--creme); padding: 56px 72px; border-radius: 36px; box-shadow: 0 28px 70px rgba(12,28,48,0.50); text-align: center; z-index: 60; }}
      #cta-final .label {{ font-family: "Source Sans 3"; font-weight: 700; font-size: 38px; letter-spacing: 0.14em; text-transform: uppercase; color: var(--petrol); margin-bottom: 22px; }}
      #cta-final .headline {{ font-family: "Philosopher"; font-weight: 700; font-size: 96px; line-height: 1.05; color: var(--dunkelblau); }}
      #cta-final .headline .pop {{ color: var(--petrol); font-style: italic; display: inline-block; transform-origin: center; background: #fff; padding: 4px 28px; border-radius: 16px; }}

      .brand-footer {{ position: absolute; top: 30px; left: 0; right: 0; text-align: center; font-family: "Philosopher"; font-weight: 700; font-size: 26px; color: #fff; text-shadow: 0 2px 8px rgba(0,0,0,0.7); letter-spacing: 0.1em; z-index: 70; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{duration:.2f}" data-width="1080" data-height="1920">

      <video id="bg-1" class="clip bg-video" data-start="{B1_START}" data-duration="{B1_DUR}" data-track-index="1" src="{B1}" muted playsinline></video>
      <video id="bg-2" class="clip bg-video" data-start="{B2_START}" data-duration="{B2_DUR}" data-track-index="2" src="{B2}" muted playsinline></video>
      <video id="bg-3" class="clip bg-video" data-start="{B3_START}" data-duration="{B3_DUR}" data-track-index="3" src="{B3}" muted playsinline></video>
      <video id="bg-4" class="clip bg-video" data-start="{B4_START}" data-duration="{B4_DUR}" data-track-index="4" src="{B4}" muted playsinline></video>
      <video id="screen-bc" class="clip" data-start="{SCREEN_START}" data-duration="{SCREEN_DUR}" data-track-index="5" src="{SCREEN}" muted playsinline></video>
      <audio id="audio-track" class="clip" data-start="0" data-duration="{duration:.2f}" data-track-index="0" src="{VOICEOVER}"></audio>

      <div id="brand-footer" class="clip brand-footer" data-start="0" data-duration="{duration:.2f}" data-track-index="70">@mum.life.balance</div>

      {chr(10).join("      " + d for d in caption_divs)}

      <div id="cta-final" class="clip" data-start="{cta_start}" data-duration="{cta_dur}" data-track-index="60">
        <div class="label">29. Juni – 3. Juli · kostenlos</div>
        <div class="headline">Kommentier <span class="pop">BOOTCAMP</span></div>
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
print(f"Cut-Plan: B1 Garten 0-{B1_DUR} | Notion {SCREEN_START}-{SCREEN_START+SCREEN_DUR} | B2 Küche {B2_START}-{B2_START+B2_DUR} | B3 Saft {B3_START}-{B3_START+B3_DUR} | B4 Pfannk {B4_START}-{B4_START+B4_DUR} | CTA {cta_start}-{cta_start+cta_dur}")
