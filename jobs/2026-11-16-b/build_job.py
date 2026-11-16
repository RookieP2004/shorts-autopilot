"""2026-11-16-b: "The night the sky fell (1833)" (wild-story).
2D Ved + townspeople staged in depth on a Blender 1833 town square at night (wide, mid on the GAZETTE, looking up at the
sky) and a deep-space plate (Earth crossing comet Tempel-Tuttle's dust trail), built from stills + cut-outs. 2D on top:
meteor streaks raining from one radiant point, a hud chip that ticks to 100,000 an hour, an eqbar (100,000 vs 15), a
cream newspaper card, a node map of towns sending reports to Olmsted, a tracker of his 3 steps, option cards
(WEATHER x / SPACE tick), a FROM SPACE stamp and honesty tags.
Facts: Leonid storm, night of 12-13 Nov 1833, est. 50,000-150,000 an hour (Smithsonian; Linda Hall: ~100,000); seen across
the US, many thought the world was ending; Denison Olmsted (Yale) crowdsourced reports through newspapers, found the radiant
in Leo moved with the stars -> cosmic origin, published in the American Journal of Science (birth of meteor-shower science);
Leonids come from comet Tempel-Tuttle, big displays roughly every 33 years; 2026 peak Nov 17-18, ZHR ~15 (Space.com).
Run after the assets exist: python jobs/2026-11-16-b/build_job.py
"""
import json, math, os, random, sys
sys.path.insert(0, os.getcwd())
from autopilot.stage import Stage

ID = "2026-11-16-b"
J = f"jobs/{ID}/"
A = J + "assets/"
ST = {n: Stage(A + f"plate_{n}.json") for n in ("town_wide", "town_mid")}

OUT = {   # recurring townspeople (1833): same outfit in every shot
    "olmsted": {"skin": "#e8b98f", "build": "slim", "hair": ["#5a4632", "short"], "hat": ["tophat", "#25262b"],
                "top": ["#34425c", "jacket"], "bottom": ["#3a3e48", "trousers"], "shoes": "#25262b", "tie": "#f6efe2"},
    "ruth": {"skin": "#c68a5e", "build": "regular", "hair": ["#1a1410", "long"], "hat": ["headscarf", "#d9534f"],
             "top": ["#f2b04a", "dress"], "bottom": ["#7c2533", "skirt"], "shoes": "#3a2a22"},
    "amos": {"skin": "#8d5a3b", "build": "regular", "hair": ["#1a1410", "short"], "hat": ["straw", "#e0c27a"],
             "top": ["#f6efe2", "shirt"], "bottom": ["#5a4632", "trousers"], "shoes": "#25262b", "apron": "#8a6142"},
}
F = "font-family='Poppins, DejaVu Sans, sans-serif' font-weight='800'"
AN = "font-family='Anton, DejaVu Sans, sans-serif'"
RAD = (0.62, 0.2)          # the radiant (in Leo) on plate_town_up


def plate(name, blur=0, **k):
    return {"type": "image", "path": A + f"plate_{name}.png", "x": 0.5, "y": 0.5, "w": 1.0, "enter": "none", "blur": blur, **k}


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


def staged(set_, people=(), fg=False, front=(), extra_top=()):
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


def tag(word="PROVEN", color="#6fc3c0"):
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 300 84'><rect x='4' y='4' width='292' height='76' rx='38' "
            f"fill='{color}' stroke='#1a1410' stroke-width='5'/><circle cx='44' cy='42' r='16' fill='#1a1410'/>"
            f"<path d='M36,42 l6,7 l11,-14' stroke='{color}' stroke-width='5' fill='none'/>"
            f"<text x='172' y='60' text-anchor='middle' font-size='50' fill='#1a1410' {AN}>{word}</text></svg>")


def tag_layer(x, y, at, word="PROVEN", color="#6fc3c0"):
    return {"type": "image", "svg": tag(word, color), "x": x, "y": y, "w": 0.24, "enter": "pop", "at": at, "sfx": "click"}


def hud(label, y=0.74, **k):
    return {"type": "hud", "label": label, "x": 0.5, "y": y, "enter": "pop", "sfx": "click", **k}


