"""2026-11-11-a: "All 8 billion humans fit in a sugar cube" (scale-shock). 2D Ved + townspeople in a sunny cafe terrace
(a hero sugar cube on a bistro table) and inside a football stadium (the atom: a marble nucleus on the centre spot,
electrons out in the stands). Props are Blender cut-outs. Run after the assets exist: python jobs/2026-11-11-a/build_job.py
"""
import json, os, sys
sys.path.insert(0, os.getcwd())
from autopilot.stage import Stage

ID = "2026-11-11-a"
J = f"jobs/{ID}/"
A = J + "assets/"
PV = "/tmp/claude-0/-home-claude-shorts-autopilot/60b13ca2-ebd8-5fb4-88eb-1278bdf271fc/scratchpad/pv/"
SRC = A if os.path.exists(A + "nucleus.png") else PV
ST = {n: Stage(SRC + f"plate_{n}.json") for n in ("cafe_wide", "cafe_mid", "stadium_pitch")}
TX, TY = 0.55, 0.4

OUT = {   # same people, same outfits in every shot
    "kofi": {"skin": "#6b4430", "hat": ["straw", "#e6c27a"], "top": ["#f2b04a", "tshirt"], "bottom": ["#34425c", "shorts"], "build": "slim"},
    "mei": {"skin": "#f0c8a8", "hair": ["#1d1712", "long"], "hat": ["beret", "#d9534f"], "top": ["#6fc3c0", "shirt"],
            "bottom": ["#34425c", "trousers"]},
    "nani": {"skin": "#a86f4c", "build": "round", "hair": ["#d8d4cc", "bun"], "top": ["#7c2533", "dress"], "necklace": "#f2b04a",
             "bag": "#8a5a3c"},
    "waiter": {"skin": "#c98e62", "hair": ["#1d1712", "short"], "top": ["#f6efe2", "shirt"], "bottom": ["#1a1410", "trousers"],
               "apron": "#1a1410", "tie": "#d9534f"},
}
F = "font-family='Poppins, DejaVu Sans, sans-serif' font-weight='800'"
AN = "font-family='Anton, DejaVu Sans, sans-serif'"


def plate(name, blur=0, **k):
    return {"type": "image", "path": A + f"plate_{name}.png", "x": 0.5, "y": 0.5, "w": 1.0, "enter": "none", "blur": blur, **k}


def fg(name):
    return {"type": "image", "path": A + f"fg_{name}.png", "x": 0.5, "y": 0.5, "w": 1.0, "enter": "none"}


def sprite(name, x, y, w, **k):
    return {"type": "image", "path": A + name + ".png", "x": x, "y": y, "w": w, "enter": k.pop("enter", "none"), **k}


def txt(t, y, size=96, **k):
    return {"type": "text", "text": t, "font": "display", "x": 0.5, "y": y, "size": size, "max_w": 0.88,
            "stroke": "#0b0f12", "stroke_width": 7, **k}


def card(svg, y, w=0.84, at=0.3, **k):
    return {"type": "image", "svg": svg, "w": w, "x": 0.5, "y": y, "enter": "pop", "at": at, "sfx": "pop", **k}


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


def staged(set_, people=(), extra_top=(), fg_layer=False, table_y=TY):
    """plate, people behind the table (far to near), the table (fg), people in front, then props/text."""
    ppl = sorted(people, key=lambda L: -L["_depth"])
    behind = [L for L in ppl if L["_depth"] > table_y]
    front = [L for L in ppl if L["_depth"] <= table_y]
    out = [plate(set_)] + behind + ([fg(set_)] if fg_layer else []) + front + list(extra_top)
    for L in out:
        L.pop("_depth", None)
    return out


