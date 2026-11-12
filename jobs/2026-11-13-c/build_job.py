"""2026-11-13-c: "How could we really reach another star?" (frontier).
2D Ved + a dish operator staged in depth inside Blender sets (a desert radio-dish station at dusk from 2 angles, a laser
array firing at the sky, deep space with a red dwarf) built from stills + cut-outs; the probe and the light sail are animated
cut-outs; honesty tags, distance bar, signal card and counters are 2D.
Run after the assets exist: python jobs/2026-11-13-c/build_job.py
"""
import json, os, sys
sys.path.insert(0, os.getcwd())
from autopilot.stage import Stage

ID = "2026-11-13-c"
J = f"jobs/{ID}/"
A = J + "assets/"
ST = {n: Stage(A + f"plate_{n}.json") for n in ("dish_wide", "dish_mid")}

OUT = {   # recurring people: same outfit in every shot
    "ana": {"skin": "#c68a5e", "top": ["#6fc3c0", "jacket"], "bottom": ["#34425c", "trousers"], "hair": ["#1a1410", "long"],
            "hat": ["cap", "#f2b04a"], "shoes": "#25262b"},                                   # the dish operator
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


def staged(set_, people=(), extra_top=()):
    out = [plate(set_)] + sorted(people, key=lambda L: -L["_depth"]) + list(extra_top)
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


def label(t, color, w=620, size=62):
    return card(f"<text x='{w/2}' y='92' text-anchor='middle' font-size='{size}' fill='{color}' {AN}>{t}</text>", w, 140)


TAGC = {"PROVEN": "#46965a", "R&amp;D": "#2f6fd6", "SPECULATION": "#d9534f"}


def tag(word, at=0.0):
    """Small honesty pill, top-left."""
    w = 150 + 40 * len(word.replace("&amp;", "&"))
    c = TAGC[word]
    svg = (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {w} 110'><rect x='5' y='5' width='{w-10}' height='100' rx='50' "
           f"fill='{c}' stroke='#1a1410' stroke-width='6'/><circle cx='55' cy='55' r='16' fill='#f6efe2'/>"
           f"<text x='{(w+60)/2}' y='77' text-anchor='middle' font-size='60' fill='#f6efe2' {AN}>{word}</text></svg>")
    return {"type": "image", "svg": svg, "x": 0.06 + w / 110 * 0.085 / 2, "y": 0.115, "w": w / 110 * 0.085,
            "enter": "pop", "at": at, "sfx": "click"}


# the signal card: Earth -> Voyager, a full day each way
SIGNAL = card(
    "<text x='450' y='72' text-anchor='middle' font-size='44' fill='#1a1410' " + F + ">ONE MESSAGE</text>"
    "<circle cx='110' cy='190' r='52' fill='#2f6fd6' stroke='#1a1410' stroke-width='6'/>"
    "<path d='M80,170 q20,-20 40,0 t30,20' fill='none' stroke='#46965a' stroke-width='14'/>"
    "<text x='110' y='290' text-anchor='middle' font-size='34' fill='#34425c' " + F + ">EARTH</text>"
    "<line x1='180' y1='190' x2='720' y2='190' stroke='#34425c' stroke-width='6' stroke-dasharray='18 14'/>"
    "<rect x='760' y='176' width='70' height='28' rx='6' fill='#d9a441' stroke='#1a1410' stroke-width='5'/>"
    "<ellipse cx='795' cy='160' rx='46' ry='14' fill='#eef1f4' stroke='#1a1410' stroke-width='5'/>"
    "<text x='795' y='290' text-anchor='middle' font-size='34' fill='#34425c' " + F + ">VOYAGER 1</text>"
    "<text x='450' y='160' text-anchor='middle' font-size='64' fill='#d9534f' " + AN + ">24 HOURS</text>"
    "<text x='450' y='280' text-anchor='middle' font-size='34' fill='#1a1410' " + F + ">EACH WAY</text>", 900, 330)

# the distance bar: Voyager's whole trip is a hair next to Earth; Proxima at the far end
BAR = card(
    "<text x='450' y='70' text-anchor='middle' font-size='42' fill='#1a1410' " + F + ">TO SCALE</text>"
    "<line x1='80' y1='170' x2='820' y2='170' stroke='#34425c' stroke-width='10'/>"
    "<circle cx='80' cy='170' r='22' fill='#2f6fd6' stroke='#1a1410' stroke-width='5'/>"
    "<line x1='81' y1='120' x2='81' y2='220' stroke='#d9a441' stroke-width='4'/>"
    "<circle cx='820' cy='170' r='30' fill='#ff6a3a' stroke='#1a1410' stroke-width='5'/>"
    "<text x='110' y='265' font-size='30' fill='#c97a1a' " + F + ">VOYAGER: 49 YEARS</text>"
    "<text x='820' y='265' text-anchor='end' font-size='34' fill='#d9534f' " + AN + ">PROXIMA</text>"
    "<text x='820' y='112' text-anchor='end' font-size='40' fill='#1a1410' " + AN + ">4.2 LIGHT-YEARS</text>", 900, 300)

# sunlight pushes a sail (IKAROS, 2010)
PUSH = card(
    "<circle cx='120' cy='170' r='70' fill='#f2b04a' stroke='#1a1410' stroke-width='6'/>"
    + "".join(f"<line x1='210' y1='{110 + k*30}' x2='520' y2='{110 + k*30}' stroke='#f2b04a' stroke-width='8' stroke-dasharray='26 16'/>" for k in range(5))
    + "<polygon points='540,80 560,90 560,260 540,270' fill='#9aa3ad' stroke='#1a1410' stroke-width='5'/>"
    "<line x1='600' y1='175' x2='760' y2='175' stroke='#d9534f' stroke-width='12'/>"
    "<polygon points='800,175 755,150 755,200' fill='#d9534f'/>"
    "<text x='680' y='255' text-anchor='middle' font-size='34' fill='#1a1410' " + F + ">A GENTLE PUSH</text>"
    "<text x='450' y='60' text-anchor='middle' font-size='40' fill='#1a1410' " + AN + ">IKAROS, 2010: IT WORKED</text>", 900, 300)

S = []
# 0. hook (dish mid): the question at frame 0, Ved arms crossed on the station's apron
S.append({"say": "How could we *really* reach another star? Start with our best try.",
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.0, "zoom": 1.06, "focus": [0.5, 0.52]}]},
          "layers": staged("dish_mid",
                           people=[ved("dish_mid", 0.9, 0.4, [["crossed", 0], ["explain", 2.2], ["point", 3.4]])],
                           extra_top=[txt("HOW COULD WE *REALLY* REACH A STAR?", 0.21, 104, enter="none")])})