STREAK = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 700 60'><defs>"
          "<linearGradient id='g' x1='0' x2='1'><stop offset='0' stop-color='#ffffff' stop-opacity='0'/>"
          "<stop offset='0.7' stop-color='#bfeaff' stop-opacity='0.55'/><stop offset='1' stop-color='#ffffff' stop-opacity='1'/></linearGradient>"
          "<radialGradient id='h'><stop offset='0' stop-color='#ffffff'/><stop offset='0.4' stop-color='#fff3c4' stop-opacity='0.9'/>"
          "<stop offset='1' stop-color='#ffd27a' stop-opacity='0'/></radialGradient></defs>"
          "<polygon points='0,30 660,22 660,38' fill='url(#g)'/><circle cx='662' cy='30' r='28' fill='url(#h)'/></svg>")
SGN = 1.0     # rotate sign: + = clockwise on screen (checked in frames)


def streak(x0, y0, x1, y1, at, dur=0.7, w=0.4):
    ang = math.degrees(math.atan2((y1 - y0) * 1920, (x1 - x0) * 1080)) * SGN
    return {"type": "image", "svg": STREAK, "x": x0, "y": y0, "w": w, "rotate": ang, "at": at, "enter": "fade", "enter_dur": 0.08,
            "until": at + dur, "exit": "fade", "keys": [{"t": 0, "x": x0, "y": y0}, {"t": dur, "x": x1, "y": y1, "ease": "linear"}]}


def rain(t0, t1, n, rad=RAD, seed=1, rmin=0.06, rmax=0.5, w=(0.22, 0.42), drift=None, ymax=0.62):
    """meteor storm: n streaks between t0 and t1, all flying away from the radiant (rad can drift: [(t, x, y), ...])."""
    random.seed(seed)
    out = []
    for k in range(n):
        at = t0 + (t1 - t0) * k / max(1, n - 1) + random.uniform(-0.05, 0.05)
        rx, ry = rad
        if drift:
            (ta, xa, ya), (tb, xb, yb) = drift
            u = min(1, max(0, (at - ta) / (tb - ta))); rx, ry = xa + (xb - xa) * u, ya + (yb - ya) * u
        a = random.uniform(0, 2 * math.pi)
        d0 = random.uniform(rmin, rmax * 0.6); d1 = d0 + random.uniform(0.18, 0.32)
        ux, uy = math.cos(a) / 1080, math.sin(a) / 1920
        nrm = math.hypot(ux, uy); ux, uy = ux / nrm * 0.5625, uy / nrm
        x0, y0, x1, y1 = rx + ux * d0, ry + uy * d0 * 0.5625, rx + ux * d1, ry + uy * d1 * 0.5625
        if not (0.02 < x0 < 0.98 and 0.02 < y0 < ymax):
            continue
        out.append(streak(x0, y0, x1, y1, max(0.0, at), random.uniform(0.45, 0.7), random.uniform(*w)))
    return out


GLOW = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 400'><defs><radialGradient id='o'>"
        "<stop offset='0' stop-color='#fff3c4'/><stop offset='0.3' stop-color='#ffd27a' stop-opacity='0.7'/>"
        "<stop offset='1' stop-color='#ff7a2a' stop-opacity='0'/></radialGradient></defs><circle cx='200' cy='200' r='200' fill='url(#o)'/></svg>")

RING = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 300 300'><circle cx='150' cy='150' r='120' fill='none' "
        "stroke='#f2b04a' stroke-width='12' stroke-dasharray='26 14'/><circle cx='150' cy='150' r='14' fill='#fff3c4'/></svg>")

# a fictional 1833 newspaper clipping, cream card style
PAPER = card(
    "<text x='450' y='78' text-anchor='middle' font-size='54' fill='#1a1410' font-family='Libre Baskerville, DejaVu Serif, serif' font-weight='700'>THE TOWN GAZETTE</text>"
    "<line x1='60' y1='100' x2='840' y2='100' stroke='#1a1410' stroke-width='4'/>"
    "<text x='450' y='160' text-anchor='middle' font-size='40' fill='#7c2533' " + AN + ">WANTED: WHAT DID YOU SEE IN THE SKY?</text>"
    "<text x='450' y='205' text-anchor='middle' font-size='28' fill='#34425c' " + F + ">Write to Prof. Olmsted, Yale College</text>"
    + "".join(f"<rect x='{60 + c * 270}' y='{235 + r * 26}' width='{230 - (r % 3) * 30}' height='10' rx='5' fill='#b9ab98'/>"
              for c in range(3) for r in range(5)), 900, 380)

