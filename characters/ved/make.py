"""Professor Ved - the channel's explainer.  Style v8: clean flat-vector illustration.

Look: 25 years old, handsome, athletic. Black hair in a swept-up quiff with a skin fade, crisp full beard
and a distinct moustache (they meet at the mouth corners; clean skin right below the lower lip), slightly
narrow jaw. White shirt, top button open, sleeves folded below the elbow; black trousers, belt, shoes;
gold watch on his left wrist.

Rendering rules (same light as every set: warm key from the viewer's left):
  * NO outlines. Forms are separated by tone only.
  * Two-tone flat shading per surface: base + one hard-edged shadow plane (viewer's right),
    plus a small warm highlight plane on the lit side. Shadows are cool (pushed toward blue).
  * Features (eyes, brows, nostrils, lips) are drawn as dark shapes, not lines.
Every pose is generated from the SAME parts below, so he never drifts.   Run: python make.py
"""
import math
import os
import re

D = os.path.dirname(os.path.abspath(__file__))
W, H = 600, 1500

# ---------------- palette ----------------
SKIN = "#e7b089"
HAIR = "#16161b"
BEARD = "#1d1919"
SHEEN = "#474b5a"
BROW = "#141317"
IRIS = "#4a2e1c"
LIPS = "#c27f6c"
SHIRT = "#f8f8f6"
TROUSER = "#24272e"
BELT = "#141416"
SILVER = "#c9ccd1"
SHOE = "#18181b"
GOLD = "#d4a64a"
STRAP = "#3a2a20"
LINE = "#2b1d16"          # only used for tiny details now (kept for sheet palette)
RIM = "#bfe6ff"
KEY = "#fff1d6"
COOL = (46, 58, 110)


def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def hexc(c):
    return "#%02x%02x%02x" % tuple(max(0, min(255, int(round(v)))) for v in c)


def mix(a, b, t):
    A, B = rgb(a), rgb(b)
    return hexc([A[i] * (1 - t) + B[i] * t for i in range(3)])


def shade(c, k=0.8, cool=0.2):
    r = rgb(c)
    return hexc([r[i] * k * (1 - cool) + COOL[i] * cool for i in range(3)])


def deep(c):
    return shade(c, 0.62, 0.3)


def light(c, k=0.3):
    r, w = rgb(c), rgb(KEY)
    return hexc([r[i] * (1 - k) + w[i] * k for i in range(3)])


SKIN_SH, SKIN_DEEP, SKIN_HL = shade(SKIN), deep(SKIN), light(SKIN, 0.35)
SHIRT_SH, SHIRT_DEEP = "#d6dbe5", "#bcc3d1"
TROUSER_SH, TROUSER_HL = "#16181d", "#3a3f4b"


class Svg:
    def __init__(self):
        self.defs, self.body, self.n = [], [], 0
        self.defs.append(f'<linearGradient id="fade" x1="0" y1="0" x2="0" y2="1">'
                         f'<stop offset="0" stop-color="{HAIR}" stop-opacity="1"/>'
                         f'<stop offset="0.55" stop-color="{HAIR}" stop-opacity="0.55"/>'
                         f'<stop offset="1" stop-color="{HAIR}" stop-opacity="0"/></linearGradient>')

    def uid(self, p="c"):
        self.n += 1
        return f"{p}{self.n}"

    def add(self, x):
        self.body.append(x)

    def part(self, d, base, shadow=None, hl=None, deep_d=None, shadow_col=None, hl_col=None, deep_col=None,
             line=False, **_):
        """Flat shape with hard-edged shadow / highlight planes clipped inside it. No outline."""
        cid = self.uid()
        self.defs.append(f'<clipPath id="{cid}"><path d="{d}"/></clipPath>')
        g = [f'<path d="{d}" fill="{base}"/>']
        inner = []
        if shadow:
            inner.append(f'<path d="{shadow}" fill="{shadow_col or shade(base)}"/>')
        if deep_d:
            inner.append(f'<path d="{deep_d}" fill="{deep_col or deep(base)}"/>')
        if hl:
            inner.append(f'<path d="{hl}" fill="{hl_col or light(base, 0.3)}"/>')
        if inner:
            g.append(f'<g clip-path="url(#{cid})">{"".join(inner)}</g>')
        self.add("".join(g))

    def line(self, d, w=2.0, color=None, op=1.0, cap="round"):
        self.add(f'<path d="{d}" fill="none" stroke="{color or SKIN_DEEP}" stroke-width="{w}" '
                 f'stroke-linecap="{cap}" stroke-linejoin="round" opacity="{op}"/>')

    def two_tone(self, x1, y1, x2, y2, base, sh, split=0.58, hl=None):
        """Across-the-limb gradient with a HARD edge: flat base, then flat shadow (flat-vector look)."""
        gid = self.uid("g")
        stops = []
        if hl:
            stops += [(0, hl), (0.14, hl), (0.14, base)]
        else:
            stops += [(0, base)]
        stops += [(split, base), (split, sh), (1, sh)]
        self.defs.append(f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{x1:.1f}" y1="{y1:.1f}" '
                         f'x2="{x2:.1f}" y2="{y2:.1f}">' +
                         "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops) + '</linearGradient>')
        return gid

    def limb(self, pts, widths, base, sh, hl=None, split=0.58):
        """Tapered limb, no outline, two-tone across its width (light from the viewer's left)."""
        for i, (a, b, wa, wb) in enumerate(zip(pts, pts[1:], widths, widths[1:])):
            dx, dy = b[0] - a[0], b[1] - a[1]
            L = math.hypot(dx, dy) or 1
            nx, ny = -dy / L, dx / L
            if nx < 0:
                nx, ny = -nx, -ny
            d = (f"M{a[0]-nx*wa/2:.1f},{a[1]-ny*wa/2:.1f} L{b[0]-nx*wb/2:.1f},{b[1]-ny*wb/2:.1f} "
                 f"L{b[0]+nx*wb/2:.1f},{b[1]+ny*wb/2:.1f} L{a[0]+nx*wa/2:.1f},{a[1]+ny*wa/2:.1f} Z")
            m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
            w = (wa + wb) / 2
            gid = self.two_tone(m[0] - nx * w / 2, m[1] - ny * w / 2, m[0] + nx * w / 2, m[1] + ny * w / 2,
                                base, sh, split, hl)
            if i > 0:
                self.add(f'<circle cx="{a[0]:.1f}" cy="{a[1]:.1f}" r="{wa/2:.1f}" fill="url(#{gid})"/>')
            self.add(f'<path d="{d}" fill="url(#{gid})"/>')

    def svg(self):
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
                f'<defs>{"".join(self.defs)}</defs>{"".join(self.body)}</svg>')


