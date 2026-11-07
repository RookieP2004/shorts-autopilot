"""Townspeople: faceless supporting cast in the channel's flat style (no outlines, two-tone shading, light from the left).

One rig, any person: the job gives each layer an `outfit` (via "rig_args": {"outfit": {...}}), e.g.
  {"skin": "#c98e62", "build": "round", "hair": ["#2a1d17", "bun"], "hat": ["headscarf", "#d9534f"],
   "top": ["#3f7fbf", "dress"], "bottom": ["#3a3e48", "trousers"], "shoes": "#2b2b30",
   "apron": "#f6efe2", "necklace": "#f2b04a", "earrings": "#f2b04a", "tie": "#7c2533", "bag": "#8a5a3c", "belt": "#1d1d22"}
  build: slim | regular | round.   hair styles: short, bun, long, bald, curly.   hats: cap, fez, headscarf, beret, bowler,
  tophat, chef, straw.   top styles: tshirt, shirt, jacket, vest, kurta, dress.   bottom styles: trousers, skirt, shorts.
Faceless: feelings are body language. Poses (BASES): idle, happy, cheer, sad, give, take, hold, shrug, point, explain, wave,
surprised. "sad" drops the head and shoulders; "happy"/"cheer" lift them.
Compatible with the acting system (ARMS, BASES, figure(arms=...)), walking (lift) and the renderer's floor shadow.
"""
import os

W, H = 600, 1500
D = os.path.dirname(os.path.abspath(__file__))

DEFAULT = {"skin": "#d9a27a", "build": "regular", "hair": ["#2a2320", "short"], "hat": None,
           "top": ["#3f7fbf", "shirt"], "bottom": ["#34383f", "trousers"], "shoes": "#25262b"}
BUILD = {"slim": 0.86, "regular": 1.0, "round": 1.28}


def shade(c, k=0.78):
    c = c.lstrip("#")
    r, g, b = (int(c[i:i + 2], 16) for i in (0, 2, 4))
    return "#%02x%02x%02x" % tuple(max(0, min(255, int(v * k))) for v in (r, g, b))


def light(c, k=1.12):
    return shade(c, k)


class Svg:
    def __init__(self):
        self.body, self.defs, self.n = [], [], 0

    def uid(self):
        self.n += 1
        return f"x{self.n}"

    def add(self, s):
        self.body.append(s)

    def part(self, d, col, split=300, k=0.8, hl=None):
        """Flat shape with a hard-edged shadow plane on the right of x=split (light from the left)."""
        i = self.uid()
        self.defs.append(f'<clipPath id="{i}"><path d="{d}"/></clipPath>')
        self.add(f'<path d="{d}" fill="{col}"/>')
        self.add(f'<rect x="{split}" y="0" width="{W}" height="{H}" fill="{shade(col, k)}" clip-path="url(#{i})"/>')
        if hl:
            self.add(f'<path d="{hl}" fill="{light(col, 1.14)}" clip-path="url(#{i})"/>')

    def svg(self):
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
                f'<defs>{"".join(self.defs)}</defs>{"".join(self.body)}</svg>')


def _limb(s, pts, w0, w1, col, dark=False):
    """A tapered limb along pts (2 points) as a filled quad with round ends."""
    (x0, y0), (x1, y1) = pts
    import math
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy) or 1
    nx, ny = -dy / L, dx / L
    c = shade(col, 0.82) if dark else col
    d = (f"M{x0 + nx * w0 / 2:.1f},{y0 + ny * w0 / 2:.1f} L{x1 + nx * w1 / 2:.1f},{y1 + ny * w1 / 2:.1f} "
         f"L{x1 - nx * w1 / 2:.1f},{y1 - ny * w1 / 2:.1f} L{x0 - nx * w0 / 2:.1f},{y0 - ny * w0 / 2:.1f} Z")
    s.add(f'<path d="{d}" fill="{c}"/>')
    s.add(f'<circle cx="{x0}" cy="{y0}" r="{w0 / 2:.1f}" fill="{c}"/><circle cx="{x1}" cy="{y1}" r="{w1 / 2:.1f}" fill="{c}"/>')


