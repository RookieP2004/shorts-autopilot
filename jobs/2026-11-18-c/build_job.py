"""2026-11-18-c: "Meteorites land red-hot? This one grew frost" (myth-bust, the Colby meteorite, 4 July 1917).
2D Ved + two farm folk (Otto, Greta) staged in depth in a Blender Wisconsin farm meadow on a summer evening (wide with sky,
mid on the fresh crater, low close-up on the rock), built from stills + cut-outs. 2D on top: MYTH? stamp, option cards
(RED-HOT cross / FROST tick), a fireball streak, a cream date card, a speed hud that ticks up to 11 km/s then brakes to
~200 m/s with an eqbar, a cut slice with a "< 1 mm" crust callout and melt flakes blowing off, a DARK FLIGHT headline,
the frosted rock with sparkles + FROST stamp, honesty tags.
Facts: Britannica (meteor and meteoroid): entry > 11 km/s (up to 72 km/s); visible flight a few seconds, then braked to
100-200 m/s "dark flight" lasting minutes; a fresh meteorite "can be touched immediately with the bare hand"; fusion crust
made by surface melting. AMNH: fusion crust usually < 1 mm. Armagh Planetarium: outer layer heats and wears away, interior
stays cold. Wisconsin Geological & Natural History Survey: Colby, 6:15 PM 4 July 1917, >200 lb in two stones; residents said
the large stone was "quickly coated with frost" on a hot summer day; the cold of space lingers inside.
Run after the assets exist: python jobs/2026-11-18-c/build_job.py
"""
import json, os, sys
sys.path.insert(0, os.getcwd())
from autopilot.stage import Stage

ID = "2026-11-18-c"
J = f"jobs/{ID}/"
A = J + "assets/"
ST = {n: Stage(A + f"plate_{n}.json") for n in ("farm_wide", "farm_mid", "farm_close")}

OUT = {   # recurring people: same outfit in every shot
    "otto": {"skin": "#e8b48a", "build": "round", "hair": ["#6b4a2e", "short"], "hat": ["straw", "#e8c870"],
             "top": ["#f6efe2", "shirt"], "bottom": ["#3f6fb8", "trousers"], "shoes": "#5a3b2e", "belt": "#5a3b2e"},
    "greta": {"skin": "#f0c8a0", "build": "slim", "hair": ["#c99a3a", "bun"], "hat": ["headscarf", "#3f7fbf"],
              "top": ["#d6483e", "dress"], "bottom": ["#34425c", "skirt"], "shoes": "#25262b", "apron": "#f6efe2"},
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


def staged(set_, behind=(), front=(), extra_top=(), fg=True):
    out = [plate(set_)] + sorted(behind, key=lambda L: -L["_depth"])
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
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 330 84'><rect x='4' y='4' width='322' height='76' rx='38' "
            f"fill='{color}' stroke='#1a1410' stroke-width='5'/><circle cx='44' cy='42' r='16' fill='#1a1410'/>"
            f"<path d='M36,42 l6,7 l11,-14' stroke='{color}' stroke-width='5' fill='none'/>"
            f"<text x='188' y='60' text-anchor='middle' font-size='50' fill='#1a1410' {AN}>{word}</text></svg>")


def tag_layer(x, y, at, word="PROVEN", color="#6fc3c0"):
    return {"type": "image", "svg": tag(word, color), "x": x, "y": y, "w": 0.26, "enter": "pop", "at": at, "sfx": "click"}


def hud(label, y=0.74, **k):
    return {"type": "hud", "label": label, "x": 0.5, "y": y, "enter": "pop", "sfx": "click", "indian": False, **k}


