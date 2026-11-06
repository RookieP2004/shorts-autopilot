"""The Vast World - background sets (1080x1920), drawn in the channel's style.

Depth rules (same in every set):
  foreground  : full colour, 4.5px warm-brown outline, hard cel shadow
  midground   : 2px outline at 60% opacity, softer shadow
  background  : NO outlines, colours pushed toward the sky colour (atmospheric perspective)
Light: warm key from the left/upper-left, cool fill in shadows (teal), warm highlights (amber).
Run: python make_backgrounds.py  -> study.svg, world.svg, cosmos.svg
"""
import math
import os
import random

D = os.path.dirname(os.path.abspath(__file__))
W, H = 1080, 1920
LINE = "#2b1d16"


def rgb(h):
    h = h.lstrip("#")
    return [int(h[i:i + 2], 16) for i in (0, 2, 4)]


def mix(a, b, t):
    A, B = rgb(a), rgb(b)
    return "#%02x%02x%02x" % tuple(int(A[i] * (1 - t) + B[i] * t) for i in range(3))


def svg(defs, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'<defs>{defs}</defs>{body}</svg>')


def lin(id_, stops, x1=0, y1=0, x2=0, y2=1):
    s = "".join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>' for o, c, a in stops)
    return f'<linearGradient id="{id_}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">{s}</linearGradient>'


def rad(id_, stops, cx=0.5, cy=0.5, r=0.5):
    s = "".join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>' for o, c, a in stops)
    return f'<radialGradient id="{id_}" cx="{cx}" cy="{cy}" r="{r}">{s}</radialGradient>'


def ridge(rng, y, amp, x0=-40, x1=W + 40, step=60, bottom=H):
    pts = []
    x = x0
    while x <= x1:
        pts.append((x, y + rng.uniform(-amp, amp) - amp * 0.5 * math.sin(x / 170.0)))
        x += step * rng.uniform(0.6, 1.3)
    d = f"M{x0},{bottom} L" + " L".join(f"{px:.0f},{py:.0f}" for px, py in pts) + f" L{x1},{bottom} Z"
    return d, pts


def landscape(rng, top, bottom, sky_far, layers, mist=True):
    """Distant mountain layers; far = lighter + closer to sky colour, no outlines."""
    out = []
    n = len(layers)
    for i, col in enumerate(layers):
        t = i / max(1, n - 1)
        y = top + (bottom - top) * (0.15 + 0.6 * t)
        d, pts = ridge(rng, y, 70 * (1 - 0.5 * t) + 20, step=50 + 40 * t, bottom=bottom + 400)
        out.append(f'<path d="{d}" fill="{col}"/>')
        # sunlit faces on the left of each peak (key light from the left)
        for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
            if yb < ya:  # rising slope faces left/light
                out.append(f'<path d="M{xa:.0f},{ya:.0f} L{xb:.0f},{yb:.0f} L{xb:.0f},{yb + 80:.0f} Z" '
                           f'fill="{mix(col, "#ffe2b0", 0.18)}" opacity="0.7"/>')
        if mist:
            out.append(f'<rect x="0" y="{y + 30:.0f}" width="{W}" height="140" fill="url(#mist)"/>')
    return "".join(out)