# ------------------------------------------------------------------ arms (shoulder, elbow, wrist, hand, front)
L_SH, R_SH = (182, 356), (418, 356)
ARMS = {
    "down": [(L_SH, (150, 560), (150, 750), "open", False), (R_SH, (450, 560), (450, 750), "open", False)],
    "up_v": [(L_SH, (120, 220), (96, 70), "open", False), (R_SH, (480, 220), (504, 70), "open", False)],
    "cheer": [(L_SH, (130, 220), (150, 70), "fist", False), (R_SH, (424, 560), (418, 760), "open", False)],
    "sad": [(L_SH, (210, 560), (250, 740), "open", True), (R_SH, (390, 560), (350, 740), "open", True)],
    "give": [(L_SH, (176, 560), (182, 760), "open", False), (R_SH, (500, 470), (600, 470), "open", False)],
    "take": [(L_SH, (100, 470), (2, 470), "open", False), (R_SH, (424, 560), (418, 760), "open", False)],
    "hold": [(L_SH, (190, 560), (276, 620), "open", True), (R_SH, (410, 560), (324, 620), "open", True)],
    "shrug": [(L_SH, (150, 540), (60, 470), "open", False), (R_SH, (450, 540), (540, 470), "open", False)],
    "point": [(L_SH, (120, 420), (40, 290), "point", False), (R_SH, (424, 560), (418, 760), "open", False)],
    "explain": [(L_SH, (150, 560), (110, 420), "open", False), (R_SH, (424, 560), (418, 760), "open", False)],
    "wave": [(L_SH, (110, 300), (130, 120), "open", False), (R_SH, (424, 560), (418, 760), "open", False)],
    "surprised": [(L_SH, (130, 480), (120, 330), "open", False), (R_SH, (470, 480), (480, 330), "open", False)],
}
# gesture -> (arms, posture, look); posture drives head/shoulder height
BASES = {
    "idle": ("down", "neutral", (0, 0)), "happy": ("up_v", "happy", (0, 0)), "cheer": ("cheer", "happy", (0, 0)),
    "sad": ("sad", "sad", (0, 0)), "give": ("give", "neutral", (0, 0)), "take": ("take", "neutral", (0, 0)),
    "hold": ("hold", "neutral", (0, 0)), "shrug": ("shrug", "neutral", (0, 0)), "point": ("point", "neutral", (0, 0)),
    "explain": ("explain", "neutral", (0, 0)), "wave": ("wave", "happy", (0, 0)), "surprised": ("surprised", "happy", (0, 0)),
}
POSTURE = {"neutral": (0, 0), "happy": (-14, -6), "sad": (46, 16), "warm": (0, 0)}   # (head drop px, shoulder drop px)


def _hand(s, wrist, kind, col):
    x, y = wrist
    r = 27
    s.add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col}"/>')
    s.add(f'<path d="M{x},{y - r} A{r},{r} 0 0 1 {x},{y + r} Z" fill="{shade(col, 0.86)}"/>')
    if kind == "point":
        s.add(f'<circle cx="{x - 22}" cy="{y - 26}" r="11" fill="{col}"/>')


def arm(s, sh, el, wr, kind, o, right, drop):
    sh = (sh[0], sh[1] + drop)
    sleeve = o["top"][0]
    long_sleeve = o["top"][1] in ("shirt", "jacket", "kurta")
    _limb(s, [sh, el], 62, 54, sleeve, dark=right)
    _limb(s, [el, wr], 52 if long_sleeve else 46, 44 if long_sleeve else 40, sleeve if long_sleeve else o["skin"], dark=right)
    _hand(s, wr, kind, o["skin"])


# ------------------------------------------------------------------ body parts
def legs(s, o, lift):
    bcol, bstyle = o["bottom"]
    shoes = o.get("shoes", "#25262b")
    for side, lx in ((0, 250), (1, 350)):
        lf = lift[side]
        k = 1 - lf / 650.0
        s.add(f'<g transform="translate({lx},800) scale(1,{k:.4f}) translate({-lx},-800)">')
        col = bcol if bstyle == "trousers" else o["skin"]
        if bstyle == "shorts":
            s.part(f"M{lx - 46},790 L{lx + 46},790 L{lx + 44},1010 L{lx - 44},1010 Z", bcol, split=300)
        _limb(s, [(lx, 800), (lx + (8 if side else -8), 1400)], 86 if bstyle == "trousers" else 52, 70 if bstyle == "trousers" else 46,
              col, dark=bool(side))
        sx = lx + (28 if side else -28)
        s.add(f'<ellipse cx="{sx}" cy="1426" rx="62" ry="30" fill="{shoes}"/>')
        s.add(f'<ellipse cx="{sx + 10}" cy="1434" rx="50" ry="20" fill="{shade(shoes, 0.75)}"/>')
        s.add('</g>')


