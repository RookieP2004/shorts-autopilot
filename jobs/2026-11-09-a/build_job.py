"""2026-11-09-a: "How heavy is a cloud?" (scale-shock) on a sunny hilltop meadow with a giant see-saw.
2D Ved + faceless townspeople staged in depth inside Blender plates (house style of jobs/2026-11-08-m3).
Run: python jobs/2026-11-09-a/build_job.py
"""
import json, math, os, random, sys
sys.path.insert(0, os.getcwd())
from PIL import Image
from autopilot.stage import Stage

random.seed(9)
ID = "2026-11-09-a"
J = f"jobs/{ID}/"
A = J + "assets/"
PV = "/tmp/claude-0/-home-claude-shorts-autopilot/6f615ca9-d5ee-5fe2-aeba-c43ba066944a/scratchpad/pv/"
SRC = A if os.path.exists(A + "crate_air.png") else PV
ST = {n: Stage(SRC + f"plate_{n}.json") for n in ("meadow_wide", "meadow_sky", "seesaw_level", "seesaw_tipped")}

OUT = {
    "nani": {"skin": "#a86f4c", "build": "round", "hair": ["#d8d4cc", "bun"], "top": ["#6fc3c0", "dress"], "necklace": "#f2b04a",
             "bag": "#8a5a3c", "earrings": "#f2b04a"},
    "kofi": {"skin": "#6b4430", "hat": ["straw", "#e6c27a"], "top": ["#f2b04a", "tshirt"], "bottom": ["#34425c", "shorts"], "build": "slim"},
    "mei": {"skin": "#f0c8a8", "hair": ["#1d1712", "long"], "hat": ["beret", "#d9534f"], "top": ["#f6efe2", "shirt"],
            "bottom": ["#34425c", "trousers"]},
    "arjun": {"skin": "#b97a55", "hat": ["cap", "#46965a"], "top": ["#34425c", "kurta"], "bottom": ["#efe3c8", "trousers"]},
}


def aspect(name):
    im = Image.open(SRC + name + ".png")
    return im.height / im.width


def plate(name, blur=0, **k):
    return {"type": "image", "path": A + f"plate_{name}.png", "x": 0.5, "y": 0.5, "w": 1.0, "enter": "none", "blur": blur, **k}


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


def staged(set_, people=(), extra_top=()):
    out = [plate(set_)] + sorted(people, key=lambda L: -L["_depth"]) + list(extra_top)
    for L in out:
        L.pop("_depth", None)
    return out


def sit(set_, name, wx, wz, width_m, th=0.0):
    """Sprite resting on the see-saw plank at plank coordinate wx (metres from the pivot). Returns x, y(centre), w."""
    st = ST[set_]
    X = wx * math.cos(th) + 0.1 * math.sin(th)
    Z = 1.42 - wx * math.sin(th) + 0.1 * math.cos(th)
    x, y = st.point(X, 2.0, Z)
    xl, _ = st.point(X - width_m / 2, 2.0, Z)
    xr, _ = st.point(X + width_m / 2, 2.0, Z)
    w = abs(xr - xl)
    h = w * aspect(name) * 1080 / 1920
    return x, y - h / 2 + 0.006, w


FONT = "font-family='Poppins, DejaVu Sans, sans-serif' font-weight='800'"
ANTON = "font-family='Anton, DejaVu Sans, sans-serif'"
S = []

# 1. HOOK (wide meadow): the number is on screen at frame 0, arrow at the big cloud
wc = ST["meadow_wide"].point(-4, 70, 36)
S.append({"say": "This fluffy cloud weighs about *five hundred tonnes*.",
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.2, "zoom": 1.06, "focus": [0.5, 0.48]}]},
          "caption_y": 0.5,
          "layers": staged("meadow_wide",
                           [person("meadow_wide", "nani", -2.2, -3.0, [["idle", 0], ["point", 0.9]]),
                            person("meadow_wide", "kofi", -0.6, -1.0, [["idle", 0], ["surprised", 1.6]]),
                            ved("meadow_wide", 0.5, -6.5, [["point", 0], ["explain", 2.0]])],
                           [txt("THIS CLOUD WEIGHS", 0.11, 84, enter="none"),
                            txt("*500 TONNES*", 0.18, 150, enter="none"),
                            {"type": "shape", "shape": "arrow", "w": 0.16, "h": 0.05, "color": "accent", "x": wc[0] + 0.02,
                             "y": wc[1] - 0.12, "rotate": 90, "enter": "none", "loop": "bob", "loop_amp": 1.2}])})
