"""2026-11-15-b: "You've been told you have 5 senses" (big-question, "you've been told X" hook). The town park with a
playground roundabout + an inner-ear close-up (Blender stills + cut-outs), 2D panels: nose test, proprioception body map,
sensor chips, the 22-33 count, Aristotle's list.
Run after the assets exist: python jobs/2026-11-15-b/build_job.py
"""
import json, os, sys
sys.path.insert(0, os.getcwd())
from autopilot.stage import Stage

ID = "2026-11-15-b"
J = f"jobs/{ID}/"
A = J + "assets/"
ST = {n: Stage(A + f"plate_{n}.json") for n in ("park_wide", "park_mid")}

OUT = {   # recurring townspeople: same outfit in every shot
    "zara": {"skin": "#c68a5e", "build": "slim", "hair": ["#1a1410", "long"], "hat": ["cap", "#d9534f"],
             "top": ["#6fc3c0", "tshirt"], "bottom": ["#34425c", "shorts"], "shoes": "#f6efe2"},
    "omar": {"skin": "#8d5a3b", "build": "round", "hair": ["#1a1410", "short"], "hat": ["fez", "#7c2533"],
             "top": ["#f2b04a", "shirt"], "bottom": ["#3a3e48", "trousers"], "shoes": "#25262b", "bag": "#8a5a3c"},
}
F = "font-family='Poppins, DejaVu Sans, sans-serif' font-weight='800'"
AN = "font-family='Anton, DejaVu Sans, sans-serif'"


def plate(name, blur=0, **k):
    return {"type": "image", "path": A + f"plate_{name}.png", "x": 0.5, "y": 0.5, "w": 1.0, "enter": "none", "blur": blur, **k}


def sprite(name, x, y, w, **k):
    return {"type": "image", "path": A + name + ".png", "x": x, "y": y, "w": w, "enter": k.pop("enter", "none"), **k}


def txt(t, y, size=96, **k):
    return {"type": "text", "text": t, "font": "display", "x": k.pop("x", 0.5), "y": y, "size": size, "max_w": 0.88,
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
    return {"type": "character", "id": "ved", "pose": acting[0][0], "x": k.pop("x", 0.5), "y": 0.8, "h": 1.06, "enter": "none",
            "acting": acting, "ground": False, "allow_outside_safe": True, **k}


def staged(set_, people=(), fg=False, front=(), extra_top=()):
    # Ved always stands in front of the picnic, so he goes over the foreground layer
    front = list(front) + [L for L in people if L.get("id") == "ved"]
    people = [L for L in people if L.get("id") != "ved"]
    out = [plate(set_)] + sorted(people, key=lambda L: -L["_depth"])
    if fg:
        out.append({"type": "image", "path": A + f"fg_{set_}.png", "x": 0.5, "y": 0.5, "w": 1.0, "enter": "none"})
    out += sorted(front, key=lambda L: -L["_depth"]) + list(extra_top)
    for L in out:
        L.pop("_depth", None)
    return out


def card(svg_body, w=900, h=150):
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {w} {h}'><rect x='5' y='5' width='{w-10}' height='{h-10}' rx='30' "
            f"fill='#f6efe2' stroke='#1a1410' stroke-width='6'/>{svg_body}</svg>")


def stamp(word, color="#d9534f", w=560, fs=110):
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {w} 170'><rect x='10' y='10' width='{w-20}' height='150' rx='18' "
            f"fill='#f6efe2' fill-opacity='0.85' stroke='{color}' stroke-width='14'/><text x='{w/2}' y='126' text-anchor='middle' font-size='{fs}' "
            f"fill='{color}' {AN}>{word}</text></svg>")


HOOK_CARD = card(f"<text x='450' y='106' text-anchor='middle' font-size='84' fill='#1a1410' {AN}>YOU'VE BEEN TOLD...</text>", 900, 150)

