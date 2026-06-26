#!/usr/bin/env python3
"""
Variant C — Voll-Edit Liane-Level: 36-Sek-Reel mit Patricia + 5 Full-Screen-Brand-Cards.
Patricia ist in ~4 Cuts à 3-4 Sek sichtbar (statt 36 Sek am Stück).
Brand-Cards überlagern Patricia in den Lücken — Audio läuft durch.
Pace: alle 2-3 Sek ein neues Visual.
Safe-Zone: alle Captions/Stamps OUTSIDE face (Captions bottom, Stamps top-corner).
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent
TRANSCRIPT = ROOT / "assets" / "talking-head.json"
VIDEO = "assets/talking-head.mp4"
OUTPUT = ROOT / "index.html"

ACCENT = {"pia", "kostenlos", "bio", "klaren", "ersten", "kein", "keine"}

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

words = load_words()
duration = max(w["end"] for w in words) + 0.5

# === CUT-IN BRAND CARDS (over Patricia, audio läuft durch) ===
CUT_CARDS = [
    # (id, start, duration, bg-class, html)
    ("cut-hook", 0.0, 1.6, "bg-creme", '''
        <div class="big-flame">🔥</div>
        <div class="cut-label">Bootcamp</div>
        <div class="cut-title">5 Tage<br/><span class="italic-pop">Klarheit.</span></div>
        <div class="date-pill">29.6. – 3.7.</div>
    '''),

    ("cut-datum", 5.4, 3.0, "bg-petrol", '''
        <div class="cut-label-white">Live vom</div>
        <div class="huge-date">29.6.<br/>—<br/>3.7.</div>
    '''),

    ("cut-no-list", 12.3, 5.0, "bg-creme", '''
        <div class="cut-label">Du brauchst nicht:</div>
        <div class="cut-no-row"><span class="cut-x">❌</span> <span class="cut-no-text">Webinar</span></div>
        <div class="cut-no-row"><span class="cut-x">❌</span> <span class="cut-no-text">Strategie&shy;-Power-Hour</span></div>
        <div class="cut-no-row"><span class="cut-x">❌</span> <span class="cut-no-text">Studium</span></div>
    '''),

    ("cut-ja-list", 17.4, 5.0, "bg-petrol", '''
        <div class="cut-label-white">Du brauchst nur:</div>
        <div class="cut-yes-row"><span class="cut-y">✅</span> <span class="cut-yes-text">5 Tage</span></div>
        <div class="cut-yes-row"><span class="cut-y">✅</span> <span class="cut-yes-text">1 Sprachnotiz/Tag</span></div>
        <div class="cut-yes-row"><span class="cut-y">✅</span> <span class="cut-yes-text">PIA</span></div>
    '''),

    ("cut-pia-name", 22.5, 3.5, "bg-creme", '''
        <div class="cut-label">Mit deiner KI-Mentorin</div>
        <div class="pia-mega">PIA<span class="pia-dot">.</span></div>
        <div class="cut-subline">Sie baut deine Bio. Deine Hooks.<br/>Deine Wochenstruktur.</div>
    '''),

    ("cut-kostenlos", 30.0, 2.8, "bg-orange", '''
        <div class="cut-label-white">Das Ganze</div>
        <div class="cut-huge-zero">0<span class="cut-chf">CHF</span></div>
    '''),
]

# Patricia-visible windows (between cards) — these get captions
# Window: (start, end, label_prefix)
PATRICIA_WINDOWS = [
    (1.6, 5.4),    # "Vom 29. Juli bis zum 3. Juli"
    (8.4, 12.3),   # "mache ich mit dir in fünf Tagen deinen ersten klaren"
    (26.0, 30.0),  # "die dann dazu führt, dass du nach den Sommerferien richtig durchstarten kannst."
    (32.8, 33.5),  # tiny bridge to CTA
]

# Build captions: only words inside Patricia-windows get caption-bubbles
def words_in_window(start, end):
    return [w for w in words if w["start"] >= start - 0.05 and w["end"] <= end + 0.2]

def render_words_html(ws):
    spans = []
    for w in ws:
        cls = "w accent" if is_accent(w["word"]) else "w"
        spans.append(f'<span class="{cls}">{w["word"]}</span>')
    out = " ".join(spans)
    out = out.replace(' <span class="w">-', '<span class="w">-').replace(' <span class="w accent">-', '<span class="w accent">-')
    return out

captions = []
for i, (ws_start, ws_end) in enumerate(PATRICIA_WINDOWS):
    win_words = words_in_window(ws_start, ws_end)
    if not win_words: continue
    # split into max 5-word chunks
    chunks = []
    cur = []
    for w in win_words:
        cur.append(w)
        if len(cur) >= 5 or w["word"].rstrip().endswith((".", ",")):
            chunks.append(cur); cur = []
    if cur: chunks.append(cur)
    for j, chunk in enumerate(chunks):
        next_chunk_start = chunks[j+1][0]["start"] if j+1 < len(chunks) else ws_end
        s = chunk[0]["start"]
        e = min(chunk[-1]["end"] + 0.3, next_chunk_start - 0.05, ws_end - 0.05)
        if e - s < 0.4: continue
        captions.append({
            "id": f"cap-w{i}-{j}",
            "start": round(s, 2),
            "duration": round(e - s, 2),
            "html": render_words_html(chunk),
        })

# === STAMPS (only during Patricia visible windows, top corners) ===
STAMPS = [
    ("stamp-5tage", "5<br>TAGE",  "right", 4.4,  1.0, "petrol"),  # during "fünf Tagen"
]

# === END-CTA (Bottom card after cut-kostenlos ends at 32.8) ===
cta_start = 32.9
cta_dur = duration - cta_start

caption_divs = [
    f'<div id="{c["id"]}" class="clip caption" data-start="{c["start"]}" '
    f'data-duration="{c["duration"]}" data-track-index="2">'
    f'<div class="bubble"><p class="text">{c["html"]}</p></div></div>'
    for c in captions
]

cut_divs = []
for cid, start, dur, bg, html in CUT_CARDS:
    cut_divs.append(
        f'<div id="{cid}" class="clip cut-card {bg}" data-start="{start}" data-duration="{dur}" data-track-index="50">\n{html}\n</div>'
    )

stamp_divs = []
for sid, text, side, start, dur, color in STAMPS:
    stamp_divs.append(
        f'<div id="{sid}" class="clip stamp stamp-{side} stamp-{color}" '
        f'data-start="{start}" data-duration="{dur}" data-track-index="3">{text}</div>'
    )

# === GSAP TWEENS ===
tweens = []
for cid, start, dur, bg, html in CUT_CARDS:
    tweens.append(f'tl.fromTo("#{cid}", {{ opacity: 0, scale: 0.96 }}, {{ opacity: 1, scale: 1, duration: 0.28, ease: "power2.out" }}, {start});')
    tweens.append(f'tl.fromTo("#{cid} > *", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.32, stagger: 0.12, ease: "back.out(1.6)" }}, {start + 0.1});')
    tweens.append(f'tl.to("#{cid}", {{ opacity: 0, duration: 0.3, ease: "power2.in" }}, {start + dur - 0.35});')
    tweens.append(f'tl.set("#{cid}", {{ opacity: 0 }}, {start + dur});')

for c in captions:
    s = c["start"]
    tweens.append(f'tl.fromTo("#{c["id"]} .bubble", {{ opacity: 0, y: 24, scale: 0.94 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.3, ease: "power3.out" }}, {s});')
    tweens.append(f'tl.fromTo("#{c["id"]} .w", {{ opacity: 0, scale: 0.7 }}, {{ opacity: 1, scale: 1, duration: 0.22, ease: "back.out(2.5)", stagger: 0.04 }}, {s});')
    tweens.append(f'tl.fromTo("#{c["id"]} .accent", {{}}, {{ "--hl": "100%", duration: 0.5, ease: "power2.out" }}, {s + 0.3});')
    exit_at = round(s + c["duration"] - 0.2, 2)
    tweens.append(f'tl.to("#{c["id"]} .bubble", {{ opacity: 0, y: -16, duration: 0.2, ease: "power2.in" }}, {exit_at});')
    tweens.append(f'tl.set("#{c["id"]}", {{ opacity: 0 }}, {round(s + c["duration"], 2)});')

for sid, text, side, start, dur, color in STAMPS:
    side_x = -120 if side == "left" else 120
    rot_in = -15 if side == "left" else 15
    rot_end = -5 if side == "left" else 5
    tweens.append(f'tl.fromTo("#{sid}", {{ x: {side_x}, opacity: 0, scale: 0.4, rotation: {rot_in} }}, {{ x: 0, opacity: 1, scale: 1, rotation: {rot_end}, duration: 0.4, ease: "back.out(2.0)" }}, {start});')
    tweens.append(f'tl.to("#{sid}", {{ opacity: 0, scale: 0.7, duration: 0.25, ease: "power2.in" }}, {start + dur - 0.25});')
    tweens.append(f'tl.set("#{sid}", {{ opacity: 0 }}, {start + dur});')

# End-CTA
tweens.append(f'tl.fromTo("#cta-final", {{ y: 100, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.4, ease: "back.out(1.4)" }}, {cta_start:.2f});')
tweens.append(f'tl.fromTo("#cta-arrow-line", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.5, ease: "power2.out" }}, {cta_start + 0.45:.2f});')
tweens.append(f'tl.fromTo("#cta-arrow-head", {{ opacity: 0, x: -10 }}, {{ opacity: 1, x: 0, duration: 0.3, ease: "power2.out" }}, {cta_start + 0.9:.2f});')
tweens.append(f'tl.to("#cta-final .pop", {{ scale: 1.08, duration: 0.35, yoyo: true, repeat: 3, ease: "power1.inOut" }}, {cta_start + 1.2:.2f});')

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

      /* CUT-IN CARDS */
      .cut-card {{
        position: absolute; inset: 0;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        padding: 80px; text-align: center;
      }}
      .bg-creme  {{ background: var(--creme); color: var(--text); }}
      .bg-petrol {{ background: var(--petrol); color: #fff; }}
      .bg-orange {{ background: var(--orange); color: #fff; }}

      /* Cut-Card content styles */
      .big-flame {{ font-size: 140px; margin-bottom: 16px; }}
      .cut-label {{ font-family: "Source Sans 3"; font-weight: 700; font-size: 56px; color: var(--petrol); letter-spacing: 0.12em; text-transform: uppercase; margin-bottom: 36px; }}
      .cut-label-white {{ font-family: "Source Sans 3"; font-weight: 700; font-size: 64px; color: #fff; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 36px; }}
      .cut-title {{ font-family: "Philosopher"; font-weight: 700; font-size: 168px; line-height: 0.95; color: var(--dunkelblau); margin-bottom: 40px; }}
      .italic-pop {{ color: var(--petrol); font-style: italic; }}
      .date-pill {{ background: #fff; color: var(--petrol); padding: 18px 48px; border-radius: 22px; font-family: "Source Sans 3"; font-weight: 700; font-size: 84px; box-shadow: 0 14px 36px rgba(18, 130, 140, 0.3); }}
      .huge-date {{ font-family: "Philosopher"; font-weight: 700; font-style: italic; font-size: 220px; line-height: 1.05; color: #fff; }}
      .cut-no-row, .cut-yes-row {{ display: flex; align-items: center; gap: 36px; margin-bottom: 36px; }}
      .cut-x {{ font-size: 88px; }}
      .cut-y {{ font-size: 88px; }}
      .cut-no-text {{ font-family: "Philosopher"; font-weight: 700; font-size: 88px; color: var(--text); line-height: 1; }}
      .cut-yes-text {{ font-family: "Philosopher"; font-weight: 700; font-size: 96px; color: #fff; line-height: 1; }}
      .pia-mega {{ font-family: "Philosopher"; font-weight: 700; font-size: 360px; line-height: 1; color: var(--petrol); letter-spacing: -0.02em; margin-bottom: 28px; }}
      .pia-dot {{ color: var(--orange); }}
      .cut-subline {{ font-family: "Source Sans 3"; font-weight: 400; font-size: 44px; line-height: 1.3; color: var(--text); opacity: 0.8; max-width: 860px; }}
      .cut-huge-zero {{ font-family: "Philosopher"; font-weight: 700; font-size: 720px; line-height: 0.85; color: #fff; position: relative; display: inline-block; }}
      .cut-chf {{ position: absolute; top: 80px; right: -200px; font-size: 96px; transform: rotate(8deg); background: #fff; color: var(--orange); padding: 10px 28px; border-radius: 16px; }}

      /* CAPTIONS — bottom safe-zone */
      .caption {{ position: absolute; left: 60px; right: 60px; bottom: 240px; display: flex; justify-content: center; }}
      .bubble {{ background: var(--creme); padding: 30px 44px; border-radius: 24px; box-shadow: 0 14px 36px rgba(12, 28, 48, 0.32); max-width: 960px; text-align: center; }}
      .bubble .text {{ font-family: "Source Sans 3"; font-weight: 600; font-size: 54px; line-height: 1.22; color: var(--text); }}
      .bubble .w {{ display: inline-block; margin-right: 0.18em; }}
      .bubble .w.accent {{ position: relative; color: var(--petrol); font-weight: 700; --hl: 0%; }}
      .bubble .w.accent::after {{ content: ""; position: absolute; left: -4px; bottom: 2px; width: var(--hl); height: 12px; background: rgba(220, 130, 46, 0.45); z-index: -1; border-radius: 4px; }}

      /* STAMPS — top corner */
      .stamp {{ position: absolute; font-family: "Philosopher"; font-weight: 700; line-height: 1; text-align: center; padding: 24px 36px; border-radius: 18px; box-shadow: 0 16px 40px rgba(0, 0, 0, 0.35); }}
      .stamp-petrol {{ background: var(--petrol); color: #fff; }}
      .stamp-orange {{ background: var(--orange); color: #fff; }}
      .stamp-left  {{ left: 40px; top: 150px; font-size: 76px; }}
      .stamp-right {{ right: 40px; top: 150px; font-size: 92px; }}

      /* END-CTA — bottom band */
      #cta-final {{
        position: absolute; left: 60px; right: 60px; bottom: 100px;
        background: var(--creme); padding: 50px 72px; border-radius: 32px;
        box-shadow: 0 24px 60px rgba(12, 28, 48, 0.45); text-align: center; z-index: 60;
      }}
      #cta-final .label {{ font-family: "Source Sans 3"; font-weight: 700; font-size: 34px; letter-spacing: 0.16em; text-transform: uppercase; color: var(--petrol); margin-bottom: 16px; }}
      #cta-final .headline {{ font-family: "Philosopher"; font-weight: 700; font-size: 88px; line-height: 1.05; color: var(--dunkelblau); margin-bottom: 22px; }}
      #cta-final .headline .pop {{ color: var(--petrol); font-style: italic; display: inline-block; transform-origin: center; }}
      #cta-arrow {{ display: flex; align-items: center; justify-content: center; gap: 10px; height: 50px; }}
      #cta-arrow-line {{ width: 220px; height: 8px; background: var(--petrol); border-radius: 4px; transform-origin: left center; }}
      #cta-arrow-head {{ width: 0; height: 0; border-top: 22px solid transparent; border-bottom: 22px solid transparent; border-left: 34px solid var(--petrol); }}

      .brand-footer {{ position: absolute; top: 30px; left: 0; right: 0; text-align: center; font-family: "Philosopher"; font-weight: 700; font-size: 24px; color: #fff; text-shadow: 0 2px 8px rgba(0, 0, 0, 0.7); letter-spacing: 0.1em; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{duration:.2f}" data-width="1080" data-height="1920">

      <video id="bg-video" class="clip" data-start="0" data-duration="{duration:.2f}" data-track-index="1" src="{VIDEO}" muted playsinline></video>
      <audio id="audio-track" class="clip" data-start="0" data-duration="{duration:.2f}" data-track-index="0" src="{VIDEO}"></audio>

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
print(f"Duration: {duration:.2f}s · Cut-Cards: {len(CUT_CARDS)} · Captions: {len(captions)} · Stamps: {len(STAMPS)} · Patricia visible windows: {len(PATRICIA_WINDOWS)}")
