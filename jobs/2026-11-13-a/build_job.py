"""2026-11-13-a: "That shooting star? It was a grain of sand" (myth-bust).
2D Ved + two stargazers staged in depth on a Blender night hilltop (wide, mid, looking up at the sky) built from stills +
cut-outs; the comet, the sand grain (cool and white-hot) are animated cut-outs; meteor streaks, the altitude panel,
the speed counter and the London-Paris card are 2D.
Run after the assets exist: python jobs/2026-11-13-a/build_job.py
"""
import json, os, sys
sys.path.insert(0, os.getcwd())
from autopilot.stage import Stage

ID = "2026-11-13-a"
J = f"jobs/{ID}/"
A = J + "assets/"
ST = {n: Stage(A + f"plate_{n}.json") for n in ("hill_wide", "hill_mid")}

OUT = {   # recurring stargazers: same outfit in every shot
    "mira": {"skin": "#c68a5e", "build": "slim", "hair": ["#1a1410", "long"], "hat": ["beret", "#d9534f"],
             "top": ["#f2b04a", "jacket"], "bottom": ["#34425c", "trousers"], "shoes": "#25262b"},
    "omar": {"skin": "#8d5a3b", "build": "regular", "hair": ["#1a1410", "curly"], "top": ["#6fc3c0", "jacket"],
             "bottom": ["#3a3e48", "trousers"], "shoes": "#25262b", "bag": "#8a5a3c"},
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


STREAK = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 700 60'><defs>"
          "<linearGradient id='g' x1='0' x2='1'><stop offset='0' stop-color='#ffffff' stop-opacity='0'/>"
          "<stop offset='0.7' stop-color='#bfeaff' stop-opacity='0.55'/><stop offset='1' stop-color='#ffffff' stop-opacity='1'/></linearGradient>"
          "<radialGradient id='h'><stop offset='0' stop-color='#ffffff'/><stop offset='0.4' stop-color='#fff3c4' stop-opacity='0.9'/>"
          "<stop offset='1' stop-color='#ffd27a' stop-opacity='0'/></radialGradient></defs>"
          "<polygon points='0,30 660,22 660,38' fill='url(#g)'/><circle cx='662' cy='30' r='28' fill='url(#h)'/></svg>")


GLOW = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 400'><defs><radialGradient id='o'>"
        "<stop offset='0' stop-color='#fff3c4'/><stop offset='0.25' stop-color='#ffb35a' stop-opacity='0.9'/>"
        "<stop offset='1' stop-color='#ff7a2a' stop-opacity='0'/></radialGradient></defs><circle cx='200' cy='200' r='200' fill='url(#o)'/></svg>")


def streak(x0, y0, x1, y1, at, dur=0.7, w=0.55, rot=-28):
    return {"type": "image", "svg": STREAK, "x": x0, "y": y0, "w": w, "rotate": rot, "at": at, "enter": "fade", "enter_dur": 0.08,
            "until": at + dur, "exit": "fade", "keys": [{"t": 0, "x": x0, "y": y0}, {"t": dur, "x": x1, "y": y1, "ease": "linear"}]}


# star vs shooting star: a sun-sized ball vs a dot
COMPARE = card(
    "<circle cx='230' cy='190' r='120' fill='#f2b04a' stroke='#1a1410' stroke-width='6'/>"
    "<text x='230' y='360' text-anchor='middle' font-size='54' fill='#1a1410' " + AN + ">REAL STAR</text>"
    "<text x='230' y='405' text-anchor='middle' font-size='30' fill='#34425c' " + F + ">A WHOLE SUN</text>"
    "<text x='450' y='210' text-anchor='middle' font-size='70' fill='#d9534f' " + AN + ">VS</text>"
    "<circle cx='680' cy='190' r='9' fill='#d9b98a' stroke='#1a1410' stroke-width='3'/>"
    "<circle cx='680' cy='190' r='34' fill='none' stroke='#d9534f' stroke-width='5' stroke-dasharray='10 8'/>"
    "<text x='680' y='360' text-anchor='middle' font-size='48' fill='#1a1410' " + AN + ">SHOOTING STAR</text>"
    "<text x='680' y='405' text-anchor='middle' font-size='30' fill='#34425c' " + F + ">A SAND GRAIN</text>", 900, 450)

