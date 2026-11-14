"""2026-11-15-c: "Mars and Jupiter aren't touching" (myth-bust).
2D Ved + two stargazers staged in depth on a Blender ridge before sunrise (wide, mid, a long-lens look at the planet pair),
then deep space with Earth, Mars and Jupiter on one line of sight (from behind Earth: overlapping; from the side: the real
gap). Distance counters, the pinky card, the light-time panel and labels are 2D.
Run after the assets exist: python jobs/2026-11-15-c/build_job.py
"""
import json, math, os, sys
sys.path.insert(0, os.getcwd())
from autopilot.stage import Stage

ID = "2026-11-15-c"
J = f"jobs/{ID}/"
A = J + "assets/"
ST = {n: Stage(A + f"plate_{n}.json") for n in ("ridge_wide", "ridge_mid", "ridge_sky", "space_eye", "space_side")}

# planet positions (same maths as assets.py)
PAIR_AZ, PAIR_EL, RS = 14.0, 21.0, 240.0


def sky_point(az, el, R=RS):
    a, e = math.radians(az), math.radians(el)
    return (R * math.sin(a) * math.cos(e), R * math.cos(a) * math.cos(e), R * math.sin(e))


D = (0.0, 0.4472, 0.8944)


def along(t):
    return (D[0] * t, D[1] * t, D[2] * t)


def scr(set_, p):
    x, y = ST[set_].point(*p)
    return round(x, 3), round(y, 3)


JUP = {s: scr(s, sky_point(PAIR_AZ, PAIR_EL)) for s in ("ridge_wide", "ridge_mid", "ridge_sky")}
MARS = {s: scr(s, sky_point(PAIR_AZ - 1.6, PAIR_EL + 1.5)) for s in ("ridge_wide", "ridge_mid", "ridge_sky")}
SE = {"earth": scr("space_side", along(0)), "mars": scr("space_side", along(22)), "jup": scr("space_side", along(89))}
EE = {"mars": scr("space_eye", along(22)), "jup": scr("space_eye", along(89))}

OUT = {   # recurring stargazers: same outfit in every shot
    "nisha": {"skin": "#b97a52", "build": "slim", "hair": ["#1a1410", "bun"], "top": ["#d9534f", "jacket"],
              "bottom": ["#34425c", "trousers"], "shoes": "#25262b", "bag": "#8a5a3c"},
    "theo": {"skin": "#e0b08a", "build": "round", "hair": ["#6b4529", "short"], "hat": ["cap", "#34425c"],
             "top": ["#6fc3c0", "jacket"], "bottom": ["#3a3e48", "trousers"], "shoes": "#25262b"},
}
F = "font-family='Poppins, DejaVu Sans, sans-serif' font-weight='800'"
AN = "font-family='Anton, DejaVu Sans, sans-serif'"


def plate(name, blur=0, **k):
    return {"type": "image", "path": A + f"plate_{name}.png", "x": 0.5, "y": 0.5, "w": 1.0, "enter": "none", "blur": blur, **k}


def sprite(name, x, y, w, **k):
    return {"type": "image", "path": A + name + ".png", "x": x, "y": y, "w": w, "enter": k.pop("enter", "none"), **k}


def txt(t, y, size=96, **k):
    return {"type": "text", "text": t, "font": "display", "x": k.pop("x", 0.5), "y": y, "size": size, "max_w": k.pop("max_w", 0.88),
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


def ring(color="#f2b04a"):
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 200'><circle cx='100' cy='100' r='84' fill='none' "
            f"stroke='{color}' stroke-width='9' stroke-dasharray='18 12'/></svg>")


def label(word, color="#f2b04a", w=420):
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {w} 96'><rect x='4' y='4' width='{w-8}' height='88' rx='20' "
            f"fill='#1a1410' fill-opacity='0.82' stroke='{color}' stroke-width='5'/><text x='{w/2}' y='68' text-anchor='middle' "
            f"font-size='56' fill='{color}' {AN}>{word}</text></svg>")


