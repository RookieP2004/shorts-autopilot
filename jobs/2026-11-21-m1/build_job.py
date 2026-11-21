"""2026-11-21-m1 (manual showcase run, owner: "best everything, 35 s"): "Your Wi-Fi and your microwave use the same wave".
Every toolkit at once, mixed into the house style: the bright town kitchen in Blender (3 angles) with Ved and two
townspeople, glossy hero cut-outs, hud chips + eqbar, a Reelsmith Balance look (1,000 W vs 0.1 W), a NumberSlam motion
clip (10,000x), a Cutaway 3D cutaway of the oven (magnetron, waveguide, water), the night plate inside the cavity with
wiggling water-molecule cut-outs, option cards + a MYTH stamp, a Reelsmith Whiteboard (why the door mesh holds the wave)
with Ved drawn in marker, the comic beat, and a KineticTitle payoff; real-instrument score, stings, sound library.
Facts: Wi-Fi uses the 2.4 GHz band, ovens 2.45 GHz (ISM band, 1947); ovens ~700-1,100 W vs routers capped ~100 mW EIRP
(ETSI EN 300 328 / FCC) = ~10,000x; water molecules are polar and keep trying to flip with the field (dielectric heating);
the "resonant frequency of water" is a folk myth (water's loss peaks ~10-20 GHz; 2.45 GHz reaches deeper into food);
wavelength ~12.2 cm vs door-screen holes of ~1 mm ("waveguide below cutoff"); ovens leak a little and can disrupt
2.4 GHz Wi-Fi nearby. Sources in meta.sources.
Run after the assets exist: python jobs/2026-11-21-m1/build_job.py
"""
import json, os, sys
sys.path.insert(0, os.getcwd())
from autopilot.stage import Stage

ID = "2026-11-21-m1"
J = f"jobs/{ID}/"
A = J + "assets/"
ST = {n: Stage(A + f"plate_{n}.json") for n in ("kitchen_wide", "kitchen_mw", "kitchen_router")}
OUT = {   # recurring townspeople: same outfit in every shot
    "priya": {"skin": "#c68a5e", "build": "slim", "hair": ["#1a1410", "long"], "top": ["#6fc3c0", "tshirt"],
              "bottom": ["#34425c", "trousers"], "shoes": "#25262b"},
    "rao": {"skin": "#a8714a", "build": "round", "hair": ["#6b6b6b", "short"], "hat": ["chef", "#f6efe2"],
            "top": ["#f2b04a", "shirt"], "bottom": ["#5a4632", "trousers"], "shoes": "#25262b", "apron": "#f6efe2"},
}
AN = "font-family='Anton, DejaVu Sans, sans-serif'"
GOLD, RED, GREEN, BLUE, CREAM, INK = "#f2b04a", "#d9534f", "#46c47a", "#57b8ff", "#f6efe2", "#1a1410"


def plate(name, blur=0, **k):
    return {"type": "image", "path": A + f"plate_{name}.png", "x": 0.5, "y": 0.5, "w": 1.0, "enter": "none", "blur": blur, **k}


def sprite(name, x, y, w, **k):
    return {"type": "image", "path": A + name + ".png", "x": x, "y": y, "w": w, "enter": k.pop("enter", "none"), **k}


def txt(t, y, size=96, **k):
    return {"type": "text", "text": t, "font": "display", "x": 0.5, "y": y, "size": size, "max_w": 0.9,
            "stroke": "#0b0f12", "stroke_width": 7, **k}


def person(set_, who, wx, wy, acting, walk=None, hops=None, **k):
    st = ST[set_]
    p = st.place(wx, wy, "extra")
    L = {"type": "character", "id": "extra", "pose": acting[0][0], "x": p["x"], "y": p["y"], "h": p["h"], "enter": "none",
         "acting": acting, "talk": False, "rig_args": {"outfit": OUT[who]}, "allow_outside_safe": True}
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
         "acting": acting, "allow_outside_safe": True}
    if walk:
        L["keys"] = st.walk(walk, p, "ved")
    if hops:
        L["hops"] = hops
    L.update(k)
    return L


def close_ved(acting, **k):
    return {"type": "character", "id": "ved", "pose": acting[0][0], "x": 0.5, "y": 0.8, "h": 1.06, "enter": "none",
            "acting": acting, "ground": False, "allow_outside_safe": True, **k}


