#!/usr/bin/env python3
"""Render the 23 Nov 2026 world-news summary image (1024x1024 PNG).

Design: newspaper front page. Masthead, one lead story (COP31 collapse)
with a drawn globe visual, then five more stories as a numbered list.
All text is real, verified against CNN / Reuters / Le Monde / Bloomberg /
The Guardian reporting of Monday 23 November 2026.

Layout note: PIL draws text from the top of the font's em box, and the
em box is ~1.17x the point size, so every vertical gap below is sized
from the em box, not the cap height — that is what kept v1's headline
and dek from colliding.

Deterministic: fixed layout, fixed fonts, no timestamps, no randomness.
Pillow writes no metadata into the PNG by default.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 231)
INK = (22, 21, 19)
GREY = (92, 88, 80)
RED = (179, 39, 30)
NAVY = (29, 78, 137)
TEAL = (14, 107, 92)
AMBER = (178, 118, 12)
RULE = (180, 172, 156)

F_BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
F_REG = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
F_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap to a pixel width."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX = 40  # side margin

    # ---------- masthead ----------
    d.line([(MX, 32), (W - MX, 32)], fill=INK, width=4)
    title = "THE WORLD TODAY"
    f_title = font(F_SERIF, 78)
    d.text(((W - d.textlength(title, font=f_title)) / 2, 36), title,
           font=f_title, fill=INK)
    f_meta = font(F_BOLD, 23)
    d.text((MX, 132), "MONDAY, 23 NOVEMBER 2026", font=f_meta, fill=INK)
    right = "SIX STORIES  ·  ONE IMAGE"
    d.text((W - MX - d.textlength(right, font=f_meta), 132), right,
           font=f_meta, fill=RED)
    d.line([(MX, 166), (W - MX, 166)], fill=INK, width=3)

    # ---------- lead story: COP31 ----------
    ly = 184
    f_kick = font(F_BOLD, 24)
    d.text((MX, ly), "CLIMATE  ·  ANTALYA, TURKEY", font=f_kick, fill=RED)
    f_h1 = font(F_BOLD, 108)
    d.text((MX, ly + 28), "COP31", font=f_h1, fill=INK)
    f_h2 = font(F_BOLD, 84)
    d.text((MX, ly + 160), "COLLAPSES", font=f_h2, fill=RED)
    dek = ("Climate talks fail after two weeks — the first COP "
           "breakdown since 2009.")
    f_dek = font(F_REG, 24)
    y = ly + 266
    for line in wrap(d, dek, f_dek, 600):
        d.text((MX, y), line, font=f_dek, fill=INK)
        y += 30
    f_side = font(F_BOLD, 20)
    d.text((MX, y + 8), "Rejected over fossil fuels; 90+ nations sign a pledge.",
           font=f_side, fill=TEAL)

    # ---------- lead visual: cracked globe ----------
    vx0, vy0, vx1, vy1 = 668, 184, 984, 550
    d.rounded_rectangle([vx0, vy0, vx1, vy1], radius=18,
                        fill=(232, 226, 210), outline=INK, width=3)
    cx, cy, r = 826, 336, 104
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=NAVY, outline=INK, width=3)
    # meridians / parallels, clipped to the disc
    mask = Image.new("L", (W, H), 0)
    md = ImageDraw.Draw(mask)
    md.ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
    globe = Image.new("RGB", (W, H), (0, 0, 0))
    gd = ImageDraw.Draw(globe)
    for dx in (-56, 0, 56):
        gd.ellipse([cx + dx - 40, cy - r, cx + dx + 40, cy + r],
                   outline=(120, 165, 205), width=3)
    for dy in (-50, 0, 50):
        gd.line([(cx - r, cy + dy), (cx + r, cy + dy)],
                fill=(120, 165, 205), width=3)
    img.paste(globe, (0, 0), mask)
    d = ImageDraw.Draw(img)
    # red crack across the globe
    crack = [(cx - 92, cy - 64), (cx - 46, cy - 22), (cx - 74, cy + 6),
             (cx - 16, cy + 32), (cx - 50, cy + 60), (cx + 6, cy + 88),
             (cx + 42, cy + 56), (cx + 92, cy + 80)]
    d.line(crack, fill=RED, width=9, joint="curve")
    # NO DEAL stamp
    stamp = Image.new("RGBA", (240, 76), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stamp)
    sd.rectangle([4, 4, 236, 72], outline=RED, width=6)
    sd.text((120, 38), "NO DEAL", font=font(F_BOLD, 40), fill=RED, anchor="mm")
    stamp = stamp.rotate(-12, expand=True, resample=Image.BICUBIC)
    img.paste(stamp, (706, 430), stamp)
    d = ImageDraw.Draw(img)

    # ---------- divider ----------
    d.line([(MX, 566), (W - MX, 566)], fill=INK, width=3)

    # ---------- five more stories ----------
    stories = [
        (NAVY, "WAR AT SEA  ·  LIBYA",
         "Ukraine sinks Russian warship off Libya",
         "Sea drones hit corvette Merkury at Benghazi; cargo ship Angara also struck."),
        (RED, "KYIV  ·  UKRAINE",
         "Russian strike on Kyiv flats kills 11+",
         "Rescuers dig through rubble in Dymer after an overnight strike on flats."),
        (TEAL, "NATO  ·  POLAND",
         "NATO meets on Russian missiles in Poland",
         "Alliance top body convenes after Kh-101 debris found in Poland."),
        (AMBER, "IRAN  ·  UNITED STATES",
         "Tehran vows 'every means' against US blockade",
         "Iran answers Trump's warning that tankers breaking the blockade will be sunk."),
        (NAVY, "TRAVEL  ·  UNITED STATES",
         "Delta outage delays 1,600 flights",
         "Weight-and-balance failure snarls Atlanta hub as Thanksgiving travel begins."),
    ]
    y = 578
    f_num = font(F_BOLD, 30)
    f_sk = font(F_BOLD, 20)
    f_sh = font(F_BOLD, 30)
    f_ss = font(F_REG, 21)
    for i, (color, kicker, head, summ) in enumerate(stories, start=2):
        # number chip
        d.rounded_rectangle([MX, y, MX + 56, y + 56], radius=10, fill=color)
        d.text((MX + 28, y + 28), str(i), font=f_num, fill=(255, 255, 255),
               anchor="mm")
        tx = MX + 72
        d.text((tx, y - 2), kicker, font=f_sk, fill=color)
        d.text((tx, y + 20), head, font=f_sh, fill=INK)
        d.text((tx, y + 56), summ, font=f_ss, fill=GREY)
        if i < 6:
            d.line([(tx, y + 82), (W - MX, y + 82)], fill=RULE, width=2)
        y += 84

    # ---------- footer ----------
    d.line([(MX, 996), (W - MX, 996)], fill=INK, width=2)
    f_foot = font(F_REG, 16)
    foot = "Sources: CNN · Reuters · Le Monde · Bloomberg · The Guardian"
    d.text(((W - d.textlength(foot, font=f_foot)) / 2, 1002), foot,
           font=f_foot, fill=GREY)

    img.save("assets/news.png", format="PNG")
    print("saved assets/news.png")


if __name__ == "__main__":
    draw()
