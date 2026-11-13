"""2026-11-13-b: "What if you could SEE Wi-Fi?" (what-if).
2D Ved + one housemate staged in depth in a Blender living room (2 angles + a "radio eyes" version where the router glows and
the walls go see-through), then a green karst valley holding a kilometre-wide eyeball, and the same valley with a FAST-style
dish. Spectrum, bee-vision and wavelength panels, honesty tags and counters are 2D; the router and eyeball are cut-outs.
Run after the assets exist: python jobs/2026-11-13-b/build_job.py
"""
import json, os, sys
sys.path.insert(0, os.getcwd())
from autopilot.stage import Stage

ID = "2026-11-13-b"
J = f"jobs/{ID}/"
A = J + "assets/"
ST = {n: Stage(A + f"plate_{n}.json") for n in ("room_wide", "room_mid", "room_wifi")}

OUT = {   # recurring people: same outfit in every shot
    "mia": {"skin": "#a8693f", "top": ["#d9534f", "jacket"], "bottom": ["#34425c", "trousers"], "hair": ["#1a1410", "bun"],
            "shoes": "#25262b"},                                        # the housemate
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


def label(t, color, w=620, size=62):
    return card(f"<text x='{w/2}' y='92' text-anchor='middle' font-size='{size}' fill='{color}' {AN}>{t}</text>", w, 140)


TAGC = {"PROVEN": "#46965a", "SPECULATION": "#d9534f"}


def tag(word, at=0.0):
    """Small honesty pill, top-left."""
    w = 150 + 40 * len(word)
    c = TAGC[word]
    svg = (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {w} 110'><rect x='5' y='5' width='{w-10}' height='100' rx='50' "
           f"fill='{c}' stroke='#1a1410' stroke-width='6'/><circle cx='55' cy='55' r='16' fill='#f6efe2'/>"
           f"<text x='{(w+60)/2}' y='77' text-anchor='middle' font-size='60' fill='#f6efe2' {AN}>{word}</text></svg>")
    return {"type": "image", "svg": svg, "x": 0.06 + w / 110 * 0.085 / 2, "y": 0.115, "w": w / 110 * 0.085,
            "enter": "pop", "at": at, "sfx": "click"}


# the spectrum: long waves on the left, the rainbow slice we see, short waves on the right
RAIN = ["#7a3fb8", "#2f6fd6", "#3fb0d9", "#46965a", "#f2d03a", "#f2b04a", "#d9534f"]
SPECTRUM = card(
    "<text x='450' y='66' text-anchor='middle' font-size='42' fill='#1a1410' " + F + ">THE LIGHT SPECTRUM</text>"
    "<rect x='40' y='110' width='820' height='70' rx='14' fill='#34425c'/>"
    + "".join(f"<rect x='{430 + k*7}' y='104' width='7' height='82' fill='{c}'/>" for k, c in enumerate(reversed(RAIN)))
    + "<text x='60' y='158' font-size='30' fill='#f6efe2' " + F + ">RADIO</text>"
    "<text x='215' y='158' font-size='30' fill='#f6efe2' " + F + ">MICRO</text>"
    "<text x='345' y='158' font-size='30' fill='#f6efe2' " + F + ">IR</text>"
    "<text x='520' y='158' font-size='30' fill='#f6efe2' " + F + ">UV</text>"
    "<text x='640' y='158' font-size='30' fill='#f6efe2' " + F + ">X-RAY</text>"
    "<polygon points='455,200 435,232 475,232' fill='#d9534f'/>"
    "<text x='640' y='270' text-anchor='middle' font-size='44' fill='#d9534f' " + AN + ">YOU SEE ONLY THIS</text>"
    "<text x='200' y='270' text-anchor='middle' font-size='34' fill='#2f6fd6' " + F + ">WI-FI IS HERE</text>"
    "<polygon points='240,200 220,226 260,226' fill='#2f6fd6'/>", 900, 310)


def flower(cx, cy, petal, center, uv=False):
    s = "".join(f"<ellipse cx='{cx}' cy='{cy-62}' rx='32' ry='60' fill='{petal}' stroke='#1a1410' stroke-width='4' "
                f"transform='rotate({a} {cx} {cy})'/>" for a in range(0, 360, 45))
    if uv:   # the bullseye bees see: dark centre band
        s += f"<circle cx='{cx}' cy='{cy}' r='70' fill='#4a2a7a' opacity='0.85'/>"
    return s + f"<circle cx='{cx}' cy='{cy}' r='30' fill='{center}' stroke='#1a1410' stroke-width='4'/>"


BEE = card(
    "<text x='225' y='70' text-anchor='middle' font-size='44' fill='#1a1410' " + AN + ">YOU SEE</text>"
    "<text x='675' y='70' text-anchor='middle' font-size='44' fill='#7a3fb8' " + AN + ">A BEE SEES</text>"
    + flower(225, 230, "#f2d03a", "#c97a1a") + flower(675, 230, "#b9a6e6", "#2b1a4a", uv=True)
    + "<line x1='450' y1='100' x2='450' y2='380' stroke='#1a1410' stroke-width='4' stroke-dasharray='12 10'/>"
    "<text x='675' y='420' text-anchor='middle' font-size='32' fill='#1a1410' " + F + ">UV LANDING STRIP</text>", 900, 450)

# a Wi-Fi wave with its length marked
WAVE = card(
    "<path d='M60,110 C110,40 170,40 220,110 S330,180 380,110 S490,40 540,110 S650,180 700,110 S810,40 840,110' "
    "fill='none' stroke='#2f6fd6' stroke-width='12'/>"
    "<line x1='220' y1='215' x2='540' y2='215' stroke='#d9534f' stroke-width='8'/>"
    "<line x1='220' y1='195' x2='220' y2='235' stroke='#d9534f' stroke-width='8'/>"
    "<line x1='540' y1='195' x2='540' y2='235' stroke='#d9534f' stroke-width='8'/>"
    "<text x='380' y='300' text-anchor='middle' font-size='54' fill='#d9534f' " + AN + ">ONE WAVE: 12 CM</text>"
    "<text x='790' y='300' text-anchor='middle' font-size='28' fill='#34425c' " + F + ">2.4 GHZ</text>", 900, 330)

# the eye-size rule: wider wave -> wider eye
RULE = card(
    "<text x='450' y='66' text-anchor='middle' font-size='42' fill='#1a1410' " + F + ">SHARP VISION NEEDS</text>"
    "<text x='450' y='130' text-anchor='middle' font-size='50' fill='#1a1410' " + AN + ">EYES WAY WIDER THAN THE WAVE</text>"
    "<circle cx='170' cy='225' r='22' fill='#2f6fd6' stroke='#1a1410' stroke-width='4'/><circle cx='170' cy='225' r='9' fill='#0b0d10'/>"
    "<text x='170' y='290' text-anchor='middle' font-size='30' fill='#34425c' " + F + ">LIGHT: 5 MM</text>"
    "<line x1='230' y1='225' x2='470' y2='225' stroke='#d9534f' stroke-width='10'/><polygon points='510,225 465,200 465,250' fill='#d9534f'/>"
    "<text x='680' y='245' text-anchor='middle' font-size='58' fill='#d9534f' " + AN + ">WI-FI: 1 KM</text>", 900, 320)

S = []
# 0. hook (room mid): the question at frame 0, Ved points at the router on the console
S.append({"say": "What if you could *see* Wi-Fi? It's light too.",
          "caption_y": 0.31,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.0, "zoom": 1.06, "focus": [0.45, 0.52]}]},
          "layers": staged("room_mid",
                           people=[ved("room_mid", -0.7, 1.3, [["crossed", 0], ["point", 1.6], ["explain", 3.0]])],
                           extra_top=[txt("WHAT IF YOU COULD *SEE* WI-FI?", 0.16, 112, enter="none")])})
