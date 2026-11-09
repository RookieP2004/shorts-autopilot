"""2026-11-09-c: "Goldfish have a 3-second memory?" (myth-bust).
2D Ved + two lab scientists staged in depth inside Blender sets (fish lab, underwater tank close-up, lab floor with a target)
built from stills + cut-outs; goldfish, pellets and the fish-on-wheels cart are animated cut-outs.
Run after the assets exist (or with previews for planning): python jobs/2026-11-09-c/build_job.py
"""
import json, os, random, sys
sys.path.insert(0, os.getcwd())
from autopilot.stage import Stage

random.seed(11)
ID = "2026-11-09-c"
J = f"jobs/{ID}/"
A = J + "assets/"
SRC = A if os.path.exists(A + "plate_lab_mid.json") else "/tmp/claude-0/pv/"
ST = {n: Stage(SRC + f"plate_{n}.json") for n in ("lab_wide", "lab_mid", "lab_floor", "tank_close")}

# ---- the lab crew (same people, same outfits in every shot)
OUT = {
    "noa": {"skin": "#e6b996", "top": ["#f6efe2", "jacket"], "bottom": ["#34425c", "trousers"], "hair": ["#6b4423", "bun"],
            "earrings": "#f2b04a", "belt": "#25262b"},
    "ilan": {"skin": "#a0694a", "top": ["#f6efe2", "jacket"], "bottom": ["#25262b", "trousers"], "hair": ["#1a1410", "curly"],
             "tie": "#d9534f", "build": "round"},
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


def staged(set_, behind=(), front=(), extra_top=(), fg_layer=True):
    out = [plate(set_)] + sorted(behind, key=lambda L: -L["_depth"])
    if fg_layer:
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


def swim(path, w, t0=0, flip=False, **k):
    """A goldfish cut-out swimming along [(t, x, y), ...] with a gentle tilt; flip=True faces left."""
    t_, x0, y0 = path[0]
    keys = [{"t": 0, "x": x0, "y": y0, "rot": 0}]
    for i, (t, x, y) in enumerate(path[1:]):
        keys.append({"t": t, "x": x, "y": y, "rot": (-6 if i % 2 else 6) * (-1 if flip else 1)})
    return sprite("goldfish", x0, y0, w, at=t0, flip=flip, keys=keys, **k)


def pellets(x, y0, y1, t0, n=6, w=0.03):
    return [sprite("pellet", x + random.uniform(-0.05, 0.05), y1, w, at=t0 + i * 0.12,
                   keys=[{"t": 0, "y": y0, "x": x}, {"t": 0.9, "y": y1 + random.uniform(-0.04, 0.03),
                                                      "x": x + random.uniform(-0.08, 0.08), "ease": "out"}]) for i in range(n)]


def card(svg_body, w=900, h=150):
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {w} {h}'><rect x='5' y='5' width='{w-10}' height='{h-10}' rx='30' "
            f"fill='#f6efe2' stroke='#1a1410' stroke-width='6'/>{svg_body}</svg>")


def stamp(word, color="#d9534f", w=520):
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {w} 170'><rect x='10' y='10' width='{w-20}' height='150' rx='18' "
            f"fill='none' stroke='{color}' stroke-width='14'/><text x='{w/2}' y='128' text-anchor='middle' font-size='118' "
            f"fill='{color}' {AN}>{word}</text></svg>")


CLOCK = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 300 300'><circle cx='150' cy='150' r='138' fill='#f6efe2' stroke='#d9534f' stroke-width='16'/>"
         + "".join(f"<rect x='146' y='24' width='8' height='22' fill='#1a1410' transform='rotate({k*30} 150 150)'/>" for k in range(12))
         + "<path d='M150,150 L150,60 A90,90 0 0,1 240,150 Z' fill='#6fc3c0' opacity='0.85'/>"
         + "<rect x='144' y='92' width='12' height='62' rx='6' fill='#1a1410'/><circle cx='150' cy='150' r='12' fill='#1a1410'/></svg>")
HAND = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 300 300'><rect x='146' y='40' width='8' height='114' rx='4' fill='#d9534f'/>"
        "<circle cx='150' cy='150' r='8' fill='#d9534f'/></svg>")


def row(label, value, color, strike=False):
    s = (f"<line x1='40' y1='75' x2='860' y2='75' stroke='#d9534f' stroke-width='12' stroke-linecap='round'/>" if strike else "")
    return card(f"<text x='40' y='96' font-size='50' fill='#1a1410' {F}>{label}</text>"
                f"<text x='860' y='112' text-anchor='end' font-size='96' fill='{color}' {AN}>{value}</text>{s}")


