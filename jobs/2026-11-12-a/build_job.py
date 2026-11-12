"""2026-11-12-a: "Do bulls really hate red?" (myth-bust).
2D Ved + townspeople (a man dressed head-to-toe in red, two cowboys, a cape waver) staged in depth inside a Blender ranch
arena (wide / mid / low angles) built from stills; the bull and the flags are animated 3D cut-outs; the cone chart, the
"what a bull sees" swatches, the 2007 test card and the two capes are 2D panels.
Run after the assets exist: python jobs/2026-11-12-a/build_job.py
"""
import json, os, sys
sys.path.insert(0, os.getcwd())
from autopilot.stage import Stage

ID = "2026-11-12-a"
J = f"jobs/{ID}/"
A = J + "assets/"
ST = {n: Stage(A + f"plate_{n}.json") for n in ("arena_wide", "arena_mid", "arena_low")}

OUT = {   # recurring people: same outfits in every shot
    "rojo": {"skin": "#c98e6a", "top": ["#c41e1a", "shirt"], "bottom": ["#a51815", "trousers"], "hair": ["#1a1410", "short"],
             "hat": ["cap", "#c41e1a"], "shoes": "#7c1512"},                                     # the man in all red
    "dusty": {"skin": "#8d5a3b", "top": ["#6fa3d6", "shirt"], "bottom": ["#34425c", "trousers"], "hair": ["#1a1410", "short"],
              "hat": ["straw", "#e8c77a"], "belt": "#5e3f2a", "shoes": "#5e3f2a"},                 # cowboy 1
    "jo": {"skin": "#e0b08a", "top": ["#f2b04a", "vest"], "bottom": ["#34425c", "trousers"], "hair": ["#7a4a2a", "long"],
           "hat": ["straw", "#d9b56a"], "shoes": "#5e3f2a", "build": "slim"},                       # cowboy 2
}
F = "font-family='Poppins, DejaVu Sans, sans-serif' font-weight='800'"
AN = "font-family='Anton, DejaVu Sans, sans-serif'"


def plate(name, blur=0, **k):
    return {"type": "image", "path": A + f"plate_{name}.png", "x": 0.5, "y": 0.5, "w": 1.0, "enter": "none", "blur": blur, **k}


def sprite(name, x, y, w, **k):
    return {"type": "image", "path": A + name + ".png", "x": x, "y": y, "w": w, "enter": k.pop("enter", "none"), **k}


def txt(t, y, size=96, **k):
    return {"type": "text", "text": t, "font": "display", "x": 0.5, "y": y, "size": size, "max_w": 0.88,
            "stroke": "#0b0f12", "stroke_width": 7, **k}


# props in the world: (world width in metres, z of the sprite centre, x offset of the sprite centre from the anchor)
PROP = {"bull_charge": (2.35, 0.85, 0.05), "bull_stand": (2.0, 0.85, 0.2), "flag_red": (1.0, 0.97, 0.47),
        "flag_blue": (1.0, 0.97, 0.47), "flag_white": (1.0, 0.97, 0.47)}


def prop(set_, name, wx, wy, flip=False, path=None, **k):
    """A cut-out standing at floor position (wx, wy); path = [(t, wx, wy), ...] moves it (scale follows depth)."""
    st = ST[set_]
    ww, zc, dx = PROP[name]
    dx = -dx if flip else dx

    def at(px, py):
        x0, _ = st.point(px + dx - ww / 2, py, zc)
        x1, _ = st.point(px + dx + ww / 2, py, zc)
        cx, cy = st.point(px + dx, py, zc)
        return cx, cy, x1 - x0
    cx, cy, w = at(wx, wy)
    L = sprite(name, round(cx, 4), round(cy, 4), round(w, 4), flip=flip, _depth=wy, allow_outside_safe=True, **k)
    if path:
        keys = []
        for i, (t, px, py) in enumerate(path):
            x, y, ww2 = at(px, py)
            kk = {"t": t, "x": round(x, 4), "y": round(y, 4), "scale": round(ww2 / w, 4)}
            if i > 0:
                kk["ease"] = "linear" if i < len(path) - 1 else "out"
            keys.append(kk)
        L["keys"] = keys
    return L


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


