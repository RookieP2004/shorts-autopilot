"""Professor Ved - the channel's explainer (late 20s to early 30s: young, sharp, calm, wise beyond his years).

Semi-realistic 2D ("animated imitation of the real world"). Every pose is generated from the SAME
parts below, so he never drifts between videos. Style rules baked in:
  * key light: warm, from upper-left  -> shadows fall on his right side (viewer's right)
  * shadows: one hard-edged cel shadow per part, colour = base darkened and pushed toward cool blue
  * highlights: small warm sheen on the lit side; cool rim light on the right contour
  * lines: warm dark brown, never black; outer contour 4.5, inner detail 2.2, fine detail 1.3
Run:  python make.py        -> writes every pose SVG next to this file
"""
import math
import os

D = os.path.dirname(os.path.abspath(__file__))
W, H = 600, 1400

# ---------------- palette ----------------
LINE = "#2b1d16"
SKIN = "#dba077"
HAIR = "#17171c"
BEARD = "#3a2c26"
SHEEN = "#5d6680"
BROW = "#18171a"
IRIS = "#5a3a22"
SHIRT = "#fbf9f4"
BELT = "#17140f"
SILVER = "#c9ccd1"
STRAP = "#3a2a20"
TIE = "#7c2533"
VEST = "#6e4b33"
JACKET = "#34425c"
TROUSER = "#262a33"
SHOE = "#1a1412"
GOLD = "#d4a64a"
SQUARE = "#d9a441"
RIM = "#bfe6ff"
KEY = "#fff1d6"
COOL = (46, 58, 110)
LW_OUT, LW_IN, LW_FINE = 4.5, 2.2, 1.3


def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def hexc(c):
    return "#%02x%02x%02x" % tuple(max(0, min(255, int(round(v)))) for v in c)


def shade(c, k=0.76, cool=0.22):
    r = rgb(c)
    return hexc([r[i] * k * (1 - cool) + COOL[i] * cool for i in range(3)])


def soft_shade(c, soft):
    if soft == "white":
        return shade(c, 0.92, 0.12)
    return shade(c, 0.8, 0.22) if soft else shade(c)


def deep(c):
    return shade(c, 0.5, 0.35)


def light(c, k=0.3):
    r, w = rgb(c), rgb(KEY)
    return hexc([r[i] * (1 - k) + w[i] * k for i in range(3)])


class Svg:
    def __init__(self):
        self.defs, self.body, self.n = [], [], 0
        # one light falloff for the whole figure: warm top-left -> cool dark bottom-right
        self.defs.append('<linearGradient id="form" gradientUnits="userSpaceOnUse" x1="170" y1="120" x2="470" y2="1500">'
                         '<stop offset="0" stop-color="#fff1d6" stop-opacity="0.16"/>'
                         '<stop offset="0.45" stop-color="#fff1d6" stop-opacity="0"/>'
                         '<stop offset="1" stop-color="#0b1030" stop-opacity="0.18"/></linearGradient>')

    def uid(self, p="c"):
        self.n += 1
        return f"{p}{self.n}"

    def add(self, s):
        self.body.append(s)

    def part(self, d, base, shadow=None, hl=None, lw=LW_OUT, deep_d=None, rim=None, line=True, soft=False):
        """A filled shape with cel shadow / highlight clipped inside it, then its outline."""
        cid = self.uid()
        self.defs.append(f'<clipPath id="{cid}"><path d="{d}"/></clipPath>')
        out = [f'<path d="{d}" fill="{base}"/>']
        inner = []
        if shadow:
            inner.append(f'<path d="{shadow}" fill="{soft_shade(base, soft)}"/>')
        if deep_d:
            inner.append(f'<path d="{deep_d}" fill="{deep(base)}"/>')
        if hl:
            inner.append(f'<path d="{hl}" fill="{light(base)}" opacity="0.85"/>')
        inner.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#form)"/>')
        out.append(f'<g clip-path="url(#{cid})">{"".join(inner)}</g>')
        if line:
            out.append(f'<path d="{d}" fill="none" stroke="{LINE}" stroke-width="{lw}" stroke-linejoin="round"/>')
        if rim:
            out.append(f'<path d="{rim}" fill="none" stroke="{RIM}" stroke-width="2.6" stroke-linecap="round" opacity="0.75"/>')
        self.add("".join(out))

    def line(self, d, w=LW_IN, color=LINE, op=1.0, cap="round"):
        self.add(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="{cap}" '
                 f'stroke-linejoin="round" opacity="{op}"/>')

    def tube(self, pts, width, base, shadow_side=1, soft=False, cap="round"):
        """Limb: an outlined thick stroke along pts, with a cel shadow strip on one side."""
        d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        self.add(f'<path d="{d}" fill="none" stroke="{LINE}" stroke-width="{width + 2 * LW_OUT}" '
                 f'stroke-linecap="{cap}" stroke-linejoin="round"/>')
        self.add(f'<path d="{d}" fill="none" stroke="{base}" stroke-width="{width}" stroke-linecap="{cap}" '
                 f'stroke-linejoin="round"/>')
        # shadow strip offset to the shadow side, perpendicular to each segment
        segs = []
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            L = math.hypot(x1 - x0, y1 - y0) or 1
            nx, ny = -(y1 - y0) / L, (x1 - x0) / L
            if nx < 0:
                nx, ny = -nx, -ny  # always toward +x (viewer's right) = shadow side
            o = width * 0.27 * shadow_side
            segs.append(((x0 + nx * o, y0 + ny * o), (x1 + nx * o, y1 + ny * o)))
        sd = "M" + " L".join(f"{a[0]:.1f},{a[1]:.1f}" for a, _ in segs) + f" L{segs[-1][1][0]:.1f},{segs[-1][1][1]:.1f}"
        self.add(f'<path d="{sd}" fill="none" stroke="{soft_shade(base, soft)}" stroke-width="{width * 0.42}" '
                 f'stroke-linecap="{cap}" stroke-linejoin="round"/>')
        hd = "M" + " L".join(f"{x - width * 0.22:.1f},{y:.1f}" for x, y in pts)
        self.add(f'<path d="{hd}" fill="none" stroke="{light(base, 0.18)}" stroke-width="{width * 0.12}" '
                 f'stroke-linecap="{cap}" opacity="0.6"/>')

    def svg(self):
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
                f'<defs>{"".join(self.defs)}</defs>{"".join(self.body)}</svg>')


