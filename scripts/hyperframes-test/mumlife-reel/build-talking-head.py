#!/usr/bin/env python3
"""
Talking-Head Reel Builder V3.
 - 4 Cover-Styles (creme / petrol / photo / video-still)
 - Full-Screen Outro-Card (kein Overlay vors Gesicht)
 - Captions mittig-unten
 - Brand-Stamps + Subtle Zoom
"""
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).parent
OUTPUT = ROOT / "index.html"
ASSETS = ROOT / "assets"

REELS = {
    "2026-07-03-heute-oeffnet-sich": {
        "cover_style": "creme",
        "cover_photo": None,
        "cover_eyebrow": "Tag 5 vorbei",
        "cover_hook_top": "Heute Abend",
        "cover_hook_pop": "öffnet sich",
        "cover_hook_bottom": "der Schritt.",
        "cover_date": "Fr · 3. Juli",
        "accent_words": ["bio", "hooks", "lead-magnet", "wochenstruktur", "postingplan", "sommer", "heute", "abend", "stories", "story"],
        "stamps": [
            {"text": "TAG 5", "at": 1.8, "dur": 5, "pos": "top-right", "color": "petrol"},
            {"text": "21 UHR", "at": 12, "dur": 4, "pos": "top-left", "color": "orange"},
        ],
        "cta_eyebrow": "Mehr in den",
        "cta_keyword": "STORIES",
        "cta_sublabel": "Heute Abend · 21 Uhr",
        "screen_pip": None,
    },
    "2026-06-09-bio-niemand-klickt": {
        "cover_style": "petrol",
        "cover_photo": None,
        "cover_eyebrow": "Niemand klickt",
        "cover_hook_top": "auf meine",
        "cover_hook_pop": "Bio.",
        "cover_hook_bottom": "",
        "cover_date": "Mentee an Patricia",
        "accent_words": ["bio", "menti", "mentee", "followerin", "schmerzpunkt", "transformation", "80", "prozent", "bio-bot"],
        "stamps": [
            {"text": "80%", "at": 18, "dur": 4, "pos": "top-right", "color": "orange"},
        ],
        "cta_eyebrow": "Kommentiere",
        "cta_keyword": "BIO",
        "cta_sublabel": "und ich schick dir den Link",
        "screen_pip": {"src": "../../../outputs/reels/2026-06-09-bio-niemand-klickt/screen-bio.mp4", "start": 8.5, "dur": 12.0},
    },
    "2026-06-10-story-story-idee-dms": {
        "cover_style": "petrol",
        "cover_photo": None,
        "cover_eyebrow": "1 Satz · 6 Sekunden",
        "cover_hook_top": "3 echte",
        "cover_hook_pop": "Anfragen",
        "cover_hook_bottom": "aus EINER Story.",
        "cover_date": "Letzte Woche",
        "accent_words": ["3", "drei", "story", "stories", "anfragen", "sekunden", "spülmaschine", "echte", "moment", "szenen", "workbook"],
        "stamps": [
            {"text": "3 ANFRAGEN", "at": 18, "dur": 4, "pos": "top-right", "color": "petrol"},
        ],
        "cta_eyebrow": "Kommentiere",
        "cta_keyword": "STORY",
        "cta_sublabel": "und ich schick dir das Workbook",
        "screen_pip": None,
    },
    "2026-06-17-sponsorin-poste-mehr": {
        "cover_style": "photo",
        "cover_photo": "assets/cover-photo-2.jpg",
        "cover_eyebrow": "Sponsorin im Teamcall",
        "cover_hook_top": "„Poste",
        "cover_hook_pop": "einfach",
        "cover_hook_bottom": "mehr.\"",
        "cover_date": "Der häufigste Tipp",
        "accent_words": ["networkerin", "monaten", "warme", "liste", "falsche", "produktbilder", "schmerzpunkt", "alltag"],
        "stamps": [
            {"text": "DAS PROBLEM", "at": 14, "dur": 4, "pos": "top-right", "color": "orange"},
        ],
        "cta_eyebrow": "Teile das",
        "cta_keyword": "in deiner Story",
        "cta_sublabel": "wenn's dich genauso trifft",
        "screen_pip": None,
    },
    "2026-06-19-webinar-bootcamp-pivot": {
        "cover_style": "photo",
        "cover_photo": "assets/cover-photo-1.jpg",
        "cover_eyebrow": "Letzte Woche entschieden",
        "cover_hook_top": "Webinar?",
        "cover_hook_pop": "Mach ich nicht.",
        "cover_hook_bottom": "",
        "cover_date": "5-Tage-Bootcamp statt 90-Min-Webinar",
        "accent_words": ["webinar", "bootcamp", "5-tage", "5", "tage", "90", "sprachnachricht", "pia", "ki-mentorin", "kostenlos", "29.", "3.", "juni", "juli"],
        "stamps": [
            {"text": "PIVOT", "at": 2, "dur": 4, "pos": "top-right", "color": "orange"},
            {"text": "5 TAGE", "at": 30, "dur": 5, "pos": "top-left", "color": "petrol"},
        ],
        "cta_eyebrow": "29. Juni – 3. Juli · kostenlos",
        "cta_keyword": "BOOTCAMP",
        "cta_sublabel": "Kommentiere für Anmeldelink",
        "screen_pip": None,
    },
    "2026-06-22-bootcamp-was-passiert": {
        "cover_style": "video-still",
        "cover_photo": None,
        "cover_eyebrow": "Eine Woche bis",
        "cover_hook_top": "Was",
        "cover_hook_pop": "passiert",
        "cover_hook_bottom": "im Bootcamp?",
        "cover_date": "29. Juni – 3. Juli",
        "accent_words": ["bootcamp", "tag", "bio", "leadmagnet", "leadmagneten", "wochenstruktur", "mama-ceo", "postingplan", "pia", "ki-mentorin", "kostenlos", "29.", "3.", "juni", "5"],
        "stamps": [
            {"text": "TAG 1", "at": 6, "dur": 4, "pos": "top-right", "color": "petrol"},
            {"text": "TAG 2", "at": 15, "dur": 4, "pos": "top-right", "color": "petrol"},
            {"text": "TAG 3", "at": 26, "dur": 4, "pos": "top-right", "color": "petrol"},
            {"text": "TAG 4", "at": 36, "dur": 4, "pos": "top-right", "color": "petrol"},
            {"text": "TAG 5", "at": 48, "dur": 4, "pos": "top-right", "color": "orange"},
        ],
        "cta_eyebrow": "29. Juni – 3. Juli · kostenlos",
        "cta_keyword": "BOOTCAMP",
        "cta_sublabel": "Kommentiere für Anmeldelink",
        "screen_pip": {"src": "../../../outputs/reels/2026-06-22-bootcamp-was-passiert/screen-notion.mp4", "start": 6.0, "dur": 35.0},
    },
    "2026-06-24-liebe-kinder-mein-ding": {
        "cover_style": "photo",
        "cover_photo": "assets/cover-photo-3.jpg",
        "cover_eyebrow": "Beides parallel.",
        "cover_hook_top": "Ich liebe",
        "cover_hook_pop": "meine Kinder.",
        "cover_hook_bottom": "Und mein Ding.",
        "cover_date": "Mama + Mama-CEO",
        "accent_words": ["beides", "vier", "kinder", "frühstück", "schulweg", "wäsche", "laptop", "business", "parallel"],
        "stamps": [
            {"text": "BEIDES", "at": 14, "dur": 4, "pos": "top-right", "color": "orange"},
        ],
        "cta_eyebrow": "Teile das",
        "cta_keyword": "in deiner Story",
        "cta_sublabel": "wenn dir's auch nie wer bestätigt hat",
        "screen_pip": None,
    },
    "2026-06-25-bootcamp-sommer-postest": {
        "cover_style": "video-still",
        "cover_photo": None,
        "cover_eyebrow": "Sonntagabend, 21 Uhr",
        "cover_hook_top": "Was poste",
        "cover_hook_pop": "ich morgen?",
        "cover_hook_bottom": "",
        "cover_date": "5 Tage. Dann weisst du es.",
        "accent_words": ["sonntagabend", "21", "uhr", "system", "bio", "hooks", "wochenstruktur", "lead-magnet", "postingplan", "sommer", "5", "tage"],
        "stamps": [
            {"text": "SONNTAGS-PANIK", "at": 2, "dur": 5, "pos": "top-right", "color": "orange"},
            {"text": "5 TAGE", "at": 24, "dur": 5, "pos": "top-left", "color": "petrol"},
        ],
        "cta_eyebrow": "29. Juni – 3. Juli · kostenlos",
        "cta_keyword": "BOOTCAMP",
        "cta_sublabel": "Kommentiere für Anmeldelink",
        "screen_pip": None,
    },
    "2026-06-30-mein-mittwoch": {
        "cover_style": "photo",
        "cover_photo": "assets/cover-photo-4.jpg",
        "cover_eyebrow": "Mein Mittwoch",
        "cover_hook_top": "Hat Platz",
        "cover_hook_pop": "für alles,",
        "cover_hook_bottom": "was zählt.",
        "cover_date": "Mama-CEO-Wochenstruktur",
        "accent_words": ["mittwoch", "mama-ceo", "konzentrierte", "zeit", "business", "network", "block", "vier", "kinder", "familienzeit"],
        "stamps": [
            {"text": "8–11:30", "at": 12, "dur": 5, "pos": "top-right", "color": "petrol"},
            {"text": "13–16", "at": 22, "dur": 5, "pos": "top-right", "color": "petrol"},
            {"text": "16–19", "at": 32, "dur": 5, "pos": "top-right", "color": "orange"},
        ],
        "cta_eyebrow": "Mein Tag · meiner",
        "cta_keyword": "Mama-CEO",
        "cta_sublabel": "Platz für alles, was zählt",
        "screen_pip": None,
    },
}

