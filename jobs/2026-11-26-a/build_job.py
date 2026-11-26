"""2026-11-26-a: "Turkeys can't fly? Wild ones hit 55 mph" (myth-bust; Ved as a coach at half-time, Thanksgiving Day).
Lane: animals and nature. Explain mode: debate (two players argue, Coach Ved settles it with the tape).
Styles mixed: animated Blender shots (moving 3D: a wild turkey racing across a striped autumn field, one flapping up to roost
in an oak at sundown, a fat white farm turkey flapping and barely leaving the straw), Coach Ved's locker room (3D plates)
with two townspeople players, a Reelsmith RS-07 Chalk board, hud chips, stamps, the comic beat.
Facts (verified 2026-11-26):
- Wild turkeys can run up to 25 mph and fly up to 55 mph (PBS Nature wild turkey fact sheet; Live Science: short bursts).
- Their flights are short bursts, often around 100 yards (Popular Science).
- At sundown they fly up into trees and roost there for the night (PBS; Live Science).
- Domesticated (commercial) turkeys can't fly: bred for bigger breasts and legs, too heavy (NWTF; Live Science, Broad
  Breasted White); they weigh 20-35 lb alive at 12-16 weeks (NWTF). Wild males typically 11-24 lb (PBS).
Run after the assets exist: python jobs/2026-11-26-a/build_job.py
"""
import json, os, sys
sys.path.insert(0, os.getcwd())
from autopilot.stage import Stage

ID = "2026-11-26-a"
J = f"jobs/{ID}/"
A = J + "assets/"
SH = J + "shots/"
ST = {n: Stage(A + f"plate_{n}.json") for n in ("locker_wide", "locker_low", "locker_board")}
CAP = {"wear": "cap"}
OUT = {   # the two players: same outfits in every shot
    "max": {"skin": "#c98e62", "build": "regular", "hair": ["#2a1d17", "short"], "top": ["#d6483e", "tshirt"],
            "bottom": ["#f6efe2", "shorts"], "shoes": "#25262b"},
    "rosa": {"skin": "#8d5a3b", "build": "slim", "hair": ["#1a1410", "bun"], "top": ["#f2b04a", "tshirt"],
            "bottom": ["#34425c", "shorts"], "shoes": "#f6efe2"},
}


def plate(name, blur=0, **k):
    return {"type": "image", "path": A + f"plate_{name}.png", "x": 0.5, "y": 0.5, "w": 1.0, "enter": "none", "blur": blur, **k}


def sprite(name, x, y, w, **k):
    return {"type": "image", "path": A + name + ".png", "x": x, "y": y, "w": w, "enter": k.pop("enter", "none"), **k}


def shot(script, dur, samples=20, res=0.45):
    return {"dur": dur, "type": "blender", "script": SH + script, "x": 0.5, "y": 0.5, "w": 1.0, "h": 1.0, "enter": "none",
            "fps": 15, "res": res, "samples": samples}


def txt(t, y, size=92, **k):
    return {"type": "text", "text": t, "font": "display", "x": 0.5, "y": y, "size": size, "max_w": 0.88,
            "stroke": "#0b0f12", "stroke_width": 7, **k}


def ved(set_, wx, wy, acting, walk=None, hops=None, **k):
    st = ST[set_]
    p = st.place(wx, wy, "ved")
    L = {"type": "character", "id": "ved", "pose": acting[0][0], "x": p["x"], "y": p["y"], "h": p["h"], "enter": "none",
         "acting": acting, "allow_outside_safe": True}
    if walk:
        L["keys"] = st.walk(walk, p, "ved")
    if hops:
        L["hops"] = hops
    L.update(k)
    return L


def person(set_, who, wx, wy, acting, walk=None, hops=None, **k):
    st = ST[set_]
    p = st.place(wx, wy, "extra")
    L = {"type": "character", "id": "extra", "pose": acting[0][0], "x": p["x"], "y": p["y"], "h": p["h"],
         "enter": "none", "acting": acting, "talk": False, "rig_args": {"outfit": OUT[who]}, "allow_outside_safe": True}
    if walk:
        L["keys"] = st.walk(walk, p, "extra")
    if hops:
        L["hops"] = hops
    L.update(k)
    return L


def close_ved(acting, **k):
    return {"type": "character", "id": "ved", "pose": acting[0][0], "x": 0.5, "y": 0.8, "h": 1.06, "enter": "none",
            "acting": acting, "ground": False, "allow_outside_safe": True, **k}


S = []
# 0. hook (moving 3D): a wild turkey races across the striped field; the myth at frame 0; BUSTED slams in
S.append({"say": "Turkeys can't fly? *Wrong.* Wild ones hit *55 miles an hour*.",
          "layers": [shot("a_fly.py", 5.4),
                     txt("MYTH: TURKEYS CAN'T *FLY*", 0.15, 96, enter="none"),
                     {"type": "stamp", "text": "BUSTED", "tone": "red", "angle": -7, "size": 72, "x": 0.5, "y": 0.29,
                      "at": 1.5, "sfx": "thud"}]})