# 1. room wide: the spectrum card, the rainbow is a sliver
S.append({"say": "Your eyes catch just *400 to 700 nanometres*.",
          "transition": "slide_left", "caption_y": 0.4,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.5, "zoom": 1.05, "focus": [0.5, 0.52]}]},
          "layers": staged("room_wide",
                           people=[ved("room_wide", 0.3, -1.6, [["explain", 0], ["point", 1.4], ["think", 3.2]],
                                       walk=[(0, -1.8, -1.9), (1.1, 0.3, -1.6)]),
                                   person("room_wide", "mia", 1.2, 1.4, [["idle", 0], ["wave", 1.0], ["idle", 2.6]])],
                           extra_top=[tag("PROVEN", 0.1),
                                      {"type": "image", "svg": SPECTRUM, "x": 0.5, "y": 0.24, "w": 0.84, "enter": "slide_up", "at": 0.3, "sfx": "pop"}])})
# 2. bee vision: two flowers, the bee one has a landing strip
S.append({"say": "Bees see ultraviolet: flowers hide *landing strips* there.",
          "transition": "zoom", "caption_y": 0.58,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.5, "zoom": 1.04, "focus": [0.5, 0.5]}]},
          "layers": [plate("room_mid", blur=10, keys=[{"t": 0, "scale": 1.25}]), tag("PROVEN", 0.1),
                     {"type": "image", "svg": BEE, "x": 0.5, "y": 0.33, "w": 0.86, "enter": "pop", "at": 0.2, "sfx": "pop"},
                     txt("*ULTRAVIOLET*", 0.7, 110, enter="pop", at=2.4, sfx="pop")]})