# 1. deep space: Voyager drifts across, the light-day counter
S.append({"say": "Voyager 1, launched in 1977. On November 18th, it hits one *light-day* from Earth.",
          "transition": "slide_left", "caption_y": 0.52,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 5.5, "zoom": 1.06, "focus": [0.5, 0.5]}]},
          "layers": [plate("deep"), tag("PROVEN", 0.2),
                     sprite("probe", 0.5, 0.68, 0.62, sfx="whoosh", keys=[{"t": 0, "x": -0.3, "rot": -8}, {"t": 2.0, "x": 0.45, "rot": -4, "ease": "out"},
                                                                         {"t": 6.0, "x": 0.56, "rot": -2, "ease": "linear"}]),
                     txt("VOYAGER 1 *1977*", 0.2, 110, enter="pop", at=0.3, sfx="pop"),
                     {"type": "counter", "from": 0, "to": 25.9, "decimals": 1, "suffix": " BILLION KM", "x": 0.5, "y": 0.37,
                      "size": 92, "color": "accent", "at": 2.6, "count_dur": 1.6, "enter": "pop", "sfx": "pop"}]})
# 2. dish wide: the operator waits for the reply, signal card
S.append({"say": "Its signal now takes a full *day* to reach us. Replies? Another day.",
          "transition": "slide_left", "caption_y": 0.44,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.55]}, {"t": 4.5, "zoom": 1.06, "focus": [0.5, 0.56]}]},
          "layers": staged("dish_wide",
                           people=[person("dish_wide", "ana", 1.6, 1.4, [["idle", 0], ["point", 0.8], ["shrug", 3.2]]),
                                   ved("dish_wide", -0.4, -1.6, [["explain", 0], ["think", 3.0]],
                                       walk=[(0, -2.6, -1.8), (1.2, -0.4, -1.6)])],
                           extra_top=[tag("PROVEN", 0.1),
                                      {"type": "image", "svg": SIGNAL, "x": 0.5, "y": 0.22, "w": 0.78, "enter": "pop", "at": 0.6, "sfx": "pop"}])})
# 3. comic beat: side-eye cut-away
S.append({"dur": 1.8, "transition": "cut", "captions": False,
          "layers": [plate("dish_mid", blur=10, keys=[{"t": 0, "scale": 1.35}]), dict(close_ved([["side_eye", 0]]), acting="none")],
          "beat": {"kind": "side_eye", "at": 0.1, "dur": 1.6, "who": "ved",
                   "text": "texting Voyager:\n*seen... tomorrow*", "text_y": 0.2}})
