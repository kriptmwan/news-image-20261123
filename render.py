#!/usr/bin/env python3
"""Render the news-image-20261123 front page: one 1024x1024 PNG summing up
Monday 23 November 2026 world news. Written fresh for this entry.
Layout: masthead with date, 2 cols x 3 rows of story panels, ALSO footer.
Deterministic: same input -> same bytes (no timestamps, no randomness)."""

import math
import sys

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (250, 247, 240)   # off-white paper
INK = (20, 20, 20)        # near-black ink
ACCENT = (27, 79, 138)    # one deep-blue accent, rules/kickers only
FAINT = (201, 194, 178)   # hairlines between panels

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
BOLD = FONT_DIR + "DejaVuSans-Bold.ttf"
REG = FONT_DIR + "DejaVuSans.ttf"

MARGIN = 36
PANEL_W, PANEL_H = 464, 232
GAP_X, GAP_Y = 24, 16
GRID_TOP = 166

f_name = ImageFont.truetype(BOLD, 40)
f_date = ImageFont.truetype(BOLD, 56)
f_kicker = ImageFont.truetype(BOLD, 18)
f_head = ImageFont.truetype(BOLD, 36)
f_sub = ImageFont.truetype(REG, 26)
f_also = ImageFont.truetype(BOLD, 22)
f_foot = ImageFont.truetype(REG, 26)


def spaced(text):
    """Letterspace a kicker: single space between letters, double between words."""
    return "  ".join(" ".join(word) for word in text.split(" "))


# (kicker, [headline line 1, headline line 2], subline, icon)
PANELS = [
    ("MIDDLE EAST",
     ["TANKER ATTACKS", "AT RECORD PACE"],
     "Three tankers hit in Hormuz", "tanker"),
    ("UNITED STATES",
     ["TWO STATES SUE", "MUSK'S SPACEX"],
     "Grok made sexual deepfakes", "scales"),
    ("ASIA",
     ["MINISTER QUITS", "OVER AI EXAMS"],
     "550,000 pupils hit by new rules", "pencil"),
    ("SOUTH ASIA",
     ["HASINA: JAIL", "IF SHE RETURNS"],
     "Ex-PM in exile in India", "courthouse"),
    ("OBITUARY",
     ["MOLLY MELDRUM", "DIES, 83"],
     "Countdown host; AC/DC, Kylie", "microphone"),
    ("LEBANON",
     ["LEBANON UNDER", "FIRE AGAIN"],
     "Families return to ruins", "burst"),
]

FOOTER = [
    "Epstein files review ends \u2014 no new charges, Deputy AG says",
    "US flight chaos lingers; Congress weighs $50bn fix",
]


def icon_tanker(d, x, y):
    d.polygon([(x + 4, y + 34), (x + 56, y + 34), (x + 50, y + 50),
               (x + 10, y + 50)], fill=INK)
    d.rectangle([x + 30, y + 22, x + 52, y + 34], fill=INK)
    d.rectangle([x + 40, y + 12, x + 48, y + 22], fill=ACCENT)
    d.line([(x + 2, y + 56), (x + 58, y + 56)], fill=INK, width=3)


def icon_scales(d, x, y):
    d.line([(x + 30, y + 8), (x + 30, y + 52)], fill=INK, width=4)
    d.line([(x + 10, y + 12), (x + 50, y + 12)], fill=INK, width=4)
    for cx in (10, 50):
        d.line([(x + cx, y + 12), (x + cx - 7, y + 26)], fill=INK, width=3)
        d.line([(x + cx, y + 12), (x + cx + 7, y + 26)], fill=INK, width=3)
        d.polygon([(x + cx - 9, y + 26), (x + cx + 9, y + 26),
                   (x + cx, y + 35)], fill=INK)
    d.line([(x + 20, y + 52), (x + 40, y + 52)], fill=INK, width=4)


def icon_pencil(d, x, y):
    d.line([(x + 14, y + 50), (x + 40, y + 20)], fill=INK, width=12)
    d.polygon([(x + 40, y + 20), (x + 54, y + 8), (x + 50, y + 26)],
              fill=ACCENT)
    d.line([(x + 8, y + 56), (x + 16, y + 48)], fill=ACCENT, width=6)


def icon_courthouse(d, x, y):
    d.polygon([(x + 6, y + 26), (x + 30, y + 8), (x + 54, y + 26)], fill=INK)
    d.rectangle([x + 6, y + 26, x + 54, y + 31], fill=INK)
    for cx in (12, 27, 42):
        d.rectangle([x + cx, y + 33, x + cx + 5, y + 48], fill=INK)
    d.rectangle([x + 6, y + 48, x + 54, y + 53], fill=INK)


