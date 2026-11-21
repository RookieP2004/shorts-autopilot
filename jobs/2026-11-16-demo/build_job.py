"""Mock-up stills (not a real video): how the three kinds of Short look with the mixed style (owner asked 2026-11-16).
Example 1 = town explainer, example 2 = what-if with a night reveal, example 3 = dark-files in the night look.
Run: python jobs/2026-11-16-demo/build_job.py   (writes job_town.json and job_night.json; preview with `frames`)
"""
import json, os, sys
sys.path.insert(0, os.getcwd())
from autopilot.stage import Stage

D = "jobs/2026-11-16-demo/"
M = "jobs/2026-11-08-m3/assets/"
L = "jobs/2026-11-14-b/assets/"
N = "jobs/2026-11-16-n/assets/"
AN = "font-family='Anton, DejaVu Sans, sans-serif'"


def plate(path, blur=0, **k):
    return {"type": "image", "path": path + ".png", "x": 0.5, "y": 0.5, "w": 1.0, "enter": "none", "blur": blur, **k}


def at(plate_json, who, wx, wy, acting, outfit=None, **k):
    p = Stage(plate_json + ".json").place(wx, wy, who)
    Lr = {"type": "character", "id": who, "pose": acting[0][0], "x": p["x"], "y": p["y"], "h": p["h"], "enter": "none",
          "acting": acting, "allow_outside_safe": True, **k}
    if who == "extra":
        Lr.update(talk=False, rig_args={"outfit": outfit})
    return Lr


def close_ved(acting, x=0.5, y=0.8, h=1.06, **k):
    return {"type": "character", "id": "ved", "pose": acting[0][0], "x": x, "y": y, "h": h, "enter": "none", "acting": acting,
            "ground": False, "allow_outside_safe": True, **k}


def card(text, x, y, w=0.8, at_=0.2, color="#1a1410", size=74, rot=-2):
    lines = text.split("\n")
    H = 60 + 90 * len(lines)
    body = "".join(f"<text x='450' y='{100 + i * 90}' text-anchor='middle' font-size='{size}' fill='{color}' {AN}>{ln}</text>"
                   for i, ln in enumerate(lines))
    svg = (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 900 {H}'><rect x='6' y='6' width='888' height='{H - 12}' rx='34' "
           f"fill='#f6efe2' stroke='#1a1410' stroke-width='7'/>{body}</svg>")
    return {"type": "image", "svg": svg, "x": x, "y": y, "w": w, "enter": "pop", "at": at_, "rotate": rot, "sfx": "pop"}


SELLER = {"skin": "#a8693f", "build": "round", "hair": ["#1a1410", "short"], "top": ["#e9e6df", "apron"],
          "bottom": ["#3a3e48", "trousers"], "shoes": "#25262b"}
BUYER = {"skin": "#d9a27a", "build": "slim", "hair": ["#2a2320", "bun"], "top": ["#2f8f5a", "shirt"],
         "bottom": ["#23262d", "trousers"], "shoes": "#151515"}
BROKER1 = {"skin": "#c68a5e", "build": "regular", "hair": ["#1a1410", "short"], "top": ["#2f3a52", "jacket"],
           "bottom": ["#23262d", "trousers"], "shoes": "#151515"}
BROKER2 = {"skin": "#8d5a3b", "build": "round", "hair": ["#1a1410", "short"], "top": ["#e9e6df", "shirt"],
           "bottom": ["#3a3e48", "trousers"], "shoes": "#151515", "hat": ["cap", "#d63a2f"]}

T = []
# ---- Example 1: town explainer "why does your chai cost more?"
T.append({"say": "Why does your cup of chai cost more every year?", "layers": [
    plate(M + "plate_market_mid"),
    at(M + "plate_market_mid", "extra", -0.6, -0.9, [["idle", 0]], SELLER),
    at(M + "plate_market_mid", "ved", 0.55, -1.3, [["surprised", 0]]),
    card("WHY IS MY CHAI\n₹5 MORE?", 0.5, 0.22, at_=0.1)]})
T.append({"say": "Same cup. Same stall. But the price keeps ticking up.", "layers": [
    plate(M + "plate_market_mid"),
    at(M + "plate_market_mid", "extra", -0.6, -0.9, [["happy", 0]], SELLER),
    at(M + "plate_market_mid", "extra", 0.1, -0.5, [["hold", 0]], BUYER),
    at(M + "plate_market_mid", "ved", 0.75, -1.4, [["point", 0]]),
    {"type": "hud", "label": "price of one chai", "steps": [[0, 10], [0.8, 15]], "prefix": "₹", "tone": "gold", "x": 0.5, "y": 0.2,
     "enter": "pop", "width_of": "₹15"},
    {"type": "tag", "text": "ILLUSTRATIVE NUMBERS", "x": 0.5, "y": 0.3, "at": 0.3, "size": 26}]})