S = []
# 0. hook (town mid): the headline + the hud tick at frame 0, meteors pour down over Ved
S.append({"say": "November 1833. The sky *fell*. Up to 100,000 shooting stars an hour.",
                    "caption_y": 0.47,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 5.0, "zoom": 1.07, "focus": [0.5, 0.52]}]},
          "layers": staged("town_mid",
                           people=[ved("town_mid", -0.2, -1.6, [["surprised", 0], ["point", 2.0], ["explain", 3.4]], hops=[[0.2, 0.06, 0.4]])],
                           fg=True,
                           extra_top=rain(0.0, 5.2, 22, rad=(0.7, -0.05), seed=3, rmin=0.05, rmax=0.6, ymax=0.4)
                           + [txt("THE NIGHT THE SKY *FELL*", 0.165, 96, enter="none"),
                              hud("shooting stars per hour", steps=[[0, 0], [0.1, 100000]], count_dur=1.0, tone="gold", y=0.3,
                                  enter="none", indian=False, width_of="100,000")])})
# 1. town wide: the townspeople panic in the street under the storm
S.append({"say": "Many thought the world was *ending*.",
          "transition": "slide_left", "caption_y": 0.47,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.2, "zoom": 1.06, "focus": [0.5, 0.47]}]},
          "layers": staged("town_wide",
                           people=[person("town_wide", "ruth", -1.8, -3.2, [["surprised", 0], ["point", 1.0], ["surprised", 2.0]],
                                          walk=[(0, -3.6, -2.4), (1.0, -1.8, -3.2)], hops=[[1.4, 0.06, 0.4]]),
                                   person("town_wide", "amos", 1.4, -4.0, [["surprised", 0], ["shrug", 1.6]], hops=[[0.5, 0.07, 0.4]]),
                                   ved("town_wide", 3.4, -4.6, [["think", 0], ["crossed", 1.6]])],
                           extra_top=rain(0.0, 3.4, 18, rad=(0.62, 0.0), seed=5, rmin=0.04, rmax=0.6, ymax=0.4)
                           + [txt("THE END OF THE *WORLD?*", 0.165, 96, enter="pop", at=0.3, sfx="pop")])})
# 2. comic beat: side-eye cut-away
S.append({"dur": 1.6, "transition": "cut", "captions": False,
          "layers": [plate("town_mid", blur=10, keys=[{"t": 0, "scale": 1.35}]), dict(close_ved([["side_eye", 0]]), acting="none")],
          "beat": {"kind": "side_eye", "at": 0.1, "dur": 1.45, "who": "ved",
                   "text": "the 1833 group chat:\n*\"u guys seeing this??\"*", "text_y": 0.2}})
# 3. town mid: Olmsted steps out of the Gazette, curious; Ved points at him
S.append({"say": "But Yale's *Denison Olmsted* got curious.",
          "transition": "slide_left", "caption_y": 0.47,
          "camera": {"keys": [{"t": 0, "zoom": 1.04, "focus": [0.5, 0.52]}, {"t": 3.6, "zoom": 1.0, "focus": [0.5, 0.5]}]},
          "layers": staged("town_mid",
                           people=[person("town_mid", "olmsted", -1.0, -0.9, [["idle", 0], ["explain", 1.2], ["point", 2.4]],
                                          walk=[(0, -0.3, -0.2), (1.0, -1.0, -0.9)]),
                                   ved("town_mid", 0.55, -1.9, [["welcome", 0], ["point", 0.6], ["explain", 2.2]])],
                           fg=True,
                           extra_top=[{"type": "image", "svg": card(
                                          "<text x='40' y='78' font-size='56' fill='#1a1410' " + AN + ">DENISON OLMSTED</text>"
                                          "<text x='40' y='122' font-size='30' fill='#34425c' " + F + ">PROFESSOR, YALE COLLEGE</text>", 620, 150),
                                       "x": 0.36, "y": 0.27, "w": 0.56, "rotate": -2, "enter": "slide_right", "at": 0.8, "sfx": "pop"},
                                      {"type": "tracker", "n": 3, "done": [], "x": 0.5, "y": 0.14, "at": 1.6, "enter": "fade"},
                                      tag_layer(0.76, 0.36, 2.0)])})
# 4. the call for reports: newspaper card, then a node map of towns feeding him reports
NODES = [{"id": "o", "pos": [0, 0, 0], "at": 1.5, "tone": "gold", "label": "OLMSTED"},
         {"id": "a", "pos": [-1.8, 1.3, 0.3], "at": 1.7, "tone": "blue", "label": "BOSTON"},
         {"id": "b", "pos": [1.7, 1.2, -0.3], "at": 1.85, "tone": "blue", "label": "NEW YORK"},
         {"id": "c", "pos": [-1.9, -1.2, 0.4], "at": 2.0, "tone": "blue", "label": "OHIO"},
         {"id": "d", "pos": [1.8, -1.3, -0.2], "at": 2.15, "tone": "blue", "label": "ALABAMA"}]