def orbit(cx, cy, rx, ry, w, at=0.0, dur=3.0, phase=0.0, n=12, turns=1.0, **k):
    """An electron cut-out circling an ellipse (props may loop, characters never do)."""
    import math
    keys = []
    for i in range(n + 1):
        a = phase + turns * 2 * math.pi * i / n
        keys.append({"t": dur * i / n, "x": cx + rx * math.cos(a), "y": cy + ry * math.sin(a), "ease": "linear"})
    return sprite("electron", keys[0]["x"], keys[0]["y"], w, at=at, enter=k.pop("enter", "pop"), keys=keys, **k)


cw, cm, sp = ST["cafe_wide"], ST["cafe_mid"], ST["stadium_pitch"]
cube_w = cw.point(TX, TY - 0.12, 0.8)
cube_m = cm.point(TX, TY - 0.12, 0.8)

S = []
# 1. HOOK (wide cafe): the number on screen at frame 0
S.append({"say": "Every human alive, all *eight billion* of us, fits in *one sugar cube*.",
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.5, "zoom": 1.06, "focus": [0.5, 0.5]}]},
          "caption_y": 0.36,
          "layers": staged("cafe_wide",
                           [person("cafe_wide", "mei", -2.0, -2.2, [["idle", 0], ["surprised", 2.6]]),
                            person("cafe_wide", "kofi", 1.5, -2.4, [["point", 0], ["surprised", 2.9]], hops=[[3.0, 0.03, 0.45]]),
                            person("cafe_wide", "waiter", 1.3, 1.2, [["hold", 0], ["shrug", 3.2]]),
                            ved("cafe_wide", -0.5, -4.6, [["welcome", 0], ["point", 2.6]])],
                           [txt("8,000,000,000", 0.1, 112, enter="none", color="accent"),
                            txt("PEOPLE", 0.165, 72, enter="none"),
                            txt("= *1 SUGAR CUBE*", 0.24, 96, enter="pop", at=2.6, sfx="pop"),
                            {"type": "shape", "shape": "ring", "x": cube_w[0], "y": cube_w[1], "w": 0.07, "color": "accent",
                             "stroke_width": 6, "enter": "pop", "at": 3.0, "loop": "pulse"}],
                           fg_layer=True)})
# 2. close-up: you are mostly nothing
S.append({"say": "Sounds fake. But you are mostly *nothing*.", "transition": "cut", "caption_y": 0.64,
          "layers": [plate("cafe_table", blur=8, keys=[{"t": 0, "scale": 1.3}, {"t": 3.2, "scale": 1.36}]),
                     close_ved([["smirk", 0], ["serious", 1.2]]),
                     txt("MOSTLY *NOTHING*", 0.14, 108, enter="pop", at=1.2, sfx="pop")]})
# 3. stadium wide: one atom = a stadium
S.append({"say": "Blow one atom up to a *football stadium*.", "transition": "slide_left",
          "camera": {"keys": [{"t": 0, "zoom": 1.12, "focus": [0.5, 0.55]}, {"t": 3.6, "zoom": 1.0, "focus": [0.5, 0.5]}]},
          "caption_y": 0.7,
          "layers": [plate("stadium_wide"),
                     txt("1 ATOM", 0.1, 110, enter="pop", at=0.1, sfx="pop"),
                     txt("= *A STADIUM*", 0.17, 96, enter="pop", at=1.3, sfx="pop"),
                     orbit(0.5, 0.42, 0.42, 0.06, 0.05, at=1.0, dur=3.0, phase=0.3),
                     orbit(0.5, 0.42, 0.38, 0.05, 0.04, at=1.4, dur=3.4, phase=2.6)]})
# 4. the marble on the centre spot
S.append({"say": "The nucleus? A *marble* on the centre spot. That's almost all the weight.", "transition": "zoom", "sfx": "whoosh",
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.5, "zoom": 1.08, "focus": [0.5, 0.52]}]},
          "caption_y": 0.74,
          "layers": [plate("stadium_marble"),
                     txt("NUCLEUS", 0.12, 110, enter="pop", at=0.6, sfx="pop"),
                     txt("= A *MARBLE*", 0.19, 90, enter="pop", at=1.4, sfx="pop"),
                     sprite("nucleus", 0.84, 0.36, 0.13, enter="pop", at=2.4, sfx="pop",
                            keys=[{"t": 0, "rot": -12}, {"t": 2.0, "rot": 12}]),
                     txt("~99.9% OF THE *MASS*", 0.26, 64, enter="pop", at=2.6)]})
