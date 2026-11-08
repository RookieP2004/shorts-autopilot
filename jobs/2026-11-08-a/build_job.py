"""2026-11-08-a: big-question "The prisoner's dilemma". Police-station cutaway (two interrogation rooms) + rival apple stalls
(Blender stills), 2D Ved and townspeople, a 2x2 payoff matrix that builds cell by cell.
python jobs/2026-11-08-a/build_job.py"""
import json, os, random, sys
sys.path.insert(0, os.getcwd())
from autopilot.stage import Stage

random.seed(11)
J = "jobs/2026-11-08-a/"
A = J + "assets/"
SRC = A if os.path.exists(A + "plate_market_two.json") else sys.argv[1]
ST = {n: Stage(SRC + f"plate_{n}.json") for n in ("station_wide", "station_left", "station_right", "market_two")}

OUT = {   # same town people as the market videos
    "ravi": {"skin": "#b97a55", "top": ["#7c2533", "kurta"], "bottom": ["#efe3c8", "trousers"], "hair": ["#2a2320", "curly"]},
    "tomas": {"skin": "#e2b48d", "hat": ["straw", "#e6c27a"], "top": ["#6fc3c0", "tshirt"], "bottom": ["#34425c", "shorts"], "build": "slim"},
    "seller": {"skin": "#c98e62", "build": "round", "hair": ["#1d1712", "short"], "hat": ["cap", "#2f6f8f"],
               "top": ["#e8e2d4", "shirt"], "apron": "#f6efe2", "bottom": ["#3a3e48", "trousers"]},
    "omar": {"skin": "#a0694a", "hat": ["fez", "#b03a2e"], "top": ["#f6efe2", "vest"], "bottom": ["#5a4636", "trousers"], "build": "round",
             "apron": "#f2b04a"},
    "amina": {"skin": "#8d5a3b", "hat": ["headscarf", "#d9534f"], "top": ["#f2b04a", "dress"], "necklace": "#6fc3c0",
              "earrings": "#f2b04a", "bag": "#8a5a3c", "hair": ["#140f0c", "long"]},
}
RX, TX, SY = -2.05, 2.05, 1.4      # suspects stand behind their tables


def plate(name, blur=0, **k):
    return {"type": "image", "path": A + f"plate_{name}.png", "x": 0.5, "y": 0.5, "w": 1.0, "enter": "none", "blur": blur, **k}

def fg(name):
    return {"type": "image", "path": A + f"fg_{name}.png", "x": 0.5, "y": 0.5, "w": 1.0, "enter": "none"}

def sprite(name, x, y, w, **k):
    return {"type": "image", "path": k.pop("path", A + name + ".png"), "x": x, "y": y, "w": w, "enter": k.pop("enter", "none"), **k}

def txt(t, y, size=96, **k):
    d = {"type": "text", "text": t, "font": "display", "x": 0.5, "y": y, "size": size, "max_w": 0.86,
         "stroke": "#0b0f12", "stroke_width": 7}
    d.update(k); return d

def person(set_, who, wx, wy, acting, walk=None, hops=None, **k):
    st = ST[set_]; p = st.place(wx, wy, "extra")
    L = {"type": "character", "id": "extra", "pose": acting[0][0], "x": p["x"], "y": p["y"], "h": p["h"], "enter": "none",
         "acting": acting, "talk": False, "rig_args": {"outfit": OUT[who]}, "_depth": wy, "allow_outside_safe": True}
    if walk: L["keys"] = st.walk(walk, p, "extra")
    if hops: L["hops"] = hops
    L.update(k); return L

def ved(set_, wx, wy, acting, walk=None, hops=None, **k):
    st = ST[set_]; p = st.place(wx, wy, "ved")
    L = {"type": "character", "id": "ved", "pose": acting[0][0], "x": p["x"], "y": p["y"], "h": p["h"], "enter": "none",
         "acting": acting, "_depth": wy, "allow_outside_safe": True}
    if walk: L["keys"] = st.walk(walk, p, "ved")
    if hops: L["hops"] = hops
    L.update(k); return L

def close_ved(acting, **k):
    return {"type": "character", "id": "ved", "pose": acting[0][0], "x": 0.5, "y": 0.8, "h": 1.06, "enter": "none",
            "acting": acting, "ground": False, "allow_outside_safe": True, **k}