T.append({"say": "Picture a thousand shoppers. Each year, a few more can't afford their usual cup.", "layers": [
    plate(M + "plate_market_wide"),
    {"type": "crowd", "plate": M + "plate_market_wide.json", "area": [-2.4, 2.4, -2.3, 0.4], "n": 1000, "fig_h": 0.34,
     "color": "#f6efe2", "in_dur": 0, "seed": 2,
     "steps": [{"at": 0, "split": "x", "colors": ["blue", "blue", "blue", "blue", "red"], "dur": 0}, {"at": 0, "keep": 0, "dur": 0},
               {"at": 0.2, "color": "blue", "dur": 0}]},
    at(M + "plate_market_wide", "ved", 1.6, -2.6, [["explain", 0]]),
    {"type": "hud", "label": "can still afford it", "steps": [[0, 1000], [0.6, 800]], "tone": "blue", "x": 0.5, "y": 0.2, "enter": "pop"},
    {"type": "eqbar", "keys": [[0.1, "₹10 × 1.05^8 ≈ *₹15*"]], "tone": "gold", "x": 0.5, "y": 0.3, "enter": "fade"}]})
T.append({"say": "More money chasing the same goods means higher prices.", "layers": [
    plate(M + "plate_market_close", blur=8),
    close_ved([["explain", 0]], x=0.78, y=0.92, h=0.7),
    card("1. MORE MONEY", 0.42, 0.24, w=0.7, at_=0.1, rot=-3),
    card("2. SAME GOODS", 0.42, 0.37, w=0.7, at_=0.3, rot=2),
    card("3. HIGHER PRICES", 0.42, 0.5, w=0.7, at_=0.5, color="#d63a2f", rot=-2),
    {"type": "tracker", "n": 3, "done": [0.2, 0.4, 0.6], "x": 0.42, "y": 0.62, "enter": "none"}]})
T.append({"dur": 1.6, "captions": False, "layers": [plate(M + "plate_market_mid", blur=12), dict(close_ved([["side_eye", 0]]), acting="none")],
          "beat": {"kind": "side_eye", "at": 0.1, "dur": 1.4, "who": "ved", "text": "chai wala every year:\n*just ₹1 more, beta*", "text_y": 0.2}})
# ---- Example 2: what-if "IQ 300" (town lab + a night reveal)
T.append({"say": "What if your IQ was three hundred?", "layers": [
    plate(L + "plate_lab_wide"),
    at(L + "plate_lab_wide", "ved", 0.6, -1.9, [["welcome", 0]]),
    card("WHAT IF YOUR\nIQ WAS 300?", 0.5, 0.2, at_=0.1, size=80)]})
T.append({"say": "Line up ten thousand people. Not one would think like you.", "layers": [
    plate(L + "plate_lab_wide"),
    {"type": "crowd", "plate": L + "plate_lab_wide.json", "area": [-2.4, 2.4, -2.2, 0.6], "n": 2400, "fig_h": 0.3, "color": "#f6efe2",
     "in_dur": 0, "seed": 5,
     "steps": [{"at": 0, "split": "x", "colors": ["blue"] * 24, "dur": 0}, {"at": 0, "keep": 12, "dur": 0, "lost": "grey"},
               {"at": 0, "split": "y", "colors": ["blue"] * 100, "dur": 0}, {"at": 0, "keep": 60, "dur": 0, "lost": "grey"},
               {"at": 0.2, "glow": "green", "dur": 0.3}]},
    at(L + "plate_lab_wide", "ved", 1.5, -2.5, [["surprised", 0]]),
    {"type": "hud", "label": "people in the line", "value": 10000, "tone": "blue", "x": 0.5, "y": 0.2, "enter": "pop"},
    {"type": "optcard", "label": "thinks like you", "text": "ZERO", "tone": "green", "x": 0.5, "y": 0.33, "w": 0.36, "enter": "pop", "at": 0.3}]})
T.append({"say": "Every choice would branch into ideas no one else can follow.", "layers": [
    plate(L + "plate_lab_mid", blur=10),
    {"type": "nodes", "x": 0.45, "y": 0.42, "yaw": [-16, 10],
     "nodes": [{"id": "r", "pos": [0, 1.6, 0], "at": 0, "tone": "blue", "label": "1 question"},
               {"id": "a", "pos": [-1.5, 0.4, 0.3], "at": 0.2, "tone": "green"}, {"id": "b", "pos": [0, 0.4, -0.4], "at": 0.2, "tone": "green"},
               {"id": "c", "pos": [1.5, 0.4, 0.2], "at": 0.2, "tone": "green"},
               {"id": "d", "pos": [-2.0, -0.8, 0.5], "at": 0.4, "tone": "gold"}, {"id": "e", "pos": [-0.9, -0.8, 0.0], "at": 0.4, "tone": "gold"},
               {"id": "f", "pos": [0.4, -0.8, -0.3], "at": 0.4, "tone": "gold"}, {"id": "g", "pos": [1.9, -0.8, 0.4], "at": 0.4, "tone": "gold", "label": "100 ideas"}],
     "edges": [["r", "a", 0.2, "green"], ["r", "b", 0.2, "green"], ["r", "c", 0.2, "green"], ["a", "d", 0.4, "gold"],
               ["a", "e", 0.4, "gold"], ["b", "f", 0.4, "gold"], ["c", "g", 0.4, "gold"]]},
    close_ved([["explain", 0]], x=0.82, y=0.92, h=0.62)]})
