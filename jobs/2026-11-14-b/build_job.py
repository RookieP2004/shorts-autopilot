"""2026-11-14-b: "He drank bacteria to win an argument" (wild-story). A 1984 Perth hospital lab and a stomach interior
(Blender stills + cut-outs), 2D panels: the old belief, the ammonia umbrella, 90% counter, honesty tags.
Run after the assets exist: python jobs/2026-11-14-b/build_job.py
"""
import json, os, sys
sys.path.insert(0, os.getcwd())
from autopilot.stage import Stage

ID = "2026-11-14-b"
J = f"jobs/{ID}/"
A = J + "assets/"
ST = {n: Stage(A + f"plate_{n}.json") for n in ("lab_wide", "lab_mid", "stomach_wide")}

OUT = {   # recurring people: same outfit in every shot
    "barry": {"skin": "#e2b48c", "build": "regular", "hair": ["#6b4a2a", "curly"], "top": ["#f6efe2", "jacket"],
              "bottom": ["#34425c", "trousers"], "shoes": "#25262b", "tie": "#6fc3c0"},
    "doc1": {"skin": "#d9a27a", "build": "round", "hair": ["#9aa0a8", "bald"], "top": ["#f6efe2", "jacket"],
             "bottom": ["#3a3e48", "trousers"], "shoes": "#25262b", "tie": "#7c2533"},
    "doc2": {"skin": "#8d5a3b", "build": "slim", "hair": ["#1a1410", "bun"], "top": ["#f6efe2", "jacket"],
             "bottom": ["#34425c", "skirt"], "shoes": "#25262b", "necklace": "#f2b04a"},
    "doc3": {"skin": "#c68a5e", "build": "regular", "hair": ["#2a2320", "short"], "hat": ["bowler", "#1a1410"],
             "top": ["#f6efe2", "jacket"], "bottom": ["#3a3e48", "trousers"], "shoes": "#25262b", "tie": "#34425c"},
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


def line_card(t, color="#1a1410", w=700, size=76):
    return card(f"<text x='{w/2}' y='{96 if size > 60 else 90}' text-anchor='middle' font-size='{size}' fill='{color}' {AN}>{t}</text>", w, 140)


def tag(word="PROVEN", color="#6fc3c0"):
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 300 84'><rect x='4' y='4' width='292' height='76' rx='38' "
            f"fill='{color}' stroke='#1a1410' stroke-width='5'/><circle cx='44' cy='42' r='16' fill='#1a1410'/>"
            f"<path d='M36,42 l6,7 l11,-14' stroke='{color}' stroke-width='5' fill='none'/>"
            f"<text x='172' y='60' text-anchor='middle' font-size='50' fill='#1a1410' {AN}>{word}</text></svg>")


def tag_layer(x, y, at, word="PROVEN", color="#6fc3c0"):
    return {"type": "image", "svg": tag(word, color), "x": x, "y": y, "w": 0.24, "enter": "pop", "at": at, "sfx": "click"}


def stamp(word, color="#d9534f", w=640):
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {w} 170'><rect x='10' y='10' width='{w-20}' height='150' rx='18' "
            f"fill='none' stroke='{color}' stroke-width='14'/><text x='{w/2}' y='124' text-anchor='middle' font-size='78' "
            f"fill='{color}' {AN}>{word}</text></svg>")


# the 1984 belief: stress + acid = ulcer
BELIEF = card(
    f"<text x='450' y='70' text-anchor='middle' font-size='48' fill='#34425c' {AN}>1984: WHAT CAUSES AN ULCER?</text>"
    # stress: a storm cloud
    "<g transform='translate(150,175)'><ellipse cx='0' cy='0' rx='70' ry='42' fill='#9aa0a8' stroke='#1a1410' stroke-width='5'/>"
    "<ellipse cx='-40' cy='10' rx='40' ry='30' fill='#9aa0a8' stroke='#1a1410' stroke-width='5'/>"
    "<path d='M-6,30 l-18,40 l20,-6 l-12,36' stroke='#f2b04a' stroke-width='9' fill='none' stroke-linejoin='round'/></g>"
    f"<text x='150' y='300' text-anchor='middle' font-size='46' fill='#1a1410' {AN}>STRESS</text>"
    f"<text x='300' y='200' text-anchor='middle' font-size='90' fill='#1a1410' {AN}>+</text>"
    # acid: a drop
    "<path d='M450,115 C490,175 510,200 510,225 C510,262 482,282 450,282 C418,282 390,262 390,225 C390,200 410,175 450,115 Z' "
    "fill='#c9e04a' stroke='#1a1410' stroke-width='5'/>"
    f"<text x='450' y='300' text-anchor='middle' font-size='46' fill='#1a1410' {AN}>ACID</text>"
    f"<text x='590' y='200' text-anchor='middle' font-size='90' fill='#1a1410' {AN}>=</text>"
    # a sore stomach
    "<path d='M700,120 C780,110 820,160 800,210 C780,265 720,290 690,250 C670,222 700,200 690,175 C680,150 660,125 700,120 Z' "
    "fill='#e8848c' stroke='#1a1410' stroke-width='5'/><circle cx='745' cy='200' r='16' fill='#d9534f' stroke='#1a1410' stroke-width='4'/>"
    f"<text x='745' y='300' text-anchor='middle' font-size='46' fill='#1a1410' {AN}>ULCER</text>", 900, 340)