# 2. close-up: let's do the maths
S.append({"say": "Sounds fake. So let's do the *maths*.", "transition": "cut", "caption_y": 0.64,
          "layers": [plate("meadow_wide", blur=10, keys=[{"t": 0, "scale": 1.35}, {"t": 2.4, "scale": 1.4}]),
                     close_ved([["smirk", 0], ["explain", 0.9]]),
                     txt("LET'S DO THE *MATHS*", 0.14, 104, enter="pop", at=0.8, sfx="pop")]})
# 3. sky: the cloud inside a 1 km box
sk = ST["meadow_sky"]
cube = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 600 600'>"
        "<g fill='none' stroke='#f2b04a' stroke-width='7' stroke-linejoin='round'>"
        "<rect x='60' y='160' width='380' height='380'/><path d='M60 160 L160 60 L540 60 L540 440 L440 540 M440 160 L540 60'/>"
        "<path d='M60 540 L160 440 L540 440 M160 440 L160 60' stroke-dasharray='18 14' opacity='0.7'/></g></svg>")
lbl = lambda t, x, y, at: {"type": "text", "text": t, "font": "display", "x": x, "y": y, "size": 64, "color": "accent",
                           "stroke": "#0b0f12", "stroke_width": 6, "enter": "pop", "at": at, "sfx": "pop"}
S.append({"say": "A normal puffy cloud is about *one kilometre* wide, tall and deep.", "transition": "slide_up",
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.0, "zoom": 1.08, "focus": [0.5, 0.5]}]},
          "caption_y": 0.72,
          "layers": [plate("meadow_sky"),
                     {"type": "image", "svg": cube, "w": 0.78, "x": 0.5, "y": 0.47, "enter": "zoom", "at": 0.6, "sfx": "whoosh"},
                     lbl("1 KM", 0.36, 0.67, 1.6), lbl("1 KM", 0.85, 0.5, 2.2), lbl("1 KM", 0.24, 0.29, 2.8),
                     txt("A NORMAL *CUMULUS*", 0.12, 100, enter="pop", at=0.2)]})
# 4. a billion one-metre boxes
S.append({"say": "That's a *billion* boxes of air, each one metre across.", "transition": "cut",
          "camera": {"zoom": [1.08, 1.14], "focus": [0.5, 0.48]}, "caption_y": 0.72,
          "layers": [plate("meadow_sky"),
                     {"type": "image", "svg": cube, "w": 0.78, "x": 0.5, "y": 0.47, "enter": "none", "opacity": 0.5},
                     {"type": "counter", "from": 0, "to": 1000000000, "count_dur": 1.6, "at": 0.3, "x": 0.5, "y": 0.13,
                      "size": 118, "stroke": "#0b0f12", "stroke_width": 7, "enter": "pop"},
                     txt("BOXES, *1 M3* EACH", 0.21, 84, enter="pop", at=1.9, sfx="pop")]})
# 5. half a gram per box = one marble
gram = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 900 420'><rect width='900' height='420' rx='34' fill='#f6efe2'/>"
        "<rect width='900' height='420' rx='34' fill='none' stroke='#1a1410' stroke-width='6'/>"
        f"<text x='60' y='100' font-size='50' fill='#1a1410' {FONT}>WATER IN ONE BOX</text>"
        "<rect x='60' y='140' width='230' height='230' rx='10' fill='#cfe6f2' stroke='#34425c' stroke-width='6'/>"
        "<text x='175' y='395' text-anchor='middle' font-size='30' fill='#5a4636' font-family='Poppins, DejaVu Sans, sans-serif' font-weight='800'>1 m x 1 m x 1 m</text>"
        f"<text x='600' y='250' text-anchor='middle' font-size='120' fill='#d98a1a' {ANTON}>0.5 g</text>"
        f"<text x='600' y='330' text-anchor='middle' font-size='44' fill='#1a1410' {FONT}>= ABOUT 1 MARBLE</text></svg>")
