"""2026-11-08-c: "How many ants live on Earth?" (scale-shock) in a sunny town park + a town square with a giant scale.
2D Ved + faceless townspeople staged in depth inside Blender plates (house style of jobs/2026-11-08-m3).
Run: python jobs/2026-11-08-c/build_job.py
"""
import json, os, random, sys
sys.path.insert(0, os.getcwd())
from autopilot.stage import Stage

random.seed(8)
J = "jobs/2026-11-08-c/"
A = J + "assets/"
PV = "/tmp/claude-0/-home-claude-shorts-autopilot/1d6c5faf-30e7-5331-8d60-42363aead0ce/scratchpad/pv/"
SRC = A if os.path.exists(A + "plate_square_tipped.json") else PV
ST = {n: Stage(SRC + f"plate_{n}.json") for n in ("park_wide", "park_mid", "park_close", "square_empty", "square_tipped")}

# ---- the town (same people, same outfits in every shot)
OUT = {
    "nani": {"skin": "#a86f4c", "build": "round", "hair": ["#d8d4cc", "bun"], "top": ["#6fc3c0", "dress"], "necklace": "#f2b04a",
             "bag": "#8a5a3c", "earrings": "#f2b04a"},
    "kofi": {"skin": "#6b4430", "hat": ["straw", "#e6c27a"], "top": ["#f2b04a", "tshirt"], "bottom": ["#34425c", "shorts"], "build": "slim"},
    "mei": {"skin": "#f0c8a8", "hair": ["#1d1712", "long"], "hat": ["beret", "#d9534f"], "top": ["#f6efe2", "shirt"],
            "bottom": ["#34425c", "trousers"]},
    "arjun": {"skin": "#b97a55", "hat": ["cap", "#46965a"], "top": ["#34425c", "kurta"], "bottom": ["#efe3c8", "trousers"]},
    "lucia": {"skin": "#c98e62", "hat": ["headscarf", "#9b59b6"], "top": ["#f2b04a", "dress"], "bag": "#7c2533"},
}


def plate(name, blur=0, **k):
    return {"type": "image", "path": A + f"plate_{name}.png", "x": 0.5, "y": 0.5, "w": 1.0, "enter": "none", "blur": blur, **k}


def fg(name):
    return {"type": "image", "path": A + f"fg_{name}.png", "x": 0.5, "y": 0.5, "w": 1.0, "enter": "none"}


def sprite(name, x, y, w, **k):
    return {"type": "image", "path": A + name + ".png", "x": x, "y": y, "w": w, "enter": k.pop("enter", "none"), **k}


def txt(t, y, size=96, **k):
    return {"type": "text", "text": t, "font": "display", "x": 0.5, "y": y, "size": size, "max_w": 0.88,
            "stroke": "#0b0f12", "stroke_width": 7, **k}


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


def staged(set_, behind=(), front=(), extra_top=(), use_fg=True):
    out = [plate(set_)] + sorted(behind, key=lambda L: -L["_depth"])
    if use_fg and set_.startswith("park"):
        out.append(fg(set_))
    out += sorted(front, key=lambda L: -L["_depth"])
    out += list(extra_top)
    for L in out:
        L.pop("_depth", None)
    return out


def clean(layers):
    for L in layers:
        L.pop("_depth", None)
    return layers


def trail(set_, p0, p1, n, w0, w1, t_walk=2.6, gap=0.22, until=None, start=0.0, jitter=0.006):
    """A marching line of side-view ants from floor point p0 to p1 (world metres). Faces right by default."""
    st = ST[set_]
    x0, y0 = st.point(*p0)
    x1, y1 = st.point(*p1)
    flip = bool(x1 < x0)
    out = []
    for k in range(n):
        at = start + k * gap
        j = random.uniform(-jitter, jitter)
        L = sprite("ant_side", x0, y0 + j, w0, at=at, flip=flip, loop="bob", loop_amp=0.6, loop_speed=3.0,
                   keys=[{"t": 0, "x": x0, "y": y0 + j, "scale": 1.0},
                         {"t": t_walk, "x": x1, "y": y1 + j, "scale": w1 / w0, "ease": "linear"}],
                   until=at + t_walk, exit="fade", exit_dur=0.15)
        if until is not None and at > until:
            break
        out.append(L)
    return out