# --------------------------------------------------------------------------------------
def study():
    rng = random.Random(11)
    defs = (lin("wall", [(0, "#2c3c46", 1), (1, "#1b252d", 1)]) +
            lin("sky", [(0, "#6fa7c2", 1), (0.55, "#cfd9cf", 1), (0.8, "#f4cf98", 1), (1, "#f2b27a", 1)]) +
            lin("mist", [(0, "#f6e6cc", 0), (0.5, "#f6e6cc", 0.35), (1, "#f6e6cc", 0)]) +
            lin("floor", [(0, "#5a3d29", 1), (1, "#2a1c14", 1)]) +
            lin("beam", [(0, "#ffe2a8", 0.42), (1, "#ffe2a8", 0)], 0, 0, 0.35, 1) +
            rad("sun", [(0, "#fff3d0", 1), (0.25, "#ffd98f", 0.8), (1, "#ffd98f", 0)]) +
            rad("glow", [(0, "#ffcf8a", 0.35), (1, "#ffcf8a", 0)], 0.5, 0.35, 0.7) +
            rad("vig", [(0.55, "#000", 0), (1, "#05080d", 0.6)], 0.5, 0.45, 0.75) +
            '<clipPath id="win"><path d="M250,1010 L250,420 A290,290 0 0 1 830,420 L830,1010 Z"/></clipPath>')
    b = [f'<rect width="{W}" height="{H}" fill="url(#wall)"/>',
         f'<rect width="{W}" height="{H}" fill="url(#glow)"/>']
    # wall panelling (midground: thin, faded lines)
    for x in (60, 1020):
        b.append(f'<rect x="{x-40}" y="1080" width="80" height="320" fill="none" stroke="{LINE}" stroke-width="2" opacity="0.4"/>')
    # window view: the vast world
    view = [f'<rect x="240" y="120" width="600" height="900" fill="url(#sky)"/>',
            '<circle cx="430" cy="800" r="230" fill="url(#sun)"/>']
    for cx, cy, s in ((380, 360, 1.0), (690, 470, 0.7), (560, 300, 0.55)):
        view.append(f'<g transform="translate({cx},{cy}) scale({s})" fill="#fff6e8" opacity="0.85">'
                    '<ellipse cx="0" cy="0" rx="90" ry="26"/><ellipse cx="-40" cy="-16" rx="46" ry="30"/>'
                    '<ellipse cx="30" cy="-24" rx="54" ry="36"/></g>')
    view.append(landscape(rng, 640, 1010, "#cfd9cf", ["#a9bfc8", "#8ba6b4", "#6c8b9c", "#4f6e7e", "#3a5560"]))
    view.append('<path d="M250,1010 C400,960 520,980 620,940 C700,910 780,930 830,900 L830,1010 Z" fill="#2f4a40"/>')
    view.append('<path d="M420,1010 C470,980 520,975 560,960" stroke="#f8dca0" stroke-width="6" fill="none" opacity="0.7"/>')
    b.append(f'<g clip-path="url(#win)">{"".join(view)}</g>')
    # window frame (foreground weight)
    frame = "M250,1010 L250,420 A290,290 0 0 1 830,420 L830,1010 Z"
    b.append(f'<path d="{frame}" fill="none" stroke="#5a3a26" stroke-width="34"/>')
    b.append(f'<path d="{frame}" fill="none" stroke="{LINE}" stroke-width="4.5"/>')
    b.append(f'<path d="M232,1030 L232,420 A308,308 0 0 1 848,420 L848,1030" fill="none" stroke="{LINE}" stroke-width="4.5"/>')
    for d in ("M540,130 L540,1010", "M250,560 L830,560", "M250,790 L830,790"):
        b.append(f'<path d="{d}" stroke="#5a3a26" stroke-width="16"/><path d="{d}" stroke="{LINE}" stroke-width="2" opacity="0.6"/>')
    b.append(f'<rect x="210" y="1010" width="660" height="40" rx="6" fill="#6b4630" stroke="{LINE}" stroke-width="4.5"/>')
    b.append('<rect x="210" y="1034" width="660" height="16" fill="#3d281b" opacity="0.8"/>')
    # bookshelves both sides (midground)
    books = ["#7c2533", "#2f5a5a", "#b8862e", "#4a5a2a", "#33405e", "#6e4b33", "#8a3b2a", "#3c6e70"]
    for x0, x1 in ((0, 200), (880, 1080)):
        b.append(f'<rect x="{x0}" y="0" width="{x1-x0}" height="1420" fill="#3a2a1f"/>')
        y = 80
        while y < 1360:
            x = x0 + 14
            while x < x1 - 30:
                w = rng.randint(16, 30)
                h = rng.randint(120, 170)
                c = rng.choice(books)
                lean = rng.random() < 0.08
                tr = f' transform="rotate(8 {x} {y+180})"' if lean else ""
                b.append(f'<rect x="{x}" y="{y+180-h}" width="{w}" height="{h}" fill="{c}"{tr}/>'
                         f'<rect x="{x}" y="{y+180-h}" width="{w*0.35:.0f}" height="{h}" fill="#fff" opacity="0.08"{tr}/>'
                         f'<rect x="{x}" y="{y+180-h+18}" width="{w}" height="5" fill="#d9b25a" opacity="0.55"{tr}/>')
                x += w + rng.randint(1, 4)
            b.append(f'<rect x="{x0}" y="{y+180}" width="{x1-x0}" height="22" fill="#5a3d2a"/>'
                     f'<rect x="{x0}" y="{y+196}" width="{x1-x0}" height="6" fill="#1e140e"/>')
            y += 220
        edge = x1 if x0 == 0 else x0
        b.append(f'<rect x="{edge-14 if x0==0 else edge}" y="0" width="14" height="1420" fill="#5a3d2a"/>'
                 f'<path d="M{edge},0 L{edge},1420" stroke="{LINE}" stroke-width="4.5"/>')
    # right shelves sit in shadow (cool), left catch window light (warm)
    b.append('<rect x="880" y="0" width="200" height="1420" fill="#0d2330" opacity="0.38"/>')
    b.append('<rect x="0" y="0" width="200" height="1420" fill="#ffcf8a" opacity="0.06"/>')
    # floor with perspective planks
    b.append(f'<rect x="0" y="1400" width="{W}" height="520" fill="url(#floor)"/>')
    b.append(f'<path d="M0,1400 L{W},1400" stroke="{LINE}" stroke-width="4.5"/>')
    for i in range(-8, 9):
        b.append(f'<path d="M{540 + i*40},1400 L{540 + i*170},1920" stroke="{LINE}" stroke-width="2" opacity="0.35"/>')
    for y in (1450, 1520, 1610, 1730, 1880):
        b.append(f'<path d="M0,{y} L{W},{y}" stroke="{LINE}" stroke-width="1.5" opacity="0.2"/>')
    b.append('<ellipse cx="540" cy="1640" rx="430" ry="120" fill="#6e2a2e" stroke="#2b1d16" stroke-width="4.5"/>'
             '<ellipse cx="540" cy="1640" rx="380" ry="96" fill="none" stroke="#d1a24a" stroke-width="5" opacity="0.7"/>'
             '<ellipse cx="610" cy="1650" rx="300" ry="80" fill="#0d1a24" opacity="0.25"/>')
    # light beam from the window across the room + dust
    b.append('<path d="M250,1000 L830,1000 L1080,1920 L120,1920 Z" fill="url(#beam)"/>')
    for _ in range(40):
        x, y = rng.uniform(300, 900), rng.uniform(1050, 1800)
        b.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rng.uniform(1.5,3.5):.1f}" fill="#fff1c8" opacity="{rng.uniform(.2,.6):.2f}"/>')
    # globe on stand (foreground, right)
    b.append('<g transform="translate(930,1430)">'
             f'<path d="M-50,170 L50,170 L30,150 L-30,150 Z" fill="#6b4630" stroke="{LINE}" stroke-width="4.5"/>'
             f'<path d="M0,150 L0,95" stroke="#b8862e" stroke-width="10"/><path d="M0,150 L0,95" stroke="{LINE}" stroke-width="2"/>'
             f'<circle cx="0" cy="0" r="92" fill="#3c6e70" stroke="{LINE}" stroke-width="4.5"/>'
             '<path d="M-60,-40 C-30,-60 0,-30 -20,0 C-40,20 -70,10 -60,-40 Z M10,-70 C40,-60 60,-20 40,10 C20,30 10,-10 10,-70 Z '
             'M-30,30 C0,30 20,60 0,80 C-20,70 -40,50 -30,30 Z" fill="#c7a25a"/>'
             '<path d="M0,-92 A92,92 0 0 1 0,92 A60,92 0 0 0 0,-92 Z" fill="#0d2330" opacity="0.35"/>'
             '<ellipse cx="-38" cy="-40" rx="22" ry="12" fill="#fff" opacity="0.35"/>'
             f'<path d="M-104,0 A104,104 0 0 1 104,0" fill="none" stroke="#b8862e" stroke-width="7"/>'
             f'<path d="M-104,0 A104,104 0 0 1 104,0" fill="none" stroke="{LINE}" stroke-width="1.6"/></g>')
    b.append(f'<rect width="{W}" height="{H}" fill="url(#vig)"/>')
    return svg(defs, "".join(b))


