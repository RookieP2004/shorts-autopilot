"""2026-11-11-b: "Can you see the Great Wall from space?" (myth-bust).
2D Ved + a tour guide and a tourist staged in depth inside Blender sets (a Great-Wall viewpoint from 3 angles, a space-station
module with a round window, Earth by day and by night from orbit) built from stills + cut-outs; spaghetti and binoculars are
animated cut-outs; scale, colour-match and the 1932-cartoon panels are 2D.
Run after the assets exist: python jobs/2026-11-11-b/build_job.py
"""
import json, os, sys
sys.path.insert(0, os.getcwd())
from autopilot.stage import Stage

ID = "2026-11-11-b"
J = f"jobs/{ID}/"
A = J + "assets/"
ST = {n: Stage(A + f"plate_{n}.json") for n in ("wall_wide", "wall_mid", "wall_close", "station_mid")}

OUT = {   # recurring people: same outfits in every shot
    "lin": {"skin": "#d9a27a", "top": ["#d9534f", "vest"], "bottom": ["#34425c", "trousers"], "hair": ["#1a1410", "bun"],
            "hat": ["straw", "#e8c77a"], "shoes": "#25262b"},                                  # tour guide
    "kofi": {"skin": "#6b4430", "top": ["#6fc3c0", "tshirt"], "bottom": ["#c9b48a", "shorts"], "hair": ["#1a1410", "short"],
             "hat": ["cap", "#f2b04a"], "bag": "#8a5a3c", "build": "round", "shoes": "#f6efe2"},  # tourist
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


def stamp(word, color="#d9534f", w=520):
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {w} 170'><rect x='10' y='10' width='{w-20}' height='150' rx='18' "
            f"fill='none' stroke='{color}' stroke-width='14'/><text x='{w/2}' y='128' text-anchor='middle' font-size='118' "
            f"fill='{color}' {AN}>{word}</text></svg>")


def label(t, color, w=620, size=62):
    return card(f"<text x='{w/2}' y='92' text-anchor='middle' font-size='{size}' fill='{color}' {AN}>{t}</text>", w, 140)


# distance card: 400 km straight up, with the ISS dot at the top and the wall as a hairline at the bottom
ALT = card(
    "<text x='300' y='70' text-anchor='middle' font-size='40' fill='#1a1410' " + F + ">HOW HIGH?</text>"
    "<line x1='300' y1='130' x2='300' y2='560' stroke='#34425c' stroke-width='8' stroke-dasharray='22 16'/>"
    "<rect x='255' y='100' width='90' height='40' rx='10' fill='#9aa3ad' stroke='#1a1410' stroke-width='5'/>"
    "<rect x='175' y='108' width='70' height='24' fill='#2f6fd6' stroke='#1a1410' stroke-width='4'/>"
    "<rect x='355' y='108' width='70' height='24' fill='#2f6fd6' stroke='#1a1410' stroke-width='4'/>"
    "<rect x='150' y='280' width='300' height='110' rx='18' fill='#f6efe2'/><text x='300' y='368' text-anchor='middle' font-size='86' fill='#d9534f' " + AN + ">400 KM</text>"
    "<path d='M60,600 Q300,560 540,600' fill='none' stroke='#46965a' stroke-width='16'/>"
    "<text x='300' y='660' text-anchor='middle' font-size='34' fill='#34425c' " + F + ">EARTH</text>", 600, 700)

# width card: the wall in cross-section next to a two-lane road
WIDTH = card(
    "<text x='450' y='70' text-anchor='middle' font-size='42' fill='#1a1410' " + F + ">HOW WIDE?</text>"
    "<rect x='120' y='170' width='260' height='230' fill='#ad9d7a' stroke='#1a1410' stroke-width='6'/>"
    + "".join(f"<rect x='{120 + k*58}' y='135' width='34' height='36' fill='#ad9d7a' stroke='#1a1410' stroke-width='5'/>" for k in range(5))
    + "<line x1='120' y1='440' x2='380' y2='440' stroke='#d9534f' stroke-width='8'/>"
    "<polygon points='120,440 145,425 145,455' fill='#d9534f'/><polygon points='380,440 355,425 355,455' fill='#d9534f'/>"
    "<text x='250' y='510' text-anchor='middle' font-size='64' fill='#d9534f' " + AN + ">~6 M</text>"
    "<rect x='520' y='330' width='260' height='70' fill='#3a3e48' stroke='#1a1410' stroke-width='6'/>"
    "<line x1='540' y1='365' x2='760' y2='365' stroke='#f2b04a' stroke-width='8' stroke-dasharray='30 20'/>"
    "<text x='650' y='510' text-anchor='middle' font-size='44' fill='#34425c' " + AN + ">A 2-LANE ROAD</text>", 900, 560)