S = []
HILL = (1.75, -0.55, 0.0)
CAKE = (0.42, 0.05, 0.03)

# 1. HOOK (medium): the number is on screen at frame 0; picnic in the park, ants already marching to the cake
S.append({"say": "Twenty *quadrillion* ants are alive on Earth, right now.",
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.6, "zoom": 1.07, "focus": [0.55, 0.5]}]},
          "layers": staged("park_mid",
                           behind=[person("park_mid", "nani", -0.35, 1.55, [["idle", 0], ["point", 1.6]]),
                                   person("park_mid", "kofi", 0.75, 1.45, [["happy", 0], ["surprised", 1.9]])],
                           front=[ved("park_mid", 0.55, -1.75, [["explain", 0], ["point", 1.5], ["warm", 2.8]])],
                           extra_top=trail("park_mid", HILL, CAKE, 14, 0.035, 0.026, t_walk=2.4, gap=0.25) + [
                               txt("20,000,000,000,000,000", 0.13, 80, enter="none", color="accent"),
                               txt("ANTS ON EARTH, *RIGHT NOW*", 0.2, 66, enter="none")])})
# 2. close-up on Ved
S.append({"say": "That's a two, followed by *sixteen zeros*.", "transition": "cut", "caption_y": 0.64,
          "layers": [plate("park_mid", blur=10, keys=[{"t": 0, "scale": 1.35}, {"t": 2.6, "scale": 1.4}]),
                     close_ved([["serious", 0], ["explain", 1.0]]),
                     txt("2 + *16 ZEROS*", 0.14, 120, enter="pop", at=1.0, sfx="pop")]})
# 3. close at ant level: the trail from the ant hill to the cake
S.append({"say": "Way too big to picture. So let's *share them out*.", "transition": "slide_left",
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.0, "zoom": 1.08, "focus": [0.6, 0.5]}]},
          "layers": [plate("park_close")] + trail("park_close", HILL, CAKE, 18, 0.07, 0.045, t_walk=2.6, gap=0.2)
                    + [fg("park_close"), txt("TOO BIG TO *PICTURE*", 0.14, 100, enter="pop", at=0.3, sfx="pop")]})
# 4. wide: the whole park; divide by everyone on Earth
div = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 900 300'><rect width='900' height='300' rx='34' fill='#f6efe2'/>"
       "<rect width='900' height='300' rx='34' fill='none' stroke='#1a1410' stroke-width='6'/>"
       "<text x='450' y='118' text-anchor='middle' font-size='66' fill='#1a1410' font-family='Anton, DejaVu Sans, sans-serif'>20 QUADRILLION ANTS</text>"
       "<text x='450' y='200' text-anchor='middle' font-size='64' fill='#d98a1a' font-family='Anton, DejaVu Sans, sans-serif'>/  8 BILLION PEOPLE</text>"
       "<rect x='300' y='228' width='300' height='10' rx='5' fill='#1a1410' opacity='0.2'/></svg>")
S.append({"say": "Split them between all *eight billion* people on Earth...", "transition": "zoom",
          "camera": {"zoom": [1.0, 1.05], "focus": [0.5, 0.52]},
          "layers": staged("park_wide",
                           behind=[person("park_wide", "nani", -0.35, 1.55, [["idle", 0], ["wave", 1.2]]),
                                   person("park_wide", "kofi", 0.75, 1.45, [["happy", 0]])],
                           front=[person("park_wide", "mei", -2.8, -2.4, [["idle", 0]], walk=[(0, -3.6, -2.9), (2.4, -1.6, -1.6)]),
                                  person("park_wide", "arjun", 2.9, -0.6, [["idle", 0]], walk=[(0, 3.8, 0.2), (2.2, 2.2, -1.0)]),
                                  person("park_wide", "lucia", -2.4, 2.4, [["hold", 0]]),
                                  ved("park_wide", 0.9, -2.7, [["welcome", 0], ["explain", 1.6]])],
                           extra_top=[{"type": "image", "svg": div, "w": 0.82, "x": 0.5, "y": 0.17, "enter": "pop", "at": 0.6, "sfx": "pop"}])})