# 1. locker room, wide: half-time; Max insists they can't; Coach Ved walks in to his tactics board (cap on)
S.append({"say": "Half-time debate. Max swears turkeys *can't* fly.",
          "transition": "slide_left", "caption_y": 0.72,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.5, "zoom": 1.07, "focus": [0.5, 0.5]}]},
          "layers": [plate("locker_wide"),
                     person("locker_wide", "rosa", 1.3, 0.35, [["idle", 0], ["shrug", 1.2]]),
                     person("locker_wide", "max", 0.65, 0.1, [["explain", 0], ["point", 1.0]]),
                     ved("locker_wide", -0.55, 0.2, [["idle", 0], ["explain", 1.3]],
                         walk=[(0, -1.8, 0.2), (1.1, -0.55, 0.2)], rig_args=CAP)]})
# 2. low angle: Mia says they can; Ved points to the tape
S.append({"say": "Rosa thinks they *can*. Coach? Roll the tape.",
          "transition": "cut", "sfx": "whoosh", "caption_y": 0.72,
          "camera": {"keys": [{"t": 0, "zoom": 1.1, "focus": [0.42, 0.5]}, {"t": 3.0, "zoom": 1.1, "focus": [0.58, 0.5]}]},
          "layers": [plate("locker_low"),
                     person("locker_low", "max", 0.9, 1.1, [["idle", 0], ["shrug", 1.4]]),
                     person("locker_low", "rosa", 1.6, 1.25, [["point", 0], ["cheer", 1.3]], hops=[[1.3, 0.05, 0.4]]),
                     ved("locker_low", 0.05, 0.55, [["explain", 0], ["point", 1.6]], rig_args=CAP)]})
# 3. RS-07 Chalk on the coach's board: the numbers
S.append({"say": "They run *25*, and fly *100-yard* bursts at *55*.",
          "transition": "zoom", "caption_y": 0.74, "pad": 0.6,
          "layers": [{"type": "look", "look": "RS-07", "x": 0.5, "y": 0.5, "w": 1.0, "h": 1.0, "at": 0.0,
                      "props": {"title": "WILD TURKEY", "lines": ["RUN: 25 MPH", "FLY: 55 MPH", "@y:~100 YARDS A BURST"],
                                "answer": "THEY FLY"}}]})
# 4. moving 3D: sundown, one flaps up into the oak to sleep
S.append({"say": "And every night, they flap up into *trees* to sleep.",
          "transition": "cut", "sfx": "whoosh", "caption_y": 0.74,
          "layers": [shot("b_roost.py", 4.0),
                     {"type": "hud", "label": "every night", "text": "ROOST IN TREES", "x": 0.5, "y": 0.13, "at": 0.4,
                      "enter": "pop", "sfx": "click", "tone": "green"}]})
# 5. close at the board: Ved gives Jay his point; the farm turkey drops in
S.append({"say": "But Max is half right. *Farm* turkeys can't.",
          "transition": "cut", "caption_y": 0.72,
          "layers": [plate("locker_board", keys=[{"t": 0, "scale": 1.0}, {"t": 3.0, "scale": 1.06}]),
                     sprite("farm_turkey", 0.7, 0.5, 0.42, enter="drop", at=1.2, sfx="pop"),
                     dict(close_ved([["explain", 0], ["point", 1.3]]), x=0.3, y=1.0, h=0.72)]})
# 6. moving 3D: the farm turkey flaps with all it has and barely leaves the straw
S.append({"say": "They're bred so heavy, *20 to 35 pounds*, they can't take off.",
          "transition": "cut", "sfx": "whoosh", "caption_y": 0.74,
          "layers": [shot("c_farm.py", 4.4),
                     {"type": "hud", "label": "farm turkey", "text": "20-35 LB", "x": 0.5, "y": 0.13, "at": 0.5,
                      "enter": "pop", "sfx": "click", "tone": "red"}]})
# 7. comic beat: deadpan cut-away
S.append({"dur": 1.6, "transition": "cut", "captions": False,
          "layers": [plate("locker_board", blur=10, keys=[{"t": 0, "scale": 1.2}]), dict(close_ved([["deadpan", 0]]), acting="none")],
          "beat": {"kind": "deadpan", "at": 0.1, "dur": 1.45, "who": "ved",
                   "text": "farm turkey: all leg day, *no wing day*", "text_y": 0.2, "sfx": "scratch"}})
# 8. low angle: the ruling; Mia cheers, Jay slumps
S.append({"say": "Ruling: wild turkeys *fly*.",
          "transition": "cut", "sfx": "whoosh", "caption_y": 0.72,
          "layers": [plate("locker_low"),
                     person("locker_low", "max", 0.9, 1.1, [["sad", 0]]),
                     person("locker_low", "rosa", 1.6, 1.25, [["cheer", 0.2]], hops=[[0.4, 0.06, 0.4]]),
                     ved("locker_low", 0.05, 0.55, [["point", 0], ["warm", 1.0]], hops=[[0.3, 0.05, 0.4]])]})
