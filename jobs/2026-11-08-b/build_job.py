"""2026-11-08-b: myth-bust "Do we only use 10% of our brain?" Lab + night-town sets (Blender stills), 2D Ved and townspeople.
python jobs/2026-11-08-b/build_job.py"""
import json, os, random, sys
sys.path.insert(0, os.getcwd())
from autopilot.stage import Stage

random.seed(7)
J = "jobs/2026-11-08-b/"
A = J + "assets/"
SRC = A if os.path.exists(A + "plate_town_all.json") else "/tmp/claude-0/bpv/"
ST = {n: Stage(SRC + f"plate_{n}.json") for n in ("lab_wide", "lab_mid", "lab_close", "town_west")}
ST["town_east"] = ST["town_all"] = ST["town_west"]

OUT = {   # same people as the market town
    "nia": {"skin": "#a8704e", "hair": ["#140f0c", "bun"], "top": ["#f6efe2", "jacket"], "bottom": ["#34425c", "trousers"],
            "earrings": "#6fc3c0"},
    "amina": {"skin": "#8d5a3b", "hat": ["headscarf", "#d9534f"], "top": ["#f2b04a", "dress"], "necklace": "#6fc3c0",
              "earrings": "#f2b04a", "bag": "#8a5a3c", "hair": ["#140f0c", "long"]},
    "tomas": {"skin": "#e2b48d", "hat": ["straw", "#e6c27a"], "top": ["#6fc3c0", "tshirt"], "bottom": ["#34425c", "shorts"], "build": "slim"},
    "ravi": {"skin": "#b97a55", "top": ["#7c2533", "kurta"], "bottom": ["#efe3c8", "trousers"], "hair": ["#2a2320", "curly"]},
    "lena": {"skin": "#e6b996", "top": ["#9b59b6", "dress"], "hair": ["#6b4423", "bun"], "earrings": "#f2b04a"},
}

def plate(name, blur=0, **k):
    return {"type": "image", "path": A + f"plate_{name}.png", "x": 0.5, "y": 0.5, "w": 1.0, "enter": "none", "blur": blur, **k}

def sprite(name, x, y, w, **k):
    return {"type": "image", "path": A + name + ".png", "x": x, "y": y, "w": w, "enter": k.pop("enter", "none"), **k}

def txt(t, y, size=96, **k):
    d = {"type": "text", "text": t, "font": "display", "x": 0.5, "y": y, "size": size, "max_w": 0.86,
         "stroke": "#0b0f12", "stroke_width": 7}
    d.update(k); return d

def person(set_, who, wx, wy, acting, walk=None, hops=None, **k):
    st = ST[set_]; p = st.place(wx, wy, "extra")
    L = {"type": "character", "id": "extra", "pose": acting[0][0], "x": p["x"], "y": p["y"], "h": p["h"], "enter": "none",
         "acting": acting, "talk": False, "rig_args": {"outfit": OUT[who]}, "_depth": wy, "allow_outside_safe": True}
    if walk: L["keys"] = st.walk(walk, p, "extra")
    if hops: L["hops"] = hops
    L.update(k); return L

def ved(set_, wx, wy, acting, walk=None, hops=None, **k):
    st = ST[set_]; p = st.place(wx, wy, "ved")
    L = {"type": "character", "id": "ved", "pose": acting[0][0], "x": p["x"], "y": p["y"], "h": p["h"], "enter": "none",
         "acting": acting, "_depth": wy, "allow_outside_safe": True}
    if walk: L["keys"] = st.walk(walk, p, "ved")
    if hops: L["hops"] = hops
    L.update(k); return L

def close_ved(acting, **k):
    return {"type": "character", "id": "ved", "pose": acting[0][0], "x": 0.5, "y": 0.8, "h": 1.06, "enter": "none",
            "acting": acting, "ground": False, "allow_outside_safe": True, **k}

def staged(base, people=(), top=()):
    out = list(base) + sorted(people, key=lambda L: -L["_depth"]) + list(top)
    for L in out: L.pop("_depth", None)
    return out

F = "font-family='Poppins, DejaVu Sans, sans-serif' font-weight='800'"
AN = "font-family='Anton, DejaVu Sans, sans-serif'"

def stamp(word, color="#d9534f"):
    W = 120 + 58 * len(word)
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {W} 200'><rect x='10' y='10' width='{W-20}' height='180' rx='22' "
            f"fill='#f6efe2' fill-opacity='0.85' stroke='{color}' stroke-width='14'/><rect x='30' y='30' width='{W-60}' height='140' rx='12' fill='none' "
            f"stroke='{color}' stroke-width='5'/><text x='{W/2}' y='140' text-anchor='middle' font-size='120' fill='{color}' {AN}>{word}</text></svg>")