S = []
tc = ST["tank_close"]
knob_x, knob_y = tc.point(0.45, 0.3, 1.43)
sm = ST["lab_mid"]
# 1. hook (lab mid): MYTH stamp at frame 0, Ved arms crossed in front of the tank, a goldfish crosses the tank
tank_l, tank_y = sm.point(-1.5, 0.3, 1.25)
tank_r, _ = sm.point(-0.5, 0.3, 1.25)
S.append({"say": "Goldfish have a *three-second* memory? Total myth.",
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.2, "zoom": 1.06, "focus": [0.5, 0.5]}]},
          "layers": staged("lab_mid",
                           behind=[person("lab_mid", "noa", -1.9, 1.4, [["idle", 0], ["shrug", 1.6]])],
                           front=[ved("lab_mid", -0.4, -0.5, [["crossed", 0], ["deadpan", 2.0]])],
                           extra_top=[txt("GOLDFISH HAVE A *3-SECOND* MEMORY", 0.2, 100, enter="none"),
                                      {"type": "image", "svg": stamp("MYTH"), "x": 0.5, "y": 0.1, "w": 0.42, "rotate": -6,
                                       "enter": "none", "keys": [{"t": 0, "scale": 1.0}, {"t": 2.2, "scale": 1.0}, {"t": 2.45, "scale": 1.15, "ease": "back"}]}]),
                           })
# 2. tank close: the Plymouth lever
fish_a = swim([(0, 1.15, 0.62), (1.6, 0.62, 0.58), (3.0, 0.42, 0.62)], 0.3, 0.2, flip=True)
fish_b = swim([(0, -0.2, 0.7), (2.0, 0.25, 0.66), (3.2, 0.3, 0.7)], 0.26, 0.6)
S.append({"say": "Scientists at Plymouth gave goldfish a *lever*.", "transition": "slide_left", "caption_y": 0.86,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.0, "zoom": 1.06, "focus": [0.55, 0.45]}]},
          "layers": [plate("tank_close"), fish_b, fish_a,
                     txt("PLYMOUTH *UNIVERSITY*", 0.1, 84, enter="pop", at=0.2, sfx="pop"),
                     {"type": "shape", "shape": "arrow", "x": knob_x - 0.16, "y": knob_y, "w": 0.12, "h": 0.05, "color": "accent",
                      "enter": "pop", "at": 1.4, "sfx": "pop", "loop": "pulse"}]})
# 3. tank close: push it, food drops in (a fish nudges the knob, pellets rain, the others rush up)
nudge = sprite("goldfish", knob_x - 0.12, knob_y + 0.06, 0.28, keys=[{"t": 0, "x": 0.25, "y": 0.66, "rot": -10},
               {"t": 0.8, "x": knob_x - 0.13, "y": knob_y + 0.07, "rot": -18}, {"t": 1.0, "x": knob_x - 0.1, "y": knob_y + 0.05, "rot": -22},
               {"t": 1.3, "x": knob_x - 0.16, "y": knob_y + 0.09, "rot": -10}])
rush = [swim([(0, x0, y0), (1.4, knob_x - 0.05 + dx, knob_y + 0.22 + dy)], 0.24, 1.3, flip=x0 > 0.5)
        for x0, y0, dx, dy in ((1.2, 0.74, 0.08, 0.02), (-0.2, 0.6, -0.14, 0.06))]
S.append({"say": "Push it... and *food* drops in.", "transition": "cut", "caption_y": 0.86,
          "layers": [plate("tank_close"), nudge] + rush + pellets(knob_x - 0.08, 0.2, knob_y + 0.2, 1.1, 8) + [
                     txt("PUSH = *FOOD*", 0.1, 110, enter="pop", at=1.0, sfx="ding")]})
# 4. lab mid: the catch, one hour a day (clock panel, Noa points at it)
S.append({"say": "The catch? It only worked for *one hour* a day.", "transition": "cut", "caption_y": 0.45,
          "camera": {"zoom": [1.0, 1.05], "focus": [0.5, 0.52]},
          "layers": staged("lab_mid",
                           behind=[person("lab_mid", "noa", -1.9, 1.4, [["explain", 0], ["point", 1.0]])],
                           front=[ved("lab_mid", -0.4, -0.5, [["explain", 0], ["point", 1.3], ["serious", 2.6]])],
                           extra_top=[{"type": "image", "svg": CLOCK, "x": 0.5, "y": 0.2, "w": 0.3, "enter": "pop", "at": 0.3, "sfx": "pop"},
                                      {"type": "image", "svg": HAND, "x": 0.5, "y": 0.2, "w": 0.3, "enter": "pop", "at": 0.3,
                                       "keys": [{"t": 0, "rot": 0}, {"t": 2.6, "rot": 90, "ease": "linear"}]},
                                      txt("*1 HOUR* A DAY", 0.34, 96, enter="pop", at=1.2, sfx="pop")])})
