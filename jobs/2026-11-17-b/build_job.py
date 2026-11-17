"""2026-11-17-b: "Voyager 1 is one light-DAY away. How do we still hear it?" (frontier, number-shock hook).
2D Ved + two station engineers (Lena, Kofi) staged in depth at a blue-hour desert tracking station built in Blender (wide,
mid by the control building, a low hero looking up the big dish), and deep space with a Voyager-style probe (hero close,
lonely wide toward the Sun-star). 2D on top: a distance hud ticking to 25.9 billion km, a live fictional chat on a phone
(hello -> reply two days later), a watts hud + fridge-bulb cut-out, an eqbar (22 W -> under a billionth of a billionth),
a signal line into the dish + cream card (70 m dish, amplifiers at -269 C), the RTG cut-out with a power hud, instrument
optcards that get crossed, a 2 LEFT stamp, honesty tags (PROVEN / R&D).
Facts: Voyager 1 crosses one light-day (25.9 billion km) at 10:16 UTC on 18 Nov 2026 (EarthSky); one-way light ~1 day;
transmitter ~22 W, like a fridge bulb (JPL); received signal weaker than 1e-18 W (JPL: "one-tenth of a billionth-trillionth
of a watt"; MakeTechEasier: ~1 attowatt); DSN 70 m dishes, liquid-helium-cooled amplifiers (MakeTechEasier, JPL);
RTGs ~470 W at launch, ~4 W lost per year (WAMC / MakeTechEasier); Cosmic Ray Subsystem off Feb 2025 (NASA) and LECP off
17 Apr 2026, two instruments left (WAMC); team hopes to keep at least one instrument running into the 2030s (WAMC).
Run after the assets exist: python jobs/2026-11-17-b/build_job.py
"""
import json, os, sys
sys.path.insert(0, os.getcwd())
from autopilot.stage import Stage

ID = "2026-11-17-b"
J = f"jobs/{ID}/"
A = J + "assets/"
ST = {n: Stage(A + f"plate_{n}.json") for n in ("dsn_wide", "dsn_mid", "dsn_up", "space_hero", "space_wide")}

OUT = {   # recurring station engineers: same outfit in every shot
    "lena": {"skin": "#e0b08a", "build": "slim", "hair": ["#6b4529", "bun"], "top": ["#f6efe2", "jacket"],
             "bottom": ["#34425c", "trousers"], "shoes": "#25262b", "bag": "#d9534f"},
    "kofi": {"skin": "#7a4a2e", "build": "regular", "hair": ["#1a1410", "short"], "hat": ["cap", "#f2b04a"],
             "top": ["#f08a24", "jacket"], "bottom": ["#3a3e48", "trousers"], "shoes": "#25262b"},
}
F = "font-family='Poppins, DejaVu Sans, sans-serif' font-weight='800'"
AN = "font-family='Anton, DejaVu Sans, sans-serif'"
DISH = (-2.2, 15.0, 7.6)


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


def staged(set_, people=(), extra_top=()):
    out = [plate(set_)] + sorted(people, key=lambda L: -L["_depth"]) + list(extra_top)
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


def label(word, color="#f2b04a", w=420):
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {w} 96'><rect x='4' y='4' width='{w-8}' height='88' rx='20' "
            f"fill='#1a1410' fill-opacity='0.82' stroke='{color}' stroke-width='5'/><text x='{w/2}' y='68' text-anchor='middle' "
            f"font-size='56' fill='{color}' {AN}>{word}</text></svg>")


def lab(word, x, y, w=0.3, color="#f2b04a", at=0.0, **k):
    return {"type": "image", "svg": label(word, color, max(420, 40 * len(word) + 90)), "x": x, "y": y, "w": w, "enter": "pop", "at": at, "sfx": "pop", **k}


def hud(lbl, y=0.74, **k):
    return {"type": "hud", "label": lbl, "x": k.pop("x", 0.5), "y": y, "enter": k.pop("enter", "pop"), "sfx": "click",
            "indian": False, **k}


def signal(x0, y0, x1, y1, at=0.0, color="#6fe3ff"):
    """A dashed radio signal sliding from x0,y0 to the dish at x1,y1 (pulses)."""
    W, H = 1080, 1920
    return {"type": "image", "x": 0.5, "y": 0.5, "w": 1.0, "enter": "fade", "at": at, "loop": "pulse", "loop_amp": 0.02,
            "svg": (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {W} {H}'><line x1='{x0*W:.0f}' y1='{y0*H:.0f}' "
                    f"x2='{x1*W:.0f}' y2='{y1*H:.0f}' stroke='{color}' stroke-width='9' stroke-dasharray='26 18' opacity='0.9'/>"
                    f"<circle cx='{x1*W:.0f}' cy='{y1*H:.0f}' r='22' fill='{color}' opacity='0.6'/></svg>")}