# fireball: bright head on the left, a tapering orange trail to the upper right
FIRE = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 900 260'><defs>"
        "<linearGradient id='t' x1='0' x2='1' y1='0' y2='0'><stop offset='0' stop-color='#fff6d8'/>"
        "<stop offset='0.18' stop-color='#ffb84a'/><stop offset='0.6' stop-color='#f0683a' stop-opacity='0.55'/>"
        "<stop offset='1' stop-color='#f0683a' stop-opacity='0'/></linearGradient>"
        "<radialGradient id='h'><stop offset='0' stop-color='#ffffff'/><stop offset='0.35' stop-color='#fff1b8'/>"
        "<stop offset='0.7' stop-color='#ffb84a' stop-opacity='0.6'/><stop offset='1' stop-color='#ff8a2a' stop-opacity='0'/></radialGradient></defs>"
        "<path d='M120,130 L900,40 L900,220 Z' fill='url(#t)'/><path d='M120,130 L900,95 L900,165 Z' fill='#fff1b8' opacity='0.55'/>"
        "<circle cx='130' cy='130' r='125' fill='url(#h)'/></svg>")


def glowball(color="#ffb84a"):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 300 300'><defs><radialGradient id='g'>"
            f"<stop offset='0' stop-color='#fff6d8'/><stop offset='0.3' stop-color='{color}'/>"
            f"<stop offset='1' stop-color='{color}' stop-opacity='0'/></radialGradient></defs><circle cx='150' cy='150' r='150' fill='url(#g)'/></svg>")


FLAKE = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 60 60'><circle cx='30' cy='30' r='26' fill='#ff8a2a' "
         "stroke='#fff1b8' stroke-width='6'/></svg>")
SPARK = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><path d='M50,0 L58,42 L100,50 L58,58 L50,100 L42,58 L0,50 L42,42 Z' "
         "fill='#ffffff' stroke='#9fd3ff' stroke-width='3'/></svg>")
ARROW = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 300 80'><path d='M10,40 L240,40' stroke='#f6efe2' stroke-width='14' "
         "stroke-linecap='round'/><path d='M220,12 L290,40 L220,68 Z' fill='#f6efe2'/></svg>")

wide, mid, close = ST["farm_wide"], ST["farm_mid"], ST["farm_close"]
CX, CY = mid.point(-0.7, -1.6, 0.25)            # the rock in the crater (mid)
KX, KY = close.point(-0.7, -1.6, 0.25)          # the rock in the crater (close)

S = []
# 0. hook (farm mid): MYTH? stamp + headline + RED-HOT card at frame 0; FROST card ticks; Otto + Greta behind the crater
S.append({"say": "You've been told meteorites land *red-hot*. This one landed in *frost*.",
          "caption_y": 0.42,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.0, "zoom": 1.07, "focus": [0.45, 0.6]}]},
          "layers": staged("farm_mid",
                           behind=[person("farm_mid", "otto", -1.4, -0.2, [["surprised", 0], ["point", 1.6]]),
                                   person("farm_mid", "greta", 0.3, -0.1, [["idle", 0], ["surprised", 2.2]], hops=[[2.3, 0.04, 0.4]])],
                           front=[ved("farm_mid", 0.15, -3.2, [["point", 0], ["explain", 1.6], ["surprised", 2.6]])],
                           extra_top=[{"type": "stamp", "text": "MYTH?", "tone": "red", "angle": -6, "size": 70, "x": 0.5, "y": 0.085,
                                       "at": 0.0, "enter": "none"},
                                      txt("THEY LAND *RED-HOT?*", 0.165, 78, enter="none"),
                                      {"type": "optcard", "label": "you've been told", "text": "RED-HOT", "tone": "red", "x": 0.28, "y": 0.29,
                                       "w": 0.42, "rotate": -3, "enter": "none", "verdict": "cross", "verdict_at": 2.0},
                                      {"type": "optcard", "label": "colby, 1917", "text": "FROST", "tone": "blue", "x": 0.72, "y": 0.29,
                                       "w": 0.42, "rotate": 3, "enter": "pop", "at": 2.3, "sfx": "pop", "verdict": "tick", "verdict_at": 0.6},
                                      {"type": "image", "svg": SPARK, "x": CX + 0.04, "y": CY - 0.04, "w": 0.06, "enter": "pop", "at": 2.6,
                                       "loop": "pulse", "loop_amp": 0.2}])})