WHISPER_FIXES = {
    "Menti": "Mentee", "menti": "Mentee",
    "Liedmagneten": "Leadmagneten", "Liedmagnet": "Leadmagnet",
    "Lidmagneten": "Leadmagneten", "Lidmagnet": "Leadmagnet",
    "Lead-Magneten": "Leadmagneten", "Lead-Magnet": "Leadmagnet",
    "Bio-Bott": "Bio-Bot", "bio-bott": "Bio-Bot",
    "Skrollen": "Scrollen", "skrollen": "scrollen",
    "Pia": "PIA", "pia": "PIA",
    "Loverin": "Lover",
    "Story-Schau": "Story",
    "Partnerin": "Partner",
}

def get_slug():
    if len(sys.argv) < 2:
        print("Usage: python build-talking-head.py <slug>")
        for s in REELS: print(f"  {s}")
        sys.exit(1)
    slug = sys.argv[1]
    if slug not in REELS:
        print(f"Unknown slug: {slug}")
        sys.exit(1)
    return slug

slug = get_slug()
cfg = REELS[slug]

# Copy clean.mp4 to assets/
src_video = ROOT.parent.parent.parent / "outputs" / "reels" / slug / "clean.mp4"
asset_path = ASSETS / f"{slug}.mp4"
if not asset_path.exists() or src_video.stat().st_mtime > asset_path.stat().st_mtime:
    shutil.copy(src_video, asset_path)
