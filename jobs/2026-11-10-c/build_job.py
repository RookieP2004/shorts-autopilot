"""2026-11-10-c: "Why do we wreck the things we all share?" (big-question): the tragedy of the commons.
2D Ved + herders staged in depth inside Blender sets (a lush shared pasture, the same pasture grazed bare) built from
stills + cut-outs (two cows). Run after the assets exist: python jobs/2026-11-10-c/build_job.py
"""
import json, os, random, sys
sys.path.insert(0, os.getcwd())
from PIL import Image
from autopilot.stage import Stage

random.seed(10)
ID = "2026-11-10-c"
J = f"jobs/{ID}/"
A = J + "assets/"
SRC = A if os.path.exists(A + "plate_lush_mid.json") else "/tmp/claude-0/pvc/"
ST = {n: Stage(SRC + f"plate_{n}.json") for n in ("lush_wide", "lush_mid", "bare_wide")}
ASPECT = {k: (lambda im: im.width / im.height)(Image.open(SRC + f"cow_{k}.png")) for k in ("bw", "brown")}

# ---- the herders (same people, same outfits in every shot)
OUT = {
    "tomas": {"skin": "#e2b48d", "hat": ["straw", "#e6c27a"], "top": ["#6fc3c0", "shirt"], "bottom": ["#34425c", "trousers"],
              "belt": "#5a3b2e", "build": "slim"},
    "amina": {"skin": "#8d5a3b", "hat": ["headscarf", "#d9534f"], "top": ["#f2b04a", "dress"], "necklace": "#6fc3c0",
              "hair": ["#140f0c", "long"]},
    "ravi": {"skin": "#b97a55", "hat": ["cap", "#f6efe2"], "top": ["#7c2533", "kurta"], "bottom": ["#efe3c8", "trousers"],
             "hair": ["#2a2320", "curly"], "build": "round"},
    "omar": {"skin": "#a0694a", "hat": ["fez", "#b03a2e"], "top": ["#f6efe2", "vest"], "bottom": ["#5a4636", "trousers"]},
    "lena": {"skin": "#e6b996", "top": ["#9b59b6", "dress"], "hair": ["#6b4423", "bun"], "earrings": "#f2b04a"},
}
F = "font-family='Poppins, DejaVu Sans, sans-serif' font-weight='800'"
AN = "font-family='Anton, DejaVu Sans, sans-serif'"


def plate(name, blur=0, **k):
    return {"type": "image", "path": A + f"plate_{name}.png", "x": 0.5, "y": 0.5, "w": 1.0, "enter": "none", "blur": blur, **k}


def fg(name):
    return {"type": "image", "path": A + f"fg_{name}.png", "x": 0.5, "y": 0.5, "w": 1.0, "enter": "none"}


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


def cow(set_, wx, wy, kind="bw", t0=None, flip=False, fall=0.5, **k):
    """A cow cut-out standing at floor position (wx, wy); with t0 it drops in from above and bounces."""
    st = ST[set_]
    gx, gy = st.point(wx, wy, 0.0)
    _, ty = st.point(wx, wy, 1.32)
    hf = gy - ty
    w = hf * 1920 / 1080 * ASPECT[kind]
    cy = gy - hf / 2
    L = {"type": "image", "path": A + f"cow_{kind}.png", "x": round(gx, 4), "y": round(cy, 4), "w": round(w, 4),
         "enter": "none", "flip": flip, "_depth": wy, "allow_outside_safe": True}
    if t0 is not None:
        L["at"] = t0
        L["keys"] = [{"t": 0, "y": -0.12, "rot": random.uniform(-25, 25)}, {"t": fall, "y": round(cy, 4), "rot": 0, "ease": "bounce"}]
        L["sfx"] = k.pop("sfx", "pop")
    L.update(k)
    return L


FENCE_Y = -2.6     # the front fence (foreground layer) stands at this floor depth


def staged(set_, behind=(), front=(), extra_top=(), fg_layer=True):
    allp = list(behind) + list(front)
    behind = [L for L in allp if L["_depth"] >= FENCE_Y]
    front = [L for L in allp if L["_depth"] < FENCE_Y]
    out = [plate(set_)] + sorted(behind, key=lambda L: -L["_depth"])
    if fg_layer:
        out.append(fg(set_))
    out += sorted(front, key=lambda L: -L["_depth"])
    out += list(extra_top)
    for L in out:
        L.pop("_depth", None)
    return out