# 1. farm wide: the date card; a fireball streaks over the picnic; the farm folk look up; Ved walks in
S.append({"say": "Colby, Wisconsin. Fourth of July, 1917. A fireball over the farms.",
          "transition": "slide_left", "caption_y": 0.45,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.0, "zoom": 1.06, "focus": [0.5, 0.4]}]},
          "layers": [plate("farm_wide"),
                     person("farm_wide", "greta", 2.0, 1.4, [["idle", 0], ["surprised", 1.6], ["point", 2.4]], hops=[[1.7, 0.04, 0.4]]),
                     person("farm_wide", "otto", 3.4, 1.3, [["happy", 0], ["surprised", 1.8]]),
                     ved("farm_wide", 1.0, -3.2, [["explain", 0], ["point", 2.0]], walk=[(0, 4.0, -3.6), (1.4, 1.0, -3.2)]),
                     {"type": "image", "svg": card(
                         "<text x='40' y='80' font-size='56' fill='#1a1410' " + AN + ">COLBY, WISCONSIN</text>"
                         "<text x='40' y='126' font-size='32' fill='#34425c' " + F + ">4 JULY 1917 - 6:15 PM</text>", 760, 150),
                      "x": 0.42, "y": 0.11, "w": 0.7, "rotate": -2, "enter": "slide_right", "at": 0.2, "sfx": "pop"},
                     {"type": "image", "svg": FIRE, "x": 0.95, "y": 0.2, "w": 0.6, "rotate": -24, "enter": "fade", "at": 1.4, "enter_dur": 0.15,
                      "sfx": "whoosh", "keys": [{"t": 0, "x": 0.95, "y": 0.2}, {"t": 1.6, "x": 0.3, "y": 0.36, "ease": "linear"}],
                      "until": 3.2, "exit": "fade"}]})
# 2. farm wide pushed into the sky: entry speed ticks to 11 km/s; the fireball glows big
S.append({"say": "It hit the air at over *eleven kilometres a second*.",
          "transition": "push", "caption_y": 0.45,
          "camera": {"keys": [{"t": 0, "zoom": 1.15, "focus": [0.5, 0.25]}, {"t": 3.2, "zoom": 1.22, "focus": [0.5, 0.25]}]},
          "layers": [plate("farm_wide"),
                     {"type": "image", "svg": FIRE, "x": 0.6, "y": 0.3, "w": 0.95, "rotate": -24, "enter": "fade", "enter_dur": 0.2,
                      "keys": [{"t": 0, "x": 0.66, "y": 0.27}, {"t": 3.2, "x": 0.5, "y": 0.33, "ease": "linear"}], "loop": "pulse", "loop_amp": 0.04},
                     hud("entry speed", y=0.1, steps=[[0, 0], [0.4, 11]], count_dur=1.2, tone="gold", suffix=" km/s",
                         width_of="72 km/s", at=0.0),
                     {"type": "eqbar", "keys": [[1.6, "= *40,000 km/h*"]], "tone": "gold", "x": 0.5, "y": 0.18,
                      "enter": "fade"},
                     tag_layer(0.78, 0.6, 2.0)]})
# 3. the cut slice: only a thin skin melts (< 1 mm) and blows off, taking the heat with it
FLAKES = [(-0.18, -0.14, 0.2), (0.2, -0.1, 0.35), (-0.24, 0.06, 0.5), (0.26, 0.08, 0.65), (0.0, -0.2, 0.8), (-0.3, -0.06, 1.0),
          (0.14, -0.22, 1.15), (0.3, -0.02, 1.3)]