# 5. medium: everyone gets ~2.5 million ants; Kofi jumps, Mei shrugs
S.append({"say": "...and every single person gets around *two and a half million* ants.", "transition": "cut",
          "camera": {"zoom": [1.0, 1.06], "focus": [0.5, 0.5], "punch": [2.2]},
          "layers": staged("park_mid",
                           behind=[person("park_mid", "nani", -0.35, 1.55, [["idle", 0], ["surprised", 2.3]]),
                                   person("park_mid", "kofi", 0.75, 1.45, [["idle", 0], ["surprised", 2.2], ["sad", 3.6]], hops=[[2.25, 0.04, 0.45]])],
                           front=[person("park_mid", "mei", -1.75, 0.3, [["idle", 0], ["shrug", 2.4]]),
                                  person("park_mid", "arjun", 1.65, 0.9, [["idle", 0], ["surprised", 2.3]], hops=[[2.35, 0.03, 0.45]])],
                           extra_top=trail("park_mid", HILL, CAKE, 16, 0.035, 0.026, t_walk=2.4, gap=0.22) + [
                               {"type": "counter", "from": 0, "to": 2500000, "count_dur": 1.4, "at": 1.0, "x": 0.5, "y": 0.13,
                                "prefix": "~", "size": 130, "stroke": "#0b0f12", "stroke_width": 7, "enter": "pop"},
                               txt("ANTS *EACH*", 0.215, 84, enter="pop", at=2.4, sfx="ding")])})
# 6. close: Ved points at camera
S.append({"say": "Yes. Including *you*.", "transition": "cut", "caption_y": 0.64,
          "layers": [plate("park_mid", blur=10, keys=[{"t": 0, "scale": 1.4}, {"t": 1.6, "scale": 1.46}]),
                     close_ved([["smirk", 0], ["point", 0.5]])]})
# 7. square, level scale: Ved walks in, crowd watches; the ants' crate drops onto the left pan
sq = ST["square_empty"]
def pan_xy(st, side, scale=1.25):
    x, y = st.point(side * 2.1, 2.0, 1.55 + 0.56 * scale)
    w = abs(st.point(side * 2.1 + 0.72 * scale, 2.0, 2.0)[0] - st.point(side * 2.1 - 0.72 * scale, 2.0, 2.0)[0])
    return x, y, w
import math
def tip_xy(side, scale=1.25, th=math.radians(11)):
    ex, ez = side * 2.1 * math.cos(th), 3.5 + side * 2.1 * math.sin(th)
    return ST["square_tipped"].point(ex, 2.0, ez - 2.0 + 0.12 + 0.56 * scale)
def label(t, x, y, size=44, **k):
    return {"type": "text", "text": t, "font": "display", "x": x, "y": y, "size": size, "max_w": 0.3, "color": "#1a1410",
            "stroke": "#f6efe2", "stroke_width": 5, "shadow": False, "enter": "none", **k}
def follow(L, keys):
    L["keys"] = keys; return L
axl, ayl, aw = pan_xy(sq, -1)
axr, ayr, _ = pan_xy(sq, 1)
crowd_sq = lambda st, act: [person(st, "lucia", -2.6, -1.0, act("lucia")), person(st, "arjun", -1.2, -1.7, act("arjun")),
                            person(st, "mei", 0.4, -1.2, act("mei")), person(st, "nani", 2.6, -0.8, act("nani")),
                            person(st, "kofi", -3.6, 0.2, act("kofi"))]
S.append({"say": "Now put every ant on Earth on one side of a giant scale...", "transition": "slide_left",
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.4, "zoom": 1.06, "focus": [0.5, 0.48]}]},
          "layers": clean([plate("square_empty")] + sorted(crowd_sq("square_empty", lambda w: [["idle", 0], ["point", 2.0] if w == "lucia" else ["idle", 2.0]]),
                                                           key=lambda L: -L["_depth"]) + [
              ved("square_empty", 1.6, -2.3, [["warm", 0], ["explain", 1.2], ["point", 2.2]], walk=[(0, 3.8, -2.6), (1.2, 1.6, -2.3)]),
              sprite("crate_ants", axl, ayl, aw, at=2.0, keys=[{"t": 0, "y": -0.12, "rot": -8}, {"t": 0.55, "y": ayl, "rot": 0, "ease": "bounce"}], sfx="pop"),
              label("ANTS", axl, ayl, 52, at=2.0, keys=[{"t": 0, "y": -0.12, "rot": -8}, {"t": 0.55, "y": ayl, "rot": 0, "ease": "bounce"}]),
              txt("ALL THE *ANTS*", 0.14, 104, enter="pop", at=2.1)])})
