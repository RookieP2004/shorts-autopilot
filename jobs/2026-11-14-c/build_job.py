"""2026-11-14-c: \"$1 a second: when are you a trillionaire?\" (scale-shock). Town square with a clock tower and a coin jar (Blender stills + cut-outs), 2D panels: cave art, bars to scale.\nRun after the assets exist: python jobs/2026-11-14-c/build_job.py\n"""
import json, os, sys
sys.path.insert(0, os.getcwd())
from autopilot.stage import Stage

ID = "2026-11-14-c"
J = f"jobs/{ID}/"
A = J + "assets/"
ST = {n: Stage(A + f"plate_{n}.json") for n in ("square_wide", "square_mid")}

OUT = {   # recurring townspeople: same outfit in every shot
    "rosa": {"skin": "#c68a5e", "build": "round", "hair": ["#1a1410", "bun"], "hat": ["headscarf", "#d9534f"],
             "top": ["#f2b04a", "dress"], "bottom": ["#34425c", "trousers"], "shoes": "#25262b", "apron": "#f6efe2", "earrings": "#f2b04a"},
    "theo": {"skin": "#8d5a3b", "build": "slim", "hair": ["#1a1410", "short"], "hat": ["bowler", "#1a1410"],
             "top": ["#34425c", "jacket"], "bottom": ["#3a3e48", "trousers"], "shoes": "#25262b", "tie": "#7c2533", "bag": "#8a5a3c"},
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




def drop_coin(x, y0, y1, at, w=0.07, until=None):
    L = sprite("coin", x, y0, w, at=at, enter="fade", sfx="pop" if at < 0.05 else None,
               keys=[{"t": 0, "x": x, "y": y0, "rot": 0}, {"t": 0.45, "x": x, "y": y1, "rot": 200, "ease": "in"}],
               until=until or at + 0.5, exit="fade")
    if L.get("sfx") is None:
        L.pop("sfx")
    return L


def coin_rain(x, y0, y1, start, end, every=1.0, w=0.07):
    out, t = [], start
    while t < end:
        out.append(drop_coin(x, y0, y1, t, w)); t += every
    return out


def big_card(lines, w=900, h=260):
    return card(lines, w, h)


# $1 a second sign + question
HOOK_CARD = card("<text x='450' y='108' text-anchor='middle' font-size='92' fill='#1a1410' " + AN + ">$1 EVERY SECOND</text>", 900, 150)


def stat_card(amount, time_txt, color="#d9534f"):
    return card(f"<text x='450' y='92' text-anchor='middle' font-size='70' fill='#1a1410' {AN}>{amount}</text>"
                f"<line x1='120' y1='120' x2='780' y2='120' stroke='#1a1410' stroke-width='4' stroke-dasharray='12 10'/>"
                f"<text x='450' y='215' text-anchor='middle' font-size='86' fill='{color}' {AN}>{time_txt}</text>", 900, 250)


# calendar pages
def cal(page):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 220'><rect x='6' y='16' width='188' height='198' rx='16' fill='#f6efe2' stroke='#1a1410' stroke-width='6'/>"
            "<rect x='6' y='16' width='188' height='54' rx='16' fill='#d9534f' stroke='#1a1410' stroke-width='6'/>"
            "<circle cx='55' cy='16' r='9' fill='#1a1410'/><circle cx='145' cy='16' r='9' fill='#1a1410'/>"
            f"<text x='100' y='170' text-anchor='middle' font-size='92' fill='#1a1410' {AN}>{page}</text></svg>")


def fly_cal(page, x, y, at, dx, dy, rot):
    return {"type": "image", "svg": cal(page), "x": x, "y": y, "w": 0.2, "at": at, "enter": "pop", "until": at + 1.1, "exit": "fade",
            "keys": [{"t": 0, "x": x, "y": y, "rot": 0}, {"t": 0.35, "x": x, "y": y, "rot": 0},
                     {"t": 1.1, "x": x + dx, "y": y + dy, "rot": rot, "ease": "in"}]}