# spaghetti scale card: a football pitch in perspective, a strand at the far end, "130 M" between
PITCH = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 900 760'>"
         "<rect x='5' y='5' width='890' height='750' rx='30' fill='#f6efe2' stroke='#1a1410' stroke-width='6'/>"
         "<polygon points='330,140 570,140 820,640 80,640' fill='#5fae55' stroke='#1a1410' stroke-width='6'/>"
         "<polygon points='360,140 395,140 220,640 160,640' fill='#6fbf62'/><polygon points='470,140 505,140 640,640 580,640' fill='#6fbf62'/>"
         "<line x1='450' y1='140' x2='450' y2='640' stroke='#f6efe2' stroke-width='5'/>"
         "<line x1='205' y1='390' x2='695' y2='390' stroke='#f6efe2' stroke-width='5'/>"
         "<ellipse cx='450' cy='390' rx='90' ry='34' fill='none' stroke='#f6efe2' stroke-width='5'/>"
         "<line x1='860' y1='640' x2='860' y2='140' stroke='#d9534f' stroke-width='7'/>"
         "<polygon points='860,140 845,170 875,170' fill='#d9534f'/>"
         "<text x='450' y='705' text-anchor='middle' font-size='52' fill='#1a1410' " + AN + ">YOU, 130 M AWAY</text>"
         "<text x='450' y='95' text-anchor='middle' font-size='40' fill='#1a1410' " + F + ">ONE STRAND, FAR END</text></svg>")

# colour match card: swatches
SWATCH = card(
    "<text x='450' y='66' text-anchor='middle' font-size='40' fill='#1a1410' " + F + ">SPOT THE DIFFERENCE</text>"
    "<rect x='90' y='110' width='330' height='170' rx='22' fill='#ad9d7a' stroke='#1a1410' stroke-width='6'/>"
    "<rect x='480' y='110' width='330' height='170' rx='22' fill='#a9a06c' stroke='#1a1410' stroke-width='6'/>"
    "<text x='255' y='340' text-anchor='middle' font-size='48' fill='#34425c' " + AN + ">WALL</text>"
    "<text x='645' y='340' text-anchor='middle' font-size='48' fill='#34425c' " + AN + ">HILLS</text>", 900, 380)

# a fictional 1930s newspaper cartoon panel (no real logo)
PAPER = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 800 700'>"
         "<rect x='8' y='8' width='784' height='684' rx='12' fill='#efe3c8' stroke='#1a1410' stroke-width='8'/>"
         "<text x='400' y='92' text-anchor='middle' font-size='74' fill='#1a1410' " + AN + ">1932</text>"
         "<line x1='40' y1='118' x2='760' y2='118' stroke='#1a1410' stroke-width='5'/>"
         "<circle cx='600' cy='250' r='90' fill='#f6efe2' stroke='#1a1410' stroke-width='6'/>"
         "<circle cx='570' cy='225' r='16' fill='#d8cdb4'/><circle cx='625' cy='275' r='22' fill='#d8cdb4'/>"
         "<path d='M520,250 L200,430' stroke='#1a1410' stroke-width='4' stroke-dasharray='14 10'/>"
         "<path d='M60,470 Q120,420 180,450 T300,430 T420,460' fill='none' stroke='#1a1410' stroke-width='14'/>"
         + "".join(f"<rect x='{70 + k*44}' y='{440 - (k % 3) * 6}' width='16' height='16' fill='#1a1410'/>" for k in range(8))
         + "<text x='400' y='585' text-anchor='middle' font-size='54' fill='#1a1410' " + AN + ">'VISIBLE FROM THE MOON!'</text>"
         "<text x='400' y='645' text-anchor='middle' font-size='30' fill='#34425c' " + F + ">a newspaper cartoon claim</text></svg>")