# 8. same shot: wild birds + mammals drop onto the right pan
S.append({"say": "...and every wild *bird* and wild *mammal* on the other.", "transition": "cut",
          "camera": {"zoom": [1.06, 1.1], "focus": [0.5, 0.48]},
          "layers": clean([plate("square_empty")] + sorted(crowd_sq("square_empty", lambda w: [["idle", 0], ["surprised", 1.6]] if w in ("mei", "kofi") else [["idle", 0]]),
                                                           key=lambda L: -L["_depth"]) + [
              ved("square_empty", 1.6, -2.3, [["point", 0], ["explain", 1.8]]),
              sprite("crate_ants", axl, ayl, aw), label("ANTS", axl, ayl, 52),
              sprite("crate_wild", axr, ayr, aw, at=1.2, keys=[{"t": 0, "y": -0.12, "rot": 8}, {"t": 0.55, "y": ayr, "rot": 0, "ease": "bounce"}], sfx="pop"),
              label("BIRDS + MAMMALS", axr, ayr, 40, max_w=0.2, at=1.2, keys=[{"t": 0, "y": -0.12, "rot": 8}, {"t": 0.55, "y": ayr, "rot": 0, "ease": "bounce"}]),
              txt("ALL WILD *BIRDS + MAMMALS*", 0.14, 92, enter="pop", at=1.3)])})
# 9. tipped: the ants win; the crowd jumps
S.append({"say": "The ants are *heavier*.", "transition": "flash", "sfx": "boom",
          "camera": {"keys": [{"t": 0, "zoom": 1.12, "focus": [0.5, 0.48]}, {"t": 1.8, "zoom": 1.02, "focus": [0.5, 0.5]}], "shake": [0.05, 0.35]},
          "layers": clean([plate("square_tipped")] + sorted(crowd_sq("square_tipped", lambda w: [["surprised", 0], ["cheer", 0.7]] if w in ("kofi", "lucia", "arjun") else [["surprised", 0]]),
                                                            key=lambda L: -L["_depth"]) + [
              ved("square_tipped", 1.6, -2.3, [["surprised", 0], ["warm", 1.0]], hops=[[0.1, 0.05, 0.45]]),
              label("ANTS", *tip_xy(-1), 52), label("BIRDS + MAMMALS", *tip_xy(1), 40, max_w=0.2),
              txt("*ANTS* WIN", 0.14, 150, enter="zoom", at=0.15)])})
for L in S[-1]["layers"]:
    if L.get("id") == "extra":
        L["hops"] = [[0.15 + random.uniform(0, 0.4), 0.03, 0.45]]
# 10. comic beat (reaction cut-away): "What's up brah?" (unbothered walk-up meme, Nov 2026)
S.append({"dur": 1.7, "transition": "cut", "captions": False,
          "layers": [plate("square_tipped", blur=10, keys=[{"t": 0, "scale": 1.35}]), dict(close_ved([["idle", 0]]), acting="none")],
          "beat": {"kind": "side_eye", "at": 0.1, "dur": 1.4, "zoom": 1.12, "focus": [0.5, 0.42],
                   "text": "Ants walking past every lion on Earth:\n*\"What's up, brah?\"*", "text_y": 0.18}})
# 11. infographic over the blurred square: a fifth of all humanity
bars = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 900 380'><rect width='900' height='380' rx='34' fill='#f6efe2'/>"
        "<rect width='900' height='380' rx='34' fill='none' stroke='#1a1410' stroke-width='6'/>"
        "<text x='60' y='92' font-size='54' fill='#1a1410' font-family='Poppins, DejaVu Sans, sans-serif' font-weight='800'>WEIGHT OF ALL...</text>"
        "<text x='60' y='170' font-size='46' fill='#1a1410' font-family='Poppins, DejaVu Sans, sans-serif' font-weight='800'>HUMANS</text>"
        "<rect x='280' y='128' width='560' height='54' rx='14' fill='#34425c'/>"
        "<text x='60' y='270' font-size='46' fill='#1a1410' font-family='Poppins, DejaVu Sans, sans-serif' font-weight='800'>ANTS</text>"
        "<rect x='280' y='228' width='112' height='54' rx='14' fill='#7a2e1c'/>"
        "<text x='410' y='270' font-size='60' fill='#d98a1a' font-family='Anton, DejaVu Sans, sans-serif'>~ 1/5</text>"
        "<text x='60' y='340' font-size='30' fill='#5a4636' font-family='Poppins, DejaVu Sans, sans-serif' font-weight='800'>about 12 million tonnes of carbon</text></svg>")