CHAT = {"kind": "chat", "name": "VOYAGER 1", "sub": "25.9 billion km away",
        "msgs": [{"text": "hi Voyager!", "side": "out", "time": "Mon 10:16", "ticks": 1, "at": 0.2},
                 {"text": "...still travelling (1 day)", "side": "out", "time": "Tue 10:16", "ticks": 1, "at": 0.9},
                 {"text": "hi Earth!", "side": "in", "time": "Wed 10:16", "at": 1.7}],
        "input": "Message"}

KM = 25_900_000_000
S = []
# 0. hook: Ved close in front of the blurred probe; distance hud ticks at frame 0, ONE LIGHT-DAY headline
S.append({"say": "November 18th: Voyager 1 hits one light-*day* from Earth.",
          "caption_y": 0.44,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.6, "zoom": 1.06, "focus": [0.5, 0.48]}]},
          "layers": [plate("space_hero", blur=5, keys=[{"t": 0, "scale": 1.12}, {"t": 4.0, "scale": 1.2}]),
                     txt("ONE *LIGHT-DAY* AWAY", 0.13, 116, enter="none", max_w=0.95),
                     hud("km from earth", y=0.25, to=KM, **{"from": 25_000_000_000}, count_dur=2.6, tone="blue", enter="none", width_of="25,900,000,000"),
                     sprite("probe", 0.78, 0.36, 0.3, enter="pop", at=0.6, sfx="whoosh",
                            keys=[{"t": 0, "x": 1.1, "y": 0.4, "rot": -8}, {"t": 1.0, "x": 0.76, "y": 0.35, "rot": 4, "ease": "out"},
                                  {"t": 4.0, "x": 0.72, "y": 0.34, "rot": 8}]),
                     close_ved([["surprised", 0], ["point", 1.6], ["explain", 2.8]], h=0.9, y=0.86)]})
# 1. station mid: Ved texts Voyager; the live chat answers two days later
S.append({"say": "Say hi: the reply takes *two days*.",
          "transition": "slide_left", "caption_y": 0.66,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.4, "zoom": 1.05, "focus": [0.46, 0.5]}]},
          "layers": staged("dsn_mid",
                           people=[ved("dsn_mid", 2.0, -0.6, [["explain", 0], ["point", 1.2], ["think", 2.4]],
                                       walk=[(0, 0.6, -0.9), (0.9, 2.0, -0.6)]),
                                   person("dsn_mid", "lena", 3.9, 1.6, [["idle", 0], ["shrug", 2.4]])],
                           extra_top=[{"type": "phone", "sprite": A + "phone.png", "screen": CHAT, "x": 0.7, "y": 0.3, "w": 0.3,
                                       "tilt": [[0, -18, 4], [3.5, 8, 2]], "enter": "rise", "at": 0.1, "sfx": "whoosh"},
                                      {"type": "eqbar", "keys": [[0.3, "1 day there"], [1.1, "1 day there + 1 day back = *2 days*"]],
                                       "tone": "blue", "x": 0.5, "y": 0.09, "enter": "fade", "at": 0.3}])})
# 2. comic beat: side-eye cut-away ('I got so mad' trend)
S.append({"dur": 1.7, "transition": "cut", "captions": False,
          "layers": [plate("dsn_mid", blur=10, keys=[{"t": 0, "scale": 1.35}]), dict(close_ved([["side_eye", 0]]), acting="none")],
          "beat": {"kind": "side_eye", "at": 0.1, "dur": 1.5, "who": "ved",
                   "text": "voyager: i got so mad i moved\n*one light-day* away", "text_y": 0.2}})
# 3. space hero: the radio = a fridge bulb
S.append({"say": "Its radio? *22 watts*. A fridge bulb.",
          "transition": "zoom", "caption_y": 0.7,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.4, 0.5]}, {"t": 3.4, "zoom": 1.1, "focus": [0.36, 0.48]}]},
          "layers": [plate("space_hero"),
                     hud("radio power", y=0.12, to=22, count_dur=1.0, suffix=" W", tone="gold", width_of="22 W", at=0.2),
                     sprite("bulb", 0.7, 0.33, 0.18, enter="pop", at=1.1, sfx="pop",
                            keys=[{"t": 0, "rot": -10}, {"t": 2.0, "rot": 6}]),
                     lab("= FRIDGE BULB", 0.64, 0.47, 0.4, "#f2b04a", at=1.3),
                     tag_layer(0.74, 0.2, 1.5)]})