# the nose test: a profile head, eyes shut, a finger landing on the nose
NOSE = card(
    "<g transform='translate(60,30)'>"
    "<path d='M120,40 C200,30 250,90 250,160 C250,190 262,205 280,222 C266,232 258,236 252,240 C256,262 252,280 236,292 "
    "C228,320 210,340 170,345 L170,400 L60,400 L64,330 C30,300 20,250 22,200 C24,110 60,48 120,40 Z' fill='#c68a5e'/>"
    "<path d='M100,30 C160,0 250,40 255,120 C220,90 170,80 120,95 C90,105 70,140 66,180 C40,130 50,60 100,30 Z' fill='#1a1410'/>"
    "<path d='M180,175 C195,188 215,188 228,175' stroke='#1a1410' stroke-width='7' fill='none' stroke-linecap='round'/>"
    "<path d='M190,186 l-4,12 M206,190 l0,12 M222,186 l4,12' stroke='#1a1410' stroke-width='4' stroke-linecap='round'/>"
    "<path d='M470,400 C420,330 360,280 300,238' stroke='#c68a5e' stroke-width='34' fill='none' stroke-linecap='round'/>"
    "<path d='M470,400 C420,330 360,280 300,238' stroke='#a8714b' stroke-width='6' fill='none' stroke-linecap='round' stroke-dasharray='2 40'/>"
    "<circle cx='290' cy='228' r='26' fill='none' stroke='#f2b04a' stroke-width='6'/>"
    "</g>"
    f"<text x='620' y='190' text-anchor='middle' font-size='64' fill='#1a1410' {AN}>EYES CLOSED</text>"
    f"<text x='620' y='275' text-anchor='middle' font-size='64' fill='#d9534f' {AN}>FINGER</text>"
    f"<text x='620' y='350' text-anchor='middle' font-size='64' fill='#d9534f' {AN}>TO NOSE</text>", 900, 470)

# proprioception: a body map, sensors in every muscle wired to the brain
PROP = card(
    f"<text x='450' y='78' text-anchor='middle' font-size='56' fill='#1a1410' {AN}>YOUR BODY MAP</text>"
    "<g transform='translate(330,110)' fill='#34425c'>"
    "<circle cx='120' cy='40' r='34'/><rect x='92' y='80' width='56' height='130' rx='26'/>"
    "<rect x='40' y='86' width='30' height='120' rx='15' transform='rotate(18 55 90)'/>"
    "<rect x='170' y='86' width='30' height='120' rx='15' transform='rotate(-18 185 90)'/>"
    "<rect x='96' y='200' width='26' height='150' rx='13'/><rect x='120' y='200' width='26' height='150' rx='13'/></g>"
    "<g fill='#f2b04a' stroke='#1a1410' stroke-width='3'>"
    "<circle cx='450' cy='150' r='12'/><circle cx='378' cy='230' r='12'/><circle cx='522' cy='230' r='12'/>"
    "<circle cx='360' cy='305' r='12'/><circle cx='540' cy='305' r='12'/><circle cx='440' cy='350' r='12'/>"
    "<circle cx='462' cy='350' r='12'/><circle cx='440' cy='420' r='12'/><circle cx='462' cy='420' r='12'/></g>"
    "<path d='M378,230 C300,200 260,160 230,150 M522,230 C600,200 640,160 670,150' stroke='#6fc3c0' stroke-width='5' fill='none' stroke-dasharray='10 8'/>"
    f"<text x='150' y='145' text-anchor='middle' font-size='40' fill='#1a1410' {AN}>WHERE?</text>"
    f"<text x='750' y='145' text-anchor='middle' font-size='40' fill='#1a1410' {AN}>HOW BENT?</text>"
    f"<text x='450' y='505' text-anchor='middle' font-size='52' fill='#d9534f' {AN}>PROPRIOCEPTION</text>", 900, 540)

# spin swirl (a prop: loops are fine)
SWIRL = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 300 300'>"
         "<path d='M150,40 A110,110 0 0 1 260,150' stroke='#f6efe2' stroke-width='16' fill='none' stroke-linecap='round'/>"
         "<path d='M150,260 A110,110 0 0 1 40,150' stroke='#f6efe2' stroke-width='16' fill='none' stroke-linecap='round'/>"
         "<path d='M262,118 L262,170 L224,140 Z' fill='#f6efe2'/><path d='M38,182 L38,130 L76,160 Z' fill='#f6efe2'/></svg>")


def label(t, color="#1a1410", w=600, fs=60):
    return card(f"<text x='{w/2}' y='{int(fs*1.45)}' text-anchor='middle' font-size='{fs}' fill='{color}' {AN}>{t}</text>", w, int(fs * 2.1))