S = []
# 1. hook (wall mid): MYTH stamp at frame 0, Ved arms crossed on the terrace, the tourist peers through binoculars
wm = ST["wall_mid"]
S.append({"say": "You can see the Great Wall of China from *space*? Total myth.",
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.6, "zoom": 1.06, "focus": [0.5, 0.52]}]},
          "layers": staged("wall_mid",
                           people=[person("wall_mid", "kofi", -1.6, 0.4, [["point", 0], ["shrug", 2.4]]),
                                   ved("wall_mid", 0.5, -1.7, [["crossed", 0], ["deadpan", 2.6]])],
                           extra_top=[txt("SEE THE GREAT WALL FROM *SPACE*?", 0.2, 98, enter="none"),
                                      {"type": "image", "svg": stamp("MYTH"), "x": 0.5, "y": 0.1, "w": 0.42, "rotate": -6,
                                       "enter": "none", "keys": [{"t": 0, "scale": 1.0}, {"t": 2.6, "scale": 1.0}, {"t": 2.85, "scale": 1.15, "ease": "back"}]}])})
# 2. station: Ved walks in to the window, binoculars float up
sm = ST["station_mid"]
S.append({"say": "Astronauts have *looked*. China's first astronaut searched for it in 2003. Nothing.",
          "transition": "slide_left", "caption_y": 0.6,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 5.0, "zoom": 1.07, "focus": [0.5, 0.45]}]},
          "layers": staged("station_mid",
                           people=[ved("station_mid", 0.5, -1.2, [["welcome", 0], ["point", 1.4], ["think", 3.2], ["shrug", 4.6]],
                                       walk=[(0, 2.4, -1.8), (1.2, 0.5, -1.2)])],
                           extra_top=[txt("ASTRONAUTS *LOOKED*", 0.1, 104, enter="pop", at=0.2, sfx="pop"),
                                      sprite("binoculars", 0.27, 0.27, 0.2, at=1.4, enter="pop", sfx="pop", loop="float", loop_amp=0.012, rotate=-12),
                                      {"type": "image", "svg": stamp("NOTHING", "#d9534f", 600), "x": 0.5, "y": 0.31, "w": 0.48, "rotate": -5,
                                       "enter": "zoom", "at": 4.2, "sfx": "boom"}])})
# 3. earth day view + altitude card
S.append({"say": "The space station flies about *400 kilometres* up.", "transition": "zoom", "caption_y": 0.7,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.2, "zoom": 1.08, "focus": [0.5, 0.55]}]},
          "layers": [plate("earth_day"),
                     {"type": "image", "svg": ALT, "x": 0.5, "y": 0.33, "w": 0.5, "enter": "slide_up", "at": 0.2, "sfx": "pop"}]})
# 4. wall wide: the guide explains, width card
S.append({"say": "And the wall? Long, but only about *six metres* wide. Like a two-lane road.", "transition": "slide_left",
          "caption_y": 0.46,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.55]}, {"t": 4.0, "zoom": 1.06, "focus": [0.5, 0.56]}]},
          "layers": staged("wall_wide",
                           people=[person("wall_wide", "lin", -1.4, 0.2, [["explain", 0], ["point", 1.0], ["explain", 2.8]]),
                                   person("wall_wide", "kofi", 1.8, -0.4, [["idle", 0], ["surprised", 2.0]],
                                          walk=[(0, 3.6, -0.6), (1.4, 1.8, -0.4)]),
                                   ved("wall_wide", 0.2, -2.4, [["explain", 0], ["point", 2.2]])],
                           extra_top=[{"type": "image", "svg": WIDTH, "x": 0.5, "y": 0.2, "w": 0.76, "enter": "pop", "at": 0.6, "sfx": "pop"}])})