# 4. deep space: the distance bar + 74,000 years
S.append({"say": "The nearest star is *4.2 light-years* away. At Voyager's speed: *74,000 years*.",
          "transition": "zoom", "caption_y": 0.6,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 6.0, "zoom": 1.12, "focus": [0.62, 0.42]}]},
          "layers": [plate("deep"), tag("PROVEN", 0.1),
                     {"type": "image", "svg": BAR, "x": 0.5, "y": 0.24, "w": 0.8, "enter": "slide_up", "at": 0.2, "sfx": "pop"},
                     {"type": "counter", "from": 0, "to": 74000, "decimals": 0, "suffix": " YEARS", "x": 0.5, "y": 0.42,
                      "size": 120, "color": "danger", "at": 3.4, "count_dur": 1.4, "enter": "zoom", "sfx": "boom"}]})
# 5. dish mid: ride light (IKAROS), the sail floats in
S.append({"say": "So forget fuel: ride *light*. Sunlight pushed Japan's IKAROS sail in 2010.",
          "transition": "slide_left", "caption_y": 0.44,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 5.0, "zoom": 1.05, "focus": [0.48, 0.52]}]},
          "layers": staged("dish_mid",
                           people=[ved("dish_mid", 0.4, -1.6, [["welcome", 0], ["point", 1.4], ["explain", 3.4]])],
                           extra_top=[tag("PROVEN", 0.1),
                                      txt("RIDE *LIGHT*", 0.2, 130, enter="pop", at=1.2, sfx="pop"),
                                      {"type": "image", "svg": PUSH, "x": 0.5, "y": 0.3, "w": 0.74, "enter": "slide_up", "at": 2.6, "sfx": "pop"},
                                      sprite("sail", 0.76, 0.56, 0.2, at=1.6, enter="pop", sfx="pop", loop="float", loop_amp=0.012, rotate=10)])})
# 6. lasers: Breakthrough Starshot, the sail rides the beams up
S.append({"say": "Breakthrough Starshot's plan: giant lasers firing gram-sized sails to *a fifth* of light speed.",
          "transition": "flash", "caption_y": 0.5,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 6.5, "zoom": 1.08, "focus": [0.5, 0.45]}]},
          "layers": [plate("lasers"), tag("R&amp;D", 0.1),
                     txt("BREAKTHROUGH *STARSHOT*", 0.19, 100, enter="pop", at=0.3, sfx="pop"),
                     sprite("sail", 0.5, 0.62, 0.3, at=2.6, sfx="whoosh",
                            keys=[{"t": 0, "y": 0.72, "scale": 1.0}, {"t": 3.0, "y": 0.34, "scale": 0.22, "ease": "in"}]),
                     {"type": "image", "svg": label("1 GRAM  -  20% LIGHT SPEED", "#2f6fd6", 900, 60), "x": 0.5, "y": 0.33, "w": 0.74,
                      "enter": "pop", "at": 3.6, "sfx": "ding"}]})
# 7. deep space: the sail streaks to the red star; twenty years
S.append({"say": "That's Proxima in about *twenty years*.", "transition": "cut", "caption_y": 0.6,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 2.6, "zoom": 1.1, "focus": [0.62, 0.42]}]},
          "layers": [plate("deep"), tag("R&amp;D", 0.0),
                     sprite("sail", 0.3, 0.7, 0.16, sfx="whoosh",
                            keys=[{"t": 0, "x": 0.18, "y": 0.78, "scale": 1.0}, {"t": 1.8, "x": 0.71, "y": 0.27, "scale": 0.15, "ease": "in"}]),
                     {"type": "counter", "from": 74000, "to": 20, "decimals": 0, "suffix": " YEARS", "x": 0.5, "y": 0.42,
                      "size": 130, "color": "accent2", "at": 0.4, "count_dur": 1.2, "enter": "pop", "sfx": "ding"}]})
# 8. dish wide: the catch, three problem cards, ON HOLD stamp; the operator slumps
S.append({"say": "The catch? *100 gigawatts* of lasers, and a sail that won't melt. Starshot is on hold.",
          "transition": "slide_left", "caption_y": 0.46,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.55]}, {"t": 6.0, "zoom": 1.06, "focus": [0.5, 0.55]}]},
          "layers": staged("dish_wide",
                           people=[person("dish_wide", "ana", 1.6, 1.4, [["idle", 0], ["surprised", 1.6], ["sad", 4.6]]),
                                   ved("dish_wide", -0.6, -1.6, [["serious", 0], ["explain", 1.6], ["crossed", 4.4]])],
                           extra_top=[tag("R&amp;D", 0.1),
                                      {"type": "image", "svg": label("100 GIGAWATTS", "#d9534f", 700, 70), "x": 0.32, "y": 0.17, "w": 0.48,
                                       "enter": "pop", "at": 1.0, "sfx": "pop", "rotate": -3},
                                      {"type": "image", "svg": label("SAIL CAN'T MELT", "#c97a1a", 700, 66), "x": 0.64, "y": 0.25, "w": 0.46,
                                       "enter": "pop", "at": 2.6, "sfx": "pop", "rotate": 3},
                                      {"type": "image", "svg": stamp("ON HOLD"), "x": 0.5, "y": 0.34, "w": 0.5, "rotate": -6,
                                       "enter": "zoom", "at": 4.4, "sfx": "boom"}])})