# 5. tank close: they learned the schedule and wait at the lever on time
wait = [swim([(0, x0, y0), (1.2, knob_x - 0.1 + dx, knob_y + 0.2 + dy)], 0.24, 0.9 + i * 0.25, flip=x0 > 0.5)
        for i, (x0, y0, dx, dy) in enumerate(((1.2, 0.7, 0.1, 0.0), (-0.2, 0.62, -0.15, 0.08), (1.2, 0.5, 0.02, 0.14)))]
S.append({"say": "The fish learned the schedule... and showed up *right on time*.", "transition": "cut", "caption_y": 0.86,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.6, "zoom": 1.08, "focus": [0.55, 0.42]}]},
          "layers": [plate("tank_close")] + wait + [
                     {"type": "image", "svg": CLOCK, "x": 0.2, "y": 0.13, "w": 0.22, "enter": "pop", "at": 0.1, "sfx": "pop"},
                     {"type": "image", "svg": HAND, "x": 0.2, "y": 0.13, "w": 0.22, "enter": "pop", "at": 0.1,
                      "keys": [{"t": 0, "rot": -60}, {"t": 2.2, "rot": 0, "ease": "out"}]},
                     txt("RIGHT *ON TIME*", 0.25, 92, enter="pop", at=2.3, sfx="ding")]})
# 6. infographic: 3 seconds vs months
S.append({"say": "So, three seconds? Try *at least three months*.", "transition": "zoom", "caption_y": 0.45,
          "layers": [plate("lab_mid", blur=14, keys=[{"t": 0, "scale": 1.2}]),
                     {"type": "image", "svg": row("THE MYTH", "3 SEC", "#d9534f"), "w": 0.86, "x": 0.5, "y": 0.13, "enter": "slide_right", "at": 0.2, "sfx": "pop"},
                     {"type": "image", "svg": row("THE MYTH", "3 SEC", "#d9534f", strike=True), "w": 0.86, "x": 0.5, "y": 0.13, "enter": "fade", "at": 1.0, "enter_dur": 0.1, "sfx": "pop"},
                     {"type": "image", "svg": row("REAL", "3+ MONTHS", "#46965a"), "w": 0.86, "x": 0.5, "y": 0.26, "enter": "slide_right", "at": 1.5, "sfx": "ding"},
                     {"type": "counter", "from": 3, "to": 7776000, "count_dur": 1.6, "suffix": " SECONDS", "x": 0.5, "y": 0.35, "size": 64,
                      "color": "accent", "at": 1.7, "enter": "pop"},
                     {"type": "character", "id": "ved", "pose": "point", "x": 0.5, "y": 0.72, "h": 0.42, "enter": "none",
                      "acting": [["explain", 0], ["point", 1.4], ["smirk", 2.8]], "allow_outside_safe": True}]})
# 7. lab floor: 2022, Israel, goldfish taught to drive (the cart rolls in)
sf = ST["lab_floor"]
tg_x, tg_y = sf.point(3.6, 4.0, 0.15)
car0 = (0.66, 0.70)
S.append({"say": "And in 2022, researchers in Israel taught goldfish to *drive*.", "transition": "slide_left",
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.55]}, {"t": 3.6, "zoom": 1.05, "focus": [0.5, 0.55]}]},
          "layers": clean([plate("lab_floor"),
                           person("lab_floor", "ilan", 4.0, 2.6, [["idle", 0], ["surprised", 2.2]], hops=[[2.3, 0.04, 0.4]]),
                           ved("lab_floor", 2.2, 0.6, [["warm", 0], ["surprised", 2.2], ["explain", 3.0]], hops=[[2.25, 0.05, 0.4]]),
                           sprite("fish_car", car0[0], car0[1], 0.36, at=0.3,
                                  keys=[{"t": 0, "x": -0.25, "y": car0[1] + 0.03}, {"t": 1.8, "x": car0[0], "y": car0[1], "ease": "out"}], sfx="whoosh"),
                           txt("GOLDFISH. *DRIVING.*", 0.12, 92, max_w=0.95, enter="pop", at=2.1, sfx="boom"),
                           txt("BEN-GURION UNIVERSITY, 2022", 0.172, 46, font="light", enter="fade", at=0.4, stroke_width=4)])})
# 8. comic beat: reaction cut-away (deadpan)
S.append({"dur": 1.8, "transition": "cut", "captions": False,
          "layers": [plate("lab_floor", blur=10, keys=[{"t": 0, "scale": 1.35}]), dict(close_ved([["crossed", 0]]), acting="none")],
          "beat": {"kind": "deadpan", "at": 0.1, "dur": 1.6, "zoom": 1.1, "focus": [0.5, 0.42],
                   "text": "the goldfish got its licence\nbefore *me*", "text_y": 0.18}})
