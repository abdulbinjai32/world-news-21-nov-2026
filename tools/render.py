#!/usr/bin/env python3
"""Draw 'THE WORLD IN ONE DAY' - Saturday 21 November 2026 (1024x1024)."""
import math
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAD = 14
CREAM = (246, 242, 230)
INK = (24, 24, 26)
GRAY = (90, 88, 84)
RED = (166, 30, 34)
NAVY = (26, 38, 70)
C_EU = (32, 68, 132)
C_AS = (176, 92, 22)
C_ME = (84, 50, 118)
C_AF = (22, 100, 74)
C_AM = (126, 30, 90)
C_OC = (20, 100, 112)
C_GL = (70, 70, 70)

FD = "/usr/share/fonts/truetype/liberation/"
def F(name, size):
    return ImageFont.truetype(FD + name, size)

SB = "LiberationSerif-Bold.ttf"
SI = "LiberationSerif-Italic.ttf"
NB = "LiberationSansNarrow-Bold.ttf"
NR = "LiberationSansNarrow-Regular.ttf"
NSB = "LiberationSans-Bold.ttf"

img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img)

def tw(s, f):
    return d.textbbox((0, 0), s, font=f)[2]

def text(x, y, s, f, fill=INK, anchor="la"):
    d.text((x, y), s, font=f, fill=fill, anchor=anchor)

def wrap(s, f, maxw):
    out, cur = [], ""
    for word in s.split():
        t = (cur + " " + word).strip()
        if tw(t, f) <= maxw or not cur:
            cur = t
        else:
            out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out

def para(x, y, s, f, maxw, fill=INK, lh=None, maxlines=3):
    lh = lh or f.size + 1
    lines = wrap(s, f, maxw)[:maxlines]
    for i, ln in enumerate(lines):
        text(x, y + i * lh, ln, f, fill)
    return y + len(lines) * lh

def rule(y, x0=PAD, x1=W - PAD, col=INK, w=1):
    d.line([(x0, y), (x1, y)], fill=col, width=w)

def box(x0, y0, x1, y1, fill=None, outline=GRAY, w=1):
    d.rectangle([x0, y0, x1, y1], fill=fill, outline=outline, width=w)

# ---------------- masthead ----------------
f_rail = F(NB, 13)
text(PAD, 5, "THE WORLD IN ONE DAY", f_rail, RED)
text(W - PAD, 5, "40 STORIES  \u00b7  7 REGIONS  \u00b7  ALL DATED 21 NOVEMBER 2026", f_rail, INK, "ra")
rule(24, w=2)