def staged(set_, people=(), extra_top=()):
    out = [plate(set_)] + sorted(people, key=lambda L: -L["_depth"]) + list(extra_top)
    for L in out:
        L.pop("_depth", None)
    return out


def card(svg_body, w=900, h=150):
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {w} {h}'><rect x='5' y='5' width='{w-10}' height='{h-10}' rx='30' "
            f"fill='#f6efe2' stroke='#1a1410' stroke-width='6'/>{svg_body}</svg>")


def stamp(word, color="#d9534f", w=520):
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {w} 170'><rect x='10' y='10' width='{w-20}' height='150' rx='18' "
            f"fill='none' stroke='{color}' stroke-width='14'/><text x='{w/2}' y='128' text-anchor='middle' font-size='118' "
            f"fill='{color}' {AN}>{word}</text></svg>")


def label(t, color, w=620, size=62):
    return card(f"<text x='{w/2}' y='92' text-anchor='middle' font-size='{size}' fill='{color}' {AN}>{t}</text>", w, 140)


def eye(cx, cy):
    return (f"<ellipse cx='{cx}' cy='{cy}' rx='70' ry='44' fill='#ffffff' stroke='#1a1410' stroke-width='6'/>"
            f"<circle cx='{cx}' cy='{cy}' r='26' fill='#34425c'/><circle cx='{cx}' cy='{cy}' r='12' fill='#0b0f12'/>")


def cones(cx, cy, cols):
    return "".join(f"<circle cx='{cx + (i - (len(cols) - 1) / 2) * 92}' cy='{cy}' r='36' fill='{c}' stroke='#1a1410' stroke-width='6'/>"
                   for i, c in enumerate(cols))


# colour cones: you 3, a bull 2 (no red-sensitive one)
CONES = card(
    "<text x='450' y='72' text-anchor='middle' font-size='42' fill='#1a1410' " + F + ">COLOUR CONES</text>"
    + eye(150, 170) + "<text x='150' y='265' text-anchor='middle' font-size='48' fill='#34425c' " + AN + ">YOU</text>"
    + cones(560, 170, ["#d23a35", "#46965a", "#2f6fd6"])
    + "<line x1='60' y1='300' x2='840' y2='300' stroke='#d8cdb4' stroke-width='5'/>"
    + eye(150, 380) + "<text x='150' y='475' text-anchor='middle' font-size='48' fill='#34425c' " + AN + ">BULL</text>"
    + cones(514, 380, ["#9aa35a", "#2f6fd6"])
    + "<circle cx='746' cy='380' r='36' fill='none' stroke='#9aa3ad' stroke-width='6' stroke-dasharray='12 10'/>"
    + "<line x1='716' y1='350' x2='776' y2='410' stroke='#d9534f' stroke-width='10'/><line x1='776' y1='350' x2='716' y2='410' stroke='#d9534f' stroke-width='10'/>"
    + "<text x='560' y='265' text-anchor='middle' font-size='56' fill='#1a1410' " + AN + ">3</text>"
    + "<text x='560' y='475' text-anchor='middle' font-size='56' fill='#d9534f' " + AN + ">2</text>", 900, 520)


def cape(x, y, col, w=230, h=170):
    return (f"<path d='M{x},{y} L{x+w},{y} Q{x+w-10},{y+h*0.6} {x+w+14},{y+h} Q{x+w*0.5},{y+h-26} {x-6},{y+h} "
            f"Q{x+14},{y+h*0.5} {x},{y} Z' fill='{col}' stroke='#1a1410' stroke-width='6'/>"
            f"<rect x='{x-12}' y='{y-14}' width='{w+24}' height='18' rx='9' fill='#8a6142' stroke='#1a1410' stroke-width='5'/>")