# 3. wavelength: the router flies in, the wave card measures 12 cm
S.append({"say": "Wi-Fi waves? About *12 centimetres* long.",
          "transition": "slide_left", "caption_y": 0.6,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.0, "zoom": 1.06, "focus": [0.5, 0.48]}]},
          "layers": [plate("room_mid", blur=8, keys=[{"t": 0, "scale": 1.3}]), tag("PROVEN", 0.0),
                     sprite("router", 0.5, 0.5, 0.52, enter="zoom", sfx="whoosh", keys=[{"t": 0, "rot": -6}, {"t": 2.5, "rot": 3}]),
                     {"type": "image", "svg": WAVE, "x": 0.5, "y": 0.27, "w": 0.84, "enter": "slide_down", "at": 0.6, "sfx": "pop"},
                     {"type": "counter", "from": 0, "to": 12, "decimals": 0, "suffix": " CM", "x": 0.5, "y": 0.72,
                      "size": 140, "color": "accent", "at": 0.9, "count_dur": 0.9, "enter": "pop", "sfx": "ding"}]})
# 4. radio eyes on: the router glows, walls go see-through; Mia jumps
S.append({"say": "From here, we're guessing: routers glow like lamps, walls go see-through.",
          "transition": "flash", "caption_y": 0.71,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 5.0, "zoom": 1.08, "focus": [0.44, 0.5]}]},
          "layers": staged("room_wifi",
                           people=[ved("room_wifi", 0.2, -1.7, [["surprised", 0], ["point", 1.6], ["explain", 3.4]]),
                                   person("room_wifi", "mia", 1.2, 1.4, [["surprised", 0], ["point", 2.4], ["cheer", 3.6]],
                                          hops=[[0.2, 0.05, 0.4], [3.7, 0.04, 0.35]])],
                           extra_top=[tag("SPECULATION", 0.1),
                                      txt("ROUTER = *LAMP*", 0.2, 120, enter="pop", at=1.6, sfx="pop"),
                                      {"type": "image", "svg": label("WALLS: SEE-THROUGH", "#2f6fd6", 760, 64), "x": 0.5, "y": 0.29,
                                       "w": 0.66, "enter": "pop", "at": 3.4, "sfx": "pop", "rotate": -2}])})
# 5. comic beat: smirk cut-away
S.append({"dur": 1.6, "transition": "cut", "captions": False,
          "layers": [plate("room_wifi", blur=10, keys=[{"t": 0, "scale": 1.35}]), dict(close_ved([["smirk", 0]]), acting="none")],
          "beat": {"kind": "smirk", "at": 0.1, "dur": 1.4, "who": "ved",
                   "text": "me, finally seeing\nthe *full-bars spot*", "text_y": 0.2}})
# 6. valley: a kilometre-wide eyeball sits between the hills
S.append({"say": "The catch: sharp eyes must be way wider than the wave. For Wi-Fi: *a kilometre*.",
          "transition": "zoom", "caption_y": 0.62,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 6.0, "zoom": 1.1, "focus": [0.52, 0.5]}]},
          "layers": [plate("valley_eye"), tag("PROVEN", 0.1),
                     {"type": "image", "svg": RULE, "x": 0.5, "y": 0.26, "w": 0.86, "enter": "slide_down", "at": 0.3, "sfx": "pop"},
                     {"type": "counter", "from": 0, "to": 1, "decimals": 0, "suffix": " KM EYE", "x": 0.5, "y": 0.74,
                      "size": 130, "color": "accent", "at": 3.0, "count_dur": 0.6, "enter": "zoom", "sfx": "boom"}]})
# 7. valley: the real thing that does this job, the 500 m dish
S.append({"say": "That's why China's FAST radio dish is *500 metres* wide.",
          "transition": "slide_left", "caption_y": 0.62,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.0, "zoom": 1.08, "focus": [0.5, 0.5]}]},
          "layers": [plate("valley_dish"), tag("PROVEN", 0.0),
                     txt("FAST *500 M*", 0.21, 140, enter="pop", at=0.3, sfx="pop"),
                     {"type": "image", "svg": label("A GIANT EAR FOR RADIO", "#2f6fd6", 760, 60), "x": 0.5, "y": 0.75,
                      "w": 0.7, "enter": "pop", "at": 1.6, "sfx": "pop", "rotate": 2}]})