# 9. payoff, wide: the one on your plate never could; MYTH BUSTED
S.append({"say": "The one on your plate? It *never* could.",
          "transition": "cut", "caption_y": 0.72, "pad": 0.7,
          "camera": {"keys": [{"t": 0, "zoom": 1.08, "focus": [0.5, 0.5]}, {"t": 3.5, "zoom": 1.0, "focus": [0.5, 0.5]}]},
          "layers": [plate("locker_wide"),
                     person("locker_wide", "rosa", 1.3, 0.35, [["happy", 0]]),
                     person("locker_wide", "max", 0.65, 0.1, [["shrug", 0]]),
                     ved("locker_wide", -0.55, 0.2, [["explain", 0], ["smirk", 2.0]]),
                     {"type": "stamp", "text": "MYTH BUSTED", "tone": "green", "angle": -6, "size": 70, "x": 0.5, "y": 0.2,
                      "at": 0.5, "sfx": "thud"}]})

SRC = ["https://www.pbs.org/wnet/nature/blog/wild-turkey-fact-sheet",
       "https://www.livescience.com/32868-five-fascinating-turkey-truths.html",
       "https://www.popsci.com/science/why-are-turkeys-so-big/",
       "https://www.nwtf.org/content-hub/domestic-vs-wild-turkeys"]
job = {"id": ID, "title": "Turkeys can't fly? Wild ones hit 55 mph 🦃",
       "description": "Happy Thanksgiving! Wild turkeys can run up to 25 mph and fly in short bursts at up to 55 mph, often "
                      "about 100 yards at a time, and every night they fly up into trees to roost. The turkey on your plate is "
                      "a different story: farm turkeys are bred for bigger breasts and legs, weigh about 20-35 lb alive, and "
                      "are too heavy to fly.\n\n"
                      "Sources: PBS Nature (wild turkey fact sheet); Live Science; Popular Science; National Wild Turkey "
                      "Federation.",
       "tags": ["turkey", "wild turkey", "can turkeys fly", "Thanksgiving", "animals", "birds", "nature", "myth busting",
                "science explained"],
       "hashtags": ["#animals", "#thanksgiving"],
       "instagram": {"hashtags": ["#animals", "#wildturkey", "#thanksgiving", "#birds", "#explained"]},
       "meta": {"format": "myth-bust",
                "topic": "can turkeys fly: wild turkeys run up to 25 mph and fly short bursts up to 55 mph (~100 yards), roost "
                         "in trees at night; farm turkeys bred for bigger breasts/legs, 20-35 lb alive, can't fly",
                "hook": "myth-bust",
                "idea_source": "trending + viral-shaped: posted on US Thanksgiving Day (most viewers are American), a myth "
                               "almost everyone believes, flipped with one number; lane animals and nature",
                "lane": "animals and nature", "role": "coach", "explain": "debate",
                "role_visual": "Coach Ved's locker room: teal lockers, bench with a football, a tactics board of X's and O's "
                               "(the RS-07 chalk scene is that board), cap on in two scenes; two players "
                               "in jerseys argue and he rules after 'rolling the tape'",
                "styles": ["blender-3d", "locker-room", "RS-07", "hud", "stamp", "comic"],
                "characters": ["ved", "extra"],
                "sources": SRC,
                "humour": {"trend": "timeless US gym card (no rising US meme fit cleanly this week): "
                                    "\"farm turkey: all leg day, no wing day\"",
                           "beat": "deadpan", "scene": 7},
                "claims": [
                    {"claim": "wild turkeys run up to 25 mph and fly up to 55 mph", "tag": "PROVEN", "source": SRC[0]},
                    {"claim": "turkey flights are short bursts, often around 100 yards", "tag": "PROVEN", "source": SRC[2]},
                    {"claim": "wild turkeys fly up into trees to roost at night", "tag": "PROVEN", "source": SRC[0]},
                    {"claim": "farm turkeys are bred for bigger breasts and legs and are too heavy to fly", "tag": "PROVEN", "source": SRC[3]},
                    {"claim": "farm turkeys weigh 20-35 lb alive at 12-16 weeks", "tag": "PROVEN", "source": SRC[3]}]},
       "thumbnail": {"title": "TURKEYS *FLY?*", "title_y": 0.2, "title_size": 165, "max_w": 0.95, "blur": 14,
                     "glow": "#f2b04a", "glow_x": 0.5, "glow_y": 0.5, "glow_strength": 1.2, "bg_saturation": 1.3,
                     "tint": ["#1c3f73", "#e0702e"], "tint_amount": 0.22,
                     "bg": [plate("locker_wide")],
                     "fg": [sprite("wild_turkey", 0.26, 0.45, 0.46, rotate=-8),
                            {"type": "character", "id": "ved", "pose": "surprised", "x": 0.62, "y": 0.95, "h": 0.95, "enter": "none",
                             "acting": "none", "talk": False, "ground": False, "allow_outside_safe": True}]},
       "privacy": "public", "speaker": "ved", "assets_script": J + "assets.py", "scenes": S}
json.dump(job, open(J + "job.json", "w"), indent=1, ensure_ascii=False)
print("scenes", len(S))