# what a bull sees: the same cape, bright vs dull
SEES = card(
    cape(70, 110, "#d23a35") + cape(500, 110, "#7b7454")
    + "<text x='185' y='370' text-anchor='middle' font-size='54' fill='#34425c' " + AN + ">YOU SEE</text>"
    + "<text x='615' y='370' text-anchor='middle' font-size='54' fill='#34425c' " + AN + ">A BULL SEES*</text>"
    + "<path d='M340,190 L450,190' stroke='#1a1410' stroke-width='10'/><polygon points='470,190 440,172 440,208' fill='#1a1410'/>"
    + "<text x='450' y='425' text-anchor='middle' font-size='28' fill='#34425c' " + F + ">*roughly: red looks dull, not bright</text>", 900, 450)

# the 2007 TV test card
TEST = card(
    "<rect x='40' y='40' width='200' height='150' rx='24' fill='#34425c' stroke='#1a1410' stroke-width='6'/>"
    "<rect x='62' y='60' width='156' height='108' rx='14' fill='#6fc3c0'/>"
    "<line x1='100' y1='40' x2='70' y2='5' stroke='#1a1410' stroke-width='6'/><line x1='180' y1='40' x2='210' y2='5' stroke='#1a1410' stroke-width='6'/>"
    "<text x='520' y='118' text-anchor='middle' font-size='96' fill='#d9534f' " + AN + ">2007</text>"
    "<text x='520' y='172' text-anchor='middle' font-size='38' fill='#1a1410' " + F + ">THE TV TEST</text>", 800, 220)

# the matador's two capes
CAPES = card(
    "<text x='450' y='70' text-anchor='middle' font-size='40' fill='#1a1410' " + F + ">THE TWO CAPES</text>"
    + cape(80, 130, "#d9539a", 300, 220)
    + "<path d='M94,144 L366,144 L360,330 L100,330 Z' fill='none'/>"
    + "<rect x='230' y='130' width='150' height='18' fill='#f2b04a'/>"
    + cape(540, 150, "#c41e1a", 220, 180)
    + "<text x='230' y='420' text-anchor='middle' font-size='46' fill='#34425c' " + AN + ">1ST: PINK + GOLD</text>"
    + "<text x='650' y='420' text-anchor='middle' font-size='46' fill='#34425c' " + AN + ">LAST: RED</text>", 900, 460)
CHECK = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 120 120'><circle cx='60' cy='60' r='54' fill='#46965a' stroke='#1a1410' "
         "stroke-width='6'/><path d='M32,62 L52,82 L90,40' fill='none' stroke='#f6efe2' stroke-width='14' stroke-linecap='round'/></svg>")

S = []
# 1. hook (arena mid): MYTH stamp at frame 0, a calm bull in the ring, Ved arms crossed in front, the man in red behind him
S.append({"say": "Bulls go wild when they see *red*? Total myth.", "caption_y": 0.32,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.2, "zoom": 1.06, "focus": [0.5, 0.52]}]},
          "layers": staged("arena_mid",
                           people=[prop("arena_mid", "bull_stand", 1.6, 4.6, flip=True),
                                   person("arena_mid", "rojo", -1.3, 2.4, [["idle", 0], ["shrug", 2.2]]),
                                   ved("arena_mid", 0.3, -0.6, [["crossed", 0], ["deadpan", 2.3]])],
                           extra_top=[txt("BULLS HATE *RED*?", 0.205, 104, enter="none"),
                                      {"type": "image", "svg": stamp("MYTH"), "x": 0.5, "y": 0.1, "w": 0.42, "rotate": -6,
                                       "enter": "none", "keys": [{"t": 0, "scale": 1.0}, {"t": 2.3, "scale": 1.0}, {"t": 2.55, "scale": 1.15, "ease": "back"}]}])})