def mirror(d):
    """Mirror an SVG path (absolute M/L/C/Q/Z commands, x,y pairs) around x=300."""
    import re
    out = []
    for tok in re.findall(r"[MLCQZ]|-?[\d.]+,-?[\d.]+", d):
        if "," in tok:
            x, y = tok.split(",")
            out.append(f"{600 - float(x):g},{y}")
        else:
            out.append(tok)
    return " ".join(out)


def curls(cx, cy, rx, ry, a0, a1, n, amp=0.06, seed=3):
    """Scalloped arc (wavy hair silhouette) from angle a0 to a1 (radians, y down). Returns 'L x,y Q ...' fragments."""
    import random
    rnd = random.Random(seed)
    pts = []
    for i in range(n + 1):
        a = a0 + (a1 - a0) * i / n
        k = 1 + rnd.uniform(-0.02, 0.03)
        pts.append((cx + rx * k * math.cos(a), cy + ry * k * math.sin(a)))
    d = f"{pts[0][0]:.1f},{pts[0][1]:.1f}"
    out = []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        ox, oy = mx - cx, my - cy
        L = math.hypot(ox, oy) or 1
        b = (amp + rnd.uniform(0, amp * 0.6)) * max(rx, ry)
        out.append(f"Q{mx + ox / L * b:.1f},{my + oy / L * b:.1f} {x1:.1f},{y1:.1f}")
    return d, " ".join(out)


# =====================================================================================
#  HEAD (front)
# =====================================================================================
FACE = ("M300,50 C352,50 380,86 382,130 C384,172 374,204 354,226 C336,246 318,256 300,256 "
        "C282,256 264,246 246,226 C226,204 216,172 218,130 C220,86 248,50 300,50 Z")