def tag(word, x, y, w=0.3, color="#f2b04a", at=0.0, **k):
    return {"type": "image", "svg": label(word, color), "x": x, "y": y, "w": w, "enter": "pop", "at": at, "sfx": "pop", **k}


def dashed(x0, y0, x1, y1, color="#f6efe2", at=0.0):
    W, H = 1080, 1920
    return {"type": "image", "x": 0.5, "y": 0.5, "w": 1.0, "enter": "fade", "at": at,
            "svg": (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {W} {H}'><line x1='{x0*W:.0f}' y1='{y0*H:.0f}' "
                    f"x2='{x1*W:.0f}' y2='{y1*H:.0f}' stroke='{color}' stroke-width='7' stroke-dasharray='22 16' opacity='0.85'/></svg>")}


# the pinky rule: 1.2 degrees = about one finger at arm's length
PINKY = card(
    "<rect x='60' y='40' width='54' height='150' rx='27' fill='#e0b08a' stroke='#1a1410' stroke-width='5'/>"
    "<rect x='30' y='150' width='120' height='80' rx='30' fill='#e0b08a' stroke='#1a1410' stroke-width='5'/>"
    "<text x='190' y='112' font-size='84' fill='#1a1410' " + AN + ">1.2 DEGREES</text>"
    "<text x='190' y='190' font-size='44' fill='#34425c' " + F + ">= ONE FINGER AT ARM'S LENGTH</text>", 900, 250)

# light time: what you see is old news
LIGHT = card(
    "<text x='450' y='78' text-anchor='middle' font-size='54' fill='#1a1410' " + AN + ">THE LIGHT YOU SEE LEFT...</text>"
    "<circle cx='200' cy='200' r='70' fill='#e07a4a' stroke='#1a1410' stroke-width='6'/>"
    "<text x='200' y='318' text-anchor='middle' font-size='40' fill='#34425c' " + F + ">MARS</text>"
    "<text x='200' y='378' text-anchor='middle' font-size='62' fill='#d9534f' " + AN + ">11 MIN AGO</text>"
    "<circle cx='680' cy='185' r='84' fill='#f4e6cc' stroke='#1a1410' stroke-width='6'/>"
    "<rect x='600' y='164' width='160' height='16' fill='#b9825a'/><rect x='608' y='206' width='144' height='13' fill='#b9825a'/>"
    "<text x='680' y='318' text-anchor='middle' font-size='40' fill='#34425c' " + F + ">JUPITER</text>"
    "<text x='680' y='378' text-anchor='middle' font-size='62' fill='#d9534f' " + AN + ">44 MIN AGO</text>", 900, 410)

jx, jy = JUP["ridge_mid"]; mx, my = MARS["ridge_mid"]
S = []
# 0. hook (ridge mid): the myth at frame 0, the planet pair ringed over Ved
S.append({"say": "Mars and Jupiter are touching this weekend. They're *600 million* kilometres apart.",
          "caption_y": 0.47,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.6, "zoom": 1.06, "focus": [0.52, 0.48]}]},
          "layers": staged("ridge_mid",
                           people=[ved("ridge_mid", -0.5, -1.1, [["crossed", 0], ["point", 1.4], ["smirk", 3.4]])],
                           fg=True,
                           extra_top=[{"type": "image", "svg": ring(), "x": (jx + mx) / 2, "y": (jy + my) / 2, "w": 0.2, "enter": "none",
                                       "loop": "pulse", "loop_amp": 0.05},
                                      {"type": "image", "svg": stamp("MYTH", w=420), "x": 0.28, "y": 0.12, "w": 0.32, "rotate": -5,
                                       "enter": "none"},
                                      txt("THEY'RE *TOUCHING*", 0.305, 104, enter="none"),
                                      {"type": "counter", "from": 0, "to": 600, "decimals": 0, "suffix": " MILLION KM APART",
                                       "x": 0.5, "y": 0.365, "size": 62, "color": "accent", "at": 2.2, "count_dur": 1.0,
                                       "enter": "pop", "sfx": "boom"}])})