# how high: meteors glow ~100 km up, planes fly at ~11 km
ALT = card(
    "<text x='450' y='70' text-anchor='middle' font-size='44' fill='#1a1410' " + AN + ">HOW HIGH?</text>"
    "<rect x='80' y='100' width='740' height='300' rx='18' fill='#23306e'/>"
    "<rect x='80' y='330' width='740' height='70' rx='0' fill='#6fc3c0' opacity='0.55'/>"
    "<line x1='80' y1='150' x2='820' y2='150' stroke='#f6efe2' stroke-width='4' stroke-dasharray='14 10'/>"
    "<polygon points='520,120 700,160 520,140' fill='#fff3c4'/><circle cx='700' cy='160' r='12' fill='#ffffff'/>"
    "<text x='110' y='137' font-size='40' fill='#f2b04a' " + AN + ">100 KM: IT GLOWS</text>"
    "<line x1='80' y1='330' x2='820' y2='330' stroke='#f6efe2' stroke-width='3' stroke-dasharray='8 10'/>"
    "<text x='110' y='318' font-size='32' fill='#f6efe2' " + F + ">11 KM: PLANES</text>"
    "<rect x='600' y='300' width='70' height='14' rx='7' fill='#f6efe2'/>"
    "<text x='110' y='385' font-size='32' fill='#1a1410' " + F + ">YOU</text>", 900, 430)

S = []
# 0. hook (hill mid): the myth at frame 0, a meteor streaks over Ved
S.append({"say": "That shooting star you wished on? It was a grain of *sand*.",
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.6, "zoom": 1.06, "focus": [0.5, 0.52]}]},
          "layers": staged("hill_mid",
                           people=[ved("hill_mid", 0.9, 1.9, [["crossed", 0], ["point", 1.3], ["smirk", 2.6]])],
                           fg=True,
                           extra_top=[streak(0.82, 0.12, 0.3, 0.34, 0.0, 1.1, 0.6),
                                      {"type": "image", "svg": stamp("MYTH", w=420), "x": 0.5, "y": 0.13, "w": 0.34, "rotate": -5,
                                       "enter": "none"},
                                      txt("SHOOTING STARS ARE *STARS*", 0.25, 100, enter="none")])})
# 1. sky: real stars are suns, the size comparison
S.append({"say": "Real stars are whole *suns*, trillions of kilometres away.",
          "transition": "slide_up", "caption_y": 0.6,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.6, "zoom": 1.08, "focus": [0.5, 0.45]}]},
          "layers": [plate("hill_up"),
                     {"type": "image", "svg": COMPARE, "x": 0.5, "y": 0.27, "w": 0.8, "enter": "slide_up", "at": 0.2, "sfx": "pop"},
                     {"type": "counter", "from": 0, "to": 40, "decimals": 0, "prefix": "NEAREST: ", "suffix": " TRILLION KM",
                      "x": 0.5, "y": 0.5, "size": 64, "color": "accent", "at": 1.6, "count_dur": 1.2, "enter": "pop", "sfx": "pop"}]})
