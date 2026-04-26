"""Render Instagram Story Slides (1080x1920) for Patricia's Wander-Stories.

Output: 10 PNGs, 5 per Profil (Mentoring + doTERRA), saved to outputs/stories/renders/.
"""
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
SRC = ROOT / "outputs" / "stories"
OUT = ROOT / "outputs" / "stories" / "renders"
FONTS = Path(__file__).parent / "fonts"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1080, 1920

PETROL = (18, 130, 140)
DUNKELBLAU = (41, 85, 109)
CREME = (241, 236, 221)
ORANGE = (220, 130, 46)
WHITE = (255, 255, 255)

F_HEAD = str(FONTS / "Philosopher-Bold.ttf")
F_SUB = str(FONTS / "SourceSans3-Regular.ttf")


def load_image(path):
    img = Image.open(path)
    img = ImageOps.exif_transpose(img)
    return img.convert("RGB")


def cover_crop(img, target_w, target_h, focal_y=0.5):
    """Resize image to cover target_w x target_h, cropping to fit. focal_y in [0,1]."""
    src_w, src_h = img.size
    src_ratio = src_w / src_h
    tgt_ratio = target_w / target_h
    if src_ratio > tgt_ratio:
        new_h = target_h
        new_w = int(target_h * src_ratio)
        img = img.resize((new_w, new_h), Image.LANCZOS)
        x_off = (new_w - target_w) // 2
        return img.crop((x_off, 0, x_off + target_w, target_h))
    else:
        new_w = target_w
        new_h = int(target_w / src_ratio)
        img = img.resize((new_w, new_h), Image.LANCZOS)
        y_off = int((new_h - target_h) * focal_y)
        return img.crop((0, y_off, target_w, y_off + target_h))


def add_gradient_overlay(img, top_alpha=80, bottom_alpha=120):
    """Add subtle dark gradient top + bottom for text legibility."""
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    h = img.size[1]
    # Top gradient (top 30%)
    for y in range(int(h * 0.30)):
        a = int(top_alpha * (1 - y / (h * 0.30)))
        draw.line([(0, y), (img.size[0], y)], fill=(0, 0, 0, a))
    # Bottom gradient (bottom 35%)
    for y in range(int(h * 0.35)):
        a = int(bottom_alpha * (y / (h * 0.35)))
        draw.line([(0, h - 1 - int(h * 0.35) + y), (img.size[0], h - 1 - int(h * 0.35) + y)], fill=(0, 0, 0, a))
    base = img.convert("RGBA")
    base.alpha_composite(overlay)
    return base


def wrap_text(text, font, max_w, draw):
    """Word-wrap text to fit within max_w pixels."""
    words = text.split()
    lines = []
    current = []
    for word in words:
        test = " ".join(current + [word])
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_w:
            current.append(word)
        else:
            if current:
                lines.append(" ".join(current))
            current = [word]
    if current:
        lines.append(" ".join(current))
    return lines


def draw_text_block(draw, text, font, x, y, max_w, color, line_spacing=1.15, align="left"):
    """Draw wrapped text and return total height used."""
    lines = wrap_text(text, font, max_w, draw)
    bbox = draw.textbbox((0, 0), "Ag", font=font)
    line_h = (bbox[3] - bbox[1]) * line_spacing
    y_cursor = y
    for line in lines:
        if align == "center":
            line_bbox = draw.textbbox((0, 0), line, font=font)
            line_w = line_bbox[2] - line_bbox[0]
            x_pos = x + (max_w - line_w) // 2
        else:
            x_pos = x
        draw.text((x_pos, y_cursor), line, font=font, fill=color)
        y_cursor += line_h
    return y_cursor - y