# ammonia umbrella: the bug makes ammonia (urease) that neutralises the acid right around it
UMBRELLA = card(
    f"<text x='450' y='66' text-anchor='middle' font-size='46' fill='#34425c' {AN}>HOW IT SURVIVES THE ACID</text>"
    # acid drops falling
    "<g fill='#c9e04a' stroke='#1a1410' stroke-width='4'>"
    "<path d='M220,95 c12,18 18,26 18,34 a18,18 0 0 1 -36,0 c0,-8 6,-16 18,-34z'/>"
    "<path d='M350,85 c12,18 18,26 18,34 a18,18 0 0 1 -36,0 c0,-8 6,-16 18,-34z'/>"
    "<path d='M560,90 c12,18 18,26 18,34 a18,18 0 0 1 -36,0 c0,-8 6,-16 18,-34z'/>"
    "<path d='M690,95 c12,18 18,26 18,34 a18,18 0 0 1 -36,0 c0,-8 6,-16 18,-34z'/></g>"
    # umbrella = an ammonia cloud
    "<path d='M210,250 C220,160 330,135 450,135 C570,135 680,160 690,250 C650,232 610,232 570,250 C530,232 490,232 450,250 "
    "C410,232 370,232 330,250 C290,232 250,232 210,250 Z' fill='#6fc3c0' stroke='#1a1410' stroke-width='6'/>"
    f"<text x='450' y='215' text-anchor='middle' font-size='44' fill='#1a1410' {AN}>AMMONIA (NH3)</text>"
    "<line x1='450' y1='250' x2='450' y2='330' stroke='#1a1410' stroke-width='6'/>"
    # the corkscrew bug
    "<path d='M330,350 c20,-30 40,30 60,0 c20,-30 40,30 60,0 c20,-30 40,30 60,0 c20,-30 40,30 60,0' stroke='#7cc35a' "
    "stroke-width='22' fill='none' stroke-linecap='round'/>"
    "<path d='M570,350 c25,-10 45,10 70,-5 M570,350 c25,5 45,25 70,15' stroke='#4f8f3a' stroke-width='6' fill='none'/>"
    f"<text x='450' y='420' text-anchor='middle' font-size='40' fill='#34425c' {F}>it neutralises the acid around itself</text>", 900, 450)

DAY3 = line_card("DAY 3: NAUSEA", "#1a1410")
DAY8 = line_card("DAY 8: INFLAMED", "#d9534f", 900, 84)

S = []
# 0. hook (lab mid): Barry raises the beaker, the headline at frame 0
S.append({"say": "This doctor drank a glass of *bacteria*. On purpose.", "caption_y": 0.34,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.0, "zoom": 1.07, "focus": [0.5, 0.52]}]},
          "layers": staged("lab_mid",
                           people=[person("lab_mid", "barry", -1.0, -0.4, [["hold", 0], ["cheer", 2.6]]),
                                   ved("lab_mid", -0.3, -1.5, [["point", 0], ["surprised", 2.6]])],
                           extra_top=[txt("HE DRANK *BACTERIA*", 0.13, 118, enter="none"),
                                      {"type": "image", "svg": line_card("PERTH, 1984"), "x": 0.5, "y": 0.235, "w": 0.46, "rotate": -3,
                                       "enter": "none"},
                                      sprite("beaker", 0.345, 0.575, 0.1, enter="none")])})