VIDEO = f"assets/{slug}.mp4"
TRANSCRIPT = ROOT.parent.parent.parent / "outputs" / "reels" / slug / "raw.json"

# Copy PIP video
if cfg.get("screen_pip"):
    pip_src = ROOT.parent.parent.parent / "outputs" / "reels" / slug / Path(cfg["screen_pip"]["src"]).name
    pip_asset = ASSETS / f"{slug}-pip.mp4"
    if not pip_asset.exists() or pip_src.stat().st_mtime > pip_asset.stat().st_mtime:
        shutil.copy(pip_src, pip_asset)
    cfg["screen_pip"]["src"] = f"assets/{slug}-pip.mp4"

def correct_word(w, start_time):
    if w in WHISPER_FIXES:
        return WHISPER_FIXES[w]
    if w.lower() == "juli" and 65 < start_time < 76 and slug in ("2026-06-19-webinar-bootcamp-pivot", "2026-06-22-bootcamp-was-passiert"):
        return "Juni"
    return w

def load_words():
    data = json.loads(TRANSCRIPT.read_text(encoding="utf-8"))
    words = []
    for seg in data["segments"]:
        for w in seg.get("words", []):
            words.append({"word": correct_word(w["word"].strip(), w["start"]), "start": w["start"], "end": w["end"]})
    return words