# 9. close payoff: where science ends
S.append({"say": "From here, we're guessing: decades away. But the physics? It *works*.", "transition": "cut",
          "caption_y": 0.64,
          "layers": [plate("lasers", blur=10, keys=[{"t": 0, "scale": 1.35}, {"t": 4.5, "scale": 1.42}]),
                     close_ved([["think", 0], ["explain", 1.8], ["smirk", 3.4]]),
                     tag("SPECULATION", 0.1),
                     txt("PHYSICS: *YES*", 0.21, 120, enter="pop", at=3.2, sfx="ding")]})

job = {"id": ID, "title": "How could we REALLY reach another star? 🚀",
       "description": "Voyager 1 reaches one light-day from Earth on 18 November 2026, after 49 years. At that speed the nearest star "
                      "would take ~74,000 years. Light sails could cut it to ~20 years, if we can build the lasers.\n\n"
                      "Sources: EarthSky / NASA on Voyager 1's light-day milestone; Big Think on Voyager's speed and travel times; "
                      "JAXA on the IKAROS solar sail; Scientific American on Breakthrough Starshot; Caltech on lightsail tests.",
       "tags": ["voyager 1", "light day", "interstellar travel", "breakthrough starshot", "light sail", "proxima centauri",
                "space", "science explained"],
       "hashtags": ["#space", "#science"],
       "meta": {"format": "frontier", "topic": "how we could really reach another star: Voyager 1 at one light-day vs laser light sails (Starshot)",
                "hook": "question", "idea_source": "trending + viral: Voyager 1 hits one light-day on 2026-11-18 (EarthSky, NASA); owner's frontier examples",
                "characters": ["ved", "extra"],
                "sources": ["https://earthsky.org/space/voyager-1-1-light-day-from-earth-november-17-18-2026/",
                            "https://www.sciencedaily.com/releases/2026/11/261105224547.htm",
                            "https://bigthink.com/strange-maps/voyager-1/",
                            "https://en.wikipedia.org/wiki/IKAROS",
                            "https://global.jaxa.jp/projects/sas/ikaros/",
                            "https://www.scientificamerican.com/article/the-quiet-demise-of-breakthrough-starshot-a-billionaires-interstellar/",
                            "https://aerospace.caltech.edu/news/the-pressure-to-explore-caltech-researchers-take-first-experimental-steps-toward-lightsails-that-could-reach-distant-star-systems"],
                "humour": {"trend": "'Tony Stark head turn' knowing side-glance (rising early Nov 2026), as a side-eye + 'seen... tomorrow' card",
                           "beat": "side_eye", "scene": 3},
                "claims": [
                    {"claim": "Voyager 1 launched 5 Sep 1977, reaches one light-day (~25.9 billion km) on 18 Nov 2026", "tag": "PROVEN",
                     "source": "https://earthsky.org/space/voyager-1-1-light-day-from-earth-november-17-18-2026/"},
                    {"claim": "a signal takes ~24 h each way", "tag": "PROVEN", "source": "https://www.sciencedaily.com/releases/2026/11/261105224547.htm"},
                    {"claim": "Proxima is ~4.2 ly away; ~74,000 years at Voyager's speed", "tag": "PROVEN", "source": "https://bigthink.com/strange-maps/voyager-1/"},
                    {"claim": "IKAROS (JAXA, 2010) was propelled by sunlight on a sail", "tag": "PROVEN", "source": "https://en.wikipedia.org/wiki/IKAROS"},
                    {"claim": "Starshot plan: ~100 GW laser array, gram-scale sails, ~20% c, ~20 years to Alpha Centauri; program on hold", "tag": "R&D",
                     "source": "https://www.scientificamerican.com/article/the-quiet-demise-of-breakthrough-starshot-a-billionaires-interstellar/"},
                    {"claim": "decades away at least", "tag": "SPECULATION", "source": "our what-if"}]},
       "privacy": "public", "speaker": "ved", "assets_script": J + "assets.py", "scenes": S}
json.dump(job, open(J + "job.json", "w"), indent=1, ensure_ascii=False)
print("scenes", len(S))