# 1. lab wide: what every doctor "knew"
S.append({"say": "In 1984, ulcers were blamed on *stress and acid*.",
          "transition": "slide_left", "caption_y": 0.44,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.6, "zoom": 1.05, "focus": [0.5, 0.5]}]},
          "layers": staged("lab_wide",
                           people=[person("lab_wide", "doc1", -1.3, -2.6, [["explain", 0], ["point", 1.6]]),
                                   person("lab_wide", "doc2", -0.6, -1.6, [["idle", 0], ["explain", 1.2]]),
                                   person("lab_wide", "doc3", 0.1, -2.4, [["explain", 0], ["shrug", 2.0]]),
                                   person("lab_wide", "barry", 0.75, -3.6, [["idle", 0], ["shrug", 2.4]])],
                           extra_top=[{"type": "image", "svg": BELIEF, "x": 0.5, "y": 0.205, "w": 0.86, "enter": "slide_down", "at": 0.1, "sfx": "pop"},
                                      {"type": "image", "svg": stamp("EVERYONE KNEW", w=760), "x": 0.6, "y": 0.335, "w": 0.5, "rotate": -8,
                                       "enter": "zoom", "at": 1.9, "sfx": "boom"}])})
# 2. stomach wide: the spiral bug, Ved walks in on the folds
S.append({"say": "But Marshall and Warren kept finding one *spiral bug* in ulcer patients.",
          "transition": "zoom", "caption_y": 0.46,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.8, "zoom": 1.08, "focus": [0.5, 0.55]}]},
          "layers": staged("stomach_wide",
                           people=[ved("stomach_wide", 0.3, -1.0, [["welcome", 0], ["point", 2.4], ["surprised", 3.8]],
                                       walk=[(0, 3.0, -1.4), (1.2, 0.3, -1.0)])],
                           extra_top=[txt("H. *PYLORI*", 0.12, 130, enter="pop", at=0.3, sfx="pop"),
                                      sprite("bug", 0.5, 0.235, 0.52, at=0.9, enter="zoom", sfx="whoosh", loop="wiggle", loop_amp=0.02),
                                      tag_layer(0.5, 0.33, 2.6)])})
# 3. lab wide: nobody believed them
S.append({"say": "*Nobody* believed them.",
          "transition": "cut", "caption_y": 0.44,
          "camera": {"keys": [{"t": 0, "zoom": 1.06, "focus": [0.5, 0.52]}, {"t": 1.6, "zoom": 1.12, "focus": [0.55, 0.55]}]},
          "layers": staged("lab_wide",
                           people=[person("lab_wide", "doc1", -1.3, -2.6, [["shrug", 0]]),
                                   person("lab_wide", "doc2", -0.6, -1.6, [["wave", 0]]),
                                   person("lab_wide", "doc3", 0.1, -2.4, [["shrug", 0]]),
                                   person("lab_wide", "barry", 0.75, -3.6, [["sad", 0]])],
                           extra_top=[txt("*NOPE.*", 0.16, 170, enter="pop", at=0.15, sfx="pop")])})
# 4. comic beat: side-eye cut-away, "What's up brah?" (calm vs odds you can't beat)
S.append({"dur": 1.5, "transition": "cut", "captions": False,
          "layers": [plate("lab_mid", blur=10, keys=[{"t": 0, "scale": 1.35}]), dict(close_ved([["side_eye", 0]]), acting="none")],
          "beat": {"kind": "side_eye", "at": 0.1, "dur": 1.35, "who": "ved",
                   "text": "the whole medical world vs one guy:\n*what's up brah?*", "text_y": 0.2}})
# 5. lab mid: so he drank it; day 3
S.append({"say": "So he drank it. Day three: *nausea*.",
          "transition": "slide_left", "caption_y": 0.355,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.0, "zoom": 1.1, "focus": [0.4, 0.5]}]},
          "layers": staged("lab_mid",
                           people=[person("lab_mid", "barry", -1.0, -0.4, [["hold", 0], ["sad", 1.9]]),
                                   ved("lab_mid", -0.3, -1.5, [["explain", 0], ["serious", 1.8]])],
                           extra_top=[sprite("beaker", 0.345, 0.575, 0.1, enter="none",
                                             keys=[{"t": 0, "x": 0.345, "y": 0.575, "rot": 0}, {"t": 0.5, "x": 0.35, "y": 0.49, "rot": -70},
                                                   {"t": 1.2, "x": 0.35, "y": 0.49, "rot": -70}, {"t": 1.5, "x": 0.345, "y": 0.575, "rot": 0}]),
                                      txt("*GULP.*", 0.15, 150, enter="pop", at=0.5, sfx="pop"),
                                      {"type": "image", "svg": DAY3, "x": 0.5, "y": 0.255, "w": 0.6, "rotate": -3, "enter": "pop", "at": 1.5, "sfx": "pop"}])})