S.append({"say": "He had newspapers collect what *everyone* saw.",
          "transition": "slide_up", "caption_y": 0.71,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.2, "zoom": 1.05, "focus": [0.5, 0.48]}]},
          "layers": [plate("town_wide", blur=8),
                     {"type": "image", "svg": PAPER, "x": 0.5, "y": 0.22, "w": 0.84, "rotate": -2, "enter": "drop", "at": 0.1, "sfx": "pop",
                      "keys": [{"t": 0, "y": 0.22, "scale": 1.0}, {"t": 1.3, "y": 0.2, "scale": 0.92}]},
                     {"type": "nodes", "nodes": NODES, "x": 0.5, "y": 0.5, "yaw": [-14, 10],
                      "edges": [["a", "o", 1.9, "blue"], ["b", "o", 2.05, "blue"], ["c", "o", 2.2, "blue"], ["d", "o", 2.35, "blue"]]},
                     {"type": "tracker", "n": 3, "done": [0.6], "x": 0.5, "y": 0.66, "enter": "none"}]})
# 5. the sky: every streak traces back to one point; ring + LEO
S.append({"say": "Every streak pointed back to *one spot*, in Leo.",
          "transition": "zoom", "caption_y": 0.7,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.4, "zoom": 1.08, "focus": [0.58, 0.4]}]},
          "layers": [plate("town_up")] + rain(0.0, 3.6, 26, seed=11, rmin=0.04, rmax=0.55, ymax=0.62)
                    + [{"type": "image", "svg": RING, "x": RAD[0], "y": RAD[1], "w": 0.2, "enter": "zoom", "at": 1.4, "sfx": "pop",
                        "loop": "pulse", "loop_amp": 0.05},
                       txt("ONE *SPOT*: LEO", 0.33, 100, enter="pop", at=1.8, sfx="pop"),
                       {"type": "tracker", "n": 3, "done": [0, 1.6], "x": 0.5, "y": 0.42, "enter": "none"}]})
# 6. the spot moved with the stars: the whole sky drifts, the ring stays on Leo -> not weather
S.append({"say": "And it moved *with the stars*. Not weather. *Space*.",
          "transition": "cut", "caption_y": 0.7,
          "layers": [plate("town_up", keys=[{"t": 0, "x": 0.5, "scale": 1.06}, {"t": 3.6, "x": 0.44, "scale": 1.06, "ease": "linear"}])]
                    + rain(0.0, 3.4, 18, seed=13, rmin=0.04, rmax=0.5, ymax=0.5, drift=[(0, RAD[0], RAD[1]), (3.6, RAD[0] - 0.06, RAD[1])])
                    + [{"type": "image", "svg": RING, "x": RAD[0], "y": RAD[1], "w": 0.2, "enter": "none",
                        "keys": [{"t": 0, "x": RAD[0]}, {"t": 3.6, "x": RAD[0] - 0.06, "ease": "linear"}]},
                       {"type": "optcard", "label": "the cause", "text": "WEATHER", "tone": "blue", "x": 0.28, "y": 0.42, "w": 0.4,
                        "rotate": -3, "enter": "pop", "at": 0.3, "sfx": "pop", "verdict": "cross", "verdict_at": 1.4},
                       {"type": "optcard", "label": "the cause", "text": "SPACE", "tone": "green", "x": 0.72, "y": 0.42, "w": 0.4,
                        "rotate": 3, "enter": "pop", "at": 0.6, "sfx": "pop", "verdict": "tick", "verdict_at": 2.2},
                       {"type": "tracker", "n": 3, "done": [0, 0, 2.4], "x": 0.5, "y": 0.53, "enter": "none"},
                       {"type": "stamp", "text": "METEOR SCIENCE IS BORN", "tone": "gold", "angle": -6, "size": 58, "x": 0.5, "y": 0.6,
                        "at": 2.8, "sfx": "thud"}]})