def tag(label, color="#f2b04a"):
    w = 60 + 34 * len(label)
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {w} 96'><rect x='4' y='4' width='{w-8}' height='88' rx='44' "
            f"fill='#f6efe2' stroke='#1a1410' stroke-width='6'/><circle cx='46' cy='48' r='16' fill='{color}'/>"
            f"<text x='{(w+40)/2}' y='64' text-anchor='middle' font-size='44' fill='#1a1410' {F}>{label}</text></svg>")

meter = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 760 110'><rect x='5' y='5' width='750' height='100' rx='50' "
         "fill='#16232b' stroke='#f6efe2' stroke-width='8'/><rect x='18' y='18' width='76' height='74' rx='37' fill='#f2b04a'/>"
         f"<text x='430' y='74' text-anchor='middle' font-size='50' fill='#f6efe2' {F} opacity='0.55'>90% UNUSED?</text></svg>")

S = []
# 1. hook, lab medium: myth on screen at frame 0; Ved walks in, arms crossed
S.append({"say": "You've heard you only use *ten percent* of your brain.", "caption_y": 0.33,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.2, "zoom": 1.06, "focus": [0.45, 0.5]}]},
          "layers": staged([plate("lab_mid")],
                           [person("lab_mid", "nia", 1.45, 0.45, [["hold", 0], ["point", 1.6]]),
                            ved("lab_mid", -0.55, -1.0, [["warm", 0], ["explain", 1.2], ["crossed", 2.4]], walk=[(0, -2.4, -1.4), (1.0, -0.55, -1.0)])],
                           [txt("MYTH:", 0.085, 80, color="#d9534f", enter="none"),
                            txt("YOU ONLY USE *10%* OF YOUR BRAIN", 0.175, 92, enter="none"),
                            {"type": "image", "svg": meter, "w": 0.66, "x": 0.5, "y": 0.27, "enter": "none"}])})
# 2. close-up: busted
S.append({"say": "Nope. You use *all* of it.", "transition": "cut", "caption_y": 0.64,
          "layers": [plate("lab_mid", blur=10, keys=[{"t": 0, "scale": 1.35}, {"t": 2.2, "scale": 1.4}]),
                     close_ved([["serious", 0], ["point", 0.9]]),
                     {"type": "image", "svg": stamp("BUSTED"), "w": 0.62, "x": 0.5, "y": 0.17, "rot": -8, "at": 0.55,
                      "keys": [{"t": 0, "scale": 2.2, "opacity": 0}, {"t": 0.18, "scale": 1.0, "opacity": 1, "ease": "out"}], "sfx": "boom"}]})
# 3. lab close: the brain lights up everywhere; labelled regions
bx, by = ST["lab_close"].point(1.0, 0.6, 1.6)
labels = [("MOVING", 0.27, 0.36, "#f2b04a", 1.1), ("SEEING", 0.74, 0.37, "#6fc3c0", 1.5),
          ("MEMORY", 0.25, 0.66, "#d9534f", 1.9), ("BREATHING", 0.7, 0.68, "#9b59b6", 2.3)]
glow = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 200'><defs><radialGradient id='g'><stop offset='0' stop-color='#fff3a0'/>"
        "<stop offset='0.35' stop-color='#ffb23a' stop-opacity='0.9'/><stop offset='1' stop-color='#ff6a00' stop-opacity='0'/></radialGradient></defs>"
        "<circle cx='100' cy='100' r='100' fill='url(#g)'/></svg>")
spots = []
for i in range(16):                    # hotspots light up all over the brain (ellipse ~ x .2-.85, y .38-.63)
    while True:
        u, v = random.uniform(-1, 1), random.uniform(-1, 1)
        if u * u + v * v < 0.8: break
    spots.append({"type": "image", "svg": glow, "x": round(0.52 + 0.3 * u, 3), "y": round(0.505 + 0.115 * v, 3),
                  "w": round(random.uniform(0.16, 0.26), 3), "opacity": 0.85, "at": round(0.5 + i * 0.13, 2), "enter": "zoom",
                  "enter_dur": 0.25, "loop": "pulse", "loop_speed": random.uniform(0.6, 1.1), "loop_amp": 0.5})
lay = [plate("lab_close")] + spots + [
       {"type": "shape", "shape": "ring", "x": bx, "y": by, "w": 0.6, "h": 0.6, "color": "#ffcf73", "stroke_width": 8, "at": 0.6,
        "keys": [{"t": 0, "scale": 0.5, "opacity": 0.9}, {"t": 1.0, "scale": 1.5, "opacity": 0}], "until": 1.6}]