def mirror(d):
    """Mirror an absolute SVG path (M/L/C/Q/Z) around x=300."""
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
FACE = ("M300,64 C341,64 369,88 370,126 C372,152 368,176 360,196 L351,214 C340,232 322,244 300,246 "
        "C278,244 260,232 249,214 L240,196 C232,176 228,152 230,126 C231,88 259,64 300,64 Z")
BROWS = {"neutral": (0, 0), "warm": (-2, 1), "smile": (-2, 1), "talk": (-2, 0), "talk2": (-1, 0),
         "think": (5, 0), "surprised": (-10, -7), "serious": (6, -1), "laugh": (-3, 2),
         "deadpan": (4, 4), "side_eye": (3, 1), "smirk": (-1, 1)}


def head(s, expr="neutral", blink=False, look=(0, 0), mouth=None):
    # ears
    ear = "M233,134 C222,128 215,136 216,152 C217,166 224,176 236,174 Z"
    s.part(ear, SKIN, shadow="M200,160 L240,160 L240,190 L200,190 Z", shadow_col=SKIN_SH)
    s.part(mirror(ear), SKIN, shadow="M360,120 L400,120 L400,190 L360,190 Z", shadow_col=SKIN_SH)
    s.add(f'<path d="M226,142 C222,150 223,160 228,166 L230,164 C227,158 226,150 229,144 Z" fill="{SKIN_DEEP}" opacity="0.6"/>')
    s.add(f'<path d="{mirror("M226,142 C222,150 223,160 228,166 L230,164 C227,158 226,150 229,144 Z")}" fill="{SKIN_DEEP}" opacity="0.7"/>')
    # neck (shadowed by the jaw)
    s.part("M266,220 L266,304 L334,304 L334,220 Z", SKIN,
           shadow="M308,210 L340,210 L340,310 L308,310 Z", shadow_col=SKIN_SH,
           deep_d="M260,210 L340,210 L340,262 Q300,282 260,262 Z", deep_col=SKIN_SH)
    # face: base, right-side shadow plane, cheekbone light, nose
    s.part(FACE, SKIN,
           shadow=("M318,60 C352,70 376,96 376,130 C378,170 368,204 350,228 C336,244 318,252 300,254 "
                   "C322,236 340,206 346,172 C352,134 342,94 318,60 Z"), shadow_col=SKIN_SH,
           hl="M244,104 C250,86 264,74 282,70 C268,82 260,96 256,114 Z", hl_col=SKIN_HL)
    s.add(f'<path d="M248,160 C256,156 266,156 274,159 C266,161 258,165 252,170 Z" fill="{SKIN_HL}" opacity="0.25"/>')
    s.add(f'<path d="M244,178 C252,188 262,194 272,196 C262,200 250,196 244,188 Z" fill="{SKIN_SH}" opacity="0.55"/>')
    s.add('<ellipse cx="256" cy="176" rx="14" ry="7" fill="#e07e70" opacity="0.14"/>')

    # eyebrows: thick, straight, confident
    bi, bo = BROWS.get(expr, (0, 0))
    lb = (f"M246,{122+bo} C254,{113+bo} 272,{109+bi} 292,{114+bi} L291,{121+bi} C276,{118+bi} 262,{120+bo} "
          f"249,{127+bo} Z")
    s.add(f'<path d="{lb}" fill="{BROW}"/>')
    rb = mirror(lb)
    if expr == "think":
        s.add(f'<g transform="translate(0,-8) rotate(-5 330 115)"><path d="{rb}" fill="{BROW}"/></g>')
    elif expr == "smirk":                                   # one brow up: "oh really?"
        s.add(f'<g transform="translate(0,-7) rotate(-4 330 115)"><path d="{rb}" fill="{BROW}"/></g>')
    else:
        s.add(f'<path d="{rb}" fill="{BROW}"/>')
    # brow ridge / eye socket shading
    s.add(f'<path d="M250,128 C264,124 282,125 292,132 C280,130 264,130 252,134 Z" fill="{SKIN_SH}" opacity="0.5"/>')
    s.add(f'<path d="{mirror("M250,128 C264,124 282,125 292,132 C280,130 264,130 252,134 Z")}" fill="{SKIN_SH}" opacity="0.7"/>')

    # eyes: almond, slightly narrowed (confident), dark upper lid
    lx, ly = look
    open_ = {"surprised": 9, "smile": 4.5, "warm": 5.5, "laugh": 0, "think": 6, "serious": 5.5,
             "deadpan": 3.2, "side_eye": 4.2, "smirk": 5}.get(expr, 6.5)
    for side in (-1, 1):
        cx = 300 + side * 31
        if blink or expr == "laugh" or open_ == 0:
            s.line(f"M{cx-14},142 C{cx-6},147 {cx+6},147 {cx+14},142", 3.0, color=BROW)
            continue
        eye = (f"M{cx-15},142 C{cx-8},{142-open_} {cx+8},{142-open_} {cx+15},141 "
               f"C{cx+8},{142+open_*0.7} {cx-8},{142+open_*0.7} {cx-15},142 Z")
        eid = s.uid()
        s.defs.append(f'<clipPath id="{eid}"><path d="{eye}"/></clipPath>')
        s.add(f'<path d="{eye}" fill="#f6f1ea"/>')
        s.add(f'<g clip-path="url(#{eid})"><circle cx="{cx+lx}" cy="{141.5+ly}" r="6.2" fill="{IRIS}"/>'
              f'<circle cx="{cx+lx}" cy="{141.5+ly}" r="3" fill="#0e0907"/>'
              f'<circle cx="{cx+lx-2}" cy="{139.5+ly}" r="1.7" fill="#fff"/>'
              f'<rect x="{cx-20}" y="120" width="40" height="{24-open_}" fill="#000" opacity="0.14"/></g>')
        lid = (f"M{cx-16},142 C{cx-8},{141-open_-1.5} {cx+8},{141-open_-1.5} {cx+16},140 "
               f"L{cx+16},{138.5} C{cx+8},{138-open_-3} {cx-8},{138-open_-3} {cx-16},{140.5} Z")
        s.add(f'<path d="{lid}" fill="{BROW}"/>')                                    # upper lid + lashes
        s.add(f'<path d="M{cx-13},{136-open_} C{cx-5},{131-open_} {cx+6},{131-open_} {cx+14},{135-open_}" '
              f'fill="none" stroke="{SKIN_SH}" stroke-width="2" opacity="0.8"/>')      # crease
        if expr in ("smile", "warm"):
            s.add(f'<path d="M{cx-12},{146} C{cx-4},{141} {cx+5},{141} {cx+12},{146}" fill="none" stroke="{SKIN_SH}" stroke-width="2"/>')

    # nose: shadow plane on the right, nostrils, tip light
    s.add(f'<path d="M303,146 C307,164 313,180 314,190 C310,197 304,198 300,196 L304,190 C304,176 303,160 300,148 Z" fill="{SKIN_SH}"/>')
    s.add(f'<path d="M286,192 C284,196 286,200 292,200 C290,197 290,195 291,192 Z" fill="{SKIN_DEEP}"/>')
    s.add(f'<path d="M314,192 C316,196 314,200 308,200 C310,197 310,195 309,192 Z" fill="{SKIN_DEEP}"/>')
    s.add(f'<path d="M290,200 Q300,204 310,200 Q300,202 290,200 Z" fill="{SKIN_DEEP}" opacity="0.7"/>')
    s.add(f'<ellipse cx="296" cy="190" rx="5" ry="3" fill="{SKIN_HL}"/>')
    s.add(f'<path d="M294,150 C293,164 292,176 293,186" fill="none" stroke="{SKIN_HL}" stroke-width="3" opacity="0.8"/>')

    # beard: crisp, full, groomed; follows the jaw; open under the lower lip
    beard = ("M226,138 C225,170 230,198 242,222 C256,246 280,264 300,267 C320,264 344,246 358,222 "
             "C370,198 375,170 374,138 L361,150 C359,170 352,188 341,201 C332,211 327,220 325,232 "
             "C321,241 312,246 300,246 C288,246 279,241 275,232 C273,220 268,211 259,201 C248,188 241,170 239,150 Z")
    s.part(beard, BEARD,
           shadow="M318,256 C342,248 364,218 372,140 L390,140 L390,290 L300,290 Z", shadow_col="#0f0d0e",
           hl="M234,168 C236,192 244,212 256,228 C246,208 240,190 240,170 Z", hl_col="#2c2727")
    for d in ("M252,214 l3,9", "M262,228 l4,8", "M276,242 l3,8", "M290,250 l1,7", "M244,190 l2,9",
              "M310,250 l-1,7", "M324,242 l-3,8", "M338,228 l-4,8", "M348,214 l-3,9", "M356,190 l-2,9"):
        s.line(d, 1.4, color=SHEEN, op=0.7)
    # moustache: distinct, full, ends turn down to the mouth corners
    must = ("M272,214 C281,205 292,203 300,207 C308,203 319,205 328,214 C332,219 334,226 332,232 "
            "C328,226 322,221 314,219 C308,218 303,219 300,220 C297,219 292,218 286,219 C278,221 272,226 268,232 "
            "C266,226 268,219 272,214 Z")
    s.part(must, BEARD, shadow="M302,200 L340,200 L340,236 L302,236 Z", shadow_col="#0f0d0e",
           hl="M278,212 C285,207 293,206 298,208 C291,209 284,211 280,215 Z", hl_col="#3a3333")

    # mouth (between moustache and the clean gap under the lip)
    shapes = {
        "m1": "M290,223 Q300,222 310,223 Q307,229 300,230 Q293,229 290,223 Z",
        "m3": "M284,221 Q300,219 316,221 Q313,243 300,244 Q287,243 284,221 Z",
        "oo": "M292,222 Q300,219 308,222 Q311,233 300,237 Q289,233 292,222 Z",
        "ee": "M281,222 Q300,220 319,222 Q315,232 300,233 Q285,232 281,222 Z",
        "talk": "M287,222 Q300,220 313,222 Q310,236 300,237 Q290,236 287,222 Z",
        "talk2": "M289,222 Q300,221 311,222 Q308,231 300,232 Q292,231 289,222 Z",
        "surprised": "M292,221 Q300,218 308,221 Q310,238 300,240 Q290,238 292,221 Z",
        "laugh": "M284,221 Q300,219 316,221 Q312,240 300,241 Q288,240 284,221 Z",
    }
    mk = mouth or expr
    if mk in shapes:
        expr_m = mk
        m = shapes[mk]
        mid = s.uid()
        s.defs.append(f'<clipPath id="{mid}"><path d="{m}"/></clipPath>')
        s.add(f'<path d="{m}" fill="#3a1612"/>')
        teeth_h = {"ee": 8, "m1": 3, "oo": 3}.get(expr_m, 6)
        s.add(f'<g clip-path="url(#{mid})"><rect x="278" y="218" width="44" height="{teeth_h}" fill="#f1ece4"/>'
              + ('' if expr_m in ("m1", "ee") else f'<ellipse cx="300" cy="{240 if expr_m != "m3" else 245}" rx="10" ry="6" fill="#b4504e"/>')
              + '</g>')
        bottom = {"m1": 230, "ee": 233, "oo": 237, "talk": 237, "talk2": 232, "m3": 244, "surprised": 240, "laugh": 241}.get(expr_m, 237)
        half = {"oo": 7, "m1": 9, "ee": 12, "m3": 11}.get(expr_m, 10)
        s.add(f'<path d="M{300-half},{bottom+1} Q300,{bottom+7} {300+half},{bottom+1} Q300,{bottom+4} {300-half},{bottom+1} Z" fill="{LIPS}"/>')
    else:
        if expr == "smirk":                                 # one corner pulled up
            s.add('<path d="M286,227 Q301,229 317,216" fill="none" stroke="#5a2c22" stroke-width="2.6" stroke-linecap="round"/>')
            s.add(f'<path d="M290,230 Q303,237 313,224 Q303,233 290,230 Z" fill="{LIPS}"/>')
        else:
            curve = {"smile": 7, "warm": 5, "serious": 1, "think": 2, "deadpan": 0, "side_eye": -1}.get(expr, 3)
            s.add(f'<path d="M286,224 Q300,{224+curve} 314,224" fill="none" stroke="#5a2c22" stroke-width="2.6" stroke-linecap="round"/>')
            s.add(f'<path d="M289,227 Q300,{236+curve*0.4:.1f} 311,227 Q300,{231+curve*0.3:.1f} 289,227 Z" fill="{LIPS}"/>')
    s.add(f'<path d="M292,241 Q300,244 308,241" fill="none" stroke="{SKIN_SH}" stroke-width="2" opacity="0.8"/>')  # chin dimple

    # hair: swept-up quiff, black, with a skin fade on the sides
    for d in ("M231,156 C226,130 228,106 238,90 L252,98 C244,112 240,132 240,158 Z",):
        s.add(f'<path d="{d}" fill="url(#fade)"/>')
        s.add(f'<path d="{mirror(d)}" fill="url(#fade)"/>')
    hair = ("M232,130 C226,104 230,80 244,64 C254,52 268,44 284,40 C292,28 306,20 324,20 C344,20 362,30 372,46 "
            "C382,62 384,84 378,104 C376,114 374,122 372,130 C368,114 360,102 348,96 C336,90 322,88 308,90 "
            "C292,86 276,88 264,94 C250,100 240,112 236,122 C234,125 233,128 232,130 Z")
    s.part(hair, HAIR,
           shadow="M336,18 C368,24 388,52 384,84 C382,104 376,118 372,132 L356,98 C368,76 362,44 336,30 Z",
           shadow_col="#0b0b0e",
           hl="M250,70 C262,52 282,40 304,34 C318,24 336,22 350,26 C332,30 316,38 302,48 C284,56 268,68 258,84 Z",
           hl_col=SHEEN)
    for d in ("M262,86 C270,66 292,50 320,42", "M284,86 C298,66 322,54 350,52", "M306,88 C322,72 344,66 366,70"):
        s.line(d, 2.2, color="#5a5f70", op=0.7)
    for d in ("M286,42 C292,34 300,30 310,30 C302,36 296,42 292,50 Z", "M328,24 C340,22 352,26 360,34 C350,32 340,32 332,34 Z"):
        s.add(f'<path d="{d}" fill="#0b0b0e"/>')                  # lock separations
    s.add(f'<path d="M298,26 C316,18 336,16 352,22 C336,22 318,28 306,36 Z" fill="#6a7083" opacity="0.55"/>')