def hud(label, y, **k):
    return {"type": "hud", "label": label, "x": 0.5, "y": y, "enter": "pop", "sfx": "click", "indian": False, **k}


def chip(label, value, color):
    """A small dark spec chip for the hook (band labels, not numbers that tick)."""
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 360 140'>"
            f"<rect x='5' y='5' width='350' height='130' rx='26' fill='#10161e' stroke='{color}' stroke-width='5'/>"
            f"<text x='180' y='48' text-anchor='middle' font-size='30' fill='#c9d3e0' {AN} letter-spacing='2'>{label}</text>"
            f"<text x='180' y='112' text-anchor='middle' font-size='62' fill='{color}' {AN}>{value}</text></svg>")


WAVE = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 600 120'>"
        "<path d='M10,60 Q47,0 85,60 T160,60 T235,60 T310,60 T385,60 T460,60 T535,60 T590,60' stroke='#f2b04a' stroke-width='12' "
        "fill='none' stroke-linecap='round'/>"
        "<path d='M10,60 Q47,0 85,60 T160,60 T235,60 T310,60 T385,60 T460,60 T535,60 T590,60' stroke='#fff3c4' stroke-width='4' "
        "fill='none' stroke-linecap='round'/></svg>")


def rings(color=BLUE):
    """Wi-Fi rings spreading out from the router (drawn as arcs, getting fainter)."""
    arcs = "".join(f"<path d='M{300 - r},{300} A{r},{r} 0 0 1 {300 + r},{300}' stroke='{color}' stroke-width='{14 - k * 2}' "
                   f"fill='none' stroke-linecap='round' opacity='{0.95 - k * 0.17:.2f}'/>" for k, r in enumerate((70, 130, 190, 250, 290)))
    return f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 600 320'>{arcs}<circle cx='300' cy='300' r='16' fill='{color}'/></svg>"


PHONE = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 300 560'>"
         "<rect x='6' y='6' width='288' height='548' rx='40' fill='#14161b' stroke='#3a3d45' stroke-width='6'/>"
         "<rect x='22' y='60' width='256' height='440' rx='16' fill='#1e2a3a'/>"
         "<rect x='22' y='60' width='256' height='150' rx='16' fill='#2f4f6e'/>"
         "<polygon points='130,105 130,165 175,135' fill='#f6efe2' opacity='0.85'/>"
         "<rect x='40' y='236' width='220' height='14' rx='7' fill='#3a4a5e'/><rect x='40' y='236' width='70' height='14' rx='7' fill='#d9534f'/>"
         f"<text x='150' y='450' text-anchor='middle' font-size='30' fill='#c9d3e0' {AN} letter-spacing='2'>BUFFERING...</text>"
         "<rect x='120' y='24' width='60' height='10' rx='5' fill='#2a2d34'/></svg>")
SPINNER = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 200'>"
           "<circle cx='100' cy='100' r='70' stroke='#3a4a5e' stroke-width='18' fill='none'/>"
           "<path d='M100,30 A70,70 0 0 1 170,100' stroke='#f6efe2' stroke-width='18' fill='none' stroke-linecap='round'/></svg>")


def molecules():
    """A field of water molecules over the cavity plate, each wiggling at its own pace (they try to flip with the wave)."""
    out = []
    spots = [(0.16, 0.3), (0.5, 0.29), (0.84, 0.31), (0.32, 0.41), (0.68, 0.4), (0.13, 0.5), (0.87, 0.49), (0.5, 0.37)]
    for k, (x, y) in enumerate(spots):
        out.append(sprite("molecule", x, y, 0.15 + 0.02 * (k % 3), enter="pop", at=0.12 * k, sfx="pop" if k % 3 == 0 else "none",
                          rotate=(k * 47) % 360 - 180, loop="wiggle", loop_speed=2.4 + 0.35 * (k % 4), loop_amp=4.5 + (k % 3)))
    return out


