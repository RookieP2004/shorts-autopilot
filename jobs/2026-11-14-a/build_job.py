"""2026-11-14-a: \"Why is gold gold? Blame Einstein\" (big-question). Goldsmith shop + atom studio (Blender stills + cut-outs), 2D panels: metal swatches, orbit before/after, white - blue = yellow.\nRun after the assets exist: python jobs/2026-11-14-a/build_job.py\n"""
import json, os, sys
sys.path.insert(0, os.getcwd())
from autopilot.stage import Stage

ID = "2026-11-14-a"
J = f"jobs/{ID}/"
A = J + "assets/"
ST = {n: Stage(A + f"plate_{n}.json") for n in ("shop_wide", "shop_mid", "atom_wide")}

OUT = {   # recurring townspeople: same outfit in every shot
    "mira": {"skin": "#a8693f", "build": "slim", "hair": ["#1a1410", "bun"], "hat": ["headscarf", "#6fc3c0"],
             "top": ["#34425c", "dress"], "bottom": ["#34425c", "trousers"], "shoes": "#25262b", "apron": "#7c2533", "earrings": "#f2b04a"},
    "omar": {"skin": "#c68a5e", "build": "round", "hair": ["#1a1410", "short"], "hat": ["fez", "#d9534f"],
             "top": ["#f2b04a", "jacket"], "bottom": ["#3a3e48", "trousers"], "shoes": "#25262b", "bag": "#8a5a3c"},
}
F = "font-family='Poppins, DejaVu Sans, sans-serif' font-weight='800'"
AN = "font-family='Anton, DejaVu Sans, sans-serif'"


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


def stamp(word, color="#d9534f", w=560):
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {w} 170'><rect x='10' y='10' width='{w-20}' height='150' rx='18' "
            f"fill='none' stroke='{color}' stroke-width='14'/><text x='{w/2}' y='128' text-anchor='middle' font-size='118' "
            f"fill='{color}' {AN}>{word}</text></svg>")






def orbit_keys(cx, cy, rx, ry, dur, turns=2.0, n=24):
    import math
    return [{"t": dur * k / n, "x": cx + rx * math.cos(2 * math.pi * turns * k / n), "y": cy + ry * math.sin(2 * math.pi * turns * k / n),
             "ease": "linear"} for k in range(n + 1)]


def tag(word, color="#46965a", w=420):
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {w} 110'><rect x='5' y='5' width='{w-10}' height='100' rx='22' "
            f"fill='{color}' stroke='#1a1410' stroke-width='6'/><text x='{w/2}' y='76' text-anchor='middle' font-size='62' "
            f"fill='#f6efe2' {AN}>{word}</text></svg>")


# metal swatches: four grey, one gold
def swatch(cx, col, name, ring="#1a1410"):
    return (f"<circle cx='{cx}' cy='120' r='62' fill='{col}' stroke='{ring}' stroke-width='6'/>"
            f"<ellipse cx='{cx-18}' cy='100' rx='22' ry='12' fill='#ffffff' opacity='0.55'/>"
            f"<text x='{cx}' y='232' text-anchor='middle' font-size='40' fill='#1a1410' {AN}>{name}</text>")


METALS = card(swatch(100, "#c9ced4", "SILVER") + swatch(270, "#8f959c", "IRON") + swatch(440, "#bfc5cb", "ALUMINIUM")
              + swatch(610, "#a9aeb3", "TIN") + swatch(800, "#e2b041", "GOLD", "#d9534f"), 900, 270)