def head(s, expr="neutral", blink=False, look=(0, 0)):
    # ears (short hair leaves them visible)
    ear = "M226,132 C212,122 203,132 205,149 C207,165 217,176 230,172 Z"
    s.part(ear, SKIN, shadow="M190,150 L240,150 L240,190 L190,190 Z", lw=LW_IN + 0.8)
    s.part(mirror(ear), SKIN, shadow="M360,110 L410,110 L410,190 L360,190 Z", lw=LW_IN + 0.8)
    s.line("M212,140 C208,150 210,162 218,168", LW_FINE, op=0.6)
    s.line("M388,140 C392,150 390,162 382,168", LW_FINE, op=0.6)

    # face
    s.part(FACE, SKIN,
           shadow=("M300,40 C356,46 386,86 384,130 C384,174 372,210 352,232 C334,254 316,266 300,268 "
                   "C326,246 348,214 354,176 C360,132 350,82 300,40 Z"),
           hl="M246,96 C252,78 266,66 284,62 C270,74 262,90 258,108 Z",
           rim="M372,96 C382,136 378,186 356,226")
    # eye sockets + cheek warmth
    s.add('<ellipse cx="252" cy="190" rx="20" ry="11" fill="#d9706a" opacity="0.18"/>')
    s.add('<ellipse cx="348" cy="190" rx="20" ry="11" fill="#c0605e" opacity="0.15"/>')
    # forehead wrinkles (age / wisdom)

    # short hair: textured waves on top swept up and back, tight tapered sides (young)
    st, arc = curls(300, 128, 86, 96, math.pi * 1.02, math.pi * 1.98, 11, 0.06, seed=12)
    hair = (f"M{st} {arc} C386,132 382,142 378,146 C376,124 368,108 354,98 C342,92 328,92 316,96 "
            f"C306,88 292,86 280,90 C266,94 252,100 242,110 C232,120 226,132 222,146 C218,142 214,132 {st} Z")
    s.part(hair, HAIR, soft=True,
           shadow="M330,26 C374,40 396,90 384,148 L364,148 C370,104 358,62 330,40 Z",
           hl="M240,70 C256,48 284,38 312,36 C288,46 266,58 254,80 Z",
           rim="M372,62 C386,86 390,116 384,140")
    for d in ("M246,104 C254,80 274,62 300,56", "M280,90 C292,70 316,60 342,64", "M316,96 C332,82 352,80 368,92",
              "M232,124 C232,100 242,80 258,66", "M300,56 C320,48 344,52 360,66"):
        s.line(d, 1.7, color=SHEEN, op=0.85)
    s.line("M250,60 C264,46 282,40 300,38", 2.6, color="#a3abc0", op=0.5)
    taper = "M222,138 C221,130 223,122 227,116 L232,118 C229,124 228,130 228,138 Z"   # short sides above the ears
    s.part(taper, HAIR, soft=True, lw=LW_FINE)
    s.part(mirror(taper), HAIR, soft=True, lw=LW_FINE)

    # brows by expression: (inner_dy, outer_dy)
    bi, bo = {"neutral": (2, -1), "smile": (-3, 1), "talk": (-3, -1), "talk2": (-1, 0), "think": (6, 1),
              "surprised": (-14, -9), "serious": (8, -1), "warm": (-4, 2), "laugh": (-5, 2)}.get(expr, (0, 0))
    rlift = -9 if expr == "think" else 0     # thinking: one sceptical raised brow
    lb = (f"M245,{122+bo} C250,{110+bo} 268,{103+bi} 292,{110+bi} C286,{114+bi} 276,{115+bi} 268,{117+bi} "
          f"C259,{119+bo} 251,{123+bo} 245,{128+bo} Z")
    s.part(lb, BROW, lw=LW_FINE + 0.5)
    rb = mirror(lb)
    if rlift:
        rb = f'" transform="translate(0,{rlift}) rotate(-6 330 115)'  # placeholder, replaced below
        rb = mirror(lb)
        s.add(f'<g transform="translate(0,{rlift}) rotate(-5 330 115)">')
        s.part(rb, BROW, soft=True, shadow="M300,90 L360,90 L360,130 L300,130 Z", lw=LW_FINE + 0.5)
        s.add('</g>')
    else:
        s.part(rb, BROW, soft=True, shadow="M300,90 L360,90 L360,130 L300,130 Z", lw=LW_FINE + 0.5)
    if expr in ("serious", "think"):
        s.line("M294,118 l2,9 M306,118 l-2,9", LW_FINE, op=0.55)        # frown lines

    for side in (-1, 1):
        for k in range(4):
            x0 = 300 + side * (52 - k * 9)
            s.line(f"M{x0},{118 + (bo if k < 2 else bi) - k} l{side * -9},-5", LW_FINE,
                   color=shade(BROW, 0.7, 0.3), op=0.8)

    # eyes
    lx, ly = look
    for side in (-1, 1):
        cx = 300 + side * 29
        if blink or expr == "laugh":
            s.line(f"M{cx-17},142 C{cx-8},{149} {cx+8},149 {cx+17},142", 3.0)
            continue
        open_ = {"surprised": 12, "smile": 6, "warm": 7.5, "serious": 7.5, "think": 8}.get(expr, 9)
        eye = (f"M{cx-18},142 C{cx-10},{142-open_-1} {cx+10},{142-open_-1} {cx+18},142 "
               f"C{cx+10},{142+open_*0.75} {cx-10},{142+open_*0.75} {cx-18},142 Z")
        eid = s.uid()
        s.defs.append(f'<clipPath id="{eid}"><path d="{eye}"/></clipPath>')
        s.add(f'<path d="{eye}" fill="#f4eee6"/>')
        s.add(f'<g clip-path="url(#{eid})"><circle cx="{cx+lx}" cy="{141.5+ly}" r="7.6" fill="{IRIS}"/>'
              f'<circle cx="{cx+lx}" cy="{141.5+ly}" r="3.4" fill="#120a07"/>'
              f'<circle cx="{cx+lx-2}" cy="{139.5+ly}" r="2.2" fill="#fff"/>'
              f'<path d="M{cx-20},{130} L{cx+20},130 L{cx+20},{140-open_+3} L{cx-20},{140-open_+3} Z" fill="#000" opacity="0.18"/></g>')
        s.line(f"M{cx-19},142 C{cx-10},{141-open_-2} {cx+10},{141-open_-2} {cx+19},141", 3.0)  # upper lid
        if expr in ("smile", "warm"):
            s.line(f"M{cx-14},{148} C{cx-5},{143} {cx+5},{143} {cx+14},{148}", 1.8, op=0.8)   # cheek squint
        else:
            s.line(f"M{cx-11},{144+open_*0.5} C{cx-4},{146+open_*0.5} {cx+5},{146+open_*0.5} {cx+12},{143+open_*0.5}",
                   LW_FINE, op=0.3)


    # nose
    s.add('<path d="M306,150 C312,172 316,188 313,198 L303,200 C306,186 305,170 302,152 Z" '
          f'fill="{shade(SKIN)}" opacity="0.8"/>')
    s.line("M297,152 C296,170 292,186 289,196", LW_FINE, op=0.5)
    s.line("M284,199 C290,208 310,208 316,199", LW_IN)
    s.line("M290,202 q4,3 7,1 M310,202 q-4,3 -7,1", LW_FINE, op=0.7)
    s.add(f'<ellipse cx="296" cy="194" rx="5" ry="3" fill="{light(SKIN, 0.45)}" opacity="0.8"/>')

    # mouth (drawn before beard/moustache so they overlap it)
    m = {
        "neutral": ("line", "M287,239 Q300,246 313,239"),
        "serious": ("line", "M287,241 Q300,240 313,241"),
        "think": ("line", "M289,241 Q300,239 311,243"),
        "smile": ("line", "M284,237 Q300,248 316,237"),
        "warm": ("line", "M285,238 Q300,246 315,238"),
        "talk": ("open", "M287,236 Q300,233 313,236 Q310,250 300,251 Q290,250 287,236 Z"),
        "talk2": ("open", "M289,237 Q300,235 311,237 Q308,245 300,246 Q292,245 289,237 Z"),
        "surprised": ("open", "M292,235 Q300,231 308,235 Q310,252 300,254 Q290,252 292,235 Z"),
        "laugh": ("open", "M284,235 Q300,233 316,235 Q312,255 300,256 Q288,255 284,235 Z"),
    }[expr if expr in ("neutral", "serious", "think", "smile", "warm", "surprised", "laugh", "talk2") else
      ("talk" if expr == "talk" else "neutral")]
    if m[0] == "line":
        s.line(m[1], 2.6)
        s.line("M293,247 Q300,249 307,247", LW_FINE, op=0.5)
    else:
        mid = s.uid()
        s.defs.append(f'<clipPath id="{mid}"><path d="{m[1]}"/></clipPath>')
        s.add(f'<path d="{m[1]}" fill="#3b1612"/>')
        s.add(f'<g clip-path="url(#{mid})"><rect x="280" y="229" width="40" height="8" fill="#efe8de"/>'
              f'<ellipse cx="300" cy="256" rx="10" ry="6" fill="#b4504e"/></g>')
        s.add(f'<path d="{m[1]}" fill="none" stroke="{LINE}" stroke-width="2.4" stroke-linejoin="round"/>')

    # short, neat young beard: dense along the jaw and chin, lighter on the cheeks, trimmed at the chin
    BFILL = hexc([rgb(SKIN)[i] * 0.2 + rgb(HAIR)[i] * 0.8 for i in range(3)])
    CHEEK = hexc([rgb(SKIN)[i] * 0.8 + rgb(HAIR)[i] * 0.2 for i in range(3)])
    cheek = ("M224,150 C224,172 230,194 240,212 L262,226 C252,210 244,190 240,166 C238,158 236,152 234,148 Z")
    s.part(cheek, CHEEK, soft=True, line=False)
    s.part(mirror(cheek), CHEEK, soft=True, line=False)
    beard = ("M226,156 C226,194 242,230 266,252 C280,264 292,272 300,272 C308,272 320,264 334,252 "
             "C358,230 374,194 374,156 L366,160 C364,194 352,216 338,228 L334,240 C324,252 312,256 300,256 "
             "C288,256 276,252 266,240 L262,228 C248,216 236,194 234,160 Z")
    s.part(beard, BFILL, soft=True, line=False,
           shadow="M316,250 C342,246 360,222 368,160 L400,160 L400,300 L300,300 Z")
    import random as _r
    rr = _r.Random(7)
    for _ in range(60):   # short hair texture
        x = 300 + rr.choice((-1, 1)) * rr.uniform(8, 66)
        y = rr.uniform(170, 268)
        if abs(x - 300) < 72 - max(0, y - 200) * 0.95 and abs(x - 300) > 62 - max(0, y - 170) * 0.9 and not (abs(x - 300) < 36 and y < 256):
            s.line(f"M{x:.1f},{y:.1f} l{rr.uniform(-1,1):.1f},{rr.uniform(3,5):.1f}", 1.1, color=SHEEN, op=0.6)
    must = ("M276,226 C284,219 292,218 300,220 C308,218 316,219 324,226 C325,228 324,229 322,229 "
            "C315,227 308,226 300,227 C292,226 285,227 278,229 C276,229 275,228 276,226 Z")
    s.part(must, hexc([rgb(SKIN)[i] * 0.38 + rgb(HAIR)[i] * 0.62 for i in range(3)]), soft=True, shadow="M304,206 L346,206 L346,250 L304,250 Z", line=False)
    s.line("M226,156 C226,194 242,230 266,252 C280,264 292,272 300,272 C308,272 320,264 334,252 "
           "C358,230 374,194 374,156", LW_IN, op=0.85)                                           # jaw silhouette

    # (no spectacles)


