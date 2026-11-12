"""2026-11-12-b: "Why do we get goosebumps?" (big-question, the human body). 2D Ved + townspeople in a snowy winter town
square (Blender plates: cocoa stall + snowman), a giant cut-away skin block (hair follicle, arrector pili muscle, nerve;
relaxed and cold states), and a macro skin landscape with tree-sized hairs (flat, then goosebumped).
Run after the assets exist: python jobs/2026-11-12-b/build_job.py
"""
import json, math, os, sys
sys.path.insert(0, os.getcwd())
from autopilot.stage import Stage

ID = "2026-11-12-b"
J = f"jobs/{ID}/"
A = J + "assets/"
PV = "/tmp/claude-0/-home-claude-shorts-autopilot/efbfe82d-4223-5616-a582-6335401cbe5d/scratchpad/pv/"
SRC = A if os.path.exists(A + "headphones.png") else PV
QA = os.environ.get("QA")
if QA:
    A = PV
ST = {n: Stage(SRC + f"plate_{n}.json") for n in ("square_wide", "cocoa_mid", "skin_relaxed", "skin_cold", "skin_wide")}

OUT = {   # same people, same outfits in every shot
    "tomas": {"skin": "#a86f4c", "build": "round", "hat": ["cap", "#7c2533"], "top": ["#46965a", "jacket"], "apron": "#f6efe2",
              "bottom": ["#34425c", "trousers"]},
    "aiko": {"skin": "#f0c8a8", "hair": ["#1d1712", "long"], "hat": ["beret", "#d9534f"], "top": ["#6fc3c0", "jacket"],
             "bottom": ["#34425c", "trousers"], "bag": "#8a5a3c"},
    "raj": {"skin": "#6b4430", "build": "slim", "hair": ["#1d1712", "short"], "top": ["#f2b04a", "jacket"],
            "bottom": ["#4a3b30", "trousers"]},
}
F = "font-family='Poppins, DejaVu Sans, sans-serif' font-weight='800'"
AN = "font-family='Anton, DejaVu Sans, sans-serif'"


def plate(name, blur=0, **k):
    return {"type": "image", "path": A + f"plate_{name}.png", "x": 0.5, "y": 0.5, "w": 1.0, "enter": "none", "blur": blur, **k}


def fg(name):
    return {"type": "image", "path": A + f"fg_{name}.png", "x": 0.5, "y": 0.5, "w": 1.0, "enter": "none", "_depth": 0.6}


def sprite(name, x, y, w, **k):
    return {"type": "image", "path": A + name + ".png", "x": x, "y": y, "w": w, "enter": k.pop("enter", "none"), **k}


def txt(t, y, size=96, **k):
    return {"type": "text", "text": t, "font": "display", "x": k.pop("x", 0.5), "y": y, "size": size, "max_w": 0.88,
            "stroke": "#0b0f12", "stroke_width": 7, **k}


def card(svg, y, w=0.84, at=0.3, **k):
    return {"type": "image", "svg": svg, "w": w, "x": k.pop("x", 0.5), "y": y, "enter": k.pop("enter", "pop"), "at": at,
            "sfx": k.pop("sfx", "pop"), **k}


def person(set_, who, wx, wy, acting, walk=None, hops=None, **k):
    st = ST[set_]
    p = st.place(wx, wy, "extra")
    L = {"type": "character", "id": "extra", "pose": acting[0][0], "x": p["x"], "y": p["y"], "h": p["h"], "enter": "none",
         "acting": acting, "talk": False, "rig_args": {"outfit": OUT[who]}, "_depth": wy, "allow_outside_safe": True}
    if walk:
        L["keys"] = st.walk(walk, p, "extra")
    if hops:
        L["hops"] = hops
    L.update(k)
    return L


def ved(set_, wx, wy, acting, walk=None, hops=None, **k):
    st = ST[set_]
    p = st.place(wx, wy, "ved")
    L = {"type": "character", "id": "ved", "pose": acting[0][0], "x": p["x"], "y": p["y"], "h": p["h"], "enter": "none",
         "acting": acting, "_depth": wy, "allow_outside_safe": True}
    if walk:
        L["keys"] = st.walk(walk, p, "ved")
    if hops:
        L["hops"] = hops
    L.update(k)
    return L