# =====================================================================================
#  BODY (front)
# =====================================================================================
TORSO = ("M300,290 C268,290 204,294 170,304 C146,312 136,330 136,356 L140,404 C148,432 162,452 172,470 "
         "C176,560 182,660 190,786 L410,786 C418,660 424,560 428,470 C438,452 452,432 460,404 L464,356 "
         "C464,330 454,312 430,304 C396,294 332,290 300,290 Z")


def _leg_open(s, lift, hip_x):
    """Start a group that shortens one leg from the hip (a lifted / bent leg) by `lift` px."""
    if lift <= 0.5:
        return False
    k = 1 - lift / 658.0
    s.add(f'<g transform="translate({hip_x},796) scale({1 + lift / 2600:.4f},{k:.4f}) translate({-hip_x},-796)">')
    return True


def legs(s, lift=(0.0, 0.0)):
    """lift = (left, right) in px: walking steps and jump tucks (0 = standing)."""
    leg = "M192,796 L298,796 L292,1404 L222,1404 C214,1180 204,980 192,796 Z"
    shoe = ("M216,1396 L294,1396 L296,1430 C296,1446 288,1454 272,1454 L190,1454 C176,1454 172,1440 182,1432 "
            "C194,1422 206,1412 216,1396 Z")
    g = _leg_open(s, lift[0], 245)
    s.part(leg, TROUSER, shadow="M258,780 L304,780 L300,1412 L266,1412 Z", shadow_col=TROUSER_SH,
           hl="M200,840 L214,840 L230,1390 L222,1390 Z", hl_col=TROUSER_HL)
    s.part(shoe, SHOE, shadow="M240,1440 L300,1440 L300,1460 L240,1460 Z", shadow_col="#0a0a0c",
           hl="M190,1432 C200,1424 214,1422 226,1424 L222,1430 Z", hl_col="#4a4d58")
    if g:
        s.add('</g>')
    g = _leg_open(s, lift[1], 355)
    s.part(mirror(leg), TROUSER, shadow="M318,780 L420,780 L420,1412 L346,1412 Z", shadow_col=TROUSER_SH,
           hl=mirror("M290,840 L298,840 L294,1390 L288,1390 Z"), hl_col=TROUSER_HL)
    s.part(mirror(shoe), SHOE, shadow="M300,1380 L440,1380 L440,1460 L300,1460 Z", shadow_col="#0a0a0c",
           hl=mirror("M190,1432 C200,1424 214,1422 226,1424 L222,1430 Z"), hl_col="#3a3d46")
    if g:
        s.add('</g>')
    _legs_rest(s)