# cave wall: ochre mammoth and hands, 30,000+ years ago
CAVE = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 900 560'>"
        "<rect x='5' y='5' width='890' height='550' rx='34' fill='#8a6142' stroke='#1a1410' stroke-width='6'/>"
        "<path d='M40,80 C200,40 380,90 520,60 C680,30 800,70 860,60 L860,520 C700,540 500,500 300,530 C180,545 90,520 40,520 Z' fill='#b98a5e'/>"
        "<path d='M40,300 C160,280 260,330 420,300 M500,420 C620,400 760,440 860,410' stroke='#9c7148' stroke-width='6' fill='none'/>"
        # mammoth: a filled charcoal silhouette (domed head, hump, sloping back, trunk, curved tusk, hairy belly)
        "<path d='M235,420 C228,360 236,300 262,262 C300,206 370,182 430,196 C470,160 548,150 600,182 C650,212 668,262 660,312 "
        "C690,340 700,390 690,450 C686,470 668,472 666,452 C670,410 660,380 640,360 C632,380 626,420 628,460 L596,462 "
        "C594,420 590,392 584,380 C560,392 520,396 500,392 L498,462 L466,462 L462,396 C420,398 360,396 330,388 L326,462 L294,462 "
        "C292,430 286,410 276,398 L270,462 L240,462 Z' fill='#3a2414'/>"
        "<path d='M640,300 C700,330 720,380 690,420' stroke='#efe3c8' stroke-width='10' fill='none' stroke-linecap='round'/>"
        "<circle cx='600' cy='240' r='7' fill='#b98a5e'/>"
        "<path d='M260,240 C300,200 380,190 460,200' stroke='#a2402a' stroke-width='9' fill='none' stroke-dasharray='4 14' stroke-linecap='round'/>"
        # hand stencils
        "<g fill='#a2402a' opacity='0.85'><ellipse cx='130' cy='190' rx='34' ry='40'/><rect x='104' y='120' width='12' height='45' rx='6'/>"
        "<rect x='121' y='110' width='12' height='50' rx='6'/><rect x='138' y='115' width='12' height='48' rx='6'/><rect x='154' y='130' width='11' height='40' rx='6'/>"
        "<rect x='86' y='185' width='30' height='12' rx='6' transform='rotate(-30 100 190)'/></g>"
        f"<text x='450' y='520' text-anchor='middle' font-size='52' fill='#f6efe2' {AN}>CAVE ART, 30,000+ YEARS AGO</text></svg>")

# the bars: million vs billion vs trillion, to scale
BARS = card(
    f"<text x='450' y='70' text-anchor='middle' font-size='52' fill='#1a1410' {AN}>DRAWN TO SCALE</text>"
    f"<text x='60' y='150' font-size='40' fill='#1a1410' {AN}>MILLION</text>"
    "<rect x='290' y='118' width='1.5' height='40' fill='#6fc3c0'/>"
    f"<text x='310' y='150' font-size='30' fill='#34425c' {F}>(invisible)</text>"
    f"<text x='60' y='240' font-size='40' fill='#1a1410' {AN}>BILLION</text>"
    "<rect x='290' y='208' width='4' height='40' fill='#f2b04a' stroke='#1a1410' stroke-width='1'/>"
    f"<text x='310' y='240' font-size='30' fill='#34425c' {F}>(a sliver)</text>"
    f"<text x='60' y='330' font-size='40' fill='#1a1410' {AN}>TRILLION</text>", 900, 380)
TRILL_BAR = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 560 44'><rect x='2' y='2' width='556' height='40' rx='6' fill='#d9534f' stroke='#1a1410' stroke-width='4'/></svg>")

S = []
# 0. hook (square mid): coins drop into the jar, the question at frame 0
S.append({"say": "One dollar every second, nonstop. When are you a *trillionaire*?",
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.2, "zoom": 1.07, "focus": [0.52, 0.52]}]},
          "layers": staged("square_mid",
                           people=[person("square_mid", "theo", -0.2, 0.0, [["idle", 0], ["surprised", 2.6]]),
                                   ved("square_mid", -1.0, -1.0, [["explain", 0], ["point", 1.6], ["think", 2.9]])],
                           extra_top=coin_rain(0.72, 0.3, 0.48, 0.0, 4.5, 1.0, 0.06) + [
                               {"type": "image", "svg": HOOK_CARD, "x": 0.5, "y": 0.13, "w": 0.78, "rotate": -2, "enter": "none"},
                               txt("TRILLIONAIRE *WHEN?*", 0.24, 118, enter="none")])})