# 4. looking up the dish: the signal fades to almost nothing
up = ST["dsn_up"]
UX, UY = up.point(*DISH)
S.append({"say": "Here, that's under a *billionth of a billionth* of a watt.",
          "transition": "slide_up", "caption_y": 0.62,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.4, "zoom": 1.07, "focus": [UX, UY]}]},
          "layers": [plate("dsn_up"),
                     signal(0.92, 0.0, UX, UY, at=0.2),
                     hud("signal reaching earth", y=0.15, text="0.000...001 W", sub="17 zeros after the point", tone="blue", at=0.4),
                     {"type": "eqbar", "keys": [[0.5, "22 W"], [1.4, "22 W ÷ a billion billion"]], "tone": "blue",
                      "x": 0.5, "y": 0.26, "enter": "fade", "at": 0.6},
                     tag_layer(0.78, 0.32, 2.0)]})
# 5. station wide: we still catch it -> the engineers cheer
wide = ST["dsn_wide"]
WX, WY = wide.point(*DISH)
S.append({"say": "We still catch it, with *70-metre* dishes and super-cold amplifiers.",
          "transition": "slide_left", "caption_y": 0.5,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.0, "zoom": 1.05, "focus": [0.48, 0.48]}]},
          "layers": staged("dsn_wide",
                           people=[ved("dsn_wide", 0.4, -4.6, [["welcome", 0], ["point", 1.0], ["warm", 2.6]]),
                                   person("dsn_wide", "kofi", 2.2, 0.6, [["point", 0], ["cheer", 2.4]], hops=[[2.4, 0.05, 0.4]]),
                                   person("dsn_wide", "lena", 3.4, 1.4, [["idle", 0], ["happy", 2.5]], hops=[[2.6, 0.04, 0.4]])],
                           extra_top=[signal(0.98, 0.02, WX, WY, at=0.0),
                                      {"type": "image", "svg": card("<text x='420' y='98' text-anchor='middle' font-size='72' fill='#1a1410' " + AN + ">70 M <tspan fill='#d9534f'>DISH</tspan></text>", 840, 150),
                                       "x": 0.5, "y": 0.12, "w": 0.64, "rotate": -2, "enter": "slide_right", "at": 0.6, "sfx": "pop"},
                                      {"type": "image", "svg": card("<text x='310' y='98' text-anchor='middle' font-size='64' fill='#1a1410' " + AN + ">AMPLIFIERS AT</text><text x='650' y='98' text-anchor='middle' font-size='64' fill='#3f7fbf' " + AN + ">-269 C</text>", 840, 150),
                                       "x": 0.5, "y": 0.205, "w": 0.7, "rotate": 2, "enter": "slide_left", "at": 1.8, "sfx": "pop"},
                                      tag_layer(0.8, 0.28, 2.4)])})
# 6. the power problem: the RTG, power hud falls
S.append({"say": "The enemy is *power*: its plutonium loses 4 watts a year.",
          "transition": "zoom", "caption_y": 0.7,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.6, "zoom": 1.06, "focus": [0.5, 0.45]}]},
          "layers": [plate("space_hero", blur=9, keys=[{"t": 0, "scale": 1.25}, {"t": 5, "scale": 1.32}]),
                     sprite("rtg", 0.5, 0.4, 0.42, enter="pop", at=0.1, sfx="pop", keys=[{"t": 0, "rot": -4}, {"t": 5, "rot": 4}]),
                     lab("PLUTONIUM POWER", 0.5, 0.585, 0.5, "#f08a24", at=0.5),
                     hud("power", y=0.12, steps=[[0, 470], [1.2, 400], [1.9, 300], [2.6, 230]], count_dur=0.5, suffix=" W",
                         tone="red", width_of="470 W", at=0.3),
                     {"type": "eqbar", "keys": [[0.4, "1977: ~470 W"], [2.2, "now: under *250 W*"]],
                      "tone": "red", "x": 0.5, "y": 0.205, "enter": "fade", "at": 0.4},
                     tag_layer(0.8, 0.27, 1.8)]})