# orbit before / after (relativity shrinks the orbit, electron gets heavier)
ORBIT = card(
    f"<text x='225' y='70' text-anchor='middle' font-size='40' fill='#34425c' {AN}>SLOW ELECTRON</text>"
    f"<text x='675' y='70' text-anchor='middle' font-size='40' fill='#d9534f' {AN}>NEAR LIGHT SPEED</text>"
    "<circle cx='225' cy='250' r='130' fill='none' stroke='#6fc3c0' stroke-width='8' stroke-dasharray='14 10'/>"
    "<circle cx='225' cy='250' r='34' fill='#f2b04a' stroke='#1a1410' stroke-width='5'/>"
    "<circle cx='355' cy='250' r='18' fill='#1fa8ff' stroke='#1a1410' stroke-width='4'/>"
    "<circle cx='675' cy='250' r='88' fill='none' stroke='#6fc3c0' stroke-width='8' stroke-dasharray='14 10'/>"
    "<circle cx='675' cy='250' r='34' fill='#f2b04a' stroke='#1a1410' stroke-width='5'/>"
    "<circle cx='763' cy='250' r='24' fill='#1fa8ff' stroke='#1a1410' stroke-width='4'/>"
    "<path d='M430,250 L500,250' stroke='#1a1410' stroke-width='10' stroke-linecap='round'/><path d='M490,228 L520,250 L490,272 Z' fill='#1a1410'/>"
    f"<text x='675' y='440' text-anchor='middle' font-size='50' fill='#1a1410' {AN}>MASS ~+20%</text>"
    f"<text x='225' y='440' text-anchor='middle' font-size='50' fill='#1a1410' {AN}>NORMAL ORBIT</text>"
    f"<text x='675' y='490' text-anchor='middle' font-size='44' fill='#d9534f' {AN}>ORBIT SHRINKS</text>", 900, 520)

# white light hits gold: blue swallowed, the rest bounces back
BEAM = card(
    f"<text x='450' y='66' text-anchor='middle' font-size='52' fill='#1a1410' {AN}>WHITE LIGHT HITS GOLD</text>"
    "<rect x='250' y='330' width='400' height='70' rx='14' fill='#e2b041' stroke='#1a1410' stroke-width='6'/>"
    "<path d='M330,330 L300,330 L110,110' stroke='#f6efe2' stroke-width='22' fill='none' stroke-linecap='round'/>"
    "<path d='M330,330 L110,110' stroke='#1a1410' stroke-width='30' stroke-linecap='round' opacity='0.12'/>"
    "<path d='M120,112 L330,325' stroke='#ffffff' stroke-width='18' stroke-linecap='round'/>"
    "<path d='M120,112 L330,325' stroke='#1a1410' stroke-width='3' fill='none'/>"
    "<path d='M455,315 L600,140' stroke='#f2b04a' stroke-width='18' stroke-linecap='round'/>"
    "<path d='M480,318 L640,170' stroke='#d9534f' stroke-width='14' stroke-linecap='round'/>"
    "<path d='M430,312 L560,120' stroke='#f6d54a' stroke-width='14' stroke-linecap='round'/>"
    "<circle cx='380' cy='300' r='26' fill='#2a6fdb' stroke='#1a1410' stroke-width='5'/>"
    "<path d='M366,286 L394,314 M394,286 L366,314' stroke='#f6efe2' stroke-width='6' stroke-linecap='round'/>"
    f"<text x='380' y='250' text-anchor='middle' font-size='40' fill='#2a6fdb' {AN}>BLUE: EATEN</text>"
    f"<text x='700' y='110' text-anchor='middle' font-size='40' fill='#d9534f' {AN}>REST: BOUNCES</text>", 900, 440)


def dot(col, label):
    return col, label


EQ = card(
    "<circle cx='130' cy='120' r='80' fill='#ffffff' stroke='#1a1410' stroke-width='6'/>"
    f"<text x='130' y='250' text-anchor='middle' font-size='42' fill='#1a1410' {AN}>WHITE</text>"
    f"<text x='265' y='148' text-anchor='middle' font-size='110' fill='#1a1410' {AN}>-</text>"
    "<circle cx='400' cy='120' r='80' fill='#2a6fdb' stroke='#1a1410' stroke-width='6'/>"
    f"<text x='400' y='250' text-anchor='middle' font-size='42' fill='#1a1410' {AN}>BLUE</text>"
    f"<text x='535' y='148' text-anchor='middle' font-size='110' fill='#1a1410' {AN}>=</text>"
    "<circle cx='700' cy='120' r='90' fill='#f2c23a' stroke='#d9534f' stroke-width='8'/>"
    f"<text x='700' y='250' text-anchor='middle' font-size='42' fill='#d9534f' {AN}>YELLOW</text>", 900, 280)