def _legs_rest(s):
    s.add(f'<path d="M296,800 L300,880 L304,800 Z" fill="{TROUSER_SH}"/>')       # fly shadow


def torso(s):
    s.part(TORSO, SHIRT,
           shadow="M346,290 C406,296 466,316 464,374 C460,422 444,450 430,474 L414,790 L372,790 C392,660 396,500 382,320 Z",
           shadow_col=SHIRT_SH,
           deep_d="M138,392 C148,428 162,452 174,472 L184,472 C172,448 160,422 150,392 Z", deep_col=SHIRT_SH)
    # chest & fabric planes (fitted shirt on an athletic body)
    s.add(f'<path d="M196,452 C230,486 270,488 294,472 C270,494 230,494 200,466 Z" fill="{SHIRT_SH}"/>')
    s.add(f'<path d="M404,452 C370,486 330,488 306,472 C330,494 370,494 400,466 Z" fill="{SHIRT_DEEP}"/>')
    for d in ("M236,600 C254,610 276,610 292,602 C276,614 252,614 236,600 Z", "M206,760 C220,744 236,742 250,756 C236,752 220,754 206,760 Z",
              "M350,756 C364,742 380,744 394,760 C380,754 364,752 350,756 Z", "M238,520 C256,530 276,530 292,522 C276,534 254,534 238,520 Z"):
        s.add(f'<path d="{d}" fill="{SHIRT_SH}"/>')
    # neck opening (top button open) + collar
    s.part("M276,296 L324,296 L300,360 Z", SKIN, shadow="M300,290 L330,290 L300,364 Z", shadow_col=SKIN_SH)
    s.add(f'<path d="M288,312 Q300,318 312,312" fill="none" stroke="{SKIN_SH}" stroke-width="2" opacity="0.8"/>')
    lc = "M266,284 C258,296 256,314 260,334 L292,350 L276,298 Z"
    s.part(lc, SHIRT, shadow="M256,320 L292,320 L292,352 L256,352 Z", shadow_col=SHIRT_SH)
    s.part(mirror(lc), SHIRT, shadow=mirror(lc), shadow_col=SHIRT_SH)
    s.add(f'<path d="M268,286 Q300,280 332,286 L326,292 Q300,288 274,292 Z" fill="{SHIRT_SH}"/>')   # collar band
    # placket + buttons
    s.add(f'<path d="M298,360 L302,360 L304,786 L298,786 Z" fill="{SHIRT_SH}"/>')
    for y in (420, 490, 560, 630, 700, 770):
        s.add(f'<circle cx="304" cy="{y}" r="3.6" fill="#e2e5eb"/><circle cx="304" cy="{y}" r="1.6" fill="#b9bfcb"/>')
    # belt
    s.part("M188,786 L412,786 L414,814 L186,814 Z", BELT, shadow="M300,780 L420,780 L420,820 L300,820 Z", shadow_col="#0a0a0b")
    s.add(f'<rect x="286" y="788" width="28" height="24" rx="3" fill="none" stroke="{SILVER}" stroke-width="4"/>')