def chip(word, icon, color):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 380 120'>"
            f"<rect x='5' y='5' width='370' height='110' rx='55' fill='#f6efe2' stroke='#1a1410' stroke-width='6'/>"
            f"<circle cx='62' cy='60' r='38' fill='{color}'/>{icon}"
            f"<text x='228' y='78' text-anchor='middle' font-size='{56 if len(word) < 7 else 40}' fill='#1a1410' {AN}>{word}</text></svg>")


I_HEAT = "<path d='M62,32 C80,52 76,64 70,74 C82,70 86,60 84,52 C96,66 92,92 62,94 C36,92 32,70 44,56 C46,66 52,70 56,70 C50,56 54,42 62,32 Z' fill='#f6efe2'/>"
I_COLD = ("<g stroke='#f6efe2' stroke-width='7' stroke-linecap='round'><line x1='62' y1='30' x2='62' y2='90'/>"
          "<line x1='36' y1='45' x2='88' y2='75'/><line x1='36' y1='75' x2='88' y2='45'/></g>")
I_PAIN = "<path d='M66,26 L44,66 L60,66 L54,96 L82,52 L66,52 Z' fill='#f6efe2'/>"
I_HEART = "<path d='M62,90 C30,66 34,36 50,36 C58,36 62,44 62,48 C62,44 66,36 74,36 C90,36 94,66 62,90 Z' fill='#f6efe2'/>"
I_HUNGER = ("<path d='M42,48 C42,40 82,40 82,48 C82,82 72,92 62,92 C52,92 42,82 42,48 Z' fill='none' stroke='#f6efe2' stroke-width='7'/>"
            "<path d='M52,60 C58,66 66,66 72,60' stroke='#f6efe2' stroke-width='5' fill='none'/>")

COUNT = card(
    f"<text x='450' y='86' text-anchor='middle' font-size='64' fill='#1a1410' {AN}>SCHOOL SAID</text>"
    + "".join(f"<circle cx='{250 + k * 100}' cy='150' r='30' fill='#c9b7a0' stroke='#1a1410' stroke-width='4'/>" for k in range(5))
    + f"<text x='450' y='265' text-anchor='middle' font-size='64' fill='#1a1410' {AN}>SCIENTISTS COUNT</text>"
    + "".join(f"<circle cx='{120 + (k % 11) * 66}' cy='{318 + (k // 11) * 62}' r='24' fill='{'#d9534f' if k >= 22 else '#f2b04a'}' "
              f"stroke='#1a1410' stroke-width='4'/>" for k in range(33))
    + f"<text x='450' y='540' text-anchor='middle' font-size='60' fill='#d9534f' {AN}>22 TO 33 SENSES</text>",
    900, 580)

SCROLL = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 640 720'>"
          "<rect x='60' y='60' width='520' height='600' fill='#efdcb0' stroke='#1a1410' stroke-width='6'/>"
          "<rect x='30' y='30' width='580' height='60' rx='30' fill='#c99a5b' stroke='#1a1410' stroke-width='6'/>"
          "<rect x='30' y='630' width='580' height='60' rx='30' fill='#c99a5b' stroke='#1a1410' stroke-width='6'/>"
          f"<text x='320' y='170' text-anchor='middle' font-size='62' fill='#5e3f2a' {AN}>THE 5 SENSES</text>"
          f"<text x='320' y='205' text-anchor='middle' font-size='30' fill='#5e3f2a' {F}>Aristotle, ~350 BC</text>"
          + "".join(f"<text x='140' y='{290 + k * 72}' font-size='54' fill='#3a2414' {AN}>{k+1}. {w}</text>"
                    for k, w in enumerate(["SIGHT", "HEARING", "SMELL", "TASTE", "TOUCH"]))
          + "</svg>")

S = []
# 0. hook (park mid): "you've been told" card + 5 SENSES at frame 0, then the 33 lands
S.append({"say": "You've been told you have five senses. Scientists count up to *thirty-three*.",
          "caption": "You've been told you have five senses. Scientists count up to *33*.",
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.4, "zoom": 1.07, "focus": [0.5, 0.52]}]},
          "layers": staged("park_mid",
                           people=[person("park_mid", "omar", -1.0, 1.3, [["idle", 0], ["surprised", 2.7]]),
                                   ved("park_mid", -0.05, -1.6, [["explain", 0], ["point", 2.5]])],
                           fg=True,
                           extra_top=[{"type": "image", "svg": HOOK_CARD, "x": 0.5, "y": 0.12, "w": 0.78, "rotate": -2, "enter": "none"},
                                      txt("*5* SENSES", 0.225, 150, enter="none", until=2.45, exit="pop"),
                                      txt("*33* SENSES", 0.225, 150, enter="zoom", at=2.5, sfx="boom")])})