S = []
# 0. hook (shop mid): gold ring pops, the claim at frame 0
S.append({"say": "Your gold ring is yellow because of *Einstein*.",
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.0, "zoom": 1.07, "focus": [0.5, 0.52]}]},
          "layers": staged("shop_mid",
                           people=[person("shop_mid", "mira", 0.1, 1.4, [["idle", 0], ["surprised", 1.6]])],
                           fg=True, front=[ved("shop_mid", -1.1, -1.3, [["point", 0], ["explain", 1.8]])],
                           extra_top=[sprite("gold_ring", 0.72, 0.29, 0.22, enter="none", loop="float", loop_amp=0.01),
                                      txt("GOLD IS YELLOW", 0.12, 104, enter="none"),
                                      txt("BECAUSE OF *EINSTEIN*", 0.2, 96, enter="pop", at=0.0)])})
# 1. shelf close: almost every metal is grey; swatch panel
S.append({"say": "Silver, iron, aluminium, tin: almost every metal is *grey*.",
          "transition": "slide_left", "caption_y": 0.66,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.0, "zoom": 1.08, "focus": [0.5, 0.55]}]},
          "layers": [plate("shelf_close"),
                     {"type": "image", "svg": METALS, "x": 0.5, "y": 0.2, "w": 0.88, "enter": "slide_down", "at": 0.1, "sfx": "pop"},
                     {"type": "image", "svg": stamp("ODD ONE OUT", "#d9534f", 900), "x": 0.6, "y": 0.31, "w": 0.48, "rotate": -6,
                      "enter": "zoom", "at": 2.6, "sfx": "pop"}]})
# 2. atom wide: Ved walks in; 79 protons
S.append({"say": "But gold's nucleus packs *79 protons*, pulling hard on its electrons.",
          "transition": "zoom", "caption_y": 0.73,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.0, "zoom": 1.1, "focus": [0.5, 0.48]}]},
          "layers": staged("atom_wide",
                           people=[ved("atom_wide", -1.3, -3.2, [["welcome", 0], ["point", 1.4], ["explain", 3.0]],
                                       walk=[(0, -2.8, -3.4), (1.1, -1.3, -3.2)])],
                           extra_top=[{"type": "counter", "from": 0, "to": 79, "decimals": 0, "suffix": " PROTONS", "x": 0.5, "y": 0.13,
                                       "size": 120, "color": "accent", "at": 0.2, "count_dur": 1.4, "enter": "none", "stroke": "#0b0f12", "stroke_width": 7},
                                      {"type": "image", "svg": tag("PROVEN"), "x": 0.76, "y": 0.21, "w": 0.26, "enter": "pop", "at": 1.6, "sfx": "pop"}])})
# 3. atom close: electron whips round, over half light speed
S.append({"say": "So its inner electrons race at over *half the speed of light*.",
          "transition": "cut", "caption_y": 0.7,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.0, "zoom": 1.06, "focus": [0.5, 0.5]}]},
          "layers": [plate("atom_close"),
                     sprite("electron", 0.5, 0.5, 0.09, enter="none", keys=orbit_keys(0.52, 0.47, 0.3, 0.12, 4.5, 4.0, 48), sfx="whoosh"),
                     {"type": "counter", "from": 0, "to": 58, "decimals": 0, "suffix": "%", "x": 0.5, "y": 0.13,
                      "size": 150, "color": "accent2", "at": 0.3, "count_dur": 1.6, "enter": "none", "stroke": "#0b0f12", "stroke_width": 8},
                     txt("OF LIGHT SPEED", 0.21, 84, enter="pop", at=1.2, sfx="pop")]})