text(W // 2, 27, "Saturday 21 November 2026", F(SB, 48), INK, "ma")
text(W // 2, 82, "COP31 runs into a 13th day  \u00b7  three missiles downed over Riyadh  \u00b7  eight killed in Ukraine",
     F(SI, 14), GRAY, "ma")
rule(99, col=RED, w=2)

stats = [("13", "day of COP31, due to close on day 12"),
         ("3", "Houthi missiles downed over Riyadh"),
         ("8", "killed in Russia's overnight barrage"),
         ("6.7", "magnitude, central Peru, 00:09 UTC"),
         ("$56.9k", "bitcoin at 03:34 UTC, down 8.2%"),
         ("146", "safe after a jet's landing at Davao")]
bw = (W - 2 * PAD) // 6
f_num, f_lab = F(SB, 24), F(NR, 10)
for i, (num, lab) in enumerate(stats):
    x0 = PAD + i * bw
    d.rectangle([x0 + 1, 107, x0 + 4, 151], fill=RED)
    text(x0 + 9, 102, num, f_num, RED)
    para(x0 + 9, 129, lab, f_lab, bw - 14, GRAY, lh=10, maxlines=2)
rule(155)

regions = [("EUROPE 6", C_EU), ("ASIA 11", C_AS), ("MIDDLE EAST 7", C_ME), ("AFRICA 4", C_AF),
           ("AMERICAS 5", C_AM), ("OCEANIA 4", C_OC), ("GLOBAL 3", C_GL)]
f_reg = F(NB, 10)
rx = PAD
for lab, col in regions:
    wt = tw(lab, f_reg) + 14
    d.rectangle([rx, 160, rx + wt, 177], fill=col)
    text(rx + 7, 163, lab, f_reg, (255, 255, 255))
    rx += wt + 6
rule(182)

# ---------------- pictograms ----------------
def icon(kind, x0, y0, x1, y1, accent):
    cx, cy = (x0 + x1) / 2.0, (y0 + y1) / 2.0
    w, h = x1 - x0, y1 - y0
    if kind == "globe":
        r = min(w, h) * 0.35
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=accent, width=4)
        d.arc([cx - r * 0.42, cy - r, cx + r * 0.42, cy + r], -80, 80, fill=accent, width=2)
        d.line([(cx - r, cy), (cx + r, cy)], fill=accent, width=2)
        d.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55], 0, 180, fill=accent, width=2)
        d.rectangle([x0 + 6, y0 + h * 0.2, x0 + 15, y1 - h * 0.14], fill=RED)
        d.ellipse([x0 + 6, y0 + h * 0.14, x0 + 15, y0 + h * 0.27], fill=RED)
        d.ellipse([x1 - 34, y1 - 34, x1 - 4, y1 - 4], outline=INK, width=3)
        d.line([(x1 - 19, y1 - 19), (x1 - 19, y1 - 29)], fill=INK, width=3)
        d.line([(x1 - 19, y1 - 19), (x1 - 11, y1 - 19)], fill=INK, width=3)
    elif kind == "missiles":
        d.rectangle([x0, y0, x1, y1], fill=NAVY)
        for sx in (0.2, 0.5, 0.8):
            x = x0 + w * sx
            d.line([(x, y1), (x - w * 0.1, y0 + h * 0.24)], fill=(255, 216, 130), width=3)
            d.ellipse([x - w * 0.15, y0 + h * 0.1, x + w * 0.03, y0 + h * 0.3], fill=(255, 148, 40))
        base = y1 - h * 0.2
        for k in range(6):
            bx0 = x0 + 4 + k * (w - 8) / 6.0
            bh = h * (0.2 + 0.12 * ((k * 5) % 3))
            d.rectangle([bx0, base - bh, bx0 + (w - 8) / 6.0 - 3, base], fill=(96, 110, 146))
        d.ellipse([x1 - 30, y0 + 8, x1 - 8, y0 + 30], fill=(242, 238, 216))
    elif kind == "barrage":
        d.rectangle([x0, y0, x1, y1], fill=(62, 26, 30))
        for sx in (0.22, 0.5, 0.79):
            sxp = x0 + w * sx
            d.polygon([(sxp, y1), (sxp - w * 0.09, y0 + h * 0.22), (sxp + w * 0.09, y0 + h * 0.22)],
                      fill=(236, 200, 124))
            d.line([(sxp, y0 + h * 0.22), (sxp - w * 0.17, y0)], fill=(255, 244, 206), width=2)
        d.ellipse([x1 - 38, y1 - 34, x1 - 6, y1 - 2], fill=(216, 84, 40))
        d.ellipse([x1 - 28, y1 - 24, x1 - 14, y1 - 10], fill=(255, 196, 96))
        d.rectangle([x0 + 6, y1 - 14, x0 + 6 + w * 0.3, y1 - 8], fill=(255, 255, 255))
        d.rectangle([x0 + 6, y1 - 8, x0 + 6 + w * 0.3, y1 - 2], fill=(216, 40, 40))
    elif kind == "drone":
        d.line([(cx - w * 0.34, cy - h * 0.2), (cx + w * 0.34, cy - h * 0.2)], fill=accent, width=4)
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], outline=accent, width=4)
        d.line([(cx - w * 0.36, cy + h * 0.24), (cx + w * 0.36, cy + h * 0.24)], fill=RED, width=3)
    elif kind == "wave":
        pts = [(x0 + i, cy + math.sin(i / 5.0) * h * 0.24 * math.exp(-i / (w * 0.75))) for i in range(0, int(w), 3)]
        d.line(pts, fill=RED, width=4)
        d.line([(x0, y0 + 5), (x1, y0 + 5)], fill=GRAY, width=1)
        d.line([(x0, y1 - 5), (x1, y1 - 5)], fill=GRAY, width=1)
    elif kind == "robot":
        d.rectangle([cx - w * 0.22, cy - h * 0.18, cx + w * 0.22, cy + h * 0.26], outline=accent, width=4)
        d.rectangle([cx - 7, cy - 5, cx - 1, cy + 2], fill=accent)
        d.rectangle([cx + 2, cy - 5, cx + 8, cy + 2], fill=accent)
        d.line([(cx, y0 + 6), (cx, cy - h * 0.18)], fill=RED, width=3)
        d.line([(cx - w * 0.22, cy + h * 0.02), (x0 + 6, cy + h * 0.02)], fill=accent, width=3)
        d.line([(cx + w * 0.22, cy + h * 0.02), (x1 - 6, cy + h * 0.02)], fill=accent, width=3)
    elif kind == "chart":
        d.line([(x0 + 8, y0 + h * 0.26), (x0 + w * 0.36, y0 + h * 0.46),
                (x0 + w * 0.62, y0 + h * 0.6), (x1 - 10, y1 - 8)], fill=RED, width=4)
        d.line([(x1 - 24, y1 - 8), (x1 - 10, y1 - 8), (x1 - 10, y1 - 24)], fill=RED, width=4)
        d.line([(x0 + 6, y0 + 4), (x0 + 6, y1 - 6)], fill=GRAY, width=2)
    elif kind == "plane":
        d.polygon([(x0 + 8, cy), (x1 - 12, cy - h * 0.12), (x1 - 4, cy), (x1 - 12, cy + h * 0.12)], fill=accent)
        d.line([(x0 + 8, cy), (x0 + w * 0.44, cy)], fill=accent, width=4)
        d.polygon([(cx - 4, cy + h * 0.1), (cx + 14, cy + h * 0.34), (cx + 20, cy + h * 0.34)], fill=accent)
        d.ellipse([x1 - 20, cy - 5, x1 - 9, cy + 6], fill=(40, 168, 110))
    elif kind == "barrel":
        d.rectangle([cx - w * 0.24, cy - h * 0.26, cx + w * 0.24, cy + h * 0.26], fill=accent)
        d.line([(cx - w * 0.24, cy - h * 0.09), (cx + w * 0.24, cy - h * 0.09)], fill=CREAM, width=3)
        d.line([(cx - w * 0.24, cy + h * 0.09), (cx + w * 0.24, cy + h * 0.09)], fill=CREAM, width=3)
    elif kind == "mine":
        d.polygon([(x0 + 8, y1 - 8), (x1 - 10, y1 - 8), (x0 + 8, y0 + 8)], fill=accent)
        d.rectangle([x0 + 10, y1 - 14, x0 + 10 + w * 0.5, y1 - 6], fill=(36, 36, 36))
        d.line([(cx, y0 + 6), (cx, y1 - 16)], fill=RED, width=3)
    elif kind == "boat":
        d.polygon([(x0 + 8, cy + h * 0.14), (x1 - 10, cy + h * 0.14), (x1 - 20, y1 - 6), (x0 + 18, y1 - 6)],
                  fill=accent)
        d.line([(cx, cy + h * 0.14), (cx, y0 + 6)], fill=INK, width=3)
        d.line([(cx, y0 + 8), (x1 - 14, cy + h * 0.06)], fill=RED, width=3)
        d.line([(x0, y1 - 3), (x1, y1 - 3)], fill=(60, 120, 170), width=3)
    elif kind == "hospital":
        d.rectangle([cx - w * 0.26, cy - h * 0.26, cx + w * 0.26, cy + h * 0.26], outline=accent, width=3)
        d.rectangle([cx - 4, cy - h * 0.17, cx + 4, cy + h * 0.17], fill=RED)
        d.rectangle([cx - w * 0.17, cy - 4, cx + w * 0.17, cy + 4], fill=RED)
    elif kind == "handshake":
        d.line([(x0 + 8, cy - 8), (cx, cy + 4)], fill=accent, width=5)
        d.line([(x1 - 8, cy - 8), (cx, cy + 4)], fill=accent, width=5)
        d.ellipse([cx - 6, cy - 1, cx + 6, cy + 11], fill=RED)
    elif kind == "fist":
        d.line([(cx - w * 0.3, y1 - 8), (cx - w * 0.3, cy)], fill=accent, width=5)
        d.rectangle([cx - w * 0.16, cy - h * 0.26, cx + w * 0.2, cy + h * 0.06], fill=accent)
        d.line([(cx - w * 0.16, cy - h * 0.1), (cx + w * 0.2, cy - h * 0.1)], fill=CREAM, width=2)
    elif kind == "ball":
        d.ellipse([cx - w * 0.21, cy - h * 0.21, cx + w * 0.21, cy + h * 0.21], fill=accent)
        d.arc([cx - w * 0.21, cy - h * 0.21, cx + w * 0.21, cy + h * 0.21], 200, 340, fill=CREAM, width=3)
    elif kind == "bat":
        d.line([(x0 + 10, y1 - 10), (x1 - 14, y0 + 10)], fill=accent, width=6)
        d.ellipse([x1 - 18, y0 + 5, x1 - 6, y0 + 17], fill=RED)
        d.ellipse([x0 + 12, y1 - 14, x0 + 22, y1 - 4], fill=INK)
    elif kind == "car":
        d.rectangle([x0 + 8, cy - 2, x1 - 8, cy + h * 0.22], fill=accent)
        d.rectangle([cx - w * 0.2, cy - h * 0.22, cx + w * 0.2, cy - 1], fill=accent)
        d.ellipse([x0 + 12, cy + h * 0.16, x0 + 26, cy + h * 0.32], fill=INK)
        d.ellipse([x1 - 26, cy + h * 0.16, x1 - 12, cy + h * 0.32], fill=INK)
    elif kind == "flag":
        d.line([(x0 + 14, y1 - 8), (x0 + 14, y0 + 6)], fill=INK, width=4)
        d.polygon([(x0 + 14, y0 + 6), (x1 - 8, y0 + 18), (x0 + 14, y0 + 32)], fill=accent)
        d.rectangle([x0 + 4, y1 - 8, x0 + 26, y1 - 3], fill=GRAY)
    elif kind == "coin":
        d.ellipse([cx - w * 0.2, cy - h * 0.2, cx + w * 0.2, cy + h * 0.2], outline=accent, width=4)
        text(cx, cy - 1, "B", F(NSB, 17), accent, "mm")
    else:
        d.rectangle([x0 + 8, y0 + 6, x1 - 8, y1 - 6], outline=accent, width=3)