# 1. close-up: the nose test
S.append({"say": "Close your eyes. Touch your nose.", "transition": "cut", "caption_y": 0.62,
          "layers": [plate("park_mid", blur=10, keys=[{"t": 0, "scale": 1.35}, {"t": 2.6, "scale": 1.4}]),
                     close_ved([["think", 0], ["point", 1.0]]),
                     {"type": "image", "svg": NOSE, "x": 0.5, "y": 0.2, "w": 0.8, "rotate": -2, "enter": "pop", "at": 0.05, "sfx": "pop"}]})
# 2. park wide: Zara does it; proprioception panel
S.append({"say": "Found it? That's *proprioception*: your muscles mapping every limb.",
          "transition": "slide_left", "caption_y": 0.44,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.5, "zoom": 1.05, "focus": [0.5, 0.52]}]},
          "layers": staged("park_wide",
                           people=[person("park_wide", "zara", 0.9, 0.2, [["idle", 0], ["point", 0.6], ["cheer", 1.6]], hops=[[1.7, 0.05, 0.4]]),
                                   person("park_wide", "omar", -1.9, 0.9, [["idle", 0], ["happy", 1.8]]),
                                   ved("park_wide", -0.5, -2.7, [["welcome", 0], ["explain", 1.4], ["point", 2.6]],
                                       walk=[(0, -3.4, -2.9), (1.0, -0.5, -2.7)])],
                           fg=True,
                           extra_top=[{"type": "image", "svg": PROP, "x": 0.5, "y": 0.2, "w": 0.84, "enter": "slide_down", "at": 1.3, "sfx": "pop"}])})
# 3. roundabout close: Zara spins, then wobbles off; swirl arrows
S.append({"say": "Spin around, and the world keeps spinning after you stop.",
          "transition": "slide_left", "caption_y": 0.44,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 1.4, "zoom": 1.04, "focus": [0.5, 0.5]},
                              {"t": 3.6, "zoom": 1.1, "focus": [0.48, 0.55]}]},
          "layers": [plate("round_close"),
                     {"type": "character", "id": "extra", "pose": "surprised", "x": 0.3, "y": 0.66, "h": 0.3, "enter": "none",
                      "acting": [["surprised", 0], ["shrug", 1.6], ["sad", 2.6]], "talk": False, "rig_args": {"outfit": OUT["zara"]},
                      "allow_outside_safe": True,
                      "keys": [{"t": 0, "x": 0.4, "y": 0.66}, {"t": 0.8, "x": 0.33, "y": 0.68, "walk": True},
                               {"t": 1.6, "x": 0.38, "y": 0.7, "walk": True}, {"t": 2.4, "x": 0.27, "y": 0.72, "walk": True},
                               {"t": 3.2, "x": 0.33, "y": 0.74, "walk": True}],
                      "hops": [[0.9, 0.02, 0.3], [2.5, 0.02, 0.3]]},
                     {"type": "image", "svg": SWIRL, "x": 0.5, "y": 0.24, "w": 0.42, "enter": "pop", "at": 0.2, "sfx": "whoosh",
                      "loop": "spin", "loop_speed": 1.4},
                     txt("STILL *SPINNING?*", 0.12, 110, enter="pop", at=1.8, sfx="pop")]})
# 4. inner-ear close: three loops of fluid = balance
S.append({"say": "That's fluid sloshing in three loops in your inner ear: *balance*.",
          "transition": "zoom", "caption_y": 0.71,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.6, "zoom": 1.1, "focus": [0.48, 0.48]}]},
          "layers": [plate("ear_close"),
                     {"type": "image", "svg": label("3 LOOPS OF FLUID"), "x": 0.36, "y": 0.1, "w": 0.56, "rotate": -3, "enter": "pop", "at": 0.6, "sfx": "pop"},
                     {"type": "shape", "shape": "arrow", "x": 0.36, "y": 0.2, "w": 0.12, "h": 0.03, "color": "accent", "rotate": 80,
                      "enter": "pop", "at": 0.8},
                     {"type": "image", "svg": label("= BALANCE", "#d9534f", 520, 70), "x": 0.72, "y": 0.19, "w": 0.44, "rotate": 3,
                      "enter": "pop", "at": 3.0, "sfx": "ding"}]})