def card(inner, w=900, h=150):
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {w} {h}'><rect x='5' y='5' width='{w-10}' height='{h-10}' rx='30' "
            f"fill='#f6efe2' stroke='#1a1410' stroke-width='6'/>{inner}</svg>")


ICON = {
    "milk": "<path d='M44,22 L76,22 L76,34 L86,50 L86,98 L34,98 L34,50 L44,34 Z' fill='#ffffff' stroke='#1a1410' stroke-width='5'/>"
            "<rect x='34' y='60' width='52' height='20' fill='#6fc3c0'/>",
    "grass": "<path d='M20,98 L32,46 L40,98 M38,98 L52,30 L62,98 M58,98 L74,40 L82,98 M78,98 L92,52 L100,98' fill='#46965a' stroke='#2f6b3c' stroke-width='4' stroke-linejoin='round'/>",
    "cod": "<path d='M14,60 C30,34 70,32 92,56 L110,40 L106,60 L110,80 L92,64 C70,88 30,86 14,60 Z' fill='#7a8fa3'/><circle cx='34' cy='56' r='5' fill='#1a1410'/>",
}


def row(icon, label, value, color, sub=None):
    s = f"<text x='150' y='{70 if sub else 96}' font-size='48' fill='#1a1410' {F}>{label}</text>"
    if sub:
        s += f"<text x='150' y='118' font-size='34' fill='#5a4636' {F}>{sub}</text>"
    return card(f"<g transform='translate(16,15)'>{ICON[icon]}</g>{s}"
                f"<text x='860' y='112' text-anchor='end' font-size='96' fill='{color}' {AN}>{value}</text>")


def cod_panel():
    bars = ("<text x='40' y='70' font-size='46' fill='#1a1410' " + F + ">NORTHERN COD (spawning stock)</text>"
            "<text x='40' y='150' font-size='40' fill='#1a1410' " + F + ">1962</text>"
            "<rect x='170' y='112' width='650' height='50' rx='14' fill='#34425c'/>"
            "<text x='800' y='150' text-anchor='end' font-size='38' fill='#f6efe2' " + F + ">1.6 MILLION T</text>"
            "<text x='40' y='235' font-size='40' fill='#1a1410' " + F + ">1992</text>"
            "<rect x='170' y='197' width='46' height='50' rx='14' fill='#d9534f'/>"
            "<text x='236' y='235' font-size='38' fill='#d9534f' " + F + ">~0.1 MILLION T</text>"
            "<text x='860' y='330' text-anchor='end' font-size='92' fill='#d9534f' " + AN + ">-93%</text>"
            "<g transform='translate(30,262) scale(0.9)'>" + ICON["cod"] + "</g>"
            "<text x='160' y='325' font-size='38' fill='#1a1410' " + F + ">in 30 years</text>")
    return card(bars, 900, 360)


def rules_panel():
    lines = ["MAX *3* COWS EACH", "EVERYONE WATCHES", "BREAK IT = PAY A FINE"]
    s = f"<text x='450' y='78' text-anchor='middle' font-size='60' fill='#7c2533' {AN}>VILLAGE RULES</text>"
    for i, l in enumerate(lines):
        l = l.replace("*", "")
        s += (f"<circle cx='70' cy='{140 + i * 72}' r='24' fill='#46965a'/><text x='70' y='{152 + i * 72}' text-anchor='middle' "
              f"font-size='34' fill='#f6efe2' {F}>{i + 1}</text><text x='118' y='{154 + i * 72}' font-size='44' fill='#1a1410' {F}>{l}</text>")
    return card(s, 900, 350)


S = []
# 1. hook (lush wide): green shared pasture, herders and cows grazing, Ved walks in
sw = ST["lush_wide"]
S.append({"say": "Why do we wreck the things we all *share*?",
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.0, "zoom": 1.06, "focus": [0.5, 0.52]}]},
          "layers": staged("lush_wide",
                           behind=[cow("lush_wide", -1.4, -0.5, "bw"), cow("lush_wide", 1.6, -1.8, "brown", flip=True),
                                   person("lush_wide", "amina", -1.9, -1.4, [["idle", 0], ["wave", 1.4]]),
                                   person("lush_wide", "ravi", 2.0, -0.6, [["idle", 0]])],
                           front=[ved("lush_wide", 0.2, -6.2, [["warm", 0], ["explain", 1.0], ["think", 2.2]],
                                      walk=[(0, 2.6, -6.6), (1.0, 0.2, -6.2)])],
                           extra_top=[txt("WHY DO WE WRECK WHAT WE *SHARE?*", 0.15, 104, enter="none")])})