words = load_words()
total_audio = max(w["end"] for w in words)
duration = total_audio + 0.5

phrases = []
cur = []
for w in words:
    cur.append(w)
    if len(cur) >= 4 or (len(cur) >= 2 and w["word"].rstrip().endswith((".", ",", "!", "?"))):
        phrases.append(cur); cur = []
if cur: phrases.append(cur)

ACCENT_SET = set(a.lower() for a in cfg["accent_words"])
def is_accent(w):
    c = re.sub(r"[^\wäöüÄÖÜß-]", "", w).lower()
    return c in ACCENT_SET

def render_phrase(words_chunk):
    spans = []
    for w in words_chunk:
        cls = "w accent" if is_accent(w["word"]) else "w"
        spans.append(f'<span class="{cls}">{w["word"]}</span>')
    return " ".join(spans).replace(' <span class="w">-', '<span class="w">-')

COVER_DUR = 1.6
CTA_DUR = 3.5
cta_start = round(duration - CTA_DUR, 2)

caption_divs, tweens = [], []
position_options = [{"top": "62%"}, {"top": "60%"}, {"top": "64%"}]

for i, ph in enumerate(phrases):
    pid = f"cap-{i:02d}"
    s = round(ph[0]["start"], 2)
    next_s = phrases[i+1][0]["start"] if i+1 < len(phrases) else duration
    dur = round(min(next_s - s - 0.05, ph[-1]["end"] + 0.35 - s), 2)
    if dur < 0.35: dur = 0.35
    if s < COVER_DUR - 0.3 or s >= cta_start - 0.3:
        continue
    html = render_phrase(ph)
    pos = position_options[i % len(position_options)]
    caption_divs.append(
        f'<div id="{pid}" class="clip caption" style="top: {pos["top"]};" data-start="{s}" data-duration="{dur}" data-track-index="20">'
        f'<div class="bubble"><p class="text">{html}</p></div></div>'
    )
    tweens.append(f'tl.fromTo("#{pid} .bubble", {{ opacity: 0, y: 20, scale: 0.94 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.28, ease: "power3.out" }}, {s});')
    tweens.append(f'tl.fromTo("#{pid} .w", {{ opacity: 0, scale: 0.75 }}, {{ opacity: 1, scale: 1, duration: 0.2, ease: "back.out(2.5)", stagger: 0.035 }}, {s});')
    tweens.append(f'tl.fromTo("#{pid} .accent", {{}}, {{ "--hl": "100%", duration: 0.45, ease: "power2.out" }}, {s + 0.25});')
    exit_at = round(s + dur - 0.18, 2)
    tweens.append(f'tl.to("#{pid} .bubble", {{ opacity: 0, y: -12, duration: 0.18, ease: "power2.in" }}, {exit_at});')
    tweens.append(f'tl.set("#{pid} .bubble", {{ opacity: 0 }}, {round(s + dur, 2)});')
    tweens.append(f'tl.set("#{pid}", {{ opacity: 0 }}, {round(s + dur, 2)});')