# ---------------- arms & hands ----------------
def hand(s, wrist, angle, kind, flip=False, watch=False):
    """Natural hand, no outline, two-tone. Local coords: wrist at (0,0), fingers toward +y."""
    x, y = wrist
    th = math.radians(angle)
    lx, ly = -math.cos(th), math.sin(th)               # world light direction (from the viewer's left) in local frame
    if flip:
        lx = -lx
    gid = s.two_tone(28 * lx, 28 * ly, -28 * lx, -28 * ly, SKIN, SKIN_SH, 0.6, SKIN_HL)
    F = f"url(#{gid})"
    g = []
    if kind == "relaxed":
        g.append(f'<path d="M-17,-10 C-22,12 -24,38 -20,62 C-18,80 -16,96 -12,110 C-10,118 -3,118 -2,110 L-1,92 '
                 f'C1,104 2,118 6,124 C9,128 15,126 15,118 L14,96 C16,104 18,112 22,114 C26,116 28,110 27,104 '
                 f'C26,86 24,62 23,40 C22,20 21,6 17,-10 Z" fill="{F}"/>')
        g.append(f'<path d="M20,18 C30,26 34,42 32,56 C31,64 25,66 22,60 C22,48 20,36 16,28 Z" fill="{F}"/>')   # thumb
        g.append(f'<path d="M-6,70 C-5,84 -3,96 -2,108 M6,74 C7,90 8,104 8,118 M15,76 C17,88 18,98 20,108" '
                 f'fill="none" stroke="{SKIN_DEEP}" stroke-width="1.6" opacity="0.6"/>')
    elif kind == "open":       # palm toward viewer, fingers spread (rotated to point up)
        g.append(f'<path d="M-22,-8 C-26,14 -26,38 -22,56 L22,56 C26,38 26,14 22,-8 Z" fill="{F}"/>')
        for fx, ln, w_ in ((-17, 40, 10), (-6, 48, 10.5), (6, 46, 10.5), (17, 38, 9.5)):
            g.append(f'<path d="M{fx},52 L{fx*1.12:.1f},{52+ln}" stroke="{F}" stroke-width="{w_}" stroke-linecap="round"/>')
        g.append(f'<path d="M-22,22 C-36,30 -44,42 -48,56" stroke="{F}" stroke-width="12" stroke-linecap="round" fill="none"/>')
        g.append(f'<path d="M-14,36 Q0,44 14,34" fill="none" stroke="{SKIN_DEEP}" stroke-width="1.6" opacity="0.6"/>')
    elif kind == "point":
        g.append(f'<path d="M-20,-8 C-25,16 -22,50 -10,62 L16,62 C26,52 26,16 20,-8 Z" fill="{F}"/>')
        g.append(f'<path d="M10,56 L12,116" stroke="{F}" stroke-width="11" stroke-linecap="round"/>')
        g.append(f'<path d="M-20,22 C-28,34 -22,46 -10,48" stroke="{F}" stroke-width="11" stroke-linecap="round" fill="none"/>')
        g.append(f'<path d="M-16,50 q8,10 18,8 M-18,38 q10,8 20,6" fill="none" stroke="{SKIN_DEEP}" stroke-width="1.6" opacity="0.6"/>')
    elif kind == "chin":
        g.append(f'<path d="M-20,-8 C-28,24 -24,58 -6,68 C8,74 22,64 26,48 C30,30 26,8 20,-8 Z" fill="{F}"/>')
        g.append(f'<path d="M-20,20 C-32,34 -28,50 -16,56" stroke="{F}" stroke-width="11" stroke-linecap="round" fill="none"/>')
        g.append(f'<path d="M-14,46 q12,8 30,0 M-16,58 q12,6 26,-2" fill="none" stroke="{SKIN_DEEP}" stroke-width="1.6" opacity="0.6"/>')
    elif kind == "tuck":       # hand tucked under the opposite arm (arms crossed): only the fingers show
        g.append(f'<path d="M-18,-8 C-22,10 -20,30 -12,40 L14,40 C20,30 22,10 18,-8 Z" fill="{F}"/>')
        g.append(f'<path d="M-10,30 L-10,40 M0,32 L0,42 M10,30 L10,40" fill="none" stroke="{SKIN_DEEP}" stroke-width="1.6" opacity="0.6"/>')
    if watch:
        g.append(f'<rect x="-21" y="-12" width="42" height="12" rx="3" fill="{STRAP}"/>'
                 f'<circle cx="0" cy="-6" r="8.5" fill="{GOLD}"/><circle cx="0" cy="-6" r="5.5" fill="#f4efe4"/>')
    sx = -1.25 if flip else 1.25
    s.add(f'<g transform="translate({x:.1f},{y:.1f}) rotate({angle:.1f})"><g transform="scale({sx},1.25)">{"".join(g)}</g></g>')