def close_ved(acting, **k):
    return {"type": "character", "id": "ved", "pose": acting[0][0], "x": 0.5, "y": 0.8, "h": 1.06, "enter": "none",
            "acting": acting, "ground": False, "allow_outside_safe": True, **k}


def staged(set_, people=(), extra_top=(), with_fg=False):
    layers = list(people) + ([fg(set_)] if with_fg else [])
    out = [plate(set_)] + sorted(layers, key=lambda L: -L["_depth"]) + list(extra_top)
    for L in out:
        L.pop("_depth", None)
    return out


def tag(text, color, w=440):
    """A small cream label pill."""
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 %d 96'><rect x='3' y='3' width='%d' height='90' rx='45' fill='#f6efe2' "
            "stroke='#1a1410' stroke-width='6'/><text x='%d' y='64' text-anchor='middle' font-size='44' fill='%s' %s>%s</text></svg>"
            % (w, w - 6, w // 2, color, F, text))


def label(text, color, x, y, w, at, **k):
    return {"type": "image", "svg": tag(text, color, int(w * 1000)), "w": w, "x": x, "y": y, "enter": "pop", "at": at, "sfx": "pop", **k}


def line(p0, p1, at, color="#f6efe2", width=0.008):
    """A thin pointer line from a label to a 3D spot (screen fractions)."""
    x0, y0 = p0; x1, y1 = p1
    dx, dy = (x1 - x0) * 1080, (y1 - y0) * 1920
    L = math.hypot(dx, dy) / 1080
    ang = math.degrees(math.atan2(dy, dx))
    return {"type": "shape", "shape": "rect", "w": L, "h": width, "color": color, "x": (x0 + x1) / 2, "y": (y0 + y1) / 2,
            "rotate": ang, "enter": "fade", "at": at, "radius": 0.004}


def dot(p, at, color="#f2b04a", r=0.035, **k):
    return {"type": "shape", "shape": "ring", "w": r, "h": r, "color": color, "x": p[0], "y": p[1], "enter": "pop", "at": at,
            "stroke_width": 8, **k}


# 3D anchor points on the skin block (must match assets.py)
D = 1.6
Z0 = 0.18
EPI = Z0 + 1.34
P = (-0.15, -D / 2 - 0.02, EPI)


def hair_pts(cold):
    a = math.radians(8 if cold else 42)
    ux, uz = math.sin(a), math.cos(a)
    tip = (P[0] + ux * 0.9, P[1], P[2] + uz * 0.9)
    mid = (P[0] - ux * 0.55, P[2] - uz * 0.55)
    anc = (P[0] + (0.42 if cold else 0.62), Z0 + 1.2)
    mus = ((mid[0] + anc[0]) / 2, P[1], (mid[1] + anc[1]) / 2)
    bulb = (P[0] - ux * 0.95, P[1], P[2] - uz * 0.95)
    return tip, mus, bulb


S = []
sw = ST["square_wide"]
# 1. HOOK (snowy square): the question on screen at frame 0
S.append({"say": "Why does cold make your skin look like a plucked *goose*?",
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.2, "zoom": 1.06, "focus": [0.5, 0.5]}]},
          "caption_y": 0.41,
          "layers": staged("square_wide",
                           [person("square_wide", "tomas", -2.3, 1.75, [["sad", 0], ["hold", 1.6]]),
                            person("square_wide", "aiko", 1.2, -0.4, [["sad", 0]], walk=[(0, 3.4, -0.6), (2.6, 1.2, -0.4)]),
                            person("square_wide", "raj", -0.4, -1.4, [["sad", 0], ["shrug", 1.8]]),
                            ved("square_wide", 1.2, -4.6, [["surprised", 0], ["think", 1.4]])],
                           [sprite("thermo", 0.14, 0.27, 0.075, enter="none", keys=[{"t": 0, "rot": -8}, {"t": 2.0, "rot": 6}]),
                            txt("WHY DO WE GET", 0.1, 96, enter="none"),
                            txt("*GOOSEBUMPS?*", 0.17, 132, enter="none")], with_fg=True)})
# 2. close-up: blame a muscle
S.append({"say": "Blame a tiny muscle. Almost every hair on your body has its *own*.", "transition": "cut",
          "caption_y": 0.64,
          "layers": [plate("square_wide", blur=10, keys=[{"t": 0, "scale": 1.35}, {"t": 4.6, "scale": 1.42}]),
                     close_ved([["explain", 0], ["point", 2.4]]),
                     txt("1 HAIR", 0.1, 100, enter="pop", at=0.6, sfx="pop"),
                     txt("= 1 *MUSCLE*", 0.19, 100, enter="pop", at=2.6, sfx="pop")]})