# Stamps
stamps_html = []
for i, st in enumerate(cfg["stamps"]):
    sid = f"stamp-{i:02d}"
    stamps_html.append(
        f'<div id="{sid}" class="clip stamp stamp-{st["pos"]} stamp-{st["color"]}" data-start="{st["at"]}" data-duration="{st["dur"]}" data-track-index="25">{st["text"]}</div>'
    )
    tweens.append(f'tl.fromTo("#{sid}", {{ opacity: 0, scale: 0.5, rotation: -10 }}, {{ opacity: 1, scale: 1, rotation: -3, duration: 0.4, ease: "back.out(2.5)" }}, {st["at"]});')
    tweens.append(f'tl.to("#{sid}", {{ opacity: 0, scale: 0.7, duration: 0.3, ease: "power2.in" }}, {st["at"] + st["dur"] - 0.3});')

# Subtle zoom
zoom_points = []
t = COVER_DUR + 2
while t < cta_start - 1:
    zoom_points.append(t)
    t += 12
for i, zt in enumerate(zoom_points):
    tweens.append(f'tl.fromTo("#bg-video", {{ scale: 1 }}, {{ scale: 1.04, duration: 4, ease: "power1.inOut" }}, {zt});')
    tweens.append(f'tl.to("#bg-video", {{ scale: 1, duration: 4, ease: "power1.inOut" }}, {zt + 4});')

# Cover-Card with style variation
tweens.append(f'tl.fromTo("#cover", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25 }}, 0);')
tweens.append(f'tl.fromTo("#cover .hook-pop", {{ scale: 0.85 }}, {{ scale: 1, duration: 0.45, ease: "back.out(2)" }}, 0.2);')
tweens.append(f'tl.to("#cover", {{ opacity: 0, duration: 0.3, ease: "power2.in" }}, {COVER_DUR - 0.3});')
tweens.append(f'tl.set("#cover", {{ opacity: 0 }}, {COVER_DUR});')

# Screen-PIP
pip_html = ""
if cfg["screen_pip"]:
    pip = cfg["screen_pip"]
    pip_html = f'<video id="screen-pip" class="clip" data-start="{pip["start"]}" data-duration="{pip["dur"]}" data-track-index="15" src="{pip["src"]}" muted playsinline></video>'
    tweens.append(f'tl.fromTo("#screen-pip", {{ opacity: 0, scale: 0.8 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "back.out(1.6)" }}, {pip["start"]});')
    tweens.append(f'tl.to("#screen-pip", {{ opacity: 0, scale: 0.8, duration: 0.3, ease: "power2.in" }}, {pip["start"] + pip["dur"] - 0.3});')

# End-CTA = Full-Screen Brand-Card (kein Overlay über Patricia)
# Patricia fadet aus, Card fadet ein
tweens.append(f'tl.fromTo("#cta-final", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.35, ease: "power2.out" }}, {cta_start});')
tweens.append(f'tl.fromTo("#cta-final .keyword", {{ scale: 0.8 }}, {{ scale: 1, duration: 0.5, ease: "back.out(1.6)" }}, {cta_start + 0.1});')
tweens.append(f'tl.to("#cta-final .pop", {{ scale: 1.08, duration: 0.35, yoyo: true, repeat: 4, ease: "power1.inOut" }}, {cta_start + 0.6});')