# 2. hill wide: a comet sheds crumbs; one crumb = a sand grain; the stargazers lean in
S.append({"say": "A shooting star is a crumb of *comet dust*, the size of a sand grain.",
          "transition": "slide_left", "caption_y": 0.44,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.5, "zoom": 1.06, "focus": [0.5, 0.48]}]},
          "layers": staged("hill_wide",
                           people=[person("hill_wide", "mira", -1.5, -1.0, [["idle", 0], ["point", 0.8], ["surprised", 3.0]]),
                                   person("hill_wide", "omar", -0.5, -2.0, [["idle", 0], ["surprised", 3.1]]),
                                   ved("hill_wide", 1.15, -2.4, [["explain", 0], ["point", 2.6]],
                                       walk=[(0, 3.4, -2.6), (1.1, 1.15, -2.4)])],
                           extra_top=[sprite("comet", 0.66, 0.15, 0.3, at=0.1, enter="fade", sfx="whoosh",
                                             keys=[{"t": 0, "x": 0.86, "y": 0.11, "rot": -10}, {"t": 4.5, "x": 0.6, "y": 0.17, "rot": 6, "ease": "linear"}]),
                                      sprite("grain", 0.5, 0.29, 0.16, at=2.4, enter="zoom", sfx="pop",
                                             keys=[{"t": 0, "x": 0.66, "y": 0.18, "scale": 0.2}, {"t": 0.6, "x": 0.38, "y": 0.29, "scale": 1.0, "ease": "back"}]),
                                      {"type": "image", "svg": card("<text x='300' y='92' text-anchor='middle' font-size='60' fill='#1a1410' " + AN + ">ABOUT 1 MM</text>", 600, 140),
                                       "x": 0.66, "y": 0.29, "w": 0.4, "rotate": 3, "enter": "pop", "at": 3.0, "sfx": "pop"}])})
# 3. sky: the speed, London to Paris in five seconds
S.append({"say": "It hits our air at *71 kilometres a second*. London to Paris in five seconds.",
          "transition": "zoom", "caption_y": 0.6,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 5.0, "zoom": 1.1, "focus": [0.5, 0.42]}]},
          "layers": [plate("hill_up"),
                     streak(0.9, 0.1, 0.1, 0.5, 0.2, 0.9, 0.7, -26),
                     {"type": "counter", "from": 0, "to": 71, "decimals": 0, "suffix": " KM/S", "x": 0.5, "y": 0.2,
                      "size": 150, "color": "accent", "at": 0.2, "count_dur": 1.4, "enter": "zoom", "sfx": "riser"},
                     {"type": "image", "svg": card("<text x='60' y='95' font-size='62' fill='#1a1410' " + AN + ">LONDON</text>"
                                                   "<line x1='310' y1='72' x2='520' y2='72' stroke='#d9534f' stroke-width='10'/>"
                                                   "<polygon points='560,72 515,48 515,96' fill='#d9534f'/>"
                                                   "<text x='600' y='95' font-size='62' fill='#1a1410' " + AN + ">PARIS</text>"
                                                   "<text x='450' y='170' text-anchor='middle' font-size='54' fill='#d9534f' " + AN + ">5 SECONDS</text>", 900, 210),
                      "x": 0.5, "y": 0.36, "w": 0.78, "enter": "slide_up", "at": 2.8, "sfx": "whoosh"}]})
# 4. sky: the air in front gets crushed and glows, 100 km up
S.append({"say": "That crushes the air in front until it *glows*, 100 kilometres up.",
          "transition": "slide_left", "caption_y": 0.62,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.0, "zoom": 1.06, "focus": [0.5, 0.48]}]},
          "layers": [plate("hill_up", blur=4),
                     sprite("grain", 0.3, 0.5, 0.14, keys=[{"t": 0, "x": 0.2, "y": 0.5, "rot": 0}, {"t": 1.2, "x": 0.42, "y": 0.5, "rot": 40, "ease": "linear"}],
                            until=1.2, exit="fade"),
                     {"type": "image", "svg": GLOW, "x": 0.42, "y": 0.5, "w": 0.5, "at": 1.0, "enter": "fade",
                      "keys": [{"t": 0, "x": 0.42, "y": 0.5, "scale": 1.0}, {"t": 2.6, "x": 0.66, "y": 0.5, "scale": 0.55, "ease": "linear"}],
                      "until": 2.6, "exit": "fade"},
                     sprite("grain_hot", 0.42, 0.5, 0.15, at=1.0, enter="fade", sfx="boom",
                            keys=[{"t": 0, "x": 0.42, "y": 0.5, "scale": 1.0}, {"t": 2.6, "x": 0.66, "y": 0.5, "scale": 0.55, "ease": "linear"}],
                            until=2.6, exit="fade"),
                     {"type": "image", "svg": ALT, "x": 0.5, "y": 0.22, "w": 0.8, "enter": "slide_down", "at": 1.6, "sfx": "pop"}]})