# 7. station mid: instruments switched off one by one -> 2 LEFT
S.append({"say": "So instruments get switched *off*. Two left.",
          "transition": "slide_left", "caption_y": 0.5,
          "camera": {"keys": [{"t": 0, "zoom": 1.04, "focus": [0.5, 0.5]}, {"t": 3.4, "zoom": 1.0, "focus": [0.5, 0.5]}]},
          "layers": staged("dsn_mid",
                           people=[ved("dsn_mid", 2.0, -0.6, [["serious", 0], ["explain", 1.4]]),
                                   person("dsn_mid", "lena", 3.9, 1.6, [["sad", 0.6]])],
                           extra_top=[{"type": "optcard", "label": "off: feb 2025", "text": "COSMIC RAYS", "tone": "red", "x": 0.3,
                                       "y": 0.12, "w": 0.4, "rotate": -2, "enter": "pop", "at": 0.1, "sfx": "pop",
                                       "verdict": "cross", "verdict_at": 0.7},
                                      {"type": "optcard", "label": "off: apr 2026", "text": "PARTICLES", "tone": "red", "x": 0.72,
                                       "y": 0.12, "w": 0.4, "rotate": 2, "enter": "pop", "at": 0.8, "sfx": "pop",
                                       "verdict": "cross", "verdict_at": 1.4},
                                      hud("instruments still on", y=0.26, steps=[[0, 4], [0.7, 3], [1.4, 2]], count_dur=0.3,
                                          tone="green", width_of="4", at=0.0),
                                      {"type": "stamp", "text": "2 LEFT", "tone": "red", "angle": -7, "size": 110, "x": 0.5, "y": 0.36,
                                       "at": 1.8, "sfx": "thud"}])})
# 8. the hope, honestly tagged: into the 2030s
S.append({"say": "The hope: one still listening into the *2030s*.",
          "transition": "slide_up", "caption_y": 0.62,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.0, "zoom": 1.08, "focus": [UX, UY]}]},
          "layers": [plate("dsn_up"),
                     signal(0.92, 0.0, UX, UY, at=0.0, color="#9fe8a0"),
                     {"type": "optcard", "label": "nasa's goal", "text": "ONE INSTRUMENT\nINTO THE 2030s", "tone": "green", "x": 0.5,
                      "y": 0.15, "w": 0.66, "rotate": -2, "enter": "pop", "at": 0.3, "sfx": "pop"},
                     tag_layer(0.78, 0.3, 1.2, "R&amp;D", "#f2b04a")]})
# 9. close payoff: it flies on in silence, the distance keeps ticking (loops to the hook)
S.append({"say": "Then silence. One light-day... and *counting*.",
          "transition": "cut", "caption_y": 0.44,
          "layers": [plate("space_wide", blur=6, keys=[{"t": 0, "scale": 1.2}, {"t": 4.0, "scale": 1.3}]),
                     hud("km from earth", y=0.2, steps=[[0, KM], [0.1, KM + 1_500_000]], count_dur=4.0, tone="blue", enter="none",
                         width_of="25,901,500,000"),
                     sprite("probe", 0.7, 0.33, 0.22, keys=[{"t": 0, "x": 0.66, "y": 0.34, "scale": 1.0},
                                                             {"t": 4.0, "x": 0.8, "y": 0.3, "scale": 0.8}]),
                     close_ved([["warm", 0], ["point", 1.2], ["smirk", 2.2]], h=0.9, y=0.86),
                     txt("AND *COUNTING*", 0.11, 120, enter="pop", at=1.6, sfx="ding")]})