# 1. square wide: a million in 11.6 days, Rosa cheers
S.append({"say": "A million dollars? Just under *twelve days*.",
          "transition": "slide_left", "caption_y": 0.44,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.0, "zoom": 1.05, "focus": [0.5, 0.5]}]},
          "layers": staged("square_wide",
                           people=[person("square_wide", "rosa", -2.2, -1.2, [["idle", 0], ["cheer", 1.6]], hops=[[1.7, 0.05, 0.4]]),
                                   person("square_wide", "theo", 2.4, -0.4, [["idle", 0], ["happy", 1.8]]),
                                   ved("square_wide", -0.4, -2.4, [["welcome", 0], ["point", 1.4]], walk=[(0, -3.5, -2.6), (1.0, -0.4, -2.4)])],
                           extra_top=[{"type": "counter", "from": 0, "to": 1000000, "decimals": 0, "prefix": "$", "x": 0.5, "y": 0.14,
                                       "size": 120, "color": "accent", "at": 0.0, "count_dur": 1.2, "enter": "none", "stroke": "#0b0f12", "stroke_width": 7},
                                      {"type": "image", "svg": card(f"<text x='350' y='96' text-anchor='middle' font-size='76' fill='#d9534f' {AN}>11.6 DAYS</text>", 700, 140),
                                       "x": 0.5, "y": 0.25, "w": 0.5, "rotate": -3, "enter": "pop", "at": 1.3, "sfx": "pop"}])})
# 2. clock up: a billion = 31.7 years; calendar pages fly off
S.append({"say": "A billion? *Thirty-two years*.",
          "transition": "slide_up", "caption_y": 0.66,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 2.6, "zoom": 1.08, "focus": [0.5, 0.47]}]},
          "layers": [plate("clock_up"),
                     {"type": "counter", "from": 1000000, "to": 1000000000, "decimals": 0, "prefix": "$", "x": 0.5, "y": 0.13,
                      "size": 100, "color": "accent", "at": 0.0, "count_dur": 1.1, "enter": "none", "stroke": "#0b0f12", "stroke_width": 7},
                     fly_cal("1995", 0.22, 0.27, 0.3, -0.25, 0.25, -40), fly_cal("2010", 0.78, 0.25, 0.6, 0.25, 0.25, 40),
                     fly_cal("2026", 0.25, 0.3, 0.9, -0.3, 0.2, -30),
                     {"type": "image", "svg": card(f"<text x='350' y='96' text-anchor='middle' font-size='76' fill='#d9534f' {AN}>31.7 YEARS</text>", 700, 140),
                      "x": 0.5, "y": 0.235, "w": 0.52, "rotate": 3, "enter": "pop", "at": 1.0, "sfx": "pop"}]})
# 3. square wide: a trillion = 31,700 years; the town is stunned
S.append({"say": "A trillion? About *thirty-one thousand, seven hundred years*.", "caption": "A trillion? About *31,700 years*.",
          "transition": "zoom", "caption_y": 0.44,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.0, "zoom": 1.08, "focus": [0.5, 0.52]}]},
          "layers": staged("square_wide",
                           people=[person("square_wide", "rosa", -2.2, -1.2, [["happy", 0], ["surprised", 1.2], ["sad", 2.6]]),
                                   person("square_wide", "theo", 2.4, -0.4, [["idle", 0], ["shrug", 1.4], ["sad", 2.8]]),
                                   ved("square_wide", -0.4, -2.4, [["serious", 0], ["surprised", 1.2]], hops=[[1.2, 0.06, 0.45]])],
                           extra_top=[{"type": "counter", "from": 0, "to": 31700, "decimals": 0, "suffix": " YEARS", "x": 0.5, "y": 0.16,
                                       "size": 130, "color": "danger", "at": 0.3, "count_dur": 1.6, "enter": "zoom", "sfx": "riser", "stroke": "#0b0f12", "stroke_width": 8},
                                      txt("FOR *$1,000,000,000,000*", 0.25, 78, enter="pop", at=1.8, sfx="boom")])})