# 5. Ved on the pitch: electrons in the back rows, empty in between
S.append({"say": "Electrons buzz in the *back rows*. Everything in between? *Empty*.",
          "transition": "cut", "caption_y": 0.2,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 5.0, "zoom": 1.06, "focus": [0.5, 0.5]}]},
          "layers": staged("stadium_pitch",
                           [ved("stadium_pitch", -3.4, -1.3, [["explain", 0], ["point", 0.9], ["shrug", 2.8]],
                                walk=[(0, -3.4, -3.4), (1.0, -3.4, -1.3)])],
                           [orbit(0.5, 0.2, 0.44, 0.035, 0.05, at=0.6, dur=2.6, phase=0.0, turns=1.5),
                            orbit(0.5, 0.24, 0.4, 0.03, 0.045, at=0.9, dur=3.0, phase=3.0, turns=1.5),
                            orbit(0.5, 0.17, 0.46, 0.03, 0.04, at=1.2, dur=2.8, phase=1.5, turns=1.5),
                            {"type": "shape", "shape": "ring", "x": sp.point(0, 0, 0.12)[0], "y": sp.point(0, 0, 0.12)[1],
                             "w": 0.05, "color": "accent", "stroke_width": 6, "enter": "pop", "at": 0.3, "loop": "pulse"},
                            txt("*EMPTY*", 0.33, 130, enter="zoom", at=2.9, sfx="whoosh", color="#f6efe2")])})
# 6. infographic: 99.9999999999% empty
emp = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 900 560'><rect width='900' height='560' rx='34' fill='#f6efe2'/>"
       "<rect width='900' height='560' rx='34' fill='none' stroke='#1a1410' stroke-width='6'/>"
       f"<text x='450' y='80' text-anchor='middle' font-size='44' fill='#1a1410' {F}>WHAT AN ATOM IS MADE OF</text>"
       "<circle cx='230' cy='300' r='150' fill='#dff1ff' stroke='#34425c' stroke-width='4' stroke-dasharray='14 10'/>"
       "<circle cx='230' cy='300' r='4' fill='#d9534f'/>"
       "<circle cx='370' cy='255' r='9' fill='#1fa8ff'/><circle cx='120' cy='398' r='9' fill='#1fa8ff'/>"
       "<line x1='236' y1='296' x2='330' y2='180' stroke='#1a1410' stroke-width='3'/>"
       f"<text x='336' y='172' font-size='26' fill='#1a1410' {F}>nucleus</text>"
       f"<text x='640' y='240' text-anchor='middle' font-size='46' fill='#d98a1a' {AN}>99.9999999999%</text>"
       f"<text x='660' y='300' text-anchor='middle' font-size='44' fill='#1a1410' {F}>EMPTY SPACE</text>"
       f"<text x='660' y='380' text-anchor='middle' font-size='28' fill='#5a4636' {F}>(not to scale:</text>"
       f"<text x='660' y='418' text-anchor='middle' font-size='28' fill='#5a4636' {F}>the dot would be invisible)</text>"
       f"<text x='450' y='520' text-anchor='middle' font-size='34' fill='#1a1410' {F}>YOU. YOUR PHONE. THIS CHAIR.</text></svg>")
S.append({"say": "You, your phone, your chair: almost all *empty space*.", "transition": "slide_up", "caption_y": 0.64,
          "layers": [plate("stadium_wide", blur=8, keys=[{"t": 0, "scale": 1.15}, {"t": 4, "scale": 1.2}]),
                     card(emp, 0.29, w=0.9, at=0.15),
                     sprite("electron", 0.2, 0.52, 0.06, enter="pop", at=1.0, loop="pulse"),
                     sprite("electron", 0.8, 0.5, 0.05, enter="pop", at=1.3, loop="pulse")]})