for name, x, y, c, t in labels:
    lay.append({"type": "image", "svg": tag(name, c), "w": 0.36, "x": x, "y": y, "enter": "pop", "at": t, "sfx": "pop"})
lay.append(txt("EVEN AT *REST*", 0.13, 100, enter="pop", at=2.9, sfx="ding"))
S.append({"say": "Brain scans light up *everywhere*, even when you're resting.", "transition": "slide_left", "caption_y": 0.24,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.5, "zoom": 1.08, "focus": [0.5, 0.52]}]},
          "layers": lay})
# 4. lab wide: 2% of the weight, 20% of the energy
card = (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 900 420'><rect width='900' height='420' rx='36' fill='#f6efe2' "
        f"stroke='#1a1410' stroke-width='6'/><text x='225' y='80' text-anchor='middle' font-size='46' fill='#1a1410' {F}>WEIGHT</text>"
        f"<text x='675' y='80' text-anchor='middle' font-size='46' fill='#1a1410' {F}>ENERGY</text>"
        "<line x1='450' y1='40' x2='450' y2='380' stroke='#1a1410' stroke-width='3' opacity='0.25'/>"
        "<rect x='95' y='300' width='260' height='40' rx='20' fill='#d8cdb8'/><rect x='95' y='300' width='16' height='40' rx='8' fill='#6fc3c0'/>"
        "<rect x='545' y='300' width='260' height='40' rx='20' fill='#d8cdb8'/><rect x='545' y='300' width='62' height='40' rx='20' fill='#f2b04a'/>"
        f"<text x='225' y='385' text-anchor='middle' font-size='30' fill='#5a4e44' {F}>of your body</text>"
        f"<text x='675' y='385' text-anchor='middle' font-size='30' fill='#5a4e44' {F}>at rest</text></svg>")
S.append({"say": "Your brain is just *2%* of your weight, but it burns about *20%* of your energy.", "transition": "cut",
          "caption_y": 0.39, "camera": {"zoom": [1.0, 1.05], "focus": [0.5, 0.5]},
          "layers": staged([plate("lab_wide")],
                           [person("lab_wide", "nia", 2.3, -0.4, [["idle", 0], ["surprised", 3.4]]),
                            ved("lab_wide", -0.6, -0.8, [["explain", 0], ["point", 1.2], ["surprised", 3.4]],
                                walk=[(0, -2.6, -1.6), (1.1, -0.6, -0.8)], hops=[[3.5, 0.03, 0.45]])],
                           [{"type": "image", "svg": card, "w": 0.84, "x": 0.5, "y": 0.2, "enter": "pop", "at": 0.2, "sfx": "pop"},
                            {"type": "counter", "from": 0, "to": 2, "suffix": "%", "count_dur": 0.6, "at": 0.9, "x": 0.29, "y": 0.205,
                             "size": 120, "color": "#34425c", "enter": "pop"},
                            {"type": "counter", "from": 0, "to": 20, "suffix": "%", "count_dur": 1.0, "at": 2.9, "x": 0.71, "y": 0.205,
                             "size": 120, "color": "#d98a1a", "enter": "pop", "sfx": "ding"}])})
# 5. the city at night: lights move district to district
S.append({"say": "Think of a city at night. Not every light is on at once...", "transition": "fade", "caption_y": 0.41,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.0, "zoom": 1.07, "focus": [0.5, 0.48]}]},
          "layers": staged([plate("town_west"), plate("town_east", keys=[{"t": 0, "opacity": 0}, {"t": 2.2, "opacity": 0}, {"t": 2.7, "opacity": 1}])],
                           [person("town_west", "amina", 1.2, -3.0, [["idle", 0]], walk=[(0, 1.3, -1.0), (4.0, 1.1, -3.4)]),
                            person("town_west", "tomas", -1.0, 1.5, [["idle", 0]], walk=[(0, -1.1, 2.5), (4.0, -0.9, 0.0)]),
                            ved("town_west", -0.8, -4.0, [["explain", 0], ["point", 1.4], ["explain", 2.8]], walk=[(0, -2.6, -4.4), (1.2, -0.8, -4.0)])],
                           [txt("YOUR BRAIN = A *CITY*", 0.12, 86, enter="pop", at=0.3, sfx="pop"),
                            txt("NOT ALL *AT ONCE*", 0.2, 80, enter="pop", at=2.5, sfx="whoosh")])})