# =====================================================================================
#  BODY (front)
# =====================================================================================
TORSO = ("M300,280 C266,280 196,288 160,304 C134,316 124,342 128,370 C134,398 152,414 170,430 "
         "C176,520 182,640 190,730 C192,770 194,796 196,814 L404,814 C406,796 408,770 410,730 "
         "C418,640 424,520 430,430 C448,414 466,398 472,370 C476,342 466,316 440,304 C404,288 334,280 300,280 Z")


def legs(s):
    leg = "M196,826 L298,826 L294,1340 L218,1340 C212,1120 204,960 196,826 Z"
    s.part(leg, TROUSER, shadow="M262,816 L310,816 L304,1348 L270,1348 Z", hl="M208,880 L214,880 L222,1310 L217,1310 Z")
    s.part(mirror(leg), TROUSER, shadow="M330,816 L420,816 L420,1348 L330,1348 Z")
    s.line("M248,880 L254,1330", LW_FINE, color="#4a4f5c", op=0.8)
    s.line("M352,880 L346,1330", LW_FINE, color="#4a4f5c", op=0.6)
    for x in (240, 360):  # knee folds
        s.line(f"M{x-14},1050 q14,8 28,0", LW_FINE, color="#4a4f5c", op=0.5)
    shoe = ("M208,1330 L294,1330 L296,1366 C296,1382 288,1390 272,1390 L188,1390 C172,1390 168,1374 180,1366 "
            "C192,1356 202,1346 208,1330 Z")
    hl = "M190,1368 C198,1362 210,1360 222,1362 L218,1368 Z"
    s.part(shoe, SHOE, shadow="M240,1374 L300,1374 L300,1398 L240,1398 Z", hl=hl)
    s.part(mirror(shoe), SHOE, shadow="M300,1318 L440,1318 L440,1398 L300,1398 Z", hl=mirror(hl))