def world():
    rng = random.Random(5)
    defs = (lin("sky", [(0, "#3e6f8e", 1), (0.45, "#9fc0c4", 1), (0.72, "#f3cf96", 1), (1, "#f0a56c", 1)]) +
            lin("mist", [(0, "#f6e6cc", 0), (0.5, "#f6e6cc", 0.4), (1, "#f6e6cc", 0)]) +
            rad("sun", [(0, "#fff6da", 1), (0.2, "#ffd98f", 0.9), (1, "#ffcf7a", 0)]) +
            lin("ground", [(0, "#4f5e34", 1), (1, "#26301c", 1)]) +
            rad("vig", [(0.55, "#000", 0), (1, "#05080d", 0.55)], 0.5, 0.45, 0.75))
    b = [f'<rect width="{W}" height="{H}" fill="url(#sky)"/>', '<circle cx="300" cy="1060" r="420" fill="url(#sun)"/>']
    for cx, cy, s in ((260, 420, 1.3), (760, 300, 1.0), (620, 620, 0.8), (920, 760, 0.6)):
        b.append(f'<g transform="translate({cx},{cy}) scale({s})" opacity="0.9">'
                 '<ellipse cx="0" cy="0" rx="120" ry="30" fill="#fff4e4"/><ellipse cx="-50" cy="-20" rx="60" ry="38" fill="#fff4e4"/>'
                 '<ellipse cx="40" cy="-30" rx="70" ry="46" fill="#fff4e4"/><ellipse cx="20" cy="6" rx="120" ry="14" fill="#c9a8a0" opacity="0.5"/></g>')
    b.append(landscape(rng, 900, 1500, "#9fc0c4", ["#b5c8c8", "#94adb4", "#7393a0", "#557789", "#3f5e6c", "#2e4852"]))
    # birds
    for x, y, s in ((640, 820, 1), (690, 790, 0.8), (720, 830, 0.7)):
        b.append(f'<path d="M{x},{y} q{10*s},-{8*s} {20*s},0 q{10*s},-{8*s} {20*s},0" stroke="{LINE}" stroke-width="2.5" fill="none" opacity="0.7"/>')
    # foreground cliff ledge where the presenter stands (full outline)
    ledge = "M-20,1540 C180,1500 420,1520 620,1500 C800,1484 960,1510 1100,1490 L1100,1940 L-20,1940 Z"
    b.append(f'<path d="{ledge}" fill="url(#ground)"/>')
    b.append('<path d="M-20,1540 C180,1500 420,1520 620,1500 C800,1484 960,1510 1100,1490 L1100,1560 C900,1580 700,1560 500,1580 C300,1600 100,1580 -20,1600 Z" fill="#7d8a45" opacity="0.6"/>')
    b.append(f'<path d="{ledge}" fill="none" stroke="{LINE}" stroke-width="4.5"/>')
    for _ in range(70):
        x, y = rng.uniform(0, W), rng.uniform(1510, 1600)
        b.append(f'<path d="M{x:.0f},{y:.0f} l{rng.uniform(-4,4):.0f},-{rng.uniform(10,22):.0f}" stroke="#9aab55" stroke-width="3" opacity="0.8"/>')
    b.append('<path d="M760,1940 L820,1700 L900,1640 L1000,1680 L1100,1620 L1100,1940 Z" fill="#3a3a2c" stroke="#2b1d16" stroke-width="4.5"/>'
             '<path d="M900,1640 L1000,1680 L1100,1620 L1100,1940 L960,1940 Z" fill="#141c24" opacity="0.35"/>')
    b.append(f'<rect width="{W}" height="{H}" fill="url(#vig)"/>')
    return svg(defs, "".join(b))