# ---------------- card ----------------
def card(x0, y0, x1, y1, kind, label, headline, accent, region, hl=14, ic=48, num=None,
         deck=None, bar=15):
    box(x0, y0, x1, y1, fill=(253, 251, 245), outline=(198, 191, 176))
    d.rectangle([x0, y0, x1, y0 + bar], fill=accent)
    f_lab = F(NB, 10 if bar >= 15 else 9)
    text(x0 + 5, y0 + int(bar * 0.22), label, f_lab, (255, 255, 255))
    if num is not None:
        text(x1 - 5, y0 + int(bar * 0.22), str(num), f_lab, (255, 255, 255), "ra")
    iw = x1 - x0 - 12
    icon(kind, x0 + 6, y0 + bar + 4, x0 + 6 + iw, y0 + bar + 4 + ic, accent)
    yy = y0 + bar + 8 + ic
    f_h = F(SB, hl)
    yy = para(x0 + 6, yy, headline, f_h, x1 - x0 - 12, INK, lh=hl + 1, maxlines=3)
    if deck:
        para(x0 + 6, yy + 3, deck, F(NR, 10), x1 - x0 - 12, GRAY, lh=11, maxlines=4)
    text(x1 - 5, y1 - 12, region, F(NB, 9), accent, "ra")


