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
W, H = 600, 1500

# ---------------- palette ----------------
LINE = "#2b1d16"
SKIN = "#c98d68"
HAIR = "#2e2420"
BEARD = "#4b3b33"
SHEEN = "#7a6a62"
BROW = "#2e2420"
IRIS = "#4a2f1f"
SHIRT = "#efe8da"
TIE = "#7c2533"
VEST = "#6e4b33"
JACKET = "#34425c"
TROUSER = "#3a3e48"
SHOE = "#4e2c1e"
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


def shade(c, k=0.68, cool=0.28):
    r = rgb(c)
    return hexc([r[i] * k * (1 - cool) + COOL[i] * cool for i in range(3)])


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
                         '<stop offset="1" stop-color="#0b1030" stop-opacity="0.30"/></linearGradient>')

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
            inner.append(f'<path d="{shadow}" fill="{shade(base, 0.8, 0.22) if soft else shade(base)}"/>')
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

    def tube(self, pts, width, base, shadow_side=1):
        """Limb: an outlined thick stroke along pts, with a cel shadow strip on one side."""
        d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        self.add(f'<path d="{d}" fill="none" stroke="{LINE}" stroke-width="{width + 2 * LW_OUT}" '
                 f'stroke-linecap="round" stroke-linejoin="round"/>')
        self.add(f'<path d="{d}" fill="none" stroke="{base}" stroke-width="{width}" stroke-linecap="round" '
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
        self.add(f'<path d="{sd}" fill="none" stroke="{shade(base)}" stroke-width="{width * 0.42}" '
                 f'stroke-linecap="round" stroke-linejoin="round"/>')
        hd = "M" + " L".join(f"{x - width * 0.22:.1f},{y:.1f}" for x, y in pts)
        self.add(f'<path d="{hd}" fill="none" stroke="{light(base, 0.18)}" stroke-width="{width * 0.12}" '
                 f'stroke-linecap="round" opacity="0.6"/>')

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


# =====================================================================================
#  HEAD (front)
# =====================================================================================
FACE = ("M300,50 C352,50 378,86 380,130 C382,172 372,206 352,230 C334,252 316,264 300,264 "
        "C284,264 266,252 248,230 C228,206 218,172 220,130 C222,86 248,50 300,50 Z")


def head(s, expr="neutral", blink=False, look=(0, 0)):
    # ears
    for d in ("M228,132 C214,122 205,132 207,149 C209,165 219,176 232,172 Z",):
        for dd in (d, mirror(d)):
            s.part(dd, SKIN, shadow="M190,150 L240,150 L240,190 L190,190 Z" if dd == d else
                   "M360,110 L410,110 L410,190 L360,190 Z", lw=LW_IN + 0.8)
    s.line("M212,140 C208,150 210,162 218,168", LW_FINE, op=0.7)
    s.line("M388,140 C392,150 390,162 382,168", LW_FINE, op=0.7)
    # face
    s.part(FACE, SKIN,
           shadow=("M300,40 C356,46 386,86 384,130 C384,174 372,210 352,232 C334,254 316,266 300,268 "
                   "C326,246 348,214 354,176 C360,132 350,82 300,40 Z"),
           hl="M246,96 C252,78 266,66 284,62 C270,74 262,90 258,108 Z",
           rim="M372,96 C382,136 378,186 356,226")
    # eye sockets + cheek warmth
    s.add('<ellipse cx="271" cy="146" rx="26" ry="15" fill="#8a5a46" opacity="0.18"/>')
    s.add('<ellipse cx="329" cy="146" rx="26" ry="15" fill="#5a4a66" opacity="0.22"/>')
    s.add('<ellipse cx="252" cy="190" rx="20" ry="11" fill="#d9706a" opacity="0.18"/>')
    s.add('<ellipse cx="348" cy="190" rx="20" ry="11" fill="#c0605e" opacity="0.15"/>')
    # forehead wrinkles (age / wisdom)

    # hair: textured side-swept quiff, short sides (young)
    hair = ("M225,128 C219,102 222,76 236,60 C240,46 252,36 266,31 C273,22 287,16 301,20 C315,12 333,14 343,23 "
            "C357,25 369,35 375,49 C385,66 386,94 377,128 C375,114 371,104 365,97 C355,90 343,88 333,91 "
            "C326,84 314,79 300,82 C288,80 274,84 263,92 C252,100 242,108 235,116 C231,120 228,124 225,128 Z")
    s.part(hair, HAIR, soft=True,
           shadow="M334,14 C372,26 394,80 380,130 L362,130 C370,92 360,52 334,30 Z",
           hl="M246,62 C262,38 288,26 316,24 C290,34 268,48 256,70 Z",
           rim="M370,46 C384,66 388,98 380,126")
    for d in ("M240,104 C250,74 276,50 312,40", "M262,92 C276,64 304,48 338,46", "M298,82 C314,62 340,54 364,64",
              "M330,90 C346,80 362,82 372,96", "M232,116 C232,92 242,70 260,54"):
        s.line(d, 1.6, color=SHEEN, op=0.75)
    s.line("M252,58 C264,44 282,36 300,34", 2.6, color="#a39189", op=0.5)
    # short side hair (fade) above the ears
    for d in ("M225,128 C224,134 224,140 226,146 L232,144 C230,138 230,132 231,124 Z",):
        s.part(d, HAIR, soft=True, lw=LW_FINE)
        s.part(mirror(d), HAIR, soft=True, lw=LW_FINE)

    # brows by expression: (inner_dy, outer_dy)
    bi, bo = {"neutral": (0, 0), "smile": (-3, 1), "talk": (-3, -1), "talk2": (-1, 0), "think": (6, 1),
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
        open_ = {"surprised": 10, "smile": 4.5, "warm": 5.5, "serious": 5.5, "think": 6}.get(expr, 7)
        eye = (f"M{cx-18},142 C{cx-10},{142-open_-1} {cx+10},{142-open_-1} {cx+18},142 "
               f"C{cx+10},{142+open_*0.75} {cx-10},{142+open_*0.75} {cx-18},142 Z")
        eid = s.uid()
        s.defs.append(f'<clipPath id="{eid}"><path d="{eye}"/></clipPath>')
        s.add(f'<path d="{eye}" fill="#f4eee6"/>')
        s.add(f'<g clip-path="url(#{eid})"><circle cx="{cx+lx}" cy="{141.5+ly}" r="6.4" fill="{IRIS}"/>'
              f'<circle cx="{cx+lx}" cy="{141.5+ly}" r="3" fill="#120a07"/>'
              f'<circle cx="{cx+lx-2}" cy="{139.5+ly}" r="1.6" fill="#fff"/>'
              f'<path d="M{cx-20},{130} L{cx+20},130 L{cx+20},{140-open_+3} L{cx-20},{140-open_+3} Z" fill="#000" opacity="0.18"/></g>')
        s.line(f"M{cx-19},142 C{cx-10},{141-open_-2} {cx+10},{141-open_-2} {cx+19},141", 3.0)  # upper lid
        if expr in ("smile", "warm"):
            s.line(f"M{cx-14},{148} C{cx-5},{143} {cx+5},{143} {cx+14},{148}", 1.8, op=0.8)   # cheek squint
        else:
            s.line(f"M{cx-12},{147+open_*0.4} C{cx-4},{149+open_*0.4} {cx+6},{149+open_*0.4} {cx+13},{146+open_*0.4}",
                   LW_FINE, op=0.55)


    # nose
    s.add('<path d="M306,150 C312,172 316,188 313,198 L303,200 C306,186 305,170 302,152 Z" '
          f'fill="{shade(SKIN)}" opacity="0.8"/>')
    s.line("M297,152 C296,170 292,186 289,196", LW_FINE, op=0.5)
    s.line("M284,199 C290,208 310,208 316,199", LW_IN)
    s.line("M290,202 q4,3 7,1 M310,202 q-4,3 -7,1", LW_FINE, op=0.7)
    s.add(f'<ellipse cx="296" cy="194" rx="5" ry="3" fill="{light(SKIN, 0.45)}" opacity="0.8"/>')

    # mouth (drawn before beard/moustache so they overlap it)
    m = {
        "neutral": ("line", "M287,240 Q300,243 313,240"),
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

    # beard + moustache
    beard = ("M224,136 C222,150 224,170 228,190 C236,220 250,246 270,260 C282,270 292,276 300,276 C308,276 318,270 330,260 "
             "C350,246 364,220 372,190 C376,170 378,150 376,136 L368,136 C370,176 360,212 342,228 L335,240 C325,254 311,258 300,258 "
             "C289,258 275,254 265,240 L260,228 C242,212 232,176 234,136 Z")
    s.part(beard, BEARD, soft=True,
           shadow="M312,252 C342,248 362,220 360,136 L400,136 L400,300 L300,300 Z",
           deep_d="M268,262 C282,280 318,280 332,262 L332,300 L268,300 Z",
           hl="M234,186 C240,212 252,232 264,244 C254,226 244,208 238,184 Z",
           rim="M366,204 C358,230 346,250 330,266")
    for d in ("M240,200 l4,12", "M250,226 l4,11", "M262,248 l3,10", "M280,266 l2,9", "M300,270 l0,10",
              "M320,266 l-2,9", "M338,248 l-3,10", "M350,226 l-4,11", "M360,200 l-4,12", "M290,276 l1,6", "M310,276 l-1,6"):
        s.line(d, LW_FINE, color=SHEEN, op=0.45)
    if expr in ("talk", "surprised", "laugh", "talk2"):
        must = ("M268,225 C276,215 288,212 300,216 C312,212 324,215 332,225 C335,230 334,234 331,235 "
                "C324,230 313,227 300,226 C287,227 276,230 269,235 C266,234 265,230 268,225 Z")
    else:
        must = ("M268,225 C276,215 288,212 300,216 C312,212 324,215 332,225 C335,231 334,236 331,237 "
                "C324,232 313,229 300,229 C287,229 276,232 269,237 C266,236 265,231 268,225 Z")
    s.part(must, BEARD, soft=True, shadow="M304,200 L346,200 L346,244 L304,244 Z",
           hl="M274,218 C280,213 290,211 296,214 C288,215 281,217 276,221 Z", lw=LW_IN)
    for d in ("M278,220 l-3,7", "M289,217 l-2,8", "M311,217 l2,8", "M322,220 l3,7"):
        s.line(d, LW_FINE, color=SHEEN, op=0.45)

    # spectacles (round gold)
    for side in (-1, 1):
        cx = 300 + side * 29
        s.add(f'<circle cx="{cx}" cy="142" r="25" fill="#dff1ff" opacity="0.07"/>')
        s.add(f'<circle cx="{cx}" cy="142" r="25" fill="none" stroke="{shade(GOLD,0.55,0.2)}" stroke-width="4.6"/>')
        s.add(f'<circle cx="{cx}" cy="142" r="25" fill="none" stroke="{GOLD}" stroke-width="2.4"/>')
        s.line(f"M{cx-16},{128} A21,21 0 0 1 {cx-4},{122}", 2.2, color="#ffffff", op=0.7)
    s.line("M296,139 Q300,133 304,139", 2.6, color=GOLD)
    s.line("M246,138 L226,132", 2.4, color=GOLD)
    s.line("M354,138 L374,132", 2.4, color=GOLD)


# =====================================================================================
#  BODY (front)
# =====================================================================================
TORSO = ("M300,288 C272,288 210,296 176,318 C152,332 146,352 148,380 C150,450 166,560 178,660 "
         "C174,720 166,780 162,836 C206,850 262,854 300,854 C338,854 394,850 438,836 C434,780 426,720 422,660 "
         "C434,560 450,450 452,380 C454,352 448,332 424,318 C390,296 328,288 300,288 Z")


def legs(s):
    leg = "M196,800 L298,800 L294,1402 L216,1402 C210,1160 202,980 196,800 Z"
    s.part(leg, TROUSER, shadow="M262,790 L310,790 L304,1410 L270,1410 Z", hl="M210,860 L216,860 L222,1370 L218,1370 Z")
    s.part(mirror(leg), TROUSER, shadow="M330,790 L420,790 L420,1410 L330,1410 Z")
    s.line("M246,870 L252,1392", LW_FINE, op=0.6)
    s.line("M354,870 L348,1392", LW_FINE, op=0.6)
    for x in (238, 362):  # knee folds
        s.line(f"M{x-14},1080 q14,8 28,0", LW_FINE, op=0.35)
    shoe = ("M208,1392 L294,1392 L296,1428 C296,1444 288,1452 272,1452 L188,1452 C172,1452 168,1436 180,1428 "
            "C192,1418 202,1408 208,1392 Z")
    s.part(shoe, SHOE, shadow="M240,1436 L300,1436 L300,1460 L240,1460 Z", hl="M190,1430 C198,1424 210,1422 222,1424 L218,1430 Z")
    s.part(mirror(shoe), SHOE, shadow="M300,1380 L440,1380 L440,1460 L300,1460 Z", hl=mirror("M190,1430 C198,1424 210,1422 222,1424 L218,1430 Z"))


def torso(s):
    # neck
    s.part("M268,228 L268,304 L332,304 L332,228 Z", SKIN,
           shadow="M300,220 L340,220 L340,310 L300,310 Z", deep_d="M260,224 L340,224 L340,262 Q300,284 260,262 Z")
    s.part(TORSO, JACKET,
           shadow="M336,288 C390,294 456,310 456,380 C452,500 430,600 424,680 L440,850 L360,856 C380,700 388,500 376,330 Z",
           hl="M168,340 C158,370 158,420 164,480 L176,480 C172,420 174,372 182,344 Z")
    # opening: vest + shirt + tie
    vest = "M258,292 L272,296 L300,426 L328,296 L342,292 L300,598 Z"
    s.part("M258,292 L342,292 L300,598 Z", SHIRT, line=False)
    s.part("M262,294 L338,294 L300,430 Z", SHIRT, shadow="M300,290 L340,290 L300,430 Z", lw=LW_IN)
    s.part("M289,300 L311,300 L307,322 L293,322 Z", TIE, shadow="M300,296 L314,296 L310,326 L300,326 Z", lw=LW_IN)
    s.part("M293,322 L307,322 L314,430 L300,446 L286,430 Z", TIE, shadow="M300,320 L318,320 L318,450 L300,450 Z", lw=LW_IN)
    s.part(vest, VEST, shadow="M300,300 L346,290 L300,600 Z", hl="M266,310 L276,312 L296,440 L290,460 Z", lw=LW_IN + 0.6)
    for y in (452, 490, 528, 566):
        s.add(f'<circle cx="300" cy="{y}" r="4.6" fill="{GOLD}" stroke="{LINE}" stroke-width="1.6"/>')
    s.line("M300,492 Q286,520 262,522", 2.4, color=GOLD)
    s.line("M300,492 Q286,520 262,522", 1.0, color="#fff4cc", op=0.6)
    # shirt collar points
    s.part("M262,292 L292,330 L280,336 L256,300 Z", SHIRT, lw=LW_IN)
    s.part(mirror("M262,292 L292,330 L280,336 L256,300 Z"), SHIRT, shadow="M300,280 L350,280 L350,340 L300,340 Z", lw=LW_IN)
    # lapels
    lap = "M258,292 L226,348 L246,358 L234,374 L300,598 Z"
    s.part(lap, JACKET, hl="M252,300 L232,346 L240,350 Z", lw=LW_IN + 1)
    s.part(mirror(lap), JACKET, shadow="M300,280 L380,280 L380,600 L300,600 Z", lw=LW_IN + 1)
    s.line("M258,292 Q300,282 342,292", LW_IN)
    # jacket front below button + gap
    s.part("M300,600 C296,700 286,790 270,852 L330,852 C314,790 304,700 300,600 Z", TROUSER,
           shadow="M300,600 L340,600 L340,850 L300,850 Z", lw=LW_IN)
    s.add(f'<circle cx="300" cy="604" r="6.5" fill="{shade(JACKET,0.55,0.2)}" stroke="{LINE}" stroke-width="1.8"/>')
    # pockets + pocket square + seams
    s.line("M190,712 L252,716", LW_IN)
    s.line("M410,712 L348,716", LW_IN)
    s.part("M362,430 L370,410 L378,424 L388,408 L398,428 Z", SQUARE, shadow="M384,400 L404,400 L404,432 L384,432 Z", lw=LW_IN)
    s.line("M354,431 L406,427", LW_IN)
    s.line("M212,330 C220,420 222,520 216,600", LW_FINE, op=0.4)
    s.line("M388,330 C380,420 378,520 384,600", LW_FINE, op=0.4)


def cuff_and_hand(s, wrist, angle, kind, flip=False):
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
    # shirt cuff
    g.insert(0, f'<rect x="-28" y="-14" width="56" height="22" rx="5" fill="{SHIRT}" stroke="{LINE}" stroke-width="{LW_IN}"/>')
    sx = -1.22 if flip else 1.22
    s.add(f'<g {t} ><g transform="scale({sx},1.22)">{"".join(g)}</g></g>')


# arm configurations: (shoulder, elbow, wrist, hand_kind, extra_angle, forearm_in_front)
# Upper arms sit BEHIND the torso so they emerge from under the jacket shoulder; hands are always in front.
L_SH, R_SH = (178, 362), (422, 362)
ARMS = {
    "down": [(L_SH, (144, 590), (146, 800), "relaxed", 0, False), (R_SH, (456, 590), (454, 800), "relaxed", 0, False)],
    "explain": [(L_SH, (140, 600), (92, 470), "open", 0, False), (R_SH, (456, 590), (454, 800), "relaxed", 0, False)],
    "point": [(L_SH, (116, 446), (58, 322), "point", 0, False), (R_SH, (456, 590), (454, 800), "relaxed", 0, False)],
    "think": [(L_SH, (196, 616), (266, 352), "chin", 0, True), (R_SH, (456, 590), (454, 800), "relaxed", 0, False)],
    "welcome": [(L_SH, (138, 586), (88, 712), "open", 0, False), (R_SH, (462, 586), (512, 712), "open", 0, False)],
    "both_explain": [(L_SH, (140, 600), (92, 470), "open", 0, False), (R_SH, (460, 600), (508, 470), "open", 0, False)],
}
SLEEVE = 68


def hand_of(s, elbow, wrist, kind, extra, flip):
    dx, dy = wrist[0] - elbow[0], wrist[1] - elbow[1]
    cuff_and_hand(s, wrist, math.degrees(math.atan2(-dx, dy)) + extra, kind, flip)


def figure(pose="down", expr="neutral", blink=False, look=(0, 0)):
    s = Svg()
    s.add('<ellipse cx="300" cy="1454" rx="200" ry="22" fill="#000" opacity="0.28"/>')
    legs(s)
    arms = ARMS[pose]
    for shoulder, elbow, wrist, kind, extra, front in arms:      # sleeves behind the torso
        s.tube([shoulder, elbow] if front else [shoulder, elbow, wrist], SLEEVE, JACKET)
    torso(s)
    for shoulder, elbow, wrist, kind, extra, front in arms:      # hands in front of the jacket
        if not front:
            hand_of(s, elbow, wrist, kind, extra, shoulder[0] > 300)
    head(s, expr, blink, look)
    for shoulder, elbow, wrist, kind, extra, front in arms:      # forearms crossing the body
        if front:
            s.tube([elbow, wrist], SLEEVE - 6, JACKET)
            hand_of(s, elbow, wrist, kind, extra, shoulder[0] > 300)
    return s.svg()



# =====================================================================================
#  TURNAROUND: side (facing left) and back views - same palette, light and line rules
# =====================================================================================
def side_view():
    s = Svg()
    s.add('<ellipse cx="300" cy="1454" rx="150" ry="20" fill="#000" opacity="0.28"/>')
    # far leg, near leg, shoes
    s.part("M286,846 L360,846 L352,1400 L296,1400 Z", shade(TROUSER, 0.8, 0.2))
    shoe = ("M252,1394 L342,1394 L344,1428 C344,1444 336,1452 322,1452 L230,1452 C214,1452 210,1436 222,1428 "
            "C236,1420 246,1410 252,1394 Z")
    s.part(shoe.replace("252,", "264,").replace("222,1428", "236,1428"), shade(SHOE, 0.8, 0.2))
    s.part("M262,846 L346,846 L338,1400 L274,1400 Z", TROUSER, shadow="M316,840 L360,840 L350,1410 L310,1410 Z")
    s.line("M300,880 C298,1000 296,1200 300,1390", LW_FINE, op=0.5)
    s.part(shoe, SHOE, shadow="M290,1436 L350,1436 L350,1460 L290,1460 Z", hl="M226,1428 C236,1422 250,1420 262,1422 L258,1428 Z")
    # neck + torso
    s.part("M300,226 L350,222 L356,304 L302,306 Z", SKIN, shadow="M330,210 L370,210 L370,310 L330,310 Z")
    torso_d = ("M296,290 C270,292 250,310 244,340 C240,380 244,440 248,500 C250,560 254,620 252,680 "
               "C250,740 248,800 250,856 L366,856 C368,800 366,740 362,680 C358,600 364,500 368,420 "
               "C370,370 366,320 350,300 C336,292 316,288 296,290 Z")
    s.part(torso_d, JACKET, shadow="M330,290 C372,300 376,420 370,520 C366,640 372,760 372,860 L340,860 C348,700 352,500 336,300 Z",
           hl="M252,340 C248,380 250,430 254,480 L262,480 C258,430 258,384 262,344 Z")
    s.part("M266,292 L292,296 L256,330 L248,318 Z", SHIRT, lw=LW_IN)
    s.part("M250,320 L262,322 L256,420 L246,410 Z", TIE, lw=LW_IN)
    s.line("M272,300 C262,380 254,470 252,560", LW_IN)          # lapel roll
    s.line("M262,712 L300,714", LW_IN)                          # pocket flap
    s.line("M360,620 C362,720 362,800 360,850", LW_FINE, op=0.5)  # back vent
    # near arm in front of torso
    s.tube([(312, 340), (300, 590), (290, 796)], SLEEVE, JACKET)
    cuff_and_hand(s, (290, 796), 3, "relaxed", flip=True)
    # head profile
    face = ("M318,46 C350,46 380,66 390,100 C398,130 392,170 372,198 C364,210 352,222 340,230 L296,246 "
            "C284,248 270,242 262,232 C258,224 258,214 258,208 C256,204 254,200 256,196 C252,192 250,190 246,188 "
            "C240,186 236,182 240,176 L254,148 C258,140 258,134 256,126 C254,116 256,104 262,94 C272,70 292,46 318,46 Z")
    s.part(face, SKIN, shadow="M330,40 L420,40 L420,260 L330,260 Z", hl="M262,100 C266,86 274,74 286,66 C276,80 270,92 268,106 Z")
    s.part("M332,128 C346,120 358,130 356,148 C354,166 344,176 334,172 Z", SKIN, shadow="M346,120 L370,120 L370,180 L346,180 Z", lw=LW_IN + 0.8)
    s.line("M340,138 C348,142 348,156 340,162", LW_FINE, op=0.6)
    hair = ("M258,96 C262,58 292,26 334,26 C376,28 404,66 402,116 C400,150 392,178 378,198 L362,194 "
            "C370,172 372,150 368,128 C352,112 332,104 312,100 C292,94 274,94 258,96 Z")
    s.part(hair, HAIR, soft=True, shadow="M350,36 L420,36 L420,210 L350,210 Z", hl="M276,78 C290,54 312,44 334,42 C314,52 296,64 286,82 Z")
    for d in ("M266,84 C292,52 336,44 374,62", "M284,94 C314,72 352,72 384,98", "M314,100 C340,96 366,108 386,132"):
        s.line(d, 1.6, color=SHEEN, op=0.75)
    s.part("M248,118 C258,110 274,110 284,116 C276,120 264,122 252,126 Z", BROW, lw=LW_FINE + 0.5)
    eye = "M256,140 C262,134 272,134 278,140 C272,144 262,144 256,140 Z"
    s.add(f'<path d="{eye}" fill="#f4eee6"/><circle cx="262" cy="140" r="4.4" fill="{IRIS}"/><circle cx="261" cy="139" r="1.2" fill="#fff"/>')
    s.line("M254,139 C262,132 274,132 280,139", 2.8)
    s.line("M282,142 l7,-2 M282,146 l7,2", LW_FINE, op=0.4)
    beard = ("M332,146 C336,176 332,204 318,226 C308,240 292,250 274,250 C262,248 256,240 256,230 "
             "C258,226 262,220 268,216 C280,216 294,206 302,192 C312,178 320,162 322,146 Z")
    s.part(beard, BEARD, soft=True, shadow="M300,236 C320,230 332,200 340,146 L360,146 L360,270 L300,270 Z",
           deep_d="M256,246 C268,262 290,262 300,256 L300,280 L256,280 Z")
    s.part("M252,194 C262,190 274,192 282,198 C276,203 264,205 254,202 Z", BEARD, soft=True, lw=LW_IN)
    s.line("M256,212 Q262,214 268,212", 2.2)
    s.add(f'<ellipse cx="256" cy="140" rx="7" ry="23" fill="#dff1ff" opacity="0.1" stroke="{GOLD}" stroke-width="2.6"/>')
    s.line("M262,134 L336,132", 2.4, color=GOLD)
    return s.svg()


def back_view():
    s = Svg()
    s.add('<ellipse cx="300" cy="1454" rx="200" ry="22" fill="#000" opacity="0.28"/>')
    legs(s)
    for shoulder, elbow, wrist, *_ in ARMS["down"]:
        s.tube([shoulder, elbow, wrist], SLEEVE, JACKET)
    s.part("M268,228 L268,304 L332,304 L332,228 Z", SKIN, shadow="M300,220 L340,220 L340,310 L300,310 Z")
    s.part(TORSO, JACKET, shadow="M336,288 C390,294 456,310 456,380 C452,500 430,600 424,680 L440,850 L360,856 C380,700 388,500 376,330 Z",
           hl="M168,340 C158,370 158,420 164,480 L176,480 C172,420 174,372 182,344 Z")
    s.part("M258,290 Q300,278 342,290 L338,312 Q300,302 262,312 Z", JACKET, lw=LW_IN)   # collar
    s.line("M300,312 C300,500 300,640 300,700", LW_IN)                                   # centre seam
    s.line("M300,700 L300,852", LW_IN)                                                   # vent
    s.line("M292,700 L300,700", LW_FINE)
    s.line("M206,340 C222,420 226,520 222,640", LW_FINE, op=0.4)
    s.line("M394,340 C378,420 374,520 378,640", LW_FINE, op=0.4)
    for shoulder, elbow, wrist, kind, extra, front in ARMS["down"]:
        hand_of(s, elbow, wrist, kind, extra, shoulder[0] < 300)
    for d in ("M228,132 C214,122 205,132 207,149 C209,165 219,176 232,172 Z",):
        s.part(d, SKIN, lw=LW_IN + 0.8)
        s.part(mirror(d), SKIN, shadow="M360,110 L410,110 L410,190 L360,190 Z", lw=LW_IN + 0.8)
    back = ("M300,30 C356,30 388,80 382,140 C378,186 362,222 338,240 C324,250 312,254 300,254 "
            "C288,254 276,250 262,240 C238,222 222,186 218,140 C212,80 244,30 300,30 Z")
    s.part(back, HAIR, soft=True, shadow="M320,24 C376,40 396,100 384,150 C376,200 352,236 316,258 L300,258 C340,220 352,150 340,90 Z",
           hl="M246,70 C262,48 284,38 302,38 C284,48 266,60 256,78 Z", rim="M368,70 C384,100 384,150 372,190")
    for d in ("M250,90 C270,140 280,200 282,240", "M276,60 C292,120 298,190 296,250", "M320,60 C312,120 306,190 306,250",
              "M352,90 C334,140 324,200 320,240"):
        s.line(d, 1.6, color=SHEEN, op=0.7)
    s.line("M226,134 L246,140", 2.4, color=GOLD)
    s.line("M374,134 L354,140", 2.4, color=GOLD)
    return s.svg()


def head_only(expr, blink=False, look=(0, 0)):
    s = Svg()
    s.add('<rect x="200" y="290" width="200" height="40" fill="none"/>')
    torso_bits = Svg()
    head(s, expr, blink, look)
    return s.svg().replace(f'viewBox="0 0 {W} {H}" width="{W}" height="{H}"', 'viewBox="180 10 240 290" width="240" height="290"')


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