S.append({"say": "But only a skin under a *millimetre* melts... and blows away with the heat.",
          "transition": "slide_up", "caption_y": 0.42,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.5, "zoom": 1.03, "focus": [0.5, 0.5]}]},
          "layers": [plate("farm_close", blur=10, keys=[{"t": 0, "scale": 1.2}]),
                     txt("ONLY THE *SKIN* MELTS", 0.1, 92, enter="pop", at=0.0, sfx="pop"),
                     sprite("slice", 0.5, 0.58, 0.78, enter="pop", at=0.15, sfx="pop",
                            keys=[{"t": 0, "rot": -4}, {"t": 4.0, "rot": 2}])]
                    + [{"type": "image", "svg": FLAKE, "x": 0.5 + dx * 0.9, "y": 0.58 + dy * 0.9, "w": 0.035, "enter": "fade", "at": 1.8 + t,
                        "enter_dur": 0.1, "keys": [{"t": 0, "x": 0.5 + dx * 0.9, "y": 0.58 + dy * 0.9},
                                                   {"t": 1.0, "x": 0.5 + dx * 2.2, "y": 0.58 + dy * 2.2 - 0.04, "ease": "out"}],
                        "until": 1.8 + t + 0.9, "exit": "fade"} for dx, dy, t in FLAKES]
                    + [{"type": "image", "svg": ARROW, "x": 0.18, "y": 0.43, "w": 0.16, "rotate": 100, "enter": "pop", "at": 0.9, "sfx": "click"},
                       hud("melted crust", x=0.4, y=0.24, text="< 1 mm", tone="red", at=0.8, width_of="< 1 mm"),
                       hud("inside", x=0.5, y=0.86 - 0.1, text="NOT MELTED", tone="blue", at=2.4, width_of="NOT MELTED"),
                       tag_layer(0.8, 0.3, 1.2)]})
# 4. farm wide: glow fades within seconds, the rock brakes to ~200 m/s and falls dark for minutes
S.append({"say": "The glow lasts seconds. Then air brakes it, and it falls *dark* for minutes.",
          "transition": "slide_left", "caption_y": 0.45,
          "camera": {"keys": [{"t": 0, "zoom": 1.06, "focus": [0.5, 0.35]}, {"t": 4.6, "zoom": 1.0, "focus": [0.5, 0.5]}]},
          "layers": [plate("farm_wide"),
                     {"type": "image", "svg": glowball(), "x": 0.62, "y": 0.26, "w": 0.3, "enter": "none", "until": 1.3, "exit": "fade",
                      "keys": [{"t": 0, "x": 0.62, "y": 0.26}, {"t": 1.3, "x": 0.58, "y": 0.33}]},
                     sprite("meteorite", 0.62, 0.26, 0.09, keys=[{"t": 0, "x": 0.62, "y": 0.26, "rot": 0},
                                                                 {"t": 1.3, "x": 0.58, "y": 0.33, "rot": 40},
                                                                 {"t": 4.4, "x": 0.4, "y": 0.75, "rot": 300, "ease": "in"}]),
                     person("farm_wide", "greta", 2.0, 1.4, [["point", 0], ["surprised", 2.6]]),
                     person("farm_wide", "otto", 3.4, 1.3, [["surprised", 0], ["shrug", 2.0]]),
                     hud("speed", y=0.1, steps=[[0, 11000], [1.0, 200]], count_dur=1.0, tone="gold", suffix=" m/s",
                         width_of="11,000 m/s", enter="none"),
                     {"type": "eqbar", "keys": [[0.2, "glow: *seconds*"], [1.9, "dark fall: *minutes*"]], "tone": "blue",
                      "x": 0.5, "y": 0.18, "enter": "fade"},
                     txt("DARK *FLIGHT*", 0.27, 100, enter="pop", at=1.9, sfx="pop"),
                     {"type": "tracker", "n": 3, "done": [0.3, 1.4, 2.6], "x": 0.5, "y": 0.66, "at": 0.1, "enter": "fade"}]})