# 3. the giant skin block (wide): Ved walks up to it
sk = ST["skin_wide"]
tip, mus, bulb = hair_pts(True)
S.append({"say": "Here's your skin, cut open. That red one is the *arrector pili*.", "transition": "slide_left",
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.0, "zoom": 1.08, "focus": [0.55, 0.5]}]},
          "caption_y": 0.3,
          "layers": staged("skin_wide",
                           [ved("skin_wide", 1.45, -2.1, [["welcome", 0], ["point", 2.0]], walk=[(0, 3.6, -2.1), (1.3, 1.45, -2.1)], flip=True)],
                           [txt("YOUR SKIN,", 0.1, 90, enter="pop", at=0.2, sfx="pop"),
                            txt("*CUT OPEN*", 0.17, 100, enter="pop", at=0.9, sfx="pop"),
                            dot(sk.point(*mus), 2.4, "#f2b04a", 0.07, loop="pulse")])})
# 4. relaxed -> cold (crossfade): the nerve fires, the muscle squeezes, the hair stands up
r_tip, r_mus, r_bulb = hair_pts(False)
sr = ST["skin_relaxed"]; sc = ST["skin_cold"]
nerve = sr.point(-0.4, P[1], Z0 + 0.76)
S.append({"say": "Relaxed, your hair lies flat. Get cold, a nerve fires, and the muscle *squeezes*.", "transition": "cut",
          "caption_y": 0.3,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.55]}, {"t": 5.0, "zoom": 1.06, "focus": [0.5, 0.55]}]},
          "layers": [plate("skin_cold"),
                     plate("skin_relaxed", keys=[{"t": 0, "opacity": 1}, {"t": 3.6, "opacity": 1}, {"t": 4.2, "opacity": 0}]),
                     label("HAIR", "#5a3a20", sr.point(*r_tip)[0] + 0.1, sr.point(*r_tip)[1] - 0.03, 0.26, 0.3, until=3.6, exit="fade"),
                     label("NERVE", "#b88a00", max(0.2, nerve[0]), nerve[1] + 0.1, 0.3, 1.9),
                     label("MUSCLE", "#c8303a", sr.point(*r_mus)[0] + 0.18, sr.point(*r_mus)[1] + 0.12, 0.34, 0.9),
                     dot(nerve, 2.6, "#ffd84a", 0.06, loop="pulse"),
                     txt("*SQUEEZE!*", 0.12, 120, enter="pop", at=3.7, sfx="pop")]})
# 5. cold: the hair stands, the skin bunches into a bump
bump = sc.point(P[0] + 0.03, P[1], EPI + 0.1)
S.append({"say": "The hair stands up, and the skin bunches into a bump. A *goosebump*.", "transition": "cut", "caption_y": 0.3,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.2, "zoom": 1.18, "focus": [bump[0], bump[1]]}]},
          "layers": [plate("skin_cold"),
                     label("HAIR UP", "#5a3a20", sc.point(*tip)[0] + 0.2, sc.point(*tip)[1] + 0.02, 0.32, 0.2),
                     dot(bump, 1.8, "#f2b04a", 0.16),
                     txt("GOOSE*BUMP*", 0.12, 120, enter="pop", at=2.4, sfx="ding")]})
# 6. the macro skin landscape: thousands at once
S.append({"say": "Now times that by *thousands* of hairs.", "transition": "zoom",
          "caption_y": 0.41,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.55]}, {"t": 3.0, "zoom": 1.1, "focus": [0.5, 0.6]}]},
          "layers": [plate("macro_cold"),
                     plate("macro_relaxed", keys=[{"t": 0, "opacity": 1}, {"t": 0.9, "opacity": 1}, {"t": 1.5, "opacity": 0}]),
                     {"type": "counter", "from": 1, "to": 5000, "count_dur": 1.4, "at": 0.6, "prefix": "x", "x": 0.5, "y": 0.15,
                      "size": 150, "color": "#f2b04a", "stroke": "#0b0f12", "stroke_width": 8, "enter": "pop", "sfx": "riser"}]})