# 4. panel: relativity -> heavier + orbit shrinks
S.append({"say": "At that speed, relativity kicks in: they get *heavier*, and their orbits *shrink*.",
          "transition": "slide_left", "caption_y": 0.73,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 5.0, "zoom": 1.05, "focus": [0.5, 0.5]}]},
          "layers": [plate("atom_close", blur=12),
                     txt("*RELATIVITY* KICKS IN", 0.11, 96, enter="pop", at=0.0),
                     {"type": "image", "svg": ORBIT, "x": 0.5, "y": 0.35, "w": 0.88, "enter": "slide_up", "at": 0.3, "sfx": "whoosh"},
                     {"type": "image", "svg": tag("PROVEN"), "x": 0.78, "y": 0.52, "w": 0.24, "enter": "pop", "at": 3.2, "sfx": "pop"}]})
# 5. comic beat: side-eye cut-away
S.append({"dur": 1.6, "transition": "cut", "captions": False,
          "layers": [plate("atom_close", blur=10, keys=[{"t": 0, "scale": 1.3}]), dict(close_ved([["side_eye", 0]]), acting="none")],
          "beat": {"kind": "side_eye", "at": 0.1, "dur": 1.45, "who": "ved",
                   "text": "einstein, hiding in\nyour *jewellery box*", "text_y": 0.2}})
# 6. shop wide: gold soaks up blue light (beam panel), customer leans in
S.append({"say": "That tunes gold to soak up *blue* light.",
          "transition": "slide_left", "caption_y": 0.44,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.2, "zoom": 1.05, "focus": [0.5, 0.55]}]},
          "layers": staged("shop_wide",
                           people=[person("shop_wide", "mira", 0.0, 1.6, [["idle", 0], ["point", 1.0]]),
                                   ],
                           fg=True,
                           front=[person("shop_wide", "omar", 1.0, -1.4, [["idle", 0], ["surprised", 1.6]],
                                         walk=[(0, 2.6, -1.6), (1.2, 1.0, -1.4)]),
                                  ved("shop_wide", -1.3, -2.2, [["explain", 0], ["point", 1.0]])],
                           extra_top=[{"type": "image", "svg": BEAM, "x": 0.5, "y": 0.2, "w": 0.86, "enter": "slide_down", "at": 0.1, "sfx": "whoosh"}])})
# 7. shop mid: white - blue = yellow; Omar cheers
S.append({"say": "Take blue out of white light, and what's left looks *yellow*.",
          "transition": "slide_left", "caption_y": 0.6,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.6, "zoom": 1.06, "focus": [0.5, 0.52]}]},
          "layers": staged("shop_mid",
                           people=[person("shop_mid", "mira", 0.1, 1.4, [["idle", 0], ["happy", 2.4]])],
                           fg=True,
                           front=[person("shop_mid", "omar", 0.2, -1.0, [["idle", 0], ["cheer", 2.5]], hops=[[2.5, 0.05, 0.4]]),
                                  ved("shop_mid", -1.1, -1.3, [["explain", 0], ["point", 2.3]])],
                           extra_top=[{"type": "image", "svg": EQ, "x": 0.5, "y": 0.2, "w": 0.86, "enter": "slide_down", "at": 0.1, "sfx": "pop"},
                                      sprite("gold_bar", 0.5, 0.33, 0.24, at=2.4, enter="drop", sfx="ding")])})
# 8. close payoff: ring turns silver, loops back to the hook
S.append({"say": "Without Einstein's relativity, your gold ring would look like *silver*.", "transition": "cut", "caption_y": 0.64,
          "layers": [plate("shop_mid", blur=10, keys=[{"t": 0, "scale": 1.35}, {"t": 4.0, "scale": 1.42}]),
                     close_ved([["warm", 0], ["explain", 1.0], ["smirk", 3.0]]),
                     sprite("gold_ring", 0.74, 0.27, 0.2, at=0.0, enter="none", until=2.4, exit="fade"),
                     sprite("silver_ring", 0.74, 0.27, 0.2, at=2.4, enter="pop", sfx="ding", loop="pulse", loop_amp=0.04),
                     txt("NO EINSTEIN = *SILVER*", 0.13, 100, enter="pop", at=2.4)]})