# 6. stomach close: day 8, inflamed lining
S.append({"say": "Day eight: an *inflamed* stomach.",
          "transition": "zoom", "caption_y": 0.46,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 2.6, "zoom": 1.1, "focus": [0.5, 0.55]}]},
          "layers": [plate("stomach_close"),
                     {"type": "shape", "shape": "rect", "x": 0.5, "y": 0.5, "w": 1.0, "h": 1.78, "color": "#d9534f", "opacity": 0.0,
                      "enter": "none", "keys": [{"t": 0, "opacity": 0.0}, {"t": 0.8, "opacity": 0.34}, {"t": 1.4, "opacity": 0.22}, {"t": 2.0, "opacity": 0.34}]},
                     {"type": "image", "svg": DAY8, "x": 0.5, "y": 0.16, "w": 0.86, "rotate": 2, "enter": "pop", "at": 0.2, "sfx": "boom"},
                     tag_layer(0.5, 0.26, 1.2)]})
# 7. stomach wide + panel: the ammonia umbrella
S.append({"say": "It survives by brewing *ammonia*, a chemical umbrella.",
          "transition": "slide_up", "caption_y": 0.6,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.0, "zoom": 1.05, "focus": [0.5, 0.45]}]},
          "layers": [plate("stomach_wide", blur=10),
                     {"type": "image", "svg": UMBRELLA, "x": 0.5, "y": 0.25, "w": 0.88, "enter": "slide_down", "at": 0.1, "sfx": "whoosh"},
                     tag_layer(0.5, 0.74, 2.4),
                     sprite("bug", 0.5, 0.49, 0.34, at=0.8, enter="pop", sfx="pop", loop="wiggle", loop_amp=0.03)]})
# 8. lab wide: today: 90% of duodenal ulcers, cured with antibiotics; the town cheers
S.append({"say": "It causes over ninety percent of duodenal ulcers, cured with *antibiotics*.",
          "caption": "It causes over *90%* of duodenal ulcers, cured with *antibiotics*.",
          "transition": "slide_left", "caption_y": 0.44,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.5, "zoom": 1.06, "focus": [0.55, 0.55]}]},
          "layers": staged("lab_wide",
                           people=[person("lab_wide", "doc1", -1.3, -2.6, [["idle", 0], ["surprised", 1.2], ["happy", 3.0]]),
                                   person("lab_wide", "doc2", -0.6, -1.6, [["idle", 0], ["cheer", 2.2]], hops=[[2.3, 0.05, 0.4]]),
                                   person("lab_wide", "doc3", 0.1, -2.4, [["idle", 0], ["happy", 2.6]]),
                                   person("lab_wide", "barry", 0.75, -3.6, [["idle", 0], ["cheer", 1.4]], hops=[[1.5, 0.07, 0.45]])],
                           extra_top=[{"type": "counter", "from": 0, "to": 90, "decimals": 0, "prefix": "OVER ", "suffix": "%", "x": 0.5, "y": 0.13,
                                       "size": 140, "color": "accent", "at": 0.2, "count_dur": 1.3, "enter": "none", "stroke": "#0b0f12", "stroke_width": 8},
                                      txt("OF DUODENAL ULCERS", 0.215, 74, enter="pop", at=1.2, sfx="pop"),
                                      tag_layer(0.5, 0.29, 2.0)])})
# 9. close payoff: Nobel 2005, loops back to the drink
S.append({"say": "Then, a Nobel Prize. Sometimes you win by *drinking the evidence*.",
          "transition": "cut", "caption_y": 0.64,
          "layers": [plate("lab_mid", blur=10, keys=[{"t": 0, "scale": 1.35}, {"t": 4.5, "scale": 1.42}]),
                     close_ved([["warm", 0], ["explain", 1.6], ["smirk", 3.6]]),
                     sprite("medal", 0.74, 0.3, 0.2, at=0.1, enter="drop", sfx="ding"),
                     txt("NOBEL, *2005*", 0.12, 130, enter="pop", at=0.1)]})