# 7. comic beat (reaction cut-away): "Always Has Been" format (rising again on Imgflip this week, Nov 2026)
S.append({"dur": 1.9, "transition": "cut", "captions": False,
          "layers": [plate("stadium_pitch", blur=10, keys=[{"t": 0, "scale": 1.35}]), dict(close_ved([["side_eye", 0]]), acting="none")],
          "beat": {"kind": "side_eye", "at": 0.1, "dur": 1.7, "text": "Wait, it's all empty space? *Always has been.*",
                   "text_y": 0.18}})
# 8. cafe mid: squeeze the space out of everyone; the townspeople shrink into the cube
def shrink(L, at, dur=0.7):
    L["keys"] = [{"t": 0, "x": L["x"], "y": L["y"], "scale": 1.0}, {"t": at, "x": L["x"], "y": L["y"], "scale": 1.0},
                 {"t": at + dur, "x": cube_m[0], "y": cube_m[1], "scale": 0.02, "ease": "in"}]
    L["ground"] = False
    return L


S.append({"say": "Squeeze that space out of *every person on Earth*.", "transition": "slide_left",
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.0, "zoom": 1.08, "focus": [0.5, 0.55]}]},
          "caption_y": 0.2,
          "layers": staged("cafe_mid",
                           [shrink(person("cafe_mid", "mei", -0.9, 1.4, [["surprised", 0]]), 1.4),
                            shrink(person("cafe_mid", "kofi", 1.4, 1.1, [["happy", 0], ["surprised", 1.0]]), 1.8),
                            shrink(person("cafe_mid", "nani", -0.5, 2.6, [["idle", 0], ["surprised", 1.2]]), 2.2),
                            shrink(person("cafe_mid", "waiter", 1.0, 2.9, [["hold", 0], ["shrug", 1.4]]), 2.5),
                            ved("cafe_mid", -0.6, -0.4, [["explain", 0], ["point", 1.3]])],
                           [{"type": "shape", "shape": "burst", "x": cube_m[0], "y": cube_m[1], "w": 0.12, "color": "accent",
                             "enter": "pop", "at": 2.2, "sfx": "pop", "until": 3.4, "exit": "fade"}],
                           fg_layer=True)})
# 9. close on the cube: all of humanity
S.append({"say": "All of humanity: about one *sugar cube*.", "transition": "cut", "sfx": "ding",
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.5, "zoom": 1.1, "focus": [0.5, 0.56]}]},
          "caption_y": 0.74,
          "layers": [plate("cafe_table"),
                     {"type": "counter", "from": 0, "to": 8000000000, "count_dur": 1.2, "x": 0.5, "y": 0.12,
                      "size": 110, "color": "accent", "stroke": "#0b0f12", "stroke_width": 7, "enter": "none"},
                     txt("HUMANS IN HERE", 0.19, 72, enter="pop", at=0.6),
                     {"type": "shape", "shape": "arrow", "x": 0.5, "y": 0.32, "w": 0.12, "rotate": 90, "color": "accent",
                      "enter": "pop", "at": 1.2, "loop": "bob"}]})
# 10. it still weighs as much as all of us (cafe mid, the cube on the table)
S.append({"say": "And it still weighs as much as all of us.", "transition": "cut", "caption_y": 0.3,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.4, "zoom": 1.05, "focus": [0.5, 0.55]}]},
          "layers": staged("cafe_mid",
                           [ved("cafe_mid", -0.6, -0.4, [["serious", 0], ["point", 1.6]])],
                           [txt("WEIGHT:", 0.12, 70, enter="pop", at=0.9, sfx="pop"),
                            txt("*ALL OF US*", 0.19, 96, enter="pop", at=1.4)],
                           fg_layer=True)})