S = []
# 0. HOOK (frame 0 shows it): the same wave links the two hero props; band chips; Ved to camera over the blurred kitchen
S.append({"say": "Your Wi-Fi and your microwave use the *same wave*.",
          "caption_y": 0.5,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.0, "zoom": 1.07, "focus": [0.5, 0.42]}]},
          "layers": [plate("kitchen_wide", blur=7, keys=[{"t": 0, "scale": 1.12}, {"t": 3.0, "scale": 1.18}]),
                     txt("SAME *WAVE*", 0.1, 132, enter="none", sting="slam"),
                     sprite("mw_hero", 0.27, 0.27, 0.42, keys=[{"t": 0, "x": 0.2}, {"t": 0.5, "x": 0.27}]),
                     sprite("router_hero", 0.76, 0.27, 0.3, keys=[{"t": 0, "x": 0.83}, {"t": 0.5, "x": 0.76}]),
                     {"type": "image", "svg": WAVE, "x": 0.5, "y": 0.205, "w": 0.34, "enter": "fade", "at": 0.15, "loop": "pulse", "loop_speed": 2.2},
                     {"type": "image", "svg": chip("MICROWAVE", "2.45 GHz", GOLD), "x": 0.27, "y": 0.38, "w": 0.34, "enter": "pop", "at": 0.5, "sfx": "click"},
                     {"type": "image", "svg": chip("WI-FI", "2.4 GHz", BLUE), "x": 0.74, "y": 0.38, "w": 0.34, "enter": "pop", "at": 0.8, "sfx": "click"},
                     dict(close_ved([["surprised", 0], ["point", 1.2], ["explain", 2.2]]), y=0.97, h=0.62, x=0.5)]})
# 1. router close-up on its shelf: Ved leans in from the side
S.append({"say": "So why doesn't your router *cook you*?",
          "transition": "whip", "caption_y": 0.44,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 2.8, "zoom": 1.12, "focus": [0.55, 0.38]}]},
          "layers": [plate("kitchen_router"),
                     {"type": "image", "svg": rings(), "x": 0.56, "y": 0.2, "w": 0.6, "enter": "fade", "at": 0.2, "loop": "pulse", "loop_speed": 1.4, "opacity": 0.85},
                     txt("COOK *YOU?*", 0.1, 104, enter="pop", at=0.45, sfx="pop"),
                     dict(close_ved([["think", 0], ["side_eye", 1.4]]), x=0.24, y=0.97, h=0.62)]})
# 2. the Balance look: 1,000 W vs 0.1 W over the dimmed microwave close-up; Ved points
S.append({"say": "Power. A microwave: *1,000 watts*. Your router: a *tenth* of one.",
          "transition": "slide_left", "caption_y": 0.6, "pad": 0.25,
          "camera": {"keys": [{"t": 0, "zoom": 1.04, "focus": [0.5, 0.5]}, {"t": 4.6, "zoom": 1.0, "focus": [0.5, 0.5]}]},
          "layers": [plate("kitchen_mw", blur=4),
                     {"type": "look", "look": "RS-03", "x": 0.5, "y": 0.3, "w": 0.96, "h": 0.5, "at": 0.15,
                      "props": {"title": "WHO HAS THE POWER?", "left": {"label": "MICROWAVE", "value": 1000, "unit": "W"},
                                "right": {"label": "ROUTER", "value": 0.1, "unit": "W"}, "verdict": "10,000x", "backdrop": "dim"}},
                     dict(close_ved([["explain", 0], ["point", 1.6], ["explain", 3.2]]), x=0.78, y=1.03, h=0.5)]})
# 3. 10,000x slam + eqbar over the wide kitchen; Wi-Fi rings fade with distance; Priya on her phone, Rao by the oven
S.append({"say": "*10,000 times* weaker, and spread across your house.",
          "transition": "cut", "caption_y": 0.44,
          "camera": {"keys": [{"t": 0, "zoom": 1.1, "focus": [0.62, 0.45]}, {"t": 3.8, "zoom": 1.0, "focus": [0.5, 0.5]}]},
          "layers": [plate("kitchen_wide"),
                     {"type": "motion", "comp": "NumberSlam", "x": 0.5, "y": 0.2, "w": 1.0, "h": 0.4, "at": 0.0,
                      "props": {"text": "10,000x", "label": "WEAKER", "color": "#ffffff", "accent": GOLD, "size": 400, "y": 0.36, "roll": 0.5}, "sting": "slam"},
                     {"type": "eqbar", "x": 0.5, "y": 0.37, "at": 0.8, "tone": "gold",
                      "keys": [[0.0, "1,000 W / 0.1 W"], [0.9, "1,000 W / 0.1 W = *10,000*"]]},
                     {"type": "image", "svg": rings(), "x": 0.72, "y": 0.42, "w": 0.75, "enter": "fade", "at": 1.6, "loop": "pulse",
                      "loop_speed": 1.2, "keys": [{"t": 0, "scale": 0.6, "opacity": 1.0}, {"t": 2.4, "scale": 1.5, "opacity": 0.25}]},
                     person("kitchen_wide", "rao", -0.95, 1.15, [["idle", 0], ["shrug", 2.2]]),
                     person("kitchen_wide", "priya", 1.15, 0.55, [["hold", 0]]),
                     ved("kitchen_wide", 0.1, 0.2, [["explain", 0], ["point", 1.4]], walk=[(0, -1.6, 0.2), (1.2, 0.1, 0.2)])]})