def tint(accent, k=0.10):
    return tuple(int(CREAM[c] * (1 - k) + accent[c] * k) for c in range(3))

def card(x0, y0, x1, y1, kind, label, headline, accent, region, hl=14, ic=48, num=None,
         deck=None, bar=15, src=None):
    box(x0, y0, x1, y1, fill=tint(accent, 0.07), outline=(198, 191, 176))
    d.rectangle([x0, y0, x1, y0 + bar], fill=accent)
    f_lab = F(NB, 11 if bar >= 17 else 10)
    text(x0 + 6, y0 + int(bar * 0.2), label, f_lab, (255, 255, 255))
    if num is not None:
        text(x1 - 6, y0 + int(bar * 0.2), str(num), f_lab, (255, 255, 255), "ra")
    iw = x1 - x0 - 12
    icon(kind, x0 + 6, y0 + bar + 4, x0 + 6 + iw, y0 + bar + 4 + ic, accent)
    yy = y0 + bar + 8 + ic
    yy = para(x0 + 6, yy, headline, F(SB, hl), x1 - x0 - 12, INK, lh=hl + 2, maxlines=3)
    if deck:
        yy = para(x0 + 7, yy + 4, deck, F(NR, 11), x1 - x0 - 14, GRAY, lh=12, maxlines=3)
    base = y1 - 13
    text(x1 - 6, base, region, F(NB, 8), accent, "ra")
    if src:
        text(x0 + 7, base, src, F(NR, 8), GRAY)

