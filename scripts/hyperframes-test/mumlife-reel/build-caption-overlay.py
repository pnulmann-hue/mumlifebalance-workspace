#!/usr/bin/env python3
"""
Reads Whisper word-timestamps JSON, groups words into phrase-chunks
(Liane-style: 3-5 words per caption bubble, broken at punctuation),
generates index.html with video + caption overlays + brand pop-up.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
TRANSCRIPT = ROOT / "assets" / "talking-head.json"
VIDEO = "assets/talking-head.mp4"
OUTPUT = ROOT / "index.html"

# === ACCENT WORDS (highlighted in Petrol) ===
ACCENT = {
    "pia", "ki-mentorin", "kostenlos", "bio", "bootcamp",
    "29.", "3.", "juni", "juli", "5", "fünf",
}

# === MAX WORDS PER BUBBLE ===
MAX_WORDS = 5
MIN_WORDS = 2

def strip_word(w):
    """Strip leading space + trailing punct from whisper output."""
    return w.strip()

def is_accent(word):
    clean = re.sub(r"[^\wäöüÄÖÜß-]", "", word).lower()
    return clean in ACCENT

def is_phrase_end(word):
    """Word ends with punctuation that should close a bubble."""
    return word.rstrip().endswith((".", ",", "?", "!", ":", ";"))

def group_into_chunks(words):
    """Group words into 2-5 word phrase chunks, prefer breaks at punctuation."""
    chunks = []
    current = []
    for w in words:
        current.append(w)
        if len(current) >= MAX_WORDS or (len(current) >= MIN_WORDS and is_phrase_end(w["word"])):
            chunks.append(current)
            current = []
    if current:
        if chunks and len(current) < MIN_WORDS:
            chunks[-1].extend(current)
        else:
            chunks.append(current)
    return chunks

def render_chunk_html(chunk):
    """Render words with accent-highlighting. Join with space, but no space before
    leading hyphens (e.g. '-Schritt' should attach to previous word)."""
    parts = []
    for w in chunk:
        word = strip_word(w["word"])
        if is_accent(word):
            parts.append(f'<span class="pop">{word}</span>')
        else:
            parts.append(word)
    # Join: insert space before each part except the first, unless part starts with -
    out = parts[0] if parts else ""
    for p in parts[1:]:
        if p.startswith("-"):
            out += p
        else:
            out += " " + p
    return out

def main():
    data = json.loads(TRANSCRIPT.read_text(encoding="utf-8"))
    words = []
    for seg in data["segments"]:
        for w in seg.get("words", []):
            words.append(w)

    chunks = group_into_chunks(words)
    duration = max(w["end"] for w in words) + 0.5  # small tail
    print(f"Total duration: {duration:.2f}s")
    print(f"Words: {len(words)}, Chunks: {len(chunks)}")

    # Build caption clips
    caption_clips = []
    for i, chunk in enumerate(chunks):
        start = chunk[0]["start"]
        end = chunk[-1]["end"]
        # Hold caption a touch longer for readability
        next_start = chunks[i + 1][0]["start"] if i + 1 < len(chunks) else duration
        hold_until = min(end + 0.3, next_start - 0.05)
        dur = max(hold_until - start, 0.6)
        html = render_chunk_html(chunk)
        caption_clips.append({
            "id": f"cap-{i:02d}",
            "start": round(start, 2),
            "duration": round(dur, 2),
            "html": html,
        })

    # Render caption divs + GSAP entries
    caption_divs = "\n      ".join(
        f'<div id="{c["id"]}" class="clip caption" data-start="{c["start"]}" data-duration="{c["duration"]}" data-track-index="2"><p class="text">{c["html"]}</p></div>'
        for c in caption_clips
    )
    caption_tweens = "\n      ".join(
        f'tl.from("#{c["id"]}", {{ opacity: 0, y: 30, duration: 0.25, ease: "power2.out" }}, {c["start"]});\n      tl.set("#{c["id"]}", {{ opacity: 0 }}, {round(c["start"] + c["duration"], 2)});'
        for c in caption_clips
    )

    template = f'''<!doctype html>
<html lang="de" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      @font-face {{
        font-family: "Philosopher";
        font-style: normal;
        font-weight: 400;
        src: url("assets/fonts/Philosopher-400.woff2") format("woff2");
      }}
      @font-face {{
        font-family: "Philosopher";
        font-style: normal;
        font-weight: 700;
        src: url("assets/fonts/Philosopher-700.woff2") format("woff2");
      }}
      @font-face {{
        font-family: "Source Sans 3";
        font-style: normal;
        font-weight: 300 700;
        src: url("assets/fonts/SourceSans3-Variable.woff2") format("woff2-variations");
      }}
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
        position: absolute;
        inset: 0;
        width: 1080px;
        height: 1920px;
        object-fit: cover;
      }}
      .caption {{
        position: absolute;
        left: 60px;
        right: 60px;
        bottom: 320px;
        background: var(--creme);
        padding: 36px 48px;
        border-radius: 28px;
        box-shadow: 0 12px 32px rgba(12, 28, 48, 0.22);
        text-align: center;
      }}
      .caption .text {{
        font-family: "Source Sans 3", sans-serif;
        font-weight: 600;
        font-size: 56px;
        line-height: 1.22;
        color: var(--text);
      }}
      .caption .text .pop {{
        color: var(--petrol);
        font-weight: 700;
      }}
      #pop-akzent {{
        position: absolute;
        top: 180px;
        left: 50%;
        background: var(--petrol);
        color: #fff;
        padding: 22px 48px;
        border-radius: 18px;
        font-family: "Source Sans 3", sans-serif;
        font-weight: 700;
        font-size: 60px;
        letter-spacing: 0.02em;
        box-shadow: 0 16px 40px rgba(18, 130, 140, 0.4);
      }}
      #cta-final {{
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: var(--creme);
        padding: 60px 72px;
        border-radius: 32px;
        box-shadow: 0 16px 48px rgba(12, 28, 48, 0.28);
        text-align: center;
        max-width: 880px;
      }}
      #cta-final .label {{
        font-family: "Source Sans 3", sans-serif;
        font-weight: 600;
        font-size: 36px;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: var(--petrol);
        margin-bottom: 24px;
      }}
      #cta-final .arrow {{
        font-family: "Philosopher", serif;
        font-weight: 700;
        font-size: 88px;
        line-height: 1.1;
        color: var(--dunkelblau);
      }}
      #cta-final .arrow .pop {{
        color: var(--petrol);
        font-style: italic;
      }}
      .brand-footer {{
        position: absolute;
        bottom: 80px;
        left: 0; right: 0;
        text-align: center;
        font-family: "Philosopher", serif;
        font-weight: 700;
        font-size: 30px;
        color: #fff;
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.6);
        letter-spacing: 0.08em;
      }}
    </style>
  </head>
  <body>
    <div
      id="root"
      data-composition-id="main"
      data-start="0"
      data-duration="{duration:.2f}"
      data-width="1080"
      data-height="1920"
    >
      <video
        id="bg-video"
        class="clip"
        data-start="0"
        data-duration="{duration:.2f}"
        data-track-index="1"
        src="{VIDEO}"
        muted
        playsinline
      ></video>
      <audio
        id="audio-track"
        class="clip"
        data-start="0"
        data-duration="{duration:.2f}"
        data-track-index="0"
        src="{VIDEO}"
      ></audio>

      <!-- Pop-Akzent (Bootcamp-Datum, oben) -->
      <div
        id="pop-akzent"
        class="clip"
        data-start="0.8"
        data-duration="3.2"
        data-track-index="3"
      >
        29.6. – 3.7.
      </div>

      <!-- Captions -->
      {caption_divs}

      <!-- End-CTA -->
      <div
        id="cta-final"
        class="clip"
        data-start="{duration - 3:.2f}"
        data-duration="3.0"
        data-track-index="4"
      >
        <div class="label">Anmeldung</div>
        <div class="arrow">Link in <span class="pop">der Bio.</span></div>
      </div>

      <!-- Brand-Footer (durchgehend) -->
      <div
        id="brand-footer"
        class="clip brand-footer"
        data-start="0"
        data-duration="{duration:.2f}"
        data-track-index="5"
      >
        @mum.life.balance
      </div>
    </div>

    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});

      // Pop-Akzent
      tl.fromTo("#pop-akzent",
        {{ xPercent: -50, scale: 0, opacity: 0 }},
        {{ xPercent: -50, scale: 1, opacity: 1, duration: 0.5, ease: "back.out(1.7)" }},
        0.8
      );
      tl.to("#pop-akzent",
        {{ xPercent: -50, scale: 0.9, opacity: 0, duration: 0.3, ease: "power2.in" }},
        3.7
      );
      tl.set("#pop-akzent", {{ opacity: 0 }}, 4.0);

      // Captions
      {caption_tweens}

      // End-CTA
      tl.fromTo("#cta-final",
        {{ scale: 0.85, opacity: 0 }},
        {{ scale: 1, opacity: 1, duration: 0.5, ease: "back.out(1.4)" }},
        {duration - 3:.2f}
      );

      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''
    OUTPUT.write_text(template, encoding="utf-8")
    print(f"Wrote {OUTPUT}")
    print(f"Captions: {len(caption_clips)}")

if __name__ == "__main__":
    main()