# 5. farm close: the rock in its crater; the inside is still space-cold, so the summer air froze onto it (frost fades in)
S.append({"say": "Inside, it's still cold from space. So the summer air *froze* onto it.",
          "transition": "cut", "caption_y": 0.45,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.55]}, {"t": 4.0, "zoom": 1.04, "focus": [0.5, 0.6]}]},
          "layers": [plate("farm_close"),
                     sprite("meteorite_frost", KX, KY, 0.5, enter="fade", at=1.8, enter_dur=1.0),
                     hud("inside the rock", y=0.13, text="SPACE-COLD", tone="blue", at=0.2, width_of="SPACE-COLD")]
                    + [{"type": "image", "svg": SPARK, "x": KX + dx, "y": KY + dy, "w": 0.05, "enter": "pop", "at": 2.2 + k * 0.2,
                        "sfx": "click" if k == 0 else None, "loop": "pulse", "loop_amp": 0.25}
                       for k, (dx, dy) in enumerate(((-0.14, -0.06), (0.12, -0.08), (0.02, -0.12), (-0.05, 0.05)))]
                    + [{"type": "stamp", "text": "FROST", "tone": "blue", "angle": -7, "size": 96, "x": 0.5, "y": 0.25,
                        "at": 2.6, "sfx": "thud"},
                       tag_layer(0.8, 0.31, 3.0, "REPORTED", "#f2b04a")]})
# 6. comic beat: deadpan cut-away
S.append({"dur": 1.6, "transition": "cut", "captions": False,
          "layers": [plate("farm_mid", blur=10, keys=[{"t": 0, "scale": 1.35}]), dict(close_ved([["deadpan", 0]]), acting="none")],
          "beat": {"kind": "deadpan", "at": 0.1, "dur": 1.45, "who": "ved",
                   "text": "4th of July BBQ:\nice delivered *from space*", "text_y": 0.2}})
# 7. close payoff: fire in the sky, frost on the ground (loops to the RED-HOT hook)
S.append({"say": "Fire in the sky. Frost on the ground. Red-hot? This one was *ice-cold*.",
          "transition": "cut", "caption_y": 0.62,
          "layers": [plate("farm_mid", blur=10, keys=[{"t": 0, "scale": 1.35}, {"t": 4.0, "scale": 1.42}]),
                     close_ved([["explain", 0], ["point", 1.8], ["smirk", 3.4]]),
                     {"type": "optcard", "label": "in the sky", "text": "FIRE", "tone": "gold", "x": 0.28, "y": 0.12,
                      "w": 0.4, "rotate": -3, "enter": "pop", "at": 0.1, "sfx": "pop"},
                     {"type": "optcard", "label": "on the ground", "text": "FROST", "tone": "blue", "x": 0.72, "y": 0.12,
                      "w": 0.4, "rotate": 3, "enter": "pop", "at": 1.1, "sfx": "pop"},
                     {"type": "stamp", "text": "MYTH BUSTED", "tone": "green", "angle": -6, "size": 80, "x": 0.5, "y": 0.25,
                      "at": 2.8, "sfx": "thud"}]})