SLEEVE, FOREARM = 90, 62


def arm(s, shoulder, elbow, wrist, kind, flip, upper=True, watch=False):
    """Shirt sleeve folded below the elbow, then the bare forearm and the hand. No gaps, no outlines."""
    dx, dy = wrist[0] - elbow[0], wrist[1] - elbow[1]
    L = math.hypot(dx, dy) or 1
    ux, uy = dx / L, dy / L
    nx, ny = -uy, ux
    if nx < 0:
        nx, ny = -nx, -ny
    roll = (elbow[0] + 0.3 * dx, elbow[1] + 0.3 * dy)
    a = (roll[0] - ux * 13, roll[1] - uy * 13)
    b = (roll[0] + ux * 13, roll[1] + uy * 13)
    wx = (wrist[0] + ux * 14, wrist[1] + uy * 14)
    fm = (b[0] + (wx[0] - b[0]) * 0.35, b[1] + (wx[1] - b[1]) * 0.35)
    s.limb([b, fm, wx], [FOREARM, FOREARM + 4, FOREARM - 18], SKIN, SKIN_SH, SKIN_HL, 0.6)
    if upper:
        s.limb([shoulder, elbow, roll], [SLEEVE, SLEEVE - 6, SLEEVE - 8], SHIRT, SHIRT_SH, None, 0.62)
    else:
        s.limb([elbow, roll], [SLEEVE - 6, SLEEVE - 8], SHIRT, SHIRT_SH, None, 0.62)
    hw = (SLEEVE + 2) / 2
    band = (f"M{a[0]+nx*hw:.1f},{a[1]+ny*hw:.1f} Q{roll[0]+nx*(hw+4):.1f},{roll[1]+ny*(hw+4):.1f} {b[0]+nx*hw:.1f},{b[1]+ny*hw:.1f} "
            f"L{b[0]-nx*hw:.1f},{b[1]-ny*hw:.1f} Q{roll[0]-nx*(hw+4):.1f},{roll[1]-ny*(hw+4):.1f} {a[0]-nx*hw:.1f},{a[1]-ny*hw:.1f} Z")
    gid = s.two_tone(roll[0] - nx * hw, roll[1] - ny * hw, roll[0] + nx * hw, roll[1] + ny * hw, SHIRT, SHIRT_SH, 0.62)
    s.add(f'<path d="{band}" fill="url(#{gid})"/>')
    s.add(f'<path d="M{a[0]+nx*hw:.1f},{a[1]+ny*hw:.1f} L{a[0]-nx*hw:.1f},{a[1]-ny*hw:.1f}" stroke="{SHIRT_DEEP}" stroke-width="2.4"/>')
    s.add(f'<path d="M{roll[0]+nx*hw:.1f},{roll[1]+ny*hw:.1f} L{roll[0]-nx*hw:.1f},{roll[1]-ny*hw:.1f}" stroke="{SHIRT_SH}" stroke-width="2"/>')
    s.add(f'<path d="M{elbow[0]-nx*24-ux*30:.1f},{elbow[1]-ny*24-uy*30:.1f} q{nx*14:.1f},{ny*14+8:.1f} {nx*34:.1f},{ny*34:.1f}" '
          f'fill="none" stroke="{SHIRT_SH}" stroke-width="3"/>')
    hand(s, wrist, math.degrees(math.atan2(-dx, dy)), kind, flip, watch)


L_SH, R_SH = (166, 348), (434, 348)
ARMS = {
    "down": [(L_SH, (142, 576), (146, 776), "relaxed", False), (R_SH, (458, 576), (454, 776), "relaxed", False)],
    "explain": [(L_SH, (132, 592), (84, 462), "open", False), (R_SH, (458, 576), (454, 776), "relaxed", False)],
    "point": [(L_SH, (106, 444), (50, 320), "point", False), (R_SH, (458, 576), (454, 776), "relaxed", False)],
    "think": [(L_SH, (196, 604), (266, 352), "chin", True), (R_SH, (458, 576), (454, 776), "relaxed", False)],
    "welcome": [(L_SH, (128, 576), (80, 704), "open", False), (R_SH, (472, 576), (520, 704), "open", False)],
    "both_explain": [(L_SH, (132, 592), (84, 462), "open", False), (R_SH, (468, 592), (516, 462), "open", False)],
    # arms folded: his left forearm (with the watch) underneath, his right forearm on top
    "crossed": [(R_SH, (462, 552), (222, 486), "tuck", True), (L_SH, (138, 552), (378, 510), "tuck", True)],
}