LEADS = [
    dict(kind="globe", label="COP31: OVERTIME", accent=C_EU, region="GLOBAL", src="Antalya \u00b7 Reuters, AFP",
         headline="COP31 runs into a 13th day with no deal",
         deck="Closing session pushed to Saturday; the draft drops fossil fuels and a $120bn adaptation target. 23 countries want the words back."),
    dict(kind="missiles", label="RIYADH: MISSILES", accent=C_ME, region="MIDDLE EAST", src="Riyadh \u00b7 Saudi-led coalition",
         headline="Three missiles downed over Riyadh",
         deck="Air defences intercepted three Houthi ballistic missiles early Saturday, a second attack on the capital in days."),
    dict(kind="barrage", label="UKRAINE: BARRAGE", accent=RED, region="EUROPE", src="Kyiv \u00b7 Ukraine air force",
         headline="Eight killed in Russia's barrage",
         deck="400 drones and 110 missiles overnight into Saturday; two hit a Kryvyi Rih car park, killing a 7-year-old."),
]
cy0, cy1 = 190, 462
cw = (W - 2 * PAD - 2 * 8) // 3
for i, s in enumerate(LEADS):
    x0 = PAD + i * (cw + 8)
    card(x0, cy0, x0 + cw, cy1, s["kind"], s["label"], s["headline"], s["accent"], s["region"],
         hl=26, ic=134, num=i + 1, deck=s["deck"], bar=19, src=s["src"])

ROW2 = [("drone", "HORMUZ: DRONE", "Iran says it downed a 58th US MQ-9", C_ME, "MIDDLE EAST", 4),
        ("handshake", "TEHRAN: TALKS", "Araqchi still hopes for a deal; Trump says no", C_ME, "MIDDLE EAST", 5),
        ("flag", "GAZA: STRIKES", "Drone strike on Bureij; tanks cross yellow line", C_ME, "MIDDLE EAST", 6),
        ("wave", "PERU: QUAKE 6.7", "Deep quake shakes the Andes at 00:09 UTC", C_AM, "AMERICAS", 7),
        ("robot", "GENEVA: ROBOTS", "UN talks end, pledging rules talks by 2028", C_EU, "EUROPE", 8)]