# Build Cover-HTML per style
def cover_html():
    e, ht, hp, hb, d = cfg["cover_eyebrow"], cfg["cover_hook_top"], cfg["cover_hook_pop"], cfg["cover_hook_bottom"], cfg["cover_date"]
    inner = f'''
        <div class="eyebrow">{e}</div>
        <div class="hook-top">{ht}</div>
        <div class="hook-pop">{hp}</div>
        <div class="hook-bottom">{hb}</div>
        <div class="date">{d}</div>'''
    style = cfg["cover_style"]
    if style == "creme":
        return f'<div id="cover" class="clip cover-creme" data-start="0" data-duration="{COVER_DUR}" data-track-index="80">{inner}</div>'
    elif style == "petrol":
        return f'<div id="cover" class="clip cover-petrol" data-start="0" data-duration="{COVER_DUR}" data-track-index="80">{inner}</div>'
    elif style == "photo":
        photo = cfg["cover_photo"]
        return f'''<div id="cover" class="clip cover-photo" data-start="0" data-duration="{COVER_DUR}" data-track-index="80">
        <img class="cover-bg-photo" src="{photo}" />
        <div class="cover-photo-overlay"></div>
        <div class="cover-photo-content">{inner}</div></div>'''
    elif style == "video-still":
        return f'''<div id="cover" class="clip cover-video-still" data-start="0" data-duration="{COVER_DUR}" data-track-index="80">
        <video class="cover-bg-video" src="{VIDEO}" muted playsinline></video>
        <div class="cover-video-overlay"></div>
        <div class="cover-video-content">{inner}</div></div>'''
    return f'<div id="cover" class="clip cover-creme" data-start="0" data-duration="{COVER_DUR}" data-track-index="80">{inner}</div>'