def torso(s):
    # neck (a little thicker: fit)

    s.part(TORSO, SHIRT, soft="white",
           shadow="M350,280 C410,290 474,312 472,372 C462,406 440,424 430,444 L412,820 L376,820 C394,700 398,520 386,330 Z",
           hl="M150,326 C140,344 140,366 148,384 L158,382 C154,366 154,348 160,332 Z")
    # neck flowing into the open-collar V: one skin shape, outline only on the neck sides
    neck = ("M262,226 C262,256 258,278 248,292 C266,300 280,330 300,388 C320,330 334,300 352,292 "
            "C342,278 338,256 338,226 Z")
    s.part(neck, SKIN, line=False,
           shadow="M312,220 C330,250 336,280 350,292 C334,306 320,340 300,392 L360,392 L360,220 Z",
           deep_d="M250,222 L350,222 L350,252 Q300,276 250,252 Z")
    s.line("M262,226 C262,256 258,278 248,292", LW_OUT)
    s.line("M338,226 C338,256 342,278 352,292", LW_OUT)
    s.line("M276,300 C288,312 296,334 300,352", LW_FINE, op=0.25)   # sternocleido hint
    s.line("M286,352 Q300,360 314,352", LW_FINE, op=0.35)   # collarbone hint
    # collar flaps lying open
    for d in ("M262,284 C252,296 250,316 254,338 L286,356 L272,300 Z",):
        s.part(d, SHIRT, soft="white", lw=LW_IN)
        s.part(mirror(d), SHIRT, soft="white", shadow="M300,280 L360,280 L360,360 L300,360 Z", lw=LW_IN)
    # placket + buttons (top button open)
    s.line("M300,388 L300,806", LW_IN)
    s.line("M308,392 L308,806", LW_FINE, op=0.4)
    for y in (430, 500, 570, 640, 710, 780):
        s.add(f'<circle cx="304" cy="{y}" r="4" fill="#ffffff" stroke="#8a8f9c" stroke-width="1.4"/>')
    # fit: chest + fabric pull lines, tucked waist folds
    for d in ("M196,446 C230,486 270,488 294,470", "M236,560 C254,568 276,568 292,560", "M240,630 C256,636 276,636 292,630",
              "M210,770 Q220,756 234,764", "M250,790 Q260,778 272,788", "M190,340 C210,330 236,322 256,316"):
        s.line(d, 1.8, color="#a3abbb", op=0.95)
        s.line(mirror(d), 1.8, color="#a3abbb", op=0.75)
    s.add('<path d="M206,458 C236,490 270,492 294,478 L294,486 C268,500 234,498 210,474 Z" fill="#c9cfdb" opacity="0.35"/>')
    s.add('<path d="M394,458 C364,490 330,492 306,478 L306,486 C332,500 366,498 390,474 Z" fill="#b9c0cf" opacity="0.4"/>')
    # belt + buckle
    s.part("M194,806 L406,806 L408,838 L192,838 Z", BELT, shadow="M300,800 L420,800 L420,840 L300,840 Z", lw=LW_IN)
    s.add(f'<rect x="286" y="806" width="28" height="28" rx="4" fill="none" stroke="{SILVER}" stroke-width="5"/>')
    s.add(f'<rect x="286" y="806" width="28" height="28" rx="4" fill="none" stroke="{LINE}" stroke-width="1.4"/>')


def cuff_and_hand(s, wrist, angle, kind, flip=False, cuff=False, watch=False):
    """wrist=(x,y), angle in degrees (0 = hand pointing straight down)."""
    x, y = wrist
    t = f'transform="translate({x:.1f},{y:.1f}) rotate({angle:.1f})"'
    g = []
    def P(d, base, shadow=None, lw=LW_IN):
        cid = s.uid()
        s.defs.append(f'<clipPath id="{cid}"><path d="{d}"/></clipPath>')
        g.append(f'<path d="{d}" fill="{base}"/>')
        if shadow:
            g.append(f'<g clip-path="url(#{cid})"><path d="{shadow}" fill="{shade(base)}"/></g>')
        g.append(f'<path d="{d}" fill="none" stroke="{LINE}" stroke-width="{lw}" stroke-linejoin="round"/>')
    def finger(d, w=13):
        g.append(f'<path d="{d}" fill="none" stroke="{LINE}" stroke-width="{w+2*LW_IN}" stroke-linecap="round"/>')
        g.append(f'<path d="{d}" fill="none" stroke="{SKIN}" stroke-width="{w}" stroke-linecap="round"/>')
    SH = "M12,-10 L40,-10 L40,120 L12,120 Z"
    if kind == "relaxed":
        P("M-21,6 C-27,28 -27,52 -21,70 C-16,86 -6,97 5,98 C15,98 21,88 23,76 C26,56 26,30 22,6 Z", SKIN, SH)
        g.append(f'<path d="M-12,52 C-13,64 -12,76 -8,86 M-1,56 C-1,70 0,82 3,92 M10,54 C11,66 12,76 14,84" '
                 f'stroke="{LINE}" stroke-width="{LW_FINE}" fill="none" opacity="0.55"/>')
        g.append(f'<path d="M-18,40 Q0,46 18,40" stroke="{LINE}" stroke-width="{LW_FINE}" fill="none" opacity="0.35"/>')
        finger("M20,20 C30,32 32,48 26,60", 12)
    elif kind == "open":   # palm toward viewer, fingers along +y (rotate so they point up)
        P("M-26,8 C-28,30 -26,48 -22,58 L22,58 C26,48 28,30 26,8 Z", SKIN, SH)
        for fx, ln in ((-17, 40), (-6, 46), (6, 44), (17, 36)):
            finger(f"M{fx},54 L{fx*1.15:.1f},{54+ln}", 11)
        finger("M-24,24 C-40,34 -46,46 -48,58", 13)
        g.append(f'<path d="M-14,40 Q0,48 14,38" stroke="{LINE}" stroke-width="{LW_FINE}" fill="none" opacity="0.5"/>')
    elif kind == "point":  # fist with index finger along +y
        P("M-24,8 C-28,30 -24,56 -10,64 L18,64 C28,54 28,30 24,8 Z", SKIN, SH)
        finger("M10,58 L12,118", 12)
        g.append(f'<path d="M-16,52 q8,10 18,8 M-18,38 q10,8 20,6" stroke="{LINE}" stroke-width="{LW_FINE}" fill="none" opacity="0.6"/>')
        finger("M-22,24 C-30,36 -24,48 -12,50", 12)
    elif kind == "chin":   # loose curled hand
        P("M-24,8 C-30,34 -24,60 -6,70 C8,76 22,66 26,50 C30,34 28,20 24,8 Z", SKIN, SH)
        g.append(f'<path d="M-14,48 q12,8 30,0 M-16,60 q12,6 26,-2" stroke="{LINE}" stroke-width="{LW_FINE}" fill="none" opacity="0.7"/>')
        finger("M-22,22 C-34,36 -30,52 -16,58", 12)
    if cuff:
        g.insert(0, f'<rect x="-28" y="-14" width="56" height="22" rx="5" fill="{SHIRT}" stroke="{LINE}" stroke-width="{LW_IN}"/>')
    if watch:
        g.append(f'<rect x="-21" y="-12" width="42" height="13" rx="3" fill="{STRAP}" stroke="{LINE}" stroke-width="1.6"/>'
                 f'<circle cx="0" cy="-6" r="9" fill="{GOLD}" stroke="{LINE}" stroke-width="1.6"/>'
                 f'<circle cx="0" cy="-6" r="5.5" fill="#f4efe4"/>')
    sx = -1.32 if flip else 1.32
    s.add(f'<g {t} ><g transform="scale({sx},1.32)">{"".join(g)}</g></g>')