def staged(base, behind=(), fgname=None, front=(), top=()):
    """plate, people behind the tables (far to near), the tables, people in front, then 2D on top."""
    out = list(base) + sorted(behind, key=lambda L: -L["_depth"]) + ([fg(fgname)] if fgname else []) \
        + sorted(front, key=lambda L: -L["_depth"]) + list(top)
    for L in out: L.pop("_depth", None)
    return out

F = "font-family='Poppins, DejaVu Sans, sans-serif' font-weight='800'"
AN = "font-family='Anton, DejaVu Sans, sans-serif'"

def tag(label, color="#f2b04a"):
    w = 60 + 34 * len(label)
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {w} 96'><rect x='4' y='4' width='{w-8}' height='88' rx='44' "
            f"fill='#f6efe2' stroke='#1a1410' stroke-width='6'/><circle cx='46' cy='48' r='16' fill='{color}'/>"
            f"<text x='{(w+40)/2}' y='64' text-anchor='middle' font-size='44' fill='#1a1410' {F}>{label}</text></svg>")

def stamp(word, color="#d9534f"):
    W = 140 + 70 * len(word)
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {W} 200'><rect x='10' y='10' width='{W-20}' height='180' rx='22' "
            f"fill='#f6efe2' fill-opacity='0.88' stroke='{color}' stroke-width='14'/><rect x='30' y='30' width='{W-60}' height='140' rx='12' fill='none' "
            f"stroke='{color}' stroke-width='5'/><text x='{W/2}' y='140' text-anchor='middle' font-size='120' fill='{color}' {AN}>{word}</text></svg>")

# ---------------------------------------------------------------- the payoff matrix (cream card, fills cell by cell)
CELLS = {("S", "S"): ("1 YR", "1 YR", "#6fc3c0"), ("S", "B"): ("3 YRS", "FREE", "#f2b04a"),
         ("B", "S"): ("FREE", "3 YRS", "#f2b04a"), ("B", "B"): ("2 YRS", "2 YRS", "#d9534f")}

def matrix(show, hi=None):
    s = [f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 940 600'><rect width='940' height='600' rx='34' fill='#f6efe2' stroke='#1a1410' stroke-width='6'/>",
         f"<text x='615' y='46' text-anchor='middle' font-size='34' fill='#2d5a5e' {F}>TOMAS</text>",
         f"<text x='462' y='100' text-anchor='middle' font-size='30' fill='#1a1410' {F}>SILENT</text>",
         f"<text x='767' y='100' text-anchor='middle' font-size='30' fill='#1a1410' {F}>BETRAYS</text>",
         f"<text x='150' y='100' text-anchor='middle' font-size='34' fill='#7c2533' {F}>RAVI</text>",
         f"<text x='150' y='242' text-anchor='middle' font-size='30' fill='#1a1410' {F}>SILENT</text>",
         f"<text x='150' y='492' text-anchor='middle' font-size='30' fill='#1a1410' {F}>BETRAYS</text>"]
    for (r, c), (rv, tv, col) in CELLS.items():
        x = 320 if c == "S" else 625; y = 125 if r == "S" else 375
        on = (r, c) in show
        s.append(f"<rect x='{x}' y='{y}' width='285' height='210' rx='22' fill='{col if on else '#e3d8c4'}' "
                 f"stroke='{'#1a1410' if (r, c) == hi else 'none'}' stroke-width='10'/>")
        if on:
            s.append(f"<text x='{x+20}' y='{y+85}' font-size='26' fill='#7c2533' {F}>RAVI</text>"
                     f"<text x='{x+265}' y='{y+88}' text-anchor='end' font-size='40' fill='#1a1410' {F}>{rv}</text>"
                     f"<text x='{x+20}' y='{y+160}' font-size='26' fill='#2d5a5e' {F}>TOMAS</text>"
                     f"<text x='{x+265}' y='{y+163}' text-anchor='end' font-size='40' fill='#1a1410' {F}>{tv}</text>")
    return "".join(s) + "</svg>"

def mx(show, hi=None, **k):
    return {"type": "image", "svg": matrix(show, hi), "w": 0.8, "x": 0.5, "y": 0.225, "enter": k.pop("enter", "none"), **k}