# 8. close payoff: loops back to the question
S.append({"say": "So yes, you *could* see Wi-Fi. With eyes the size of a town.", "transition": "cut",
          "caption_y": 0.64,
          "layers": [plate("room_wifi", blur=10, keys=[{"t": 0, "scale": 1.35}, {"t": 4.0, "scale": 1.42}]),
                     close_ved([["explain", 0], ["think", 1.6], ["smirk", 3.0]]),
                     sprite("eye", 0.8, 0.2, 0.22, at=2.0, enter="pop", sfx="pop", loop="float", loop_amp=0.01),
                     txt("EYES *1 KM* WIDE", 0.16, 110, enter="pop", at=2.0, sfx="ding", max_w=0.6, x=0.4)]})

THUMB = {"title": "SEE *WI-FI?*", "title_y": 0.15, "title_size": 170, "max_w": 0.95, "blur": 14,
         "glow": "#6fe0ff", "glow_x": 0.5, "glow_y": 0.5, "glow_strength": 1.4, "bg_saturation": 1.5,
         "tint": ["#1f4fb8", "#f08a24"], "tint_amount": 0.38,
         "bg": [plate("room_wifi")],
         "fg": [sprite("router", 0.2, 0.55, 0.32, rot=-10), sprite("eye", 0.82, 0.55, 0.3, rot=8),
                {"type": "character", "id": "ved", "pose": "surprised", "x": 0.5, "y": 0.93, "h": 0.95, "enter": "none",
                 "acting": "none", "talk": False, "ground": False, "allow_outside_safe": True}]}

job = {"id": ID, "title": "What if you could SEE Wi-Fi? 📶",
       "description": "Wi-Fi is light too, with waves about 12 cm long instead of 400-700 nanometres. To see it as sharply as you "
                      "see now, your eyes would need to be about a kilometre wide, which is why radio telescopes like FAST are huge.\n\n"
                      "Sources: Wikipedia (2.4 GHz radio use, visible spectrum, FAST); NCBI/PMC on bees, flowers and UV; "
                      "OpenStax Astronomy on why radio telescopes must be so large.",
       "tags": ["wifi", "electromagnetic spectrum", "visible light", "what if", "radio telescope", "FAST telescope",
                "bee vision", "physics explained", "science"],
       "hashtags": ["#physics", "#science"],
       "meta": {"format": "what-if", "topic": "what if you could see Wi-Fi: visible light vs 12 cm Wi-Fi waves, why your eyes would need to be ~1 km wide (diffraction), FAST dish",
                "hook": "what-if",
                "idea_source": "unique + viral-shaped: everyday object (Wi-Fi) made into a physics what-if; owner's 'what is a spectrum' example",
                "characters": ["ved", "extra"],
                "sources": ["https://en.wikipedia.org/wiki/2.4_GHz_radio_use",
                            "https://en.wikipedia.org/wiki/Visible_spectrum",
                            "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12477309/",
                            "https://openstax.org/books/astronomy/pages/6-4-radio-telescopes",
                            "https://en.wikipedia.org/wiki/Five-hundred-meter_Aperture_Spherical_Telescope",
                            "https://en.wikipedia.org/wiki/Angular_resolution"],
                "humour": {"trend": "timeless (no current trend fit cleanly): the hunt for the one full-bars Wi-Fi spot, smirk + caption card",
                           "beat": "smirk", "scene": 5},
                "claims": [
                    {"claim": "Wi-Fi/radio waves are electromagnetic radiation, the same family as visible light", "tag": "PROVEN",
                     "source": "https://en.wikipedia.org/wiki/Visible_spectrum"},
                    {"claim": "human eyes detect roughly 400-700 nm (often quoted 380-750 nm)", "tag": "PROVEN",
                     "source": "https://en.wikipedia.org/wiki/Visible_spectrum"},
                    {"claim": "bees see ultraviolet; many flowers have UV nectar guides", "tag": "PROVEN",
                     "source": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12477309/"},
                    {"claim": "2.4 GHz Wi-Fi has a wavelength of ~12.5 cm", "tag": "PROVEN", "source": "https://en.wikipedia.org/wiki/2.4_GHz_radio_use"},
                    {"claim": "router glowing / walls see-through if eyes caught 12 cm waves", "tag": "SPECULATION", "source": "our what-if"},
                    {"claim": "diffraction limit: same sharpness at 12.5 cm as a 5 mm pupil at 550 nm needs an aperture of ~1.1 km (theta ~ 1.22 lambda/D)",
                     "tag": "PROVEN", "source": "https://en.wikipedia.org/wiki/Angular_resolution"},
                    {"claim": "FAST, China's radio telescope, has a 500 m dish; radio telescopes are large because of long wavelengths",
                     "tag": "PROVEN", "source": "https://openstax.org/books/astronomy/pages/6-4-radio-telescopes"}]},
       "privacy": "public", "speaker": "ved", "assets_script": J + "assets.py", "thumbnail": THUMB, "scenes": S}
json.dump(job, open(J + "job.json", "w"), indent=1, ensure_ascii=False)
print("scenes", len(S))