# 5. park mid: heat, cold, pain, heartbeat, hunger (chips + 3D props)
S.append({"say": "Others feel heat, cold, pain, even your *heartbeat* and your *hunger*.",
          "transition": "slide_left", "caption_y": 0.44,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.4, "zoom": 1.05, "focus": [0.5, 0.5]}]},
          "layers": staged("park_mid",
                           people=[person("park_mid", "omar", -1.0, 1.3, [["idle", 0], ["shrug", 2.8], ["sad", 3.6]]),
                                   ved("park_mid", -0.05, -1.6, [["explain", 0], ["point", 1.2], ["explain", 2.6]])],
                           fg=True,
                           extra_top=[{"type": "image", "svg": chip("HEAT", I_HEAT, "#d9534f"), "x": 0.27, "y": 0.11, "w": 0.36, "enter": "pop", "at": 0.3, "sfx": "pop"},
                                      {"type": "image", "svg": chip("COLD", I_COLD, "#3d7fd1"), "x": 0.71, "y": 0.11, "w": 0.36, "enter": "pop", "at": 0.75, "sfx": "pop"},
                                      {"type": "image", "svg": chip("PAIN", I_PAIN, "#f2b04a"), "x": 0.27, "y": 0.2, "w": 0.36, "enter": "pop", "at": 1.25, "sfx": "pop"},
                                      {"type": "image", "svg": chip("HEARTBEAT", I_HEART, "#c8323c"), "x": 0.71, "y": 0.2, "w": 0.36, "enter": "pop", "at": 1.9, "sfx": "pop"},
                                      {"type": "image", "svg": chip("HUNGER", I_HUNGER, "#46965a"), "x": 0.5, "y": 0.29, "w": 0.36, "enter": "pop", "at": 2.7, "sfx": "pop"},
                                      sprite("heart", 0.78, 0.29, 0.13, enter="pop", at=1.95, loop="pulse", loop_amp=0.08, loop_speed=1.6)])})
# 6. comic beat: side-eye reaction cut-away ("Tony Stark head turn" = the sideways 'I noticed that' glance)
S.append({"dur": 1.6, "transition": "cut", "captions": False,
          "layers": [plate("park_mid", blur=10, keys=[{"t": 0, "scale": 1.35}]), dict(close_ved([["side_eye", 0]]), acting="none")],
          "beat": {"kind": "side_eye", "at": 0.1, "dur": 1.45, "who": "ved",
                   "text": "my stomach when chips open\n*two rooms* away:", "text_y": 0.2}})
# 7. park wide: count them all, 22 to 33
S.append({"say": "Count them all, and you get *twenty-two* to *thirty-three*.", "caption": "Count them all, and you get *22* to *33*.",
          "transition": "slide_up", "caption_y": 0.5,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.4, "zoom": 1.05, "focus": [0.5, 0.5]}]},
          "layers": staged("park_wide",
                           people=[person("park_wide", "zara", 0.9, 0.2, [["idle", 0], ["surprised", 1.6]]),
                                   person("park_wide", "omar", -1.9, 0.9, [["idle", 0], ["cheer", 1.8]], hops=[[1.9, 0.05, 0.4]]),
                                   ved("park_wide", -0.5, -2.7, [["explain", 0], ["point", 1.4]])],
                           fg=True,
                           extra_top=[{"type": "image", "svg": COUNT, "x": 0.5, "y": 0.22, "w": 0.86, "enter": "slide_down", "at": 0.1, "sfx": "whoosh"}])})
# 8. close payoff: Aristotle's scroll gets stamped; loops to the hook
S.append({"say": "Aristotle wrote the list of five. Your body never read it.", "transition": "cut", "caption_y": 0.64,
          "layers": [plate("park_mid", blur=10, keys=[{"t": 0, "scale": 1.35}, {"t": 4.0, "scale": 1.42}]),
                     close_ved([["explain", 0], ["warm", 1.6], ["smirk", 2.6]]),
                     {"type": "image", "svg": SCROLL, "x": 0.5, "y": 0.17, "w": 0.4, "rotate": -3, "enter": "slide_down", "at": 0.05, "sfx": "whoosh"},
                     {"type": "image", "svg": stamp("INCOMPLETE", w=700, fs=96), "x": 0.5, "y": 0.22, "w": 0.6, "rotate": -9,
                      "enter": "zoom", "at": 2.0, "sfx": "boom"}]})