# 11. crash: hundreds of millions of tonnes (crushed table)
S.append({"say": "*Hundreds of millions* of tonnes. Sorry, table.", "transition": "flash", "sfx": "boom",
          "camera": {"keys": [{"t": 0, "zoom": 1.08, "focus": [0.5, 0.55]}, {"t": 3.0, "zoom": 1.0, "focus": [0.5, 0.5]}], "shake": [0, 0.6]},
          "caption_y": 0.3,
          "layers": staged("cafe_crushed",
                           [ved("cafe_mid", -0.6, -0.4, [["surprised", 0], ["side_eye", 1.9]], hops=[[0.05, 0.05, 0.5]])],
                           [txt("100s OF MILLIONS", 0.12, 96, enter="pop", at=0.2, color="accent"),
                            txt("OF TONNES", 0.19, 80, enter="pop", at=0.5)])})
# 12. close payoff: why you don't fall through your chair
S.append({"say": "So why don't you fall through your chair? Your electrons *push* the chair's away. That push is what you call *touch*.",
          "transition": "cut", "caption_y": 0.64,
          "layers": [plate("cafe_table", blur=10, keys=[{"t": 0, "scale": 1.35}, {"t": 7.0, "scale": 1.45}]),
                     close_ved([["think", 0], ["explain", 2.0], ["point", 3.8], ["smirk", 5.4]]),
                     sprite("electron", 0.3, 0.2, 0.08, enter="pop", at=2.4, sfx="pop",
                            keys=[{"t": 0, "x": 0.4}, {"t": 0.6, "x": 0.3, "ease": "back"}]),
                     sprite("electron", 0.7, 0.2, 0.08, enter="pop", at=2.4,
                            keys=[{"t": 0, "x": 0.6}, {"t": 0.6, "x": 0.7, "ease": "back"}]),
                     txt("PUSH", 0.13, 90, enter="pop", at=2.8, color="accent"),
                     txt("= *TOUCH*", 0.28, 110, enter="pop", at=4.4, sfx="ding")]})

SRCS = ["https://www.syfy.com/syfy-wire/follow-up-the-volume-of-humanity-if-all-the-space-in-our-atoms-is-removed",
        "https://www.fnal.gov/pub/today/archive/archive_2013/today13-12-06_NutshellReadMore.html",
        "https://openstax.org/books/university-physics-volume-3/pages/10-1-properties-of-nuclei",
        "https://bigthink.com/starts-with-a-bang/matter-mostly-empty-space/",
        "https://zmescience.com/ecology/world-problems/world-human-population-mass-287-million-tonnes-432432"]
job = {"id": ID, "title": "All 8 billion humans fit in a sugar cube 🧊",
       "description": "Atoms are almost entirely empty space: blow one up to a football stadium and the nucleus is a marble on "
                      "the centre spot. Squeeze that space out of every person on Earth and humanity shrinks to roughly a sugar "
                      "cube (a few cubic centimetres), which would still weigh hundreds of millions of tonnes. You never fall "
                      "through your chair because electrons push each other away.\n\nSources: " + " ; ".join(SRCS),
       "tags": ["atoms", "empty space", "physics", "sugar cube", "nucleus", "electrons", "neutron star", "science explained", "facts"],
       "hashtags": ["#physics", "#science"],
       "meta": {"format": "scale-shock", "topic": "atoms are mostly empty space: all of humanity compressed fits in a sugar cube",
                "hook": "number-shock", "idea_source": "search (classic physics scale fact; backlog atoms/grain-of-sand idea as a cousin)",
                "characters": ["ved", "extra"], "sources": SRCS,
                "humour": {"trend": "'Always Has Been' (astronaut format, rising again on Imgflip this week, Nov 2026), as a text card",
                           "beat": "side_eye", "scene": 6}},
       "privacy": "public", "speaker": "ved", "assets_script": J + "assets.py", "scenes": S}
json.dump(job, open(J + "job.json", "w"), indent=1, ensure_ascii=False)
print("scenes", len(S), "using", SRC)