# Outro-CTA = always full-screen creme card (consistent + kein Gesicht)
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
      #bg-video {{ position: absolute; inset: 0; width: 1080px; height: 1920px; object-fit: cover; z-index: 5; transform-origin: center center; }}

      /* === Cover Styles === */
      #cover {{ position: absolute; inset: 0; z-index: 80; overflow: hidden; }}

      /* Style: Creme */
      .cover-creme {{ background: var(--creme); display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; padding: 80px; }}
      .cover-creme .eyebrow {{ font-family: "Source Sans 3"; font-weight: 700; font-size: 44px; color: var(--petrol); letter-spacing: 0.14em; text-transform: uppercase; margin-bottom: 32px; }}
      .cover-creme .hook-top {{ font-family: "Philosopher"; font-weight: 700; font-size: 140px; line-height: 1.0; color: var(--dunkelblau); }}
      .cover-creme .hook-pop {{ font-family: "Philosopher"; font-weight: 700; font-style: italic; font-size: 168px; line-height: 1.0; color: var(--petrol); background: #fff; padding: 8px 32px; border-radius: 22px; display: inline-block; margin: 16px 0; box-shadow: 0 16px 40px rgba(18,130,140,0.3); }}
      .cover-creme .hook-bottom {{ font-family: "Philosopher"; font-weight: 700; font-size: 116px; line-height: 1.0; color: var(--dunkelblau); }}
      .cover-creme .date {{ font-family: "Source Sans 3"; font-weight: 600; font-size: 36px; color: var(--text); margin-top: 48px; opacity: 0.7; }}

      /* Style: Petrol */
      .cover-petrol {{ background: linear-gradient(135deg, var(--dunkelblau) 0%, var(--petrol) 100%); display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; padding: 80px; }}
      .cover-petrol .eyebrow {{ font-family: "Source Sans 3"; font-weight: 700; font-size: 44px; color: var(--creme); letter-spacing: 0.14em; text-transform: uppercase; margin-bottom: 32px; opacity: 0.85; }}
      .cover-petrol .hook-top {{ font-family: "Philosopher"; font-weight: 700; font-size: 140px; line-height: 1.0; color: var(--creme); }}
      .cover-petrol .hook-pop {{ font-family: "Philosopher"; font-weight: 700; font-style: italic; font-size: 168px; line-height: 1.0; color: var(--orange); background: var(--creme); padding: 8px 32px; border-radius: 22px; display: inline-block; margin: 16px 0; box-shadow: 0 20px 50px rgba(0,0,0,0.4); }}
      .cover-petrol .hook-bottom {{ font-family: "Philosopher"; font-weight: 700; font-size: 116px; line-height: 1.0; color: var(--creme); }}
      .cover-petrol .date {{ font-family: "Source Sans 3"; font-weight: 600; font-size: 36px; color: var(--creme); margin-top: 48px; opacity: 0.7; }}

      /* Style: Photo */
      .cover-photo .cover-bg-photo {{ position: absolute; inset: 0; width: 1080px; height: 1920px; object-fit: cover; z-index: 0; }}
      .cover-photo-overlay {{ position: absolute; inset: 0; background: linear-gradient(180deg, rgba(12,28,48,0.15) 0%, rgba(12,28,48,0.5) 60%, rgba(12,28,48,0.85) 100%); z-index: 1; }}
      .cover-photo-content {{ position: absolute; inset: 0; display: flex; flex-direction: column; justify-content: flex-end; align-items: center; text-align: center; padding: 80px; padding-bottom: 200px; z-index: 2; }}
      .cover-photo-content .eyebrow {{ font-family: "Source Sans 3"; font-weight: 700; font-size: 40px; color: #fff; letter-spacing: 0.14em; text-transform: uppercase; margin-bottom: 28px; text-shadow: 0 4px 12px rgba(0,0,0,0.8); }}
      .cover-photo-content .hook-top {{ font-family: "Philosopher"; font-weight: 700; font-size: 124px; line-height: 1.0; color: #fff; text-shadow: 0 6px 20px rgba(0,0,0,0.8); }}
      .cover-photo-content .hook-pop {{ font-family: "Philosopher"; font-weight: 700; font-style: italic; font-size: 144px; line-height: 1.0; color: var(--petrol); background: var(--creme); padding: 6px 28px; border-radius: 18px; display: inline-block; margin: 14px 0; box-shadow: 0 18px 44px rgba(0,0,0,0.55); }}
      .cover-photo-content .hook-bottom {{ font-family: "Philosopher"; font-weight: 700; font-size: 104px; line-height: 1.0; color: #fff; text-shadow: 0 6px 20px rgba(0,0,0,0.8); }}
      .cover-photo-content .date {{ font-family: "Source Sans 3"; font-weight: 600; font-size: 32px; color: #fff; margin-top: 36px; opacity: 0.85; text-shadow: 0 2px 8px rgba(0,0,0,0.8); }}

      /* Style: Video-Still */
      .cover-video-still .cover-bg-video {{ position: absolute; inset: 0; width: 1080px; height: 1920px; object-fit: cover; z-index: 0; filter: brightness(0.75); }}
      .cover-video-overlay {{ position: absolute; inset: 0; background: linear-gradient(135deg, rgba(18,130,140,0.55) 0%, rgba(41,85,109,0.75) 100%); z-index: 1; }}
      .cover-video-content {{ position: absolute; inset: 0; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; padding: 80px; z-index: 2; }}
      .cover-video-content .eyebrow {{ font-family: "Source Sans 3"; font-weight: 700; font-size: 44px; color: var(--creme); letter-spacing: 0.14em; text-transform: uppercase; margin-bottom: 30px; opacity: 0.9; }}
      .cover-video-content .hook-top {{ font-family: "Philosopher"; font-weight: 700; font-size: 132px; line-height: 1.0; color: var(--creme); text-shadow: 0 6px 16px rgba(0,0,0,0.5); }}
      .cover-video-content .hook-pop {{ font-family: "Philosopher"; font-weight: 700; font-style: italic; font-size: 156px; line-height: 1.0; color: var(--orange); background: var(--creme); padding: 6px 28px; border-radius: 20px; display: inline-block; margin: 16px 0; box-shadow: 0 20px 50px rgba(0,0,0,0.55); }}
      .cover-video-content .hook-bottom {{ font-family: "Philosopher"; font-weight: 700; font-size: 108px; line-height: 1.0; color: var(--creme); text-shadow: 0 6px 16px rgba(0,0,0,0.5); }}
      .cover-video-content .date {{ font-family: "Source Sans 3"; font-weight: 600; font-size: 34px; color: var(--creme); margin-top: 38px; opacity: 0.8; }}

      /* === Captions === */
      .caption {{ position: absolute; left: 60px; right: 60px; transform: translateY(-50%); display: flex; justify-content: center; z-index: 40; }}
      .bubble {{ background: var(--creme); padding: 28px 42px; border-radius: 24px; box-shadow: 0 16px 40px rgba(12,28,48,0.45); max-width: 960px; text-align: center; }}
      .bubble .text {{ font-family: "Source Sans 3"; font-weight: 600; font-size: 52px; line-height: 1.22; color: var(--text); }}
      .bubble .w {{ display: inline-block; margin-right: 0.16em; }}
      .bubble .w.accent {{ position: relative; color: var(--petrol); font-weight: 700; --hl: 0%; }}
      .bubble .w.accent::after {{ content: ""; position: absolute; left: -4px; bottom: 2px; width: var(--hl); height: 12px; background: rgba(220,130,46,0.5); z-index: -1; border-radius: 4px; }}

      /* === Stamps === */
      .stamp {{ position: absolute; font-family: "Philosopher"; font-weight: 700; font-style: italic; padding: 18px 32px; border-radius: 16px; box-shadow: 0 12px 28px rgba(0,0,0,0.35); font-size: 56px; letter-spacing: 0.04em; }}
      .stamp-petrol {{ background: var(--petrol); color: #fff; }}
      .stamp-orange {{ background: var(--orange); color: #fff; }}
      .stamp-top-left {{ top: 220px; left: 48px; }}
      .stamp-top-right {{ top: 220px; right: 48px; }}

      /* === Screen-PIP === */
      #screen-pip {{ position: absolute; left: 60px; bottom: 380px; width: 380px; height: 676px; object-fit: cover; border-radius: 28px; border: 6px solid var(--creme); box-shadow: 0 24px 60px rgba(12,28,48,0.6); z-index: 30; }}

      /* === Outro-CTA Full-Screen === */
      #cta-final {{ position: absolute; inset: 0; background: var(--creme); display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; padding: 80px; z-index: 60; opacity: 0; }}
      #cta-final .eyebrow {{ font-family: "Source Sans 3"; font-weight: 700; font-size: 48px; letter-spacing: 0.14em; text-transform: uppercase; color: var(--petrol); margin-bottom: 32px; }}
      #cta-final .keyword {{ font-family: "Philosopher"; font-weight: 700; font-size: 124px; line-height: 1.05; color: var(--dunkelblau); margin-bottom: 32px; }}
      #cta-final .keyword .pop {{ display: inline-block; background: #fff; color: var(--petrol); font-style: italic; padding: 8px 36px; border-radius: 22px; transform-origin: center; box-shadow: 0 18px 44px rgba(18,130,140,0.35); }}
      #cta-final .sublabel {{ font-family: "Source Sans 3"; font-weight: 600; font-size: 44px; color: var(--text); margin-top: 16px; max-width: 900px; line-height: 1.3; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{duration:.2f}" data-width="1080" data-height="1920">

      <video id="bg-video" class="clip" data-start="0" data-duration="{duration:.2f}" data-track-index="1" data-has-audio="true" src="{VIDEO}" playsinline></video>

      {pip_html}

      {cover_html()}

      {chr(10).join("      " + s for s in stamps_html)}
      {chr(10).join("      " + d for d in caption_divs)}

      <div id="cta-final" class="clip" data-start="{cta_start}" data-duration="{CTA_DUR}" data-track-index="60">
        <div class="eyebrow">{cfg["cta_eyebrow"]}</div>
        <div class="keyword"><span class="pop">{cfg["cta_keyword"]}</span></div>
        <div class="sublabel">{cfg["cta_sublabel"]}</div>
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
print(f"Slug: {slug} | Cover-Style: {cfg['cover_style']}")
print(f"Duration: {duration:.2f}s | Captions: {len(caption_divs)} | Stamps: {len(cfg['stamps'])} | PIP: {'yes' if cfg['screen_pip'] else 'no'}")