def logic_card(head, l1, l2, color):
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 900 330'><rect width='900' height='330' rx='34' fill='#f6efe2' "
            f"stroke='#1a1410' stroke-width='6'/><text x='450' y='78' text-anchor='middle' font-size='46' fill='{color}' {F}>{head}</text>"
            f"<text x='60' y='170' font-size='36' fill='#1a1410' {F}>{l1[0]}</text><text x='840' y='170' text-anchor='end' font-size='40' fill='#46965a' {F}>{l1[1]}</text>"
            f"<text x='60' y='260' font-size='36' fill='#1a1410' {F}>{l2[0]}</text><text x='840' y='260' text-anchor='end' font-size='40' fill='#46965a' {F}>{l2[1]}</text></svg>")

def price(n, col):
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 300 170'><path d='M40 10 H290 V160 H40 L6 85 Z' fill='#f6efe2' stroke='#1a1410' stroke-width='6'/>"
            f"<circle cx='42' cy='85' r='12' fill='#1a1410'/><circle cx='120' cy='85' r='34' fill='#f2b04a' stroke='#b8822a' stroke-width='6'/>"
            f"<text x='225' y='118' text-anchor='middle' font-size='96' fill='{col}' {AN}>{n}</text></svg>")

def flip_tag(x, y, old, new, at):
    """price tag card-flip: old shrinks to 0 width, new grows from 0."""
    return [{"type": "image", "svg": price(old, "#1a1410"), "w": 0.26, "x": x, "y": y, "enter": "pop", "at": 0.2, "until": at + 0.18, "exit": "fade",
             "keys": [{"t": 0, "sx": 1}, {"t": at - 0.2, "sx": 1}, {"t": at, "sx": 0.02}]},
            {"type": "image", "svg": price(new, "#d9534f"), "w": 0.26, "x": x, "y": y, "enter": "none", "at": at, "sfx": "click",
             "keys": [{"t": 0, "sx": 0.02}, {"t": 0.2, "sx": 1}]}]

def move(col, label, who_col):
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 150 150'><circle cx='75' cy='75' r='66' fill='{col}' stroke='#1a1410' stroke-width='6'/>"
            f"<text x='75' y='92' text-anchor='middle' font-size='46' fill='#f6efe2' {F}>{label}</text></svg>")

S = []
# 1. hook, wide: both rooms, the question on screen at frame 0; Ved walks into the corridor between the rooms
S.append({"say": "Why would two smart people both pick the *worse* option?", "caption_y": 0.32,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.4, "zoom": 1.06, "focus": [0.5, 0.52]}]},
          "layers": staged([plate("station_wide")],
                           [person("station_wide", "ravi", RX, SY, [["idle", 0], ["shrug", 1.6]]),
                            person("station_wide", "tomas", TX, SY, [["idle", 0], ["shrug", 2.0]])], "station_wide",
                           [ved("station_wide", 0.0, -2.8, [["explain", 0], ["think", 1.6]], walk=[(0, -2.6, -3.3), (1.2, 0.0, -2.8)])],
                           [txt("WHY WOULD TWO SMART PEOPLE PICK THE *WORSE* OPTION?", 0.165, 88, enter="none")])})
# 2. close-up: name it
S.append({"say": "It's called the *prisoner's dilemma*.", "transition": "cut", "caption_y": 0.64,
          "layers": [plate("station_left", blur=10, keys=[{"t": 0, "scale": 1.35}, {"t": 2.2, "scale": 1.4}]),
                     close_ved([["warm", 0], ["point", 0.8]]),
                     {"type": "image", "svg": stamp("PRISONER'S DILEMMA", "#f2b04a"), "w": 0.8, "x": 0.5, "y": 0.17, "rot": -5, "at": 0.5,
                      "keys": [{"t": 0, "scale": 2.0, "opacity": 0}, {"t": 0.18, "scale": 1.0, "opacity": 1, "ease": "out"}], "sfx": "boom"}]})
# 3. wide: two suspects, separate rooms, no talking
rx, ry = ST["station_wide"].point(RX, SY, 2.25); tx, ty = ST["station_wide"].point(TX, SY, 2.25)
dx, dy = ST["station_wide"].point(0, 0.3, 2.4)
nochat = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 200'><path d='M40 50 h120 a20 20 0 0 1 20 20 v50 a20 20 0 0 1 -20 20 h-70 l-30 28 v-28 h-20 "
          "a20 20 0 0 1 -20 -20 v-50 a20 20 0 0 1 20 -20 z' fill='#f6efe2' stroke='#1a1410' stroke-width='8'/><circle cx='100' cy='100' r='88' fill='none' "
          "stroke='#d9534f' stroke-width='16'/><line x1='38' y1='162' x2='162' y2='38' stroke='#d9534f' stroke-width='16'/></svg>")