def torso(s, o, drop):
    col, style = o["top"]
    top = 330 + drop
    d = (f"M216,{top} C246,{top - 18} 354,{top - 18} 384,{top} C430,{top + 10} 446,{top + 40} 440,{top + 110} "
         f"L428,820 C380,840 220,840 172,820 L160,{top + 110} C154,{top + 40} 170,{top + 10} 216,{top} Z")
    if style == "dress":
        d = (f"M216,{top} C246,{top - 18} 354,{top - 18} 384,{top} C430,{top + 10} 446,{top + 40} 440,{top + 110} "
             f"L470,1180 C380,1210 220,1210 130,1180 L160,{top + 110} C154,{top + 40} 170,{top + 10} 216,{top} Z")
    if style == "kurta":
        d = d.replace("L428,820 C380,840 220,840 172,820", "L440,1040 C380,1060 220,1060 160,1040")
    s.part(d, col, hl=f"M176,{top + 60} C182,{top + 30} 200,{top + 12} 226,{top + 6} C206,{top + 30} 196,{top + 70} 194,{top + 200} Z")
    if style in ("shirt", "jacket", "kurta"):
        s.add(f'<path d="M262,{top - 8} L300,{top + 60} L338,{top - 8}" fill="none" stroke="{shade(col, 0.7)}" stroke-width="10" stroke-linejoin="round"/>')
    if style == "jacket":
        s.add(f'<path d="M300,{top + 60} L300,820" stroke="{shade(col, 0.6)}" stroke-width="8"/>')
        s.add(f'<path d="M262,{top - 6} L300,{top + 120} L250,{top + 150} Z" fill="{shade(col, 0.88)}"/>')
        s.add(f'<path d="M338,{top - 6} L300,{top + 120} L350,{top + 150} Z" fill="{shade(col, 0.7)}"/>')
    if style == "vest":
        s.add(f'<path d="M300,{top + 20} L300,820" stroke="{shade(col, 0.6)}" stroke-width="6"/>')
        for k in range(4):
            s.add(f'<circle cx="312" cy="{top + 120 + k * 90}" r="9" fill="#d4a64a"/>')
    if o.get("tie"):
        t = o["tie"]
        s.add(f'<path d="M290,{top + 10} L310,{top + 10} L318,{top + 230} L300,{top + 262} L282,{top + 230} Z" fill="{t}"/>')
        s.add(f'<path d="M300,{top + 10} L310,{top + 10} L318,{top + 230} L300,{top + 262} Z" fill="{shade(t, 0.8)}"/>')
    if o.get("apron"):
        a = o["apron"]
        s.part(f"M206,{top + 150} L394,{top + 150} L412,1060 C360,1074 240,1074 188,1060 Z", a, k=0.86)
        s.add(f'<path d="M206,{top + 150} L180,{top + 20} M394,{top + 150} L420,{top + 20}" stroke="{a}" stroke-width="10"/>')
        s.add(f'<rect x="250" y="{top + 300}" width="100" height="70" rx="10" fill="{shade(a, 0.9)}"/>')
    if o.get("belt") and style not in ("dress", "kurta"):
        s.add(f'<rect x="168" y="790" width="264" height="26" fill="{o["belt"]}"/><rect x="286" y="788" width="30" height="30" rx="4" fill="#d4a64a"/>')
    if o.get("necklace"):
        n = o["necklace"]
        for k in range(9):
            import math
            a = math.pi * (0.15 + 0.7 * k / 8)
            s.add(f'<circle cx="{300 - 60 * math.cos(a):.1f}" cy="{top + 4 + 52 * math.sin(a):.1f}" r="9" fill="{n}"/>')
    if o.get("bag"):
        b = o["bag"]
        s.add(f'<path d="M200,{top} L420,760" stroke="{shade(b, 0.8)}" stroke-width="12"/>')
        s.add(f'<rect x="380" y="720" width="110" height="96" rx="16" fill="{b}"/><rect x="380" y="720" width="110" height="26" rx="10" fill="{shade(b, 0.8)}"/>')