# 5. spaghetti scale card
S.append({"say": "That's like spotting one strand of *spaghetti*... from 130 metres away.",
          "transition": "zoom", "caption_y": 0.52,
          "layers": [plate("earth_day", blur=14, keys=[{"t": 0, "scale": 1.2}]),
                     {"type": "image", "svg": PITCH, "x": 0.5, "y": 0.24, "w": 0.78, "enter": "slide_up", "at": 0.1, "sfx": "pop"},
                     sprite("spaghetti", 0.5, 0.125, 0.05, at=1.8, enter="pop", sfx="pop"),
                     sprite("spaghetti", 0.5, 0.67, 0.72, at=1.6, sfx="whoosh", rotate=-4,
                            keys=[{"t": 0, "x": 1.4}, {"t": 0.5, "x": 0.5, "ease": "out"}]),
                     txt("1 STRAND @ *130 M*", 0.75, 92, enter="pop", at=3.4, sfx="ding")]})
# 6. comic beat: silent reaction cut-away (silence + crickets) with a meme caption
S.append({"dur": 1.9, "transition": "cut", "captions": False,
          "layers": [plate("earth_day", blur=10, keys=[{"t": 0, "scale": 1.35}]), dict(close_ved([["side_eye", 0]]), acting="none")],
          "beat": {"kind": "silence", "at": 0.1, "dur": 1.7, "who": "ved",
                   "text": "astronauts at every river:\n*is this the Great Wall?*", "text_y": 0.18}})
# 7. wall close: same colour as the hills
S.append({"say": "Plus, it's built from local stone and earth. Same colour as the hills. *Camouflage*.", "transition": "slide_left",
          "caption_y": 0.7,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.4, "zoom": 1.1, "focus": [0.45, 0.5]}]},
          "layers": [plate("wall_close"),
                     {"type": "image", "svg": SWATCH, "x": 0.5, "y": 0.15, "w": 0.72, "enter": "pop", "at": 1.2, "sfx": "pop"},
                     txt("*CAMOUFLAGE*", 0.3, 120, enter="zoom", at=3.4, sfx="boom")]})
# 8. earth at night: what they CAN see
S.append({"say": "What *can* they see? City lights at night. Runways. Long desert roads.",
          "transition": "flash", "caption_y": 0.7,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.5, "zoom": 1.06, "focus": [0.5, 0.5]}]},
          "layers": [plate("earth_night"),
                     txt("WHAT THEY *CAN* SEE", 0.11, 96, enter="pop", at=0.1, sfx="pop"),
                     {"type": "image", "svg": label("CITY LIGHTS", "#c97a1a"), "x": 0.3, "y": 0.2, "w": 0.42, "enter": "pop", "at": 1.3, "sfx": "pop", "rotate": -3},
                     {"type": "image", "svg": label("RUNWAYS", "#34425c"), "x": 0.7, "y": 0.28, "w": 0.38, "enter": "pop", "at": 2.4, "sfx": "pop", "rotate": 3},
                     {"type": "image", "svg": label("DESERT ROADS", "#7c2533", 680), "x": 0.36, "y": 0.36, "w": 0.46, "enter": "pop", "at": 3.4, "sfx": "pop", "rotate": -2},
                     {"type": "image", "svg": label("BIG + HIGH CONTRAST", "#2f6fd6", 820, 58), "x": 0.5, "y": 0.47, "w": 0.66, "enter": "zoom", "at": 4.6, "sfx": "ding"}]})
# 9. wall mid: where the myth came from (1932 cartoon), guide + tourist react
S.append({"say": "Where did the myth start? A *1932* cartoon said you could see it from the *Moon*.", "transition": "slide_left",
          "caption_y": 0.46,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.52]}, {"t": 4.6, "zoom": 1.05, "focus": [0.5, 0.52]}]},
          "layers": staged("wall_mid",
                           people=[person("wall_mid", "lin", -2.0, 0.6, [["explain", 0], ["point", 1.4]]),
                                   person("wall_mid", "kofi", -0.6, 0.9, [["idle", 0], ["surprised", 3.6]], hops=[[3.7, 0.05, 0.4]]),
                                   ved("wall_mid", 0.9, -1.7, [["think", 0], ["explain", 1.6], ["point", 3.0]])],
                           extra_top=[{"type": "image", "svg": PAPER, "x": 0.5, "y": 0.2, "w": 0.6, "rotate": -3, "enter": "drop",
                                       "at": 1.4, "sfx": "pop"}])})