def figure(pose="down", expr="neutral", blink=False, look=(0, 0), mouth=None, arms=None, lift=(0.0, 0.0), shadow=True):
    """arms: optional list of (shoulder, elbow, wrist, hand_kind, forearm_in_front) - used by the renderer
    to interpolate smoothly between poses. lift: leg lifts for walking/jumping. shadow: draw the floor shadow
    (the renderer draws its own when the character moves)."""
    s = Svg()
    if shadow:
        s.add('<ellipse cx="300" cy="1456" rx="190" ry="20" fill="#000" opacity="0.22"/>')
    legs(s, lift)
    arms = arms if arms is not None else ARMS[pose]
    for shoulder, elbow, wrist, kind, front in arms:      # sleeves sit behind the torso's shoulder line
        if not front:
            arm(s, shoulder, elbow, wrist, kind, shoulder[0] > 300, watch=shoulder[0] > 300)
    torso(s)
    for right in (False, True):                           # shoulder caps over the sleeve tops
        d = "M170,304 C146,312 136,330 136,356 L140,404 C152,410 174,406 190,392 C200,370 202,332 198,306 Z"
        d = mirror(d) if right else d
        s.part(d, SHIRT, shadow="M408,290 L470,290 L470,420 L408,420 Z" if right else None, shadow_col=SHIRT_SH)
    head(s, expr, blink, look, mouth)
    for shoulder, elbow, wrist, kind, front in arms:      # forearms in front of the body (think, crossed)
        if front:
            s.limb([shoulder, elbow], [SLEEVE, SLEEVE - 6], SHIRT, SHIRT_SH, None, 0.62)
            arm(s, shoulder, elbow, wrist, kind, shoulder[0] > 300, upper=False, watch=shoulder[0] > 300)
    return s.svg()


# =====================================================================================
#  TURNAROUND: side (facing left) and back
# =====================================================================================
def side_view():
    s = Svg()
    s.add('<ellipse cx="300" cy="1456" rx="140" ry="18" fill="#000" opacity="0.22"/>')
    s.part("M282,800 L356,800 L350,1404 L294,1404 Z", TROUSER_SH)
    shoe = ("M256,1396 L344,1396 L346,1430 C346,1446 338,1454 324,1454 L232,1454 C216,1454 212,1440 224,1432 "
            "C238,1424 248,1412 256,1396 Z")
    s.part(shoe.replace("256,", "268,").replace("224,1432", "238,1432"), "#0e0e10")
    s.part("M258,800 L346,800 L338,1404 L272,1404 Z", TROUSER, shadow="M316,790 L360,790 L350,1412 L310,1412 Z",
           shadow_col=TROUSER_SH, hl="M266,840 L274,840 L282,1390 L276,1390 Z", hl_col=TROUSER_HL)
    s.part(shoe, SHOE, hl="M226,1432 C236,1424 250,1422 262,1424 L258,1430 Z", hl_col="#4a4d58")
    s.part("M300,224 L350,220 L356,306 L298,306 Z", SKIN, shadow="M330,210 L370,210 L370,310 L330,310 Z", shadow_col=SKIN_SH)
    torso_d = ("M296,288 C266,290 244,308 236,340 C230,386 238,446 246,500 C250,560 252,640 252,700 "
               "C252,740 252,770 252,796 L366,796 C368,770 366,740 362,700 C358,620 366,500 372,420 "
               "C374,370 368,320 352,300 C336,292 316,286 296,288 Z")
    s.part(torso_d, SHIRT, shadow="M326,288 C372,300 376,420 370,520 C366,640 372,760 372,800 L340,800 "
                                  "C348,700 352,500 336,300 Z", shadow_col=SHIRT_SH)
    s.add(f'<path d="M244,420 C254,440 266,448 280,448 C266,454 252,448 244,436 Z" fill="{SHIRT_SH}"/>')
    s.part("M262,290 L290,290 L270,344 L250,320 Z", SKIN, shadow_col=SKIN_SH)
    s.part("M262,284 C256,296 252,314 256,332 L272,328 L268,298 Z", SHIRT, shadow="M250,310 L275,310 L275,335 L250,335 Z", shadow_col=SHIRT_SH)
    s.part("M250,786 L368,786 L370,814 L252,814 Z", BELT)
    arm(s, (312, 336), (306, 572), (298, 772), "relaxed", True, watch=True)
    face = ("M318,62 C350,62 378,82 386,114 C392,144 386,172 368,196 L344,230 C330,244 312,250 296,250 "
            "C284,250 272,244 266,234 C262,226 262,216 262,210 C258,206 256,202 258,198 C254,194 252,192 248,190 "
            "C242,188 238,184 242,178 L256,150 C260,142 260,136 258,128 C256,118 258,106 264,96 C274,74 294,62 318,62 Z")
    s.part(face, SKIN, shadow="M334,56 L420,56 L420,260 L334,260 Z", shadow_col=SKIN_SH,
           hl="M264,104 C268,90 276,80 288,72 C278,84 272,96 270,108 Z", hl_col=SKIN_HL)
    s.part("M334,130 C346,122 358,132 356,150 C354,168 344,178 334,174 Z", SKIN, shadow="M346,120 L370,120 L370,180 L346,180 Z", shadow_col=SKIN_SH)
    s.add(f'<path d="M248,118 C258,110 274,110 286,116 C276,120 264,122 252,126 Z" fill="{BROW}"/>')
    s.add(f'<path d="M256,140 C262,134 272,134 278,140 C272,144 262,144 256,140 Z" fill="#f6f1ea"/>'
          f'<circle cx="262" cy="140" r="4" fill="{IRIS}"/><path d="M254,139 C262,131 274,131 280,138 L280,136 C274,129 262,129 254,137 Z" fill="{BROW}"/>')
    s.part("M342,132 C350,170 348,208 332,234 C318,254 296,266 272,266 C258,264 252,254 255,244 "
           "C264,244 270,242 274,236 C276,226 276,218 280,210 C288,196 298,180 308,164 C316,152 322,144 326,136 Z", BEARD,
           shadow="M310,170 L360,170 L360,270 L310,270 Z", shadow_col="#0f0d0e")
    s.add(f'<path d="M250,194 C260,188 274,190 284,198 C278,206 264,208 252,204 Z" fill="{BEARD}"/>')
    s.add(f'<path d="M258,214 Q264,216 270,214" fill="none" stroke="#5a2c22" stroke-width="2.4"/>')
    s.add(f'<path d="M336,116 C348,104 366,108 378,124 L384,176 L338,176 Z" fill="url(#fade)"/>')
    hair = ("M258,100 C254,72 266,44 290,30 C310,18 340,16 362,24 C388,34 402,58 402,88 C402,112 396,132 388,150 "
            "L378,152 C376,136 370,124 360,118 L344,116 C338,128 336,140 334,152 L326,152 C322,134 312,118 296,108 "
            "C282,102 270,100 258,100 Z")
    s.part(hair, HAIR, shadow="M360,18 C392,30 406,70 396,110 L376,146 C380,110 376,60 352,30 Z", shadow_col="#0b0b0e",
           hl="M266,82 C276,56 300,36 330,26 C312,40 292,56 280,80 Z", hl_col=SHEEN)
    for d in ("M276,84 C296,58 330,44 370,48", "M300,98 C322,78 352,70 384,82"):
        s.line(d, 2.2, color="#3a3e4c", op=0.7)
    s.part("M334,130 C346,122 358,132 356,150 C354,168 344,178 334,174 Z", SKIN,
           shadow="M346,120 L370,120 L370,180 L346,180 Z", shadow_col=SKIN_SH)          # ear in front of the fade
    s.add(f'<path d="M340,140 C346,146 346,158 340,164" fill="none" stroke="{SKIN_DEEP}" stroke-width="2" opacity="0.7"/>')
    return s.svg()