# 2. close-up + cone chart
S.append({"say": "Bulls are red-green colour blind. Two kinds of colour cones. You have *three*.",
          "transition": "zoom", "caption_y": 0.64,
          "layers": [plate("arena_mid", blur=10, keys=[{"t": 0, "scale": 1.35}, {"t": 5, "scale": 1.42}]),
                     close_ved([["explain", 0], ["point", 2.4], ["smirk", 4.2]]),
                     {"type": "image", "svg": CONES, "x": 0.5, "y": 0.22, "w": 0.74, "enter": "slide_up", "at": 0.2, "sfx": "pop"}]})
# 3. what a bull sees (low angle, blurred) + swatches
S.append({"say": "That bright red cape? To a bull, it's a dull, muddy blob.",
          "transition": "slide_left", "caption_y": 0.62,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.6, "zoom": 1.06, "focus": [0.5, 0.5]}]},
          "layers": [plate("arena_low", blur=6),
                     prop("arena_low", "bull_stand", 0.0, 6.2),
                     {"type": "image", "svg": SEES, "x": 0.5, "y": 0.24, "w": 0.82, "enter": "pop", "at": 0.3, "sfx": "pop"}]})
# 4. arena wide: the 2007 TV test
S.append({"say": "In 2007, MythBusters put it to the test.", "transition": "slide_left", "caption_y": 0.5,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.55]}, {"t": 2.8, "zoom": 1.06, "focus": [0.5, 0.56]}]},
          "layers": staged("arena_wide",
                           people=[prop("arena_wide", "bull_stand", 2.2, 7.5, flip=True),
                                   person("arena_wide", "dusty", -2.5, 4.0, [["wave", 0], ["idle", 1.6]]),
                                   ved("arena_wide", -0.4, 0.2, [["welcome", 0], ["point", 1.4]],
                                       walk=[(0, -3.6, -0.2), (1.2, -0.4, 0.2)])],
                           extra_top=[{"type": "image", "svg": TEST, "x": 0.5, "y": 0.17, "w": 0.66, "enter": "drop", "at": 0.3, "sfx": "pop"}])})
# 5. arena mid: three still flags, the bull charges each one the same
fl = [("flag_red", -1.9, 5.0), ("flag_blue", -0.2, 5.6), ("flag_white", 1.5, 5.0)]
S.append({"say": "Red, blue and white flags, standing still. The bull charged them *all the same*.",
          "transition": "cut", "caption_y": 0.66,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 5.0, "zoom": 1.08, "focus": [0.5, 0.48]}]},
          "layers": staged("arena_mid",
                           people=[prop("arena_mid", n, x, y, at=0.15 + i * 0.45, enter="pop", sfx="pop",
                                        keys=[{"t": 0, "rot": 0}, {"t": 2.6 + i * 0.7 - 0.15 - i * 0.45, "rot": 0},
                                              {"t": 2.75 + i * 0.7 - 0.15 - i * 0.45, "rot": -12, "ease": "out"},
                                              {"t": 3.3 + i * 0.7 - 0.15 - i * 0.45, "rot": 0, "ease": "bounce"}])
                                   for i, (n, x, y) in enumerate(fl)]
                           + [prop("arena_mid", "bull_charge", 4.5, 5.6, flip=True, at=2.0, sfx="whoosh",
                                   path=[(0, 4.5, 5.6), (0.7, 1.5, 5.3), (1.4, -0.2, 5.9), (2.1, -1.9, 5.3), (2.9, -4.6, 5.2)])],
                           extra_top=[txt("ALL *STILL*", 0.13, 110, enter="pop", at=0.2, sfx="pop"),
                                      {"type": "image", "svg": label("RED = BLUE = WHITE", "#34425c", 820, 60), "x": 0.5, "y": 0.24,
                                       "w": 0.7, "enter": "zoom", "at": 3.9, "sfx": "ding"}])})