S.append({"say": "Each box holds just *half a gram* of water. About one *marble*.", "transition": "slide_left",
          "caption_y": 0.64,
          "layers": [plate("meadow_sky", blur=6, keys=[{"t": 0, "scale": 1.15}, {"t": 4, "scale": 1.2}]),
                     card(gram, 0.24, at=0.2),
                     sprite("marble", 0.29, 0.255, 0.12, enter="drop", at=1.8, sfx="pop")]})
# 6. a billion half-grams = 500 tonnes
S.append({"say": "Half a gram, a billion times, is *five hundred tonnes*.", "transition": "cut", "sfx": "boom",
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.0, "zoom": 1.1, "focus": [0.5, 0.5]}], "punch": [2.4]},
          "caption_y": 0.72,
          "layers": [plate("meadow_sky"),
                     txt("0.5 g  x  1,000,000,000", 0.12, 84, enter="pop", at=0.2, sfx="pop"),
                     {"type": "counter", "from": 0, "to": 500, "count_dur": 1.3, "at": 1.0, "x": 0.5, "y": 0.21,
                      "suffix": " TONNES", "size": 140, "color": "accent", "stroke": "#0b0f12", "stroke_width": 8, "enter": "pop"}]})
# 7. the see-saw, level: the cloud on the left, elephants on the right
cx, cy, cw = sit("seesaw_level", "cloud", -2.9, 0, 3.4)
ex, ey, ew = sit("seesaw_level", "elephant", 2.7, 0, 2.6)
crowd = lambda st, act: [person(st, "nani", -2.6, -1.4, act("nani")), person(st, "arjun", -0.9, -2.4, act("arjun")),
                         person(st, "mei", 2.2, -1.8, act("mei")), person(st, "kofi", 4.6, -0.6, act("kofi"))]
drop = lambda t0, y: [{"t": 0, "y": -0.12, "rot": -6}, {"t": 0.55, "y": y, "rot": 0, "ease": "bounce"}]
jet = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 900 170'><rect width='900' height='170' rx='30' fill='#f6efe2'/>"
       "<rect width='900' height='170' rx='30' fill='none' stroke='#1a1410' stroke-width='6'/>"
       f"<text x='450' y='78' text-anchor='middle' font-size='46' fill='#1a1410' {FONT}>FULLY LOADED JUMBO JET</text>"
       f"<text x='450' y='140' text-anchor='middle' font-size='52' fill='#d98a1a' {ANTON}>~410 t  &lt;  CLOUD 500 t</text></svg>")
S.append({"say": "That's about *a hundred elephants*. Heavier than a fully loaded *jumbo jet*.", "transition": "slide_left",
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.5, "zoom": 1.05, "focus": [0.5, 0.5]}]},
          "caption_y": 0.3,
          "layers": staged("seesaw_level",
                           crowd("seesaw_level", lambda w: [["idle", 0], ["surprised", 1.4]] if w in ("kofi", "mei") else [["idle", 0], ["point", 1.2]])
                           + [ved("seesaw_level", 0.3, -4.6, [["explain", 0], ["point", 0.9], ["warm", 3.0]])],
                           [sprite("cloud", cx, cy, cw, at=0.0, keys=drop(0, cy), sfx="pop"),
                            sprite("elephant", ex + 0.03, ey, ew, at=0.7, keys=drop(0, ey), sfx="pop"),
                            sprite("elephant", ex - 0.05, ey + 0.004, ew * 0.95, at=0.9, keys=drop(0, ey + 0.004), flip=True),
                            {"type": "text", "text": "x100", "font": "display", "x": ex, "y": ey - 0.09, "size": 84, "color": "accent",
                             "stroke": "#0b0f12", "stroke_width": 7, "enter": "pop", "at": 1.3, "sfx": "pop"},
                            txt("= *100 ELEPHANTS*", 0.12, 104, enter="pop", at=0.9),
                            card(jet, 0.215, w=0.8, at=2.6)])})