S.append({"say": "Two suspects, separate rooms. They *can't* talk.", "transition": "slide_left", "caption_y": 0.3,
          "camera": {"keys": [{"t": 0, "zoom": 1.04, "focus": [0.5, 0.5]}, {"t": 3.2, "zoom": 1.1, "focus": [0.5, 0.52]}]},
          "layers": staged([plate("station_wide")],
                           [person("station_wide", "ravi", RX, SY, [["idle", 0], ["hold", 1.0]]),
                            person("station_wide", "tomas", TX, SY, [["idle", 0], ["hold", 1.4]])], "station_wide", [],
                           [{"type": "image", "svg": tag("RAVI", "#7c2533"), "w": 0.24, "x": rx, "y": ry - 0.075, "enter": "pop", "at": 0.3, "sfx": "pop"},
                            {"type": "image", "svg": tag("TOMAS", "#6fc3c0"), "w": 0.27, "x": tx, "y": ty - 0.075, "enter": "pop", "at": 0.8, "sfx": "pop"},
                            {"type": "image", "svg": nochat, "w": 0.2, "x": dx, "y": dy - 0.03, "enter": "zoom", "at": 2.1, "sfx": "boom"},
                            txt("SEPARATE *ROOMS*", 0.14, 96, enter="pop", at=0.2)])})
# 4-6. the matrix builds cell by cell over the wide
S.append({"say": "If both stay *silent*: one year each.", "transition": "cut", "caption_y": 0.44,
          "layers": staged([plate("station_wide", blur=6)],
                           [person("station_wide", "ravi", RX, SY, [["idle", 0], ["happy", 1.2]]),
                            person("station_wide", "tomas", TX, SY, [["idle", 0], ["happy", 1.2]])], "station_wide", [],
                           [mx(set()), mx({("S", "S")}, ("S", "S"), at=0.9, enter="pop", sfx="pop")])})
S.append({"say": "If one *betrays*, he walks free, and the other gets *three*.", "transition": "cut", "caption_y": 0.44,
          "layers": staged([plate("station_wide", blur=6)],
                           [person("station_wide", "ravi", RX, SY, [["idle", 0], ["cheer", 0.9], ["sad", 2.6]], hops=[[0.9, 0.04, 0.45]]),
                            person("station_wide", "tomas", TX, SY, [["idle", 0], ["sad", 0.9], ["cheer", 2.6]], hops=[[2.6, 0.04, 0.45]])],
                           "station_wide", [],
                           [mx({("S", "S")}), mx({("S", "S"), ("B", "S")}, ("B", "S"), at=0.8, enter="pop", sfx="pop"),
                            mx({("S", "S"), ("B", "S"), ("S", "B")}, ("S", "B"), at=2.5, enter="pop", sfx="pop")])})
S.append({"say": "If both betray: *two* years each.", "transition": "cut", "caption_y": 0.44,
          "layers": staged([plate("station_wide", blur=6)],
                           [person("station_wide", "ravi", RX, SY, [["idle", 0], ["sad", 1.0]]),
                            person("station_wide", "tomas", TX, SY, [["idle", 0], ["sad", 1.0]])], "station_wide", [],
                           [mx({("S", "S"), ("B", "S"), ("S", "B")}), mx(set(CELLS), ("B", "B"), at=0.8, enter="pop", sfx="pop")])})
# 7. room 1 medium: Ravi's logic
S.append({"say": "Ravi thinks: whatever Tomas does, betraying means *less* time.", "transition": "slide_left", "caption_y": 0.36,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.6, "zoom": 1.07, "focus": [0.5, 0.52]}]},
          "layers": staged([plate("station_left")],
                           [person("station_left", "ravi", RX, SY, [["shrug", 0], ["explain", 1.8], ["point", 3.0]])], "station_left",
                           [ved("station_left", -3.0, -0.6, [["think", 0], ["explain", 1.6], ["point", 3.0]])],
                           [{"type": "image", "svg": logic_card("RAVI'S LOGIC", ("Tomas silent? Betray:", "FREE, not 1"),
                                                                ("Tomas betrays? Betray:", "2, not 3"), "#7c2533"),
                             "w": 0.84, "x": 0.5, "y": 0.17, "enter": "pop", "at": 0.3, "sfx": "pop"},
                            txt("BETRAY *WINS* EITHER WAY", 0.285, 64, enter="pop", at=2.6, sfx="ding")])})