# 2. close-up on Ved
S.append({"say": "It's called the *tragedy of the commons*. Picture a village.", "transition": "cut", "caption_y": 0.64,
          "layers": [plate("lush_mid", blur=10, keys=[{"t": 0, "scale": 1.35}, {"t": 3.2, "scale": 1.4}]),
                     close_ved([["explain", 0], ["welcome", 1.9]]),
                     txt("THE TRAGEDY OF THE *COMMONS*", 0.14, 100, enter="pop", at=0.5, sfx="pop")]})
# 3. wide: herders walk in, one cow each drops onto the free pasture
herders = [("amina", -1.6, -2.0), ("ravi", 1.7, -1.4), ("tomas", -0.5, -3.6), ("omar", 1.1, -4.6), ("lena", -1.4, -5.2)]
hl, cl = [], []
for i, (who, wx, wy) in enumerate(herders):
    side = -1 if wx < 0 else 1
    hl.append(person("lush_wide", who, wx, wy, [["idle", 0], ["happy", 1.0 + i * 0.2]], walk=[(0, wx + side * 3.0, wy - 0.4), (0.9, wx, wy)]))
    cx, cy = [(-0.6, -0.6), (0.9, 0.0), (0.4, -2.4), (1.9, -3.4), (-2.0, -3.6)][i]
    cl.append(cow("lush_wide", cx, cy, "bw" if i % 2 == 0 else "brown", t0=0.5 + i * 0.25, flip=cx > 0))
S.append({"say": "*Ten* herders share one *free* pasture.", "transition": "slide_left",
          "camera": {"zoom": [1.0, 1.04], "focus": [0.5, 0.52]},
          "layers": staged("lush_wide", behind=hl + cl, front=[],
                           extra_top=[txt("1 PASTURE · *10* HERDERS", 0.13, 80, enter="pop", at=0.2, sfx="pop"),
                                      txt("FREE FOR ALL", 0.2, 70, enter="pop", at=1.2, color="accent")])})
# 4. mid: Tomas adds one more cow and cheers
sm = ST["lush_mid"]
S.append({"say": "Tomas thinks: one more cow, more milk... all for *me*.", "transition": "cut",
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.6, "zoom": 1.07, "focus": [0.48, 0.52]}]},
          "layers": staged("lush_mid",
                           behind=[cow("lush_mid", 1.3, 1.0, "brown", flip=True),
                                   person("lush_mid", "tomas", 0.1, -0.8, [["idle", 0], ["point", 1.4], ["cheer", 2.4]], hops=[[2.5, 0.04, 0.45]]),
                                   cow("lush_mid", -1.5, 0.2, "bw", t0=1.5, sfx="boom")],
                           front=[ved("lush_mid", 1.5, -1.6, [["explain", 0], ["smirk", 2.6]])],
                           extra_top=[txt("+1 COW = *MORE MILK*", 0.13, 84, enter="pop", at=1.6, sfx="pop"),
                                      txt("ALL FOR *ME*", 0.21, 80, enter="pop", at=2.6)])})
# 5. infographic: the gain is private, the cost is shared
S.append({"say": "The extra milk is *all his*. The lost grass? Split *ten ways*.", "transition": "zoom", "caption_y": 0.45,
          "layers": [plate("lush_mid", blur=14, keys=[{"t": 0, "scale": 1.2}]),
                     {"type": "image", "svg": row("milk", "HIS GAIN", "100%", "#46965a", "the milk is all his"), "w": 0.86,
                      "x": 0.5, "y": 0.13, "enter": "slide_right", "at": 0.2, "sfx": "pop"},
                     {"type": "image", "svg": row("grass", "HIS COST", "1/10", "#d9534f", "the grass loss is shared"), "w": 0.86,
                      "x": 0.5, "y": 0.235, "enter": "slide_right", "at": 1.9, "sfx": "pop"},
                     txt("SO ADDING A COW *ALWAYS* PAYS", 0.33, 64, enter="pop", at=3.2, sfx="ding"),
                     {"type": "character", "id": "ved", "pose": "point", "x": 0.5, "y": 0.72, "h": 0.42, "enter": "none",
                      "acting": [["explain", 0], ["point", 1.5], ["serious", 3.0]], "allow_outside_safe": True}]})