ROW3 = [("coin", "MARKETS: BITCOIN", "Bitcoin at $56,900 in an AI-led selloff", C_GL, "GLOBAL", 9),
        ("plane", "DAVAO: 146 SAFE", "Jet lands safely after engine-fire warning", C_AS, "ASIA", 10),
        ("barrel", "TOKYO: OIL", "Saudi to triple crude stored in Japan", C_AS, "ASIA", 11),
        ("mine", "SYDNEY: COALMINE", "NSW passes Mount Pleasant mine law", C_OC, "OCEANIA", 12),
        ("boat", "BAYELSA: BOAT", "Burial boat capsizes; 30 dead, 300 missing", C_AF, "AFRICA", 13)]

def draw_row(row, y0, y1):
    cwid = (W - 2 * PAD - 4 * 5) // 5
    for i, (kind, label, head, accent, region, num) in enumerate(row):
        x0 = PAD + i * (cwid + 5)
        card(x0, y0, x0 + cwid, y1, kind, label, head, accent, region, hl=13, ic=44, num=num, bar=15)

draw_row(ROW2, 470, 616)
draw_row(ROW3, 624, 770)

MY0, MY1 = 778, 950
mx1 = PAD + 300
box(PAD, MY0, mx1, MY1, fill=(251, 249, 241), outline=(198, 191, 176))
text(PAD + 7, MY0 + 5, "WHERE IT HAPPENED", F(NB, 10), RED)
text(PAD + 7, MY0 + 18, "stories 1-13", F(NR, 9), GRAY)
mw0, mw1 = PAD + 10, mx1 - 10
mh0, mh1 = MY0 + 32, MY1 - 14
LAND = (208, 198, 174)
cons = [[(-170, 65), (-100, 70), (-60, 60), (-55, 45), (-70, 25), (-100, 18), (-120, 30), (-165, 55)],
        [(-80, 12), (-35, 8), (-35, -10), (-50, -25), (-58, -40), (-70, -50), (-76, 0)],
        [(-10, 36), (30, 45), (60, 55), (40, 30), (35, 12), (12, -10), (0, -30), (10, -34),
         (18, -30), (16, 5), (-10, 20), (-18, 30)],
        [(35, 32), (60, 32), (78, 8), (68, -10), (40, -18), (32, 5)],
        [(60, 55), (140, 55), (150, 40), (120, 20), (95, 5), (75, 20), (55, 30)],
        [(95, 5), (120, 5), (135, -8), (100, -10), (95, 0)],
        [(113, -22), (145, -12), (150, -38), (120, -36), (113, -28)],
        [(-45, 60), (-20, 70), (-25, 82), (-55, 80)]]

def ll(lon, lat):
    return (mw0 + (lon + 180) / 360.0 * (mw1 - mw0), mh0 + (85 - lat) / 170.0 * (mh1 - mh0))

for poly in cons:
    d.polygon([ll(a, b) for a, b in poly], fill=LAND)
d.rectangle([mw0, mh0, mw1, mh1], outline=(198, 191, 176))
dots = [(52, 26, 2), (46, 24, 1), (51, 26, 3), (56, 27, 4), (-11, -11, 5), (8, 46, 6),
        (-76, -10, 7), (-47, -15, 8), (35, 44, 9), (125, 7, 10), (140, 36, 11), (151, -33, 12), (6, 5, 13)]
f_dot = F(NSB, 8)
for lon, lat, n in dots:
    x, y = ll(lon, lat)
    d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=RED)
    text(x, y, str(n), f_dot, (255, 255, 255), "mm")