# 4. the Cutaway: inside the oven, built from wire; MAGNETRON, WAVEGUIDE, WATER; waves run and spread; the mug heats
S.append({"say": "Inside, the wave flips *billions of times a second*.",
          "transition": "flash", "caption_y": 0.17,
          "layers": [{"type": "video", "path": A + "cutaway_microwave.mp4", "x": 0.5, "y": 0.5, "w": 1.0, "h": 1.0, "at": 0.0, "sting": "reveal"}]})
# 5. inside the cavity (night plate): water molecules wiggle to keep up; the count ticks; heat
S.append({"say": "Water molecules wiggle to keep up. That wiggle is *heat*.",
          "transition": "cut", "caption_y": 0.6,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.4, "zoom": 1.1, "focus": [0.5, 0.55]}]},
          "layers": [plate("cavity")] + molecules() +
                    [hud("field flips per second", 0.19, steps=[[0.0, 0], [0.4, 2450000000]], at=0.1, tone="gold", width_of="2,450,000,000"),
                     {"type": "stamp", "text": "HEAT", "tone": "red", "angle": -7, "size": 130, "x": 0.5, "y": 0.5, "at": 1.9, "sfx": "thud"},
                     dict(close_ved([["explain", 0], ["surprised", 2.6]]), x=0.82, y=0.97, h=0.52, rim=True)]})
# 6. the myth: two option cards and a MYTH stamp over the blurred microwave; Ved smirks
S.append({"say": "And no, it's not water's 'magic frequency'. *Myth*.",
          "transition": "cut", "caption_y": 0.6,
          "layers": [plate("kitchen_mw", blur=10, keys=[{"t": 0, "scale": 1.15}, {"t": 3.0, "scale": 1.22}]),
                     {"type": "optcard", "label": "the old story", "text": "WATER'S\nMAGIC FREQUENCY", "tone": "red", "x": 0.5, "y": 0.15,
                      "w": 0.6, "rotate": -3, "enter": "pop", "at": 0.1, "sfx": "pop"},
                     {"type": "optcard", "label": "what's true", "text": "REACHES DEEP\nINTO FOOD", "tone": "green", "x": 0.5, "y": 0.37,
                      "w": 0.6, "rotate": 2, "enter": "pop", "at": 1.3, "sfx": "pop", "verdict": "tick", "verdict_at": 0.4},
                     {"type": "stamp", "text": "MYTH", "tone": "red", "angle": -8, "size": 120, "x": 0.62, "y": 0.265, "at": 1.0, "sfx": "stamp", "sting": "turn"},
                     dict(close_ved([["serious", 0], ["smirk", 1.8]]), y=0.97, h=0.58, x=0.5)]})
# 7. the Whiteboard look: why the wave stays in (holes ~1 mm, wave ~12 cm); Ved drawn in marker beside it
S.append({"say": "The door's holes are tiny. The wave is *12 cm*. It can't get out.",
          "transition": "paper", "caption_y": 0.2, "pad": 0.2, "bg": {"type": "solid", "colors": ["#fbfaf5"], "pattern": "none"},
          "layers": [{"type": "look", "look": "RS-13", "x": 0.5, "y": 0.5, "w": 1.0, "h": 1.0, "at": 0.0,
                      "props": {"title": "WHY IT STAYS IN", "steps": ["WAVE: 12 CM", "DOOR HOLES: ~1 MM", "TOO BIG TO FIT"], "key": 2}},
                     dict(close_ved([["explain", 0], ["point", 1.6]]), x=0.84, y=0.98, h=0.44, style="marker")]})