# 6. wide: everyone does the same; cows rain in
rain = []
for i in range(9):
    wx = random.uniform(-1.8, 1.8); wy = random.uniform(-5.0, 0.0)
    rain.append(cow("lush_wide", wx, wy, random.choice(["bw", "brown"]), t0=0.3 + i * 0.22, flip=random.random() < 0.5,
                    sfx="pop" if i % 2 == 0 else "none"))
S.append({"say": "So *every* herder adds one more.", "transition": "cut",
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 2.6, "zoom": 1.05, "focus": [0.5, 0.52]}]},
          "layers": staged("lush_wide",
                           behind=[person("lush_wide", w, x, y, [["happy", 0], ["cheer", 0.8 + i * 0.2]], hops=[[0.9 + i * 0.2, 0.04, 0.4]])
                                   for i, (w, x, y) in enumerate(herders)] + rain,
                           extra_top=[{"type": "counter", "from": 10, "to": 20, "count_dur": 2.2, "suffix": " COWS", "size": 120,
                                       "x": 0.5, "y": 0.15, "color": "accent", "at": 0.3, "enter": "pop"}])})
# 7. comic beat: reaction cut-away
S.append({"dur": 1.8, "transition": "cut", "captions": False,
          "layers": [plate("lush_mid", blur=10, keys=[{"t": 0, "scale": 1.35}]), dict(close_ved([["idle", 0]]), acting="none")],
          "beat": {"kind": "side_eye", "at": 0.1, "dur": 1.6, "zoom": 1.12, "focus": [0.5, 0.42],
                   "text": "all 10 herders, at the same time:\n*\"one more can't hurt\"*", "text_y": 0.18}})
# 8. bare wide: the grass is gone, herders slump and walk away
sb = ST["bare_wide"]
gone = [person("bare_wide", w, x, y, [["sad", 0]], walk=[(0.8, x, y), (3.4, x + (-3.2 if x < 0 else 3.2), y - 0.5)])
        for (w, x, y) in herders[:4]]
S.append({"say": "Until the grass is gone... and *everyone* loses.", "transition": "flash", "sfx": "boom",
          "camera": {"keys": [{"t": 0, "zoom": 1.06, "focus": [0.5, 0.52]}, {"t": 3.0, "zoom": 1.0, "focus": [0.5, 0.5]}]},
          "layers": staged("bare_wide",
                           behind=gone + [cow("bare_wide", -1.2, -0.5, "bw"), cow("bare_wide", 1.5, -2.5, "brown", flip=True)],
                           front=[ved("bare_wide", 0.5, -6.4, [["surprised", 0], ["serious", 1.4]])],
                           extra_top=[txt("GRASS: *0*", 0.14, 130, enter="pop", at=0.3, sfx="pop", highlight="danger"),
                                      txt("EVERYONE LOSES", 0.23, 80, enter="pop", at=1.6)])})
# 9. real world: the northern cod collapse
S.append({"say": "It's real. In 1992, Canada shut its cod fishery after the fish crashed. Around *30,000* jobs, gone.",
          "transition": "slide_up", "caption_y": 0.465,
          "bg": {"type": "gradient", "colors": ["#123047", "#1f5a73"], "angle": 90, "pattern": "dots"},
          "layers": [{"type": "image", "svg": cod_panel(), "w": 0.86, "x": 0.5, "y": 0.2, "enter": "pop", "at": 0.1, "sfx": "pop"},
                     txt("1992: FISHERY *CLOSED*", 0.38, 74, enter="pop", at=2.6, sfx="boom"),
                     {"type": "counter", "from": 0, "to": 30000, "count_dur": 1.4, "prefix": "~", "suffix": " JOBS LOST", "size": 80,
                      "x": 0.5, "y": 0.56, "color": "danger", "at": 4.0, "enter": "pop"},
                     {"type": "character", "id": "ved", "pose": "serious", "x": 0.5, "y": 0.8, "h": 0.32, "enter": "slide_up",
                      "acting": [["serious", 0], ["explain", 2.4], ["think", 4.6]], "allow_outside_safe": True}]})