# 1. sky: the pair, labelled; the finger rule
jx, jy = JUP["ridge_sky"]; mx, my = MARS["ridge_sky"]
S.append({"say": "Before sunrise, look up: Jupiter and Mars, one *finger* apart.",
          "transition": "slide_up", "caption_y": 0.62,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.45]}, {"t": 4.0, "zoom": 1.12, "focus": [jx, jy]}]},
          "layers": [plate("ridge_sky"),
                     tag("JUPITER", jx + 0.2, jy + 0.035, 0.3, "#f6efe2", at=0.9),
                     tag("MARS", mx - 0.17, my - 0.035, 0.24, "#e07a4a", at=1.6),
                     {"type": "image", "svg": PINKY, "x": 0.5, "y": 0.2, "w": 0.82, "enter": "slide_down", "at": 2.4, "sfx": "whoosh"}]})
# 2. ridge wide: the stargazers point and cheer; Ved walks in, sceptical
S.append({"say": "But that's only from *here*.",
          "transition": "slide_left", "caption_y": 0.5,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.0, "zoom": 1.05, "focus": [0.55, 0.48]}]},
          "layers": staged("ridge_wide",
                           people=[person("ridge_wide", "nisha", -1.0, -0.4, [["point", 0], ["happy", 1.2]], hops=[[1.3, 0.04, 0.4]]),
                                   person("ridge_wide", "theo", 0.1, -1.3, [["cheer", 0], ["point", 1.4]]),
                                   ved("ridge_wide", 1.3, -2.6, [["explain", 0], ["point", 1.6]],
                                       walk=[(0, 3.4, -2.8), (1.0, 1.3, -2.6)])],
                           extra_top=[{"type": "image", "svg": ring(), "x": (JUP["ridge_wide"][0] + MARS["ridge_wide"][0]) / 2,
                                       "y": (JUP["ridge_wide"][1] + MARS["ridge_wide"][1]) / 2, "w": 0.14, "enter": "pop", "at": 0.3,
                                       "sfx": "pop"},
                                      txt("FROM *HERE*", 0.14, 120, enter="pop", at=1.6, sfx="pop")])})
# 3. space, from behind Earth: Mars sits right on Jupiter; the Mars distance counts up
S.append({"say": "Mars is *196 million* kilometres away.",
          "transition": "zoom", "caption_y": 0.7,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 2.6, "zoom": 1.1, "focus": [EE["mars"][0], EE["mars"][1] - 0.05]}]},
          "layers": [plate("space_eye"),
                     tag("MARS", EE["mars"][0] - 0.2, EE["mars"][1] + 0.02, 0.24, "#e07a4a", at=0.4),
                     tag("JUPITER", EE["jup"][0] + 0.18, EE["jup"][1] - 0.07, 0.3, "#f6efe2", at=0.4),
                     {"type": "counter", "from": 0, "to": 196, "decimals": 0, "prefix": "MARS: ", "suffix": " MILLION KM",
                      "x": 0.5, "y": 0.18, "size": 76, "color": "accent", "at": 0.6, "count_dur": 1.0, "enter": "zoom", "sfx": "riser"}]})