job = {"id": ID, "title": "He drank bacteria to win an argument 🦠",
       "description": "In 1984, Australian doctor Barry Marshall drank a broth of Helicobacter pylori to prove that a bacterium, not "
                      "stress, causes stomach ulcers. Within days he had nausea and, by day eight, an inflamed stomach. He and Robin "
                      "Warren won the 2005 Nobel Prize; ulcers became curable with antibiotics. (A story, not medical advice.)\n\n"
                      "Sources: Nobel Assembly 2005 announcement (via Al Jazeera); Britannica 'Barry J. Marshall'; Wikipedia 'Barry Marshall'.",
       "tags": ["barry marshall", "helicobacter pylori", "h pylori", "stomach ulcer", "nobel prize", "self experiment",
                "history of medicine", "science story", "explained"],
       "hashtags": ["#science", "#history"],
       "meta": {"format": "wild-story",
                "topic": "Barry Marshall drank H. pylori (1984) to prove bacteria, not stress, cause ulcers; ammonia shield; 90% of duodenal ulcers; Nobel 2005",
                "hook": "story",
                "idea_source": "viral-shaped (crazy true self-experiment, one sentence hook) + unique (first wild-story on the channel; few Shorts tell it with the acid-survival mechanism)",
                "characters": ["ved", "extra"],
                "sources": ["https://en.wikipedia.org/wiki/Barry_Marshall",
                            "https://www.britannica.com/EBchecked/topic/366546/Barry-J-Marshall",
                            "https://www.aljazeera.com/amp/news/2005/10/4/australians-win-nobel-for-medicine",
                            "https://www.jove.com/science-education/v/40832/peptic-ulcer"],
                "humour": {"trend": "'What's up brah?' (calm face-off vs odds you can't beat; Nov 2026) bent into 'the whole medical world vs one guy'; side-eye cut-away",
                           "beat": "side_eye", "scene": 4},
                "claims": [
                    {"claim": "Marshall drank a culture of H. pylori in 1984", "tag": "PROVEN", "source": "https://en.wikipedia.org/wiki/Barry_Marshall"},
                    {"claim": "ulcers were blamed mainly on stress, spicy food and excess acid", "tag": "PROVEN",
                     "source": "https://www.britannica.com/EBchecked/topic/366546/Barry-J-Marshall"},
                    {"claim": "Marshall and Warren found the bacterium in almost all ulcer/gastritis patients (100-patient study)", "tag": "PROVEN",
                     "source": "https://www.britannica.com/EBchecked/topic/366546/Barry-J-Marshall"},
                    {"claim": "day 3 nausea, day 8 endoscopy showed massive inflammation (gastritis)", "tag": "PROVEN",
                     "source": "https://en.wikipedia.org/wiki/Barry_Marshall"},
                    {"claim": "H. pylori survives acid by making ammonia (urease) that neutralises acid around it", "tag": "PROVEN",
                     "source": "https://www.jove.com/science-education/v/40832/peptic-ulcer"},
                    {"claim": "causes more than 90% of duodenal ulcers; curable with antibiotics + acid inhibitors", "tag": "PROVEN",
                     "source": "https://www.aljazeera.com/amp/news/2005/10/4/australians-win-nobel-for-medicine"},
                    {"claim": "Nobel Prize 2005, with Robin Warren", "tag": "PROVEN", "source": "https://en.wikipedia.org/wiki/Barry_Marshall"}]},
       "thumbnail": {"title": "HE DRANK *IT?*", "title_y": 0.15, "title_size": 190, "max_w": 0.95, "blur": 14,
                     "glow": "#ffcf5a", "glow_x": 0.5, "glow_y": 0.55, "glow_strength": 1.4, "bg_saturation": 1.5,
                     "tint": ["#1f8f6a", "#f08a24"], "tint_amount": 0.35,
                     "bg": [plate("lab_wide")],
                     "fg": [sprite("beaker", 0.8, 0.55, 0.2), sprite("bug", 0.2, 0.36, 0.3),
                            {"type": "character", "id": "ved", "pose": "surprised", "x": 0.45, "y": 0.93, "h": 0.95, "enter": "none",
                             "acting": "none", "talk": False, "ground": False, "allow_outside_safe": True}]},
       "privacy": "public", "speaker": "ved", "assets_script": J + "assets.py", "scenes": S}
for sc in S:
    if "say" in sc:
        sc.setdefault("pad", 0.14); sc.setdefault("lead", 0.06)
json.dump(job, open(J + "job.json", "w"), indent=1, ensure_ascii=False)
print("scenes", len(S))