# 6. arena wide: the man in red stands still, two cowboys move around
S.append({"say": "Then a man in all red stood *perfectly still*, while two cowboys moved around.",
          "transition": "slide_left", "caption_y": 0.62,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.55]}, {"t": 4.6, "zoom": 1.07, "focus": [0.5, 0.56]}]},
          "layers": staged("arena_wide",
                           people=[person("arena_wide", "rojo", 0.0, 4.6, [["idle", 0]], acting_none=True),
                                   person("arena_wide", "dusty", -3.0, 6.5, [["wave", 0], ["point", 2.0]],
                                          walk=[(0, -3.0, 6.5), (2.0, -1.6, 8.0), (4.0, -3.4, 7.2)]),
                                   person("arena_wide", "jo", 3.2, 3.6, [["wave", 0], ["cheer", 2.4]],
                                          walk=[(0, 3.2, 3.6), (2.2, 2.4, 6.4), (4.2, 3.6, 5.0)]),
                                   prop("arena_wide", "bull_stand", 3.6, 9.6, flip=True)],
                           extra_top=[txt("RED = *FROZEN*", 0.15, 104, enter="pop", at=0.6, sfx="pop"),
                                      txt("COWBOYS = *MOVING*", 0.24, 92, enter="pop", at=3.0, sfx="pop")])})
# 7. arena low: the bull thunders past the man in red, after the cowboys
S.append({"say": "The bull chased the cowboys. And *ignored* the man in red.",
          "transition": "cut", "caption_y": 0.62,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.55]}, {"t": 0.5, "zoom": 1.0, "focus": [0.5, 0.55]}],
                     "shake": [0.6, 0.6]},
          "layers": staged("arena_low",
                           people=[person("arena_low", "rojo", -0.2, 7.0, [["idle", 0], ["surprised", 2.6]]),
                                   person("arena_low", "dusty", 2.6, 8.6, [["surprised", 0]],
                                          walk=[(0, 2.6, 8.6), (1.2, 4.6, 9.2)]),
                                   person("arena_low", "jo", 1.8, 9.6, [["surprised", 0]], hops=[[0.4, 0.15, 0.5]],
                                          walk=[(0, 1.8, 9.6), (1.4, 3.9, 10.2)]),
                                   prop("arena_low", "bull_charge", -3.4, 5.6, sfx="whoosh",
                                        path=[(0, -3.4, 5.6), (1.6, 3.2, 7.0)])],
                           extra_top=[{"type": "image", "svg": stamp("IGNORED", "#d9534f", 640), "x": 0.4, "y": 0.27, "w": 0.46,
                                       "rotate": -6, "enter": "zoom", "at": 2.4, "sfx": "boom"}])})
# 8. comic beat: silent reaction cut-away
S.append({"dur": 1.8, "transition": "cut", "captions": False,
          "layers": [plate("arena_low", blur=10, keys=[{"t": 0, "scale": 1.35}]), dict(close_ved([["deadpan", 0]]), acting="none")],
          "beat": {"kind": "deadpan", "at": 0.1, "dur": 1.6,
                   "text": "full red fit, zero movement.\nthe bull: *who?*", "text_y": 0.18}})
# 9. arena mid: movement is the trigger - a cowboy flicks a cape, the bull turns and charges it
S.append({"say": "What sets it off? *Movement*. A cape flicking in its face.",
          "transition": "slide_left", "caption_y": 0.7,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.0, "zoom": 1.08, "focus": [0.46, 0.5]}]},
          "layers": staged("arena_mid",
                           people=[person("arena_mid", "jo", -0.4, 4.4, [["explain", 0], ["wave", 1.2], ["surprised", 3.2]],
                                          hops=[[3.3, 0.12, 0.45]]),
                                   prop("arena_mid", "flag_red", 0.05, 4.3, at=0.2, enter="pop", sfx="pop",
                                        keys=[{"t": 0, "rot": 0}] + [{"t": 1.0 + k * 0.25, "rot": (-14 if k % 2 == 0 else 12)} for k in range(8)]
                                        + [{"t": 3.2, "rot": 0}]),
                                   prop("arena_mid", "bull_charge", 4.0, 5.0, flip=True, at=1.6, sfx="whoosh",
                                        path=[(0, 4.2, 5.0), (1.6, 1.5, 4.6)]),
                                   ved("arena_mid", -0.4, 1.0, [["point", 0], ["explain", 2.4]])],
                           extra_top=[txt("IT'S THE *MOVE*", 0.14, 116, enter="pop", at=1.0, sfx="pop")])})