job = {"id": ID, "title": "Meteorites land red-hot? This one grew frost 🧊",
       "description": "You've been told meteorites hit the ground red-hot. On 4 July 1917 a meteorite fell on Colby, Wisconsin, "
                      "and people who found it said it was quickly coated with frost on a hot summer evening. Why: a meteoroid "
                      "enters the air at more than 11 km/s, but only a skin less than a millimetre thick melts, and that melt "
                      "blows away, taking the heat with it. The glow lasts seconds; then the air brakes the rock to about "
                      "100-200 m/s and it falls 'dark' for minutes. Inside it is still cold from space, so fresh meteorites can "
                      "be touched with a bare hand, and some even frost over.\n\n"
                      "Sources: Encyclopaedia Britannica (meteor and meteoroid); Wisconsin Geological & Natural History Survey "
                      "(Wisconsin meteorites: Colby); AMNH (fusion crust); Armagh Observatory and Planetarium.",
       "tags": ["meteorite", "meteorites", "meteor", "fireball", "space facts", "myth busted", "Colby meteorite",
                "science facts", "astronomy"],
       "hashtags": ["#science", "#space"],
       "instagram": {"hashtags": ["#space", "#meteorite", "#astronomy", "#sciencefacts", "#explained"]},
       "meta": {"format": "myth-bust", "topic": "the red-hot meteorite myth: Colby, Wisconsin (4 July 1917) meteorite reported "
                                                "coated with frost; entry >11 km/s but only a <1 mm skin melts and ablates away; "
                                                "glow lasts seconds, then 100-200 m/s dark flight for minutes; interior still cold "
                                                "from space, touchable on landing",
                "hook": "you've been told X",
                "idea_source": "viral-shaped + unique + timely: a famous 'everyone knows' image (red-hot space rock) flipped into "
                               "frost; backlog idea, runner-up of the meteor videos, Leonid/meteor season this week; this week's "
                               "'you've been told X' hook test",
                "characters": ["ved", "extra"],
                "sources": ["https://www.britannica.com/science/meteor/Introduction",
                            "https://home.wgnhs.wisc.edu/wisconsin-geology/meteorites",
                            "https://research.amnh.org/~debel/eduSource1/HallPix/fusionCrust1.htm",
                            "https://armaghplanet.com/10-amazing-myths-about-meteorites.html"],
                "humour": {"trend": "timeless dry aside (no rising meme fit; 'I Got So Mad' / 'My Type Quiz' already used this "
                                    "week): deadpan + '4th of July BBQ: ice delivered from space'",
                           "beat": "deadpan", "scene": 6},
                "claims": [
                    {"claim": "meteoroids enter the atmosphere at more than 11 km/s (up to ~72 km/s)", "tag": "PROVEN",
                     "source": "https://www.britannica.com/science/meteor/Introduction"},
                    {"claim": "only the surface melts into a fusion crust, usually less than 1 mm thick; the melt ablates away", "tag": "PROVEN",
                     "source": "https://research.amnh.org/~debel/eduSource1/HallPix/fusionCrust1.htm"},
                    {"claim": "the glow lasts seconds; then the air brakes the rock to 100-200 m/s and it falls for minutes (dark flight)", "tag": "PROVEN",
                     "source": "https://www.britannica.com/science/meteor/Introduction"},
                    {"claim": "the interior keeps the cold of space; fresh meteorites can be touched with a bare hand", "tag": "PROVEN",
                     "source": "https://home.wgnhs.wisc.edu/wisconsin-geology/meteorites"},
                    {"claim": "the Colby, Wisconsin meteorite (6:15 PM, 4 July 1917) was reported by residents to be quickly coated with frost", "tag": "REPORTED",
                     "source": "https://home.wgnhs.wisc.edu/wisconsin-geology/meteorites"}]},
       "thumbnail": {"title": "RED-HOT? *FROST!*", "title_y": 0.15, "title_size": 170, "max_w": 0.95, "blur": 14,
                     "glow": "#ffb35a", "glow_x": 0.5, "glow_y": 0.5, "glow_strength": 1.3, "bg_saturation": 1.4,
                     "tint": ["#1f6fb8", "#f08a24"], "tint_amount": 0.28,
                     "bg": [plate("farm_wide"),
                            {"type": "image", "svg": FIRE, "x": 0.62, "y": 0.3, "w": 0.95, "rotate": -24, "enter": "none"}],
                     "fg": [sprite("meteorite_frost", 0.5, 0.42, 0.62),
                            {"type": "character", "id": "ved", "pose": "surprised", "x": 0.5, "y": 0.95, "h": 0.8, "enter": "none",
                             "acting": "none", "talk": False, "ground": False, "allow_outside_safe": True}]},
       "privacy": "public", "speaker": "ved", "assets_script": J + "assets.py", "scenes": S}
json.dump(job, open(J + "job.json", "w"), indent=1, ensure_ascii=False)
print("scenes", len(S))