# 10. station: nearly 30 years before spaceflight (timeline)
TIMELINE = card(
    "<line x1='80' y1='120' x2='820' y2='120' stroke='#1a1410' stroke-width='8'/>"
    "<circle cx='120' cy='120' r='22' fill='#f2b04a' stroke='#1a1410' stroke-width='6'/>"
    "<circle cx='720' cy='120' r='22' fill='#2f6fd6' stroke='#1a1410' stroke-width='6'/>"
    "<text x='120' y='215' text-anchor='middle' font-size='54' fill='#1a1410' " + AN + ">1932</text>"
    "<text x='120' y='265' text-anchor='middle' font-size='30' fill='#34425c' " + F + ">THE CLAIM</text>"
    "<text x='720' y='215' text-anchor='middle' font-size='54' fill='#1a1410' " + AN + ">1961</text>"
    "<text x='690' y='265' text-anchor='middle' font-size='26' fill='#34425c' " + F + ">FIRST PERSON IN SPACE</text>"
    "<text x='450' y='85' text-anchor='middle' font-size='46' fill='#d9534f' " + AN + ">29 YEARS</text>", 900, 300)
S.append({"say": "Nearly thirty years before anyone even went to space.", "transition": "cut", "caption_y": 0.6,
          "camera": {"keys": [{"t": 0, "zoom": 1.04, "focus": [0.5, 0.5]}, {"t": 3.0, "zoom": 1.1, "focus": [0.5, 0.48]}]},
          "layers": staged("station_mid",
                           people=[ved("station_mid", -0.4, -1.4, [["explain", 0], ["smirk", 2.0]])],
                           extra_top=[{"type": "image", "svg": TIMELINE, "x": 0.5, "y": 0.16, "w": 0.8, "enter": "slide_up", "at": 0.2, "sfx": "pop"}])})
# 11. close payoff
S.append({"say": "The wall is great. Just not *that* great from up there.", "transition": "cut", "caption_y": 0.64,
          "layers": [plate("wall_wide", blur=10, keys=[{"t": 0, "scale": 1.35}, {"t": 3.2, "scale": 1.42}]),
                     close_ved([["warm", 0], ["smirk", 1.6], ["crossed", 2.4]]),
                     txt("GREAT. JUST NOT *THAT* GREAT.", 0.13, 96, enter="pop", at=1.4, sfx="ding")]})

job = {"id": ID, "title": "Can you see the Great Wall from space? Nope 🛰️",
       "description": "The Great Wall of China is not visible to the naked eye from orbit: it's only a few metres wide and the same "
                      "colour as the land around it. The myth is older than spaceflight.\n\n"
                      "Sources: Scientific American, 'Is China's Great Wall Visible from Space?'; NASA, 'China's Wall Less Great in View from Space'; "
                      "Space.com, 'What human-made structures can be seen from space?'; Travel China Guide on the wall's width.",
       "tags": ["great wall of china", "visible from space", "myth busting", "space", "astronauts", "iss", "science explained", "history"],
       "hashtags": ["#space", "#mythbusting"],
       "meta": {"format": "myth-bust", "topic": "the Great Wall visible-from-space myth", "hook": "myth-bust",
                "idea_source": "backlog", "characters": ["ved", "extra"],
                "sources": ["https://www.scientificamerican.com/article/is-chinas-great-wall-visible-from-space/",
                            "https://webarchive.library.unt.edu/eot2008/20080917153200/http://www.nasa.gov/vision/space/workinginspace/great_wall.html",
                            "https://www.space.com/human-made-structures-seen-from-space",
                            "https://www.universetoday.com/25364/can-you-see-the-great-wall-of-china-from-space",
                            "https://www.travelchinaguide.com/how-wide-is-great-wall-of-china.htm",
                            "https://www.airspacemag.com/space/cities-at-night-an-astronauts-view-12574626"],
                "humour": {"trend": "'Is This a Pigeon?' misidentification format (rising on Imgflip this week, Nov 2026), as a text card",
                           "beat": "silence", "scene": 6}},
       "privacy": "public", "speaker": "ved", "assets_script": J + "assets.py", "scenes": S}
json.dump(job, open(J + "job.json", "w"), indent=1, ensure_ascii=False)
print("scenes", len(S))