def icon_microphone(d, x, y):
    d.rounded_rectangle([x + 21, y + 6, x + 39, y + 30], radius=9, fill=INK)
    d.line([(x + 22, y + 14), (x + 38, y + 14)], fill=PAPER, width=2)
    d.line([(x + 22, y + 22), (x + 38, y + 22)], fill=PAPER, width=2)
    d.rectangle([x + 28, y + 30, x + 32, y + 44], fill=INK)
    d.line([(x + 20, y + 50), (x + 40, y + 50)], fill=INK, width=4)


def icon_burst(d, x, y):
    cx, cy = x + 30, y + 30
    for k in range(8):
        a = math.radians(k * 45)
        x1, y1 = cx + 10 * math.cos(a), cy + 10 * math.sin(a)
        x2, y2 = cx + 26 * math.cos(a), cy + 26 * math.sin(a)
        d.line([(x1, y1), (x2, y2)], fill=INK, width=4)
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=ACCENT)


ICONS = {"tanker": icon_tanker, "scales": icon_scales, "pencil": icon_pencil,
         "courthouse": icon_courthouse, "microphone": icon_microphone,
         "burst": icon_burst}


def check_widths():
    """Fail loudly on any text that overflows its slot."""
    problems = []
    if f_name.getlength("THE WORLD IN ONE DAY") > W - 2 * MARGIN:
        problems.append("nameplate too wide")
    if f_date.getlength("MONDAY, 23 NOVEMBER 2026") > W - 2 * MARGIN:
        problems.append("date too wide")
    text_w = PANEL_W - 18 - 60 - 14 - 18  # padding + icon slot + gap + padding
    for kicker, lines, sub, _ in PANELS:
        if f_kicker.getlength(spaced(kicker)) > PANEL_W - 2 * 18:
            problems.append(f"kicker overflow: {kicker}")
        for line in lines:
            if f_head.getlength(line) > text_w:
                problems.append(f"headline overflow: {line!r} "
                                f"({f_head.getlength(line):.0f} > {text_w})")
        if f_sub.getlength(sub) > PANEL_W - 2 * 18:
            problems.append(f"subline overflow: {sub!r} "
                            f"({f_sub.getlength(sub):.0f} > {PANEL_W - 36})")
    for line in FOOTER:
        if f_foot.getlength(line) > W - 2 * MARGIN:
            problems.append(f"footer overflow: {line!r}")
    return problems


def draw_panel(d, px, py, kicker, lines, sub, icon):
    d.text((px + 18, py + 39), spaced(kicker), font=f_kicker,
           fill=ACCENT, anchor="la")
    ICONS[icon](d, px + 18, py + 81)
    tx = px + 92
    d.text((tx, py + 67), lines[0], font=f_head, fill=INK, anchor="la")
    d.text((tx, py + 111), lines[1], font=f_head, fill=INK, anchor="la")
    d.text((px + 18, py + 179), sub, font=f_sub, fill=INK, anchor="la")


def main():
    problems = check_widths()
    if problems:
        print("OVERFLOW — fix wording:")
        for p in problems:
            print(" -", p)
        sys.exit(1)

    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead
    d.text((MARGIN, 30), "THE WORLD IN ONE DAY", font=f_name, fill=INK,
           anchor="la")
    d.text((MARGIN, 78), "MONDAY, 23 NOVEMBER 2026", font=f_date, fill=INK,
           anchor="la")
    d.line([(MARGIN, 150), (W - MARGIN, 150)], fill=INK, width=3)

    # Panels
    for i, (kicker, lines, sub, icon) in enumerate(PANELS):
        col, row = i % 2, i // 2
        px = MARGIN + col * (PANEL_W + GAP_X)
        py = GRID_TOP + row * (PANEL_H + GAP_Y)
        draw_panel(d, px, py, kicker, lines, sub, icon)

    # Footer
    d.line([(MARGIN, 908), (W - MARGIN, 908)], fill=INK, width=2)
    d.text((MARGIN, 920), "ALSO", font=f_also, fill=ACCENT, anchor="la")
    d.text((MARGIN, 946), FOOTER[0], font=f_foot, fill=INK, anchor="la")
    d.text((MARGIN, 978), FOOTER[1], font=f_foot, fill=INK, anchor="la")

    img.save("entry.png", format="PNG")
    print("wrote entry.png")


if __name__ == "__main__":
    main()