def draw_creme_box(canvas, x, y, w, h, opacity=220, radius=24):
    """Draw a semi-transparent creme box with rounded corners."""
    box = Image.new("RGBA", (w, h), (*CREME, opacity))
    mask = Image.new("L", (w, h), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle((0, 0, w, h), radius=radius, fill=255)
    canvas.paste(box, (x, y), mask)


def render_slide(bg_path, slides_config, out_path):
    """Render a single slide based on config."""
    bg = load_image(bg_path)
    bg = cover_crop(bg, W, H, focal_y=slides_config.get("focal_y", 0.5))
    bg = add_gradient_overlay(
        bg,
        top_alpha=slides_config.get("top_alpha", 80),
        bottom_alpha=slides_config.get("bottom_alpha", 120),
    )
    canvas = bg.copy()
    draw = ImageDraw.Draw(canvas)

    headline = slides_config["headline"]
    sub = slides_config.get("sub", "")
    head_size = slides_config.get("head_size", 92)
    sub_size = slides_config.get("sub_size", 44)
    box_y = slides_config.get("box_y", "middle")
    box_visible = slides_config.get("box_visible", True)
    align = slides_config.get("align", "center")
    headline_color = slides_config.get("headline_color", PETROL)
    sub_color = slides_config.get("sub_color", DUNKELBLAU)

    head_font = ImageFont.truetype(F_HEAD, head_size)
    sub_font = ImageFont.truetype(F_SUB, sub_size)

    pad_x = 80
    box_inner_w = W - 2 * pad_x - 80
    box_x = pad_x
    box_w = W - 2 * pad_x

    # Calculate text heights to size box
    head_lines = wrap_text(headline, head_font, box_inner_w, draw)
    head_bbox = draw.textbbox((0, 0), "Ag", font=head_font)
    head_line_h = (head_bbox[3] - head_bbox[1]) * 1.15
    head_total_h = int(head_line_h * len(head_lines))

    sub_total_h = 0
    if sub:
        sub_lines = wrap_text(sub, sub_font, box_inner_w, draw)
        sub_bbox = draw.textbbox((0, 0), "Ag", font=sub_font)
        sub_line_h = (sub_bbox[3] - sub_bbox[1]) * 1.25
        sub_total_h = int(sub_line_h * len(sub_lines))

    box_h = head_total_h + (sub_total_h + 30 if sub else 0) + 100  # padding

    if box_y == "top":
        by = 220
    elif box_y == "bottom":
        by = H - box_h - 280
    else:
        by = (H - box_h) // 2

    if box_visible:
        draw_creme_box(canvas, box_x, by, box_w, box_h, opacity=slides_config.get("box_opacity", 220))

    # Re-create draw on the modified canvas
    draw = ImageDraw.Draw(canvas)

    text_x = box_x + 40
    text_y = by + 50

    h_used = draw_text_block(
        draw,
        headline,
        head_font,
        text_x,
        text_y,
        box_inner_w,
        headline_color,
        line_spacing=1.15,
        align=align,
    )
    if sub:
        draw_text_block(
            draw,
            sub,
            sub_font,
            text_x,
            text_y + h_used + 30,
            box_inner_w,
            sub_color,
            line_spacing=1.25,
            align=align,
        )

    canvas.convert("RGB").save(out_path, "PNG", optimize=True)
    print(f"  ✓ {out_path.name}")


# ---------------------------------------------------------------
# SLIDE-DEFINITIONEN
# ---------------------------------------------------------------

SLIDES = [
    # PROFIL 1 — MENTORING
    {
        "out": "p1-mentoring-01-sonntag.png",
        "bg": "01-berge-tanne.jpg",
        "headline": "Sonntag.",
        "sub": "Kein Laptop. Volle Akkus.",
        "head_size": 140,
        "sub_size": 56,
        "box_y": "bottom",
        "align": "center",
        "focal_y": 0.35,
    },
    {
        "out": "p1-mentoring-02-business.png",
        "bg": "02-patricia-am-bach.jpg",
        "headline": "Genau dafür hab ich mein Business so gebaut.",
        "head_size": 80,
        "box_y": "top",
        "align": "center",
        "focal_y": 0.55,
    },
    {
        "out": "p1-mentoring-03-vier-kinder.png",
        "bg": "05-wasserfall.jpg",
        "headline": "4 Kinder. 1 Business. 0 Hustle-Kult.",
        "sub": "Das geht. Ehrlich.",
        "head_size": 80,
        "sub_size": 48,
        "box_y": "bottom",
        "align": "center",
        "focal_y": 0.3,
    },
    {
        "out": "p1-mentoring-04-freiheit.png",
        "bg": "04-selfie-im-gras.jpg",
        "headline": "Das ist Freiheit für mich.",
        "head_size": 86,
        "box_y": "bottom",
        "align": "center",
        "focal_y": 0.35,
    },
    {
        "out": "p1-mentoring-05-bio-check.png",
        "bg": "01-berge-tanne.jpg",
        "headline": "Dein Profil sollte das auch können.",
        "sub": "Magnetisch. In 3 Sekunden klar. So, dass jemand sofort denkt: shit, wow.\n\nMach den kostenlosen Bio-Check ↓",
        "head_size": 70,
        "sub_size": 40,
        "box_y": "bottom",
        "align": "center",
        "focal_y": 0.3,
    },
    # PROFIL 2 — DOTERRA / REGENERATION
    {
        "out": "p2-doterra-01-koerper.png",
        "bg": "05-wasserfall.jpg",
        "headline": "Mein Körper hat heute danach geschrien.",
        "head_size": 76,
        "box_y": "bottom",
        "align": "center",
        "focal_y": 0.3,
    },
    {
        "out": "p2-doterra-02-saeule.png",
        "bg": "02-patricia-am-bach.jpg",
        "headline": "Bewegung in der Natur.",
        "sub": "Säule 3 von 4 meiner Energie-Routine.",
        "head_size": 84,
        "sub_size": 42,
        "box_y": "top",
        "align": "center",
        "focal_y": 0.55,
    },
    {
        "out": "p2-doterra-03-fruehling.png",
        "bg": "03-sumpfdotterblume.jpg",
        "headline": "Frühling beginnt im Kleinen.",
        "sub": "Genau wie deine Regeneration.",
        "head_size": 80,
        "sub_size": 46,
        "box_y": "bottom",
        "align": "center",
    },
    {
        "out": "p2-doterra-04-energie.png",
        "bg": "04-selfie-im-gras.jpg",
        "headline": "So fühlt sich Energie an.",
        "sub": "…wenn man sie wirklich aufbaut, statt sie zu pushen.",
        "head_size": 76,
        "sub_size": 40,
        "box_y": "bottom",
        "align": "center",
        "focal_y": 0.3,
    },
    {
        "out": "p2-doterra-05-saeule-frage.png",
        "bg": "01-berge-tanne.jpg",
        "headline": "Welche Säule fehlt dir gerade?",
        "sub": "Bewegung  ·  Schlaf  ·  Nährstoffe  ·  Stille",
        "head_size": 72,
        "sub_size": 38,
        "box_y": "bottom",
        "align": "center",
        "focal_y": 0.3,
    },
]


def main():
    print(f"Rendering {len(SLIDES)} slides → {OUT}\n")
    for slide in SLIDES:
        bg = SRC / slide["bg"]
        out = OUT / slide["out"]
        render_slide(bg, slide, out)
    print(f"\nDone: {len(SLIDES)} PNGs in {OUT}")


if __name__ == "__main__":
    main()