ax1 = W - PAD
box(mx1 + 8, MY0, ax1, MY1, fill=(251, 249, 241), outline=(198, 191, 176))
ALSO = [
    ("EUROPE", "Rome: strike and protests in 100+ cities"),
    ("EUROPE", "Poland: missiles there called a provocation"),
    ("EUROPE", "Brussels: UK and EU seal trade, youth deals"),
    ("EUROPE", "Antalya: EU warns of a 'fossil summit'"),
    ("GLOBAL", "Antalya: 23 countries demand fossil-fuel text"),
    ("MIDDLE EAST", "Tehran: tanker burns after a mine off Khasab"),
    ("MIDDLE EAST", "Trump claims 'total control' of Hormuz"),
    ("MIDDLE EAST", "Yemen: army reports 854 operations"),
    ("ASIA", "Beijing: Singapore and China plan 20+ deals"),
    ("ASIA", "New Delhi: Modi opens works in Bihar"),
    ("ASIA", "Rawalpindi: Pakistan beat Sri Lanka by 8 wickets"),
    ("ASIA", "Dhaka: service chiefs call on PM on Forces Day"),
    ("ASIA", "Jakarta: Indonesia and EU finish CEPA talks"),
    ("ASIA", "Tokyo: Japan wary of a US-China-Russia bloc"),
    ("ASIA", "New Delhi: India condemns Hormuz shipping attacks"),
    ("ASIA", "Beijing: China tells Japan to fix Taiwan words"),
    ("ASIA", "Trump: China's nuclear build 'hot and heavy'"),
    ("AFRICA", "Kogi: troops rescue 21 kidnap victims"),
    ("AFRICA", "Nairobi: Kenya shilling steady, region weaker"),
    ("AFRICA", "Khartoum: army clears RSF posts in Kordofan"),
    ("AMERICAS", "Bras\u00edlia: Bolsonaro taken to hospital"),
    ("AMERICAS", "Las Vegas: Verstappen on pole for the GP"),
    ("AMERICAS", "Las Vegas: Fundora keeps flyweight titles"),
    ("AMERICAS", "Trump sees a Mexico deal near, presses Canada"),
    ("OCEANIA", "Wellington: Rahul 136, a first for an opener"),
    ("OCEANIA", "Melbourne: Kangaroos into a 4th AFLW final"),
    ("OCEANIA", "Melbourne: Cummins keeps the captaincy"),
]
f_al, f_alr = F(NR, 9), F(NB, 8)
text(mx1 + 15, MY0 + 5, "ALSO ON SATURDAY 21 NOVEMBER 2026 \u2014 %d MORE" % len(ALSO), F(NB, 10), RED)
col_w = (ax1 - mx1 - 26) // 2
half = (len(ALSO) + 1) // 2
for i, (reg, line) in enumerate(ALSO):
    col, row = i // half, i % half
    x = mx1 + 15 + col * (col_w + 8)
    y = MY0 + 24 + row * 14.4
    text(x, y, reg, f_alr, (120, 116, 108))
    for k, ln in enumerate(wrap(line, f_al, col_w - 4)[:2]):
        text(x, y + 8 + k * 8.4, ln, f_al, INK)

DY0 = 956
box(PAD, DY0, W - PAD, 998, fill=(251, 245, 233), outline=RED)
text(PAD + 7, DY0 + 4, "DATE CHECK", F(NB, 10), RED)
para(PAD + 74, DY0 + 4,
     "Every story happened, or was first reported, on Saturday 21 November 2026; items first reported on Friday, such as the COP31 draft and the missiles that fell in Poland, are shown as Saturday's deadlock and fallout. Older items, and claims denied that day, are left out.",
     F(NR, 9), W - 2 * PAD - 84, INK, lh=11, maxlines=3)
text(W // 2, 1003, "THE WORLD IN ONE DAY  \u00b7  drawn from wire reports of 21 November 2026  \u00b7  counts and claims attributed to those who made them",
     F(NR, 8), GRAY, "ma")

img.save("/home/ubuntu/makefun-news/entry7.png", optimize=True)
print("saved")