def head(s, o, drop, tilt):
    cx, cy, r = 300, 178 + drop, 96
    skin = o["skin"]
    s.add(f'<rect x="272" y="{240 + drop * 0.5:.0f}" width="56" height="{100 - drop * 0.4:.0f}" fill="{shade(skin, 0.85)}"/>')   # neck
    s.add(f'<g transform="rotate({tilt} {cx} {cy + 60})">')
    hair = o.get("hair") or [None, "bald"]
    hc, hs = hair if isinstance(hair, list) else (hair, "short")
    if hs == "long" and hc:
        s.add(f'<path d="M{cx - 104},{cy - 10} C{cx - 110},{cy + 120} {cx - 90},{cy + 190} {cx - 60},{cy + 200} L{cx + 60},{cy + 200} '
              f'C{cx + 90},{cy + 190} {cx + 110},{cy + 120} {cx + 104},{cy - 10} Z" fill="{hc}"/>')
    s.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{skin}"/>')
    s.add(f'<path d="M{cx + 30},{cy - r + 6} A{r},{r} 0 0 1 {cx + 30},{cy + r - 6} C{cx + 70},{cy + 40} {cx + 74},{cy - 40} {cx + 30},{cy - r + 6} Z" fill="{shade(skin, 0.85)}"/>')
    s.add(f'<ellipse cx="{cx - r + 4}" cy="{cy + 10}" rx="16" ry="24" fill="{shade(skin, 0.9)}"/><ellipse cx="{cx + r - 4}" cy="{cy + 10}" rx="16" ry="24" fill="{shade(skin, 0.8)}"/>')
    if o.get("earrings"):
        e = o["earrings"]
        s.add(f'<circle cx="{cx - r + 2}" cy="{cy + 44}" r="10" fill="{e}"/><circle cx="{cx + r - 2}" cy="{cy + 44}" r="10" fill="{e}"/>')
    if hc and hs in ("short", "long", "bun", "curly"):
        if hs == "curly":
            for k in range(9):
                import math
                a = math.pi * (1.05 + 0.9 * k / 8)
                s.add(f'<circle cx="{cx + 88 * math.cos(a):.0f}" cy="{cy - 8 + 80 * math.sin(a):.0f}" r="34" fill="{hc}"/>')
        else:
            s.add(f'<path d="M{cx - r - 4},{cy + 6} C{cx - r - 10},{cy - 90} {cx - 40},{cy - r - 22} {cx + 10},{cy - r - 16} '
                  f'C{cx + 70},{cy - r - 12} {cx + r + 10},{cy - 70} {cx + r + 4},{cy + 6} C{cx + 60},{cy - 50} {cx - 60},{cy - 60} {cx - r - 4},{cy + 6} Z" fill="{hc}"/>')
        if hs == "bun":
            s.add(f'<circle cx="{cx}" cy="{cy - r - 22}" r="40" fill="{hc}"/>')
    hat = o.get("hat")
    if hat:
        kind, hcol = hat
        top = cy - r
        if kind == "cap":
            s.add(f'<path d="M{cx - 98},{cy - 20} C{cx - 96},{top - 30} {cx + 96},{top - 30} {cx + 98},{cy - 20} Z" fill="{hcol}"/>')
            s.add(f'<path d="M{cx - 20},{cy - 26} L{cx - 150},{cy - 16} C{cx - 150},{cy - 2} {cx - 30},{cy - 6} {cx - 20},{cy - 14} Z" fill="{shade(hcol, 0.8)}"/>')
        elif kind == "fez":
            s.add(f'<path d="M{cx - 60},{top + 20} L{cx - 48},{top - 70} L{cx + 48},{top - 70} L{cx + 60},{top + 20} Z" fill="{hcol}"/>')
            s.add(f'<path d="M{cx + 48},{top - 70} C{cx + 70},{top - 40} {cx + 76},{top} {cx + 70},{top + 30}" stroke="#1a1410" stroke-width="6" fill="none"/>')
        elif kind == "headscarf":
            fx, fy, rx, ry = cx, cy + 14, 74, 80
            s.add(f'<path d="M{cx - r - 16},{cy + 80} C{cx - r - 24},{top - 44} {cx + r + 24},{top - 44} {cx + r + 16},{cy + 80} '
                  f'C{cx + 80},{cy + 150} {cx - 80},{cy + 150} {cx - r - 16},{cy + 80} Z '
                  f'M{fx - rx},{fy} A{rx},{ry} 0 1 0 {fx + rx},{fy} A{rx},{ry} 0 1 0 {fx - rx},{fy} Z" '
                  f'fill="{hcol}" fill-rule="evenodd"/>')
            s.add(f'<path d="M{cx + 40},{cy - r} C{cx + r + 30},{cy - 40} {cx + r + 24},{cy + 80} {cx + 50},{cy + 130} L{cx + 70},{cy + 70} C{cx + 76},{cy} {cx + 60},{cy - 50} {cx + 40},{cy - r} Z" fill="{shade(hcol, 0.82)}"/>')
        elif kind == "beret":
            s.add(f'<ellipse cx="{cx - 10}" cy="{top + 10}" rx="110" ry="40" fill="{hcol}"/><circle cx="{cx - 10}" cy="{top - 28}" r="10" fill="{hcol}"/>')
        elif kind in ("bowler", "tophat"):
            h = 70 if kind == "bowler" else 150
            s.add(f'<ellipse cx="{cx}" cy="{top + 18}" rx="130" ry="20" fill="{hcol}"/>')
            if kind == "bowler":
                s.add(f'<path d="M{cx - 86},{top + 18} C{cx - 86},{top - h} {cx + 86},{top - h} {cx + 86},{top + 18} Z" fill="{hcol}"/>')
            else:
                s.add(f'<rect x="{cx - 80}" y="{top - h + 18}" width="160" height="{h}" fill="{hcol}"/>')
            s.add(f'<rect x="{cx - 84}" y="{top}" width="168" height="16" fill="{shade(hcol, 1.6)}"/>')
        elif kind == "chef":
            s.add(f'<rect x="{cx - 80}" y="{top - 50}" width="160" height="70" fill="{hcol}"/>')
            for k in (-60, 0, 60):
                s.add(f'<circle cx="{cx + k}" cy="{top - 80}" r="56" fill="{hcol}"/>')
        elif kind == "straw":
            s.add(f'<ellipse cx="{cx}" cy="{top + 22}" rx="170" ry="30" fill="{hcol}"/>')
            s.add(f'<path d="M{cx - 80},{top + 22} C{cx - 80},{top - 70} {cx + 80},{top - 70} {cx + 80},{top + 22} Z" fill="{hcol}"/>')
            s.add(f'<rect x="{cx - 82}" y="{top}" width="164" height="18" fill="#7c2533"/>')
    s.add('</g>')