# 6. every district gets used
S.append({"say": "...but over a day, every neighbourhood gets *busy*.", "transition": "cut",
          "camera": {"zoom": [1.07, 1.0], "focus": [0.5, 0.5]},
          "layers": staged([plate("town_all")],
                           [person("town_all", "amina", 1.1, -3.4, [["happy", 0], ["cheer", 1.0]], hops=[[1.0, 0.03, 0.45]]),
                            person("town_all", "tomas", -0.9, 0.0, [["wave", 0]], walk=[(0, -0.9, 0.0), (3.0, -0.6, -2.0)]),
                            person("town_all", "ravi", 0.5, 3.0, [["idle", 0]], walk=[(0, 1.4, 4.0), (3.0, 0.4, 1.5)]),
                            person("town_all", "lena", -1.5, -1.5, [["idle", 0], ["happy", 1.4]]),
                            ved("town_all", -0.8, -4.0, [["welcome", 0], ["point", 1.6]])],
                           [txt("EVERY DISTRICT *USED*", 0.13, 86, enter="pop", at=0.4, sfx="ding")])})
# 7. comic beat (reaction cut-away)
S.append({"dur": 1.8, "transition": "cut", "captions": False,
          "layers": [plate("town_all", blur=10, keys=[{"t": 0, "scale": 1.35}]), dict(close_ved([["idle", 0]]), acting="none")],
          "beat": {"kind": "deadpan", "at": 0.1, "dur": 1.5, "zoom": 1.15, "focus": [0.5, 0.42],
                   "text": "\"Wait, it's ALL brain?\"\n*\"Always has been.\"*", "text_y": 0.18}})
# 8. where the myth came from: a 1936 self-help book
S.append({"say": "The ten percent idea? Probably a *1936* self-help book, misquoting a *Harvard* psychologist.", "transition": "slide_left",
          "caption_y": 0.36,
          "layers": staged([plate("lab_mid")],
                           [ved("lab_mid", -0.5, -1.0, [["think", 0], ["explain", 1.6], ["shrug", 3.4]])],
                           [sprite("book", 0.5, 0.19, 0.3, at=0.3, keys=[{"t": 0, "y": -0.15, "rot": -30}, {"t": 0.6, "y": 0.19, "rot": -6, "ease": "bounce"}], sfx="whoosh"),
                            {"type": "image", "svg": stamp("MISQUOTED"), "w": 0.66, "x": 0.5, "y": 0.27, "rot": 7, "at": 3.3,
                             "keys": [{"t": 0, "scale": 2.0, "opacity": 0}, {"t": 0.18, "scale": 1.0, "opacity": 1, "ease": "out"}], "sfx": "boom"}])})
# 9. payoff close-up
S.append({"say": "So there's no secret ninety percent to unlock. You already use *all of it*.", "transition": "cut", "caption_y": 0.64,
          "layers": [plate("lab_close", blur=10, keys=[{"t": 0, "scale": 1.3}, {"t": 4, "scale": 1.38}]),
                     close_ved([["explain", 0], ["warm", 2.0], ["point", 3.0]]),
                     txt("*100%*", 0.16, 220, enter="zoom", at=3.0, sfx="ding")]})

job = {"id": "2026-11-08-b", "title": "Do we really only use 10% of our brain? 🧠",
       "description": "The 10% brain myth, busted: scans show activity all over the brain, and a 2% organ that burns 20% of your energy isn't sitting idle.\n\n"
                      "Sources:\nhttps://www.livescience.com/health/neuroscience/do-we-really-use-only-10-of-our-brains\n"
                      "https://en.wikipedia.org/wiki/Ten-percent-of-the-brain_myth\n"
                      "https://www.sciencefocus.com/author/deanburnett/news/myth-use-10-per-cent-brain",
       "tags": ["10 percent brain myth", "brain", "neuroscience", "myth busted", "psychology", "science explained", "human body", "brain facts"],
       "hashtags": ["#brain", "#science"],
       "meta": {"format": "myth-bust", "topic": "the 10% of the brain myth", "hook": "myth-bust", "idea_source": "backlog",
                "characters": ["ved", "extra"],
                "sources": ["https://www.livescience.com/health/neuroscience/do-we-really-use-only-10-of-our-brains",
                            "https://en.wikipedia.org/wiki/Ten-percent-of-the-brain_myth",
                            "https://lenz.io/c/adult-human-brain-body-weight-energy-consumption-50c89742"],
                "humour": {"trend": "'Always Has Been' format (rising on Imgflip this week), as a text card", "beat": "deadpan", "scene": 7}},
       "privacy": "public", "speaker": "ved", "assets_script": J + "assets.py", "scenes": S}
json.dump(job, open(J + "job.json", "w"), indent=1, ensure_ascii=False)
print("scenes", len(S), "using", SRC)