# 4. cave wall infographic over the blurred clock
S.append({"say": "To finish today, you'd have started when people painted *mammoths* in caves.",
          "transition": "slide_left", "caption_y": 0.6,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.5, "zoom": 1.05, "focus": [0.5, 0.45]}]},
          "layers": [plate("clock_up", blur=12),
                     {"type": "image", "svg": CAVE, "x": 0.5, "y": 0.27, "w": 0.86, "enter": "slide_up", "at": 0.15, "sfx": "whoosh"},
                     {"type": "image", "svg": card(f"<text x='300' y='88' text-anchor='middle' font-size='58' fill='#1a1410' {AN}>START: ~29,700 BC</text>", 600, 130),
                      "x": 0.5, "y": 0.73, "w": 0.6, "rotate": -2, "enter": "pop", "at": 2.2, "sfx": "pop"}]})
# 5. comic beat: deadpan close-up, "trillionaire arc" card
S.append({"dur": 1.6, "transition": "cut", "captions": False,
          "layers": [plate("square_mid", blur=10, keys=[{"t": 0, "scale": 1.35}]), dict(close_ved([["deadpan", 0]]), acting="none")],
          "beat": {"kind": "deadpan", "at": 0.1, "dur": 1.45, "who": "ved",
                   "text": "my trillionaire *arc*\nETA: year 33,700", "text_y": 0.2}})
# 6. square mid: why: thousand millions, thousand billions (bars to scale)
S.append({"say": "A billion is a thousand millions. A trillion? A thousand *billions*.",
          "transition": "slide_left", "caption_y": 0.44,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 5.0, "zoom": 1.05, "focus": [0.5, 0.5]}]},
          "layers": staged("square_mid",
                           people=[person("square_mid", "theo", -0.2, 0.0, [["explain", 0], ["point", 2.5]]),
                                   ved("square_mid", -1.0, -1.0, [["explain", 0], ["point", 2.6]])],
                           extra_top=[{"type": "image", "svg": BARS, "x": 0.5, "y": 0.2, "w": 0.86, "enter": "slide_down", "at": 0.1, "sfx": "pop"},
                                      {"type": "image", "svg": TRILL_BAR, "x": 0.614, "y": 0.269, "w": 0.535, "enter": "none", "at": 2.6, "sfx": "whoosh",
                                       "keys": [{"t": 0, "x": 0.347, "sx": 0.0}, {"t": 1.0, "x": 0.614, "sx": 1.0, "ease": "linear"}]}])})
# 7. square wide: yet more than a dozen companies are worth over a trillion
S.append({"say": "Yet more than a dozen companies are now worth over a *trillion*.",
          "transition": "slide_left", "caption_y": 0.44,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.6, "zoom": 1.06, "focus": [0.55, 0.55]}]},
          "layers": staged("square_wide",
                           people=[person("square_wide", "rosa", -2.2, -1.2, [["sad", 0], ["surprised", 1.4]]),
                                   person("square_wide", "theo", 2.4, -0.4, [["idle", 0], ["surprised", 1.5]], hops=[[1.6, 0.04, 0.4]]),
                                   ved("square_wide", -0.4, -2.4, [["explain", 0], ["point", 1.6]])],
                           extra_top=[sprite("coin_pile", 0.5, 0.235, 0.3, at=0.4, enter="drop", sfx="boom"),
                                      txt("12+ COMPANIES", 0.12, 110, enter="pop", at=0.2, sfx="pop"),
                                      {"type": "image", "svg": card(f"<text x='350' y='94' text-anchor='middle' font-size='68' fill='#d9534f' {AN}>WORTH $1T+</text>", 700, 140),
                                       "x": 0.5, "y": 0.335, "w": 0.5, "rotate": -3, "enter": "pop", "at": 1.7, "sfx": "pop"}])})
# 8. close payoff, loops to the hook
S.append({"say": "So keep collecting. See you in the year *thirty-three thousand, seven hundred*.", "caption": "So keep collecting. See you in the year *33,700*.", "transition": "cut", "caption_y": 0.64,
          "layers": [plate("square_mid", blur=10, keys=[{"t": 0, "scale": 1.35}, {"t": 4.0, "scale": 1.42}]),
                     close_ved([["warm", 0], ["explain", 1.2], ["smirk", 3.0]]),
                     sprite("coin", 0.76, 0.3, 0.14, at=2.6, enter="pop", sfx="ding", loop="pulse", loop_amp=0.05),
                     txt("YEAR *33,700*", 0.17, 130, enter="pop", at=2.6)]})


