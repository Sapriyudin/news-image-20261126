#!/usr/bin/env python3
"""Front page for Thursday 26 November 2026 — THE WORLD IN ONE DAY.

Builds a 1024 by 1024 newspaper page with PIL only (no network calls),
then saves it as /output/entry.png. The render is deterministic: running
it twice gives byte-identical output.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

PAGE_W = 1024
PAGE_H = 1024
MARGIN = 28

COL_PAPER = (247, 242, 231)
COL_INK = (26, 26, 26)
COL_RED = (139, 26, 26)
COL_GREY = (110, 105, 95)
COL_PANEL = (233, 226, 210)
COL_SEA = (31, 58, 95)
COL_LAND = (214, 205, 182)
COL_WHITE = (255, 255, 255)

FONT_FOLDER = "/usr/share/fonts/truetype/dejavu"

_loaded = {}


def typeface(filename, size):
    """Return a cached TrueType font."""
    key = (filename, size)
    if key not in _loaded:
        _loaded[key] = ImageFont.truetype(os.path.join(FONT_FOLDER, filename), size)
    return _loaded[key]


def serif_bold(size):
    return typeface("DejaVuSerif-Bold.ttf", size)


def serif(size):
    return typeface("DejaVuSerif.ttf", size)


def sans_bold(size):
    return typeface("DejaVuSans-Bold.ttf", size)


def sans(size):
    return typeface("DejaVuSans.ttf", size)


LEAD_KICKER = "MARKETS  ·  WALL STREET"
LEAD_HEAD = "THE GREAT REVERSAL"
LEAD_SUB = (
    "Dow erases a 1,100-point plunge to close higher; Nasdaq "
    "brushes a bear market, then rebounds."
)
LEAD_NUM = "1"

# Each card: number, region, headline, one-line sub, pictogram key.
CARD_ROWS = [
    dict(num="2", region="WASHINGTON", head="US proposes tariffs on 14 partners",
         sub="China, the EU, Japan and India in the firing line.", pic="scales"),
    dict(num="3", region="GULF", head="Houthis hit Saudi ports, top refinery",
         sub="Ras Tanura struck; Riyadh air defences fire.", pic="flame"),
    dict(num="4", region="CAIRO", head="Fuel tanker fire kills at least 31",
         sub="A tanker overturns on the Ring Road; 21 hurt.", pic="tanker"),
    dict(num="5", region="SANTA CLARA", head="Huang apologises; Nvidia off 3.9%",
         sub="S&P puts the chipmaker's AA rating on watch.", pic="chip"),
    dict(num="6", region="UKRAINE", head="Kyiv strikes Russian airbase",
         sub="Three MiG-31s and two Su-34s damaged.", pic="pin"),
    dict(num="7", region="PYONGYANG", head="Kim widens tactical nuke rollout",
         sub="North Korea also expels the Swiss envoy.", pic="flag"),
    dict(num="8", region="BRUSSELS", head="EU leaders clash over Ukraine loan",
         sub="€45bn loan and the next budget divide them.", pic="ballot"),
    dict(num="9", region="TIANGONG", head="First Pakistani aboard Tiangong",
         sub="Zeeshan Ali boards China's station on Shenzhou-24.", pic="rocket"),
    dict(num="10", region="SPACE", head="FCC clears SpaceX 1m-satellite plan",
         sub="Orbital data centres get the green light.", pic="satellite"),
    dict(num="11", region="CLIMATE", head="Earth tops 2°C for six days running",
         sub="Daily heat hits a record 2.24°C above baseline.", pic="sun"),
    dict(num="12", region="UNITED STATES", head="Measles kills nine in worst outbreak",
         sub="6,039 cases across 47 jurisdictions, CDC says.", pic="cross"),
    dict(num="13", region="MADRID", head="Spain votes Sunday; right favoured",
         sub="Snap poll could end Sánchez's eight years.", pic="gavel"),
]

# Each brief: number, region, headline.
BRIEF_ROWS = [
    dict(num="14", region="TEL AVIV", head="Judges doubt Netanyahu bribery charge"),
    dict(num="15", region="GAZA", head="Israeli strike kills Hamas security chief"),
    dict(num="16", region="TEHRAN", head="US tells citizens to leave Iran"),
    dict(num="17", region="SANAA", head="Blast hits Sanaa; missiles intercepted"),
    dict(num="18", region="BEIRUT", head="Lebanon to open second airport next month"),
    dict(num="19", region="MURMANSK", head="Governor detained in corruption probe"),
    dict(num="20", region="MOSCOW", head="Russia lost nearly 500,000 troops, leak shows"),
    dict(num="21", region="NATO", head="Alliance vows to defend space"),
    dict(num="22", region="HONIARA", head="Australia–Solomon Islands sign security treaty"),
    dict(num="23", region="CARTAGENA", head="Police free 76 supermarket hostages"),
    dict(num="24", region="NAIROBI", head="Kenya cult leader convicted of new charges"),
    dict(num="25", region="KYIV", head="States urge Russia to halt riot-agent use"),
    dict(num="26", region="QUITO", head="Ecuador in talks with US on operations"),
    dict(num="27", region="KINSHASA", head="DR Congo demands answers on Ugandan general"),
    dict(num="28", region="LUSAKA", head="Zambia bans protest on term-limit push"),
    dict(num="29", region="HASAKAH", head="ISIL attack kills two security personnel"),
    dict(num="30", region="SAN JUAN", head="Puerto Rico cancels Luma power contract"),
    dict(num="31", region="BRUSSELS", head="UK–EU treaty has 10-year exit clause"),
    dict(num="32", region="LONDON", head="Tube strike disrupts travel Thu–Fri"),
    dict(num="33", region="WASHINGTON", head="Second judge blocks birthright order"),
    dict(num="34", region="PARIS", head="Sanofi to buy Insmed for $41bn"),
    dict(num="35", region="IRAN", head="Death-row women appeal after protests"),
    dict(num="36", region="BOGOR", head="13 miners trapped in flooded gold mine"),
    dict(num="37", region="HONG KONG", head="Renovation blaze killed 168"),
    dict(num="38", region="MUSIC", head="Duran Duran guitarist Andy Taylor dies at 65"),
    dict(num="39", region="NEW YORK", head="Thanksgiving: markets shut; parade postponed"),
    dict(num="40", region="SEOUL", head="Bank of Korea raises rate to 3.25%"),
    dict(num="41", region="BROOKLYN", head="Huawei guilty of stealing US trade secrets"),
    dict(num="42", region="BEIJING", head="How China got Nvidia AI chips despite rules"),
    dict(num="43", region="LIVERPOOL", head="Liverpool beat Club Brugge 3-0"),
    dict(num="44", region="LILLE", head="Lille stun Bayern Munich 2-1"),
    dict(num="45", region="CULTURE", head="Jennifer Barreto wins Miss Universe 2026"),
]

MARKETS_STRIP = (
    "Dow 50,183 +0.33%   S&P 500 7,183 -0.25%   Nasdaq 23,586 -0.62%   "
    "Brent $91.19 +0.6%   Gold $3,565 -0.4%   BTC $60,822 +3.0%"
)

UTC_STRIP = (
    "UTC  12:00  ·  LONDON  12:00  ·  BERLIN  13:00  ·  DELHI  17:30  ·  "
    "SINGAPORE  20:00  ·  TOKYO  21:00"
)

DATE_LINE = (
    "DATE CHECK: every story above was reported on THURSDAY 26 NOVEMBER 2026  ·  "
    "Sources: Reuters · AP · AFP · Al Jazeera · OneTurn"
)


def split_lines(draw, text, fnt, max_w):
    """Split text into lines that fit max_w (greedy, word by word)."""
    out = []
    current = ""
    for word in text.split():
        candidate = (current + " " + word).strip()
        if draw.textlength(candidate, font=fnt) <= max_w:
            current = candidate
        else:
            if current:
                out.append(current)
            current = word
    if current:
        out.append(current)
    return out


def _px(x, y, s, fx, fy):
    return (x + s * fx, y + s * fy)


def pic_ship(d, x, y, s, col):
    d.polygon([_px(x, y, s, 0.0, 0.55), _px(x, y, s, 0.95, 0.55),
               _px(x, y, s, 0.8, 0.9), _px(x, y, s, 0.15, 0.9)], fill=col)
    d.rectangle([x + s * 0.42, y + s * 0.1, x + s * 0.52, y + s * 0.55], fill=col)
    d.polygon([_px(x, y, s, 0.52, 0.12), _px(x, y, s, 0.85, 0.38),
               _px(x, y, s, 0.52, 0.38)], fill=col)


def pic_tanker(d, x, y, s, col):
    d.rectangle([x, y + s * 0.4, x + s, y + s * 0.75], fill=col)
    d.rectangle([x + s * 0.72, y + s * 0.18, x + s * 0.9, y + s * 0.4], fill=col)
    for i in range(3):
        d.ellipse([x + s * (0.15 + i * 0.28), y + s * 0.2,
                   x + s * (0.25 + i * 0.28), y + s * 0.32], fill=col)


def pic_building(d, x, y, s, col):
    d.rectangle([x + s * 0.12, y + s * 0.25, x + s * 0.88, y + s * 0.95], fill=col)
    for r in range(3):
        for c in range(3):
            d.rectangle([x + s * (0.22 + c * 0.24), y + s * (0.35 + r * 0.2),
                         x + s * (0.32 + c * 0.24), y + s * (0.45 + r * 0.2)],
                        fill=COL_PAPER)


def pic_pin(d, x, y, s, col):
    d.ellipse([x + s * 0.25, y + s * 0.08, x + s * 0.75, y + s * 0.58], fill=col)
    d.polygon([_px(x, y, s, 0.28, 0.45), _px(x, y, s, 0.72, 0.45),
               _px(x, y, s, 0.5, 0.95)], fill=col)
    d.ellipse([x + s * 0.4, y + s * 0.23, x + s * 0.6, y + s * 0.43], fill=COL_PAPER)


def pic_ballot(d, x, y, s, col):
    d.rectangle([x + s * 0.1, y + s * 0.18, x + s * 0.9, y + s * 0.92],
                outline=col, width=4)
    d.line([_px(x, y, s, 0.22, 0.58), _px(x, y, s, 0.42, 0.78),
            _px(x, y, s, 0.8, 0.3)], fill=col, width=5)


def pic_rocket(d, x, y, s, col):
    d.polygon([_px(x, y, s, 0.5, 0.05), _px(x, y, s, 0.72, 0.45),
               _px(x, y, s, 0.5, 0.62), _px(x, y, s, 0.28, 0.45)], fill=col)
    d.polygon([_px(x, y, s, 0.28, 0.5), _px(x, y, s, 0.1, 0.85),
               _px(x, y, s, 0.38, 0.68)], fill=col)
    d.polygon([_px(x, y, s, 0.72, 0.5), _px(x, y, s, 0.9, 0.85),
               _px(x, y, s, 0.62, 0.68)], fill=col)
    d.ellipse([x + s * 0.4, y + s * 0.68, x + s * 0.6, y + s * 0.95], fill=COL_RED)


def pic_flame(d, x, y, s, col):
    d.polygon([_px(x, y, s, 0.5, 0.05), _px(x, y, s, 0.78, 0.45),
               _px(x, y, s, 0.68, 0.6), _px(x, y, s, 0.85, 0.75),
               _px(x, y, s, 0.5, 0.95), _px(x, y, s, 0.15, 0.75),
               _px(x, y, s, 0.32, 0.6), _px(x, y, s, 0.22, 0.45)], fill=col)


def pic_boat(d, x, y, s, col):
    d.polygon([_px(x, y, s, 0.05, 0.6), _px(x, y, s, 0.95, 0.6),
               _px(x, y, s, 0.8, 0.9), _px(x, y, s, 0.2, 0.9)], fill=col)
    d.rectangle([x + s * 0.45, y + s * 0.15, x + s * 0.55, y + s * 0.6], fill=col)
    d.polygon([_px(x, y, s, 0.55, 0.18), _px(x, y, s, 0.88, 0.5),
               _px(x, y, s, 0.55, 0.5)], fill=col)


def pic_flag(d, x, y, s, col):
    d.rectangle([x + s * 0.15, y + s * 0.08, x + s * 0.25, y + s * 0.95], fill=col)
    d.polygon([_px(x, y, s, 0.25, 0.08), _px(x, y, s, 0.92, 0.08),
               _px(x, y, s, 0.92, 0.5), _px(x, y, s, 0.25, 0.5)], fill=col)
    d.ellipse([x + s * 0.5, y + s * 0.2, x + s * 0.66, y + s * 0.36], fill=COL_PAPER)


def pic_gavel(d, x, y, s, col):
    d.rectangle([x + s * 0.2, y + s * 0.15, x + s * 0.8, y + s * 0.38], fill=col)
    d.rectangle([x + s * 0.45, y + s * 0.38, x + s * 0.55, y + s * 0.85], fill=col)
    d.rectangle([x + s * 0.2, y + s * 0.85, x + s * 0.8, y + s * 0.95], fill=col)


def pic_scales(d, x, y, s, col):
    d.line([_px(x, y, s, 0.5, 0.1), _px(x, y, s, 0.5, 0.9)], fill=col, width=4)
    d.line([_px(x, y, s, 0.15, 0.28), _px(x, y, s, 0.85, 0.28)], fill=col, width=4)
    d.polygon([_px(x, y, s, 0.05, 0.32), _px(x, y, s, 0.25, 0.32),
               _px(x, y, s, 0.15, 0.55)], fill=col)
    d.polygon([_px(x, y, s, 0.75, 0.32), _px(x, y, s, 0.95, 0.32),
               _px(x, y, s, 0.85, 0.55)], fill=col)


def pic_factory(d, x, y, s, col):
    d.polygon([_px(x, y, s, 0.05, 0.95), _px(x, y, s, 0.05, 0.4),
               _px(x, y, s, 0.25, 0.4), _px(x, y, s, 0.25, 0.55),
               _px(x, y, s, 0.45, 0.55), _px(x, y, s, 0.45, 0.4),
               _px(x, y, s, 0.95, 0.4), _px(x, y, s, 0.95, 0.95)], fill=col)
    d.rectangle([x + s * 0.68, y + s * 0.1, x + s * 0.78, y + s * 0.4], fill=col)


def pic_chip(d, x, y, s, col):
    d.rectangle([x, y, x + s, y + s], fill=col)
    for i in range(3):
        d.rectangle([x + s * 0.18, y + s * (0.15 + i * 0.28),
                     x + s * 0.82, y + s * (0.25 + i * 0.28)], fill=COL_PAPER)
    d.rectangle([x + s * 0.38, y + s * 0.38, x + s * 0.62, y + s * 0.62], fill=COL_RED)


def pic_satellite(d, x, y, s, col):
    d.rectangle([x + s * 0.05, y + s * 0.38, x + s * 0.32, y + s * 0.62], fill=col)
    d.rectangle([x + s * 0.68, y + s * 0.38, x + s * 0.95, y + s * 0.62], fill=col)
    d.rectangle([x + s * 0.35, y + s * 0.3, x + s * 0.65, y + s * 0.7], fill=col)
    d.line([_px(x, y, s, 0.5, 0.3), _px(x, y, s, 0.5, 0.08)], fill=col, width=3)
    d.ellipse([x + s * 0.42, y + s * 0.02, x + s * 0.58, y + s * 0.16], fill=col)


def pic_sun(d, x, y, s, col):
    d.ellipse([x + s * 0.28, y + s * 0.28, x + s * 0.72, y + s * 0.72], fill=col)
    for a in range(8):
        ang = a * math.pi / 4
        x1 = x + s * (0.5 + 0.5 * math.cos(ang))
        y1 = y + s * (0.5 + 0.5 * math.sin(ang))
        x2 = x + s * (0.5 + 0.36 * math.cos(ang))
        y2 = y + s * (0.5 + 0.36 * math.sin(ang))
        d.line([(x1, y1), (x2, y2)], fill=col, width=4)


def pic_cross(d, x, y, s, col):
    d.rectangle([x + s * 0.38, y + s * 0.08, x + s * 0.62, y + s * 0.92], fill=col)
    d.rectangle([x + s * 0.08, y + s * 0.38, x + s * 0.92, y + s * 0.62], fill=col)


def pic_chart(d, x, y, s, col):
    pts = [_px(x, y, s, 0.05, 0.78), _px(x, y, s, 0.22, 0.58),
           _px(x, y, s, 0.38, 0.68), _px(x, y, s, 0.55, 0.38),
           _px(x, y, s, 0.72, 0.5), _px(x, y, s, 0.92, 0.15)]
    d.line(pts, fill=col, width=5, joint="curve")
    d.polygon([_px(x, y, s, 0.92, 0.15), _px(x, y, s, 0.78, 0.16),
               _px(x, y, s, 0.88, 0.3)], fill=col)
    d.line([_px(x, y, s, 0.05, 0.92), _px(x, y, s, 0.95, 0.92)],
           fill=col, width=3)


PICTOGRAMS = {
    "ship": pic_ship,
    "tanker": pic_tanker,
    "building": pic_building,
    "pin": pic_pin,
    "ballot": pic_ballot,
    "rocket": pic_rocket,
    "flame": pic_flame,
    "boat": pic_boat,
    "flag": pic_flag,
    "gavel": pic_gavel,
    "scales": pic_scales,
    "factory": pic_factory,
    "chip": pic_chip,
    "satellite": pic_satellite,
    "sun": pic_sun,
    "cross": pic_cross,
    "chart": pic_chart,
}


def draw_pictogram(d, kind, x, y, s, col):
    """Draw the small pictogram named kind in a square of side s at (x, y)."""
    fn = PICTOGRAMS.get(kind)
    if fn is not None:
        fn(d, x, y, s, col)


# Rough continent outlines, as fractions of the map box.
LAND_SHAPES = [
    # North America
    [(0.03, 0.30), (0.10, 0.10), (0.20, 0.08), (0.26, 0.22),
     (0.22, 0.38), (0.16, 0.52), (0.10, 0.48), (0.05, 0.40)],
    # South America
    [(0.20, 0.55), (0.26, 0.52), (0.30, 0.62), (0.27, 0.85),
     (0.23, 0.92), (0.20, 0.72)],
    # Europe
    [(0.44, 0.12), (0.50, 0.08), (0.55, 0.16), (0.52, 0.28),
     (0.46, 0.28), (0.43, 0.20)],
    # Africa
    [(0.44, 0.34), (0.52, 0.32), (0.57, 0.42), (0.54, 0.62),
     (0.49, 0.78), (0.45, 0.62), (0.42, 0.45)],
    # Asia
    [(0.55, 0.08), (0.72, 0.06), (0.88, 0.12), (0.92, 0.30),
     (0.82, 0.42), (0.72, 0.38), (0.64, 0.48), (0.58, 0.32),
     (0.53, 0.18)],
    # Australia
    [(0.78, 0.68), (0.88, 0.66), (0.90, 0.78), (0.80, 0.82),
     (0.76, 0.74)],
]

# Numbered story locations on the map: (number, x fraction, y fraction).
MAP_PINS = [
    ("1", 0.18, 0.30),
    ("2", 0.14, 0.42),
    ("3", 0.60, 0.40),
    ("4", 0.50, 0.40),
    ("5", 0.07, 0.38),
    ("6", 0.54, 0.14),
    ("7", 0.87, 0.22),
    ("8", 0.47, 0.18),
    ("9", 0.78, 0.28),
    ("10", 0.12, 0.22),
    ("11", 0.25, 0.65),
    ("12", 0.15, 0.28),
    ("13", 0.44, 0.24),
]


def paint_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=COL_SEA)
    for shape in LAND_SHAPES:
        pts = [(x + px * w, y + py * h) for px, py in shape]
        d.polygon(pts, fill=COL_LAND)
    for num, fx, fy in MAP_PINS:
        cx = x + fx * w
        cy = y + fy * h
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=COL_RED,
                  outline=COL_WHITE, width=2)
        f = sans_bold(10)
        tw = d.textlength(num, font=f)
        d.text((cx - tw / 2, cy - 5), num, font=f, fill=COL_WHITE)


def section_masthead(d):
    d.text((MARGIN, 14), "THE WORLD IN ONE DAY", font=serif_bold(44), fill=COL_INK)
    tag = "No. 26 — 2026"
    d.text((PAGE_W - MARGIN - d.textlength(tag, font=sans(16)), 30),
           tag, font=sans(16), fill=COL_GREY)
    d.line([(MARGIN, 66), (PAGE_W - MARGIN, 66)], fill=COL_INK, width=3)
    d.text((MARGIN, 74), "THURSDAY  26  NOVEMBER  2026", font=sans_bold(34), fill=COL_RED)
    count = "45 STORIES  ·  9 REGIONS"
    d.text((PAGE_W - MARGIN - d.textlength(count, font=sans_bold(14)), 82),
           count, font=sans_bold(14), fill=COL_INK)
    d.line([(MARGIN, 112), (PAGE_W - MARGIN, 112)], fill=COL_INK, width=2)


def section_lead(d):
    top = 124
    height = 164
    d.rectangle([MARGIN, top, PAGE_W - MARGIN, top + height], fill=COL_PANEL)
    d.rectangle([MARGIN, top, MARGIN + 8, top + height], fill=COL_RED)
    d.text((MARGIN + 22, top + 10), LEAD_KICKER, font=sans_bold(13), fill=COL_RED)
    d.text((MARGIN + 22, top + 30), LEAD_HEAD, font=serif_bold(46), fill=COL_INK)
    lines = split_lines(d, LEAD_SUB, serif(20), 560)
    yy = top + 84
    for ln in lines:
        d.text((MARGIN + 22, yy), ln, font=serif(20), fill=COL_INK)
        yy += 26
    draw_pictogram(d, "chart", 684, top + 28, 84, COL_INK)
    d.text((684, top + 120), "LARGEST COMEBACK SINCE APR 2025",
           font=sans_bold(13), fill=COL_RED)
    d.line([(MARGIN + 22, top + height - 30), (PAGE_W - MARGIN - 22, top + height - 30)],
           fill=COL_GREY, width=1)
    d.text((MARGIN + 22, top + height - 24), MARKETS_STRIP,
           font=sans_bold(12), fill=COL_INK)
    return top + height


def section_grid(d):
    gy = 300
    gh = 280
    cell_w = (PAGE_W - 2 * MARGIN - 16) // 3
    cell_h = (gh - 18) // 4
    for i, card in enumerate(CARD_ROWS):
        r, c = divmod(i, 3)
        x = MARGIN + c * (cell_w + 8)
        y = gy + r * (cell_h + 6)
        d.rectangle([x, y, x + cell_w, y + cell_h], outline=COL_GREY, width=1)
        d.text((x + 8, y + 5), card["num"], font=sans_bold(13), fill=COL_RED)
        d.text((x + 30, y + 5), card["region"], font=sans_bold(12), fill=COL_GREY)
        draw_pictogram(d, card["pic"], x + 8, y + 22, 26, COL_INK)
        head_lines = split_lines(d, card["head"], sans_bold(13), cell_w - 48)
        yy = y + 20
        for ln in head_lines[:2]:
            d.text((x + 40, yy), ln, font=sans_bold(13), fill=COL_INK)
            yy += 14
        d.text((x + 8, y + cell_h - 16), card["sub"], font=sans(11), fill=COL_INK)
    return gy + gh


def section_briefs(d, grid_bottom):
    by = grid_bottom + 12
    d.text((MARGIN, by), "THE DAY IN BRIEF", font=sans_bold(15), fill=COL_RED)
    d.line([(MARGIN, by + 20), (PAGE_W - MARGIN, by + 20)], fill=COL_INK, width=2)
    col_w = (PAGE_W - 2 * MARGIN - 20) // 2
    per_col = 16
    for i, brief in enumerate(BRIEF_ROWS):
        col, row = divmod(i, per_col)
        x = MARGIN + col * (col_w + 20)
        y = by + 28 + row * 14
        d.text((x, y), brief["num"], font=sans_bold(12), fill=COL_RED)
        d.text((x + 26, y), brief["region"] + " — " + brief["head"],
               font=sans(12), fill=COL_INK)
    return by + 28 + per_col * 14


def section_map(d, briefs_bottom):
    my = briefs_bottom + 10
    mh = 88
    d.text((MARGIN, my), "WHERE IT HAPPENED — numbered stories on the map",
           font=sans_bold(13), fill=COL_RED)
    paint_map(d, MARGIN, my + 20, PAGE_W - 2 * MARGIN, mh - 20)
    return my + mh


def section_footer(d, map_bottom):
    fy = map_bottom + 10
    d.rectangle([MARGIN, fy, PAGE_W - MARGIN, fy + 46], fill=COL_INK)
    d.text((MARGIN + 12, fy + 6), UTC_STRIP,
           font=sans_bold(12), fill=COL_PAPER)
    d.text((MARGIN + 12, fy + 26), DATE_LINE,
           font=sans(12), fill=COL_PAPER)


def build_page():
    """Assemble the whole front page and return the finished image."""
    img = Image.new("RGB", (PAGE_W, PAGE_H), COL_PAPER)
    d = ImageDraw.Draw(img)
    section_masthead(d)
    section_lead(d)
    grid_bottom = section_grid(d)
    briefs_bottom = section_briefs(d, grid_bottom)
    map_bottom = section_map(d, briefs_bottom)
    section_footer(d, map_bottom)
    return img


def main():
    img = build_page()
    assert img.size == (1024, 1024), "entry must be 1024x1024"
    os.makedirs("/output", exist_ok=True)
    img.save("/output/entry.png", format="PNG", optimize=True)
    out_size = os.path.getsize("/output/entry.png")
    assert out_size <= 1048576, "entry must be <= 1 MiB"
    # Keep a local copy next to the program for inspection.
    here = os.path.dirname(os.path.abspath(__file__))
    local_copy = os.path.join(here, "entry.png")
    img.save(local_copy, format="PNG", optimize=True)
    assert os.path.getsize(local_copy) == out_size, "local copy must match"


if __name__ == "__main__":
    main()
