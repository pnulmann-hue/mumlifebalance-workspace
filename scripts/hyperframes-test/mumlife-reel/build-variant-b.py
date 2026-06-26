#!/usr/bin/env python3
"""
Variant B — B-Roll-Cut-Reel: Patricia's video als Backbone, ABER
mit Full-Screen-Brand-Cards die Patricia für ~1.2s ersetzen (kein Overlay über Gesicht).
- Captions: bottom only (y > 1300px) → unter Hals/Brust, nie über Gesicht
- Stamps: top corners (y 150-300px) → über Kopf
- End-CTA: bottom-aligned card (Patricia bleibt oben sichtbar)
- 3 Cut-In Full-Cards bei ❌-Liste (12-14s), ✅-Liste (17-19s), 0-CHF-Splash (30-31s)
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent
TRANSCRIPT = ROOT / "assets" / "talking-head.json"
VIDEO = "assets/talking-head.mp4"
OUTPUT = ROOT / "index.html"

ACCENT = {"pia", "ki-mentorin", "kostenlos", "bio", "bootcamp", "29.", "3.", "juni", "juli", "5", "fünf", "klaren", "ersten", "kein", "keine", "kostenlos.", "tage,", "tage."}

def strip_word(w): return w.strip()
def is_accent(w):
    c = re.sub(r"[^\wäöüÄÖÜß-]", "", w).lower()
    return c in ACCENT

def load_words():
    data = json.loads(TRANSCRIPT.read_text(encoding="utf-8"))
    words = []
    for seg in data["segments"]:
        for w in seg.get("words", []):
            words.append({"word": strip_word(w["word"]), "start": w["start"], "end": w["end"]})
    return words

def correct_word(word, start_time):
    """Fix obvious Whisper transcription errors / Patricia verbal slips that Patricia approved to correct."""
    w_lower = word.lower().rstrip(".,!?")
    # "29. Juli" → "29. Juni" (Bootcamp starts 29.6.) — only the FIRST 'Juli' under 2.5s
    if w_lower == "juli" and start_time < 2.5:
        return word.replace("Juli", "Juni").replace("juli", "Juni")
    # "durchstalten" → "durchstarten" (clear verbal slip / Whisper miss)
    if "durchstalten" in w_lower:
        return word.replace("durchstalten", "durchstarten")
    return word

def render_phrase_html(words_chunk, marker):
    spans = []
    for w in words_chunk:
        corrected = correct_word(w["word"], w["start"])
        cls = "w accent" if is_accent(corrected) else "w"
        spans.append(f'<span class="{cls}">{corrected}</span>')
    marker_html = f'<span class="marker">{marker}</span> ' if marker else ''
    out = marker_html + " ".join(spans)
    out = out.replace(' <span class="w">-', '<span class="w">-').replace(' <span class="w accent">-', '<span class="w accent">-')
    return out

words = load_words()
duration = max(w["end"] for w in words) + 0.5

# Phrase boundaries — ALL bottom (face safe-zone)
PHRASES = [
    (0, 6,   None,  "p1"),
    (7, 13,  None,  "p2"),
    (14, 21, None,  "p3"),
    (22, 28, None,  "p4"),
    # p5-p7 collapsed → replaced by FULL-SCREEN ❌-CARDS (no overlap with face)
    (40, 43, "✅",   "p8"),
    (44, 49, "✅",   "p9"),
    (50, 54, "✅",   "p10"),
    (55, 59, "✅",   "p11"),
    (60, 63, "✅",   "p12"),
    (64, 68, None,  "p13"),
    (69, 71, None,  "p14"),
    # p15 → replaced by full-screen 0-CHF SPLASH-CARD
]

phrases = []
for start_i, end_i, marker, label in PHRASES:
    chunk = words[start_i:end_i + 1]
    if not chunk: continue
    phrases.append({
        "id": label,
        "words": chunk,
        "start": chunk[0]["start"],
        "end": chunk[-1]["end"],
        "marker": marker,
    })

# Phrase durations: end at next phrase start (or +0.5 after end)
for i, ph in enumerate(phrases):
    next_ph = phrases[i + 1] if i + 1 < len(phrases) else None
    # Also cap before full-screen cards (which take over)
    next_card_start = None
    if 11.5 > ph["start"]:  # before first ❌-card cut-in
        candidates = [c for c in (11.9, 16.5, 30.4) if c > ph["start"]]
        if candidates: next_card_start = min(candidates)
    end_fade = next_ph["start"] - 0.05 if next_ph else ph["end"] + 0.4
    if next_card_start: end_fade = min(end_fade, next_card_start - 0.05)
    ph["duration"] = max(end_fade - ph["start"], 0.6)

# Full-Screen Cut-In Cards (replace Patricia for ~1.5s each)
CUT_CARDS = [
    # (id, start, duration, bg-class, html)
    ("cut-no-list", 11.9, 4.5, "bg-creme", '''
        <div class="cut-label">Du brauchst nicht:</div>
        <div class="cut-no-row"><span class="cut-x">❌</span> <span class="cut-no-text">Webinar</span></div>
        <div class="cut-no-row"><span class="cut-x">❌</span> <span class="cut-no-text">Strategie&shy;-Power-Hour</span></div>
        <div class="cut-no-row"><span class="cut-x">❌</span> <span class="cut-no-text">zweites Studium</span></div>
    '''),
    ("cut-kostenlos", 30.4, 2.6, "bg-orange", '''
        <div class="cut-label-white">Das Ganze</div>
        <div class="cut-huge-zero">0<span class="cut-chf">CHF</span></div>
    '''),
]

# Caption divs
caption_divs = []
for ph in phrases:
    html = render_phrase_html(ph["words"], ph["marker"])
    caption_divs.append(
        f'<div id="{ph["id"]}" class="clip caption" data-start="{round(ph["start"], 2)}" '
        f'data-duration="{round(ph["duration"], 2)}" data-track-index="2">'
        f'<div class="bubble"><p class="text">{html}</p></div></div>'
    )

# Stamps (top of screen, safely above face)
STAMPS = [
    # (id, text, side, start, duration, color)
    ("stamp-5tage", "5<br>TAGE",  "right", 5.4,  2.8, "petrol"),
    ("stamp-pia",   "🤖 PIA",    "left",  10.4, 1.4, "petrol"),
]
stamp_divs = []
for sid, text, side, start, dur, color in STAMPS:
    stamp_divs.append(
        f'<div id="{sid}" class="clip stamp stamp-{side} stamp-{color}" '
        f'data-start="{start}" data-duration="{dur}" data-track-index="3">{text}</div>'
    )

# Cut-In Card divs (track-index 50 — high so over video)
cut_divs = []
for cid, start, dur, bg, html in CUT_CARDS:
    cut_divs.append(
        f'<div id="{cid}" class="clip cut-card {bg}" data-start="{start}" data-duration="{dur}" data-track-index="50">\n{html}\n</div>'
    )

# CTA — full bottom band (Patricia still visible top half), starts at "Den Link dazu"
cta_start = next((w["start"] for w in words if w["word"].lower() in ("den", "link")), duration - 4.0)
if cta_start < 33.0: cta_start = 33.0  # ensure CTA starts AFTER 0-CHF cut-card (ends 33.0)

# === GSAP TWEENS ===
tweens = []
# Hook-Card (0 - 1.5s) — full overlay before Patricia
tweens.append('tl.fromTo("#hook-card", { opacity: 0, scale: 0.92 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(1.4)" }, 0);')
tweens.append('tl.to("#hook-card", { opacity: 0, scale: 1.05, duration: 0.4, ease: "power2.in" }, 1.1);')
tweens.append('tl.set("#hook-card", { opacity: 0 }, 1.5);')

# Caption phrases
for ph in phrases:
    s = ph["start"]
    tweens.append(f'tl.fromTo("#{ph["id"]} .bubble", {{ opacity: 0, y: 24, scale: 0.94 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.32, ease: "power3.out" }}, {s});')
    tweens.append(f'tl.fromTo("#{ph["id"]} .w", {{ opacity: 0, scale: 0.7 }}, {{ opacity: 1, scale: 1, duration: 0.22, ease: "back.out(2.5)", stagger: 0.04 }}, {s});')
    tweens.append(f'tl.fromTo("#{ph["id"]} .accent", {{}}, {{ "--hl": "100%", duration: 0.5, ease: "power2.out" }}, {s + 0.3});')
    exit_at = round(s + ph["duration"] - 0.25, 2)
    tweens.append(f'tl.to("#{ph["id"]} .bubble", {{ opacity: 0, y: -16, duration: 0.25, ease: "power2.in" }}, {exit_at});')
    tweens.append(f'tl.set("#{ph["id"]}", {{ opacity: 0 }}, {round(s + ph["duration"], 2)});')

# Stamps — pop from side
for sid, text, side, start, dur, color in STAMPS:
    side_x = -120 if side == "left" else 120
    rot_in = -15 if side == "left" else 15
    rot_end = -5 if side == "left" else 5
    tweens.append(f'tl.fromTo("#{sid}", {{ x: {side_x}, opacity: 0, scale: 0.4, rotation: {rot_in} }}, {{ x: 0, opacity: 1, scale: 1, rotation: {rot_end}, duration: 0.5, ease: "back.out(2.0)" }}, {start});')
    tweens.append(f'tl.to("#{sid}", {{ scale: 1.08, duration: 0.25, yoyo: true, repeat: 1, ease: "power1.inOut" }}, {start + 0.6});')
    tweens.append(f'tl.to("#{sid}", {{ opacity: 0, scale: 0.7, duration: 0.3, ease: "power2.in" }}, {start + dur - 0.3});')
    tweens.append(f'tl.set("#{sid}", {{ opacity: 0 }}, {start + dur});')

# Cut-In Cards — Full-screen replace Patricia with brand statement
for cid, start, dur, bg, html in CUT_CARDS:
    tweens.append(f'tl.fromTo("#{cid}", {{ opacity: 0, scale: 0.96 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "power2.out" }}, {start});')
    tweens.append(f'tl.fromTo("#{cid} > *", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.35, stagger: 0.15, ease: "back.out(1.6)" }}, {start + 0.15});')
    tweens.append(f'tl.to("#{cid}", {{ opacity: 0, duration: 0.3, ease: "power2.in" }}, {start + dur - 0.35});')
    tweens.append(f'tl.set("#{cid}", {{ opacity: 0 }}, {start + dur});')

# End-CTA — bottom card, Patricia stays visible top half
cta_dur = duration - cta_start
tweens.append(f'tl.fromTo("#cta-final", {{ y: 200, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.45, ease: "back.out(1.4)" }}, {cta_start:.2f});')
tweens.append(f'tl.fromTo("#cta-arrow-line", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.55, ease: "power2.out" }}, {cta_start + 0.5:.2f});')
tweens.append(f'tl.fromTo("#cta-arrow-head", {{ opacity: 0, x: -10 }}, {{ opacity: 1, x: 0, duration: 0.3, ease: "power2.out" }}, {cta_start + 1.0:.2f});')
tweens.append(f'tl.to("#cta-final .pop", {{ scale: 1.08, duration: 0.35, yoyo: true, repeat: 3, ease: "power1.inOut" }}, {cta_start + 1.4:.2f});')

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
        --petrol: #12828c; --dunkelblau: #29556d; --creme: #f1ecdd; --orange: #dc822e; --text: #0c1c30;
      }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #000; font-family: "Source Sans 3", sans-serif; color: var(--text); }}
      #bg-video {{ position: absolute; inset: 0; width: 1080px; height: 1920px; object-fit: cover; }}

      /* === HOOK-CARD === */
      #hook-card {{
        position: absolute; inset: 0; background: var(--creme);
        display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center;
        padding: 80px; z-index: 50;
      }}
      #hook-card .flame {{ font-size: 140px; margin-bottom: 16px; }}
      #hook-card .label {{ font-family: "Source Sans 3"; font-weight: 700; font-size: 48px; color: var(--petrol); letter-spacing: 0.16em; text-transform: uppercase; margin-bottom: 28px; }}
      #hook-card .title {{ font-family: "Philosopher"; font-weight: 700; font-size: 168px; line-height: 0.95; color: var(--dunkelblau); margin-bottom: 40px; }}
      #hook-card .title .pop {{ color: var(--petrol); font-style: italic; }}
      #hook-card .date {{ font-family: "Source Sans 3"; font-weight: 700; font-size: 84px; color: var(--petrol); background: #fff; padding: 18px 48px; border-radius: 22px; box-shadow: 0 14px 36px rgba(18, 130, 140, 0.3); }}

      /* === CAPTIONS — BOTTOM ONLY (safe-zone) === */
      .caption {{
        position: absolute; left: 60px; right: 60px;
        bottom: 280px;  /* under chest/shoulders, above brand-footer */
        display: flex; justify-content: center;
      }}
      .bubble {{
        background: var(--creme); padding: 32px 44px; border-radius: 26px;
        box-shadow: 0 14px 36px rgba(12, 28, 48, 0.32);
        max-width: 960px; text-align: center;
      }}
      .bubble .text {{ font-family: "Source Sans 3"; font-weight: 600; font-size: 56px; line-height: 1.25; color: var(--text); }}
      .bubble .marker {{ display: inline-block; margin-right: 8px; }}
      .bubble .w {{ display: inline-block; margin-right: 0.18em; }}
      .bubble .w.accent {{ position: relative; color: var(--petrol); font-weight: 700; --hl: 0%; }}
      .bubble .w.accent::after {{ content: ""; position: absolute; left: -4px; bottom: 2px; width: var(--hl); height: 14px; background: rgba(220, 130, 46, 0.45); z-index: -1; border-radius: 4px; }}

      /* === STAMPS — TOP CORNERS (above face) === */
      .stamp {{
        position: absolute;
        font-family: "Philosopher"; font-weight: 700; line-height: 1; text-align: center;
        padding: 24px 36px; border-radius: 18px;
        box-shadow: 0 16px 40px rgba(0, 0, 0, 0.35);
      }}
      .stamp-petrol {{ background: var(--petrol); color: #fff; }}
      .stamp-orange {{ background: var(--orange); color: #fff; }}
      .stamp-left   {{ left: 40px;  top: 150px; font-size: 76px; }}
      .stamp-right  {{ right: 40px; top: 150px; font-size: 92px; }}

      /* === CUT-IN CARDS — FULL-SCREEN REPLACE === */
      .cut-card {{
        position: absolute; inset: 0;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        padding: 80px; text-align: center;
      }}
      .bg-creme  {{ background: var(--creme); color: var(--text); }}
      .bg-orange {{ background: var(--orange); color: #fff; }}
      .cut-label {{ font-family: "Source Sans 3"; font-weight: 700; font-size: 56px; color: var(--petrol); letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 80px; }}
      .cut-label-white {{ font-family: "Source Sans 3"; font-weight: 700; font-size: 96px; color: #fff; margin-bottom: 30px; }}
      .cut-no-row {{ display: flex; align-items: center; gap: 40px; margin-bottom: 40px; }}
      .cut-x {{ font-size: 100px; }}
      .cut-no-text {{ font-family: "Philosopher"; font-weight: 700; font-size: 96px; color: var(--text); line-height: 1; }}
      .cut-huge-zero {{ font-family: "Philosopher"; font-weight: 700; font-size: 720px; line-height: 0.85; color: #fff; position: relative; display: inline-block; }}
      .cut-chf {{ position: absolute; top: 80px; right: -200px; font-size: 96px; transform: rotate(8deg); background: #fff; color: var(--orange); padding: 10px 28px; border-radius: 16px; }}

      /* === END-CTA — BOTTOM BAND (face stays visible top) === */
      #cta-final {{
        position: absolute;
        left: 60px; right: 60px;
        bottom: 100px;
        background: var(--creme);
        padding: 56px 72px;
        border-radius: 36px;
        box-shadow: 0 24px 60px rgba(12, 28, 48, 0.45);
        text-align: center;
        z-index: 60;
      }}
      #cta-final .label {{ font-family: "Source Sans 3"; font-weight: 700; font-size: 36px; letter-spacing: 0.16em; text-transform: uppercase; color: var(--petrol); margin-bottom: 18px; }}
      #cta-final .headline {{ font-family: "Philosopher"; font-weight: 700; font-size: 92px; line-height: 1.05; color: var(--dunkelblau); margin-bottom: 24px; }}
      #cta-final .headline .pop {{ color: var(--petrol); font-style: italic; display: inline-block; transform-origin: center; }}
      #cta-arrow {{ display: flex; align-items: center; justify-content: center; gap: 10px; height: 50px; }}
      #cta-arrow-line {{ width: 220px; height: 8px; background: var(--petrol); border-radius: 4px; transform-origin: left center; }}
      #cta-arrow-head {{ width: 0; height: 0; border-top: 22px solid transparent; border-bottom: 22px solid transparent; border-left: 34px solid var(--petrol); }}

      /* === BRAND-FOOTER === */
      .brand-footer {{ position: absolute; top: 30px; left: 0; right: 0; text-align: center; font-family: "Philosopher"; font-weight: 700; font-size: 26px; color: #fff; text-shadow: 0 2px 8px rgba(0, 0, 0, 0.7); letter-spacing: 0.1em; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{duration:.2f}" data-width="1080" data-height="1920">

      <video id="bg-video" class="clip" data-start="0" data-duration="{duration:.2f}" data-track-index="1" src="{VIDEO}" muted playsinline></video>
      <audio id="audio-track" class="clip" data-start="0" data-duration="{duration:.2f}" data-track-index="0" src="{VIDEO}"></audio>

      <div id="hook-card" class="clip" data-start="0" data-duration="1.5" data-track-index="50">
        <div class="flame">🔥</div>
        <div class="label">Bootcamp</div>
        <div class="title">5 Tage<br /><span class="pop">Klarheit.</span></div>
        <div class="date">29.6. – 3.7.</div>
      </div>

      <div id="brand-footer" class="clip brand-footer" data-start="0" data-duration="{duration:.2f}" data-track-index="70">@mum.life.balance</div>

      {chr(10).join("      " + d for d in caption_divs)}

      {chr(10).join("      " + d for d in stamp_divs)}

      {chr(10).join("      " + d for d in cut_divs)}

      <div id="cta-final" class="clip" data-start="{cta_start:.2f}" data-duration="{cta_dur:.2f}" data-track-index="60">
        <div class="label">Anmeldung</div>
        <div class="headline">Link in <span class="pop">der Bio.</span></div>
        <div id="cta-arrow">
          <div id="cta-arrow-line"></div>
          <div id="cta-arrow-head"></div>
        </div>
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
print(f"Duration: {duration:.2f}s · Phrases: {len(phrases)} · Cut-Cards: {len(CUT_CARDS)} · Stamps: {len(STAMPS)}")