# 4. space, from the side: the real gap, Jupiter 4x farther
S.append({"say": "Jupiter? *790 million*. Four times farther, hiding behind it.",
          "transition": "slide_left", "caption_y": 0.5,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.0, "zoom": 1.04, "focus": [0.5, 0.48]}]},
          "layers": [plate("space_side"),
                     dashed(SE["earth"][0], SE["earth"][1], SE["jup"][0], SE["jup"][1], at=0.1),
                     tag("EARTH", SE["earth"][0] - 0.12, SE["earth"][1] - 0.05, 0.22, "#6fc3c0", at=0.1),
                     tag("MARS", SE["mars"][0] + 0.12, SE["mars"][1] + 0.045, 0.22, "#e07a4a", at=0.3),
                     {"type": "image", "svg": ring("#e07a4a"), "x": SE["mars"][0], "y": SE["mars"][1], "w": 0.09, "enter": "pop", "at": 0.3},
                     tag("JUPITER", SE["jup"][0] + 0.25, SE["jup"][1] + 0.0, 0.28, "#f6efe2", at=0.5),
                     {"type": "counter", "from": 196, "to": 790, "decimals": 0, "prefix": "JUPITER: ", "suffix": " MILLION KM",
                      "x": 0.5, "y": 0.34, "size": 66, "color": "accent", "at": 0.3, "count_dur": 1.4, "enter": "pop", "sfx": "riser"},
                     {"type": "image", "svg": card("<text x='350' y='96' text-anchor='middle' font-size='72' fill='#d9534f' " + AN + ">4X FARTHER</text>", 700, 140),
                      "x": 0.5, "y": 0.41, "w": 0.46, "rotate": -3, "enter": "pop", "at": 1.9, "sfx": "pop"}]})
# 5. comic beat: smirk cut-away, the long-distance "situationship"
S.append({"dur": 1.6, "transition": "cut", "captions": False,
          "layers": [plate("ridge_mid", blur=10, keys=[{"t": 0, "scale": 1.35}]), dict(close_ved([["smirk", 0]]), acting="none")],
          "beat": {"kind": "smirk", "at": 0.1, "dur": 1.45, "who": "ved",
                   "text": "mars + jupiter:\nlong-distance *situationship*", "text_y": 0.2}})
# 6. ridge wide: the stargazers look up; the light-time panel
S.append({"say": "Even their light is late: Mars's left *11 minutes* ago, Jupiter's *44*.",
          "transition": "slide_left", "caption_y": 0.5,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 5.0, "zoom": 1.05, "focus": [0.5, 0.46]}]},
          "layers": staged("ridge_wide",
                           people=[person("ridge_wide", "nisha", -1.0, -0.4, [["idle", 0], ["surprised", 2.4]]),
                                   person("ridge_wide", "theo", 0.1, -1.3, [["point", 0], ["shrug", 3.2]]),
                                   ved("ridge_wide", 1.3, -2.6, [["explain", 0], ["point", 2.2]])],
                           extra_top=[{"type": "image", "svg": LIGHT, "x": 0.5, "y": 0.2, "w": 0.8, "enter": "slide_down", "at": 0.6,
                                       "sfx": "whoosh"}])})
# 7. close payoff that loops to the hook
S.append({"say": "Not touching. Just sharing your line of *sight*.", "transition": "cut", "caption_y": 0.64,
          "layers": [plate("ridge_sky", blur=8, keys=[{"t": 0, "scale": 1.3}, {"t": 3.5, "scale": 1.38}]),
                     close_ved([["warm", 0], ["point", 1.2], ["smirk", 2.6]]),
                     sprite("jupiter", 0.74, 0.27, 0.16, at=1.2, enter="pop", sfx="pop"),
                     sprite("mars", 0.66, 0.22, 0.08, at=1.4, enter="pop"),
                     txt("LINE OF *SIGHT*", 0.14, 120, enter="pop", at=2.0, sfx="ding")]})