job = {"id": ID, "title": "Voyager 1 is one light-DAY away. We still hear it 📡",
       "description": "On 18 November 2026 Voyager 1 becomes the first human-made object one light-day from Earth: 25.9 billion km, "
                      "so a 'hello' takes a day to arrive and the reply another day. Its radio runs on about 22 watts (a fridge "
                      "bulb), and the signal reaches us weaker than a billionth of a billionth of a watt, yet NASA's 70 m dishes "
                      "with super-cold amplifiers still catch it. The catch: its plutonium power drops ~4 W a year, so instruments "
                      "are being switched off (two left); the team hopes to keep one running into the 2030s.\n\n"
                      "Sources: EarthSky; NASA/JPL; WAMC (April 2026); MakeTechEasier on how the Deep Space Network hears Voyager.",
       "tags": ["voyager 1", "one light day", "voyager 1 2026", "nasa", "deep space network", "space", "interstellar space",
                "space explained", "astronomy"],
       "hashtags": ["#space", "#nasa"],
       "instagram": {"hashtags": ["#space", "#voyager1", "#nasa", "#astronomy", "#explained"]},
       "meta": {"format": "frontier", "topic": "Voyager 1 reaches one light-day (25.9 billion km) on 18 Nov 2026: 2-day round trip, "
                                               "22 W radio, signal under 1e-18 W, 70 m DSN dishes + cryo amplifiers, RTG losing ~4 W/yr, "
                                               "instruments switched off (2 left), hope of one instrument into the 2030s",
                "hook": "number-shock",
                "idea_source": "trending + unique: the one-light-day milestone is this week's space news (18 Nov 2026); "
                               "the 'how do we still hear it' angle (fridge-bulb radio, attowatt signal) is rarely done in Shorts; backlog idea 2026-11-16",
                "characters": ["ved", "extra"],
                "sources": ["https://earthsky.org/space/voyager-1-1-light-day-from-earth-november-17-18-2026/",
                            "https://www.jpl.nasa.gov/news/two-voyagers-taught-us-how-to-listen-to-space/",
                            "https://maketecheasier.com/how-deep-space-network-hears-voyager/",
                            "https://www.wamc.org/2026-04-19/the-little-probe-that-could-why-voyager-1-matters-and-why-nasa-just-switched-part-of-it-off",
                            "https://www.jpl.nasa.gov/news/nasa-turns-off-two-voyager-science-instruments-to-extend-mission/",
                            "https://www.space.com/17688-voyager-1.html"],
                "humour": {"trend": "'I Got So Mad' TikTok trend (absurd retaliation captions, rising late Oct-Nov 2026, Know Your Meme 13 Nov): "
                                    "'voyager: i got so mad i moved one light-day away'",
                           "beat": "side_eye", "scene": 2},
                "claims": [
                    {"claim": "Voyager 1 crosses one light-day (~25.9 billion km) at 10:16 UTC on 18 Nov 2026, launched 5 Sep 1977", "tag": "PROVEN",
                     "source": "https://earthsky.org/space/voyager-1-1-light-day-from-earth-november-17-18-2026/"},
                    {"claim": "a one-way message takes about a day, so a reply takes about two days", "tag": "PROVEN",
                     "source": "https://earthsky.org/space/voyager-1-1-light-day-from-earth-november-17-18-2026/"},
                    {"claim": "its transmitter is about 22 W, like a refrigerator bulb", "tag": "PROVEN",
                     "source": "https://www.jpl.nasa.gov/news/two-voyagers-taught-us-how-to-listen-to-space/"},
                    {"claim": "the signal arrives weaker than a billionth of a billionth of a watt (JPL: one-tenth of a billionth-trillionth; ~1 attowatt quoted)", "tag": "PROVEN",
                     "source": "https://www.jpl.nasa.gov/news/two-voyagers-taught-us-how-to-listen-to-space/"},
                    {"claim": "caught by 70 m DSN dishes with liquid-helium-cooled (~-269 C) amplifiers", "tag": "PROVEN",
                     "source": "https://maketecheasier.com/how-deep-space-network-hears-voyager/"},
                    {"claim": "RTGs gave ~470 W at launch and lose ~4 W a year; now under 250 W", "tag": "PROVEN",
                     "source": "https://maketecheasier.com/how-deep-space-network-hears-voyager/"},
                    {"claim": "Cosmic Ray Subsystem switched off Feb 2025, LECP 17 Apr 2026; two science instruments left", "tag": "PROVEN",
                     "source": "https://www.wamc.org/2026-04-19/the-little-probe-that-could-why-voyager-1-matters-and-why-nasa-just-switched-part-of-it-off"},
                    {"claim": "engineers hope to keep at least one instrument running into the 2030s (power-saving plan being tested)", "tag": "R&D",
                     "source": "https://www.wamc.org/2026-04-19/the-little-probe-that-could-why-voyager-1-matters-and-why-nasa-just-switched-part-of-it-off"}]},
       "thumbnail": {"title": "ONE *LIGHT-DAY*", "title_y": 0.15, "title_size": 150, "max_w": 0.95, "blur": 12,
                     "glow": "#ffb35a", "glow_x": 0.5, "glow_y": 0.5, "glow_strength": 1.3, "bg_saturation": 1.4,
                     "tint": ["#1f4fb8", "#f08a24"], "tint_amount": 0.3,
                     "bg": [plate("dsn_wide")],
                     "fg": [sprite("probe", 0.66, 0.4, 0.62),
                            {"type": "character", "id": "ved", "pose": "surprised", "x": 0.42, "y": 0.95, "h": 0.85, "enter": "none",
                             "acting": "none", "talk": False, "ground": False, "allow_outside_safe": True}]},
       "privacy": "public", "speaker": "ved", "assets_script": J + "assets.py", "scenes": S}
json.dump(job, open(J + "job.json", "w"), indent=1, ensure_ascii=False)
print("scenes", len(S), "UP", (UX, UY), "WIDE", (WX, WY))