job = {"id": ID, "title": "Why is gold gold? Blame Einstein ✨",
       "description": "Almost every metal is grey, so why is gold yellow? Gold's nucleus has 79 protons, so its inner electrons move at "
                      "over half the speed of light. Einstein's relativity makes them heavier and pulls their orbits in, which tunes "
                      "gold to absorb blue light. Take blue out of white light and what bounces back looks yellow. Without "
                      "relativity, gold would look silvery, like silver.\n\n"
                      "Sources: Wikipedia, Relativistic quantum chemistry; Fourmilab, What gives gold that mellow glow?; "
                      "Scientific American, Mercury, gold and Einstein's relativity.",
       "tags": ["why is gold yellow", "gold", "relativity", "einstein", "physics", "chemistry", "science explained",
                "special relativity", "explained"],
       "hashtags": ["#physics", "#science"],
       "meta": {"format": "big-question", "topic": "why gold is yellow: 79 protons, inner electrons at ~58% light speed, relativistic mass/orbit contraction shifts absorption into the blue",
                "hook": "question",
                "idea_source": "backlog (ideas.md 'Why is gold yellow?') + viral-shaped (Einstein's relativity explained with a ring) + unique (few Shorts do the relativity angle)",
                "characters": ["ved", "extra"],
                "sources": ["https://en.wikipedia.org/wiki/Relativistic_quantum_chemistry",
                            "https://fourmilab.ch/documents/golden_glow/",
                            "https://www.scientificamerican.com/blog/the-curious-wavefunction/what-does-mercury-being-liquid-at-room-temperature-have-to-do-with-einsteins-theory-of-relativity/"],
                "humour": {"trend": "timeless (no rising trend fit cleanly; recent ones already used this week): side-eye + 'einstein, hiding in your jewellery box' card",
                           "beat": "side_eye", "scene": 5},
                "claims": [
                    {"claim": "gold has 79 protons", "tag": "PROVEN", "source": "https://en.wikipedia.org/wiki/Relativistic_quantum_chemistry"},
                    {"claim": "gold's 1s electrons move at ~58% of light speed (v/c ~ Z/137)", "tag": "PROVEN", "source": "https://en.wikipedia.org/wiki/Relativistic_quantum_chemistry"},
                    {"claim": "relativistic mass increase ~20% contracts s orbitals", "tag": "PROVEN", "source": "https://fourmilab.ch/documents/golden_glow/"},
                    {"claim": "gold's 5d-6s absorption moves from UV into blue; silver's stays in UV, so silver looks silvery", "tag": "PROVEN",
                     "source": "https://www.scientificamerican.com/blog/the-curious-wavefunction/what-does-mercury-being-liquid-at-room-temperature-have-to-do-with-einsteins-theory-of-relativity/"}]},
       "thumbnail": {"title": "BLAME *EINSTEIN*", "title_y": 0.15, "title_size": 160, "max_w": 0.95, "blur": 14,
                     "glow": "#ffcf5a", "glow_x": 0.5, "glow_y": 0.55, "glow_strength": 1.4, "bg_saturation": 1.5,
                     "tint": ["#1f4fb8", "#f08a24"], "tint_amount": 0.35,
                     "bg": [plate("shop_wide")],
                     "fg": [sprite("gold_ring", 0.78, 0.5, 0.3),
                            {"type": "character", "id": "ved", "pose": "surprised", "x": 0.42, "y": 0.93, "h": 0.95, "enter": "none",
                             "acting": "none", "talk": False, "ground": False, "allow_outside_safe": True}]},
       "privacy": "public", "speaker": "ved", "assets_script": J + "assets.py", "scenes": S}
json.dump(job, open(J + "job.json", "w"), indent=1, ensure_ascii=False)
print("scenes", len(S))