def back_view():
    s = Svg()
    s.add('<ellipse cx="300" cy="1456" rx="190" ry="20" fill="#000" opacity="0.22"/>')
    legs(s)
    for shoulder, elbow, wrist, kind, front in ARMS["down"]:
        arm(s, shoulder, elbow, wrist, kind, shoulder[0] < 300, watch=shoulder[0] < 300)
    s.part("M272,210 L272,304 L328,304 L328,210 Z", SKIN, shadow="M308,200 L340,200 L340,310 L308,310 Z", shadow_col=SKIN_SH)
    s.part(TORSO, SHIRT, shadow="M344,290 C400,296 452,316 450,372 C446,420 432,448 424,472 L414,790 L372,790 C390,660 394,500 380,320 Z",
           shadow_col=SHIRT_SH)
    s.add(f'<path d="M188,330 C240,350 360,350 412,330 C360,356 240,356 188,330 Z" fill="{SHIRT_SH}"/>')     # yoke seam
    s.add(f'<path d="M298,360 L302,360 L302,780 L298,780 Z" fill="{SHIRT_SH}" opacity="0.6"/>')
    s.part("M266,284 Q300,272 334,284 L330,302 Q300,294 270,302 Z", SHIRT, shadow="M300,270 L340,270 L340,306 L300,306 Z", shadow_col=SHIRT_SH)
    s.part("M188,786 L412,786 L414,814 L186,814 Z", BELT)
    ear = "M233,134 C222,128 215,136 216,152 C217,166 224,176 236,174 Z"
    s.part(ear, SKIN, shadow_col=SKIN_SH)
    s.part(mirror(ear), SKIN, shadow=mirror(ear), shadow_col=SKIN_SH)
    nape = "M232,122 C232,190 258,226 300,230 C342,226 368,190 368,122 Z"
    s.part(nape, SKIN, shadow="M310,120 L380,120 L380,240 L310,240 Z", shadow_col=SKIN_SH)
    s.defs.append(f'<clipPath id="napeclip"><path d="{nape}"/></clipPath>')
    s.add('<g clip-path="url(#napeclip)"><rect x="220" y="118" width="160" height="96" fill="url(#fade)"/></g>')
    hair = ("M232,128 C226,96 238,62 262,42 C282,26 318,22 342,34 C366,46 376,74 370,104 C368,114 368,122 368,128 "
            "C346,124 324,122 300,122 C276,122 254,124 232,128 Z")
    s.part(hair, HAIR, shadow="M320,20 L390,20 L390,140 L330,140 C352,100 348,60 320,30 Z", shadow_col="#0b0b0e",
           hl="M256,60 C266,46 282,38 298,36 C284,44 272,54 264,66 Z", hl_col=SHEEN)
    for d in ("M262,60 C276,80 284,100 288,118", "M300,40 C304,64 304,92 302,118", "M336,56 C328,78 322,100 318,118"):
        s.line(d, 2, color="#3a3e4c", op=0.7)
    return s.svg()


def head_only(expr, blink=False, look=(0, 0)):
    s = Svg()
    head(s, expr, blink, look)
    return s.svg().replace(f'viewBox="0 0 {W} {H}" width="{W}" height="{H}"', 'viewBox="196 0 208 300" width="208" height="300"')


# base poses: (body pose, expression, eye look). Each gets <name>, <name>_blink and 5 mouth shapes
# <name>_m1 (slightly open), <name>_talk (open), <name>_m3 (wide), <name>_oo (round), <name>_ee (wide, teeth)
BASES = {
    "idle": ("down", "neutral", (0, 0)), "warm": ("down", "warm", (0, 0)), "serious": ("down", "serious", (0, 0)),
    "explain": ("explain", "warm", (0, 0)), "point": ("point", "neutral", (-3, -2)), "think": ("think", "think", (3, -3)),
    "welcome": ("welcome", "smile", (0, 0)), "surprised": ("both_explain", "surprised", (0, 0)),
    "crossed": ("crossed", "serious", (0, 0)),
    # reaction faces for comedy beats (job "beats"); never picked by auto acting
    "deadpan": ("crossed", "deadpan", (0, 0)), "side_eye": ("down", "side_eye", (10, 1)),
    "smirk": ("explain", "smirk", (-1, 0)),
}
MOUTHS = ["m1", "talk", "m3", "oo", "ee"]
POSES = {}
for _n, (_p, _e, _l) in BASES.items():
    POSES[_n] = dict(pose=_p, expr=_e, look=_l)
    POSES[_n + "_blink"] = dict(pose=_p, expr=_e, look=_l, blink=True)
    for _m in MOUTHS:
        POSES[f"{_n}_{_m}"] = dict(pose=_p, expr=_e, look=_l, mouth=_m)
POSES["talk"] = POSES["idle_talk"]      # legacy names used by older jobs
POSES["blink"] = POSES["idle_blink"]

EXPRESSIONS = ["neutral", "warm", "smile", "talk", "think", "surprised", "serious", "laugh",
               "deadpan", "side_eye", "smirk"]

if __name__ == "__main__":
    for f in os.listdir(D):
        if f.endswith(".svg"):
            os.remove(os.path.join(D, f))
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