# 5. comic beat: side-eye cut-away, the "Remember November 2026" meme bent to fit
S.append({"dur": 1.6, "transition": "cut", "captions": False,
          "layers": [plate("hill_mid", blur=10, keys=[{"t": 0, "scale": 1.35}]), dict(close_ved([["side_eye", 0]]), acting="none")],
          "beat": {"kind": "side_eye", "at": 0.1, "dur": 1.45, "who": "ved",
                   "text": "remember november 2026?\n*it was sand*", "text_y": 0.2}})
# 6. hill wide: the Leonids, streaks everywhere, the stargazers cheer
S.append({"say": "And on November 17th, the *Leonids* bring up to fifteen an hour.",
          "transition": "slide_left", "caption_y": 0.44,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.5, "zoom": 1.05, "focus": [0.5, 0.46]}]},
          "layers": staged("hill_wide",
                           people=[person("hill_wide", "mira", -1.5, -1.0, [["point", 0], ["cheer", 1.2]], hops=[[1.3, 0.05, 0.4]]),
                                   person("hill_wide", "omar", -0.5, -2.0, [["idle", 0], ["happy", 1.4], ["wave", 2.6]], hops=[[1.5, 0.04, 0.4]]),
                                   ved("hill_wide", 1.15, -2.4, [["welcome", 0], ["point", 1.4]])],
                           extra_top=[streak(0.78, 0.06, 0.4, 0.2, 0.3, 0.6, 0.4), streak(0.6, 0.1, 0.2, 0.26, 1.2, 0.7, 0.5),
                                      streak(0.9, 0.18, 0.55, 0.32, 2.1, 0.6, 0.35), streak(0.7, 0.04, 0.3, 0.18, 3.0, 0.6, 0.45),
                                      txt("THE *LEONIDS*", 0.14, 120, enter="pop", at=0.6, sfx="pop"),
                                      {"type": "image", "svg": card("<text x='350' y='92' text-anchor='middle' font-size='60' fill='#1a1410' " + AN + ">NOV 17-18</text>", 700, 140),
                                       "x": 0.5, "y": 0.225, "w": 0.42, "rotate": -3, "enter": "pop", "at": 1.6, "sfx": "pop"},
                                      {"type": "counter", "from": 0, "to": 15, "decimals": 0, "prefix": "UP TO ", "suffix": " AN HOUR", "x": 0.5, "y": 0.3,
                                       "size": 72, "color": "accent", "at": 2.6, "count_dur": 0.8, "enter": "pop", "sfx": "pop"}])})
# 7. close payoff that loops to the hook
S.append({"say": "So go on, make a wish. On a grain of *sand*.", "transition": "cut", "caption_y": 0.64,
          "layers": [plate("hill_up", blur=10, keys=[{"t": 0, "scale": 1.35}, {"t": 3.5, "scale": 1.42}]),
                     streak(0.85, 0.08, 0.35, 0.26, 0.3, 0.9, 0.5),
                     close_ved([["warm", 0], ["explain", 1.0], ["smirk", 2.2]]),
                     {"type": "image", "svg": GLOW, "x": 0.74, "y": 0.3, "w": 0.32, "at": 2.0, "enter": "pop"},
                     sprite("grain_hot", 0.74, 0.3, 0.1, at=2.0, enter="pop", sfx="ding", loop="pulse", loop_amp=0.05),
                     txt("WISH ON *SAND*", 0.18, 120, enter="pop", at=2.0)]})