# 7. why: fur traps warm air (infographic)
fur = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 900 560'><rect width='900' height='560' rx='34' fill='#f6efe2'/>"
       "<rect width='900' height='560' rx='34' fill='none' stroke='#1a1410' stroke-width='6'/>"
       f"<text x='225' y='70' text-anchor='middle' font-size='40' fill='#5a4636' {F}>FLAT FUR</text>"
       f"<text x='675' y='70' text-anchor='middle' font-size='40' fill='#d98a1a' {F}>FLUFFED UP</text>"
       "<line x1='450' y1='40' x2='450' y2='470' stroke='#1a1410' stroke-width='4' stroke-dasharray='14 12'/>"
       # left: skin band + flat hairs, thin air layer
       "<rect x='60' y='330' width='330' height='70' rx='10' fill='#dba07e'/>"
       + "".join(f"<line x1='{80 + k * 30}' y1='330' x2='{112 + k * 30}' y2='310' stroke='#3b2716' stroke-width='7' stroke-linecap='round'/>" for k in range(10)) +
       "<rect x='60' y='290' width='330' height='22' rx='8' fill='#f2b04a' opacity='0.5'/>"
       f"<text x='225' y='250' text-anchor='middle' font-size='34' fill='#4a8fe0' {F}>COLD GETS IN</text>"
       # right: skin band + upright hairs, thick warm-air layer
       "<rect x='510' y='160' width='330' height='170' rx='16' fill='#f2b04a' opacity='0.55'/>"
       "<rect x='510' y='330' width='330' height='70' rx='10' fill='#dba07e'/>"
       + "".join(f"<line x1='{530 + k * 30}' y1='330' x2='{534 + k * 30}' y2='175' stroke='#3b2716' stroke-width='7' stroke-linecap='round'/>" for k in range(10)) +
       f"<text x='675' y='135' text-anchor='middle' font-size='34' fill='#d9534f' {F}>WARM AIR TRAPPED</text>"
       f"<text x='450' y='520' text-anchor='middle' font-size='46' fill='#1a1410' {AN}>FUR + AIR = A BLANKET</text></svg>")
S.append({"say": "Why bother? On a furry animal, fluffed-up fur traps a blanket of *warm air*.", "transition": "slide_up",
          "caption_y": 0.64,
          "layers": [plate("macro_cold", blur=8, keys=[{"t": 0, "scale": 1.15}, {"t": 5, "scale": 1.21}]),
                     card(fur, 0.27, w=0.9, at=0.3)],})
# 8. looking bigger: cat and porcupine (wide square, Ved points at the panel)


def cat(cx, cy, s, puffed):
    out = ""
    if puffed:   # spiky fluffed outline
        pts = []
        for k in range(36):
            a = k / 36 * 2 * math.pi
            r = (118 if k % 2 else 96) * s
            pts.append(f"{cx + math.cos(a) * r * 1.25:.0f},{cy + math.sin(a) * r * 0.9:.0f}")
        out += f"<polygon points='{' '.join(pts)}' fill='#5a4636'/>"
        out += f"<path d='M{cx + 120 * s} {cy - 10 * s} q {60 * s} {-50 * s} {40 * s} {-150 * s}' stroke='#5a4636' stroke-width='{44 * s}' fill='none' stroke-linecap='round'/>"
    else:
        out += f"<ellipse cx='{cx}' cy='{cy}' rx='{95 * s}' ry='{55 * s}' fill='#5a4636'/>"
        out += f"<path d='M{cx + 90 * s} {cy} q {50 * s} {-30 * s} {40 * s} {-100 * s}' stroke='#5a4636' stroke-width='{18 * s}' fill='none' stroke-linecap='round'/>"
    hx, hy = cx - (115 if puffed else 95) * s, cy - (70 if puffed else 50) * s
    out += f"<circle cx='{hx}' cy='{hy}' r='{48 * s}' fill='#5a4636'/>"
    out += f"<polygon points='{hx - 40 * s},{hy - 22 * s} {hx - 30 * s},{hy - 80 * s} {hx - 4 * s},{hy - 40 * s}' fill='#5a4636'/>"
    out += f"<polygon points='{hx + 40 * s},{hy - 22 * s} {hx + 30 * s},{hy - 80 * s} {hx + 4 * s},{hy - 40 * s}' fill='#5a4636'/>"
    out += f"<circle cx='{hx - 16 * s}' cy='{hy - 4 * s}' r='{9 * s}' fill='#f2b04a'/><circle cx='{hx + 16 * s}' cy='{hy - 4 * s}' r='{9 * s}' fill='#f2b04a'/>"
    for sx in (-50, -15, 30, 60):     # legs
        out += f"<rect x='{cx + sx * s}' y='{cy + (40 if puffed else 35) * s}' width='{16 * s}' height='{(70 if puffed else 55) * s}' rx='{6 * s}' fill='#5a4636'/>"
    return out