S.append({"say": "All together, they weigh about *a fifth* as much as every human alive.", "transition": "slide_up",
          "caption_y": 0.6,
          "layers": [plate("square_tipped", blur=6, keys=[{"t": 0, "scale": 1.15}, {"t": 4, "scale": 1.2}]),
                     {"type": "image", "svg": bars, "w": 0.84, "x": 0.5, "y": 0.22, "enter": "pop", "at": 0.3, "sfx": "pop"},
                     sprite("ant", 0.72, 0.74, 0.3, enter="pop", at=1.6, sfx="pop", rot=-6)]})
# 12. park, ant level: one ant crashes the picnic
stc = ST["park_close"]
hx, hy = stc.point(2.0, -1.0, 0.0)
cx, cy = stc.point(*CAKE)
S.append({"say": "So next time one ant *crashes your picnic*...", "transition": "cut",
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.0, "zoom": 1.12, "focus": [0.52, 0.5]}]},
          "layers": [plate("park_close"), fg("park_close"),
                     sprite("ant", 0.95, 0.74, 0.34, flip=True, loop="bob", loop_amp=0.8, loop_speed=4.0,
                            keys=[{"t": 0, "x": 1.1, "y": 0.78, "scale": 1.0}, {"t": 2.6, "x": cx + 0.08, "y": cy + 0.03, "scale": 0.45, "ease": "out"}]),
                     txt("ONE ANT?", 0.14, 120, enter="pop", at=0.4, sfx="pop")]})
# 13. close: payoff
S.append({"say": "...relax. He's just one of *your* two and a half million.", "transition": "cut", "caption_y": 0.64,
          "layers": [plate("park_mid", blur=10, keys=[{"t": 0, "scale": 1.35}, {"t": 3.2, "scale": 1.42}]),
                     close_ved([["warm", 0], ["explain", 1.0], ["crossed", 2.6]]),
                     txt("*1* OF YOUR *2,500,000*", 0.14, 96, enter="pop", at=2.4, sfx="ding")]})

job = {"id": "2026-11-08-c", "title": "There are 2.5 million ants for every human 🐜",
       "description": "Twenty quadrillion ants live on Earth. Shared out, that's about two and a half million each, and together they outweigh every wild bird and wild mammal combined.\n\nSources: Schultheiss et al., \"The abundance, biomass, and distribution of ants on Earth\", PNAS (2022) https://www.pnas.org/doi/10.1073/pnas.2201550119 ; https://phys.org/news/2022-09-earth-harbours-ants-wild-birds.html ; world population: https://www.census.gov/newsroom/stories/world-population-day.html",
       "tags": ["ants", "how many ants", "science", "nature", "biology", "insects", "scale", "facts", "explained"],
       "hashtags": ["#science", "#ants"],
       "meta": {"format": "scale-shock", "topic": "how many ants live on Earth (20 quadrillion)", "hook": "number-shock",
                "idea_source": "backlog (ideas.md) + PNAS 2022", "characters": ["ved", "extra"],
                "sources": ["https://www.pnas.org/doi/10.1073/pnas.2201550119",
                            "https://phys.org/news/2022-09-earth-harbours-ants-wild-birds.pdf",
                            "https://cdn.www.census.gov/newsroom/stories/world-population-day.html"],
                "humour": {"trend": "'What's up brah?' unbothered walk-up meme (Nov 2026)", "beat": "side_eye", "scene": 9}},
       "privacy": "public", "speaker": "ved", "assets_script": J + "assets.py", "scenes": S}
json.dump(job, open(J + "job.json", "w"), indent=1, ensure_ascii=False)
print("scenes", len(S), "using", SRC)