def cosmos():
    rng = random.Random(3)
    defs = (lin("space", [(0, "#070b1e", 1), (0.6, "#141640", 1), (1, "#241a3e", 1)]) +
            rad("neb1", [(0, "#3fb6b0", 0.45), (1, "#3fb6b0", 0)]) +
            rad("neb2", [(0, "#c0587a", 0.35), (1, "#c0587a", 0)]) +
            rad("neb3", [(0, "#f0b060", 0.25), (1, "#f0b060", 0)]) +
            rad("planet", [(0, "#e9a066", 1), (0.6, "#a0563a", 1), (1, "#3a1a20", 1)], 0.35, 0.3, 0.8) +
            rad("atmo", [(0.8, "#7fd6ff", 0), (0.92, "#7fd6ff", 0.55), (1, "#7fd6ff", 0)]) +
            lin("stone", [(0, "#6b6a78", 1), (1, "#2c2b38", 1)]) +
            rad("vig", [(0.55, "#000", 0), (1, "#000", 0.6)], 0.5, 0.45, 0.75))
    b = [f'<rect width="{W}" height="{H}" fill="url(#space)"/>',
         '<ellipse cx="300" cy="500" rx="520" ry="380" fill="url(#neb1)"/>',
         '<ellipse cx="820" cy="760" rx="480" ry="420" fill="url(#neb2)"/>',
         '<ellipse cx="520" cy="1150" rx="600" ry="300" fill="url(#neb3)"/>']
    for _ in range(420):
        x, y = rng.uniform(0, W), rng.uniform(0, 1500)
        r = rng.choice([0.8, 1.0, 1.2, 1.6, 2.4]) if rng.random() > 0.03 else 3.4
        b.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#fff6e6" opacity="{rng.uniform(.35,1):.2f}"/>')
    for x, y in ((180, 260), (860, 420), (420, 940)):
        b.append(f'<path d="M{x-18},{y} L{x+18},{y} M{x},{y-18} L{x},{y+18}" stroke="#fff" stroke-width="2" opacity="0.8"/>'
                 f'<circle cx="{x}" cy="{y}" r="4" fill="#fff"/>')
    # big planet with key light from the left + cool rim on the right
    b.append('<circle cx="840" cy="1240" r="330" fill="url(#planet)"/>')
    b.append('<path d="M840,910 A330,330 0 0 1 840,1570 A230,330 0 0 0 840,910 Z" fill="#0a0d24" opacity="0.55"/>')
    for i, y in enumerate((1110, 1180, 1260, 1330)):
        b.append(f'<path d="M520,{y} C700,{y-30+i*8} 980,{y-20} 1170,{y+10}" stroke="#ffd2a0" stroke-width="{10-i*2}" opacity="0.18" fill="none"/>')
    b.append('<circle cx="840" cy="1240" r="345" fill="url(#atmo)"/>')
    # small ringed planet
    b.append('<g transform="translate(250,700) rotate(-18)"><ellipse cx="0" cy="0" rx="140" ry="34" fill="none" stroke="#d9c09a" stroke-width="10" opacity="0.8"/>'
             '<circle cx="0" cy="0" r="70" fill="#8fb6c8"/><path d="M0,-70 A70,70 0 0 1 0,70 A44,70 0 0 0 0,-70 Z" fill="#0b1026" opacity="0.5"/>'
             '<path d="M-140,0 A140,34 0 0 0 140,0" fill="none" stroke="#e7d2ae" stroke-width="10"/></g>')
    # floating stone platform for the presenter (foreground)
    plat = "M140,1560 C300,1520 780,1520 940,1560 C900,1640 760,1700 540,1712 C320,1700 180,1640 140,1560 Z"
    b.append(f'<path d="{plat}" fill="url(#stone)"/>'
             '<path d="M140,1560 C300,1520 780,1520 940,1560 C780,1590 300,1590 140,1560 Z" fill="#8f8ea0"/>'
             '<path d="M540,1712 C760,1700 900,1640 940,1560 C860,1600 700,1640 600,1650 Z" fill="#0b0d22" opacity="0.4"/>'
             f'<path d="{plat}" fill="none" stroke="{LINE}" stroke-width="4.5"/>'
             '<path d="M300,1700 L320,1800 L340,1712 M700,1712 L690,1830 L740,1700" fill="#2c2b38" stroke="#2b1d16" stroke-width="3"/>')
    b.append(f'<rect width="{W}" height="{H}" fill="url(#vig)"/>')
    return svg(defs, "".join(b))


if __name__ == "__main__":
    for name, fn in (("study", study), ("world", world), ("cosmos", cosmos)):
        with open(os.path.join(D, name + ".svg"), "w") as f:
            f.write(fn())
    print("wrote study.svg world.svg cosmos.svg")