job = {"id": ID, "title": "That shooting star? It was a grain of sand 🌠",
       "description": "Shooting stars aren't stars: most are crumbs of comet dust the size of a sand grain, hitting the air at up "
                      "to 71 km/s and making it glow ~100 km up. The Leonids peak on 17-18 November 2026 (up to ~15 an hour).\n\n"
                      "Sources: Britannica on meteors; NASA on meteors and meteorites; Space.com on the 2026 Leonids.",
       "tags": ["shooting stars", "meteors", "leonids", "leonid meteor shower", "meteor shower 2026", "space", "astronomy",
                "science explained"],
       "hashtags": ["#space", "#science"],
       "meta": {"format": "myth-bust", "topic": "shooting stars are sand-grain comet dust (speed, glow at ~100 km, Leonids 2026)",
                "hook": "myth-bust",
                "idea_source": "trending + viral: Leonids peak 17-18 Nov 2026 (Space.com); 'shooting stars are just sand' surprise",
                "characters": ["ved", "extra"],
                "sources": ["https://www.britannica.com/science/meteor/Introduction",
                            "https://solarsystem.nasa.gov/asteroids-comets-and-meteors/meteors-and-meteorites/in-depth.amp",
                            "https://www.space.com/leonid-meteor-shower"],
                "humour": {"trend": "'Remember November 2026' meme (revived on TikTok since late Aug 2026, peaking now it's November), "
                                    "as a side-eye + 'remember november 2026? it was sand' card",
                           "beat": "side_eye", "scene": 5},
                "claims": [
                    {"claim": "a typical visible meteor comes from a sand-grain-sized particle", "source": "https://www.britannica.com/science/meteor/Introduction"},
                    {"claim": "shower meteors are comet debris (Leonids: comet 55P/Tempel-Tuttle)", "source": "https://www.space.com/leonid-meteor-shower"},
                    {"claim": "Leonids enter at ~71 km/s; London-Paris ~344 km = ~5 s", "source": "https://www.space.com/leonid-meteor-shower"},
                    {"claim": "glow from heated, ionised air and vapour, starting ~100 km up", "source": "https://www.britannica.com/science/meteor/Introduction"},
                    {"claim": "nearest star ~40 trillion km (4.2 ly)", "source": "https://bigthink.com/strange-maps/voyager-1/"},
                    {"claim": "Leonids peak 17-18 Nov 2026, ZHR ~15", "source": "https://www.space.com/leonid-meteor-shower"}]},
       "thumbnail": {"title": "JUST *SAND?*", "title_y": 0.15, "title_size": 190, "max_w": 0.95, "blur": 14,
                     "glow": "#ffb35a", "glow_x": 0.5, "glow_y": 0.5, "glow_strength": 1.4, "bg_saturation": 1.5,
                     "tint": ["#1f4fb8", "#f08a24"], "tint_amount": 0.35,
                     "bg": [plate("hill_wide")],
                     "fg": [{"type": "image", "svg": STREAK, "x": 0.62, "y": 0.3, "w": 0.7, "rotate": -28, "enter": "none"},
                            {"type": "image", "svg": GLOW, "x": 0.8, "y": 0.5, "w": 0.42, "enter": "none"},
                            sprite("grain_hot", 0.8, 0.5, 0.2),
                            {"type": "character", "id": "ved", "pose": "surprised", "x": 0.45, "y": 0.93, "h": 0.95, "enter": "none",
                             "acting": "none", "talk": False, "ground": False, "allow_outside_safe": True}]},
       "privacy": "public", "speaker": "ved", "assets_script": J + "assets.py", "scenes": S}
json.dump(job, open(J + "job.json", "w"), indent=1, ensure_ascii=False)
print("scenes", len(S))