job = {"id": ID, "title": "You've been told you have 5 senses. Try 33 👃",
       "description": "Close your eyes and touch your nose: you just used a sense that's not on the school list. Proprioception "
                      "(muscle sensors that map your body), balance (fluid in three loops in your inner ear), heat, cold, pain, "
                      "your heartbeat and hunger... Depending on how you split them, scientists count 22 to 33 senses, not "
                      "Aristotle's five.\n\n"
                      "Sources: Charles Spence (Oxford Crossmodal Research Lab) via VICE; BBC Science Focus (Lisa Feldman Barrett); "
                      "'Human senses and sensors from Aristotle to the present', Frontiers in Neurology 2024.",
       "tags": ["how many senses do humans have", "five senses", "proprioception", "sense of balance", "inner ear",
                "interoception", "human body", "neuroscience", "science explained"],
       "hashtags": ["#science", "#humanbody"],
       "instagram": {"hashtags": ["#science", "#humanbody", "#neuroscience", "#proprioception", "#explained"]},
       "meta": {"format": "big-question", "topic": "how many senses you really have: proprioception (nose test), balance (inner-ear fluid loops), heat/cold/pain, heartbeat/hunger; 22-33 by scientists' counts vs Aristotle's 5",
                "hook": "you've been told X",
                "idea_source": "backlog (ideas.md \"You've been told: we have 5 senses\", the review's hook test) + viral-shaped (a school 'fact' overturned with a test you do on yourself) + unique angle (do-it-now nose test)",
                "characters": ["ved", "extra"],
                "sources": ["https://www.vice.com/en/article/humans-dont-have-5-senses-they-have-as-many-as-33/",
                            "https://www.sciencefocus.com/how-many-senses-do-we-have",
                            "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11252028/",
                            "https://www.newworldencyclopedia.org/entry/Proprioception"],
                "experiment": "'you've been told X' hook test (review 2026-11-15), 1 of 2",
                "humour": {"trend": "Tony Stark head-turn format (the sideways 'I noticed that' glance, trending early Nov 2026) as a side-eye cut-away: 'my stomach when chips open two rooms away'",
                           "beat": "side_eye", "scene": 6},
                "claims": [
                    {"claim": "the five-sense list goes back to Aristotle", "tag": "PROVEN", "source": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11252028/"},
                    {"claim": "scientists count roughly 22 to 33 senses depending on how they are split (Charles Spence, Oxford)", "tag": "PROVEN",
                     "source": "https://www.vice.com/en/article/humans-dont-have-5-senses-they-have-as-many-as-33/"},
                    {"claim": "proprioception: receptors in muscles, tendons and joints tell the brain where the limbs are", "tag": "PROVEN",
                     "source": "https://www.newworldencyclopedia.org/entry/Proprioception"},
                    {"claim": "balance: fluid in the three semicircular canals of the inner ear senses rotation and keeps moving after you stop spinning", "tag": "PROVEN",
                     "source": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11252028/"},
                    {"claim": "separate receptors for temperature and pain; interoception senses heartbeat and hunger", "tag": "PROVEN",
                     "source": "https://www.sciencefocus.com/how-many-senses-do-we-have"}]},
       "thumbnail": {"title": "33 *SENSES?*", "title_y": 0.15, "title_size": 190, "max_w": 0.95, "blur": 14,
                     "glow": "#ffcf5a", "glow_x": 0.5, "glow_y": 0.55, "glow_strength": 1.4, "bg_saturation": 1.5,
                     "tint": ["#1f4fb8", "#f08a24"], "tint_amount": 0.35,
                     "bg": [plate("park_wide")],
                     "fg": [sprite("inner_ear", 0.76, 0.5, 0.36),
                            {"type": "character", "id": "ved", "pose": "surprised", "x": 0.42, "y": 0.93, "h": 0.95, "enter": "none",
                             "acting": "none", "talk": False, "ground": False, "allow_outside_safe": True}]},
       "privacy": "public", "speaker": "ved", "assets_script": J + "assets.py", "scenes": S}
json.dump(job, open(J + "job.json", "w"), indent=1, ensure_ascii=False)
print("scenes", len(S))