# 7. space: comet Tempel-Tuttle's dust trail; Earth ploughs through it every November
S.append({"say": "It's dust from Comet *Tempel-Tuttle*. We hit it every November.",
          "transition": "slide_up", "caption_y": 0.6,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.0, "zoom": 1.08, "focus": [0.5, 0.55]}]},
          "layers": [plate("trail"),
                     sprite("comet", 0.78, 0.2, 0.22, at=0.0, enter="fade", sfx="whoosh",
                            keys=[{"t": 0, "x": 0.86, "y": 0.16, "rot": -8}, {"t": 4.0, "x": 0.72, "y": 0.22, "rot": 6, "ease": "linear"}]),
                     txt("COMET *TEMPEL-TUTTLE*", 0.15, 84, enter="pop", at=0.4, sfx="pop"),
                     {"type": "stamp", "text": "FROM SPACE", "tone": "green", "angle": -7, "size": 96, "x": 0.42, "y": 0.27, "at": 1.3, "sfx": "thud"},
                     tag_layer(0.76, 0.34, 1.8),
                     {"type": "image", "svg": card("<text x='300' y='92' text-anchor='middle' font-size='58' fill='#1a1410' " + AN + ">EVERY NOVEMBER</text>", 600, 140),
                      "x": 0.5, "y": 0.44, "w": 0.46, "rotate": 2, "enter": "pop", "at": 2.8, "sfx": "pop"}]})
# 8. town wide: tomorrow night's Leonids vs 1833 (hud + eqbar); a few gentle streaks, townspeople look up
S.append({"say": "This week? About *fifteen* an hour.",
          "transition": "slide_left", "caption_y": 0.47,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.2, "zoom": 1.05, "focus": [0.5, 0.47]}]},
          "layers": staged("town_wide",
                           people=[person("town_wide", "ruth", -1.8, -3.2, [["point", 0], ["happy", 1.4]]),
                                   person("town_wide", "amos", 1.4, -4.0, [["idle", 0], ["shrug", 1.8]]),
                                   ved("town_wide", 3.4, -4.6, [["explain", 0], ["point", 1.4]])],
                           extra_top=[streak(0.8, 0.06, 0.5, 0.16, 0.6, 0.6, 0.35), streak(0.3, 0.1, 0.12, 0.22, 2.2, 0.6, 0.3),
                                      hud("Leonids, Nov 17-18, 2026", steps=[[0, 100000], [0.6, 15]], count_dur=0.9, tone="blue", y=0.14,
                                          indian=False, suffix=" / hour", width_of="100,000 / hour"),
                                      {"type": "eqbar", "keys": [[0.8, "1833: 100,000 / hour"], [1.8, "100,000 ÷ 15 ≈ *6,700x* more"]],
                                       "tone": "gold", "x": 0.5, "y": 0.24, "enter": "fade"}])})
# 9. close payoff: every ~33 years the comet returns, the sky can fall again (loops to the hook)
S.append({"say": "But every 33 years the comet returns, and the sky can *fall* again.",
          "transition": "cut", "caption_y": 0.64,
          "layers": [plate("town_up", blur=10, keys=[{"t": 0, "scale": 1.35}, {"t": 4.0, "scale": 1.42}])]
                    + rain(1.6, 4.4, 14, rad=(0.7, 0.06), seed=17, rmin=0.04, rmax=0.5, ymax=0.4)
                    + [close_ved([["warm", 0], ["explain", 1.0], ["point", 2.6], ["smirk", 3.6]]),
                       hud("next big return", text="~33 YEARS", tone="gold", y=0.16, at=0.6),
                       tag_layer(0.78, 0.26, 1.2, "THEORY", "#f2b04a")]})