# arm configurations: (shoulder, elbow, wrist, hand_kind, extra_angle, forearm_in_front)
L_SH, R_SH = (168, 356), (432, 356)
ARMS = {
    "down": [(L_SH, (128, 580), (132, 772), "relaxed", 0, False), (R_SH, (472, 580), (468, 772), "relaxed", 0, False)],
    "explain": [(L_SH, (120, 594), (76, 464), "open", 0, False), (R_SH, (472, 580), (468, 772), "relaxed", 0, False)],
    "point": [(L_SH, (98, 440), (44, 316), "point", 0, False), (R_SH, (472, 580), (468, 772), "relaxed", 0, False)],
    "think": [(L_SH, (190, 610), (262, 350), "chin", 0, True), (R_SH, (472, 580), (468, 772), "relaxed", 0, False)],
    "welcome": [(L_SH, (118, 580), (70, 706), "open", 0, False), (R_SH, (482, 580), (530, 706), "open", 0, False)],
    "both_explain": [(L_SH, (120, 594), (76, 464), "open", 0, False), (R_SH, (480, 594), (524, 464), "open", 0, False)],
}
SLEEVE = 88
FOREARM = 60


def sleeve(s, shoulder, elbow, wrist, upper=True):
    """White shirt sleeve rolled just below the elbow, then a bare forearm. Seams hide under the cuff band."""
    dx, dy = wrist[0] - elbow[0], wrist[1] - elbow[1]
    L = math.hypot(dx, dy) or 1
    ux, uy = dx / L, dy / L
    nx, ny = -uy, ux
    roll = (elbow[0] + 0.3 * dx, elbow[1] + 0.3 * dy)
    band_len = 26
    a = (roll[0] - ux * band_len / 2, roll[1] - uy * band_len / 2)
    b = (roll[0] + ux * band_len / 2, roll[1] + uy * band_len / 2)
    s.tube([b, wrist], FOREARM, SKIN, cap="butt")                                   # forearm, from under the band
    mid = ((b[0] + wrist[0]) / 2, (b[1] + wrist[1]) / 2)
    s.line(f"M{b[0]-nx*12:.1f},{b[1]-ny*12:.1f} Q{mid[0]-nx*16:.1f},{mid[1]-ny*16:.1f} {wrist[0]-nx*10:.1f},{wrist[1]-ny*10:.1f}",
           LW_FINE, op=0.3)                                                          # forearm muscle line
    if upper:
        s.tube([shoulder, elbow, roll], SLEEVE, SHIRT, soft="white", cap="butt")
    else:
        s.tube([elbow, roll], SLEEVE - 4, SHIRT, soft="white")
    hw = (SLEEVE + 6) / 2
    band = (f"M{a[0]+nx*hw:.1f},{a[1]+ny*hw:.1f} Q{roll[0]+nx*(hw+4):.1f},{roll[1]+ny*(hw+4):.1f} {b[0]+nx*hw:.1f},{b[1]+ny*hw:.1f} "
            f"L{b[0]-nx*hw:.1f},{b[1]-ny*hw:.1f} Q{roll[0]-nx*(hw+4):.1f},{roll[1]-ny*(hw+4):.1f} {a[0]-nx*hw:.1f},{a[1]-ny*hw:.1f} Z")
    s.part(band, SHIRT, soft="white", shadow=f"M{roll[0]:.1f},{roll[1]-60:.1f} L{roll[0]+80:.1f},{roll[1]-60:.1f} L{roll[0]+80:.1f},{roll[1]+60:.1f} L{roll[0]:.1f},{roll[1]+60:.1f} Z", lw=LW_IN)
    s.line(f"M{roll[0]+nx*hw:.1f},{roll[1]+ny*hw:.1f} L{roll[0]-nx*hw:.1f},{roll[1]-ny*hw:.1f}", LW_FINE, color="#b6bdcb", op=0.9)
    s.line(f"M{elbow[0]-16},{elbow[1]-6} q12,10 30,2", LW_FINE, color="#b6bdcb", op=0.8)  # elbow crease


def hand_of(s, elbow, wrist, kind, extra, flip):
    dx, dy = wrist[0] - elbow[0], wrist[1] - elbow[1]
    cuff_and_hand(s, wrist, math.degrees(math.atan2(-dx, dy)) + extra, kind, flip, cuff=False, watch=flip)


def figure(pose="down", expr="neutral", blink=False, look=(0, 0)):
    s = Svg()
    s.add('<ellipse cx="300" cy="1392" rx="200" ry="22" fill="#000" opacity="0.28"/>')
    legs(s)
    arms = ARMS[pose]
    for shoulder, elbow, wrist, kind, extra, front in arms:      # sleeves behind the torso
        if front:
            s.tube([shoulder, elbow], SLEEVE, SHIRT, soft="white")
        else:
            sleeve(s, shoulder, elbow, wrist)
    torso(s)
    for shoulder, elbow, wrist, kind, extra, front in arms:      # hands in front of the jacket
        if not front:
            hand_of(s, elbow, wrist, kind, extra, shoulder[0] > 300)
    head(s, expr, blink, look)
    for shoulder, elbow, wrist, kind, extra, front in arms:      # forearms crossing the body
        if front:
            sleeve(s, shoulder, elbow, wrist, upper=False)
            hand_of(s, elbow, wrist, kind, extra, shoulder[0] > 300)
    return s.svg()