job = {"id": ID, "title": "$1 a second: when are you a trillionaire? 💸",
       "description": "Earn one dollar every second, nonstop: a million takes 11.6 days, a billion 31.7 years, and a trillion about "
                      "31,700 years, so you'd have had to start back when people painted mammoths on cave walls. A billion is a "
                      "thousand millions; a trillion is a thousand billions.\n\n"
                      "Sources: unit arithmetic (1 year = 31,557,600 s); Chauvet Cave art dating (French Ministry of Culture); "
                      "trillion-dollar companies count (Jon Erlichman via OfficeChai, 2026).",
       "tags": ["how big is a trillion", "trillion", "billion vs trillion", "million billion trillion", "money", "economics",
                "big numbers", "personal finance", "explained"],
       "hashtags": ["#money", "#economics"],
       "meta": {"format": "scale-shock", "topic": "how big is a trillion: $1 a second = millionaire in 11.6 days, billionaire in 31.7 years, trillionaire in ~31,700 years (cave-art era)",
                "hook": "question",
                "idea_source": "backlog (ideas.md 'How big is a trillion? money version') + viral-shaped (huge numbers made feelable, wallet framing) + trending (trillion-dollar companies)",
                "characters": ["ved", "extra"],
                "sources": ["https://simple.wikipedia.org/wiki/Orders_of_magnitude_(time)",
                            "https://archeologie.culture.gouv.fr/chauvet/en/aurignacian-cave-art",
                            "https://www.britannica.com/place/Chauvet-Pont-dArc/Artists-of-the-cave",
                            "https://officechai.com/stories/from-having-no-trillion-dollar-companies-in-2017-there-are-now-17-in-2026/"],
                "humour": {"trend": "'___ arc' slang (my villain/era arc) bent into 'my trillionaire arc: ETA year 33,700'; dry deadpan close-up",
                           "beat": "deadpan", "scene": 5},
                "claims": [
                    {"claim": "1,000,000 s = 11.57 days", "tag": "PROVEN", "source": "arithmetic"},
                    {"claim": "1,000,000,000 s = 31.7 years", "tag": "PROVEN", "source": "arithmetic (365.25-day year)"},
                    {"claim": "1,000,000,000,000 s = ~31,700 years (start ~29,700 BC to finish 2026)", "tag": "PROVEN", "source": "arithmetic"},
                    {"claim": "people painted mammoths on cave walls 30,000+ years ago (Chauvet: ~36,000 and ~31,000 years ago)", "tag": "PROVEN",
                     "source": "https://archeologie.culture.gouv.fr/chauvet/en/aurignacian-cave-art"},
                    {"claim": "more than a dozen companies worth over $1 trillion in 2026 (17 per Erlichman)", "tag": "PROVEN",
                     "source": "https://officechai.com/stories/from-having-no-trillion-dollar-companies-in-2017-there-are-now-17-in-2026/"}]},
       "thumbnail": {"title": "31,700 *YEARS?*", "title_y": 0.15, "title_size": 170, "max_w": 0.95, "blur": 14,
                     "glow": "#ffcf5a", "glow_x": 0.5, "glow_y": 0.55, "glow_strength": 1.4, "bg_saturation": 1.5,
                     "tint": ["#1f4fb8", "#f08a24"], "tint_amount": 0.35,
                     "bg": [plate("square_wide")],
                     "fg": [sprite("jar_full", 0.78, 0.55, 0.32),
                            {"type": "character", "id": "ved", "pose": "surprised", "x": 0.42, "y": 0.93, "h": 0.95, "enter": "none",
                             "acting": "none", "talk": False, "ground": False, "allow_outside_safe": True}]},
       "privacy": "public", "speaker": "ved", "assets_script": J + "assets.py", "scenes": S}
json.dump(job, open(J + "job.json", "w"), indent=1, ensure_ascii=False)
print("scenes", len(S))