job = {"id": ID, "title": "The night the sky fell (1833) 🌠",
       "description": "On 13 November 1833 up to ~100,000 shooting stars an hour fell over America, and many thought the world "
                      "was ending. Yale's Denison Olmsted collected reports through newspapers, saw every streak came from one point "
                      "in Leo that moved with the stars, and showed meteors come from space. They're dust from comet Tempel-Tuttle; "
                      "the Leonids peak again on 17-18 November 2026 (~15 an hour).\n\n"
                      "Sources: Smithsonian Magazine; Linda Hall Library; The Irish Times; Space.com.",
       "tags": ["leonids", "1833 meteor storm", "leonid meteor shower", "meteor shower 2026", "denison olmsted",
                "night the stars fell", "astronomy history", "science history", "space"],
       "hashtags": ["#space", "#history"],
       "instagram": {"hashtags": ["#science", "#leonids", "#meteorshower", "#astronomy", "#explained"]},
       "meta": {"format": "wild-story", "topic": "the 1833 Leonid meteor storm: up to ~100,000 an hour, panic, Denison Olmsted "
                                                 "crowdsourced reports via newspapers, radiant in Leo moving with the stars = from space "
                                                 "(birth of meteor science), comet Tempel-Tuttle, ~33-year cycle, 2026 peak ~15/h",
                "hook": "number-shock",
                "idea_source": "trending + unique: Leonids peak 17-18 Nov 2026 (Space.com) and the 1833 storm anniversary week; "
                               "backlog idea (1833 Leonid storm); few Shorts tell the Olmsted crowdsourcing story",
                "characters": ["ved", "extra"],
                "sources": ["https://www.smithsonianmag.com/smart-news/americans-fell-in-love-with-science-when-the-breathtaking-leonid-meteor-shower-lit-up-the-skies-across-nation-180985435/",
                            "https://www.lindahall.org/about/news/scientist-of-the-day/denison-olmsted/",
                            "https://www.irishtimes.com/culture/they-thought-it-was-judgment-day-the-night-the-stars-fell-on-the-us-south-1.4075652",
                            "https://www.space.com/leonid-meteor-shower"],
                "humour": {"trend": "timeless dry aside (no current meme fit: 'Remember November' already used twice this week): "
                                    "side-eye + 'the 1833 group chat: u guys seeing this??' card",
                           "beat": "side_eye", "scene": 2},
                "claims": [
                    {"claim": "the 1833 Leonid storm (night of 12-13 Nov) reached ~50,000-150,000 meteors an hour (~100,000)", "tag": "PROVEN",
                     "source": "https://www.smithsonianmag.com/smart-news/americans-fell-in-love-with-science-when-the-breathtaking-leonid-meteor-shower-lit-up-the-skies-across-nation-180985435/"},
                    {"claim": "many who saw it thought it was Judgment Day / the end of the world", "tag": "PROVEN",
                     "source": "https://www.irishtimes.com/culture/they-thought-it-was-judgment-day-the-night-the-stars-fell-on-the-us-south-1.4075652"},
                    {"claim": "Olmsted (Yale) crowdsourced observations through newspapers", "tag": "PROVEN",
                     "source": "https://www.smithsonianmag.com/smart-news/americans-fell-in-love-with-science-when-the-breathtaking-leonid-meteor-shower-lit-up-the-skies-across-nation-180985435/"},
                    {"claim": "meteors radiated from a point in Leo that moved with the stars -> cosmic, not atmospheric; birth of meteor-shower science", "tag": "PROVEN",
                     "source": "https://www.lindahall.org/about/news/scientist-of-the-day/denison-olmsted/"},
                    {"claim": "the Leonids come from comet Tempel-Tuttle; big displays roughly every 33 years", "tag": "PROVEN",
                     "source": "https://www.irishtimes.com/culture/they-thought-it-was-judgment-day-the-night-the-stars-fell-on-the-us-south-1.4075652"},
                    {"claim": "2026 Leonids peak 17-18 Nov, ZHR ~15", "tag": "PROVEN", "source": "https://www.space.com/leonid-meteor-shower"},
                    {"claim": "the sky 'can fall again' on a future return (storms are forecast, not guaranteed)", "tag": "THEORY",
                     "source": "https://www.irishtimes.com/culture/they-thought-it-was-judgment-day-the-night-the-stars-fell-on-the-us-south-1.4075652"}]},
       "thumbnail": {"title": "THE SKY *FELL*", "title_y": 0.15, "title_size": 190, "max_w": 0.95, "blur": 14,
                     "glow": "#ffb35a", "glow_x": 0.5, "glow_y": 0.5, "glow_strength": 1.4, "bg_saturation": 1.5,
                     "tint": ["#1f4fb8", "#f08a24"], "tint_amount": 0.3,
                     "bg": [plate("town_wide")],
                     "fg": [{"type": "image", "svg": STREAK, "x": 0.4, "y": 0.32, "w": 0.6, "rotate": 130, "enter": "none"},
                            {"type": "image", "svg": STREAK, "x": 0.72, "y": 0.42, "w": 0.5, "rotate": 120, "enter": "none"},
                            {"type": "image", "svg": STREAK, "x": 0.25, "y": 0.5, "w": 0.45, "rotate": 140, "enter": "none"},
                            {"type": "character", "id": "ved", "pose": "surprised", "x": 0.5, "y": 0.93, "h": 0.95, "enter": "none",
                             "acting": "none", "talk": False, "ground": False, "allow_outside_safe": True}]},
       "privacy": "public", "speaker": "ved", "assets_script": J + "assets.py", "scenes": S}
json.dump(job, open(J + "job.json", "w"), indent=1, ensure_ascii=False)
print("scenes", len(S))