# =====================================================================================
#  TURNAROUND: side (facing left) and back views - same palette, light and line rules
# =====================================================================================
def side_view():
    s = Svg()
    s.add('<ellipse cx="300" cy="1392" rx="150" ry="20" fill="#000" opacity="0.28"/>')
    # far leg, near leg, shoes
    s.part("M286,830 L360,830 L352,1338 L296,1338 Z", shade(TROUSER, 0.8, 0.2))
    shoe = ("M252,1332 L342,1332 L344,1366 C344,1382 336,1390 322,1390 L230,1390 C214,1390 210,1374 222,1366 "
            "C236,1358 246,1348 252,1332 Z")
    s.part(shoe.replace("252,", "264,").replace("222,1428", "236,1428"), shade(SHOE, 0.8, 0.2))
    s.part("M256,830 L346,830 L338,1338 L274,1338 Z", TROUSER, shadow="M316,824 L360,824 L350,1348 L310,1348 Z")
    s.line("M300,880 C298,1000 296,1150 300,1328", LW_FINE, op=0.5)
    s.part(shoe, SHOE, shadow="M290,1374 L350,1374 L350,1398 L290,1398 Z", hl="M226,1366 C236,1360 250,1358 262,1360 L258,1366 Z")
    # neck + torso
    snk = "M298,214 C300,250 296,280 286,300 L362,300 C356,280 352,250 352,210 Z"
    s.part(snk, SKIN, line=False, shadow="M330,200 L380,200 L380,310 L330,310 Z")
    s.line("M298,226 C300,254 296,280 286,300", LW_OUT)
    s.line("M352,210 C352,250 356,280 362,300", LW_OUT)
    torso_d = ("M296,290 C266,292 238,312 230,346 C224,390 232,446 242,500 C250,560 252,620 252,680 "
               "C252,740 250,790 250,820 L366,820 C368,790 366,740 362,680 C358,600 366,500 372,420 "
               "C374,370 368,320 352,300 C336,292 316,288 296,290 Z")
    s.part(torso_d, SHIRT, soft="white", shadow="M330,290 C372,300 376,420 370,520 C366,640 372,760 372,860 L340,860 C348,700 352,500 336,300 Z",
           hl="M252,340 C248,380 250,430 254,480 L262,480 C258,430 258,384 262,344 Z")
    s.part("M262,292 L290,292 L270,346 L250,322 Z", SKIN, lw=LW_IN)               # open collar, chest
    s.part("M262,286 C256,298 252,316 256,334 L272,330 L268,300 Z", SHIRT, soft="white", lw=LW_IN)
    s.line("M252,360 C250,500 252,640 254,800", LW_FINE, color="#a3abbb", op=0.8)  # placket edge
    for d in ("M262,770 Q276,760 290,768", "M320,790 Q334,780 348,788", "M270,440 C290,452 310,452 326,444"):
        s.line(d, LW_FINE, color="#a3abbb", op=0.7)
    s.part("M248,806 L368,806 L370,840 L250,840 Z", BELT, lw=LW_IN)
    # near arm: rolled sleeve, bare forearm, watch
    sleeve(s, (312, 340), (304, 580), (296, 772))
    cuff_and_hand(s, (296, 772), 3, "relaxed", flip=True, watch=True)
    # head profile
    face = ("M318,46 C350,46 380,66 390,100 C398,130 392,170 372,198 C364,210 352,222 340,230 L296,246 "
            "C284,248 270,242 262,232 C258,224 258,214 258,208 C256,204 254,200 256,196 C252,192 250,190 246,188 "
            "C240,186 236,182 240,176 L254,148 C258,140 258,134 256,126 C254,116 256,104 262,94 C272,70 292,46 318,46 Z")
    s.part(face, SKIN, shadow="M330,40 L420,40 L420,260 L330,260 Z", hl="M262,100 C266,86 274,74 286,66 C276,80 270,92 268,106 Z")
    s.part("M332,128 C346,120 358,130 356,148 C354,166 344,176 334,172 Z", SKIN, shadow="M346,120 L370,120 L370,180 L346,180 Z", lw=LW_IN + 0.8)
    s.line("M340,138 C348,142 348,156 340,162", LW_FINE, op=0.6)
    st, arc = curls(326, 128, 80, 96, math.pi * 1.1, math.pi * 2.28, 11, 0.06, seed=5)
    hair = (f"M{st} {arc} C376,186 370,170 366,150 C362,132 350,114 330,104 C310,96 284,94 {st} Z")
    s.part(hair, HAIR, soft=True, shadow="M350,36 L420,36 L420,210 L350,210 Z", hl="M276,78 C290,54 312,44 334,42 C314,52 296,64 286,82 Z")
    for d in ("M266,84 C292,52 336,44 374,62", "M284,94 C314,72 352,72 384,98", "M314,100 C340,96 366,108 386,132"):
        s.line(d, 1.6, color=SHEEN, op=0.75)
    s.part("M248,118 C258,110 274,110 284,116 C276,120 264,122 252,126 Z", BROW, lw=LW_FINE + 0.5)
    eye = "M256,140 C262,134 272,134 278,140 C272,144 262,144 256,140 Z"
    s.add(f'<path d="{eye}" fill="#f4eee6"/><circle cx="262" cy="140" r="4.4" fill="{IRIS}"/><circle cx="261" cy="139" r="1.2" fill="#fff"/>')
    s.line("M254,139 C262,132 274,132 280,139", 2.8)
    s.line("M282,142 l7,-2 M282,146 l7,2", LW_FINE, op=0.4)
    beard = ("M330,150 C334,180 330,208 318,228 C308,244 292,252 276,252 C264,250 258,242 257,232 "
             "C258,226 262,220 268,216 C280,216 294,206 302,192 C312,178 320,162 322,146 Z")
    s.part(beard, hexc([rgb(SKIN)[i] * 0.3 + rgb(HAIR)[i] * 0.7 for i in range(3)]), soft=True, lw=LW_FINE,
           shadow="M300,236 C320,230 332,200 340,146 L360,146 L360,270 L300,270 Z",
           deep_d="M256,246 C268,262 290,262 300,256 L300,280 L256,280 Z")
    s.part("M252,194 C262,190 274,192 282,198 C276,203 264,205 254,202 Z",
           hexc([rgb(SKIN)[i] * 0.16 + rgb(HAIR)[i] * 0.84 for i in range(3)]), soft=True, lw=LW_FINE)
    s.line("M256,212 Q262,214 268,212", 2.2)
    return s.svg()