job = {"id": ID, "title": "Mars and Jupiter 'touching'? 600 million km apart 🪐",
       "description": "This weekend Mars and Jupiter look about one finger-width apart before sunrise (closest on 16 Nov 2026, "
                      "~1.2 degrees). But Mars is ~196 million km from us and Jupiter ~790 million km: about 600 million km "
                      "apart, just on the same line of sight. Their light left ~11 and ~44 minutes ago.\n\n"
                      "Sources: Telescope Advisor and Sky at Night on the Nov 2026 conjunction; EarthSky on measuring the sky with your hand.",
       "tags": ["mars and jupiter", "conjunction", "planetary conjunction", "mars jupiter conjunction 2026", "night sky", "astronomy",
                "space", "science explained"],
       "hashtags": ["#space", "#astronomy"],
       "meta": {"format": "myth-bust", "topic": "Mars-Jupiter conjunction (Nov 2026): 1.2 deg apart in the sky, ~600 million km apart in space; line of sight, light-time 11 vs 44 min",
                "hook": "myth-bust",
                "idea_source": "trending + viral: the Mars-Jupiter conjunction peaks 15-16 Nov 2026 (in the news this week); 'planets touching' is a common misreading; idea from ideas.md",
                "characters": ["ved", "extra"],
                "sources": ["https://www.telescopeadvisor.com/mars-jupiter-conjunction-november-2026/",
                            "https://www.skyatnightmagazine.com/news/mars-jupiter-november-2026",
                            "https://whenthecurveslineup.com/2026/11/06/2026-november-15-jupiter-mars-conjunction-and-bright-planets/",
                            "https://earthsky.org/astronomy-essentials/sky-measurements-degrees-arc-minutes-arc-seconds/"],
                "humour": {"trend": "timeless (no rising trend fit; 'What's up brah' and 'Remember November 2026' already used this week): "
                                    "'situationship' slang as a smirk + 'mars + jupiter: long-distance situationship' card",
                           "beat": "smirk", "scene": 5},
                "claims": [
                    {"claim": "Mars and Jupiter closest ~1.2 deg apart, 16 Nov 2026 02:04 UTC, best seen before sunrise 15-16 Nov", "source": "https://www.telescopeadvisor.com/mars-jupiter-conjunction-november-2026/"},
                    {"claim": "Mars ~196 million km, Jupiter ~790 million km from Earth", "source": "https://www.telescopeadvisor.com/mars-jupiter-conjunction-november-2026/"},
                    {"claim": "the two are nearly 370 million miles (~595 million km) apart", "source": "https://whenthecurveslineup.com/2026/11/06/2026-november-15-jupiter-mars-conjunction-and-bright-planets/"},
                    {"claim": "a finger (pinky) at arm's length covers about 1 degree", "source": "https://earthsky.org/astronomy-essentials/sky-measurements-degrees-arc-minutes-arc-seconds/"},
                    {"claim": "light time: 196e6 km / 299,792 km/s = 10.9 min; 790e6 km = 43.9 min (computed)", "source": "https://www.telescopeadvisor.com/mars-jupiter-conjunction-november-2026/"}]},
       "thumbnail": {"title": "NOT *TOUCHING*", "title_y": 0.14, "title_size": 180, "max_w": 0.95, "blur": 12,
                     "glow": "#ffb35a", "glow_x": 0.5, "glow_y": 0.5, "glow_strength": 1.3, "bg_saturation": 1.5,
                     "tint": ["#1f4fb8", "#f08a24"], "tint_amount": 0.3,
                     "bg": [plate("ridge_wide")],
                     "fg": [sprite("jupiter", 0.74, 0.42, 0.34), sprite("mars", 0.6, 0.36, 0.17),
                            {"type": "character", "id": "ved", "pose": "surprised", "x": 0.42, "y": 0.93, "h": 0.95, "enter": "none",
                             "acting": "none", "talk": False, "ground": False, "allow_outside_safe": True}]},
       "privacy": "public", "speaker": "ved", "assets_script": J + "assets.py", "scenes": S}
json.dump(job, open(J + "job.json", "w"), indent=1, ensure_ascii=False)
print("scenes", len(S), "JUP", JUP, "MARS", MARS, "SE", SE, "EE", EE)