T.append({"say": "But would anyone understand you?", "look": "night", "layers": [
    plate(N + "plate_arena_hero"),
    at(N + "plate_arena_hero", "ved", 0.4, -0.6, [["serious", 0]]),
    {"type": "stamp", "text": "LONELY AT THE TOP?", "tone": "red", "angle": -8, "size": 92, "x": 0.5, "y": 0.27, "at": 0.2}]})

N_ = []
# ---- Example 3: dark files (night look) "how hawala moves money without moving money"
CHAT = {"kind": "chat", "name": "Rafiq Bhai", "sub": "online", "msgs": [
    {"text": "Need to send 1 lakh to Dubai today", "side": "out", "time": "8:02"},
    {"text": "Give cash here. Your cousin collects there in 1 hour. Code word: KITE", "time": "8:03"}]}
N_.append({"say": "How do you send money abroad without sending any money?", "layers": [
    plate(N + "plate_arena_hero"),
    at(N + "plate_arena_hero", "ved", 1.0, -1.2, [["explain", 0]]),
    {"type": "phone", "sprite": N + "phone.png", "screen": CHAT, "x": 0.34, "y": 0.45, "w": 0.44, "tilt": [[0, -16, 5], [3, 8, 2]], "enter": "rise"}]})
N_.append({"say": "Two brokers, two cities. The cash never crosses the border. Only trust does.", "layers": [
    plate(N + "plate_arena_mid"),
    at(N + "plate_arena_mid", "extra", -1.6, 0.6, [["idle", 0]], BROKER1),
    at(N + "plate_arena_mid", "extra", 2.4, -0.2, [["idle", 0]], BROKER2),
    at(N + "plate_arena_mid", "ved", 0.5, -1.4, [["explain", 0]]),
    {"type": "nodes", "x": 0.5, "y": 0.36, "yaw": [0, 0], "cam": {"pitch": 0},
     "nodes": [{"id": "m", "pos": [-1.9, 0, 0], "at": 0, "tone": "blue", "label": "MUMBAI", "label_side": "right"},
               {"id": "d", "pos": [1.9, 0, 0], "at": 0, "tone": "blue", "label": "DUBAI", "label_side": "left"}],
     "edges": [["m", "d", 0.2, "gold"]]},
    card("NO TRANSFER.\nJUST TRUST.", 0.5, 0.2, w=0.7, at_=0.3, size=70)]})
N_.append({"say": "Is it legal in India? No.", "layers": [
    plate(N + "plate_arena_hero"),
    at(N + "plate_arena_hero", "ved", 1.0, -1.2, [["crossed", 0]]),
    {"type": "optcard", "label": "legal in India?", "text": "NO", "sub": "FEMA · PMLA", "tone": "blue", "x": 0.36, "y": 0.32, "w": 0.44,
     "verdict": "cross", "verdict_at": 0.2, "enter": "pop"},
    {"type": "stamp", "text": "ILLEGAL", "tone": "red", "angle": -10, "size": 110, "x": 0.38, "y": 0.52, "at": 0.4},
    {"type": "tag", "text": "SOURCE: FEMA 1999, PMLA 2002", "x": 0.5, "y": 0.66, "at": 0.4, "size": 26}]})
N_.append({"say": "Ever got a message like this? Comment YES or NO.", "layers": [
    plate(N + "plate_arena_hero", blur=16),
    {"type": "phone", "sprite": N + "phone.png", "x": 0.5, "y": 0.5, "w": 0.6, "tilt": [[0, 6, 4]], "enter": "rise",
     "screen": {"kind": "lock", "time": "8:04", "date": "Friday", "cta": "Comment YES or NO", "cta_at": 0.2,
                "notes": [{"app": "Rafiq Bhai", "title": "Code word: KITE", "body": "Collect at the shop near the market, 1 hour."}]}},
    close_ved([["point", 0]], x=0.85, y=0.92, h=0.5)]})

base = {"privacy": "private", "speaker": "ved", "description": "mock-up", "tags": [], "meta": {"format": "demo", "humour": {"beat": "side_eye", "scene": 4}}}
for name, scenes, extra_keys in (("job_town.json", T, {}), ("job_night.json", N_, {"look": "night"})):
    for s in scenes:
        if "say" in s:
            s.setdefault("pad", 0.14)
    job = dict(base, id="2026-11-16-demo", title="demo", scenes=scenes, **extra_keys)
    json.dump(job, open(D + name, "w"), indent=1, ensure_ascii=False)
print("ok")