def back_view():
    s = Svg()
    s.add('<ellipse cx="300" cy="1392" rx="200" ry="22" fill="#000" opacity="0.28"/>')
    legs(s)
    for shoulder, elbow, wrist, *_ in ARMS["down"]:
        sleeve(s, shoulder, elbow, wrist)
    nk = "M262,200 C262,240 258,272 246,294 L354,294 C342,272 338,240 338,200 Z"
    s.part(nk, SKIN, line=False, shadow="M310,190 L360,190 L360,300 L310,300 Z")
    s.line("M262,200 C262,240 258,272 246,294", LW_OUT)
    s.line("M338,200 C338,240 342,272 354,294", LW_OUT)
    s.part(TORSO, SHIRT, soft="white", shadow="M346,282 C400,290 462,312 460,370 C450,404 430,420 420,440 L414,820 L374,820 C390,700 394,520 382,330 Z",
           hl="M160,330 C152,346 152,364 158,380 L168,378 C164,364 164,350 170,336 Z")
    s.part("M256,288 Q300,276 344,288 L340,308 Q300,298 260,308 Z", SHIRT, soft="white", lw=LW_IN)   # collar
    s.line("M178,330 C230,350 370,350 422,330", LW_FINE, color="#a3abbb", op=0.9)                   # back yoke seam
    for d in ("M300,360 L300,780", "M236,700 Q250,720 246,760", "M364,700 Q350,720 354,760"):
        s.line(d, LW_FINE, color="#a3abbb", op=0.7)
    s.part("M194,806 L406,806 L408,838 L192,838 Z", BELT, shadow="M300,800 L420,800 L420,840 L300,840 Z", lw=LW_IN)
    for shoulder, elbow, wrist, kind, extra, front in ARMS["down"]:
        hand_of(s, elbow, wrist, kind, extra, shoulder[0] < 300)
    for d in ("M228,132 C214,122 205,132 207,149 C209,165 219,176 232,172 Z",):
        s.part(d, SKIN, lw=LW_IN + 0.8)
        s.part(mirror(d), SKIN, shadow="M360,110 L410,110 L410,190 L360,190 Z", lw=LW_IN + 0.8)
    st, arc = curls(300, 132, 92, 104, math.pi * 0.84, math.pi * 2.16, 13, 0.06, seed=4)
    back = f"M{st} {arc} Q336,226 300,220 Q264,226 {st} Z"
    s.part(back, HAIR, soft=True, shadow="M320,24 C376,40 396,100 384,150 C376,200 352,236 316,258 L300,258 C340,220 352,150 340,90 Z",
           hl="M246,70 C262,48 284,38 302,38 C284,48 266,60 256,78 Z", rim="M368,70 C384,100 384,150 372,190")
    for d in ("M246,90 C262,130 272,170 276,206", "M276,60 C290,110 296,160 296,212", "M322,60 C312,110 306,160 306,212",
              "M354,90 C338,130 328,170 324,206"):
        s.line(d, 1.6, color=SHEEN, op=0.7)
    return s.svg()


def head_only(expr, blink=False, look=(0, 0)):
    s = Svg()
    s.add('<rect x="200" y="290" width="200" height="40" fill="none"/>')
    torso_bits = Svg()
    head(s, expr, blink, look)
    return s.svg().replace(f'viewBox="0 0 {W} {H}" width="{W}" height="{H}"', 'viewBox="176 4 248 296" width="248" height="296"')


POSES = {
    # renderer poses: <pose>, <pose>_talk, <pose>_blink
    "idle": dict(pose="down", expr="neutral"),
    "talk": dict(pose="down", expr="talk"),
    "blink": dict(pose="down", expr="neutral", blink=True),
    "warm": dict(pose="down", expr="warm"),
    "warm_talk": dict(pose="down", expr="talk"),
    "explain": dict(pose="explain", expr="warm"),
    "explain_talk": dict(pose="explain", expr="talk"),
    "explain_blink": dict(pose="explain", expr="warm", blink=True),
    "point": dict(pose="point", expr="neutral", look=(-3, -2)),
    "point_talk": dict(pose="point", expr="talk", look=(-3, -2)),
    "think": dict(pose="think", expr="think", look=(3, -3)),
    "think_talk": dict(pose="think", expr="talk2", look=(3, -3)),
    "welcome": dict(pose="welcome", expr="smile"),
    "welcome_talk": dict(pose="welcome", expr="talk"),
    "surprised": dict(pose="both_explain", expr="surprised"),
    "surprised_talk": dict(pose="both_explain", expr="surprised"),
    "serious": dict(pose="down", expr="serious"),
    "serious_talk": dict(pose="down", expr="talk2"),
}

EXPRESSIONS = ["neutral", "warm", "smile", "talk", "think", "surprised", "serious", "laugh"]

if __name__ == "__main__":
    for name, kw in POSES.items():
        with open(os.path.join(D, name + ".svg"), "w") as f:
            f.write(figure(**kw))
    sheet = os.path.join(D, "sheet")
    os.makedirs(sheet, exist_ok=True)
    open(os.path.join(sheet, "turn_side.svg"), "w").write(side_view())
    open(os.path.join(sheet, "turn_back.svg"), "w").write(back_view())
    for e in EXPRESSIONS:
        open(os.path.join(sheet, f"expr_{e}.svg"), "w").write(head_only(e))
    print("wrote", len(POSES), "poses + sheet views")