for L in S[-1]["layers"]:
    if L.get("id") == "extra" and L["rig_args"]["outfit"] is OUT["kofi"]:
        L["hops"] = [[1.45, 0.03, 0.45]]
# 8. comic beat (reaction cut-away): "They don't know" (rising this week)
S.append({"dur": 1.7, "transition": "cut", "captions": False,
          "layers": [plate("seesaw_level", blur=10, keys=[{"t": 0, "scale": 1.35}]), dict(close_ved([["surprised", 0]]), acting="none")],
          "beat": {"kind": "zoom_punch", "at": 0.1, "dur": 1.5, "zoom": 1.14, "focus": [0.5, 0.42],
                   "text": "*They don't know* it weighs 100 elephants", "text_y": 0.18}})
# 9. close: so why doesn't it fall?
S.append({"say": "So why doesn't it *fall* on us?", "transition": "cut", "caption_y": 0.64,
          "layers": [plate("meadow_sky", blur=10, keys=[{"t": 0, "scale": 1.35}, {"t": 2.2, "scale": 1.4}]),
                     close_ved([["think", 0], ["explain", 1.2]]),
                     txt("WHY DOESN'T IT *FALL?*", 0.14, 100, enter="pop", at=0.6, sfx="pop")]})
# 10. droplets thinner than a hair + rising warm air
drops = "".join(f"<circle cx='{random.randint(470, 840)}' cy='{random.randint(150, 420)}' r='{random.choice((4, 5, 6))}' fill='#6fc3c0'/>" for _ in range(40))
mag = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 900 560'><rect width='900' height='560' rx='34' fill='#f6efe2'/>"
       "<rect width='900' height='560' rx='34' fill='none' stroke='#1a1410' stroke-width='6'/>"
       f"<text x='450' y='80' text-anchor='middle' font-size='46' fill='#1a1410' {FONT}>ZOOMED IN, SAME SCALE</text>"
       "<rect x='120' y='120' width='120' height='320' rx='20' fill='#3a2a20'/>"
       f"<text x='180' y='500' text-anchor='middle' font-size='40' fill='#1a1410' {FONT}>1 HAIR</text>"
       + drops +
       f"<text x='655' y='500' text-anchor='middle' font-size='40' fill='#1a1410' {FONT}>CLOUD DROPLETS</text>"
       "<g fill='#d98a1a'><path d='M330 430 L330 210 L300 210 L350 140 L400 210 L370 210 L370 430 Z'/></g>"
       f"<text x='350' y='470' text-anchor='middle' font-size='26' fill='#d98a1a' {FONT}>WARM AIR</text></svg>")
S.append({"say": "The water is split into billions of droplets, far thinner than a *hair*. And rising *warm air* keeps pushing them up.",
          "transition": "slide_up", "caption_y": 0.66,
          "layers": [plate("meadow_sky", blur=6, keys=[{"t": 0, "scale": 1.15}, {"t": 6, "scale": 1.22}]),
                     card(mag, 0.29, w=0.86, at=0.2),
                     sprite("cloud", 0.5, 0.56, 0.3, enter="fade", at=3.6, keys=[{"t": 0, "y": 0.57}, {"t": 2.5, "y": 0.53}])]})