# 10. lush wide: two answers; Ostrom's third way
S.append({"say": "Hardin's fix: private fields, or government rules. But Elinor Ostrom won a *Nobel* for a third way.",
          "transition": "slide_left",
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 5.0, "zoom": 1.06, "focus": [0.5, 0.52]}]},
          "layers": staged("lush_wide",
                           behind=[cow("lush_wide", -1.4, -0.5, "bw"), cow("lush_wide", 1.6, -1.8, "brown", flip=True)],
                           front=[ved("lush_wide", 0.2, -6.2, [["explain", 0], ["point", 2.6], ["surprised", 4.0]], hops=[[4.0, 0.04, 0.4]])],
                           extra_top=[{"type": "image", "svg": row("grass", "FIX 1", "FENCE IT", "#34425c", "private fields"), "w": 0.8,
                                       "x": 0.5, "y": 0.12, "enter": "slide_right", "at": 0.3, "sfx": "pop"},
                                      {"type": "image", "svg": row("milk", "FIX 2", "RULES", "#34425c", "set by government"), "w": 0.8,
                                       "x": 0.5, "y": 0.215, "enter": "slide_right", "at": 1.5, "sfx": "pop"},
                                      txt("ELINOR OSTROM · *NOBEL 2009*", 0.32, 70, enter="pop", at=3.4, sfx="ding")])})
# 11. mid: the villagers make their own rules and keep the grass
S.append({"say": "Villages that make their *own* rules, and watch each other, can keep the grass for generations.",
          "transition": "cut", "caption_y": 0.4,
          "layers": staged("lush_mid",
                           behind=[cow("lush_mid", 1.3, 1.0, "brown", flip=True), cow("lush_mid", -1.4, 1.4, "bw"),
                                   person("lush_mid", "tomas", 0.1, -0.6, [["explain", 0], ["point", 1.8], ["happy", 3.4]]),
                                   person("lush_mid", "amina", -0.9, -0.2, [["idle", 0], ["happy", 1.2], ["cheer", 3.6]], hops=[[3.7, 0.04, 0.4]])],
                           front=[person("lush_mid", "ravi", 1.0, -0.8, [["shrug", 0], ["happy", 2.0]])],
                           extra_top=[{"type": "image", "svg": rules_panel(), "w": 0.84, "x": 0.5, "y": 0.2, "enter": "pop",
                                       "at": 0.4, "sfx": "pop"}])})
# 12. close: payoff
S.append({"say": "So sharing isn't the problem. Sharing with *no rules* is.", "transition": "cut", "caption_y": 0.64,
          "layers": [plate("lush_mid", blur=10, keys=[{"t": 0, "scale": 1.35}, {"t": 3.6, "scale": 1.42}]),
                     close_ved([["explain", 0], ["serious", 1.6], ["crossed", 2.8]]),
                     txt("SHARING + *NO RULES* = TRAGEDY", 0.14, 96, enter="pop", at=1.8, sfx="ding")]})

job = {"id": ID, "title": "Why do we wreck the things we all share? 🐄",
       "description": "One free pasture, ten herders, one extra cow each: the tragedy of the commons in under a minute, "
                      "plus the real cod collapse and the Nobel-winning way villages avoid it.\n\n"
                      "Sources: Hardin, 'The Tragedy of the Commons' (Science, 1968); Penn State GEOG 30 on the commons; "
                      "Heritage Newfoundland & Labrador, 'Cod Moratorium'; Econlib, Elinor Ostrom biography.",
       "tags": ["tragedy of the commons", "economics", "game theory", "Elinor Ostrom", "overfishing", "cod collapse",
                "shared resources", "economics explained"],
       "hashtags": ["#economics", "#explained"],
       "meta": {"format": "big-question", "topic": "the tragedy of the commons (Hardin vs Ostrom)", "hook": "question",
                "idea_source": "backlog", "characters": ["ved", "extra"],
                "sources": ["https://courses.ems.psu.edu/geog30/node/343",
                            "https://webarchive.library.unt.edu/web/20141030101943/http://en.wikipedia.org/wiki/Tragedy_of_the_commons",
                            "https://www.heritage.nf.ca/articles/economy/moratorium.php",
                            "https://www.econlib.org/library/Enc/bios/Ostrom.html"],
                "humour": {"trend": "timeless: 'X, at the same time:' quote caption (no current trend fitted cleanly)",
                           "beat": "side_eye", "scene": 6}},
       "privacy": "public", "speaker": "ved", "assets_script": J + "assets.py", "scenes": S}
json.dump(job, open(J + "job.json", "w"), indent=1, ensure_ascii=False)
print("scenes", len(S), "using", SRC)