# 8. the leak: Priya's phone buffers while Rao runs the oven; Ved side-eyes
S.append({"say": "Well... *mostly*.",
          "transition": "cut", "caption_y": 0.44, "pad": 0.2,
          "layers": [plate("kitchen_wide"),
                     person("kitchen_wide", "rao", -0.95, 1.15, [["explain", 0]]),
                     person("kitchen_wide", "priya", 1.15, 0.55, [["sad", 0]]),
                     {"type": "image", "svg": PHONE, "x": 0.5, "y": 0.2, "w": 0.3, "enter": "pop", "at": 0.05, "sfx": "error"},
                     {"type": "image", "svg": SPINNER, "x": 0.5, "y": 0.243, "w": 0.1, "enter": "fade", "at": 0.1, "loop": "spin", "loop_speed": 4},
                     dict(close_ved([["side_eye", 0]]), x=0.18, y=0.97, h=0.52)]})
# 9. comic beat: silent reaction cut-away
S.append({"dur": 1.35, "transition": "cut", "captions": False,
          "layers": [plate("kitchen_wide", blur=10, keys=[{"t": 0, "scale": 1.35}]), dict(close_ved([["deadpan", 0]]), acting="none")],
          "beat": {"kind": "deadpan", "at": 0.1, "dur": 1.2, "who": "ved", "text": "my Wi-Fi when someone heats *noodles*", "text_y": 0.2}})
# 10. payoff: kinetic title + the microwave; the ding loops back to the hook
S.append({"say": "Same wave. *10,000 times* the power, locked in a box.",
          "transition": "zoom", "caption_y": 0.52, "sfx": "ding",
          "camera": {"keys": [{"t": 0, "zoom": 1.1, "focus": [0.5, 0.5]}, {"t": 3.6, "zoom": 1.0, "focus": [0.5, 0.5]}]},
          "layers": [plate("kitchen_wide", blur=6, keys=[{"t": 0, "scale": 1.1}, {"t": 3.6, "scale": 1.16}]),
                     {"type": "motion", "comp": "KineticTitle", "x": 0.5, "y": 0.16, "w": 1.0, "h": 0.28, "at": 0.05,
                      "props": {"lines": ["SAME WAVE.", "10,000x POWER"], "accent": "10,000x", "style": "slam", "size": 118}},
                     sprite("mw_hero", 0.27, 0.36, 0.36, enter="pop", at=1.4, sfx="pop"),
                     sprite("router_hero", 0.78, 0.37, 0.2, enter="pop", at=1.6),
                     dict(close_ved([["warm", 0], ["smirk", 2.4]]), y=0.97, h=0.62, x=0.5)]})