def porcupine(cx, cy, s):
    out = ""
    for k in range(17):
        a = math.radians(200 + k * 8.5)
        out += (f"<line x1='{cx + math.cos(a) * 60 * s:.0f}' y1='{cy + math.sin(a) * 40 * s:.0f}' x2='{cx + math.cos(a) * 150 * s:.0f}' "
                f"y2='{cy + math.sin(a) * 120 * s:.0f}' stroke='#f6efe2' stroke-width='{9 * s:.0f}' stroke-linecap='round'/>"
                f"<line x1='{cx + math.cos(a) * 60 * s:.0f}' y1='{cy + math.sin(a) * 40 * s:.0f}' x2='{cx + math.cos(a) * 118 * s:.0f}' "
                f"y2='{cy + math.sin(a) * 92 * s:.0f}' stroke='#3b2716' stroke-width='{9 * s:.0f}' stroke-linecap='round'/>")
    out += f"<ellipse cx='{cx}' cy='{cy}' rx='{95 * s}' ry='{52 * s}' fill='#6b4a30'/>"
    out += f"<ellipse cx='{cx - 92 * s}' cy='{cy + 14 * s}' rx='{34 * s}' ry='{24 * s}' fill='#8a6142'/>"
    out += f"<circle cx='{cx - 100 * s}' cy='{cy + 6 * s}' r='{6 * s}' fill='#1a1410'/>"
    return out


big = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 900 520'><rect width='900' height='520' rx='34' fill='#f6efe2'/>"
       "<rect width='900' height='520' rx='34' fill='none' stroke='#1a1410' stroke-width='6'/>"
       f"<text x='240' y='70' text-anchor='middle' font-size='40' fill='#d9534f' {F}>SCARED CAT</text>"
       f"<text x='680' y='70' text-anchor='middle' font-size='40' fill='#d9534f' {F}>PORCUPINE</text>"
       + cat(250, 300, 1.15, True) + porcupine(690, 330, 1.25) +
       f"<text x='450' y='485' text-anchor='middle' font-size='46' fill='#1a1410' {AN}>LOOK BIGGER = LOOK SCARIER</text></svg>")
S.append({"say": "It also makes them look *bigger*. That's the puffed-up cat, and the porcupine's quills.", "transition": "slide_left",
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 5.0, "zoom": 1.06, "focus": [0.5, 0.52]}]},
          "caption_y": 0.41,
          "layers": staged("square_wide",
                           [person("square_wide", "raj", 0.6, 1.6, [["idle", 0], ["surprised", 2.6]]),
                            person("square_wide", "tomas", -2.3, 1.75, [["idle", 0]]),
                            ved("square_wide", -1.3, -3.8, [["explain", 0], ["point", 1.0]], walk=[(0, -4.2, -3.8), (1.1, -1.3, -3.8)],
                                hops=[[2.7, 0.05, 0.4]])],
                           [card(big, 0.2, w=0.88, at=0.4)], with_fg=True)})
# 9. close: we kept the reflex
S.append({"say": "Our ancestors had the fur. We lost it, but kept the *reflex*.", "transition": "cut",
          "caption_y": 0.64,
          "layers": [plate("square_wide", blur=10, keys=[{"t": 0, "scale": 1.35}, {"t": 4.0, "scale": 1.42}]),
                     close_ved([["explain", 0], ["shrug", 2.2]]),
                     txt("FUR: *GONE*", 0.1, 100, enter="pop", at=0.7, sfx="pop"),
                     txt("REFLEX: *STILL HERE*", 0.19, 84, enter="pop", at=2.4, sfx="pop")]})