def figure(pose="down", expr="neutral", blink=False, look=(0, 0), mouth=None, arms=None, lift=(0.0, 0.0), shadow=True, outfit=None):
    o = dict(DEFAULT)
    o.update(outfit or {})
    bw = BUILD.get(o.get("build", "regular"), 1.0)
    hd, shd = POSTURE.get(expr, (0, 0))
    tilt = {"sad": -6, "happy": 4}.get(expr, 0)
    s = Svg()
    if shadow:
        s.add('<ellipse cx="300" cy="1456" rx="180" ry="20" fill="#000" opacity="0.22"/>')
    arms = arms if arms is not None else ARMS[pose]
    s.add(f'<g transform="translate(300,0) scale({bw:.3f},1) translate(-300,0)">')
    legs(s, o, lift)
    torso(s, o, shd)
    s.add('</g>')
    head(s, o, hd, tilt)
    s.add(f'<g transform="translate(300,0) scale({bw:.3f},1) translate(-300,0)">')
    for sh, el, wr, kind, front in arms:                  # arms over the body: flat style, always readable
        arm(s, sh, el, wr, kind, o, sh[0] > 300, shd)
    s.add('</g>')
    return s.svg()


POSES = {n: dict(pose=p, expr=e) for n, (p, e, _) in BASES.items()}

if __name__ == "__main__":
    for f in os.listdir(D):
        if f.endswith(".svg"):
            os.remove(os.path.join(D, f))
    for name, kw in POSES.items():
        with open(os.path.join(D, name + ".svg"), "w") as f:
            f.write(figure(**kw))
    print("wrote", len(POSES), "poses")