# 9. lab floor: the cart steers to the target, the crew cheers
S.append({"say": "It steered its tank on wheels toward a *target*... and hit it.", "transition": "cut",
          "layers": clean([plate("lab_floor"),
                           person("lab_floor", "ilan", 4.0, 2.6, [["idle", 0], ["cheer", 2.6]], hops=[[2.7, 0.04, 0.45]]),
                           person("lab_floor", "noa", 3.0, 2.4, [["point", 0], ["happy", 2.6]], walk=[(0, 1.6, 2.6), (1.2, 3.0, 2.4)]),
                           sprite("fish_car", car0[0], car0[1], 0.36,
                                  keys=[{"t": 0, "x": car0[0], "y": car0[1], "scale": 1.0}, {"t": 1.2, "x": (car0[0] + tg_x) / 2 - 0.08, "y": (car0[1] + tg_y) / 2, "scale": 0.72},
                                        {"t": 2.5, "x": tg_x - 0.02, "y": tg_y, "scale": 0.45, "ease": "out"}]),
                           {"type": "shape", "shape": "burst", "x": tg_x, "y": tg_y - 0.08, "w": 0.3, "color": "accent", "at": 2.5, "enter": "pop", "sfx": "ding", "until": 3.6, "exit": "fade"},
                           ved("lab_floor", 2.2, 0.6, [["point", 0], ["warm", 2.6]]),
                           txt("*TARGET* HIT", 0.13, 110, enter="pop", at=2.5)])})
# 10. lab mid: where did the myth come from? nobody knows
S.append({"say": "So where did the myth come from? Nobody really knows. We just never *checked*.", "transition": "cut", "caption_y": 0.45,
          "camera": {"zoom": [1.05, 1.0], "focus": [0.5, 0.52]},
          "layers": staged("lab_mid",
                           behind=[person("lab_mid", "noa", -1.9, 1.4, [["shrug", 0], ["idle", 2.0]]),
                                   person("lab_mid", "ilan", 0.2, 1.5, [["idle", 0], ["shrug", 1.2]], walk=[(0, 2.2, 1.6), (1.0, 0.2, 1.5)])],
                           front=[ved("lab_mid", -0.4, -0.5, [["think", 0], ["shrug", 1.8], ["serious", 3.6]])],
                           extra_top=[txt("ORIGIN: *UNKNOWN*", 0.14, 110, enter="pop", at=1.6, sfx="pop"),
                                      txt("TIMES ANYONE CHECKED: *0*", 0.24, 72, enter="pop", at=3.6, sfx="pop")])})
# 11. close: payoff that loops to everyday forgetting
S.append({"say": "So next time you forget why you walked into a room... don't blame the *goldfish*.", "transition": "cut", "caption_y": 0.64,
          "layers": [plate("lab_mid", blur=10, keys=[{"t": 0, "scale": 1.35}, {"t": 4.5, "scale": 1.42}]),
                     close_ved([["explain", 0], ["smirk", 2.6], ["crossed", 3.6]]),
                     swim([(0, 1.2, 0.3), (2.6, -0.2, 0.26)], 0.26, 1.0, flip=True),
                     txt("DON'T BLAME *THE GOLDFISH*", 0.14, 104, enter="pop", at=2.8, sfx="ding")]})

job = {"id": ID, "title": "Goldfish have a 3-second memory? Total myth 🐟",
       "description": "Goldfish learned to push a lever on a schedule, and even to drive a tank on wheels. Here's what their memory can really do.\n\n"
                      "Sources: Discover Wildlife, 'Do goldfish really only have a 3 second memory?'; Science ABC; "
                      "Global News / VOA on the 2022 Ben-Gurion University goldfish-driving study.",
       "tags": ["goldfish", "goldfish memory", "myth busting", "animal facts", "fish intelligence", "science explained", "animal memory", "biology"],
       "hashtags": ["#science", "#animals"],
       "meta": {"format": "myth-bust", "topic": "the goldfish 3-second memory myth", "hook": "myth-bust",
                "idea_source": "backlog", "characters": ["ved", "extra"],
                "sources": ["https://www.discoverwildlife.com/animal-facts/fish/goldfish-memory",
                            "https://www.scienceabc.com/nature/animals/do-goldfish-really-have-a-3-second-memory.html",
                            "https://www.earth.com/news/goldfish-memory-much-better-than-previously-believed",
                            "https://globalnews.ca/news/8496803/goldfish-drive-cars-study/",
                            "https://learningenglish.voanews.com/amp/israeli-researchers-teach-goldfish-to-drive-robotic-car/6395501.html"],
                "humour": {"trend": "timeless dry reaction (no current trend fit naturally): 'got its licence before me'",
                           "beat": "deadpan", "scene": 7}},
       "privacy": "public", "speaker": "ved", "assets_script": J + "assets.py", "scenes": S}
json.dump(job, open(J + "job.json", "w"), indent=1, ensure_ascii=False)
print("scenes", len(S), "using", SRC)