# 10. comic beat (reaction cut-away)
S.append({"dur": 1.7, "transition": "cut", "captions": False,
          "layers": [plate("square_wide", blur=10, keys=[{"t": 0, "scale": 1.35}]), dict(close_ved([["deadpan", 0]]), acting="none")],
          "beat": {"kind": "deadpan", "at": 0.1, "dur": 1.5, "text": "Me trying to look scary with *3 arm hairs*", "text_y": 0.18}})
# 11. the cocoa stall: emotions trigger it too
S.append({"say": "The same alarm fires for fear, awe, or a great song. That's music *chills*.", "transition": "slide_left",
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.6, "zoom": 1.07, "focus": [0.5, 0.52]}]},
          "caption_y": 0.72,
          "layers": staged("cocoa_mid",
                           [person("cocoa_mid", "tomas", -2.35, 1.75, [["idle", 0], ["give", 1.0]]),
                            person("cocoa_mid", "aiko", -1.4, -0.6, [["idle", 0], ["surprised", 2.6], ["cheer", 3.2]],
                                   walk=[(0, 0.2, -0.9), (1.4, -1.4, -0.6)], hops=[[3.3, 0.06, 0.45]])],
                           [label("FEAR", "#34425c", 0.2, 0.12, 0.26, 0.6),
                            label("AWE", "#2f8f8a", 0.5, 0.12, 0.22, 1.2),
                            label("MUSIC", "#d9534f", 0.8, 0.12, 0.28, 1.8),
                            sprite("headphones", 0.72, 0.27, 0.26, enter="pop", at=2.4, sfx="pop", keys=[{"t": 0, "rot": 8}, {"t": 2.5, "rot": -6}]),
                            txt("*CHILLS*", 0.37, 120, enter="pop", at=3.4, sfx="pop")], with_fg=True)})
# 12. close payoff
S.append({"say": "So a goosebump is your body putting on a fur coat... you *don't have*.",
          "transition": "cut", "caption_y": 0.64,
          "layers": [plate("square_wide", blur=10, keys=[{"t": 0, "scale": 1.35}, {"t": 5.0, "scale": 1.43}]),
                     close_ved([["warm", 0], ["explain", 1.6], ["smirk", 3.4]]),
                     sprite("mug", 0.82, 0.13, 0.2, enter="pop", at=0.5, sfx="pop", keys=[{"t": 0, "rot": 10}, {"t": 4, "rot": -4}]),
                     txt("A FUR COAT", 0.1, 100, enter="pop", at=0.6, x=0.42),
                     txt("YOU *DON'T HAVE*", 0.19, 92, enter="pop", at=3.0, sfx="ding")]})

SRCS = ["https://www.health.harvard.edu/blog/wondering-about-goosebumps-of-course-you-are-2020080320688",
        "https://livescience.com/32349-what-causes-goose-bumps.html",
        "https://neurosciencenews.com/goosebumps-reason-16669/"]
job = {"id": ID, "title": "Why do we get goosebumps? 🥶",
       "description": "Goosebumps are a tiny muscle at work: the arrector pili. Cold (or a strong feeling) fires a nerve, the muscle "
                      "squeezes, the hair stands up and the skin bunches into a bump. On furry animals that traps warm air and makes "
                      "them look bigger; we lost the fur but kept the reflex.\n\nSources: " + " ; ".join(SRCS),
       "tags": ["goosebumps", "human body", "biology", "arrector pili", "evolution", "science explained", "why do we get goosebumps",
                "chills", "explained"],
       "hashtags": ["#science", "#humanbody"],
       "meta": {"format": "big-question", "topic": "why we get goosebumps (arrector pili, fur, vestigial reflex, emotional chills)",
                "hook": "question", "idea_source": "backlog (ideas.md: Why do we get goosebumps?)",
                "characters": ["ved", "extra"], "sources": SRCS,
                "humour": {"trend": "'Me when / me trying to' caption hook (still a top recurring Reels/TikTok title hook, Nov 2026); deadpan card 'Me trying to look scary with 3 arm hairs'",
                           "beat": "deadpan", "scene": 9}},
       "privacy": "public", "speaker": "ved", "assets_script": J + "assets.py", "scenes": S}
if QA:
    job.pop("assets_script")
OUTF = PV + "../job_qa.json" if QA else J + "job.json"
json.dump(job, open(OUTF, "w"), indent=1, ensure_ascii=False)
print("scenes", len(S), "using", SRC)