# 10. close-up + the two capes
S.append({"say": "Even the matador's first cape is pink and gold. Bulls charge it *just as hard*.",
          "transition": "zoom", "caption_y": 0.64,
          "layers": [plate("arena_wide", blur=10, keys=[{"t": 0, "scale": 1.35}, {"t": 5, "scale": 1.42}]),
                     close_ved([["explain", 0], ["point", 1.8], ["think", 3.8]]),
                     {"type": "image", "svg": CAPES, "x": 0.5, "y": 0.22, "w": 0.8, "enter": "slide_up", "at": 0.2, "sfx": "pop"},
                     {"type": "image", "svg": CHECK, "x": 0.25, "y": 0.1, "w": 0.1, "enter": "pop", "at": 3.4, "sfx": "ding"}]})
# 11. payoff: wide, Ved and the man in red, the bull calm again
S.append({"say": "Red is for the crowd. The bull only cares what *moves*.", "transition": "cut", "caption_y": 0.62,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.55]}, {"t": 3.4, "zoom": 1.06, "focus": [0.5, 0.56]}]},
          "layers": staged("arena_wide",
                           people=[prop("arena_wide", "bull_stand", -2.6, 7.8),
                                   person("arena_wide", "rojo", 1.6, 3.4, [["idle", 0], ["shrug", 1.4]]),
                                   ved("arena_wide", -0.2, 0.4, [["warm", 0], ["smirk", 1.6], ["crossed", 2.6]])],
                           extra_top=[txt("IT'S NOT RED.\nIT'S *MOTION.*", 0.16, 100, enter="pop", at=1.2, sfx="ding")])})

# person() does not know acting_none; strip it and hold the pose
for sc in S:
    for L in sc["layers"]:
        if L.pop("acting_none", False):
            L["acting"] = "none"

job = {"id": ID, "title": "Do bulls really hate red? Total myth 🐂",
       "description": "Bulls are red-green colour blind, and in a 2007 TV test a bull charged red, blue and white flags alike, then "
                      "chased moving cowboys and ignored a man in red standing still. It's the movement, not the colour.\n\n"
                      "Sources: Live Science, 'Why Do Bulls Charge When They See Red?'; Mental Floss, 'What Really Happens If You Wear "
                      "Red in Front of a Bull?'; Ripley's, 'Seeing Red: Bulls Don't Care About Red'.",
       "tags": ["bulls", "colour blind", "myth busting", "animal facts", "mythbusters", "science explained", "bull red cape", "vision"],
       "hashtags": ["#animals", "#mythbusting"],
       "meta": {"format": "myth-bust", "topic": "the bulls-hate-red myth (dichromat vision, movement triggers the charge)",
                "hook": "myth-bust", "idea_source": "backlog", "characters": ["ved", "extra"],
                "sources": ["https://www.livescience.com/33700-bulls-charge-red.html",
                            "https://www.mentalfloss.com/article/28488/what-really-happens-if-you-wear-red-front-bull",
                            "https://www.ripleys.com/stories/bulls-seeing-red",
                            "https://scienceblog.com/m-bulls-arent-enraged-by-red-theyre-red-green-colour-blind-and-its-the-movement-of-the-cape-that-triggers-the-charge/"],
                "humour": {"trend": "timeless dry reaction ('the bull: who?' card); nothing current fit naturally",
                           "beat": "deadpan", "scene": 7}},
       "privacy": "public", "speaker": "ved", "assets_script": J + "assets.py", "scenes": S}
json.dump(job, open(J + "job.json", "w"), indent=1, ensure_ascii=False)
print("scenes", len(S))