# 8. room 2 medium: Tomas thinks the same
S.append({"say": "Tomas thinks the *exact same* thing.", "transition": "slide_left", "caption_y": 0.36,
          "layers": staged([plate("station_right")],
                           [person("station_right", "tomas", TX, SY, [["shrug", 0], ["point", 1.2]])], "station_right", [],
                           [{"type": "image", "svg": logic_card("TOMAS'S LOGIC", ("Ravi silent? Betray:", "FREE, not 1"),
                                                                ("Ravi betrays? Betray:", "2, not 3"), "#2d5a5e"),
                             "w": 0.84, "x": 0.5, "y": 0.17, "enter": "pop", "at": 0.2, "sfx": "pop"}])})
# 9. wide: both betray, both lose
S.append({"say": "So both betray, and get *two* years instead of one.", "transition": "cut", "caption_y": 0.5,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 3.2, "zoom": 1.05, "focus": [0.5, 0.5]}]},
          "layers": staged([plate("station_wide", blur=6)],
                           [person("station_wide", "ravi", RX, SY, [["point", 0], ["sad", 1.4]]),
                            person("station_wide", "tomas", TX, SY, [["point", 0], ["sad", 1.4]])], "station_wide", [],
                           [mx(set(CELLS), ("B", "B")),
                            {"type": "shape", "shape": "ring", "x": 0.493, "y": 0.191, "w": 0.3, "h": 0.3, "color": "#46965a", "stroke_width": 10,
                             "at": 2.4, "enter": "zoom", "sfx": "pop"},
                            txt("BOTH *LOSE*", 0.41, 92, enter="pop", at=1.3, sfx="boom")])})
# 10. comic beat: reaction cut-away (the "W chews / L nibbles" rating trend, bent to game theory)
S.append({"dur": 1.9, "transition": "cut", "captions": False,
          "layers": [plate("station_right", blur=10, keys=[{"t": 0, "scale": 1.35}]), dict(close_ved([["idle", 0]]), acting="none")],
          "beat": {"kind": "side_eye", "at": 0.1, "dur": 1.6, "zoom": 1.12, "focus": [0.5, 0.42],
                   "text": "The logic: *W chews*.\nThe result: *L nibbles*.", "text_y": 0.18}})
# 11. market: two rival stalls in a price war
mk = ST["market_two"]
lx, ly = mk.point(-1.55, -0.55, 0.45); rx2, ry2 = mk.point(1.55, -0.55, 0.45)
S.append({"say": "Same trap in a price war: both shops cut prices. Both earn *less*.", "transition": "slide_left", "caption_y": 0.29,
          "camera": {"keys": [{"t": 0, "zoom": 1.0, "focus": [0.5, 0.5]}, {"t": 4.2, "zoom": 1.06, "focus": [0.5, 0.52]}]},
          "layers": staged([plate("market_two")],
                           [person("market_two", "seller", -1.55, 0.55, [["wave", 0], ["give", 1.4], ["sad", 3.6]]),
                            person("market_two", "omar", 1.55, 0.55, [["wave", 0], ["give", 1.8], ["sad", 3.6]])], "market_two",
                           [person("market_two", "amina", 0.3, -1.2, [["idle", 0], ["happy", 2.4]], walk=[(0, 2.6, -1.4), (2.0, 0.3, -1.2)])],
                           [txt("PRICE *WAR*", 0.12, 104, enter="pop", at=0.2, sfx="whoosh")]
                           + flip_tag(lx, ly - 0.02, "10", "8", 1.5) + flip_tag(rx2 - 0.05, ry2 - 0.02, "10", "6", 2.1)
                           + [{"type": "shape", "shape": "arrow", "x": 0.5, "y": 0.22, "w": 0.16, "h": 0.05, "rotate": 90, "color": "#d9534f",
                              "at": 3.4, "enter": "pop", "sfx": "ding"}])})
