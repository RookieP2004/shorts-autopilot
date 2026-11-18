"""DEMO 2026-11-18-motion (private, not posted): Remotion + GSAP + three.js clips (`motion` layers) mixed into the house
style: Ved in the town, townspeople, house captions, cream cards, the comic beat, one night beat. Numbers illustrative.
Run: python jobs/2026-11-18-motion/build_job.py
"""
import json, os, sys
sys.path.insert(0, os.getcwd())
from autopilot.stage import Stage

ID = "2026-11-18-motion"
J = f"jobs/{ID}/"
M = "jobs/2026-11-08-m3/assets/"
N = "jobs/2026-11-16-n/assets/"


def plate(path, blur=0, **k):
    return {"type": "image", "path": path + ".png", "x": 0.5, "y": 0.5, "w": 1.0, "enter": "none", "blur": blur, **k}


def at(pl, who, wx, wy, acting, outfit=None, **k):
    p = Stage(pl + ".json").place(wx, wy, who)
    L = {"type": "character", "id": who, "pose": acting[0][0], "x": p["x"], "y": p["y"], "h": p["h"], "enter": "none",
         "acting": acting, "allow_outside_safe": True, **k}
    if who == "extra":
        L.update(talk=False, rig_args={"outfit": outfit})
    return L


def close_ved(acting, x=0.5, y=0.8, h=1.06, **k):
    return {"type": "character", "id": "ved", "pose": acting[0][0], "x": x, "y": y, "h": h, "enter": "none", "acting": acting,
            "ground": False, "allow_outside_safe": True, **k}


def motion(comp, props, x=0.5, y=0.5, w=1.0, h=1.0, at_=0.0, **k):
    return {"type": "motion", "comp": comp, "props": props, "x": x, "y": y, "w": w, "h": h, "at": at_, "enter": "none", **k}


SELLER = {"skin": "#a8693f", "build": "round", "hair": ["#1a1410", "short"], "top": ["#e9e6df", "apron"],
          "bottom": ["#3a3e48", "trousers"], "shoes": "#25262b"}
S = []
S.append({"say": "Why does your cup of chai cost more every single year?", "layers": [
    plate(M + "plate_market_mid"),
    at(M + "plate_market_mid", "extra", -0.6, -0.9, [["idle", 0], ["happy", 2.0]], SELLER),
    at(M + "plate_market_mid", "ved", 0.55, -1.3, [["surprised", 0], ["point", 1.8]]),
    motion("KineticTitle", {"lines": ["WHY IS MY", "*CHAI* COSTLIER?"], "size": 150, "y": 0.2, "style": "rise"})]})
S.append({"say": "Same cup, same stall. But the price only goes one way.", "transition": "push", "transition_frames": 12, "layers": [
    plate(M + "plate_market_mid", blur=6),
    motion("Hero3D", {"object": "coin", "spin": 720, "zoom": 0.7}, x=0.34, y=0.6, w=0.62, h=0.34),
    {"type": "hud", "label": "price of one chai", "steps": [[0, 10], [0.9, 15]], "prefix": "₹", "tone": "gold", "x": 0.5,
     "y": 0.24, "enter": "pop", "width_of": "₹15"},
    close_ved([["explain", 0]], x=0.8, y=0.93, h=0.62)]})
S.append({"say": "Prices rise a little, every year. It adds up fast.", "transition": "cut", "layers": [
    plate(M + "plate_market_wide"),
    motion("Hero3D", {"object": "bars", "values": [10, 10.5, 11, 11.6, 12.2, 12.8, 13.4, 14.1, 14.8],
                      "colors": ["#4aa3ff"] * 8 + ["#f4c04e"], "zoom": 1.05}, x=0.5, y=0.36, w=1.0, h=0.5),
    {"type": "eqbar", "keys": [[0.4, "₹10 × 1.05^8 ≈ *₹15*"]], "tone": "gold", "x": 0.5, "y": 0.66, "enter": "fade"},
    at(M + "plate_market_wide", "ved", 1.6, -2.6, [["explain", 0]])]})
S.append({"say": "More money chasing the same goods means higher prices.", "transition": "cut", "layers": [
    plate(M + "plate_market_close", blur=10),
    motion("FlowDiagram", {"nodes": [{"id": "m", "label": "MORE MONEY", "x": 0.33, "y": 0.2},
                                     {"id": "g", "label": "SAME GOODS", "x": 0.64, "y": 0.56},
                                     {"id": "p", "label": "HIGHER PRICES", "x": 0.38, "y": 0.72, "color": "#ffd9d2"}],
                           "edges": [["m", "g"], ["g", "p"]], "step": 0.55}),
    close_ved([["explain", 0], ["point", 1.6]], x=0.82, y=0.93, h=0.6)]})
S.append({"dur": 1.6, "captions": False, "transition": "cut", "layers": [plate(M + "plate_market_mid", blur=12, keys=[{"t": 0, "scale": 1.3}]),
          dict(close_ved([["side_eye", 0]]), acting="none")],
          "beat": {"kind": "side_eye", "at": 0.1, "dur": 1.4, "who": "ved", "text": "chai wala every year:\n*just ₹1 more, beta*", "text_y": 0.2}})
S.append({"say": "And when the rupee weakens, everything we import gets pricier too.", "look": "night", "transition": "push",
          "transition_frames": 12, "layers": [
    plate(N + "plate_arena_hero", blur=10),
    motion("Hero3D", {"object": "globe", "arcs": [[19, 73, 25, 55], [19, 73, 51, 0], [19, 73, 1, 104], [19, 73, 40, -74]],
                      "tone": "#e0b25a"}, x=0.5, y=0.4, w=1.0, h=0.56),
    {"type": "dottext", "text": "IMPORTS: *PRICIER*", "size": 56, "x": 0.5, "y": 0.7, "at": 0.8, "accent": "red"},
    close_ved([["explain", 0]], x=0.84, y=0.93, h=0.5)]})
S.append({"say": "Follow for more everyday money, explained.", "transition": "cut", "min_dur": 2.8, "layers": [
    plate(M + "plate_market_mid", blur=12),
    close_ved([["point", 0], ["smirk", 1.6]]),
    motion("KineticTitle", {"lines": ["FOLLOW FOR", "*MORE*"], "size": 140, "y": 0.2, "style": "pop"})]})

job = {"id": ID, "title": "DEMO motion engine", "description": "demo (not posted)", "tags": [], "privacy": "private",
       "speaker": "ved", "meta": {"format": "demo", "humour": {"beat": "side_eye", "scene": 4}}, "scenes": S}
for sc in S:
    if "say" in sc:
        sc.setdefault("pad", 0.14)
json.dump(job, open(J + "job.json", "w"), indent=1, ensure_ascii=False)
print("scenes", len(S))
