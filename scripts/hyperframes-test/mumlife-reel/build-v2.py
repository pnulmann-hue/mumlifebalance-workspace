#!/usr/bin/env python3
"""
V2 Builder — Liane-Meusel-Style Talking-Head-Reel:
  - Hook-Card overlay (0-1.2s) BEFORE Patricia appears
  - Word-by-word stagger reveal in caption bubbles
  - Highlighter-Sweep under accent words (Petrol underline animation)
  - 3 Section positions: bottom / top (with ❌-Liste) / center (with ✅-Liste)
  - Pop-Stamps for key moments: 5 TAGE, PIA, 0 CHF
  - End-CTA with drawing-arrow + pulse on "Bio"
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
TRANSCRIPT = ROOT / "assets" / "talking-head.json"
VIDEO = "assets/talking-head.mp4"
OUTPUT = ROOT / "index.html"

ACCENT = {
    "pia", "ki-mentorin", "kostenlos", "bio", "bootcamp",
    "29.", "3.", "juni", "juli", "5", "fünf",
    "klaren", "ersten", "kein", "keine", "kostenlos.",
}

def strip_word(w):
    return w.strip()

def is_accent(w):
    clean = re.sub(r"[^\wäöüÄÖÜß-]", "", w).lower()
    return clean in ACCENT

def load_words():
    data = json.loads(TRANSCRIPT.read_text(encoding="utf-8"))
    words = []
    for seg in data["segments"]:
        for w in seg.get("words", []):
            words.append({
                "word": strip_word(w["word"]),
                "start": w["start"],
                "end": w["end"],
            })
    return words

# ====== SECTION DEFINITION ======
# Manual chunking: each phrase = one bubble that appears as a unit (with word-by-word stagger inside).
# Position rotates: bottom → top → center → bottom → ...
# Negative-List uses ❌, Positive-List uses ✅

def build_phrases(words):
    """Group words into phrases with explicit boundaries (manual cuts for narrative)."""
    # Manual boundaries by word-index (inclusive end)
    boundaries = [
        # (start_idx, end_idx, position, list_marker, label)
        # ALL captions BOTTOM only (out of face zone). Top only used for stamps.
        (0, 6,   "bottom", None,  "p1"),
        (7, 13,  "bottom", None,  "p2"),
        (14, 21, "bottom", None,  "p3"),
        (22, 28, "bottom", None,  "p4"),
        (29, 33, "bottom", "❌",   "p5"),
        (34, 36, "bottom", "❌",   "p6"),
        (37, 39, "bottom", "❌",   "p7"),
        (40, 43, "bottom", "✅",   "p8"),
        (44, 49, "bottom", "✅",   "p9"),
        (50, 54, "bottom", "✅",   "p10"),
        (55, 59, "bottom", "✅",   "p11"),
        (60, 63, "bottom", "✅",   "p12"),
        (64, 68, "bottom", None,  "p13"),
        (69, 71, "bottom", None,  "p14"),
        (72, 75, "bottom", None,  "p15"),
    ]
    phrases = []
    for start_i, end_i, pos, marker, label in boundaries:
        chunk = words[start_i:end_i + 1]
        if not chunk:
            continue
        phrases.append({
            "id": label,
            "words": chunk,
            "start": chunk[0]["start"],
            "end": chunk[-1]["end"],
            "position": pos,
            "marker": marker,
        })
    return phrases

def render_phrase_html(phrase):
    """Render words as individual spans for staggered animation. Mark accent words."""
    spans = []
    for w in phrase["words"]:
        word = w["word"]
        cls = "w"
        if is_accent(word):
            cls = "w accent"
        # Avoid leading space before hyphen-fragments
        spans.append(f'<span class="{cls}">{word}</span>')
    return " ".join(spans).replace(" <span class=\"w\">-", "<span class=\"w\">-").replace(" <span class=\"w accent\">-", "<span class=\"w accent\">-")

def main():
    words = load_words()
    phrases = build_phrases(words)
    duration = max(w["end"] for w in words) + 0.8
    print(f"Duration: {duration:.2f}s · Phrases: {len(phrases)}")

    # --- Render phrase HTML ---
    phrase_html = []
    for p in phrases:
        marker_html = f'<span class="marker">{p["marker"]}</span> ' if p["marker"] else ""
        # Phrase visible until NEXT phrase begins (cap to avoid overlap on same track)
        next_phrase = next((x for x in phrases if x["start"] > p["start"]), None)
        end_fade = (next_phrase["start"] - 0.05) if next_phrase else (p["end"] + 0.6)
        dur = max(end_fade - p["start"], 0.6)
        phrase_html.append({
            "id": p["id"],
            "start": round(p["start"], 2),
            "duration": round(dur, 2),
            "html": f'{marker_html}{render_phrase_html(p)}',
            "position": p["position"],
            "word_count": len(p["words"]),
        })

    # Render caption divs
    caption_divs = []
    for ph in phrase_html:
        caption_divs.append(
            f'<div id="{ph["id"]}" class="clip caption pos-{ph["position"]}" '
            f'data-start="{ph["start"]}" data-duration="{ph["duration"]}" data-track-index="2">'
            f'<div class="bubble"><p class="text">{ph["html"]}</p></div></div>'
        )

    # Stamps with timestamps from transcript
    stamps_definitions = [
        # (id, text, side, start, duration, color)
        ("stamp-5tage", "5<br>TAGE",        "right", 5.4,  2.5, "petrol"),
        ("stamp-pia",   "🤖 PIA",           "left",  10.4, 2.5, "petrol"),
        ("stamp-0chf",  "0<br>CHF",         "right", 30.5, 3.0, "orange"),
    ]
    stamp_divs = []
    for sid, text, side, start, dur, color in stamps_definitions:
        stamp_divs.append(
            f'<div id="{sid}" class="clip stamp stamp-{side} stamp-{color}" '
            f'data-start="{start}" data-duration="{dur}" data-track-index="3">{text}</div>'
        )

    # Build GSAP tweens
    tweens = []
    # Hook-Card (0-1.2s): full brand-card OVER video
    tweens.append('tl.fromTo("#hook-card", { opacity: 0, scale: 0.92 }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(1.4)" }, 0);')
    tweens.append('tl.to("#hook-card", { opacity: 0, scale: 1.05, duration: 0.4, ease: "power2.in" }, 1.1);')
    tweens.append('tl.set("#hook-card", { opacity: 0 }, 1.5);')

    # Caption phrases — word-by-word stagger inside bubble
    for ph in phrase_html:
        # Bubble itself slides + fades in
        tweens.append(f'tl.fromTo("#{ph["id"]} .bubble", '
                      f'{{ opacity: 0, y: 24, scale: 0.94 }}, '
                      f'{{ opacity: 1, y: 0, scale: 1, duration: 0.32, ease: "power3.out" }}, {ph["start"]});')
        # Words stagger inside bubble — STARTS PARALLEL to bubble fadeIn (no offset → no empty-bubble moment)
        tweens.append(f'tl.fromTo("#{ph["id"]} .w", '
                      f'{{ opacity: 0, scale: 0.7 }}, '
                      f'{{ opacity: 1, scale: 1, duration: 0.22, ease: "back.out(2.5)", stagger: 0.04 }}, {ph["start"]});')
        # Accent words: highlighter-sweep (animate underline width 0 → 100%)
        tweens.append(f'tl.fromTo("#{ph["id"]} .accent::after, #{ph["id"]} .accent", '
                      f'{{}}, {{ "--hl": "100%", duration: 0.5, ease: "power2.out" }}, {ph["start"] + 0.3});')
        # Exit: fade
        exit_at = round(ph["start"] + ph["duration"] - 0.25, 2)
        tweens.append(f'tl.to("#{ph["id"]} .bubble", {{ opacity: 0, y: -16, duration: 0.25, ease: "power2.in" }}, {exit_at});')
        tweens.append(f'tl.set("#{ph["id"]}", {{ opacity: 0 }}, {round(ph["start"] + ph["duration"], 2)});')

    # Stamps — pop in from side with rotate+scale
    for sid, text, side, start, dur, color in stamps_definitions:
        side_x = -150 if side == "left" else 150
        tweens.append(f'tl.fromTo("#{sid}", '
                      f'{{ x: {side_x}, opacity: 0, scale: 0.4, rotation: {-15 if side == "left" else 15} }}, '
                      f'{{ x: 0, opacity: 1, scale: 1, rotation: {-6 if side == "left" else 6}, duration: 0.5, ease: "back.out(2.0)" }}, {start});')
        # Pulse
        tweens.append(f'tl.to("#{sid}", {{ scale: 1.08, duration: 0.25, yoyo: true, repeat: 1, ease: "power1.inOut" }}, {start + 0.6});')
        # Exit
        tweens.append(f'tl.to("#{sid}", {{ opacity: 0, scale: 0.7, duration: 0.3, ease: "power2.in" }}, {start + dur - 0.3});')
        tweens.append(f'tl.set("#{sid}", {{ opacity: 0 }}, {start + dur});')

    # End-CTA timed to "Den Link dazu findest du in meiner Bio." — starts when Patricia says "Den"
    # word index 76 = "Den" (start ≈ 32s); CTA covers remaining audio
    cta_start_word = next((w for w in words if w["word"].lower() in ("den", "link")), None)
    cta_start = cta_start_word["start"] if cta_start_word and cta_start_word["start"] > 30 else (duration - 4.0)
    tweens.append(f'tl.fromTo("#cta-final", '
                  f'{{ scale: 0.85, opacity: 0 }}, '
                  f'{{ scale: 1, opacity: 1, duration: 0.45, ease: "back.out(1.6)" }}, {cta_start:.2f});')
    tweens.append(f'tl.fromTo("#cta-arrow-line", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.55, ease: "power2.out" }}, {cta_start + 0.45:.2f});')
    tweens.append(f'tl.fromTo("#cta-arrow-head", {{ opacity: 0, x: -10 }}, {{ opacity: 1, x: 0, duration: 0.3, ease: "power2.out" }}, {cta_start + 0.95:.2f});')
    tweens.append(f'tl.to("#cta-final .pop", {{ scale: 1.08, duration: 0.35, yoyo: true, repeat: 3, ease: "power1.inOut" }}, {cta_start + 1.3:.2f});')

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
      html, body {{
        width: 1080px; height: 1920px; overflow: hidden;
        background: #000;
        font-family: "Source Sans 3", sans-serif;
        color: var(--text);
      }}
      #bg-video {{
        position: absolute; inset: 0;
        width: 1080px; height: 1920px;
        object-fit: cover;
      }}

      /* ===== HOOK-CARD (overlay first 1.2s) ===== */
      #hook-card {{
        position: absolute;
        inset: 0;
        background: var(--creme);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        padding: 80px;
        z-index: 50;
      }}
      #hook-card .flame {{ font-size: 120px; margin-bottom: 20px; }}
      #hook-card .label {{
        font-family: "Source Sans 3", sans-serif;
        font-weight: 700;
        font-size: 48px;
        color: var(--petrol);
        letter-spacing: 0.16em;
        text-transform: uppercase;
        margin-bottom: 32px;
      }}
      #hook-card .title {{
        font-family: "Philosopher", serif;
        font-weight: 700;
        font-size: 156px;
        line-height: 0.95;
        color: var(--dunkelblau);
        margin-bottom: 40px;
      }}
      #hook-card .title .pop {{
        color: var(--petrol);
        font-style: italic;
      }}
      #hook-card .date {{
        font-family: "Source Sans 3", sans-serif;
        font-weight: 700;
        font-size: 80px;
        color: var(--petrol);
        background: #fff;
        padding: 16px 48px;
        border-radius: 20px;
        box-shadow: 0 12px 32px rgba(18, 130, 140, 0.25);
      }}

      /* ===== CAPTION (3 positions) ===== */
      .caption {{
        position: absolute;
        left: 60px;
        right: 60px;
        display: flex;
        justify-content: center;
      }}
      .caption.pos-bottom {{ bottom: 280px; }}
      .caption.pos-top    {{ top: 360px; }}
      .caption.pos-center {{ top: 50%; transform: translateY(-50%); }}

      .bubble {{
        background: var(--creme);
        padding: 32px 44px;
        border-radius: 26px;
        box-shadow: 0 14px 36px rgba(12, 28, 48, 0.28);
        max-width: 960px;
        text-align: center;
      }}
      .bubble .text {{
        font-family: "Source Sans 3", sans-serif;
        font-weight: 600;
        font-size: 56px;
        line-height: 1.25;
        color: var(--text);
      }}
      .bubble .marker {{
        display: inline-block;
        margin-right: 8px;
      }}
      .bubble .w {{
        display: inline-block;
        margin-right: 0.18em;
      }}

      /* Accent words: highlighter-sweep + pop color */
      .bubble .w.accent {{
        position: relative;
        color: var(--petrol);
        font-weight: 700;
        --hl: 0%;
      }}
      .bubble .w.accent::after {{
        content: "";
        position: absolute;
        left: -4px;
        bottom: 2px;
        width: var(--hl);
        height: 14px;
        background: rgba(220, 130, 46, 0.45); /* orange highlighter */
        z-index: -1;
        border-radius: 4px;
      }}

      /* ===== STAMPS (side-pop) ===== */
      .stamp {{
        position: absolute;
        font-family: "Philosopher", serif;
        font-weight: 700;
        line-height: 1;
        text-align: center;
        padding: 24px 36px;
        border-radius: 18px;
        box-shadow: 0 16px 40px rgba(0, 0, 0, 0.3);
      }}
      .stamp-petrol {{ background: var(--petrol); color: #fff; }}
      .stamp-orange {{ background: var(--orange); color: #fff; }}
      .stamp-left   {{ left: 50px;  top: 700px; font-size: 80px; }}
      .stamp-right  {{ right: 50px; top: 700px; font-size: 96px; }}

      /* ===== END-CTA ===== */
      #cta-final {{
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: var(--creme);
        padding: 80px 96px 100px;
        border-radius: 36px;
        box-shadow: 0 24px 60px rgba(12, 28, 48, 0.4);
        text-align: center;
        max-width: 920px;
        z-index: 60;
      }}
      #cta-final .label {{
        font-family: "Source Sans 3", sans-serif;
        font-weight: 700;
        font-size: 38px;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        color: var(--petrol);
        margin-bottom: 24px;
      }}
      #cta-final .headline {{
        font-family: "Philosopher", serif;
        font-weight: 700;
        font-size: 108px;
        line-height: 1.05;
        color: var(--dunkelblau);
        margin-bottom: 36px;
      }}
      #cta-final .headline .pop {{
        color: var(--petrol);
        font-style: italic;
        display: inline-block;
        transform-origin: center;
      }}
      #cta-arrow {{
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        height: 60px;
      }}
      #cta-arrow-line {{
        width: 240px;
        height: 8px;
        background: var(--petrol);
        border-radius: 4px;
        transform-origin: left center;
      }}
      #cta-arrow-head {{
        width: 0; height: 0;
        border-top: 24px solid transparent;
        border-bottom: 24px solid transparent;
        border-left: 36px solid var(--petrol);
      }}

      /* ===== BRAND-FOOTER ===== */
      .brand-footer {{
        position: absolute;
        bottom: 60px;
        left: 0; right: 0;
        text-align: center;
        font-family: "Philosopher", serif;
        font-weight: 700;
        font-size: 28px;
        color: #fff;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.7);
        letter-spacing: 0.1em;
      }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{duration:.2f}" data-width="1080" data-height="1920">

      <video id="bg-video" class="clip" data-start="0" data-duration="{duration:.2f}" data-track-index="1" src="{VIDEO}" muted playsinline></video>
      <audio id="audio-track" class="clip" data-start="0" data-duration="{duration:.2f}" data-track-index="0" src="{VIDEO}"></audio>

      <!-- HOOK-CARD (0 - 1.5s) -->
      <div id="hook-card" class="clip" data-start="0" data-duration="1.5" data-track-index="50">
        <div class="flame">🔥</div>
        <div class="label">Bootcamp</div>
        <div class="title">5 Tage<br /><span class="pop">Klarheit.</span></div>
        <div class="date">29.6. – 3.7.</div>
      </div>

      <!-- CAPTIONS -->
      {chr(10).join("      " + d for d in caption_divs)}

      <!-- STAMPS -->
      {chr(10).join("      " + d for d in stamp_divs)}

      <!-- END-CTA -->
      <div id="cta-final" class="clip" data-start="{cta_start:.2f}" data-duration="{duration - cta_start:.2f}" data-track-index="60">
        <div class="label">Anmeldung</div>
        <div class="headline">Link in<br /><span class="pop">der Bio.</span></div>
        <div id="cta-arrow">
          <div id="cta-arrow-line"></div>
          <div id="cta-arrow-head"></div>
        </div>
      </div>

      <!-- BRAND-FOOTER (always on) -->
      <div id="brand-footer" class="clip brand-footer" data-start="0" data-duration="{duration:.2f}" data-track-index="70">@mum.life.balance</div>
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

if __name__ == "__main__":
    main()