# 12. the way out: a 1980 computer tournament
S.append({"say": "The way out? Repeat the game. In a *1980* computer tournament, the winner was simple:", "transition": "fade",
          "caption_y": 0.44, "bg": {"type": "radial", "colors": ["#24343d", "#0e1418"], "pattern": "grid"},
          "layers": [txt("REPEAT THE *GAME*", 0.13, 96, enter="pop", at=0.1, sfx="pop"),
                     sprite("computer", 0.3, 0.62, 0.36, at=1.6, keys=[{"t": 0, "y": 1.1}, {"t": 0.5, "y": 0.62, "ease": "bounce"}], sfx="whoosh"),
                     sprite("computer", 0.7, 0.62, 0.36, at=1.9, flip=True, keys=[{"t": 0, "y": 1.1}, {"t": 0.5, "y": 0.62, "ease": "bounce"}]),
                     {"type": "counter", "from": 1900, "to": 1980, "count_dur": 0.9, "commas": False, "at": 2.2, "x": 0.5, "y": 0.25, "size": 160,
                      "color": "#f2b04a", "enter": "pop", "sfx": "ding"},
                     {"type": "text", "text": "VS", "font": "display", "x": 0.5, "y": 0.6, "size": 90, "color": "#f6efe2",
                      "stroke": "#0b0f12", "stroke_width": 6, "enter": "zoom", "at": 2.6}]})
# 13. tit for tat: be nice first, then copy
moves = []
ME = [("#46965a", "NICE"), ("#46965a", "NICE"), ("#d9534f", "MEAN"), ("#46965a", "NICE")]
THEM = [("#46965a", "NICE"), ("#d9534f", "MEAN"), ("#46965a", "NICE"), ("#46965a", "NICE")]
for i in range(4):
    x = 0.2 + i * 0.2
    t = 0.3 + i * 0.75
    moves.append({"type": "image", "svg": move(*THEM[i], None), "w": 0.15, "x": x, "y": 0.2, "enter": "pop", "at": t, "sfx": "pop"})
    moves.append({"type": "image", "svg": move(*ME[i], None), "w": 0.15, "x": x, "y": 0.62, "enter": "pop", "at": t + 0.3})
    if i > 0:
        moves.append({"type": "shape", "shape": "arrow", "x": x - 0.1, "y": 0.41, "w": 0.34, "h": 0.022, "rotate": 75,
                      "color": "#f2b04a", "at": t + 0.15, "enter": "fade"})
S.append({"say": "be nice first, then *copy* whatever the other player did last.", "transition": "cut", "caption_y": 0.41,
          "bg": {"type": "radial", "colors": ["#24343d", "#0e1418"], "pattern": "grid"},
          "layers": [txt("THEM", 0.11, 60, font="body", color="#6fc3c0", enter="none"),
                     txt("WINNER", 0.73, 60, font="body", color="#f2b04a", enter="none")] + moves})
# 14. payoff close-up
S.append({"say": "*Tit for tat*. Trust first, but keep *score*.", "transition": "cut", "caption_y": 0.64,
          "layers": [plate("station_wide", blur=10, keys=[{"t": 0, "scale": 1.3}, {"t": 3.5, "scale": 1.38}]),
                     close_ved([["warm", 0], ["explain", 1.2], ["smirk", 2.4]]),
                     txt("TIT FOR *TAT*", 0.16, 150, enter="zoom", at=0.1, sfx="ding")]})

SOURCES = ["https://www.econlib.org/library/Enc/PrisonersDilemma.html",
           "https://www.geeksforgeeks.org/?p=141634",
           "https://praxis.ac.in/tit-for-tat-how-a-1980-game-theory-experiment-proved-co-operation-triumphs-above-all/"]
job = {"id": "2026-11-08-a", "title": "Why do smart people both make the worse choice? 🤝",
       "description": "The prisoner's dilemma in under a minute: why two people acting rationally can both end up worse off, "
                      "why price wars happen, and the simple strategy that won a 1980 computer tournament (tit for tat).\n\n"
                      "Sources:\n" + "\n".join(SOURCES),
       "tags": ["prisoners dilemma", "game theory", "tit for tat", "economics explained", "psychology", "decision making",
                "price war", "nash equilibrium", "explained simply"],
       "hashtags": ["#gametheory", "#economics"],
       "meta": {"format": "big-question", "topic": "the prisoner's dilemma (game theory)", "hook": "question", "idea_source": "backlog",
                "characters": ["ved", "extra"], "sources": SOURCES,
                "humour": {"trend": "'W chews / L nibbles' food-rating videos (KYM weekly roundup, 2026-11-06), as a text card",
                           "beat": "side_eye", "scene": 10}},
       "privacy": "public", "speaker": "ved", "assets_script": J + "assets.py", "scenes": S}
json.dump(job, open(J + "job.json", "w"), indent=1, ensure_ascii=False)
print("scenes", len(S), "using", SRC)