# 11. see-saw, tipped: the air in the same box goes down hard
th = math.radians(13)
tx, ty, tw = sit("seesaw_tipped", "cloud", -2.9, 0, 3.4, th)
ax, ay, aw = sit("seesaw_tipped", "crate_air", 2.7, 0, 2.2, th)
S.append({"say": "And the *air* in that same box? About *a million tonnes*.", "transition": "flash", "sfx": "boom",
          "camera": {"keys": [{"t": 0, "zoom": 1.1, "focus": [0.5, 0.5]}, {"t": 2.0, "zoom": 1.02, "focus": [0.5, 0.5]}], "shake": [1.6, 0.35]},
          "caption_y": 0.3,
          "layers": staged("seesaw_tipped",
                           crowd("seesaw_tipped", lambda w: [["idle", 0], ["surprised", 1.6], ["cheer", 2.4]] if w in ("kofi", "arjun") else [["idle", 0], ["surprised", 1.6]])
                           + [ved("seesaw_tipped", 0.3, -4.6, [["explain", 0], ["surprised", 1.6], ["warm", 2.8]], hops=[[1.65, 0.04, 0.45]])],
                           [sprite("cloud", tx, ty, tw),
                            sprite("crate_air", ax, ay, aw, at=1.3, keys=[{"t": 0, "y": -0.12, "rot": 8}, {"t": 0.4, "y": ay, "rot": -13, "ease": "bounce"}], sfx="pop"),
                            {"type": "text", "text": "AIR", "font": "display", "x": ax, "y": ay, "size": 80, "color": "#1a1410", "stroke": "#f6efe2",
                             "stroke_width": 5, "shadow": False, "at": 1.3, "enter": "none",
                             "keys": [{"t": 0, "y": -0.12, "rot": 8}, {"t": 0.4, "y": ay, "rot": -13, "ease": "bounce"}]},
                            txt("AIR IN THE SAME BOX", 0.11, 84, enter="pop", at=0.3),
                            txt("*~1,000,000 TONNES*", 0.18, 110, enter="zoom", at=1.6)])})
for L in S[-1]["layers"]:
    if L.get("id") == "extra" and L["acting"][-1][0] == "cheer":
        L["hops"] = [[2.45 + random.uniform(0, 0.3), 0.03, 0.45]]
# 12. close payoff
S.append({"say": "So the cloud isn't light. The *sky* around it is just *heavier*.", "transition": "cut", "caption_y": 0.64,
          "layers": [plate("meadow_wide", blur=10, keys=[{"t": 0, "scale": 1.35}, {"t": 3.6, "scale": 1.42}]),
                     close_ved([["warm", 0], ["explain", 1.2], ["crossed", 2.8]]),
                     txt("THE AIR: *2,000x* HEAVIER", 0.14, 92, enter="pop", at=2.6, sfx="ding")]})

job = {"id": ID, "title": "This fluffy cloud weighs 100 elephants ☁️",
       "description": "A normal puffy cumulus cloud holds about 500 tonnes of water, roughly 100 elephants. So why doesn't it fall? Tiny droplets, rising warm air, and a sky that weighs far more.\n\n"
                      "Sources: https://www.loc.gov/everyday-mysteries/meteorology-climatology/item/how-much-does-a-cloud-weigh/ ; "
                      "https://www.earthdate.org/episodes/puffy-clouds-weigh-in ; https://www.zmescience.com/science/how-much-do-clouds-weigh ; "
                      "https://www.sciencealert.com/this-is-how-much-a-cloud-weighs",
       "tags": ["clouds", "how heavy is a cloud", "cloud weight", "weather", "science", "physics", "science explained", "facts", "nature"],
       "hashtags": ["#science", "#weather"],
       "meta": {"format": "scale-shock", "topic": "how much a cloud weighs (~500 tonnes)", "hook": "number-shock",
                "idea_source": "backlog (ideas.md)", "characters": ["ved", "extra"],
                "sources": ["https://www.loc.gov/everyday-mysteries/meteorology-climatology/item/how-much-does-a-cloud-weigh/",
                            "https://www.earthdate.org/episodes/puffy-clouds-weigh-in",
                            "https://www.zmescience.com/science/how-much-do-clouds-weigh",
                            "https://www.sciencealert.com/this-is-how-much-a-cloud-weighs"],
                "humour": {"trend": "'They don't know' format (rising on Imgflip, Nov 7-8 2026), as a text card", "beat": "zoom_punch", "scene": 7}},
       "privacy": "public", "speaker": "ved", "assets_script": J + "assets.py", "scenes": S}
json.dump(job, open(J + "job.json", "w"), indent=1, ensure_ascii=False)
print("scenes", len(S), "using", SRC)