job = {"id": ID, "title": "Your Wi-Fi and your microwave use the SAME wave 📶",
       "description": "Wi-Fi and microwave ovens both use the 2.4 GHz band. So why doesn't your router cook you? Power: an oven "
                      "pumps roughly 700-1,100 watts into a sealed metal box, while a Wi-Fi router is capped at about 0.1 watt "
                      "(100 mW), spread through your house, about 10,000 times weaker. Inside the oven the field flips direction "
                      "billions of times a second; water molecules are polar and keep trying to flip with it, and that jostling "
                      "turns into heat. 2.45 GHz is not water's 'resonant frequency' (a popular myth): water absorbs most around "
                      "10-20 GHz, and 2.45 GHz was chosen because it reaches deeper into food (and sits in a licence-free band). "
                      "The wave is ~12 cm long, the holes in the door's metal screen ~1 mm, so it can't get out... mostly: a "
                      "tiny leak can still disturb 2.4 GHz Wi-Fi nearby.\n\n"
                      "Sources: Make Tech Easier (2.4 GHz and water); Illinois Physics Van (door screen); SlashGear (Wi-Fi "
                      "interference); Physics Forums summary (oven vs router power).",
       "tags": ["wifi", "microwave", "microwave oven", "how microwaves work", "2.4 ghz", "wifi router", "physics",
                "science explained", "explained", "myth"],
       "hashtags": ["#physics", "#wifi"],
       "instagram": {"hashtags": ["#science", "#wifi", "#microwave", "#physicsfacts", "#explained"]},
       "meta": {"format": "big-question", "topic": "why Wi-Fi doesn't cook you though microwave ovens use the same 2.4 GHz band: "
                                                   "~1,000 W in a sealed box vs ~0.1 W spread out (~10,000x); polar water molecules "
                                                   "jostle as the field flips (heat); the 'water resonance' myth; 12 cm wave vs ~1 mm "
                                                   "door holes; a small leak can still disrupt Wi-Fi",
                "hook": "question",
                "idea_source": "viral-shaped + unique: an everyday 'does my Wi-Fi cook me?' worry made picturable with one "
                               "comparison (same wave, 10,000x power); backlog idea 'Your microwave and your Wi-Fi use the same "
                               "wave'; owner's showcase brief (every toolkit in one Short)",
                "characters": ["ved", "extra"],
                "overrides": "one-off showcase (owner 2026-11-21: 'use 100% of everything'): Reelsmith Balance + Whiteboard looks, "
                             "Ved drawn in marker on the whiteboard, Cutaway cutaway clip, NumberSlam + KineticTitle motion clips, "
                             "night cavity plate inside a town video",
                "sources": ["https://maketecheasier.com/?p=861805",
                            "https://van.physics.illinois.edu/ask/listing/12217",
                            "https://www.slashgear.com/1893423/microwave-wifi-interference-explained",
                            "https://www.physicsforums.com/threads/wireless-routers-vs-microwave-ovens.990804/page-2",
                            "https://gizmodo.com/why-does-your-microwave-oven-mess-with-the-wi-fi-connec-1666117933"],
                "humour": {"trend": "the 'my X when Y' reaction format (timeless; this week's rising 'nervous reaction' memes are "
                                    "tied to a film character we can't draw), bent to the topic: Wi-Fi dropping while noodles heat",
                           "beat": "deadpan", "scene": 9},
                "claims": [
                    {"claim": "Wi-Fi (2.4 GHz band) and microwave ovens (2.45 GHz) use the same band", "tag": "PROVEN",
                     "source": "https://maketecheasier.com/?p=861805"},
                    {"claim": "ovens ~700-1,100 W vs routers capped ~100 mW EIRP: about 10,000x", "tag": "PROVEN",
                     "source": "https://maketecheasier.com/?p=861805"},
                    {"claim": "polar water molecules keep trying to flip with the field; the lag becomes heat", "tag": "PROVEN",
                     "source": "https://maketecheasier.com/?p=861805"},
                    {"claim": "2.45 GHz is not water's resonant frequency; water's loss peaks ~10-20 GHz; 2.45 GHz penetrates deeper", "tag": "PROVEN",
                     "source": "https://maketecheasier.com/?p=861805"},
                    {"claim": "wavelength ~12.2 cm; door screen holes ~mm, so the waves can't get through", "tag": "PROVEN",
                     "source": "https://van.physics.illinois.edu/ask/listing/12217"},
                    {"claim": "running ovens can disrupt 2.4 GHz Wi-Fi nearby", "tag": "PROVEN",
                     "source": "https://www.slashgear.com/1893423/microwave-wifi-interference-explained"}]},
       "thumbnail": {"title": "SAME *WAVE?*", "title_y": 0.2, "title_size": 160, "max_w": 0.95, "blur": 14,
                     "glow": "#ffd23a", "glow_x": 0.5, "glow_y": 0.5, "glow_strength": 1.3, "bg_saturation": 1.25,
                     "tint": ["#2f8fe0", "#f08a24"], "tint_amount": 0.22,
                     "bg": [plate("kitchen_wide")],
                     "fg": [sprite("mw_hero", 0.22, 0.45, 0.4), sprite("router_hero", 0.8, 0.46, 0.26),
                            {"type": "character", "id": "ved", "pose": "surprised", "x": 0.5, "y": 0.95, "h": 0.95, "enter": "none",
                             "acting": "none", "talk": False, "ground": False, "allow_outside_safe": True}]},
       "privacy": "public", "speaker": "ved", "voice": {"voice": "bm_lewis", "speed": 1.1, "lang": "en-us"}, "assets_script": J + "assets.py", "scenes": S}
json.dump(job, open(J + "job.json", "w"), indent=1, ensure_ascii=False)
print("scenes", len(S))
